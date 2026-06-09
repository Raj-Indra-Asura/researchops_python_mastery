<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 20 — Final Hardening and v1 Release:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Week 20 Notes: Final Hardening and v1.0 Release

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 20: Final Hardening and v1.0 Release

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Finishing is a skill**.
The practical milestone is: `v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.
The expected capability is: Can apply semantic versioning, write a changelog, create a git tag, and explain what v1.0 means for a software project.
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

- Week 16 taught Local Worker and Job System; keep its responsibility in mind, but do not rebuild it here.
- Week 17 taught RAG Assistant; keep its responsibility in mind, but do not rebuild it here.
- Week 18 taught Docker and Environment Configuration; keep its responsibility in mind, but do not rebuild it here.
- Week 19 taught Documentation and Portfolio Polish; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 20 solves the project problem behind **Final Hardening and v1.0 Release**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` helps solve part of this gap.
- The concept `Release checklist discipline: scope control, no new features before release` helps solve part of this gap.
- The concept `Changelog writing: what changed, for whom, and why` helps solve part of this gap.
- The concept `Git tagging: `git tag -a v1.0.0 -m "..."`` helps solve part of this gap.
- The concept `Final retrospective: 20 weeks in review` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Final Hardening and v1.0 Release**?
- Ask: what is the owner for **Final Hardening and v1.0 Release**?
- Ask: what is the transformation for **Final Hardening and v1.0 Release**?
- Ask: what is the proof for **Final Hardening and v1.0 Release**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| Semantic versioning | Semantic versioning: MAJOR.MINOR.PATCH and what each number means | This term names one job in the Week 20 milestone. |
| Release checklist discipline | Release checklist discipline: scope control, no new features before release | This term names one job in the Week 20 milestone. |
| Changelog writing | Changelog writing: what changed, for whom, and why | This term names one job in the Week 20 milestone. |
| Git tagging | Git tagging: `git tag -a v1.0.0 -m "..."` | This term names one job in the Week 20 milestone. |
| Final retrospective | Final retrospective: 20 weeks in review | This term names one job in the Week 20 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: Semantic versioning: MAJOR.MINOR.PATCH and what each number means
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 20, it supports the milestone: `v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Release checklist discipline: scope control, no new features before release
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 20, it supports the milestone: `v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: Changelog writing: what changed, for whom, and why
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 20, it supports the milestone: `v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Git tagging: `git tag -a v1.0.0 -m "..."`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 20, it supports the milestone: `v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Final retrospective: 20 weeks in review
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 20, it supports the milestone: `v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `CHANGELOG.md` — complete version history
- `ROADMAP.md` — all weeks marked ✅
- `pyproject.toml` — version bumped to `1.0.0`
- `src/researchops/__init__.py` — `__version__ = "1.0.0"`
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
def is_major_release(version: str) -> bool:
    major, minor, patch = version.split(".")
    return int(major) >= 1 and int(minor) == 0 and int(patch) == 0
```

