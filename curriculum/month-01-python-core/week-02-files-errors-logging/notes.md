# Notes - Week 02 Files, Errors, and Logging

Programs that touch the file system fail in more ways than simple in-memory code. Paths can be missing, files can have the wrong extension, permissions can be wrong, and text can be encoded differently than expected. The goal this week is not to eliminate all failures — it is to make failures understandable.

## pathlib.Path

Use `pathlib.Path` instead of string concatenation for paths. `Path` objects know how to join segments correctly across operating systems and give you helpful methods like `.exists()`, `.is_file()`, `.suffix`, and `.rglob()`.

```python
from pathlib import Path

# In ResearchOps, the scan command uses:
root = Path("examples/sample_papers")
for pdf_path in root.glob("*.pdf"):
    print(pdf_path.name)
```

The `find_pdfs()` helper in `researchops/utils/paths.py` centralises this pattern:

```python
# src/researchops/utils/paths.py
from pathlib import Path
import logging

log = logging.getLogger(__name__)


def find_pdfs(directory: Path, recursive: bool = False) -> list[Path]:
    if not directory.exists():
        raise NotADirectoryError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdfs = sorted(directory.glob(pattern))
    log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
    return pdfs
```

When reading text files, be explicit about encoding. UTF-8 is the modern default:

```python
config_path = Path("settings.txt")
text = config_path.read_text(encoding="utf-8")
```

## Exceptions

ResearchOps defines a custom exception hierarchy in `core/exceptions.py`. Every application exception inherits from `ResearchOpsError`, which lets callers catch the whole family with a single clause if needed.

```python
# src/researchops/core/exceptions.py

class ResearchOpsError(Exception):
    """Base class for all ResearchOps application errors."""


class ParsingError(ResearchOpsError):
    """Raised when a document cannot be parsed."""


class UnsupportedFileTypeError(ParsingError):
    """Raised when a file type is not supported (e.g. .docx instead of .pdf)."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Unsupported file type: {path}")
        self.path = path


class EmptyDocumentError(ParsingError):
    """Raised when a parsed document contains no extractable text."""

    def __init__(self, path: str) -> None:
        super().__init__(f"No text could be extracted from: {path}")
        self.path = path
```

You should not use `try/except` to hide problems. Use it to decide what to do next. A missing optional file might be logged and skipped. A missing required database path might be a fatal error.

The `else` block in a `try` statement runs only if no exception occurred — useful for separating success-path logic from error handling:

```python
try:
    data = path.read_text(encoding="utf-8")
except OSError as exc:
    log.error("failed to read %s: %s", path, exc)
else:
    log.info("read %d bytes from %s", len(data), path)
```

## Logging

`researchops/config/logging.py` provides two public functions: `configure_logging()` and `get_logger()`. Call `configure_logging()` once at startup (the CLI does this in `cli/main.py`). Use `get_logger(__name__)` in every module that needs to log.

```python
# src/researchops/config/logging.py (simplified view)
import logging


def configure_logging(level: str | None = None, use_rich: bool = True) -> None:
    """Set up root logger. Call once at application startup."""
    ...


def get_logger(name: str) -> logging.Logger:
    """Return a named module logger. Use __name__ as the name."""
    return logging.getLogger(name)
```

Usage in any module:

```python
from researchops.config.logging import get_logger

log = get_logger(__name__)

log.info("scan started")
log.warning("skipping unsupported file: %s", path)
log.error("scan failed: %s", exc)
```

Common levels and what they mean in ResearchOps context:
- `DEBUG`: internal detail (path visited, bytes read, cache hit).
- `INFO`: normal progress (scan started, N PDFs found, ingestion complete).
- `WARNING`: unexpected but recoverable (skipping `.txt`, retrying failed parse).
- `ERROR`: a specific file or operation failed and was recorded.

## Defensive programming

Do not catch exceptions too broadly. If you write `except Exception`, you may accidentally hide `TypeError` or `AttributeError` that should crash during development. Catch the narrowest useful exception, add context, and either handle or re-raise it.

A good scan result returns structured information. Instead of a flat list of paths, separate accepted, skipped, and failed paths. That makes tests cleaner and downstream logic simpler. You will build this pattern fully when `IngestionResult` is introduced in Week 3.
