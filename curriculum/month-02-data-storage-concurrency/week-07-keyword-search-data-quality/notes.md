<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 07 Notes — Keyword Search and Data Quality

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 07: Keyword Search and Data Quality

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Finding signal in stored text**.
The practical milestone is: `researchops search "transformer attention"` returns ranked results from stored papers.
The expected capability is: Can implement basic text search with ranking, use fake repositories in unit tests, and explain what a data quality gate is.
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

- Week 3 taught OOP, Dataclasses, and Domain Modeling; keep its responsibility in mind, but do not rebuild it here.
- Week 4 taught CLI and Packaging; keep its responsibility in mind, but do not rebuild it here.
- Week 5 taught SQLite Storage Layer; keep its responsibility in mind, but do not rebuild it here.
- Week 6 taught PDF Parsing Pipeline; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 7 solves the project problem behind **Keyword Search and Data Quality**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `In-memory inverted index basics` helps solve part of this gap.
- The concept `Text normalisation: lowercasing, punctuation stripping, stopwords` helps solve part of this gap.
- The concept `Basic scoring and ranking` helps solve part of this gap.
- The concept `Data quality gates: detecting and reporting bad data` helps solve part of this gap.
- The concept ``SearchService` and `SearchResult` domain objects` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Keyword Search and Data Quality**?
- Ask: what is the owner for **Keyword Search and Data Quality**?
- Ask: what is the transformation for **Keyword Search and Data Quality**?
- Ask: what is the proof for **Keyword Search and Data Quality**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| In-memory inverted index basics | In-memory inverted index basics | This term names one job in the Week 7 milestone. |
| Text normalisation | Text normalisation: lowercasing, punctuation stripping, stopwords | This term names one job in the Week 7 milestone. |
| Basic scoring and ranking | Basic scoring and ranking | This term names one job in the Week 7 milestone. |
| Data quality gates | Data quality gates: detecting and reporting bad data | This term names one job in the Week 7 milestone. |
| SearchService` and `SearchResult` domain objects | `SearchService` and `SearchResult` domain objects | This term names one job in the Week 7 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: In-memory inverted index basics
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 7, it supports the milestone: `researchops search "transformer attention"` returns ranked results from stored papers.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Text normalisation: lowercasing, punctuation stripping, stopwords
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 7, it supports the milestone: `researchops search "transformer attention"` returns ranked results from stored papers.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: Basic scoring and ranking
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 7, it supports the milestone: `researchops search "transformer attention"` returns ranked results from stored papers.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Data quality gates: detecting and reporting bad data
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 7, it supports the milestone: `researchops search "transformer attention"` returns ranked results from stored papers.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: `SearchService` and `SearchResult` domain objects
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 7, it supports the milestone: `researchops search "transformer attention"` returns ranked results from stored papers.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/services/search_service.py`
- `src/researchops/services/paper_service.py` — stats, list, show
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
def score(query_words: set[str], document_words: set[str]) -> int:
    matches = query_words & document_words
    return len(matches)
```

Line-by-line explanation:
- Line 1: `def score(query_words: set[str], document_words: set[str]) -> int:` — This names a reusable action and shows what information it receives.
- Line 2: `matches = query_words & document_words` — This stores a clear intermediate value for the next step.
- Line 3: `return len(matches)` — This produces the result or performs the declared setup step.

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
- `tests/unit/test_search_service.py` — search with FakePaperRepository
- `tests/unit/test_paper_service.py`
Validation commands:
```bash
researchops search "machine learning"
researchops papers stats
pytest tests/unit/test_search_service.py -v
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
Week 7 contributes by making **keyword search and data quality** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 7 solve?
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

- Explain Keyword Search and Data Quality in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Keyword Search and Data Quality.
- The milestone: `researchops search "transformer attention"` returns ranked results from stored papers.
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

