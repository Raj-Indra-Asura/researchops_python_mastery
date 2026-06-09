<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 12 Experiment Tracking

## Chapter overview

### Purpose

Week 12 teaches ResearchOps to remember machine-learning work.
The Week 11 classifier can produce a score, but a score printed once is not durable evidence.
A tracker records the run ID, experiment name, parameters, metrics, artifacts, and metadata.
A learner should finish this chapter able to explain how a saved model file is tied to the settings that produced it.
Stay local: JSON files and SQLite-style thinking are enough for this chapter.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Milestone

The visible milestone is a local experiment tracker for classifier runs.
It should save one record per training attempt.
It should list old records in deterministic order.
It should show a single record in detail.
It should compare selected records by metrics such as macro F1.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Boundaries

This chapter is not about hosted ML platforms.
It is not about web APIs, containers, dashboards, or future model-representation topics.
It is about the basic engineering habit of recording what happened.
That habit makes later model work auditable.
The implementation should remain understandable to a learner who has completed Weeks 1 through 11.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Study path

First learn the vocabulary.
Then inspect a run as a plain dictionary.
Then wrap the shape in a dataclass.
Then save and load records.
Finally connect the tracker to Week 11 training and compare runs.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## What you already know from previous weeks

### Files and paths

Week 2 taught you that paths are data, not magic strings.
Run records live on disk when JSON is used.
Artifact paths must be written carefully because another command will read them later.
A useful error message should include the path or run ID that failed.
That makes tracking bugs much easier to diagnose.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Domain objects

Week 3 introduced objects that represent project ideas.
An experiment run is a domain idea, not just a random dictionary.
A dataclass gives the run a named shape.
Named fields make code easier to read than scattered keys.
The shape also tells tests what must be preserved.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### SQLite memory

Week 5 introduced SQLite as a local database.
This week can start with JSON because it is simple.
SQLite becomes useful when you want sorted, filtered, and aggregated run queries.
The concepts are the same either way: save records, load records, and preserve fields.
Do not let the storage choice change the meaning of a run.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Protocols

Week 9 taught dependency boundaries.
A service should depend on an `ExperimentRepository` protocol.
A JSON repository and SQLite repository can both implement that protocol.
The service should not care which storage implementation is currently wired in.
That is how ResearchOps stays flexible without becoming tangled.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Classifier context

Week 11 supplied the ML behavior being tracked.
The classifier has parameters such as feature limits and model settings.
It has metrics such as accuracy and macro F1.
It produces an artifact such as a saved model file.
Week 12 records those facts instead of changing the classifier concept itself.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## What problem this week solves

### Memory loss

A terminal score disappears when the terminal scrolls away.
A notebook note may not say which code path produced the result.
An overwritten model file destroys the previous artifact.
These are ordinary ML project failures.
Experiment tracking prevents them by creating durable records.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Comparison

Research requires comparing attempts.
If one run uses `max_features=5000` and another uses `max_features=10000`, the comparison only makes sense if both settings are recorded.
The metrics alone do not tell the full story.
The parameter difference explains what changed.
A comparison command should make that difference visible or easy to inspect.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Lineage

Lineage means the chain from data to run to artifact.
A model file should not be anonymous.
The run record should say which dataset reference and parameters produced it.
The artifact filename should usually include the run ID.
That way a saved file can be traced back to its evidence.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Reproducibility

Reproducibility means reducing mystery.
It does not promise that every decimal will match on every machine.
It does require enough recorded information to rerun or audit the attempt.
For this chapter, record parameters, dataset reference, random seed, metrics, status, and artifact path.
Without those fields, future debugging becomes guesswork.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Beginner mental model

### Lab notebook

Think of the tracker as a lab notebook for the classifier.
The dataset is the ingredient collection.
The parameters are recipe choices.
The metrics are measured outcomes.
The artifact is the saved result.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Before and after

Every run has a before side and an after side.
Before training, you know experiment name, dataset reference, seed, and parameters.
After evaluation, you know metrics.
After saving files, you know artifact paths.
After errors, you know status and error message.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Right amount

Tracking does not mean saving every object in memory.
It means saving the information needed to understand and repeat the run.
Too little information makes the record useless.
Too much information makes the record noisy.
The useful middle is params, metrics, artifacts, and reproducibility metadata.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Future reader

