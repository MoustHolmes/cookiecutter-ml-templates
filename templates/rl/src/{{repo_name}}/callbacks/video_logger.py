"""WandB video logging callback for reinforcement learning.

:class:`VideoLoggerCallback` periodically renders a full greedy episode
and uploads it as a video to Weights & Biases, letting you visually inspect
how the policy evolves throughout training.

Uses ``gymnasium.wrappers.RecordVideo`` to write the episode to an mp4 file
on disk, then passes the file path to ``wandb.Video`` — the approach
recommended by the WandB Gymnasium integration docs.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import torch
import lightning as L
import gymnasium as gym
from gymnasium.wrappers import RecordVideo


class VideoLoggerCallback(L.Callback):
    """Renders a greedy episode and logs it as a WandB video.

    At the end of every ``log_every_n_epochs`` training epochs the callback:

    1. Creates a *separate* ``RecordVideo``-wrapped environment so the
       training environment is never disturbed.
    2. Runs one deterministic episode using the agent's greedy policy.
    3. Passes the recorded mp4 file to ``wandb.Video`` for upload.

    Args:
        log_every_n_epochs: How often (in Lightning epochs) to record a video.
        fps: Frame-rate for the uploaded video.
        max_episode_steps: Hard cap on episode length to avoid runaway rollouts.
            ``None`` uses the environment's own time limit.
    """

    def __init__(
        self,
        log_every_n_epochs: int = 50,
        fps: int = 30,
        max_episode_steps: int | None = 500,
    ) -> None:
        super().__init__()
        self.log_every_n_epochs = log_every_n_epochs
        self.fps = fps
        self.max_episode_steps = max_episode_steps

    def on_train_epoch_end(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """Render and log a video episode.

        Args:
            trainer: The active Lightning trainer.
            pl_module: The agent LightningModule (SACModule or TD3Module).
        """
        if (trainer.current_epoch + 1) % self.log_every_n_epochs != 0:
            return

        # WandB logger must be active (skipped during fast_dev_run / no logger)
        if trainer.logger is None or not hasattr(trainer.logger, "experiment"):
            return

        dm = trainer.datamodule
        if dm is None:
            return

        try:
            import wandb
        except ImportError:
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = self._record_episode(pl_module, dm, tmpdir)
            if video_path is None:
                return

            try:
                trainer.logger.experiment.log(
                    {
                        "eval/episode_video": wandb.Video(
                            str(video_path),
                            fps=self.fps,
                            format="mp4",
                            caption=f"Epoch {trainer.current_epoch + 1}",
                        )
                    },
                    step=trainer.global_step,
                )
            except Exception as exc:
                # Never crash training because of a logging failure — but do warn
                import warnings
                warnings.warn(f"VideoLoggerCallback: failed to log video to WandB: {exc}", stacklevel=2)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _record_episode(
        self,
        pl_module: L.LightningModule,
        dm: L.LightningDataModule,
        video_dir: str,
    ) -> Path | None:
        """Roll out one greedy episode and save it as an mp4 via RecordVideo.

        A fresh environment is created and torn down inside this method
        so that the training environment (``dm.env``) is untouched.

        Args:
            pl_module: Agent module with an ``actor`` attribute.
            dm: Datamodule with ``hparams.env_id`` and ``_maybe_normalize``.
            video_dir: Directory where the mp4 will be written.

        Returns:
            Path to the recorded mp4, or ``None`` if recording failed.
        """
        env_id: str = dm.hparams.env_id

        try:
            base_env = gym.make(env_id, render_mode="rgb_array")
            # Record exactly one episode (episode_trigger always returns True)
            env = RecordVideo(
                base_env,
                video_folder=video_dir,
                episode_trigger=lambda _: True,
                disable_logger=True,
            )
        except Exception as exc:
            import warnings
            warnings.warn(f"VideoLoggerCallback: could not create render env: {exc}", stacklevel=2)
            return None

        pl_module.eval()
        try:
            obs, _ = env.reset()
            obs = obs.astype(np.float32)
            done = False
            step = 0

            with torch.no_grad():
                while not done:
                    obs_normalised = dm._maybe_normalize(obs)
                    obs_t = torch.tensor(obs_normalised).unsqueeze(0).to(pl_module.device)

                    action_np = pl_module.act_deterministic(obs_t).squeeze(0).cpu().numpy()
                    if isinstance(base_env.action_space, gym.spaces.Discrete):
                        step_action = int(np.round(float(action_np.flat[0])))
                    else:
                        step_action = action_np.astype(np.float32)
                    obs, _, terminated, truncated, _ = env.step(step_action)
                    obs = obs.astype(np.float32)
                    done = bool(terminated) or bool(truncated)
                    step += 1

                    if self.max_episode_steps is not None and step >= self.max_episode_steps:
                        break
        except Exception as exc:
            import warnings
            warnings.warn(f"VideoLoggerCallback: episode recording failed: {exc}", stacklevel=2)
            return None
        finally:
            env.close()
            pl_module.train()

        # RecordVideo names files like "rl-video-episode-0.mp4"
        mp4_files = sorted(Path(video_dir).glob("*.mp4"))
        return mp4_files[0] if mp4_files else None
