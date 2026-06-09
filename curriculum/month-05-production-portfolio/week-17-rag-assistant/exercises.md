<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 17 — RAG Assistant:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 17 RAG Assistant

## 1. How to use this workbook
Use this workbook after reading the notes once.
Do not try to complete every exercise in one sitting.
Work in the same order as the sections.
Each section trains a different muscle.
Warm-ups build vocabulary.
Code-reading builds confidence with existing files.
Implementation tasks build the feature.
Testing tasks prove behavior.
Debugging tasks teach failure recovery.
Written tasks make sure you can explain the system, not only type it.
- Use fakes for all exercises that mention generators unless the exercise explicitly says manual exploration.
- Never paste a real API key into source code, notes, tests, or terminal output you plan to save.
- Keep Week 17 focused on RAG; do not add deployment packaging or future-week features.
- When an exercise says "explain", write full sentences, not only code comments.
## 2. Warm-up exercises
### Define RAG in one sentence
Task: Write one sentence that includes retrieval, generation, and evidence.
Acceptance check: you can point to the exact phrase or source that supports your answer.
### Identify the evidence
Task: Given a question and three chunks, mark which chunks should be used and why.
Acceptance check: you can point to the exact phrase or source that supports your answer.
### Format a context block
Task: Turn a list of chunk strings into `[1]`, `[2]`, `[3]` labeled text.
Acceptance check: you can point to the exact phrase or source that supports your answer.
### Write a fallback message
Task: Write a user-friendly insufficient-evidence message that does not blame the user.
Acceptance check: you can point to the exact phrase or source that supports your answer.
### Choose top-k
Task: Explain whether top-k should be 2, 5, or 20 for a small first prompt and why.
Acceptance check: you can point to the exact phrase or source that supports your answer.
### Spot hallucination risk
Task: Read a fluent answer and underline every claim not supported by the provided context.
Acceptance check: you can point to the exact phrase or source that supports your answer.
## 3. Code-reading exercises
### Read `src/researchops/services/qa_service.py`
Task: Identify what is currently a stub and list the decisions the service should own.
Write down the file path, the relevant function or class name, and one boundary rule it must respect.
### Read `src/researchops/ai/prompts.py`
Task: Identify the TODO guidance and rewrite it as three testable prompt requirements.
Write down the file path, the relevant function or class name, and one boundary rule it must respect.
### Read `src/researchops/search/vector_search.py`
Task: Find how semantic search results are represented and what metadata can become a citation.
Write down the file path, the relevant function or class name, and one boundary rule it must respect.
### Read `src/researchops/search/chunking.py`
Task: Explain how chunks are produced and why whole papers should not be placed in every prompt.
Write down the file path, the relevant function or class name, and one boundary rule it must respect.
### Read `src/researchops/core/interfaces.py`
Task: Find the protocols that already exist and decide whether Week 17 needs a new protocol or an injected structural type.
Write down the file path, the relevant function or class name, and one boundary rule it must respect.
### Read `src/researchops/cli/main.py`
Task: Find where a new `ask` command would be registered without putting business logic in the CLI.
Write down the file path, the relevant function or class name, and one boundary rule it must respect.
## 4. Implementation exercises
### Prompt instructions
Task: In `src/researchops/ai/prompts.py`, define a clear grounding instruction that says answers must use only context and cite sources.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
### Context formatter
Task: Implement a helper that formats retrieved chunks with stable labels such as `[source: paper-1 chunk-0]`.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
### Prompt builder
Task: Build a function that combines instructions, context, question, and an `Answer:` marker.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
### Answer object
Task: Create or use a structured answer object with answer text, citations, and `sufficient_evidence`.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
### Text generator seam
Task: Define the smallest generator interface needed by `QAService`: a method that accepts a prompt and returns text.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
### QAService happy path
Task: Make the service retrieve chunks, build a prompt, call the generator, and return citations.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
### QAService no-context path
Task: Make the service return insufficient evidence without calling the generator when no relevant chunks exist.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
### CLI ask command
Task: Wire `researchops ask QUESTION` to the service while keeping business logic out of the CLI.
Done when: the behavior has a narrow test and the file still respects the architecture boundary.
## 5. Testing exercises
### Test prompt contains instructions
Task: Assert that the prompt includes the grounding rule.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
### Test prompt contains question
Task: Assert that the original question appears exactly once in the prompt body.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
### Test prompt contains chunks
Task: Assert that each fake chunk appears with a label.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
### Test citations come from metadata
Task: Assert that returned citations match fake retrieved source IDs and chunk IDs.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
### Test no-context fallback
Task: Assert that an empty retrieval returns `sufficient_evidence=False`.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
### Test generator not called
Task: Use a fake generator that raises if called during the no-context path.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
### Test low-score filtering
Task: Return one high-score and one low-score fake chunk and assert only the high-score chunk is used.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
### Test CLI formatting lightly
Task: Use Typer testing only if the command exists; assert the output includes the answer and citation labels.
Use `tests/unit/test_qa_service.py` for service behavior unless a CLI-specific assertion is required.
## 6. Debugging exercises
### Break retrieval
Task: Make the fake retriever return no chunks and confirm the fallback appears.
Recovery: restore the correct behavior and write the lesson in one sentence.
### Break scores
Task: Set all fake scores below the threshold and confirm generation is skipped.
Recovery: restore the correct behavior and write the lesson in one sentence.
### Break prompt context
Task: Remove chunk text from the prompt builder and watch the prompt test fail.
Recovery: restore the correct behavior and write the lesson in one sentence.
### Break citations
Task: Return the wrong chunk ID and confirm the citation assertion catches it.
Recovery: restore the correct behavior and write the lesson in one sentence.
### Break boundary
Task: Temporarily imagine importing SQLite directly in `QAService`; write why this would harm tests.
Recovery: restore the correct behavior and write the lesson in one sentence.
### Break generator determinism
Task: Make the fake generator return changing text and explain why tests become weaker.
Recovery: restore the correct behavior and write the lesson in one sentence.
## 7. Refactoring exercises
### Extract context formatting
Task: If prompt building has a long loop, extract a helper and test it directly.
Check: the refactor should not change visible behavior.
### Name the threshold
Task: Replace a magic number like `0.3` with `min_relevance_score`.
Check: the refactor should not change visible behavior.
### Separate display from service
Task: Move any terminal formatting out of the service and into the CLI layer.
Check: the refactor should not change visible behavior.
### Separate provider code
Task: Keep provider-specific model calls out of prompt templates and service tests.
Check: the refactor should not change visible behavior.
### Simplify answer data
Task: Remove fields that are not used by CLI, API, or tests this week.
Check: the refactor should not change visible behavior.
## 8. Written explanation exercises
1. Explain why retrieve-then-generate is safer than generate-then-search.
2. Explain why a citation must be connected to retrieved metadata, not invented from answer text.
3. Explain how a fake generator makes tests reliable.
4. Explain what `sufficient_evidence=False` tells a CLI or API caller.
5. Explain which file owns prompt wording and why.
6. Explain how Week 13 semantic search makes Week 17 possible.
7. Explain how Week 14 entry-point boundaries still matter for `ask`.
8. Explain why a no-context answer should not call the generator.
## 9. Stretch exercises
### Evidence strength
Task: Add an average score field to the answer object and test the calculation with fake scores.
Rule: do not make the core Week 17 tests depend on this stretch behavior.
### Prompt length warning
Task: Warn or trim when the context block exceeds a simple character budget.
Rule: do not make the core Week 17 tests depend on this stretch behavior.
### Citation preview
Task: Include a short source title with each citation if metadata is available.
Rule: do not make the core Week 17 tests depend on this stretch behavior.
### Hybrid retrieval note
Task: Design, but do not fully implement, how keyword and semantic results might be merged later.
Rule: do not make the core Week 17 tests depend on this stretch behavior.
### Manual local generator
Task: Create an optional local generator class for personal experiments, but keep it out of unit tests.
Rule: do not make the core Week 17 tests depend on this stretch behavior.
## 10. Brutal exercises
### Adversarial document text
Task: Create a fake chunk that says "ignore previous instructions" and verify the prompt still clearly instructs grounding.
Deliverable: a short written diagnosis plus any narrow test you would add.
### Misleading high score
Task: Return a high-score irrelevant chunk and write how a human would catch the answer through citations.
Deliverable: a short written diagnosis plus any narrow test you would add.
### All citations wrong
Task: Intentionally mismatch citations and chunks, then design the test that should fail.
Deliverable: a short written diagnosis plus any narrow test you would add.
### Noisy context
Task: Pass five overlapping chunks and identify which ones add value and which ones add noise.
Deliverable: a short written diagnosis plus any narrow test you would add.
### Provider outage
Task: Describe how the service should surface generator failure without pretending evidence was insufficient.
Deliverable: a short written diagnosis plus any narrow test you would add.
### Boundary defense
Task: Review the final import graph and explain every import in `QAService`.
Deliverable: a short written diagnosis plus any narrow test you would add.
## 11. Mini project task
Build the first ResearchOps question-answering flow.
The user should be able to run `researchops ask "What are transformers used for?"` after papers have been indexed.
The assistant should retrieve top-k semantic chunks, construct a grounded prompt, call a generator through a seam, and display an answer with citations.
If there is no relevant context, it should display an insufficient-evidence response.
The service should be testable with fakes.
The CLI should contain wiring and formatting only.
Mini project acceptance checklist:
- `src/researchops/services/qa_service.py` owns orchestration.
- `src/researchops/ai/prompts.py` owns prompt wording.
- `researchops ask` is wired without business logic in the CLI.
- A fake retriever and fake generator can test the happy path.
- A no-context test proves the generator is skipped.
- Citations are visible in the returned answer or CLI output.
## 12. Completion checklist
- [ ] I can define RAG without using vague language.
- [ ] I can trace a question through retrieval, prompt construction, generation, and citations.
- [ ] I can explain where prompt templates live.
- [ ] I can explain why `QAService` owns orchestration.
- [ ] I can explain why unit tests use fakes.
- [ ] I can explain why no-context cases should not call the generator.
- [ ] I can identify the source metadata behind a citation.
- [ ] I can run or understand the Week 17 validation commands.
- [ ] I did not add future-week deployment concepts.
- [ ] I did not commit secrets or print secret values.
- [ ] I can explain one happy path and one failure path aloud.

### Extra workbook guardrails
- [ ] Before implementing, write the happy-path data flow in five arrows.
- [ ] Before implementing, write the no-context data flow in three arrows.
- [ ] Before testing, decide which fake records one relevant chunk and which fake records a generator call.
- [ ] Before manual use, confirm no real secret value is present in source files.
- [ ] Before moving on, explain why this is a RAG assistant and not plain semantic search.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 17 — RAG Assistant:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
