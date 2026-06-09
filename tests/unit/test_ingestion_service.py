"""Unit tests for services/ingestion_service.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from researchops.core.exceptions import ParsingError
from researchops.core.models import ParsedDocument
from researchops.services.ingestion_service import IngestionService
from tests.fakes.fake_repository import (
    FakeDocumentParser,
    FakeFailureRepository,
    FakePaperRepository,
)


def _parsed_doc(path: Path, text: str = "Some paper text about neural networks.") -> ParsedDocument:
    return ParsedDocument(
        source_path=path,
        raw_text=text,
        num_pages=2,
        file_size_bytes=1024,
        metadata={"Title": path.stem, "Author": "Test Author"},
    )


@pytest.fixture()
def paper_repo() -> FakePaperRepository:
    return FakePaperRepository()


@pytest.fixture()
def failure_repo() -> FakeFailureRepository:
    return FakeFailureRepository()


@pytest.fixture()
def parser() -> FakeDocumentParser:
    return FakeDocumentParser()


@pytest.fixture()
def service(
    parser: FakeDocumentParser,
    paper_repo: FakePaperRepository,
    failure_repo: FakeFailureRepository,
) -> IngestionService:
    return IngestionService(
        parser=parser,
        paper_repo=paper_repo,
        failure_repo=failure_repo,
    )


class TestIngestDirectory:
    def test_ingests_single_pdf(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
        paper_repo: FakePaperRepository,
    ) -> None:
        pdf = tmp_path / "paper.pdf"
        pdf.touch()
        parser.set_result(pdf, _parsed_doc(pdf))

        result = service.ingest_directory(tmp_path)

        assert len(result.successes) == 1
        assert len(result.failures) == 0
        assert result.is_complete()

    def test_ingests_multiple_pdfs(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
    ) -> None:
        for name in ["a.pdf", "b.pdf", "c.pdf"]:
            pdf = tmp_path / name
            pdf.touch()
            parser.set_result(pdf, _parsed_doc(pdf))

        result = service.ingest_directory(tmp_path)
        assert len(result.successes) == 3

    def test_parse_failure_recorded(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
        failure_repo: FakeFailureRepository,
    ) -> None:
        pdf = tmp_path / "bad.pdf"
        pdf.touch()
        parser.set_error(pdf, ParsingError("corrupted file"))

        result = service.ingest_directory(tmp_path)

        assert len(result.successes) == 0
        failures = failure_repo.list_failures()
        assert len(failures) == 1
        assert "corrupted file" in failures[0].error_message

    def test_unexpected_error_recorded_as_failure(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
        failure_repo: FakeFailureRepository,
    ) -> None:
        pdf = tmp_path / "boom.pdf"
        pdf.touch()
        parser.set_error(pdf, RuntimeError("unexpected boom"))

        result = service.ingest_directory(tmp_path)

        assert len(result.successes) == 0
        failures = failure_repo.list_failures()
        assert len(failures) == 1

    def test_skip_existing_paper(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
        paper_repo: FakePaperRepository,
    ) -> None:
        pdf = tmp_path / "existing.pdf"
        pdf.touch()
        parsed = _parsed_doc(pdf)
        parser.set_result(pdf, parsed)

        # Ingest once
        first_result = service.ingest_directory(tmp_path)
        assert len(first_result.successes) == 1

        # Ingest again — should skip
        second_result = service.ingest_directory(tmp_path, skip_existing=True)
        assert len(second_result.successes) == 0
        assert len(second_result.skipped) == 1

    def test_no_skip_when_skip_existing_false(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
    ) -> None:
        pdf = tmp_path / "paper.pdf"
        pdf.touch()
        parsed = _parsed_doc(pdf)
        parser.set_result(pdf, parsed)

        # Ingest once
        service.ingest_directory(tmp_path)
        # Ingest again with skip_existing=False → duplicate error handled
        result = service.ingest_directory(tmp_path, skip_existing=False)
        # Save raises DuplicatePaperError → _ingest_one returns None → failure
        assert len(result.skipped) == 0

    def test_empty_directory_returns_empty_result(
        self,
        tmp_path: Path,
        service: IngestionService,
    ) -> None:
        result = service.ingest_directory(tmp_path)
        assert result.total == 0
        assert result.is_complete()

    def test_invalid_directory_returns_empty_result(
        self,
        tmp_path: Path,
        service: IngestionService,
    ) -> None:
        nonexistent = tmp_path / "does_not_exist"
        result = service.ingest_directory(nonexistent)
        assert result.total == 0
        assert result.is_complete()

    def test_result_has_run_id(
        self,
        tmp_path: Path,
        service: IngestionService,
    ) -> None:
        result = service.ingest_directory(tmp_path)
        assert result.run_id != ""

    def test_recursive_discovers_nested_pdfs(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
    ) -> None:
        sub = tmp_path / "subdir"
        sub.mkdir()
        pdf = sub / "nested.pdf"
        pdf.touch()
        parser.set_result(pdf, _parsed_doc(pdf))

        result = service.ingest_directory(tmp_path, recursive=True)
        assert len(result.successes) == 1

    def test_nonrecursive_misses_nested_pdfs(
        self,
        tmp_path: Path,
        parser: FakeDocumentParser,
        service: IngestionService,
    ) -> None:
        sub = tmp_path / "subdir"
        sub.mkdir()
        pdf = sub / "nested.pdf"
        pdf.touch()
        parser.set_result(pdf, _parsed_doc(pdf))

        result = service.ingest_directory(tmp_path, recursive=False)
        assert len(result.successes) == 0
