# Notes - Week 11 Classical ML Topic Classification

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 11 — Classical ML: Topic Classification](./README.md) › **notes.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Why ML appears only after the data pipeline exists

Machine learning needs data. Not just raw data — clean, labeled, accessible data. Before Week 11, ResearchOps built that foundation:

- **Month 2**: papers are parsed, cleaned, and stored in SQLite.
- **Week 9**: the architecture is clean — services depend on protocols, making the ML layer easy to add without tangling existing code.
- **Week 10**: quality gates exist — we can add ML code and immediately test it.

Now the data pipeline is the dataset. Every paper in the SQLite database is a potential training example. The ML work can begin because the infrastructure is ready.

This is not accidental. Professional ML engineering always works this way:

```
data pipeline first → labeled dataset → ML model → evaluation → artifact
```

Jumping to model code before the data pipeline is solid is a common mistake. It leads to months of "the model is not learning" when the real problem is bad data.

---

## Core vocabulary: dataset, example, label, feature

**Dataset**: a collection of examples used to train or evaluate a model.

**Example**: one row in the dataset. For ResearchOps, one example is one paper with its text and topic label. Example: `("We propose a new attention mechanism for neural machine translation...", "nlp")`.

**Label**: the target output you want the model to predict. In supervised learning, labels are provided during training. For this project, labels are topic categories: `nlp`, `systems`, `vision`, `rag`, `optimization`.

**Feature**: a numeric representation of an input that the model can learn from. Raw text is not a feature. You must convert it to numbers first. This conversion is called **feature extraction** or **vectorization**.

For a tiny example:

| text (raw input) | label |
|---|---|
| "attention is all you need transformer self-attention" | `nlp` |
| "distributed file system fault tolerance replication" | `systems` |
| "image recognition convolutional neural network" | `vision` |

---

## Text vectorization: from words to numbers

Classical ML models like logistic regression work on numeric vectors, not strings. You need a function that maps a text document to a vector of numbers.

The simplest approach: **bag of words**. You count how many times each word appears.

For a vocabulary of ["attention", "transformer", "file", "system"], the document "attention transformer attention" becomes the vector `[2, 1, 0, 0]`.

The problem with raw counts: common words like "the", "is", "a" dominate. They appear in every document and carry no useful information. The model would "learn" that "the" predicts everything.

---

## TF-IDF: giving weight to informative words

**TF-IDF** stands for Term Frequency — Inverse Document Frequency. It is a classic solution to the common-word problem.

**Term Frequency (TF)**: how often a word appears in this document. Words that appear more often are more important to this document.

```
TF(word, document) = count(word in document) / total words in document
```

**Inverse Document Frequency (IDF)**: how rare a word is across all documents. Words that appear in every document (like "the") have low IDF. Words that appear in only a few documents have high IDF.

```
IDF(word) = log(total documents / documents containing word)
```

**TF-IDF**: multiply them together.

```
TF-IDF(word, document) = TF(word, document) × IDF(word)
```

The result: a word that appears often in one document but rarely in the corpus gets a high score. That is exactly what you want — it identifies the distinctive vocabulary of each document.

Intuition for ResearchOps:

- "the" appears in every paper → low IDF → low TF-IDF → near zero weight.
- "transformer" appears in many NLP papers but few systems papers → medium IDF → helps distinguish NLP.
- "fault-tolerance" appears in very few papers → high IDF → very distinctive for systems papers.

---

## scikit-learn pipeline: the right way to combine steps

