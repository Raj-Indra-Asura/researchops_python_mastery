# Exercises - Week 09 Protocols and Clean Architecture

## Warm-up: Protocol mechanics

These exercises build muscle memory before touching the project.

**Exercise W9-1: Write your first protocol**

Without looking at `interfaces.py`, write a protocol called `TextSummarizer` with one method: `summarize(text: str) -> str`. Then write two classes that satisfy the protocol: `TruncatingSummarizer` (returns the first 100 characters) and `SentenceSummarizer` (returns the first sentence). Do not use inheritance. Verify with `isinstance(obj, TextSummarizer)`.

**Exercise W9-2: Spot the violation**

Read this code and identify every dependency rule violation. Write a one-sentence explanation for each:

```python
import sqlite3
from researchops.storage.sqlite_repository import SQLiteRepository
from researchops.parsing.pdf_parser import PyMuPDFParser

class TopicService:
    def __init__(self) -> None:
        conn = sqlite3.connect("researchops.db")
        self.repo = SQLiteRepository(conn)
        self.parser = PyMuPDFParser()

    def classify(self, pdf_path: str) -> str:
        doc = self.parser.parse(pdf_path)
        papers = self.repo.list_all()
        return "nlp"  # placeholder
```

How many violations can you find? Write them all.

**Exercise W9-3: Dependency injection by hand**

Rewrite the `TopicService` above so it accepts its dependencies from the outside. Define the minimal protocols needed. Do not create fake implementations yet — just the protocol definitions and the refactored constructor.

**Exercise W9-4: Protocol satisfiability check**

Create a class `WeirdSaver` that has a `save` method but with a slightly different signature than `PaperRepository.save`:

```python
def save(self, p) -> None:  # note: no type annotation
    pass
```

Does `isinstance(WeirdSaver(), PaperRepository)` return `True` or `False`? Try it. What does this tell you about runtime_checkable and structural subtyping?

---

## Project exercises: ResearchOps codebase

**Exercise W9-5: Read and annotate interfaces.py**

Open `src/researchops/core/interfaces.py`. For each protocol, write:

- One sentence explaining what it represents.
- The name of the concrete class that implements it (hint: look in `storage/` and `parsing/`).
- The name of the fake class used in tests (hint: look in `tests/fakes/`).
- One example of a test that uses the fake instead of the real implementation.

**Exercise W9-6: Trace the dependency chain**

Start from `src/researchops/cli/commands/ingest.py`. Trace every import. Draw (or write as a list) the full dependency chain from CLI to model, following imports. Then identify: at which point does the chain switch from infrastructure to application layer?

**Exercise W9-7: Write a new fake**

The `FakeDocumentParser` exists. But there is no `FakeSearchEngine` yet.

Write `FakeSearchEngine` in `tests/fakes/fake_repository.py` that satisfies the `SearchEngine` protocol. It should store indexed papers in a list and return any stored papers whose text contains the query string. Make it simple but correct.

**Exercise W9-8: Write a service test using your fake**

Write a new test file `tests/unit/test_search_service_with_fake.py`. Import your `FakeSearchEngine` (or `FakePaperRepository` since `KeywordSearchService` uses `PaperRepository`). Write at least three tests:

1. `test_search_empty_repository_returns_no_results`
2. `test_search_finds_paper_by_keyword`
3. `test_search_returns_results_ordered_by_score`

Each test must use only fakes — no SQLite, no real files.

**Exercise W9-9: Forbidden import audit**

Write a Python script (in `/tmp/` so it is not committed) that checks every file in `src/researchops/services/` and `src/researchops/core/` for imports of `sqlite3`, `pymupdf`, `sklearn`, or any other infrastructure library. Report violations. Then check: does this project pass your audit?

---

## Stretch exercises

**Exercise W9-S1: Protocol for a clock**

Time-dependent code is hard to test because `datetime.utcnow()` returns different values in different test runs. Define a `Clock` protocol with one method: `now() -> datetime`. Write a `RealClock` that calls `datetime.utcnow()` and a `FixedClock` that always returns the same datetime. Show how you would inject `Clock` into a service that needs to timestamp records.

**Exercise W9-S2: Draw the full architecture**

Draw the full dependency graph for ResearchOps. Use boxes for modules and arrows for "depends on." Verify that no arrow points from `core/` outward and no arrow points from `services/` to `storage/` or `parsing/`.

**Exercise W9-S3: ExperimentRepository protocol**

Read the `ExperimentRepository` protocol in `interfaces.py`. It has four methods. Write a `FakeExperimentRepository` that stores runs in memory. Then write a minimal test that creates a run, logs two metrics, and retrieves the run to verify the metrics are present.

---

## Written reflection questions

Answer each question in 3–5 sentences.

1. You have just built a new `MLPredictionService`. A colleague says: "Just import `SQLiteRepository` directly — it's faster to write." How do you respond? What would you show them?

2. What is the difference between a fake and a mock? When would you prefer a fake?

3. Your `PaperRepository` protocol has five methods. You add a sixth method `search_by_title`. What must you also update? What could break?

4. A junior developer says "protocols are just documentation — the program works without them." How do you correct this, specifically mentioning type checkers and runtime_checkable?

5. Where is the composition root in ResearchOps? Why does it matter that composition happens there and not inside a service?
