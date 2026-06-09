<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 15 Async I/O and Network Fetching

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 15: Async I/O Network Fetching

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Waiting without blocking**.
The practical milestone is: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
The expected capability is: Can write async functions, apply timeouts and retries, avoid blocking the event loop, and test async code with pytest-asyncio. ---
This chapter is one step in the ResearchOps system, not a random lesson.
The visible feature matters because it proves the idea works.
The hidden skill matters because it lets you build the next chapter without confusion.
A complete pass through this chapter means you can read the code, run it, test it, break it, and explain it aloud.

Use this study order:
- Read the story first without typing.
- Trace the smallest code example.
- Find the project file that owns the behavior.
- Run the validation command.
- Explain one happy path and one failure path.

## What you already know from previous weeks

- Week 11 taught Classical ML — Topic Classification; keep its responsibility in mind, but do not rebuild it here.
- Week 12 taught Experiment Tracking; keep its responsibility in mind, but do not rebuild it here.
- Week 13 taught Embeddings and Semantic Search; keep its responsibility in mind, but do not rebuild it here.
- Week 14 taught FastAPI Layer; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 15 solves the project problem behind **Async I/O Network Fetching**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept ``asyncio` event loop: one thread, many concurrent waits` helps solve part of this gap.
- The concept ``async def` and `await`: what they actually do` helps solve part of this gap.
- The concept ``httpx.AsyncClient` for async HTTP requests` helps solve part of this gap.
- The concept `Timeouts and retry logic: exponential backoff` helps solve part of this gap.
- The concept `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` helps solve part of this gap.
- The concept ``pytest-asyncio` for testing async code` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Async I/O Network Fetching**?
- Ask: what is the owner for **Async I/O Network Fetching**?
- Ask: what is the transformation for **Async I/O Network Fetching**?
- Ask: what is the proof for **Async I/O Network Fetching**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| asyncio` event loop | `asyncio` event loop: one thread, many concurrent waits | This term names one job in the Week 15 milestone. |
| async def` and `await | `async def` and `await`: what they actually do | This term names one job in the Week 15 milestone. |
| httpx.AsyncClient` for async HTTP requests | `httpx.AsyncClient` for async HTTP requests | This term names one job in the Week 15 milestone. |
| Timeouts and retry logic | Timeouts and retry logic: exponential backoff | This term names one job in the Week 15 milestone. |
| Never block the event loop | Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor | This term names one job in the Week 15 milestone. |
| pytest-asyncio` for testing async code | `pytest-asyncio` for testing async code | This term names one job in the Week 15 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: `asyncio` event loop: one thread, many concurrent waits
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 15, it supports the milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: `async def` and `await`: what they actually do
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 15, it supports the milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: `httpx.AsyncClient` for async HTTP requests
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 15, it supports the milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Timeouts and retry logic: exponential backoff
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 15, it supports the milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 15, it supports the milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: `pytest-asyncio` for testing async code
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 15, it supports the milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/services/fetch_service.py` — async fetching with retry
- `src/researchops/cli/commands/ingest.py` — `fetch-url`, `fetch-arxiv` commands
Study those files in this order:
1. Find the user-facing entry point.
2. Find the service or core concept that owns the meaning.
3. Find the infrastructure only when outside resources are needed.
4. Find the tests that prove the behavior.
5. Find the validation command that a learner runs manually.
The goal is to know why each file exists.
If two files seem to own the same decision, stop and clarify the boundary.

## Code examples with line-by-line explanation

```python
async def fetch_one(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url, timeout=10)
    response.raise_for_status()
    return response.text
```

Line-by-line explanation:
- Line 1: `async def fetch_one(client: httpx.AsyncClient, url: str) -> str:` — This names a reusable action and shows what information it receives.
- Line 2: `response = await client.get(url, timeout=10)` — This stores a clear intermediate value for the next step.
- Line 3: `response.raise_for_status()` — This performs one small visible step in the workflow.
- Line 4: `return response.text` — This produces the result or performs the declared setup step.

