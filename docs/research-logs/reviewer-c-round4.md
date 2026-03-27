# Reviewer C — Round 4

**Paper:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the Brown Note"

**Reviewer focus:** Reproducibility, numerical rigour, uncertainty quantification, code–paper consistency.

---

## Overall Assessment

This is an inventive and well-structured paper that applies fluid-filled shell theory to a colourful question. The underlying physics is sound, the code is well-organised, and the central qualitative conclusion — that airborne infrasound couples far more weakly than mechanical vibration — is robust. However, I have identified **several quantitative inconsistencies between the paper text, the tables, and the code output** that collectively undermine confidence in the reported numbers. Some of these are parameter mismatches between different sections of the paper; others are methodological inconsistencies in how displacement is computed across different tables. These must be resolved before the paper can be considered reproducible.

---

## Code Verification Results (show my work!)

### 1. Natural Frequencies (Table 2, Section 2.3)

Using the **canonical parameters from Table 1** (`E=0.1 MPa, a=0.18 m, c=0.12 m, h=0.01 m, ν=0.45, ρ_w=1100, ρ_f=1020`):

| Mode | Code Output (Hz) | Paper Claim (Hz) | Match? |
|------|:---:|:---:|:---:|
| n=0 (breathing) | **2491** | ~2900 (Eq. 9), ~2500 (abstract) | ✗ — Off by 16% from Eq. 9 |
| n=2 | **3.95** | 4.0 | ✓ (rounding) |
| n=3 | **6.31** | 6.3 | ✓ |
| n=4 | **8.88** | 8.9 | ✓ |

**Issue B-1:** The breathing mode frequency is quoted as "approximately 2900 Hz" in Eq. (9) but the code computes **2491 Hz** for the canonical parameters. The abstract and conclusion say "approximately 2500 Hz" — so even within the paper, the breathing mode is given as two different values (2500 vs 2900). The code agrees with 2491 ≈ 2500, not 2900. The `≈2900` in Eq. (9) may be from an earlier parameter set.

**Table 2 (E sweep):** All six rows match the code to within rounding. ✓

### 2. Loss Tangent / Q-Factor Inconsistency

**Issue M-1 (MAJOR):** The paper uses **two different values of the loss tangent** without acknowledgement:

| Location | η | Q = 1/η | ζ = η/2 |
|----------|:---:|:---:|:---:|
| **Table 1** (baseline parameters) | 0.25 | 4.0 | 0.125 |
| **Section 2, line 71–72** (text) | 0.30 | 3.3 | 0.15 |
| **Tables 5–6 header** | — | **4.0** | 0.125 |
| **Discussion §5.1, line 38** | — | — | **0.15** |
| **Code default** (`AbdominalModelV2`) | 0.30 | 3.3 | 0.15 |
| **UQ nominal** (`uncertainty_quantification.py` line 73) | 0.25 | 4.0 | 0.125 |

Table 1 says η = 0.25 but the very next page says "The baseline value η = 0.30 (Q = 3.3) represents a central estimate." These cannot both be the baseline. Tables 5–6 use Q = 4.0, consistent with η = 0.25. The Discussion uses ζ = 0.15, consistent with η = 0.30. The code defaults to η = 0.30 but the UQ and the scripts that generate Table 5/6 use η = 0.25. **This is confusing and needs to be resolved into a single consistent baseline.**

### 3. Airborne Displacement (Table 5)

Using canonical parameters with η = 0.25 (Q = 4.0), as implied by Table 5 header:

| SPL (dB) | Code ξ_energy (μm) | Paper ξ_energy | Code ξ_pressure (μm) | Paper ξ_pressure |
|:---:|:---:|:---:|:---:|:---:|
| 100 | 0.0014 | 0.001 | 0.018 | 0.018 | 
| 110 | 0.0043 | 0.004 | 0.058 | 0.058 |
| 120 | **0.0137** | **0.014** | **0.184** | **0.18** |
| 130 | 0.0435 | 0.044 | 0.583 | 0.58 |
| 140 | 0.1374 | 0.14 | 1.844 | 1.84 |

Table 5 matches the code output closely. ✓ (Rounding only.)

**However:** The abstract says "wall displacements of order 0.01 μm at 120 dB SPL" (energy-consistent = 0.014 μm, OK). Section 2.4 (Eq. 14) says "ξ_air ≈ 0.14 μm for n=2" — this is the **pressure-based** value, not the energy-consistent value. The Discussion (line 72) repeats "0.14 μm." **The paper switches between energy-consistent and pressure-based values without consistent labelling**, differing by a factor of 13.4×.

