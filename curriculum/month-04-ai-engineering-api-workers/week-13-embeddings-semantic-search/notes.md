<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 13 Embeddings and Semantic Search

## Chapter overview

The chapter title is **Meaning as a vector**.

This week turns ResearchOps search from exact-word matching into meaning-based retrieval.

The visible milestone is:

```bash
researchops semantic-search "efficient transformers"
```

The command should return papers or passages ranked by vector similarity to the query.

That sentence contains several new ideas, so this chapter slows down and defines them carefully.

A **paper** is still the research document you have been ingesting and storing throughout the project.

A **passage** is a smaller piece of the paper, usually produced by splitting the paper text into chunks.

A **query** is the text the user types when they ask ResearchOps to find something.

A **vector** is a list of numbers, such as `[0.12, -0.44, 0.08]`.

An **embedding** is a vector produced from text by a model.

A **semantic search result** is a result chosen because its vector points in a similar direction to the query vector.

The success condition is not that ResearchOps becomes a perfect search engine.

The success condition is that you can explain and test the complete path from text to chunks, from chunks to embeddings, from embeddings to cosine scores, and from scores to top-k search results.

The main files named by the syllabus are:

- `src/researchops/search/chunking.py` — splits long paper text into smaller overlapping pieces.
- `src/researchops/search/embeddings.py` — owns embedding generation and caching.
- `src/researchops/search/vector_search.py` — owns cosine similarity and top-k ranking.
- `src/researchops/core/interfaces.py` — contains the `SearchEngine` protocol contract.
- `tests/unit/test_chunking.py` — proves chunk boundaries and metadata are correct.
- `tests/unit/test_vector_search.py` — proves cosine similarity and ranking are correct.
- `tests/fakes/` — contains deterministic fake implementations used by tests.

By the end of this chapter, you should be able to answer these questions without guessing:
- Why does keyword search miss useful papers?
- What is stored inside an embedding vector?
- Why does a long paper need chunking before embedding?
- Why must the indexing model and query model be the same?
- How does cosine similarity compare two vectors?
- Why does `top_k=5` return only the five highest-scoring hits?
- Why should tests use a deterministic fake embedder instead of a real local model?
- What does an embedding cache save, and what can go wrong if the cache key is bad?

Study sequence for the week:
1. Read the mental model before reading code.
2. Trace one tiny paper text through `chunk_text` by hand.
3. Trace one query vector through `cosine_similarity` by hand.
4. Read `vector_search.py` after you understand the formula.
5. Read `embeddings.py` after you understand the fake embedder and cache.
6. Run the validation commands only when the code is ready; this documentation task does not require running them.

## What you already know from previous weeks

Week 13 is not the first time ResearchOps has searched, stored, tested, or modeled text.

It is the week where those earlier ideas meet dense vector representations.

- **Week 5: SQLite storage.** You learned that ResearchOps data can persist in a local database instead of disappearing when Python exits.
- **Week 6: repository patterns.** You learned to hide persistence details behind a repository-style boundary.
- **Week 7: services.** You learned that workflows belong in service/use-case code rather than in command handlers.
- **Week 8: multiprocessing.** You learned that CPU-heavy work should be isolated from user-facing orchestration.
- **Week 9: Protocols and clean architecture.** You learned that services depend on contracts in `core/interfaces.py`, not concrete infrastructure.
- **Week 10: testing discipline.** You learned that fast unit tests and fakes protect behavior before integration tests run.
- **Week 11: classical ML topic classification.** You learned that text can become numeric features and feed a machine-learning pipeline.
- **Week 12: experiment tracking.** You learned to record parameters, metrics, artifacts, and runs so ML work remains reproducible.

Week 11 is especially important because it introduced the idea that text can be transformed into numbers.

TF-IDF represented text by counting how important words are inside documents.

Embeddings also represent text with numbers, but they are learned dense vectors rather than sparse word-count features.

Week 12 is important because embedding systems also need reproducibility.

If you change the embedding model, chunk size, overlap, or scoring formula, search results can change.

A careful engineer records those choices when evaluating retrieval quality.

Week 9 matters because this week introduces `src/researchops/search/` as infrastructure.

The architecture says infrastructure may import third-party libraries such as `sentence-transformers`, but services should depend on protocols rather than directly importing heavy model classes.

That boundary lets the CLI and future API wire real implementations while tests use fakes.

If any previous idea feels weak, pause and review it before adding semantic search.

Semantic search has more moving parts than keyword search, so unclear boundaries become painful quickly.

## What problem this week solves

ResearchOps already has keyword search in the project plan.

Keyword search is useful when the user knows the exact words in the stored paper.

