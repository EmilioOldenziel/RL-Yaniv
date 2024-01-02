from typing import Dict, Tuple

import numpy as np
from gymnasium import Env, spaces
from rl_yaniv.game.actions import (
    CallYaniv,
    PickupDeckCard,
    PickupPileTopCard,
    ThrowCard,
)
from rl_yaniv.game.player import Player, HighThrowPlayer, RLPLayer
from rl_yaniv.game.yaniv import Yaniv


class YanivEnv(Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None, env_config=None) -> None:
        self.yaniv = Yaniv(players=[RLPLayer(player_id=0), HighThrowPlayer(player_id=1)])
        self.yaniv.reset()

        self.action_space = spaces.Discrete(57)

        # 54 cards binary mask (your cards)
        # 54 cards one-hot (top pile card)

        self.observation_space = spaces.Dict(
            {
                "observation": spaces.MultiBinary((2, 54)),
                "points": spaces.Box(low=0, high=50, shape=(1,), dtype=np.int8),
                #'scores': spaces.Box(low=0, high=150, shape=(2,), dtype=np.int16),
                "action_mask": spaces.MultiBinary((57,)),
            }
        )

        self.reward = 0

    def reset(self, seed=None, options=None) -> Tuple[Dict[str, np.array], Dict]:
        self.yaniv.reset()
        rl_player = self.yaniv.get_player(0)

        current_player = self.yaniv.get_current_player()
        while current_player.player_id != 0:
            current_player.step(self.yaniv)
            current_player = self.yaniv.get_current_player()

        return self._get_state(rl_player), {}

    def _get_state(self, rl_player: Player) -> Dict[str, np.array]:
        observations = np.zeros((2, 54), dtype=np.int8)
        player_cards = rl_player.get_cards()
        for card in player_cards:
            observations[0, card.index_number] = 1

        # top card observation one-hot
        top_card = self.yaniv.yaniv_round.get_pile_top_card()
        observations[1, top_card.index_number] = 1

        return {
            "observation": observations,
            "points": np.array([rl_player.get_points()], dtype=np.int8),
            # 'scores': np.array([player.game_score for player in self.yaniv.get_players()], dtype=np.int16),
            "action_mask": self._get_action_mask(rl_player),
        }

    def _get_reward(self, action: int) -> float:
        """
        win round +1
        lose round -1
        invalid action -1
        win game +10
        """
        # check if game is won
        if self.yaniv.is_over():
            winning_player, *losers = sorted(self.yaniv.get_players(), key=lambda p: p.game_score)
            if self.yaniv.get_current_player().player_id == winning_player.player_id:
                return 10
            else:
                return -10

        if action == 0:  # action was calling yaniv
            if self.yaniv.last_round_winner == 0:  # round was won by agent
                return 1
            else:
                return -1

        return 0

    def _get_action_mask(self, rl_player: Player) -> np.array:

        action_mask = np.zeros((57,), np.int8)
        if self.yaniv.get_current_player().player_id == rl_player.player_id:
            legal_actions = rl_player.get_legal_actions()

            if legal_actions == []:
                print("turn but no legal actions")

            if CallYaniv() in legal_actions:
                action_mask[0] = 1
            elif PickupPileTopCard() in legal_actions:
                action_mask[55] = 1
            elif PickupDeckCard() in legal_actions:
                action_mask[56] = 1

            for legal_action in legal_actions:
                if isinstance(legal_action, ThrowCard):
                    action_mask[legal_action.card.index_number + 1] = 1

            # if the its rl player's turn there should be a valid action
            assert np.sum(action_mask) != 0

        return action_mask

    def step(self, action: int):

        current_player = self.yaniv.get_current_player()

        rl_player = self.yaniv.get_player(0)
        last_legal_actions = self._get_action_mask(rl_player)

        # took invalid action, game is corrupt.
        if action not in np.argwhere(last_legal_actions):
            return self._get_state(rl_player), -1, False, True, {}

        # execute action
        current_player.step(self.yaniv, action)
        # get reward
        reward = self._get_reward(action)

        current_player = self.yaniv.get_current_player()
        while current_player.player_id != 0:
            current_player.step(self.yaniv)
            current_player = self.yaniv.get_current_player()

        # get observation
        observation = self._get_state(rl_player)

        info = {}

        terminated = self.yaniv.is_over()
        return observation, reward, terminated, False, info

    def render(self):
        """
        Render in console by printing
        """
        self.yaniv.render()
