from flask import Flask
from flask import render_template
from flask import request

import deck_reader

import bs4
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
    #print all_cards

    deck_data = request.form['deck_data']
    deck = deck_reader.get_deck_from_text(deck_data, all_cards)
    print deck['identity']
    if not deck:
        return "Deck was invalid."
    cat_deck = deck_reader.categorize_deck(deck)
    #completion = deck_reader.deck_completion(deck)
    flaws = deck_reader.find_flaws(deck, all_cards)
    return render_template('read_deck.html', deck=deck, cat_deck=cat_deck, flaws=flaws)

if __name__ == '__main__':
    app.run(debug=True)
