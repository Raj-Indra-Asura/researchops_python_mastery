# Exercises — Week 07 Keyword Search and Data Quality

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › [Week 7 — Keyword Search & Data Quality](./README.md) › **exercises.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

---

## Easy exercises

### E1 — Normalize a string manually

Apply each normalization step manually to `"  The BERT Model: Pre-Training of Transformers!  "`.
Show the string after each step:
1. Unicode NFKC normalization.
2. Lowercase.
3. Punctuation removal.
4. Whitespace collapse.

What is the final string?

### E2 — Count term frequency

Given `doc = "the cat sat on the mat the cat"`, count how many times each of these terms appears:
- `"cat"` → ?
- `"the"` → ?
- `"dog"` → ?

Write the count using `doc.split().count("cat")`.

### E3 — Simple scorer

Write a function `score(query: str, document: str) -> int` that:
1. Normalizes both inputs with `normalise_for_search`.
2. Splits into tokens.
3. Returns the sum of query-term counts in the document.

Test with:
- `score("transformer attention", "transformer models use attention mechanisms")` → should be 2.
- `score("quantum", "deep learning paper")` → should be 0.

### E4 — Handle empty query

Write a wrapper for your scorer that raises a `ValueError` if the query is empty or whitespace-only.
Write a test for it.

### E5 — Build a snippet

Given `text = "Attention mechanisms allow models to focus on relevant parts of the input sequence."` and `term = "attention"`, write code that returns a snippet of 40 characters around the first occurrence.

### E6 — Unicode normalization demonstration

Run this in a Python REPL:
```python
import unicodedata
s = "ﬁeld"  # fi-ligature
print(s, len(s))  # one character for ﬁ
normalized = unicodedata.normalize("NFKC", s)
print(normalized, len(normalized))  # two characters: f + i
```

Confirm that `"ﬁeld" != "field"` but `unicodedata.normalize("NFKC", "ﬁeld") == "field"`.

---

## Medium exercises

### M1 — Implement normalise_for_search

Implement the full `normalise_for_search(text: str) -> str` function from scratch.
Do not look at the existing implementation first.
Then compare yours to `parsing/text_cleaner.py`.

Write tests for:
- Empty string returns empty string.
- Uppercase is lowercased.
- Punctuation is removed.
- Multiple spaces become one space.
- Unicode ligatures are normalized.
- Leading and trailing whitespace is stripped.

### M2 — Implement keyword search

Implement `KeywordSearchService` from scratch:
1. Accept a `PaperRepository` in `__init__`.
2. Implement `search(query, limit)` that:
   - Raises `EmptyQueryError` for blank queries.
   - Normalizes the query.
   - Loads all papers.
   - Scores each paper.
   - Returns top `limit` results ordered by score.

Write tests for:
- Empty query raises error.
- No-match query returns empty list.
- Query with one matching paper returns one result.
- Query with two papers returns higher-scoring paper first.

### M3 — Snippet extraction

Implement `_extract_snippet(text, terms, context=80) -> str`.
The snippet should:
- Find the first occurrence of any term (case-insensitive).
- Return text starting from `context` characters before and ending `context` characters after.
- Add `"…"` at the start if the match is not at position 0.
- Add `"…"` at the end always.
- Replace newlines with spaces.

Write tests:
- Term at start of text: no leading `"…"`.
- Term in middle of text: leading `"…"`.
- No matching term: return first 160 characters.

### M4 — Data quality checker

Implement `quality_check(paper: Paper) -> list[str]` that returns warnings for:
- Empty text.
- Word count below 100.
- Title is `"Untitled"`.
- More than 70% of lines are identical (boilerplate repetition).

Write tests for each warning condition.

### M5 — Stats command

Implement `compute_stats(repo: PaperRepository) -> dict` that returns:
- `total_papers`
- `total_failures`
- `total_words`
- `average_words_per_paper`
- `papers_with_empty_text`
- `papers_with_short_text` (< 100 words)

Write a test that populates a database with 5 papers of varying lengths and verifies the stats.

### M6 — SHA-256 file hashing

Implement `sha256_file(path: Path) -> str` that:
1. Opens the file in binary mode.
2. Reads in 64 KB chunks.
3. Returns the hex digest.

Write tests:
- Two files with identical content produce the same hash.
- Files with any difference produce different hashes.
- Empty file produces a known hash (look it up: SHA-256 of empty input is `e3b0c44298fc1c14...`).

---

## Hard exercises

### H1 — Title-boosted scoring

Modify your search to count title matches separately.
Implement a scoring strategy where title matches count as 5 points each and body text matches count as 1 point each.

Write tests that:
- A paper with the query term only in the title outscores a paper with the term appearing once in the body.
- A paper with the term 10 times in the body outscores one with it once in the title.
  (i.e., enough body matches can overcome the title boost)

### H2 — Stopword filtering

Create a small stopword list: `{"the", "a", "an", "is", "are", "in", "of", "and", "to", "for", "with"}`.

Implement `remove_stopwords(tokens: list[str]) -> list[str]` that filters out stopwords.

Write tests:
- All stopwords removed from a token list.
- Non-stopwords preserved.
- Empty list returns empty list.

Discuss in comments: what breaks if you remove stopwords from the query `"is this paper good"`?

### H3 — Full-text search using SQLite FTS5

SQLite has a built-in full-text search extension called FTS5.
Research how to:
1. Create a virtual FTS5 table.
2. Insert rows into it.
3. Query it with `MATCH`.

Implement a `FTS5SearchService` that:
1. Creates a virtual table `papers_fts` during initialization.
2. Indexes papers when they are saved.
3. Queries using FTS5's `MATCH` operator.

