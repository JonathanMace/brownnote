# Reviewer C — Paper 2 Post-Fix Review (Round 2)

**Paper:** "Bowel Gas as an Acoustic Transducer: A Constrained Bubble Model for
Infrasound-Induced Mechanotransduction in the Gastrointestinal Tract"

**Code reviewed:** `src/analytical/gas_pocket_detailed.py` (primary),
`src/analytical/gas_pocket_resonance.py` (legacy module),
`paper2-gas-pockets/generate_figures.py`

**Context:** Post-fix review after PR #129 (Church equation rewrite),
PR #128 (wit adjustments), PR #130 (cross-paper harmonisation)

**Date:** 2026-03-29
**Reviewer:** C (computational mechanics / reproducibility specialist)

---

## Overall Assessment

The fundamental physics is now sound. The Church (1995)/Hoff (2001)
per-displacement formulation correctly recovers the Minnaert limit when
wall parameters vanish — verified to machine precision. Table 1 is exact
against code output. All 203 regression tests pass. The 10 mL frequency
of 222 Hz now matches the PR #129 target and Paper 5 cross-reference.

**However, I found two sentences of stale prose that directly contradict
the paper's own table**, plus two quantitative claims in the MC results
section that do not match the current code output. These are residual
artefacts of the equation rewrite that were not caught during
harmonisation.

**Verdict: MINOR REVISION — fix 4 specific text discrepancies, all
identified with line numbers below.**

---

## Code Verification Results (all work shown)

### 1. Minnaert Recovery: VERIFIED (machine precision)

| Volume (mL) | constrained(free) | Minnaert | Relative error |
|-------------|-------------------|----------|----------------|
| 1           | 524.041724        | 524.041724 | 0.0          |
| 5           | 306.461459        | 306.461459 | 0.0          |
| 10          | 243.238622        | 243.238622 | 0.0          |
| 50          | 142.246809        | 142.246809 | 0.0          |
| 100         | 112.901367        | 112.901367 | 0.0          |

Also verified with E_w=0, h_w→0, ρ_w=0 (elastic mode): identical to Minnaert.
**The fatal bug from the old equation is fully resolved.**

### 2. Table 1 — Resonance Frequencies: ALL MATCH

| V (mL) | Geom | a/R paper (mm) | a/R code (mm) | fM paper | fM code | f0 paper | f0 code | Match |
|---------|------|----------------|---------------|----------|---------|----------|---------|-------|
| 1       | Sph  | 6.2            | 6.2           | 524      | 524     | 438      | 438     | ✓     |
| 5       | Sph  | 10.6           | 10.6          | 306      | 307     | 273      | 273     | ✓     |
| 10      | Sph  | 13.4           | 13.4          | 243      | 243     | 222      | 222     | ✓     |
| 20      | Sph  | 16.8           | 16.8          | 193      | 193     | 179      | 179     | ✓     |
| 50      | Sph  | 22.9           | 22.9          | 142      | 142     | 134      | 134     | ✓     |
| 100     | Sph  | 28.8           | 28.8          | 113      | 113     | 108      | 108     | ✓     |
| 10      | Cyl  | 15.0           | 15.0          | ---      | ---     | 99       | 99      | ✓     |
| 50      | Cyl  | 15.0           | 15.0          | ---      | ---     | 44       | 44      | ✓     |
| 100     | Cyl  | 15.0           | 15.0          | ---      | ---     | 31       | 31      | ✓     |

Cylindrical radial (breathing) mode: 162.0 Hz independent of volume. Matches footnote.

### 3. SPL Thresholds: MATCH

| Config | SPL_thresh (code) | Paper claim | Match |
|--------|------------------|-------------|-------|
| 5 mL spherical | 120.2 dB | ~120 dB | ✓ |
| 100 mL spherical | 111.4 dB | ~111 dB | ✓ |
| Cylindrical (all) | 113.2–113.5 dB | ~114 dB | ✓ |

### 4. Pathway Comparison: MATCH

- 100 mL spherical at 120 dB: ξ = 1.347 µm (paper: ~1.3 µm) ✓
- Ratio to whole-cavity (0.014 µm): 96× (paper: 35–100×) ✓
- 5 mL spherical: 35×; 100 mL spherical: 96× — range confirmed

### 5. Wall Stiffness Fractions: MARGINAL MATCH

Code gives 0.88% (100 mL) to 2.36% (5 mL). Paper claims "0.9–2.4%".
The 100 mL value is 0.88%, not quite 0.9%. Rounding issue — defensible
but tight.

### 6. Helmholtz Short-Circuit: MATCH

