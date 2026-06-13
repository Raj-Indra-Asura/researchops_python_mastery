
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 3 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)

**Week 03 — OOP and Domain Modeling:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Week 03 Validation - Exact Checkpoint

## Purpose
Use this checklist only after you have studied the chapter.
The goal is to verify both code understanding and environment setup.
Because this week is about domain models, your validation should combine reading, test execution, and concept recall.

---

## Pre-validation checklist

Before running the formal checks, confirm all of these are true.

- [ ] You are in the repository root.
- [ ] You are using Python 3.11 or newer.
- [ ] Your virtual environment is created and activated.
- [ ] The package has been installed with `-e ".[dev]"`.
- [ ] You have read `src/researchops/core/models.py` at least once, not just skimmed it.
- [ ] You have read `src/researchops/core/value_objects.py` at least once.
- [ ] You can point to the definition of `PaperId`, `Paper`, `ParsedDocument`, `FailedDocument`, and `IngestionResult`.
- [ ] You know what `frozen=True` does to a dataclass.
- [ ] You know what `field(default_factory=list)` prevents.
- [ ] You are ready to explain design decisions, not just recite class names.

---

## Commands to run

Run these commands from the repository root, in order.

### 1. Environment setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Windows PowerShell equivalent for activation:
```powershell
.venv\Scripts\Activate.ps1
```

### 2. Confirm the package imports cleanly

```bash
python -c "from researchops.core.models import Paper, PaperId, ParsedDocument, FailedDocument, IngestionResult; print('models ok')"
python -c "from researchops.core.value_objects import Query, Tag; print('value objects ok')"
```

Expected output for each command:
```text
models ok
value objects ok
```

Any `ImportError` here means the environment is not set up correctly or a module has a syntax error.

### 3. Quick REPL smoke test

This command uses `python -c` so the same smoke test works in Windows PowerShell, Command Prompt, macOS, and Linux.

```text
python -c "from pathlib import Path; from researchops.core.models import Paper, PaperId; pid = PaperId.from_path(Path('sample.pdf')); print('PaperId:', pid); print('Type:', type(pid).__name__); paper = Paper(id=str(pid), title='Test Paper', source_path='sample.pdf', text='hello world from a test', num_pages=1, file_size_bytes=512); print('word_count:', paper.word_count()); print('is_empty:', paper.is_empty())"
```

Expected output (exact hash will differ):
```text
PaperId: <16-character hex string>
Type: PaperId
word_count: 5
is_empty: False
```

If `word_count` returns a wrong value or `is_empty` returns `True`, your understanding of the method logic needs review.

### 4. Run domain model unit tests

```bash
pytest tests/unit/test_models.py -v
```

Expected result:
- all tests in `TestPaper`, `TestPaperId`, `TestParsedDocument`, `TestFailedDocument`, and `TestIngestionResult` pass.
- no failures.
- no errors.

Read the test names as you watch them run. Each name describes a specific behavioral promise.

### 5. Run value object unit tests

```bash
pytest tests/unit/test_value_objects.py -v
```

Expected result:
- all tests for `Query` and `Tag` pass.
- no failures.
- no errors.

### 6. Combined fast check

```bash
pytest tests/unit/test_models.py tests/unit/test_value_objects.py -q
```

Expected result:
- all tests pass.
- the summary line shows only passes.

### 7. Full suite check

```bash
pytest -q
```

Expected result:
- the full current test suite passes.
- no regressions from any other test file.

### 8. Linting check

```bash
ruff check src tests
```

Expected result:
- no issues, or only pre-existing issues unrelated to your Week 3 work.

---

## Expected outputs
Use these outputs as the pass/fail contract.

- The import check prints `models ok` and `value objects ok`.
- The REPL smoke test prints a 16-character `PaperId`, `Type: PaperId`, `word_count: 5`, and `is_empty: False`.
- `pytest tests/unit/test_models.py -v` collects and passes `14` tests.
- `pytest tests/unit/test_value_objects.py -v` collects and passes `20` tests.
- The combined model/value-object check passes `34` tests.
- `pytest -q` completes with all currently available tests passing.
- `ruff check src tests` reports no issues introduced by your work.

## Tests that must pass

### TestPaper

- `word_count()` correctly counts space-separated words.
- `is_empty()` returns `True` only for blank or whitespace-only text.
- `tags` defaults to an empty list.
- `created_at` defaults to a `datetime` value.

### TestPaperId

- `from_path()` produces a stable identifier for the same path.
- `str(PaperId(...))` returns the raw hex string, not the dataclass representation.
- `PaperId` produces different identifiers for different paths.

### TestParsedDocument

