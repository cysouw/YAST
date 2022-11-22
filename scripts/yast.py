import re
from lxml import etree as ET
from lexicon import *

# ==============
# Pure recursion
# ==============

# Choice of recursion determined by lexeme: 
# Verb (no capital, ending in -n), Nomen (capitalised), Other (only lists?)

def R(addto = None, lexeme = None, juncture = None, *early):
  if lexeme is None:
    out = Phrase(addto, juncture) # or SATZ!!!
  # PHRASE
  elif lexeme[:1].isupper() or lexeme[:1] in list('12') or lexeme in list('mnfp'):
    out = Phrase(addto, juncture)
    for i in early:
      eval(i)(out)
    Referent(out, lexeme)
  # ADDENDUM
  elif lexeme in Adverbien + Frageadverbien + Negationen + Adjektive:
    if juncture == 'Prädikativ':
      link = Link(addto)
      out = Addendum(link, lexeme)
    else:
      out = Addendum(addto, lexeme)
  # KOORDINATION
  elif lexeme in Konjunktionen:
    out = Koordination(addto, lexeme)
  # SATZ
  else:
    out = Satz(addto, juncture)
    for i in early:
      eval(i)(out)
    Prädikat(out, lexeme)
  return out

earlyfeatures = ['Plural', 'Kontrolle', 'Vorfeld', 'Relator']

def Vorfeld(node):
  branch = upSubClause(node)
  vorfeld = branch.getparent().find('VORFELD')
  if len(vorfeld) == 0:
    vorfeld.append(branch)

# ====
# Satz
# ====

def Satz(addto = None, juncture = None):
  # start new sentence
  if addto is None:
    return Hauptsatz()
  else:
    # finish up everything before
    articulator(addto)
    # look for lexical roles
    if juncture is not None:
      role = addto.find(f'*[@role="{juncture}"]')
    # different options for subordinate clauses
    if juncture in Subjunktionen:
      return Subjunktionsatz(addto, juncture)
    elif juncture in Satzpartizipien + Satzpräpositionen:
      return Präpositionssatz(addto, juncture)
    elif juncture in Relatorsubjunktionen:
      return Adverbialrelativsatz(addto, juncture)
    elif juncture in Genera:
      return Pronominalrelativsatz(addto, juncture)
    elif role is not None:
      return Komplementsatz(addto, juncture)
    elif addto.tag == 'SATZ' and addto[0] is not None:
      return Weiterführungssatz(addto)
    elif addto.tag == 'PHRASE':
      return Relativsatz(addto)
    elif addto.tag in ['KOORDINATION', 'SATZ']:
      return Satzkoordination(addto, juncture)

def Prädikat(clause, verb):
  if verb.split()[0] in Kopula:
    Prädikativ(clause, verb)
  elif verb == 'haben':
    Besitz(clause, verb)
  else:
    Verb(clause, verb)

# ========
# Vollsatz
# ========

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
  return newclause

def Präpositionssatz(clause, preposition):
  tense = clause.get('tense')
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = preposition
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Präpositionssatz', 'tense': tense})
  ET.SubElement(newclause, 'RELATOR').text = 'dass'
  return newclause

# ===========
# Relatorsatz
# ===========

# In komplementsatz there is a special structure when Relator is argument of embedded clause
# then you get 'was' for phrases and 'wo+prep' for prepositional phrases
# Weiterführungssatz only allows these constructions

def Komplementsatz(clause, role):
  if clause.tag == 'KOORDINATION':
    leaf = clause
  else:
    node = clause.find(f'*[@role="{role}"]')
    # move node to end of sentence
    clause.append(node)
    # go to tip of branch to add junktor
    leaf = list(node.iter())[-1]
    # add phrase
    juncture = leaf.get('juncture')
    # governed prepositions
    if role in Präpositionen:
      juncture = role
    if juncture is not None:
      ET.SubElement(leaf, 'JUNKTOR').text = 'da' + addR(juncture) + juncture
      node.set('move', 'da-Junktor')
  tense = clause.get('tense')
  newclause = ET.SubElement(leaf, 'SATZ', attrib = {'kind': 'Komplementsatz', 'tense': tense})
  return newclause

