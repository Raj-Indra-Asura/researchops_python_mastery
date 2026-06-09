"""E2E CLI tests using Typer's test runner."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from researchops.cli.main import app

runner = CliRunner()


class TestCLIHelp:
    def test_help_exits_zero(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

    def test_help_contains_scan(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert "scan" in result.output.lower()


class TestScanCommand:
    def test_scan_empty_directory(self, tmp_path: Path) -> None:
        result = runner.invoke(app, ["scan", str(tmp_path)])
        assert result.exit_code == 0
        assert "No PDF" in result.output or "0" in result.output

    def test_scan_lists_pdf_files(self, tmp_path: Path) -> None:
        (tmp_path / "paper_a.pdf").touch()
        (tmp_path / "paper_b.pdf").touch()
        result = runner.invoke(app, ["scan", str(tmp_path)])
        assert result.exit_code == 0
        assert "paper_a.pdf" in result.output
        assert "paper_b.pdf" in result.output

    def test_scan_ignores_non_pdf_files(self, tmp_path: Path) -> None:
        (tmp_path / "paper.pdf").touch()
        (tmp_path / "readme.txt").touch()
        result = runner.invoke(app, ["scan", str(tmp_path)])
        assert result.exit_code == 0
        assert "readme.txt" not in result.output

    def test_scan_nonexistent_directory(self) -> None:
        result = runner.invoke(app, ["scan", "/tmp/this_does_not_exist_researchops"])
        assert result.exit_code != 0

    def test_scan_recursive_flag(self, tmp_path: Path) -> None:
        sub = tmp_path / "subdir"
        sub.mkdir()
        (tmp_path / "top.pdf").touch()
        (sub / "nested.pdf").touch()

        non_recursive = runner.invoke(app, ["scan", str(tmp_path)])
        recursive = runner.invoke(app, ["scan", str(tmp_path), "--recursive"])

        assert "top.pdf" in non_recursive.output
        assert "nested.pdf" not in non_recursive.output
        assert "nested.pdf" in recursive.output
