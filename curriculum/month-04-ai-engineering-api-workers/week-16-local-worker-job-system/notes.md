<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)

**Week 16 — Local Worker Job System:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 16 Local Worker and Job System

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 16: Local Worker and Job System

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Work that happens in the background**.
The practical milestone is: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
The expected capability is: Can implement a state machine, build a polling worker loop, design idempotent job processing, and explain how to recover from worker crashes safely.
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

- Week 12 taught Experiment Tracking; keep its responsibility in mind, but do not rebuild it here.
- Week 13 taught Embeddings and Semantic Search; keep its responsibility in mind, but do not rebuild it here.
- Week 14 taught FastAPI Layer; keep its responsibility in mind, but do not rebuild it here.
- Week 15 taught Async I/O Network Fetching; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 16 solves the project problem behind **Local Worker and Job System**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `Job state machine: pending → running → done / failed` helps solve part of this gap.
- The concept `Persistent job queue in SQLite` helps solve part of this gap.
- The concept `Worker loop: poll → claim → execute → update state` helps solve part of this gap.
- The concept `Retry logic and idempotency` helps solve part of this gap.
- The concept `Worker failure recovery without data corruption` helps solve part of this gap.
- The concept ``JobService` and `JobRepository`` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Local Worker and Job System**?
- Ask: what is the owner for **Local Worker and Job System**?
- Ask: what is the transformation for **Local Worker and Job System**?
- Ask: what is the proof for **Local Worker and Job System**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| Job state machine | Job state machine: pending → running → done / failed | This term names one job in the Week 16 milestone. |
| Persistent job queue in SQLite | Persistent job queue in SQLite | This term names one job in the Week 16 milestone. |
| Worker loop | Worker loop: poll → claim → execute → update state | This term names one job in the Week 16 milestone. |
| Retry logic and idempotency | Retry logic and idempotency | This term names one job in the Week 16 milestone. |
| Worker failure recovery without data corruption | Worker failure recovery without data corruption | This term names one job in the Week 16 milestone. |
| JobService` and `JobRepository | `JobService` and `JobRepository` | This term names one job in the Week 16 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: Job state machine: pending → running → done / failed
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 16, it supports the milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Persistent job queue in SQLite
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 16, it supports the milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: Worker loop: poll → claim → execute → update state
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 16, it supports the milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Retry logic and idempotency
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 16, it supports the milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Worker failure recovery without data corruption
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 16, it supports the milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: `JobService` and `JobRepository`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 16, it supports the milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/storage/job_repository.py`
- `src/researchops/services/job_service.py`
- `src/researchops/workers/job_runner.py`
- `src/researchops/cli/commands/ingest.py` — `jobs list`, `jobs run`, `jobs retry` commands
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
def mark_running(job: Job) -> Job:
    if job.status != "pending":
        raise InvalidJobTransition(job.status)
    return job.with_status("running")
```

