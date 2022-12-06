import re
from lxml import etree as ET
from lexicon import *

# ====
# Satz
# ====

def Satz(addto, juncture = None):
  checkAgreement(addto)
  # abbreviations
  role = addto.find(f'*[@role="{juncture}"]')
  # subordinate clauses
  if juncture in Subjunktionen:
    node = Subjunktionsatz(addto, juncture)
  elif juncture in Satzpartizipien + Satzpräpositionen:
    node = Präpositionssatz(addto, juncture)
  elif juncture in Präpositionen or role is not None:
    node = Komplementsatz(addto, juncture)
  elif juncture is None:
    node = Relativsatz(addto)
  checkVorfeld(addto, node)
  return node

def Prädikat(clause, verb = None):
  if verb is None or verb in Adjektive + Adverbien + list(Präpositionen.keys()):
    Prädikativ(clause, verb)
  else:
    Verb(clause, verb)

# =====
# Sätze
# =====

def Start():
  clause = ET.Element('SATZ', attrib = {'kind': 'Hauptsatz', 'tense': 'Präsens'})
  ET.SubElement(clause, 'VORFELD')
  return clause

def Hauptsatz(addto):
  # Hauptsatz in coordination
  tense = addto.get('tense')
  clause = ET.SubElement(addto, 'SATZ', attrib = {'kind': 'Hauptsatz', 'tense': tense})
  ET.SubElement(clause, 'VORFELD')
  return clause

def Subjunktionsatz(clause, juncture):
  # includes a vorfeld, although there is no evidence for it
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Subjunktionsatz', 'tense': tense})
  ET.SubElement(newclause, 'VORFELD')
  return newclause

def Präpositionssatz(clause, juncture):
  # special set of prepositions: um ohne anstatt etc.
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Präpositionssatz', 'tense': tense})
  ET.SubElement(newclause, 'VORFELD')
  # special case of 'um'
  if juncture == 'um':
    Infinit(node)
  return newclause

def Relativsatz(addto):
  # can both be attributiv and adverbial
  tense = upClause(addto).get('tense')
  predicative = addto.find('.//PRÄDIKATIV/PHRASE')
  if predicative is not None:
    node = ET.SubElement(predicative, 'ATTRIBUT')
  elif addto.tag == 'SATZ':
    node = ET.SubElement(addto, 'ADVERBIALE')
  elif addto.tag == 'PHRASE':
    node = ET.SubElement(addto, 'ATTRIBUT')
  clause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Relativsatz', 'tense': tense})
  ET.SubElement(clause, 'VORFELD')
  return clause

def Komplementsatz(clause, role):
  # präposition-komplementsatz
  if role in Präpositionen:
    node = leaf = ET.SubElement(clause, 'ADVERBIALE')
    juncture = role
  # komplementsatz
  else:
    # find role and go to tip of branch
    node = clause.find(f'*[@role="{role}"]')
    leaf = node.xpath('.|.//*[not(name()="REFLEXIV")]')[-1]
    # get the prepositional juncture from role, if available
    juncture = leaf.get('case')
  # --- treat prepositions
  correlative = None
  if juncture in Präpositionen:
    # 'anhand dessen' type construction, seem grammaticalised
    if Präpositionen[juncture] == 'Genitiv':
      ET.SubElement(leaf, 'JUNKTOR').text = juncture + ' dessen'
    # make correlative
    else:
      correlative = ET.SubElement(leaf, 'KORRELAT')
      correlative.text = 'da' + addR(juncture) + juncture
  # --- add clause
  tense = clause.get('tense')
  tense = upClause(clause).get('tense') if tense is None else tense
  newclause = ET.SubElement(leaf, 'SATZ', attrib = {'kind': 'Komplementsatz', 'tense': tense})
  ET.SubElement(newclause, 'VORFELD')
  # --- position: if vorfeld already filled: clause to back, but correlative stays
  vorfeld = clause.find('VORFELD')
  if vorfeld is None or (vorfeld is not None and len(vorfeld) != 0):
    clause.append(node)
    if correlative is not None:
      predicate = clause.find('PRÄDIKAT')
      predicate.addprevious(correlative)
      correlative.set('role', role)
      node.set('role', role)
  # --- agreement, in case this clause is the nominative
  passPersonNumber(newclause, juncture, '3', 'Singular')
  return newclause

# ===========
# Prädikation
# ===========

def Verb(clause, verb):
  clause.set('verb', verb)
  # --- roles ---
  # start with a default nominative role, except when Nominative listed in dictionary
  if not 'Nominativ' in Verben.get(verb, {}).get('Rollen', {}).values():
    nominative = verb.capitalize() + 'de'
    ET.SubElement(clause, 'ARGUMENT', attrib = {'role': nominative, 'case': 'Nominativ'})
  # then go through all roles listed in the lexicon
  if Verben.get(verb, {}).get('Rollen', False):
    for role,case in Verben[verb]['Rollen'].items():
        ET.SubElement(clause, 'ARGUMENT', attrib = {'role': role, 'case': case})
  # obligatory reflexive verbs
  if Verben.get(verb, {}).get('Reflexiv', False):
    nominative = clause.find('*[@case="Nominativ"]')
    ET.SubElement(nominative, 'REFLEXIV', attrib = {'case': 'Akkusativ'})
  # --- verb ---
  predicate = ET.SubElement(clause, 'PRÄDIKAT')
  lexeme = ET.SubElement(predicate, 'VERB')
  # lexicalised preverbs from lexicon are split
  if Verben.get(verb, {}).get('Präverb', False):
    ET.SubElement(lexeme, 'PRÄVERBIALE').text = Verben[verb]['Präverb'] + '+'
    verb = Verben[verb]['Stamm']
  # lexicalised nominal predicatives from lexicon are split
  if Verben.get(verb, {}).get('Prädikat', False):
    predicative = ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikat', 'case': 'Akkusativ'})
    phrase = Phrase(predicative, 'Prädikat')
    Referent(phrase, Verben[verb]['Prädikat'])
    verb = Verben[verb]['Stamm']
  # add verb to info
  lexeme.set('verb', verb)

def Prädikativ(clause, predicate = None):
  verb = clause.get('verb')
  # --- subject and predicate
  subject = ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  predicative = ET.SubElement(clause, 'PRÄDIKATIV')
  # locational predication
  if predicate in Präpositionen:
    predicative.set('role', 'Ort')
    predicative.set('case', predicate)
  # adjectival predication
  elif predicate in Adjektive + Adverbien:
    adverbial = ET.SubElement(predicative, 'ADVERBIALE')
    tag = 'ADVERB' if predicate in Adverbien else 'ADJEKTIV'
    ET.SubElement(adverbial, tag).text = predicate
  # nominal predication
  else:
    predicative.set('role', 'Prädikat')
    # special existential clause 'es gibt'
    if verb == 'geben':
      predicative.set('case', 'Akkusativ')
      subject.tag ='SUBJEKTERSATZ'
      subject.text = 'es'
      passPersonNumber(subject, 'Nominativ', '3', 'Singular')
    else:
      predicative.set('case', 'Nominativ')
  # --- verb ---
  verbnode = ET.SubElement(clause, 'PRÄDIKAT')
  ET.SubElement(verbnode, 'VERB', attrib = {'verb': verb})

