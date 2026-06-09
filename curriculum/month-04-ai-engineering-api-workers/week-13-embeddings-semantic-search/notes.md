<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 13 Embeddings and Semantic Search

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 13: Embeddings and Semantic Search

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Meaning as a vector**.
The practical milestone is: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
The expected capability is: Can explain what an embedding is, implement cosine similarity search, chunk text for a retrieval pipeline, and explain why caching matters. ---
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

- Week 9 taught Protocols, Interfaces, and Clean Architecture; keep its responsibility in mind, but do not rebuild it here.
- Week 10 taught Testing Discipline and Quality Gates; keep its responsibility in mind, but do not rebuild it here.
- Week 11 taught Classical ML — Topic Classification; keep its responsibility in mind, but do not rebuild it here.
- Week 12 taught Experiment Tracking; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 13 solves the project problem behind **Embeddings and Semantic Search**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `What embeddings are: a dense numeric representation of meaning` helps solve part of this gap.
- The concept `Chunking text for embedding: why long documents need to be split` helps solve part of this gap.
- The concept ``sentence-transformers` local models: no API key, no network call needed` helps solve part of this gap.
- The concept `Cosine similarity: angle between vectors as a measure of semantic closeness` helps solve part of this gap.
- The concept `Embedding cache: don't recompute what you already have` helps solve part of this gap.
- The concept `Retrieval evaluation: does the top result make sense?` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Embeddings and Semantic Search**?
- Ask: what is the owner for **Embeddings and Semantic Search**?
- Ask: what is the transformation for **Embeddings and Semantic Search**?
- Ask: what is the proof for **Embeddings and Semantic Search**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| What embeddings are | What embeddings are: a dense numeric representation of meaning | This term names one job in the Week 13 milestone. |
| Chunking text for embedding | Chunking text for embedding: why long documents need to be split | This term names one job in the Week 13 milestone. |
| sentence-transformers` local models | `sentence-transformers` local models: no API key, no network call needed | This term names one job in the Week 13 milestone. |
| Cosine similarity | Cosine similarity: angle between vectors as a measure of semantic closeness | This term names one job in the Week 13 milestone. |
| Embedding cache | Embedding cache: don't recompute what you already have | This term names one job in the Week 13 milestone. |
| Retrieval evaluation | Retrieval evaluation: does the top result make sense? | This term names one job in the Week 13 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: What embeddings are: a dense numeric representation of meaning
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 13, it supports the milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Chunking text for embedding: why long documents need to be split
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 13, it supports the milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: `sentence-transformers` local models: no API key, no network call needed
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 13, it supports the milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Cosine similarity: angle between vectors as a measure of semantic closeness
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 13, it supports the milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Embedding cache: don't recompute what you already have
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 13, it supports the milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: Retrieval evaluation: does the top result make sense?
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 13, it supports the milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/search/chunking.py` — text chunker
- `src/researchops/search/embeddings.py` — embedding generation and cache
- `src/researchops/search/vector_search.py` — cosine similarity ranking
- `src/researchops/core/interfaces.py` — `SearchEngine` protocol updated
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
def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_length = sum(a * a for a in left) ** 0.5
    right_length = sum(b * b for b in right) ** 0.5
    return dot / (left_length * right_length)
```

Line-by-line explanation:
- Line 1: `def cosine_similarity(left: list[float], right: list[float]) -> float:` — This names a reusable action and shows what information it receives.
- Line 2: `dot = sum(a * b for a, b in zip(left, right))` — This stores a clear intermediate value for the next step.
- Line 3: `left_length = sum(a * a for a in left) ** 0.5` — This stores a clear intermediate value for the next step.
- Line 4: `right_length = sum(b * b for b in right) ** 0.5` — This stores a clear intermediate value for the next step.
- Line 5: `return dot / (left_length * right_length)` — This produces the result or performs the declared setup step.

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
- `tests/unit/test_chunking.py`
- `tests/unit/test_vector_search.py` — cosine similarity with known vectors
Validation commands:
```bash
researchops semantic-search "machine learning"
pytest tests/unit/test_chunking.py tests/unit/test_vector_search.py -v
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
Week 13 contributes by making **embeddings and semantic search** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 13 solve?
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

