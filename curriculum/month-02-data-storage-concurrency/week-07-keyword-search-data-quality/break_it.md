<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

---
<!-- NAV_END -->

# Break It — Week 07 Keyword Search and Data Quality

## Purpose of failure practice

Week 7 failures are about search trust. Keyword search can fail quietly: a paper is present, but case differences, punctuation, Unicode artifacts, empty queries, bad scoring, or boilerplate text hide the result from the learner. Data quality checks also fail quietly when duplicate or empty papers look like valid rows.

These labs force you to make those quiet failures visible. When you can explain why a query returned zero results, why a snippet looks wrong, or why a duplicate matters, you are ready to make ResearchOps search useful instead of merely available.

## Failure lab rules

1. Keep the starting paper set tiny so you can calculate scores by hand.
2. Record the raw query, normalized query, raw paper text, and normalized haystack for each confusing search.
3. Treat blank query behavior and no-match behavior as different cases.
4. Do not fix ranking by hard-coding a test result; fix the scoring rule or the normalization rule.
5. If a data-quality check fails, identify whether the data is bad or the checker is too strict.
6. Stay in keyword search for Week 7; do not replace these labs with later retrieval techniques.

---

## Intentional break experiments

Work through the scenarios below one at a time. Each one asks you to cause a failure, inspect what happened, fix it, and name the test or check that should catch it in ResearchOps.

---

## Scenario 1 — Case mismatch without normalization

**Setup:** Save a paper with title `"Transformer Models"` and text containing the word `"Transformer"` (uppercase T).

**Break it:**
1. Implement a search WITHOUT `normalise_for_search`.
2. Search for `"transformer"` (lowercase).

**Expected result:** Score of 0. No results returned.

**What to observe:**
- `"Transformer".count("transformer")` is 0 in Python.
- Case-sensitive matching is the default.

**Fix:** Apply `normalise_for_search` to both the document text and the query before counting.

**Verify the fix:** After applying normalization, the same search should return the paper.

---

## Scenario 2 — Punctuation in query

**Setup:** Save a paper about `"self-attention"` mechanisms.
The text contains `"self-attention"` many times.

**Break it:** Search for `"self-attention"` as the query.

**What to observe:**
- `normalise_for_search("self-attention")` → `"self attention"` (hyphen removed, split into two terms).
- `normalise_for_search("...self-attention...")` → `"...self attention..."` (same treatment in document).
- The search for tokens `["self", "attention"]` actually works correctly here.

**Now break it differently:** Search for `"self–attention"` with an em-dash (`–`) instead of a regular hyphen (`-`).

**What to observe:**
- Both dashes are removed by punctuation stripping.
- The result is the same query `["self", "attention"]`.
- Normalization handles this case correctly.

**Lesson:** Normalization makes the system robust to punctuation variations in both queries and documents.

---

## Scenario 3 — Empty query

**Break it:**
```python
service.search("")       # empty string
service.search("   ")   # whitespace only
service.search("\t\n")  # tabs and newlines
```

**Expected behavior:** All three should raise `EmptyQueryError`.

**What to observe if you forgot the check:**
- `"".strip()` is falsy.
- `normalise_for_search("").split()` returns `[]` (empty list).
- `sum(...)` over an empty list of terms returns 0.
- Every paper gets score 0.
- No results returned.
- No error raised.

This is a silent failure: the user gets an empty result with no explanation.

**Fix:** Check for empty query before tokenizing.

---

## Scenario 4 — Query with only stopwords

**Setup:** You have implemented stopword filtering.
Your stopword list includes `"the"`, `"is"`, `"a"`.

**Break it:** Search for `"the"`.

**What to observe with stopword filtering:**
- `"the"` is removed from the query tokens.
- The token list is empty after filtering.
- You get a silent empty result (or an error if you check for empty tokens).

**Expected behavior:** Searching for only stopwords should either:
- Return an empty result with a helpful message (`"Query contains only stopwords"`), OR
- Fall back to searching without stopword filtering.

**Lesson:** Stopword filtering requires handling the edge case where all query tokens are removed.

---

## Scenario 5 — The singular/plural mismatch

**Setup:** Save a paper about `"neural networks"` (plural).

**Break it:** Search for `"neural network"` (singular).

**What to observe:**
- `normalise_for_search` does not do stemming.
- `"networks"` does not match `"network"`.
- Score is 0 for the `"network"` term.
- The `"neural"` term does match.
- Total score is the count of `"neural"` only.

**Experiment:**
1. How many results does `"neural network"` return?
2. How many does `"neural networks"` return?
3. Are they the same results?

**Discuss:** This is the fundamental limitation of exact token matching.
Write a one-paragraph explanation of why you would need stemming to fix this, and what stemming does conceptually.

---

## Scenario 6 — Index all papers for every query

**Setup:** In an earlier exercise, imagine you wrote a version where every paper is loaded and scored from scratch for each query.

**Break it:** Populate the database with 1000 papers.
Run 100 queries in a loop.
Time the total duration.

