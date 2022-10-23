import xml.etree.ElementTree as ET
import copy

# =====
# Sätze
# =====

def Satz(attach = None):
  if attach is None:
    sentence = ET.Element('SATZ', attrib = {'kind': 'Hauptsatz'})
  else:
    sentence = ET.SubElement(attach, 'SATZ', attrib = {'kind': 'Hauptsatz'})
    if attach.get('kind') is not None:
      attach.attrib.pop('kind')
  return sentence

def Satzende(satz, clean = True):
  if satz.get('kind') == 'Hauptsatz':
    Kongruenz(satz)
    Verbzweit(satz)
    Vorfeld(satz)
  for clause in reversed(satz.findall('.//SATZ[@kind]')):
    Kongruenz(clause)
    if clause.get('kind') == 'Hauptsatz':
      Verbzweit(clause)
    Vorfeld(clause)
  if clean:
    cleanup(satz)

# ===========
# Prädikation
# ===========

def Prädikation_Verb(clause, verb, tense = None):
  if tense is None:
    tense = 'Infinit'
  for role,case in Rollen[verb].items():
    ET.SubElement(clause, 'ARGUMENT', attrib = {'role': role, 'case': case})
  ET.SubElement(clause, 'PRÄDIKAT', attrib = {'verb': verb, 'tense': tense})
  return clause

def Prädikation_Nominal(clause, verb = 'sein', tense = None):
  if tense is None:
    tense = 'Infinit'
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Nominalprädikat', 'case': 'Nominativ'})
  ET.SubElement(clause, 'PRÄDIKAT', attrib = {'verb': verb, 'tense': tense})

def Prädikation_Adjektiv(clause, adjective, verb = 'sein', tense = None, intensifier = None, position = None):
  if tense is None:
    tense = 'Infinit'
  ET.SubElement(clause, 'ARGUMENT', attrib = {'role': 'Subjekt', 'case': 'Nominativ'})
  node = ET.SubElement(clause, 'ADJEKTIVPRÄDIKAT')
  if intensifier is not None:
    ET.SubElement(node, "GRADPARTIKEL").text = intensifier
  ET.SubElement(node, "ADJEKTIV").text = adjective
  ET.SubElement(clause, 'PRÄDIKAT', attrib = {'verb': verb, 'tense': tense})
  # set flag for fronting
  if position is not None:
    node.set('position', position)

# =========
# Ableitung
# =========

def Diathese_Vorgangspassiv(clause, demoted = 'von'):
  addlightverb(clause, 'werden', 'Partizip', 'VORGANGSPASSIV')
  for node in clause.findall('ARGUMENT'):
    leaf = list(node.iter())[-1]
    if leaf.get('case') == 'Nominativ':
      if demoted is not None:
        ET.SubElement(node, 'VORGANGSPASSIV', attrib = {'juncture': demoted})
      else:
        clause.remove(leaf)
    if leaf.get('case') == "Akkusativ":
      ET.SubElement(node, 'VORGANGSPASSIV', attrib = {'case':'Nominativ'})
      clause.insert(0, copy.deepcopy(node))
      clause.remove(node)

def Diathese_ReflexivErlebniskonversiv(clause):
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
      clause.insert(0, copy.deepcopy(node))
      clause.remove(node)

def Epithese_Perfekt(clause):
  node = findverb(clause)
  verb = node.get('verb')
  addlightverb(clause, Verben[verb]['Perfekt'], 'Partizip', 'PERFEKT')

# ========
# Argument
# ========

