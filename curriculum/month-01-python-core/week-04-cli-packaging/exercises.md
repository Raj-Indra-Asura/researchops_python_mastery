<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 04 — CLI and Packaging:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 04 CLI and Packaging

## How to use this workbook
This workbook is designed to move you from recognition to recall to independent design.
Do not only read the questions.
Write answers.
Trace code.
Run commands.
Break assumptions.
Explain your reasoning out loud.

The chapter goal is not merely to remember Typer syntax.
The goal is to internalize how a professional CLI layer fits into a larger application.

---

## Warm-up exercises
Answer these without opening the code first.
Then verify your answers against `notes.md`.

1. In one sentence, what is a CLI?
2. In one sentence, what is Typer?
3. What is the difference between `typer.Argument(...)` and `typer.Option(...)`?
4. What does `@app.command()` do?
5. What does `@app.callback()` do?
6. Why would `--verbose` usually belong in the callback instead of inside one command?
7. What does `app.add_typer()` let you build?
8. What does exit code `0` mean?
9. Why does a non-zero exit code matter to CI?
10. What object is exported by `researchops.cli.main` as the installed entry point?
11. What does `CliRunner.invoke()` give you after a test run?
12. Why should CLI handlers stay thin?
13. What is Rich adding that plain `print()` does not?
14. What does `[project.scripts]` in `pyproject.toml` control?
15. Why are optional dependency groups useful in this project?

### Self-check key
Use this key only after attempting the questions yourself.

1. A CLI is a text-based interface for interacting with a program through terminal commands.
2. Typer is a Python CLI framework that turns typed function signatures into command-line interfaces.
3. `Argument` is usually required and positional; `Option` is usually optional and flag-based.
4. `@app.command()` registers a function as a CLI command.
5. `@app.callback()` runs before commands and is commonly used for global options and setup.
6. Because `--verbose` changes app-wide behavior, not just one command.
7. It lets you attach sub-apps to build grouped commands such as `researchops ingest ...`.
8. Success.
9. CI reads exit codes to decide whether a command passed or failed.
10. The `app` Typer object.
11. A result object containing output, exit code, and exception information.
12. So interface code stays easy to test, reason about, and replace.
13. Styled terminal output such as color, tables, and clearer presentation.
14. It defines shell command entry points installed from the package.
15. They let users install only the parts of the system they currently need.

---

## Section 2 - Vocabulary drills
Fill in the blanks.

1. A required positional value in Typer is commonly declared with `typer.________(...)`.
2. A flag such as `--recursive` is commonly declared with `typer.________(...)`.
3. To exit a Typer command with a specific code, you raise `typer.________(code=...)`.
4. The installed command name `researchops` is defined under `[project.________]`.
5. A test helper that runs the app in-process is called `________`.
6. Rich color tags such as `[red]` and `[bold]` are examples of Rich `________`.
7. A grouped Typer application is attached with `app.________(...)`.
8. The file format used by `pyproject.toml` is called `________`.
9. A dependency collection such as `dev` or `ml` is an optional dependency `________`.
10. The comment `# noqa: E402` tells a linter to ignore an import-order `________`.

### Answers
1. `Argument`
2. `Option`
3. `Exit`
4. `scripts`
5. `CliRunner`
6. markup
7. `add_typer`
8. TOML
9. group
10. warning

---

## Code-reading exercises
Open `src/researchops/cli/main.py`.
Read it top to bottom.
Then answer the questions.

### Part A - Observation
1. What is the first executable object created in the file?
2. Which object is responsible for user-facing terminal output?
3. Which imports are delayed until after `app` and `console` are created?
4. Why might the file create the root app before importing grouped commands?
5. Which function handles global logging setup?
6. Which function implements the `scan` command?
7. Which part of the file converts a string path into a `Path` object?
8. Which part of the file catches a user-facing directory error?
9. Which part prints the total number of PDFs found?
10. Which part ends the process with exit code `1`?

