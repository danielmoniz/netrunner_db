import deck_reader

# /////////////////////////////////////////////

def to_be_updated():
    all_cards = deck_reader.get_all_cards()


    print "="*10
    identity = deck['identity']
    print "Identity: {}".format(identity.text)
    print ""



    c.execute("DROP TABLE IF EXISTS netrunner_deck_cards")
    """
    c.execute('''CREATE TABLE IF NOT EXISTS netrunner_decks (
                deck_id integer primary key autoincrement, 
                 integer, 
                last_update text, 
                creation_date text,
                user integer''')
    """
    c.execute('''CREATE TABLE IF NOT EXISTS netrunner_deck_cards (
                deck_card_id integer primary key autoincrement, 
                deck_id integer, 
                card_id integer, 
                card_name text UNIQUE, 
                quantity integer, 
                date text, 
                user integer, 
                FOREIGN KEY(card_id) REFERENCES netrunner(card_id))''')

    for card in deck['main']:
        full_card = cards[card['name']]
        card_id = full_card[constants.CARD_ID]
        card_name = card['name']
        card_quantity = card['qty']
        now = str(datetime.datetime.now())
        c.execute('''INSERT INTO netrunner_deck_cards
                VALUES (?,?,?,?,?,?,?)''', (None, 1, card_id, card_name, card_quantity, now, 11))

    print '-'*20
    print len(c.execute('''SELECT * FROM netrunner''').fetchall())
    print len(c.execute('''SELECT * FROM netrunner_deck_cards''').fetchall())
    print c.execute('''SELECT card_name, quantity FROM netrunner_deck_cards as dc INNER JOIN netrunner AS n ON dc.card_id=n.card_id''').fetchall()

    connection.close()
    exit()


    for card in deck:
        full_card = cards[card.text]
        card_type = full_card[constants.TYPE]
        print "{} (x{}), type: {}".format(card.text, card.attrib['qty'], card_type)

    print "="*10
    print ""

    for card in deck:
        full_card = cards[card.text]
        card_type = full_card[constants.TYPE]
        card_subtype = full_card[constants.SUBTYPE]
