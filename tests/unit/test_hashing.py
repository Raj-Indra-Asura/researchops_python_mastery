"""Unit tests for utils/hashing.py."""

from __future__ import annotations

from pathlib import Path

from researchops.utils.hashing import sha256_file, sha256_string, short_hash


class TestSha256String:
    def test_returns_hex_string(self) -> None:
        result = sha256_string("hello")
        assert isinstance(result, str)
        assert all(c in "0123456789abcdef" for c in result)

    def test_length_is_64(self) -> None:
        assert len(sha256_string("test")) == 64

    def test_same_input_same_output(self) -> None:
        assert sha256_string("deterministic") == sha256_string("deterministic")

    def test_different_inputs_differ(self) -> None:
        assert sha256_string("aaa") != sha256_string("bbb")

    def test_empty_string(self) -> None:
        result = sha256_string("")
        assert len(result) == 64


class TestSha256File:
    def test_hashes_file_content(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.write_bytes(b"hello world")
        result = sha256_file(f)
        assert isinstance(result, str)
        assert len(result) == 64

    def test_same_content_same_hash(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_bytes(b"same content")
        f2.write_bytes(b"same content")
        assert sha256_file(f1) == sha256_file(f2)

    def test_different_content_different_hash(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_bytes(b"content a")
        f2.write_bytes(b"content b")
        assert sha256_file(f1) != sha256_file(f2)

    def test_large_file_chunked(self, tmp_path: Path) -> None:
        f = tmp_path / "large.bin"
        f.write_bytes(b"x" * 200_000)
        result = sha256_file(f, chunk_size=65536)
        assert len(result) == 64


class TestShortHash:
    def test_default_length_16(self) -> None:
        result = short_hash("something")
        assert len(result) == 16

    def test_custom_length(self) -> None:
        result = short_hash("something", length=8)
        assert len(result) == 8

    def test_is_prefix_of_full_hash(self) -> None:
        value = "test value"
        full = sha256_string(value)
        assert short_hash(value, length=16) == full[:16]
