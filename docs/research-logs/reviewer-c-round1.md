# Reviewer C — Round 1

## Overall Assessment

Paper 10 advances a coherent formal framework (one theorem, three propositions, one supporting proposition) that formalises the relationship between shell geometry, spectral organisation, and inverse identifiability. The paper's central argument — that forward adequacy does not imply inverse adequacy — is a genuinely useful insight for the shell-acoustics and spectral-inverse communities.

I have run the code systematically against every quantitative claim in the paper. The headline numbers are reproducible and numerically well-behaved. The code is clean, well-structured, and passes its full test suite (44/44 for the core identifiability module). However, I have identified one potential discrepancy (prolate κ range), one subtle internal inconsistency (which model's f₂ is "the" f₂), and several observations about the relationship between the theoretical propositions and what the code can actually verify.

---

## Code Verification Results

### Claim 1: f₂ = 3.95 Hz at canonical oblate parameters (a = 0.18, c = 0.12)

| Model | Code output | Paper claim | Status |
|-------|-------------|-------------|--------|
| Sphere (equiv. radius) | 3.9524 Hz | 3.95 Hz | ✅ VERIFIED |
| 2-DOF Ritz (N=1) | 3.7995 Hz | 3.800 Hz (Appendix Table) | ✅ VERIFIED |
| Converged Ritz (N≥4) | — (not in code) | 3.678 Hz (Appendix Table) | ⚠️ Cannot verify from code |

**Concern:** The paper uses f₂ = 3.95 Hz universally as "the" canonical abdominal frequency (Results §4, Eqs. in background and results), including in the identifiability-lifting discussion where the relevant model is the Ritz oblate model (which gives f₂ = 3.80 Hz, not 3.95). The 3.95 value comes from the *sphere* model. This is not an error per se — Paper 1 used the sphere model — but it creates ambiguity when the paper simultaneously uses the Ritz model for κ = 69.4 and the sphere model's f₂ in the same paragraph (Results §4.2, line "The lowest abdominal flexural mode already sits at f₂ = 3.95 Hz").

### Claim 2: κ_oblate = 69.4 (five-mode, canonical)

| Quantity | Code output | Paper claim | Status |
|----------|-------------|-------------|--------|
| κ_oblate | 69.4 | 69.4 | ✅ VERIFIED |
| σ₁ | 1.8354 | — | — |
| σ₂ | 0.1301 | — | — |
| σ₃ | 0.0264 | — | — |

Verified via both `jacobian_condition_number()` and manual SVD. Result is stable across FD step sizes from 10⁻⁴ to 10⁻⁸.

### Claim 3: κ_sphere ≈ 1.37 × 10¹⁰

| Quantity | Code output | Paper claim | Status |
|----------|-------------|-------------|--------|
| κ_sphere | 1.368 × 10¹⁰ | 1.37 × 10¹⁰ | ✅ VERIFIED |
| σ₃ (sphere) | 1.38 × 10⁻¹⁰ | — | Confirms near-rank-deficiency |

### Claim 4: Forward error E_fwd = 0.0936

| Quantity | Code output | Paper claim | Status |
|----------|-------------|-------------|--------|
| E_fwd | 0.0936 | 0.0936 | ✅ VERIFIED |

Per-mode errors: n=2: +4.0%, n=3: +8.7%, n=4: +9.7%, n=5: +9.8%, n=6: +9.4%. All consistent with "< 0.1" and "< 10%" claims.

### Claim 5: R_eq = 0.157 m

| Quantity | Code output | Paper claim | Status |
|----------|-------------|-------------|--------|
| R_eq = (a²c)^(1/3) | 0.1572 m | 0.157 m | ✅ VERIFIED |

### Claim 6: Eccentricity ε = 0.745

| Quantity | Code output | Paper claim | Status |
|----------|-------------|-------------|--------|
| ε = √(1 − (c/a)²) | 0.7454 | 0.745 | ✅ VERIFIED |

### Claim 7: Sphere Jacobian proportionality (Theorem 1)

The code numerically verifies that for the sphere model, df_n/da / df_n/dc = 2c/a = 1.333 for ALL modes n = 2,...,6. Maximum relative error: 5.6 × 10⁻¹⁰. This confirms the chain-rule proof.

**Status: ✅ VERIFIED**

### Claim 8: Breathing mode f₀ ≈ 2490 Hz

| Quantity | Code output | Paper claim | Status |
|----------|-------------|-------------|--------|
| f₀ | 2491 Hz | ~2490 Hz | ✅ VERIFIED |

### Claim 9: Prolate κ ≈ 561–729

This is the most problematic claim. The paper (§4.3) states κ_prolate ≈ 561–729 "across the tested prolate branch" citing Papers 8 and 9.

When I run the dedicated prolate Ritz model from `universality.py` (the correct code path, as noted in Paper 8's footnote), I get:

| ε range | Code κ range | Paper claim | Status |
|---------|-------------|-------------|--------|
| 0.30–0.65 | 566–643 | 561–729 | ⚠️ PARTIAL MATCH |

The code gives a *narrower* range than claimed. The lower bound (566 vs 561) is close. The upper bound (643 vs 729) differs meaningfully — the code never reaches 729 in the ε ∈ [0.3, 0.65] range. Extending to the full default sweep (ε ∈ [0.05, 0.75]) gives κ values up to ~646, still well below 729.

**Possible explanations:** (a) The 561–729 range comes from a wider ε range than tested; (b) different canonical parameters were used; (c) the code has been updated since the number was generated.

**Status: ⚠️ PARTIAL DISCREPANCY — lower bound matches, upper bound differs by ~13%**

### Claim 10: σ₃(ε) = λ₁ε² + O(ε⁴) with σ₃(0) = 0

This is a *theoretical* claim (Proposition 3) about the continuum problem. The 2-DOF Ritz code shows:

| ε | σ₃ | σ₃/ε² |
|---|-----|--------|
| 0.045 | 0.00705 | 3.527 |
| 0.141 | 0.01298 | 0.652 |
| 0.199 | 0.01096 | 0.277 |
| 0.312 | 0.01130 | 0.116 |
| 0.745 | 0.02639 | 0.048 |

The code does NOT show σ₃ → 0 as ε → 0. Instead, σ₃ plateaus at ~0.007. The ratio σ₃/ε² is NOT converging to a constant — it diverges as ε → 0.

The paper explicitly identifies this as a "discretisation artefact of the low-order Ritz spherical limit" (Proposition 3 proof and Results §4.3). The sphere-blending transition at c/a = 0.98 adds further numerical complications. The theoretical proof relies on symmetry arguments (even expansion in ε, Theorem 1 at ε = 0) that are sound but cannot be verified from the 2-DOF code.

**Status: ⚠️ THEORETICAL CLAIM — consistent with paper's stated caveats but unverifiable from code**

### Claim 11: Coupling ratio R ≈ 3.3 × 10⁴

The code gives R ≈ 24,900 (at 0.5 m/s²) or R ≈ 49,800 (at 1.0 m/s²) depending on the mechanical excitation amplitude. The paper's R ≈ 33,000 likely corresponds to a specific comparison scenario. Order-of-magnitude is correct.

**Status: ✅ ORDER-OF-MAGNITUDE VERIFIED (exact value depends on comparison scenario)**

### Claim 12: Robustness — κ_oblate ∈ [27, 210]

| Parameter sweep | Code range | Paper claim | Status |
|----------------|------------|-------------|--------|
| E ∈ [0.01, 1.0] MPa | 26.9–210.2 | 27–210 | ✅ VERIFIED |
| Drop n=2 | κ = 468.1 | ~468 | ✅ VERIFIED |
| All leave-one-out | 62.9–468.1 | O(10¹)–O(10²) | ✅ VERIFIED |

### Claim 13: Quadrature convergence by N_quad = 20

f₂ is converged to machine precision by N_quad = 15 (all digits agree for N ≥ 15). The claim "converged by N_quad = 20" is conservative and correct.

**Status: ✅ VERIFIED**

---

## Reproducibility Issues

1. **The prolate κ range 561–729 cannot be exactly reproduced.** The code gives 566–643. A reader following the code would obtain different bounds. This needs either an updated number in the paper or documentation of the exact ε range and parameters used to produce 561–729.

2. **The σ₃ ∝ ε² asymptotic cannot be demonstrated from the code.** This is correctly flagged in the paper as a theoretical result, but a reviewer or reader looking to verify it numerically would see the opposite (a finite floor). The paper could be improved by showing the code-level behavior alongside the theoretical prediction.

3. **Which f₂ is "the" f₂?** A reader wanting to reproduce Table 1 would get f₂ = 3.95 Hz from the sphere model or f₂ = 3.80 Hz from the Ritz model. The paper uses 3.95 throughout but the identifiability results use the Ritz model. This is not wrong but requires careful reading to disambiguate.

4. **No enriched-basis code available.** The convergence table (Appendix, N ≥ 2) references higher-DOF Ritz results that are not present in the current codebase. Only the N = 1 (2-DOF) result can be verified.

---

## Uncertainty and Statistical Rigour

1. **No uncertainty on κ_oblate = 69.4.** The finite-difference step sensitivity is excellent (κ is stable from step = 10⁻⁴ to 10⁻⁸), but there is no reported uncertainty from parameter uncertainty. Given the robustness sweep shows κ ∈ [27, 210] over physically plausible ranges, reporting κ = 69.4 as a point value is defensible but incomplete.

2. **No Monte Carlo or bootstrap for κ.** The paper performs MC for some quantities in earlier papers (f₂ distributions) but not for κ itself. Given that κ is the paper's headline metric, some form of uncertainty quantification would strengthen the claim.

3. **The "gap exceeds 10⁷" claim (§4.5) is well-supported.** κ_sphere/κ_oblate ranges from 10⁸ to 10¹¹ across all tested configurations. This is a robust qualitative finding.

---

## Major Issues

**M1. Prolate κ range discrepancy.** The claimed range 561–729 is not reproducible from the current code (which gives 566–643). Either update the paper's numbers or document the exact computational setup that produced the claimed range. This is minor in the sense that the qualitative conclusion (prolate κ is "high and flat") is unchanged, but it is a reproducibility failure for the specific numbers.

**M2. Ambiguous f₂.** The paper reports f₂ = 3.95 Hz as if it comes from "the" model, but this is the sphere model value. The Ritz model used for identifiability gives 3.80 Hz. The converged Ritz gives 3.678 Hz. This creates the impression that the oblate Ritz model and the sphere model agree on f₂, which obscures the forward error. Recommendation: explicitly label which model produces which f₂ value in the cross-application table and in Results §4.2.

---

## Minor Issues

**m1.** The finite-difference step δ = 10⁻⁶ is stated in Theory §3.1 but not in the code's default. The code uses `step_fraction=1e-6` as the default, so this is consistent — but stating it in both places is good practice. ✅ Consistent.

**m2.** The paper's Proposition 3 proof uses the first-order eigenvalue perturbation argument (Eq. 25) correctly but does not verify it numerically. A supplementary figure showing the actual σ₃ vs ε² alongside the theoretical prediction would strengthen the claim.

**m3.** The coupling ratio R ≈ 3.3 × 10⁴ is cited from Paper 1 without specifying the exact comparison scenario (which acceleration amplitude, which SPL). The code output depends on this choice. This is inherited from Paper 1 and not Paper 10's fault, but a footnote clarifying the specific comparison would help.

**m4.** Table 1 gives R_eq = 0.157 m for the abdomen but the exact code value is 0.1572 m. This rounding is fine for a table but should be consistent with the precision used elsewhere.

**m5.** The convergence table (Appendix) claims N ≥ 4 converged value of 3.678 Hz but the enriched-basis code is not in the repository. This means the table cannot be independently verified.

---

## What's Done Well

1. **Exceptional numerical stability.** The κ = 69.4 result is rock-solid across four decades of FD step size and robust to parameter perturbations. This is not always the case with condition-number analyses of shell models.

2. **Clean code architecture.** The separation between `oblate_spheroid_ritz.py` (forward model), `kac_identifiability.py` (inverse analysis), and `universality.py` (cross-geometry comparisons) is well-designed. Parameter normalisation handles multiple naming conventions gracefully.

3. **Comprehensive test suite.** 44 tests for the identifiability module alone, covering edge cases, round-trip inversions, and numerical consistency.

4. **The Theorem 1 verification is elegant.** The chain-rule proportionality check (ratio = 2c/a across all modes to 10⁻¹⁰ precision) provides a clean computational confirmation of the rank-deficiency theorem.

5. **The robustness analysis is thorough.** The sweeps over E, h, ρ_f, and mode subsets convincingly demonstrate that the qualitative finding (κ_oblate << κ_sphere) is not parameter-specific.

6. **The forward-inverse gap concept is original and well-quantified.** The E_fwd = 0.0936 with κ_sphere/κ_oblate ≈ 2 × 10⁸ is a striking concrete demonstration of the paper's central thesis.

---

## Summary Recommendation: MINOR REVISION

The paper is substantially sound. The headline numbers (κ_oblate = 69.4, κ_sphere ≈ 1.37 × 10¹⁰, E_fwd = 0.0936) are exactly reproducible from the code. The four formal results are well-stated and supported by computational evidence. The following items should be addressed:

1. **[Required]** Correct or document the prolate κ range (561–729 vs 566–643 from current code).
2. **[Required]** Clarify in the cross-application table and §4.2 that f₂ = 3.95 Hz is the sphere-model value, while the Ritz model gives f₂ = 3.80 Hz. This matters because the reader may not realise the identifiability analysis operates on a different frequency spectrum than the one reported in the table.
3. **[Recommended]** Add a supplementary figure or remark showing the numerical σ₃(ε) behavior from the 2-DOF Ritz code (finite floor) alongside the theoretical quadratic prediction, to make the "discretisation artefact" claim verifiable.
4. **[Recommended]** Include the enriched-basis code (N ≥ 2) in the repository, or add a note that the convergence table values were computed with code not included in the companion release.
