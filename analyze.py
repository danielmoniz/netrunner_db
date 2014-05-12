import data
import re

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

    #analysis_ftns = get_general_analysis_ftns()
    return run_analysis_ftns(analysis_ftns, cards, **kwargs)


def get_analysis_ftn_blocks(side, cards):
    if side.lower() == 'corp':
        return get_corp_analysis_ftn_blocks(cards)
    elif side.lower() == 'runner':
        return get_runner_analysis_ftn_blocks(cards)
    else:
        raise ValueError("side variable is not 'corp' or 'runner'.")


def get_corp_general_column_names():
    return [
        "All",
        "ICE",
        "Asset",
        "Agenda",
        "Operation",
        "Upgrade",
    ]

def get_runner_general_column_names():
    return [
        "All",
        #"Icebreaker",
        "Program",
        "Hardware",
        "Resource",
        "Event",
    ]

def get_mandatory_ice_column_names():
    return [
        'Barrier',
        'Code Gate',
        'Sentry',
    ]

def get_mandatory_icebreaker_column_names():
    return [
        'Fracter',
        'Decoder',
        'Killer',
        'AI',
    ]


def get_ice_subtype_columns(cards):
    mandatory_subtypes = get_mandatory_ice_column_names()
    return ["All"] + data.get_subtypes(cards, mandatory_subtypes)

def get_icebreaker_subtype_columns(cards):
    mandatory_subtypes = get_mandatory_icebreaker_column_names()
    subtypes = ["All"] + data.get_subtypes(cards, mandatory_subtypes)
    subtypes.remove('Icebreaker')
    return subtypes

def get_corp_analysis_ftn_blocks(cards):
    analysis_ftn_blocks = [
        {'title': 'Deck constraints', 
            'analysis_ftns':
            [
                total,
                total_out_of_faction_influence,
                turns_to_play,
            ],
            'column_names': get_corp_general_column_names(),
            'column_map_ftn': data.get_cards_of_type,
        },

        {'title': 'General Analysis', 
            'analysis_ftns':
            [
                total_as_ratio,
                total_cost,
                total_cost_without_duplicates,
                mean_cost,
                max_cost,
                total_actions,
                total_actions_with_draw,
                total_net_cost,
                total_net_cost_with_draw,
            ],
            'column_names': get_corp_general_column_names(),
            'column_map_ftn': data.get_cards_of_type,
        },

        {'title': 'Ice Analysis (general)', 
            'analysis_ftns':
            [
                total,
                total_cost,
                total_cost_without_duplicates,
                mean_strength,
                max_strength,
                mean_cost,
                mean_cost_to_strength_ratio,
                mean_cost_to_strength_ratio_without_duplicates,
                number_of_ice_that_ends_runs,
            ],
            'column_names': get_ice_subtype_columns(data.get_ice(cards)),
            'column_map_ftn': data.get_cards_of_subtype,
            'card_subset': data.get_ice(cards),
        },
    ]
    return analysis_ftn_blocks

def get_runner_analysis_ftn_blocks(cards):
    analysis_ftn_blocks = [
        {'title': 'Deck constraints', 
            'analysis_ftns':
            [
                total,
                total_out_of_faction_influence,
                turns_to_play,
            ],
            'column_names': get_runner_general_column_names(),
            'column_map_ftn': data.get_cards_of_type,
        },

        {'title': 'General Analysis', 
            'analysis_ftns':
            [
                total_as_ratio,
                total_cost,
                total_cost_without_duplicates,
                mean_cost,
                max_cost,
                total_actions,
                total_actions_with_draw,
                total_net_cost,
                total_net_cost_with_draw,
            ],
            'column_names': get_runner_general_column_names(),
            'column_map_ftn': data.get_cards_of_type,
        },

        {'title': 'Icebreaker Analysis (general)', 
            'analysis_ftns':
            [
                total,
                total_cost,
                total_cost_without_duplicates,
                mean_strength,
                max_strength,
                mean_cost_to_strength_ratio,
                mean_cost_to_strength_ratio_without_duplicates,
            ],
            'column_names': get_icebreaker_subtype_columns(data.get_icebreakers(cards)),
            'column_map_ftn': data.get_cards_of_subtype,
            'card_subset': data.get_icebreakers(cards),
        },

        {'title': 'Program Analysis (general)', 
            'analysis_ftns':
            [
                total_memory_units,
                total_memory_units_without_duplicates,
                total_generated_memory,
            ],
            'column_names': ['All', 'Icebreaker',],
            'column_map_ftn': data.get_cards_of_subtype,
            'card_subset': data.get_cards_of_type("program", cards),
        },

        {'title': "Memory Analysis", 
            'analysis_ftns':
            [
                total_generated_memory,
                total,
                deck_memory,
            ],
            'column_names': get_memory_column_names(cards),
            'column_map_ftn': data.get_cards_of_name,
            'card_subset': data.get_memory_added_cards(cards),
        },

    ]
    
    return analysis_ftn_blocks
