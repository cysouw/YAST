
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
  