- Explain Embeddings and Semantic Search in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Embeddings and Semantic Search.
- The milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity to the query.
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

Next week is Week 14: **FastAPI Layer**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `What embeddings are: a dense numeric representation of meaning` from user input to project result.
- Drill 2: Write one sentence defining `What embeddings are: a dense numeric representation of meaning` without copying the notes.
- Drill 3: Find the file where `What embeddings are: a dense numeric representation of meaning` appears or should appear.
- Drill 4: Name one wrong implementation of `What embeddings are: a dense numeric representation of meaning` and why it would hurt.
- Drill 5: Name one test that would protect `What embeddings are: a dense numeric representation of meaning`.
- Drill 6: Trace `Chunking text for embedding: why long documents need to be split` from user input to project result.
- Drill 7: Write one sentence defining `Chunking text for embedding: why long documents need to be split` without copying the notes.
- Drill 8: Find the file where `Chunking text for embedding: why long documents need to be split` appears or should appear.
- Drill 9: Name one wrong implementation of `Chunking text for embedding: why long documents need to be split` and why it would hurt.
- Drill 10: Name one test that would protect `Chunking text for embedding: why long documents need to be split`.
- Drill 11: Trace ``sentence-transformers` local models: no API key, no network call needed` from user input to project result.
- Drill 12: Write one sentence defining ``sentence-transformers` local models: no API key, no network call needed` without copying the notes.
- Drill 13: Find the file where ``sentence-transformers` local models: no API key, no network call needed` appears or should appear.
- Drill 14: Name one wrong implementation of ``sentence-transformers` local models: no API key, no network call needed` and why it would hurt.
- Drill 15: Name one test that would protect ``sentence-transformers` local models: no API key, no network call needed`.
- Drill 16: Trace `Cosine similarity: angle between vectors as a measure of semantic closeness` from user input to project result.
- Drill 17: Write one sentence defining `Cosine similarity: angle between vectors as a measure of semantic closeness` without copying the notes.
- Drill 18: Find the file where `Cosine similarity: angle between vectors as a measure of semantic closeness` appears or should appear.
- Drill 19: Name one wrong implementation of `Cosine similarity: angle between vectors as a measure of semantic closeness` and why it would hurt.
- Drill 20: Name one test that would protect `Cosine similarity: angle between vectors as a measure of semantic closeness`.
- Drill 21: Trace `Embedding cache: don't recompute what you already have` from user input to project result.
- Drill 22: Write one sentence defining `Embedding cache: don't recompute what you already have` without copying the notes.
- Drill 23: Find the file where `Embedding cache: don't recompute what you already have` appears or should appear.
- Drill 24: Name one wrong implementation of `Embedding cache: don't recompute what you already have` and why it would hurt.
- Drill 25: Name one test that would protect `Embedding cache: don't recompute what you already have`.
- Drill 26: Trace `Retrieval evaluation: does the top result make sense?` from user input to project result.
- Drill 27: Write one sentence defining `Retrieval evaluation: does the top result make sense?` without copying the notes.
- Drill 28: Find the file where `Retrieval evaluation: does the top result make sense?` appears or should appear.
- Drill 29: Name one wrong implementation of `Retrieval evaluation: does the top result make sense?` and why it would hurt.
- Drill 30: Name one test that would protect `Retrieval evaluation: does the top result make sense?`.
- Drill 31: Draw the Week 13 data flow in four boxes.
- Drill 32: Say why `Embeddings and Semantic Search` belongs in this month of the curriculum.
- Drill 33: Rewrite one error message in beginner-friendly language.
- Drill 34: List the exact assumptions made by the example code.
- Drill 35: List the exact assumptions checked by the tests.
- Drill 36: Point to the line where raw input becomes project meaning.
- Drill 37: Point to the line where the result becomes visible to a user.
- Drill 38: Explain what would happen if the main file were deleted.
- Drill 39: Explain what would happen if the main test were deleted.
- Drill 40: Describe the smallest manual check you can run.
- Drill 41: Describe the smallest automated check you can run.
- Drill 42: Name the most likely beginner mistake for this week.
- Drill 43: Name the safest recovery move for that mistake.
- Drill 44: Explain what knowledge should be carried into the next chapter.
- Drill 45: Trace `What embeddings are: a dense numeric representation of meaning` from user input to project result.
- Drill 46: Write one sentence defining `What embeddings are: a dense numeric representation of meaning` without copying the notes.
- Drill 47: Find the file where `What embeddings are: a dense numeric representation of meaning` appears or should appear.
- Drill 48: Name one wrong implementation of `What embeddings are: a dense numeric representation of meaning` and why it would hurt.
- Drill 49: Name one test that would protect `What embeddings are: a dense numeric representation of meaning`.
- Drill 50: Trace `Chunking text for embedding: why long documents need to be split` from user input to project result.
- Drill 51: Write one sentence defining `Chunking text for embedding: why long documents need to be split` without copying the notes.
- Drill 52: Find the file where `Chunking text for embedding: why long documents need to be split` appears or should appear.
- Drill 53: Name one wrong implementation of `Chunking text for embedding: why long documents need to be split` and why it would hurt.
- Drill 54: Name one test that would protect `Chunking text for embedding: why long documents need to be split`.
- Drill 55: Trace ``sentence-transformers` local models: no API key, no network call needed` from user input to project result.
- Drill 56: Write one sentence defining ``sentence-transformers` local models: no API key, no network call needed` without copying the notes.
- Drill 57: Find the file where ``sentence-transformers` local models: no API key, no network call needed` appears or should appear.
- Drill 58: Name one wrong implementation of ``sentence-transformers` local models: no API key, no network call needed` and why it would hurt.
- Drill 59: Name one test that would protect ``sentence-transformers` local models: no API key, no network call needed`.
- Drill 60: Trace `Cosine similarity: angle between vectors as a measure of semantic closeness` from user input to project result.
- Drill 61: Write one sentence defining `Cosine similarity: angle between vectors as a measure of semantic closeness` without copying the notes.
- Drill 62: Find the file where `Cosine similarity: angle between vectors as a measure of semantic closeness` appears or should appear.
- Drill 63: Name one wrong implementation of `Cosine similarity: angle between vectors as a measure of semantic closeness` and why it would hurt.
- Drill 64: Name one test that would protect `Cosine similarity: angle between vectors as a measure of semantic closeness`.
- Drill 65: Trace `Embedding cache: don't recompute what you already have` from user input to project result.
- Drill 66: Write one sentence defining `Embedding cache: don't recompute what you already have` without copying the notes.
- Drill 67: Find the file where `Embedding cache: don't recompute what you already have` appears or should appear.
- Drill 68: Name one wrong implementation of `Embedding cache: don't recompute what you already have` and why it would hurt.
- Drill 69: Name one test that would protect `Embedding cache: don't recompute what you already have`.
- Drill 70: Trace `Retrieval evaluation: does the top result make sense?` from user input to project result.
- Drill 71: Write one sentence defining `Retrieval evaluation: does the top result make sense?` without copying the notes.
- Drill 72: Find the file where `Retrieval evaluation: does the top result make sense?` appears or should appear.
- Drill 73: Name one wrong implementation of `Retrieval evaluation: does the top result make sense?` and why it would hurt.
- Drill 74: Name one test that would protect `Retrieval evaluation: does the top result make sense?`.
- Drill 75: Draw the Week 13 data flow in four boxes.
- Drill 76: Say why `Embeddings and Semantic Search` belongs in this month of the curriculum.
- Drill 77: Rewrite one error message in beginner-friendly language.
- Drill 78: List the exact assumptions made by the example code.
- Drill 79: List the exact assumptions checked by the tests.
- Drill 80: Point to the line where raw input becomes project meaning.
- Drill 81: Point to the line where the result becomes visible to a user.
- Drill 82: Explain what would happen if the main file were deleted.
- Drill 83: Explain what would happen if the main test were deleted.
- Drill 84: Describe the smallest manual check you can run.
- Drill 85: Describe the smallest automated check you can run.
- Drill 86: Name the most likely beginner mistake for this week.
- Drill 87: Name the safest recovery move for that mistake.
- Drill 88: Explain what knowledge should be carried into the next chapter.
- Drill 89: Trace `What embeddings are: a dense numeric representation of meaning` from user input to project result.
- Drill 90: Write one sentence defining `What embeddings are: a dense numeric representation of meaning` without copying the notes.
- Drill 91: Find the file where `What embeddings are: a dense numeric representation of meaning` appears or should appear.
- Drill 92: Name one wrong implementation of `What embeddings are: a dense numeric representation of meaning` and why it would hurt.
- Drill 93: Name one test that would protect `What embeddings are: a dense numeric representation of meaning`.
- Drill 94: Trace `Chunking text for embedding: why long documents need to be split` from user input to project result.
- Drill 95: Write one sentence defining `Chunking text for embedding: why long documents need to be split` without copying the notes.
- Drill 96: Find the file where `Chunking text for embedding: why long documents need to be split` appears or should appear.
- Drill 97: Name one wrong implementation of `Chunking text for embedding: why long documents need to be split` and why it would hurt.
- Drill 98: Name one test that would protect `Chunking text for embedding: why long documents need to be split`.
- Drill 99: Trace ``sentence-transformers` local models: no API key, no network call needed` from user input to project result.
- Drill 100: Write one sentence defining ``sentence-transformers` local models: no API key, no network call needed` without copying the notes.
- Drill 101: Find the file where ``sentence-transformers` local models: no API key, no network call needed` appears or should appear.
- Drill 102: Name one wrong implementation of ``sentence-transformers` local models: no API key, no network call needed` and why it would hurt.
- Drill 103: Name one test that would protect ``sentence-transformers` local models: no API key, no network call needed`.
- Drill 104: Trace `Cosine similarity: angle between vectors as a measure of semantic closeness` from user input to project result.
- Drill 105: Write one sentence defining `Cosine similarity: angle between vectors as a measure of semantic closeness` without copying the notes.
- Drill 106: Find the file where `Cosine similarity: angle between vectors as a measure of semantic closeness` appears or should appear.
- Drill 107: Name one wrong implementation of `Cosine similarity: angle between vectors as a measure of semantic closeness` and why it would hurt.
- Drill 108: Name one test that would protect `Cosine similarity: angle between vectors as a measure of semantic closeness`.
- Drill 109: Trace `Embedding cache: don't recompute what you already have` from user input to project result.
- Drill 110: Write one sentence defining `Embedding cache: don't recompute what you already have` without copying the notes.
- Drill 111: Find the file where `Embedding cache: don't recompute what you already have` appears or should appear.
- Drill 112: Name one wrong implementation of `Embedding cache: don't recompute what you already have` and why it would hurt.
- Drill 113: Name one test that would protect `Embedding cache: don't recompute what you already have`.
- Drill 114: Trace `Retrieval evaluation: does the top result make sense?` from user input to project result.
- Drill 115: Write one sentence defining `Retrieval evaluation: does the top result make sense?` without copying the notes.
- Drill 116: Find the file where `Retrieval evaluation: does the top result make sense?` appears or should appear.
- Drill 117: Name one wrong implementation of `Retrieval evaluation: does the top result make sense?` and why it would hurt.
- Drill 118: Name one test that would protect `Retrieval evaluation: does the top result make sense?`.
- Drill 119: Draw the Week 13 data flow in four boxes.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes

