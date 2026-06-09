# Notes - Week 04 CLI and Packaging

A command-line interface turns your code from a library into a tool people can actually use. Typer is a good fit for beginner-friendly Python CLIs because it builds on function signatures and type hints. If you can write a normal Python function, you can usually turn it into a command.

## CLI structure in ResearchOps

The CLI uses a two-level layout. The root app lives in `cli/main.py`. Future command groups (added from Week 5 onwards) are registered as sub-apps via `app.add_typer()`:

```python
# src/researchops/cli/main.py
import typer
from rich.console import Console

from researchops.config.logging import configure_logging
from researchops.config.settings import settings

app = typer.Typer(
    name="researchops",
    help="ResearchOps — research paper processing platform.",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()

# Sub-command groups registered here (Week 5+):
# from researchops.cli.commands import ingest, papers, search
# app.add_typer(ingest.app, name="ingest", ...)
```

The `@app.callback()` is where global flags like `--verbose` are declared:

```python
@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging."),
) -> None:
    configure_logging(level="DEBUG" if verbose else settings.log_level)
```

## The scan command

The top-level `scan` command is the Week 1/4 deliverable. It calls `find_pdfs()` from `utils/paths.py` and formats results using Rich:

```python
@app.command()
def scan(
    directory: str = typer.Argument(..., help="Path to a directory containing PDF files."),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Search subdirectories."),
) -> None:
    """Scan a directory and list discovered PDF files."""
    from pathlib import Path
    from researchops.utils.paths import find_pdfs

    path = Path(directory)

    try:
        pdfs = find_pdfs(path, recursive=recursive)
    except NotADirectoryError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1) from exc

    if not pdfs:
        console.print(f"[yellow]No PDF files found in {path}[/yellow]")
        raise typer.Exit(0)

    for pdf in pdfs:
        size_kb = pdf.stat().st_size / 1024
        console.print(f"  {pdf.name}  ({size_kb:.1f} KB)")

    console.print(f"\n[bold]{len(pdfs)} PDF(s) found[/bold]")
```

The command handler stays thin: gather input, call application logic (`find_pdfs`), format output. The heavy work lives in `utils/paths.py`.

## Entry point in pyproject.toml

```toml
[project.scripts]
researchops = "researchops.cli.main:app"
```

When the package is installed, this line creates a `researchops` shell command. If the module path or object name is wrong, the CLI will fail at launch with an `ImportError` or `AttributeError`. Always re-run `pip install -e .` after changing the entry point.

## Testing the CLI

Typer's built-in `CliRunner` (from `typer.testing`) lets you call the app in-process, capture output, and assert on both exit code and text:

```python
from typer.testing import CliRunner
from researchops.cli.main import app

runner = CliRunner()


def test_scan_help() -> None:
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "Directory containing PDF files" in result.output


def test_scan_nonexistent_directory() -> None:
    result = runner.invoke(app, ["scan", "/tmp/does_not_exist_researchops"])
    assert result.exit_code != 0
```

Existing CLI tests live in `tests/e2e/test_cli.py`.

## Exit codes

A CLI should not show Python tracebacks for ordinary user errors. Catch domain exceptions and convert them into a clean message plus a non-zero exit code:

```python
raise typer.Exit(code=1)
```

Scripts and CI systems use exit codes to detect failure. Exit 0 means success; any other value means failure.

## Packaging also affects imports

When code is installed in editable mode (`pip install -e .`), `researchops` resolves as an installed package, not a random directory on disk. That consistency is why packaging work happens early in a serious project. If you move files, update imports everywhere before reinstalling.
