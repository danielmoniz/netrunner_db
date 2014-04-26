import xml.etree.ElementTree as ET
tree = ET.parse('weyland.xml')
root = tree.getroot()

print "="*10
identity = root[0][0]
print "Identity: {}".format(identity.text)
print ""

deck = root[1]
for card in deck:
    print "{} (x{})".format(card.text, card.attrib['qty'])

print "="*10
