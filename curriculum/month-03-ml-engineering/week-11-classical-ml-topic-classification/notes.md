<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 11 Classical ML Topic Classification

This is one unified beginner chapter. There is no short version followed by a second older version.
The goal is to teach classical machine learning for paper-topic classification from first principles.
You will use scikit-learn only: TF-IDF, train/test split, LogisticRegression, MultinomialNB, and evaluation metrics.
Do not use embeddings, transformers, torch, sentence-transformers, FastAPI, or async in this chapter.

## Chapter overview

Week 11 is the point where ResearchOps first learns from labeled examples instead of only following hand-written rules.
Before this week, the system could store papers, search text, run quality checks, and keep architecture boundaries clear.
Those skills matter because machine learning is not magic sitting apart from the application.
A model is only useful when the surrounding project can provide clean inputs and trustworthy evaluation.
This chapter builds a topic classifier for research-paper abstracts.
The input is a short piece of paper text, usually an abstract or title plus abstract.
The output is a topic label such as `nlp`, `systems`, `vision`, or `rag`.
The model is classical machine learning, not deep learning.
Classical means the features are designed by a known algorithm and the classifier is relatively small and fast.
Here the feature algorithm is TF-IDF.
TF-IDF converts text into numbers by asking which words are frequent in one document but not common everywhere.
The classifier is either LogisticRegression or MultinomialNB from scikit-learn.
LogisticRegression is a strong linear baseline for text classification.
MultinomialNB is a simple probabilistic baseline that often works surprisingly well for word-count-like features.
The chapter milestone is not merely to call `.fit()` once.
The milestone is to understand the full learning loop: prepare labeled examples, split data, train, predict, evaluate, inspect mistakes, and save a usable artifact.
A beginner should finish this chapter able to explain why the model saw the training set but not the test set during learning.
A beginner should also explain why accuracy alone can hide failure on smaller classes.
The ResearchOps story is concrete: papers arrive with abstracts, humans or fixtures provide labels, and the model learns patterns that map abstracts to topics.
The chapter avoids future-week material on embeddings and neural models.
That boundary is intentional because TF-IDF plus a linear classifier is easier to debug and often good enough for a first production baseline.
Think of this week as building the honest baseline that future AI work must beat.
If a later embedding model cannot beat this baseline under the same evaluation rules, the simpler model deserves respect.
The main command shape is training first and prediction second.
Training consumes labeled examples and creates a fitted pipeline.
Prediction loads the fitted pipeline and applies it to new paper text.
Evaluation reports how well the model did on held-out examples.
Every part of that loop has a failure mode.
Bad labels teach the wrong lesson.
A leaky split gives fake confidence.
A missing class in the test set makes metrics misleading.
A saved classifier without its vectorizer cannot understand new raw text.
This is why scikit-learn Pipeline is central to the chapter.
A Pipeline keeps vectorization and classification together so the same transformations are used during training and inference.

## What you already know from previous weeks

Week 1 gave ResearchOps a project shape and a small CLI surface.
That matters because ML code should not live as a random script forever.
Week 2 focused on paths, files, exceptions, and logging.
That matters because training data is usually stored in files and bad file paths are one of the first beginner problems.
Week 3 introduced stronger domain modeling with dataclasses and explicit objects.
That matters because a paper is not just a dictionary; it has fields with meaning.
Week 4 made the command-line interface more real.
That matters because a training run should be repeatable from a command, not only from a notebook cell.
Week 5 introduced SQLite storage.
That matters because labeled paper records may come from persistent storage instead of a hand-written list.
Week 6 and Week 7 strengthened parsing, search, and data quality ideas.
That matters because a classifier trained on messy abstracts will learn messy shortcuts.
Week 8 introduced multiprocessing ingestion.
That matters as background context, but this week does not add CPU-heavy parallel training logic.
Week 9 introduced protocols and clean architecture boundaries.
That matters because services should depend on interfaces, not directly on a specific ML implementation.
Week 10 introduced testing discipline and quality gates.
That matters because a model can appear to work while tests reveal data leakage or brittle assumptions.
You already know how to read a function signature and ask what type comes in and what type comes out.
Apply that habit to ML functions.
`fit(texts, labels)` is not just an incantation; it consumes examples and stores learned state.
`predict(texts)` is not just a guess; it applies stored state to new inputs.
You already know that user interfaces should delegate business decisions.
Apply that habit to training commands.
The CLI may parse options, but the training service should own loading data, fitting the pipeline, and returning metrics.
You already know that tests should be narrow.
Apply that habit to model code by testing data loading, split behavior, and prediction shape separately.
You already know that validation commands should be exact.
Apply that habit to model evaluation by recording commands, data paths, and expected metric format.
This week builds on all of that, but it still starts from beginner ML vocabulary.

## What problem this week solves

