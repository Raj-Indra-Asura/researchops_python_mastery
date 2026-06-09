<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->
# Notes - Week 09 Protocols and Clean Architecture

## Chapter overview

This week is about one sentence that professional Python developers repeat often: **depend on what something can do, not on the exact class that does it**.
In Python, the tool that lets us write that sentence in code is `typing.Protocol`.
A protocol describes a shape: method names, parameter types, return types, and properties that an object must provide.
A class does not need to inherit from the protocol to match it.
If it has the right methods with the right meanings, type checkers can treat it as satisfying the protocol.
That style is called **structural typing** because the structure of the object matters more than its family tree.
ResearchOps uses protocols to protect its architecture boundaries.
The core layer defines the project language: `Paper`, `ParsedDocument`, `FailedDocument`, repository interfaces, parser interfaces, and service-facing contracts.
The infrastructure layer provides concrete tools: SQLite storage, PDF parsing code, and other adapters that talk to outside systems.
The service layer coordinates use cases such as ingestion and search.
The service layer should not know whether papers come from SQLite, a fake in-memory dictionary, or a later storage adapter.
It only needs to know that the object passed in can `save`, `get`, `list_all`, `exists`, and `delete` papers.
That is exactly what `PaperRepository` says in `src/researchops/core/interfaces.py`.
The practical milestone for this chapter is architectural clarity.
A learner should be able to open `src/researchops/core/interfaces.py` and explain why the protocols live there.
A learner should be able to open `src/researchops/services/ingestion_service.py` and point to constructor arguments typed as protocols.
A learner should be able to open `tests/fakes/fake_repository.py` and explain why a fake repository is useful.
A learner should be able to say why `services/` must not import concrete storage or parser implementations.
This chapter does not ask you to add a new product feature.
It asks you to make the existing project easier to change, easier to test, and easier to explain.
That is still real engineering work.
A messy project can have working features but become painful to extend.
A clean project can accept new features without each change damaging unrelated code.
Week 9 is where ResearchOps starts behaving like a modular system instead of a collection of scripts.
By the end, you should be able to draw the dependency arrows from memory.
CLI commands wire objects together at the outside edge.
Services receive collaborators through their constructors.
Services call methods on protocols.
Infrastructure implements those protocols.
Core defines the shared language and imports no infrastructure.
Tests use fakes that implement the same protocols as real infrastructure.
This is the dependency inversion principle in practice, not as a slogan.
High-level policy, such as ingestion workflow rules, should not depend on low-level details, such as SQLite connection handling.
Both should meet at an abstraction owned by the core/application boundary.
For ResearchOps, those abstractions are Python protocols.
Keep the phrase **shape before class** in your mind as you read.
A protocol names the shape a service needs.
A concrete class provides that shape.
A fake class provides the same shape for tests.
If all three agree, the project stays flexible.
If they disagree, errors appear as import tangles, brittle tests, or services that are hard to run without real files and databases.
This chapter teaches you to notice those problems early.

## What you already know from previous weeks

- **Week 1:** You saw the repository scaffold, the first domain models, and a simple CLI shape.
- **Week 2:** You practiced paths, file discovery, exceptions, and logging so command-line behavior could fail clearly.
- **Week 3:** You worked with classes and dataclasses, which prepared you to understand objects as bundles of data and behavior.
- **Week 4:** You learned how CLI commands expose project behavior to a user without owning every business rule.
- **Week 5:** You built SQLite persistence, which gave ResearchOps a real infrastructure adapter that stores papers on disk.
- **Week 6:** You built the parsing pipeline, which gave ResearchOps another infrastructure adapter that turns PDFs into parsed documents.
- **Week 7:** You added keyword search and data-quality thinking, which showed how services can read stored papers and produce useful results.
- **Week 8:** You learned multiprocessing ingestion, which made the boundary between orchestration and CPU-heavy work more important.

The important pattern from those weeks is that every new ability created a new responsibility.
File discovery should not be mixed with database schema code.
PDF parsing should not be hidden inside a command-line option parser.
Search ranking should not be written inside a SQLite connection helper.
When responsibilities stay separate, you can test each one more directly.
When responsibilities blend together, every test becomes an integration test whether you wanted that or not.
Before protocols, you may have used concrete classes directly because that felt simpler.
For example, a service could create a SQLite repository in its own constructor.
That seems convenient for the first run because the caller passes fewer objects.
It becomes inconvenient when a unit test wants to avoid disk I/O.
It also becomes inconvenient when a learner tries to answer, "What does this service actually need?"
A constructor that accepts `db_path: Path` hides the real need.
The service does not truly need a path.
The service needs something that can store and retrieve papers.
That difference is the doorway into Week 9.
You also already know enough type hints to read protocol method signatures.
A line such as `def parse(self, path: Path) -> ParsedDocument:` says: give me a `Path`, I return a `ParsedDocument`.
A line such as `def list_all(self) -> list[Paper]:` says: I need no extra input and I return a list of `Paper` objects.
Protocols collect those signatures under a project name.
Do not think of protocols as advanced magic.
Think of them as named expectations.
A service has expectations about collaborators.
A protocol writes those expectations down.

## What problem this week solves

- **Hard-coded infrastructure:** A service that imports SQLite directly is hard to test without a database file.
- **Hidden collaborators:** A constructor that creates its own parser hides the fact that parsing is a separate dependency.
- **Import tangles:** If services import storage and parsing modules freely, dependency arrows point in too many directions.
- **Slow unit tests:** Tests that need real PDFs and real SQLite setup are slower and harder to understand.
- **Unsafe refactors:** Changing a concrete class can break unrelated code when no stable contract exists.
- **Vague architecture:** A diagram is not enough; code must enforce the same boundary the diagram describes.

