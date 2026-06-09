<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 17 — RAG Assistant:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 17 RAG Assistant

## 1. Chapter overview
Week 17 is the first week where ResearchOps is allowed to use a large language model.
The chapter title is **Answers grounded in evidence**.
The feature is the `researchops ask` command.
The command should accept a natural-language question.
The system should retrieve relevant chunks from the existing semantic search index.
The system should build a prompt that contains only those chunks as evidence.
The system should send that prompt to a text generator.
The system should return an answer with citations.
The answer should be honest when the indexed documents do not contain enough evidence.
This is retrieval-augmented generation, usually shortened to RAG.
RAG is not a model by itself.
RAG is a pipeline that combines search and generation.
Search finds evidence.
Generation turns evidence into readable language.
The important word is **evidence**.
ResearchOps is a research-paper platform, so every answer must be traceable back to papers and chunks.
A fluent answer without a source is not enough.
A source without an answer is not enough.
This week teaches how to combine both without breaking the architecture you have built since Week 1.
- The user-facing milestone is `researchops ask "What are transformers used for?"`.
- The service milestone is `QAService` coordinating retrieval, prompt construction, generation, and citations.
- The prompt milestone is `src/researchops/ai/prompts.py` holding reusable prompt templates.
- The testing milestone is `tests/unit/test_qa_service.py` proving the pipeline with fakes.
- The safety milestone is an insufficient-evidence path that does not call the generator.
Read this chapter slowly.
Do not start by adding a provider SDK.
Do not start by chasing model quality.
Start by making the data flow visible.
A beginner-friendly RAG system is a boring, explicit pipeline.
It says what it knows.
It says where that knowledge came from.
It says when it does not know.
## 2. What you already know from previous weeks
ResearchOps has grown in layers.
Week 1 gave you a project scaffold and a CLI entry point.
Week 2 made file handling and errors more deliberate.
Week 3 strengthened domain modeling with Python objects.
Week 4 made the CLI installable and easier to run.
Week 5 introduced SQLite persistence.
Week 6 added a service layer so business workflows did not live in the CLI.
Week 7 added keyword search and ranking over stored papers.
Week 8 taught that CPU-heavy parsing belongs in a process pool.
Week 9 introduced protocols so services can depend on contracts instead of concrete classes.
Week 10 improved test discipline with fakes and clearer boundaries.
Week 11 and Week 12 brought ML classification and experiment tracking.
Week 13 introduced embeddings, chunking, and semantic search.
Week 14 exposed features through FastAPI without moving business logic into routes.
Week 15 added async fetching for I/O-bound network work.
Week 16 added a local job system for work that should be queued, retried, and observed.
This week uses those ideas instead of replacing them.
- From Week 13, remember that chunks are smaller text fragments created from papers.
- From Week 13, remember that embeddings are numeric vectors representing meaning.
- From Week 13, remember that cosine similarity ranks chunks by closeness to a query.
- From Week 14, remember that API routes are entry points, not owners of business logic.
- From Week 16, remember that long or retryable work should have clear state and failure handling.
The most important continuity point is this: RAG does not replace semantic search.
RAG consumes semantic search results.
If Week 13 retrieval is weak, Week 17 answers will be weak.
If Week 13 chunk metadata is missing, Week 17 citations will be weak.
If Week 14 boundaries were ignored, Week 17 wiring will become confusing.
The assistant is impressive only when the boring pieces are trustworthy.
## 3. What problem this week solves
Before Week 17, ResearchOps can store papers and search them.
Search results are useful, but they make the learner or user read many chunks manually.
A user may ask a research question such as: "What are transformers used for?"
A search command can return matching papers or chunks.
But it does not synthesize the answer.
It does not say which retrieved evidence supports which sentence.
It does not refuse when evidence is missing.
The Week 17 problem is to build a safe question-answering layer over the existing library.
- The input is a user question.
- The first transformation is retrieval of top-k chunks from semantic search.
- The second transformation is prompt construction from the question and chunks.
- The third transformation is text generation from the prompt.
- The proof is an answer object that includes citations and an evidence flag.
The unsafe solution would be to send the user question directly to an LLM.
That would be easy to implement but wrong for ResearchOps.
The model might answer from its training data.
The model might invent a paper that was never ingested.
The model might summarize a concept correctly in general but incorrectly for the user's library.
ResearchOps is not trying to build a generic chatbot.
ResearchOps is trying to answer from the papers it has processed.
That is why retrieval must come first.
## 4. Beginner mental model
Use the mental model of a careful research assistant sitting at a desk.
The user asks a question.
The assistant does not answer from memory.
The assistant first searches the paper library.
The assistant pulls out a few relevant highlighted paragraphs.
The assistant writes a short answer using only those highlighted paragraphs.
The assistant adds a note beside each claim saying which paragraph supports it.
If the library has no relevant paragraphs, the assistant says there is not enough evidence.
That desk model is RAG.
- Question: the user request, such as "What is attention?".
- Retriever: the part that finds candidate chunks.
- Context: the selected chunks placed into a prompt.
- Prompt: instructions plus context plus question.
- Generator: the component that produces answer text.
- Citation: a reference back to the source paper and chunk.
- Fallback: the safe response when context is missing or weak.
A beginner mistake is to think the LLM is the center of the system.
In ResearchOps, the LLM is only one component.
The center of the system is the evidence flow.
Evidence enters through retrieval.
Evidence is formatted in the prompt.
Evidence is reflected in the answer.
Evidence is exposed through citations.
When debugging, always ask where the evidence first went missing.
## 5. Core vocabulary
| Term | Beginner meaning | ResearchOps reason |
|---|---|---|
| RAG | Retrieval-augmented generation; a pipeline that retrieves evidence before generating an answer. | It names a responsibility in Week 17. |
| Retrieval | Finding relevant chunks from the indexed paper library. | It names a responsibility in Week 17. |
| Generation | Producing readable answer text from a prompt. | It names a responsibility in Week 17. |
| Top-k | The number of highest-ranked chunks requested from search. | It names a responsibility in Week 17. |
| Chunk | A smaller piece of a paper created so search and prompts can handle long documents. | It names a responsibility in Week 17. |
| Context | The retrieved chunk text supplied to the generator. | It names a responsibility in Week 17. |
| Prompt template | A reusable text structure with slots for context and question. | It names a responsibility in Week 17. |
| Grounding | Restricting the answer to claims supported by context. | It names a responsibility in Week 17. |
| Hallucination | A fluent claim that is false or not supported by the provided evidence. | It names a responsibility in Week 17. |
| Citation | A source reference that lets the user inspect the chunk behind an answer. | It names a responsibility in Week 17. |
| Insufficient evidence | The safe answer when retrieval finds no useful support. | It names a responsibility in Week 17. |
| Text generator | An object with a method that accepts a prompt and returns answer text. | It names a responsibility in Week 17. |
| Fake generator | A deterministic generator used in tests instead of a real LLM. | It names a responsibility in Week 17. |
| QAService | The service that owns the retrieve → prompt → generate → cite workflow. | It names a responsibility in Week 17. |
| Prompt injection | User or document text trying to override the system instructions. | It names a responsibility in Week 17. |
Do not memorize these as isolated definitions.
Attach each word to a place in the pipeline.
If you can point to the line where chunks become context, the word context becomes concrete.
If you can point to the line where citations are created, the word citation becomes concrete.
## 6. Concept explanations from first principles
### Retrieve-then-generate
Generation without retrieval is like answering an exam without reading the assigned passage.
The answer may sound polished but may not match the source material.
Retrieval changes the task from "answer from memory" to "answer from this evidence".
The retrieved chunks should be selected before prompt construction.
The generated answer should never be asked to discover sources after the fact.
A beginner check: explain the input, output, and failure path for this concept before writing code.
A ResearchOps check: identify which existing week provided the dependency this concept uses.

