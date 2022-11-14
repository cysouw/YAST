from lxml import etree as ET
from copy import deepcopy
import re

# ==============
# Pure recursion
# ==============

# Choice of recursion determined by lexeme: 
# Verb (no capital, ending in -n), Nomen (capitalised), Other (only lists?)

def R(addto = None, lexeme = None, juncture = None):
  if lexeme is None:
    out = Phrase(addto, juncture)
  elif lexeme[0].isupper() or lexeme[0].isdigit() or lexeme in Genera:
    out = Phrase(addto, juncture)
    Referenz(out, lexeme)
  elif lexeme in Adverbien + Frageadverbien + Negationen + Adjektive:
    if juncture == 'Prädikativ':
      link = Link(addto, juncture)
      out = Addendum(link, lexeme)
    else:
      out = Addendum(addto, lexeme)
  elif lexeme in Konjunktionen:
    out = Koordination(addto, lexeme)
  else:
    out = Satz(addto, juncture)
    Prädikat(out, lexeme)
  return out

# adjective as noun: 
# R(addto, 'mfnp') + R(addto, adjective)
# adjective as predicate:
# R(addto, 'sein') + R(addto, adjective, 'Prädikativ')

# =======
# Satzart
# =======

def Satz(addto = None, juncture = None):
  if addto is None:
    return Hauptsatz()
  elif juncture in Subjunktionen:
    return Subjunktionsatz(addto, juncture)
  elif juncture in Satzpartizipien + Satzpräpositionen:
    return Präpositionssatz(addto, juncture)
  elif juncture in Relatorsubjunktionen:
    return Adverbialrelativsatz(addto, juncture)
  elif addto.find(f'*[@role="{juncture}"]') is not None:
    return Komplementsatz(addto, juncture)
  elif juncture in Genera or juncture in Genera.values():
    return Pronominalrelativsatz(addto, juncture)
  elif addto.tag == 'SATZ':
    return Weiterführungssatz(addto)
  elif addto.tag == 'PHRASE':
    return Relativsatz(addto)
  elif addto.tag == 'KOORDINATION':
    return eval(addto.get('kind'))(addto, juncture)

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

def Hauptsatz(addto = None, juncture = None):
  if addto is None:
    clause = ET.Element('SATZ', attrib = {'kind': 'Hauptsatz'})
  else:
    clause = ET.SubElement(addto, 'SATZ', attrib = {'kind': 'Hauptsatz'})
  return clause

def Subjunktionsatz(clause, juncture):
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Subjunktionsatz'})
  return newclause

def Präpositionssatz(clause, preposition):
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = preposition
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Präpositionssatz'})
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
  newclause = ET.SubElement(leaf, 'SATZ', attrib = {'kind': 'Komplementsatz'})
  return newclause

def Weiterführungssatz(clause, juncture = None):
  # reversed Komplementsatz: relator is always the complement-taking argument, set by Vorfeldposition
  # traditionally called 'weiterführender Relativsatz'
  node = ET.SubElement(clause, 'ADVERBIALE')
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Weiterführungssatz'})
  return newclause

def Adverbialrelativsatz(clause, juncture):
  # only for a few seemingly newly grammaticalised connectors
  # 'Anhand dessen, wo wir leben'
  if clause.tag == 'KOORDINATION':
    node = clause
  else:
    node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Adverbialrelativsatz'})
  return newclause

def Relativsatz(phrase, juncture = None):
  relative = phrase.get('gender')
  head = phrase.get('referent')
  if phrase.tag == 'KOORDINATION':
    node = phrase
  else:
    node = ET.SubElement(phrase, 'ATTRIBUT')
  clause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Relativsatz', 'head': head, 'relative': relative})
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
  Referenz(phrase, gender)
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

# turn finite sentences into controlled sentences

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
    # reset control
    PartizipPräsens(clause) # by default

# ===========
# Prädikation
# ===========

def Prädikat(clause, verb):
  if re.split(' ', verb)[0] in ['sein', 'werden', 'bleiben', 'haben']:
    Prädikativ(clause, verb)
  else:
    Verb(clause, verb)

# tense is Präsens by default and has to be explicitly changed to an infinite from
# insertion point 'break' is added to make Mittelfeld-insertion easier. Removed at the end
# Nominative '-de' role is assumed by default, except when listed differently in the lexicon

def Verb(clause, verb):
  # start with a default nominative role, except when listed in dictionary
  if not 'Nominative' in Verben.get(verb, {}).get('Rollen', {}).values():
    nominative = verb.capitalize() + 'de'
    ET.SubElement(clause, 'ARGUMENT', attrib = {'role': nominative, 'case': 'Nominativ'})
  # then go through all roles listed in the lexicon
  if Verben.get(verb, {}).get('Rollen', False):
    for role,case in Verben[verb]['Rollen'].items():
        ET.SubElement(clause, 'ARGUMENT', attrib = {'role': role, 'case': case})
  # insertion point for Mittelfeld, removed at end
  ET.SubElement(clause, 'break') 
  # make predicate node
  predicate = ET.Element('PRÄDIKAT', attrib = {'verb': verb})
  # lexical preverbs from lexicon are split
  if Verben.get(verb, {}).get('Präverb', False):
    ET.SubElement(predicate, 'PRÄVERBIALE').text = Verben[verb]['Präverb']
    #prädikat.set('verb', Verben[verb]['Stamm'])
    verb = Verben[verb]['Stamm']
  # lexicalised predicatives from lexicon are split
  elif Verben.get(verb, {}).get('Prädikativ', False):
    predicative = ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikativ'})
    phrase = ET.SubElement(predicative, 'PHRASE', attrib = {'case': 'Akkusativ'})
    Referenz(phrase, Verben[verb]['Prädikativ'])
    Generisch(phrase)
    #prädikat.set('verb', Verben[verb]['Stamm'])
    verb = Verben[verb]['Stamm']
  # add verb
  verb = ET.SubElement(predicate, 'VERB', attrib = {'verb': verb})
  clause.append(predicate)
  # default Präsens
  if clause.get('tense') == 'Infinit':
    verb.set('tense', 'Infinit')
  else:
    verb.set('tense', 'Präsens')
  # return for coordination
  return predicate

# combine adverbial, adjectival and nominal predication.
# preposition needs trick 'ich bin in den Garten' with the addition of PHRASE
# allow for 'haben' with accusative
# da-Relativsatz: possibly better kind of Nominalprädikat
# 'Es ist die Rede/Folge/Verständnis davon, dass  

def Prädikativ(clause, copula = 'sein'):
  # Subjekt argument
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  # insertion point for Mittelfeld, removed at end
  ET.SubElement(clause, 'break')
  # transitive auxiliaries, there are more to be done
  if copula == 'haben':
    case = 'Akkusativ'
  else:
    case = 'Nominativ'
  # add predicative
  predicate = ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikativ', 'case': case})
  # add preposition to input, split first
  complex = re.split(' ', copula)
  if len(complex) > 1:
    copula = complex[0]
    ET.SubElement(predicate, 'ORT', attrib = {'juncture': complex[1]})
  # add copula
  node = ET.SubElement(clause, 'PRÄDIKAT', attrib = {'verb': copula})
  verb = ET.SubElement(node, 'VERB', attrib = {'verb': copula})
  # default Präsens
  if clause.get('tense') == 'Infinit':
    verb.set('tense', 'Infinit')
  else:
    verb.set('tense', 'Präsens')
  # return for coordination
  return predicate

# dummy function to expose prädikativ node for connection of addendum

def Link(addto, link = 'Prädikativ'):
  return addto.find(link.upper())

# Alternatively, the verb 'haben (besitzen)' can be included as a main verb with these roles.
# note the accusative case
# 'Angst haben' is probably a lexicalised verb with some kind of nominal preverbial

