# Cross-paper coupling ratio and citation harmonisation — 2026-03-29T0043

**Author**: Opus
**Branch**: cross-paper-harmonise
**PR**: #130

## Summary
Harmonised coupling-ratio notation and citation keys across the five-paper Browntone portfolio without changing any underlying physics or canonical parameters. Paper 1 now uses $\mathcal{R}_\mathrm{full}$, Paper 3 explicitly distinguishes $\mathcal{R}_\mathrm{scat}$ from Paper 1's full ratio, Paper 4 now labels its organ-specific metric $\mathcal{R}_\mathrm{bladder}$, and Paper 5 now cites the gas-pocket manuscript that introduced the constrained-bubble mechanism.

## Key Findings
- Paper 1 now labels the headline abdominal mechanical-to-airborne displacement ratio as $\mathcal{R}_\mathrm{full} \approx 6.6 \times 10^4$.
- Paper 3 retains the scattering-only metric $\mathcal{R}_\mathrm{scat}$ and now states explicitly that the human value $\mathcal{R}_\mathrm{scat} = 7.7 \times 10^3$ is about $8\times$ smaller than Paper 1's $\mathcal{R}_\mathrm{full}$ because it excludes the air--tissue impedance mismatch.
- Paper 4 now labels the bladder pathway ratio as $\mathcal{R}_\mathrm{bladder} \approx 6.4 \times 10^3$ and explicitly states that this is a different metric from Paper 1's abdominal $\mathcal{R}_\mathrm{full} \approx 6.6 \times 10^4$.
- Citation keys for Paper 1 were standardised to `Mace2026browntone`; the incorrect Paper 4 bibliographic year was corrected from 2025 to 2026.
- Paper 5 now cites Paper 2 as the first abdominal-resonance analysis of the constrained-bubble gas-pocket mechanism.
- Validation: all 5 papers compiled with no undefined-citation warnings, and `python -m pytest tests/ -v` passed with 199/199 tests.

## Changes Made
- Modified `paper\sections\section2_formulation.tex`
- Modified `paper\sections\section4_coupling.tex`
- Modified `paper\sections\results.tex`
- Modified `paper3-scaling-laws\main.tex`
- Modified `paper3-scaling-laws\references.bib`
- Modified `projects\bladder-resonance\paper\sections\introduction.tex`
- Modified `projects\bladder-resonance\paper\sections\theory.tex`
- Modified `projects\bladder-resonance\paper\sections\results.tex`
- Modified `projects\bladder-resonance\paper\references.bib`
- Modified `projects\borborygmi\paper\main.tex`
- Modified `projects\borborygmi\paper\references.bib`
- Created `docs\research-logs\2026-03-29T0043-cross-paper-harmonisation.md`
- Created `docs\research-logs\2026-03-29T0043-paper-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0043-paper2-gas-pockets-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0043-paper3-scaling-laws-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0043-paper4-bladder-snapshot.pdf`
- Created `docs\research-logs\2026-03-29T0043-paper5-borborygmi-snapshot.pdf`

## Issues Identified
- MINOR: `latexmk` is not usable in the current Windows environment because MiKTeX cannot find a Perl engine; explicit `pdflatex`/`bibtex` cycles were used instead.
- MINOR: The working tree contains unrelated pre-existing modifications outside this task (for example in `data\figures\` and `src\analytical\gas_pocket_detailed.py`), so only task-specific files should be committed.

## Next Steps
- Create and merge a PR containing only the harmonisation files plus the research-log artefacts.
- Before the next submission-oriented compile, run the consistency auditor across the portfolio to catch any further cross-paper notation drift.
