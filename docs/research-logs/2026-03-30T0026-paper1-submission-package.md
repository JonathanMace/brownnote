# Paper 1 submission package refresh

- **Timestamp:** 2026-03-30 00:26
- **Topic:** Paper 1 submission package completeness check and refresh

## Summary

Updated `papers/paper1-brown-note/submission/` to include a current manuscript PDF, synchronised cover letter assets, and copied supplementary files. Recompiled `papers/paper1-brown-note/main.tex`, created a fresh draft snapshot, and updated the repository README to point to the new Paper 1 draft.

## Quantitative results

- Submission manuscript copied to `submission/manuscript.pdf` at **753851 bytes**.
- Supplementary package copied to `submission/supplementary.pdf` at **340541 bytes** plus `submission/supplementary.tex`.
- Submission cover letter refreshed to `submission/cover-letter.pdf` at **98116 bytes** with updated `submission/cover-letter.tex`.
- New Paper 1 draft snapshot created: `papers/paper1-brown-note/drafts/draft_2026-03-30_0024.pdf` (**753851 bytes**).
- Main manuscript recompiled successfully to **30 pages** (`main.pdf`, **753851 bytes**).

## Validation

- Consistency audit before recompilation: **non-blocking fail** for a known pressure-based vs energy-consistent airborne-coupling helper mismatch in figure-generation code; current LaTeX recompilation deemed safe.
- Post-change test run in clean worktree: `python -m pytest tests/ -v` → **482 passed, 1 warning** in **934.41 s**.
- Baseline test run in the dirty main checkout failed with **1 pre-existing failure** in `tests/test_universality.py::TestProlateNullResult::test_prolate_kappa_is_flat`; this failure was unrelated to the submission-package changes.

## Files changed

- `README.md`
- `papers/paper1-brown-note/main.pdf`
- `papers/paper1-brown-note/drafts/draft_2026-03-30_0024.pdf`
- `papers/paper1-brown-note/submission/cover-letter.pdf`
- `papers/paper1-brown-note/submission/cover-letter.tex`
- `papers/paper1-brown-note/submission/manuscript.pdf`
- `papers/paper1-brown-note/submission/supplementary.pdf`
- `papers/paper1-brown-note/submission/supplementary.tex`
