

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