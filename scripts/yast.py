import re
from lxml import etree as ET
from lexicon import *

# ====
# Satz
# ====

def Satz(addto, juncture = None):
  # abbreviations
  sub = upSubClause(addto)
  parent = addto.getparent()
  role = addto.find(f'*[@role="{juncture}"]')
  # subordinate clauses
  if juncture in Subjunktionen:
    node = Subjunktionsatz(addto, juncture)
  elif juncture in Satzpartizipien + Satzpräpositionen:
    node = Präpositionssatz(addto, juncture)
  elif role is not None or juncture in Präpositionen:
    node = Komplementsatz(addto, juncture)
  elif juncture is None:
    node = Relativsatz(addto)
  # check vorfeld
  vorfeld(node)
  return node

def Prädikat(clause, verb):
  copula = verb.split()[0]
  if copula in Kopulas:
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

def Satzkoordination(addto, juncture):
  return eval(addto.get('kind'))(addto, juncture)
# put conjunction in right position
# shiftconjunction(coordination)

def Subjunktionsatz(clause, juncture):
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
  vorfeld = ET.SubElement(newclause, 'VORFELD')
  # these only occur with dass
  ET.SubElement(vorfeld, 'VORFELDERSATZ').text = 'dass'
  # special case of 'um'
  if juncture == 'um':
    Infinit(node)
  return newclause

def Relativsatz(addto):
  # can both be attributiv and adverbial
  tense = upClause(addto).get('tense')
  if addto.tag == 'SATZ':
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
    # find role
    node = clause.find(f'*[@role="{role}"]')
    # go to tip of branch to add junktor
    leaf = list(node.iter())[-1]
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
  # if vorfeld already filled: clause to back, but correlative stays
  vorfeld = clause.find('VORFELD')
  if len(vorfeld) != 0:
    predicate = clause.find('PRÄDIKAT')
    clause.append(node)
    if correlative is not None:
      predicate.addprevious(correlative)
      correlative.set('role', role)
      node.set('role', role)
  # in case this clause is nominative
  passPersonNumber(newclause, juncture, '3', 'Singular')
  return newclause

# =====================
# Early Event Structure
# =====================

def Unbestimmt(clause):
  clause.set('truth', 'Unbestimmt')

def Frage(clause):
  clause.set('mood', 'Frage')

def Infinit(clause):
  clause.set('tense', 'Infinit')
  # remove relator
  clause.remove(clause.find('VORFELD'))
  # complex rules for infinite relative clause
  if clause.get('kind') == 'Relativsatz':
    makeRelativecontrol(clause)
  # simple for others
  elif clause.get('kind') in ['Präpositionssatz', 'Komplementsatz']:
    finitum = clause.find('PRÄDIKAT')[-1]
    verb = finitum.get('verb')
    ET.SubElement(finitum, 'ZU-INFINITIV').text = 'zu ' + verb

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

# combine locational, adverbial, adjectival and nominal predication
# they use the same construction in German

def Prädikativ(clause, verb):
  clause.set('verb', verb)
  # --- roles ---
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  predicative = ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikat', 'case': 'Nominativ'})
  # --- verb ---
  parts = verb.split()
  copula = parts[0]
  # location
  if len(parts) > 1:
    ET.SubElement(predicative, 'PRÄDIKATIV', attrib = {'role': 'Ort', 'juncture': parts[1]})
  # add predicate node
  predicate = ET.SubElement(clause, 'PRÄDIKAT')
  ET.SubElement(predicate, 'VERB', attrib = {'verb': copula})

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
  addlightverb(clause, modal, 'Infinitiv', 'MODALVERB')
  
def Perfekt(clause):
  # get info
  node = clause.find('PRÄDIKAT')[-1]
  verb = node.get('verb') if node.find('PRÄVERBIALE') is None else clause.get('verb') 
  # default to auxiliary 'haben', when not otherwise noted in dictionary
  auxiliary = Verben.get(verb, {}).get('Perfekt', 'haben')
  # Ersatzinfinitiv
  if node.tag == 'MODALVERB':
    addlightverb(clause, auxiliary, 'Infinitiv', 'PERFEKT')
    # set flag for ordering with Ersatzinfinitiv
    clause.set('cluster', 'Ersatzinfinitiv')
  # special participle with Vorgangspassiv
  elif node.tag == 'VORGANGSPASSIV':
    addlightverb(clause, auxiliary, 'Partizip', 'PERFEKT', form = 'worden')
  # Regular perfect
  else:
    addlightverb(clause, auxiliary, 'Partizip', 'PERFEKT')

