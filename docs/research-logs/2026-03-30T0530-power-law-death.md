# Death of the Power Law — 2026-03-30T0530

**Author**: Opus
**Branch**: main
**PR**: N/A (direct main commit requested by user)

## Summary
This session records the decisive negative result for Paper 8 and Paper 9: the conjectured identifiability law \(\kappa \sim C\varepsilon^{-2}\) has been disproved by our own computations. Re-analysis after the sphere-branch smoothness fix in PR #246 showed that the Ritz model retains a non-zero spherical singular-value floor, the fitted exponent is range-sensitive rather than universal, and prolate shells do not exhibit the expected lifting at all.

The scientific pivot is therefore substantive, not cosmetic. Reviewer B R4 was correct to flag the contradiction between a claimed divergence and an observed floor, and Dietrich's replacement framing now redirects the programme from a false lifting-law narrative toward a geometry-class classification theorem with oblate-prolate asymmetry as the central open phenomenon.

## Key Findings
- **The power-law conjecture is dead**: the fitted exponent \(\alpha\) is not stable. Across fitting windows, \(\alpha\) varies from approximately **0.4** to **3.0**, while **\(R^2\) never exceeds 0.84** in the diagnostic sweep that motivated this log. That is not evidence for a robust universal law.
- **The Ritz model has a finite spherical floor**: in the five-mode expansion, \(\sigma_{\min}(\varepsilon)\) is better described by
  \[
  \sigma_{\min} = \sigma_0 + \lambda_1 \varepsilon^2 + \lambda_2 \varepsilon^4,
  \]
  with **\(\sigma_0 = 0.01113\)** and **\(\lambda_1 = 0.00507\)**. Because **\(\sigma_0 > 0\)** at the sphere, \(\kappa\) approaches a **finite floor \(\approx 270\)** rather than diverging to infinity. See `src/analytical/power_law_proof.py:255-309`.
- **The analytical prefactor was never robust**: after the sphere-branch fix in **PR #246**, **\(C_{\mathrm{analytical}}\)** shifted from **160** to **373**, confirming that it is not a trustworthy invariant quantity. The relevant smootherstep sphere blending lives in `src/analytical/oblate_spheroid_ritz.py:143-229`.
- **Canonical and limiting oblate conditioning are now explicit**: in the five-mode basis, the oblate condition number spans roughly **270** as \(\varepsilon \to 0\) down to **17** at **\(\varepsilon = 0.95\)**, with the canonical abdomen at **\(\kappa = 69.4\)**. This is bounded improvement, not singular lifting.
- **Prolate shells show no identifiability improvement**: over the informative mid-range, prolate \(\kappa\) remains essentially flat at **561–729**, with fitted **\(\alpha \approx -0.07\)**. That is a null result for the original universality story and the strongest evidence yet for class-dependent behaviour. See `src/analytical/universality.py:758-869`.
- **Reviewer B R4 called the central contradiction correctly**: the manuscript could not simultaneously claim a near-sphere divergence and report a non-zero floor. This session confirms that the floor is the real phenomenon and the divergence story was an artefact of over-fitting.
- **Dietrich supplied the correct replacement language**: the right asymptotic object is the regular perturbation expansion
  \[
  \sigma_{\min} = \sigma_0 + \lambda_1 \varepsilon^2 + \lambda_2 \varepsilon^4,
  \]
  with headline quantities **\(\kappa_{\mathrm{floor}}\)**, **\(\varepsilon_c = \sqrt{\sigma_0/\lambda_1}\)**, and the expansion coefficients themselves. His summary line deserves to survive into the paper draft: **“Better a true curved story than a false straight line.”**
- **Paper 9 has pivoted accordingly**: the original “lifting theorem” framing is no longer tenable. The emerging theorem is classificatory:
  - **Singular class**: \(J_0\) rank-deficient equivalent-sphere models
  - **Regular bounded class**: oblate Ritz models with **\(\sigma_0 > 0\)**
  - **Non-lifting class**: prolate models with essentially flat \(\kappa\)
- **Oblate-prolate asymmetry is now the key finding under active investigation**: the important question is no longer whether all geometries obey \(\varepsilon^{-2}\), but why oblate symmetry breaking improves conditioning modestly while prolate symmetry breaking appears not to help at all.
- **Five-mode reference values for the current paper state**:
  - **\(\sigma_0 = 0.01113\)**
  - **\(\lambda_1 = 0.00507\)**
  - **\(C_{\mathrm{analytical}} = 373\)**
  - **\(\kappa_{\mathrm{floor}} \approx 170\)** (as the asymptotic headline quantity now used in the working notes)

## Changes Made
- Created `docs/research-logs/2026-03-30T0530-power-law-death.md`.
- Created companion snapshot `docs/research-logs/2026-03-30T0530-paper-snapshot.pdf` from `papers/paper8-kac/main.pdf`.
- Documented the numerical falsification of the \(\kappa \sim C\varepsilon^{-2}\) conjecture for Paper 8 / Paper 9 strategy.
- Recorded the post-PR-#246 interpretation shift tied to `src/analytical/power_law_proof.py`, `src/analytical/universality.py`, and `src/analytical/oblate_spheroid_ritz.py`.

## Issues Identified
- **CRITICAL**: Paper 8 can no longer present \(\kappa \sim C\varepsilon^{-2}\) as a theorem, conjecture strongly supported by numerics, or even a robust empirical summary. The evidence now favours a bounded-floor expansion instead.
- **MAJOR**: Any text, figure, test, or discussion in Paper 9 that still uses “lifting theorem” language is scientifically stale and must be rewritten as a geometry-class classification problem.
- **MAJOR**: The prolate null result means the old “universality” framing is false; oblate and prolate geometries must be discussed separately from now on.
- **MINOR**: The numerical headline quantity should move away from \(C_{\mathrm{analytical}}\), whose jump from **160** to **373** after PR #246 demonstrates sensitivity to implementation details near the sphere branch.

## Next Steps
- Rewrite Paper 8 results, discussion, and conclusion around the bounded expansion \(\sigma_{\min} = \sigma_0 + \lambda_1\varepsilon^2 + \lambda_2\varepsilon^4\), with \(\kappa_{\mathrm{floor}}\) and \(\varepsilon_c\) as the headline quantities.
- Remove or qualify every surviving “power law”, “universality”, and “lifting theorem” claim in Paper 8 and the Paper 9 scaffold.
- Build Paper 9 around the **classification theorem**: singular equivalent-sphere, regular bounded oblate Ritz, and non-lifting prolate classes.
- Investigate the **oblate-prolate asymmetry** directly: identify which terms in the Jacobian perturbation or curvature sampling survive in the oblate case but cancel or saturate in the prolate case.
- Preserve the five-mode basis consistently in all future conditioning calculations and cite the PR #246 sphere-branch fix whenever comparing pre- and post-fix prefactors.