It struggles when the user and the paper use different vocabulary for the same idea.

A user might type `efficient transformers`.

A paper might say `attention models with reduced computational cost`.

Keyword search may miss the paper because the phrase `efficient transformers` does not appear exactly.

Semantic search tries to match meaning instead of matching only characters.

This week solves four concrete ResearchOps gaps:
1. Long paper text must be split into chunks so specific passages can be found.
2. Each chunk must be turned into a numeric vector that can be compared mathematically.
3. The query must be embedded with the same kind of model used for the chunks.
4. The system must rank chunks by similarity and return the top-k most relevant hits with source metadata.

The result is not just a new command.

It is a new retrieval layer inside ResearchOps.

A retrieval layer answers the question: "Which stored text should I inspect first for this user intent?"

The answer must include enough metadata to trace the hit back to the paper and chunk where it came from.

A hit without source metadata is like a library search result with no shelf location.

It may be interesting, but it is not actionable.

## Beginner mental model

Think of semantic search as building a meaning map for your paper library.

Every chunk of text becomes a point on the map.

Every query also becomes a point on the same map.

Search means: find the stored points that point in the most similar direction to the query point.

The map has too many dimensions to draw.

A small local model such as `sentence-transformers/all-MiniLM-L6-v2` produces 384 numbers for each text.

You cannot visualize 384 dimensions, but you can still calculate with them.

Use this five-box flow:
- **Raw paper text:** A stored paper body, abstract, or extracted PDF text.
- **Chunks:** Smaller overlapping passages with `source_id`, `chunk_index`, and `start_word`.
- **Embeddings:** One dense vector per chunk, created by an embedding model.
- **Scores:** Cosine similarity values comparing query vector to chunk vectors.
- **Top-k hits:** The highest-scoring chunks returned with scores and source metadata.

The key beginner shift is this: the words themselves are not compared directly during vector search.

The numeric representations are compared.

That does not mean the words stop mattering.

The embedding model read the words and produced the vector from them.

But after embedding, ranking is arithmetic.

The simplest mental model for the arithmetic is direction.

If two vectors point in nearly the same direction, cosine similarity is close to `1.0`.

If two vectors point in unrelated directions, cosine similarity is closer to `0.0`.

If two vectors point in opposite directions, cosine similarity can be negative.

For search ranking, bigger usually means more similar.

When debugging, always ask where you are in the five-box flow.

A chunking bug is different from an embedding bug.

An embedding bug is different from a ranking bug.

A ranking bug is different from a display bug.

## Core vocabulary

| Term | Plain meaning | Why it matters here |
|---|---|---|
| keyword search | Search that compares the literal words in the query with literal words in stored text. | It is the baseline semantic search improves on when users use synonyms or paraphrases. |
| semantic search | Search that tries to match meaning, not only exact words. | It lets `efficient transformers` find passages that discuss cheaper attention models even if the wording differs. |
| embedding | A dense list of floating-point numbers produced from text. | ResearchOps stores or computes embeddings so chunks and queries can be compared mathematically. |
| dense vector | A vector where most positions contain meaningful non-zero values. | Embedding vectors are dense, unlike sparse bag-of-words features where most positions are zero. |
| dimension | One position in a vector. | A 384-dimensional model returns 384 numbers per text, so all compared vectors must have length 384. |
| chunk | A smaller piece of a long document. | Research papers are too long to search precisely as one huge vector. |
| chunk size | The target amount of text in each chunk. | Too large can dilute the relevant passage; too small can remove necessary context. |
| overlap | Repeated text shared between neighboring chunks. | It prevents an important sentence or idea from being split cleanly in half at a boundary. |
| chunk metadata | Information that tells where a chunk came from. | `source_id`, `chunk_index`, and `start_word` let a search hit point back to the original paper. |
| embedding model | The code or model that turns text into vectors. | The real implementation can use `sentence-transformers`; tests should use a deterministic fake. |
| local model | A model that runs on the learner machine instead of calling an external API. | Week 13 uses local sentence-transformers so no API key is needed for the learning path. |
| fake embedder | A small test implementation that returns predictable vectors. | It makes unit tests fast, offline, deterministic, and easy to reason about. |
| cosine similarity | A score based on the angle between two vectors. | It ranks chunks by vector direction and usually ignores vector length. |
| dot product | The sum of pairwise multiplications between two vectors. | It is the numerator in the cosine similarity formula. |
| magnitude | The length of a vector. | Cosine similarity divides by magnitudes so long vectors do not automatically win. |
| zero vector | A vector where every value is `0.0`. | It has no direction, so cosine similarity must handle it deliberately. |
| top-k | The first `k` items after sorting by score. | `top_k=5` means return only the five highest-scoring hits. |
| embedding cache | A lookup that reuses previously computed embeddings. | It avoids recomputing vectors for unchanged chunk text. |
| cache key | The value used to identify cached data. | A hash of model name plus text is safer than text alone when models can change. |
| retrieval evaluation | Checking whether returned results make sense for known queries. | It catches failures that arithmetic tests cannot fully capture. |

