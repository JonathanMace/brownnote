# Reviewer B — Round 1 (Bladder Resonance Paper)

**Paper:** "Resonant Frequencies of the Human Urinary Bladder: A Fluid-Filled Viscoelastic Shell Model"
**Reviewer:** B (Technical correctness, internal consistency, logical gaps)
**Date:** 2025-07-09

---

## Decision: MAJOR REVISION (bordering REJECT)

The paper applies a known fluid-filled shell formulation (Lamb 1882, Junger & Feit) to the urinary bladder with fill-volume-dependent parameters. The physics framework is sound in principle, but I identify **two fatal flaws** (F1, F2), **seven major issues** (M1–M7), and **nine minor issues** (m1–m9) that collectively undermine the quantitative claims. The paper cannot be published in its present form.

---

## Fatal Flaws (paper is unpublishable until fixed)

### F1. Shear Modulus / Young's Modulus Confusion — Material Parameter Error

The introduction (lines 38–39, `introduction.tex`) correctly identifies the Nenadic et al. (2013) data as **shear moduli** (μ₁ = 9.6–48.7 kPa). The `references.bib` (line 61) also labels these as "μ₁". However, the elastic modulus model (Eq. 6, `theory.tex` lines 72–78; `bladder_model.py` lines 79–82) uses E_min = 10 kPa, which is numerically equal to the **lowest shear modulus**, not the Young's modulus.

For nearly incompressible tissue (ν = 0.49):

$$E = 2(1+\nu)\mu \approx 2.98\mu$$

Therefore:
- Nenadic μ₁ = 9.6 kPa at 187 mL → **E ≈ 28.6 kPa** (not 10 kPa)
- Nenadic μ₁ = 48.7 kPa at 267 mL → **E ≈ 145 kPa** (not ~53 kPa from model)

The paper also cites Barnes (2016) who reports E directly at 10 kPa "at rest" — but "rest" likely means zero stretch (excised tissue), not the 50 mL fill state where the bladder is already distended. These two sources are conflated without proper conversion or reconciliation.

**Impact:** If E_min is corrected from 10 kPa to ~30 kPa, the f₂ minimum shifts from 12.0 Hz at 170 mL to **13.9 Hz at 220 mL** — a 16% change in frequency and a 29% shift in the critical volume. The entire quantitative narrative of the paper changes. I verified this computationally.

**Required action:** Clearly distinguish shear modulus from Young's modulus throughout. Apply E = 2(1+ν)μ when converting vibrometry data. Re-derive E(V) bounds using properly converted values. Recompute all results.

### F2. Thin-Shell Assumption Violated at Low Fill Volumes

The paper checks h/R only at 300 mL (`theory.tex` line 17: "h/R ≈ 0.04"), where indeed the thin-shell criterion holds. But the model is applied from **50 mL**, where I compute:

| Volume (mL) | h/R   | Thin-shell valid? |
|-------------|-------|-------------------|
| 50          | 0.219 | **NO** — grossly violated |
| 100         | 0.120 | **NO** — marginal at best |
| 150         | 0.083 | Borderline |
| 200         | 0.063 | Acceptable |
| 300         | 0.043 | Good |
| 500         | 0.030 | Good |

At h/R = 0.22, Love–Kirchhoff thin-shell theory is completely inapplicable. Shear deformation and rotatory inertia (Mindlin–Reissner effects) become significant. The 16.2 Hz value at 50 mL in Table 2 is unreliable, and results below ~150 mL should be treated with extreme caution.

**Required action:** Either (a) restrict the analysis to V ≥ 150–200 mL where h/R < 0.1, or (b) implement a thick-shell correction (e.g., Naghdi-type) and quantify the error, or (c) at minimum, clearly state the domain of validity and flag low-fill results as unreliable.

---

## Major Issues (must be addressed)

### M1. Numerical Error in Breathing Mode Section

`theory.tex` lines 128–131 state:

> "k_fluid ≈ 1.6 × 10¹¹ Pa/m while k_shell ≈ 2.2 × 10⁴ Pa/m — a ratio exceeding 10⁶"

I recompute at 300 mL (E = 52.8 kPa, h = 1.79 mm, R = 41.5 mm, ν = 0.49):

$$k_\text{shell} = \frac{2Eh}{R^2(1-\nu)} = \frac{2 \times 52800 \times 0.00179}{0.0415^2 \times 0.51} = 2.15 \times 10^5 \text{ Pa/m}$$

The paper says 2.2 × 10⁴ — **off by an order of magnitude** (should be ~2.2 × 10⁵). The ratio k_fluid/k_shell ≈ 7.4 × 10⁵, which does **not** exceed 10⁶ as claimed. The breathing mode frequency (~9,500 Hz) is still correct because it is overwhelmingly dominated by k_fluid, but the stated numerical values are wrong.

**Required action:** Correct k_shell to ~2.2 × 10⁵ Pa/m and the ratio to ~7 × 10⁵.

### M2. Boundary Conditions: Free Shell is Physically Unjustified