## Why keyword search is not enough

Keyword search finds documents that contain the words you typed. That sounds useful, and it often is. But it has a hard limit: it matches letters, not ideas.

Suppose a researcher stored a paper that calls a technique "dense retrieval" and later queries for "vector search". Keyword search finds nothing, even though the paper is deeply relevant. The problem is that natural language is rich and inconsistent. Authors use synonyms, abbreviations, domain-specific terms, and different phrasing for the same concept.

Semantic search tries to find documents that mean the same thing as the query, even if the exact words do not appear. To do that, text must be converted into a mathematical form that captures meaning. That form is called an embedding.

---

## What an embedding is

An embedding is a list of numbers that represents the meaning of a piece of text.

Here is the most important intuition: text that means similar things should produce numbers that are close together. Text that means different things should produce numbers that are far apart.

For example:
- "neural network" and "deep learning model" should have similar numbers.
- "neural network" and "tomato soup" should have very different numbers.

The list of numbers is called a vector. A vector is just a sequence of floating-point values, like `[0.12, -0.45, 0.87, ...]`. The length of that list is called the number of dimensions.

---

## Vector intuition and dimensions

Think of a two-dimensional vector as a point on a map. `[3.0, 1.0]` is a location. `[3.1, 0.9]` is a nearby location. `[-5.0, 8.0]` is far away.

