
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 7 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 07 Keyword Search and Data Quality

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,storage]"
researchops search "retrieval" --db researchops.db
pytest tests/unit/test_normalize.py -v
pytest tests/unit/test_keyword_search.py -v
pytest tests/integration/test_search_command.py -v
```

## Expected outputs
- Search command returns ranked results or an explicit no-match message.
- Normalization tests pass.
- Keyword ranking tests pass in deterministic order.
- Integration search command test passes against a seeded database.

## Pytest commands and expected results
```bash
pytest -k "normalize or keyword_search or search_command" -v
pytest -q
```

Expected result: search is case-insensitive after normalization, ranking is predictable, and low-quality data is surfaced instead of silently ignored.

## Completion checklist
- [ ] Text normalization is implemented.
- [ ] Tokenization is implemented.
- [ ] Ranking logic is tested.
- [ ] Empty-query behavior is defined.
- [ ] Search CLI command exists.
- [ ] Search reads from SQLite-backed data.
- [ ] Snippet or summary output is useful.
- [ ] Low-quality document checks exist.
- [ ] Integration search test passes.
- [ ] `pytest -q` passes.
- [ ] You can explain how your search score is computed.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
