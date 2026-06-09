"""Keyword search service.

Week 7 TODO: implement full-text search over stored papers.
"""

from __future__ import annotations

import logging

from researchops.core.exceptions import EmptyQueryError
from researchops.core.interfaces import PaperRepository
from researchops.core.models import SearchResult
from researchops.parsing.text_cleaner import normalise_for_search

log = logging.getLogger(__name__)


class KeywordSearchService:
    """Simple keyword search over stored paper text.

    This is an in-memory implementation: it loads all papers and
    filters/ranks them with Python. Good enough for Week 7; replace
    with SQLite FTS5 in a later week if needed.
    """

    def __init__(self, paper_repo: PaperRepository) -> None:
        self._repo = paper_repo

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Return papers matching *query*, ordered by relevance (descending).

        Raises:
            EmptyQueryError: if the query is blank.
        """
        query = query.strip()
        if not query:
            raise EmptyQueryError()

        terms = normalise_for_search(query).split()
        papers = self._repo.list_all()
        results: list[SearchResult] = []

        for paper in papers:
            haystack = normalise_for_search(paper.title + " " + paper.text)
            score = sum(haystack.count(term) for term in terms)
            if score > 0:
                snippet = self._extract_snippet(paper.text, terms)
                results.append(SearchResult(paper=paper, score=float(score), snippet=snippet))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    @staticmethod
    def _extract_snippet(text: str, terms: list[str], context: int = 80) -> str:
        """Return a short text snippet containing the first matched term."""
        lower = text.lower()
        for term in terms:
            idx = lower.find(term)
            if idx >= 0:
                start = max(0, idx - context)
                end = min(len(text), idx + len(term) + context)
                snippet = text[start:end].replace("\n", " ")
                return f"…{snippet}…" if start > 0 else f"{snippet}…"
        return text[:160]
