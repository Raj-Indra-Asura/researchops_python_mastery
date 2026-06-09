<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 17 — RAG Assistant:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 16 Reflection](../../month-04-ai-engineering-api-workers/week-16-local-worker-job-system/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 17 - RAG Assistant

## 1. Week title
Week 17 is **RAG Assistant: Answers grounded in evidence**.
This is the first chapter where ResearchOps uses an LLM-style generator.
The goal is not to build a generic chatbot.
The goal is to answer questions from the indexed research-paper library with citations.
## 2. Story of the week
A researcher has ingested papers, searched them, trained models, exposed an API, fetched documents, and queued work.
Now the researcher wants to ask a question in plain English.
ResearchOps should search the paper library, gather relevant chunks, and produce a short answer grounded in those chunks.
If the library does not contain enough evidence, ResearchOps should say so instead of guessing.
## 3. What you already know
You already know how papers enter the system, how storage works, how services protect business logic, and how semantic search finds chunks by meaning.
You also know that CLI and API entry points should delegate to services.
Week 17 assumes Week 13 semantic search and Week 14 entry-point boundaries are familiar enough to reuse.
## 4. What this week adds
This week adds a retrieve-then-generate workflow.
It adds prompt templates in `src/researchops/ai/prompts.py`.
It adds `QAService` orchestration in `src/researchops/services/qa_service.py`.
It adds the `researchops ask QUESTION` user experience.
It adds citations and insufficient-evidence behavior.
## 5. Why this week matters
A research assistant that cannot cite evidence is risky.
A model can produce fluent answers that are not supported by the user's papers.
RAG reduces that risk by making search the source of truth and generation the summarizer.
This week turns ResearchOps from a search tool into an evidence-grounded assistant.
## 6. Learning objectives
- Explain RAG as retrieval plus generation.
- Retrieve top-k chunks using the Week 13 semantic search capability.
- Build a grounded prompt with instructions, context, question, and citation rules.
- Call a generator through a testable interface.
- Return answers with citations.
- Handle no-context cases safely.
- Test the workflow with fakes instead of real model calls.
## 7. Project milestone
`researchops ask "What are transformers used for?"` returns an answer based on retrieved chunks and includes source citations.
When no relevant chunks exist, the command returns an insufficient-evidence message.
The service test proves retrieval, prompt construction, generation, and citations without requiring a real model.
## 8. Files/modules touched
- `src/researchops/services/qa_service.py` — owns the RAG workflow.
- `src/researchops/ai/prompts.py` — owns prompt templates and formatting helpers.
- `src/researchops/cli/main.py` — wires the `ask` command to the service.
- `src/researchops/search/` — provides semantic retrieval from Week 13.
- `tests/unit/test_qa_service.py` — proves service behavior with fakes.
## 9. Commands introduced
```bash
researchops ask "What are transformers used for?"
pytest tests/unit/test_qa_service.py -v
```
The first command is the user-facing milestone.
The second command is the narrow validation test named by the syllabus.
## 10. Tests involved
The central test file is `tests/unit/test_qa_service.py`.
Tests should use a fake retriever and fake generator.
They should cover the happy path, citation creation, prompt construction, low-score filtering, and no-context fallback.
They should not call a real model or require network access.
## 11. Study plan
Day 1: Read the notes and explain RAG with the desk-assistant mental model.
Day 2: Read Week 13 semantic search files and identify what metadata can become a citation.
Day 3: Design and test the prompt template.
Day 4: Implement or inspect `QAService` orchestration with fakes.
Day 5: Wire the CLI command and run the validation command.
Day 6: Complete break-it and reflection prompts.
## 12. Estimated time breakdown
- Notes reading: 2 to 3 hours.
- Code reading: 1 to 2 hours.
- Prompt/template exercises: 1 hour.
- Service implementation and tests: 3 to 5 hours.
- CLI wiring and manual validation: 1 hour.
- Break-it and reflection: 1 to 2 hours.
## 13. How to know the learner is stuck
The learner is stuck if they want to call the LLM before retrieving chunks.
They are stuck if citations are invented from answer text instead of source metadata.
They are stuck if prompt text is hidden inside CLI code.
They are stuck if tests require a real model.
They are stuck if the assistant answers unsupported questions instead of returning insufficient evidence.
## 14. Definition of done
- [ ] The learner can explain retrieve-then-generate.
- [ ] The prompt includes grounding and citation instructions.
- [ ] `QAService` coordinates retrieval, prompt construction, generation, and citations.
- [ ] Empty or weak retrieval returns insufficient evidence.
- [ ] Tests use fakes and pass for the service behavior.
- [ ] The CLI command delegates to the service.
- [ ] The learner can explain one happy path and one failure path aloud.
## 15. Ruthless mentor checkpoint
Do not accept a chatbot that merely sounds correct.
Show the chunks.
Show the citations.
Show the fallback.
Show the test where the generator is not called because evidence is missing.
If the answer cannot be traced to retrieved context, it is not done.
## 16. What not to do this week
Do not build future deployment work in this chapter.
Do not add a web UI.
Do not add multi-turn memory.
Do not hard-code provider keys.
Do not make unit tests call a real LLM.
Do not move semantic search into the QA service.
Do not put business logic in CLI or API entry points.
## 17. Bridge to next week
After Week 17, ResearchOps has a local evidence-grounded assistant.
The next chapter focuses on making the already-working system easier to run consistently in a production-style setup.
That next step is only useful if the Week 17 behavior is already clear, tested, and safe.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 16 Reflection](../../month-04-ai-engineering-api-workers/week-16-local-worker-job-system/reflection.md) · ➡️ [Notes →](notes.md)

**Week 17 — RAG Assistant:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
