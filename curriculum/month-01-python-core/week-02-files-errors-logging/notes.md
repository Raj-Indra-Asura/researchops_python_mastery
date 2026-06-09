# Chapter 2 Notes — Files, Errors, and Logging

## 1. Chapter overview
Week 2 is about making file-based programs dependable.
A beginner script often works only when the inputs are perfect.
A production-minded script still behaves clearly when the inputs are imperfect.
ResearchOps is starting that transition now.
This chapter sits between “the CLI exists” and “the application has rich domain models.”
It teaches the habits that make later weeks stable.
Those habits are path safety, deliberate exceptions, and structured logging.

A research paper pipeline touches the outside world constantly.
It reads directories.
It discovers files.
It opens text.
It writes outputs.
It creates folders.
It reports failures.
The outside world is messy.
Your code has to acknowledge that mess.

The theme of this chapter is simple.
Do not pretend failure will not happen.
Design the code so that when failure happens, the program remains understandable.
That is the foundation of maintainable software.

## 2. What you already know
From Week 1, you already know how to create a virtual environment.
You know how to install the project in editable mode.
You know that the repository uses a `src/` layout.
You know that the CLI entry point lives in `src/researchops/cli/main.py`.
You know how Typer commands are declared.
You know how to run tests.
You know basic functions, imports, and return values.
You know that the `scan` command exists.

That earlier knowledge matters here.
This week does not replace Week 1.
It deepens it.
The command still starts the same way.
The project structure still matters.
But now you are looking at what happens when the command leaves the safe world of pure Python objects and interacts with the filesystem.

## 3. What problem this week solves
Imagine a user runs:

```bash
researchops scan ./papers
```

Now ask the uncomfortable questions.
What if `./papers` does not exist?
What if `./papers` is actually a file?
What if the folder contains PDFs and non-PDFs mixed together?
What if the PDFs are nested three levels deep?
What if some files are empty?
What if a downstream reader cannot decode text?
What if you need to debug why one user found 50 PDFs and another found 0?

Naive code tends to answer these questions badly.
It might crash with a confusing traceback.
It might silently return the wrong result.
It might mix diagnostics with user output.
It might behave differently on different machines.
It might be impossible to test deterministically.

Week 2 solves that class of problem.
It gives the scanner a contract.
It gives failures names.
It gives developers observability.
It gives tests specific guarantees to verify.

## 4. Beginner mental model
Use this mental model for the whole chapter.
A path is not just text.
A path is a promise about where something should be.
Your code should verify that promise before relying on it.

An exception is not just a crash.
An exception is a signal that a function could not keep its promise.
Good exception design makes that signal precise.

A log is not just output.
A log is a breadcrumb for understanding what the program did.
Good logs tell a story without shouting constantly.

Put those together.
A robust program asks careful questions about the world.
If the answers are acceptable, it proceeds.
If not, it raises the right signal.
As it works, it leaves useful breadcrumbs.
That is the Week 2 mindset.

## 5. Core vocabulary
### `pathlib.Path`
A `Path` object represents a filesystem path as a Python object.
It replaces fragile string-based path manipulation.
It provides methods and properties that make file code more expressive.

### glob
A glob is a pattern used to match file or directory names.
Examples include `*.pdf` and `**/*.pdf`.
Glob patterns are simpler than regular expressions.
They are designed specifically for filesystem matching.

### exception hierarchy
An exception hierarchy is a family tree of exception classes.
A base class sits above narrower subclasses.
This lets callers catch a whole family or a specific branch.

### traceback
A traceback is Python’s printed record of where an exception happened.
It shows the call stack.
It is useful for developers.
It is often too raw for end users.

### log level
A log level is a severity category like `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
Levels help filter what messages appear.
They turn “all output” into “the right output for this moment.”

### structured logging
Structured logging means writing logs in a deliberate, consistent format.
It does not always require JSON.
It does require predictable fields and stable meaning.
For this repository, consistency in level, module name, and message context matters.

### encoding
An encoding is the rule that maps bytes to text characters and back.
UTF-8 is the modern default choice for most Python projects.
Being explicit about encoding avoids cross-machine surprises.

### recursive
A recursive file search descends into subdirectories.
A non-recursive search only looks at the current directory level.
Recursive searches are powerful, but they should be intentional.

### pattern matching
In this chapter, pattern matching means matching file names against glob patterns.
It does not mean the newer `match` statement in Python.
Context matters.

## 6. `pathlib.Path` from first principles
### Why not use plain strings?
A string like `"papers/report.pdf"` can represent a path.
But the string itself does not know anything about filesystems.
It cannot tell you whether it exists.
It cannot tell you whether it is a file or a directory.
It cannot join path segments safely without help.
It cannot expose a clear `.suffix` or `.parent` API.

With raw strings, beginners often write code like this:

```python
folder = "papers"
filename = "report.pdf"
path = folder + "/" + filename
```

This is fragile for several reasons.
It hard-codes a separator.
It encourages manual slicing later.
It makes the code read like text manipulation instead of filesystem logic.
It scales badly when paths become more complex.

`Path` solves that by turning paths into first-class objects.
You can write:

```python
from pathlib import Path
path = Path("papers") / "report.pdf"
```

Now the code says what it means.
You are joining path parts, not concatenating strings.

### Creating `Path` objects
The simplest form is:

```python
from pathlib import Path
p = Path("examples/sample_papers")
```

This creates a path object.
It does not read the disk yet.
It does not verify existence yet.
It is just a representation.
That laziness is important.
A `Path` can represent both existing and not-yet-existing locations.

### Joining paths with `/`
One of the nicest `Path` features is the `/` operator.

```python
root = Path("examples")
child = root / "sample_papers" / "README.md"
```

This is not division.
For `Path`, `/` means path joining.
It is readable and hard to misuse.

### `.exists()`
Use `.exists()` to ask whether the path currently exists on disk.

```python
p.exists()
```

It returns `True` or `False`.
It does not tell you what kind of thing exists there.
A path can exist as a file, directory, symlink, or other filesystem object.
That is why `.exists()` is often followed by another check.

### `.is_dir()`
Use `.is_dir()` to ask whether the path points to a directory.

```python
p.is_dir()
```

If the path does not exist, this returns `False`.
That is why separating the existence check from the directory-type check makes error messages clearer.
The user deserves to know whether the path is missing or simply the wrong kind.

### `.is_file()`
Use `.is_file()` to ask whether the path points to a file.

```python
p.is_file()
```

This is the sibling concept to `.is_dir()`.
It is often used when opening a single file instead of scanning a folder.

### `.name`
`.name` returns the final path component.

```python
p = Path("papers/report.pdf")
p.name
```

This would be `"report.pdf"`.
It is useful when displaying filenames to users.

### `.stem`
`.stem` returns the file name without the final suffix.

```python
p.stem
```

For `report.pdf`, the stem is `"report"`.
This is useful when generating related output names.

### `.suffix`
`.suffix` returns the final file extension, including the leading dot.

```python
p.suffix
```

For `report.pdf`, the suffix is `".pdf"`.
This is helpful for extension-based filtering.
Remember that suffix checks can be case-sensitive depending on how you use them.

### `.parent`
`.parent` gives the containing directory.

```python
p.parent
```

For `papers/report.pdf`, the parent is `papers`.
This is useful when you need to create sibling files or directories.

### `.glob()`
`.glob(pattern)` finds matching entries below the current path according to the pattern.

```python
root = Path("papers")
root.glob("*.pdf")
```

This does not return a list automatically.
It returns an iterator-like object.
That means you often wrap it in `list(...)` or `sorted(...)`.
ResearchOps uses `sorted(...)` because deterministic order matters.

### `.rglob()`
`.rglob(pattern)` means recursive glob.
It walks through subdirectories.

```python
root.rglob("*.pdf")
```

This is conceptually similar to `root.glob("**/*.pdf")`.
The codebase uses the second style because it keeps both branches flowing through one call shape.

### `.read_text()`
`.read_text()` reads a file as text and returns a string.

```python
text = p.read_text(encoding="utf-8")
```

Always think about encoding when reading text.
Always think about whether the file exists.
Always think about whether the file is truly text.

### `.write_text()`
`.write_text()` writes a string into a file.

```python
p.write_text("hello\n", encoding="utf-8")
```

Again, specify UTF-8 explicitly.
That habit makes your code clearer and more portable.

### `.mkdir()`
`.mkdir()` creates a directory.

```python
p.mkdir(parents=True, exist_ok=True)
```

`parents=True` means create missing parent directories too.
`exist_ok=True` means do not error if the directory already exists.
This is perfect for idempotent setup helpers.

### `.stat()`
`.stat()` returns filesystem metadata.

```python
size = p.stat().st_size
```

In the scan command, `pdf.stat().st_size` is used to show file sizes in KB.
This is a nice example of `Path` carrying more than just naming convenience.

### Why this API matters in ResearchOps
ResearchOps will eventually scan, parse, store, search, and learn from files.
Every one of those stages benefits from paths being objects with clear capabilities.
Path handling is infrastructure literacy.
Without it, later features become brittle.

## 7. How glob patterns work
### `*.pdf`
This pattern means “match files in the current directory whose names end with `.pdf`.”
It does not descend into subdirectories.
It is the non-recursive option.

### `**/*.pdf`
This pattern means “recursively descend through subdirectories and match files ending with `.pdf`.”
The `**` part is what makes the pattern recursive.
This is the pattern ResearchOps uses when `recursive=True`.

### `glob()` vs `rglob()`
`glob()` follows whatever pattern you give it.
`rglob("*.pdf")` is a convenience form for recursive matching.
`glob("**/*.pdf")` and `rglob("*.pdf")` are often equivalent in practice.
The current code uses `glob(pattern)` so one function call handles both modes.
That keeps the implementation small and readable.