Line-by-line explanation:
- Line 1: `def is_major_release(version: str) -> bool:` — This names a reusable action and shows what information it receives.
- Line 2: `major, minor, patch = version.split(".")` — This stores a clear intermediate value for the next step.
- Line 3: `return int(major) >= 1 and int(minor) == 0 and int(patch) == 0` — This produces the result or performs the declared setup step.

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
- All existing tests pass (no regressions introduced)
- End-to-end: `researchops --help`, full pipeline commands
Validation commands:
```bash
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
researchops --help
git tag v1.0.0
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
Week 20 contributes by making **final hardening and v1.0 release** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 20 solve?
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

- Explain Final Hardening and v1.0 Release in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Final Hardening and v1.0 Release.
- The milestone: `v1.0.0` is tagged. CI is green. Every ROADMAP.md row is ✅. A demo exists. The project is portfolio-ready.
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

This is the final week, so the bridge is into maintenance, presentation, and responsible extension after v1.0.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` from user input to project result.
- Drill 2: Write one sentence defining `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` without copying the notes.
- Drill 3: Find the file where `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` appears or should appear.
- Drill 4: Name one wrong implementation of `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` and why it would hurt.
- Drill 5: Name one test that would protect `Semantic versioning: MAJOR.MINOR.PATCH and what each number means`.
- Drill 6: Trace `Release checklist discipline: scope control, no new features before release` from user input to project result.
- Drill 7: Write one sentence defining `Release checklist discipline: scope control, no new features before release` without copying the notes.
- Drill 8: Find the file where `Release checklist discipline: scope control, no new features before release` appears or should appear.
- Drill 9: Name one wrong implementation of `Release checklist discipline: scope control, no new features before release` and why it would hurt.
- Drill 10: Name one test that would protect `Release checklist discipline: scope control, no new features before release`.
- Drill 11: Trace `Changelog writing: what changed, for whom, and why` from user input to project result.
- Drill 12: Write one sentence defining `Changelog writing: what changed, for whom, and why` without copying the notes.
- Drill 13: Find the file where `Changelog writing: what changed, for whom, and why` appears or should appear.
- Drill 14: Name one wrong implementation of `Changelog writing: what changed, for whom, and why` and why it would hurt.
- Drill 15: Name one test that would protect `Changelog writing: what changed, for whom, and why`.
- Drill 16: Trace `Git tagging: `git tag -a v1.0.0 -m "..."`` from user input to project result.
- Drill 17: Write one sentence defining `Git tagging: `git tag -a v1.0.0 -m "..."`` without copying the notes.
- Drill 18: Find the file where `Git tagging: `git tag -a v1.0.0 -m "..."`` appears or should appear.
- Drill 19: Name one wrong implementation of `Git tagging: `git tag -a v1.0.0 -m "..."`` and why it would hurt.
- Drill 20: Name one test that would protect `Git tagging: `git tag -a v1.0.0 -m "..."``.
- Drill 21: Trace `Final retrospective: 20 weeks in review` from user input to project result.
- Drill 22: Write one sentence defining `Final retrospective: 20 weeks in review` without copying the notes.
- Drill 23: Find the file where `Final retrospective: 20 weeks in review` appears or should appear.
- Drill 24: Name one wrong implementation of `Final retrospective: 20 weeks in review` and why it would hurt.
- Drill 25: Name one test that would protect `Final retrospective: 20 weeks in review`.
- Drill 26: Draw the Week 20 data flow in four boxes.
- Drill 27: Say why `Final Hardening and v1.0 Release` belongs in this month of the curriculum.
- Drill 28: Rewrite one error message in beginner-friendly language.
- Drill 29: List the exact assumptions made by the example code.
- Drill 30: List the exact assumptions checked by the tests.
- Drill 31: Point to the line where raw input becomes project meaning.
- Drill 32: Point to the line where the result becomes visible to a user.
- Drill 33: Explain what would happen if the main file were deleted.
- Drill 34: Explain what would happen if the main test were deleted.
- Drill 35: Describe the smallest manual check you can run.
- Drill 36: Describe the smallest automated check you can run.
- Drill 37: Name the most likely beginner mistake for this week.
- Drill 38: Name the safest recovery move for that mistake.
- Drill 39: Explain what knowledge should be carried into the next chapter.
- Drill 40: Trace `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` from user input to project result.
- Drill 41: Write one sentence defining `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` without copying the notes.
- Drill 42: Find the file where `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` appears or should appear.
- Drill 43: Name one wrong implementation of `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` and why it would hurt.
- Drill 44: Name one test that would protect `Semantic versioning: MAJOR.MINOR.PATCH and what each number means`.
- Drill 45: Trace `Release checklist discipline: scope control, no new features before release` from user input to project result.
- Drill 46: Write one sentence defining `Release checklist discipline: scope control, no new features before release` without copying the notes.
- Drill 47: Find the file where `Release checklist discipline: scope control, no new features before release` appears or should appear.
- Drill 48: Name one wrong implementation of `Release checklist discipline: scope control, no new features before release` and why it would hurt.
- Drill 49: Name one test that would protect `Release checklist discipline: scope control, no new features before release`.
- Drill 50: Trace `Changelog writing: what changed, for whom, and why` from user input to project result.
- Drill 51: Write one sentence defining `Changelog writing: what changed, for whom, and why` without copying the notes.
- Drill 52: Find the file where `Changelog writing: what changed, for whom, and why` appears or should appear.
- Drill 53: Name one wrong implementation of `Changelog writing: what changed, for whom, and why` and why it would hurt.
- Drill 54: Name one test that would protect `Changelog writing: what changed, for whom, and why`.
- Drill 55: Trace `Git tagging: `git tag -a v1.0.0 -m "..."`` from user input to project result.
- Drill 56: Write one sentence defining `Git tagging: `git tag -a v1.0.0 -m "..."`` without copying the notes.
- Drill 57: Find the file where `Git tagging: `git tag -a v1.0.0 -m "..."`` appears or should appear.
- Drill 58: Name one wrong implementation of `Git tagging: `git tag -a v1.0.0 -m "..."`` and why it would hurt.
- Drill 59: Name one test that would protect `Git tagging: `git tag -a v1.0.0 -m "..."``.
- Drill 60: Trace `Final retrospective: 20 weeks in review` from user input to project result.
- Drill 61: Write one sentence defining `Final retrospective: 20 weeks in review` without copying the notes.
- Drill 62: Find the file where `Final retrospective: 20 weeks in review` appears or should appear.
- Drill 63: Name one wrong implementation of `Final retrospective: 20 weeks in review` and why it would hurt.
- Drill 64: Name one test that would protect `Final retrospective: 20 weeks in review`.
- Drill 65: Draw the Week 20 data flow in four boxes.
- Drill 66: Say why `Final Hardening and v1.0 Release` belongs in this month of the curriculum.
- Drill 67: Rewrite one error message in beginner-friendly language.
- Drill 68: List the exact assumptions made by the example code.
- Drill 69: List the exact assumptions checked by the tests.
- Drill 70: Point to the line where raw input becomes project meaning.
- Drill 71: Point to the line where the result becomes visible to a user.
- Drill 72: Explain what would happen if the main file were deleted.
- Drill 73: Explain what would happen if the main test were deleted.
- Drill 74: Describe the smallest manual check you can run.
- Drill 75: Describe the smallest automated check you can run.
- Drill 76: Name the most likely beginner mistake for this week.
- Drill 77: Name the safest recovery move for that mistake.
- Drill 78: Explain what knowledge should be carried into the next chapter.
- Drill 79: Trace `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` from user input to project result.
- Drill 80: Write one sentence defining `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` without copying the notes.
- Drill 81: Find the file where `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` appears or should appear.
- Drill 82: Name one wrong implementation of `Semantic versioning: MAJOR.MINOR.PATCH and what each number means` and why it would hurt.
- Drill 83: Name one test that would protect `Semantic versioning: MAJOR.MINOR.PATCH and what each number means`.
- Drill 84: Trace `Release checklist discipline: scope control, no new features before release` from user input to project result.
- Drill 85: Write one sentence defining `Release checklist discipline: scope control, no new features before release` without copying the notes.
- Drill 86: Find the file where `Release checklist discipline: scope control, no new features before release` appears or should appear.
- Drill 87: Name one wrong implementation of `Release checklist discipline: scope control, no new features before release` and why it would hurt.
- Drill 88: Name one test that would protect `Release checklist discipline: scope control, no new features before release`.
- Drill 89: Trace `Changelog writing: what changed, for whom, and why` from user input to project result.
- Drill 90: Write one sentence defining `Changelog writing: what changed, for whom, and why` without copying the notes.
- Drill 91: Find the file where `Changelog writing: what changed, for whom, and why` appears or should appear.
- Drill 92: Name one wrong implementation of `Changelog writing: what changed, for whom, and why` and why it would hurt.
- Drill 93: Name one test that would protect `Changelog writing: what changed, for whom, and why`.
- Drill 94: Trace `Git tagging: `git tag -a v1.0.0 -m "..."`` from user input to project result.
- Drill 95: Write one sentence defining `Git tagging: `git tag -a v1.0.0 -m "..."`` without copying the notes.
- Drill 96: Find the file where `Git tagging: `git tag -a v1.0.0 -m "..."`` appears or should appear.
- Drill 97: Name one wrong implementation of `Git tagging: `git tag -a v1.0.0 -m "..."`` and why it would hurt.
- Drill 98: Name one test that would protect `Git tagging: `git tag -a v1.0.0 -m "..."``.
- Drill 99: Trace `Final retrospective: 20 weeks in review` from user input to project result.
- Drill 100: Write one sentence defining `Final retrospective: 20 weeks in review` without copying the notes.
- Drill 101: Find the file where `Final retrospective: 20 weeks in review` appears or should appear.
- Drill 102: Name one wrong implementation of `Final retrospective: 20 weeks in review` and why it would hurt.
- Drill 103: Name one test that would protect `Final retrospective: 20 weeks in review`.
- Drill 104: Draw the Week 20 data flow in four boxes.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes
## What "done" actually means

