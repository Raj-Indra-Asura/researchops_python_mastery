<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 14 — FastAPI Layer:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 14 FastAPI Layer

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 14: FastAPI Layer

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Your work, available over HTTP**.
The practical milestone is: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
The expected capability is: Can define REST endpoints with FastAPI, inject dependencies, validate responses with Pydantic, and test the API without running a real server. ---
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

- Week 10 taught Testing Discipline and Quality Gates; keep its responsibility in mind, but do not rebuild it here.
- Week 11 taught Classical ML — Topic Classification; keep its responsibility in mind, but do not rebuild it here.
- Week 12 taught Experiment Tracking; keep its responsibility in mind, but do not rebuild it here.
- Week 13 taught Embeddings and Semantic Search; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 14 solves the project problem behind **FastAPI Layer**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `FastAPI app factory pattern` helps solve part of this gap.
- The concept `Route handlers that delegate to services (no business logic in routes)` helps solve part of this gap.
- The concept ``Depends` for dependency injection` helps solve part of this gap.
- The concept `Pydantic response models: validating what you return` helps solve part of this gap.
- The concept `HTTP status codes: 200, 201, 404, 422, 500` helps solve part of this gap.
- The concept `Testing with `httpx.AsyncClient` / `TestClient`` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **FastAPI Layer**?
- Ask: what is the owner for **FastAPI Layer**?
- Ask: what is the transformation for **FastAPI Layer**?
- Ask: what is the proof for **FastAPI Layer**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| FastAPI app factory pattern | FastAPI app factory pattern | This term names one job in the Week 14 milestone. |
| Route handlers that delegate to services (no business logic in routes) | Route handlers that delegate to services (no business logic in routes) | This term names one job in the Week 14 milestone. |
| Depends` for dependency injection | `Depends` for dependency injection | This term names one job in the Week 14 milestone. |
| Pydantic response models | Pydantic response models: validating what you return | This term names one job in the Week 14 milestone. |
| HTTP status codes | HTTP status codes: 200, 201, 404, 422, 500 | This term names one job in the Week 14 milestone. |
| Testing with `httpx.AsyncClient` / `TestClient | Testing with `httpx.AsyncClient` / `TestClient` | This term names one job in the Week 14 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: FastAPI app factory pattern
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 14, it supports the milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Route handlers that delegate to services (no business logic in routes)
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 14, it supports the milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: `Depends` for dependency injection
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 14, it supports the milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Pydantic response models: validating what you return
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 14, it supports the milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: HTTP status codes: 200, 201, 404, 422, 500
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 14, it supports the milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: Testing with `httpx.AsyncClient` / `TestClient`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 14, it supports the milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/api/main.py` — FastAPI app factory
- `src/researchops/api/routes/papers.py` — papers routes
- `src/researchops/api/routes/search.py` — search routes
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
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

Line-by-line explanation:
- Line 1: `from fastapi import FastAPI` — This imports a tool before the example can use it.
- Line 2: `(blank line)` — This blank line separates ideas so the example is easier to read.
- Line 3: `app = FastAPI()` — This stores a clear intermediate value for the next step.
- Line 4: `(blank line)` — This blank line separates ideas so the example is easier to read.
- Line 5: `@app.get("/health")` — This attaches framework or test behavior to the next function or class.
- Line 6: `def health() -> dict[str, str]:` — This names a reusable action and shows what information it receives.
- Line 7: `return {"status": "ok"}` — This produces the result or performs the declared setup step.

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
- `tests/e2e/test_api.py` — endpoint tests with TestClient
Validation commands:
```bash
uvicorn researchops.api.main:app --reload &
curl http://localhost:8000/health
pytest tests/e2e/test_api.py -v
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
Week 14 contributes by making **fastapi layer** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 14 solve?
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

- Explain FastAPI Layer in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: FastAPI Layer.
- The milestone: `GET /papers`, `GET /papers/{id}`, `GET /papers/search?q=QUERY`, `GET /health` work and return correct JSON.
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