### Chunked retrieval
Research papers are too long to place entirely into every prompt.
Chunks make long papers searchable in smaller meaningful units.
A good chunk is large enough to contain a complete idea.
A good chunk is small enough to fit with other chunks in the prompt.
Week 13 already introduced chunking; Week 17 uses those chunks as evidence.
A beginner check: explain the input, output, and failure path for this concept before writing code.
A ResearchOps check: identify which existing week provided the dependency this concept uses.

### Prompt engineering
A prompt is not just the user question.
A prompt includes instructions, evidence, the question, and answer rules.
Good prompt structure makes behavior easier to test.
The template should tell the model to use only the provided context.
The template should tell the model how to cite sources.
A beginner check: explain the input, output, and failure path for this concept before writing code.
A ResearchOps check: identify which existing week provided the dependency this concept uses.

### Grounding
Grounding means every important claim can be tied to supplied evidence.
Grounding does not mean the model becomes perfect.
Grounding reduces the space of possible answers.
The user can verify grounded answers by opening cited chunks.
Ungrounded answers should be treated as defects in a research assistant.
A beginner check: explain the input, output, and failure path for this concept before writing code.
A ResearchOps check: identify which existing week provided the dependency this concept uses.

### Hallucination handling
A hallucination is not just a silly answer.
It is a confident answer that appears trustworthy but lacks support.
The safest first defense is refusing unsupported questions.
The second defense is requiring citations.
The third defense is testing the no-context path separately.
A beginner check: explain the input, output, and failure path for this concept before writing code.
A ResearchOps check: identify which existing week provided the dependency this concept uses.

