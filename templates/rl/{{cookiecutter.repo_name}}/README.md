# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Setup

{% if cookiecutter.deps_manager == "pixi" %}
```bash
pixi install
```
{% elif cookiecutter.deps_manager == "uv" %}
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```
{% else %}
```bash
conda create -n {{cookiecutter.repo_name}} python={{cookiecutter.python_version}}
conda activate {{cookiecutter.repo_name}}
pip install -e ".[dev]"
```
{% endif %}

## Training

```bash
# Train SAC on Pendulum-v1 (default)
python src/{{cookiecutter.repo_name}}/train.py

# Train TD3 instead
python src/{{cookiecutter.repo_name}}/train.py agent=td3

# Fast debug run (single step, tiny buffer)
python src/{{cookiecutter.repo_name}}/train.py +experiment=debug

# Train on LunarLanderContinuous-v2
python src/{{cookiecutter.repo_name}}/train.py +experiment=lunar_lander

# Override hyperparameters from the command line
python src/{{cookiecutter.repo_name}}/train.py agent.gamma=0.98 env.normalize_obs=false
```

## Testing

```bash
pytest tests/ -v
```

## Project Layout

```
configs/         Hydra configuration files
  agent/         Algorithm configs (sac.yaml, td3.yaml)
  env/           Environment configs (pendulum.yaml, lunar_lander.yaml)
  experiment/    Override bundles (debug.yaml, lunar_lander.yaml)
src/{{cookiecutter.repo_name}}/
  train.py         Hydra entry point
  sac_module.py    SAC LightningModule
  td3_module.py    TD3 LightningModule
  models/          Actor and Critic networks
  data/            ReplayBuffer + RLDataModule
  modules/         Observation normalizer (RunningMeanStd)
  callbacks/       Episode reward logger
tests/           Unit and integration tests
```