Real embedding models use hundreds or thousands of dimensions. You cannot visualize 384 dimensions, but the math works the same way. Two vectors are close if their values are similar across all dimensions.

A popular small model called `all-MiniLM-L6-v2` produces 384-dimensional vectors. A larger model might produce 768 or 1536 dimensions. More dimensions can capture finer distinctions, but require more memory and compute.

The key insight: you do not define what each dimension means. The model learns that during training. The model has seen enormous amounts of text and has learned to encode meaning as geometry.

---

## Cosine similarity

To compare two vectors, you need a distance or similarity measure. The most common is cosine similarity.

Cosine similarity measures the angle between two vectors, not the distance between their endpoints. Two vectors pointing in exactly the same direction have cosine similarity of 1.0. Two vectors pointing in opposite directions have cosine similarity of -1.0. Two unrelated vectors point in roughly perpendicular directions and have cosine similarity near 0.

```python
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))      # line 1
    norm_a = math.sqrt(sum(x * x for x in a))   # line 2
    norm_b = math.sqrt(sum(y * y for y in b))   # line 3
    return dot / (norm_a * norm_b)               # line 4
```

Line 1: compute the dot product. Multiply matching positions and sum. Two vectors pointing the same direction produce a large positive dot product.

Line 2: compute the magnitude (length) of vector `a`. Square each element, sum them, take the square root.

