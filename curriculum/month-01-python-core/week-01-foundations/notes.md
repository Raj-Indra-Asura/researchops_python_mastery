# Notes - Week 01 Foundations

# Chapter 1: Python Foundations and Repository Setup

## 1. Chapter overview

This chapter turns basic Python knowledge into project-level Python understanding. You already know how to write variables, loops, functions, and conditionals. This week teaches you what happens when those pieces need to live inside a real repository that other tools, tests, and future teammates can understand.

ResearchOps is a production-style learning project. It will eventually scan research papers, parse documents, store records, search data, expose an API, and support machine-learning workflows. None of that later work is safe if the repository is confusing from day one. Week 1 therefore focuses on the foundation: environment setup, repository layout, package layout, a command-line entry point, a small utility function, and tests.

The visible feature is simple: `researchops scan PATH`. The invisible lesson is bigger: you are learning how software becomes installable, importable, testable, and maintainable.

By the end of this chapter, you should understand not only what commands to run, but why they exist, what files control them, and how execution flows through the project.

---

## 2. What you already know from previous weeks

This is Week 1, so there are no previous course chapters. Instead, we assume you already know Python basics:

- variables and assignment
- strings, integers, booleans
- lists and dictionaries
- `if`/`else`
- `for` loops
- defining and calling functions
- basic imports
- basic return values

You do **not** need to already understand:

- Python packaging
- repository structure
- virtual environments
- editable installs
- CLI entry points
- pytest discovery
- linting
- CI

Those are the new ideas this chapter teaches.

A useful way to think about the chapter is this:

- your existing Python knowledge teaches you how to write code **inside one file**
- this chapter teaches you how many files work **together as one project**

---

## 3. What problem this week solves

A beginner can often write a script that works on their machine. Professional work asks a harder question: can the code be installed, imported, tested, and extended predictably?

Week 1 solves several problems at once.

### Problem A: "My code only works when I run it from one exact folder."

That usually means the project is not packaged cleanly. A proper package layout and `src/` structure reduce that confusion.

### Problem B: "I can run a file directly, but I don't know how a real CLI command appears in the terminal."

A CLI entry point in `pyproject.toml` solves that.

### Problem C: "I changed something and now I don't know if the project still works."

Tests solve that.

### Problem D: "My code and output are mixed together."

Small utilities that return values, plus CLI code that handles presentation, solve that.

### Problem E: "The project already feels messy, and it is only Week 1."

Intentional structure solves that. The goal is not to add bureaucracy. The goal is to create a shape that can survive growth.

So the chapter is not "terminal trivia." It is the answer to a real engineering problem: turning isolated Python code into a coherent software project.

---

## 4. Beginner mental model

Before definitions, build a picture in your head.

### Mental model 1: repository vs package vs module

```text
Repository
├── pyproject.toml
├── src/
│   └── researchops/
│       ├── __init__.py
│       ├── cli/
│       │   └── main.py
│       └── utils/
│           └── paths.py
└── tests/
```

Read that slowly:

- the **repository** is the whole project folder
- the **package** is `researchops`
- a **module** is a single `.py` file like `main.py` or `paths.py`

### Mental model 2: terminal command to Python execution

```text
You type: researchops scan ./papers
            |
            v
Shell finds the installed command named researchops
            |
            v
Entry point points to researchops.cli.main:app
            |
            v
Typer parses the command and options
            |
            v
scan() runs
            |
            v
scan() calls find_pdfs()
            |
            v
find_pdfs() returns Path objects
            |
            v
CLI formats and prints output
```

### Mental model 3: separation of concerns

```text
Utility function
- takes input
- returns data
- easy to test

CLI command
- accepts user arguments
- calls utility/service
- prints user-facing output
```

That separation is one of the most important design habits in the chapter.

### Mental model 4: why `src/` exists

```text
repo root
├── pyproject.toml
├── src/
│   └── researchops/
└── tests/
```

The `src/` folder forces tools and developers to be explicit about where importable code lives. That is stricter than putting the package directly at the repo root, and that strictness is helpful.

---

## 5. Core vocabulary

These terms should become part of your working language.

### Repository
The full project folder, including code, tests, docs, and configuration.

### Package
An importable Python directory such as `src/researchops/`.

### Module
A single Python file, such as `paths.py`.

### `__init__.py`
A file that marks a directory as a package and may optionally run package-level code.

### Virtual environment
An isolated Python environment for one project.

### Dependency
A library your project needs, such as `typer` or `pytest`.

### Editable install
A development install where Python points to your working source code rather than a copied package snapshot.

### CLI
Command-line interface. A way to use a program from the terminal.

### Entry point
A mapping from a shell command name to a Python object.

### Linter
A tool that checks code for likely mistakes or style issues.

### Test discovery
The process by which pytest automatically finds test files and test functions.

### Assertion
A statement in a test that declares what must be true.

### Traceback
Python’s error report showing the chain of calls that led to a failure.

### Working directory
The directory your terminal command is currently operating in.

### CI
Continuous Integration: automated checks that run when code changes.

---

## 6. Concept explanations from first principles

### What is a repository?

A repository is the home of the whole software project. It contains more than code. It also contains tests, documentation, configuration, and project metadata. In this project, `pyproject.toml`, `src/`, `tests/`, and `curriculum/` all live in the repository root.

A repository is therefore a **project container**. The Python package is just one part of it.

### What is a Python package vs a module?

A module is a single `.py` file. A package is a directory that Python treats as importable. In this repository:

- `src/researchops/cli/main.py` is a module
- `src/researchops/cli/` is a package or subpackage
- `src/researchops/` is the main package

When you write:

```python
from researchops.utils.paths import find_pdfs
```