How to use this example:
- Name the input.
- Name the output.
- Predict the result before running anything.
- Connect the shape to the real ResearchOps file.
- Write one sentence about why each line belongs.

## Common beginner mistakes

- **Mistake:** Pasting code before knowing the owner of the behavior.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Changing many files at once.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Skipping the failure path.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Reading only the happy path test.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Ignoring the validation command.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Using vague names.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Putting business rules in the user interface layer.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Treating logs, errors, and tests as decoration.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Optimizing before correctness is visible.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Building future-week features early.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.

## Debugging guidance

- Copy the exact failing command.
- Read the first useful error line.
- Read the final error line.
- Classify the failure as import, input, state, file, database, network, model, or expectation.
- Reproduce it with the smallest command.
- Inspect the value closest to the failure.
- Fix the cause, not only the symptom.
- Run the narrowest test.
- Run the chapter validation command.
- Write down what the error was teaching.
Debugging questions:
- What did I expect?
- What happened?
- Which value first became wrong?
- Which layer created that value?
- Which test should catch this next time?

## Design tradeoffs

- **Simple first version:** Easy to understand, but not the final production shape.
- **Clear layers:** More files, but less confusion as features grow.
- **Explicit errors:** More code, but failures become teachable.
- **Small unit tests:** Fast feedback, but less end-to-end confidence.
- **Integration tests:** Real wiring, but slower and more setup.
- **Configuration:** Flexible behavior, but defaults must be clear.
The right question is not "What is the fanciest design?"
The right question is "What design teaches the responsibility clearly and can grow next week?"

## Testing implications

Tests for this chapter:
- `tests/unit/test_fetch_service.py` — mocked HTTP with monkeypatch
Validation commands:
```bash
researchops fetch-arxiv "attention is all you need"
pytest tests/unit/test_fetch_service.py -v
```
- Arrange the data.
- Act on the system.
- Assert the visible promise.
- Check one failure path.
- Keep unit tests fast.
- Use integration tests only when real wiring matters.

## Architecture implications

ResearchOps stays understandable when dependencies point inward.
```text
CLI / API / Worker -> Services -> Core
Infrastructure implements core-facing contracts and is wired at the outside.
```
- Does the UI layer avoid business logic?
- Does the service layer own workflow decisions?
- Does core avoid infrastructure imports?
- Does infrastructure do outside-world work?
- Do tests use fakes when possible?
Architecture is not ceremony.
Architecture is named responsibility.

## How this connects to AI engineering / ML research

AI engineering needs more than models.
It needs reliable data flow, clear interfaces, repeatable experiments, visible failures, and honest evaluation.
Week 15 contributes by making **async i/o network fetching** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 15 solve?
- What is the main input?
- What is the main output?
- Which file owns the main responsibility?
- Which layer should not contain business logic?
- What is one happy path?
- What is one failure path?
- What command proves the chapter works?
- What should you not build early?
- How does this prepare the next week?

## Explain-it-aloud prompts

- Explain Async I/O Network Fetching in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Async I/O Network Fetching.
- The milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- The main project files.
- The validation command.
- The boundary rule for the layer you are touching.
- The habit of testing before moving forward.

## What to understand deeply

- Why this feature belongs now.
- How data moves through the chapter.
- Which file owns which decision.
- How the failure path is handled.
- Why the tests prove behavior.
- How this week makes future work safer.

## What not to worry about yet

- Perfect scale.
- Fancy abstractions.
- Future-week features.
- Every option in every library.
- Premature optimization.
- Comparing your speed to someone else.
Focus on the milestone.
A clear small milestone beats a confusing large one.

## Bridge to next week

