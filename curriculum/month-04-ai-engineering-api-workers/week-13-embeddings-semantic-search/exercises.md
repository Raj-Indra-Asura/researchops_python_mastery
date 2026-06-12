<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 13 Embeddings and Semantic Search

## How to use this workbook

This workbook turns the chapter into deliberate practice. Work in order unless you already know exactly why you are skipping an exercise.

For every code exercise, produce three things: the code, at least one test or manual check, and a short explanation of what the result proves.

Use real ResearchOps names: chunks, source ids, search hits, embeddings, cosine scores, and top-k results.

Do not use real sentence-transformers models in unit tests. Use deterministic fake embeddings for fast, offline checks.

Do not build Week 14 API routes, async fetchers, or deployment files here. Stay inside Week 13 retrieval work.

## Warm-up exercises

1. **Vocabulary map.** Write definitions for embedding, vector, dimension, chunk, overlap, cosine similarity, top-k, and cache key. Success: each definition mentions how the term appears in ResearchOps.

2. **Keyword failure pairs.** Create ten pairs of phrases where keyword search could miss a relevant paper, such as `dense retrieval` and `vector search`. Success: each pair includes one sentence explaining the shared meaning.

3. **Two-dimensional intuition.** Draw vectors `[1, 0]`, `[0, 1]`, and `[0.7, 0.7]` on paper. Success: you can say which pair should have the highest cosine similarity before calculating.

4. **Chunk boundary rehearsal.** Take a 45-word paragraph and chunk it by hand with `chunk_size=20` and `overlap=5`. Success: the last five words of chunk 1 become the first five words of chunk 2.

5. **Metadata rehearsal.** For three chunks from a paper id `paper-001`, write the expected `source_id`, `chunk_index`, and `start_word`. Success: chunk indexes start at 0.

6. **Score ordering rehearsal.** Given scores `0.11`, `0.94`, `0.42`, and `0.94`, write the order in which hits should appear. Success: ties are handled intentionally and higher scores appear before lower scores.

7. **Cache-key rehearsal.** Write two cache-key inputs for the same text with model names `fake-small` and `fake-large`. Success: you can explain why those keys must not collide.

## Code-reading exercises

1. **Read the chunker.** Open `src/researchops/search/chunking.py` once it exists. Mark the lines that validate `chunk_size`, validate `overlap`, create metadata, advance `start`, and stop at the end. Success: you can explain why no infinite loop occurs.

2. **Read vector scoring.** Open `src/researchops/search/vector_search.py`. Find the dot product, magnitude calculation, zero-vector behavior, sort key, and `top_k` slice. Success: you can explain the output order.

3. **Read the embedder boundary.** Open `src/researchops/search/embeddings.py`. Identify where the real model is wrapped and where caching is applied. Success: the service or CLI should not need to know local-model details.

4. **Read fake implementations.** Inspect `tests/fakes/`. Find or design the fake embedding model. Success: the fake is deterministic and does not import sentence-transformers.

5. **Read tests as a specification.** Read `tests/unit/test_chunking.py` and `tests/unit/test_vector_search.py`. Success: write three behavior promises from the test names alone.

6. **Read architecture boundaries.** Compare any semantic-search code with `ARCHITECTURE.md`. Success: you can point to the layer that owns model calls and the layer that must not import them.

7. **Read result objects.** Find the structure used for a search hit. Success: you can identify where score, source id, chunk index, and excerpt are stored.

## Implementation exercises

1. **Implement chunk metadata.** Create or update a `TextChunk` dataclass with `source_id`, `chunk_index`, `start_word`, and `text`. Produce: code plus a test that the first chunk for `paper-1` has index `0` and start word `0`.

2. **Implement chunking validation.** Add checks for positive `chunk_size`, non-negative `overlap`, and `overlap < chunk_size`. Produce: tests for each invalid case and one valid case.

3. **Implement cosine similarity.** Write the formula from scratch with length checks and zero-vector behavior. Produce: tests for identical vectors, perpendicular vectors, mismatched lengths, and zero vectors.

4. **Implement `SearchHit`.** Define a result object containing `source_id`, `chunk_index`, `text`, and `score`. Produce: a test that every returned hit has non-empty source metadata.

