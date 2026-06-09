"""Custom exception hierarchy for ResearchOps.

Rule: every exception the application raises should be a subclass of
ResearchOpsError so callers can catch the whole family with one clause.

These exceptions live in core/ and must not import from storage,
parsing, CLI, API, or any infrastructure layer.
"""


class ResearchOpsError(Exception):
    """Base class for all ResearchOps application errors."""


# ---------------------------------------------------------------------------
# Parsing errors
# ---------------------------------------------------------------------------


class ParsingError(ResearchOpsError):
    """Raised when a document cannot be parsed."""


class EmptyDocumentError(ParsingError):
    """Raised when a parsed document contains no extractable text."""

    def __init__(self, path: str) -> None:
        super().__init__(f"No text could be extracted from: {path}")
        self.path = path


class UnsupportedFileTypeError(ParsingError):
    """Raised when a file type is not supported (e.g. .docx instead of .pdf)."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Unsupported file type: {path}")
        self.path = path


# ---------------------------------------------------------------------------
# Storage errors
# ---------------------------------------------------------------------------


class StorageError(ResearchOpsError):
    """Raised for database / persistence failures."""


class PaperNotFoundError(StorageError):
    """Raised when a paper ID does not exist in storage."""

    def __init__(self, paper_id: str) -> None:
        super().__init__(f"Paper not found: {paper_id}")
        self.paper_id = paper_id


class DuplicatePaperError(StorageError):
    """Raised when trying to insert a paper that already exists."""

    def __init__(self, paper_id: str) -> None:
        super().__init__(f"Paper already exists: {paper_id}")
        self.paper_id = paper_id


# ---------------------------------------------------------------------------
# Search errors
# ---------------------------------------------------------------------------


class SearchError(ResearchOpsError):
    """Raised for search-related failures."""


class EmptyQueryError(SearchError):
    """Raised when a search query is blank or whitespace-only."""

    def __init__(self) -> None:
        super().__init__("Search query must not be empty.")


# ---------------------------------------------------------------------------
# Configuration errors
# ---------------------------------------------------------------------------


class ConfigurationError(ResearchOpsError):
    """Raised when the application configuration is invalid or missing."""


# ---------------------------------------------------------------------------
# ML errors
# ---------------------------------------------------------------------------


class MLError(ResearchOpsError):
    """Base class for ML-related errors."""


class ModelNotTrainedError(MLError):
    """Raised when trying to use a model that hasn't been trained yet."""

    def __init__(self, model_name: str) -> None:
        super().__init__(f"Model not trained: {model_name}. Run the train command first.")
        self.model_name = model_name


class InsufficientDataError(MLError):
    """Raised when there is not enough data to train a model."""

    def __init__(self, needed: int, available: int) -> None:
        super().__init__(
            f"Need at least {needed} samples to train, but only {available} available."
        )


# ---------------------------------------------------------------------------
# Job / worker errors
# ---------------------------------------------------------------------------


class JobError(ResearchOpsError):
    """Base class for job / worker errors."""


class JobNotFoundError(JobError):
    """Raised when a job ID does not exist."""

    def __init__(self, job_id: str) -> None:
        super().__init__(f"Job not found: {job_id}")
        self.job_id = job_id
