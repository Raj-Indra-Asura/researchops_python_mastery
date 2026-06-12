<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 02 — Files, Errors, Logging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It — Failure Lab for Chapter 2
## Purpose of failure practice
Failure practice teaches you to recognize broken filesystem, exception, and logging behavior before those failures appear in a real ResearchOps run. A beginner often sees an error message and immediately guesses; this lab trains you to inspect the path, exception type, exit code, and test that describes the intended behavior. Treat each break as a controlled experiment, not as vandalism.

This lab is where you stop treating failures as surprises.
Each experiment asks you to predict behavior, cause a controlled failure, inspect the result, and explain what the code is teaching you.
Do not skip the prediction step.
Good debugging starts before the command runs.

---

## Failure lab rules
- Work in a disposable branch or revert your changes after each experiment.
- Break one thing at a time.
- Record the exact command you ran.
- Record the exact error message or log output you saw.
- End each experiment by restoring the original code.

---

## Intentional break experiments
Each experiment below follows the same pattern: cause one small break, observe the expected error, inspect the exact line involved, fix the break, identify the test that should catch it, and write down the lesson. Do not combine multiple experiments, because combined failures teach confusion instead of diagnosis.

## Experiment 1 — Delete the directory and trigger `NotADirectoryError`
### Goal
See how the scanner behaves when the target path does not exist.

### Predict
Before running anything, write down what you expect:
- exception type,
- user-facing CLI message,
- and exit behavior.

### Break it
Run:

```bash
researchops scan examples/does_not_exist
```

### Observe
Capture the message exactly.
Then answer:
- Did the CLI show a traceback or a clean message?
- Where did the message text come from?
- Which layer decided the exit code?

### Repair
No code change is needed.
Your repair step is conceptual: explain why this is not treated as “0 PDFs found.”

### Lesson
A missing directory is invalid input, not an empty scan result.

---

## Experiment 2 — Pass a file instead of a directory
### Goal
See why `is_dir()` matters separately from `exists()`.

### Predict
If the path exists but points to a file, what should happen?
Would returning an empty list be acceptable here?
Why or why not?

### Break it
Run Python interactively:

```python
from pathlib import Path
from researchops.utils.paths import find_pdfs
find_pdfs(Path("examples/sample_papers/README.md"))
```

### Observe
Record the exception type and message.
Then answer:
- Why is this a different failure from a missing path?
- Why does the code still use the same built-in exception type?

### Repair
Restore your shell state and explain why both checks belong in the function.

### Lesson
Existence and type are different questions.
Production code must ask both.

---

## Experiment 3 — Remove the `.exists()` check and inspect `glob()` behavior
### Goal
Discover why explicit validation is better than relying on later behavior.

### Predict
If you delete this block from `find_pdfs()`:

```python
if not directory.exists():
    raise NotADirectoryError(f"Directory does not exist: {directory}")
```

what do you think `directory.glob("*.pdf")` will do for a missing path?
Will it raise?
Will it return `[]`?
Will the failure become harder to understand?

### Break it
Temporarily remove only the existence check.
Run the relevant path tests.
Then manually call `find_pdfs()` on a missing directory.

### Observe
Write down what changed.
Which guarantee became weaker?
Which test now protects that guarantee more clearly?

### Repair
Put the check back exactly as it was.

### Lesson
Early validation creates clearer contracts than accidental downstream behavior.

---

## Experiment 4 — Raise the wrong exception type
### Goal
See how exception choice affects meaning.

### Predict
If `find_pdfs()` raises `ValueError` instead of `NotADirectoryError`, what becomes worse?
Think about the CLI, tests, and future callers.

### Break it
Temporarily change one of the `raise NotADirectoryError(...)` lines to `raise ValueError(...)`.
Run the path tests.
Then run the CLI manually on a bad directory.

### Observe
Answer:
- Which tests fail?
- Does the CLI still catch the failure cleanly?
- What does this teach you about catching specific exceptions?

### Repair
Restore `NotADirectoryError`.

### Lesson
Exception types are part of the public contract, not just decoration.

---

## Experiment 5 — Catch too broadly with `except Exception`
### Goal
See how broad catches hide real bugs.

### Predict
What kinds of mistakes could broad exception handling hide?
Consider `AttributeError`, `TypeError`, and programming mistakes.

### Break it
Temporarily rewrite the CLI handling like this:

```python
try:
    pdfs = find_pdfs(path, recursive=recursive)
except Exception as exc:
    console.print(f"[red]Error:[/red] {exc}")
    raise typer.Exit(1) from exc
```

Then deliberately introduce a bug inside `find_pdfs()`, such as misspelling `directory.glob` as `directory.glbo`.
Run the CLI.

### Observe
Did the CLI make a programmer bug look like ordinary user input failure?
Why is that dangerous during development?

