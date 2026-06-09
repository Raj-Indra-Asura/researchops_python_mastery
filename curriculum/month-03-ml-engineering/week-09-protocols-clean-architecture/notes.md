<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 09 Protocols and Clean Architecture

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 09: Protocols, Interfaces, and Clean Architecture

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Depending on shapes, not implementations**.
The practical milestone is: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
The expected capability is: Can define a Protocol, implement it in both a real class and a test fake, and explain why services should depend on interfaces rather than concrete implementations.
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

- Week 5 taught SQLite Storage Layer; keep its responsibility in mind, but do not rebuild it here.
- Week 6 taught PDF Parsing Pipeline; keep its responsibility in mind, but do not rebuild it here.
- Week 7 taught Keyword Search and Data Quality; keep its responsibility in mind, but do not rebuild it here.
- Week 8 taught Multiprocessing Ingestion; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 9 solves the project problem behind **Protocols, Interfaces, and Clean Architecture**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept ``typing.Protocol` and structural subtyping` helps solve part of this gap.
- The concept ``@runtime_checkable` and `isinstance` checks` helps solve part of this gap.
- The concept `Dependency inversion principle` helps solve part of this gap.
- The concept `Import boundary rules: services import protocols, not concrete classes` helps solve part of this gap.
- The concept `Detecting import violations with `grep` or `import-linter`` helps solve part of this gap.
- The concept `Fake repositories implementing core protocols` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **Protocols, Interfaces, and Clean Architecture**?
- Ask: what is the owner for **Protocols, Interfaces, and Clean Architecture**?
- Ask: what is the transformation for **Protocols, Interfaces, and Clean Architecture**?
- Ask: what is the proof for **Protocols, Interfaces, and Clean Architecture**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| typing.Protocol` and structural subtyping | `typing.Protocol` and structural subtyping | This term names one job in the Week 9 milestone. |
| @runtime_checkable` and `isinstance` checks | `@runtime_checkable` and `isinstance` checks | This term names one job in the Week 9 milestone. |
| Dependency inversion principle | Dependency inversion principle | This term names one job in the Week 9 milestone. |
| Import boundary rules | Import boundary rules: services import protocols, not concrete classes | This term names one job in the Week 9 milestone. |
| Detecting import violations with `grep` or `import-linter | Detecting import violations with `grep` or `import-linter` | This term names one job in the Week 9 milestone. |
| Fake repositories implementing core protocols | Fake repositories implementing core protocols | This term names one job in the Week 9 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: `typing.Protocol` and structural subtyping
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 9, it supports the milestone: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: `@runtime_checkable` and `isinstance` checks
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 9, it supports the milestone: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: Dependency inversion principle
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 9, it supports the milestone: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Import boundary rules: services import protocols, not concrete classes
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 9, it supports the milestone: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Detecting import violations with `grep` or `import-linter`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 9, it supports the milestone: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: Fake repositories implementing core protocols
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 9, it supports the milestone: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/core/interfaces.py` — `PaperRepository`, `DocumentParser`, `SearchEngine`, `ExperimentRepository` protocols
- `tests/fakes/fake_paper_repository.py`
- `tests/fakes/fake_document_parser.py`
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
from typing import Protocol

class PaperRepository(Protocol):
    def list_papers(self) -> list[Paper]:
        ...
```

Line-by-line explanation:
- Line 1: `from typing import Protocol` — This imports a tool before the example can use it.
- Line 2: `(blank line)` — This blank line separates ideas so the example is easier to read.
- Line 3: `class PaperRepository(Protocol):` — This names a project concept so the code can talk in domain language.
- Line 4: `def list_papers(self) -> list[Paper]:` — This names a reusable action and shows what information it receives.
- Line 5: `...` — This performs one small visible step in the workflow.

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
- All service tests updated to use fakes
- `tests/unit/test_interfaces.py` — `isinstance` checks on fakes
Validation commands:
```bash
pytest tests/unit/ -v
python -c "from researchops.core.interfaces import PaperRepository; print('interfaces ok')"
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
Week 9 contributes by making **protocols, interfaces, and clean architecture** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 9 solve?
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

