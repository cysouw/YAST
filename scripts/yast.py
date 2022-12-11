import re
from lxml import etree as ET
from lexicon import *

# ====
# Satz
# ====

def Satz(addto, juncture = None):
  # abbreviations
  role = addto.find(f'*[@role="{juncture}"]')
  # subordinate clauses
  if juncture in Subjunktionen:
    return Subjunktionsatz(addto, juncture)
  elif juncture in Satzpartizipien + Satzpräpositionen:
    return Präpositionsatz(addto, juncture)
  elif juncture in Präpositionen or role is not None:
    return Komplementsatz(addto, juncture)
  elif juncture is None:
    return Relativsatz(addto)

def Ereignis(clause, verb = None):
  # abbreviations
  head = clause.get('head')
  # Verbal structure depends on lexeme
  if verb == 'e':
    Ereigniskopf(clause)
  elif head == 'Einsetzen':
    Kopfeinsatz(clause, verb)
  elif isAdjectival(verb) or verb in Adverbien or verb in Präpositionen or verb is None:
    Prädikativ(clause, verb)
  else:
    Verb(clause, verb)

# =====
# Sätze
# =====

def Start():
  clause = ET.Element('SATZ', attrib = {'kind': 'Hauptsatz', 'tense': 'Präsens'})
  # add vorfeld for early vorfeld specification
  ET.SubElement(clause, 'VORFELD')
  return clause

def Hauptsatz(addto):
  # Hauptsatz in coordination
  tense = addto.get('tense')
  clause = ET.SubElement(addto, 'SATZ', attrib = {'kind': 'Hauptsatz', 'tense': tense})
  return clause

def Subjunktionsatz(clause, juncture):
  # includes a vorfeld, although there is no evidence for it
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Subjunktionsatz', 'tense': tense})
  return newclause

def Präpositionsatz(clause, juncture):
  # special set of prepositions: um ohne anstatt etc.
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Präpositionssatz', 'tense': tense})
  # special case of 'um'
  if juncture == 'um':
    Infinit(node)
  return newclause

def Relativsatz(addto):
  # can both be attribute and adverbial, with nonverbal predication it is added to predicative
  tense = upClause(addto).get('tense')
  predicative = addto.find('.//PRÄDIKATIV/PHRASE')
  if predicative is not None:
    node = ET.SubElement(predicative, 'ATTRIBUT')
  elif addto.tag == 'SATZ':
    node = ET.SubElement(addto, 'ADVERBIALE')
  elif addto.tag == 'PHRASE':
    node = ET.SubElement(addto, 'ATTRIBUT')
  clause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Relativsatz', 'tense': tense})
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
  tense = upClause(clause).get('tense') if clause.get('tense') is None else clause.get('tense')
  newclause = ET.SubElement(leaf, 'SATZ', attrib = {'kind': 'Komplementsatz', 'tense': tense})
  # --- position: if vorfeld already filled: clause to back, but correlative stays
  vorfeld = clause.find('VORFELD')
  if len(vorfeld) != 0:
    clause.append(node)
    if correlative is not None:
      moveBeforeHead(clause, correlative)
      correlative.set('role', role)
      node.set('role', role)
  # --- agreement, in case this clause is the nominative
  passPersonNumber(newclause, juncture, '3', 'Singular')
  return newclause

# ===========
# Prädikation
# ===========

def Ereigniskopf(clause):
  ET.SubElement(clause, 'VORFELD')
  ET.SubElement(clause, 'PRÄDIKAT')

