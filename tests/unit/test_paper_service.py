"""Unit tests for services/paper_service.py."""

from __future__ import annotations

import pytest

from researchops.core.exceptions import PaperNotFoundError
from researchops.core.models import Paper
from researchops.services.paper_service import PaperService
from tests.fakes.fake_repository import FakePaperRepository


def _make_paper(
    paper_id: str = "p1",
    title: str = "Test Paper",
    text: str = "hello world " * 10,
    num_pages: int = 5,
) -> Paper:
    return Paper(
        id=paper_id,
        title=title,
        source_path=f"/tmp/{paper_id}.pdf",
        text=text,
        num_pages=num_pages,
        file_size_bytes=1024,
    )


@pytest.fixture()
def repo() -> FakePaperRepository:
    return FakePaperRepository()


@pytest.fixture()
def service(repo: FakePaperRepository) -> PaperService:
    return PaperService(paper_repo=repo)


class TestGetPaper:
    def test_returns_paper_by_id(self, repo: FakePaperRepository, service: PaperService) -> None:
        paper = _make_paper("abc")
        repo.save(paper)
        result = service.get_paper("abc")
        assert result.id == "abc"

    def test_raises_when_not_found(self, service: PaperService) -> None:
        with pytest.raises(PaperNotFoundError):
            service.get_paper("nonexistent")


class TestListPapers:
    def test_empty_when_no_papers(self, service: PaperService) -> None:
        assert service.list_papers() == []

    def test_returns_all_saved_papers(
        self, repo: FakePaperRepository, service: PaperService
    ) -> None:
        repo.save(_make_paper("p1"))
        repo.save(_make_paper("p2"))
        result = service.list_papers()
        assert len(result) == 2


class TestStats:
    def test_empty_stats(self, service: PaperService) -> None:
        stats = service.stats()
        assert stats["total_papers"] == 0
        assert stats["total_words"] == 0
        assert stats["total_pages"] == 0

    def test_counts_papers_words_pages(
        self, repo: FakePaperRepository, service: PaperService
    ) -> None:
        repo.save(_make_paper("p1", text="word " * 20, num_pages=3))
        repo.save(_make_paper("p2", text="word " * 10, num_pages=2))
        stats = service.stats()
        assert stats["total_papers"] == 2
        assert stats["total_words"] == 30
        assert stats["total_pages"] == 5