Next week is Week 15: **Async I/O Network Fetching**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops fetch-arxiv "transformers"` downloads paper metadata from the arXiv API asynchronously. `researchops fetch-url URL` fetches a single paper.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `FastAPI app factory pattern` from user input to project result.
- Drill 2: Write one sentence defining `FastAPI app factory pattern` without copying the notes.
- Drill 3: Find the file where `FastAPI app factory pattern` appears or should appear.
- Drill 4: Name one wrong implementation of `FastAPI app factory pattern` and why it would hurt.
- Drill 5: Name one test that would protect `FastAPI app factory pattern`.
- Drill 6: Trace `Route handlers that delegate to services (no business logic in routes)` from user input to project result.
- Drill 7: Write one sentence defining `Route handlers that delegate to services (no business logic in routes)` without copying the notes.
- Drill 8: Find the file where `Route handlers that delegate to services (no business logic in routes)` appears or should appear.
- Drill 9: Name one wrong implementation of `Route handlers that delegate to services (no business logic in routes)` and why it would hurt.
- Drill 10: Name one test that would protect `Route handlers that delegate to services (no business logic in routes)`.
- Drill 11: Trace ``Depends` for dependency injection` from user input to project result.
- Drill 12: Write one sentence defining ``Depends` for dependency injection` without copying the notes.
- Drill 13: Find the file where ``Depends` for dependency injection` appears or should appear.
- Drill 14: Name one wrong implementation of ``Depends` for dependency injection` and why it would hurt.
- Drill 15: Name one test that would protect ``Depends` for dependency injection`.
- Drill 16: Trace `Pydantic response models: validating what you return` from user input to project result.
- Drill 17: Write one sentence defining `Pydantic response models: validating what you return` without copying the notes.
- Drill 18: Find the file where `Pydantic response models: validating what you return` appears or should appear.
- Drill 19: Name one wrong implementation of `Pydantic response models: validating what you return` and why it would hurt.
- Drill 20: Name one test that would protect `Pydantic response models: validating what you return`.
- Drill 21: Trace `HTTP status codes: 200, 201, 404, 422, 500` from user input to project result.
- Drill 22: Write one sentence defining `HTTP status codes: 200, 201, 404, 422, 500` without copying the notes.
- Drill 23: Find the file where `HTTP status codes: 200, 201, 404, 422, 500` appears or should appear.
- Drill 24: Name one wrong implementation of `HTTP status codes: 200, 201, 404, 422, 500` and why it would hurt.
- Drill 25: Name one test that would protect `HTTP status codes: 200, 201, 404, 422, 500`.
- Drill 26: Trace `Testing with `httpx.AsyncClient` / `TestClient`` from user input to project result.
- Drill 27: Write one sentence defining `Testing with `httpx.AsyncClient` / `TestClient`` without copying the notes.
- Drill 28: Find the file where `Testing with `httpx.AsyncClient` / `TestClient`` appears or should appear.
- Drill 29: Name one wrong implementation of `Testing with `httpx.AsyncClient` / `TestClient`` and why it would hurt.
- Drill 30: Name one test that would protect `Testing with `httpx.AsyncClient` / `TestClient``.
- Drill 31: Draw the Week 14 data flow in four boxes.
- Drill 32: Say why `FastAPI Layer` belongs in this month of the curriculum.
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
- Drill 45: Trace `FastAPI app factory pattern` from user input to project result.
- Drill 46: Write one sentence defining `FastAPI app factory pattern` without copying the notes.
- Drill 47: Find the file where `FastAPI app factory pattern` appears or should appear.
- Drill 48: Name one wrong implementation of `FastAPI app factory pattern` and why it would hurt.
- Drill 49: Name one test that would protect `FastAPI app factory pattern`.
- Drill 50: Trace `Route handlers that delegate to services (no business logic in routes)` from user input to project result.
- Drill 51: Write one sentence defining `Route handlers that delegate to services (no business logic in routes)` without copying the notes.
- Drill 52: Find the file where `Route handlers that delegate to services (no business logic in routes)` appears or should appear.
- Drill 53: Name one wrong implementation of `Route handlers that delegate to services (no business logic in routes)` and why it would hurt.
- Drill 54: Name one test that would protect `Route handlers that delegate to services (no business logic in routes)`.
- Drill 55: Trace ``Depends` for dependency injection` from user input to project result.
- Drill 56: Write one sentence defining ``Depends` for dependency injection` without copying the notes.
- Drill 57: Find the file where ``Depends` for dependency injection` appears or should appear.
- Drill 58: Name one wrong implementation of ``Depends` for dependency injection` and why it would hurt.
- Drill 59: Name one test that would protect ``Depends` for dependency injection`.
- Drill 60: Trace `Pydantic response models: validating what you return` from user input to project result.
- Drill 61: Write one sentence defining `Pydantic response models: validating what you return` without copying the notes.
- Drill 62: Find the file where `Pydantic response models: validating what you return` appears or should appear.
- Drill 63: Name one wrong implementation of `Pydantic response models: validating what you return` and why it would hurt.
- Drill 64: Name one test that would protect `Pydantic response models: validating what you return`.
- Drill 65: Trace `HTTP status codes: 200, 201, 404, 422, 500` from user input to project result.
- Drill 66: Write one sentence defining `HTTP status codes: 200, 201, 404, 422, 500` without copying the notes.
- Drill 67: Find the file where `HTTP status codes: 200, 201, 404, 422, 500` appears or should appear.
- Drill 68: Name one wrong implementation of `HTTP status codes: 200, 201, 404, 422, 500` and why it would hurt.
- Drill 69: Name one test that would protect `HTTP status codes: 200, 201, 404, 422, 500`.
- Drill 70: Trace `Testing with `httpx.AsyncClient` / `TestClient`` from user input to project result.
- Drill 71: Write one sentence defining `Testing with `httpx.AsyncClient` / `TestClient`` without copying the notes.
- Drill 72: Find the file where `Testing with `httpx.AsyncClient` / `TestClient`` appears or should appear.
- Drill 73: Name one wrong implementation of `Testing with `httpx.AsyncClient` / `TestClient`` and why it would hurt.
- Drill 74: Name one test that would protect `Testing with `httpx.AsyncClient` / `TestClient``.
- Drill 75: Draw the Week 14 data flow in four boxes.
- Drill 76: Say why `FastAPI Layer` belongs in this month of the curriculum.
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
- Drill 89: Trace `FastAPI app factory pattern` from user input to project result.
- Drill 90: Write one sentence defining `FastAPI app factory pattern` without copying the notes.
- Drill 91: Find the file where `FastAPI app factory pattern` appears or should appear.
- Drill 92: Name one wrong implementation of `FastAPI app factory pattern` and why it would hurt.
- Drill 93: Name one test that would protect `FastAPI app factory pattern`.
- Drill 94: Trace `Route handlers that delegate to services (no business logic in routes)` from user input to project result.
- Drill 95: Write one sentence defining `Route handlers that delegate to services (no business logic in routes)` without copying the notes.
- Drill 96: Find the file where `Route handlers that delegate to services (no business logic in routes)` appears or should appear.
- Drill 97: Name one wrong implementation of `Route handlers that delegate to services (no business logic in routes)` and why it would hurt.
- Drill 98: Name one test that would protect `Route handlers that delegate to services (no business logic in routes)`.
- Drill 99: Trace ``Depends` for dependency injection` from user input to project result.
- Drill 100: Write one sentence defining ``Depends` for dependency injection` without copying the notes.
- Drill 101: Find the file where ``Depends` for dependency injection` appears or should appear.
- Drill 102: Name one wrong implementation of ``Depends` for dependency injection` and why it would hurt.
- Drill 103: Name one test that would protect ``Depends` for dependency injection`.
- Drill 104: Trace `Pydantic response models: validating what you return` from user input to project result.
- Drill 105: Write one sentence defining `Pydantic response models: validating what you return` without copying the notes.
- Drill 106: Find the file where `Pydantic response models: validating what you return` appears or should appear.
- Drill 107: Name one wrong implementation of `Pydantic response models: validating what you return` and why it would hurt.
- Drill 108: Name one test that would protect `Pydantic response models: validating what you return`.
- Drill 109: Trace `HTTP status codes: 200, 201, 404, 422, 500` from user input to project result.
- Drill 110: Write one sentence defining `HTTP status codes: 200, 201, 404, 422, 500` without copying the notes.
- Drill 111: Find the file where `HTTP status codes: 200, 201, 404, 422, 500` appears or should appear.
- Drill 112: Name one wrong implementation of `HTTP status codes: 200, 201, 404, 422, 500` and why it would hurt.
- Drill 113: Name one test that would protect `HTTP status codes: 200, 201, 404, 422, 500`.
- Drill 114: Trace `Testing with `httpx.AsyncClient` / `TestClient`` from user input to project result.
- Drill 115: Write one sentence defining `Testing with `httpx.AsyncClient` / `TestClient`` without copying the notes.
- Drill 116: Find the file where `Testing with `httpx.AsyncClient` / `TestClient`` appears or should appear.
- Drill 117: Name one wrong implementation of `Testing with `httpx.AsyncClient` / `TestClient`` and why it would hurt.
- Drill 118: Name one test that would protect `Testing with `httpx.AsyncClient` / `TestClient``.
- Drill 119: Draw the Week 14 data flow in four boxes.
- Drill 120: Say why `FastAPI Layer` belongs in this month of the curriculum.
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
- Drill 133: Trace `FastAPI app factory pattern` from user input to project result.
- Drill 134: Write one sentence defining `FastAPI app factory pattern` without copying the notes.
- Drill 135: Find the file where `FastAPI app factory pattern` appears or should appear.
- Drill 136: Name one wrong implementation of `FastAPI app factory pattern` and why it would hurt.
- Drill 137: Name one test that would protect `FastAPI app factory pattern`.
- Drill 138: Trace `Route handlers that delegate to services (no business logic in routes)` from user input to project result.
- Drill 139: Write one sentence defining `Route handlers that delegate to services (no business logic in routes)` without copying the notes.
- Drill 140: Find the file where `Route handlers that delegate to services (no business logic in routes)` appears or should appear.
- Drill 141: Name one wrong implementation of `Route handlers that delegate to services (no business logic in routes)` and why it would hurt.
- Drill 142: Name one test that would protect `Route handlers that delegate to services (no business logic in routes)`.
- Drill 143: Trace ``Depends` for dependency injection` from user input to project result.
- Drill 144: Write one sentence defining ``Depends` for dependency injection` without copying the notes.
- Drill 145: Find the file where ``Depends` for dependency injection` appears or should appear.
- Drill 146: Name one wrong implementation of ``Depends` for dependency injection` and why it would hurt.
- Drill 147: Name one test that would protect ``Depends` for dependency injection`.
- Drill 148: Trace `Pydantic response models: validating what you return` from user input to project result.
- Drill 149: Write one sentence defining `Pydantic response models: validating what you return` without copying the notes.
- Drill 150: Find the file where `Pydantic response models: validating what you return` appears or should appear.
- Drill 151: Name one wrong implementation of `Pydantic response models: validating what you return` and why it would hurt.
- Drill 152: Name one test that would protect `Pydantic response models: validating what you return`.
- Drill 153: Trace `HTTP status codes: 200, 201, 404, 422, 500` from user input to project result.
- Drill 154: Write one sentence defining `HTTP status codes: 200, 201, 404, 422, 500` without copying the notes.
- Drill 155: Find the file where `HTTP status codes: 200, 201, 404, 422, 500` appears or should appear.
- Drill 156: Name one wrong implementation of `HTTP status codes: 200, 201, 404, 422, 500` and why it would hurt.
- Drill 157: Name one test that would protect `HTTP status codes: 200, 201, 404, 422, 500`.
- Drill 158: Trace `Testing with `httpx.AsyncClient` / `TestClient`` from user input to project result.
- Drill 159: Write one sentence defining `Testing with `httpx.AsyncClient` / `TestClient`` without copying the notes.
- Drill 160: Find the file where `Testing with `httpx.AsyncClient` / `TestClient`` appears or should appear.
- Drill 161: Name one wrong implementation of `Testing with `httpx.AsyncClient` / `TestClient`` and why it would hurt.
- Drill 162: Name one test that would protect `Testing with `httpx.AsyncClient` / `TestClient``.
- Drill 163: Draw the Week 14 data flow in four boxes.
- Drill 164: Say why `FastAPI Layer` belongs in this month of the curriculum.
- Drill 165: Rewrite one error message in beginner-friendly language.
- Drill 166: List the exact assumptions made by the example code.
- Drill 167: List the exact assumptions checked by the tests.
- Drill 168: Point to the line where raw input becomes project meaning.
- Drill 169: Point to the line where the result becomes visible to a user.
- Drill 170: Explain what would happen if the main file were deleted.
- Drill 171: Explain what would happen if the main test were deleted.
- Drill 172: Describe the smallest manual check you can run.
- Drill 173: Describe the smallest automated check you can run.
- Drill 174: Name the most likely beginner mistake for this week.
- Drill 175: Name the safest recovery move for that mistake.
- Drill 176: Explain what knowledge should be carried into the next chapter.
- Drill 177: Trace `FastAPI app factory pattern` from user input to project result.
- Drill 178: Write one sentence defining `FastAPI app factory pattern` without copying the notes.
- Drill 179: Find the file where `FastAPI app factory pattern` appears or should appear.
- Drill 180: Name one wrong implementation of `FastAPI app factory pattern` and why it would hurt.
- Drill 181: Name one test that would protect `FastAPI app factory pattern`.
- Drill 182: Trace `Route handlers that delegate to services (no business logic in routes)` from user input to project result.
- Drill 183: Write one sentence defining `Route handlers that delegate to services (no business logic in routes)` without copying the notes.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes

## What a web API is

An API is a way for one program to talk to another. A web API uses HTTP — the same protocol a web browser uses — so that any program, on any machine, can communicate with your application over a network.

Until now, ResearchOps only ran from the command line. That means only a human with terminal access can use it. An HTTP API changes that: a web frontend, a mobile app, a data pipeline, a teammate's script, or an automated test can all send a request and get a structured response.

---

## HTTP from first principles

HTTP is a request-response protocol. A client sends a request. The server returns a response. That is the entire model.

### The request

A request has four main parts:

**Method** — a verb that describes what the client wants to do.

| Method | Meaning |
|--------|---------|
| `GET` | Read or retrieve something |
| `POST` | Create or submit something |
| `PUT` | Replace something |
| `PATCH` | Update part of something |
| `DELETE` | Remove something |

**Path** — the URL path that identifies the resource. For example `/search`, `/documents/42`, `/health`.

**Query parameters** — optional key-value pairs appended to the URL after a `?`. For example: `/search?query=transformers&limit=5`. They are often used to filter or configure a GET request.

**Body** — data sent with the request. Usually JSON. Only meaningful for methods like POST, PUT, and PATCH. GET requests should not have a body.

### The response

A response has three main parts:

**Status code** — a three-digit number that tells the client whether the request succeeded or failed, and why.

| Code | Meaning |
|------|---------|
| `200 OK` | Request succeeded. Response body contains the result. |
| `201 Created` | Resource was created successfully. |
| `400 Bad Request` | Client sent invalid input. The client must fix the request. |
| `404 Not Found` | The resource does not exist. |
| `422 Unprocessable Entity` | FastAPI validation error — the body did not match the schema. |
| `500 Internal Server Error` | Something unexpected broke on the server side. |

**Headers** — metadata about the response. For example, `Content-Type: application/json` tells the client the body is JSON.

**Body** — the response data. Usually JSON when building an API.

---

## JSON

JSON is the standard text format for API data. It maps closely to Python dicts, lists, strings, numbers, and booleans.

```json
{
  "query": "attention mechanism",
  "limit": 5,
  "results": [
    {"title": "Transformers paper", "score": 0.92, "snippet": "..."},
    {"title": "BERT", "score": 0.88, "snippet": "..."}
  ]
}
```

Python's `json` module can parse and generate JSON. FastAPI does this automatically for you when you return a dict or a Pydantic model.

---

## FastAPI from first principles

FastAPI is a Python web framework. It lets you define routes — URL paths with handler functions — and handles the HTTP plumbing for you.

```python
from fastapi import FastAPI       # line 1

