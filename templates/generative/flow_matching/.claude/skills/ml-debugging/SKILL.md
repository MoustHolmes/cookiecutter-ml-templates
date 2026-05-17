---
name: ml-debugging
description: Diagnoses ML-specific bugs where training code runs but produces wrong results — NaN/flat loss, train/val divergence, models that learn nothing, suspiciously perfect metrics, OOM, distributed hangs. Use when the user says training "isn't working", "won't converge", "loss is NaN", "val accuracy is stuck", a model "works on a small batch but not at scale", or any ML result that looks wrong even though nothing crashed. Use even when the error resembles an ordinary Python exception — the silent ML bugs underneath are the dangerous ones.
---

# Debugging ML code

**The skill is classification.** ML bugs split into four kinds and each kind
has a different debugging strategy — picking the wrong strategy wastes hours.
A crash is the easy case. The dangerous case is code that runs to completion
and produces a plausible-looking wrong answer. Everything below hangs off
getting the classification right first.

For the general discipline (build a feedback loop, form falsifiable
hypotheses, change one variable at a time) defer to `diagnose` or
`systematic-debugging` if installed. This skill adds the ML-specific layer.

## Phase 1 — Classify the bug

Do not touch code until the bug is classified. The four kinds:

1. **Hard crash** — CUDA OOM, shape/dtype mismatch, exception with a stack
   trace. Easiest: the bug is usually within a few frames of the error.
2. **Silent numerical bug** — loss is NaN/Inf, gradients explode or vanish,
   values stuck. Medium: bisect the forward pass.
3. **Silent correctness bug** — training "works" but the model learns nothing,
   or learns the wrong thing. Hardest: the bug is almost never where you're
   looking, and it's usually in the data.
4. **Performance bug** — slow or memory-hungry but otherwise correct. Wrong
   skill: use `ml-profiling`, the toolset is entirely different.

**Gate: state which of the four this is before continuing.** If it could be
two of them (a crash that might be hiding a correctness bug), treat the
silent one as primary — it's the one that survives a superficial fix.

## Phase 2 — Apply the strategy for that class

### Class 1: Hard crash

- **Shape mismatch** — `print(x.shape)` at layer boundaries up to the error.
  Don't trust einops/`rearrange`; verify.
- **dtype mismatch** — AMP and `bfloat16` cause most. Check whether the op
  needs `float32` (softmax over long sequences, loss reduction).
- **CUDA OOM** — quick wins: smaller batch, gradient checkpointing, AMP. If it
  OOMs *after* N steps rather than at step 1, it's a leak, not a size problem
  — go to Class 2.
- **`device-side assert triggered`** — out-of-range index in an embedding
  lookup or loss `ignore_index`. Re-run with `CUDA_LAUNCH_BLOCKING=1` for a
  real stack trace.

### Class 2: Silent numerical bug

- Wrap forward+backward in `torch.autograd.detect_anomaly()` to localize the
  op. Remove it after — it's slow.
- Print `loss.item()`, gradient norms, weight norms for the first N steps. NaN
  traces back to: division by ~0, `log(0)`, `sqrt` of a negative, softmax over
  `-inf`, or an unstable loss formulation.
- AMP NaN: confirm the `GradScaler` is being stepped, and that no `float32`-only
  op is running inside the autocast region.
- Vanishing/exploding gradients: check init, activation, normalization; print
  `param.grad.norm()` per layer.

### Class 3: Silent correctness bug — check in this order, stop when found

This is the order on purpose: cheapest and most common first.

1. **Read the data.** Look at 10 real examples — inputs *and* labels — before
   reading any model code. Wrong labels, off-by-one indices, double-applied
   or missing normalization, leaked test set. Most "model isn't learning"
   bugs die here.
2. **Train/eval mode.** Is `model.eval()` called before validation?
   `BatchNorm`/`Dropout` behave completely differently.
3. **Killed gradients.** `torch.no_grad()` or `.detach()` in the wrong place.
4. **Loss function.** `CrossEntropyLoss` fed already-softmaxed inputs (it
   wants logits); `BCEWithLogitsLoss` fed sigmoided inputs; wrong reduction
   mode (`'sum'` vs `'mean'`).
5. **Optimizer scope.** Optimizing the wrong parameter set; "frozen" layers
   that aren't actually frozen.
6. **Metric implementation.** Especially custom metrics in `validation_step`.
   Verify on a tiny dataset where the answer is known.

### Class 4: Performance bug

Stop. This is the `ml-profiling` skill's job. Switch skills.

## Phase 3 — The single-batch test (the universal probe)

Whatever the class, this disambiguates more than any other single action:

**A correct model + training loop can drive loss to ~0 on a batch of 2
examples in a few hundred steps.**

- If it *can't* overfit two examples → the bug is in the model, loss, or
  optimizer. Not the data pipeline.
- If it *can* overfit but full training fails → the bug is in the data, the
  split, or the eval path.

Run this before any deep dive. It's 30 seconds and it halves the search space.

## Distributed / multi-GPU notes

These cut across the classes above:
- Sampler not set to `DistributedSampler` → every rank trains on the same data.
- `sync_dist=True` missing on logged metrics → ranks log different values.
- Hangs → usually mismatched collective ops between ranks (one rank exits
  early, or a conditional `all_reduce`).
- Per-rank seeding wrong — same when you wanted different (dropout masks) or
  different when you wanted same.

## Anti-patterns

**Guess-and-check thrashing.** Changing something, re-running the whole
training job, eyeballing the loss curve, changing something else. ML runs are
too slow and too noisy for this. Build a fast signal (single-batch overfit,
a unit test on the loss, a 20-step smoke run) and change one variable against
it.

**"It must be the framework."** It's almost never PyTorch/Lightning. The pivot
order when stuck: model → data → loss → optimizer → train-mode → *then*
consider the framework, and even then check the issue tracker before
believing it.

**Fixing the crash, ignoring the cause.** A shape error "fixed" with a
`.reshape()` that makes the error go away but silently scrambles a batch
dimension is now a Class 3 bug. When you fix a crash, confirm you fixed the
*cause*, not the symptom.

**Changing two things at once.** ML is non-deterministic enough already. Two
changes means you can't attribute the result, and one can mask the other.

## When 3+ fixes have failed

Stop fixing. The bug is in a layer you haven't questioned. Write a minimal
reproduction — smallest model, fewest examples, fixed seed. Writing the repro
usually surfaces the bug on its own; if it doesn't, you now have something a
colleague or an issue tracker can act on.

## Per-cycle checklist

```
[ ] Bug is classified (1 crash / 2 numerical / 3 correctness / 4 perf)
[ ] Single-batch overfit test has been run and its result interpreted
[ ] Only one variable changed since the last signal
[ ] The fix addresses the cause, not the symptom
[ ] A regression test or smoke check covers the bug (or absence noted)
[ ] Temporary instrumentation (detect_anomaly, debug prints) removed
```

## Project conventions

Debug logs and traces go in `outputs/debug/` (gitignored). Repro scripts go in
`tests/repro/` and must include the seed and full config that triggers the
bug. Don't commit model-state `.pkl` for repros — link the W&B run instead.
