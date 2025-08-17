# coding=utf-8
import random
import sys

from Classes.Deck import Deck
from Classes.Player import Player
from Classes.AI import AI


class Game21:
    def __init__(self, player_name="Вы", opponent_name="Противник", biased_draw=None):
        self.deck = Deck()
        self.human = Player(player_name)
        self.opponent = AI(opponent_name)
        self.round_num = 0
        self.first_player_index = None

        self.bias = {"player": 0.0, "opponent": 0.0}
        if biased_draw:
            who, prob = biased_draw
            if who == "player":
                self.bias["player"] = float(prob)
            elif who == "opponent":
                self.bias["opponent"] = float(prob)

    def _clear_hands(self):
        self.human.hand = []
        self.opponent.hand = []

    def _maybe_refresh_deck(self):
        if len(self.deck.cards) < 10:
            self.deck = Deck()

    def _draw_one(self, player):
        if player is self.human:
            prob = self.bias["player"]
        else:
            prob = self.bias["opponent"]

        if prob > 0.0:
            c = self.deck.draw_with_bias(prob)
        else:
            c = self.deck.draw_top()

        if c is not None:
            player.hand.append(c)
        return c

    def _hand_str(self, p, hide=False):
        if hide:
            return "[??] " + " ".join(str(c) for c in p.hand[1:])
        return " ".join(str(c) for c in p.hand)

    def _show_table(self, hide_opponent=True):
        print "\n=== TABLE ==="
        print "%s: %s  (total %d)" % (self.human.name, self._hand_str(self.human), self.human.total21())
        if hide_opponent:
            print "%s: %s  (total %d)" % (self.opponent.name, "[hidden]", self.opponent.total21())
        else:
            print "%s: %s  (total %d)" % (self.opponent.name, self._hand_str(self.opponent), self.opponent.total21())
        print "Bias (You/AI): %.0f%% / %.0f%%" % (self.bias["player"]*100, self.bias["opponent"]*100)
        print "=============\n"

    def _instant_win(self, winner):
        print "\nInstant WIN: %s reached 21!" % winner.name
        self._print_results(winner)
        return True

    def _initial_deal(self):
        for _ in range(2):
            self._draw_one(self.human)
            self._draw_one(self.opponent)

    def _human_turn(self):
        while True:
            total = self.human.total21()
            if total == 21:
                return self._instant_win(self.human)
            if self.human.is_bust21():
                print "You bust at %d!" % total
                return False

            choice = raw_input("Hit or Pass? [h/p]: ").strip().lower()
            if choice == 'h':
                c = self._draw_one(self.human)
                print "You draw: %s (total %d)" % (c, self.human.total21())
            elif choice == 'p':
                print "You pass at %d." % total
                return False
            else:
                print "Please enter 'h' or 'p'."

    def _opponent_turn(self):
        while True:
            total = self.opponent.total21()
            if total == 21:
                return self._instant_win(self.opponent)
            if self.opponent.is_bust21():
                print "AI busts at %d!" % total
                return False

            seen = list(self.opponent.hand)

            opponent_total = self.human.total21()
            move = self.opponent.decide(seen_cards=seen, opponent_total=opponent_total)

            if move == 'h':
                c = self._draw_one(self.opponent)
                print "AI hits: %s -> total %d" % (c, self.opponent.total21())
            else:
                print "AI passes at %d." % total
                return False

    def _print_results(self, winner=None):
        if winner is not None:
            if isinstance(winner, Player):
                if winner is self.human:
                    print "\nResults:\n  You : WIN\n  AI  : LOSE\n"
                else:
                    print "\nResults:\n  You : LOSE\n  AI  : WIN\n"
            return

        ht = self.human.total21()
        at = self.opponent.total21()
        hbust = self.human.is_bust21()
        abust = self.opponent.is_bust21()

        if hbust and abust:
            res_h, res_a = "DRAW", "DRAW"
        elif hbust:
            res_h, res_a = "LOSE", "WIN"
        elif abust:
            res_h, res_a = "WIN", "LOSE"
        elif ht == at:
            res_h, res_a = "DRAW", "DRAW"
        elif ht > at:
            res_h, res_a = "WIN", "LOSE"
        else:
            res_h, res_a = "LOSE", "WIN"

        print "\nResults:"
        print "  You : %s" % res_h
        print "  AI  : %s" % res_a
        print ""

    def play_round(self):
        self.round_num += 1
        print "\n==================== ROUND %d ====================" % self.round_num
        self._maybe_refresh_deck()
        self._clear_hands()
        self._initial_deal()
        self._show_table()

        if self.first_player_index is None:
            self.first_player_index = random.choice([0, 1])
        else:
            self.first_player_index = 1 - self.first_player_index
        players = [self.human, self.opponent]
        order = players[self.first_player_index:] + players[:self.first_player_index]
        print "Turn order: %s -> %s" % (order[0].name, order[1].name)

        # Turns
        for p in order:
            if p is self.human:
                if self._human_turn():
                    return
            else:
                if self._opponent_turn():
                    return

        self._show_table(hide_opponent=False)
        self._print_results()


def mopponentn():
    print "=== 21 (Durak 6..A) — You vs AI ==="
    print "Scoring: A=11, K=4, Q=3, J=2; 10..6 = pip."
    game = Game21()
    try:
        while True:
            game.play_round()
            ans = raw_input("Play another round? [Y/n]: ").strip().lower()
            if ans in ('n', 'q'):
                print "Goodbye!"
                break
    except KeyboardInterrupt:
        sys.exit("\n(Interrupted)")


if __name__ == "__mopponentn__":
    mopponentn()