def Weiterführungssatz(clause, juncture = None):
  # reversed Komplementsatz: relator is always the complement-taking argument, set by Vorfeldposition
  # traditionally called 'weiterführender Relativsatz'
  node = ET.SubElement(clause, 'ADVERBIALE')
  tense = clause.get('tense')
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Weiterführungssatz', 'tense': tense})
  return newclause

def Adverbialrelativsatz(clause, juncture):
  # only for a few seemingly newly grammaticalised connectors
  # 'Anhand dessen, wo wir leben'
  if clause.tag == 'KOORDINATION':
    node = clause
  else:
    node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  tense = clause.get('tense')
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Adverbialrelativsatz', 'tense': tense})
  return newclause

def Relativsatz(phrase, juncture = None):
  relative = phrase.get('gender')
  head = phrase.get('referent')
  tense = upClause(phrase).get('tense')
  if phrase.tag == 'KOORDINATION':
    node = phrase
  else:
    node = ET.SubElement(phrase, 'ATTRIBUT')
  clause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Relativsatz', 'head': head, 'relative': relative, 'tense': tense})
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

def Pronominalrelativsatz(phrase, gender):
  Referent(phrase, gender)
  Demonstrativ(phrase)
  clause = Relativsatz(phrase)
  clause.set('kind', 'Pronominalrelativsatz')
  return clause

# ============
# Kontrollsatz
# ============

# TODO: trace 'es' sometimes possible, sometimes required
# e.g. 'Ich habe es beim Sport gehasst, rennen zu müssen.'

def Kontrollsatz(clause, role):
  newclause = Komplementsatz(clause, role)
  Infinit(newclause)
  return newclause

def Präpositionskontrollsatz(clause, juncture):
  newclause = Präpositionssatz(clause, juncture)
  Infinit(newclause)
  return newclause

def Partizipsatz(phrase, juncture = None):
  clause = Relativsatz(phrase, juncture)
  Infinit(clause)
  return clause

# ====================
# Clause Determination
# ====================

def Satzkoordination(addto, juncture):
  return eval(addto.get('kind'))(addto, juncture)
# put conjunction in right position
# shiftconjunction(coordination)

# attribute clauses can be detached to become secondary predicates
# Partizipsatz only in Vorzeit/Zustand. Detached Nachzeit does not seem to occur?

def Frei(clause):
  clause.set('position', 'Adverbial')

  # no agreement here!
  # also for real adjectives? syntactically the same as adverbials!
  if clause.get('kind') == 'Partizipsatz':
    pass
  # relative clauses move to after predicate of containing clause
  elif clause.get('kind') == 'Relativsatz':
    clause.set('move', 'hinterVerb')
    clause = clause.getparent()
    while clause.tag != 'SATZ':
      clause = clause.getparent()
    predicate = clause.find('PRÄDIKAT')
    predicate.addnext(clause.getparent())

# =====================
# Early Event Structure
# =====================

# Frage seems also necessary for the Komplementsatz 
# default relator 'dass' vs. 'ob' as determined in 'Vorfeldposition'
# Some verbs have a real choice here
# https://grammis.ids-mannheim.de/systematische-grammatik/2091

def Frage(clause):
  clause.set('mood', 'Inhaltsfrage')

def Entscheidungsfrage(clause):
  clause.set('mood', 'Entscheidungsfrage')
  clause.find('VORFELD').text = ''

def Imperativ(clause):
  clause.set('mood', 'Imperativ')
  clause.find('VORFELD').text = ''

def Kontrolle(clause):
  clause.set('???', 'Kontrolle')
  kind = clause.get('kind')
  # move relativsatz inside phrase
  if kind == 'Relativsatz':
    attribute = clause.getparent()
    phrase = attribute.getparent()
    referent = phrase.find('REFERENT')
    referent.addprevious(attribute)
  # change names
  clause.tag = 'KONTROLLSATZ'
  kind = 'Kontroll' + kind.lower()
  clause.set('kind', kind)
  clause.set('tense', 'Infinit')

# turn finite sentences into controlled sentences

