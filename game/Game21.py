# coding=utf-8
import random

from Classes.Deck import Deck
from Classes.Player import Player
from Classes.AI import AI

class Game21:
    def __init__(self, player_name="Вы", opponent_name="Противник", biased_draw=None):
        self.deck = Deck()
        self.player = Player(player_name)
        self.opponent = AI(opponent_name)
        self.first_player_index = None
        self.state = "idle"
        self.result = None

        self.bias = {"player": 0.0, "opponent": 0.0}
        if biased_draw:
            who, prob = biased_draw
            prob = float(prob)
            if who == "player":
                self.bias["player"] = prob
            elif who == "opponent":
                self.bias["opponent"] = prob

    # ---------- internals ----------
    def _clear_hands(self):
        self.player.hand = []
        self.opponent.hand = []

    def _maybe_refresh_deck(self):
        if len(self.deck.cards) < 10:
            self.deck = Deck()

    def _draw_one(self, who):
        prob = self.bias["player"] if who is self.player else self.bias["opponent"]
        c = self.deck.draw_with_bias(prob) if prob > 0.0 else self.deck.draw_top()
        if c is not None:
            who.hand.append(c)
        return c

    def _deal_two_each(self):
        for _ in range(2):
            self._draw_one(self.player)
            self._draw_one(self.opponent)

    def _instant_check(self):
        if self.player.total21() == 21:
            self.finalize(winner=self.player)
            return True
        if self.opponent.total21() == 21:
            self.finalize(winner=self.opponent)
            return True
        return False

    def start_round(self):
        self._maybe_refresh_deck()
        self._clear_hands()
        self.result = None
        self.state = "initial_deal"
        self._deal_two_each()
        if self._instant_check():
            return

        if self.first_player_index is None:
            self.first_player_index = random.choice([0, 1])

        order0 = self.player if self.first_player_index == 0 else self.opponent
        self.state = "player_turn" if order0 is self.player else "opponent_turn"

    def player_pass(self):
        if self.state == "player_turn" and self.result is None:
            self.state = "opponent_turn"

    def opponent_turn(self):
        return self.opponent.decide(seen_cards=list(self.opponent.hand), opponent_total=self.player.total21())

    def finalize(self, winner=None):
        if winner is self.player:
            self.result = self.player.name
        elif winner is self.opponent:
            self.result = self.opponent.name
        else:
            ht, at = self.player.total21(), self.opponent.total21()
            hb, ab = self.player.is_bust21(), self.opponent.is_bust21()
            if hb and ab:
                self.result = "draw"
            elif hb:
                self.result = self.opponent.name
            elif ab:
                self.result = self.player.name
            elif ht == at:
                self.result = "draw"
            elif ht > at:
                self.result = self.player.name
            else:
                self.result = self.opponent.name
        # Always end in the terminal state your loop checks
        self.state = "result"
