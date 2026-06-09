"""Unit tests for path utilities."""

from __future__ import annotations

from pathlib import Path

import pytest

from researchops.utils.paths import ensure_dir, find_pdfs


class TestFindPdfs:
    def test_returns_sorted_list(self, tmp_path: Path) -> None:
        (tmp_path / "b.pdf").touch()
        (tmp_path / "a.pdf").touch()
        result = find_pdfs(tmp_path)
        assert [p.name for p in result] == ["a.pdf", "b.pdf"]

    def test_excludes_non_pdf_files(self, tmp_path: Path) -> None:
        (tmp_path / "paper.pdf").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "image.png").touch()
        result = find_pdfs(tmp_path)
        assert len(result) == 1
        assert result[0].name == "paper.pdf"

    def test_returns_empty_for_empty_directory(self, tmp_path: Path) -> None:
        result = find_pdfs(tmp_path)
        assert result == []

    def test_raises_for_nonexistent_directory(self, tmp_path: Path) -> None:
        with pytest.raises(NotADirectoryError):
            find_pdfs(tmp_path / "does_not_exist")

    def test_raises_for_file_not_directory(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.touch()
        with pytest.raises(NotADirectoryError):
            find_pdfs(f)

    def test_recursive_finds_nested_pdfs(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "top.pdf").touch()
        (sub / "nested.pdf").touch()

        non_recursive = find_pdfs(tmp_path, recursive=False)
        recursive = find_pdfs(tmp_path, recursive=True)

        assert len(non_recursive) == 1
        assert len(recursive) == 2

    def test_non_recursive_ignores_subdirectory_pdfs(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.pdf").touch()
        result = find_pdfs(tmp_path, recursive=False)
        assert result == []


class TestEnsureDir:
    def test_creates_directory(self, tmp_path: Path) -> None:
        target = tmp_path / "new" / "nested" / "dir"
        result = ensure_dir(target)
        assert target.exists()
        assert target.is_dir()
        assert result == target

    def test_existing_directory_is_idempotent(self, tmp_path: Path) -> None:
        ensure_dir(tmp_path)  # already exists
        assert tmp_path.exists()