# TODO: local not clear!!!

def Infinit(clause):
  kind = clause.get('kind')
  clause.set('tense', 'Infinit')
  # make Kontrollsatz
  if kind == 'Komplementsatz':
    clause.set('kind', 'Kontrollsatz')
    # find controlling clause
    control = clause.getparent()
    while control.tag != 'SATZ':
      control = control.getparent()
    setcontrol(control, clause)
  # make Präpositionskontrollsatz
  elif kind == 'Präpositionssatz':
    clause.set('kind', 'Präpositionskontrollsatz')
    # find controlling clause
    control = clause.getparent().getparent()
    setcontrol(control, clause)
    # remove 'dass' from Präpositionssatz
    dass = clause.find('RELATOR')
    clause.remove(dass)
  # make Partizipsatz
  elif kind == 'Relativsatz':
    clause.set('kind', 'Partizipsatz')
    # find controlling phrase
    parent = clause.getparent()
    grandparent = parent.getparent()
    # move clause to adjective position
    if parent.tag == 'KOORDINATION':
      setcontrol(parent, clause)
      parent.append(clause)
    elif grandparent[0].tag == 'DETERMINATIV':
      setcontrol(grandparent, clause)
      grandparent.insert(1, parent)
    else:
      setcontrol(grandparent, clause)
      grandparent.insert(0, parent)

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
    ET.SubElement(lexeme, 'PRÄVERBIALE').text = Verben[verb]['Präverb']
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
  
def Perfekt(clause):
  # get info
  node = clause.find('PRÄDIKAT')[-1]
  verb = node.get('verb')
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

def Modalverb(clause, modal):
  addlightverb(clause, modal, 'Infinitiv', 'MODALVERB')

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
  # finish up everything before
  articulator(addto)
  # abreviations
  parent = addto.getparent()
  sub = upSubClause(addto)
  argument = addto.find(f'*[@role="{connection}"]')
  # possibilities
  if argument is not None or (addto.tag == 'KOORDINATION' and sub.tag == 'ARGUMENT'):
    return Argumentphrase(addto, connection)
  elif addto.tag == 'SATZ' or (addto.tag == 'KOORDINATION' and parent.tag == 'SATZ'):
    return Adverbialphrase(addto, connection)
  elif addto.tag == 'PHRASE' or addto.tag == 'KOORDINATION':
    return Attributphrase(addto, connection)

def Referent(phrase, referent = None):
  # with empty head, gender is needed
  if referent in list('mnfp'):
    Genuskopf(phrase, referent)
  # insert personal pronoun
  elif referent[:1] in list('12'):
    Pronomen(phrase, referent)
  # make reference to another referent
  elif referent in Teilnehmer:
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
  # optionally, specify number as 'p'
  if len(person) > 1:
    number = 'Plural'
    person = person[:1]
  # make new node
  node = ET.SubElement(phrase, 'PRONOMEN', attrib = {'person': person, 'number': number})
  node.text = Personalpronomina[number][person][case]
  # set flags at phrase for relative clause
  phrase.set('gender', number)
  # check verb agreement
  passPersonNumber(phrase, case, person, number)

def Anapher(phrase, referent):
  # get info from phrase
  case = phrase.get('case')
  # get gender from Teilnehmer
  gender = Teilnehmer[referent]
  # can be plural ('+3') when marked at phrase
  number = phrase.get('gender')
  gender = number if number == 'Plural' else gender
  # update Teilnehmer
  Teilnehmer[referent] = gender
  # make new node
  node = ET.SubElement(phrase, 'ANAPHER', attrib = {'referent': referent})
  # set flags at phrase for relative clause
  phrase.set('gender', gender)
  # local participants for reflexivitiy
  local = upClause(phrase).get('local')
  referents = local.split(',') if local is not None else []
  # reflexive
  if referent in referents:
    node.tag = 'REFLEXIV'
    node.text = 'sich'
  # anapher
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

def KeinAnapher(phrase):
  # reverse anaphor and make a full noun phrase instead
  referent = phrase.find('ANAPHER').get('referent')
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

