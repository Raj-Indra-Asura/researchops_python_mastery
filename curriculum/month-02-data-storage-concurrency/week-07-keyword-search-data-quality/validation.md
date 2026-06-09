
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 7 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation - Week 07 Keyword Search and Data Quality

## 1. Pre-validation checklist
- [ ] Run from the repository root.
- [ ] Know the Week 7 milestone.
- [ ] Know this week is keyword search and data quality, not future retrieval work.
- [ ] Identify `src/researchops/services/search_service.py`.
- [ ] Identify `src/researchops/services/paper_service.py`.
- [ ] Identify `tests/unit/test_search_service.py`.
- [ ] Identify `tests/unit/test_paper_service.py`.
- [ ] Understand why `FakePaperRepository` is used.
- [ ] Understand blank query versus no-match query.
- [ ] Understand why stored-data quality affects search.
- [ ] Confirm no future retrieval or concurrency internals were added.
- [ ] Confirm service logic is not in the CLI.
- [ ] Confirm core does not import infrastructure.
- [ ] Install editable dependencies before CLI validation.
- [ ] Be ready to explain one result score by hand.

## 2. Commands to run
```bash
python -m pip install -e ".[dev,storage]"
researchops --help
pytest tests/unit/test_search_service.py -v
pytest tests/unit/test_paper_service.py -v
researchops search "machine learning"
researchops papers stats
pytest -q
```

Week 7 syllabus validation command:
```bash
researchops search "machine learning"
researchops papers stats
pytest tests/unit/test_search_service.py -v
```

Run targeted tests before the full suite. If your local CLI exposes paper statistics under a slightly different command shape, use the implemented stats command and update the docs when behavior changes.

## 3. Expected outputs
### Editable install
- Completes successfully.
- Makes `researchops` available.
- Does not add heavy future-week dependencies.

### Help command
- Displays CLI help.
- Search and paper/statistics commands are visible or discoverable.

### Search unit tests
- Title search passes.
- Body text search passes.
- No-match returns empty list.
- Blank query raises `EmptyQueryError`.
- Results sort by score descending.
- Limits are respected.
- Snippets are present.

### Paper service tests
- Existing lookup works.
- Missing lookup raises the expected error.
- Empty list and empty stats are safe.
- Paper, word, and page totals are correct.

### Search CLI
- Matching papers are ranked.
- No-match state is explicit.
- Empty library does not crash as a normal state.

### Paper stats CLI
- Stored-paper totals are displayed.
- Word/page totals are plausible.
- Output helps judge data quality.

### Full suite
- All existing behavior remains green.
- Week 7 does not break previous weeks.

## 4. Tests that must pass
Required files:
- `tests/unit/test_search_service.py`
- `tests/unit/test_paper_service.py`

- `TestSearch.test_finds_matching_paper_by_title`
- `TestSearch.test_finds_matching_paper_by_text`
- `TestSearch.test_no_match_returns_empty`
- `TestSearch.test_empty_query_raises`
- `TestSearch.test_results_ordered_by_score_descending`
- `TestSearch.test_limit_is_respected`
- `TestSearch.test_result_has_snippet`
- `TestSearch.test_snippet_extracted_from_text`
- `TestSearchWithEmptyRepo.test_empty_repo_returns_empty_list`
- `TestExtractSnippet.test_snippet_for_term_at_start`
- `TestExtractSnippet.test_snippet_for_term_not_found`
- `TestExtractSnippet.test_snippet_uses_ellipsis_for_mid_text`
- `TestGetPaper.test_returns_paper_by_id`
- `TestGetPaper.test_raises_when_not_found`
- `TestListPapers.test_empty_when_no_papers`
- `TestListPapers.test_returns_all_saved_papers`
- `TestStats.test_empty_stats`
- `TestStats.test_counts_papers_words_pages`

## 5. Manual checks
- [ ] Search a word in a known title.
- [ ] Search a word in known body text.
- [ ] Search a query that should not match.
- [ ] Try extra query spaces.
- [ ] Try different casing.
- [ ] Try a blank query.
- [ ] Inspect result order.
- [ ] Inspect snippets.
- [ ] Run paper stats.
- [ ] Compare stats to known data.
- [ ] Investigate zero words with nonzero papers.
- [ ] Check duplicate-looking results.
- [ ] Check `Untitled` results as quality warnings.
- [ ] Confirm no normal user state shows a traceback.
- [ ] Explain one score aloud.

## 6. Architecture checks
- [ ] Core protocols stay in `core/interfaces.py`.
- [ ] Core models do not import CLI/API/storage/ML/workers/search infrastructure.
- [ ] Search service depends on protocols and models.
- [ ] Search service does not construct SQLite directly.
- [ ] CLI delegates to services.
- [ ] Stats behavior belongs in service logic.
- [ ] Fakes live under `tests/fakes/`.
- [ ] Unit tests avoid real DB/PDF/network.
- [ ] SQLite LIKE/FTS discussion remains keyword-search focused.
- [ ] No future retrieval feature is introduced.
- [ ] No concurrency feature is introduced.
- [ ] No Week 8 internals are introduced.
- [ ] Import graph points inward.
- [ ] Service code remains beginner-readable.
- [ ] Tests document behavior.

## 7. Documentation checks
- [ ] QUICKREF is preserved verbatim.
- [ ] NAV blocks are preserved verbatim.
- [ ] Notes are one unified chapter.
- [ ] Notes have no LEARNING_FORMAT block.
- [ ] Notes have no Existing detailed notes wrapper.
- [ ] Notes contain all 20 required sections in order.
- [ ] Validation contains all 10 sections.
- [ ] Commands match Week 7 syllabus intent.
- [ ] Real test names are listed.
- [ ] Expected outputs are specific.
- [ ] Manual checks are actionable.
- [ ] Architecture checks name boundaries.
- [ ] Warnings block future-week leakage.
- [ ] Definition of done is strict.
- [ ] Docs mention keyword search and data quality throughout.

