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

    def __init__(self, players: List[Player]) -> None:

        self._num_players: int = len(players)
        self.players: OrderedDict[int, Player] = OrderedDict((player.player_id, player) for player in players)
        
        self.yaniv_round: Optional[YanivRound] = None
        self.last_round_winner: Optional[int] = None

        self.num_rounds = 0

    def reset(self) -> None:
        for player in self.players.values():
            player.reset()
        self.last_round_winner = None

        self.reset_round()

    def reset_player_cards(self):
        for player in self.players.values():
            player.reset_cards()

    def reset_round(self) -> None:
        self.reset_player_cards()
        self.yaniv_round = YanivRound(self.players, self.last_round_winner)
        self.yaniv_round.deal()
        self.yaniv_round.start()

    def step(self, action: Action):

        if isinstance(action, PickupDeckCard):
            self.yaniv_round.draw_deck_card()
            self.yaniv_round.end_player_turn()

        elif isinstance(action, PickupPileTopCard):
            self.yaniv_round.pickup_pile_top_card()
            self.yaniv_round.end_player_turn()

        elif isinstance(action, ThrowCard):
            self.yaniv_round.throw_card(card_index=action.card_index)

        elif isinstance(action, CallYaniv):
            winner, *losers = self.yaniv_round.yaniv()
            winner_id, _ = winner
            current_player = self.get_current_player()

            # punish player that called yaniv for asaf situation
            if winner_id != current_player.player_id:
                current_player.game_score += self.PUNISHMENT_SCORE

            for player_id, points in losers:
                # current player was already punished
                if player_id == current_player.player_id:
                    continue
                self.players[player_id].game_score += points

            self.last_round_winner = winner_id
            self.reset_round()

    def get_current_player(self) -> Player:
        return self.players[self.yaniv_round._current_player_id]

    def get_player(self, player_id: int) -> Optional[Player]:
        return self.players.get(player_id)

    def get_num_players(self) -> int:
        return self._num_players

    def is_over(self) -> bool:
        return any([player.game_score > self.MAX_HALVATION_SCORE for player in self.players.values()])
