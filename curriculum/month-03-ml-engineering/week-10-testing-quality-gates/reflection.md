# Reflection - Week 10 Testing Discipline and Quality Gates

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 10 — Testing & Quality Gates](./README.md) › **reflection.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

This is your personal record for Week 10. Fill it in honestly. The goal is not to claim you completed everything, but to understand what you know and what you still need to solidify.

---

## What I built

**New fixtures I wrote:**
(Name them and describe what they set up.)

**Tests I added this week:**
(List test names and which behaviors they cover.)

**Quality gates now active:**
(Which of ruff / pytest / coverage / CI are now running?)

---

## What broke

**Test failure I did not expect:**
(Describe the error. Was it a fixture error, assertion failure, or coverage failure?)

**CI or tooling issue I encountered:**
(Did CI fail for an unexpected reason? What was it?)

**How I isolated the problem:**
(What command helped you narrow it down? Did `-vv`, `--maxfail`, or `--durations` help?)

---

## What I misunderstood

**Fixture concept I had to re-read:**
(Was it scope, dependency chaining, or conftest.py placement?)

**Coverage signal I misread:**
(Did you think a line was covered when it was not? Or the opposite?)

**Difference I was fuzzy on:**
(Did you confuse unit and integration scope? Or monkeypatch vs. fake?)

---

## What I fixed

**Brittle test I made robust:**
(What made it brittle? How did you fix it — fake, tmp_path, or monkeypatch?)

**Missing gate I added:**
(Which check was not running before?)

**Evidence the suite is healthier:**
(Number of tests before and after. Coverage percentage before and after.)

---

## My quality gate results

Run these and record the actual output:

```bash
ruff check src tests
```

Result:

```bash
pytest --cov=researchops --cov-report=term-missing -q
```

Coverage percentage:

Tests: passed / failed / errors

---

## Test pyramid audit

| Layer | Test count | Approximate run time |
|---|---|---|
| Unit (`tests/unit/`) | | |
| Integration (`tests/integration/`) | | |
| E2E (`tests/e2e/`) | | |

Is the pyramid shaped correctly (more unit than integration than E2E)?

---

## Confidence score

- Week 10 confidence (1–10):
- Reason for that score:
- The testing habit I will keep doing automatically:
- The one thing I still find confusing:

---

## Preparation for Week 11

- [ ] I trust the test suite enough to safely add ML code.
- [ ] I know how to write a test before I write the feature.
- [ ] I understand what coverage tells me and what it does not.
- [ ] I am ready to learn TF-IDF and scikit-learn next week.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 10 — Testing & Quality Gates** · *reflection.md — the journal* (step 6 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [validation.md](./validation.md)
- ▶ **Next:** [Write your Week 10 report](../../../docs/weekly-reports/README.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. **➡ [reflection.md](./reflection.md) ← you are here**
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 11](../../../curriculum/month-03-ml-engineering/week-11-classical-ml-topic-classification/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 11 — Classical ML: Topic Classification](../../../curriculum/month-03-ml-engineering/week-11-classical-ml-topic-classification/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 10 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