def Argument_Phrase(clause, role, position = None):
  node = clause.find(f'ARGUMENT[@role="{role}"]')
  # set flag for fronting
  if position is not None:
    node.set('position', position)
  # go to tip of branch to add stuff
  leaf = list(node.iter())[-1]
  # change arguments for Partizipsatz
  leaf = switchPartizipsatz(clause, leaf)
  # add phrase
  if leaf.get('case') is not None:
    if clause.get('kind') == 'Weiterführender Relativsatz' and position == 'Relator':
      ET.SubElement(leaf,'PHRASE').text = 'was'
      phrase = ET.Element('dummy', attrib = {'case': 'Akkusativ'}) # will remain empty
    else:
      case = leaf.get('case')
      phrase = ET.SubElement(leaf,'PHRASE', attrib = {'case': case})
  elif leaf.get('juncture') is not None:
    juncture = leaf.get('juncture')
    if clause.get('kind') == 'Weiterführender Relativsatz':
      ET.SubElement(leaf, 'JUNKTOR').text = 'wo' + Daform[juncture]
      phrase = ET.Element('dummy', attrib = {'case': 'Akkusativ'}) # will remain empty
    else:
      case = Präpositionskasus[juncture]
      ET.SubElement(leaf, 'JUNKTOR').text = juncture
      phrase = ET.SubElement(leaf, 'PHRASE', attrib = {'case': case})
  # add gender/number for relative pronouns
  if position == 'Relator':
    phrase.set('relative', clause.get('relative', 'Neutrum'))
  # add role for info
  phrase.set('role', role)
  return phrase

def Argument_Satz(clause, role, position = None):
  node = clause.find(f'ARGUMENT[@role="{role}"]')
  newclause = ET.Element('SATZ', attrib = {'kind': 'Argumentsatz'})
  copynode = copy.deepcopy(node)
  # go to tip of branch to add junktor
  leaf = list(node.iter())[-1]
  # change arguments for Partizipsatz
  leaf = switchPartizipsatz(clause, leaf)
  # add phrase
  juncture = leaf.get('juncture')
  if juncture is not None:
    ET.SubElement(leaf, 'JUNKTOR').text = 'da' + Daform[juncture]
  # set flag for fronting and add newclause
  if position is not None:
    node.set('position', position)
    leaf.append(newclause)
  # when not fronted, add newclause to back
  else:
    # leave trace
    ET.SubElement(leaf, 'SATZ', attrib = {'move': "Satzende"})
    # append sentence to back
    leaf = list(copynode.iter())[-1]
    clause.append(copynode)
    leaf.append(newclause)
    if juncture is None:
      clause.remove(node)
  return newclause

def Argument_Kontrollsatz(clause, role, position = None):
  newclause = setcontrol(clause, Argument_Satz(clause, role, position))
  return newclause

# ==========
# Adverbiale
# ==========

def Adverbiale_Adverb(clause, adverb, position = None):
  node = ET.Element('ADVERBIALE')
  ET.SubElement(node, "ADVERB").text = adverb
  # set flag for fronting
  if position is not None:
    node.set('position', position)
  # find insertion point for branch
  if clause.tag == 'KOORDINATION':
    clause.append(node)
  else:
    insertafter = clause.findall('ARGUMENT')[-1]
    place = list(clause).index(insertafter) + 1
    clause.insert(place, node)
  return node

def Adverbiale_Adjektiv(clause, adjective, intensifier = None, position = None):
  node = ET.Element("ADVERBIALE")
  if intensifier is not None:
    ET.SubElement(node, "GRADPARTIKEL").text = intensifier
  ET.SubElement(node, "ADJEKTIV").text = adjective
  # set flag for fronting
  if position is not None:
    node.set('position', position)
  # find insertion point for branch
  if clause.tag == 'KOORDINATION':
    clause.append(node)
  else:
    insertafter = clause.findall('ARGUMENT')[-1]
    place = list(clause).index(insertafter) + 1
    clause.insert(place, node)
  return node