### 4. Mechanical Coupling (Table 6)

**Issue M-2 (MAJOR):** Table 6 values **cannot be reproduced from the code using the formula stated in the paper**.

Paper Eq. (20) explicitly states:
$$x_{\text{base}} = \frac{a_{\text{rms}} \sqrt{2}}{\omega^2}$$

But the Table 6 values are computed **without the √2 factor**:

| a_rms (m/s²) | Paper x_base (μm) | Code with √2 (μm) | Code without √2 (μm) |
|:---:|:---:|:---:|:---:|
| 0.1 | **162** | 229 | **162** ✓ |
| 0.5 | **811** | 1147 | **811** ✓ |
| 1.15 | **1865** | 2637 | **1865** ✓ |

Table 6 uses `x_base = a_rms / ω²`, omitting the √2, while Eq. (20) says `x_base = a_rms√2 / ω²`. The code (`WBVExposure.displacement_amplitude_m`) includes √2. So **Table 6 contradicts both the equation and the code**. The relative displacement column (x_rel = x_base × H_rel with H_rel = 4 at resonance) is internally self-consistent with the "wrong" x_base, so the error propagates: the paper's x_rel values are a factor of √2 too small.

This means the **actual** predicted mechanical displacement at the EU limit (1.15 m/s²) is ~10,500 μm, not 7,459 μm as stated.

### 5. ka Value and Section 2.4

**Issue m-1:** Section 2.4 quotes `ka ≈ 0.017` "at 7 Hz," yielding `(ka)² ≈ 2.8 × 10⁻⁴`. Running the code:

- With **canonical parameters** (R = 0.157 m): `ka` at 7 Hz = **0.0202**, at f₂ = 3.95 Hz = **0.0114**.
- With **code default parameters** (R = 0.131 m): `ka` at 7 Hz = **0.0168** ≈ 0.017. ✓

The `ka = 0.017` comes from the code's default model (a = 0.15 m, c = 0.10 m), **not** from the canonical model in Table 1 (a = 0.18 m, c = 0.12 m). Section 2.4 evaluates `ka` at 7 Hz, which is not even the predicted f₂ for those parameters. The canonical model gives ka² = 1.3 × 10⁻⁴ at f₂, not 2.8 × 10⁻⁴. **The (ka)² penalty used in the formulation section is numerically wrong for the canonical model.**

### 6. Discussion Section Values

**Issue m-2:** Discussion §5.2 (line 65) states "The flexural n = 2 mode at 4.4 Hz (for E = 0.1 MPa, relaxed musculature)." The code gives **f₂ = 3.95 Hz** for E = 0.1 MPa with canonical geometry. The value 4.4 Hz appears nowhere in the code output; this may be a stale number from an earlier model version.

### 7. Table 7 (Pathway Summary)

Table 7 reports WBV displacement at 0.5 m/s² = **3,115 μm** and at 1.15 m/s² = **7,165 μm**. These match neither:
- Table 6 values (3,243 / 7,459 μm, no √2)
- Code with √2 (4,586 / 10,549 μm)

The ratio x_rel/x_base ≈ 3.84, which corresponds to neither Q = 4.0 (H = 4.0) nor Q = 3.3 (H = 3.33). **Table 7 appears to come from yet another model parameterisation** and its provenance cannot be determined from the paper or code.

The airborne cavity resonance entry in Table 7 is **0.14 μm** (pressure-based), while Table 5 says the energy-consistent value is 0.014 μm. The coupling ratio in Eq. (24) then uses 649/0.014 = 4.6 × 10⁴, **mixing the mechanical value from one method with the airborne value from another**. If the pressure-based airborne value (0.18 μm) were used consistently with the √2-correct mechanical value (917 μm at 0.1 m/s²), the coupling ratio would be 917/0.18 ≈ 5,100 — still large, but 9× smaller than claimed.

### 8. Oblate Ritz Correction (Table 4)

| Mode | Paper Sphere | Paper Ritz | Code Sphere | Code Ritz | Match? |
|------|:---:|:---:|:---:|:---:|:---:|
| n=2 (E=0.1) | 4.0 | 3.6 | 4.0 | **3.8** | ✗ |
| n=3 (E=0.1) | 6.3 | 5.6 | 6.3 | **5.8** | ✗ |
| n=4 (E=0.1) | 8.9 | 8.0 | 8.9 | **8.1** | ✗ |
| n=2 (E=0.5) | 7.1 | 6.0 | 7.1 | **6.2** | ✗ |
| n=3 (E=0.5) | 11.3 | 9.5 | 10.0 | **8.5** | ✗ |
| n=4 (E=0.5) | 14.4 | 12.9 | 12.9 | **11.3** | ✗ |

