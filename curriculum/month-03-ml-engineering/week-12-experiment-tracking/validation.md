
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

## Exact shell commands to run

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

## Completion checklist

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
