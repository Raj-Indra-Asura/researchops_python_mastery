# Reflection - Week 10 Testing Discipline and Quality Gates

This is your personal record for Week 10. Fill it in honestly. The goal is not to claim you completed everything, but to understand what you know and what you still need to solidify.

---

## What I built

**New fixtures I wrote:**
(Name them and describe what they set up.)

**Tests I added this week:**
(List test names and which behaviors they cover.)

**Quality gates now active:**
(Which of ruff / pytest / coverage / CI are now running?)

---

## What broke

**Test failure I did not expect:**
(Describe the error. Was it a fixture error, assertion failure, or coverage failure?)

**CI or tooling issue I encountered:**
(Did CI fail for an unexpected reason? What was it?)

**How I isolated the problem:**
(What command helped you narrow it down? Did `-vv`, `--maxfail`, or `--durations` help?)

---

## What I misunderstood

**Fixture concept I had to re-read:**
(Was it scope, dependency chaining, or conftest.py placement?)

**Coverage signal I misread:**
(Did you think a line was covered when it was not? Or the opposite?)

**Difference I was fuzzy on:**
(Did you confuse unit and integration scope? Or monkeypatch vs. fake?)

---

## What I fixed

**Brittle test I made robust:**
(What made it brittle? How did you fix it — fake, tmp_path, or monkeypatch?)

**Missing gate I added:**
(Which check was not running before?)

**Evidence the suite is healthier:**
(Number of tests before and after. Coverage percentage before and after.)

---

## My quality gate results

Run these and record the actual output:

```bash
ruff check src tests
```

Result:

```bash
pytest --cov=researchops --cov-report=term-missing -q
```

Coverage percentage:

Tests: passed / failed / errors

---

## Test pyramid audit

| Layer | Test count | Approximate run time |
|---|---|---|
| Unit (`tests/unit/`) | | |
| Integration (`tests/integration/`) | | |
| E2E (`tests/e2e/`) | | |

Is the pyramid shaped correctly (more unit than integration than E2E)?

---

## Confidence score

- Week 10 confidence (1–10):
- Reason for that score:
- The testing habit I will keep doing automatically:
- The one thing I still find confusing:

---

## Preparation for Week 11

- [ ] I trust the test suite enough to safely add ML code.
- [ ] I know how to write a test before I write the feature.
- [ ] I understand what coverage tells me and what it does not.
- [ ] I am ready to learn TF-IDF and scikit-learn next week.
