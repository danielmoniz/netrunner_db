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


    new_cards = data.get_cards_of_attr("set", "Honor and Profit", all_cards)
    new_cards_in_order = data.sort_by_attr('num', new_cards, convert_type=int, descending=False)
    for card in new_cards_in_order:
        pass
        #print card, card.side, card.num

    ice = data.get_ice(all_cards)
    ice = data.sort_by_attr('strength', ice, convert_type=int)
    for card in ice:
        print card, card.cost, card.strength, card.loyalty

    money_makers = data.get_money_making_cards(all_cards, instant=True)
    #money_makers = data.get_cards_of_attr("identity", "Neutral", money_makers)
    print "="*20
    for card in money_makers:
        print card
    print "="*20
    for card in money_makers:
        print "{} - {}".format(card, card.type)
        print card.text + "\n"
    print len(money_makers)

    for card in money_makers:
        print "\n" + str(card)
        income = data.get_income(card)
        print card, income
    print "="*20

    import re
    card_set = data.advanced_text_search(all_cards[:], mandatory_words=['gain', 'click'])
    for card in card_set:
        print card
        print card.text + "\n"
    print '*'*20
    for card in card_set[:]:
        match = re.search('[Gg]ain (\d) \[Credit', card.text)
        match = re.search('[Gg]ain(( \[Click\])+)', card.text)
        if not match:
            card_set.remove(card)
        else:
            print card
            print match.groups()[0].count('Click')
            print card.text + "\n"
    print len(card_set)
    print '&'*20
    card_set = data.get_cards_of_attr("side", "corp", card_set)
    for card in card_set:
        actions = data.get_card_actions(card)
        print card, card.actions
        if card.type == "Agenda":
            print card.cost, card.agendapoints
        print card.text + "\n"
    print '%'*20

    import pprint
    test_card = full_card_map["Crypsis"]
    #pprint.pprint(test_card)

    # ANALYSIS +++++++++++++++++++++++++++++++

    def get_subtypes_map(card_subtypes, cards):
        card_subtypes_map = {}
        for card_subtype in card_subtypes:
            if card_subtype.lower() == 'all':
                card_subtypes_map[card_subtype] = cards
                continue
            card_subtypes_map[card_subtype] = data.get_cards_of_subtype(card_subtype, cards)
        return card_subtypes_map

    if deck.side.lower() == "corp":
        special_cards = data.get_cards_of_type("ice", deck)
        mandatory_subtypes = ['Barrier', 'Code Gate', 'Sentry']
        special_table_title = "Ice Analysis (basic)"
    else:
        special_cards = data.get_cards_of_subtype("icebreaker", deck)
        mandatory_subtypes = ['AI', 'Fracter', 'Decoder', 'Killer']
        special_table_title = "Icebreaker Analysis (basic)"

    special_types = ["All"] + data.get_subtypes(special_cards, mandatory_subtypes)
    special_map = get_subtypes_map(special_types, special_cards)

    general_types = analyze.get_general_types()[deck.side.lower()]
    general_map = analyze.get_general_types_maps(deck)[deck.side.lower()]

    analysis_blocks = []
    
    general_analysis_block = []
    general_analysis_block.append([""] + analyze.get_general_analysis_ftn_names())
    for card_type in general_types:
        column = []
        column.append(card_type)
        cards = general_map[card_type]
        analysis = analyze.run_general_analyses(cards, full_deck=deck)
        column.extend(analysis)
        general_analysis_block.append(column)

    special_analysis_block = []
    special_analysis_block.append([""] + analyze.get_special_analysis_ftn_names(deck.side))
    print "Special types:", special_types
    for special_type in special_types:
        column = []
        column.append(special_type)
        cards = special_map[special_type]
        analysis = analyze.run_special_analyses(cards, deck.side, full_deck=deck)
        column.extend(analysis)
        special_analysis_block.append(column)

    analysis_blocks.append({'title': "General Analysis", 'table': general_analysis_block})
    analysis_blocks.append({'title': special_table_title, 'table': special_analysis_block})
    for i in range(len(analysis_blocks)):
        block = analysis_blocks[i]['table']
        analysis_blocks[i]['table'] = zip(*block)

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
