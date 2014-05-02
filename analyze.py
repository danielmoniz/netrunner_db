import data


def get_general_analysis_ftns():
    general_analysis_ftns = [
        total,
        total_as_ratio,
        total_cost,
        mean_cost,
        max_cost,
    ]
    return general_analysis_ftns

def get_general_analysis_ftn_names():
    general_analysis_ftn_names = [ftn.__name__.capitalize() for ftn in get_general_analysis_ftns()]
    return general_analysis_ftn_names

def get_ice_analysis_ftns():
    ice_analysis_ftns = [
        total,
        total_cost,
        mean_strength,
        max_strength,
        cost_to_strength_ratio,
    ]
    return ice_analysis_ftns

def get_ice_analysis_ftn_names():
    ice_analysis_ftn_names = [ftn.__name__.capitalize() for ftn in get_ice_analysis_ftns()]
    return ice_analysis_ftn_names

def run_analyses(deck, side=None, name_of_analysis=""):
    analyses = []


    analysis_ftns = get_general_analysis_ftns()
    """
    if side == 'corp':
        analysis_ftns.extend(corp_analysis_ftns)
    elif side == 'runner':
        analysis_ftns.extend(runner_analysis_ftns)
    """

    for ftn in analysis_ftns:
        analyses.append(ftn(deck))
    return analyses

def total(cards):
    """Note that 'unique' is set to true for summing the 'quantity' attribute.
    If it wasn't, cards would be double- and triple-counted.
    """
    return data.sum_over_attr('quantity', cards, unique=True, convert_type=int)

def total_as_ratio(cards):
    return 'TBC'

def total_cost(cards):
    total_cost = data.sum_over_attr("cost", cards, convert_type=int)
    return total_cost

def mean_cost(cards):
    mean = data.average_over_attr("cost", cards)
    return mean

def max_cost(cards):
    costs = data.get_list_of_attr("cost", cards, convert_type=int)
    if not costs:
        return '/'
    return max(costs)

# ICE analysis functions

def mean_strength(cards):
    mean = data.average_over_attr("strength", cards)
    return mean

def max_strength(cards):
    strengths = data.get_list_of_attr("strength", cards, convert_type=int)
    return max(strengths)

def cost_to_strength_ratio(cards):
    return 'TBC'

def total_cost_of_icebreakers(deck):
    pass

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

