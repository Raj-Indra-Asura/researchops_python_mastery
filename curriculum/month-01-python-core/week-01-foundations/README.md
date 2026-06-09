<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 01 — Python Foundations:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ *(start of curriculum)* · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Chapter 1: Python Foundations and Repository Setup

## Story of the week

You are joining the ResearchOps project on day one.
The product vision is ambitious: a local-first platform that can scan research papers, ingest them, search them, and eventually support ML workflows, experiment tracking, semantic retrieval, and an API.
But none of that matters if the repository is confusing, the package cannot be imported, and the command line tool does not run.

This week is the moment where the project becomes real.
You are not building the full platform yet.
You are building the ground it will stand on.
You will learn how a Python repository is organized, how a package becomes installable, how a command-line interface starts, how tests prove behavior, and how a tiny utility function can become the seed of a larger architecture.

In ResearchOps, the first concrete user-facing behavior is simple:
scan a directory and list PDF files.
That sounds small, and it is.
It is also exactly the right size for learning the professional workflow without drowning in complexity.

---

## What you already know

Before this chapter, you are assumed to know basic Python programming:

- variables and assignment
- strings, integers, booleans, and lists
- `if`/`else`
- `for` loops
- function definition and return values
- basic importing such as `import math` or `from pathlib import Path`

You do **not** need to already understand:

- repository structure
- Python packaging
- virtual environments
- editable installs
- command-line entry points
- test discovery
- linting
- CI pipelines

Those are exactly what this chapter adds.

---

## What this week adds

This week turns “I can write Python” into “I can work inside a real Python project.”

You will add:

- a professional repository layout
- a `src/`-based package structure
- a command-line app powered by Typer
- project metadata and tooling inside `pyproject.toml`
- a small but real file-discovery utility
- unit tests and end-to-end CLI tests
- the habit of validating work from the terminal

---

## Why this matters

A lot of beginners can write a script.
Far fewer can explain why a repository is structured the way it is.
Even fewer can install their own package, run its CLI, and verify behavior with tests.

That gap matters.
Professional Python work is not just writing logic.
It is organizing logic so that:

- imports are predictable
- environments are reproducible
- tests are easy to run
- tools know where code lives
- later architecture can grow without collapse

If you skip these foundations, later weeks become frustrating.
If you learn them now, later weeks become much easier.

---

## Learning objectives

By the end of this chapter, you should be able to:

1. Explain the difference between a repository, a package, and a module.
2. Create and activate a Python virtual environment for this project.
3. Install the project in editable mode and explain what `-e` changes.
4. Read the important sections of `pyproject.toml` without guessing.
5. Describe why this project uses a `src/` layout instead of putting the package at the repository root.
6. Trace how the `researchops` shell command connects to `researchops.cli.main:app`.
7. Read the `scan` command in `src/researchops/cli/main.py` and explain its flow.
8. Explain why `find_pdfs()` returns data instead of printing directly.
9. Use `pathlib.Path` to work with directories and files safely.
10. Run pytest and identify which tests verify utilities versus CLI behavior.
11. Recognize the job of Ruff and the job of CI in a Python project.
12. Describe how Week 1 lays the architectural foundation for later services, storage, parsing, and ML layers.

---

## Project milestone

**Milestone:** the ResearchOps repository can be installed locally, imported as a package, and exercised through a working CLI command that scans directories for PDF files and is backed by tests.

That milestone sounds modest.
It is not.
It means the project has crossed from “folder of code” to “runnable software project.”

---

## Files touched this week

### Project files

- `pyproject.toml`  
  The project contract: package metadata, dependencies, entry points, pytest config, Ruff config, and mypy config.

- `src/researchops/__init__.py`  
  Marks `researchops` as a package and gives Python a stable import root.

- `src/researchops/cli/main.py`  
  Defines the Typer application, top-level callback, and the Week 1 `scan` command.