def Prädikativ(clause, predicate = None):
  # ad hoc solution for coordination of adjektive with relative clause
  if clause.tag == 'ATTRIBUT':
    clause.tag = 'SATZ'
    clause.set('kind', 'Relativsatz')
   # get copula from clause
  copula = clause.get('verb')
  # add vorfeld
  if clause.find('VORFELD') is None:
    ET.SubElement(clause, 'VORFELD')
  # subject and predicate for default nominal predicate
  subject = ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  predicative = ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikat', 'case': 'Nominativ'})
  # add copula
  verb = ET.SubElement(clause, 'PRÄDIKAT')
  ET.SubElement(verb, 'VERB', attrib = {'verb': copula})
  # different kinds of predication
  if predicate is not None and isAdjectival(predicate):
    adverbial = ET.SubElement(predicative, 'ADVERBIALE')
    ET.SubElement(adverbial, 'ADJEKTIV').text = predicate
  # adverbial predication 'ich bin hier, die Sitzung war gestern'
  elif predicate is not None and predicate in Adverbien:
    adverbial = ET.SubElement(predicative, 'ADVERBIALE')
    ET.SubElement(adverbial, 'ADVERB').text = predicate
  # locational predication
  elif predicate is not None and predicate in Präpositionen:
    predicative.set('role', 'Ort')
    predicative.set('case', predicate)
  # possession with 'haben'
  elif copula == 'haben':
    subject.set('role', 'Habende')
    predicative.set('case', 'Akkusativ')
  # existential clause 'es gibt'
  elif copula == 'geben':
    predicative.set('case', 'Akkusativ')
    subject.tag ='SUBJEKTERSATZ'
    subject.text = 'es'
    passPersonNumber(subject, 'Nominativ', '3', 'Singular')

def Verb(clause, verb):
  # ad hoc solution for coordination of adjektive with relative clause
  if clause.tag == 'ATTRIBUT':
    clause.tag = 'SATZ'
    clause.set('kind', 'Relativsatz')
  # remember original full verb
  clause.set('verb', verb)
  # add vorfeld
  if clause.find('VORFELD') is None:
    ET.SubElement(clause, 'VORFELD')
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
  verbnode = ET.SubElement(predicate, 'VERB')
  # lexicalised preverbs from lexicon are split
  if Verben.get(verb, {}).get('Präverb', False):
    ET.SubElement(verbnode, 'PRÄVERBIALE').text = Verben[verb]['Präverb'] + '+'
    verb = Verben[verb]['Stamm']
  # lexicalised nominal predicatives from lexicon are split
  if Verben.get(verb, {}).get('Prädikat', False):
    predicative = ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikat', 'case': 'Akkusativ'})
    phrase = Phrase(predicative, 'Prädikat')
    Referent(phrase, Verben[verb]['Prädikat'])
    verb = Verben[verb]['Stamm']
  # add verb to info
  verbnode.set('verb', verb)

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
  # add copula for nonverbal predication
  clause.set('verb', copula)

def Kopf(addto):
  addto.set('head', 'Einsetzen')

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
  passiv(clause, 'lassen', 'Infinitiv', 'Permissivpassiv', 'Akkusativ', demoted)
  addReflexive(clause)

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
      es = ET.Element('SUBJEKTERSATZ')
      es.text = 'es'
      node.addnext(es)
      passPersonNumber(es, 'Nominativ', '3', 'Singular')
      clause.remove(node)

# ======
# Phrase
# ======

def Phrase(addto, juncture = None):
  # abreviations
  role = addto.find(f'*[@role="{juncture}"]')
  # possibilities
  if juncture in Präpositionen:
    return Präpositionphrase(addto, juncture)
  elif role is not None:
    return Komplementphrase(addto, juncture)
  elif juncture is None:
    return Relativphrase(addto)

def Referent(phrase, referent = None):
  # abbreviations
  head = phrase.get('head')
  full = phrase.get('full')
  # phrasal structure depends on lexeme
  if referent[:1] in list('012'):
    Pronomen(phrase, referent)
  elif (referent in Teilnehmer or referent == 'e') and full is None:
    Anapher(phrase, referent)
  elif referent in list('mnfpqr'):
    Genuskopf(phrase, referent)
  elif head == 'Einsetzen':
    Kopfeinsatz(phrase, referent)
  else:
    Nomen(phrase, referent)

# =======
# Phrasen
# =======

