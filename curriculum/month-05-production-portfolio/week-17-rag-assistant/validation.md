
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 17 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 17 — RAG Assistant:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation — Week 17 RAG Assistant

## 1. Pre-validation checklist

- [ ] `.[dev,ml,api]` is installed in an active virtual environment.
- [ ] Every answer is built from retrieved chunks and **cites** them.
- [ ] The assistant can return an **"insufficient evidence"** response.
- [ ] Tests use a **fake generator** — no real LLM, no network.

## 2. Exact commands

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,ml,api]"
ruff check src tests
pytest tests/unit/test_rag_prompting.py -v
pytest tests/integration/test_rag_answering.py -v
pytest -q
```

## 3. Expected behavior

- Answerable questions produce grounded answers **with citations** to the
  supporting chunks.
- Unanswerable questions produce an honest "insufficient evidence" response rather
  than a confident fabrication.
- The whole suite runs with a fake generator, offline.

## 4. Tests that must pass

- `tests/unit/test_rag_prompting.py`
- `tests/integration/test_rag_answering.py`
- `pytest -q` (whole suite)

## 5. Manual checks

- Ask a question the corpus supports; confirm the answer cites real chunks.
- Ask a question the corpus cannot support; confirm the fallback fires.
- Inspect one citation; confirm it traces back to a real source document.

## 6. Architecture checks

- The generator is behind an interface; the real provider and the fake generator
  are interchangeable adapters.
- Retrieval feeds generation; the RAG service depends on protocols, not concrete
  models.

```bash
grep -rn "openai\|anthropic\|import requests" src/researchops/services/ --include="*.py"
# Expected: no hard-coded provider calls inside services
```

## 7. Documentation checks

- `notes.md` explains the full RAG pipeline and the citation format.
- The "insufficient evidence" policy is documented.

## 8. Do-not-proceed warnings

**Do not proceed to Week 18 if:**

- **Answers do not cite chunks** — grounding without traceable citations is not
  trustworthy.
- **The system cannot say "insufficient evidence"** — it must decline rather than
  hallucinate.
- **Tests require a real LLM** — the suite must pass with the fake generator,
  offline.

## 9. Ruthless mentor checkpoint

- "Show me an answer and trace each citation back to its chunk and source."
- "Ask something unanswerable. Does it refuse, or invent?"
- "Run the RAG tests with no network. Do they pass with the fake generator?"

## 10. Definition of done

- [ ] Prompt builder and retrieval-to-answer flow exist.
- [ ] Every answer maps to citations that trace to sources.
- [ ] An "insufficient evidence" fallback exists and is tested.
- [ ] A fake generator backs all tests; no real LLM is required.
- [ ] A real provider can be swapped in behind the same interface.
- [ ] `pytest -q` passes offline; `ruff` clean.
- [ ] You can explain the full RAG pipeline aloud.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 17 — RAG Assistant:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