Design every field for a future reader.
The future reader might be you tomorrow.
They might be a teammate.
They might be a mentor reviewing your project.
If they can explain the run from the record, the tracker is doing its job.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Core vocabulary

| Term | Simple meaning | ResearchOps example |
|---|---|---|
| Experiment | Named group of related runs | `topic-classifier-baseline` |
| Run | One training attempt | `run-20240915-103042-a3f8` |
| Parameter | Choice before training | `max_features=8000` |
| Metric | Measurement after evaluation | `f1_macro=0.84` |
| Artifact | File produced by a run | saved `.joblib` model |
| Metadata | Context for auditing | dataset reference and seed |

The table is not decoration.
Use these words consistently in code, tests, and CLI output.
Consistent language prevents design mistakes.
If a value is chosen before training, call it a parameter.
If a value is measured after evaluation, call it a metric.

### Experiment

An experiment is a named investigation.
It groups related runs under a shared goal.
For example, `topic-classifier-baseline` can hold several attempts to improve the Week 11 classifier.
The name should describe the investigation, not the final winner.
A good name makes `experiment list` easier to scan.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Run

A run is one execution of training or evaluation.
It has one run ID and one timestamp.
It should point to the artifacts it produced.
It should keep the metrics from that exact attempt.
Do not merge multiple training attempts into one run record.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Parameter

A parameter is chosen before training.
Examples include `max_features`, `C`, `test_size`, and `random_seed`.
Parameters explain what you changed.
They belong in the run record even if the result is bad.
Bad results with known parameters are still useful evidence.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Metric

A metric is measured after evaluation.
Examples include `accuracy`, `precision_macro`, `recall_macro`, and `f1_macro`.
Macro F1 is especially useful when topic labels are imbalanced.
Metrics explain what happened.
They should use stable names across runs.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Artifact

An artifact is a file produced by the run.
The saved classifier model is an artifact.
A predictions file can also be an artifact.
The run record should store artifact paths, not binary model bytes.
The artifact filename should include the run ID to avoid overwrites.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Metadata

Metadata is context.
Dataset reference, code version, seed, status, and error message are metadata.
Metadata answers questions that metrics alone cannot answer.
It helps decide whether two runs are fairly comparable.
It is the difference between a score and an auditable result.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Concept explanations from first principles

### Run records

A run record is structured memory.
It is not just a log line.
It has stable keys and values.
Stable shape matters because old records should remain readable after small code changes.
A dataclass can make that shape explicit.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### JSON storage

JSON is text that maps naturally to Python dictionaries.
It is easy to open and inspect.
One file per run is simple for beginners.
The weakness is that listing and filtering many runs means reading many files.
That weakness is acceptable for the first local tracker.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### SQLite storage

SQLite stores records in tables.
It is better when queries become important.
A simple table can keep run ID, experiment name, timestamp, status, dataset reference, and JSON text for params, metrics, and artifacts.
This avoids over-normalizing too early.
The repository protocol can hide whether JSON or SQLite is used.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Artifact separation

Model artifacts can be large and binary.
JSON metadata should stay readable.
Therefore store a path to the artifact rather than the artifact itself.
The display command can warn if the path no longer exists.
A missing artifact does not mean the record is invalid; it means lineage is broken.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Failed runs

A failed run is still an experiment result.
It tells you that a certain configuration did not work.
If training fails after run creation, save status `failed` and an error message when possible.
This prevents repeated attempts that fail the same way.
Failure records are part of research honesty.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## ResearchOps-specific application

### Classifier run

A ResearchOps classifier run starts with labeled paper data.
It chooses text-processing and model parameters.
It trains the Week 11 topic classifier.
It evaluates predictions against labels.
It saves a model artifact and records the result.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Useful fields

A practical record includes `run_id`, `experiment_name`, `timestamp`, `params`, `metrics`, `artifacts`, `dataset_ref`, `status`, and `error_message`.
The `params` dictionary might hold `max_features`, `C`, `test_size`, and `random_seed`.
The `metrics` dictionary might hold `accuracy` and `f1_macro`.
The `artifacts` dictionary might hold a `model` path.
The `dataset_ref` might be a version label or stable hash.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### CLI behavior

`researchops experiment list` should read existing records.
It should not train a model.
`researchops experiment show RUN_ID` should display one record clearly.
`researchops experiment compare A B` should show metrics side by side.
Those commands make past work discoverable.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Service flow

