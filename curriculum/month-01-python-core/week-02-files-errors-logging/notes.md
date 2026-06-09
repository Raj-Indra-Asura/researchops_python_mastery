# Notes - Week 02 Files, Errors, and Logging

Programs that touch the file system fail in more ways than simple in-memory code. Paths can be missing, files can have the wrong extension, permissions can be wrong, and text can be encoded differently than you expected. The goal this week is not to eliminate all failures. The goal is to make failures understandable.

Use `pathlib.Path` instead of string concatenation for paths. `Path` objects know how to join segments correctly across operating systems and give you helpful methods like `.exists()`, `.is_file()`, `.suffix`, and `.rglob()`.

```python
from pathlib import Path

root = Path("examples/sample_papers")
for pdf_path in root.rglob("*.pdf"):
    print(pdf_path.name)
```

Compare that to hand-building paths like `root + "/papers/" + name`, which is more fragile and harder to read.

When reading text, be explicit about encoding. UTF-8 is the normal default for modern projects:

```python
from pathlib import Path

config_path = Path("settings.txt")
text = config_path.read_text(encoding="utf-8")
```

Exceptions are Python objects that signal something went wrong. You should not use `try/except` to hide problems. You should use it to decide what to do next. For example, a missing optional file might be logged and skipped. A missing required database path might be a fatal error.

```python
class ScanError(Exception):
    pass


def ensure_directory(path: Path) -> Path:
    if not path.exists():
        raise ScanError(f"Directory does not exist: {path}")
    if not path.is_dir():
        raise ScanError(f"Expected directory, got file: {path}")
    return path
```

The `else` block in a `try` statement runs only if no exception happened, which is useful for separating success-path logic from error handling:

```python
try:
    data = path.read_text(encoding="utf-8")
except OSError as exc:
    logger.error("failed to read %s: %s", path, exc)
else:
    logger.info("read %s bytes from %s", len(data), path)
```

Logging matters because `print()` does not tell you severity or context. A logger can distinguish debug detail from user-facing errors.

```python
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("scan started")
logger.warning("unsupported file skipped: %s", path)
logger.error("scan failed: %s", exc)
```

Common levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. For this project, think of them this way:
- `INFO`: normal progress such as how many files were found.
- `WARNING`: something unexpected but recoverable, like skipping `.txt` files when only PDFs are supported.
- `ERROR`: a specific file or operation failed.

A good scanner returns structured results. Instead of returning only a list of paths, you might return accepted files, skipped files, and failures separately. That makes testing easier and avoids guessing later.

Finally, do not catch exceptions too broadly. If you write `except Exception`, you may accidentally hide bugs like `TypeError` or `AttributeError` that should crash during development. Catch the narrowest useful exception, add context, and either handle it or re-raise it. That habit turns debugging from random guessing into a disciplined process.
