# Validation - Week 12 Experiment Tracking

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,ml]"
python -m researchops.ml.train --data examples/training_data --output artifacts/topic_classifier.joblib
ls -1 artifacts/experiments
pytest tests/unit/test_experiment_tracker.py -v
pytest tests/integration/test_training_records_run.py -v
```

## Expected outputs
- Training command prints metrics and writes a model artifact.
- `artifacts/experiments/` contains a new run file.
- Tracker tests and integration tests pass.

## Pytest commands and expected results
```bash
pytest -k "experiment_tracker or training_records_run" -v
pytest -q
```

Expected result: each training run leaves behind a usable record containing params, metrics, and artifact references, making the ML workflow reproducible.

## Completion checklist
- [ ] Experiment model exists.
- [ ] Tracker writes run files.
- [ ] Run IDs are unique.
- [ ] Params are recorded.
- [ ] Metrics are recorded.
- [ ] Artifact path is recorded.
- [ ] Training integrates with the tracker.
- [ ] Unit and integration tests pass.
- [ ] Run records are human-readable.
- [ ] `pytest -q` passes.
- [ ] You can compare at least two stored runs.
