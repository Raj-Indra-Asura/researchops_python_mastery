# Break It - Week 13 Embeddings and Semantic Search

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 13 — Embeddings & Semantic Search](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Intentional failure experiments

### 1. Infinite loop from bad overlap
Set `overlap = chunk_size` (e.g., both equal to 50) and call `chunk_text`. What happens? The `start` pointer never advances. Python will loop forever or until memory is exhausted. Add a `ValueError` guard. Write a test that catches it.

### 2. Mismatched vector lengths
Create two vectors of different lengths: `a = [1.0, 0.0]` and `b = [1.0, 0.0, 0.5]`. Call `cosine_similarity`. The `zip` silently truncates to the shorter length, producing an incorrect result with no error. Fix this: add a check that raises `ValueError` when lengths differ. Write a test.

### 3. Zero vector
Pass `a = [0.0, 0.0, 0.0]` to `cosine_similarity`. Division by zero occurs. What should the function return for a zero vector? Some systems return 0.0 similarity. Others raise. Define your convention, implement it, and write a test.

### 4. All embeddings identical
Use a fake embedder that always returns the same vector regardless of input. Index five documents. Run a query. What are the cosine similarity scores? They are all 1.0. The ranking is now determined by insertion order, not by relevance. This is a retrieval quality collapse. Observe it, then write a comment in your code documenting the assumption: the embedder must produce distinct vectors for distinct texts.

### 5. Empty query string
Call `embed("")`. What does `FakeEmbeddingModel` return? It returns `[0.0, 0.0, 0.0]` — the zero vector. Then cosine similarity with any stored vector hits the zero-division bug from experiment 3. Decide and implement: should empty queries be rejected at the search entry point with a clear error? Write a test.

### 6. Chunk index off by one
Modify `chunk_text` to start `chunk_index` at 1 instead of 0. Watch the metadata test fail. Understand how the error propagates: any code that tries to look up chunk 0 from a document now finds nothing. Always start indexes at 0 in this project and write tests that pin the first chunk to index 0.

### 7. Missing chunk metadata
Remove the `source_id` field from `SearchHit` or return `None` for it. What breaks downstream? A caller who tries to display where the hit came from now has no information. This simulates a common real-world error: search returns relevant text but no pointer back to the source. Your integration test should assert that `source_id` is non-empty on every hit.

### 8. Querying with the wrong model dimension
Generate an index using 3-dimensional fake embeddings. Then query using a 4-dimensional vector. Your cosine similarity function will silently truncate (or raise, if you added the length check). This simulates mixing models. Write a test that verifies the search function raises `ValueError` when the query embedding dimension does not match the index embedding dimension.

---

## Debugging tasks

- After chunking a 500-word document with `chunk_size=100, overlap=20`, print all chunks and verify that words at each boundary appear in both the ending and starting chunk.
- Run `pytest tests/unit/test_chunking.py -v` and inspect the failure message for each test you break deliberately.
- Add `print(f"Chunk {i}: score={score:.4f}")` inside your search function temporarily. Run a query and inspect whether scores feel plausible.

---

## Edge cases to explore

| Case | Expected behaviour |
|------|-------------------|
| Document shorter than `chunk_size` | One chunk, no overlap applied |
| Document with only whitespace | Zero chunks or one empty-string chunk (define and test) |
| `top_k=0` | Return empty list |
| `top_k` larger than index | Return all chunks sorted by score |
| Duplicate chunk texts | Both appear in index; both can be returned |
| Query text identical to a stored chunk | Score should be very close to 1.0 |

---

## What did you learn?

- Which chunking parameter mattered most for your test documents?
- Which failure was hardest to notice without a test?
- How will you explain to a user why a retrieval result is relevant even without matching words?
- What is the most dangerous assumption your current implementation makes silently?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 13 — Embeddings & Semantic Search** · *break_it.md — the failure lab* (step 4 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [exercises.md](./exercises.md)
- ▶ **Next:** [validation.md](./validation.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. **➡ [break_it.md](./break_it.md) ← you are here**
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
