# Reviewer B - Paper 2, Round 2

**Manuscript:** Bowel Gas as an Acoustic Transducer: A Constrained Bubble Model for Infrasound-Induced Mechanotransduction in the Gastrointestinal Tract

**Review date:** 2026-03-28

---

## Decision: MINOR REVISION

The authors have addressed all five Round 1 issues, and the paper is substantially improved. The acoustic short-circuit discussion (Sec. 4.2) is a genuine addition, the cylindrical threshold is corrected, the amplification range is accurate, and the population exceedance language is now honest. However, the quantitative defence in the short-circuit section contains a numerical error that must be fixed before acceptance.

---

## Verification of Round 1 Fixes

### F1. Acoustic Short-Circuit - VERIFIED (with caveats)

New Sec. 4.2 added. Helmholtz estimate f_H = 15 Hz is correct (independently verified: f_H = (343/2pi)*sqrt(S/VL) = 15.30 Hz). Three mitigating factors are physically reasonable. Limitation bullet 6 (line 746) cross-references Sec. 4.2.

**Verdict:** The conceptual gap is closed. Two quantitative errors remain (see M1 and m1 below).

### Fix 2. Cylindrical SPL Threshold: 118 to 114 dB - VERIFIED

Line 494 now reads ~114 dB. Code verification:

| Volume | SPL (binary search) | SPL (analytical) |
|--------|---------------------|------------------|
| 5 mL   | 113.55 dB           | 113.57 dB        |
| 20 mL  | 113.49 dB           | 113.57 dB        |
| 50 mL  | 113.36 dB           | 113.57 dB        |
| 100 mL | 113.15 dB           | 113.57 dB        |

~114 dB is a 0.4-0.9 dB overstatement from analytical 113.6 dB. Within tilde precision. **Acceptable.**

### Fix 3. Amplification Ratio: 50-100x to 35-100x - VERIFIED

Verified in abstract (line 87), Sec. 3.4 (line 559), and conclusion (line 767). Code gives 5 mL sphere = 34.8x, 100 mL sphere = 95.8x, cylinders = 75-79x. **Fixed.**

### Fix 4. Wall Constraint Acknowledged - VERIFIED

New text after Eq. (4) (lines 249-254) states wall stiffness is only 0.9-2.4% of k_eff. Verified: 5 mL sphere = 2.36%, 100 mL sphere = 0.88%, cylinder = 0.88%. **Fixed.**

### Fix 5. Population Exceedance Language - VERIFIED

Lines 520-528 now read "nearly all simulated individuals" with caveat about internal consistency. **Fixed.**

---

## NEW Issues Found in Round 2

### M1. Mitigation 3 Is Numerically False (MAJOR)

Lines 658-666 state:

> "However, even a factor of five reduction in effective Delta P still yields sub-micrometre displacements for pockets > 20 mL at 120 dB, keeping the mechanism above the PIEZO threshold."

This is **arithmetically wrong**. I computed xi/5 for every pocket at 120 dB:

| Pocket               | xi at 120 dB | xi/5     | Above 0.5 um? |
|----------------------|-------------|----------|---------------|
| 20 mL spherical      | 0.780 um    | 0.156 um | **NO**        |
| 50 mL spherical      | 1.062 um    | 0.212 um | **NO**        |
| 100 mL spherical     | 1.341 um    | 0.268 um | **NO**        |
| 20 mL cylindrical    | 1.058 um    | 0.212 um | **NO**        |
| 50 mL cylindrical    | 1.073 um    | 0.215 um | **NO**        |
| 100 mL cylindrical   | 1.100 um    | 0.220 um | **NO**        |

**Every pocket falls below the PIEZO threshold after a factor-of-five reduction.** The maximum survivable factor at 120 dB is only **2.7x** (100 mL sphere: 1.341/0.5 = 2.68).

Moreover, the paper's own Helmholtz estimate implies ~83% equalization at 7 Hz (code: equalization_ratio = 0.827), corresponding to only 17% effective Delta P - a factor of ~5.9 reduction. The paper's own short-circuit model predicts that **open pockets are below threshold at 120 dB**, contradicting mitigation 3.

**Required action:** Replace the factor-of-five claim. Options:
1. State that for open (unsealed) segments, the mechanism is below threshold at 120 dB, reinforcing that sealed pockets are essential.
2. Replace with "factor of two" and restrict to cylindrical pockets > 20 mL (which survive 2x at ~0.53 um, barely above threshold).
3. Note that at >= 125 dB, even a 5x-reduced 100 mL pocket reaches threshold.

The sealed-pocket argument (mitigations 1 and 2) is the paper's real defence and is sound.

### m1. Equalization Ratio Formula Is Physically Incorrect (MINOR)

The code (line 396) computes:

    equalization_ratio = 1.0 / (1.0 + (f_drive / f_H) ** 2)

This is an ad hoc low-pass filter, not the standard Helmholtz transfer function. The correct undamped transfer is |T(f)| = 1/|1-(f/f_H)^2|.

At f = 7 Hz, f_H = 15.3 Hz:

| Formula               | Value |
|-----------------------|-------|
| Code (ad hoc)         | 0.827 |
| Correct, undamped     | 1.265 |
| Correct, zeta = 0.3   | 1.195 |
| Correct, zeta = 0.5   | 1.095 |
| Correct, zeta = 1.0   | 0.827 |

Below f_H, correct physics gives amplification (|T| > 1). The code coincidentally matches zeta = 1.0, but GI damping is never justified. Fix or keep discussion qualitative.

### m2. Helmholtz Parameters (L_eff, S) Are Unjustified (MINOR)

L_eff = 5 m and d = 10 mm are stated without justification. A sensitivity sweep or anatomical citations would strengthen the analysis.

---

## Round 1 Minor Issues - Status

| # | Issue | Status |
|---|-------|--------|
| m1 | Eq. (10) dimensional analysis | Not addressed |
| m2 | Impedance ratio 3600:1 (actual ~3740:1) | Not addressed |
| m3 | Frequency dependence of large cylinders | Not addressed |
| m4 | Table 2 missing cylinder lengths | Not addressed |
| m5 | delta_wall = 0.3 needs citation | Not addressed |
| m6 | Reference formatting | Not addressed |
| m7 | Thermal damping delta_th = 0.04 justification | Not addressed |
| m8 | "Only plausible mechanism" overclaim (lines 88, 768) | Not addressed |

None blocking, but m5 and m8 should be addressed before submission.

---

## Tests

All **161 tests pass**, including 8 new tests in TestHelmholtzSealedGI.

---

## Positive Comments

1. **All five Round 1 issues were addressed substantively.** The authors engaged with the critique rather than cosmetic edits.
2. **The acoustic short-circuit section (Sec. 4.2) is a genuine contribution.** The Helmholtz estimate and sealed-segment argument are physically correct.
3. **The f_H ~ 15 Hz estimate is correct** and provides a testable prediction.
4. **Code-paper consistency is now excellent.**
5. **The test suite is well-structured.**

---

## Summary

The paper has improved markedly. One new major issue: the factor-of-five robustness claim (lines 662-666) is arithmetically false. Two new minor issues concern the ad hoc Helmholtz formula and unjustified parameters.

**Bottom line:** Fix the factor-of-five claim (30 min of work), clean up the Helmholtz formula, and this paper is ready for external submission. The core physics is sound, the sealed-pocket argument is compelling, and the code is verified.