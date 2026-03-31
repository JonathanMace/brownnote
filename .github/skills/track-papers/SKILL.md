---
name: track-papers
description: >-
  Bootstrap and maintain a per-session SQL tracking system for all papers,
  their statuses, stale values, submission readiness, and granular TODO items.
  Use at session start and after any paper modification.
---

# Track Papers: Paper Status & TODO Management

This skill defines how to track the status of all Browntone papers using the
session SQL database. Because SQL is session-scoped, the tracking system must
be **bootstrapped at the start of every session** from the persistent source
of truth in `copilot-instructions.md` (Publication Pipeline table) and
verified against the actual repo state.

## When to Use

- **Session start**: Bootstrap the tracking tables from repo state.
- **After any paper modification**: Update the relevant rows.
- **Before launching fix agents**: Query for pending work to build accurate prompts.
- **At semester breaks**: Reconcile SQL state with repo state.

## Schema

### `papers` — One row per paper

```sql
CREATE TABLE IF NOT EXISTS papers (
    id TEXT PRIMARY KEY,           -- 'p1' through 'p10'
    number INTEGER NOT NULL,
    title TEXT NOT NULL,
    venue TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN (
        'skeleton',           -- Section headers only, no prose
        'drafting',           -- Partially written
        'draft_complete',     -- Full draft exists, not yet reviewed
        'revision_needed',    -- Has known issues (stale values, reviewer feedback)
        'submission_ready',   -- Text clean, reviewed, ready to package
        'submitted',          -- Uploaded to journal
        'accepted',           -- Journal accepted
        'published'           -- Published with DOI
    )),
    pages INTEGER,
    stale_values INTEGER DEFAULT 0,    -- Count of known stale values
    submission_pkg_ready BOOLEAN DEFAULT 0,
    notes TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);
```

### `paper_todos` — Granular action items per paper

```sql
CREATE TABLE IF NOT EXISTS paper_todos (
    id TEXT PRIMARY KEY,           -- e.g. 'p2-stale-displacement'
    paper_id TEXT NOT NULL REFERENCES papers(id),
    title TEXT NOT NULL,
    description TEXT,              -- Include file:line when possible
    priority TEXT DEFAULT 'medium' CHECK(priority IN ('critical','high','medium','low')),
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending','in_progress','done','blocked')),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

## Bootstrap Procedure

At session start, run this sequence:

### Step 1: Create tables

Run both CREATE TABLE statements above.

### Step 2: Audit repo state

For each paper directory under `papers/`:
1. Check for stale values by grepping ALL `.tex` files for known stale patterns:
   - `6.6 \times 10^4` or `6.6\times` (should be `3.3 \times 10^4`)
   - `0.014` near `um` or `micro` (should be `0.028`)
   - `66,000` or `66 000` (should be `~33,000`)
   - `158` near `dB` (should be `~151`)
   - `13` as an overestimate factor (should be `~6.5`)
2. Check `submission/` directory completeness (cover letter, highlights, compiled PDFs).
3. Check `drafts/` for latest snapshot date.
4. Check for TODO/FIXME markers in `.tex` files.

### Step 3: Populate tables

Insert one row per paper into `papers` with current status.
Insert one row per action item into `paper_todos` with file:line specifics.

### Step 4: Reconcile with copilot-instructions.md

Compare the Publication Pipeline table in `.github/copilot-instructions.md`
against the SQL state. Flag any discrepancies. The repo state (files on disk)
is the ground truth; the instructions table should match.

## Querying

### What needs fixing right now?

```sql
SELECT pt.id, p.title, pt.title AS todo, pt.description, pt.priority
FROM paper_todos pt
JOIN papers p ON pt.paper_id = p.id
WHERE pt.status = 'pending' AND pt.priority IN ('critical', 'high')
ORDER BY pt.priority, p.number;
```

### Paper dashboard

```sql
SELECT id, number, title, venue, status, pages, stale_values,
       submission_pkg_ready, notes
FROM papers ORDER BY number;
```

### What's blocking submission?

```sql
SELECT p.id, p.title, p.venue,
       COUNT(CASE WHEN pt.status != 'done' THEN 1 END) AS open_todos,
       SUM(CASE WHEN pt.priority = 'critical' AND pt.status != 'done' THEN 1 ELSE 0 END) AS critical_open
FROM papers p
LEFT JOIN paper_todos pt ON pt.paper_id = p.id
WHERE p.status NOT IN ('submitted', 'accepted', 'published', 'skeleton')
GROUP BY p.id
ORDER BY p.number;
```

## After Making Changes

When an agent fixes a stale value, builds a submission package, or completes
any paper_todo:

```sql
-- Mark the todo done
UPDATE paper_todos SET status = 'done', updated_at = datetime('now')
WHERE id = '<todo-id>';

-- Update the paper's stale count
UPDATE papers
SET stale_values = (SELECT COUNT(*) FROM paper_todos
                    WHERE paper_id = '<paper-id>'
                    AND status != 'done'
                    AND title LIKE '%stale%'),
    updated_at = datetime('now')
WHERE id = '<paper-id>';

-- If all critical/high todos done, upgrade status
UPDATE papers SET status = 'submission_ready', updated_at = datetime('now')
WHERE id = '<paper-id>'
AND NOT EXISTS (
    SELECT 1 FROM paper_todos
    WHERE paper_id = '<paper-id>'
    AND status != 'done'
    AND priority IN ('critical', 'high')
);
```

## Stale Value Patterns

These are the known stale (v1 / pre-Breit-Wigner) values that MUST NOT appear
in any paper. When bootstrapping, grep for all of them:

| Pattern | Stale Value | Correct Value | Context |
|---------|-------------|---------------|---------|
| `6.6 \times 10^4` | R = 6.6×10⁴ | R = 3.3×10⁴ | Pre-Breit-Wigner coupling ratio |
| `66,000` | 66,000 | ~33,000 | Same, in words |
| `0.014` (near μm) | ξ = 0.014 μm | ξ = 0.028 μm | Pre-Breit-Wigner displacement |
| `158` (near dB) | 158 dB | ~151 dB | Pre-Breit-Wigner PIEZO threshold |
| `factor of.*13` | 13× overestimate | ~6.5× | Pre-Breit-Wigner overestimate factor |
| `\eta.*0.30` | η = 0.30 | η = 0.25 | v1 loss tangent |
| `ka.*0.017` | ka = 0.017 | ka = 0.0114 | v1 scattering parameter |
| `R_eq.*0.133` | R_eq = 0.133 | R_eq = 0.157 | v1 equivalent radius |

## Submission Package Checklist

Each paper targeting submission needs these in `submission/`:

- [ ] `cover-letter.tex` — LaTeX source
- [ ] `cover-letter.pdf` — Compiled
- [ ] `highlights.txt` — 3–5 bullet points
- [ ] `main.pdf` — Latest compiled manuscript
- [ ] `ai-statement.md` — AI usage disclosure (required by most journals)
- [ ] `reviewer-suggestions.md` — Optional but recommended

## Cross-References

- The Publication Pipeline table in `copilot-instructions.md` is the
  persistent human-readable status. Update it when paper statuses change.
- The `consistency-auditor` agent checks parameter values across code and
  papers. Run it before any submission.
- The `compile-paper` skill handles LaTeX compilation and PDF snapshots.
