# Week 13 - Embeddings and Semantic Search

## Learning objectives
- Understand how embeddings represent text as vectors.
- Chunk long documents into searchable segments.
- Compute cosine similarity for nearest-neighbor retrieval.
- Compare semantic search with keyword search.
- Store chunk metadata and embedding vectors.
- Build a first semantic retrieval path for ResearchOps.
- Evaluate semantic results qualitatively.

## Project milestone
Add chunked embeddings and semantic search so ResearchOps can retrieve conceptually similar passages, not only exact keyword matches.

## Files to modify/create
- `src/researchops/semantic/chunking.py`
- `src/researchops/semantic/embeddings.py`
- `src/researchops/semantic/search.py`
- `tests/unit/test_chunking.py`
- `tests/unit/test_semantic_search.py`
- `tests/integration/test_semantic_retrieval.py`

## Concepts covered
Chunking, vector representations, cosine similarity, semantic retrieval, embedding storage, and relevance comparison.

## Expected deliverables
- A chunking strategy for parsed documents.
- An embedding generation interface or implementation.
- Semantic search returning top-k chunks with similarity scores.
- Tests for chunking and retrieval behavior.

## Definition of done
- [ ] Chunking is implemented and tested.
- [ ] Embeddings are generated or faked behind an interface.
- [ ] Cosine similarity ranking works.
- [ ] Semantic search returns chunk-level hits.
- [ ] Metadata links chunks back to source documents.
- [ ] Integration test covers indexing and retrieval.
- [ ] You can explain when semantic search beats keyword search.
