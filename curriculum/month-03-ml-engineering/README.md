<!-- NAV_START -->
---
[🏠 Home](../../README.md) · [🗺 Roadmap](../../ROADMAP.md) · [📋 Syllabus](../../SYLLABUS.md) · [🗂 Curriculum Map](../NAVIGATION.md)

**Month 3 — Advanced Python and ML Engineering**

[Week 09: Protocols and Clean Architecture](./week-09-protocols-clean-architecture/README.md) · [Week 10: Testing and Quality Gates](./week-10-testing-quality-gates/README.md) · [Week 11: Classical ML: Topic Classification](./week-11-classical-ml-topic-classification/README.md) · [Week 12: Experiment Tracking](./week-12-experiment-tracking/README.md)

⬅️ [← Month 2: Storage, Search, Multiprocessing](../month-02-data-storage-concurrency/README.md) · ➡️ [Month 4: AI Engineering, API, Workers →](../month-04-ai-engineering-api-workers/README.md)

---
<!-- NAV_END -->

# Month 3 — ML Engineering

> **Book section 3 of 5.** This month the working library becomes an *engineered*
> system. You learn the architecture, testing, and reproducibility discipline
> that separates a script from software — and you train and track your first real
> machine-learning model inside it.

---

## The big idea of the month

You have a system that *works*. Month 3 asks a harder question: **is it well
built?** You will refactor toward clean architecture using Python protocols,
build a real test pyramid behind CI quality gates, and only then add classical
machine learning (TF-IDF topic classification) with proper model artifacts and
experiment tracking.

The theme: **ML is software engineering.** A model is worthless if you cannot
test the system around it, reproduce its results, or explain why one run beat
another. This month makes ML *engineered*, not improvised.

## What you already know before this month

From Months 1–2 you can:

- Build and install a `src/`-layout CLI application.
- Persist data in SQLite behind a repository, parse PDFs, search, and ingest in
  parallel.
- Explain the pipeline `scan → parse → store → search → parallelize`.

You do **not** need prior ML experience. We start from zero on the ML side.

## What you will learn this month

- **Protocols and interfaces** (`typing.Protocol`) — defining behavior without
  inheritance.
- **Clean architecture** — dependency inversion, ports and adapters, keeping
  services free of infrastructure.
- **The test pyramid** — many fast unit tests, fewer integration tests, minimal
  end-to-end tests; fakes and test doubles.
- **CI and quality gates** — automated lint, type-check, tests, and coverage
  thresholds that block bad merges.
- **Classical ML** — supervised learning fundamentals, train/test split, leakage
  prevention.
- **TF-IDF** — turning text into numeric features for a classifier.
- **Evaluation metrics** — accuracy, precision, recall, F1 (macro).
- **Model artifacts** — saving and loading trained models (`joblib`).
- **Experiment tracking** — recording each run's params, metrics, and artifact.
- **Reproducibility** — making a result you can recreate and explain.

## What ResearchOps capability will exist by the end

The ability to **train and track a classical ML model inside a structured Python
application**:

```bash
researchops train --experiment tfidf-baseline   # train + log a run
researchops experiment list                       # see all runs
researchops experiment compare RUN_A RUN_B        # diff metrics side by side
```

Every run is reproducible, versioned, and comparable — backed by clean
architecture and a test suite that protects it.

## Week-by-week chapter flow

| Week | Chapter | What it adds |
|---|---|---|
| **Week 9 — Protocols & Clean Architecture** | "Taming dependencies" | `typing.Protocol`, dependency inversion, fakes, layer boundaries. |
| **Week 10 — Testing & Quality Gates** | "Trust through tests" | Test pyramid, fixtures, coverage, CI gates. |
| **Week 11 — Classical ML: Topic Classification** | "The first model" | TF-IDF features, train/test split, metrics, a real classifier. |
| **Week 12 — Experiment Tracking** | "Remembering experiments" | Run records, model artifacts, comparison, reproducibility. |

## How each week connects to the previous week

- **Week 9 → 10:** clean architecture makes code *testable* (you can swap fakes
  for real adapters); Week 10 cashes that in by building the test pyramid and CI
  gates that depend on it.
- **Week 10 → 11:** with a safety net of tests in place, you can add the first ML
  model without fear of silently breaking the system.
- **Week 11 → 12:** once you can train a model, you immediately hit the question
  "which run was better and why?" — Week 12 answers it with experiment tracking,
  artifacts, and reproducibility.

## What not to skip