ResearchOps has many papers, but raw storage does not answer every question.
A researcher may ask, "Which of these papers are probably about NLP?"
Keyword search can help when the obvious words are present.
Keyword search struggles when the vocabulary changes.
For example, an NLP paper might mention `sequence-to-sequence`, `attention`, `translation`, or `language model` without using the label `nlp`.
A systems paper might mention `replication`, `consensus`, `latency`, or `fault tolerance` without using the word `systems`.
Topic classification solves this by learning from examples.
Instead of writing every possible keyword rule by hand, you provide abstracts with known labels.
The classifier learns statistical associations between words and labels.
The problem is supervised learning because the examples include target labels.
The problem is classification because the target is a category, not a number on a continuous scale.
The problem is multiclass when there are more than two topics.
The chapter also solves a project maturity problem.
It teaches how to evaluate a model before trusting it.
A model that sounds smart but has no held-out evaluation is not evidence.
A model evaluated on the same examples it trained on is also not evidence.
The honest question is: how well does the model perform on examples it did not learn from?
That is why `train_test_split` appears early.
The chapter uses `stratify=labels` when possible so each split keeps roughly the same class proportions.
The chapter solves another problem: how to avoid losing preprocessing at inference time.
If you train a vectorizer separately and save only the classifier, prediction later will fail or use the wrong vocabulary.
A scikit-learn Pipeline solves that by saving the vectorizer and classifier as one fitted object.
The final practical problem is communication.
The learner must be able to explain metrics to a teammate.
Accuracy answers, "How often was the model right overall?"
Precision answers, "When it predicted this topic, how often was that prediction correct?"
Recall answers, "Of the real papers in this topic, how many did it find?"
F1 combines precision and recall when you need one balanced number.
This week turns topic labeling from guessing into a measured, repeatable workflow.

## Beginner mental model

Use the classroom analogy first.
Imagine teaching a student to sort research abstracts into folders.
You hand the student many examples where the correct folder is already written on each paper.
The student notices that `attention`, `translation`, and `token` often appear in the NLP folder.
The student notices that `latency`, `replication`, and `consensus` often appear in the systems folder.
The student notices that `image`, `segmentation`, and `convolution` often appear in the vision folder.
After practice, you hide the answers on new papers and ask the student to choose folders.
That is supervised classification.
Now replace the student with a model.
The model cannot read meaning like a human beginner can.
The model needs numbers.
TF-IDF is the translator from words to numbers.
The classifier is the decision-maker that learns how number patterns connect to labels.
The training set is the practice pile with answers visible.
The test set is the quiz pile with answers hidden until grading.
Fitting means learning from the practice pile.
Predicting means choosing labels for the quiz pile or for new user input.
Evaluating means comparing predictions to correct labels.
The most important beginner rule is this: the model must not study the quiz before taking it.
If test examples influence TF-IDF vocabulary or classifier weights, your score is contaminated.
That contamination is called leakage.
A Pipeline helps because it fits transformations only on the training data during `.fit()`.
When you call `.predict()` on test text, it uses the training vocabulary instead of learning a new one.
A second mental model is the recipe card.
Raw abstracts are ingredients.
TF-IDF is the chopping and measuring step.
LogisticRegression or Naive Bayes is the cooking step.
The fitted Pipeline is the complete recipe plus learned measurements.
Saving the Pipeline preserves the recipe so the CLI can use it later.

## Core vocabulary

| Term | Beginner meaning | ResearchOps meaning |
|---|---|---|
| Document | One piece of text | One abstract or title-plus-abstract |
| Corpus | A collection of documents | All labeled training abstracts |
| Label | The answer category | `nlp`, `systems`, `vision`, `rag`, or another topic |
| Example | One input with one label | One abstract paired with its topic |
| Feature | A number the model can use | A TF-IDF value for a term |
| Vector | A list of feature numbers | One abstract represented numerically |
| Vocabulary | Known terms from training | Words TF-IDF learned from training text |
| TF | Term frequency | How much a word appears in one abstract |
| IDF | Inverse document frequency | How rare a word is across abstracts |
| TF-IDF | TF multiplied by IDF | High for words important to one abstract but not common everywhere |
| Vectorizer | Tool that converts text to features | `TfidfVectorizer` |
| Classifier | Tool that predicts a category | `LogisticRegression` or `MultinomialNB` |
| Estimator | scikit-learn object with `.fit()` | The pipeline and its classifier step |
| Transformer | scikit-learn object that changes data | The TF-IDF vectorizer |
| Pipeline | Ordered chain of steps | Vectorizer followed by classifier |
| Training set | Examples used to learn | Abstracts the model studies |
| Test set | Examples held back for grading | Abstracts used for honest evaluation |
| Accuracy | Overall fraction correct | Useful but incomplete metric |
| Precision | Correctness of positive predictions | Trustworthiness when model says a topic |
| Recall | Coverage of real examples | Ability to find all papers in a topic |
| F1 | Balance of precision and recall | Helpful when classes are uneven |
| Confusion matrix | Table of true vs predicted labels | Shows which topics are mixed up |
| Baseline | Simple first serious model | TF-IDF plus LogisticRegression or Naive Bayes |
| Overfitting | Memorizing training examples | High train score but poor test score |
| Leakage | Test information enters training | Metrics look better than reality |
| Artifact | Saved trained object | A fitted pipeline file loaded for prediction |

