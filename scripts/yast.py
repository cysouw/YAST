import re
from lxml import etree as ET
from lexicon import *

# ====
# Satz
# ====

def Satz(addto = None, juncture = None, *early):
  # start new sentence
  if addto is None:
    return Hauptsatz()
  else:
    # look for lexical roles
    if addto is not None:
      role = addto.find(f'*[@role="{juncture}"]')
    # different options for subordinate clauses
    if role is not None:
      node = Komplementsatz(addto, juncture, *early)
    elif addto.tag == 'SATZ':
      if juncture in Subjunktionen:
        node = Subjunktionsatz(addto, juncture)
      elif juncture in Satzpartizipien + Satzpräpositionen:
        node = Präpositionssatz(addto, juncture)
      elif juncture in Relatorsubjunktionen:
        node = Adverbialrelativsatz(addto, juncture)
      else:
        node = Relativsatz(addto, juncture)
    elif addto.tag == 'PHRASE':
        node = Relativsatz(addto, juncture)
    # check vorfeld
    Vorfeld(node)
    # return for predicate
    return node

   #elif juncture in Genera:
   #  return Pronominalrelativsatz(addto, juncture)
   #elif addto.tag == 'SATZ' and juncture
   #elif addto.tag == 'SATZ' and addto[0] is not None:
   #  return Weiterführungssatz(addto)
   #elif addto.tag == 'PHRASE':
   #elif addto.tag in ['KOORDINATION', 'SATZ']:
   #  return Satzkoordination(addto, juncture)

def Prädikat(clause, verb):
  if verb.split()[0] in Kopula:
    Prädikativ(clause, verb)
  elif verb == 'haben':
    Besitz(clause, verb)
  else:
    Verb(clause, verb)

# =====
# Sätze
# =====

# 'Vollsatz': only Hauptsatz and Subjunktionsatz
# TODO conjunction reduction
# NOTE Konjunktionaladverbien are Hauptsatz-Coordination with adverb in Vorfeld

# TODO structures like 'wenn - dann', subordinate sentence to the front, but with 'dann' in Vorfeld
# Conditional: Wenn er kommt, dann gehe ich. 
# Temporal: Ich gehe wenn er kommt.

# TODO without juncture possible in Vorfeld, but then with 'Verberst'
# only conditional meaning?!
# e.g. "Sollte die Heizung nicht dicht sein, wird der Installateur noch einmal kommen."

# TODO sequential nature of tense
# now: pass on tense to the next clause by default

def Start():
  clause = ET.Element('SATZ', attrib = {'kind': 'Hauptsatz', 'tense': 'Präsens'})
  ET.SubElement(clause, 'VORFELD')
  return clause

def Hauptsatz(addto = None, juncture = None):
  # start new sentence
  if addto is None:
    clause = ET.Element('SATZ', attrib = {'kind': 'Hauptsatz', 'tense': 'Präsens'})
  # Hauptsatz in coordination
  else:
    tense = addto.get('tense')
    clause = ET.SubElement(addto, 'SATZ', attrib = {'kind': 'Hauptsatz', 'tense': tense})
  # add vorfeld
  ET.SubElement(clause, 'VORFELD')
  return clause

def Subjunktionsatz(clause, juncture):
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Subjunktionsatz', 'tense': tense})
  ET.SubElement(newclause, 'VORFELD')
  return newclause

def Präpositionssatz(clause, preposition):
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = preposition
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Präpositionssatz', 'tense': tense})
  ET.SubElement(newclause, 'VORFELD').text = 'dass'
  return newclause

