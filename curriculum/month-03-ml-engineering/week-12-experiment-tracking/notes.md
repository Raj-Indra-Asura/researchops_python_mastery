<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 12 Experiment Tracking

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 12: Experiment Tracking

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Remembering what you tried**.
The practical milestone is: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
The expected capability is: Can implement a tracking system that persists experiment metadata, retrieve and compare runs, and explain why reproducibility matters in ML.
This chapter is one step in the ResearchOps system, not a random lesson.
The visible feature matters because it proves the idea works.
The hidden skill matters because it lets you build the next chapter without confusion.
A complete pass through this chapter means you can read the code, run it, test it, break it, and explain it aloud.

Use this study order:
- Read the story first without typing.
- Trace the smallest code example.
- Find the project file that owns the behavior.
- Run the validation command.
- Explain one happy path and one failure path.

## What you already know from previous weeks

- Week 8 taught Multiprocessing Ingestion; keep its responsibility in mind, but do not rebuild it here.
- Week 9 taught Protocols, Interfaces, and Clean Architecture; keep its responsibility in mind, but do not rebuild it here.
- Week 10 taught Testing Discipline and Quality Gates; keep its responsibility in mind, but do not rebuild it here.
- Week 11 taught Classical ML — Topic Classification; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 12 solves the project problem behind **Experiment Tracking**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `Experiment tracking concepts: params, metrics, artifacts, runs` helps solve part of this gap.
- The concept ``ExperimentRepository` protocol and SQLite implementation` helps solve part of this gap.
- The concept `Model versioning: linking a saved model artifact to a run` helps solve part of this gap.
- The concept `Reproducibility requirements: recording random seeds, data splits` helps solve part of this gap.
- The concept ``ExperimentService` orchestration` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Experiment Tracking**?
- Ask: what is the owner for **Experiment Tracking**?
- Ask: what is the transformation for **Experiment Tracking**?
- Ask: what is the proof for **Experiment Tracking**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| Experiment tracking concepts | Experiment tracking concepts: params, metrics, artifacts, runs | This term names one job in the Week 12 milestone. |
| ExperimentRepository` protocol and SQLite implementation | `ExperimentRepository` protocol and SQLite implementation | This term names one job in the Week 12 milestone. |
| Model versioning | Model versioning: linking a saved model artifact to a run | This term names one job in the Week 12 milestone. |
| Reproducibility requirements | Reproducibility requirements: recording random seeds, data splits | This term names one job in the Week 12 milestone. |
| ExperimentService` orchestration | `ExperimentService` orchestration | This term names one job in the Week 12 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: Experiment tracking concepts: params, metrics, artifacts, runs
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 12, it supports the milestone: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: `ExperimentRepository` protocol and SQLite implementation
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 12, it supports the milestone: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: Model versioning: linking a saved model artifact to a run
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 12, it supports the milestone: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Reproducibility requirements: recording random seeds, data splits
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 12, it supports the milestone: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: `ExperimentService` orchestration
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 12, it supports the milestone: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/storage/experiment_repository.py`
- `src/researchops/services/experiment_service.py`
- `src/researchops/cli/commands/experiments.py`
- `src/researchops/storage/schema.sql` — experiment tables
Study those files in this order:
1. Find the user-facing entry point.
2. Find the service or core concept that owns the meaning.
3. Find the infrastructure only when outside resources are needed.
4. Find the tests that prove the behavior.
5. Find the validation command that a learner runs manually.
The goal is to know why each file exists.
If two files seem to own the same decision, stop and clarify the boundary.

## Code examples with line-by-line explanation

```python
run = ExperimentRun(
    params={"model": "tfidf-logistic-regression"},
    metrics={"f1": 0.82},
    artifact_path=Path("models/topic.joblib"),
)
repository.save(run)
```

Line-by-line explanation:
- Line 1: `run = ExperimentRun(` — This stores a clear intermediate value for the next step.
- Line 2: `params={"model": "tfidf-logistic-regression"},` — This stores a clear intermediate value for the next step.
- Line 3: `metrics={"f1": 0.82},` — This stores a clear intermediate value for the next step.
- Line 4: `artifact_path=Path("models/topic.joblib"),` — This stores a clear intermediate value for the next step.
- Line 5: `)` — This performs one small visible step in the workflow.
- Line 6: `repository.save(run)` — This performs one small visible step in the workflow.

How to use this example:
- Name the input.
- Name the output.
- Predict the result before running anything.
- Connect the shape to the real ResearchOps file.
- Write one sentence about why each line belongs.

## Common beginner mistakes

- **Mistake:** Pasting code before knowing the owner of the behavior.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Changing many files at once.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Skipping the failure path.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Reading only the happy path test.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Ignoring the validation command.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Using vague names.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Putting business rules in the user interface layer.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Treating logs, errors, and tests as decoration.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Optimizing before correctness is visible.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Building future-week features early.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.

## Debugging guidance

- Copy the exact failing command.
- Read the first useful error line.
- Read the final error line.
- Classify the failure as import, input, state, file, database, network, model, or expectation.
- Reproduce it with the smallest command.
- Inspect the value closest to the failure.
- Fix the cause, not only the symptom.
- Run the narrowest test.
- Run the chapter validation command.
- Write down what the error was teaching.
Debugging questions:
- What did I expect?
- What happened?
- Which value first became wrong?
- Which layer created that value?
- Which test should catch this next time?

## Design tradeoffs

- **Simple first version:** Easy to understand, but not the final production shape.
- **Clear layers:** More files, but less confusion as features grow.
- **Explicit errors:** More code, but failures become teachable.
- **Small unit tests:** Fast feedback, but less end-to-end confidence.
- **Integration tests:** Real wiring, but slower and more setup.
- **Configuration:** Flexible behavior, but defaults must be clear.
The right question is not "What is the fanciest design?"
The right question is "What design teaches the responsibility clearly and can grow next week?"

## Testing implications

Tests for this chapter:
- `tests/unit/test_experiment_service.py` — log, list, compare with fake repo
- `tests/integration/test_experiment_repository.py`
Validation commands:
```bash
researchops experiment list
researchops experiment compare
pytest tests/unit/test_experiment_service.py -v
```
- Arrange the data.
- Act on the system.
- Assert the visible promise.
- Check one failure path.
- Keep unit tests fast.
- Use integration tests only when real wiring matters.

## Architecture implications

ResearchOps stays understandable when dependencies point inward.
```text
CLI / API / Worker -> Services -> Core
Infrastructure implements core-facing contracts and is wired at the outside.
```
- Does the UI layer avoid business logic?
- Does the service layer own workflow decisions?
- Does core avoid infrastructure imports?
- Does infrastructure do outside-world work?
- Do tests use fakes when possible?
Architecture is not ceremony.
Architecture is named responsibility.

## How this connects to AI engineering / ML research

AI engineering needs more than models.
It needs reliable data flow, clear interfaces, repeatable experiments, visible failures, and honest evaluation.
Week 12 contributes by making **experiment tracking** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 12 solve?
- What is the main input?
- What is the main output?
- Which file owns the main responsibility?
- Which layer should not contain business logic?
- What is one happy path?
- What is one failure path?
- What command proves the chapter works?
- What should you not build early?
- How does this prepare the next week?

## Explain-it-aloud prompts

- Explain Experiment Tracking in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Experiment Tracking.
- The milestone: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
- The main project files.
- The validation command.
- The boundary rule for the layer you are touching.
- The habit of testing before moving forward.

## What to understand deeply

- Why this feature belongs now.
- How data moves through the chapter.
- Which file owns which decision.
- How the failure path is handled.
- Why the tests prove behavior.
- How this week makes future work safer.

## What not to worry about yet

- Perfect scale.
- Fancy abstractions.
- Future-week features.
- Every option in every library.
- Premature optimization.
- Comparing your speed to someone else.
Focus on the milestone.
A clear small milestone beats a confusing large one.

## Bridge to next week

Next week is Week 13: **Embeddings and Semantic Search**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `Experiment tracking concepts: params, metrics, artifacts, runs` from user input to project result.
- Drill 2: Write one sentence defining `Experiment tracking concepts: params, metrics, artifacts, runs` without copying the notes.
- Drill 3: Find the file where `Experiment tracking concepts: params, metrics, artifacts, runs` appears or should appear.
- Drill 4: Name one wrong implementation of `Experiment tracking concepts: params, metrics, artifacts, runs` and why it would hurt.
- Drill 5: Name one test that would protect `Experiment tracking concepts: params, metrics, artifacts, runs`.
- Drill 6: Trace ``ExperimentRepository` protocol and SQLite implementation` from user input to project result.
- Drill 7: Write one sentence defining ``ExperimentRepository` protocol and SQLite implementation` without copying the notes.
- Drill 8: Find the file where ``ExperimentRepository` protocol and SQLite implementation` appears or should appear.
- Drill 9: Name one wrong implementation of ``ExperimentRepository` protocol and SQLite implementation` and why it would hurt.
- Drill 10: Name one test that would protect ``ExperimentRepository` protocol and SQLite implementation`.
- Drill 11: Trace `Model versioning: linking a saved model artifact to a run` from user input to project result.
- Drill 12: Write one sentence defining `Model versioning: linking a saved model artifact to a run` without copying the notes.
- Drill 13: Find the file where `Model versioning: linking a saved model artifact to a run` appears or should appear.
- Drill 14: Name one wrong implementation of `Model versioning: linking a saved model artifact to a run` and why it would hurt.
- Drill 15: Name one test that would protect `Model versioning: linking a saved model artifact to a run`.
- Drill 16: Trace `Reproducibility requirements: recording random seeds, data splits` from user input to project result.
- Drill 17: Write one sentence defining `Reproducibility requirements: recording random seeds, data splits` without copying the notes.
- Drill 18: Find the file where `Reproducibility requirements: recording random seeds, data splits` appears or should appear.
- Drill 19: Name one wrong implementation of `Reproducibility requirements: recording random seeds, data splits` and why it would hurt.
- Drill 20: Name one test that would protect `Reproducibility requirements: recording random seeds, data splits`.
- Drill 21: Trace ``ExperimentService` orchestration` from user input to project result.
- Drill 22: Write one sentence defining ``ExperimentService` orchestration` without copying the notes.
- Drill 23: Find the file where ``ExperimentService` orchestration` appears or should appear.
- Drill 24: Name one wrong implementation of ``ExperimentService` orchestration` and why it would hurt.
- Drill 25: Name one test that would protect ``ExperimentService` orchestration`.
- Drill 26: Draw the Week 12 data flow in four boxes.
- Drill 27: Say why `Experiment Tracking` belongs in this month of the curriculum.
- Drill 28: Rewrite one error message in beginner-friendly language.
- Drill 29: List the exact assumptions made by the example code.
- Drill 30: List the exact assumptions checked by the tests.
- Drill 31: Point to the line where raw input becomes project meaning.
- Drill 32: Point to the line where the result becomes visible to a user.
- Drill 33: Explain what would happen if the main file were deleted.
- Drill 34: Explain what would happen if the main test were deleted.
- Drill 35: Describe the smallest manual check you can run.
- Drill 36: Describe the smallest automated check you can run.
- Drill 37: Name the most likely beginner mistake for this week.
- Drill 38: Name the safest recovery move for that mistake.
- Drill 39: Explain what knowledge should be carried into the next chapter.
- Drill 40: Trace `Experiment tracking concepts: params, metrics, artifacts, runs` from user input to project result.
- Drill 41: Write one sentence defining `Experiment tracking concepts: params, metrics, artifacts, runs` without copying the notes.
- Drill 42: Find the file where `Experiment tracking concepts: params, metrics, artifacts, runs` appears or should appear.
- Drill 43: Name one wrong implementation of `Experiment tracking concepts: params, metrics, artifacts, runs` and why it would hurt.
- Drill 44: Name one test that would protect `Experiment tracking concepts: params, metrics, artifacts, runs`.
- Drill 45: Trace ``ExperimentRepository` protocol and SQLite implementation` from user input to project result.
- Drill 46: Write one sentence defining ``ExperimentRepository` protocol and SQLite implementation` without copying the notes.
- Drill 47: Find the file where ``ExperimentRepository` protocol and SQLite implementation` appears or should appear.
- Drill 48: Name one wrong implementation of ``ExperimentRepository` protocol and SQLite implementation` and why it would hurt.
- Drill 49: Name one test that would protect ``ExperimentRepository` protocol and SQLite implementation`.
- Drill 50: Trace `Model versioning: linking a saved model artifact to a run` from user input to project result.
- Drill 51: Write one sentence defining `Model versioning: linking a saved model artifact to a run` without copying the notes.
- Drill 52: Find the file where `Model versioning: linking a saved model artifact to a run` appears or should appear.
- Drill 53: Name one wrong implementation of `Model versioning: linking a saved model artifact to a run` and why it would hurt.
- Drill 54: Name one test that would protect `Model versioning: linking a saved model artifact to a run`.
- Drill 55: Trace `Reproducibility requirements: recording random seeds, data splits` from user input to project result.
- Drill 56: Write one sentence defining `Reproducibility requirements: recording random seeds, data splits` without copying the notes.
- Drill 57: Find the file where `Reproducibility requirements: recording random seeds, data splits` appears or should appear.
- Drill 58: Name one wrong implementation of `Reproducibility requirements: recording random seeds, data splits` and why it would hurt.
- Drill 59: Name one test that would protect `Reproducibility requirements: recording random seeds, data splits`.
- Drill 60: Trace ``ExperimentService` orchestration` from user input to project result.
- Drill 61: Write one sentence defining ``ExperimentService` orchestration` without copying the notes.
- Drill 62: Find the file where ``ExperimentService` orchestration` appears or should appear.
- Drill 63: Name one wrong implementation of ``ExperimentService` orchestration` and why it would hurt.
- Drill 64: Name one test that would protect ``ExperimentService` orchestration`.
- Drill 65: Draw the Week 12 data flow in four boxes.
- Drill 66: Say why `Experiment Tracking` belongs in this month of the curriculum.
- Drill 67: Rewrite one error message in beginner-friendly language.
- Drill 68: List the exact assumptions made by the example code.
- Drill 69: List the exact assumptions checked by the tests.
- Drill 70: Point to the line where raw input becomes project meaning.
- Drill 71: Point to the line where the result becomes visible to a user.
- Drill 72: Explain what would happen if the main file were deleted.
- Drill 73: Explain what would happen if the main test were deleted.
- Drill 74: Describe the smallest manual check you can run.
- Drill 75: Describe the smallest automated check you can run.
- Drill 76: Name the most likely beginner mistake for this week.
- Drill 77: Name the safest recovery move for that mistake.
- Drill 78: Explain what knowledge should be carried into the next chapter.
- Drill 79: Trace `Experiment tracking concepts: params, metrics, artifacts, runs` from user input to project result.
- Drill 80: Write one sentence defining `Experiment tracking concepts: params, metrics, artifacts, runs` without copying the notes.
- Drill 81: Find the file where `Experiment tracking concepts: params, metrics, artifacts, runs` appears or should appear.
- Drill 82: Name one wrong implementation of `Experiment tracking concepts: params, metrics, artifacts, runs` and why it would hurt.
- Drill 83: Name one test that would protect `Experiment tracking concepts: params, metrics, artifacts, runs`.
- Drill 84: Trace ``ExperimentRepository` protocol and SQLite implementation` from user input to project result.
- Drill 85: Write one sentence defining ``ExperimentRepository` protocol and SQLite implementation` without copying the notes.
- Drill 86: Find the file where ``ExperimentRepository` protocol and SQLite implementation` appears or should appear.
- Drill 87: Name one wrong implementation of ``ExperimentRepository` protocol and SQLite implementation` and why it would hurt.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes
## Why training once is not research

After Week 11, you have a trained model. But a single training run immediately raises questions:

- What parameters did I use?
- What was the F1 score?
- If I change `max_features` from 5000 to 10000, does it improve?
- Which model produced the artifact that is currently in production?
- When was it trained? On which dataset version?

Without experiment tracking, you cannot answer these questions. You are left guessing, checking git log, or running training again hoping to get the same result.

**Experiment tracking** is the discipline of recording everything about every training run — parameters, metrics, artifact paths, dataset references, timestamps — in a structured, queryable form.

This is not optional in real ML work. It is as fundamental as version control for code. The code is versioned in git. The experiments must be versioned in an experiment store.

---

## Core vocabulary

**Experiment**: a series of related training runs with a shared goal. "Which vectorizer configuration works best for topic classification?" is an experiment. It may contain dozens of runs.

**Run**: one specific execution of the training pipeline. A run has a unique ID, specific parameters, resulting metrics, and saved artifacts.

**Parameter**: a configuration value that determines how a run behaves. For ResearchOps: `max_features=5000`, `C=1.0`, `test_size=0.2`. Parameters are set before training begins.

**Hyperparameter**: a parameter that is not learned from data but chosen by the engineer. `max_features` and `C` are hyperparameters. The model's logistic regression weights are learned parameters, not hyperparameters.

**Metric**: a numeric measurement of model quality produced after training. `accuracy=0.87`, `f1_macro=0.85`, `recall_nlp=0.91` are metrics.

**Artifact**: a file produced by a training run. The model joblib file, a confusion matrix image, a CSV of predictions — these are artifacts. Each run should link to its own artifacts.

**Dataset version**: a reference to which data was used for training. Could be a file path, a hash, a date, or a query description. Without this, "which data produced this model?" becomes unanswerable.

**Model version**: an identifier for a specific trained model artifact, distinct from all other artifacts. A run ID or timestamp-based filename serves this purpose.

**Reproducibility**: the ability to recreate the conditions of a past run and get a consistent result. Full reproducibility requires: same code, same data, same parameters, same random seed.

**Lineage**: the chain of cause and effect from data to model. "This model artifact was produced by this run, which was trained on this dataset, using this code version."

---

## What a run record contains

A minimal run record for ResearchOps:

```json
{
  "run_id": "run-20240915-1030",
  "experiment_name": "tfidf-baseline",
  "timestamp": "2024-09-15T10:30:42",
  "params": {
    "max_features": 5000,
    "C": 1.0,
    "test_size": 0.2,
    "ngram_range": "1,2",
    "classifier": "LogisticRegression",
    "random_state": 42
  },
  "metrics": {
    "accuracy": 0.87,
    "f1_macro": 0.85,
    "f1_nlp": 0.91,
    "f1_systems": 0.78,
    "f1_vision": 0.88,
    "train_size": 80,
    "test_size": 20
  },
  "artifact_path": "artifacts/models/topic-classifier-run-20240915-1030.joblib",
  "dataset_ref": "examples/training_data/ (sha256: abc123)"
}
```

Every field serves a purpose:

- `run_id` — unique identifier. Essential for referring to a specific run.
- `experiment_name` — groups related runs.
- `timestamp` — when the run happened.
- `params` — exactly what was configured. Without this, you cannot reproduce the run.
- `metrics` — the outcome. Without this, you cannot compare runs.
- `artifact_path` — where the model is saved. Without this, the run is useless for deployment.
- `dataset_ref` — what data was used.

---

## Storage design

For ResearchOps, run records are stored as JSON files in `artifacts/experiments/`:

```
artifacts/
  experiments/
    run-20240915-1030.json
    run-20240915-1145.json
    run-20240916-0830.json
  models/
    topic-classifier-run-20240915-1030.joblib
    topic-classifier-run-20240915-1145.joblib