## Concept explanations from first principles

### 6.1 What embeddings are: a dense numeric representation of meaning

An embedding is a numeric representation of text.

Representation means one thing stands in for another thing.

A paper title such as `Efficient Attention for Long Documents` is human-readable text.

A vector such as `[0.13, -0.22, 0.91, ...]` is machine-comparable data.

The vector does not contain words in a visible form.

It contains numbers learned by a model during training.

Similar meanings should land near each other in vector space.

Different meanings should land farther apart or point in different directions.

This is why the query `cheap transformer inference` can retrieve a chunk about `reducing attention computation`.

The model has learned from many text examples that those phrases often live near the same idea.

Dense means most dimensions matter.

This differs from a sparse TF-IDF vector where one dimension might mean a specific vocabulary word.

With embeddings, you usually do not know what dimension 17 means by itself.

The full pattern across all dimensions carries the meaning.

### 6.2 Chunking text for embedding: why long documents need to be split

A research paper can contain an abstract, introduction, related work, methods, experiments, limitations, and references.

One whole-paper embedding has to compress all of that into one vector.

Compression loses detail.

If the user asks about an optimization detail in the methods section, a whole-paper vector may be too broad.

Chunking splits text into smaller passages before embedding.

Each chunk gets its own vector.

The query can then match the exact methods passage rather than the entire paper.

Chunk size controls how much text goes into each passage.

Overlap repeats boundary words so ideas are not cut in half.

Metadata keeps each chunk connected to its source paper.

Without metadata, a relevant chunk is not enough because the user cannot locate the paper.

A good first chunker is simple, deterministic, and heavily tested.

### 6.3 `sentence-transformers` local models: no API key, no network call needed for normal use

`sentence-transformers` is a Python library that wraps pretrained text embedding models.

A local model runs on your machine rather than sending paper text to an outside embedding API.

For a learning project, local execution has three advantages.

First, no API key is needed for the normal command path.

Second, private research text stays on the local machine.

Third, tests can be designed to avoid model downloads by using fakes.

The real model still belongs behind an implementation boundary.

Do not sprinkle `SentenceTransformer(...)` calls throughout services or command handlers.

Put real embedding generation in `src/researchops/search/embeddings.py`.

Let tests use deterministic fakes from `tests/fakes/` so unit tests remain fast and offline.

If a real model is used for a manual smoke check, the code should make that dependency explicit.

### 6.4 Cosine similarity: angle between vectors as semantic closeness

Cosine similarity compares vector direction.

Direction matters because embeddings often use orientation to represent meaning.

The formula is `dot(a, b) / (length(a) * length(b))`.

The dot product multiplies matching positions and adds the products.

The length of a vector is the square root of the sum of squared values.

Dividing by both lengths prevents long vectors from winning just because they are long.

A score near `1.0` means the vectors point in a very similar direction.

A score near `0.0` means they are mostly unrelated in direction.

A negative score means they point away from each other.

Cosine similarity only makes sense when both vectors have the same length.

It also needs a deliberate rule for zero vectors because zero has no direction.

### 6.5 Embedding cache: do not recompute what you already have

Embedding generation is slower than ordinary string operations.

If ResearchOps embeds the same chunk text every time a command runs, the user waits unnecessarily.

A cache stores the vector for a known input.

The next time the same input appears, the cache returns the saved vector.

A useful cache key should include the text and the model identity.

If the key uses only text, changing models can accidentally reuse vectors from an old vector space.

For beginner code, an in-memory dictionary cache is enough to teach the idea.

For a longer-lived application, a persistent cache can store vectors in SQLite or another local format.

The important behavior is the same: unchanged text plus same model should not be recomputed.

### 6.6 Retrieval evaluation: does the top result make sense?

Unit tests can prove arithmetic.

They cannot fully prove retrieval quality.

Retrieval quality asks whether the returned results are useful for real research questions.

For Week 13, evaluation can be small and manual.

Create a few known paper snippets.

Write queries where you know which snippet should rank first.

Check the top hit and top three hits.

Record whether semantic search finds a relevant chunk even when exact keywords differ.

When results are poor, inspect chunk size, overlap, model choice, query wording, and metadata.

Do not hide bad retrieval behind a passing unit test.

## ResearchOps-specific application

