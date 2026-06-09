# Exercises - Week 13 Embeddings and Semantic Search

## Warm-up exercises
1. Split a paragraph into overlapping chunks.
2. Compute cosine similarity for two tiny vectors by hand and in code.
3. Rank three vectors by similarity to a query vector.
4. Compare a semantic hit with a keyword hit for the same query.

## Project exercises
1. Implement chunking for parsed documents.
2. Add an embedder interface and a deterministic fake embedder for tests.
3. Build semantic search that returns top-k chunk hits.
4. Write integration tests for indexing documents and retrieving relevant chunks.

## Stretch exercises
1. Add chunk overlap tuning experiments.
2. Persist chunk embeddings in SQLite or artifact files.
3. Combine keyword and semantic scores into one ranking.

## Writing questions
1. Why search over chunks instead of whole documents?
2. What does cosine similarity measure intuitively?
3. Where did semantic search outperform keywords?
4. What new complexity did embeddings introduce?
