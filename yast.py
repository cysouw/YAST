from lxml import etree as ET
from copy import deepcopy

# ==============
# Pure recursion
# ==============

# Choice of recursion determined by lexeme: Verb (no capital, ending in -n), Nomen (capitalised), Other (only lists?)

def R(addto = None, lexeme = None, juncture = None):
  if lexeme is None:
    out = Phrase(addto, juncture)
  elif lexeme[0].isupper() or lexeme[0].isdigit():
    out = Phrase(addto, juncture)
    Referenz(out, lexeme)
  elif lexeme in Adverbien + Frageadverbien + Negationen + Adjektive:
    out = Addendum(addto, lexeme)
  else:
    out = Satz(addto, juncture)
    Prädikat(out, lexeme)
  return out

# adjective as noun: 
# R(addto, 'mfnp') + R(addto, adjective)
# adjective as predicate:
# R(addto, 'sein') + R(addto, adjective)

# distinction 'er ist ein Vater' vs 'er hat einen Vater'

# =======
# Satzart
# =======

def Satz(addto = None, juncture = None):
  if addto is None:
    return Vollsatz(addto, juncture)
  elif juncture in Konjunktionen + Subjunktionen + Satzpartizipien + Satzpräpositionen:
    return Vollsatz(addto, juncture)
  elif addto.tag == 'KOORDINATION':
    return Vollsatz(addto, juncture)
  elif juncture in Relatorsubjunktionen:
    return Relatorsatz(addto, juncture)
  else:
    return Relatorsatz(addto, juncture) 

def Vollsatz(addto = None, juncture = None):
  # start with a new main sentence
  if addto is None:
    sentence = ET.Element('SATZ', attrib = {'kind': 'Hauptsatz'})
  # coordination of sentences
  elif addto.tag == 'KOORDINATION':
    # coordination of main sentences
    if juncture is None:
      sentence = ET.SubElement(addto, 'SATZ', attrib = {'kind': 'Hauptsatz'})
      parent = addto.getparent()
      if parent.get('kind') == 'Hauptsatz':
        parent.attrib.pop('kind')
  # Präpositionssatz
  elif juncture in Satzpräpositionen + Satzpartizipien:
    sentence = Präpositionssatz(addto, juncture)
  # Subjunktionsatz
  elif juncture in Subjunktionen:
    sentence = Subjunktionsatz(addto, juncture)
  return sentence

def Relatorsatz(addto, connection = None):
  if addto.tag == 'SATZ':
    # argument
    if addto.find(f'*[@role="{connection}"]') is not None:
      clause = Komplementsatz(addto, connection)
    # adverbial
    elif connection in Relatorsubjunktionen:
      clause = Adverbialrelativsatz(addto, connection)
    else:
      clause = Weiterführungssatz(addto)
  elif addto.tag == 'PHRASE':
    clause = Relativsatz(addto)
  return clause

def Kontrollsatz(addto, connection = None):
  if addto.tag == 'SATZ':
    # argument
    if addto.find(f'*[@role="{connection}"]') is not None:
      clause = Komplementkontrollsatz(addto, connection)
    # adverbial
    elif connection in Kontrollsatzpräpositionen:
      clause = Präpositionskontrollsatz(addto, connection)
  elif addto.tag == 'PHRASE':
    clause = Partizipsatz(addto)
  return clause

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

