"""PDF parser — extracts text and metadata from PDF files.

This module wraps the ``pypdf`` library. The function is intentionally
synchronous and CPU-bound: it is designed to run inside a
ProcessPoolExecutor (see workers/process_pool.py), never directly
inside an asyncio event loop.

Week 6 TODO:
- Add more robust metadata extraction (DOI, year, abstract).
- Handle password-protected PDFs gracefully.
- Fall back to page-level extraction if full-text fails.
"""

from __future__ import annotations

import logging
from pathlib import Path

from researchops.core.exceptions import EmptyDocumentError, ParsingError
from researchops.core.models import ParsedDocument

log = logging.getLogger(__name__)


def parse_pdf(path: Path) -> ParsedDocument:
    """Parse a single PDF file and return a ParsedDocument.

    Args:
        path: Absolute or relative path to a ``.pdf`` file.

    Returns:
        A :class:`~researchops.core.models.ParsedDocument` with the
        extracted text, page count, file size, and any metadata the
        PDF header contains.

    Raises:
        ParsingError: If the file cannot be opened or read.
        EmptyDocumentError: If no text can be extracted (e.g. scanned
            image PDFs without embedded text).
    """
    try:
        # pypdf is an optional dependency — import lazily so the core
        # package works even without it installed.
        import pypdf  # type: ignore[import]
    except ImportError as exc:
        raise ParsingError(
            "pypdf is required for PDF parsing. Install it with: "
            "pip install 'researchops[parsing]'"
        ) from exc

    if not path.exists():
        raise ParsingError(f"File not found: {path}")
    if path.suffix.lower() != ".pdf":
        from researchops.core.exceptions import UnsupportedFileTypeError

        raise UnsupportedFileTypeError(str(path))

    log.debug("Parsing PDF: %s", path)

    try:
        reader = pypdf.PdfReader(str(path))
        pages_text: list[str] = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages_text.append(text)

        full_text = "\n".join(pages_text)

        # Extract PDF metadata (optional fields)
        meta = reader.metadata or {}
        metadata: dict[str, str] = {}
        for key, value in meta.items():
            if isinstance(value, str) and value.strip():
                clean_key = key.lstrip("/")
                metadata[clean_key] = value.strip()

    except Exception as exc:
        raise ParsingError(f"Failed to parse {path}: {exc}") from exc

    doc = ParsedDocument(
        source_path=path,
        raw_text=full_text,
        num_pages=len(reader.pages),
        file_size_bytes=path.stat().st_size,
        metadata=metadata,
    )

    if doc.is_empty():
        raise EmptyDocumentError(str(path))

    log.info("Parsed %d pages from %s (%d chars)", doc.num_pages, path.name, len(full_text))
    return doc
