# Notes - Week 03 OOP and Domain Modeling

Object-oriented programming is most useful when it helps your code speak the language of the problem. If a paper in your system always has a path, title, and source identifier, that should probably be modeled as a `Paper` object rather than as a dictionary with loosely remembered keys.

Python's `@dataclass` decorator is a practical way to define data-rich classes. It generates common methods such as `__init__`, `__repr__`, and equality behavior for you.

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Paper:
    source_path: Path
    title: str
    source_type: str = "pdf"
```

This is easier to read and maintain than manually writing a long `__init__` for every model. `slots=True` is optional, but it can reduce memory use and prevent accidental new attributes.

Domain modeling means deciding which objects deserve names and which rules belong on those objects. For example, a parsed document is more than text. It may include page count, extracted metadata, and normalized content.

```python
from dataclasses import dataclass, field


@dataclass
class ParsedDocument:
    paper_id: str
    title: str
    text: str
    keywords: list[str] = field(default_factory=list)

    def word_count(self) -> int:
        return len(self.text.split())
```

Notice that behavior can live with data. `word_count()` belongs naturally on a parsed document because it depends on the document's text. But not every helper needs to become a method. If a function does not need object state, a module-level function is often simpler.

Separate success and failure models when the states are truly different. A failed parse might not have text at all, but it should still capture the path and failure reason.

```python
@dataclass
class FailedDocument:
    source_path: str
    reason: str
    retryable: bool = False
```

If you tried to force failures into the same model as successes, you would end up with many optional fields and messy conditionals. Distinct models make downstream logic cleaner.

An `IngestionResult` model can aggregate lists of successes and failures:

```python
@dataclass
class IngestionResult:
    parsed_documents: list[ParsedDocument]
    failed_documents: list[FailedDocument]

    @property
    def success_count(self) -> int:
        return len(self.parsed_documents)
```

This is helpful because services can return one object describing the full run instead of several parallel lists.

A key idea in domain modeling is invariants. An invariant is a rule that should always be true. For example, a `Paper` should probably not have an empty title. You can enforce simple invariants in `__post_init__`:

```python
@dataclass
class Paper:
    source_path: Path
    title: str

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Paper title cannot be empty")
```

Testing models is not only about construction. Test behavior and meaning. If two `Paper` objects with the same fields should compare equal, assert that. If `word_count()` should ignore repeated spaces, test that. If `FailedDocument.retryable` should default to `False`, test that too.

The larger lesson: objects are not about making everything into classes. They are about building a shared vocabulary. Once your codebase speaks in terms of `Paper`, `ParsedDocument`, and `IngestionResult`, later features like storage, search, and ML become easier to design because they build on stable concepts instead of shapeless dictionaries.
