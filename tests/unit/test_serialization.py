"""Unit tests for utils/serialization.py."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from researchops.utils.serialization import from_json, to_json


class TestToJson:
    def test_simple_dict(self) -> None:
        result = to_json({"key": "value"})
        assert '"key"' in result
        assert '"value"' in result

    def test_datetime_serialised_as_isoformat(self) -> None:
        dt = datetime(2024, 1, 15, 12, 30, 0)
        result = to_json({"ts": dt})
        assert "2024-01-15T12:30:00" in result

    def test_path_serialised_as_string(self) -> None:
        p = Path("/tmp/test.pdf")
        result = to_json({"path": p})
        assert "/tmp/test.pdf" in result

    def test_unsupported_type_raises(self) -> None:
        class Unpicklable:
            pass

        with pytest.raises(TypeError):
            to_json({"obj": Unpicklable()})

    def test_default_indent_is_2(self) -> None:
        result = to_json({"a": 1})
        assert "\n" in result  # indented output has newlines

    def test_list_serialised(self) -> None:
        result = to_json([1, 2, 3])
        assert "[" in result


class TestFromJson:
    def test_parses_simple_dict(self) -> None:
        data = from_json('{"key": "value"}')
        assert data == {"key": "value"}

    def test_parses_list(self) -> None:
        data = from_json("[1, 2, 3]")
        assert data == [1, 2, 3]

    def test_roundtrip_plain_types(self) -> None:
        original = {"name": "paper", "count": 42, "flag": True}
        assert from_json(to_json(original)) == original
