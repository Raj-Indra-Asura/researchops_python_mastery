# Notes - Week 13 Embeddings and Semantic Search

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 13 — Embeddings & Semantic Search](./README.md) › **notes.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Why keyword search is not enough

Keyword search finds documents that contain the words you typed. That sounds useful, and it often is. But it has a hard limit: it matches letters, not ideas.

Suppose a researcher stored a paper that calls a technique "dense retrieval" and later queries for "vector search". Keyword search finds nothing, even though the paper is deeply relevant. The problem is that natural language is rich and inconsistent. Authors use synonyms, abbreviations, domain-specific terms, and different phrasing for the same concept.

Semantic search tries to find documents that mean the same thing as the query, even if the exact words do not appear. To do that, text must be converted into a mathematical form that captures meaning. That form is called an embedding.

---

## What an embedding is

An embedding is a list of numbers that represents the meaning of a piece of text.

Here is the most important intuition: text that means similar things should produce numbers that are close together. Text that means different things should produce numbers that are far apart.

For example:
- "neural network" and "deep learning model" should have similar numbers.
- "neural network" and "tomato soup" should have very different numbers.

The list of numbers is called a vector. A vector is just a sequence of floating-point values, like `[0.12, -0.45, 0.87, ...]`. The length of that list is called the number of dimensions.

---

## Vector intuition and dimensions

Think of a two-dimensional vector as a point on a map. `[3.0, 1.0]` is a location. `[3.1, 0.9]` is a nearby location. `[-5.0, 8.0]` is far away.

Real embedding models use hundreds or thousands of dimensions. You cannot visualize 384 dimensions, but the math works the same way. Two vectors are close if their values are similar across all dimensions.

A popular small model called `all-MiniLM-L6-v2` produces 384-dimensional vectors. A larger model might produce 768 or 1536 dimensions. More dimensions can capture finer distinctions, but require more memory and compute.

The key insight: you do not define what each dimension means. The model learns that during training. The model has seen enormous amounts of text and has learned to encode meaning as geometry.

---

## Cosine similarity

To compare two vectors, you need a distance or similarity measure. The most common is cosine similarity.

Cosine similarity measures the angle between two vectors, not the distance between their endpoints. Two vectors pointing in exactly the same direction have cosine similarity of 1.0. Two vectors pointing in opposite directions have cosine similarity of -1.0. Two unrelated vectors point in roughly perpendicular directions and have cosine similarity near 0.

```python
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))      # line 1
    norm_a = math.sqrt(sum(x * x for x in a))   # line 2
    norm_b = math.sqrt(sum(y * y for y in b))   # line 3
    return dot / (norm_a * norm_b)               # line 4
```

Line 1: compute the dot product. Multiply matching positions and sum. Two vectors pointing the same direction produce a large positive dot product.

Line 2: compute the magnitude (length) of vector `a`. Square each element, sum them, take the square root.

Line 3: compute the magnitude of vector `b`.

Line 4: divide the dot product by the product of magnitudes. This normalises by how long the vectors are, so only direction matters. The result is always between -1 and 1.

Why cosine and not Euclidean distance? Because embedding magnitudes can vary. A long text might produce a larger-magnitude vector than a short text. Cosine similarity ignores magnitude and compares only direction, which gives more stable similarity scores.

---

## Why long documents need chunking

A research paper can be 10 000 words or more. If you embed the entire paper as one vector, that single vector must encode everything: abstract, methods, results, conclusion. When a user queries for a specific technique described in the methods section, the whole-document embedding is too diluted. The signal from that one section is washed out.

Chunking solves this by splitting the document into smaller pieces. Each chunk is embedded separately. When a user queries, you compare the query vector to all chunk vectors and retrieve the most relevant chunks. This gives much finer-grained retrieval.

### Chunk size

Chunk size is measured in tokens or words. Common values are 200–500 words. Smaller chunks are more precise but provide less context per hit. Larger chunks provide more context but reduce precision.

A good default for research papers is 300 words. Start there and adjust based on qualitative inspection of results.

### Overlap

If you cut a document into non-overlapping windows, you risk splitting a sentence or idea across two chunks. Overlap solves this by repeating some words at the boundary between consecutive chunks.

For example, with chunk size 300 and overlap 50, chunk 1 covers words 0–299, chunk 2 covers words 250–549, chunk 3 covers words 500–799, and so on.

```python
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()          # line 1
    chunks: list[str] = []        # line 2
    start = 0                     # line 3
    while start < len(words):     # line 4
        end = min(len(words), start + chunk_size)       # line 5
        chunks.append(" ".join(words[start:end]))       # line 6
        start = end - overlap                           # line 7
    return chunks                 # line 8
```

