"""Value objects for ResearchOps.

Value objects are small, immutable domain concepts that are equal
by value (not by identity). They live in core/ and have no
infrastructure dependencies.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    """A sanitised search query.

    Guarantees that the query is non-empty after stripping whitespace.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            from researchops.core.exceptions import EmptyQueryError

            raise EmptyQueryError()
        # normalise: collapse internal whitespace
        object.__setattr__(self, "value", " ".join(self.value.split()))

    def terms(self) -> list[str]:
        """Return individual lowercase search terms."""
        return self.value.lower().split()

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Tag:
    """A normalised, lowercase, no-whitespace tag label."""

    value: str

    def __post_init__(self) -> None:
        normalised = re.sub(r"\s+", "-", self.value.strip().lower())
        if not normalised:
            raise ValueError("Tag value must not be empty.")
        object.__setattr__(self, "value", normalised)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class FilePath:
    """A validated, resolved absolute file path."""

    value: str

    def __post_init__(self) -> None:
        from pathlib import Path

        resolved = str(Path(self.value).resolve())
        object.__setattr__(self, "value", resolved)

    def __str__(self) -> str:
        return self.value