## 8. Do-not-proceed warnings
- ⚠️ Do not proceed if search unit tests fail.
- ⚠️ Do not proceed if paper service tests fail.
- ⚠️ Do not proceed if blank query is not explicit.
- ⚠️ Do not proceed if no-match crashes.
- ⚠️ Do not proceed if ranking is undefined.
- ⚠️ Do not proceed if title/body search is broken.
- ⚠️ Do not proceed if service imports concrete storage.
- ⚠️ Do not proceed if CLI owns scoring.
- ⚠️ Do not proceed if core imports outward.
- ⚠️ Do not proceed if stats crash on empty repo.
- ⚠️ Do not proceed if docs still have split notes.
- ⚠️ Do not proceed if future retrieval features were added.
- ⚠️ Do not proceed if unrelated concurrency features were added.
- ⚠️ Do not proceed if Week 8 internals were added.
- ⚠️ Do not proceed if you cannot explain the flow.

## 9. Ruthless mentor checkpoint
- [ ] Can you trace query to result?
- [ ] Can you define normalization?
- [ ] Can you compute a simple score?
- [ ] Can you explain ranking?
- [ ] Can you distinguish blank query from no match?
- [ ] Can you name the search service?
- [ ] Can you name the search result model?
- [ ] Can you explain fake repositories?
- [ ] Can you explain data-quality gates?
- [ ] Can you interpret paper stats?
- [ ] Can you explain SQLite LIKE?
- [ ] Can you explain SQLite FTS?
- [ ] Can you explain why FTS is still keyword full-text search?
- [ ] Can you name Week 7 tests?
- [ ] Can you name what belongs to later retrieval weeks instead?

## 10. Definition of done
- [ ] Notes are unified.
- [ ] Notes have 20 required sections.
- [ ] Notes are 800+ lines.
- [ ] Validation has 10 sections.
- [ ] Validation is 280+ lines.
- [ ] QUICKREF and NAV are preserved.
- [ ] Syllabus commands are included.
- [ ] Real test names are included.
- [ ] Search tests pass when run by learner.
- [ ] Paper service tests pass when run by learner.
- [ ] CLI search behavior is manually checked.
- [ ] Paper stats behavior is manually checked.
- [ ] Architecture boundaries are intact.
- [ ] No future-week features leaked in.
- [ ] Learner can explain the feature aloud.

### Troubleshooting reference
| Symptom | Likely cause | First move |
|---|---|---|
| No search results | Empty corpus or mismatch | Run stats and inspect normalized text |
| Wrong order | Score/tie issue | Inspect IDs and scores |
| Blank query accepted | Missing validation | Check `EmptyQueryError` path |
| Stats wrong | Fixture or word count issue | Inspect fake papers |
| Import error | Editable install or path issue | Reinstall editable package |
| Docs mention future retrieval features | Future topic leak | Replace with keyword/FTS wording |

### Evidence log prompts
Use these prompts to decide whether validation evidence is strong enough.
- [ ] I can name the exact command that proves search-service behavior.
- [ ] I can name the exact command that proves paper-service stats behavior.
- [ ] I can describe the expected result of a matching search.
- [ ] I can describe the expected result of a no-match search.
- [ ] I can describe the expected result of a blank search.
- [ ] I can describe what a suspicious zero-word library means.
- [ ] I can explain why the CLI is not the owner of ranking rules.
- [ ] I can explain why the repository is not the owner of presentation rules.
- [ ] I can explain why `SearchResult` is better than returning raw tuples.
- [ ] I can explain why snippets should be readable rather than fully normalized.
- [ ] I can explain why `LIKE` is easy but limited.
- [ ] I can explain why FTS is storage-backed keyword search.
- [ ] I can explain why a fake repository is enough for service unit tests.
- [ ] I can explain when a real SQLite test would be appropriate.
- [ ] I can explain one data-quality warning in beginner language.
- [ ] I can explain one ranking limitation in beginner language.
- [ ] I can explain one architecture boundary in beginner language.
- [ ] I can explain one recovery step for each common failure below.

### Common failure recovery checks
- [ ] If install fails, inspect dependency groups before changing code.
- [ ] If help fails, inspect package entry points before changing search code.
- [ ] If title search fails, inspect haystack construction.
- [ ] If body search fails, inspect whether `paper.text` is included.
- [ ] If no-match crashes, inspect normal empty-result handling.
- [ ] If blank query succeeds, inspect `EmptyQueryError` handling.
- [ ] If ordering fails, inspect scores before changing sort order.
- [ ] If limit fails, inspect slicing after sorting.
- [ ] If snippets fail, inspect `_extract_snippet` separately from scoring.
- [ ] If empty stats fail, inspect `PaperService.stats()` with an empty fake repository.
- [ ] If word totals fail, inspect `Paper.word_count()` and fixture text.
- [ ] If page totals fail, inspect fixture `num_pages` values.
- [ ] If CLI search fails but service tests pass, inspect wiring and database path.
- [ ] If docs and CLI disagree, update the relevant validation command.
- [ ] If a future-week idea appears, remove it and return to keyword search.
- [ ] If you cannot explain a failure, reduce to one query and one paper.
- [ ] If the full suite fails, start with the first failing targeted test.
- [ ] If everything passes but behavior is unclear, improve documentation before moving on.

<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