The Ritz values in the paper do not match the current code for any mode. At E = 0.5 MPa, even the **sphere** values differ (paper says 11.3 and 14.4 for n=3,4; code gives 10.0 and 12.9). This suggests Table 4 was generated with different parameters or a different code version and was never re-generated after the canonical parameters were finalised.

### 9. SPL for PIEZO Threshold

- Conclusion says "approximately 158 dB" — computed from energy-consistent approach: 120 + 20log₁₀(1/0.014) = 157.1 dB. ✓
- Discussion says "approximately 137 dB" — computed from pressure-based: 120 + 20log₁₀(1/0.184) ≈ 134.7 dB. ✗ (should be ~135, not 137)
- UQ Table 3 says median = 135 dB (pressure-based). ✓ for pressure-based approach.

**These are three different answers (135, 137, 158 dB) for the same question in the same paper.** The 23 dB difference between the energy-consistent and pressure-based estimates is enormous (×14 in pressure!).

### 10. UQ Results (Table 3)

Comparing saved `uq_results.json` to Paper Table 3:

| Quantity | JSON median | Paper median | JSON 90% CI | Paper 90% CI | Match? |
|----------|:---:|:---:|:---:|:---:|:---:|
| f₂ (Hz) | **6.4** | **7.5** | [3.3, 15.5] | [3.3, 15.5] | ✗ median |
| ξ_air (μm) | **0.178** | **0.07** | [0.108, 0.394] | [0.01, 0.4] | ✗ both |
| ξ_mech (μm) | **1818** | **600** | [296, 8176] | [100, 3000] | ✗ both |
| R_coupling | **9,820** | **10⁴** | [1780, 34169] | [10³, 10⁵] | ~✓ (order) |
| SPL PIEZO (dB) | **135.0** | **135** | [128.1, 139.4] | [128, 139] | ✓ |

**Issue M-3 (MAJOR):** The f₂ median in the JSON is 6.4 Hz but the paper claims 7.5 Hz. The ξ_air median from JSON is 0.178 μm (pressure-based) but the paper claims 0.07 μm (which matches neither energy-consistent nor pressure-based). The ξ_mech median from JSON is 1818 μm but the paper claims 600 μm (3× discrepancy). **Paper Table 3 does not match the saved computational results.** Either the table was manually edited, or it was generated from a different code version and not updated.

---

## Reproducibility Issues

### R-1. Code defaults ≠ Paper canonical parameters
The `AbdominalModelV2` class defaults (`E=0.5 MPa, a=0.15, c=0.10, h=0.015, ν=0.49, ρ_w=1050, ρ_f=1040, η=0.30`) differ from Table 1 canonical values (`E=0.1 MPa, a=0.18, c=0.12, h=0.01, ν=0.45, ρ_w=1100, ρ_f=1020, η=0.25`). This means anyone running the code with `AbdominalModelV2()` will get **completely different** numbers from the paper. There is no single function call that produces the paper's baseline. The scripts that generate paper results override the defaults, but this is fragile and error-prone. **Recommendation:** Either change the class defaults to match Table 1, or provide a `canonical_model()` factory function.

### R-2. No single entry point reproduces all tables
There is no script that generates Tables 2–7 from a single run. Each table appears to have been generated from different scripts with slightly different parameters. A `reproduce_paper.py` script would be extremely valuable.

### R-3. Figure 3 not reproducible from text alone
The paper references Figure 3 (frequency vs. E) but does not specify the solver settings, quadrature order, or random seed. The figure is generated by `parametric_analysis.py` but relies on specific parameter sweeps that are only documented in the code, not the paper.

---

## Uncertainty and Statistical Rigour

### U-1. Partial UQ creates false confidence
Monte Carlo UQ was performed for f₂ and the results are propagated to ξ_air, ξ_mech, and the coupling ratio. This is good. However:

- **The energy-consistent displacement was NOT propagated through UQ.** The UQ code uses `flexural_mode_pressure_response` (pressure-based), not `self_consistent_displacement` (energy-consistent). Since the paper's "primary" result (abstract, conclusion) uses the energy-consistent value, but the UQ uses the pressure-based value, the uncertainty intervals in Table 3 **do not apply to the quantity reported in the abstract**. This is exactly the kind of partial UQ that gives false confidence.