def Besitz(clause, verb = 'haben'):
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Besitzer', 'case': 'Nominativ'})
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Besitz', 'case': 'Akkusativ'})
  ET.SubElement(clause, 'break') 
  predicate = ET.SubElement(clause, 'PRÄDIKAT', attrib = {'verb': verb})
  # default Präsens
  Präsens(clause)
  # return for coordination
  return predicate

# ================
# Ereignisstruktur
# ================

# The following is necessary for the Komplementsatz 
# default relator 'dass' vs. 'ob' as determined in 'Vorfeldposition'
# Some verbs have a real choice here
# https://grammis.ids-mannheim.de/systematische-grammatik/2091

def WahrheitUnbestimmt(clause):
  clause.set('truth', 'unbestimmt')

def PartizipPerfekt(clause):
  # only for Partizipsatz!
  clause.set('variant', 'Vergangenheit')

def PartizipPräsens(clause):
  # only for Partizipsatz!
  clause.set('variant', 'Präsens')

def PartizipFutur(clause):
  # only for Partizipsatz!
  clause.set('variant', 'Futur')

def Präsens(clause):
  verb = clause.find('PRÄDIKAT')[-1]
  verb.set('tense', 'Präsens')

def Präteritum(clause):
  verb = clause.find('PRÄDIKAT')[-1]
  verb.set('tense', 'Präteritum')

def Modalverb(clause, modal):
  addlightverb(clause, modal, 'Infinitiv', 'MODALVERB')
  
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

def Vorgangspassiv(clause, demoted = 'von'):
  # add light verb
  addlightverb(clause, 'werden', 'Partizip', 'VORGANGSPASSIV')
  # change arguments
  for node in clause.findall('ARGUMENT'):
    leaf = list(node.iter())[-1]
    if leaf.get('case') == 'Nominativ':
      if demoted is not None:
        ET.SubElement(node, 'VORGANGSPASSIV', attrib = {'juncture': demoted})
      else:
        clause.remove(leaf)
    if leaf.get('case') == "Akkusativ":
      ET.SubElement(node, 'VORGANGSPASSIV', attrib = {'case': 'Nominativ'})
      clause.insert(0, node)

def Rezipientenpassiv(clause):
  # add light verb
  addlightverb(clause, 'bekommen', 'Partizip', 'REZIPIENTENPASSIV')
  # change arguments
  for node in clause.findall('ARGUMENT'):
    leaf = list(node.iter())[-1]
    if leaf.get('case') == 'Nominativ':
      ET.SubElement(node, 'REZIPIENTENPASSIV', attrib = {'juncture': 'von'})
    if leaf.get('case') == "Dativ":
      ET.SubElement(node, 'REZIPIENTENPASSIV', attrib = {'case': 'Nominativ'})
      clause.insert(0, node)
  pass

def ReflexivErlebniskonversiv(clause):
  # get verb to find junture from lexicon
  verb = clause.find('PRÄDIKAT').get('verb')
  juncture = Verben[verb]['Konversiv']
  # change arguments
  for node in clause.findall('ARGUMENT'):
    leaf = list(node.iter())[-1]
    if leaf.get('case') == 'Nominativ':
      ET.SubElement(node, 'ERLEBNISKONVERSIV', attrib = {'juncture': juncture})
    if leaf.get('case') == "Akkusativ":
      ET.SubElement(node, 'ERLEBNISKONVERSIV', attrib = {'case': 'Nominativ'})
      reflexiv = ET.Element('ERLEBNISKONVERSIV')
      ET.SubElement(reflexiv, 'REFLEXIV', attrib = {'case': 'Akkusativ'})
      clause.insert(0, reflexiv)
      clause.insert(0, node)

# ======
# Phrase
# ======

def Phrase(addto, connection = None):
  parent = addto.getparent()
  # ======
  # argument phrase
  # ======
  node = addto.find(f'*[@role="{connection}"]')
  if node is not None:
    # Check for already filled predicative
    # which happens with lexicalised constructions like 'Angst haben'
    phrase = node.find('PHRASE')
    if connection == 'Prädikativ' and phrase is not None:
      return phrase
    # go to tip of branch to add stuff
    leaf = list(node.iter())[-1]
    # change arguments for Partizipsatz
    leaf = switchPartizipsatz(addto, leaf)
    # insert phrase, get juncture from governed preposition
    juncture = leaf.get('juncture')
    if juncture is None and connection not in Präpositionen:
      case = leaf.get('case')
    else:
      # lexically governed prepositions
      if connection in Präpositionen:
        juncture = node.get('role')
      # strange exceptions in case assignment for governed prepositions
      case = Präpositionen[juncture]
      if connection != 'Prädikativ' and juncture in ['an', 'in', 'auf', 'über']:
        case = 'Akkusativ'
      ET.SubElement(leaf, 'JUNKTOR').text = juncture
    phrase = ET.SubElement(leaf, 'PHRASE', attrib = {'case': case})
  # add role for unknown verbs: only useful for verbs that are not yet in the dictionary
  # for verfication, this should not be allowed.
  # use capitalisation as criterion
  elif connection is not None and connection[0].isupper():
    if connection == "Rezipient":
      case = 'Dativ'
    else:
      case = 'Akkusativ'
    # make node
    argument = ET.Element('ARGUMENT', attrib = {'role': connection, 'case': case})
    phrase = ET.SubElement(argument, 'PHRASE', attrib = {'case': case})
    # insert
    insert = addto.find('break')
    insert.addprevious(argument)
  # ======
  # adverbial phrase
  # ======
  elif addto.tag == 'SATZ' or parent.tag == 'SATZ':
    # prepare node
    node = ET.Element('ADVERBIALE')
    # prepositionphrase
    if connection is not None:
      ET.SubElement(node, 'JUNKTOR').text = connection
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionen[connection]})
    # No juncture then measurephrase in accusative, e.g. 'den ganzen Tag'
    else:
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Akkusativ'})
    # find insertion point for branch
    if addto.tag == 'KOORDINATION':
      addto.append(node)
    else:
      insert = addto.find('break')
      insert.addnext(node)
  # ======
  # attribute phrase
  # ======
  elif addto.tag == 'PHRASE' or parent.tag == 'PHRASE':
    # prepare node
    node = ET.Element('ATTRIBUT')
    # prepositionphrase
    if connection is not None:
      ET.SubElement(node, 'JUNKTOR').text = connection
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionen[connection]})
    # When there is already case assignment, that means there has been an empty phrase before this command
    # simply ignore the current command: there is no content added. This is user convenience, no content decision
    #elif addto.get('case') is not None:
    #  return addto
    # Genitive when no juncture
    else:
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Genitiv'})
    # find insertion point for branch
    addto.append(node)
  # ======
  # Coordination of roles
  # ======
  elif addto.tag == 'KOORDINATION':
    # simply add attribute to end of the phrase
    case = parent.get('case')
    phrase = ET.SubElement(addto, 'PHRASE', attrib = {'case': case})
    # set phrase to plural in case it is subject
    addto.set('person', '3')
    addto.set('gender', 'Plural')
  # ======
  # For relators: add info to all phrases
  relative = addto.get('relative')
  if relative is not None:
    phrase.set('relative', relative)
  kind = addto.get('kind')
  if kind is not None:
    phrase.set('kind', kind)
  # ======
  return phrase

# =======
# Addenda
# =======

# adjective and adverb addition are almost completely the same
# they are distinguished to allow for lexical checks
# and there are differences in attributive function
# there are differences in specification as well

def Addendum (addto, adword):
  if adword in Adverbien + Frageadverbien + Negationen:
    node = Adverb(addto, adword)
  elif adword in Adjektive:
    node = Adjektiv(addto, adword)
  return node

