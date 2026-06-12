<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 01 — Python Foundations:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 01 Foundations

## Purpose of failure practice

If you only ever see working code, you build a false sense of understanding.
Real skill appears when something breaks and you can answer four questions calmly:

1. What failed?
2. Where did it fail?
3. Why did it fail?
4. What evidence proves the fix is correct?

This lab is designed to make failure normal.
You will break setup, imports, CLI wiring, and utility behavior on purpose.
That practice matters because Week 1 is mostly about project structure.
Structure problems often fail before your “real logic” even runs.

---

## Failure lab rules

1. Break **one thing at a time**.
2. Predict the failure before you run the command.
3. Capture the exact command and exact error message.
4. Do not apply a “mystery fix.”
5. After every fix, run the relevant test.
6. Write down what layer failed: packaging, import, CLI, utility, or test.
7. If you do not know what the traceback means, read it from the bottom upward.
8. Never leave the repository in a broken state when you finish the lab.

---

## Intentional break experiments
Each experiment below is a controlled break. Change one assumption, predict the failure, run the smallest relevant command, inspect the output, restore the code, and identify the test that should catch the problem.

## Experiment 1 — Break the editable install assumption

### How to cause it

1. Create and activate the virtual environment.
2. Do **not** run `python -m pip install -e ".[dev]"`.
3. Immediately run:

```bash
researchops --help
```

### Expected error or symptom

The shell will likely say the command is not found, or Python will fail to resolve the installed entry point.

### How to inspect the failure

- Check whether `.venv` is activated.
- Run `which python` or `python -c "import sys; print(sys.executable)"`.
- Ask: did I install the package, or did I only create the environment?

### How to fix it

Run:

```bash
python -m pip install -e ".[dev]"
```

Then retry:

```bash
researchops --help
```

### Test that should catch it

No Python test catches “you forgot to install the package.”
This is caught by your manual validation commands in `validation.md`.

### What this failure teaches

Creating a virtual environment and installing the package are different steps.
An environment is an isolated Python space.
An editable install registers your project inside that space.

### Common wrong fixes

- Running commands from the system Python and assuming the project is installed there.
- Editing files instead of installing the package properly.
- Recreating the whole repo when only installation was missing.

---

## Experiment 2 — Break the CLI entry point

### How to cause it

Edit `pyproject.toml` so this line is wrong:

```toml
researchops = "researchops.cli.main:app"
```

For example, change `main` to `mainn` or `app` to `application`.

Then reinstall:

```bash
python -m pip install -e ".[dev]"
```

Run:

```bash
researchops --help
```

### Expected error or symptom

The CLI command exists but fails to import the target object, or installation may complain that the entry point cannot be resolved correctly.

### How to inspect the failure

- Compare the string in `[project.scripts]` to the actual file path and object name.
- Read it left to right: `researchops.cli.main:app` means module `researchops.cli.main`, object `app`.
- Open `src/researchops/cli/main.py` and verify the object name.

### How to fix it

Restore the correct entry point string and reinstall editable mode.

### Test that should catch it

Manual command:

```bash
researchops --help
```

Indirectly, `tests/e2e/test_cli.py` protects CLI behavior once imports work.

### What this failure teaches

A package command is wiring.
The CLI command name is not magic.
It is created from metadata.

### Common wrong fixes

- Renaming code to match the mistake instead of fixing the metadata.
- Forgetting to reinstall after changing `pyproject.toml`.
- Blaming Typer when the problem is packaging.

---

## Experiment 3 — Remove `src` from pytest path configuration

### How to cause it

In `pyproject.toml`, temporarily change:

```toml
pythonpath = ["src"]
```

to:

```toml
pythonpath = []
```

Then run:

```bash
pytest -q
```

### Expected error or symptom

Pytest may fail with `ModuleNotFoundError` when tests try to import `researchops`.

### How to inspect the failure

- Read the traceback bottom-up.
- Identify which import failed.
- Ask: does Python know that `src/` is where the package lives during test execution?

