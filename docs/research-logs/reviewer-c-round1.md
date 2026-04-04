# Reviewer C — Round 1

## Overall Assessment

Paper 10 advances a capstone thesis: in fluid-filled viscoelastic shells, geometry simultaneously filters forcing, organises spectra, and determines inverse identifiability. It formalises this through four proved results (two theorems, two propositions) plus one supporting excitation proposition, illustrated across abdominal, watermelon, bladder, and borborygmi applications. The mathematical framework is well-structured and the key identifiability claims (rank collapse under scalar reduction, lifting by oblate asphericity) are verified by code. However, I find one significant discrepancy between the paper's asymptotic claims and what the code actually computes, along with several numerical mismatches.

---

## Code Verification Results (show your work!)

### 1. Eccentricity and Equivalent Radius — ✅ MATCH

```
Code:  ε = sqrt(1 - (0.12/0.18)²) = 0.7454
Paper: ε = 0.745  ✓

Code:  R_eq = (0.18² × 0.12)^(1/3) = 0.1572 m
Paper: R_eq = 0.157 m  ✓ (rounding)

Watermelon: R_eq = (0.158² × 0.123)^(1/3) = 0.1453 m
Paper: R_eq = 0.1453 m  ✓
```

### 2. Condition Numbers — ✅ MATCH at canonical point

```
Code (kac_identifiability):
  κ_oblate  = 69.4       Paper: 69.4  ✓
  κ_sphere  = 1.37×10¹⁰  Paper: 1.37×10¹⁰  ✓
  Gap ratio = 1.97×10⁸   Paper: ~2×10⁸  ✓
```

### 3. Forward Error — ✅ MATCH

```
Code:  E_fwd = 0.0936 (9.36%)
Paper: E_fwd = 0.0936 < 0.1  ✓
```

### 4. Singular Values — ✅ MATCH

```
Oblate Ritz SVs:  [1.8354, 0.1301, 0.0264]
Sphere SVs:       [1.89, 0.112, 1.38×10⁻¹⁰]
```

σ₃(sphere) ≈ 10⁻¹⁰ confirms numerical rank deficiency. The sphere model's J[:,a]/J[:,c] = [2, 2, 2, 2, 2] exactly, confirming the chain-rule prediction in Theorem 1.

### 5. Kernel-Direction Test — ✅ MATCH

```
v_null = (1, -2, 0)/√5  (preserves R_eq)
||J̃_ritz · v_null||   = 1.1013  (full model sees null dir)
||J̃_sphere · v_null|| = 2.22×10⁻¹⁰  (sphere blind)  ✓
```

### 6. f₂ = 3.95 Hz — ⚠️ MISLEADING ATTRIBUTION

```
Sphere model f₂   = 3.9524 Hz  → matches paper's "f₂ = 3.95 Hz"
Oblate Ritz f₂    = 3.7995 Hz  → does NOT match
```

The paper states (background.tex, line 68): "the second mode occurring at f₂ = 3.95 Hz" when describing the abdominal model. This is the equivalent-sphere value, not the oblate Ritz value. Since the paper's central thesis is that the oblate model is the correct one (and the sphere is rank-deficient), it should report f₂ = 3.80 Hz from the Ritz model, or at minimum clarify which model produces the stated frequency. The 3.95 Hz value appears at least 3 times in the paper (Eqs. background-f2, results §4.2, discussion §5.2).

### 7. Prolate κ Range — ❌ MISMATCH

```
Code (30-point sweep over ε ∈ [0.05, 0.80]):
  κ_prolate range: [334.1, 741.5]

Paper (results.tex, line 265):
  κ_prolate ≈ 561–729
```

The paper's range appears cherry-picked from the middle of the eccentricity sweep (roughly ε ∈ [0.10, 0.70]). The full range extends lower (334 at ε ≈ 0.05 and 0.80) and higher (741 at ε ≈ 0.72). The paper should report the actual range or specify the eccentricity domain.