Next week is Week 8: **Multiprocessing Ingestion**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops ingest ./papers --workers 4` ingests using 4 parallel worker processes.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `In-memory inverted index basics` from user input to project result.
- Drill 2: Write one sentence defining `In-memory inverted index basics` without copying the notes.
- Drill 3: Find the file where `In-memory inverted index basics` appears or should appear.
- Drill 4: Name one wrong implementation of `In-memory inverted index basics` and why it would hurt.
- Drill 5: Name one test that would protect `In-memory inverted index basics`.
- Drill 6: Trace `Text normalisation: lowercasing, punctuation stripping, stopwords` from user input to project result.
- Drill 7: Write one sentence defining `Text normalisation: lowercasing, punctuation stripping, stopwords` without copying the notes.
- Drill 8: Find the file where `Text normalisation: lowercasing, punctuation stripping, stopwords` appears or should appear.
- Drill 9: Name one wrong implementation of `Text normalisation: lowercasing, punctuation stripping, stopwords` and why it would hurt.
- Drill 10: Name one test that would protect `Text normalisation: lowercasing, punctuation stripping, stopwords`.
- Drill 11: Trace `Basic scoring and ranking` from user input to project result.
- Drill 12: Write one sentence defining `Basic scoring and ranking` without copying the notes.
- Drill 13: Find the file where `Basic scoring and ranking` appears or should appear.
- Drill 14: Name one wrong implementation of `Basic scoring and ranking` and why it would hurt.
- Drill 15: Name one test that would protect `Basic scoring and ranking`.
- Drill 16: Trace `Data quality gates: detecting and reporting bad data` from user input to project result.
- Drill 17: Write one sentence defining `Data quality gates: detecting and reporting bad data` without copying the notes.
- Drill 18: Find the file where `Data quality gates: detecting and reporting bad data` appears or should appear.
- Drill 19: Name one wrong implementation of `Data quality gates: detecting and reporting bad data` and why it would hurt.
- Drill 20: Name one test that would protect `Data quality gates: detecting and reporting bad data`.
- Drill 21: Trace ``SearchService` and `SearchResult` domain objects` from user input to project result.
- Drill 22: Write one sentence defining ``SearchService` and `SearchResult` domain objects` without copying the notes.
- Drill 23: Find the file where ``SearchService` and `SearchResult` domain objects` appears or should appear.
- Drill 24: Name one wrong implementation of ``SearchService` and `SearchResult` domain objects` and why it would hurt.
- Drill 25: Name one test that would protect ``SearchService` and `SearchResult` domain objects`.
- Drill 26: Draw the Week 7 data flow in four boxes.
- Drill 27: Say why `Keyword Search and Data Quality` belongs in this month of the curriculum.
- Drill 28: Rewrite one error message in beginner-friendly language.
- Drill 29: List the exact assumptions made by the example code.
- Drill 30: List the exact assumptions checked by the tests.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes
## 1. Chapter overview

In Weeks 5 and 6 you built a system that can ingest PDFs and store them in a database.
Now you have papers.
But having papers is not enough.
You need to be able to find them.

This week you build keyword search.

Keyword search is not glamorous.
It is not neural, semantic, or intelligent.
But it is the foundation that every more sophisticated search system is built on top of.
Understanding keyword search teaches you to think about text as data, normalization as a prerequisite, and ranking as a tunable function.

You also learn something equally important: **data quality**.
If the text in your database is noisy, inconsistent, or empty, search will be poor no matter how clever your algorithm is.
This week you learn to measure and improve data quality as part of the engineering process.

By the end of this week, `researchops search "query"` will return ranked results from your database.

---

## 2. Why search before AI?

A natural question is: why not skip keyword search and go directly to embeddings and semantic search?

The answer is that semantic search requires your data to be clean and complete first.

If 30% of your PDFs extracted no useful text (image-only pages, corrupt files), vector embeddings of that empty text are meaningless.
If titles are garbled and abstract fields are empty, semantic similarity cannot work on things that do not exist.

Keyword search forces you to confront data quality directly.
When a search for `"transformer architecture"` returns nothing from a paper you know discusses transformers, the bug is often in the data pipeline, not the search algorithm.
Fixing the data makes all downstream systems better — including future semantic search.

This is also why ResearchOps implements search in this order:
1. Week 7: keyword search (forces data quality)
2. Month 3+: embeddings and vector search (builds on clean data)

---

## 3. The text processing journey

Raw text extracted from a PDF is not clean.
A research paper's raw text might look like:

```
Attention Is All You Need\n\nVaswani et al., 2017\n\nAbstract\n\nThe dominant  sequence\ntransduction models  are based on complex  recurrent...\n\x0c\n2\nTable 1 Model comparisons...\n\fPage footer repeated here
```

Problems you can see:
- Extra whitespace between words.
- Page breaks (`\x0c` is a form feed character).
- Repeated headers and footers on every page.
- Broken line breaks splitting words across lines.

Before you can search this text, you need to normalize it.

---

## 4. Text normalization

Normalization is the process of transforming text into a consistent, predictable form.

The goal is not to make the text "better" in a human reading sense.
The goal is to make comparisons reliable.

If a document says `Transformer Models` and a query says `transformer models`, these are the same words, and normalization should make the system recognize that.

### Step 1: Unicode normalization

```python
import unicodedata

