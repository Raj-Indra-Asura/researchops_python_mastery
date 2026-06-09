<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 6 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 06 PDF Parsing Pipeline

## 1. Pre-validation checklist

- [ ] Start at repository root where `pyproject.toml` is visible.
- [ ] Confirm `src/researchops/parsing/pdf_parser.py` exists.
- [ ] Confirm `src/researchops/parsing/text_cleaner.py` exists.
- [ ] Confirm `src/researchops/parsing/metadata_extractor.py` exists.
- [ ] Confirm `src/researchops/services/ingestion_service.py` exists.
- [ ] Confirm `src/researchops/cli/commands/ingest.py` exists.
- [ ] Confirm `examples/sample_papers/` exists.
- [ ] Confirm Week 6 has not added multiprocessing validation.
- [ ] Confirm Week 6 has not added async ingestion validation.
- [ ] Confirm the parser returns `ParsedDocument`.
- [ ] Confirm failures can be represented by `FailedDocument`.
- [ ] Confirm the CLI command is `researchops ingest`.
- [ ] Confirm optional extras include `dev`, `parsing`, and `storage`.
- [ ] Confirm sample PDFs or repeatable test fixtures exist for real parsing proof.

A clean validation run should prove successful papers, failed documents, and readable counts.

## 2. Commands to run

### Activate environment
```bash
source .venv/bin/activate
```

### Install Week 6 extras
```bash
python -m pip install -e ".[dev,parsing,storage]"
```

### CLI smoke test
```bash
researchops --help
```

### Ingest help
```bash
researchops ingest --help
```

### Syllabus ingest command
```bash
researchops ingest ./examples/sample_papers
```

### List stored papers
```bash
researchops papers list
```

### List failed documents
```bash
researchops papers failed
```

### Syllabus integration test
```bash
pytest tests/integration/test_ingestion_service.py -v
```

### Current ingestion service unit tests
```bash
pytest tests/unit/test_ingestion_service.py -v
```

### Parser unit tests when present
```bash
pytest tests/unit/test_pdf_parser.py -v
```

### Metadata extractor tests
```bash
pytest tests/unit/test_metadata_extractor.py -v
```

### Text cleaner tests
```bash
pytest tests/unit/test_text_cleaner.py -v
```

### Focused Week 6 tests
```bash
pytest -k "ingestion_service or pdf_parser or metadata_extractor or text_cleaner" -v
```

### Full test suite
```bash
pytest -q
```

### Existing lint check
```bash
ruff check src tests
```

Do not use a `--workers` option for Week 6 validation; that belongs to a later week.

## 3. Expected outputs

- Install completes and `researchops` is executable.
- `researchops --help` shows the main CLI.
- `researchops ingest --help` shows a directory-based ingest command.
- `researchops ingest ./examples/sample_papers` prints counts for successes, failures, and skips.
- If valid sample PDFs exist, at least one should become visible through `researchops papers list`.
- If corrupt or empty PDFs exist, they should be visible through `researchops papers failed`.
- The integration test reports PASSED for the full pipeline test.
- The service unit tests report PASSED for the orchestration scenarios.
- Parser tests prove success and failure behavior when present.
- The full suite exits successfully before moving on.
A conceptual good summary is:
```text
Ingestion complete: 2 ok / 1 failed / 0 skipped
```

### Evidence log for manual validation

- **Installation:** the install command exits successfully and `pypdf` can be imported by parser code.
  Record this evidence before deciding the week is complete.
- **CLI availability:** `researchops --help` and `researchops ingest --help` both display help.
  Record this evidence before deciding the week is complete.
- **Ingest attempt:** the ingest command reports counts instead of a placeholder.
  Record this evidence before deciding the week is complete.
- **Successful storage:** `researchops papers list` shows papers after valid PDFs are ingested.
  Record this evidence before deciding the week is complete.
- **Failure storage:** `researchops papers failed` shows failed documents after bad PDFs are attempted.
  Record this evidence before deciding the week is complete.
- **Repeat behavior:** a second run does not silently duplicate every paper.
  Record this evidence before deciding the week is complete.
- **Integration proof:** the syllabus integration test passes.
  Record this evidence before deciding the week is complete.
- **Service proof:** the existing service unit tests pass.
  Record this evidence before deciding the week is complete.
- **Parser proof:** parser tests cover success and parse failure.
  Record this evidence before deciding the week is complete.
- **Documentation proof:** notes and validation contain the required sections.
  Record this evidence before deciding the week is complete.

A learner should be able to copy the commands, compare the outputs, and know exactly which layer to inspect when a check fails.

## 4. Tests that must pass

The syllabus specifically requires:
```bash
pytest tests/integration/test_ingestion_service.py -v
```

