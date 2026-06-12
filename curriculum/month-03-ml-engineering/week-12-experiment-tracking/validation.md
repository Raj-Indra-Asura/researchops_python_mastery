
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 12 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 12 Experiment Tracking

## Pre-validation checklist

Before validating experiment tracking:

- [ ] Week 11 training works and saves a loadable classifier artifact.
- [ ] Each new run gets a unique run ID.
- [ ] Params are simple JSON-serializable values, preferably strings for configuration choices.
- [ ] Metric names are consistent across runs you plan to compare.
- [ ] Artifact filenames include the run ID or another unique run-specific identifier.


## Commands to run

```bash
# Activate your environment
source .venv/bin/activate
python -m pip install -e ".[dev,ml]"

# Step 1: Lint
ruff check src tests

# Step 2: Train run 1 (baseline)
python -m researchops.ml.train \
  --data examples/training_data \
  --output artifacts/models/topic_classifier.joblib \
  --experiment tfidf-baseline \
  --max-features 5000

# Step 3: Train run 2 (different params)
python -m researchops.ml.train \
  --data examples/training_data \
  --output artifacts/models/topic_classifier.joblib \
  --experiment tfidf-baseline \
  --max-features 10000

# Step 4: List all runs
researchops experiment list

# Step 5: Show the first run (replace with actual run ID from list output)
researchops experiment show RUN_ID_1

# Step 6: Compare both runs
researchops experiment compare RUN_ID_1 RUN_ID_2

# Step 7: Verify experiment files
ls -la artifacts/experiments/

# Step 8: Verify model files (one per run)
ls -la artifacts/models/

# Step 9: Run all tests
pytest -q
```

## Tests that must pass

Experiment tracking needs round-trip proof:

- Unit tests for run creation, serialization, save/load, list, and compare must pass.
- A test must prove missing run IDs produce a clear error or empty result according to the chosen contract.
- An integration test must prove every recorded artifact path points to an existing model file.
- `ruff check src tests` and `pytest -q` must pass after two separate tracked runs.

## Expected outputs

After two training runs:

```bash
$ ls artifacts/experiments/
run-20240915-1030-a3f8b2.json
run-20240915-1145-c9d2e1.json

$ ls artifacts/models/
topic-classifier-run-20240915-1030-a3f8b2.joblib
topic-classifier-run-20240915-1145-c9d2e1.joblib
```

Two model files, not one — no overwriting.

`experiment list` output:

```
Run ID                       Experiment       Timestamp              F1 Macro
run-20240915-1030-a3f8b2     tfidf-baseline   2024-09-15 10:30:42   0.85
run-20240915-1145-c9d2e1     tfidf-baseline   2024-09-15 11:45:03   0.87
```

`experiment compare RUN_ID_1 RUN_ID_2` output:

```
Metric               run-20240915-1030-a3f8b2      run-20240915-1145-c9d2e1
---------------------------------------------------------------------------
accuracy             0.87                          0.89
f1_macro             0.85                          0.87
train_size           80                            80
test_size            20                            20
```

## Manual checks

Use the CLI output as evidence:

- Run `researchops experiment list` and confirm both runs are visible.
- Run `researchops experiment show RUN_ID` and confirm params, metrics, timestamp, status, and artifact path are present.
- Run `researchops experiment compare RUN_ID_1 RUN_ID_2` and confirm metric rows line up by exact metric key.
- Open the experiment record file or SQLite row and verify it matches the CLI output.

## Integrity check

Run this to verify every run record points to an existing artifact:

```bash
python -c "
from pathlib import Path
import json

experiments_dir = Path('artifacts/experiments')
for f in sorted(experiments_dir.glob('*.json')):
    data = json.loads(f.read_text())
    artifact = Path(data['artifact_path'])
    status = 'OK' if artifact.exists() else 'MISSING'
    print(f\"{data['run_id']}: {status}\")
"
```

Expected: all runs report `OK`.

## Architecture checks

- `src/researchops/core/interfaces.py` owns the `ExperimentRepository` protocol.
- `src/researchops/services/experiment_service.py` should depend on that protocol, not on SQLite or file layout details.
- `src/researchops/storage/experiment_repository.py` may implement concrete persistence details.
- Training or CLI code may wire concrete repositories, artifact paths, and command arguments at the edge.

## Documentation checks

- [ ] Notes define run, parameter, metric, artifact, metadata, lineage, and reproducibility in beginner language.
- [ ] Exercises include code reading for the experiment protocol, service seam, and storage seam.
- [ ] Break-it labs show how missing artifacts, overwrites, bad params, metric-name drift, and crashes damage evidence.
- [ ] Validation defines exactly what counts as a trustworthy tracked run.

## Do-not-proceed warnings

Do not finish Month 3 if any of these are true:

- Two training runs overwrite the same model artifact.
- A run record exists without an artifact path, or the artifact path points to a missing file.
- Params cannot be serialized and loaded back.
- Metric names differ accidentally between runs, making comparison misleading.
- The learner cannot answer what changed between two runs using only the tracker output.

## Ruthless mentor checkpoint

Answer these aloud:

1. What minimum fields make a run record useful six weeks later?
2. Why is a model artifact without params and metrics not enough evidence?
3. How does run-specific artifact naming prevent silent data loss?
4. Why should experiment services depend on a repository protocol instead of a concrete SQLite implementation?

## Definition of done

- [ ] `ExperimentRun` dataclass implemented with all fields.
- [ ] `save_run`, `load_run`, `list_runs`, `compare_runs` implemented.
- [ ] Training pipeline logs every run automatically.
- [ ] Artifact filenames include the run ID.
- [ ] Two runs with different params are logged.
- [ ] `experiment list` displays a summary table.
- [ ] `experiment show RUN_ID` displays all fields.
- [ ] `experiment compare RUN_ID_1 RUN_ID_2` shows side-by-side metrics.
- [ ] Unit tests for `ExperimentRun` pass.
- [ ] Unit tests for `save_run`/`load_run` pass.
- [ ] Integration test verifying artifact existence pass.
- [ ] Every run record links to an existing artifact.
- [ ] `pytest -q` passes.
- [ ] `ruff check src tests` exits clean.
- [ ] You can answer: "What changed between these two runs?" using only the CLI.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 12 — Experiment Tracking:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
