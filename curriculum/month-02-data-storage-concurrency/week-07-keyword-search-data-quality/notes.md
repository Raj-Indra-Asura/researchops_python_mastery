<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 07 Notes — Keyword Search and Data Quality

## 1. Chapter overview
In Weeks 5 and 6 you built a system that can ingest PDFs and store them in a database.
Now you have papers.
But having papers is not enough.
You need to be able to find them.

This week you build keyword search.

Keyword search is not glamorous.
It is not a future advanced retrieval system; it is direct word matching.
But it is the foundation that every more sophisticated search system is built on top of.
Understanding keyword search teaches you to think about text as data, normalization as a prerequisite, and ranking as a tunable function.

You also learn something equally important: **data quality**.
If the text in your database is noisy, inconsistent, or empty, search will be poor no matter how clever your algorithm is.
This week you learn to measure and improve data quality as part of the engineering process.

By the end of this week, `researchops search "query"` will return ranked results from your database.

---

The unified chapter you are reading replaces the previous two-part format.
There is no separate learning-format preface and no older-notes wrapper; this is one continuous beginner chapter.
The syllabus title is **Finding signal in stored text**.
The project milestone is `researchops search "transformer attention"` returning ranked results from stored papers.
The validation thread also includes `researchops papers stats`, because search quality depends on stored-data quality.
This week is intentionally ordinary keyword search and data-quality checking, not future-week retrieval or concurrency work.
Ordinary keyword search is the baseline that later AI features must be able to beat and explain.

## 2. What you already know from previous weeks
- Week 1 gave you the repository scaffold, package layout, and first CLI habits.
- Week 2 made paths, exceptions, and logging part of normal development rather than afterthoughts.
- Week 3 introduced domain modeling, so `Paper` and `SearchResult` should be meaningful objects instead of loose dictionaries.
- Week 4 established that CLI commands should be thin and should delegate workflow decisions to services.
- Week 5 introduced SQLite storage and the repository pattern, so services can ask for papers without knowing SQL details.
- Week 6 introduced PDF parsing and showed that extracted text can be clean, empty, garbled, repeated, or incomplete.
- You already know that `core/` must not depend on infrastructure layers.
- You already know that fake repositories make unit tests fast and focused.
- You already know that user-facing commands need clear errors for normal failure states.
- You already know that validation commands are evidence, not ceremony.

Week 7 combines those ideas: stored papers from Week 5 and parsed text from Week 6 become searchable through a service boundary.
- Previous-week connection for **In-memory inverted index basics**: a mapping from terms to papers, introduced conceptually before more advanced storage-backed search, but implemented using only concepts available through Week 7.
- Previous-week connection for **Text normalisation**: consistent lowercasing, Unicode cleanup, punctuation handling, and whitespace cleanup before comparison, but implemented using only concepts available through Week 7.
- Previous-week connection for **Basic scoring and ranking**: a visible rule that counts matches and sorts higher scores first, but implemented using only concepts available through Week 7.
- Previous-week connection for **Data quality gates**: checks that reveal empty, short, duplicated, or suspicious stored papers before search output is trusted, but implemented using only concepts available through Week 7.
- Previous-week connection for **SearchService and SearchResult domain objects**: service workflow plus a domain object carrying paper, score, and snippet, but implemented using only concepts available through Week 7.

## 3. What problem this week solves
ResearchOps can store papers, but storage alone does not help a learner find a useful paper quickly.
A paper library without search forces users to remember filenames, IDs, or ingestion order.
Keyword search solves the first retrieval problem: compare a user query against stored title/body text and return the strongest matches first.
Data-quality checks solve the trust problem: they reveal when stored data is too empty, short, suspicious, or inconsistent to support good retrieval.
A natural question is: why not skip keyword search and jump to a later retrieval technique?

The answer is that later retrieval techniques require your data to be clean and complete first.

If 30% of your PDFs extracted no useful text, any later retrieval layer will be built on missing data.
If titles are garbled and abstract fields are empty, later retrieval cannot use information that does not exist.

Keyword search forces you to confront data quality directly.
When a search for `"transformer architecture"` returns nothing from a paper you know discusses transformers, the bug is often in the data pipeline, not the search algorithm.
Fixing the data makes all downstream retrieval and analysis systems better.

