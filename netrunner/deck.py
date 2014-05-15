import random
import re
import xml.etree.ElementTree as ET

import bs4

import card as card_module
import data

class Deck(object):

    def __init__(self, cards, identity = None, full_card_map_lower=None, shortlist=None):
        if not shortlist:
            shortlist = []
        self.identity = identity
        self.card_map = full_card_map_lower
        if not full_card_map_lower:
            self.card_map = deck_reader.get_card_map_of_all_cards()

        self.cards = []
        for card in cards:
            card_name = card['name'].lower()
            detailed_card = card_module.DetailedCard(self.card_map[card_name])
            detailed_card.quantity = card['qty']
            self.cards.append(detailed_card)
        self.shortlist = []
        for card_name in shortlist:
            card_name = card_name.lower()
            detailed_card = card_module.DetailedCard(self.card_map[card_name])
            self.shortlist.append(detailed_card)

        self.cat_cards = self.categorize_cards()

        if identity:
            identity_card = self.card_map[identity.lower()]
            self.identity = card_module.DetailedCard(identity_card)
            self.side = identity_card["side"]
            self.faction = identity_card['identity']
        else:
            if not cards:
                return None
            self.side = self.cards[0].side

        sum_list = [card.quantity for card in self.cards]
        self.total_cards = sum(sum_list)
        self.total_unique_cards = len(self.cards)

        #self.shuffle = self._shuffle()

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __str__(self):
        return_str = ""
        if self.identity:
            return_str += "{}\n\n".format(self.identity)
        for subdeck_type, subdeck in self.cat_cards.iteritems():
            return_str += "{} ({} total, {} unique)\n".format(subdeck_type, subdeck['total'], len(subdeck))
            for card in subdeck['cards']:
                return_str += unicode(card) + "\n"
            return_str += "\n"
        return_str += "\nShortlist ({})\n".format(len(self.shortlist))
        for card in self.shortlist:
            return_str += unicode(card) + "\n"
        return_str = unicode(return_str)
        print return_str
        return return_str

    def __len__(self):
        return len(self.cards)

    @property
    def shuffle(self):
        card_list = []
        for card in self:
            try:
                quantity = card.quantity
            except AttributeError:
                quantity = 1
            for i in range(quantity):
                card_list.append(card)
        random.shuffle(card_list)
        return card_list

    @classmethod
    def build_deck_from_text(cls, deck_text, full_card_map_lower):
        """Parse a text file for cards that make up a deck.
        @TODO Allow for multiple cards of the same name to be written, 
        without causing issues.
        ->  Eg. if 'Snare!' is written twice, it should either count as one or two 
            Snares, but not two Snare entries.
        """
        valid_cards = {}
        deck_cards = []
        shortlist = []
        identity = None
        deck_info = deck_text.split('\n')
        mode = None
        for line in deck_info:
            line = unicode(bs4.BeautifulSoup(line)).lower()
            if "shortlist" in line or "short list" in line:
                mode = "shortlist"
            card_info = cls.read_card_from_line(line, full_card_map_lower)
            if not card_info:
                continue
            card_name, quantity = card_info
            if mode == "shortlist":
                shortlist.append(card_name)
            else:
                try:
                    valid_cards[card_name] += int(quantity)
                except KeyError:
                    valid_cards[card_name] = int(quantity)
        for card_name, quantity in valid_cards.iteritems():
            full_card = full_card_map_lower[card_name.lower()]
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

        deck_obj = Deck(deck_cards, identity, full_card_map_lower, shortlist=shortlist)
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
    def read_card_from_line(cls, line, full_card_map_lower):
        quantity = 1
        line = unicode(bs4.BeautifulSoup(line)).lower()
        match = re.search(' x\d', line)
        if match:
            quantity = int(line[match.start() + 2:match.end()])
            line = line[:match.start()].rstrip()

        match = re.search('\(', line)
        if match:
            line = line[:match.start()].rstrip()
        card_name = line.strip()
        try:
            full_card_map_lower[card_name.lower()]
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
