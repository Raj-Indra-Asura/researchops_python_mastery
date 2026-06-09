<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · **Reflection**

⬅️ [← Validation](validation.md) · ➡️ [📝 Week 12 Report](../../../docs/weekly-reports/README.md) · [Week 13 →](../../month-04-ai-engineering-api-workers/week-13-embeddings-semantic-search/README.md)

---
<!-- NAV_END -->

# Reflection - Week 12 Experiment Tracking

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

<!-- WEEKLY_REPORT -->
---

## Weekly Report

When you have completed this reflection, write your [Week 12 report](../../../docs/weekly-reports/README.md).

Store it at `docs/weekly-reports/week-12-report.md` (see the [weekly reports guide](../../../docs/weekly-reports/README.md) for the template).

Once your report is committed, advance to [Week 13 →](../../month-04-ai-engineering-api-workers/week-13-embeddings-semantic-search/README.md).
<!-- WEEKLY_REPORT_END -->

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Validation](validation.md) · ➡️ [📝 Week 12 Report](../../../docs/weekly-reports/README.md) · [Week 13 →](../../month-04-ai-engineering-api-workers/week-13-embeddings-semantic-search/README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · **Reflection**

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
