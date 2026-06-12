<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 11 Classical ML Topic Classification

## How to use this workbook

Work through the exercises in order unless a mentor tells you otherwise.
The goal is not to finish quickly; the goal is to build a trustworthy classical ML workflow.
Use scikit-learn only for modeling in this week.
Do not use torch, transformers, sentence-transformers, embeddings, FastAPI, or async.
For every code exercise, write down the command you ran and the output you expected.
For every metric exercise, explain the result in plain English before changing code.
When an exercise says "paper abstract," use realistic research-style text rather than single keywords.
When an exercise asks for tests, keep them small and deterministic.
If an exercise feels too easy, add one more label and inspect how the metrics change.
If an exercise feels impossible, reduce the dataset to two labels and rebuild the mental model.

## Warm-up exercises

**Exercise W11-W1: TF-IDF by hand**

Use these three mini-documents:
1. `attention mechanism improves neural translation attention`
2. `neural language model learns translation patterns`
3. `storage replication improves fault tolerance`

Answer:
- Which documents contain `attention`?
- Which documents contain `translation`?
- Which term feels more topic-specific for document 1?
- Why should `improves` probably receive less trust as a topic clue?

**Exercise W11-W2: Vocabulary inspection**

Create a `TfidfVectorizer` in a Python REPL or script.
Fit it on the three documents above.
Print `vectorizer.get_feature_names_out()`.
Write down five vocabulary entries and explain what each column means.

**Exercise W11-W3: One prediction by intuition**

Before training any model, classify this abstract by intuition:
`We evaluate consensus and replication strategies for low-latency distributed storage.`
Choose from `nlp`, `systems`, and `vision`.
List the words that influenced your decision.
Later compare your reasoning to the model features.

**Exercise W11-W4: Split vocabulary**

Explain in writing why this order is wrong:
```python
features = vectorizer.fit_transform(all_texts)
X_train, X_test = train_test_split(features)
```
Then explain why this order is safer:
```python
X_train, X_test, y_train, y_test = train_test_split(texts, labels)
pipeline.fit(X_train, y_train)
```

## Code-reading exercises

**Exercise W11-C1: Read a Pipeline**

Given this code:
```python
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000)),
])
```
Answer:
1. Which step converts raw text into numbers?
2. Which step learns how features map to labels?
3. Why are the step names useful during debugging?
4. What would break if the classifier step came first?

**Exercise W11-C2: Read a classification report**

Given this report fragment:
```text
              precision    recall  f1-score   support
nlp              0.80      1.00      0.89         4
systems          1.00      0.50      0.67         4
vision           0.75      0.75      0.75         4
```
Answer:
- Which class had the best recall?
- Which class was missed most often?
- Why might `systems` have perfect precision but weak recall?
- Which class would you inspect first and why?

**Exercise W11-C3: Spot leakage**

Read a training function in the project or in your draft.
Mark the exact line where raw text is split.
Mark the exact line where the vectorizer is fit.
If vectorizer fitting happens before splitting, write a short bug report.

**Exercise W11-C4: Read the ML module boundaries**

Open `src/researchops/ml/topic_classifier.py`, `src/researchops/ml/preprocessing.py`, and `src/researchops/ml/evaluation.py`. For each file, write the Week 11 responsibility in one sentence: model training/prediction, text-to-feature preparation, or metric/reporting helpers. Then write one sentence explaining why none of these files should import `researchops.cli` or construct a database connection.

**Exercise W11-C5: Read the optional ML dependency group**

Open `pyproject.toml` and find the `[project.optional-dependencies]` section named `ml`. Copy the three package names into your notes and explain why Week 11 uses `scikit-learn` for the classifier instead of adding a new heavy dependency. Then answer: which command installs only the packages needed for this week?

**Exercise W11-C6: Read fake repositories before designing ML tests**

Open `tests/fakes/fake_repository.py` and find `FakePaperRepository.list_all`. Explain how a future topic-classification service could read paper text through the `PaperRepository` protocol without touching SQLite. Write a test idea that uses the fake repository to supply three `Paper` objects and proves the classifier receives their text in a predictable order.

## Implementation exercises

**Exercise W11-I1: Create a labeled JSONL dataset**

Create a small local training dataset in the project only if your mentor or validation flow expects it.
Use four files: `nlp.jsonl`, `systems.jsonl`, `vision.jsonl`, and `rag.jsonl`.
Each line should be JSON with a `text` field.
Write at least six realistic abstracts per label.
Do not include the label word in every example; make the language natural.