def Komplementphrase(clause, role = None):
  # go to tip of branch to add stuff
  argument = clause.find(f'*[@role="{role}"]')
  leaf = argument.xpath('.|.//*[not(name()="REFLEXIV")]')[-1]
  case = leaf.get('case')
  # prepositional argument
  if case in Präpositionen:
    ET.SubElement(leaf, 'JUNKTOR').text = case
    case = Präpositionen[case]
    # special case assignment for governed prepositions
    if case in ['an', 'in', 'auf', 'über'] and role != 'Ort':
      case = 'Akkusativ'
  # add phrase
  phrase = ET.SubElement(leaf, 'PHRASE', attrib = {'case': case})
  # position argument before predicate
  moveBeforeHead(clause, argument)
  return phrase

def Präpositionphrase(addto, juncture):
  # switch to attribut when there is a predicative in the sentence
  predicative = addto.find('.//PRÄDIKATIV/PHRASE')
  # attributive phrase
  if addto.tag == 'PHRASE' or predicative is not None:
    node = ET.SubElement(addto, 'ATTRIBUT')
  # adverbial phrase
  elif addto.tag == 'SATZ':
    node = ET.Element('ADVERBIALE')
    # ad-hoc solution for comparative phrases
    if juncture in ['als', 'wie']:
      addto.append(node)
    else:
      moveBeforeHead(addto, node)
  # for Vollkoordination
  elif addto.tag == 'KOORDINATION':
    node = addto
  # add nodes
  case = Präpositionen[juncture]
  ET.SubElement(node, 'JUNKTOR').text = juncture
  phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': case})
  return phrase

def Relativphrase(addto):
  # adverbial measure-phrase in accusative, e.g. 'den ganzen Tag'
  if addto.tag == 'SATZ':
    case = 'Akkusativ'
    node = ET.Element('ADVERBIALE')
    moveBeforeHead(addto, node)
  # adnominal genitive
  elif addto.tag == 'PHRASE':
    case = 'Genitiv'
    node = ET.SubElement(addto, 'ATTRIBUT')
  # add phrase
  phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': case})
  return phrase

# ==========
# Referenten
# ==========

def Genuskopf(phrase, referent):
  # get info from phrase
  case = phrase.get('case')
  number = phrase.get('gender')
  # expand abbreviation 
  gender = Genera[referent]
  # override with plural
  if number == 'Plural':
    gender = 'Runde' if gender == 'Queer' else 'Plural'
  # set flags for agreement
  phrase.set('gender', gender)
  phrase.set('declension', 'stark')
  # in relative clause, gender can be used for 'freier relativsatz'
  kind = upClause(phrase).get('kind')
  position = upSubClause(phrase).tag.capitalize()
  if kind == 'Relativsatz' and position == 'Vorfeld':
    Anapher(phrase, gender)
  # else full out noun phrase
  else:
    ET.SubElement(phrase, 'DETERMINATIV')   
    ET.SubElement(phrase, 'REFERENT')
    # add unnamed Teilnehmer
    Teilnehmer[gender] = gender
    # update local context within clause for reflexivity
    local = upClause(phrase).get('local')
    local = gender if local is None else local + ',' + gender
    # check verb agreement
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
  # get gender and animacy from Teilnehmer, also allow direct gender as referent
  if referent in Genera.values():
    gender = referent
  else:
    gender = 'Neutrum' if referent == 'e' else Teilnehmer[referent]
  # can be plural ('+3') when marked at phrase
  number = phrase.get('gender')
  gender = 'Plural' if number in ['Plural', 'Runde'] else gender
  # update Teilnehmer
  Teilnehmer[referent] = gender
  # get local participants for reflexivitiy
  local = upClause(phrase).get('local')
  localreferents = local.split(',') if local is not None else []
  # get info from clause for relative pronouns
  kind = upClause(phrase).get('kind')
  position = upSubClause(phrase).tag.capitalize()
  # get junctor and animacy for correlative form
  animacy = getAnimacy(referent)
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
  # set flags at phrase
  phrase.set('gender', gender)
  phrase.set('referent', referent)
  # check verb agreement
  passPersonNumber(phrase, case, '3', gender)