In ResearchOps, semantic search is not a standalone notebook experiment.

It is part of the application architecture.

The command from the syllabus is:

```bash
researchops semantic-search "machine learning"
pytest tests/unit/test_chunking.py tests/unit/test_vector_search.py -v
```

The command path should stay thin.

The CLI parses the query and limit, wires dependencies, and displays results.

The search logic itself belongs below the command layer.

The search package owns embedding and vector ranking details.

A typical ResearchOps indexing flow looks like this:
1. A paper has already been ingested and stored.
2. The stored text is passed to `chunk_text`.
3. `chunk_text` returns chunk objects with text and metadata.
4. The embedder converts each chunk text into a vector.
5. The vector is stored or held in an index together with the chunk metadata.
6. Later, the query text is embedded with the same model family.
7. `vector_search.py` scores query vector against chunk vectors.
8. The highest-scoring chunks become `SearchHit` results.

Notice that the chunk text and metadata travel together.

A search hit should not be just a string.

It should say which paper produced the chunk and which chunk index matched.

A beginner often wants to return only the text because that is easiest.

That loses important product behavior.

ResearchOps is a research tool, so traceability matters.

When the system says a passage is relevant, the learner should be able to inspect the source paper.

## Code examples with line-by-line explanation

### Cosine similarity with validation

```python
import math


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have the same length")
    if not left:
        raise ValueError("vectors must not be empty")

    dot_product = sum(a * b for a, b in zip(left, right))
    left_length = math.sqrt(sum(a * a for a in left))
    right_length = math.sqrt(sum(b * b for b in right))

    if left_length == 0.0 or right_length == 0.0:
        return 0.0

    return dot_product / (left_length * right_length)
```

Line-by-line explanation:

- `import math` loads Python standard-library math functions; `sqrt` is used for vector length.
- `def cosine_similarity(...) -> float:` names a reusable scoring function and states that it returns one number.
- `if len(left) != len(right):` checks that both vectors have the same number of dimensions.
- `raise ValueError(...)` fails loudly instead of silently comparing only part of a vector.
- `if not left:` rejects empty vectors because an empty direction is not meaningful for search.
- `dot_product = ...` multiplies matching dimensions and adds them into one numerator value.
- `zip(left, right)` pairs values by position: first with first, second with second, and so on.
- `left_length = ...` squares each left value, sums the squares, and takes the square root.
- `right_length = ...` does the same length calculation for the right vector.
- `if left_length == 0.0 or right_length == 0.0:` handles the zero-vector case before division.
- `return 0.0` chooses a safe convention: a vector with no direction has no similarity.
- `return dot_product / ...` divides by both lengths so direction matters more than raw magnitude.

### Chunking with metadata

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    source_id: str
    chunk_index: int
    start_word: int
    text: str


