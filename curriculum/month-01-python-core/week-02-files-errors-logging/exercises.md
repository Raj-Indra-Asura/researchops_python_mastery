# Exercises — Chapter 2 Workbook

## How to use this workbook
This workbook is designed to be done with the codebase open beside you.
Do not rush to type first.
Read, predict, then verify.
If an exercise asks for code, write it in a scratch Python shell, a temporary branch, or on paper before comparing with the repository.
The goal is not just to finish tasks.
The goal is to build reliable instincts.

---

## Section 1 — Recall from Week 1
### Exercise 1.1 — Startup story
In 5 to 7 sentences, describe what happened in Week 1 when a user ran the `scan` command.
Focus on environment setup, imports, CLI entry points, and basic function flow.
Then add one sentence describing what Week 1 did **not** yet solve.

### Exercise 1.2 — Command memory check
Without looking at the code, write the command you would use to:
1. install the project in editable mode with dev tools,
2. run only the path tests,
3. run the scanner on `examples/sample_papers`,
4. and run the scanner with verbose logging.
Then check yourself against `validation.md`.

### Exercise 1.3 — Architecture recall
Answer in complete sentences:
- Why should `core/` avoid importing from `cli/` or `storage/`?
- Why should the CLI delegate work instead of owning business logic?
- Why does this matter even in a small project?

---

## Section 2 — `pathlib` warm-up
### Exercise 2.1 — Read a path like data
Open a Python shell.
Create this object:

```python
from pathlib import Path
p = Path("examples/sample_papers/README.md")
```

Now answer:
- What is `p.name`?
- What is `p.stem`?
- What is `p.suffix`?
- What is `p.parent`?
- Is `p.exists()` true?
- Is `p.is_file()` true?
- Is `p.is_dir()` true?

Write the answers before you run anything.
Prediction first is part of the training.

### Exercise 2.2 — Build paths without string concatenation
Rewrite these string-based ideas using `Path` objects:

1. `"examples" + "/" + "sample_papers"`
2. `root + "/paper.pdf"`
3. `"data/cache/results"`

After rewriting them, explain in one sentence why the `Path` version is more robust.

### Exercise 2.3 — Relative vs absolute
Create a `Path("examples/sample_papers")`.
Then call `.absolute()` and `.resolve()` on it.
Record the difference you observe.
If you do not see a visible difference on your machine, explain what *conceptual* difference still exists.

### Exercise 2.4 — Directory creation
Look at `ensure_dir()` in `src/researchops/utils/paths.py`.
Answer these questions:
- Why does it call `mkdir(parents=True, exist_ok=True)`?
- What would break if `parents=True` were removed?
- What would break if `exist_ok=True` were removed?
- Why does the function return the path instead of `None`?

---

## Section 3 — Glob and recursive scanning
### Exercise 3.1 — Pattern translation
Translate each pattern into plain English:
- `*.pdf`
- `**/*.pdf`
- `*.txt`
- `reports/**/*.json`

Then write one example path that would match and one that would not.

### Exercise 3.2 — Predict before you scan
Suppose a directory contains:

```text
papers/
├── a.pdf
├── b.pdf
├── notes.txt
└── nested/
    └── c.pdf
```

Predict the result of:

```python
find_pdfs(Path("papers"), recursive=False)
find_pdfs(Path("papers"), recursive=True)
```

Write the returned filenames in order.
Then explain why sorted output matters in tests.

### Exercise 3.3 — `glob()` vs `rglob()`
Answer in your own words:
- What does `Path.glob()` do?
- What does `Path.rglob()` do?
- Why does the current implementation use `glob(pattern)` for both cases instead of switching methods?
- What does that choice say about API design?

### Exercise 3.4 — Case sensitivity thought experiment
On Linux, will `*.pdf` match `PAPER.PDF`?
On a case-insensitive filesystem, what might happen instead?
Why is this important when writing portable software?

---

## Section 4 — Reading the real code
### Exercise 4.1 — Trace `find_pdfs()`
Read `src/researchops/utils/paths.py` line by line.
For each line in `find_pdfs()`, fill in this table in your notebook:

| Line purpose | What assumption does it check? | What guarantee does it create? |
|---|---|---|
| `if not directory.exists():` | ? | ? |
| `if not directory.is_dir():` | ? | ? |
| `pattern = ...` | ? | ? |
| `pdfs = sorted(...)` | ? | ? |
| `log.debug(...)` | ? | ? |
| `return pdfs` | ? | ? |

