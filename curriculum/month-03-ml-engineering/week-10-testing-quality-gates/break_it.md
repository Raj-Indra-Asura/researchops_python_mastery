# Break It — Week 10 Testing Discipline and Quality Gates

These experiments teach you what goes wrong when testing discipline breaks down. Do each one deliberately, observe the result, restore the code, and write what you learned.

---

## Experiment 1: Delete a fixture and watch the cascade

In `tests/unit/test_ingestion_service.py`, delete the `paper_repo` fixture (or rename it to `paper_repo_x`).

Run:

```bash
pytest tests/unit/test_ingestion_service.py -v
```

**What to observe:** pytest shows a `ERRORS` block, not a `FAILED` block. Every test that depends on `paper_repo` (directly or through other fixtures) reports a fixture error.

**Question to answer:** How many tests failed? Which ones failed by fixture error versus by assertion error? What does this tell you about the blast radius of a broken fixture?

**Restore before continuing.**

---

## Experiment 2: Lower coverage below the threshold

Find the coverage threshold in `pyproject.toml`. Then deliberately delete three test methods from `tests/unit/test_ingestion_service.py`.

Run:

```bash
pytest --cov=researchops --cov-report=term-missing -q
```

**What to observe:** The output shows lower coverage. If you delete enough tests, `--cov-fail-under` triggers and pytest exits with code 2, not 0.

**Question to answer:** What is the current threshold? By how much did coverage drop? What would the CI report?

**Restore before continuing.**

---

## Experiment 3: Break the CI workflow command

Open `.github/workflows/ci.yml`. Change the ruff command from `ruff check src tests` to `ruff check srcc tests` (typo: `srcc`).

Push to a branch and observe the GitHub Actions run. While waiting, also run locally:

```bash
ruff check srcc tests
```

**What to observe:** The CI step fails immediately with "path not found" or "no such directory." The failure is clear and fast.

**Question to answer:** How quickly did CI report the failure? What would happen if you had not tested this locally first?

**Restore the workflow file before continuing.**

---

## Experiment 4: Monkeypatch the wrong path

Write a test that patches `researchops.parsing.text_cleaner.clean_text` with:

```python
monkeypatch.setattr("researchops.services.ingestion_service.clean_text", lambda _: "PATCHED")
```

But also try:

```python
monkeypatch.setattr("researchops.parsing.text_cleaner.clean_text", lambda _: "PATCHED")
```

**What to observe:** The first patch works. The second might not, depending on how `clean_text` is imported. If `ingestion_service.py` imports `clean_text` as `from researchops.parsing.text_cleaner import clean_text`, you must patch the name as imported, not the original location.

**Question to answer:** What is the difference? This is one of the most common monkeypatch pitfalls. Write an explanation in your own words.

---

## Experiment 5: Create a flaky test

Write a test that stores the current timestamp:

```python
def test_flaky_timing():
    start = datetime.utcnow()
    # some operation
    end = datetime.utcnow()
    assert (end - start).total_seconds() < 0.001  # 1 millisecond
```

Run it 100 times with:

```bash
pytest tests/path/to/test_flaky.py --count=10 -v
# (install pytest-repeat: pip install pytest-repeat)
```

**What to observe:** The test may sometimes fail if the machine is under load. This is a classic flaky test.

**Question to answer:** How do you fix this? (Hint: the fix involves injecting a clock, not measuring real time.)

---

## Debugging tasks

**Task D1: Run a single failing test with maximum detail**

Introduce a deliberate assertion failure in any test (change `== 1` to `== 2`). Run:

```bash
pytest tests/unit/test_ingestion_service.py::TestIngestDirectory::test_ingests_single_pdf -vv -s
```

Look at the diff output. pytest shows the actual versus expected value. This is more informative than a simple assertion error.

**Task D2: Find the slowest tests**

Run:

```bash
pytest --durations=10 -q
```

This shows the 10 slowest tests. Which tests take the longest? Are they unit tests or integration tests? If a unit test appears on this list, it is a sign it might have unintended I/O.

**Task D3: Find tests that are order-dependent**

Run:

```bash
pytest tests/unit/ -v --randomly-seed=last
# (install pytest-randomly: pip install pytest-randomly)
```

Run multiple times with different seeds. If a test sometimes fails depending on order, it has a hidden dependency on test execution order. Find it and fix it.

---

## Edge cases to explore

**EC1: Flaky behavior from shared state**

Create a module-level variable in a test file:

```python
shared_list = []

def test_adds_to_list():
    shared_list.append(1)
    assert len(shared_list) == 1

def test_list_is_empty():
    assert len(shared_list) == 0
```

Run these two tests. What order do they need to run in to both pass? What happens if the order is reversed?

**EC2: Slow test in unit scope**

Write a test in `tests/unit/` that sleeps for 1 second:

```python
import time

def test_that_is_too_slow():
    time.sleep(1)
    assert True
```

Run `pytest tests/unit/ --durations=5`. It appears at the top. This is a problem — unit tests must be fast. Move this test to `tests/integration/` or fix the underlying cause.

**EC3: Environment variable dependency**

Write a test that checks an environment variable without setting it:

```python
import os

def test_reads_env_var():
    path = os.environ["RESEARCHOPS_DB_PATH"]
    assert path.endswith(".db")
```

Run without the variable set. What error do you get? Fix it with `monkeypatch.setenv` in the fixture.

---

## What did you learn?

1. Which quality gate catches the most mistakes in the least time?
2. What made one test brittle when you explored edge cases?
3. Will you run `ruff check src tests && pytest -q` before every commit? Why?
4. What is the difference between a test that documents behavior and a test that documents implementation?
5. What would you add to the quality gate if you were the tech lead on this project?