## Concept explanations from first principles

Start with the smallest possible dataset.
Suppose there are three abstracts.
`attention model translation` has label `nlp`.
`replication consensus latency` has label `systems`.
`image segmentation convolution` has label `vision`.
Python strings are not enough for most scikit-learn classifiers.
The classifier expects rows of numbers.
Each row represents one document.
Each column represents one feature.
With text, a feature is often connected to a word or token.
A basic count vectorizer could count how many times each word appears.
TF-IDF improves on raw counts by reducing the influence of words that appear everywhere.
The term `model` can mean the whole fitted pipeline or only the classifier step.
Be precise when debugging.
If TF-IDF fails, the classifier never receives useful numbers.
If the classifier fails, the vectorizer may still be working.
The scikit-learn method `.fit()` means "learn internal state from data."
For `TfidfVectorizer`, fitting learns the vocabulary and IDF weights.
For `LogisticRegression`, fitting learns coefficients for each class.
For `MultinomialNB`, fitting learns word evidence probabilities for each class.
The method `.transform()` means "convert input using already learned state."
The method `.predict()` means "return labels using learned state."
A Pipeline combines these operations.
During `pipeline.fit(X_train, y_train)`, the vectorizer fits and transforms the training text, then the classifier fits on the resulting numbers.
During `pipeline.predict(X_test)`, the vectorizer only transforms, then the classifier predicts.
That difference protects the evaluation from accidental learning on the test set.
LogisticRegression is called regression for historical reasons, but in this setting it performs classification.
It learns a score for each class and chooses the strongest score.
Naive Bayes is called naive because it uses a simplifying independence assumption about features.
The assumption is not fully true for language, but the method can still work well.
The first-principles lesson is simple: text becomes numbers, numbers feed a classifier, predictions are compared to labels.
Everything else in this chapter makes that loop safer and more honest.

## ResearchOps-specific application

In ResearchOps, topic classification is not a standalone demo.
It helps users triage papers by research area.
A paper record may contain a title, abstract, authors, year, and storage identifier.
The classifier should focus on textual content such as title and abstract.
Do not train on database IDs, filenames, or paths because those are accidental metadata.
Accidental metadata can create fake performance.
For example, if all NLP sample files happen to have names containing `nlp`, a model using filenames would cheat.
A clean training example should look like text plus label.
The label may come from a JSONL filename, a CSV column, or a database field depending on the project stage.
For this week, file-based labeled examples are easiest for beginners to inspect.
Each JSONL line can hold one object with a `text` field.
The filename can provide the label: `nlp.jsonl`, `systems.jsonl`, and so on.
This format is not fancy, but it is transparent.
Transparency is valuable when learning ML.
A learner can open the file and immediately see what the model is studying.
A training command should print class counts before fitting.
Class counts reveal imbalance early.
If `nlp` has 100 examples and `systems` has 5, accuracy can become misleading.
A training command should print train and test sizes.
Sizes reveal whether the split is plausible.
A training command should print a classification report.
The report communicates precision, recall, F1, and support for each label.
Support means how many true examples of that class were evaluated.
A prediction command should load the saved artifact and accept raw paper text.
It should not refit the model during prediction.
Refitting during prediction would erase the meaning of evaluation.
The ResearchOps boundary remains: CLI wires the command, service code owns the training workflow, core protocols describe contracts, and infrastructure implements details.
Do not move ML decisions into FastAPI in this week.
Do not add async work for this week.
Do not replace TF-IDF with neural embeddings yet.

## Code examples with line-by-line explanation

First, examine a minimal dataset.
```python
texts = [
    "attention transformer translation",
    "consensus replication latency",
    "image segmentation convolution",
]
labels = ["nlp", "systems", "vision"]
```
Line 1 creates the variable `texts`.
Line 2 opens a list that will hold raw document strings.
Line 3 is one abstract-like text for NLP.
Line 4 is one abstract-like text for systems.
Line 5 is one abstract-like text for vision.
Line 6 closes the list.
Line 7 creates labels in the same order as the texts.
The order matters because `texts[0]` belongs with `labels[0]`.