### Exercise 4.2 — Explain the function to a beginner
Pretend your classmate has never seen `find_pdfs()` before.
Explain the function in exactly six sentences.
You must mention:
- input type,
- validation,
- pattern choice,
- sorting,
- logging,
- and return value.

### Exercise 4.3 — Read for hidden decisions
Answer these questions:
- Why does the function raise `NotADirectoryError` instead of returning an empty list?
- Why is the error raised before calling `glob()`?
- Why is the list sorted even though filesystem iteration already returns something?
- Why is the log level `DEBUG` and not `INFO`?

---

## Section 5 — Exceptions and error design
### Exercise 5.1 — Draw the hierarchy
Read `src/researchops/core/exceptions.py`.
Draw a tree showing inheritance relationships.
At minimum include:
- `ResearchOpsError`
- `ParsingError`
- `StorageError`
- `SearchError`
- `ConfigurationError`
- `MLError`
- `JobError`
- and the concrete child exceptions.

### Exercise 5.2 — Message anatomy
For each of the following exceptions, write down:
1. the human-facing message,
2. the metadata stored on `self`,
3. and the practical reason that metadata is useful.

Use:
- `EmptyDocumentError`
- `UnsupportedFileTypeError`
- `PaperNotFoundError`
- `DuplicatePaperError`
- `ModelNotTrainedError`
- `JobNotFoundError`

### Exercise 5.3 — Built-in or custom?
For each scenario, choose the best fit and justify your choice:
- A path argument points to a file, but the function requires a directory.
- The user submits an empty search query.
- A PDF parser extracted zero text.
- A config file is missing required settings.
- A database lookup cannot find the requested paper.

### Exercise 5.4 — Constructor reasoning
Why do some exception classes define `__init__`, while others only use a docstring and `pass` through inheritance?
What determines whether a custom constructor is necessary?

---

## Section 6 — `try` / `except` / `else` / `finally`
### Exercise 6.1 — Clause matching
Match each clause to its job:
- `try`
- `except`
- `else`
- `finally`

Jobs:
- runs only if no exception happened,
- runs whether success or failure happened,
- contains the operation that might fail,
- handles a named failure type.

### Exercise 6.2 — Explain the scan command flow
Read the `scan()` function in `src/researchops/cli/main.py`.
Describe the control flow from `directory: str` to `typer.Exit(1)`.
Your answer must explain:
- where string input becomes a `Path`,
- where failure is converted into user output,
- and why the CLI does not silently swallow the error.

### Exercise 6.3 — Narrow catch practice
Rewrite these broad handlers into narrower ones:

```python
try:
    pdfs = find_pdfs(path)
except Exception:
    print("failed")
```

```python
try:
    text = path.read_text()
except Exception as exc:
    log.error("bad file: %s", exc)
```

For each rewrite, explain what bug could be hidden by `except Exception`.

### Exercise 6.4 — Chaining practice
Write a small example that catches `OSError` while reading a text file and raises `ConfigurationError` with the original exception chained underneath using `raise ... from ...`.
Then write two sentences explaining why chaining is better than throwing away the original cause.

---

## Section 7 — Logging practice
### Exercise 7.1 — Level selection
Choose the best log level for each event:
- scan started,
- found 12 PDFs,
- skipping a `.docx` file,
- failed to open a file,
- internal count of how many directories were visited,
- application cannot start because configuration is invalid.

Then justify each choice.

### Exercise 7.2 — `print()` vs logging
Write two versions of a message that reports a skipped file.
First use `print()`.
Then use `log.warning()`.
Now compare them using these questions:
- Which version can be filtered by level?
- Which version includes module context?
- Which version integrates with test capture tools?
- Which version belongs in production code?

### Exercise 7.3 — Message formatting
Convert these log calls to the preferred style:

```python
log.info(f"Found {count} PDF(s) in {directory}")
log.error(f"Failed to read {path}: {exc}")
```

Then explain why the `%s` style is preferred inside logging calls.

### Exercise 7.4 — Read the config
Open `src/researchops/config/logging.py`.
Answer:
- What is the root logger?
- What is a handler?
- What is the format string doing?
- Why is `force=True` used?
- Why are `httpx`, `httpcore`, and `urllib3` set to `WARNING`?

---