Next week is Week 16: **Local Worker and Job System**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace ``asyncio` event loop: one thread, many concurrent waits` from user input to project result.
- Drill 2: Write one sentence defining ``asyncio` event loop: one thread, many concurrent waits` without copying the notes.
- Drill 3: Find the file where ``asyncio` event loop: one thread, many concurrent waits` appears or should appear.
- Drill 4: Name one wrong implementation of ``asyncio` event loop: one thread, many concurrent waits` and why it would hurt.
- Drill 5: Name one test that would protect ``asyncio` event loop: one thread, many concurrent waits`.
- Drill 6: Trace ``async def` and `await`: what they actually do` from user input to project result.
- Drill 7: Write one sentence defining ``async def` and `await`: what they actually do` without copying the notes.
- Drill 8: Find the file where ``async def` and `await`: what they actually do` appears or should appear.
- Drill 9: Name one wrong implementation of ``async def` and `await`: what they actually do` and why it would hurt.
- Drill 10: Name one test that would protect ``async def` and `await`: what they actually do`.
- Drill 11: Trace ``httpx.AsyncClient` for async HTTP requests` from user input to project result.
- Drill 12: Write one sentence defining ``httpx.AsyncClient` for async HTTP requests` without copying the notes.
- Drill 13: Find the file where ``httpx.AsyncClient` for async HTTP requests` appears or should appear.
- Drill 14: Name one wrong implementation of ``httpx.AsyncClient` for async HTTP requests` and why it would hurt.
- Drill 15: Name one test that would protect ``httpx.AsyncClient` for async HTTP requests`.
- Drill 16: Trace `Timeouts and retry logic: exponential backoff` from user input to project result.
- Drill 17: Write one sentence defining `Timeouts and retry logic: exponential backoff` without copying the notes.
- Drill 18: Find the file where `Timeouts and retry logic: exponential backoff` appears or should appear.
- Drill 19: Name one wrong implementation of `Timeouts and retry logic: exponential backoff` and why it would hurt.
- Drill 20: Name one test that would protect `Timeouts and retry logic: exponential backoff`.
- Drill 21: Trace `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` from user input to project result.
- Drill 22: Write one sentence defining `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` without copying the notes.
- Drill 23: Find the file where `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` appears or should appear.
- Drill 24: Name one wrong implementation of `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` and why it would hurt.
- Drill 25: Name one test that would protect `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor`.
- Drill 26: Trace ``pytest-asyncio` for testing async code` from user input to project result.
- Drill 27: Write one sentence defining ``pytest-asyncio` for testing async code` without copying the notes.
- Drill 28: Find the file where ``pytest-asyncio` for testing async code` appears or should appear.
- Drill 29: Name one wrong implementation of ``pytest-asyncio` for testing async code` and why it would hurt.
- Drill 30: Name one test that would protect ``pytest-asyncio` for testing async code`.
- Drill 31: Draw the Week 15 data flow in four boxes.
- Drill 32: Say why `Async I/O Network Fetching` belongs in this month of the curriculum.
- Drill 33: Rewrite one error message in beginner-friendly language.
- Drill 34: List the exact assumptions made by the example code.
- Drill 35: List the exact assumptions checked by the tests.
- Drill 36: Point to the line where raw input becomes project meaning.
- Drill 37: Point to the line where the result becomes visible to a user.
- Drill 38: Explain what would happen if the main file were deleted.
- Drill 39: Explain what would happen if the main test were deleted.
- Drill 40: Describe the smallest manual check you can run.
- Drill 41: Describe the smallest automated check you can run.
- Drill 42: Name the most likely beginner mistake for this week.
- Drill 43: Name the safest recovery move for that mistake.
- Drill 44: Explain what knowledge should be carried into the next chapter.
- Drill 45: Trace ``asyncio` event loop: one thread, many concurrent waits` from user input to project result.
- Drill 46: Write one sentence defining ``asyncio` event loop: one thread, many concurrent waits` without copying the notes.
- Drill 47: Find the file where ``asyncio` event loop: one thread, many concurrent waits` appears or should appear.
- Drill 48: Name one wrong implementation of ``asyncio` event loop: one thread, many concurrent waits` and why it would hurt.
- Drill 49: Name one test that would protect ``asyncio` event loop: one thread, many concurrent waits`.
- Drill 50: Trace ``async def` and `await`: what they actually do` from user input to project result.
- Drill 51: Write one sentence defining ``async def` and `await`: what they actually do` without copying the notes.
- Drill 52: Find the file where ``async def` and `await`: what they actually do` appears or should appear.
- Drill 53: Name one wrong implementation of ``async def` and `await`: what they actually do` and why it would hurt.
- Drill 54: Name one test that would protect ``async def` and `await`: what they actually do`.
- Drill 55: Trace ``httpx.AsyncClient` for async HTTP requests` from user input to project result.
- Drill 56: Write one sentence defining ``httpx.AsyncClient` for async HTTP requests` without copying the notes.
- Drill 57: Find the file where ``httpx.AsyncClient` for async HTTP requests` appears or should appear.
- Drill 58: Name one wrong implementation of ``httpx.AsyncClient` for async HTTP requests` and why it would hurt.
- Drill 59: Name one test that would protect ``httpx.AsyncClient` for async HTTP requests`.
- Drill 60: Trace `Timeouts and retry logic: exponential backoff` from user input to project result.
- Drill 61: Write one sentence defining `Timeouts and retry logic: exponential backoff` without copying the notes.
- Drill 62: Find the file where `Timeouts and retry logic: exponential backoff` appears or should appear.
- Drill 63: Name one wrong implementation of `Timeouts and retry logic: exponential backoff` and why it would hurt.
- Drill 64: Name one test that would protect `Timeouts and retry logic: exponential backoff`.
- Drill 65: Trace `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` from user input to project result.
- Drill 66: Write one sentence defining `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` without copying the notes.
- Drill 67: Find the file where `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` appears or should appear.
- Drill 68: Name one wrong implementation of `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` and why it would hurt.
- Drill 69: Name one test that would protect `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor`.
- Drill 70: Trace ``pytest-asyncio` for testing async code` from user input to project result.
- Drill 71: Write one sentence defining ``pytest-asyncio` for testing async code` without copying the notes.
- Drill 72: Find the file where ``pytest-asyncio` for testing async code` appears or should appear.
- Drill 73: Name one wrong implementation of ``pytest-asyncio` for testing async code` and why it would hurt.
- Drill 74: Name one test that would protect ``pytest-asyncio` for testing async code`.
- Drill 75: Draw the Week 15 data flow in four boxes.
- Drill 76: Say why `Async I/O Network Fetching` belongs in this month of the curriculum.
- Drill 77: Rewrite one error message in beginner-friendly language.
- Drill 78: List the exact assumptions made by the example code.
- Drill 79: List the exact assumptions checked by the tests.
- Drill 80: Point to the line where raw input becomes project meaning.
- Drill 81: Point to the line where the result becomes visible to a user.
- Drill 82: Explain what would happen if the main file were deleted.
- Drill 83: Explain what would happen if the main test were deleted.
- Drill 84: Describe the smallest manual check you can run.
- Drill 85: Describe the smallest automated check you can run.
- Drill 86: Name the most likely beginner mistake for this week.
- Drill 87: Name the safest recovery move for that mistake.
- Drill 88: Explain what knowledge should be carried into the next chapter.
- Drill 89: Trace ``asyncio` event loop: one thread, many concurrent waits` from user input to project result.
- Drill 90: Write one sentence defining ``asyncio` event loop: one thread, many concurrent waits` without copying the notes.
- Drill 91: Find the file where ``asyncio` event loop: one thread, many concurrent waits` appears or should appear.
- Drill 92: Name one wrong implementation of ``asyncio` event loop: one thread, many concurrent waits` and why it would hurt.
- Drill 93: Name one test that would protect ``asyncio` event loop: one thread, many concurrent waits`.
- Drill 94: Trace ``async def` and `await`: what they actually do` from user input to project result.
- Drill 95: Write one sentence defining ``async def` and `await`: what they actually do` without copying the notes.
- Drill 96: Find the file where ``async def` and `await`: what they actually do` appears or should appear.
- Drill 97: Name one wrong implementation of ``async def` and `await`: what they actually do` and why it would hurt.
- Drill 98: Name one test that would protect ``async def` and `await`: what they actually do`.
- Drill 99: Trace ``httpx.AsyncClient` for async HTTP requests` from user input to project result.
- Drill 100: Write one sentence defining ``httpx.AsyncClient` for async HTTP requests` without copying the notes.
- Drill 101: Find the file where ``httpx.AsyncClient` for async HTTP requests` appears or should appear.
- Drill 102: Name one wrong implementation of ``httpx.AsyncClient` for async HTTP requests` and why it would hurt.
- Drill 103: Name one test that would protect ``httpx.AsyncClient` for async HTTP requests`.
- Drill 104: Trace `Timeouts and retry logic: exponential backoff` from user input to project result.
- Drill 105: Write one sentence defining `Timeouts and retry logic: exponential backoff` without copying the notes.
- Drill 106: Find the file where `Timeouts and retry logic: exponential backoff` appears or should appear.
- Drill 107: Name one wrong implementation of `Timeouts and retry logic: exponential backoff` and why it would hurt.
- Drill 108: Name one test that would protect `Timeouts and retry logic: exponential backoff`.
- Drill 109: Trace `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` from user input to project result.
- Drill 110: Write one sentence defining `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` without copying the notes.
- Drill 111: Find the file where `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` appears or should appear.
- Drill 112: Name one wrong implementation of `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor` and why it would hurt.
- Drill 113: Name one test that would protect `Never block the event loop: CPU-bound work belongs in ProcessPoolExecutor`.
- Drill 114: Trace ``pytest-asyncio` for testing async code` from user input to project result.
- Drill 115: Write one sentence defining ``pytest-asyncio` for testing async code` without copying the notes.
- Drill 116: Find the file where ``pytest-asyncio` for testing async code` appears or should appear.
- Drill 117: Name one wrong implementation of ``pytest-asyncio` for testing async code` and why it would hurt.
- Drill 118: Name one test that would protect ``pytest-asyncio` for testing async code`.
- Drill 119: Draw the Week 15 data flow in four boxes.
- Drill 120: Say why `Async I/O Network Fetching` belongs in this month of the curriculum.
- Drill 121: Rewrite one error message in beginner-friendly language.
- Drill 122: List the exact assumptions made by the example code.
- Drill 123: List the exact assumptions checked by the tests.
- Drill 124: Point to the line where raw input becomes project meaning.
- Drill 125: Point to the line where the result becomes visible to a user.
- Drill 126: Explain what would happen if the main file were deleted.
- Drill 127: Explain what would happen if the main test were deleted.
- Drill 128: Describe the smallest manual check you can run.
- Drill 129: Describe the smallest automated check you can run.
- Drill 130: Name the most likely beginner mistake for this week.
- Drill 131: Name the safest recovery move for that mistake.
- Drill 132: Explain what knowledge should be carried into the next chapter.
- Drill 133: Trace ``asyncio` event loop: one thread, many concurrent waits` from user input to project result.
- Drill 134: Write one sentence defining ``asyncio` event loop: one thread, many concurrent waits` without copying the notes.
- Drill 135: Find the file where ``asyncio` event loop: one thread, many concurrent waits` appears or should appear.
- Drill 136: Name one wrong implementation of ``asyncio` event loop: one thread, many concurrent waits` and why it would hurt.
- Drill 137: Name one test that would protect ``asyncio` event loop: one thread, many concurrent waits`.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes

## Synchronous vs asynchronous code: the core idea

In synchronous code, statements execute one at a time, in order. Each statement must finish before the next one starts.

```python
import time

def fetch_one(url: str) -> str:
    time.sleep(2)          # pretend this is a network round-trip
    return f"content of {url}"

result_a = fetch_one("https://example.com/a")   # waits 2 seconds
result_b = fetch_one("https://example.com/b")   # waits another 2 seconds
# total: 4 seconds
```

The two requests run sequentially. While waiting for `a` to respond, the program does nothing. The CPU is idle. That is waste.

Asynchronous code allows the program to do useful work while waiting. Instead of blocking until a response arrives, the program suspends that operation and moves on to other work.

```python
import asyncio

async def fetch_one(url: str) -> str:
    await asyncio.sleep(2)   # suspend here; let other tasks run
    return f"content of {url}"

async def fetch_all() -> None:
    results = await asyncio.gather(
        fetch_one("https://example.com/a"),
        fetch_one("https://example.com/b"),
    )
    # total: ~2 seconds (both run concurrently)
```

Both fetches start almost simultaneously. While one waits, the other makes progress. The total time is approximately 2 seconds, not 4.

---

## The event loop

Python's `asyncio` module runs on an event loop. The event loop is a scheduler that manages all running coroutines. It works like this:

1. You start the event loop with `asyncio.run(main())`.
2. The loop calls your `main` coroutine.
3. When a coroutine hits `await`, it tells the loop "I'm waiting for something — run someone else."
4. The loop picks the next ready coroutine and runs it.
5. When the awaited operation finishes, the loop resumes the original coroutine.

This happens in a single thread. There is no parallelism. Coroutines take turns using the CPU. They are cooperative: they voluntarily yield control at `await` points.

---

## What is a coroutine?

A coroutine is a function defined with `async def`. Calling it does not run it — it returns a coroutine object. The coroutine runs only when it is awaited or given to the event loop.

```python
async def greet(name: str) -> str:       # line 1: define a coroutine
    await asyncio.sleep(0)               # line 2: yield to the event loop (no-op sleep)
    return f"Hello, {name}"             # line 3: return a value

result = await greet("Alice")            # line 4: run the coroutine and get the result
```

Line 1: `async def` marks this as a coroutine function.

Line 2: `await asyncio.sleep(0)` suspends for zero seconds, giving the event loop a chance to run other tasks. This is often used in tests to simulate a yield point.

Line 3: returns the result normally.

Line 4: `await greet("Alice")` runs the coroutine and waits for its result. You can only `await` inside an `async def` function.

---

## Tasks

A task is a scheduled coroutine. When you create a task, the event loop schedules it to run independently of the current coroutine.