def Indefinit(phrase):
  determiner = phrase.find('DETERMINATIV')
  # ignore when no determiner
  if determiner is None:
    return
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # make article
  inflection = Quantoren['ein']['Flexion']
  article = 'ein' + Quantorflexion[inflection][case][gender]
  # insert article
  ET.strip_elements(determiner, '*')
  ET.SubElement(determiner, 'ARTIKEL').text = article
  # set declension for agreement
  phrase.set('declension', 'gemischt')

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

def Quantor(phrase, quantor):
  determiner = phrase.find('DETERMINATIV')
  # ignore when no determiner
  if determiner is None:
    return
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # prepare the quantor as listed in the lexicon
  if quantor in Quantoren:
    inflection = Quantoren[quantor]['Flexion']
    declension = Quantoren[quantor]['Deklination']
    quantor = quantor + Quantorflexion[inflection][case][gender]
  # insert quantor
  ET.strip_elements(determiner, '*')
  ET.SubElement(determiner, 'QUANTOR').text = quantor
  # set declension for agreement
  phrase.set('declension', declension)

def Besitzer(phrase, referent = None): 
  determiner = phrase.find('DETERMINATIV')
  # ignore when no determiner
  if determiner is None:
    return
  # get attributes from phrase for agreement
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # prepare possessive pronoun
  if referent is None:
    pronoun = referent
  elif referent[:1] in list('12'):
    person = referent[:1]
    number = 'Plural' if len(referent) > 1 else 'Singular'
    pronoun = Personalpronomina[number][person]['Attributiv']
    # add inflection
    pronoun = pronoun + Quantorflexion['ein'][case][gender]
  else:
    person = '3'
    gender = Teilnehmer[referent]
    pronoun = Anaphora[gender]['Attributiv']
    # add inflection
    pronoun = pronoun + Quantorflexion['ein'][case][gender]
  # insert possessive
  ET.strip_elements(determiner, '*')
  ET.SubElement(determiner, 'POSSESSSIV').text = pronoun
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

# ========
# Addendum
# ========

# this is like PHRASE/SATZ, but only necessary for this one situation
def Link(clause):
  return clause.find('PRÄDIKATIV')

def Addendum(addto, adword):
  # finish up everything before
  articulator(addto)
  # choices
  if addto.tag in ['SATZ', 'PRÄDIKATIV']:
    return Adverbiale(addto, adword)
  elif addto.tag == 'PHRASE':
    return Attribut(addto, adword)
  elif addto.tag == 'KOORDINATION':
    return Addendumkoordination(addto, adword)

# ======= 
# Addenda
# =======

def Attribut(phrase, adword):
  # make new node
  attribute = ET.Element('ATTRIBUT')
  # find referent for insertion
  referent = phrase.find('REFERENT')
  # ignore when no 'real' referent TODO: maybe change to relative clause?
  if referent is None:
    return
  # move node after referent when adverb, e.g. 'das Treffen gestern', also for 'selbst'
  if adword in Adverbien:
    referent.addnext(attribute)
    ET.SubElement(attribute, "ADVERB").text = adword
  # else insert adjective before referent
  elif adword in Adjektive:
    referent.addprevious(attribute)
    # adjective agreement
    case = phrase.get('case')
    gender = phrase.get('gender')
    declension = phrase.get('declension')
    adjective = adword + Adjektivflexion[declension][case][gender]
    # insert adjective
    ET.SubElement(attribute, "ADJEKTIV").text = adjective
    # adjective as head
    referent = phrase.find('REFERENT')
    if referent.text is None:
      # make head, remove attribute node
      referent.text = adjective.capitalize()
      phrase.remove(attribute)
      # add to Teilnehmer
      name = adword.capitalize() + 'e'
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

def Gradpartikel(adjective, intensifier):
  # insert before adjective
  node = ET.Element('GRADPARTIKEL')
  node.text = intensifier
  adjective.insert(0, node)

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

# =======
# Relator
# =======

# has to be combined in 'unbestimmt' below

  ## ======
  ## For relators: add info to all phrases
  #relative = addto.get('relative')
  #if relative is not None:
  #  phrase.set('relative', relative)
  #kind = addto.get('kind')
  #if kind is not None:
  #  phrase.set('kind', kind)
  ## ======
  #return phrase

