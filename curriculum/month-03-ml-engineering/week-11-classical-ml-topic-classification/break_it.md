# Break It - Week 11 Classical ML Topic Classification

## Intentional failure experiments
1. Fit the vectorizer on the full dataset before splitting and compare the suspiciously good metrics.
2. Train on extremely imbalanced labels and inspect how accuracy can mislead you.
3. Save a model artifact to a missing directory and handle the failure cleanly.
4. Predict on empty strings and decide what your system should do.
5. Shuffle labels intentionally and verify that metrics collapse.

## Debugging tasks
- Print class counts before training.
- Inspect the train/test sizes and label distribution.
- Run `pytest -k training_pipeline -v` after changing ML code.

## Edge cases to explore
- Tiny datasets.
- Duplicate documents with different labels.
- Rare classes with only one or two examples.
- Very short extracted texts.

## What did you learn?
- Which metric hid a real problem?
- What did leakage look like in practice?
- What would improve the dataset more than the model choice?
