---
name: pytorch-docs
description: Provides authoritative, version-correct PyTorch documentation by fetching from docs.pytorch.org instead of relying on training-data recall. Use when working with `torch.*` APIs — tensor ops, autograd, nn.Module, optimizers, AMP, dataloaders, hooks, distributed, torch.compile — and especially when the user names a PyTorch version, hits a deprecation warning, or asks about anything where the API may have shifted between releases.
---

# PyTorch documentation

PyTorch's API surface is large and changes between versions, especially around
`torch.compile`, AMP, distributed, and dataloader internals. When a question
touches any non-trivial PyTorch API, **fetch the relevant docs page rather than
answering from memory** — Claude's recall here is frequently a version or two
stale.

## Canonical sources

Docs live under `docs.pytorch.org/docs/<version>/`. Match the version to what
the project pins (check `pixi.toml` / `pyproject.toml` / `pip freeze`). If the
version is unknown, default to `stable`:

- Index: https://docs.pytorch.org/docs/stable/
- Tensors: https://docs.pytorch.org/docs/stable/tensors.html
- `torch.nn`: https://docs.pytorch.org/docs/stable/nn.html
- `torch.optim`: https://docs.pytorch.org/docs/stable/optim.html
- Autograd: https://docs.pytorch.org/docs/stable/autograd.html
- DataLoader / Dataset: https://docs.pytorch.org/docs/stable/data.html
- `torch.compile`: https://docs.pytorch.org/docs/stable/torch.compiler.html
- AMP: https://docs.pytorch.org/docs/stable/amp.html
- Distributed: https://docs.pytorch.org/docs/stable/distributed.html
- Tutorials (separate domain): https://docs.pytorch.org/tutorials/

## How to use

1. Identify the topic, fetch the matching page above.
2. Pages are large — fetch with a focused target in mind ("find the section on
   `pin_memory`"), don't dump the whole page into context.
3. For a specific function, prefer its direct URL:
   `https://docs.pytorch.org/docs/stable/generated/torch.gather.html` — same
   pattern for any `torch.*` symbol.

## When to skip the fetch

Skip for: basic tensor creation and arithmetic, common indexing, the standard
training-loop skeleton — stable across versions and well-represented in
training data.

Fetch for: anything involving `torch.compile`, anything async or distributed,
anything where the user names a version, anything where the first instinct
produces a deprecation warning.

## Checklist

```
[ ] Topic matched to a canonical URL (or a torch.* symbol's direct page)
[ ] Version matched to the project's pin, or stable used deliberately
[ ] Answer reflects the fetched page, not pre-fetch memory
```