def Vorgangspassiv(clause, demoted = 'von'):
  Passiv(clause, 'werden', 'Partizip', 'VORGANGSPASSIV', 'Akkusativ', demoted)

def Zustandspassiv(clause, demoted = 'von'):
  Passiv(clause, 'sein', 'Partizip', 'ZUSTANDSPASSIV', 'Akkusativ', demoted)

def Rezipientenpassiv(clause, demoted = 'von'):
  Passiv(clause, 'bekommen', 'Partizip', 'REZIPIENTENPASSIV', 'Dativ', demoted)

def Modalpassiv(clause, demoted = 'von'):
  Passiv(clause, 'sein', 'zu-Infinitiv', 'MODALPASSIV', 'Akkusativ', demoted)

def Passiv(clause, auxiliary = 'werden', nonfinite = 'Partizip', name = 'VORGANGSPASSIV', promoted = 'Akkusativ', demoted = 'von'):
  # add light verb
  addlightverb(clause, auxiliary, nonfinite, name)
  # change arguments
  for node in clause.findall('ARGUMENT'):
    leaf = list(node.iter())[-1]
    if leaf.get('case') == 'Nominativ':
      ET.SubElement(node, name, attrib = {'case': demoted})
    if leaf.get('case') == promoted:
      ET.SubElement(node, name, attrib = {'case': 'Nominativ'})
      # default order nominative first
      clause.insert(1, node)

def ReflexivErlebniskonversiv(clause):
  # get verb to find junture from lexicon
  verb = clause.get('verb')
  juncture = Verben[verb]['Konversiv']
  # change arguments
  for node in clause.findall('ARGUMENT'):
    leaf = list(node.iter())[-1]
    if leaf.get('case') == 'Nominativ':
      ET.SubElement(node, 'ERLEBNISKONVERSIV', attrib = {'case': juncture})
    if leaf.get('case') == "Akkusativ":
      ET.SubElement(node, 'REFLEXIV', attrib = {'case': 'Akkusativ'})
      ET.SubElement(node, 'ERLEBNISKONVERSIV', attrib = {'case': 'Nominativ'})
      # default order nominative first
      clause.insert(1, node)

# ======
# Phrase
# ======

def Phrase(addto, juncture = None):
  # abreviations
  sub = upSubClause(addto)
  parent = addto.getparent()
  role = addto.find(f'*[@role="{juncture}"]')
  # possibilities
  if role is not None or (addto.tag == 'KOORDINATION' and sub.tag == 'ARGUMENT'):
    node = Argumentphrase(addto, juncture)
  elif addto.tag == 'SATZ' or (addto.tag == 'KOORDINATION' and parent.tag == 'SATZ'):
    node = Adverbialphrase(addto, juncture)
  elif addto.tag == 'PHRASE' or addto.tag == 'KOORDINATION':
    node = Attributphrase(addto, juncture)
  # check vorfeld
  vorfeld(node)
  # return for referent
  return node

def Referent(phrase, referent = None):
  # with empty head, gender is needed
  if referent in list('mnfp'):
    Genuskopf(phrase, referent)
  # insert personal pronoun
  elif referent[:1] in list('012'):
    Pronomen(phrase, referent)
  # make reference to another referent
  elif (referent in Teilnehmer or referent in list('e')) and phrase.get('new') is None:
    Anapher(phrase, referent)
  # insert noun
  else:
    Nomen(phrase, referent)
  # send to articulator
  clause = upClause(phrase)
  if phrase.getparent().tag != 'KOORDINATION':
    articulator(clause)

# =======
# Phrasen
# =======

def Argumentphrase(clause, role = None):
  # also includes prädikativ here
  argument = clause.find(f'*[@role="{role}"]')
  # simply add phrase to end of the koordination
  if clause.tag == 'KOORDINATION':
    case = clause.get('case')
    phrase = ET.SubElement(clause, 'PHRASE', attrib = {'case': case})
    # put conjunction in right position
    shiftconjunction(clause)
    return phrase
  # Check for already filled predicative: do not add another phrase then
  # this happens with lexicalised constructions like 'Angst haben'
  elif role == 'Prädikativ' and argument.find('PHRASE') is not None:
    return phrase
  # ----
  # go to tip of branch to add stuff
  leaf = list(argument.iter())[-1]
  # get the prepositional juncture, if available
  case = leaf.get('case')
  if case in Präpositionen:
    ET.SubElement(leaf, 'JUNKTOR').text = case
    # special case assignment for governed prepositions
    if case in ['an', 'in', 'auf', 'über']:
      case = 'Akkusativ'
    else:
      case = Präpositionen[case]
  # add phrase
  phrase = ET.SubElement(leaf, 'PHRASE', attrib = {'case': case})
  return phrase