Line-by-line explanation:
- Line 1: `def mark_running(job: Job) -> Job:` — This names a reusable action and shows what information it receives.
- Line 2: `if job.status != "pending":` — This controls what happens when the normal path changes.
- Line 3: `raise InvalidJobTransition(job.status)` — This reports a meaningful failure instead of hiding it.
- Line 4: `return job.with_status("running")` — This produces the result or performs the declared setup step.

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
- `tests/unit/test_job_service.py` — state transitions with fake repo
- `tests/integration/test_job_repository.py`
Validation commands:
```bash
researchops jobs list
researchops jobs run
pytest tests/unit/test_job_service.py -v
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
Week 16 contributes by making **local worker and job system** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 16 solve?
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

- Explain Local Worker and Job System in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Local Worker and Job System.
- The milestone: `researchops jobs run` starts a worker that processes jobs from the queue. `researchops jobs list` shows job states.
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

Next week is Week 17: **RAG Assistant**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops ask "What is attention?"` returns a cited answer based on retrieved paper chunks.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `Job state machine: pending → running → done / failed` from user input to project result.
- Drill 2: Write one sentence defining `Job state machine: pending → running → done / failed` without copying the notes.
- Drill 3: Find the file where `Job state machine: pending → running → done / failed` appears or should appear.
- Drill 4: Name one wrong implementation of `Job state machine: pending → running → done / failed` and why it would hurt.
- Drill 5: Name one test that would protect `Job state machine: pending → running → done / failed`.
- Drill 6: Trace `Persistent job queue in SQLite` from user input to project result.
- Drill 7: Write one sentence defining `Persistent job queue in SQLite` without copying the notes.
- Drill 8: Find the file where `Persistent job queue in SQLite` appears or should appear.
- Drill 9: Name one wrong implementation of `Persistent job queue in SQLite` and why it would hurt.
- Drill 10: Name one test that would protect `Persistent job queue in SQLite`.
- Drill 11: Trace `Worker loop: poll → claim → execute → update state` from user input to project result.
- Drill 12: Write one sentence defining `Worker loop: poll → claim → execute → update state` without copying the notes.
- Drill 13: Find the file where `Worker loop: poll → claim → execute → update state` appears or should appear.
- Drill 14: Name one wrong implementation of `Worker loop: poll → claim → execute → update state` and why it would hurt.
- Drill 15: Name one test that would protect `Worker loop: poll → claim → execute → update state`.
- Drill 16: Trace `Retry logic and idempotency` from user input to project result.
- Drill 17: Write one sentence defining `Retry logic and idempotency` without copying the notes.
- Drill 18: Find the file where `Retry logic and idempotency` appears or should appear.
- Drill 19: Name one wrong implementation of `Retry logic and idempotency` and why it would hurt.
- Drill 20: Name one test that would protect `Retry logic and idempotency`.
- Drill 21: Trace `Worker failure recovery without data corruption` from user input to project result.
- Drill 22: Write one sentence defining `Worker failure recovery without data corruption` without copying the notes.
- Drill 23: Find the file where `Worker failure recovery without data corruption` appears or should appear.
- Drill 24: Name one wrong implementation of `Worker failure recovery without data corruption` and why it would hurt.
- Drill 25: Name one test that would protect `Worker failure recovery without data corruption`.
- Drill 26: Trace ``JobService` and `JobRepository`` from user input to project result.
- Drill 27: Write one sentence defining ``JobService` and `JobRepository`` without copying the notes.
- Drill 28: Find the file where ``JobService` and `JobRepository`` appears or should appear.
- Drill 29: Name one wrong implementation of ``JobService` and `JobRepository`` and why it would hurt.
- Drill 30: Name one test that would protect ``JobService` and `JobRepository``.
- Drill 31: Draw the Week 16 data flow in four boxes.
- Drill 32: Say why `Local Worker and Job System` belongs in this month of the curriculum.
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
- Drill 45: Trace `Job state machine: pending → running → done / failed` from user input to project result.
- Drill 46: Write one sentence defining `Job state machine: pending → running → done / failed` without copying the notes.
- Drill 47: Find the file where `Job state machine: pending → running → done / failed` appears or should appear.
- Drill 48: Name one wrong implementation of `Job state machine: pending → running → done / failed` and why it would hurt.
- Drill 49: Name one test that would protect `Job state machine: pending → running → done / failed`.
- Drill 50: Trace `Persistent job queue in SQLite` from user input to project result.
- Drill 51: Write one sentence defining `Persistent job queue in SQLite` without copying the notes.
- Drill 52: Find the file where `Persistent job queue in SQLite` appears or should appear.
- Drill 53: Name one wrong implementation of `Persistent job queue in SQLite` and why it would hurt.
- Drill 54: Name one test that would protect `Persistent job queue in SQLite`.
- Drill 55: Trace `Worker loop: poll → claim → execute → update state` from user input to project result.
- Drill 56: Write one sentence defining `Worker loop: poll → claim → execute → update state` without copying the notes.
- Drill 57: Find the file where `Worker loop: poll → claim → execute → update state` appears or should appear.
- Drill 58: Name one wrong implementation of `Worker loop: poll → claim → execute → update state` and why it would hurt.
- Drill 59: Name one test that would protect `Worker loop: poll → claim → execute → update state`.
- Drill 60: Trace `Retry logic and idempotency` from user input to project result.
- Drill 61: Write one sentence defining `Retry logic and idempotency` without copying the notes.
- Drill 62: Find the file where `Retry logic and idempotency` appears or should appear.
- Drill 63: Name one wrong implementation of `Retry logic and idempotency` and why it would hurt.
- Drill 64: Name one test that would protect `Retry logic and idempotency`.
- Drill 65: Trace `Worker failure recovery without data corruption` from user input to project result.
- Drill 66: Write one sentence defining `Worker failure recovery without data corruption` without copying the notes.
- Drill 67: Find the file where `Worker failure recovery without data corruption` appears or should appear.
- Drill 68: Name one wrong implementation of `Worker failure recovery without data corruption` and why it would hurt.
- Drill 69: Name one test that would protect `Worker failure recovery without data corruption`.
- Drill 70: Trace ``JobService` and `JobRepository`` from user input to project result.
- Drill 71: Write one sentence defining ``JobService` and `JobRepository`` without copying the notes.
- Drill 72: Find the file where ``JobService` and `JobRepository`` appears or should appear.
- Drill 73: Name one wrong implementation of ``JobService` and `JobRepository`` and why it would hurt.
- Drill 74: Name one test that would protect ``JobService` and `JobRepository``.
- Drill 75: Draw the Week 16 data flow in four boxes.
- Drill 76: Say why `Local Worker and Job System` belongs in this month of the curriculum.
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
- Drill 89: Trace `Job state machine: pending → running → done / failed` from user input to project result.
- Drill 90: Write one sentence defining `Job state machine: pending → running → done / failed` without copying the notes.
- Drill 91: Find the file where `Job state machine: pending → running → done / failed` appears or should appear.
- Drill 92: Name one wrong implementation of `Job state machine: pending → running → done / failed` and why it would hurt.
- Drill 93: Name one test that would protect `Job state machine: pending → running → done / failed`.
- Drill 94: Trace `Persistent job queue in SQLite` from user input to project result.
- Drill 95: Write one sentence defining `Persistent job queue in SQLite` without copying the notes.
- Drill 96: Find the file where `Persistent job queue in SQLite` appears or should appear.
- Drill 97: Name one wrong implementation of `Persistent job queue in SQLite` and why it would hurt.
- Drill 98: Name one test that would protect `Persistent job queue in SQLite`.
- Drill 99: Trace `Worker loop: poll → claim → execute → update state` from user input to project result.
- Drill 100: Write one sentence defining `Worker loop: poll → claim → execute → update state` without copying the notes.
- Drill 101: Find the file where `Worker loop: poll → claim → execute → update state` appears or should appear.
- Drill 102: Name one wrong implementation of `Worker loop: poll → claim → execute → update state` and why it would hurt.
- Drill 103: Name one test that would protect `Worker loop: poll → claim → execute → update state`.
- Drill 104: Trace `Retry logic and idempotency` from user input to project result.
- Drill 105: Write one sentence defining `Retry logic and idempotency` without copying the notes.
- Drill 106: Find the file where `Retry logic and idempotency` appears or should appear.
- Drill 107: Name one wrong implementation of `Retry logic and idempotency` and why it would hurt.
- Drill 108: Name one test that would protect `Retry logic and idempotency`.
- Drill 109: Trace `Worker failure recovery without data corruption` from user input to project result.
- Drill 110: Write one sentence defining `Worker failure recovery without data corruption` without copying the notes.
- Drill 111: Find the file where `Worker failure recovery without data corruption` appears or should appear.
- Drill 112: Name one wrong implementation of `Worker failure recovery without data corruption` and why it would hurt.
- Drill 113: Name one test that would protect `Worker failure recovery without data corruption`.
- Drill 114: Trace ``JobService` and `JobRepository`` from user input to project result.
- Drill 115: Write one sentence defining ``JobService` and `JobRepository`` without copying the notes.
- Drill 116: Find the file where ``JobService` and `JobRepository`` appears or should appear.
- Drill 117: Name one wrong implementation of ``JobService` and `JobRepository`` and why it would hurt.
- Drill 118: Name one test that would protect ``JobService` and `JobRepository``.
- Drill 119: Draw the Week 16 data flow in four boxes.
- Drill 120: Say why `Local Worker and Job System` belongs in this month of the curriculum.
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
- Drill 133: Trace `Job state machine: pending → running → done / failed` from user input to project result.
- Drill 134: Write one sentence defining `Job state machine: pending → running → done / failed` without copying the notes.
- Drill 135: Find the file where `Job state machine: pending → running → done / failed` appears or should appear.
- Drill 136: Name one wrong implementation of `Job state machine: pending → running → done / failed` and why it would hurt.
- Drill 137: Name one test that would protect `Job state machine: pending → running → done / failed`.
- Drill 138: Trace `Persistent job queue in SQLite` from user input to project result.
- Drill 139: Write one sentence defining `Persistent job queue in SQLite` without copying the notes.
- Drill 140: Find the file where `Persistent job queue in SQLite` appears or should appear.
- Drill 141: Name one wrong implementation of `Persistent job queue in SQLite` and why it would hurt.
- Drill 142: Name one test that would protect `Persistent job queue in SQLite`.
- Drill 143: Trace `Worker loop: poll → claim → execute → update state` from user input to project result.
- Drill 144: Write one sentence defining `Worker loop: poll → claim → execute → update state` without copying the notes.
- Drill 145: Find the file where `Worker loop: poll → claim → execute → update state` appears or should appear.
- Drill 146: Name one wrong implementation of `Worker loop: poll → claim → execute → update state` and why it would hurt.
- Drill 147: Name one test that would protect `Worker loop: poll → claim → execute → update state`.
- Drill 148: Trace `Retry logic and idempotency` from user input to project result.
- Drill 149: Write one sentence defining `Retry logic and idempotency` without copying the notes.
- Drill 150: Find the file where `Retry logic and idempotency` appears or should appear.
- Drill 151: Name one wrong implementation of `Retry logic and idempotency` and why it would hurt.
- Drill 152: Name one test that would protect `Retry logic and idempotency`.
- Drill 153: Trace `Worker failure recovery without data corruption` from user input to project result.
- Drill 154: Write one sentence defining `Worker failure recovery without data corruption` without copying the notes.
- Drill 155: Find the file where `Worker failure recovery without data corruption` appears or should appear.
- Drill 156: Name one wrong implementation of `Worker failure recovery without data corruption` and why it would hurt.
- Drill 157: Name one test that would protect `Worker failure recovery without data corruption`.
- Drill 158: Trace ``JobService` and `JobRepository`` from user input to project result.
- Drill 159: Write one sentence defining ``JobService` and `JobRepository`` without copying the notes.
- Drill 160: Find the file where ``JobService` and `JobRepository`` appears or should appear.
- Drill 161: Name one wrong implementation of ``JobService` and `JobRepository`` and why it would hurt.
- Drill 162: Name one test that would protect ``JobService` and `JobRepository``.
- Drill 163: Draw the Week 16 data flow in four boxes.
- Drill 164: Say why `Local Worker and Job System` belongs in this month of the curriculum.
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
- Drill 177: Trace `Job state machine: pending → running → done / failed` from user input to project result.
- Drill 178: Write one sentence defining `Job state machine: pending → running → done / failed` without copying the notes.
- Drill 179: Find the file where `Job state machine: pending → running → done / failed` appears or should appear.
- Drill 180: Name one wrong implementation of `Job state machine: pending → running → done / failed` and why it would hurt.
- Drill 181: Name one test that would protect `Job state machine: pending → running → done / failed`.
- Drill 182: Trace `Persistent job queue in SQLite` from user input to project result.
- Drill 183: Write one sentence defining `Persistent job queue in SQLite` without copying the notes.
- Drill 184: Find the file where `Persistent job queue in SQLite` appears or should appear.
- Drill 185: Name one wrong implementation of `Persistent job queue in SQLite` and why it would hurt.
- Drill 186: Name one test that would protect `Persistent job queue in SQLite`.
- Drill 187: Trace `Worker loop: poll → claim → execute → update state` from user input to project result.
- Drill 188: Write one sentence defining `Worker loop: poll → claim → execute → update state` without copying the notes.
- Drill 189: Find the file where `Worker loop: poll → claim → execute → update state` appears or should appear.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes
## Why long-running tasks need a job system