The specific ResearchOps problem is this: services should express business workflows, not infrastructure decisions.
`IngestionService` should answer workflow questions.
Which PDF files were discovered?
Should an existing paper be skipped?
What happens when parsing fails?
When should a failure record be stored?
It should not answer infrastructure questions.
Which SQLite pragma should be enabled?
Which database file should be opened?
Which concrete PDF parser class should be constructed?
Which fake parser should a test use?
Those choices belong outside the service.
The protocol boundary lets the service say only what it needs.
It needs a parser-shaped object.
It needs a paper-repository-shaped object.
It needs a failure-repository-shaped object.
The caller decides which concrete objects fill those roles.
That caller might be a CLI command in normal use.
That caller might be a unit test in test use.
Both callers use the same service because the service depends on shapes.
This is the exact problem dependency inversion solves.
Instead of high-level service code depending on low-level infrastructure code, both depend on stable abstractions.
In ResearchOps, those stable abstractions live in `core/interfaces.py`.
The result is not merely prettier code.
The result is code that can be tested with fakes, audited with import rules, and extended without rewriting central workflows.

## Beginner mental model

Imagine a wall outlet.
The lamp does not know the power plant.
The lamp knows the outlet shape and voltage expectation.
The power plant, solar panel, or battery system can change behind the wall.
As long as the outlet contract is honored, the lamp works.
A protocol is the outlet shape for Python objects.
`PaperRepository` is an outlet shape for paper storage.
`DocumentParser` is an outlet shape for parsing documents.
`FailureRepository` is an outlet shape for recording failed documents.
The service is the lamp.
The concrete repository is the power source adapter.
The fake repository is a small battery used during tests.
The service should not unscrew the wall and inspect the power plant.
In code terms, that means the service should not import `researchops.storage.sqlite_repository`.
It should import `researchops.core.interfaces` instead.
Another mental model is a job description.
A job description says, "This role must save papers, retrieve papers by ID, list all papers, check existence, and delete papers."
It does not say, "The person must be named SQLitePaperRepository."
A real employee can satisfy the job description.
A temporary test double can satisfy the job description during practice.
What matters is behavior at the boundary.
Do not confuse the protocol with the implementation.
The protocol is a promise about available operations.
The implementation is code that performs those operations.
Do not confuse dependency injection with a framework.
Here, dependency injection simply means passing collaborators into a constructor instead of constructing them inside the service.
Do not confuse clean architecture with folder decoration.
Clean architecture is about dependency direction.
Folders help humans see the direction, but imports enforce it.
A useful four-question checklist is:
- What does this object need from the outside world?
- Can that need be described as a protocol?
- Which layer should define the protocol?
- Which outer layer should provide the concrete implementation?
If you can answer those questions, protocols become practical instead of abstract.

## Core vocabulary

| Term | Meaning in this chapter |
|---|---|
| Protocol | A class-like type from `typing` that describes methods and attributes an object must provide. |
| Structural typing | Type compatibility based on shape rather than explicit inheritance. |
| Nominal typing | Type compatibility based on declared names or inheritance relationships. |
| Concrete class | A class with real behavior, such as a repository that opens SQLite connections. |
| Abstraction | A simplified contract that hides implementation details while preserving needed behavior. |
| Interface | A boundary description that tells callers what methods are available. |
| Port | A use-case-facing interface owned by the application or core boundary. |
| Adapter | A concrete object that plugs into a port and talks to an outside detail. |
| Dependency | Something one piece of code needs in order to do its job. |
| Dependency inversion | The rule that high-level policy depends on abstractions, not low-level details. |
| Dependency injection | Supplying dependencies from outside an object, commonly through the constructor. |
| Service layer | Application use-case code that coordinates models, protocols, and rules. |
| Infrastructure layer | Concrete code that talks to files, databases, parsers, tools, or other outside mechanisms. |
| Core layer | The innermost layer containing domain models, exceptions, value objects, and protocol definitions. |
| Fake | A simple working implementation used in tests, usually in memory and fully controlled by the test. |
| Stub | A test double that returns prepared answers and may not implement full behavior. |
| Mock | A test double focused on recording or asserting calls; useful sometimes but easy to overuse. |
| Composition root | The outer place where real implementations are constructed and passed into services. |
| Import boundary | A rule about which package is allowed to import which other package. |
| Runtime check | A check performed while Python is running, such as `isinstance(obj, ProtocolName)` when allowed. |
| Static check | A check performed by a type checker before running code. |
| Ellipsis body | The `...` used in protocol methods to say the method exists but is not implemented here. |

Vocabulary is useful only if you can point to code.
When you say protocol, point to `src/researchops/core/interfaces.py`.
When you say adapter, point to `src/researchops/storage/sqlite_repository.py` or `src/researchops/parsing/pdf_parser.py`.
When you say fake, point to `tests/fakes/fake_repository.py`.
When you say service layer, point to `src/researchops/services/ingestion_service.py` or `src/researchops/services/search_service.py`.
When you say composition root, point to CLI command code that creates concrete objects and passes them into services.

## Concept explanations from first principles

### 6.1 Why ordinary imports create coupling
An import is more than a way to reuse a name.
An import is a dependency arrow.
When `A` imports `B`, `A` cannot even be loaded unless `B` can be loaded.
If `B` imports a third-party package, opens a heavy module, or assumes a certain environment, `A` inherits that burden.
This is acceptable when the dependency direction matches the architecture.
It is dangerous when inner application logic imports outer details.
For example, a CLI command can import a SQLite repository because CLI code is at the outside edge.
The CLI command is responsible for wiring real tools together.
A service should not import that SQLite repository because the service is high-level workflow code.
If the service imports SQLite directly, every service test becomes tied to SQLite setup.
The service also becomes harder to reuse with a different storage mechanism.
Protocols reduce this coupling by moving the dependency to a small, stable contract.
The service imports `PaperRepository` from core.
The SQLite adapter imports `Paper` and exceptions from core and implements the methods.
A fake repository imports the same models and exceptions and implements the same methods in memory.
The service can use either object without changing its own code.