def Subjunktionsatz(addto, juncture):
  node = ET.SubElement(addto, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  sentence = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Subjunktionsatz'})
  return sentence

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

def Weiterführungssatz(clause):
  # reversed Komplementsatz: relator is always the complement-taking argument, set by Vorfeldposition
  # traditionally called 'weiterführender Relativsatz'
  node = ET.SubElement(clause, 'ADVERBIALE')
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Weiterführungssatz'})
  return newclause

def Adverbialrelativsatz(clause, juncture):
  # only for a few seemingly newly grammaticalised connectors
  # 'Anhand dessen, wo wir leben'
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Adverbialrelativsatz'})
  return newclause

def Relativsatz(phrase):
  relative = phrase.get('gender')
  node = ET.SubElement(phrase, 'ATTRIBUT')
  clause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Relativsatz', 'relative': relative})
  # check for pronoun head, then neutrum relator is 'was'
  # also empty relator is possible, leading to 'dass'
  head = clause.getparent().getparent().find('REFERENT')
  if head.text is None:
    clause.set('kind', 'Pronominalrelativsatz')
  return clause
  
# NOTE: 'das, was' Konstruktion, 'freier Relativsatz'
# Head seems to be relative pronoun (check 'dessen')
# encoded as combination of Referenz(m/f/n/p) with relative clause.
# Adverbial relator: Die Urlauber füllen sie fleißig mit dem, was sie am Strand finden.

# gender is decided on insertion of pronoun, because relator in relative clause agrees
# Ich sehen den, der da liegt.

def Pronominalrelativsatz(phrase, gender):
  Nomen(phrase, gender)
  Demonstrativ(phrase)
  clause = Relativsatz(phrase)
  # check for pronoun head, then neutrum relator is 'was'
  # also empty relator is possible, leading to 'dass'
  head = clause.getparent().getparent().find('DETERMINATIV')
  if head is not None:
    clause.set('kind', 'Pronominalrelativsatz')
  return clause

# ============
# Kontrollsatz
# ============

# TODO: trace 'es' sometimes possible, sometimes required
# e.g. 'Ich habe es beim Sport gehasst, rennen zu müssen.'

def Komplementkontrollsatz(clause, role):
  newclause = Komplementsatz(clause, role)
  newclause.set('kind', 'Kontrollsatz')
  setcontrol(clause, newclause)
  return newclause

def Präpositionskontrollsatz(clause, juncture):
  node = ET.SubElement(clause, 'ADVERBIALE')
  ET.SubElement(node, 'JUNKTOR').text = juncture
  newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Präpositionskontrollsatz'})
  setcontrol(clause, newclause)
  return newclause 

def Partizipsatz(phrase):
  node = ET.Element('ATTRIBUT')
  clause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Partizipsatz'})
  setcontrol(phrase, clause)
  PartizipPräsens(clause) # by default
  # insert after determiner, or at end in koordination
  if phrase[0].tag == 'DETERMINATIV':
    phrase.insert(1, node)
  elif phrase.tag == 'KOORDINATION':
    phrase.append(node)
  else:
    phrase.insert(0, node)
  return clause

# Alternative: turn finite Relatorsatz into Kontrollsatz

def Infinit(clause):
  node = findverb(clause)
  node.set('tense', 'Infinit')
  kind = clause.get('kind')
  # reset control
  if kind == 'Komplementsatz':
    clause.set('kind', 'Kontrollsatz')
    # find controlling clause
    control = clause
    control = control.getparent()
    while control.tag != 'SATZ':
      control = control.getparent()
    setcontrol(control, clause)
  elif kind == 'Präpositionssatz':
    clause.set('kind', 'Präpositionskontrollsatz')
    control = clause.getparent().getparent()
    setcontrol(control, clause)
    # remove 'dass' from Präpositionssatz
    dass = clause.find('RELATOR')
    clause.remove(dass)
  elif kind == 'Relativsatz':
    clause.set('kind', 'Partizipsatz')
    # find controlling phrase
    attribut = clause.getparent()
    phrase = clause.getparent().getparent()
    # move clause to adjective position
    if phrase[0].tag == 'DETERMINATIV':
      phrase.insert(1, attribut)
    elif phrase.tag == 'KOORDINATION':
      phrase.append(attribut)
    else:
      phrase.insert(0, attribut)
    # reset control
    setcontrol(phrase, clause)
    PartizipPräsens(clause) # by default

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
    controller = node.find('REFERENT').text
    # set attributes partizipsatz
    newclause.set('controller', controller)
    newclause.set('case', case)
    newclause.set('relative', relative)
    newclause.set('declension', declension)

# =======

# Attribut
# 'kind': 'Genitivsatz'
# mashup of genitive attribute and relative clause
# e.g. "die Konsequenz dessen, dass im Wettbewerb immer mehr Geld verdient wird"
# 'dessen' is a juncture here, not a relator!

# Nominalprädikat:
# retention of pronoun 'Reversed relative clause' (Gender/number determined by Subject)
# e.g. "Mein Eindruck ist der, dass Sie Ihre Meinung exklusiv haben"
# article determined by case, then followed by a 'dass' Satz
# gender/number determined by subject

# Argument:
# The following is an alternative to a regular Komplementsatz: daran ~ an dem
# e.g. "Es ist ein vernünftiger Kompromiss, der festhält an dem, dass Klimaschutz auch und gerade Angelegenheit der deutschen Wirtschaft ist."

# da-Relativsatz: possibly better kind of Nominalprädikat
# 'Es ist die Rede/Folge/Verständnis davon, dass  

# ===========
# Prädikation
# ===========

# generic predicate insertion. Defaults to Präsens.

def Prädikat(clause, verb):
  if verb in ['sein', 'werden', 'bleiben']:
    Prädikativ(clause, verb)
  else:
    Verb(clause, verb)

# tense is Präsens by default and has to be explicitly changed to an infinite from
# insertion point 'break' is added to make Mittelfeld-insertion easier. Removed at the end

def Verb(clause, verb):
  # prepare node
  prädikat = ET.Element('PRÄDIKAT', attrib = {'verb': verb})
  if verb in Verben:
    # lexicales preverbs are split
    if Verben[verb].get('Präverb', False):
      ET.SubElement(prädikat, 'PRÄVERBIALE').text = Verben[verb]['Präverb']
      verb = Verben[verb]['Stamm']
      prädikat.set('verb', verb)
    # go through all roles
    for role,case in Verben[verb]['Rollen'].items():
        ET.SubElement(clause, 'ARGUMENT', attrib = {'role': role, 'case': case})
  # when verbs are not in the lexicon, assume as single subject role in nominative
  else:
    rolename = verb.capitalize() + 'de'
    ET.SubElement(clause, 'ARGUMENT', attrib = {'role': rolename, 'case': 'Nominativ'})
  # insertion point, removed at end
  ET.SubElement(clause, 'break') 
  # insert verb
  clause.append(prädikat)
  # default Präsens
  Präsens(clause)

# combine adverbial, adjectival and nominal predication.
# preposition needs trick 'ich bin in den Garten' with the addition of PHRASE

def Prädikativ(clause, auxiliary = 'sein'):
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  ET.SubElement(clause, 'break')
  ET.SubElement(clause, 'PRÄDIKATIV', attrib = {'role': 'Prädikativ', 'case': 'Nominativ'})
  verb = ET.SubElement(clause, 'PRÄDIKAT', attrib = {'verb': auxiliary})
  # default Präsens
  Präsens(clause)

# this function should rebuild a nominal phrase into a nominal predication
# 'ich warte auf den Vater' -> 'ich warte darauf, dass ich Vater bin'.

def Finit(phrase, auxiliary = 'sein'):
  # change phrase to predication in subordinate position
  parent = phrase.getparent()
  grandparent = parent.getparent()
  # move subordinatoe to back
  grandparent.append(parent)
  # change juncture
  juncture = parent.find('JUNKTOR')
  if juncture is not None:
    juncture.text = 'da' + addR(juncture.text) + juncture.text
    parent.set('move', 'da-Junktor')
  # insert new clause
  clause = ET.SubElement(parent, 'SATZ', attrib = {'kind': 'Komplementsatz'})
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  ET.SubElement(clause, 'break')
  predicative = ET.SubElement(clause, 'PRÄDIKATIV')
  ET.SubElement(clause, 'PRÄDIKAT')
  # insert original phrase
  predicative.append(phrase)
  # add auxiliary to predication
  verb = clause.find('PRÄDIKAT')
  verb.set('verb', auxiliary)
  # default Präsens
  Präsens(clause)
  return clause

# Alternatively, the verb 'haben (besitzen)' can be included as a main verb with these roles.
# note the accusative case
def Besitz(clause, verb = 'haben'):
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Besitzer', 'case': 'Nominativ'})
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Besitz', 'case': 'Akkusativ'})
  ET.SubElement(clause, 'break') 
  ET.SubElement(clause, 'PRÄDIKAT', attrib = {'verb': verb, 'tense': 'Präsens'})

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
  if clause.get('kind') == 'Partizipsatz':
    clause.set('variant', 'Vergangenheit')

def PartizipPräsens(clause):
  # only for Partizipsatz!
  if clause.get('kind') == 'Partizipsatz':
    clause.set('variant', 'Präsens')

def PartizipFutur(clause):
  # only for Partizipsatz!
  if clause.get('kind') == 'Partizipsatz':
    clause.set('variant', 'Futur')

def Vorgangspassiv(clause, demoted = 'von'):
  addlightverb(clause, 'werden', 'Partizip', 'VORGANGSPASSIV')
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

def ReflexivErlebniskonversiv(clause):
  verb = clause.find('PRÄDIKAT').get('verb')
  juncture = Verben[verb]['Konversiv']
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

def Perfekt(clause):
  node = findverb(clause)
  verb = node.get('verb')
  auxiliary = Verben[verb]['Perfekt']
  addlightverb(clause, auxiliary, 'Partizip', 'PERFEKT')

def Modalverb(clause, modal):
  addlightverb(clause, modal, 'Infinitiv', 'MODALVERB')

def Präsens(clause):
  node = findverb(clause)
  node.set('tense', 'Präsens')

def Präteritum(clause):
  node = findverb(clause)
  node.set('tense', 'Präteritum')

# ======
# Phrase
# ======

def Phrase(addto, connection = None):
  parent = addto.getparent()
  if parent is not None:
    grandparent = parent.getparent()
  # ======
  # argument phrase
  # ======
  node = addto.find(f'*[@role="{connection}"]')
  predicative = addto.find('*[@role="Prädikativ"]')
  if node is not None:
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
      # strange exception in case assignment for governed prepositions
      case = Präpositionen[juncture]
      if juncture in ['auf', 'über']:
        case = 'Akkusativ'
      ET.SubElement(leaf, 'JUNKTOR').text = juncture
    phrase = ET.SubElement(leaf, 'PHRASE', attrib = {'case': case})
  # special case for prepositional connection to a predicative phrase 'ich bin im Garten'
  # assumes there are no diatheses above
  elif predicative is not None and not predicative:
    case = Präpositionen[connection]
    ET.SubElement(predicative, 'JUNKTOR').text = connection
    phrase = ET.SubElement(predicative, 'PHRASE', attrib = {'case': case})
  # ======
  # adverbial phrase
  # ======
  elif addto.tag == 'SATZ' or (addto.tag == 'KOORDINATION' and grandparent.tag == 'SATZ'):
    # prepare node
    node = ET.Element('ADVERBIALE')
    # find insertion point for branch
    if addto.tag == 'KOORDINATION':
      addto.append(node)
    else:
      insertafter = addto.find('break')
      place = list(addto).index(insertafter) + 1
      addto.insert(place, node)
    # prepositionphrase
    if connection is not None:
      ET.SubElement(node, 'JUNKTOR').text = connection
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionen[connection]})
    # No juncture then measurephrase in accusative, e.g. 'den ganzen Tag'
    else:
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Akkusativ'})
  # ======
  # attribute phrase
  # ======
  elif addto.tag == 'PHRASE' or grandparent.tag == 'PHRASE':
    # when in coordination, move coordination to behind referent
    if addto.tag == 'KOORDINATION':
      if len(addto.findall('*')) ==  1:
        referent = grandparent.find('REFERENT')
        place = list(grandparent).index(referent) + 1
        grandparent.insert(place, parent)
    # simply add attribute to end of the phrase
    node = ET.SubElement(addto, 'ATTRIBUT')
    # prepositionphrase
    if connection is not None:
      ET.SubElement(node, 'JUNKTOR').text = connection
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionen[connection]})
    # Genitive when no juncture
    else:
      phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Genitiv'})
  # ======
  # For relators: add info to all phrases
  relative = addto.get('relative')
  kind = addto.get('kind')
  if relative is not None:
    phrase.set('relative', relative)
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
  # ======
  # in a coordination
  # ======
  if addto.tag == 'KOORDINATION':
    coordination = addto
    parent = addto.getparent()
    grandparent = parent.getparent()
    # Adverbprädikat
    if parent.tag == 'PRÄDIKATIV':
      node = ET.SubElement(coordination, "PRÄDIKATIV")
      ET.SubElement(node, "ADVERB").text = adverb
    # Adverb Adverbiale
    elif grandparent.tag == 'SATZ':
      # prepare new adverbial node
      node = ET.SubElement(coordination, "ADVERBIALE")
      ET.SubElement(node, "ADVERB").text = adverb
    # Adverb Attribut
    elif grandparent.tag == 'PHRASE':
      if len(addto.find('*')) == 1:
        # move coordination to behind referent
        referent = grandparent.find('REFERENT')
        place = list(grandparent).index(referent) + 1
        grandparent.insert(place, parent)
        # prepare new attributive node
        node = ET.SubElement(coordination, 'ATTRIBUT')
        ET.SubElement(node, 'ADVERB').text = adverb
  # ======
  # not in a coordination
  # ======
  else:
    # Adverbprädikat
    node = addto.find('PRÄDIKATIV')
    if node is not None and not node:
      ET.SubElement(node, "ADVERB").text = adverb
    elif adverb in Frageadverbien:
      node = ET.SubElement(addto, 'ADVERBIALE')
      sub = ET.SubElement(node, 'FRAGEWORT')
      sub.text = adverb
      if addto.get('kind') == 'Hauptsatz':
        addto.set('mood', 'Fragesatz')
        Vorfeld(node)
      else:
        sub.tag = 'RELATOR'
        Relator(node)
    # Adverb Adverbiale
    elif addto.tag == 'SATZ':
      # prepare new adverbial node
      node = ET.Element("ADVERBIALE")
      ET.SubElement(node, "ADVERB").text = adverb
      # insert after arguments
      insertafter = addto.find('break')
      place = list(addto).index(insertafter) + 1
      addto.insert(place, node)
    # Adverb Attribut
    elif addto.tag == 'PHRASE':
      # this is rare, e.g. 'das Treffen gestern'
      # prepare new attributive node
      node = ET.SubElement(addto, 'ATTRIBUT')
      ET.SubElement(node, 'ADVERB').text = adverb
  return node

