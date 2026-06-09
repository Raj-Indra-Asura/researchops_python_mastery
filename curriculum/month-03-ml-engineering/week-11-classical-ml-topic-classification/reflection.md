# Reflection - Week 11 Classical ML Topic Classification

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 11 — Classical ML: Topic Classification](./README.md) › **reflection.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 11 — Classical ML: Topic Classification** · *reflection.md — the journal* (step 6 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [validation.md](./validation.md)
- ▶ **Next:** [Write your Week 11 report](../../../docs/weekly-reports/README.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. **➡ [reflection.md](./reflection.md) ← you are here**
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
