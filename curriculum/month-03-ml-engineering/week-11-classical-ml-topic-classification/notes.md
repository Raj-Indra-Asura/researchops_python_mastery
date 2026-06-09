<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 11 Classical ML Topic Classification

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 11: Classical ML — Topic Classification

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Teaching the machine to label papers**.
The practical milestone is: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
The expected capability is: Can build a TF-IDF + classifier pipeline, evaluate it with classification_report, persist the model, and wire it to a CLI command. ---
This chapter is one step in the ResearchOps system, not a random lesson.
The visible feature matters because it proves the idea works.
The hidden skill matters because it lets you build the next chapter without confusion.
A complete pass through this chapter means you can read the code, run it, test it, break it, and explain it aloud.

Use this study order:
- Read the story first without typing.
- Trace the smallest code example.
- Find the project file that owns the behavior.
- Run the validation command.
- Explain one happy path and one failure path.

## What you already know from previous weeks

- Week 7 taught Keyword Search and Data Quality; keep its responsibility in mind, but do not rebuild it here.
- Week 8 taught Multiprocessing Ingestion; keep its responsibility in mind, but do not rebuild it here.
- Week 9 taught Protocols, Interfaces, and Clean Architecture; keep its responsibility in mind, but do not rebuild it here.
- Week 10 taught Testing Discipline and Quality Gates; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 11 solves the project problem behind **Classical ML — Topic Classification**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `TF-IDF vectorisation: what term frequency and inverse document frequency mean` helps solve part of this gap.
- The concept `scikit-learn `Pipeline` — chaining transformers and estimators` helps solve part of this gap.
- The concept ``LogisticRegression` as a baseline classifier` helps solve part of this gap.
- The concept ``train_test_split`, `classification_report`, precision/recall/F1` helps solve part of this gap.
- The concept ``joblib.dump` / `joblib.load` for model persistence` helps solve part of this gap.
- The concept `Exposing training and prediction through CLI` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Classical ML — Topic Classification**?
- Ask: what is the owner for **Classical ML — Topic Classification**?
- Ask: what is the transformation for **Classical ML — Topic Classification**?
- Ask: what is the proof for **Classical ML — Topic Classification**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| TF-IDF vectorisation | TF-IDF vectorisation: what term frequency and inverse document frequency mean | This term names one job in the Week 11 milestone. |
| scikit-learn `Pipeline | scikit-learn `Pipeline` — chaining transformers and estimators | This term names one job in the Week 11 milestone. |
| LogisticRegression` as a baseline classifier | `LogisticRegression` as a baseline classifier | This term names one job in the Week 11 milestone. |
| train_test_split`, `classification_report`, precision/recall/F1 | `train_test_split`, `classification_report`, precision/recall/F1 | This term names one job in the Week 11 milestone. |
| joblib.dump` / `joblib.load` for model persistence | `joblib.dump` / `joblib.load` for model persistence | This term names one job in the Week 11 milestone. |
| Exposing training and prediction through CLI | Exposing training and prediction through CLI | This term names one job in the Week 11 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: TF-IDF vectorisation: what term frequency and inverse document frequency mean
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 11, it supports the milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: scikit-learn `Pipeline` — chaining transformers and estimators
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 11, it supports the milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: `LogisticRegression` as a baseline classifier
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 11, it supports the milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: `train_test_split`, `classification_report`, precision/recall/F1
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 11, it supports the milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: `joblib.dump` / `joblib.load` for model persistence
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 11, it supports the milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: Exposing training and prediction through CLI
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 11, it supports the milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/ml/preprocessing.py` — TF-IDF pipeline
- `src/researchops/ml/topic_classifier.py` — training and prediction
- `src/researchops/ml/evaluation.py` — metrics reporting
- `src/researchops/cli/commands/papers.py` — `classify`, `train-topic-model` commands
Study those files in this order:
1. Find the user-facing entry point.
2. Find the service or core concept that owns the meaning.
3. Find the infrastructure only when outside resources are needed.
4. Find the tests that prove the behavior.
5. Find the validation command that a learner runs manually.
The goal is to know why each file exists.
If two files seem to own the same decision, stop and clarify the boundary.

## Code examples with line-by-line explanation

```python
from sklearn.pipeline import Pipeline

