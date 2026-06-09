# Notes - Week 01 Foundations

Python code is easiest to maintain when you separate concerns early. In this project, the repository itself is not the package. The package lives in `src/researchops`, and tests live in `tests`. That `src` layout prevents Python from importing the wrong files just because you ran a command from the repository root.

A module is a single `.py` file. A package is a directory of modules with an `__init__.py`. The `researchops` package is itself divided into sub-packages: `cli/`, `config/`, `core/`, `utils/`, and eventually `storage/`, `services/`, `ml/`, and more. This structure means each concern gets its own home from day one.

## Package layout

```
src/researchops/
├── __init__.py
├── cli/
│   ├── __init__.py
│   ├── main.py        ← Typer app, top-level commands
│   └── commands/      ← One file per command group (added in Week 4+)
├── config/
│   ├── __init__.py
│   ├── settings.py    ← Pydantic Settings loaded from .env / env vars
│   └── logging.py     ← configure_logging() and get_logger()
├── core/              ← Domain models and exceptions (no external deps)
│   └── ...
└── utils/
    ├── __init__.py
    └── paths.py       ← find_pdfs(), ensure_dir(), safe_resolve()
```

## Importing between modules

Use absolute imports throughout. For example, the CLI scan command imports from `utils/paths.py`:

```python
# src/researchops/cli/main.py
from researchops.utils.paths import find_pdfs
```

And configuration is accessed via the settings singleton:

```python
# anywhere in the codebase
from researchops.config.settings import settings

print(settings.db_path)   # Path("data/researchops.db") by default
print(settings.log_level) # "INFO" by default
```

Functions are the first tool for keeping logic understandable. A good function does one thing, has a short name based on the domain, and returns a value rather than printing everything. Returning values makes testing easier.

```python
# src/researchops/utils/paths.py
from pathlib import Path
import logging

log = logging.getLogger(__name__)


def find_pdfs(directory: Path, recursive: bool = False) -> list[Path]:
    """Return a sorted list of PDF files found in *directory*."""
    if not directory.exists():
        raise NotADirectoryError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdfs = sorted(directory.glob(pattern))
    log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
    return pdfs
```

The function raises `NotADirectoryError` for invalid input and returns a sorted list for predictable output — both choices make the function easy to test.

## Python collections

Use a `list` when order matters and duplicates are allowed. Use a `set` when you want unique values. Use a `dict` when you want named fields or key-value lookup. Use a `tuple` when the shape is fixed and immutable.

```python
pdf_paths: list[Path] = [Path("a.pdf"), Path("b.pdf")]
seen_ids: set[str] = {"abc123", "def456"}
paper_meta: dict[str, str] = {"title": "Graph Search", "author": "Ada"}
version: tuple[int, int, int] = (1, 0, 0)
```

## Virtual environment and editable install

A virtual environment keeps project dependencies isolated from the system Python:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The `-e` flag means editable install. Your code lives in the repository, but Python treats it as an installed package. After installing, you can run:

```bash
python -c "import researchops; print('import ok')"
researchops --help
```

## pyproject.toml entry point

`pyproject.toml` declares package metadata, dependencies, and tool configuration. The CLI entry point tells the packaging tool which Python object to expose as a shell command:

```toml
[project.scripts]
researchops = "researchops.cli.main:app"
```

That line means: create a shell command named `researchops` that calls the `app` object in `researchops/cli/main.py`. After `pip install -e .`, typing `researchops` in your terminal runs that Typer app.

## Circular imports

Be careful with imports. If `a.py` imports from `b.py` and `b.py` imports from `a.py`, you create a circular import. The fix is usually to move the shared code into a third module — `utils/` is often the right place for project-wide helpers that nothing else should depend on.

If something fails, read the traceback from the bottom up. Usually the last few lines tell you which module import or function call actually broke. That debugging habit matters every week of this curriculum.
