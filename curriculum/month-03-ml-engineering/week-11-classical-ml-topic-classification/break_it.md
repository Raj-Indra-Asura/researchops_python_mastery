<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It — Week 11 Classical ML Topic Classification

These experiments reveal how ML pipelines fail in ways that are easy to miss. Each one is designed to produce an instructive failure.

---

## Purpose of failure practice

Classical ML can fail while still producing numbers that look official. These experiments teach you to distrust impressive metrics until you have checked leakage, labels, class balance, artifact paths, and input validation. In ResearchOps, a topic classifier is only useful if the learner can explain why the evaluation is honest.

## Failure lab rules

1. Change only one part of the pipeline at a time: split order, labels, artifact path, input text, or class balance.
2. Predict the metric or exception before running the experiment.
3. Keep the correct Pipeline version nearby so you can compare against the broken version.
4. For each experiment, record how to cause it, expected error or metric change, how to inspect it, how to fix it, the test that should catch it, what it teaches, and common wrong fixes.
5. Restore the safe training flow before continuing: split raw texts first, fit TF-IDF inside the Pipeline, then evaluate on held-out data.
6. Do not introduce later-week techniques to hide the problem; Week 11 uses classical scikit-learn tools only.

## Intentional break experiments

## Experiment 1: Fit the vectorizer before splitting

Implement this explicitly wrong version:

```python
# LEAKY VERSION
vectorizer = TfidfVectorizer(max_features=5000)
all_features = vectorizer.fit_transform(texts)  # fit on everything
X_train, X_test, y_train, y_test = train_test_split(all_features, labels, test_size=0.2)
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
print(classification_report(y_test, preds))
```

Then run the correct Pipeline version with the same data and compare the accuracy scores.

**What to observe:** On a small dataset, the leaky version may show 5-15% higher accuracy. It looks better but it is not. The model has been evaluated on data it already "knows" through the IDF calculation.

**Questions to answer:** By how much does accuracy differ? If someone showed you only the leaky results, would you trust them? What is the cost of deploying a model evaluated with leakage?

---

## Experiment 2: Shuffle labels intentionally

After building a working pipeline, shuffle the labels randomly before training:

```python
import random
random.seed(999)
random.shuffle(labels)  # labels no longer correspond to texts
```

Train the model. What does the `classification_report` show? What happened to F1?

**What to observe:** All metrics should collapse toward the random baseline (~1/N for N classes, e.g., 25% for 4 classes). The model cannot learn anything because the signal has been destroyed.

**Questions to answer:** What does this experiment prove about the training process? If a model shows near-random metrics, what are the possible causes? (Hint: shuffled labels, too little data, labels that do not correspond to actual text patterns, or leakage in the opposite direction.)

---

## Experiment 3: Save to a missing directory

Try:

```python
joblib.dump(pipeline, Path("/tmp/nonexistent_dir/model.joblib"))
```

**What to observe:** `FileNotFoundError: [Errno 2] No such file or directory`. joblib does not create parent directories.

Now fix it with:

```python
output_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(pipeline, output_path)
```

**Questions to answer:** Should the training script or the caller be responsible for creating the output directory? What is `parents=True` and `exist_ok=True` doing? Write a test that verifies the directory is created.

---

## Experiment 4: Predict on an empty string

After training, run:

```python
pipeline.predict([""])
pipeline.predict(["   "])
pipeline.predict(["the the the the"])
```

**What to observe:** These do not crash — scikit-learn handles them gracefully. But what label is predicted? Is it meaningful? What would happen in production if the paper extraction produced empty text?

**Questions to answer:** What should your system do with an empty text input? Should you validate inputs before prediction? Write a guard that raises a clear error for empty or near-empty inputs.

---

## Experiment 5: Extremely imbalanced dataset

Create a training dataset where 90% of examples are `nlp` and 10% are `systems`. Train and evaluate.

**What to observe:** Accuracy may be 88-92% even if the model only ever predicts `nlp`. Look at the `systems` row in the classification report. What is the recall?

Now add `class_weight="balanced"` to LogisticRegression. How do the metrics for `systems` change?

**Questions to answer:** Is high accuracy a sign of a good model here? What metric would you optimize for if you cared most about not missing `systems` papers? What is the tradeoff of `class_weight="balanced"`?

---

## Experiment 6: Tiny dataset

Reduce your training dataset to 3 examples per class (total: 12-16 examples). Train and evaluate.

**What to observe:** With `test_size=0.2`, you might get 2-3 test examples. The metrics become unstable — a single prediction change shifts F1 by 30%. 

Also, `stratify=labels` may fail if there are fewer examples than splits (try it).

**Questions to answer:** What is the minimum dataset size for meaningful evaluation? What warning does scikit-learn give when a class has too few examples? How does this affect your trust in the reported metrics?

---

## Debugging tasks

**Task D1: Print class counts before every training run**

Add to your training function:

```python
from collections import Counter
label_counts = Counter(labels)
for label, count in sorted(label_counts.items()):
    print(f"  {label}: {count}")
```

Run this on your dataset. Are the classes balanced? If not, does that match what the classification report shows?

**Task D2: Inspect the vocabulary**

After training, check how many unique terms your vectorizer learned:

```python
vocab_size = len(pipeline.named_steps["tfidf"].vocabulary_)
print(f"Vocabulary size: {vocab_size}")
```

How does this compare to `max_features=5000`? What happens if your dataset has fewer than 5000 unique terms?

**Task D3: Run pytest after adding ML code**

Add the ML code and run:

```bash
pytest -q
```

**What to verify:** The existing test suite still passes. Adding new code should not break existing tests. If it does, find the dependency that changed.

---

## Debugging checklist

Use this checklist when a Week 11 model result looks suspicious:

- [ ] Did `train_test_split` happen before `TfidfVectorizer.fit`?
- [ ] Are labels still aligned with texts after shuffling or loading?
- [ ] Did you print class counts before training?
- [ ] Does the classification report show per-class precision, recall, F1, and support?
- [ ] Does the artifact parent directory exist before `joblib.dump`?
- [ ] Did you test empty or near-empty prediction input with a clear guard?
- [ ] Did `pytest -q` still pass after adding ML code?

---

## Edge cases to explore

**EC1: Duplicate documents with different labels**

Add the same text twice with different labels (e.g., one as `nlp` and one as `systems`). What does the classifier learn? What does this suggest about label quality?

**EC2: Very short texts**

Add examples that are only 3-5 words long. Does TF-IDF still work meaningfully? What is the TF-IDF score for a word that appears in a 4-word document?

**EC3: A label with only one training example**

Add a label `survey` with exactly one training example. What happens during `train_test_split` with `stratify=labels`? What happens to the metrics for that class?

---

## Reflection after breaking

1. Which metric hid a real problem in your experiments? How would you detect it without the experiments?
2. What did leakage look like in practice? How large was the metric inflation?
3. What would improve the dataset more than switching the model class?
4. If you had to report the quality of this model to a non-technical stakeholder, what would you say?
5. What is the one thing you would change about your training dataset before adding more model complexity?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
