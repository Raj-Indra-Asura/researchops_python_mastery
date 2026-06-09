# Week 04 - CLI and Packaging

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 1](../README.md) › **Week 4 — CLI & Packaging**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Chapter role in Month 1
Weeks 1 through 3 taught you how to set up a project, work with files and errors, and model a real domain.
Week 4 is the moment those pieces become a tool a user can actually run.
This is the chapter where ResearchOps stops feeling like "some Python modules" and starts feeling like software.

You already have scanner logic.
You already have domain ideas.
You already have error-handling habits.
Now you need a real command-line interface, real package metadata, a real installable entry point, and real tests that prove the tool works.

This is how you ship code.

## Story of the week
Imagine a teammate asking a simple question:
"Can I install this and run it from my terminal?"

Before this chapter, the honest answer is "not cleanly yet."
You may have functions.
You may have scripts.
You may even have useful logic.
But users should not need to open Python files and call functions by hand.
They should be able to type a command such as:

```bash
researchops scan ./papers
```

That one line represents several professional skills working together:
- a CLI framework that parses arguments,
- a clean boundary between interface code and application logic,
- packaging metadata that exposes a shell command,
- helpful output formatting,
- meaningful exit codes,
- automated tests that run without a human at the keyboard.

## What this chapter builds
By the end of Week 4, Month 1 culminates in a working, packaged command-line tool with:
- a root `researchops` command,
- a top-level `scan` command,
- grouped sub-apps for future capabilities such as `ingest`, `papers`, and `search`,
- global flags handled at the application level,
- clean success and failure exit codes,
- Rich-formatted output,
- Typer-powered help text,
- packaging through `pyproject.toml`,
- E2E tests using `typer.testing.CliRunner`.

## Core questions this week answers
- What is a CLI, and why do serious tools still use one?
- Why is Typer a strong beginner-friendly choice for Python CLIs?
- What is the difference between a positional argument and an option flag?
- Why should command handlers stay thin?
- How does `researchops` become an installable terminal command?
- Why do exit codes matter to shells, scripts, and CI?
- How do you test a CLI without manually typing commands?

## What you should already know from Weeks 1-3
You are not starting from zero.
You are standing on work you already did.

From Week 1, you bring:
- repository structure,
- project scaffolding,
- the first scanning behavior,
- early tests,
- the idea that ResearchOps is a real application, not a toy script.

From Week 2, you bring:
- `pathlib` thinking,
- file traversal basics,
- exception handling,
- logging awareness,
- user-facing error messages.

From Week 3, you bring:
- domain models,
- richer architecture awareness,
- the difference between data shape and application behavior,
- respect for dependency direction.

Week 4 does not replace that work.
Week 4 connects it.

## The chapter roadmap
### Part 1: The interface layer
You will learn to treat the CLI as a user interface, not as the place where business logic lives.

### Part 2: Typer fundamentals
You will turn ordinary Python functions into commands using decorators, arguments, and options.

### Part 3: Multi-command structure
You will see how a root app can register sub-apps so the CLI can grow without becoming chaotic.

### Part 4: Output and failure behavior
You will format friendly terminal output with Rich and communicate success or failure with exit codes.

### Part 5: Packaging
You will connect `pyproject.toml` to your CLI so `pip install -e .` creates a working `researchops` shell command.

### Part 6: Testing
You will use `CliRunner` to execute commands in-process and assert on output and exit codes.

## Key files for this chapter
### Primary code files
- `src/researchops/cli/main.py`
- `pyproject.toml`
- `tests/e2e/test_cli.py`

### Supporting code you should mentally connect
- `src/researchops/utils/paths.py`
- `src/researchops/config/logging.py`
- `src/researchops/config/settings.py`

### Curriculum files in this folder
- `README.md` — chapter roadmap
- `notes.md` — textbook chapter
- `exercises.md` — workbook
- `break_it.md` — failure lab
- `validation.md` — exact checkpoint commands
- `reflection.md` — Month 1 reflection prompts

## Learning outcomes
If this week goes well, you will be able to:
- explain a CLI as one of several ways users talk to software,
- build a typed command with Typer,
- choose between `typer.Argument` and `typer.Option`,
- use `@app.callback()` for global options like `--verbose`,
- use `app.add_typer()` to organize future command groups,
- print useful terminal output with Rich,
- return exit code `0` on success and non-zero on user-facing failure,
- describe how `[project.scripts]` turns Python code into an installed command,
- test CLI behavior with `CliRunner`,
- keep interface code thin and delegate real work to application logic.

## Why this matters beyond this course
CLI skills transfer everywhere.
You will use the same ideas when you build:
- training scripts for machine learning,
- data pipelines,
- admin tools,
- automation scripts,
- reproducible experiment runners,
- deployment helpers,
- internal developer tooling.

A good CLI is not "just terminal stuff."
It is a disciplined interface contract.

## Definition of done for Week 4
Use this checklist as the chapter finish line.

- [ ] I can explain what `researchops = "researchops.cli.main:app"` means.
- [ ] I can explain why `directory` is a `typer.Argument(...)` and `--recursive` is a `typer.Option(...)`.
- [ ] I understand why `--verbose` belongs in `@app.callback()` instead of inside one command.
- [ ] I understand why `scan()` should call other logic instead of implementing all file traversal itself.
- [ ] I can describe what happens when a path does not exist.
- [ ] I can explain why `raise typer.Exit(1)` matters.
- [ ] I can explain what `CliRunner.invoke()` returns.
- [ ] I can run `researchops --help` and understand the structure of the output.
- [ ] I can run `researchops scan <path>` and interpret the result.
- [ ] I can explain why packaging and testing belong in the same chapter.

## Recommended learning sequence
1. Read `notes.md` carefully from top to bottom.
2. Keep `src/researchops/cli/main.py`, `pyproject.toml`, and `tests/e2e/test_cli.py` open while reading.
3. Work through `exercises.md` in order.
4. Use `break_it.md` to learn how failures actually look.
5. Finish with `validation.md` and run every checkpoint command exactly.
6. Answer the prompts in `reflection.md` as your end-of-Month-1 review.

## End-of-month significance
Month 1 began with project scaffolding.
Month 1 ends with a real installable interface.
That is a major shift.
You are no longer only practicing Python syntax.
You are learning how Python becomes product behavior.

Week 4 is the bridge from "I wrote some code" to "I shipped a usable tool."

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 1 — Python Core and Project Foundation · **Week 4 — CLI & Packaging** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 3 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
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