def Adverbialphrase(clause, connection = None):
  # prepare node
  node = ET.Element('ADVERBIALE')
  # prepositionphrase
  if connection is not None:
    ET.SubElement(node, 'JUNKTOR').text = connection
    phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionen[connection]})
  # No juncture then measure-phrase in accusative, e.g. 'den ganzen Tag'
  else:
    phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Akkusativ'})
  # insert before predicate
  predicate = clause.xpath('PRÄDIKATIV|PRÄDIKAT')
  if len(predicate) > 0:
    predicate[0].addprevious(node)
  else:
    clause.append(node)
  # put conjunction in right position
  if clause.tag == 'KOORDINATION':
    shiftconjunction(clause)
  return phrase

def Attributphrase(phrase, connection = None):
  # prepare node
  node = ET.Element('ATTRIBUT')
  # prepositionphrase
  if connection is not None:
    ET.SubElement(node, 'JUNKTOR').text = connection
    newphrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionen[connection]})
  # for coordination: when added to empty phrase, then new phrase is doubled, later replaced by coordination
  elif len(phrase) == 0:
    case = phrase.get('case')
    newphrase = ET.SubElement(phrase, 'PHRASE', attrib = {'case': case})
    return newphrase
  # or add phrase to conjunction
  elif phrase.tag == 'KOORDINATION':
    case = phrase.get('case')
    newphrase = ET.SubElement(phrase, 'PHRASE', attrib = {'case': case})
    # put conjunction in right position
    shiftconjunction(phrase)
  # Genitive when no juncture
  else:
    newphrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Genitiv'})
  # simply add to end of phrase
  phrase.append(node)
  return newphrase

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

def Neu(phrase):
  # ignore anaphor and make a full noun phrase instead
  phrase.set('new', 'True')

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
    node = ET.SubElement(determiner, 'DEMONSTRATIV')
    node.text = Demonstrativpronomina[case][gender]
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

# this is like PHRASE/SATZ, but only necessary for this one situation
def Link(clause):
  return clause.find('PRÄDIKATIV')

def Addendum(addto, adword):
  # choices
  if addto.tag in ['SATZ', 'PRÄDIKATIV']:
   node = Adverbiale(addto, adword)
  elif addto.tag == 'PHRASE':
    node = Attribut(addto, adword)
  elif addto.tag == 'KOORDINATION':
    node = Addendumkoordination(addto, adword)
  # send to articulator
  if addto.tag != 'KOORDINATION':
    articulator(addto)
  # check Vorfeld
  vorfeld(node)
  # return for specification
  return node

# ======= 
# Addenda
# =======

def Attribut(phrase, adword):
  # make new node
  attribute = ET.Element('ATTRIBUT')
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
  return attribute

def Adverbiale(clause, adword):
  # insert adverbial
  adverbial = ET.SubElement(clause, 'ADVERBIALE')
  if adword in Adjektive:
    ET.SubElement(adverbial, "ADJEKTIV").text = adword
  else:
    ET.SubElement(adverbial, "ADVERB").text = adword
  # location to insert
  predicate = clause.xpath('PRÄDIKATIV|PRÄDIKAT')
  # without predication, this a vorfeld adverbial
  if len(predicate) == 0:
    clause.append(adverbial)
  # normally: attach before predicate
  else:
    predicate[0].addprevious(adverbial)
  return adverbial

def Addendumkoordination(coordination, adword):
  # link to node above, then move into coordination
  parent = coordination.getparent()
  addendum = Addendum(parent, adword)
  coordination.append(addendum)
  # put conjunction in right position
  shiftconjunction(coordination)
  return coordination

# ===========
# Eingrenzung
# ===========

def Grad(adjective, intensifier):
  # insert Gradpartikel before adjective
  node = ET.Element('GRADPARTIKEL')
  adjective.insert(0, node)
  # attributes for interrogative
  mood = upClause(adjective).get('mood')
  position = upSubClause(adjective).tag.capitalize()
  # interrogative
  if mood == 'Frage' and position == 'Vorfeld':
    node.text = 'wie'
  else:
    node.text = intensifier

def Adverbialpräposition(adverbial, preposition):
  # insert before adverbial
  node = ET.Element('ADVERBIALPRÄPOSITION')
  node.text = preposition
  adverbial.insert(0, node)