def Adverb(addto, adverb):
  # In coordination, get label from parent
  if addto.tag == 'KOORDINATION':
    tags = {'SATZ': 'ADVERBIALE', 'PHRASE': 'ATTRIBUT', 'PRÄDIKATIV': 'ADVERBIALE'}
    parent = addto.getparent()
    node = ET.SubElement(addto, tags[parent.tag])
  # Adverb Prädikat
  elif addto.tag == 'PRÄDIKATIV':
    node = ET.SubElement(addto, "ADVERBIALE")
  # Adverb Attribut, this is rare, e.g. 'das Treffen gestern'
  elif addto.tag == 'PHRASE':
    node = ET.SubElement(addto, 'ATTRIBUT')
  # Adverb Adverbiale
  elif addto.tag == 'SATZ':
    node = ET.Element("ADVERBIALE")
    # insert after arguments
    insertafter = addto.find('break')
    place = list(addto).index(insertafter) + 1
    addto.insert(place, node)
  # add adverb to prepared node
  sub = ET.SubElement(node, "ADVERB")
  sub.text = adverb
  # Fragewörter
  if adverb in Frageadverbien:
    if addto.get('kind') == 'Hauptsatz':
      addto.set('mood', 'Fragesatz')
      sub.tag = 'FRAGEWORT'
      # by default: maybe better explicit?
      Vorfeld(node)
    elif addto.tag == 'SATZ':
      sub.tag = 'RELATOR'
      # by default: maybe better explicit?
      Relator(node)
  # return for specification
  return node

def Adjektiv(addto, adjective):
  # In coordination, get label from parent
  if addto.tag == 'KOORDINATION':
    tags = {'SATZ': 'ADVERBIALE', 'PHRASE': 'ATTRIBUT', 'PRÄDIKATIV': 'ADVERBIALE'}
    parent = addto.getparent()
    node = ET.SubElement(addto, tags[parent.tag])
  # Adjective Prädikat
  elif addto.tag == 'PRÄDIKATIV':
    node = ET.SubElement(addto, "ADVERBIALE")
  # Adjective Attribut
  elif addto.tag == 'PHRASE':
    node = ET.Element('ATTRIBUT')
    addto.insert(1, node)
  # Adjective Adverbiale
  elif addto.tag == 'SATZ':
    node = ET.Element("ADVERBIALE")
    # insert after arguments
    insertafter = addto.find('break')
    place = list(addto).index(insertafter) + 1
    addto.insert(place, node)
  # Adjective agreement
  parent = addto.getparent()
  search = None
  if addto.tag == 'PHRASE':
      search = addto
  elif parent is not None:
    if parent.tag == 'PHRASE':
      search = parent
  if search is not None:
    case = search.get('case')
    gender = search.get('gender')
    declension = search.get('declension')
    adjective = adjective + Adjektivflexion[declension][case][gender]
  # Add adjective to prepared node
  sub = ET.SubElement(node, "ADJEKTIV")
  sub.text = adjective
  # Adjective as head
  referent = addto.find('REFERENT')
  if addto.tag == 'PHRASE' and referent.text is None:
    referent.text = adjective.capitalize()
    addto.remove(node)
  # return for Gradpartikel
  return node

# =============
# Specifikation
# =============

def Gradpartikel(adjective, intensifier):
  # insert before adjective
  node = ET.Element('GRADPARTIKEL')
  node.text = intensifier
  adjective.insert(0, node)
  # deal with interrogative Gradpartikel 'wie'
  addto = adjective.getparent()
  while addto.tag != 'SATZ':
    addto = addto.getparent()
  if intensifier == 'wie':
    if addto.get('kind') == 'Hauptsatz':
      adjective.set('mood', 'Fragesatz')
      node.tag = 'FRAGEWORT'
      Vorfeld(adjective)
    else:
      node.tag = 'RELATOR'
      Relator(adjective)

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

def Adverbialpräposition(adverbial, preposition):
  # insert before adverbial
  node = ET.Element('ADVERBIALPRÄPOSITION')
  node.text = preposition
  adverbial.insert(0, node)

def Vorwärts(adverbial):
  # move adverbial in front of preceding constituent
  clause = adverbial.getparent()
  while clause.tag != 'SATZ':
    clause = clause.getparent()
    adverbial = adverbial.getparent()
  # move one constituent to the front
  position = list(clause).index(adverbial) - 2
  clause.insert(position, adverbial)
  #infront = adverbial.getprevious()
  #infront.addprevious(adverbial)

# attributes can be detached to become secondary predicates

def Frei(attribute):
  # adjectives go to before predicate
  # NOTE: they do not have agreement there!
  if attribute.tag == 'ATTRIBUT':
    pass
  elif attribute.get('kind') == 'Partizipsatz':
    pass
  # relative clauses move to after predicate of containing clause
  elif attribute.get('kind') == 'Relativsatz':
    attribute.set('move', 'hinterVerb')
    clause = attribute.getparent()
    while clause.tag != 'SATZ':
      clause = clause.getparent()
    predicate = clause.find('PRÄDIKAT')
    predicate.addnext(attribute.getparent())

# ========
# Referenz
# ========

# TODO indefinita 'irgendwer', 'jemand' etc.

def Referenz(phrase, referent = None):
  # Fragepronomen
  if referent == 'wer':
    return Fragepronomen(phrase)
  # insert personal pronoun
  elif referent[0].isnumeric():
    return Pronomen(phrase, referent)
  # insert demonstrative/relative
  elif referent in Genera or referent in Genera.values():
    return Nomen(phrase, referent)
  # insert noun
  elif referent not in Teilnehmer:
    return Nomen(phrase, referent)
  # make reference to another referent
  else:
    return Anapher(phrase, referent)

def Anapher(phrase, referent):
  # including reflexive pronoun
  # agreement set by Kongruenz at Satzende
  case = phrase.get('case')
  node = ET.SubElement(phrase, 'ANAPHER', attrib = {'case': case, 'referent': referent})
  # return for coordination
  return node

def Fragepronomen(phrase):
  case = phrase.get('case')
  pronoun = Fragepronomina[case]
  node = ET.SubElement(phrase, 'FRAGEWORT')
  node.text = pronoun
  if phrase.get('kind') == 'Hauptsatz':
    phrase.set('mood', 'Fragesatz')
    Vorfeld(phrase)
  else:
    node.tag = 'RELATOR'
    Relator(phrase)
  # return for coordination
  return node

def Pronomen(phrase, pronoun):
  # get attributes from phrase
  case = phrase.get('case')
  # personal pronoun
  if pronoun[-1:] == 'p':
    number = 'Plural'
  elif pronoun[-1:] == 's':
    number = 'Singular'
  person = pronoun[:-1]
  # make new node
  node = ET.Element('PRONOMEN')
  node.text = Personalpronomina[number][person][case]
  # set flags for agreement
  if person == '3m':
    gender = 'Maskulin'
  elif person == '3f':
    gender = 'Feminin'
  elif person == '3n':
    gender = 'Neutrum'
  elif person == '3':
    gender = 'Plural'
  else:
    gender = number
  person = person[:1]
  node.set('person', person)
  node.set('gender', gender)
  # combine coordinants into person hierarchy
  if phrase.get('person') is None:
    phrase.set('person', person)
  else:
    p1 = phrase.get('person')
    phrase.set('person', min(p1,person))
  if phrase.get('gender') is None:
    phrase.set('gender', gender)
  else:
    phrase.set('gender', 'Plural')
  # if direct reference into koordination, add extra phrase
  if phrase.tag == 'KOORDINATION':
    phrase = ET.SubElement(phrase, 'PHRASE', attrib = {'case': case})
  # insert pronoun node
  phrase.append(node)
  # return for coordination
  return node