# ============
# Satzstruktur
# ============

def Frage(clause):
  clause.set('mood', 'Frage')

def Imperativ(clause):
  clause.set('mood', 'Imperativ')

def Thetisch(clause):
  # empty vorfeld
  clause.set('discourse', 'Thetisch')

def Unbestimmt(clause):
  # ob-sentences
  clause.set('truth', 'Unbestimmt')

def Vorn(clause):
  # move verb or predicative to vorfeld 
  clause.set('predicate', 'Vorfeld')

def Infinit(clause):
  # make subordinate clause infinite
  clause.set('tense', 'Infinit')

def Kopula(clause, copula):
  clause.set('verb', copula)

# ================
# Ereignisstruktur
# ================

def Präsens(clause):
  clause.set('tense', 'Präsens')

def Präteritum(clause):
  clause.set('tense', 'Präteritum')

def Konjunktiv(clause):
  clause.set('tense', 'Konjunktiv')

def Irrealis(clause):
  clause.set('tense', 'Irrealis')

def Modalverb(clause, modal):
  addlightverb(clause, modal, 'Infinitiv', 'Modalverb')

def Vorgangspassiv(clause, demoted = 'von'):
  passiv(clause, 'werden', 'Partizip', 'Vorgangspassiv', 'Akkusativ', demoted)

def Zustandspassiv(clause, demoted = 'von'):
  passiv(clause, 'sein', 'Partizip', 'Zustandspassiv', 'Akkusativ', demoted)

def Rezipientenpassiv(clause, demoted = 'von'):
  passiv(clause, 'bekommen', 'Partizip', 'Rezipientenpassiv', 'Dativ', demoted)

def Modalpassiv(clause, demoted = 'von'):
  passiv(clause, 'sein', 'zu-Infinitiv', 'Modalpassiv', 'Akkusativ', demoted)

def Permissivpassiv(clause, demoted = 'von'):
  passiv(clause, 'lassen', 'Infinitiv', 'Permissivpassiv', 'Akkusativ', demoted, reflexive = True)

def Perfekt(clause):
  # get info
  node = clause.find('PRÄDIKAT')[-1]
  verb = node.get('verb') if node.find('PRÄVERBIALE') is None else clause.get('verb') 
  # default to auxiliary 'haben', when not otherwise noted in dictionary
  auxiliary = Verben.get(verb, {}).get('Perfekt', 'haben')
  # Ersatzinfinitiv
  if node.tag == 'MODALVERB':
    addlightverb(clause, auxiliary, 'Infinitiv', 'Perfekt')
    # set flag for ordering with Ersatzinfinitiv
    clause.set('cluster', 'Ersatzinfinitiv')
  # special participle with Vorgangspassiv
  elif node.tag == 'VORGANGSPASSIV':
    addlightverb(clause, auxiliary, 'Partizip', 'Perfekt', form = 'worden')
  # Regular perfect
  else:
    addlightverb(clause, auxiliary, 'Partizip', 'Perfekt')

def ReflexivErlebniskonversiv(clause):
  # get verb to find junture from lexicon
  verb = clause.get('verb')
  juncture = Verben[verb]['Konversiv']
  # change arguments
  for node in clause.findall('ARGUMENT'):
    leaf = node.xpath('.|.//*[not(name()="REFLEXIV")]')[-1]
    if leaf.get('case') == 'Nominativ':
      ET.SubElement(node, 'ERLEBNISKONVERSIV', attrib = {'case': juncture})
    if leaf.get('case') == "Akkusativ":
      ET.SubElement(node, 'ERLEBNISKONVERSIV', attrib = {'case': 'Nominativ'})
      ET.SubElement(node, 'REFLEXIV', attrib = {'case': 'Akkusativ'})
      # default order nominative first
      clause.insert(1, node)

def Möglichkeitsdesubjektiv(clause):
  addlightverb(clause, 'geben', 'zu-Infinitiv', 'Möglichkeitsdesubjektiv')
  # remove nominative
  for node in clause.findall('ARGUMENT'):
    leaf = node.xpath('.|.//*[not(name()="REFLEXIV")]')[-1]
    if leaf.get('case') == 'Nominativ':
      clause.remove(node)
  # Subjektersatz
  vorfeld = clause.find('VORFELD')
  es = ET.Element('SUBJEKTERSATZ')
  es.text = 'es'
  if len(vorfeld) == 0:
    vorfeld.append(es)
  else:
    vorfeld.addnext(es)
  # verb agreement
  clause.set('person', '3')
  clause.set('number', 'Singular')

# ======
# Phrase
# ======

def Phrase(addto, juncture = None):
  checkAgreement(addto)
  # abreviations
  role = addto.find(f'*[@role="{juncture}"]')
  # possibilities
  if role is not None:
    node = Argumentphrase(addto, juncture)
  elif addto.tag == 'SATZ':
    node = Adverbialphrase(addto, juncture)
  elif addto.tag == 'PHRASE':
    node = Attributphrase(addto, juncture)
  elif addto.tag == 'KOORDINATION':
    node = Phrasenkoordination(addto, juncture)
  checkVorfeld(addto, node)
  return node

def Referent(phrase, referent = None):
  # with empty head, gender is needed
  if referent in list('mnfp'):
    Genuskopf(phrase, referent)
  # insert personal pronoun
  elif referent[:1] in list('012'):
    Pronomen(phrase, referent)
  # make reference to another referent
  elif phrase.get('full') is None and (referent in Teilnehmer or referent == 'e'):
    Anapher(phrase, referent)
  # insert noun
  else:
    Nomen(phrase, referent)

# =======
# Phrasen
# =======

def Argumentphrase(clause, role = None):
  # also includes prädikativ here
  argument = clause.find(f'*[@role="{role}"]')
  # go to tip of branch to add stuff
  leaf = argument.xpath('.|.//*[not(name()="REFLEXIV")]')[-1]
  # get the prepositional juncture, if available
  case = leaf.get('case')
  if case in Präpositionen:
    ET.SubElement(leaf, 'JUNKTOR').text = case
    # special case assignment for governed prepositions
    if case in ['an', 'in', 'auf', 'über'] and role != 'Ort':
      case = 'Akkusativ'
    else:
      case = Präpositionen[case]
  # add phrase
  phrase = ET.SubElement(leaf, 'PHRASE', attrib = {'case': case})
  # reorder node
  predicate = clause.find('PRÄDIKAT')
  predicative = clause.find('PRÄDIKATIV')
  if role == 'Subjekt' and predicative is not None:
    predicative.addprevious(argument)
  else:
    predicate.addprevious(argument)
  # return phrase for further processing
  return phrase

