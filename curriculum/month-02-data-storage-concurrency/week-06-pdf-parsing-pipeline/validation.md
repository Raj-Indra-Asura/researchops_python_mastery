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
