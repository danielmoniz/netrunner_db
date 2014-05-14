import json
import sqlite3
import datetime

import redis
import bs4

import card as card_module

deck_filename = "weyland.txt"


def get_all_cards():
    """Return a list of every card in the card pool."""
    NETRUNNER_CARD_LIST = 'netrunner:cards:all'
    redis_instance = redis.StrictRedis(host="localhost", port=6379, db=0)
    redis_cards = redis_instance.get(NETRUNNER_CARD_LIST)
    redis_cards = False
    if redis_cards:
        cards = json.loads(redis_cards)
    else:
        connection = sqlite3.connect("/Users/daniel.moniz/dev/projects/personal/netrunner_database/cards.db")
        c = connection.cursor()
        query = c.execute("SELECT * FROM netrunner")
        cards = query.fetchall()
        connection.close()

        real_cards = []
        for card in cards:
            real_card = card_module.DetailedCard(card)
            real_cards.append(real_card)

        cards = clean_card_data(real_cards)
        json_dump_list = []
        for card in cards:
            json_dump_list.append(card.__dict__)
        json_dump = json.dumps(json_dump_list)
        redis_instance.set(NETRUNNER_CARD_LIST, json_dump)
    return cards


def get_card_map_of_all_cards(lower=False):
    """Return a map of every Netrunner card in the database.
    Retrieve from redis cache if possible.
    """
    cards = get_all_cards()

    cards_map = reformat_cards(cards, lower)

    # Add duplicate Indentity entries with short versions of names
    for card in cards:
        if card.type.lower() == "identity" and card.side.lower() == 'runner':
            if ':' not in card.name:
                continue
            new_card_name = card.name[:card.name.index(':')]
            if lower:
                new_card_name = new_card_name.lower()
            new_card = card_module.DetailedCard(card)
            cards_map[new_card_name] = new_card.__dict__

    return cards_map


def clean_card_data(cards):
    attrs_to_clean = ["name"]
    for card in cards:
        for attr in attrs_to_clean:
            attr_value = getattr(card, attr)
            if not isinstance(attr_value, basestring):
                continue
            clean_attr = str(bs4.BeautifulSoup(attr_value))
            setattr(card, attr, clean_attr)

    return cards


def find_flaws(deck, all_cards):
    side = deck.side.lower()
    flaws_map = {"corp": find_corp_flaws, "runner": find_runner_flaws}
    return flaws_map[side.lower()](deck, all_cards)

def find_corp_flaws(deck, all_cards):
    flaws = []
    cat_deck = deck.cat_cards
    ice = get_category_from_cat_deck('ICE', cat_deck)
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


def reformat_cards(card_list, lower=False):
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
            card_name = str(bs4.BeautifulSoup(card.name))
            if lower:
                card_name = card_name.lower()
            card_dict[card_name] = card.__dict__
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
