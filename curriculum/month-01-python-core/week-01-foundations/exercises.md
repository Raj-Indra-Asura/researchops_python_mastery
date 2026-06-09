# Exercises - Week 01 Foundations

## How to use this workbook

This workbook is not a checklist to rush through.
It is a practice sequence.
Each section trains a different professional skill:

- **warm-ups** build fluency
- **code reading** builds understanding
- **implementation** builds construction skill
- **testing** builds confidence
- **debugging** builds resilience
- **refactoring** builds judgment
- **writing** builds clarity

Use the workbook in order the first time.
If you get stuck, do not skip immediately.
Instead:

1. restate the task in your own words
2. identify the exact file involved
3. predict the behavior before you run anything
4. test the smallest possible thing
5. write down what surprised you

Keep a notebook or plain text file nearby.
You should be producing explanations, not just code.

---

## Warm-up exercises

These are intentionally small.
Do them without opening the internet if possible.
The goal is to reactivate your Python basics.

### Warm-up 1 — Titles and slugs

Write a function:

```python
def slugify_title(title: str) -> str:
    ...
```

Requirements:

- lowercase the string
- strip leading and trailing whitespace
- replace spaces with hyphens
- do not worry about punctuation yet

Questions to answer after writing it:

- What type goes in?
- What type comes out?
- Why is returning better than printing?

### Warm-up 2 — Count unique paper titles

Given:

```python
titles = ["Attention Is All You Need", "BERT", "BERT", "GPT"]
```

Return the number of unique titles.

Then explain:

- why a `set` helps
- what information is lost when converting to a set

### Warm-up 3 — Build one paper record

Create a dictionary representing one paper:

- title
- authors
- year
- source_file

Then answer:

- Why is a dictionary a reasonable Week 1 choice?
- Why will the project eventually need richer models than raw dictionaries?

### Warm-up 4 — Path objects

Create three `Path` objects:

- the repository root
- a `papers/` directory inside it
- a `sample.pdf` file inside `papers/`

Then print:

- the full path
- the filename
- the suffix
- the parent directory

### Warm-up 5 — Function boundaries

Take a problem like “find all `.pdf` files in a directory.”
Write down:

- what inputs the function needs
- what outputs it should return
- which errors it might raise
- what it should **not** do

### Warm-up 6 — Terminal vocabulary

Without running anything yet, define these in one sentence each:

- repository
- package
- module
- virtual environment
- editable install
- CLI
- test
- traceback

If you cannot define at least five cleanly, revisit `notes.md` first.

---

## Code-reading exercises

Read the actual project code.
Do not modify it yet.
Your job is to learn to read structure, not just write syntax.

### Code-reading 1 — `pyproject.toml`

Open `pyproject.toml` and answer:

1. What is the project name?
2. What Python version is required?
3. Which dependencies are installed by default?
4. Which dependencies are installed only for development?
5. What shell command is created by `[project.scripts]`?
6. Where does pytest look for tests?
7. Why does pytest add `src` to `pythonpath`?
8. What tool is configured under `[tool.ruff]`?
9. What tool is configured under `[tool.mypy]`?
10. Which build backend is used?

### Code-reading 2 — `src/researchops/cli/main.py`

Read the file slowly and answer:

1. What object represents the CLI application?
2. Why is `Console()` created near the top?
3. What does `@app.callback()` do?
4. What is the job of the `verbose` option?
5. Where does the `scan` command turn a string into a `Path`?
6. Which function does `scan` delegate file discovery to?
7. How does the command handle invalid directories?
8. Why is `typer.Exit(1)` used for an error?
9. Why is `typer.Exit(0)` used when no PDFs are found?
10. Which part of the file is business logic and which part is wiring?

### Code-reading 3 — `src/researchops/utils/paths.py`

Answer:

1. Why does `find_pdfs()` accept a `Path` instead of a string?
2. What happens if the path does not exist?
3. What happens if the path is a file, not a directory?
4. What does `"**/*.pdf"` mean?
5. Why is the result sorted?
6. Why does the function log a debug message?
7. What does `ensure_dir()` guarantee?
8. Why might `safe_resolve()` catch `OSError`?

### Code-reading 4 — `tests/unit/test_paths.py`

For each test, write:

- the behavior under test
- the setup
- the action
- the assertion

Then answer:

- Which tests check happy paths?
- Which tests check failures?
- Which test proves recursion matters?
- Which test proves the function ignores non-PDF files?

### Code-reading 5 — `tests/e2e/test_cli.py`

Answer:

1. Why does this file use `CliRunner` instead of calling `scan()` directly?
2. What is the difference between these tests and the unit tests?
3. How does `tmp_path` help make the tests safe and isolated?
4. Which tests protect the CLI help text?
5. Which tests protect recursive behavior?

