# Notes - Week 03 OOP and Domain Modeling

Object-oriented programming is most useful when it helps your code speak the language of the problem. The core domain of ResearchOps revolves around a small set of objects that every other layer — CLI, storage, ML, API — depends on. Those objects live in `src/researchops/core/` and must not import from any infrastructure layer (no database, no PDF library, no HTTP client).

## The core/ sub-package

```
src/researchops/core/
├── __init__.py
├── models.py        ← Paper, ParsedDocument, FailedDocument, IngestionResult, SearchResult
├── exceptions.py    ← ResearchOpsError and sub-classes
├── interfaces.py    ← typing.Protocol definitions (Week 9)
└── value_objects.py ← PaperId, Query, Tag
```

## Dataclasses

Python's `@dataclass` decorator generates `__init__`, `__repr__`, and equality methods from field declarations. It is the right choice for data-rich objects where behaviour is minimal.

The actual `Paper` in `core/models.py` looks like this:

```python
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Paper:
    id: str
    title: str
    source_path: str       # stored as string for JSON-serialisation convenience
    text: str
    num_pages: int
    file_size_bytes: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    author: str | None = None
    abstract: str | None = None
    tags: list[str] = field(default_factory=list)

    def word_count(self) -> int:
        return len(self.text.split())

    def is_empty(self) -> bool:
        return len(self.text.strip()) == 0
```

`field(default_factory=list)` is important. If you write `tags: list[str] = []` instead, every `Paper` instance shares the same list object — a notorious dataclass pitfall.

## ParsedDocument — the intermediate object

`ParsedDocument` is what the parsing layer returns before the ingestion service saves anything. It has a `Path` (not a string) because it is still in-memory and hasn't been serialised yet.

```python
@dataclass
class ParsedDocument:
    source_path: Path
    raw_text: str
    num_pages: int
    file_size_bytes: int
    metadata: dict[str, str] = field(default_factory=dict)

    def is_empty(self) -> bool:
        return len(self.raw_text.strip()) == 0
```

## FailedDocument — tracking what went wrong

ResearchOps tracks failures with the same discipline as successes. The `FailedDocument` object stores the source path, error type, and message, plus a `summary()` method for display.

```python
@dataclass
class FailedDocument:
    source_path: Path
    error_message: str
    error_type: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)

    def summary(self) -> str:
        return f"[{self.error_type}] {self.source_path.name}: {self.error_message}"
```

## IngestionResult — aggregating an entire run

`IngestionResult` collects everything that happened during one `ingest_directory` run. Using a single result object means downstream code (CLI, API, logging) reads one value instead of managing three parallel lists.

```python
@dataclass
class IngestionResult:
    run_id: str
    directory: Path
    started_at: datetime
    finished_at: datetime | None = None
    successes: list[Paper] = field(default_factory=list)
    failures: list[FailedDocument] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.successes) + len(self.failures) + len(self.skipped)

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return len(self.successes) / self.total
```

## PaperId — a stable value object

`PaperId` is a `frozen=True` dataclass (a value object). It derives a 16-character hex ID from the SHA-256 of the resolved file path. This means the same PDF always gets the same ID, which prevents duplicates during re-ingestion.

```python
import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PaperId:
    value: str

    @classmethod
    def from_path(cls, path: Path) -> "PaperId":
        digest = hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]
        return cls(value=digest)

    def __str__(self) -> str:
        # Returns the raw hex string so str(paper_id) and f"{paper_id}" give
        # "abc123" rather than the dataclass repr "PaperId(value='abc123')".
        return self.value
```

## Testing models

Model tests go beyond construction. Test the behaviour and meaning of methods. For `Paper`, test that `word_count()` counts words correctly and that `is_empty()` returns `True` for whitespace-only text. For `IngestionResult`, test that `total` sums all three lists and that `success_rate` returns `0.0` when nothing was processed. You can see existing tests in `tests/unit/test_models.py`.

The larger lesson: once the codebase speaks in terms of `Paper`, `ParsedDocument`, and `IngestionResult`, later features like storage, search, and ML become easier to design because they build on stable concepts instead of shapeless dictionaries.