def Nomen(phrase, referent):
  # get info from phrase
  case = phrase.get('case')
  number = phrase.get('gender')
  # find gender from Teilnehmer
  if referent in Teilnehmer:
    gender = Teilnehmer[referent]
  # find gender from dictionary
  elif referent in Substantive:
    gender = Substantive[referent]['Geschlecht']
  # look at the ending to guess gender
  else:
    gender = getGender(referent)
  # override gender with plurality from phrase
  if number == 'Plural':
    gender = 'Runde' if gender == 'Queer' else 'Plural'
  # add new Teilnehmer to context
  Teilnehmer[referent] = gender
  # update local context within clause for reflexivity
  local = upClause(phrase).get('local')
  local = referent if local is None else local + ',' + referent
  upClause(phrase).set('local', local)
  # inflection of noun
  referent = nounInflection(referent, case, gender)
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
  # reduce gender
  gender = 'Feminin' if gender == 'Queer' else gender
  gender = 'Plural' if gender == 'Runde' else gender
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
  # reduce gender
  gender = 'Feminin' if gender == 'Queer' else gender
  gender = 'Plural' if gender == 'Runde' else gender
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
  # reduce gender
  gender = 'Feminin' if gender == 'Queer' else gender
  gender = 'Plural' if gender == 'Runde' else gender
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
  # reduce gender
  gender = 'Feminin' if gender == 'Queer' else gender
  gender = 'Plural' if gender == 'Runde' else gender
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
  # reduce gender
  gender = 'Feminin' if gender == 'Queer' else gender
  gender = 'Plural' if gender == 'Runde' else gender
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
      # reduce gender
      gender = 'Feminin' if gender == 'Queer' else gender
      gender = 'Plural' if gender == 'Runde' else gender
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

def Admodifikation(addto):
  # abbreviations
  predicative = addto.find('.//PRÄDIKATIV/PHRASE')
  # special case: rebase for adjectives in noun predication
  if predicative is not None:
    return ET.SubElement(predicative, 'ATTRIBUT')
  elif addto.tag == 'PHRASE':
    return ET.SubElement(addto, 'ATTRIBUT')
  elif addto.tag == 'SATZ':
    return ET.SubElement(addto, 'ADVERBIALE')

def Addendum(addto, adword):
  # abbreviations
  head = addto.get('head')
  # different kinds of lexemes
  if head == 'Einsetzen':
    Kopfeinsatz(addto, adword)
  elif isAdjectival(adword):
    Adjektiv(addto, adword)
  elif isAdverbial(adword):
    Adverb(addto, adword)

# ======= 
# Addenda
# =======

def Adjektiv(addto, adjective):
  # add adjective node
  node = ET.SubElement(addto, "ADJEKTIV")
  # make comparison
  if addto.get('comparison') == 'Komparativ':
    adjective = makeComparative(adjective)
  elif addto.get('comparison') == 'Superlativ':
    adjective = makeSuperlative(adjective)
  # in phrase insert adjective with agreement and move before referent
  if addto.tag == 'ATTRIBUT':
    phrase = upPhrase(addto)
    node.text = adjective + adjectiveInflection(phrase)
    moveBeforeHead(phrase, addto)
  # in clause add adjective as adverbial
  elif addto.tag == 'ADVERBIALE':
    clause = addto.getparent()
    node.text = adjective
    moveBeforeHead(clause, addto)

def Adverb(addto, adverb):
  # add adverb node
  node = ET.SubElement(addto, "ADVERB")
  # in phrase move adverb after referent, e.g. 'das Treffen gestern', also for 'selbst'
  if addto.tag == 'ATTRIBUT':
    phrase = upPhrase(addto)
    node.text = adverb
    phrase.append(node)
  # in clause move adverb before verb
  elif addto.tag == 'ADVERBIALE':
    clause = addto.getparent()
    node.text = adverb
    moveBeforeHead(clause, node)

# ==========
# Komparativ
# ==========

# added as rules because the suffixes ruin the recognition of word class

def Komparativ(addto):
  addto.set('comparison', 'Komparativ')

def Superlativ(addto):
  addto.set('comparison', 'Superlativ')

# ===========
# Eingrenzung
# ===========

