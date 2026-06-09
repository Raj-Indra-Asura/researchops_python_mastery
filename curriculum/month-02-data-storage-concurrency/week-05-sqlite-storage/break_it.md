# Break It — Week 05 SQLite Storage Layer

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 2](../README.md) › [Week 5 — SQLite Storage](./README.md) › **break_it.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

Breaking things deliberately is the fastest way to understand constraints, error messages, and edge cases.
Each scenario here asks you to cause a specific failure, observe what happens, and then fix it.

---

## Scenario 1 — The duplicate primary key

**Setup:** Save a paper with `id = "abc123"`.

**Break it:** Try to save another paper with the same `id = "abc123"`.

**Expected error:**
```
sqlite3.IntegrityError: UNIQUE constraint failed: papers.id
```

**What to observe:**
- Which line of your code raises the exception?
- Does the partial write leave any data in the database?
- Open the database with the `sqlite3` CLI and verify no partial rows exist.

**Fix:** The `SQLitePaperRepository.save()` method should call `self.exists(paper.id)` first and raise a domain-specific `DuplicatePaperError` before attempting the insert.

---

## Scenario 2 — The transaction that fails halfway

**Setup:** Create a table `items (id TEXT PRIMARY KEY, name TEXT NOT NULL)` with a related table `item_details (item_id TEXT PRIMARY KEY REFERENCES items(id), description TEXT NOT NULL)`.

**Break it:**
1. Start a transaction.
2. Insert a row into `items`.
3. Attempt to insert a row into `item_details` with an `item_id` that does not exist in `items`.
   (Disable `ON DELETE CASCADE` here so the constraint fires.)

**Expected error:** A foreign key violation.

**What to observe:**
- Is the first insert (into `items`) still present after the exception?
- It should NOT be if you used `with conn:` as the context manager.

**Experiment:** Try the same scenario WITHOUT `with conn:` (manually calling `commit()` after the first insert).
Observe that now the first insert persists even though the second insert failed.
This is the inconsistency that transactions prevent.

---

## Scenario 3 — Forgetting `PRAGMA foreign_keys = ON`

**Setup:** Create the `paper_tags` table with a foreign key to `papers`.
Do NOT call `PRAGMA foreign_keys = ON`.

**Break it:** Insert a row into `paper_tags` with a `paper_id` that does not exist in `papers`.

**Expected behavior (wrong):** The insert succeeds silently.

**What to observe:**
- SQLite does not enforce foreign keys by default.
- This means you can have orphan `paper_tags` rows pointing to non-existent papers.
- This is a subtle data integrity bug that only appears when you later try to query the related paper.

**Fix:** Always enable foreign keys:
```python
conn.execute("PRAGMA foreign_keys = ON")
```

**Why this matters for ResearchOps:** If you delete a paper and foreign keys are not enforced, all its tags remain in `paper_tags` as orphan data.
Search results may include ghost tags from deleted papers.

---

## Scenario 4 — Storing a `Path` object directly

**Setup:** Create a paper where `source_path` is a `Path` object rather than a string.

**Break it:**
```python
paper = Paper(
    id="xyz",
    source_path=Path("papers/attention.pdf"),  # Path, not str
    ...
)
conn.execute(
    "INSERT INTO papers (source_path) VALUES (?)",
    (paper.source_path,),   # Passing Path directly
)
```

**Expected behavior:** The `sqlite3` module does not know how to serialize a `Path` object.
You may see a `sqlite3.InterfaceError` or the value stored may be something unexpected.

**Experiment:**
1. Read the stored value back.
2. Try to create a `Path` from it.
3. Observe whether it round-trips correctly.

**Fix:** Always convert: `str(paper.source_path)`.
When reading back: `Path(row["source_path"])`.

---

## Scenario 5 — No schema initialization

**Setup:** Create a `SQLitePaperRepository` but skip the schema initialization.
Connect to an empty `.db` file and try to call `repo.save(paper)`.

**Expected error:**
```
sqlite3.OperationalError: no such table: papers
```

**What to observe:**
- The error message is very clear.
- The database file exists but has no tables.
- Use the `sqlite3` CLI to confirm: `.tables` should return nothing.

**Fix:** Always call `_init_schema()` in `__init__`.
Use `CREATE TABLE IF NOT EXISTS` to make it idempotent.

---

## Scenario 6 — f-string SQL injection

**Setup:** Build a search function that uses f-string query construction.

```python
def search_title(conn, term):
    return conn.execute(
        f"SELECT * FROM papers WHERE title = '{term}'"
    ).fetchall()
```

**Break it:** Call `search_title(conn, "'; DROP TABLE papers; --")`.

**What to observe:**
- If foreign keys and write protection are not in place, this could destroy your data.
- Even in a safe test environment, observe what SQL is actually being executed.
- Add `conn.set_trace_callback(print)` to see the raw SQL that runs.