def Adverbialphrase(clause, connection = None):
  # prepare node
  adverbial = ET.Element('ADVERBIALE')
  # prepositionphrase
  if connection is not None:
    ET.SubElement(adverbial, 'JUNKTOR').text = connection
    phrase = ET.SubElement(adverbial, 'PHRASE', attrib = {'case': Präpositionen[connection]})
  # No juncture then measure-phrase in accusative, e.g. 'den ganzen Tag'
  else:
    phrase = ET.SubElement(adverbial, 'PHRASE', attrib = {'case': 'Akkusativ'})
  # positioning node
  predicate = clause.find('PRÄDIKAT')
  if predicate is None:
    clause.append(adverbial)
  elif connection in ['als', 'wie']:
    clause.append(adverbial)
  else:
    predicate.addprevious(adverbial)
  # return phrase for further processing
  return phrase

def Attributphrase(phrase, connection = None):
  # prepare node
  attribute = ET.Element('ATTRIBUT')
  # prepositionphrase
  if connection is not None:
    ET.SubElement(attribute, 'JUNKTOR').text = connection
    newphrase = ET.SubElement(attribute, 'PHRASE', attrib = {'case': Präpositionen[connection]})
  # Genitive when no juncture
  else:
    newphrase = ET.SubElement(attribute, 'PHRASE', attrib = {'case': 'Genitiv'})
  # simply add to end of phrase
  phrase.append(attribute)
  return newphrase

def Phrasenkoordination(coordination, juncture):
  # only for whole-phrase koordinatino: link to node above, then move into coordination
  addto = coordination.getparent().getparent()
  phrase = Phrase(addto, juncture)
  coordination.append(phrase.getparent())
  return phrase

# ==========
# Referenten
# ==========

def Genuskopf(phrase, referent):
  # adjective can be used as head 
  gender = Genera[referent] if len(referent) == 1 else referent
  # in relative clause, gender can be used for 'freier relativsatz'
  kind = upClause(phrase).get('kind')
  position = upSubClause(phrase).tag.capitalize()
  if kind == 'Relativsatz' and position == 'Vorfeld':
    Anapher(phrase, gender)
  # else insert nodes
  else:
    ET.SubElement(phrase, 'DETERMINATIV')   
    ET.SubElement(phrase, 'REFERENT')
    # set flags at phrase for phrasal agreement
    phrase.set('gender', gender)
    phrase.set('declension', 'stark')
    # add unnamed Teilnehmer
    Teilnehmer[gender] = gender
    # update local context within clause for reflexivity
    local = upClause(phrase).get('local')
    local = gender if local is None else local + ',' + gender
    # check verb agreement
    case = phrase.get('case')
    passPersonNumber(phrase, case, '3', gender)

def Pronomen(phrase, person):
  # get info from phrase
  case = phrase.get('case')
  number = phrase.get('gender')
  number = 'Singular' if number is None else number
  animacy = phrase.get('animacy')
  animacy = 'Unbelebt' if animacy is None else animacy
  # optionally, specify number as 'p', animacy as 'b'
  if len(person) > 1:
    number = 'Plural' if person[-1] == 'p' else 'Singular'
    animacy = 'Belebt' if person [-1] == 'b' else 'Unbelebt'
    person = person[:1]
  # personal pronouns
  if person in list('12'):
    node = ET.SubElement(phrase, 'PRONOMEN', attrib = {'person': person, 'number': number})
    node.text = Personalpronomina[number][person][case]
    gender = number
  # indefinite/interrogative pronouns
  elif person == '0':
    # info from clause
    mood = upClause(phrase).get('mood')
    position = upSubClause(phrase).tag.capitalize()
    # flags for agreement
    person = '3'
    number = 'Singular'
    # interrogative pronoun
    if mood == 'Frage' and position == 'Vorfeld':
      node = ET.SubElement(phrase, 'FRAGEPRONOMEN')
      gender = 'Maskulin'
      # check on preposition for correlative
      junctornode = phrase.getparent().find('JUNKTOR')
      junctor = junctornode.text if junctornode is not None else None
      if junctor in Präpositionen and animacy == 'Unbelebt':
        node.text = 'wo' + addR(junctor) + junctor
        junctornode.text = None
        junctornode.set('move', 'Korrelat')
      else:
        node.text = Fragepronomina[animacy][case]
    # indefinite pronoun
    else:
      node = ET.SubElement(phrase, 'INDEFINITPRONOMEN')
      if animacy == 'Belebt':
        gender = 'Maskulin'
        node.text = 'jemand' + Quantorflexion['ein'][case][gender]
      elif animacy == 'Unbelebt':
        gender = 'Neutrum'
        node.text = 'etwas'
  # set flags at phrase
  phrase.set('gender', gender)
  phrase.set('animacy', animacy)
  # check verb agreement
  passPersonNumber(phrase, case, person, number)

def Anapher(phrase, referent):
  # get info from phrase
  case = phrase.get('case')
  # get gender and animacy from Teilnehmer
  gender = 'Neutrum' if referent == 'e' else Teilnehmer[referent]
  # can be plural ('+3') when marked at phrase
  number = phrase.get('gender')
  gender = number if number == 'Plural' else gender
  # update Teilnehmer
  Teilnehmer[referent] = gender
  # get local participants for reflexivitiy
  local = upClause(phrase).get('local')
  localreferents = local.split(',') if local is not None else []
  # get info from clause for relative pronouns
  kind = upClause(phrase).get('kind')
  position = upSubClause(phrase).tag.capitalize()
  # get junctor and animacy for correlative form
  animacy = belebtheit(referent)
  junctornode = phrase.getparent().find('JUNKTOR')
  junctor = junctornode.text if junctornode is not None else None
  # --- make new node ---
  node = ET.SubElement(phrase, 'ANAPHER', attrib = {'referent': referent})
  # reflexive pronoun
  if referent in localreferents:
    node.tag = 'REFLEXIVPRONOMEN'
    node.text = 'sich'
  # relative pronoun
  elif kind in ['Relativsatz', 'Komplementsatz'] and position == 'Vorfeld':
    # correlative relative with 'wo'
    if referent == 'e':
      node.tag = 'KORRELAT'
      if junctor in Präpositionen:
        node.text = 'wo' + addR(junctor) + junctor
        junctornode.text = None
      else:
        node.text = 'was'
    # relative
    else:
      node.tag = 'RELATIVPRONOMEN'
      # exception for 'das, was' free relatives
      if referent == 'Neutrum':
        node.text = 'was'
      # real relative pronoun
      else:
        node.text = Demonstrativpronomina[case][gender]
  # anaphoric pronoun
  else:
    # correlative anapher with 'da'
    if junctor in Präpositionen and (animacy == 'Unbelebt' or referent == 'e'):
      node.tag = 'KORRELAT'
      node.text = 'da' + addR(junctor) + junctor
      junctornode.text = None
    else:
      node.tag = 'ANAPHER'
      node.text = Anaphora[gender][case]
      # update local participants for reflexivity
      local = referent if local is None else local + ',' + referent
      upClause(phrase).set('local', local)
  # check verb agreement
  passPersonNumber(phrase, case, '3', gender)
  # set flags at phrase
  phrase.set('gender', gender)
  phrase.set('referent', referent)

