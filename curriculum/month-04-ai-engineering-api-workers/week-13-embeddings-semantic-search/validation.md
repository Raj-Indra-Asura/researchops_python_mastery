# Validation — Week 13 Embeddings and Semantic Search

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 4](../README.md) › [Week 13 — Embeddings & Semantic Search](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## 1. Pre-validation checklist

Before running anything, confirm:

- [ ] Your virtual environment is active and `.[dev,ml]` is installed.
- [ ] Chunking produces chunks that each carry a **source reference**.
- [ ] There is a clear separation between a **real** embedder and a **fake**
      embedder used in tests.
- [ ] No test reaches out to download a model from the internet.

## 2. Exact commands

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,ml]"
ruff check src tests
pytest tests/unit/test_chunking.py -v
pytest tests/unit/test_semantic_search.py -v
pytest tests/integration/test_semantic_retrieval.py -v
pytest -q
```

## 3. Expected behavior

- Chunking splits documents deterministically, and every chunk knows its source.
- Cosine-similarity ranking returns the most relevant chunks first.
- Integration retrieval returns relevant hits that point back to their source
  document.
- The full suite passes without any network access.

## 4. Tests that must pass

- `tests/unit/test_chunking.py`
- `tests/unit/test_semantic_search.py`
- `tests/integration/test_semantic_retrieval.py`
- `pytest -q` (whole suite, coverage above threshold)

## 5. Manual checks

- Run a semantic query you know the answer to; confirm the top hit is sensible and
  cites a real source document.
- Run a nonsense query; confirm ranking degrades gracefully rather than erroring.
- Compare a keyword search and a semantic search for the same intent; note where
  semantic wins.

## 6. Architecture checks

- The embedder is accessed through an interface/protocol (`EmbeddingModel`), not
  imported concretely inside services.
- Chunking and ranking logic live in the appropriate module, not in the CLI.
- Services do not import a heavy ML model directly; the real model is wired at the
  composition root.

```bash
grep -rn "import sentence_transformers\|SentenceTransformer" src/researchops/services/ --include="*.py"
# Expected: no output
```

## 7. Documentation checks

- `notes.md` explains embeddings, chunking, and cosine similarity in your own
  words.
- The chunk-to-source mapping is documented so the citations in Week 17 can rely
  on it.

## 8. Do-not-proceed warnings

**Do not proceed to Week 14 if:**

- Semantic search "works" only because of **hardcoded or fake data** baked into
  the path — it must work over real chunked content.
- The responsibilities of the **real embedder** and the **fake embedder** are
  confused or interchangeable in a way that hides bugs.
- Tests **download models** unnecessarily (tests must be offline and fast).

## 9. Ruthless mentor checkpoint

- "Show me the source reference on a chunk. If Week 17 asked 'where did this come
  from?', could you answer from the data alone?"
- "Which embedder runs in your tests — the real one or the fake? Prove it does not
  hit the network."
- "Explain the vector search flow end to end without reading the code."

## 10. Definition of done

- [ ] Chunking exists and attaches source metadata to each chunk.
- [ ] An embedder interface exists; a fake embedder backs the tests.
- [ ] Cosine similarity is implemented and tested.
- [ ] Semantic top-k retrieval works and maps hits to sources.
- [ ] Empty-query behavior is defined.
- [ ] Tests run offline; `pytest -q` passes; `ruff` is clean.
- [ ] You can explain the full vector search flow aloud.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 4 — AI Engineering, API, Async, Workers · **Week 13 — Embeddings & Semantic Search** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
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