### Why pattern choice is a design choice
A recursive search can be more helpful.
It can also be more expensive and more surprising.
If a user points at a large top-level directory and recursive search is on by default, the program might visit far more files than expected.
This is why the code makes recursion explicit with a boolean flag.
Good defaults reduce surprise.
Explicit options increase control.

### Hidden detail: case sensitivity
Pattern matching interacts with the filesystem.
On Linux, `*.pdf` usually will not match `PAPER.PDF`.
On case-insensitive filesystems, behavior may differ.
That means extension-based matching should be tested, not assumed.
This is a wonderful example of why reading code is not enough.
Real systems live on real operating systems.

## 8. File encodings
### What is an encoding?
Computers store bytes.
Humans read text.
An encoding tells Python how to translate between those worlds.
Without an encoding, bytes are just bytes.
With the wrong encoding, valid bytes can become nonsense or errors.

### Why UTF-8 matters
UTF-8 is the dominant text encoding for modern software.
It supports Unicode.
It works well with international text.
It is the safest default for modern Python applications unless you have a very specific reason otherwise.

### Why explicit encoding matters
When you write:

```python
text = path.read_text()
```

Python uses a default encoding influenced by the environment.
That may differ across machines.
Code that “works for me” can fail for someone else.
Explicit UTF-8 removes that ambiguity.

Write this instead:

```python
text = path.read_text(encoding="utf-8")
```

That line communicates intent.
It also makes debugging easier because the choice is visible in the code.

### What happens without explicit encoding?
Sometimes nothing obvious happens.
That is the dangerous case.
The code may appear fine until one machine, one file, or one locale exposes the hidden assumption.
Sometimes you get a `UnicodeDecodeError`.
Sometimes you get text that technically decodes but is wrong.
Silent corruption is often worse than a loud exception.

### ResearchOps perspective
Research papers, notes, configs, prompts, logs, and exported metadata are all text-bearing artifacts.
When the project grows, encoding discipline becomes non-optional.
Week 2 plants that habit early.

## 9. Exception design from first principles
### Python already has exceptions.
Why add custom ones?
Built-in exceptions are useful.
You should absolutely use them when they fit.
`NotADirectoryError` is a great example in this chapter.
It precisely describes a filesystem contract violation.

But applications often need domain meaning too.
“Paper not found” is more specific than a generic lookup failure.
“Empty document” is more specific than a generic parse failure.
That is where custom exceptions shine.

### Why create `ResearchOpsError`?
A shared base class gives the application an exception family.
If a caller wants to catch all application-level failures in one place, it can catch `ResearchOpsError`.
If it wants only parsing failures, it can catch `ParsingError`.
If it wants only storage issues, it can catch `StorageError`.
This is a powerful design pattern.

### What makes a good custom exception?
A good custom exception has:
- a clear name,
- a clear place in the hierarchy,
- a useful message,
- and any metadata that callers may need.

For example:

```python
class PaperNotFoundError(StorageError):
    def __init__(self, paper_id: str) -> None:
        super().__init__(f"Paper not found: {paper_id}")
        self.paper_id = paper_id
```

This design does two things.
It produces a message useful to humans.
It preserves structured data useful to code.
That is excellent exception design.

### Why store `self.path` or `self.paper_id`?
Because messages are for people.
Attributes are for programs.
Tests can check `exc.paper_id` directly.
Higher-level code can branch on `exc.path` without parsing strings.
String parsing is fragile.
Dedicated attributes are strong design.

### When do you need a custom `__init__`?
Use a custom constructor when the exception needs to:
- build a helpful message from structured inputs,
- store metadata on the instance,
- or normalize the error shape.

If an exception needs no special data, an empty subclass with a docstring is often enough.
That is why some classes in `core/exceptions.py` define `__init__` and some do not.

## 10. Python’s exception hierarchy and ResearchOps’ hierarchy
Python has a very large built-in hierarchy.
At the top of application-relevant exceptions is `Exception`.
Under that are many built-ins like `ValueError`, `TypeError`, and `OSError`.
`NotADirectoryError` lives under the OS-related branch.
That is why it fits path validation so well.

ResearchOps adds its own hierarchy beneath `Exception`.
Conceptually, it looks like this:

```text
Exception
└── ResearchOpsError
    ├── ParsingError
    │   ├── EmptyDocumentError
    │   └── UnsupportedFileTypeError
    ├── StorageError
    │   ├── PaperNotFoundError
    │   └── DuplicatePaperError
    ├── SearchError
    │   └── EmptyQueryError
    ├── ConfigurationError
    ├── MLError
    │   ├── ModelNotTrainedError
    │   └── InsufficientDataError
    └── JobError
        └── JobNotFoundError
```

Notice the design benefit.
The hierarchy matches the architecture of the application.
That makes errors easier to reason about.
It also future-proofs the project.
New features can add new subclasses without disturbing the base contract.

## 11. `try`, `except`, `else`, and `finally`
### `try`
The `try` block contains code that may fail.
It is where you place the risky operation.
The point is not to assume failure.
The point is to mark the boundary where failure becomes meaningful.

### `except`
The `except` block handles a named failure type.
You should catch the narrowest exception you can actually respond to.
If you do not know how to recover or translate the failure, do not catch it casually.

### `else`
The `else` block runs only if no exception occurred in the `try` block.
This is useful because it keeps success-only code visually separate from failure-handling code.
It prevents the `try` block from becoming too large.

### `finally`
The `finally` block runs whether or not an exception occurred.
Use it for cleanup actions such as closing resources when a context manager is not available.
In modern Python, `with` often handles this pattern more elegantly.
Still, you must understand `finally`.

### Simple example

```python
try:
    text = path.read_text(encoding="utf-8")
except OSError as exc:
    log.error("Failed to read %s: %s", path, exc)
else:
    log.info("Read %d characters from %s", len(text), path)
finally:
    log.debug("Read attempt finished for %s", path)
```

This example teaches four separate jobs.
The risky operation is the file read.
The named failure is any OS-level read problem.
The success-only code reports the text length.
The cleanup-style message marks the end of the attempt regardless of outcome.

### Why not put everything inside `try`?
Because huge `try` blocks blur the source of errors.
If ten lines live inside the `try`, the `except` may catch failures from lines you did not intend.
Smaller `try` blocks produce clearer reasoning.

## 12. How to raise exceptions intentionally
Raising an exception is part of API design.
It is how a function says, “I cannot fulfill my contract under these inputs or conditions.”

Example:

```python
if not directory.exists():
    raise NotADirectoryError(f"Directory does not exist: {directory}")
```

This is intentional and correct.
The function is not waiting for some later operation to fail mysteriously.
It is checking a precondition and raising early with a precise message.
That is defensive programming.

Another example:

```python
if not query.strip():
    raise EmptyQueryError()
```

This turns an invalid domain input into a named application signal.
Again, this is not “being dramatic.”
It is communicating clearly.

