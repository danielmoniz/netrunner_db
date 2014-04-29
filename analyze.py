import netrunner_constants as constants

def total_deck_cost(deck, cards):
    cost = 0
    total_cost = 0
    return_costs = []
    for card in deck.cards:
        card_name = card['name']
        full_card = cards[card_name]
        card_cost = int(full_card[constants.COST])
        card_total_cost = int(full_card[constants.TOTALCOST])
        cost += card_cost
        total_cost += card_total_cost
        return_costs.append("{}: ({}, {})".format(card_name, card_cost, card_total_cost))
    return return_costs
    return cost, total_cost