Line 3: compute the magnitude of vector `b`.

Line 4: divide the dot product by the product of magnitudes. This normalises by how long the vectors are, so only direction matters. The result is always between -1 and 1.

Why cosine and not Euclidean distance? Because embedding magnitudes can vary. A long text might produce a larger-magnitude vector than a short text. Cosine similarity ignores magnitude and compares only direction, which gives more stable similarity scores.

---

## Why long documents need chunking

A research paper can be 10 000 words or more. If you embed the entire paper as one vector, that single vector must encode everything: abstract, methods, results, conclusion. When a user queries for a specific technique described in the methods section, the whole-document embedding is too diluted. The signal from that one section is washed out.

Chunking solves this by splitting the document into smaller pieces. Each chunk is embedded separately. When a user queries, you compare the query vector to all chunk vectors and retrieve the most relevant chunks. This gives much finer-grained retrieval.

### Chunk size

Chunk size is measured in tokens or words. Common values are 200–500 words. Smaller chunks are more precise but provide less context per hit. Larger chunks provide more context but reduce precision.

A good default for research papers is 300 words. Start there and adjust based on qualitative inspection of results.

### Overlap

If you cut a document into non-overlapping windows, you risk splitting a sentence or idea across two chunks. Overlap solves this by repeating some words at the boundary between consecutive chunks.

For example, with chunk size 300 and overlap 50, chunk 1 covers words 0–299, chunk 2 covers words 250–549, chunk 3 covers words 500–799, and so on.

```python
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()          # line 1
    chunks: list[str] = []        # line 2
    start = 0                     # line 3
    while start < len(words):     # line 4
        end = min(len(words), start + chunk_size)       # line 5
        chunks.append(" ".join(words[start:end]))       # line 6
        start = end - overlap                           # line 7
    return chunks                 # line 8
```

Line 1: split the text on whitespace. This is a simple word-level split.

Line 2: accumulate chunks in a list.

Line 3: start at the beginning.

Line 4: keep going while there are still words.

Line 5: clip `end` so the last chunk does not exceed the document length.

Line 6: join the words back into a string and add it to the list.

Line 7: advance `start` by `chunk_size - overlap`. The overlap amount is repeated in the next chunk.

Line 8: return all chunks.

Edge case: if `overlap >= chunk_size`, `start` never advances and the loop runs forever. Always validate that `overlap < chunk_size` before calling this function.

