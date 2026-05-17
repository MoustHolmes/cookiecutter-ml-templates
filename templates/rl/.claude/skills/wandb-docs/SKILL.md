---
name: wandb-docs
description: Provides authoritative Weights & Biases documentation by fetching from docs.wandb.ai instead of relying on training-data recall. Use when working with `wandb.init`, logging metrics/images/videos/tables, artifacts, the model registry, sweeps, the Lightning `WandbLogger` integration, or offline/resume behavior. W&B's surface has grown a lot and the artifact and integration APIs have had quiet breaking changes — fetch for anything past `init` + `log`.
---

# Weights & Biases documentation

W&B's surface area has grown substantially — artifacts, registry, sweeps,
reports, weave — and the SDK has had quiet breaking changes, especially around
the artifact APIs and the Lightning integration. **Fetch the docs for anything
beyond `wandb.init` + `wandb.log`.**

## Canonical sources

W&B doesn't expose per-version doc URLs; `docs.wandb.ai` serves "current."
Usually fine since W&B mostly adds rather than breaks, but re-check for newer features.
- LLM index (start here): https://docs.wandb.ai/llms.txt
- Index: https://docs.wandb.ai/
- Python SDK reference: https://docs.wandb.ai/ref/python/
- `wandb.init`: https://docs.wandb.ai/ref/python/init/
- `wandb.log` & data types: https://docs.wandb.ai/guides/track/log/
- Logging images & media: https://docs.wandb.ai/guides/track/log/media/
- Artifacts (overview): https://docs.wandb.ai/guides/artifacts/
- Artifacts API: https://docs.wandb.ai/ref/python/artifact/
- Model registry: https://docs.wandb.ai/guides/registry/
- Sweeps: https://docs.wandb.ai/guides/sweeps/
- Lightning integration: https://docs.wandb.ai/guides/integrations/lightning/
- Offline / resume: https://docs.wandb.ai/guides/track/launch/

## How to use

1. "Log X" questions → fetch the data types page. W&B has specific classes
   (`wandb.Image`, `wandb.Video`, `wandb.Table`, `wandb.Histogram`) each with
   their own constructor gotchas.
2. Artifact questions → fetch the overview *and* the API reference; the
   conceptual flow (create → add → log → use) is half the answer.
3. Lightning integration → use the W&B Lightning integration page, not the
   Lightning loggers page. It covers `log_model="all"`, media logging, and the
   current correct way to log images during training.

## Common traps

- `wandb.Image` accepts numpy arrays, PIL images, paths, or tensors — but
  tensor handling assumes CHW order. Verify against the data types docs.
- For RL video logging, **don't** use `wandb.gym.monitor()` — broken for
  Gymnasium ≥1.0. Collect frames in memory as a (T, C, H, W) numpy array and
  pass to `wandb.Video(arr, fps=...)`.
- `WandbLogger(log_model="all")` logs checkpoints as artifacts; the older
  `save_top_k` / file-path approach is deprecated.
- `wandb.init(reinit=True)` semantics changed — check current docs before
  relying on it for multi-model-per-process scripts.
- Project / entity / mode should be read from Hydra config, never hardcoded.

## When to skip the fetch

Skip for: a basic `wandb.init(project=...)` + `wandb.log({"loss": x})` pattern.

Fetch for: anything with artifacts, the registry, sweeps, media logging, the
Lightning integration, or offline/resume behavior.

## Checklist

```
[ ] Topic matched to a canonical URL
[ ] Media/artifact answers verified against the page, not memory
[ ] RL video logging uses wandb.Video(np_array), never wandb.gym.monitor()
```
