# Exercises - Week 13 Embeddings and Semantic Search

## Beginner

1. **Manual cosine similarity.** Take two vectors `a = [1.0, 0.0]` and `b = [0.707, 0.707]`. Compute cosine similarity by hand (dot product divided by product of magnitudes). Then write the `cosine_similarity` function from notes.md and confirm your hand calculation matches.

2. **Chunking a paragraph.** Copy a paragraph of at least 100 words from any source. Call `chunk_text` with `chunk_size=20` and `overlap=5`. Print each chunk on a separate line. Count how many chunks were produced and verify the overlap is correct by checking that the last 5 words of chunk 1 appear at the start of chunk 2.

3. **The FakeEmbeddingModel.** Implement `FakeEmbeddingModel.embed` exactly as shown in notes.md. Call it on three short phrases. Print the three resulting vectors. Explain in a comment why these vectors have different values.

4. **Ranking by similarity.** Create three vectors: one for a query and two for documents. Manually compute cosine similarity between the query and each document. Print them sorted highest first. Do not use any library — write the arithmetic yourself.

5. **Keyword vs semantic mismatch.** List five pairs of phrases where keyword search would fail to recognise relevance but semantic search should succeed. Example: ("dense retrieval", "vector search"). Write them in a comment block with a one-sentence explanation for each pair.

---

## Intermediate

1. **Implement `chunk_text` with validation.** Write the `chunk_text` function from notes.md. Add a check at the top: if `overlap >= chunk_size`, raise a `ValueError` with a clear message. Write three tests: one that chunks normally, one that chunks a document shorter than `chunk_size`, and one that raises on bad overlap.

2. **ChunkMetadata dataclass.** Define a `ChunkMetadata` dataclass with fields `source_id: str`, `chunk_index: int`, `start_word: int`, and `chunk_text: str`. Modify `chunk_text` to return `list[ChunkMetadata]` instead of `list[str]`. Track `start_word` correctly through the overlap logic.

3. **CachedEmbedder.** Implement the `CachedEmbedder` class from notes.md. Write a test that calls `embed` three times on the same text and confirms the underlying model was called only once. Use a counter or mock to verify call count.

4. **Top-k retrieval.** Implement the `search` function from notes.md. Write a unit test that creates 10 fake chunks with known embeddings, runs a query, and asserts the top-3 results are the three most similar chunks. Use `FakeEmbeddingModel` to produce all embeddings.

5. **Empty and edge queries.** Test `search` with:
   - An empty index (should return an empty list).
   - `top_k` larger than the index (should return all chunks).
   - A query whose embedding matches nothing closely (score near 0 for all results).
   Document the expected behaviour for each case.

---

## Advanced

1. **Sentence-transformers integration.** Install `sentence-transformers`. Implement `SentenceTransformerEmbedder` that wraps `SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")` and satisfies the `EmbeddingModel` protocol. Run a real embedding on five short phrases. Print their shapes. Verify two semantically similar phrases score higher than two unrelated phrases.

2. **SQLite chunk store.** Design a SQLite table to persist chunks and embeddings. The table should store `source_id`, `chunk_index`, `chunk_text`, and the embedding as a JSON-serialised float list. Implement `insert_chunk` and `load_chunks_for_source`. Write an integration test that inserts five chunks and retrieves them.

3. **Index-and-search pipeline.** Write an end-to-end function that takes a list of `(source_id, full_text)` pairs, chunks each document, embeds each chunk, stores the results, and then accepts a query string and returns the top-5 hits across all documents. Use `FakeEmbeddingModel` for tests and `SentenceTransformerEmbedder` for a manual smoke test.

4. **Hybrid scoring.** Write a `hybrid_score` function that combines a keyword relevance score (count of query words in chunk text) with a semantic cosine similarity score. Use a configurable weight `alpha` to blend: `alpha * semantic_score + (1 - alpha) * keyword_score`. Write tests that show how `alpha = 1.0` behaves differently from `alpha = 0.0`.

5. **Evaluate retrieval quality.** Manually create five short documents covering different ML topics. Define five queries that each should retrieve one specific document. Run your pipeline. For each query, report which document ranked first and whether it was the expected one. Write a brief analysis: where did semantic search outperform keywords, and where did it fail?

---

## Brutal

1. **Chunk size ablation.** Index the same set of five documents with `chunk_size` values of 50, 100, 200, 400. For each configuration, run the same five queries and record which documents appear in the top-3. Does smaller chunk size improve precision or hurt recall? Write a structured report (table or prose) analysing the results. There is no single correct answer — the goal is rigorous observation.

2. **Persistent embedding cache with TTL.** Extend `CachedEmbedder` to persist to SQLite. Add a time-to-live (TTL) so cached embeddings expire after a configurable number of hours. On lookup, if the cached entry is expired, recompute and update. Write tests that use fake time (mock `datetime.now()`) to verify TTL expiry without sleeping.

3. **Implement approximate nearest-neighbour search.** Standard top-k search scans every embedding. For large indexes this is slow. Implement a bucketed index: hash each embedding's highest-dimension component into one of 8 buckets. On query, only search embeddings in the same bucket as the query. Write tests that confirm the bucketed search returns the same top-1 result as the exhaustive search for all test cases. Document cases where it might not.

4. **Protocol-safe embedder factory.** Write an `EmbedderFactory` that reads a string configuration value ("fake", "sentence-transformers", "noop") and returns the appropriate embedder, each satisfying the `EmbeddingModel` protocol. Add a configuration setting to `researchops` settings that controls which embedder is constructed. Write tests for all three modes — do not require `sentence-transformers` installed for the "fake" and "noop" tests (use a conditional import guard).

5. **RAG readiness audit.** Read the Month 5 preview in the syllabus or roadmap. Identify five design decisions you made this week (chunk size, overlap, metadata fields, storage schema, scoring strategy) that will affect Month 5's RAG assistant. For each decision, write: what you chose, why, and what you would need to change if the RAG system required higher precision. Commit this as a short markdown document in `docs/`.
