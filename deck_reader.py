import re
import xml.etree.ElementTree as ET
import json
import sqlite3
import datetime

import redis
import bs4

import netrunner_constants as constants

deck_filename = "weyland.txt"

def read_card_from_line(line, full_card_map):
    quantity = 1
    line = str(bs4.BeautifulSoup(line))
    match = re.search(' x\d', line)
    if match:
        quantity = int(line[match.start() + 2:match.end()])
        line = line[:match.start()].rstrip()

    match = re.search('\(', line)
    if match:
        line = line[:match.start()].rstrip()
    card_name = line.strip()
    try:
        full_card_map[card_name]
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

def get_deck_from_text(deck_text, full_card_map):
    """Parse a text file for cards that make up a deck.
    @TODO Allow for multiple cards of the same name to be written, 
    without causing issues.
    ->  Eg. if 'Snare!' is written twice, it should either count as one or two 
        Snares, but not two Snare entries.
    """
    deck_cards = []
    for key, value in full_card_map.iteritems():
        print key
        print value[constants.NAME]
    print "@"*20
    identity = None
    deck_info = deck_text.split('\n')
    for line in deck_info:
        card_info = read_card_from_line(line, full_card_map)
        if not card_info:
            print "Skipping line"
            continue
        card_name, quantity = card_info
        if "Hadrian" in card_name:
            print repr(card_name)
            print '*'*10
        full_card = full_card_map[card_name]
        card_name = full_card[constants.NAME] # replace name w/ official name
        if "Hadrian" in card_name:
            print repr(card_name)
            print '='*10
        card_type = full_card[constants.TYPE]

        if full_card[constants.TYPE].lower() == 'identity':
            if quantity > 1:
                print "Cannot have more than one identity."
                return False
            identity = card_name
            continue
        card_data = {
            'name': card_name,
            'qty': quantity,
            'type': card_type,
        }
        deck_cards.append(card_data)

    import deck as deck_struct
    deck_obj = deck_struct.Deck(deck_cards, identity)
    return deck_obj


def get_all_cards():
    """Return a list of every Netrunner card in the database.
    Retrieve from redis cache if possible.
    """
    NETRUNNER_CARD_LIST = 'netrunner:cards:all'
    redis_instance = redis.StrictRedis(host="localhost", port=6379, db=0)
    redis_cards = redis_instance.get(NETRUNNER_CARD_LIST)
    redis_cards = False
    if redis_cards:
        cards = json.loads(redis_cards)
    else:
        connection = sqlite3.connect("cards.db")
        c = connection.cursor()
        query = c.execute("SELECT * FROM netrunner")
        cards = query.fetchall()
        connection.close()

        print "PRINTING CARD"
        print len(cards[0])
        for card in cards:
            if len(card) != 30:
                print len(card)
        cards = clean_card_data(cards)
        redis_instance.set(NETRUNNER_CARD_LIST, json.dumps(cards))

    cards_map = reformat_cards(cards)

    # Add duplicate Indentity entries with short versions of names
    for card in cards:
        side = card[constants.NAME][constants.SIDE].lower()
        if card[constants.TYPE].lower() == "identity" and side == 'runner':
            card_name = card[constants.NAME]
            new_card_name = card_name[:card_name.index(':')]
            cards_map[new_card_name] = card
    
    return cards_map


def clean_card_data(cards):
    attrs_to_clean = [constants.NAME]
    cleaned_cards = []
    for card in cards:
        new_card = list(card)
        for attr in attrs_to_clean:
            if not isinstance(card[attr], basestring):
                continue
            clean_attr = str(bs4.BeautifulSoup(card[attr]))
            new_card[attr] = clean_attr
        cleaned_cards.append(tuple(new_card))
    return cleaned_cards


def find_flaws(deck, all_cards):
    print deck.identity
    print all_cards[deck.identity]
    side = all_cards[deck.identity][constants.SIDE]
    flaws_map = {"corp": find_corp_flaws, "runner": find_runner_flaws}
    return flaws_map[side.lower()](deck, all_cards)

def find_corp_flaws(deck, all_cards):
    flaws = []
    cat_deck = deck.cat_cards
    ice = get_category_from_cat_deck('ice', cat_deck)
    if len(ice) == 0:
        flaws.append("No ice!")
    return flaws

def find_runner_flaws(deck, all_cards):
    flaws = []
    cat_deck = deck.cat_cards
    icebreakers = get_category_from_cat_deck('Program', cat_deck)
    if len(icebreakers) == 0:
        flaws.append("No programs!!")
    return flaws

def get_category_from_cat_deck(category, deck):
    try:
        subdeck = deck[category]
    except KeyError:
        subdeck = []
    return subdeck


def reformat_cards(card_list):
    """Change list of cards into a desirable data structure.
    """
    NETRUNNER_CARD_MAP = 'netrunner:cards:all:map'
    redis_instance = redis.StrictRedis(host="localhost", port=6379, db=0)
    redis_cards = redis_instance.get(NETRUNNER_CARD_MAP)
    redis_cards = False
    if redis_cards:
        return json.loads(redis_cards)
    else:
        card_dict = {}
        for card in card_list:
            card_name = str(bs4.BeautifulSoup(card[constants.NAME]))
            card_dict[card_name] = card
        redis_instance.set(NETRUNNER_CARD_MAP, json.dumps(card_dict))
    return card_dict


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
            cat_deck['main'][card_type]['cards'].append(card)
            cat_deck['main'][card_type]['total'] += card['qty']
        except KeyError:
            cat_deck['main'][card_type] = {
                "total": card['qty'],
                "cards": [],
                }
            cat_deck['main'][card_type]['cards'].append(card)
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

def to_be_converted():
    print "="*10
    identity = deck['identity']
    print "Identity: {}".format(identity.text)
    print ""



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