app = FastAPI()                   # line 2


@app.get("/health")               # line 3
def health() -> dict[str, str]:   # line 4
    return {"status": "ok"}       # line 5
```

Line 1: import the `FastAPI` class.

Line 2: create the application object. This is the central object that registers routes and starts the server.

Line 3: the `@app.get("/health")` decorator tells FastAPI: "when a GET request arrives at `/health`, call the function below". The decorator registers the route.

Line 4: the handler function. It takes no parameters here because this is a simple status check.

Line 5: return a Python dict. FastAPI automatically serialises this to JSON and sets `Content-Type: application/json`.

To run locally:
```bash
uvicorn researchops.api.main:app --reload
```

Then visit `http://localhost:8000/health` in a browser or with `curl`.

---

## Pydantic models for validation

Pydantic is FastAPI's data validation library. You define a class that inherits from `BaseModel`, declare fields with types, and Pydantic validates incoming data automatically.

```python
from pydantic import BaseModel    # line 1


class SearchRequest(BaseModel):   # line 2
    query: str                    # line 3
    limit: int = 5                # line 4
```

Line 1: import `BaseModel` from Pydantic.

Line 2: define the schema. Any class inheriting `BaseModel` becomes a schema.

Line 3: `query` is a required `str`. If the client omits it or sends a non-string, Pydantic raises a validation error and FastAPI returns `422` automatically.

