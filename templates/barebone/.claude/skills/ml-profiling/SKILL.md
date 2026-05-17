---
name: ml-profiling
description: Finds and interprets performance bottlenecks in ML training and inference — slow steps, low GPU utilization, memory leaks, dataloader stalls, poor multi-GPU scaling. Use when the user says training is "slow", "taking forever", "GPU usage is low", asks "why is this so slow", wants to "speed up training", or needs help reading profiler output (PyTorch Profiler, Lightning profilers, nvidia-smi, py-spy). Use even when the word "profile" never appears — "training is slow" is a profiling task.
---

# Profiling ML code

**The skill is classifying the bottleneck before measuring.** A workload is
GPU-bound, CPU-bound, IO-bound, or comm-bound, and each one points at a
different tool. Reaching for the PyTorch Profiler when the real problem is a
starved dataloader wastes an hour reading a trace that was never going to show
the cause. Two minutes of cheap signals first; the right profiler second.

## Phase 1 — Classify the bottleneck (cheap signals, ~2 min)

Run these *before* any profiler:

- **`nvidia-smi dmon -s u`** in a second terminal during training:
  - util consistently >85% → **GPU-bound**, profile GPU ops
  - util <50% with spikes → **CPU- or IO-bound**, the GPU is waiting
  - util sawtoothing 0→100→0 → **dataloader-bound**, classic starvation
- **`htop`** during training:
  - all cores pegged → **CPU-bound**, likely the dataloader workers
  - one core pegged, rest idle → single-threaded bottleneck somewhere
- **Multi-GPU**: if 1→2 GPUs gives <1.8× throughput → **comm-bound**.

**Gate: name the bottleneck class before opening a profiler.** The class
selects the tool. If signals are ambiguous, the SimpleProfiler in Phase 2 is
the tiebreaker — but still form a hypothesis first.

## Phase 2 — Profile with the matching tool

### GPU-bound or "don't know yet" → start with SimpleProfiler

Cheapest first profile if using Lightning, zero code beyond a flag:

```python
trainer = Trainer(profiler="simple", max_steps=100)
```

Per-hook breakdown. Read it **by ratio, not absolute time**:
- `training_step` should dominate. If it doesn't, the problem is elsewhere.
- `get_train_batch` significant → dataloader-bound, go to the dataloader
  section below.
- `on_*_end` callbacks >5% → an expensive callback (often an image-logging or
  W&B callback running every step).

### GPU-bound, need per-op detail → PyTorch Profiler

```python
from torch.profiler import profile, ProfilerActivity, schedule

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    schedule=schedule(wait=2, warmup=2, active=6, repeat=1),
    on_trace_ready=torch.profiler.tensorboard_trace_handler("./prof"),
    record_shapes=True,
) as prof:
    for step, batch in enumerate(loader):
        ...  # training step
        prof.step()
```

Reading it:
- **"Self CUDA time"** is the column that matters for GPU-bound work.
- Big gaps between CUDA kernels on the timeline → CPU-GPU sync, or CPU is the
  real bottleneck.
- `cudaStreamSynchronize` / `cudaMemcpy*` near the top → unnecessary CPU↔GPU
  transfers.
- `aten::item`, `aten::nonzero`, `aten::unique` → hidden synchronization
  points in your code, a common stall cause.

### Dataloader-bound → fix config before profiling deeper

If the signal said sawtooth, check these in order:
1. `num_workers` — start near `4 * num_gpus`; don't blindly maximize.
2. `pin_memory=True` for GPU training.
3. `persistent_workers=True` if epochs are short.
4. `prefetch_factor` — default 2, raise if samples are fast but irregular.
5. Still slow? `py-spy dump --pid <worker_pid>` to see what a worker is stuck
   on — usually image decode, network IO, or heavy augmentation.

Measure loader time directly to confirm:
```python
import time
it = iter(loader); t0 = time.perf_counter()
for _ in range(20): next(it)
print(f"avg fetch: {(time.perf_counter()-t0)/20*1000:.1f}ms")
```
If fetch time is >20% of `training_step` time, the loader is the bottleneck no
matter what the op profiler says.

### Memory bound / OOM → memory snapshot

```python
torch.cuda.memory._record_memory_history(max_entries=100_000)
...  # train a few steps
torch.cuda.memory._dump_snapshot("memory.pickle")
torch.cuda.memory._record_memory_history(enabled=None)
```
Open the `.pickle` at https://pytorch.org/memory_viz. Look for: memory growing
monotonically with step (a leak — accumulating loss tensors in a list, a
callback storing tensors without `.detach().cpu()`); one huge allocation
before OOM (needs activation checkpointing); many tiny allocations
(fragmentation — try `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`).

## Phase 3 — Fix, then re-profile

**Gate: every fix must be followed by a re-profile.** You cannot claim a
speedup you didn't measure. Re-run the same profile, compare the breakdown.

Fix the biggest ratio first; ignore anything under ~5% of step time (Amdahl's
law is unforgiving).

## Anti-patterns

**Profiling step 0.** CUDA caches are cold, cudnn is still benchmarking,
prefetch hasn't filled. The `wait`/`warmup` schedule exists for this reason —
use it. Step 0 numbers are noise.

**Profiling at batch size 1 "to isolate."** Batch size 1 changes which
component is the bottleneck entirely. Real bottlenecks only appear at real
batch sizes.

**Optimizing the op you recognize instead of the op that's slow.** It's
tempting to optimize the matmul you understand. Profile, then optimize what
the profile says — not what's familiar.

**Comparing wall-clock with profiling on vs. off.** The profiler has its own
overhead. Compare *relative breakdowns*, never absolute numbers across a
profiled and unprofiled run.

**Stacking `record_shapes` + `with_stack` + `profile_memory`.** They compound;
the overhead distorts the result. Enable only what the current question needs.

## Checklist

```
[ ] Bottleneck class named before any profiler was opened
[ ] Profiler matched to the class (not just "PyTorch Profiler by default")
[ ] Warmup steps skipped (wait/warmup schedule, or first steps discarded)
[ ] Fix targets the largest ratio, not the most familiar op
[ ] Re-profiled after the fix; speedup is measured, not assumed
```

## Project conventions

Profile artifacts go to `outputs/profiling/<run-name>/` (gitignored), with the
config used alongside. The `WandbLogger` can upload PyTorch Profiler traces as
artifacts — see `wandb-docs`. For nanoGPT-speedrun-style benchmarking, measure
steady-state tokens/sec on the target hardware, not total wall-clock — startup
amortizes differently across run lengths.
