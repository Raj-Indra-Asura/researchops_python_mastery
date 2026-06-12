
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 4 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 04 — CLI and Packaging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 04 CLI and Packaging

## Purpose of this checkpoint
This checkpoint verifies the full Week 4 contract:
- the package installs,
- the entry point resolves,
- the root CLI help is discoverable,
- the `scan` command behaves correctly,
- recursive scanning changes behavior,
- invalid directories exit non-zero,
- CLI tests pass,
- the repository test suite still passes.

Run the commands exactly as written from the repository root.
Do not skip the scratch-data setup block, because the expected results depend on it.

---

## Pre-validation checklist
Before running commands, confirm these are true.

- [ ] You are in the repository root.
- [ ] Your virtual environment is activated.
- [ ] You know that `[project.scripts]` maps `researchops` to `researchops.cli.main:app`.
- [ ] You have read `src/researchops/cli/main.py`.
- [ ] You have read `tests/e2e/test_cli.py`.
- [ ] You understand that `scan` should list PDFs, not parse or store them.

---

## Commands to run

### 1. Activate your environment
```bash
source .venv/bin/activate
```

### 2. Install the package in editable mode with development tools
```bash
python -m pip install -e ".[dev]"
```

### 3. Build a tiny local validation dataset inside the repository
```bash
python - <<'PY'
from pathlib import Path
root = Path('.scratch/week-04-cli/papers')
(root / 'nested').mkdir(parents=True, exist_ok=True)
(root / 'paper_a.pdf').touch()
(root / 'nested' / 'paper_b.pdf').touch()
(root / 'notes.txt').write_text('not a pdf\n')
print(root)
PY
```

Expected final printed line:

```text
.scratch/week-04-cli/papers
```

### 4. Check root help
```bash
researchops --help
```

You should see all of these substrings in the output:
- `ResearchOps — research paper processing and experiment-tracking platform.`
- `scan`
- `ingest`
- `papers`
- `search`
- `--verbose`

### 5. Check command-specific help
```bash
researchops scan --help
```

You should see all of these substrings in the output:
- `Usage: researchops scan [OPTIONS] DIRECTORY`
- `Scan a directory and list discovered PDF files.`
- `Path to a directory containing PDF files.`
- `--recursive`

### 6. Run a non-recursive scan
```bash
researchops scan .scratch/week-04-cli/papers
```

You should observe:
- exit code `0`,
- output contains `paper_a.pdf`,
- output does **not** contain `paper_b.pdf`,
- output does **not** contain `notes.txt`,
- output contains `1 PDF(s) found`.

### 7. Run a recursive scan
```bash
researchops scan .scratch/week-04-cli/papers --recursive
```

You should observe:
- exit code `0`,
- output contains `paper_a.pdf`,
- output contains `paper_b.pdf`,
- output does **not** contain `notes.txt`,
- output contains `2 PDF(s) found`.

### 8. Run a failing scan against a missing directory
```bash
researchops scan .scratch/week-04-cli/missing
```

You should observe:
- output contains `Error:`,
- output contains `Directory does not exist`,
- command exits with code `1`.

### 9. Prove the failing command returned `1`
```bash
researchops scan .scratch/week-04-cli/missing ; echo $?
```

Expected final printed line:

```text
1
```

### 10. Run the CLI test file
```bash
pytest tests/e2e/test_cli.py -v
```

Expected result:
- `7` tests collected,
- all `7` passed,
- no failures,
- no errors.

### 11. Run the full test suite
```bash
pytest -q
```

Expected result:
- test run completes successfully,
- final summary shows all tests passed.

---

## Expected outputs
The exact Rich table spacing may vary, but these observable results must hold.

- Dataset setup prints `.scratch/week-04-cli/papers`.
- `researchops --help` includes `scan`, `ingest`, `papers`, `search`, and `--verbose`.
- `researchops scan --help` shows the required `DIRECTORY` argument and `--recursive` option.
- Non-recursive scan contains `paper_a.pdf`, excludes `paper_b.pdf`, excludes `notes.txt`, and reports `1 PDF(s) found`.
- Recursive scan contains both PDF names, excludes `notes.txt`, and reports `2 PDF(s) found`.
- Missing-directory scan prints `Error:` and `Directory does not exist`, then exits with code `1`.
- `pytest tests/e2e/test_cli.py -v` reports `7` tests passed.
- `pytest -q` reports the full suite passing.

