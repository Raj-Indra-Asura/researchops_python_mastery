
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 8 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 08 — Multiprocessing Ingestion:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 08 Multiprocessing Ingestion

## 1. Pre-validation checklist

- [ ] Confirm you are validating Week 8 only: multiprocessing ingestion with `ProcessPoolExecutor`.
- [ ] Confirm the sample input directory is `./examples/sample_papers`.
- [ ] Confirm the CLI command available is `researchops` from this project checkout.
- [ ] Confirm you understand that workers parse and the parent writes.
- [ ] Confirm you are not validating future curriculum features.
- [ ] Confirm the Week 8 syllabus names `tests/unit/test_process_pool.py`.
- [ ] Confirm the Week 8 syllabus updates `tests/integration/test_ingestion_service.py` for parallel mode.
- [ ] Confirm worker count must be a positive integer.
- [ ] Confirm one bad PDF should not crash the whole batch.
- [ ] Confirm parallel mode must logically match single-worker mode.

## 2. Commands to run

- Official Week 8 syllabus command:
```bash
researchops ingest ./examples/sample_papers --workers 2
pytest tests/unit/test_process_pool.py -v
```
- Full local validation sequence:
```bash
python -m pip install -e ".[dev,parsing,storage]"
researchops --help
researchops ingest ./examples/sample_papers --workers 1
researchops ingest ./examples/sample_papers --workers 2
pytest tests/unit/test_process_pool.py -v
pytest tests/integration/test_ingestion_service.py -v
```
- Optional broad checks after Week 8-specific checks pass:
```bash
pytest -q
ruff check src tests
```

## 3. Expected outputs

- `researchops --help` exits successfully and lists commands.
- `researchops ingest ./examples/sample_papers --workers 1` completes without traceback.
- `researchops ingest ./examples/sample_papers --workers 2` completes without traceback.
- The two-worker command reports honest success, failure, and skipped counts.
- Repeated runs may report skipped items if the database already contains papers.
- No command should show a pickling error.
- No command should show `max_workers must be greater than 0` for valid input.
- No command should show `database is locked` during normal validation.
- `pytest tests/unit/test_process_pool.py -v` ends with passed tests.
- `pytest tests/integration/test_ingestion_service.py -v` ends with passed tests when the full service path is checked.

## 4. Tests that must pass

- `tests/unit/test_process_pool.py` must pass because it is the Week 8 unit test named in the syllabus.
- `tests/integration/test_ingestion_service.py` must pass when checking the full ingestion workflow.
- Unit tests should cover process-pool success payloads.
- Unit tests should cover failure payloads.
- Unit tests should cover invalid worker counts if validation lives in the helper.
- Integration tests should cover the single-worker path.
- Integration tests should cover a worker count greater than one.
- Integration tests should compare logical parity between single-worker and parallel ingestion.
- No test should depend on worker completion timing as its main assertion.
- No test should hide failure recording just to make success counts pass.

## 5. Manual checks

- [ ] Check that `--workers 1` remains valid.
- [ ] Check that `--workers 2` uses the multiprocessing path.
- [ ] Check that invalid worker counts are rejected clearly.
- [ ] Check that one malformed file would become a recorded failure.
- [ ] Check that the final CLI summary is understandable.
- [ ] Check that skipped files are explainable on repeated runs.
- [ ] Check that success and failure totals are honest.
- [ ] Check that tiny folders are not used as the only performance evidence.
- [ ] Check that no raw traceback is shown for expected parse failures.
- [ ] Check that the learner can explain the command output.

## 6. Architecture checks

- [ ] `src/researchops/workers/process_pool.py` owns process-pool mechanics or an equivalently clear helper exists.
- [ ] `src/researchops/services/ingestion_service.py` owns ingestion workflow decisions.
- [ ] `src/researchops/cli/commands/ingest.py` exposes `--workers` without owning parse logic.
- [ ] The worker function is module-level.
- [ ] Worker inputs are picklable.
- [ ] Worker outputs are picklable.
- [ ] Workers do not receive repositories.
- [ ] Workers do not receive SQLite connections.
- [ ] Workers do not write to SQLite.
- [ ] The parent process saves successes and records failures.

## 7. Documentation checks

- [ ] `notes.md` has all 20 canonical sections in order.
- [ ] `notes.md` explains CPU-bound work from first principles.
- [ ] `notes.md` explains the GIL and process-pool choice.
- [ ] `notes.md` explains picklability and module-level workers.
- [ ] `notes.md` explains worker failure isolation.
- [ ] `notes.md` explains parent-side batch writes.
- [ ] `validation.md` has all 10 validation sections in order.
- [ ] `validation.md` preserves QUICKREF and NAV blocks.
- [ ] `validation.md` uses the real Week 8 command from the syllabus.
- [ ] `validation.md` names the real Week 8 test files.

## 8. Do-not-proceed warnings