There is no perfect software. "Done" for a v1.0 release means:

1. The stated requirements are met.
2. The tests pass.
3. The documentation is accurate.
4. The project can be demonstrated end-to-end.
5. You can talk about it confidently.

None of these say "all possible features are built" or "all edge cases are handled". Software is never complete. "Done" is a decision, not a state.

The most common failure mode for side projects is **infinite polish**. This is the loop where you never release because there is always one more thing to fix or add. Breaking this loop requires explicitly deciding that the current state is version 1.0 and committing to that decision.

The discipline of finishing is as important as the discipline of building. Employers care whether you can ship, not just whether you can code.

---

## Why not to add features forever

Every new feature added to an unreleased project:
- Increases the scope of what must be tested before release.
- Introduces new bugs that delay release further.
- Makes the codebase harder to understand in an interview.
- Dilutes your portfolio story (if it does five things adequately, it does none of them memorably).

The right time to stop adding features to v1.0 is when the core feature set is complete and working. All future features belong in v1.1 or later.

Before finalising v1.0, write down everything you want to add. Then move every item to a `ROADMAP.md` entry labelled v1.1 or later. This is not giving up. It is scope management, which is a professional skill.

---

## Release

A **release** is a named, versioned snapshot of your software that has been tested and documented. It is a statement: "This version, at this point in time, is intentionally made available."

