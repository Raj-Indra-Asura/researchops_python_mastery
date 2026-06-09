# ADR-0001: Start ResearchOps as a Modular Monolith

- **Status:** Accepted
- **Date:** Week 1
- **Source:** Expands ADR-001 in [`adr-log.md`](./adr-log.md)

> New to architecture decision records? An ADR is a short note that captures
> one important choice, why it was made, and what it costs. Read it like a
> diary entry from the team's past self. This one is written for a beginner —
> if a sentence uses a new word, the word is explained the first time it
> appears.

## Decision title

Build ResearchOps as a single installable Python package (`researchops`) with
clear internal module boundaries — a *modular monolith* — instead of many
separate published packages.

## Context

When a project starts, you have to decide how to split the code. Two extremes:

- **One big blob:** everything in a few files, imported freely. Fast to start,
  but it rots into spaghetti where every file depends on every other file.
- **Many packages from day one:** `researchops-core`, `researchops-storage`,
  `researchops-ml`, each versioned and published separately. This feels
  "professional," but on day one you do not yet know where the real seams are.

ResearchOps is also a *learning* project. The learner has only Python basics and
needs to see the **whole system in one place** while still practising good
structure. Premature package-splitting would force the learner to fight
packaging tooling (multiple `pyproject.toml` files, version pinning between
internal packages, editable installs across repos) before they have written any
interesting logic.

A *modular monolith* sits between the two extremes: **one** deployable/installable
unit, but with **internal modules that are not allowed to import each other
freely.** The boundaries are real even though there is only one package.

## Decision

Keep all code inside one `researchops` package under a `src/` layout, organised
into clear layers/modules:

```
researchops/
  core/        # domain models + protocols (no infrastructure imports)
  services/    # application logic; depends only on core protocols
  storage/     # SQLite adapters (infrastructure)
  parsing/     # PDF adapters (infrastructure)
  ml/          # classical ML (infrastructure)
  ai/          # embeddings / RAG (infrastructure)
  api/         # FastAPI transport
  cli/         # Typer transport + composition root
```

Enforce import direction by **convention now, and tooling later** (e.g.
`import-linter`): `core` imports nothing from the outer layers, `services`
imports only `core` (protocols), and `cli`/`api` are the only places allowed to
wire concrete adapters together (the *composition root* — the single place where
the real objects are constructed and plugged in).

## Why ResearchOps starts as a modular monolith

- **One mental model.** The learner can open one repository and trace any
  feature end to end (`cli → service → protocol → adapter`).
- **Refactoring is cheap.** Moving a function between modules is a local change,
  not a cross-repository release dance.
- **Boundaries are still taught.** Import rules give the *discipline* of
  separate packages without the *overhead* of separate packages.
- **One test suite, one CI pipeline.** Simpler to keep green while learning.

## Why not micro-packages initially

- You cannot draw correct package boundaries before you understand the domain.
  Boundaries chosen in Week 1 would almost certainly be wrong by Week 12.
- Internal version pinning (package A needs B==0.3) creates upgrade friction
  that teaches packaging pain, not software design.
- It hides the system: no learner benefits from `pip install`-ing six tiny
  packages just to read how ingestion works.
- It is **easy to split later** and **hard to un-split** — start coarse.

## Consequences

**Positive**

- Fast iteration; simple onboarding; one `pyproject.toml`.
- Import rules teach dependency inversion in a concrete, visible way.
- The composition root pattern (in `cli/`) becomes obvious.

**Negative / costs**

- Import direction is enforced by humans until `import-linter` is added; a
  careless import can violate the architecture silently.
- A single package can still grow messy if module responsibilities are not
  respected — the monolith must stay *modular*, not just *mono*.
- Everything is released together; you cannot version `ml` separately from
  `storage`.

## Alternatives considered

1. **Single flat module (no layers).** Rejected: teaches nothing about
   architecture and rots quickly.
2. **Multi-package monorepo (separate `pyproject.toml` per package).**
   Rejected for now: real boundaries are unknown early, and packaging overhead
   distracts from learning.
3. **Multiple repositories / microservices.** Rejected: enormous operational
   overhead (deployment, networking, versioning) for a single-developer
   learning project. This would be "platform cosplay" — looking like a big
   system without the substance.

## When splitting into multiple packages would become justified

Split only when **evidence** appears, not on a hunch:

- A module (e.g. `ml` or `ai`) needs an **independent release cadence** or must
  be reused by a *different* project.
- Build/test time becomes painful and a module could be tested in isolation.
- Two clear teams own different modules and step on each other.
- A module accretes heavy optional dependencies that most users should not
  install (a candidate for an optional extra first, a separate package second).

Until at least one of these is true, the modular monolith wins.

## Related curriculum weeks

- **Week 1 — Foundations:** establishes the `src/` layout and the single
  `researchops` package this ADR describes.
- **Week 4 — CLI & Packaging:** builds the composition root in `cli/`, the one
  place allowed to wire concrete adapters.
- **Week 9 — Protocols & Clean Architecture:** makes the import rules explicit
  with `typing.Protocol` and dependency inversion — the discipline that keeps
  the monolith modular.
- **Week 14 — FastAPI Layer:** adds a second transport (`api/`) without
  duplicating business logic, proving the layering pays off.
- **Week 18 — Docker & Environment Config:** packages and ships the single unit;
  a good moment to reflect on whether any split is yet justified (it usually is
  not).
