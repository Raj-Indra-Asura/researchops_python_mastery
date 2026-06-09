<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 12 Experiment Tracking

## 1. How to use this workbook

### Read, build, inspect

Read the goal before writing code. Build the smallest piece that proves the concept. Inspect saved records manually so experiment tracking feels concrete. Then write or update the test that would catch a regression.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### Stay inside Week 12

Use the Week 11 classifier as the model being tracked. Use JSON and optional SQLite-style storage. Do not add hosted tracking tools, web APIs, containers, or next-week concepts.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### Use evidence

For every implementation task, identify the parameters, metrics, artifacts, and metadata. If you cannot name those four groups, pause before coding.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 2. Warm-up exercises

### W12-W1: Sort fields into tracking categories

Make a four-column table: params, metrics, artifacts, metadata. Place `max_features`, `C`, `random_seed`, `accuracy`, `f1_macro`, `model.joblib`, `dataset_ref`, `status`, and `error_message` into the correct column. Write one sentence explaining every placement.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-W2: Generate run IDs

Write `generate_run_id()` using a UTC timestamp plus an eight-character UUID fragment. Generate ten IDs. Answer: which part is readable, which part prevents collisions, and why is timestamp-only risky?

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-W3: JSON round trip

Create a complete run dictionary. Save it with `json.dumps(..., indent=2)`. Load it with `json.loads`. Assert the loaded `run_id`, `params`, and `metrics` match the original.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-W4: Serialization failure

Put a `Path` and a `datetime` in a run dictionary. Observe the JSON error. Fix the record by converting those values to strings. Write a rule describing JSON-friendly values.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 3. Code-reading exercises

### W12-C1: Read an ExperimentRun dataclass

For each field, write whether it is known before training, after evaluation, after artifact saving, or after failure. Mark which fields are required for a useful record.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-C2: Read save_run

Annotate the save function line by line. Identify where the directory is created, where the filename is chosen, where JSON conversion happens, and where encoding is specified.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-C3: Read load_run

Trace what happens when the run ID exists. Trace what happens when it does not exist. Improve the missing-run message if it does not include the requested ID.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-C4: Read comparison output

Given two run records with different metric dictionaries, sketch the expected comparison table before reading code. Decide how missing values should be displayed.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 4. Implementation exercises

### W12-I1: Implement ExperimentRun

Create a dataclass with run ID, experiment name, timestamp, params, metrics, artifacts, dataset reference, status, and error message. Add `create`, `to_dict`, and `from_dict` methods.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-I2: Implement JSON repository functions

Implement `save_run`, `load_run`, and `list_runs`. Save one file per run. Return an empty list if the directory does not exist. Sort listed runs by timestamp.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-I3: Implement compare_runs

Load selected runs, gather all metric names, and produce a text table with metric names as rows. Show a clear placeholder such as `--` when a run lacks a metric.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-I4: Link artifacts to run IDs

Update the Week 11 training flow so the saved classifier filename includes the run ID. Store the model path in `run.artifacts["model"]`.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-I5: Record failed runs

Wrap the training flow so a failure can still save a run record with `status="failed"` and a useful `error_message`. Do not hide the original exception from debugging output.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 5. Testing exercises

### W12-T1: Test dataclass round trip

Create a run, convert to dict, convert back, and assert important fields match.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-T2: Test save and load

Use `tmp_path`. Save a run. Assert `{run_id}.json` exists. Load it and assert params and metrics survived.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-T3: Test missing run

Call `load_run` with a missing ID. Assert `FileNotFoundError` and assert the message contains the ID.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-T4: Test list order

Create three records with timestamps out of order. Assert `list_runs` returns them sorted.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-T5: Test comparison

Create two runs with shared and missing metrics. Assert both run IDs appear and missing values are displayed gracefully.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-T6: Test failure recording

Simulate a training error. Assert a failed run record exists and contains a non-empty error message.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 6. Debugging exercises

### W12-D1: Break JSON serialization

Intentionally store a `Path` in params. Capture the exception. Fix by converting to string. Add a regression test.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-D2: Break artifact lineage

Create a record whose model artifact path does not exist. Make the show command or display helper warn without crashing.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-D3: Break metric names

Write one run with `f1_macro` and another with `macro_f1`. Compare them. Fix the writer so one stable key is used.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-D4: Break timestamp sorting

Use human dates such as `9/1/2024` and `10/1/2024`. Show why string sorting fails. Replace with ISO-style timestamps.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-D5: Break directory assumptions

