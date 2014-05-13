import data

class Card(object):

    def __init__(self, basic_card):
        self.name = basic_card

    def __str__(self):
        return_str = ""
        return_str += self.name
        num_tabs =  (3 - len(self.name) / 8) + 2
        """
        if hasattr(self, "type"):
            return_str += "\t" * num_tabs + "({})".format(self.type)
        """
        if hasattr(self, "quantity"):
            return_str += " x{}".format(self.quantity)
        return return_str

class DetailedCard(Card):
    def __init__(self, card):
        # find a way to test for being iterable and not a dict

        if not isinstance(card, dict) and not isinstance(card, Card):
            self.card_id = card[CARD_ID]
            self.name = unicode(card[NAME])
            self.side = card[SIDE]
            self.identity = card[IDENTITY]
            self.type = card[TYPE]
            self.subtype = card[SUBTYPE]
            self.cost = card[COST]
            self.totalcost = card[TOTALCOST]
            self.strength = card[STRENGTH]
            self.agendapoints = card[AGENDAPOINTS]
            self.text = card[TEXT]
            self.loyalty = card[LOYALTY]
            self.trash = card[TRASH]
            self.memory = card[MEMORY]
            self.link = card[LINK]
            self.unique = card[UNIQUE]
            self.errata = card[ERRATA]
            self.set = card[SET]
            self.num = card[NUM]
            self.count = card[COUNT]
            self.flavor = card[FLAVOR]
            self.illustrator = card[ILLUSTRATOR]
            self.rating = card[RATING]
            self.guid = card[GUID]
            self.identitytop = card[IDENTITYTOP]
            self.id = card[ID]
            self.img = card[IMG]
            self.furl = card[FURL]
            self.identitybottom = card[IDENTITYBOTTOM]
            self.numcomments = card[NUMCOMMENTS]
            if card[TYPE] == "identity":
                print "CREATED REGULAR CARD USING LIST OR TUPLE"

        elif isinstance(card, dict):
            self.card_id = card["card_id"]
            self.name = unicode(card["name"], "utf8")
            self.side = card["side"]
            self.identity = card["identity"]
            self.type = card["type"]
            self.subtype = card["subtype"]
            self.cost = card["cost"]
            self.totalcost = card["totalcost"]
            self.strength = card["strength"]
            self.agendapoints = card["agendapoints"]
            self.text = card["text"]
            self.loyalty = card["loyalty"]
            self.trash = card["trash"]
            self.memory = card["memory"]
            self.link = card["link"]
            self.unique = card["unique"]
            self.errata = card["errata"]
            self.set = card["set"]
            self.num = card["num"]
            self.count = card["count"]
            self.flavor = card["flavor"]
            self.illustrator = card["illustrator"]
            self.rating = card["rating"]
            self.guid = card["guid"]
            self.identitytop = card["identitytop"]
            self.id = card["id"]
            self.img = card["img"]
            self.furl = card["furl"]
            self.identitybottom = card["identitybottom"]
            self.numcomments = card["numcomments"]
            if card['type'] == "identity":
                print "CREATED CARD USING DICT"

        elif isinstance(card, Card):
            self.card_id = card.card_id
            self.name = unicode(card.name)
            self.side = card.side
            self.identity = card.identity
            self.type = card.type
            self.subtype = card.subtype
            self.cost = card.cost
            self.totalcost = card.totalcost
            self.strength = card.strength
            self.agendapoints = card.agendapoints
            self.text = card.text
            self.loyalty = card.loyalty
            self.trash = card.trash
            self.memory = card.memory
            self.link = card.link
            self.unique = card.unique
            self.errata = card.errata
            self.set = card.set
            self.num = card.num
            self.count = card.count
            self.flavor = card.flavor
            self.illustrator = card.illustrator
            self.rating = card.rating
            self.guid = card.guid
            self.identitytop = card.identitytop
            self.id = card.id
            self.img = card.img
            self.furl = card.furl
            self.identitybottom = card.identitybottom
            self.numcomments = card.numcomments
            if card.type == "identity":
                print "CREATED NEW CARD BASED ON OLD CARD"

        else:
            print "Failed to properly make card!"
            return False
        
        self.actions, self.actions_with_draw = data.get_card_actions(self)
        self.income = data.get_income(self)
        self.net_cost, self.net_cost_with_draw = data.get_net_cost(self)
        if self.name == 'Blackguard':
            print '*'*20
            print self.name
            print data.get_generated_memory(self)
            print '*'*20
        self.memory_added = data.get_generated_memory(self)
        self.quantity = 1



CARD_ID = 0
NAME = 1
SIDE = 2
IDENTITY = 3
TYPE = 4
SUBTYPE = 5
COST = 6
TOTALCOST = 7
STRENGTH = 8
AGENDAPOINTS = 9
TEXT = 10
LOYALTY = 11
TRASH = 12
MEMORY = 13
LINK = 14
UNIQUE = 15
ERRATA = 16
SET = 17
NUM = 18
COUNT = 19
FLAVOR = 20
ILLUSTRATOR = 21
RATING = 22
GUID = 23
IDENTITYTOP = 24
ID = 25
IMG = 26
FURL = 27
IDENTITYBOTTOM = 28
NUMCOMMENTS = 29