- Explain Protocols, Interfaces, and Clean Architecture in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: Protocols, Interfaces, and Clean Architecture.
- The milestone: All services depend on protocols from `core/interfaces.py`. No service imports from `storage/`, `parsing/`, or `ml/` directly. Fake repositories in `tests/fakes/` pass protocol `isinstance` checks.
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

Next week is Week 10: **Testing Discipline and Quality Gates**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: Test coverage ≥ 70%. CI fails if coverage drops below threshold. All services tested via fixtures and fakes.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace ``typing.Protocol` and structural subtyping` from user input to project result.
- Drill 2: Write one sentence defining ``typing.Protocol` and structural subtyping` without copying the notes.
- Drill 3: Find the file where ``typing.Protocol` and structural subtyping` appears or should appear.
- Drill 4: Name one wrong implementation of ``typing.Protocol` and structural subtyping` and why it would hurt.
- Drill 5: Name one test that would protect ``typing.Protocol` and structural subtyping`.
- Drill 6: Trace ``@runtime_checkable` and `isinstance` checks` from user input to project result.
- Drill 7: Write one sentence defining ``@runtime_checkable` and `isinstance` checks` without copying the notes.
- Drill 8: Find the file where ``@runtime_checkable` and `isinstance` checks` appears or should appear.
- Drill 9: Name one wrong implementation of ``@runtime_checkable` and `isinstance` checks` and why it would hurt.
- Drill 10: Name one test that would protect ``@runtime_checkable` and `isinstance` checks`.
- Drill 11: Trace `Dependency inversion principle` from user input to project result.
- Drill 12: Write one sentence defining `Dependency inversion principle` without copying the notes.
- Drill 13: Find the file where `Dependency inversion principle` appears or should appear.
- Drill 14: Name one wrong implementation of `Dependency inversion principle` and why it would hurt.
- Drill 15: Name one test that would protect `Dependency inversion principle`.
- Drill 16: Trace `Import boundary rules: services import protocols, not concrete classes` from user input to project result.
- Drill 17: Write one sentence defining `Import boundary rules: services import protocols, not concrete classes` without copying the notes.
- Drill 18: Find the file where `Import boundary rules: services import protocols, not concrete classes` appears or should appear.
- Drill 19: Name one wrong implementation of `Import boundary rules: services import protocols, not concrete classes` and why it would hurt.
- Drill 20: Name one test that would protect `Import boundary rules: services import protocols, not concrete classes`.
- Drill 21: Trace `Detecting import violations with `grep` or `import-linter`` from user input to project result.
- Drill 22: Write one sentence defining `Detecting import violations with `grep` or `import-linter`` without copying the notes.
- Drill 23: Find the file where `Detecting import violations with `grep` or `import-linter`` appears or should appear.
- Drill 24: Name one wrong implementation of `Detecting import violations with `grep` or `import-linter`` and why it would hurt.
- Drill 25: Name one test that would protect `Detecting import violations with `grep` or `import-linter``.
- Drill 26: Trace `Fake repositories implementing core protocols` from user input to project result.
- Drill 27: Write one sentence defining `Fake repositories implementing core protocols` without copying the notes.
- Drill 28: Find the file where `Fake repositories implementing core protocols` appears or should appear.
- Drill 29: Name one wrong implementation of `Fake repositories implementing core protocols` and why it would hurt.
- Drill 30: Name one test that would protect `Fake repositories implementing core protocols`.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes
## Why Month 2 code starts to hurt

You have built something real. ResearchOps can ingest PDFs, parse them, store them in SQLite, and search them. That is a genuine achievement. But now a problem is developing underneath the surface.

Open `src/researchops/services/ingestion_service.py`. Look at the constructor:

```python
def __init__(
    self,
    parser: DocumentParser,
    paper_repo: PaperRepository,
    failure_repo: FailureRepository,
) -> None:
```

This already looks clean. But imagine the version before Week 9 was written. Many codebases at this stage look like this instead:

```python
# BEFORE — tight coupling
import sqlite3
from researchops.storage.sqlite_repository import SQLiteRepository

class IngestionService:
    def __init__(self, db_path: str) -> None:
        conn = sqlite3.connect(db_path)          # directly creates its own database
        self.repository = SQLiteRepository(conn) # directly knows about SQLite
```

This is called **tight coupling**. The service knows exactly which database technology is used. It creates its own connection. It depends on a specific file path. Every single thing is locked in.

Why is this painful?

1. **Testing is expensive.** Every test must create a real SQLite database file. That is slow and creates cleanup problems.
2. **Swapping is impossible.** If you later want to test against a Postgres database or an in-memory store, you cannot without rewriting the service.
3. **Reading is harder.** A reader of the service cannot tell "what does this service really need?" because it is buried in construction details.
4. **Reuse fails.** You cannot take `IngestionService` and reuse it in a different project because it drags in all of SQLite with it.

This week you learn the tools to fix all of these problems.

---

## What coupling actually means

**Coupling** is the degree to which one module depends on the internal details of another. Low coupling is good. High coupling is a maintenance problem.

There are different kinds of coupling:

- **Data coupling**: modules share data structures (generally fine).
- **Control coupling**: one module controls the internal flow of another (problematic).
- **Content coupling**: one module reaches directly into the internals of another (worst case).

The tight example above shows content coupling — the service is reaching into SQLite internals directly by creating a `sqlite3.connect()` call.

**Dependency** is a formal relationship where module A needs module B to exist and function. Dependencies in Python are created by `import` statements. The key insight is: **the direction of dependencies matters**.

In bad code, high-level things (business logic) depend on low-level things (database drivers). In clean code, the relationship is inverted.

---

## Concrete class vs. abstraction

A **concrete class** is a real implementation. `SQLiteRepository`, `PyMuPDFParser`, `LogisticRegressionClassifier` — these are concrete. They have actual code inside them that does specific things using specific libraries.

An **abstraction** is a description of a capability without specifying the implementation. An abstraction says "something that can save a paper" rather than "the specific SQLite-backed class that saves a paper using this particular schema."

In Python, abstractions can be expressed several ways:

1. `typing.Protocol` — behavior-based, no inheritance required.
2. `abc.ABC` with abstract methods — inheritance-based, more explicit.
3. Duck typing — implicit, no annotation at all.

For this project, we use `typing.Protocol` because it is the most Pythonic, requires no inheritance, and works well with type checkers.

---

## Python Protocol in depth

`typing.Protocol` was added in Python 3.8. It allows you to define a structural subtype — meaning: any object that has the right methods and attributes satisfies the protocol, regardless of its class hierarchy.

Here is the `PaperRepository` protocol from `src/researchops/core/interfaces.py`:

```python
from typing import Protocol, runtime_checkable
from researchops.core.models import Paper


@runtime_checkable
class PaperRepository(Protocol):
    """Can persist and retrieve Paper objects."""

    def save(self, paper: Paper) -> None:
        """Persist a paper. Raises DuplicatePaperError if ID already exists."""
        ...

    def get(self, paper_id: str) -> Paper:
        """Retrieve a paper by ID. Raises PaperNotFoundError if missing."""
        ...

    def list_all(self) -> list[Paper]:
        """Return all stored papers."""
        ...

    def exists(self, paper_id: str) -> bool:
        """Return True if a paper with this ID is already stored."""
        ...

    def delete(self, paper_id: str) -> None:
        """Delete a paper by ID."""
        ...
```

Let us read this line by line.

`@runtime_checkable` — without this decorator, `isinstance(obj, PaperRepository)` would raise `TypeError`. With it, you can check at runtime whether an object satisfies the protocol. Useful for debug and validation.

`class PaperRepository(Protocol):` — inheriting from `Protocol` tells Python (and type checkers like mypy or pyright) that this class is not meant to be instantiated directly. It is a contract.

