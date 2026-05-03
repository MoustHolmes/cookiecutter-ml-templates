"""Episodic reward logging callback for reinforcement learning.

:class:`EpisodeLoggerCallback` runs greedy evaluation rollouts at the end of
each evaluation epoch and logs mean episode reward and length to the trainer's
logger (e.g. Weights & Biases).
"""

from __future__ import annotations

import gymnasium as gym
import numpy as np
import torch
import lightning as L


class EpisodeLoggerCallback(L.Callback):
    """Periodically evaluates the agent with greedy rollouts and logs metrics.

    At the end of every ``log_every_n_epochs`` training epochs the callback:

    1. Runs ``eval_episodes`` deterministic episodes in the datamodule's
       environment using the actor's greedy (mean) action.
    2. Logs ``eval/mean_episode_reward`` and ``eval/mean_episode_length``
       to the trainer logger.

    Args:
        eval_episodes: Number of greedy episodes to run per evaluation.
        log_every_n_epochs: How often (in Lightning epochs) to run evaluation.
    """

    def __init__(self, eval_episodes: int = 5, log_every_n_epochs: int = 10) -> None:
        super().__init__()
        self.eval_episodes = eval_episodes
        self.log_every_n_epochs = log_every_n_epochs

    def on_train_epoch_end(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """Run evaluation rollouts and log results.

        Args:
            trainer: The active Lightning trainer.
            pl_module: The agent LightningModule (SACModule or TD3Module).
        """
        if (trainer.current_epoch + 1) % self.log_every_n_epochs != 0:
            return

        dm = trainer.datamodule
        # RolloutDataModule (PPO) doesn't have dm.env — skip rollout-based eval
        if dm is None or not hasattr(dm, "env") or dm.env is None:
            return

        rewards: list[float] = []
        lengths: list[int] = []

        pl_module.eval()
        with torch.no_grad():
            for _ in range(self.eval_episodes):
                obs, _ = dm.env.reset()
                obs = obs.astype(np.float32)
                episode_reward = 0.0
                episode_length = 0
                done = False

                while not done:
                    obs_normalised = dm._maybe_normalize(obs)
                    obs_t = torch.tensor(obs_normalised).unsqueeze(0).to(pl_module.device)
                    action = pl_module.act_deterministic(obs_t)
                    action_np = action.squeeze(0).cpu().numpy()
                    if isinstance(dm.env.action_space, gym.spaces.Discrete):
                        step_action = int(np.round(float(action_np.flat[0])))
                    else:
                        step_action = action_np.astype(np.float32)
                    obs, reward, terminated, truncated, _ = dm.env.step(step_action)
                    obs = obs.astype(np.float32)
                    episode_reward += float(reward)
                    episode_length += 1
                    done = bool(terminated) or bool(truncated)

                rewards.append(episode_reward)
                lengths.append(episode_length)

        pl_module.train()

        mean_reward = float(np.mean(rewards))
        mean_length = float(np.mean(lengths))

        pl_module.log("eval/mean_episode_reward", mean_reward, prog_bar=True)
        pl_module.log("eval/mean_episode_length", mean_length, prog_bar=False)