The CLI wires dependencies.
The service creates or receives a run object.
The training code produces metrics and artifacts.
The repository saves the final record.
Each layer keeps one job.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Code examples with line-by-line explanation

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
import json

@dataclass
class ExperimentRun:
    run_id: str
    experiment_name: str
    timestamp: str
    params: dict[str, object] = field(default_factory=dict)
    metrics: dict[str, float | str | None] = field(default_factory=dict)
    artifacts: dict[str, str] = field(default_factory=dict)
    dataset_ref: str | None = None
    status: str = "created"
    error_message: str | None = None

    @classmethod
    def create(cls, experiment_name: str, params: dict[str, object], dataset_ref: str | None = None) -> "ExperimentRun":
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        run_id = f"run-{stamp}-{uuid4().hex[:8]}"
        return cls(run_id=run_id, experiment_name=experiment_name, timestamp=datetime.now(timezone.utc).isoformat(), params=dict(params), dataset_ref=dataset_ref)

    def to_dict(self) -> dict[str, object]:
        return {"run_id": self.run_id, "experiment_name": self.experiment_name, "timestamp": self.timestamp, "params": self.params, "metrics": self.metrics, "artifacts": self.artifacts, "dataset_ref": self.dataset_ref, "status": self.status, "error_message": self.error_message}
```

Line 1: `from dataclasses import dataclass, field`
This line imports dataclass helpers.
Line 2: `from datetime import datetime, timezone`
This line imports UTC time helpers.
Line 3: `from pathlib import Path`
This line imports path type for storage functions.
Line 4: `from uuid import uuid4`
This line imports UUID fragments for safer IDs.
Line 5: `import json`
This line imports JSON for text storage.
Line 7: `@dataclass`
This line marks the class as a dataclass.
Line 8: `class ExperimentRun:`
This line names the run object.
Line 9: `    run_id: str`
This line stores the unique run identifier.
Line 10: `    experiment_name: str`
This line stores the experiment group.
Line 11: `    timestamp: str`
This line stores creation time as text.
Line 12: `    params: dict[str, object] = field(default_factory=dict)`
This line stores choices made before training.
Line 13: `    metrics: dict[str, float | str | None] = field(default_factory=dict)`
This line stores measurements or status-like metric values.
Line 14: `    artifacts: dict[str, str] = field(default_factory=dict)`
This line stores produced file paths by name.
Line 15: `    dataset_ref: str | None = None`
This line stores the data reference when known.
Line 16: `    status: str = "created"`
This line records lifecycle state.
Line 17: `    error_message: str | None = None`
This line records failure detail when present.
Line 19: `    @classmethod`
This line declares a class method constructor.
Line 20: `    def create(cls, experiment_name: str, params: dict[str, object], dataset_ref: str | None = None) -> "ExperimentRun":`
This line accepts the experiment name, parameter dictionary, and optional data reference.
Line 21: `        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")`
This line creates a readable timestamp for the ID.
Line 22: `        run_id = f"run-{stamp}-{uuid4().hex[:8]}"`
This line adds a random suffix to reduce collisions.
Line 23: `        return cls(run_id=run_id, experiment_name=experiment_name, timestamp=datetime.now(timezone.utc).isoformat(), params=dict(params), dataset_ref=dataset_ref)`
This line returns a new run while copying params.
Line 25: `    def to_dict(self) -> dict[str, object]:`
This line defines conversion to JSON-friendly data.
Line 26: `        return {"run_id": self.run_id, "experiment_name": self.experiment_name, "timestamp": self.timestamp, "params": self.params, "metrics": self.metrics, "artifacts": self.artifacts, "dataset_ref": self.dataset_ref, "status": self.status, "error_message": self.error_message}`
This line returns stable keys that old records can continue to use.

```python
def save_run(run: ExperimentRun, experiments_dir: Path) -> Path:
    experiments_dir.mkdir(parents=True, exist_ok=True)
    output_path = experiments_dir / f"{run.run_id}.json"
    output_path.write_text(json.dumps(run.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return output_path

def load_run(run_id: str, experiments_dir: Path) -> ExperimentRun:
    input_path = experiments_dir / f"{run_id}.json"
    if not input_path.exists():
        raise FileNotFoundError(f"No experiment run found for {run_id}")
    return ExperimentRun.from_dict(json.loads(input_path.read_text(encoding="utf-8")))
```

