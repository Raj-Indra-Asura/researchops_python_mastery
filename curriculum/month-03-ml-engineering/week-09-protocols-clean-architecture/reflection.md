# Reflection - Week 09 Protocols and Clean Architecture

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
