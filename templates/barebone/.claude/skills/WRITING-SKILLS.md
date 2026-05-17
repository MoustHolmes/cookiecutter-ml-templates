# Writing skills for this repo

How to add new skills to `.claude/skills/` — the conventions this repo's skills
follow, and a fill-in-the-blanks template for the case you'll hit most often:
**a docs skill for a new library** when you add a template that uses it.

This guide is itself written to be read by a human. If you want Claude to help
*author* a skill, point it at this file.

---

## Part 1 — The rules every skill follows

These come from Anthropic's official skill-authoring guidance, the
obra/superpowers writing-skills skill, and the mattpocock/skills repo. They're
not arbitrary — each one fixes a specific failure mode.

### The description is the whole game

At idle, Claude sees *only* the `name` and `description` of each skill — the
body isn't loaded until the description triggers. A perfect body behind a vague
description never runs.

Rules for the description:

1. **Third person, declarative.** "Provides authoritative pixi
   documentation..." Not "Use this to..." or "I help with...". Inconsistent
   point-of-view across skills measurably hurts triggering, because all the
   descriptions share one system-prompt list.
2. **Two-part structure: what, then when.** First sentence(s): what the skill
   does. Then: the trigger conditions — "Use when...".
3. **Triggers are situations and user phrases, not topics.** Bad: "Use for
   PyTorch questions." Good: "Use when the user names a PyTorch version, hits
   a deprecation warning, or asks about `torch.compile`." Quote what the user
   would actually say.
4. **Be a little pushy.** Claude under-triggers skills by default — it tends to
   answer from memory for anything that feels easy. Counter it: "Use even for
   a 'simple' Trainer flag question; the defaults move."
5. **No workflow in the description.** Don't summarize the steps. If the
   description summarizes the body, Claude may act on the summary and never
   open the file. Triggers only.
6. **Under ~1024 characters.** It's a system-prompt resident; keep it tight.

### The body has bones, not just content

Flat prose is hard for Claude to act on under pressure. The skills in this repo
use a consistent skeleton:

- **One bolded anchor line near the top** — "**The skill is X.**" — that says
  where the real difficulty is and where to spend effort. Every workflow skill
  has exactly one.
- **Phases with explicit gates** when there's a real sequence. "Gate: name the
  bottleneck class before opening a profiler." A gate is a stop condition —
  Claude shouldn't proceed past it without having done the thing.
- **Named anti-patterns.** Not just "do X" but "here is the specific wrong
  thing people do, here's why it's wrong." Named anti-patterns are stickier
  than positive instructions. ("Guess-and-check thrashing", "Profiling step
  0".)
- **A tickable checklist at the end.** Literal `[ ]` boxes, concrete and
  verifiable, not prose. It's what Claude self-checks against.
- **A "when to skip" section** for anything advisory. Telling Claude when *not*
  to trigger is as valuable as when to — it prevents noise.

### Keep it lean, split when it grows

- SKILL.md body should be short. Anthropic's rough line is ~500 lines as a hard
  ceiling, but mattpocock targets ~100 and it shows — those skills are crisp.
  Aim for under ~120 lines.
- Everything in the body loads into context on trigger, competing with the
  actual conversation. Every line costs.
- When a skill genuinely needs more depth, **split into sibling files** and
  link them: `skill-name/SKILL.md` + `skill-name/reference.md`. The sibling
  loads only when Claude follows the link. This is "progressive disclosure
  within a skill."
- Add a `scripts/` subfolder if there's a deterministic operation (validation,
  formatting) — a script Claude runs costs only its output in tokens, not its
  source.

### Other conventions

- **Explain why, not just what.** "Explaining why is more effective than piling
  on must" — Anthropic's own guidance. Claude follows reasoning better than it
  follows capitalized commands.
- **No time-sensitive content.** No "as of 2026", no "the latest version is
  X". Skills outlive those statements. Pin versions where needed, but frame
  them as "the project's pin", not "the current release".
- **Consistent terminology.** Pick one term for a concept and use it
  everywhere — within the skill and across skills.
- **One skill, one job.** If a skill is accumulating a second responsibility,
  that's a second skill. Mega-skills trigger unreliably and are hard to
  maintain.
