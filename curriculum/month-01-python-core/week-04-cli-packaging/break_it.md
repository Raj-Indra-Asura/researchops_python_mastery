<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 04 — CLI and Packaging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It - Week 04 CLI and Packaging

## Why this lab exists
Stable systems are easier to understand when you have seen them fail in controlled ways.
This lab teaches you to recognize the difference between:
- a packaging failure,
- a parsing failure,
- a user-input failure,
- a testing mistake,
- a formatting issue,
- an architecture mistake.

Do these experiments in a throwaway branch or restore each change immediately after observing it.
The point is not to leave the code broken.
The point is to train your debugging instincts.

---

## Safety rules
1. Make one breakage at a time.
2. Record the exact symptom before fixing anything.
3. Restore the code after each experiment.
4. Reinstall after packaging changes.
5. Re-run tests after each repair.
6. Focus on what kind of failure it is, not only the error text.

---

## Experiment 1 - Break the entry point path
### Goal
Learn what happens when the installed shell command points to the wrong Python module or object.

### Break it
Change:

```toml
researchops = "researchops.cli.main:app"
```

To something wrong, such as:

```toml
researchops = "researchops.cli.broken:app"
```

Or:

```toml
researchops = "researchops.cli.main:typer_app"
```

### Run
```bash
python -m pip install -e ".[dev]"
researchops --help
```

### What you should observe
- The command exists at the shell level.
- Startup fails immediately.
- The error usually mentions import failure or missing attribute.

### Diagnosis
The shell script was installed, but the script points at Python code that cannot be imported correctly.
This is not a `scan` logic bug.
This is packaging metadata pointing at the wrong target.

### Repair
Restore the entry point to:

```toml
researchops = "researchops.cli.main:app"
```

Then reinstall.

### Lesson
Packaging can fail before your command logic ever runs.

---

## Experiment 2 - Forget to reinstall after changing the entry point
### Goal
See why editable installs still need reinstalling when metadata changes.

### Break it
1. Change the entry point string in `pyproject.toml`.
2. Do **not** run `pip install -e .` again.
3. Run `researchops --help`.

### What you should observe
You may still get old behavior.
The installed script can continue pointing at the previously installed metadata.

### Diagnosis
Editable installs make source-code edits visible quickly, but not every metadata change is automatically refreshed in the already-installed script.

### Repair
Reinstall the package.

### Lesson
When packaging metadata changes, reinstall first, then debug.

---

## Experiment 3 - Make a required argument accidentally optional
### Goal
Feel the difference between `typer.Argument(...)` and a defaulted argument.

### Break it
Change the command signature from:

```python
directory: str = typer.Argument(..., help="Path to a directory containing PDF files.")
```

To something like:

```python
directory: str = typer.Argument(".", help="Path to a directory containing PDF files.")
```

### Run
```bash
researchops scan
researchops scan --help
```

### What you should observe
- The command may now run without a directory argument.
- Help output will no longer show the argument as required.

### Diagnosis
The `...` sentinel means required.
A real default means optional.
You changed the interface contract, not just a convenience detail.

### Repair
Restore `...`.

### Lesson
Defaults change semantics.
In a CLI, they change how users are allowed to call the command.

---

## Experiment 4 - Print an error but forget to exit non-zero
### Goal
See why messaging and process status are separate responsibilities.

### Break it
Find the invalid-directory branch.
Keep the error print, but replace:

```python
raise typer.Exit(1)
```

With a plain `return`.

### Run
```bash
researchops scan does-not-exist
echo $?
pytest tests/e2e/test_cli.py -v -k nonexistent
```

### What you should observe
- The screen still shows an error message.
- The shell may report exit code `0`.
- The test for invalid directory should fail.

### Diagnosis
Humans saw an error.
The shell did not.
Automation only gets the exit code.

### Repair
Restore `raise typer.Exit(1)`.

### Lesson
A user-visible error is not enough.
Machine-readable failure matters too.

---

## Experiment 5 - Catch `Exception` too broadly
### Goal
Understand how broad exception handling hides real problems.

### Break it
Replace the targeted exception handling with:

```python
except Exception as exc:
    console.print(f"[red]Error:[/red] {exc}")
    raise typer.Exit(1) from exc
```

### Run
Trigger two kinds of problems:
1. an invalid directory,
2. an unrelated bug you intentionally introduce temporarily.

### What you should observe
Different failures now look deceptively similar.
The CLI may hide useful debugging information.

### Diagnosis
A user mistake and a programmer mistake are not the same category.
Broad exception handling collapses them together.

### Repair
Catch the specific exception you actually expect.

### Lesson
Be kind to users, but do not blind yourself while debugging.

---

## Experiment 6 - Misspell Rich markup
### Goal
Learn the difference between data being correct and presentation being correct.

### Break it
Change:

```python
console.print(f"[red]Error:[/red] {exc}")
```

To:

```python
console.print(f"[redd]Error:[/redd] {exc}")
```

### Run
Trigger an invalid-directory error.

### What you should observe
The message text still appears.
The styling may not.
The CLI is functionally correct but visually degraded.

### Diagnosis
Rich markup is interpreted text.
If the tag is wrong, the user experience changes even though the control flow still works.

