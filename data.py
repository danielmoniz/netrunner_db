import collections
import re

def sort_by_attr(attr, cards, convert_type=None, descending=True, secondary_attr=None):
    if not convert_type:
        convert_type = str
    cards = cards[:]
    cards = get_cards_with_attr(attr, cards, data_format=int)
    if secondary_attr:
        sorted_cards = sorted(cards, key=lambda card: (convert_type(getattr(card, attr)), 
            getattr(card, secondary_attr)), reverse=descending)
        return sorted_cards
    sorted_cards = sorted(cards, key=lambda card: convert_type(getattr(card, attr)), reverse=descending)
    return sorted_cards


def get_cards_with_attr(attr, cards, data_format):
    """Return a subset of cards that have a valid attribute of the given 
    data format.
    """
    valid_cards = []
    for card in cards:
        card_attr_value = getattr(card, attr)
        try:
            converted_attr = data_format(card_attr_value)
        except ValueError:
            continue
        valid_cards.append(card)
    return valid_cards


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
        return False
    attr_list = get_list_of_attr(attr, deck, unique=unique, convert_type=convert_type)
    if average == "mean":
        mean = sum(attr_list) / get_total_cards(deck)
        return round(mean, decimal_places)
    elif average == "mode":
        return collections.Counter.attr_list.most_common(1)

def get_total_cards(cards):
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
                # @TODO Check this - can we continue in all cases?
                else:
                    print "Attribute failed to convert:", attr, attr_value
                    continue
                raise e
            if unique:
                attr_list.append(attr_value)
            else:
                for i in range(card.quantity):
                    attr_list.append(attr_value)
    return attr_list

def get_money_making_cards(cards, instant=False):
    money_makers = advanced_text_search(
        cards,
        mandatory_words=["credit"],
        partial_words=["gain", "take"],
        same_sentence=True,
    )
    if instant:
        money_makers = get_cards_of_attr_in("type", ("operation", "event"), money_makers)
    return money_makers

def get_income(card):
    """Return income of card of text: "Gain X credit[s]."
    Returns the first instance of this text found in the card's text.
    NOTE: May not be instant. Eg. may be an asset, agenda, etc.
    """
    if hasattr(card, 'actions'):
        actions = card.actions
    else:
        actions = get_card_actions(card)
    sentences = get_sentences_from_text(card.text)
    card_matches = False
    for sentence in sentences:
        match = re.search('[Gg]ain ((\d)+) \[Credit', card.text)
        if match:
            income_size = match.groups()[0]
            return int(income_size)
    return 0

def get_net_cost(card):
    """Assume card has 'actions' and 'income' attributes.
    Also assume that 1 Click = 1 Credit.
    """
    if card.cost == "X":
        return ("X", "X+1")
    if card.cost == "":
        return ("", "")
    net_cost = int(card.cost) + card.actions - card.income
    net_cost_with_draw = net_cost + 1
    return net_cost, net_cost_with_draw
    

def get_total_actions(deck):
    actions = 0
    actions_with_draw = 0
    for card in deck:
        new_actions, new_actions_with_draw = get_card_actions(card, unique=False)
        actions += new_actions
        actions_with_draw += new_actions_with_draw
    return actions, actions_with_draw

def get_card_actions(card, unique=True):
    if card.type.lower() == 'identity':
        return ("", "")
    actions = 1 # one action to play card
    subtypes = parse_subtype(card.subtype, lower=True)
    if "double" in subtypes:
        actions += 1
    """
    if "priority" in subtypes:
        actions -= 1
    """
    if is_instant(card):
        match = re.search('[Gg]ain(( \[Click\])+)', card.text)
        if match:
            num_clicks = match.groups()[0].count('Click')
            actions -= num_clicks
    if card.type.lower() == "agenda":
        actions += int(card.cost)
    if 'run' in subtypes:
        if ("instead of accessing cards" not in card.text.lower()
            and "you cannot access any cards" not in card.text.lower()):
            actions -= 1

    actions_with_draw = actions + 1
    if not unique:
        return actions * int(card.quantity), actions_with_draw * int(card.quantity)
    return actions, actions_with_draw

def is_instant(card):
    return card.type in ("Event", "Operation")

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

def get_cards_of_attr_in(attr, attr_value, deck):
    cards = get_cards_of_attr(attr, attr_value, deck, compare=lambda x, y: x in y, convert_type=unicode)
    return cards

def get_cards_of_attr_not_in(attr, attr_value, deck):
    cards = get_cards_of_attr(attr, attr_value, deck, compare=lambda x, y: x not in y, convert_type=unicode)
    return cards

def get_cards_of_attr(attr, attr_value, deck, compare=None, convert_type=None):
    """Note that the default comparison operator is equality.
    This should NOT be specified in a parameter if equality is desired.
    """
    new_convert_type, new_compare = get_attr_conversion(compare)
    if not convert_type:
        convert_type = new_convert_type
    if not compare:
        compare = new_compare
    cards = []
    for card in deck:
        try:
            card_attr_value = getattr(card, attr)
        except AttributeError:
            print 'attribute error'
            continue
        if isinstance(card_attr_value, basestring):
            card_attr_value = card_attr_value.lower()
        if card_attr_value in ("", "-"):
            continue
        if card_attr_value == 'x':
            cards.append(card)
            continue
        try:
            attr_value = convert_type(attr_value)
        except ValueError:
            print "Value to match cannot be properly converted."
            raise e
        try:
            card_attr_value = convert_type(card_attr_value)
        except TypeError:
            print 'type error: skipping'
            print card_attr_value, type(card_attr_value)
            print attr_value, type(attr_value)
            continue
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


def advanced_text_search(text, exact_text=None, mandatory_words=None, partial_words=None):
    if not exact_text and not mandatory_words and not partial_match_words:
        return True
    if exact_text:
        exact_text_matches = False
        for temp_text in exact_text:
            if exact_match_is_in_text(temp_text, text):
                exact_text_matches = True
                break
        if not exact_text_matches:
            return False
    if mandatory_words:
        if not all_words_are_in_text(mandatory_words, text):
            return False
    if partial_words:
        if not one_word_is_in_text(partial_words, text):
            return False

    # if we've made it this far, the text must be valid
    return True


def advanced_deck_search(deck, same_sentence=False, **kwargs):
    valid_cards = []
    for card in deck:
        if not same_sentence:
            sentences = [card.text]
        else:
            sentences = get_sentences_from_text(card.text)
        for sentence in sentences:
            sentence_has_match = advanced_text_search(sentence, **kwargs)
            if sentence_has_match:
                valid_cards.append(card)
                break
    return valid_cards


def get_sentences_from_text(text):
    return text.split('.')


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

def shuffle_deck(deck):
    import random
    return random.shuffle(deck[:])
