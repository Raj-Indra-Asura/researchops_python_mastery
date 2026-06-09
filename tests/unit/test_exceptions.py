"""Unit tests for core/exceptions.py — verifies exception messages and hierarchy."""

from __future__ import annotations

import pytest

from researchops.core.exceptions import (
    ConfigurationError,
    DuplicatePaperError,
    EmptyDocumentError,
    EmptyQueryError,
    InsufficientDataError,
    JobError,
    JobNotFoundError,
    MLError,
    ModelNotTrainedError,
    PaperNotFoundError,
    ParsingError,
    ResearchOpsError,
    SearchError,
    StorageError,
    UnsupportedFileTypeError,
)


class TestExceptionHierarchy:
    def test_parsing_error_is_researchops_error(self) -> None:
        assert issubclass(ParsingError, ResearchOpsError)

    def test_storage_error_is_researchops_error(self) -> None:
        assert issubclass(StorageError, ResearchOpsError)

    def test_search_error_is_researchops_error(self) -> None:
        assert issubclass(SearchError, ResearchOpsError)

    def test_ml_error_is_researchops_error(self) -> None:
        assert issubclass(MLError, ResearchOpsError)

    def test_job_error_is_researchops_error(self) -> None:
        assert issubclass(JobError, ResearchOpsError)

    def test_configuration_error_is_researchops_error(self) -> None:
        assert issubclass(ConfigurationError, ResearchOpsError)


class TestEmptyDocumentError:
    def test_message_includes_path(self) -> None:
        exc = EmptyDocumentError("/tmp/paper.pdf")
        assert "/tmp/paper.pdf" in str(exc)

    def test_path_attribute(self) -> None:
        exc = EmptyDocumentError("/tmp/paper.pdf")
        assert exc.path == "/tmp/paper.pdf"


class TestUnsupportedFileTypeError:
    def test_message_includes_path(self) -> None:
        exc = UnsupportedFileTypeError("paper.docx")
        assert "paper.docx" in str(exc)

    def test_path_attribute(self) -> None:
        exc = UnsupportedFileTypeError("paper.docx")
        assert exc.path == "paper.docx"


class TestPaperNotFoundError:
    def test_message_includes_id(self) -> None:
        exc = PaperNotFoundError("abc123")
        assert "abc123" in str(exc)

    def test_paper_id_attribute(self) -> None:
        exc = PaperNotFoundError("abc123")
        assert exc.paper_id == "abc123"


class TestDuplicatePaperError:
    def test_message_includes_id(self) -> None:
        exc = DuplicatePaperError("dup42")
        assert "dup42" in str(exc)

    def test_paper_id_attribute(self) -> None:
        exc = DuplicatePaperError("dup42")
        assert exc.paper_id == "dup42"


class TestEmptyQueryError:
    def test_can_be_raised(self) -> None:
        with pytest.raises(EmptyQueryError):
            raise EmptyQueryError()

    def test_is_search_error(self) -> None:
        assert issubclass(EmptyQueryError, SearchError)


class TestModelNotTrainedError:
    def test_message_includes_model_name(self) -> None:
        exc = ModelNotTrainedError("TopicClassifier")
        assert "TopicClassifier" in str(exc)

    def test_model_name_attribute(self) -> None:
        exc = ModelNotTrainedError("TopicClassifier")
        assert exc.model_name == "TopicClassifier"


class TestInsufficientDataError:
    def test_message_includes_counts(self) -> None:
        exc = InsufficientDataError(needed=100, available=10)
        assert "100" in str(exc)
        assert "10" in str(exc)


class TestJobNotFoundError:
    def test_message_includes_job_id(self) -> None:
        exc = JobNotFoundError("job-99")
        assert "job-99" in str(exc)

    def test_job_id_attribute(self) -> None:
        exc = JobNotFoundError("job-99")
        assert exc.job_id == "job-99"
