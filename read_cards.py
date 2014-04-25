import json
import HTMLParser

html_parser = HTMLParser.HTMLParser()
with open('corp_cards.json') as f:
    corp_cards = html_parser.unescape(json.loads(f.read()))

with open('runner_cards.json') as f:
    runner_cards = json.loads(f.read())

print "{} runner cards total: {}".format(len(runner_cards), '-'*10)
print "{} corp cards total: {}".format(len(corp_cards), '-'*10)

print "Runner cards: -----"
for card in runner_cards[:10]:
    print card['name']
print ""
print "Corp cards: -----"
for card in corp_cards[:10]:
    print card['name']

print "{} runner cards total: {}".format(len(runner_cards), '-'*10)
print "{} corp cards total: {}".format(len(corp_cards), '-'*10)
print corp_cards[0].keys()

for card in corp_cards[:50]:
    attrs = ['type', 'identity', 'name']
    for attr in attrs:
        print "{},".format(card[attr]),
    print ""