def Nomen(phrase, referent):
  # get info from phrase
  case = phrase.get('case')
  number = phrase.get('gender')
  # find gender
  if referent in Teilnehmer:
    gender = Teilnehmer[referent]
    noundeclination = Substantive.get(referent, {}).get('Deklination', 'stark')
  elif referent in Substantive:
    gender = Substantive[referent]['Geschlecht']
    noundeclination = Substantive.get(referent, {}).get('Deklination', 'stark')
  # else assume that it is Neutrum, e.g. 'das Laufen'
  else:
    gender = 'Neutrum'
    noundeclination = 'stark'
  # override gender from phrase
  gender = gender if number is None else number
  # add new Teilnehmer to context
  Teilnehmer[referent] = gender
  # update local context within clause for reflexivity
  local = upClause(phrase).get('local')
  local = referent if local is None else local + ',' + referent
  upClause(phrase).set('local', local)
  # inflection of noun
  if gender == 'Plural':
    referent = Substantive[referent]['Plural']
    if case == 'Dativ' and referent[-1] not in list('ns'):
      referent = referent + 'n'
  # schwach: https://www.charlingua.de/n-deklination
  if gender in ['Maskulin', 'Neutrum']:
    if noundeclination == 'schwach' and case != 'Nominativ':
      referent = referent + 'en'
    elif noundeclination == 'stark' and case == 'Genitiv':
      referent = referent + 'es'
  # insert nodes
  ET.SubElement(phrase, 'DETERMINATIV')   
  ET.SubElement(phrase, 'REFERENT').text = referent
  # set flags at phrase for phrasal agreement
  phrase.set('gender', gender)
  phrase.set('declension', 'stark')
  phrase.set('referent', referent)
  # check verb agreement
  passPersonNumber(phrase, case, '3', gender)

# =============
# Determination
# =============

def Plural(phrase):
  phrase.set('gender', 'Plural')

def Belebt(phrase):
  phrase.set('animacy', 'Belebt')

def Bewegung(phrase):
  # to change case of wechselprepostions
  phrase.set('case', 'Akkusativ')

def Voll(phrase):
  # ignore anaphor and make a full noun phrase instead
  phrase.set('full', 'True')

def Definit(phrase):
  # get info from phrase
  case = phrase.get('case')
  gender = phrase.get('gender')
  determiner = phrase.find('DETERMINATIV')
  # ignore when there is no determiner
  if determiner is not None:
    # insert definite article
    ET.strip_elements(determiner, '*')
    ET.SubElement(determiner, 'ARTIKEL').text = Definitartikel[case][gender] 
    # set declension for agreement
    phrase.set('declension', 'schwach')

def Demonstrativ(phrase):
  # get info from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  determiner = phrase.find('DETERMINATIV')
  # ignore when there is no determiner
  if determiner is not None:
    # insert demonstrative
    ET.strip_elements(determiner, '*')
    ET.SubElement(determiner, 'DEMONSTRATIV').text = Demonstrativpronomina[case][gender]
    # set declension for agreement
    phrase.set('declension', 'schwach')
 
def Indefinit(phrase):
  # get info from phrase
  case = phrase.get('case')
  gender = phrase.get('gender')
  determiner = phrase.find('DETERMINATIV')
  # ignore when there is no determiner
  if determiner is not None:
    # insert article node
    ET.strip_elements(determiner, '*')
    node = ET.SubElement(determiner, 'ARTIKEL')
    # attributes for interrogative
    mood = upClause(phrase).get('mood')
    position = upSubClause(phrase).tag.capitalize()
    # interrogative choice
    if mood == 'Frage' and position == 'Vorfeld':
      node.tag = 'FRAGEWORT'
      node.text = 'welch' + Adjektivflexion['stark'][case][gender]
    # plural indefinite choice
    elif gender == 'Plural':
      node.text = 'einig' + Adjektivflexion['stark'][case][gender]
    # singular indefinite article
    else:
      node.text = 'ein' + Quantorflexion['ein'][case][gender]
    # set declension for agreement
    phrase.set('declension', 'gemischt')

def Quantor(phrase, quantor = None):
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender')
  determiner = phrase.find('DETERMINATIV')
  # ignore when there is no determiner
  if determiner is not None:
    # insert quantor node
    ET.strip_elements(determiner, '*')
    node = ET.SubElement(determiner, 'QUANTOR')
    # attributes for interrogative
    mood = upClause(phrase).get('mood')
    position = upSubClause(phrase).tag.capitalize()
    # interrogative quantor
    if mood == 'Frage' and position == 'Vorfeld':
      if gender == 'Plural':
        node.text = 'wie viel' + Quantorflexion['ein'][case]['Plural']
      else:
        node.text = 'wie viel' 
      declension = 'stark'
    # prepare the quantor as listed in the lexicon
    elif quantor in Quantoren:
      inflection = Quantoren[quantor]['Flexion']
      declension = Quantoren[quantor]['Deklination']
      node.text = quantor + Quantorflexion[inflection][case][gender]
    # set declension for adjective agreement
    phrase.set('declension', declension)

def Besitzer(phrase, referent = None): 
  # get info from phrase for agreement
  case = phrase.get('case')
  gender = phrase.get('gender') 
  determiner = phrase.find('DETERMINATIV')
  # attributes from clause
  mood = upClause(phrase).get('mood')
  kind = upClause(phrase).get('kind')
  position = upSubClause(phrase).tag.capitalize()
  # ignore when no determiner
  if determiner is not None:
    # insert possessive node
    ET.strip_elements(determiner, '*')
    node = ET.SubElement(determiner, 'POSSESSSIV')
    # interrogative pronoun
    if mood == 'Frage' and position == 'Vorfeld':
      node.text = 'wessen'
    # relative pronoun
    elif kind == 'Relativsatz' and position == 'Vorfeld':
      referentgender = Teilnehmer[referent]
      node.text = Demonstrativpronomina['Genitiv'][referentgender]
    # indefinite phrase 'von jemanden'
    elif referent[:1] == '0':
      besitzer = Phrase(phrase, 'von')
      Referent(besitzer, '0b')
    # personal pronoun
    elif referent[:1] in list('12'):
      person = referent[:1]
      number = 'Plural' if len(referent) > 1 else 'Singular'
      pronoun = Personalpronomina[number][person]['Attributiv']
      node.text = pronoun + Quantorflexion['ein'][case][gender]
    # Anaphoric pronooun
    else:
      person = '3'
      referentgender = Teilnehmer[referent]
      pronoun = Anaphora[referentgender]['Attributiv']
      node.text = pronoun + Quantorflexion['ein'][case][gender]
    # set declension for agreement
    phrase.set('declension', 'gemischt')

