import sqlite3
import json

row = [
    "card_id",
    "name",
    "side",
    "identity",
    "type",
    "subtype",

    "cost",
    "totalcost",
    "strength",
    "agendapoints",
    "text",
    "loyalty",
    "trash",
    "memory",
    "link",
    "unique",

    "errata",

    "set",
    "num",
    "count",

    "flavor",
    "illustrator",

    "rating",
    "GUID",
    "identitytop",
    "id",
    "img",
    "furl",
    "identitybottom",
    "numcomments",
]

connection = sqlite3.connect("cards.db")
c = connection.cursor()

# Create table
c.execute('''DROP TABLE IF EXISTS netrunner''')
c.execute('''CREATE TABLE IF NOT EXISTS netrunner
            (card_id integer primary key autoincrement, name text, side text, identity text, type text, subtype text, cost text, totalcost integer, strength text, agendapoints text, card_text text, loyalty text, trash text, memory text, link text, is_unique text, errata text, release_set text, num text, count text, flavor text, illustrator text, rating text, GUID text, identitytop text, id text, img text, furl text, identitybottom text, numcomments text)''')

# add initial cards

sides = ['corp', 'runner']
for side in sides:
    with open('{}_cards.json'.format(side)) as f:
        cards = json.loads(f.read())
    for card in cards:
        ordered_card_values = []
        for key in row:
            if key == "card_id":
                # empty value for primary key
                ordered_card_values.append(None)
                continue
            ordered_card_values.append(card[key])
        c.execute('INSERT INTO netrunner VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(side), ordered_card_values)

connection.commit()
connection.close()




row_dict = {
    "name": "Anonymous Tip", 
    "side": "Corp",
    "identity": "NBN", 
    "type": "Operation", 
    "subtype": "", 

    "cost": "0", 
    "totalcost": 1, 
    "strength": "", 
    "agendapoints": "0", 
    "text": "Draw 3 cards.", 
    "loyalty": "1", 
    "trash": "", 
    "memory": "", 
    "link": "0", 
    "unique": "No", 

    "errata": "", 

    "set": "Core", 
    "num": "83", 
    "count": "2", 

    "flavor": "&quot;Please stay connected. Priority transfer in progress. An operator will shortly verif-&quot;", 
    "illustrator": "Mike Nesbitt", 

    "rating": "3", 
    "GUID": "bc0f047c-01b1-427f-a439-d451eda01083", 
    "identitytop": "", 
    "id": "5", 
    "img": "", 
    "furl": "anonymous-tip-core", 
    "identitybottom": "", 
    "numcomments": "2", 
}