Line 4: `limit` is an optional `int` with a default of 5. If the client does not include it, the default is used.

Response schemas work the same way:

```python
class SearchHitResponse(BaseModel):
    title: str
    score: float
    snippet: str
```

When you return an instance of this class, FastAPI serialises it to JSON. The fields and types are documented automatically.

---

## Why API comes after CLI

Weeks 1–12 built the CLI, services, and storage. The API reuses all of that. The rule is:

> Route handlers must stay thin. They parse input, call a service, and shape the response. Business logic belongs in services, not in routes.

A route that does its own database queries, validation, and computation is hard to test, hard to maintain, and breaks the separation of concerns built in earlier weeks.

Compare a fat route to a thin route:

**Fat route (wrong):**
```python
@app.post("/search")
def search(body: dict) -> list:
    # queries database directly
    # applies ranking logic here
    # formats response here
    return results
```

**Thin route (correct):**
```python
@app.post("/search")
def search(request: SearchRequest, service: SearchService = Depends(get_search_service)) -> list[SearchHitResponse]:
    hits = service.search(request.query, request.limit)
    return [SearchHitResponse(title=h.title, score=h.score, snippet=h.snippet) for h in hits]
```

The thin route does exactly three things: receive the validated request, call the service, and map the result to a response schema.

---

