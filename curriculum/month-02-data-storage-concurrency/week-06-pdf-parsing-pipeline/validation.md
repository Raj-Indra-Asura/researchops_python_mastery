
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

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"
researchops ingest examples/sample_papers --db researchops.db
pytest tests/unit/test_pdf_parser.py -v
pytest tests/integration/test_ingest_pipeline.py -v
```

## Expected outputs
- `researchops ingest ...` prints counts for successful and failed files.
- Parser unit tests pass.
- Integration test proves parsed text reaches SQLite.

## Pytest commands and expected results
```bash
pytest -k "pdf_parser or ingest_pipeline" -v
pytest -q
```

Expected result: the ingest command processes sample PDFs, parse failures are reported clearly, and the stored database contains successful parse results.

## Completion checklist
- [ ] `pypdf` dependency is installed.
- [ ] Parser extracts text page by page.
- [ ] Blank extraction is handled intentionally.
- [ ] Ingestion service returns `IngestionResult`.
- [ ] `ingest` CLI command is registered.
- [ ] SQLite writes occur after successful parse.
- [ ] Integration pipeline test passes.
- [ ] Duplicate-ingest behavior is defined.
- [ ] Output summary is readable.
- [ ] `pytest -q` passes.
- [ ] You can explain the stages of your ingestion pipeline.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 06 — PDF Parsing Pipeline:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
