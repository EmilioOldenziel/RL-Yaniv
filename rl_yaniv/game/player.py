from collections import OrderedDict

from rl_yaniv.game.card import Card


class Player():
    
    def __init__(self, player_id) -> None:
        self.player_id = player_id
        self.cards: OrderedDict[str, Card] = OrderedDict()
        self.game_score: int = 0

    def add_card(self, card: Card) -> None:
        self.cards[card.get_index()] = card

    def get_points(self) -> int:
        return sum([card.points for card in self.cards.values()])
