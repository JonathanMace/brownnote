# Reviewer B — Round 1 (Paper 3: Scaling Laws)

**Paper:** "Scaling Laws for the Flexural Resonance of Fluid-Filled Viscoelastic Shells: From Rats to Humans"
**Target:** Journal of Sound and Vibration — Short Communication
**Reviewer:** B (technical correctness, internal consistency, logical gaps, fatal flaws)
**Date:** 2026-03-28
**Reviewing commit:** paper3-scaling-laws/main.tex (first draft)

---

## Decision: MAJOR REVISION

---

## Fatal Flaws (paper is unpublishable until fixed)

### F1. Dimensional error in the breathing-mode infrasound-size calculation (Section 5, Abstract)

The function `breathing_mode_infrasound_size` in `src/analytical/dimensional_analysis.py` (line 280) computes:

```python
R_needed = 3 * K_f / (rho_f * omega_target**2)
```

**This has a dimensional error.** The units of the right-hand side are:

$$\frac{[\text{Pa}]}{[\text{kg/m}^3][\text{s}^{-2}]} = \frac{[\text{kg}\,\text{m}^{-1}\,\text{s}^{-2}]}{[\text{kg}\,\text{m}^{-3}\,\text{s}^{-2}]} = \text{m}^2$$

The result has units of m², not m. The correct formula, derived from
$\omega^2 = 3K_f / (\rho_f R^2)$ (the large-$R$ limit where fluid compressibility
dominates shell stiffness and fluid mass dominates wall mass), is:

$$R = \sqrt{\frac{3K_f}{\rho_f\,\omega^2}}$$

**Numerical consequence:** The paper claims (abstract, line 53–54; Section 5, line 259) that f₀ = 20 Hz requires R ≈ 410 m. The correct answer is R ≈ 20 m. I verified this by direct numerical evaluation: `breathing_mode_v2` at R = 20.2 m gives f₀ = 19.74 Hz, while at R = 410 m it gives f₀ = 0.99 Hz.

**Qualitative conclusion survives:** R = 20 m is still absurdly large for any organism, so the statement that "the breathing mode is irrelevant to infrasound for any biological organism" remains correct. But a factor-of-20 error in the key quantitative result of Section 5 is unacceptable — especially in a paper whose central contribution is dimensional analysis.

**This is a dimensional error in a paper about dimensional analysis.** It must be fixed before any consideration of publication.

**Lines affected:** Abstract (line 53–54), Section 5 (lines 258–260), code (`src/analytical/dimensional_analysis.py` line 280), paper's highlight bullet 5 implicitly.

---

## Major Issues (must be addressed)

### M1. The "machine-precision collapse" is a tautology, not a validation

The paper claims (Section 3, lines 176–177) that "the analytical Φₙ reproduces every numerical point to machine precision (maximum relative error 5.8 × 10⁻¹⁶)." Running the code, I obtain a max relative error of 4.28 × 10⁻¹⁶, confirming the claim.

However, this result is **trivially expected by construction** and has zero scientific content. The "numerical" Π₀ is computed by:
1. Evaluating ω² = (K_bend + K_memb + K_pre) / m_eff via `flexural_mode_frequencies_v2`
2. Computing f = ω/(2π), then Π₀ = f·a·√(ρ_f/E)

The "analytical" Φ is computed by:
1. Non-dimensionalising the same K and m expressions with K̃ = K·a/E, m̃ = m/(ρ_f·a)
2. Computing Φ = √(K̃/m̃)/(2π)

These are **algebraically identical transformations of the same formula**. The "collapse" is not validating a physical model or even verifying a non-trivial mathematical result. It is confirming that `f × a × sqrt(rho_f/E)` is the same whether you compute `f` first and multiply, or factor out the dimensional scales first. The residual ~10⁻¹⁶ is IEEE-754 floating-point rounding noise, not a measure of model quality.