def Adjektiv(addto, adjective):
  # ======
  # in a coordination
  # ======
  if addto.tag == 'KOORDINATION':
    coordination = addto
    parent = addto.getparent()
    grandparant = parent.getparent()
    # Adjektivprädikat
    if parent.tag == 'PRÄDIKATIV':
      node = ET.SubElement(coordination, "PRÄDIKATIV")
      ET.SubElement(node, "ADJEKTIV").text = adjective
    # Adjektiv Adverbiale
    elif grandparant.tag == 'SATZ':
      # prepare new adverbial node
      node = ET.SubElement(coordination, "ADVERBIALE")
      ET.SubElement(node, "ADJEKTIV").text = adjective
    # Adjektiv Attribut
    elif grandparant.tag == 'PHRASE':
      # get agreement features
      case = grandparant.get('case')
      gender = grandparant.get('gender')
      declension = grandparant.get('declension')
      # prepare new attributive node
      node = ET.SubElement(coordination, 'ATTRIBUT')
      ET.SubElement(node, 'ADJEKTIV').text = \
        adjective + Adjektivflexion[declension][case][gender]
  # ======
  # not in a coordination
  # ======
  else:
    # Adjektivprädikat
    node = addto.find('PRÄDIKATIV')
    if node is not None and not node:
      ET.SubElement(node, "ADJEKTIV").text = adjective
    # Adjektiv Adverbiale
    elif addto.tag == 'SATZ':
      # prepare new adverbial node
      node = ET.Element("ADVERBIALE")
      ET.SubElement(node, "ADJEKTIV").text = adjective
      # insert after arguments
      insertafter = addto.find('break')
      place = list(addto).index(insertafter) + 1
      addto.insert(place, node)
    # Adjektiv Attribut
    elif addto.tag == 'PHRASE':
      # add agreement features
      case = addto.get('case')
      gender = addto.get('gender')
      declension = addto.get('declension')
      adjective = adjective + Adjektivflexion[declension][case][gender]
      # check if referent is absent, then adjective becomes head
      if addto.find('REFERENT').text is None:
        adjective = adjective.capitalize()
        node = ET.Element('REFERENT')
      # prepare new attributive node
      else:
        node = ET.Element('ATTRIBUT')
      # insert
      ET.SubElement(node, 'ADJEKTIV').text = adjective
      # insert after determiner
      addto.insert(1, node)
  # return for Gradpartikel
  return node

