import xml.etree.ElementTree as ET
import json

import bs4

tree = ET.parse('weyland.xml')
root = tree.getroot()

print "="*10
identity = root[0][0]
print "Identity: {}".format(identity.text)
print ""

with open('corp_cards_test.json') as f:
    corp_cards = json.loads(f.read())

with open('runner_cards_test.json') as f:
    runner_cards = json.loads(f.read())


all_cards = [corp_cards, runner_cards]

deck = root[1]
for card in deck:
    card_type = all_cards[0][card.text]['type']
    print "{} (x{}), type: {}".format(card.text, card.attrib['qty'], card_type)

print "="*10
print ""

d = {
    "identity": {
        "name": "test identity",
    },
    "deck": [
        {
            "name": "card1",
            "qty": 2,
        },
    ]
}
