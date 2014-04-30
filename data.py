

def get_icebreakers(deck):
    return get_cards_of_subtype('icebreaker', deck)


def get_ai(deck):
    return get_cards_of_subtype('ai', deck)


def get_cards_of_type(card_type, deck):
    cards = []
    for card in deck.cards:
        if card.type.lower() == card_type.lower():
            print "{}: {}".format(card.type, card.name)
            cards.append(card)
    return cards


def get_cards_of_subtype(subtype, deck):
    cards = []
    for card in deck.cards:
        subtypes = card.subtype.lower()
        subtypes = subtypes.split(' - ')
        if subtype in subtypes:
            cards.append(card)
            print "{}: {}".format(subtype, card.name)
    return cards


def find_cards_with_exact_text(text, deck):
    cards = []
    for card in deck.cards:
        if exact_match_is_in_text(text, card.text):
            print card.name
            cards.append(card)
    return cards


def find_cards_with_all_words(text, deck):
    """Takes space-separated text."""
    print '*'*10
    print text
    print text.lower().split(' ')
    cards = []
    words = text.split(' ')
    for card in deck.cards:
        words_in_text = all_words_are_in_text(words, card.text)
        if words_in_text:
            print card.name
            cards.append(card)
    return cards


def advanced_text_search(deck, exact_text=None, mandatory_words=None, partial_words=None):
    if not exact_text and not mandatory_words and not partial_match_words:
        return deck.cards
    cards = []
    current_card_set = deck.cards
    if exact_text:
        for card in current_card_set[:]:
            if not exact_match_is_in_text(exact_text, card.text):
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
    for card in deck.cards:
        card_type = card.type
        try:
            types_in_deck[card.type] += card.quantity
        except KeyError:
            types_in_deck[card.type] = card.quantity
    type_count = [(key, value) for key, value in types_in_deck.iteritems()]
    type_count.sort(key=lambda tup: tup[1], reverse=True)
    print type_count
    return type_count


def count_subtypes(deck):
    subtypes_in_deck = {}
    for card in deck.cards:
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