def Komplementsatz(clause, role, *early):
  if clause.tag == 'KOORDINATION':
    leaf = clause
  else:
    node = clause.find(f'*[@role="{role}"]')
    # go to tip of branch to add junktor
    leaf = list(node.iter())[-1]
    # get the prepositional juncture, if available
    juncture = leaf.get('case')
    correlative = None
    if juncture in Präpositionen:
      correlative = ET.SubElement(leaf, 'KORRELAT')
      correlative.text = 'da' + addR(juncture) + juncture
  # add clause
  tense = clause.get('tense')
  newclause = ET.SubElement(leaf, 'SATZ', attrib = {'kind': 'Komplementsatz', 'tense': tense})
  # add default relator when not interrogative
  if 'Frage' in early:
    relator = None
  elif 'Unbestimmt' in early:
    relator = 'ob'
  else:
    relator = 'dass'
  ET.SubElement(newclause, 'VORFELD').text = relator
  # if not vorfeld: clause to back, but correlative stays
  if 'Vorfeld' not in early:
    predicate = clause.find('PRÄDIKAT')
    clause.append(node)
    if correlative is not None:
      predicate.addprevious(correlative)
      correlative.set('role', role)
  return newclause

def Relativsatz(phrase, head = None):
  # get tense from high up
  tense = upClause(phrase).get('tense')
  # make new node
  function = 'ATTRIBUT' if phrase.tag == 'PHRASE' else 'ADVERBIALE'
  node = ET.SubElement(phrase, function)
  clause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Relativsatz', 'tense': tense})
  # add relator position
  ET.SubElement(clause, 'VORFELD')
  # when no head, then extract head from phrase
  if head is None:
    gender = phrase.get('gender')
    headnode = phrase.find('REFERENT')
    if headnode is not None:
      head = headnode.text
  else:
    gender = Genera[head] if len(head) == 1 else Teilnehmer[head]
  # when there is a head, pass it on to relative clause
  if head is not None:
    clause.set('head', head)
  if gender is not None:
    clause.set('gender', gender)
  return clause

# NOTE: 'das, was' Konstruktion, 'freier Relativsatz'
# Head seems to be relative pronoun (check 'dessen')
# encoded as combination of Referenz(m/f/n/p) with relative clause.
# Adverbial relator: Die Urlauber füllen sie fleißig mit dem, was sie am Strand finden.
# gender is decided on insertion of pronoun, because relator in relative clause agrees
# Ich sehen den, der da liegt.
# die Konsequenz dessen, dass im Wettbewerb immer mehr Geld verdient wird
# e.g. "Mein Eindruck ist der, dass Sie Ihre Meinung exklusiv haben"
# article determined by case, then followed by a 'dass' Satz
# e.g. "Es ist ein vernünftiger Kompromiss, der festhält an dem, dass Klimaschutz auch und gerade Angelegenheit der deutschen Wirtschaft ist."

def Weiterführungssatz(clause, juncture = None):
  # reversed Komplementsatz: relator is always the complement-taking argument, set by Vorfeldposition
  # traditionally called 'weiterführender Relativsatz'
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Weiterführungssatz', 'tense': tense})
  return newclause

def Adverbialrelativsatz(clause, juncture):
  # only for a few seemingly newly grammaticalised connectors
  # 'Anhand dessen, wo wir leben'
  if clause.tag == 'KOORDINATION':
    node = clause
  else:
    node = ET.SubElement(clause, 'ADVERBIALE')
  tense = clause.get('tense')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Adverbialrelativsatz', 'tense': tense})
  return newclause

def Pronominalrelativsatz(phrase, gender):
  Referent(phrase, gender)
  Demonstrativ(phrase)
  clause = Relativsatz(phrase)
  clause.set('kind', 'Pronominalrelativsatz')
  return clause

def Satzkoordination(addto, juncture):
  return eval(addto.get('kind'))(addto, juncture)
# put conjunction in right position
# shiftconjunction(coordination)

# =====================
# Early Event Structure
# =====================

# Frage seems also necessary for the Komplementsatz 
# default relator 'dass' vs. 'ob' as determined in 'Vorfeldposition'
# Some verbs have a real choice here
# https://grammis.ids-mannheim.de/systematische-grammatik/2091

def Unbestimmt(clause):
  clause.set('truth', 'Unbestimmt')

def Frage(clause):
  clause.set('mood', 'Frage')