text = unicodedata.normalize("NFKC", raw_text)
```

`NFKC` normalization does two things:
- **K (compatibility)**: collapses visual variants to canonical form.
  For example, `ﬁ` (the fi ligature, often seen in PDFs) becomes `fi`.
  The string `ﬁeld` becomes `field`.
- **C (composition)**: composes characters with their diacritics.
  Useful for consistent handling of accented characters.

Without this step, the string `"ﬁeld"` would not match a query for `"field"`.

### Step 2: Lowercase

```python
text = text.lower()
```

Case differences are almost never meaningful for research paper search.
`"Transformer"` and `"transformer"` should match.

### Step 3: Remove punctuation and special characters

```python
import re

text = re.sub(r"[^a-z0-9\s]", " ", text)
```

`[^a-z0-9\s]` is a character class that matches anything that is NOT a lowercase letter, digit, or whitespace.
The `^` inside the brackets inverts the match.
`re.sub` replaces every match with a space.

The result: `"Attention Is All You Need, 2017."` becomes `"attention is all you need  2017 "`.

### Step 4: Collapse whitespace

```python
text = " ".join(text.split())
```

`text.split()` splits on any whitespace (spaces, tabs, newlines) and removes empty strings.
`" ".join(...)` rejoins with single spaces.

The result: `"attention is all you need  2017 "` becomes `"attention is all you need 2017"`.

### Complete normalization function

This is the actual `normalise_for_search` function in the codebase:

```python
import re
import unicodedata


def normalise_for_search(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)      # step 1: unicode
    text = text.lower()                              # step 2: lowercase
    text = re.sub(r"[^a-z0-9\s]", " ", text)        # step 3: punctuation
    return " ".join(text.split())                    # step 4: whitespace
```

This function is used both when indexing papers (normalizing stored text) and when processing queries (normalizing the search term).
If both sides go through the same normalization, the comparison is fair.

---

## 5. Tokenization

Tokenization means splitting text into individual tokens (usually words).

For a basic keyword search system, tokenization is just `str.split()` on normalized text:

```python
def tokenize(text: str) -> list[str]:
    return normalise_for_search(text).split()
