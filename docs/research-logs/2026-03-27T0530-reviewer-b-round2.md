# Reviewer B — Round 2 Review of Browntone v2 Model

**Date:** 2026-03-27T05:30  
**Reviewer:** B (Computational Acoustics / Fluid-Structure Interaction)  
**Documents reviewed:**
- `src/analytical/natural_frequency_v2.py` (corrected modal analysis)
- `src/analytical/mechanical_coupling.py` (WBV vs airborne comparison)
- `src/analytical/parametric_analysis.py` (comprehensive parametric study)
- `src/analytical/mechanotransduction.py` (PIEZO pathway — still v1)
- `docs/research-logs/2026-03-27T0515-reviewer-b-triage.md` (triage response)
- All numerical output from running the above scripts

---

## Overall Verdict: MAJOR REVISION (upgraded from REJECT)

The v2 model represents a **substantial and creditable improvement** over v1. The two
most egregious errors — omission of fluid bulk modulus from the breathing mode (F1)
and naive use of full p_inc for flexural drive (F2) — are both corrected. The pivot
from "airborne brown note" to "mechanical vs airborne pathway comparison" is
physically well-motivated and, in my assessment, **qualitatively correct**.

The flexural-mode frequencies now fall in a range (3–11 Hz, depending on parameters)
that is broadly consistent with the ISO 2631 whole-body vibration literature. The
argument that airborne acoustic coupling to these modes is vanishingly weak (via the
(ka)^n penalty) is sound in principle. The mechanical coupling pathway is the
correct physics for explaining GI effects of low-frequency vibration.

**However**, the model still contains **no fatal flaws but five major quantitative
issues** that must be resolved before this is publishable. Three of these are internal
inconsistencies that undermine the numerical conclusions even though the qualitative
story is correct.

---

## Fatal Flaws: NONE

This is a significant improvement. The qualitative physics is now correct.

---

## Major Issues (5)

### M1. Energy budget is VIOLATED, not conserved — code output contradicts its own conclusion

**Severity: Major (internal inconsistency)**

The `parametric_analysis.py` energy budget (lines 95–168) correctly computes
P_dissipated and P_available, and the output clearly shows:

```
SPL(dB)    P_avail(W)    P_diss(W)    Conserved?
  100      9.35e-12      1.95e-11        ✗ NO
  110      9.35e-11      1.95e-10        ✗ NO
  120      9.35e-10      1.95e-09        ✗ NO
  ...
```

The ratio P_diss / P_avail ≈ **2.08 at every SPL** (constant, as expected since
both scale as p_inc²). This is an energy conservation violation — the model predicts
more power dissipated than is available through the coupling channel.

**Yet the conclusion text (lines 369–371) states:**
> "ENERGY BUDGET: For v2 flexural modes with (ka)^n coupling, energy is conserved
> at all tested SPL."

This directly contradicts the numerical output. Either (a) the displacement should
be reduced by a factor of √2.08 ≈ 1.44, or (b) the available power estimate is
too conservative. The discrepancy likely arises from an inconsistency between:

- Pressure coupling: p_eff = p_inc × (ka)^n → energy ∝ (ka)^2n
- Scattering cross-section: σ_n ∝ R² × (ka)^(2n+2) (Rayleigh limit)

The extra (ka)^2 in the scattering formula accounts for radiation efficiency, which
the pressure-based coupling neglects. If the scattering cross-section is the correct
measure of available power, the violation would be not 2× but ~2/(ka)² ≈ 13,000×
for ka ≈ 0.013. This needs rigorous resolution.

**In practice**, the factor-of-2 error does not change the qualitative conclusion
(airborne coupling is still far too weak), but for a quantitative paper this
inconsistency is disqualifying.

**Fix:** Derive the energy budget self-consistently from either (a) the full
scattering problem (Junger & Feit §9.3), or (b) a reciprocity argument linking
absorbed power to radiation resistance. Reconcile the pressure-based and
energy-based coupling estimates.

### M2. Theoretical vs empirical mechanical coupling: 3.7× discrepancy, unresolved

**Severity: Major (undermines quantitative predictions)**

At the n=2 resonance frequency (4.38 Hz), the mechanical coupling model
(`mechanical_coupling.py`, lines 119–138) gives two predictions:

| Method | Amplification | x_rel for 1.15 m/s² |
|--------|--------------|---------------------|
| Theoretical (SDOF FRF) | H_rel = 3.33 (= Q) | 7165 μm |
| Empirical (ISO 2631 T) | T−1 = 0.89 | 1911 μm |

