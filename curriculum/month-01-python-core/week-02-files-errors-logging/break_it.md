# Break It - Week 02 Files, Errors, and Logging

## Intentional failure experiments
1. Call `find_pdfs()` with a file path (not a directory) and confirm the `NotADirectoryError` message contains the actual path.
2. Call `find_pdfs()` on a missing directory and decide: is `NotADirectoryError` the right signal? Read the code in `utils/paths.py` and explain why it was chosen.
3. Drop a `.txt` file, a hidden file (`.hidden.pdf`), and a zero-byte `.pdf` into a temp directory and observe which ones `find_pdfs()` returns.
4. Force a logging format typo in `configure_logging()` call and see how early startup failures appear.
5. Read a file using the wrong encoding (`latin-1` instead of `utf-8`) and capture the `UnicodeDecodeError`.

## Debugging tasks
- Run only the path tests with `pytest tests/unit/test_paths.py -v`.
- Add a temporary `log.debug("visiting %s", path)` line inside `find_pdfs` and run `researchops --verbose scan examples/sample_papers` to see it.
- Compare `Path.glob("*.pdf")` and `Path.rglob("*.pdf")` results on the same directory to understand `recursive=True`.

## Edge cases to explore
- Empty directory.
- Deeply nested folder tree (3+ levels).
- Duplicate PDF names in different sub-folders.
- Files with uppercase extensions like `.PDF` — does `glob("*.pdf")` catch them? (Hint: test it on your OS. On case-sensitive Linux filesystems it will not match `.PDF`. On macOS with HFS+ it may. This is why production code normalises extensions before filtering.)

## What did you learn?
- Which failure should be a warning instead of an error?
- What context belongs in an exception message?
- How will you keep logs useful without making them noisy?
