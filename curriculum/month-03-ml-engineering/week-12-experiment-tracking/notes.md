<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 12 Experiment Tracking

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
