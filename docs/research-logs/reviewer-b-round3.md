# Reviewer B — Round 3 (Verification Review)

**Paper:** "What pitch is a growling stomach? A unified multi-mode acoustic model of borborygmi"
**Manuscript:** `projects/borborygmi/paper/main.tex`
**Code:** `src/analytical/borborygmi_model.py`
**Tests:** `tests/test_borborygmi.py` (58 tests, all passing)
**Total project tests:** 206 collected, all passing

## Decision: ACCEPT

---

## Fix-by-Fix Verification Table

| # | Fix | Claimed | Independently Verified | Status |
|---|-----|---------|----------------------|--------|
| F2 | Radial breathing mode rederived with per-displacement stiffness (1329→163 Hz) | k_gas=2γP₀/R, k_wall=Eh/[R²(1−ν²)] → f_r≈163 Hz | Computed: f_r=162.8 Hz. Dimensional analysis confirms [Pa/m]/[kg/m²]→[1/s²]. Cylindrical plane-strain hoop stiffness factor 1/(1−ν²) is correct. Gas compressibility factor 2 (vs 3 for sphere) follows from δV/V=2δR/R for cylinder. OLD total-stiffness formulation (without /R divisors) gives ~20 Hz, not 1329 Hz — the pre-fix error was evidently a different variant. | ✅ VERIFIED |
| F1 | Axial sub-audibility threshold corrected (1 mL → ~10 mL) at 4 locations | f_ax < 100 Hz for V > ~10 mL | Computed exact crossover: V=9.88 mL (f=100 Hz). Paper says "~10 mL" — correct. Checked L.352, L.447, L.601, L.730: all four threshold statements are internally consistent. | ✅ VERIFIED |
| M1 | Axial scaling V⁻¹ → V⁻¹/² at 2 locations | f_ax ∝ V⁻¹/² | Algebraically: k_ax = γP₀π²R⁴/V → ω² ∝ 1/V → f ∝ V⁻¹/². Numerically: f(1 mL)/f(10 mL) = 3.1623 = √10. Paper L.347, L.411, L.598 all say V⁻¹/². No remaining V⁻¹ claims found. | ✅ VERIFIED |
| M3 | Q vs burst duration inconsistency acknowledged | Q=4 → τ≈18 ms vs 0.5–0.8 s bursts; now explained as sustained excitation | Computed: Q/f = 4/223 = 17.9 ms ≈ 18 ms. Paper L.684–695 now explicitly states that Q characterises spectral width, not temporal duration, and that observed bursts are sustained excitation events. Physically sound explanation. | ✅ VERIFIED |
| M4 | Five mechanisms → four (Minnaert as limiting case) | Abstract, Sec 2, Conclusions all say "four" | Searched for "five" / "5 mech" — zero hits. "Four" appears at L.44, L.112, L.140, L.710 — all consistent. Limiting-case reduction verified: constrained(E=0, h→0) = Minnaert to machine precision. | ✅ VERIFIED |
| — | 3 new regression tests (206 total) | test_radial_canonical_regression, test_axial_scaling_v_minus_half, test_axial_subaudible_threshold_10mL | All three present at L.129, L.141, L.148 of test file. Total suite: 206 collected, 58 in borborygmi file. All pass. | ✅ VERIFIED |

---

## Fatal Flaws

None.

## Major Issues

None remaining.

## Minor Issues (observations, not blocking)

### M1 (cosmetic). Code docstrings still reference "all 5" modes

The `mode_transition_map` docstring (L.471) says "Compute all 5 mode frequencies" and `plot_mode_transition_map` (L.692) says "all 5 resonance modes." This is *technically* correct — the code does compute 5 frequency curves including Minnaert — but creates a slight tension with the paper's "four mechanisms" framing. Consider aligning the docstrings, e.g., "all 5 frequency curves (4 mechanisms plus the Minnaert limiting case)."

### M2 (precision). Ring-down multiplier bounds

L.689–690: "30–45× shorter than the observed 0.5–0.8 s bowel sound burst durations." Strictly, 500/18 = 27.8× and 800/18 = 44.4×, so "~28–44×" would be more precise. The lower bound overshoots by ~8%. This is an order-of-magnitude comparison making a qualitative point, so it is not misleading, but "approximately 30–45×" or "~28–45×" would be marginally more defensible.

### M3 (modelling note). Plane-strain assumption in radial mode

The cylindrical wall stiffness uses the plane-strain factor 1/(1−ν²). For gas slugs shorter than the tube diameter (V < ~5 mL, L_slug < 7 mm in a 30 mm tube), plane stress (no (1−ν²) correction) would be more appropriate, introducing a ~25% difference in k_wall. Since k_wall is only 0.9% of k_gas for the canonical parameters, this changes f_r by < 0.5%, so it is not a practical concern. A footnote acknowledging this would be thorough but is not required.

### M4 (notation). Ring-down time definition

The "free ring-down time" of 18 ms is defined as Q/f (the time for Q oscillation periods, during which amplitude decays to e⁻π ≈ 4.3%). The more standard definition is the e-folding time 1/(ζω) = Q/(πf) = 5.7 ms. Both are valid; the comparison with burst durations holds regardless. A one-line clarification of which convention is used would forestall reviewer confusion.

---

## Positive Comments

1. **All six fixes are correctly implemented.** Every claimed correction was verified by independent hand calculation and matches the code and paper to ≤1 Hz. This is the kind of revision response I wish I saw more often.

2. **The per-displacement stiffness rederivation (F2) is now physically correct.** The cylindrical gas compressibility factor of 2 (from δV/V = 2δR/R) and the plane-strain hoop stiffness Eh/[R²(1−ν²)] are standard thin-shell results. The resulting 163 Hz is now dimensionally consistent and physically plausible for a 30 mm elastic tube.

3. **The V⁻¹/² scaling for the axial mode is algebraically exact** (k ∝ 1/V, m = const → ω ∝ V⁻¹/²), and the numerical tests confirm it to 4 decimal places.

4. **The sustained-excitation interpretation of the Q vs. burst-duration mismatch (M3) is physically sound** and is now honestly stated in the limitations section rather than swept under the rug.

5. **The Minnaert-as-limiting-case framing (M4) is clean.** The analytical reduction is exact, the numerical verification is in the test suite, and the paper consistently uses "four mechanisms" throughout.

6. **Regression tests are well-targeted.** Each new test directly guards against the specific error it was written to prevent: the radial canonical value (163 Hz ± 1), the V⁻¹/² scaling ratio, and the 10 mL sub-audibility crossover.

7. **The canonical parameter table (Table 1) and mode frequency table (Table 2) are now internally consistent with both the equations and the code output.** Cross-checked: Minnaert 244 Hz, constrained 223 Hz, Helmholtz 647 Hz, axial 99 Hz, radial 163 Hz — all match to ≤1 Hz.

---

## Summary

All five major issues raised in Round 2 have been correctly addressed. The radial breathing mode equation has been properly rederived from first principles with per-displacement stiffness, yielding a physically reasonable 163 Hz (verified independently). The axial scaling, threshold, and mechanism-count corrections are all internally consistent across the paper, code, and test suite. The Q vs. burst-duration tension is now honestly acknowledged with a physically sound interpretation.

The paper presents a clean, self-consistent, first-principles analytical model that makes falsifiable predictions without curve-fitting. The minor issues noted above are cosmetic and do not affect any scientific conclusions. I am satisfied that this manuscript is ready for publication.

**Verdict: ACCEPT**