## 13. Re-raising with context using `raise X from Y`
Sometimes a lower-level exception is technically correct but too low-level for the caller.
You may want to translate it into a more domain-appropriate exception while preserving the original cause.
That is what exception chaining is for.

Example:

```python
from researchops.core.exceptions import ConfigurationError

try:
    text = config_path.read_text(encoding="utf-8")
except OSError as exc:
    raise ConfigurationError("Could not read configuration file") from exc
```

The new exception is more meaningful at the application layer.
The original exception is still attached underneath.
A traceback will show both.
That is much better than losing the original cause.

Use chaining when you are translating layers.
Do not use it if you are merely logging and re-raising the exact same exception unchanged.
Choose the tool that matches the reason.

## 14. Catch width and why `except Exception` is dangerous
### The temptation
Beginners often write:

```python
try:
    do_the_thing()
except Exception:
    print("Something went wrong")
```

This feels safe.
It is actually dangerous.

### Why it is dangerous
It hides programming bugs.
It can swallow `TypeError` caused by wrong arguments.
It can swallow `AttributeError` caused by misspelled method names.
It can make development failures look like routine user input problems.
It turns debugging into mud.

### What to do instead
Catch specific exceptions that you can classify and handle.
For file scanning, catching `NotADirectoryError` at the CLI boundary is sensible.
Catching every possible exception from anywhere is not.

### A practical rule
If you catch an exception, ask yourself two questions.
Do I know what this means?
Do I know what the program should do next?
If the answer to either question is no, reconsider catching it there.

## 15. Logging vs `print`
### Why beginners reach for `print`
`print()` is immediate.
It is simple.
It feels like the fastest way to see what the program is doing.
For tiny experiments, it can be fine.

### Why production code needs logging
Logging has levels.
Logging can be turned on or filtered.
Logging carries logger names.
Logging works with handlers and formatters.
Logging integrates with test capture and operational tooling.
`print()` does none of that well.

### Example comparison
Bad production habit:

```python
print(f"Found {len(pdfs)} PDF(s) in {directory}")
```

Better application habit:

```python
log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
```

The second line can be hidden in normal mode and shown in verbose mode.
The first line always shouts.
The second line knows which module emitted it.
The first line does not.
The second line belongs in instrumentation.
The first line belongs mainly in quick scripts or throwaway debugging.

## 16. Python logging module basics
### Loggers
A logger is the object you call `.debug()`, `.info()`, `.warning()`, `.error()`, or `.critical()` on.
Loggers are usually named.
Logger names form a hierarchy using dots.
For example, `researchops.utils.paths` sits under `researchops.utils`, which sits under `researchops`.

### Handlers
A handler decides where log records go.
A stream handler writes to standard error.
A file handler writes to a file.
Rich’s handler renders logs prettily in the terminal.
Handlers are output destinations.

### Formatters
A formatter decides how a log record is rendered as text.
It controls fields like time, level name, logger name, and message.
Formatters shape readability.

### The root logger
The root logger sits at the top of the logging tree.
Calling `logging.basicConfig(...)` configures it in a simple way.
Child loggers inherit behavior from it unless configured otherwise.
That is why calling `configure_logging()` once at startup is enough for many modules.

## 17. Why `logging.getLogger(__name__)` is the right pattern
`__name__` is the current module’s name.
If you call:

```python
log = logging.getLogger(__name__)
```

inside `researchops.utils.paths`, the logger name becomes `researchops.utils.paths`.
That is exactly what you want.
The logger identifies the source module automatically.
If the file is renamed or moved, the logger name updates with the module name.
That is better than hard-coding a string.

Using `__name__` also keeps logs consistent across the project.
Every module follows the same rule.
Consistency is part of observability.

## 18. Log levels in ResearchOps
### `DEBUG`
Use `DEBUG` for internal state details helpful during development or troubleshooting.
Examples include counts, chosen patterns, visited paths, or timing details.
In this repository, `find_pdfs()` logs the number of PDFs found at `DEBUG` level.
That is appropriate because normal users do not always need that detail.

### `INFO`
Use `INFO` for expected, important progress.
Examples include “scan started,” “ingestion complete,” or “12 PDFs found.”
An operator or user might reasonably want to see this in normal mode.

### `WARNING`
Use `WARNING` for recoverable problems.
Examples include “skipping unsupported file type” or “optional config missing, using default.”
The program continues, but the event matters.

### `ERROR`
Use `ERROR` when a specific operation failed and should be noticed.
Examples include “failed to read file” or “database write failed.”
The whole application might continue, but something important did not work.

### `CRITICAL`
Use `CRITICAL` for catastrophic failures that likely stop the application or make it unsafe to continue.
This level is rare.
Overusing it weakens its meaning.

## 19. How to write log messages well
### Prefer parameterized logging
Write:

```python
log.error("Failed to read %s: %s", path, exc)
```

instead of:

```python
log.error(f"Failed to read {path}: {exc}")
```

### Why `%s` formatting is preferred in log calls
The logging system can defer string interpolation until needed.
That matters when a level is filtered out.
It is also the conventional style in Python logging APIs.
It keeps message templates stable.
It helps tooling reason about logs more easily.

### What belongs in a good message?
A good log message answers three questions.
What happened?
To what?
With what relevant context?

For example:
- “Found 3 PDF(s) in examples/sample_papers”
- “Skipping unsupported file type: notes.txt”
- “Failed to read config/settings.toml: permission denied”

### What not to do
Do not write vague messages like “Error happened.”
Do not repeat context the logger already gives you unless it improves clarity.
Do not log the same failure in five different layers unless each layer adds distinct value.
Noise is not observability.

## 20. Defensive programming patterns
Defensive programming means checking assumptions early and making failures legible.
It does not mean wrapping every line in fear.
It means protecting the boundaries where reality enters your program.

Useful patterns in this chapter include:
- validating a directory before scanning it,
- using explicit encodings when reading text,
- sorting discovered files for deterministic behavior,
- raising specific exceptions with context,
- and logging enough detail to reconstruct what happened.

Defensive programming supports tests.
Tests support refactoring.
Refactoring supports growth.
That chain matters.

## 21. ResearchOps-specific application
The ResearchOps scanner is not just a toy file lister.
It is the first stage of a future research paper pipeline.
The pipeline will later parse text, store metadata, run search, and support ML workflows.
If file discovery is unreliable, every later stage inherits uncertainty.

Consider these future consequences.
A bad path function could cause missing inputs for parsing.
A vague exception could make storage failures look like parser failures.
A noisy logging setup could bury real warnings during ingestion.
A silent encoding assumption could corrupt metadata exports.
Week 2 is operational hygiene.
Operational hygiene compounds.

## 22. Full annotated `paths.py`
Here is the current file, followed by explanation of each meaningful line.

```python
"""Path utilities for ResearchOps.

This module provides helpers for discovering and validating file paths.
It uses pathlib throughout — never os.path.
"""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def find_pdfs(directory: Path, recursive: bool = False) -> list[Path]:
    """Return a sorted list of PDF files found in *directory*.

    Args:
        directory: The directory to scan.
        recursive: If True, search all subdirectories as well.

    Returns:
        A sorted list of Path objects pointing to .pdf files.

    Raises:
        NotADirectoryError: If *directory* does not exist or is not a directory.
    """
    if not directory.exists():
        raise NotADirectoryError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdfs = sorted(directory.glob(pattern))
    log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
    return pdfs


def ensure_dir(path: Path) -> Path:
    """Create *path* and all parent directories if they don't exist.

    Returns the path so callers can use this inline:
        db_path = ensure_dir(settings.db_path.parent) / "researchops.db"
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_resolve(path: Path) -> Path:
    """Return a resolved absolute path without raising on symlink loops."""
    try:
        return path.resolve()
    except OSError:
        return path.absolute()
```

### Module docstring lines
`"""Path utilities for ResearchOps.` states the file’s responsibility immediately.
The next docstring lines explain that the module centralizes discovery and validation behavior.
The line saying “never os.path” is pedagogical and architectural.
It tells contributors that `Path` is the repository convention.
That kind of convention note reduces drift.

### `from __future__ import annotations`
This postpones evaluation of annotations.
In modern Python, it helps keep type hints lightweight and avoids some forward-reference issues.
It is a common project-wide style choice.

### `import logging`
This imports the standard library logging module.
The file needs it because `find_pdfs()` emits a debug message.

### `from pathlib import Path`
This imports the path object used throughout the module.
It is central because every public function here works with `Path`.

