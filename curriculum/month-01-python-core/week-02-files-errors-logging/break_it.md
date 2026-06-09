# Break It - Week 02 Files, Errors, and Logging

## Intentional failure experiments
1. Pass a file path where your scanner expects a directory. Confirm the custom exception message is specific.
2. Point the scanner at a missing directory and decide whether it should return an empty result or fail loudly.
3. Drop a `.txt` file, a hidden file, and a zero-byte file into the sample directory and inspect behavior.
4. Force a logging format typo or invalid config and see how early startup failures appear.
5. Read a file with the wrong encoding and capture the exception details.

## Debugging tasks
- Run only the scanner tests with `pytest -k scanner -v`.
- Add temporary DEBUG logs that print each visited path.
- Compare `Path.iterdir()` and `Path.rglob()` on the same directory.

## Edge cases to explore
- Empty directory.
- Deeply nested folder tree.
- Duplicate file names in different folders.
- Files with uppercase extensions like `.PDF`.

## What did you learn?
- Which failure should be a warning instead of an error?
- What context belongs in an exception message?
- How will you keep logs useful without making them noisy?
