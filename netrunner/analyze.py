import data
import re
import card as card_module
import output
import parse

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


def get_analysis_ftn_blocks(side, deck):
    if side.lower() == 'corp':
        return get_corp_analysis_ftn_blocks(deck)
    elif side.lower() == 'runner':
        return get_runner_analysis_ftn_blocks(deck)
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

def get_sets(cards):
    sets = set(data.get_list_of_attr('set', cards, unique=True))
    sets.update(["Core"])
    return list(sets)

def get_ice_subtype_columns(cards):
    mandatory_subtypes = get_mandatory_ice_column_names()
    return ["All"] + data.get_subtypes(cards, mandatory_subtypes)

def get_icebreaker_subtype_columns(cards):
    mandatory_subtypes = get_mandatory_icebreaker_column_names()
    subtypes = ["All"] + data.get_subtypes(cards, mandatory_subtypes)
    if 'Icebreaker' in subtypes:
        subtypes.remove('Icebreaker')
    return subtypes

def get_corp_analysis_ftn_blocks(deck):
    analysis_ftn_blocks = [
        {'title': 'Deck constraints', 
            'analysis_ftns':
            [
                total_cards,
                total_out_of_faction_influence,
                agenda_points,
            ],
            'column_names': get_corp_general_column_names(),
            'column_map_ftn': data.get_cards_of_type,
        },

        {'title': 'General Analysis', 
            'analysis_ftns':
            [
                total_cards,
                total_as_ratio,
                total_cost,
                total_cost_without_duplicates,
                mean_cost,
                max_cost,
                total_actions,
                total_actions_with_draw,
                total_net_cost,
                total_net_cost_with_draw,
                turns_to_play,
            ],
            'column_names': get_corp_general_column_names(),
            'column_map_ftn': data.get_cards_of_type,
        },

        {'title': 'Ice Analysis (general)', 
            'analysis_ftns':
            [
                total_cards,
                total_cost,
                total_cost_without_duplicates,
                mean_strength,
                max_strength,
                mean_cost,
                mean_cost_to_strength_ratio,
                mean_cost_to_strength_ratio_without_duplicates,
                number_of_ice_that_ends_runs,
            ],
            'column_names': get_ice_subtype_columns(data.get_ice(deck)),
            'column_map_ftn': data.get_cards_of_subtype,
            'card_subset': data.get_ice(deck),
        },

        {'title': 'Agenda Analysis', 
            'analysis_ftns':
            [
                total_cards,
                agenda_points,
                minimum_turns_to_win,
                average_agendas_scored_to_win,
                average_actions_to_score_winning_agendas,
            ],
            'column_names': ['All'] + data.get_list_of_attr('name', data.get_cards_of_type('agenda', deck), unique=True),
            'column_map_ftn': data.get_cards_of_name,
            'card_subset': data.get_cards_of_type('agenda', deck),
            'notes': "Cards for fastest win: " + output.print_single_line_card_list(parse.condense_card_list(get_cards_for_fastest_win(deck))),
        },

        {'title': 'Income Analysis',
            'analysis_ftns':
            [
                total_cards,
                total_net_income_from_instant_cards,
                average_net_income_from_instant_cards,
                draw_rate_of_income_cards,
                net_income_draw_rate,
            ],
            'column_names': ['All'] + data.get_list_of_attr('name', data.get_money_making_cards(deck, instant=True), unique=True),
            'column_map_ftn': data.get_cards_of_name,
            'card_subset': data.get_money_making_cards(deck, instant=True),
        },

        {'title': 'Set Analysis',
            'analysis_ftns':
            [
                total_cards,
                agenda,
                ice,
                asset,
                operation,
                upgrade,
            ],
            'column_names': get_sets(deck),
            'column_map_ftn': data.get_cards_of_set,
            'transpose': True,
        },

        {'title': 'Bad Publicity Analysis',
            'analysis_ftns':
            [
                total_cards,
                bad_publicity,
            ],
            'column_names': ['All'] + data.get_list_of_attr('name', data.get_bad_publicity_cards(deck), unique=True),
            'column_map_ftn': data.get_cards_of_name,
            'card_subset': data.get_bad_publicity_cards(deck),
            'notes': data.get_bad_publicity.__doc__
        },

    ]
    return analysis_ftn_blocks