The paper must either:
(a) State clearly that this is an algebraic identity check, not an independent validation, or
(b) Compare against a genuinely independent computation (e.g., FEM eigenvalue solver, Ritz variational solution with different trial functions, or experimental data).

As written, the "machine precision" claim misleads the reader into thinking an independent validation has been performed. The physical model was validated (or not) in Paper 1; this paper cannot claim new validation.

### M2. The coupling ratio ℛ = 1/(ka)² is under-defined and inconsistently described

The caption to Table 2 (line 208) defines "ℛ = 1/(ka)² quantifies the radiation-efficiency penalty for airborne excitation." Several problems:

**(a) ℛ is not radiation efficiency.** Radiation efficiency in acoustics is σ_rad = W_rad/(ρcS⟨v²⟩). The quantity 1/(ka)² is more properly described as the inverse squared coupling coefficient for the n = 2 multipole order. Using "radiation-efficiency penalty" conflates two distinct concepts.

**(b) ℛ omits the air–tissue impedance mismatch.** For airborne excitation, the total coupling penalty includes both the multipole order factor (ka)^n *and* the impedance mismatch Z_tissue/Z_air ≈ 3600. The "coupling ratio" as computed (1/(ka)² ≈ 8000–17000) is only the multipole part. The actual displacement ratio for airborne-vs-mechanical excitation is the product of both factors, giving ℛ_total ~ 10⁷. Paper 1 quotes ℛ ~ 6.6 × 10⁴, which includes impedance mismatch. The factor-of-10 discrepancy between papers needs reconciliation.

**(c) ℛ = 1/(ka)^n is mode-dependent**, but this is not stated. For n = 3, ℛ = 1/(ka)³, which is much larger.

**(d) A displacement or force ratio requires specifying both excitation levels.** The paper states (line 226) that ℛ quantifies the ratio, but a ratio of what to what? At what SPL? At what mechanical acceleration? Without specifying the reference excitation, the ratio is not well-defined physically. The code (line 242–243) computes `coupling_ratio = 1/coupling_air` where `coupling_air = ka^n`, confirming this is just the inverse coupling coefficient, not a ratio of measurable displacements.

### M3. The parametric sweep does not actually vary all five Π-groups

The paper claims (line 164–169) that the 486-point sweep spans "physiological ranges of all parameters." Running the code, I find:

| Π-group | Values in sweep |
|---------|----------------|
| h/a | Varies (3 values of h × 3 values of a) |
| c/a | Varies (3 values) |
| ρ_w/ρ_f | **Fixed at 1.078** |
| P_iap/E | Varies (because E varies, P fixed) |
| ν | **Fixed at 0.45** |

Two of the five "governing" input groups (ρ_w/ρ_f and ν) are never varied. The sweep is therefore a **3-parameter** exploration of (h/a, c/a, P/E) with the other two held constant. Yet the paper claims (line 131–132) that six Π-groups govern the problem and that the collapse validates the scaling law. A collapse that holds two of five inputs constant has not demonstrated universality — it has demonstrated that a 3-parameter function is a 3-parameter function.

To validate the full scaling law, the sweep must include at least one variation of ρ_w/ρ_f (e.g., 0.9–1.2, spanning from fat-dominated to muscle-dominated tissue) and ν (e.g., 0.3–0.499). Without this, the claim of "complete dimensional reduction" is overstated.

### M4. Cross-species allometric parameters are unjustified

Table 2 provides predictions for four mammals, citing only Fung (1993) — a general biomechanics textbook — as the source for "allometric estimates of E and a." Examining the code (`ANIMAL_MODELS` dict, line 207–216), each species has 8 assumed parameters (a, c/a, h, E, ρ_w, ρ_f, P_iap, ν). These are:

| Parameter | Rat | Cat | Pig | Human |
|-----------|-----|-----|-----|-------|
| a (cm) | 3 | 8 | 15 | 18 |
| h (mm) | 2 | 4 | 8 | 10 |
| E (kPa) | 50 | 80 | 100 | 100 |
| P_iap (Pa) | 300 | 600 | 800 | 1000 |
| ρ_w (kg/m³) | 1060 | 1070 | 1080 | 1100 |
| ρ_f (kg/m³) | 1020 | 1020 | 1020 | 1020 |
| ν | 0.45 | 0.45 | 0.45 | 0.45 |

**Where do these numbers come from?** Fung (1993) does not provide abdominal wall elastic moduli for rats, cats, and pigs as a function of body mass. These appear to be reasonable guesses, not literature values. The paper must either:
(a) Provide specific literature citations for each species' parameters with stated measurement conditions (in vivo vs ex vivo, strain rate, loading direction), or
(b) Acknowledge that these are assumed values and provide uncertainty bounds.

The claim that "Π₀ is approximately constant (0.065–0.072) across a six-fold range of body size" (lines 220–222) depends entirely on the assumed parameters. If the rat wall modulus were 100 kPa instead of 50 kPa, or the cat wall thickness were 2 mm instead of 4 mm, the constancy would break. The result is only as strong as the weakest input.

### M5. Standalone merit: is this a Short Communication or supplementary material?