- **Writing your own fake repository in Week 9.** This is the single most
  important skill of the month; do not just read the existing one.
- **The import-boundary discipline.** Services and `core` must not import SQLite,
  PyMuPDF, or sklearn. Enforce it (see
  [ADR-0001](../../docs/decisions/0001-modular-monolith.md)).
- **Leakage prevention in Week 11.** Fitting the vectorizer on the whole dataset
  before the split silently inflates your metrics. Split first.
- **Per-run artifact naming in Week 12.** Overwriting one model file destroys
  your ability to compare runs.

## What concepts must be understood before moving on

Be able to explain aloud:

- The dependency inversion principle, and why `IngestionService` takes a
  `PaperRepository` protocol rather than a concrete `SQLiteRepository`.
- The difference between a fake and a mock, and when to prefer a fake.
- What each layer of the test pyramid is for.
- What TF-IDF computes and why raw word counts are not enough.
- Why train/test split and leakage prevention matter.
- What macro-F1 measures and why accuracy alone can mislead.
- What makes a run reproducible and how an experiment record captures it.

## Month-end self-assessment

Rate yourself 1–10 with evidence:

- [ ] I can define a protocol and write a fake that satisfies it from scratch.
- [ ] I can identify which architectural layer any source file belongs to.
- [ ] I can explain and run the test pyramid and read a coverage report.
- [ ] I can describe what the CI quality gates check and why.
- [ ] I can train a TF-IDF + classifier model without data leakage.
- [ ] I can interpret precision, recall, and macro-F1.
- [ ] I can save and load a model artifact.
- [ ] I can log two runs and explain what changed between them using only the CLI.

## Month-end mini capstone

Run a small, honest ML experiment:

1. Train a baseline topic classifier and log the run (params + metrics +
   artifact path).
2. Train a second run with a different hyperparameter (e.g. `max_features`).
3. Use `experiment compare` to show the metric difference side by side.
4. Confirm each run wrote a **distinct** artifact (no overwrite) and that every
   run record points to a file that exists.
5. Prove the whole thing is protected: `pytest` green, coverage above threshold,
   `ruff` clean.

Done when you can answer "which run is better, and why?" using only the CLI and
your experiment records.

## Bridge to Month 4

You can now classify papers and track experiments — but a classifier is not yet
*AI engineering*. Month 4 adds the parts that make ResearchOps an AI platform:
**embeddings** and **semantic search**, a **FastAPI** HTTP layer, **async** network
fetching, and a **background worker/job system**. Crucially, you build
**retrieval before RAG** — you cannot generate grounded answers until you can
find the right context.

## Warning signs you are not ready to move on

- Your services import SQLite, PyMuPDF, or sklearn directly.
- You cannot write a fake without copying the existing one.
- Your model's metrics look "too good" (a sign of leakage).
- Two training runs overwrite the same artifact file.
- Tests pass but you do not trust them to catch a real regression.

## Suggested weekly study rhythm

~9–11 hours/week (this is a conceptually heavy month):

- **Read** week README + notes (~1–1.5 hrs).
- **Build/refactor** in small commits (~5–6 hrs) — Week 9 especially is
  think-heavy, not type-heavy.
- **Break it** with `break_it.md` (~1 hr) — induce a leakage bug, a protocol
  mismatch.
- **Test** and check coverage (~1.5–2 hrs).
- **Reflect** in `reflection.md` and the weekly report (~30–45 min).

## Suggested Git milestone at end of month

```bash
git add .
git commit -m "Month 3 complete: clean architecture, test pyramid, trained + tracked ML model"
git tag month-3-complete
```

Your repo should now train and compare reproducible ML runs behind a clean,
tested, CI-gated architecture.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Month 2: Storage, Search, Multiprocessing](../month-02-data-storage-concurrency/README.md) · ➡️ [Month 4: AI Engineering, API, Workers →](../month-04-ai-engineering-api-workers/README.md)

[Week 09: Protocols and Clean Architecture](./week-09-protocols-clean-architecture/README.md) · [Week 10: Testing and Quality Gates](./week-10-testing-quality-gates/README.md) · [Week 11: Classical ML: Topic Classification](./week-11-classical-ml-topic-classification/README.md) · [Week 12: Experiment Tracking](./week-12-experiment-tracking/README.md)

[🏠 Home](../../README.md) · [🗺 Roadmap](../../ROADMAP.md) · [📋 Syllabus](../../SYLLABUS.md) · [🗂 Curriculum Map](../NAVIGATION.md)
---
<!-- NAV_BOTTOM_END -->
