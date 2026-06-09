# Notes - Week 13 Embeddings and Semantic Search

Keyword search depends on exact terms. Semantic search tries to retrieve meaning. The core idea is to convert text into vectors called embeddings. If two passages discuss similar ideas, their vectors should be close together in embedding space even if they do not share many exact words.

Because documents can be long, semantic search usually works on chunks rather than whole files. A chunk is a smaller span of text, such as 200-500 words with some overlap. Chunking improves retrieval because a whole paper may cover many topics, but the user often needs one specific passage.

```python
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return chunks
```

The exact chunking logic can vary, but the principle is stable: preserve enough context while keeping chunks small enough to retrieve precisely.

Embeddings may come from a local model, an API, or a fake implementation during testing. This is another place where protocols help. Your semantic search service should depend on an embedding interface, not on one provider.

Cosine similarity measures how aligned two vectors are. If vectors point in a similar direction, the cosine similarity is closer to 1.

```python
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)
```

Semantic retrieval usually works like this:
1. chunk documents
2. compute and store embeddings for each chunk
3. embed the query
4. compare query vector to stored chunk vectors
5. return top-k chunks and metadata

A search hit should include the chunk text, score, and a link back to the source document. That link matters because retrieval is not the final answer; it is evidence for later workflows like RAG.

Evaluation this week is mostly qualitative. Ask whether semantic results retrieve conceptually related passages that keyword search misses. For example, a query for `semantic retrieval` might still retrieve a chunk discussing `dense vector search`.

Be honest about trade-offs. Semantic search can retrieve meaning better, but it is more complex. You must manage chunking, vector storage, model dependencies, and scoring. That is why having a solid keyword baseline was worthwhile first.

Testing semantic systems does not require a real large model in every test. Use fixed small vectors or fake embedders to verify ranking logic deterministically. Reserve integration tests for the full indexing and retrieval flow.

This week introduces a major shift in the project: documents are no longer only strings to match literally. They become items in a vector space, which opens the door to retrieval-augmented generation and more helpful search experiences.
