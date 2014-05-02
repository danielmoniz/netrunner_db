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

    deck_data = request.form['deck_data']
    deck = deck_module.Deck.build_deck_from_text(deck_data, full_card_map)
    if not deck:
        return "Deck was invalid."
    flaws = deck_reader.find_flaws(deck, full_card_map)
    #flaws = []

    # test
    import data

    advanced_results = data.advanced_text_search(
        deck,
        mandatory_words="credit",
        partial_words=["gain", "take"]
    )
    print '*'*10
    print "ADVANCED CARD SEARCH:"
    for card in advanced_results:
        print card.name
    test_cards = data.get_cards_of_type('program', deck)
    for card in test_cards:
        print card

    import pprint

    print '*'*10
    # lambda comparison test
    attr = 'memory'
    attr_value = 1
    test_cards = data.get_cards_of_attr(attr, attr_value, deck)
    print '*'*10
    if test_cards:
        for card in test_cards:
            print card, "{}: {}".format(attr, getattr(card, attr))

    print '*'*10
    test_cards = data.advanced_text_search(
        all_cards,
        exact_text=("at least", "advancement token"),
        #mandatory_words=(,),
    )
    for card in test_cards:
        print card


    test_card = full_card_map["Hadrian's Wall"]
    #pprint.pprint(test_card)

    # ANALYSIS +++++++++++++++++++++++++++++++

    #deck_analysis = analyze.run_analyses(deck)

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

    general_corp_types_map = {
        "All": deck,
        "ICE": data.get_cards_of_type("ice", deck),
        "Asset": data.get_cards_of_type("asset", deck),
        "Agenda": data.get_cards_of_type("agenda", deck),
        "Operation": data.get_cards_of_type("operation", deck),
        "Upgrade": data.get_cards_of_type("upgrade", deck),
    }
    general_runner_types_map = {
        "All": deck,
        "Icebreaker": data.get_cards_of_subtype("icebreaker", deck),
        "Program": data.get_cards_of_type("program", deck),
        "Hardware": data.get_cards_of_type("hardware", deck),
        "Event": data.get_cards_of_type("event", deck),
        "Resource": data.get_cards_of_type("resource", deck),
    }

    if deck.side.lower() == "corp":
        ice = data.get_cards_of_type("ice", deck)
        ice_types = list(set(data.get_list_of_attr("subtype", ice)))
        ice_types_set = set()
        for ice_type_str in ice_types:
            current_ice_types = data.parse_subtype(ice_type_str)
            current_ice_types = [ice_type.title() for ice_type in current_ice_types]
            ice_types_set.update(current_ice_types)
        ice_types = ['All'] + list(ice_types_set)
        ice_types_map = {}
        for ice_type in ice_types:
            ice_of_type = data.get_ice(deck)
            if ice_type.lower() == 'all':
                ice_types_map[ice_type] = ice
                continue
            ice_types_map[ice_type] = data.get_cards_of_subtype(ice_type, ice_of_type)
    else:
        icebreakers = data.get_cards_of_subtype("icebreaker", deck)
        icebreaker_types = ["All"] + list(set(data.get_list_of_attr("subtype", icebreakers)))
        icebreaker_types_map = {}
        for icebreaker_type in icebreaker_types:
            icebreakers = data.get_icebreakers(deck)
            if icebreaker_type.lower() == 'all':
                icebreaker_types_map[icebreaker_type] = icebreakers
                continue
            icebreaker_types_map[icebreaker_type] = data.get_cards_of_subtype(icebreaker_type, icebreakers)


    analysis_blocks = []
    
    if deck.side.lower() == 'corp':
        general_types = general_corp_types
        general_map = general_corp_types_map
        special_types = ice_types
        special_map = ice_types_map
    else:
        general_types = general_runner_types
        general_map = general_runner_types_map
        special_types = icebreaker_types
        special_map = icebreaker_types_map

    general_analysis_block = []
    general_analysis_block.append([""] + analyze.get_general_analysis_ftn_names())
    for card_type in general_types:
        column = []
        column.append(card_type)
        cards = general_map[card_type]
        analysis = analyze.run_general_analyses(cards)
        column.extend(analysis)
        general_analysis_block.append(column)

    special_analysis_block = []
    special_analysis_block.append([""] + analyze.get_special_analysis_ftn_names(deck.side))
    print "Special types:", special_types
    for special_type in special_types:
        column = []
        column.append(special_type)
        cards = special_map[special_type]
        analysis = analyze.run_special_analyses(cards, side=deck.side)
        column.extend(analysis)
        special_analysis_block.append(column)

    analysis_blocks.append(general_analysis_block)
    analysis_blocks.append(special_analysis_block)
    for i in range(len(analysis_blocks)):
        block = analysis_blocks[i]
        analysis_blocks[i] = zip(*block)

    return render_template(
        'read_deck.html', 
        deck=deck,
        identity=deck.identity, 
        cards=deck.cards, 
        side=deck.side,
        cat_cards=deck.cat_cards, 
        flaws=flaws,
        analysis=analysis_blocks,
        general_analysis=general_analysis_block,
        special_analysis=special_analysis_block,
        #analysis=deck_analysis,
    )

if __name__ == '__main__':
    app.run(debug=True)
