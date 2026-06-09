<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 04 — CLI and Packaging:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

---
<!-- NAV_END -->

# Notes - Week 04 CLI and Packaging

<!-- LEARNING_FORMAT_START -->
# Complete Learning Format — Week 04: CLI and Packaging

This guide is the clean learning path for the chapter.
It uses short sentences.
It breaks ideas into small pieces.
It tells you what to focus on and what to ignore for now.
Read it before the older detailed notes that follow.

## Chapter overview

The chapter title is **Software that users can install and run**.
The practical milestone is: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
The expected capability is: Can install a Python package with an entry point, write CLI tests with CliRunner, and explain how `pyproject.toml` wires a command to a function.
This chapter is one step in the ResearchOps system, not a random lesson.
The visible feature matters because it proves the idea works.
The hidden skill matters because it lets you build the next chapter without confusion.
A complete pass through this chapter means you can read the code, run it, test it, break it, and explain it aloud.

Use this study order:
- Read the story first without typing.
- Trace the smallest code example.
- Find the project file that owns the behavior.
- Run the validation command.
- Explain one happy path and one failure path.

## What you already know from previous weeks

- Week 1 taught Python Foundations and Repository Setup; keep its responsibility in mind, but do not rebuild it here.
- Week 2 taught Files, Paths, Exceptions, and Logging; keep its responsibility in mind, but do not rebuild it here.
- Week 3 taught OOP, Dataclasses, and Domain Modeling; keep its responsibility in mind, but do not rebuild it here.
- You should be able to run the previous validation command before trusting new work.
- You should be able to point at the main file from the previous week and say what job it owns.
- If a previous idea feels weak, reread the example and trace one concrete value through it.
- The safest learning rhythm is: understand one thing, change one thing, test one thing, explain one thing.

## What problem this week solves

Week 4 solves the project problem behind **CLI and Packaging**.
Before this chapter, ResearchOps has a gap.
The gap may be a missing feature, a missing boundary, a missing safety check, or a missing way to communicate with users.
This chapter closes that gap with a focused milestone.
Do not treat the milestone as a checklist only.
Treat it as proof that the idea belongs in the system.
- The concept ``[project.scripts]` entry points in `pyproject.toml`` helps solve part of this gap.
- The concept `Typer sub-apps and command groups` helps solve part of this gap.
- The concept ``typer.testing.CliRunner` for CLI tests` helps solve part of this gap.
- The concept `Optional dependency groups `[project.optional-dependencies]`` helps solve part of this gap.
- The concept `Editable installs and import paths` helps solve part of this gap.
- The concept `Shell completion` helps solve part of this gap.

## Beginner mental model

Use a simple four-part model: input, owner, transformation, proof.
Input means the concrete thing entering the system.
Owner means the file, object, or function responsible for the decision.
Transformation means the useful change from raw data to meaningful result.
Proof means the test or command that confirms the result.
- Ask: what is the input for **CLI and Packaging**?
- Ask: what is the owner for **CLI and Packaging**?
- Ask: what is the transformation for **CLI and Packaging**?
- Ask: what is the proof for **CLI and Packaging**?
If you cannot answer those four questions, do not add more code yet.

## Core vocabulary

| Term | Simple meaning | Why it matters here |
|------|----------------|---------------------|
| [project.scripts]` entry points in `pyproject.toml | `[project.scripts]` entry points in `pyproject.toml` | This term names one job in the Week 4 milestone. |
| Typer sub-apps and command groups | Typer sub-apps and command groups | This term names one job in the Week 4 milestone. |
| typer.testing.CliRunner` for CLI tests | `typer.testing.CliRunner` for CLI tests | This term names one job in the Week 4 milestone. |
| Optional dependency groups `[project.optional-dependencies] | Optional dependency groups `[project.optional-dependencies]` | This term names one job in the Week 4 milestone. |
| Editable installs and import paths | Editable installs and import paths | This term names one job in the Week 4 milestone. |
| Shell completion | Shell completion | This term names one job in the Week 4 milestone. |
| Boundary | A line between responsibilities | It keeps the chapter understandable for a beginner. |
| Failure path | What happens when the happy path is not available | It keeps the chapter understandable for a beginner. |
| Validation | Evidence that the system still works | It keeps the chapter understandable for a beginner. |
| Responsibility | The one job a file or function owns | It keeps the chapter understandable for a beginner. |

## Concept explanations from first principles

Read each concept as if you have never heard the term before.
Do not skip the plain meaning.
### Concept 1: `[project.scripts]` entry points in `pyproject.toml`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 4, it supports the milestone: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 2: Typer sub-apps and command groups
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 4, it supports the milestone: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 3: `typer.testing.CliRunner` for CLI tests
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 4, it supports the milestone: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 4: Optional dependency groups `[project.optional-dependencies]`
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 4, it supports the milestone: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 5: Editable installs and import paths
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 4, it supports the milestone: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

### Concept 6: Shell completion
- **Plain meaning:** This is a named tool for solving one part of the chapter problem.
- **Why it exists:** Real projects become confusing when this concern is unnamed.
- **ResearchOps use:** In Week 4, it supports the milestone: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
- **Input question:** What data, command, file, request, or state reaches this concept?
- **Output question:** What value, saved record, response, log, or state change should come out?
- **Failure question:** What can be missing, malformed, slow, duplicated, stale, or invalid?
- **Test question:** Which test would catch the mistake before a user sees it?
- **Beginner trap:** Memorizing the word without tracing it in the project.
- **Recovery move:** Use one concrete example and follow it through the files.
- **Mastery signal:** You can explain the concept without saying "magic" or "it just works".

## ResearchOps-specific application

The chapter belongs to these project locations:
- `src/researchops/cli/main.py` — sub-app registration
- `src/researchops/cli/commands/papers.py` — `papers` command group
- `src/researchops/cli/commands/search.py` — `search` command group
- `pyproject.toml` — script entry, optional dep groups
Study those files in this order:
1. Find the user-facing entry point.
2. Find the service or core concept that owns the meaning.
3. Find the infrastructure only when outside resources are needed.
4. Find the tests that prove the behavior.
5. Find the validation command that a learner runs manually.
The goal is to know why each file exists.
If two files seem to own the same decision, stop and clarify the boundary.

## Code examples with line-by-line explanation

```python
import typer

app = typer.Typer()

@app.command()
def scan(path: str) -> None:
    typer.echo(f"Scanning {path}")
```

Line-by-line explanation:
- Line 1: `import typer` — This imports a tool before the example can use it.
- Line 2: `(blank line)` — This blank line separates ideas so the example is easier to read.
- Line 3: `app = typer.Typer()` — This stores a clear intermediate value for the next step.
- Line 4: `(blank line)` — This blank line separates ideas so the example is easier to read.
- Line 5: `@app.command()` — This attaches framework or test behavior to the next function or class.
- Line 6: `def scan(path: str) -> None:` — This names a reusable action and shows what information it receives.
- Line 7: `typer.echo(f"Scanning {path}")` — This performs one small visible step in the workflow.

How to use this example:
- Name the input.
- Name the output.
- Predict the result before running anything.
- Connect the shape to the real ResearchOps file.
- Write one sentence about why each line belongs.

## Common beginner mistakes

- **Mistake:** Pasting code before knowing the owner of the behavior.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Changing many files at once.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Skipping the failure path.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Reading only the happy path test.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Ignoring the validation command.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Using vague names.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Putting business rules in the user interface layer.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Treating logs, errors, and tests as decoration.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Optimizing before correctness is visible.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.
- **Mistake:** Building future-week features early.
  **Why it hurts:** it hides the mental model and makes debugging harder.
  **Better move:** make one small behavior clear, then prove it.

## Debugging guidance

- Copy the exact failing command.
- Read the first useful error line.
- Read the final error line.
- Classify the failure as import, input, state, file, database, network, model, or expectation.
- Reproduce it with the smallest command.
- Inspect the value closest to the failure.
- Fix the cause, not only the symptom.
- Run the narrowest test.
- Run the chapter validation command.
- Write down what the error was teaching.
Debugging questions:
- What did I expect?
- What happened?
- Which value first became wrong?
- Which layer created that value?
- Which test should catch this next time?

## Design tradeoffs

- **Simple first version:** Easy to understand, but not the final production shape.
- **Clear layers:** More files, but less confusion as features grow.
- **Explicit errors:** More code, but failures become teachable.
- **Small unit tests:** Fast feedback, but less end-to-end confidence.
- **Integration tests:** Real wiring, but slower and more setup.
- **Configuration:** Flexible behavior, but defaults must be clear.
The right question is not "What is the fanciest design?"
The right question is "What design teaches the responsibility clearly and can grow next week?"

## Testing implications

Tests for this chapter:
- `tests/e2e/test_cli.py` — expanded with CliRunner tests for each command group
Validation commands:
```bash
researchops --help
researchops papers --help
researchops search --help
pytest tests/e2e/ -v
```
- Arrange the data.
- Act on the system.
- Assert the visible promise.
- Check one failure path.
- Keep unit tests fast.
- Use integration tests only when real wiring matters.

