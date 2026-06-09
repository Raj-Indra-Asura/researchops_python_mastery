<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 13 Embeddings and Semantic Search

## 1. Purpose of failure practice

Semantic search failures are often quiet. A command can return results that look formatted and professional while the ranking is wrong, the metadata is missing, or the scores are meaningless. This lab teaches you to create those failures on purpose so you can recognize them later.

## 2. Failure lab rules

- Break one thing at a time.
- Write down the exact symptom before fixing it.
- Prefer a failing test over a vague feeling.
- Restore the correct implementation after each experiment.
- Do not use real model files for unit-test failures.
- Do not build future-week API, async, or deployment behavior in this lab.

## 3. Intentional break experiments

### Experiment 1 — Infinite loop from bad overlap

#### How to cause it
Set `chunk_size=50` and `overlap=50`, or temporarily remove the validation guard that rejects `overlap >= chunk_size`.

#### Expected error or symptom
The chunker may never finish because `start = end - overlap` returns to the same position. In a real run this can look like a hung command or growing memory use.

#### How to inspect the failure
Print `start`, `end`, and `overlap` for the first few iterations. You should see `start` stop advancing. Inspect the test timeout or interrupt the run if needed.

#### How to fix it
Restore validation: `overlap` must be smaller than `chunk_size`, `chunk_size` must be positive, and `overlap` must not be negative.

#### Test that should catch it
`test_chunk_text_rejects_overlap_equal_to_chunk_size` should assert a `ValueError` with a clear message.

#### What this failure teaches
Progress through a loop is a design requirement. Validation protects both correctness and the learner from a command that appears frozen.

#### Common wrong fixes
Changing `start = end` and removing overlap entirely; silently changing overlap to zero; catching every exception in the CLI instead of fixing the chunker.

### Experiment 2 — Mismatched vector lengths silently truncate

#### How to cause it
Remove the length check from cosine similarity and compare `[1.0, 0.0]` with `[1.0, 0.0, 0.5]`.

#### Expected error or symptom
`zip` compares only the first two positions, so the function returns a plausible but wrong score. There may be no exception.

#### How to inspect the failure
Print `len(left)`, `len(right)`, and `list(zip(left, right))`. The third value disappears from the paired list.

#### How to fix it
Raise `ValueError` when vector lengths differ before computing the dot product.

#### Test that should catch it
`test_cosine_similarity_rejects_mismatched_dimensions` should fail without the guard.

#### What this failure teaches
Silent truncation is worse than a crash because it hides mixed embedding models or broken fakes.

#### Common wrong fixes
Padding the shorter vector with zeros without understanding the model; ignoring the extra dimension; rounding the score until it looks reasonable.

### Experiment 3 — Zero vector division

#### How to cause it
Pass `[0.0, 0.0, 0.0]` as either the query embedding or chunk embedding.

#### Expected error or symptom
Without a guard, `dot / (left_length * right_length)` can raise `ZeroDivisionError` because one magnitude is zero.

#### How to inspect the failure
Print the dot product and both magnitudes. The failing denominator should be `0.0`.

#### How to fix it
Choose and implement a convention. A common beginner-friendly convention is returning `0.0` when either vector has no direction.

#### Test that should catch it
`test_cosine_similarity_returns_zero_for_zero_vector` or `test_cosine_similarity_rejects_zero_vector` should document the chosen convention.

#### What this failure teaches
A zero vector has no direction, so cosine similarity needs intentional behavior rather than accidental division.

#### Common wrong fixes
Adding a tiny random number to the denominator; returning `1.0`; hiding the error only at the command display layer.

### Experiment 4 — All embeddings identical

#### How to cause it
Replace the fake embedder with one that always returns `[1.0, 1.0, 1.0]` for every text.

#### Expected error or symptom
Every non-zero chunk has the same cosine score against the query. Ranking becomes insertion order, not relevance.

#### How to inspect the failure
Print each hit score and source id. You should see repeated scores such as `1.0000` for unrelated chunks.

#### How to fix it
Restore a fake embedder that produces different deterministic vectors from text features. Add a test corpus where expected order is meaningful.

#### Test that should catch it
`test_search_orders_known_vectors_by_similarity` should fail when every embedding is identical.

#### What this failure teaches
Search quality depends on the embedder producing useful distinctions. Ranking code cannot recover relevance from collapsed vectors.

#### Common wrong fixes
Tweaking sort order; adding random noise; hardcoding expected paper ids into search.

### Experiment 5 — Empty query creates meaningless search

#### How to cause it
Call semantic search with an empty string or whitespace-only query, then let the fake embedder produce a zero-like vector.