This is also why ResearchOps implements search in this order:
1. Week 7: keyword search (forces data quality)
2. Later retrieval work builds on clean data.

---

Four practical user questions drive this week:
- Can I find papers that mention this topic?
- Why did this paper rank above another paper?
- Why did a known paper fail to appear?
- Is my stored library healthy enough to search?

## 4. Beginner mental model
Search is comparison plus ordering.
Comparison asks whether a paper contains the query terms after both sides are made comparable.
Ordering asks which matching paper should appear first.
Data quality asks whether the stored paper text is trustworthy enough for either answer to matter.

Trace the Week 7 flow as twelve small steps:
- User enters a query.
- CLI passes the query to a service.
- Service strips whitespace.
- Service rejects a blank query.
- Query is normalized.
- Query becomes terms.
- Repository provides stored papers.
- Each paper title and text become a haystack.
- Each haystack receives a score.
- Positive-score papers become SearchResult objects.
- Results are sorted by score descending.
- CLI displays results and stats in a human-readable way.

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

## 5. Core vocabulary
- **Keyword search:** search that matches words or text fragments directly, without learned meaning.
- **Query:** the text the user asks the system to search for.
- **Document:** one searchable item; in ResearchOps this is usually a stored `Paper`.
- **Corpus:** the full set of searchable papers.
- **Normalization:** turning text into a consistent form before comparison.
- **Tokenization:** splitting normalized text into searchable terms.
- **Stopword:** a very common word such as `the`, `of`, or `and` that may carry little search meaning.
- **Score:** a number representing match strength.
- **Ranking:** sorting search results by score or another relevance rule.
- **Snippet:** a short preview showing matching context.
- **Inverted index:** a structure mapping terms to documents that contain them.
- **SQLite LIKE:** basic SQL pattern matching over stored text.
- **SQLite FTS:** SQLite full-text search support for keyword-style text search.
- **Data quality gate:** a check that reports suspicious data before downstream features trust it.
- **Fake repository:** an in-memory test double that implements repository behavior.
- **Protocol:** an interface describing methods an object must provide.
- **Boundary:** a responsibility line between core, services, CLI, and infrastructure.

## 6. Concept explanations from first principles
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

**Stopwords** are very common words that carry little meaning for search purposes: `the`, `a`, `is`, `are`, `in`, `of`, `and`, `to`.

The idea is that a query like `"what is a transformer"` should match on `"transformer"`, not on `"what"`, `"is"`, `"a"`.

The week-07 implementation does not remove stopwords.
That is an intentional simplification.
Removing stopwords requires a curated list and can cause unexpected behavior (imagine searching for the paper `"Is This a Good Algorithm?"` — removing stopwords strips almost the entire query).

For a first implementation, keyword matching without stopword removal is fine.
Stopword removal is a meaningful stretch exercise.

---

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

### SQLite LIKE from first principles
SQLite `LIKE` is a simple way to ask whether one text value contains a pattern.
For example, `WHERE lower(text) LIKE "%attention%"` asks SQLite to find rows whose lowercase text contains `attention`.
This can be useful for tiny libraries, but ranking multiple terms is awkward and large text scans can become slow.
Use `LIKE` as a stepping stone, not as a magical search engine.

### SQLite FTS from first principles
SQLite FTS, usually FTS5, creates a full-text virtual table designed for keyword search.
FTS stores an index that is conceptually similar to an inverted index: terms point back to rows that contain them.
FTS is still keyword search; it indexes terms and rows rather than replacing the Week 7 scoring lesson.
Week 7 can mention FTS as the realistic storage-backed direction while still keeping the beginner implementation understandable.

### Data quality from first principles
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

## 7. ResearchOps-specific application
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

In this repository, read the Week 7 files in this order:
- `src/researchops/services/search_service.py` for query handling, scoring, ranking, and snippets.
- `src/researchops/parsing/text_cleaner.py` for `normalise_for_search`.
- `src/researchops/core/models.py` for `Paper` and `SearchResult`.
- `src/researchops/services/paper_service.py` for stored-paper stats.
- `tests/unit/test_search_service.py` for service behavior with `FakePaperRepository`.
- `tests/unit/test_paper_service.py` for paper lookup/list/stats behavior.