def Adverbiale_Phrase(clause, juncture = None, position = None, coordination = False):
  node = ET.Element('ADVERBIALE')
  # set flag for fronting
  if position is not None:
    node.set('position', position)
  # find insertion point for branch
  insertafter = clause.findall('ARGUMENT')[-1]
  place = list(clause).index(insertafter) + 1
  clause.insert(place, node)
  # Präpositionsphrase
  if juncture is not None:
    ET.SubElement(node, 'JUNKTOR').text = juncture
    phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionskasus[juncture]})
  # Measurephrase, e.g. 'den ganzen Tag'
  else:
    phrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Akkusativ'})
  # add gender/number for relative pronouns
  if position == 'Relator':
    phrase.set('relative', clause.get('relative', 'Neutrum'))
  # coordination trick: use 'node' for coordination of prepositional phrases
  if coordination:
    return phrase, node
  else:
    return phrase

def Adverbiale_Satz(clause, juncture = None, position = None):
  # insert at end of clause
  node = ET.SubElement(clause, 'ADVERBIALE')
  # set flag for fronting
  if position is not None:
    node.set('position', position)
  if juncture is not None:
    ET.SubElement(node, 'JUNKTOR').text = juncture
    newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Adverbialsatz'})
  else:
    newclause = ET.SubElement(node, 'SATZ', attrib = {'kind': 'Weiterführender Relativsatz'})
  return newclause

def Adverbiale_Kontrollsatz(clause, juncture = None, position = None):
  newclause = setcontrol(clause, Adverbiale_Satz(clause, juncture, position))
  return newclause 

# ========
# Referenz
# ========

def Referenz_Pronomen(phrase, person = None):
  case = phrase.get('case')
  # reflexive pronoun
  if person == 'Reflexiv':
    node = ET.SubElement(phrase, "REFLEXIV", attrib = {'case': case})
  # relative pronoun
  elif phrase.get('relative') is not None:
    relative = phrase.get('relative')
    pronoun = Artikel['Relativpronomen'][case][relative]
    phrase.attrib.pop('relative')
    node = ET.SubElement(phrase, "RELATOR", attrib = {'relative': relative})
    node.text = pronoun
    # set flags for agreement
    phrase.set('person', '3')
    if relative == 'Plural':
      phrase.set('number', 'Plural')
    else:
      phrase.set('number', 'Singular')
  # personal pronoun
  else:
    if person[-1:] == 'p':
      number = 'Plural'
    elif person[-1:] == 's':
      number = 'Singular'
    person = person[:-1]
    node = ET.SubElement(phrase, "PRONOMEN")
    node.text = Personalpronomen[number][person][case]
    # set flags for agreement
    phrase.set('person', person[:1])
    phrase.set('number', number)
  return node

def Referenz_Nomen(phrase, noun, determiner = None, number = None, numeral = None):
  case = phrase.get('case')
  gender = Substantive[noun]['Geschlecht']
  # treat plural as a gender
  if number == 'Plural':
    gender = number
  if number is None:
    number = 'Singular'
  # attributive relative pronoun as genitive
  if phrase.get('relative') is not None:
    relative = phrase.get('relative')
    pronoun = Artikel['Relativpronomen']['Genitiv'][relative]
    declension = 'gemischt'
    phrase.attrib.pop('relative')
    ET.SubElement(phrase, 'RELATOR', attrib = {'relative': relative, 'case': 'Genitiv'}).text = pronoun
  # regular determiner with agreement
  else:
    node = ET.SubElement(phrase, 'DETERMINATIV')
    if determiner is not None:
      article,declension = getdeclension(determiner, case, gender)
      ET.SubElement(node, 'ARTIKEL').text = article
    else:
      declension = 'stark'
    if numeral is not None:
      ET.SubElement(node, 'NUMERALE').text = numeral
  # form of noun
  if number == 'Plural':
    noun = Substantive[noun][number]
  if number == 'Plural' and case == 'Dativ':
    noun = noun + 'n'
  nomen = ET.SubElement(phrase, "REFERENT")
  nomen.text = noun
  # set flags for agreement
  phrase.set('person', '3')
  phrase.set('number', number)
  phrase.set('gender', gender)
  phrase.set('declension', declension)
  return nomen

# ========
# Attribut
# ========

