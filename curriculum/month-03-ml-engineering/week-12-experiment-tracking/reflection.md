# Reflection - Week 12 Experiment Tracking

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 12 — Experiment Tracking](./README.md) › **reflection.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

This is your personal record for Week 12 and the completion of Month 3. Fill it in carefully — this is the capstone of your ML engineering learning.

---

## What I built

**ExperimentRun fields I store:**
(List every field and what it records.)

**Tracker operations I implemented:**
(save_run, load_run, list_runs, compare_runs — which ones work?)

**CLI commands I implemented:**
(experiment list, experiment show, experiment compare — which ones work?)

**Artifact versioning approach:**
(How are artifacts named? Do they include the run ID? Do two runs ever overwrite each other?)

---

## Two runs I compared

| Field | Run 1 | Run 2 |
|---|---|---|
| Run ID | | |
| max_features | | |
| C | | |
| accuracy | | |
| f1_macro | | |
| Artifact path | | |

What changed between the two runs? Did the metrics improve?

---

## What broke

**Serialization issue:**
(Did a non-serializable value appear in params or metrics? What type? How did you fix it?)

**Missing run metadata:**
(Which field was missing from your first implementation? What did you discover when you tried to use the record?)

**How I noticed it:**
(Was it a test failure, a crash in the CLI, or a wrong comparison result?)

---

## What I misunderstood

**Reproducibility concept I clarified:**
(What does reproducibility actually mean for a model? What does it NOT mean?)

**Versioning mistake I nearly made:**
(Did you almost use a fixed artifact filename? What stopped you?)

**Comparison challenge I discovered:**
(Did metric key naming cause confusion? How did you fix it?)

---

## What I fixed

**Tracker bug:**
(What was wrong in your first implementation? How did you identify and fix it?)

**Naming or storage fix:**
(Did you change how artifacts are named or where runs are stored?)

**Evidence run records are useful:**
(Run the comparison command and paste the output here.)

---

## Month 3 completion assessment

Rate yourself (1–10) on each Week 9–12 concept:

| Concept | Score |
|---|---|
| Python Protocol and structural typing | |
| Dependency inversion | |
| Fake implementations | |
| Test pyramid | |
| pytest fixtures | |
| monkeypatch | |
| Coverage and quality gates | |
| TF-IDF | |
| Train/test split and leakage prevention | |
| Evaluation metrics (precision, recall, F1) | |
| Model artifacts (save/load) | |
| Experiment run records | |
| Run comparison | |
| Reproducibility and lineage | |

**Overall Month 3 confidence (1–10):**

**The most important thing I learned this month:**

**The concept I would most like to revisit:**

---

## Preparation for Month 4

Month 4 adds LLM integration, async APIs, and background workers. The architecture you built in Month 3 makes this possible.

- [ ] I trust the test suite to catch regressions when I add new features.
- [ ] I understand how protocols allow new adapters (e.g., OpenAI embedding) without changing services.
- [ ] I can explain the dependency graph from CLI to service to repository.
- [ ] I know how to run a training experiment and compare results.
- [ ] I am ready to build on this foundation.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 12 — Experiment Tracking** · *reflection.md — the journal* (step 6 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [validation.md](./validation.md)
- ▶ **Next:** [Write your Week 12 report](../../../docs/weekly-reports/README.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. **➡ [reflection.md](./reflection.md) ← you are here**
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 13](../../../curriculum/month-04-ai-engineering-api-workers/week-13-embeddings-semantic-search/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 13 — Embeddings & Semantic Search](../../../curriculum/month-04-ai-engineering-api-workers/week-13-embeddings-semantic-search/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 12 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
