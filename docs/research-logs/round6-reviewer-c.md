# Reviewer C --- Round 6

**Paper:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the Brown Note"

**Reviewer focus:** Reproducibility, numerical rigour, code--paper consistency, uncertainty completeness.

---

## Overall Assessment

The paper has matured significantly since Round 4.  The breathing-mode discrepancy (2900 vs 2500 Hz) flagged previously is now fully resolved in the main text.  The canonical parameters in Table 1 are consistent with code defaults, the modal frequencies match, and the energy-budget framework is self-consistent.  The test suite (118 tests, all passing) provides strong confidence in the core analytical pipeline.

However, I have identified one **material numerical error** in the Discussion (Section 5.1) and several **minor but reportable** discrepancies between paper tables and the current code for the oblate Ritz and boundary-condition analyses.  The coupling ratio $\mathcal{R}$ is defined on three different bases across the paper, UQ table, and abstract---this should be reconciled.  Overall the paper is close to acceptance but needs a targeted revision pass to clean up the remaining inconsistencies.

---

## Code Verification Results (show my work!)

### 1. Canonical Parameters: Code Defaults vs Paper Table 1

| Parameter | Paper (Table 1) | Code Default | Match? |
|-----------|:---:|:---:|:---:|
| $a$ (semi-major) | 0.18 m | 0.18 m | OK |
| $c$ (semi-minor) | 0.12 m | 0.12 m | OK |
| $h$ (wall thickness) | 0.010 m | 0.010 m | OK |
| $E$ (elastic modulus) | 0.1 MPa | 0.1e6 Pa | OK |
| $\nu$ (Poisson) | 0.45 | 0.45 | OK |
| $\rho_w$ (wall density) | 1100 kg/m^3 | 1100.0 | OK |
| $\rho_f$ (fluid density) | 1020 kg/m^3 | 1020.0 | OK |
| $K_f$ (bulk modulus) | 2.2 GPa | 2.2e9 | OK |
| $P_\text{iap}$ | 1000 Pa | 1000.0 | OK |
| $\eta$ (loss tangent) | 0.25 | 0.25 | OK |

**Verdict:** Perfect match. The `AbdominalModelV2` defaults and `CANONICAL` dict in `modal_participation.py` are identical and consistent with Table 1.

### 2. Natural Frequencies (Table 2, Section 2)

| Mode | Code (Hz) | Paper (Hz) | Match? |
|------|:---------:|:----------:|:------:|
| $n=0$ (breathing) | 2490.7 | ~2500 | OK (0.4% rounding) |
| $n=2$ | 3.952 | 4.0 | OK (rounds to 4.0) |
| $n=3$ | 6.309 | 6.3 | OK |
| $n=4$ | 8.880 | 8.9 | OK |

### 3. E-Sweep Table (Table: tab:E_sweep)

| $E$ (MPa) | Code $f_2$ (Hz) | Paper $f_2$ (Hz) | Match? |
|:----------:|:---------------:|:----------------:|:------:|
| 0.05 | 3.4 | 3.4 | OK |
| 0.10 | 4.0 | 4.0 | OK |
| 0.20 | 4.9 | 4.9 | OK |
| 0.50 | 7.1 | 7.1 | OK |
| 1.00 | 9.6 | 9.6 | OK |
| 2.00 | 13.3 | 13.3 | OK |

### 4. ISO Validation Table (Table: tab:iso)

| Body type | Code $f_2$ (Hz) | Paper $f_2$ (Hz) | Match? |
|-----------|:-:|:-:|:-:|
| Lean ($E=0.2$, $a=15$ cm) | 6.2 | 6.2 | OK |
| Average ($E=0.1$, $a=18$ cm) | 4.0 | 4.0 | OK |
| Large ($E=0.08$, $a=20$ cm) | 3.3 | 3.3 | OK |

### 5. Airborne Displacement Table (Table: tab:airborne)

| SPL (dB) | Code $\xi_\text{energy}$ (um) | Paper (um) | Code $\xi_\text{pressure}$ (um) | Paper (um) | Match? |
|:--------:|:----:|:----:|:-----:|:-----:|:------:|
| 100 | 0.0014 | 0.001 | 0.018 | 0.018 | OK (rounding) |
| 110 | 0.0043 | 0.004 | 0.058 | 0.058 | OK |
| 120 | 0.0137 | 0.014 | 0.184 | 0.18 | OK |
| 130 | 0.0435 | 0.044 | 0.583 | 0.58 | OK |
| 140 | 0.1374 | 0.14 | 1.844 | 1.84 | OK |

### 6. Mechanical Displacement Table (Table: tab:mechanical)