def Attribut_Adjektiv(phrase, adjective, intensifier = None):
  case = phrase.get('case')
  gender = phrase.get('gender')
  declension = phrase.get('declension')
  # prepare node
  node = ET.Element('ATTRIBUT')
  if intensifier is not None:
    ET.SubElement(node, 'GRADPARTIKEL').text = intensifier
  ET.SubElement(node, 'ADJEKTIV').text = adjective + Adjektivflexion[declension][case][gender]
  # insert after determiner, or at end in koordination
  if phrase[0].tag == 'DETERMINATIV':
    phrase.insert(1, node)
  elif phrase.tag == 'KOORDINATION':
    phrase.append(node)
  else:
    phrase.insert(0, node)
  return node

def Attribut_Phrase(phrase, juncture = None, coordination = False):
  node = ET.SubElement(phrase, 'ATTRIBUT')
  if juncture is not None:
    ET.SubElement(node, 'JUNKTOR').text = juncture
    newphrase = ET.SubElement(node, 'PHRASE', attrib = {'case': Präpositionskasus[juncture]})
  else:
    newphrase = ET.SubElement(node, 'PHRASE', attrib = {'case': 'Genitiv'})
  # coordination trick: use 'node' for coordination of prepositional phrases
  if coordination:
    return newphrase,node
  else:
    return newphrase

def Attribut_Satz(phrase):
  relative = phrase.get('gender')
  clause = ET.SubElement(phrase, 'SATZ', attrib = {'kind': 'Attributsatz', 'relative': relative})
  return clause

def Attribut_Partizipsatz(phrase, variant):
  person = phrase.get('person')
  number = phrase.get('number')
  case = phrase.get('case')
  relative = phrase.get('gender')
  declension = phrase.get('declension')
  controller = phrase.get('role')
  clause = ET.Element('SATZ', attrib = {
    'kind': 'Partizipsatz', 'variant': variant, 'controller': controller, 'declension': declension, 
    'case': case, 'relative': relative, 'person': person, 'number': number
    })
  # insert after determiner, or at end in koordination
  if phrase[0].tag == 'DETERMINATIV':
    phrase.insert(1, clause)
  elif phrase.tag == 'KOORDINATION':
    phrase.append(clause)
  else:
    phrase.insert(0, clause)
  return clause

# ============
# Koordination
# ============

def Koordination(attachment, conjunct, conjunction = 'und', position = None):
  # where is conjunct?
  place = [i for i,j in enumerate(attachment) if j == conjunct][0]
  # copy nodes to prepare coordination
  koordination = copy.deepcopy(attachment)
  for child in koordination.findall('*'):
    koordination.remove(child)
  attachment.insert(place, koordination)
  koordination.tag = 'KOORDINATION'
  # copy conjunct to new koordination node
  tmp = conjunct
  attachment.remove(conjunct)
  koordination.append(tmp)
  # add coordination
  if conjunction is not None:
    ET.SubElement(koordination, 'KONJUNKTION').text = conjunction
  # set flag for fronting the whole coordination
  if position is not None:
    koordination.set('position', position)
  # change person/number for agreement
  if attachment.tag == 'PHRASE' and conjunct.tag in ['PRONOMEN', 'REFERENT']:
    # person hierarchy for agreement
    p1 = attachment.get('person')
    p2 = koordination.get('person')
    person = min(p1, p2)
    # set new agreement flags
    attachment.set('person', person)
    attachment.set('number', 'Plural')
  # new conjunct has to be attached to the result of this function
  return koordination

# =======
# Satzart
# =======

