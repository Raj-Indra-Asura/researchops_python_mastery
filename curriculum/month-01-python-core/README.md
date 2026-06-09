# Month 1 — Python Core and Project Foundation

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../README.md) › [🗺️ Roadmap](../../ROADMAP.md) › **Month 1** (Python Core and Project Foundation)
>
> 📘 This is a **book section overview**. Read it, then start the first week: [Week 1 — Foundations](./week-01-foundations/README.md).
<!-- NAV:TOP:END -->

> **Book section 1 of 5.** This is where ResearchOps comes alive. By the end of
> the month you will have a small but *real* installable Python tool — and, more
> importantly, you will understand every part of it.

---

## The big idea of the month

You already know a little Python *syntax*. This month you learn what a real
Python *project* is: how it is laid out, installed, imported, tested, and run
from a terminal. We turn "scripts in a folder" into "an installable application
with structure, tests, and a command-line interface."

The running theme: **structure is not bureaucracy — it is what lets a project
grow without collapsing.** Everything ML and AI you do later sits on the
foundation you pour this month.

## What you already know before this month

- Basic Python: variables, functions, `if`/`for`/`while`, lists and dicts.
- How to run a single `.py` file.
- Roughly what a library is (you have used `print` and maybe `math`).

That is enough. You do **not** need prior experience with packaging, testing,
classes, or the command line.

## What you will learn this month

- **Repository structure** and the **`src/` layout** — where code lives and why.
- **Virtual environments** — isolated per-project Python installs — and editable
  installs (`pip install -e`).
- **Modules and imports** — how Python files find each other inside a package.
- **CLI basics** with Typer — turning functions into terminal commands.
- **`pathlib`** — the modern, object-oriented way to work with files and paths.
- **Custom exceptions** — defining your own error types for clear failure.
- **Logging** — recording what the program does instead of scattering `print`.
- **Dataclasses** — concise classes for holding structured data.
- **Packaging** with `pyproject.toml` — metadata, dependencies, entry points.
- **Tests** with pytest — proving behavior and catching regressions.
- **Why this foundation matters** before databases and ML ever appear.

## What ResearchOps capability will exist by the end

A working, installable **CLI scanner**:

```bash
researchops scan ./examples/sample_papers
```

It discovers PDF files under a directory and reports them. It is small on
purpose — but it is a *genuine* installed command, backed by tests and a clean
package layout, that you can explain line by line.

## Week-by-week chapter flow

| Week | Chapter | What it adds |
|---|---|---|
| **Week 1 — Foundations** | "The project comes alive" | `src/` layout, virtualenv, editable install, `pathlib` discovery, first Typer command, first pytest test. |
| **Week 2 — Files, Errors, Logging** | "When things go wrong" | Robust file reading, custom exceptions, structured logging instead of `print`. |
| **Week 3 — OOP & Domain Modeling** | "Naming the things" | Dataclasses and domain models (e.g. `Paper`), methods, equality, modeling the problem. |
| **Week 4 — CLI & Packaging** | "Shipping a tool" | Full Typer CLI, `pyproject.toml` entry points, the *composition root*, an installable command. |

## How each week connects to the previous week

- **Week 1 → 2:** the scanner can *find* files; Week 2 teaches it to *read* them
  safely and fail loudly and clearly when it cannot.
- **Week 2 → 3:** once you can read raw data, you need *types* to hold it; Week 3
  introduces domain models like `Paper` to give that data shape and meaning.
- **Week 3 → 4:** with models and logic in place, Week 4 wraps everything in a
  polished CLI and packages it so it installs as a real command.

Each week's output is the next week's input. Nothing is throwaway.

## What not to skip

- **The virtual environment.** Skipping it pollutes your system Python and causes
  mysterious failures all month. Create and activate it every session.
- **The editable install (`pip install -e`).** Without it, imports and the
  `researchops` command will not work as taught.
- **Writing the tests by hand.** Reading about tests is not the same as writing
  them. Type them yourself.
- **`pathlib` over `os.path`.** The whole project uses `pathlib`; learn it now.

## What concepts must be understood before moving on

You should be able to **explain aloud, without notes**:

- Why a `src/` layout exists and what an editable install does.
- How Python resolves an `import researchops...` statement.
- The difference between an exception you raise on purpose and a crash.
- What a dataclass gives you over a plain dict.
- How a Typer command maps a terminal call to a Python function.
- How pytest discovers and runs your tests.

If any of these is fuzzy, review before Month 2 — databases assume all of it.

## Month-end self-assessment

Rate yourself 1–10 on each, and note one piece of evidence:

- [ ] I can create and activate a virtualenv and install the project editable.
- [ ] I can explain the `src/` layout to another beginner.
- [ ] I can write a new Typer subcommand from scratch.
- [ ] I can walk a directory with `pathlib` and filter by suffix.
- [ ] I can define and raise a custom exception.
- [ ] I can configure and use the `logging` module instead of `print`.
- [ ] I can model a small entity with a dataclass.
- [ ] I can add an entry point in `pyproject.toml`.
- [ ] I can write and run a pytest test over a `tmp_path` fixture.

## Month-end mini capstone

Extend the scanner without breaking it:

1. Add a `--ext` option so `researchops scan ./papers --ext pdf` (default) can
   also scan, say, `.txt`.
2. Make it log a one-line summary (count of files found) via the `logging`
   module, not `print`.
3. Raise a clear custom exception with a friendly message when the target
   directory does not exist.
4. Cover all three behaviors with pytest tests, including the error path.

Done when `ruff check src tests`, `pytest -q`, and a manual run all pass.

## Bridge to Month 2

The scanner can *find* files — but ResearchOps **does not remember anything**.
Every run starts from zero. Month 2 fixes that: it adds **persistence**
(SQLite), real **PDF parsing**, an **ingestion pipeline**, **keyword search**,
and **multiprocessing** for speed. In other words, Month 2 turns a one-shot
scanner into a local research *library*.

## Warning signs you are not ready to move on

- You copy commands without knowing what they do.
- The `researchops` command "sometimes works" depending on your terminal (a
  virtualenv/activation gap).
- You cannot explain why imports resolve the way they do.
- Your tests pass but you could not write a new one unaided.
- You still reach for `print` to debug instead of logging or a test.

If two or more apply, repeat the weakest week before continuing.

## Suggested weekly study rhythm

A sustainable ~8–10 hours/week split:

- **Read** the week README + notes (~1 hr) — understand the goal.
- **Build** the milestone in small commits (~4–5 hrs) — the core work.
- **Break it** using the week's `break_it.md` (~1 hr) — learn the failure modes.
- **Test** — write/extend tests until the milestone is proven (~1–2 hrs).
- **Reflect** — fill in `reflection.md` and the weekly report (~30 min).

Never skip the reflection — it is where understanding consolidates.

## Suggested Git milestone at end of month

Tag the foundation so you can always return to a known-good base:

```bash
git add .
git commit -m "Month 1 complete: installable CLI scanner with tests"
git tag month-1-complete
```

Your repository should now: install cleanly, pass `ruff` and `pytest`, and run
`researchops scan ./examples/sample_papers` successfully.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Book section 1 of 5 — **Month 1 — Python Core and Project Foundation**.

### Weeks in this month
- [Week 1 — Foundations](./week-01-foundations/README.md)
- [Week 2 — Files, Errors, Logging](./week-02-files-errors-logging/README.md)
- [Week 3 — OOP & Domain Modeling](./week-03-oop-domain-modeling/README.md)
- [Week 4 — CLI & Packaging](./week-04-cli-packaging/README.md)

### ◀ Previous / Next ▶
- ◀ **Previous:** [◀ Root README (Start Here)](../../README.md)
- ▶ **Next:** [Month 2 overview ▶](../month-02-data-storage-concurrency/README.md)

### Optional paths
- ▶️ **Ready to start?** → [Week 1 — Foundations](./week-01-foundations/README.md)
- 📓 **Finished a week?** → [Write your weekly report](../../docs/weekly-reports/README.md)
- 🗺️ **Want the full map?** → [Roadmap](../../ROADMAP.md) · [Syllabus](../../SYLLABUS.md)

### Global navigation
[🏠 Home](../../README.md) · [🗺️ Roadmap](../../ROADMAP.md) · [📚 Syllabus](../../SYLLABUS.md) · [📓 Weekly reports](../../docs/weekly-reports/README.md)
<!-- NAV:BOTTOM:END -->
