

import data
import analyze



# ANALYSIS +++++++++++++++++++++++++++++++

def get_subtypes_map(card_subtypes, cards):
    card_subtypes_map = {}
    for card_subtype in card_subtypes:
        if card_subtype.lower() == 'all':
            card_subtypes_map[card_subtype] = cards
            continue
        card_subtypes_map[card_subtype] = data.get_cards_of_subtype(card_subtype, cards)
    return card_subtypes_map

def build_analysis_blocks(deck):
    analysis_blocks = []
    analysis_ftn_blocks = analyze.get_analysis_ftn_blocks(deck.side, deck)
    for ftn_block in analysis_ftn_blocks:
        title = ftn_block['title']
        ftn_list = ftn_block['analysis_ftns']
        column_names = ftn_block['column_names']
        card_set_map_ftn = ftn_block['column_map_ftn']
        analysis_block = build_analysis_block(ftn_block, ftn_list, card_set_map_ftn, column_names, deck)
        analysis_blocks.append(analysis_block)

    # format analysis blocks
    for i in range(len(analysis_blocks)):
        block = analysis_blocks[i]['table']
        if 'transpose' in analysis_blocks[i] and analysis_blocks[i]['transpose']:
            continue
        analysis_blocks[i]['table'] = zip(*block)

    return analysis_blocks

def build_analysis_block(ftn_block, analysis_ftns, card_set_map_ftn, column_names, deck):
    table = []
    ftn_names = analyze.get_names_from_functions(analysis_ftns)
    card_subset = deck[:]
    if 'card_subset' in ftn_block:
        card_subset = ftn_block['card_subset']
    table.append([""] + ftn_names)
    for column_name in column_names:
        column = []
        column.append(column_name)
        if column_name.lower() == 'all':
            cards = card_subset
        else:
            cards = card_set_map_ftn(column_name, card_subset)
        analysis = analyze.run_analysis_ftns(
            analysis_ftns,
            cards, 
            full_deck=deck, 
            faction=deck.faction,
            identity=deck.identity,
        )
        column.extend(analysis)
        table.append(column)
    ftn_block['table'] = table
    return ftn_block