**Exercise W11-I2: Implement `load_training_data`**

Write a function with this shape:
```python
def load_training_data(data_dir: Path) -> tuple[list[str], list[str]]:
    ...
```
Requirements:
1. Read every `.jsonl` file in the directory.
2. Use the file stem as the label.
3. Parse each non-empty line as JSON.
4. Require a string field named `text`.
5. Append text and label together so ordering cannot drift.
6. Raise a clear error for an empty dataset.

**Exercise W11-I3: Build a LogisticRegression pipeline**

Write a function that returns:
```python
Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000)),
])
```
Do not fit inside the builder function.
The builder should create the object; the training workflow should fit it.

**Exercise W11-I4: Build a Naive Bayes comparison pipeline**

Create a second builder that swaps the classifier for `MultinomialNB`.
Use the same TF-IDF settings so the comparison is fair.
Write a paragraph predicting which model you expect to perform better and why.

## Testing exercises

**Exercise W11-T1: Test the data loader**

Use `tmp_path` in pytest.
Create two JSONL files with two lines each.
Assert that the function returns four texts and four labels.
Assert that labels match file stems.
Assert that text order and label order remain aligned.

**Exercise W11-T2: Test empty data failure**

Create an empty training directory.
Call `load_training_data`.
Assert that it raises the project-specific error or `ValueError` selected by the implementation.
Assert that the message mentions no training examples were found.

**Exercise W11-T3: Test pipeline steps**

Call your LogisticRegression pipeline builder.
Assert that `pipeline.named_steps` contains `tfidf`.
Assert that `pipeline.named_steps` contains `classifier`.
Assert that the classifier is a `LogisticRegression` instance.

**Exercise W11-T4: Test fit-predict plumbing**

Create a tiny deterministic dataset with at least two labels.
Fit the pipeline.
Predict on two new abstract-like strings.
Assert the number of predictions equals the number of inputs.
Assert each prediction is one of the known labels.
Do not assert a serious quality score on this tiny dataset.

## Debugging exercises

**Exercise W11-D1: Empty vocabulary**

Intentionally train with texts that are empty strings or only stop words.
Observe the vectorizer error.
Write the exact error message.
Fix the dataset by adding real abstract text.
Explain why the fix belongs in data validation, not in the classifier.

**Exercise W11-D2: Stratify failure**

Create labels where one class has only one example.
Call `train_test_split(..., stratify=labels)`.
Record the error.
Fix it by adding more examples to the small class.
Explain why deleting `stratify` is usually the wrong first fix.

**Exercise W11-D3: All predictions become one class**

Create an imbalanced dataset with many `nlp` examples and few `systems` examples.
Train the model and inspect the classification report.
Write down accuracy, macro F1, and the minority-class recall.
Explain why the model behavior is dangerous even if accuracy looks acceptable.

**Exercise W11-D4: Wrong artifact saved**

Save only `pipeline.named_steps["classifier"]` instead of the full pipeline in a scratch experiment.
Try to call `.predict(["new abstract text"])` on the loaded object.
Observe the failure or incorrect input expectations.
Fix by saving the fitted Pipeline.

## Refactoring exercises

**Exercise W11-R1: Separate building from training**

If your training function creates the pipeline, loads data, splits, fits, evaluates, and saves all inline, refactor carefully.
Extract a `build_topic_pipeline` function.
Extract a `load_training_data` function.
Keep one orchestration function that calls them in order.
Run the narrow tests after each extraction.

**Exercise W11-R2: Replace magic constants**

Find values such as `0.2`, `42`, and `1000`.
Give them descriptive names or function parameters where useful.
Do not overengineer with a complex config system yet.
The goal is readability, not abstraction for its own sake.

**Exercise W11-R3: Improve metric printing**

Refactor evaluation code so the function returns the report text or metrics dictionary instead of only printing.
The CLI may print the result.
The service or training function should be testable without capturing terminal output whenever possible.

## Written explanation exercises

Answer in complete sentences.
1. Why is TF-IDF a better first feature representation than raw text for scikit-learn classifiers?
2. Why must you split raw text before fitting `TfidfVectorizer`?
3. Explain accuracy, precision, recall, and F1 using paper-topic examples.
4. A model has 95% accuracy but 0.10 recall for `systems`. What does that mean for a researcher looking for systems papers?
5. Why is a classical baseline valuable before future neural models?
6. Why should prediction code load an existing artifact instead of training again?
7. What does `support` tell you in a classification report?
8. What question does a confusion matrix answer that accuracy does not?
9. Why is label quality often more important than classifier choice?
10. Which architecture boundary would be violated if `core/` imported `TfidfVectorizer`?