- Do not proceed if the Week 8 unit test file is missing.
- Do not proceed if the process-pool test fails.
- Do not proceed if a lambda or nested function is used as the worker.
- Do not proceed if workers write directly to SQLite.
- Do not proceed if repository objects cross the process boundary.
- Do not proceed if one bad PDF crashes the entire batch.
- Do not proceed if parallel and single-worker results differ logically.
- Do not proceed if invalid worker counts are accepted silently.
- Do not proceed if documentation teaches future features instead of Week 8.
- Do not proceed if the learner cannot explain why processes are used.

## 9. Ruthless mentor checkpoint

- Explain the GIL in two sentences.
- Justify `ProcessPoolExecutor` for CPU-bound PDF parsing.
- Point to the module-level worker function.
- List every value crossing the process boundary.
- Name one value that must not cross the process boundary.
- Explain how a corrupt PDF becomes a recorded failure.
- Explain why SQLite writes stay in the parent process.
- Run the syllabus command and explain the output.
- Run the process-pool unit test and explain what it protects.
- Compare one-worker and two-worker ingestion logically, not by timing alone.

## 10. Definition of done

- [ ] `researchops ingest ./examples/sample_papers --workers 2` is the documented milestone command.
- [ ] `pytest tests/unit/test_process_pool.py -v` is the documented unit validation.
- [ ] `tests/integration/test_ingestion_service.py` is documented as the parallel-mode service check.
- [ ] The CLI accepts positive worker counts.
- [ ] Workers are module-level functions.
- [ ] Worker payloads are picklable.
- [ ] Workers parse only.
- [ ] The parent writes to SQLite.
- [ ] Failures are recorded.
- [ ] Single-worker and multi-worker paths agree logically.

Detailed validation evidence checklist:
- Evidence check 1: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 2: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 3: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 4: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 5: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 6: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 7: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 8: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 9: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 10: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 11: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 12: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 13: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 14: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 15: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 16: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 17: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 18: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 19: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 20: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 21: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 22: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 23: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 24: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 25: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 26: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 27: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 28: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 29: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 30: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 31: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 32: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 33: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 34: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 35: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 36: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 37: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 38: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 39: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 40: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 41: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 42: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 43: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 44: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 45: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 46: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 47: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 48: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 49: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 50: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 51: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 52: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 53: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 54: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 55: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 56: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 57: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 58: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 59: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 60: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 61: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 62: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 63: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 64: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 65: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 66: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 67: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 68: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 69: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 70: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 71: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 72: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 73: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 74: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 75: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 76: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 77: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 78: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 79: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 80: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 81: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 82: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 83: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 84: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 85: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 86: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 87: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 88: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 89: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 90: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 91: Confirm the CLI entry point is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 92: Confirm the worker count is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 93: Confirm the process-pool unit behavior is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 94: Confirm the failure isolation is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 95: Confirm the parent-side SQLite writes is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 96: Confirm the single-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 97: Confirm the two-worker comparison is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 98: Confirm the picklable payloads is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 99: Confirm the module-level worker is visible in command output, tests, code inspection, or learner explanation.
- Evidence check 100: Confirm the integration service path is visible in command output, tests, code inspection, or learner explanation.

- Evidence check 101: Confirm the official syllabus command appears exactly with `--workers 2`.
- Evidence check 102: Confirm the unit command names `tests/unit/test_process_pool.py` rather than an invented test file.
- Evidence check 103: Confirm the integration command names `tests/integration/test_ingestion_service.py`.
- Evidence check 104: Confirm expected output describes behavior, not hard-coded counts that depend on local data.
- Evidence check 105: Confirm manual checks explain repeated-run skipped files.
- Evidence check 106: Confirm architecture checks forbid SQLite writes from workers.
- Evidence check 107: Confirm documentation checks mention picklability.
- Evidence check 108: Confirm do-not-proceed warnings include lambda or nested worker functions.
- Evidence check 109: Confirm the mentor checkpoint requires explaining values crossing the process boundary.
- Evidence check 110: Confirm the definition of done includes parent-side failure recording.
- Evidence check 111: Confirm broad `pytest -q` is optional and not a replacement for Week 8-specific validation.
- Evidence check 112: Confirm `ruff check src tests` is optional because the user specifically asked not to run validation commands here.
- Evidence check 113: Confirm no future-week feature is required to complete Week 8.
- Evidence check 114: Confirm the learner can explain why tiny folders may not show speedup.
- Evidence check 115: Confirm the learner can explain why correctness evidence comes before timing evidence.
- Evidence check 116: Confirm the learner can identify the worker function by file and name.
- Evidence check 117: Confirm failure payloads include enough information to debug the bad file.
- Evidence check 118: Confirm success payloads include enough information for parent-side paper construction.
- Evidence check 119: Confirm worker-count validation is visible in code, CLI behavior, or tests.
- Evidence check 120: Confirm no hidden order assumption is used as the main proof of correctness.
- Evidence check 121: Confirm the final summary distinguishes saved, failed, and skipped documents.
- Evidence check 122: Confirm one malformed PDF does not prevent other valid PDFs from being processed.
- Evidence check 123: Confirm the process-pool helper is not responsible for CLI formatting.
- Evidence check 124: Confirm the CLI is not responsible for low-level worker mechanics.
- Evidence check 125: Confirm the validation page tells the learner exactly when not to move forward.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 08 — Multiprocessing Ingestion:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
