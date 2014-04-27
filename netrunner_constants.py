# constants representing Netrunner card attributes in a database table
# These will be used for referring to elements of a tuple.

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

card_attr_map = {
    "card_id": CARD_ID,
    "name": NAME,
    "side": SIDE,
    "identity": IDENTITY,
    "type": TYPE,
    "subtype": SUBTYPE,
    "cost": COST,
    "totalcost": TOTALCOST,
    "strength": STRENGTH,
    "agendapoints": AGENDAPOINTS,
    "text": TEXT,
    "loyalty": LOYALTY,
    "trash": TRASH,
    "memory": MEMORY,
    "link": LINK,
    "unique": UNIQUE,
    "errata": ERRATA,
    "set": SET,
    "num": NUM,
    "count": COUNT,
    "flavor": FLAVOR,
    "illustrator": ILLUSTRATOR,
    "rating": RATING,
    "guid": GUID,
    "identitytop": IDENTITYTOP,
    "id": ID,
    "img": IMG,
    "furl": FURL,
    "identitybottom": IDENTITYBOTTOM,
    "numcomments": NUMCOMMENTS,
}
