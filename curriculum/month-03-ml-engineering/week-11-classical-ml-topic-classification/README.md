# Week 11 - Classical ML Topic Classification

## Learning objectives
- Prepare labeled text data for supervised learning.
- Use TF-IDF features to represent documents numerically.
- Split data into train and test sets responsibly.
- Train a simple classifier with scikit-learn.
- Evaluate precision, recall, F1, and confusion patterns.
- Persist a baseline model artifact.
- Integrate topic prediction into the ResearchOps workflow.

## Project milestone
Train and evaluate a first topic classifier for research documents using TF-IDF and a classical scikit-learn model.

## Files to modify/create
- `src/researchops/ml/dataset.py`
- `src/researchops/ml/train.py`
- `src/researchops/ml/predict.py`
- `tests/unit/test_ml_dataset.py`
- `tests/integration/test_training_pipeline.py`
- `examples/training_data/`

## Concepts covered
Supervised learning, labels, train/test split, TF-IDF, logistic regression or linear models, metrics, and model artifacts.

## Expected deliverables
- A labeled dataset format for topics.
- A training script or command that outputs metrics.
- A saved model artifact.
- Tests covering dataset preparation and training pipeline shape.

## Definition of done
- [ ] Dataset loader works.
- [ ] TF-IDF vectorization is implemented.
- [ ] Model training succeeds.
- [ ] Metrics are reported on a holdout set.
- [ ] Label leakage is avoided.
- [ ] A model artifact is saved.
- [ ] You can explain what the baseline gets right and wrong.