you are saying:

1. start at package `researchops`
2. go into subpackage `utils`
3. open module `paths`
4. import the name `find_pdfs`

### What is `__init__.py` and what does it actually do?

At the beginner level, `__init__.py` does two things.

1. It marks a directory as a package in the classic packaging model.
2. It can optionally contain package-level code, docstrings, exports, or constants.

What it does **not** do:

- it does not install the package
- it does not automatically create CLI commands
- it does not fix broken imports by magic

A minimal `__init__.py` is often enough. That is normal.

### What is the `src/` layout and why use it?

The `src/` layout means your importable package code lives under `src/` rather than directly in the repository root.

```text
repo/
├── src/
│   └── researchops/
└── tests/
```

Why use it?

- it separates project metadata from package code
- it makes imports more honest
- it reduces accidental success caused by the current working directory
- it scales better for real projects

If your package sits at the repo root, Python may import it simply because you are standing in the root folder. That can hide packaging mistakes. With `src/`, you must deliberately expose the package through installation or tool config.

### Why do virtual environments exist?

Different projects often need different dependency versions. A virtual environment gives one project its own isolated Python space. That space holds:

- installed packages
- Python wrappers
- command scripts

This prevents dependency collisions and keeps system Python cleaner. It also makes projects more reproducible because the environment can be rebuilt from the project’s declared dependencies.

### What is an editable install and why does `-e` matter?

A normal install places a built copy of the package into the environment. An editable install instead points the environment at your working source tree. That means if you edit `src/researchops/utils/paths.py`, the installed environment sees the new code immediately.

This matters during development because you do not want to reinstall the package after every small change.

### What does `pyproject.toml` do?

`pyproject.toml` is the modern coordination file for Python projects. It can define:

- build-system information
- project metadata
- dependencies
- CLI entry points
- tool configuration for pytest, Ruff, mypy, and more

In this repository, it is the central contract between your code and the tools around your code.

### What is a CLI? What is Typer?

A CLI is a command-line interface. Instead of clicking buttons, users type commands such as:

```bash
researchops scan ./papers
```

Typer is a library that turns Python functions with type hints into CLI commands. It handles argument parsing, help text, option parsing, and user input validation based on the function signature.

### What is pytest and how does it find tests?

Pytest is the test runner used in this project. It discovers tests automatically by looking for files and functions that follow test naming conventions. This repo also configures pytest in `pyproject.toml`, telling it:

- where tests live (`tests`)
- which default options to use
- where package code lives (`src`)

That is why `pytest -q` can usually run the suite without additional setup.

### What is Ruff?

Ruff is the project’s linter. A linter is not a test runner. It checks code quality signals such as:

- unused imports
- undefined names
- suspicious patterns
- import ordering problems
- some style and upgrade opportunities

Tests ask, "does behavior work?"
Linters ask, "does the code smell wrong?"

### What is CI in plain language?

CI means Continuous Integration. In plain language, it means a robot runs checks when code changes. Those checks usually include installation, tests, and linting. CI matters because it gives fast, repeatable feedback that does not depend on human memory.

---

## 7. ResearchOps-specific application

These ideas are not abstract. They directly shape the project.

### Why the project starts with a CLI

ResearchOps is designed to grow into a larger system, but the course deliberately starts with a local CLI because it is the lowest-friction user interface. It lets you verify project behavior quickly before adding API complexity.

### Why `scan` is the first feature

Scanning a directory is a perfect Week 1 feature because it exercises many foundations at once:

- command-line arguments
- `Path` handling
- a simple boolean option
- input validation
- returned data vs printed data
- user-facing output formatting
- tests with `tmp_path`

### Why `utils/paths.py` already matters

Even a tiny project benefits from a place for reusable path logic. If the CLI does its own scanning inline, the first command becomes harder to test and harder to reuse later. `find_pdfs()` is small, but it teaches a big habit: place reusable logic in reusable modules.

### Why architecture shows up so early

The project’s architecture rules say the CLI layer should not contain business logic. Week 1 does not yet have big services, but it already demonstrates the boundary: CLI code wires inputs and outputs, while utility code does focused reusable work.

### Why this foundation matters for later ML work

Later chapters will introduce parsing, storage, services, search, and ML. All of that still depends on a stable package, a reproducible environment, and testable components. Week 1 is not a detour; it is the root system.

---

## 8. Code examples with every line explained

This section is long on purpose. It moves from raw files to annotated understanding.

### 8.1 Full annotated `pyproject.toml` walkthrough

Here is the current file.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "researchops"
version = "0.1.0"
description = "A Python-based research paper processing and experiment-tracking platform"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "ResearchOps" }]
keywords = ["research", "papers", "ml", "nlp", "cli"]

dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.scripts]
researchops = "researchops.cli.main:app"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.4.0",
    "mypy>=1.10.0",
]
storage = [
    "sqlalchemy>=2.0.0",
]
parsing = [
    "pypdf>=4.0.0",
]
ml = [
    "scikit-learn>=1.4.0",
    "numpy>=1.26.0",
    "pandas>=2.2.0",
]
api = [
    "fastapi>=0.111.0",
    "uvicorn[standard]>=0.30.0",
    "httpx>=0.27.0",
]
all = [
    "researchops[storage,parsing,ml,api]",
]

