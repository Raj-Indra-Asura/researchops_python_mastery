# Validation - Week 07 Keyword Search and Data Quality

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › [Week 7 — Keyword Search & Data Quality](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 7 — Keyword Search & Data Quality** · *validation.md — the checkpoint* (step 5 of 6 this week).

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
8. [Next week → Week 8](../../../curriculum/month-02-data-storage-concurrency/week-08-multiprocessing-ingestion/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 8 — Multiprocessing Ingestion](../../../curriculum/month-02-data-storage-concurrency/week-08-multiprocessing-ingestion/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 2 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 2 overview](../README.md) · [📄 Week 7 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
