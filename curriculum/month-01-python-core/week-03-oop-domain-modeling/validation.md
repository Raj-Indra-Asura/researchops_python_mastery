# Week 03 Validation - Exact Checkpoint

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 1](../README.md) › [Week 3 — OOP & Domain Modeling](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

## Exact shell commands

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

```bash
python - <<'PY'
from pathlib import Path
from researchops.core.models import Paper, PaperId

pid = PaperId.from_path(Path("sample.pdf"))
print("PaperId:", pid)
print("Type:", type(pid).__name__)

paper = Paper(
    id=str(pid),
    title="Test Paper",
    source_path="sample.pdf",
    text="hello world from a test",
    num_pages=1,
    file_size_bytes=512,
)
print("word_count:", paper.word_count())
print("is_empty:", paper.is_empty())
PY
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

## What each test class protects

### TestPaper

- `word_count()` correctly counts space-separated words.
- `is_empty()` returns `True` only for blank or whitespace-only text.
- `tags` does not leak shared mutable state between instances.
- `Paper` stores `source_path` as a `str`, not a `Path` object.

### TestPaperId

- `from_path()` produces a stable identifier for the same path.
- `str(PaperId(...))` returns the raw hex string, not the dataclass representation.
- `PaperId` is frozen and raises an error on mutation attempt.

### TestParsedDocument

- `is_empty()` detects whitespace-only text correctly.
- `ParsedDocument` accepts `Path` objects for `source_path`.

### TestFailedDocument

- `summary()` returns a string containing the error type and filename.
- The `FailedDocument` stores both `error_message` and `error_type`.

### TestIngestionResult

- `total` is computed from current lists, not a stored integer.
- `success_rate` returns `0.0` for an empty result.
- `success_rate` returns `0.5` for one success and one failure.
- `total` updates automatically when successes or failures are appended.

---

## Reading checks

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

## Manual concept checks

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

## Final pass condition

You pass Week 3 validation when both statements are true:
1. The commands succeed.
2. You can explain the design decisions behind the code without reading from the file.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 1 — Python Core and Project Foundation · **Week 3 — OOP & Domain Modeling** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 4](../../../curriculum/month-01-python-core/week-04-cli-packaging/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 4 — CLI & Packaging](../../../curriculum/month-01-python-core/week-04-cli-packaging/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 1 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 1 overview](../README.md) · [📄 Week 3 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