def Numerale(phrase, numeral):
  # ignore when no determiner
  determiner = phrase.find('DETERMINATIV')
  if determiner is not None:
    # 'ein' is the only numeral with declension
    if numeral == 'ein':
      # get attributes from phrase
      case = phrase.get('case')
      gender = phrase.get('gender')
      declension = phrase.get('declension')
      # add inflection
      numeral = numeral + Adjektivflexion[declension][case][gender]
    # insert numeral
    ET.SubElement(determiner, 'NUMERALE').text = numeral

def Fokuspartikel(phrase, particle):
  # add fokuspartikel to front
  fokus = ET.Element("FOKUSPARTIKEL")
  fokus.text = particle
  phrase.insert(0, fokus)

# ========
# Addendum
# ========

def Link(addto):
  checkAgreement(addto)
  if addto.tag == 'SATZ':
    node = ET.SubElement(addto, 'ADVERBIALE')
  elif addto.tag == 'PHRASE':
    node = ET.SubElement(addto, 'ATTRIBUT')
  checkVorfeld(addto, node)
  return node

def Addendum(addto, adword):
  if addto.tag == 'ADVERBIALE':
   Adverbiale(addto, adword)
  elif addto.tag == 'ATTRIBUT':
    Attribut(addto, adword)

# ======= 
# Addenda
# =======

def Attribut(attribute, adword):
  # find phrase
  phrase = upPhrase(attribute)
  # find referent for insertion
  head = phrase.xpath('REFERENT|ANAPHOR|REFLEXIVPRONOMEN|PRONOMEN')[0]
  # move node after referent when adverb, e.g. 'das Treffen gestern', also for 'selbst'
  if adword in Adverbien:
    head.addnext(attribute)
    ET.SubElement(attribute, "ADVERB").text = adword
  # else insert adjective before referent
  elif adword in Adjektive:
    head.addprevious(attribute)
    # adjective agreement
    agreement = adjectiveAgreement(phrase)
    # insert adjective
    ET.SubElement(attribute, "ADJEKTIV").text = adword + agreement
    # adjective as head
    referent = phrase.find('REFERENT')
    if referent.text is None:
      # make head, remove attribute node
      referent.text = adword.capitalize() + agreement
      phrase.remove(attribute)
      # add to Teilnehmer
      name = adword.capitalize() + 'e'
      gender = phrase.get('gender')
      Teilnehmer[name] = gender
      # add to locals for reflexivity
      local = upClause(phrase).get('local')
      local = referent if local is None else local + ',' + name
      upClause(phrase).set('local', local)

def Adverbiale(adverbial, adword):
  clause = adverbial.getparent()
  # --- adjectives
  if adword in Adjektive:
    # switch to attribut when there is a predicative in the sentence
    predicative = clause.find('.//PRÄDIKATIV/PHRASE')
    if predicative is not None:
      predicative.append(adverbial)
      Attribut(adverbial, adword)
      return
    # else just add adjective as adverbial
    else:
      ET.SubElement(adverbial, "ADJEKTIV").text = adword
  # --- adverbs
  else:
    ET.SubElement(adverbial, "ADVERB").text = adword
  # reorder
  predicate = clause.find('PRÄDIKAT')
  if predicate is None:
    clause.append(adverbial)
  else:
    predicate.addprevious(adverbial)

# ===========
# Eingrenzung
# ===========

def Grad(addto, intensifier):
  # insert Gradpartikel before adjective
  node = ET.Element('GRADPARTIKEL')
  # special case with predicative adjectives
  if addto.tag == 'SATZ':
    addto = addto.find('PRÄDIKATIV/ADVERBIALE')
  addto.insert(0, node)
  # attributes for interrogative
  mood = upClause(addto).get('mood')
  position = upSubClause(addto).tag.capitalize()
  predicate = upClause(addto).get('predicate')
  # interrogative
  if mood == 'Frage' and (position == 'Vorfeld' or predicate == 'Vorfeld'):
    node.text = 'wie'
  else:
    node.text = intensifier

def Grenze(adverbial, preposition):
  # insert Grenzpräposition before adverbial
  # bis morgen, seit gestern, ab heute, von gestern
  # nach links, von hier, nach oben, für gleich  
  # bis in den frühen Morgen, seit unser letztes Treffen
  node = ET.Element('ADVERBIALPRÄPOSITION')
  node.text = preposition
  adverbial.insert(0, node)

# ============
# Koordination
# ============

def Koordination(addto, conjunction = 'und'):
  # add nodes
  coordination = ET.SubElement(addto, 'KOORDINATION')
  ET.SubElement(coordination, 'KONJUNKTION').text = conjunction
  # copy info from above
  if addto.tag == 'PHRASE':
    case = addto.get('case')
    node = ET.SubElement(coordination, 'PHRASE', attrib = {'case': case})
  elif addto.tag == 'SATZ':
    tense = addto.get('tense')
    kind = addto.get('kind')
    node = ET.SubElement(coordination, 'SATZ', attrib = {'tense': tense, 'kind': kind})
    ET.SubElement(node, 'VORFELD')
  elif addto.tag == 'ATTRIBUT':
    node = ET.SubElement(coordination, 'ATTRIBUT')
  elif addto.tag == 'ADVERBIALE':
    node = ET.SubElement(coordination, 'ADVERBIALE')
  return node

def Vollkoordination(addto, conjunction = 'und'):
  # go up (assume clause or phrase, no root)
  parent = addto.getparent()
  # add nodes with notice for downstream
  coordination = ET.SubElement(parent, 'KOORDINATION')
  ET.SubElement(coordination, 'KONJUNKTION').text = conjunction
  if addto.tag == 'SATZ':
    coordination.set('tense', addto.get('tense'))
  return coordination

# ========
# Satzende
# ========

def Ende(satz, clean = True):
  checkAgreement(satz)
  # optional cleanup of attributes for readability
  if clean:
   cleanup(satz)