### 8. general_identifiability.py Misreports Canonical κ — ⚠️

The script output says "κ at canonical (ε≈0.75): 87.5" but this is actually the value at ε = 0.80 (the nearest log-spaced grid point), not at the true canonical ε = 0.745. The value at the actual canonical point is 69.4 (from kac_identifiability). This is an internal inconsistency in the computational pipeline.

---

## Reproducibility Issues

### R1. Two Different R Values

`kac_identifiability.py` uses the exact canonical parameters (a=0.18, c=0.12), while `universality.py` uses `R=0.157` (CANONICAL_PARAMS) which gives R_eq = 0.157 ≠ (0.18²×0.12)^(1/3) = 0.1572. The rounding to 3 significant figures causes the universality module to derive slightly different (a,c) values at any given eccentricity: a = 0.1797 vs 0.1800, c = 0.1199 vs 0.1200. This produces κ = 69.6 vs 69.4 — a small but unnecessary discrepancy.

### R2. Sphere vs. Ritz Model at the Sphere Limit

At the exact sphere (a = c = 0.18):
```
Oblate Ritz f₂ = 3.050 Hz
Sphere f₂      = 3.353 Hz
```

These differ by ~10%, showing the Ritz model does NOT reduce to the sphere model at c/a = 1. This is noted in the source code (oblate_spheroid_ritz.py, line 393: "the 2-DOF single-mode Ritz has a systematic ~8% offset vs the analytical sphere formula at c/a→1") but is not acknowledged in the paper.

### R3. Figure Reproducibility

The scripts are well-structured and produce the figures directly. Running `python scripts/forward_inverse_gap.py` from the repo root produces `fig_forward_inverse_gap.{pdf,png}` and `python scripts/general_identifiability.py` produces `fig_general_identifiability.{pdf,png}`. Both run cleanly and produce consistent output.

---

## Critical Assessment: Near-Spherical Asymptotics (Proposition 3 and Corollary 1)

### The Paper Claims

Proposition 3 states: σ₃(ε) = λ₁ε² + O(ε⁴) with σ₃(0) = 0.
Corollary 1 states: κ(ε) = (σ₁(0)/λ₁)·ε⁻² + O(1) as ε → 0.

### What the Code Shows

Running the oblate Ritz model from ε = 0.014 (c/a = 0.9999) to ε = 0.745:

```
c/a      ε        σ₃        σ₃/ε²     κ
0.9999   0.0141   0.00705   0.6522    268.7
0.9990   0.0447   0.00705   0.2768    268.5
0.9980   0.0632   0.00708   0.1773    267.1
0.9950   0.0999   0.00796   0.0798    235.0
0.9900   0.1411   0.01298   0.0652    144.3
0.9800   0.1990   0.01096   0.0278    168.8
0.9500   0.3122   0.01130   0.0116    162.7
0.6670   0.7451   0.02639   0.0048    69.5
```

**σ₃ does NOT approach zero as ε → 0.** It plateaus at ~0.007 for ε < 0.1. Consequently, σ₃/ε² diverges (0.65 at ε = 0.014), which is the opposite of what approaching a constant λ₁ would show. The condition number κ also plateaus at ~268 near the sphere rather than diverging as ε⁻².

### Assessment

The paper's Proposition 3 and Corollary 1 are **not verified by the code**. The Ritz model exhibits a finite σ₃ floor (~0.007) and a finite κ ceiling (~268) near the sphere. The paper describes this as a "discretisation artefact of the low-order Ritz spherical limit" and claims the "continuum inverse problem" would have σ₃(0) = 0, but:

1. The proposition is stated for "a smooth one-parameter oblate family of **Ritz shell models**" (emphasis mine) — i.e., the very model that shows the floor.
2. The column ratios J[:,0]/J[:,1] in the Ritz model at c/a = 0.9999 are [4.70, 2.23, 1.26] — they do NOT converge to a common value (the sphere has [2, 2, 2, 2, 2]). The Ritz model retains geometric information even at near-unity aspect ratios because its oblate spheroidal coordinate system is fundamentally different from the sphere model.
3. No independent computation (e.g., FEM, higher-order Ritz) is provided to verify σ₃(0) = 0 in any "continuum" sense.

