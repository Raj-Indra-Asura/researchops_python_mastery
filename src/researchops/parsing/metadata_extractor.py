"""Metadata extraction helpers.

Week 6 TODO:
- Extract DOI using regex from text.
- Extract year from metadata or text.
- Extract abstract heuristically (first long paragraph).
"""

from __future__ import annotations

import re

from researchops.core.models import ParsedDocument


def extract_title(doc: ParsedDocument) -> str:
    """Best-effort title extraction.

    Uses PDF metadata first, then falls back to the first non-empty line.
    """
    title = doc.metadata.get("Title", "").strip()
    if title:
        return title

    # Fall back to first meaningful line of text
    for line in doc.raw_text.splitlines():
        stripped = line.strip()
        if stripped and len(stripped) > 5:
            return stripped[:200]

    return doc.source_path.stem


def extract_author(doc: ParsedDocument) -> str | None:
    """Return the PDF-metadata author field if present."""
    return doc.metadata.get("Author") or None


def extract_abstract(doc: ParsedDocument) -> str | None:
    """Heuristically extract an abstract from the document text.

    Week 6 TODO: Improve with more robust pattern matching.
    """
    # Look for an "Abstract" section header
    pattern = re.compile(r"\bAbstract\b[:\s]*(.+?)(?=\n\n|\Z)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(doc.raw_text[:3000])  # only search the beginning
    if match:
        abstract = match.group(1).strip()
        return abstract[:1000] if abstract else None
    return None