- `TestIngestDirectory::test_ingests_single_pdf` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_ingests_multiple_pdfs` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_parse_failure_recorded` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_unexpected_error_recorded_as_failure` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_skip_existing_paper` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_no_skip_when_skip_existing_false` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_empty_directory_returns_empty_result` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_invalid_directory_returns_empty_result` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_result_has_run_id` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_recursive_discovers_nested_pdfs` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `TestIngestDirectory::test_nonrecursive_misses_nested_pdfs` must remain understandable and passing in `tests/unit/test_ingestion_service.py`.
- `tests/unit/test_pdf_parser.py` should cover valid parse, missing file, unsupported file type, empty extraction, and missing dependency guidance.
- `tests/unit/test_metadata_extractor.py` should cover metadata title, fallback title, author present, and author absent.
- `tests/unit/test_text_cleaner.py` should cover whitespace and control-character cleanup.
- The full `pytest -q` run should pass after focused tests pass.

## 5. Manual checks

- Inspect `researchops ingest --help` and confirm the feature is not a placeholder.
- Inspect sample inputs with `find examples/sample_papers -maxdepth 2 -type f`.
- Run the sample ingest command and write down success, failure, and skip counts.
- Run `researchops papers list` and confirm successes are stored papers.
- Run `researchops papers failed` and confirm failures are visible.
- Run ingest a second time and confirm duplicate behavior is defined.
- If needed, create project-local `.validation/week06_bad_inputs/bad.pdf` with invalid content, ingest it, inspect failures, then remove the scratch directory.
- Explain aloud which command proved each fact.

## 6. Architecture checks

- `core/` must not import parser, storage, CLI, API, ML, workers, or search packages.
- `parsing/pdf_parser.py` may import `pypdf` because it is infrastructure.
- `services/ingestion_service.py` should not import `SQLitePaperRepository`.
- `cli/commands/ingest.py` may wire `PdfParser` and `SQLitePaperRepository` into `IngestionService`.
- `storage/sqlite_repository.py` may know SQL because persistence is its job.
- Failures belong in domain records, not only in terminal output.
- The command line should display results, not own business policy.
- Do not add future parallel or API architecture to Week 6.
- Integration tests should use `tmp_path` and not hard-coded absolute database paths.
- Validation should use repository-relative paths.

## 7. Documentation checks

- [ ] `notes.md` has no `LEARNING_FORMAT` block.
- [ ] `notes.md` has no `Existing detailed notes` wrapper.
- [ ] `notes.md` has all 20 required notes sections in order.
- [ ] `notes.md` is at least 800 lines of beginner teaching.
- [ ] `validation.md` has all 10 required validation sections.
- [ ] `validation.md` is roughly Week-1 standard depth and at least 280 lines.
- [ ] The Quick Commands block remains unchanged.
- [ ] The NAV blocks remain unchanged.
- [ ] Validation includes the syllabus commands.
- [ ] Validation includes real service test names from the current repository.

## 8. Do-not-proceed warnings

- **Warning:** Do not proceed if `researchops --help` fails.
- **Warning:** Do not proceed if `researchops ingest --help` is missing.
- **Warning:** Do not proceed if ingest only prints a placeholder.
- **Warning:** Do not proceed if successful PDFs are not stored.
- **Warning:** Do not proceed if corrupt PDFs crash the batch.
- **Warning:** Do not proceed if failures are only printed and not recorded.
- **Warning:** Do not proceed if `researchops papers failed` cannot show failures.
- **Warning:** Do not proceed if `pypdf` leaks into service or CLI business logic.
- **Warning:** Do not proceed if service imports concrete SQLite implementation.
- **Warning:** Do not proceed if tests depend on personal files.
- **Warning:** Do not proceed if Week 6 validates workers, async, API, OCR, or RAG.
- **Warning:** Do not proceed if documentation still has split-format wrapper text.

## 9. Ruthless mentor checkpoint

1. What exact command ingests sample papers?
2. What command lists successful papers?
3. What command lists failed documents?
4. What integration test does the syllabus name?
5. What model does the parser return?
6. What model represents failed parsing?
7. Why is a skipped file not a failed file?
8. Why does `extract_text() or ""` matter?
9. Which file owns PDF extraction?
10. Which file owns orchestration?
11. Which file owns CLI wiring?
12. Which file owns SQLite persistence?
13. Why do service tests use fakes?
14. Why does Week 6 still need real integration proof?
15. What future-week behavior must not be added now?
If you cannot answer these, rerun the focused validation and reread the corresponding notes section.

## 10. Definition of done

- [ ] `researchops ingest ./examples/sample_papers` runs through the real pipeline.
- [ ] Successful PDFs become stored `Paper` records.
- [ ] Failed PDFs become stored `FailedDocument` records.
- [ ] `researchops papers list` shows successes.
- [ ] `researchops papers failed` shows failures.
- [ ] The parser returns `ParsedDocument`.
- [ ] Empty extraction is handled intentionally.
- [ ] Missing `pypdf` produces beginner-friendly guidance.
- [ ] The service coordinates without concrete storage imports.
- [ ] The CLI wires concrete parser and repository objects.
- [ ] Repeated ingest behavior is defined and tested.
- [ ] Recursive and non-recursive discovery behavior are tested.
- [ ] `pytest tests/integration/test_ingestion_service.py -v` passes.
- [ ] `pytest tests/unit/test_ingestion_service.py -v` passes.
- [ ] Parser, cleaner, and metadata tests pass.
- [ ] The full test suite passes.
- [ ] `notes.md` is unified and complete.
- [ ] `validation.md` has all 10 sections.
- [ ] The learner can explain happy path and failure path aloud.
Move forward only when commands, tests, manual checks, architecture checks, and explanations all agree.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
