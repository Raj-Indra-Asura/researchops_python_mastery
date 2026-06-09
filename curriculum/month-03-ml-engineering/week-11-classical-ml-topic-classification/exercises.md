# Exercises - Week 11 Classical ML Topic Classification

## Warm-up exercises
1. Create a tiny labeled dataset of 6-10 documents with topic labels.
2. Vectorize two example texts with `TfidfVectorizer`.
3. Train a classifier on a toy dataset and print predictions.
4. Compute a simple accuracy score on held-out examples.

## Project exercises
1. Build a dataset loader that reads labeled training data.
2. Train a TF-IDF + linear classifier pipeline.
3. Save the trained model artifact and metrics.
4. Add tests for dataset loading and a small end-to-end training run.

## Stretch exercises
1. Compare Logistic Regression with Linear SVM.
2. Add class weights if labels are imbalanced.
3. Print the top weighted terms for each topic.

## Writing questions
1. Why is TF-IDF a strong baseline for text?
2. What leakage risk did you actively avoid?
3. Which metric mattered most for your labels?
4. Where did the model confuse classes?
