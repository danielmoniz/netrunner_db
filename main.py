from flask import Flask
from flask import render_template
from flask import request
import bs4

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
    #print all_cards

    deck_data = request.form['deck_data']
    deck = deck_reader.get_deck_from_text(deck_data, all_cards)
    print deck.side
    if not deck:
        return "Deck was invalid."
    flaws = deck_reader.find_flaws(deck, all_cards)
    #flaws = []

    deck_analysis = []
    deck_analysis.append(analyze.total_deck_cost(deck, all_cards))

    return render_template(
        'read_deck.html', 
        identity=deck.identity, 
        deck=deck.cards, 
        side=deck.side,
        cat_deck=deck.cat_cards, 
        flaws=flaws,
        analysis=deck_analysis,
    )

if __name__ == '__main__':
    app.run(debug=True)