## 8. Code examples with line-by-line explanation
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

### Minimal query normalization walkthrough
```python
query = "  Transformer Attention!  "
query = query.strip()
terms = normalise_for_search(query).split()
```
Line by line:
- The first line creates a realistic messy query with spaces, uppercase letters, and punctuation.
- The second line removes spaces at the beginning and end so accidental typing does not change meaning.
- The third line normalizes the query and splits it into comparable terms.
- The expected terms are `transformer` and `attention`.

### Minimal quality-gate walkthrough
```python
papers = repo.list_all()
empty_papers = [paper for paper in papers if paper.is_empty()]
total_words = sum(paper.word_count() for paper in papers)
```
Line by line:
- The first line asks the repository for stored papers without caring whether storage is fake or SQLite.
- The second line finds records that cannot support body-text search.
- The third line measures how much searchable text exists across the library.

## 9. Common beginner mistakes
- **Mistake:** Normalizing only the query and not the document.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Deleting punctuation so words get glued together.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Treating blank query and no-match query as the same state.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Putting scoring rules in CLI code.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Importing SQLite storage directly inside the service.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Forgetting that title text should be searchable.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Depending on accidental tie order in ranking tests.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Assuming term frequency is perfect relevance.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Ignoring zero-word libraries.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Introducing future retrieval features before their assigned week.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Treating SQLite FTS as something other than keyword full-text search.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Writing tests that only assert results are not empty.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Forgetting snippets are display context, not score evidence.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Changing many layers before checking stored data.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.
- **Mistake:** Skipping `researchops papers stats` after ingestion.
  **Better move:** trace one query, one paper, one score, and one test before adding complexity.

## 10. Debugging guidance
- Copy the exact failing command.
- Classify the failure as input, normalization, repository state, scoring, sorting, snippet display, CLI wiring, or data quality.
- Inspect the normalized query before changing ranking.
- Inspect stored `Paper.title` and `Paper.text` before changing search code.
- Check whether a blank query should have raised `EmptyQueryError`.
- Check whether a no-match query is valid and should return `[]`.
- Check scores as `(paper.id, score)` pairs when order surprises you.
- Use targeted unit tests before running the full suite.
- Remove temporary debug prints once the cause is understood.
- Explain the cause in one sentence before moving on.
**Conceptual questions:**

1. What is normalization?
   Give an example of two strings that are different before normalization but equal after.

2. Why does keyword search come before later retrieval work in the curriculum?

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

9. Why does later answer quality depend on search quality?

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

## 11. Design tradeoffs
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

Extra Week 7 tradeoff: in-memory scanning is easy to teach; SQLite `LIKE` is easy to write; SQLite FTS is more scalable for keyword text, but adds index maintenance concepts.

## 12. Testing implications
Tests named by the syllabus: `tests/unit/test_search_service.py` and `tests/unit/test_paper_service.py`.
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

Current real search-service tests include:
- `TestSearch.test_finds_matching_paper_by_title`
- `TestSearch.test_finds_matching_paper_by_text`
- `TestSearch.test_no_match_returns_empty`
- `TestSearch.test_empty_query_raises`
- `TestSearch.test_results_ordered_by_score_descending`
- `TestSearch.test_limit_is_respected`
- `TestSearch.test_result_has_snippet`
- `TestSearch.test_snippet_extracted_from_text`
- `TestSearchWithEmptyRepo.test_empty_repo_returns_empty_list`
- `TestExtractSnippet.test_snippet_for_term_at_start`
- `TestExtractSnippet.test_snippet_for_term_not_found`
- `TestExtractSnippet.test_snippet_uses_ellipsis_for_mid_text`
Current real paper-service tests include:
- `TestGetPaper.test_returns_paper_by_id`
- `TestGetPaper.test_raises_when_not_found`
- `TestListPapers.test_empty_when_no_papers`
- `TestListPapers.test_returns_all_saved_papers`
- `TestStats.test_empty_stats`
- `TestStats.test_counts_papers_words_pages`

