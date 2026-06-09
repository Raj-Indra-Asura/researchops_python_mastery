# Week 12 - Experiment Tracking

## Learning objectives
- Track parameters, metrics, and artifacts for ML runs.
- Design a lightweight experiment record format.
- Version model outputs and training data references.
- Compare multiple training runs systematically.
- Make experiment results reproducible.
- Separate run metadata from model logic.
- Prepare the project for iterative ML improvement.

## Project milestone
Add experiment tracking so every training run records its configuration, metrics, and artifacts in a reproducible way.

## Files to modify/create
- `src/researchops/experiments/tracker.py`
- `src/researchops/experiments/models.py`
- `src/researchops/ml/train.py`
- `tests/unit/test_experiment_tracker.py`
- `tests/integration/test_training_records_run.py`
- `artifacts/experiments/`

## Concepts covered
Experiment metadata, reproducibility, model versioning, parameters, metrics, artifacts, and comparative analysis.

## Expected deliverables
- A tracker that records run IDs, params, metrics, and artifact paths.
- Training code that logs a run automatically.
- Tests proving experiment records are written correctly.
- A convention for model versions and artifact storage.

## Definition of done
- [ ] Experiment runs have unique IDs.
- [ ] Params and metrics are stored together.
- [ ] Artifacts are linked from the run record.
- [ ] Training code logs every run.
- [ ] Run records are easy to inspect.
- [ ] Tests verify tracker behavior.
- [ ] You can compare at least two runs meaningfully.
