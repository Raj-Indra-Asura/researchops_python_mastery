<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It — Week 06 PDF Parsing Pipeline

---

## Scenario 1 — A file that is not a PDF

**Setup:** Create a plain text file named `fake.pdf` with contents `"This is just text."`.

**Break it:** Pass it to `parse_pdf(Path("fake.pdf"))`.

**What to observe:**
- `pypdf` will open the file.
- It may either raise an exception immediately or produce a `PdfReader` with 0 pages and empty text.
- Print the exact exception type and message.

**Expected behavior in your implementation:**
`ParsingError` should be raised with a message that includes the file path.

**Discuss:** Should you detect the non-PDF file before calling `pypdf`, or let `pypdf` detect it?
What are the tradeoffs?

---

## Scenario 2 — Zero-byte PDF

**Setup:**
```python
Path("empty.pdf").write_bytes(b"")
```

**Break it:** Call `parse_pdf(Path("empty.pdf"))`.

**What to observe:**
- `pypdf` will likely raise `PdfStreamError` or similar.
- Your code should catch this and raise `ParsingError`.

**Verify:** The `FailedDocument` error type should be `"ParsingError"`, not a raw `pypdf` exception.

---

## Scenario 3 — Image-only PDF (no embedded text)

**Setup:** Find or create a PDF that contains only scanned images.
(You can use any image converted to PDF, or find a scan online.)

**Break it:** Call `parse_pdf` on it.

**What to observe:**
- `page.extract_text()` returns `None` or `""` for every page.
- The full text after joining is empty.
- Your code should raise `EmptyDocumentError`.

**Discuss:** How would you handle this case if you had an OCR library available?
What would the fallback pipeline look like?

---

## Scenario 4 — Force a service-level failure after a successful parse

**Setup:** Create a fake parser that returns a valid `ParsedDocument`.
Create a fake repository whose `save()` method always raises `Exception("Database full")`.

**Break it:** Run `ingest_directory`.

**What to observe:**
- The parse succeeds.
- The save fails.
- Does the service record a `FailedDocument` for this case?
- What does `result.successes` contain?
- What does `result.failures` contain?

**Expected behavior:** The paper does not appear in successes.
The save failure should be handled (logged or recorded) without crashing the batch.

---

## Scenario 5 — Ingest the same directory twice with `skip_existing=False`

**Setup:** Ingest a directory of 3 PDFs.
After the first run, call `ingest_directory` on the same directory again with `skip_existing=False`.

**What to observe:**
- Your `save()` method will encounter duplicate `paper_id` values.
- `DuplicatePaperError` is raised.
- Does this crash the batch or just record failures?

**Expected behavior:** The duplicate check should convert `DuplicatePaperError` into a skip or a graceful log, not an unhandled crash.

---

## Scenario 6 — Ingest a directory that does not exist

**Setup:** Call `ingest_directory(Path("/tmp/nonexistent_xyz_folder"))`.

**What to observe:**
- The `find_pdfs` utility will likely raise `NotADirectoryError`.
- Check whether `ingest_directory` handles this or crashes.

**Expected behavior:** The service should catch this and return an empty `IngestionResult` or raise a clear error, not an unhandled exception.

---

## Scenario 7 — Very large text field

**Setup:** Create a `ParsedDocument` where `raw_text` is 10 MB of repeated characters.
Pass it through `clean_text`.
Try to save the resulting `Paper` to the repository.

**What to observe:**
- SQLite can store large `TEXT` values, but how does performance change?
- How long does the `save()` call take?
- How long does `list_all()` take when it loads papers with large text fields?

**Discuss:** Should you store the full text in the database, or only a truncated version?
What are the tradeoffs for search quality versus storage efficiency?

---

## Scenario 8 — Unicode in PDF metadata

**Setup:** Find or create a PDF with non-ASCII characters in its metadata:
- Title in Chinese or Japanese.
- Author name with accented characters.

**Break it:** Run `parse_pdf` and inspect `doc.metadata`.

**What to observe:**
- Does the title extract correctly?
- Does `extract_title` handle non-ASCII titles?
- Does round-tripping through SQLite preserve the Unicode correctly?

**Verify:** Save a paper with a non-ASCII title.
Load it back.
Assert the title is unchanged.

---

## Scenario 9 — Duplicate source paths

**Setup:** Ingest a directory.
Now rename one of the PDFs and ingest the directory again with `skip_existing=False`.

**What to observe:**
- The renamed file has a different path, so `PaperId.from_path` produces a different `id`.
- But the text content may be identical to the original file.
- Is there a way to detect this as a duplicate?

**Discuss:** The current design uses path-based IDs.
What would a content-based ID (`sha256_file`) do differently?
What are the tradeoffs?

---

## Scenario 10 — Parser that takes too long

**Setup:** Create a fake parser that sleeps for 5 seconds before returning a result.

```python
import time

class SlowParser:
    def parse(self, path):
        time.sleep(5)
        return ...
```

**Break it:** Run `ingest_directory` on a directory with 5 PDFs.

**What to observe:**
- Total time is approximately `5 × 5 = 25` seconds.
- The current sequential implementation has no timeout.
- If one PDF takes forever, the whole batch stalls.

**Discuss:** This is the motivation for Week 8 (multiprocessing).
How would you add a timeout per-file?
What Python tools support timeouts on function calls?

---

## Edge cases to explore

1. **Empty directory:** Run `ingest_directory` on an empty directory.
   Assert the result has zero successes, failures, and skipped.
   Assert no crash.

2. **Directory with only non-PDF files:** Put `.txt` and `.docx` files in the directory.
   Assert no PDFs are found.
   Assert no crash.

3. **Recursive vs non-recursive:** Put PDFs in a subdirectory.
   Run with `recursive=False`.
   Assert PDFs in subdirectories are not found.
   Run with `recursive=True`.
   Assert they are found.

4. **PDF with 0 pages:** Some corrupted PDFs have empty page lists.
   What does `for page in reader.pages` do with an empty list?
   Does `join([])` produce an empty string?
   Does your `EmptyDocumentError` trigger?

5. **Metadata with None values:** Some `reader.metadata` objects contain `None` for certain keys.
   Does your metadata extraction handle `None` values?
   Does `str(None)` produce `"None"` (the string)?
   Is that acceptable?

---

## What did you learn?

1. Which failure case was hardest to handle gracefully?
2. What information in `FailedDocument` was most useful for debugging?
3. Which edge case would be most likely to appear in real usage?
4. How would you extend the pipeline to handle a second PDF library as a fallback?
5. What would you add to the failure recording to make re-processing failures easier?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