def Grad(addto, intensifier):
  # rebase with predicative adjectives
  if addto.tag == 'SATZ':
    addto = addto.find('PRÄDIKATIV/ADVERBIALE')
  # insert Gradpartikel before adjective
  node = ET.Element('GRADPARTIKEL')
  addto.insert(0, node)
  # attributes for interrogative
  mood = upClause(addto).get('mood')
  position = upSubClause(addto).tag.capitalize()
  predicate = upClause(addto).get('predicate')
  # interrogative
  if mood == 'Frage' and (position == 'Vorfeld' or predicate == 'Vorfeld'):
    node.text = 'wie'
  # intensifier
  else:
    node.text = intensifier

def Grenze(adverbial, preposition):
  # insert Grenzpräposition before adverbial: von/seit/ab and bis/nach
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
  node = ET.SubElement(coordination, addto.tag)
  # copy info from above
  if addto.tag == 'PHRASE':
    node.set('case', addto.get('case'))
  elif addto.tag == 'SATZ':
    node.set('tense' , addto.get('tense'))
    node.set('kind', addto.get('kind'))
  # pass plurality upwards for finite verb
  case = addto.get('case')
  if case is not None and case == 'Nominativ':
    clause = upClause(addto)
    clause.set('number', 'Plural')
    #Verbcheck(clause)
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

# ===========
# Kopfeinsatz
# ===========

def Kopfeinsatz (addto, lexeme):
  # rebase insertion point
  if addto.tag in ['PHRASE', 'SATZ']:
    insert = addto.getparent().getparent()
    insert.remove(addto.getparent())
  else:
    insert = addto.getparent()
    insert.remove(addto)
  # --- fill in the blanc referent
  if insert.tag == 'PHRASE':
    gender = insert.get('gender')
    case = insert.get('case')
    head = insert.find('REFERENT')
    if isReferential(lexeme):
      animacy = getAnimacy(lexeme)
      form = lexeme
      if animacy == 'Belebt':
        if gender == 'Feminin':
          form = lexeme + 'in'
        elif gender == 'Queer':
          form = lexeme + '*in'
        elif gender == 'Runde':
          form = lexeme + '*innen'
      if head.text is None:
        head.text = nounInflection(form, case, gender)
    # --- adjective as head
    elif isAdjectival(lexeme):
      if head.text is None:
        head.text = lexeme.capitalize() + adjectiveInflection(insert)
      # name for Teilnehmer
      lexeme = lexeme.capitalize() + 'e'
      pass
    # verb as head only works with Neutrum, e.g. 'das Laufen'
    # add new Teilnehmer to context
    Teilnehmer[lexeme] = gender
    Teilnehmer.pop(gender)
    # update local context within clause for reflexivity
    local = upClause(insert).get('local')
    local = lexeme if local is None else local + ',' + lexeme
    upClause(insert).set('local', local)
  # --- fill in the blanc predicate
  elif insert.tag == 'SATZ':
    if isReferential(lexeme):
      pass
    elif isAdjectival(lexeme):
      pass
    else:
      pass

# ========
# Satzende
# ========

def Vorfeldcheck(addto, node):
  vorfeld = addto.find('VORFELD')
  branch = upSubClause(node)
  if addto.tag == 'SATZ' and vorfeld is not None:
    if len(vorfeld) == 0:
      kind = addto.get('kind')
      mood = addto.get('mood')
      truth = addto.get('truth')
      tense = addto.get('tense')
      person = addto.get('person')
      predicate = addto.get('predicate')
      discourse = addto.get('discourse')
      # complementclause dass/ob
      if kind in ['Komplementsatz', 'Präpositionssatz'] and mood != 'Frage':
        node = ET.SubElement(vorfeld, 'VORFELDERSATZ')
        if tense != 'Infinit':
          node.text = 'ob' if truth == 'Unbestimmt' else 'dass'
      # yes/no question
      elif discourse == 'Thetisch' and mood == 'Frage':
        node = ET.SubElement(vorfeld, 'VORFELDFÜLLUNG')
      # thetic 'es' sentences
      elif discourse == 'Thetisch':
        subjectEs = addto.find('SUBJEKTERSATZ')
        if subjectEs is None and person is None:
          node = ET.SubElement(vorfeld, 'SUBJEKTERSATZ')
          node.text = 'es'
          passPersonNumber(node, 'Nominativ', '3', 'Singular')
        elif subjectEs is None:
          node = ET.SubElement(vorfeld, 'VORFELDERSATZ')
          node.text = 'es'
        else:
          vorfeld.append(subjectEs)
      # do nothing when node is predicative, but it is not supposed to be in vorfeld
      elif branch.tag == 'PRÄDIKATIV' and predicate != 'Vorfeld':
        return
      # predicate into vorfeld, including do-support!
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
      # no vorfeld in infinite clauses
      elif tense == 'Infinit':
        node = ET.SubElement(vorfeld, 'VORFELDFÜLLUNG')
      # else: move branch with inserted node to the front
      else:
        vorfeld.append(branch)