Line 1: split the text on whitespace. This is a simple word-level split.

Line 2: accumulate chunks in a list.

Line 3: start at the beginning.

Line 4: keep going while there are still words.

Line 5: clip `end` so the last chunk does not exceed the document length.

Line 6: join the words back into a string and add it to the list.

Line 7: advance `start` by `chunk_size - overlap`. The overlap amount is repeated in the next chunk.

Line 8: return all chunks.

Edge case: if `overlap >= chunk_size`, `start` never advances and the loop runs forever. Always validate that `overlap < chunk_size` before calling this function.

### Chunk metadata

Every chunk must carry metadata linking it back to its source document. Without that link, retrieval is useless: the user gets a passage but cannot find the paper it came from.

Metadata should include at minimum:
- `source_id` — the document's unique identifier
- `chunk_index` — the position within the document
- `start_word` — where in the document this chunk begins

---

## The embedding pipeline

The full semantic retrieval process has two phases.

**Indexing phase** (run once per document):
1. Parse the document into clean text.
2. Chunk the text.
3. Embed each chunk using a model.
4. Store each (chunk_text, embedding, metadata) tuple.

**Query phase** (run for each search query):
1. Embed the query using the same model.
2. Compare the query embedding to all stored chunk embeddings.
3. Sort by cosine similarity descending.
4. Return the top-k chunks and their metadata.

The model used for indexing and querying must be the same. If you index with one model and query with another, the vector spaces are incompatible and the comparisons are meaningless.

---

## Using sentence-transformers locally

Install the library:

```bash
pip install -U sentence-transformers
```

Minimal example:

```python
from sentence_transformers import SentenceTransformer          # line 1

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # line 2
texts = ["attention mechanism", "convolutional neural networks"]        # line 3
embeddings = model.encode(texts)                                        # line 4
print(embeddings.shape)                                                 # line 5
```

Line 1: import the `SentenceTransformer` class. This class wraps a pretrained transformer model.

Line 2: load the model by name. On the first run this downloads the weights from the Hugging Face Hub (about 90 MB). On subsequent runs the weights are cached locally.

Line 3: a list of two short text strings. These are what you want to embed.

Line 4: `encode` takes a list of strings and returns a NumPy array of shape `(n_texts, embedding_dim)`. For this model that is `(2, 384)`.

Line 5: print `(2, 384)`. Two texts, 384 dimensions each.

To embed a single string, pass a list with one element: `model.encode(["my query"])`.

---

## Local models versus API embeddings

|                    | Local model (`sentence-transformers`) | API (OpenAI, Cohere, etc.) |
|--------------------|---------------------------------------|---------------------------|
| **Cost per call**  | Free after download                  | Pay per token              |
| **Latency**        | Milliseconds on CPU, faster on GPU   | Hundreds of milliseconds   |
| **Privacy**        | Text never leaves your machine       | Text sent to third party   |
| **Setup**          | Larger install (~90 MB model)        | Just an API key            |
| **Reproducibility**| Fully deterministic                  | Provider may change models |

For a learning project, local models are better: free, private, and reproducible.

The tradeoff for production: large-scale embedding via API may be cheaper than running a GPU server, but you lose control over versioning and privacy.

---

## The embedding interface and why it matters

Your code should not call `SentenceTransformer` directly everywhere. Wrap it behind a simple interface (a Protocol in Python terms).

```python
from typing import Protocol


class EmbeddingModel(Protocol):
    def embed(self, text: str) -> list[float]:
        ...
```

Any class that has an `embed(self, text: str) -> list[float]` method satisfies this protocol, without inheriting from it. This is called structural subtyping.

With this interface you can swap implementations:
- `SentenceTransformerEmbedder` for real use
- `FakeEmbeddingModel` for tests
- `OpenAIEmbedder` for cloud use

---

## Deterministic fake embeddings for tests

Real models are slow to load, require downloaded weights, and are non-deterministic across platforms. Tests must be fast, offline, and fully reproducible.

Use a fake that produces tiny deterministic vectors:

```python
class FakeEmbeddingModel:
    def embed(self, text: str) -> list[float]:
        return [float(len(text)), float(text.count(" ")), float(text.lower().count("a"))]
```

Line by line:
- `len(text)`: the number of characters. Longer texts produce a higher first dimension.
- `text.count(" ")`: the number of spaces, which approximates word count.
- `text.lower().count("a")`: the number of letter "a" characters.

This produces a 3-dimensional vector. That is enough to test cosine similarity ranking. You do not need 384 dimensions to check that your ranking logic sorts correctly.

