"""Copier-based generation tests for the barebone, classification, flow_matching, rl, and vae templates."""

from pathlib import Path
from typing import Any

import copier
import pytest

REPO_ROOT = (Path(__file__).parent / "..").resolve()
BAREBONE_TEMPLATE = REPO_ROOT / "templates" / "barebone"
CLASSIFICATION_TEMPLATE = REPO_ROOT / "templates" / "core" / "classification"
FLOW_MATCHING_TEMPLATE = REPO_ROOT / "templates" / "generative" / "flow_matching"
RL_TEMPLATE = REPO_ROOT / "templates" / "rl"
VAE_TEMPLATE = REPO_ROOT / "templates" / "generative" / "vae"


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


def _generate(dst: Path, **data: Any) -> Path:
    defaults = {
        "project_name": "test_project",
        "user_name": "Test Author",
        "description": "Test Description",
        "python_version": "3.12",
    }
    defaults.update(data)
    copier.run_copy(
        src_path=str(BAREBONE_TEMPLATE),
        dst_path=str(dst),
        data=defaults,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def test_barebone_full_structure(temp_dir: Path) -> None:
    out = _generate(temp_dir / "full")

    assert (out / "src" / "test_project").exists()
    assert (out / "src" / "test_project" / "__init__.py").exists()
    assert (out / "src" / "test_project" / "train.py").exists()
    assert (out / "src" / "test_project" / "barebones_lightningmodule.py").exists()
    assert (out / "src" / "test_project" / "models" / "__init__.py").exists()
    assert (out / "src" / "test_project" / "data" / "__init__.py").exists()
    assert (out / "src" / "test_project" / "data" / "barebones_datamodule.py").exists()

    assert (out / "configs" / "train_config.yaml").exists()
    assert (out / "configs" / "paths_config.yaml").exists()
    assert (out / "configs" / "model" / "default_model.yaml").exists()
    assert (out / "configs" / "data" / "default_data_module.yaml").exists()
    assert (out / "configs" / "trainer" / "default_trainer.yaml").exists()
    assert (out / "configs" / "logger" / "wandb_logger.yaml").exists()
    assert (out / "configs" / "callbacks" / "default_callbacks.yaml").exists()

    assert (out / "tests" / "__init__.py").exists()
    assert (out / "tests" / "conftest.py").exists()
    assert (out / "tests" / "test_config.py").exists()
    assert (out / "tests" / "test_data.py").exists()
    assert (out / "tests" / "test_model.py").exists()

    assert (out / "docs" / "mkdocs.yaml").exists()
    assert (out / "data" / "README.md").exists()
    assert (out / "notebooks" / ".gitkeep").exists()
    assert (out / "reports" / "figures" / ".gitkeep").exists()

    assert (out / "pyproject.toml").exists()
    assert (out / "README.md").exists()
    assert (out / ".gitignore").exists()
    assert (out / ".pre-commit-config.yaml").exists()
    assert (out / ".github" / "workflows" / "ci.yml").exists()
    assert (out / ".copier-answers.yml").exists()


def test_barebone_minimal_no_docs(temp_dir: Path) -> None:
    out = _generate(temp_dir / "minimal", project_structure="minimal")

    assert not (out / "docs").exists()
    assert (out / "src" / "test_project").exists()
    assert (out / "tests").exists()

    tasks = (out / "tasks.py").read_text()
    assert "def build_docs" not in tasks
    assert "def serve_docs" not in tasks
    assert "def test" in tasks
    assert "def train" in tasks


def test_barebone_pip_deps_manager(temp_dir: Path) -> None:
    out = _generate(temp_dir / "pip", deps_manager="pip")

    assert (out / "requirements.txt").exists()
    assert (out / "requirements_dev.txt").exists()
    assert not (out / "pixi.toml").exists()

    tasks = (out / "tasks.py").read_text()
    assert "pip install" in tasks
    assert "uv run" not in tasks


def test_barebone_uv_deps_manager(temp_dir: Path) -> None:
    out = _generate(temp_dir / "uv", deps_manager="uv")

    assert not (out / "requirements.txt").exists()
    assert not (out / "pixi.toml").exists()

    pyproject = (out / "pyproject.toml").read_text()
    assert "dependencies = [" in pyproject
    assert "[project.optional-dependencies]" in pyproject

    tasks = (out / "tasks.py").read_text()
    assert "uv run" in tasks


def test_barebone_pixi_deps_manager(temp_dir: Path) -> None:
    out = _generate(temp_dir / "pixi", deps_manager="pixi")

    assert (out / "pixi.toml").exists()
    assert not (out / "requirements.txt").exists()
    assert not (out / "tasks.py").exists()


def test_barebone_mit_license(temp_dir: Path) -> None:
    out = _generate(temp_dir / "mit", open_source_license="MIT")
    assert (out / "LICENSE").exists()
    assert "MIT" in (out / "LICENSE").read_text()


def test_barebone_no_license(temp_dir: Path) -> None:
    out = _generate(temp_dir / "nolicense", open_source_license="No license file")
    assert not (out / "LICENSE").exists()


def test_barebone_config_uses_repo_name(temp_dir: Path) -> None:
    out = _generate(temp_dir / "naming", project_name="my_model")
    model_cfg = (out / "configs" / "model" / "default_model.yaml").read_text()
    assert "my_model.barebones_lightningmodule" in model_cfg
    data_cfg = (out / "configs" / "data" / "default_data_module.yaml").read_text()
    assert "my_model.data.barebones_datamodule" in data_cfg


def test_barebone_answers_file_written(temp_dir: Path) -> None:
    out = _generate(temp_dir / "answers")
    answers = (out / ".copier-answers.yml").read_text()
    assert "project_name: test_project" in answers
    assert "_src_path:" in answers


# --- Classification template ---


def _generate_cls(dst: Path, **data: Any) -> Path:
    defaults = {
        "project_name": "test_cls",
        "user_name": "Test Author",
        "description": "Test Description",
        "python_version": "3.12",
    }
    defaults.update(data)
    copier.run_copy(
        src_path=str(CLASSIFICATION_TEMPLATE),
        dst_path=str(dst),
        data=defaults,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def test_classification_full_structure(temp_dir: Path) -> None:
    out = _generate_cls(temp_dir / "full")

    assert (out / "src" / "test_cls").exists()
    assert (out / "src" / "test_cls" / "__init__.py").exists()
    assert (out / "src" / "test_cls" / "train.py").exists()
    assert (out / "src" / "test_cls" / "classification_module.py").exists()
    assert (out / "src" / "test_cls" / "models" / "__init__.py").exists()
    assert (out / "src" / "test_cls" / "data" / "mnist_datamodule.py").exists()
    assert (out / "src" / "test_cls" / "callbacks" / "__init__.py").exists()

    assert (out / "configs" / "train_config.yaml").exists()
    assert (out / "configs" / "experiments" / "debug.yaml").exists()
    assert (out / "configs" / "model" / "default_model.yaml").exists()
    assert (out / "configs" / "data" / "default_data_module.yaml").exists()
    assert (out / "docs" / "mkdocs.yaml").exists()

    assert (out / "tests" / "test_model.py").exists()
    assert (out / "tests" / "test_data.py").exists()
    assert (out / ".github" / "workflows" / "ci.yml").exists()
    assert (out / ".copier-answers.yml").exists()


def test_classification_pip_deps_manager(temp_dir: Path) -> None:
    out = _generate_cls(temp_dir / "pip", deps_manager="pip")
    assert (out / "requirements.txt").exists()
    assert not (out / "pixi.toml").exists()


def test_classification_uv_deps_manager(temp_dir: Path) -> None:
    out = _generate_cls(temp_dir / "uv", deps_manager="uv")
    assert not (out / "requirements.txt").exists()
    assert not (out / "pixi.toml").exists()
    assert "dependencies = [" in (out / "pyproject.toml").read_text()


def test_classification_pixi_deps_manager(temp_dir: Path) -> None:
    out = _generate_cls(temp_dir / "pixi", deps_manager="pixi")
    assert (out / "pixi.toml").exists()
    assert not (out / "tasks.py").exists()
    assert not (out / "requirements.txt").exists()


def test_classification_config_uses_repo_name(temp_dir: Path) -> None:
    out = _generate_cls(temp_dir / "naming", project_name="my_cls")
    model_cfg = (out / "configs" / "model" / "default_model.yaml").read_text()
    assert "my_cls.classification_module.ClassificationModule" in model_cfg
    data_cfg = (out / "configs" / "data" / "default_data_module.yaml").read_text()
    assert "my_cls.data.mnist_datamodule.MNISTDataModule" in data_cfg


# --- Flow matching template ---


def _generate_flow(dst: Path, **data: Any) -> Path:
    defaults = {
        "project_name": "test_flow",
        "user_name": "Test Author",
        "description": "Test Description",
        "python_version": "3.12",
    }
    defaults.update(data)
    copier.run_copy(
        src_path=str(FLOW_MATCHING_TEMPLATE),
        dst_path=str(dst),
        data=defaults,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def test_flow_matching_full_structure(temp_dir: Path) -> None:
    out = _generate_flow(temp_dir / "full")

    assert (out / "src" / "test_flow").exists()
    assert (out / "src" / "test_flow" / "__init__.py").exists()
    assert (out / "src" / "test_flow" / "train.py").exists()
    assert (out / "src" / "test_flow" / "flow_matching_module.py").exists()
    assert (out / "src" / "test_flow" / "vae_module.py").exists()
    assert (out / "src" / "test_flow" / "models" / "unet.py").exists()
    assert (out / "src" / "test_flow" / "models" / "mlp.py").exists()
    assert (out / "src" / "test_flow" / "data" / "MNIST_datamodule.py").exists()
    assert (out / "src" / "test_flow" / "data" / "moons_datamodule.py").exists()
    assert (out / "src" / "test_flow" / "modules" / "solvers.py").exists()
    assert (out / "src" / "test_flow" / "modules" / "samplers.py").exists()
    assert (out / "src" / "test_flow" / "modules" / "schedulers.py").exists()
    assert (out / "src" / "test_flow" / "callbacks" / "image_logger.py").exists()

    assert (out / "configs" / "train_config.yaml").exists()
    assert (out / "configs" / "model" / "default_model.yaml").exists()
    assert (out / "configs" / "data" / "default_data_module.yaml").exists()
    assert (out / "configs" / "experiment" / "debug.yaml").exists()

    assert (out / "tests" / "test_model.py").exists()
    assert (out / "tests" / "test_data.py").exists()
    assert (out / "tests" / "test_config.py").exists()
    assert (out / "tests" / "test_train_script.py").exists()

    assert (out / "data" / "MNIST" / "raw" / ".gitkeep").exists()
    assert (out / ".github" / "workflows" / "ci.yml").exists()
    assert (out / ".copier-answers.yml").exists()


def test_flow_matching_uv_deps_manager(temp_dir: Path) -> None:
    out = _generate_flow(temp_dir / "uv", deps_manager="uv")

    assert not (out / "requirements.txt").exists()
    assert not (out / "pixi.toml").exists()

    pyproject = (out / "pyproject.toml").read_text()
    assert "dependencies = [" in pyproject
    assert "[project.optional-dependencies]" in pyproject

    tasks = (out / "tasks.py").read_text()
    assert "uv run" in tasks


def test_flow_matching_pip_deps_manager(temp_dir: Path) -> None:
    out = _generate_flow(temp_dir / "pip", deps_manager="pip")

    assert (out / "requirements.txt").exists()
    assert (out / "requirements_dev.txt").exists()
    assert not (out / "pixi.toml").exists()

    tasks = (out / "tasks.py").read_text()
    assert "uv run" not in tasks


def test_flow_matching_pixi_deps_manager(temp_dir: Path) -> None:
    out = _generate_flow(temp_dir / "pixi", deps_manager="pixi")

    assert (out / "pixi.toml").exists()
    assert not (out / "requirements.txt").exists()
    assert not (out / "tasks.py").exists()


def test_flow_matching_config_uses_repo_name(temp_dir: Path) -> None:
    out = _generate_flow(temp_dir / "naming", project_name="my_flow")
    model_cfg = (out / "configs" / "model" / "default_model.yaml").read_text()
    assert "my_flow.flow_matching_module.FlowMatching" in model_cfg


def test_flow_matching_skip_mnist_data(temp_dir: Path) -> None:
    out = _generate_flow(temp_dir / "skip")

    # Seed a fake data file to simulate downloaded MNIST data
    fake_data = out / "data" / "MNIST" / "raw" / "train-images-idx3-ubyte"
    fake_data.write_bytes(b"fake mnist content")
    original_mtime = fake_data.stat().st_mtime

    # Re-run copy — _skip_if_exists should preserve existing MNIST data
    copier.run_copy(
        src_path=str(FLOW_MATCHING_TEMPLATE),
        dst_path=str(out),
        data={"project_name": "my_flow", "user_name": "Test Author", "description": "Test", "python_version": "3.12"},
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    assert fake_data.stat().st_mtime == original_mtime


# --- RL template ---


def _generate_rl(dst: Path, **data: Any) -> Path:
    defaults = {
        "project_name": "test_rl",
        "user_name": "Test Author",
        "description": "Test Description",
        "python_version": "3.11",
    }
    defaults.update(data)
    copier.run_copy(
        src_path=str(RL_TEMPLATE),
        dst_path=str(dst),
        data=defaults,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def test_rl_full_structure(temp_dir: Path) -> None:
    out = _generate_rl(temp_dir / "full")

    src = out / "src" / "test_rl"
    assert src.exists()
    assert (src / "__init__.py").exists()
    assert (src / "train.py").exists()
    for module in ("sac_module.py", "td3_module.py", "ppo_module.py", "dqn_module.py"):
        assert (src / module).exists(), f"Missing {module}"
    for model_file in ("actor.py", "critic.py", "mlp.py"):
        assert (src / "models" / model_file).exists()
    for data_file in ("replay_buffer.py", "env_datamodule.py", "rollout_datamodule.py"):
        assert (src / "data" / data_file).exists()
    for cb in ("episode_logger.py", "video_logger.py"):
        assert (src / "callbacks" / cb).exists()

    configs = out / "configs"
    for agent_cfg in ("sac.yaml", "td3.yaml", "ppo_discrete.yaml", "ppo_continuous.yaml", "dqn.yaml", "rpo.yaml"):
        assert (configs / "agent" / agent_cfg).exists()
    for env_cfg in ("pendulum.yaml", "cartpole.yaml", "cartpole_replay.yaml", "lunar_lander.yaml"):
        assert (configs / "environment" / env_cfg).exists()

    tests = out / "tests"
    for test_file in ("conftest.py", "test_config.py", "test_data.py", "test_model.py", "test_train_script.py"):
        assert (tests / test_file).exists()

    assert (out / ".github" / "workflows" / "ci.yml").exists()
    assert (out / ".copier-answers.yml").exists()


def test_rl_pip_deps_manager(temp_dir: Path) -> None:
    out = _generate_rl(temp_dir / "pip", deps_manager="pip")

    assert (out / "requirements.txt").exists()
    assert (out / "requirements_dev.txt").exists()
    assert not (out / "pixi.toml").exists()
    assert (out / "tasks.py").exists()


def test_rl_uv_deps_manager(temp_dir: Path) -> None:
    out = _generate_rl(temp_dir / "uv", deps_manager="uv")

    assert not (out / "requirements.txt").exists()
    assert not (out / "pixi.toml").exists()

    pyproject = (out / "pyproject.toml").read_text()
    assert "dependencies = [" in pyproject
    assert "[project.optional-dependencies]" in pyproject

    tasks = (out / "tasks.py").read_text()
    assert "uv run" in tasks


def test_rl_pixi_deps_manager(temp_dir: Path) -> None:
    out = _generate_rl(temp_dir / "pixi", deps_manager="pixi")

    assert (out / "pixi.toml").exists()
    assert not (out / "requirements.txt").exists()
    assert not (out / "tasks.py").exists()

    pixi_content = (out / "pixi.toml").read_text()
    assert "gymnasium" in pixi_content
    assert "[tasks]" in pixi_content
    assert "train" in pixi_content


def test_rl_config_uses_repo_name(temp_dir: Path) -> None:
    out = _generate_rl(temp_dir / "naming", project_name="my_rl")
    sac_cfg = (out / "configs" / "agent" / "sac.yaml").read_text()
    assert "my_rl.sac_module" in sac_cfg


# --- VAE template ---


def _generate_vae(dst: Path, **data: Any) -> Path:
    defaults = {
        "project_name": "test_vae",
        "user_name": "Test Author",
        "description": "Test Description",
        "python_version": "3.12",
    }
    defaults.update(data)
    copier.run_copy(
        src_path=str(VAE_TEMPLATE),
        dst_path=str(dst),
        data=defaults,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return dst


def test_vae_full_structure(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "full")

    src = out / "src" / "test_vae"
    assert src.exists()
    assert (src / "__init__.py").exists()
    assert (src / "train.py").exists()
    assert (src / "vae_module.py").exists()
    assert (src / "models" / "__init__.py").exists()
    assert (src / "models" / "encoder.py").exists()
    assert (src / "models" / "decoder.py").exists()
    assert (src / "data" / "__init__.py").exists()
    assert (src / "data" / "datamodule.py").exists()
    assert (src / "callbacks" / "__init__.py").exists()
    assert (src / "callbacks" / "vae_image_logger.py").exists()

    assert (out / "configs" / "train_config.yaml").exists()
    assert (out / "configs" / "paths_config.yaml").exists()
    assert (out / "configs" / "model" / "default_model.yaml").exists()
    assert (out / "configs" / "data" / "default_data_module.yaml").exists()
    assert (out / "configs" / "trainer" / "default_trainer.yaml").exists()
    assert (out / "configs" / "callbacks" / "default_callbacks.yaml").exists()
    assert (out / "configs" / "logger" / "wandb_logger.yaml").exists()
    assert (out / "configs" / "experiment" / "debug.yaml").exists()

    assert (out / "tests" / "__init__.py").exists()
    assert (out / "tests" / "conftest.py").exists()
    assert (out / "tests" / "test_config.py").exists()
    assert (out / "tests" / "test_model.py").exists()
    assert (out / "tests" / "test_data.py").exists()
    assert (out / "tests" / "test_train_script.py").exists()

    assert (out / "data" / "MNIST" / "raw" / ".gitkeep").exists()
    assert (out / ".github" / "workflows" / "ci.yml").exists()
    assert (out / ".copier-answers.yml").exists()
    assert (out / "pyproject.toml").exists()
    assert (out / "README.md").exists()


def test_vae_uv_deps_manager(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "uv", deps_manager="uv")

    assert not (out / "requirements.txt").exists()
    assert not (out / "pixi.toml").exists()

    pyproject = (out / "pyproject.toml").read_text()
    assert "dependencies = [" in pyproject
    assert "[project.optional-dependencies]" in pyproject

    tasks = (out / "tasks.py").read_text()
    assert "uv run" in tasks


def test_vae_pip_deps_manager(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "pip", deps_manager="pip")

    assert (out / "requirements.txt").exists()
    assert (out / "requirements_dev.txt").exists()
    assert not (out / "pixi.toml").exists()

    tasks = (out / "tasks.py").read_text()
    assert "uv run" not in tasks


def test_vae_pixi_deps_manager(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "pixi", deps_manager="pixi")

    assert (out / "pixi.toml").exists()
    assert not (out / "requirements.txt").exists()
    assert not (out / "tasks.py").exists()


def test_vae_config_uses_repo_name(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "naming", project_name="my_vae")
    model_cfg = (out / "configs" / "model" / "default_model.yaml").read_text()
    assert "my_vae.vae_module.VAEModule" in model_cfg
    assert "my_vae.models.encoder.Encoder" in model_cfg
    assert "my_vae.models.decoder.Decoder" in model_cfg


def test_vae_mnist_defaults(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "mnist")
    model_cfg = (out / "configs" / "model" / "default_model.yaml").read_text()
    assert "in_channels: 1" in model_cfg
    assert "[28, 28]" in model_cfg
    datamodule = (out / "src" / "test_vae" / "data" / "datamodule.py").read_text()
    assert "MNIST" in datamodule


def test_vae_default_model_config(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "defaults")
    model_cfg = (out / "configs" / "model" / "default_model.yaml").read_text()
    assert "beta: 1.0" in model_cfg
    assert "kl_warmup_epochs: 0" in model_cfg
    assert "torch.nn.Sigmoid" in model_cfg


def test_vae_skip_mnist_data(temp_dir: Path) -> None:
    out = _generate_vae(temp_dir / "skip")

    fake_data = out / "data" / "MNIST" / "raw" / "train-images-idx3-ubyte"
    fake_data.write_bytes(b"fake mnist content")
    original_mtime = fake_data.stat().st_mtime

    copier.run_copy(
        src_path=str(VAE_TEMPLATE),
        dst_path=str(out),
        data={"project_name": "test_vae", "user_name": "Test Author", "description": "Test", "python_version": "3.12"},
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    assert fake_data.stat().st_mtime == original_mtime
