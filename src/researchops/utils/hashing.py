"""Hashing utilities for ResearchOps."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 65536) -> str:
    """Return the hex SHA-256 digest of a file's contents.

    Reads the file in chunks to avoid loading large files into memory.
    """
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def sha256_string(value: str) -> str:
    """Return the hex SHA-256 digest of a UTF-8 string."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def short_hash(value: str, length: int = 16) -> str:
    """Return a short hex hash suitable for use as an ID."""
    return sha256_string(value)[:length]