The theoretical argument (symmetry → rank collapse at ε = 0) is logically sound for the true continuum problem, but the proposition is stated for the Ritz model, and the Ritz model doesn't satisfy it. This is a significant gap between theory and computation.

### Oblate κ Sweep is Non-Monotonic

The universality module's oblate sweep shows:
```
ε = 0.05:  κ = 268.4
ε = 0.16:  κ = 124.4  (local minimum)
ε = 0.22:  κ = 168.0  (increases again)
ε = 0.80:  κ = 87.5
```

The paper's power-law fit gives κ ~ 94.7·ε⁻⁰·³⁶ (R² = 0.80), not ε⁻². The exponent is off by a factor of ~5.5 from the theoretical prediction. Even interpreting the theory as an asymptotic (ε → 0) result, the code shows the scaling is nowhere near ε⁻² in any regime.

---

## Mathematical and Logical Review of Proofs

### Proposition 1 (Breit–Wigner): ✅ Correct

Standard result from acoustic scattering theory. The proof is a textbook derivation. Dimensional analysis confirms [m²] for σ_abs. The efficiency factor 4x/(1+x)² ≤ 1 with equality at x = 1 is elementary AM-GM. The Rayleigh-limit scaling ζ_rad ∝ (ka)^(2n+2) is standard.

Numerical check: at f = 4 Hz, a = 0.18 m, ka = 0.013, so (ka)⁶ = 5.3 × 10⁻¹² — confirming the enormous mismatch between radiation damping and structural damping.

### Theorem 1 (Rank Collapse): ✅ Correct

The chain-rule argument is mathematically rigorous. The key step — that D_f and D_θ are nonsingular and therefore don't change rank — is correct. The specific computation for R_eq = (a²c)^(1/3) yielding J̃[:,a] = 2·J̃[:,c] is verified numerically to machine precision.

### Theorem 2 (Identifiability Lifting): ✅ Correct (modulo verification at canonical point)

This is an existential proof relying on: (1) σ₃ > 0 at the canonical point (verified: σ₃ = 0.0264), (2) continuity of singular values. The logic is sound. The theorem claims only existence of a non-empty open set, not global or universal results.

### Proposition 3 (Near-Spherical Asymptotics): ❌ NOT VERIFIED

See detailed analysis above. The even-expansion argument (ε → −ε describes the same geometry) is correct in principle. The claim σ₃(0) = 0 follows from Theorem 1 IF the Ritz model reduces to a scalar-reduction model at ε = 0. But the code shows it doesn't — the Ritz model at c/a ≈ 1 is NOT equivalent to the sphere model. The proposition applies to an idealised model family, not to the implemented code.

### Corollary 1 (κ ~ ε⁻²): ❌ NOT VERIFIED

Follows from Proposition 3, which is unverified. Code shows κ plateaus at ~268 near the sphere.

### Proposition 4 (Forward ≠ Inverse): ✅ VERIFIED

E_fwd = 0.0936 < 0.1 while κ_sphere = 1.37 × 10¹⁰. The kernel-direction mechanism is elegant and confirmed: the sphere model has zero sensitivity along v_null while the oblate model has sensitivity 1.10.

---

## Minor Issues

1. **Eq. numbering reference**: The proof of Proposition 4 references the forward error as "Eq. (3.16)" in the proof text (`\eqref{eq:p10_forward_error}`), but I can't verify the numbering without a compiled version. Ensure cross-references are correct.

2. **Breathing mode**: Paper states n = 0 breathing mode near 2490 Hz (background.tex). Code confirms f₀ = 2490.65 Hz. ✓

3. **Bladder volume check**: R = 4.15 cm → V = (4/3)π(0.0415)³ = 299.4 mL ≈ 300 mL. ✓