### Part B - Explanation
Write 2-4 sentences for each.

1. Why is `directory` annotated as `str` in the command signature instead of `Path`?
2. Why is `Path(directory)` created inside the function?
3. Why is `find_pdfs()` called inside a `try` block?
4. Why is empty-directory behavior not treated as an error?
5. Why is `console.print()` preferred over raw `print()` here?

### Part C - Architecture thinking
1. Which line shows the CLI delegating work instead of doing everything itself?
2. If `scan()` directly walked the filesystem line by line, what architectural risk would that create?
3. If you later added an API endpoint for scanning, why would you want shared logic outside the CLI file?

---

## Section 4 - Argument versus option drills
For each input, decide whether it should be modeled as an argument or an option.
Explain why.

1. The directory to scan.
2. Whether to recurse into subdirectories.
3. Whether to enable verbose logging globally.
4. A maximum number of results to print.
5. The output format: table, plain text, or JSON.
6. The experiment run name for a future training command.
7. The path to a required configuration file.
8. A `--dry-run` flag.

### Challenge extension
Rewrite each item as a Typer declaration in pseudocode.
Example format:

```python
limit: int = typer.Option(10, "--limit", help="Maximum rows to show.")
```

---

## Section 5 - Mental model practice
Write a short answer for each prompt.

1. Explain the phrase "the CLI is a user interface layer" to a beginner.
2. Explain the phrase "thin command handler" to a beginner.
3. Explain why packaging is part of user experience.
4. Explain why help text is part of the feature, not an extra.
5. Explain why exit codes matter even when the on-screen message looks correct.

### Speaking drill
Say this aloud without notes:

> The command layer should gather input, call application logic, and format output.
> If it starts owning domain rules, parsing logic, storage decisions, and heavy work, the CLI becomes hard to test and hard to reuse.

Now restate it in your own words.

---

## Section 6 - Trace the end-to-end flow
Use the actual code and fill in the blanks.

```text
researchops scan ./papers
    -> installed entry point from __________________
    -> imports object named __________________
    -> Typer resolves subcommand __________________
    -> function __________________ runs
    -> string argument becomes __________________
    -> helper function __________________ is called
    -> result list is formatted into a __________________
    -> terminal output is written through __________________
```

### Answers
- `pyproject.toml`
- `app`
- `scan`
- `scan`
- `Path(directory)`
- `find_pdfs`
- Rich table
- `console.print`

### Extension prompt
Now trace the error flow when the directory does not exist.
Name the exception, the message path, and the exit code.

---

## Section 7 - Packaging workbook
Open `pyproject.toml`.
Answer every question in writing.

1. Which build backend is configured?
2. Why does the project specify `requires-python = ">=3.11"`?
3. Which dependencies are required for the core CLI to run?
4. Which dependency group contains testing and linting tools?
5. Which group adds database-related tools?
6. Which group adds PDF parsing capability?
7. Which group adds ML data stack tools?
8. Which group adds API framework tools?
9. What does the `all` group do conceptually?
10. What is the exact entry point string for the installed CLI?
11. Why would a typo in that string break the installed command?
12. What does the Hatch wheel target include in the package?

### Applied exercise
Rewrite the meaning of this line in plain English:

```toml
researchops = "researchops.cli.main:app"
```

Your answer should mention all three pieces:
- the shell command name,
- the Python module path,
- the Python object being loaded.

---

## Testing exercises
Open `tests/e2e/test_cli.py`.
Work through the file in order.

### Part A - Identify what is under test
1. What object is imported from `researchops.cli.main`?
2. Why is `CliRunner()` created once at module level?
3. What does `runner.invoke(app, ["--help"])` simulate?
4. Why do these tests not need a real terminal window?
5. Why do these tests still count as end-to-end for the CLI layer?

### Part B - Match tests to behavior
Match each test to the contract it verifies.

