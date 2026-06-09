<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

---
<!-- NAV_END -->

# Exercises - Week 10 Testing Discipline and Quality Gates

## 1. How to use this workbook
- This workbook is the hands-on path for Week 10 testing discipline and quality gates.
- Work from warm-ups toward brutal exercises; later tiers assume earlier habits are comfortable.
- Use behavior-focused test names, not ticket numbers or vague names like `test_case_1`.
- Use `tests/fakes/` for fake implementations of ResearchOps protocols.
- Use `tmp_path` for file and SQLite tests so no exercise depends on local machine state.
- Use `monkeypatch` for environment variables and hard-to-trigger failure paths, not as a substitute for clean dependency injection.
- The exact lint gate is `ruff check src tests`.
- The exact test gate is `pytest --cov=researchops --cov-report=term-missing -q`.
- The coverage floor is 70 percent through configuration.
- Do not introduce classical ML model code, embeddings, FastAPI, async patterns, or new heavy dependencies.
- Written answers belong in scratch notes unless your mentor explicitly asks for a committed file.

## 2. Warm-up exercises
### W10-W1: Classify the current tests
- List five tests from `tests/unit/`, two tests from `tests/integration/`, and one test from `tests/e2e/` if present.
- For each test, write whether it is unit, integration, or E2E smoke.
- Justify the classification by naming the real dependency or fake dependency involved.
- If a test classification is unclear, write what change would make the test boundary clearer.
### W10-W2: Write a fixture chain
- Create a local test fixture named `empty_paper_repo` that returns a fresh `FakePaperRepository`.
- Create `paper_repo_with_one_paper` that depends on `empty_paper_repo` and saves one paper.
- Create `paper_repo_with_three_papers` that depends on `empty_paper_repo` and saves three papers.
- Write one test per fixture proving the expected count.
- Explain why function scope keeps the fixtures from contaminating each other.
### W10-W3: Parametrize text normalization cases
- Find a current text-cleaning or search-normalization function.
- Write a parametrized test with at least six cases: mixed case, leading spaces, trailing spaces, repeated spaces, empty string, and punctuation or hyphenated text.
- Each case must include the raw input and exact expected output.
- If one case fails, the others should still report independently.
### W10-W4: Use tmp_path for one file behavior
- Write a test that creates a text file under `tmp_path`.
- Call a ResearchOps helper or tiny local helper that reads from the path.
- Assert exact content, not only that something was returned.
- Do not manually delete the file.
### W10-W5: Use monkeypatch for one environment variable
- Find a setting that can read an environment variable, or write a tiny test-only helper if no setting exists.
- Use `monkeypatch.setenv` before constructing the settings object.
- Assert the override is used.
- Add a second case with `monkeypatch.delenv` if default behavior is part of the contract.

## 3. Code-reading exercises
### W10-R1: Map fakes to protocols
- Open `tests/fakes/` and list each fake class.
- For each fake, identify the protocol, service collaborator, or production concept it stands in for.
- Write which test files import the fake.
- Write one method the fake must keep accurate so service tests do not lie.
### W10-R2: Read one service test as a specification
- Open a service test such as ingestion, paper, or search service tests.
- For five tests, label Arrange, Act, and Assert lines.
- Write the behavior sentence communicated by each test name.
- Identify one assertion that could be more precise, or explain why all five are already precise.
### W10-R3: Inspect SQLite integration boundaries
- Open the SQLite repository integration tests.
- Find where the test database path is created.
- Confirm the path is isolated under `tmp_path` or an equivalent pytest-managed fixture.
- List which repository behaviors are covered: save, get, list, exists, update, delete, or schema creation.
- Name one persistence behavior that still deserves coverage.
### W10-R4: Read pyproject quality configuration
- Open `pyproject.toml`.
- Find pytest options, coverage run options, coverage report options, and Ruff options.
- Write the exact location of the 70 percent coverage floor.
- Explain whether the coverage command relies on command-line flags, configuration, or both.
### W10-R5: Read CI as a contract
- Open `.github/workflows/ci.yml` if present.
- Write the exact lint command used by CI.
- Write the exact pytest command used by CI.
- If the commands differ from Week 10 requirements, write the mismatch clearly.
- Explain why a learner should be able to reproduce CI locally.