`save_run` creates the directory before writing so first-time use works.
The output filename uses the run ID so runs do not overwrite each other.
Indented JSON is easier for learners to inspect manually.
`load_run` checks for missing records before parsing.
The missing-run error includes the requested ID so the CLI message is actionable.
A complete implementation also needs `from_dict`, list, compare, and tests.

## Common beginner mistakes

### Only scores

Saving only `f1_macro=0.84` is too thin.
You cannot tell which parameters produced the value.
You cannot tell which data was used.
You cannot locate the model artifact.
Always store context with the score.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Overwrites

Writing every model to `model.joblib` overwrites history.
The newest file replaces the previous file.
The old run record may then point to the wrong model.
Use filenames that contain the run ID.
Example: `topic-classifier-run-20240915-103042-a3f8.joblib`.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Serialization

JSON cannot save every Python object automatically.
`Path`, `datetime`, and some numeric library types may fail.
Convert paths and timestamps to strings.
Convert metrics to plain Python numbers when needed.
Test this with a JSON round trip.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Boundary leaks

Storage code should not train the classifier.
CLI code should not compute macro F1.
Core protocols should not import JSON repositories.
These leaks make tests harder and changes riskier.
Keep responsibilities separate even when the project is small.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Debugging guidance

### Missing record

If a record is missing, check whether training reached the save call.
Then check the experiments directory.
Then check the run ID and filename.
Then inspect errors from JSON writing.
A wrong directory is more common than a broken JSON library.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Bad JSON

If loading raises `JSONDecodeError`, open the file.
The file may be empty, partially written, or manually edited incorrectly.
Create a smaller reproduction with one run record.
Validate that `to_dict()` returns JSON-friendly values.
Add a test that saves and loads the same object.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Wrong comparison

If comparison output is blank, inspect metric keys.
`f1_macro` and `macro_f1` are different strings.
Choose one name and use it consistently.
Handle missing values gracefully in display output.
Do not crash just because one run lacks an optional metric.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Missing artifact

If a record points to a missing artifact, do not pretend the artifact exists.
Display a warning.
Check whether training saved the model before assigning the path.
Check whether cleanup deleted artifacts but not records.
This is a lineage problem, not necessarily a JSON problem.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Design tradeoffs

### JSON first

JSON is ideal for first implementation because it is visible.
A learner can open the run file and read it.
Tests can create isolated directories easily.
The cost is slower querying across many runs.
That cost is acceptable for Week 12.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### SQLite later

SQLite becomes attractive when run counts grow.
It can sort, filter, and aggregate with SQL.
It can enforce uniqueness on run IDs.
It can store params and metrics as JSON text inside columns.
It adds schema complexity, so introduce it deliberately.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Mutable during run

It is practical to create a run before training and fill fields later.
The status may move from `created` to `completed` or `failed`.
After completion, treat the record as historical evidence.
Do not silently edit old metrics to make results look better.
If you need a correction, record it explicitly or create a new run.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Best metric

A simple best-run function can assume higher is better for accuracy and F1.
That assumption should be documented.
It would be wrong for lower-is-better metrics such as loss.
A future extension can store metric direction.
Do not build that extension before the project needs it.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Testing implications

### Round trip

A run converted to a dictionary and back should preserve fields.
This test catches missing keys.
It also catches accidental renames.
Use realistic params and metrics from the classifier.
Keep the test small and direct.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Filesystem

Use `tmp_path` for JSON save and load tests.
Never rely on a personal artifacts directory.
Assert the file exists.
Assert the file contains the run ID.
Then load it through the public loader.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Listing

Create records with known timestamps.
Save them out of order.
Assert `list_runs` returns them sorted.
Deterministic output helps users and tests.
It also makes CLI examples easier to document.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Comparison

Create two runs with one shared metric and one missing metric.
Assert both run IDs appear.
Assert the missing value appears as a clear placeholder.
Assert numeric formatting does not change stored values.
This test protects real comparison behavior.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Failure

Simulate a training error.
Assert a failed run record is saved when possible.
Assert `status` is `failed`.
Assert `error_message` is useful.
This test proves failures are not silently erased.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Architecture implications

### Core

