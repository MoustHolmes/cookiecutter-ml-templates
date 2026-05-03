# Data Directory

This directory is reserved for offline datasets (e.g. for offline RL) or environment assets.

For standard online RL with Gymnasium environments (Pendulum, LunarLander, etc.) no data files
are needed — the environment generates experience on the fly during training.

## Replay Buffer

Experience collected during training is stored in an in-memory `ReplayBuffer` managed by
`RLDataModule`. It is not persisted to disk between runs by default.
