<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It — Week 09 Protocols and Clean Architecture

These experiments are designed to make things fail in instructive ways. Do each one, observe what happens, and write down what you learned.

---

## Purpose of failure practice

Protocols and architecture boundaries can feel invisible when everything is working. Failure practice makes the invisible contract visible: you remove a method, cross a layer boundary, or change a signature, then watch which tool notices first. In ResearchOps, this protects the learner from building services that accidentally depend on SQLite, PDF parsing, or other concrete infrastructure.

## Failure lab rules

1. Make exactly one intentional break at a time.
2. Predict the failure before running a command: expected error, expected test failure, or expected architecture violation.
3. Run the narrowest command first, then the broader gate only after the narrow command teaches you something.
4. Record how to cause it, the expected error, how to inspect it, how to fix it, the test that should catch it, what it teaches, and one common wrong fix.
5. Restore the original code before moving to the next experiment.
6. Never leave a broken protocol, fake, or service import in the repository.

## Intentional break experiments

## Experiment 1: Remove a required method from a fake

Go to `tests/fakes/fake_repository.py`. Delete the `exists` method from `FakePaperRepository`.

Then run:

```bash
pytest tests/unit/test_ingestion_service.py -v
```

**What to observe:** The test suite may still pass because `runtime_checkable` only checks method names at the `isinstance()` call, not at construction time. But a type checker like mypy will catch it.

Now run:

```bash
mypy src tests
```

**Question to answer:** mypy reports that `FakePaperRepository` does not satisfy `PaperRepository`. Which test fails first? Which behavior of `IngestionService` relies on `exists`?

**Restore the method before continuing.**

---

## Experiment 2: Put an infrastructure import inside a service

Open `src/researchops/services/ingestion_service.py`. At the top, add this import:

```python
import sqlite3
```

You are not using it. Just importing it.

Run:

```bash
ruff check src
```

**What to observe:** ruff may flag it as an unused import (`F401`). Now run your forbidden-import audit script from Exercise W9-9.

Now change the import to actually use it:

```python
import sqlite3
conn = sqlite3.connect(":memory:")  # inside the class constructor
```

**Questions to answer:** Does the project still pass tests? Does this violate the architecture rules you mapped in Exercise W9-6? What is the real danger of this?

**Restore the original file before continuing.**

---

## Experiment 3: Change a protocol method signature

In `src/researchops/core/interfaces.py`, change the `PaperRepository.save` signature to:

```python
def save(self, paper: Paper, *, overwrite: bool = False) -> None:
    ...
```

Run:

```bash
mypy src tests
```

**What to observe:** The concrete `SQLiteRepository.save` and `FakePaperRepository.save` no longer match the updated protocol signature. mypy should report errors.

**Questions to answer:** How many files need to change? What is the cost of changing a protocol? Does this help you understand why protocol interfaces should be stable and minimal?

**Restore the original signature before continuing.**

---

## Experiment 4: Build a fake that behaves differently from the real repo

Write a new class `PermissiveFakePaperRepository` that does NOT raise `DuplicatePaperError` when saving an existing paper ID. Instead, it silently overwrites.

Write a test that:

1. Saves a paper with ID "abc".
2. Saves a different paper with the same ID "abc".
3. Calls `list_all()` and asserts how many papers are returned.

Now ask: would this test pass against the real `SQLiteRepository`? Try it (use `tmp_path` and create a real SQLite database).

**Questions to answer:** If your unit test passes with `PermissiveFakePaperRepository` but fails with the real repo, what does that tell you about test confidence? What rule were you supposed to follow when writing fakes?

---

## Experiment 5: Make a service construct its own dependency

In `tests/unit/test_ingestion_service.py`, modify the `service` fixture to not inject a parser:

```python
@pytest.fixture()
def service(paper_repo, failure_repo) -> IngestionService:
    # attempt to construct without a parser
    return IngestionService(
        parser=None,   # pass None deliberately
        paper_repo=paper_repo,
        failure_repo=failure_repo,
    )
```

Run the test suite. When does the failure actually occur — at construction time, or later when `parse()` is called?

**Questions to answer:** What is the difference between "fail at construction time" and "fail at call time"? Which is easier to debug? How would you add a guard to fail fast at construction time?

---

## Debugging tasks

**Task D1: Find where the composition root is**

Run:

```bash
grep -r "SQLiteRepository" src/researchops/ --include="*.py" -l
```

List every file that imports `SQLiteRepository`. Each file that appears is a "composition point." Are any of them inside `services/`? Should they be?

**Task D2: Run tests by layer**

```bash
pytest tests/unit -v      # unit tests: should need no database
pytest tests/integration -v   # integration tests: may use SQLite
```

How long does each suite take? Which layer runs faster? Why?

**Task D3: Check runtime_checkable**

Open a Python REPL:

```python
from researchops.core.interfaces import PaperRepository
from tests.fakes.fake_repository import FakePaperRepository

repo = FakePaperRepository()
print(isinstance(repo, PaperRepository))  # should be True

class EmptyClass:
    pass

print(isinstance(EmptyClass(), PaperRepository))  # should be False
```

Now try with an object that has only some of the required methods. What does `isinstance` return?

---

## Debugging checklist

Use this checklist whenever a Week 9 break behaves differently than expected:

- [ ] Did you break only one protocol, fake, service, or import at a time?
- [ ] Did you run the smallest relevant command first (`pytest tests/unit/ -q`, `ruff check src tests`, or `mypy src tests`)?
- [ ] Did you inspect both the protocol in `src/researchops/core/interfaces.py` and the fake in `tests/fakes/fake_repository.py`?
- [ ] Did you check whether the service imports only protocols/models/exceptions from `core/`?
- [ ] Did you restore the exact method name, argument list, return type, and exception behavior?
- [ ] Did you rerun the command that originally failed and confirm it now passes?

---

## Edge cases to explore

**EC1: Fake repository with duplicate IDs**

What happens if you call `FakePaperRepository.save` with a paper whose ID is the empty string `""`? What about a paper with `id=None` (if you remove the type annotation)? Does the real `SQLiteRepository` behave the same way?

**EC2: Fake parser with empty text**

Configure `FakeDocumentParser.set_result` to return a `ParsedDocument` with `raw_text=""`. Run ingestion. Does the paper get saved? Is that the right behavior? Look at the `is_empty()` method on `ParsedDocument`.

**EC3: Multiple services sharing one fake**

Create one `FakePaperRepository` instance. Inject it into both an `IngestionService` and a `KeywordSearchService`. Ingest a paper using the ingestion service. Then search for it using the search service. Does the search service find the paper? Why?

---

## Reflection after breaking

After completing all experiments, answer these questions:

1. Which coupling was the hardest to remove? Why?
2. How did fake-based tests change your testing speed and confidence?
3. What makes an abstraction useful instead of ceremonial?
4. If you had to explain dependency inversion to someone in one minute, what would you say?
5. Where in ResearchOps do you still see tight coupling that future weeks will need to address?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
