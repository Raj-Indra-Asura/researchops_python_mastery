# Reflection - Week 09 Protocols and Clean Architecture

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 3](../README.md) › [Week 9 — Protocols & Clean Architecture](./README.md) › **reflection.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

This document is your personal learning record for Week 9. Fill it in honestly. The goal is not to show a perfect result but to capture what you actually experienced.

---

## What I built

**Protocols I can now explain:**
(List each protocol in `interfaces.py` and write one sentence about what it represents.)

- `DocumentParser`:
- `PaperRepository`:
- `FailureRepository`:
- `SearchEngine`:
- `EmbeddingModel`:
- `ExperimentRepository`:

**Dependencies I traced:**
(Which services did you read from constructor to adapter? What surprised you?)

**Fakes I wrote or extended:**
(Did you write a new fake? Which protocol does it satisfy?)

---

## What broke

**Mypy error I hit:**
(Copy the exact error message and explain what caused it.)

**Test that revealed unexpected coupling:**
(Which test failed and what infrastructure dependency did it expose?)

**The violation that was hardest to see:**
(Was it an import, a constructor, or something else?)

---

## What I misunderstood

**Protocol concept I had to re-read:**
(What was confusing at first? What cleared it up?)

**Dependency inversion misconception:**
(Did you initially confuse dependency injection with dependency inversion? What is the difference?)

**Layer boundary I mixed up:**
(Did you ever put service logic in infrastructure or vice versa? What happened?)

---

## What I fixed

**Refactor I completed:**
(Describe the before and after. What changed in the constructor? What changed in the tests?)

**Evidence that both fake and real adapters work:**
(Name the specific pytest command you ran and what it showed.)

**Code that became easier to understand:**
(What does the code communicate now that it did not before?)

---

## Architecture diagram

Sketch or describe the dependency graph for `IngestionService`.
Show which direction the arrows point. Mark which modules are in Core, Service, Infrastructure, and CLI layers.

```
[your diagram here — text form is fine]
```

---

## Confidence score

- Week 9 confidence (1–10):
- Reason for that score:
- One thing I would explain confidently to a peer:
- One thing I am still uncertain about:

---

## Preparation for Week 10

- [ ] I can swap a fake for a real dependency by changing only the composition root.
- [ ] I understand why fast unit tests matter and what makes integration tests slower.
- [ ] I know what `ruff`, `mypy`, and `pytest` are each checking.
- [ ] I am ready to formalize quality gates and testing discipline next week.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 3 — ML Engineering · **Week 9 — Protocols & Clean Architecture** · *reflection.md — the journal* (step 6 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [validation.md](./validation.md)
- ▶ **Next:** [Write your Week 9 report](../../../docs/weekly-reports/README.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
6. **➡ [reflection.md](./reflection.md) ← you are here**
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 10](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 10 — Testing & Quality Gates](../../../curriculum/month-03-ml-engineering/week-10-testing-quality-gates/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 3 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 3 overview](../README.md) · [📄 Week 9 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
