from ray.rllib.policy.policy import Policy
from ray.rllib.models.modelv2 import _unpack_obs
import numpy as np


class RandomHeuristic(Policy):
    """Play a random legal move."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exploration = self._create_exploration()

    def compute_actions(
        self,
        obs_batch,
        state_batches=None,
        prev_action_batch=None,
        prev_reward_batch=None,
        info_batch=None,
        episodes=None,
        **kwargs
    ):

        # Working call to _unpack_obs
        unpacked_obs = _unpack_obs(
            np.array(obs_batch, dtype=np.float32), self.observation_space.original_space, tensorlib=np
        )

        # The nvironment returns observation of the form: {agent_id: {'observations': observations, 'action_mask': action_mask}}
        action_masks = unpacked_obs["action_mask"]

        actions = []
        for action_mask in action_masks:
            if np.any(action_mask):
                action = np.random.choice(np.argwhere(action_mask).flatten())
            else:
                action = 0
            actions.append(action)

        return actions, [], {}

    def learn_on_batch(self, samples):
        pass

    def get_weights(self):
        pass

    def set_weights(self, weights):
        pass