def get_memory_column_names(cards):
        memory_cards = data.get_cards_of_attr("memory_added", 1, cards, convert_type=int, compare=lambda x,y:x>=y)
        column_names = data.get_list_of_attr("name", memory_cards, unique=True)
        return ['All'] + column_names

def deck_memory(cards, **kwargs):
    return data.get_generated_memory_from_deck(cards)

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

def total_generated_memory(cards, **kwargs):
    total_memory = 0
    for card in cards:
        memory_added = data.get_generated_memory(card)
        total_memory += int(memory_added)
    return total_memory

def total_memory_units(cards, **kwargs):
    total = data.sum_over_attr("memory", cards, convert_type=int)
    return total


def total_memory_units_without_duplicates(cards, **kwargs):
    total = data.sum_over_attr("memory", cards, convert_type=int, unique=True)
    return total


def total(cards, **kwargs):
    return data.get_total_cards(cards)

def total_as_ratio(cards, **kwargs):
    deck = kwargs['full_deck']
    set_total = data.get_total_cards(cards)
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
    if strengths:
        return max(strengths)
    return '/'

def mean_cost_to_strength_ratio(cards, **kwargs):
    mean_cost = data.average_over_attr("cost", cards)
    mean_strength = data.average_over_attr("strength", cards)
    if not mean_strength:
        return '/'
    ratio = float(mean_cost) / float(mean_strength)
    return round(ratio, 2)

def mean_cost_to_strength_ratio_without_duplicates(cards, **kwargs):
    mean_cost = data.average_over_attr("cost", cards, unique=True)
    mean_strength = data.average_over_attr("strength", cards, unique=True)
    if not mean_strength:
        return '/'
    ratio = float(mean_cost) / float(mean_strength)
    return round(ratio, 2)

def total_cost_without_duplicates(cards, **kwargs):
    total_cost = data.sum_over_attr("cost", cards, convert_type=int, unique=True)
    return total_cost

def total_actions(cards, **kwargs):
    return data.get_total_actions(cards)[0]

def total_actions_with_draw(cards, **kwargs):
    return data.get_total_actions(cards)[1]

def turns_to_play(cards, **kwargs):
    return (float(data.get_total_actions(cards)[1]))/ 4.0

def total_net_cost(cards, **kwargs):
    return data.sum_over_attr("net_cost", cards, convert_type=int)

def total_net_cost_with_draw(cards, **kwargs):
    return data.sum_over_attr("net_cost_with_draw", cards, convert_type=int)

def number_of_ice_that_ends_runs(cards, **kwargs):
    ice = data.get_ice(cards)
    end_run_ice = data.advanced_deck_search(ice, exact_text=["end the run"])
    return data.get_total_cards(end_run_ice)

def total_out_of_faction_influence(cards, identity=None, **kwargs):
    if not identity:
        raise ValueError
    out_of_faction_cards = data.get_cards_of_attr_not_in("identity", identity, cards)
    return data.sum_over_attr("loyalty", out_of_faction_cards, convert_type=int)

# ---------


def get_run_events(cards, **kwargs):
    events = data.get_cards_of_type('event', cards)
    run_events = data.get_cards_of_subtype('run', events)
    return data.total_cards(run_events)
    

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

def get_names_from_functions(ftns):
    ftn_names = [ftn.__name__.capitalize().replace('_', ' ') for ftn in ftns]
    return ftn_names

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

