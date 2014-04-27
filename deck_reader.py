import xml.etree.ElementTree as ET
import json
import sqlite3

import bs4

import netrunner_constants as constants

tree = ET.parse('weyland.xml')
root = tree.getroot()

print "="*10
identity = root[0][0]
print "Identity: {}".format(identity.text)
print ""

connection = sqlite3.connect("cards.db")
c = connection.cursor()
query = c.execute("SELECT * FROM netrunner")
cards = query.fetchall()

def reformat_cards(card_list):
    """Change list of cards into a desirable data structure.
    """
    card_dict = {}
    for card in card_list:
        card_name = str(bs4.BeautifulSoup(card[constants.NAME]))
        card_dict[card_name] = card
    return card_dict

cards = reformat_cards(cards)

#@TODO Cache with Redis to avoid unnecessary queries

connection.close()


deck = root[1]
for card in deck:
    full_card = cards[card.text]
    card_type = full_card[constants.TYPE]
    print "{} (x{}), type: {}".format(card.text, card.attrib['qty'], card_type)

print "="*10
print ""

for card in deck:
    full_card = cards[card.text]
    card_type = full_card[constants.TYPE]
    card_subtype = full_card[constants.SUBTYPE]