### `log = logging.getLogger(__name__)`
This creates a module-level logger.
Using `__name__` ties the logger name to the module path.
That makes log output traceable to the source.
A module-level logger is a clean pattern because every function can reuse it.

### `def find_pdfs(directory: Path, recursive: bool = False) -> list[Path]:`
The function signature tells you a lot.
`directory` is expected to be a `Path`, not a string.
`recursive` is optional and defaults to `False`.
The return type is a list of `Path` objects.
This is a clean, testable contract.

### Function docstring overview
The first docstring sentence promises sorted PDF results.
The `Args` section names the inputs.
The `Returns` section states the output shape.
The `Raises` section states the important failure contract.
A good docstring is a compact API document.

### `if not directory.exists():`
This is the first precondition check.
The function refuses to continue if the target path is missing.
This is better than letting later behavior be ambiguous.

### `raise NotADirectoryError(f"Directory does not exist: {directory}")`
This raises a precise built-in exception.
The message includes the actual bad path.
That helps both users and tests.
Using `NotADirectoryError` here is reasonable because the contract specifically requires a usable directory path.

### `if not directory.is_dir():`
This is the second precondition check.
Even an existing path might be the wrong kind.
Separating this from the existence check yields better error messages.

### `raise NotADirectoryError(f"Not a directory: {directory}")`
This uses the same exception type with a different message.
The type says “directory contract violated.”
The message says *which* kind of violation occurred.
That is a strong combination.

### Blank line before pattern selection
The blank line visually separates validation from discovery.
Visual structure helps readers reason in phases.

### `pattern = "**/*.pdf" if recursive else "*.pdf"`
This line converts a boolean into a filesystem search pattern.
It keeps the branch small and local.
The program’s behavior is easy to predict from this one line.

### `pdfs = sorted(directory.glob(pattern))`
This is the discovery step.
`directory.glob(pattern)` yields matching paths.
`sorted(...)` makes the result deterministic.
Determinism is excellent for tests, logs, and user trust.
Without sorting, result order can depend on filesystem behavior.

### `log.debug("Found %d PDF(s) in %s", len(pdfs), directory)`
This logs internal diagnostic detail.
The count and directory together are meaningful context.
The message uses parameterized logging instead of an f-string.
The level is `DEBUG`, which means verbose mode can reveal it without bothering normal users.

### `return pdfs`
The function returns only the discovered list.
It does not print.
It does not render tables.
It does not decide CLI behavior.
That separation of concerns is excellent design.

### `def ensure_dir(path: Path) -> Path:`
This helper creates a directory and returns it.
The return value makes chaining convenient.
That improves ergonomics without hiding behavior.

### `"""Create *path* and all parent directories if they don't exist.`
This docstring states the side effect clearly.
Creating directories is not a pure action.
The docstring should say so.

### `Returns the path so callers can use this inline:`
This sentence explains the design reason for returning the path.
It shows the function is not returning the path by accident.
It is supporting a fluent usage style.

### `db_path = ensure_dir(settings.db_path.parent) / "researchops.db"`
This example demonstrates real utility.
It shows how a setup helper can fit neatly into path composition.
Examples like this reduce “why does it return the path?” confusion.

### `path.mkdir(parents=True, exist_ok=True)`
This is the whole operational behavior of the helper.
`parents=True` means create missing parent directories too.
`exist_ok=True` means the call is idempotent for existing directories.
That combination is exactly what setup code often needs.

### `return path`
Returning the path enables inline composition and easy testing.
The tests check both the side effect and this returned value.
That is a nice example of API ergonomics reinforced by tests.

### `def safe_resolve(path: Path) -> Path:`
This helper tries to produce a resolved absolute path while avoiding a hard failure on certain OS issues like symlink loops.
The name communicates its intent clearly.

### `"""Return a resolved absolute path without raising on symlink loops."""`
The docstring explains both the goal and the safety behavior.
It tells the reader why this function exists separately from calling `.resolve()` directly.

### `try:`
The risky operation begins here.
Resolving paths can raise `OSError` in edge cases.

### `return path.resolve()`
This is the preferred outcome.
A resolved path usually collapses symlinks and produces an absolute representation.
That can be useful for logging, configuration, and consistent identity.

### `except OSError:`
This catches a specific family of OS-level failures.
It does not catch all exceptions.
That is a good choice.

### `return path.absolute()`
This is the fallback behavior.
It still produces an absolute path, even if full resolution failed.
That makes the helper robust while preserving usefulness.
This is a good example of graceful degradation.

## 23. Full annotated `exceptions.py`
Here is the current file, followed by explanation of each meaningful part.

```python
"""Custom exception hierarchy for ResearchOps.

Rule: every exception the application raises should be a subclass of
ResearchOpsError so callers can catch the whole family with one clause.

These exceptions live in core/ and must not import from storage,
parsing, CLI, API, or any infrastructure layer.
"""


class ResearchOpsError(Exception):
    """Base class for all ResearchOps application errors."""


# ---------------------------------------------------------------------------
# Parsing errors
# ---------------------------------------------------------------------------


class ParsingError(ResearchOpsError):
    """Raised when a document cannot be parsed."""


class EmptyDocumentError(ParsingError):
    """Raised when a parsed document contains no extractable text."""

    def __init__(self, path: str) -> None:
        super().__init__(f"No text could be extracted from: {path}")
        self.path = path


class UnsupportedFileTypeError(ParsingError):
    """Raised when a file type is not supported (e.g. .docx instead of .pdf)."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Unsupported file type: {path}")
        self.path = path


# ---------------------------------------------------------------------------
# Storage errors
# ---------------------------------------------------------------------------


class StorageError(ResearchOpsError):
    """Raised for database / persistence failures."""


class PaperNotFoundError(StorageError):
    """Raised when a paper ID does not exist in storage."""

    def __init__(self, paper_id: str) -> None:
        super().__init__(f"Paper not found: {paper_id}")
        self.paper_id = paper_id


class DuplicatePaperError(StorageError):
    """Raised when trying to insert a paper that already exists."""

    def __init__(self, paper_id: str) -> None:
        super().__init__(f"Paper already exists: {paper_id}")
        self.paper_id = paper_id


# ---------------------------------------------------------------------------
# Search errors
# ---------------------------------------------------------------------------


class SearchError(ResearchOpsError):
    """Raised for search-related failures."""


class EmptyQueryError(SearchError):
    """Raised when a search query is blank or whitespace-only."""

    def __init__(self) -> None:
        super().__init__("Search query must not be empty.")


# ---------------------------------------------------------------------------
# Configuration errors
# ---------------------------------------------------------------------------


class ConfigurationError(ResearchOpsError):
    """Raised when the application configuration is invalid or missing."""


# ---------------------------------------------------------------------------
# ML errors
# ---------------------------------------------------------------------------


class MLError(ResearchOpsError):
    """Base class for ML-related errors."""


class ModelNotTrainedError(MLError):
    """Raised when trying to use a model that hasn't been trained yet."""

    def __init__(self, model_name: str) -> None:
        super().__init__(f"Model not trained: {model_name}. Run the train command first.")
        self.model_name = model_name


class InsufficientDataError(MLError):
    """Raised when there is not enough data to train a model."""

    def __init__(self, needed: int, available: int) -> None:
        super().__init__(
            f"Need at least {needed} samples to train, but only {available} available."
        )


# ---------------------------------------------------------------------------
# Job / worker errors
# ---------------------------------------------------------------------------


class JobError(ResearchOpsError):
    """Base class for job / worker errors."""


class JobNotFoundError(JobError):
    """Raised when a job ID does not exist."""

    def __init__(self, job_id: str) -> None:
        super().__init__(f"Job not found: {job_id}")
        self.job_id = job_id
```

### Module docstring meaning
The opening docstring explains the central rule.
Every application-raised exception should inherit from `ResearchOpsError`.
That one sentence defines the design contract for the whole file.
The docstring also reminds readers of an architecture rule.
Exceptions in `core/` must stay independent of infrastructure.
That preserves clean dependency direction.

### `class ResearchOpsError(Exception):`
This is the application root exception.
It is intentionally simple.
Its power comes from what inherits from it.

### `"""Base class for all ResearchOps application errors."""`
The docstring turns the class into documentation, not just mechanics.
It tells every future contributor what belongs under this root.

### Comment separators like `# Parsing errors`
These lines are not operational.
They are organizational.
In long exception files, category separators improve readability.
Readable error hierarchies are part of good architecture.

