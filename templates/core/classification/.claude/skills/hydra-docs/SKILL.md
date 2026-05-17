---
name: hydra-docs
description: Provides authoritative, version-correct Hydra documentation by fetching from hydra.cc instead of relying on training-data recall. Use when working with Hydra config composition, config groups, structured configs, the defaults list, `@hydra.main`, `instantiate`/`_target_`, OmegaConf interpolation, override grammar, or multirun/sweepers. Hydra is a high-hallucination area — old StackOverflow answers for Hydra 1.0/1.1 still rank high — so fetch even when the answer feels obvious.
---

# Hydra documentation

Hydra is a high-hallucination zone. The compose API, structured configs, and
the `_target_` instantiation pattern are subtly wrong in much of Claude's
training data because the API evolved across 1.0 → 1.1 → 1.2 → 1.3 and stale
answers still rank high in search. **Fetch authoritative docs before answering
any Hydra question that isn't trivially basic.**

## Canonical sources

Pinned to 1.3 (current stable). Update the version in URLs if the project pins
a newer major.

- Index: https://hydra.cc/docs/intro/
- Tutorial – basic: https://hydra.cc/docs/tutorials/intro/
- Tutorial – structured configs: https://hydra.cc/docs/tutorials/structured_config/intro/
- Config groups: https://hydra.cc/docs/tutorials/basic/your_first_app/config_groups/
- Defaults list: https://hydra.cc/docs/advanced/defaults_list/
- `instantiate` / `_target_`: https://hydra.cc/docs/advanced/instantiate_objects/overview/
- OmegaConf interpolation: https://omegaconf.readthedocs.io/en/latest/usage.html#variable-interpolation
- Override grammar: https://hydra.cc/docs/advanced/override_grammar/basic/
- Multirun & sweepers: https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/
- Compose API (for tests/notebooks): https://hydra.cc/docs/advanced/compose_api/

## How to use

1. `_target_` questions → fetch the instantiate page. `_partial_`,
   `_recursive_`, `_convert_` are the usual sources of confusion.
2. "How do I override X from the CLI" → fetch the override grammar page rather
   than guessing syntax for nested keys, list items, or appending to defaults.
3. Config group / defaults list questions → fetch the defaults list page. The
   `@package` directive and the special `_self_` entry are non-obvious and
   frequently misremembered.

## Common traps

- `defaults` list ordering matters. `_self_` placement decides whether the
  current config or the included group wins on key conflicts.
- `MISSING` (the required-field sentinel) comes from `omegaconf`, not `hydra`.
- `hydra.utils.instantiate` vs `hydra.utils.call` — different semantics.
- `${...}` interpolation is lazy. `${oc.env:VAR,default}` is the current way to
  read env vars; `${env:...}` is the deprecated older form.

## When to skip the fetch

Skip for: explaining what Hydra is at a high level, or a single trivial
`config.yaml` with no groups.

Fetch for: anything with config groups, the defaults list, `_target_`
instantiation, override syntax, structured configs, or a named Hydra version.

## Project convention

In this repo, configs live under `configs/` in each generated template. Models,
datamodules, and optimizers always use `_target_` instantiation — no manual
`__init__` calls in template code. See `templates/barebone/configs/` for the
canonical layout.

## Checklist

```
[ ] Topic matched to a canonical URL
[ ] Version matched to the project's pin (URL edited if not 1.3)
[ ] _target_ / defaults-list / override answers verified against the page
```