```python
async def main() -> None:
    task_a = asyncio.create_task(fetch_one("url_a"))   # line 1: schedule
    task_b = asyncio.create_task(fetch_one("url_b"))   # line 2: schedule
    result_a = await task_a                            # line 3: wait for result
    result_b = await task_b                            # line 4: wait for result
```

Line 1–2: create two tasks. They start running immediately (as soon as the event loop gets control).

Line 3–4: wait for each to finish. If `task_a` finishes first, awaiting `task_b` does not restart `task_a`.

Using `asyncio.gather` is more concise for multiple tasks:

```python
results = await asyncio.gather(fetch_one("url_a"), fetch_one("url_b"))
```

`gather` collects all results in order, even if the tasks complete out of order.

---

## I/O-bound vs CPU-bound work

This is the most important distinction for async programming.

**I/O-bound work** spends most of its time waiting: waiting for a network response, waiting for a disk read, waiting for a database query. The CPU is idle during that wait. Async helps here because while one I/O operation waits, the event loop runs other coroutines.

**CPU-bound work** spends most of its time computing: parsing a PDF, running a machine learning model, sorting a huge list. The CPU is fully occupied. Async does NOT help here. A coroutine doing CPU-heavy work blocks the event loop for the entire duration, preventing all other coroutines from running.