def Verbcheck(addto):
  clauses = addto.iter('SATZ') if addto.tag == 'SATZ' else []
  for clause in clauses:
    if clause.get('agreement') is None:
      if clause.get('tense') == 'Infinit':
        makeInfinite(clause)
        clause.set('agreement', 'done')
      elif clause.get('person') is not None:
        verbInflection(clause)
        clause.set('agreement', 'done')

def passPersonNumber(trigger, case, person, gender):
  # only for nominative in argument (not for predicative nominative!)
  if case == 'Nominativ' and checkArgument(trigger):
    number = 'Plural' if gender in ['Plural', 'Runde'] else 'Singular'
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
    # make finite verb if plural
    #if number == 'Plural':
    #  Verbcheck(clause)
  # setting argument-attached reflexives from diathesis
  constituent = upSubClause(trigger)
  reflexive = constituent.find('.//REFLEXIV')
  if reflexive is not None:
    if person in list('12'):
      case = reflexive.get('case')
      reflexive.text = Personalpronomina[number][person][case]
    else:
      reflexive.text = 'sich'
    # detach reflexive
    constituent.addnext(reflexive)

# ------------
# German forms
# ------------

def getGender(lexeme):
  if lexeme[-2:] in ['er'] or lexeme[-4:] in ['ling']:
    gender = 'Maskulin'
  elif lexeme[-2:] in ['en'] or lexeme[-3:] in ['tum', 'nis'] or lexeme[-4:] in ['chen', 'lein']:
    gender = 'Neutrum'
  elif lexeme[-2:] in ['ei', 'in'] or lexeme[-3:] in ['ung'] or lexeme[-4:] in ['heit', 'keit', 'haft']:
    gender = 'Feminin'
  # default return, will be mostly wrong!
  else:
    gender = 'Neutrum'
  return gender

def getAnimacy(referent):
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
    or lexeme in list('emnfpqr') \

def isAdjectival(lexeme):
  return lexeme in Adjektive \
    or lexeme[-2:] in ['ig'] \
    or lexeme[-3:] in ['bar', 'sam'] \
    or lexeme[-4:] in ['lich', 'haft', 'isch'] \
    or lexeme[-5:] in ['gemäß']

def isAdverbial(lexeme):
  return lexeme in Adverbien + Frageadverbien + Negationen

def adjectiveInflection(phrase):
  case = phrase.get('case')
  gender = phrase.get('gender')
  declension = phrase.get('declension')
  # reduce gender
  gender = 'Feminin' if gender == 'Queer' else gender
  gender = 'Plural' if gender == 'Runde' else gender
  return Adjektivflexion[declension][case][gender]

def nounInflection(referent, case, gender):
  # check dictionary
  nDeclination = Substantive.get(referent, {}).get('n-Deklination', False)
  # regulars
  if gender == 'Maskulin' and \
     (referent[-1] == 'e' \
      or referent[-2:] in ['ad', 'at', 'et', 'ik', 'it', 'ot', 'ut'] \
      or referent[-3:] in ['ade', 'ale', 'and', 'ant', 'aut', 'eut', 'ent', 'isk', 'ist', 'nom', 'oge', 'one'] \
      or referent[-4:] in ['arch', 'graf', 'soph'] \
      or referent[-5:] in ['graph'] \
      ):
    nDeclination = True
  # add endings to noun
  if nDeclination:
    if case != 'Nominativ' or gender == 'Plural':
      if referent[-1] in list('er'):
        referent = referent + 'n'
      else:
        referent = referent + 'en'
  else:
    # plural from dictionary
    if gender == 'Plural':
      referent = Substantive[referent]['Plural']
      if case == 'Dativ' and referent[-1] not in list('ns'):
        referent = referent + 'n'
    # special case of Herz
    elif referent == 'Herz':
      if case == 'Dativ':
        referent = 'Herzen'
      elif case == 'Genitiv':
        referent = 'Herzens'
    # genitiv singular
    else:
      if case == 'Genitiv' and gender in ['Maskulin', 'Neutrum']:
        if referent[-1] in list('lnr'):
          referent = referent + 's'
        else:
          referent = referent + 'es'
  return referent