4. **The oblate Ritz model's 2-DOF limitation**: The source code acknowledges a systematic ~8% offset vs the sphere formula at c/a → 1 (line 393 of oblate_spheroid_ritz.py). This should be mentioned in the paper when the Ritz model is introduced, not left only in code comments.

5. **Step size for finite differences**: The Jacobian uses step_fraction = 1×10⁻⁶ (central differences). For condition numbers of order 10¹⁰, this means the smallest singular value (~10⁻¹⁰) is at the noise floor of double-precision finite differences. The sphere model's σ₃ ≈ 1.4 × 10⁻¹⁰ is consistent with FD noise, not a real singular value. This is actually what one expects (rank-deficient system + FD → noise floor), but it should be noted.

6. **Quadrature**: The Ritz model uses n_quad = 200 Gauss-Legendre points by default. No convergence study is presented. For Legendre polynomials of degree 6, 200 points is likely more than sufficient, but confirming with n_quad = 400 would strengthen the claim.

---

## What's Done Well

1. **Code-paper pipeline**: The scripts are clean, well-commented, and directly generate the figures. Running them from the repo root works without modification. This is better than most papers.

2. **Theorem 1 proof**: Mathematically elegant and verified to machine precision. The chain-rule argument is airtight.

3. **The forward ≠ inverse demonstration**: Proposition 4 is the paper's strongest result. The kernel-direction mechanism (Eq. 3.35) is a clear, verifiable geometric argument.

4. **Honest limitations section**: The paper acknowledges it is theoretical, uses reduced kinematics, and has no experimental validation.

5. **Scaled Jacobian framework**: Using the dimensionless sensitivity matrix rather than the raw Jacobian is the correct choice for identifiability analysis. The scaling is implemented correctly.

---

## Summary of Discrepancies

| Claim | Paper | Code | Status |
|-------|-------|------|--------|
| κ_oblate at canonical | 69.4 | 69.4 | ✅ |
| κ_sphere at canonical | 1.37×10¹⁰ | 1.37×10¹⁰ | ✅ |
| E_fwd | 0.0936 | 0.0936 | ✅ |
| f₂ (abdomen) | 3.95 Hz | 3.95 (sphere) / 3.80 (Ritz) | ⚠️ |
| κ_prolate range | 561–729 | 334–742 | ❌ |
| σ₃(0) = 0 | Stated | σ₃ → 0.007 | ❌ |
| κ ~ ε⁻² near sphere | Stated | κ → 268 (flat) | ❌ |
| J[:,a] = 2·J[:,c] (sphere) | Stated | [2,2,2,2,2] exactly | ✅ |
| Gap ratio | ~2×10⁸ | 1.97×10⁸ | ✅ |
| R_eq watermelon | 0.1453 | 0.1453 | ✅ |

---

## Summary Recommendation: MAJOR REVISION

The paper's strongest results (Theorems 1–2, Proposition 4) are verified and mathematically sound. However, Proposition 3 and Corollary 1 — the near-spherical asymptotic claims — are stated for the Ritz model but **not confirmed by running that model**. The σ₃ floor and κ ceiling near the sphere are real features of the implemented Ritz model, not artefacts. Either:

(a) Restate Proposition 3 for the idealised continuum model (not the Ritz model) and provide independent verification (FEM or higher-order Ritz), or
(b) Remove the ε² scaling claim and report what the Ritz model actually shows: a finite σ₃ floor at ε → 0, which could be attributed to the 2-DOF basis not fully reducing to the sphere limit.

Additionally:
- Correct the prolate κ range or specify the eccentricity interval.
- Clarify which model produces f₂ = 3.95 Hz (it's the sphere model, not the Ritz model). Since the paper argues the sphere model is inadequate, citing its frequency as the canonical result is inconsistent.
- Note the ~10% discrepancy between Ritz and sphere models at c/a = 1 somewhere in the main text.
