import re
import xml.etree.ElementTree as ET

import bs4

import netrunner_constants as constants
import card as card_module
import data

class Deck(object):

    def __init__(self, cards, identity, full_card_map=None):
        self.identity = identity
        self.card_map = full_card_map
        if not full_card_map:
            self.card_map = deck_reader.get_card_map_of_all_cards()

        self.cards = []
        for card in cards:
            card_name = card['name']
            detailed_card = card_module.DetailedCard(self.card_map[card_name])
            detailed_card.quantity = card['qty']
            self.cards.append(detailed_card)

        self.cat_cards = self.categorize_cards()

        identity_card = self.card_map[identity]
        self.side = identity_card["side"]

        sum_list = [card.quantity for card in self.cards]
        self.total_cards = sum(sum_list)
        self.total_unique_cards = len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __str__(self):
        return_str = ""
        for card in self.cards:
            return_str += str(card) + "\n"
        return return_str

    @classmethod
    def build_deck_from_text(cls, deck_text, full_card_map):
        """Parse a text file for cards that make up a deck.
        @TODO Allow for multiple cards of the same name to be written, 
        without causing issues.
        ->  Eg. if 'Snare!' is written twice, it should either count as one or two 
            Snares, but not two Snare entries.
        """
        deck_cards = []
        identity = None
        deck_info = deck_text.split('\n')
        for line in deck_info:
            card_info = cls.read_card_from_line(line, full_card_map)
            if not card_info:
                continue
            card_name, quantity = card_info
            full_card = full_card_map[card_name]
            if 'Noise' in card_name:
                print full_card
                print '%'*10
            card_name = full_card['name'] # replace name w/ official name
            card_type = full_card['type']

            if full_card["type"].lower() == 'identity':
                if quantity > 1:
                    print "Cannot have more than one identity."
                    return False
                identity = full_card['name']
                continue
            card_data = {
                'name': card_name,
                'qty': quantity,
                'type': card_type,
            }
            deck_cards.append(card_data)

        if not identity:
            return False
        deck_obj = Deck(deck_cards, identity, full_card_map)
        return deck_obj

    def categorize_cards(self):
        cat_deck = {}
        for card in self.cards:
            card_type = card.type
            try:
                cat_deck[card_type]['cards'].append(card)
                cat_deck[card_type]['total'] += card.quantity
            except KeyError:
                cat_deck[card_type] = {
                    "total": card.quantity,
                    "cards": [],
                    }
                cat_deck[card_type]['cards'].append(card)
        return cat_deck

    def get_category_from_cat_deck(self, category):
        try:
            subdeck = self.cards[category]
        except KeyError:
            subdeck = []
        return subdeck

    @classmethod
    def read_card_from_line(cls, line, full_card_map):
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

    def print_deck(self, deck):
        deck_output = {'output': ""}
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


    """
    def get_deck_from_xml(self, deck_filename, cards):
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
    """
