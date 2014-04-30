import netrunner_constants as constants

def run_analyses(deck):
    analyses = []
    analysis_ftns = [
        total_deck_cost,
    ]
    for ftn in analysis_ftns:
        analyses.append(ftn(deck))
    return analyses

def total_deck_cost(deck):
    cost = 0
    total_cost = 0
    return_costs = []
    return_costs.append("Deck Cost (cost, total_cost)")
    for card in deck.cards:
        card_name = card.name
        card_cost = int(card.cost)
        card_total_cost = int(card.totalcost)
        cost += card_cost
        total_cost += card_total_cost
        return_costs.append("{}: ({}, {})".format(card_name, card_cost, card_total_cost))
    return return_costs
    return cost, total_cost