[tool.hatch.build.targets.wheel]
packages = ["src/researchops"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
pythonpath = ["src"]

[tool.coverage.run]
source = ["src/researchops"]
omit = ["tests/*"]

[tool.coverage.report]
show_missing = true
fail_under = 70

[tool.ruff]
src = ["src"]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
mypy_path = "src"
```

#### Annotated walkthrough by line group

- **Lines 1-3** define the build system. Hatchling is the tool used to build the package, and `hatchling.build` is the backend implementation.
- **Line 4** is a blank separator to keep sections readable.
- **Lines 5-13** define core project metadata: name, version, description, README file, minimum Python version, license, authors, and searchable keywords.
- **Line 14** is another separator.
- **Lines 15-20** define the default runtime dependencies. Typer powers the CLI, Rich formats terminal output, and Pydantic/Pydantic Settings support structured configuration.
- **Line 21** separates dependencies from scripts.
- **Lines 22-23** define the CLI entry point. This is the most important operational line in the file: it says the shell command `researchops` should execute the object `app` in module `researchops.cli.main`.
- **Line 24** separates scripts from optional extras.
- **Lines 25-31** define the `dev` extras group: pytest, pytest-cov, Ruff, and mypy. These tools are for development rather than end-user runtime behavior.
- **Lines 32-34** define storage-related optional dependencies, which preview later database work.
- **Lines 35-37** define parsing-related extras, specifically `pypdf`.
- **Lines 38-42** define machine-learning extras such as scikit-learn, NumPy, and pandas.
- **Lines 43-47** define API extras such as FastAPI, Uvicorn, and httpx.
- **Lines 48-50** define a convenience extras group called `all`, which installs all the major optional groups together.
- **Line 51** separates optional dependency groups from build-target configuration.
- **Lines 52-53** tell Hatch where the actual package code lives: `src/researchops`. This is where the `src/` layout becomes real to the build tool.
- **Line 54** separates build config from pytest config.
- **Lines 55-58** configure pytest. Tests live in `tests`, default output is verbose with short tracebacks, and `src` is added to the import path so tests can import the package cleanly.
- **Line 59** separates pytest from coverage.
- **Lines 60-62** configure coverage collection. Coverage should measure package code under `src/researchops` and ignore the test files themselves.
- **Line 63** separates coverage run config from coverage report config.
- **Lines 64-66** configure coverage reporting. Missing lines should be shown, and coverage should fail below 70%.
- **Line 67** separates coverage from Ruff.
- **Lines 68-71** configure Ruff. It should focus on `src`, use a line length of 88, and lint as Python 3.11 code.
- **Line 72** separates general Ruff settings from lint-rule selection.
- **Lines 73-75** define which Ruff rule families are enabled and which specific rule is ignored.
- **Line 76** separates Ruff from mypy.
- **Lines 77-80** configure mypy. Python 3.11 is the target, strict mode is enabled, and `src` is again declared as the code location.

The key insight is that `pyproject.toml` is a coordination hub, not a decorative metadata file.

### 8.2 Full annotated `src/researchops/cli/main.py` walkthrough

Here is the file.

```python
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
```

#### Annotated walkthrough by line group

- **Lines 1-14** are the module docstring. It names the file’s role, shows example commands, and states an architectural rule: the CLI layer is not supposed to contain business logic.
- **Line 17** imports postponed annotations support. This keeps type hints consistent and flexible.
- **Lines 19-20** import Typer and Rich’s `Console`, the main third-party tools used in the file.
- **Lines 22-23** import project-local configuration helpers: logging setup and settings.
- **Lines 25-30** construct the Typer application object named `app`. The command name, top-level help text, completion behavior, and Rich markup behavior are all declared here.
- **Line 32** constructs a Rich `Console` for styled output.
- **Lines 34-39** import and register subcommand groups. Even though Week 1 mainly cares about `scan`, the file is already shaped to support future commands like `ingest`, `papers`, and `search`.
- **Lines 42-49** define the callback function. `@app.callback()` means this function handles root-level app setup, including the `--verbose` option. When `verbose` is enabled, logging uses `DEBUG`; otherwise it respects configured settings.
- **Lines 52-54** are a comment banner marking the Week 1 command section. These lines carry no runtime behavior but improve readability.
- **Lines 57-66** define the `scan` command signature. `directory` is a required argument. `recursive` is an optional boolean flag exposed as `--recursive` and `-r`.
- **Lines 67-71** are the command docstring. They clarify that `scan` only discovers PDFs; it does not ingest or store them.
- **Lines 72, 74, and 76** are local imports of `Path`, `Table`, and `find_pdfs`. The function uses these names directly, and the local imports make the function’s dependencies obvious at the point of use.
- **Line 78** converts the incoming string argument into a `Path` object. This is the boundary where CLI text becomes filesystem-aware data.
- **Lines 80-84** delegate file discovery to `find_pdfs()` and handle the expected error case. If the path is invalid, the command prints a red error and exits with status code `1`.
- **Lines 86-88** handle the empty-result case. No PDFs found is still a valid run, so the command prints a friendly message and exits with code `0`.
- **Lines 90-93** create a Rich table and declare its columns. Presentation belongs in the CLI layer, so this code lives here rather than in the utility module.
- **Lines 95-97** loop over the returned `Path` objects, compute file size in kilobytes, and add table rows.
- **Lines 99-100** print the table and a bold summary line.
- **Lines 103-104** provide the classic `if __name__ == "__main__":` guard so the file can be run directly during development as well as via the installed entry point.

What matters most is not Typer syntax. What matters most is the design shape: input parsing, error handling, delegation, and rendering are all visible and separated.

### 8.3 Full annotated `src/researchops/utils/paths.py` walkthrough

Here is the file.

```python
"""Path utilities for ResearchOps.

This module provides helpers for discovering and validating file paths.
It uses pathlib throughout — never os.path.
"""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def find_pdfs(directory: Path, recursive: bool = False) -> list[Path]:
    """Return a sorted list of PDF files found in *directory*.

    Args:
        directory: The directory to scan.
        recursive: If True, search all subdirectories as well.

    Returns:
        A sorted list of Path objects pointing to .pdf files.

    Raises:
        NotADirectoryError: If *directory* does not exist or is not a directory.
    """
    if not directory.exists():
        raise NotADirectoryError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdfs = sorted(directory.glob(pattern))
    log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
    return pdfs


def ensure_dir(path: Path) -> Path:
    """Create *path* and all parent directories if they don't exist.

    Returns the path so callers can use this inline:
        db_path = ensure_dir(settings.db_path.parent) / "researchops.db"
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_resolve(path: Path) -> Path:
    """Return a resolved absolute path without raising on symlink loops."""
    try:
        return path.resolve()
    except OSError:
        return path.absolute()
```

#### Annotated walkthrough by line group

- **Lines 1-5** are the module docstring. They tell you this file owns path helpers and that the project standard is `pathlib`, not `os.path`.
- **Line 7** imports postponed annotations support.
- **Lines 9-10** import the standard library modules used here: `logging` and `Path`.
- **Line 12** creates a module-level logger named after the module’s import path.
- **Line 15** declares `find_pdfs(directory: Path, recursive: bool = False) -> list[Path]`. Even before reading the body, you know the function’s input and output contract.
- **Lines 16-27** are the docstring. They explain what the function does, what arguments it expects, what it returns, and which exception it raises for invalid input.
- **Lines 28-31** validate the path. First the function checks whether the path exists. Then it checks whether the path is actually a directory. Both failure cases raise `NotADirectoryError` with explicit messages.
- **Line 33** chooses the glob pattern. `*.pdf` means top-level only; `**/*.pdf` means recursive traversal.
- **Line 34** runs the glob and sorts the results. Sorting is important because filesystem iteration order is not guaranteed to be stable.
- **Line 35** logs a debug message showing how many PDFs were found.
- **Line 36** returns the list of `Path` objects. That return value is what makes the function reusable and testable.
- **Lines 39-46** define `ensure_dir()`. The docstring explains both the side effect and the returned value. `mkdir(parents=True, exist_ok=True)` makes the function safe for nested creation and repeated calls.
- **Lines 49-54** define `safe_resolve()`. The function first tries `path.resolve()`, then falls back to `path.absolute()` if resolution raises `OSError`. This is a good example of graceful degradation.

This file is tiny, but it already demonstrates several professional habits: explicit contracts, standard-library-first design, narrow responsibilities, and test-friendly behavior.

### 8.4 Full annotated `tests/unit/test_paths.py` walkthrough

Here is the file.

```python
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
```

#### Annotated walkthrough by line group

- **Lines 1-9** set up the test file: docstring, postponed annotations, imports, and imports of the code under test.
- **Lines 12-17** define a sorting test. The setup creates `b.pdf` and `a.pdf`, the action calls `find_pdfs`, and the assertion proves the result is alphabetically ordered.
- **Lines 19-25** define a filtering test. The setup mixes one PDF with non-PDF files, and the assertions confirm only the PDF remains.
- **Lines 27-29** define the empty-directory test. The expectation is an empty list, not `None` and not an exception.
- **Lines 31-33** define the missing-directory test using `pytest.raises(NotADirectoryError)`.
- **Lines 35-39** define the file-instead-of-directory test. This proves the function validates both existence and directory-ness.
- **Lines 41-51** define the recursive scan test. The setup creates a nested directory structure, then compares non-recursive and recursive results.
- **Lines 53-58** define the complementary non-recursive test: a nested PDF alone should not appear unless recursion is enabled.
- **Lines 61-67** test `ensure_dir()` by creating a nested directory and checking both the side effect and the return value.
- **Lines 69-71** test idempotence. Calling `ensure_dir()` on an existing directory should still be safe.

The important lesson is that tests are not vague. Each one encodes a single behavioral promise.

### 8.5 Full annotated `src/researchops/core/exceptions.py` walkthrough

Here is the file.

```python
"""Custom exception hierarchy for ResearchOps.

Rule: every exception the application raises should be a subclass of
ResearchOpsError so callers can catch the whole family with one clause.

These exceptions live in core/ and must not import from storage,
parsing, CLI, API, or any infrastructure layer.
"""


class ResearchOpsError(Exception):
    """Base class for all ResearchOps application errors."""


class ParsingError(ResearchOpsError):
    """Raised when a document cannot be parsed."""


class EmptyDocumentError(ParsingError):
    """Raised when a parsed document contains no extractable text."""

    def __init__(self, path: str) -> None:
        super().__init__(f"No text could be extracted from: {path}")
        self.path = path


class UnsupportedFileTypeError(ParsingError):
    """Raised when a file type is not supported (e.g. .docx instead of .pdf)."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Unsupported file type: {path}")
        self.path = path