### Chunk metadata

Every chunk must carry metadata linking it back to its source document. Without that link, retrieval is useless: the user gets a passage but cannot find the paper it came from.

Metadata should include at minimum:
- `source_id` — the document's unique identifier
- `chunk_index` — the position within the document
- `start_word` — where in the document this chunk begins

---

## The embedding pipeline

The full semantic retrieval process has two phases.

**Indexing phase** (run once per document):
1. Parse the document into clean text.
2. Chunk the text.
3. Embed each chunk using a model.
4. Store each (chunk_text, embedding, metadata) tuple.

**Query phase** (run for each search query):
1. Embed the query using the same model.
2. Compare the query embedding to all stored chunk embeddings.
3. Sort by cosine similarity descending.
4. Return the top-k chunks and their metadata.

The model used for indexing and querying must be the same. If you index with one model and query with another, the vector spaces are incompatible and the comparisons are meaningless.

---

## Using sentence-transformers locally

Install the library:

```bash
pip install -U sentence-transformers
```

Minimal example:

```python
from sentence_transformers import SentenceTransformer          # line 1

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # line 2
texts = ["attention mechanism", "convolutional neural networks"]        # line 3
embeddings = model.encode(texts)                                        # line 4
print(embeddings.shape)                                                 # line 5
```

Line 1: import the `SentenceTransformer` class. This class wraps a pretrained transformer model.

Line 2: load the model by name. On the first run this downloads the weights from the Hugging Face Hub (about 90 MB). On subsequent runs the weights are cached locally.

Line 3: a list of two short text strings. These are what you want to embed.

Line 4: `encode` takes a list of strings and returns a NumPy array of shape `(n_texts, embedding_dim)`. For this model that is `(2, 384)`.

Line 5: print `(2, 384)`. Two texts, 384 dimensions each.

To embed a single string, pass a list with one element: `model.encode(["my query"])`.

---

## Local models versus API embeddings

|                    | Local model (`sentence-transformers`) | API (OpenAI, Cohere, etc.) |
|--------------------|---------------------------------------|---------------------------|
| **Cost per call**  | Free after download                  | Pay per token              |
| **Latency**        | Milliseconds on CPU, faster on GPU   | Hundreds of milliseconds   |
| **Privacy**        | Text never leaves your machine       | Text sent to third party   |
| **Setup**          | Larger install (~90 MB model)        | Just an API key            |
| **Reproducibility**| Fully deterministic                  | Provider may change models |

For a learning project, local models are better: free, private, and reproducible.

The tradeoff for production: large-scale embedding via API may be cheaper than running a GPU server, but you lose control over versioning and privacy.

---

## The embedding interface and why it matters

Your code should not call `SentenceTransformer` directly everywhere. Wrap it behind a simple interface (a Protocol in Python terms).

```python
from typing import Protocol


class EmbeddingModel(Protocol):
    def embed(self, text: str) -> list[float]:
        ...
```

Any class that has an `embed(self, text: str) -> list[float]` method satisfies this protocol, without inheriting from it. This is called structural subtyping.

With this interface you can swap implementations:
- `SentenceTransformerEmbedder` for real use
- `FakeEmbeddingModel` for tests
- `OpenAIEmbedder` for cloud use

---

## Deterministic fake embeddings for tests

Real models are slow to load, require downloaded weights, and are non-deterministic across platforms. Tests must be fast, offline, and fully reproducible.

Use a fake that produces tiny deterministic vectors:

```python
class FakeEmbeddingModel:
    def embed(self, text: str) -> list[float]:
        return [float(len(text)), float(text.count(" ")), float(text.lower().count("a"))]
```

Line by line:
- `len(text)`: the number of characters. Longer texts produce a higher first dimension.
- `text.count(" ")`: the number of spaces, which approximates word count.
- `text.lower().count("a")`: the number of letter "a" characters.

This produces a 3-dimensional vector. That is enough to test cosine similarity ranking. You do not need 384 dimensions to check that your ranking logic sorts correctly.

Why is this better than using real embeddings in tests?
1. No internet or file download required.
2. Runs in microseconds.
3. The output is predictable: you can calculate expected similarity by hand.
4. CI does not need the `sentence-transformers` package installed.

