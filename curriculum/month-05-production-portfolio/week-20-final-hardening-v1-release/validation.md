# Validation — Week 20 Final Hardening and v1.0.0 Release

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 20 — Final Hardening & v1.0 Release](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## 1. Pre-validation checklist

- [ ] The whole suite passes with zero failures.
- [ ] `ruff` is clean.
- [ ] The version is set to `1.0.0` in both `pyproject.toml` and `__init__.py`.
- [ ] The changelog describes **only** features that actually work.

## 2. Exact commands

```bash
source .venv/bin/activate
pytest                       # expected: all passed, 0 failed
ruff check src tests         # expected: no output

# CLI smoke test
researchops --help
researchops scan ./examples/sample_papers

# Version check
python -c "import researchops; print(researchops.__version__)"   # expected: 1.0.0

# Follow the demo end to end
#   docs/demo.md  (run every command)
```

Release (only after everything above is green):

```bash
git add .
git commit -m "v1.0.0: final release"
git tag -a v1.0.0 -m "ResearchOps v1.0.0"
```

## 3. Expected behavior

- All final-validation commands succeed.
- The CLI smoke test runs cleanly.
- The version reports `1.0.0`; the demo runs without errors.

## 4. Tests that must pass

- `pytest` (entire suite, 0 failures)
- Every command in `docs/demo.md`

## 5. Manual checks

- Run the full demo as a stranger would; confirm each step matches the docs.
- Re-read the `[1.0.0]` changelog entry against what the code actually does.
- Confirm `ROADMAP.md` reflects the true state of all 20 weeks.

## 6. Architecture checks

- No half-finished feature is exposed as if complete.
- The final dependency structure still respects the layer boundaries
  (core ← services ← transports).

## 7. Documentation checks

- `CHANGELOG.md` has a `[1.0.0]` section dated today, listing only working
  features.
- README, demo, and architecture docs are consistent with the released code.

## 8. Do-not-proceed warnings

**Do not tag the release if:**

- **The changelog claims unfinished features** — every listed feature must work.
- **Final validation commands fail** — a release is cut only from a fully green
  state.

## 9. Ruthless mentor checkpoint

- "Read me the changelog. Can you demonstrate every single line right now?"
- "Run the full final-validation block. Is any command red?"
- "Could a stranger clone this, follow the demo, and succeed without your help?"

## 10. Definition of done

- [ ] `pytest` passes with 0 failures; `ruff` clean.
- [ ] Version is `1.0.0` in `pyproject.toml` and `__init__.py`.
- [ ] `CHANGELOG.md` `[1.0.0]` section is accurate and dated.
- [ ] `ROADMAP.md` shows all 20 weeks complete.
- [ ] `docs/demo.md` runs without errors.
- [ ] The `v1.0.0` tag is created from a fully green state.
- [ ] You are genuinely proud of the project.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 20 — Final Hardening & v1.0 Release** · *validation.md — the checkpoint* (step 5 of 6 this week).

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
8. 🎉 You have reached the final week — see the [Release Checklist](../../../RELEASE_CHECKLIST.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Finish: Release Checklist](../../../RELEASE_CHECKLIST.md) and the [portfolio outcome](../../../README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 5 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 5 overview](../README.md) · [📄 Week 20 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