When a user triggers an action in a CLI or API, the response must come back quickly. A user waiting 30 seconds for a command to return is a bad experience. An API that keeps a request open for 5 minutes will time out.

But some tasks genuinely take a long time:
- Fetching 100 remote PDFs over HTTP
- Embedding 10 000 chunks with a local model
- Parsing a large batch of documents

The solution is to separate submission from execution. The user submits a job. The submission is instant. A background worker picks up the job and runs it later. The user can check the job status when they want.

This is the core idea behind job queues, task queues, and message brokers (Celery, SQS, RQ, Temporal). They all implement the same mental model, just at different scales. This week you build the same pattern locally with SQLite.

---

## Jobs, queues, and workers — from first principles

### A job

A job is a unit of deferred work. It has:

- **ID** — a unique identifier so you can look it up later.
- **Type** — what kind of work to do. For example, `"ingest_document"` or `"embed_chunk_batch"`.
- **Payload** — the data the handler needs. Stored as JSON.
- **Status** — where the job is in its lifecycle.
- **Attempts** — how many times it has been tried.
- **Last error** — what went wrong on the most recent failure.
- **Timestamps** — when it was created and last updated.

### A queue

A queue is a storage layer for jobs. Its responsibilities:
- Accept new jobs (enqueue).
- Hand the next job to a worker (dequeue/claim).
- Update job status.
- Report job counts by status.