Why is this better than using real embeddings in tests?
1. No internet or file download required.
2. Runs in microseconds.
3. The output is predictable: you can calculate expected similarity by hand.
4. CI does not need the `sentence-transformers` package installed.

The fake is honest about what it tests: ranking logic, not embedding quality. When you want to test embedding quality, write separate integration tests that use the real model and mark them as slow or optional.

---

## Embedding cache

Computing embeddings for thousands of chunks is expensive (slow, even on CPU). If you re-index the same document twice, you waste time. An embedding cache stores previously computed embeddings and returns them on subsequent calls without calling the model.

A simple cache key is the hash of the chunk text. If the text has not changed, return the cached embedding.

```python
import hashlib


class CachedEmbedder:
    def __init__(self, model: EmbeddingModel) -> None:
        self._model = model
        self._cache: dict[str, list[float]] = {}

    def embed(self, text: str) -> list[float]:
        key = hashlib.sha256(text.encode()).hexdigest()
        if key not in self._cache:
            self._cache[key] = self._model.embed(text)
        return self._cache[key]
```

This in-memory cache lives only for the lifetime of the object. For a persistent cache, write to SQLite or a file.

---

## Vector search and top-k retrieval

Once embeddings are stored, vector search is a loop:
1. Embed the query.
2. Compute cosine similarity between the query and each stored chunk.
3. Sort results by similarity descending.
4. Return the top-k results.

```python
from dataclasses import dataclass


@dataclass
class SearchHit:
    chunk_text: str
    score: float
    source_id: str
    chunk_index: int


def search(
    query_embedding: list[float],
    index: list[tuple[list[float], str, str, int]],
    top_k: int = 5,
) -> list[SearchHit]:
    scored = []
    for embedding, chunk_text, source_id, chunk_index in index:
        score = cosine_similarity(query_embedding, embedding)
        scored.append(SearchHit(chunk_text, score, source_id, chunk_index))
    scored.sort(key=lambda h: h.score, reverse=True)
    return scored[:top_k]
```

The `index` parameter is a list of tuples: (embedding, chunk_text, source_id, chunk_index). In production you might use a vector database like FAISS or Chroma for faster search, but a plain list works for hundreds of documents.

---

## Retrieval quality

How do you know if semantic search is working well? For this week, qualitative inspection is enough:
1. Index several papers.
2. Run queries that should match specific passages.
3. Inspect the top-3 hits.
4. Ask: does any hit match even though the exact words are absent?

For example: query "gradient descent optimisation" should retrieve a passage about "back-propagation and weight updates" even without the word "gradient" appearing.

When retrieval fails, common causes are:
- Chunk size too large (query gets diluted)
- Chunk size too small (too little context)
- Wrong model for the domain
- Query too short to have a meaningful embedding

---

## File locations in this project

The problem statement specifies these files. Use exactly these paths:

```
src/researchops/search/chunking.py
src/researchops/search/embeddings.py
src/researchops/search/vector_search.py
```

Not `semantic/`. The `search/` package already exists. Place your implementations there.

---

## Why RAG depends on retrieval

RAG stands for Retrieval-Augmented Generation. It is a pattern where you:
1. Retrieve relevant chunks from your document collection.
2. Pass those chunks as context to a language model.
3. The language model generates an answer using that context.

Step 1 is the retrieval step. If retrieval is bad — if it returns irrelevant chunks — the language model produces unreliable or hallucinated answers. Good retrieval is the foundation of good RAG.

This is why Week 13 matters so much. You are not just building search. You are building the retrieval foundation that Month 5's RAG assistant will depend on.

---

## Summary

- Keyword search matches words; semantic search matches meaning.
- An embedding is a list of numbers representing text meaning.
- Similar texts have similar (close) vectors; different texts have distant vectors.
- Cosine similarity measures the angle between two vectors, ignoring magnitude.
- Documents must be chunked before embedding; whole-document embeddings are too coarse.
- Overlap at chunk boundaries prevents ideas from being cut in half.
- Every chunk must carry metadata linking back to its source document.
- Use the same model for indexing and querying.
- Use a fake embedder for unit tests; real models in integration tests.
- `sentence-transformers` provides free, local, reproducible embeddings.
- The embedding interface decouples your code from any specific model.
- Retrieval quality is the foundation of RAG systems.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 13 — Embeddings & Semantic Search** · *notes.md — the textbook chapter* (step 2 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [README](./README.md)
- ▶ **Next:** [exercises.md](./exercises.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. **➡ [notes.md](./notes.md) ← you are here**
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