model = Pipeline([
    ("vectorizer", TfidfVectorizer()),
    ("classifier", LogisticRegression()),
])
model.fit(training_texts, labels)
```

Line-by-line explanation:
- Line 1: `from sklearn.pipeline import Pipeline` — This imports a tool before the example can use it.
- Line 2: `(blank line)` — This blank line separates ideas so the example is easier to read.
- Line 3: `model = Pipeline([` — This stores a clear intermediate value for the next step.
- Line 4: `("vectorizer", TfidfVectorizer()),` — This performs one small visible step in the workflow.
- Line 5: `("classifier", LogisticRegression()),` — This performs one small visible step in the workflow.
- Line 6: `])` — This performs one small visible step in the workflow.
- Line 7: `model.fit(training_texts, labels)` — This performs one small visible step in the workflow.

How to use this example:
- Name the input.
- Name the output.
- Predict the result before running anything.
- Connect the shape to the real ResearchOps file.
- Write one sentence about why each line belongs.

## Common beginner mistakes

- **Mistake:** Pasting code before knowing the owner of the behavior.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Changing many files at once.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Skipping the failure path.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Reading only the happy path test.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Ignoring the validation command.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Using vague names.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Putting business rules in the user interface layer.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Treating logs, errors, and tests as decoration.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Optimizing before correctness is visible.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Building future-week features early.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.

## Debugging guidance

- Copy the exact failing command.
- Read the first useful error line.
- Read the final error line.
- Classify the failure as import, input, state, file, database, network, model, or expectation.
- Reproduce it with the smallest command.
- Inspect the value closest to the failure.
- Fix the cause, not only the symptom.
- Run the narrowest test.
- Run the chapter validation command.
- Write down what the error was teaching.
Debugging questions:
- What did I expect?
- What happened?
- Which value first became wrong?
- Which layer created that value?
- Which test should catch this next time?

## Design tradeoffs

- **Simple first version:** Easy to understand, but not the final production shape.
- **Clear layers:** More files, but less confusion as features grow.
- **Explicit errors:** More code, but failures become teachable.
- **Small unit tests:** Fast feedback, but less end-to-end confidence.
- **Integration tests:** Real wiring, but slower and more setup.
- **Configuration:** Flexible behavior, but defaults must be clear.
The right question is not "What is the fanciest design?"
The right question is "What design teaches the responsibility clearly and can grow next week?"

## Testing implications

Tests for this chapter:
- `tests/unit/test_topic_classifier.py` — train, predict, evaluate with small fixture data
Validation commands:
```bash
researchops train-topic-model
researchops classify PAPER_ID
pytest tests/unit/test_topic_classifier.py -v
```
- Arrange the data.
- Act on the system.
- Assert the visible promise.
- Check one failure path.
- Keep unit tests fast.
- Use integration tests only when real wiring matters.

## Architecture implications

ResearchOps stays understandable when dependencies point inward.
```text
CLI / API / Worker -> Services -> Core
Infrastructure implements core-facing contracts and is wired at the outside.
```
- Does the UI layer avoid business logic?
- Does the service layer own workflow decisions?
- Does core avoid infrastructure imports?
- Does infrastructure do outside-world work?
- Do tests use fakes when possible?
Architecture is not ceremony.
Architecture is named responsibility.

## How this connects to AI engineering / ML research

AI engineering needs more than models.
It needs reliable data flow, clear interfaces, repeatable experiments, visible failures, and honest evaluation.
Week 11 contributes by making **classical ml — topic classification** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 11 solve?
- What is the main input?
- What is the main output?
- Which file owns the main responsibility?
- Which layer should not contain business logic?
- What is one happy path?
- What is one failure path?
- What command proves the chapter works?
- What should you not build early?
- How does this prepare the next week?

## Explain-it-aloud prompts

- Explain Classical ML — Topic Classification in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Classical ML — Topic Classification.
- The milestone: `researchops train-topic-model` trains and saves a classifier. `researchops classify PAPER_ID` returns the predicted topic.
- The main project files.
- The validation command.
- The boundary rule for the layer you are touching.
- The habit of testing before moving forward.

## What to understand deeply

- Why this feature belongs now.
- How data moves through the chapter.
- Which file owns which decision.
- How the failure path is handled.
- Why the tests prove behavior.
- How this week makes future work safer.

## What not to worry about yet

- Perfect scale.
- Fancy abstractions.
- Future-week features.
- Every option in every library.
- Premature optimization.
- Comparing your speed to someone else.
Focus on the milestone.
A clear small milestone beats a confusing large one.

## Bridge to next week

Next week is Week 12: **Experiment Tracking**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops experiment list` shows all training runs with params and metrics. `researchops experiment compare` shows which run had the best F1.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes

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
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