- `test_help_exits_zero`
- `test_help_contains_scan`
- `test_scan_empty_directory`
- `test_scan_lists_pdf_files`
- `test_scan_ignores_non_pdf_files`
- `test_scan_nonexistent_directory`
- `test_scan_recursive_flag`

Contracts to match:
- empty successful run stays successful,
- help text is discoverable,
- root help does not fail,
- top-level command listing includes `scan`,
- non-PDF files are filtered out,
- user error becomes non-zero exit,
- recursive option changes behavior.

### Part C - Add your own tests on paper first
Before writing code, design tests for these future features.

1. A `--count-only` option.
2. A `version` command.
3. A `--json` output mode.
4. A path that exists but points to a file instead of a directory.
5. A future `papers list` command group.

For each one, state:
- the invocation,
- the expected exit code,
- one output assertion.

---

## Implementation exercises
These are optional build exercises if you are actively coding along.
They are ordered from easiest to harder.

### Exercise 1 - Add a `version` command
Goal: add a simple command with no positional arguments.

Requirements:
- command name: `version`
- output: package version string
- exit code: `0`
- test: confirm help or output contains a version value

Questions to answer after implementing:
1. Why is this a good first command to practice with?
2. Why does it not need a separate service layer yet?
3. At what point would even a small command deserve abstraction?

### Exercise 2 - Add a `--count-only` option to `scan`
Goal: practice adding an option without changing the core scan logic.

Requirements:
- default behavior remains the existing Rich table
- `--count-only` prints just the number of PDFs found
- empty directory still exits `0`
- invalid directory still exits `1`

Reflection:
- Did you keep the handler thin?
- Did the option affect formatting only, or did it change business logic too?

### Exercise 3 - Add a `--json` option
Goal: practice output modes.

Requirements:
- when omitted, keep current behavior
- when enabled, print JSON-compatible output
- decide whether the JSON should include file sizes, names, or paths
- add tests for both modes

Architecture question:
- Should formatting live entirely in `cli/main.py`, or should some serialization move elsewhere?

### Exercise 4 - Add a grouped command under `papers`
Goal: understand `app.add_typer()` and nested command organization.

Requirements:
- inspect the existing grouped apps
- add one simple read-only command under `papers`
- confirm `researchops papers --help` shows the subcommand
- write at least one test

Design question:
- When should a command become its own sub-app instead of staying at the root?

---

## Written explanation exercises
Answer in complete sentences.

1. Why is the root CLI app created before sub-apps are attached?
2. Why is it valuable that Typer uses type hints?
3. Why is help text part of interface design?
4. Why is a friendly error plus exit code better than a raw traceback for normal user mistakes?
5. Why is an installable command more professional than telling users to run a Python file directly?
6. Why is `CliRunner` especially useful in a teaching repo like this one?
7. Why should optional dependencies be separated by capability?
8. Why does CLI design matter for future ML and experiment workflows?

---

## Debugging exercises
For each mistake, write:
- what the beginner was probably trying to do,
- what went wrong,
- how to fix it.

1. Using `typer.Option(...)` for a required path that should be positional.
2. Giving `typer.Argument(".")` a default, then wondering why the argument is not required.
3. Printing an error message but forgetting to exit non-zero.
4. Catching `Exception` and hiding the real cause.
5. Changing `[project.scripts]` but forgetting to reinstall.
6. Testing the wrong `app` object.
7. Asserting on exact table spacing instead of important substrings.
8. Moving business logic into the CLI handler because it "felt faster."

---

## Stretch exercises
Write a paragraph for each comparison.

1. CLI versus GUI.
2. CLI versus API.
3. Typer versus `argparse`.
4. Typer versus Click.
5. Testing CLI behavior versus testing underlying utility functions directly.

### Challenge
Explain why a mature project often needs all three user interfaces at different times:
- CLI,
- API,
- GUI or web UI.

Use ResearchOps examples in your answer.

---

## Section 13 - Architecture alignment drill
Read the architecture rules for the repository.
Then answer these questions.