## Architecture implications

ResearchOps stays understandable when dependencies point inward.
```text
CLI / API / Worker -> Services -> Core
Infrastructure implements core-facing contracts and is wired at the outside.
```
- Does the UI layer avoid business logic?
- Does the service layer own workflow decisions?
- Does core avoid infrastructure imports?
- Does infrastructure do outside-world work?
- Do tests use fakes when possible?
Architecture is not ceremony.
Architecture is named responsibility.

## How this connects to AI engineering / ML research

AI engineering needs more than models.
It needs reliable data flow, clear interfaces, repeatable experiments, visible failures, and honest evaluation.
Week 4 contributes by making **cli and packaging** clear enough to trust.
- Bad data creates bad model behavior.
- Unclear boundaries make experiments hard to reproduce.
- Missing tests let regressions change research results silently.
- Good logs and errors shorten investigation time.
- Clear documentation lets future users understand the system.

## Mini quizzes

- What problem does Week 4 solve?
- What is the main input?
- What is the main output?
- Which file owns the main responsibility?
- Which layer should not contain business logic?
- What is one happy path?
- What is one failure path?
- What command proves the chapter works?
- What should you not build early?
- How does this prepare the next week?

## Explain-it-aloud prompts

- Explain CLI and Packaging in simple words.
- Explain the data flow from input to result.
- Explain the first file you would open.
- Explain the test that gives confidence.
- Explain what can break.
- Explain the tradeoff made in this chapter.
- Explain what you still find weak.

## What to memorize

- The topic: CLI and Packaging.
- The milestone: `pip install -e .` produces a working `researchops` command with sub-command groups: `scan`, `papers`, `search`. CLI tests use `CliRunner`.
- The main project files.
- The validation command.
- The boundary rule for the layer you are touching.
- The habit of testing before moving forward.

## What to understand deeply

- Why this feature belongs now.
- How data moves through the chapter.
- Which file owns which decision.
- How the failure path is handled.
- Why the tests prove behavior.
- How this week makes future work safer.

## What not to worry about yet

- Perfect scale.
- Fancy abstractions.
- Future-week features.
- Every option in every library.
- Premature optimization.
- Comparing your speed to someone else.
Focus on the milestone.
A clear small milestone beats a confusing large one.

## Bridge to next week

Next week is Week 5: **SQLite Storage Layer**.
This week prepares you by giving ResearchOps a clearer piece of behavior before the next milestone: `researchops papers list` shows papers stored in SQLite. `PaperRepository` protocol implemented by `SqlitePaperRepository`.
- Run validation.
- Explain the main files.
- Explain one failure.
- Explain one test.
- Write down what still feels weak before moving on.

## Guided deepening drills

Use these drills if the chapter still feels abstract.
- Drill 1: Trace ``[project.scripts]` entry points in `pyproject.toml`` from user input to project result.
- Drill 2: Write one sentence defining ``[project.scripts]` entry points in `pyproject.toml`` without copying the notes.
- Drill 3: Find the file where ``[project.scripts]` entry points in `pyproject.toml`` appears or should appear.
- Drill 4: Name one wrong implementation of ``[project.scripts]` entry points in `pyproject.toml`` and why it would hurt.
- Drill 5: Name one test that would protect ``[project.scripts]` entry points in `pyproject.toml``.
- Drill 6: Trace `Typer sub-apps and command groups` from user input to project result.
- Drill 7: Write one sentence defining `Typer sub-apps and command groups` without copying the notes.
- Drill 8: Find the file where `Typer sub-apps and command groups` appears or should appear.
- Drill 9: Name one wrong implementation of `Typer sub-apps and command groups` and why it would hurt.
- Drill 10: Name one test that would protect `Typer sub-apps and command groups`.
- Drill 11: Trace ``typer.testing.CliRunner` for CLI tests` from user input to project result.
- Drill 12: Write one sentence defining ``typer.testing.CliRunner` for CLI tests` without copying the notes.
- Drill 13: Find the file where ``typer.testing.CliRunner` for CLI tests` appears or should appear.
- Drill 14: Name one wrong implementation of ``typer.testing.CliRunner` for CLI tests` and why it would hurt.
- Drill 15: Name one test that would protect ``typer.testing.CliRunner` for CLI tests`.
- Drill 16: Trace `Optional dependency groups `[project.optional-dependencies]`` from user input to project result.
- Drill 17: Write one sentence defining `Optional dependency groups `[project.optional-dependencies]`` without copying the notes.
- Drill 18: Find the file where `Optional dependency groups `[project.optional-dependencies]`` appears or should appear.
- Drill 19: Name one wrong implementation of `Optional dependency groups `[project.optional-dependencies]`` and why it would hurt.
- Drill 20: Name one test that would protect `Optional dependency groups `[project.optional-dependencies]``.
- Drill 21: Trace `Editable installs and import paths` from user input to project result.
- Drill 22: Write one sentence defining `Editable installs and import paths` without copying the notes.
- Drill 23: Find the file where `Editable installs and import paths` appears or should appear.
- Drill 24: Name one wrong implementation of `Editable installs and import paths` and why it would hurt.
- Drill 25: Name one test that would protect `Editable installs and import paths`.
- Drill 26: Trace `Shell completion` from user input to project result.
- Drill 27: Write one sentence defining `Shell completion` without copying the notes.
- Drill 28: Find the file where `Shell completion` appears or should appear.
- Drill 29: Name one wrong implementation of `Shell completion` and why it would hurt.
- Drill 30: Name one test that would protect `Shell completion`.

<!-- LEARNING_FORMAT_END -->

---

# Existing detailed notes
## Chapter overview
Week 4 is the Month 1 culmination.
You are no longer only writing Python code that works inside files.
You are learning how to expose that code as a usable tool.
The keyword for this week is interface.
A command-line interface is one of the oldest and most powerful software interfaces.
It is still everywhere because it is scriptable, testable, automatable, and precise.
ResearchOps now has enough internal pieces that it deserves a real command.
This chapter explains how that command is built, packaged, and tested.

By the end of this chapter, you should understand that `researchops scan ./papers` is not magic.
It is a chain of small decisions.
Those decisions live in code structure, decorators, output formatting, packaging metadata, and tests.
If you understand the chain, you can build more commands with confidence.

## What you already know from Weeks 1 to 3
You already know how to work inside a repository.
You already know how to read and write Python modules.
You already know how to think about paths and files with `pathlib`.
You already know that user-facing errors should be clear.
You already know that logging can help you understand program behavior.
You already know that domain models matter because shape and meaning matter.
You already know that architecture boundaries protect future growth.

Week 4 uses all of that.
The CLI needs path handling.
The CLI needs clear errors.
The CLI needs a place to send logging configuration.
The CLI needs to respect the architecture.
The CLI needs to call real logic rather than duplicate it.

So the big idea is not that Week 4 abandons earlier weeks.
The big idea is that Week 4 integrates earlier weeks.
Month 1 began with scaffold and structure.
Month 1 ends with a runnable, installable command.
That is why this chapter feels more product-like than the earlier ones.

## What problem this week solves
Imagine that your codebase contains useful functions but no proper CLI.
A teammate asks how to scan a directory of papers.
You say something awkward like this:

```bash
python -c 'from researchops.utils.paths import find_pdfs; ...'
```

That answer technically works.
It is also a sign that the user interface is unfinished.
Users should not need to know internal module paths to use core functionality.
Users should not need to open Python files and call functions manually.
Users should not need to guess how errors are communicated.
Users should not need to inspect source code just to discover available commands.

A proper CLI solves those problems.
A proper CLI gives the project a public face.
A proper CLI makes behavior discoverable through help text.
A proper CLI creates a stable contract between the user and the application.
A proper CLI makes automation possible because the command has clear inputs, outputs, and exit codes.
A proper CLI is how utility code becomes a usable tool.

## Beginner mental model
Think of the CLI as the front desk of the application.
The front desk greets the user.
The front desk asks for the necessary information.
The front desk sends the request to the right internal team.
The front desk returns a clean answer.
The front desk does not secretly do all the hospital surgery in the lobby.

That is the thin-command-handler pattern.
A command handler should do three things well.
First, it should gather inputs.
Second, it should call application logic.
Third, it should format output.
That is enough.

A command handler should not become a giant pile of business rules.
It should not become the only place where scanning logic exists.
It should not become a private world of duplicate logic that the rest of the application cannot reuse.
If the CLI owns too much logic, then future APIs, workers, or background jobs cannot reuse that behavior cleanly.
That would violate the architecture goals of ResearchOps.

So when you see a handler like `scan()`, you should think this way:
- read the user input,
- translate it into the shapes the application expects,
- call a helper or service,
- present the result.

That mental model will matter even more in future chapters.
Today the helper is `find_pdfs()`.
Later the helper may be a service object, repository-backed use case, or ML pipeline.
The CLI remains the interface layer.

