import data

def run_analyses(deck, name_of_analysis=""):
    analyses = []
    neutral_analysis_ftns = [
        total_deck_cost,
    ]
    corp_analysis_ftns = [
        total_cost_of_ice,
        number_of_agenda_points,
    ]
    runner_analysis_ftns = [
        total_cost_of_icebreakers,
        total_cost_of_unique_icebreakers,
        mean_cost_of_icebreakers,
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
    return ("Total cost of ice", total_cost)

def total_cost_of_icebreakers(deck):
    icebreakers = data.get_cards_of_attr("subtype", "icebreaker", deck)
    total_cost = data.sum_over_attr("cost", icebreakers, convert_type=int)
    return ("Total cost of icebreakers", total_cost)

def total_cost_of_unique_icebreakers(deck):
    icebreakers = data.get_cards_of_attr("subtype", "icebreaker", deck)
    total_cost = data.sum_over_attr("cost", icebreakers, convert_type=int, unique=True)
    return ("Total cost of unique icebreakers", total_cost)

def mean_cost_of_icebreakers(deck):
    icebreakers = data.get_cards_of_attr("subtype", "icebreaker", deck)
    mean = data.average_over_attr("cost", icebreakers)
    return ("Mean cost of icebreakers", mean)

def number_of_agenda_points(deck):
    agendas = data.get_cards_of_attr("type", "agenda", deck)
    total = data.sum_over_attr("agendapoints", agendas)
    return ("Number of agenda points", total)

def average_agenda_points_scored_to_win(deck):
    pass

def total_deck_cost(deck):
    return ("Total cost of deck", data.sum_over_attr("cost", deck, convert_type=int))

