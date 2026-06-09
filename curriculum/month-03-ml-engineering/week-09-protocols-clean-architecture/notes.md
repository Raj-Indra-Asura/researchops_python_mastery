# Notes - Week 09 Protocols and Clean Architecture

As projects grow, the biggest source of pain is often not syntax but coupling. Coupling means one part of the system knows too much about another part. If your ingestion service directly imports SQLite details, it becomes harder to test and harder to reuse. Clean architecture tries to reduce that pain by making core business logic depend on stable abstractions instead of fragile implementation details.

In Python, `typing.Protocol` is a lightweight way to describe an interface by behavior rather than inheritance.

```python
from typing import Protocol


class ParsedDocumentRepository(Protocol):
    def save_parsed_document(self, paper: Paper, document: ParsedDocument) -> None:
        ...
```

Anything with a compatible `save_parsed_document` method satisfies this protocol, even if it does not inherit from a base class. That is powerful because your service can depend on the protocol, and the concrete implementation can vary.

```python
class IngestionService:
    def __init__(self, repository: ParsedDocumentRepository, parser: ParserProtocol) -> None:
        self.repository = repository
        self.parser = parser
```

This is dependency inversion in practice. The high-level service no longer depends directly on `SQLiteRepository`; both depend on an abstraction.

A useful mental model is ports and adapters. A port is the interface the application expects. An adapter is the concrete implementation that plugs into that port. In this repo:
- service code is the application layer
- protocol definitions are the ports
- SQLite repositories and PDF parsers are adapters
- CLI and API layers are external interfaces

Fake repositories are simple in-memory implementations used for testing.

```python
class FakeRepository:
    def __init__(self) -> None:
        self.saved: list[ParsedDocument] = []

    def save_parsed_document(self, paper: Paper, document: ParsedDocument) -> None:
        self.saved.append(document)
```

With a fake, you can test service behavior without setting up a database. That makes unit tests faster and more focused. Integration tests still matter, but now they can be reserved for the places where infrastructure really matters.

Clean architecture does not mean creating many layers just to sound sophisticated. It means being intentional about direction of dependency. Domain models should not know about SQL tables. Application services should not need a shell or HTTP request object. Infrastructure code should be replaceable.

One common refactor this week is moving construction logic to the outer edge. For example, the CLI may build a real `SQLiteRepository`, then pass it into `IngestionService`. The service itself should not call `sqlite3.connect()`.

Protocols also improve readability. When you annotate a dependency as `ParsedDocumentRepository`, you are telling future readers what capability the service needs. That is more informative than tying the service to a specific class name.

Testing architecture means checking substitutability. If the same service test passes with a fake repository and the integration test passes with the SQLite repository, your boundary is probably healthy.

The larger lesson is strategic: abstractions are useful when they reduce change cost. If later you add a Postgres repository, API-backed search index, or job queue, services built around protocols will adapt more easily. This week prepares the codebase for that future.
