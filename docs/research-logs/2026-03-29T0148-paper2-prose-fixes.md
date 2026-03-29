# Paper 2 prose fixes from Reviewer C post-fix review — 2026-03-29T0148

**Author**: Opus
**Branch**: p2-prose-fix
**PR**: #148

## Summary
Applied Reviewer C's post-fix corrections to the Paper 2 gas-pocket manuscript and aligned the analytical code comments with the paper where parameter labels had drifted. The update removes stale pre-PR-129 frequency prose, corrects the Monte Carlo displacement and log-normal confidence-interval summaries, clarifies the \(f_0/f_M\) range for clinically relevant volumes, and relabels \(P_0\) consistently as atmospheric pressure.

## Key Findings
- Elastic-wall spherical pocket resonances span \(\SI{107.82}{\hertz}\) at \(\SI{100}{\milli\litre}\) to \(\SI{437.64}{\hertz}\) at \(\SI{1}{\milli\litre}\); the cylindrical radial mode is \(\SI{161.99}{\hertz}\).
- For clinically relevant spherical volumes of \(\SIrange{5}{100}{\milli\litre}\), the constrained-bubble frequency ratio is \(f_0/f_M = 0.892\) to \(0.955\), supporting the revised prose range of roughly 89--96\%.
- The Monte Carlo model (\(N=10{,}000\), seed 42) gives a maximum wall-displacement range of \(\SIrange{1.026}{2.699}{\micro\metre}\) with median \(\SI{1.079}{\micro\metre}\).
- The same log-normal gas model (median \(\SI{200}{\milli\litre}\), \(\sigma_{\ln}=0.65\)) yields a 95\% interval of \(\SIrange{55.5}{719.3}{\milli\litre}\), consistent with the updated rounded prose \(\SIrange{56}{715}{\milli\litre}\).
- Validation passed: `python -m pytest tests/ -v` completed with 203/203 tests passing, and `pdflatex`/`bibtex`/`pdflatex`/`pdflatex` produced a 16-page Paper 2 PDF snapshot (`docs\research-logs\2026-03-29T0148-paper2-gas-pockets-snapshot.pdf`, 696,850 bytes).

## Changes Made
- Modified `paper2-gas-pockets\main.tex`
- Modified `src\analytical\gas_pocket_detailed.py`
- Modified `src\analytical\gas_pocket_resonance.py`
- Created `docs\research-logs\2026-03-29T0148-paper2-prose-fixes.md`
- Created `docs\research-logs\2026-03-29T0148-paper2-gas-pockets-snapshot.pdf`

## Issues Identified
- MINOR: A consistency-audit pass also flagged stale frequency wording in the abstract and discussion; these statements were corrected in the same edit set before the final compile.
- MINOR: The rounded analytical 95\% interval from the seeded Monte Carlo sample is \(\SIrange{55.5}{719.3}{\milli\litre}\), so the manuscript now uses the parameter-consistent rounded values \(\SIrange{56}{715}{\milli\litre}\).

## Next Steps
- Merge PR #148 once CI is satisfied, as the manuscript prose, code comments, tests, and compiled snapshot are now mutually consistent for the reviewed items.
