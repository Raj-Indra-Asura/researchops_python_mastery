"""Fake repository implementations for use in tests.

These fakes implement the PaperRepository and FailureRepository protocols
without touching a database. They are safe to use in unit tests where
you don't want disk I/O.

Usage:
    repo = FakePaperRepository()
    service = IngestionService(parser=..., paper_repo=repo, failure_repo=repo)
"""

from __future__ import annotations

from pathlib import Path

from researchops.core.exceptions import DuplicatePaperError, PaperNotFoundError
from researchops.core.models import FailedDocument, Paper


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


class FakeFailureRepository:
    """In-memory failure repository for testing."""

    def __init__(self) -> None:
        self._failures: list[FailedDocument] = []

    def record_failure(self, failure: FailedDocument) -> None:
        self._failures.append(failure)

    def list_failures(self) -> list[FailedDocument]:
        return list(self._failures)

    def clear_failures(self) -> None:
        self._failures.clear()


class FakeDocumentParser:
    """A configurable fake parser for testing.

    Usage:
        parser = FakeDocumentParser()
        parser.set_result(path, ParsedDocument(...))
        # or
        parser.set_error(path, ParsingError("bad file"))
    """

    def __init__(self) -> None:
        from researchops.core.models import ParsedDocument

        self._results: dict[str, ParsedDocument] = {}
        self._errors: dict[str, Exception] = {}

    def set_result(self, path: Path, doc: object) -> None:  # type: ignore[override]
        self._results[str(path)] = doc  # type: ignore[assignment]

    def set_error(self, path: Path, error: Exception) -> None:
        self._errors[str(path)] = error

    def parse(self, path: Path) -> object:
        key = str(path)
        if key in self._errors:
            raise self._errors[key]
        if key in self._results:
            return self._results[key]
        from researchops.core.exceptions import ParsingError

        raise ParsingError(f"FakeParser: no result configured for {path}")