def Relator(node):
  # set relator attribute
  node.set('position', 'Relator')
  # get attributes from phrase
  case = node.get('case')
  relative = node.get('relative')
  kind = node.get('kind')
  # ===
  # attributive relative pronoun as genitive
  # when added to phrase with reference/determiner
  # ===
  determiner = node.find('DETERMINATIV')
  if determiner is not None:
    # prepare genitive relative pronoun
    pronoun = Relativpronomina['Genitiv'][relative]
    # set flags for agreement
    node.set('declension', 'gemischt')
    # insert relative pronoun as article
    article = determiner.find('ARTIKEL')
    if article is not None:
      article.tag = 'RELATOR'
      article.text = pronoun
      article.set('relative', relative)
      article.set('case', 'Genitiv')
    else:
      ET.SubElement(determiner, 'RELATOR', attrib = {'relative': relative, 'case': 'Genitiv'}).text = pronoun
  # ===
  # prepositional relators
  # only with embedded complementclause!
  # assume that they are coded correctly. Role checking will be done with fronting
  # ===
  elif kind in ['Komplementsatz', 'Adverbialrelativsatz']:
    juncture = node.getparent().find('JUNKTOR')
    if juncture is not None:
      juncture.text = 'wo' + addR(juncture.text) + juncture.text
      juncture.tag = 'RELATOR'
      juncture.set('position', 'Relator')
      node.getparent().remove(node)
    else:
      node.clear()
      node.tag = 'RELATOR'
      node.text = Fragepronomina[case]
      node.set('position', 'Relator')
  # ===
  # ignore relators for Weiterführungssatz: they are automatically generated
  # this only occurs with embedded complementclauses
  # ===
  elif kind == 'Weiterführungssatz':
    node.attrib.pop('position')
  # ===
  # regular relative pronoun
  # ===
  elif kind in ['Relativsatz', 'Pronominalrelativsatz']:
    # remove any existing referent
    ET.strip_elements(node, '*')
    # insert relative pronoun
    relator = ET.SubElement(node, "RELATOR", attrib = {'relative': relative, 'case': case})
    # Pronominalrelativsatz 'das, was' with 'was' in neutrum
    if kind == 'Pronominalrelativsatz' and relative == 'Neutrum':
      relator.text = 'was'
    else:
      relator.text = pronoun = Relativpronomina[case][relative]
    # set flags for agreement in case the relative pronoun turns out to be subject
    if case == 'Nominativ':
      node.set('person', '3')
      node.set('gender', relative)

# Default relators 'dass/ob' are handeled by 'Vorfeldposition'

# ===========
# Unbestimmmt
# ===========

# Questions and indefinites: depends on mood of the clause
# kind of question depends on addto node

# zero referent: 'wer/wen/wem/was', insert: REFERENT
# full referent: 'welch', insert DETERMINER/QUANTOR
# Possessed referent: 'wessen', insert DETERMINER/POSSESSIV
# Prepositional juncture: 'wo+Preposition', insert as JUNCTURE
# adjective: 'wie' (irgendwie is possible though rare), insert GRADPARTIKEL
# interrogative adverbs...

