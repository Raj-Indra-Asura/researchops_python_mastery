"""Papers command group.

Week 6 TODO: implement list, show, stats, failed.
"""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("list")
def list_papers() -> None:
    """List all papers in the library.

    [dim]Implemented in Week 6.[/dim]
    """
    # TODO (Week 6): wire PaperService with SQLitePaperRepository
    console.print("[yellow]⚠ Paper listing is not yet implemented (Week 6 deliverable).[/yellow]")


@app.command("show")
def show_paper(paper_id: str = typer.Argument(..., help="Paper ID to display.")) -> None:
    """Show full details of a single paper.

    [dim]Implemented in Week 6.[/dim]
    """
    # TODO (Week 6): wire PaperService
    console.print("[yellow]⚠ Paper show is not yet implemented (Week 6 deliverable).[/yellow]")
    console.print(f"  Paper ID: {paper_id}")


@app.command("stats")
def stats() -> None:
    """Show library statistics.

    [dim]Implemented in Week 7.[/dim]
    """
    # TODO (Week 7): wire PaperService.stats()
    console.print("[yellow]⚠ Stats are not yet implemented (Week 7 deliverable).[/yellow]")


@app.command("failed")
def failed() -> None:
    """Show documents that failed to ingest.

    [dim]Implemented in Week 7.[/dim]
    """
    # TODO (Week 7): wire FailureRepository
    console.print("[yellow]⚠ Failure tracking is not yet implemented (Week 7 deliverable).[/yellow]")