The fake is honest about what it tests: ranking logic, not embedding quality. When you want to test embedding quality, write separate integration tests that use the real model and mark them as slow or optional.

---

## Embedding cache

Computing embeddings for thousands of chunks is expensive (slow, even on CPU). If you re-index the same document twice, you waste time. An embedding cache stores previously computed embeddings and returns them on subsequent calls without calling the model.

A simple cache key is the hash of the chunk text. If the text has not changed, return the cached embedding.

```python
import hashlib


class CachedEmbedder:
    def __init__(self, model: EmbeddingModel) -> None:
        self._model = model
        self._cache: dict[str, list[float]] = {}

    def embed(self, text: str) -> list[float]:
        key = hashlib.sha256(text.encode()).hexdigest()
        if key not in self._cache:
            self._cache[key] = self._model.embed(text)
        return self._cache[key]
```

This in-memory cache lives only for the lifetime of the object. For a persistent cache, write to SQLite or a file.

---

## Vector search and top-k retrieval

Once embeddings are stored, vector search is a loop:
1. Embed the query.
2. Compute cosine similarity between the query and each stored chunk.
3. Sort results by similarity descending.
4. Return the top-k results.

```python
from dataclasses import dataclass


@dataclass
class SearchHit:
    chunk_text: str
    score: float
    source_id: str
    chunk_index: int


def search(
    query_embedding: list[float],
    index: list[tuple[list[float], str, str, int]],
    top_k: int = 5,
) -> list[SearchHit]:
    scored = []
    for embedding, chunk_text, source_id, chunk_index in index:
        score = cosine_similarity(query_embedding, embedding)
        scored.append(SearchHit(chunk_text, score, source_id, chunk_index))
    scored.sort(key=lambda h: h.score, reverse=True)
    return scored[:top_k]
```

The `index` parameter is a list of tuples: (embedding, chunk_text, source_id, chunk_index). In production you might use a vector database like FAISS or Chroma for faster search, but a plain list works for hundreds of documents.

---

## Retrieval quality

How do you know if semantic search is working well? For this week, qualitative inspection is enough:
1. Index several papers.
2. Run queries that should match specific passages.
3. Inspect the top-3 hits.
4. Ask: does any hit match even though the exact words are absent?

For example: query "gradient descent optimisation" should retrieve a passage about "back-propagation and weight updates" even without the word "gradient" appearing.

When retrieval fails, common causes are:
- Chunk size too large (query gets diluted)
- Chunk size too small (too little context)
- Wrong model for the domain
- Query too short to have a meaningful embedding

---

## File locations in this project

The problem statement specifies these files. Use exactly these paths:

```
src/researchops/search/chunking.py
src/researchops/search/embeddings.py
src/researchops/search/vector_search.py
```

Not `semantic/`. The `search/` package already exists. Place your implementations there.

---

## Why RAG depends on retrieval

RAG stands for Retrieval-Augmented Generation. It is a pattern where you:
1. Retrieve relevant chunks from your document collection.
2. Pass those chunks as context to a language model.
3. The language model generates an answer using that context.

Step 1 is the retrieval step. If retrieval is bad — if it returns irrelevant chunks — the language model produces unreliable or hallucinated answers. Good retrieval is the foundation of good RAG.

This is why Week 13 matters so much. You are not just building search. You are building the retrieval foundation that Month 5's RAG assistant will depend on.

---

## Summary

- Keyword search matches words; semantic search matches meaning.
- An embedding is a list of numbers representing text meaning.
- Similar texts have similar (close) vectors; different texts have distant vectors.
- Cosine similarity measures the angle between two vectors, ignoring magnitude.
- Documents must be chunked before embedding; whole-document embeddings are too coarse.
- Overlap at chunk boundaries prevents ideas from being cut in half.
- Every chunk must carry metadata linking back to its source document.
- Use the same model for indexing and querying.
- Use a fake embedder for unit tests; real models in integration tests.
- `sentence-transformers` provides free, local, reproducible embeddings.
- The embedding interface decouples your code from any specific model.
- Retrieval quality is the foundation of RAG systems.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
