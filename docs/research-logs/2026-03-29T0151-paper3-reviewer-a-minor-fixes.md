# Paper 3 Reviewer A minor fixes — 2026-03-29T0151

**Author**: Opus
**Branch**: p3-minor-fix
**PR**: #149

## Summary
Addressed Reviewer A's minor revision requests in `paper3-scaling-laws/main.tex` by making the allometric sourcing language more candid, quantifying the quasi-universal spread in $\Pi_0$, clarifying the relationship between $\mathcal{R}_\mathrm{scat}$ and Paper 1's fuller coupling ratio, adding the breathing-mode formula explicitly, removing the duplicate competing-interest block, and softening the acknowledgements. Updated the bibliography to add McMahon and Bonner's allometry book and to list both J. Mace and B. R. Mace on the companion Paper 1 citation, then recompiled the paper and reran the full test suite.

## Key Findings
- Table 2 now reports $P_\mathrm{iap}/E$ explicitly for all four species: rat 0.006, cat 0.008, pig 0.008, human 0.010.
- The cross-species flexural frequency metric remains tightly clustered at $\Pi_0 = 0.065$--0.072; the manuscript now states the coefficient of variation as 4.5\% against approximately 20\% uncertainty in any individual $E$ or $h$ estimate.
- Section 5 now shows $f_0 \approx (1/2\pi)\sqrt{3K_f/(\rho_f R^2)}$ explicitly and distinguishes the fluid-dominated estimate of \SI{2.57}{\kilo\hertz} from the full fluid--shell model value of approximately \SI{2490}{\hertz} at the canonical human scale.
- Validation: `python -m pytest tests/ -v` passed with 203/203 tests in 8.96 s; `pdflatex`/`bibtex`/`pdflatex`/`pdflatex` produced an 11-page PDF (`paper3-scaling-laws\main.pdf`, 471319 bytes).

## Changes Made
- Modified `paper3-scaling-laws\main.tex`
- Modified `paper3-scaling-laws\references.bib`
- Created `docs\research-logs\2026-03-29T0151-paper3-reviewer-a-minor-fixes.md`
- Created `docs\research-logs\2026-03-29T0151-paper-snapshot.pdf`

## Issues Identified
- MINOR: `hyperref` still emits existing PDF-string warnings during compilation for title/author metadata; these predate this edit and do not block output.
- MINOR: The manuscript still contains some pre-existing overfull box warnings in the compiled layout.

## Next Steps
- Create and merge a PR containing the Paper 3 text, bibliography, and research-log artefacts.
- If a final submission-format pass is performed, consider cleaning the existing `hyperref` metadata warnings and overfull boxes.
