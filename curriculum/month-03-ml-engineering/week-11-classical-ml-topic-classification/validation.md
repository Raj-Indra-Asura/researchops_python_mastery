
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 11 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 11 Classical ML Topic Classification

## Pre-validation checklist

Before validating the classifier:

- [ ] The ML optional dependencies are installed with `python -m pip install -e ".[dev,ml]"`.
- [ ] Training data is labeled consistently and each class has enough examples for a meaningful split.
- [ ] The vectorizer is inside a scikit-learn `Pipeline`, not fitted before the train/test split.
- [ ] Artifact output directories are created by the training flow before saving.


## Commands to run

```bash
# Activate your environment
source .venv/bin/activate
python -m pip install -e ".[dev,ml]"

# Step 1: Lint — check ML code follows style rules
ruff check src tests

# Step 2: Run the training pipeline
python -m researchops.ml.train \
  --data examples/training_data \
  --output artifacts/topic_classifier.joblib

# Step 3: Verify artifact was created
ls -lh artifacts/topic_classifier.joblib

# Step 4: Run inference on a new text
python -m researchops.ml.predict "attention mechanism transformer self-attention"

# Step 5: Run ML tests
pytest tests/unit/ -k "ml" -v
pytest tests/integration/ -k "training" -v

# Step 6: Full suite
pytest -q
```

## Tests that must pass

Week 11 must prove both ordinary code quality and ML-specific behavior:

- `ruff check src tests` must pass.
- Unit tests for data loading, preprocessing helpers, and prediction guards must pass.
- Integration tests for the training command or training function must pass.
- `pytest -q` must pass after the classifier artifact can be loaded and used for prediction.

## Expected outputs

Training command should print:
```
Dataset: N examples, M classes
  nlp: X examples
  systems: Y examples
  ...
Train: N_train, Test: N_test

Classification report (test set):
              precision    recall  f1-score   support

         nlp       0.xx      0.xx      0.xx        N
     systems       0.xx      0.xx      0.xx        N
      vision       0.xx      0.xx      0.xx        N

    accuracy                           0.xx        N

Model saved to artifacts/topic_classifier.joblib
```

The exact metric values depend on your dataset. What matters is that the report prints, the artifact is saved, and the metrics make sense (not all zeros, not 100%).

## Manual checks

Inspect model behavior, not just command exit codes:

- Read the class-count printout and confirm no class is accidentally empty.
- Read the classification report and inspect precision, recall, F1, and support for every class.
- Load the saved `.joblib` artifact and make one prediction on a new abstract-like sentence.
- Confirm suspiciously perfect scores are explained by tiny data, duplicate examples, or leakage before trusting them.

## Verifying no leakage

The vectorizer must be inside the Pipeline:

```bash
python -c "
import joblib
p = joblib.load('artifacts/topic_classifier.joblib')
print(type(p.named_steps['tfidf']))   # should be TfidfVectorizer
print(type(p.named_steps['clf']))     # should be LogisticRegression
print('Pipeline structure OK')
"
```

## Artifact integrity check

```bash
python -c "
import joblib
p = joblib.load('artifacts/topic_classifier.joblib')
result = p.predict(['neural network attention transformer'])
print(f'Prediction: {result[0]}')
print('Artifact loads and predicts OK')
"
```

## Architecture checks

- ML implementation belongs under `src/researchops/ml/`.
- Services should depend on core protocols and should not import scikit-learn directly.
- Core models and interfaces must not import `sklearn`, `numpy`, `pandas`, or joblib.
- CLI or training entry points may wire data paths, model training, and artifact output, but business decisions should remain testable without the CLI.

## Documentation checks

- [ ] Notes explain TF-IDF, train/test split, Pipeline, LogisticRegression, and metrics from first principles.
- [ ] Exercises include code reading for `src/researchops/ml/`, implementation, testing, debugging, and dataset-quality work.
- [ ] Break-it labs warn about leakage, shuffled labels, empty input, imbalance, tiny data, and artifact paths.
- [ ] Validation tells the learner which metric patterns are suspicious, not only which command should pass.

## Do-not-proceed warnings

Do not advance to Week 12 if any of these are true:

- `TfidfVectorizer` is fitted on all texts before splitting.
- Metrics are all zeros, all perfect, or based on only one or two test examples and you cannot explain why.
- The artifact cannot be loaded with joblib and used for prediction.
- Empty or whitespace-only prediction input produces a confident-looking topic without a clear guard or documented behavior.
- New ML code breaks existing non-ML tests.

## Ruthless mentor checkpoint

Answer these aloud:

1. Why must raw text be split before TF-IDF fitting?
2. What does `support` tell you in a classification report?
3. Why can high accuracy be misleading on an imbalanced paper-topic dataset?
4. What exactly is stored in the `.joblib` artifact, and how do you prove it still works?

## Definition of done

- [ ] `examples/training_data/` exists with at least 4 JSONL topic files.
- [ ] Each file has at least 5 examples.
- [ ] Training command runs without errors.
- [ ] `classification_report` is printed.
- [ ] `artifacts/topic_classifier.joblib` exists.
- [ ] Loading the artifact and predicting works.
- [ ] Vectorizer is inside the Pipeline (no leakage risk).
- [ ] Unit test for `load_training_data` passes.
- [ ] Integration test for full training run passes.
- [ ] `pytest -q` passes.
- [ ] `ruff check src tests` exits clean.
- [ ] You can explain every line of the training script.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
