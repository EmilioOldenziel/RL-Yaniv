from random import choice

import numpy as np
import gym

from rl_yaniv.envs.yaniv import YanivEnv


class TestYanivEnv:

    def test_init_env(self):
        yaniv_env = YanivEnv()
        assert yaniv_env

    def test_env_reset(self):
        yaniv_env = YanivEnv()
        obs = yaniv_env.reset()
        assert isinstance(obs, dict)

    def test_obs_shapes(self):
        yaniv_env = YanivEnv()
        obs = yaniv_env.reset()
        
        for key in obs.keys():
            assert obs[key].shape == yaniv_env.observation_space[key].shape
            assert obs[key].dtype == yaniv_env.observation_space[key].dtype

    def test_env(self):
        yaniv_env = YanivEnv()
        obs = yaniv_env.reset()

        for i in range (50):
            action = choice(np.argwhere(obs.get('action_mask'))).squeeze(0).item()
            obs, *_ = yaniv_env.step(action)
        assert True

    def test_register_env(self):
        gym.envs.register(
            id='Yaniv-v0',
            entry_point='rl_yaniv.envs.yaniv:YanivEnv',
            max_episode_steps=1000,
        )
        env = gym.make('Yaniv-v0')
        assert env