# Reviewer C ΓÇö Round 1

## Overall Assessment

This paper presents a clean analytical framework for a genuinely interesting
question. The core physics (fluid-filled shell modes, Rayleigh-regime
acoustic coupling, energy-budget reciprocity) is implemented competently
and the main conclusions are qualitatively robust. However, my forensic
code-level review reveals a **systematic parameter inconsistency** between
the paper's canonical values (Table 1) and the code defaults used for
figure generation and regression tests. I also found several numerical
errors in specific tables and one section of the Discussion that mixes
frequencies, producing incorrect intermediate numbers. None of these
issues threaten the paper's central conclusion ΓÇö the coupling disparity is
real and large ΓÇö but they undermine reproducibility and require correction
before publication.

---

## Test Suite Status

| Metric | Result |
|---|---|
| Total tests | 118 |
| Passed | 118 |
| Failed | 0 |
| Warnings | 1 (deprecation in dateutil) |
| Runtime | 10.4 s |

**All 118 tests pass.** The test suite is well-structured, covering
dimensional consistency, physical limits, energy conservation, reciprocity
bounds, symmetry, regression, edge cases, and monotonicity. However, the
regression tests freeze values for the **code-default** model
(`soft_tissue_model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)`),
which uses h=0.015, ╬╜=0.49, ╧ü_w=1050, ╧ü_f=1040, ╬╖=0.30 ΓÇö **not** the
paper's Table 1 canonical values (h=0.01, ╬╜=0.45, ╧ü_w=1100, ╧ü_f=1020,
╬╖=0.25).

---

## Code Verification Results

### A. Core Canonical Outputs (Paper Table 1 Parameters)

All verified with: `E=0.1e6, a=0.18, c=0.12, h=0.01, ╬╜=0.45, ╧ü_w=1100, ╧ü_f=1020, P=1000, ╬╖=0.25`

| Quantity | Paper Claim | Code Output | Match? |
|---|---|---|---|
| R_eq | 0.157 m | 0.15724 m | Γ£ô |
| fΓéÇ (breathing) | ~2500 Hz | 2490.7 Hz | Γ£ô |
| fΓéé | 4.0 Hz | 3.952 Hz | Γ£ô (rounds) |
| fΓéâ | 6.3 Hz | 6.309 Hz | Γ£ô |
| fΓéä | 8.9 Hz | 8.880 Hz | Γ£ô |
| ka at fΓéé | 0.0114 | 0.01139 | Γ£ô |
| (ka)┬▓ | 1.3├ù10Γü╗Γü┤ | 1.296├ù10Γü╗Γü┤ | Γ£ô |
| ╬╛_energy (120 dB) | 0.014 ╬╝m | 0.01374 ╬╝m | Γ£ô |
| ╬╛_pressure (120 dB) | 0.18 ╬╝m | 0.1844 ╬╝m | Γ£ô |
| ╬╛_mech (0.1 m/s┬▓) | 917 ╬╝m | 917.3 ╬╝m | Γ£ô |
| ╬╛_mech (0.5 m/s┬▓) | 4586 ╬╝m | 4586.3 ╬╝m | Γ£ô |
| ╬╛_mech (1.15 m/s┬▓) | 10549 ╬╝m | 10548.6 ╬╝m | Γ£ô |
| ╬╢_rad (air) | ~10Γü╗┬╣Γü╡ | 8.98├ù10Γü╗┬╣Γü╢ | Γ£ô |
| Sobol S_T(E) | 0.86 | 0.861 | Γ£ô |
| Q | 4.0 | 4.0 | Γ£ô |
| Z_air | 420 Pa┬╖s/m | 420.2 Pa┬╖s/m | Γ£ô |
| T (impedance) | 5├ù10Γü╗Γü┤ | 5.25├ù10Γü╗Γü┤ | Γ£ô |
| k_fluid | 4.2├ù10┬╣Γü░ | 4.20├ù10┬╣Γü░ | Γ£ô |
| k_shell | ~1.5├ù10Γü╡ | 1.47├ù10Γü╡ | Γ£ô |
| Fluid/shell mass ratio | 7.4├ù | 7.3├ù | Γ£ô (minor) |
| SPL for PIEZO (1 ╬╝m) | ~158 dB | 157.2 dB | Γ£ô (rounding) |

### B. Table-by-Table Cross-Check

