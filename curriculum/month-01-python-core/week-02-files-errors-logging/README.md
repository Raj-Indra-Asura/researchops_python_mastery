# Chapter 2: Files, Errors, and Logging

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 1](../README.md) › **Week 2 — Files, Errors, Logging**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## The story of the week
A ResearchOps user drops 50 PDFs into a folder and runs the scanner.
Some files are valid.
Some are nested in subfolders.
Some are not PDFs at all.
One path is misspelled.
One document is empty.
One file may decode strangely.
One run should produce a calm, readable summary instead of a crash.
This chapter teaches you how to make that happen.

## What you already know from Week 1
By the end of Week 1, you can create and activate a virtual environment.
You can install the project in editable mode.
You can read a basic project tree.
You can follow imports through `src/`.
You can run a Typer command from the CLI.
You can write simple functions and basic tests.
You have already met the `scan` command at a very high level.

## What this week adds
This week moves from “the command runs” to “the command behaves well in the real world.”
You will learn how to represent filesystem locations with `pathlib.Path`.
You will learn how to search directories safely.
You will learn how to raise meaningful exceptions instead of vague failures.
You will learn how to catch only the errors you actually understand.
You will learn how to log normal events, recoverable problems, and real failures.
You will learn how tests prove that your scanner handles edge cases.

## Why this matters
Almost every production Python system touches the filesystem.
Research pipelines read raw papers, write outputs, create cache folders, and report failures.
If path handling is sloppy, your tool behaves differently on different machines.
If exceptions are vague, users cannot tell what went wrong.
If logs are noisy or missing, debugging becomes guesswork.
Week 2 is where your project stops feeling like a toy script and starts feeling like an application.

## Learning objectives
By the end of this chapter, you should be able to:

1. Explain why `Path` objects are safer than raw path strings.
2. Use `.exists()`, `.is_dir()`, `.is_file()`, `.glob()`, and `.rglob()` correctly.
3. Predict the difference between `*.pdf` and `**/*.pdf`.
4. Read and write text files with explicit UTF-8 encoding.
5. Design a small custom exception hierarchy around a shared base class.
6. Decide when to raise a built-in exception and when to raise a custom one.
7. Use `try`, `except`, `else`, and `finally` for clear control flow.
8. Re-raise exceptions with more context using `raise ... from ...`.
9. Distinguish between `DEBUG`, `INFO`, `WARNING`, and `ERROR` log messages.
10. Explain why `logging` is more useful than `print()` in application code.
11. Read tests for path and exception behavior and describe what each one proves.
12. Trace how the CLI turns a bad directory into a clean user-facing error message.

## Project milestone
Build a dependable file-discovery layer for ResearchOps.
At the end of the week, your scanner should be able to:

- validate the path it receives,
- find PDF files predictably,
- support optional recursive scanning,
- report empty results cleanly,
- preserve useful failure context,
- and emit logs that help both users and developers.

This is the operational foundation for later ingestion, storage, and search work.

## Files touched in this chapter
- `src/researchops/utils/paths.py` — path validation, directory creation, and safe path resolution.
- `src/researchops/core/exceptions.py` — the shared exception hierarchy for application-level failures.
- `src/researchops/config/logging.py` — startup logging configuration and module logger access.
- `src/researchops/cli/main.py` — the scan command that turns lower-level behavior into user-facing CLI behavior.
- `tests/unit/test_paths.py` — unit tests for sorted results, edge cases, and directory validation.
- `tests/unit/test_exceptions.py` — unit tests for message clarity, hierarchy, and stored metadata.

## Commands introduced or reinforced
```bash
python -m pip install -e ".[dev]"
python -m pytest tests/unit/test_paths.py -v
python -m pytest tests/unit/test_exceptions.py -v
researchops scan examples/sample_papers
researchops scan examples/sample_papers --recursive
researchops --verbose scan examples/sample_papers
```

## Tests involved this week
### Automated tests
- `tests/unit/test_paths.py`
- `tests/unit/test_exceptions.py`