The model treats the bladder as a **free spherical shell**, but anatomically:
- The trigone (base) is attached to the pelvic bone via ligaments
- Two ureters and one urethra penetrate the wall
- ~40% of the bladder surface contacts the pelvic floor (acknowledged in `discussion.tex` line 87)

The paper states (`discussion.tex` line 88–89):

> "A partial rigid boundary would modify the effective mode shapes and **could lower** the resonant frequency by restricting the free surface area."

This is physically **incorrect**. Adding constraints to a vibrating structure **raises** natural frequencies — this is a theorem (Rayleigh's principle / min-max theorem). Clamping part of the surface removes degrees of freedom and increases the stiffness-to-mass ratio. The only exception would be if the boundary condition fundamentally changes the mode type (e.g., from a symmetric to an asymmetric mode), which requires specific justification that is not provided.

If the free-shell model overestimates the vibrating surface area, it **underestimates** the frequency. The paper's conclusion that f₂ = 12–18 Hz may therefore be a **lower** bound, not an "upper bound" as the paper suggests in `discussion.tex` line 111.

**Required action:** Correct the physical claim. State clearly whether the free-shell result is a lower or upper bound, and justify the choice.

### M3. Coupling Ratio is Dimensionally Inconsistent

Equation (16) (`theory.tex` line 233):

$$\mathcal{R} = \frac{T(f_2) \times H(f_2)}{(ka)^2} \approx 7{,}600$$

This ratio divides:
- **Numerator:** dimensionless transfer function chain (seat displacement → pelvis displacement → bladder wall displacement)
- **Denominator:** (ka)², the n=2 multipole coefficient of a plane-wave expansion

These quantities have **different physical inputs**: the numerator takes a mechanical displacement as input, while the denominator takes a pressure field. The ratio as defined does not answer the question "how many times larger is the bladder wall displacement from mechanical vs. airborne excitation at the same source strength?" — because "same source strength" is undefined for two different input types.

A proper comparison would require expressing both pathways in terms of the **same** physical quantity at the bladder wall (e.g., wall displacement per unit acceleration, or wall displacement per unit energy input).

**Required action:** Redefine the coupling ratio with consistent input normalization, or explicitly state the assumptions and limitations of this order-of-magnitude comparison.

### M4. Abdominal Coupling Ratio Inconsistency Between Papers

Table 3 (`results.tex` line 147) states the abdominal coupling ratio is ~66,000, citing the companion paper. Using the **same** coupling formula (Eq. 16) with the Paper 1 canonical parameters (R = 15.7 cm, f₂ = 3.95 Hz, Q = 4.0), I compute:

- ka = 0.0114, (ka)² = 1.30 × 10⁻⁴
- T_pelvis(3.95 Hz) = 1.76
- Coupling ratio = 1.76 × 4.0 / 1.30 × 10⁻⁴ = **54,400**

This is 17% below the claimed 66,000. If Paper 1 uses a different coupling calculation, this needs to be reconciled. If both papers use the same formula, one of them is wrong.

**Required action:** Verify consistency of coupling ratio calculation between the two papers.

### M5. Salami-Slicing Concern

The core analysis applies **identical equations** (Lamb flexural modes on a pressurized fluid-filled sphere) with different parameter substitutions. The mathematical formulation section (Section 2) is almost entirely borrowed from Paper 1. The only genuinely new content is:
1. The fill-volume-dependent parameter model (Eqs. 3–8, ~1 page)
2. The U-shaped frequency curve and minimum analysis (~1 page of results)
3. Clinical context for WBV-induced urgency

The coupling analysis (Section 2.5–2.6) is a trivial adaptation. The comparison table (Table 3) could be a single table in Paper 1. A dedicated JSV paper requires substantially more novelty than parameter substitution.

**Required action:** Either (a) fold this analysis into Paper 1 as a section/application, or (b) substantially expand the bladder-specific contributions — e.g., FEM validation of the spherical approximation, thick-shell correction, parametric Monte Carlo analysis, or experimental comparison with bladder vibrometry data.

### M6. E(V) Model is Under-Constrained

The log-linear E(V) interpolation (Eq. 6) is calibrated to two anchor points: E_min at V_min and E_max at V_max. The Nenadic data provide only **two measurements** (at 187 mL and 267 mL), and the Barnes data are from excised tissue at arbitrary stretch states. The choice of an exponential form vs. polynomial, sigmoid, or piecewise-linear is entirely **ad hoc** with no physical or statistical justification. Different functional forms could shift the location of the f₂ minimum substantially.

**Required action:** (a) Show that the f₂ minimum location is robust to the choice of E(V) interpolation (e.g., test linear, quadratic, sigmoid). (b) Provide error bars on the anchor points. (c) The sensitivity analysis (if it existed in the paper) should vary the **functional form**, not just the endpoints.

### M7. Sensitivity Analysis is Absent from the Paper

The code (`bladder_model.py` lines 266–363) implements a tornado sensitivity analysis and minimum-shift analysis, but **neither appears in the manuscript**. The paper makes precise claims (f₂ = 12–18 Hz, minimum at ~170 mL, coupling ratio ~7,600) without any uncertainty quantification. Furthermore, the sensitivity code has a bug: the E_scale lower bound is 0.01e6/10e3 = 1.0, which produces **zero perturbation** from baseline, making the E sensitivity one-sided.

**Required action:** Include the sensitivity analysis in the paper. Fix the E_scale bug. Report confidence intervals on all key claims.

---

## Minor Issues (should be addressed)

### m1. Scaling Claim is Incorrect
`results.tex` lines 155–157: "the stiffness-to-mass ratio scales roughly as 1/R²." For membrane-dominated modes with constant E and h, f ∝ R⁻³/². With h(V) from tissue conservation (h ∝ R⁻²), f ∝ R⁻⁵/². Neither is "roughly 1/R²." State the correct scaling or remove the claim.

### m2. h(V) Floor Violates Tissue Conservation
The 1.5 mm floor on wall thickness (`bladder_model.py` line 67) activates at ~400 mL, at which point the constant-tissue-volume assumption is violated by 16% at 500 mL. This artificial discontinuity in dh/dV could affect the stiffness derivative analysis. Either justify the floor physically or remove it and let tissue conservation hold to arbitrary thinness.

### m3. Mode Degeneracy Not Discussed
The n=2 mode on a perfect sphere is 5-fold degenerate (2n+1 = 5). Real bladder geometry (irregular, non-spherical, partially constrained) would split these into distinct frequencies. The paper presents a single f₂ value without acknowledging the splitting.

### m4. "170 mL ≈ Early Need-to-Go" is Unsourced
`results.tex` line 34: "a fill state corresponding to the early 'need to go' sensation in most individuals." No reference is provided. The clinical literature generally places first desire to void at 150–250 mL, but this varies enormously. Source it or soften the claim.

### m5. Loss Tangent Approximation
With η = 0.4, the approximation ζ = η/2 and Q = 1/η carries ~7% error compared to the exact Kelvin–Voigt result Q = √(1+η²)/η = 2.69 vs. 2.50. This is acceptable for the precision of the model but should be noted.

### m6. Intravesical Pressure Model
The quadratic P(V) (Eq. 8) is a rough fit to the cystometric curve. Real cystometry data show a compliance phase (nearly flat ~5–10 cmH₂O) to ~300 mL, then a steep exponential rise. A quadratic underestimates pressure at high fill and overestimates it at moderate fill. This affects K_P.

### m7. Akkus (2014) Reference May Be Incorrect
`references.bib` line 89: PLoS ONE article ID e157818 with volume 9, year 2014. PLoS ONE article IDs in 2014 were 5-digit (e.g., e105XXX), not 6-digit. Verify this citation.

### m8. ν = 0.49 vs. 0.45 (Cross-Paper Consistency)
Paper 1 (abdominal model) uses ν = 0.45; Paper 2 uses ν = 0.49. Both are described as "soft tissue." The choice of ν = 0.49 is defensible for nearly-incompressible detrusor muscle, but the difference should be explicitly justified rather than silently changed.

### m9. Sub-Resonant Forced Response Deserves Quantification
The discussion (`discussion.tex` lines 15–22) correctly identifies that at 4–8 Hz the bladder responds sub-resonantly. At 5.5 Hz (pelvic resonance peak), I compute T_pelvis × H_bladder = 2.24 × 1.18 = 2.64, which is **larger** than the T × H = 0.78 product at f₂ = 13.4 Hz. This means the bladder is **more** effectively driven at pelvic resonance frequencies than at its own resonance. This critical finding is buried in qualitative discussion — it should be quantified and foregrounded.

---

## Positive Comments

1. **Sound physical framework.** The Lamb-type flexural mode analysis for a fluid-filled shell is well-established and correctly implemented (equations verified against code, code verified against hand calculations). The computed frequencies are internally consistent.

2. **Fill-dependent parametric analysis is a genuine contribution.** The U-shaped f₂(V) curve and the identification of a frequency minimum from competing geometric softening and strain-stiffening is physically insightful and non-trivial.

3. **Honest limitations section.** The paper acknowledges five significant limitations (`discussion.tex` lines 77–112), including the pelvic constraint, layered wall, and surrounding tissue. This is commendable, though the analysis of boundary condition effects (M2) is incorrect.

4. **Code-paper consistency.** With the exception of the k_shell error (M1), all numerical values in the tables match the code output exactly. The code is well-structured and reproducible.

5. **Clinically relevant question.** The connection between WBV and bladder urgency is genuinely under-studied and deserves first-principles analysis.

---

## Summary

This paper poses a good question and uses a reasonable (if borrowed) analytical framework, but it has two fatal flaws that make the quantitative results unreliable: the shear-modulus/Young's-modulus confusion (F1) and the thin-shell violation at low fill (F2). Beyond these, the boundary condition analysis contains a physics error (M2), the coupling ratio is dimensionally inconsistent (M3), a numerical value is wrong by 10× (M1), and no uncertainty analysis appears in the manuscript (M7). The paper also raises a salami-slicing concern (M5) that the editors should weigh.

If the authors correct F1 and F2, address M1–M7, and substantially expand the bladder-specific contributions to justify a standalone paper, I would consider this for re-review. In its present form, it is not suitable for publication in JSV.

---

*Reviewer B, Round 1*
