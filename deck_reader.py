import xml.etree.ElementTree as ET
import json
import sqlite3
import datetime

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
deck = root[1]

#@TODO Cache with Redis to avoid unnecessary queries

"""
for card in deck:
    print card.text, cards[card.text]
    exit()
"""

c.execute("DROP TABLE IF EXISTS netrunner_deck_cards")
"""
c.execute('''CREATE TABLE IF NOT EXISTS netrunner_decks (
            deck_id integer primary key autoincrement, 
             integer, 
            last_update text, 
            creation_date text,
            user integer''')
"""
c.execute('''CREATE TABLE IF NOT EXISTS netrunner_deck_cards (
            deck_card_id integer primary key autoincrement, 
            deck_id integer, 
            card_id integer, 
            card_name text, 
            quantity integer, 
            date text, 
            user integer, 
            FOREIGN KEY(card_id) REFERENCES netrunner(card_id))''')

for card in deck:
    full_card = cards[card.text]
    card_id = full_card[constants.CARD_ID]
    print card_id
    card_name = full_card[constants.NAME]
    card_quantity = card.attrib['qty']
    now = str(datetime.datetime.now())
    c.execute('''INSERT INTO netrunner_deck_cards
            VALUES (?,?,?,?,?,?,?)''', (None, 1, card_id, card_name, card_quantity, now, 11))

print '-'*20
print len(c.execute('''SELECT * FROM netrunner''').fetchall())
print len(c.execute('''SELECT * FROM netrunner_deck_cards''').fetchall())
print c.execute('''SELECT card_name, quantity FROM netrunner_deck_cards as dc INNER JOIN netrunner AS n ON dc.card_id=n.card_id''').fetchall()

connection.close()
exit()


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