## Section 8 — Tests as specifications
### Exercise 8.1 — What does each path test prove?
Read every test in `tests/unit/test_paths.py`.
For each test, complete this sentence:

> “This test protects the guarantee that ...”

Examples of guarantees include sorting, filtering, idempotency, and correct failure signals.

### Exercise 8.2 — Test vocabulary
Define these testing ideas in your own words:
- fixture,
- `tmp_path`,
- assertion,
- idempotent,
- edge case.

### Exercise 8.3 — Exception tests
Read `tests/unit/test_exceptions.py`.
Why do those tests check both `str(exc)` and `exc.path` or `exc.paper_id`?
Why is checking only one of those not enough?

### Exercise 8.4 — Predict failures
If the `sorted(...)` call were removed from `find_pdfs()`, which test would fail first?
If the `.exists()` check were removed, which behavior would become ambiguous?
Write your predictions before changing anything.

---

## Section 9 — Manual CLI lab
### Exercise 9.1 — Happy path smoke check
Run:

```bash
researchops scan examples/sample_papers
```

Record exactly what appears.
If no PDFs exist, record the “no files found” message.
If you add PDFs locally, record the table output.
Then explain how the command communicates success without parsing the files themselves.

### Exercise 9.2 — Verbose mode
Run:

```bash
researchops --verbose scan examples/sample_papers
```

Identify which extra lines come from logging and which output comes from Rich console rendering.
Why is that distinction useful?

### Exercise 9.3 — Bad input path
Run the scanner on a clearly missing directory.
Write down:
- the exit code,
- the message shown to the user,
- and the exception type caught by the CLI.

Then answer this question:
Why is this a better user experience than a raw traceback?

---

## Section 10 — Short written answers
Write 4 to 6 sentences for each prompt.

1. Why is “return an empty list on every failure” a bad design for a scanner?
2. Why is a shared base exception valuable in a growing application?
3. Why should logs contain context such as paths and counts?
4. What is the difference between user-facing output and developer-facing diagnostics?
5. Why do deterministic tests matter for file discovery code?

---

## Section 11 — Explain-it-aloud drills
Speak these answers out loud, without reading the code.
If you cannot explain one clearly, review that section.

1. Explain `Path` to someone who only knows strings.
2. Explain why `find_pdfs()` checks `exists()` before `is_dir()`.
3. Explain the difference between `NotADirectoryError` and `UnsupportedFileTypeError`.
4. Explain why logging belongs in startup and long-running workflows.
5. Explain why tests use `tmp_path` instead of hard-coded directories.

---

## Section 12 — Stretch work
These are optional, but they deepen your understanding.

### Stretch 12.1 — Design review
Write a paragraph defending the decision to keep exceptions in `core/`.
Then write a paragraph arguing the opposite.
Finally, decide which design better fits this repository and why.

### Stretch 12.2 — Logging design
Design a hypothetical log schema for a future ingestion command.
Include at least these fields conceptually:
- file path,
- action,
- duration,
- result,
- and failure reason.
You do not need JSON.
You do need consistent thinking.

### Stretch 12.3 — Path edge cases
Investigate each of these and write down what you observe on your OS:
- uppercase `.PDF`,
- hidden files like `.hidden.pdf`,
- symlinked directories,
- broken symlinks,
- and paths containing spaces.

---

## Section 13 — Self-check rubric
Use this before moving on.

### Green
- I can explain the main methods on `Path` without looking them up.
- I understand why exceptions carry attributes like `path` and `paper_id`.
- I can choose a sensible logging level for normal events and failures.
- I can read the path tests and predict what would break if the implementation changed.

### Yellow
- I know the names, but I still mix up `glob()` and `rglob()`.
- I understand exceptions in theory, but I still overuse `except Exception`.
- I can run the tests, but I cannot yet explain all of them.

### Red
- I still build paths with string concatenation.
- I cannot tell the difference between a warning and an error.
- I think logging is just prettier `print()`.
- I do not know where the CLI should catch failures.

If you are in yellow or red on several points, return to `notes.md` before continuing.

---

## Section 14 — Completion challenge
Without opening the code, write a one-page walkthrough of what happens when a user runs:

```bash
researchops --verbose scan examples/sample_papers --recursive
```

Your walkthrough must include:
- CLI parsing,
- logging configuration,
- string-to-`Path` conversion,
- recursive file discovery,
- exception handling,
- table rendering,
- and exit behavior.

If you can produce that walkthrough accurately, you are ready for Week 3.
