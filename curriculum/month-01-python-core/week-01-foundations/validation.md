
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 1 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 01 — Python Foundations:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 01 Foundations

## Pre-validation checklist

Before you run the formal checks, confirm all of these are true:

- [ ] You are in the repository root.
- [ ] You are using Python 3.11 or newer.
- [ ] Your virtual environment is created.
- [ ] Your virtual environment is activated.
- [ ] The package has been installed with `-e`.
- [ ] You have read `pyproject.toml` at least once.
- [ ] You can point to `src/researchops/cli/main.py` and `src/researchops/utils/paths.py`.
- [ ] You know what `find_pdfs()` is supposed to return.
- [ ] You know what `researchops scan` is supposed to do on an empty directory.
- [ ] You are ready to explain failures, not just celebrate passing tests.

---

## Commands to run

Run these commands exactly, in order, from the repository root.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -c "import researchops; print('import ok')"
python -c "from researchops.cli.main import app; print(type(app).__name__)"
researchops --help
researchops scan curriculum/month-01-python-core/week-01-foundations
pytest tests/unit/test_paths.py -v
pytest tests/e2e/test_cli.py -v
pytest -q
ruff check src tests
```

If you want one extra smoke test for recursive behavior, also run:

```bash
researchops scan . --recursive
```

---

## Expected outputs

### Environment and install

For:

```bash
python -m pip install -e ".[dev]"
```

You should see successful installation output with no dependency-resolution failure.

### Import smoke tests

For:

```bash
python -c "import researchops; print('import ok')"
```

Expected:

```text
import ok
```

For:

```bash
python -c "from researchops.cli.main import app; print(type(app).__name__)"
```

Expected output includes:

```text
Typer
```

### CLI help

For:

```bash
researchops --help
```

You should see:

- the command name `researchops`
- descriptive help text
- at least the `scan` command
- exit code `0`

### Scan command

For:

```bash
researchops scan curriculum/month-01-python-core/week-01-foundations
```

You should see one of these outcomes:

- a friendly “No PDF files found” message if that directory contains no PDFs
- or a Rich table listing PDFs if PDFs exist

Both are acceptable.
A crash is not.

### Tests

For:

```bash
pytest tests/unit/test_paths.py -v
```

You should see the path utility tests collected and passing.

For:

```bash
pytest tests/e2e/test_cli.py -v
```

You should see the CLI tests collected and passing.

For:

```bash
pytest -q
```

You should see the full current test suite pass.

### Linting

For:

```bash
ruff check src tests
```

You should see either no issues or a clear report you can fix.
Week 1 is not complete if obvious lint problems remain in the current tracked code.

---

## Tests that must pass

These named tests are non-negotiable for Week 1 understanding.

### Unit tests

- `test_returns_sorted_list`
- `test_excludes_non_pdf_files`
- `test_returns_empty_for_empty_directory`
- `test_raises_for_nonexistent_directory`
- `test_raises_for_file_not_directory`
- `test_recursive_finds_nested_pdfs`
- `test_non_recursive_ignores_subdirectory_pdfs`
- `test_creates_directory`
- `test_existing_directory_is_idempotent`

### End-to-end CLI tests

- `test_help_exits_zero`
- `test_help_contains_scan`
- `test_scan_empty_directory`
- `test_scan_lists_pdf_files`
- `test_scan_ignores_non_pdf_files`
- `test_scan_nonexistent_directory`
- `test_scan_recursive_flag`

If any of these fail, you are not done.
You are still learning something important.

---

## Manual checks

Do these even if tests are green.

- [ ] I can explain where the `researchops` shell command comes from.
- [ ] I can point to the exact `[project.scripts]` entry in `pyproject.toml`.
- [ ] I can explain why the package lives under `src/researchops`.
- [ ] I can explain why `find_pdfs()` accepts a `Path`.
- [ ] I can explain what happens when the directory does not exist.
- [ ] I can explain the difference between a unit test and a CLI test in this repo.
- [ ] I can explain why returning values is easier to test than printing from utility functions.
- [ ] I can explain the meaning of `recursive=True` in plain language.
- [ ] I can read the scan command top to bottom without getting lost.

---

## Architecture checks

Week 1 is small, but architecture already matters.
Confirm all of these:

- [ ] `core/` is treated as the domain layer, not a dumping ground for CLI logic.
- [ ] `cli/` is an entry layer that wires commands and presentation.
- [ ] `utils/paths.py` contains reusable path helpers, not Rich table formatting.
- [ ] The CLI delegates file discovery to a helper instead of inlining everything.
- [ ] Business logic has not started leaking into Typer callback declarations.
- [ ] The `src/` layout keeps package imports explicit and professional.
- [ ] Tests import the package the way users will interact with it.

---

## Documentation checks

- [ ] I read the chapter README and understand the milestone.
- [ ] I read the notes chapter, not just the summary.
- [ ] I completed at least the core exercises.
- [ ] I practiced at least two failure experiments from `break_it.md`.
- [ ] I completed the reflection prompts honestly.
- [ ] I can link each validation command to the concept it verifies.

---

## Do-not-proceed warnings

Do **not** move to Week 2 if any of these are true:

- [ ] You cannot explain what `pip install -e` does.
- [ ] You do not understand why the package lives under `src/`.
- [ ] You only know that tests pass, but not what they are testing.
- [ ] You cannot tell the difference between a repository and a package.
- [ ] You panic when you see `ModuleNotFoundError` or `NotADirectoryError`.
- [ ] You have never run `researchops --help` yourself.
- [ ] You cannot trace the flow from terminal command to utility function.

If any box above is true, revisit the notes and exercises first.

---

## Ruthless mentor checkpoint

Answer these without opening the code if possible:

1. What does `researchops = "researchops.cli.main:app"` mean exactly?
2. Why is `src/` better than putting the package directly at repo root for this project?
3. Why is `find_pdfs()` easier to test than if it printed everything itself?
4. Why do we raise `NotADirectoryError` for invalid input instead of silently returning `[]`?
5. What is the difference between `researchops --help` passing and `pytest -q` passing?
6. Which layer should own Rich table formatting?
7. Which layer should own reusable path discovery logic?
8. Why do we use a virtual environment if Python is already installed on the machine?
9. What does pytest use `tmp_path` for?
10. If recursive scanning stops working, which two tests should fail first?

If you cannot answer at least 8 of 10 cleanly, review before advancing.

---

## Definition of done

- [ ] Environment created and activated correctly.
- [ ] Editable install works.
- [ ] Import smoke tests pass.
- [ ] CLI help works.
- [ ] `scan` works on at least one real path.
- [ ] Unit tests pass.
- [ ] E2E CLI tests pass.
- [ ] Lint checks pass.
- [ ] I can explain the repository/package/module distinction.
- [ ] I can explain the Week 1 execution flow from command line to output.
- [ ] I completed reflection and know whether I am genuinely ready for Week 2.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 01 — Python Foundations:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
