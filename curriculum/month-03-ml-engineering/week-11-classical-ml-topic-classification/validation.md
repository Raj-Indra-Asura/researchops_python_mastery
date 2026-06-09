# Validation - Week 11 Classical ML Topic Classification

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 11 — Classical ML: Topic Classification](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Exact shell commands to run

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

## Completion checklist

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 11 — Classical ML: Topic Classification** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 12](../../../curriculum/month-03-ml-engineering/week-12-experiment-tracking/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 12 — Experiment Tracking](../../../curriculum/month-03-ml-engineering/week-12-experiment-tracking/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 11 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
