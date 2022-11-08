import xml.etree.ElementTree as ET

class Syntax(ET.Element):
  def __init__(self):
    super().__init__('SATZ')

  def Phrase(self, text):
    ET.SubElement(self, 'WITHOUT CHILDREN').text = text
    return(self)
  
  # trying to get hierarchy with class methods
  def Sub(self, text):
    node = ET.SubElement(self, 'WITH CHILDREN')
    node.text = text
    return node
  
beispiel = Syntax()
a = beispiel.Phrase('hallo').Sub('Welt')

# However: the following doesn't work: 
# 'Kontinent' should be a subnode of 'Welt'

# a.Phrase('Kontinent')

# The problem is that ET.SubElement is a function
# and the result of this function does not inherit to the new class
# obvious type changes do not work either

# a.__class__ = Syntax

ET.indent(beispiel)
ET.dump(beispiel)