```

The result of `tokenize("Attention Is All You Need")`:
```python
["attention", "is", "all", "you", "need"]
```

More advanced tokenizers handle:
- Compound words (`"machine-learning"` → `["machine", "learning"]`)
- Stemming (`"running"` → `"run"`)
- Lemmatization (`"better"` → `"good"`)

None of that is needed this week.
Simple whitespace splitting on normalized text is enough.

---

## 6. Stopwords

**Stopwords** are very common words that carry little meaning for search purposes: `the`, `a`, `is`, `are`, `in`, `of`, `and`, `to`.

The idea is that a query like `"what is a transformer"` should match on `"transformer"`, not on `"what"`, `"is"`, `"a"`.

The week-07 implementation does not remove stopwords.
That is an intentional simplification.
Removing stopwords requires a curated list and can cause unexpected behavior (imagine searching for the paper `"Is This a Good Algorithm?"` — removing stopwords strips almost the entire query).

For a first implementation, keyword matching without stopword removal is fine.
Stopword removal is a meaningful stretch exercise.

---

## 7. Exact match versus partial match

**Exact token match**: `"transformer"` matches only the word `"transformer"`.

**Partial/substring match**: `"trans"` matches `"transformer"`, `"transform"`, `"translucent"`.

The `normalise_for_search` + `split` approach gives you exact token matching.
If you need substring matching, use Python's `in` operator:

```python
# exact token match
score = doc_tokens.count(query_token)

# substring match
score = sum(1 for tok in doc_tokens if query_token in tok)
```

Substring matching has higher recall (more results) but lower precision (more noise).
For a first implementation, exact token matching is cleaner.

---

## 8. Simple scoring

Once you have normalized tokens for both the query and each document, scoring is straightforward.

**Term frequency score**: count how many times each query term appears in the document.

```python
def score_document(query_tokens: list[str], doc_tokens: list[str]) -> int:
    return sum(doc_tokens.count(term) for term in query_tokens)
```

For the query `["attention", "mechanism"]` and a document containing `"attention"` 8 times and `"mechanism"` 3 times, the score is `11`.

This is the simplest possible ranking.
Its weakness: a 500-word abstract with 8 occurrences of `"attention"` may score lower than a 5000-word full paper with 50 occurrences.
In this simple system, that is acceptable.

More advanced scoring (like TF-IDF) accounts for document length and rarity of terms.
That is a natural extension for a stretch exercise.

---

## 9. The KeywordSearchService

Here is the actual implementation from the codebase:

```python
class KeywordSearchService:
    def __init__(self, paper_repo: PaperRepository) -> None:
        self._repo = paper_repo

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        query = query.strip()
        if not query:
            raise EmptyQueryError()

        terms = normalise_for_search(query).split()
        papers = self._repo.list_all()
        results: list[SearchResult] = []

        for paper in papers:
            haystack = normalise_for_search(paper.title + " " + paper.text)
            score = sum(haystack.count(term) for term in terms)
            if score > 0:
                snippet = self._extract_snippet(paper.text, terms)
                results.append(SearchResult(paper=paper, score=float(score), snippet=snippet))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]
```

Let us trace through each line.

`query = query.strip()` — Removes leading and trailing whitespace.
A query like `"  transformers  "` becomes `"transformers"`.

`if not query: raise EmptyQueryError()` — An empty query is an error, not a valid search.
This prevents loading all papers for no reason and gives the user a clear error.

`terms = normalise_for_search(query).split()` — Normalizes and tokenizes the query.
`"Transformer Models!"` becomes `["transformer", "models"]`.

`papers = self._repo.list_all()` — Loads all papers from the database.
This is an in-memory search implementation.
It does not use SQLite's full-text search features.
For small databases (hundreds of papers), this is fast enough.
For large databases (thousands), you would want to push the search into SQL.

`haystack = normalise_for_search(paper.title + " " + paper.text)` — Prepends the title.
Title matches are treated the same as body text matches.
(You could boost title matches by scoring them separately and multiplying by a factor.)

`score = sum(haystack.count(term) for term in terms)` — Counts total occurrences of all query terms.
`str.count()` is an exact substring count.
It is efficient on Python's built-in string type.

`if score > 0:` — Only papers with at least one term match are included.
Papers with `score = 0` are not added to results.

`results.sort(key=lambda r: r.score, reverse=True)` — Sorts by score descending.
Highest score first.

`return results[:limit]` — Returns at most `limit` results.
Default is 10.

---

## 10. Snippet extraction

A search result should show more than a title.
A snippet gives the user a glimpse of the context where the term was found.

```python
@staticmethod
def _extract_snippet(text: str, terms: list[str], context: int = 80) -> str:
    lower = text.lower()
    for term in terms:
        idx = lower.find(term)
        if idx >= 0:
            start = max(0, idx - context)
            end = min(len(text), idx + len(term) + context)
            snippet = text[start:end].replace("\n", " ")
            return f"…{snippet}…" if start > 0 else f"{snippet}…"
    return text[:160]
