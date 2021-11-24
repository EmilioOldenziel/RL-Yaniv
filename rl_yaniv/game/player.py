from typing import List

from rl_yaniv.game.card import Card


class Player():
    
    def __init__(self, player_id) -> None:
        self.player_id = player_id
        self.cards: List[Card] = []
        self.game_score: int = 0

    def get_points(self) -> int:
        return sum([card.points for card in self.hand_cards])

    def add_card(self, card: Card) -> None:
        self.cards.append(card)