# TODO attributes can be detached to become secondary predicates

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

def Adverbialpräposition(adverbial, preposition):
  # insert before adverbial
  node = ET.Element('ADVERBIALPRÄPOSITION')
  node.text = preposition
  adverbial.insert(0, node)

# NOTE: the following is a combination of two adverbials
# "vorne/hinten im Garten"
# they have to be inserted separately
# semantics are inferred from regular scoping of multiple modifiers
# also for 'noch nicht' ???

# ========
# Referenz
# ========

# TODO indefinita 'irgendwer', 'jemand' etc.

def Referenz(phrase, referent = None):
  if referent == 'wer':
    Fragepronomen(phrase)
  # insert personal pronoun
  elif referent[0].isnumeric():
    Pronomen(phrase, referent)
  # insert demonstrative/relative
  elif referent in list('mfnp'):
    Nomen(phrase, referent)
  # insert noun
  elif referent not in Markierungen:
    Nomen(phrase, referent)
  # make reference to another referent
  else:
    Anapher(phrase, referent)

def Anapher(phrase, referent):
  # reflexive pronoun, agreement set by Kongruenz at Satzende
  case = phrase.get('case')
  ET.SubElement(phrase, 'ANAPHER', attrib = {'case': case, 'referent': referent})

def Fragepronomen(phrase):
  case = phrase.get('case')
  pronoun = Fragepronomina[case]
  sub = ET.SubElement(phrase, 'FRAGEWORT').text = pronoun
  if phrase.get('kind') == 'Hauptsatz':
    phrase.set('mood', 'Fragesatz')
    Vorfeld(phrase)
  else:
    sub.tag = 'RELATOR'
    Relator(phrase)

