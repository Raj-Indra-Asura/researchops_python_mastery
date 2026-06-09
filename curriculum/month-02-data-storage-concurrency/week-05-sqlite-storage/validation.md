
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 5 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 05 — SQLite Storage:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 05 SQLite Storage Layer

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest tests/unit/test_sqlite_repository.py -v
pytest tests/integration/test_storage_roundtrip.py -v
pytest -k storage -v
```

## Expected outputs
- Schema initialization tests pass.
- Repository unit tests pass.
- Integration test proves rows round-trip from models to SQLite and back.

## Pytest commands and expected results
```bash
pytest tests/integration/test_storage_roundtrip.py -v
pytest -q
```

Expected result: inserts are committed only on success, duplicate or invalid writes fail predictably, and repository methods return the correct domain data.

## Completion checklist
- [ ] Database initialization function exists.
- [ ] Tables and constraints are defined.
- [ ] Repository object encapsulates SQL.
- [ ] Insert path is transactional.
- [ ] Read path maps rows to models.
- [ ] Duplicate source-path behavior is tested.
- [ ] Rollback behavior is tested.
- [ ] Integration round trip passes.
- [ ] SQL uses parameters, not string interpolation.
- [ ] `pytest -q` passes.
- [ ] You can explain the repository pattern in one paragraph.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 05 — SQLite Storage:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
