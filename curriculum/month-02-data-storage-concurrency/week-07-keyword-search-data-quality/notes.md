# Notes - Week 07 Keyword Search and Data Quality

Search feels magical when it works, but under the hood even a simple keyword search depends on many small decisions. The first one is normalization: making text consistent before you compare it. If one document says `Transformer Models` and another says `transformer models`, your system should probably treat them as the same words.

A common normalization pipeline lowercases text, strips extra whitespace, and removes or standardizes punctuation.

```python
import re


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
```

This is not the only correct approach, but it gives you a predictable baseline. Predictability matters more than cleverness at first.

Tokenization means splitting text into words or tokens. For a basic system, normalized whitespace splitting is enough.

```python
def tokens(text: str) -> list[str]:
    return normalize_text(text).split()
```

A keyword search engine compares query tokens with document tokens. The simplest ranking is raw match count.

```python
def score_document(query: str, text: str) -> int:
    query_terms = tokens(query)
    doc_terms = tokens(text)
    return sum(doc_terms.count(term) for term in query_terms)
```

This is not state-of-the-art ranking, but it teaches an important lesson: ranking is a function. Once you define it clearly, you can improve it later.

Search quality is tied to data quality. If a PDF parser produces empty text, repeated headers on every page, or random broken characters, the search results will be worse. That is why engineering teams often build quality checks close to ingestion.

Useful first checks include:
- empty text after normalization
- text below a minimum length
- very high repetition of the same token
- duplicate source paths or duplicate normalized titles

A search result should return more than a raw score. It should likely include document identity and maybe a short snippet.

```python
@dataclass
class SearchHit:
    paper_id: str
    title: str
    score: int
    snippet: str
```

Even if the snippet is simple, it helps users decide whether a result is relevant.

You also need to think about where search runs. For now, it is fine to load documents from SQLite, normalize them in Python, and rank them in memory. Later you may push more work into SQL or a vector index, but starting simple is valuable.

Testing search should focus on deterministic behavior. If two documents match a query differently, your tests should confirm which one ranks first and why. Also test edge cases: empty query, no matches, punctuation-heavy text, and case differences.

Keyword search has limits. It misses synonyms, deeper meaning, and conceptual similarity. A query for `neural retrieval` may not match a paper that only says `dense semantic search`. That is okay for now. You are building an understandable baseline. Later, embeddings and semantic search will address some of those gaps.

This week trains an important ResearchOps instinct: when results look bad, inspect both the ranking logic and the underlying data. Search problems are often data problems in disguise.