### A worker

A worker is a loop that repeatedly:
1. Asks the queue for the next available job.
2. Marks it as running.
3. Calls the appropriate handler for that job type.
4. Marks it as succeeded or failed.
5. Waits briefly (polling) before checking again.

---

## The SQLite job table

Storing jobs in SQLite is enough for local development and small-scale production. Here is the schema:

```sql
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

Line by line:

`id TEXT PRIMARY KEY` — each job gets a unique identifier, typically a UUID. Using `TEXT` instead of `INTEGER` avoids coordination problems if you ever run multiple inserters.

`job_type TEXT NOT NULL` — a string name for the job type. The worker uses this to look up the right handler. Examples: `"fetch_url"`, `"index_document"`, `"send_summary_email"`.

`status TEXT NOT NULL` — the current lifecycle state. Must be one of a fixed set of values (enforced in application code or via a CHECK constraint).

`payload_json TEXT NOT NULL` — the job's input data, JSON-serialised. Python dict → `json.dumps()` on insert, `json.loads()` on read. Storing as TEXT keeps the schema simple and portable.

`attempts INTEGER NOT NULL DEFAULT 0` — how many times execution has been attempted. Incremented each time the worker tries the job. Used by retry logic to decide when to give up.

`last_error TEXT` — nullable. Contains the error message (or stack trace excerpt) from the most recent failure. Invaluable for debugging.

`created_at TEXT NOT NULL` — ISO 8601 timestamp when the job was inserted. Example: `"2026-06-09T10:30:00Z"`.

`updated_at TEXT NOT NULL` — ISO 8601 timestamp of the most recent status change. Useful for detecting stuck jobs.

---

## Job status lifecycle

```
PENDING → RUNNING → SUCCEEDED
                  ↘ FAILED → RETRIED → RUNNING → ...
                                     ↘ FAILED (permanently)
