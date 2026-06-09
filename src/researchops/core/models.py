"""Core domain models for ResearchOps.

These models are the heart of the application. They must not import
anything from storage, CLI, API, ML, or workers — only stdlib and
each other.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path


class IngestionStatus(StrEnum):
    """Possible outcomes for a single document ingestion attempt."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class PaperId:
    """Value object: a stable, content-derived identifier for a paper.

    Derived from the SHA-256 of the source file path (normalised).
    This means re-ingesting the same file always yields the same ID.
    """

    value: str

    @classmethod
    def from_path(cls, path: Path) -> PaperId:
        """Create a PaperId by hashing the absolute, resolved path."""
        digest = hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]
        return cls(value=digest)

    def __str__(self) -> str:
        return self.value


@dataclass
class Paper:
    """Represents a research paper stored in the system.

    A Paper is created once a PDF has been successfully parsed and
    persisted. It holds both the raw extracted text and lightweight
    metadata so consumers don't need to re-parse the original file.
    """

    id: str
    title: str
    source_path: str
    text: str
    num_pages: int
    file_size_bytes: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    author: str | None = None
    abstract: str | None = None
    tags: list[str] = field(default_factory=list)

    def word_count(self) -> int:
        """Return approximate word count of extracted text."""
        return len(self.text.split())

    def is_empty(self) -> bool:
        """True when extracted text has no meaningful content."""
        return len(self.text.strip()) == 0


@dataclass
class ParsedDocument:
    """Raw result of parsing a single PDF file.

    This is an intermediate object produced by the parsing layer.
    It has NOT yet been validated or persisted — it's just what
    the parser found.
    """

    source_path: Path
    raw_text: str
    num_pages: int
    file_size_bytes: int
    metadata: dict[str, str] = field(default_factory=dict)

    def is_empty(self) -> bool:
        return len(self.raw_text.strip()) == 0


@dataclass
class FailedDocument:
    """Records a document that could not be ingested, and why.

    Tracking failures is just as important as tracking successes.
    This object lets users see which papers are missing and debug
    the root cause.
    """

    source_path: Path
    error_message: str
    error_type: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)

    def summary(self) -> str:
        return f"[{self.error_type}] {self.source_path.name}: {self.error_message}"


@dataclass
class IngestionResult:
    """Summary of a full ingestion run over a directory of PDFs."""

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

    def is_complete(self) -> bool:
        return self.finished_at is not None


@dataclass
class SearchResult:
    """A single search hit with its relevance score."""

    paper: Paper
    score: float
    snippet: str = ""

    def __lt__(self, other: SearchResult) -> bool:
        return self.score < other.score
