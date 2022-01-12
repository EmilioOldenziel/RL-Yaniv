from typing import Dict, List

import numpy as np
from gym import Env, spaces
from rl_yaniv.game.actions import (Action, CallYaniv, PickupDeckCard,
                                   PickupPileTopCard, ThrowCard, DoNothing)
from rl_yaniv.game.player import Player, RandomPlayer, RLPLayer
from rl_yaniv.game.yaniv import Yaniv


class YanivEnv(Env):
    
    def __init__(self, env_config=None) -> None:
        self.yaniv = Yaniv(players=[RLPLayer(player_id=0), RandomPlayer(player_id=1)])
        self.yaniv.reset()

        self.action_space = spaces.Discrete(58)

        # 54 cards binary mask (your cards)
        # 54 cards one-hot (top pile card)

        self.observation_space = spaces.Dict({
            'card_observation': spaces.Box(low=0, high=1, shape=(2, 54), dtype=np.int8),
            'points': spaces.Box(low=0, high=50, shape=(1,), dtype=np.int8),
            'scores': spaces.Box(low=0, high=150, shape=(2,), dtype=np.int16),
            'action_mask': spaces.Box(low=0, high=1, shape=(58,), dtype=np.int8),
        })

        self.reward = 0

    def reset(self) -> Dict[str, np.array]:
        self.yaniv.reset()
        rl_player = self.yaniv.get_player(0)
        return self._get_state(rl_player)

    def _get_state(self, rl_player: Player) -> Dict[str, np.array]:
        observations = np.zeros((2, 54), dtype=np.int8)
        player_cards = rl_player.get_cards()
        for card in player_cards:
            observations[0, card.index_number] = 1

        # top card observation one-hot
        top_card = self.yaniv.yaniv_round.get_pile_top_card()
        observations[1, top_card.index_number] = 1

        return {
            'card_observation': observations,
            'points': np.array([rl_player.get_points()], dtype=np.int8),
            'scores': np.array([player.game_score for player in self.yaniv.get_players()], dtype=np.int16),
            'action_mask': self._get_action_mask(rl_player)
        }

    def _get_reward(self, action: int, last_legal_actions: np.array) -> float:
        """
            win round +1
            lose round -1
            invalid action -1
            win game +10
        """
        # check if action was valid
        if action not in np.argwhere(last_legal_actions):
            return -1

        # check if game is won
        if self.yaniv.is_over():
            winning_player, *losers = sorted(self.yaniv.get_players(), key=lambda p: p.game_score)
            if self.yaniv.get_current_player().player_id == winning_player.player_id:
                return 10
            else:
                return -10

        # check if round is won and last action was calling yaniv
        if action == 0:
            if self.yaniv.last_round_winner == self.yaniv.get_current_player().player_id:
                return 1
            else:
                return 0

        return 0

    def _get_action_mask(self, rl_player: Player) -> np.array:
        if self.yaniv.get_current_player().player_id == rl_player.player_id:
            action_mask = np.zeros((58,))
            legal_actions = rl_player.get_legal_actions()

            if CallYaniv() in legal_actions:
                action_mask[0] = 1
            elif PickupPileTopCard() in legal_actions:
                action_mask[55] = 1
            elif PickupDeckCard() in legal_actions:
                action_mask[56] = 1

            for legal_action in legal_actions:
                if isinstance(legal_action, ThrowCard):
                    action_mask[legal_action.card.index_number + 1] = 1

            return action_mask.astype(np.int8)
        else:
            action_mask = np.zeros((58,), dtype=np.int8)
            action_mask[57] = 1  # the do nothing action
            return action_mask

    def step(self, action: int):

        current_player = self.yaniv.get_current_player()

        rl_player = self.yaniv.get_player(0)
        last_legal_actions = self._get_action_mask(rl_player)

        # took invalid action, game is corrupt.
        if action not in np.argwhere(last_legal_actions):
            return self._get_state(rl_player), -1, True, {}

        if current_player.player_id == rl_player.player_id:
            current_player.step(self.yaniv, action)
        else:
            current_player.step(self.yaniv)

        observation = self._get_state(rl_player)

        reward = self._get_reward(action, last_legal_actions)

        info = {}

        done = self.yaniv.is_over()
        return observation, reward, done, info

    def render(self):
        """
        Render in console by printing
        """
        self.yaniv.render()