1. Why must CLI not contain business logic?
2. If future ingestion logic grows complex, where should that logic live?
3. Why is it helpful that both CLI and API can call the same service layer?
4. What kind of code belongs in `cli/main.py`?
5. What kind of code does not belong there?
6. Why does this separation become even more important as command count grows?

### Scenario question
A teammate wants to parse PDFs directly inside a CLI command because "it is only one place."
Write a response explaining why that is risky in this architecture.

---

## Section 14 - CLI and ML thinking
These prompts connect Week 4 to later AI work.

1. Why are ML training scripts often designed as CLIs?
2. Why are command-line flags useful for reproducible experiments?
3. Why is a command such as `train --model linear --seed 42 --epochs 10` easier to document than hidden notebook state?
4. Why do exit codes matter in scheduled jobs and pipelines?
5. Why do thin handlers matter even more when commands trigger long-running or expensive work?

### Applied prompt
Imagine a future command:

```bash
researchops train-topics --input data/papers.json --model lda --topics 20 --seed 42
```

Write a design note explaining:
- which values should be arguments,
- which should be options,
- where the training logic should live,
- what success output should include,
- what failures should return.

---

## Brutal exercises
These tasks require careful CLI reasoning. They are still Month 1 tasks: stay with packaging, Typer, tests, and thin command handlers.

### Brutal 1 - Design a non-brittle assertion strategy
For the Rich table produced by `researchops scan`, list five substrings that are stable enough to assert in tests and five visual details that are too brittle. Explain why table spacing should not be the main contract.

### Brutal 2 - Diagnose three packaging failures
For each symptom, write the likely cause and first fix: the `researchops` command is missing, the command exists but cannot import `researchops.cli.main`, and the command runs but `scan` is not listed in help.

### Brutal 3 - Keep a new option thin
Design a `--names-only` option for `scan` on paper. State what belongs in the CLI handler, what should remain in `find_pdfs()`, what tests you would add, and what exit codes should remain unchanged.


---

## Mini project task
Complete this capstone write-up after finishing the chapter.

### Prompt 1 - Explain the current ResearchOps CLI to a new teammate
Your explanation must include:
- what `researchops` is,
- what `scan` does,
- what `--recursive` changes,
- what happens on an invalid directory,
- how the command becomes installable,
- how the tests prove it works.

### Prompt 2 - Draw the execution path
Draw or describe this flow in text:

```text
shell command -> entry point -> Typer app -> command function -> helper logic -> Rich output -> exit code
```

### Prompt 3 - Defend the thin-handler rule
Write a short argument for why the CLI should not directly own scanning, parsing, storage, and business rules.
Use maintainability, testing, and reuse in your answer.

---

## Section 16 - Oral exam prompts
Use these for solo speaking practice or pair review.

1. Walk through `researchops scan ./papers` from shell to output.
2. Explain `@app.callback()` as if teaching a classmate.
3. Explain why entry points live in `pyproject.toml` instead of inside the shell.
4. Explain why `result.exit_code` matters in tests.
5. Explain what happens if the entry point module path is wrong.
6. Explain why optional dependency groups are not just an optimization but a design choice.
7. Explain why Rich helps users trust output.
8. Explain why Month 1 ends with packaging, not just more Python syntax.

---

## Completion checklist
Do not leave the week until you can answer these from memory.

1. What exact string installs the `researchops` command?
2. What exact object does the entry point load?
3. Which decorator makes a function a command?
4. Which decorator defines global behavior before commands run?
5. Which helper class lets Typer tests run in-process?
6. What exit code should a normal success return?
7. What exit code should an invalid directory return?
8. What principle keeps CLI files small and maintainable?

### Final written summary
Write 8-12 sentences answering this question:

> How did Week 4 turn ResearchOps from a Python project into a usable tool?

Your answer should connect interface design, packaging, testing, and architecture.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 04 — CLI and Packaging:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