### 6.2 What `typing.Protocol` actually does
`Protocol` comes from Python's `typing` module.
It lets you write a class whose main job is to describe required methods.
A protocol method usually has a signature and an ellipsis body.
The signature says what the method must look like.
The ellipsis says this protocol is not providing the real implementation.
That is why a protocol is not a repository by itself.
It is a contract for repositories.
If a class has all required methods, it satisfies the protocol structurally.
The class does not need to write `class SQLitePaperRepository(PaperRepository)`.
It may do so, but ResearchOps does not require it.
This keeps infrastructure classes independent while still letting type hints describe expectations.

### 6.3 Structural typing versus nominal typing
Nominal typing asks, "Does this object have the right declared name or base class?"
Structural typing asks, "Does this object have the right shape?"
A beginner analogy is a phone charger cable.
If the plug shape fits and the electrical expectations are correct, the charger works.
You do not care whether the cable inherited from an official base cable class.
In Python, structural typing fits the language culture because Python already often uses duck typing.
Duck typing means: if it walks like a duck and quacks like a duck, code can treat it like a duck.
Protocols make duck typing visible to tools and readers.
Without a protocol, a service constructor might accept `object`, which communicates almost nothing.
With a protocol, the constructor says exactly which duck behaviors are needed.

### 6.4 Why `@runtime_checkable` exists
Most protocol benefits happen during static analysis and human reading.
Python itself normally does not enforce type hints at runtime.
If you want to use `isinstance(fake_repo, PaperRepository)`, the protocol must be decorated with `@runtime_checkable`.
ResearchOps marks its core protocols with `@runtime_checkable` so tests can check that fakes have the required method names.
This is useful but limited.
Runtime protocol checks confirm method presence, not every detail of type annotations or method behavior.
A fake could have a `save` method that accepts the wrong kind of object, and a simple runtime check might not catch the full mismatch.
Therefore runtime checks are a quick safety net, not a replacement for meaningful service tests.
Use them to catch obvious shape errors.
Use unit tests to catch behavior errors.

### 6.5 Dependency inversion in plain language
The dependency inversion principle has two related ideas.
First, high-level modules should not depend on low-level modules.
Second, both should depend on abstractions.
In ResearchOps, `IngestionService` is high-level because it describes the ingestion use case.
`SQLitePaperRepository` is lower-level because it describes a specific storage mechanism.
The high-level service should not import the low-level repository.
Both should depend on the `PaperRepository` protocol.
The service depends on it by accepting it in the constructor.
The SQLite repository depends on it by matching its method shape.
The fake repository depends on it by matching the same method shape.
This is inversion because the high-level policy no longer points downward at details.
The detail plugs upward into a contract owned near the center of the system.

### 6.6 Clean architecture without buzzwords
Clean architecture can sound intimidating because diagrams often use circles and arrows.
For this project, the practical rule is simple: inner code should not import outer code.
Core is inner code.
Services are close to the center because they express application workflows.
Infrastructure is outer code because it talks to implementation details such as databases and parsers.
CLI code is outer code because it translates user commands into service calls and wires concrete objects together.
The allowed imports should mostly point inward.
Outer layers may know inner layers.
Inner layers should not know outer layers.
If an inner layer needs a capability from the outside world, it describes that capability as a protocol.
Then an outer adapter implements the protocol.

### 6.7 Hexagonal architecture: ports and adapters
Hexagonal architecture is another name for the same boundary idea.
A port is a place where the application asks for a capability.
An adapter is a concrete plug that provides the capability.
`PaperRepository` is a port.
`SQLitePaperRepository` is an adapter.
`FakePaperRepository` is also an adapter, but it exists for tests.
`DocumentParser` is a port.
A real PDF parser is an adapter.
`FakeDocumentParser` is a test adapter.
The application service talks to ports.
The outside world supplies adapters.
This naming helps you avoid putting infrastructure decisions in the middle of the application.

### 6.8 Why fakes are better than real infrastructure for unit tests
A unit test should be narrow.
If you are testing ingestion workflow decisions, the test should not fail because a database file could not be opened.
If you are testing parse-failure handling, the test should not need a corrupted real PDF file.
A fake lets the test control exactly what the collaborator does.
The fake repository can store papers in a dictionary.
The fake parser can return a prepared parsed document.
The fake parser can raise a prepared parsing error.
The service sees the same protocol shape either way.
This makes tests faster and more precise.
It also makes beginner debugging easier because fewer moving parts are involved.

### 6.9 Why protocols belong in `core/interfaces.py`
A protocol used by services and infrastructure must live somewhere both sides can import safely.
If the protocol lived in `storage/`, services would need to import storage to know the contract.
That would defeat the boundary.
If the protocol lived in `services/`, infrastructure might need to import services, creating another awkward direction.
ResearchOps places protocols in `core/` because core is the shared inner language.
Core already owns models such as `Paper` and `ParsedDocument`.
Core can describe interfaces using those models without depending on concrete adapters.
That location also gives learners one obvious file to inspect for project contracts.

## ResearchOps-specific application

The real protocol file is `src/researchops/core/interfaces.py`.
It imports `Path`, `Protocol`, `runtime_checkable`, and domain models from `researchops.core.models`.
It does not import SQLite.
It does not import PDF parser implementations.
It does not import CLI code.
That is the first architectural win.
The file defines `DocumentParser`, `PaperRepository`, `FailureRepository`, `SearchEngine`, and other project contracts.
For this week, focus on the protocols that support the current ingestion and search flows.
The most important ones are `DocumentParser`, `PaperRepository`, and `FailureRepository`.
`DocumentParser` says a parser must provide `parse(self, path: Path) -> ParsedDocument`.
The service does not care whether the parser reads a real PDF, returns a configured fake result, or raises a configured fake error.
It only cares about the `parse` method contract.
`PaperRepository` says a repository must provide `save`, `get`, `list_all`, `exists`, and `delete`.
The service does not care whether those operations use SQLite or a dictionary.
It cares that paper persistence behaves consistently.
`FailureRepository` says a failure store must provide `record_failure`, `list_failures`, and `clear_failures`.
The ingestion service uses that contract when parsing fails.
The fake implementations live in `tests/fakes/fake_repository.py`.
`FakePaperRepository` uses `self._papers: dict[str, Paper] = {}` to hold papers in memory.
`FakeFailureRepository` uses `self._failures: list[FailedDocument] = []` to hold failure records in memory.
`FakeDocumentParser` lets tests configure path-specific success or failure.
Those fakes are not throwaway hacks.
They are deliberately shaped like the real ports.
Because they implement the same protocols, services can use them without special test-only branches.
That last sentence is important.
If production code contains many `if testing:` branches, the design is usually leaking.
Protocols let tests supply different collaborators without changing service code.

