<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 12 Experiment Tracking

## Warm-up: Tracking mechanics

**Exercise W12-1: Generate unique run IDs**

Write three different approaches to generating a unique run ID:

1. Using `uuid.uuid4()`.
2. Using `datetime.utcnow().strftime(...)`.
3. A hybrid: timestamp + short UUID fragment (as used in the notes).

For each, write the code, generate 5 IDs, and answer: are they sortable? Are they human-readable? Are they guaranteed unique?

**Exercise W12-2: JSON round-trip**

Write code that:
1. Creates an `ExperimentRun` with params and metrics.
2. Serializes it to JSON with `json.dumps`.
3. Deserializes it with `json.loads`.
4. Asserts the deserialized object has the same `run_id`, params, and metrics as the original.

Then try putting an unsupported type in params (e.g., a `Path` object). What error do you get? Fix it by converting to `str` first.

**Exercise W12-3: Compare two dictionaries**

Write a function `compare_metric_dicts(a: dict, b: dict) -> dict` that returns a dict where each key maps to a tuple `(a_value, b_value, delta)`. Example:

```python
compare_metric_dicts(
    {"accuracy": 0.87, "f1_macro": 0.85},
    {"accuracy": 0.89, "f1_macro": 0.84}
)
# → {"accuracy": (0.87, 0.89, +0.02), "f1_macro": (0.85, 0.84, -0.01)}
```

This is a primitive version of `compare_runs`.

**Exercise W12-4: Load and print a run record**

Save a run record to `tmp_path / "run-test.json"` manually. Then write a function that loads it and prints every key/value pair in sorted order. Run it.

---

## Project exercises: ResearchOps

**Exercise W12-5: Implement ExperimentRun**

Implement the `ExperimentRun` dataclass following the structure in notes.md. Requirements:

- `run_id`, `experiment_name`, `timestamp`, `params`, `metrics`, `artifact_path`, `dataset_ref`.
- A `create(experiment_name, params)` class method.
- A `to_dict()` method.
- A `from_dict(data)` class method (inverse of `to_dict`).

Write a test that creates a run, converts to dict, converts back from dict, and asserts equality.

**Exercise W12-6: Implement save_run and load_run**

Implement `save_run(run, output_dir)` and `load_run(run_id, experiments_dir)`. Requirements:

- `save_run` creates the directory if it does not exist.
- `save_run` writes a JSON file named `{run_id}.json`.
- `load_run` raises `FileNotFoundError` with a useful message if the ID is not found.
- `load_run` returns an `ExperimentRun` with all fields.

Write tests:
- `test_save_run_creates_file`: verify the file is created.
- `test_load_run_returns_correct_run_id`: verify round-trip.
- `test_load_run_raises_for_missing_id`: verify the error.

**Exercise W12-7: Implement list_runs and compare_runs**

Implement `list_runs(experiments_dir)` and `compare_runs(run_ids, experiments_dir)`:

- `list_runs` returns all runs sorted by timestamp.
- `compare_runs` prints a readable table: metric names as rows, run IDs as columns.

Write tests:
- `test_list_runs_returns_all_runs_sorted`: create 3 runs, list them, verify order.
- `test_compare_runs_shows_delta`: create 2 runs with different f1_macro, compare, verify both values appear in the output.

**Exercise W12-8: Update the training pipeline**

Modify your `train()` function from Week 11 to:

1. Accept `experiment_name`, `max_features`, and `C` as parameters.
2. Create an `ExperimentRun` at the start.
3. Name the artifact `topic-classifier-{run.run_id}.joblib`.
4. Fill `run.metrics` from the classification report.
5. Fill `run.artifact_path` after saving the artifact.
6. Call `save_run(run, experiments_dir)` before returning.

Write an integration test that:
1. Runs training.
2. Checks that `artifacts/experiments/` contains a JSON file.
3. Loads the run record.
4. Checks that `run.artifact_path` exists on disk.
5. Checks that required metrics keys are present.

**Exercise W12-9: Implement CLI commands**

Implement these commands in `src/researchops/cli/commands/experiments.py`:

```bash
researchops experiment list
# prints all runs with run_id, experiment_name, timestamp, f1_macro

researchops experiment show RUN_ID
# prints all params and metrics for the given run

researchops experiment compare RUN_ID_1 RUN_ID_2
# prints side-by-side metric comparison
```

Test the `experiment list` command manually. Then write a test using `CliRunner` (from Click's testing utilities) that calls `experiment list` and verifies the output contains at least one run ID.

---

## Stretch exercises

**Exercise W12-S1: Add a dataset hash to the run record**

Compute a SHA-256 hash of the training data directory and store it in `dataset_ref`:

```python
import hashlib
import json
from pathlib import Path

def hash_dataset(data_dir: Path) -> str:
    """Hash all JSONL files in data_dir for a stable dataset reference."""
    h = hashlib.sha256()
    for jsonl_file in sorted(data_dir.glob("*.jsonl")):
        h.update(jsonl_file.read_bytes())
    return h.hexdigest()[:16]
```

Store `dataset_ref = hash_dataset(data_dir)` in the run record. Now if the dataset changes, the hash changes, and you can see which runs used which dataset version.

**Exercise W12-S2: Handle failed runs**

Modify `train()` to catch exceptions and still save a run record with an error:

```python
try:
    # ... training ...
    run.metrics["error"] = None
except Exception as exc:
    run.metrics["error"] = str(exc)
    run.metrics["status"] = "failed"
finally:
    save_run(run, experiments_dir)
```

Write a test that injects a training error and verifies a run record is still saved with `"status": "failed"`.

**Exercise W12-S3: Add a best-run finder**

Write a function `find_best_run(experiments_dir: Path, metric: str) -> ExperimentRun | None` that returns the run with the highest value for a given metric. Test it.

---

## Written reflection questions

1. You trained 10 runs last week and today you cannot remember which one you deployed. With experiment tracking, how do you find out? Without tracking, what would you do?

2. You update the training data and retrain. The new model has lower F1. How does the experiment tracker help you diagnose whether the problem is the data or the code?

3. What is the difference between a parameter and a metric? Give two examples of each from this project.

4. A colleague says: "I don't need experiment tracking — I just look at the last model." What failure scenario would change their mind?

5. Where does file-based experiment tracking (JSON files) break down? When would you need a tool like MLflow or Weights & Biases?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
