
from gym import spaces
from rlcard.envs import Env

from rl_yaniv.game.actions import Yaniv

class YanivEnv(Env):
    
    def __init__(self) -> None:
        self.yaniv = Yaniv()

        self.action_space = {i: spaces.Discrete(9) for i in self.agents}

        # 54 cards binary mask (your cards)
        # 54 cards one-hot (top pile card)

        self.observation_space = spaces.Dict({
            'observation': spaces.Box(low=0, high=1, shape=(3, 54), dtype=np.int8),
            'action_mask': spaces.Box(low=0, high=1, shape=(55,), dtype=np.int8)
        })
                

        self.reward = 0

    def reset(self):
        self.yaniv.reset()

    def step(self, action: int):

        self.yaniv.step(action)

        observation = self.yaniv.get_state()

        reward = self.yaniv.get_reward()

        info = {}

        done = {'__all__': self.yaniv.is_over()}
        return observation, reward, done, info