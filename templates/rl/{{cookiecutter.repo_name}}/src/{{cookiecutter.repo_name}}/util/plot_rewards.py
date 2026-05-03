"""Utility for plotting episodic reward curves.

Example usage::

    from {{cookiecutter.repo_name}}.util.plot_rewards import plot_reward_curve

    plot_reward_curve(
        rewards=[...],
        window=50,
        title="SAC on Pendulum-v1",
        save_path="outputs/reward_curve.png",
    )
"""

from __future__ import annotations

import numpy as np


def plot_reward_curve(
    rewards: list[float],
    window: int = 50,
    title: str = "Episode Reward",
    save_path: str | None = None,
) -> None:
    """Plot a smoothed episode reward curve.

    Args:
        rewards: List of per-episode total rewards.
        window: Rolling-average window size for smoothing.
        title: Plot title.
        save_path: If provided, save the figure to this path instead of
                   displaying interactively.
    """
    import matplotlib.pyplot as plt

    rewards_arr = np.array(rewards, dtype=np.float32)
    episodes = np.arange(1, len(rewards_arr) + 1)

    # Raw rewards (transparent)
    plt.figure(figsize=(10, 4))
    plt.plot(episodes, rewards_arr, alpha=0.3, color="steelblue", label="Raw")

    # Smoothed rewards
    if len(rewards_arr) >= window:
        kernel = np.ones(window) / window
        smoothed = np.convolve(rewards_arr, kernel, mode="valid")
        plt.plot(
            episodes[window - 1:],
            smoothed,
            color="steelblue",
            linewidth=2,
            label=f"Smoothed (w={window})",
        )

    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title(title)
    plt.legend()
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.show()