def Pronomen(phrase, pronoun):
  # personal pronoun
  if pronoun[-1:] == 'p':
    number = 'Plural'
  elif pronoun[-1:] == 's':
    number = 'Singular'
  person = pronoun[:-1]
  node = ET.SubElement(phrase, 'PRONOMEN')
  # if koordination, set flags on parent,
  if phrase.tag == 'KOORDINATION':
    phrase = phrase.getparent()
  # get attributes from phrase
  case = phrase.get('case')
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

def Nomen(phrase, referent):
  # get attributes from phrase
  case = phrase.get('case')
  # set referent as attribute
  phrase.set('referent', referent)
  # insert extra PHRASE when inside koordination
  if phrase.tag == 'KOORDINATION':
    node = ET.SubElement(phrase, 'PHRASE')
    node.set('case', case)
    # set flags above for agreement
    phrase.getparent().set('person', '3')
    phrase.getparent().set('gender', 'Plural')
    phrase = node
  # with empty head, gender determined for rest
  # adjective can be used as head
  # with demonstratives and relative clause this leads to 'freier relativsatz'
  elif referent in list('mfnp'):
    abbreviations = {'m': 'Maskulin', 'f': 'Feminin', 'n': 'Neutrum', 'p': 'Plural'}
    gender = abbreviations[referent]
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
  if referent is not None:
    if declination == 'schwach' and case != 'Nominativ':
      referent = referent + 'en'
    elif declination == 'stark' and case == 'Genitiv':
      referent = referent + 'es'
  # insert node for reference
  # insert default definite article, possibly replaced by Quantor
  ET.SubElement(phrase, 'DETERMINATIV')   
  ET.SubElement(phrase, "REFERENT").text = referent
  # set flags for agreement with adjective
  phrase.set('gender', gender)
  phrase.set('person', '3')
  # for convenience, insert definite article
  Definit(phrase)