## Core vocabulary
### CLI
CLI means command-line interface.
It is a text-based way to talk to a program.
A user types commands in a terminal.
The program parses the text.
The program runs behavior.
The program prints text back.

### Typer
Typer is a Python library for building CLIs.
It uses normal Python functions, decorators, and type hints.
That means the code often looks close to ordinary Python.
This is one reason it feels beginner-friendly.

### `typer.Argument`
`typer.Argument` declares a positional command-line input.
It usually represents something required.
Users provide it by position rather than by flag name.
In this chapter, the directory path is an argument.

### `typer.Option`
`typer.Option` declares a flag-based input.
It usually represents something optional, configurable, or toggle-like.
Users provide it with names such as `--recursive` or `-r`.
In this chapter, the recursive flag is an option.

### `app.callback()`
`app.callback()` defines logic that runs before commands.
It is a good place for global options.
It is also a good place for application-wide setup.
In ResearchOps, `--verbose` belongs here because logging level affects the whole application, not just one command.

### `@app.command()`
`@app.command()` registers a function as a command.
Typer reads the decorated function and turns it into part of the CLI.
The function name usually becomes the command name unless configured otherwise.
A decorated `scan()` function becomes the `scan` command.

### `app.add_typer()`
`app.add_typer()` attaches a Typer sub-application to another Typer app.
This is how you build command groups.
It supports structures like `researchops ingest ...` and `researchops papers ...`.
It helps large CLIs stay organized.

### Exit code
An exit code is the numeric status a process returns when it finishes.
The shell reads it.
Automation reads it.
CI reads it.
By convention, `0` means success.
Any non-zero value signals some kind of failure or abnormal outcome.

### `CliRunner`
`CliRunner` is a test helper from `typer.testing`.
It runs a Typer application in-process.
It captures output.
It returns a result object.
That result object includes `result.output` and `result.exit_code`.

### Entry point
An entry point is the mapping between an installed shell command and a Python import target.
In this project, the shell command `researchops` maps to the Python object `app` inside `researchops.cli.main`.
That mapping lives in `pyproject.toml`.

### `rich.console.Console`
`Console` is Rich's object for printing styled terminal output.
It supports colors, markup, tables, and more readable output.
It replaces many plain `print()` use cases in CLI applications.

### Rich markup
Rich markup is the bracket-based styling syntax used inside output strings.
Examples include `[red]`, `[yellow]`, and `[bold]`.
It lets terminal text communicate importance visually.

### TOML
TOML is the configuration file format used by `pyproject.toml`.
It is structured, readable, and common in modern Python packaging.
The name expands to Tom's Obvious, Minimal Language.
You do not need to memorize the name expansion.
You do need to recognize TOML as structured project configuration.

### Optional dependency group
An optional dependency group is a named bundle of dependencies that users can install when needed.
Examples here include `dev`, `storage`, `parsing`, `ml`, and `api`.
This lets the project stay modular.
Not every user needs every capability at install time.

## First principles
### What is a CLI
A CLI is not just a way to avoid GUIs.
A CLI is a contract built from commands, arguments, options, text output, and exit codes.
It is often the fastest way to interact with developer tools.
It is also easy to automate in scripts and CI jobs.
A CLI is especially strong when the user already knows the action they want.
Typing a command can be faster than clicking through several screens.

A CLI is one of three common ways to talk to a program.
The first is a GUI.
The second is an API.
The third is a CLI.
Understanding the differences matters.

A GUI is visual.
It uses windows, buttons, forms, and layouts.
It is often best for discoverability and broad audiences.
A web app dashboard is a GUI.
A desktop application is a GUI.

An API is program-to-program communication.
One piece of software sends structured requests to another.
The other replies with structured data.
HTTP APIs are a common example.
An API is not primarily designed for humans typing in terminals.
It is designed for systems integrating with systems.

A CLI is a human-facing interface that is also automation-friendly.
That dual nature is what makes it so useful.
A person can run it interactively.
A shell script can run it automatically.
A CI pipeline can run it repeatedly.
A scheduled job can run it without a screen.

For ResearchOps, a CLI is a natural early interface.
It is simpler than building a GUI.
It is easier to validate than a full API surface.
It is excellent for developer workflows.
It fits the project's early stage.

### What is Typer
Typer is a library that helps Python functions become command-line commands.
It is built on ideas from Click.
Its main beginner-friendly feature is that it uses Python type hints and function signatures directly.
That means the code feels closer to normal Python than some older CLI styles.

If you can understand a function like this:

```python
def scan(directory: str, recursive: bool = False) -> None:
    ...
```

Then you are already close to understanding a Typer command.
Typer adds decorators and argument or option declarations around that function.
From there, it generates parsing behavior, help output, and invocation rules.

Typer rewards good naming and good typing.
A parameter name becomes part of the interface.
A type hint informs parsing and help.
A docstring informs command descriptions.
So a Typer CLI is not separate from Python style.
It is built on Python style.

### `typer.Argument` versus `typer.Option`
This is one of the most important distinctions in the week.
Arguments are positional.
Options are named flags.

A positional argument is something the user must place in the right slot.
Example:

```bash
researchops scan ./papers
```

Here `./papers` is positional.
The command expects it after `scan`.
That makes sense because the directory is the core thing being acted on.
Without a target directory, `scan` does not know what to scan.

An option is named.
Example:

```bash
researchops scan ./papers --recursive
```

Here `--recursive` is a toggle-like flag.
The command still makes sense without it.
The flag modifies behavior.
That is why it belongs as an option instead of an argument.

A helpful rule is this:
Use an argument for the main thing the command acts on.
Use an option for extra control over how the command behaves.

### `@app.command()`
Decorators are functions that modify other functions.
When you place `@app.command()` above a function, Typer registers that function as a command.
This does not mean the function runs immediately.
It means Typer stores information about that function for later CLI use.

When the user types `researchops scan ...`, Typer looks up the registered command named `scan`.
Then Typer parses the command-line pieces according to the function signature.
Then Typer calls the function with real Python values.
That is the core mapping.
Text from the terminal becomes typed Python function inputs.

### `@app.callback()`
A callback belongs to the app rather than one specific command.
It runs before command execution.
This makes it a natural home for global options and setup behavior.

Why does `--verbose` belong here.
Because logging level affects the whole application.
It is not only about scanning.
If future commands such as `ingest` or `search` also need verbose logging, they should not each define their own separate copy of `--verbose`.
The callback centralizes that concern.

So `@app.callback()` helps you answer this question:
What should happen for the whole app before a specific command runs.
In ResearchOps, the answer is logging configuration.

## More first principles
### `app.add_typer()`
As a CLI grows, one flat list of commands becomes harder to navigate.
You do not want fifty unrelated commands all living at the root.
Grouping commands makes the interface easier to learn.
Grouping also keeps the code easier to organize.

`app.add_typer()` is how Typer supports grouped structure.
You create another Typer app.
That sub-app owns its own commands.
Then you attach it to the root app with a name.
The result is a multi-level CLI.

ResearchOps uses this idea already.
The root app adds grouped apps named `ingest`, `papers`, and `search`.
That means the root command becomes a hub.
Future features can grow under logical families.
This is better than dumping every command at the top level.

### Exit codes from first principles
A terminal command is a process.
When it ends, it returns a number.
That number is the exit code.
This may feel small.
It is actually one of the most important parts of CLI design.

Humans read text.
Scripts read status codes.
A shell script may never inspect the full printed output.
It may simply ask whether the previous command returned success.
CI works the same way.
A failing exit code can stop a pipeline.
A successful exit code can let the next step proceed.

By convention:
- `0` means success.
- non-zero means failure or abnormal termination.

That does not mean every non-zero code must be unique in a small project.
It does mean you should never accidentally return `0` for a real failure.
That is how automation gets lied to.

### `raise typer.Exit(code=...)`
Typer gives you a clean way to end command execution with a chosen exit code.
That mechanism is `raise typer.Exit(code=...)`.
The important word here is raise.
You are not just returning from a function.
You are telling the CLI framework to stop processing and finish with a specific status.

This is why code like this matters:

```python
raise typer.Exit(1)
```

If you only print an error and then `return`, the process may still end with `0`.
That would tell the shell that everything was fine.
So the print message and the exit code serve different audiences.
The message serves the human.
The exit code serves the machine.

### Rich Console
Rich is a library for nicer terminal output.
Its `Console` object is the main tool for printing styled content.
If plain `print()` is a ballpoint pen, `Console` is a full set of formatting tools.
It can still print simple text.
It can also print tables, colors, emphasis, status messages, panels, and more.

For a beginner, the most important idea is not every Rich feature.
The most important idea is that output design matters.
A CLI with clean output is easier to trust.
A CLI with readable sections and clear highlighting is easier to debug.
A CLI with visual emphasis can communicate success, warning, and error states quickly.

### Rich markup
Rich markup uses bracket tags inside strings.
Examples:
- `[red]Error[/red]`
- `[yellow]Warning[/yellow]`
- `[bold]Done[/bold]`