Here is the intended dependency direction:

```text
CLI command code
    imports services and concrete adapters
    creates SQLite and parser objects
    passes them into services

services/
    imports core models, exceptions, and protocols
    does not import storage or parser implementations

core/
    imports only safe standard-library tools and core-owned definitions
    defines models, exceptions, value objects, and protocols

storage/ and parsing/
    import core models and exceptions
    implement concrete behavior
```

Read that block from top to bottom as responsibility, not superiority.
CLI code is not less important because it is outside.
Infrastructure is not less important because it is concrete.
The point is that concrete details should be replaceable without rewriting policy.

## Code examples with line-by-line explanation

### 8.1 A small protocol

```python
from pathlib import Path
from typing import Protocol

from researchops.core.models import ParsedDocument

class DocumentParser(Protocol):
    def parse(self, path: Path) -> ParsedDocument:
        ...
```

- **`from pathlib import Path`:** The protocol names `Path` because parsing starts from a file path object, not from a raw string.
- **`from typing import Protocol`:** This imports the standard-library tool used to define structural interfaces.
- **blank line after imports:** The blank line separates standard-library imports from project imports, making the example easier to scan.
- **`from researchops.core.models import ParsedDocument`:** The return type is a core model, so the protocol can describe project data without importing infrastructure.
- **blank line before class:** The blank line separates import setup from the protocol definition.
- **`class DocumentParser(Protocol):`:** This names the expected shape. Any parser-shaped object must provide the methods listed inside.
- **`def parse(self, path: Path) -> ParsedDocument:`:** This says a parser receives a `Path` and returns a `ParsedDocument`.
- **`...`:** The ellipsis means the protocol declares the method but does not implement parsing here.

The key beginner mistake is expecting `DocumentParser` to parse a file.
It does not.
It describes what a parser must be able to do.
A concrete class performs the actual parsing.

### 8.2 A repository protocol

```python
from typing import Protocol

from researchops.core.models import Paper

class PaperRepository(Protocol):
    def save(self, paper: Paper) -> None:
        ...

    def get(self, paper_id: str) -> Paper:
        ...

    def list_all(self) -> list[Paper]:
        ...

    def exists(self, paper_id: str) -> bool:
        ...

    def delete(self, paper_id: str) -> None:
        ...
```

- **`from typing import Protocol`:** The repository contract is a protocol, not a concrete base class.
- **`from researchops.core.models import Paper`:** The repository speaks in core domain objects rather than database rows.
- **`class PaperRepository(Protocol):`:** The class name describes a storage capability needed by services.
- **`def save(self, paper: Paper) -> None:`:** Saving receives a full `Paper` object and returns nothing on success.
- **`...` under `save`:** The protocol does not say whether saving means an INSERT statement, a dictionary assignment, or something else.
- **`def get(self, paper_id: str) -> Paper:`:** Retrieval receives a paper ID and returns one `Paper` if found.
- **`...` under `get`:** The protocol leaves missing-paper behavior to the contract documentation and concrete implementation.
- **`def list_all(self) -> list[Paper]:`:** Listing returns domain objects, not raw database rows.
- **`def exists(self, paper_id: str) -> bool:`:** Existence checking lets services skip duplicates without knowing how storage checks them.
- **`def delete(self, paper_id: str) -> None:`:** Deletion is part of the storage shape even though not every service uses it immediately.

Notice what is absent.
There is no `sqlite3.Connection` in this protocol.
There is no SQL string in this protocol.
There is no database path in this protocol.
The absence is the design.

### 8.3 A fake repository that satisfies the protocol

```python
class FakePaperRepository:
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

- **`class FakePaperRepository:`:** The fake does not need to inherit from `PaperRepository`; structural typing cares about methods.
- **`def __init__(self) -> None:`:** The fake initializes simple in-memory state for the test.
- **`self._papers: dict[str, Paper] = {}`:** The dictionary maps paper IDs to `Paper` objects, replacing a database table for unit tests.
- **`def save(self, paper: Paper) -> None:`:** The fake provides the same save method the protocol requires.
- **`if paper.id in self._papers:`:** The fake checks duplicates so service behavior resembles the real repository.
- **`raise DuplicatePaperError(paper.id)`:** The fake raises the same core exception as real storage should raise.
- **`self._papers[paper.id] = paper`:** A successful save stores the paper by ID.
- **`def get(self, paper_id: str) -> Paper:`:** The fake provides lookup by ID.
- **`if paper_id not in self._papers:`:** The fake handles missing records explicitly.
- **`raise PaperNotFoundError(paper_id)`:** Again, the fake uses a core exception so services see consistent failure behavior.
- **`return self._papers[paper_id]`:** On success, the fake returns the stored domain object.
- **`def list_all(self) -> list[Paper]:`:** The fake supports listing because search services need all papers.
- **`return list(self._papers.values())`:** The fake returns a new list so callers do not receive the dictionary view directly.
- **`def exists(self, paper_id: str) -> bool:`:** The fake supports duplicate checks without database queries.
- **`return paper_id in self._papers`:** Dictionary membership gives the answer simply and quickly.
- **`def delete(self, paper_id: str) -> None:`:** The fake completes the repository shape.
- **`self._papers.pop(paper_id, None)`:** Deleting a missing paper does not crash here because the method chooses silent removal semantics.

The fake is small, but it is not careless.
It uses core models.
It uses core exceptions.
It matches the public methods of the protocol.
That is why it is useful in service tests.

### 8.4 Constructor injection in a service

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

- **`from researchops.core.interfaces import ...`:** The service imports contracts from core, not concrete storage or parser classes.
- **`class IngestionService:`:** The service owns the ingestion use case, not the database implementation.
- **`def __init__(`:** The constructor declares what collaborators the service needs.
- **`self,`:** The instance being constructed is passed automatically by Python when methods run.
- **`parser: DocumentParser,`:** The service needs an object with a `parse` method matching the parser protocol.
- **`paper_repo: PaperRepository,`:** The service needs an object that can store and retrieve papers.
- **`failure_repo: FailureRepository,`:** The service needs an object that can record parsing failures.
- **`) -> None:`:** The constructor sets up the instance and does not return a separate value.
- **`self._parser = parser`:** The service stores the parser collaborator for later use.
- **`self._paper_repo = paper_repo`:** The service stores the paper repository collaborator for duplicate checks and saves.
- **`self._failure_repo = failure_repo`:** The service stores the failure repository collaborator for error reporting.

The constructor does not call `SQLitePaperRepository(...)`.
The constructor does not call a real parser class.
That absence is what makes unit tests clean.

### 8.5 A service method using a protocol

```python
def _ingest_one(self, path: Path, paper_id: str) -> Paper | None:
    try:
        doc = self._parser.parse(path)
    except ParsingError as exc:
        failure = FailedDocument(
            source_path=path,
            error_message=str(exc),
            error_type=type(exc).__name__,
        )
        self._failure_repo.record_failure(failure)
        return None

    paper = Paper(
        id=paper_id,
        title=extract_title(doc),
        source_path=str(path),
        text=clean_text(doc.raw_text),
        num_pages=doc.num_pages,
        file_size_bytes=doc.file_size_bytes,
    )
    self._paper_repo.save(paper)
    return paper
