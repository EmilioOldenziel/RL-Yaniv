from random import choice

import numpy as np

from rl_yaniv.envs.yaniv import YanivEnv


class TestYanivEnv:

    def test_init_env(self):
        yaniv_env = YanivEnv()
        assert yaniv_env

    def test_env_reset(self):
        yaniv_env = YanivEnv()
        obs = yaniv_env.reset()
        assert isinstance(obs, dict)

    def test_env(self):
        yaniv_env = YanivEnv()
        obs = yaniv_env.reset()

        for i in range (50):
            action = choice(np.argwhere(obs.get('action_mask'))).squeeze(0).item()
            yaniv_env.step(action)
        assert True