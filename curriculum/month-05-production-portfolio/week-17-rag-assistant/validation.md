# Validation - Week 17 RAG Assistant

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,ml,api]"
pytest tests/unit/test_rag_prompting.py -v
pytest tests/integration/test_rag_answering.py -v
```

## Expected outputs
- Prompt-building tests pass.
- Integration answer tests pass with citations included.
- Unsupported questions return a fallback or low-evidence response.

## Pytest commands and expected results
```bash
pytest -k "rag_prompting or rag_answering" -v
pytest -q
```

Expected result: the assistant uses retrieved context, produces answers with traceable citations, and avoids confident unsupported claims when evidence is missing.

## Completion checklist
- [ ] Prompt builder exists.
- [ ] Retrieval is connected to answer generation.
- [ ] Citation mapping exists.
- [ ] Empty-context behavior is defined.
- [ ] Tests cover grounded behavior.
- [ ] Citation output is human-readable.
- [ ] Unsupported-claim fallback exists.
- [ ] Integration tests pass.
- [ ] `pytest -q` passes.
- [ ] You can explain the full RAG pipeline.