`def save(self, paper: Paper) -> None:` — this defines one required method. Any class that has a method named `save` accepting a `Paper` and returning `None` satisfies this part of the protocol. The method body is `...` (Ellipsis), which means "no implementation here, just the signature."

Now, `FakePaperRepository` in `tests/fakes/fake_repository.py`:

```python
class FakePaperRepository:
    """In-memory paper repository for testing."""

    def __init__(self) -> None:
        self._papers: dict[str, Paper] = {}

    def save(self, paper: Paper) -> None:
        if paper.id in self._papers:
            raise DuplicatePaperError(paper.id)
        self._papers[paper.id] = paper

    def get(self, paper_id: str) -> Paper:
        if paper_id not in self._papers:
            raise PaperNotFoundError(paper_id)
        return self._papers[paper_id]

    def list_all(self) -> list[Paper]:
        return list(self._papers.values())

    def exists(self, paper_id: str) -> bool:
        return paper_id in self._papers

    def delete(self, paper_id: str) -> None:
        self._papers.pop(paper_id, None)
```

`FakePaperRepository` does NOT inherit from `PaperRepository`. It does NOT inherit from anything (except the implicit `object`). But it satisfies the `PaperRepository` protocol because it implements all five required methods with matching signatures. Python's type checker will verify this automatically.

This is called **structural subtyping** or **duck typing with types**. Traditional inheritance is called **nominal subtyping** — a class must explicitly declare its parent. Structural subtyping only cares about shape.

---

## Dependency inversion

The **Dependency Inversion Principle** is one of the SOLID principles. It says:

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

In plain English: your business logic should not import your database code. Both your business logic and your database code should agree on an interface that sits between them.

Here is the before/after for `IngestionService`:

**Before — violation:**

```python
# BAD: the service reaches down into infrastructure
from researchops.storage.sqlite_repository import SQLiteRepository

class IngestionService:
    def __init__(self, db_path: str) -> None:
        self.repository = SQLiteRepository(db_path)
```

The dependency graph looks like:

```
IngestionService ──depends on──▶ SQLiteRepository ──depends on──▶ sqlite3
```

High-level service depends on a low-level detail.

**After — inversion applied:**

```python
# GOOD: the service depends on an abstraction
from researchops.core.interfaces import PaperRepository

class IngestionService:
    def __init__(self, paper_repo: PaperRepository, ...) -> None:
        self._paper_repo = paper_repo
```

The dependency graph now looks like:

```
IngestionService ──depends on──▶ PaperRepository (interface)
                                        ▲
SQLiteRepository ──implements──────────┘
FakePaperRepository ──implements───────┘
```

Both the high-level service and low-level implementations depend on the abstraction in the middle. The direction of the arrows changed. That is the inversion.

The **constructor** now receives a `PaperRepository`. The caller (CLI code, test code) decides which implementation to provide. This is called **constructor injection** or **dependency injection**.

---

## Interface

An **interface** is the contract that an abstraction expresses. It says: "any collaborator must provide these specific operations."

In languages like Java and C#, interfaces are formal language constructs. In Python, we use `Protocol` (or `ABC`) to achieve the same effect.

The key properties of a good interface:

1. **Minimal**: only include methods that callers actually use.
2. **Stable**: changing an interface affects everyone who implements it.
3. **Coherent**: all methods belong to the same concept.

`PaperRepository` is a good interface. Every method belongs to "how to manage papers." It does not include unrelated things like "how to send emails."

`DocumentParser` is another good interface:

```python
@runtime_checkable
class DocumentParser(Protocol):
    """Can parse a PDF file into a ParsedDocument."""

    def parse(self, path: Path) -> ParsedDocument:
        """Parse a single file and return its content + metadata."""
        ...
```

One method. Completely minimal. Any class with a `parse(path) -> ParsedDocument` method satisfies it.

---

## src/researchops/core/interfaces.py explained

This file is the architectural heart of Month 3. It lives in `core/` because it belongs to the domain — it describes what the application needs, not how those needs are fulfilled.

The file defines:

| Protocol | Purpose |
|---|---|
| `DocumentParser` | Parse a PDF file into a `ParsedDocument` |
| `PaperRepository` | Persist and retrieve `Paper` objects |
| `FailureRepository` | Record and retrieve `FailedDocument` records |
| `SearchEngine` | Search and index papers |
| `EmbeddingModel` | Produce vector embeddings from text |
| `ExperimentRepository` | Store ML experiment runs and metrics |

None of these protocols import SQLite, PyMuPDF, scikit-learn, or any other infrastructure library. They only import from `researchops.core.models` — the pure domain.

This is the **allowed imports rule**: code in `core/` may only import from Python stdlib and other `core/` modules. It must never import from `storage/`, `parsing/`, `ml/`, `cli/`, or any external library that involves I/O.

Why? Because `core/` must be importable anywhere, testable without any setup, and not drag in dependencies it does not need.

---

## Fake implementation and test double

A **test double** is any substitute for a real component used in tests. There are several types:

- **Fake**: a working but simplified implementation (e.g., in-memory repository).
- **Stub**: returns fixed data but does not record calls.
- **Mock**: records how it was called so tests can assert on interactions.
- **Spy**: a real implementation that also records calls.
- **Dummy**: passed around but never actually used.

For this project, fakes are the most useful because they behave correctly — they store papers, raise the right errors, and return real data — just without a database.

`FakePaperRepository` in `tests/fakes/fake_repository.py` is a complete fake:

```python
class FakePaperRepository:
    def __init__(self) -> None:
        self._papers: dict[str, Paper] = {}   # in-memory store; never touches disk

    def save(self, paper: Paper) -> None:
        if paper.id in self._papers:
            raise DuplicatePaperError(paper.id)  # same error as the real repo
        self._papers[paper.id] = paper

    def get(self, paper_id: str) -> Paper:
        if paper_id not in self._papers:
            raise PaperNotFoundError(paper_id)   # same error as the real repo
        return self._papers[paper_id]

    def list_all(self) -> list[Paper]:
        return list(self._papers.values())       # returns real Paper objects

    def exists(self, paper_id: str) -> bool:
        return paper_id in self._papers

    def delete(self, paper_id: str) -> None:
        self._papers.pop(paper_id, None)         # silent if not found
```

Line by line:

- `self._papers: dict[str, Paper] = {}` — papers are stored as a dictionary keyed by ID. Simple and fast.
- `raise DuplicatePaperError(paper.id)` — importantly, the fake raises the *same exceptions* as the real repository. This means service code written against the fake will behave the same against SQLite.
- `list(self._papers.values())` — returns a copy so callers cannot accidentally modify internal state.

The corresponding `FakeDocumentParser` allows tests to configure both successful parses and deliberate failures:

```python
class FakeDocumentParser:
    def __init__(self) -> None:
        self._results: dict[str, ParsedDocument] = {}
        self._errors: dict[str, Exception] = {}

    def set_result(self, path: Path, doc: ParsedDocument) -> None:
        self._results[str(path)] = doc

    def set_error(self, path: Path, error: Exception) -> None:
        self._errors[str(path)] = error

    def parse(self, path: Path) -> ParsedDocument:
        key = str(path)
        if key in self._errors:
            raise self._errors[key]
        if key in self._results:
            return self._results[key]
        raise ParsingError(f"FakeParser: no result configured for {path}")
```

This design is deliberate. A test that needs a parser failure calls `parser.set_error(pdf, ParsingError("corrupted"))`. A test that needs a successful parse calls `parser.set_result(pdf, _parsed_doc(pdf))`. The fake is fully controllable.

---

## Service layer and infrastructure layer

**Clean architecture** separates code into layers with strict dependency rules:

```
┌─────────────────────────────────────────────────┐
│  CLI / API Layer (external interface)           │
│  Knows about services. Builds real adapters.    │
├─────────────────────────────────────────────────┤
│  Application Layer (services)                   │
│  IngestionService, SearchService, etc.          │
│  Depends only on core protocols and models.     │
├─────────────────────────────────────────────────┤
│  Domain / Core Layer                            │
│  Models, interfaces, exceptions, value objects  │
│  No external dependencies. Pure Python.         │
├─────────────────────────────────────────────────┤
│  Infrastructure Layer (adapters)                │
│  SQLiteRepository, PyMuPDFParser, etc.          │
│  Implements the core protocols.                 │
└─────────────────────────────────────────────────┘
```

