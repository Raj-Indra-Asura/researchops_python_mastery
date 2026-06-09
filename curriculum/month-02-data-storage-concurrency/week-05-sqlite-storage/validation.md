# Validation - Week 05 SQLite Storage Layer

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › [Week 5 — SQLite Storage](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 5 — SQLite Storage** · *validation.md — the checkpoint* (step 5 of 6 this week).

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
8. [Next week → Week 6](../../../curriculum/month-02-data-storage-concurrency/week-06-pdf-parsing-pipeline/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 6 — PDF Parsing Pipeline](../../../curriculum/month-02-data-storage-concurrency/week-06-pdf-parsing-pipeline/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 2 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 2 overview](../README.md) · [📄 Week 5 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