**Table E_sweep (results.tex Table 1) ΓÇö PASS**

| E (MPa) | Paper fΓéé | Code fΓéé | Match? |
|---|---|---|---|
| 0.05 | 3.4 | 3.37 | Γ£ô |
| 0.10 | 4.0 | 3.95 | Γ£ô |
| 0.20 | 4.9 | 4.92 | Γ£ô |
| 0.50 | 7.1 | 7.06 | Γ£ô |
| 1.00 | 9.6 | 9.62 | Γ£ô |
| 2.00 | 13.3 | 13.35 | Γ£ô |

**Table airborne (section4 Table 4) ΓÇö PASS** (all verified above)

**Table mechanical (section4 Table 5) ΓÇö PASS** (all verified above)

**Table oblate_correction (results.tex Table 3) ΓÇö PARTIAL FAIL**

| Config | Paper Sphere | Code Sphere | Paper Ritz | Code Ritz | Sphere Match? |
|---|---|---|---|---|---|
| E=0.1, n=2 | 4.0 | 4.0 | 3.6 | 3.8 | Γ£ô |
| E=0.1, n=3 | 6.3 | 6.3 | 5.6 | 5.8 | Γ£ô |
| E=0.1, n=4 | 8.9 | 8.9 | 8.0 | 8.1 | Γ£ô |
| E=0.5, n=2 | 7.1 | 7.1 | 6.0 | 6.2 | Γ£ô |
| **E=0.5, n=3** | **11.3** | **10.0** | 9.5 | 8.5 | **Γ£ù (-13%)** |
| **E=0.5, n=4** | **14.4** | **12.9** | 12.9 | 11.3 | **Γ£ù (-11%)** |

**Table ISO (results.tex Table 5) ΓÇö PASS (with undocumented assumption)**

Reproduces only when c/a=0.67 is applied to each body type (e.g., Lean:
a=0.15, c=0.1005 ΓåÆ fΓéé=6.23 Hz Γëê 6.2 Hz). The table does not specify c values.

**Table BC (results.tex Table 2) ΓÇö PASS numerically but parameters differ**

The BC analysis (`fea_modal_results.json`) used ╧ü_f=1000 (not 1020),
P_iap=1500 (not 1000), and R=0.162 (not 0.157) ΓÇö undocumented. Values match
the JSON exactly: 4.13, 3.91, 3.89, 3.66 Hz.

**UQ Table (results.tex Table 2) ΓÇö PASS with one CI error**

| Quantity | Paper | JSON | Match? |
|---|---|---|---|
| fΓéé median | 6.4 Hz | 6.43 Hz | Γ£ô |
| fΓéé 90% CI | [3.3, 15.5] | [3.32, 15.48] | Γ£ô |
| ╬╛_air median | 0.18 ╬╝m | 0.178 ╬╝m | Γ£ô |
| ╬╛_air 90% CI | [0.11, 0.39] | [0.107, 0.394] | Γ£ô |
| ╬╛_mech median | 1800 ╬╝m | 1818 ╬╝m | Γ£ô |
| ╬╛_mech 90% CI | [300, 8200] | [296, 8176] | Γ£ô |
| **R 90% CI** | **[10┬│, 10Γü┤]** | **[1780, 34169]** | **Γ£ù** |
| SPL PIEZO median | 135 dB | 135.0 dB | Γ£ô |
| SPL PIEZO 90% CI | [128, 139] | [128.1, 139.4] | Γ£ô |

---

## Reproducibility Assessment

### Figure Generation

All 7 paper-referenced figures have corresponding generation functions
in `scripts/generate_jsv_figures.py` and PDF files exist in `data/figures/`.
The test suite verifies they generate without error (`test_figures.py`).

**However**, figures are generated using **code-default parameters**, not
the paper's Table 1 canonical parameters. The consequence is:

| Parameter | Paper Table 1 | Code Default | Effect |
|---|---|---|---|
| h | 0.010 m | 0.015 m | Γåæ bending stiffness |
| ╬╜ | 0.45 | 0.49 | Γåæ membrane stiffness |
| ╧ü_w | 1100 kg/m┬│ | 1050 kg/m┬│ | Γåô wall mass |
| ╧ü_f | 1020 kg/m┬│ | 1040 kg/m┬│ | Γåæ fluid mass |
| ╬╖ | 0.25 | 0.30 | Γåæ damping |
| **fΓéé** | **3.95 Hz** | **4.38 Hz** | **11% shift** |

