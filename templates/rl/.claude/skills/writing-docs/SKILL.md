---
name: writing-docs
description: Writes and edits documentation for this repo following its house style — MkDocs Material, Diátaxis structure, direct no-marketing tone, Google-style docstrings. Use when the user asks to "document X", "write docs for Y", "explain Z in the docs", edit a README or MkDocs page, or write docstrings. Use even when the format isn't specified — the repo has conventions that override generic Markdown habits. Skip only for inline code comments and commit messages.
---

# Writing documentation for this project

**The skill is picking the right Diátaxis mode and staying in it.** The single
most common docs failure is one page trying to be a tutorial, a reference, and
an explanation at once. Decide which of the four a page is *before* writing a
line, and don't drift. The audience is ML engineers picking up a template for
real work — confident, specific, assumes competence, but explains *why*.

## Phase 1 — Pick the mode

Every page is exactly one of:

- **Tutorial** — learning-oriented. One specific hand-held path, working
  end-to-end. `docs/tutorials/`.
- **How-to guide** — task-oriented. Reader knows the basics, wants one thing
  done. "How to add a custom callback." `docs/how-to/`.
- **Reference** — information-oriented. Exhaustive, dry, accurate. API docs,
  config schema. `docs/reference/`, often auto-generated.
- **Explanation** — understanding-oriented. The *why* of a design decision and
  its trade-offs. `docs/explanation/` or `docs/architecture/`.

A tutorial that suddenly enumerates every flag is broken. A reference page
that opens with "Welcome! Let's learn about callbacks" is broken. **Gate: name
the mode before writing.** If a page genuinely needs two modes, it's two pages.

## Phase 2 — Write in the house tone

- **Direct.** "Use `pixi run train` to start training." Not "You may wish to
  consider invoking the training process."
- **Specific.** "Set `precision=bf16-mixed` for A100 and newer; `16-mixed` on
  V100/T4." Not "Mixed precision can help."
- **No marketing words.** Not "powerful", "robust", "seamless", "leverages".
  Say what it does.
- **Confident on opinions, honest on trade-offs.** "We use Hydra because the
  config-group pattern scales better than argparse for multi-model setups. It
  has a learning curve."
- **Lead with the use case.** Every page opens with one sentence answering
  "what is this for?" before any setup.
- **Working code, not pseudocode.** Doc code must run, or be clearly marked
  illustrative. Broken doc-code is worse than none.
- **Pin versions in examples.** "Tested with Lightning 2.5, Hydra 1.3" at the
  top of any non-trivial example.
- **Diagrams for structure, prose for procedure.** A flowchart of a 6-component
  pipeline earns its place; a flowchart of a 3-step procedure doesn't.

## Phase 3 — Docstrings (Google style)

Consistent Google style across the codebase — it renders in mkdocstrings.

```python
def train_one_epoch(model, loader, optimizer, *, device="cuda"):
    """Run one epoch of supervised training.

    Args:
        model: The model to train. Must be in `.train()` mode on entry.
        loader: A DataLoader yielding (input, target) batches.
        optimizer: An initialized optimizer over `model.parameters()`.
        device: Device to run on. Inputs and targets are moved here.

    Returns:
        The average loss over the epoch.

    Raises:
        RuntimeError: If `model` is not in training mode.
    """
```

One-line summary in imperative mood ("Run one epoch", not "Runs"). Skip
docstrings on trivial helpers. Don't repeat the type signature in prose.
Always mention non-obvious side effects (mutates optimizer state, touches the
filesystem, calls W&B).

## Page templates

**How-to guide:**
```markdown
# How to <task>
When to use this: <one sentence>
## TL;DR
<the answer in 5–10 lines>
## Walkthrough
<ordered steps, each justifying itself>
## Common pitfalls
<the 2–3 things people get wrong>
## See also
<links to reference docs and the nearest example in templates/>
```

**Explanation page:**
```markdown
# Why <thing>
## The problem
<what we'd be stuck with otherwise>
## How <thing> solves it
<concrete mechanism, not adjectives>
## Trade-offs
<honest costs>
## Alternatives we considered
<and why we didn't pick them>
```

## Anti-patterns

**Mode-mixing.** Covered above — it's the big one. A page that can't name its
mode is the page that needs splitting.

**"In this section we will cover..."** Just cover it. The header already said
what the section is.

**Restating code in prose.** "The `train()` function calls `fit()` on the
trainer" directly above the code block showing exactly that. Show the code or
describe the behavior — never both.

**Comparison tables as marketing.** A table with more than two columns of
✅/❌ is a sales sheet, not documentation.

**"Simply" / "just" / "this is easy."** Patronizing when it isn't, false when
it is. Cut them.

**Walls of bullets.** Bullets are for genuinely parallel items. Steps that
happen in order are a numbered list or prose.

## MkDocs Material specifics

- Use `mkdocs.yml`'s `nav` to enforce reading order; don't rely on filename
  sort.
- `pymdownx.tabbed` is good for showing one example in pixi vs. uv vs. conda
  form — three tabs max.
- `pymdownx.snippets` includes code from real source files; prefer it over
  copy-paste that will drift.
- Configure `mkdocstrings-python` to fail the build on missing docstrings for
  public symbols.

## Checklist

```
[ ] Page's Diátaxis mode is named and the page stays in it
[ ] Opens with one sentence answering "what is this for?"
[ ] No marketing words, no "simply"/"just", no prose restating code
[ ] Code examples run, and pin versions if non-trivial
[ ] Docstrings are Google style, imperative summary, side effects noted
```

## When asked for "a quick doc"

Default to a how-to guide on the template above. Resist making it more
elaborate than asked — a focused how-to that answers one question beats a
sprawling page that almost answers ten.