```

**PENDING** (also called QUEUED): job has been submitted and is waiting for a worker.

**RUNNING**: a worker has claimed the job and is executing it.

**SUCCEEDED**: the handler completed without exception.

**FAILED**: the handler raised an exception. If `attempts < max_attempts`, the status may move back to PENDING for a retry.

**RETRIED**: a transient state indicating the job will be re-queued. Some systems skip this and move directly back to PENDING.

Status transitions must be explicit. Never update the status outside the queue layer. This ensures consistency and makes the transitions testable.

---

## The worker polling loop

The worker is a loop. Here is pseudo-code with full explanation:

```python
def run_worker(queue: JobQueue, handlers: dict, max_attempts: int = 3) -> None:
    while True:                                          # (1)
        job = queue.claim_next_pending()                 # (2)
        if job is None:                                  # (3)
            time.sleep(1)                               # (4)
            continue                                    # (5)
        queue.mark_running(job.id)                      # (6)
        try:
            handler = handlers[job.job_type]            # (7)
            payload = json.loads(job.payload_json)      # (8)
            handler(payload)                            # (9)
            queue.mark_succeeded(job.id)                # (10)
        except KeyError:                                # (11)
            queue.mark_failed(job.id, "unknown job type")  # (12)
        except Exception as exc:                        # (13)
            new_attempts = job.attempts + 1             # (14)
            if new_attempts < max_attempts:             # (15)
                queue.requeue(job.id, str(exc))         # (16)
            else:
                queue.mark_failed(job.id, str(exc))     # (17)