The figures thus show fΓééΓëê4.4 Hz while the text says fΓéé=4.0 Hz. This is
a systematic reproducibility failure: someone following the paper's
parameters will get different numbers from those shown in the figures.

### Sobol Convergence

- N_SOBOL_base = 4096 ΓåÆ 4096├ù(2├ù9+2) = 81,920 total evaluations
- For 9 parameters with first-order only: adequate sample size
- S_T(E) = 0.861, SΓéü(E) = 0.812 ΓÇö the gap (0.049) indicates modest
  interaction effects
- Second-order indices not computed (`calc_second_order=False`); this is
  acceptable given the dominance of E

### MC Sample Size

- N_MC = 10,000 ΓÇö adequate for median and 90% CI estimation
- My independent 2000-sample MC gives median=6.56 Hz, CI=[3.4, 15.9],
  consistent with sampling noise at that sample size
- The log-normal E distribution is the dominant source of skewness;
  10k samples captures the tail adequately

---

## Uncertainty and Statistical Rigour

1. **UQ is done for fΓéé and displacement** ΓÇö Good. The Sobol analysis correctly
   identifies E as dominant (86%) with h second (12%).

2. **UQ for ╬╛_air uses pressure-based displacement, not energy-consistent** ΓÇö
   The table footnote acknowledges this. However, the coupling ratio R in
   Table 2 is therefore computed as ╬╛_mech/╬╛_air_pressure Γëê 10Γü┤, while the
   standalone coupling ratio (eq 35) uses ╬╛_air_energy giving R Γëê 6.6├ù10Γü┤.
   These are a factor of ~13 apart, and the paper doesn't fully reconcile them.

3. **No UQ on coupling ratio R through the energy-consistent pathway** ΓÇö Since
   R is the "central result," this is a gap. The pressure-based UQ on R gives
   CI=[10┬│, 3.4├ù10Γü┤], but the energy-consistent R would be 13├ù larger at
   each sample. The paper should clarify which R it means in each context.

4. **Boundary condition parameters not propagated through UQ** ΓÇö The 6ΓÇô11%
   frequency shift from BCs is outside the UQ, which only varies material
   and geometric parameters. The UQ CI should be acknowledged as conditional
   on free-shell BCs.

---

## Major Issues

**M1. Internal coupling ratio inconsistency (4.6├ù10Γü┤ vs 6.6├ù10Γü┤)**

The abstract and conclusion both state R Γëê 4.6├ù10Γü┤. Equation (35) gives
R = 917/0.014 Γëê 6.6├ù10Γü┤. The UQ Table 2 reports R median Γëê 10Γü┤
(pressure-based). I was unable to reproduce 4.6├ù10Γü┤ from any parameter
combination in the code. This appears to be a stale number from an earlier
model version. The abstract, conclusion, eq (35), and UQ table should all
agree on the definition and value of R.

**M2. FigureΓÇôtable parameter mismatch**

Figure generation scripts use `AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)`
which leaves h, ╬╜, ╧ü_w, ╧ü_f, and ╬╖ at code defaults (h=0.015, ╬╜=0.49,
╬╖=0.30). The paper's Table 1 specifies h=0.01, ╬╜=0.45, ╬╖=0.25. This
produces fΓéé=4.38 Hz in figures vs fΓéé=3.95 Hz in tables ΓÇö an 11% discrepancy.
All figure scripts should use Table 1 parameters explicitly.

**M3. Table 3 sphere frequencies wrong for E=0.5 MPa at n=3, n=4**

Paper Table 3 (oblate correction) claims sphere frequencies of 11.3 Hz
(n=3) and 14.4 Hz (n=4) at E=0.5 MPa. Running `flexural_mode_frequencies_v2`
with Table 1 geometry gives 10.0 Hz and 12.9 Hz. The error is 13% and 12%
respectively. These values appear to have been computed with different
(undocumented) parameters.

---

## Minor Issues

**m1. Discussion ┬º5.1 ka error at 7 Hz**

