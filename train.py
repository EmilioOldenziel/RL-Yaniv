from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.logger import pretty_print
from ray.rllib.models import ModelCatalog

from rl_yaniv.envs.yaniv_env import YanivEnv

from models.parametric_actions_model import TorchParametricActionsEmbeddingsModel

ModelCatalog.register_custom_model("pa_model", TorchParametricActionsEmbeddingsModel)

config = (  # 1. Configure the algorithm,
    PPOConfig()
    .environment(YanivEnv)
    .rollouts(num_rollout_workers=4)
    .framework("torch")
    .training(
        model={
            "custom_model": "pa_model",
            "vf_share_layers": True,
        }
    )
    .resources(num_gpus=0)
    .evaluation(evaluation_num_workers=1)
)

algo = config.build()  # 2. build the algorithm

for i in range(100):
    # Perform one iteration of training the policy with PPO
    result = algo.train()
    print(pretty_print(result))

# Evaluate the trained Trainer (and render each timestep to the shell's
# output).
algo.evaluate()
