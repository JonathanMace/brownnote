# Paper 9 Scaffold — 2026-03-29

**Author:** Opus (PI)  
**Branch:** `paper9-scaffold`  
**Session window:** ~23:00 UTC

## Summary

This session created the initial repository scaffold for **Paper 9**,
*A singular-value lifting theorem for symmetry-broken spectral inverse
problems*, and integrated it into the Browntone paper infrastructure. The new
paper directory was created with a compileable `main.tex`, seven section stubs,
a seeded `references.bib`, and tracked placeholder directories for drafts,
submission material, and figures.

## Work completed

- Created `papers/paper9-lifting-theorem/` with:
  - **1** master manuscript file
  - **7** section stub files
  - **1** seeded BibTeX database with **16** references
  - **3** tracked placeholder directories (`drafts/`, `submission/`, `figures/`)
- Updated `README.md` to add a Paper 9 entry, increment the repository paper
  count from **8** to **9**, and expose the latest draft link.
- Added Paper 9 to the publication pipeline metadata in:
  - `.github/copilot-instructions.md`
  - `.github/skills/compile-paper/SKILL.md`
  - `.github/workflows/ci.yml`
  - `.github/workflows/paper.yml`
- Added `.github/instructions/paper9.instructions.md` so future edits follow the
  standard compile → snapshot → README sync workflow.

## Quantitative results

| Metric | Value |
|--------|-------|
| Paper 9 section stubs created | 7 |
| Seed references added | 16 |
| Paper 9 compiled length | 2 pages |
| `main.pdf` size | 100,841 bytes |
| Snapshot created | `draft_2026-03-29_2301.pdf` |
| Baseline test result | 454 passed |
| Post-change test result | 454 passed |

## Notes

- The manuscript compiled successfully with the article-class fallback because
  `iopart.cls` was not available in the local TeX installation.
- A `\nocite{*}` placeholder was added so the seeded bibliography appears in the
  scaffold draft and the BibTeX pass completes cleanly.

## Next steps

1. Draft the theorem statement and reduced nullspace coupling framework.
2. Replace the placeholder abstract with the actual contribution claim.
3. Add the first shell-family figure and theorem diagram once the analysis is
   stabilised.
