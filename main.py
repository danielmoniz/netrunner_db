import pprint

from flask import Flask
from flask import render_template
from flask import request

import deck as deck_module
import deck_reader
import analyze
import netrunner_constants as constants

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    return render_template('read_deck.html')

@app.route('/read_deck', methods=["GET", "POST"])
def read_deck():
    if request.method == 'GET':
        return render_template('read_deck.html')
    all_cards = deck_reader.get_all_cards()
    full_card_map = deck_reader.get_card_map_of_all_cards()
    full_card_map_lower = deck_reader.get_card_map_of_all_cards(lower=True)

    deck_data = request.form['deck_data']
    deck = deck_module.Deck.build_deck_from_text(deck_data, full_card_map_lower)
    if not deck:
        return render_template('read_deck.html')
    """
    if not deck:
        return "Deck was invalid."
    """
    #flaws = deck_reader.find_flaws(deck, full_card_map)
    flaws = []

    # test
    import data

    """
    print '*'*10
    print "ADVANCED CARD SEARCH:"
    advanced_results = data.advanced_text_search(
        deck,
        mandatory_words="credit",
        partial_words=["gain", "take"]
    )
    for card in advanced_results:
        print card.name
    """
    
    print "$"*20
    cards = data.get_cards_of_attr("side", "corp", all_cards[:])
    cards = data.get_cards_of_attr("actions", 0, cards, convert_type=int, compare=lambda x,y: x<=y)
    for card in cards:
        print card, card.actions
    print len(cards)
    print "$"*20

    print "$"*20
    cards = data.advanced_deck_search(all_cards[:], exact_text=["only if you made a successful"])
    #cards = data.get_cards_of_attr("actions", 0, cards, convert_type=int, compare=lambda x,y: x<=y)
    for card in cards:
        print card
    print len(cards)
    print "$"*20

    card_set = data.get_ice(all_cards[:])
    card_set = data.get_cards_of_attr('cost', 2, card_set, convert_type=int, compare=lambda x,y:x<=y)
    card_set = data.advanced_deck_search(card_set, exact_text=["end the run"])
    #card_set = data.get_cards_of_subtype("sentry", card_set)
    for card in card_set:
        print card, card.cost, card.strength, card.identity, card.loyalty
        print card.subtype
        print card.text
        print ""
    print "\n" + str(len(card_set))
    print "*"*20


    test_card = full_card_map["Blackguard"]
    # @TODO This causes a KeyError. Fix this!
    #test_card = full_card_map["Unregistered S&W '35"]
    pprint.pprint(test_card)

    # ANALYSIS +++++++++++++++++++++++++++++++

    def get_subtypes_map(card_subtypes, cards):
        card_subtypes_map = {}
        for card_subtype in card_subtypes:
            if card_subtype.lower() == 'all':
                card_subtypes_map[card_subtype] = cards
                continue
            card_subtypes_map[card_subtype] = data.get_cards_of_subtype(card_subtype, cards)
        return card_subtypes_map

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
                identity=deck.faction
            )
            column.extend(analysis)
            table.append(column)
        print '*'*20
        print card_subset
        ftn_block['table'] = table
        print ftn_block['title']
        print '*'*20
        return ftn_block


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
        return analysis_blocks
            
    analysis_blocks = build_analysis_blocks(deck)
    for i in range(len(analysis_blocks)):
        block = analysis_blocks[i]['table']
        analysis_blocks[i]['table'] = zip(*block)

    cards = all_cards[:]
    cards = data.get_cards_of_attr('rating', '4', cards)
    cards = data.get_cards_of_attr_in('identity', ('Criminal', 'Neutral'), cards)
    cards = data.get_cards_of_attr('side', 'runner', cards)
    print '%'*20
    for card in cards:
        print card
    print '#'*20


    return render_template(
        'read_deck.html', 
        deck=deck,
        shuffled_deck=deck.shuffle,
        identity=deck.identity, 
        cards=deck.cards, 
        side=deck.side,
        cat_cards=deck.cat_cards, 
        flaws=flaws,
        analysis=analysis_blocks,
    )


if __name__ == '__main__':
    app.run(debug=True)