def get_runner_analysis_ftn_blocks(deck):
    analysis_ftn_blocks = [
        {'title': 'Deck constraints', 
            'analysis_ftns':
            [
                total_cards,
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
                total_cards,
                total_cost,
                total_cost_without_duplicates,
                mean_strength,
                max_strength,
                mean_cost_to_strength_ratio,
                mean_cost_to_strength_ratio_without_duplicates,
            ],
            'column_names': get_icebreaker_subtype_columns(data.get_icebreakers(deck)),
            'column_map_ftn': data.get_cards_of_subtype,
            'card_subset': data.get_icebreakers(deck),
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
            'card_subset': data.get_cards_of_type("program", deck),
        },

        {'title': "Memory Analysis", 
            'analysis_ftns':
            [
                total_generated_memory,
                total_cards,
                deck_memory,
            ],
            'column_names': get_memory_column_names(deck),
            'column_map_ftn': data.get_cards_of_name,
            'card_subset': data.get_memory_added_cards(deck),
        },

        {'title': 'Income Analysis',
            'analysis_ftns':
            [
                total_cards,
                total_net_income_from_instant_cards,
                average_net_income_from_instant_cards,
                draw_rate_of_income_cards,
                net_income_draw_rate,
            ],
            'column_names': ['All'] + data.get_list_of_attr('name', data.get_money_making_cards(deck, instant=True), unique=True),
            'column_map_ftn': data.get_cards_of_name,
            'card_subset': data.get_money_making_cards(deck, instant=True),
        },

        {'title': 'Set Analysis',
            'analysis_ftns':
            [
                total_cards,
                event,
                icebreaker,
                program,
                hardware,
                resource,
            ],
            'column_names': get_sets(deck),
            'column_map_ftn': data.get_cards_of_set,
            'transpose': True,
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


def total_cards(cards, **kwargs):
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

def total_cost_of_deck(cards, full_deck=None, **kwargs):
    if not full_deck:
        return False
    total_cost = data.sum_over_attr("cost", full_deck, convert_type=int)
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

def total_out_of_faction_influence(cards, faction=None, **kwargs):
    if not faction:
        raise ValueError
    out_of_faction_cards = data.get_cards_of_attr_not_in("identity", faction, cards)
    return data.sum_over_attr("loyalty", out_of_faction_cards, convert_type=int)


def agenda_points(cards, **kwargs):
    num_agenda_points = data.sum_over_attr('agendapoints', cards, convert_type=int)
    if num_agenda_points == 0:
        return '/'
    return num_agenda_points

def average_agendas_scored_to_win(cards, identity=None, **kwargs):
    points_to_win = 7
    if identity.name == "Harmony Medtech: Biomedical Pioneer":
        points_to_win = 6
    agendas = data.get_cards_of_type('agenda', cards)
    num_agendas = data.get_total_cards(agendas)
    total_agenda_points = data.sum_over_attr('agendapoints', agendas, convert_type=int)
    points_per_agenda = float(total_agenda_points) / float(num_agendas) 
    num_scored_to_win = float(points_to_win) / points_per_agenda
    if int(num_scored_to_win) == num_scored_to_win:
        return int(num_scored_to_win)
    return round(num_scored_to_win, 2)

def minimum_turns_to_win(cards, identity=None, **kwargs):
    clicks_per_turn = 3
    starting_credits = 5

    cards_for_win = get_cards_for_fastest_win(cards, identity, kwargs['full_deck'])
    if not cards_for_win:
        return '/'
    turns_to_play = data.get_turns_to_play(cards_for_win)
    return turns_to_play


def get_cards_for_fastest_win(cards, identity=None, full_deck=None):
    if not identity:
        identity = cards.identity
    if not full_deck:
        full_deck = cards
    points_to_win = 7
    if identity.name == "Harmony Medtech: Biomedical Pioneer":
        points_to_win = 6
    agendas = data.get_cards_of_type('agenda', cards)
    agendas = data.get_agendas_to_fastest_win(agendas, identity, points_to_win)
    if not agendas:
        return False
    actions_to_play = data.sum_over_attr("actions", agendas, convert_type=int)

    total_cost = data.sum_over_attr('cost', agendas, convert_type=int)
    start_credits = 5
    clicks_per_turn = 3
    # for now, assume player must use actions to take credits
    #turns_for_credits = max(0, total_cost - 5)
    credits_needed = max(0, total_cost - 5)
    money_makers = data.get_money_making_cards(full_deck, instant=True)
    money_makers = parse.get_full_card_list(money_makers)
    money_makers = sorted(money_makers, key=lambda card: int(card.net_cost))
    money_makers_used = []
    actions_used_for_moneymakers = 0
    for card in money_makers:
        if credits_needed < card.actions:
            break
        money_makers_used.append(card)
        credits_needed -= card.net_income
        actions_used_for_moneymakers += card.actions

    return agendas + money_makers_used


def average_actions_to_score_winning_agendas(cards, identity=None, **kwargs):
    points_to_win = 7
    if identity.name == "Harmony Medtech: Biomedical Pioneer":
        points_to_win = 6
    agendas = data.get_cards_of_type('agenda', cards)
    print '^'*20
    for card in agendas:
        print card.name, card.actions, card.agendapoints
    print '^'*20
    num_agendas = data.get_total_cards(agendas)
    total_actions = data.sum_over_attr('actions', agendas, convert_type=int)
    total_points = data.sum_over_attr('agendapoints', agendas, convert_type=int)
    ratio = points_to_win / float(total_points)
    #actions_per_agenda = float(total_actions) / num_agendas
    average_actions_to_score = float(total_actions) * ratio
    if average_actions_to_score == int(average_actions_to_score):
        return int(average_actions_to_score)
    return round(average_actions_to_score, 2)

def net_income_draw_rate(cards, full_deck=None, **kwargs):
    income_cards = data.get_money_making_cards(cards, instant=True)
    total_net_income = data.sum_over_attr('net_income', income_cards)
    total_cards = data.get_total_cards(full_deck)
    net_income_draw_rate = float(total_net_income) / total_cards
    return round(net_income_draw_rate, 2)

def draw_rate_of_income_cards(cards, full_deck=None, **kwargs):
    num_cards = data.get_total_cards(full_deck)
    income_cards = data.get_money_making_cards(cards)
    num_income_cards = data.get_total_cards(income_cards)
    ratio = num_income_cards / float(num_cards)
    return get_percent_from_decimal(ratio)


def average_net_income_from_instant_cards(cards, **kwargs):
    cards = data.get_money_making_cards(cards)
    total_income = data.get_net_income_from_cards(cards, instant=True)
    num_income_cards = data.get_total_cards(cards)
    return round(float(total_income) / num_income_cards, 2)

def total_net_income_from_instant_cards(cards, **kwargs):
    cards = data.get_money_making_cards(cards)
    total_income = data.get_net_income_from_cards(cards, instant=True)
    return total_income

def bad_publicity(cards, **kwargs):
    total = 0
    for card in cards:
        total += card.bad_publicity * int(card.quantity)
    return total

# Specific category getters (to use functions as columns)
# ---- Corp category getters

def agenda(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('agenda', cards))

def ice(cards, **kwargs):
    return data.get_total_cards(data.get_ice(cards))

def asset(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('asset', cards))

def operation(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('operation', cards))

def upgrade(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('upgrade', cards))

# ---- Runner category getters

def event(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('event', cards))

def icebreaker(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_subtype('icebreaker', cards))

def program(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('program', cards))

def hardware(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('hardware', cards))

def resource(cards, **kwargs):
    return data.get_total_cards(data.get_cards_of_type('resource', cards))


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

