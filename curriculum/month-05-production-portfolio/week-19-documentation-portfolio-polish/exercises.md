<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 19 — Documentation and Portfolio Polish:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Week 19 Exercises: Documentation and Portfolio Polish

## How to use this workbook

Work through the sections in order — they climb a difficulty ladder from warm-ups to brutal exercises. Documentation exercises have a unique trap: they *feel* done before they *are* done, because prose always looks finished. The acceptance criteria in each exercise are therefore strict and mechanical. Do not check off an exercise until its criteria are literally true.

Rules for this week:

- Every documented command must be executed before it is written down, and its output copy-pasted, never typed from memory.
- Every README claim must be verifiable by a stranger with only the repository.
- Do the writing in the real files (`README.md`, `ARCHITECTURE.md`, `docs/`), not in scratch documents. This week's exercises *are* the deliverables.
- When an exercise reveals a code bug (a command that no longer works), fix the bug in its own commit, then continue the documentation work.

Budget roughly: warm-ups and code-reading on day 1, docstrings and diagrams on day 2, README and demo script on days 3–4, stretch and brutal work on day 5.

---

## Warm-up exercises

### W1. Find excellent READMEs

Find three open-source Python projects on GitHub with excellent READMEs (suggested starting points: `fastapi/fastapi`, `pydantic/pydantic`, `tiangolo/sqlmodel`). For each, answer in writing:

- Does it have a one-paragraph description at the top? Is there jargon in the first two sentences?
- Does it have a working-looking Quick Start? How many commands from clone to first result?
- Does it document architecture? Limitations?
- What do all three have in common?

**Done when:** you have a written list of at least five structural patterns shared by all three.

### W2. Explain ResearchOps in one paragraph, twice

Write one paragraph explaining ResearchOps to someone with no ML background. Constraints: no jargon in the first two sentences; must include what it does, who it is for, and one concrete usage example; under 100 words. Then write a second version for a technical interviewer — jargon allowed, architecture choices mentioned.

**Done when:** both paragraphs exist and the first passes this test: a non-engineer friend (or your honest imagination of one) could repeat back what the project does.

### W3. Docstring spotting

Open `src/researchops/core/interfaces.py` and `src/researchops/services/`. For every public class and method, record: has a docstring / has only a stub docstring / has none. Build the table — it is your worklist for I1.

**Done when:** the table covers every public name in both locations.

### W4. PEP 257 lightning round

Without looking at the notes, write from memory: where a docstring must be placed, which quotes to use, what mood the summary line uses, and the three Google-style section names. Then check against notes.md section 6.2 and correct yourself.

**Done when:** you can state all four rules correctly without notes.

---

## Code-reading exercises

### R1. Derive the import graph

Run:

```bash
grep -rn "^from researchops\|^import researchops" src/researchops/ | sort
```

On paper, group the hits by package (cli, api, services, core, storage, search, ai, workers) and draw the arrows they imply. Compare your drawing against the dependency diagram in `ARCHITECTURE.md`.

**Done when:** you have a written list of (a) arrows in the code missing from the docs, (b) arrows in the docs missing from the code, and (c) any arrow that violates the architecture rules. List (c) should be empty — if it is not, you have found a code bug to fix first.

### R2. Read the docstrings Python sees

In a REPL:

```python
import researchops.core.interfaces as i
for name in dir(i):
    obj = getattr(i, name)
    if isinstance(obj, type) and not name.startswith("_"):
        print(name, "→", (obj.__doc__ or "MISSING").splitlines()[0])
```

**Done when:** you understand exactly which classes currently expose a docstring to tooling, and you have verified the output matches your W3 table.

### R3. Audit the existing ARCHITECTURE.md

Read `ARCHITECTURE.md` end to end with the code open beside it. Mark every statement as: still true / outdated / never was true / true but undocumented rationale.

**Done when:** every paragraph has one of the four marks and you have a fix list for I4.

### R4. Trace one documented command to its test

Pick one CLI command mentioned in the repository README. Find: the Typer function that implements it, the service it delegates to, and the `CliRunner` test that covers it. Write the three file:line locations down.

**Done when:** you have the full chain — or you have discovered the command lacks a test, which becomes a finding for T2.

---

## Implementation exercises

### I1. Docstring pass over core and services

Using your W3 worklist: write Google-style docstrings for every public protocol method in `core/interfaces.py` (contract language: what any implementation must guarantee, what it raises) and at minimum a PEP 257 summary line for every public service method (use-case language). Follow the protocol example in notes.md section "Code examples" exactly: class-level docstring for cross-cutting rules, method docstrings for per-method contracts.

**Done when:** the R2 REPL loop prints no `MISSING`, and `ruff check src tests` still passes.

### I2. The three Mermaid diagrams

