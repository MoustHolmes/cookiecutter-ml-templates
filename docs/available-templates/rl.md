# Reinforcement Learning Template

Complete reinforcement learning implementation supporting multiple off-policy and on-policy algorithms.

## Features

- **Multiple algorithms:** SAC, TD3, PPO (discrete & continuous), RPO, DQN
- **PyTorch Lightning** structured modules with callbacks
- **Hydra** configuration with per-algorithm and per-environment configs
- **Pre-configured environments:** Pendulum-v1, CartPole-v1, LunarLander-v2
- **Replay buffer** for off-policy methods + rollout buffer for on-policy methods
- **Observation normalizer** (RunningMeanStd) for stable training
- **W&B** experiment tracking integration

## Usage

```bash
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/rl
```

## Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| `deps_manager` | `pip`, `uv` | Dependency manager |
| `open_source_license` | MIT, BSD-3-Clause, Apache-2.0, No license file | License |
| `create_github_repo` | `no`, `yes` | Auto-create GitHub repo via `gh` CLI |

## Training

```bash
# SAC on Pendulum-v1 (default)
python src/my_rl_project/train.py

# Switch algorithm
python src/my_rl_project/train.py agent=td3
python src/my_rl_project/train.py agent=ppo_continuous
python src/my_rl_project/train.py agent=ppo_discrete
python src/my_rl_project/train.py agent=dqn
python src/my_rl_project/train.py agent=rpo

# Switch environment
python src/my_rl_project/train.py env=lunar_lander

# Use pre-built experiment configs
python src/my_rl_project/train.py +experiment=sac_pendulum
python src/my_rl_project/train.py +experiment=ppo_cartpole
python src/my_rl_project/train.py +experiment=dqn_cartpole

# Fast debug run
python src/my_rl_project/train.py +experiment=debug

# Override hyperparameters inline
python src/my_rl_project/train.py agent.gamma=0.98 env.normalize_obs=false
```

## Project Layout

```
configs/
  agent/          Algorithm configs (sac, td3, ppo_continuous, ppo_discrete, rpo, dqn)
  environment/    Environment configs (pendulum, cartpole, lunar_lander, ...)
  experiment/     Override bundles (debug, sac_pendulum, ppo_cartpole, dqn_cartpole, ...)
  logger/         W&B logger config
  trainer/        Trainer config
  callbacks/      Callback configs
src/<repo_name>/
  train.py            Hydra entry point
  sac_module.py       SAC LightningModule
  td3_module.py       TD3 LightningModule
  ppo_module.py       PPO LightningModule (discrete + continuous)
  dqn_module.py       DQN LightningModule
  models/
    actor.py          Stochastic/deterministic actor networks
    critic.py         Q-value critic networks
    ppo_agent.py      PPO actor-critic agent
    qnetwork.py       DQN Q-network
  data/
    replay_buffer.py      Off-policy replay buffer
    env_datamodule.py     Gymnasium environment data module
    rollout_datamodule.py On-policy rollout buffer
  modules/
    normalizers.py    RunningMeanStd observation normalizer
  callbacks/
    episode_logger.py Episode reward / length logging
    video_logger.py   Episode video recording
  util/
    plot_rewards.py   Reward curve plotting utilities
tests/
  test_config.py      Config loading tests
  test_data.py        Data module tests
  test_model.py       Model forward-pass tests
  test_train_script.py End-to-end training smoke tests
```

## Algorithms

| Algorithm | Type | Action Space | Key Config |
|-----------|------|-------------|------------|
| SAC | Off-policy | Continuous | `agent=sac` |
| TD3 | Off-policy | Continuous | `agent=td3` |
| PPO | On-policy | Continuous | `agent=ppo_continuous` |
| PPO | On-policy | Discrete | `agent=ppo_discrete` |
| RPO | On-policy | Continuous | `agent=rpo` |
| DQN | Off-policy | Discrete | `agent=dqn` |

## Use Cases

- Solving standard Gymnasium environments
- Benchmarking RL algorithms
- Research baselines
- Learning RL with structured, readable code