def Unbestimmt(phrase):

  # info from phrase
  case = phrase.get('case')
  gender = phrase.get('gender')
  # info from clause
  mood = upClause(phrase).get('mood')
  kind = upClause(phrase).get('kind')
  # make question word
  frage = 'Person' if gender in ['Maskulin', 'Feminin'] else 'Neutral'
  qword = Fragepronomina[frage][case]
  # make new node
  ET.strip_elements(phrase, '*')
  node = ET.SubElement(phrase, 'UNBESTIMMT')
  # insert
  if mood == 'Inhaltsfrage' and kind == 'Hauptsatz':
    node.tag = 'FRAGEPRONOMEN'
    node.text = qword
    Vorfeld(phrase)
  else:
    node.tag = 'INDEFINITPRONOMEN'
    node.text = 'irgend' + qword

  # Interrogative quantor
  if quantor == 'welch':
    clause = upClause(phrase)
    if clause.get('kind') == 'Hauptsatz':
      if clause.set('mood', 'Inhaltsfrage'):
        sub.tag = 'FRAGEWORT'
        Vorfeld(phrase)
      else:
        sub.tag = 'INDEFINIT'
        sub.text = 'irgend' + sub.text
    else:
      sub.tag = 'RELATOR'
      Relator(phrase)

  # interrogative possessor
  if person == 'wessen':
    pronoun = 'wessen'
    clause = upClause(phrase)
    if clause.get('kind') == 'Hauptsatz':
      clause.set('mood', 'Inhaltsfrage')
      sub.tag = 'FRAGEWORT'
      Vorfeld(phrase)
    else:
      sub.tag = 'RELATOR'
      Relator(phrase)

  # deal with interrogative Gradpartikel 'wie'
  addto = adjective.getparent()
  while addto.tag != 'SATZ':
    addto = addto.getparent()
  # interrogate gradpartikel
  if intensifier == 'wie':
    if addto.get('kind') == 'Hauptsatz':
      adjective.set('mood', 'Inhaltsfrage')
      node.tag = 'FRAGEWORT'
      Vorfeld(adjective)
    else:
      node.tag = 'RELATOR'
      Relator(adjective)

  # interrogative adverb
  elif adword in Frageadverbien:
    kind = clause.get('kind')
    mood = clause.get('mood')
    if kind == 'Hauptsatz' and mood == 'Inhaltsfrage':
      ET.SubElement(adverbial, "FRAGEWORT").text = adword
      Vorfeld(adverbial)
    else:
      ET.SubElement(adverbial, "RELATOR").text = adword
      Relator(adverbial)

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
      if kind in ['Relativsatz', 'Partizipsatz']:
        coordination.set('gender', addto.get('relative'))
        coordination.set('referent', addto.get('head'))
      if kind == 'Partizipsatz':
        setcontrol(addto, coordination)
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

def Satzende(satz, clean = True):
  articulator(satz)
  # optional cleanup of attributes for readability
  if clean:
   cleanup(satz)

def articulator(addto):
  # at the start of each new node, mark the previous node as done
  # the content can then be sent to the articulator
  # but not when signal comes from inside a coordination
  if addto.tag != 'KOORDINATION':
    clause = upClause(addto)
    # syntactically, verb agreement is also triggered by this command
    if clause.get('person') is not None and clause.get('agreement') is None:
      verbkongruenz(clause)
      clause.set('agreement', 'done')

# Vorfeld-positional 'es' has to be explicitly decided by speaker
# Subject-replacing 'es' only occurs through diathesis

def verbkongruenz(clause):
  # get verb
  finitum = clause.find('PRÄDIKAT')[-1]
  verb = finitum.get('verb')
  # get agreement attributes
  tense = clause.get('tense')
  person = clause.get('person')
  number = clause.get('number')
  # only make finite form
  if tense != 'Infinit':
    finite = verbfinite(verb, person, number, tense)
    # insert finite verb
    node = ET.SubElement(finitum, 'FINITUM', 
      attrib = {'verb': verb, 'tense': tense, 'person': person, 'number': number})
    node.text = finite
  # Verbzweit
  if clause.get('kind') == 'Hauptsatz':
    # leave trace
    ET.SubElement(finitum, 'FINITUM', attrib = {'move': 'Verbzweit'})
    # move to second position
    verbzweit = ET.Element('VERBZWEIT')
    verbzweit.append(node)
    clause.insert(1, verbzweit)
    # insert position-es when nothing in Vorfeld yet
    vorfeld = clause.find('VORFELD')
    if len(vorfeld) == 0:
      ET.SubElement(vorfeld, 'VORFELDERSATZ').text = 'es'
  # reorder verbcluster for Erstatzinfinitiv
  elif clause.get('cluster') == 'Ersatzinfinitiv':
    # leave trace
    ET.SubElement(finitum, 'FINITUM', attrib = {'move': 'Finiterst'})
    # move finite to front of verb cluster
    predicate = clause.find('PRÄDIKAT')
    predicate.insert(0, node)

# === REMOVE ===