Save records in one directory and list from another. Add configuration or clearer wiring so CLI and service use the same experiments directory.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 7. Refactoring exercises

### W12-R1: Extract display formatting

If repository code builds CLI tables, move formatting out. Repository code should return run objects or comparison data.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-R2: Add ExperimentRepository protocol

Define `save`, `get`, and `list` operations in the protocol. Make services depend on it. Keep concrete JSON details in infrastructure.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-R3: Use a fake repository

Write service tests using an in-memory fake repository. Prove service behavior without touching the filesystem.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-R4: Split training and tracking responsibilities

Separate run creation, classifier training, metric recording, artifact saving, repository saving, and CLI display into readable pieces.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 8. Written explanation exercises

### W12-X1: Why tracking matters

In 150 to 250 words, explain why a classifier that already trains still needs experiment tracking.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-X2: Failed run value

Describe a failure that happens after run creation but before artifact saving. What should the record contain and why is it useful?

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-X3: JSON vs SQLite

List three strengths of JSON tracking and three strengths of SQLite tracking. Choose the first implementation for this project and justify it.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-X4: Fair comparison

Run A has `f1_macro=0.83` on `papers-v1`. Run B has `f1_macro=0.86` on `papers-v2`. Explain why claiming improvement may be unsafe.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-X5: Architecture boundary

Explain why a service should depend on a repository protocol rather than directly opening JSON files.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 9. Stretch exercises

### W12-S1: Dataset hash

Hash sorted `.jsonl` training files with SHA-256 and store a short prefix in `dataset_ref`. Explain why sorted file order matters.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-S2: Best run finder

Implement `find_best_run(experiments_dir, metric_name)` for higher-is-better metrics. Return `None` when no run has the metric.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-S3: Experiment filtering

Add optional filtering by experiment name to `list_runs`. Test that unrelated experiments are excluded.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-S4: SQLite repository

Implement the same repository protocol with SQLite. Use columns for core fields and JSON text for params, metrics, and artifacts.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-S5: Metric direction

Extend best-run logic so the caller can say whether higher or lower is better. Keep the default documented and simple.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 10. Brutal exercises

### W12-B1: Reproduce from a record

Pick a saved run. Use only its record and project code to rerun training with the same parameters and dataset reference. Compare metrics and explain differences.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-B2: Five-run report

Create five run records. Generate a text report showing best macro F1, all runs sorted by macro F1, parameter differences between best and worst, artifact path, and missing-artifact warnings.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-B3: Orphan artifact detector

Simulate a crash after model saving but before run saving. Write a helper that lists model artifacts not referenced by any run record.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### W12-B4: Compatibility loader

Create an old thin run record missing `status` and `artifacts`. Make `from_dict` load it with documented defaults while preserving newer full records.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 11. Mini project task

### Build the Week 12 tracker

Implement a local experiment tracker for the Week 11 classifier. It must start a run, record params, train, save a run-ID-named artifact, record metrics, record dataset reference and seed, save the record, list runs, show one run, compare runs, and preserve failed-run information.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### Acceptance criteria

Records include params, metrics, artifacts, dataset reference, timestamp, status, and error message. Listing is deterministic. Comparison handles missing metrics. Tests cover round trip, save, load, missing run, listing, comparison, and failed runs. Architecture boundaries remain clean.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

## 12. Completion checklist

### Final checklist

You can define the vocabulary, explain every run-record field, save and load records, list and compare runs, tie artifacts to run IDs, record dataset reference and seed, record failed runs, test filesystem behavior with isolated paths, and explain why no future-week tools were needed.

**Do this:**
1. Write the smallest implementation or written answer that satisfies the prompt.
2. Use Week 11 classifier examples for parameters, metrics, and artifacts.
3. Check your work manually before relying on a test.
4. Add or describe a test that would catch the most likely regression.

**Done when:**
- The result is readable to a beginner.
- The behavior preserves params, metrics, artifacts, or reproducibility metadata.
- The work does not introduce future-week concepts or unrequested dependencies.

### Checklist items

- [ ] I can define experiment, run, parameter, metric, artifact, metadata, reproducibility, and lineage.
- [ ] I can implement or sketch `ExperimentRun`.
- [ ] I can save and load JSON records.
- [ ] I can list runs deterministically.
- [ ] I can compare runs with missing metrics.
- [ ] I can connect a saved model artifact to a run ID.
- [ ] I can record dataset reference and random seed.
- [ ] I can preserve failed-run information.
- [ ] I can test with isolated filesystem paths.
- [ ] I can explain the architecture boundaries aloud.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