Now build the classical ML pipeline.
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000)),
])
pipeline.fit(texts, labels)
```
Line 1 imports the TF-IDF vectorizer from scikit-learn.
Line 2 imports LogisticRegression, the baseline classifier.
Line 3 imports Pipeline, the object that keeps steps together.
Line 4 is blank for readability.
Line 5 creates a Pipeline object.
Line 6 adds a step named `tfidf`.
`lowercase=True` makes `Attention` and `attention` match.
`ngram_range=(1, 2)` lets the model consider single words and two-word phrases.
Line 7 adds a classifier step named `classifier`.
`max_iter=1000` gives the optimizer enough attempts to converge on small text datasets.
Line 8 closes the Pipeline list.
Line 9 fits the complete pipeline on raw text and labels.
The vectorizer learns vocabulary first.
The classifier learns label patterns second.

Now split data before fitting.
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
Line 1 imports the splitting helper.
Line 2 is blank for readability.
Line 3 starts assignment to four variables.
`X_train` is training text.
`X_test` is held-out test text.
`y_train` is training labels.
`y_test` is held-out true labels.
Line 4 passes the texts.
Line 5 passes the labels in matching order.
Line 6 asks for 20 percent test data.
Line 7 makes the split repeatable.
Line 8 asks scikit-learn to preserve class proportions.
Line 9 closes the call.
If a class has too few examples, stratification can fail.
That failure teaches you to collect more examples or adjust the split for tiny practice data.

Now evaluate predictions.
```python
from sklearn.metrics import classification_report, confusion_matrix

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
print(classification_report(y_test, predictions, zero_division=0))
print(confusion_matrix(y_test, predictions, labels=pipeline.classes_))
```
Line 1 imports metric helpers.
Line 2 is blank for readability.
Line 3 trains only on training examples.
Line 4 predicts labels for test examples.
Line 5 prints precision, recall, F1, and support.
`zero_division=0` avoids a warning becoming confusing when a class receives no predictions.
Line 6 prints a table showing which labels were confused.
`pipeline.classes_` provides the learned class order.

Now try Naive Bayes as a comparison.
```python
from sklearn.naive_bayes import MultinomialNB