5. **Implement top-k search.** Score every indexed chunk, sort descending, and return `hits[:top_k]`. Produce: a test with known vectors where the expected hit order is obvious.

6. **Implement a deterministic fake embedder.** Put the fake where tests can import it, preferably under `tests/fakes/`. Produce: a test proving the same input returns the same vector twice.

7. **Implement cache behavior.** Wrap an embedder with a cache keyed by model identity and text hash. Produce: a test using a counting fake showing repeated input calls the wrapped model once.

8. **Wire the command behavior conceptually.** Sketch the data flow for `researchops semantic-search "efficient transformers"`. Produce: a short comment or note in your work log, not a committed planning file.

9. **Implement blank-query behavior.** Decide whether blank queries raise a clear error or return no hits. Produce: one test that documents the convention. Hint: validate before embedding so empty input does not become a mysterious zero vector.

10. **Implement score formatting separately.** Write a tiny formatter that displays scores to four decimal places without changing ranking logic. Produce: a sample string and a test or manual check. Success: display code does not recompute similarity.

## Testing exercises

1. **Chunk count tests.** Build inputs of 0 words, 3 words, 10 words, and 25 words. Success: expected chunk counts are documented and asserted.

2. **Overlap tests.** For `chunk_size=5` and `overlap=2`, assert that boundary words repeat exactly. Success: the test fails if `start = end` is used accidentally.

3. **Source preservation tests.** Create chunks for two source ids and search across both. Success: returned hits keep the correct source id.

4. **Sorting tests.** Give three chunks scores you can predict. Success: the highest score appears first and the lowest last.

5. **Top-k edge tests.** Test `top_k=0`, `top_k=1`, `top_k` equal to index size, and `top_k` larger than index size. Success: every behavior is intentional.

6. **Cache tests.** Use a counting fake embedder. Success: two identical requests hit the wrapped fake once; two different texts hit it twice.

7. **No-network test audit.** Search tests for `SentenceTransformer` imports. Success: unit tests do not construct the real model.

8. **Mutation safety test.** If your cache returns lists, mutate a returned vector in a test and call the cache again. Success: cached storage is not corrupted by caller mutation.

9. **Metadata round-trip test.** Build chunks, create indexed embeddings, search, and assert the top hit still references the original source. Success: metadata survives every transformation.

## Debugging exercises

1. **Break vector length checks.** Temporarily remove the length check and compare `[1, 0]` with `[1, 0, 1]`. Produce: a failing test or written explanation showing why silent truncation is dangerous.

2. **Break zero-vector handling.** Force the fake embedder to return `[0, 0, 0]` for empty text. Produce: the observed error or chosen safe behavior.

3. **Break overlap validation.** Set `overlap = chunk_size`. Produce: a description of the loop behavior and the guard that prevents it.

4. **Break sorting direction.** Sort ascending. Produce: a failing test proving the worst hit appears first.

5. **Break metadata propagation.** Drop `source_id` from `SearchHit`. Produce: a failing test showing why traceability matters.

6. **Break cache identity.** Remove the model name from the cache key. Produce: a failing test showing two model names collide for the same text.

7. **Break `top_k`.** Return all hits instead of slicing to `top_k`. Produce: a failing test where five indexed chunks and `top_k=2` return exactly two hits.

## Refactoring exercises

1. **Extract score calculation.** If `search_top_k` becomes crowded, extract a helper that creates one `SearchHit` from a query vector and indexed chunk. Success: tests still pass and names remain beginner-readable.

2. **Clarify cache keys.** Replace ad-hoc string concatenation with a small helper function such as `make_cache_key(model_name, text)`. Success: tests prove model name changes the key.

3. **Separate fake and real code.** Ensure fake embedders live in tests and real local-model wrappers live in `src/researchops/search/embeddings.py`. Success: production modules do not import from tests.

4. **Rename vague variables.** Replace names like `x`, `y`, and `arr` with `query_embedding`, `chunk_embedding`, and `indexed_chunks` where useful. Success: a beginner can read the function aloud.

5. **Extract validation helpers cautiously.** If validation repeats, extract helpers such as `validate_vector_pair`. Success: the helper name teaches the rule and does not hide the simple formula.