class StorageError(ResearchOpsError):
    """Raised for database / persistence failures."""


class PaperNotFoundError(StorageError):
    """Raised when a paper ID does not exist in storage."""

    def __init__(self, paper_id: str) -> None:
        super().__init__(f"Paper not found: {paper_id}")
        self.paper_id = paper_id


class DuplicatePaperError(StorageError):
    """Raised when trying to insert a paper that already exists."""

    def __init__(self, paper_id: str) -> None:
        super().__init__(f"Paper already exists: {paper_id}")
        self.paper_id = paper_id


class SearchError(ResearchOpsError):
    """Raised for search-related failures."""


class EmptyQueryError(SearchError):
    """Raised when a search query is blank or whitespace-only."""

    def __init__(self) -> None:
        super().__init__("Search query must not be empty.")


class ConfigurationError(ResearchOpsError):
    """Raised when the application configuration is invalid or missing."""
```

#### Annotated walkthrough by line group

- **Lines 1-8** are the module docstring. The docstring explains not just what this file does, but also states a design rule: every application-level exception must extend `ResearchOpsError`. It also says that this module must not import anything from the outer layers. Reading a module docstring first is a good habit.
- **Line 11** defines `ResearchOpsError`. This is the root of the exception tree. It inherits from Python's built-in `Exception`. Its body contains only a docstring because no new behavior or attributes are needed at this base level. It exists purely to create a named group.
- **Line 14** defines `ParsingError`. This is a narrower specialization. Anything that goes wrong during document parsing should raise `ParsingError` or one of its subclasses. Notice that `ParsingError` inherits from `ResearchOpsError`, not from `Exception` directly. That keeps the hierarchy connected.
- **Lines 17-21** define `EmptyDocumentError`. The `__init__` method accepts a `path` string. It calls `super().__init__(...)` with a formatted message. This is the standard way to pass a message upward to `Exception`. It also stores `self.path = path`. Storing the path attribute lets callers inspect which file caused the error programmatically, not just by reading the string.
- **Lines 24-28** define `UnsupportedFileTypeError`. Same pattern as `EmptyDocumentError`. Different meaning: this error is for file type mismatches, such as accidentally sending a `.docx` through a PDF-only pipeline.
- **Line 31** defines `StorageError`. The base class for database and persistence failures. Callers who want to catch any storage problem can catch `StorageError` in one `except` clause.
- **Lines 34-38** define `PaperNotFoundError`. When a paper ID cannot be found in the database, this is the right exception to raise. The `paper_id` attribute lets the caller log or display which paper was missing without parsing the message text.
- **Lines 41-45** define `DuplicatePaperError`. Used when inserting a paper that already exists. Storing `paper_id` again lets callers respond programmatically.
- **Lines 48-49** define `SearchError` with no custom `__init__`.
- **Lines 52-55** define `EmptyQueryError`. No custom attributes needed here because an empty query carries no useful metadata beyond the message.
- **Lines 58-59** define `ConfigurationError`. Used when the application detects a missing or invalid configuration at startup.

#### The exception hierarchy as a tree

```text
Exception (built-in)
  └── ResearchOpsError
        ├── ParsingError
        │     ├── EmptyDocumentError
        │     └── UnsupportedFileTypeError
        ├── StorageError
        │     ├── PaperNotFoundError
        │     └── DuplicatePaperError
        ├── SearchError
        │     └── EmptyQueryError
        ├── ConfigurationError
        ├── MLError
        │     ├── ModelNotTrainedError
        │     └── InsufficientDataError
        └── JobError
              └── JobNotFoundError