```
Async waits efficiently.
Async does not make CPU-heavy work magically faster.
```

This rule is worth repeating until it is automatic.

Consequences:
- Network fetching → async. Good fit.
- PDF parsing → synchronous or multiprocessing. Not async.
- Embedding computation → synchronous or multiprocessing. Not async.
- Database queries → async (with an async driver like `aiosqlite`). Good fit.

If you put PDF parsing inside an `async def` function, you block the event loop. Every other coroutine stalls until parsing completes. This is worse than just running it synchronously.

---

## Async HTTP client

For async HTTP requests, use `httpx.AsyncClient`:

```python
import httpx


async def fetch(url: str) -> str:                         # line 1
    async with httpx.AsyncClient(timeout=10.0) as client: # line 2
        response = await client.get(url)                  # line 3
        response.raise_for_status()                       # line 4
        return response.text                              # line 5
```

Line 1: async function — it can be awaited.

Line 2: `async with` creates the client and ensures it is closed when the block exits, even if an exception is raised. `timeout=10.0` sets a 10-second timeout on the request.

Line 3: `await client.get(url)` suspends this coroutine while waiting for the server to respond. The event loop runs other tasks during this wait.

Line 4: raises `httpx.HTTPStatusError` if the status code indicates failure (4xx, 5xx).

Line 5: returns the response body as a string.

---

## Timeouts

Without a timeout, a hanging server can stall your coroutine indefinitely.

```python
async with httpx.AsyncClient(timeout=10.0) as client:
    try:
        response = await client.get(url)
    except httpx.TimeoutException:
        # handle timeout
        raise
```

Always set a timeout. A good default for academic APIs is 10–30 seconds. For internal services, 5 seconds is usually generous.

`httpx.Timeout` lets you set different timeouts for connect, read, and write phases:
```python
timeout = httpx.Timeout(connect=5.0, read=30.0, write=10.0)
```

---

## Retries and backoff

Not all failures are permanent. A `503 Service Unavailable` might resolve in a second. A timeout might be a brief network blip. Retrying with a short wait can recover from these.

```python
async def fetch_with_retry(url: str, max_attempts: int = 3) -> str:
    last_error: Exception | None = None
    for attempt in range(max_attempts):                       # line 1
        try:
            return await fetch(url)                           # line 2
        except (httpx.TimeoutException, httpx.HTTPStatusError) as exc:
            last_error = exc                                  # line 3
            wait = 0.5 * (attempt + 1)                        # line 4
            await asyncio.sleep(wait)                         # line 5
    raise RuntimeError(f"Failed after {max_attempts} attempts") from last_error  # line 6
```

Line 1: try up to `max_attempts` times.

Line 2: if the fetch succeeds, return immediately.

Line 3: save the exception.

Line 4: compute wait time. First retry waits 0.5s, second waits 1.0s, third waits 1.5s. This is linear backoff.

Line 5: `await asyncio.sleep(wait)` suspends without blocking. The event loop runs other tasks during the wait.

Line 6: if all attempts fail, raise a descriptive error that wraps the last exception.

**When to retry:** temporary failures — timeouts, 429 (rate limit), 503 (temporary unavailability).

**When not to retry:** permanent failures — 404 (not found), 400 (bad request), 401 (unauthorized). Retrying these wastes time and may cause harm.

---

## Concurrency limits with semaphores

Just because async can launch hundreds of concurrent requests does not mean it should. Too many concurrent requests can:
- Overwhelm the remote server (especially academic APIs).
- Hit your machine's file descriptor limits.
- Trigger rate limiting (429 responses).

A semaphore is a counter that limits how many coroutines can be in a critical section simultaneously.

