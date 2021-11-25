
from rlcard.envs import Env

from rl_yaniv.game.actions import Yaniv

class YanivEnv(Env):
    
    def __init__(self) -> None:
        self.yaniv = Yaniv()

        self.action_spaces = {i: spaces.Discrete(9) for i in self.agents}
        self.observation_spaces = {i: spaces.Dict({
                                        'observation': spaces.Box(low=0, high=1, shape=(3, 3, 2), dtype=np.int8),
                                        'action_mask': spaces.Box(low=0, high=1, shape=(9,), dtype=np.int8)
                                  }) for i in self.agents}

        self.rewards = {i: 0 for i in self.agents}
        self.dones = {i: False for i in self.agents}

    def reset(self):
        pass

    def step(self, action: int):


        done = {'__all__': self.yaniv.is_over()}
        return observation, reward, done, info