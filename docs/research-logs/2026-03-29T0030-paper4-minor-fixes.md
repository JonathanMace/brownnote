# Paper 4 minor revision fixes

## Summary

Addressed the three remaining Reviewer C minor issues in the bladder-resonance
manuscript and recompiled the paper.

## Changes made

1. Corrected the breathing-mode shell stiffness in
   `projects/bladder-resonance/paper/sections/theory.tex` from
   \(\SI{2.2e4}{\pascal\per\metre}\) to \(\SI{2.9e5}{\pascal\per\metre}\), and
   updated the fluid-to-shell stiffness ratio from \(>10^6\) to
   \(\sim 5.5 \times 10^5\).
2. Added the relative base-excitation transfer function
   \(H_\mathrm{rel}(f) = r^2 / \sqrt{(1-r^2)^2 + (2\zeta r)^2}\) and updated the
   discussion to cite this equation for the sub-resonant wall-displacement
   estimates.
3. Corrected the dynamic strain-rate comparison from \(500\times\) to
   \(440\times\), and tightened the conclusion wording to ``roughly two to
   three orders'' for the displacement comparison.

## Quantitative checks

- At \SI{300}{\milli\litre}: \(k_\mathrm{shell} \approx \SI{2.888e5}{\pascal\per\metre}\),
  \(k_\mathrm{fluid} \approx \SI{1.589e11}{\pascal\per\metre}\),
  \(k_\mathrm{fluid}/k_\mathrm{shell} \approx 5.50 \times 10^5\).
- At \SI{6}{\hertz}: the absolute transfer function gives
  \(\approx\SI{833}{\micro\metre}\), whereas the relative base-excitation form
  gives \(\approx\SI{154}{\micro\metre}\), consistent with the manuscript's
  rounded \(\SI{160}{\micro\metre}\) value.
- At resonance (\SI{13.9}{\hertz}): predicted relative wall displacement remains
  \(\approx\SI{47}{\micro\metre}\), with peak strain rate
  \(\approx\SI{0.10}{\per\second}\), about \(440\times\) the nominal filling
  strain rate used in the manuscript summary.

## Validation

- `python -m pytest projects/bladder-resonance/tests/ -v` → 27 passed
- `python -m pytest tests/ -v` → 199 passed
- `pdflatex`/`bibtex`/`pdflatex`/`pdflatex` completed successfully

## Artifacts

- Compiled paper: `projects/bladder-resonance/paper/main.pdf`
- Snapshot: `projects/bladder-resonance/paper/drafts/draft_2026-03-29_0030.pdf`
