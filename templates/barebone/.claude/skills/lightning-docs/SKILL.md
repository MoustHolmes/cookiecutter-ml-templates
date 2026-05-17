---
name: lightning-docs
description: Provides authoritative, version-correct PyTorch Lightning documentation by fetching from lightning.ai instead of relying on training-data recall. Use when working with the Lightning Trainer, LightningModule or LightningDataModule, callbacks, strategies (DDP/FSDP), loggers, checkpointing, or Fabric — Lightning's API churns hard across versions, so this is the stack's highest-risk library for stale recall. Use even for a "simple" Trainer flag question; the defaults move.
---

# PyTorch Lightning documentation

Lightning is the library in this stack where Claude's training data hurts most.
Hooks have been renamed, Trainer flags moved, and the recommended patterns for
mixed precision, distributed strategies, and callbacks shifted across 2.0 → 2.2
→ 2.4 → 2.5. **Fetch the docs before writing any non-trivial Lightning code,
and before stating any Trainer default.**

## Canonical sources

Pinned to 2.5 by default — replace the version in the URL with the project's
pin if different. Lightning serves a separate doc tree per version, and the
`stable` alias redirects in ways that confuse caching.

- Index: https://lightning.ai/docs/pytorch/stable/
- Trainer: https://lightning.ai/docs/pytorch/stable/common/trainer.html
- LightningModule: https://lightning.ai/docs/pytorch/stable/common/lightning_module.html
- LightningDataModule: https://lightning.ai/docs/pytorch/stable/data/datamodule.html
- Callbacks index: https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html
- Callback API: https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.Callback.html
- Loggers (incl. WandbLogger): https://lightning.ai/docs/pytorch/stable/extensions/logging.html
- Checkpointing: https://lightning.ai/docs/pytorch/stable/common/checkpointing.html
- Strategies (DDP/FSDP/etc.): https://lightning.ai/docs/pytorch/stable/extensions/strategy.html
- Mixed precision: https://lightning.ai/docs/pytorch/stable/common/precision.html
- Fabric (low-level): https://lightning.ai/docs/fabric/stable/

## How to use

1. Trainer flag questions → fetch the Trainer page and grep the flag name.
   Never guess a default; they've changed.
2. Callback patterns (logging images, gradient stats) → fetch the Callback API
   page first. The hook names and signatures are the trap.
3. W&B integration inside Lightning → fetch the Loggers page, not the W&B docs.
   Lightning wraps `wandb` and the wrapper has its own quirks.

## Common traps

- `Trainer(strategy=...)` replaced older `accelerator`/`gpus` flag
  combinations. Verify against current docs.
- `LightningModule.log()` arguments (`on_step`, `on_epoch`, `prog_bar`,
  `sync_dist`) — defaults vary by hook context. Don't assume.
- `on_train_batch_end` and sibling hook signatures have changed; the `outputs`
  argument is no longer always present.
- `wandb.gym.monitor()` auto-upload is broken for Gymnasium ≥1.0 — use
  in-memory frame collection with `wandb.Video(np_array)` instead.

## When to skip the fetch

Skip for: the bare LightningModule skeleton (`training_step`,
`configure_optimizers`, `forward`) and one-liners like
`Trainer(max_epochs=N).fit(model, dm)` — stable.

Fetch for: any named Lightning version, distributed strategies, custom
callbacks, manual optimization, precision, or any Trainer default.

## Checklist

```
[ ] Topic matched to a canonical URL
[ ] Version matched to the project's pin (URL edited if not 2.5)
[ ] No Trainer default stated from memory — all verified against the page
```
