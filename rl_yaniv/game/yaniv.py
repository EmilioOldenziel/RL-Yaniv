from typing import List, Optional
from collections import OrderedDict

from rl_yaniv.game.actions import (Action, EndTurn, PickupDeckCard,
                                   PickupPileTopCard, ThrowCard, CallYaniv)
from rl_yaniv.game.player import Player
from rl_yaniv.game.yaniv_round import YanivRound


class Yaniv:

    SUIT_LIST: List[str] = ['S', 'H', 'D', 'C']
    RANK_LIST:  List[str]= ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    PUNISHMENT_SCORE: int = 30
    MAX_HALVATION_SCORE: int = 100

    def __init__(self, num_players: int=4) -> None:

        self._num_players: int = num_players
        self.players: OrderedDict[int, Player] = OrderedDict()
        
        self.yaniv_round: Optional[YanivRound] = None
        self.last_round_winner: Optional[int] = None

    def reset(self) -> None:
        self.players = OrderedDict((player_id, Player(player_id)) for player_id in range(self._num_players))
        self.last_round_winner = None

        self.reset_round()

    def reset_round(self) -> None:
        self.yaniv_round = YanivRound(self.players, self.last_round_winner)
        self.yaniv_round.deal()
        self.yaniv_round.start()

    def step(self, action: Action):

        if isinstance(action, PickupDeckCard):
            self.yaniv_round.draw_deck_card()

        if isinstance(action, PickupPileTopCard):
            self.yaniv_round.pickup_pile_top_card()

        if isinstance(action, ThrowCard):
            self.yaniv_round.throw_card(card_index=action.card_index)

        if isinstance(action, CallYaniv):
            winner, *losers = self.yaniv_round.yaniv()
            winner_id, _ = winner
            current_player = self.get_current_player()
            if winner_id != current_player.player_id:
                current_player.game_score += self.PUNISHMENT_SCORE

            for player_id, points in losers:
                # current player was already punished
                if player_id == current_player.player_id:
                    continue
                self.players[player_id].game_score += points

            self.last_round_winner = winner_id
            self.reset_round()

        if isinstance(action, EndTurn):
            self.yaniv_round.end_player_turn()

    def get_current_player(self) -> int:
        return self.players[self.yaniv_round._current_player_id]

    def get_num_players(self) -> int:
        return self._num_players

    def is_over(self) -> bool:
        return any([player.game_score > self.MAX_HALVATION_SCORE for _, player in self.players.items()])
