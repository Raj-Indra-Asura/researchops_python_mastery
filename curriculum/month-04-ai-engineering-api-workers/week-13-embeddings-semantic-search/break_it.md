# Break It - Week 13 Embeddings and Semantic Search

## Intentional failure experiments
1. Set chunk overlap greater than chunk size and fix the bug or validation.
2. Use vectors with different lengths and inspect the similarity failure.
3. Return identical vectors for every chunk and see retrieval quality collapse.
4. Query with an empty string and define the correct behavior.
5. Forget to store chunk metadata and notice how retrieval loses traceability.

## Debugging tasks
- Print chunk counts per document.
- Inspect the top similarity scores for one query.
- Run `pytest -k semantic_search -v` after ranking changes.

## Edge cases to explore
- Very short documents.
- Extremely long documents.
- Duplicate chunks.
- Ties in similarity score.

## What did you learn?
- Which chunking choice changed results most?
- What failure should be blocked with validation?
- How will you explain semantic retrieval to a user?