**What to observe:**
- Each query loads 1000 papers from SQLite.
- Each load involves disk I/O and row-to-object conversion.
- For 100 queries: 100 × 1000 paper loads.

**This is the correct approach for now** — do not optimize prematurely.
But timing it teaches you when to start worrying.

**Discuss:** At what paper count would you expect the search to become noticeably slow (more than 1 second per query)?
What would you do to fix it?

---

## Scenario 7 — High-repetition boilerplate text

**Setup:** Create a paper where the extracted text is:
```
Page 1 of 50 - ResearchOps Journal
Page 2 of 50 - ResearchOps Journal
Page 3 of 50 - ResearchOps Journal
...
```
(repeat 50 times, with very little actual content)

**Break it:** Search for `"researchops"`.

**What to observe:**
- This paper gets a very high score for `"researchops"`.
- It may outrank papers with actual relevant content about ResearchOps.

**Discuss:** How would your quality check detect this?
What is the `unique_ratio` for this text?
Is flagging this paper helpful, or would it cause false positives for legitimate papers with repeated structures (e.g., legal documents)?

---

## Scenario 8 — Score tie-breaking

**Setup:** Create two papers with identical scores for a query.

**Break it:** Run the search twice.
Are the results in the same order both times?

**What to observe:**
- Python's `list.sort()` is stable.
- If two items have the same key, they stay in their original order.
- The original order is the order returned by `list_all()`, which is `ORDER BY created_at DESC`.
- So tie-breaking is currently by creation date (newest first).

**Is this correct behavior?** Discuss.
What tie-breaking rule would you prefer?
Add a secondary sort to enforce your preferred rule.

---

## Scenario 9 — Unicode ligatures

**Setup:** Create a paper whose extracted text contains `"ﬁeld experiments"` where `ﬁ` is the fi-ligature character (U+FB01).

**Break it (without NFKC normalization):**
Search for `"field"`.

**What to observe:**
- `"field"` (two characters: f + i + e + l + d) is different from `"ﬁeld"` (ligature + e + l + d).
- They do not match.
- Score is 0.

**Fix:** Apply `unicodedata.normalize("NFKC", text)` before further processing.
This converts `ﬁ` to `fi`.

**Verify:** After normalization, `"field"` matches `"ﬁeld"`.

---

## Scenario 10 — SHA-256 collision experiment

**Setup:** This is a thought experiment, not actual code.

SHA-256 has never had a confirmed collision found (as of the time of writing).
However, in theory, two different inputs could produce the same hash.

**Question:** If two different PDF files had the same SHA-256 hash (a collision), what would happen in a deduplication system that uses the hash as a unique ID?

**Answer to think through:**
- The system would treat them as the same file.
- Only one of them would be stored.
- The other would be silently skipped.
- You could never retrieve the skipped file because its hash points to the wrong paper.

**Lesson:** In practice, SHA-256 collisions are astronomically unlikely (there are more possible SHA-256 hashes than atoms in the observable universe).
But in cryptographic contexts, this theoretical risk matters.
For a research library ID system, it is irrelevant.

---

## Edge cases to explore

1. **Search with 10,000 character query:** What happens? Is there a maximum query length?
   Does performance degrade?

2. **Paper with only numbers in text:** A table of data with no words.
   What does `normalise_for_search` return?
   What is the word count?

3. **Snippet at position 0:** The query term is the very first word of the text.
   Does your snippet include a leading `"…"`?
   It should not.

4. **Snippet at the very end:** The query term appears only in the last 10 characters of a very long text.
   Is the snippet computed correctly?
   Does it extend beyond the text boundaries?

5. **Query with numbers:** `search("2017")` should match papers published in 2017 if their text contains `"2017"`.
   Verify this works.

6. **Limit of 0:** `service.search("transformer", limit=0)`.
   What should this return?
   Is `[]` the correct answer?

7. **Limit larger than results:** `service.search("transformer", limit=1000)` when only 3 papers match.
   Should return all 3, not crash.

---

## Debugging checklist

- [ ] Is the query blank before or after normalization?
- [ ] What are the exact normalized query terms?
- [ ] What is the normalized haystack for the paper you expected to match?
- [ ] Does punctuation, case, whitespace, or Unicode explain the mismatch?
- [ ] Is the score zero because the term is absent or because the scorer is wrong?
- [ ] Are results sorted before the limit is applied?
- [ ] Does the snippet search use comparable text to the scorer?
- [ ] Do empty repositories and no-match searches return empty lists without crashing?

## Reflection after breaking

1. Which normalization step made the biggest difference to search quality?
2. What query produced unexpected results and why?
3. How does data quality connect directly to search quality?
4. What is the tradeoff between exact matching and substring matching?
5. What would you add to the normalization pipeline for a research library specifically?
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Exercises](exercises.md) · ➡️ [Validation →](validation.md)

**Week 07 — Keyword Search and Data Quality:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · **Break It** · [Validation](validation.md) · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 2: Storage, Search, Multiprocessing](../README.md)
---
<!-- NAV_BOTTOM_END -->
