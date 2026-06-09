"""Unit tests for core value objects: Query, Tag, FilePath."""

from __future__ import annotations

from pathlib import Path

import pytest

from researchops.core.exceptions import EmptyQueryError
from researchops.core.value_objects import FilePath, Query, Tag


class TestQuery:
    def test_valid_query_stores_value(self) -> None:
        q = Query("neural networks")
        assert q.value == "neural networks"

    def test_empty_query_raises(self) -> None:
        with pytest.raises(EmptyQueryError):
            Query("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(EmptyQueryError):
            Query("   ")

    def test_internal_whitespace_collapsed(self) -> None:
        q = Query("neural   networks  paper")
        assert q.value == "neural networks paper"

    def test_leading_trailing_whitespace_stripped(self) -> None:
        q = Query("  deep learning  ")
        assert q.value == "deep learning"

    def test_terms_returns_lowercase_list(self) -> None:
        q = Query("Deep Learning NLP")
        assert q.terms() == ["deep", "learning", "nlp"]

    def test_str_returns_value(self) -> None:
        q = Query("transformer")
        assert str(q) == "transformer"

    def test_equality_by_value(self) -> None:
        assert Query("test") == Query("test")

    def test_immutable(self) -> None:
        q = Query("immutable")
        with pytest.raises((AttributeError, TypeError)):
            q.value = "changed"  # type: ignore[misc]


class TestTag:
    def test_valid_tag_stored_lowercase(self) -> None:
        t = Tag("MachineLearning")
        assert t.value == "machinelearning"

    def test_spaces_converted_to_hyphens(self) -> None:
        t = Tag("machine learning")
        assert t.value == "machine-learning"

    def test_leading_trailing_whitespace_stripped(self) -> None:
        t = Tag("  nlp  ")
        assert t.value == "nlp"

    def test_empty_tag_raises(self) -> None:
        with pytest.raises(ValueError):
            Tag("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError):
            Tag("   ")

    def test_str_returns_value(self) -> None:
        t = Tag("deep-learning")
        assert str(t) == "deep-learning"

    def test_equality_by_value(self) -> None:
        assert Tag("nlp") == Tag("nlp")

    def test_case_normalisation(self) -> None:
        assert Tag("NLP") == Tag("nlp")


class TestFilePath:
    def test_valid_path_resolves_absolute(self, tmp_path: Path) -> None:
        fp = FilePath(str(tmp_path))
        assert fp.value == str(tmp_path.resolve())

    def test_str_returns_value(self, tmp_path: Path) -> None:
        fp = FilePath(str(tmp_path))
        assert str(fp) == fp.value

    def test_equality_by_resolved_path(self, tmp_path: Path) -> None:
        fp1 = FilePath(str(tmp_path))
        fp2 = FilePath(str(tmp_path.resolve()))
        assert fp1 == fp2
