# Validation - Week 11 Classical ML Topic Classification

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,ml]"
python -m researchops.ml.train --data examples/training_data --output artifacts/topic_classifier.joblib
pytest tests/unit/test_ml_dataset.py -v
pytest tests/integration/test_training_pipeline.py -v
```

## Expected outputs
- Training command prints split sizes and evaluation metrics.
- A model artifact is written to `artifacts/`.
- ML dataset and integration tests pass.

## Pytest commands and expected results
```bash
pytest -k "ml_dataset or training_pipeline" -v
pytest -q
```

Expected result: the baseline model trains successfully, evaluation metrics are reported on held-out data, and the saved artifact can be loaded for prediction.

## Completion checklist
- [ ] Labeled dataset loader exists.
- [ ] Train/test split is performed correctly.
- [ ] TF-IDF vectorizer is inside the pipeline.
- [ ] Classifier trains successfully.
- [ ] Metrics are reported.
- [ ] Model artifact is saved.
- [ ] Leakage risks were considered.
- [ ] Dataset and training tests pass.
- [ ] `pytest -q` passes.
- [ ] You can explain the baseline to someone without ML jargon.
