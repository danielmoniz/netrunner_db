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


    test_card = full_card_map["The Cleaners"]
    pprint.pprint(test_card)


    deck_analysis = analyze.run_analyses(deck)
    #deck_analysis.append(analyze.total_deck_cost(deck))

    return render_template(
        'read_deck.html', 
        deck=deck,
        identity=deck.identity, 
        cards=deck.cards, 
        side=deck.side,
        cat_cards=deck.cat_cards, 
        flaws=flaws,
        analysis=deck_analysis,
    )

def print_data():
    print '*'*10

if __name__ == '__main__':
    app.run(debug=True)
