"""Search command group.

Week 7 TODO: implement `researchops search QUERY` using KeywordSearchService.
Week 13 TODO: implement `researchops semantic-search QUERY`.
"""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def search(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search query."),
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum results to return."),
) -> None:
    """Search the paper library by keyword.

    [dim]Implemented in Week 7.[/dim]
    """
    # TODO (Week 7): wire KeywordSearchService with SQLitePaperRepository
    console.print("[yellow]⚠ Keyword search is not yet implemented (Week 7 deliverable).[/yellow]")
    console.print(f"  Query : {query}")
    console.print(f"  Limit : {limit}")