Compare the performance and results of `FTS5SearchService` vs `KeywordSearchService` on 100 papers.

### H4 — Deduplication detection

Implement a `DuplicateDetector` that:
1. Computes SHA-256 of each paper's text.
2. Groups papers by hash.
3. Returns groups that have more than one member.

Write a test that:
1. Creates 5 papers, 2 of which have identical text (but different IDs and paths).
2. Runs `DuplicateDetector`.
3. Asserts exactly one duplicate group is found with 2 members.

### H5 — Search result pagination

Add `offset: int = 0` to the `search` method signature.
Return results starting from `offset`, up to `limit`.

Write tests for:
- `offset=0, limit=5` returns first 5 results.
- `offset=5, limit=5` returns next 5 results.
- `offset` beyond total results returns empty list.

---

## Brutal exercises

### B1 — Full test suite for search

Write `tests/unit/test_keyword_search.py` with at least 15 tests covering:
- Empty query error.
- No-match returns empty list.
- Single-term query ranks by frequency.
- Multi-term query.
- Case-insensitive matching.
- Unicode normalization (fi-ligature).
- Score ordering (highest first).
- Limit parameter.
- Title content is searchable.
- Snippet contains matched term.
- Snippet at start of text (no leading ellipsis).
- Snippet in middle of text (with leading ellipsis).
- Quality check for empty paper.
- Quality check for short paper.
- Stats calculation with known data.

### B2 — Benchmarking search

Write a benchmark script that:
1. Populates a database with 500 papers (generate synthetic text with varying lengths).
2. Runs 20 different queries.
3. Times each query.
4. Reports average and maximum query latency.

Discuss in comments: at what paper count would this in-memory approach become unacceptably slow?
What is your estimate?

### B3 — Complete stats command

Implement `researchops stats --db researchops.db` that prints:
```
Database: researchops.db
Papers: 42
  - With text: 39
  - Empty: 3
  - Short (< 100 words): 5
  - Average words: 4523
Failures: 7
  - Most common error: ParsingError (5 times)
Quality warnings: 8 papers flagged
```

Write integration tests for the command output.

---

## Written explanation exercises

### W1 — Explain normalization to a non-technical person

Write a paragraph that explains why `"Transformer"` and `"transformer"` should match in a search system.
Use an everyday analogy (e.g., a phone book, a library catalog).

### W2 — Explain hashing

Write a short explanation of SHA-256 using an analogy.
The explanation should cover:
- What goes in.
- What comes out.
- Why the same input always gives the same output.
- Why different inputs give different outputs.
- Why it is not encryption.

Do NOT use any math or binary representation.

### W3 — Data quality reflection

Write a paragraph describing the data quality problem you would most expect to encounter with ResearchOps.
Which specific aspect of PDF parsing creates it?
How would you detect it?
How would you fix it?

---

## Testing exercises

### T1 — Test normalization idempotency

```python
def test_normalise_is_idempotent():
    text = "Attention Is All You Need"
    once = normalise_for_search(text)
    twice = normalise_for_search(once)
    assert once == twice
```

Applying normalization twice should give the same result as applying it once.

### T2 — Test search is case-insensitive

```python
def test_search_is_case_insensitive(repo, paper_with_transformer_text):
    service = KeywordSearchService(repo)
    results_lower = service.search("transformer")
    results_upper = service.search("TRANSFORMER")
    assert len(results_lower) == len(results_upper)
```

### T3 — Test search with multi-word query

```python
def test_multi_word_query_aggregates_scores(tmp_path):
    # Create a paper where "attention" appears 5 times and "mechanism" appears 3 times
    # Score for query "attention mechanism" should be 8
    ...
```

---

## Debugging exercises

### D1 — Trace a zero-score mystery

A paper contains the word `"transformers"` (plural).
A user queries for `"transformer"` (singular).
The score is 0.
No result is returned.

Explain why this happens with the current implementation.
What is the fix?
(Hint: stemming. But for now, explain the problem and the tradeoff of fixing it with substring matching.)

### D2 — Boilerplate detection

Create a paper where every page's footer `"ResearchOps - Confidential"` was extracted and repeated 30 times.
Run `quality_check` on it.
Does the repetition warning trigger?
Verify by printing the `unique_ratio` calculation.

### D3 — Snippet debugging

Create a paper where the query term appears only at position 10000 (near the end of a long text).
Inspect the snippet.
Is it correct?
Does the `"…"` appear?

---

## Mini project task

### P1 — Search milestone

Complete the keyword search feature for ResearchOps:

1. Verify `parsing/text_cleaner.py` has the full `normalise_for_search` function.
2. Implement or verify `services/search_service.py` (KeywordSearchService).
3. Verify `cli/commands/search.py` accepts `"query"` and `--db`.
4. Implement `researchops stats --db` to show data quality summary.
5. Write `tests/unit/test_keyword_search.py` with at least 10 tests.
6. Run `pytest -k search` and confirm tests pass.
7. Run `researchops search "attention mechanism" --db /tmp/test.db` after ingesting sample papers.
8. Inspect the results and note any data quality issues.
9. Write one improvement to normalization or scoring based on what you observed.

Deliverable: a working search command with quality reporting.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 7 — Keyword Search & Data Quality** · *exercises.md — the workbook* (step 3 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [notes.md](./notes.md)
- ▶ **Next:** [break_it.md](./break_it.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. **➡ [exercises.md](./exercises.md) ← you are here**
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 8](../../../curriculum/month-02-data-storage-concurrency/week-08-multiprocessing-ingestion/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 8 — Multiprocessing Ingestion](../../../curriculum/month-02-data-storage-concurrency/week-08-multiprocessing-ingestion/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 2 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 2 overview](../README.md) · [📄 Week 7 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
