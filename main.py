from flask import Flask
from flask import render_template
from flask import request

import deck_reader

import sqlite3
import bs4
import netrunner_constants as constants

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    return render_template('read_deck.html')


def reformat_cards(card_list):
    """Change list of cards into a desirable data structure.
    """
    card_dict = {}
    for card in card_list:
        card_name = str(bs4.BeautifulSoup(card[constants.NAME]))
        card_dict[card_name] = card
    return card_dict


@app.route('/read_deck', methods=["GET", "POST"])
def read_deck():
    if request.method == 'GET':
        return render_template('read_deck.html')
    connection = sqlite3.connect("cards.db")
    c = connection.cursor()
    query = c.execute("SELECT * FROM netrunner")
    cards = query.fetchall()
    cards = reformat_cards(cards)

    deck_data = request.form['deck_data']
    deck = deck_reader.get_deck_from_text(deck_data, cards)
    if not deck:
        return "Deck was invalid."
    cat_deck = deck_reader.categorize_deck(deck)
    print cat_deck
    return render_template('read_deck.html', deck=deck, cat_deck=cat_deck)

if __name__ == '__main__':
    app.run(debug=True)