The theoretical model overpredicts by a factor of **3.75**. The paper presents
both without resolving which is correct. This is a 575% discrepancy in the
primary quantity of interest.

**Root causes:**
1. The SDOF model at exact resonance gives H_rel = Q, but the real body has
   multiple coupled DOF (spine, pelvis, other organs) that drain energy from the
   abdominal mode. The effective Q at the abdomen is lower than the tissue Q.
2. The ISO transmissibility peak at 5–6 Hz is primarily the whole-body
   seated bouncing mode, not the abdominal cavity flexural mode specifically.
   Using T−1 as "relative displacement of the abdominal wall" conflates two
   different phenomena.
3. Modal participation factor: not all of the base excitation energy goes into
   mode n=2. Higher modes, rigid-body motion, and non-resonant deformation
   all compete.

**Fix:** The paper must either (a) derive an effective modal participation factor
that brings the theoretical prediction into agreement with the empirical data
(this would give a participation factor of ~0.24), or (b) abandon the theoretical
SDOF prediction in favor of the empirical ISO data alone, with proper error bars.
Do not present both as equally valid — the 3.75× gap must be explained.

### M3. Absolute transmissibility formula is wrong

**Severity: Major (incorrect vibration mechanics)**

In `mechanical_coupling.py`, line 137:
```python
x_abdomen_abs = x_base * (1 + H_rel)  # approx
```

This is **algebraically incorrect**. The absolute transmissibility for a SDOF
base-excited system is:

$$T_{abs}(r) = \sqrt{\frac{1 + (2\zeta r)^2}{(1-r^2)^2 + (2\zeta r)^2}}$$

At resonance (r = 1, ζ = 0.15):

$$T_{abs} = \frac{\sqrt{1 + 4\zeta^2}}{2\zeta} = \frac{\sqrt{1.09}}{0.3} = 3.48$$

The code computes 1 + H_rel = 1 + 3.33 = **4.33**, which is **24% too high**.

The error arises from adding the magnitudes of complex quantities:
X_mass = X_base + X_rel as phasors, but |X_mass| ≠ |X_base| + |X_rel| because at
resonance the relative displacement lags the base by ~90°. The correct relationship
is |X_mass| = |X_base| × T_abs = |X_base| × √(1 + H_rel² + 2H_rel·cos(φ))
where φ ≈ −π/2 at resonance, giving |X_mass| ≈ |X_base| × √(1 + H_rel²).

This error propagates to the `abdomen_absolute_um` output but does NOT affect
`relative_displacement_um`, which is the key mechanotransduction quantity. Still,
incorrect equations in a published paper are unacceptable.

**Fix:** Replace line 137 with the correct absolute transmissibility formula,
or at minimum clearly label it as an approximation and quantify the error.

### M4. Complete-sphere shell theory applied to an incomplete shell

**Severity: Major (questionable applicability of modal formulae)**

All the modal formulae — Lamb membrane stiffness λ_n (line 163), bending stiffness
K_bend (line 160), added mass m_added = ρ_f R/n (line 177), and pre-stress
stiffness K_prestress (line 170) — are derived for a **complete spherical shell**.

The abdomen is approximately a **half-shell** or partial shell. The posterior surface
is bounded by the vertebral column and paraspinal muscles. The superior boundary is
the diaphragm. The inferior boundary is the pelvic floor. Only the anterior-lateral
wall is a compliant shell.

For a partial shell with rigid boundaries:
1. **Mode shapes change fundamentally.** The complete-sphere Y_n^m harmonics do not
   satisfy the boundary conditions at the rigid boundaries. The actual mode shapes
   are some linear combination of Y_n^m, and the eigenfrequencies are different.
2. **The frequency multiplier approach (line 46 of parametric_analysis.py) is too
   crude.** Simply multiplying by 2.0 for "clamped" BCs has no rigorous basis for
   a partial shell. The actual factor depends on the angular extent of the free vs
   constrained boundary, the mode order, and the constraint type (pinned vs clamped).
3. **The added mass changes.** For a partial shell, the internal fluid volume is
   bounded by both compliant and rigid walls. The velocity field (and hence kinetic
   energy) differs from the complete-sphere case.

