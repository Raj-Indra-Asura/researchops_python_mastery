# Week 20 Validation: Final Release

## Pre-Release Commands

```bash
# All tests pass
pytest
# Expected: X passed, 0 failed

# Linter clean
ruff check src tests
# Expected: no output (no errors)

# CLI smoke test
researchops --help
researchops scan ./examples/sample_papers
researchops ingest ./examples/sample_papers
researchops search "machine learning"

# Full demo
# Follow docs/demo.md line by line

# Check version
python -c "import researchops; print(researchops.__version__)"
# Expected: 1.0.0
```

## Release Commands

```bash
git add .
git commit -m "v1.0.0: final release"
git tag -a v1.0.0 -m "ResearchOps v1.0.0"
git push && git push --tags
```

## Final Checklist

- [ ] All tests pass (0 failures)
- [ ] ruff clean
- [ ] Version = 1.0.0 in pyproject.toml and __init__.py
- [ ] CHANGELOG.md has [1.0.0] section with today's date
- [ ] ROADMAP.md shows all 20 weeks ✅
- [ ] v1.0.0 tag exists on GitHub
- [ ] docs/demo.md runs without errors
- [ ] README is complete and accurate
- [ ] You are proud of this project
