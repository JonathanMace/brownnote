# Paper 8 submission package

## Summary

- Built the first `papers/paper8-kac/submission/` package for Paper 8 from scratch.
- Recompiled `papers/paper8-kac/main.tex`, regenerated `main.pdf`, and created draft snapshot `papers/paper8-kac/drafts/draft_2026-03-30_2336.pdf`.
- Updated `README.md` and `.github/copilot-instructions.md` so Paper 8 now points to the latest draft and is marked submission-ready.

## Quantitative results

- Manuscript status remains **29 pages** with **0 stale values**.
- Submission highlights capture the main conditioning results: equivalent-sphere
  inversion is effectively singular with $\kappa \approx 1.37 \times 10^{10}$,
  the canonical oblate case improves to $\kappa = 69.4$, and the practical
  conditioning floor is $\kappa_{\mathrm{floor}} \approx 269$.
- Repository regression suite passed unchanged: **487/487 tests passed** in
  **427.16 s**, with **1 warning**.

## Files created

- `papers/paper8-kac/submission/cover-letter.tex`
- `papers/paper8-kac/submission/cover-letter.pdf`
- `papers/paper8-kac/submission/highlights.txt`
- `papers/paper8-kac/submission/ai-statement.md`
- `papers/paper8-kac/submission/reviewer-suggestions.md`
- `papers/paper8-kac/submission/main.pdf`

## Notes

- The cover letter targets *Inverse Problems in Science and Engineering* and
  frames the manuscript around the forward--inverse adequacy gap.
- Temporary LaTeX build artefacts for the cover letter were removed from the
  submission package after compilation.