---

## Implementation exercises

These exercises mirror the actual project.
If you are following the course from scratch, implement them yourself before comparing with the repository.

### Implementation 1 — Build the package skeleton

Create a minimal package structure:

```text
src/
└── researchops/
    ├── __init__.py
    ├── cli/
    │   └── main.py
    └── utils/
        └── paths.py
```

Requirements:

- `researchops` must be importable
- the package must live under `src/`
- imports must use the package name, not relative filesystem hacks

### Implementation 2 — Add project metadata

Write the minimum `pyproject.toml` sections needed for:

- build system
- project name and version
- Python requirement
- core dependencies
- CLI entry point
- pytest configuration

Then explain what breaks if `[project.scripts]` is missing.

### Implementation 3 — Create the Typer app

In `src/researchops/cli/main.py`:

- create a Typer app called `app`
- give it a helpful name and description
- add a top-level callback with a `--verbose` option
- make sure the file can be run directly with `if __name__ == "__main__":`

### Implementation 4 — Create `find_pdfs()`

Write:

```python
def find_pdfs(directory: Path, recursive: bool = False) -> list[Path]:
    ...
```

Rules:

- raise `NotADirectoryError` if the path does not exist
- raise `NotADirectoryError` if the path is not a directory
- search only `*.pdf` by default
- search `**/*.pdf` if `recursive=True`
- return a sorted list

### Implementation 5 — Create the `scan` command

The command should:

- accept a directory argument
- accept `--recursive` / `-r`
- call `find_pdfs()`
- handle invalid input gracefully
- print a table of PDFs when files exist
- print a friendly message when no PDFs exist

### Implementation 6 — Add small path helpers

Create:

- `ensure_dir(path: Path) -> Path`
- `safe_resolve(path: Path) -> Path`

Then explain why these helpers belong in `utils/paths.py` instead of inside the CLI file.

---

## Testing exercises

### Testing 1 — Sort order

Write a unit test that creates:

- `b.pdf`
- `a.pdf`

Then assert that `find_pdfs()` returns `a.pdf` before `b.pdf`.

Question:
Why is deterministic ordering important for tests and for user-facing output?

### Testing 2 — Ignore non-PDF files

Write a test that places these files in a temp directory:

- `paper.pdf`
- `notes.txt`
- `image.png`

Assert that only the PDF appears in the result.

### Testing 3 — Empty directory

Write a test proving that an empty directory returns `[]`.

Then explain why returning an empty list is often better than returning `None`.

### Testing 4 — Missing directory

Write a test that calls `find_pdfs()` on a path that does not exist.
Assert that `NotADirectoryError` is raised.

Then write one sentence explaining why raising an exception is better than silently returning `[]` for this case.

### Testing 5 — File instead of directory

Create a normal file.
Pass it to `find_pdfs()`.
Assert that `NotADirectoryError` is raised.

### Testing 6 — Recursive behavior

Create:

- `top.pdf`
- `sub/nested.pdf`

Then verify:

- non-recursive scan finds only `top.pdf`
- recursive scan finds both files

### Testing 7 — CLI help

Use `CliRunner` to assert:

- `--help` exits with code `0`
- the help output includes `scan`

### Testing 8 — CLI scan output

Use `CliRunner` to assert that:

- a PDF filename appears in output when present
- non-PDF files do not appear
- recursive mode shows nested PDFs
- nonexistent directories return a non-zero exit code

---

## Debugging exercises

These are designed for deliberate practice.
Do not fix them instantly.
First predict the failure.

### Debugging 1 — Wrong entry point

Change the script target in `pyproject.toml` from:

```toml
researchops = "researchops.cli.main:app"
```

to something incorrect.

Then answer:

- What command fails?
- What error message appears?
- Why is this a packaging problem, not a logic problem?

### Debugging 2 — Return `None`

Change `find_pdfs()` so it returns `None` for an empty directory.
Run the tests.
Record:

- which tests fail
- what type mismatch is revealed
- why the original `list[Path]` return type was clearer

### Debugging 3 — Remove sorting

Delete `sorted(...)` from `find_pdfs()`.
Run tests multiple times if needed.
Answer:

- Why might this create flaky output?
- Why do predictable outputs matter in CLIs?

### Debugging 4 — Catch too much

Wrap the whole body of `scan()` in a giant `try/except Exception` block.
Print a vague message like `Something went wrong`.
Then explain why this is worse debugging behavior than the current targeted exception handling.

### Debugging 5 — Use `print()` inside the utility