**Fix:** Use parameterized queries:
```python
def search_title(conn, term):
    return conn.execute(
        "SELECT * FROM papers WHERE title = ?",
        (term,),
    ).fetchall()
```

---

## Scenario 7 — Skipping `row_factory`

**Setup:** Connect WITHOUT setting `conn.row_factory = sqlite3.Row`.

**Break it:**
```python
conn = sqlite3.connect("test.db")
# No row_factory set
row = conn.execute("SELECT id, title FROM papers LIMIT 1").fetchone()
print(row["title"])   # Try to access by name
```

**Expected error:**
```
TypeError: tuple indices must be integers or slices, not str
```

**What to observe:**
- Without `row_factory`, rows are tuples.
- Column names are unavailable.
- Accessing by index is fragile because adding a column changes every index.

**Fix:**
```python
conn.row_factory = sqlite3.Row
```

---

## Scenario 8 — The missing `commit`

**Setup:** Insert rows into a database without committing.

```python
conn = sqlite3.connect("test.db")
conn.execute("INSERT INTO papers ...")
# No commit, no context manager
conn.close()
```

**Break it:** Open a new connection and query the table.

**What to observe:**
- The data is NOT there.
- Writes without a commit are not persisted to disk.
- The `with conn:` context manager handles this automatically, but if you bypass it, you must call `conn.commit()` manually.

**Variation:** Open two connections to the same file.
Insert via connection 1 (without commit).
Query via connection 2.
Does connection 2 see the data?

---

## Scenario 9 — Creating schema inside every save call

**Setup:** Move the `CREATE TABLE` statement into the `save()` method:

```python
def save(self, paper):
    with self._connect() as conn:
        conn.execute("CREATE TABLE papers (...)")  # <-- wrong place
        conn.execute("INSERT INTO papers ...")
```

**Break it:** Save two papers.

**Expected error:**
```
sqlite3.OperationalError: table papers already exists
```

**What to observe:**
- Schema creation should be idempotent and should only run on initialization.
- Putting DDL inside DML methods is a classic beginner mistake.

**Fix:** Use `IF NOT EXISTS`, or move schema creation to `__init__` / `_init_schema()`.

---

## Scenario 10 — Failing without `tmp_path` isolation

**Setup:** Write two tests that both insert a paper with `id = "test123"`.
Do NOT use the `tmp_path` fixture; instead, use a hardcoded path like `"test_researchops.db"`.

**Break it:** Run both tests.

**Expected behavior:** The first test passes.
The second test fails with a `DuplicatePaperError` because the paper already exists from the previous test run.

**What to observe:**
- Tests that share state are order-dependent.
- A test passing locally does not mean it passes in CI if state leaks.

**Fix:** Use `tmp_path` or clean up the database file in a `teardown` fixture.
The standard approach for ResearchOps tests is `tmp_path`.

---

## Edge cases to explore

1. **Empty text:** Save a paper where `text = ""`.
   Does `NOT NULL` allow this?
   (It allows empty string. `NOT NULL` only blocks `NULL`, not empty string.)
   Is `is_empty()` correct?

2. **Very long text:** Save a paper with `text` that is 10 MB of repeated characters.
   How long does the insert take?
   How long does the select take?
   Does `list_all()` become slow?

3. **Unicode in title:** Save a paper with a title like `"深度学习在研究中的应用"`.
   Verify it round-trips correctly.
   SQLite stores text as UTF-8, so this should work without special handling.

4. **Timestamp precision:** `datetime.utcnow()` may include microseconds.
   Does `isoformat()` preserve them?
   Does `fromisoformat()` reconstruct them correctly?
   Write a test that checks this.

5. **Null optional fields:** Save a paper where `author = None` and `abstract = None`.
   Verify they come back as `None` (not the string `"None"`).

6. **Empty tags list:** Save a paper with `tags = []`.
   Query `paper_tags` and verify no rows were inserted.

7. **Special characters in path:** Save a paper with a source path containing spaces or quotes.
   Verify the path round-trips correctly with parameterized queries.

---

## What did you learn?

After completing these scenarios, answer:

1. Which constraint saved you from the most dangerous data problem?
2. What error message surprised you the most?
3. How will you remember to always enable foreign keys?
4. What aspect of transaction semantics was not obvious until you broke it?
5. How will you structure future tests to avoid shared database state?

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 2 — Data Storage and Concurrency · **Week 5 — SQLite Storage** · *break_it.md — the failure lab* (step 4 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [exercises.md](./exercises.md)
- ▶ **Next:** [validation.md](./validation.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. **➡ [break_it.md](./break_it.md) ← you are here**
5. [validation.md](./validation.md)
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 6](../../../curriculum/month-02-data-storage-concurrency/week-06-pdf-parsing-pipeline/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 6 — PDF Parsing Pipeline](../../../curriculum/month-02-data-storage-concurrency/week-06-pdf-parsing-pipeline/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 2 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 2 overview](../README.md) · [📄 Week 5 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
