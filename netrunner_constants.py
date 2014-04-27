# constants representing Netrunner card attributes in a database table
# These will be used for referring to elements of a tuple.

NAME = 0
SIDE = 1
IDENTITY = 2
TYPE = 3
SUBTYPE = 4
COST = 5
TOTALCOST = 6
STRENGTH = 7
AGENDAPOINTS = 8
TEXT = 9
LOYALTY = 10
TRASH = 11
MEMORY = 12
LINK = 13
UNIQUE = 14
ERRATA = 15
SET = 16
NUM = 17
COUNT = 18
FLAVOR = 19
ILLUSTRATOR = 20
RATING = 21
GUID = 22
IDENTITYTOP = 23
ID = 24
IMG = 25
FURL = 26
IDENTITYBOTTOM = 27
NUMCOMMENTS = 28

card_attr_map = {
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