def Kongruenz(clause):
  # find verb
  finitum = findverb(clause)
  verb = finitum.get('verb')
  tense = finitum.get('tense')
  finitum.attrib.pop('tense')
  # find subject person/number
  subject = findcase(clause, 'Nominativ')
  if subject is None:
    person = '3'
    number = 'Singular'
  else:
    person = subject.get('person')
    number = subject.get('number')
  # Control replaces subject person/number
  if clause.get('kind') in ['Kontrollsatz', 'Partizipsatz']:
    subject.clear()
    person = clause.get('person')
    number = clause.get('number')
    subject.set('person', person)
    subject.set('number', number)
    subject.set('controller', clause.get('controller'))
  # zu-Infinitiv Kontrollsatz
  if clause.get('kind') == 'Kontrollsatz':
    ET.SubElement(finitum, 'INFINITUM', 
      attrib = {'verb': verb, 'non-finite': 'zu-Infinitiv'}).text = 'zu ' + verb
  # Partizip-Relativsatz
  elif clause.get('kind') == 'Partizipsatz':
    partizip = makePartizip(clause, verb)
    kind = clause.get('variant') + 'partizip'
    ET.SubElement(finitum, 'INFINITUM', 
      attrib = {'verb': verb, 'non-finite': kind}).text = partizip
  # only agreement when tense is finite
  elif tense != 'Infinit':
    finite = Verben[verb][tense][number][person]
    ET.SubElement(finitum, 'FINITUM', 
      attrib = {'verb': verb, 'tense': tense, 'person': person, 'number': number}).text = finite
  # find reflexives and set person/number
  for child in clause:
    for node in child.iter():
      if node.tag == "REFLEXIV":
        setreflexive(node, person, number)
      if node.tag == "SATZ":
        break

def Verbzweit(clause):
  finitum = findverb(clause)
  second = copy.deepcopy(finitum)
  second.tag = 'VERBZWEIT'
  clause.insert(0, second)
  finitum.text = ""
  finitum.attrib.clear()
  finitum.set('move', 'Verbzweit')

def Vorfeld(clause):
  # move to Vorfeld
  for child in clause:
    if child.get('position') == 'Vorfeld':
      child.attrib.pop('position')
      vorfeld = ET.Element('VORFELD')
      vorfeld.append(copy.deepcopy(child))
      clause.insert(0, vorfeld)
      clause.remove(child)
    elif child.get('position') is not None:
      clause.insert(0, copy.deepcopy(child))
      clause.remove(child)
  # Default entry for empty Vorfeld
  if clause[0].tag == 'VERBZWEIT':
    es = ET.Element('VORFELDFÜLLER')
    es.text = 'es'
    clause.insert(0, es)
  # Default relator for Argumentsatz
  if clause.get('kind') == 'Argumentsatz' and clause[0].get('position') is None:
    finitum = findverb(clause)
    if finitum.tag == 'FINITUM':
      dass = ET.Element('RELATOR')
      dass.text = 'dass'
      clause.insert(0, dass)

# ==============
# help functions
# ==============

def findverb(clause):
  node = clause.find('PRÄDIKAT')
  if len(list(node)) > 0:
    node = list(node.iterfind(".//*[@verb]"))[-1]
  return node

def findcase(clause, value):
  result = None
  for child in clause:
    for node in child.iter():
      if node.tag == 'PHRASE' and node.get('case') == value:
        result = node
      if node.tag == 'SATZ':
        break
  return result

def setreflexive(node, person, number):
  if person == '3':
    node.text = 'sich'
  else:
    case = node.get('case')
    node.text = Personalpronomen[number][person][case]
    node.set('person', person)
    node.set('number', number)

def getdeclension(determiner, case, gender):
  if determiner == 'der':
    article = Artikel[determiner][case][gender]
    declension = 'schwach'
  elif determiner in ['dies', 'jen']:
    article = determiner + Artikel['dies'][case][gender]
    declension = 'schwach'
  elif determiner in ['all', 'jed', 'beid', 'solch', 'manch']:
    article = determiner + Artikel['all'][case][gender]
    declension = 'schwach'
  elif determiner in ['ein', 'kein']:
    article = determiner + Artikel['ein'][case][gender]
    declension = 'gemischt'
  elif determiner[:1].isnumeric(): # possessive pronoun
    if determiner[-1:] == 'p':
      possnumber = 'Plural'
    elif determiner[-1:] == 's':
      possnumber = 'Singular'
    person = determiner[:-1]
    article = Personalpronomen[possnumber][person]['Attributiv'] + Artikel['ein'][case][gender]
    declension = 'gemischt'
  return article,declension

