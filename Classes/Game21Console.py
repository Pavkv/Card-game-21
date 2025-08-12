# coding=utf-8
import random
import sys

from Classes.Deck import Deck
from Classes.Player import Player
from Classes.AI import AI
from Classes.Dealer import Dealer


class Game21:
    def __init__(self, player_name="Вы", opponent_name="Противник", biased_draw=None):
        self.deck = Deck()
        self.human = Player(player_name)
        self.ai = AI(opponent_name)
        self.dealer = Dealer("Dealer")
        self.round_num = 0

    def _clear_hands(self):
        self.human.hand = []
        self.ai.hand = []
        self.dealer.hand = []

    def _maybe_refresh_deck(self):
        if len(self.deck.cards) < 10:
            self.deck = Deck()

    def _draw_one(self, player):
        c = self.deck.draw_top()
        if c is not None:
            player.hand.append(c)
        return c

    def _hand_str(self, p, hide_first=False):
        if hide_first and p.hand:
            return "[??] " + " ".join(str(c) for c in p.hand[1:])
        return " ".join(str(c) for c in p.hand)

    def _show_table(self, reveal_dealer=False, hide_players=False):
        print ""
        print "=== TABLE ==="
        print "Dealer: %s" % self._hand_str(self.dealer, hide_first=(not reveal_dealer))
        if hide_players:
            print "%s: %s  (total %d)" % (self.human.name, "[hidden]", self.human.total21())
            print "%s: %s  (total %d)" % (self.ai.name, "[hidden]", self.ai.total21())
        else:
            print "%s: %s  (total %d)" % (self.human.name, self._hand_str(self.human), self.human.total21())
            print "%s: %s  (total %d)" % (self.ai.name, self._hand_str(self.ai), self.ai.total21())
        print "=============\n"

    # ---------- dealing & turn order ----------
    def _initial_deal(self):
        order = [self.human, self.ai, self.dealer,
                 self.human, self.ai, self.dealer]
        for p in order:
            self._draw_one(p)

    def _random_turn_order(self):
        players = [self.human, self.ai]
        random.shuffle(players)
        return players

    # ---------- turns ----------
    def _human_turn(self, dealer_up):
        while True:
            if self.human.is_bust21() or self.human.is_natural21():
                return
            print "%s, your total is %d." % (self.human.name, self.human.total21())
            choice = raw_input("Hit or Pass? [h/p]: ").strip().lower()
            if choice == 'h':
                c = self._draw_one(self.human)
                print "You draw: %s (total %d)" % (c, self.human.total21())
                if self.human.is_bust21():
                    print "You bust at %d. (Outcome evaluated after dealer turn.)" % self.human.total21()
                    return
            elif choice == 'p':
                print "You pass at %d." % self.human.total21()
                return
            else:
                print "Please enter 'h' or 'p'."

    def _ai_turn(self, dealer_up):
        while not self.ai.is_bust21() and not self.ai.is_natural21():
            move = self.ai.decide(dealer_up)
            if move == 'h':
                c = self._draw_one(self.ai)
                print "AI hits: %s -> total %d" % (c, self.ai.total21())
            else:
                print "AI passes at %d." % self.ai.total21()
                break

    def _dealer_turn(self):
        print ""
        print "Dealer reveals hole card: %s" % self.dealer.hand[0]
        self._show_table(reveal_dealer=True)
        while True:
            move = self.dealer.decide()
            if move == 'h':
                c = self._draw_one(self.dealer)
                print "Dealer hits: %s -> total %d" % (c, self.dealer.total21())
                if self.dealer.is_bust21():
                    print "Dealer busts at %d." % self.dealer.total21()
                    break
            else:
                print "Dealer stands at %d." % self.dealer.total21()
                break

    # ---------- resolve per your rules ----------
    def _resolve_vs_dealer(self, player):
        pt = player.total21()
        pb = player.is_bust21()
        dt = self.dealer.total21()
        db = self.dealer.is_bust21()

        # Rule: if dealer busts → DRAW for players (even if player busted)
        if db:
            return "DRAW"

        # Dealer not bust:
        # Tie conditions:
        if pt == dt:
            return "DRAW"
        if pb and (not db) and self.dealer.total21() <= 21:
            # still might be "both busted" tie, but dealer isn't bust here, so not both
            return "LOSE"
        # If both busted (only possible if we changed rules, but honoring your tie clause):
        if pb and db:
            return "DRAW"

        if pb:
            return "LOSE"

        # Compare totals (closest to 21 wins)
        if pt > dt:
            return "WIN"
        else:
            return "LOSE"

    def _print_results(self):
        res_h = self._resolve_vs_dealer(self.human)
        res_a = self._resolve_vs_dealer(self.ai)
        print ""
        print "Results:"
        print "  You : %s" % res_h
        print "  AI  : %s" % res_a
        print ""

    # ---------- round driver ----------
    def play_round(self):
        self.round_num += 1
        print "\n==================== ROUND %d ====================" % self.round_num
        self._maybe_refresh_deck()
        self._clear_hands()
        self._initial_deal()

        # Show table with dealer upcard only
        self._show_table(reveal_dealer=False)

        dealer_up = self.dealer.hand[1]

        # Randomize who goes first
        order = self._random_turn_order()
        print "Turn order: %s -> %s" % (order[0].name, order[1].name)

        # Run player turns
        for p in order:
            if p is self.human:
                self._human_turn(dealer_up)
            else:
                self._ai_turn(dealer_up)

        # Dealer acts last
        self._dealer_turn()

        # Final table and results
        self._show_table(reveal_dealer=True)
        self._print_results()

def main():
    print "=== 21 (Durak 6..A) — You vs AI vs Dealer ==="
    print "Scoring: A=11, K=4, Q=3, J=2; 10..6 = pip. Dealer draws to 17."
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

if __name__ == "__main__":
    main()