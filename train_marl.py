from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.logger import pretty_print
from ray.rllib.models import ModelCatalog
from ray.rllib.policy.policy import PolicySpec
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from rl_yaniv.envs.yaniv_multiagent import YanivMultiAgentEnv

from models.parametric_actions_model import TorchParametricActionsEmbeddingsModel
from rl_yaniv.policy import RandomHeuristic

ModelCatalog.register_custom_model("pa_model", TorchParametricActionsEmbeddingsModel)


def select_policy(agent_id, episode, **kwargs):
    if agent_id == 0 or agent_id == 2:
        return "learned"
    else:
        return "random_player"


config = (  # 1. Configure the algorithm,
    PPOConfig()
    .environment(YanivMultiAgentEnv, disable_env_checking=True)
    .rollouts(num_rollout_workers=4)
    .framework("torch")
    .multi_agent(
        policies={
            "random_player": PolicySpec(policy_class=RandomHeuristic),
            "learned": PolicySpec(
                config=AlgorithmConfig.overrides(
                    model={"custom_model": "pa_model", "vf_share_layers": True},
                    framework_str="torch",
                )
            ),
        },
        policy_mapping_fn=select_policy,
        policies_to_train=["learned"],
    )
    .reporting(metrics_num_episodes_for_smoothing=200)
    .resources(num_gpus=0)
    .evaluation(evaluation_num_workers=1)
)

algo = config.build()  # 2. build the algorithm

for _ in range(100):
    # Perform one iteration of training the policy with PPO
    results = algo.train()
    print(pretty_print(results))

# Evaluate the trained Trainer (and render each timestep to the shell's
# output).
algo.evaluate()