def Vorfeldposition(clause):
  # search for 'Vorfeld' tag and copy upwards
  # also for 'mood' for interrogative
  for child in clause:
    for node in child.iter():
      position = node.get('position')
      mood = node.get('mood')
      if position is not None:
        child.set('position', position)
      if mood is not None:
        clause.set('mood', mood)
      # do not search in subclauses!
      if node.tag == 'SATZ':
        break
  # Relators for Weiterführungssatz: only complement-taking arguments can be used.
  # ignore all others markers of 'Relator'
  # remove all content in the complement
  if clause.get('kind') == 'Weiterführungssatz':
    verb = clause.find('PRÄDIKAT').get('verb')
    complement = Verben[verb]['Kontrolliert']
    argument = clause.find(f'*[@role="{complement}"]')
    argument.set('position', 'Relator')
    for node in argument.iter():
      # 'wo' + governed preposition
      if node[0].tag == 'JUNKTOR':
        juncture = node[0].text
        for rest in node.findall('*'):
          node.remove(rest)
        ET.SubElement(node, 'RELATOR').text =  'wo' + addR(juncture) + juncture
        break
      # 'was'
      if node[0].tag == 'PHRASE' or node[0] is None:
        for rest in node.findall('*'):
          node.remove(rest)
        ET.SubElement(node, 'RELATOR').text =  'was'
        break
  # move 'Vorfeld' to front in all clauses
  for child in clause:
    if child.get('position') == 'Vorfeld':
      vorfeld = ET.Element('VORFELD')
      vorfeld.append(child)
      clause.insert(0, vorfeld)
    # also Relator move to front
    elif child.get('position') is not None:
      clause.insert(0, child)
  # Default Vorfeld when nothing tagged as Vorfeld
  if clause[0].tag == 'VERBZWEIT':
    # Check for dummy subject as inserted by Kongruenz
    for child in clause:
      if child.get('subject') == 'dummy':
        vorfeld = ET.Element('VORFELD')
        vorfeld.append(child)
        clause.insert(0, vorfeld)
  # if still nothing in Vorfeld, then add positional dummy
  if clause[0].tag == 'VERBZWEIT':
    es = ET.Element('VORFELDFÜLLER')
    es.text = 'es'
    clause.insert(0, es)
  # insert dummy relator 'dass' when none present
  if clause.get('kind') in ['Komplementsatz', 'Pronominalrelativsatz']:
    if clause[0].get('position') is None:
      relator = ET.Element('RELATOR')
      if clause.get('mood') == 'Inhaltsfrage':
        relator.text = 'ob'
      else:
        relator.text = 'dass'
      clause.insert(0, relator)
  # Relators in complementclauses have to be checked for applicability
  #if clause.get('kind') == 'Komplementsatz':
    # TEST: role == complement for Komplementsatz
    #relator = clause.find('*[@position="Relator"]')
    #role = relator.get('role')
    #verb = clause.find('PRÄDIKAT').get('verb')
    #complement = Verben[verb]['Kontrolliert'] 

# ==============
# help functions
# ==============

def upClause(node):
  # go up to clause
  while node.tag != 'SATZ':
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

def upPhrase(node):
  # go up to phrase, but not when already at a phrase
  while node.tag != 'PHRASE':
    node = node.getparent()
  return node

def findcase(clause, value):
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

def verbfinite(verb, person, number, tense):
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

def checkArgument(node):
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

def makePartizipsatz(clause, verb):
  # participle for Partizipsatz
  if variant == 'Vorzeit':
    partizip = participle(verb)
  elif variant == 'Zustand':
    partizip = verb + 'd'
  elif variant == 'Nachzeit':
    partizip = 'zu ' + verb + 'd' 
  # declension if inside phrase
  if clause.getparent().tag == 'ATTRIBUT':
    case = clause.get('case')
    declension = clause.get('declension')
    gender = clause.get('relative')
    variant = clause.get('variant')
    partizip = partizip + Adjektivflexion[declension][case][gender]
  return partizip