def Entscheidungsfrage(clause):
  clause.set('mood', 'Entscheidungsfrage')
  clause.find('VORFELD').text = ''

def Imperativ(clause):
  clause.set('mood', 'Imperativ')
  clause.find('VORFELD').text = ''

def Vorfeld(node):
  branch = upSubClause(node)
  vorfeld = branch.getparent().find('VORFELD')
  if vorfeld is not None:
    if len(vorfeld) == 0:
      vorfeld.append(branch)

def Infinit(clause):
  clause.set('tense', 'Infinit')
  # remove relator
  clause.remove(clause.find('VORFELD'))
  # complex rules for infinite relative clause
  if clause.get('kind') == 'Relativsatz':
    makeRelativecontrol(clause)
  # simple for others
  else:
    finitum = clause.find('PRÄDIKAT')[-1]
    verb = finitum.get('verb')
    ET.SubElement(finitum, 'ZU-INFINITIV').text = 'zu ' + verb

# ===========
# Prädikation
# ===========

# Nominative '-de' role is assumed by default, except when listed differently in the lexicon

def Verb(clause, verb):
  clause.set('verb', verb)
  # --- roles ---
  # start with a default nominative role, except when Nominative listed in dictionary
  if not 'Nominative' in Verben.get(verb, {}).get('Rollen', {}).values():
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
  if Verben.get(verb, {}).get('Prädikativ', False):
    predicative = ET.Element(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikativ', 'case': 'Akkusativ'})
    phrase = Phrase(predicative, 'Prädikativ')
    Referent(phrase, Verben[verb]['Prädikativ'])
    verb = Verben[verb]['Stamm']
  # add verb
  lexeme.set('verb', verb)

# combine locational, adverbial, adjectival and nominal predication
# they use the same construction in German

def Prädikativ(clause, verb):
  clause.set('verb', verb)
  # --- roles ---
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  predicative = ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikativ', 'case': 'Nominativ'})
  # --- verb ---
  parts = verb.split()
  copula = parts[0]
  # location
  if len(parts) > 1:
    ET.SubElement(predicative, 'PRÄDIKATIV', attrib = {'role': 'Ort', 'juncture': parts[1]})
  # add predicate node
  predicate = ET.SubElement(clause, 'PRÄDIKAT')
  ET.SubElement(predicate, 'VERB', attrib = {'verb': copula})

# maybe also for verbs 'besitzen' and the like?
# 'haben' could also be listed in the lexicon as a separate verb

def Besitz(clause, verb = 'haben'):
  clause.set('verb', verb)
  # --- roles ---
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Besitzer', 'case': 'Nominativ'})
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Besitz', 'case': 'Akkusativ'})
  # --- verb ---
  predicate = ET.SubElement(clause, 'PRÄDIKAT')
  ET.SubElement(predicate, 'VERB', attrib = {'verb': verb}) 

# ================
# Ereignisstruktur
# ================

def Präsens(clause):
  clause.set('tense', 'Präsens')

def Präteritum(clause):
  clause.set('tense', 'Präteritum')

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

def Phrase(addto, connection = None):
  # abreviations
  parent = addto.getparent()
  sub = upSubClause(addto)
  argument = addto.find(f'*[@role="{connection}"]')
  # possibilities
  if argument is not None or (addto.tag == 'KOORDINATION' and sub.tag == 'ARGUMENT'):
    node = Argumentphrase(addto, connection)
  elif addto.tag == 'SATZ' or (addto.tag == 'KOORDINATION' and parent.tag == 'SATZ'):
    node = Adverbialphrase(addto, connection)
  elif addto.tag == 'PHRASE' or addto.tag == 'KOORDINATION':
    node = Attributphrase(addto, connection)
  # check vorfeld
  Vorfeld(node)
  # return for referent
  return node

def Referent(phrase, referent = None):
  # with empty head, gender is needed
  if referent in list('mnfp') or referent in Genera.values():
    Genuskopf(phrase, referent)
  # insert personal pronoun
  elif referent[:1] in list('012'):
    Pronomen(phrase, referent)
  # make reference to another referent
  elif referent in Teilnehmer:
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
  # adjective can be used as head, also used in 'freier relativsatz'
  gender = Genera[referent] if len(referent) == 1 else referent
  # insert nodes
  ET.SubElement(phrase, 'DETERMINATIV')   
  ET.SubElement(phrase, 'REFERENT')
  # set flags at phrase for phrasal agreement
  phrase.set('gender', gender)
  phrase.set('declension', 'stark')
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
    mood = upClause(phrase).get('mood')
    position = upSubClause(phrase).tag.capitalize()
    # flags for agreement
    person = '3'
    number = 'Singular'
    # interrogative
    if mood == 'Frage' and position == 'Vorfeld':
      node = ET.SubElement(phrase, 'FRAGEPRONOMEN')
      node.text = Fragepronomina[animacy][case]
      gender = 'Maskulin'
    # indefinites
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
  # check verb agreement
  passPersonNumber(phrase, case, person, number)

def Anapher(phrase, referent):
  # get info from phrase
  case = phrase.get('case')
  # get gender and animacy from Teilnehmer
  gender = Teilnehmer[referent]
  # can be plural ('+3') when marked at phrase
  number = phrase.get('gender')
  gender = number if number == 'Plural' else gender
  # update Teilnehmer
  Teilnehmer[referent] = gender
  # set flags at phrase
  phrase.set('gender', gender)
  # get animacy from dictionary
  if referent in Substantive:
    animacy = Substantive[referent].get('Belebt', False) 
    animacy = 'Belebt' if animacy else 'Unbelebt'
  # Belebt when not in dictionary (for new names in Teilnehmer)
  else:
    animacy = 'Belebt'
  # get local participants for reflexivitiy
  local = upClause(phrase).get('local')
  localreferents = local.split(',') if local is not None else []
  # get clause info for relative pronoun
  kind = upClause(phrase). get('kind')
  position = upSubClause(phrase).tag.capitalize()
  # get junctor, if present, for da/wo-form
  junctornode = phrase.getparent().find('JUNKTOR')
  junctor = junctornode.text if junctornode is not None else None
  # --- make new node
  node = ET.SubElement(phrase, 'ANAPHER', attrib = {'referent': referent})
  # reflexive pronoun
  if referent in localreferents:
    node.tag = 'REFLEXIV'
    node.text = 'sich'
  # relative pronoun
  elif kind == 'Relativsatz' and position == 'Vorfeld':
    node.tag = 'RELATIV'
    node.text = Relativpronomina[case][gender]
  # inanimate prepositional anapher with 'da'
  elif junctor in Präpositionen and animacy == 'Unbelebt':
    node.text = 'da' + addR(junctor) + junctor
    junctornode.text = None
    junctornode.set('move', 'hinterAnapher')
  # anaphoric pronoun
  else:
    node.text = Anaphora[gender][case]
    # update local participants
    local = referent if local is None else local + ',' + referent
    upClause(phrase).set('local', local)
  # check verb agreement
  passPersonNumber(phrase, case, '3', gender)

def Nomen(phrase, referent):
  # get info from phrase
  case = phrase.get('case')
  number = phrase.get('gender')
  # find gender
  if referent in Teilnehmer:
    gender = Teilnehmer[referent]
    noundeclination = Substantive[referent].get('Deklination', 'stark')
  elif referent in Substantive:
    gender = Substantive[referent]['Geschlecht']
    noundeclination = Substantive[referent].get('Deklination', 'stark')
  # else assume that it is Neutrum, e.g. 'das Laufen'
  else:
    gender = 'Neutrum'
    noundeclination = 'stark'
    referent = referent.capitalize()
  # override gender from phrase
  gender = gender if number is None else number
  # add new Teilnehmer to context
  Teilnehmer[referent] = gender
  # local context within clause for reflexivity
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
  # check verb agreement
  passPersonNumber(phrase, case, '3', gender)

# =============
# Determination
# =============

def Plural(phrase):
  phrase.set('gender', 'Plural')

def Belebt(phrase):
  phrase.set('animacy', 'Belebt')

def KeinAnapher(phrase):
  # reverse anaphor and make a full noun phrase instead
  referent = phrase.xpath('ANAPHER|RELATIV')[0].get('referent')
  ET.strip_elements(phrase, '*')
  Nomen(phrase, referent)

def Definit(phrase):
  determiner = phrase.find('DETERMINATIV')
  # ignore when no determiner
  if determiner is None:
    return
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender')
  # make article
  article = Definitartikel[case][gender] 
  # insert article
  ET.strip_elements(determiner, '*')
  ET.SubElement(determiner, 'ARTIKEL').text = article
  # set declension for agreement
  phrase.set('declension', 'schwach')

def Demonstrativ(phrase):
  determiner = phrase.find('DETERMINATIV')
  # ignore when no determiner
  if determiner is None:
    return
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # make demonstrative/relative
  demonstrative = Relativpronomina[case][gender]
  # find insertion point
  ET.strip_elements(determiner, '*')
  ET.SubElement(determiner, 'DEMONSTRATIVE').text = demonstrative
  # set declension for agreement
  phrase.set('declension', 'schwach')

def Indefinit(phrase):
  # ignore when no determiner
  determiner = phrase.find('DETERMINATIV')
  if determiner is None:
    return
  # insert article node
  ET.strip_elements(determiner, '*')
  node = ET.SubElement(determiner, 'ARTIKEL')
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender')
  # attributes for interrogative
  mood = upClause(phrase).get('mood')
  position = upSubClause(phrase).tag.capitalize()
  # interrogative
  if mood == 'Frage' and position == 'Vorfeld':
    node.text = 'welch' + Adjektivflexion['stark'][case][gender]
  # make article
  elif gender == 'Plural':
    node.text = 'einig' + Adjektivflexion['stark'][case][gender]
  else:
    node.text = 'ein' + Quantorflexion['ein'][case][gender]
  # set declension for agreement
  phrase.set('declension', 'gemischt')

def Quantor(phrase, quantor = None):
  # ignore when no determiner
  determiner = phrase.find('DETERMINATIV')
  if determiner is None:
    return
  # insert quantor node
  ET.strip_elements(determiner, '*')
  node = ET.SubElement(determiner, 'QUANTOR')
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender')
  # attributes for interrogative
  mood = upClause(phrase).get('mood')
  position = upSubClause(phrase).tag.capitalize()
  # interrogative
  if mood == 'Frage' and position == 'Vorfeld':
    node.text = 'wie viel' 
    if gender == 'Plural':
      node.text = node.text + Quantorflexion['ein'][case][gender]
    declension = 'gemischt'
  # prepare the quantor as listed in the lexicon
  elif quantor in Quantoren:
    inflection = Quantoren[quantor]['Flexion']
    declension = Quantoren[quantor]['Deklination']
    node.text = quantor + Quantorflexion[inflection][case][gender]
  # set declension for adjective agreement
  phrase.set('declension', declension)

def Besitzer(phrase, referent = None): 
  # ignore when no determiner
  determiner = phrase.find('DETERMINATIV')
  if determiner is None:
    return
  # insert possessive node
  ET.strip_elements(determiner, '*')
  node = ET.SubElement(determiner, 'POSSESSSIV')
  # get attributes from phrase for agreement
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # attributes from clause
  mood = upClause(phrase).get('mood')
  kind = upClause(phrase).get('kind')
  position = upSubClause(phrase).tag.capitalize()
  # interrogative pronoun
  if mood == 'Frage' and position == 'Vorfeld':
    node.text = 'wessen'
  # relative pronoun
  elif kind == 'Relativsatz' and position == 'Vorfeld':
    referentgender = Teilnehmer[referent]
    node.text = Relativpronomina['Genitiv'][referentgender]
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
  determiner = phrase.find('DETERMINATIV')
  # ignore when no determiner
  if determiner is None:
    return
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

def Bewegung(phrase):
  # ad-hoc rule to change case of wechselprepostions
  phrase.set('case', 'Akkusativ')

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
  Vorfeld(node)
  # return for specification
  return node

# ======= 
# Addenda
# =======

def Attribut(phrase, adword):
  # make new node
  attribute = ET.Element('ATTRIBUT')
  # find referent for insertion
  #head = phrase.find('REFLEXIV')
  head = phrase.xpath('REFERENT|ANAPHOR|REFLEXIV|PRONOUN')[0]
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

def Satzende(satz, clean = True):
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
  # --- Relator ---
  else:

    # reorder Erstatzinfinitiv in subordinate clauses
    if clause.get('cluster') == 'Ersatzinfinitiv':
      # leave trace
      ET.SubElement(finitum, 'FINITUM', attrib = {'move': 'Finiterst'})
      # move finite to front of verb cluster
      predicate = clause.find('PRÄDIKAT')
      predicate.insert(0, node)

# ==============
# help functions
# ==============

def upPhrase(node):
  # go up to phrase, but not when already at a phrase
  while node.tag != 'PHRASE':
    node = node.getparent()
  return node

def upClause(node):
  # go up to clause
  while node.tag != 'SATZ' and node.get('tense') != 'Infinit':
    node = node.getparent()
  return node

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

def verbstem(verb):
  # common -en infinitive
  if verb[-2:] == 'en':
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
  if verb not in Verben or tense not in Verben[verb]:
    stem = verbstem(verb)
    if tense == 'Präsens' and stem[-1:] in list('td'):
      if person == '2' or (person == '3' and number == 'Singular'):
        stem = stem + 'e'
    elif tense == 'Präsens' and stem[-1:] in list('mn') and stem[-2:-1] not in list('mnrl'):
      if person == '2' or (person == '3' and number == 'Singular'):
        stem = stem + 'e'
    finite = stem + Verbflexion[tense][number][person]
    # drop of 's' in second singular
    if tense == 'Präsens' and stem[-1:] in list('szxß'):
      if person == '2' and number == 'Singular':
        finite = finite[:-2] + 't'
    # reversal in first singular
    elif tense == 'Präsens' and stem[-2:] == 'el':
      if person == '1' and number == 'Singular':
        finite = finite[:-3] + 'le'
  # lookup in dictionary 
  else:
      finite = Verben[verb][tense][number][person]
  return finite

def adjectiveAgreement(phrase):
  case = phrase.get('case')
  gender = phrase.get('gender')
  declension = phrase.get('declension')
  return Adjektivflexion[declension][case][gender]

def checkArgument(node):
  # check whether node is in an argument branch
  while node.tag != 'ARGUMENT':
    node = node.getparent()
    if node.tag == 'SATZ':
      return False
    else:
      return True

def passPersonNumber(phrase, case, person, gender):
  number = 'Plural' if gender == 'Plural' else 'Singular'
  # verb agreement flagging
  # only for nominative in argument (not for predicative nominative!)
  if case == 'Nominativ' and checkArgument(phrase):
    clause = upClause(phrase)
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
  parent = phrase.getparent()
  if parent.find('REFLEXIV') is not None:
    reflexive = parent.find('REFLEXIV')
    case = reflexive.get('case')
    if person in list('12'):
      pronoun = Personalpronomina[number][person][case]
    else:
      pronoun = 'sich'
    reflexive.text = pronoun
    # move reflexive to other side of branch
    parent.append(reflexive)

def shiftconjunction(coordination):
  conjunction = coordination.find('KONJUNKTION')
  goal = len(coordination) - 1
  coordination.insert(goal, conjunction)

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
  # ignore first indent, because every sentence starts automatically
  # first indent is just for user-consistency
  #level2 = sorted(depth)[1]
  #depth = [0 if i == level2 else i for i in depth]
  return depth

def reference(file):
  depth = [0] + level(file)
  stack = {0: 0}
  ref = []
  for nr,elem in enumerate(depth[1:]):
    if elem > depth[nr]:
      ref.append(nr)
      stack.update({elem: nr})
    elif elem == depth[nr]:
      ref.append(ref[-1])
    elif elem < depth[nr]:
      ref.append(stack[elem])
  return ref

def specification(raw, lineNr, refs):
  # prepare line number
  id = 's' + str(lineNr+1)
  if lineNr == 0:
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
  base = id + ' = R(' + ref
  if len(recursion) == 1:
    recursion = base + ', \'' + recursion[0] + '\', None'
  elif len(recursion) == 2:
    if recursion[1] in ['', '-']:
      recursion = base + ', None, \'' + recursion[0] + '\''
    else:
      recursion = base + ', \'' + recursion[1] + '\', \'' + recursion[0] + '\''
  # specification part
  features = ''
  if len(spec) > 1:
    parts = spec[1].split(' + ')
    for part in parts:
      feature = part.split(': ')
      # early features
      if feature[0] in earlyfeatures:
        recursion = recursion + ', \'' + feature[0] + '\''
      # lexical abbreviations
      elif feature[0][:1].islower():
        features = features + '\nR(' + id + ', \'' + feature[0] + '\')'
      else:
        base = feature[0] + '(' + id
        # format features
        if len(feature) == 1:
          feature = base + ')'
        else:
          feature = base + ', \'' + feature[1] + '\')'
        features = features + '\n' + feature
  return recursion + ')' + features

def convert(sentence, clean = True):
  sentence = re.split('\n', sentence)
  sentence = list(filter(None, sentence))
  refs = reference(sentence)
  for nr,elem in enumerate(sentence):
    sentence[nr] = specification(elem, nr, refs) 
  rules = 's = Start()\n' + '\n'.join(sentence) + f'\nEnde(s, {clean})\n'
  return rules

def makeTree(rules):
  loc = {}
  exec(rules, globals(), loc)
  return loc['s']

# ================
# Output from file
# ================

def Syntax(file, code = False, xml = False, all = False, raw = False):
  clean = not all
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
  
# ==============
# Pure recursion
# ==============

# Choice of recursion determined by lexeme: 
# Verb (no capital, ending in -n), Nomen (capitalised), Other (only lists?)

def R(addto = None, lexeme = None, juncture = None, *early):
  # abbreviations
  if lexeme in Modalverben:
    out = Modalverb(addto, lexeme)
  elif lexeme in Quantoren:
    out = Quantor(addto, lexeme)
  # real rules
  elif lexeme is None:
    out = Phrase(addto, juncture)
  # PHRASE
  elif lexeme[:1].isupper() or lexeme[:1] in list('012') or lexeme in list('mnfp') or lexeme in Genera.values():
    out = Phrase(addto, juncture)
    for i in early:
      eval(i)(out)
    Referent(out, lexeme)
  # ADDENDUM
  elif lexeme in Adverbien + Frageadverbien + Negationen + Adjektive:
    if juncture == 'Prädikativ':
      out = Addendum(Link(addto), lexeme)
    else:
      out = Addendum(addto, lexeme)
      # temporary solution for Vorfeld
      #if juncture is not None:
      # eval(juncture)(out)
  # KOORDINATION
  elif lexeme in Konjunktionen:
    out = Koordination(addto, lexeme)
  # SATZ
  elif addto.get('kind') == 'Hauptsatz':
    for i in early:
      eval(i)(out)
    out = Prädikat(addto, lexeme)
  else:
    out = Satz(addto, juncture, *early)
    for i in early:
      eval(i)(out)
    Prädikat(out, lexeme)
  return out

earlyfeatures = ['Plural', 'Bewegung', 'Belebt', 'Vorfeld', 'Frage', 'Unbestimmt']