#### Expected error or symptom
The command may return arbitrary low-quality results, or cosine similarity may hit the zero-vector path.

#### How to inspect the failure
Inspect the raw query before embedding. Print `repr(query)` and the query embedding.

#### How to fix it
Reject empty or whitespace-only queries at the search entry point with a clear error, or define a documented empty-result behavior.

#### Test that should catch it
`test_semantic_search_rejects_blank_query` should assert the chosen behavior.

#### What this failure teaches
Input validation prevents meaningless model work and confusing user output.

#### Common wrong fixes
Embedding the empty string and pretending results are meaningful; trimming after embedding; returning all papers as if that were search.

### Experiment 6 — Chunk index off by one

#### How to cause it
Change the first `chunk_index` from `0` to `1`.

#### Expected error or symptom
Tests or callers expecting chunk 0 fail. Display may skip the first chunk or link to the wrong passage.

#### How to inspect the failure
Print all chunk indexes for a short document. Compare them with Python list positions.

#### How to fix it
Restore zero-based chunk indexes and ensure the index increments once per appended chunk.

#### Test that should catch it
`test_first_chunk_index_is_zero` should catch this immediately.

#### What this failure teaches
Consistent indexing matters because metadata becomes a contract between chunking, storage, search, and display.

#### Common wrong fixes
Changing tests to expect 1-based indexes without a project-wide decision; storing both index styles; subtracting 1 randomly in display code.

### Experiment 7 — Missing source metadata

#### How to cause it
Remove `source_id` from `TextChunk` or `SearchHit`, or set it to an empty string.

#### Expected error or symptom
Search still returns text and scores, but the user cannot trace the result to a stored paper.

#### How to inspect the failure
Inspect the `SearchHit` objects directly. Check whether each hit has `source_id` and `chunk_index` before formatting output.

#### How to fix it
Preserve metadata from chunk creation through indexing and top-k results.

#### Test that should catch it
`test_search_hits_include_source_metadata` should assert non-empty `source_id` on every hit.

#### What this failure teaches
Retrieval is not complete unless results are traceable. Relevance without provenance is not useful in a research tool.

#### Common wrong fixes
Trying to infer the source from text later; using list position as a paper id; hiding source fields from tests because display looks okay.

### Experiment 8 — Wrong sorting direction

#### How to cause it
Change `hits.sort(key=lambda hit: hit.score, reverse=True)` to omit `reverse=True`.

#### Expected error or symptom
The least similar chunks appear first while output still looks normal.

#### How to inspect the failure
Print scores before and after sorting. The first score after sorting will be the smallest.

#### How to fix it
Restore descending sort for similarity scores where larger means more similar.

#### Test that should catch it
`test_search_returns_highest_score_first` should fail with ascending sort.

#### What this failure teaches
A polished result table can hide a reversed ranking. Tests should pin the intended order.

#### Common wrong fixes
Negating scores in one place; reversing display order only; changing the fake vectors so the bad order accidentally passes.

### Experiment 9 — Cache key ignores model identity

#### How to cause it
Build a cache key from text only, then simulate two model names returning different vector dimensions for the same text.

#### Expected error or symptom
The second model may reuse the first model vector, causing mismatched dimensions or wrong scores.

#### How to inspect the failure
Log or print cache keys for `(model-a, text)` and `(model-b, text)`. If they match, the cache is unsafe.

#### How to fix it
Include model identity and text in the hashed cache input.

#### Test that should catch it
`test_cache_key_changes_when_model_name_changes` should prove the fix.

#### What this failure teaches
Embedding vectors are only comparable inside the vector space produced by the same model family.

#### Common wrong fixes
Clearing the whole cache on every run; ignoring model upgrades; storing only the first 20 characters as the key.

## 4. Debugging checklist

- [ ] Can I reproduce the failure with one small input?
- [ ] Did I inspect chunk count before inspecting embeddings?
- [ ] Did I inspect query embedding length and chunk embedding length?
- [ ] Did I check for zero vectors before scoring?
- [ ] Did I print scores before and after sorting?
- [ ] Did I verify every hit has `source_id` and `chunk_index`?
- [ ] Did I confirm unit tests use fake embeddings?
- [ ] Did I fix the production cause instead of only changing the display?
- [ ] Did I add or restore the test that would catch this next time?

## 5. Reflection after breaking

- Which failure looked most harmless but caused the worst result?
- Which failure produced a loud exception, and which produced quiet bad ranking?
- Which test gave the clearest explanation of the bug?
- Which missing validation check would most confuse a beginner user?
- How would you explain the bug without using the word magic?
- What will you inspect first the next time semantic search returns strange hits?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
