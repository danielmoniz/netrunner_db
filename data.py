import collections


def get_subtypes(cards, mandatory_subtypes):
    card_subtypes = list(set(get_list_of_attr("subtype", cards)))
    card_subtypes_set = set()
    for card_subtypes_str in card_subtypes:
        current_subtypes = parse_subtype(card_subtypes_str)
        card_subtypes_set.update(current_subtypes)
    card_subtypes_set.difference_update(mandatory_subtypes)
    card_subtypes = mandatory_subtypes + list(card_subtypes_set)
    return card_subtypes

def average_over_attr(attr, deck, average="mean", decimal_places=2, unique=False, convert_type=None):
    if average == "median":
        raise NotImplementedError
    if not convert_type:
        convert_type = float
    if average == "mean":
        convert_type = float
    if not len(deck):
        return "/"
    attr_list = get_list_of_attr(attr, deck, unique=unique, convert_type=convert_type)
    if average == "mean":
        mean = sum(attr_list) / total_cards_in_list(deck)
        return round(mean, decimal_places)
    elif average == "mode":
        return collections.Counter.attr_list.most_common(1)

def total_cards_in_list(cards):
    """Note that 'unique' is set to true for summing the 'quantity' attribute.
    If it wasn't, cards would be double- and triple-counted.
    """
    return sum_over_attr('quantity', cards, unique=True, convert_type=int)

def sum_over_attr(attr, deck, unique=False, convert_type=None):
    if not convert_type:
        convert_type = float
    attr_list = get_list_of_attr(attr, deck, unique=unique, convert_type=convert_type)
    return sum(attr_list)

def get_list_of_attr(attr, deck, unique=False, convert_type=None):
    if not convert_type:
        convert_type = unicode
    attr_list = []
    for card in deck:
        attr_value = getattr(card, attr)
        if convert_type:
            try:
                attr_value = convert_type(attr_value)
            except ValueError as e:
                if attr_value.lower() == 'x':
                    continue
                raise e
            if unique:
                attr_list.append(attr_value)
            else:
                for i in range(card.quantity):
                    attr_list.append(attr_value)
    return attr_list

def get_actions(deck):
    actions = []
    for card in deck:
        actions.append(get_number_of_actions(card))
    return actions

def get_number_of_actions(card):
    if card.type.lower() == 'identity':
        return (0, 0)
    actions = 1 # one action to play card
    subtypes = parse_subtype(card.subtype)
    if "double" in subtypes:
        actions += 1
    if "priority" in subtypes:
        actions -= 1
    if card.type.lower() == "agenda":
        actions += int(card.cost)

    actions_with_draw = actions + 1
    return actions, actions_with_draw

def get_icebreakers(deck):
    return get_cards_of_subtype('icebreaker', deck)

def get_ice(deck):
    return get_cards_of_type('ice', deck)


def get_ai(deck):
    return get_cards_of_subtype('ai', deck)


"""
def get_cards_with_attr_less_than(attr, attr_value, deck):
    return get_cards_of_attr(attr, float(attr_value), 
"""


def get_attr_conversion(comparison_operator):
    """Default comparison is equality.
    Sets the attribute conversion to str or float, depending on the comparison 
    operator. This is because equality will always work with strings, but 
    numerical comparisons might require a numerical data type for proper 
    comparison.
    """
    if not comparison_operator:
        comparison_operator = lambda x,y: x == y
        attr_convert = unicode
    else:
        attr_convert = float
    return attr_convert, comparison_operator

def get_cards_of_attr(attr, attr_value, deck, compare=None):
    """Note that the default comparison operator is equality.
    This should NOT be specified in a parameter if equality is desired.
    """
    attr_convert, compare = get_attr_conversion(compare)
    cards = []
    for card in deck:
        card_attr_value = getattr(card, attr).lower()
        if card_attr_value in ("", "-"):
            continue
        if card_attr_value.lower() == 'x':
            cards.append(card)
            continue
        try:
            card_attr_value = attr_convert(card_attr_value)
            attr_value = attr_convert(attr_value)
        except ValueError as e:
            print "VALUE ERROR"
            print card, repr(attr_value), repr(card_attr_value)
            print str(e)
            return

        if isinstance(attr_value, basestring):
            attr_value = attr_value.lower()
        if isinstance(card_attr_value, basestring):
            card_attr_value = card_attr_value.lower()
        if attr == 'subtype':
            subtypes = parse_subtype(card_attr_value)
            if attr_value in subtypes:
                cards.append(card)
            continue
        if compare(card_attr_value, attr_value):
            cards.append(card)
    return cards


def get_cards_of_type(card_type, deck):
    return get_cards_of_attr('type', card_type, deck)

def parse_subtype(subtype_text, lower=False):
    if lower:
        subtype_text = subtype_text.lower()
    subtypes = subtype_text.split(' - ')
    return subtypes


def get_cards_of_subtype(subtype, deck):
    return get_cards_of_attr('subtype', subtype, deck)


def find_cards_with_exact_text(text, deck):
    cards = []
    for card in deck:
        if exact_match_is_in_text(text, card.text):
            cards.append(card)
    return cards


def find_cards_with_all_words(text, deck):
    """Takes space-separated text."""
    cards = []
    words = text.split(' ')
    for card in deck:
        words_in_text = all_words_are_in_text(words, card.text)
        if words_in_text:
            cards.append(card)
    return cards


def advanced_text_search(deck, exact_text=None, mandatory_words=None, partial_words=None):
    if not exact_text and not mandatory_words and not partial_match_words:
        return deck
    cards = []
    current_card_set = deck[:]
    if exact_text:
        for text in exact_text:
            for card in current_card_set[:]:
                if not exact_match_is_in_text(text, card.text):
                    current_card_set.remove(card)
    if mandatory_words:
        for card in current_card_set[:]:
            if not all_words_are_in_text(mandatory_words, card.text):
                current_card_set.remove(card)
    if partial_words:
        for card in current_card_set[:]:
            if not one_word_is_in_text(partial_words, card.text):
                current_card_set.remove(card)
    return current_card_set



def one_word_is_in_text(words, text):
    for word in words:
        if word.strip().lower() in text.lower():
            return True
    return False


def all_words_are_in_text(words, text):
    words_in_text = True
    for word in words:
        if word.strip().lower() not in text.lower():
            words_in_text = False
    return words_in_text


def exact_match_is_in_text(search, text):
    if search.lower() in text.lower():
        return True
    return False


def count_types(deck):
    types_in_deck = {}
    for card in deck:
        card_type = card.type
        try:
            types_in_deck[card.type] += card.quantity
        except KeyError:
            types_in_deck[card.type] = card.quantity
    type_count = [(key, value) for key, value in types_in_deck.iteritems()]
    type_count.sort(key=lambda tup: tup[1], reverse=True)
    return type_count


def count_subtypes(deck):
    subtypes_in_deck = {}
    for card in deck:
        if not card.subtype:
            continue
        subtypes = card.subtype.split(' - ')
        for subtype in subtypes:
            try:
                subtypes_in_deck[subtype] += card.quantity
            except KeyError:
                subtypes_in_deck[subtype] = card.quantity
    subtype_count = [(key, value) for key, value in subtypes_in_deck.iteritems()]
    subtype_count.sort(key=lambda tup: tup[1], reverse=True)
    return subtype_count
