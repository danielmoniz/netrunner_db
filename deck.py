import netrunner_constants as constants

class Deck(object):

    def __init__(self, cards, identity, side, card_map=None):
        self.identity = identity
        self.cards = cards
        self.cat_cards = self.categorize_cards()
        self.card_map = None
        self.side = side
        if card_map:
            self.card_map = card_map

    def __getitem__(self, index):
        return self.cards[index]

    def categorize_cards(self):
        cat_deck = {}
        for card in self.cards:
            card_type = card['type']
            try:
                cat_deck[card_type]['cards'].append(card)
                cat_deck[card_type]['total'] += card['qty']
            except KeyError:
                cat_deck[card_type] = {
                    "total": card['qty'],
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
