import card as card_module


def get_full_card_list(cards):
    all_cards = []
    for card in cards:
        for i in range(card.quantity):
            new_card = card_module.DetailedCard(card)
            all_cards.append(new_card)
    return all_cards


def condense_card_list(cards):
    """Look for duplicate cards and instead return a list with quantities attached to unique cards.
    """
    condensed_cards = []
    card_count = {}
    for card in cards:
        try:
            card_count[card.name] += card.quantity
        except KeyError:
            card_count[card.name] = card.quantity

    for name, quantity in card_count.iteritems():
        card = filter(lambda card: card.name == name, cards)[0]
        card.quantity = quantity
        condensed_cards.append(card)
    return condensed_cards
