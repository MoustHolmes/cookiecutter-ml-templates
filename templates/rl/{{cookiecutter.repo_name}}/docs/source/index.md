# {{cookiecutter.project_name}}

A minimal, well-structured PyTorch Lightning template for training Reinforcement Learning agents.

## Overview

This project provides a clean, modular framework for experimenting with deep RL algorithms. It includes:

- **SAC (Soft Actor-Critic)**: Off-policy, entropy-regularised actor-critic for continuous actions
- **TD3 (Twin Delayed DDPG)**: Deterministic off-policy variant with target policy smoothing
- **Modular Components**: Easy-to-swap actors, critics, replay buffers, and environment wrappers
- **Configuration Management**: Hydra-based config system for reproducible experiments
- **Experiment Tracking**: Weights & Biases integration for episodic reward logging
- **Production Ready**: Type hints, tests, and documentation

## Quick Start

### Installation

```bash
pip install -e .[dev]
```

### Training

Train SAC on Pendulum-v1 (default):
```bash
python src/{{cookiecutter.repo_name}}/train.py
```

Run a fast debug training pass:
```bash
python src/{{cookiecutter.repo_name}}/train.py +experiment=debug
```

Train on LunarLanderContinuous-v2:
```bash
python src/{{cookiecutter.repo_name}}/train.py +experiment=lunar_lander
```

Switch to TD3:
```bash
python src/{{cookiecutter.repo_name}}/train.py agent=td3
```

### Configuration

Override any configuration from the command line:
```bash
# Change batch size and learning rate
python src/{{cookiecutter.repo_name}}/train.py env.batch_size=128 agent.actor_optimizer.lr=1e-4

# Disable observation normalisation
python src/{{cookiecutter.repo_name}}/train.py env.normalize_obs=false
```

## Project Structure

```
├── configs/
│   ├── train_config.yaml     # Main config
│   ├── agent/                # Agent configs (sac, td3)
│   ├── env/                  # Environment configs (pendulum, lunar_lander)
│   ├── trainer/              # Trainer configs
│   ├── callbacks/            # Callback configs
│   └── experiment/           # Experiment overrides
├── src/{{cookiecutter.repo_name}}/
│   ├── train.py              # Hydra entry point
│   ├── sac_module.py         # SAC LightningModule
│   ├── td3_module.py         # TD3 LightningModule
│   ├── models/               # Actor and Critic networks
│   ├── data/                 # ReplayBuffer and RLDataModule
│   ├── modules/              # Obs normalizer (RunningMeanStd)
│   ├── callbacks/            # Episode logger callback
│   └── util/                 # Plotting utilities
└── tests/                    # Unit and integration tests
```

## Key Algorithms

### SAC (Soft Actor-Critic)

SAC maximises both expected return and policy entropy, which encourages exploration and prevents premature convergence:

```python
from {{cookiecutter.repo_name}}.sac_module import SACModule
from {{cookiecutter.repo_name}}.models.actor import StochasticActor
from {{cookiecutter.repo_name}}.models.critic import TwinCritic

agent = SACModule(
    actor=StochasticActor(obs_dim=3, action_dim=1),
    critic=TwinCritic(obs_dim=3, action_dim=1),
    gamma=0.99,
    tau=0.005,
)
```

### TD3 (Twin Delayed DDPG)

TD3 addresses Q-value overestimation with twin critics, delayed policy updates, and target policy smoothing:

```python
from {{cookiecutter.repo_name}}.td3_module import TD3Module
from {{cookiecutter.repo_name}}.models.actor import DeterministicActor
from {{cookiecutter.repo_name}}.models.critic import TwinCritic

agent = TD3Module(
    actor=DeterministicActor(obs_dim=3, action_dim=1),
    critic=TwinCritic(obs_dim=3, action_dim=1),
    policy_delay=2,
    target_noise=0.2,
)
```

## Testing

```bash
pytest tests/ -v
pytest tests/test_model.py -v   # model unit tests only
```

## License

{% if cookiecutter.open_source_license != "No license file" %}{{cookiecutter.open_source_license}} License — see LICENSE file for details.{% else %}See repository for license details.{% endif %}