- f_H = 15.3 Hz (paper: ~15 Hz) ✓
- Short-circuit ratio at 7 Hz: 0.827 (paper: ~0.8) ✓
- Maximum survivable reduction: 2.7× (paper: ~2.7×) ✓

### 7. Formula Verification

Independently derived all stiffness/inertia terms:
- Spherical: k_wall = 2Eh/(a²(1−ν)) — correct thin spherical shell (biaxial stress)
- Cylindrical: k_wall = Eh/(R²(1−ν²)) — correct thin cylindrical shell (plane strain)
- Ratio at same radius: 2(1+ν) = 2.90 — verified to machine precision
- Church (1995) form with Hoff (2001) shell-mass addition: consistent with code

### 8. All Tests Pass

```
203 passed, 1 warning in 7.69s
```

Includes 4 Minnaert-recovery regression tests (TestMinnaertRecovery class):
- `test_sphere_free_equals_minnaert` (5 volumes, rel=1e-10)
- `test_sphere_zero_wall_params_equals_minnaert` (3 volumes, rel=1e-6)
- `test_constrained_below_minnaert` (3 volumes)
- `test_cylindrical_radial_regression` (162 ± 5 Hz)

---

## Major Issues

### M1. STALE PROSE: Lines 465–467 contradict Table 1 (MUST FIX)

**Current text (line 465–467):**
> "Spherical pocket resonances exceed 600 Hz for all volumes studied, and
> the cylindrical radial (breathing) mode lies at ~1300 Hz."

**Actual values (from Table 1 and code):**
- Spherical: 108–438 Hz (NONE exceed 600 Hz)
- Cylindrical radial: 162 Hz (NOT 1300 Hz)

This is unreformed text from the pre-PR-#129 equation. The old equation
gave ~8.6× higher frequencies (10 mL was 1916 Hz; now 222 Hz), so
"exceed 600 Hz" and "~1300 Hz" are consistent with the old model but
are now wrong by nearly an order of magnitude.

**This must be corrected before any submission. The prose directly
contradicts the paper's own table on the same page.**

Suggested replacement:
> "Spherical pocket resonances range from ~440 Hz (1 mL) down to ~108 Hz
> (100 mL) for all volumes studied, and the cylindrical radial
> (breathing) mode lies at ~162 Hz."

---

## Minor Issues

### m1. MC displacement range: Lines 549–550

**Paper claims:** "The distribution of maximum pocket-wall displacement
spans approximately 0.6–3.5 µm, with a median of ~1.2 µm."

**Code gives (seed=42):** range [1.03, 2.70] µm, median 1.08 µm.
Across 4 seeds: range [0.92, 3.03] µm, median 1.08 µm.

The lower bound of 0.6 µm never appears because 70% of pockets are
cylindrical with fixed R_lumen = 15 mm, giving ξ ≈ 1.05 µm regardless
of volume. The minimum is floored at ~1 µm, not 0.6.

**Likely cause:** stale values from old equation. Should read approximately
"1.0–3.0 µm, with a median of ~1.1 µm."

### m2. Log-normal 95% CI: Line 442

**Paper claims:** "95% CI of approximately 70–570 mL"

**Analytical 95% CI** for log-normal(median=200, σ_ln=0.65):
- Lower: exp(ln(200) − 1.96×0.65) = 56 mL
- Upper: exp(ln(200) + 1.96×0.65) = 715 mL

Empirical (N=10⁶): [56, 716] mL.

The correct 95% CI is [56, 715], not [70, 570]. A σ_ln of ~0.535 would
give [70, 570] — the paper appears to have a different σ_ln in mind, or
the range was estimated by eye. Either way, the stated CI does not match
the stated parameters.

**Fix:** Either change σ_ln to 0.535 or change the CI to "56–715 mL".

### m3. f0/fM ratio range: Lines 303–304

**Paper claims:** "roughly 80–90% of f_M"

**Code gives:**
- 1 mL: 83.5%, 5 mL: 89.2%, 10 mL: 91.1%, 50 mL: 94.4%, 100 mL: 95.5%

For the physiological range 5–100 mL, the ratio is 89–96%, not 80–90%.
80% only occurs at 1 mL. Suggest: "roughly 85–95% of f_M" or simply
remove the specific range and say "somewhat below f_M due to wall mass."

### m4. Gas pocket resonance module density inconsistency

`gas_pocket_resonance.py` (old module) uses ρ_fluid = 1040 kg/m³ by default;
`gas_pocket_detailed.py` (current module) uses ρ_tissue = 1020 kg/m³.
Both are cited as tissue density. The discrepancy is small (~2%) and the old
module is not used by Paper 2, but it should be harmonised for codebase
hygiene. Not blocking.

---