- `src/researchops/config/settings.py`  
  Central place for application settings so the CLI can read configuration consistently.

- `src/researchops/config/logging.py`  
  Logging setup used by the CLI callback.

- `src/researchops/utils/paths.py`  
  Small path utilities, including `find_pdfs()`, `ensure_dir()`, and `safe_resolve()`.

- `src/researchops/core/exceptions.py`  
  Beginning of the project’s domain-specific exception hierarchy.

### Test files

- `tests/unit/test_paths.py`  
  Fast tests for `find_pdfs()` and `ensure_dir()` using temporary directories.

- `tests/e2e/test_cli.py`  
  CLI-level tests using Typer’s `CliRunner` to simulate real command execution.

### Curriculum files

- `curriculum/month-01-python-core/week-01-foundations/README.md`  
  Weekly roadmap and success criteria.

- `curriculum/month-01-python-core/week-01-foundations/notes.md`  
  Full textbook chapter for this week.

- `curriculum/month-01-python-core/week-01-foundations/exercises.md`  
  Guided practice workbook.

- `curriculum/month-01-python-core/week-01-foundations/break_it.md`  
  Failure lab for deliberate debugging practice.

- `curriculum/month-01-python-core/week-01-foundations/validation.md`  
  Strict checkpoint for proving the week is complete.

- `curriculum/month-01-python-core/week-01-foundations/reflection.md`  
  Prompts for metacognition and readiness review.

---

## Commands introduced

```bash
python -m venv .venv
```
Create a project-specific virtual environment.

```bash
source .venv/bin/activate
```
Activate the virtual environment on macOS/Linux so project tools come from `.venv`.

```powershell
# Windows PowerShell equivalent
.venv\Scripts\Activate.ps1
```

```bash
python -m pip install --upgrade pip
```
Upgrade pip inside the virtual environment before installing dependencies.

```bash
python -m pip install -e ".[dev]"
```
Install the package in editable mode plus development tools like pytest and Ruff.

```bash
python -c "import researchops; print('import ok')"
```
Quick smoke test that proves the package imports successfully.

```bash
researchops --help
```
Show the CLI help text and verify that the entry point resolves.

```bash
researchops scan PATH
```
Run the Week 1 feature: scan one directory for PDF files.

```bash
researchops scan PATH --recursive
```
Search subdirectories as well.

```bash
pytest tests/unit/test_paths.py -v
```
Run the focused unit tests for path utilities.

```bash
pytest tests/e2e/test_cli.py -v
```
Run the CLI behavior tests.

```bash
pytest -q
```
Run the whole test suite quietly.

```bash
ruff check src tests
```
Run the linter to catch import, syntax, and style issues Ruff knows how to detect.

### Windows PowerShell notes

All commands except virtual environment activation are identical on Windows. On Windows, replace `source .venv/bin/activate` with `.venv\Scripts\Activate.ps1`. To confirm the environment is active, run `where.exe python` and verify the result points to `.venv\Scripts\python.exe`. To check an exit code after a command fails, use `echo $LASTEXITCODE` instead of `echo $?`.

---

## Tests involved

### Unit tests

From `tests/unit/test_paths.py`:

- `test_returns_sorted_list`
- `test_excludes_non_pdf_files`
- `test_returns_empty_for_empty_directory`
- `test_raises_for_nonexistent_directory`
- `test_raises_for_file_not_directory`
- `test_recursive_finds_nested_pdfs`
- `test_non_recursive_ignores_subdirectory_pdfs`
- `test_creates_directory`
- `test_existing_directory_is_idempotent`

These tests focus on pure behavior of small functions.
They are fast.
They isolate one unit at a time.

### End-to-end CLI tests

From `tests/e2e/test_cli.py`:

- `test_help_exits_zero`
- `test_help_contains_scan`
- `test_scan_empty_directory`
- `test_scan_lists_pdf_files`
- `test_scan_ignores_non_pdf_files`
- `test_scan_nonexistent_directory`
- `test_scan_recursive_flag`

