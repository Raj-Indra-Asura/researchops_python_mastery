# Week 02 - Files, Errors, and Logging

## Learning objectives
- Use `pathlib.Path` instead of manual string path building.
- Read and write text files safely with explicit encodings.
- Scan directories recursively and filter supported file types.
- Raise, catch, and re-raise exceptions intentionally.
- Introduce structured logging for normal events and failures.
- Distinguish between recoverable errors and fatal configuration problems.
- Build a directory scanner that returns useful results instead of crashing.

## Project milestone
Implement a file-system scanner that walks a papers directory, discovers candidate documents, and logs what was accepted, skipped, or failed.

## Files to modify/create
- `src/researchops/utils/paths.py`
- `src/researchops/config/logging.py`
- `src/researchops/core/exceptions.py`
- `tests/unit/test_paths.py`
- `tests/unit/test_exceptions.py`

## Concepts covered
`pathlib`, file encodings, recursion, `try/except/else/finally`, custom exceptions, log levels, and defensive programming.

## Expected deliverables
- `utils/paths.py` with `find_pdfs()`, `ensure_dir()`, and `safe_resolve()` fully tested.
- `config/logging.py` with `configure_logging()` and `get_logger()`.
- `core/exceptions.py` with a `ResearchOpsError` base and specific sub-classes for parsing and file-system errors.
- Tests for empty directories, missing directories, non-directory paths, and unsupported file types.

## Definition of done
- [ ] All path operations use `Path`.
- [ ] `find_pdfs()` handles missing paths, non-directories, and empty directories gracefully.
- [ ] Unsupported extensions are not returned by the scanner.
- [ ] Logging has at least INFO and ERROR code paths.
- [ ] Custom exceptions are sub-classes of `ResearchOpsError`.
- [ ] Unit tests cover success and failure cases.
- [ ] Manual run of `researchops scan examples/sample_papers` produces readable output.
- [ ] No broad `except Exception` without a re-raise or explicit reason.
- [ ] Debug notes capture one real failure you traced.