The tags are interpreted by Rich when printed through `console.print()`.
If you use invalid tags, the styling may fail or behave unexpectedly.
So markup is useful, but it is still part of the interface contract.
You should treat it carefully.

### Rich Table
A table is useful when output has repeated structure.
ResearchOps uses a Rich table to show discovered PDFs.
Each row represents one file.
Each column represents one attribute.
The table makes scanning output more readable than a stream of plain lines.

This matters because users make decisions from output.
A table helps the eye compare entries.
A count at the bottom helps the user confirm the scope of the result.
Structured output communicates confidence.

### Entry points in `pyproject.toml`
The line below is one of the most important lines in the whole week.

```toml
[project.scripts]
researchops = "researchops.cli.main:app"
```

This line tells the packaging system to install a shell command named `researchops`.
When a user runs that command, Python imports the module `researchops.cli.main`.
Then Python loads the object named `app` from that module.
That object is the Typer application.
So the shell command and the Python app object are connected through packaging metadata.

If the module path is wrong, startup fails.
If the object name is wrong, startup fails.
If you change the entry point and forget to reinstall, you may still be running stale installed metadata.
Packaging is part of runtime behavior.

### What happens when the entry point module is wrong
Suppose you write:

```toml
researchops = "researchops.cli.broken:app"
```

Now the installed shell command still exists.
But when it tries to start, it cannot import the target module.
That means the failure happens before your CLI logic runs.
The parser has not even reached `scan()` yet.
This is a packaging startup failure, not a command-logic failure.

That distinction matters.
When debugging, ask first whether the command launches at all.
If startup fails immediately, inspect packaging metadata and imports before debugging command behavior.

### Optional dependency groups
ResearchOps defines several optional groups.
They include `dev`, `storage`, `parsing`, `ml`, `api`, and `all`.
This is not only about convenience.
It is about architecture and installation cost.

A learner exploring the CLI may not need FastAPI yet.
A user working on parsing may not need ML dependencies yet.
A contributor running tests does need the `dev` group.
Grouping dependencies lets the project scale capability without forcing every environment to carry every tool.

This also teaches good software boundaries.
If every feature required every dependency, the project would become heavier and harder to reason about.
Optional groups communicate modularity.

### `CliRunner`
`CliRunner` is how you test Typer applications without manually typing in a real terminal.
It creates an in-process execution environment.
You hand it the app object and the argument list.
It runs the command.
It captures output.
It returns a result object.

This is powerful for three reasons.
First, tests run quickly.
Second, you can assert on output and exit code directly.
Third, you can simulate many command scenarios using ordinary test functions.

If you care about CLI quality, `CliRunner` is not a luxury.
It is one of the core tools of the chapter.

### `# noqa: E402`
You will see this line in `cli/main.py`:

```python
from researchops.cli.commands import ingest, papers, search  # noqa: E402
```

`noqa` means no quality assurance warning for this line.
More specifically, `E402` is a lint rule about import placement.
That rule typically expects imports to be at the top of the file.
Here the import appears after creating `app` and `console`.

Why allow that.
Because sometimes structure and runtime setup make a slightly later import reasonable.
The linter does not know your intent automatically.
The comment tells the linter that this exception is intentional.
This is not a random magic comment.
It is a documented exception to a code-style rule.

### `from __future__ import annotations`
This import changes how type annotations are handled.
In modern Python, it is often used so annotations are stored more lazily as strings rather than fully evaluated immediately.
For beginners, the practical meaning is simpler.
It helps type hints stay flexible and avoids some forward-reference issues.
It also keeps annotation behavior more predictable across modules with interdependent types.

You do not need to become a type-system expert this week.
You do need to recognize that the import exists to improve annotation behavior, not to change the CLI itself.
It is part of modern Python style in many codebases.

## ResearchOps-specific application
Let us ground all of this in the actual project.
ResearchOps is building a research paper processing and experiment-tracking platform.
By Week 4, the project has enough internal structure to expose a real command.
That command is `scan`.

What does `scan` do.
It does not parse PDFs.
It does not ingest them into storage.
It does not generate embeddings.
It does not run ML.
It performs one smaller but useful task.
It scans a directory and lists PDF files.

Why is that a good Month 1 command.
Because it is real.
Because it touches files and paths.
Because it returns meaningful output.
Because it can succeed, fail, or find nothing.
Because it demonstrates help text, options, exit codes, packaging, and tests.
Because it sets the pattern for future commands.

The code path is simple enough for a beginner to follow and real enough to matter.
That makes it a perfect Month 1 culmination.

### End-to-end flow in plain English
A user types `researchops scan ./papers`.
The shell finds the installed `researchops` command.
That command loads `researchops.cli.main:app`.
Typer reads the command line.
Typer decides that `scan` is the command being requested.
Typer sees that `./papers` should be bound to the `directory` parameter.
Typer calls the `scan()` function with `directory` as a Python string and `recursive` as a Python boolean.
Inside `scan()`, the string becomes a `Path` object.
The command calls `find_pdfs(path, recursive=recursive)`.
If scanning fails because the path is not a directory, the command prints a user-friendly error and exits with code `1`.
If scanning succeeds but finds nothing, the command prints a friendly message and exits with code `0`.
If scanning finds PDFs, the command formats a Rich table and prints a final count.

That is the entire interaction chain.
A strong CLI is simply a well-designed version of that chain.

## Full annotated `src/researchops/cli/main.py`
Here is the code for the main CLI entry point.
Study it as a whole before reading the line-by-line commentary.

