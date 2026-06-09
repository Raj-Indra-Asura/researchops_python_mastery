"""Path utilities for ResearchOps.

This module provides helpers for discovering and validating file paths.
It uses pathlib throughout — never os.path.
"""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def find_pdfs(directory: Path, recursive: bool = False) -> list[Path]:
    """Return a sorted list of PDF files found in *directory*.

    Args:
        directory: The directory to scan.
        recursive: If True, search all subdirectories as well.

    Returns:
        A sorted list of Path objects pointing to .pdf files.

    Raises:
        NotADirectoryError: If *directory* does not exist or is not a directory.
    """
    if not directory.exists():
        raise NotADirectoryError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdfs = sorted(directory.glob(pattern))
    log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
    return pdfs


def ensure_dir(path: Path) -> Path:
    """Create *path* and all parent directories if they don't exist.

    Returns the path so callers can use this inline:
        db_path = ensure_dir(settings.db_path.parent) / "researchops.db"
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_resolve(path: Path) -> Path:
    """Return a resolved absolute path without raising on symlink loops."""
    try:
        return path.resolve()
    except OSError:
        return path.absolute()