### `class ParsingError(ResearchOpsError):`
This creates a branch for parser-related problems.
A caller can catch all parsing issues together without catching unrelated storage or search issues.
That is the benefit of hierarchy.

### `class EmptyDocumentError(ParsingError):`
This is a narrow parsing failure.
The file was parseable enough to inspect, but no extractable text was found.
Naming matters here.
This is more informative than a generic `ParsingError`.

### `def __init__(self, path: str) -> None:`
The constructor accepts the path that caused the failure.
A narrow exception should preserve the important input that triggered it.

### `super().__init__(f"No text could be extracted from: {path}")`
This builds the human-facing message.
Users and logs can display this directly.
A message should say what happened and where.

### `self.path = path`
This stores structured metadata on the exception.
Now code can inspect the path directly.
Tests can verify it without parsing the message.
That is clean design.

### `class UnsupportedFileTypeError(ParsingError):`
This is another narrow parsing-related failure.
It communicates that the file type is outside supported formats.
Again, the hierarchy allows both specific and general catches.

### Its constructor lines
These mirror the design of `EmptyDocumentError`.
Consistency across sibling exceptions makes the API easier to learn.

### `class StorageError(ResearchOpsError):`
This begins the storage branch.
As the project grows, database or persistence problems can hang under this category.
This keeps storage concerns grouped.

### `class PaperNotFoundError(StorageError):`
This is a domain-specific storage failure.
The missing thing is not just “a row.”
It is a paper identified by `paper_id`.
Good domain naming makes code speak the language of the application.

### `self.paper_id = paper_id`
This follows the same structured-data pattern as path-bearing exceptions.
Again, messages are for humans.
Attributes are for code and tests.

### `class DuplicatePaperError(StorageError):`
This models a different storage contract violation.
The target already exists.
That is not the same as “not found.”
Separate classes keep meanings crisp.

### Search branch
`class SearchError(ResearchOpsError):` creates a search-related category.
`class EmptyQueryError(SearchError):` expresses a specific invalid search input.
An empty query is not a storage failure.
It is not a parsing failure.
The hierarchy encodes that truth.

### `super().__init__("Search query must not be empty.")`
This constructor has no extra metadata.
That is fine.
Not every exception needs stored attributes.
Only store extra data when it helps.

### `class ConfigurationError(ResearchOpsError):`
This is a standalone branch for bad or missing configuration.
It currently has no custom constructor because the base exception machinery is enough.
A plain subclass is still useful because the name carries meaning.

### ML branch
The ML branch shows that the hierarchy is preparing for later chapters.
`MLError` groups model-related issues.
This anticipates future architecture while staying lightweight.

### `class ModelNotTrainedError(MLError):`
This expresses a state-dependent failure.
The model exists conceptually, but it is not ready for use.
The message includes an instruction: run the train command first.
That is a nice example of an exception guiding the user toward recovery.

### `self.model_name = model_name`
Again, structured metadata is preserved.
This is consistent with the project’s exception design pattern.

### `class InsufficientDataError(MLError):`
This represents another ML-specific precondition failure.
Training requires enough samples.
The constructor includes both `needed` and `available` counts in the message.
Even without storing them as attributes, the message itself is quite informative.
A later revision could store them too if callers need programmatic access.

### Job / worker branch
`JobError` creates a category for background work or asynchronous processing concerns.
`JobNotFoundError` then narrows that to a missing job identifier.
This shows the hierarchy is scaling with the project’s roadmap.

### Final takeaway on this file
This file is small, but it teaches a big lesson.
Error names are part of domain design.
The hierarchy is not just for catching.
It is also a map of what kinds of failure the application cares about.

## 24. Full annotated `logging.py`
Here is the current file, followed by explanation of each meaningful part.

```python
"""Structured logging configuration for ResearchOps.

Call ``configure_logging()`` once at application startup (in the CLI
entry point or the API lifespan handler). After that, use the stdlib
``logging`` module everywhere — no direct dependency on this module
required.

Design decisions:
- Use ``logging.basicConfig`` with a structured format for simplicity.
- Rich handler for pretty terminal output in development mode.
- Plain stream handler for production / CI environments.
"""

import logging
import sys


def configure_logging(
    level: str | None = None,
    use_rich: bool = True,
) -> None:
    """Configure the root logger for the application.

    Args:
        level: Logging level string (DEBUG, INFO, WARNING, ERROR).
               Defaults to INFO if not provided.
        use_rich: Use Rich's pretty handler for development output.
                  Set to False in production or when capturing logs.
    """
    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)

    if use_rich:
        try:
            from rich.logging import RichHandler

            handler: logging.Handler = RichHandler(
                rich_tracebacks=True,
                show_path=False,
            )
            fmt = "%(message)s"
        except ImportError:
            handler = logging.StreamHandler(sys.stderr)
            fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    else:
        handler = logging.StreamHandler(sys.stderr)
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    logging.basicConfig(
        level=log_level,
        format=fmt,
        handlers=[handler],
        force=True,  # override any existing configuration
    )

    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger.

    Usage:
        log = get_logger(__name__)
        log.info("Processing file: %s", path)
    """
    return logging.getLogger(name)
```

### Logging module docstring
The docstring explains when to call `configure_logging()`.
It should happen once at startup.
That matters because logging configuration is a global concern.
The docstring also says that after configuration, regular `logging` usage is enough.
That is a nice design choice.
Modules do not need to import custom helper code just to emit logs.
They can use the standard library API directly if desired.

### `import logging`
The file relies on the standard logging system.
That is the central dependency here.

### `import sys`
This is needed because the plain stream handler writes to `sys.stderr`.
Standard error is the correct place for logs in many CLI contexts.
It keeps logs separate from ordinary command output if needed.

### `def configure_logging(...) -> None:`
This function configures application-wide logging behavior.
It is intentionally called once at startup.
That keeps configuration centralized.

### `level: str | None = None`
The logging level is accepted as a string so callers can pass values like `"DEBUG"` or `"INFO"`.
Allowing `None` gives a clean way to fall back to a default.

### `use_rich: bool = True`
This flag controls whether rich terminal rendering is used.
Rich is nice for development.
Plain output is often better for CI or log capture.
This is a practical design choice.

### Function docstring args section
The docstring explains both parameters clearly.
That matters because configuration functions influence many modules.
Small misunderstandings here spread widely.

### `log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)`
This line converts a string like `"debug"` into the actual logging constant `logging.DEBUG`.
`(level or "INFO")` applies a fallback.
`.upper()` normalizes case.
`getattr(..., logging.INFO)` ensures an invalid string falls back safely to `INFO`.
This is a compact and practical normalization step.

### `if use_rich:`
This branches between development-friendly and plain handlers.
Configuration often needs small environment-dependent choices like this.

### `try:` inside the rich branch
Even if the code prefers Rich, it does not assume Rich is importable at runtime.
That makes the configuration more resilient.
Graceful fallback is a strong operational habit.

### `from rich.logging import RichHandler`
This imports the optional pretty handler only when needed.
That is a nice example of lazy importing based on configuration.

### `handler: logging.Handler = RichHandler(...)`
This creates the handler object that will receive log records.
The explicit type annotation here is a readability bonus.
It reminds the reader what kind of object `handler` is conceptually.

### `rich_tracebacks=True`
This tells Rich to render tracebacks nicely.
That is useful in development because tracebacks become easier to read.

### `show_path=False`
This suppresses path display inside Rich’s rendered output.
The code is choosing a cleaner visual style.
This is a formatter-like presentation decision.

### `fmt = "%(message)s"`
When using Rich, the handler often handles presentation richly enough that a minimal format string is appropriate.
This line keeps the rendered output uncluttered.

### `except ImportError:`
If Rich is unavailable, the code falls back to plain logging output.
That is much better than crashing during startup because a cosmetic dependency is missing.

### `handler = logging.StreamHandler(sys.stderr)`
This creates a standard stream handler that writes to standard error.
It is a solid default for CLI applications.

### `fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"`
This format includes timestamp, level, logger name, and message.
Those are excellent default fields.
They create readable, structured console logs without being too verbose.

### The `else:` branch for `use_rich=False`
This uses the same plain handler and structured format intentionally.
That makes behavior predictable in CI or other non-rich environments.

