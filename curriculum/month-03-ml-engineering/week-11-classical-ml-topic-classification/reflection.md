# Reflection - Week 11 Classical ML Topic Classification

This is your personal record for Week 11. The quality of this reflection is a signal of how deeply you understood the material.

---

## What I built

**Dataset format:**
(Describe the JSONL structure, number of labels, and approximate number of examples per label.)

**Model pipeline:**
(Write the two steps of your Pipeline — vectorizer settings and classifier settings.)

**Metrics I observed (fill in from your actual run):**

| Class | Precision | Recall | F1 |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| Overall accuracy | | | |

---

## What broke

**Training or split issue:**
(Did `stratify=labels` fail? Did the split produce empty splits? Describe and explain.)

**Artifact or file issue:**
(Did saving fail? Did loading produce an unexpected type? What error appeared?)

**How I noticed it:**
(Was it a test failure, a crash, or a wrong prediction?)

---

## What I misunderstood

**TF-IDF concept I had to re-read:**
(Was it IDF vs. TF? Or why the vectorizer must not be fit on test data?)

**Metric I first misread:**
(Did you trust accuracy too early? Did you misread recall as precision?)

**Leakage risk I had not seen before:**
(Write the specific mistake in your own words. Why does it matter?)

---

## What I fixed

**Dataset or training bug:**
(What did you fix? How did you know it was a bug?)

**Evaluation improvement:**
(Did you switch from accuracy to F1? Did you add stratification? Add class weights?)

**Evidence the baseline is trustworthy:**
(What properties of the evaluation give you confidence the metrics are real?)

---

## Leakage audit

Write the answer to these questions directly:

1. Is your vectorizer inside the Pipeline? (Yes/No)
2. Is `train_test_split` called before or after the Pipeline is fit? (Before/After)
3. Is the test set ever used for anything other than final evaluation? (Yes/No — should be No)

---

## Confusion matrix analysis

Draw or paste your confusion matrix here:

```
[your confusion matrix]
```

What do the off-diagonal entries reveal? Which class pair is most confused and why?

---

## Confidence score

- Week 11 confidence (1–10):
- Reason for that score:
- The one ML concept I can now explain confidently:
- The one thing I am still uncertain about:

---

## Preparation for Week 12

- [ ] I can explain what parameters (max_features, C) were used in this training run.
- [ ] I know where the model artifact is saved.
- [ ] I know what metrics were achieved, from memory.
- [ ] I am ready to track these details automatically in Week 12.
