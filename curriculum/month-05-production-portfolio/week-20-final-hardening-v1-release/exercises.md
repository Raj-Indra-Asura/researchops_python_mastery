<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 20 — Final Hardening and v1 Release:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Week 20 Exercises: Final Hardening and v1.0 Release

## How to use this workbook
Use this workbook as a release rehearsal, not as a reading quiz. Do not start a new feature. For each exercise, produce evidence: a command result, a file diff, a written decision, or a checklist mark backed by observation.

## Warm-up exercises
1. Define shippable in five bullet points.
2. Explain why v1.0 is not the same as perfect.
3. Sort ten desired improvements into release blocker, v1.1, future idea, or reject.
4. Write the difference between MAJOR, MINOR, and PATCH without looking.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Code-reading exercises
1. Read `pyproject.toml` and identify the package name, version, scripts, and optional dependencies.
2. Read `src/researchops/__init__.py` and confirm version exposure.
3. Read CLI registration and identify where business logic is delegated.
4. Read one service and list its protocol dependencies.
5. Read one integration test and explain what real infrastructure it touches.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Implementation exercises
1. Update version references only if the checklist says they are wrong.
2. Draft a `[1.0.0]` changelog entry with Added, Changed, Fixed, Documentation, and Known limitations.
3. Update roadmap status without inventing completed work.
4. Improve one unclear error message discovered during validation.
5. Improve one demo instruction that a fresh user would misunderstand.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Testing exercises
1. Map each checklist test command to the behavior it proves.
2. Identify one unit test, one integration test, and one E2E test that matter for v1.0.
3. For a failing test, write the expected behavior before editing code.
4. Add or adjust tests only for release-blocking behavior, not new features.
5. Record any manual check that cannot reasonably be automated yet.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Debugging exercises
1. Pick a failing or fragile workflow and trace it layer by layer.
2. For a CLI error, inspect command registration before service logic.
3. For a storage error, inspect schema assumptions and test fixtures.
4. For an API error, compare status code, response body, and service exception.
5. For worker errors, draw state transitions before editing.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Refactoring exercises
1. Remove duplicated release wording if two docs contradict each other.
2. Move business logic out of CLI/API only if the release audit finds it there.
3. Rename unclear local variables only when it improves hardening readability.
4. Do not perform broad refactors that are not required for v1.0 evidence.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Written explanation exercises
1. Write a two-minute explanation of ResearchOps v1.0.
2. Write an interviewer answer for why the architecture uses protocols.
3. Write a known-limitations paragraph that is honest but not apologetic.
4. Write release notes for a user who has never seen the repo.
5. Write a retrospective on the most important engineering habit you learned.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Stretch exercises
1. Perform a fresh-clone mental walkthrough and list every assumption.
2. Create a release-risk table with likelihood, impact, owner, and mitigation.
3. Compare local install, editable install, wheel build, and Docker run paths.
4. Review docs for private paths, secrets, stale commands, and overclaims.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Brutal exercises
1. Pretend an interviewer gives you five minutes and no context: demo the project story on paper.
2. Pretend a user reports “search is broken”: write the first ten diagnostic questions.
3. Pretend CI fails only on Linux: list possible environment differences.
4. Pretend v1.0 shipped with a broken tag: write the recovery plan without rewriting history.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Mini project task
Prepare the v1.0 release candidate packet: completed checklist, changelog section, version consistency notes, demo proof, known limitations, and v1.1 candidate list. The packet should let a maintainer decide whether to tag.

**Evidence requirement:** write down what you inspected, what you expected, what happened, and what decision you made.
**Release discipline rule:** if the exercise tempts you to add a feature, stop and classify it as v1.1 or later.
**ResearchOps anchor:** connect the exercise to at least one real module, command, test, or documentation file in this repository.
- Drill 1: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 2: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 3: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 4: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 5: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 6: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.
- Drill 7: perform the exercise on a concrete ResearchOps workflow and record the smallest useful proof.

## Completion checklist
- [ ] I did not add unplanned features.
- [ ] I can explain every checklist item.
- [ ] I know which tests prove which workflows.
- [ ] I audited errors, security, performance, packaging, docs, and demo steps.
- [ ] I wrote honest known limitations.
- [ ] I can explain ResearchOps v1.0 aloud.
- [ ] I know what belongs in v1.1 instead of v1.0.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 20 — Final Hardening and v1 Release:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