## 4. Implementation exercises
### W10-I1: Create only useful shared fixtures
- Find duplicated fake repository setup across at least two test files.
- Move the duplicated setup to `tests/conftest.py` only if it improves readability.
- Keep single-use fixtures local to their test module.
- Use function scope unless the fixture is immutable or explicitly reset.
- Update tests to request fixtures by parameter name.
### W10-I2: Complete KeywordSearchService behavior coverage
- Use `FakePaperRepository` to arrange controlled papers.
- Cover empty query behavior with the project exception if one exists.
- Cover no-match behavior returning an empty list.
- Cover one-match and multi-match behavior.
- Cover score ordering if ordering is part of the service contract.
- Cover limit behavior with more matches than the limit.
### W10-I3: Add a real SQLite delete/list integration test
- Create a database path under `tmp_path`.
- Initialize the real SQLite repository schema.
- Save three papers with distinct IDs.
- Delete one paper through the repository API.
- Assert `list_all()` returns exactly the remaining two IDs.
- Assert `exists()` is false for the deleted ID if that API exists.
### W10-I4: Test ingestion unexpected failure recording
- Arrange fakes for paper and failure repositories.
- Use a fake parser or `monkeypatch` so parsing raises `RuntimeError`.
- Run the ingestion behavior for one controlled path.
- Assert a failure record is stored with error type `RuntimeError`.
- Assert the failed path or paper identifier is recorded if the failure model stores it.
- Do not use a real PDF in this unit test.
### W10-I5: Align the quality gate configuration
- Confirm Ruff checks both `src` and `tests`.
- Confirm pytest coverage measures `researchops`.
- Confirm terminal missing-line reporting is enabled by command or configuration.
- Confirm coverage fails under 70 percent.
- Do not change unrelated tooling or add future-week dependencies.

## 5. Testing exercises
### W10-T1: Run the narrowest possible feedback loop
- Choose one test you added or edited.
- Run that single test by path and test name during normal practice.
- If it fails, classify the failure as import, fixture, assertion, runtime, or configuration.
- Fix the narrow failure before running broad commands.
### W10-T2: Compare unit and integration feedback
- Run unit tests during normal practice.
- Run integration tests during normal practice.
- Record which set is faster and why.
- Write one sentence explaining why both levels are still useful.
### W10-T3: Interpret coverage missing lines
- Run `pytest --cov=researchops --cov-report=term-missing -q` during normal practice.
- Choose three missing line ranges from the report.
- For each range, classify it as happy path, failure path, defensive branch, or future-week stub.
- Write one meaningful test for the highest-value missing behavior.
### W10-T4: Treat Ruff failures as product failures
- Run `ruff check src tests` during normal practice.
- If Ruff reports unused imports in tests, remove them.
- If Ruff reports import ordering, fix ordering rather than ignoring the rule.
- Explain why test code should be held to a quality gate.
### W10-T5: Verify the full Week 10 gate
- Run `ruff check src tests`.
- Run `pytest --cov=researchops --cov-report=term-missing -q`.
- Confirm coverage is at least 70 percent.
- If either command fails, write the first failing file and the first corrective action.

## 6. Debugging exercises
### W10-D1: Break fixture discovery safely
- Change one test parameter to a fixture name that does not exist.
- Run that single test during normal practice.
- Read the fixture-not-found message and note the available fixture list if pytest shows it.
- Restore the correct parameter name.
- Explain why pytest uses exact names rather than guessing.
### W10-D2: Expose mutable fixture leakage
- In a scratch test, create a module-scoped list fixture.
- Write two tests that append different values.
- Observe how shared state can make the second test depend on the first.
- Change the fixture to function scope and observe the difference.
- Remove the scratch test or leave only the corrected educational version if appropriate.
### W10-D3: Patch the wrong lookup location
- Write a small monkeypatch test that patches a function where it is defined but not where it is imported by the code under test.
- Observe that the original function may still run.
- Patch the object where the code under test actually looks it up.
- Write the rule: patch the lookup location, not the place you first found the function.
### W10-D4: Understand assertion diffs
- Temporarily change one expected list of IDs to the wrong order.
- Run the test during normal practice.
- Read how pytest displays the expected and actual values.
- Restore the correct assertion.
- Explain why exact assertions make failures easier to diagnose.
### W10-D5: Handle coverage failure honestly
- Reason about or temporarily simulate a coverage failure without committing the simulation.
- Do not lower the threshold as the first response.
- Open missing lines and decide whether they represent meaningful behavior.
- Add a meaningful test or justify why the line should not count if it is truly unreachable.