The central equation of this paper (Eq. 2, the scaling law) is obtained by algebraic rearrangement of the frequency formula from Paper 1. The Buckingham Pi analysis identifies the dimensionless groups, but these are the obvious choices (thickness ratio, aspect ratio, density ratio, prestress ratio, Poisson's ratio) — any graduate student in fluid-structure interaction would write down the same groups by inspection. The dimensional analysis does not reveal anything surprising.

The cross-species table and breathing-mode impossibility argument have genuine standalone value. But the rest of the paper — the Π-group identification, the parametric collapse, the scaling-law derivation — is straightforward algebra that would naturally appear as a subsection of Paper 1 or as supplementary material.

For JSV Short Communication standards, the paper needs to clearly articulate what **new physical insight** it provides that could not have been included in Paper 1. As a structural suggestion: if the cross-species predictions were validated against even one experimental data point (e.g., measured abdominal resonance in a pig or rat model), this would immediately justify standalone publication.

---

## Minor Issues (should be addressed)

### m1. Inconsistent parameter count language

The abstract (line 39) says "eleven physical parameters," which matches the variable list (including f_n as output). But the Buckingham Pi count in the Introduction (line 69–71) lists 10 input parameters plus 3 fundamental dimensions, giving "11 − 3 = 8" groups (line 101–102). This is correct only if f_n is counted among the 11 variables. The text should clarify that the 11 includes the output variable f_n, as Buckingham Pi requires.

### m2. Section 5 title is imprecise

The section title "The breathing mode is always ultrasonic" is incorrect for small animals. For a rat (R ~ 2.6 cm), f₀ ≈ 2490 × (15.7cm / 2.6cm) ≈ 15 kHz — within the audible range for rats (up to ~76 kHz). The correct statement is "the breathing mode is always far above the infrasonic range." (Reviewer A also flagged this.)

### m3. λ_n is referenced but not defined in the paper

Equation (7) uses λ_n ("the membrane mode-shape factor") without providing its formula. The expression λ_n = (n² + n − 2 + 2ν)/(n² + n + 1 − ν) is in the code (line 113 of `dimensional_analysis.py`) and in Paper 1, but a Short Communication should be self-contained. (Reviewer A also flagged this.)

### m4. Highlight 2 overclaims

"486-point parametric study collapses to machine precision" — as discussed in M1, this is algebraic identity, not physical validation. The highlight should be rephrased to reflect this.

### m5. The paper text (line 132) says "six" Π-groups govern flexural modes

Six = five inputs + one output. This counting is correct but the language "six govern" is ambiguous. Better: "the dimensionless frequency Π₀ is a function of five input groups."

### m6. Inconsistency between Eq. (2) and Eq. (5)

Equation (2) writes f_n = (1/2π)√(E/ρ_f) (1/a) Φ_n(...). Equation (5) writes Φ_n = (1/2π)√(K̃/m̃) · a√(ρ_f/E). The (1/2π) factor appears in both. Substituting Eq. (5) into Eq. (2) gives f_n = (1/2π)² √(E/ρ_f)(1/a) √(K̃/m̃) a√(ρ_f/E) = (1/2π)² √(K̃/m̃), which has a spurious (2π)² factor. One of these equations has an inconsistent definition of Φ_n. The code (`phi_analytical`, line 125) returns `sqrt(K_tilde/m_tilde) / (2*pi)`, which is Eq. (5). For Eq. (2) to be consistent, it should either drop the 1/(2π) prefactor, or Φ_n should be defined without the 1/(2π).

### m7. Table 2 values are rounded inconsistently

The code outputs Π₀ = 0.0673 (rat), 0.0646 (cat), 0.0686 (pig), 0.0717 (human). The paper rounds these to 0.067, 0.065, 0.069, 0.072. The cat value rounds from 0.0646 to 0.065 (correct) but the human rounds from 0.0717 to 0.072 (should be 0.072 at 3sf, but at 2sf is 0.072). This is acceptable, but I note that 0.065 vs 0.072 looks like a 10% variation in a quantity claimed to be "approximately constant." The paper should state what "approximately constant" means quantitatively (e.g., coefficient of variation = X%).

### m8. The "Data availability" URL points to "brownnote" not "browntone"

Line 284: `https://github.com/JonathanMace/brownnote`. The repository is apparently named "browntone" based on the working directory. Minor, but should be verified.

### m9. Only 9 references

For JSV, even a Short Communication typically carries 15–25 references. Key omissions identified by Reviewer A (Warburton 1976, Abramson 1966, West et al. 1997 for allometry) should be addressed.

---

## Positive Comments

1. **The breathing-mode impossibility result is elegant and conclusive** (once the numerical value is corrected). The qualitative argument — that f₀ scales as 1/R and would require R ~ 20 m to reach 20 Hz — is a genuinely useful result that closes an entire line of inquiry.

2. **The cross-species table is immediately practical.** Experimentalists designing animal studies of whole-body vibration could use these predictions directly. This is the paper's strongest claim to standalone value.

3. **Parameter consistency with Paper 1 is good.** The human model parameters (a = 0.18 m, c/a = 0.67, h = 0.01 m, E = 0.1 MPa, ν = 0.45, ρ_w = 1100, ρ_f = 1020, K_f = 2.2 GPa, P_iap = 1000 Pa) match Paper 1's Table 1 exactly. The v2 code defaults are consistent. Earlier v1 defaults (a = 0.15, E = 0.5 MPa) represent an older parameter set that has been superseded.

4. **The code is well-structured and readable.** The `phi_analytical` function clearly mirrors the dimensional stiffness expressions, making the non-dimensionalisation auditable.

5. **The writing is clear and appropriately concise** for a Short Communication. The three-panel Figure 1 concept is effective.

---

## Summary

The paper applies Buckingham Pi analysis to a known frequency formula and draws cross-species conclusions. The dimensional analysis itself is trivially correct but the paper oversells the algebraic identity as "validation." Three substantive issues prevent publication:

1. **A dimensional error in the headline result of Section 5** (Fatal Flaw F1). R ≈ 20 m, not 410 m. Fix is trivial but embarrassing.
2. **The machine-precision collapse is tautological** (Major M1). Must be honestly described.
3. **Allometric inputs are unvalidated** (Major M4). Without literature citations or uncertainty bounds, the cross-species predictions are speculative.

Additionally, the coupling ratio definition needs tightening (M2), the parametric sweep is incomplete (M3), and the standalone merit needs clearer justification (M5).

With corrections, this could become an acceptable Short Communication. The cross-species predictions and breathing-mode impossibility argument have genuine value. But the current draft contains a fatal dimensional error and several instances of overclaiming that make it unsuitable for publication.

**Recommendation: MAJOR REVISION**
