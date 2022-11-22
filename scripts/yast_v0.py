# deleted code

# this function should rebuild a nominal phrase into a nominal predication
# 'ich warte auf den Vater' -> 'ich warte darauf, dass ich Vater bin'.
# however: it has to be referred to separtely to add new elements to the clause
# e.g. to add adverbials, it has to be referenced separately.
# so there is no difference to first adding 'PRÄDIKATIV' and then add the predicate...

# too complex, does not work properly

def Finit(node, auxiliary = 'sein'):
  # for attributive/adverbial phrases, go up one level
  if node.getparent().tag in ['ADVERBIALE', 'ATTRIBUT']:
    node = node.getparent()
  # when node is adverbial: assume there is no predication yet
  if node.tag == 'ADVERBIALE':
    clause = node.getparent()
    predicate = Prädikativ(clause, auxiliary)
    clause.replace(predicate, node)
    node.tag = 'PRÄDIKATIV'
  # when node is attribut: make relative clause
  elif node.tag == 'ATTRIBUT':
    phrase = node.getparent()
    clause = Relativsatz(phrase)
    predicate = Prädikativ(clause, auxiliary)
    subject = Phrase(clause, 'Subjekt')
    Relator(subject)
    clause.replace(predicate, node)
    node.tag = 'PRÄDIKATIV'
    # get stem of adjective instead of inflected form
    adjective = node.find('ADJEKTIV')
    if adjective is not None:
      adjective.text = node.get('stem')
  # argument in all other cases: make Komplementsatz
  else:
    phrase = deepcopy(node)
    argument = node
    # go up to argument node
    while argument.tag != 'ARGUMENT':
      argument = argument.getparent()
    # delete phrase and junktor, to be inserted in new Komplementsatz
    ET.strip_elements(node.getparent(), '*')
    # make new Komplementsatz
    clause = Komplementsatz(argument.getparent(), argument.get('role'))
    predicate = Prädikativ(clause, auxiliary)
    clause.replace(predicate, phrase)
    phrase.tag = 'PRÄDIKATIV'
  return clause


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


def Adjektiv_alt(addto, adjective):
  # ======
  # in a coordination
  # ======
  if addto.tag == 'KOORDINATION':
    coordination = addto
    parent = addto.getparent()
    # Adjektiv Prädikat
    if parent.tag == 'PRÄDIKATIV':
      node = ET.SubElement(coordination, "PRÄDIKATIV")
      ET.SubElement(node, "ADJEKTIV").text = adjective
    # Adjektiv Adverbiale
    elif parent.tag == 'SATZ':
      # prepare new adverbial node
      node = ET.SubElement(coordination, "ADVERBIALE")
      ET.SubElement(node, "ADJEKTIV").text = adjective
    # Adjektiv Attribut
    elif parent.tag == 'PHRASE':
      # get agreement features
      case = parent.get('case')
      gender = parent.get('gender')
      declension = parent.get('declension')
      adjectiveAgree = adjective + Adjektivflexion[declension][case][gender]
      # prepare new attributive node
      node = ET.SubElement(coordination, 'ATTRIBUT')
      ET.SubElement(node, 'ADJEKTIV').text = adjectiveAgree
  # ======
  # not in a coordination
  # ======
  else:
    # Adverb Prädikat
    if addto.tag == 'PRÄDIKATIV':
      node = ET.Element("ADVERBIALE")
      ET.SubElement(node, "ADJEKTIV").text = adjective
      addto.append(node)
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
      adjectiveAgree = adjective + Adjektivflexion[declension][case][gender]
      # check if referent is absent, then adjective becomes head
      if addto.find('REFERENT').text is None:
        adjectiveAgree = adjectiveAgree.capitalize()
        node = ET.Element('REFERENT')
      # prepare new attributive node
      else:
        node = ET.Element('ATTRIBUT', attrib = {'stem': adjective})
      ET.SubElement(node, 'ADJEKTIV').text = adjectiveAgree
      # insert after determiner
      addto.insert(1, node)
  # return for Gradpartikel
  return node



def Koordination(addto, conjunction = 'und'):
  # prepare koordination node
  node = ET.Element('KOORDINATION')
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
    # coordination of clauses when not yet predicated
    if addto.find('PRÄDIKAT') is None:
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
  elif addto.tag == 'PRÄDIKATIV':
    addto.append(node)
  return node
 

 def Phrase(addto, connection = None):
  parent = addto.getparent()
  if parent is not None:
    grandparent = parent.getparent()
  # ======
  # argument phrase
  # ======
  node = addto.find(f'*[@role="{connection}"]')
  if node is not None:
    # Check for already filled predicative
    # which happens with lexicalised constructions 'Angst haben'
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
      if juncture in ['an', 'in', 'auf', 'über']:
        case = 'Akkusativ'
      ET.SubElement(leaf, 'JUNKTOR').text = juncture
    phrase = ET.SubElement(leaf, 'PHRASE', attrib = {'case': case})
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
      insert = addto.find('break')
      if insert is not None:
        insertafter = addto.find('break')
        place = list(addto).index(insertafter) + 1
        addto.insert(place, node)
      else:
        addto.append(node)
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

 #or (addto.tag == 'KOORDINATION' and grandparent.tag == 'PHRASE'):
 #   # when in coordination, move coordination to behind referent
 #   if addto.tag == 'KOORDINATION':
 #     if len(addto.findall('*')) ==  1:
 #       referent = grandparent.find('REFERENT')
 #       place = list(grandparent).index(referent) + 1
 #       grandparent.insert(place, parent)

  elif addto.tag == 'PHRASE' or addto.getparent().tag == 'PHRASE':
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
  # Coordination of roles
  # ======
  elif addto.tag == 'KOORDINATION':
    # simply add attribute to end of the phrase
    case = parent.get('case')
    phrase = ET.SubElement(addto, 'PHRASE', attrib = {'case': case})
    # set phrase to plural in case it is subject
    parent.set('person', '3')
    parent.set('gender', 'Plural')
  # ======
  # For relators: add info to all phrases
  relative = addto.get('relative')
  kind = addto.get('kind')
  if relative is not None:
    phrase.set('relative', relative)
  #if kind is not None:
  #  phrase.set('kind', kind)
  # ======
  return phrase