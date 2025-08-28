from Classes.Card import Card

class Player:
    def __init__(self, name, aces_low=False):
        self.name = name
        self.hand = []
        self.aces_low = aces_low

    def __str__(self):
        return "Player {} has {} cards: {}".format(
            self.name, len(self.hand), ", ".join(str(c) for c in self.hand)
        )

    def __len__(self):
        return len(self.hand)

    def draw_from_deck(self, deck, trump_suit=None, good_prob=0.0):
        if good_prob != 0.0:
            self.hand.extend(deck.deal_biased(len(self.hand), good_prob))
        else:
            self.hand.extend(deck.deal(len(self.hand)))
        self.sort_hand(trump_suit)

    def sort_hand(self, trump_suit):
        def card_sort_key(card):
            is_trump = (card.suit == trump_suit)
            rank_value = Card.rank_values[card.rank]
            return is_trump, rank_value

        self.hand.sort(key=card_sort_key)

    def lowest_trump_card(self, trump):
        trump_cards = [card for card in self.hand if card.suit == trump]
        if not trump_cards:
            return None
        return min(trump_cards, key=lambda card: Card.rank_values[card.rank])

    def total21(self):
        total = 0
        aces = 0
        for c in self.hand:
            pts = Card.points21_map[c.rank]
            if c.rank == 'A':
                aces += 1
            total += pts

        if self.aces_low:
            while total > 21 and aces > 0:
                total -= 10
                aces -= 1

        return total

    def is_bust21(self):
        return self.total21() > 21

    def is_natural21(self):
        return len(self.hand) == 2 and self.total21() == 21