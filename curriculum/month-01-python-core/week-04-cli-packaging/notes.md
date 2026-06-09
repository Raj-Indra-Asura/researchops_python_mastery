# Notes - Week 04 CLI and Packaging

A command-line interface turns your code from a library into a tool people can actually use. Typer is a good fit for beginner-friendly Python CLIs because it builds on function signatures and type hints. If you can write a normal Python function, you can usually turn it into a command.

```python
import typer
from pathlib import Path

app = typer.Typer()


@app.command()
def scan(path: Path) -> None:
    typer.echo(f"Scanning {path}")
```

Typer reads the parameter type and converts command-line input into a `Path` object automatically. That means your command logic can stay focused on the project domain instead of manually parsing strings.

As CLIs grow, keep command handlers thin. A command should gather inputs, call application logic, and format output. The heavy work should live in services such as `scanner.py` or `ingestion.py`. That separation makes testing easier.

```python
@app.command()
def scan(path: Path, verbose: bool = False) -> None:
    result = scan_directory(path, verbose=verbose)
    typer.echo(f"accepted={result.accepted_count} failed={result.failed_count}")
```

Packaging connects your Python code to the shell. In `pyproject.toml`, this line matters:

```toml
[project.scripts]
researchops = "researchops.cli.main:app"
```

When the package is installed, a `researchops` command becomes available. If the path is wrong, the CLI will not launch. That is why packaging errors often feel mysterious: the Python code may be fine, but the entry point is misconfigured.

Good CLI design means good help text. Users should be able to run `researchops --help` and immediately see what the tool does. Use descriptive command names and option help strings.

```python
@app.command()
def scan(
    path: Path = typer.Argument(..., help="Directory containing research papers"),
    verbose: bool = typer.Option(False, "--verbose", help="Show debug logging"),
) -> None:
    ...
```

Exit behavior matters too. A CLI should not show a Python traceback for ordinary user errors like a missing directory. Instead, catch the domain exception and convert it into a clean message plus a non-zero exit code.

```python
raise typer.Exit(code=1)
```

That way scripts and CI systems can detect failure reliably.

Testing CLIs often uses Typer's or Click's runner utilities. The important idea is that you can call the app in-process, capture output, and assert on both exit code and text.

```python
def test_scan_help(runner):
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "Directory containing research papers" in result.output
```

Packaging also affects imports. When code is installed in editable mode, `researchops` resolves as an installed package, not as a random folder on disk. That consistency is why packaging work happens early in a serious project.

By the end of this week, you should think of the CLI as the outside boundary of the system. It is the layer users touch first, but it should stay simple because the real logic belongs deeper in the application. That design choice will matter when you later add storage, APIs, and background workers.