```

Each run gets its own JSON file. Each model artifact has a run-specific name. This means:

- No overwriting.
- Every artifact is linked to its run.
- Listing `artifacts/experiments/` shows all historical runs.
- Comparing two runs is as simple as reading two JSON files.

This is a **file-based experiment store**. It requires no database, no external service, and no extra dependencies. It is suitable for a solo project or a small team. More sophisticated projects use tools like MLflow or Weights & Biases — but those tools implement the same concepts.

---

## The ExperimentRun dataclass

```python
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class ExperimentRun:
    """Records a single ML training run with its parameters and metrics."""

    run_id: str
    experiment_name: str
    timestamp: str
    params: dict[str, str | int | float]
    metrics: dict[str, float]
    artifact_path: str
    dataset_ref: str = ""

    @classmethod
    def create(cls, experiment_name: str, params: dict) -> ExperimentRun:
        """Create a new run with a generated ID and current timestamp."""
        run_id = f"run-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
        return cls(
            run_id=run_id,
            experiment_name=experiment_name,
            timestamp=datetime.utcnow().isoformat(),
            params=params,
            metrics={},
            artifact_path="",
        )

    def to_dict(self) -> dict:
        """Convert to a plain dict for JSON serialization."""
        return {
            "run_id": self.run_id,
            "experiment_name": self.experiment_name,
            "timestamp": self.timestamp,
            "params": self.params,
            "metrics": self.metrics,
            "artifact_path": self.artifact_path,
            "dataset_ref": self.dataset_ref,
        }
