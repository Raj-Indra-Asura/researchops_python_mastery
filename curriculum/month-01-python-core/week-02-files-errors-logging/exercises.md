# Exercises - Week 02 Files, Errors, and Logging

## Warm-up exercises
1. Create a `Path` to `examples/sample_papers` and print whether it exists.
2. Write a function that returns all `.pdf` files in a directory.
3. Catch `FileNotFoundError` when reading a missing text file.
4. Configure a logger and emit one INFO and one ERROR message.

## Project exercises
1. Implement `scan_directory(root: Path)` that returns discovered document paths.
2. Add validation that rejects non-directories and missing paths.
3. Log counts for scanned, accepted, skipped, and failed files.
4. Write tests for empty directories, nested directories, and unsupported extensions.

## Stretch exercises
1. Add a `--verbose` flag that switches logging to DEBUG.
2. Write a custom exception carrying both a path and a message.
3. Record scan duration with `time.perf_counter()` and log it.

## Writing questions
1. When should code skip a failure versus stop immediately?
2. Which exception types did you actually encounter?
3. How did logging help more than `print()`?
4. What path handling mistake are you least likely to repeat now?
