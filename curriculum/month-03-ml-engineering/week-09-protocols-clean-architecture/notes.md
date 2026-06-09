# Notes - Week 09 Protocols and Clean Architecture

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 9 — Protocols & Clean Architecture](./README.md) › **notes.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 9 — Protocols & Clean Architecture** · *notes.md — the textbook chapter* (step 2 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [README](./README.md)
- ▶ **Next:** [exercises.md](./exercises.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. **➡ [notes.md](./notes.md) ← you are here**
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 10](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 10 — Testing & Quality Gates](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 9 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
