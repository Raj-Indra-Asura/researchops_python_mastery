"""Paper service — higher-level operations on papers.

Week 6 TODO: implement list, get, stats, show.
"""

from __future__ import annotations

import logging

from researchops.core.interfaces import PaperRepository
from researchops.core.models import Paper

log = logging.getLogger(__name__)


class PaperService:
    """Query and manage stored papers."""

    def __init__(self, paper_repo: PaperRepository) -> None:
        self._repo = paper_repo

    def get_paper(self, paper_id: str) -> Paper:
        """Return a paper by ID. Raises PaperNotFoundError if missing."""
        return self._repo.get(paper_id)

    def list_papers(self) -> list[Paper]:
        """Return all stored papers."""
        return self._repo.list_all()

    def stats(self) -> dict[str, int]:
        """Return summary statistics about the paper library."""
        papers = self._repo.list_all()
        total_words = sum(p.word_count() for p in papers)
        return {
            "total_papers": len(papers),
            "total_words": total_words,
            "total_pages": sum(p.num_pages for p in papers),
        }
