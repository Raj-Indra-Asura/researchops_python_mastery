"""Ingest command group.

Week 6 TODO: implement `researchops ingest PATH` using IngestionService.
"""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def ingest(
    ctx: typer.Context,
    directory: str = typer.Argument(".", help="Directory of PDFs to ingest."),
    workers: int = typer.Option(1, "--workers", "-w", help="Parallel worker processes (Week 8)."),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recurse into subdirectories."),
) -> None:
    """Ingest PDF files from a directory into the ResearchOps library.

    [dim]Implemented in Week 6.[/dim]
    """
    # TODO (Week 6): wire IngestionService with SQLitePaperRepository and PDFParser
    console.print("[yellow]⚠ Ingestion is not yet implemented (Week 6 deliverable).[/yellow]")
    console.print(f"  Directory : {directory}")
    console.print(f"  Recursive : {recursive}")
    console.print(f"  Workers   : {workers}")