nb_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB()),
])
```
Line 1 imports the Naive Bayes classifier appropriate for non-negative text features.
Line 2 is blank for readability.
Line 3 creates a second Pipeline.
Line 4 uses the same TF-IDF transformation.
Line 5 swaps the classifier.
Line 6 closes the Pipeline.
Changing one step while keeping the evaluation the same is how you make a fair comparison.

## Common beginner mistakes

Mistake 1: fitting TF-IDF before the train/test split.
Why it hurts: the vocabulary and IDF weights have seen the test set.
Better move: split raw text first, then fit the Pipeline on `X_train` only.
Mistake 2: evaluating on the training set.
Why it hurts: the model may look excellent because it is being graded on examples it studied.
Better move: always keep a held-out test set for the first honest check.
Mistake 3: trusting accuracy alone.
Why it hurts: a majority-class model can be accurate while failing minority topics.
Better move: read per-class precision, recall, F1, and support.
Mistake 4: saving only the classifier.
Why it hurts: the classifier expects numeric features, not raw strings.
Better move: save the fitted Pipeline containing both vectorizer and classifier.
Mistake 5: mixing labels and texts out of order.
Why it hurts: the model learns wrong associations.
Better move: append text and label together in the same loop.
Mistake 6: using tiny datasets and believing the metric.
Why it hurts: one lucky split can dominate the score.
Better move: treat tiny-data metrics as smoke tests, not proof.
Mistake 7: adding future-week neural tooling too early.
Why it hurts: it hides basic evaluation problems behind heavy dependencies.
Better move: make TF-IDF baselines strong first.
Mistake 8: ignoring mislabeled examples.
Why it hurts: the model learns from your labels even when they are wrong.
Better move: inspect errors and correct training data when labels are inconsistent.
Mistake 9: training on duplicated abstracts across train and test.
Why it hurts: duplicates make the test set easier than reality.
Better move: deduplicate or group related records before splitting.
Mistake 10: changing the data and comparing scores as if nothing changed.
Why it hurts: you cannot know whether the model or dataset caused the metric change.
Better move: record dataset version, command, parameters, and random seed.

## Debugging guidance

When training fails, identify which stage failed.
Stage 1 is loading labeled examples.
Stage 2 is splitting examples.
Stage 3 is vectorizing text.
Stage 4 is fitting the classifier.
Stage 5 is predicting.
Stage 6 is calculating metrics.
Stage 7 is saving or loading the artifact.
If loading fails, print the data directory and list the files you expected.
If JSON parsing fails, inspect the exact line number and content.
If labels are empty, check filename parsing or label column parsing.
If `train_test_split` fails with stratification, count examples per class.
A common error says the least populated class has too few members.
That means at least one class cannot be split into train and test safely.
If vectorization fails with empty vocabulary, inspect your text cleaning.
You may have removed every token or supplied empty strings.
If LogisticRegression does not converge, increase `max_iter` and check data size.
If every prediction is one class, inspect class counts and confusion matrix.
If `classification_report` shows zeros, the model may not predict some classes.
That is not a formatting problem; it is signal about model behavior or data imbalance.
If loaded prediction fails, confirm you saved the fitted Pipeline, not an unfitted object.
If a new abstract predicts a strange topic, print the top terms for that label when using LogisticRegression.
For debugging, prefer tiny reproducible datasets over large mysterious ones.
A five-example-per-class dataset can test plumbing.
A larger realistic dataset is needed to trust performance.
Always copy the exact failing command into your notes or issue.
Always record the random seed when discussing a surprising metric.
Run the narrowest check first: data loader tests before full training tests.
Do not fix a metric by hiding warnings.
Warnings often reveal classes with no predicted examples or insufficient data.

## Design tradeoffs

TF-IDF is simple, fast, and transparent.
Its weakness is that it does not truly understand meaning.
It treats words and short phrases as signals.
For Week 11, that weakness is acceptable because the goal is an honest baseline.
LogisticRegression is often strong for sparse text features.
It can produce coefficients that help inspect influential words.
Its weakness is that it assumes a linear decision boundary in feature space.
MultinomialNB is very fast and simple.
It can work well when word evidence is strong.
Its weakness is the naive independence assumption.
A Pipeline adds structure and reduces leakage risk.
Its weakness is that beginners may forget how to inspect individual steps.
That is why step names like `tfidf` and `classifier` matter.
A random train/test split is easy.
Its weakness is that small datasets can produce unstable metrics.
A stratified split is usually better for classification.
Its weakness is that it requires enough examples per class.
Accuracy is easy to explain.
Its weakness is class imbalance.
F1 is better for balancing precision and recall.
Its weakness is that one number can still hide which class failed.
Printing metrics to the terminal is beginner-friendly.
Its weakness is poor experiment history.
Week 12 will improve this with tracking.
Saving a model artifact enables reuse.
Its weakness is that artifacts can become stale when training data changes.
The tradeoff theme is repeatability over cleverness.
A boring baseline that anyone can run is more valuable than a fancy model no one can reproduce.

## Testing implications

ML testing has two layers: software correctness and model quality.
Software correctness asks whether functions behave as promised.
Model quality asks whether predictions are useful enough for the product goal.
Unit tests should not depend on a large real dataset.
A unit test for `load_training_data` can create tiny files with `tmp_path` and verify returned texts and labels.
A unit test for pipeline construction can assert the step names are `tfidf` and `classifier`.
A unit test can fit on a tiny dataset only to prove the plumbing runs.
Do not treat that tiny fit score as scientific evidence.
Integration tests may write a small artifact to a temporary path and load it back.
The loaded object should predict one of the known labels for new text.
Tests should catch missing labels.
Tests should catch malformed JSONL lines if the loader promises clear errors.
Tests should catch empty datasets.
Tests should catch classes with too few examples when stratified splitting is required.
Tests should catch accidental future dependencies.
For this week, a test should not import torch or transformer libraries.
A deterministic random seed makes tests stable.
Use `random_state=42` or a named constant.
Avoid tests that assert exact F1 scores on very tiny data unless the dataset is carefully controlled.
Prefer assertions about shape, labels, artifact existence, and clear error messages.
When testing metrics formatting, assert that expected label names appear in the report.
When testing prediction, assert the output type is a string or list of strings as designed.
Testing cannot prove the model is universally correct.
Testing can prove the training workflow is honest, repeatable, and guarded against obvious mistakes.

## Architecture implications

The ResearchOps architecture still matters when adding ML.
`core/` should not import scikit-learn.
Core contains models, exceptions, interfaces, and value objects.
A protocol may describe a topic classifier behavior without naming LogisticRegression.
For example, an interface can say that a classifier predicts a topic for text.
The infrastructure implementation can use scikit-learn.
`services/` should depend on protocols rather than concrete files.
A service can coordinate classification without knowing whether the implementation is LogisticRegression or Naive Bayes.
`cli/` should parse command options and call services.
The CLI should not contain the training algorithm.
`storage/` can load paper records from SQLite when the project reaches that workflow.
`ml/` can contain scikit-learn-specific pipeline construction, training, evaluation, and artifact loading.
Do not place FastAPI code in this week.
Do not add async code to wrap scikit-learn fitting.
Fitting a classical model is CPU work and should not be hidden in an event loop.
For this week, a synchronous command is simpler and correct.
The saved artifact is infrastructure detail.
A service can ask a repository or classifier provider for what it needs.
The architecture boundary protects future changes.
If Week 13 introduces embeddings, you should not need to rewrite the entire CLI.
You should be able to swap a classifier implementation behind the same higher-level behavior.
Avoid importing training scripts from random notebooks.
Training code belongs in importable modules so tests can call it directly.
Good architecture makes ML boring to operate.
Boring is a compliment in production systems.

## How this connects to AI engineering / ML research

Modern AI engineering still needs classical baselines.
A neural model may be powerful, but it is also heavier, slower, and harder to debug.
TF-IDF plus LogisticRegression can train quickly on a laptop.
It can also reveal whether labels are useful before expensive modeling begins.
In ML research, baselines keep claims honest.
A paper that proposes a complex method should compare against simpler methods.
ResearchOps follows the same discipline.
Before using embeddings, retrieval-augmented generation, or transformer classifiers, build the simple baseline.
If the baseline solves the user need, the project may not need heavier tooling yet.
If the baseline fails, its errors teach what a future model must handle.
For example, TF-IDF may confuse `rag` and `nlp` because both mention language models.
That confusion can motivate better data, clearer labels, or later semantic representations.
Evaluation metrics are part of AI engineering culture.
Without precision and recall, model discussions become vague.
With metrics, teammates can decide whether false positives or false negatives hurt more.
In a research-paper triage tool, false positives may waste reviewer time.
False negatives may hide relevant papers from a researcher.
The right metric depends on product cost.
This is why ML engineering is not just coding.
It is data, evaluation, tradeoffs, communication, and software design working together.
Week 11 gives you the language to participate in those decisions.

## Mini quizzes

Quiz 1: What is the difference between a document and a corpus?
Quiz 2: Why does a classifier need text converted into numbers?
Quiz 3: What does TF measure?
Quiz 4: What does IDF reduce the importance of?
Quiz 5: Why is a Pipeline safer than fitting a vectorizer separately before splitting?
Quiz 6: What does `pipeline.fit(X_train, y_train)` learn?
Quiz 7: What does `pipeline.predict(X_test)` avoid learning?
Quiz 8: Why should raw test text not influence vocabulary fitting?
Quiz 9: What does LogisticRegression output in a classification pipeline?
Quiz 10: Why can MultinomialNB work well for text?
Quiz 11: What does `test_size=0.2` mean?
Quiz 12: Why use `random_state`?
Quiz 13: What does `stratify=labels` try to preserve?
Quiz 14: What does accuracy measure?
Quiz 15: What does precision measure?
Quiz 16: What does recall measure?
Quiz 17: Why is F1 useful?
Quiz 18: What does support mean in `classification_report`?
Quiz 19: What can a confusion matrix show that accuracy hides?
Quiz 20: Why should you save the fitted Pipeline instead of only the classifier?
Quiz 21: What is leakage?
Quiz 22: What is overfitting?
Quiz 23: Why can duplicated abstracts inflate test results?
Quiz 24: Why should this week avoid torch and transformer libraries?
Quiz 25: What future week will improve metric history and experiment comparison?

## Explain-it-aloud prompts

Explain how a paper abstract becomes a row of numbers.
Explain why common words should usually receive less weight.
Explain why `attention` might be useful for NLP but not always sufficient.
Explain why the model must not train on the test set.
Explain the difference between fitting and transforming.
Explain what each Pipeline step owns.
Explain why LogisticRegression is a reasonable baseline.
Explain why Naive Bayes is called naive but still useful.
Explain how you would load JSONL training files by label.
Explain how you would detect class imbalance before training.
Explain why a classifier predicting only `nlp` can still have high accuracy.
Explain precision using a false-positive example.
Explain recall using a missed-paper example.
Explain F1 without saying it is magic.
Explain a confusion matrix row.
Explain a confusion matrix column.
Explain why saving a model artifact matters.
Explain why refitting during prediction is wrong.
Explain how a CLI should delegate to service code.
Explain which parts of this chapter belong in `ml/` rather than `core/`.
Explain what a future embeddings model would need to beat.
Explain one failure path from bad data to bad metrics.
Explain one debugging move for an empty vocabulary error.
Explain one debugging move for a class with zero recall.

## What to memorize

Memorize that TF-IDF stands for term frequency-inverse document frequency.
Memorize that TF measures how much a term appears in one document.
Memorize that IDF gives less weight to terms common across many documents.
Memorize that raw text must be converted into numeric features before classical classifiers can use it.
Memorize that `TfidfVectorizer` is the scikit-learn tool used here for text features.
Memorize that `Pipeline` keeps preprocessing and modeling together.
Memorize the safe order: split raw data, fit Pipeline on train, predict on test, evaluate.
Memorize that `train_test_split` creates held-out evaluation data.
Memorize that `random_state` makes the split repeatable.
Memorize that `stratify` helps preserve label proportions.
Memorize that LogisticRegression is the primary baseline classifier in this chapter.
Memorize that MultinomialNB is the comparison baseline.
Memorize that accuracy is overall correctness.
Memorize that precision asks whether predicted positives were correct.
Memorize that recall asks whether actual positives were found.
Memorize that F1 balances precision and recall.
Memorize that support is the number of true examples per class.
Memorize that leakage means test information influenced training.
Memorize that an artifact should contain the fitted Pipeline.
Memorize that this week does not use embeddings, torch, transformers, FastAPI, or async.

## What to understand deeply

Understand why the train/test split is a trust boundary.
The split is not just a convenience function.
It separates learning from grading.
When that boundary is broken, the metric stops meaning what you think it means.
Understand why TF-IDF is useful for topic classification.
It captures words that are locally important and globally distinctive.
That is often enough to separate research areas with different vocabulary.
Understand why TF-IDF is limited.
It does not know that two different phrases can mean similar things unless the words overlap.
Understand why simple baselines matter.
They establish a measurement floor for future models.
Understand why class imbalance changes metric interpretation.
A model can be mostly right overall while useless for a rare class.
Understand why precision and recall answer different product questions.
High precision means predictions are trustworthy when made.
High recall means the model finds most true examples.
Understand why Pipeline reduces operational mistakes.
The same object used during training can be saved and used during prediction.
Understand why label quality may matter more than model choice.
A classifier trained on inconsistent labels learns inconsistency.
Understand why architecture boundaries still matter in ML code.
Without boundaries, training scripts become impossible to test and reuse.
Understand why this chapter is synchronous and local.
The learner needs transparent mechanics before distributed services or web APIs.

## What not to worry about yet

Do not worry about neural embeddings yet.
Embeddings begin later, after classical baselines and evaluation discipline are in place.
Do not worry about torch.
This week uses scikit-learn only.
Do not worry about transformers.
Transformer models are intentionally outside the Week 11 boundary.
Do not worry about sentence-transformers.
Semantic vector search belongs to a later chapter.
Do not worry about RAG generation.
This week predicts topics; it does not generate answers.
Do not worry about FastAPI endpoints.
The CLI and service workflow should work before an API exists.
Do not worry about async code.
There is no network I/O lesson here.
Do not worry about perfect model performance.
A beginner baseline is allowed to be imperfect as long as evaluation is honest.
Do not worry about hyperparameter search grids yet.
Manual comparison of LogisticRegression and Naive Bayes is enough for this chapter.
Do not worry about production monitoring yet.
First learn how to create and evaluate a local artifact.
Do not worry about advanced calibration, ROC curves, or threshold tuning yet.
Those topics are useful later but can distract from the core loop.
Do not worry about large-scale training performance yet.
Small and clear is the correct learning target now.

## Bridge to next week

At the end of Week 11, you can train a topic classifier and print metrics.
That is a real milestone, but it leaves an important weakness.
The terminal output disappears unless you copy it somewhere.
If you change `ngram_range`, `min_df`, classifier type, or training data, you need a way to compare runs.
Week 12 addresses that weakness with experiment tracking.
Experiment tracking records parameters, metrics, dataset notes, and artifact paths.
It answers questions like, "Which run produced the best macro F1?"
It also answers, "Did the Naive Bayes model improve recall for systems papers?"
The bridge from Week 11 to Week 12 is the idea that model training is not a one-time event.
Training is an experiment that should leave evidence.
Week 11 teaches how to produce the evidence.
Week 12 teaches how to store and compare it.
Carry forward the same discipline.
Keep data loading explicit.
Keep splits repeatable.
Keep evaluation honest.
Keep artifacts connected to the configuration that produced them.
Do not skip the baseline once future models arrive.
The Week 11 classifier remains the reference point.
Future improvements must beat it under fair evaluation.
If they cannot, the simple model wins.

## Unified practice walkthrough: fitting on paper abstracts

This walkthrough stays inside the same chapter and expands the required sections with concrete practice.
Imagine you have twelve labeled abstracts.
Four are NLP, four are systems, and four are vision.
This is still too small for real performance claims, but it is enough to learn the mechanics.
The text should look like paper language, not random keywords only.
For example: `We introduce an attention-based encoder for document summarization.`
A systems example might say: `We evaluate a replication protocol for low-latency storage clusters.`
A vision example might say: `We segment medical images using convolutional feature hierarchies.`
Notice that each example contains several clues.
The model is not told which words are clues.
The model discovers associations through repeated examples.
If every NLP example mentions attention, attention becomes a strong NLP signal.
If every topic uses the word model, model becomes less distinctive.
TF-IDF handles that distinction better than raw counts.
When using `TfidfVectorizer`, do not manually lowercase text first unless you have a clear reason.
The vectorizer can lowercase consistently through `lowercase=True`.
Beginner code often over-cleans text.
Over-cleaning can remove useful tokens such as `tf-idf`, `BERT` in later chapters, or domain abbreviations.
For Week 11, use simple vectorizer options and inspect results before adding more cleaning.
A useful first configuration is `TfidfVectorizer(lowercase=True, min_df=1, ngram_range=(1, 2))`.
`min_df=1` keeps terms appearing in at least one document.
On a tiny dataset, higher `min_df` may remove too much.
On a larger dataset, `min_df=2` can remove one-off noise.
`ngram_range=(1, 2)` includes unigrams and bigrams.
A unigram is one token such as `attention`.
A bigram is two adjacent tokens such as `language model`.
Bigrams can capture research phrases better than single words alone.
Do not add trigrams immediately unless you have enough data.
More features can help, but they can also overfit.
After splitting, inspect class counts in train and test.
If the test set lacks a class, per-class metrics for that class are not meaningful.
If stratification fails, the dataset is probably too small for the requested split.
For classroom data, you can reduce the number of labels or collect more examples.
For project data, collect more labeled abstracts before claiming performance.
When fitting LogisticRegression, convergence warnings are common for beginners.
Start with `max_iter=1000` to avoid needless friction.
If warnings remain, check whether the dataset is strange or extremely small.
When fitting MultinomialNB, remember it expects non-negative features.
TF-IDF features are non-negative, so the pairing is valid.
After prediction, read the classification report slowly.
Do not jump to the average line first.
Read each class row.
A class with precision 1.00 and recall 0.25 means predictions for that class were usually correct, but most actual examples were missed.
A class with precision 0.25 and recall 1.00 means the model found all actual examples but also mislabeled many other examples as that class.
Macro average treats every class equally.
Weighted average gives larger classes more influence.
If macro F1 is much lower than weighted F1, smaller classes may be suffering.
A confusion matrix gives the next level of detail.
Rows are actual labels when you pass `y_test` first.
Columns are predicted labels when you pass predictions second.
The diagonal cells are correct predictions.
Off-diagonal cells are mistakes.
Mistakes are not only bad news.
Mistakes are data about what the model does not understand.
If `rag` is confused with `nlp`, maybe the label definitions overlap.
If `systems` is confused with `optimization`, maybe the abstracts share performance vocabulary.
Inspecting errors often improves datasets faster than changing algorithms.
A model artifact should be treated as tied to its training data and parameters.
If you retrain with new labels, the old artifact is not the same model anymore.
Name artifacts clearly or store metadata beside them.
Week 12 will formalize that habit.
For now, write down the command used to create the artifact.
During inference, pass a list of strings to `pipeline.predict`.
Even one abstract should be wrapped in a list: `[abstract_text]`.
The result is usually an array-like object of predicted labels.
Take the first element for a single prediction.
Do not call `fit` in prediction code.
Prediction code should load and call `predict` only.
If a prediction seems wrong, compare it to similar training examples.
The model can only learn from patterns present in training data.
If the training data has no retrieval papers, it cannot reliably learn `rag`.
If the training data contains labels with different naming conventions, standardize them.
`NLP`, `nlp`, and `natural_language_processing` should not accidentally become three labels unless that is intended.
Finally, remember the human role.
A topic classifier suggests a label.
It does not replace judgment about a paper.
ResearchOps should communicate predictions as model outputs, not absolute truth.

## Unified chapter checklist

- Before training, ask whether every example has exactly one intended topic label.
- Before training, ask whether each label has enough examples to split.
- Before training, ask whether abstracts are realistic or only keyword lists.
- Before training, ask whether duplicate examples cross the split boundary.
- Before training, ask whether labels are consistently spelled.
- Before training, ask whether file loading order could hide bugs.
- Before training, ask whether empty abstracts are filtered or reported.
- Before training, ask whether the command prints the dataset path.
- Before training, ask whether class counts are visible.
- Before training, ask whether random seed is fixed.
- During training, confirm that `.fit()` is called on training text only.
- During training, confirm that TF-IDF and classifier are in one Pipeline.
- During training, confirm that LogisticRegression uses enough iterations.
- During training, confirm that Naive Bayes comparisons use the same split.
- During training, confirm that no future-week dependencies are imported.
- During evaluation, read support before reading F1.
- During evaluation, compare macro and weighted averages.
- During evaluation, inspect at least three wrong predictions.
- During evaluation, decide whether false positives or false negatives are more expensive.
- During evaluation, write down one data improvement before one model improvement.
- During artifact handling, save the fitted Pipeline.
- During artifact handling, load the artifact in a separate process or command if possible.
- During artifact handling, predict with raw text to prove the vectorizer was saved.
- During artifact handling, do not overwrite important artifacts without recording what changed.
- During inference, never refit the vectorizer on the new abstract.
- During inference, treat very short abstracts as low-context inputs.
- During inference, show the predicted label clearly.
- During inference, avoid presenting the prediction as a human-reviewed topic.
- After training, document the command, data path, model type, and score summary.
- After training, keep the baseline result available for future comparison.
- Final check: explain one NLP abstract from raw words through TF-IDF columns to a predicted class.
- Final check: explain one systems abstract and name the vocabulary clues the model might learn.
- Final check: explain one vision abstract and identify which bigrams might be more useful than unigrams.
- Final check: describe how the same raw abstract is handled differently during fitting and prediction.
- Final check: point to the exact moment the test set stops being available for learning.
- Final check: name one metric that would reveal poor minority-class performance.
- Final check: name one confusion-matrix cell that would worry a ResearchOps maintainer.
- Final check: describe what should happen if a JSONL file has an empty `text` value.
- Final check: describe what should happen if a class has too few examples for stratification.
- Final check: explain why the majority-class baseline belongs in an honest comparison.
- Final check: state why `ngram_range=(1, 2)` might help paper-topic classification.
- Final check: state why too many feature settings can overfit a small training set.
- Final check: explain why `MultinomialNB` is a comparison baseline, not a future-week neural model.
- Final check: explain why saved artifacts must be connected to the data that trained them.
- Final check: describe how a CLI command should call service code instead of owning ML logic.
- Final check: identify one place where a test can catch accidental data leakage.
- Final check: identify one place where a test can catch a malformed training example.
- Final check: explain what macro F1 tells you that weighted F1 may soften.
- Final check: explain why error analysis can improve labels before changing classifiers.
- Final check: say aloud why this chapter is complete without embeddings or transformer models.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 11 — Classical ML: Topic Classification:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
