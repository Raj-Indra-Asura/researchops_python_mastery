<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 20 — Final Hardening and v1 Release:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Week 19 Reflection](../week-19-documentation-portfolio-polish/reflection.md) · ➡️ [Notes →](notes.md)

---
<!-- NAV_END -->

# Week 20: Final Hardening and v1.0 Release

## 1. Week title
**Week 20: Final Hardening and v1.0 Release**
Chapter title: **Finishing is a skill.**

## 2. Story of the week
ResearchOps already has many parts. This week you stop expanding and start proving. The story is a release candidate moving from “it works for me” to “another serious learner can run, inspect, and trust it.”

## 3. What you already know
You know the CLI, storage, parsing, search, ML, experiments, API, async I/O, workers, RAG, Docker, and documentation pieces built across Weeks 1–19. You also know the clean architecture boundaries that keep those pieces understandable.

## 4. What this week adds
A release-readiness process: end-to-end validation, error-handling audit, edge-case review, security review, version consistency, changelog finalization, packaging/distribution checks, and a precise definition of shippable.

## 5. Why this week matters
Finishing is a professional skill. A portfolio project that cannot be installed, tested, explained, or released is still a prototype. Week 20 teaches how to turn a prototype into a coherent v1.0 artifact.

## 6. Learning objectives
- Define “done” for a software release.
- Use `RELEASE_CHECKLIST.md` as the source of truth.
- Explain semantic versioning and why `v1.0.0` matters.
- Audit errors, edge cases, performance, security, docs, packaging, and demos.
- Write release notes and final changelog entries.
- Say no to new features during scope freeze.

## 7. Project milestone
`v1.0.0` is ready to tag after every checklist item passes. CI is green, the demo is reproducible, the changelog is complete, versions match, and the project is portfolio-ready.

## 8. Files/modules touched
- `RELEASE_CHECKLIST.md` — release readiness checklist.
- `CHANGELOG.md` — complete version history.
- `ROADMAP.md` — final status and future work.
- `pyproject.toml` — package version and entry points.
- `src/researchops/__init__.py` — `__version__` consistency.
- `docs/demo.md` or demo script — final walkthrough.
- Tests under `tests/` — confidence evidence, not decoration.

## 9. Commands introduced
```bash
researchops --help
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
python -m build
git tag -a v1.0.0 -m "ResearchOps v1.0.0"
git show v1.0.0 --no-patch
```

## 10. Tests involved
Use existing tests only: unit tests for models/services, integration tests for SQLite/parsing/search/workers, E2E tests for CLI/API workflows, and manual demo checks documented in validation.

## 11. Study plan
Day 1: read notes and checklist without changing scope.
Day 2: run validation commands and classify failures.
Day 3: fix release-blocking errors only.
Day 4: update changelog, versions, roadmap, and demo docs.
Day 5: perform fresh release review and final reflection.

## 12. Estimated time breakdown
- Reading and planning: 1–2 hours.
- Full validation pass: 1–3 hours.
- Fixing release blockers: 3–8 hours.
- Documentation and changelog: 2–4 hours.
- Final demo rehearsal: 1–2 hours.
- Reflection and release decision: 1 hour.

## 13. How to know the learner is stuck
They add features instead of fixing checklist failures. They cannot explain which layer owns a bug. They mark commands complete without running them. They hide limitations. They cannot describe what v1.0 includes in plain language.

## 14. Definition of done
- All required release checklist items are complete.
- Tests and lint pass according to validation.
- Versions match in package metadata and code.
- Changelog includes `[1.0.0]`.
- Demo runs from documented steps.
- Known limitations are written clearly.
- No architecture boundary is knowingly violated.

## 15. Ruthless mentor checkpoint
If you would be embarrassed to run the demo live, the release is not done. If the README promises behavior that validation does not prove, the release is not done. If you are adding features during final hardening, you are avoiding the real work.

## 16. What not to do this week
Do not add new ML providers. Do not redesign architecture. Do not introduce heavy dependencies. Do not rewrite the CLI. Do not create a cloud platform. Do not tag a release before evidence is complete.

## 17. Bridge to what's next / life after v1.0
After v1.0, maintain the project like software: triage issues, plan v1.1 deliberately, keep changelog entries current, protect tests, and improve the demo based on real user confusion.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Week 19 Reflection](../week-19-documentation-portfolio-polish/reflection.md) · ➡️ [Notes →](notes.md)

**Week 20 — Final Hardening and v1 Release:** **README** · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