## 7. Refactoring exercises
### W10-F1: Extract a paper factory for tests
- Find repeated `Paper` construction in tests.
- Create a small test helper named like `make_paper` in the test module or shared fixture area.
- Give it clear defaults for ID, title, and text.
- Allow tests to override the fields that matter for the behavior.
- Do not move test factories into production code.
### W10-F2: Move fixtures without hiding intent
- Choose two duplicated fixtures and one single-use fixture.
- Move only the duplicated fixtures to `tests/conftest.py`.
- Keep the single-use fixture near its test.
- Explain why hidden global fixture setup can harm readability.
### W10-F3: Replace monkeypatch with fakes where possible
- Find or create a test that monkeypatches a ResearchOps-owned repository method.
- Rewrite it to use a fake repository passed through normal construction.
- Compare which version better communicates the service dependency.
- Keep the clearer version.
### W10-F4: Split a multi-act test
- Find a test that calls the system under test more than once for different reasons.
- Split it into focused behavior tests.
- Give each new test a precise behavior name.
- Keep shared setup in a fixture only if it remains easy to read.
### W10-F5: Strengthen weak assertions
- Find an assertion like `assert result` or `assert result is not None`.
- Replace it with an exact count, exact ID, exact exception, exact status, or exact order.
- Explain what regression the stronger assertion would catch.

## 8. Written explanation exercises
1. Explain the difference between a fake, a mock, and a real infrastructure dependency in ResearchOps terms.
2. Explain why service unit tests should usually use fakes instead of SQLite.
3. Explain why SQLite still needs integration tests with `tmp_path`.
4. Explain fixture scope using a mutable fake repository example.
5. Explain when `monkeypatch.setenv` is the right tool.
6. Explain one situation where monkeypatch would make a test more fragile.
7. Explain what `pytest --cov=researchops --cov-report=term-missing -q` tells you.
8. Explain why coverage above 70 percent is not automatically good testing.
9. Explain why lowering `fail_under` is usually the wrong response to a red gate.
10. Explain why Ruff should check tests as well as source.
11. Explain what a flaky test does to team trust.
12. Explain why Week 10 must not add classical ML, embeddings, FastAPI, or async behavior.

## 9. Stretch exercises
### W10-S1: Coverage improvement plan with judgment
- Run the coverage command during normal practice.
- Select five missing line ranges from different modules if possible.
- For each range, inspect the source and write what behavior is missing.
- Reject ranges that are future-week stubs unless they affect current behavior.
- Implement tests for the two highest-value current behaviors.
- Your tests must assert exact outcomes, not merely execute lines.
### W10-S2: Fake contract tests
- Choose one fake in `tests/fakes/`.
- Write tests proving it satisfies the core operations services rely on.
- For a repository fake, cover save, list, exists, and delete if available.
- Do not assert private storage details unless no public behavior can express the contract.
- Explain how fake contract tests prevent misleading unit tests.
### W10-S3: Slow marker policy
- Identify any tests that are slow for a real reason, not because of accidental inefficiency.
- Add a `slow` marker only if the distinction helps local workflow.
- Document the marker in pytest configuration if used.
- Ensure CI still runs the full required gate unless the project explicitly changes policy.
- Explain why hiding slow tests can hide real regressions.
### W10-S4: Ingestion failure matrix
- List at least six ingestion failures: parse error, unexpected exception, duplicate paper, missing file, empty text, repository save failure, or invalid metadata.
- For each failure, choose fake, `tmp_path`, or monkeypatch as the safest tool.
- Implement two missing failure tests.
- Assert stored failure type and location precisely.
- Do not use real PDFs unless the exercise is explicitly integration-level.
### W10-S5: Beginner-readable CI logs
- Read the CI workflow.
- Ensure lint and coverage run as separate named steps.
- Preserve the exact commands required for Week 10.
- Do not add services, model training, embedding generation, or web server startup.
- Explain how named CI steps help a beginner fix the first failure faster.