6. **Keep dataclasses small.** Review `TextChunk` and `SearchHit`. Success: they carry data, not unrelated workflow behavior.

## Written explanation exercises

1. Explain why semantic search can find related text without exact word overlap.

2. Explain why a 384-dimensional vector can be useful even if you cannot visualize it.

3. Explain why chunk overlap improves boundary behavior.

4. Explain why unit tests should use a deterministic fake embedder.

5. Explain why an embedding cache key should include the model identity.

6. Explain why `source_id` is part of search correctness, not only display formatting.

7. Explain why Week 13 should not implement Week 14 HTTP routes.

8. Explain why two embeddings from different model dimensions cannot be compared safely.

9. Explain why a high cosine score is evidence for ranking but not absolute proof that a result is useful.

10. Explain what you would tell a teammate who wants to put `SentenceTransformer` construction inside a CLI command.

## Stretch exercises

1. **Qualitative retrieval set.** Create five short ML-themed documents and five queries with expected top documents. Produce: a table of query, expected source, actual top source, and notes.

2. **Chunk-size comparison.** Run the same documents with chunk sizes 30, 60, and 120. Produce: observations about precision and context.

3. **Model name cache guard.** Prove that the same text embedded under model names `fake-a` and `fake-b` uses different cache keys. Produce: a unit test.

4. **Stable tie handling.** Create two chunks with equal scores. Decide whether insertion order should be preserved. Produce: a test documenting the behavior.

5. **Readable result formatting.** Design CLI display text for hits showing score, source id, chunk index, and excerpt. Produce: a sample output only; keep ranking logic out of display code.

6. **Known-answer query cards.** Write five query cards: query text, expected source, and reason. Success: a human can review search quality without reading code.

7. **Duplicate chunks.** Add two identical chunks from different sources. Success: both can appear as separate hits because source metadata distinguishes them.

## Brutal exercises

1. **Dimension-mismatch audit.** Find every path where embeddings enter vector search. Add tests ensuring dimension mismatches fail loudly. Success: no silent truncation remains.

2. **Cache mutation trap.** Return a cached list directly, mutate it in caller code, then observe corruption. Fix by returning a copy. Success: a test proves caller mutation does not alter cache storage.

3. **Boundary fuzzing by hand.** Generate many combinations of document length, chunk size, and overlap. Success: no combination duplicates the final chunk unexpectedly or loops forever.

4. **Retrieval regression suite.** Build a tiny fixed corpus and expected top-1 answers using fake embeddings. Success: changing the sort direction or metadata propagation fails tests immediately.

5. **Architecture audit.** Search for `SentenceTransformer` outside `src/researchops/search/` and tests. Success: no service or core module imports the real model class directly.

6. **Explain every failure.** For each failure from `break_it.md`, write the smallest test that catches it. Success: every bug has a clear automated guard or a justified manual check.

7. **Tiny corpus challenge.** With only fake embeddings, design a tiny corpus where the top result is not the longest text. Success: your fake features and scoring prove ranking is not just length sorting.

## Mini project task

Build a tiny semantic search prototype for three stored paper snippets.

Input: three `(source_id, text)` pairs about different research topics.

Step 1: chunk each text with metadata.

Step 2: embed each chunk with a deterministic fake embedder.

Step 3: embed a query with the same fake embedder.

Step 4: run top-k vector search.

Step 5: print each hit as `score | source_id | chunk_index | excerpt`.

Success criteria: the code path preserves metadata, uses cosine similarity, returns sorted hits, and can be tested without internet access.

## Completion checklist

- [ ] I can define embeddings, chunks, cosine similarity, top-k, and cache keys.

- [ ] I implemented or can explain `chunk_text` with validation and metadata.

- [ ] I implemented or can explain cosine similarity with length and zero-vector handling.

- [ ] I can explain why unit tests use fake embeddings.

- [ ] I can explain why every hit needs source metadata.

- [ ] I have tests for chunk boundaries, invalid overlap, vector scoring, and ranking order.

- [ ] I understand the validation command from the syllabus.

- [ ] I did not build API routes, async fetchers, or deployment files for Week 13.

- [ ] I can explain how this retrieval behavior prepares cleanly for Week 14 without copying logic.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
