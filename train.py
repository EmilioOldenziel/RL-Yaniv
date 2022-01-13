from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.logger import pretty_print

from rl_yaniv.envs.yaniv import YanivEnv

# Configure the algorithm.
config = {
    "num_workers": 10,
    "num_envs_per_worker": 2,
    "train_batch_size": 600,
    "lr": 0.001,
    "gamma": 0.9,
    "num_gpus": 1,

    "framework": "torch",

    "model": {
        "fcnet_hiddens": [64],
        "fcnet_activation": "relu",
    },
    "horizon": 1000,
    # Set up a separate evaluation worker set for the
    # `trainer.evaluate()` call after training (see below).
    "evaluation_num_workers": 1,
    # Only for evaluation runs, render the env.
}

# Create our RLlib Trainer.
trainer = PPOTrainer(env=YanivEnv, config=config)


for i in range(1000):
   # Perform one iteration of training the policy with PPO
   result = trainer.train()
   print(pretty_print(result))

# Evaluate the trained Trainer (and render each timestep to the shell's
# output).
trainer.evaluate()