### How to fix it

Restore:

```toml
pythonpath = ["src"]
```

Then rerun tests.

### Test that should catch it

Any test importing `researchops`, such as:

- `tests/unit/test_paths.py`
- `tests/e2e/test_cli.py`

### What this failure teaches

The `src/` layout is deliberate.
Tooling must be told where the package code lives.

### Common wrong fixes

- Copying package files into the repo root.
- Modifying imports to odd relative paths.
- Running tests only from a context that hides the real problem.

---

## Experiment 4 — Return `None` instead of `[]`

### How to cause it

Change `find_pdfs()` so that an empty directory returns `None`.
Then run:

```bash
pytest tests/unit/test_paths.py -v
```

### Expected error or symptom

Tests expecting a list will fail.
You may see assertion failures or downstream errors if code tries to iterate over `None`.

### How to inspect the failure

- Find which test failed first.
- Read the assertion and expected type.
- Ask what the function contract promised.

### How to fix it

Return `[]` for “no matching files found.”
That keeps the return type stable: always `list[Path]` on success.

### Test that should catch it

- `test_returns_empty_for_empty_directory`

### What this failure teaches

Stable return types simplify code.
A function that sometimes returns a list and sometimes `None` forces extra defensive logic everywhere.

### Common wrong fixes

- Changing the test to allow `None` just to make it pass.
- Wrapping the caller in `if result is not None` instead of fixing the contract.

---

## Experiment 5 — Stop sorting the results

### How to cause it

Edit `find_pdfs()` and remove `sorted(...)`.
Run:

```bash
pytest tests/unit/test_paths.py -v
```

### Expected error or symptom

The sort-order test should fail, or output ordering may become platform-dependent.

### How to inspect the failure

- Look at the list the test expected.
- Look at the list returned.
- Ask whether filesystem iteration order is guaranteed.

### How to fix it

Restore deterministic ordering with `sorted(...)`.

### Test that should catch it

- `test_returns_sorted_list`

### What this failure teaches

Deterministic behavior is a feature.
It makes tests reliable and CLI output easier to reason about.

### Common wrong fixes

- Deleting the test because “the files are all there anyway.”
- Sorting only in the test instead of the real function.

---

## Experiment 6 — Ignore recursion flag behavior

### How to cause it

Hard-code the pattern to `"*.pdf"` even when `recursive=True`.
Then run:

```bash
pytest tests/unit/test_paths.py -v
pytest tests/e2e/test_cli.py -v
```

### Expected error or symptom

Nested PDFs will not appear in recursive scans.
Tests covering recursion should fail.

### How to inspect the failure

- Compare the command/test input with the returned output.
- Look for the pattern selection line.
- Ask whether the function respected the flag.

### How to fix it

Restore:

```python
pattern = "**/*.pdf" if recursive else "*.pdf"
```

### Test that should catch it

- `test_recursive_finds_nested_pdfs`
- `test_scan_recursive_flag`

### What this failure teaches

Flags are part of the function contract.
A parameter that does nothing is a hidden bug.

### Common wrong fixes

- Changing the tests to stop checking recursive behavior.
- Making the CLI recursive all the time instead of honoring the option cleanly.

---

## Experiment 7 — Pass a file path instead of a directory

### How to cause it

Temporarily delete or bypass the `is_dir()` check in `find_pdfs()`.
Then call the function with a normal file path.

### Expected error or symptom

The function may behave strangely or fail later in a less clear way.
You lose the clean, explicit `NotADirectoryError` contract.

### How to inspect the failure

- Check whether the validation guard still exists.
- Ask whether the function rejects invalid inputs early.
- Compare the current error with the clearer original one.

### How to fix it

Restore the explicit directory validation:

```python
if not directory.is_dir():
    raise NotADirectoryError(...)
```

### Test that should catch it

- `test_raises_for_file_not_directory`

### What this failure teaches

Good functions fail early and clearly.
Input validation is part of usability, not just correctness.

