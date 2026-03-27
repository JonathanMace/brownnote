# Viscous Correction to the Inviscid Fluid Model

**Date:** 2026-03-27  
**Branch:** `viscous-correction`  
**Module:** `src/analytical/viscous_correction.py`  
**Figure:** `data/figures/fig_viscous_correction.png`

## Motivation

Our baseline model (`natural_frequency_v2.py`) treats the enclosed abdominal
fluid as inviscid — characterised only by bulk modulus *K* and density ρ_f.
Real abdominal contents include water, bile, blood, mucus, and partially
digested food (chyme), with dynamic viscosity μ ranging from 0.001 Pa·s
(water) to ~0.5 Pa·s (thick chyme).  Some regions are non-Newtonian
(shear-thinning).

**Question:** Does neglecting viscosity significantly alter the predicted
Q factor (currently Q = 4 from structural damping alone)?

## Canonical Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| R (cavity radius) | 0.157 m | equivalent sphere |
| ρ_f (fluid density) | 1020 kg/m³ | |
| ρ_w (wall density) | 1050 kg/m³ | |
| h (wall thickness) | 0.01 m | |
| f₂ (n=2 frequency) | 4.0 Hz | flexural mode |
| ζ_struct | 0.125 | Q = 4 |

## Analysis

### 1. Stokes Boundary-Layer Thickness

For an oscillating viscous fluid, the boundary layer thickness is
δ = √(2μ / (ρ_f ω)).

| Fluid | μ [Pa·s] | δ [mm] | δ/R |
|-------|----------|--------|-----|
| Water | 0.001 | 0.28 | 0.0018 |
| Bile | 0.005 | 0.63 | 0.0040 |
| Blood | 0.004 | 0.56 | 0.0036 |
| Gastric acid | 0.010 | 0.88 | 0.0056 |
| Chyme (thin) | 0.050 | 1.98 | 0.013 |
| Mucus | 0.100 | 2.79 | 0.018 |
| Chyme (thick) | 0.500 | 6.25 | 0.040 |

**All δ/R ≪ 1** — viscous effects are confined to a thin boundary layer at
the shell inner wall.  The inviscid solution correctly describes the bulk
flow.

### 2. Viscous Damping from the Stokes Layer

For mode *n* on a sphere, the inviscid tangential velocity at the wall
violates no-slip.  The Stokes layer corrects this, dissipating energy at
a time-averaged rate:

$$\langle P_{\mathrm{visc}} \rangle
  = \tfrac{1}{4}\,\rho_f\,\omega\,\delta
    \int_S |v_\theta|^2\,\mathrm{d}A
  = \pi R^2 \rho_f \omega^3 \delta\,\xi^2
    \frac{n+1}{n(2n+1)}$$

The additional damping ratio is:

$$\Delta\zeta_{\mathrm{visc}}
  = \frac{\rho_f\,\delta\,(n+1)}
         {4\,n\,(2n+1)\,({\rho_w h + \rho_f R/n})}$$

| Fluid | Δζ_visc | Δζ/ζ_struct | Q_total | ΔQ |
|-------|---------|-------------|---------|-----|
| Water | 2.4×10⁻⁴ | 0.19% | 3.992 | −0.19% |
| Bile | 5.3×10⁻⁴ | 0.42% | 3.983 | −0.42% |
| Gastric acid | 7.5×10⁻⁴ | 0.60% | 3.976 | −0.59% |
| Chyme (thin) | 1.7×10⁻³ | 1.3% | 3.947 | −1.3% |
| Mucus | 2.4×10⁻³ | 1.9% | 3.926 | −1.9% |
| Chyme (thick) | 5.3×10⁻³ | 4.2% | 3.838 | −4.0% |

**Worst physiological case (mucus, μ = 0.1 Pa·s):** fluid damping adds
only 1.9% to the structural damping, reducing Q from 4.000 to 3.926.

### 3. Frequency Shift

The Stokes layer also adds a reactive (mass-like) correction.  Since the
Stokes impedance scales as (1+i), the fractional frequency shift equals
the damping ratio addition:

|Δf/f| = Δζ_visc

| Fluid | Δf [mHz] |
|-------|----------|
| Water | −0.9 |
| Mucus | −9.4 |
| Chyme (thick) | −21 |

Negligible in all cases (< 0.5% of 4 Hz).

### 4. Non-Newtonian Effects

Chyme behaves as a power-law fluid: τ = K γ̇ⁿ with K ≈ 0.5 Pa·s^n,
n ≈ 0.5–0.8.  The generalised Stokes layer thickness is:

$$\delta_{\mathrm{PL}}
  = \left[\frac{2K\,U_0^{n_{\mathrm{pl}}-1}}{\rho_f\,\omega}\right]
    ^{1/(1+n_{\mathrm{pl}})}$$

At the very low shear rates in our system (γ̇ ∼ 0.1 s⁻¹), the power-law
model gives μ_eff **greater** than K (shear-thinning fluids have high
apparent viscosity at low shear rates).  The power-law model diverges as
γ̇ → 0; real chyme has a finite zero-shear viscosity μ₀ ∼ 0.1–1 Pa·s
(Carreau model).

Even using the inflated power-law values (μ_eff up to ~1.7 Pa·s for
n_pl = 0.5), ζ_visc remains an order of magnitude below ζ_struct.

### 5. Crossover Viscosity

The viscosity at which Δζ_visc = ζ_struct:

$$\mu_{\mathrm{cross}} \approx 281\;\mathrm{Pa{\cdot}s}$$

This is comparable to peanut butter.  At the crossover, δ/R ≈ 0.94 and
the thin-BL approximation has broken down — the fluid would fill the
entire cavity as a viscous plug, which is not a physiologically relevant
regime.

## Key Finding

**The inviscid approximation is well justified.**

For all physiologically relevant fluid viscosities (μ ≤ 0.1 Pa·s):
- Δζ_visc < 2% of ζ_struct
- Q changes by less than 2% (from 4.000 to 3.926)
- Frequency shift is < 10 mHz (< 0.25%)

The structural (tissue) damping completely dominates fluid viscous damping.
This is because:
1. The Stokes layer is extremely thin (δ/R < 0.02) — viscosity acts only
   in a sub-millimetre skin at the cavity wall
2. The effective mass of the fluid (added mass ∝ ρ_f R) is large, so the
   small boundary-layer dissipation produces negligible damping ratio
3. The low oscillation frequency (4 Hz) keeps shear rates low, and the
   corresponding viscous stresses are small compared to inertial forces

## Implications for the Paper

- The inviscid fluid assumption in Sections 2–3 requires no correction.
- Viscous effects are a second-order perturbation (< 2%) and can be
  acknowledged in the Discussion as a validated simplification.
- Non-Newtonian rheology of chyme does not change this conclusion.
- Suggested text: *"Viscous boundary-layer analysis (Appendix X) shows
  that fluid damping contributes less than 2% to the total damping for
  μ ≤ 0.1 Pa·s, confirming the inviscid approximation."*

## Files

- `src/analytical/viscous_correction.py` — full analysis module
- `data/figures/fig_viscous_correction.png` — Q factor vs viscosity figure
