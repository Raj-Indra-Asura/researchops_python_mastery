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
- `src/researchops/files.py`
- `src/researchops/logging_config.py`
- `src/researchops/scanner.py`
- `tests/unit/test_files.py`
- `tests/unit/test_scanner.py`
- `tests/unit/test_logging_config.py`

## Concepts covered
`pathlib`, file encodings, recursion, `try/except/else/finally`, custom exceptions, log levels, and defensive programming.

## Expected deliverables
- A scanner that accepts a root directory and finds files.
- Logging configuration that prints useful messages.
- Exceptions that include context such as path and failure reason.
- Tests for empty directories, missing directories, and unsupported files.

## Definition of done
- [ ] All path operations use `Path`.
- [ ] Scanner handles missing paths gracefully.
- [ ] Unsupported extensions are skipped deliberately.
- [ ] Logging has at least INFO and ERROR paths.
- [ ] Custom exceptions are meaningful.
- [ ] Unit tests cover success and failure cases.
- [ ] Manual run against `examples/` produces readable output.
- [ ] No broad `except Exception` without a reason.
- [ ] Debug notes capture one real failure you traced.
