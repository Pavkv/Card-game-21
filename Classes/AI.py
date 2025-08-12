from Classes.Player import Player


class AI(Player):
    def decide(self, dealer_upcard):
        if self.total21() < 17:
            return 'h'
        return 's'