def Nomen(phrase, referent):
  # get attributes
  case = phrase.get('case')
  # set base form of referent as attribute for Plural
  phrase.set('referent', referent)
  # with empty head, gender is neede, adjective can be used as head
  # with demonstratives and relative clause this can be used for 'freier relativsatz'
  if referent in Genera:
    gender = Genera[referent]
    referent = None
  elif referent in Genera.values():
    gender = referent
    referent = None
  # check for word class and find gender
  elif referent in Substantive:
    gender = Substantive[referent]['Geschlecht']
    declination = Substantive[referent].get('Deklination', 'stark')
  # else assume that it is a verb, used as nomen, e.g. 'das Laufen'
  else:
    gender = 'Neutrum'
    declination = 'stark'
    referent = referent.capitalize()
  # case suffix, status of 'e' needs precision
  if referent is not None and gender != 'Feminin':
    if declination == 'schwach' and case != 'Nominativ':
      referent = referent + 'en'
    elif declination == 'stark' and case == 'Genitiv':
      referent = referent + 'es'
  # with coordination: possibly insert an extra node
  # set flags at koordination for verb agreement
  if phrase.tag == 'KOORDINATION':
    phrase.set('gender', 'Plural')
    phrase.set('person', '3')
    phrase = ET.SubElement(phrase, 'PHRASE', attrib = {'case': case})
  # insert nodes
  ET.SubElement(phrase, 'DETERMINATIV')   
  node = ET.SubElement(phrase, "REFERENT")
  node.text = referent
  # set flags for agreement with adjective
  phrase.set('gender', gender)
  phrase.set('person', '3')
  # return for coordination
  Definit(phrase)
  return node

# =============
# Determination
# =============

def Plural(phrase):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # current implementation assumes this comes before Quantor/Possessiv
  case = phrase.get('case')
  noun = phrase.get('referent')
  # change form of noun
  if noun is not None:
    if noun in Genera or noun in Genera.values():
      phrase.set('referent', 'Plural')
    else:
      noun = Substantive[noun]['Plural']
      if case == 'Dativ' and noun[:-1] != 'n':
        noun = noun + 'n'
      # insert noun
      phrase.find('REFERENT').text = noun
  # change form of determiner
  article = phrase.find('DETERMINATIV/ARTIKEL')
  article.text = Definitartikel[case]['Plural']  
  # set gender/number for agreement
  phrase.set('gender', 'Plural')

def Definit(phrase):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # for convenience, this is by default added with Nomen
  determiner = phrase.find('DETERMINATIV')
  # remove anything present
  ET.strip_elements(determiner, '*')
  # insert article
  article = Definitartikel[case][gender] 
  ET.SubElement(determiner, 'ARTIKEL').text = article
  # set declension for agreement
  phrase.set('declension', 'schwach')

def Indefinit(phrase):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # for convenience, this is by default added with Nomen
  determiner = phrase.find('DETERMINATIV')
  # remove anything present
  ET.strip_elements(determiner, '*')
  # insert article
  inflection = Quantoren['ein']['Flexion']
  article = 'ein' + Quantorflexion[inflection][case][gender]
  ET.SubElement(determiner, 'ARTIKEL').text = article
  # set declension for agreement
  phrase.set('declension', 'gemischt')

def Generisch(phrase):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # absence of determiner means generic reference, which has no article in German
  determiner = phrase.find('DETERMINATIV')
  # remove anything present
  ET.strip_elements(determiner, '*')
  # set declension for agreement
  phrase.set('declension', 'stark')

def Demonstrativ(phrase):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # replace determiner by demonstrative/relative
  demonstrative = Relativpronomina[case][gender]
  # find insertion point
  determiner = phrase.find('DETERMINATIV')
  ET.strip_elements(determiner, '*')
  ET.SubElement(determiner, 'DEMONSTRATIVE').text = demonstrative
  phrase.set('declension', 'schwach')

def Quantor(phrase, quantor):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # replace determiner by quantor
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # prepare the quantor as listed in the lexicon
  if quantor in Quantoren:
    inflection = Quantoren[quantor]['Flexion']
    declension = Quantoren[quantor]['Deklination']
    article = quantor + Quantorflexion[inflection][case][gender]
  # find insertion point
  determiner = phrase.find('DETERMINATIV')
  ET.strip_elements(determiner, '*')
  sub = ET.SubElement(determiner, 'QUANTOR')
  sub.text = article
  # Interrogative quantor
  if quantor == 'welch':
    if phrase.get('kind') == 'Hauptsatz':
      phrase.set('mood', 'Fragesatz')
      sub.tag = 'FRAGEWORT'
      Vorfeld(phrase)
    else:
      sub.tag = 'RELATOR'
      Relator(phrase)
  # set declension for agreement
  phrase.set('declension', declension)

def Possessiv(phrase, person): 
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # get attributes from phrase
  case = phrase.get('case')
  gender = phrase.get('gender') 
  # prepare possessive pronoun
  if person[:1].isnumeric(): 
    if person[-1:] == 'p':
      number = 'Plural'
    elif person[-1:] == 's':
      number = 'Singular'
    person = person[:-1]
    pronoun = Personalpronomina[number][person]['Attributiv'] + Quantorflexion['ein'][case][gender]
  # find insertion point
  determiner = phrase.find('DETERMINATIV')
  ET.strip_elements(determiner, '*')
  sub = ET.SubElement(determiner, 'POSSESSSIV')
  # interrogative possessor
  if person == 'wessen':
    pronoun = 'wessen'
    if phrase.get('kind') == 'Hauptsatz':
      phrase.set('mood', 'Fragesatz')
      sub.tag = 'FRAGEWORT'
      Vorfeld(phrase)
    else:
      sub.tag = 'RELATOR'
      Relator(phrase)
  # set pronoun
  sub.text = pronoun
  # set declension for agreement
  phrase.set('declension', 'gemischt')

def Numerale(phrase, numeral):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # 'ein' is the only numeral with declension
  if numeral == 'ein':
    # get attributes from phrase
    case = phrase.get('case')
    gender = phrase.get('gender')
    declension = phrase.get('declension')
    # add inflection
    numeral = numeral + Adjektivflexion[declension][case][gender]
  # insert numeral
  determiner = phrase.find('DETERMINATIV')
  ET.SubElement(determiner, 'NUMERALE').text = numeral

def Fokuspartikel(phrase, particle):
  # for usage flexibility
  if phrase.tag != 'PHRASE':
    phrase = phrase.getparent()
  # add fokuspartikel
  fokus = ET.Element("FOKUSPARTIKEL")
  fokus.text = particle
  phrase.insert(0, fokus)

# ============
# Markierungen
# ============

def Markierung(phrase, name):
  phrase.set('mark', name)
  # add name to local dictionary
  Teilnehmer[name] = {'Person': phrase.get('person')}
  Teilnehmer[name]['Geschlecht'] = phrase.get('gender')

def Vorfeld(node):
  node.set('position', 'Vorfeld')

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

# ============
# Koordination
# ============

def Koordination(addto, conjunction = 'und'):
  parent = addto.getparent()
  if parent is not None:
    grandparent = parent.getparent()
  # prepare koordination node
  node = ET.Element('KOORDINATION')
  ET.SubElement(node, 'KONJUNKTION').text = conjunction
  # do nothing special for main clauses
  if addto.tag == 'SATZ' and addto.get('kind') == 'Hauptsatz':
    node.set('kind', addto.get('kind'))
  else:
    # Subordinate sentences
    if addto.tag == 'SATZ':
      insertion = parent
      # pass on kind of subordinate sentence
      kind = addto.get('kind')
      node.set('kind', kind)
      # for relative clause reference
      if kind in ['Relativsatz', 'Partizipsatz']:
        node.set('gender', addto.get('relative'))
        node.set('referent', addto.get('head'))
      if kind == 'Partizipsatz':
        setcontrol(addto, node)
    # simple insertion with attribut/adverbiale
    elif addto.tag in ['ATTRIBUT', 'ADVERBIALE']:
      insertion = parent
    # insertion with attribute/adverbiale phrase at parent (phrase) grandparent (reference)
    elif parent.tag in ['ATTRIBUT', 'ADVERBIALE'] or grandparent.tag in ['ATTRIBUT', 'ADVERBIALE']:
      insertion = grandparent
      addto = parent
      # pass on case
      if addto.get('case') is not None:
        node.set('case', addto.get('case'))
    # for arguments, two encoding options that give the same result
    elif addto.tag == 'PHRASE':
      insertion = parent
      node.set('case', addto.get('case'))
    elif addto.tag in ['REFERENT', 'PRONOMEN']:
      insertion = grandparent
      addto = parent
      # pass on features
      node.set('case', addto.get('case'))
      node.set('person', addto.get('person'))
      node.set('gender', addto.get('gender'))
    # insert new coordination node
    position = list(insertion).index(addto)
    insertion.insert(position, node)
  # attach original coordinant
  node.append(addto)
  return node