def chunk_text(source_id: str, text: str, chunk_size: int = 300, overlap: int = 50) -> list[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap must not be negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks: list[TextChunk] = []
    start = 0
    chunk_index = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append(
            TextChunk(
                source_id=source_id,
                chunk_index=chunk_index,
                start_word=start,
                text=" ".join(chunk_words),
            )
        )
        chunk_index += 1
        start = end - overlap
        if end == len(words):
            break

    return chunks
```

Line-by-line explanation:

- `from dataclasses import dataclass` imports the decorator used to define a small data container.
- `@dataclass(frozen=True)` creates an immutable chunk object so tests can compare it easily.
- `class TextChunk:` defines the shape of one chunk returned by the chunker.
- `source_id: str` stores the paper or document identifier.
- `chunk_index: int` stores the chunk position inside that source, starting at `0`.
- `start_word: int` stores where this chunk begins in the original word list.
- `text: str` stores the actual passage that will be embedded.
- `def chunk_text(...)` accepts source metadata, raw text, and chunking parameters.
- `if chunk_size <= 0:` prevents a chunk size that cannot make progress.
- `if overlap < 0:` rejects a boundary rule that would skip unexpected text.
- `if overlap >= chunk_size:` prevents the classic infinite-loop bug.
- `words = text.split()` turns text into a simple whitespace-based word list.
- `chunks: list[TextChunk] = []` prepares the output list.
- `start = 0` begins at the first word.
- `chunk_index = 0` follows Python indexing conventions used elsewhere in tests.
- `while start < len(words):` loops while unread words remain.
- `end = min(...)` chooses the chunk end without running past the document.
- `chunk_words = words[start:end]` slices the current chunk words.
- `chunks.append(...)` records both the text and the metadata together.
- `source_id=source_id` preserves the connection to the paper.
- `chunk_index=chunk_index` records the current chunk number.
- `start_word=start` records the original boundary for debugging and display.
- `text=" ".join(chunk_words)` returns readable text rather than a list of words.
- `chunk_index += 1` prepares the next chunk index.
- `start = end - overlap` moves forward while repeating overlap words.
- `if end == len(words): break` stops after the final chunk so overlap does not create a duplicate tail chunk.
- `return chunks` returns every chunk in document order.

### Deterministic fake embedder for tests

```python
class FakeEmbeddingModel:
    def embed(self, text: str) -> list[float]:
        lowered = text.lower()
        return [
            float(len(text)),
            float(len(text.split())),
            float(lowered.count("model")),
            float(lowered.count("search")),
        ]
```

Line-by-line explanation:

- `class FakeEmbeddingModel:` defines a tiny object with the same kind of method as a real embedder.
- `def embed(self, text: str) -> list[float]:` accepts one text string and returns one vector.
- `lowered = text.lower()` makes word counting case-insensitive.
- `return [` starts a deterministic four-dimensional vector.
- `float(len(text))` uses character count as the first dimension.
- `float(len(text.split()))` uses word count as the second dimension.
- `float(lowered.count("model"))` counts a topic word relevant to ML papers.
- `float(lowered.count("search"))` counts a topic word relevant to retrieval examples.
- `]` ends the vector; the same input always produces the same output.

### Simple embedding cache

```python
import hashlib


class CachedEmbedder:
    def __init__(self, model_name: str, model: FakeEmbeddingModel) -> None:
        self._model_name = model_name
        self._model = model
        self._cache: dict[str, list[float]] = {}

    def embed(self, text: str) -> list[float]:
        key_text = f"{self._model_name}
{text}"
        cache_key = hashlib.sha256(key_text.encode("utf-8")).hexdigest()

        if cache_key not in self._cache:
            self._cache[cache_key] = self._model.embed(text)

        return list(self._cache[cache_key])
```

Line-by-line explanation:

- `import hashlib` loads a standard-library module for stable hashes.
- `class CachedEmbedder:` wraps another embedder and remembers previous results.
- `def __init__(...)` receives a model name and the model object to wrap.
- `self._model_name = model_name` stores the model identity so cache keys can include it.
- `self._model = model` stores the underlying embedder that does the real work.
- `self._cache: dict[str, list[float]] = {}` creates an in-memory dictionary from hash to vector.
- `def embed(...)` exposes the same method shape as the wrapped model.
- `key_text = ...` combines model name and text so different models do not share cached vectors accidentally.
- `hashlib.sha256(...)` creates a fixed-length cache key from the combined text.
- `if cache_key not in self._cache:` checks whether this exact input has been embedded already.
- `self._cache[cache_key] = ...` calls the underlying model only on a cache miss.
- `return list(...)` returns a copy so callers cannot mutate the cached list accidentally.

### Top-k vector search

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchHit:
    source_id: str
    chunk_index: int
    text: str
    score: float


def search_top_k(
    query_embedding: list[float],
    indexed_chunks: list[tuple[list[float], TextChunk]],
    top_k: int = 5,
) -> list[SearchHit]:
    if top_k <= 0:
        return []

    hits: list[SearchHit] = []
    for chunk_embedding, chunk in indexed_chunks:
        score = cosine_similarity(query_embedding, chunk_embedding)
        hits.append(
            SearchHit(
                source_id=chunk.source_id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                score=score,
            )
        )

    hits.sort(key=lambda hit: hit.score, reverse=True)
    return hits[:top_k]
```

Line-by-line explanation:

- `@dataclass(frozen=True)` makes each result easy to compare in tests.
- `class SearchHit:` defines the visible result returned by vector search.
- `source_id` tells which paper produced the hit.
- `chunk_index` tells which chunk inside that paper matched.
- `text` stores the passage shown to the user.
- `score` stores the cosine similarity used for ranking.
- `def search_top_k(...)` accepts a query vector, an index of chunk vectors, and a result limit.
- `query_embedding` must come from the same model family as the chunk embeddings.
- `indexed_chunks` pairs each stored vector with its `TextChunk` metadata.
- `top_k: int = 5` defaults to five visible hits.
- `if top_k <= 0: return []` defines a clear behavior for zero or negative limits.
- `hits: list[SearchHit] = []` prepares the output before scoring.
- `for chunk_embedding, chunk in indexed_chunks:` scans each stored chunk once.
- `score = cosine_similarity(...)` computes the ranking number.
- `hits.append(...)` records the score and metadata together.
- `source_id=chunk.source_id` preserves traceability.
- `chunk_index=chunk.chunk_index` preserves chunk position.
- `text=chunk.text` keeps the result readable.
- `score=score` stores the numeric evidence used for sorting.
- `hits.sort(...)` orders results from highest score to lowest score.
- `return hits[:top_k]` returns only the requested number of best hits.

## Common beginner mistakes

### Mistake: Embedding the whole paper as one vector

**Why it breaks:** A specific methods paragraph is diluted by the abstract, introduction, experiments, and references.

**Fix:** Chunk the text and embed each chunk separately.

### Mistake: Using `zip` without checking vector lengths

**Why it breaks:** `zip` silently stops at the shorter vector, so a 3D vector and 4D vector can produce a fake score.

**Fix:** Raise `ValueError` when lengths differ.

### Mistake: Dividing by zero for empty or zero vectors

**Why it breaks:** A zero vector has magnitude `0.0`, so cosine similarity can crash.

**Fix:** Define a convention such as returning `0.0` similarity or rejecting the input.

### Mistake: Letting `overlap >= chunk_size`

**Why it breaks:** The start pointer never advances and the chunking loop can run forever.

**Fix:** Validate `overlap < chunk_size` before the loop.

### Mistake: Dropping `source_id` from search hits

**Why it breaks:** The user sees a relevant passage but cannot find the paper it came from.

**Fix:** Carry metadata from chunking through search results.

### Mistake: Using the real model in every unit test

**Why it breaks:** Tests become slow, may require model files, and become hard to reason about by hand.

**Fix:** Use deterministic fakes in unit tests and reserve real models for explicit integration or manual checks.

### Mistake: Caching only by text when model can change

**Why it breaks:** A vector from one model can be reused for another model, mixing incompatible vector spaces.

**Fix:** Include model identity in the cache key.

### Mistake: Sorting scores ascending

**Why it breaks:** The least similar chunks appear first.

**Fix:** Sort with `reverse=True` so highest cosine scores win.

### Mistake: Forgetting `top_k` edge cases

**Why it breaks:** `top_k=0` or `top_k` larger than the index may behave accidentally.

**Fix:** Define and test these cases.

### Mistake: Putting vector ranking in the CLI command

**Why it breaks:** The command handler becomes business logic and cannot be reused cleanly.

**Fix:** Keep ranking in `src/researchops/search/vector_search.py` or a service that depends on interfaces.

## Debugging guidance

Debug semantic search by locating the first wrong value in the pipeline.

Do not start by changing the model.

Most beginner bugs are ordinary data-shape bugs: wrong chunk boundaries, missing metadata, mismatched vector lengths, or reversed sorting.

- **Symptom:** The command returns no results
  **Inspect:** Check whether the index is empty, whether chunking returned zero chunks, and whether the query was rejected as blank.
- **Symptom:** The command returns results with no paper id
  **Inspect:** Inspect the chunk object and `SearchHit`; metadata was probably dropped between chunking and ranking.
- **Symptom:** All scores are exactly the same
  **Inspect:** The fake embedder may be returning identical vectors, or the same chunk embedding may be reused for every chunk.
- **Symptom:** A `ZeroDivisionError` appears
  **Inspect:** One vector has magnitude zero; inspect the query embedding and chunk embeddings before scoring.
- **Symptom:** A `ValueError` about vector lengths appears
  **Inspect:** The query embedder and index embedder probably use different dimensions or an inconsistent fake.
- **Symptom:** The worst-looking result appears first
  **Inspect:** Check whether sorting uses `reverse=True` and whether the score key is correct.
- **Symptom:** Chunking never finishes
  **Inspect:** Check `overlap >= chunk_size`; the start pointer is not advancing.
- **Symptom:** A test unexpectedly downloads model files
  **Inspect:** Find imports or fixtures using the real sentence-transformers model; unit tests should use fakes.

A useful print-debugging sequence during development is:

1. Print the number of chunks produced for one known paper.
2. Print the first chunk metadata: source id, chunk index, start word, and first 80 characters.
3. Print the query embedding length.
4. Print the first stored embedding length.
5. Print the first five `(source_id, chunk_index, score)` tuples before sorting.
6. Print the first five tuples after sorting.

Remove temporary prints after the failing behavior is understood.

A good permanent test is better than a permanent debug print.

## Design tradeoffs

| Choice | Benefit | Cost | Week 13 guidance |
|---|---|---|---|
| Whole-document embeddings | Simple and cheap to store. | Too coarse for specific methods or results questions. | Use only as a first baseline, not the main Week 13 design. |
| Chunk embeddings | Better precision and source traceability. | More vectors to store and search. | Best fit for this week. |
| Small chunks | Precise hits. | May lack context and can split ideas too aggressively. | Use overlap and inspect results. |
| Large chunks | More context per hit. | Relevant details can be diluted. | Avoid making chunks as large as full papers. |
| No overlap | Less duplicated text and fewer vectors. | Boundary ideas can be lost. | Useful only when chunk boundaries are already semantic. |
| Overlap | Safer boundaries. | More storage and possible duplicate-looking hits. | A practical default for beginner chunking. |
| Real local model | Meaningful semantic vectors without an API key. | Heavier dependency and slower startup than a fake. | Use for real search behavior, not unit tests. |
| Fake embedder | Fast, deterministic, offline tests. | Does not measure true semantic quality. | Use for unit tests of control flow and ranking. |
| Linear scan top-k | Easy to understand and test. | Slow for very large indexes. | Acceptable for the learning milestone. |
| Embedding cache | Saves repeated model calls. | Can become stale if keys ignore model identity. | Use clear keys and tests. |

## Testing implications

Testing semantic search requires separating deterministic behavior from model quality.

Deterministic behavior belongs in unit tests.

Model quality belongs in manual checks or carefully marked integration checks.

The syllabus names these Week 13 tests:

- `tests/unit/test_chunking.py`
- `tests/unit/test_vector_search.py`

The Week 13 README also mentions semantic retrieval integration tests as a useful deliverable.

Unit test ideas:
- A short document produces exactly one chunk.
- A longer document produces overlapping chunks with expected `start_word` values.
- `overlap >= chunk_size` raises `ValueError`.
- The first chunk index is `0`.
- Every chunk includes `source_id`.
- Cosine similarity of identical non-zero vectors is close to `1.0`.
- Cosine similarity of perpendicular vectors is close to `0.0`.
- Mismatched vector lengths raise `ValueError`.
- Zero vectors follow the chosen convention.
- Top-k search returns an empty list for an empty index.
- Top-k search returns all hits when `top_k` is larger than the index.
- Sorting places the highest score first.
- The fake embedder returns the same vector for the same text every time.
- The cache calls the underlying embedder only once for repeated text and model name.

A deterministic fake embedder is essential because it lets you compute expected behavior by hand.

Do not write a unit test that passes only if a real model has already been downloaded.

That kind of test is slow, fragile, and unfair to a fresh development machine.

A useful test name tells the behavior, such as `test_search_returns_highest_cosine_score_first`.

## Architecture implications

The architecture rule for Week 13 is simple: keep dependencies pointing inward.

`src/researchops/search/` is infrastructure.

It may import Python standard-library tools and third-party embedding libraries allowed for this week.

`src/researchops/core/interfaces.py` is core.

Core must not import from `search/`, `storage/`, `cli/`, `api/`, or any other ResearchOps layer.

Services should depend on protocols, not concrete sentence-transformer classes.

CLI commands should delegate instead of containing ranking formulas.

The approved import direction is:

```text
CLI / API / Worker
    -> Services / Use Cases
        -> Core Models + Protocols
Infrastructure such as search/ implements or supports those contracts from the outside.
```

For Week 13, ask these boundary questions during review:
- Does `core/` stay free of `sentence_transformers` imports?
- Does `services/` avoid constructing `SentenceTransformer` directly?
- Does `cli/` avoid implementing cosine similarity?
- Do fake implementations live under `tests/fakes/` rather than inside production modules?
- Does `search/embeddings.py` hide local-model details behind a small embedder interface?
- Does `search/vector_search.py` know about vectors and hits, not terminal display formatting?

## How this connects to AI engineering / ML research

AI engineering is not only model training.

It is also building dependable systems around model outputs.

Semantic search is a practical example.

The embedding model gives ResearchOps a numeric representation of text meaning.

Engineering turns that representation into a reliable feature.

A research workflow needs traceability.

If a search result influences a literature review, the researcher must know where the passage came from.

A research workflow needs reproducibility.

If chunk size changes from 300 to 800, top results can change.

A research workflow needs tests.

If cosine sorting reverses accidentally, the tool quietly recommends worse papers first.

A research workflow needs honest evaluation.

A passing arithmetic test does not prove a search result is useful to a scientist.

This week sits at the boundary between machine learning and software engineering.

The model supplies vectors.

The software supplies chunking, caching, ranking, metadata, tests, and debugging discipline.

## Mini quizzes

1. **Question:** What is an embedding?
   **Answer:** A dense numeric vector that represents the meaning of a piece of text.

2. **Question:** Why is keyword search not enough?
   **Answer:** It matches exact words and can miss synonyms, paraphrases, and related phrases.

3. **Question:** Why chunk a long paper?
   **Answer:** A whole-paper vector is too broad; chunks let search find specific passages.

4. **Question:** What metadata should every chunk carry?
   **Answer:** `source_id`, `chunk_index`, and usually `start_word` plus the chunk text.

5. **Question:** What does cosine similarity compare?
   **Answer:** The direction of two vectors using dot product divided by vector magnitudes.

6. **Question:** Why must compared vectors have the same length?
   **Answer:** Each position represents part of the same vector space; mismatched dimensions make the score meaningless.

7. **Question:** What is a zero vector problem?
   **Answer:** A zero vector has no direction and magnitude zero, so cosine division must be handled deliberately.

8. **Question:** Why use a fake embedder in unit tests?
   **Answer:** It is fast, offline, deterministic, and easy to reason about.

9. **Question:** What should an embedding cache key include?
   **Answer:** At least the text and model identity, commonly hashed into a stable key.

10. **Question:** What does top-k mean?
   **Answer:** Return only the first `k` items after sorting by score descending.

11. **Question:** Where should vector ranking code live?
   **Answer:** `src/researchops/search/vector_search.py` or service-level orchestration, not directly in CLI display code.

12. **Question:** What is retrieval evaluation?
   **Answer:** Checking whether known queries return sensible, traceable top results.

## Explain-it-aloud prompts

- Explain why `efficient transformers` might fail in keyword search but succeed in semantic search.
- Explain what happens to one paper from raw text to chunk metadata.
- Explain what an embedding vector is without saying it is magic.
- Explain why a fake embedder can test ranking even though it is not semantically smart.
- Explain the cosine similarity formula using one two-dimensional example.
- Explain why `overlap >= chunk_size` is dangerous.
- Explain why a search hit without `source_id` is incomplete.
- Explain why the indexing model and query model must match.
- Explain how an embedding cache saves work.
- Explain what you would inspect if all search scores were identical.
- Explain which code belongs in `search/` and which code belongs in `cli/`.
- Explain what Week 13 gives Week 14 before the API layer appears.

## What to memorize

- The Week 13 milestone: `researchops semantic-search "efficient transformers"` returns papers ranked by vector similarity.
- The main files: `search/chunking.py`, `search/embeddings.py`, `search/vector_search.py`, and `core/interfaces.py`.
- The formula: cosine similarity equals dot product divided by the product of vector magnitudes.
- The chunk metadata fields: `source_id`, `chunk_index`, `start_word`, and text.
- The test rule: unit tests use deterministic fake embeddings, not real model downloads.
- The architecture rule: `core/` does not import infrastructure, and services depend on protocols.
- The ranking rule: higher cosine similarity sorts earlier.
- The validation command from the syllabus: `pytest tests/unit/test_chunking.py tests/unit/test_vector_search.py -v`.

## What to understand deeply

- Embedding vectors are useful because similar meanings should produce similar numeric directions.
- Chunking is not busywork; it controls retrieval precision and source traceability.
- Cosine similarity is simple arithmetic, but only meaningful when vector dimensions match.
- A local model removes API-key requirements, but unit tests still need fakes.
- A cache improves speed only if it does not mix incompatible model outputs.
- Search quality must be inspected with realistic paper snippets, not only formula tests.
- Architecture boundaries keep the model implementation replaceable and the command layer thin.

## What not to worry about yet

- Do not worry about specialized vector databases this week; a clear top-k scan is enough for the milestone.
- Do not worry about web request handling; Week 14 introduces the API layer.
- Do not worry about async network fetching; that comes later.
- Do not worry about container deployment; this is still a local CLI-first learning path.
- Do not build future question-answering behavior; Week 13 is retrieval only.
- Do not optimize for millions of embeddings before the small, correct version works.
- Do not compare every possible embedding model; start with one local model and one fake test embedder.
- Do not add unrequested dependencies beyond what the curriculum already expects.

## Bridge to next week

Next week is Week 14: **FastAPI Layer**.

Week 14 exposes proven ResearchOps behavior over HTTP.

That only works well if Week 13 keeps semantic search behavior cleanly separated from the command line.

If vector ranking lives in `search/` or a service, a future route can call the same behavior without copying logic.

If vector ranking is buried inside a Typer command, the API would either duplicate it or import the wrong layer.

So the bridge is architectural as much as technical.

Before moving on, make sure you can say:
- where chunking happens,
- where embeddings are generated or faked,
- where cosine similarity is calculated,
- where top-k sorting happens,
- where source metadata is preserved,
- and why the command layer should stay thin.

Week 14 will add HTTP endpoints, request validation, response models, and route tests.

The semantic search lesson to carry forward is: build the behavior once, keep the boundary clean, and let entry points adapt it rather than reinvent it.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
