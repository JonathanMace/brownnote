# Reviewer B — Round 1 Review

**Manuscript:** "Infrasound-Induced Resonance of the Human Abdominal Cavity: A Fluid-Filled Shell Model with Mechanotransduction Pathway Analysis"

**Date:** 2026-03-27

**Recommendation:** ❌ **REJECT** — Multiple fatal physics errors invalidate all quantitative claims.

---

## Summary

The authors model the human abdomen as a thin-walled oblate spheroidal shell
filled with incompressible fluid and compute natural frequencies, acoustic
coupling, and mechanotransduction thresholds. The headline claims are that the
breathing mode falls at 5.8 Hz, that only 80 dB SPL is needed to produce 1 μm
tissue displacement, and that the "corrected" coupling model predicts 231×
larger displacements than a naïve free-field estimate. I identify at least
**four fatal errors** that, individually, each invalidate the main conclusions,
plus several major and moderate issues. Until these are resolved, no
quantitative claim in this work should be trusted.

---

## 🔴 FATAL FLAW #1: Breathing Mode Stiffness Omits Fluid Bulk Modulus

**This is the most serious error in the entire study.**

The breathing mode frequency is computed in `natural_frequency.py` (lines 89–101)
as:

```python
k_eff = 2 * E * h / (R**2 * (1 - nu))      # membrane stiffness only
m_eff = rho_w * h + rho_f * R               # wall mass + fluid added mass
omega = np.sqrt(k_eff / m_eff)
```

This formulation uses the **membrane stiffness alone** and completely omits the
**volumetric stiffness of the contained fluid**.

For the breathing mode (n = 0), radial shell displacement ξ produces a
volumetric strain ΔV/V = 3ξ/R, which compresses the contained fluid. The
resulting pressure increment is:

$$\Delta p_\text{fluid} = K_f \cdot \frac{3\xi}{R}$$

This acts as an **additional restoring force**, giving a fluid stiffness
contribution:

$$k_\text{fluid} = \frac{3 K_f}{R}$$

With the authors' own parameters (K_f = 2.2 GPa, R = 0.157 m):

| Quantity | Value |
|---|---|
| k_membrane (code) | 238,000 Pa/m |
| k_fluid (omitted) | **4.20 × 10¹⁰ Pa/m** |
| **Ratio** | **k_fluid / k_membrane = 176,000×** |

The fluid stiffness exceeds the membrane stiffness by **five orders of
magnitude**. The correct breathing mode frequency is:

$$f_0 = \frac{1}{2\pi}\sqrt{\frac{k_\text{membrane} + k_\text{fluid}}{m_\text{eff}}}$$

**Independent computation:**

- Code (membrane only): **f₀ = 5.80 Hz**
- Correct (with fluid K): **f₀ ≈ 2,435 Hz**

The breathing mode of a water-filled shell at these dimensions is in the
**kilohertz range**, not at 5–10 Hz. The entire "brown note resonance"
conclusion collapses.