# ========
# Satzende
# ========

def Satzende(satz, clean = True):
  # set agreement of anaphora
  Anaphora(satz)
  # go through all clauses 
  for clause in findallclauses(satz):
    Kongruenz(clause)
    Verbzweitposition(clause)
    Vorfeldposition(clause)
    Reflexive(clause)
  # re-ordering inside koordination
  Konjunktionposition(satz)
  # separation of da-preposition with complement clause
  Komplementsatzposition(satz)
  # optional cleanup of attributes for readability
  if clean:
   cleanup(satz)

def Kongruenz(clause):
  # find verb
  finitum = clause.find('PRÄDIKAT')[-1]
  verb = finitum.get('verb')
  tense = finitum.get('tense')
  finitum.attrib.pop('tense')
  # find subject
  subject = findcase(clause, 'Nominativ')
  # insert dummy subject when there is no subject
  if subject is None or subject.get('person') is None:
    person = '3'
    gender = 'Singular'
    if clause.get('kind') not in ['Kontrollsatz', 'Präpositionskontrollsatz', 'Partizipsatz']:
      dummy = ET.Element('SUBJEKTERSATZ', attrib = {'subject': 'dummy'})
      dummy.text = 'es'
      clause.insert(0, dummy)
  # get person/number from subject
  else:
    person = subject.get('person')
    gender = subject.get('gender')
  # Non-finite: zu-Infinitiv Kontrollsatz
  if clause.get('kind') == 'Partizipsatz':
    if subject is not None:
      subject.clear()
  # Control replaces subject person/number
  if clause.get('kind') in ['Kontrollsatz', 'Präpositionskontrollsatz']:
    person = clause.get('person')
    gender = clause.get('gender')
    if subject is not None:
      subject.clear()
      subject.set('person', person)
      subject.set('gender', gender)
      subject.set('controller', clause.get('controller'))
    # insert zu-Infinitiv
    ET.SubElement(finitum, 'INFINITUM', 
      attrib = {'verb': verb, 'non-finite': 'zu-Infinitiv'}).text = 'zu ' + verb
  # Non-finite: Partizipsatz
  elif clause.get('kind') == 'Partizipsatz':
    partizip = makePartizipsatz(clause, verb)
    kind = clause.get('variant') + 'partizip'
    ET.SubElement(finitum, 'INFINITUM', 
      attrib = {'verb': verb, 'non-finite': kind}).text = partizip
  # Finite: only agreement when tense is finite
  elif tense != 'Infinit':
    number = gender
    if number != 'Plural':
      number = 'Singular'
    if verb not in Verben or tense not in Verben[verb]:
      finite = verbfinite(verb, person, number, tense)
    else:
      finite = Verben[verb][tense][number][person]
    # insert finite verb
    node = ET.SubElement(finitum, 'FINITUM', 
      attrib = {'verb': verb, 'tense': tense, 'person': person, 'number': number})
    node.text = finite
  # reorder for Erstatzinfinitiv
  if clause.get('cluster') == 'Ersatzinfinitiv':
    # leave trace
    ET.SubElement(finitum, 'FINITUM', attrib = {'move': 'Finiterst'})
    # move finite to front
    predicate = clause.find('PRÄDIKAT')
    predicate.insert(0, node)
  # find reflexives and set person/number agreement
  # only reflexives from diathesis!
  for child in clause:
    for node in child.iter():
      if node.tag == 'REFLEXIV': 
        setreflexive(node, person, gender)
      if node.tag == "SATZ":
        break

def Reflexive(clause):
  # search for marks in the clause 
  marks = []
  # move the search one clause up when in Kontrollsatz
  start = clause
  if start.get('kind') in ['Kontrollsatz', 'Präpositionskontrollsatz']:
    start = start.getparent()
    while start.tag != 'SATZ':
      start = start.getparent()
  for child in start:
    for node in child.iter():
      mark = node.get('mark')
      if mark is not None:
        marks.append(mark)
        node.set('test', 'test')
      if node.tag == "SATZ" and node != clause:
        break
  # search for anaphors to be replaces by reflexives
  for child in clause:
    for node in child.iter():
      referent = node.get('referent')
      if node.tag == 'ANAPHER' and referent in marks:
        person = Teilnehmer[referent]['Person']
        gender = Teilnehmer[referent]['Geschlecht']
        node.tag = "REFLEXIV"
        setreflexive(node, person, gender)
      if node.tag == "SATZ":
        break

def Anaphora(satz):
  marks = []
  # find all marks in the sentence
  for node in satz.iter():
    mark = node.get('mark')
    if mark is not None:
      marks.append(mark)
  # set all anaphora
  for node in satz.iter():
    if node.tag == 'ANAPHER':
      case = node.get('case')
      referent = node.get('referent')
      person = Teilnehmer[referent]['Person']
      gender = Teilnehmer[referent]['Geschlecht']
      # set info for agreement
      node.getparent().set('person', person)
      node.getparent().set('gender', gender)
      # prepare pronoun
      if gender == 'Plural':
        number = 'Plural'
      else:
        number = 'Singular'
      if person == '3' and number == 'Singular':
        person = person + gender[0].lower()
      node.text = Personalpronomina[number][person][case]

def Verbzweitposition(clause):
  # only in Hauptsatz
  if clause.get('kind') == 'Hauptsatz':
    finitum = clause.find('PRÄDIKAT')[-1].find('FINITUM')
    second = deepcopy(finitum)
    second.tag = 'VERBZWEIT'
    clause.insert(0, second)
    finitum.clear()
    finitum.set('move', 'Verbzweit')

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
      if clause.get('truth') == 'unbestimmt':
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

def Konjunktionposition(satz):
  # easy solution to allow for arbitrary number of coordinants
  for coordination in satz.findall('.//KOORDINATION'):
    coordination.insert(-1, coordination[0])
  # also for root node as coordination
  if satz.tag == 'KOORDINATION':
    satz.insert(-1, satz[0])

def Komplementsatzposition(satz):
  # separate complement clause from its preposition
  for clause in findallclauses(satz):
    for child in clause:
      if child.get('move') == 'da-Junktor' and child.get('position') is None:
          child.attrib.pop('move')
          # copy juncture
          daJunktor = deepcopy(child)
          drop = daJunktor.find('.//SATZ')
          if drop.getparent().tag == 'KOORDINATION':
            drop = drop.getparent()
          drop.clear()
          drop.tag = 'SATZ'
          drop.set('move', 'Satzende')
          # insert juncture in Mittelfeld
          insertion = clause.find('PRÄDIKAT')
          #insertion = clause.find('break')
          place = list(clause).index(insertion)
          clause.insert(place, daJunktor)
          # remove Junktor from clause
          drop = child.find('.//JUNKTOR')
          drop.getparent().remove(drop)

# ==============
# help functions
# ==============

