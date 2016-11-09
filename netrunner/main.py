import pprint

from flask import Flask
from flask import render_template
from flask import request

import deck as deck_module
import deck_reader
import analysis
import card as card_module

from netrunner import app

#app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    return render_template('read_deck.html')

@app.route('/read_deck', methods=["GET", "POST"])
def read_deck():
    # get all cards for reference
    # read deck
    # analyze deck
    # return analysis information
    if request.method == 'GET':
        return render_template('read_deck.html')
    all_cards = deck_reader.get_all_cards()
    full_card_map = deck_reader.get_card_map_of_all_cards()
    full_card_map_lower = deck_reader.get_card_map_of_all_cards(lower=True)

    deck_data = request.form['deck_data']
    deck = deck_module.Deck.build_deck_from_text(deck_data, full_card_map_lower)
    if not deck:
        return render_template('read_deck.html')
    #flaws = deck_reader.find_flaws(deck, full_card_map)
    flaws = []

    # test
    import data

    test_card = full_card_map["Q-Coherence Chip"]
    pprint.pprint(test_card)
    new_card = card_module.DetailedCard(test_card)
    print new_card, new_card.cost, new_card.net_cost

    # @TODO This causes a KeyError. Fix this!
    #test_card = full_card_map["Unregistered S&W '35"]
            
    analysis_blocks = analysis.build_analysis_blocks(deck)

    print ')'*20
    for card in deck:
        if not data.is_instant(card):
            continue
        if int(card.income) > 0:
            print card, card.income, card.cost, card.net_income
    print ')'*20

    cards = data.get_memory_added_cards(all_cards)
    for card in cards:
        print card
    print '&'*20

    cards = data.get_cards_of_attr("bad_publicity", 0, all_cards, convert_type=int, compare=lambda x,y: x != y)
    for card in cards:
        print card.name, card.bad_publicity
    print '#'*20

    cards = data.advanced_deck_search(all_cards, exact_text=["bad publicity"])
    extra = []
    for card in cards:
        item = ""
        item += card.name + " " + unicode(card.bad_publicity) + "<br />"
        item += card.type + "<br />"
        item += card.text + "<br />"
        extra.append(item)
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
        extra=extra,
    )


if __name__ == '__main__':
    app.run(debug=True)