# after some prepositions it is possible to add an adverb:
# bis morgen, seit gestern, ab heute, von gestern
# nach links, von hier, nach oben, für gleich  

# Also with general adverbials:
# bis in den frühen Morgen
# seit unser letztes Treffen

# NOTE: the following is a combination of two adverbials
# "vorne/hinten im Garten"
# they have to be inserted separately
# semantics are inferred from regular scoping of multiple modifiers
# also for 'noch nicht' ???

# TODO: what about 'nur heute' ? cf. Fokuspartikel!?

# ============
# Koordination
# ============

def Koordination(addto, conjunction = 'und'):
  parent = addto.getparent()
  if parent is not None:
    grandparent = parent.getparent()
  # prepare koordination node and attach original coordinant
  coordination = ET.Element('KOORDINATION')
  # do nothing special for main clauses
  if addto.tag == 'SATZ' and addto.get('kind') == 'Hauptsatz':
    coordination.set('kind', addto.get('kind'))
  else:
    # === settings ===
    if addto.tag == 'SATZ':
      kind = addto.get('kind')
      coordination.set('kind', kind)
      # for relative clause reference
      if kind in 'Relativsatz':
        coordination.set('gender', addto.get('relative'))
        coordination.set('referent', addto.get('head'))
    elif addto.tag == 'PHRASE':
      case = addto.get('case')
      coordination.set('case', case)
    # === insertion ====
    # simple insertion with addendum
    if addto.tag in ['ATTRIBUT', 'ADVERBIALE']:
      addto.addnext(coordination)
      coordination.append(addto)
    # doubling of whole attributes/adverbial nodes, both for SATZ and PHRASE
    elif parent.tag in ['ATTRIBUT', 'ADVERBIALE']:
      parent.addnext(coordination)
      coordination.append(parent)
    # double-S/P trick, leading to coordination under the same juncture, both for:
    # addto.tag == 'PHRASE' and parent.tag == 'PHRASE'
    # addto.tag == 'SATZ' and parent.tag == 'SATZ'
    elif grandparent.tag in ['ATTRIBUT', 'ADVERBIALE']:
      parent.addnext(coordination)
      coordination.append(addto)
      grandparent.remove(parent) # delete superfluous node
    # leftovers: simple insertion for arguments
    elif addto.tag == 'PHRASE':
      addto.addnext(coordination)
      coordination.append(addto)
  # add conjunction to end
  conjunction = '' if conjunction == None else conjunction
  conj = ET.Element('KONJUNKTION')
  conj.text = conjunction
  coordination.append(conj)
  return coordination

# ========
# Satzende
# ========

def Ende(satz, clean = True):
  # optional cleanup of attributes for readability
  if clean:
   cleanup(satz)

def articulator(addto):
  # send content everything before to articulator
  # ----
  # verb agreement is triggered by this
  if addto.tag == 'SATZ':
    if addto.get('person') is not None and addto.get('agreement') is None:
      verbkongruenz(addto)
      addto.set('agreement', 'done')

def vorfeld(node):
  clause = upClause(node)
  branch = upSubClause(node)
  vorfeld = clause.find('VORFELD')
  if vorfeld is not None: # because of infinit clauses
    if len(vorfeld) == 0:
      kind = clause.get('kind')
      mood = clause.get('mood')
      if kind in ['Komplementsatz'] and mood != 'Frage':
        node = ET.SubElement(vorfeld, 'VORFELDERSATZ')
        if clause.get('truth') == 'Unbestimmt':
          node.text = 'ob'
        else:
          node.text = 'dass'
      else:
        vorfeld.append(branch)

def verbkongruenz(clause):
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
    # insert position-filling 'es' when nothing in Vorfeld yet
    # Subject-replacing 'es' only occurs through diathesis
    vorfeld = clause.find('VORFELD')
    if len(vorfeld) == 0:
      ET.SubElement(vorfeld, 'VORFELDERSATZ').text = 'es'
  # --- Movement in subordinate clauses ---
  else:
    # reorder Erstatzinfinitiv in subordinate clauses
    if clause.get('cluster') == 'Ersatzinfinitiv':
      # leave trace
      ET.SubElement(finitum, 'FINITUM', attrib = {'move': 'Finiterst'})
      # move finite to front of verb cluster
      predicate = clause.find('PRÄDIKAT')
      predicate.insert(0, node)

