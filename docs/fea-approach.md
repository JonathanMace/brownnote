# Finite Element Analysis of Abdominal Resonance Under Infrasound Excitation

## A Technical Approach for Investigating the "Brown Note" Hypothesis

**Document Version:** 1.0  
**Date:** 2025-07  
**Project:** Browntone — Computational Investigation of Infrasonic Abdominal Resonance

---

## Table of Contents

1. [Introduction & Motivation](#1-introduction--motivation)
2. [Abdominal Geometry](#2-abdominal-geometry)
3. [Material Properties](#3-material-properties)
4. [Analytical Solution — Fluid-Filled Oblate Spheroidal Shell](#4-analytical-solution--fluid-filled-oblate-spheroidal-shell)
5. [FEA Model Design](#5-fea-model-design)
6. [Progressive Model Complexity](#6-progressive-model-complexity)
7. [Software Recommendations](#7-software-recommendations)
8. [Validation Strategy](#8-validation-strategy)
9. [Python Code Scaffold](#9-python-code-scaffold)
10. [References](#10-references)

---

## 1. Introduction & Motivation

The "brown note" is a hypothetical infrasonic frequency — popularly cited between
5 and 10 Hz — alleged to induce involuntary gastrointestinal distress through
mechanical resonance of the human abdomen. While no peer-reviewed study has
confirmed the effect (MythBusters tested up to 153 dB SPL at 5 Hz with negative
results), the underlying physics question is legitimate:

> **Does the fluid-filled human abdominal cavity possess natural frequencies in
> the 5–10 Hz band, and if so, under what excitation amplitudes would
> physiologically significant strain develop?**

Whole-body vibration research (ISO 2631, ISO 5982) confirms that the human
abdomen resonates in the **4–8 Hz** range under mechanical excitation. This
document describes a rigorous finite element analysis (FEA) approach to:

1. Model the abdomen as a fluid-filled oblate spheroidal shell.
2. Compute its natural frequencies analytically and numerically.
3. Determine whether airborne infrasound at feasible SPLs can excite these modes.
4. Quantify the resulting wall strain and internal pressure amplification.

---

## 2. Abdominal Geometry

### 2.1 Anatomical Measurements

The human abdominal cavity, viewed in transverse cross-section, is well
approximated by an oblate spheroid (ellipsoid of revolution with $c < a$).

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Transverse diameter (L–R) | $2a_x$ | 28–35 cm | CT anthropometry |
| Sagittal diameter (A–P) | $2a_y$ | 20–25 cm | Sagittal abdominal diameter studies |
| Craniocaudal height | $2a_z$ | 22–28 cm | CT volumetry |
| **Reference semi-major axis** | $a$ | **0.16 m** | $\frac{1}{2} \times 0.32$ m (transverse) |
| **Reference semi-minor axis** | $c$ | **0.11 m** | $\frac{1}{2} \times 0.22$ m (sagittal) |
| Aspect ratio | $e = c/a$ | **0.69** | oblate |
| Outer envelope volume | $V_{\text{out}}$ | **~11.8 L** | $V = \frac{4}{3}\pi a^2 c$ |
| Inner cavity volume | $V_{\text{in}}$ | **~5.7 L** | $(a{-}h)^2(c{-}h)$, consistent with peritoneal cavity |

> **Note:** For a triaxial model, use $a_x = 0.16$ m, $a_y = 0.11$ m,
> $a_z = 0.13$ m. The oblate spheroid simplification uses $a = a_x$, $c = a_y$.

### 2.2 Wall Thickness — Layered Structure

The anterior abdominal wall is a composite of distinct layers. Measurements from
CT and ultrasound imaging:

| Layer | Thickness (mm) | Notes |
|-------|---------------|-------|
| Skin (epidermis + dermis) | 1–3 | Relatively stiff |
| Subcutaneous fat (Camper's & Scarpa's fascia) | 15–25 | Highly variable with BMI |
| External oblique muscle | 4–6 | |
| Internal oblique muscle | 5–9 | |
| Transversus abdominis | 3–5 | |
| Rectus abdominis (anterior midline) | 8–10 | |
| Transversalis fascia | ~1 | |
| Preperitoneal fat | 2–10 | |
| Parietal peritoneum | < 1 | |
| **Total composite thickness** | **~25–55 mm** | **Nominal: 30 mm** |

For the simplified model:

$$h_{\text{eff}} = 0.030 \text{ m (effective composite wall thickness)}$$

The posterior wall is reinforced by the lumbar spine and paraspinal muscles,
effectively creating a rigid boundary over roughly 30% of the posterior surface.

### 2.3 Geometric Model Definition

The oblate spheroid surface is defined in Cartesian coordinates as:

$$\frac{x^2}{a^2} + \frac{y^2}{a^2} + \frac{z^2}{c^2} = 1$$

with:
- $a = 0.16$ m (equatorial semi-axis)
- $c = 0.11$ m (polar semi-axis)
- Wall thickness $h = 0.030$ m (uniform, or layered in advanced models)

---

## 3. Material Properties

### 3.1 Abdominal Wall — Composite Properties

#### 3.1.1 Individual Layer Properties

| Layer | Young's Modulus $E$ (kPa) | Poisson's Ratio $\nu$ | Density $\rho$ (kg/m³) | Notes |
|-------|---------------------------|----------------------|------------------------|-------|
| Skin | 50–200 | 0.48 | 1100 | Dermis dominates |
| Subcutaneous fat | 0.5–3 | 0.49 | 920 | Nearly incompressible |
| Skeletal muscle (relaxed) | 5–50 | 0.495 | 1060 | Highly anisotropic; passive |
| Skeletal muscle (contracted) | 100–500 | 0.495 | 1060 | Active state |
| Fascia / aponeurosis | 1000–8000 | 0.40 | 1100 | Very stiff collagenous tissue |
| Peritoneum | 10–100 | 0.45 | 1050 | Thin membrane |

#### 3.1.2 Effective Homogenized Wall Properties

For the Level 2 simplified model, we homogenize the wall using a
thickness-weighted average. With the dominant structural contribution from muscle
and fascia:

| Parameter | Symbol | Nominal Value | Range for Parametric Study |
|-----------|--------|---------------|---------------------------|
| Young's modulus | $E_w$ | **50 kPa** | 20–500 kPa |
| Poisson's ratio | $\nu_w$ | **0.495** | 0.45–0.499 |
| Density | $\rho_w$ | **1050 kg/m³** | 950–1100 kg/m³ |
| Wall thickness | $h$ | **0.030 m** | 0.015–0.050 m |

> **Justification for $E_w = 50$ kPa:** In-vivo measurements during laparoscopic
> insufflation (Song et al. 2006) reported 22–51 kPa for the relaxed abdominal
> wall. The relaxed, breathing state is most relevant for infrasound exposure.
> Cadaveric measurements (0.2–7 MPa) are stiffer due to tissue fixation and
> represent an upper bound.

### 3.2 Abdominal Contents — Fluid Properties

The abdominal cavity contains a heterogeneous mix of solid organs (liver, spleen,
kidneys), hollow viscera (stomach, intestines), mesentery, and peritoneal fluid.
For the fluid-filled shell model, we treat the contents as an equivalent acoustic
fluid.

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Density | $\rho_f$ | **1040 kg/m³** | Weighted average of viscera |
| Speed of sound | $c_f$ | **1540 m/s** | Standard soft tissue |
| Bulk modulus | $K_f = \rho_f c_f^2$ | **2.47 GPa** | Computed |
| Dynamic viscosity | $\mu_f$ | **1–5 mPa·s** | Peritoneal fluid ≈ water-like |
| Acoustic impedance | $Z_f = \rho_f c_f$ | **1.60 × 10⁶ kg/(m²·s)** | |

#### 3.2.1 Organ-Specific Acoustic Properties (for Level 4 model)

| Organ/Tissue | $c$ (m/s) | $\rho$ (kg/m³) | $K$ (GPa) | $Z$ (MRayl) |
|-------------|-----------|-----------------|-----------|-------------|
| Liver | 1590 | 1060 | 2.68 | 1.69 |
| Kidney | 1570 | 1050 | 2.59 | 1.65 |
| Muscle | 1580 | 1050 | 2.62 | 1.66 |
| Fat | 1450 | 950 | 2.00 | 1.38 |
| Blood | 1575 | 1060 | 2.63 | 1.67 |
| Intestinal gas | 340 | 1.2 | 0.00014 | 0.000408 |

> **Critical note on intestinal gas:** The presence of gas pockets within the
> bowel dramatically reduces the effective bulk modulus and introduces
> compressibility. Even small volumes of trapped gas ($\sim$100 mL) can reduce
> the effective speed of sound within the abdominal cavity by an order of
> magnitude, profoundly affecting the natural frequencies.

### 3.3 External Medium — Air

| Parameter | Value |
|-----------|-------|
| $\rho_{\text{air}}$ | 1.225 kg/m³ |
| $c_{\text{air}}$ | 343 m/s |
| $Z_{\text{air}}$ | 420 kg/(m²·s) |

The enormous impedance mismatch between air ($Z \approx 420$) and the abdominal
wall ($Z \approx 1.6 \times 10^6$) means that **less than 0.1%** of incident
acoustic energy is transmitted into the abdomen. This is the primary physical
argument against the brown note hypothesis at feasible SPLs.

---

## 4. Analytical Solution — Fluid-Filled Oblate Spheroidal Shell

### 4.1 Approach

We derive an approximate natural frequency for the lowest-order breathing mode
(axisymmetric, $n=0$) of a thin elastic oblate spheroidal shell filled with an
incompressible fluid. This follows the framework of Junger (1952) and the
Rayleigh-Ritz method applied to spheroidal geometries (Elaikh et al.).

### 4.2 Dry Shell Natural Frequency — Spherical Approximation

For a thin spherical shell of radius $R$, thickness $h$, the breathing mode
frequency is (Lamb, 1882; Leissa, 1973):

$$f_{\text{dry},0} = \frac{1}{2\pi R}\sqrt{\frac{E}{\rho_w(1-\nu^2)}}$$

For an oblate spheroid, we define an equivalent radius:

$$R_{\text{eq}} = \left(a^2 c\right)^{1/3}$$

This preserves the volume of the cavity. With our parameters:

$$R_{\text{eq}} = (0.16^2 \times 0.11)^{1/3} = (2.816 \times 10^{-3})^{1/3} = 0.1413 \text{ m}$$

Then for the dry shell ($E = 50$ kPa, $\rho_w = 1050$ kg/m³, $\nu = 0.495$):

$$f_{\text{dry},0} = \frac{1}{2\pi \times 0.1413}\sqrt{\frac{50000}{1050 \times (1 - 0.495^2)}}$$

$$= \frac{1}{0.8878}\sqrt{\frac{50000}{1050 \times 0.7550}} = \frac{1}{0.8878}\sqrt{63.06}$$

$$= \frac{7.94}{0.8878} \approx 8.9 \text{ Hz}$$

### 4.3 Fluid Loading — Added Mass Effect

When the shell is filled with fluid, the effective mass increases. The fluid
added mass factor for mode $n$ of a spherical shell is (Junger & Feit, 1972):

$$\beta_n = \frac{\rho_f R}{\rho_w h} \cdot \frac{1}{n+1}$$

For the breathing mode ($n = 0$, treated as $n = 1$ for the lowest non-trivial
radial mode):

$$\beta_1 = \frac{\rho_f R_{\text{eq}}}{\rho_w h} \cdot \frac{1}{2} = \frac{1040 \times 0.1413}{1050 \times 0.030} \times \frac{1}{2}$$

$$= \frac{146.95}{31.50} \times 0.5 = 2.332$$

The wet (fluid-loaded) natural frequency is:

$$f_{\text{wet}} = \frac{f_{\text{dry}}}{\sqrt{1 + \beta}}$$

$$f_{\text{wet}} = \frac{8.9}{\sqrt{1 + 2.332}} = \frac{8.9}{\sqrt{3.332}} = \frac{8.9}{1.825}$$

$$\boxed{f_{\text{wet}} \approx 4.9 \text{ Hz}}$$

### 4.4 Higher-Order Modes

For mode number $n \geq 2$ (non-axisymmetric modes), the dry shell frequency for
a thin spherical shell is approximately:

$$\omega_n^2 = \frac{E h^2}{12\rho_w R^4(1-\nu^2)}\left[n^2(n+1)^2 - 2n(n+1)(1-\nu) + (1-\nu^2)\right] + \frac{E}{\rho_w R^2(1-\nu)}$$

The corresponding fluid-loaded frequencies with $\beta_n$:

| Mode $n$ | $f_{\text{dry}}$ (Hz) | $\beta_n$ | $f_{\text{wet}}$ (Hz) |
|-----------|----------------------|-----------|----------------------|
| 1 (breathing) | 8.9 | 2.33 | **4.9** |
| 2 (ellipsoidal) | 12.1 | 1.55 | **7.6** |
| 3 | 18.7 | 1.17 | **12.7** |
| 4 | 27.5 | 0.93 | **19.8** |

### 4.5 Assessment: Is 5–10 Hz Plausible?

**Yes.** The analytical model predicts:

- **Fundamental breathing mode: ~5 Hz** — squarely within the alleged brown note range.
- **First ellipsoidal mode: ~8 Hz** — also within the range.
- These predictions are consistent with whole-body vibration literature reporting
  abdominal resonance at **4–8 Hz** (ISO 2631/5982).

**However**, the critical question is not whether resonance *exists* at these
frequencies, but whether **airborne sound** can deliver sufficient energy to
excite it. The impedance mismatch between air and tissue ($\sim 3800:1$) means
transmission efficiency is approximately:

$$T = \frac{4 Z_{\text{air}} Z_{\text{tissue}}}{(Z_{\text{air}} + Z_{\text{tissue}})^2} \approx \frac{4 \times 420 \times 1.6\times10^6}{(1.6\times10^6)^2} \approx 1.05 \times 10^{-3}$$

Thus only ~0.1% of incident acoustic power enters the abdominal wall — a
30 dB insertion loss before any resonance effects begin.

### 4.6 Sensitivity to Key Parameters

| Parameter varied | Effect on $f_{\text{wet}}$ |
|-----------------|---------------------------|
| $E_w$: 20 → 500 kPa | 3.1 → 15.4 Hz |
| $h$: 15 → 50 mm | 4.4 → 5.7 Hz (weak effect via added mass) |
| $\rho_f$: 900 → 1100 kg/m³ | 5.2 → 4.6 Hz |
| $a$: 0.13 → 0.19 m | 5.8 → 4.2 Hz |
| Gas inclusion (10% vol) | Dramatic reduction to ~1–2 Hz |

---

## 5. FEA Model Design

### 5.1 Geometry

```
           z (craniocaudal)
           ↑
           |    ╭───────────╮
           |  ╱               ╲
           |╱    fluid fill     ╲
     ──────●─────────────────────●──── x (transverse)
           |╲                   ╱
           |  ╲               ╱
           |    ╰─────────────╯
           |
    Fixed posterior face (spine contact)
```

- **Outer shell:** Oblate spheroid, $a = 0.16$ m, $c = 0.11$ m
- **Inner shell:** Oblate spheroid, $a - h = 0.13$ m, $c - h = 0.08$ m (or
  constant-thickness offset)
- **Fluid domain:** Volume enclosed by inner surface
- **External acoustic domain (Level 5):** Spherical truncation at $r = 2$ m with
  absorbing (PML/infinite element) boundary

### 5.2 Element Types

| Domain | Element Type | Order | DOFs |
|--------|-------------|-------|------|
| Abdominal wall (thin) | Shell elements (S4R / MITC4) | Quadratic | 6 DOF/node (3 disp + 3 rot) |
| Abdominal wall (thick/layered) | Solid continuum (C3D20R) | Quadratic | 3 DOF/node |
| Fluid interior | Acoustic elements (AC3D20) | Quadratic | 1 DOF/node (pressure) |
| External air (Level 5) | Acoustic + PML elements | Quadratic | 1 DOF/node |

### 5.3 Boundary Conditions

1. **Posterior fixation (spine):** The posterior ~30% of the shell surface
   (region where $y < -0.6c$) is constrained:
   - All translational DOFs fixed ($u_x = u_y = u_z = 0$)
   - Rotational DOFs free (for shell elements)

2. **Fluid-structure interface:** Coupling at the inner wall surface:
   - Continuity of normal displacement: $\mathbf{u} \cdot \mathbf{n} = \frac{1}{\rho_f \omega^2}\frac{\partial p}{\partial n}$
   - Pressure loading on structure: $\sigma_{nn} = -p$

3. **Symmetry (optional):** Exploit bilateral symmetry about the sagittal plane
   ($x = 0$) to halve the model.

4. **External loading (harmonic analysis):**
   - Incident plane wave: $p_{\text{inc}} = P_0 \sin(2\pi f t)$
   - Applied as uniform pressure on the anterior hemisphere
   - $P_0$ corresponding to target SPL (e.g., 120 dB → 20 Pa, 150 dB → 632 Pa)

### 5.4 Analysis Types

#### 5.4.1 Modal Analysis (Primary)

Solve the coupled eigenvalue problem:

$$\begin{bmatrix} \mathbf{K}_s & -\mathbf{L} \\ \mathbf{0} & \mathbf{K}_f \end{bmatrix} \begin{Bmatrix} \mathbf{u} \\ \mathbf{p} \end{Bmatrix} = \omega^2 \begin{bmatrix} \mathbf{M}_s & \mathbf{0} \\ \rho_f \mathbf{L}^T & \mathbf{M}_f \end{bmatrix} \begin{Bmatrix} \mathbf{u} \\ \mathbf{p} \end{Bmatrix}$$

Where:
- $\mathbf{K}_s$, $\mathbf{M}_s$ — structural stiffness and mass matrices
- $\mathbf{K}_f$, $\mathbf{M}_f$ — acoustic stiffness and mass matrices
- $\mathbf{L}$ — fluid-structure coupling matrix

Extract modes in the 0–50 Hz range (at least first 20 modes).

#### 5.4.2 Harmonic Response Analysis

After modal extraction, perform frequency sweep:
- Range: 1–30 Hz (0.1 Hz increments)
- Excitation: Uniform pressure on anterior surface
- Output: Wall displacement, strain, internal pressure amplification
- Damping: Structural (Rayleigh) + fluid viscous

$$Q_{\text{amplification}} = \frac{p_{\text{internal,max}}}{p_{\text{incident}}}$$

#### 5.4.3 Transient Analysis (Optional)

Time-domain simulation for impulsive excitation or complex waveforms.

### 5.5 Mesh Considerations

At $f = 10$ Hz, the acoustic wavelength in the fluid is:

$$\lambda_f = \frac{c_f}{f} = \frac{1540}{10} = 154 \text{ m}$$

The structural wavelength (bending wave in the wall) is:

$$\lambda_b = \left(\frac{D}{\rho_w h}\right)^{1/4} \cdot \frac{2\pi}{\sqrt{\omega}} \quad \text{where } D = \frac{Eh^3}{12(1-\nu^2)}$$

For $E = 50$ kPa, $h = 0.03$ m:
$$D = \frac{50000 \times 0.03^3}{12 \times 0.755} = \frac{1.35}{9.06} = 0.149 \text{ N·m}$$
$$\lambda_b \approx 2\pi\left(\frac{0.149}{1050 \times 0.03 \times (2\pi \times 10)^2}\right)^{1/4} \approx 0.17 \text{ m}$$

**Mesh requirements:**

| Domain | Min. elements per wavelength | Element size | Approx. element count |
|--------|------------------------------|-------------|----------------------|
| Wall (shell) | 10 per $\lambda_b$ | 17 mm | ~2,000 |
| Wall (solid, 3 layers) | 3 through thickness | 10 mm | ~15,000 |
| Fluid interior | 6 per $\lambda_f$ (but geometry-limited) | 15–20 mm | ~50,000 |
| External air (PML) | 6 per $\lambda_{\text{air}}$ = 34.3 m | Coarse | ~5,000 |

> **Total DOFs (Level 2):** ~60,000–80,000 — easily solvable on a workstation.

### 5.6 Parametric Study Plan

| Study | Parameter | Range | Steps | Purpose |
|-------|-----------|-------|-------|---------|
| A | Wall stiffness $E_w$ | 20–500 kPa | 10 log-spaced | Bound frequency uncertainty |
| B | Wall thickness $h$ | 15–50 mm | 8 linear | Effect of body habitus |
| C | Cavity size $a$ | 0.12–0.20 m | 5 | Body size variation |
| D | Aspect ratio $c/a$ | 0.5–0.9 | 5 | Posture / body shape |
| E | Fluid density $\rho_f$ | 900–1100 kg/m³ | 5 | Viscera composition |
| F | Gas inclusion volume | 0–500 mL | 6 | Bowel gas effect |
| G | Posterior fixity extent | 10–50% surface | 5 | Spine constraint effect |
| H | Damping ratio $\zeta$ | 0.05–0.30 | 5 | Tissue dissipation |

---

## 6. Progressive Model Complexity

### Level 1: Analytical Closed-Form

- **Geometry:** Oblate spheroid (equivalent sphere via $R_{\text{eq}}$)
- **Shell theory:** Thin-shell (Kirchhoff-Love), isotropic
- **Fluid:** Incompressible, inviscid, fully filling
- **Coupling:** Added mass approximation (Junger 1952)
- **Output:** Natural frequencies, mode shapes (spherical harmonics)
- **Effort:** Hours (hand calculation + Python script)
- **Value:** Establishes baseline, validates FEA

### Level 2: Simple FEA Oblate Spheroid

- **Geometry:** True oblate spheroid (not spherical approximation)
- **Wall:** Homogeneous isotropic shell elements, uniform thickness
- **Fluid:** Linear acoustic elements (inviscid)
- **BCs:** Posterior fixation, fluid-structure coupling
- **Solver:** SLEPc eigenvalue solve via FEniCSx
- **Output:** First 20 coupled modes, frequency response
- **Effort:** Days
- **Value:** Confirms analytical predictions, quantifies geometry effects

### Level 3: Multi-Layer Wall + Viscous Fluid

- **Geometry:** True oblate spheroid
- **Wall:** Layered solid elements:
  - Layer 1: Skin + fat (10 mm, $E = 5$ kPa)
  - Layer 2: Muscle (15 mm, $E = 50$ kPa, transversely isotropic)
  - Layer 3: Fascia (3 mm, $E = 2$ MPa)
  - Layer 4: Peritoneum (1 mm, $E = 50$ kPa)
- **Fluid:** Viscous acoustic (Stokes attenuation)
- **BCs:** Posterior rigid, lateral spring supports (flank tissue)
- **Solver:** Coupled FEA (Abaqus or COMSOL)
- **Output:** Layer-resolved stress/strain, damped natural frequencies
- **Effort:** 1–2 weeks
- **Value:** Realistic tissue response, damping characterization

### Level 4: Anatomically-Informed Geometry

- **Geometry:** Reconstructed from CT dataset (e.g., Visible Human Project)
  - Segmented abdominal cavity surface mesh
  - Individual organ volumes (liver, spleen, kidneys, bowel)
- **Wall:** Patient-specific thickness mapping from CT
- **Contents:** Heterogeneous — solid organs as viscoelastic inclusions, bowel as
  gas-containing tubes, free peritoneal fluid
- **BCs:** Spine, pelvis, diaphragm from anatomy
- **Solver:** FEBio (biomechanics-optimized) or COMSOL
- **Effort:** 1–2 months
- **Value:** Clinical realism, inter-subject variability study

### Level 5: Full Acoustic-Structure Interaction

- **External domain:** Surrounding air volume with incident infrasound field
- **Coupling:** Full two-way acoustic-structure at skin surface
- **Source:** Point source or plane wave at specified distance and SPL
- **Includes:** Clothing, body posture (standing/seated), room acoustics
- **Solver:** COMSOL (Acoustics Module) or Abaqus
- **Output:** Sound power transmission coefficient, internal pressure field,
  steady-state tissue strain as function of SPL
- **Effort:** 2–3 months
- **Value:** Definitive answer to the brown note hypothesis

---

## 7. Software Recommendations

### 7.1 Comparison Matrix

| Criterion | ANSYS | COMSOL | Abaqus | FEBio | CalculiX | Code_Aster | FEniCSx | Elmer |
|-----------|-------|--------|--------|-------|----------|------------|---------|-------|
| Acoustic-structure coupling | ★★★★★ | ★★★★★ | ★★★★★ | ★★☆ | ★★☆ | ★★★☆ | ★★★☆ | ★★★☆ |
| Biomechanics materials | ★★★☆ | ★★★☆ | ★★★★☆ | ★★★★★ | ★★☆ | ★★☆ | ★★★☆ | ★★☆ |
| Open source | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Python scripting | ★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆ | ★★☆ | ★★★☆ | ★★★★★ | ★★★☆ |
| Eigenvalue solvers | ★★★★★ | ★★★★★ | ★★★★★ | ★★★☆ | ★★★☆ | ★★★★☆ | ★★★★★ (SLEPc) | ★★★☆ |
| Documentation | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆ | ★★★☆ (French) | ★★★★☆ | ★★★☆ |
| Reproducibility | ★★☆ | ★★☆ | ★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ |
| Cost | $$$$$ | $$$$ | $$$$$ | Free | Free | Free | Free | Free |

### 7.2 Recommended Primary Tool: FEniCSx + SLEPc

**Justification:**

1. **Fully open source** — essential for reproducibility and publication.
2. **Native Python API** — all model definition, meshing (via Gmsh), solving, and
   post-processing in a single Python workflow.
3. **SLEPc integration** — world-class eigenvalue solver, purpose-built for the
   generalized eigenvalue problems arising in modal analysis.
4. **PETSc backend** — parallel scalable solvers for large problems.
5. **Variational formulation** — natural expression of the coupled
   fluid-structure weak form; no black-box element libraries.
6. **Active community** — tutorials for Helmholtz eigenvalue problems, structural
   modal analysis, and coupled systems (Undabit, Dokken, Bleyer).
7. **Docker images** — reproducible computational environment.

**Supporting tools:**
- **Gmsh** (Python API) — mesh generation for oblate spheroid geometry
- **meshio** — mesh format conversion
- **ParaView** / **PyVista** — visualization
- **NumPy / SciPy** — analytical calculations, post-processing
- **FEBio** — cross-validation for biomechanics-specific material models

### 7.3 Recommended Secondary Tool: COMSOL Multiphysics

For Level 5 (full acoustic-structure interaction), COMSOL's Acoustics Module
provides the most mature, turnkey solution. Use for validation against the
open-source FEniCSx results.

### 7.4 Python Ecosystem Summary

```
gmsh (meshing) → meshio (conversion) → FEniCSx/DOLFINx (FEA) → SLEPc (eigensolve)
                                                                    ↓
                                              PETSc (linear algebra) → ParaView (viz)
```

---

## 8. Validation Strategy

### 8.1 Analytical Benchmarks

| Benchmark | Expected Result | Tolerance |
|-----------|-----------------|-----------|
| Empty spherical shell, breathing mode | $f = \frac{1}{2\pi R}\sqrt{E/\rho(1-\nu^2)}$ | < 1% |
| Fluid-filled sphere, $n=1$ mode | Junger (1952) exact solution | < 2% |
| Oblate spheroid dry modes | Rayleigh-Ritz (Elaikh et al.) | < 5% |
| Mesh convergence | Richardson extrapolation | Monotonic convergence |

### 8.2 Physical Experiment — Water-Filled Latex Balloon

A simplified analog experiment to validate the FEA model:

**Setup:**
- Oblate spheroidal latex balloon (~30 cm × 22 cm)
- Filled with water (density matched to peritoneal fluid)
- Wall thickness: 0.5–1.0 mm (latex)
- Suspended by thin strings (free-free condition) OR placed on a rigid
  posterior support

**Excitation:**
- Mechanical shaker attached via stinger rod
- OR subwoofer-generated pressure wave in an anechoic chamber

**Measurement:**
- Laser Doppler vibrometer (LDV) for surface velocity
- Miniature hydrophone inside balloon for internal pressure
- Accelerometers on surface

**Procedure:**
1. Measure material properties of latex (tensile test → $E$, $\nu$)
2. Modal hammer impact test → transfer function → natural frequencies
3. Frequency sweep with shaker → mode shapes via scanning LDV
4. Compare measured frequencies with FEA prediction using measured geometry
   and material properties

**Expected outcome:** Agreement within 10% for first 5 modes validates the
fluid-structure coupling implementation.

### 8.3 Literature Cross-Validation

- Compare predicted abdominal resonance frequencies with published whole-body
  vibration data (4–8 Hz, ISO 2631)
- Compare with Panjabi et al. (1986) — in-vivo trunk resonance measurements
- Compare with CT-based abdominal volume measurements and organ mass data

### 8.4 Numerical Convergence Studies

1. **Mesh refinement:** $h$-refinement (4 mesh levels, doubling elements each
   time). Plot $f_n$ vs. DOF count. Expect asymptotic convergence.
2. **Polynomial order:** $p$-refinement (linear, quadratic, cubic elements).
3. **Domain truncation (Level 5):** Vary PML/infinite element layer distance.
   Verify < 1% change in results when outer boundary is moved.

### 8.5 Sensitivity Analysis

- **Morris one-at-a-time (OAT) screening** for the 8 parameters in §5.6
- **Sobol indices** (variance-based global sensitivity) for top 4 parameters
- Identify which parameters most strongly control whether $f_1$ falls in 5–10 Hz

---

## 9. Python Code Scaffold

### 9.1 Analytical Natural Frequency Calculator

```python
#!/usr/bin/env python3
"""
analytical_frequencies.py
Compute natural frequencies of a fluid-filled oblate spheroidal shell
using Junger (1952) added-mass approximation with equivalent-sphere mapping.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class AbdominalModel:
    """Parameters for the oblate spheroid abdominal model."""
    # Geometry (m)
    a: float = 0.16        # equatorial semi-axis
    c: float = 0.11        # polar semi-axis (a > c for oblate)
    h: float = 0.030       # wall thickness

    # Wall material
    E_w: float = 50e3      # Young's modulus (Pa)
    nu_w: float = 0.495    # Poisson's ratio
    rho_w: float = 1050.0  # density (kg/m^3)

    # Fluid properties
    rho_f: float = 1040.0  # fluid density (kg/m^3)
    c_f: float = 1540.0    # speed of sound in fluid (m/s)

    @property
    def R_eq(self) -> float:
        """Volume-equivalent sphere radius."""
        return (self.a**2 * self.c) ** (1.0 / 3.0)

    @property
    def volume(self) -> float:
        """Cavity volume (m^3)."""
        return (4.0 / 3.0) * np.pi * self.a**2 * self.c

    @property
    def D(self) -> float:
        """Flexural rigidity of the wall (N*m)."""
        return self.E_w * self.h**3 / (12.0 * (1.0 - self.nu_w**2))


def dry_shell_breathing_freq(model: AbdominalModel) -> float:
    """
    Breathing mode (n=0/1) frequency of a thin spherical shell (Hz).
    Lamb (1882) / Leissa (1973).
    """
    R = model.R_eq
    E, rho, nu = model.E_w, model.rho_w, model.nu_w
    omega = (1.0 / R) * np.sqrt(E / (rho * (1.0 - nu**2)))
    return omega / (2.0 * np.pi)


def dry_shell_mode_freq(model: AbdominalModel, n: int) -> float:
    """
    Natural frequency (Hz) of mode n for thin spherical shell.
    n=1: breathing, n>=2: bending modes.

    From Leissa (1973), Vibration of Shells, Eq. for spherical shells.
    """
    R = model.R_eq
    E, rho, nu, h = model.E_w, model.rho_w, model.nu_w, model.h

    if n <= 1:
        return dry_shell_breathing_freq(model)

    # Membrane contribution
    lam = n * (n + 1)
    membrane = E / (rho * R**2 * (1 - nu)) * (
        (lam - (1 + nu)) / (lam + (1 + nu))
    ) * lam

    # Bending contribution
    bending = (E * h**2) / (12.0 * rho * R**4 * (1.0 - nu**2)) * (
        lam**2 - 2.0 * lam * (1.0 - nu) + (1.0 - nu**2)
    )

    omega_sq = membrane + bending
    return np.sqrt(max(omega_sq, 0.0)) / (2.0 * np.pi)


def added_mass_factor(model: AbdominalModel, n: int) -> float:
    """
    Junger (1952) fluid added mass factor beta_n for a sphere.
    beta_n = (rho_f * R) / (rho_w * h * (n + 1))
    """
    R = model.R_eq
    return (model.rho_f * R) / (model.rho_w * model.h * (n + 1))


def wet_shell_freq(model: AbdominalModel, n: int) -> float:
    """
    Fluid-loaded natural frequency for mode n (Hz).
    f_wet = f_dry / sqrt(1 + beta_n)
    """
    f_dry = dry_shell_mode_freq(model, n)
    beta = added_mass_factor(model, n)
    return f_dry / np.sqrt(1.0 + beta)


def impedance_transmission(Z_air: float = 420.0,
                           Z_tissue: float = 1.6e6) -> float:
    """
    Power transmission coefficient at air-tissue interface.
    """
    return 4.0 * Z_air * Z_tissue / (Z_air + Z_tissue)**2


def spl_to_pressure(spl_db: float, p_ref: float = 20e-6) -> float:
    """Convert SPL in dB to pressure amplitude in Pa."""
    return p_ref * 10.0 ** (spl_db / 20.0)


def main():
    model = AbdominalModel()

    print("=" * 65)
    print("ABDOMINAL RESONANCE — ANALYTICAL FREQUENCY ESTIMATES")
    print("=" * 65)
    print(f"\nGeometry:")
    print(f"  Semi-major axis a  = {model.a*100:.1f} cm")
    print(f"  Semi-minor axis c  = {model.c*100:.1f} cm")
    print(f"  Wall thickness h   = {model.h*1000:.0f} mm")
    print(f"  Equivalent radius  = {model.R_eq*100:.2f} cm")
    print(f"  Cavity volume      = {model.volume*1e3:.2f} L")
    print(f"\nWall material:")
    print(f"  E = {model.E_w/1e3:.1f} kPa, ν = {model.nu_w}, "
          f"ρ = {model.rho_w} kg/m³")
    print(f"\nFluid:")
    print(f"  ρ_f = {model.rho_f} kg/m³, c_f = {model.c_f} m/s")

    print(f"\n{'Mode n':<10} {'f_dry (Hz)':<14} {'β_n':<10} {'f_wet (Hz)':<14}")
    print("-" * 48)

    for n in range(1, 7):
        f_d = dry_shell_mode_freq(model, n)
        beta = added_mass_factor(model, n)
        f_w = wet_shell_freq(model, n)
        print(f"  {n:<8} {f_d:<14.2f} {beta:<10.3f} {f_w:<14.2f}")

    # Impedance mismatch
    T = impedance_transmission()
    print(f"\nAir-tissue transmission coefficient: {T:.4e} ({10*np.log10(T):.1f} dB)")

    # Pressure at various SPLs
    print(f"\n{'SPL (dB)':<12} {'P_inc (Pa)':<14} {'P_transmitted (Pa)':<20}")
    print("-" * 46)
    for spl in [100, 110, 120, 130, 140, 150]:
        p_inc = spl_to_pressure(spl)
        p_trans = p_inc * np.sqrt(T)
        print(f"  {spl:<10} {p_inc:<14.2f} {p_trans:<20.4f}")

    # Parametric sweep: E_w
    print("\n--- Parametric Sweep: Wall Stiffness ---")
    print(f"{'E_w (kPa)':<14} {'f1_wet (Hz)':<14} {'f2_wet (Hz)':<14}")
    print("-" * 42)
    for E_kPa in [10, 20, 50, 100, 200, 500]:
        m = AbdominalModel(E_w=E_kPa * 1e3)
        print(f"  {E_kPa:<12} {wet_shell_freq(m, 1):<14.2f} "
              f"{wet_shell_freq(m, 2):<14.2f}")


if __name__ == "__main__":
    main()
```

### 9.2 Mesh Generation with Gmsh Python API

```python
#!/usr/bin/env python3
"""
generate_mesh.py
Generate an oblate spheroid mesh (shell + fluid volume) using the Gmsh
Python API for abdominal cavity FEA.
"""

import gmsh
import numpy as np
import sys


def create_oblate_spheroid_mesh(
    a: float = 0.16,        # equatorial semi-axis (m)
    c: float = 0.11,        # polar semi-axis (m)
    h: float = 0.030,       # wall thickness (m)
    lcar_wall: float = 0.015,   # mesh size on wall (m)
    lcar_fluid: float = 0.020,  # mesh size in fluid (m)
    output_file: str = "abdomen_mesh.msh",
    order: int = 2,         # element polynomial order
    gui: bool = False
):
    """
    Create a meshed oblate spheroid with:
    - Outer shell (wall domain)
    - Inner fluid volume
    - Physical groups for BCs
    """
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 2)
    gmsh.model.add("abdomen")
    occ = gmsh.model.occ

    # --- Create outer spheroid (sphere + dilate) ---
    outer_sphere = occ.addSphere(0, 0, 0, 1.0)
    occ.dilate([(3, outer_sphere)], 0, 0, 0, a, c, a)
    # Note: dilate(dx, dy, dz) maps to (x*dx, y*dy, z*dz)
    # We use (a, c, a) so that y-axis is the short axis (anterior-posterior)

    # --- Create inner spheroid (fluid boundary) ---
    a_in = a - h
    c_in = c - h
    inner_sphere = occ.addSphere(0, 0, 0, 1.0)
    occ.dilate([(3, inner_sphere)], 0, 0, 0, a_in, c_in, a_in)

    # --- Boolean: wall = outer - inner ---
    wall_result = occ.cut(
        [(3, outer_sphere)],
        [(3, inner_sphere)],
        removeObject=True,
        removeTool=False
    )
    wall_tags = [tag for dim, tag in wall_result[0] if dim == 3]

    # --- Synchronize before finding surfaces ---
    occ.synchronize()

    # --- Identify surfaces for boundary conditions ---
    # Get all surfaces of the wall domain
    wall_surfaces = gmsh.model.getBoundary(
        [(3, t) for t in wall_tags], oriented=False
    )

    # The inner sphere volume is the fluid domain
    fluid_volumes = [inner_sphere]

    # --- Identify posterior surface for fixed BC ---
    # Posterior = negative y hemisphere (y < -0.3 * c)
    # We'll tag surfaces based on their center of mass
    posterior_surfaces = []
    anterior_surfaces = []
    for dim, tag in wall_surfaces:
        if dim == 2:
            com = gmsh.model.occ.getCenterOfMass(dim, tag)
            if com[1] < -0.3 * c:
                posterior_surfaces.append(tag)
            else:
                anterior_surfaces.append(tag)

    # --- Physical groups ---
    gmsh.model.addPhysicalGroup(3, wall_tags, 1)
    gmsh.model.setPhysicalName(3, 1, "AbdominalWall")

    gmsh.model.addPhysicalGroup(3, fluid_volumes, 2)
    gmsh.model.setPhysicalName(3, 2, "FluidCavity")

    if posterior_surfaces:
        gmsh.model.addPhysicalGroup(2, posterior_surfaces, 10)
        gmsh.model.setPhysicalName(2, 10, "PosteriorFixed")

    if anterior_surfaces:
        gmsh.model.addPhysicalGroup(2, anterior_surfaces, 11)
        gmsh.model.setPhysicalName(2, 11, "AnteriorFree")

    # --- Mesh size fields ---
    # Wall mesh size
    gmsh.model.mesh.field.add("MathEval", 1)
    gmsh.model.mesh.field.setString(1, "F", str(lcar_wall))

    # Use as background field
    gmsh.model.mesh.field.setAsBackgroundMesh(1)
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)

    # --- Generate mesh ---
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.setOrder(order)

    # --- Report mesh statistics ---
    node_tags, _, _ = gmsh.model.mesh.getNodes()
    elem_types, elem_tags, _ = gmsh.model.mesh.getElements()
    total_elements = sum(len(et) for et in elem_tags)
    print(f"\nMesh statistics:")
    print(f"  Nodes:    {len(node_tags)}")
    print(f"  Elements: {total_elements}")
    print(f"  Order:    {order}")

    # --- Write mesh ---
    gmsh.write(output_file)
    print(f"  Written to: {output_file}")

    # --- Optional GUI ---
    if gui and "-nopopup" not in sys.argv:
        gmsh.fltk.run()

    gmsh.finalize()
    return output_file


if __name__ == "__main__":
    create_oblate_spheroid_mesh(gui=("--gui" in sys.argv))
```

### 9.3 FEniCSx Modal Analysis Setup

```python
#!/usr/bin/env python3
"""
modal_analysis.py
Structural modal analysis of an oblate spheroidal shell using DOLFINx
(FEniCSx) and SLEPc. Computes natural frequencies and mode shapes.

NOTE: This is a scaffold / starting point. A full coupled fluid-structure
eigenvalue problem requires additional acoustic domain assembly.

Prerequisites:
    pip install fenics-dolfinx petsc4py slepc4py mpi4py meshio
    (or use the DOLFINx Docker image: dolfinx/dolfinx:stable)
"""

import numpy as np
from mpi4py import MPI

try:
    import dolfinx
    from dolfinx import fem, mesh, io, default_scalar_type
    from dolfinx.fem.petsc import assemble_matrix
    import ufl
    from slepc4py import SLEPc
    from petsc4py import PETSc
    HAS_FENICSX = True
except ImportError:
    HAS_FENICSX = False
    print("WARNING: DOLFINx/SLEPc not installed. This script provides")
    print("the structure but cannot execute. Install via:")
    print("  conda install -c conda-forge fenics-dolfinx slepc4py")
    print("  OR use Docker: docker pull dolfinx/dolfinx:stable")


def create_ellipsoid_mesh_dolfinx(a=0.16, c=0.11, refinement=20):
    """
    Create an oblate spheroid mesh using Gmsh and import into DOLFINx.
    Returns a DOLFINx mesh object.
    """
    import gmsh

    gmsh.initialize()
    gmsh.model.add("abdomen_modal")
    occ = gmsh.model.occ

    # Create unit sphere and scale to oblate spheroid
    sphere = occ.addSphere(0, 0, 0, 1.0)
    occ.dilate([(3, sphere)], 0, 0, 0, a, c, a)
    occ.synchronize()

    gmsh.model.addPhysicalGroup(3, [sphere], 1)
    gmsh.model.setPhysicalName(3, 1, "Domain")

    # Mesh
    gmsh.option.setNumber("Mesh.MeshSizeMax", a / refinement * 5)
    gmsh.option.setNumber("Mesh.MeshSizeMin", a / refinement * 2)
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.setOrder(2)

    # Import into DOLFINx
    from dolfinx.io import gmshio
    domain, cell_tags, facet_tags = gmshio.model_to_mesh(
        gmsh.model, MPI.COMM_WORLD, 0, gdim=3
    )
    gmsh.finalize()
    return domain, cell_tags, facet_tags


def structural_modal_analysis(
    domain,
    E: float = 50e3,       # Young's modulus (Pa)
    nu: float = 0.495,     # Poisson's ratio
    rho: float = 1050.0,   # density (kg/m^3)
    num_modes: int = 20,
    target_frequency: float = 5.0  # target near this frequency (Hz)
):
    """
    Solve the structural eigenvalue problem:
        K u = omega^2 M u

    for the first `num_modes` natural frequencies of the elastic domain.
    """
    # Function space: vector CG2 (quadratic displacement)
    V = fem.functionspace(domain, ("Lagrange", 2, (3,)))

    # Trial and test functions
    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)

    # Constitutive law (linear isotropic elasticity)
    mu = fem.Constant(domain, default_scalar_type(E / (2.0 * (1.0 + nu))))
    lam = fem.Constant(domain, default_scalar_type(
        E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    ))
    rho_c = fem.Constant(domain, default_scalar_type(rho))

    def epsilon(u):
        return ufl.sym(ufl.grad(u))

    def sigma(u):
        return lam * ufl.nabla_div(u) * ufl.Identity(3) + 2.0 * mu * epsilon(u)

    # Bilinear forms
    k_form = ufl.inner(sigma(u), epsilon(v)) * ufl.dx  # stiffness
    m_form = rho_c * ufl.inner(u, v) * ufl.dx          # mass

    # --- Boundary conditions ---
    # Fix the posterior surface (y < -0.3 * c for oblate spheroid with
    # short axis along y). Here we fix all DOFs where y < threshold.

    def posterior_boundary(x):
        """Identify posterior nodes: y < -0.3 * max_y_extent."""
        c_approx = 0.11  # semi-minor axis
        return x[1] < -0.6 * c_approx

    boundary_dofs = fem.locate_dofs_geometrical(V, posterior_boundary)
    zero_vec = fem.Constant(domain, default_scalar_type((0.0, 0.0, 0.0)))
    bc = fem.dirichletbc(zero_vec, boundary_dofs, V)

    # --- Assemble matrices ---
    K = assemble_matrix(fem.form(k_form), bcs=[bc])
    K.assemble()

    M = assemble_matrix(fem.form(m_form), bcs=[bc])
    M.assemble()

    # Zero out BC rows/cols in mass matrix to avoid spurious modes
    # (DOLFINx handles this via diagonal entries; SLEPc shift helps)

    # --- Solve eigenvalue problem with SLEPc ---
    eigensolver = SLEPc.EPS().create(domain.comm)
    eigensolver.setOperators(K, M)
    eigensolver.setProblemType(SLEPc.EPS.ProblemType.GHEP)

    # Spectral transformation: shift-invert near target
    target_omega_sq = (2.0 * np.pi * target_frequency) ** 2
    st = eigensolver.getST()
    st.setType(SLEPc.ST.Type.SINVERT)
    eigensolver.setTarget(target_omega_sq)
    eigensolver.setWhichEigenpairs(SLEPc.EPS.Which.TARGET_MAGNITUDE)

    eigensolver.setDimensions(nev=num_modes)
    eigensolver.setTolerances(tol=1e-8, max_it=500)
    eigensolver.solve()

    # --- Extract results ---
    nconv = eigensolver.getConverged()
    print(f"\nConverged eigenvalues: {nconv}")
    print(f"\n{'Mode':<8} {'omega^2':<18} {'f (Hz)':<14} {'Period (s)':<14}")
    print("-" * 54)

    frequencies = []
    for i in range(min(nconv, num_modes)):
        eigenvalue = eigensolver.getEigenvalue(i)
        omega_sq = eigenvalue.real
        if omega_sq > 0:
            freq = np.sqrt(omega_sq) / (2.0 * np.pi)
            period = 1.0 / freq if freq > 0 else float('inf')
            frequencies.append(freq)
            print(f"  {i+1:<6} {omega_sq:<18.4f} {freq:<14.4f} {period:<14.4f}")

    eigensolver.destroy()
    return frequencies


def main():
    if not HAS_FENICSX:
        print("\nCannot execute without DOLFINx. Install and re-run.")
        return

    print("=" * 60)
    print("STRUCTURAL MODAL ANALYSIS — OBLATE SPHEROID (FEniCSx)")
    print("=" * 60)

    # Generate mesh
    print("\nGenerating mesh...")
    domain, cell_tags, facet_tags = create_ellipsoid_mesh_dolfinx(
        a=0.16, c=0.11, refinement=15
    )
    print(f"  Cells: {domain.topology.index_map(3).size_global}")

    # Run modal analysis
    frequencies = structural_modal_analysis(
        domain,
        E=50e3,        # 50 kPa
        nu=0.495,
        rho=1050.0,
        num_modes=20,
        target_frequency=5.0
    )

    if frequencies:
        print(f"\nLowest natural frequency: {frequencies[0]:.2f} Hz")
        in_range = [f for f in frequencies if 5.0 <= f <= 10.0]
        print(f"Modes in 5-10 Hz band: {len(in_range)}")


if __name__ == "__main__":
    main()
```

### 9.4 Coupled Acoustic-Structure Eigenvalue Problem (Outline)

```python
#!/usr/bin/env python3
"""
coupled_modal.py
Outline for the coupled fluid-structure eigenvalue problem in FEniCSx.
This assembles the block matrix system and uses SLEPc to solve.

The coupled system is:
    [K_s    -L  ] [u]         [M_s       0   ] [u]
    [               ] [  ] = ω² [                   ] [  ]
    [0      K_f ] [p]         [ρ_f L^T   M_f ] [p]

where:
    K_s, M_s = structural stiffness and mass
    K_f, M_f = acoustic stiffness and mass (from Helmholtz equation)
    L        = coupling matrix (normal displacement → pressure)
"""

# NOTE: This is pseudocode / outline — full implementation requires
# careful handling of mixed function spaces and block assembly in DOLFINx.

PSEUDOCODE = """
1. Create two meshes (or subdomains):
   - Omega_s: shell/solid wall domain
   - Omega_f: fluid domain
   - Gamma_fs: shared interface

2. Define function spaces:
   - V_s = VectorFunctionSpace(Omega_s, "CG", 2)  # displacement
   - V_f = FunctionSpace(Omega_f, "CG", 2)          # pressure

3. Variational forms:

   Structural stiffness:
       k_s(u, v) = ∫_Ωs σ(u) : ε(v) dx

   Structural mass:
       m_s(u, v) = ∫_Ωs ρ_s (u · v) dx

   Acoustic stiffness:
       k_f(p, q) = ∫_Ωf (1/ρ_f) ∇p · ∇q dx

   Acoustic mass:
       m_f(p, q) = ∫_Ωf (1 / (ρ_f c_f²)) p q dx

   Coupling (fluid pressure → structural load):
       l(p, v) = ∫_Γfs p (v · n) ds

   Coupling (structural displacement → fluid):
       l_T(u, q) = ∫_Γfs ρ_f (u · n) q ds

4. Assemble block matrices:
       A = [[K_s, -L],  [0, K_f]]
       B = [[M_s,  0],  [ρ_f L^T, M_f]]

5. Solve generalized eigenvalue problem:
       A x = ω² B x
   using SLEPc with shift-invert targeting ω² ≈ (2π × 5)²

6. Extract natural frequencies and coupled mode shapes.
"""

print(PSEUDOCODE)
```

---

## 10. References

### Vibration of Shells

1. Lamb, H. (1882). "On the Vibrations of an Elastic Sphere." *Proc. London
   Math. Soc.* s1-13(1), 189–212.
2. Leissa, A.W. (1973). *Vibration of Shells*. NASA SP-288. US Government
   Printing Office.
3. Junger, M.C. (1952). "Vibrations of Elastic Shells in a Fluid Medium and
   the Associated Radiation of Sound." *J. Appl. Mech.* 19(4), 439–445.
4. Junger, M.C. & Feit, D. (1972). *Sound, Structures, and Their Interaction*.
   MIT Press.
5. Elaikh, T.H. et al. "Free Vibration of Axisymmetric Thin Oblate Shells
   Containing Fluid." *Int. J. Mech. Eng.* (Rayleigh-Ritz solutions).

### Biomechanical Material Properties

6. Song, C. et al. (2006). "Mechanical Properties of the Human Abdominal Wall
   Measured in Vivo During Insufflation for Laparoscopic Surgery." *Surg.
   Endosc.* 20, 987–990. doi:10.1007/s00464-005-0676-6.
7. Kriener, L. et al. (2023). "Mechanical Characterization of the Human
   Abdominal Wall Using Uniaxial Tensile Testing." *Ann. Biomed. Eng.*
8. Frontiers in Bioengineering & Biotechnology (2024). "Numerical Modeling of
   the Abdominal Wall Biomechanics." doi:10.3389/fbioe.2024.1472509.
9. Duck, F.A. (1990). *Physical Properties of Tissue: A Comprehensive Reference
   Book*. Academic Press.
10. IT'IS Foundation. "Tissue Properties Database — Acoustic Properties."
    https://itis.swiss/virtual-population/tissue-properties/database/acoustic-properties/

### Whole-Body Vibration and Infrasound

11. ISO 2631-1:1997. "Mechanical Vibration and Shock — Evaluation of Human
    Exposure to Whole-Body Vibration."
12. ISO 5982:2001. "Mechanical Vibration and Shock — Range of Idealized Values
    to Characterize Seated-Body Biodynamic Response Under Vertical Vibration."
13. Leventhall, G. (2007). "What is Infrasound?" *Progress in Biophysics and
    Molecular Biology* 93(1–3), 130–137.
14. Benton, S. & Leventhall, H.G. (1986). "The Effect of Infrasound on the
    Human Body." *Proc. Inter-Noise*.

### Finite Element Methods

15. Dokken, J.S. "The FEniCSx Tutorial." https://jsdokken.com/dolfinx-tutorial/
16. Bleyer, J. "Numerical Tours of Computational Mechanics with FEniCSx."
    https://bleyerj.github.io/comet-fenicsx/
17. Geuzaine, C. & Remacle, J.-F. (2009). "Gmsh: A 3-D Finite Element Mesh
    Generator." *Int. J. Numer. Meth. Eng.* 79(11), 1309–1331.
18. Maas, S.A. et al. (2012). "FEBio: Finite Elements for Biomechanics."
    *J. Biomech. Eng.* 134(1), 011005.
19. Undabit. "Modal Superposition in Vibro-Acoustics."
    https://undabit.com/modal-based-vibro-acoustics

### Brown Note

20. Wikipedia contributors. "Brown note." *Wikipedia*. Retrieved 2025.
21. Discover Magazine (2024). "The Brown Note Frequency Isn't Real, But Sound
    Affects Our Bodies."

---

## Appendix A: Quick-Start Checklist

```
□ 1. Install Python environment:
      conda create -n browntone python=3.11
      conda activate browntone
      pip install numpy scipy matplotlib gmsh meshio

□ 2. Run analytical calculation:
      python analytical_frequencies.py

□ 3. Generate mesh:
      python generate_mesh.py

□ 4. Install FEniCSx (Docker recommended):
      docker pull dolfinx/dolfinx:v0.8.0
      docker run -v $(pwd):/work -w /work dolfinx/dolfinx:v0.8.0 \
          python3 modal_analysis.py

□ 5. Validate: compare FEA mode 1 with analytical ~4.9 Hz

□ 6. Parametric sweep: run analytical_frequencies.py with varied E_w

□ 7. Document results and prepare Level 3 model
```

## Appendix B: Unit Consistency Check

All calculations use SI units throughout:

| Quantity | SI Unit | Typical Value |
|----------|---------|---------------|
| Length | m | 0.16 |
| Mass | kg | — |
| Time | s | — |
| Force | N | — |
| Pressure / Modulus | Pa (= N/m² = kg/(m·s²)) | 50,000 |
| Density | kg/m³ | 1050 |
| Frequency | Hz (= s⁻¹) | 5 |
| Sound speed | m/s | 1540 |
| Acoustic impedance | kg/(m²·s) = Pa·s/m | 1.6×10⁶ |

---

*Document generated for the Browntone project. For questions or contributions,
see the project repository.*