The arrows of allowed imports point **inward only**:

- Infrastructure can import from Core.
- Services can import from Core.
- CLI can import from Services and Infrastructure.
- Core imports from nothing (except stdlib).

The rules that ResearchOps enforces:

- `core/` — no imports from `storage/`, `parsing/`, `ml/`, `cli/`, `api/`, `workers/`.
- `services/` — no imports from `storage/`, `parsing/`, or other concrete infrastructure.
- `storage/`, `parsing/`, `ml/` — may import from `core/`, stdlib, and external libraries.
- `cli/`, `api/` — the composition root; they wire everything together and are allowed to import broadly.

This is why `IngestionService` is in `services/` and `SQLiteRepository` is in `storage/`. They are different layers.

---

## Ports and adapters (hexagonal architecture)

A more visual way to think about this is **ports and adapters**, also called hexagonal architecture.

A **port** is an interface the application defines for itself. It says: "I need something that can do X."

An **adapter** is a concrete implementation that plugs into a port. It says: "I am the SQLite implementation of X."

```
                        ┌──────────────────┐
                        │   Application    │
  ┌──────────┐  port    │                  │  port    ┌──────────────┐
  │  CLI     │◀────────▶│  IngestionService│◀────────▶│ PaperRepository │
  │ (adapter)│          │                  │ (port)   │ (port)          │
  └──────────┘          └──────────────────┘          └────────┬─────┘
                                                               │
                                                    ┌──────────▼────────┐
                                                    │ SQLiteRepository  │
                                                    │ (adapter)         │
                                                    └───────────────────┘
```

In ResearchOps:

| Port (protocol) | Adapter (concrete) |
|---|---|
| `PaperRepository` | `SQLiteRepository` |
| `FailureRepository` | `SQLiteRepository` |
| `DocumentParser` | `PyMuPDFParser` |
| `PaperRepository` (test) | `FakePaperRepository` |
| `DocumentParser` (test) | `FakeDocumentParser` |

The application layer never knows which adapter is plugged in. This is the entire point.

---

## Modular monolith

ResearchOps is a **modular monolith**. It runs as a single process (not microservices), but the codebase is divided into clearly bounded modules with enforced dependency rules.

The modules are:

- `core/` — domain models and interfaces (no infrastructure).
- `services/` — application logic (no infrastructure).
- `storage/` — SQLite adapters.
- `parsing/` — PDF parsers.
- `ml/` — machine learning code.
- `search/` — search engine.
- `cli/` — command-line interface.
- `api/` — HTTP API.
- `workers/` — background job processing.

Each module has a clear purpose and its imports can be audited. A modular monolith is easier to maintain than a tangle because you can reason about one module at a time.

Why not microservices? For a learning project and a small production system, microservices add infrastructure complexity (networking, service discovery, deployment, serialization) without proportional benefit. Modular monoliths can be refactored into microservices later, if needed, precisely because the boundaries are already clear.

---

## Why this is not overengineering

A common objection: "This seems like a lot of abstractions for a small project. Is it necessary?"

The answer depends on what the abstractions are earning.

In ResearchOps, protocols earn real benefits:

1. **Unit tests run without a database.** `tests/unit/test_ingestion_service.py` runs all twelve test cases using `FakePaperRepository` and `FakeDocumentParser`. No SQLite file. No PDF files. Each test completes in milliseconds.
2. **The service is readable.** The constructor type annotations tell you exactly what the service needs.
3. **Infrastructure can be swapped.** If you later replace PyMuPDF with pdfminer, only the adapter changes. The service and all its tests continue to pass unchanged.
4. **ML code (Week 11) can be added without touching services.** The ML pipeline is independent of the ingestion pipeline because they both depend on the same `PaperRepository` protocol.