### `logging.basicConfig(...)`
This is the central configuration call.
It binds the chosen level, format, and handlers to the root logger.
Many projects use `basicConfig` successfully for small to medium applications.
ResearchOps is using the simplest thing that works.
That is a good Week 2 decision.

### `level=log_level`
This sets the global threshold.
Records below this level are filtered out.

### `format=fmt`
This applies the chosen rendering format.

### `handlers=[handler]`
This attaches the selected handler.
Using a list allows the system to support multiple handlers later if desired.

### `force=True`
This tells Python to override any existing logging configuration.
That is important in CLI environments where prior configuration may exist.
Without `force=True`, repeated runs or tests may produce confusing behavior.
This small flag prevents a lot of mystery.

### Noise reduction lines
`logging.getLogger("httpx").setLevel(logging.WARNING)` lowers noise from third-party libraries.
The same happens for `httpcore` and `urllib3`.
This is an operationally mature move.
A logging system is only useful if signal remains visible.
External dependency chatter can drown your own diagnostics.

### `def get_logger(name: str) -> logging.Logger:`
This small helper wraps `logging.getLogger(name)`.
It gives the repository a central, explicit API for obtaining loggers.
Even though the function is thin, it documents intent.
Thin wrappers can be worthwhile when they standardize usage.

### Helper docstring usage example
The docstring shows the intended call pattern with `__name__`.
Examples reduce misuse.
That is especially valuable for beginners.

### `return logging.getLogger(name)`
The function simply returns the requested named logger.
This keeps the helper transparent.
Nothing magical is hidden.

## 25. Annotated logging usage patterns
Here are common patterns this chapter wants you to internalize.

### Startup configuration pattern

```python
from researchops.config.logging import configure_logging

configure_logging(level="DEBUG")
```

This belongs near application startup.
Do not scatter logging configuration throughout the codebase.
Global setup should happen once.

### Module logger pattern

```python
import logging

log = logging.getLogger(__name__)
```

This belongs near the top of modules that emit logs.
It is simple, conventional, and easy to search for.

### Progress message pattern

```python
log.info("Scan started for %s", directory)
```

This records an important normal event.
It is good candidate information for operators and verbose users.

### Recoverable problem pattern

```python
log.warning("Skipping unsupported file: %s", path)
```

The program continues.
The event still matters.
That is what warnings are for.

### Failure pattern

```python
log.error("Failed to read %s: %s", path, exc)
```

This tells you what failed and where.
It also preserves the original exception string.
That is a strong baseline error log.

### Internal detail pattern

```python
log.debug("Found %d PDF(s) in %s", len(pdfs), directory)
```

This is useful during troubleshooting.
It is not essential for every user run.
That is why `DEBUG` is appropriate.

## 26. Full annotated `test_paths.py`
Here is the current test file, followed by what each meaningful line verifies.

```python
"""Unit tests for path utilities."""

from __future__ import annotations

from pathlib import Path

import pytest

from researchops.utils.paths import ensure_dir, find_pdfs


class TestFindPdfs:
    def test_returns_sorted_list(self, tmp_path: Path) -> None:
        (tmp_path / "b.pdf").touch()
        (tmp_path / "a.pdf").touch()
        result = find_pdfs(tmp_path)
        assert [p.name for p in result] == ["a.pdf", "b.pdf"]

    def test_excludes_non_pdf_files(self, tmp_path: Path) -> None:
        (tmp_path / "paper.pdf").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "image.png").touch()
        result = find_pdfs(tmp_path)
        assert len(result) == 1
        assert result[0].name == "paper.pdf"

    def test_returns_empty_for_empty_directory(self, tmp_path: Path) -> None:
        result = find_pdfs(tmp_path)
        assert result == []

    def test_raises_for_nonexistent_directory(self, tmp_path: Path) -> None:
        with pytest.raises(NotADirectoryError):
            find_pdfs(tmp_path / "does_not_exist")

    def test_raises_for_file_not_directory(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.touch()
        with pytest.raises(NotADirectoryError):
            find_pdfs(f)

    def test_recursive_finds_nested_pdfs(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "top.pdf").touch()
        (sub / "nested.pdf").touch()

        non_recursive = find_pdfs(tmp_path, recursive=False)
        recursive = find_pdfs(tmp_path, recursive=True)

        assert len(non_recursive) == 1
        assert len(recursive) == 2

    def test_non_recursive_ignores_subdirectory_pdfs(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.pdf").touch()
        result = find_pdfs(tmp_path, recursive=False)
        assert result == []


class TestEnsureDir:
    def test_creates_directory(self, tmp_path: Path) -> None:
        target = tmp_path / "new" / "nested" / "dir"
        result = ensure_dir(target)
        assert target.exists()
        assert target.is_dir()
        assert result == target

    def test_existing_directory_is_idempotent(self, tmp_path: Path) -> None:
        ensure_dir(tmp_path)  # already exists
        assert tmp_path.exists()
```

### `"""Unit tests for path utilities."""`
The module docstring names the test target.
This is small but helpful when scanning the file quickly.

### Imports
`Path` is imported because the tests use path objects directly.
`pytest` is imported for `raises` and the testing framework.
`ensure_dir` and `find_pdfs` are the functions under test.
A test file should import the smallest target surface needed.

### `class TestFindPdfs:`
Grouping related tests in a class improves readability.
The class is not required by pytest, but it makes the file easier to scan.
The class name acts like a category heading.

### `def test_returns_sorted_list(...)`
This test protects deterministic ordering.
The setup intentionally creates `b.pdf` before `a.pdf`.
That means any sorted output is the function’s doing, not the setup order.
The assertion checks names rather than full paths for clarity.
This is a great test because it protects a subtle but important guarantee.

### `def test_excludes_non_pdf_files(...)`
This test mixes valid and invalid extensions.
It verifies that filtering is by `.pdf` pattern, not by “all files in directory.”
The two assertions together check both count and exact surviving filename.
That makes the failure message more informative if the test breaks.

### `def test_returns_empty_for_empty_directory(...)`
An empty directory is a normal case, not an exceptional one.
This test protects that design choice.
The scanner should return `[]`, not raise an error, when the directory exists but contains no PDFs.
That distinction matters.

### `def test_raises_for_nonexistent_directory(...)`
This test protects the missing-path contract.
It says invalid input should raise `NotADirectoryError`.
This is one of the most important behavioral guarantees in the file.

### `with pytest.raises(NotADirectoryError):`
This is the pytest context-manager style for asserting exceptions.
It makes the expected failure explicit.
Tests should treat expected failure as first-class behavior.

### `def test_raises_for_file_not_directory(...)`
This test protects the second validation branch.
A path can exist and still be the wrong shape.
The test creates a file, then verifies the scanner rejects it as a directory target.
This is exactly the kind of real-world misuse a public function should define clearly.

### `f = tmp_path / "file.txt"`
The variable is short but readable in context.
It represents a concrete existing file.
That is enough for this narrow test.

### `f.touch()`
`touch()` creates the file without needing content.
This keeps the test minimal.
Tests should create only as much reality as needed to prove the behavior.

### `def test_recursive_finds_nested_pdfs(...)`
This test verifies the `recursive` flag changes behavior.
It creates one top-level PDF and one nested PDF.
Then it compares non-recursive and recursive results.
This is a strong behavioral test because it proves both branches in one setup.

### `sub = tmp_path / "sub"`
This creates a nested directory path for the test.
The path name is simple and readable.

### `sub.mkdir()`
The nested directory must exist before the nested file can exist.
This mirrors real filesystem behavior.

### `non_recursive = find_pdfs(tmp_path, recursive=False)`
This is the baseline behavior.
It should see only the top-level file.

### `recursive = find_pdfs(tmp_path, recursive=True)`
This is the opt-in deeper behavior.
It should see both the top-level and nested file.

### `assert len(non_recursive) == 1`
This protects the non-recursive promise.

### `assert len(recursive) == 2`
This protects the recursive promise.
Together, these assertions make the flag’s meaning concrete.

### `def test_non_recursive_ignores_subdirectory_pdfs(...)`
This test isolates the negative case.
It creates only a nested PDF.
Then it verifies the non-recursive search returns nothing.
This is excellent because it proves the function is not accidentally descending.

### `class TestEnsureDir:`
This second test class focuses on the other helper.
Keeping test categories separate improves scanning and maintenance.

### `def test_creates_directory(...)`
This test verifies both side effect and return value.
The target directory path is nested to force parent creation.
That means the test covers `parents=True` behavior indirectly.