### QAService orchestration
The service owns the workflow decision order.
It should ask the retriever for chunks.
It should decide whether evidence is sufficient.
It should build the prompt only when evidence exists.
It should call the generator only after prompt construction.
It should return a structured answer instead of printing directly.
A beginner check: explain the input, output, and failure path for this concept before writing code.
A ResearchOps check: identify which existing week provided the dependency this concept uses.

## 7. ResearchOps-specific application
The Week 17 feature should fit the existing architecture.
The CLI command is an entry point.
The service owns the use case.
The semantic search implementation remains in `src/researchops/search/`.
The prompt templates live in `src/researchops/ai/prompts.py`.
The service should not import a concrete SQLite repository.
The service should not import FastAPI.
The service should not print directly.
The service should return values that callers can display.
Recommended project flow:
- `researchops ask "What are transformers used for?"` receives the question in the CLI.
- The CLI wires a `QAService` with a semantic search dependency and a generator dependency.
- `QAService` asks the retriever for top-k relevant chunks.
- `QAService` filters out chunks below the minimum relevance threshold.
- `QAService` calls `build_rag_prompt` or an equivalent prompt builder from `ai/prompts.py`.
- `QAService` passes the prompt to a `TextGenerator` implementation.
- `QAService` returns an answer with citations and a sufficient-evidence flag.
- The CLI formats that answer for the terminal.
The prompt template location matters.
If prompt strings are scattered through CLI commands, tests become fragile.
If prompt strings live in the service, they can be tested, but they mix orchestration and wording.
The project spec names `src/researchops/ai/prompts.py` as the home for RAG prompt templates.
That file is infrastructure-like support for AI behavior.
It should stay small, explicit, and easy to test.
## 8. Code examples with line-by-line explanation
The code below is educational pseudocode shaped like the Week 17 implementation.
It avoids provider-specific SDK details because the first goal is to understand the pipeline.
### Example 1: a prompt template function
```python
RAG_SYSTEM_INSTRUCTIONS = """
You are a ResearchOps assistant.
Answer only from the provided context.
If the context does not contain enough evidence, say you do not have enough evidence.
Cite sources using the labels shown in the context.
""".strip()
```
- Line 1 names the instruction block so other code can import it.
- Line 2 tells the model which role it should play.
- Line 3 is the grounding rule: answer only from context.
- Line 4 defines the no-evidence behavior.
- Line 5 defines the citation behavior.
- Line 6 removes leading and trailing blank lines from the triple-quoted string.
```python
def format_context(chunks: list[str]) -> str:
    numbered_chunks: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        numbered_chunks.append(f"[{index}] {chunk}")
    return "

".join(numbered_chunks)
```
- Line 1 defines a function that receives chunk text and returns one context string.
- Line 2 creates an empty list that will hold formatted chunks.
- Line 3 loops through chunks and starts numbering at 1 because humans read `[1]` more naturally than `[0]`.
- Line 4 creates a label such as `[1]` and stores the chunk after it.
- Line 5 joins chunks with blank lines so the prompt is readable.
```python
def build_rag_prompt(question: str, chunks: list[str]) -> str:
    context_block = format_context(chunks)
    return (
        f"{RAG_SYSTEM_INSTRUCTIONS}

"
        f"Context:
{context_block}

"
        f"Question:
{question}

"
        "Answer:"
    )
```
- Line 1 names the main prompt-building function and gives it typed parameters.
- Line 2 converts the list of chunks into one numbered context block.
- Line 3 starts a parenthesized string expression so the prompt can be built across several lines.
- Line 4 puts the grounding instructions first.
- Line 5 inserts the retrieved evidence under a clear `Context` heading.
- Line 6 inserts the original user question without changing its meaning.
- Line 7 gives the model a clear place to start its response.
- Line 8 closes the string expression and returns the completed prompt.
### Example 2: the answer object
```python
from dataclasses import dataclass, field


@dataclass
class QAAnswer:
    answer: str
    citations: list[str] = field(default_factory=list)
    sufficient_evidence: bool = True
```
- Line 1 imports the tools for creating a small data object.
- Line 4 marks the class as a dataclass so Python creates an initializer and representation.
- Line 5 names the object that callers receive from the service.
- Line 6 stores the generated or fallback answer text.
- Line 7 stores citations and uses `default_factory` so each answer gets its own list.
- Line 8 stores whether retrieval found enough evidence to answer.
### Example 3: a generator protocol
```python
from typing import Protocol


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```
- Line 1 imports `Protocol`, which describes behavior without requiring inheritance.
- Line 4 defines the shape that any generator must satisfy.
- Line 5 says a generator receives a prompt string and returns a string.
- Line 6 uses `...` because the protocol declares a method but does not implement it.
### Example 4: the no-context guard
```python
INSUFFICIENT_EVIDENCE = (
    "I do not have enough evidence in the indexed documents "
    "to answer this question."
)


def answer(question: str) -> QAAnswer:
    hits = retriever.search(question, limit=5)
    relevant_hits = [hit for hit in hits if hit.score >= 0.30]
    if not relevant_hits:
        return QAAnswer(answer=INSUFFICIENT_EVIDENCE, sufficient_evidence=False)
```
- Lines 1 through 4 define one standard fallback message.
- Line 7 begins an educational `answer` function.
- Line 8 retrieves candidate chunks before generation.
- Line 9 filters weak results using a minimum relevance score.
- Line 10 checks the failure path before building a prompt.
- Line 11 returns a structured fallback and marks evidence as insufficient.
Notice the order.
The generator is not called before the `if not relevant_hits` check.
That order is a safety rule.
If there is no context, generation would invite the model to guess.
## 9. Common beginner mistakes
### Mistake: Calling the LLM before retrieval
Why it hurts: The answer may come from model memory instead of the indexed papers.
Better move: Retrieve chunks first and pass them into the prompt.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Treating citations as decoration
Why it hurts: Users cannot verify unsupported claims.
Better move: Create citations from actual retrieved chunk metadata.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Putting prompt text inside the CLI
Why it hurts: Prompt wording becomes hard to test and reuse.
Better move: Keep prompt templates in `src/researchops/ai/prompts.py`.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Using a real model in unit tests
Why it hurts: Tests become slow, flaky, expensive, and network-dependent.
Better move: Use a fake generator with deterministic output.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Ignoring the no-context case
Why it hurts: The assistant will answer questions that the library cannot support.
Better move: Return an insufficient-evidence answer without calling the generator.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Retrieving whole papers instead of chunks
Why it hurts: The prompt becomes too long and noisy.
Better move: Use Week 13 chunking and semantic search outputs.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Hiding the relevance threshold
Why it hurts: Nobody can explain why a chunk was accepted or rejected.
Better move: Name the threshold and test both sides of it.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Letting services import concrete infrastructure
Why it hurts: The clean architecture boundary breaks.
Better move: Depend on protocols or injected objects instead.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Printing inside the service
Why it hurts: The API cannot reuse the behavior cleanly.
Better move: Return an answer object and let entry points format it.
Beginner check: write one test or manual check that would reveal this mistake.