## Dependency injection

Dependency injection means a function receives the objects it needs rather than constructing them itself. FastAPI has a built-in system for this using `Depends`.

```python
from fastapi import Depends


def get_search_service() -> SearchService:      # line 1
    return SearchService(...)                   # line 2


@app.post("/search")
def search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),   # line 3
) -> list[SearchHitResponse]:
    hits = service.search(request.query, request.limit)
    return [SearchHitResponse(...) for h in hits]
```

Line 1: a plain Python function that returns a `SearchService`. This is a "dependency provider".

Line 2: construct and return the service. In practice this might read from settings, open a database connection, and pass it to the service.

Line 3: `Depends(get_search_service)` tells FastAPI: before calling `search`, call `get_search_service()` and pass its return value as `service`. FastAPI handles this for every request.

Why does this matter for tests? In tests you can replace the dependency with a fake:

```python
from fastapi.testclient import TestClient

app.dependency_overrides[get_search_service] = lambda: FakeSearchService()
client = TestClient(app)
```

Now every test request uses `FakeSearchService` instead of the real one. No database, no file system, fast tests.

---

## Status codes and error mapping

Do not return `200` for every response. Status codes carry meaning that clients rely on.

```python
from fastapi import HTTPException


@app.get("/documents/{doc_id}")
def get_document(doc_id: str, service: DocumentService = Depends(get_doc_service)) -> DocumentResponse:
    doc = service.get(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
    return DocumentResponse(...)
```

