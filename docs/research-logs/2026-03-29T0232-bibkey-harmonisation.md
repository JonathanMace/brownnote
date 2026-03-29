# BibTeX key harmonisation across Browntone papers — 2026-03-29T0232

**Author**: Opus
**Branch**: bibkey-harmonise
**PR**: pending

## Summary
Harmonised three shared bibliography keys across the five-paper Browntone portfolio: `Junger1986`, `Kitazaki1998`, and `Griffin1990`. Source edits were required in Paper 1, Paper 3, and Paper 4; Paper 2 already used the standard keys and Paper 5 did not reference any of the three works.

## Quantitative Results
- Standardised 3 shared references across 3 affected bibliography files and 10 affected `.tex` citation sites.
- Paper 1: renamed `kitazaki1998resonance` → `Kitazaki1998` and `griffin1990handbook` → `Griffin1990`; regenerated PDF to 30 pages (767813 bytes).
- Paper 3: renamed `JungerFeit1986` → `Junger1986`; regenerated PDF to 8 pages (569675 bytes).
- Paper 4: renamed `junger2012sound` → `Junger1986`, `kitazaki1998resonance` → `Kitazaki1998`, and `griffin1990handbook` → `Griffin1990`; regenerated PDF to 19 pages (870733 bytes).
- Paper 2 compiled unchanged to 16 pages (753081 bytes); Paper 5 compiled unchanged to 14 pages (510041 bytes).
- Validation: `python -m pytest tests\ -v` passed with 206/206 tests in 8.87 s.

## Validation Notes
- All five papers completed `pdflatex` → `bibtex` → `pdflatex` → `pdflatex`, and fresh PDFs plus timestamped snapshots were produced.
- Final `.aux`/`.bbl` files contain the standardised keys (`Junger1986`, `Kitazaki1998`, `Griffin1990`) with corresponding `\bibcite{...}` entries where applicable.
- MiKTeX still reports the pre-existing `\Bbbk` redefinition error during `pdflatex`; this is repository-wide and not introduced by the bibliography-key changes.

## Changes Made
- Modified `paper\references.bib`
- Modified `paper\sections\discussion.tex`
- Modified `paper\sections\introduction.tex`
- Modified `paper\sections\section2_formulation.tex`
- Modified `paper\sections\section4_coupling.tex`
- Modified `paper3-scaling-laws\main.tex`
- Modified `paper3-scaling-laws\references.bib`
- Modified `projects\bladder-resonance\paper\references.bib`
- Modified `projects\bladder-resonance\paper\sections\discussion.tex`
- Modified `projects\bladder-resonance\paper\sections\introduction.tex`
- Modified `projects\bladder-resonance\paper\sections\theory.tex`
- Created `docs\research-logs\2026-03-29T0232-bibkey-harmonisation.md`
- Created `docs\research-logs\2026-03-29T0232-paper-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0232-paper2-gas-pockets-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0232-paper3-scaling-laws-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0232-paper4-bladder-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0232-paper5-borborygmi-snapshot.pdf`

## Next Steps
- Open and squash-merge the PR after staging only task-specific source files and research-log artefacts.
- Address the long-standing MiKTeX `\Bbbk` package conflict separately if clean zero-exit LaTeX builds become a submission requirement.
