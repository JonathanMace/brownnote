# Reviewer C — Paper 2 Round 1

**Paper:** "Bowel Gas as an Acoustic Transducer: A Constrained Bubble Model for
Infrasound-Induced Mechanotransduction in the Gastrointestinal Tract"

**Code reviewed:** src/analytical/gas_pocket_detailed.py
**Figure script reviewed:** paper2-gas-pockets/generate_figures.py

**Date:** 2026-03-27
**Reviewer:** C (computational mechanics / reproducibility specialist)

---

## Overall Assessment

The physics is clean, the code is well-structured, and many of the central claims
check out. Table 2 resonance frequencies reproduce exactly, the 50–100× efficiency
claim is numerically sound, and the Paper 1 canonical displacement (0.014 µm) is
correctly cross-referenced. However, I found **two numerical discrepancies** between
the text and the code output, plus one **misleading framing** of the Monte Carlo
result. These should be corrected before submission.

---

## Code Verification Results

### 1. Table 2 — Resonance Frequencies ✅ ALL MATCH

| V (mL) | Geometry | a/R (mm) | f_Minnaert (Hz) | f₀ (Hz) | Paper | Code | Match |
|---------|----------|----------|-----------------|---------|-------|------|-------|
| 1  | Spherical    | 6.2  | 524  | 5556 | 5556 | 5556 | ✅ |
| 5  | Spherical    | 10.6 | 306  | 2653 | 2653 | 2653 | ✅ |
| 10 | Spherical    | 13.4 | 243  | 1916 | 1916 | 1916 | ✅ |
| 20 | Spherical    | 16.8 | 193  | 1379 | 1379 | 1379 | ✅ |
| 50 | Spherical    | 22.9 | 142  | 889  | 889  | 889  | ✅ |
| 100| Spherical    | 28.8 | 113  | 635  | 635  | 635  | ✅ |
| 10 | Cylindrical  | 15.0 | —    | 99   | 99   | 99   | ✅ |
| 50 | Cylindrical  | 15.0 | —    | 44   | 44   | 44   | ✅ |
| 100| Cylindrical  | 15.0 | —    | 31   | 31   | 31   | ✅ |

Cylindrical radial mode: code gives 1323 Hz; paper footnote says "~1323 Hz". ✅

### 2. Figure 2 — SPL Thresholds ⚠️ PARTIAL MISMATCH

**Spherical pockets:**
- 5 mL: paper says ~120 dB, code gives 120.2 dB ✅
- 100 mL: paper says ~111 dB, code gives 111.4 dB ✅
- 9-dB range (5→100 mL spherical): 120.2 − 111.4 = 8.8 dB ≈ 9 dB ✅

**Cylindrical pockets:**
- Paper (Section 4.2, line ~487): "threshold is nearly independent of volume (~118 dB)"
- **Code gives: ~113.5 dB for ALL cylindrical volumes (1–200 mL)**
- **This is a 4.5 dB discrepancy.** Traced to: k_eff_cyl = 19.08 MPa/m,
  p_needed = k_eff × 0.5 µm = 9.54 Pa → SPL = 113.6 dB.
- The wall stiffness (167 kPa/m) is negligible vs gas stiffness (18.9 MPa/m),
  so the threshold is controlled entirely by 2γP₀/R and is volume-independent by construction.
- **This error appears in the text only; the code and Figure 2 are correct.**

### 3. Figure 3 — Monte Carlo Population ⚠️ NUMBERS DON'T MATCH TEXT

Ran with seed=42, N=10,000, verified across 50 seeds (500k total):

| Quantity | Paper claim | Code (seed=42) | Code (50 seeds range) |
|----------|------------|----------------|----------------------|
| Fraction above 0.5 µm | 100% | 100% | 100% (all seeds) ✅ |
| Displacement range | 0.6–3.5 µm | 1.024–2.661 µm | 0.917–2.920 µm ❌ |
| Median displacement | ~1.2 µm | 1.079 µm | ~1.08 µm (stable) ❌ |
| Total gas 95% CI | ~[70, 570] mL | — | — |