def findallclauses(satz):
  # clauses that are named with 'kind'
  clauses = satz.findall('.//SATZ[@kind]')
  # add main clause, when Hauptsatz
  if satz.tag == 'SATZ' and satz.get('kind') == 'Hauptsatz':
    clauses.append(satz)
  return clauses

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
  # add nonfinite form, remove flag for tense
  ET.SubElement(node, nonfinite.upper()).text = form
  node.attrib.pop('tense')
  # insert new node for light verb
  new = ET.SubElement(node.getparent(), label, attrib = {'verb': auxiliary, 'tense': tense})
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
  # various rules for the right verb inflection
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
  return finite

def setreflexive(node, person, number):
  if number != 'Plural':
    number = 'Singular'
  node.set('person', person)
  node.set('number', number)
  if person == '3':
    node.text = 'sich'
  else:
    case = node.get('case')
    node.text = Personalpronomina[number][person][case]
  node.attrib.pop('case')

def switchPartizipsatz(clause, leaf):
  # Participants are switched in Partizipsatz
  # somewhat reminiscent of passive
  kind = clause.get('kind')
  variant = clause.get('variant')
  case = leaf.get('case')
  if kind == 'Partizipsatz' and variant in ['Vergangenheit', 'Futur']:
    if case == 'Akkusativ':
      leaf = ET.SubElement(leaf, 'PARTIZIPSATZ', attrib = {'case': 'Nominativ'})
    elif case == 'Nominativ':
      leaf = ET.SubElement(leaf, 'PARTIZIPSATZ', attrib = {'juncture': 'von'})
  return leaf

def makePartizipsatz(clause, verb):
  # participle with declension for Partizipsatz
  case = clause.get('case')
  declension = clause.get('declension')
  gender = clause.get('relative')
  variant = clause.get('variant')
  if variant == 'Vergangenheit':
    partizip = participle(verb)
  elif variant == 'Präsens':
    partizip = verb + 'd'
  elif variant == 'Futur':
    partizip = 'zu ' + verb + 'd' 
  return partizip + Adjektivflexion[declension][case][gender]

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

# ======
# Output
# ======

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

def showresult(clause):
  sentence = ' '.join(clause.itertext())
  if clause.get('mood') == 'Fragesatz':
    sentence = capfirst(sentence) + '?'
  else:
    sentence = capfirst(sentence) + '.'
  print('<?xml version="1.0"?>')
  print('<!--') 
  print(sentence)
  print('-->')
  ET.indent(clause)
  ET.dump(clause)

# ==========
# parse file
# ==========

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
  ID = 's' + str(lineNr+1)
  if lineNr == 0:
    REF = 'None'
  else:
    REF = 's' + str(refs[lineNr])
  raw = re.sub('\)', '', raw)
  spec = re.split(' \(', raw)
  # recursion part
  recursion = spec[0].lstrip()
  recursion = re.split(':', recursion)
  recursion = [x.strip() for x in recursion]
  base = ID + ' = R(' + REF
  if len(recursion) == 1:
    string = base + ', \'' + recursion[0] + '\')'
  elif len(recursion) == 2:
    if recursion[1] in ['', '-']:
      string = base + ', None, \'' + recursion[0] + '\')'
    else:
      string = base + ', \'' + recursion[1] + '\', \'' + recursion[0] + '\')'
  #string = re.sub('\'-\'', 'None', string)
  # specification part
  if len(spec) > 1:
    parts = re.split(' \+ ', spec[1])
    for nr,part in enumerate(parts):
      tmp = re.split(': ', part)
      base = tmp[0] + '(' + ID
      if len(tmp) == 1:
        parts[nr] = base + ')'
      else:
        parts[nr] = base + ', \'' + tmp[1] + '\')'
    parts = '\n' + '\n'.join(parts)
  else:
    parts = ''
  return string + parts

def Syntax(file, execute = True, clean = True):
  file = re.split('\n', file)
  file = list(filter(None, file))
  refs = reference(file)
  for nr,elem in enumerate(file):
    file[nr] = specification(elem, nr, refs) 
  generative = '\n'.join(file)
  generative = generative + f'\nSatzende(s1, {clean})\nshowresult(s1)'

  if execute:
    exec(generative)
  else:
    return generative

def readfile(path):
  with open(path) as g:
    file = g.read()
    g.close()
  return file

# =======
# Lexicon
# =======

# default Perfect-Auxiliary is 'haben'
# default Nominative role is 'verb+de'

Verben = {
  'glauben':{
    'Rollen':{
      'Geglaubte': 'Akkusativ'
    },
    'Kontrolle': 'Glaubende',
    'Kontrolliert': 'Geglaubte'
  },
  'bekommen':{
    'Partizip': 'bekommen'
  },
  'schenken':{
    'Rollen':{
      'Geschenkte': 'Akkusativ',
      'Rezipient': 'Dativ',
    },
  },
  'stellen':{
    'Rollen':{
      'Gestellte': 'Akkusativ',
      'in': 'Akkusativ'
    }
  },
  'darstellen':{
    'Präverb': 'dar',
    'Stamm': 'stellen',
    'Rollen':{
      'Dargestellte': 'Akkusativ'
    }
  },
  'vorliegen':{
    'Präverb': 'vor',
    'Stamm': 'liegen',
    'Rollen':{
      'Vorgelegte': 'Akkusativ'
    }
  },
  'Angst haben':{
    'Prädikativ': 'Angst',
    'Stamm': 'haben',
    'Rollen':{
      'vor': 'Dativ'
    }
  },
  'hoffen':{
    'Rollen':{
      'Gehoffte': 'Akkusativ',
      'auf': 'Akkusativ'
    },
    'Kontrolle': 'Hoffende',
    'Kontrolliert': 'auf'
  },
  'warten':{
    'Rollen':{
      'auf': 'Akkusativ'
    },
    'Kontrolle': 'Wartende',
    'Kontrolliert': 'Bewartete'
  },
  'versprechen':{
    'Partizip': 'versprochen',
    'Rollen':{
      'Rezipient': 'Dativ',
      'Versprochene': 'Akkusativ',
    },
    'Kontrolle': 'Versprechende',
    'Kontrolliert': 'Versprochene',
  },
  'weglaufen':{
    'Präverb': 'weg',
    'Stamm': 'laufen',
  },
  'kommen':{
    'Partizip': 'gekommmen',
    'Perfekt': 'sein',
  },
  'ärgern':{
    'Konversiv': 'über',
    'Rollen':{
      'Auslöser': 'Nominativ',
      'Ärgernde': 'Akkusativ',
    },
    'Kontrolle': 'Ärgernde',
    'Kontrolliert': 'Auslöser',
  },
  'freuen':{
    'Konversiv': 'über',
    'Rollen':{
      'Auslöser': 'Nominativ',
      'Freuende': 'Akkusativ',
    },
    'Kontrolle': 'Freuende',
    'Kontrolliert': 'Auslöser',
  },
  'erwarten':{
    'Rollen':{
      'Erwartete': 'Akkusativ'
    },
    'Kontrolle': 'Erwartende',
    'Kontrolliert': 'Erwartete',
  },
  'laufen':{
    'Partizip': 'gelaufen',
    'Präsens':{
      'Singular':{
        '1': 'laufe',
        '2': 'läufst',
        '3': 'läuft'
      },
      'Plural':{
        '1': 'laufen',
        '2': 'läuft',
        '3': 'laufen'
      }
    }
  },
  'schlafen':{
    'Partizip': 'geschlafen',
    'Präsens':{
      'Singular':{
        '1': 'schlafe',
        '2': 'schläfst',
        '3': 'schläft'
      },
      'Plural':{
        '1': 'schlafen',
        '2': 'schläft',
        '3': 'schlafen'
      }
    }
  },
  'sehen':{
    'Partizip': 'gesehen',
    'Rollen': {
      'Gesehene': 'Akkusativ'
    },
    'Kontrolle': 'Seher',
    'Präsens':{
      'Singular':{
        '1': 'sehe',
        '2': 'siehst',
        '3': 'sieht'
      },
      'Plural':{
        '1': 'sehen',
        '2': 'sieht',
        '3': 'sehen'
      }
    }
  },
  'sein':{
    'Partizip': 'gewesen',
    'Perfekt': 'sein',
    'Präsens':{
      'Singular':{
        '1': 'bin',
        '2': 'bist',
        '3': 'ist'
      },
      'Plural':{
        '1': 'sind',
        '2': 'seit',
        '3': 'sind'
      }
    }
  },
  'haben':{
    'Präsens':{
      'Singular':{
        '1': 'habe',
        '2': 'hast',
        '3': 'hat'
      },
      'Plural':{
        '1': 'haben',
        '2': 'habt',
        '3': 'haben'
      }
    }
  },
  'werden':{
    'Partizip': 'geworden',
    'Perfekt': 'sein',
    'Präsens':{
      'Singular':{
        '1': 'werde',
        '2': 'wirst',
        '3': 'wird'
      },
      'Plural':{
        '1': 'werden',
        '2': 'werdet',
        '3': 'werden'
      }
    }
  },
  'bleiben':{
    'Partizip': 'geblieben',
    'Perfekt': 'sein',
  },
  'müssen':{
    'Partizip': 'gemusst',
    'Präsens':{
      'Singular':{
        '1': 'muss',
        '2': 'musst',
        '3': 'muss'
      },
      'Plural':{
        '1': 'müssen',
        '2': 'müsst',
        '3': 'müssen'
      }
    }
  },
  'können':{
    'Partizip': 'gekonnt',
    'Präsens':{
      'Singular':{
        '1': 'kann',
        '2': 'kannst',
        '3': 'kann'
      },
      'Plural':{
        '1': 'können',
        '2': 'könnt',
        '3': 'können'
      }
    }
  },
  'dürfen':{
    'Partizip': 'gedurtf',
    'Präsens':{
      'Singular':{
        '1': 'darf',
        '2': 'darfst',
        '3': 'darf'
      },
      'Plural':{
        '1': 'dürfen',
        '2': 'darfst',
        '3': 'dürfen'
      }
    }
  }
}