### Repair
Restore valid markup tags such as `[red]`, `[yellow]`, and `[bold]`.

### Lesson
Presentation bugs matter because they affect clarity and trust.

---

## Experiment 7 - Test the wrong app object
### Goal
See how easy it is for a test to target the wrong interface object.

### Break it
In `tests/e2e/test_cli.py`, import the wrong thing or create a different Typer app in the test file.
For example, imagine accidentally doing this:

```python
import typer
app = typer.Typer()
```

And then testing that empty app.

### Run
```bash
pytest tests/e2e/test_cli.py -v
```

### What you should observe
- Commands you expected may be missing.
- Help output may look almost empty.
- Tests may fail in confusing ways.

### Diagnosis
The test runner is working.
Your test target is wrong.
You are not exercising the real application object.

### Repair
Import the real app:

```python
from researchops.cli.main import app
```

### Lesson
A good test can still be useless if it points at the wrong object.

---

## Experiment 8 - Assert the wrong exit code
### Goal
Train yourself to think about contracts, not wishes.

### Break it
Find the nonexistent-directory test and change the assertion to:

```python
assert result.exit_code == 0
```

### Run
```bash
pytest tests/e2e/test_cli.py -v -k nonexistent
```

### What you should observe
The test fails clearly.
The failure message reminds you what the contract really is.

### Diagnosis
The application behavior was correct.
The test expectation was wrong.

### Repair
Restore a non-zero expectation.

### Lesson
Tests are executable specifications.
If the specification is wrong, the test becomes noise.

---

## Experiment 9 - Remove the `--recursive` option but keep using it
### Goal
See how parser-level failures differ from application-level failures.

### Break it
Remove the `recursive` option from the `scan` signature.
Then run a command that still passes `--recursive`.

### Run
```bash
researchops scan examples/sample_papers --recursive
```

### What you should observe
Typer rejects the invocation before your command logic runs.
The error is about invalid command usage, not directory scanning.

### Diagnosis
This is a parsing contract failure.
The parser could not map the command line to the function signature.

### Repair
Restore the option definition.

### Lesson
Some failures happen before your function body executes.

---

## Experiment 10 - Replace a clean user-facing error with a raw exception
### Goal
Compare normal user experience with raw Python crash behavior.

### Break it
Temporarily raise a `RuntimeError` inside `scan()` or remove the targeted error handling and let the error bubble up.

### Run
```bash
researchops scan does-not-exist
```

### What you should observe
The output becomes more technical and less friendly.
Depending on the failure, you may see a traceback or lower-level message.

### Diagnosis
Internal debugging information leaked into the user experience.
That is sometimes useful while developing, but not ideal as the steady-state interface.

### Repair
Restore the clean exception-to-message mapping.

### Lesson
A polished CLI translates expected failures into calm, actionable output.

---

## Experiment 11 - Use an exact-output assertion that is too brittle
### Goal
Learn why CLI tests should usually assert important substrings, not terminal art spacing.

### Break it
Write a test that asserts the entire Rich table output exactly, including spacing and borders.

### Run
```bash
pytest tests/e2e/test_cli.py -v
```

### What you should observe
The test may become fragile across terminal formatting changes or minor output layout changes.

### Diagnosis
You tested rendering details that are not the real contract.
The important behavior is that relevant filenames, messages, and exit codes appear.

### Repair
Assert on stable substrings and exit codes.

### Lesson
Test the behavior users rely on, not every pixel-equivalent character.

---

## Experiment 12 - Put too much logic inside the CLI handler
### Goal
Feel the maintainability cost of violating the thin-handler rule.

### Break it
Move directory traversal logic directly into `scan()` and stop delegating to `find_pdfs()`.
Do not keep it that way; this is only to observe the effect.

### What you should observe
- the function gets longer,
- testing becomes more coupled,
- reuse becomes harder,
- the CLI file starts owning behavior it should only orchestrate.

### Diagnosis
The command layer is drifting into application logic.
That makes future API reuse and service extraction harder.

### Repair
Move reusable work back into a helper or service.
Keep the CLI focused on input, output, and orchestration.

### Lesson
The architecture rule is not ceremony.
It protects growth.

---

## Pattern recognition checklist
After finishing the lab, make sure you can identify these failure categories on sight.

- **Packaging failure**: installed command cannot import the configured target.
- **Metadata refresh failure**: you changed config but forgot to reinstall.
- **Parser failure**: Typer rejects the command line before your function runs.
- **User-input failure**: command runs, validates input, and exits non-zero cleanly.
- **Programmer bug**: unexpected exception or broken logic.
- **Test-target failure**: the test is not invoking the real app.
- **Assertion failure**: behavior is correct but the test expectation is wrong.
- **Presentation failure**: output styling or layout is wrong while core logic still works.

---

## Debrief prompts
Write a short paragraph for each.

1. Which breakage felt most confusing at first, and why?
2. Which breakage was a packaging problem rather than a code problem?
3. Which breakage proved that exit codes are part of the feature?
4. Which breakage taught you the most about test design?
5. Which breakage showed why the CLI should stay thin?
6. If a teammate says "the command is broken," what questions would you now ask first?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 04 — CLI and Packaging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
