import netrunner_constants as constants

def total_deck_cost(deck, cards):
    cost = 0
    total_cost = 0
    for card in deck.cards:
        card_name = card['name']
        if "Hadrian" in card_name:
            print card
        full_card = cards[card_name]
        cost += int(full_card[constants.COST])
        total_cost += int(full_card[constants.TOTALCOST])
    return cost, total_cost

