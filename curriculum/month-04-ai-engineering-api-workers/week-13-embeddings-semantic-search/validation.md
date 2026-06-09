# Validation - Week 13 Embeddings and Semantic Search

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,ml]"
pytest tests/unit/test_chunking.py -v
pytest tests/unit/test_semantic_search.py -v
pytest tests/integration/test_semantic_retrieval.py -v
```

## Expected outputs
- Chunking tests pass.
- Semantic ranking tests pass deterministically.
- Integration retrieval test returns relevant chunk hits with source metadata.

## Pytest commands and expected results
```bash
pytest -k "chunking or semantic_search or semantic_retrieval" -v
pytest -q
```

Expected result: chunked embeddings can be indexed and queried, cosine similarity drives ranking correctly, and each hit points back to its original document.

## Completion checklist
- [ ] Chunking function exists.
- [ ] Chunk metadata includes source reference.
- [ ] Embedder interface or implementation exists.
- [ ] Cosine similarity is tested.
- [ ] Semantic top-k retrieval works.
- [ ] Empty-query behavior is defined.
- [ ] Integration retrieval test passes.
- [ ] Keyword versus semantic behavior is compared.
- [ ] `pytest -q` passes.
- [ ] You can explain the vector search flow end to end.
