import json

import bs4

def pretty(text):
    return bs4.BeautifulSoup(text)


with open('corp_cards.json') as f:
    corp_cards = json.loads(f.read())

with open('runner_cards.json') as f:
    runner_cards = json.loads(f.read())

if runner_cards:
    print "Runner cards: -----"
    for card in runner_cards[:10]:
        print pretty(card['name'])
    print ""

if corp_cards:
    print "Corp cards: -----"
    for card in corp_cards[:10]:
        print pretty(card['name'])

"""
if corp_cards:
    print corp_cards[0].keys()
"""

if corp_cards:
    for card in corp_cards[:50]:
        attrs = ['type', 'identity', 'name']
        for attr in attrs:
            print pretty("{},".format(card[attr])),
        print ""

print ""
if runner_cards:
    print "{} runner cards total".format(len(runner_cards), '-'*10)
if corp_cards:
    print "{} corp cards total".format(len(corp_cards), '-'*10)
