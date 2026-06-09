-- ResearchOps SQLite schema
-- Week 5: initial schema
-- Week 6: add ingestion tracking
-- Week 8: add job tables (job_queue)
-- Week 12: add experiment tables

-- ---------------------------------------------------------------------------
-- Papers
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS papers (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    source_path     TEXT NOT NULL UNIQUE,
    text            TEXT NOT NULL,
    num_pages       INTEGER NOT NULL DEFAULT 0,
    file_size_bytes INTEGER NOT NULL DEFAULT 0,
    author          TEXT,
    abstract        TEXT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_papers_title ON papers(title);

-- ---------------------------------------------------------------------------
-- Paper tags (many-to-many)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paper_tags (
    paper_id TEXT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    tag      TEXT NOT NULL,
    PRIMARY KEY (paper_id, tag)
);

-- ---------------------------------------------------------------------------
-- Failed documents
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS failed_documents (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    source_path   TEXT NOT NULL,
    error_message TEXT NOT NULL,
    error_type    TEXT NOT NULL,
    occurred_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

-- ---------------------------------------------------------------------------
-- Experiments (Week 12)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS experiment_runs (
    id         TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'created',
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS experiment_params (
    run_id TEXT NOT NULL REFERENCES experiment_runs(id) ON DELETE CASCADE,
    key    TEXT NOT NULL,
    value  TEXT NOT NULL,
    PRIMARY KEY (run_id, key)
);

CREATE TABLE IF NOT EXISTS experiment_metrics (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL REFERENCES experiment_runs(id) ON DELETE CASCADE,
    key    TEXT NOT NULL,
    value  REAL NOT NULL,
    step   INTEGER NOT NULL DEFAULT 0,
    logged_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

-- ---------------------------------------------------------------------------
-- Jobs (Week 16)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS jobs (
    id          TEXT PRIMARY KEY,
    type        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending',
    payload     TEXT NOT NULL DEFAULT '{}',
    result      TEXT,
    error       TEXT,
    attempts    INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
