# Validation - Week 06 PDF Parsing Pipeline

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › [Week 6 — PDF Parsing Pipeline](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 6 — PDF Parsing Pipeline** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 7](../../../curriculum/month-02-data-storage-concurrency/week-07-keyword-search-data-quality/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 7 — Keyword Search & Data Quality](../../../curriculum/month-02-data-storage-concurrency/week-07-keyword-search-data-quality/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 2 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 2 overview](../README.md) · [📄 Week 6 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
