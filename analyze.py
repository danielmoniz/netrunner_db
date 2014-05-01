import data

def run_analyses(deck):
    analyses = []
    neutral_analysis_ftns = [
        total_deck_cost,
    ]
    corp_analysis_ftns = [
        total_cost_of_ice,
    ]
    runner_analysis_ftns = [
        total_cost_of_icebreakers,
        total_cost_of_unique_icebreakers,
    ]

    analysis_ftns = neutral_analysis_ftns
    if deck.side.lower() == 'corp':
        analysis_ftns.extend(corp_analysis_ftns)
    elif deck.side.lower() == 'runner':
        analysis_ftns.extend(runner_analysis_ftns)

    for ftn in analysis_ftns:
        analyses.append(ftn(deck))
    return analyses

def total_cost_of_ice(deck):
    ice = data.get_cards_of_attr("type", "ice", deck)
    total_cost = data.sum_over_attr("cost", ice, int)
    return ("total cost of ice", total_cost)

def total_cost_of_icebreakers(deck):
    icebreakers = data.get_cards_of_attr("subtype", "icebreaker", deck)
    print len(icebreakers)
    total_cost = data.sum_over_attr("cost", icebreakers, convert_type=int)
    return ("total cost of icebreakers", total_cost)

def total_cost_of_unique_icebreakers(deck):
    icebreakers = data.get_cards_of_attr("subtype", "icebreaker", deck)
    total_cost = data.sum_over_attr("cost", icebreakers, convert_type=int, unique=True)
    return ("total cost of unique icebreakers", total_cost)

def total_deck_cost(deck):
    cost = 0
    total_cost = 0
    return_costs = []
    return_costs.append("Deck Cost (cost, total_cost)")
    for card in deck:
        card_name = card.name
        card_cost = int(card.cost)
        card_total_cost = int(card.totalcost)
        cost += card_cost
        total_cost += card_total_cost
        return_costs.append("{}: ({}, {})".format(card_name, card_cost, card_total_cost))
    return return_costs
    return cost, total_cost

