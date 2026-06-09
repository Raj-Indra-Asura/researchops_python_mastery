"""Unit tests for parsing/metadata_extractor.py."""

from __future__ import annotations

from pathlib import Path

from researchops.core.models import ParsedDocument
from researchops.parsing.metadata_extractor import (
    extract_abstract,
    extract_author,
    extract_title,
)


def _doc(
    raw_text: str = "",
    metadata: dict[str, str] | None = None,
    path: str = "/tmp/paper.pdf",
) -> ParsedDocument:
    return ParsedDocument(
        source_path=Path(path),
        raw_text=raw_text,
        num_pages=1,
        file_size_bytes=100,
        metadata=metadata or {},
    )


class TestExtractTitle:
    def test_uses_metadata_title_when_present(self) -> None:
        doc = _doc(metadata={"Title": "My Great Paper"})
        assert extract_title(doc) == "My Great Paper"

    def test_falls_back_to_first_meaningful_line(self) -> None:
        doc = _doc(raw_text="\n\nIntroduction to Deep Learning\nSome body text.")
        assert extract_title(doc) == "Introduction to Deep Learning"

    def test_falls_back_to_stem_when_no_text(self) -> None:
        doc = _doc(raw_text="", path="/tmp/my_paper.pdf")
        assert extract_title(doc) == "my_paper"

    def test_metadata_title_stripped(self) -> None:
        doc = _doc(metadata={"Title": "  Spaced Title  "})
        assert extract_title(doc) == "Spaced Title"

    def test_short_lines_skipped_in_fallback(self) -> None:
        doc = _doc(raw_text="Hi\nA Longer Title Line Here")
        assert extract_title(doc) == "A Longer Title Line Here"

    def test_title_truncated_at_200_chars(self) -> None:
        long_line = "A" * 250
        doc = _doc(raw_text=long_line)
        assert len(extract_title(doc)) <= 200


class TestExtractAuthor:
    def test_returns_author_from_metadata(self) -> None:
        doc = _doc(metadata={"Author": "Jane Doe"})
        assert extract_author(doc) == "Jane Doe"

    def test_returns_none_when_no_author(self) -> None:
        doc = _doc()
        assert extract_author(doc) is None

    def test_returns_none_for_empty_author(self) -> None:
        doc = _doc(metadata={"Author": ""})
        assert extract_author(doc) is None


class TestExtractAbstract:
    def test_extracts_text_after_abstract_header(self) -> None:
        text = "Title\n\nAbstract\nThis paper presents a novel approach.\n\nIntroduction"
        doc = _doc(raw_text=text)
        result = extract_abstract(doc)
        assert result is not None
        assert "novel approach" in result

    def test_returns_none_when_no_abstract(self) -> None:
        doc = _doc(raw_text="Introduction\nSome text with no relevant header section.")
        assert extract_abstract(doc) is None

    def test_abstract_with_colon(self) -> None:
        text = "Abstract: This study investigates ML techniques.\n\nSection 2"
        doc = _doc(raw_text=text)
        result = extract_abstract(doc)
        assert result is not None
        assert "investigates" in result

    def test_abstract_truncated_at_1000_chars(self) -> None:
        long_abstract = "A" * 2000
        text = f"Abstract\n{long_abstract}\n\n"
        doc = _doc(raw_text=text)
        result = extract_abstract(doc)
        assert result is not None
        assert len(result) <= 1000
