# Week 13 - Embeddings and Semantic Search

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › **Week 13 — Embeddings & Semantic Search**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 13 — Embeddings & Semantic Search** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 12 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 14](../../../curriculum/month-04-ai-engineering-api-workers/week-14-fastapi-layer/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 14 — FastAPI Layer](../../../curriculum/month-04-ai-engineering-api-workers/week-14-fastapi-layer/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 4 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 4 overview](../README.md) · [📄 Week 13 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