Move CLI-style printing into `find_pdfs()`.
Then answer:

- What becomes harder to test?
- What architectural boundary gets blurred?
- Why is returning values cleaner?

---

## Refactoring exercises

### Refactoring 1 — Separate wiring from logic

Look at `scan()`.
Identify which lines are:

- CLI input parsing
- business-ish orchestration
- rendering/output
- error handling

Write a short note on how the command could become even thinner in future weeks when service classes are introduced.

### Refactoring 2 — Improve naming

Review these names and decide whether they are clear enough:

- `app`
- `console`
- `path`
- `pdfs`
- `recursive`

For each one:

- keep it if it is already good
- or propose a better name and justify it

### Refactoring 3 — Reduce responsibility creep

Imagine `find_pdfs()` starts doing all of these:

- finding files
- printing output
- reading metadata
- storing results in a database

Refactor the imagined design on paper.
Which responsibilities belong in separate layers?

### Refactoring 4 — Pathlib migration thought experiment

Suppose the code had used `os.path` everywhere instead of `pathlib`.
List three things that would become less readable.
Then rewrite one small example using `Path`.

---

## Written explanation exercises

Write short answers in full sentences.
No bullet fragments.

1. What is the difference between a repository and a Python package?
2. Why does this project place code under `src/researchops/`?
3. What problem does a virtual environment solve?
4. What does editable install mean in practice?
5. Why is a CLI useful even for a project that may later have an API?
6. Why are tests part of the development workflow from Week 1?
7. Why is `find_pdfs()` easier to test than a function that only prints?
8. What is one reason the project uses `pathlib.Path` instead of raw strings?
9. What does pytest test discovery save you from doing manually?
10. Why is Week 1 architecture work not “just setup”?

---

## Stretch exercises

These are useful if the core work felt manageable.

### Stretch 1 — Add a `version` command

Add a CLI command that prints the package version using `importlib.metadata`.
Do not hard-code the version string in the command.

Questions:

- Where should the command live?
- How would you test it?
- Why is reading metadata better than duplicating version text?

### Stretch 2 — Case-insensitive extension matching

Right now the project looks for `*.pdf`.
Think about files like `PAPER.PDF`.

- Should those count?
- If yes, how would you implement that carefully?
- How would you test it?

### Stretch 3 — Add richer empty-state output

If no PDFs are found, improve the message.
Possible additions:

- whether the scan was recursive
- a suggestion to check the directory path
- a reminder that only `.pdf` files are counted

Then ask yourself:
Does this belong in the CLI layer or the utility layer?

### Stretch 4 — Design a future service boundary

Sketch a future `IngestionService` with no implementation.
What responsibilities would it have that `scan()` does not?

---

## Brutal exercises

These are optional.
They are meant to force deep understanding.

### Brutal 1 — Explain the whole flow from memory

Without opening the code, explain this chain aloud:

terminal command → entry point → Typer app → callback → `scan()` → `find_pdfs()` → returned `Path` objects → Rich table output

If you hesitate on any step, review the notes.

### Brutal 2 — Recreate `pyproject.toml` from a blank file

From memory, rebuild the essential parts needed to:

- install the package
- create the CLI command
- run pytest successfully

Then compare against the real file.
Mark every section you forgot.

### Brutal 3 — Write tests first

Delete your implementation of `find_pdfs()` in a scratch copy.
Now re-create the function **only** by reading the tests.
This exercise teaches how tests specify behavior.

### Brutal 4 — Find the architectural leak

Imagine a teammate adds direct file-system scanning code inside future API route handlers.
Write a critique:

- what boundary is being violated
- why it hurts maintainability
- where the logic should move instead

---

## Mini project task

Tie everything together by doing this from scratch in a fresh practice folder:

1. create a virtual environment
2. install a small package in editable mode
3. create a `src/` layout package
4. add a Typer app
5. add one file-discovery utility
6. add unit tests
7. add one CLI test
8. run the full test suite
9. explain the whole flow in writing

Your deliverable is not just code.
It is a working package plus a written explanation of why each file exists.

---

## Completion checklist

- [ ] I completed the warm-ups without blindly copying.
- [ ] I read the real project files before writing my own version.
- [ ] I can explain what `pyproject.toml` is doing.
- [ ] I wrote or mentally simulated the `find_pdfs()` implementation.
- [ ] I understand why the CLI delegates to a utility function.
- [ ] I can tell which tests are unit tests and which are CLI tests.
- [ ] I practiced at least two debugging exercises.
- [ ] I completed at least one written explanation exercise in full sentences.
- [ ] I can trace the Week 1 execution flow from terminal input to output.
- [ ] I know exactly which concepts still feel weak.