scikit-learn's `Pipeline` chains transformers and an estimator into a single object. This is important because it prevents leakage (explained below).

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000)),
])
```

Line by line:

`Pipeline([...])` — creates a sequential transformation chain. Each step is a tuple of `(name, transformer_or_estimator)`.

`TfidfVectorizer(max_features=5000)` — converts text to TF-IDF vectors. `max_features=5000` limits the vocabulary to the 5000 most common terms, which controls memory use and sometimes improves generalization.

`LogisticRegression(max_iter=1000)` — a linear classifier. Despite the name, it is a classification algorithm, not regression. `max_iter=1000` allows enough optimization iterations to converge.

When you call `pipeline.fit(X_train, y_train)`:

1. `TfidfVectorizer.fit_transform(X_train)` is called — it learns the vocabulary and IDF weights from the training texts, then transforms them to TF-IDF matrices.
2. `LogisticRegression.fit(tfidf_matrix, y_train)` is called — it learns the classification weights.

When you call `pipeline.predict(X_test)`:

1. `TfidfVectorizer.transform(X_test)` is called — it applies the vocabulary and IDF weights learned from training.
2. `LogisticRegression.predict(tfidf_matrix)` is called — it applies the learned weights.

Note: `.transform` is used on test data, NOT `.fit_transform`. The vocabulary must be fixed from training. This is enforced automatically by using a Pipeline.

---

## Train/test split

You must evaluate the model on data it has never seen during training. Otherwise you are measuring memorization, not generalization.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels,
)
```

Line by line:

`texts` — list of document strings. `labels` — list of topic strings.

`test_size=0.2` — reserve 20% of examples for testing; use 80% for training.

`random_state=42` — seed the random number generator so the split is reproducible. Every time you run with `random_state=42`, you get the same split.

`stratify=labels` — keep the same proportion of each label in both splits. Without this, a rare label might end up entirely in train or entirely in test.

After the split:

- `X_train`, `y_train` — used to fit the pipeline.
- `X_test`, `y_test` — used to evaluate. Touch these only at evaluation time.

---

## Overfitting

**Overfitting** means the model has memorized the training data and does not generalize to new data. Signs: very high accuracy on training set, much lower accuracy on test set.

Example: if you use a very large vocabulary and train on a small dataset, the model may learn that a specific document has the word "Vaswani" (author of the Attention paper), and correctly classify it — but only because it memorized that specific document.

Ways to detect overfitting:

- Evaluate on the held-out test set (not the training set).
- Compare training accuracy vs. test accuracy. A large gap is a warning sign.

Ways to reduce overfitting:

