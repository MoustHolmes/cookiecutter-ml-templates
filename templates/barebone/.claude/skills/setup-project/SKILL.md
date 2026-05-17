---
name: setup-project
description: Interviews the user about a project's goal, scope, and constraints, then writes a specific README.md and CLAUDE.md from the answers. Use when the user says "set up the project", "I just generated a template", "let's start a new project", "initialize this repo", or "the README is empty/wrong/outdated". Run this before writing any project-level docs — a README written from assumptions is worse than no README.
---

# Setting up a new project

**The skill is the interview.** A generic AI-written README is actively
harmful: it's confident and plausible while saying nothing. "This is a Python
project for machine learning" pattern-matches as informative and isn't.
"Trains a flow-matching model on protein backbones, evaluated against
RFdiffusion on the CASP15 holdout" is useful. The only way to get the second
kind is to ask. The drafting is mechanical; the interview is the work.

## Phase 1 — Read the repo first

Before asking anything, read what's already there: existing `README.md`,
`CLAUDE.md`, `pixi.toml`/`pyproject.toml`, the directory layout. Every
question you can answer from the repo is a question you must not ask the user.

## Phase 2 — Interview

Use `AskUserQuestion` (or equivalent), **one question at a time** — answers
inform follow-ups. Cover at minimum:

1. **The goal** — the *outcome*, not the methods. "Train a model that X",
   "Investigate whether Y", "Reproduce paper Z".
2. **Research or production-bound** — research optimizes for iteration speed
   and experiment tracking; production for testing and reproducibility.
3. **Success criterion** — a number, a comparison, a working demo. The README
   cannot be written without this.
4. **Scope now vs. eventually** — the README describes the MVP; CLAUDE.md may
   hint at the longer arc.
5. **Which template, and what's changing** — a fresh cookiecutter output keeps
   default conventions until told otherwise.
6. **Compute setup** — local GPU, a named cluster (Gefion/DCAI/SLURM), cloud.
   This shapes CLAUDE.md more than the README.
7. **Audience** — just you, a team, public. Sets tone and assumed background.

When an answer is vague, ask one or two follow-ups: "success looks like the
model converging" → "converges to what, measured how?" → a usable answer.

**Gate: do not draft until the goal and the success criterion are concrete.**
If either is still a vibe, the README will be a vibe.

## Phase 3 — Draft both files

They have different audiences and different jobs.

### README.md — for humans

Someone landing on the repo. In this order: **what is this** (one sentence,
says what it does), **why it exists** (one paragraph, the problem or
question), **how to run it** (the 30-second copy-pasteable quickstart),
**structure** (only the parts that matter), **where to learn more** (docs,
paper, W&B project).

Not in the README: marketing-style feature bullets, install instructions for
every OS, a long preamble before the quickstart, "TODO" sections, generic
jargon ("leveraging deep learning to..."). For style, defer to `writing-docs`.

### CLAUDE.md — for the agent

Claude Code on a future session. It needs: **repo orientation in ~5 lines**;
**project-specific conventions** that override generic defaults ("configs in
`configs/`, always `_target_` instantiation"); **commands the agent will
actually run** (`pixi run test`, not "run the tests"); **what not to do**
("don't add top-level deps without updating `pixi.toml`", "don't disable
failing tests — ask"); **pointers to skills** in `.claude/skills/`.

Not in CLAUDE.md: re-explanations of how PyTorch/Lightning work (that's what
skills are for), generic best practices Claude already follows, personality
instructions, or anything that belongs in a skill.

**Gate: CLAUDE.md stays under ~80 lines.** It loads every session. If a
section is growing long, it's a skill, not a CLAUDE.md addition.

## Phase 4 — Review and commit

Show both files to the user side by side. Ask what's wrong before committing —
the usual misses are a too-vague goal section or an overlooked compute
constraint. Iterate, then propose a clean starting commit:
`git add README.md CLAUDE.md && git commit -m "Initial project README and CLAUDE.md"`.

## Anti-patterns

**Drafting from inference.** The whole failure mode this skill exists to
prevent. If you catch yourself writing a goal statement the user never
confirmed, stop and ask.

**Dumping all seven questions at once.** Batched questions get batched,
shallow answers. One at a time, follow-ups where it's vague.

**Asking what the repo already answers.** Reading `pixi.toml` and then asking
"what libraries are you using" tells the user you didn't look. Phase 1 exists
to prevent this.

**Letting the user skip the interview entirely.** Some will say "just write
it." Push back once: *"READMEs written from inference tend to be generic and
miss what makes this project specific — can I ask three questions?"* If they
still decline, write a visibly skeletal README with `[clarify: ...]`
placeholders rather than hallucinating a confident goal.

## Stale-README variant

Same skill, different entry point. Open with: "The current README says <X> —
is that still accurate?" Staleness is usually one of two kinds: the *goal*
shifted (rewrite the top sections) or the *structure* changed (mechanical fix
to the layout section). Diagnose which before deciding how much to rewrite.

## Checklist

```
[ ] Repo state read before any question was asked
[ ] Goal and success criterion are concrete, not vibes
[ ] README leads with what-it-does, not "a project to..."
[ ] CLAUDE.md is under ~80 lines and has no library re-explanations
[ ] Both files shown to the user and iterated before commit
```