```

(1) Loop forever. A real worker runs until stopped by a signal.

(2) Ask the queue for the next PENDING job. This should be atomic (SELECT + UPDATE in a single transaction) so two workers cannot claim the same job.

(3) If no job is available, the queue is empty.

(4) Sleep briefly before polling again. Without this, the worker hammers the database with queries when idle.

(5) `continue` skips the rest of the loop body and polls again.

(6) Mark the job as RUNNING before executing. If the worker crashes after this, the job stays RUNNING indefinitely — this is a "stuck job". Production systems detect stuck jobs by checking `updated_at`.

(7) Look up the handler function for this job type. Raises `KeyError` if unknown.

(8) Deserialise the JSON payload into a Python dict.

(9) Execute the handler. This is where the real work happens: fetching, parsing, indexing.

(10) If the handler returns without raising, mark the job SUCCEEDED.

(11) Unknown job type — no handler registered.

(12) Mark failed with a descriptive error. Do not retry unknown types.

(13) Any other exception — a real failure.

(14) Increment the attempt count.

(15) Check whether we have more attempts remaining.

(16) `requeue` increments `attempts`, stores the error in `last_error`, and sets status back to PENDING. The job will be picked up again.

(17) Exceeded retry limit. Mark permanently failed.

---

## Idempotency

Idempotency means: running the same operation more than once produces the same result as running it once.

Why it matters for jobs: if a worker crashes after completing the work but before marking the job SUCCEEDED, the job will be retried. The handler runs again. If the handler is not idempotent, it may create duplicate records, send duplicate emails, or corrupt state.

**Non-idempotent (dangerous):**
```python
def handle_index_document(payload: dict) -> None:
    doc = parse(payload["text"])
    db.insert_document(doc)   # will fail or duplicate if called twice
```

**Idempotent (safe):**
```python
def handle_index_document(payload: dict) -> None:
    doc = parse(payload["text"])
    db.upsert_document(doc)   # insert or update, safe to call twice