```

- **`def _ingest_one(self, path: Path, paper_id: str) -> Paper | None:`:** The helper returns a `Paper` on success or `None` when ingestion fails.
- **`try:`:** Parsing can fail, so the risky operation is placed in a controlled block.
- **`doc = self._parser.parse(path)`:** The service calls the parser protocol method without knowing the concrete parser class.
- **`except ParsingError as exc:`:** The service handles a known parsing failure in a predictable way.
- **`failure = FailedDocument(`:** A core model records what went wrong.
- **`source_path=path,`:** The failure keeps the file path that caused the problem.
- **`error_message=str(exc),`:** The exception becomes a readable message.
- **`error_type=type(exc).__name__,`:** The failure records the exception class name for debugging.
- **`self._failure_repo.record_failure(failure)`:** The service calls the failure repository protocol, not a concrete database method.
- **`return None`:** The service reports that no paper was created from this file.
- **`paper = Paper(`:** On success, parsed data is converted into the core `Paper` model.
- **`id=paper_id,`:** The stable paper ID comes from earlier workflow logic.
- **`title=extract_title(doc),`:** The service derives a title from parsed document metadata and text.
- **`source_path=str(path),`:** The paper stores the source path as text.
- **`text=clean_text(doc.raw_text),`:** The raw parsed text is cleaned before storage.
- **`num_pages=doc.num_pages,`:** The paper preserves the parsed page count.
- **`file_size_bytes=doc.file_size_bytes,`:** The paper preserves the parsed file size.
- **`self._paper_repo.save(paper)`:** The service saves through the repository protocol.
- **`return paper`:** The caller receives the created paper object.

This example is shortened for teaching.
The real file includes additional exception handling and logging.
The dependency lesson is the same: service logic calls protocol methods.

### 8.6 Runtime protocol check

```python
from researchops.core.interfaces import PaperRepository
from tests.fakes.fake_repository import FakePaperRepository

repo = FakePaperRepository()
assert isinstance(repo, PaperRepository)
```

- **`from researchops.core.interfaces import PaperRepository`:** The test imports the protocol from the core layer.
- **`from tests.fakes.fake_repository import FakePaperRepository`:** The test imports the fake adapter from the test support package.
- **`repo = FakePaperRepository()`:** The test creates the fake without opening a database.
- **`assert isinstance(repo, PaperRepository)`:** Because the protocol is runtime-checkable, this verifies the fake has the required method names.

Remember the limitation: this check is about shape, not full behavior.
You still need tests that save, retrieve, list, and handle duplicates.

### 8.7 A bad service import

```python
# Bad inside services/
from researchops.storage.sqlite_repository import SQLitePaperRepository
```

- **`# Bad inside services/`:** The comment identifies that this is a teaching anti-example, not a pattern to copy.
- **`from researchops.storage.sqlite_repository import SQLitePaperRepository`:** This makes service code depend on a concrete infrastructure adapter.
- **Why it is bad:** The service can no longer be understood or tested without storage details leaking into the middle of the application.
- **Better import:** `from researchops.core.interfaces import PaperRepository`.

### 8.8 Wiring at the outside edge

```python
repo = SQLitePaperRepository(db_path)
parser = PyMuPDFParser()
service = IngestionService(
    parser=parser,
    paper_repo=repo,
    failure_repo=repo,
)
```

- **`repo = SQLitePaperRepository(db_path)`:** Outer wiring code creates the real storage adapter.
- **`parser = PyMuPDFParser()`:** Outer wiring code creates the real parser adapter.
- **`service = IngestionService(`:** The service is created after its collaborators exist.
- **`parser=parser,`:** The real parser is passed into the parser port.
- **`paper_repo=repo,`:** The real repository is passed into the paper repository port.
- **`failure_repo=repo,`:** The same concrete repository can implement more than one protocol if it has both method sets.
- **`)`:** After construction, service code can run without knowing how the objects were built.

This wiring belongs at the edge of the application, not inside the service constructor.

## Common beginner mistakes

- **Mistake: Thinking a protocol is an implementation.**
  - Why it hurts: A protocol describes required methods; it does not store papers or parse documents.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Adding inheritance just to satisfy the protocol.**
  - Why it hurts: A class can match a protocol structurally without subclassing it.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Putting protocols in infrastructure.**
  - Why it hurts: If services import infrastructure to get a contract, the boundary is already broken.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Letting services construct concrete adapters.**
  - Why it hurts: A service that creates SQLite or parser objects cannot be cleanly tested with fakes.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Writing fakes that behave nothing like real adapters.**
  - Why it hurts: A fake should use the same core exceptions and method meanings where practical.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Trusting only `isinstance` checks.**
  - Why it hurts: Runtime protocol checks are helpful but cannot prove every behavior.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Using `object` instead of a protocol.**
  - Why it hurts: `object` hides the required collaborator shape from readers and tools.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Over-abstracting every tiny helper.**
  - Why it hurts: Use protocols for meaningful boundaries, not for every one-line function.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Importing from `tests/` in production code.**
  - Why it hurts: Production code must never depend on test fakes.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Moving business logic into CLI wiring.**
  - Why it hurts: The CLI should assemble objects and call services; services own workflow decisions.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Confusing dependency inversion with dependency injection.**
  - Why it hurts: Injection is a technique; inversion is the design principle behind the direction of dependencies.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.
- **Mistake: Ignoring exception contracts.**
  - Why it hurts: If fake and real repositories raise different exceptions, service tests become misleading.
  - Better move: identify the protocol, confirm the method shape, and keep the import direction inward.

A useful self-correction is to ask, "Could this service run with a fake?"
If the answer is no, find out whether the service is constructing or importing a concrete detail.
Another useful question is, "Could this fake be accidentally accepted but behave differently?"
If the answer is yes, add behavior tests around the important contract.

## Debugging guidance

Protocol and architecture bugs often appear as ordinary Python errors.
The trick is to classify the error correctly.

- **Symptom: `ImportError` or `ModuleNotFoundError`.**
  - First response: Check whether a layer imported a package it should not know about.
- **Symptom: `AttributeError: object has no attribute save`.**
  - First response: The passed object does not actually satisfy the repository shape.
- **Symptom: `TypeError` about missing arguments.**
  - First response: A fake method signature may not match the protocol method signature.
- **Symptom: A test unexpectedly opens a database.**
  - First response: The service or fixture may be constructing concrete storage instead of using a fake.
- **Symptom: A test needs a real PDF for a service unit test.**
  - First response: The parser dependency may not have been injected as a fake.
- **Symptom: A runtime protocol check fails.**
  - First response: Compare the fake method names to the protocol method names exactly.
- **Symptom: A runtime protocol check passes but behavior fails.**
  - First response: Remember that method presence is not the same as correct behavior.
- **Symptom: A circular import appears.**
  - First response: A protocol or model may have been placed in a layer that points the wrong direction.

Use this step-by-step debugging routine:
1. Copy the exact failing command or test name.
2. Read the first traceback line that belongs to ResearchOps code.
3. Read the last traceback line to identify the actual exception.
4. Ask which layer the failing file belongs to: core, services, infrastructure, CLI, or tests.
5. Check whether the failing import points inward or outward.
6. If an object is missing a method, open `core/interfaces.py` and compare method names.
7. If a fake behaves incorrectly, compare its exceptions and return values to the real adapter contract.
8. If a service constructs a concrete class, move construction to the composition root instead of patching around it.
9. Run only the narrow relevant check after the fix when validation is allowed for the task.
10. Write down the boundary lesson so you can recognize the same smell next time.

When debugging architecture, do not start by changing many files.
Start by drawing one arrow.
For example: `IngestionService -> PaperRepository` is good because service points to core.
`IngestionService -> SQLitePaperRepository` is bad because service points to infrastructure.
One wrong arrow often explains a large amount of pain.

## Design tradeoffs

- **Protocol versus concrete type:** A concrete type is simpler for a tiny script; a protocol is better when tests and future adapters need a stable contract.
- **Protocol versus abstract base class:** A protocol supports structural typing and avoids forcing inheritance; an abstract base class can be useful when shared implementation or explicit registration is needed.
- **Fake versus real adapter in unit tests:** A fake is faster and more focused; a real adapter is better for integration tests that verify persistence details.
- **Constructor injection versus creating inside methods:** Constructor injection makes dependencies visible; creating inside methods can hide coupling and make tests patch internals.
- **One large repository protocol versus smaller protocols:** A large protocol can be convenient but may force classes to implement unused methods; smaller protocols express needs more precisely.
- **Runtime checks versus static checks:** Runtime checks catch obvious shape mismatches during tests; static checks can catch broader type mismatches before execution.
- **Strict boundaries versus quick imports:** Quick imports may finish a feature faster today; strict boundaries reduce rewrite cost later.
- **Dictionary fake versus mock object:** A dictionary fake supports realistic behavior; a mock can be useful for call assertions but may overfit implementation details.

The most important tradeoff in Week 9 is cost now versus flexibility later.
Writing a protocol and fake takes more thought than directly importing SQLite.
The payoff appears every time you write a service test without disk setup.
The payoff appears every time you change infrastructure without rewriting service logic.
The payoff appears when a beginner can inspect constructor type hints and understand the service dependencies.
Do not abstract randomly.
Abstract at boundaries where one policy can have more than one implementation.
Storage is a boundary.
Parsing is a boundary.
A tiny local string formatting helper is usually not a boundary.

## Testing implications

Protocols change how you design tests.
Instead of building a database for every service test, you can build fakes.
Instead of collecting real PDFs for every parser-dependent workflow test, you can configure a fake parser.
This produces a healthier test pyramid.
Many unit tests use fakes and run quickly.
A smaller number of integration tests use real SQLite and real parser adapters.
The two kinds of tests answer different questions.
A unit test with fakes asks: does the service make the right decisions when collaborators behave in known ways?
An integration test with real infrastructure asks: does the adapter correctly talk to the outside mechanism?
Do not make one test answer every question.

Good service tests for this week should verify examples like these:
- An ingestion service stores a paper when the fake parser returns a parsed document.
- An ingestion service records a failure when the fake parser raises a parsing error.
- An ingestion service skips an existing paper when the fake repository says the ID exists.
- A search service can list papers through `PaperRepository` without knowing storage details.
- A fake repository raises the same duplicate-paper exception as the real repository contract.
- A fake repository passes a runtime protocol check for the methods it claims to implement.

Good adapter tests should verify different examples:
- `SQLitePaperRepository.save` actually writes a row to a temporary database location chosen by the test fixture.
- `SQLitePaperRepository.get` reconstructs a `Paper` domain object from stored data.
- `SQLitePaperRepository.exists` returns true after saving and false before saving.
- The real parser adapter returns a `ParsedDocument` for a controlled sample when parser testing is in scope.

A fake is not a substitute for all integration testing.
A fake cannot prove SQL schema correctness.
A fake cannot prove file parsing correctness.
A fake proves service behavior under controlled collaborator behavior.
That distinction is a professional testing skill.

When writing tests around protocols, avoid overusing mocks that assert every internal call.
If a test says "method `save` must be called exactly once before method `exists`", it may become brittle.
Prefer outcome-focused tests when possible.
For example, after ingestion succeeds, assert that the fake repository contains the expected paper.
After parsing fails, assert that the fake failure repository contains a failure record.
Those assertions match user-visible behavior more closely.

## Architecture implications

Protocols are small pieces of code with large architecture consequences.
They make the dependency graph easier to reason about.
Here is the boundary rule in compact form:

```text
core        -> no ResearchOps outer-layer imports
services    -> core only for contracts, models, and exceptions
storage     -> core, stdlib, and storage-specific tools
parsing     -> core, stdlib, and parsing-specific tools
cli         -> services plus concrete adapters for wiring
tests/fakes -> core contracts and models, no real infrastructure required
```

The service layer becomes stable because it is protected from detail churn.
If the SQLite schema changes, service constructor types do not change.
If parser internals change, service constructor types do not change.
If a fake becomes more capable, service constructor types do not change.
The protocols are the architectural seam.
A seam is a place where code can be separated, replaced, or tested independently.
ResearchOps needs seams because it is a learning system that grows week by week.
Without seams, every new topic would require rewriting earlier work.
With seams, later chapters can build adapters around stable service workflows.

Architecture also affects reading order.
When you enter an unfamiliar feature, read from the center outward.
Start with the core model and protocol names.
Then read the service that uses them.
Then read the concrete adapter that implements them.
Finally read the CLI command that wires them.
This order prevents you from drowning in implementation details too early.

Another implication is that architecture can be checked mechanically.
You can search for forbidden imports in `src/researchops/services`.
You can inspect whether `core/` imports infrastructure packages.
You can add tests that assert fakes satisfy runtime-checkable protocols.
You can review pull requests by asking whether a new dependency arrow points inward.
Architecture is not only a diagram in a document.
It is a set of code facts you can inspect.

## How this connects to AI engineering / ML research

Research and AI systems change often.
A paper-processing workflow might change its parser.
A storage layer might change its schema.
A search workflow might try a different ranking method later.
Evaluation code might need repeatable test data instead of live infrastructure.
Protocols help because they separate experimental change from stable workflow rules.
In research software, you want to compare approaches without rewriting the application each time.
That requires clear seams.
A repository protocol is a seam around stored papers.
A parser protocol is a seam around document extraction.
A service constructor is a seam where a real adapter or fake adapter can be plugged in.
This is especially important when experiments become expensive or slow.
You do not want every service test to repeat expensive work.
You want unit tests to verify orchestration quickly and integration tests to verify real adapters separately.
Clean architecture also helps reproducibility.
If a service depends on a clear protocol, you can build a fake with known data and rerun the same scenario many times.
That makes debugging easier when research results surprise you.
It also helps collaboration.
One person can improve a parser adapter while another person improves service logic, as long as the protocol remains stable.
Do not jump ahead to later project topics here.
The important Week 9 AI-engineering lesson is not a particular model.
The lesson is that research systems need boundaries because experiments change faster than core workflow concepts.
Protocols are one Pythonic way to create those boundaries.

## Mini quizzes

1. **Question:** What does `Protocol` describe: behavior shape or storage implementation?
   - **Answer:** Behavior shape.
2. **Question:** Does a class need to inherit from `PaperRepository` to satisfy it structurally?
   - **Answer:** No.
3. **Question:** Why should `PaperRepository` live in `core/interfaces.py` instead of `storage/`?
   - **Answer:** Services and infrastructure both need the contract without services importing infrastructure.
4. **Question:** What layer should create `SQLitePaperRepository` for a normal CLI run?
   - **Answer:** The outer wiring layer, such as CLI command code.
5. **Question:** What layer should call `paper_repo.save(paper)` during ingestion?
   - **Answer:** The service layer.
6. **Question:** What is the difference between `PaperRepository` and `SQLitePaperRepository`?
   - **Answer:** `PaperRepository` is the contract; `SQLitePaperRepository` is a concrete adapter.
7. **Question:** What is the difference between a fake and the real repository?
   - **Answer:** The fake stores data in controlled in-memory structures for tests; the real repository persists data with SQLite.
8. **Question:** What does `@runtime_checkable` allow?
   - **Answer:** It allows runtime checks such as `isinstance(obj, SomeProtocol)`.
9. **Question:** Can a runtime protocol check prove that duplicate handling is correct?
   - **Answer:** No; behavior tests are still needed.
10. **Question:** Why is `from researchops.storage.sqlite_repository import SQLitePaperRepository` suspicious inside `services/`?
   - **Answer:** It points from service logic to concrete infrastructure.
11. **Question:** What is dependency injection in this chapter?
   - **Answer:** Passing parser and repository collaborators into a service constructor.
12. **Question:** What is dependency inversion in this chapter?
   - **Answer:** Service policy and infrastructure details meet at core protocols instead of the service depending on concrete details.
13. **Question:** Which object should know SQL statements: service or SQLite adapter?
   - **Answer:** SQLite adapter.
14. **Question:** Which object should decide whether parsing failure records are created: service or CLI?
   - **Answer:** Service.
15. **Question:** What is a port?
   - **Answer:** A protocol/interface the application uses to request a capability.
16. **Question:** What is an adapter?
   - **Answer:** A concrete implementation that plugs into a port.

If you missed more than three, reread sections 4 through 8 before continuing.
If you got them right by memorizing words but cannot point to files, reread section 7.
If you can answer while pointing to real files, you are building the right mental model.

## Explain-it-aloud prompts

- Explain `typing.Protocol` to someone who knows functions and classes but has never heard the word interface.
- Explain why a fake repository can be used by `IngestionService` without changing service code.
- Explain why `core/interfaces.py` is a safer home for protocols than `storage/`.
- Explain the difference between the parser protocol and a concrete parser class.
- Explain the difference between dependency inversion and dependency injection.
- Explain why runtime protocol checks are useful but incomplete.
- Explain why services should not import SQLite repository classes directly.
- Explain how the CLI acts as the composition root for real application runs.
- Explain why a fake should raise the same core exceptions as a real adapter.
- Explain how protocols make unit tests faster and more focused.
- Explain how a wrong import direction can create architecture pain later.
- Explain what you would inspect if `isinstance(fake_repo, PaperRepository)` returned false.
- Explain why a protocol method uses `...` instead of real SQL or parsing code.
- Explain how ports and adapters describe the same idea as clean architecture boundaries.
- Explain what should happen when a parsing adapter changes but the `DocumentParser` protocol stays the same.

Use complete sentences when answering aloud.
Do not use the word "magic" as a substitute for explanation.
If you say "it just works," stop and name the protocol method that makes it work.

## What to memorize

- `Protocol` comes from `typing`.
- `runtime_checkable` allows limited `isinstance` checks against a protocol.
- Protocols in ResearchOps live in `src/researchops/core/interfaces.py`.
- Core must not import infrastructure layers.
- Services should depend on core protocols, models, and exceptions, not concrete adapters.
- Infrastructure implements protocols by providing the required methods.
- Fakes live in `tests/fakes/` and should match the protocol shapes they replace.
- Constructor injection means dependencies are passed in from outside.
- Dependency inversion means high-level policy depends on abstractions instead of low-level details.
- A port is the protocol; an adapter is the concrete implementation.
- Runtime protocol checks confirm method presence, not complete behavior.
- Unit tests use fakes for speed and control; integration tests use real adapters for concrete behavior.

Memorization is not enough, but it helps you move quickly while reading code.
The most important memorized sentence is: **services depend on protocols, not concretes**.
The second most important sentence is: **outer layers wire concrete implementations**.

## What to understand deeply

- **A type hint is communication:** When a constructor says `paper_repo: PaperRepository`, it tells every reader what capability is required.
- **A protocol is a boundary object:** It sits between policy and implementation so both sides can evolve more safely.
- **A fake is an adapter too:** The fake plugs into the same port as the real adapter, just for tests.
- **Architecture is import direction:** Folder names help, but imports reveal the real dependency graph.
- **Behavior matters beyond shape:** Matching method names is necessary but not enough; exceptions and return meanings must align.
- **Small abstractions can protect large workflows:** A few method signatures can keep service logic independent of database and parser details.
- **Clean architecture is about change:** The point is not ceremony; the point is making likely changes safer.
- **Testing and architecture reinforce each other:** If a service is hard to test with fakes, the boundary may be wrong.

Deep understanding means you can predict consequences.
If someone adds a storage import inside a service, you should predict slower or more brittle tests.
If someone changes a protocol method name, you should predict that real and fake adapters must be updated together.
If someone puts SQL inside a service, you should predict that storage concerns are leaking into workflow code.
If someone creates a fake that never raises duplicate errors, you should predict that duplicate-handling service tests may be misleading.

## What not to worry about yet

- Do not worry about advanced static type checker configuration in this chapter.
- Do not worry about generating protocols automatically.
- Do not worry about plugin systems or dynamic adapter loading.
- Do not worry about turning every helper function into a protocol.
- Do not worry about web application wiring here.
- Do not worry about asynchronous application design here.
- Do not worry about future research-model implementation details here.
- Do not worry about replacing SQLite in this chapter.
- Do not worry about building a full dependency-injection framework.
- Do not worry about perfect theoretical definitions of every architecture school.
- Do not worry about inheritance unless a specific class needs shared implementation.
- Do not worry about optimizing fake repositories for huge datasets.

The Week 9 target is narrower and more valuable than it may seem.
You need to understand the current ResearchOps contracts.
You need to understand how services use those contracts.
You need to understand how real and fake adapters satisfy those contracts.
You need to understand why import direction matters.
If you can do those things, you are ready to move forward.

## Bridge to next week

Week 9 gives ResearchOps cleaner seams.
Those seams make the next lessons safer because future work can plug into existing boundaries instead of rewriting the center of the system.
When a later chapter needs a new adapter, you will know to ask which protocol it satisfies.
When a later chapter needs a new service behavior, you will know to ask which dependencies should be passed in.
When a later chapter needs tests, you will know whether the test should use a fake or a real adapter.
This is how a learning project becomes a maintainable project.
You are no longer only asking, "Does this function work?"
You are also asking, "Can this part change without forcing unrelated parts to change?"
That question is the beginning of software design.
Carry forward these habits:
- Look for constructor dependencies before reading method bodies.
- Check whether services import only inward-facing contracts and models.
- Keep fakes small but behaviorally honest.
- Use protocols at meaningful boundaries.
- Draw dependency arrows when a design feels confusing.
- Prefer clear seams over clever shortcuts.

Before leaving this chapter, make sure you can explain the complete path of one ingestion scenario.
Start at the CLI wiring code that creates real adapters.
Move into `IngestionService`, which receives protocol-shaped collaborators.
Follow the call to `self._parser.parse(path)`.
Follow the creation of a `Paper` model.
Follow the call to `self._paper_repo.save(paper)`.
Then repeat the same story using fakes in a unit test.
If both stories use the same service code, the architecture is doing its job.
That is the lesson of Week 9.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 09 — Protocols and Clean Architecture:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
