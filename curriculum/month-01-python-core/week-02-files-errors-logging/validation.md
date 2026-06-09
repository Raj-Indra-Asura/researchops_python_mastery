
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 2 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 02 — Files, Errors, Logging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation — Chapter 2 Checkpoint

Use this file as a strict pass/fail gate.
Do not mark the chapter complete because the ideas feel familiar.
Mark it complete only when the commands work and you can explain *why* they work.

---

## 1. Environment setup
Run these commands from the repository root.

```bash
python -m pip install -e ".[dev]"
```

Expected result:
- the project installs in editable mode,
- the `researchops` command becomes available,
- and `pytest` is available in the active Python environment.

If installation fails, stop and fix the environment before validating anything else.

---

## 2. Unit tests for path behavior
Run:

```bash
python -m pytest tests/unit/test_paths.py -v
```

Expected result:
- every test in `TestFindPdfs` passes,
- every test in `TestEnsureDir` passes,
- the final summary reports `9 passed`.

What this proves:
- results are sorted,
- non-PDF files are excluded,
- empty directories return `[]`,
- missing paths raise `NotADirectoryError`,
- file paths passed as directories raise `NotADirectoryError`,
- recursive scanning finds nested PDFs,
- non-recursive scanning ignores nested PDFs,
- `ensure_dir()` creates nested directories,
- and `ensure_dir()` is idempotent.

---

## 3. Unit tests for exception behavior
Run:

```bash
python -m pytest tests/unit/test_exceptions.py -v
```

Expected result:
- all hierarchy checks pass,
- all message checks pass,
- all attribute checks pass,
- the final summary reports `21 passed`.

What this proves:
- custom exceptions inherit from the correct base classes,
- exception messages preserve useful context,
- and metadata such as `path`, `paper_id`, `model_name`, and `job_id` is stored correctly.

---

## 4. Combined fast check
Run:

```bash
python -m pytest tests/unit/test_paths.py tests/unit/test_exceptions.py -q
```

Expected result:

```text
tests/unit/test_paths.py .........
tests/unit/test_exceptions.py .....................
30 passed in <time>
```

The exact runtime will vary.
The important part is that all 30 tests pass.

---

## 5. Manual CLI smoke test
Run:

```bash
researchops scan examples/sample_papers
```

Expected result in the repository’s default sample state:
- the command exits cleanly,
- no traceback is shown,
- and the console reports that no PDF files were found in `examples/sample_papers`.

Because this repository ships that folder with a `README.md` but no sample PDFs, the normal expected output is:

```text
No PDF files found in examples/sample_papers
```

If you added PDFs locally, your output will instead show a table of files and a final count.
That is still valid, but you should understand why the output differs.

---

## 6. Verbose logging check
Run:

```bash
researchops --verbose scan examples/sample_papers
```

Expected result in the default sample state:
- the command still exits cleanly,
- the user-facing “no PDFs found” message still appears,
- and a debug log line appears reporting the number of PDFs found.

Observed default output in this repository looked like:

```text
[time] DEBUG    Found 0 PDF(s) in examples/sample_papers
No PDF files found in examples/sample_papers
```

The exact timestamp formatting may vary depending on Rich.
The important validation points are the `DEBUG` level, the `Found 0 PDF(s)` message, and the matching path.

---

## 7. Failure-path smoke test
Run:

```bash
researchops scan examples/does_not_exist
```

Expected result:
- the command exits with status code `1`,
- the user sees a clean error message,
- and the message includes the missing path.

Observed output:

```text
Error: Directory does not exist: examples/does_not_exist
```

This confirms that invalid input is reported clearly instead of producing a raw traceback.

---

## 8. Knowledge checkpoint
You are only done if you can answer **yes** to all of these.

- [ ] I can explain why `Path` is preferred over manual path strings.
- [ ] I can explain the difference between `glob("*.pdf")` and `glob("**/*.pdf")`.
- [ ] I can explain why `find_pdfs()` validates existence before scanning.
- [ ] I can explain why `find_pdfs()` returns a sorted list.
- [ ] I can explain why `ensure_dir()` uses both `parents=True` and `exist_ok=True`.
- [ ] I can explain why `ResearchOpsError` exists even though Python already has `Exception`.
- [ ] I can explain why some exception classes store attributes like `path` and `paper_id`.
- [ ] I can explain what `try`, `except`, `else`, and `finally` each do.
- [ ] I can explain why broad `except Exception` blocks are risky.
- [ ] I can explain why logging is better than `print()` for production software.
- [ ] I can choose a sensible log level for a normal event, a recoverable problem, and a real failure.
- [ ] I can trace how the CLI turns a lower-level exception into a clean command-line message.

---

## 9. Definition of pass
You pass Chapter 2 when:
- installation succeeds,
- all 30 relevant unit tests pass,
- manual scan works on both valid and invalid inputs,
- verbose mode reveals debug information,
- and you can explain the design decisions, not just repeat the commands.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 02 — Files, Errors, Logging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