For an open-source project on GitHub, a release consists of:
1. A version number (e.g., `1.0.0`).
2. A git tag pointing to the release commit.
3. A GitHub Release (on the Releases page) with release notes.
4. An updated changelog.

The act of creating a release forces you to:
- Verify the version number is correct everywhere.
- Write release notes that explain what changed.
- Confirm the tests pass one final time.
- Make a public statement that this version works.

---

## Version

A **version number** is a label that identifies a specific state of the software. The standard format is `MAJOR.MINOR.PATCH`, known as **semantic versioning** (SemVer).

- **MAJOR**: incremented when you make a breaking change. Existing users must update their code to use the new version.
- **MINOR**: incremented when you add new functionality in a backward-compatible way. Existing users do not need to change anything.
- **PATCH**: incremented when you fix bugs without adding new functionality. Always backward-compatible.

For v1.0.0:
- This is the first intentional public release.
- There is no previous version to break compatibility with.
- All previous versions were development versions (0.x.x).

Version numbers must be consistent across three places:
1. `pyproject.toml`: `version = "1.0.0"`
2. `src/researchops/__init__.py`: `__version__ = "1.0.0"`
3. `CHANGELOG.md`: `[1.0.0] — YYYY-MM-DD`

If any of these are out of sync, the release is incomplete.

---

## Changelog

A **changelog** is a human-readable file that lists what changed between versions. It is written for users, not for Git.

The standard format (keepachangelog.com):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.0] — 2026-06-09

### Added
- RAG assistant with grounded Q&A and citations (Week 17)
- Docker packaging and environment configuration (Week 18)
- Complete documentation and portfolio polish (Week 19)
- v1.0.0 release with pre-release checklist (Week 20)

### Changed
- Settings module refactored to use pydantic-settings

### Fixed
- Vector index returns insufficient-evidence response when no relevant chunks found

## [0.9.0] — 2026-05-12

### Added
- FastAPI REST layer (Week 14)
- Async ingestion pipeline (Week 15)
- Background job runner (Week 16)
```

The changelog should not duplicate commit messages. Commit messages are for developers. The changelog is for users. Describe what changed from the user's perspective, not how you implemented it.

---

## Release notes

**Release notes** are a summary of the changes in a specific release, written for the GitHub Releases page. They are shorter than the full changelog and focus on the most important changes.

Template:

```markdown
## ResearchOps v1.0.0

This is the first production-ready release of ResearchOps.

### What's included

- **RAG assistant**: ask questions about your research papers and receive
  grounded answers with citations.
- **Docker packaging**: run the app, API, and worker in containers with
  docker compose.
- **Complete documentation**: README, architecture diagrams, demo script,
  and retrospective.

### How to install

\```bash
pip install researchops==1.0.0
\```

Or clone the repository:

\```bash
git clone https://github.com/YOUR_USERNAME/researchops_python_mastery.git
cd researchops_python_mastery
pip install -e ".[all]"
\```

### Known limitations

See README.md for the full list of known limitations.
```