```python
"""ResearchOps CLI entry point."""
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

from researchops.cli.commands import ingest, papers, search  # noqa: E402
app.add_typer(ingest.app, name="ingest", help="Ingest PDF files into the library.")
app.add_typer(papers.app, name="papers", help="Manage and view stored papers.")
app.add_typer(search.app, name="search", help="Search the paper library.")

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging."),
) -> None:
    """ResearchOps — build, search, and analyse a research paper library."""
    configure_logging(level="DEBUG" if verbose else settings.log_level)

@app.command()
def scan(
    directory: str = typer.Argument(..., help="Path to a directory containing PDF files."),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Search subdirectories recursively."),
) -> None:
    """Scan a directory and list discovered PDF files."""
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

### Line-by-line explanation
Line 1 is the module docstring.
It tells readers the purpose of the file.
A short, accurate docstring is useful because this file is the top CLI entry point.

Line 2 imports future annotation behavior.
This affects type hints.
It does not directly change CLI behavior.
It supports cleaner typing style.

Line 3 imports Typer.
Without this import, there is no CLI framework available.
Typer provides the `Typer` app class, decorators, `Argument`, `Option`, and `Exit`.

Line 4 imports Rich's `Console`.
This is the output object used for styled terminal messages.
It makes the CLI output more readable than plain printing.

Line 5 imports `configure_logging`.
This function handles logging setup.
The CLI should trigger that setup rather than reimplement logging configuration logic inline.

Line 6 imports `settings`.
This gives the CLI access to configured defaults such as the default log level.
The callback can then choose between the configured default and debug mode.

Lines 8 through 13 create the root Typer app.
This app is the central CLI object.
Typer will register commands and sub-apps on it.
The installed command points at this object.

The `name` argument sets the CLI name to `researchops`.
This affects help text and presentation.
It tells Typer how the root app should identify itself.

The `help` argument supplies a user-facing description.
This text appears in `researchops --help`.
Good help text is part of interface quality.

`add_completion=False` disables shell completion setup output.
That keeps the early-stage CLI simpler.
You do not need to worry about shell completion in this chapter.

`rich_markup_mode="rich"` tells Typer help output to understand Rich markup.
This keeps help formatting compatible with Rich's style system.

Line 14 creates a `Console` instance.
This object is reused throughout the file.
Creating it once keeps output consistent.

Line 16 imports grouped command apps.
The import is intentionally placed after app and console creation.
That is why the lint-suppression comment is present.
The code is choosing a structure that the linter would otherwise complain about.

Line 17 attaches the `ingest` sub-app.
The root command now has a grouped command family named `ingest`.
This shows that the CLI is already being designed for growth.

Line 18 attaches the `papers` sub-app.
This keeps paper-management commands under a logical namespace.
Namespaces matter because command discoverability matters.

Line 19 attaches the `search` sub-app.
Again, the structure is communicating domain organization.
Not every command belongs at the root.

Line 21 applies `@app.callback()` to `main()`.
This means `main()` becomes the callback for the root app.
It will run before a command body executes.

Lines 22 through 24 declare the `verbose` option.
It is a boolean option.
Its long form is `--verbose`.
Its short form is `-v`.
Its default is `False`.
Its help text explains its purpose.

Line 25 gives the callback a docstring.
This contributes to the root app description and reader understanding.
Docstrings in CLI code double as both developer documentation and, in some contexts, user-facing help.

Line 26 configures logging.
If `verbose` is true, the level becomes `DEBUG`.
Otherwise the level comes from settings.
This is a nice example of global setup belonging in the callback.

Line 28 applies `@app.command()` to `scan()`.
This registers `scan()` as a root-level command.
The function is not just a normal utility anymore.
It is now part of the public CLI contract.

Line 29 defines `directory`.
It is annotated as `str`.
It is declared with `typer.Argument(...)`.
The `...` means required.
The help text explains what the argument represents.

Why not declare it as an option.
Because the directory is the main target of the command.
Users naturally think of it positionally.
The command acts on that directory.

Line 30 defines `recursive`.
It is a boolean option.
Its default is `False`.
It is exposed as `--recursive` and `-r`.
The help text explains that it changes traversal behavior.

Why not make recursion another argument.
Because recursion modifies how the scan works.
It is not the main object being scanned.
That makes it a better fit for an option.

Line 31 gives `scan()` a docstring.
This helps both readers and command help output.
A concise docstring makes the command more discoverable.

Line 32 imports `Path` inside the function.
This keeps the import close to where it is used.
That is a local-style choice.
The important part is that the handler converts the user string into a path object before delegating work.

Line 33 imports Rich's `Table` inside the function.
This shows that output formatting is part of the command layer.
Formatting belongs here because it is interface work.

Line 34 imports `find_pdfs`.
This is the crucial delegation line.
The CLI is not reimplementing scanning logic.
It is calling reusable application logic.
That is the thin-handler rule in action.

Line 36 converts the raw string to `Path`.
This is the moment where CLI text becomes a richer Python object.
The rest of the function can now work with path methods more naturally.

Line 37 starts a `try` block.
This anticipates a specific failure mode.
The handler expects that user input can be invalid.
That expectation is realistic and user-friendly.

Line 38 calls `find_pdfs(path, recursive=recursive)`.
This is the heart of the command.
Notice how little actual scanning code exists in the handler.
That is a good sign.

Line 39 catches `NotADirectoryError` as `exc`.
This is targeted exception handling.
The code is not swallowing every possible bug.
It is handling one expected user-facing problem cleanly.

Line 40 prints a Rich-formatted error message.
The word `Error:` is highlighted in red.
This helps the user see what happened quickly.

Line 41 raises `typer.Exit(1)`.
This ends command execution with a failure code.
The `from exc` keeps exception chaining information.
The user gets a clean error path.
The shell gets an honest non-zero status.

Line 42 checks for an empty result list.
Empty results are not an error.
They are a successful scan with no matches.
This distinction is important.

Line 43 prints a yellow informational message.
Yellow communicates caution or absence without implying a hard failure.
The message includes the path for clarity.

Line 44 raises `typer.Exit(0)`.
This may look unusual because success can often simply return.
Here it makes the command's completion explicit.
Either approach can work.
The key point is that empty results still count as success.

Line 45 creates a Rich table.
The title includes the scanned path.
`show_lines=False` keeps the table visually simpler.

Line 46 adds the number column.
The style is dim because the index is supporting information.
The width is fixed for readability.

Line 47 adds the filename column.
The cyan style gives the main content visual emphasis.
The file name is usually the thing the user scans first.

Line 48 adds the size column.
The style is green.
The text is right-justified so numeric values align neatly.
That is a small design choice that improves readability.

Line 49 begins a loop over discovered PDFs.
`enumerate(..., start=1)` gives human-friendly row numbers.
The user sees rows starting at 1 rather than 0.

Line 50 computes the file size in kilobytes.
The raw file size comes from `pdf.stat().st_size`.
Dividing by 1024 converts bytes into kilobytes.

Line 51 adds a row to the table.
The row contains the row number, the file name, and the formatted size string.
This is where raw filesystem data becomes presentation data.

Line 52 prints the table.
This is the main visible result of a successful scan with matches.
The user can now inspect files at a glance.

Line 53 prints the final count.
The count confirms the scope of the result.
The bold formatting gives the summary emphasis.

Lines 55 and 56 implement the standard Python module-entry pattern.
If the file is run directly, `app()` starts the CLI.
When the installed shell command loads the module, the app object is imported through the entry point.
Both routes point at the same Typer application.

## Full annotated `pyproject.toml` sections
The packaging file matters because the CLI is not truly shippable until the environment can install it cleanly.
Here are the relevant sections.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "researchops"
version = "0.1.0"
description = "A Python-based research paper processing and experiment-tracking platform"
requires-python = ">=3.11"
dependencies = ["typer>=0.12.0", "rich>=13.0.0", "pydantic>=2.0.0", "pydantic-settings>=2.0.0"]

[project.scripts]
researchops = "researchops.cli.main:app"

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "pytest-cov>=5.0.0", "ruff>=0.4.0", "mypy>=1.10.0"]
storage = ["sqlalchemy>=2.0.0"]
parsing = ["pypdf>=4.0.0"]
ml = ["scikit-learn>=1.4.0", "numpy>=1.26.0", "pandas>=2.2.0"]
api = ["fastapi>=0.111.0", "uvicorn[standard]>=0.30.0", "httpx>=0.27.0"]
all = ["researchops[storage,parsing,ml,api]"]

[tool.hatch.build.targets.wheel]
packages = ["src/researchops"]
```

### Section-by-section explanation
`[build-system]` declares how the project is built.
This tells packaging tools what backend to use.
In this case, the backend is Hatchling.
You do not need deep build-backend expertise this week.
You do need to recognize that modern Python packaging is driven through this metadata.

`requires = ["hatchling"]` says the build system needs Hatchling available.
That is about building the project package itself.
It is different from runtime dependencies like Typer and Rich.

`build-backend = "hatchling.build"` identifies the Python object that performs the build.
Again, this is packaging infrastructure rather than CLI logic.
Still, it is part of what makes the project installable.

`[project]` begins the main project metadata block.
This section contains the package name, version, description, Python version requirement, and base dependencies.
These fields matter to installation and distribution.

`name = "researchops"` defines the package name.
This name matters for installation and metadata.
It is related to, but not identical with, the CLI script name.
In this repo, the package name and command name match, which is a nice simplification.

`version = "0.1.0"` declares the current package version.
This matters for release management.
It also matters for future `version` commands if you add one.

`description = "A Python-based research paper processing and experiment-tracking platform"` gives a one-line project summary.
Good metadata improves understanding when others inspect the package.

`requires-python = ">=3.11"` defines the minimum supported Python version.
That protects the project from being installed on unsupported interpreters.
Version requirements are part of packaging contracts too.

`dependencies = [...]` lists required runtime dependencies.
These are the packages the core project needs in order to run.
Typer and Rich are essential for the CLI.
Pydantic and pydantic-settings support configuration behavior.

`[project.scripts]` is the star of the week.
This section defines console scripts.
Each entry maps a shell command name to a Python import target.

`researchops = "researchops.cli.main:app"` means this.
Install a shell command named `researchops`.
When it runs, import the module `researchops.cli.main`.
Then load the object `app`.
That object is the Typer application.

This is why the exact spelling matters.
If the module path is wrong, the command cannot start.
If the object name is wrong, the command cannot start.
If the object is not the Typer app, the command behaves incorrectly.
Packaging metadata is executable truth.

`[project.optional-dependencies]` begins the optional groups section.
These groups let the project stay modular.
Different capabilities can bring different dependency bundles.

The `dev` group contains testing and quality tools.
`pytest` runs tests.
`pytest-cov` measures coverage.
`ruff` handles linting.
`mypy` handles static type checking.
This group is about contributors and development workflows.

The `storage` group contains `sqlalchemy`.
That signals future database or repository work.
It is not needed for the earliest CLI behavior.
That is why it is separated.

The `parsing` group contains `pypdf`.
This signals future PDF parsing capability.
Scanning files is not the same as parsing documents.
Keeping that dependency optional makes the architecture clearer.

The `ml` group contains `scikit-learn`, `numpy`, and `pandas`.
Those are heavy compared with the Week 4 CLI dependencies.
Separating them keeps the basic installation lighter.
It also reflects the staged curriculum.

The `api` group contains FastAPI, Uvicorn, and HTTPX.
Again, this is future-facing capability.
CLI users do not need web server dependencies just to scan a directory.

The `all` group installs the combined capability groups.
This is a convenience bundle.
It is useful for fully loaded environments.
It is not required for a learner who only needs the current chapter.

`[tool.hatch.build.targets.wheel]` configures what goes into the built wheel.
`packages = ["src/researchops"]` tells Hatch which package directory to include.
This matters because the repository uses a `src/` layout.
That layout reduces accidental import confusion during development.

### Packaging summary in one sentence
The CLI becomes installable because `pyproject.toml` tells Python packaging tools which code to install, which dependencies to bring, and which shell command should point at which Typer app object.

## Full annotated `tests/e2e/test_cli.py`
The test file is short, which is good.
Short tests often mean the CLI layer is staying small and direct.
Here is the file.