```

This tree structure matters. A caller can catch `ResearchOpsError` to handle any application failure. A caller can catch `StorageError` to handle only storage failures. A caller can catch `PaperNotFoundError` to respond to a very specific situation. Each level of the tree gives callers different degrees of precision.

#### Why this file lives in `core/` and nowhere else

The module docstring says these exceptions must not import from storage, CLI, API, or any other outer layer. That rule exists because `core/` is the stable center of the architecture. Services, repositories, the CLI, the API, and future workers can all import from `core/`. If `core/` imported from those layers in return, you would have circular imports and fragile architecture. The exception hierarchy is shared language. Shared language belongs in the center.

#### What Week 1 does with this file

Week 1 does not directly raise `ParsingError` or `StorageError`. Those features come later. But `NotADirectoryError` is used in `find_pdfs()`, and the CLI catches it there. The exceptions file is presented in Week 1 because understanding the structure of the hierarchy makes later chapters easier to follow.

---

### 8.6 Full annotated `tests/e2e/test_cli.py` walkthrough

Here is the file.

```python
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
```

#### Annotated walkthrough by line group

- **Line 1** is the module docstring. It says these are end-to-end tests using Typer's test runner. "E2E" means the test exercises the whole chain from the CLI interface down to file discovery, rather than testing a single function in isolation.
- **Lines 3-9** contain imports. `from __future__ import annotations` keeps type hint processing consistent. `Path` is needed for `tmp_path` parameter types. `CliRunner` is Typer's built-in test helper. `app` is the Typer application object imported from the main CLI module.
- **Line 11** creates a single shared `runner` at module level. `CliRunner` is lightweight, stateless, and safe to reuse. Creating it once here avoids repeating `CliRunner()` in every test method.
- **Lines 14-21** define `TestCLIHelp`. These two tests verify the application's help behavior.
  - `test_help_exits_zero` calls `runner.invoke(app, ["--help"])`. The `invoke` method runs the Typer app in-process with the given arguments. `result.exit_code` contains the integer exit status. `assert result.exit_code == 0` proves that asking for help succeeds cleanly.
  - `test_help_contains_scan` invokes the same help, then checks that the word `scan` appears somewhere in `result.output`. `.lower()` avoids case sensitivity. This test ensures the `scan` command remains discoverable through help text.
- **Lines 24-60** define `TestScanCommand`. These tests verify the `scan` command's behavior across different scenarios.
  - `test_scan_empty_directory` uses `tmp_path`, a pytest built-in fixture that provides a real temporary directory guaranteed to be empty and isolated. The test scans an empty directory and asserts that the exit code is zero. Empty directories are not errors. The assertion on `result.output` uses `or` because the exact message wording may vary.
  - `test_scan_lists_pdf_files` creates two fake PDF files using `.touch()`. Then it invokes the scan command and asserts both filenames appear in the output. Note that `.touch()` creates zero-byte files. The `scan` command does not read their content; it only checks that they exist and match `*.pdf`.
  - `test_scan_ignores_non_pdf_files` verifies the exclusion contract. A `readme.txt` is created alongside a `.pdf` file. After scanning, the test asserts that `readme.txt` does not appear in the output.
  - `test_scan_nonexistent_directory` passes a path that is almost certainly missing. The assertion is that the exit code is not zero. It does not check the exact error message, which makes the test slightly more robust against message wording changes.
  - `test_scan_recursive_flag` sets up a nested directory structure with a top-level and a nested PDF. Two invocations are run: one without `--recursive` and one with. The assertions verify that non-recursive mode misses the nested file and recursive mode includes it. This test protects the `recursive` parameter's behavior contract.

#### Why these are called end-to-end tests

Unit tests in `tests/unit/` call `find_pdfs()` directly, bypassing the CLI. E2E tests in `tests/e2e/` go through the full command path: Typer parses arguments, the callback runs, the `scan` function runs, `find_pdfs()` is called, and the result is formatted and printed. The `CliRunner` captures the output and exit code. This is "end-to-end" because it exercises the full chain without a real terminal.

#### What `result` contains

After `runner.invoke(app, [...])`:

- `result.exit_code` is an integer, usually `0` for success or a non-zero value for failure.
- `result.output` is a string containing everything the command printed to standard output.
- `result.exception` holds any unhandled exception that leaked out. If your tests fail unexpectedly, `result.exception` is often the clue.

#### The difference between unit tests and E2E tests in this project

```text
Unit test (tests/unit/test_paths.py)
  - calls find_pdfs() directly
  - does not involve Typer, CLI argument parsing, or console output
  - fast and precise
  - best for testing function contracts