## Uncertainty and Statistical Rigour

### MC sample size: Adequate but result is trivially pre-determined

The N = 10,000 MC gives 100.0% exceedance across all seeds tested
(42, 123, 999, 7777). The result is robust but also trivial: since the
minimum displacement from a cylindrical pocket is ~1.05 µm (2× the
threshold), and 70% of pockets are cylindrical, NO individual can fall
below the threshold unless they have only tiny spherical pockets. The MC
adds no information beyond what a single back-of-envelope calculation shows.

The paper acknowledges this correctly (lines 540–547: "This high
exceedance fraction is expected rather than surprising... The result
therefore confirms internal consistency"). This is honest framing.

### Partial UQ: Acceptable for the scope

No formal uncertainty is propagated on E_w, ν_w, h_w, or the PIEZO
threshold. This is a reasonable simplification for a first-principles
exploration paper, but should be noted as future work. The sensitivity
to E_w is genuinely small (wall stiffness is <3% of total), so
propagating E_w uncertainty would have negligible effect. The PIEZO
threshold uncertainty is the dominant unknown, acknowledged in
Limitations §5.4.

### Convergence: N/A

All computations are closed-form (no iteration, no PDE solve). The MC
is the only stochastic component and converges trivially due to the
large margin above threshold.

---

## Reproducibility Assessment

### Can someone reproduce Figure 3 from the text alone?

**Almost.** The MC parameters are fully specified in §2.6 (lines 436–449):
- N = 10,000
- Log-normal(median=200, σ_ln=0.65), clipped [30, 2000]
- Poisson(λ=10), clipped [2, 40]
- Dirichlet partition
- 70/30 cylindrical/spherical split
- Seed not specified in paper (seed=42 in code)

To exactly reproduce the figure, one needs the seed. Without it,
statistical properties will be reproduced but not the exact histogram.
This is acceptable for a stochastic figure.

### Can someone reproduce Table 1 from equations alone?

**Yes, exactly.** All parameters are in Table 1 (line 184) and equations
(3)–(5). I verified this by hand calculation for 10 mL:
- a = (3×10⁻⁵/(4π))^(1/3) = 13.365 mm
- k_gas = 3×1.4×101325/0.013365 = 31,841,641 Pa/m
- k_wall = 2×10000×0.003/(0.013365²×0.55) = 610,728 Pa/m
- m_fluid = 1020×0.013365 = 13.632 kg/m²
- m_wall = 1040×0.003 = 3.120 kg/m²
- f₀ = √((k_gas+k_wall)/(m_fluid+m_wall))/(2π) = 221.5 Hz ✓

---

## What's Done Well

1. **Clean physics.** The Church/Hoff formulation is standard, correctly
   implemented, and now provably recovers the Minnaert limit. This was
   the fatal flaw in the old equation; it is fully resolved.

2. **Honest framing.** The paper correctly calls the MC result "expected
   rather than surprising" (line 541) and does not oversell the 100%
   exceedance as a prediction. The Limitations section (§5) is thorough.

3. **Excellent test coverage.** The TestMinnaertRecovery class tests the
   exact limiting behaviour at rel=1e-10. This is the gold standard for
   regression testing a physics equation rewrite.

4. **Consistent equation numbering.** Eqs. (3)–(5) for stiffness/inertia,
   Eqs. (13)–(14) for k_eff — all match the code exactly, including the
   Poisson ratio distinction (1−ν for sphere, 1−ν² for cylinder).

5. **Cross-paper consistency.** The 0.014 µm whole-cavity reference from
   Paper 1 is correctly used in Figure 4 and the code (generate_figures.py
   line 326).

6. **Short-circuit discussion.** §3.2 is intellectually honest about the
   acoustic short-circuit problem and gives quantitative bounds.

---

## Summary Recommendation: MINOR REVISION

**Required fixes (all text-only, no code changes needed):**

| # | Location | Issue | Severity |
|---|----------|-------|----------|
| M1 | Lines 465–467 | "exceed 600 Hz" and "~1300 Hz" are stale (should be 108–438 Hz and ~162 Hz) | **Critical** — contradicts own table |
| m1 | Line 550 | "0.6–3.5 µm" should be "~1.0–3.0 µm"; "~1.2 µm" should be "~1.1 µm" | Minor |
| m2 | Line 442 | "70–570 mL" should be "56–715 mL" (or adjust σ_ln) | Minor |
| m3 | Line 304 | "80–90%" should be "~85–95%" | Minor |

The code is correct and well-tested. The physics is sound post-PR-#129.
The four text discrepancies are all trivial to fix and do not affect any
conclusions. Once corrected, the paper is defensible for submission.
