# Break It - Week 07 Keyword Search and Data Quality

## Intentional failure experiments
1. Search for a term with different capitalization before and after normalization.
2. Query with only punctuation and decide what the system should do.
3. Index a document with empty text and see how ranking behaves.
4. Create two identical documents and inspect tie behavior.
5. Add repeated boilerplate to every document and observe result pollution.

## Debugging tasks
- Print normalized query tokens and normalized document tokens.
- Log each document score for one search query.
- Run `pytest -k keyword_search -v` after changing ranking logic.

## Edge cases to explore
- No-match queries.
- One-character queries.
- Documents with Unicode punctuation.
- Multiple documents with the same score.

## What did you learn?
- Which bug came from normalization rather than ranking?
- What tie-breaking rule feels fairest?
- What quality check would you add next?