- `is_empty()` detects whitespace-only text correctly.
- `ParsedDocument` accepts `Path` objects for `source_path`.

### TestFailedDocument

- `summary()` returns a string containing the error type and filename.
- The `FailedDocument` stores both `error_message` and `error_type`.

### TestIngestionResult

- `total` is computed from current lists, not a stored integer.
- `success_rate` returns `0.0` for an empty result.
- `total` counts successes, failures, and skipped paths in one number.

---

## Manual checks

Open these files and confirm you can answer what each one contributes.

```bash
sed -n '1,60p' src/researchops/core/models.py
sed -n '1,60p' src/researchops/core/value_objects.py
```

After reading, answer these questions without looking back.

1. Why is `PaperId` frozen?
2. Why is `Paper.source_path` stored as a `str` instead of a `Path`?
3. Why is `ParsedDocument` separate from `Paper`?
4. Why does `IngestionResult` use `@property` for `total` and `success_rate`?
5. Why does `Tag` normalise its value during construction?
6. Why does `Query` validate in `__post_init__`?
7. Which domain class is the primary entity of the system?
8. What is the difference between `FailedDocument` and a logged error message?
9. What does `field(default_factory=list)` prevent?
10. What would happen if `core/models.py` imported from `cli/main.py`?

---

## Architecture checks

Domain models should live in `core/` and must not import infrastructure.

- [ ] `core/models.py` does not import `cli`, `storage`, `api`, or `ml` modules.
- [ ] `core/value_objects.py` does not import infrastructure code.
- [ ] The exception hierarchy is also in `core/` and follows the same rule.
- [ ] The domain objects are testable without a CLI, database, or API running.

If any architecture check fails, you have introduced a coupling that will make future layers harder to build.

---

## Documentation checks
- [ ] Week 3 notes explain classes, dataclasses, value objects, and entities before using them in ResearchOps examples.
- [ ] Week 3 exercises include code-reading, implementation, testing, debugging, written, stretch, brutal, mini-project, and completion-checklist work.
- [ ] Break-it experiments are restored before validation starts.
- [ ] Reflection answers are your own prompts and observations, not copied solutions.

## Manual checks

Do these even if all tests pass.

- [ ] I can explain class versus instance without reading the notes.
- [ ] I can explain what `@dataclass` generates.
- [ ] I can explain why mutable defaults are dangerous and what fixes them.
- [ ] I can explain the difference between an entity and a value object.
- [ ] I can explain why `PaperId` is frozen and `IngestionResult` is not.
- [ ] I can trace the pipeline from `Path` to `ParsedDocument` to `Paper` or `FailedDocument` to `IngestionResult`.
- [ ] I can explain why composition beats inheritance for `IngestionResult`.
- [ ] I can explain `__post_init__` and give one example from the project.
- [ ] I can explain `@property` and give one example from the project.
- [ ] I can explain why `str(PaperId(...))` is cleaner than the default `repr`.

---

## Failure signals

Stop and review the chapter if any of these are true.

- You can run the tests but cannot explain what they protect.
- You think `frozen=True` is only a style preference.
- You still want to replace domain models with plain dictionaries.
- You are unsure why `field(default_factory=list)` is not the same as `= []`.
- You cannot explain why `IngestionResult.total` is a property.
- You cannot explain the difference between `ParsedDocument` and `Paper`.
- You cannot explain why `core/` must stay independent.
- You cannot trace the pipeline from file path to ingestion result.

---

## Do-not-proceed warnings

Do **not** move to Week 4 if any of these are true.

- [ ] You cannot explain class, instance, attribute, and method.
- [ ] You cannot explain what `@dataclass` generates.
- [ ] You do not understand why mutable defaults are a bug.
- [ ] You cannot explain value object versus entity.
- [ ] You cannot explain the Week 3 pipeline in one spoken paragraph.
- [ ] You cannot describe why `core/` must not import infrastructure code.
- [ ] You cannot run the domain model tests and explain what they prove.

---

## Ruthless mentor checkpoint
Answer these aloud without looking at the code.

1. Why is `PaperId` a value object instead of a plain string everywhere?
2. Why does `Paper.word_count()` compute from `text` instead of storing a separate number?
3. What bug does `field(default_factory=list)` prevent?
4. Why is `ParsedDocument` not the same thing as `Paper`?
5. Why should core domain models stay independent from interface and storage code?

## Definition of done

You pass Week 3 validation when both statements are true:
1. The commands succeed.
2. You can explain the design decisions behind the code without reading from the file.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 03 — OOP and Domain Modeling:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 1: Python Core and Project Foundation](../README.md)
---
<!-- NAV_BOTTOM_END -->