E2E test (tests/e2e/test_cli.py)
  - invokes the full Typer app with a simulated argument list
  - exercises argument parsing, callback, command logic, and output formatting
  - tests the "public contract" of the CLI
  - slightly more realistic
  - still fast because CliRunner runs in-process (no subprocess)
```

Both kinds are necessary. Unit tests tell you whether `find_pdfs()` works correctly. E2E tests tell you whether the wiring between arguments, the command function, the utility, and the output is correct.

---

### 8.7 Execution flow diagram: terminal → CLI entry → scan → find_pdfs → output

```text
Terminal
  |
  | user types: researchops scan ./papers --recursive
  v
Installed script entry point
  |
  | defined in pyproject.toml as researchops = researchops.cli.main:app
  v
Typer application object: app
  |
  | parses command-line arguments and options
  v
scan(directory="./papers", recursive=True)
  |
  | converts string to Path
  v
path = Path("./papers")
  |
  | delegates file discovery
  v
find_pdfs(path, recursive=True)
  |
  | validates path
  | chooses glob pattern
  | returns sorted list[Path]
  v
scan receives data
  |
  | empty result -> friendly message, exit 0
  | invalid path -> error message, exit 1
  | found PDFs -> build table and print summary
  v
Console output shown to user
```

The execution flow matters because it shows the layer boundaries clearly:

- terminal command is user input
- `pyproject.toml` creates the entry point
- Typer parses commands
- `scan()` orchestrates
- `find_pdfs()` does reusable discovery work
- Rich handles terminal presentation

---

## 9. Common beginner mistakes

Each mistake below includes the mistake, the fix, and the reason.

### Mistake 1 — Confusing repository with package

**Mistake:** assuming the whole repo is the importable package.

**Fix:** remember that the package is `src/researchops/`, while the repository contains many other things too.

**Why it matters:** if you confuse these, imports and tool behavior feel random.

### Mistake 2 — Forgetting to activate the virtual environment

**Mistake:** running install or test commands against the wrong Python.

**Fix:** activate `.venv` before using project commands.

**Why it matters:** otherwise you may debug the wrong environment instead of the real problem.

### Mistake 3 — Thinking editable install copies your code permanently elsewhere

**Mistake:** assuming `-e` works like a frozen duplicate.

**Fix:** understand that editable install points Python at your working source tree.

**Why it matters:** this explains why code changes are visible immediately after editing.

### Mistake 4 — Putting all logic inside the CLI command

**Mistake:** making `scan()` discover files, parse them, print them, and later maybe store them too.

**Fix:** keep CLI code focused on input parsing, orchestration, and output.

**Why it matters:** thin entry points are easier to test and easier to extend.

### Mistake 5 — Returning inconsistent types

**Mistake:** returning `None` in one branch and `list[Path]` in another.

**Fix:** preserve a stable return contract. For no matches, return `[]`.

**Why it matters:** stable return types simplify both caller logic and tests.

### Mistake 6 — Ignoring sort order

**Mistake:** trusting filesystem iteration order.

**Fix:** sort the results explicitly.

**Why it matters:** deterministic output makes tests reliable and user output predictable.

### Mistake 7 — Catching `Exception` too broadly

**Mistake:** swallowing all errors with a vague `Something went wrong`.

**Fix:** catch expected exceptions precisely and preserve useful error messages.

**Why it matters:** broad exception handling hides the clues you need for debugging.

### Mistake 8 — Treating tests as optional because the code looks simple

**Mistake:** skipping test runs after small changes.

**Fix:** run tests anyway.

**Why it matters:** simple code breaks too, and tests provide evidence rather than feelings.

### Mistake 9 — Reading only the first line of a traceback

**Mistake:** stopping before you find the real failing import or line.

**Fix:** read from the bottom upward.

**Why it matters:** the bottom of the traceback often contains the most specific failure context.

### Mistake 10 — Printing inside utility functions

**Mistake:** mixing computation and presentation in lower-level helpers.

**Fix:** let utilities return data and let the CLI render it.

**Why it matters:** returned data is easier to test, reuse, and compose.

---

## 10. Debugging guidance

### Step 1: classify the failure

Ask whether the problem is one of these:

- installation problem
- import problem
- CLI parsing problem
- logic problem
- test expectation problem

Correct classification narrows the search space.

### Step 2: run the smallest useful command

Use tiny smoke tests when possible:

```bash
python -c "import researchops; print('import ok')"
python -c "from researchops.cli.main import app; print(type(app).__name__)"
researchops --help
pytest tests/unit/test_paths.py -v
```

These commands let you isolate layers quickly.

### Step 3: read tracebacks from the bottom upward

A traceback is a stack of calls. The last part often shows the real exception type and the file/line that triggered it.

When you read a traceback, ask:

- what exception type is this?
- what module failed?
- what line number failed?
- what was Python trying to do at that point?

### Step 4: inspect the contract

For `find_pdfs()`, the contract is clear:

- input: a `Path` pointing to a directory
- option: `recursive` boolean
- output: `list[Path]`
- failures: `NotADirectoryError` for invalid directories

If behavior changes, compare the new behavior against that contract.

### Step 5: rerun narrow tests first

If you changed a path utility, start with `tests/unit/test_paths.py`. If those pass, then run the broader suite.

### Common checks when things break

- Is `.venv` activated?
- Did I install with `-e`?
- Did I change `pyproject.toml` and forget to reinstall?
- Did I misspell an import path?
- Did I change a return type?
- Did I accidentally remove sorting?
- Did I break recursive behavior?

### Reading common failures in plain language

- `ModuleNotFoundError` usually means Python could not find a named module or package.
- `NotADirectoryError` means code expected a directory path and did not get a valid one.
- An assertion failure usually means the code returned a different value or type than the test expected.

Debugging gets easier when you translate errors into plain English instead of treating them as magic.

---

## 11. Design tradeoffs

### Why `src/` layout?

**Benefit:** clearer packaging and fewer accidental imports.

**Cost:** tools need explicit configuration.

**Why it is worth it:** the project is meant to grow, and stricter structure helps early.

### Why editable install?

**Benefit:** fast development loop.

**Cost:** you must understand installation and environment setup.

**Why it is worth it:** development without constant reinstalls is far more pleasant.

### Why `pathlib` instead of `os.path`?

**Benefit:** cleaner, object-oriented path handling with readable methods like `.exists()`, `.is_dir()`, `.glob()`, and `.resolve()`.

**Cost:** beginners must learn `Path` objects rather than only strings.

**Why it is worth it:** readability and correctness both improve.

### Why return values instead of printing inside helpers?

**Benefit:** easier testing and reuse.

**Cost:** the caller must handle presentation.

**Why it is worth it:** separation of concerns scales better.

### Why start with CLI instead of API?

**Benefit:** lower complexity, faster local validation.

**Cost:** no network interface yet.

**Why it is worth it:** the course intentionally proves local behavior before adding distributed complexity.

---

## 12. Testing implications

This week quietly teaches what makes code testable.

### Clear inputs

`find_pdfs(directory: Path, recursive: bool = False)` is testable because the inputs are explicit and easy to construct.

### Clear outputs

A returned `list[Path]` is easy to assert against.

### Explicit failures

`pytest.raises(NotADirectoryError)` works because the function fails in a deliberate, documented way.

### Limited side effects

`find_pdfs()` does not print. That keeps the function simple to test.

### Why `tmp_path` is powerful

`tmp_path` gives each test its own temporary directory. That means tests can create files and directories safely without touching real project data or depending on another test’s leftovers.

### Unit tests vs CLI tests

- unit tests focus on one small function
- CLI tests verify behavior through the application interface

Both matter. Unit tests are precise. CLI tests prove the wiring works.

---

## 13. Architecture implications

The repository already follows layered thinking, even in Week 1.

```text
CLI / API / Workers
        |
        v