### Manual checks
- Run `researchops scan` on an existing directory.
- Run it on a missing directory.
- Run it with `--recursive`.
- Run it with `--verbose` and read the logs.

## Suggested study plan
### Day 1 — Learn the filesystem model
Read the chapter overview and the `pathlib` sections.
Create small `Path` objects in a Python shell.
Practice `.name`, `.suffix`, `.parent`, and `.exists()`.

### Day 2 — Learn scanning and glob patterns
Trace `find_pdfs()` slowly.
Create tiny practice folders.
Compare `glob("*.pdf")` and `glob("**/*.pdf")`.
Write down what sorted output buys you.

### Day 3 — Learn exceptions
Read `core/exceptions.py` carefully.
Draw the exception hierarchy as a tree.
Practice deciding what information belongs in an exception message.

### Day 4 — Learn error handling flow
Study `try/except/else/finally`.
Trace the `scan` command from input string to CLI exit.
Explain why `NotADirectoryError` is caught at the CLI boundary.

### Day 5 — Learn logging
Read `config/logging.py` and identify root logger configuration, handlers, and levels.
Practice writing `DEBUG`, `INFO`, `WARNING`, and `ERROR` messages for the same scenario.

### Day 6 — Read the tests
Treat the tests as executable specifications.
For each test, answer: what behavior is being protected here?
Then run the tests.

### Day 7 — Consolidate
Do the exercises.
Run the break-it labs.
Complete the reflection prompts.
If you can explain the full scan flow aloud, you are ready for Week 3.

## Estimated time
- Core reading: 3 to 4 hours
- Code tracing: 2 hours
- Exercises: 2 to 3 hours
- Break-it labs: 1 to 2 hours
- Validation and reflection: 1 hour

**Recommended total:** 8 to 12 hours across the week.

## How to know you are stuck
You are probably stuck if:

- you keep treating paths as plain strings and feel confused by `Path` methods,
- you cannot explain the difference between a missing path and a file path,
- you catch `Exception` because you do not know what else to catch,
- you are using `print()` everywhere because logging feels mysterious,
- you cannot tell whether a failure belongs in the service layer or the CLI layer,
- or you can run the code but cannot explain why the tests exist.

When that happens, slow down.
Return to the mental model sections.
Make tiny examples in a Python shell.
Trace one function line by line.
Say out loud what each line assumes and guarantees.

## Definition of done
You are done with Chapter 2 when you can honestly say:

- [ ] I can use `Path` for joins, checks, directory creation, and file discovery.
- [ ] I understand how non-recursive and recursive scanning differ.
- [ ] I can explain why `find_pdfs()` validates the directory before globbing.
- [ ] I can explain why the result list is sorted.
- [ ] I can read and write text with explicit UTF-8 encoding.
- [ ] I can describe the `ResearchOpsError` hierarchy and why it lives in `core/`.
- [ ] I can choose between raising a built-in exception and a custom exception.
- [ ] I can explain each clause in `try/except/else/finally`.
- [ ] I can justify a logging level for a given event.
- [ ] I can explain why `%s` formatting is preferred inside log calls.
- [ ] I can read the path and exception tests and tell what each test protects.
- [ ] I can run the scanner manually and interpret both success and failure output.

## Bridge to next week
Week 3 turns files into objects.
This week teaches you how to find papers safely.
Next week teaches you how to model papers cleanly.
You will move from paths and exceptions into dataclasses, domain models, and richer object design.
A dependable scanner is the foundation.
A dependable model layer is what you build on top of it.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 1 — Python Core and Project Foundation · **Week 2 — Files, Errors, Logging** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 1 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 3](../../../curriculum/month-01-python-core/week-03-oop-domain-modeling/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 3 — OOP & Domain Modeling](../../../curriculum/month-01-python-core/week-03-oop-domain-modeling/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 1 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 1 overview](../README.md) · [📄 Week 2 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