```python
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

    def test_scan_lists_pdf_files(self, tmp_path: Path) -> None:
        (tmp_path / "paper_a.pdf").touch()
        (tmp_path / "paper_b.pdf").touch()
        result = runner.invoke(app, ["scan", str(tmp_path)])
        assert result.exit_code == 0
        assert "paper_a.pdf" in result.output

    def test_scan_ignores_non_pdf_files(self, tmp_path: Path) -> None:
        (tmp_path / "paper.pdf").touch()
        (tmp_path / "readme.txt").touch()
        result = runner.invoke(app, ["scan", str(tmp_path)])
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

### Line-by-line explanation
The first line imports `Path`.
This is used only for typing the `tmp_path` fixture parameter.
It also reinforces that file paths are first-class objects in the tests.

The second line imports `CliRunner`.
This is the testing helper that lets Typer run the app in-process.
Without it, testing the CLI would be slower and more awkward.

The third line imports the real `app` object from the real CLI module.
This is crucial.
If you accidentally test the wrong app object, your tests stop validating the real interface.

The fourth meaningful line creates `runner = CliRunner()`.
This instance is reused across tests.
That is normal and efficient.
A new runner per test is usually unnecessary for simple cases like these.

`class TestCLIHelp:` groups help-related tests.
This is optional organizational structure.
It improves readability by separating root-help concerns from scan-command concerns.

`test_help_exits_zero` verifies that asking for help is a successful action.
Help output is not an error.
A user should be able to explore the CLI without causing failure status.
That is why exit code `0` matters here.

`runner.invoke(app, ["--help"])` simulates the user running the root command with the help flag.
Typer parses that invocation.
The result object captures what the CLI printed and how it exited.

`assert result.exit_code == 0` is the core contract assertion.
The test is not checking everything.
It is checking one important promise.
That promise is that help runs successfully.

`test_help_contains_scan` asks whether the help output exposes the `scan` command.
This is a discoverability test.
A command that exists but cannot be found through help is a weaker interface.

The test lowercases the output before searching for `scan`.
That makes the assertion less sensitive to letter casing.
This is a good example of keeping tests focused on meaning rather than typography.

`class TestScanCommand:` groups tests for scan behavior.
Again, this is organizational.
It tells the reader what part of the interface the following tests cover.

`test_scan_empty_directory` uses the `tmp_path` fixture.
Pytest creates a temporary directory automatically.
The directory starts empty.
This is a great test input because it is controlled and isolated.

The invocation passes `str(tmp_path)`.
The CLI expects command-line text.
So the test converts the `Path` object into the string a real user would type.

The assertion expects exit code `0`.
That matters because empty results are not an error.
The command succeeded at scanning.
It simply found no PDFs.

`test_scan_lists_pdf_files` creates two empty files ending with `.pdf`.
The content of the files does not matter for this scan command.
Only their presence and names matter.
That keeps the test focused.

The command runs against the directory.
The first assertion checks success.
The second checks that at least one expected filename appears in output.
This confirms visible reporting, not just internal behavior.

`test_scan_ignores_non_pdf_files` creates one PDF and one text file.
This tests filtering behavior.
A scan command that showed the text file would be violating its contract.
The assertion checks that the non-PDF name is absent from output.

`test_scan_nonexistent_directory` calls the CLI with a path that should not exist.
This is the main error-path test.
The assertion is intentionally broad.
It does not care whether the exit code is exactly `1` or another non-zero code in this test.
It cares that the command signals failure.

`test_scan_recursive_flag` creates a nested directory structure.
This is how you test behavior changes caused by an option.
The test runs the command twice.
One invocation omits `--recursive`.
The other includes it.

The assertions compare outputs rather than internal variables.
That is appropriate for a CLI test.
The test is validating visible behavior from the user perspective.
Without recursion, nested files should stay hidden.
With recursion, nested files should appear.

### What `result.output` gives you
`result.output` is the captured text printed by the CLI.
This is the user-facing transcript of the run.
It lets you assert on messages, filenames, and help content.
When a test fails, reading the output often tells you whether the problem is parsing, application logic, or formatting.

### What `result.exit_code` gives you
`result.exit_code` is the machine-facing status of the command.
This matters for shell scripts, CI, and automation.
In tests, it also acts as a quick truth check.
Did the command succeed when it should succeed.
Did it fail when it should fail.
Output alone cannot answer that.

## Execution flow diagram
Study this diagram until you can say it from memory.

```text
researchops scan ./papers
        |
        v
installed shell script from [project.scripts]
        |
        v
import researchops.cli.main
        |
        v
load object app
        |
        v
Typer parses command line
        |
        +--> root callback runs
        |        |
        |        v
        |   configure logging
        |
        v
Typer selects scan command
        |
        v
scan(directory="./papers", recursive=False)
        |
        v
path = Path(directory)
        |
        v
find_pdfs(path, recursive=recursive)
        |
        +--> raises NotADirectoryError --> print error --> exit 1
        |
        +--> returns [] --> print no PDFs --> exit 0
        |
        +--> returns [pdfs] --> build Rich table --> print count --> exit 0