Substantive = {
  'Mann':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Männer'
  }, 
  'Karl':{
    'Geschlecht': 'Maskulin'
  },
  'Frau':{
    'Geschlecht': 'Feminin',
    'Plural': 'Frauen'
  },  
  'Schrank':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Schränke'
  },  
  'Rat':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Räte'
  },
  'Beschluss':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Beschlüsse'
  },
  'Grundlage':{
    'Geschlecht': 'Feminin',
    'Plural': 'Grundlagen'
  },
  'Dokument':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Dokumente'
  },
  'Angst':{
    'Geschlecht': 'Feminin',
    'Plural': 'Ängste'
  },
  'Mutter':{
    'Geschlecht': 'Feminin',
    'Plural': 'Mütter',
  },
  'Vater':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Väter'
  },
  'Zuschauer':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Zuschauer',
  },
  'Buch':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Bücher',
  },
  'Kind':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Kinder',
  },
  'Plan':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Pläne',
  },
  'Frage':{
    'Geschlecht': 'Feminin',
    'Plural': 'Fragen',
  },
  'Haus':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Häuser'
  },
  'Fenster':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Fenster',
  },
  'Ursache':{
    'Geschlecht': 'Feminin',
    'Plural': 'Ursachen'
  },
  'Tanz':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Tänze'
  },
  'Mensch':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Menschen',
    'Deklination': 'schwach'
  },
}

Teilnehmer = dict()

# TODO: double conjuncturs: entweder/oder, sowohl/als-wie-auch, wenn/dann, weder/noch, nichtnur/sondernauch
Konjunktionen = ['und', 'aber', 'doch', 'sondern', 'denn']
# NOTE: 'wie/wo' here in the meaning of 'als'
# NOTE: combination 'als ob' and 'als wenn' are unclear. Maybe just a single subjunction?
Subjunktionen = ['als', 'bevor', 'bis', 'da', 'damit', 'ehe', 'falls ', 'indem', 'insofern', 'insoweit', 'nachdem', 'obgleich', 'obschon', 'obwohl', 'obzwar', 'seit', 'seitdem', 'sobald', 'sofern', 'solange', 'sooft', 'sosehr', 'soviel', 'soweit', 'sowie', 'trotzdem', 'während', 'weil', 'wenn', 'wenngleich', 'wie', 'wo']
# NOTE: there is an old-fashioned usage of 'bis dass', which is not possible now
Satzpräpositionen = ['ohne', 'außer', 'statt', 'anstatt', 'im Falle', 'für den Fall']
Satzpartizipien = ['vorausgesetzt', 'ausgenommen', 'gegeben', 'ungeachtet', 'unterstellt', 'angenommen', 'gesetzt']

# newly grammaticalised adverbial junktors with following relator-clause 'dass'
Relatorsubjunktionen = ['abgesehen davon', 'angesichts dessen', 'anhand dessen', 'aufgrund dessen', 'unbeschadet dessen', 'ungeachtet dessen']

# Begründung (um)
# Alternative (statt, anstatt, anstelle)
# Außnahme (ohne: A-aber-nicht-B, außer: nicht-A-aber-B)
Kontrollsatzpräpositionen = ['um', 'statt', 'anstatt', 'anstelle', 'ohne', 'außer', 'ausser']

Adverbien = ['abends', 'allerdings', 'anfangs', 'bald', 'bisher', 'blindlings', 'da', 'dort', 'draußen', 'drinnen', 'drüben', 'früh', 'gestern', 'gewiss', 'halbwegs', 'heute', 'hier', 'hinten', 'jetzt', 'keinesfalls', 'keineswegs', 'links', 'manchmal', 'meinerseits', 'mittags', 'morgen', 'morgens', 'nachmittags', 'nachts', 'natürlich', 'neulich', 'nun', 'oben', 'oft', 'rechts', 'selbst', 'sofort', 'stündlich', 'überall', 'übermorgen', 'unbedingt', 'vorgestern', 'vorn', ]
Frageadverbien = ['warum', 'weshalb', 'wieso', 'wofür', 'wo', 'wohin', 'woher', 'wann', 'wie']
Negationen = ['nicht', 'nie', 'niemals', 'nicht mehr']