Services / Use Cases
        |
        v
Core Models + Protocols
        ^
        |
Infrastructure implementations
```

Week 1 mostly touches the CLI layer and reusable utilities. The important lesson is that the CLI is an entry point, not the whole system. It translates user intent into calls to lower-level logic.

The current `scan` command is healthy because it does not own the entire filesystem-discovery algorithm. It delegates to `find_pdfs()`. Later, other layers will grow around that discipline:

- services will orchestrate use cases
- storage modules will handle persistence
- parsing modules will handle PDF extraction
- core will stay free of infrastructure-specific imports

Architecture is easier to maintain when boundaries are respected early.

---

## 14. How this connects to AI/ML engineering

AI/ML engineering often looks glamorous from far away: models, embeddings, experiments, evaluation. But those systems still depend on unglamorous fundamentals.

### Virtual environments matter even more in ML

ML stacks often have many dependencies. Version conflicts are common. If you cannot manage environments, ML work becomes fragile fast.

### Reproducibility begins before model training

Reproducibility is not just about random seeds. It also means knowing:

- which Python version
- which dependencies
- which project structure
- which commands

Week 1 starts that discipline.

### Real packages beat notebook copy-paste

ML projects often suffer when logic is copied between notebooks and scripts. A real package encourages reusable modules instead of scattered duplication.

### Testable utilities help data pipelines too

Even if later chapters deal with parsing and ML, the boring path utilities still matter. Reliable pipelines are built from reliable small parts.

### CI matters for research tooling

Experiments are only trustworthy when the surrounding codebase remains healthy. CI helps preserve that health.

---

## 15. Mini quizzes

### Quiz 1
**Question:** What is the difference between a repository and a package?

**Answer:** The repository is the whole project folder. The package is the importable Python code unit inside it, such as `src/researchops/`.

### Quiz 2
**Question:** What does the `-e` flag do during installation?

**Answer:** It installs the project in editable mode so the environment points to your working source code.

### Quiz 3
**Question:** Why is `src/` layout useful?

**Answer:** It separates package code from repo metadata and catches packaging mistakes more honestly.

### Quiz 4
**Question:** Why does `find_pdfs()` return a list instead of printing file names?

**Answer:** Returning data makes the function reusable and easy to test. Printing belongs in the CLI layer.

### Quiz 5
**Question:** What does `researchops = "researchops.cli.main:app"` mean?

**Answer:** It creates a shell command named `researchops` that targets the `app` object in module `researchops.cli.main`.

### Quiz 6
**Question:** What is the difference between a unit test and a CLI test in this repo?

**Answer:** A unit test checks one function directly. A CLI test invokes the application through its command interface.

### Quiz 7
**Question:** Why does pytest need `pythonpath = ["src"]` here?

**Answer:** Because the package lives under `src`, and pytest needs that path available for imports during tests.

### Quiz 8
**Question:** Is “no PDFs found” an error?

**Answer:** No. It is a valid empty result, so the CLI exits with code `0`.

---

## 16. Explain-it-aloud prompts

Practice these aloud without notes.

1. Explain how a shell command becomes a Python object being executed.
2. Explain why this repository uses `src/` layout.
3. Explain why a virtual environment is useful even for a small project.
4. Explain why `find_pdfs()` is easier to test than a function that only prints.
5. Explain the difference between an invalid path and an empty result.

---

## 17. What to memorize

Memorize these anchors:

- the package lives in `src/researchops`
- the CLI entry point is `researchops.cli.main:app`
- the shell command is `researchops`
- pytest looks in `tests`
- `find_pdfs()` returns `list[Path]`
- `recursive=True` means recursive globbing
- Ruff is the linter
- CI means automated checks on code changes

---

## 18. What to understand deeply

Understand these ideas, not just the commands:

- project structure shapes developer experience
- thin interfaces are easier to test and extend
- returning data is a design choice, not just a syntax habit
- explicit contracts reduce confusion
- tooling configuration is part of the software project itself

---

## 19. What not to worry about yet

Do not panic about advanced topics yet. You do **not** need to master:

- packaging internals beyond the sections you use
- every Typer feature
- advanced pytest fixture design
- Docker
- FastAPI
- database migrations
- vector search
- model training internals
- deployment infrastructure

The goal is a stable mental model for the current project, not encyclopedic knowledge.

---

## 20. PowerShell equivalents for Windows learners

All commands in this chapter use macOS/Linux shell syntax. If you are using Windows with PowerShell, the following equivalents apply.

### Creating a virtual environment

```bash
# macOS / Linux
python -m venv .venv
```

```powershell
# Windows PowerShell
python -m venv .venv
```

The `python -m venv .venv` command is identical on all platforms. The difference appears in the next step.

### Activating the virtual environment

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

On Windows, the activation script lives in `.venv\Scripts\` and is called `Activate.ps1`. If PowerShell execution policy blocks scripts, first run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry the activation command.

To confirm which Python is active after activation:

```powershell
# Windows PowerShell
where.exe python
```

```bash
# macOS / Linux
which python
```

### Upgrading pip

```bash
# macOS / Linux and Windows PowerShell (identical)
python -m pip install --upgrade pip
```

### Installing the project in editable mode

```bash
# macOS / Linux and Windows PowerShell (identical)
python -m pip install -e ".[dev]"
```

The quotes are important on Windows too.

### Import smoke test

```bash
# macOS / Linux and Windows PowerShell (identical)
python -c "import researchops; print('import ok')"
```

### Running the CLI

```bash
# macOS / Linux and Windows PowerShell (identical)
researchops --help
researchops scan PATH
researchops scan PATH --recursive
```

The shell command `researchops` works the same way on Windows once editable install succeeds, because pip creates a wrapper script in `.venv\Scripts\researchops.exe`.

### Running pytest

```bash
# macOS / Linux and Windows PowerShell (identical)
pytest
pytest tests/unit/test_paths.py -v
pytest tests/e2e/test_cli.py -v
pytest -q
```

### Running Ruff

```bash
# macOS / Linux and Windows PowerShell (identical)
ruff check src tests
```

### Checking exit codes

```bash
# macOS / Linux: $? holds the last exit code
researchops scan missing_path ; echo $?
```

```powershell
# Windows PowerShell: $LASTEXITCODE holds the last exit code
researchops scan missing_path ; echo $LASTEXITCODE
```

### Path separators

On Windows, filesystem paths use backslashes. However, most Python code that uses `pathlib.Path` handles this automatically. When passing paths as command arguments from PowerShell, you can use either `/` or `\` and the project will handle them correctly.

```powershell
researchops scan .\examples\sample_papers
researchops scan ./examples/sample_papers
```

Both forms work in PowerShell.

### Summary table

| macOS / Linux | Windows PowerShell |
|---|---|
| `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| `which python` | `where.exe python` |
| `echo $?` | `echo $LASTEXITCODE` |
| `python -m venv .venv` | same |
| `python -m pip install -e ".[dev]"` | same |
| `pytest -q` | same |
| `ruff check src tests` | same |
| `researchops --help` | same |

---

## 21. Bridge to next week

Week 1 teaches where the code lives, how the package is installed, how the CLI starts, and how tests describe behavior. Week 2 builds directly on that by going deeper into files, `pathlib`, exceptions, and logging.

That means the small Week 1 utilities are not throwaway exercises. They are the beginning of the project’s real filesystem behavior. If you can clearly explain the repository/package/module distinction, the CLI entry point, and the execution flow from `researchops scan` to `find_pdfs()`, you are ready to move forward.
