# Validation — Week 17 RAG Assistant

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 17 — RAG Assistant](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 17 — RAG Assistant** · *validation.md — the checkpoint* (step 5 of 6 this week).

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
8. [Next week → Week 18](../../../curriculum/month-05-production-portfolio/week-18-docker-environment-config/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 18 — Docker & Environment Config](../../../curriculum/month-05-production-portfolio/week-18-docker-environment-config/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 5 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 5 overview](../README.md) · [📄 Week 17 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
