# P1 external review response — 2026-04-03T03:38:00

**Author**: Opus
**Branch**: p1-review-log
**PR**: #326

## Summary
Jonathan forwarded seven external-reviewer comments on Paper 1 (*The Brown Note*, JSV), including three marked major. This session ran three parallel investigations (`scripts/n1_mode_analysis.py`, `scripts/gamma2_figure.py`, and a Dietrich consultation), then completed two revision passes merged as PRs #323 and #325, with an intermediate Reviewer-D simulation agent added in PR #324 to emulate the external reviewer and test whether the fixes actually closed the loop.

## Key Findings
- The external reviewer identified **7 issues**: **3 MAJOR**, **3 MODERATE**, and **1 MINOR**.
- The constrained `n=1` mode is **not** a trivial rigid-body omission: four analysis routes in `scripts/n1_mode_analysis.py` placed `f_1` between **1.45 Hz** and **9.4 Hz**, showing that the constrained case is support-dominated and best described as a low-frequency “belly bounce”.
- The wall-support coupling factor `\Gamma_2(\theta_c)` is **non-monotonic**. `scripts/gamma2_figure.py` found a peak of about **0.49** at **125°**, a canonical value of about **0.48** at **120°**, and only about **0.30** at **150°**; the manuscript’s previous statement of **0.7 at 5\pi/6** was wrong by roughly a factor of **2.3**.
- The coupling comparison is better framed as transfer functions than as a supposed system-intrinsic ratio: revision pass 1 introduced `H_air \approx 1.4\times10^{-9} \ \mathrm{m/Pa}` and `H_mech \approx 9.17\times10^{-3} \ \mathrm{m/(m/s^2)}` in `papers/paper1-brown-note/sections/section4_coupling.tex`, making the excitation dependence explicit.
- Revision pass 1 (merged as **PR #323**) changed **8 files** with **163 insertions / 59 deletions** at merge, including `section4_coupling.tex` (**+189/-61** in the originating PR description), `section2_formulation.tex`, `results.tex`, two new figures, and a fresh P1 draft snapshot.
- Reviewer D judged pass 1 **MAJOR REVISION**: **4/7** original concerns resolved, **3/7** only partially resolved, and **2 new MAJOR concerns** surfaced (transfer-function framing still localised to §4; UQ still leaning on the pressure-based airborne path).
- Revision pass 2 (merged as **PR #325**) changed **10 files** with **140 insertions / 118 deletions**, promoting the transfer-function framing into the abstract, introduction, discussion, and conclusion; softening the Ritz-convergence caveats; aligning the UQ section with the energy-consistent airborne formulation; and further condensing redundant tables.
- Reviewer-D infrastructure landed in **PR #324**: `.github/agents/reviewer-d.agent.md`, `scripts/gamma2_figure.py`, and `scripts/n1_mode_analysis.py` were added in a **4-file**, **890-insertion / 2-deletion** change so the external review could be regression-tested inside the repo.
- Paper snapshot archived with this log: `docs/research-logs/2026-04-03T0338-paper-snapshot.pdf` (copied from `papers/paper1-brown-note/drafts/draft_2026-04-02_2027.pdf`).

## Changes Made
- Session analysis scripts created: `scripts/n1_mode_analysis.py`, `scripts/gamma2_figure.py`.
- External-review simulation agent created: `.github/agents/reviewer-d.agent.md`.
- Paper 1 manuscript updated across:
  - `papers/paper1-brown-note/sections/section2_formulation.tex`
  - `papers/paper1-brown-note/sections/section4_coupling.tex`
  - `papers/paper1-brown-note/sections/results.tex`
  - `papers/paper1-brown-note/sections/introduction.tex`
  - `papers/paper1-brown-note/sections/discussion.tex`
  - `papers/paper1-brown-note/sections/conclusion.tex`
  - `papers/paper1-brown-note/main.tex`
  - `papers/paper1-brown-note/main.pdf`
  - `papers/paper1-brown-note/drafts/draft_2026-04-03_2000.pdf`
  - `papers/paper1-brown-note/drafts/draft_2026-04-02_2027.pdf`
  - `papers/paper1-brown-note/figures/fig_constraint_geometry.pdf`
  - `papers/paper1-brown-note/figures/fig_gamma2_thetac.pdf`
- README draft link updated in `README.md` during pass 2.
- This session log created: `docs/research-logs/2026-04-03T0338-p1-external-review.md`.
- Companion manuscript snapshot created: `docs/research-logs/2026-04-03T0338-paper-snapshot.pdf`.

## Issues Identified
- **MAJOR** — The original manuscript treated `R` as if it were a system property, but the quoted value depends on the chosen excitation pair (**120 dB SPL** airborne vs **0.1 m/s^2 RMS** mechanical). The response fixed this by reframing the comparison in terms of `H_air` and `H_mech`.
- **MAJOR** — The `n=1` constrained mode had been effectively skipped; analysis showed it is non-trivial and support-dominated, so the revision now acknowledges it explicitly rather than implying the flexural spectrum simply begins at `n=2` without caveat.
- **MODERATE** — The Ritz basis had not been written down explicitly. The revision now states `w(\eta)=\beta\,P_n(\eta)` and `u(\theta)=\alpha\sin\theta\,P_n'(\cos\theta)` in the formulation.
- **MODERATE** — Tables 7–8 were redundant for a linear system. Both revision passes condensed them to reduce repetition.
- **MODERATE** — The `\Gamma_2` treatment lacked a figure and omitted derivation steps. The session generated `fig_gamma2_thetac.pdf` and integrated the corrected support-angle discussion.
- **MAJOR** — The old `\Gamma_2(\theta_c)` text claimed monotonic growth to **0.7** at **150°**; analysis showed the correct value is about **0.30** there, with a peak near **125°** instead.
- **MINOR** — Forward references from §2 into §4 appeared before the derivation. Both passes cleaned these references to restore narrative order.
- **MAJOR (new after pass 1)** — Reviewer D found that transfer-function language introduced in §4 had not yet propagated manuscript-wide. Pass 2 addressed this across the abstract, introduction, discussion, and conclusion.
- **MAJOR (new after pass 1)** — Reviewer D found the uncertainty quantification section still using the pressure-based airborne path, contradicting the paper’s energy-consistent recommendation. Pass 2 aligned the UQ discussion with the energy-consistent route.

## Next Steps
- Run Reviewer D once more on the post-PR-325 manuscript to verify that the transfer-function framing and UQ alignment now close the last partial concerns.
- Draft the external-review response letter issue-by-issue, using the quantitative corrections above (`f_1=1.45–9.4 Hz`, `\Gamma_2(120^\circ)\approx0.48`, `\Gamma_2(150^\circ)\approx0.30`, `H_air\approx1.4\times10^{-9}`, `H_mech\approx9.17\times10^{-3}`) so the rebuttal is numerically specific.
- Perform a final consistency audit and one clean compile of Paper 1 before resubmission to JSV.