```

`lower = text.lower()` — Lowercases the full text for case-insensitive finding.
We do NOT normalize it (no punctuation removal) so the snippet shows readable text.

`idx = lower.find(term)` — Finds the first occurrence of the term.

`start = max(0, idx - context)` — Go `context` characters before the match.
`max(0, ...)` prevents going before the start of the string.

`end = min(len(text), idx + len(term) + context)` — Go `context` characters after the match.
`min(len(text), ...)` prevents going past the end.

`snippet = text[start:end].replace("\n", " ")` — Use the ORIGINAL text (not lowercased) for display.
Replace newlines with spaces so the snippet shows on one line.

`return f"…{snippet}…" if start > 0 else ...` — The leading ellipsis indicates the snippet is not the beginning of the text.

---

## 11. The SearchResult model

From `core/models.py`:

```python
@dataclass
class SearchResult:
    paper: Paper
    score: float
    snippet: str = ""
```

`SearchResult` carries:
- The full `Paper` object (so the CLI can display any field).
- The relevance score (for sorting and display).
- A short snippet (for preview).

The `score` is a `float` even though the current implementation produces integers.
Keeping it as `float` allows future ranking functions (like TF-IDF) to use decimal scores without changing the type.

---

## 12. Hashing and duplicate detection

### Why duplicates are a problem

Imagine you accidentally run the ingestion twice on the same directory with `skip_existing=False`.
Now you have duplicate papers.
When a user searches for `"transformer"`, they get the same paper returned twice at the same score.
This is confusing and looks like a bug.

More subtly: what if someone uploads the same PDF under two different filenames?
`paper_v1.pdf` and `paper_final.pdf` may be identical files.
The path-based ID system treats them as different papers.

Content-based deduplication uses the file's actual bytes to detect identical content.

### SHA-256 conceptually

SHA-256 is a **hash function**.
A hash function takes an input (any sequence of bytes) and produces a fixed-length output (a "digest" or "hash").

For SHA-256, the output is always exactly 256 bits (64 hexadecimal characters), regardless of input size.

Key properties:
- **Deterministic**: the same input always produces the same hash.
- **Avalanche effect**: changing one bit in the input completely changes the hash.
- **One-way**: you cannot reconstruct the input from the hash.
- **Collision resistant**: it is computationally infeasible to find two different inputs that produce the same hash.

SHA-256 is NOT encryption.
You cannot decrypt it.
It is a fingerprint: a way to uniquely identify content.

### Using SHA-256 for deduplication

```python
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hex digest of a file's contents."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(65536):  # Read in 64 KB chunks
            h.update(chunk)
    return h.hexdigest()
```

Line by line:

`h = hashlib.sha256()` — Creates a new SHA-256 hash object.
It starts with no data.

`path.open("rb")` — Opens the file in binary mode (`rb`).
All files are bytes at the lowest level.
Binary mode avoids any text encoding translation.

`while chunk := fh.read(65536):` — The walrus operator (`:=`) reads 65536 bytes and assigns to `chunk`.
The `while` loop continues as long as `chunk` is non-empty (more data to read).
Reading in chunks avoids loading a 50 MB PDF entirely into RAM.

`h.update(chunk)` — Feeds the chunk to the hash computation.
SHA-256 is computed incrementally.

`return h.hexdigest()` — Returns the final hash as a 64-character hex string.

Two identical files produce the same SHA-256 digest.
Two different files (with any difference at all) produce completely different digests.

### How hashing connects to PaperId

Look at `PaperId.from_path` in `core/models.py`:

```python
@classmethod
def from_path(cls, path: Path) -> PaperId:
    digest = hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]
    return cls(value=digest)
