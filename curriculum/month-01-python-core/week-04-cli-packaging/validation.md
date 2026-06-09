# Validation - Week 04 CLI and Packaging

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 1](../README.md) › [Week 4 — CLI & Packaging](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

## Exact commands

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

## Strict success criteria
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

## Final oral checkpoint
Before leaving Week 4, say these answers out loud without looking:

1. What turns `researchops` into an installed terminal command?
2. What is the difference between `typer.Argument(...)` and `typer.Option(...)`?
3. Why does `scan` return exit code `0` for an empty directory?
4. Why does an invalid directory return exit code `1`?
5. Why is the CLI handler supposed to stay thin?
6. How does `CliRunner` help you test behavior without typing commands manually?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 1 — Python Core and Project Foundation · **Week 4 — CLI & Packaging** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 5](../../../curriculum/month-02-data-storage-concurrency/week-05-sqlite-storage/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 5 — SQLite Storage](../../../curriculum/month-02-data-storage-concurrency/week-05-sqlite-storage/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 1 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 1 overview](../README.md) · [📄 Week 4 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