The parametric analysis (Section 5) acknowledges this with BC multipliers of 1.0–3.0,
but presents them as estimates from "structural dynamics literature" without citation.
For n=2 on a hemisphere clamped at the equator, I would expect the fundamental
frequency to increase by a factor of ~2.5–4.0 (not 1.3–2.2 as listed for realistic
cases), based on FEM studies of hemispherical shells.

**Fix:** Either (a) run a FEM calculation of the actual partial-shell geometry
(even a simplified FEniCS model would be far better than analytical guesswork), or
(b) cite specific references for the BC multipliers used, with uncertainty bounds.
The current estimates are essentially un-referenced assertions.

### M5. mechanotransduction.py still uses v1 model — numerical conclusions are wrong

**Severity: Major (known bug, unfixed)**

As acknowledged in the triage document, `mechanotransduction.py` (line 32) still
imports from v1:
```python
from analytical.natural_frequency import AbdominalModel, shell_modal_frequencies, breathing_mode_frequency
```

This means:
- The breathing mode frequency used is ~5.8 Hz (v1, wrong) instead of ~2900 Hz (v2)
- All SPL threshold calculations are based on the wrong resonance
- The "PIEZO activation at 120 dB" conclusion from this module is invalid

The v2 airborne pathway gives displacement of ~0.14 μm at 120 dB (from
`natural_frequency_v2.py`), which is **below** the PIEZO threshold of 0.5–2.0 μm.
The mechanotransduction module would predict ~28 μm at 120 dB using v1 physics —
a 200× error.

**Fix:** Migrate mechanotransduction.py to v2. This is listed as "next iteration"
in the triage but must be done before any review of quantitative claims.

---

## Moderate Issues (6)

### m1. Membrane stiffness dominates — regime validity concern

For the soft-tissue model (E = 0.1 MPa, R ≈ 0.157 m, h = 0.015 m), the stiffness
contributions for n=2 are approximately:
- K_bend ≈ 1,950 Pa/m (2.6%)
- K_memb ≈ 46,550 Pa/m (63%)
- K_prestress ≈ 25,480 Pa/m (34%)

Membrane stiffness dominates. This is physical for thin shells but raises a concern:
the Lamb formula λ_n was derived assuming classical thin shell theory (Kirchhoff-Love),
which requires h/R << 1. Here h/R ≈ 0.015/0.157 = 9.6%, which is at the boundary
of thin shell theory (typically valid for h/R < 5%).

At 10% thickness ratio, shear deformation and rotary inertia (Mindlin-Reissner
corrections) become non-negligible and can reduce frequencies by 10–20%.

**Recommendation:** Add a Mindlin-Reissner correction factor or bound the error.
For n=2, the correction is approximately:
f_thick/f_thin ≈ 1 / √(1 + n²(n+1)²h²/(12R²))
which for n=2, h/R=0.096 gives f_thick/f_thin ≈ 0.96 — only 4%. Minor for n=2 but
becomes significant for n ≥ 5.

### m2. Equivalent sphere approximation loses ellipsoidal mode splitting

Using R = (abc)^{1/3} as the equivalent sphere radius (line 57) collapses the
oblate ellipsoidal geometry into a single length scale. For a sphere, the n=2 mode
is 5-fold degenerate (m = −2,−1,0,1,2). For an oblate ellipsoid (c < a), this
degeneracy splits into distinct frequencies.

The m=0 mode (axisymmetric oblate-prolate along the short axis) has a different
frequency from the m=2 mode (equatorial deformation). The splitting is of order
(1 − c/a), which for c/a = 0.67 is ~33%. This means the n=2 frequencies span a
range, not a single value.

**Recommendation:** At minimum, estimate the splitting and present the frequency
as a range. Better: use an ellipsoidal shell analysis (Leissa, 1973).

### m3. Loss tangent Q relationship at high damping

The code uses Q = 1/tan δ, which is the small-damping approximation. For
tan δ = 0.3 (ζ = 0.15), this is adequate (error < 2%). But the parametric sweep
includes tan δ = 0.40, for which the exact relationship Q = 1/(2ζ) with
ζ = ½√(√(1+tan²δ) − 1) differs from tan δ/2 by ~4%. Not large, but should be
noted, especially since the parametric range could be extended to tan δ > 0.5 for
some soft tissues.

### m4. ISO 2631 transmissibility data sourcing

The ISO 2631 transmissibility table (lines 65–79 of `mechanical_coupling.py`) is
described as "approximate" and attributed to Kitazaki & Griffin (1998) and Mansfield
(2005). However:
1. No specific figure or table number is cited
2. The data appears to be hand-read or interpolated
3. The ISO 2631 standard itself does not provide transmissibility curves (it
   provides frequency weighting curves, which are different)