- **Reference other skills by name** when work hands off ("defer to
  `ml-profiling`"). Skills compose; they don't need to be self-contained.

### Test before trusting

Untested skills have issues — always. The cheap test: open a fresh Claude Code
session and throw **realistic, messy prompts** at it (not clean ones). Check
two things: does the right skill trigger, and does it produce the right
behavior. If it doesn't trigger, the description is missing the words the
prompt actually used — fix the description, not the body.

Good test prompt: "ugh my lightning run has been going for 4h and gpu util is
like 30%, whats wrong" — messy, lowercase, how people actually type.
Bad test prompt: "Please diagnose the performance bottleneck in my training
run." — too clean; real users don't write this.

---

## Part 2 — Template: a docs skill for a new library

This is the case you'll hit repeatedly: you add a template that uses some
library (say, `einops`, `accelerate`, `optuna`, `polars`), and you want Claude
to have version-correct docs for it instead of stale recall.

### Step 1 — Decide if it even needs a docs skill

A docs skill earns its place when **at least one** of these is true:

- The library is **newer than Claude's training data** or **evolves fast**
  (pixi, uv — the strongest case).
- The library has a **large API surface that shifts between versions**
  (PyTorch, Lightning).
- The library is a **known hallucination zone** — Claude is confidently wrong
  about it (Hydra).

If none hold — the library is small, stable, and well-known (`tqdm`,
`pathlib`) — **don't write a skill.** Claude's memory is fine. A skill that
adds nothing is pure context-noise tax.

### Step 2 — Check for an `llms.txt`

Before writing, check whether the library publishes one:
- Try `https://<docs-domain>/llms.txt` and `.../llms-full.txt`.
- Search "<library> llms.txt".

If it exists, the skill is mostly "fetch the llms.txt index first, then the
page it points to" — much less manual URL curation. pixi has one; lean on it.

### Step 3 — Fill in the template

Copy this into `.claude/skills/<library>-docs/SKILL.md` and replace every
`<...>`:

```markdown
---
name: <library>-docs
description: Provides authoritative <Library> documentation by fetching from
  <docs-domain> instead of relying on training-data recall. Use when working
  with <the 3-5 most common API surfaces>, or when the user mentions
  <library-name or distinctive filenames/commands>. <One sentence on WHY recall
  is risky here — newer than training data / large shifting API / hallucination
  zone.>
---

# <Library> documentation

<2-3 sentences: what the library is, and the specific reason Claude's memory of
it is unreliable. Be concrete — "the artifact API had quiet breaking changes",
not "it changes sometimes".>
**<Bolded anchor: the one-line rule. Usually "Fetch before answering anything
beyond <trivial baseline>.">**

## Canonical sources

<If there's an llms.txt, list it FIRST and say "fetch this first".>
<Then 6-12 deep links to the highest-traffic pages. Format as a flat list.
Pin to a version if the library serves per-version docs; say which version and
tell the reader to swap it for the project's pin.>

- <Index>: <url>
- <Topic>: <url>
- ...

## How to use

<2-4 numbered points: for THIS kind of question, fetch THIS page. Name the
specific traps — the flags/concepts that are the usual confusion sources.>

## Common traps

<3-6 bullets: the specific things Claude gets wrong about this library. This is
the highest-value section — it's the "gotchas". Grow it over time as you catch
Claude being wrong.>

## When to skip the fetch

Skip for: <the genuinely trivial, stable, well-known basics>.

Fetch for: <the version-dependent, the advanced, the recently-changed, anything
where the user named a version>.

## Checklist

​```
[ ] Topic matched to a canonical URL (llms.txt index first if one exists)
[ ] Version matched to the project's pin where the library is versioned
[ ] Answer reflects the fetched page, not pre-fetch memory
[ ] <one library-specific check — e.g. "RL video uses wandb.Video, not gym.monitor">
​```
```

### Step 4 — Wire it into `ml-templates`

Open `.claude/skills/ml-templates/SKILL.md`, find the "Division of labor with
the docs skills" list, and add a line:

```
- `<library>-docs` — <the surfaces it covers>
```

That's what tells the project skill to route questions to it.

### Step 5 — Test it

Fresh Claude Code session. A realistic prompt that should trigger it ("how do I
do <common task> with <library> again"), and one that shouldn't (a trivial
basic usage). Confirm it triggers on the first and stays quiet on the second.
If it under-triggers, add the missing words to the description's trigger
clause.

---

## Part 3 — Quick reference

**Workflow skill** (debugging, profiling, a process): needs the full skeleton —
anchor, phases with gates, named anti-patterns, checklist. Look at
`ml-debugging` or `setup-project` as the model.

**Docs skill** (version-correct library reference): use the Part 2 template.
Lighter — canonical sources, how-to-use, common traps, skip section, checklist.
No phase gates needed; fetching isn't really sequential. Look at `pytorch-docs`
or `pixi-docs`.

**Convention skill** (project-specific rules, like `ml-templates`): mostly a
structured list of conventions + workflows + a checklist. No anchor needed if
it's pure reference rather than a process.

**When in doubt:**
- One job per skill.
- Description is third-person, what-then-when, situational triggers, a little
  pushy.
- Body under ~120 lines; split to sibling files if longer.
- End with a tickable checklist.
- Test with messy prompts before trusting it.

**External references worth reading:**
- Anthropic's skill-authoring best practices (platform.claude.com docs)
- `obra/superpowers` → `skills/writing-skills/SKILL.md`
- `mattpocock/skills` → `skills/productivity/write-a-skill/` — and read
  `skills/engineering/diagnose/` as an example of a well-built workflow skill