def checkVorfeld(addto, node):
  vorfeld = addto.find('VORFELD')
  branch = upSubClause(node)
  if addto.tag == 'SATZ' and vorfeld is not None:
    if len(vorfeld) == 0:
      kind = addto.get('kind')
      mood = addto.get('mood')
      truth = addto.get('truth')
      tense = addto.get('tense')
      predicate = addto.get('predicate')
      discourse = addto.get('discourse')
      # complementclause dass/ob
      if kind in ['Komplementsatz', 'Präpositionssatz'] and mood != 'Frage' and tense != 'Infinit':
        node = ET.SubElement(vorfeld, 'VORFELDERSATZ')
        node.text = 'ob' if truth == 'Unbestimmt' else 'dass'
      # yes/no question
      elif discourse == 'Thetisch' and mood == 'Frage':
        node = ET.SubElement(vorfeld, 'VORFELDERSATZ')
      # thetic 'es' sentences
      elif discourse == 'Thetisch':
        subjectEs = addto.find('SUBJEKTERSATZ')
        if subjectEs is None:
          node = ET.SubElement(vorfeld, 'VORFELDERSATZ').text = 'es'
        else:
          vorfeld.append(subjectEs)
      # predicate into vorfeld, including do-support!
      elif branch.tag == 'PRÄDIKATIV' and predicate != 'Vorfeld':
        return
      elif predicate == 'Vorfeld':
        predicative = addto.find('PRÄDIKATIV')
        # move predicative if it exists
        if predicative is not None:
          vorfeld.append(predicative)
        # take verb, but only when there is an auxiliary, else do support!
        else:
          if addto.find('PRÄDIKAT/VERB') is not None:
            addlightverb(addto, 'tun', 'Infinitiv', 'TUN-UNTERSTÜTZUNG')
          nonfinite = addto.xpath('PRÄDIKAT/*/*')[0]
          vorfeld.append(nonfinite)
          pass
      # move branch with inserted node to the front
      else:
        vorfeld.append(branch)

def checkAgreement(addto):
  clauses = upClause(addto).iter('SATZ')
  for clause in clauses:
    if clause.get('tense') == 'Infinit' and clause.get('agreement') is None:
      makeInfinite(clause)
      clause.set('agreement', 'done')
    if clause.get('person') is not None and clause.get('agreement') is None:
      verbAgreement(clause)
      clause.set('agreement', 'done')

def makeInfinite(clause):
  # complex rules for infinite relative clause
  if clause.get('kind') == 'Relativsatz':
    makeRelativecontrol(clause)
  # simple for others
  elif clause.get('kind') in ['Präpositionssatz', 'Komplementsatz']:
    finitum = clause.find('PRÄDIKAT')[-1]
    verb = finitum.get('verb')
    ET.SubElement(finitum, 'ZU-INFINITIV').text = 'zu ' + verb

def verbAgreement(clause):
  # get verb
  finitum = clause.find('PRÄDIKAT')[-1]
  verb = finitum.get('verb')
  # get agreement attributes
  tense = clause.get('tense')
  person = clause.get('person')
  number = clause.get('number')
  # --- finite ---
  finite = finiteverb(verb, person, number, tense)
  # insert finite verb
  node = ET.SubElement(finitum, 'FINITUM', 
    attrib = {'verb': verb, 'tense': tense, 'person': person, 'number': number})
  node.text = finite
  # --- Verbzweit ---
  if clause.get('kind') == 'Hauptsatz':
    # leave trace
    ET.SubElement(finitum, 'FINITUM', attrib = {'move': 'Verbzweit'})
    # move to second position
    verbzweit = ET.Element('VERBZWEIT')
    verbzweit.append(node)
    clause.insert(1, verbzweit)
  # --- Erstatzinfinitiv in subordinate clauses ---
  else:
    if clause.get('cluster') == 'Ersatzinfinitiv':
      # leave trace
      ET.SubElement(finitum, 'FINITUM', attrib = {'move': 'Finiterst'})
      # move finite to front of verb cluster
      predicate = clause.find('PRÄDIKAT')
      predicate.insert(0, node)

def passPersonNumber(trigger, case, person, gender):
  # only for nominative in argument (not for predicative nominative!)
  if case == 'Nominativ' and checkArgument(trigger):
    number = 'Plural' if gender == 'Plural' else 'Singular'
    clause = upClause(trigger)
    # check whether already present, in case of coordination
    existing = clause.get('person')
    if existing is not None:
      # person hierarchy, almost non-functional in German (even 2+3 is mostly 3+ agreement)
      person = min(existing, person)
      number = 'Plural'
    # set flags for verb agreement at clause level
    clause.set('person', person)
    clause.set('number', number)
  # setting argument-attached reflexives from diathesis
  constituent = upSubClause(trigger)
  reflexive = constituent.find('.//REFLEXIV')
  if reflexive is not None:
    case = reflexive.get('case')
    if person in list('12'):
      pronoun = Personalpronomina[number][person][case]
    else:
      pronoun = 'sich'
    reflexive.text = pronoun
    # detach reflexive
    constituent.addnext(reflexive)

def checkArgument(node):
  # check whether node is in an argument branch
  if node.tag == 'SUBJEKTERSATZ':
    return True
  while node.tag != 'ARGUMENT':
    node = node.getparent()
    if node.tag == 'SATZ':
      return False
  return True

# ------------
# German forms
# ------------

def addlightverb(clause, auxiliary, nonfinite, label, form = None):
  # get info
  node = clause.find('PRÄDIKAT')[-1]
  tense = node.get('tense')
  verb = node.get('verb')
  # make nonfinite form
  if form is None:
    if nonfinite == 'Partizip':
      form = participle(verb)
    elif nonfinite == 'zu-Infinitiv':
      form = 'zu ' + verb
    elif nonfinite == 'Infinitiv':
      form = verb
  # add nonfinite form
  ET.SubElement(node, nonfinite.upper()).text = form
  # insert new node for light verb
  new = ET.SubElement(node.getparent(), label.upper(), attrib = {'verb': auxiliary})
  # pass on tense
  if tense is not None:
    new.set('tense', tense)
    node.attrib.pop('tense')
  # add old node to new light verb
  new.append(node)

def addR(preposition):
  # insert 'r' for prepositions 'darauf'
  if preposition[0] in list('aeiouäöü'):
    return 'r'
  else:
    return ''

def verbstem(verb, tense = None):
  # stem listed in dictionary
  tenseform = Verben.get(verb, {}).get(tense)
  if tenseform is not None and isinstance(tenseform, str):
    stem = Verben[verb][tense]
  # common -en infinitive
  elif verb[-2:] == 'en':
    stem = verb[:-2]
  # e.g infinitive like ärgern
  elif verb[-3:] in ['ern', 'eln']:
    stem = verb[:-1]
  elif verb [-1:] == 'n':
    stem = verb[:-1]
  return stem

def participle(verb):
  # take form from lexicon
  participle = Verben.get(verb, {}).get('Partizip', False)
  # else assume regular participle
  if not participle:
    # decide on prefix
    stem = verbstem(verb)
    prefixes = ['ge', 'be', 'er', 'ver', 'zer', 'ent', 'miss']
    if sum([stem.startswith(prefix) for prefix in prefixes]) == 1:
      ge = ''
    else:
      ge = 'ge'
    # decide on suffix
    if stem[-1:] in list('mntd'):
      participle = ge + stem + 'et'
    else:
      participle = ge + stem + 't'
  return participle