def addlightverb(clause, auxiliary, nonfinite, derivation):
  node = findverb(clause)
  tense = node.get('tense')
  verb = node.get('verb')
  ET.SubElement(node, nonfinite.upper()).text = Verben[verb][nonfinite]
  ET.SubElement(node, derivation, attrib = {'verb': auxiliary, 'tense': tense})
  node.attrib.pop('tense')

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

def makePartizip(clause, verb):
  case = clause.get('case')
  declension = clause.get('declension')
  gender = clause.get('relative')
  variant = clause.get('variant')
  if variant == 'Vergangenheit':
    partizip = Verben[verb]['Partizip'] + Adjektivflexion[declension][case][gender]
  elif variant == 'Präsens':
    partizip = verb + 'd' + Adjektivflexion[declension][case][gender]
  elif variant == 'Futur':
    partizip = 'zu ' + verb + 'd' + Adjektivflexion[declension][case][gender]
  return partizip

def setcontrol(clause, newclause):  
  verb = clause.find('PRÄDIKAT').get('verb')
  controller = Kontrolle[verb]
  node = clause.find(f'ARGUMENT[@role="{controller}"]//PHRASE')
  newclause.set('kind', 'Kontrollsatz')
  newclause.set('controller', controller)
  newclause.set('person', node.get('person'))
  newclause.set('number', node.get('number'))
  return newclause

# ======
# Output
# ======

def cleanup(satz):
  for phrase in satz.findall('.//PHRASE'):
    keep = ['case', 'controller', 'move']
    phrase.attrib = {k:v for k,v in phrase.attrib.items() if k in keep}
  for clause in satz.findall('.//SATZ'):
    keep = ['kind', 'controller', 'move']
    clause.attrib = {k:v for k,v in clause.attrib.items() if k in keep}
  for koordination in satz.findall('.//KOORDINATION'):
    koordination.attrib.clear()
 
def capfirst(s):
  return s[:1].upper() + s[1:]

def showresult(clause):
  sentence = ' '.join(clause.itertext())
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

Rollen = {
  'laufen':{
    'Läufer': 'Nominativ'
  },
  'sehen':{
    'Seher': 'Nominativ',
    'Gesehene': 'Akkusativ'
  },
  'erwarten':{
    'Erwarter': 'Nominativ',
    'Erwartete': 'Akkusativ'
  },
  'freuen':{
    'Auslöser': 'Nominativ',
    'Freuer': 'Akkusativ',
  },
  'kommen':{
    'Kommer': 'Nominativ'
  }
}

Kontrolle = {
  'freuen': 'Freuer',
  'erwarten': 'Erwarter',
  'sehen': 'Seher',
  }

Verben = {
  'bleiben':{
    'Partizip': 'geblieben',
    'Perfekt': 'sein',
  },
  'kommen':{
    'Partizip': 'gekommmen',
    'Perfekt': 'sein',
  },
  'freuen':{
    'Partizip': 'gefreut',
    'Perfekt': 'haben',
    'Konversiv': 'über'
  },
  'erwarten':{
    'Partizip': 'erwartet',
    'Perfekt': 'haben'
  },
  'laufen':{
    'Partizip': 'gelaufen',
    'Perfekt': 'haben',
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
    'Partizip': 'gehabt',
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
  }
}

Substantive = {
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
  }
}

# ==============
# Finite Lexicon
# ==============

Präpositionskasus = {
  'von': 'Dativ',
  'mit': 'Dativ',
  'ohne': 'Akkusativ',
  'über': 'Akkusativ' # simplification
}

Daform = {
  'von': 'von',
  'mit': 'mit',
  'über': 'rüber'
}

Personalpronomen = {
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

Artikel = {
  'der':{
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
  },
  'Relativpronomen':{
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
  },
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