```python
semaphore = asyncio.Semaphore(10)          # line 1: allow at most 10 concurrent


async def fetch_bounded(url: str) -> str:
    async with semaphore:                  # line 2: acquire before fetching
        return await fetch(url)            # line 3: fetch (semaphore released when block exits)
```

Line 1: create a semaphore with a limit of 10.

Line 2: `async with semaphore` decrements the counter. If the counter is already 0, this coroutine suspends until another coroutine releases the semaphore.

Line 3: do the actual work. When the `async with` block exits, the semaphore is released (counter incremented).

A good default limit for public academic APIs is 5–10 concurrent requests.

---

## Cancellation

Sometimes you want to abandon a running operation. `asyncio.wait_for` adds a deadline:

```python
try:
    result = await asyncio.wait_for(fetch(url), timeout=15.0)
except asyncio.TimeoutError:
    # the coroutine was cancelled
    pass
```

When the timeout expires, `asyncio` raises `CancelledError` inside the coroutine at its next `await` point. The coroutine can catch it to do cleanup, but must re-raise it (or let it propagate) to actually cancel.

Do not silently swallow `CancelledError` in most cases. If you catch it for cleanup, re-raise it:

```python
try:
    result = await some_operation()
except asyncio.CancelledError:
    await cleanup()
    raise  # always re-raise CancelledError
```

---

## Testing async code

Use `pytest-asyncio` to write async test functions:

```bash
pip install pytest-asyncio
```

```python
import pytest


@pytest.mark.asyncio
async def test_fetch_success() -> None:
    result = await fetch_with_retry("https://httpbin.org/get")
    assert result is not None
```

However, tests must not depend on real network access. Use a fake HTTP client:

```python
class FakeHttpClient:
    def __init__(self, responses: dict[str, str]) -> None:
        self._responses = responses

    async def get(self, url: str) -> "FakeResponse":
        if url not in self._responses:
            raise httpx.TimeoutException(f"No mock for {url}")
        return FakeResponse(self._responses[url])


class FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text
        self.status_code = 200

    def raise_for_status(self) -> None:
        pass
```

Inject the fake in tests. This gives you complete control over responses, timeouts, and error conditions without any network activity.

---

## Partial failure and batch results

When fetching a batch of URLs, do not crash the entire batch if one URL fails. Return structured results:

```python
from dataclasses import dataclass


@dataclass
class FetchResult:
    url: str
    content: str | None
    error: str | None


async def fetch_batch(urls: list[str]) -> list[FetchResult]:
    async def fetch_one_safe(url: str) -> FetchResult:
        try:
            content = await fetch_with_retry(url)
            return FetchResult(url=url, content=content, error=None)
        except Exception as exc:
            return FetchResult(url=url, content=None, error=str(exc))

    return list(await asyncio.gather(*(fetch_one_safe(url) for url in urls)))
```

This returns one `FetchResult` per URL. Successes have `content`. Failures have `error`. The caller decides what to do with partial failures.

---

## Summary

- Synchronous code waits serially. One operation at a time.
- Asynchronous code suspends at `await` points, letting the event loop run other coroutines.
- The event loop is a single-threaded cooperative scheduler.
- A coroutine is an `async def` function. Calling it returns a coroutine object; it only runs when awaited.
- A task is a scheduled coroutine. `asyncio.gather` runs multiple tasks concurrently.
- **Async helps I/O-bound work. It does not help CPU-bound work.**
- PDF parsing, embedding computation, and data transformation are CPU-bound. Do not put them in async paths.
- Network fetching is I/O-bound. Always use async for it.
- Always set timeouts. Without them, one hanging server stalls your program.
- Retry only recoverable failures. Do not retry 404 or 400.
- Use semaphores to cap concurrent requests and protect remote services.
- Use `FakeHttpClient` in tests — never real network access.
- Return structured batch results that capture partial failures.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 15 — Async IO and Network Fetching:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
