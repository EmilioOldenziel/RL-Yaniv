from typing import Any, Tuple, Dict, List

import numpy as np
import gymnasium as gym
from ray.rllib.env.multi_agent_env import MultiAgentEnv

from rl_yaniv.envs.yaniv_env import YanivEnv
from rl_yaniv.game.player import RLPLayer
from rl_yaniv.game.yaniv import Yaniv


class YanivMultiAgentEnv(YanivEnv, MultiAgentEnv):
    """
    Yaniv Env implemented as as RLLib's multi agent environment.
    """

    def __init__(self, render_mode=None, env_config=None) -> None:
        super().__init__()

        self.yaniv = Yaniv(players=[RLPLayer(player_id=0), RLPLayer(player_id=1), RLPLayer(player_id=2)])
        self.yaniv.reset()

        self.action_space = gym.spaces.Discrete(57)

        # 54 cards binary mask (your cards)
        # 54 cards one-hot (top pile card)

        self.observation_space = gym.spaces.Dict(
            {
                "observation": gym.spaces.MultiBinary((2, 54)),
                "points": gym.spaces.Box(low=0, high=50, shape=(1,), dtype=np.int8),
                #'scores': spaces.Box(low=0, high=150, shape=(2,), dtype=np.int16),
                "action_mask": gym.spaces.MultiBinary((57,)),
            }
        )

        self._agent_ids = [player.player_id for player in self.yaniv.get_players()]

    def _get_reward(self, action: int, agent_id: int) -> float:
        """
        win round +1
        lose round -1
        invalid action -1
        win game +10
        """
        if action == 0:  # action was calling yaniv
            # check if game is won
            if self.yaniv.is_over():
                winning_player, *losers = sorted(self.yaniv.get_players(), key=lambda p: p.game_score)
                if agent_id == winning_player.player_id:
                    return 10
                else:
                    return -10
            # NOTE: if game is won by player and also called yaniv in the last round we just give 10 and not 11
            if self.yaniv.last_round_winner == agent_id:  # round was won by agent
                return 1
            else:
                return -1

        return 0

    def reset(self, seed: int | None = None, options: dict | None = None) -> Tuple[Dict[Any, Any], Dict[Any, Any]]:
        self.yaniv.reset()

        return {player.player_id: self._get_state(player) for player in self.yaniv.get_players()}, {}

    def step(
        self, action_dict: Dict[Any, Any]
    ) -> Tuple[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]:

        current_player = self.yaniv.get_current_player()
        current_player_id = current_player.player_id
        action = action_dict[current_player_id]

        # check for truncation by illegal action
        truncations = {"__all__": False}
        for agent_id in self._agent_ids:
            last_legal_actions = self._get_action_mask(self.yaniv.get_player(agent_id))
            if (action not in np.argwhere(last_legal_actions).flatten()) and (current_player_id == agent_id):
                rewards = {agent: 0 for agent in self._agent_ids}
                rewards[agent_id] = -10
                print(
                    f"Player {agent_id} takes an ilegal action {action} where {np.argwhere(last_legal_actions).flatten()} was allowed!"
                )
                return (
                    {agent: self._get_state(self.yaniv.get_player(agent_id)) for agent in self._agent_ids},
                    rewards,
                    {"__all__": True},
                    {"__all__": True},
                    {agent: {} for agent in self._agent_ids},
                )

        # if all(list(truncations.values())):
        #     truncations["__all__"] = True

        # execute action
        current_player.step(self.yaniv, action)

        # rewards
        rewards = {current_player_id: self._get_reward(action, agent_id=current_player_id)}

        # set terminateds
        if self.yaniv.is_over():
            terminateds = {current_player_id: True}
            terminateds["__all__"] = True
        else:
            terminateds = {current_player_id: False}
            terminateds["__all__"] = False

        next_player = self.yaniv.get_current_player()
        next_player_id = next_player.player_id

        # get observations
        observations = {next_player_id: self._get_state(self.yaniv.get_player(next_player_id))}

        infos = {next_player_id: {}}

        return observations, rewards, terminateds, truncations, infos