## 10. Brutal exercises
### W10-B1: Order independence audit
- Audit ten tests and identify every piece of state each test depends on.
- Mark any state that could come from another test, the working directory, environment variables, or an existing database.
- Refactor at least three risks using fixtures, fakes, `tmp_path`, or monkeypatch.
- Write a short isolation report naming the exact risk removed from each test.
### W10-B2: Behavior proof over call-count proof
- Find a test that could be written as a call-count assertion.
- Write the call-count version in scratch notes, then reject it unless the call count is truly user-visible behavior.
- Implement a state-based or result-based assertion instead.
- Explain why the behavior proof is more robust during refactoring.
### W10-B3: Dangerous failure without real damage
- Choose a failure that would be unsafe to trigger with real infrastructure, such as repository write failure or parser explosion.
- Use a fake or monkeypatch to trigger it safely.
- Assert the service records or raises the correct failure.
- Prove no real database, real PDF, network, or permanent file is needed.
### W10-B4: Coverage without vanity
- Pick one missing branch that matters to current ResearchOps behavior.
- Write a test that would fail if the branch regressed.
- Write a paragraph explaining why the branch matters.
- Also identify one missing line you deliberately did not test and justify the decision.
- The goal is judgment, not a perfect percentage.
### W10-B5: Clean-checkout contributor simulation
- Pretend you have no local database, no sample files, and no special environment variables.
- Read the tests and identify anything that assumes hidden local state.
- Replace those assumptions with fixtures, fakes, `tmp_path`, or monkeypatch.
- Explain how the suite now teaches its own setup requirements.
### W10-B6: Quality gate failure response drill
- Imagine CI fails at Ruff, then imagine it fails at coverage, then imagine it fails at one integration test.
- For each failure, write the first three investigation steps.
- Include the command you would run locally, the file you would open, and the kind of fix you would expect.
- Do not include lowering thresholds, skipping tests, or adding future-week dependencies as first responses.

## 11. Mini project task
- Build a coherent Week 10 quality gate story for ResearchOps.
- Ensure shared fixtures exist only where they reduce real duplication.
- Ensure service tests use fakes for project protocols.
- Ensure at least one real SQLite integration flow uses `tmp_path`.
- Ensure at least one controlled failure path uses a fake or monkeypatch appropriately.
- Ensure parametrized tests cover repeated edge cases in search, text, paths, or settings.
- Ensure `ruff check src tests` is documented or configured as the lint gate.
- Ensure `pytest --cov=researchops --cov-report=term-missing -q` is the coverage gate.
- Ensure coverage fails under 70 percent.
- Ensure no classical ML model code, embeddings, FastAPI, async behavior, or new heavy dependency appears.
- Write a final scratch-note explanation of what the gate proves and what it does not prove.

## 12. Completion checklist
- [ ] I can classify ResearchOps tests by level and justify the classification.
- [ ] I can write and request a pytest fixture by name.
- [ ] I can explain function, module, and session fixture scope.
- [ ] I can use `tmp_path` for isolated files and SQLite databases.
- [ ] I can use `monkeypatch` for environment variables and hard failure paths.
- [ ] I can choose a fake instead of monkeypatch when dependency injection is available.
- [ ] I can keep fakes in `tests/fakes/` and align them with protocols.
- [ ] I can write parametrized edge-case tests.
- [ ] I can strengthen weak assertions into behavior assertions.
- [ ] I can read coverage missing-line output.
- [ ] I can explain the 70 percent coverage floor.
- [ ] I can run `ruff check src tests` during normal validation.
- [ ] I can run `pytest --cov=researchops --cov-report=term-missing -q` during normal validation.
- [ ] I can explain why CI failures are blockers.
- [ ] I can avoid adding Week 11 or later concepts during Week 10 work.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Notes](notes.md) · ➡️ [Break It →](break_it.md)

**Week 10 — Testing and Quality Gates:** [README](README.md) · [Notes](notes.md) · **Exercises** · [Break It](break_it.md) · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 3: Advanced Python and ML Engineering](../README.md)
---
<!-- NAV_BOTTOM_END -->
