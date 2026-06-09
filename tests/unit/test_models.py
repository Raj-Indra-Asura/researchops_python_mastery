"""Unit tests for core domain models."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from researchops.core.models import (
    FailedDocument,
    IngestionResult,
    Paper,
    PaperId,
    ParsedDocument,
)


class TestPaperId:
    def test_from_path_returns_stable_id(self, tmp_path: Path) -> None:
        """Same path always produces the same ID."""
        pdf = tmp_path / "paper.pdf"
        pdf.touch()
        id1 = PaperId.from_path(pdf)
        id2 = PaperId.from_path(pdf)
        assert id1 == id2

    def test_from_different_paths_differ(self, tmp_path: Path) -> None:
        pdf_a = tmp_path / "a.pdf"
        pdf_b = tmp_path / "b.pdf"
        pdf_a.touch()
        pdf_b.touch()
        assert PaperId.from_path(pdf_a) != PaperId.from_path(pdf_b)

    def test_str_representation(self, tmp_path: Path) -> None:
        pdf = tmp_path / "paper.pdf"
        pdf.touch()
        pid = PaperId.from_path(pdf)
        assert str(pid) == pid.value
        assert len(pid.value) == 16


class TestPaper:
    def _make_paper(self, text: str = "hello world") -> Paper:
        return Paper(
            id="abc123",
            title="Test Paper",
            source_path="/tmp/test.pdf",
            text=text,
            num_pages=5,
            file_size_bytes=1024,
        )

    def test_word_count(self) -> None:
        paper = self._make_paper("one two three")
        assert paper.word_count() == 3

    def test_word_count_empty(self) -> None:
        paper = self._make_paper("")
        assert paper.word_count() == 0

    def test_is_empty_true(self) -> None:
        paper = self._make_paper("   ")
        assert paper.is_empty() is True

    def test_is_empty_false(self) -> None:
        paper = self._make_paper("some text")
        assert paper.is_empty() is False

    def test_default_created_at_is_datetime(self) -> None:
        paper = self._make_paper()
        assert isinstance(paper.created_at, datetime)

    def test_default_tags_is_empty_list(self) -> None:
        paper = self._make_paper()
        assert paper.tags == []


class TestParsedDocument:
    def test_is_empty_when_blank(self, tmp_path: Path) -> None:
        doc = ParsedDocument(
            source_path=tmp_path / "x.pdf",
            raw_text="   ",
            num_pages=1,
            file_size_bytes=100,
        )
        assert doc.is_empty() is True

    def test_is_not_empty_with_content(self, tmp_path: Path) -> None:
        doc = ParsedDocument(
            source_path=tmp_path / "x.pdf",
            raw_text="Some text",
            num_pages=1,
            file_size_bytes=100,
        )
        assert doc.is_empty() is False


class TestFailedDocument:
    def test_summary_contains_filename(self, tmp_path: Path) -> None:
        failure = FailedDocument(
            source_path=tmp_path / "broken.pdf",
            error_message="cannot read",
            error_type="ParsingError",
        )
        assert "broken.pdf" in failure.summary()
        assert "ParsingError" in failure.summary()


class TestIngestionResult:
    def test_total_counts_all_types(self, tmp_path: Path) -> None:
        result = IngestionResult(
            run_id="r1",
            directory=tmp_path,
            started_at=datetime.utcnow(),
        )
        result.successes.append(
            Paper(id="1", title="T", source_path="/x", text="t", num_pages=1, file_size_bytes=1)
        )
        result.failures.append(
            FailedDocument(
                source_path=tmp_path / "f.pdf", error_message="err", error_type="E"
            )
        )
        result.skipped.append(tmp_path / "s.pdf")
        assert result.total == 3

    def test_success_rate_zero_when_no_total(self, tmp_path: Path) -> None:
        result = IngestionResult(
            run_id="r1", directory=tmp_path, started_at=datetime.utcnow()
        )
        assert result.success_rate == 0.0
