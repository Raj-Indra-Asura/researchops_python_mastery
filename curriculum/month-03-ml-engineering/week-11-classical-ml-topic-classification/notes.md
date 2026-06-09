# Notes - Week 11 Classical ML Topic Classification

Machine learning starts long before model code. First you need examples with labels. In this week, each training example is a document text plus a topic label such as `nlp`, `systems`, or `vision`. Supervised learning means the model learns a mapping from input features to known labels.

Raw text cannot be fed directly into most classical models. It must be converted into numbers. TF-IDF stands for term frequency-inverse document frequency. It gives higher weight to words that are frequent in one document but not common across all documents. That makes words like `transformer` or `retrieval` more informative than words like `the` or `paper`.

Scikit-learn makes this convenient:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000)),
])
```

A pipeline is helpful because it packages preprocessing and model training together. That reduces the chance that training and prediction paths drift apart.

You should split data into train and test sets before evaluating.

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

`stratify=labels` helps keep class balance similar across the split, which matters when some topics are rarer than others.

After training, evaluate more than raw accuracy. If one class dominates the data, accuracy can be misleading. Precision asks: when the model predicts a topic, how often is it right? Recall asks: of the documents that truly belong to a topic, how many did the model find? F1 balances precision and recall.

```python
from sklearn.metrics import classification_report

predictions = model.predict(X_test)
print(classification_report(y_test, predictions))
```

A confusion matrix can reveal patterns such as the model often confusing `rag` papers with `semantic-search` papers. That is useful because it points toward better labels, more examples, or clearer feature engineering.

Be careful about leakage. Leakage happens when information from the test set sneaks into training, making the evaluation unrealistically optimistic. Fitting the vectorizer on the full dataset before the split is a classic mistake. Using a pipeline avoids that because the vectorizer is fit only inside training.

Model persistence matters if you want to reuse the trained baseline.

```python
import joblib
joblib.dump(model, "artifacts/topic_classifier.joblib")
```

That artifact can later be loaded for batch prediction or API serving.

Your goal this week is not to beat state-of-the-art benchmarks. It is to build a trustworthy baseline. A well-understood TF-IDF model is fast, interpretable, and surprisingly competitive on many document tasks. It also teaches the engineering habits needed for more advanced models later: clean datasets, careful splits, evaluation discipline, and artifact management.
