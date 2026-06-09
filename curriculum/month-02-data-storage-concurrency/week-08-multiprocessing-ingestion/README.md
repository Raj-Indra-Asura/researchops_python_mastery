# Week 08 — Multiprocessing Ingestion

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › **Week 8 — Multiprocessing Ingestion**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

> **Chapter title: "Doing many things at once, safely."**
> The week ingestion gets fast — without getting wrong.

---

## 1. Week title

Week 8 — Multiprocessing Ingestion (Month 2, Chapter 4 of 4 — month finale).

## 2. Story of the week

Your ingestion pipeline is correct and tested, but it parses PDFs one at a time.
Feed it a few hundred papers and you will wait. This week you make it fast the
*right* way: by understanding why threads will not help (the GIL), and reaching
for `ProcessPoolExecutor` to parse PDFs across multiple CPU cores. The catch is
that processes do not share memory — arguments and results must be *picklable*,
worker functions must live at module level, and one bad PDF in a worker must not
take down the whole batch. Done well, `--workers 4` is dramatically faster and
produces **exactly** the same stored result as the single-process path.

## 3. What you already know

- From Weeks 6–7: a correct, tested ingestion pipeline and search.
- From Month 1: functions, modules, exceptions.
- The concept of CPU-bound vs I/O-bound (formalised this week).

You have not yet written any concurrent or parallel code.

## 4. What this week adds

- The distinction between **CPU-bound** and **I/O-bound** work.
- The **GIL** and why `ThreadPoolExecutor` does not speed up CPU-heavy parsing.
- **`concurrent.futures.ProcessPoolExecutor`** for true multi-core parallelism.
- **Pickling constraints**: worker functions must be module-level; arguments and
  returns must be picklable.
- **Worker failure isolation**: one bad PDF must not crash the batch.
- **Batch writes** after parallel parsing.

## 5. Why this week matters

This is your first real concurrency, and it cements a principle you will reuse all
the way to Month 4: **match the tool to the workload.** PDF parsing is CPU-bound,
so it needs *processes*, not threads or async — the reasoning is captured in
[ADR-0002](../../../docs/decisions/0002-multiprocessing-vs-asyncio.md). Equally
important is the discipline of proving that an optimisation did not change
behavior: correctness first, speed second, always verifiable.

## 6. Learning objectives

By the end of the week you can:

- Explain the GIL and why threads do not parallelise CPU-bound work.
- Implement CPU-bound parallelism with `ProcessPoolExecutor`.
- Satisfy pickling constraints (module-level workers, picklable payloads).
- Isolate worker failures so one bad file does not crash the batch.
- Prove the parallel path produces the same result as the serial path.

## 7. Project milestone

`researchops ingest ./papers --workers 4` ingests using 4 parallel worker
processes, with identical results to the single-worker run.

## 8. Files / modules touched

- `src/researchops/workers/process_pool.py` — `ProcessPoolExecutor` wrapper.
- `src/researchops/services/ingestion_service.py` — gains a `workers` parameter.
- `src/researchops/cli/commands/ingest.py` — exposes the `--workers` option.

## 9. Commands introduced

```bash
researchops ingest ./examples/sample_papers --workers 2   # parallel ingestion
```

## 10. Tests involved

- `tests/unit/test_process_pool.py` — pool behavior and failure isolation.
- `tests/integration/test_ingestion_service.py` — updated to cover parallel mode
  and assert parity with serial mode.

```bash
pytest tests/unit/test_process_pool.py -v
```

## 11. Study plan for the week

1. **Day 1 — Concepts.** CPU-bound vs I/O-bound; the GIL; why threads fail here.
   Run a small CPU benchmark with threads vs processes in `/tmp`.
2. **Day 2 — Pickling.** Move the parse worker to module level; confirm arguments
   and returns are picklable.
3. **Day 3 — process_pool wrapper.** Build the `ProcessPoolExecutor` wrapper and
   collect results.
4. **Day 4 — Failure isolation + batch writes.** Make one worker raise; ensure the
   batch survives and writes the rest.
5. **Day 5 — Parity test + milestone + month report.** Assert serial == parallel.

## 12. Estimated time breakdown

| Activity | Time |
|---|---|
| Reading + GIL/benchmark experiments | ~2 hrs |
| process_pool wrapper + pickling fixes | ~3 hrs |
| Failure isolation + batch writes | ~2 hrs |
| Parity + tests | ~2 hrs |
| Reflection + month report | ~1 hr |

## 13. How to know the learner is stuck

- `PicklingError` / "can't pickle" — your worker is a closure or takes an
  unpicklable argument (e.g. an open connection).
- The parallel run is *slower* than serial (overhead on tiny inputs, or you
  accidentally used threads).
- One bad PDF crashes the whole pool.
- Parallel results differ from serial results (ordering or dropped items).

## 14. Definition of done

- [ ] `--workers N` runs ingestion across N processes.
- [ ] Worker functions are module-level and all payloads are picklable.
- [ ] A failing worker is isolated; the batch completes.
- [ ] Parallel output equals serial output (asserted in a test).
- [ ] You can explain the GIL and why processes (not threads) are used here.
- [ ] `pytest tests/unit/test_process_pool.py` passes.

## 15. Ruthless mentor checkpoint

- "Explain the GIL to me in two sentences, then justify `ProcessPoolExecutor` over
  `ThreadPoolExecutor` for this workload."
- "Ingest the same folder with `--workers 1` and `--workers 4`. Are the stored
  results byte-for-byte equivalent?"
- "Make one PDF raise inside a worker. Did the other papers still ingest?"

If parallel and serial disagree, the optimisation is a bug, not a feature.

## 16. What not to do this week

- Do **not** use threads for the CPU-bound parsing and call it parallel.
- Do **not** pass open file handles or DB connections into workers (not
  picklable).
- Do **not** let a worker failure abort the batch.
- Do **not** ship a faster pipeline that produces *different* results — parity is
  non-negotiable.

## 17. Bridge to next week

Month 2 is complete: ResearchOps can scan, parse, store, search, and ingest in
parallel — `scan → parse → store → search → parallelize`. But "works on my
machine" is not "engineered." **Week 9** opens Month 3 by stepping back to
*architecture*: protocols, dependency inversion, fakes, and strict layer
boundaries — the discipline that will let you add ML, experiment tracking, APIs,
and RAG without the system collapsing under its own weight.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 8 — Multiprocessing Ingestion** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 7 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
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