The Discussion states "At 7 Hz with R_eq=0.157 m, we obtain ka Γëê 0.0114."
At 7 Hz: ka = 2╧Ç├ù7├ù0.157/343 = 0.0201, not 0.0114. The value 0.0114 is
correct at fΓééΓëê4 Hz. The (ka)┬▓Γëê1.3├ù10Γü╗Γü┤ and ╬╗/diameter Γëê 370 claims in
the same paragraph are also from fΓééΓëê4 Hz, not 7 Hz. The paragraph should
consistently use one frequency.

**m2. BC table uses non-canonical parameters**

The `fea_modal_results.json` underlying Table 2 (BC) was computed with
╧ü_f=1000 (not 1020), P_iap=1500 (not 1000). These deviations are not
documented in the table or text.

**m3. BC table claim of "exact" reproduction**

The paper states "The free-sphere Ritz frequency (4.13 Hz) reproduces the
analytical solution exactly." The analytical Lamb solution at those parameters
gives 4.26 Hz ΓÇö a 3.1% discrepancy. This should say "within 3%" not "exactly."

**m4. UQ Table R 90% CI upper bound**

Paper says R 90% CI = [10┬│, 10Γü┤]. The actual p95 = 3.4├ù10Γü┤, not 10Γü┤.
Should be [10┬│, 3├ù10Γü┤] or expressed in order-of-magnitude notation.

**m5. ISO table (Table 5) undocumented assumption**

The ISO validation table reproduces only when c/a=0.67 is used for all
body types. Since only E and a are given in the table, a reader cannot
reproduce the values without guessing c. Add a c column or footnote.

**m6. Code defaults don't match paper defaults**

The `AbdominalModelV2` dataclass defaults (E=0.5 MPa, a=0.15, h=0.015, ╬╜=0.49,
╧ü_w=1050, ╬╖=0.3) don't match the paper's canonical parameters. This is a
latent reproducibility hazard for anyone who writes `AbdominalModelV2()`
expecting the paper's baseline.

**m7. SPL threshold rounding**

Paper says "approximately 158 dB"; code gives 157.2 dB. Suggest "~157 dB"
or "157ΓÇô158 dB."

**m8. Pressure-based "upper bound" terminology inconsistent**

The paper refers to ╬╛_pressure as an "upper bound" but section4 Table 4
presents both ╬╛_energy and ╬╛_pressure columns, calling the latter simply
"pressure" not "bound." The Table 2 footnote says energy-consistent is
"~13├ù smaller" but the actual ratio varies from 13.0 to 13.5 across SPL.

---

## What's Done Well

1. **Energy budget is self-consistent**: `P_absorbed == P_dissipated` to
   machine precision for the energy-based displacement. This was verified
   across all SPL levels (100ΓÇô140 dB). The code explicitly checks this.

2. **Comprehensive test suite**: 118 tests covering 8 categories. Edge
   cases (E=0, hΓåÆ0, c=a) are handled gracefully. Monotonicity tests catch
   physics violations automatically.

3. **UQ is genuine, not decorative**: Real MC sampling (N=10k), real Sobol
   analysis (N_base=4096), proper inverse-CDF mapping for non-uniform
   distributions, and the code is seed-controlled (seed=42) for reproducibility.

4. **Clear separation of pressure-based and energy-based approaches**: The
   code maintains both and documents the ~13├ù discrepancy. The energy-budget
   resolution via Junger & Feit reciprocity is physically well-motivated.

5. **Multiple independent consistency checks**: Optical theorem bounds,
   reciprocity, sphere-limit convergence of the oblate Ritz solver, and
   energy conservation are all tested.

6. **The core result is robust**: Despite the parameter inconsistencies,
   the coupling disparity (10┬│ΓÇô10Γü╡) is so large that no reasonable
   parameter choice can close it. The conclusion is qualitatively correct
   regardless of which exact numbers are used.

---

## Summary Recommendation: MINOR REVISION

The central physics and conclusions are sound and well-supported by the
computational framework. The issues are:

- **3 major**: Coupling ratio inconsistency (M1), figureΓÇôtable parameter
  mismatch (M2), wrong numbers in Table 3 (M3). All are fixable by
  (a) updating the abstract/conclusion R to match eq (35), (b) passing
  canonical parameters to all figure scripts, and (c) regenerating Table 3.

- **8 minor**: Mostly editorial (ka error in discussion, rounding,
  undocumented assumptions). All straightforward fixes.

None of the issues change the qualitative conclusion. The four-order-of-magnitude
coupling disparity survives under any consistent parameterization.