Create `docs/diagrams/modules.md`, `docs/diagrams/ingestion.md`, and `docs/diagrams/rag.md`, each containing one focused Mermaid diagram plus a one-paragraph explanation:

- `modules.md` — the module dependency graph, derived from your R1 grep results, with `-->|implements|` arrows for infrastructure.
- `ingestion.md` — directory → scan → parse → chunk → embed → store, each node labeled with the real module or function name.
- `rag.md` — the seven-step RAG pipeline from Week 17, each node labeled with the class or method that implements it.

**Done when:** all three render correctly on GitHub (push a branch and view them), and every node label names something that exists in the code.

### I3. The final README

Rewrite the repository `README.md` to the ten-section structure from notes.md: what / who / quick start / features / architecture (small diagram + link) / usage examples / how to run tests / status / limitations / future work. Spend at least 90 minutes. The Quick Start must be tested from a fresh clone *before* you commit (see break_it.md Experiment 1). Usage examples must show real, copy-pasted output.

**Done when:** every section exists, every command was executed, and the opening paragraph passes the W2 no-jargon constraint.

### I4. Update ARCHITECTURE.md

Apply your R3 fix list. Add or refresh: a module overview (one sentence per package in `src/researchops/`), the three diagrams (inline or linked from `docs/diagrams/`), and a design-decisions section with at least three tradeoffs written in the four-part structure (suggested: SQLite, Protocol interfaces, ProcessPoolExecutor).

**Done when:** every R3 "outdated" and "never was true" mark is resolved, and the three tradeoffs read correctly in the chose/why/gave-up/when-differently format.

### I5. Write docs/demo.md

Write the 2-minute demo script following the template in notes.md: setup, ingest, search, ask, API — exact commands, copy-pasted expected output, timing labels. Then run the entire script top to bottom in a fresh directory.

**Done when:** one full rehearsal completes with zero deviations between script and reality.

### I6. Write docs/retrospective.md

Cover the 19 weeks honestly. Answer at minimum: the most important design decision and why; what you would do differently; the hardest concept; what you are most proud of; what you would build in the next five weeks.

**Done when:** all five questions have specific answers — concrete weeks, files, and bugs, not generalities.

---

## Testing exercises

### T1. Docstring presence test

Add a test (suggested: `tests/unit/test_documentation.py`) that imports `researchops.core.interfaces` and asserts every public class and every public method of those classes has a non-empty `__doc__`. Use `inspect.getmembers` and skip dunder names.

**Done when:** the test passes, and temporarily deleting one docstring makes it fail with a message naming the offender.

### T2. README-to-test cross-check

For every CLI command shown in the README's usage section, confirm a `CliRunner` E2E test exists that runs that command. Produce a two-column list: README command → covering test. For any uncovered command, add a minimal E2E test asserting exit code 0 and a recognizable fragment of the documented output.

**Done when:** the list has no empty right-hand cells and `pytest --cov=researchops --cov-report=term-missing -q` passes.

### T3. Run the documented test commands as documented

Copy the test instructions from your new README into a fresh shell, character for character, and run them.

**Done when:** they pass exactly as written — including any extras group the README told the reader to install.

---

## Debugging exercises

### D1. Plant and find a stale command