These tests exercise the app through its command interface.
They are closer to real usage.

---

## Study plan for the week

### Day 1 — Orientation

- Read this README.
- Open the repository tree.
- Identify `src/`, `tests/`, and `curriculum/`.
- Read `pyproject.toml` once without trying to memorize it.
- Run `researchops --help` after installation and confirm the CLI exists.

### Day 2 — Environment and packaging

- Create `.venv`.
- Activate it.
- Install the project with `-e`.
- Practice explaining what an editable install means.
- Confirm `python -c "import researchops"` works.

### Day 3 — Repository structure and imports

- Read `src/researchops/cli/main.py`.
- Read `src/researchops/utils/paths.py`.
- Map which modules import which other modules.
- Explain package vs module vs repository aloud.

### Day 4 — CLI behavior

- Run `researchops scan` on a directory with no PDFs.
- Run it on a directory with one PDF.
- Run it with `--recursive`.
- Trace the flow from terminal command to utility function.

### Day 5 — Testing

- Read `tests/unit/test_paths.py` line by line.
- Read `tests/e2e/test_cli.py` line by line.
- Run tests individually, then together.
- Identify what behavior each test protects.

### Day 6 — Failure practice

- Work through the `break_it.md` experiments.
- Intentionally trigger import, CLI, and path-related failures.
- Practice reading tracebacks from bottom to top.

### Day 7 — Validation and reflection

- Use `validation.md` as a strict final checkpoint.
- Complete `reflection.md` honestly.
- If you cannot explain the week aloud, review before moving on.

---

## Estimated time breakdown

- Reading roadmap and notes: **2.5-4 hours**
- Environment setup and command practice: **1-2 hours**
- Code reading and walkthroughs: **2-3 hours**
- Exercises: **3-5 hours**
- Failure lab: **1.5-3 hours**
- Validation and reflection: **1-2 hours**

**Total estimated time:** **11-19 hours**

If you are brand new to terminal workflows, expect to land toward the high end.
That is normal.

---

## How to know you are stuck

You are probably stuck if any of these are true:

1. You can run commands by memory, but you cannot explain what they are doing.
2. You confuse the repository root with the Python package import root.
3. You can make `pytest` pass, but you do not know which test is checking what.
4. You still think `pip install -e .` copies your code somewhere else permanently.
5. You see a traceback and only read the first line instead of tracing where the failure actually happened.

If one or more of those is true, slow down.
Re-read the notes.
Then practice with smaller commands and explanations.

---

## Definition of done

- [ ] I created and activated a Python 3.11 virtual environment.
- [ ] I installed the project with `python -m pip install -e ".[dev]"`.
- [ ] I can explain what editable install means in plain language.
- [ ] I can point to the CLI entry point in `pyproject.toml`.
- [ ] I can explain the purpose of `src/researchops/`.
- [ ] I can run `researchops --help` successfully.
- [ ] I can run `researchops scan PATH` successfully.
- [ ] I understand why `find_pdfs()` returns a list instead of printing directly.
- [ ] I ran unit tests and CLI tests locally.
- [ ] I can explain the difference between unit tests and end-to-end tests.
- [ ] I can describe at least three common setup failures and how to debug them.
- [ ] I completed reflection honestly and know whether I am ready for Week 2.

---

## Bridge to next week

This chapter gives you a working project skeleton.
Next week builds on that skeleton by going deeper into files, `pathlib`, exceptions, and logging.
That means the things you learn here are not temporary setup trivia.
They are the basis for real file-handling behavior across the whole ResearchOps platform.

If Week 1 teaches you how the project starts,
Week 2 teaches you how the project touches the filesystem safely and predictably.
<!-- NAV_BOTTOM_START -->
---
⬅️ *(start of curriculum)* · ➡️ [Notes →](notes.md)

**Week 01 — Python Foundations:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