### `assert target.exists()`
The directory should now exist.

### `assert target.is_dir()`
Existence alone is not enough.
The created thing must be a directory.
This mirrors the same distinction the production code cares about.

### `assert result == target`
This protects the ergonomic return-value design.
Tests should verify not only behavior but also API shape.

### `def test_existing_directory_is_idempotent(...)`
This test protects `exist_ok=True` behavior.
Calling `ensure_dir()` on an existing directory should not fail.
Idempotency is extremely valuable in setup code.

### `ensure_dir(tmp_path)  # already exists`
The inline comment clarifies the scenario quickly.
This is a justified comment because it makes the intent of the existing fixture path explicit.

### `assert tmp_path.exists()`
The test finishes with a minimal assertion.
The main guarantee is “no failure and still exists.”
That is enough for this case.

## 27. Error handling in the `scan` command
Now focus on the CLI boundary.
This is where lower-level file logic becomes user-facing behavior.

Relevant code:

```python
@app.command()
def scan(
    directory: str = typer.Argument(
        ...,
        help="Path to a directory containing PDF files.",
    ),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Search subdirectories recursively."
    ),
) -> None:
    """Scan a directory and list discovered PDF files.

    This command is a quick sanity-check: it finds PDFs without parsing
    or storing them. Use [bold]ingest[/bold] to actually process them.
    """
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
```

### `directory: str = typer.Argument(...)`
Typer receives CLI input as text.
That is normal.
Command-line arguments start as strings.

### `recursive: bool = typer.Option(...)`
This turns recursion into an explicit user option.
It is opt-in behavior.
That is a good UX choice for potentially expansive scans.

### Command docstring
The docstring clarifies that `scan` is a sanity-check command.
It does not parse or store files.
This is excellent scope communication.
Users should know what a command does *not* do.

### Local imports inside the function
The function imports `Path`, `Table`, and `find_pdfs` inside the command body.
This is acceptable in CLI code when it keeps startup structure or dependencies organized.
It also keeps the command self-contained for readers.

### `path = Path(directory)`
This converts raw CLI text into a path object immediately.
That is a strong boundary move.
The rest of the command can now think in `Path`, not strings.

### `try:` around `find_pdfs(...)`
The CLI knows that this lower-level function may reject invalid directory input.
This is the correct place to translate that failure into user-facing output.
The CLI is an outer boundary.
Outer boundaries are where exception translation often belongs.

### `except NotADirectoryError as exc:`
This catch is narrow and intentional.
The command handles exactly the failure it expects from bad directory input.
It does not swallow unrelated programming bugs.
That is excellent practice.

### `console.print(f"[red]Error:[/red] {exc}")`
This turns the exception into a clean user message.
The message includes the specific reason provided by the lower layer.
The CLI adds presentation.
The lower layer supplied meaning.
That separation is healthy.

### `raise typer.Exit(1) from exc`
The command exits with a non-zero status code to signal failure.
Using `from exc` preserves causal chaining.
That helps debugging.
This is a beautiful example of turning a Python exception into a CLI contract.

### `if not pdfs:`
This handles a normal, non-exceptional case.
The path was valid.
The scan succeeded.
There were simply no matching PDFs.
That should not be treated like an error.

### `console.print(f"[yellow]No PDF files found in {path}[/yellow]")`
This is user-facing information, not a log.
It belongs in the command output.
The color choice communicates mild importance without implying failure.

### `raise typer.Exit(0)`
The command exits successfully because the operation itself worked.
“No matches” is a valid result.
This is a subtle but important design distinction.

### `table = Table(...)`
This begins the success display path.
Rich tables are presentation logic.
That belongs in the CLI, not in `find_pdfs()`.
This is a nice architecture lesson.

### `table.add_column(...)`
These lines define the shape of the output table.
They are purely about display.
Again, that reinforces the CLI’s role as a presentation layer.

### `for i, pdf in enumerate(pdfs, start=1):`
The CLI iterates over the discovered results.
It numbers them for readability.

### `size_kb = pdf.stat().st_size / 1024`
This is a neat use of `Path.stat()` to show human-friendly size information.
It adds useful context to the output without complicating the lower layer.

### `table.add_row(...)`
This converts each `Path` into display data.
Notice what is *not* happening.
The CLI is not changing discovery logic.
It is only formatting already-found results.

### Final `console.print(...)` lines
These present the table and the total count.
The command ends with a clear summary.
That is good command-line UX.

## 28. Common beginner mistakes
### Mistake 1: Building paths with string concatenation
This leads to brittle code and hides intent.
Use `Path` objects and `/` joining instead.

### Mistake 2: Assuming an existing path is the right kind of thing
A file is not a directory.
A directory is not a file.
Check both existence and type.

### Mistake 3: Forgetting that `glob()` is not recursive by default
Many beginners assume `*.pdf` will search everywhere.
It will not.
Recursion must be explicit.

### Mistake 4: Returning `[]` for every failure
An empty list can mean “valid directory with no PDFs.”
It should not also mean “path missing” or “wrong path type.”
Conflating these meanings makes debugging harder.

### Mistake 5: Catching `Exception` out of fear
This hides real bugs.
Catch specific exceptions you understand.
Let unexpected programming errors stay visible during development.

### Mistake 6: Using `print()` as permanent instrumentation
`print()` cannot express levels.
It cannot be filtered cleanly.
It does not integrate well with structured diagnostics.
Use logging for application behavior.

### Mistake 7: Using f-strings inside log calls everywhere
This works, but it gives up the standard parameterized logging pattern.
Prefer `%s`-style argument passing inside logger methods.

### Mistake 8: Forgetting explicit encodings
Text file code should name UTF-8 unless there is a strong reason otherwise.
Default encodings are environment-sensitive.
That leads to non-portable behavior.

### Mistake 9: Ignoring deterministic order
If your file discovery order is unstable, tests may flicker and users may see inconsistent output.
Sort results when order matters.
In this chapter, it does.

### Mistake 10: Putting business logic in the CLI
The scanner helper should discover files.
The CLI should render results and exit appropriately.
Mixing these responsibilities makes code harder to test and reuse.

## 29. Debugging guidance
### How to read a `FileNotFoundError`
A `FileNotFoundError` usually means the program tried to open or inspect a path that does not exist.
Read the path carefully first.
Typos are common.
Then ask where that path was constructed.
Was it user input, config, or derived from another path?

### How to read an `OSError`
`OSError` is a family of OS-related failures.
It can include permission issues, missing files, invalid operations, or other filesystem problems.
Do not stop at the exception class.
Read the message.
Read the path.
Read the operation that triggered it.

### How to read an `ImportError`
If paths are wrong in a Python project, sometimes the symptom appears as an import failure rather than a file failure.
Check whether your environment is activated.
Check whether the package is installed in editable mode.
Check your `pythonpath` test settings if needed.
Not every path-related bug looks like a path bug at first glance.

### Debugging a missing directory issue in this repo
Start by reproducing it with the exact CLI command.
Then inspect the `Path(directory)` conversion in the CLI.
Then inspect `find_pdfs()` precondition checks.
Then run the relevant test or create a minimal shell reproduction.
That is a disciplined path from symptom to cause.

### Debugging a wrong result count
If `find_pdfs()` returns fewer results than expected, ask:
- is recursion enabled?
- are extensions lowercase `.pdf`?
- is the directory correct?
- are files nested deeper than you assumed?
- did the pattern intentionally exclude them?

### Debugging log visibility
If a debug message does not appear, ask:
- was logging configured?
- what level was chosen?
- are you running with `--verbose`?
- is the message logged at `DEBUG` while the logger threshold is `INFO`?
Logging bugs are often configuration misunderstandings, not missing log calls.

## 30. Design tradeoffs
### Why use a built-in exception for directory validation?
Using `NotADirectoryError` keeps the code aligned with Python’s existing vocabulary.
It avoids inventing a custom exception where the built-in meaning is already good.
That is a sign of restraint.
Good design does not create custom types unnecessarily.

### Why also create custom exceptions elsewhere?
Because some failures are specific to the application domain.
“Empty search query” or “model not trained” are not well captured by a single built-in exception.
This is the balance.
Use built-ins when they fit.
Use custom types when the domain deserves its own language.

### Why sort results?
Sorting adds a tiny cost.
But it buys determinism, cleaner tests, predictable UI, and simpler reasoning.
That tradeoff is worth it for file discovery at this scale.

