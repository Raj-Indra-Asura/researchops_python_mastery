# Week 13 - Embeddings and Semantic Search

## Learning objectives
- Understand why keyword search fails on synonyms and paraphrases.
- Explain what an embedding is and why similar texts have similar vectors.
- Understand vector dimensions and cosine similarity intuitively and mathematically.
- Chunk long documents with configurable size and overlap.
- Attach metadata to every chunk so retrieval results trace back to sources.
- Implement cosine similarity from scratch.
- Use `FakeEmbeddingModel` to write fast, offline, deterministic tests.
- Install and use `sentence-transformers` for local embeddings.
- Build an indexing and query pipeline for semantic top-k retrieval.
- Understand the local model vs. API embedding tradeoff.
- Know that good retrieval is the foundation of RAG systems.

## Project milestone
Add chunked embeddings and semantic search so ResearchOps can retrieve conceptually similar passages, not only exact keyword matches.

## Files to modify or create
- `src/researchops/search/chunking.py`
- `src/researchops/search/embeddings.py`
- `src/researchops/search/vector_search.py`
- `tests/unit/test_chunking.py`
- `tests/unit/test_semantic_search.py`
- `tests/integration/test_semantic_retrieval.py`

> **Note:** these files are in `src/researchops/search/`, not `src/researchops/semantic/`.

## Concepts covered
Embeddings, vector dimensions, cosine similarity, chunking, chunk overlap, chunk metadata, embedding interface, fake embedder, embedding cache, top-k retrieval, local vs. API models, retrieval quality, RAG foundation.

## Expected deliverables
- `chunk_text` with validation, returning chunk metadata.
- `EmbeddingModel` protocol and `FakeEmbeddingModel`.
- `cosine_similarity` function.
- `search` function returning `SearchHit` objects.
- Unit tests for chunking, cosine similarity, and top-k ranking.
- Integration test for the full index-and-query pipeline.

## Definition of done
- [ ] `chunk_text` is implemented, tested, and raises on invalid overlap.
- [ ] Every chunk carries `source_id`, `chunk_index`, and `start_word`.
- [ ] `EmbeddingModel` protocol exists.
- [ ] `FakeEmbeddingModel` is used in all unit tests.
- [ ] `cosine_similarity` handles zero vectors and mismatched lengths.
- [ ] Top-k search returns `SearchHit` objects with `score` and `source_id`.
- [ ] Integration test indexes multiple documents and queries across them.
- [ ] `pytest -q` passes.
- [ ] `ruff check src tests` passes.
- [ ] You can explain the cosine similarity formula without looking it up.