## Tests that must pass
You are only done if all of the following are true.

- [ ] `python -m pip install -e ".[dev]"` succeeds.
- [ ] `researchops --help` works from the installed shell command.
- [ ] Root help lists `scan`, `ingest`, `papers`, and `search`.
- [ ] `researchops scan --help` shows a required `DIRECTORY` argument.
- [ ] Non-recursive scan shows only the top-level PDF.
- [ ] Recursive scan includes the nested PDF.
- [ ] Non-PDF files are not shown.
- [ ] Missing-directory scan prints a human-readable error.
- [ ] Missing-directory scan exits with code `1`.
- [ ] `tests/e2e/test_cli.py` passes.
- [ ] `pytest -q` passes.
- [ ] You can explain why the shell command exists only after packaging metadata points at `researchops.cli.main:app`.

---

## Manual checks
- [ ] Run `researchops --help` yourself and confirm the command names are discoverable.
- [ ] Run the non-recursive and recursive scans against the scratch dataset and compare the filenames.
- [ ] Run the missing-directory command and confirm the final `echo $?` output is `1`.

## Architecture checks
- [ ] `scan()` delegates PDF discovery to `find_pdfs()` instead of walking the filesystem inline.
- [ ] CLI code formats user output and exit codes; helper logic remains outside the command handler.
- [ ] Grouped Typer apps are attached with `app.add_typer()` rather than duplicated at the root.
- [ ] Tests import the actual `app` object from `researchops.cli.main`.

## Documentation checks
- [ ] Week 4 notes explain the entry point string and command flow.
- [ ] Exercises include code-reading, implementation, testing, debugging, stretch, brutal, mini-project, and completion-checklist work.
- [ ] Validation commands match the current `researchops` CLI behavior.

## Do-not-proceed warnings
Do not leave Month 1 if any of these are true.

- The installed `researchops` command is missing.
- `researchops --help` does not list `scan`.
- `researchops scan --help` does not show a required directory argument.
- A missing directory prints an error but exits `0`.
- Recursive and non-recursive scan output are identical for nested PDFs.
- You cannot explain how `[project.scripts]` creates the command.

---

## If something fails, diagnose by category
Use this table before randomly changing code.

| Symptom | Likely category | First thing to check |
|---|---|---|
| `researchops` command is missing | install problem | Did editable install succeed? |
| `researchops` exists but crashes on startup | entry point problem | Is `[project.scripts]` correct? |
| `--recursive` is rejected | parser/signature problem | Is the option declared in the command signature? |
| Error message prints but exit code is `0` | exit-code problem | Are you raising `typer.Exit(1)`? |
| Tests import but commands are missing | wrong app under test | Does the test import `app` from `researchops.cli.main`? |
| Output format differs slightly | brittle assertion problem | Are you asserting stable substrings instead of exact spacing? |

---

## Ruthless mentor checkpoint
Before leaving Week 4, say these answers out loud without looking:

1. What turns `researchops` into an installed terminal command?
2. What is the difference between `typer.Argument(...)` and `typer.Option(...)`?
3. Why does `scan` return exit code `0` for an empty directory?
4. Why does an invalid directory return exit code `1`?
5. Why is the CLI handler supposed to stay thin?
6. How does `CliRunner` help you test behavior without typing commands manually?
---

## Definition of done
- [ ] Editable installation succeeds.
- [ ] Root help and scan help are correct.
- [ ] Non-recursive scan, recursive scan, and missing-directory scan match the expected outputs.
- [ ] `tests/e2e/test_cli.py` passes.
- [ ] The full test suite passes.
- [ ] You can explain entry points, Typer arguments/options, exit codes, and thin CLI handlers aloud.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 04 — CLI and Packaging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