Core can hold the `ExperimentRun` model and repository protocol.
Core should not know about CLI commands.
Core should not know whether storage is JSON or SQLite.
Core names the concepts.
Infrastructure implements persistence.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Services

An `ExperimentService` can create runs, record metrics, choose comparisons, and call the repository.
It should depend on the protocol.
It should be testable with a fake repository.
It should not print rich CLI tables directly.
It should return data the CLI can display.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Infrastructure

A JSON repository writes files.
A SQLite repository writes rows.
Both can implement the same methods.
Neither should train models.
Neither should decide which metric matters for the user.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### CLI

CLI commands parse arguments and display results.
They wire concrete repositories to services.
They should be thin.
Thin CLI code is easier to test with command runners.
Business logic belongs below it.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## How this connects to AI engineering / ML research

### Evidence

ML engineering turns model claims into evidence.
A run record says what was tried.
Metrics say what happened.
Artifacts show what was produced.
Metadata explains the context.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Iteration

Research improves through repeated attempts.
Repeated attempts need memory.
The tracker prevents teams from rediscovering the same failed settings.
It also prevents confusing a lucky run with a reproducible improvement.
This is true even for a small local classifier.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Review

A teammate can inspect records before trusting a model.
A mentor can ask why macro F1 changed.
A future employer can see that your project records lineage.
That makes the project look engineered rather than improvised.
The tool is small, but the habit is professional.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## Mini quizzes

### Quiz set

Is `max_features` a parameter or metric?
Why should the model filename include the run ID?
What does `dataset_ref` protect you from forgetting?
What should `load_run` do when the ID does not exist?
Why can comparing different datasets be misleading?

### More questions

Which layer should know about JSON paths?
Which layer should format CLI output?
Why are failed runs useful?
What values are needed for reproducibility?
When would SQLite be better than JSON?

## Explain-it-aloud prompts

### Prompts

Explain a run without using the word tracker.
Explain params versus metrics using Week 11 examples.
Explain how a run ID links a JSON record to a model artifact.
Explain why `experiment compare` should not retrain models.
Explain how you would debug a record with a missing artifact.

### More prompts

Explain why JSON is a good first storage choice.
Explain what a repository protocol buys you.
Explain why failed run records are honest.
Explain how macro F1 helps with imbalanced topics.
Explain when you are allowed to move to the next week.

## What to memorize

### Memorize

Parameters are chosen before training.
Metrics are measured after evaluation.
Artifacts are files produced by a run.
Metadata is context for audit and reproduction.
Run IDs must be unique and should appear in artifact filenames.

### Also memorize

JSON needs JSON-friendly values.
Use `tmp_path` for filesystem tests.
Services depend on protocols.
Repositories save and load records.
Reproducibility needs data, code, parameters, seed, metrics, and artifacts.

## What to understand deeply

### Depth

Experiment tracking is evidence management.
The tracker supports claims about model quality.
A stable record shape keeps old results readable.
Comparison depends on shared context, not metrics alone.
Reproducibility reduces avoidable mystery.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Deeper

Storage should be replaceable without rewriting business behavior.
Failures are part of the research history.
Artifact paths can become stale and should be checked.
Metric naming consistency is a design decision.
Tests define what historical truth the tracker promises to preserve.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

## What not to worry about yet

### Avoid

Do not add hosted experiment tools.
Do not add automatic hyperparameter search.
Do not add web APIs.
Do not add containers.
Do not add dashboards.

### Also avoid

Do not record every temporary variable.
Do not solve distributed training.
Do not design a large registry too early.
Do not introduce future-week topics.
Do not replace understanding with a dependency.

## Bridge to next week

### Bridge

ResearchOps now has memory for classifier experiments.
Future model work can be compared against saved history.
Before moving forward, you should be able to open a run record and explain every field.
You should be able to trace from data reference to run ID to model artifact.
You should be able to decide whether two runs are fairly comparable.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

### Readiness

You are ready when `list`, `show`, and `compare` make sense without magic.
You are ready when failed runs feel useful rather than embarrassing.
You are ready when storage and service boundaries remain clean.
You are ready when tests protect the record shape.
You are ready when you can explain the full flow aloud.

ResearchOps check:
Can this idea help a future reader understand which data, settings, metrics, and artifacts belonged to one classifier run?
If yes, it belongs in the Week 12 mental model.
If no, leave it out until the project needs it.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 12 — Experiment Tracking:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
