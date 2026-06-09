"""Protocols (interfaces) for the ResearchOps core layer.

Using typing.Protocol lets us define abstract "contracts" without
forcing concrete inheritance. This supports:
- dependency inversion (services depend on protocols, not implementations)
- easy fake/stub creation for tests
- clear module boundary documentation

These protocols live in core/ and must NOT import infrastructure.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from researchops.core.models import (
    FailedDocument,
    Paper,
    ParsedDocument,
    SearchResult,
)


@runtime_checkable
class DocumentParser(Protocol):
    """Can parse a PDF file into a ParsedDocument."""

    def parse(self, path: Path) -> ParsedDocument:
        """Parse a single file and return its content + metadata."""
        ...


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


@runtime_checkable
class FailureRepository(Protocol):
    """Can persist and retrieve FailedDocument records."""

    def record_failure(self, failure: FailedDocument) -> None:
        """Persist a failure record."""
        ...

    def list_failures(self) -> list[FailedDocument]:
        """Return all recorded failures."""
        ...

    def clear_failures(self) -> None:
        """Remove all failure records."""
        ...


@runtime_checkable
class SearchEngine(Protocol):
    """Can search over stored papers."""

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Return papers matching the query, ordered by relevance."""
        ...

    def index_paper(self, paper: Paper) -> None:
        """Add (or update) a paper in the search index."""
        ...


@runtime_checkable
class EmbeddingModel(Protocol):
    """Can produce embeddings from text."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return a list of embedding vectors for the given texts."""
        ...

    @property
    def dimension(self) -> int:
        """Return the embedding dimensionality."""
        ...


@runtime_checkable
class ExperimentRepository(Protocol):
    """Can persist and retrieve ML experiment records."""

    def create_run(self, name: str, params: dict[str, str]) -> str:
        """Create a new experiment run. Returns the run ID."""
        ...

    def log_metric(self, run_id: str, key: str, value: float) -> None:
        """Record a metric value for a run."""
        ...

    def get_run(self, run_id: str) -> dict[str, object] | None:
        """Return run data including params and metrics."""
        ...

    def list_runs(self) -> list[dict[str, object]]:
        """Return all experiment runs."""
        ...