def passPersonNumber(phrase, case, person, gender):
  number = 'Plural' if gender == 'Plural' else 'Singular'
  clause = upClause(phrase)
  constituent = upSubClause(phrase)
  # verb agreement flagging
  # only for nominative in argument (not for predicative nominative!)
  if case == 'Nominativ' and checkArgument(phrase):
    # check whether already present, in case of coordination
    existing = clause.get('person')
    if existing is not None:
      # person hierarchy
      person = min(existing, person)
      number = 'Plural'
    # set flags for verb agreement at clause level
    clause.set('person', person)
    clause.set('number', number)
  # setting argument-attached reflexives from diathesis
  reflexive = constituent.find('.//REFLEXIV')
  if reflexive is not None:
    case = reflexive.get('case')
    if person in list('12'):
      pronoun = Personalpronomina[number][person][case]
    else:
      pronoun = 'sich'
    reflexive.text = pronoun
    # move reflexive to other side of branch and detach from it
    constituent.addnext(reflexive)

def shiftconjunction(coordination):
  conjunction = coordination.find('KONJUNKTION')
  goal = len(coordination) - 1
  coordination.insert(goal, conjunction)

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
  new = ET.SubElement(node.getparent(), label, attrib = {'verb': auxiliary})
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
  phrase = clause.getparent().getparent()
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
  while node.tag != 'PHRASE':
    node = node.getparent()
  return node

def upClause(node):
  # ignore when at root
  if node.getparent() is None:
    return node
  # go up to clause, also when already at clause
  while node.getparent().tag != 'SATZ':
    node = node.getparent()
  return node.getparent()

def upSubClause(node):
  # ignore when at root
  if node.getparent() is None:
    return node
  # go up last node in branch before clause
  while node.getparent().tag != 'SATZ':
    node = node.getparent()
  return node

def findcase(clause, value):
  # find cased argument after diatheses
  result = None
  for child in clause:
    if child.tag == 'ARGUMENT':
      for node in child.iter():
        if node.tag in ['PHRASE', 'KOORDINATION'] and node.get('case') == value:
          result = node
          break
        if node.tag == 'SATZ':
          break
  return result

def checkArgument(node):
  # check whether node is in an argument branch
  while node.tag != 'ARGUMENT':
    node = node.getparent()
    if node.tag == 'SATZ':
      return False
    else:
      return True

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
  for node in satz.findall('.//KONTROLLSATZ'):
    keep = ['kind', 'head']
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
  # recursion part
  recursion = spec[0].lstrip()
  recursion = recursion.split(':')
  recursion = [x.strip() for x in recursion]
  lexeme = recursion[-1]
  connection = recursion[0] if len(recursion) == 2 else ''
  # specification part
  features = ''
  early = ''
  if len(spec) > 1:
    parts = spec[1].split(' + ')
    for part in parts:
      feature = part.split(': ')
      # early features
      if feature[0] in earlyfeatures:
        early = early + feature[0] + '(' + id + ')\n'
      # lexical abbreviations
      elif feature[0][:1].islower():
        if feature[0] in Modalverben:
          features = features + 'Modalverb(' + id + ', \'' + feature[0] + '\')\n'
        elif feature[0] in Quantoren:
          features = features + 'Quantor(' + id + ', \'' + feature[0] + '\')\n'
      else:
        if len(feature) == 1:
          features = features + feature[0] + '(' + id + ')\n'
        else:
          features = features + feature[0] + '(' + id + ', \'' + feature[1] + '\')\n'
  # build commands
  if lexeme in Adverbien + Frageadverbien + Negationen + Adjektive:
    if connection == 'Prädikativ':
      return id + ' = Addendum(Link(' + ref + '), \'' + lexeme + '\')\n' + features
    else:
      return id + ' = Addendum(' + ref + ', \'' + lexeme + '\')\n' + features
  elif isReferential(lexeme) or lexeme == '':
    linkage = 'Phrase'
    content = 'Referent'
  else:
    linkage = 'Satz'
    content = 'Prädikat'
  # conjunction
  if connection in Konjunktionen:
    linkage = 'Koordination'
  # options linkage
  if linkage == 'Satz' and lineNr == head:
    linkage = ''
  elif connection == '':
    linkage = id + ' = ' + linkage + '(' + ref + ')\n'
  else:
    linkage = id + ' = ' + linkage + '(' + ref + ', \'' + connection + '\')\n'
  # options content
  if lexeme == '':
    content = ''
  else:
    content = content + '(' + id + ', \'' + lexeme + '\')\n'
  # all combined
  return linkage + early + content + features

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

earlyfeatures = ['Plural', 'Bewegung', 'Belebt', 'Unbestimmt', 'Neu']

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