### Mistake: Hard-coding API keys
Why it hurts: Secrets can leak into Git history.
Better move: Read secrets from environment variables and never print them.
Beginner check: write one test or manual check that would reveal this mistake.

## 10. Debugging guidance
Debug RAG as a pipeline, not as a mysterious model failure.
When an answer is bad, do not immediately blame the generator.
The bad answer may have started with bad retrieval.
The prompt may have omitted the important chunk.
The citations may have been created from the wrong metadata.
The no-context guard may have accepted weak evidence.
Use a staged checklist.
- Print or inspect the exact user question after CLI parsing.
- Inspect the retrieved chunk count before filtering.
- Inspect the score for each candidate chunk.
- Inspect which chunks survive the minimum-score filter.
- Inspect the final context block before generation.
- Inspect the final prompt length and headings.
- Inspect whether the generator was called in no-context cases.
- Inspect the returned citations and compare them to retrieved metadata.
- Inspect the `sufficient_evidence` flag.
- Inspect the terminal formatting only after the service result is correct.
Use fakes when debugging service logic.
A fake retriever can return exactly two chunks with known scores.
A fake generator can return a fixed answer.
That removes randomness.
Once the service works with fakes, a real model failure is easier to classify.
If a real model ignores citations, the prompt wording is the likely place to inspect.
If a real model answers from outside context, strengthen the grounding instruction and reduce distracting context.
If retrieval returns irrelevant chunks, revisit Week 13 chunking, embedding, and similarity behavior.
## 11. Design tradeoffs
| Choice | Benefit | Cost |
|---|---|---|
| Small top-k | Uses fewer tokens and keeps the prompt focused. | May miss evidence spread across several chunks. |
| Large top-k | Gives the generator more evidence. | May add noise and exceed the context window. |
| Strict score threshold | Reduces unsupported answers. | May refuse questions that have partial evidence. |
| Loose score threshold | Answers more questions. | Increases hallucination risk. |
| Fake generator in tests | Fast and deterministic. | Does not measure real model quality. |
| Real generator in manual checks | Shows actual user experience. | Costs time, money, or local compute. |
| Prompt templates in one file | Easy to audit and test. | Can become crowded if not kept organized. |
| Structured answer object | Reusable by CLI and API. | Requires slightly more code than returning a string. |
The beginner-friendly default is conservative.
Prefer fewer, better chunks.
Prefer refusing when evidence is weak.
Prefer deterministic tests.
Prefer explicit data objects.
You can improve ranking and answer quality later, but a safe first RAG pipeline must be understandable now.
## 12. Testing implications
Week 17 tests should prove the workflow without depending on a real LLM.
The syllabus names `tests/unit/test_qa_service.py` as the main test file.
That test should use fakes.
The fake search engine controls retrieved chunks and scores.
The fake generator controls generated text.
The service test then proves orchestration.
- Test that a question is passed to retrieval.
- Test that retrieved chunk text appears in the built prompt.
- Test that citations are derived from retrieved chunk metadata.
- Test that low-score or empty retrieval returns insufficient evidence.
- Test that the generator is not called when evidence is insufficient.
- Test that the answer object marks `sufficient_evidence=True` on the happy path.
A useful fake generator can record the prompt it received.
That lets the test assert that instructions, context, and question were all present.
A useful fake retriever can return one relevant chunk and one weak chunk.
That lets the test assert that filtering works.
Avoid snapshot-testing a huge prompt unless the prompt is intentionally stable.
Instead, assert important substrings: the grounding instruction, chunk label, source label, and question.
Example test intention:
```python
def test_qa_service_builds_grounded_prompt() -> None:
    retriever = FakeRetriever([...])
    generator = RecordingFakeGenerator("answer [source: paper-1 chunk-0]")
    service = QAService(retriever=retriever, generator=generator)
    result = service.answer("What is attention?")
    assert result.sufficient_evidence is True
    assert "Answer only from the provided context" in generator.last_prompt
    assert "What is attention?" in generator.last_prompt
    assert result.citations == ["paper-1 chunk-0"]
```
Line-by-line purpose:
- Line 1 names the behavior being tested.
- Line 2 creates controlled retrieval results.
- Line 3 creates a generator that records the prompt.
- Line 4 wires the service with fakes.
- Line 5 exercises the public service method.
- Line 6 checks the happy-path evidence flag.
- Line 7 checks that the prompt includes the grounding rule.
- Line 8 checks that the user question reached the prompt.
- Line 9 checks citations come from evidence metadata.
## 13. Architecture implications
RAG touches several layers, so architecture discipline matters more this week than it may appear.
The CLI should parse the question and display the result.
The CLI should not decide how to rank chunks.
The CLI should not assemble prompt text.
The service should own the workflow.
The service should depend on interfaces or injected collaborators.
The search infrastructure should own embedding and vector similarity.
The AI prompt module should own reusable prompt wording.
The generator implementation should own provider-specific calls.
Safe dependency direction for Week 17:
```text
cli/main.py
  -> services/qa_service.py
      -> core-facing protocols and simple data objects
      -> ai/prompts.py for prompt templates
  <- search/vector_search.py is injected from the outside
  <- generator implementation is injected from the outside
```
Do not move semantic search into the QA service.
Do not move QA workflow into the search module.
Do not make `ai/prompts.py` call the LLM.
Do not make `core/` import AI or search code.
The boundary is simple: search finds evidence, prompts format evidence, generation writes text, service coordinates the use case.
## 14. How this connects to AI engineering / ML research
Modern AI engineering is mostly system engineering around models.
A model call alone is rarely enough for a trustworthy product.
Research teams need traceability.
They need reproducibility.
They need to know which documents support an answer.
They need to distinguish "the model said so" from "the indexed evidence supports this".
Week 17 introduces those habits.
- RAG connects private or local data to a general language model.
- Citations make research answers auditable.
- No-context fallbacks reduce the risk of confident nonsense.
- Fakes make AI system tests deterministic even when real models are not.
- Prompt templates make model behavior reviewable in code review.
- Evidence thresholds make answer quality a product decision, not a hidden accident.
In ML research, the exact same model can appear better or worse depending on retrieval quality.
If the retrieved chunks are irrelevant, even a strong model may produce a bad answer.
If the retrieved chunks are concise and on-topic, a modest model can produce a useful answer.
This is why Week 17 should make you think like a systems engineer.
Model quality matters, but data flow quality matters first.
## 15. Mini quizzes
1. What does RAG stand for?
2. Why does ResearchOps retrieve chunks before calling the generator?
3. What is the difference between a chunk and a citation?
4. Why should a prompt template live in `src/researchops/ai/prompts.py`?
5. What should the assistant do when no chunks pass the relevance threshold?
6. Why should unit tests use a fake generator?
7. What is one sign that the retrieval step failed?
8. What is one sign that the prompt construction step failed?
9. What is one sign that the generator ignored grounding instructions?
10. Which layer should own the `researchops ask` workflow?
11. Why is returning a structured answer better than returning a raw string?
12. What previous week provides the semantic search capability used here?
13. What previous week introduced the API boundary that should not be violated?
14. Why are citations useful for debugging?
15. Why is an insufficient-evidence answer a feature rather than a failure?
## 16. Explain-it-aloud prompts
- Explain RAG to someone who has only used keyword search.
- Explain why a generic chatbot answer is not enough for ResearchOps.
- Explain the path from `researchops ask` to retrieved chunks.
- Explain the difference between context and prompt.
- Explain why prompt templates are code, not casual text.
- Explain how citations help a user trust or reject an answer.
- Explain why tests should not call a real model by default.
- Explain the no-context path without using the word "magic".
- Explain where you would look if the answer is fluent but unsupported.
- Explain where you would look if citations point to irrelevant chunks.
- Explain why the service should not print terminal output.
- Explain how Week 13 made Week 17 possible.
## 17. What to memorize
- RAG means retrieval-augmented generation.
- The order is retrieve, build prompt, generate, cite, return.
- The Week 17 command is `researchops ask QUESTION`.
- The main service file is `src/researchops/services/qa_service.py`.
- The prompt template file is `src/researchops/ai/prompts.py`.
- The main test file is `tests/unit/test_qa_service.py`.
- The safe fallback is an insufficient-evidence answer.
- Unit tests use fakes, not real model calls.
- Citations must come from retrieved source metadata.
- Services own workflows; entry points format inputs and outputs.
## 18. What to understand deeply
Understand that RAG quality is bounded by retrieval quality.
A generator cannot cite evidence that was not retrieved.
A prompt cannot make irrelevant chunks relevant.
A citation cannot prove a claim if it points to the wrong source.
A pretty answer is not the same as a grounded answer.
This distinction is the heart of Week 17.
- Understand why evidence is checked before generation.
- Understand why prompt construction is testable without a model.
- Understand why fakes are not a shortcut but a design tool.
- Understand why citation metadata must travel with chunk text.
- Understand why no-context behavior protects users.
- Understand why provider-specific code should not dominate the service design.
- Understand why the same service result should be usable by CLI and API entry points.
## 19. What not to worry about yet
- Do not worry about perfect answer quality on the first pass.
- Do not worry about multi-turn chat history.
- Do not worry about a web UI.
- Do not worry about deployment packaging in this chapter.
- Do not worry about advanced reranking.
- Do not worry about streaming tokens.
- Do not worry about agent tools or autonomous planning.
- Do not worry about optimizing token cost before the safe pipeline works.
- Do not worry about supporting every LLM provider.
- Do not worry about replacing Week 13 retrieval; reuse it.
The goal is a first grounded assistant.
A grounded assistant that refuses unsupported questions is better than a flashy assistant that invents sources.
Keep the surface area small.
Make the behavior explainable.
Then move forward.
## 20. Bridge to next week
Week 17 gives ResearchOps its first LLM-powered feature.
Next week focuses on making the working system easier to run consistently in a production-style environment.
That next step only makes sense if the local assistant behavior is already clear.
Before leaving Week 17, you should be able to run the validation command, read the service test, and explain why the assistant answers or refuses.
- If retrieval feels weak, revisit Week 13 before moving on.
- If API boundaries feel weak, revisit Week 14 before moving on.
- If job and operational thinking feels weak, revisit Week 16 before moving on.
- If prompt behavior feels mysterious, reread the line-by-line examples in this chapter.
- If citations feel optional, reread the grounding and hallucination sections.
The bridge sentence is simple: Week 17 makes ResearchOps answer questions with evidence; the next chapter makes the completed local system easier to operate repeatably.
Do not jump ahead while the assistant is still guessing.
Make it grounded first.
### Closing deepening drills
- Drill 1.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 1.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 1.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 1.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 1.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 1.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 1.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 1.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 2.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 3.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 4.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 5.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 6.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 7.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.retrieval evidence trace: Take one question and write down the exact chunks that should support the answer.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.prompt audit: Read the final prompt aloud and identify instruction, context, question, and answer marker.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.citation audit: For each citation, locate the source paper and chunk metadata that produced it.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.fallback audit: Use a question unrelated to the library and confirm the generator is not called.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.threshold audit: Lower and raise the relevance threshold in a controlled test and predict the result.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.fake isolation: Replace the real generator with a fake and confirm service logic still works.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.boundary audit: Open each changed file and name the single responsibility it owns.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.
- Drill 8.hallucination audit: Compare a direct LLM answer with a grounded RAG answer and identify unsupported claims.
  Write the observed input, output, and evidence source in one sentence.
  If you cannot name the evidence source, the assistant is not grounded enough yet.