### Repair
Restore the narrow `except NotADirectoryError` block and fix the typo.

### Lesson
Catch only what you can truly classify and handle.

---

## Experiment 6 — Use a string path where a `Path` is expected
### Goal
Feel the difference between API expectations and lucky accidents.

### Predict
If you call `find_pdfs("examples/sample_papers")` directly, what do you think will happen?
What attribute access will fail first?

### Break it
In a Python shell, run:

```python
from researchops.utils.paths import find_pdfs
find_pdfs("examples/sample_papers")
```

### Observe
Record the exception type.
Then answer:
- Why does the function signature matter?
- Why is it helpful that the failure is loud instead of quietly coercing types?

### Repair
Call the function correctly with `Path(...)`.

### Lesson
A clear type contract keeps bugs close to their source.

---

## Experiment 7 — Forget `encoding="utf-8"`
### Goal
Learn why explicit encodings belong in serious code.

### Predict
What happens when text is read using the platform default encoding and the file contains characters that do not fit?
Do you expect consistent behavior across machines?

### Break it
Create or use a text file containing non-ASCII characters.
Try reading it without specifying an encoding.
Then try again with the wrong encoding.
Finally try with `encoding="utf-8"`.

Example shell session:

```python
from pathlib import Path
p = Path("examples/sample_papers/README.md")
p.read_text()
p.read_text(encoding="latin-1")
p.read_text(encoding="utf-8")
```

### Observe
If your platform default does not fail, explain why that still does **not** prove the code is portable.
If you do get a `UnicodeDecodeError`, copy the important part of the traceback.

### Repair
Return to explicit UTF-8 in every educational example you write.

### Lesson
Code that “works on my machine” is not enough for data pipelines.

---

## Experiment 8 — Replace `log.debug()` with `print()`
### Goal
See what logging gives you that printing does not.

### Predict
What will you lose if you swap structured logging for `print()` inside `find_pdfs()`?
Think about verbosity control, test capture, and output cleanliness.

### Break it
Temporarily replace:

```python
log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
```

with:

```python
print(f"Found {len(pdfs)} PDF(s) in {directory}")
```

Run the CLI normally and with `--verbose`.
Then run the path tests.

### Observe
Answer:
- Does the message appear even when debug mode is off?
- Is the output mixed awkwardly with Rich console output?
- Would a logging capture fixture see this the same way?

### Repair
Restore `log.debug(...)`.

### Lesson
Logging is controllable instrumentation.
Printing is uncontrolled console output.

---

## Experiment 9 — Compare `glob()` and recursive scanning directly
### Goal
Make recursion concrete.

### Predict
How many files should be found by each pattern in a nested folder tree?

### Break it
Create a small nested directory tree.
Then run both of these in Python:

```python
from pathlib import Path
root = Path("your_test_directory")
list(root.glob("*.pdf"))
list(root.glob("**/*.pdf"))
```

### Observe
Which files disappear in the non-recursive case?
Why is that behavior desirable sometimes?

### Repair
No code repair is needed.
The repair is conceptual: write one rule for when to choose each style.

### Lesson
Recursive search is useful, but it should be explicit.

---

## Experiment 10 — Remove sorting and watch determinism weaken
### Goal
See why stable ordering matters.

### Predict
If you remove `sorted(...)`, will the result order always stay the same?
Should tests depend on filesystem ordering?

### Break it
Temporarily change:

```python
pdfs = sorted(directory.glob(pattern))
```

to:

```python
pdfs = list(directory.glob(pattern))
```

Run the path tests.
If they still pass on your machine, think beyond your machine.
Would this be reliable across platforms and filesystems?

### Observe
Write a short paragraph about determinism.
Include why predictable ordering matters for tests, logs, and user trust.

### Repair
Restore sorting.

### Lesson
Stable output is a feature, not a cosmetic choice.

---

## Experiment 7 — Remove the `exist_ok=True` flag from `ensure_dir()`

### Scenario
`ensure_dir()` creates a directory and all missing parents.
It also accepts paths that already exist.
The `exist_ok=True` flag is what makes repeated calls safe.

### How to cause it
Edit `ensure_dir()` so it calls:
```python
path.mkdir(parents=True)
```
instead of:
```python
path.mkdir(parents=True, exist_ok=True)
```

Then call `ensure_dir()` on a path that already exists:
```python
from pathlib import Path
from researchops.utils.paths import ensure_dir
ensure_dir(Path("tests"))
```

### Expected failure or symptom
Python raises `FileExistsError` because `mkdir` refuses to create a directory that already exists when `exist_ok=False`.

### How to inspect the failure
Read the error message. It will name the path that already existed.
Ask yourself: how often will callers of `ensure_dir()` know in advance whether the directory exists?
Answer: almost never. That is why idempotency matters.