This error arises from conflating **external** fluid loading (where the fluid
adds mass but not stiffness for n = 0) with **internal** fluid loading (where
the fluid's bulk modulus dominates the restoring force). The Junger & Feit
formulation the code references is for shells **submerged in** fluid, not
**filled with** fluid. The physics is fundamentally different: a contained
fluid that must compress under volumetric deformation is a stiff spring, not
an added mass.

**Consequence:** All frequency results for n = 0 are wrong by a factor of
~420. No mode of this system falls near 5–10 Hz due to this mechanism.

---

## 🔴 FATAL FLAW #2: The "Full Incident Pressure Drives the Shell" Argument Is Wrong

The core argument of `acoustic_coupling.py` (docstring, lines 6–27; code,
lines 205–206) is:

> "In the long-wavelength limit, the FULL incident pressure acts on the shell."

And the displacement is computed (line 206) as:

```python
xi = p_inc / k_per_area * H_mag
```

This treats the shell as if one side has the incident pressure and the other
side has **vacuum** — i.e., the shell is an empty pressure vessel.

**But the shell is filled with nearly incompressible fluid.** In the
long-wavelength limit (ka = 0.017 ≪ 1), the pressure field is spatially
uniform. This means the same oscillating pressure acts on **both sides** of
the shell membrane simultaneously:

- Exterior: p_inc (incident pressure)
- Interior: ≈ p_inc (the pressure wave penetrates the thin, soft shell and
  pressurizes the contained fluid)

The net driving force on the shell wall is the **pressure differential**, which
is approximately:

$$\Delta p \approx p_\text{inc} \times O\bigl((ka)^2\bigr)$$

For ka = 0.017: Δp ≈ p_inc × 2.9 × 10⁻⁴, reducing the effective drive by
a factor of ~3,400.

The pendulum analogy in the docstring (line 27) is misleading. A pendulum has
a **rigid pivot** that provides the reaction force. Here, there is no rigid
boundary — the pressure acts uniformly everywhere. A correct analogy: try to
squeeze a water balloon by placing it in a pressure chamber. The balloon
doesn't deform because the internal and external pressures equalize.

**Consequence:** The driving force is overestimated by ~3,400×. Combined with
Fatal Flaw #1, the displacement is overestimated by a factor of at least
**10⁵–10⁶**.

---

## 🔴 FATAL FLAW #3: The Shell Is Not in Air — It Is Embedded in Tissue

The entire acoustic coupling model assumes the shell radiates into (and is
driven by) **air** (lines 47–49: `RHO_AIR = 1.225`, `C_AIR = 343.0`).

In reality, the abdominal cavity is bounded by:

| Direction | Structure | Medium |
|---|---|---|
| Anterior | Abdominal wall → subcutaneous fat → skin → air | Last ~1 cm is air |
| Posterior | Spine, psoas muscles, retroperitoneum | **Tissue/bone** |
| Lateral | Oblique/transversus muscles, body wall | **Tissue** |
| Superior | Diaphragm → thoracic cavity | **Tissue/air** |
| Inferior | Pelvic floor, iliac bones | **Tissue/bone** |

Roughly **80–90% of the shell surface faces tissue, not air.** The external
acoustic impedance should be Z_tissue ≈ 1.6 × 10⁶ Pa·s/m for most of the
surface, not Z_air ≈ 420 Pa·s/m.

This has two critical consequences:

1. **Radiation damping is NOT negligible.** The code computes ζ_rad = 3.67 ×
   10⁻⁶ (line 278 of output) using air properties. With tissue exterior,
   ζ_rad would be ~3,600× larger (proportional to ρc of the exterior medium).
   This would dominate or compete with structural damping.

2. **The shell is acoustically transparent.** When both the internal and
   external media have similar impedance (~1.6 MRayl), the thin shell is
   essentially invisible to the wave. Sound passes through without
   significant interaction. There is no mechanism for resonant energy buildup.

**Consequence:** The radiation damping estimate, the energy absorption
calculation, and the assumed driving mechanism are all qualitatively wrong.

---

## 🔴 FATAL FLAW #4: Energy Budget Is Violated

Even accepting the code's own framework for the sake of argument, the energy
accounting fails catastrophically.

At 100 dB SPL and 5.8 Hz:

| Quantity | Value |
|---|---|
| Acoustic intensity | 9.5 × 10⁻³ W/m² |
| Power intercepted (πR²) | 7.4 × 10⁻⁴ W |
| Rayleigh absorption efficiency (ka)⁴ | 7.8 × 10⁻⁸ |
| Estimated absorbed power | **5.8 × 10⁻¹¹ W** |
| Power dissipated at claimed 28 μm amplitude | **3.2 × 10⁻⁴ W** |
| **Ratio (dissipated / absorbed)** | **5.5 × 10⁶** |

The claimed oscillation would require **5.5 million times more power** than
the sound field can deliver to the shell in the Rayleigh scattering regime.

The code computes an energy absorption fraction (lines 219–225) but this
calculation contains a **dimensional error**: `P_absorbed` is computed as
intensity (W/m²) while `P_intercepted` is total power (W), making their ratio
dimensionally inconsistent.

---

## 🟡 MAJOR ISSUE #5: Membrane Stiffness Gives an Unphysical Shell

With E = 0.1 MPa and the model geometry, the membrane stiffness is k ≈ 238,000
Pa/m. The static deformation of this shell under atmospheric pressure would be:

$$\xi_\text{atm} = \frac{p_\text{atm}}{k} = \frac{101{,}325}{238{,}000} = 0.43\ \text{m} = 43\ \text{cm}$$

An empty shell with these properties would **collapse under its own weight**.
It cannot exist without the internal fluid pressure for support. This
immediately tells us the breathing mode MUST include the fluid's
compressibility as a restoring force (cf. Fatal Flaw #1).

The fact that this shell would deform 43 cm under 1 atm but supposedly
deforms only 28 μm under 2 Pa is not a contradiction — it's self-consistent
within the model's own (flawed) framework. But it should have raised a flag
that the model is treating the shell as a structure that cannot physically
exist in the configuration assumed.

---

## 🟡 MAJOR ISSUE #6: Binary Search Bug Floors All Thresholds at 80 dB

In `acoustic_coupling.py` (lines 336–345), the binary search for the PIEZO
activation threshold uses:

```python
spl_lo, spl_hi = 80.0, 200.0
```

The lower bound of 80 dB means any true threshold below 80 dB will be reported
as 80 dB. **All four rows of the output table report "SPL for 1μm = 80.0 dB"
because the true thresholds (65–74 dB) fall below the search floor.**

Independent verification:

| tan(δ) | Q | True SPL for 1 μm | Code reports |
|---|---|---|---|
| 0.15 | 6.7 | **65.0 dB** | 80.0 dB |
| 0.20 | 5.0 | **67.5 dB** | 80.0 dB |
| 0.30 | 3.3 | **71.0 dB** | 80.0 dB |
| 0.40 | 2.5 | **73.5 dB** | 80.0 dB |

The fact that the "corrected" model predicts PIEZO activation at 65 dB SPL
(quieter than normal conversation) should have been recognized as a
**reductio ad absurdum** invalidating the model, not celebrated as a result.
Billions of people are exposed to 65 dB daily without gastrointestinal effects.

---

## 🟡 MAJOR ISSUE #7: Q² Error in Pressure-from-Displacement Function

In `mechanotransduction.py`, the function `pressure_from_displacement`
(lines 140–162) computes:

```python
delta_p = params.rho_tissue * (2 * np.pi * freq)**2 * xi_m
delta_p_resonant = delta_p * Q    # line 159
```

The calling code (line 256) passes `xi_res = xi_free * Q_val * 1e6` — a
displacement **already amplified by Q**. The function then multiplies by Q
**again**, producing a Q² error.

For Q = 5, the reported internal pressures are **5× too large**. The output
table "RESONANT INTERNAL PRESSURE AT VARIOUS SPL" is therefore wrong.

---

## 🟡 MAJOR ISSUE #8: PIEZO Threshold Comparison Remains Apples-to-Oranges

The prior review (Reviewer A, 2026-03-27T04:15) correctly flagged this. The
code in `acoustic_coupling.py` (line 354) acknowledges the issue:

> "This is BULK strain, not localized indentation"

But then proceeds to compare the numbers anyway. The PIEZO1/PIEZO2 activation
thresholds (0.5–2.0 μm) come from patch-clamp experiments where a glass
pipette directly indents a single cell membrane over an area of ~1 μm². The
model computes bulk radial displacement of a macroscopic shell. The
relationship between these two quantities depends on:

- Tissue microstructure and strain concentration
- Cell orientation relative to the displacement field
- The frequency-dependent viscoelastic transfer function from bulk to
  cellular scale
- Whether the oscillation is compressive or shear at the cellular level

None of these are addressed. Without a multiscale model bridging macroscopic
shell displacement to cellular membrane deformation, the comparison is
quantitatively meaningless.

---

## 🟡 MAJOR ISSUE #9: Boundary Conditions Entirely Ignored

The shell model assumes a free, unconstrained shell (`natural_frequency.py`
uses standard Lamb/Junger-Feit for a free sphere). The real abdominal cavity
is:

- **Posteriorly constrained** by the lumbar spine (rigid)
- **Superiorly constrained** by the rib cage (semi-rigid) and diaphragm
  (flexible)
- **Inferiorly constrained** by the pelvis (rigid)
- Connected to the thoracic cavity via the esophageal hiatus

These constraints eliminate certain mode shapes (particularly those requiring
displacement at the constrained boundaries) and significantly raise the
frequencies of surviving modes. A hemispherical shell clamped at its equator
has natural frequencies roughly 2–3× higher than the corresponding free shell.
For the abdomen, where constraints exist on multiple boundaries, the effect is
even larger.

---

## 🟠 MODERATE ISSUES

### M1: Dimensional Error in Energy Absorption (acoustic_coupling.py, lines 219–225)

```python
P_absorbed = radiation_impedance_sphere(...).real * velocity**2 / (4 * np.pi * R**2)
P_intercepted = P_incident * cross_section
absorption = P_absorbed / P_intercepted
```

`P_absorbed` has units of W/m² (intensity); `P_intercepted` has units of W
(power). Their ratio has units of m⁻² and is not a valid efficiency. The
correct absorbed power is `½ × R_rad × v²` (total, not per unit area, and
time-averaged).

### M2: The 231× "Correction Factor" Is an Artifact

The comparison between "naïve" and "corrected" models at resonance
(`acoustic_coupling.py`, lines 299–323) shows a constant 231× ratio. This
ratio is simply:

$$\frac{\xi_\text{corrected}}{\xi_\text{naive}} = \frac{p / k_\text{shell}}{p / (\rho_f c_f \omega)} \times \frac{Q_\text{eff}}{Q_\text{eff}} = \frac{\rho_f c_f \omega}{k_\text{shell}}$$

This is not a physics insight — it's the ratio of the tissue acoustic stiffness
to the (unrealistically low) shell membrane stiffness. The Q factors cancel.
The large ratio reflects the fact that the shell is absurdly soft (cf. Major
Issue #5), not that the coupling physics has been improved.

### M3: E = 0.1 MPa Is at the Extreme Low End

The model achieves the 5.8 Hz target by using E = 0.1 MPa (relaxed, passive
tissue). Published values for the composite abdominal wall:

| Source | Condition | E (MPa) |
|---|---|---|
| Hernandez-Gascon et al. (2013) | Passive linea alba | 0.05–0.5 |
| Forstemann et al. (2011) | In-vivo, relaxed | 0.2–1.0 |
| Brown & McGill (2009) | Activated muscle | 5–30 |
| Tran et al. (2014) | Composite (in-vivo) | 0.5–2.0 |

The choice of E = 0.1 MPa represents a **fully relaxed, untensed** abdominal
wall — essentially a person lying supine with zero muscle tone. Most waking
postures involve some degree of abdominal bracing. The sensitivity analysis
shows that doubling E to 0.2 MPa already shifts the (incorrectly computed)
frequency above 8 Hz, and physiologically realistic values (0.5–2 MPa) move
it far out of the infrasound range.

### M4: Loss Tangent Values Are Uncertain

The structural damping ratio uses tan(δ) = 0.3 as a default
(`acoustic_coupling.py`, line 144). The cited range (0.15–0.40) is for
**small-amplitude, quasi-static** measurements. At the frequencies and strain
rates relevant here (5–10 Hz, cyclic), viscoelastic tissue may exhibit:

- Frequency-dependent stiffening (storage modulus increases with frequency)
- Nonlinear damping at large strains
- Thixotropic effects from sustained oscillation

The Q factor could easily differ by 2–3× from the assumed value in either
direction, propagating linearly into displacement estimates.

### M5: Internal Organ Heterogeneity

The model treats abdominal contents as a uniform fluid. In reality, the
abdomen contains:

- Liver (right upper quadrant, ~1.5 kg, solid)
- Stomach and intestines (varying solid/gas/liquid)
- Kidneys (retroperitoneal, solid)
- Mesentery (complex folded membrane)
- Variable quantities of gas (bowel gas changes resonance dramatically)

The presence of gas pockets (Z ≈ 400 vs. tissue Z ≈ 1.6 × 10⁶) creates
dramatic impedance discontinuities that would scatter internal waves and
prevent any coherent cavity resonance.

---

## 🔵 MINOR ISSUES

### m1: No Validation Against Any Data

- No comparison with Elaikh's published oblate spheroid frequencies
- No comparison with ISO 2631-1 whole-body vibration resonance data (which
  places whole-body vertical resonance at 4–8 Hz for seated posture — but
  this is a **whole-body** resonance driven by skeletal mechanics, not a
  cavity resonance)
- No comparison with published abdominal vibration measurements
- No comparison with cadaver or phantom experiments

### m2: Missing Physical Effects

- **Gravity**: The abdominal contents exert a hydrostatic pressure gradient
  (~1 kPa over 15 cm height). This pre-stresses the shell non-uniformly and
  breaks the symmetry assumed in the breathing mode.
- **Respiration**: The diaphragm moves 1–10 cm during breathing at 0.2–0.3
  Hz. This is a vastly larger displacement than any acoustic effect, and it
  continuously modulates the cavity geometry and internal pressure.
- **Posture**: Supine vs. standing changes the effective geometry, boundary
  conditions, hydrostatic loading, and muscle activation. None discussed.
- **Clothing**: Tight clothing (belts, waistbands) adds external constraint
  and changes both stiffness and damping.

### m3: The `mechanotransduction.py` Module Uses Tissue Impedance Inconsistently

In `find_piezo_activation_threshold` (line 134), the displacement is computed
using tissue acoustic impedance (ρ_tissue × c_tissue = 1.6 MRayl), which gives
the **free-field tissue displacement**. But in `acoustic_coupling.py`, the
displacement is computed from shell mechanics (p / k_shell × H). These are
completely different models giving answers that differ by 231×. The two modules
are **mutually contradictory** and cannot both be correct.

### m4: Code Quality

- `sys.path.insert(0, ...)` manipulations (lines 30–32 of
  `mechanotransduction.py`, lines 41–42 of `acoustic_coupling.py`) are fragile.
  Use proper package installation.
- No unit tests for any computation.
- No docstrings on `CouplingResult` fields explaining sign conventions or
  reference frames.

---

## Summary of Errors and Their Impact

| # | Error | Impact on Displacement | Impact on Frequency |
|---|---|---|---|
| F1 | Missing fluid K in stiffness | — | f₀ wrong by ~420× |
| F2 | Full p_inc as drive (vs. Δp) | ~3,400× overestimate | — |
| F3 | Air exterior (vs. tissue) | Qualitatively wrong coupling | — |
| F4 | Energy budget violated | 5.5 × 10⁶× impossible | — |
| M5 | Binary search floor | Hides absurd 65 dB threshold | — |
| M7 | Q² in pressure calc | 5× error in internal pressure | — |

**Cumulative effect of F1 + F2 alone:** displacements are overestimated by a
factor of approximately **10⁵–10⁶**. The "28 μm at 100 dB" becomes
**0.03–0.3 pm** — far below any biological threshold.

---

## Recommendations

1. **Derive the breathing mode properly** including the bulk modulus of the
   contained fluid. The result will be kilohertz, not hertz. Look for
   **non-volumetric modes** (n ≥ 2 flexural/sloshing modes) that can exist at
   low frequencies — these do not require fluid compression.

2. **Model the correct boundary value problem.** The driving force is not
   p_inc but the scattering-induced pressure differential. For a fluid-filled
   elastic shell embedded in tissue, use a full coupled acoustic-elastic
   formulation (e.g., Junger & Feit Ch. 9, or a FEA model in COMSOL/Abaqus).

3. **Use realistic exterior medium properties.** Replace air with tissue for
   the radiation impedance and scattering calculations. Only the anterior
   surface sees air (through skin/fat layers).

4. **Validate against SOMETHING.** Even a simple comparison with a water-filled
   rubber balloon experiment would provide a sanity check on the coupled
   shell-fluid dynamics.

5. **If the goal is to explain the brown note**, consider mechanisms that don't
   require cavity resonance: whole-body vibration (skeletal transmission),
   chest wall compliance, diaphragm-mediated pressure transmission, or
   direct vagal nerve stimulation via mechanical vibration of the torso.

---

**Reviewer B**
*25 years in computational acoustics and fluid-structure interaction*
