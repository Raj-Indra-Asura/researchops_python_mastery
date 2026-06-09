# Validation — Week 19 Documentation and Portfolio Polish

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 19 — Documentation & Portfolio Polish](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## 1. Pre-validation checklist

- [ ] The full suite passes and `ruff` is clean before you touch docs.
- [ ] Every command in the README has been run **exactly as written**.
- [ ] Architecture docs and diagrams match the code as it actually is.
- [ ] `docs/demo.md` has been followed step by step from a clean state.

## 2. Exact commands

```bash
# Fresh-clone test (simulates a stranger using your repo)
cd /tmp
rm -rf fresh_test
git clone <your-repo-url> fresh_test
cd fresh_test
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
researchops --help

# Quality still green
pytest
ruff check src tests
```

## 3. Expected behavior

- The README renders correctly on GitHub (code blocks, tables, Mermaid diagrams).
- A fresh clone installs and `researchops --help` works with no extra steps.
- Following `docs/demo.md` produces the documented output.

## 4. Tests that must pass

- `pytest` (whole suite) in the fresh clone.
- Every documented command runs successfully (the docs are themselves a test).

## 5. Manual checks

- Open the README on GitHub; confirm images, tables, and Mermaid diagrams render.
- Walk `docs/demo.md` line by line; fix anything that does not match reality.
- Read the architecture docs against the code; reconcile any contradiction.

## 6. Architecture checks

- Diagrams reflect the real module dependencies (no arrows the code does not
  have).
- Documented data flows (ingest, search, RAG) match the implemented flows.

## 7. Documentation checks

- README, architecture docs, and `docs/demo.md` are accurate and current.
- `docs/retrospective.md` is written honestly.
- Every README command has been executed and verified this week.

## 8. Do-not-proceed warnings

**Do not proceed to Week 20 if:**

- **README commands are not tested** — untested setup instructions are how fresh
  clones fail for everyone but you.
- **Architecture docs contradict the code** — the docs must describe what exists,
  not what you intended.

## 9. Ruthless mentor checkpoint

- "On a fresh clone, did `pip install -e` + `researchops --help` work with no
  undocumented steps?"
- "Point at one architecture diagram and the code it describes. Do they agree?"
- "Did you actually run every README command this week, or assume they still
  work?"

## 10. Definition of done

- [ ] README renders correctly on GitHub.
- [ ] Mermaid diagrams render and match the code.
- [ ] `docs/demo.md` produces correct output when followed.
- [ ] Fresh clone + install + `researchops --help` works.
- [ ] `pytest` passes and `ruff` is clean in a fresh clone.
- [ ] `docs/retrospective.md` is written and honest.
- [ ] Every documented command has been verified.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 19 — Documentation & Portfolio Polish** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 20](../../../curriculum/month-05-production-portfolio/week-20-final-hardening-v1-release/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 20 — Final Hardening & v1.0 Release](../../../curriculum/month-05-production-portfolio/week-20-final-hardening-v1-release/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 5 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 5 overview](../README.md) · [📄 Week 19 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