```

This hashes the **path string**, not the file contents.
It is a path-based ID, not a content-based ID.

The advantage: it is fast (no need to read the file) and stable across program runs.
The limitation: two files with different paths but identical content get different IDs.

A content-based ID would use `sha256_file(path)` instead:

```python
digest = sha256_file(path)[:16]
```

This would detect identical content under different filenames.
That is a meaningful improvement for deduplication, but it requires reading the entire file on every ingestion check.

---

## 13. Data quality

Data quality is the degree to which your stored data is accurate, complete, and consistent.
Poor data quality is the hidden enemy of search systems.

### Common data quality problems in ResearchOps

**Empty text:** A PDF was ingested but `text = ""` or `text` is only whitespace.
This happens for image-only PDFs that `pypdf` cannot extract from.
Stored, but useless for search.

**Extremely short text:** A paper with `word_count() < 50` may have had extraction problems.
A 20-page paper with 40 words is suspicious.

**Repeated boilerplate:** Some PDFs repeat headers and footers on every page.
The extracted text becomes `"Page 1 of 50 - Journal of AI"` repeated 50 times, diluting the actual content.

**Garbled Unicode:** Some PDF fonts use non-standard encoding.
The extracted text looks like `"Tùéánsformer"` instead of `"Transformer"`.

**Wrong title:** The metadata title may say `"Microsoft Word - paper.docx"` instead of the actual paper title.

### Detecting quality problems

```python
from researchops.core.models import Paper


def quality_check(paper: Paper) -> list[str]:
    """Return a list of quality warnings for a paper."""
    warnings = []

    if paper.is_empty():
        warnings.append("No text extracted")

    elif paper.word_count() < 100:
        warnings.append(f"Very short text: only {paper.word_count()} words")

    if paper.title == "Untitled":
        warnings.append("Could not extract title from metadata or text")

    # Check for repetitive content (high ratio of repeated lines)
    lines = paper.text.splitlines()
    if lines:
        unique_ratio = len(set(lines)) / len(lines)
        if unique_ratio < 0.3:
            warnings.append("High line repetition — possible boilerplate")

    return warnings
```

### The stats command

A `stats` command gives you a bird's-eye view of data quality:

```python
def compute_stats(repo: PaperRepository) -> dict:
    papers = repo.list_all()
    failures = repo.list_failures()

    total_words = sum(p.word_count() for p in papers)
    empty_papers = [p for p in papers if p.is_empty()]
    short_papers = [p for p in papers if not p.is_empty() and p.word_count() < 100]

    return {
        "total_papers": len(papers),
        "total_failures": len(failures),
        "total_words": total_words,
        "average_words": total_words / len(papers) if papers else 0,
        "empty_papers": len(empty_papers),
        "short_papers": len(short_papers),
    }
