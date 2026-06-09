# Validation - Week 08 Multiprocessing Ingestion

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › [Week 8 — Multiprocessing Ingestion](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,parsing,storage]"
researchops ingest examples/sample_papers --db researchops.db --workers 1
researchops ingest examples/sample_papers --db researchops.db --workers 4
pytest tests/unit/test_parallel_ingestion.py -v
pytest tests/integration/test_ingest_workers.py -v
```

## Expected outputs
- Both ingest commands complete successfully.
- Multi-worker mode reports the same logical results as single-worker mode.
- Parallel ingestion tests pass.

## Pytest commands and expected results
```bash
pytest -k "parallel_ingestion or ingest_workers" -v
pytest -q
```

Expected result: worker-based parsing is stable, failures are captured, and the parent process persists consistent results regardless of worker count.

## Completion checklist
- [ ] Worker-safe parse function exists.
- [ ] CLI accepts `--workers`.
- [ ] Worker count validation exists.
- [ ] Parent process owns database writes.
- [ ] Success and failure aggregation works.
- [ ] Sequential and parallel tests agree on totals.
- [ ] A benchmark or timing note exists.
- [ ] No hidden ordering assumption breaks tests.
- [ ] `pytest -q` passes.
- [ ] You can explain why this workload is CPU-bound.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 8 — Multiprocessing Ingestion** · *validation.md — the checkpoint* (step 5 of 6 this week).

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
8. [Next week → Week 9](../../../curriculum/month-03-ml-engineering/week-09-protocols-clean-architecture/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 9 — Protocols & Clean Architecture](../../../curriculum/month-03-ml-engineering/week-09-protocols-clean-architecture/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 2 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 2 overview](../README.md) · [📄 Week 8 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