| $a_\text{rms}$ (m/s^2) | Code $x_\text{base}$ (um) | Paper (um) | Code $\xi_\text{rel}$ (um) | Paper (um) | Match? |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0.1 | 229 | 229 | 917 | 917 | OK |
| 0.5 | 1147 | 1147 | 4586 | 4586 | OK |
| 1.0 | 2293 | 2293 | 9173 | 9173 | OK |
| 1.15 | 2637 | 2637 | 10549 | 10549 | OK |

### 7. Coupling Ratio (Eq. 30)

Paper states: $\mathcal{R} = 917 / 0.014 \approx 6.6 \times 10^4$.

Code: $917.3 / 0.0137 = 66{,}950 \approx 6.7 \times 10^4$.

Arithmetic check: $917 / 0.014 = 65{,}500$ (paper's calculation), $6.6 \times 10^4 = 66{,}000$.

**Verdict:** Consistent within rounding.  The abstract says "roughly $7 \times 10^4$" which also matches.

### 8. Modal Participation Factor $\Gamma_2$ (Section 4.3)

Paper claims: $\Gamma_2 \approx 0.48$

Code (`participation_factor(0.18, 0.12, 2, 2*pi/3)`): **$\Gamma_2 = 0.4841$**

**Verdict:** Match.

### 9. Radiation Damping

Paper (Section 4.4): $\zeta_\text{rad} \approx 10^{-15}$

Code: $\zeta_\text{rad} = 8.98 \times 10^{-16}$

**Verdict:** Match (order of magnitude).

### 10. SPL for 1 um Threshold

Paper (Discussion, Section 5.2): "approximately 158 dB"

Code (binary search on energy-consistent displacement): **157.2 dB**

**Verdict:** Match (within rounding to nearest integer).

### 11. ka Value

Paper (Eq. 16): $ka \approx 0.0114$

Code ($2\pi \times 3.952 \times 0.1572 / 343$): **$ka = 0.01139$**

**Verdict:** Match.

### 12. Derived quantities

| Quantity | Paper | Code | Match? |
|----------|:-----:|:----:|:------:|
| $R_\text{eq}$ | 0.157 m (implicit) | 0.15724 m | OK |
| $Q$ | 4.0 | 4.0 | OK |
| $\zeta$ | 0.125 | 0.125 | OK |
| $(ka)^2$ | $1.3 \times 10^{-4}$ | $1.296 \times 10^{-4}$ | OK |
| $\lambda$ at $f_2$ | ~87 m | 86.8 m | OK |

### 13. UQ Results vs Paper Table (tab:uq_summary)

| Quantity | JSON Result | Paper | Match? |
|----------|:-----:|:----:|:------:|
| $f_2$ median | 6.43 Hz | 6.4 Hz | OK |
| $f_2$ 90% CI | [3.32, 15.48] Hz | [3.3, 15.5] Hz | OK |
| $\xi_\text{air}$ median | 0.178 um | 0.18 um | OK |
| $\xi_\text{mech}$ median | 1818 um | 1800 um | OK |
| $\mathcal{R}$ median | 9820 | $10^4$ | OK |
| SPL for PIEZO median | 135.0 dB | 135 dB | OK |
| SPL 90% CI | [128.1, 139.4] dB | [128, 139] dB | OK |
| $S_T(E)$ for $f_2$ | 0.861 | 0.86 | OK |

### 14. Oblate Spheroid Ritz Table (tab:oblate_correction)

| E | Mode | Paper Ritz (Hz) | Code Ritz (Hz) | Discrepancy |
|:-:|:----:|:---:|:---:|:---:|
| 0.1 MPa | $n=2$ | 3.6 | 3.80 | **+5.6%** |
| 0.1 MPa | $n=3$ | 5.6 | 5.80 | +3.6% |
| 0.1 MPa | $n=4$ | 8.0 | 8.09 | +1.1% |
| 0.5 MPa | $n=2$ | 6.0 | 6.17 | +2.8% |
| 0.5 MPa | $n=3$ | 9.5 | 8.50 | **-10.5%** |
| 0.5 MPa | $n=4$ | 12.9 | 11.30 | **-12.4%** |

**Verdict:** Several Ritz table entries do not match the current code output.  The most severe discrepancy is E=0.5 MPa, n=3 (9.5 vs 8.5 Hz, 10.5% off) and n=4 (12.9 vs 11.3 Hz, 12.4% off).  This suggests the Ritz code was refactored after the table was generated.

### 15. BC Results Table (tab:bc_results)

Paper says: "Free sphere (Ritz) = 4.13 Hz"

Code (`oblate_ritz_frequency(2, 0.18, 0.12, ...)`): **3.80 Hz**

**Verdict:** 8.7% discrepancy.  The table needs regeneration from the current code.

### 16. Test Suite

```
118 passed, 1 warning in 11.64s
```

All tests pass.  The test suite includes regression tests with frozen values (e.g., f2 ~ 3.95, xi_energy ~ 0.0137 um, xi_mech ~ 917 um), energy conservation checks, optical theorem bounds, symmetry limits, edge cases, and parametric monotonicity.  This is excellent test coverage.

---

## Reproducibility Issues

### R-1. Discussion Section 5.1: Wrong frequency for ka value [MAJOR]

Lines 24--33 of `discussion.tex` state:

> At 7 Hz with $R_\text{eq} = 0.157$ m, we obtain $ka \approx 0.0114$ and therefore $(ka)^2 \approx 1.3 \times 10^{-4}$ ... the incident wavelength ($\lambda \approx 49$ m) is nearly 370 times the body diameter.

**Three errors in this sentence:**

1. **$ka = 0.0114$ is at $f_2 \approx 4$ Hz, not 7 Hz.**  At 7 Hz, $ka = 2\pi \times 7 \times 0.157 / 343 = 0.0202$.
2. **$\lambda = 49$ m is correct at 7 Hz**, but $\lambda = 87$ m at the canonical $f_2 = 4$ Hz where $ka = 0.0114$ actually applies.
3. **"370 times the body diameter"** does not hold at any relevant frequency.  At 7 Hz: $49 / 0.314 = 156$.  At 4 Hz: $87 / 0.314 = 277$.

The Formulation (Section 2.4, Eq. 16) correctly computes $ka = 0.0114$ at $f_2 \approx 4$ Hz.  The Discussion section has copy-pasted the ka value but attributed it to the wrong frequency, and the other numbers (lambda, diameter ratio) correspond to 7 Hz.  This paragraph mixes two different frequencies.

### R-2. Oblate Ritz and BC tables are stale [MINOR]

Tables `tab:oblate_correction` and `tab:bc_results` contain values that differ from the current `oblate_spheroid_ritz.py` output by up to 12.4%.  Most likely the Ritz solver was improved after these tables were typeset.  The tables should be regenerated from the current code to ensure reproducibility.

### R-3. Could someone reproduce Figure 3 (fig_coupling_comparison) from text alone?

Largely yes.  The paper provides:
- All model equations (Section 2)
- All canonical parameters (Table 1)
- The energy-budget reciprocity formulation (Section 4)
- The base-excitation FRF (Eq. 26-28)

Missing details that would help:
- The exact frequency sweep range used in the figure (1--20 Hz, extractable from code)
- The exact log-scale plotting convention
- Whether the airborne curve uses pressure-based or energy-consistent displacement (the figure script uses `flexural_mode_pressure_response`, i.e., pressure-based)

---

## Uncertainty and Statistical Rigour

### U-1. Coupling Ratio Computed on Different Bases [MODERATE]

The coupling ratio $\mathcal{R}$ appears in three places with three different values:

| Location | $\mathcal{R}$ | Airborne basis | Mech $a_\text{rms}$ |
|----------|:---:|:---:|:---:|
| Eq. 30 | $6.6 \times 10^4$ | Energy-consistent (0.014 um) | 0.1 m/s^2 |
| UQ Table (canonical) | ${\sim}2.5 \times 10^4$ | Pressure-based (0.184 um) | 0.5 m/s^2 |
| UQ Table (median) | ${\sim}10^4$ | Pressure-based | 0.5 m/s^2 |

The UQ code in `uncertainty_quantification.py` line 142 uses `flexural_mode_pressure_response` (pressure-based) for `xi_air_um`, whereas eq. 30 in the paper explicitly uses the energy-consistent value.  The UQ also evaluates mechanical displacement at $a_\text{rms} = 0.5$ m/s^2 (the EU Action Value), while eq. 30 uses 0.1 m/s^2.  These compounding differences produce a ~2.6x gap.

While the paper's UQ table caption notes "Airborne displacement $\xi_\text{air}$ is the pressure-based upper bound," the coupling ratio column does not carry a corresponding caveat.  This means a reader comparing the UQ median ($10^4$) with eq. 30 ($6.6 \times 10^4$) might think the two are inconsistent, when in fact they measure the same ratio using different definitions.

**Recommendation:** Either compute the UQ coupling ratio on the same basis as eq. 30 (energy-consistent airborne, 0.1 m/s^2 mechanical), or add an explicit note to the UQ table explaining why R differs.

### U-2. UQ Table R 90% CI Reporting [MINOR]

Paper (tab:uq_summary): $\mathcal{R}$ 90% CI = [$10^3$, $10^4$]

JSON data: p5 = 1780, p95 = 34,169

The lower bound rounds to ~$2 \times 10^3$ (reported as $10^3$, which is conservative). The upper bound is $3.4 \times 10^4$ (reported as $10^4$, which rounds away a factor of 3).  The reported CI underestimates the spread.  Consider reporting as [$2 \times 10^3$, $3 \times 10^4$] for honesty.

### U-3. MC Sample Size Adequacy [OK]

$N = 10{,}000$ MC samples with 10,000/10,000 valid evaluations (100% success rate).  The Sobol analysis uses $N = 4096$ base samples ($\times (2D+2) = 81{,}920$ total evaluations).  For 9 parameters, this exceeds the typical convergence threshold.  The $S_T$ sum for $f_2$ is $\sum S_T \approx 1.027$ (should be ~1.0); the slight excess is normal for Sobol estimators.  **Adequate.**

### U-4. UQ on Coupling Ratio and Displacement [PARTIAL]

The MC propagates uncertainty through $f_2$, $\xi_\text{air}$, $\xi_\text{mech}$, $\mathcal{R}$, and SPL for PIEZO threshold.  **Positive:** the coupling ratio is included, and its distribution confirms the $10^3$--$10^4$ range.  However, the Sobol indices for $\mathcal{R}$ show $S_T(E) = 0.43$ and $S_T(P_\text{iap}) = 0.13$ --- the dominance of $E$ is weaker for the coupling ratio than for $f_2$ alone.  This nuance is not discussed in the paper.

---

## Major Issues

### M-1. Discussion ka/frequency mismatch (R-1)

The paragraph in Section 5.1 (lines 24--33 of discussion.tex) contains three compounding numerical errors, all from mixing 4 Hz and 7 Hz values.  This is in the Discussion section of the paper and will confuse careful readers.  Must be fixed.

**Fix:** Replace "At 7 Hz" with "At $f_2 \approx 4$ Hz" and update $\lambda$ to 87 m and the diameter ratio accordingly, OR recalculate all values consistently at 7 Hz ($ka = 0.020$, $(ka)^2 = 4.0 \times 10^{-4}$, $\lambda = 49$ m, ratio = 156).

---

## Minor Issues

### m-1. Oblate Ritz and BC tables stale (R-2)

Regenerate Tables `tab:oblate_correction` and `tab:bc_results` from current code.  The maximum discrepancy is 12.4%.

### m-2. Coupling ratio basis inconsistency (U-1)

Add a footnote to the UQ coupling ratio column or reconcile the bases used in eq. 30 vs the UQ.

### m-3. UQ R 90% CI rounded too aggressively (U-2)

Report as [$2 \times 10^3$, $3 \times 10^4$] instead of [$10^3$, $10^4$].

### m-4. outline.md still says 2900 Hz

The `outline.md` file (not part of the submitted paper, but in the repo) still references the old 2900 Hz breathing mode value.  Housekeeping only.

### m-5. Figure coupling comparison: clarify pressure vs energy basis

The coupling comparison figure (fig_coupling_comparison) uses `flexural_mode_pressure_response` for the airborne curve, giving the pressure-based displacement.  Since the paper text prominently features the energy-consistent value (0.014 um), the figure should either use the energy-consistent curve or annotate clearly that it shows the pressure-based upper bound.

---

## What's Done Well

1. **Canonical parameter consistency:** Table 1, code defaults, `CANONICAL` dict, figure generation scripts, and UQ parameter distributions all use the same values.  This is a significant improvement over earlier rounds.

2. **Test suite:** 118 tests covering dimensional consistency, known limits, energy conservation, optical theorem bounds, symmetry/convergence, regression values, edge cases, and parametric monotonicity.  This is publication-grade test coverage for a computational mechanics paper.

3. **Energy budget self-consistency:** The energy-conserved check (`P_abs == P_diss` within 1%) passes at all SPL levels.  The known ~13.4x overestimate of the pressure-based approach is documented and quantified.

4. **UQ pipeline:** Full MC + Sobol with physiologically justified distributions, proper inverse-CDF transforms for the Saltelli sampling, saved JSON results, and seeded reproducibility (seed=42).

5. **Numerical stability:** No crashes or NaN outputs across the full parameter range tested, including extreme edge cases (E=0, h=1e-6, c=a).

6. **Quantitative core result is robust:** The four-order-of-magnitude coupling disparity holds across all parameter variations, uncertainty propagation, and model refinements (oblate, nonlinear, BC corrections).  The conclusion is solid.

---

## Summary Recommendation: MINOR REVISION

The core results are correct, well-tested, and reproducible.  The one major issue (Discussion ka/frequency mismatch) is a localised text error that does not affect any computation or conclusion.  The stale Ritz tables and coupling ratio basis inconsistency are addressable in a single revision pass.  Once these items are cleaned up, the paper should be ready for acceptance.