## Stretch exercises

**Exercise W11-S1: Compare LogisticRegression and MultinomialNB**

Train both models on the same split.
Print both classification reports.
Compare macro F1, weighted F1, and the weakest class for each model.
Write a short recommendation for which baseline should become the default.

**Exercise W11-S2: Inspect top LogisticRegression features**

After fitting LogisticRegression, inspect `pipeline.named_steps["classifier"].coef_`.
Use `pipeline.named_steps["tfidf"].get_feature_names_out()` to map coefficients to words.
Print the top positive terms per class.
Write whether the terms match your understanding of the topics.

**Exercise W11-S3: Try vectorizer settings**

Compare `ngram_range=(1, 1)` with `ngram_range=(1, 2)`.
Keep the classifier and split the same.
Record which labels improve or degrade.
Explain whether bigrams helped or overfit.

**Exercise W11-S4: Try `class_weight="balanced"`**

Use LogisticRegression with and without balanced class weights.
Focus on minority-class recall and macro F1.
Explain the tradeoff if accuracy decreases but minority recall improves.

## Brutal exercises

**Exercise W11-B1: Build a no-leakage audit checklist**

Create a checklist for reviewing any topic-classification training PR.
Include data split timing, vectorizer fitting, duplicate examples, label counts, saved artifact contents, and metric reporting.
Apply your checklist to your own code and record one improvement.

**Exercise W11-B2: Error analysis table**

Collect at least ten wrong predictions from a held-out set if your dataset is large enough.
For each wrong prediction, record true label, predicted label, abstract clue words, and likely cause.
Group causes into label ambiguity, weak text, data imbalance, or model limitation.
Propose one data fix and one model-setting fix.

**Exercise W11-B3: Reproducibility challenge**

Run the same training command twice with the same random seed.
Confirm that the split and metrics are stable.
Change the seed and observe whether the score changes.
Explain what this teaches about small datasets.

**Exercise W11-B4: Majority-class baseline**

Write a tiny baseline that always predicts the most common class.
Compare its accuracy and macro F1 to the TF-IDF model.
If the TF-IDF model barely beats it, explain why the dataset or labels need attention.

## Mini project task

Build a complete local topic-classification training workflow for ResearchOps.
The workflow must stay within Week 11 boundaries.
Use scikit-learn only.
Use TF-IDF plus LogisticRegression as the primary model.
Optionally compare MultinomialNB as a second baseline.

Deliverables:
1. A labeled training dataset or fixture with at least three topics.
2. A loader that returns `texts` and `labels` in aligned order.
3. A pipeline builder for LogisticRegression.
4. A training function that splits raw text before fitting.
5. A classification report printed or returned after evaluation.
6. A saved fitted Pipeline artifact.
7. A prediction path that loads the artifact and predicts a topic for new abstract text.
8. Tests for the loader, pipeline construction, and fit-predict plumbing.

Acceptance questions:
- Can you explain exactly where leakage is prevented?
- Can you explain which metric you would optimize first and why?
- Can you run prediction without retraining?
- Can you point to the architecture boundary that keeps scikit-learn out of `core/`?

## Completion checklist

- [ ] I can define document, corpus, label, feature, vectorizer, classifier, and Pipeline.
- [ ] I can explain TF-IDF without saying "it just weights words."
- [ ] I can explain why raw text must be split before vectorizer fitting.
- [ ] I can build a scikit-learn Pipeline with `TfidfVectorizer` and `LogisticRegression`.
- [ ] I can build a comparison Pipeline with `MultinomialNB`.
- [ ] I can load labeled JSONL examples into aligned text and label lists.
- [ ] I can print class counts before training.
- [ ] I can use `train_test_split` with a fixed `random_state`.
- [ ] I can explain when `stratify=labels` helps and when it fails.
- [ ] I can read a classification report class by class.
- [ ] I can explain accuracy, precision, recall, F1, and support.
- [ ] I can inspect a confusion matrix and identify confused topics.
- [ ] I can describe at least three common beginner mistakes.
- [ ] I can save and load a fitted Pipeline artifact.
- [ ] I can predict a topic for new abstract text without refitting.
- [ ] I avoided torch, transformers, sentence-transformers, embeddings, FastAPI, and async.
- [ ] I wrote or identified tests for loader behavior, pipeline construction, and prediction plumbing.
- [ ] I can explain why Week 12 needs experiment tracking.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
