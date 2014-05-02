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
    data.count_subtypes(deck)
    data.count_types(deck)
    print "TEST: Sure Gamble has text:", full_card_map['Sure Gamble']['text']
    data.find_cards_with_exact_text("Gain", deck)
    data.find_cards_with_all_words("Gain credits", deck)

    print '*'*10
    advanced_results = data.advanced_text_search(
        deck,
        mandatory_words="credit",
        partial_words=["gain", "take"]
    )
    print "ADVANCED CARD SEARCH:"
    for card in advanced_results:
        print card.name
    test_cards = data.get_cards_of_type('program', deck)
    for card in test_cards:
        print card
    print '*'*10
    icebreakers = data.get_icebreakers(deck)
    for card in icebreakers:
        print card
    ai = data.get_ai(deck)
    print '*'*10
    for card in ai:
        print card
    print '*'*10
    diff_cost_cards = all_cards[:]
    #diff_cost_cards = data.get_cards_of_attr("side", "runner", diff_cost_cards)
    #diff_cost_cards = data.get_cards_of_attr("identity", "criminal", diff_cost_cards)

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
    pprint.pprint(test_card)

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

    if deck.side == "corp":
        ice = data.get_cards_of_type("ice", deck)
        ice_types = list(set(data.get_list_of_attr("subtype", ice)))
    else:
        icebreakers = data.get_cards_of_subtype("icebreaker", deck)
        icebreaker_types = list(set(data.get_list_of_attr("subtype", icebreakers)))


    general_analysis_block = []
    #general_analysis_block.append(general_corp_types)
    general_analysis_block.append([""] + analyze.get_general_analysis_ftn_names())
    
    if deck.side.lower() == 'corp':
        general_types = general_corp_types
        general_map = general_corp_types_map
    else:
        general_types = general_runner_types
        general_map = general_runner_types_map
    for card_type in general_types:
        column = []
        column.append(card_type)
        cards = general_map[card_type]
        analysis = analyze.run_analyses(cards)
        column.extend(analysis)
        general_analysis_block.append(column)

    special_analysis_block = []
    special_analysis_block.append(analyze.get_ice_analysis_ftn_names())
    if deck.side == "corp":
        for ice_type in ice_types:
            analysis = analyze.run_analyses(general_corp_types_map[card_type])
            special_analysis_block.append(analysis)
    else:
        for icebreaker_type in icebreaker_types:
            analysis = analyze.run_analyses(general_runner_types_map[card_type])
            special_analysis_block.append(analysis)

    general_analysis_block = zip(*general_analysis_block)
    print special_analysis_block

    return render_template(
        'read_deck.html', 
        deck=deck,
        identity=deck.identity, 
        cards=deck.cards, 
        side=deck.side,
        cat_cards=deck.cat_cards, 
        flaws=flaws,
        general_analysis=general_analysis_block,
        special_analysis=special_analysis_block,
        #analysis=deck_analysis,
    )

if __name__ == '__main__':
    app.run(debug=True)