# =============
# Determination
# =============

def Plural(phrase):
  # only for Nomen!
  # current implementation assumes this comes before Quantor/Possessiv
  # get attributes from phrase
  case = phrase.get('case')
  noun = phrase.get('referent')
  # change form of noun
  if noun is not None:
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
  # absence of determiner means generic reference, which has no article in German
  determiner = phrase.find('DETERMINATIV')
  # remove anything present
  ET.strip_elements(determiner, '*')
  # set declension for agreement
  phrase.set('declension', 'stark')

def Demonstrativ(phrase):
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
  fokus = ET.Element("FOKUSPARTIKEL")
  fokus.text = particle
  phrase.insert(0, fokus)

# ============
# Markierungen
# ============

def Markierung(phrase, name):
  phrase.set('mark', name)
  # add name to local dictionary
  Markierungen[name] = {'Person': phrase.get('person')}
  Markierungen[name]['Geschlecht'] = phrase.get('gender')

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
  # prepare koordination node
  node = ET.Element('KOORDINATION')
  node.set('addto', addto.tag)
  ET.SubElement(node, 'KONJUNKTION').text = conjunction
  # coordination in a phrase
  if addto.tag == 'PHRASE':
    # coordination of phrases when not yet referenced
    if addto.find('REFERENT') is None:
      addto.append(node)
    else:
      # coordination of attributes
      attribute = ET.Element('ATTRIBUT')
      attribute.append(node)
      # insert after determiner by default
      # depending on content, it will be moved to the back by 'Koordinationposition'
      if addto[0].tag == 'DETERMINATIV':
        addto.insert(1, attribute)
      else:
        addto.insert(0, attribute)
  # coordination in sentences
  elif addto.tag == 'SATZ':
    # coordination of adjectival/adverbial predicates
    if addto.find('PRÄDIKATIV') is not None:
      addto.find('PRÄDIKATIV').append(node)
    # coordination of Hauptsatz when not yet predicated
    elif addto.find('PRÄDIKAT') is None:
      addto.append(node)
    else:
      # coordination of adverbials 
      adverbial = ET.Element('ADVERBIALE')
      adverbial.append(node)
      # insert after arguments by default
      # will be moved to back for adverbial sentences by 'Koordinationposition'
      insertafter = addto.find('break')
      place = list(addto).index(insertafter) + 1
      addto.insert(place, adverbial)
  return node
 
# ========
# Satzende
# ========

def Satzende(satz, clean = True):
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
  # set unbound anaphora
  Anaphora(satz)
  # optional cleanup of attributes for readability
  if clean:
   cleanup(satz)

def Kongruenz(clause):
  # find verb
  finitum = findverb(clause)
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
  if clause.get('kind') in ['Kontrollsatz', 'Präpositionskontrollsatz']:
    # Control replaces subject person/number
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
    ET.SubElement(finitum, 'FINITUM', 
      attrib = {'verb': verb, 'tense': tense, 'person': person, 'number': number}).text = finite
  # find reflexives and set person/number agreement
  for child in clause:
    for node in child.iter():
      if node.tag == 'REFLEXIV': # only reflexives from diathesis!
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
        person = Markierungen[referent]['Person']
        gender = Markierungen[referent]['Geschlecht']
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
  # set all unresolved anaphora
  for node in satz.iter():
    if node.tag == 'ANAPHER':
      case = node.get('case')
      referent = node.get('referent')
      person = Markierungen[referent]['Person']
      gender = Markierungen[referent]['Geschlecht']
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
    finitum = findverb(clause)
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

def Komplementsatzposition(satz):
  # separate complement clause from its preposition
  for clause in findallclauses(satz):
    for child in clause:
      if child.get('move') == 'da-Junktor' and child.get('position') is None:
          child.attrib.pop('move')
          # copy juncture
          daJunktor = deepcopy(child)
          drop = daJunktor.find('.//SATZ')
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