def setcontrol(node, newclause):  
  # control of clause subject
  if newclause.get('kind') in ['Kontrollsatz','Präpositionskontrollsatz']:
    verb = node.find('PRÄDIKAT').get('verb')
    controller = Verben[verb]['Kontrolle']
    controlnode = node.find(f'ARGUMENT[@role="{controller}"]//PHRASE')
    person = controlnode.get('person')
    gender = controlnode.get('gender')
    # set attributes kontrollsatz
    newclause.set('controller', controller)
    newclause.set('person', person)
    newclause.set('gender', gender)
  # control of phrase referent
  elif newclause.get('kind') == 'Partizipsatz':
    case = node.get('case')
    relative = node.get('gender')
    declension = node.get('declension')
    controller = node.get('referent')
    if relative is None:
      relative = node.get('relative')
    if controller is None:
      controller = node.get('controller')
    # set attributes partizipsatz
    newclause.set('controller', controller)
    newclause.set('case', case)
    newclause.set('relative', relative)
    newclause.set('declension', declension)

# ==============
# Practicalities
# ==============

def reset():
  Teilnehmer.clear()

def add(name, gender = None):
  if gender is None:
    gender = Substantive[name]['Geschlecht']
  Teilnehmer[name] = gender

# ======
# Output
# ======

def findallclauses(satz):
  # clauses that are named with 'kind'
  clauses = satz.findall('.//SATZ[@kind]')
  # add main clause, when Hauptsatz
  if satz.tag == 'SATZ' and satz.get('kind') == 'Hauptsatz':
    clauses.append(satz)
  return clauses

def cleanup(satz):
  for clause in findallclauses(satz):
    keep = ['kind', 'controller', 'move', 'mood', 'head']
    new = {k:v for k,v in clause.attrib.items() if k in keep}
    att = clause.attrib 
    att.clear()
    att.update(new)
    # remove breaks used for inserting adverbials into clause
    if clause.find('break') is not None:
      clause.remove(clause.find('break'))
  for phrase in satz.findall('.//PHRASE'):
    keep = ['case', 'controller', 'move', 'mark']
    new = {k:v for k,v in phrase.attrib.items() if k in keep}
    att = phrase.attrib
    att.clear()
    att.update(new)
  for koordination in satz.findall('.//KOORDINATION'):
    keep = []
    new = {k:v for k,v in koordination.attrib.items() if k in keep}
    att = koordination.attrib
    att.clear()
    att.update(new)
 
def capfirst(s):
  return s[:1].upper() + s[1:]

def sentence(clause):
  sentence = ' '.join(clause.itertext())
  if clause.get('mood') in ['Inhaltsfrage', 'Entscheidungsfrage']:
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
  return(depth)

def reference(file):
  depth = level(file)
  stack = {}
  ref = ['None']
  for nr,elem in enumerate(depth[1:]):
    if elem > depth[nr]:
      ref.append(nr+1)
      stack.update({elem: nr+1})
    elif elem == depth[nr]:
      ref.append(ref[-1])
    elif elem < depth[nr]:
      ref.append(stack[elem])
  return ref

def specification(raw, lineNr, refs):
  # prepare line number
  id = 's' + str(lineNr+1)
  if lineNr == 0:
    ref = 'None'
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
    recursion = base + ', \'' + recursion[0] + '\''
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
  rules = '\n'.join(sentence)+ f'\nSatzende(s1, {clean})\n'
  return rules

def makeTree(rules):
  loc = {}
  exec(rules, globals(), loc)
  return loc['s1']

# ================
# Output from file
# ================

def Syntax(file, exe = True, clean = True, xml = False):
  # split into sentences separated by empty line
  sentences = re.split('\n\s*\n', file)
  parsed = [convert(s, clean) for s in sentences]
  if exe:
    # execute all
    trees = [makeTree(s) for s in parsed]
    # extract text
    text = [sentence(s) for s in trees]
    text = '\n'.join(text)
    if xml:
      trees = [ET.tostring(s, pretty_print = True, encoding = 'utf-8').decode('utf-8') for s in trees]
      trees = '====\n'.join(trees)
      text = text + '\n=====\n' + trees
  else:
    text = '\n\n'.join(parsed)
  return text
  
  