import data

def run_analysis_ftns(analysis_ftns, cards, **kwargs):
    analyses = []

    for ftn in analysis_ftns:
        if not len(cards):
            analyses.append('/')
            continue
        analyses.append(ftn(cards, **kwargs))
    return analyses

def run_general_analyses(cards, **kwargs):
    analysis_ftns = get_general_analysis_ftns()
    return run_analysis_ftns(analysis_ftns, cards, **kwargs)

def run_special_analyses(cards, side, **kwargs):
    analyses = []
    analysis_ftns = []
    if side.lower() == 'corp':
        analysis_ftns.extend(get_ice_analysis_ftns())
    elif side.lower() == 'runner':
        analysis_ftns.extend(get_icebreaker_analysis_ftns())

    analysis_ftns = get_general_analysis_ftns()
    return run_analysis_ftns(analysis_ftns, cards, **kwargs)

def get_general_analysis_ftns():
    general_analysis_ftns = [
        total,
        total_as_ratio,
        total_cost,
        total_cost_without_duplicates,
        mean_cost,
        max_cost,
    ]
    return general_analysis_ftns

def get_ice_analysis_ftns():
    ice_analysis_ftns = [
        total,
        total_cost,
        total_cost_without_duplicates,
        mean_strength,
        max_strength,
        mean_cost_to_strength_ratio,
        mean_cost_to_strength_ratio_without_duplicates,
    ]
    return ice_analysis_ftns

def get_icebreaker_analysis_ftns():
    analysis_ftns = [
        total,
        total_cost,
        total_cost_without_duplicates,
        mean_strength,
        max_strength,
        mean_cost_to_strength_ratio,
        mean_cost_to_strength_ratio_without_duplicates,
    ]
    return analysis_ftns

# ANALYSIS FUNCTIONS

def total(cards, **kwargs):
    return data.total_cards_in_list(cards)

def total_as_ratio(cards, **kwargs):
    deck = kwargs['full_deck']
    set_total = data.total_cards_in_list(cards)
    total = deck.total_cards
    ratio = float(set_total) / float(total)
    return get_percent_from_decimal(ratio)

def get_percent_from_decimal(number):
    return str(int(round(number, 2) * 100)) + "%"

def total_cost(cards, **kwargs):
    total_cost = data.sum_over_attr("cost", cards, convert_type=int)
    return total_cost

def mean_cost(cards, **kwargs):
    mean = data.average_over_attr("cost", cards)
    return mean

def max_cost(cards, **kwargs):
    costs = data.get_list_of_attr("cost", cards, convert_type=int)
    if not costs:
        return '/'
    return max(costs)

def mean_strength(cards, **kwargs):
    mean = data.average_over_attr("strength", cards)
    return mean

def max_strength(cards, **kwargs):
    strengths = data.get_list_of_attr("strength", cards, convert_type=int)
    return max(strengths)

def mean_cost_to_strength_ratio(cards, **kwargs):
    mean_cost = data.average_over_attr("cost", cards)
    mean_strength = data.average_over_attr("strength", cards)
    ratio = float(mean_cost) / float(mean_strength)
    return round(ratio, 2)
    #return get_percent_from_decimal(ratio)

def mean_cost_to_strength_ratio_without_duplicates(cards, **kwargs):
    mean_cost = data.average_over_attr("cost", cards, unique=True)
    mean_strength = data.average_over_attr("strength", cards, unique=True)
    ratio = float(mean_cost) / float(mean_strength)
    return round(ratio, 2)
    #return get_percent_from_decimal(ratio)

def total_cost_without_duplicates(cards, **kwargs):
    total_cost = data.sum_over_attr("cost", cards, convert_type=int, unique=True)
    return total_cost

# ----------

def number_of_agenda_points(deck, **kwargs):
    agendas = data.get_cards_of_attr("type", "agenda", deck)
    total = data.sum_over_attr("agendapoints", agendas)
    return ("Number of agenda points", total)

def average_agenda_points_scored_to_win(deck, **kwargs):
    pass


# HELPER FUNCTIONS +++++++++++++++++++++++++++++++

def get_general_types():
    general_corp_types = [
        "All",
        "ICE",
        "Asset",
        "Agenda",
        "Operation",
        "Upgrade",
    ]
    general_runner_types = [
        "All",
        "Icebreaker",
        "Program",
        "Hardware",
        "Resource",
        "Event",
    ]
    return {'corp': general_corp_types, 'runner': general_runner_types}

def get_general_types_maps(cards):
    general_corp_types_map = {
        "All": cards,
        "ICE": data.get_cards_of_type("ice", cards),
        "Asset": data.get_cards_of_type("asset", cards),
        "Agenda": data.get_cards_of_type("agenda", cards),
        "Operation": data.get_cards_of_type("operation", cards),
        "Upgrade": data.get_cards_of_type("upgrade", cards),
    }
    general_runner_types_map = {
        "All": cards,
        "Icebreaker": data.get_cards_of_subtype("icebreaker", cards),
        "Program": data.get_cards_of_type("program", cards),
        "Hardware": data.get_cards_of_type("hardware", cards),
        "Event": data.get_cards_of_type("event", cards),
        "Resource": data.get_cards_of_type("resource", cards),
    }
    return {
        'corp': general_corp_types_map, 
        'runner': general_runner_types_map
    }

def get_general_analysis_ftn_names():
    general_analysis_ftn_names = [ftn.__name__.capitalize().replace('_', ' ') for ftn in get_general_analysis_ftns()]
    return general_analysis_ftn_names

def get_ice_analysis_ftn_names():
    ftn_names = [ftn.__name__.capitalize().replace('_', ' ') for ftn in get_ice_analysis_ftns()]
    return ftn_names

def get_icebreaker_analysis_ftn_names():
    ftn_names = [ftn.__name__.capitalize().replace('_', ' ') for ftn in get_icebreaker_analysis_ftns()]
    return ftn_names

def get_special_analysis_ftn_names(side):
    if side.lower() == 'corp':
        return get_ice_analysis_ftn_names()
    elif side.lower() == 'runner':
        return get_icebreaker_analysis_ftn_names()
    else:
        raise ValueError("'side' is not Runner or Corp!")