```

Use `INSERT OR REPLACE` or `INSERT ... ON CONFLICT DO UPDATE` in SQLite for idempotent inserts.

Alternatively, check first:
```python
if not db.document_exists(doc.id):
    db.insert_document(doc)
```

A simpler approach: store the document's content hash in the job payload. Before inserting, check if a document with that hash already exists. If yes, skip the insert.

---

## Poison jobs

A poison job is a job that consistently fails, exhausts its retry limit, and stays in FAILED state permanently. Left unchecked, poison jobs accumulate and pollute your job table.

Handling poison jobs:
1. Set a clear `max_attempts` limit (e.g., 3).
2. Store the full error in `last_error` for diagnosis.
3. Provide a CLI command to list and inspect FAILED jobs.
4. Allow manual re-queuing after a human investigates and fixes the root cause.
5. Optionally, move permanently-failed jobs to a dead-letter table for archival.

---

## Why workers call services, not raw storage

A worker's handler should call the application service layer, not query the database directly.

**Wrong:**
```python
def handle_embed(payload: dict) -> None:
    conn = sqlite3.connect("data.db")
    chunks = conn.execute("SELECT ...").fetchall()
    # embed and insert directly
```

**Right:**
```python
def handle_embed(payload: dict) -> None:
    service = build_embedding_service()
    service.embed_document(payload["document_id"])
```

This keeps the worker as a thin dispatcher, just like route handlers. The service layer contains business logic. The worker just orchestrates: claim job, call service, update status.

---

## API + worker: the standard pattern

A common production pattern:

1. User sends `POST /jobs/ingest` with a document URL.
2. The API creates a PENDING job in the database and returns `{"job_id": "abc123"}` with `201 Created`.
3. The background worker polls, finds the job, and fetches and indexes the document.
4. The user polls `GET /jobs/abc123` and eventually sees `{"status": "succeeded"}`.

The API is never blocked waiting for the document to be indexed. The user gets instant feedback. The worker does the real work asynchronously.

This pattern prepares you for production: replicate the worker, use a proper queue (Redis, SQS), and the architecture scales horizontally.

---

## Testing a job system

Unit tests should focus on state transitions:

```python
def test_successful_job() -> None:
    queue = InMemoryJobQueue()
    job_id = queue.enqueue("noop", {"value": 1})
    assert queue.get_status(job_id) == "pending"
    
    run_worker_once(queue, handlers={"noop": lambda p: None})
    
    assert queue.get_status(job_id) == "succeeded"


def test_failed_job_retries() -> None:
    queue = InMemoryJobQueue()
    job_id = queue.enqueue("fail", {})

    def always_fail(payload: dict) -> None:
        raise RuntimeError("boom")

    run_worker_once(queue, handlers={"fail": always_fail})
    assert queue.get_status(job_id) == "pending"  # re-queued for retry
    assert queue.get_attempts(job_id) == 1
```

Use an in-memory queue implementation for unit tests. This avoids the database and keeps tests fast. The in-memory implementation should satisfy the same interface as the SQLite-backed queue.

---

## Summary

- Long-running work should not block the API or CLI — use a job system.
- A job has ID, type, status, payload, attempts, error, and timestamps.
- The SQLite schema stores everything needed to run, retry, and inspect jobs.
- Status transitions are explicit: PENDING → RUNNING → SUCCEEDED or FAILED.
- The worker polling loop claims, executes, and updates status.
- Polling with a small sleep prevents wasted database queries when idle.
- Idempotency means handlers are safe to run more than once.
- Use upsert logic or existence checks to make handlers idempotent.
- Poison jobs exhaust retries; store the error and provide manual inspection tools.
- Workers call services, not raw storage — the same rule as route handlers.
- The API + worker pattern is the standard production model for async work.
- Test with an in-memory queue for fast, isolated state-transition tests.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 16 — Local Worker Job System:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 4: AI Engineering, API, Workers](../README.md)
---
<!-- NAV_BOTTOM_END -->
