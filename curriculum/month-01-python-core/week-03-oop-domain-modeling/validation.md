# Week 03 Validation - Exact Checkpoint
## Purpose
Use this checklist only after you have studied the chapter.
The goal is to verify both code understanding and environment setup.
Because this week is about domain models, your validation should combine reading, test execution, and concept recall.
## Exact shell commands
Run these commands from the repository root.
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest tests/unit/test_models.py -v
pytest tests/unit/test_value_objects.py -v
pytest -q
python - <<'PY'
from pathlib import Path
notes = Path("curriculum/month-01-python-core/week-03-oop-domain-modeling/notes.md")
line_count = len(notes.read_text().splitlines())
print(f"notes.md lines: {line_count}")
assert 800 <= line_count <= 1500, "notes.md must stay within the chapter target range"
PY
```
## What each command proves
- `python -m venv .venv` creates an isolated environment for the course.
- `source .venv/bin/activate` ensures you are using that environment.
- `python -m pip install --upgrade pip` prevents avoidable installer issues.
- `python -m pip install -e ".[dev]"` installs the package and the test tooling.
- `pytest tests/unit/test_models.py -v` validates core model behavior.
- `pytest tests/unit/test_value_objects.py -v` validates value object invariants.
- `pytest -q` checks that your broader test suite still passes.
- the embedded Python snippet verifies the chapter notes stay at the intended textbook scale.
## Expected test themes
When the tests pass, you should have confirmed behavior such as:
- `Paper.word_count()` returns the number of whitespace-separated words
- `Paper.is_empty()` treats whitespace-only text as empty
- `Paper.tags` does not leak shared mutable state between instances
- `PaperId.from_path()` is stable for the same path
- `str(PaperId(...))` returns the raw identifier value
- `ParsedDocument.is_empty()` correctly handles blank raw text
- `FailedDocument.summary()` includes the error type and filename
- `IngestionResult.total` counts successes, failures, and skipped files together
- `IngestionResult.success_rate` returns `0.0` when nothing was processed
- `Query` rejects invalid empty input
- `Tag` normalises tag text consistently
## Exact reading checks
Open these files and confirm you can answer what each one contributes:
```bash
sed -n '1,220p' src/researchops/core/models.py
sed -n '1,220p' src/researchops/core/value_objects.py
sed -n '1,220p' tests/unit/test_models.py
sed -n '1,220p' tests/unit/test_value_objects.py
```
After reading, answer these questions without looking back:
1. Why is `PaperId` frozen?
2. Why is `Paper.source_path` stored as a string?
3. Why is `ParsedDocument` separate from `Paper`?
4. Why does `IngestionResult` use properties for `total` and `success_rate`?
5. Why does `Tag` normalise its value during construction?
## Strict completion checklist
Do not mark an item done unless you can explain it aloud.
- [ ] I created or activated the project virtual environment.
- [ ] I installed the editable package with dev dependencies.
- [ ] I ran `pytest tests/unit/test_models.py -v` successfully.
- [ ] I ran `pytest tests/unit/test_value_objects.py -v` successfully.
- [ ] I ran `pytest -q` successfully.
- [ ] I confirmed that `notes.md` stays within the chapter line-count target.
- [ ] I can define `class`, `instance`, `attribute`, and `method`.
- [ ] I can explain what `@dataclass` generates.
- [ ] I can explain why `field(default_factory=list)` prevents shared state bugs.
- [ ] I can explain why `PaperId`, `Query`, and `Tag` are value objects.
- [ ] I can explain why `Paper` is the main Week 3 entity.
- [ ] I can explain `__post_init__`, `@property`, `__str__`, and `StrEnum`.
- [ ] I can explain why `core/` must not import from `storage/`, `cli/`, or `api/`.
- [ ] I can describe the ingestion pipeline using the correct domain nouns.
## Failure signals
Stop and review the chapter if any of these are true:
- you can run the tests but cannot explain what they protect
- you think `frozen=True` is only about style
- you still want to replace `IngestionResult` with a tuple of three lists
- you are unsure why mutable defaults are dangerous
- you are unsure whether `Query` should allow blank strings
- you cannot explain why a domain model is different from a transport dictionary
## Final pass condition
You pass Week 3 validation when both statements are true:
1. The commands succeed.
2. You can explain the design decisions behind the code without reading from the file.