```

### Another view of the same flow
Input text comes from the shell.
Typer translates that text into typed function inputs.
The command handler converts and validates user-facing data.
Application logic performs the real work.
Rich formats the human-facing output.
Exit codes communicate the machine-facing status.
That is the full loop.

## Common beginner mistakes
This section matters because most CLI frustration comes from a small set of repeated errors.
If you can recognize these patterns, you will debug faster.

### Mistake 1
Using `typer.Option(...)` for the main required target of a command.
Why it happens.
Beginners sometimes think every input should be a flag.
Why it is a problem.
The command becomes more awkward and less natural to call.
Why the Week 4 code avoids it.
The directory is the main thing being acted on, so it is positional.

### Mistake 2
Giving `typer.Argument` a real default when you intended the value to be required.
Why it happens.
A default feels convenient.
Why it is a problem.
The interface contract silently changes.
The help output also changes.
The user may now omit an input you actually needed.
The Week 4 code uses `...` to mark the argument as required.

### Mistake 3
Printing an error message but forgetting to exit non-zero.
Why it happens.
The developer thinks the message itself is enough.
Why it is a problem.
Humans see failure, but scripts see success.
That can break automation and CI.
The Week 4 code uses `raise typer.Exit(1)` to avoid this.

### Mistake 4
Treating an empty directory as an error.
Why it happens.
Beginners may think no results means failure.
Why it is a problem.
The scan still worked correctly.
It simply found no PDFs.
The Week 4 code treats that as success with a helpful message.

### Mistake 5
Catching `Exception` too broadly.
Why it happens.
It seems like a fast way to keep the CLI from crashing.
Why it is a problem.
It hides real bugs and makes debugging harder.
The Week 4 code catches a specific expected error instead.

### Mistake 6
Testing the wrong app object.
Why it happens.
The test imports the wrong module or constructs a dummy app.
Why it is a problem.
The tests no longer validate the real CLI.
The Week 4 test file imports `app` directly from `researchops.cli.main`.

### Mistake 7
Forgetting to reinstall after changing entry point metadata.
Why it happens.
Source edits often feel instantly visible in editable installs.
Why it is a problem.
Installed console script metadata can remain stale.
The result is confusing startup behavior.
Packaging changes often require reinstalling.

### Mistake 8
Asserting on exact terminal spacing instead of stable content.
Why it happens.
A beginner wants to prove the whole output is correct.
Why it is a problem.
Rich formatting can make brittle exact-output assertions annoying.
It is usually better to assert on important substrings and exit code.

### Mistake 9
Putting too much business logic into the command handler.
Why it happens.
The handler feels like the easiest place to write code.
Why it is a problem.
The CLI becomes long, hard to test, and hard to reuse.
The Week 4 code delegates scanning to `find_pdfs()`.

### Mistake 10
Confusing packaging name, module path, and command name.
Why it happens.
All three names can look related.
Why it is a problem.
A typo in one place breaks the startup chain.
You must know which name belongs to packaging metadata, which belongs to Python imports, and which belongs to shell invocation.

## Debugging guidance
Debugging CLIs gets easier when you classify the failure first.
Do not start by changing random code.
Start by asking what kind of failure you are looking at.

### Question 1
Does the shell recognize the command name at all.
If not, the problem may be installation or environment activation.
Check whether the package was installed.
Check whether the virtual environment is active.
Check whether `[project.scripts]` exists.

### Question 2
Does the command exist but crash before showing help.
If yes, suspect the entry point.
Check `researchops = "researchops.cli.main:app"`.
Check that the module path exists.
Check that the object name is really `app`.
Then reinstall.

### Question 3
Does help work, but the command invocation fail before your function body runs.
If yes, suspect argument or option parsing.
Check the command signature.
Check whether you used `Argument` versus `Option` correctly.
Check whether the user invocation matches the signature.

### Question 4
Does the command run but give the wrong visible result.
If yes, inspect the delegated logic.
For `scan`, that means `find_pdfs()` and the conditions around its result.
Also inspect output formatting code if the data seems correct but presentation is wrong.

### Question 5
Does the message look correct but tests still fail.
If yes, check the exit code assertion.
Output and exit status are separate dimensions.
The test may be catching a contract bug you did not notice manually.

### Debugging wrong entry point
Symptom.
`researchops --help` fails immediately.
Likely cause.
Wrong module path or wrong object name in `[project.scripts]`.
What to inspect.
`pyproject.toml` and the existence of `researchops.cli.main:app`.
What to do next.
Restore the correct entry point and reinstall the package.

### Debugging wrong exit code
Symptom.
The CLI prints an error, but the test expects non-zero and gets `0`.
Likely cause.
You printed an error but returned normally.
What to inspect.
The error-handling branch inside the command.
What to do next.
Use `raise typer.Exit(1)` for user-facing failure.

### Debugging captured output in tests
Symptom.
The test says output does not contain something you thought was printed.
Likely cause.
Either the wrong app was invoked, the branch did not execute, or the formatting differs from your assumption.
What to inspect.
`result.output` directly.
Also inspect the exact invocation passed to `runner.invoke()`.
What to do next.
Print or read `result.output` in the failing test run and compare it to the expected branch.

### A reliable debugging order
1. Confirm the environment is active.
2. Confirm the package installs.
3. Confirm the root help works.
4. Confirm command help works.
5. Confirm the command signature matches the invocation.
6. Confirm the delegated logic returns what you think it returns.
7. Confirm output assertions are testing stable content.
8. Confirm exit-code assertions match the intended contract.

## Design tradeoffs
Design is often choosing the least painful compromise.
This chapter contains several tradeoffs worth noticing.

### Typer versus `argparse`
`argparse` is part of the standard library.
That is a real advantage.
It avoids an extra dependency.
It is also very common in older Python code.

So why use Typer here.
Because Typer is easier to read for beginners.
It maps naturally onto function signatures.
It integrates help generation cleanly.
It works well with type hints.
For a learning repo and a modern CLI, that readability matters.

The tradeoff is dependency versus developer experience.
This course chooses better learning ergonomics and clean modern structure.
That is a reasonable choice.

### Typer versus Click
Typer builds on Click ideas.
Click is mature and widely used.
Typer feels more type-hint-native.
For this course, Typer makes the code feel closer to ordinary Python.
That reduces conceptual friction.

The tradeoff is that Click experience transfers well to Typer, but Typer often feels more approachable for newer Python developers who are already learning function signatures and annotations.

### Thin handlers versus all-in-one scripts
Putting logic directly in the command can feel faster at first.
There is less jumping between files.
A tiny script sometimes really is fine.

But ResearchOps is not being built as a one-off script.
It is being built as a layered application.
Thin handlers cost a bit more thought early.
They save a lot of pain later.
They make testing easier.
They make reuse easier.
They make API and CLI parity easier.

### Testing the CLI versus only testing helpers
Testing only `find_pdfs()` would be easier than testing the CLI.
But it would miss interface problems.
It would not tell you whether help text works.
It would not tell you whether exit codes are correct.
It would not tell you whether `--recursive` is wired into the CLI signature.

Testing the CLI catches user-interface contract issues.
Testing helpers catches core logic issues.
A mature project needs both.
The Week 4 test file focuses on CLI behavior because this chapter is about the interface layer.

### Rich output versus plain text output
Plain text is simpler.
Rich output is more expressive.
Rich tables and colors improve readability.
They also add some formatting complexity.
For a user-facing tool, the readability benefit is worth it here.

### Root-level commands versus grouped subcommands
A flat CLI is simpler at very small scale.
A grouped CLI scales better.
ResearchOps already anticipates growth.
That is why grouped sub-apps are present even though Month 1 is still early.
The tradeoff favors future organization.

## Testing implications
CLI testing changes how you think about software contracts.
The contract is not only internal return values.
The contract includes:
- what the user types,
- what the command prints,
- what exit code it returns,
- which help text appears,
- how options change behavior.

That means CLI tests often assert on three layers at once.
They assert invocation shape.
They assert output behavior.
They assert process status.
This is different from many pure unit tests that inspect direct function return values only.

The good news is that Typer makes this approachable.
`CliRunner` keeps the tests compact.
Pytest fixtures like `tmp_path` make filesystem scenarios easy to isolate.
The current test file is a good model because it tests real outcomes without becoming noisy.

There is also a deeper lesson.
When your interface layer is thin, CLI tests stay small.
When your interface layer is bloated, CLI tests become awkward because they must indirectly exercise too much logic through one entry point.
So testability and architecture are linked.

## Architecture implications
The course architecture rules matter here.
The CLI is not supposed to become the business core of the application.
It is a wiring layer.
That means the CLI may import and call lower-level logic.
It does not mean lower layers should import the CLI.
Dependency direction still matters.

This chapter already hints at the correct pattern.
`scan()` calls `find_pdfs()`.
The handler gathers input, delegates work, and formats output.
That keeps reusable behavior outside the interface layer.

As ResearchOps grows, the same principle should apply more strongly.
A future ingestion command should call a service.
A future search command should call a service.
A future API endpoint should call that same service.
That is how you avoid duplicating business rules across interfaces.

The CLI can know about user input patterns and presentation choices.
The CLI should not become the place where domain logic lives permanently.
That would violate the project's layered direction.

### CLI responsibilities
The CLI should:
- declare commands,
- parse arguments and options,
- perform light input adaptation,
- trigger logging or app setup,
- call services or helpers,
- format terminal output,
- set exit codes.

### CLI non-responsibilities
The CLI should not:
- own long-term business rules,
- embed storage implementation details everywhere,
- perform heavy domain workflows inline,
- become the only interface where core behavior exists,
- hide architecture boundaries for convenience.

## How this connects to ML and AI work
This week may feel like terminal plumbing.
It is much more than that.
Many serious ML and AI workflows are CLI-driven.

Training scripts are often CLIs.
Evaluation scripts are often CLIs.
Batch inference jobs are often CLIs.
Data preprocessing pipelines are often CLIs.
Experiment runners are often CLIs.
Even when a web dashboard exists, the reproducible core workflow is often a command.

Why.
Because command lines are explicit.
Flags make parameters visible.
A command can be copied into documentation.
A command can be pasted into a notebook cell or shell script.
A command can be saved in logs.
A command can be rerun exactly.
That is reproducibility.

Imagine a future command like this.

```bash
researchops train-topics --input data/papers.json --model lda --topics 20 --seed 42
```

That command becomes a recorded experiment configuration.
You know the input.
You know the model choice.
You know the topic count.
You know the seed.
The interface itself helps reproducibility.

Exit codes matter there too.
A failed training job in CI or a scheduled pipeline must return non-zero.
Thin handlers matter there too.
You do not want expensive ML logic buried in a messy command function.
You want the CLI to pass validated parameters into reusable training logic.

So Week 4 is not a side lesson.
It is foundational for later AI workflow design.

## Scenario drills
Sometimes understanding becomes clearer when you apply the ideas to small scenarios.
Use these as mental rehearsals.

### Scenario 1
A user runs `researchops --help`.
What should happen.
The app should print discoverable help.
The exit code should be `0`.
No domain logic like scanning should run.
This is interface exploration, not task execution.

### Scenario 2
A user runs `researchops scan ./papers`.
What should happen.
Typer should bind `./papers` to the `directory` argument.
The callback should configure logging.
The command should convert the string to `Path`.
The command should call `find_pdfs()`.
The result should be formatted for the terminal.

### Scenario 3
A user runs `researchops scan ./papers --recursive`.
What should change.
Only the traversal behavior.
The shape of the command stays the same.
The option modifies behavior without becoming the main object of the command.

### Scenario 4
A user runs `researchops scan does-not-exist`.
What should happen.
The command should catch the expected directory error.
The command should print a clean error message.
The command should exit non-zero.
The command should not pretend the run succeeded.

### Scenario 5
A contributor changes `[project.scripts]` and forgets to reinstall.
What should you suspect.
Stale installed metadata.
This is not necessarily a bug in `scan()`.
This is a packaging refresh issue.

### Scenario 6
A test asserts that `result.output` contains `paper_a.pdf`, but it does not.
What should you inspect first.
The created files.
The invocation arguments.
Whether the right app was imported.
Whether recursion was needed.
Whether the output branch was the one you expected.

## Quick comparison table
Use this table to compress the chapter into a few contrasts.

| Concept | Best short description | Week 4 example |
|---|---|---|
| CLI | Text interface for a program | `researchops scan ./papers` |
| GUI | Visual interface for a program | future dashboard or desktop app |
| API | Programmatic interface for other software | future FastAPI endpoints |
| Argument | Required positional input | `directory` |
| Option | Named modifier input | `--recursive` |
| Callback | Global setup before commands | `--verbose` logging setup |
| Command decorator | Registers a function as a command | `@app.command()` on `scan` |
| Sub-app | Group of related commands | `ingest`, `papers`, `search` |
| Exit code `0` | Success | help, empty scan, successful scan |
| Exit code non-zero | Failure | invalid directory |
| Entry point | Installed command mapping | `researchops.cli.main:app` |
| Rich markup | Styled text syntax | `[red]Error:[/red]` |
| `CliRunner` | In-process CLI test helper | `runner.invoke(app, [...])` |
| Optional group | Installable capability bundle | `dev`, `ml`, `api` |

## Mini quizzes
Try the question before reading the answer.

### Quiz 1
Why is `directory` modeled as an argument instead of an option.

Answer.
Because it is the main thing the command acts on.
Users naturally supply the target directory positionally.
Options are better for modifiers such as recursion.

### Quiz 2
Why does `--verbose` belong in the callback.

Answer.
Because logging level is a global concern.
It affects the app as a whole, not only one command.
The callback is where app-wide setup belongs.

### Quiz 3
What does `researchops = "researchops.cli.main:app"` mean.

Answer.
Install a shell command named `researchops`.
When it runs, import the module `researchops.cli.main`.
Then load the object named `app` from that module.
That object is the Typer application.

### Quiz 4
A command prints `Error:` but exits with code `0`.
Why is that a bug.

Answer.
Because the shell and CI will treat the run as success.
Human-visible output and machine-visible status are separate.
A real failure must return non-zero.

### Quiz 5
Why use `CliRunner` instead of manually running subprocesses for every small CLI test.

Answer.
Because it runs the app quickly in-process.
It captures output and exit status directly.
It keeps tests compact and focused.

### Quiz 6
Why is `find_pdfs()` called from the handler instead of copying its logic into `scan()`.

Answer.
Because the CLI should stay thin.
Delegated logic is easier to test, reuse, and share with future interfaces.
This supports the project architecture.

### Quiz 7
What is the point of optional dependency groups.

Answer.
They keep installations modular.
Users and contributors can install only the capabilities they need.
This keeps the project lighter and clearer.

### Quiz 8
What problem does `# noqa: E402` solve in this file.

