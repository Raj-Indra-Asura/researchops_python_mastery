# Week 20 Notes: Final Hardening and v1.0 Release

## What "Done" Actually Means

There is no perfect software. "Done" means: the requirements are met, the tests pass, the documentation is accurate, and you can demonstrate it confidently.

The most common failure mode for side projects is **infinite polish**. You keep thinking "I'll release it when X is better." X never gets better because you keep adding new X. 

Finish the version. Ship it. Then start v1.1.

## Semantic Versioning

`MAJOR.MINOR.PATCH` — e.g., `1.0.0`

- **MAJOR**: Breaking change (existing users must update their code)
- **MINOR**: New feature added in a backward-compatible way
- **PATCH**: Bug fix, no new features

For a v1.0.0 release: this is the first production-ready version. No API breakage since it's the first release.

## Pre-Release Checklist

Before tagging v1.0.0, run through this:

```
Code quality:
□ All tests pass: pytest
□ Linter clean: ruff check src tests  
□ Types check: mypy src (if configured)
□ No hard-coded paths or credentials

Functionality:
□ researchops --help works
□ researchops scan works
□ researchops ingest works  
□ researchops search works
□ All week milestones tested

Documentation:
□ README accurate and complete
□ CHANGELOG up to date
□ ARCHITECTURE.md matches the code
□ demo.md produces correct output

Release:
□ Version bumped in pyproject.toml
□ Version bumped in __init__.py
□ CHANGELOG has a [1.0.0] section with today's date
□ git tag -a v1.0.0 -m "Version 1.0.0"
□ git push --tags
```

## How to Create a Git Release Tag

```bash
# Create an annotated tag
git tag -a v1.0.0 -m "ResearchOps v1.0.0 — 20-week build complete"

# Push the tag to GitHub
git push origin v1.0.0

# On GitHub: go to Releases → Draft a new release → choose tag v1.0.0
```

## The Retrospective

A retrospective is a structured reflection on a completed project. Answer these questions honestly:

1. What did I build? (be specific)
2. What did I learn that I didn't expect to learn?
3. What would I do differently?
4. What was hardest?
5. What am I most proud of?
6. What would v1.1 look like?