### Final self-check before validation
- Can you name the exact retriever object used by the service?
- Can you name the exact generator object used by the service?
- Can you show the prompt before it is sent to the generator in a test?
- Can you show that citations come from source metadata rather than model text?
- Can you show that weak evidence prevents generation?
- Can you explain why a refusal can be the correct answer?
- Can you explain how a user would verify the answer manually?
- Can you explain what would break if the service imported concrete storage?
- Can you explain why real model quality is a separate concern from orchestration correctness?
- Can you explain what the learner should revisit if retrieved chunks are irrelevant?
- Can you explain what the learner should revisit if CLI wiring contains business logic?
- Can you explain what the learner should revisit if the no-context path still calls the generator?
- Can you explain why this chapter is the first safe place to introduce an LLM?
- Can you explain why the answer must cite chunks, not just papers?
- Can you explain why prompt injection from document text is a reason to keep instructions explicit?
- Can you explain why tests should inspect the prompt structure without asserting every word?
- Can you explain why the assistant is part of ResearchOps rather than a separate toy chatbot?
- Can you explain how this feature improves the portfolio story of the project?
- Can you explain which tradeoff you would tune first if answers are too often refused?
- Can you explain which tradeoff you would tune first if answers are too often unsupported?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 17 — RAG Assistant:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
