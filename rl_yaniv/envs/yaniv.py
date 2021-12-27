from typing import Dict, List, Union

import numpy as np
from gym import spaces
from rlcard.envs import Env

from rl_yaniv.game.actions import Action
from rl_yaniv.game.yaniv import Yaniv
from rl_yaniv.game.player import Player, RandomPlayer, RLPLayer

class YanivEnv(Env):
    
    def __init__(self) -> None:
        self.yaniv = Yaniv(players=[RLPLayer(player_id=0), RandomPlayer(player_id=1)])
        self.yaniv.reset()

        self.action_space = spaces.Discrete(58)

        # 54 cards binary mask (your cards)
        # 54 cards one-hot (top pile card)

        self.observation_space = spaces.Dict({
            'card_observation': spaces.MultiBinary((2, 54)),
            'points': spaces.Box(low=0, high=50, shape=(1,)),
            'score': spaces.Box(low=0, high=150, shape=(self.yaniv.get_num_players(),)),
            'action_mask': spaces.MultiBinary((58,))
        })

        self.reward = 0

    def reset(self):
        self.yaniv.reset()
        rl_player = self.yaniv.get_player(0)
        obs = self._get_state(rl_player)
        rl_player.last_valid_actions = obs.get('action_mask')
        return obs

    def _get_state(self, rl_player: Player) -> Dict[str, List]:
        observations = np.zeros((2, 54))
        player_cards = rl_player.cards
        for card in player_cards.values():
            observations[0, card.index_number] = 1

        # top card observation one-hot
        top_card = self.yaniv.yaniv_round.get_pile_top_card()
        observations[1, top_card.index_number] = 1

        return {
            'card_observation': observations,
            'points': rl_player.get_points(),
            'scores': np.array([player.game_score for player in self.yaniv.players.values()]),
            'action_mask': self._get_action_mask(rl_player)
        }

    def _get_reward(self, rl_player: Player, action: Action) -> float:
        """
         win round +1
         lose round -1
         invalid action -1
         win game +10
        """
        # check if action was valid
        if rl_player.last_action not in rl_player.last_valid_actions:
            self.yaniv.reset()  # game is corrupt and has to be restart
            return -1

        # check if game is won
        if self.yaniv.isover():
            winning_player, *losers = sorted(self.yaniv.players.values(), key=lambda p: p.game_score)
            if self.yaniv.get_current_player().player_id == winning_player.player_id:
                return 10
            else:
                return -10

        # check if round is won and last action was calling yaniv
        if action == 0:
            if self.yaniv.last_round_winner == self.yaniv.get_current_player().id:
                return 1
            else:
                return 0

    def _get_action_mask(self, rl_player: Player) -> np.array:
        if self.yaniv.get_current_player().player_id == rl_player.player_id:
            return np.array(rl_player.get_legal_actions())
        else:
            action_mask = np.zeros((58,))
            action_mask[57] = 1  # the do nothing action
            return action_mask

    def step(self, action: int):

        current_player = self.yaniv.get_current_player()

        if current_player.player_id == 0:
            current_player.step(self.yaniv, action)
        else:
            current_player.step(self.yaniv)

        rl_player = self.yaniv.get_player(0)
        observation = self._get_state(rl_player)

        reward = self._get_reward(rl_player, action)
        rl_player.last_valid_actions = observation.get('action_mask')

        info = {}

        done = self.yaniv.is_over()
        return observation, reward, done, info