def verbInflection(clause):
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

def makeComparative(lexeme):
  # suppletion
  if lexeme in comparisonSuppletion:
    comparative = comparisonSuppletion[lexeme]['Komparativ']
  else:
    # umlaut
    if lexeme in comparisonUmlaut:
      lexeme = lexeme.replace('a', 'ä')
      lexeme = lexeme.replace('o', 'ö')
      lexeme = lexeme.replace('u', 'ü')
    # suffix
    if lexeme[-1] == 'e':
      comparative = lexeme + 'r'
    elif lexeme[-2:] == 'el':
      comparative = lexeme[:-2] + 'ler'
    else:
      comparative = lexeme + 'er'
  return comparative

def makeSuperlative(lexeme):
  # suppletion
  if lexeme in comparisonSuppletion:
    superlative = comparisonSuppletion[lexeme]['Superlativ']
  else:
    # umlaut
    if lexeme in comparisonUmlaut:
      lexeme = lexeme.replace('a', 'ä')
      lexeme = lexeme.replace('o', 'ö')
      lexeme = lexeme.replace('u', 'ü')
    # suffix
    if lexeme[-1] == 'e':
      superlative = lexeme[:-1] + 'st'
    elif lexeme[-1] in list('tdsß') or lexeme [-3:] == 'sch':
      superlative = lexeme + 'est'
    else:
      superlative = lexeme + 'st'
  return superlative

def addR(preposition):
  # insert 'r' for prepositions 'darauf'
  return 'r' if preposition[0] in list('aeiouäöü') else ''

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

def makeInfinite(clause):
  # complex rules for infinite relative clause
  if clause.get('kind') == 'Relativsatz':
    makeRelativecontrol(clause)
  # simple for others
  elif clause.get('kind') in ['Präpositionssatz', 'Komplementsatz']:
    finitum = clause.find('PRÄDIKAT')[-1]
    verb = finitum.get('verb')
    ET.SubElement(finitum, 'ZU-INFINITIV').text = 'zu ' + verb

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
    agreement = adjectiveInflection(phrase)
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
  # --- adjective as head
  referent = phrase.find('REFERENT')
  if phrase.get('head') == 'Einsetzen':
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

def addReflexive(clause):
  for node in clause.findall('ARGUMENT'):
    leaf = node.xpath('.|.//*[not(name()="REFLEXIV")]')[-1]
    if leaf.get('case') == 'Nominativ':
      ET.SubElement(node, 'REFLEXIV', attrib = {'case': 'Akkusativ'})

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

def moveBeforeHead(addto, node):
  # ignore for adverbs in Vorfeld
  if addto.tag == 'VORFELD':
    return
  # find head
  elif addto.tag == 'SATZ':
    head = addto.xpath('PRÄDIKAT|PRÄDIKATIV')
  elif addto.tag == 'PHRASE':
    head = addto.xpath('REFERENT|ANAPHOR|REFLEXIVPRONOMEN|PRONOMEN')
  # move before head
  if len(head) > 0:
    head[0].addprevious(node)
  # except when there is no head
  else:
    addto.append(node)

def checkArgument(node):
  # check whether node is in an argument branch
  if node.tag == 'SUBJEKTERSATZ':
    return True
  while node.tag != 'ARGUMENT':
    node = node.getparent()
    if node.tag == 'SATZ':
      return False
  return True

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

def Endcheck(satz):
  Verbcheck(satz)