**Root cause:** The paper's displacement range (0.6–3.5 µm) does not match code
output. With 70% cylindrical geometry, the minimum displacement is always ~1.0 µm
because cylindrical k_eff depends on the fixed lumen radius R=15 mm, not pocket
volume. The lower bound 0.6 µm could only occur if spherical geometry dominated
(and it doesn't at 70% cylindrical probability). The upper bound 3.5 µm would
require extremely large spherical pockets not produced by the MC distribution.

The 95% CI for total bowel gas is also slightly off: the theoretical 95% CI for
log-normal(ln 200, 0.65) is [56, 715] mL, not [70, 570] mL as stated. The paper
may have intended a different CI (e.g., IQR) or a different σ_ln.

### 4. Figure 4 — Pathway Comparison ✅ CORRECT

Paper 1 canonical value verified against self_consistent_displacement():
- Energy-consistent ξ at 120 dB, n=2: 0.01374 µm ≈ 0.014 µm ✅
- Figure 4 hardcodes xi_ref_120dB_um = 0.014 — correct (0.98× exact) ✅

### 5. 50–100× Efficiency Claim ✅ VERIFIED

At 120 dB, 7 Hz (whole-cavity reference = 0.014 µm):

| Gas pocket | ξ (µm) | Ratio vs whole-cavity |
|-----------|--------|----------------------|
| 5 mL cylindrical | 1.051 | 75× |
| 20 mL cylindrical | 1.058 | 76× |
| 100 mL spherical | 1.341 | 96× |

The 50–100× range is numerically accurate. ✅

### 6. Paper 1 Test Suite ✅ 118/118 PASSED

`
118 passed, 1 warning in 11.20s
`

### 7. Dimensional Consistency ✅ ALL EQUATIONS CHECKED

- Eq 3–4 (spherical stiffness/mass): [Pa]/([m²]·[kg/m²]) = [1/s²] ✅
- Eq 8 (cylindrical radial): same structure ✅
- Eq 9 (cylindrical axial): [N/m]/[kg] = [1/s²] ✅
- Eq 13 (k_eff sphere): [Pa/m] ✅
- Eq 14 (k_eff cylinder): [Pa/m] ✅
- Eq 11 (forced displacement): [Pa]/[Pa/m] = [m] ✅
- Eq 16 (volume displacement): [m²]·[m] = [m³] ✅
- Code k_eff values match paper formulas exactly (verified for 10, 50, 100 mL) ✅
- Resonance ω₀² derivable from k_eff and effective mass — verified ✅

---

## Reproducibility Issues

1. **Figure 3 is reproducible** with seed=42 — same output every time. ✅
2. **Figure 2** is also reproducible (deterministic binary search). ✅
3. **BUT:** The paper text describing Figure 3 results cannot be reproduced
   from the code. Someone running the code would get median 1.08 µm, not 1.2 µm,
   and range 1.02–2.66 µm, not 0.6–3.5 µm.
4. **Missing:** The generate_figures.py script is not referenced in the paper's
   data availability section — just "[repository URL]".

---

## Uncertainty and Statistical Rigour

### What's done
- Monte Carlo over gas volume distribution and pocket count (N=10,000)
- Dirichlet partitioning of total volume into pockets — sensible choice
- Log-normal gas distribution grounded in literature

### What's missing (partial UQ is worse than no UQ)

1. **No UQ on tissue mechanical parameters.** E_w = 10 kPa is used as a point
   estimate but literature values range from 5–50 kPa. Since k_wall ≪ k_gas for
   cylindrical pockets, this barely matters there, but for small spherical pockets
   (where k_wall can matter) it could shift thresholds by several dB.

2. **No UQ on wall thickness h_w.** Literature gives 2–4 mm for intestinal wall.
   This directly scales k_wall.

3. **No UQ on the PIEZO threshold.** The paper acknowledges the 0.5–2.0 µm range
   but uses only 0.5 µm in all calculations. A sensitivity analysis showing
   thresholds at 0.5, 1.0, and 2.0 µm would be more honest.

4. **No UQ on lumen radius R.** This is the most critical parameter for
   cylindrical pockets (k_eff ~ 1/R). Small intestine R ≈ 12–18 mm; large
   intestine R ≈ 25–35 mm. The choice of R=15 mm determines the cylindrical
   threshold entirely.

5. **Sobol sensitivity indices** not computed. Which parameter dominates the
   SPL threshold variance? (Almost certainly R for cylindrical, volume for
   spherical.)

6. **N=10,000 adequacy.** For the 100% claim (testing a lower tail), 10,000
   is sufficient since even 500k samples (50 seeds) never produce a failure.
   However, the paper should note that this is because the 70% cylindrical
   geometry assumption guarantees ξ > 1 µm for essentially all individuals.
   **The 100% claim is a model artifact of the fixed R_lumen assumption, not a
   robust finding about human physiology.**

---

## Major Issues

### M1. Cylindrical SPL threshold: paper says ~118 dB, code gives ~113.5 dB

- **Location:** Section 4.2, line ~487
- **Severity:** The 4.5 dB error means the paper text is wrong. Figure 2
  (generated from code) will show ~113.5 dB, contradicting the text.
- **Fix:** Change "~118 dB" to "~114 dB" in the text.

### M2. Monte Carlo displacement statistics don't match code

- **Location:** Section 4.3, lines ~518–521
- **Paper says:** "spans approximately 0.6–3.5 µm, with a median of ~1.2 µm"
- **Code gives:** range 1.02–2.66 µm (seed=42), median 1.08 µm
- **Severity:** The lower bound is wrong by 70% and the median is wrong by 11%.
  These are the kind of numbers reviewers will check.
- **Fix:** Update text to: "spans approximately 1.0–2.7 µm, with a median of
  ~1.1 µm." Or re-run with varied tissue parameters to get a wider range.

### M3. 95% CI for bowel gas distribution stated incorrectly

- **Location:** Section 2.6, line ~418
- **Paper says:** "95% CI of approximately 70–570 mL"
- **Theory gives:** [56, 715] mL for log-normal(ln 200, 0.65)
- **Fix:** Either correct the CI or state it as an approximate range.

---

## Minor Issues

### m1. Cylindrical "volume-independent" threshold framing

The paper correctly notes that cylindrical threshold is "nearly independent of
volume" — but should explain WHY: k_eff is dominated by gas stiffness 2γP₀/R,
which depends only on the fixed lumen radius, not pocket length. This is an
interesting physical insight that deserves a sentence.

### m2. Wall damping dominates all other damping terms

At 7 Hz, δ_wall = 0.3 accounts for 88% of total damping. The radiation (δ_rad
≈ 0.0004), thermal (δ_th = 0.04), and viscous (δ_vis ≈ 0.0004) terms are
negligible. The paper should note this, and cite a source for δ_wall = 0.3.
Currently line 304 gives no reference for this value.

### m3. Magic number: δ_wall = 0.3

The structural loss tangent of 0.3 is hardcoded without citation or uncertainty
range. Intestinal wall loss tangent literature gives 0.1–0.5 depending on
frequency and tissue type. This should be cited and its impact on results noted
(though since H ≈ 1.0 in the sub-resonant regime, damping barely matters for
the displacement calculation — this should be stated explicitly).

### m4. Abstract claims "100 mL pocket → 111 dB" without specifying geometry

The abstract says "111 dB (100 mL pocket)" but this is the SPHERICAL result.
The cylindrical 100 mL gives 113 dB. Since most bowel gas is cylindrical (by
the paper's own 70/30 assumption), the abstract should clarify geometry.

### m5. The 100% claim is model-determined, not empirically robust

Because the MC uses 70% cylindrical geometry and cylindrical pockets always
give ξ ≈ 1.05 µm at 120 dB (regardless of volume), the "100% exceed threshold"
result is guaranteed by construction. It would fail for an all-spherical
population with small pockets. The paper should discuss this sensitivity.

### m6. Hardcoded Paper 1 value in generate_figures.py

Line 326 of generate_figures.py hardcodes xi_ref_120dB_um = 0.014. This should
be computed from Paper 1's self_consistent_displacement() for full traceability,
or at minimum have a comment noting the exact computed value (0.01374 µm).

### m7. No comparison with axial-mode sub-resonant response

For cylindrical pockets, the paper computes both radial and axial resonance
frequencies but the forced response (Section 2.4) uses only the RADIAL k_eff.
The axial mode's sub-resonant displacement could be different and should be
discussed.

---

## What's Done Well

1. **Code quality is high.** Clear dataclasses, well-documented functions,
   consistent units throughout. No unit conversion errors found.

2. **Physics is sound.** The constrained-bubble model is well-motivated, the
   equations are correct, and the dimensional analysis holds.

3. **Table 2 is flawless.** Every number reproduces exactly.

4. **Cross-referencing Paper 1 is done correctly.** The energy-consistent
   displacement (0.014 µm) is the right value to use, not the pressure-based
   one (0.184 µm).

5. **The 50–100× claim is honest.** The ratios (75–96×) genuinely span
   that range and use the correct Paper 1 baseline.

6. **Paper 1 test suite passes** (118/118), confirming the foundation hasn't
   regressed.

7. **MC is seeded and reproducible.** Seed=42 gives identical output every
   time.

---

## Summary Recommendation: MINOR REVISION

The physics and code are solid. The three textual discrepancies (cylindrical
threshold, MC statistics, gas CI) are straightforward fixes — likely stale
numbers from an earlier version of the model that weren't updated when the
code was refined. The missing UQ on tissue parameters is a limitation worth
acknowledging but not blocking. Fix the numbers, add the geometric sensitivity
note, and this is ready.

**Priority fixes:**
1. Correct "~118 dB" → "~114 dB" for cylindrical threshold (or re-derive)
2. Update MC displacement range and median to match code output
3. Correct the 95% CI for gas distribution
4. Add one sentence noting the 100% result depends on cylindrical geometry assumption