## 13. Architecture implications
The Week 7 import direction remains `CLI -> Services -> Core`, with infrastructure implementing core-facing protocols.
`KeywordSearchService` should depend on `PaperRepository`, not on a concrete SQLite class.
`SearchResult` belongs in core models because it is a domain result, not terminal formatting.
If SQLite FTS is added as infrastructure later, keep FTS SQL behind a repository/search adapter boundary.
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

## 14. How this connects to AI engineering / ML research
AI engineering is not only model code.
It is also data preparation, retrieval discipline, evaluation, and repeatable debugging.
Week 7 contributes by making the stored paper corpus inspectable and searchable before any later layer depends on it.

A research workflow often starts with questions like:
- Which papers mention this method?
- Which papers discuss this dataset?
- Which papers contain this failure mode?
- Which papers have enough extracted text to be useful?
- Which records look suspicious before analysis begins?

Keyword search gives a simple baseline for those questions.
A baseline is valuable because it is easy to inspect.
If the query is `attention`, you can point at the stored text and count why a result matched.
If a result is missing, you can inspect the query normalization, the stored text, and the score.
That kind of traceability is essential in research systems because unexplained retrieval behavior can lead to bad conclusions.

Data quality is equally important.
Empty text means there is no evidence to retrieve.
Repeated boilerplate can distort frequency-based ranking.
Duplicate records can make one paper look more important than it is.
Garbled characters can hide terms that should have matched.
Weak titles can make otherwise correct results hard for a human to recognize.

This week therefore teaches an ML-engineering habit: inspect data before blaming the algorithm.
When a search result is bad, do not immediately make the scoring function more complex.
First ask whether the stored text is present, normalized, complete, and representative.
Then ask whether the scoring rule did what it promised.
Only after those checks should you consider a more advanced retrieval design.

Keyword search is also a baseline. Future retrieval work should be compared against this simple, inspectable behavior. If a later layer cannot find obvious keyword matches, it is not trustworthy yet.

## 15. Mini quizzes
1. What is the Week 7 milestone?
2. Why does keyword search come before later retrieval work?
3. What does normalization change?
4. What is the difference between a blank query and a no-match query?
5. What does `SearchResult` contain?
6. Why should the service use `PaperRepository`?
7. What is one weakness of frequency scoring?
8. What does a snippet prove and not prove?
9. What does `researchops papers stats` reveal?
10. How is SQLite FTS different from a plain Python scan?
11. Which tests prove search behavior?
12. Which tests prove paper stats behavior?
13. What data-quality issue would make search look broken?
14. Where should CLI presentation logic live?
15. What should not be implemented before its assigned future week?

## 16. Explain-it-aloud prompts
- Explain the query-to-result path.
- Explain normalization with a concrete string.
- Explain scoring for one paper.
- Explain ranking after scoring.
- Explain a no-match result.
- Explain an empty-query error.
- Explain a data-quality gate.
- Explain fake repositories.
- Explain SQLite LIKE.
- Explain SQLite FTS as keyword full-text search.
- Explain why Week 8 needs trustworthy Week 7 data.

## 17. What to memorize
- Milestone: `researchops search "transformer attention"`.
- Validation command: `researchops search "machine learning"`, `researchops papers stats`, `pytest tests/unit/test_search_service.py -v`.
- Main files: `search_service.py`, `paper_service.py`, `models.py`, `interfaces.py`.
- Blank queries raise `EmptyQueryError`.
- Results are sorted by score descending.
- `SearchResult` carries paper, score, and snippet.
- Do not add future retrieval features in Week 7.

## 18. What to understand deeply
- Search is a pipeline of small decisions, not one magical operation.
- Normalization must be consistent on query and document text.
- Scoring rules are product behavior and must be tested.
- Data quality limits search quality.
- Fakes make service tests focused; real storage belongs in integration tests.
- Architecture boundaries make debugging smaller.
- Keyword search remains useful even after later AI features exist.

## 19. What not to worry about yet
- Future retrieval representations.
- Future answer-generation templates.
- Week 8 ingestion internals beyond the high-level bridge.
- Perfect TF-IDF or BM25 ranking.
- A complete stopword policy.
- Stemming and lemmatization.
- Internet-scale indexing.
- Cloud deployment.
- Replacing SQLite.