def finiteverb(verb, person, number, tense):
  # various rules for verb inflection
  if verb not in Verben or tense not in Verben[verb] or isinstance(Verben[verb][tense], str):
    stem = verbstem(verb, tense)
    if tense == 'Präsens' and stem[-1:] in list('td'):
      if person == '2' or (person == '3' and number == 'Singular'):
        stem = stem + 'e'
    elif tense == 'Präsens' and stem[-1:] in list('mn') and stem[-2:-1] not in list('mnrl'):
      if person == '2' or (person == '3' and number == 'Singular'):
        stem = stem + 'e'
    elif tense == 'Präteritum':
      stem = stem + 't'
    elif tense == 'Konjunktiv':
      tense = 'Präteritum'
    elif tense == 'Irrealis':
      if stem[-1:] not in list('td'):
        stem = stem + 't'
      tense = 'Präteritum'
    finite = stem + Verbflexion[tense][number][person]
    # drop of 's' in second singular
    if tense == 'Präsens' and stem[-1:] in list('szxß'):
      if person == '2' and number == 'Singular':
        finite = finite[:-2] + 't'
    # reversal in first singular
    elif tense == 'Präsens' and stem[-2:] == 'el':
      if person == '1' and number == 'Singular':
        finite = finite[:-3] + 'le'
  # lookup in dictionary when whole paradigm is irregular
  else:
    finite = Verben[verb][tense][number][person]
  return finite

def passiv(clause, auxiliary = 'werden', nonfinite = 'Partizip', name = 'Vorgangspassiv', promoted = 'Akkusativ', demoted = 'von', reflexive = False):
  # add light verb
  addlightverb(clause, auxiliary, nonfinite, name)
  # change arguments
  for node in clause.findall('ARGUMENT'):
    leaf = node.xpath('.|.//*[not(name()="REFLEXIV")]')[-1]
    if leaf.get('case') == 'Nominativ':
      ET.SubElement(node, name, attrib = {'case': demoted})
    if leaf.get('case') == promoted:
      if reflexive:
        ET.SubElement(node, 'REFLEXIV', attrib = {'case': 'Akkusativ'})
      ET.SubElement(node, name, attrib = {'case': 'Nominativ'})
      # default order nominative first
      clause.insert(1, node)

def adjectiveAgreement(phrase):
  case = phrase.get('case')
  gender = phrase.get('gender')
  declension = phrase.get('declension')
  return Adjektivflexion[declension][case][gender]

def makeRelativecontrol(clause):
  # --- position of relative clause
  link = clause.getparent()
  addto = link.getparent()
  if link.tag == 'ATTRIBUT':
    # move relativsatz before referent
    referent = addto.find('REFERENT')
    referent.addprevious(link)
  elif link.tag == 'ADVERBIALE':
    # move before predicate
    predicate = addto.find('PRÄDIKAT')
    predicate.addprevious(link)
  # --- form of relative clause
  finitum = clause.find('PRÄDIKAT')[-1]
  verb = finitum.get('verb')
  # insert non-finite node
  infinite = ET.SubElement(finitum, 'PARTIZIP')
  # when inside phrase, then adjective agreement
  phrase = upPhrase(clause)
  if phrase.tag == 'PHRASE':
    agreement = adjectiveAgreement(phrase)
  else:
    agreement = ''
  # auxiliary 'sein' is removed, '+' is resolved at output
  # Modalpassiv has a special effect
  if verb == 'sein':
    infinite.set('removed', 'sein')
    if finitum.tag == 'MODALPASSIV':
      infinite.text = '+d'
    else:
      infinite.text = '+'
  else:
    infinite.text = verb + 'd'
  # combine into one form for nominalisation
  form = ''.join(clause.find('PRÄDIKAT').itertext())
  form = form.replace('+','')
  # add agreement
  infinite.text = infinite.text + agreement
  if infinite.text == '+':
    infinite.text = None
  # ---adjective as head
  referent = phrase.find('REFERENT')
  if referent is not None:
    if referent.text is None:
      # make head, remove attribute node
      referent.text = form.capitalize() + agreement
      phrase.remove(clause.getparent())
      # add to Teilnehmer
      name = form.capitalize() + 'e'
      Teilnehmer[name] = phrase.get('gender')
      # add to locals for reflexivity
      local = upClause(phrase).get('local')
      local = name if local is None else local + ',' + name
      upClause(phrase).set('local', local)

# ==============
# help functions
# ==============

def upPhrase(node):
  # go up to phrase, but not when already at a phrase
  while node.tag != 'PHRASE' and node.getparent() is not None:
    node = node.getparent()
  return node

def upClause(node):
  # ignore when at root or Hauptsatz
  if node.getparent() is None or node.get('kind') == 'Hauptsatz':
    return node
  # go up to clause, also when already at clause
  while node.getparent().tag != 'SATZ':
    node = node.getparent()
  return node.getparent()

def upSubClause(node):
  # ignore when at root or Hauptsatz
  if node.getparent() is None or node.get('kind') == 'Hauptsatz':
    return node
  # go up last node in branch before clause
  while node.getparent().tag != 'SATZ':
    node = node.getparent()
  return node

def belebtheit(referent):
  # get animacy from dictionary
  if referent in Substantive:
    animacy = Substantive[referent].get('Belebt', False) 
    animacy = 'Belebt' if animacy else 'Unbelebt'
  # guess when not in dictionary (for new names in Teilnehmer)
  else:
    gender = Teilnehmer[referent]
    animacy = 'Unbelebt' if gender == 'Neutrum' else 'Belebt'
  return animacy

def isReferential(lexeme):
  return lexeme[:1].isupper() \
  or lexeme[:1] in list('012') \
  or lexeme in list('emnfp') \

# =======
# Kontext
# =======

def reset():
  # clear the context
  Teilnehmer.clear()
  Themen.clear()

def add(name, gender = None):
  if name[:1].isupper():
    # add a participant to the context
    if gender is None:
      gender = Substantive[name]['Geschlecht']
    Teilnehmer[name] = gender
  else:
    Themen.append(name)

# ======
# Output
# ======

def cleanup(satz):
  for node in [satz] + satz.findall('.//SATZ'):
    keep = ['kind', 'controller', 'move', 'mood', 'head']
    clean(node, keep)
  for node in satz.findall('.//PHRASE'):
    keep = ['case', 'controller', 'move', 'mark']
    clean(node, keep)
  for node in satz.findall('.//KOORDINATION'):
    keep = []
    clean(node, keep)
  # remove unused arguments
  for node in satz.findall('.//ARGUMENT'):
    if ''.join(node.itertext()) == '':
      node.getparent().remove(node)

