"""ResearchOps CLI entry point.

Run with:
    researchops --help
    researchops scan ./papers
    researchops ingest ./papers        (Week 6)
    researchops search "query"         (Week 7)
    researchops list                   (Week 6)
    researchops show PAPER_ID          (Week 6)
    researchops stats                  (Week 7)
    researchops failed                 (Week 7)

Architecture rule: the CLI layer MUST NOT contain business logic.
All real work is delegated to service classes.
"""

from __future__ import annotations

import typer
from rich.console import Console

from researchops.config.logging import configure_logging
from researchops.config.settings import settings

app = typer.Typer(
    name="researchops",
    help="ResearchOps — research paper processing and experiment-tracking platform.",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()

# Import and register sub-command modules
from researchops.cli.commands import ingest, papers, search  # noqa: E402

app.add_typer(ingest.app, name="ingest", help="Ingest PDF files into the library.")
app.add_typer(papers.app, name="papers", help="Manage and view stored papers.")
app.add_typer(search.app, name="search", help="Search the paper library.")


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging."),
) -> None:
    """ResearchOps — build, search, and analyse a research paper library."""
    configure_logging(
        level="DEBUG" if verbose else settings.log_level,
    )


# ---------------------------------------------------------------------------
# Top-level scan command (Week 1 deliverable)
# ---------------------------------------------------------------------------


@app.command()
def scan(
    directory: str = typer.Argument(
        ...,
        help="Path to a directory containing PDF files.",
    ),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Search subdirectories recursively."
    ),
) -> None:
    """Scan a directory and list discovered PDF files.

    This command is a quick sanity-check: it finds PDFs without parsing
    or storing them. Use [bold]ingest[/bold] to actually process them.
    """
    from pathlib import Path

    from rich.table import Table

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

    table = Table(title=f"PDFs in {path}", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Filename", style="cyan")
    table.add_column("Size", style="green", justify="right")

    for i, pdf in enumerate(pdfs, start=1):
        size_kb = pdf.stat().st_size / 1024
        table.add_row(str(i), pdf.name, f"{size_kb:.1f} KB")

    console.print(table)
    console.print(f"\n[bold]{len(pdfs)} PDF(s) found[/bold]")


if __name__ == "__main__":
    app()