---

## Regression testing

A **regression** is a bug that was fixed in a previous version but reappears in a later version. The name comes from the idea of going backward (regressing) in quality.

**Regression testing** is running the full test suite before a release to ensure that previously working behaviour still works.

For v1.0.0, run:

```bash
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
```

If any test fails that was passing before, that is a regression. Fix it before releasing. Do not adjust the tests to make them pass if the underlying code is wrong.

The purpose of the test suite is exactly this moment: to give you confidence that v1.0.0 works. If you have been maintaining tests throughout Weeks 1–20, this step is fast and reassuring.

---

## Final validation

Final validation is a structured, manual walkthrough of every major feature. It is not a substitute for automated tests, but a complement. Automated tests catch regressions; manual validation catches integration issues that are hard to automate.

Final validation flow for ResearchOps:

```
1. Start from a fresh clone (no .venv, no data/).
2. pip install -e ".[all]"
3. researchops --help                        → shows all commands
4. researchops ingest ./examples/sample_papers → ingests 3 papers
5. researchops search "attention mechanism"  → returns ranked results
6. researchops ask "what is attention?"      → returns answer with citations
7. uvicorn researchops.api.main:app &        → API starts
8. curl http://localhost:8000/papers         → returns paper list
9. docker build -t researchops:local .       → image builds
10. docker compose up api -d                 → API starts in container
11. curl http://localhost:8000/papers        → returns paper list
12. docker compose down                      → containers stop cleanly
```

Each step has an expected result. If any step fails, fix the code or documentation before tagging the release.

---

## Known limitations section

Write a `## Known Limitations` section in the README. This is mandatory for a production-grade project. Not because it makes the project look bad, but because:

1. It shows engineering maturity. Engineers who know their system's limits are trustworthy.
2. It prevents users from hitting a surprise failure that was known.
3. It gives you a clear v1.1 roadmap.

Known limitations for ResearchOps v1.0.0 (adapt to your actual state):

- In-memory vector index not persisted: rebuilds on every start.
- No authentication on the API.
- PDF parsing may fail on scanned or complex-layout PDFs.
- Single-user: concurrent writes to SQLite may produce errors.
- Fake generator is the default: real generation requires Ollama or an API key.

---

## Future roadmap

The roadmap distinguishes what you committed to in v1.0.0 from what you plan for future versions. A `ROADMAP.md` file in the repository root should list:

- ✅ Completed features (with week references)
- 🔜 v1.1 planned features
- 💡 v2.0 ideas (speculative)

Example v1.1 roadmap items:
- Persist vector index to SQLite
- Streaming API endpoint for RAG responses
- Hybrid search (keyword + semantic) with score fusion
- Authentication layer for the API
- OpenAI-compatible provider configuration

---

## Retrospective

A **retrospective** is a structured reflection on a completed project. It is not a performance review. It is a learning exercise.

Five honest questions:

1. **What did I build?** Be specific. List every major feature that actually works.

2. **What did I learn that I did not expect to learn?** This is usually something about tradeoffs, not about syntax.

3. **What would I do differently?** Pick one real thing. The best retrospectives are uncomfortable.

4. **What was hardest?** Not what was most complex, but what cost you the most time or caused the most doubt.

5. **What am I most proud of?** At least one thing should make you proud. If nothing does, the retrospective is not done.

6. **What would v1.1 look like?** What would you build next?

The retrospective in `docs/retrospective.md` is for you. Write it honestly. You will read it again in six months and be glad you did.

---

## Portfolio handoff

After tagging v1.0.0, the project is portfolio-ready. To hand it off to your portfolio:

1. **Pin the repository** on your GitHub profile.
2. **Update your LinkedIn** with a description of the project and a link.
3. **Add it to your CV/resume** in the Projects section with a one-sentence description and a link.
4. **Prepare the demo** from `docs/demo.md`. Practice it until it takes under two minutes.
5. **Prepare the verbal story** (two to three minutes): problem, solution, what you learned.

When someone asks "walk me through your portfolio", ResearchOps should be the first thing you mention. You have 20 weeks of work behind it. You can answer every technical question about it. You built every part of it yourself. That is rare and valuable.

---

## How to decide if the project is done

Use this decision tree before tagging:

```
Does pytest pass with 0 failures?
  No → Fix failing tests first.
  Yes → continue.

Does ruff check src tests pass with 0 errors?
  No → Fix lint errors first.
  Yes → continue.

Does the demo script in docs/demo.md run end-to-end without errors?
  No → Fix the broken commands or update the expected output.
  Yes → continue.

Is the README accurate for the current state of the code?
  No → Update the README.
  Yes → continue.

Is the CHANGELOG up to date with a [1.0.0] section?
  No → Write the changelog entry.
  Yes → continue.

Is the version number 1.0.0 in pyproject.toml and __init__.py?
  No → Bump the version.
  Yes → continue.

TAG THE RELEASE.
```

If you complete this checklist and everything passes, the project is done. Do not add more features. Tag the release.

---

## Release checklist (copy to use)

Copy this checklist to your final commit message or a temporary file:

```
Code quality:
[ ] pytest passes: 0 failures, 0 errors
[ ] ruff check src tests: 0 errors
[ ] No hard-coded paths or credentials in source
[ ] No .env file committed

Functionality:
[ ] researchops --help works
[ ] researchops ingest ./examples/sample_papers works
[ ] researchops search "query" works
[ ] researchops ask "question" works
[ ] FastAPI server starts and responds
[ ] Docker image builds

Documentation:
[ ] README is accurate for the current code
[ ] Quick Start section works from a fresh clone
[ ] ARCHITECTURE.md matches current code
[ ] docs/demo.md produces correct output
[ ] Known limitations section is present and honest
[ ] Future work section is present

Release:
[ ] Version is 1.0.0 in pyproject.toml
[ ] Version is 1.0.0 in src/researchops/__init__.py
[ ] CHANGELOG.md has [1.0.0] section with today's date
[ ] git tag -a v1.0.0 -m "ResearchOps v1.0.0" created
[ ] git push --tags completed
[ ] GitHub Release created with release notes
```

---

## How to create a git release tag

```bash
# Commit all changes
git add .
git commit -m "v1.0.0: final release"

# Create an annotated tag
git tag -a v1.0.0 -m "ResearchOps v1.0.0 — 20-week build complete"

# Push the tag to GitHub
git push origin v1.0.0

# On GitHub: go to Releases → Draft a new release → choose tag v1.0.0
# Fill in the title and release notes from the template above
# Click "Publish release"
```

An **annotated tag** (created with `-a`) stores metadata: the tagger, the date, and a message. It is different from a lightweight tag (created with just `git tag v1.0.0`). For releases, always use annotated tags.

---

## What to say in a portfolio interview

**When asked "tell me about this project"**:

Open with the problem, not the technology. "I built a tool that lets researchers search and ask questions about their paper collections using retrieval-augmented generation." Then describe the pipeline briefly. Then mention one specific technical decision you made and why.

**When asked "how does the RAG pipeline work"**:

Walk through the 7 steps. Use the diagram. Emphasise that retrieval quality determines answer quality. Mention the fake generator and why it was the right choice for tests.

**When asked "what would you improve"**:

Use your known limitations list. Choose one that demonstrates systems thinking, not just more features. "I would persist the vector index to SQLite so users do not have to re-index on every startup. The challenge is updating specific chunks without invalidating the whole index."

**When asked "how did you ensure quality"**:

"I wrote unit tests for each component using dependency injection and fakes, so tests run in milliseconds without external dependencies. I added a CI pipeline that runs ruff and pytest on every push. Before the v1.0 release, I ran a final validation checklist end-to-end from a fresh clone."

**When asked "how long did this take"**:

"Twenty weeks, roughly five to ten hours per week. Each week built on the previous one: storage before search, search before RAG, RAG before packaging. The structured progression helped because I was never building on an unstable foundation."

---

## Summary

- "Done" is a decision, not a state. Make it explicitly.
- Infinite polish is the enemy of shipping. List future features in the roadmap and leave them there.
- A release is a named, tested, documented snapshot. v1.0.0 is the first public commitment.
- Semantic versioning: MAJOR breaks, MINOR adds, PATCH fixes.
- A changelog is for users. Commit messages are for developers.
- Regression testing is running the full test suite before tagging.
- Final validation is a manual end-to-end walkthrough from a fresh clone.
- Known limitations demonstrate engineering maturity, not weakness.
- A retrospective is a gift to future you.
- Portfolio handoff requires: a working demo, a verbal story, and confidence.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 20 — Final Hardening and v1 Release:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