- The UQ mechanical displacement uses `a_rms√2/ω²` (code with √2), but Table 6 uses `a_rms/ω²` (no √2). So the UQ's ξ_mech distribution is √2 larger than what Table 6 implies. The 90% CI reported in Table 3 for ξ_mech is based on the √2 version.

### U-2. Sobol indices: convergence not verified
The paper reports Sobol indices with N_base = 4096, giving 4096 × (2×9 + 2) = 81,920 evaluations. This is generally adequate for 9 parameters, but **no convergence study is shown**. The standard approach is to double N_base and check that indices change by <5%. Given the log-normal distribution of E (which introduces heavy tails), convergence should be explicitly demonstrated.

### U-3. 10,000 MC samples
For a 9-dimensional input space with a heavy-tailed (log-normal) parameter, 10k samples is marginal. The 90% CI appears stable (JSON matches paper for f₂ bounds despite median discrepancy), but the tails of the coupling ratio distribution (which involves ratios of random variables) may not be well-resolved. A brief convergence check (e.g., bootstrap CI of the CI bounds) would strengthen the claim.

### U-4. No UQ on oblate Ritz correction
The 11–20% correction from the oblate Ritz analysis is presented as a point estimate. No uncertainty is propagated through this correction. Since it shifts f₂ from 4.0 to 3.6 Hz (10%), which is comparable to the 90% CI lower bound of 3.3 Hz, this correction is clearly important relative to the parameter uncertainty and should be included in the Monte Carlo.

### U-5. No UQ on nonlinear reduction
The nonlinear analysis predicts a 27% reduction in displacement at large amplitudes (mentioned in discussion). This correction is not applied to the mechanical coupling estimates in Tables 6–7, nor is it propagated through the UQ. For the airborne pathway (where displacements are sub-micrometre), nonlinearity is irrelevant. But for the mechanical pathway, the linear model overestimates displacement by ~27%, and this is nowhere reflected in the uncertainty intervals.

---

## Major Issues

### M-1. Loss tangent inconsistency (η = 0.25 vs 0.30)
Table 1 and Tables 5–6 use η = 0.25 (Q = 4). Section 2 text and the code default use η = 0.30 (Q = 3.3). The Discussion uses ζ = 0.15 (η = 0.30). Pick one. This affects every displacement value by 20%.

### M-2. Table 6 contradicts Eq. (20)
The √2 factor is missing from Table 6. Either the equation or the table is wrong. The mechanical displacement values in the paper are understated by √2 ≈ 41%.

### M-3. UQ results (Table 3) do not match saved JSON
The f₂ median (6.4 vs 7.5 Hz), ξ_air median (0.178 vs 0.07 μm), and ξ_mech median (1818 vs 600 μm) all differ substantially. The paper Table 3 appears to have been manually curated or generated from an earlier code version.

### M-4. Energy-consistent vs pressure-based values used interchangeably
The paper reports displacement as 0.014 μm (energy), 0.14 μm (Eq. 14 pressure-based), and 0.18 μm (Table 5 pressure-based) at 120 dB — three different values for the same physical quantity. The coupling ratio (Eq. 24) uses the energy-consistent airborne value but the no-√2 mechanical value, cherry-picking the combination that maximises the ratio. The SPL threshold for PIEZO is reported as 135 dB (pressure-based, UQ), 137 dB (discussion), and 158 dB (conclusion, energy-consistent). These span a 23 dB range.

### M-5. Table 4 (oblate Ritz) does not match current code
Both the Ritz frequencies and (at E = 0.5 MPa) even the sphere frequencies differ from code output. This table appears stale.

### M-6. Section 2.4 ka calculation uses wrong model parameters
The `ka = 0.017` comes from the code default model (a = 0.15 m), not from the Table 1 canonical model (a = 0.18 m). With canonical parameters, ka at f₂ is 0.011, and (ka)² = 1.3 × 10⁻⁴ — roughly half the stated 2.8 × 10⁻⁴.

---

## Minor Issues

### m-1. Discussion says f₂ = 4.4 Hz for E = 0.1 MPa (§5.2, line 65)
Code gives 3.95 Hz. The value 4.4 appears to be a leftover from an earlier version.

### m-2. Table 7 WBV displacements (3,115 / 7,165 μm) match no identifiable calculation
They are approximately but not exactly consistent with any Q or √2 convention.

### m-3. Breathing mode inconsistency
Eq. (9) says "≈ 2900 Hz", abstract says "near 2500 Hz", code gives 2491 Hz. Pick one value.

### m-4. Code quality: magic numbers
`R_char = 0.16` is hardcoded in `mechanotransduction.py` line 169. The viscous correction module hardcodes `R_CANONICAL = 0.157`, `F2_HZ = 4.0`, `ZETA_STRUCT = 0.125` which match Table 1 but not the code defaults. These should be derived from a shared canonical model.