def findverb(clause):
  node = clause.find('PRÄDIKAT')
  verb = list(node.iterfind(".//*[@verb]"))
  if len(list(verb)) > 0:
    return verb[-1]
  else:
    return node

def findallclauses(satz):
  # clauses that are named with 'kind'
  clauses = satz.findall('.//SATZ[@kind]')
  # add main clause, when Hauptsatz
  if satz.get('kind') == 'Hauptsatz':
    clauses.append(satz)
  return clauses

def findcase(clause, value):
  result = None
  for child in clause:
    if child.tag == 'ARGUMENT':
      for node in child.iter():
        if node.tag == 'PHRASE' and node.get('case') == value:
          result = node
        if node.tag == 'SATZ':
          break
  return result

def addlightverb(clause, auxiliary, nonfinite, label):
  node = findverb(clause)
  tense = node.get('tense')
  verb = node.get('verb')
  if nonfinite == 'Partizip':
    if 'Partizip' in Verben[verb]:
      form = Verben[verb]['Partizip']
    else:
      form = participle(verb)
  elif nonfinite == 'zu-Infinitiv':
    form = 'zu ' + verb
  elif nonfinite == 'Infinitiv':
    form = verb
  ET.SubElement(node, nonfinite.upper()).text = form
  ET.SubElement(node, label, attrib = {'verb': auxiliary, 'tense': tense})
  node.attrib.pop('tense')

def addR(preposition):
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
  stem = verbstem(verb)
  prefixes = ['ge', 'be', 'er', 'ver', 'zer', 'ent', 'miss']
  if sum([stem.startswith(prefix) for prefix in prefixes]) == 1:
    ge = ''
  else:
    ge = 'ge'
  if stem[-1:] in list('mntd'):
    participle = ge + stem + 'et'
  else:
    participle = ge + stem + 't'
  return participle

def verbfinite(verb, person, number, tense):
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
  case = clause.get('case')
  declension = clause.get('declension')
  gender = clause.get('relative')
  variant = clause.get('variant')
  if variant == 'Vergangenheit':
    if 'Partizip' in Verben[verb]:
      partizip = Verben[verb]['Partizip']
    else:
      partizip = participle(verb)
  elif variant == 'Präsens':
    partizip = verb + 'd'
  elif variant == 'Futur':
    partizip = 'zu ' + verb + 'd' 
  return partizip + Adjektivflexion[declension][case][gender]

# ======
# Output
# ======

def cleanup(satz):
  for clause in findallclauses(satz):
    keep = ['kind', 'controller', 'move', 'mood']
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

# =======
# Lexicon
# =======

