from random import randint
from typing import List, Optional

from rl_yaniv.game.card import YanivCard
from rl_yaniv.game.deck import Deck
from rl_yaniv.game.player import Player


class Yaniv:

    SUIT_LIST: List[str] = ['S', 'H', 'D', 'C']
    RANK_LIST:  List[str]= ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    YANIV_TARGET_POINTS: int = 5  # below or equal can call Yaniv

    def __init__(self, num_players: int=4) -> None:

        self.max_halvation_score = 200  # # if player reaches a score of 200 its points are reduced/halved to 100.
        self.midway_halvation_score = 100  # if player reaches a score of 100 its points are reduced/halved to 50.
        self.punishment_score = 30  # if player called Yaniv but did not have the lowest score, get 30 punishment extra score.

        self._num_players: int = num_players

        self.players: List[Player] = [Player(player_id) for player_id in range(num_players)]
        self.last_round_winner: Optional[int] = None

        self.deck: Deck = Deck.init_54_deck()
        self.dump_pile: List[YanivCard] = []

        self._current_player: Optional[int] = None  # starting player is not selected yet

    def deal(self) -> None:
        for _ in range(5):
            for player in self.players:
                player.add_card(self.deck.pop_from_deck())

    def start(self) -> None:
        
        # put first card on the dump pile
        self.dump_pile.append(self.deck.pop_from_deck())

        # select starting player
        if self.last_round_winner is not None:
            self.player_turn = self.last_round_winner
        else:
            self.player_turn = randint(0, self._num_players - 1)

    def end_turn_player(self) -> None:
        NotImplementedError

    def pickup_pile_top_card(self) -> None:
        NotImplementedError

    def throw_set(self) -> None:
        NotImplementedError

    def throw_sequence(self) -> None:
        NotImplementedError

    def yaniv(self) -> None:
        NotImplementedError

    def get_current_player(self) -> int:
        return self._current_player

    def get_num_players(self) -> int:
        return self._num_players

    def is_over(self) -> bool:
        return any([player.score > self.max_halvation_score for player in self.players])
