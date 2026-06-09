<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It — Week 12 Experiment Tracking

These experiments expose what happens when experiment tracking is done incorrectly or not at all.

---

## Experiment 1: Train without recording the artifact path

Modify the training function to save the model but NOT set `run.artifact_path`:

```python
joblib.dump(pipeline, artifact_path)
# run.artifact_path = str(artifact_path)   ← comment this out
save_run(run, experiments_dir)
```

Now run `experiment show RUN_ID`. The record exists but the artifact path is empty.

**Questions to answer:** How do you deploy this model? What do you know about this run? What information did you lose? How would you automate a check that catches this mistake?

---

## Experiment 2: Overwrite the same artifact name for two runs

Change the artifact path to always be `artifacts/models/topic_classifier.joblib` (fixed name, no run ID).

Train twice with different `max_features` values.

**What to observe:** The second training run overwrites the first artifact. The first run record still exists and its `artifact_path` points to a file — but that file now contains the second run's model.

**Questions to answer:** How would you discover this problem one month from now? What is the real cost? How does run-specific naming in `topic-classifier-{run.run_id}.joblib` prevent it?

---

## Experiment 3: Store a non-serializable value in params

Try putting a `Path` object in params:

```python
run = ExperimentRun.create(
    experiment_name="test",
    params={"data_dir": Path("/tmp/data")},  # Path is not JSON-serializable
)
save_run(run, tmp_path)  # crashes with TypeError
```

**What to observe:** `json.dumps` raises `TypeError: Object of type PosixPath is not JSON serializable`.

Fix it by converting to string: `"data_dir": str(Path("/tmp/data"))`. Then verify that `load_run` correctly loads the string value.

**Questions to answer:** What other Python types are not JSON-serializable? (Hint: `datetime`, `numpy.float32`, `set`, `tuple`). Write a one-liner that converts any params dict to be serializable.

---

## Experiment 4: Delete a run file and see how list reacts

Create three run records. Delete one JSON file from `artifacts/experiments/`.

Run `experiment list`. What happens?

**What to observe:** `list_runs` reads all `.json` files in the directory. If one is deleted, it simply does not appear. There is no warning.

**Questions to answer:** Is this acceptable? Should `experiment list` warn about gaps in run IDs? What about an orphaned artifact (model file with no run record)?

---

## Experiment 5: Use the wrong metric name for one run

Train two runs. In the second run, log the accuracy metric with a different key:

Run 1: `"accuracy": 0.87`
Run 2: `"test_accuracy": 0.89` (different key name)

Now run `experiment compare RUN_ID_1 RUN_ID_2`.

**What to observe:** `accuracy` appears only for run 1. `test_accuracy` appears only for run 2. They are shown as separate rows. You cannot compare them directly.

**Questions to answer:** How do you prevent this? Should metric key names be enforced? Where in the code would you add that constraint? Write a constant dictionary of standard metric names.

---

## Experiment 6: Training failure between artifact write and record write

Simulate a crash after the artifact is saved but before the run record is saved:

```python
joblib.dump(pipeline, artifact_path)
run.artifact_path = str(artifact_path)
raise RuntimeError("Simulated crash!")   # ← add this
save_run(run, experiments_dir)           # never reached
```

**What to observe:** The artifact exists. No run record exists. This is an orphaned artifact.

**Questions to answer:** How would you detect orphaned artifacts? (Hint: compare model filenames to artifact paths in all run records.) How would you prevent this? (Hint: save the record first, then save the artifact — or use a try/finally block.)

---

## Debugging tasks

**Task D1: Print the full run record immediately after training**

Add to your training function:

```python
import json
print(json.dumps(run.to_dict(), indent=2))
```

Is every field populated? Is `artifact_path` pointing to a real file? Is `timestamp` in the right format?

**Task D2: Verify artifact existence from the record**

Write a verification script:

```python
for run in list_runs(experiments_dir):
    artifact = Path(run.artifact_path)
    if not artifact.exists():
        print(f"WARNING: {run.run_id} artifact missing: {run.artifact_path}")
    else:
        print(f"OK: {run.run_id}")
```

Run it after training. Does every run have an accessible artifact?

**Task D3: Run pytest after adding tracking code**

```bash
pytest -q
```

Does the full suite still pass? Did adding tracker imports or calls break any existing test?

---

## Edge cases to explore

**EC1: Multiple runs in the same second**

Generate two run IDs using only the timestamp (no UUID fragment). Are they the same? What happens when you try to save both? Fix it by adding a UUID fragment.

**EC2: Empty metrics dictionary**

Create a run record with `metrics={}`. Save it, load it, pass it to `compare_runs`. Does it produce a sensible output (a row with empty values) or does it crash?

**EC3: Very long parameter dictionary**

Create a run with 50 parameters. Save and load it. Does the comparison table format break when a run has many params?

---

## What did you learn?

1. What minimum metadata makes a run genuinely valuable (not just a file that exists)?
2. How did versioning mistakes (overwriting artifact names) actually erase evidence?
3. What comparison would you automate next if you ran 100 experiments?
4. At what point would you switch from file-based tracking to a dedicated tool like MLflow?
5. How does experiment tracking change the way you think about training a model?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