`HTTPException` is FastAPI's way to return an error response. The `detail` field is returned in the JSON body as `{"detail": "..."}`.

Common mapping rules:
- Domain "not found" → `404`
- Validation failure (your own logic) → `400` with a helpful message
- Unexpected exception → log it, return `500`, do not leak stack traces

Do not return `200` with `{"success": false}` in the body. That hides the error from automated clients.

---

## Testing the API

FastAPI's `TestClient` wraps the app in a test harness. Requests go through your route handlers, validation, and dependency injection — but no real network is involved.

```python
from fastapi.testclient import TestClient
from researchops.api.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")           # line 1
    assert response.status_code == 200         # line 2
    assert response.json() == {"status": "ok"} # line 3
```

Line 1: send a GET request to `/health`. Returns a `Response` object.

Line 2: check the HTTP status code.

Line 3: check the JSON body. `response.json()` parses the response body as JSON and returns a Python dict or list.

For routes that require a body:
```python
def test_search() -> None:
    response = client.post("/search", json={"query": "transformers", "limit": 3})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 3
```

Use `dependency_overrides` to inject fake services in tests. This avoids real database or file system operations.

---

## The API as an adapter

The most important architectural concept this week is that the API is just another adapter for your application. Your services, models, and storage did not change. The API layer is a new entry point — alongside the CLI — that connects the outside world to your existing logic.

This mirrors the CLI architecture from earlier weeks: CLI commands are thin adapters over services. API routes are thin adapters over the same services. Both use the same protocols and domain objects.

That is why good architecture from Month 3 pays dividends in Month 4. If services were well-defined and protocol-driven, adding an API layer is just plumbing.

---

## Summary

- HTTP is a request-response protocol: method + path + optional body → status code + body.
- Common methods: GET (read), POST (create/submit).
- Status codes communicate success (200, 201) and failure (400, 404, 500).
- FastAPI creates an app object, routes are registered with decorators.
- Pydantic models validate and document request and response data automatically.
- Route handlers must be thin: validate → call service → return response.
- Dependency injection keeps route code flexible and testable.
- Use `app.dependency_overrides` in tests to inject fakes.
- `TestClient` lets you test routes without a real server.
- The API is another adapter; services and business logic do not change.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 14 — FastAPI Layer:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