Verben = {
  'warten':{
    'Perfekt': 'haben',
    'Rollen':{
      'Wartende': 'Nominativ',
      'auf': 'Akkusativ'
    },
    'Kontrolle': 'Wartende',
    'Kontrolliert': 'Bewartete'
  },
  'versprechen':{
    'Partizip': 'versprochen',
    'Perfekt': 'haben',
    'Rollen':{
      'Versprechende': 'Nominativ',
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
    'Rollen':{
      'Kommende': 'Nominativ'
    }
  },
  'ärgern':{
    'Perfekt': 'haben',
    'Konversiv': 'über',
    'Rollen':{
      'Ärger': 'Nominativ',
      'Ärgernde': 'Akkusativ',
    },
    'Kontrolle': 'Ärgernde',
    'Kontrolliert': 'Ärger',
  },
  'freuen':{
    'Perfekt': 'haben',
    'Konversiv': 'über',
    'Rollen':{
      'Freudeauslösende': 'Nominativ',
      'Freuende': 'Akkusativ',
    },
    'Kontrolle': 'Freuende',
    'Kontrolliert': 'Freudeauslösende',
  },
  'erwarten':{
    'Perfekt': 'haben',
    'Rollen':{
      'Erwartende': 'Nominativ',
      'Erwartete': 'Akkusativ'
    },
    'Kontrolle': 'Erwartende',
    'Kontrolliert': 'Erwartete',
  },
  'laufen':{
    'Partizip': 'gelaufen',
    'Perfekt': 'haben',
    'Rollen':{
      'Laufende': 'Nominativ'
    },
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
  'sehen':{
    'Partizip': 'gesehen',
    'Perfekt': 'haben',
    'Rollen': {
      'Sehende': 'Nominativ',
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
    'Perfekt': 'haben',
    'Rollen': {
      'Besitzende': 'Nominativ',
      'Besitz': 'Akkusativ'
    },
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
    'Partizip': 'worden',
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
    'Perfekt': 'haben',
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
    'Perfekt': 'haben',
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
  }
}

Substantive = {
  'Mutter':{
    'Geschlecht': 'Feminin',
    'Plural': 'Mutter',
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

Markierungen = dict()

# =======
# Lexicon
# =======

Konjunktionen = ['und', 'aber', 'doch']
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

Adverbien = ['selbst', 'da', 'dort', 'draußen', 'hier', 'hinten', 'links', 'rechts', 'überall', 'drinnen', 'draußen', 'oben', 'vorn', 'anfangs', 'früh', 'morgens', 'mittags', 'nachmittags', 'abends', 'nachts', 'neulich', 'vorgestern', 'gestern', 'morgen', 'übermorgen', 'heute', 'stündlich', 'nun', 'jetzt', 'bald', 'bisher', 'blindlings', 'keineswegs', 'halbwegs', 'meinerseits', 'allerdings', 'oft', 'manchmal', 'natürlich', 'gewiss', 'unbedingt', 'keinesfalls']
Frageadverbien = ['warum', 'weshalb', 'wieso', 'wofür', 'wo', 'wohin', 'woher', 'wann', 'wie']
Negationen = ['nicht', 'nie', 'niemals', 'nicht mehr']

# NOTE: it looks like adjectives can not be used productively!
# new ones are mainly added through derivation or complete new innovation
Adjektive = ['albern', 'alt', 'arg', 'arm', 'barsch', 'bieder', 'bitter', 'blank', 'blass', 'blau', 'bleich', 'blind', 'blöd', 'blond', 'bös', 'böse', 'braun', 'brav', 'breit', 'brüsk', 'bunt', 'derb', 'deutsch', 'dicht', 'dick', 'doof', 'dreist', 'dumm', 'dumpf', 'dunkel', 'dünn', 'dürr', 'düster', 'echt', 'edel', 'eigen', 'einzig', 'eitel', 'elend', 'eng', 'ernst', 'fad', 'falsch', 'faul', 'feig', 'feige', 'fein', 'feist', 'fern', 'fesch', 'fest', 'fett', 'feucht', 'fies', 'finster', 'firn', 'flach', 'flau', 'flink', 'flott', 'forsch', 'frech', 'frei', 'fremd', 'froh', 'fromm', 'früh', 'gar', 'geil', 'gelb', 'gemein', 'genau', 'gerade', 'gering', 'geschwind', 'gesund', 'glatt', 'gleich', 'grau', 'greis', 'grell', 'grob', 'groß', 'grün', 'gut', 'hager', 'harsch', 'hart', 'heikel', 'heil', 'heiser', 'heiß', 'heiter', 'hell', 'herb', 'hoh', 'hohl', 'hübsch', 'irr', 'jäh', 'jung', 'kahl', 'kalt', 'kaputt', 'karg', 'keck', 'kess', 'keusch', 'kirre', 'klamm', 'klar', 'klein', 'klug', 'knapp', 'krank', 'krass', 'kraus', 'krud', 'krumm', 'kühl', 'kühn', 'kurz', 'lahm', 'lang', 'lasch', 'lau', 'laut', 'lauter', 'lecker', 'leer', 'leicht', 'leise', 'licht', 'lieb', 'lila', 'locker', 'los', 'mager', 'matt', 'mies', 'mild', 'morsch', 'müde', 'munter', 'mürb', 'nackt', 'nah', 'nass', 'nett', 'neu', 'nieder', 'öd', 'offen', 'orange', 'platt', 'plump', 'prall', 'prüde', 'rank', 'rar', 'rasch', 'rau', 'rauch', 'recht', 'rege', 'reich', 'reif', 'rein', 'roh', 'rosa', 'rot', 'rüd', 'rund', 'sacht', 'sanft', 'satt', 'sauber', 'sauer', 'schal', 'scharf', 'scheu', 'schick', 'schief', 'schlaff', 'schlank', 'schlapp', 'schlau', 'schlecht', 'schlicht', 'schlimm', 'schmal', 'schmuck', 'schnell', 'schnöd', 'schön', 'schräg', 'schrill', 'schroff', 'schwach', 'schwarz', 'schwer', 'schwul', 'schwül', 'seicht', 'selten', 'sicher', 'spät', 'spitz', 'spröd', 'stark', 'starr', 'steif', 'steil', 'stier', 'still', 'stolz', 'straff', 'stramm', 'streng', 'stumm', 'stumpf', 'stur', 'süß', 'tapfer', 'taub', 'teuer', 'tief', 'toll', 'tot', 'träg', 'treu', 'trocken', 'trüb', 'unscharf', 'übel', 'vag', 'viel', 'voll', 'wach', 'wacker', 'wahr', 'warm', 'weh', 'weich', 'weise', 'weiß', 'weit', 'wild', 'wirr', 'wirsch', 'wund', 'wüst', 'zäh', 'zähe', 'zahm', 'zart']

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
  # governed roles are variable: auf/über take accusative, an takes dative
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