### How to fix it
Restore `exist_ok=True`.
Then rerun the idempotency test:
```bash
pytest tests/unit/test_paths.py::TestEnsureDir -v
```

### Test that catches it
- `test_existing_directory_is_idempotent`

### Lesson
A utility function that fails on repeated calls is not a utility.
It is a source of unpredictable failures in callers that cannot know whether the path already exists.

---

## Experiment 8 — Add `print()` inside `find_pdfs()`

### Scenario
Beginners sometimes put `print()` statements inside utility functions to "see what is happening."
That habit seems harmless at first.
It has real architectural consequences.

### How to cause it
Edit `find_pdfs()` so it prints each PDF path:
```python
for pdf in pdfs:
    print(pdf)
return pdfs
```

Then run the unit tests:
```bash
pytest tests/unit/test_paths.py -v -s
```

### Expected symptom
The tests still pass, but output now appears unexpectedly during test runs.
The utility has grown a side effect that tests cannot easily control.

### Think about the implications
- What happens when this utility is called from a background worker that redirects stdout?
- What happens when a service calls `find_pdfs()` and wants to log the results in a structured format instead of printing?
- What happens when a test wants to assert that no console output was produced?

### How to fix it
Remove the `print()` calls.
Use `log.debug(...)` instead if you need visibility into function behavior.
Let the CLI layer handle presentation.

### Lesson
Adding `print()` to a utility function adds a hidden dependency on standard output.
That makes the function harder to reuse, test, and audit.
A logger call at the right level is almost always better.

---

## Experiment 9 — Force UTF-8 encoding failures

### Scenario
When reading or writing text files, omitting the encoding argument lets Python guess.
That guess is right on some machines and wrong on others.

### How to cause it
If the project has any file-reading logic, temporarily change:
```python
path.read_text(encoding="utf-8")
```
to:
```python
path.read_text()
```

Then observe whether the behavior changes in a different locale or on a Windows machine with `cp1252` as the default.

### Why this matters without requiring a different machine
Even on a single machine, the default encoding depends on the system locale.
A developer who writes tests on a Mac with UTF-8 and deploys to a Windows server may encounter `UnicodeDecodeError` only in production.

### Expected failure or symptom
On a machine with a non-UTF-8 default encoding, `read_text()` without encoding may raise `UnicodeDecodeError` for files containing accented characters, curly quotes, or other non-ASCII text.

### How to inspect the failure
Temporarily create a file that contains a character like `ñ` or `—` (em dash).
Read it both ways and compare.

### How to fix it
Always specify `encoding="utf-8"` explicitly.

### Lesson
Implicit encoding relies on platform defaults that developers cannot control.
Explicit encoding is a one-word portability guarantee.

---

## Experiment 10 — Make a custom exception inherit from the wrong base

### Scenario
Exception hierarchy placement is a design decision.
If an exception inherits from the wrong base class, callers may catch it incorrectly or miss it entirely.

### How to cause it
Temporarily edit one exception to change its parent.
For example, change:
```python
class EmptyDocumentError(ParsingError):
    ...
```
to:
```python
class EmptyDocumentError(StorageError):
    ...
```

### Expected failure or symptom
Code that catches `ParsingError` to handle document parsing issues will no longer catch `EmptyDocumentError`.
Code that catches `StorageError` will start catching `EmptyDocumentError` unexpectedly.
The exception hierarchy test should fail.

### How to inspect the failure
Run the exception hierarchy tests:
```bash
pytest tests/unit/test_exceptions.py -v
```

Read which assertion failed.
Then ask: which business rule was this exception supposed to express?
Is "empty document" a parsing failure or a storage failure?

### How to fix it
Restore the correct parent class.

### Lesson
Exception type is part of the API contract.
Bad hierarchy placement creates silent confusion for callers.

---

## Debugging checklist
- Did you reproduce the failure with one command?
- Did you identify whether the symptom came from `Path`, an exception class, logging, or Typer exit behavior?
- Did you read the failing test before changing code?
- Did you undo the intentional break before moving on?
- Did you rerun the smallest relevant test before running the full suite?

---

## Reflection after breaking
After all experiments, answer these in writing:

1. Which failure taught you the most about API contracts?
2. Which failure showed the biggest difference between user-facing output and developer-facing diagnostics?
3. Which experiment changed your opinion about `except Exception` the most?
4. Which logging behavior do you now consider essential for production code?
5. Which guarantee from the tests feels most important to preserve as the project grows?
6. Which experiment surprised you most, and why?
7. Which failure would be the hardest to debug in a codebase you had never seen before?
8. Which design rule from this lab do you now feel was earned rather than arbitrary?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 02 — Files, Errors, Logging:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