```

Running `researchops stats` should show you immediately whether your database is healthy.

---

## 14. Connecting to previous weeks

This week builds on both Week 5 and Week 6.

**From Week 5 (storage):**
`KeywordSearchService` calls `self._repo.list_all()`.
This method was implemented in Week 5.
Without the storage layer, there is nothing to search.

**From Week 6 (pipeline):**
The text stored by the ingestion pipeline is what gets searched.
If Week 6 stored clean, complete text, Week 7 search will work well.
If Week 6 stored empty or garbled text, Week 7 search will return bad results.
This is the direct relationship between data quality and search quality.

---

## 15. Why RAG will fail later without good search now

Month 4 introduces Retrieval-Augmented Generation (RAG).
RAG works by:
1. Searching for the most relevant documents for a query.
2. Passing those documents as context to a language model.
3. Generating a response based on that context.

If your search (step 1) returns low-quality or irrelevant documents, the language model gets bad context.
Garbage in, garbage out.

The specific failure modes:
- **Empty retrieved documents**: if search returns papers with empty text, the LLM has nothing to work with.
- **Wrong papers retrieved**: if normalization is inconsistent, relevant papers may score 0 and be excluded.
- **Duplicate results**: if data deduplication failed, the same paper appears 3 times in the context, wasting tokens and producing confused answers.

Investing in search quality and data quality now directly improves the quality of AI-powered features in Month 4.

---

## 16. Testing search

Search tests need to be deterministic.

**Test exact ranking:**
```python
def test_search_ranks_higher_frequency_first(tmp_path):
    repo = SQLitePaperRepository(tmp_path / "test.db")

    # paper_a: "transformer" appears 10 times
    paper_a = Paper(
        id="a1",
        title="Transformers",
        source_path="a.pdf",
        text="transformer " * 10,
        num_pages=1, file_size_bytes=100,
        created_at=datetime.utcnow(),
    )

    # paper_b: "transformer" appears 2 times
    paper_b = Paper(
        id="b1",
        title="Transformers",
        source_path="b.pdf",
        text="transformer " * 2,
        num_pages=1, file_size_bytes=100,
        created_at=datetime.utcnow(),
    )

    repo.save(paper_a)
    repo.save(paper_b)

    service = KeywordSearchService(repo)
    results = service.search("transformer")

    assert results[0].paper.id == "a1"  # higher frequency first
    assert results[1].paper.id == "b1"
```

**Test empty query:**
```python
def test_empty_query_raises(tmp_path):
    repo = SQLitePaperRepository(tmp_path / "test.db")
    service = KeywordSearchService(repo)
    with pytest.raises(EmptyQueryError):
        service.search("   ")
```

**Test no matches:**
```python
def test_no_matches_returns_empty_list(tmp_path):
    repo = SQLitePaperRepository(tmp_path / "test.db")
    service = KeywordSearchService(repo)
    # (no papers saved)
    results = service.search("quantum entanglement")
    assert results == []
```

---

## 17. Review questions and self-checks

**Conceptual questions:**

1. What is normalization?
   Give an example of two strings that are different before normalization but equal after.

2. Why does keyword search come before semantic/vector search in the curriculum?

3. What are stopwords?
   Give five examples.
   Why might removing them sometimes be harmful?

4. What is term frequency?
   What is its weakness as a relevance metric?

5. What does SHA-256 do?
   Is SHA-256 encryption?
   Explain the difference.

6. What is the "avalanche effect" in hash functions?

7. What is the difference between a path-based paper ID and a content-based paper ID?
   When would you choose each?

8. List four data quality problems that can affect search results.

9. Why does RAG quality depend on search quality?

**Code-reading questions:**

10. Look at `normalise_for_search` in `parsing/text_cleaner.py`.
    What happens to the string `"ﬁeld trials (2023)"` after each step?

11. Look at `KeywordSearchService.search`.
    What happens when `query = ""`?
    Trace through the code.

12. In `_extract_snippet`, why is `text` (not `lower`) used for the final snippet?

**Design questions:**

13. The current search loads ALL papers for every query.
    If the database had 10,000 papers, how would you improve this?
    Name two approaches (hint: SQLite FTS5, inverted index).

14. You want title matches to count twice as much as body text matches.
    What change would you make to the scoring function?

15. A user searches for `"ml"` and gets no results, but they expected papers about machine learning.
    What is the root cause?
    How would you fix this with query expansion?

**Practice tasks:**

16. Trace `normalise_for_search("The BERT Model: Pre-training of Deep Bidirectional Transformers")` step by step.
    What is the final output?

17. Compute the score for query `"deep learning"` against a document containing `"deep learning deep neural networks"`.
    Show your working.

18. Write a function that detects if two `Paper` objects have identical content (ignoring IDs and paths).
    Use SHA-256 on `paper.text`.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