4. Kitazaki & Griffin report seat-to-*spine* transmissibility, not
   seat-to-*abdomen* specifically

The distinction between spine/pelvis transmissibility and abdomen transmissibility is
crucial. The abdominal organs can oscillate relative to the spine, which is the whole
point of the flexural mode model. Using spine transmissibility as abdomen
transmissibility conflates the input with the response.

**Recommendation:** Use original published data from Kitazaki & Griffin Fig. 4 or
Mansfield Table 3.2, with proper attribution. Distinguish between spine and viscera
measurements.

### m5. PIEZO threshold: displacement vs strain

The PIEZO activation threshold is cited as 0.5–2.0 μm displacement (line 164 of
`mechanical_coupling.py`), but PIEZO channels are activated by **membrane strain**,
not absolute displacement. The relevant quantity is the local strain in the
intestinal wall:

ε = Δξ / L_cell ≈ ξ / L_characteristic

where L_characteristic is the cell size (~10–50 μm for intestinal epithelium). A
wall displacement of 1 μm distributed over a cell of 20 μm gives a strain of 5%,
which is indeed in the PIEZO activation range. But the mapping from modal displacement
to local cell strain depends on the spatial wavelength of the deformation, the tissue
microstructure, and the mechanical coupling between the macroscopic shell mode and
the cellular-scale strain field.

The current model assumes ξ_modal ≈ ξ_cell, which is an upper bound.

**Recommendation:** Present the PIEZO threshold in terms of strain (ε > 1–5%) and
derive the modal-to-cellular strain transfer function, even if approximately.

### m6. Internal pressure estimate in mechanical_coupling.py

Line 145: `delta_P = model.rho_fluid * a_rel * R`

This is a dimensional estimate ΔP ~ ρ × a × L, which is the pressure scale for
an accelerating fluid column of length R. For a flexural mode, the internal pressure
distribution is NOT uniform — it has angular dependence following the mode shape.
The peak pressure occurs at antinodes and is zero at nodes.

Furthermore, the relevant R should be the radius of curvature of the mode shape, not
the cavity radius. For n=2, the effective length is R/2, not R.

**Recommendation:** Replace with the modal pressure formula:
ΔP_n = ρ_f × ω² × ξ × R / n for mode n.

---

## Minor Issues (5)

### µ1. Breathing mode added mass overestimated

In `breathing_mode_v2` (line 114), the effective fluid mass per unit area is
`m_eff = rho_wall*h + rho_fluid*R`. For a uniformly expanding sphere, the fluid
kinetic energy integral gives m_added = ρ_f × R / 3 per unit area, not ρ_f × R.
This overestimates the fluid added mass by 3×, which would increase the breathing
frequency by √3 ≈ 1.73. However, since the breathing mode is ≈ 2900 Hz (dominated
by K_fluid), and at this frequency kR ≈ 2.0 in the fluid, the incompressible
added mass formula breaks down anyway. The net effect on the breathing frequency is
modest and doesn't change the conclusion that it's in the kHz range. Note this
approximation in the text.

### µ2. Surface area property defined but never used in calculations

The `surface_area` property (v2, line 69) is correctly computed for an oblate
spheroid but is never referenced in any stiffness, mass, or energy calculation.
The energy budget (parametric_analysis.py line 147) uses `4πR²` instead. This is
fine as a leading-order approximation but should be noted.

### µ3. Magic number R_char = 0.16 in mechanotransduction.py

Line 160 of `mechanotransduction.py` hardcodes `R_char = 0.16` instead of
computing it from the model parameters. This will become stale or inconsistent when
the model geometry changes.

### µ4. Parametric analysis uses b = a throughout

All parametric models set b = a (axially symmetric oblate spheroid). The real
abdomen is tri-axial (a ≠ b ≠ c). While the equivalent-sphere approach absorbs this,
the sensitivity to asymmetry (b/a ≠ 1) should be noted as an unexplored dimension.

### µ5. Missing units in some docstrings

Several return dictionaries mix units without consistent annotation. For example,
`energy_budget_v2` returns `displacement_m` and `displacement_um` (good), but
`stiffness` fields in `flexural_mode_pressure_response` are labeled `stiffness_pa_m`
which is ambiguous (Pa/m? Pa·m?). The actual unit is Pa/m (stiffness per unit area).

