# Week 12 — Experiment Tracking

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › **Week 12 — Experiment Tracking**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Theme

You can train a model. Now you need to do it repeatedly, systematically, and with memory. This week turns the training pipeline into a research system: every run is logged, every artifact is versioned, every result is comparable.

## Learning objectives

By the end of this week you will be able to:

- Explain what an experiment, run, parameter, hyperparameter, metric, and artifact are.
- Define reproducibility and lineage for a trained model.
- Implement an `ExperimentRun` dataclass that captures all run metadata.
- Implement a file-based tracker that saves and loads run records as JSON.
- Update the training pipeline to automatically log every run.
- Use run-specific artifact names so training runs never overwrite each other.
- Write CLI commands to create, list, show, and compare experiments.
- Explain why dataset version and artifact path must be stored together.
- Write tests that verify training produces a valid run record.
- Explain when file-based tracking is sufficient and when tools like MLflow are needed.

## Project milestone

Integrate experiment tracking into the training pipeline. Every training run should produce both a model artifact and a run record. Implement `experiment list`, `experiment show`, and `experiment compare` CLI commands.

## Key source files to study

| File | What it teaches |
|---|---|
| `src/researchops/services/experiment_service.py` | Stub for Week 12 — you implement this |
| `src/researchops/storage/experiment_repository.py` | Stub for Week 12 — you implement this |
| `src/researchops/core/interfaces.py` | `ExperimentRepository` protocol |
| `src/researchops/cli/commands/experiments.py` | CLI commands for experiments |

## Concepts covered

Experiment, run, parameter, hyperparameter, metric, artifact, dataset version, model version, reproducibility, lineage, experiment store, file-based tracking, JSON serialization, run comparison, failed runs, research notebook vs. experiment tracker.

## Expected deliverables

- `ExperimentRun` dataclass with all required fields.
- `save_run`, `load_run`, `list_runs`, `compare_runs` functions.
- Training pipeline updated to log every run automatically.
- Model artifacts named with run IDs (no overwriting).
- CLI commands: `experiment list`, `experiment show RUN_ID`, `experiment compare RUN_ID RUN_ID`.
- At least two different training runs logged (different `max_features` values).
- Tests verifying run record creation and artifact linkage.

## Definition of done

- [ ] You can explain what information makes a run reproducible.
- [ ] Every training run produces a JSON record in `artifacts/experiments/`.
- [ ] Artifact filenames include the run ID.
- [ ] `experiment list` prints a summary of all runs.
- [ ] `experiment show RUN_ID` prints all params and metrics for that run.
- [ ] `experiment compare RUN_ID_1 RUN_ID_2` prints a side-by-side metric table.
- [ ] Tests verify run records have required fields.
- [ ] Tests verify artifact path in record exists on disk.
- [ ] `pytest -q` passes.
- [ ] `ruff check src tests` exits clean.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 12 — Experiment Tracking** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 11 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 13](../../../curriculum/month-04-ai-engineering-api-workers/week-13-embeddings-semantic-search/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 13 — Embeddings & Semantic Search](../../../curriculum/month-04-ai-engineering-api-workers/week-13-embeddings-semantic-search/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 12 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
