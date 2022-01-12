from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.logger import pretty_print

from rl_yaniv.envs.yaniv import YanivEnv

# Configure the algorithm.
config = {
    # Use 2 environment workers (aka "rollout workers") that parallelly
    # collect samples from their own environment clone(s).
    "num_workers": 4,
    # Change this to "framework: torch", if you are using PyTorch.
    # Also, use "framework: tf2" for tf2.x eager execution.
    "framework": "torch",
    # Tweak the default model provided automatically by RLlib,
    # given the environment's observation- and action spaces.
    "model": {
        "fcnet_hiddens": [64, 64],
        "fcnet_activation": "relu",
    },
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