---

## What v2 Gets Right (Credit Where Due)

1. **Breathing mode fix is correct and important.** The inclusion of fluid bulk
   modulus (k_fluid = 3K/R, line 109) moves the breathing mode from 5.8 Hz to
   ~2900 Hz. This is textbook fluid-structure interaction (Junger & Feit §8.2) and
   represents a genuine correction of a 176,000× stiffness omission in v1.

2. **Flexural mode physics is qualitatively sound.** For n ≥ 2, the fluid provides
   added mass (not volumetric stiffness), and the resulting frequencies fall in the
   1–25 Hz range depending on tissue properties. This is consistent with the
   biomechanics literature.

3. **Added mass formula m_added = ρ_f R/n for flexural modes is correct.** This
   is the standard result for incompressible flow inside a sphere with surface
   deformation proportional to Y_n (Lamb 1881, Junger & Feit §8.4).

4. **The (ka)^n coupling argument is directionally correct.** For a sphere in a
   long-wavelength acoustic field, the pressure distribution on the surface expands
   in spherical harmonics with coefficients proportional to (ka)^n. The n=2 mode
   sees only the quadrupolar component, which is O((ka)²) ≈ 1.6×10⁻⁴. This
   correctly identifies airborne coupling as extremely weak.

5. **The pre-stress term is physically appropriate.** Intra-abdominal pressure
   (1000 Pa ≈ 7.5 mmHg) provides tension stiffening that raises the flexural mode
   frequencies. The formula K_prestress = P/R × (n−1)(n+2) is the correct expression
   for a pressurized spherical shell (Kraus, 1967).

6. **The pivot to mechanical coupling is the right move.** Whole-body vibration at
   5–10 Hz through the skeleton is the physiologically relevant pathway. This
   bypasses the (ka)^n penalty entirely. The ISO 2631 literature supports resonance
   amplification of the abdominal contents at 4–8 Hz under WBV exposure.

7. **The parametric analysis is admirably comprehensive.** 486 parameter
   combinations spanning realistic ranges of E, geometry, thickness, and damping.
   The finding that only 37% of combinations give 5–10 Hz, and that relaxed
   musculature is required, is an honest and useful result.

8. **Transparent error correction process.** The research log trail from v1 through
   the devastating Round 1 review to v2 is exemplary scientific practice. The
   authors did not defend the indefensible — they fixed it.

---

## Assessment of Key Claims

### Claim 1: "Flexural modes (n≥2) ARE in the 5–10 Hz range"

**Verdict: PARTIALLY SUPPORTED.** For soft tissue (E = 0.05–0.2 MPa) with free
BCs, the n=2 mode falls at 3.2–5.6 Hz. With realistic boundary constraints
(×1.5–2.5), this becomes 5–14 Hz. The overlap with the 5–10 Hz "brown note" range
exists but is **not robust** — it requires specific combinations of soft tissue,
relaxed musculature, and moderate constraint. The paper's own parametric analysis
shows this: only 37% of combinations hit the 5–10 Hz window.

This is actually a nuanced and defensible position if framed correctly: "the n=2
flexural mode CAN fall in the 5–10 Hz range for specific body configurations,
consistent with the known inter-individual variability in WBV response."

### Claim 2: "Airborne coupling is orders of magnitude too weak"

**Verdict: SUPPORTED.** At 120 dB SPL, the predicted wall displacement via airborne
coupling is ~0.14 μm, well below the PIEZO threshold. Even at 140 dB (physically
dangerous), the displacement is only ~1.4 μm. The (ka)² factor of ~1.6×10⁻⁴ is
correct physics and makes airborne excitation of flexural modes negligible.

The energy budget violation (M1) actually makes this case **stronger** — the real
displacement would be even smaller than calculated.

### Claim 3: "Mechanical coupling is the real mechanism"

**Verdict: SUPPORTED IN PRINCIPLE, QUANTITATIVELY UNCERTAIN.** The basic argument
is correct: WBV at 5–10 Hz couples directly to the body at full amplitude, bypassing
the (ka)^n penalty. At occupational exposure levels (0.5–1.15 m/s²), the predicted
wall displacement is 1,600–7,200 μm (empirical/theoretical range), far exceeding
PIEZO thresholds.

However, the 3.7× discrepancy between theoretical and empirical predictions (M2)
means the quantitative conclusions have large uncertainty. The paper should present
the empirical estimate as primary and the theoretical as a consistency check, not
the other way around.

