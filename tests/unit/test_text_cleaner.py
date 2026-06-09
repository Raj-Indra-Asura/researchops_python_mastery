"""Unit tests for text cleaning utilities."""

from __future__ import annotations

from researchops.parsing.text_cleaner import clean_text, normalise_for_search


class TestCleanText:
    def test_strips_leading_trailing_whitespace(self) -> None:
        assert clean_text("  hello  ") == "hello"

    def test_collapses_multiple_blank_lines(self) -> None:
        result = clean_text("a\n\n\n\n\nb")
        assert "\n\n\n" not in result

    def test_handles_empty_string(self) -> None:
        assert clean_text("") == ""

    def test_preserves_newlines(self) -> None:
        result = clean_text("line one\nline two")
        assert "\n" in result


class TestNormaliseForSearch:
    def test_lowercases(self) -> None:
        assert normalise_for_search("Hello World") == "hello world"

    def test_removes_punctuation(self) -> None:
        result = normalise_for_search("hello, world!")
        assert "," not in result
        assert "!" not in result

    def test_collapses_whitespace(self) -> None:
        result = normalise_for_search("  multiple   spaces  ")
        assert "  " not in result
        assert result == "multiple spaces"

    def test_empty_string(self) -> None:
        assert normalise_for_search("") == ""
