# Week 11 — Classical ML Topic Classification

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › **Week 11 — Classical ML: Topic Classification**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Theme

The data pipeline is ready. Quality gates are in place. Now you build the first ML model. This week teaches you how to go from raw text in SQLite to a trained classifier that can predict the topic of any new paper.

## Learning objectives

By the end of this week you will be able to:

- Explain why ML happens after the data pipeline, not before.
- Define dataset, example, label, and feature without looking at notes.
- Describe how TF-IDF converts text to numbers.
- Write a scikit-learn Pipeline combining TF-IDF and logistic regression.
- Perform a stratified train/test split and explain why it matters.
- Explain overfitting and describe one way to detect it.
- Explain leakage and describe how a Pipeline prevents it.
- Interpret a `classification_report` output for a multi-class problem.
- Read a confusion matrix and explain what off-diagonal entries mean.
- Save a fitted Pipeline to disk with `joblib.dump`.
- Load it back and use it for inference.
- Build a CLI-based training workflow.

## Project milestone

Train a TF-IDF + logistic regression topic classifier using labeled ResearchOps papers. Save the artifact. Evaluate on a held-out test set. Verify the pipeline with at least one test.

## Key source files to study

| File | What it teaches |
|---|---|
| `src/researchops/ml/topic_classifier.py` | Stub for Week 11 — you implement this |
| `src/researchops/ml/preprocessing.py` | Text preprocessing utilities |
| `src/researchops/ml/evaluation.py` | Evaluation helpers |
| `src/researchops/core/interfaces.py` | See how ML fits into the protocol layer |
| `examples/training_data/` | Where labeled training data lives |

## Concepts covered

Dataset, example, label, feature, text vectorization, bag of words, TF-IDF (term frequency, inverse document frequency), scikit-learn Pipeline, classifier, logistic regression, train/test split, stratification, overfitting, leakage, accuracy, precision, recall, F1, confusion matrix, classification report, model artifact, joblib, inference, CLI-based ML workflow.

## Expected deliverables

- A set of labeled training examples in `examples/training_data/`.
- A working `train.py` that loads data, trains, evaluates, and saves an artifact.
- Printed metrics on the held-out test set.
- A saved model artifact at `artifacts/topic_classifier.joblib`.
- At least one test for the data loading function.
- At least one test for a small end-to-end training run.

## Definition of done

- [ ] You can explain TF-IDF with a concrete example from the notes without reading them.
- [ ] You can explain why fitting the vectorizer on all data before splitting is a leakage mistake.
- [ ] Training command runs and prints a classification report.
- [ ] Model artifact is saved to `artifacts/`.
- [ ] You can load the artifact and run a prediction on a new text.
- [ ] Tests for data loading and training pipeline exist and pass.
- [ ] `pytest -q` still passes after adding ML code.
- [ ] `ruff check src tests` still exits clean.
- [ ] You can explain the confusion matrix output to someone without ML background.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 11 — Classical ML: Topic Classification** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 10 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 12](../../../curriculum/month-03-ml-engineering/week-12-experiment-tracking/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 12 — Experiment Tracking](../../../curriculum/month-03-ml-engineering/week-12-experiment-tracking/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 11 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