```

Line by line:

`@dataclass` — generates `__init__`, `__repr__`, `__eq__` automatically.

`params: dict[str, str | int | float]` — parameters must be serializable to JSON. Only strings, integers, and floats are allowed. No complex objects.

`metrics: dict[str, float]` — metrics are always floats (fractions, percentages).

`ExperimentRun.create(...)` — factory method that generates a unique run ID and timestamp. This ensures every run is distinguishable.

`run_id = f"run-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"` — a run ID looks like `run-20240915-103042-a3f8b2`. Human-readable date plus uniqueness suffix.

`to_dict()` — conversion to plain dict for JSON serialization. `json.dumps` cannot serialize a dataclass directly.

---

## The tracker: saving and loading runs

```python
def save_run(run: ExperimentRun, output_dir: Path) -> Path:
    """Write the run record as a JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{run.run_id}.json"
    path.write_text(
        json.dumps(run.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def load_run(run_id: str, experiments_dir: Path) -> ExperimentRun:
    """Load a run record by ID."""
    path = experiments_dir / f"{run_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"No run record found for {run_id}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return ExperimentRun(**data)


def list_runs(experiments_dir: Path) -> list[ExperimentRun]:
    """Return all run records, sorted by timestamp."""
    runs = []
    for json_file in sorted(experiments_dir.glob("*.json")):
        data = json.loads(json_file.read_text(encoding="utf-8"))
        runs.append(ExperimentRun(**data))
    return sorted(runs, key=lambda r: r.timestamp)


def compare_runs(run_ids: list[str], experiments_dir: Path) -> None:
    """Print a comparison table for the given run IDs."""
    runs = [load_run(rid, experiments_dir) for rid in run_ids]
    all_metrics = sorted({k for r in runs for k in r.metrics})

    header = f"{'Metric':<20}" + "".join(f"{r.run_id:<30}" for r in runs)
    print(header)
    print("-" * len(header))

    for metric in all_metrics:
        row = f"{metric:<20}"
        for r in runs:
            value = r.metrics.get(metric, "N/A")
            row += f"{str(value):<30}"
        print(row)
```

`save_run` — writes the run as indented JSON. `ensure_ascii=False` allows non-ASCII characters in text fields. `parents=True` creates intermediate directories.

`load_run` — deserializes a JSON file back into an `ExperimentRun`. Raises `FileNotFoundError` with a clear message if the run does not exist.

`list_runs` — reads all JSON files in the experiments directory and sorts by timestamp. This gives a history of all runs.

`compare_runs` — side-by-side comparison table. Each metric is a row; each run is a column. This is the core analysis tool.

---

## Integrating tracking into training

The training function from Week 11 needs two additions:

1. Create a run record at the start.
2. Fill in metrics and artifact path at the end, then save.

```python
from researchops.experiments.tracker import save_run
from researchops.experiments.models import ExperimentRun

def train(
    data_dir: Path,
    output_path: Path,
    experiment_name: str = "tfidf-baseline",
    max_features: int = 5000,
    C: float = 1.0,
) -> ExperimentRun:
    """Train topic classifier and log the run."""

    # Create run record early
    run = ExperimentRun.create(
        experiment_name=experiment_name,
        params={
            "max_features": max_features,
            "C": C,
            "test_size": 0.2,
            "random_state": 42,
            "classifier": "LogisticRegression",
        },
    )

    # ... (load data, split, fit pipeline) ...

    # Record metrics
    run.metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "f1_macro": float(f1_score(y_test, predictions, average="macro")),
        "train_size": len(X_train),
        "test_size": len(X_test),
    }

    # Save artifact with run-specific name
    artifact_path = output_path.parent / f"topic-classifier-{run.run_id}.joblib"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, artifact_path)
    run.artifact_path = str(artifact_path)

    # Save run record
    experiments_dir = output_path.parent.parent / "experiments"
    save_run(run, experiments_dir)
    print(f"Run {run.run_id} saved to {experiments_dir}")

    return run
```

Key changes from Week 11:

1. Training accepts `experiment_name`, `max_features`, and `C` as parameters instead of hard-coding them. This allows different runs to use different values.
2. The artifact path includes `run.run_id` in the filename, so different runs produce different artifacts.
3. `run.artifact_path` is set before saving the run record, so the record always links to its artifact.
4. The function returns the `ExperimentRun` so callers (CLI, tests) can inspect or display the result.

---

## CLI commands for experiment tracking

The problem statement specifies these commands. Here is what each should do:

```bash
# Create a named experiment (optional grouping step)
researchops experiment create "tfidf-baseline"
```

This creates a directory or marker indicating a named experiment is starting. Optional if you include `experiment_name` in every training run.

```bash
# Train and log a run
researchops train-topic-model --experiment tfidf-baseline
```

Calls the training function, logging the run under the `tfidf-baseline` experiment name.

```bash
# List all runs
researchops experiment list
```

Reads all JSON files from `artifacts/experiments/`, prints a summary table:

```
Run ID                     Experiment          Timestamp              F1 Macro
run-20240915-1030-a3f8b2   tfidf-baseline      2024-09-15 10:30:42   0.85
run-20240915-1145-c9d2e1   tfidf-baseline      2024-09-15 11:45:03   0.87
```

```bash
# Show a specific run
researchops experiment show run-20240915-1030-a3f8b2
```

Reads the JSON file for that run ID, prints all params and metrics in a readable format.

```bash
# Compare two or more runs
researchops experiment compare run-20240915-1030-a3f8b2 run-20240915-1145-c9d2e1
```

Calls `compare_runs` and prints the side-by-side metric table.

---

## Failed runs

What if training crashes after saving the artifact but before saving the run record? The artifact exists but no record points to it. It is an orphan.

What if the run record is saved but training crashed before saving the artifact? The record's `artifact_path` points to a file that does not exist.

Both are real failure modes. Handle them:

1. **Always save the run record even on failure** — log what you know: params, timestamp, and an error message in the metrics. A failed run with `"error": "OOMKilled"` is valuable information.
2. **Validate artifact paths on load** — when displaying a run, check whether `artifact_path` exists on disk and warn if it does not.

---

## Research notebook vs. experiment tracker

A Jupyter notebook is good for exploration: visualizing data, trying code snippets, producing one-off charts. It is a scratchpad.

An experiment tracker is good for history: recording what you ran, comparing results, understanding why the current model is the current model.

| Notebook | Experiment tracker |
|---|---|
| Execution order matters | Results are independent of order |
| State mutates as cells are run | Each run is self-contained |
| Hard to version | Versioned by run ID and timestamp |
| Hard to test | Can be tested |
| Hard to automate | Callable from CLI and CI |

Use notebooks for exploration. Use the experiment tracker for production ML work. They complement each other.

---

## Why this supports ML research

A portfolio-grade ML project must demonstrate that you can:

1. **Train repeatedly** — not just once.
2. **Improve systematically** — by comparing runs, not guessing.
3. **Explain past results** — by reading run records.
4. **Reproduce results** — by re-running with the same params.

Without experiment tracking, "I improved the model" means you changed some numbers and the new model happened to score better. With tracking, it means "I increased `max_features` from 5000 to 10000 and F1 improved from 0.85 to 0.87. Both runs are logged."

That is the difference between a student project and engineering work.

---

## Summary

| Concept | Meaning |
|---|---|
| Experiment | A series of related training runs sharing a goal |
| Run | One execution of the training pipeline with specific params |
| Parameter | Configuration value chosen before training |
| Hyperparameter | Parameter not learned from data, chosen by the engineer |
| Metric | Numeric measurement of model quality after training |
| Artifact | File produced by a training run (model, predictions, etc.) |
| Dataset version | Reference to which data produced this model |
| Model version | Unique identifier for a specific trained model artifact |
| Reproducibility | Ability to recreate a past run's conditions and results |
| Lineage | Chain from data → training run → model artifact |
| Run record | Structured file (JSON) containing all run metadata |
| Experiment tracker | System for saving, listing, and comparing run records |
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 12 — Experiment Tracking:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