- More training data.
- Smaller vocabulary (`max_features`).
- Regularization (logistic regression's `C` parameter).

For a beginner baseline, do not worry too much about overfitting. Build a working system first, measure it, then improve.

---

## Leakage

**Leakage** is when information from the test set influences the training process, making your evaluation metrics unrealistically optimistic.

The classic TF-IDF leakage mistake:

```python
# WRONG — leakage!
vectorizer = TfidfVectorizer()
all_features = vectorizer.fit_transform(texts)  # fit on ALL data including test
X_train, X_test = split(all_features)           # split AFTER fitting — too late!
```

The IDF values are now computed from the test set too. The model has implicitly "seen" the test documents when learning term weights.

The correct approach:

```python
# CORRECT — no leakage, achieved by using a Pipeline
pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression())])
pipeline.fit(X_train, y_train)   # vectorizer is fit ONLY on X_train
pipeline.predict(X_test)         # vectorizer transforms X_test using training vocabulary
```

A Pipeline protects you from this because `fit_transform` is called only on training data, and `transform` is called on test data.

---

## Metrics: accuracy, precision, recall, F1, confusion matrix

**Accuracy** is the simplest metric: percentage of correct predictions.

```
accuracy = correct predictions / total predictions
```

The problem: accuracy is misleading when classes are imbalanced. If 90% of papers are labelled "nlp", a model that always predicts "nlp" has 90% accuracy but is useless for other topics.

**Precision** for a class: of all predictions of this class, how many were correct?

```
precision = true positives / (true positives + false positives)
```

Example: the model predicted "systems" 10 times. 7 were actually systems papers. Precision = 7/10 = 0.70.

**Recall** for a class: of all actual examples of this class, how many did the model find?

```
recall = true positives / (true positives + false negatives)
```

Example: there were 15 actual systems papers. The model found 7. Recall = 7/15 = 0.47.

**F1 score**: the harmonic mean of precision and recall. Useful when you want a single number that balances both.

```
F1 = 2 × (precision × recall) / (precision + recall)
```

**Confusion matrix**: a table showing what the model predicted vs. the true labels.

```
                Predicted:
              nlp  sys  vis
Actual: nlp [  8    1    0 ]
        sys [  2    6    0 ]
        vis [  0    1    7 ]
```

Each row is a true class. Each column is a predicted class. The diagonal (8, 6, 7) shows correct predictions. Off-diagonal entries show confusions.

This matrix reveals patterns: the model sometimes confuses `systems` papers with `nlp` papers (2 cases). This might mean both contain the word "network." That is a useful signal for improving the dataset or features.

scikit-learn makes reporting easy:

```python
from sklearn.metrics import classification_report, confusion_matrix

predictions = pipeline.predict(X_test)
print(classification_report(y_test, predictions))
print(confusion_matrix(y_test, predictions))
```

`classification_report` prints precision, recall, F1, and support (number of examples) for each class. Always look at this, not just accuracy.

---

## Model artifact: saving and loading

After training, you want to reuse the model without retraining. You save the fitted pipeline to a file.

```python
import joblib

# Save
joblib.dump(pipeline, "artifacts/topic_classifier.joblib")

# Load
loaded_pipeline = joblib.load("artifacts/topic_classifier.joblib")
```

`joblib` is scikit-learn's recommended serialization library. It is efficient for large numpy arrays.

The saved artifact contains both the `TfidfVectorizer` (with its learned vocabulary and IDF weights) and the `LogisticRegression` (with its learned weights). Everything needed for inference is bundled together.

**Artifact naming convention**: using a fixed name like `topic_classifier.joblib` means every training run overwrites the previous artifact. Week 12 will improve this with versioned names. For now, a fixed name is acceptable.

---

## Inference: using the trained model

**Inference** means applying the trained model to new, unseen data to produce a prediction.

```python
pipeline = joblib.load("artifacts/topic_classifier.joblib")

new_text = "We propose a novel attention mechanism based on sparse representations..."
predicted_topic = pipeline.predict([new_text])[0]
print(f"Predicted topic: {predicted_topic}")
```

Note `[new_text]` — scikit-learn expects a list of texts, even for a single document. `[0]` extracts the first (and only) prediction.

For ResearchOps, inference could be triggered from the CLI:

```bash
researchops predict-topic "We propose a new retrieval-augmented generation approach..."
```

Or applied in batch when new papers are ingested:

```bash
researchops tag-topics --model artifacts/topic_classifier.joblib
```

---

## CLI-based ML workflow

The complete flow from data to inference:

```
SQLite papers
→ labeled training rows  (export with labels you assign)
→ preprocessing          (clean text)
→ TF-IDF                 (vectorize with vocabulary from training data)
→ classifier             (fit logistic regression)
→ evaluation             (print metrics on test set)
→ saved artifact         (joblib file)
→ CLI inference          (load and predict new papers)
```

Why not notebooks? Jupyter notebooks are excellent for exploration and visualization. But they have serious limitations for portfolio-grade ML engineering:

1. **Reproducibility**: notebook state depends on cell execution order, which is not tracked.
2. **Testing**: you cannot easily write pytest tests for notebook cells.
3. **Version control**: notebook JSON diffs are unreadable.
4. **Automation**: notebooks cannot be called from CI or scheduled jobs without extra tooling.

Build your training pipeline as Python modules, callable from the CLI. Keep notebooks for exploration only. This is the professional pattern.

---

## The full scikit-learn code example

```python
"""
train.py — Topic classifier training script.

Usage:
    python -m researchops.ml.train \
        --data examples/training_data \
        --output artifacts/topic_classifier.joblib
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def load_training_data(data_dir: Path) -> tuple[list[str], list[str]]:
    """Load texts and labels from JSONL files in data_dir.

    Each file should be labelled by its name: nlp.jsonl, systems.jsonl, etc.
    Each line is a JSON object with a "text" field.
    """
    texts: list[str] = []
    labels: list[str] = []

    for jsonl_file in sorted(data_dir.glob("*.jsonl")):
        label = jsonl_file.stem  # filename without extension = topic label
        with jsonl_file.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                texts.append(record["text"])
                labels.append(label)

    return texts, labels


def train(data_dir: Path, output_path: Path) -> None:
    """Full training pipeline: load, split, fit, evaluate, save."""

    # 1. Load dataset
    texts, labels = load_training_data(data_dir)
    print(f"Dataset: {len(texts)} examples, {len(set(labels))} classes")
    for label in sorted(set(labels)):
        count = labels.count(label)
        print(f"  {label}: {count} examples")

    # 2. Split — BEFORE fitting the vectorizer
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")

    # 3. Build pipeline — vectorizer inside prevents leakage
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000, C=1.0)),
    ])

    # 4. Fit on training data only
    pipeline.fit(X_train, y_train)

    # 5. Evaluate on held-out test set
    predictions = pipeline.predict(X_test)
    print("\nClassification report (test set):")
    print(classification_report(y_test, predictions))

    # 6. Save artifact
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output_path)
    print(f"\nModel saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    train(args.data, args.output)
```

Line by line explanation:

`from sklearn.feature_extraction.text import TfidfVectorizer` — the class that converts text to TF-IDF matrices.

`from sklearn.linear_model import LogisticRegression` — the classifier. Despite the name, it is used for classification.

`from sklearn.metrics import classification_report` — generates the full metrics table.

`from sklearn.model_selection import train_test_split` — splits data into training and testing subsets.

`from sklearn.pipeline import Pipeline` — chains steps together in order.

`load_training_data` — reads JSONL files from a directory. Each file name is the label (e.g., `nlp.jsonl` → label `"nlp"`). Each line is one training example.

`train_test_split(..., stratify=labels)` — stratified split ensures each class is represented proportionally in both train and test.

`Pipeline([("tfidf", ...), ("clf", ...)])` — the pipeline chains TF-IDF vectorization and logistic regression. When you call `fit`, both steps are trained in order. When you call `predict`, both are applied in order.

`ngram_range=(1, 2)` — include both unigrams ("attention") and bigrams ("attention mechanism") as features. Bigrams capture phrase-level meaning.

`C=1.0` — the regularization parameter for logistic regression. Higher C = less regularization = model fits training data more closely. Lower C = more regularization = model generalizes more. `C=1.0` is a safe default.

`classification_report(y_test, predictions)` — prints per-class precision, recall, F1, and overall accuracy. This is your evaluation.

`joblib.dump(pipeline, output_path)` — serializes the fitted pipeline. The vocabulary and weights are now on disk.

---

## How this prepares Week 12

After this week, you have:

1. A working training pipeline that runs in one command.
2. A saved model artifact.
3. Printed metrics, but only to stdout — they disappear when the terminal closes.

Week 12 fixes that last problem. You will add **experiment tracking**: every training run will log its parameters and metrics to a structured file. That makes training runs comparable, reproducible, and searchable.

The question Week 12 answers: "Which configuration produced the best results?" Without tracking, you have to remember or guess. With tracking, you can query your history.

---

## Summary

| Concept | Plain English |
|---|---|
| Dataset | Collection of labeled examples |
| Example | One paper + its topic label |
| Label | The topic category you want to predict |
| Feature | A numeric representation of the text |
| TF-IDF | Gives words high weight if frequent in this doc but rare across all docs |
| Classifier | A model that learns to map features to labels |
| Train/test split | Hold back 20% for evaluation; touch it only once |
| Overfitting | Model memorizes training data, fails on new data |
| Leakage | Test data sneaks into training, inflating metrics |
| Pipeline | Chains vectorizer + classifier to prevent leakage |
| Precision | When model predicts class X, how often is it right? |
| Recall | Of all actual class X, how many did the model find? |
| F1 | Harmonic mean of precision and recall |
| Confusion matrix | Table of true vs. predicted labels |
| Model artifact | The saved file containing the trained pipeline |
| Inference | Using the saved model on new data |

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 11 — Classical ML: Topic Classification** · *notes.md — the textbook chapter* (step 2 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [README](./README.md)
- ▶ **Next:** [exercises.md](./exercises.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. **➡ [notes.md](./notes.md) ← you are here**
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
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