def clean(node, keep):
  new = {k:v for k,v in node.attrib.items() if k in keep}
  att = node.attrib 
  att.clear()
  att.update(new)

def capfirst(s):
  return s[:1].upper() + s[1:]

def sentence(clause):
  sentence = ' '.join(clause.itertext())
  # orthographic reductions
  sentence = sentence.replace(' +', '')
  sentence = sentence.replace('+ zu ', 'zu')
  sentence = sentence.replace('+ ', '')
  sentence = sentence.replace('  ', ' ')
  # end of sentence
  if clause.get('mood') == 'Frage':
    sentence = capfirst(sentence) + '?'
  else:
    sentence = capfirst(sentence) + '.'
  return sentence

def showresult(clause):
  print('<?xml version="1.0"?>')
  print('<!--') 
  print(sentence(clause))
  print('-->')
  ET.indent(clause)
  ET.dump(clause)

# ==========
# parse file
# ==========

def readfile(path):
  with open(path) as g:
    file = g.read()
    g.close()
  return file

def level(file):
  depth = []
  for line in file:
    depth.append(len(line) - len(line.lstrip()))
  return depth

def reference(file):
  depth = [0] + level(file)
  stack = {0: 0}
  ref = [0]
  for nr,elem in enumerate(depth[1:]):
    if elem > depth[nr]:
      ref.append(nr)
      stack.update({elem: nr})
    elif elem == depth[nr]:
      ref.append(ref[-1])
    elif elem < depth[nr]:
      ref.append(stack[elem])
  return ref[1:]

def specification(raw, lineNr, refs, head):
  # prepare line number
  id = 's' if lineNr == head else 's' + str(lineNr+1)
  if refs[lineNr] == 0:
    ref = 's'
  elif refs[lineNr] == head + 1:
    ref = 's'
  else:
    ref = 's' + str(refs[lineNr])
  # parse brackets
  raw = raw.replace(')', '')
  spec = raw.split(' (')
  # --- features between brackets ---
  features = dict()
  if len(spec) > 1:
    parts = spec[1].split(' + ')
    for part in parts:
      feature = part.split(': ')
      # lexical abbreviations
      if feature[0][:1].islower():
        if feature[0] in Modalverben:
          command = 'Modalverb(' + id + ', \'' + feature[0] + '\')\n'
          feature[0] = 'Modalverb'
        elif feature[0] in Quantoren:
          command = 'Quantor(' + id + ', \'' + feature[0] + '\')\n'
          feature[0] = 'Quantor'
        elif feature[0] in Kopulas:
          command = 'Kopula(' + id + ', \'' + feature[0] + '\')\n'
          feature[0] = 'Kopula'
      # other features
      else:
        if len(feature) == 1:
          command = feature[0] + '(' + id + ')\n'
        else:
          command = feature[0] + '(' + id + ', \'' + feature[1] + '\')\n'
      # collect features and names
      features[feature[0]] = command
  # separate early and late and join together
  early = ''.join([command for name,command in features.items() if name in earlyfeatures])
  late = ''.join([command for name,command in features.items() if name in nominalfeatures])
  kopula = features.get('Kopula', '')
  verbal = ''.join([command for name,command in features.items() if (name != 'Kopula' and name not in nominalfeatures + earlyfeatures)])
  # --- recursion part before brackets ---
  recursion = spec[0].lstrip()
  recursion = recursion.split(':')
  recursion = [x.strip() for x in recursion]
  lexeme = recursion[-1]
  connection = recursion[0] if len(recursion) == 2 else None
  # special case for predication
  if 'Kopula' in features:
    if isReferential(lexeme):
      if lineNr == head:
        satz = ''
      elif connection is None:
        satz = id + ' = Satz(' + ref + ')\n'
      else:
        satz = id + ' = Satz(' + ref + ', \'' + connection + '\')\n'
      prädikativ = 'Prädikativ(' + id + ')\n'
      phrase = 'p = Phrase(' + id + ', \'Prädikat\')\n'
      referent = 'Referent(p, \'' + lexeme + '\')\n'
      early = re.sub('\(s\d*', '(p', early)
      late = re.sub('\(s\d*', '(p', late)
      return satz + kopula + prädikativ + verbal + phrase + early + referent + late
    else:
      linkage = 'Satz'
      content = 'Prädikativ'
  # choose commands based on lexeme
  elif lexeme in Adverbien + Frageadverbien + Negationen + Adjektive:
    linkage = 'Link'
    content = 'Addendum'
  elif isReferential(lexeme):
    linkage = 'Phrase'
    content = 'Referent'
  else:
    linkage = 'Satz'
    content = 'Prädikat'
  # special coordination link, replacing others
  if connection in Konjunktionen or connection == '':
    linkage = 'Vollkoordination' if lexeme == '' else 'Koordination'
  # linkcommand
  if linkage == 'Satz' and lineNr == head:
    linkcommand = ''
  elif connection is None:
    linkcommand = id + ' = ' + linkage + '(' + ref + ')\n'
  else:
    linkcommand = id + ' = ' + linkage + '(' + ref + ', \'' + connection + '\')\n'
  # contentcommand
  if lexeme == '':
    contentcommand = ''
  else:
    contentcommand = content + '(' + id + ', \'' + lexeme + '\')\n'
  # --- all commands together ---
  return linkcommand + kopula + early + contentcommand + late + verbal

def convert(sentence, clean = True):
  sentence = re.split('\n', sentence)
  sentence = list(filter(None, sentence))
  refs = reference(sentence)
  head = level(sentence).index(0)
  for nr,elem in enumerate(sentence):
    sentence[nr] = specification(elem, nr, refs, head) 
  rules = 's = Start()\n' + ''.join(sentence) + f'Ende(s, {clean})\n'
  return rules

def makeTree(rules):
  loc = {}
  exec(rules, globals(), loc)
  return loc['s']

earlyfeatures = ['Plural', 'Bewegung', 'Belebt', 'Voll']
nominalfeatures = ['Definit', 'Demontrativ', 'Indefinit', 'Quantor', 'Besitzer', 'Numerale', 'Fokuspartikel']

# ================
# Output from file
# ================

def Syntax(file, code = False, xml = False, details = False, raw = False):
  clean = not details
  # split into sentences separated by empty line
  sentences = re.split('\n\s*\n', file)
  parsed = [convert(s, clean) for s in sentences]
  if code:
    text = '\n\n'.join(parsed)
  else:
    # execute all
    trees = [makeTree(s) for s in parsed]
    # extract text
    text = [sentence(s) for s in trees]
    text = '\n'.join(text)
    if xml:
      trees = [ET.tostring(s, pretty_print = True, encoding = 'utf-8').decode('utf-8') for s in trees]
      trees = '====\n'.join(trees)
      text = text + '\n=====\n' + trees
  if raw:
    return text
  else:
    print(text)