def cleanup(satz):
  # remove many flags for readability
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
  return satz

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
  # check vorfeld
  vorfeld = 'Vorfeldcheck(' + ref + ', ' + id + ')\n'
  end = 'Endcheck(' + ref + ')\n'
  # special case for predication
  if 'Kopula' in features:
    if isReferential(lexeme):
      if lineNr == head:
        satz = ''
        vorfeld = ''
        end = ''
      elif connection is None:
        satz = id + ' = Satz(' + ref + ')\n'
      else:
        satz = id + ' = Satz(' + ref + ', \'' + connection + '\')\n'
      prädikativ = 'Prädikativ(' + id + ')\n'
      phrase = 'p = Phrase(' + id + ', \'Prädikat\')\n'
      referent = 'Referent(p, \'' + lexeme + '\')\n'
      early = re.sub('\(s\d*', '(p', early)
      late = re.sub('\(s\d*', '(p', late)
      vorfeld2 = 'Vorfeldcheck(' + id + ', p)\n'
      end2 = 'Endcheck(' + id + ')\n'
      return end + satz + vorfeld + kopula + prädikativ + verbal + end2 + phrase + vorfeld2 + early + referent + late
    else:
      linkage = 'Satz'
      content = 'Prädikativ'
  # choose commands based on lexeme
  elif isAdjectival(lexeme) or isAdverbial(lexeme):
    linkage = 'Admodifikation'
    content = 'Addendum'
  elif isReferential(lexeme):
    linkage = 'Phrase'
    content = 'Referent'
  else:
    linkage = 'Satz'
    content = 'Ereignis'
  # special coordination link, replacing others
  if connection in Konjunktionen or connection == '':
    linkage = 'Vollkoordination' if lexeme == '' else 'Koordination'
  # linkcommand
  if linkage == 'Satz' and lineNr == head:
    # start of sentence
    linkcommand = ''
    vorfeld = ''
    end = ''
  elif connection is None:
    linkcommand = id + ' = ' + linkage + '(' + ref + ')\n'
  else:
    linkcommand = id + ' = ' + linkage + '(' + ref + ', \'' + connection + '\')\n'
  # contentcommand
  if lexeme == '':
    # only used for full-coordination with different connections
    contentcommand = ''
  else:
    contentcommand = content + '(' + id + ', \'' + lexeme + '\')\n'
  # --- all commands together ---
  return end + linkcommand + vorfeld + kopula + early + contentcommand + late + verbal

def convert(sentence):
  sentence = re.split('\n', sentence)
  sentence = list(filter(None, sentence))
  refs = reference(sentence)
  head = level(sentence).index(0)
  for nr,elem in enumerate(sentence):
    sentence[nr] = specification(elem, nr, refs, head) 
  rules = 's = Start()\n' + ''.join(sentence) + 'Endcheck(s)\n'
  return rules

def makeTree(rules):
  loc = {}
  exec(rules, globals(), loc)
  return loc['s']

earlyfeatures = ['Plural', 'Bewegung', 'Belebt', 'Voll', 'Kopf', 'Komparativ', 'Superlativ']
nominalfeatures = ['Definit', 'Demontrativ', 'Indefinit', 'Quantor', 'Besitzer', 'Numerale', 'Fokuspartikel']

# ======
# Output
# ======

def Syntax(file, code = False, xml = False, details = False, raw = False):
  # split into sentences separated by empty line
  sentences = re.split('\n\s*\n', file)
  parsed = [convert(s) for s in sentences]
  if code:
    text = '\n\n'.join(parsed)
  else:
    # execute all
    trees = [makeTree(s) for s in parsed]
    # extract text
    text = [sentence(s) for s in trees]
    text = '\n'.join(text)
    # cleanup trees
    if not details:
      trees = [cleanup(s) for s in iter(trees)]
    # prepare xml output
    if xml:
      trees = [ET.tostring(s, pretty_print = True, encoding = 'utf-8').decode('utf-8') for s in trees]
      trees = '====\n'.join(trees)
      text = text + '\n=====\n' + trees
  if raw:
    return text
  else:
    print(text)
