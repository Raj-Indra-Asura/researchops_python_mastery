# Week 17 - RAG Assistant

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › **Week 17 — RAG Assistant**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Learning objectives
- Understand retrieval-augmented generation as a pipeline.
- Combine search results with prompt construction.
- Require citations or evidence links in answers.
- Reduce hallucination by grounding responses in retrieved chunks.
- Evaluate answer quality and citation usefulness.
- Design prompts that separate instructions, context, and user question.
- Build a first ResearchOps assistant workflow.

## Project milestone
Create a retrieval-grounded assistant that answers questions using retrieved ResearchOps documents and returns citations to supporting chunks.

## Files to modify/create
- `src/researchops/rag/prompting.py`
- `src/researchops/rag/assistant.py`
- `src/researchops/rag/citations.py`
- `tests/unit/test_rag_prompting.py`
- `tests/integration/test_rag_answering.py`

## Concepts covered
RAG pipelines, prompting, context windows, grounding, citations, answer evaluation, and failure boundaries.

## Expected deliverables
- A retrieval step that fetches supporting chunks.
- Prompt assembly that includes instructions and evidence.
- Answer objects with citations.
- Tests for prompt structure and grounded-answer flow.

## Definition of done
- [ ] Retrieval feeds the assistant.
- [ ] Prompt template is explicit.
- [ ] Answers include citations.
- [ ] Empty-context behavior is defined.
- [ ] Tests cover prompt and answer shape.
- [ ] You can explain how grounding reduces hallucination.
- [ ] The assistant refuses unsupported claims when evidence is weak.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 17 — RAG Assistant** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 16 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
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