Overengineering means creating abstractions that do not earn these benefits. A protocol for a utility function that is never swapped and never faked would be overengineering. A protocol for the persistence layer of a growing system is not.

The rule of thumb: create an abstraction when you have two or more implementations (real and fake counts), or when you expect the implementation to change.

---

## The before/after refactor in full

Here is the full before/after for IngestionService, explained line by line.

**Before:**

```python
import sqlite3
from researchops.storage.sqlite_repository import SQLiteRepository
from researchops.parsing.pdf_parser import PyMuPDFParser

class IngestionService:
    def __init__(self, db_path: str) -> None:
        conn = sqlite3.connect(db_path)
        self.repository = SQLiteRepository(conn)
        self.parser = PyMuPDFParser()
```

- `import sqlite3` — the service imports a database driver directly. Any test must have SQLite available.
- `SQLiteRepository(conn)` — the service constructs its own collaborator. Tests cannot substitute a fake.
- `PyMuPDFParser()` — same problem. Tests cannot inject a controlled fake parser.
- `db_path: str` — the constructor takes a file path. Tests must create real files.

**After:**

```python
from researchops.core.interfaces import DocumentParser, FailureRepository, PaperRepository

class IngestionService:
    def __init__(
        self,
        parser: DocumentParser,
        paper_repo: PaperRepository,
        failure_repo: FailureRepository,
    ) -> None:
        self._parser = parser
        self._paper_repo = paper_repo
        self._failure_repo = failure_repo
```

- `from researchops.core.interfaces import ...` — the service imports only from `core/`. No infrastructure.
- `parser: DocumentParser` — the service receives a parser. The caller decides which implementation.
- `paper_repo: PaperRepository` — the service receives a repository. A fake can be passed in tests.
- `failure_repo: FailureRepository` — same pattern.
- The constructor stores collaborators as private attributes (`_parser`, `_paper_repo`). It does not create them.

The CLI then wires the real implementations:

```python
# In cli/commands/ingest.py (the composition root):
conn = sqlite3.connect(db_path)
real_repo = SQLiteRepository(conn)
real_parser = PyMuPDFParser()
service = IngestionService(
    parser=real_parser,
    paper_repo=real_repo,
    failure_repo=real_repo,
)
```

The CLI is allowed to import from both `storage/` and `parsing/` because it is the outer layer that assembles the system. Services are not.

---

## Why this matters when you change things later

Month 4 adds an HTTP API. Month 5 adds production deployment. Imagine if `IngestionService` had SQLite hard-coded inside it. Every API endpoint and every deployment configuration would drag in SQLite assumptions.

With protocols:

- Swapping SQLite for Postgres: write a new `PostgresRepository` that implements `PaperRepository`. Point the CLI at it. Nothing else changes.
- Adding a test for the API that needs paper storage: inject `FakePaperRepository`. No database needed.
- Adding an ML model that reads papers: inject any `PaperRepository` implementation. The model does not care which.

This is why clean architecture is an investment. It costs a little more now. It pays back every time the system changes.

---

## Summary of key vocabulary

| Term | Meaning |
|---|---|
| Coupling | Degree to which one module depends on another's internals |
| Dependency | A module that another module requires to function |
| Concrete class | A real implementation with actual code |
| Abstraction | A description of capability without specifying implementation |
| Interface | The contract that an abstraction expresses |
| Protocol | Python's mechanism for structural interfaces (`typing.Protocol`) |
| Dependency inversion | High-level code depends on abstractions, not low-level details |
| Dependency injection | Passing collaborators in from the outside (constructor injection) |
| Fake | A working simplified implementation used in tests |
| Test double | Any substitute for a real component in tests |
| Port | An interface the application defines for itself |
| Adapter | A concrete implementation that plugs into a port |
| Service layer | Application logic; depends on abstractions, not infrastructure |
| Infrastructure layer | Concrete implementations: SQLite, parsers, ML models |
| Modular monolith | Single-process app with clear module boundaries |
| Composition root | The outer layer (CLI/API) that wires everything together |
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
