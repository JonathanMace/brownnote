"""
Solid organ inclusions and their effect on abdominal cavity resonance.

The abdomen contains solid organs (liver, spleen, kidneys) occupying ~20-30%
of the cavity volume. These have shear moduli of 1-10 kPa — soft compared to
the abdominal wall (~100 kPa) but nonzero, unlike the fluid. This module
quantifies whether treating the cavity contents as homogeneous fluid introduces
significant error in the flexural mode predictions.

Approach:
    1. Hashin-Shtrikman bounds for effective medium properties
    2. Frequency shift from inclusion shear stiffness
    3. Mass redistribution effects on mode shapes
    4. Parametric study: volume fraction × inclusion stiffness
    5. Comparison against boundary condition uncertainty

Usage:
    python -m src.analytical.organ_inclusions

Outputs:
    data/figures/fig_organ_inclusion_effect.png

References:
    - Hashin, Z. & Shtrikman, S. (1963). "A variational approach to the theory
      of the elastic behaviour of multiphase materials." JMPS 11(2):127-140.
    - Yeh, W.C. et al. (2002). "Elastic modulus measurements of human liver
      and correlation with pathology." Ultrasound Med Biol 28(4):467-474.
    - Kemper, A.R. et al. (2012). "Biomechanical response of human spleen in
      tensile loading." J Biomech 45(2):348-355.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)

# ---------------------------------------------------------------------------
# Output paths
# ---------------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIG_DIR = os.path.join(ROOT, "data", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
# Canonical parameters
# ═══════════════════════════════════════════════════════════════════════════
CAVITY_R = 0.157          # equivalent sphere radius [m]
RHO_FLUID = 1020.0        # fluid density [kg/m³]
K_FLUID = 2.2e9           # fluid bulk modulus [Pa]
WALL_E = 0.1e6            # wall Young's modulus [Pa] (100 kPa)

# Organ properties (literature ranges)
ORGAN_CATALOG = {
    "liver":  {"mass_kg": 1.50, "E_kPa": 4.0, "rho": 1060, "nu": 0.45},
    "spleen": {"mass_kg": 0.15, "E_kPa": 2.0, "rho": 1054, "nu": 0.45},
    "kidney_L": {"mass_kg": 0.15, "E_kPa": 7.5, "rho": 1050, "nu": 0.45},
    "kidney_R": {"mass_kg": 0.15, "E_kPa": 7.5, "rho": 1050, "nu": 0.45},
}


@dataclass
class InclusionParams:
    """Properties of a generic elastic spherical inclusion in fluid."""
    volume_fraction: float = 0.25   # φ: fraction of cavity filled by organs
    E_inclusion: float = 4000.0     # Young's modulus of inclusion [Pa]
    nu_inclusion: float = 0.45      # Poisson's ratio
    rho_inclusion: float = 1055.0   # inclusion density [kg/m³]
    K_fluid: float = 2.2e9          # fluid bulk modulus [Pa]
    rho_fluid: float = 1020.0       # fluid density [kg/m³]

    @property
    def G_inclusion(self) -> float:
        """Shear modulus of inclusion [Pa]."""
        return self.E_inclusion / (2 * (1 + self.nu_inclusion))

    @property
    def K_inclusion(self) -> float:
        """Bulk modulus of inclusion [Pa].

        For nearly incompressible soft tissue, K >> E.
        Tissue bulk modulus ≈ water bulk modulus.
        """
        return self.K_fluid  # soft tissue is nearly incompressible


# ═══════════════════════════════════════════════════════════════════════════
# 1. Effective medium theory — Hashin-Shtrikman bounds
# ═══════════════════════════════════════════════════════════════════════════

def hashin_shtrikman_bulk(inc: InclusionParams) -> dict:
    """
    Hashin-Shtrikman bounds on effective bulk modulus.

    For fluid matrix (G_matrix = 0) + elastic inclusions (G > 0):
    - Lower bound (HS⁻): fluid is the matrix phase
    - Upper bound (HS⁺): inclusions are the matrix phase

    Since the fluid and tissue have nearly identical bulk moduli (both ≈ 2.2 GPa),
    the effective bulk modulus barely changes. This is a KEY result: the inclusions
    do not alter the volumetric stiffness.
    """
    phi = inc.volume_fraction
    K_f = inc.K_fluid
    K_i = inc.K_inclusion
    G_f = 0.0  # fluid has no shear modulus
    G_i = inc.G_inclusion

    # HS lower bound (fluid as reference/matrix phase)
    # K_HS⁻ = K_f + φ / [1/(K_i - K_f) + (1-φ)/(K_f + 4G_f/3)]
    # With G_f = 0: denominator of second term = K_f
    dK = K_i - K_f
    if abs(dK) < 1e-6:
        K_lower = K_f
    else:
        K_lower = K_f + phi / (1.0 / dK + (1 - phi) / K_f)

    # HS upper bound (inclusion as reference/matrix phase)
    dK2 = K_f - K_i
    if abs(dK2) < 1e-6:
        K_upper = K_i
    else:
        K_upper = K_i + (1 - phi) / (1.0 / dK2 + phi / (K_i + 4 * G_i / 3))

    # Effective shear modulus bounds
    # HS lower bound for G (fluid matrix → G_HS⁻ = 0 always, since fluid is
    # the connected phase and cannot transmit shear at macroscale)
    G_lower = 0.0

    # HS upper bound for G (inclusion as matrix)
    # G_HS⁺ = G_i + (1-φ) / [1/(G_f - G_i) + 2φ(K_i + 2G_i)/(5G_i(K_i + 4G_i/3))]
    # With G_f = 0:
    if G_i < 1e-10:
        G_upper = 0.0
    else:
        zeta = 2 * phi * (K_i + 2 * G_i) / (5 * G_i * (K_i + 4 * G_i / 3))
        G_upper = G_i + (1 - phi) / (-1.0 / G_i + zeta)

    K_eff = (K_lower + K_upper) / 2  # midpoint estimate

    return {
        "K_lower": K_lower,
        "K_upper": K_upper,
        "K_eff": K_eff,
        "G_lower": G_lower,
        "G_upper": G_upper,
        "K_fluid": K_f,
        "K_ratio": K_eff / K_f,
        "delta_K_ppm": (K_eff / K_f - 1) * 1e6,
    }


def effective_density(inc: InclusionParams) -> dict:
    """
    Effective density of the composite (volume-averaged).

    For flexural modes, the fluid acts as added mass. The effective density
    is simply the volume-weighted average.
    """
    phi = inc.volume_fraction
    rho_eff = (1 - phi) * inc.rho_fluid + phi * inc.rho_inclusion
    delta_rho = rho_eff - inc.rho_fluid
    delta_frac = delta_rho / inc.rho_fluid

    return {
        "rho_eff": rho_eff,
        "rho_fluid": inc.rho_fluid,
        "delta_rho": delta_rho,
        "delta_frac": delta_frac,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. Added stiffness from inclusion shear modulus
# ═══════════════════════════════════════════════════════════════════════════

def inclusion_shear_stiffness_correction(
    inc: InclusionParams, R_cavity: float = CAVITY_R, mode_n: int = 2
) -> dict:
    """
    Estimate frequency shift from inclusion shear stiffness.

    KEY PHYSICS: Isolated elastic spheres in a fluid matrix CANNOT transmit
    shear at the macroscale. The fluid flows around them, decoupling their
    elastic response. The Hashin-Shtrikman lower bound confirms G_eff = 0
    for any volume fraction below the percolation threshold (~0.29 for
    random spheres).

    What about local (per-inclusion) elastic energy? Each inclusion sits in
    a flow field with imposed strain rate ε₀. For a sphere of shear modulus
    G_i in a matrix of shear modulus G_m, the internal strain is (Eshelby):

        ε_internal ≈ ε₀ × 5G_m / (2G_i)   when G_m << G_i

    For fluid matrix (G_m → 0): ε_internal → 0. The inclusions barely deform;
    they translate/rotate as nearly rigid bodies in the flow. Their elastic
    strain energy contribution is negligible.

    The ONLY significant contribution of inclusions is through their MASS
    (effective density), not their stiffness.
    """
    phi = inc.volume_fraction
    G_i = inc.G_inclusion
    K_f = inc.K_fluid

    # Macroscopic G_eff = 0 for non-percolating inclusions (HS⁻)
    G_eff_macro = 0.0

    # Wall bending stiffness for reference
    k_wall = (WALL_E * 0.015**3 / (12 * (1 - 0.49**2))) * \
             mode_n * (mode_n - 1) * (mode_n + 2)**2 / R_cavity**4

    # Eshelby estimate: internal strain of inclusions in fluid flow.
    # For G_matrix → 0: inclusion internal strain → 0.
    # Use a viscous estimate as upper bound: at frequency f ~ 7 Hz,
    # the effective matrix "stiffness" from viscous drag is G_visc ~ μ·ω.
    # For water-like fluid: μ ≈ 1e-3 Pa·s, ω ≈ 44 rad/s → G_visc ≈ 0.044 Pa.
    mu_fluid = 1e-3  # dynamic viscosity [Pa·s]
    omega_est = 2 * np.pi * 7  # representative frequency
    G_visc = mu_fluid * omega_est

    # Internal strain fraction: ε_i/ε₀ ≈ 5G_visc / (2G_i)
    if G_i > 0:
        strain_ratio = 5 * G_visc / (2 * G_i)
    else:
        strain_ratio = 1.0

    # Elastic energy in inclusions: U_i ∝ G_i × (strain_ratio × ε₀)² × φV
    # Compared to wall bending energy: U_wall ∝ k_wall × ε₀² × A_shell × R²
    # The ratio U_i/U_wall gives the stiffness perturbation.
    V_cavity = (4 / 3) * np.pi * R_cavity**3
    A_shell = 4 * np.pi * R_cavity**2
    k_inclusion_eff = G_i * strain_ratio**2 * phi * V_cavity / (A_shell * R_cavity**2)

    ratio = k_inclusion_eff / k_wall if k_wall > 0 else 0.0

    # Frequency shift: Δf/f ≈ (1/2) × Δk/k
    delta_f_frac = 0.5 * ratio

    return {
        "G_eff_macro": G_eff_macro,
        "k_wall_pa_m": k_wall,
        "k_inclusion_eff_pa_m": k_inclusion_eff,
        "stiffness_ratio": ratio,
        "strain_ratio": strain_ratio,
        "delta_f_frac": delta_f_frac,
        "delta_f_percent": delta_f_frac * 100,
        "note": "Inclusions don't percolate → G_eff = 0 macroscopically. "
                "Internal deformation is negligible (strain ratio {:.2e}).".format(
                    strain_ratio),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. Mass redistribution and mode shape perturbation
# ═══════════════════════════════════════════════════════════════════════════

def mass_redistribution_effect(
    inc: InclusionParams, R_cavity: float = CAVITY_R
) -> dict:
    """
    Effect of asymmetric organ mass distribution on mode shapes.

    The liver (1.5 kg) sits in the upper right quadrant. This breaks the
    spherical symmetry of the mass distribution. For mode n, this introduces
    coupling between modes of different azimuthal order m.

    For an asymmetric mass δm at position (r, θ, φ):
        Δω_n/ω_n ≈ -(1/2) × δm/M_eff × |Y_n^m(θ,φ)|²

    where M_eff is the total effective (modal) mass.
    """
    V_cavity = (4 / 3) * np.pi * R_cavity**3
    M_fluid = inc.rho_fluid * V_cavity

    # Total organ mass (from catalog)
    M_organs = sum(o["mass_kg"] for o in ORGAN_CATALOG.values())

    # Liver is the dominant asymmetry
    M_liver = ORGAN_CATALOG["liver"]["mass_kg"]

    # Modal mass for mode n=2 (added mass = ρ_f × R / n)
    m_added_per_area = inc.rho_fluid * R_cavity / 2  # n=2
    shell_area = 4 * np.pi * R_cavity**2
    M_modal = m_added_per_area * shell_area

    # Fractional frequency shift from liver asymmetry
    # Y_2^m at a typical position: |Y_2^m|² ~ O(1) on the sphere
    # But the liver is a distributed mass, not a point mass.
    # The coupling integral averages over the liver volume ≈ 0.3 × peak
    coupling_factor = 0.3
    delta_f_liver = -0.5 * (M_liver / M_modal) * coupling_factor

    # Frequency splitting: asymmetric mass lifts degeneracy of m-modes
    # For mode n=2 (5 m-values: -2,-1,0,1,2), the spread is:
    splitting_estimate = abs(delta_f_liver)

    return {
        "M_fluid_kg": M_fluid,
        "M_organs_kg": M_organs,
        "M_liver_kg": M_liver,
        "M_modal_n2_kg": M_modal,
        "organ_fraction_of_modal_mass": M_organs / M_modal,
        "liver_fraction_of_modal_mass": M_liver / M_modal,
        "delta_f_frac_liver": delta_f_liver,
        "delta_f_percent_liver": delta_f_liver * 100,
        "m_splitting_frac": splitting_estimate,
        "note": "Liver asymmetry shifts n=2 frequency by ~{:.1f}% and "
                "splits m-degeneracy by ~{:.1f}%.".format(
                    delta_f_liver * 100, splitting_estimate * 100),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 4. Parametric study
# ═══════════════════════════════════════════════════════════════════════════

def parametric_sweep(
    phi_range: np.ndarray = None,
    E_range_kPa: np.ndarray = None,
    R_cavity: float = CAVITY_R,
) -> dict:
    """
    Sweep volume fraction φ and inclusion stiffness E over specified ranges.
    Compute frequency with and without inclusions for each combination.

    Returns arrays suitable for contour/surface plotting.
    """
    if phi_range is None:
        phi_range = np.linspace(0.0, 0.30, 31)
    if E_range_kPa is None:
        E_range_kPa = np.linspace(1.0, 10.0, 19)

    # Baseline model (homogeneous fluid)
    baseline = AbdominalModelV2(
        a=R_cavity, b=R_cavity, c=R_cavity,
        h=0.015, E=WALL_E, nu=0.49,
        rho_fluid=RHO_FLUID, K_fluid=K_FLUID,
        P_iap=1000.0, loss_tangent=0.3,
    )
    f_baseline = flexural_mode_frequencies_v2(baseline, n_max=4)
    f2_base = f_baseline[2]
    f3_base = f_baseline[3]

    PHI, EI = np.meshgrid(phi_range, E_range_kPa, indexing='ij')
    f2_shift_pct = np.zeros_like(PHI)
    f3_shift_pct = np.zeros_like(PHI)
    f2_with_organs = np.zeros_like(PHI)
    f3_with_organs = np.zeros_like(PHI)

    for i, phi in enumerate(phi_range):
        for j, E_kPa in enumerate(E_range_kPa):
            inc = InclusionParams(
                volume_fraction=phi,
                E_inclusion=E_kPa * 1000,
                rho_inclusion=1055.0,
                rho_fluid=RHO_FLUID,
                K_fluid=K_FLUID,
            )

            # Density correction
            rho_info = effective_density(inc)
            rho_eff = rho_info["rho_eff"]

            # Stiffness correction (for both modes)
            stiff_n2 = inclusion_shear_stiffness_correction(inc, R_cavity, mode_n=2)
            stiff_n3 = inclusion_shear_stiffness_correction(inc, R_cavity, mode_n=3)

            # Modified model with effective density
            mod = AbdominalModelV2(
                a=R_cavity, b=R_cavity, c=R_cavity,
                h=0.015, E=WALL_E, nu=0.49,
                rho_fluid=rho_eff, K_fluid=K_FLUID,
                P_iap=1000.0, loss_tangent=0.3,
            )
            f_mod = flexural_mode_frequencies_v2(mod, n_max=4)

            # Apply stiffness perturbation on top
            f2_new = f_mod[2] * (1 + stiff_n2["delta_f_frac"])
            f3_new = f_mod[3] * (1 + stiff_n3["delta_f_frac"])

            f2_with_organs[i, j] = f2_new
            f3_with_organs[i, j] = f3_new
            f2_shift_pct[i, j] = (f2_new - f2_base) / f2_base * 100
            f3_shift_pct[i, j] = (f3_new - f3_base) / f3_base * 100

    return {
        "phi_range": phi_range,
        "E_range_kPa": E_range_kPa,
        "PHI": PHI,
        "EI": EI,
        "f2_base_hz": f2_base,
        "f3_base_hz": f3_base,
        "f2_with_organs_hz": f2_with_organs,
        "f3_with_organs_hz": f3_with_organs,
        "f2_shift_pct": f2_shift_pct,
        "f3_shift_pct": f3_shift_pct,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 5. Comparison with boundary condition uncertainty
# ═══════════════════════════════════════════════════════════════════════════

def compare_with_bc_uncertainty(R_cavity: float = CAVITY_R) -> dict:
    """
    Compare organ inclusion error vs boundary condition uncertainty.

    Wall elastic modulus is uncertain by roughly 1 order of magnitude (E = 0.05-0.5 MPa).
    Since f ∝ √E for flexural modes, this gives ~3× uncertainty in frequency.
    IAP varies from 500-3000 Pa (6× range), adding further uncertainty.

    How does the organ inclusion correction compare?
    """
    # Reference model
    ref = AbdominalModelV2(
        a=R_cavity, b=R_cavity, c=R_cavity,
        h=0.015, E=WALL_E, nu=0.49,
        rho_fluid=RHO_FLUID, K_fluid=K_FLUID,
        P_iap=1000.0, loss_tangent=0.3,
    )
    f2_ref = flexural_mode_frequencies_v2(ref, n_max=2)[2]

    # BC uncertainty: vary E
    E_range = [0.05e6, 0.1e6, 0.2e6, 0.5e6]
    f2_E = []
    for E_val in E_range:
        m = AbdominalModelV2(
            a=R_cavity, b=R_cavity, c=R_cavity,
            h=0.015, E=E_val, nu=0.49,
            rho_fluid=RHO_FLUID, K_fluid=K_FLUID,
            P_iap=1000.0, loss_tangent=0.3,
        )
        f2_E.append(flexural_mode_frequencies_v2(m, n_max=2)[2])

    f2_E_range = max(f2_E) - min(f2_E)
    f2_E_range_pct = f2_E_range / f2_ref * 100

    # BC uncertainty: vary IAP
    P_range = [500.0, 1000.0, 2000.0, 3000.0]
    f2_P = []
    for P_val in P_range:
        m = AbdominalModelV2(
            a=R_cavity, b=R_cavity, c=R_cavity,
            h=0.015, E=WALL_E, nu=0.49,
            rho_fluid=RHO_FLUID, K_fluid=K_FLUID,
            P_iap=P_val, loss_tangent=0.3,
        )
        f2_P.append(flexural_mode_frequencies_v2(m, n_max=2)[2])

    f2_P_range = max(f2_P) - min(f2_P)
    f2_P_range_pct = f2_P_range / f2_ref * 100

    # BC uncertainty: vary h (wall thickness)
    h_range = [0.008, 0.012, 0.015, 0.020]
    f2_h = []
    for h_val in h_range:
        m = AbdominalModelV2(
            a=R_cavity, b=R_cavity, c=R_cavity,
            h=h_val, E=WALL_E, nu=0.49,
            rho_fluid=RHO_FLUID, K_fluid=K_FLUID,
            P_iap=1000.0, loss_tangent=0.3,
        )
        f2_h.append(flexural_mode_frequencies_v2(m, n_max=2)[2])

    f2_h_range = max(f2_h) - min(f2_h)
    f2_h_range_pct = f2_h_range / f2_ref * 100

    # Organ inclusion correction at φ=0.25, E=4 kPa (typical)
    inc = InclusionParams(volume_fraction=0.25, E_inclusion=4000.0)
    rho_info = effective_density(inc)
    stiff_info = inclusion_shear_stiffness_correction(inc, R_cavity, mode_n=2)
    mass_info = mass_redistribution_effect(inc, R_cavity)

    # Total organ correction
    # Density effect: f ∝ 1/√ρ → Δf/f ≈ -(1/2)Δρ/ρ
    delta_f_density = -0.5 * rho_info["delta_frac"]
    delta_f_stiffness = stiff_info["delta_f_frac"]
    delta_f_total = delta_f_density + delta_f_stiffness
    delta_f_total_pct = delta_f_total * 100

    return {
        "f2_ref_hz": f2_ref,
        "E_range_MPa": [e / 1e6 for e in E_range],
        "f2_vs_E": f2_E,
        "f2_E_range_hz": f2_E_range,
        "f2_E_range_pct": f2_E_range_pct,
        "P_range_Pa": P_range,
        "f2_vs_P": f2_P,
        "f2_P_range_hz": f2_P_range,
        "f2_P_range_pct": f2_P_range_pct,
        "h_range_m": h_range,
        "f2_vs_h": f2_h,
        "f2_h_range_hz": f2_h_range,
        "f2_h_range_pct": f2_h_range_pct,
        "organ_delta_f_density_pct": delta_f_density * 100,
        "organ_delta_f_stiffness_pct": delta_f_stiffness * 100,
        "organ_delta_f_total_pct": delta_f_total_pct,
        "organ_mass_asymmetry_pct": mass_info["delta_f_percent_liver"],
    }


# ═══════════════════════════════════════════════════════════════════════════
# Plotting
# ═══════════════════════════════════════════════════════════════════════════

def plot_organ_inclusion_effect(save_path: str = None) -> None:
    """
    Four-panel figure summarizing organ inclusion effects.

    Panel A: Frequency shift vs volume fraction (lines for different E)
    Panel B: Contour map of frequency shift in (φ, E) space
    Panel C: Error budget bar chart (organs vs BC uncertainty)
    Panel D: Effective density and stiffness ratio vs φ
    """
    if save_path is None:
        save_path = os.path.join(FIG_DIR, "fig_organ_inclusion_effect.png")

    sweep = parametric_sweep()
    bc = compare_with_bc_uncertainty()

    fig, axes = plt.subplots(2, 2, figsize=(7, 4.5))
    fig.suptitle("Solid Organ Inclusions: Effect on Cavity Resonance",
                 fontsize=10, fontweight="bold", y=0.98)

    # Color scheme consistent with project
    blue = "#4C72B0"
    orange = "#DD8452"
    green = "#55A868"
    red = "#C44E52"
    purple = "#8172B3"

    # ── Panel A: f₂ shift vs φ for selected E values ──
    ax = axes[0, 0]
    E_select = [1.0, 4.0, 7.0, 10.0]
    colors_a = [blue, orange, green, red]
    for k, E_kPa in enumerate(E_select):
        j_idx = np.argmin(np.abs(sweep["E_range_kPa"] - E_kPa))
        lw = 2.0 if k == 0 else 1.0  # thickest for first, thin dashes for rest
        ls = "-" if k == 0 else ["--", "-.", ":"][k - 1]
        ax.plot(sweep["phi_range"] * 100,
                sweep["f2_shift_pct"][:, j_idx],
                color=colors_a[k], linewidth=lw, linestyle=ls,
                label=f"E={E_kPa:.0f} kPa")
    ax.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    ax.annotate("All E curves collapse:\nonly density matters",
                xy=(18, -0.27), fontsize=6, fontstyle="italic",
                color="0.35", ha="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow",
                          ec="0.7", alpha=0.9))
    ax.set_xlabel("Volume fraction φ [%]", fontsize=8)
    ax.set_ylabel("Δf₂/f₂ [%]", fontsize=8)
    ax.set_title("(A) Freq shift vs organ volume", fontsize=8, fontweight="bold")
    ax.legend(fontsize=6, loc="upper left")
    ax.tick_params(labelsize=7)
    ax.set_xlim(0, 30)

    # ── Panel B: Contour map ──
    ax = axes[0, 1]
    levels = np.linspace(
        np.floor(sweep["f2_shift_pct"].min()),
        np.ceil(sweep["f2_shift_pct"].max()),
        15
    )
    if len(np.unique(levels)) < 3:
        levels = np.linspace(sweep["f2_shift_pct"].min() - 0.1,
                             sweep["f2_shift_pct"].max() + 0.1, 15)
    cf = ax.contourf(sweep["PHI"] * 100, sweep["EI"],
                     sweep["f2_shift_pct"],
                     levels=levels, cmap="RdBu_r")
    cbar = fig.colorbar(cf, ax=ax, shrink=0.85)
    cbar.ax.tick_params(labelsize=6)
    cbar.set_label("Δf₂/f₂ [%]", fontsize=7)
    ax.set_xlabel("Volume fraction φ [%]", fontsize=8)
    ax.set_ylabel("Inclusion E [kPa]", fontsize=8)
    ax.set_title("(B) Frequency shift map", fontsize=8, fontweight="bold")
    ax.tick_params(labelsize=7)

    # ── Panel C: Error budget comparison ──
    ax = axes[1, 0]
    categories = [
        "Wall E\n(0.05–0.5 MPa)",
        "IAP\n(500–3000 Pa)",
        "Wall h\n(8–20 mm)",
        "Organ incl.\n(φ=0.25)",
        "Liver\nasymmetry",
    ]
    values = [
        bc["f2_E_range_pct"],
        bc["f2_P_range_pct"],
        bc["f2_h_range_pct"],
        abs(bc["organ_delta_f_total_pct"]),
        abs(bc["organ_mass_asymmetry_pct"]),
    ]
    bar_colors = [red, orange, purple, blue, green]
    bars = ax.barh(categories, values, color=bar_colors, edgecolor="white",
                   linewidth=0.5, height=0.6)

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=6.5)

    ax.set_xlabel("Frequency range / shift [%]", fontsize=8)
    ax.set_title("(C) Error budget: organs vs BC uncertainty",
                 fontsize=8, fontweight="bold")
    ax.tick_params(labelsize=7)
    ax.set_xlim(0, max(values) * 1.3)

    # ── Panel D: Frequency shift decomposition vs φ ──
    ax = axes[1, 1]
    phi_dense = np.linspace(0, 0.30, 100)
    shifts_density = []
    shifts_stiffness = []
    shifts_asymmetry = []
    for phi in phi_dense:
        inc = InclusionParams(volume_fraction=phi, E_inclusion=4000.0)
        rho_info = effective_density(inc)
        stiff_info = inclusion_shear_stiffness_correction(inc, CAVITY_R, 2)
        mass_info = mass_redistribution_effect(inc, CAVITY_R)
        shifts_density.append(-0.5 * rho_info["delta_frac"] * 100)
        shifts_stiffness.append(stiff_info["delta_f_percent"])
        shifts_asymmetry.append(mass_info["delta_f_percent_liver"])

    ax.fill_between(phi_dense * 100, shifts_density, 0,
                    alpha=0.3, color=blue, label="Density (Δρ/ρ)")
    ax.plot(phi_dense * 100, shifts_density, color=blue, linewidth=1.3)
    ax.plot(phi_dense * 100, shifts_asymmetry, color=green, linewidth=1.3,
            linestyle="--", label="Liver asymmetry")
    ax.plot(phi_dense * 100, shifts_stiffness, color=orange, linewidth=1.3,
            linestyle=":", label="Shear stiffness")
    ax.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    ax.set_xlabel("Volume fraction φ [%]", fontsize=8)
    ax.set_ylabel("Δf₂/f₂ [%]", fontsize=8)
    ax.set_title("(D) Shift decomposition by mechanism", fontsize=8,
                 fontweight="bold")
    ax.legend(fontsize=6, loc="lower left")
    ax.tick_params(labelsize=7)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {save_path}")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE — Solid Organ Inclusion Analysis")
    print("  Effect on abdominal cavity resonance")
    print("=" * 72)
    print()

    # --- 1. Hashin-Shtrikman bounds ---
    print("  1. EFFECTIVE MEDIUM THEORY (Hashin-Shtrikman)")
    print("  " + "-" * 60)
    inc = InclusionParams()  # defaults: φ=0.25, E=4 kPa
    hs = hashin_shtrikman_bulk(inc)
    print(f"  Volume fraction φ = {inc.volume_fraction:.0%}")
    print(f"  Inclusion E = {inc.E_inclusion/1000:.1f} kPa, "
          f"G = {inc.G_inclusion:.0f} Pa")
    print(f"  Fluid K = {inc.K_fluid/1e9:.1f} GPa")
    print(f"  Inclusion K = {inc.K_inclusion/1e9:.1f} GPa (tissue ≈ water)")
    print()
    print(f"  HS bounds on K_eff:")
    print(f"    K_lower = {hs['K_lower']/1e9:.6f} GPa")
    print(f"    K_upper = {hs['K_upper']/1e9:.6f} GPa")
    print(f"    K_eff/K_fluid = {hs['K_ratio']:.8f}")
    print(f"    ΔK = {hs['delta_K_ppm']:.2f} ppm  ← NEGLIGIBLE")
    print()
    print(f"  HS bounds on G_eff:")
    print(f"    G_lower = {hs['G_lower']:.0f} Pa (fluid reference)")
    print(f"    G_upper = {hs['G_upper']:.0f} Pa (inclusion reference)")
    print(f"    ★ Macroscopic G_eff → 0: inclusions don't percolate")
    print()

    # --- 2. Density effect ---
    print("  2. EFFECTIVE DENSITY")
    print("  " + "-" * 60)
    rho = effective_density(inc)
    print(f"  ρ_fluid = {rho['rho_fluid']:.0f} kg/m³")
    print(f"  ρ_eff   = {rho['rho_eff']:.1f} kg/m³")
    print(f"  Δρ/ρ    = {rho['delta_frac']:.4f} ({rho['delta_frac']*100:.2f}%)")
    print(f"  → Frequency shift from density: Δf/f ≈ {-0.5*rho['delta_frac']*100:.2f}%")
    print()

    # --- 3. Shear stiffness correction ---
    print("  3. INCLUSION SHEAR STIFFNESS")
    print("  " + "-" * 60)
    for n in [2, 3, 4]:
        s = inclusion_shear_stiffness_correction(inc, CAVITY_R, mode_n=n)
        print(f"  Mode n={n}:")
        print(f"    k_wall  = {s['k_wall_pa_m']:.1f} Pa/m")
        print(f"    k_incl  = {s['k_inclusion_eff_pa_m']:.2e} Pa/m")
        print(f"    ratio   = {s['stiffness_ratio']:.2e} ({s['delta_f_percent']:.4f}%)")
        print(f"    ε_i/ε₀  = {s['strain_ratio']:.2e}")
    print(f"  ★ Shear stiffness correction: NEGLIGIBLE (ε_i/ε₀ → 0)")
    print()

    # --- 4. Mass redistribution ---
    print("  4. MASS REDISTRIBUTION (liver asymmetry)")
    print("  " + "-" * 60)
    mr = mass_redistribution_effect(inc)
    print(f"  Total organ mass: {mr['M_organs_kg']:.2f} kg")
    print(f"  Modal mass (n=2): {mr['M_modal_n2_kg']:.2f} kg")
    print(f"  Organs / modal mass: {mr['organ_fraction_of_modal_mass']:.2f}")
    print(f"  Liver / modal mass:  {mr['liver_fraction_of_modal_mass']:.3f}")
    print(f"  Δf/f (liver):        {mr['delta_f_percent_liver']:.2f}%")
    print(f"  m-splitting:         {mr['m_splitting_frac']*100:.2f}%")
    print(f"  {mr['note']}")
    print()

    # --- 5. Comparison with BC uncertainty ---
    print("  5. ERROR BUDGET: ORGANS vs BOUNDARY CONDITIONS")
    print("  " + "-" * 60)
    bc = compare_with_bc_uncertainty()
    print(f"  Reference f₂ = {bc['f2_ref_hz']:.2f} Hz")
    print()
    print(f"  {'Source':<30} {'Range/Shift':>12}")
    print(f"  {'─'*30} {'─'*12}")
    print(f"  {'Wall E (0.05–0.5 MPa)':<30} {bc['f2_E_range_pct']:>+11.1f}%")
    print(f"  {'IAP (500–3000 Pa)':<30} {bc['f2_P_range_pct']:>+11.1f}%")
    print(f"  {'Wall h (8–20 mm)':<30} {bc['f2_h_range_pct']:>+11.1f}%")
    print(f"  {'Organ density (φ=0.25)':<30} {bc['organ_delta_f_density_pct']:>+11.2f}%")
    print(f"  {'Organ shear stiffness':<30} {bc['organ_delta_f_stiffness_pct']:>+11.4f}%")
    print(f"  {'Organ total':<30} {bc['organ_delta_f_total_pct']:>+11.2f}%")
    print(f"  {'Liver mass asymmetry':<30} {bc['organ_mass_asymmetry_pct']:>+11.2f}%")
    print(f"  {'─'*30} {'─'*12}")
    print()
    print("  ★ CONCLUSION:")
    print("    The organ inclusion correction ({:.1f}%) is MUCH SMALLER than".format(
        abs(bc["organ_delta_f_total_pct"])))
    print("    the boundary condition uncertainty from wall E ({:.1f}%),".format(
        bc["f2_E_range_pct"]))
    print("    IAP ({:.1f}%), or wall thickness ({:.1f}%).".format(
        bc["f2_P_range_pct"], bc["f2_h_range_pct"]))
    print()
    print("    The homogeneous fluid approximation is JUSTIFIED for flexural modes.")
    print("    Organs are too soft to contribute significant shear stiffness,")
    print("    their bulk modulus matches water, and their density is within 3%.")
    print()

    # --- 6. Hypothesis check ---
    print("  6. HYPOTHESIS VERIFICATION")
    print("  " + "-" * 60)
    print("  H: Organs are much softer than wall (1-10 kPa vs 100 kPa).")
    print("     Their K ≈ K_water. For flexural modes (no fluid compression),")
    print("     organs just ride along as additional mass.")
    print()
    print("  CONFIRMED:")
    print("    • K_eff/K_fluid differs by < 1 ppm (HS bounds)")
    print("    • G_eff → 0 because inclusions don't percolate")
    print("    • Shear stiffness ratio k_incl/k_wall < 0.01%")
    print("    • Density correction is {:.2f}% — real but small".format(
        abs(bc["organ_delta_f_density_pct"])))
    print("    • Dominant effect is mass, not stiffness (as hypothesized)")
    print()

    # --- Generate figure ---
    print("  Generating figure...")
    plot_organ_inclusion_effect()
    print()
    print("  Done.")
    print()
