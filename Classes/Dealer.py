from Classes.Player import Player


class Dealer(Player):
    def decide(self):
        if self.total21() < 17:
            return 'h'
        return 's'