### Claim 4: "This explains ISO 2631 data and debunks airborne brown note"

**Verdict: REASONABLE BUT OVERSTATED.** The model is consistent with the frequency
range in ISO 2631 data, and the airborne/mechanical comparison is compelling. But
"debunks" is too strong without:
- A FEM or experimental validation of the actual abdominal flexural modes
- Resolution of the energy budget inconsistency
- A rigorous treatment of the partial-shell geometry

A fairer framing: "Our analysis provides quantitative evidence that the airborne
'brown note' is implausible, while mechanical whole-body vibration is a viable
pathway for GI effects in the 5–10 Hz range."

---

## Is This Publishable in Journal of Sound and Vibration?

**Not yet, but it is within reach.**

JSV requires rigorous mechanics, validated models, and careful uncertainty
quantification. The current state has:

| JSV Requirement | Status |
|---|---|
| Correct governing equations | ✅ Qualitatively correct |
| Validated against experiment/FEM | ❌ No validation |
| Self-consistent energy budget | ❌ 2× violation |
| Proper treatment of BCs | ❌ Crude multipliers |
| Uncertainty quantification | ⚠️ Parametric sweep but no formal UQ |
| Consistent codebase | ❌ mechanotransduction.py still uses v1 |
| Novel contribution | ✅ Airborne vs mechanical comparison is novel |
| Literature engagement | ✅ Good use of ISO 2631, Junger & Feit |

**Path to publication:**
1. Fix the energy budget inconsistency (M1) — 1 week
2. Resolve the theoretical/empirical discrepancy with a participation factor or
   effective Q (M2) — 1 week
3. Fix the absolute transmissibility formula (M3) — 1 hour
4. Run even a simple FEniCS model of a hemispherical shell to validate the BC
   multipliers (M4) — 2 weeks
5. Migrate mechanotransduction.py to v2 (M5) — 1 day
6. Add proper uncertainty bounds to all numerical claims — 1 week

Estimated effort to reach JSV-ready state: **4–6 weeks of focused work**.

---

## Specific Recommendations

1. **Frame the paper around the comparison.** The strongest contribution is the
   quantitative airborne-vs-mechanical comparison. Make this the central argument,
   not the modal frequencies per se.

2. **Use the empirical ISO data as primary evidence.** The SDOF theoretical model
   is useful for building intuition but should not carry quantitative weight. The
   empirical transmissibility data from Kitazaki & Griffin is far more credible.

3. **Add a FEM validation.** Even a linearized eigenvalue problem for a
   hemispherical shell with clamped boundary on a FEniCS mesh would enormously
   strengthen the paper. It would replace the crude BC multipliers with actual
   computed mode shapes and frequencies.

4. **Resolve the energy budget rigorously.** Use the Junger & Feit reciprocity
   formulation: the power absorbed by mode n from an incident plane wave is
   P_abs = (σ_abs × I) where σ_abs = (2n+1)λ²/(4π) × (Γ_rad / Γ_total), with
   Γ_rad being the radiation damping and Γ_total = Γ_rad + Γ_structural. For a
   bio-tissue shell at 5 Hz, Γ_rad << Γ_structural, so σ_abs is tiny — which
   further supports the "airborne is too weak" conclusion.

5. **Present results as ranges, not point estimates.** Given the sensitivity to E,
   geometry, BCs, and damping, single-number predictions are misleading. Report
   frequency bands and displacement ranges for realistic parameter distributions.

6. **Clean up the codebase.** Having mechanotransduction.py on v1 while everything
   else is on v2 is a latent source of error. All modules must use the same
   physical model.

---

## Summary Scorecard

| Category | Round 1 | Round 2 | Change |
|---|---|---|---|
| Fatal flaws | 4 | 0 | ✅ All resolved |
| Major issues | 5 | 5 | → New set (quantitative, not qualitative) |
| Moderate issues | 5 | 6 | → (different issues) |
| Minor issues | 3 | 5 | → (different issues) |
| Verdict | REJECT | MAJOR REVISION | ↑ Significant improvement |
| Publishable? | No | Not yet (4–6 weeks) | ↑ On track |

The authors have demonstrated the ability to take devastating criticism, find the
real physics, and rebuild. That is the hardest part. The remaining issues are
tractable engineering problems, not fundamental misconceptions. I look forward to
Round 3.

— Reviewer B
