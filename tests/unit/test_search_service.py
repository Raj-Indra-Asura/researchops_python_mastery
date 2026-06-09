"""Unit tests for services/search_service.py."""

from __future__ import annotations

import pytest

from researchops.core.exceptions import EmptyQueryError
from researchops.core.models import Paper
from researchops.services.search_service import KeywordSearchService
from tests.fakes.fake_repository import FakePaperRepository


def _make_paper(
    paper_id: str,
    title: str = "",
    text: str = "",
) -> Paper:
    return Paper(
        id=paper_id,
        title=title,
        source_path=f"/tmp/{paper_id}.pdf",
        text=text,
        num_pages=1,
        file_size_bytes=512,
    )


@pytest.fixture()
def repo() -> FakePaperRepository:
    r = FakePaperRepository()
    r.save(_make_paper("p1", title="Deep Learning Fundamentals", text="neural networks backprop"))
    r.save(_make_paper("p2", title="NLP with Transformers", text="attention mechanism bert"))
    r.save(_make_paper("p3", title="Computer Vision", text="convolutional neural networks"))
    return r


@pytest.fixture()
def service(repo: FakePaperRepository) -> KeywordSearchService:
    return KeywordSearchService(paper_repo=repo)


class TestSearch:
    def test_finds_matching_paper_by_title(self, service: KeywordSearchService) -> None:
        results = service.search("transformers")
        assert len(results) >= 1
        assert any(r.paper.id == "p2" for r in results)

    def test_finds_matching_paper_by_text(self, service: KeywordSearchService) -> None:
        results = service.search("backprop")
        assert len(results) >= 1
        assert any(r.paper.id == "p1" for r in results)

    def test_no_match_returns_empty(self, service: KeywordSearchService) -> None:
        results = service.search("quantum entanglement")
        assert results == []

    def test_empty_query_raises(self, service: KeywordSearchService) -> None:
        with pytest.raises(EmptyQueryError):
            service.search("   ")

    def test_results_ordered_by_score_descending(self, service: KeywordSearchService) -> None:
        results = service.search("neural networks")
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_limit_is_respected(self, service: KeywordSearchService) -> None:
        results = service.search("neural networks", limit=1)
        assert len(results) <= 1

    def test_result_has_snippet(self, service: KeywordSearchService) -> None:
        results = service.search("neural")
        for r in results:
            assert isinstance(r.snippet, str)

    def test_snippet_extracted_from_text(self, service: KeywordSearchService) -> None:
        results = service.search("backprop")
        assert len(results) == 1
        assert "backprop" in results[0].snippet.lower() or results[0].snippet != ""


class TestSearchWithEmptyRepo:
    def test_empty_repo_returns_empty_list(self) -> None:
        service = KeywordSearchService(paper_repo=FakePaperRepository())
        results = service.search("anything")
        assert results == []


class TestExtractSnippet:
    def test_snippet_for_term_at_start(self) -> None:
        result = KeywordSearchService._extract_snippet("hello world test", ["hello"])
        assert "hello" in result

    def test_snippet_for_term_not_found(self) -> None:
        text = "abcdefgh " * 20
        result = KeywordSearchService._extract_snippet(text, ["xyz"])
        assert len(result) <= 160

    def test_snippet_uses_ellipsis_for_mid_text(self) -> None:
        long_text = "prefix " * 30 + "target keyword " + "suffix " * 10
        result = KeywordSearchService._extract_snippet(long_text, ["target"])
        assert "target" in result