## 20. Bridge to next week
Week 8 introduces multiprocessing ingestion.
Week 7 prepares for it by making stored text visibly useful and visibly inspectable.
Faster ingestion is only valuable if the resulting records remain searchable and trustworthy.
Carry forward the habits from this week: preserve boundaries, test service rules with fakes, inspect data quality, and avoid future-week features until the curriculum reaches them.
Before moving on, say aloud: `A user query is normalized, compared against stored paper text, scored, sorted into SearchResult objects, displayed by the CLI, and checked against paper statistics for data quality.`

### Guided tracing drills
1. Trace **tokenization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in tokenization.
2. Trace **score calculation** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in score calculation.
3. Trace **ranking** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in ranking.
4. Trace **snippet extraction** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in snippet extraction.
5. Trace **empty-query behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in empty-query behavior.
6. Trace **no-match behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in no-match behavior.
7. Trace **paper stats** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in paper stats.
8. Trace **fake repository setup** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in fake repository setup.
9. Trace **architecture boundary** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in architecture boundary.
10. Trace **normalization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in normalization.
11. Trace **tokenization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in tokenization.
12. Trace **score calculation** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in score calculation.
13. Trace **ranking** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in ranking.
14. Trace **snippet extraction** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in snippet extraction.
15. Trace **empty-query behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in empty-query behavior.
16. Trace **no-match behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in no-match behavior.
17. Trace **paper stats** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in paper stats.
18. Trace **fake repository setup** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in fake repository setup.
19. Trace **architecture boundary** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in architecture boundary.
20. Trace **normalization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in normalization.
21. Trace **tokenization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in tokenization.
22. Trace **score calculation** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in score calculation.
23. Trace **ranking** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in ranking.
24. Trace **snippet extraction** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in snippet extraction.
25. Trace **empty-query behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in empty-query behavior.
26. Trace **no-match behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in no-match behavior.
27. Trace **paper stats** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in paper stats.
28. Trace **fake repository setup** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in fake repository setup.
29. Trace **architecture boundary** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in architecture boundary.
30. Trace **normalization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in normalization.
31. Trace **tokenization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in tokenization.
32. Trace **score calculation** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in score calculation.
33. Trace **ranking** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in ranking.
34. Trace **snippet extraction** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in snippet extraction.
35. Trace **empty-query behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in empty-query behavior.
36. Trace **no-match behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in no-match behavior.
37. Trace **paper stats** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in paper stats.
38. Trace **fake repository setup** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in fake repository setup.
39. Trace **architecture boundary** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in architecture boundary.
40. Trace **normalization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in normalization.
41. Trace **tokenization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in tokenization.
42. Trace **score calculation** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in score calculation.
43. Trace **ranking** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in ranking.
44. Trace **snippet extraction** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in snippet extraction.
45. Trace **empty-query behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in empty-query behavior.
46. Trace **no-match behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in no-match behavior.
47. Trace **paper stats** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in paper stats.
48. Trace **fake repository setup** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in fake repository setup.
49. Trace **architecture boundary** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in architecture boundary.
50. Trace **normalization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in normalization.
51. Trace **tokenization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in tokenization.
52. Trace **score calculation** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in score calculation.
53. Trace **ranking** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in ranking.
54. Trace **snippet extraction** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in snippet extraction.
55. Trace **empty-query behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in empty-query behavior.
56. Trace **no-match behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in no-match behavior.
57. Trace **paper stats** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in paper stats.
58. Trace **fake repository setup** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in fake repository setup.
59. Trace **architecture boundary** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in architecture boundary.
60. Trace **normalization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in normalization.
61. Trace **tokenization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in tokenization.
62. Trace **score calculation** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in score calculation.
63. Trace **ranking** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in ranking.
64. Trace **snippet extraction** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in snippet extraction.
65. Trace **empty-query behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in empty-query behavior.
66. Trace **no-match behavior** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in no-match behavior.
67. Trace **paper stats** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in paper stats.
68. Trace **fake repository setup** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in fake repository setup.
69. Trace **architecture boundary** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in architecture boundary.
70. Trace **normalization** using one concrete query and one concrete paper.
   - Name the input value, the intermediate value, the output value, and the test that would catch a mistake in normalization.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
