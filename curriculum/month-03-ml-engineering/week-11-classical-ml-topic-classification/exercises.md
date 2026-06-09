<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 11 Classical ML Topic Classification

## Warm-up: ML mechanics

**Exercise W11-1: TF-IDF by hand**

Take three sentences:

1. "attention is all you need transformer attention"
2. "transformer model attention mechanism layer"
3. "distributed file system replication fault tolerance"

Compute TF-IDF by hand (or in a Python REPL using `TfidfVectorizer`) for the word "attention". 

- What is TF("attention", sentence 1)?
- What is IDF("attention") across all three sentences?
- What is TF-IDF("attention", sentence 3)?

What does the TF-IDF score of "attention" in sentence 3 tell you?

**Exercise W11-2: Pipeline vs. manual leakage**

Write two training pipelines:

**Leaky version** (wrong):
```python
vectorizer = TfidfVectorizer()
all_features = vectorizer.fit_transform(texts)
X_train, X_test = split after vectorizing
```

**Correct version**:
```python
pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression())])
X_train, X_test = split before training
pipeline.fit(X_train, y_train)
```

Use a toy dataset of 10-20 short sentences with two labels. Measure accuracy on the test set for both versions. Is the leaky version's accuracy higher? Why?

**Exercise W11-3: Confusion matrix reading**

Given this confusion matrix for three classes (nlp, systems, vision):

```
              Predicted:
            nlp  sys  vis
Actual: nlp [ 10   2    0 ]
        sys [  3   8    1 ]
        vis [  0   0   12 ]
```

Answer:
1. How many `systems` papers were misclassified as `nlp`?
2. What is the recall for `vision`?
3. What is the precision for `nlp`?
4. Which class is the model best at? Which is it worst at?
5. What does the model confuse `systems` papers with?

**Exercise W11-4: Class imbalance experiment**

Create a toy dataset where 90% of examples have label `nlp` and 10% have label `systems`. Train a classifier. What accuracy does the model report if it just always predicts `nlp`? Now compute precision and recall for `systems`. What does this teach you about accuracy as a metric?

---

## Project exercises: ResearchOps

**Exercise W11-5: Create a labeled training dataset**

Create `examples/training_data/` with at least 4 JSONL files (one per topic). Each file should have at least 5 examples. Topics to use: `nlp`, `systems`, `vision`, `rag`.

Format for each line:
```json
{"text": "attention mechanism transformer self-attention multi-head"}
```

Aim for realistic research-paper-like text. If you have no real papers to use, write short representative descriptions.

**Exercise W11-6: Write load_training_data**

Implement `load_training_data(data_dir: Path) -> tuple[list[str], list[str]]` that:

1. Reads all `.jsonl` files in `data_dir`.
2. Uses the filename (without extension) as the label.
3. Parses each line as JSON and extracts the `"text"` field.
4. Returns `(texts, labels)`.

Write a unit test for this function with a temporary directory containing two JSONL files.

**Exercise W11-7: Implement the full training pipeline**

Implement `train(data_dir, output_path)` following the structure in notes.md. Your implementation must:

1. Print class counts before training.
2. Print train and test sizes after splitting.
3. Use a Pipeline with TF-IDF and LogisticRegression.
4. Print the full `classification_report`.
5. Save the artifact to `output_path`.

Run it:
```bash
python -m researchops.ml.train --data examples/training_data --output artifacts/topic_classifier.joblib
```

**Exercise W11-8: Test the training pipeline**

Write a test in `tests/integration/test_training_pipeline.py` that:

1. Creates a temporary training directory with at least 3 labels and 5 examples each.
2. Calls your training function.
3. Asserts that the artifact file was created.
4. Loads the artifact with `joblib.load`.
5. Calls `pipeline.predict(["some text about neural networks"])`.
6. Asserts that the returned label is one of the known classes.

**Exercise W11-9: Load and run inference from the CLI**

Write a simple prediction script or CLI command that:
1. Loads the saved artifact.
2. Accepts a text argument from the command line.
3. Prints the predicted topic.

Test it:
```bash
python -m researchops.ml.predict "We propose a novel attention mechanism..."
# Expected output: Predicted topic: nlp
```

---

## Stretch exercises

**Exercise W11-S1: Compare two classifiers**

Replace `LogisticRegression` with `LinearSVC` (Support Vector Machine) and compare the classification reports. Which performs better on your dataset? Why might that be?

```python
from sklearn.svm import LinearSVC
```

**Exercise W11-S2: Print top features per class**

After training a LogisticRegression pipeline, extract the most informative words for each class:

```python
feature_names = pipeline.named_steps["tfidf"].get_feature_names_out()
clf = pipeline.named_steps["clf"]
for i, class_name in enumerate(clf.classes_):
    top_indices = clf.coef_[i].argsort()[-10:][::-1]
    top_words = [feature_names[j] for j in top_indices]
    print(f"{class_name}: {', '.join(top_words)}")
```

Do the top words make sense for each class? What does this tell you about how the model works?

**Exercise W11-S3: Add class weights for imbalance**

If your dataset has imbalanced classes, try:

```python
LogisticRegression(max_iter=1000, class_weight="balanced")
```

Does the F1 score for the minority class improve? Does overall accuracy change? Write a one-paragraph explanation of the tradeoff.

---

## Written reflection questions

1. You built a model with 85% accuracy on the test set. Your colleague is excited. You are cautious. What three questions do you ask before celebrating?

2. You fit `TfidfVectorizer` before the train/test split. Your accuracy looks great. Why is this result untrustworthy?

3. The model confuses `rag` and `nlp` papers 30% of the time. What would you do first — change the model or change the labels? Why?

4. Why is `classification_report` more useful than accuracy alone? Give a concrete example where accuracy would lie.

5. A colleague says "just use a Jupyter notebook for the training pipeline." What is your response? What specific problems would you encounter six months from now?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
