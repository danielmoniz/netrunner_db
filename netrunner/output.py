def print_single_line_card_list(cards):
    if not cards:
        return "No cards"
    card_str = "{} x{}".format(cards[0].name, str(cards[0].quantity))
    for card in cards[1:]:
        card_str += ", {} x{}".format(card.name, card.quantity)
    return card_str