Have a study partner (or yourself, after a day's gap) change one command in `docs/demo.md` to something subtly wrong — a renamed flag, a wrong path. Then run the rehearsal procedure and find it.

**Done when:** the rehearsal caught the planted error, and you have written one sentence on which habit caught it.

### D2. Break a Mermaid diagram three ways

In a scratch branch, break `docs/diagrams/modules.md` three different ways: remove the `mermaid` fence tag; add an unquoted label containing parentheses; split the fence with a blank line in the wrong place. Push, view on GitHub, record the symptom of each, then revert.

**Done when:** you can describe, from observation, how each failure mode *looks* when rendered (raw text dump, error box, half-rendered diagram).

### D3. The `__doc__` is None hunt

Write a function with its docstring placed *above* the `def` line in a scratch file. Confirm `__doc__` is `None`. Move the string to each wrong position (after a statement, as a comment) and confirm it stays `None`. Then place it correctly.

**Done when:** you can state precisely which placements work and why.

---

## Refactoring exercises

### F1. Single-source the duplicated facts

Find every place the project version, the Python version requirement, and the install command appear (README, CHANGELOG, `pyproject.toml`, docs, demo script). For each fact, either single-source it (everything links to one authoritative location) or record every location in `RELEASE_CHECKLIST.md` so future releases update them together.

**Done when:** `grep -rn` for the current version string finds only the authoritative locations plus the checklist entry.

### F2. Diátaxis re-sort

Re-read your README and `ARCHITECTURE.md` and find at least two paragraphs living in the wrong document type — explanation inside the Quick Start, tutorial steps inside the architecture doc. Move each to its correct home and leave a one-line link behind.

**Done when:** both moves are committed and the README is shorter than before the exercise.

---

## Written explanation exercises

### E1. The four-part tradeoff, three times

Write three tradeoffs in the chose / why / gave-up / when-differently structure: SQLite vs. PostgreSQL, Protocols vs. concrete imports, local embeddings vs. embedding API. Maximum 120 words each.

### E2. The portfolio story, written

Write your problem / solution / learning narrative in two to three paragraphs, suitable for a portfolio site or LinkedIn. The learning paragraph must name something that was genuinely hard, with the specific week it happened.

### E3. Explain documentation rot

In one paragraph each, explain: what documentation rot is, why it is inevitable without process, and the two habits this repository uses to arrest it (validation.md updates on output changes; fresh-clone/demo rehearsals).

**Done when (all three):** a peer could read each answer and learn the concept without having read the notes.

---

## Stretch exercises

### S1. Record a screen capture

Record a 2-minute demo using any screen recorder, following `docs/demo.md` exactly. Link the recording from the README. A rough recording that shows the system working beats a polished one that never ships.

### S2. GitHub Pages

Enable GitHub Pages for the repository pointed at `docs/`. Verify the pages render and the Mermaid diagrams display (Pages' renderer differs from the repository file view — note any differences you find).

### S3. Draft blog post

Write a draft post titled "What I learned building a RAG assistant in 20 weeks": the project in one paragraph; three things I got wrong at first; one architectural decision I am proud of; what I would do differently; what I would build next. It does not need publishing — writing it sharpens the interview narrative.

### S4. MkDocs dry run on paper

Without installing anything, write the complete `mkdocs.yml` that would serve your current `docs/` folder (site name, nav tree mapping every page). Confirm every referenced file exists.

---

## Brutal exercises

### B1. The hostile fresh clone

On a machine (or container, or VM) that has never seen this project — not your daily environment — clone the repository and follow the README with zero improvisation: if the README does not say it, you may not type it. Log every single deviation, no matter how small ("had to install poppler", "needed to create data/ first", "command printed a warning the docs do not mention"). Fix every deviation either in docs or in code. Then repeat the entire test from scratch.

**Done when:** a full pass completes with an empty deviation log.

### B2. The cold interview

Have someone (or record yourself) ask the six interview questions from notes.md in random order: architecture walkthrough, why-X tradeoff, what differently, hardest bug, limitations, how RAG works. Answer aloud, no notes, using only the diagrams as props. Listen back and grade each answer: did it have structure, did it name specifics, did it stay under two minutes?

**Done when:** every answer scores yes on all three, possibly after multiple takes.

### B3. The docstring adversary

Pick the three most complex public methods in `services/`. For each, cover the implementation and write down everything its docstring promises. Then read the code and hunt for any behaviour the docstring does not predict — an unmentioned exception path, an edge case (empty input, missing paper), a side effect. Every discrepancy is either a docstring fix or a genuine bug; classify and fix each.

**Done when:** for all three methods, the docstring predicts every observable behaviour, and any real bugs found have failing-then-passing tests.

---

## Mini project task

**Deliverable: the employer-ready repository.**

Assemble everything from I1–I6 and T1–T3 into a coherent final state and verify it as a whole:

1. Docstrings complete in `core/interfaces.py` and `services/` (I1, guarded by T1).
2. Three rendering diagrams in `docs/diagrams/` (I2).
3. Final README with verified Quick Start (I3).
4. Accurate `ARCHITECTURE.md` with tradeoffs (I4).
5. Rehearsed `docs/demo.md` (I5) and honest `docs/retrospective.md` (I6).
6. One full hostile fresh-clone pass (B1) with an empty deviation log.
7. `ruff check src tests` and `pytest --cov=researchops --cov-report=term-missing -q` green.

Commit in small, single-concern commits as always (docstrings, diagrams, README, demo each separately).

---

## Completion checklist

- [ ] W1–W4 warm-ups complete with written artifacts
- [ ] R1 import graph matches the documented diagram, with zero rule violations
- [ ] Every public protocol method and service entry point has a docstring (R2 shows no MISSING)
- [ ] `docs/diagrams/modules.md`, `ingestion.md`, `rag.md` exist and render on GitHub
- [ ] README has all ten sections; Quick Start verified from a fresh clone
- [ ] ARCHITECTURE.md is accurate and contains at least three four-part tradeoffs
- [ ] `docs/demo.md` rehearsed end-to-end with zero deviations
- [ ] `docs/retrospective.md` answers all five questions with specifics
- [ ] Docstring presence test (T1) and README-command coverage (T2) in the test suite, passing
- [ ] Documented test commands run verbatim and pass (T3)
- [ ] At least one brutal exercise completed
- [ ] `ruff check src tests` and `pytest --cov=researchops --cov-report=term-missing -q` pass

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 19 — Documentation and Portfolio Polish:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