### Why keep logging configuration simple?
A large application might use dictConfig, JSON logs, multiple handlers, and environment-specific settings.
Week 2 uses `basicConfig` because it is enough right now.
This is a deliberate simplicity tradeoff.
You should not over-engineer early.
You should also not skip fundamentals.

### Why return `Path` objects instead of strings?
Returning `Path` objects keeps the richer API available downstream.
Callers can inspect names, stats, parents, and more without reconstructing objects.
The richer output type supports growth.

## 31. Testing implications
Testing file code can become messy fast.
Hard-coded directories are brittle.
Global machine state is unreliable.
That is why pytest’s `tmp_path` fixture matters so much.

### Why `tmp_path` is powerful
`tmp_path` gives each test an isolated temporary directory represented as a `Path` object.
Tests can create exactly the files and folders they need.
The OS handles cleanup.
The test remains independent of your real project folders.
That is excellent test hygiene.

### Why test both success and failure cases
A function contract includes both.
If you only test success, the failure shape becomes accidental.
In this chapter, failure shape matters a lot.
The right exception type is part of the API.

### Why test order
Humans trust stable output.
Tests also need stable output.
If the function promises sorted results, one test should make that promise explicit.
That is exactly what `test_returns_sorted_list` does.

### Why test idempotency
Setup helpers often run more than once.
If they fail on the second run, automation becomes brittle.
`ensure_dir()` therefore benefits from an idempotency test.
That test protects future refactors from accidentally removing `exist_ok=True`.

## 32. Architecture implications
### Why exceptions live in `core/`
The `core/` layer defines shared domain language and interfaces.
Exceptions are part of that shared language.
A service layer can raise `PaperNotFoundError` without knowing anything about CLI or storage implementation details.
That is exactly what you want.

### Why `core/` must stay independent
If `core/` imported `rich`, `sqlite`, or FastAPI concerns, every higher layer would be tangled with infrastructure choices.
That would make testing, reuse, and long-term maintenance harder.
Shared language belongs in the stable center.

### Where logging configuration belongs
Logging configuration is infrastructure.
It lives in `config/`, not in `core/`.
Core domain code may use loggers, but the actual configuration policy is an outer-layer concern.
That preserves dependency direction.

### Where CLI error translation belongs
The CLI is an application boundary.
That makes it the right place to turn exceptions into colored console messages and process exit codes.
The lower layer should not import Typer just to decide exit codes.
That would violate layering.

## 33. How this connects to ML and AI work
At first glance, paths, exceptions, and logging may feel far away from ML.
They are not.
ML systems are data pipelines.
Data pipelines are operational systems.
Operational systems live or die by input clarity, failure handling, and observability.

### Reproducible datasets need stable paths
If you cannot reliably locate your training files, you cannot reproduce a run.
Path discipline matters before any model is trained.

### Training loops need logging
When a model trains for minutes or hours, `print()` is not enough.
You need levels, timestamps, structured context, and the ability to reduce noise.
The habits you learn here scale directly.

### Data quality failures need named exceptions
An empty dataset, malformed label file, or missing feature cache should not all collapse into generic failure.
Named exceptions make ML pipelines safer and easier to debug.

### Encoding discipline matters for text ML
ResearchOps is likely to process paper text, notes, and metadata.
Encoding mistakes can corrupt training inputs or downstream search indexes.
That is not a small issue.
It is a data integrity issue.

## 34. Mini quizzes
### Quiz 1
What is the main advantage of using `Path` instead of raw strings for filesystem code?

**Answer:**
`Path` provides filesystem-aware methods and clearer semantics, making code safer and more expressive than manual string manipulation.

### Quiz 2
Why does `find_pdfs()` raise an exception for a missing directory instead of returning `[]`?

**Answer:**
Because “missing directory” is invalid input, while `[]` should mean “valid directory, no matching PDFs.”
Those are different meanings and should not be conflated.

### Quiz 3
What is the difference between `glob("*.pdf")` and `glob("**/*.pdf")`?

**Answer:**
The first searches only the current directory.
The second searches recursively through subdirectories.

### Quiz 4
Why is `ResearchOpsError` useful even though it does not add behavior itself?

**Answer:**
It creates a shared application-level exception family that callers can catch broadly when appropriate.

### Quiz 5
When should you prefer `log.warning(...)` over `log.error(...)`?

**Answer:**
Use `WARNING` when something unexpected happened but the program can continue safely.
Use `ERROR` when an important operation failed and deserves stronger attention.

### Quiz 6
Why is `%s` formatting preferred inside logger method calls?

**Answer:**
It follows the logging API’s parameterized style and avoids eager string interpolation when messages are filtered out.

### Quiz 7
What does `force=True` do in `logging.basicConfig(...)`?

**Answer:**
It overrides existing logging configuration so the application gets predictable behavior.

## 35. Explain-it-aloud prompts
Try answering these without looking at the code.
If you struggle, revisit the earlier sections.

1. Explain why a path object is more than a string.
2. Explain why `find_pdfs()` checks `.exists()` before `.is_dir()`.
3. Explain why sorted file output matters.
4. Explain why some exceptions store metadata attributes.
5. Explain why the CLI catches `NotADirectoryError` specifically.
6. Explain why `print()` is not a substitute for logging.
7. Explain what `DEBUG` means in this project.
8. Explain how `tmp_path` makes tests reliable.

## 36. What to memorize
Memorize these because they remove friction.

- `from pathlib import Path`
- `path.exists()`
- `path.is_dir()`
- `path.is_file()`
- `path.read_text(encoding="utf-8")`
- `path.write_text(text, encoding="utf-8")`
- `path.mkdir(parents=True, exist_ok=True)`
- `logging.getLogger(__name__)`
- `log.debug(...)`, `log.info(...)`, `log.warning(...)`, `log.error(...)`
- `pytest.raises(...)`

Also memorize the key command forms.

- `researchops scan <directory>`
- `researchops scan <directory> --recursive`
- `researchops --verbose scan <directory>`
- `python -m pytest tests/unit/test_paths.py -v`

Memorization is not the whole goal.
But some fluency speeds up deeper thinking.

## 37. What to understand deeply
Do not just memorize these.
Understand them.

- the semantic difference between invalid input and empty results,
- why API contracts include exception types,
- why deterministic output matters,
- why architecture boundaries determine where errors are translated,
- why explicit encoding is a portability decision,
- why logging is about observability, not decoration,
- and why narrow exception handling protects debugging quality.

These are durable ideas.
They will matter long after the exact function names fade.

## 38. What not to worry about yet
Do not worry yet about advanced logging backends.
Do not worry yet about JSON log aggregators.
Do not worry yet about every possible filesystem edge case on every operating system.
Do not worry yet about async file I/O or process pools.
Do not worry yet about complex parser recovery logic.
Those topics will matter later.
Right now, you are building clean fundamentals.

## 38b. PowerShell equivalents for Windows learners
All commands in this chapter are written in macOS/Linux shell syntax.
On Windows with PowerShell, substitute the following.

Activate the environment:
```powershell
.venv\Scripts\Activate.ps1
```

All other commands in this chapter — `python -m pip install`, `pytest`, `ruff check`, `researchops scan`, and `researchops --verbose scan` — are identical on Windows PowerShell.

For path arguments, both forward slashes and backslashes work:
```powershell
researchops scan examples\sample_papers
researchops scan examples/sample_papers
```

To check the exit code of the last command:
```powershell
echo $LASTEXITCODE
```

On macOS/Linux the equivalent is:
```bash
echo $?
```

If `Activate.ps1` is blocked by execution policy, run this once in PowerShell as administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```



## 39. Bridge to next week
This week gives you safe input handling and visible behavior.
Next week gives you richer internal models.
Once you can find files reliably, you need a better way to represent what those files mean.
That is where object-oriented design and domain modeling enter.
You will move from “I found these PDF paths” to “I can represent a paper as a meaningful Python object.”
That step only works well if the Week 2 foundation is solid.

## 40. Final chapter summary
A serious program does not just succeed.
It succeeds clearly and fails clearly.
`Path` makes filesystem code readable and robust.
Custom exceptions give failures names and structure.
Logging gives the application a memory of what it did.
Tests turn these promises into something enforceable.
That is what Week 2 is really teaching.
It is not only about files, errors, and logging.
It is about learning to design software that can be trusted.
