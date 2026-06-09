"""Integration tests for the SQLite paper repository."""

from __future__ import annotations

from pathlib import Path

import pytest

from researchops.core.exceptions import DuplicatePaperError, PaperNotFoundError
from researchops.core.models import FailedDocument, Paper
from researchops.storage.sqlite_repository import SQLitePaperRepository


@pytest.fixture
def repo(tmp_path: Path) -> SQLitePaperRepository:
    """Create a fresh in-memory (tmp_path) SQLite repository for each test."""
    return SQLitePaperRepository(tmp_path / "test.db")


def _make_paper(paper_id: str = "paper1", title: str = "Test Paper") -> Paper:
    return Paper(
        id=paper_id,
        title=title,
        source_path=f"/tmp/{paper_id}.pdf",
        text="Some extracted text about machine learning.",
        num_pages=10,
        file_size_bytes=2048,
    )


class TestSQLitePaperRepository:
    def test_save_and_get(self, repo: SQLitePaperRepository) -> None:
        paper = _make_paper()
        repo.save(paper)
        retrieved = repo.get("paper1")
        assert retrieved.id == "paper1"
        assert retrieved.title == "Test Paper"

    def test_get_raises_when_not_found(self, repo: SQLitePaperRepository) -> None:
        with pytest.raises(PaperNotFoundError):
            repo.get("nonexistent")

    def test_save_raises_on_duplicate(self, repo: SQLitePaperRepository) -> None:
        paper = _make_paper()
        repo.save(paper)
        with pytest.raises(DuplicatePaperError):
            repo.save(paper)

    def test_exists(self, repo: SQLitePaperRepository) -> None:
        paper = _make_paper()
        assert repo.exists("paper1") is False
        repo.save(paper)
        assert repo.exists("paper1") is True

    def test_list_all(self, repo: SQLitePaperRepository) -> None:
        repo.save(_make_paper("p1", "First"))
        repo.save(_make_paper("p2", "Second"))
        papers = repo.list_all()
        assert len(papers) == 2
        titles = {p.title for p in papers}
        assert titles == {"First", "Second"}

    def test_delete(self, repo: SQLitePaperRepository) -> None:
        repo.save(_make_paper())
        repo.delete("paper1")
        assert repo.exists("paper1") is False

    def test_record_and_list_failures(self, repo: SQLitePaperRepository) -> None:
        failure = FailedDocument(
            source_path=Path("/tmp/broken.pdf"),
            error_message="Cannot read file",
            error_type="ParsingError",
        )
        repo.record_failure(failure)
        failures = repo.list_failures()
        assert len(failures) == 1
        assert failures[0].error_type == "ParsingError"

    def test_clear_failures(self, repo: SQLitePaperRepository) -> None:
        repo.record_failure(
            FailedDocument(
                source_path=Path("/tmp/x.pdf"),
                error_message="err",
                error_type="E",
            )
        )
        repo.clear_failures()
        assert repo.list_failures() == []
