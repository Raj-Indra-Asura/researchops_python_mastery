# Exercises - Week 02 Files, Errors, and Logging

## Warm-up exercises
1. Create a `Path` to `examples/sample_papers` and print whether it exists.
2. Call `find_pdfs(path)` from `researchops.utils.paths` and print the count.
3. Catch `NotADirectoryError` when calling `find_pdfs` with a missing path.
4. Call `configure_logging()` from `researchops.config.logging` and emit one INFO and one ERROR message using `get_logger(__name__)`.

## Project exercises
1. Study `src/researchops/utils/paths.py`. Add a test in `tests/unit/test_paths.py` for the case where `find_pdfs` is called with a file path instead of a directory — confirm it raises `NotADirectoryError`.
2. Study `src/researchops/core/exceptions.py`. Add a new exception `ScanDirectoryError(ResearchOpsError)` with a constructor that stores the `path` and a human-readable `reason`. Write a test in `tests/unit/test_exceptions.py`.
3. Log counts for scanned, accepted, and skipped files using `get_logger(__name__)` at INFO level.
4. Write a test that confirms `find_pdfs` returns an empty list for an empty directory and a sorted list for a directory with PDFs.

## Stretch exercises
1. Add a `--verbose` flag to `researchops scan` that enables DEBUG logging (the CLI already has `--verbose` on the root app — trace how it reaches `configure_logging()`).
2. Add `ensure_dir(path)` to `utils/paths.py` if it is not already there: it creates a directory and its parents, returns the path, and is idempotent.
3. Record scan duration with `time.perf_counter()` and log it at INFO level.

## Writing questions
1. When should code skip a failure versus stop immediately?
2. Which exception types did you actually encounter?
3. How did logging help more than `print()`?
4. What path handling mistake are you least likely to repeat now?
