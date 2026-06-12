
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 13 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation — Week 13 Embeddings and Semantic Search

## Pre-validation checklist

Before running anything, confirm:

- [ ] Your virtual environment is active and `.[dev,ml]` is installed.
- [ ] Chunking produces chunks that each carry a **source reference**.
- [ ] There is a clear separation between a **real** embedder and a **fake**
      embedder used in tests.
- [ ] No test reaches out to download a model from the internet.

## Commands to run

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,ml]"
ruff check src tests
pytest tests/unit/test_chunking.py -v
pytest tests/unit/test_semantic_search.py -v
pytest tests/integration/test_semantic_retrieval.py -v
pytest -q
```

## Expected outputs

Expected output is not one giant exact transcript because package installers and pytest counts can vary slightly. The important part is that every command ends successfully and shows the right kind of evidence.

- `source .venv/bin/activate` prints nothing. Your shell prompt may change to show the virtual environment.
- `python -m pip install -e ".[dev,ml]"` ends with a successful editable install message. It may say requirements are already satisfied. It must not end with `ERROR`, dependency resolution failure, or permission errors.
- `ruff check src tests` ends with `All checks passed!`. If it prints file names and rule codes, fix those before moving on.
- `pytest tests/unit/test_chunking.py -v` shows each chunking test as `PASSED`. Look for tests proving empty input, invalid overlap, sliding-window boundaries, and source metadata.
- `pytest tests/unit/test_semantic_search.py -v` shows vector-scoring and ranking tests as `PASSED`. Look for tests covering identical vectors, zero vectors, mismatched dimensions, descending score order, and `top_k`.
- `pytest tests/integration/test_semantic_retrieval.py -v` shows an end-to-end retrieval path as `PASSED`: text is chunked, chunks are embedded, the query is embedded, and the returned hit still names its source document.
- `pytest -q` finishes with a green summary such as `... passed`. Warnings are acceptable only if they are understood and not hiding model downloads, network access, or skipped Week 13 behavior.

Behavior you should be able to observe after the commands pass:

- Chunking splits documents deterministically, and every chunk knows its source.
- Cosine-similarity ranking returns the most relevant chunks first.
- Integration retrieval returns relevant hits that point back to their source document.
- The full suite passes without any network access or real model construction inside unit tests.

## Tests that must pass

- `tests/unit/test_chunking.py`
- `tests/unit/test_semantic_search.py`
- `tests/integration/test_semantic_retrieval.py`
- `pytest -q` (whole suite, coverage above threshold)

## Manual checks

- Run a semantic query you know the answer to; confirm the top hit is sensible and
  cites a real source document.
- Run a nonsense query; confirm ranking degrades gracefully rather than erroring.
- Compare a keyword search and a semantic search for the same intent; note where
  semantic wins.

## Architecture checks

- The embedder is accessed through an interface/protocol (`EmbeddingModel`), not
  imported concretely inside services.
- Chunking and ranking logic live in the appropriate module, not in the CLI.
- Services do not import a heavy ML model directly; the real model is wired at the
  composition root.

```bash
grep -rn "import sentence_transformers\|SentenceTransformer" src/researchops/services/ --include="*.py"
# Expected: no output
```

## Documentation checks

- `notes.md` explains embeddings, chunking, and cosine similarity in your own
  words.
- The chunk-to-source mapping is documented so the citations in Week 17 can rely
  on it.

## Do-not-proceed warnings

**Do not proceed to Week 14 if:**

- Semantic search "works" only because of **hardcoded or fake data** baked into
  the path — it must work over real chunked content.
- The responsibilities of the **real embedder** and the **fake embedder** are
  confused or interchangeable in a way that hides bugs.
- Tests **download models** unnecessarily (tests must be offline and fast).
- A result can rank text but cannot tell you which paper or chunk produced the hit.
- `overlap >= chunk_size` can reach production code; that is an infinite-loop risk, not a cosmetic issue.
- Vector length mismatches are silently ignored with `zip` instead of failing loudly.

## Ruthless mentor checkpoint

- "Show me the source reference on a chunk. If Week 17 asked 'where did this come
  from?', could you answer from the data alone?"
- "Which embedder runs in your tests — the real one or the fake? Prove it does not
  hit the network."
- "Explain the vector search flow end to end without reading the code."

## Definition of done

- [ ] Chunking exists and attaches source metadata to each chunk.
- [ ] An embedder interface exists; a fake embedder backs the tests.
- [ ] Cosine similarity is implemented and tested.
- [ ] Semantic top-k retrieval works and maps hits to sources.
- [ ] Empty-query behavior is defined.
- [ ] Tests run offline; `pytest -q` passes; `ruff` is clean.
- [ ] You can explain the full vector search flow aloud.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 13 — Embeddings and Semantic Search:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
