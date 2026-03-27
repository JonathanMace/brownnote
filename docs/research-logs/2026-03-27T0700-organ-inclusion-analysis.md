# Research Log — 2026-03-27T0700 — Solid Organ Inclusions

## What Was Done

Investigated whether treating the abdominal cavity contents as homogeneous fluid
introduces significant error in the flexural mode predictions. The abdomen
contains solid organs (liver 1.5 kg, spleen 0.15 kg, kidneys 0.3 kg total)
occupying ~20–30% of the cavity volume with shear moduli of 1–10 kPa.

## Approach

Four analysis pathways:

1. **Hashin-Shtrikman effective medium theory** — composite of fluid matrix +
   elastic spherical inclusions to bound effective bulk and shear moduli
2. **Inclusion shear stiffness** — Eshelby analysis of isolated elastic spheres
   in inviscid fluid; do they add macroscopic shear restoring force?
3. **Mass redistribution** — liver asymmetry (1.5 kg in upper right quadrant)
   breaks spherical symmetry; perturbation theory for frequency shift and
   m-degeneracy splitting
4. **Parametric sweep** — volume fraction φ ∈ [0, 0.30], E ∈ [1, 10] kPa;
   compare against boundary condition uncertainty

Canonical parameters: R = 0.157 m, ρ_f = 1020 kg/m³, K_f = 2.2 GPa,
E_wall = 100 kPa, h = 15 mm, P_IAP = 1000 Pa.

## Key Results

### 1. Bulk modulus is unchanged

Tissue bulk modulus ≈ water bulk modulus (both ~2.2 GPa). Hashin-Shtrikman
bounds give ΔK/K < 1 ppm. The breathing mode is completely unaffected.

### 2. Macroscopic shear modulus is zero

Isolated elastic spheres in a fluid matrix cannot transmit shear because the
fluid flows around them. The HS lower bound confirms G_eff = 0 for any
sub-percolation volume fraction (threshold ~0.29 for random spheres). The
Eshelby internal strain ratio ε_i/ε₀ ≈ 8 × 10⁻⁵ — the inclusions behave as
nearly rigid bodies in the flow field.

### 3. Density is the only significant effect

| Effect | Δf₂/f₂ |
|--------|---------|
| Effective density (φ = 0.25, Δρ/ρ = 0.86%) | −0.43% |
| Shear stiffness perturbation | ~0.0000% |
| Liver mass asymmetry (perturbation theory) | −0.91% |

The density correction is linear in φ and independent of inclusion stiffness E.
Panel A of the figure shows all four E curves (1, 4, 7, 10 kPa) collapsing
onto a single line — the stiffness simply doesn't matter.

### 4. Error budget: organs ≪ boundary conditions

| Uncertainty source | Frequency range/shift |
|--------------------|----------------------|
| Wall E (0.05–0.5 MPa) | 108% |
| IAP (500–3000 Pa) | 39% |
| Wall thickness (8–20 mm) | 23% |
| **Organ inclusions (φ = 0.25)** | **0.4%** |
| **Liver asymmetry** | **0.9%** |

The organ correction is **two orders of magnitude smaller** than the wall
stiffness uncertainty.

### 5. Hypothesis confirmed

> **H:** Organs are much softer than the wall (1–10 kPa vs 100 kPa) and their
> bulk modulus matches water. For flexural modes (no fluid compression), the
> organs just ride along as additional mass.

This is confirmed on all counts:
- K_tissue ≈ K_water → no volumetric stiffness change
- G_eff = 0 macroscopically → no shear restoring force
- k_incl/k_wall ~ 10⁻⁹ → negligible stiffness perturbation
- Density correction is real but small (0.4%)
- Dominant organ effect is mass, not stiffness

## Physical Interpretation

The flexural modes of the fluid-filled abdominal shell involve the wall bending
while the fluid sloshes around inside. The solid organs — being nearly
incompressible and much softer than the wall — are simply entrained by the
fluid motion. They translate and rotate as nearly rigid bodies within the flow
field, contributing their mass to the modal inertia but essentially zero
stiffness.

This is fundamentally different from, say, a steel ball bearing suspended in
gelatin, where the inclusion is stiffer than the matrix. Here, the "matrix" for
bulk stiffness is water (~2.2 GPa) and for shear stiffness is the abdominal
wall (~100 kPa). The organs (1–10 kPa) are softer than both by orders of
magnitude in the relevant modulus.

## Implications for the Model

1. **The homogeneous fluid approximation is justified.** It introduces < 1%
   error in flexural mode frequencies, compared to > 100% uncertainty from
   wall properties alone.

2. **A simple density correction suffices** if higher accuracy is ever needed:
   use ρ_eff = (1−φ)ρ_fluid + φ·ρ_organ ≈ 1029 kg/m³ instead of 1020 kg/m³.

3. **Liver asymmetry could matter for mode identification** — it splits the
   m-degeneracy by ~1%, which might be observable in high-resolution
   measurements but is irrelevant for the brown note frequency estimate.

4. **This analysis does NOT apply to the breathing mode** (n = 0), which
   compresses the fluid. There, the relevant comparison is K_tissue vs K_water,
   and since they're equal, the conclusion is the same: organs don't matter.

## Files

- `src/analytical/organ_inclusions.py` — analysis module
- `data/figures/fig_organ_inclusion_effect.png` — four-panel summary figure

## What's Next

This closes the organ inclusion question. The error budget is now clear:
wall properties dominate, fluid properties are secondary, and organ
inclusions are negligible. The remaining uncertainty drivers to investigate
are the boundary conditions (clamped vs free vs intermediate) and the
geometry (oblate spheroid aspect ratio).