### m-5. No experimental validation
The model predicts f₂ ≈ 4 Hz for the canonical parameters. The paper compares favourably to the ISO 2631 band (4–8 Hz) but cites no direct measurement of abdominal wall eigenfrequencies. Cadaver modal testing, MRI elastography resonance measurements, or accelerometer studies (e.g., Kitazaki & Griffin 1998) could provide direct validation. The paper should be clearer about the distinction between "consistent with ISO 2631 transmissibility data" and "validated against eigenfrequency measurements."

### m-6. Code `AbdominalModelV2` uses `rho_wall` as attribute name but constructor accepts `rho_w`
Looking at the dataclass: the field is `rho_wall` in the dataclass but the paper canonical model instantiation uses `rho_w=1100` as keyword — wait, actually it accepts `rho_wall`. But some scripts use `rho_w` as local variables, which could cause confusion. This is cosmetic.

### m-7. Eq. (20) uses `x_base` notation but the code calls it `displacement_amplitude_m`
Minor naming inconsistency; both are clear in context.

---

## What's Done Well

1. **Mode family separation** is physically correct and well-explained. The distinction between breathing modes (kHz, fluid-dominated) and flexural modes (Hz, shape-changing) is the key insight and it is rigorously derived.

2. **Comprehensive sensitivity analysis.** The parametric sweep over 486 configurations, multi-layer wall model, oblate spheroid correction, viscous correction, nonlinear analysis, gas pocket mechanism, and orifice coupling analysis represent an impressively thorough investigation of alternative pathways and model limitations.

3. **Code organisation.** 17 well-documented analytical modules with clear docstrings, proper unit annotations, and a comprehensive test suite. The code is genuinely readable and the physics is traceable from the docstrings.

4. **Honest limitations section.** Eight numbered limitations, each with a qualitative assessment of its effect on conclusions. This is exemplary.

5. **Energy budget cross-check.** The reciprocity-based energy analysis (absorption cross-section, radiation damping) provides an independent verification of the displacement estimate. This is a strong methodological contribution.

6. **Qualitative robustness.** Despite all the numerical issues above, the central conclusion — that airborne coupling is orders of magnitude weaker than mechanical coupling — holds under any reasonable parameter combination. The coupling ratio would need to be wrong by 3–4 orders of magnitude to change the conclusion, and none of the issues I've identified come close to that.

7. **Sobol analysis identifies E as dominant.** ST = 0.86 for E is a clear, actionable result for future experimental work. The saved JSON confirms this.

---

## Summary Recommendation: **MAJOR REVISION**

The physics is sound and the qualitative conclusions are robust. But the paper currently contains **too many quantitative inconsistencies** to be considered reproducible:

- Two different loss tangent baselines used without acknowledgement
- Table 6 contradicts the stated equation by a factor of √2
- Table 3 (UQ) does not match the saved computational results
- Three different values (0.014, 0.14, 0.18 μm) reported for the same quantity at 120 dB
- Table 4 does not match the current code
- ka calculation uses wrong model parameters
- SPL for PIEZO threshold reported as 135, 137, or 158 dB depending on section

**Required actions:**

1. **Standardise the loss tangent.** Pick η = 0.25 or η = 0.30 and use it everywhere. Update Table 1, Section 2 text, Tables 5–7, Discussion, UQ, and code defaults to be consistent.

2. **Resolve the √2 discrepancy** in Table 6 / Eq. (20). If Eq. (20) is correct (a_rms√2/ω²), update Table 6. If the table is correct (RMS displacement, not peak), update Eq. (20) and label it clearly.

3. **Re-run UQ and update Table 3** to match the code. Alternatively, if the paper Table 3 is from a deliberate different analysis, explain what that analysis was.

4. **Choose one displacement convention** (energy-consistent or pressure-based) as primary, present it consistently, and report the other as a cross-check. Do not mix them in the coupling ratio or SPL threshold.

5. **Regenerate Table 4** (oblate Ritz) from the current code with canonical parameters.

6. **Fix Section 2.4 ka calculation** to use canonical parameters, or make the example parameters explicit.

7. **Provide a single `reproduce_paper.py` script** that generates all tables from consistent parameters.

8. **Add a convergence check** for the Sobol indices (e.g., N_base = 2048 vs 4096 vs 8192).

None of these issues alter the paper's conclusion. They are bookkeeping problems, but in a quantitative paper, the bookkeeping *is* the science.