Answer.
It tells the linter that the intentionally delayed import is acceptable.
The code structure is choosing a later import for a reason.
The comment prevents an import-order warning from becoming noise.

## Explain-it-aloud prompts
If you can explain these aloud clearly, you understand the chapter.

1. Explain the difference between a CLI, a GUI, and an API using ResearchOps examples.
2. Explain why Typer feels beginner-friendly compared with older CLI styles.
3. Explain `typer.Argument` and `typer.Option` to someone who has never built a CLI.
4. Explain `@app.callback()` in one minute without reading notes.
5. Explain why `scan()` is a thin handler and why that is good.
6. Explain how `researchops` becomes an installed shell command.
7. Explain why exit codes matter even when the printed message looks clear.
8. Explain how `CliRunner` helps test interface behavior.
9. Explain why optional dependency groups support architecture boundaries.
10. Explain why this week matters for future ML workflows.

## What to memorize
Some facts are worth memorizing exactly.
Memorization is not the whole chapter, but it reduces friction.

Memorize that `0` means success.
Memorize that non-zero means failure.
Memorize that `typer.Argument(...)` usually means positional required input.
Memorize that `typer.Option(...)` usually means named optional input.
Memorize that `@app.command()` registers a command.
Memorize that `@app.callback()` handles app-wide setup.
Memorize that `app.add_typer()` attaches a sub-app.
Memorize that the entry point is `researchops = "researchops.cli.main:app"`.
Memorize that `CliRunner` tests a Typer app in-process.
Memorize that `[red]`, `[yellow]`, and `[bold]` are Rich markup tags.

## What to understand deeply
These are deeper than memorization.
If you understand them, you can adapt to new situations.

Understand that the CLI is an interface layer, not the business core.
Understand that input parsing, domain work, and output formatting are different concerns.
Understand that help text and exit codes are part of the feature, not decoration.
Understand that packaging metadata participates in runtime behavior.
Understand that command grouping is an interface design decision, not just code organization.
Understand that tests validate contracts visible to both humans and automation.
Understand that optional dependencies express project boundaries and capability staging.
Understand that reproducible ML workflows depend on explicit command-line parameters and reliable exit behavior.

## What not to worry about yet
A good curriculum protects beginners from premature complexity.
You do not need to master every packaging detail this week.
You do not need to master shell completion.
You do not need to memorize every Rich feature.
You do not need to build nested subcommand trees from scratch yet.
You do not need to become an expert in Python build backends.
You do not need to know every possible POSIX exit code convention.
You do not need to overengineer a service layer for tiny placeholder commands.
You do need the core mental model.

## PowerShell equivalents for Windows learners

All validation commands in this chapter are shown in macOS/Linux shell syntax.
The following table covers the differences for Windows PowerShell.

### Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### Run all standard commands

These work identically on all platforms.

```powershell
python -m pip install -e ".[dev]"
researchops --help
researchops scan --help
researchops scan .scratch\week-04-cli\papers
researchops scan .scratch\week-04-cli\papers --recursive
researchops scan .scratch\week-04-cli\missing
pytest tests/e2e/test_cli.py -v
pytest -q
ruff check src tests
```

### Check exit code

After running a command that should fail:

```powershell
researchops scan .scratch\week-04-cli\missing ; echo $LASTEXITCODE
```

Expected output:
```text
1
```

On macOS/Linux, use `echo $?` instead.

### Create the scratch validation dataset on Windows

On macOS/Linux, the validation dataset can be created with a heredoc:
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

PowerShell does not support the `<<'PY'` heredoc syntax. Instead, save the Python snippet to a temporary file and run it:

```powershell
Set-Content -Path "$env:TEMP\setup.py" -Value @'
from pathlib import Path
root = Path(".scratch/week-04-cli/papers")
(root / "nested").mkdir(parents=True, exist_ok=True)
(root / "paper_a.pdf").touch()
(root / "nested" / "paper_b.pdf").touch()
(root / "notes.txt").write_text("not a pdf\n")
print(root)
'@
python "$env:TEMP\setup.py"
```

### Summary difference table

| macOS / Linux shell | Windows PowerShell |
|---|---|
| `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| `echo $?` | `echo $LASTEXITCODE` |
| `<<'PY' ... PY` heredoc | save to temp file and `python file.py` |
| Everything else | identical |



## A compact chapter recap
Week 4 teaches how a real command gets shipped.
Typer turns typed Python functions into CLI commands.
Arguments capture the main target of the command.
Options modify behavior.
Callbacks configure app-wide behavior such as logging.
Sub-apps organize command families.
Rich improves terminal output quality.
Exit codes communicate success and failure to machines.
Entry points in `pyproject.toml` connect shell commands to Python objects.
`CliRunner` lets you test the CLI contract in-process.
Thin handlers protect architecture and reuse.
ResearchOps uses all of these ideas to deliver `researchops scan`.

## Bridge to next week and Month 2
Month 1 ends with a usable tool.
That is a big achievement.
You now have a project that can be installed, invoked, and tested through a public interface.
That means Month 2 can build on something real.

In the next phase of the curriculum, you will likely care more about persistence, service boundaries, and richer workflows.
When storage enters the picture, the CLI patterns from this week become even more important.
A command will need to trigger real application services.
Those services may talk to repositories.
Those repositories may talk to SQLite.
The CLI should still remain thin.

So the Month 2 preview is this.
The interface gets more powerful.
The internals get richer.
The architecture matters more, not less.
Week 4 prepared you for that by teaching the public boundary first.

## Final synthesis
If you remember one sentence from the whole chapter, remember this.
A professional CLI is a thin, testable interface that turns typed user input into delegated application behavior, formats the result clearly, and exits honestly.

If you remember one ResearchOps-specific sentence, remember this.
`researchops scan` is valuable not because scanning files is glamorous, but because it proves the project can now expose real behavior through a packaged, testable, user-facing command.

If you remember one forward-looking sentence, remember this.
The same CLI design habits you learn here will later support data pipelines, experiment runners, ingestion jobs, search workflows, and ML training commands.

## End-of-chapter self-check
Answer these without looking back.

1. What are the three main jobs of a thin CLI handler.
2. Why is `directory` a positional argument.
3. Why is `--recursive` an option.
4. Why is `--verbose` handled by the callback.
5. What does `app.add_typer()` make possible.
6. What does exit code `0` mean.
7. What should happen on an invalid directory.
8. What object does the `researchops` entry point load.
9. What does `CliRunner` capture.
10. Why are optional dependencies grouped.
11. What does `# noqa: E402` communicate.
12. Why does this week matter for future ML and AI workflows.

### Self-check answers
1. Gather input, call application logic, format output.
2. Because it is the main thing being acted on.
3. Because it modifies behavior rather than identifying the main target.
4. Because logging configuration is app-wide.
5. Grouped command families and multi-level CLI structure.
6. Success.
7. Print a clean error and exit non-zero.
8. The Typer app object named `app` in `researchops.cli.main`.
9. Output text and exit status, along with related run information.
10. To keep capabilities modular and installations lighter.
11. That an intentionally delayed import should not trigger the import-order lint rule.
12. Because reproducible pipelines and experiment runners often depend on clear CLI parameters, good output, and honest exit codes.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← README](README.md) · ➡️ [Exercises →](exercises.md)

**Week 04 — CLI and Packaging:** [README](README.md) · **Notes** · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