### Common wrong fixes

- Letting a lower-level exception leak with a confusing message.
- Returning `[]` for invalid input and hiding the misuse.

---

## Experiment 8 — Swallow all CLI errors

### How to cause it

In `scan()`, replace the focused `except NotADirectoryError` block with:

```python
except Exception:
    console.print("Something went wrong")
    raise typer.Exit(1)
```

Then trigger an invalid path.

### Expected error or symptom

The user gets a vague message.
You lose the specific reason that would have helped debugging.

### How to inspect the failure

- Compare the original output with the vague replacement.
- Ask what information the user needed.
- Ask which exceptions you actually expected here.

### How to fix it

Handle only the exception you expect in this boundary,
then print the real message.

### Test that should catch it

- `test_scan_nonexistent_directory`

Manual inspection is also important because tests may only check exit code.

### What this failure teaches

Overly broad exception handling hides truth.
Specific failures are easier to debug than generic ones.

### Common wrong fixes

- Catching everything because “users should never see errors.”
- Replacing clear errors with vague friendly text that says nothing useful.

---

## Experiment 9 — Move printing into the utility function

### How to cause it

Edit `find_pdfs()` so that it prints the filenames directly instead of returning them.
Then try to keep the CLI working.

### Expected error or symptom

The CLI becomes harder to control.
Unit tests become awkward because behavior is now tied to console output.

### How to inspect the failure

- Ask what `find_pdfs()` now returns.
- Ask whether the utility or the CLI should own formatting.
- Notice how mixing concerns makes reuse harder.

### How to fix it

Restore the separation:

- utility returns data
- CLI renders data

### Test that should catch it

- `tests/unit/test_paths.py` should start failing if return values change
- `tests/e2e/test_cli.py` may reveal confusing output behavior

### What this failure teaches

Testable code usually separates computation from presentation.
That is also the beginning of clean architecture.

### Common wrong fixes

- Updating tests to assert prints instead of preserving the cleaner design.
- Making utilities depend on Rich or Typer.

---

## Experiment 10 — Break an import path

### How to cause it

Misspell an import in `src/researchops/cli/main.py`, for example:

```python
from researchops.utils.pathz import find_pdfs
```

Then run:

```bash
pytest tests/e2e/test_cli.py -v
```

or:

```bash
researchops --help
```

### Expected error or symptom

Python raises `ModuleNotFoundError` or `ImportError`.
The CLI may fail before command logic even begins.

### How to inspect the failure

- Read the import name carefully.
- Compare it to the real filesystem path.
- Ask whether the missing thing is a file, package, or symbol.

### How to fix it

Restore the correct import path exactly.
Python import names are precise.

### Test that should catch it

- any CLI test importing the app
- manual import smoke test: `python -c "from researchops.cli.main import app"`

### What this failure teaches

Import errors often happen before “real code” runs.
That does not make them trivial.
They are structural failures.

### Common wrong fixes

- Creating duplicate files with typo-matching names.
- Editing `sys.path` manually instead of fixing the import.

---

## Debugging checklist

When something breaks this week, work through this list in order:

1. What exact command did I run?
2. What is the exact error message?
3. Is this failure happening during install, import, command startup, or inside function logic?
4. Did I activate the correct virtual environment?
5. Did I install the package in editable mode?
6. Does `python -c "import researchops"` work?
7. Does `researchops --help` work?
8. Which test fails first?
9. What behavior was that test trying to protect?
10. Did I change a return type, import path, or configuration value?
11. Did I accidentally move logic into the wrong layer?
12. What is the smallest possible fix that restores the original contract?

---

## Reflection after breaking

After completing the failure lab, write short answers to these:

- Which failure felt most confusing at first?
- Which failure turned out to be only a wiring problem?
- Which traceback line mattered most often?
- Which test gave the clearest signal?
- Which wrong fix were you most tempted to try?
- What rule will you follow next time before panicking?
- Can you now distinguish packaging failures from logic failures?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 01 — Python Foundations:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
