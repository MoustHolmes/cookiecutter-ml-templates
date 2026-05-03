"""Online running statistics for observation normalisation.

Deep RL networks are sensitive to input scale.  :class:`RunningMeanStd`
tracks a running mean and variance using Welford's online algorithm and
exposes a :meth:`normalize` method that zero-centres and unit-scales
observations, with optional clipping to prevent extreme inputs.

Usage inside :class:`~{{cookiecutter.repo_name}}.data.env_datamodule.RLDataModule`:

.. code-block:: python

    normalizer = RunningMeanStd(shape=(obs_dim,))
    normalizer.update(batch_of_obs)          # update statistics
    normalised = normalizer.normalize(obs)   # apply normalisation
"""

from __future__ import annotations

import numpy as np


class RunningMeanStd:
    """Welford's online algorithm for running mean and variance.

    Maintains a numerically stable estimate of the mean and variance across
    all observations seen during training.  Thread-safety is not guaranteed
    — use in a single-process training loop only.

    Args:
        shape: Shape of the quantity being tracked (e.g. ``(obs_dim,)`` for
               a 1-D observation).
        epsilon: Small constant added to the variance estimate to avoid
                 division by zero during normalisation.
    """

    def __init__(self, shape: tuple[int, ...] = (), epsilon: float = 1e-8) -> None:
        self.mean = np.zeros(shape, dtype=np.float64)
        self.var = np.ones(shape, dtype=np.float64)
        self.count: float = epsilon

    def update(self, x: np.ndarray) -> None:
        """Update running statistics with a batch of observations.

        Uses the parallel/batch variant of Welford's algorithm so that the
        entire collected batch is incorporated in a single call.

        Args:
            x: Array of shape ``(N, *shape)`` containing ``N`` observations.
        """
        batch_mean = np.mean(x, axis=0)
        batch_var = np.var(x, axis=0)
        batch_count = x.shape[0]

        delta = batch_mean - self.mean
        total_count = self.count + batch_count

        new_mean = self.mean + delta * batch_count / total_count
        m_a = self.var * self.count
        m_b = batch_var * batch_count
        m_2 = m_a + m_b + delta ** 2 * self.count * batch_count / total_count
        new_var = m_2 / total_count

        self.mean = new_mean
        self.var = new_var
        self.count = total_count

    def normalize(self, x: np.ndarray, clip: float = 10.0) -> np.ndarray:
        """Normalise observations to approximately zero mean and unit variance.

        Args:
            x: Observation array of shape ``(*shape,)`` or ``(N, *shape)``.
            clip: Symmetric clip value applied after normalisation.  Prevents
                  extreme outliers from destabilising training.

        Returns:
            Normalised float32 array with the same shape as ``x``,
            clipped to ``[-clip, clip]``.
        """
        normalised = (x - self.mean) / np.sqrt(self.var + 1e-8)
        return np.clip(normalised, -clip, clip).astype(np.float32)
