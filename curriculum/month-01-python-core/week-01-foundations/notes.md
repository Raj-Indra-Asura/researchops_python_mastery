# Notes - Week 01 Foundations

Python code is easiest to maintain when you separate concerns early. In this project, the repository itself is not the package. The package lives in `src/researchops`, and tests live in `tests`. That `src` layout prevents Python from importing the wrong files just because you ran a command from the repository root.

A module is a single `.py` file. A package is a directory of modules, usually with an `__init__.py`. Imports let modules reuse code from other modules. For example:

```python
# src/researchops/utils.py
from pathlib import Path


def project_name() -> str:
    return "ResearchOps"


def data_dir(root: Path) -> Path:
    return root / "data"
```

```python
# src/researchops/cli/main.py
import typer

from researchops.utils import project_name

app = typer.Typer()


@app.command()
def info() -> None:
    typer.echo(f"{project_name()} is ready")
```

Functions are the first tool for keeping logic understandable. A good function usually does one thing, has a short name based on the domain, and returns a value instead of printing everything. Returning values makes testing easier.

Python collections are the main building blocks for simple data. Use a `list` when order matters and duplicates are allowed. Use a `set` when you want unique values. Use a `dict` when you want named fields or key-value lookup. Use a `tuple` when the shape is fixed.

```python
authors = ["Ada", "Grace", "Linus"]
seen_topics = {"ml", "systems", "ml"}
paper = {"title": "Graph Search", "pages": 12}
coords = (42.0, -71.0)
```

A virtual environment keeps project dependencies isolated from the system Python. A common flow is:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The `-e` means editable install. Your code is still in the repository, but Python treats it like an installed package. That is ideal for active development.

`pyproject.toml` is the standard place to declare package metadata, dependencies, and tool configuration. In this repo it also defines the CLI entry point:

```toml
[project.scripts]
researchops = "researchops.cli.main:app"
```

That tells the packaging tool to expose a shell command named `researchops` that points at the Typer app object.

Be careful with imports. If `a.py` imports `b.py` and `b.py` also imports `a.py`, you can create a circular import. The simplest fix is usually to move shared logic into a third module such as `utils.py` or `models.py`.

Beginner-friendly code is explicit code. Prefer:

```python
def paper_count(items: list[str]) -> int:
    return len(items)
```

instead of overly clever one-liners. During week 1, your goal is not abstraction for its own sake. Your goal is to build a working package skeleton and become comfortable moving between shell commands, Python files, and tests.

If something fails, read the traceback from the bottom up. Usually the last few lines tell you which module import or function call actually broke. That debugging habit will matter every week of this curriculum.