# NOTE: it looks like adjectives can not be used productively!
# new ones are mainly added through derivation or complete new innovation
Adjektive = ['albern', 'alt', 'arg', 'arm', 'barsch', 'bieder', 'bitter', 'blank', 'blass', 'blau', 'bleich', 'blind', 'blöd', 'blond', 'bös', 'böse', 'braun', 'brav', 'breit', 'brüsk', 'bunt', 'derb', 'deutsch', 'dicht', 'dick', 'doof', 'dreist', 'dumm', 'dumpf', 'dunkel', 'dünn', 'dürr', 'düster', 'echt', 'edel', 'eigen', 'einzig', 'eitel', 'elend', 'eng', 'ernst', 'fad', 'falsch', 'faul', 'feig', 'feige', 'fein', 'feist', 'fern', 'fesch', 'fest', 'fett', 'feucht', 'fies', 'finster', 'firn', 'flach', 'flau', 'flink', 'flott', 'forsch', 'frech', 'frei', 'fremd', 'froh', 'fromm', 'früh', 'gar', 'geil', 'gelb', 'gemein', 'genau', 'gerade', 'gering', 'geschwind', 'gesund', 'glatt', 'gleich', 'grau', 'greis', 'grell', 'grob', 'groß', 'grün', 'gut', 'hager', 'harsch', 'hart', 'heikel', 'heil', 'heiser', 'heiß', 'heiter', 'hell', 'herb', 'hoh', 'hohl', 'hübsch', 'irr', 'jäh', 'jung', 'kahl', 'kalt', 'kaputt', 'karg', 'keck', 'kess', 'keusch', 'kirre', 'klamm', 'klar', 'klein', 'klug', 'knapp', 'krank', 'krass', 'kraus', 'krud', 'krumm', 'kühl', 'kühn', 'kurz', 'lahm', 'lang', 'langsam', 'lasch', 'lau', 'laut', 'lauter', 'lecker', 'leer', 'leicht', 'leise', 'licht', 'lieb', 'lila', 'locker', 'los', 'mager', 'matt', 'mies', 'mild', 'morsch', 'müde', 'munter', 'mürb', 'nackt', 'nah', 'nass', 'nett', 'neu', 'nieder', 'öd', 'offen', 'orange', 'platt', 'plump', 'prall', 'prüde', 'rank', 'rar', 'rasch', 'rau', 'rauch', 'recht', 'rege', 'reich', 'reif', 'rein', 'roh', 'rosa', 'rot', 'rüd', 'rund', 'sacht', 'sanft', 'satt', 'sauber', 'sauer', 'schal', 'scharf', 'scheu', 'schick', 'schief', 'schlaff', 'schlank', 'schlapp', 'schlau', 'schlecht', 'schlicht', 'schlimm', 'schmal', 'schmuck', 'schnell', 'schnöd', 'schön', 'schräg', 'schrill', 'schroff', 'schwach', 'schwarz', 'schwer', 'schwul', 'schwül', 'seicht', 'selten', 'sicher', 'spät', 'spitz', 'spröd', 'stark', 'starr', 'steif', 'steil', 'stier', 'still', 'stolz', 'straff', 'stramm', 'streng', 'stumm', 'stumpf', 'stur', 'süß', 'tapfer', 'taub', 'teuer', 'tief', 'toll', 'tot', 'träg', 'treu', 'trocken', 'trüb', 'unscharf', 'übel', 'vag', 'viel', 'voll', 'wach', 'wacker', 'wahr', 'warm', 'weh', 'weich', 'weise', 'weiß', 'weit', 'wild', 'wirr', 'wirsch', 'wund', 'wüst', 'zäh', 'zähe', 'zahm', 'zart']

Genera = {
  'm': 'Maskulin',
  'f': 'Feminin', 
  'n': 'Neutrum',
  'p': 'Plural'
}

Präpositionen = {
  'mit': 'Dativ',
  'nach': 'Dativ',
  'bei': 'Dativ',
  'seit': 'Dativ',
  'von': 'Dativ',
  'zu': 'Dativ',
  'außer': 'Dativ',
  'aus': 'Dativ',
  'für': 'Akkusativ',
  'durch': 'Akkusativ',
  'gegen': 'Akkusativ',
  'ohne': 'Akkusativ',
  'um': 'Akkusativ',
  # Wechselpräpositionen: dative default for stative location!
  # only accusative through diathesis???
  # governed roles are variable, but: auf/über/in/vor take accusative when governed
  # an is variable (denken an Dativ, Dativ alternation with accusative)
  'an': 'Dativ',
  'auf': 'Dativ',
  'hinter': 'Dativ',
  'neben': 'Dativ',
  'in': 'Dativ',
  'über': 'Dativ',
  'unter': 'Dativ',
  'vor': 'Dativ',
  'zwischen': 'Dativ',
}

Personalpronomina = {
  'Singular':{
    '1':{
      'Nominativ': 'ich',
      'Akkusativ': 'mich',
      'Dativ': 'mir',
      'Genitiv': 'meiner',
      'Attributiv': 'mein'
    },
    '2':{
      'Nominativ': 'du',
      'Akkusativ': 'dich',
      'Dativ': 'dir',
      'Genitiv': 'deiner',
      'Attributiv': 'dein'
    },
    '3m':{
      'Nominativ': 'er',
      'Akkusativ': 'ihn',
      'Dativ': 'ihm',
      'Genitiv': 'seiner',
      'Attributiv': 'sein'
    },
    '3f':{
      'Nominativ': 'sie',
      'Akkusativ': 'sie',
      'Dativ': 'ihr',
      'Genitiv': 'ihrer',
      'Attributiv': 'ihr'
    },
    '3n':{
      'Nominativ': 'es',
      'Akkusativ': 'es',
      'Dativ': 'ihm',
      'Genitiv': 'seiner',
      'Attributiv': 'sein'
    }
  },
  'Plural':{
    '1':{
      'Nominativ': 'wir',
      'Akkusativ': 'uns',
      'Dativ': 'uns',
      'Genitiv': 'unser',
      'Attributiv': 'unser'
    },
    '2':{
      'Nominativ': 'ihr',
      'Akkusativ': 'euch',
      'Dativ': 'euch',
      'Genitiv': 'euer',
      'Attributiv': 'euer'
    },
    '3':{
      'Nominativ': 'sie',
      'Akkusativ': 'sie',
      'Dativ': 'ihnen',
      'Genitiv': 'ihrer',
      'Attributiv': 'ihr'
    }
  }
}

Fragepronomina = {
  'Nominativ': 'wer',
  'Akkusativ': 'wen',
  'Dativ': 'wem',
  'Genitiv': 'wessen',
  'Attributiv': 'wessen'
}

Relativpronomina = {
  'Nominativ':{
    'Maskulin': 'der',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
    },
  'Akkusativ':{
    'Maskulin': 'den',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
  },
  'Dativ':{
    'Maskulin': 'dem',
    'Neutrum': 'dem',
    'Feminin': 'der',
    'Plural': 'denen'
  },
  'Genitiv':{
    'Maskulin': 'dessen',
    'Neutrum': 'dessen',
    'Feminin': 'deren',
    'Plural': 'deren'
  }
}

Definitartikel = {
  'Nominativ':{
    'Maskulin': 'der',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
    },
  'Akkusativ':{
    'Maskulin': 'den',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
  },
  'Dativ':{
    'Maskulin': 'dem',
    'Neutrum': 'dem',
    'Feminin': 'der',
    'Plural': 'den'
  },
  'Genitiv':{
    'Maskulin': 'des',
    'Neutrum': 'des',
    'Feminin': 'der',
    'Plural': 'der'
  }
}

Quantoren = {
  'dies':{
    'Flexion': 'dies',
    'Deklination': 'schwach',
  },
  'jen':{
    'Flexion': 'dies',
    'Deklination': 'schwach',
  },
  'all':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'jed':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'beid':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'solch':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'manch':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'welch':{
    'Flexion': 'all',
    'Deklination': 'schwach'
  },
  'ein':{
    'Flexion': 'ein',
    'Deklination': 'gemischt',
  },
  'kein':{
    'Flexion': 'ein',
    'Deklination': 'gemischt',
  },
}

# ==========
# Inflection
# ==========

Verbflexion = {
  'Präsens':{
    'Singular':{
       '1': 'e',
       '2': 'st',
       '3': 't',
     },
     'Plural':{
       '1': 'en',
       '2': 't',
       '3': 'en',
    }
  },
  'Präteritum':{
    'Singular':{
       '1': 'te',
       '2': 'test',
       '3': 'te',
     },
     'Plural':{
       '1': 'ten',
       '2': 'tet',
       '3': 'ten',
    }
  },
}

Adjektivflexion = {
  'schwach':{
    'Nominativ':{
      'Maskulin': 'e',
      'Neutrum': 'e',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'e',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Dativ':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    }
  },
  'gemischt':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Dativ':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    }
  },
  'stark':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'er',
      'Plural': 'er'
    }
  }
}

Quantorflexion = {
  'ein':{
    'Nominativ':{
      'Maskulin': '',
      'Neutrum': '',
      'Feminin': 'e',
      'Plural': 'e'
      },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': '',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'es',
      'Neutrum': 'es',
      'Feminin': 'er',
      'Plural': 'er'
    }
  },
  'dies':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
      },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'es',
      'Neutrum': 'es',
      'Feminin': 'er',
      'Plural': 'er'
    }
  },
  'all':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
      },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'er',
      'Plural': 'er'
    }
  },
}
