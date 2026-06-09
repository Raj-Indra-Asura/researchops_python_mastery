<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 17 — RAG Assistant:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 16 Reflection](../../month-04-ai-engineering-api-workers/week-16-local-worker-job-system/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 17 - RAG Assistant

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
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 16 Reflection](../../month-04-ai-engineering-api-workers/week-16-local-worker-job-system/reflection.md) · ➡️ [Notes →](notes.md)

**Week 17 — RAG Assistant:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
