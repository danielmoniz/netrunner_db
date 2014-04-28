import re
import xml.etree.ElementTree as ET
import json
import sqlite3
import datetime

import bs4

import netrunner_constants as constants

deck_filename = "weyland.txt"

def read_card_from_line(line, full_card_list):
    quantity = 1
    match = re.search(' x\d', line)
    if match:
        quantity = int(line[match.start() + 2:match.end()])
        line = line[:match.start()].rstrip()

    match = re.search('\(', line)
    if match:
        line = line[:match.start()].rstrip()
    card_name = line
    try:
        full_card_list[card_name]
    except KeyError:
        return False
    return card_name, quantity

    """
    try:
        pattern = re.compile('(')
        match = re.search('(', line)
        stop1 = line.index('(')
    except ValueError:
        pass
    try:
        match = re.search(' x\d')
        if match:
            stop = match.start()
    """

def get_deck_from_xml(deck_filename, cards):
    tree = ET.parse('weyland.xml')
    root = tree.getroot()
    deck_xml = root[1]
    deck = {}
    deck['identity'] = root[0][0]
    deck['main'] = []
    for card in deck_xml:
        card_name = card.text
        full_card = cards[card_name]
        card_type = full_card[constants.TYPE]
        card_data = {
            'name': card_name,
            'qty': card.attrib['qty'],
            'type': card_type,
        }
        deck['main'].append(card_data)
    return deck

def get_deck_from_text(deck_text, cards):
    deck = {"identity": None, "main": []}
    deck_info = deck_text.split('\n')
    for line in deck_info:
        card_info = read_card_from_line(line, cards)
        if not card_info:
            continue
        card_name, quantity = card_info
        full_card = cards[card_name]
        card_type = full_card[constants.TYPE]

        if full_card[constants.TYPE].lower() == 'identity':
            if quantity > 1:
                print "Cannot have more than one identity."
                exit()
            deck['identity'] = card_name
            continue
        card_data = {
            'name': card_name,
            'qty': quantity,
            'type': card_type,
        }
        deck['main'].append(card_data)
    """
    if not deck['identity']:
        print "Deck must have an identity card."
        return False
    """
    return deck



def more_to_be_reformatted():
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

#cards = reformat_cards(cards)


def get_deck_from_input(deck_data):
    if deck_filename.endswith(".xml"):
        deck = get_deck_from_xml(deck_filename, cards)
    elif deck_filename.endswith(".txt") or deck_filename.endswith(".text"):
        deck = get_deck_from_text(deck_filename, cards)
    else:
        print "Cannot read this deck format."
        return False
    return deck

def print_deck(deck):
    deck_output = {'output': ""}
    #add_line = lambda x: deck_output += x + "\n"
    def add_line(text=""):
        deck_output['output'] += text + "\n"
    add_line('-'*12)
    add_line("Identity:")
    add_line(deck['identity'])
    add_line()
    for card in deck['main']:
        add_line("{} x{}".format(card['name'], card['qty']))

    print deck_output['output']
    return deck_output['output']

def categorize_deck(deck):
    cat_deck = deck.copy()
    cat_deck['main'] = {}
    for card in deck['main']:
        card_type = card['type']
        try:
            cat_deck['main'][card_type].append(card)
        except KeyError:
            cat_deck['main'][card_type] = []
            cat_deck['main'][card_type].append(card)
    return cat_deck

"""
def print_deck_advanced(deck):
    deck_output = {'output': ""}
    #add_line = lambda x: deck_output += x + "\n"
    def add_line(text=""):
        deck_output['output'] += text + "\n"
    add_line('-'*12)
    add_line("Identity:")
    add_line(deck['identity'])
    add_line()
    for category, subdeck in deck['main'].iteritems():
        add_line(category.upper())
        for card in deck['main']:
            add_line("{} x{}".format(card['name'], card['qty']))
        add_line()

    print deck_output['output']
    return deck_output['output']
"""

#cat_deck = categorize_deck(deck)
#print_deck(deck)

def to_be_converted():
    print "="*10
    identity = deck['identity']
    print "Identity: {}".format(identity.text)
    print ""



#@TODO Cache with Redis to avoid unnecessary queries

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

    for card in deck['main']:
        full_card = cards[card['name']]
        card_id = full_card[constants.CARD_ID]
        card_name = card['name']
        card_quantity = card['qty']
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
