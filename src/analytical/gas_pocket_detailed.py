"""
Detailed analysis of bowel gas pockets as acoustic transducers.

Extends the preliminary Minnaert analysis with:
  1. Constrained-bubble model (elastic intestinal wall)
  2. Cylindrical geometry (real bowel topology)
  3. Multiple distributed gas pockets (collective response)
  4. Monopole tissue-coupling (near-field displacement)
  5. Parameter study over volume, geometry, wall constraint, frequency
  6. Inter-individual variability (population Monte-Carlo)

Physics summary
---------------
A gas pocket of volume V inside the intestine is compressible while the
surrounding tissue/fluid is essentially incompressible at infrasound
wavelengths (λ ~ 50 m >> body).  An incident pressure p drives radial
oscillation of the gas–tissue interface.

Three wall-constraint limits:
  • Free   — classical Minnaert bubble in infinite liquid
  • Elastic — intestinal wall adds both stiffness and mass
  • Rigid   — gas pocket cannot oscillate (control case)

Two geometries:
  • Spherical — radius a = (3V/4π)^{1/3}
  • Cylindrical — fixed lumen radius R_lumen, length L = V/(πR²)

Canonical tissue parameters:
  ρ_tissue  = 1020  kg/m³
  E_tissue  = 10e3  Pa  (intestinal wall, much softer than abdominal muscle)
  ν_tissue  = 0.45
  c_tissue  = 1540  m/s (longitudinal)
  h_wall    = 3e-3  m   (intestinal wall thickness)

References:
  Minnaert (1933) Phil. Mag. 16(104):235
  Leighton (1994) "The Acoustic Bubble", Academic Press
  Commander & Prosperetti (1989) JASA 85(2):732
  Levitt (1971) New Engl. J. Med. 284:1394 — bowel gas volumes
  Suarez et al. (1997) Am. J. Physiol. 272:G1028
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Literal
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
GAMMA = 1.4           # specific-heat ratio (air/gas mix)
P0 = 101325.0         # atmospheric + mean intra-abdominal pressure [Pa]
RHO_TISSUE = 1020.0   # surrounding tissue density [kg/m³]
E_WALL = 10.0e3       # intestinal wall Young's modulus [Pa]
NU_WALL = 0.45        # Poisson's ratio
H_WALL = 3.0e-3       # intestinal wall thickness [m]
RHO_WALL = 1040.0     # wall density [kg/m³]
C_TISSUE = 1540.0     # longitudinal speed of sound in tissue [m/s]
MU_TISSUE = 1.0e-3    # dynamic viscosity (water-like) [Pa·s]
R_LUMEN = 0.015       # typical small-intestine lumen radius [m]
P_REF = 20.0e-6       # reference pressure (hearing threshold) [Pa]
C_AIR = 343.0             # speed of sound in air [m/s]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class GasPocketParams:
    """Parameters for a single gas pocket."""
    volume_mL: float = 10.0
    geometry: Literal["spherical", "cylindrical"] = "spherical"
    wall: Literal["free", "elastic", "rigid"] = "elastic"
    gamma: float = GAMMA
    P0: float = P0
    rho_f: float = RHO_TISSUE
    E_w: float = E_WALL
    nu_w: float = NU_WALL
    h_w: float = H_WALL
    rho_w: float = RHO_WALL
    R_lumen: float = R_LUMEN

    @property
    def volume_m3(self) -> float:
        return self.volume_mL * 1.0e-6

    @property
    def a_sphere(self) -> float:
        """Equivalent spherical radius [m]."""
        return (3.0 * self.volume_m3 / (4.0 * np.pi)) ** (1.0 / 3.0)

    @property
    def L_cyl(self) -> float:
        """Cylindrical length [m] for fixed lumen radius."""
        return self.volume_m3 / (np.pi * self.R_lumen ** 2)


# ---------------------------------------------------------------------------
# 1. Resonance frequencies
# ---------------------------------------------------------------------------
def minnaert_frequency(p: GasPocketParams) -> float:
    """Classical Minnaert resonance of a free spherical bubble."""
    a = p.a_sphere
    return (1.0 / (2.0 * np.pi * a)) * np.sqrt(
        3.0 * p.gamma * p.P0 / p.rho_f
    )


def constrained_sphere_frequency(p: GasPocketParams) -> float:
    """
    Resonance of a spherical gas pocket enclosed by an elastic shell.

    Effective stiffness per unit volume change:
        K_gas  = 3γP₀
        K_wall = 2 E_w h / (a (1 - ν))       [hoop-stress thin-shell]

    Effective inertia per unit volume change:
        M_gas  = ρ_f a      (radiation added mass of surrounding fluid)
        M_wall = ρ_w h      (shell inertia per unit area)

    ω² = (K_gas + K_wall) / (a² (M_gas + M_wall))
    """
    a = p.a_sphere
    K_gas = 3.0 * p.gamma * p.P0
    K_wall = 2.0 * p.E_w * p.h_w / (a * (1.0 - p.nu_w))
    M_gas = p.rho_f * a
    M_wall = p.rho_w * p.h_w

    if p.wall == "free":
        K_wall = 0.0
        M_wall = 0.0
    elif p.wall == "rigid":
        return np.inf  # no oscillation

    omega2 = (K_gas + K_wall) / (a ** 2 * (M_gas + M_wall))
    return np.sqrt(max(omega2, 0.0)) / (2.0 * np.pi)


def cylindrical_radial_frequency(p: GasPocketParams) -> float:
    """
    Breathing (radial) mode of a long cylindrical gas column in an
    elastic tube.

    ω² = (2γP₀ + E_w h / (R(1-ν²))) / (R² (ρ_f + ρ_w h / R))

    The factor 2 (vs 3 for sphere) comes from cylindrical geometry.
    """
    R = p.R_lumen
    K_gas = 2.0 * p.gamma * p.P0
    K_wall = p.E_w * p.h_w / (R * (1.0 - p.nu_w ** 2))
    M_fluid = p.rho_f * R
    M_wall = p.rho_w * p.h_w

    if p.wall == "free":
        K_wall = 0.0
        M_wall = 0.0
    elif p.wall == "rigid":
        return np.inf

    omega2 = (K_gas + K_wall) / (R ** 2 * (M_fluid + M_wall))
    return np.sqrt(max(omega2, 0.0)) / (2.0 * np.pi)


def cylindrical_axial_frequency(p: GasPocketParams) -> float:
    """
    Axial (piston) mode of a cylindrical gas slug.

    Gas acts as a spring: k = γP₀ πR² / L
    Radiation mass at each open end: m_end ≈ ρ_f × 8R³/3  (piston in baffle)
    Total inertia: 2 × m_end

    f = (1/2π) √(k / (2 m_end))
    """
    R = p.R_lumen
    L = p.L_cyl
    k_gas = p.gamma * p.P0 * np.pi * R ** 2 / L
    m_end = p.rho_f * 8.0 * R ** 3 / 3.0
    omega2 = k_gas / (2.0 * m_end)
    return np.sqrt(max(omega2, 0.0)) / (2.0 * np.pi)


def resonance_frequency(p: GasPocketParams) -> float:
    """Return the lowest relevant resonance frequency for the pocket."""
    if p.geometry == "spherical":
        if p.wall == "free":
            return minnaert_frequency(p)
        return constrained_sphere_frequency(p)
    else:
        f_rad = cylindrical_radial_frequency(p)
        f_ax = cylindrical_axial_frequency(p)
        return min(f_rad, f_ax)


# ---------------------------------------------------------------------------
# 2. Damping
# ---------------------------------------------------------------------------
def damping_ratio(p: GasPocketParams, freq_hz: float) -> float:
    """
    Total damping ratio ζ = (δ_rad + δ_th + δ_vis) / 2.

    Components:
      δ_rad  = ωa/c  — radiation into surrounding tissue
      δ_th   ≈ 0.04  — thermal conduction in the gas (weakly frequency-dependent)
      δ_vis  = 4μ/(ρ ω a²) — viscous boundary layer at interface
      δ_wall — structural damping in intestinal wall (loss tangent ≈ 0.2–0.4)
    """
    omega = 2.0 * np.pi * freq_hz
    if p.geometry == "spherical":
        a = p.a_sphere
    else:
        a = p.R_lumen

    delta_rad = omega * a / C_TISSUE
    delta_th = 0.04
    delta_vis = 4.0 * MU_TISSUE / (p.rho_f * max(omega, 1e-6) * a ** 2)
    # Wall structural damping (loss tangent of intestinal tissue ~0.3)
    delta_wall = 0.3 if p.wall == "elastic" else 0.0

    return (delta_rad + delta_th + delta_vis + delta_wall) / 2.0


# ---------------------------------------------------------------------------
# 3. Forced response (single pocket)
# ---------------------------------------------------------------------------
def pocket_response(
    p: GasPocketParams,
    freq_hz: float | np.ndarray,
    spl_dB: float = 120.0,
) -> dict:
    """
    Forced-oscillator response of one gas pocket to incident pressure.

    Returns displacement of the gas-tissue interface, internal pressure
    oscillation, volume change, and radiated tissue displacement at
    various distances.
    """
    freq_hz = np.atleast_1d(np.asarray(freq_hz, dtype=float))
    omega = 2.0 * np.pi * freq_hz
    p_inc = P_REF * 10.0 ** (spl_dB / 20.0)

    f0 = resonance_frequency(p)
    if not np.isfinite(f0):
        # Rigid wall → no oscillation
        z = np.zeros_like(freq_hz)
        return dict(
            freq_hz=freq_hz, f0_hz=f0, xi_m=z, xi_um=z,
            delta_V_m3=z, delta_p_Pa=z, H=z, zeta=z,
            tissue_disp_at_2a_um=z, tissue_disp_at_5a_um=z,
        )

    omega0 = 2.0 * np.pi * f0

    # Stiffness per unit radial displacement
    if p.geometry == "spherical":
        a = p.a_sphere
        k_eff = 3.0 * p.gamma * p.P0 / a
        if p.wall == "elastic":
            k_eff += 2.0 * p.E_w * p.h_w / (a ** 2 * (1.0 - p.nu_w))
    else:
        a = p.R_lumen
        k_eff = 2.0 * p.gamma * p.P0 / a
        if p.wall == "elastic":
            k_eff += p.E_w * p.h_w / (a ** 2 * (1.0 - p.nu_w ** 2))

    # Frequency-dependent damping (evaluate at each freq)
    zeta_arr = np.array([damping_ratio(p, float(f)) for f in freq_hz])

    r = omega / omega0
    H = 1.0 / np.sqrt((1.0 - r ** 2) ** 2 + (2.0 * zeta_arr * r) ** 2)

    # Radial displacement of the gas-tissue interface
    xi = (p_inc / k_eff) * H

    # Volume change  ΔV = surface_area × ξ
    if p.geometry == "spherical":
        dV = 4.0 * np.pi * a ** 2 * xi
    else:
        L = p.L_cyl
        dV = 2.0 * np.pi * a * L * xi  # radial breathing

    # Internal pressure oscillation  Δp = -γP₀ ΔV/V
    delta_p = p.gamma * p.P0 * np.abs(dV) / p.volume_m3

    # Tissue displacement via monopole near-field: u(r) ≈ (a/r)² ξ
    tissue_2a = xi * 0.25   # at r = 2a
    tissue_5a = xi * 0.04   # at r = 5a

    return dict(
        freq_hz=freq_hz,
        f0_hz=f0,
        xi_m=xi,
        xi_um=xi * 1e6,
        delta_V_m3=dV,
        delta_p_Pa=delta_p,
        H=H,
        zeta=zeta_arr,
        tissue_disp_at_2a_um=tissue_2a * 1e6,
        tissue_disp_at_5a_um=tissue_5a * 1e6,
    )


# ---------------------------------------------------------------------------
# 4. Multiple gas pockets — collective response
# ---------------------------------------------------------------------------
def multi_pocket_response(
    pockets: list[GasPocketParams],
    freq_hz: float | np.ndarray,
    spl_dB: float = 120.0,
) -> dict:
    """
    Collective response of N distributed gas pockets.

    At infrasound frequencies the wavelength in tissue (~220 m at 7 Hz) is
    far larger than the abdomen (~0.3 m), so all pockets experience the
    same driving pressure and oscillate coherently.

    The total volume displacement sums linearly (monopole superposition).
    Peak tissue strain occurs at the wall of the largest pocket.
    """
    freq_hz = np.atleast_1d(np.asarray(freq_hz, dtype=float))
    total_dV = np.zeros_like(freq_hz)
    max_xi = np.zeros_like(freq_hz)
    pocket_results = []

    for pk in pockets:
        res = pocket_response(pk, freq_hz, spl_dB)
        total_dV += res["delta_V_m3"]
        max_xi = np.maximum(max_xi, res["xi_m"])
        pocket_results.append(res)

    total_gas_mL = sum(pk.volume_mL for pk in pockets)

    return dict(
        freq_hz=freq_hz,
        total_delta_V_m3=total_dV,
        max_wall_xi_um=max_xi * 1e6,
        n_pockets=len(pockets),
        total_gas_mL=total_gas_mL,
        individual=pocket_results,
    )


# ---------------------------------------------------------------------------
# 5. Tissue-coupling: monopole radiation into tissue
# ---------------------------------------------------------------------------
def tissue_displacement_field(
    p: GasPocketParams,
    freq_hz: float,
    spl_dB: float,
    r_distances_m: np.ndarray,
) -> np.ndarray:
    """
    Displacement amplitude in surrounding tissue vs distance from pocket
    centre.  Near-field monopole: u(r) = a² ξ / r² for r > a.
    """
    res = pocket_response(p, np.array([freq_hz]), spl_dB)
    xi = float(res["xi_m"][0])
    a = p.a_sphere if p.geometry == "spherical" else p.R_lumen
    r = np.maximum(r_distances_m, a)
    return (a / r) ** 2 * xi




# ---------------------------------------------------------------------------
# 5b. Acoustic short-circuit analysis (sealed GI segments)
# ---------------------------------------------------------------------------
def helmholtz_sealed_gi(
    V_gas_mL: float = 200.0,
    S_constriction_m2: float | None = None,
    d_constriction_mm: float = 10.0,
    L_gi_eff_m: float = 5.0,
) -> dict:
    """
    Helmholtz resonator estimate for a sealed GI segment.

    f_H = (c_air / 2*pi) * sqrt(S / (V * L_eff))

    Default params give f_H ~ 15 Hz.
    """
    V = V_gas_mL * 1e-6
    if S_constriction_m2 is not None:
        S = S_constriction_m2
    else:
        d = d_constriction_mm * 1e-3
        S = np.pi * (d / 2) ** 2
    L = L_gi_eff_m
    f_H = (C_AIR / (2.0 * np.pi)) * np.sqrt(S / (V * L))
    f_drive = 7.0
    equalization_ratio = 1.0 / (1.0 + (f_drive / f_H) ** 2)
    return dict(
        f_helmholtz_hz=f_H,
        V_gas_m3=V,
        S_m2=S,
        L_eff_m=L,
        short_circuit_ratio_7Hz=equalization_ratio,
    )

# ---------------------------------------------------------------------------
# 6. Population variability model
# ---------------------------------------------------------------------------
def population_gas_model(
    n_individuals: int = 10_000,
    seed: int = 42,
) -> dict:
    """
    Monte-Carlo model of inter-individual gas-pocket variability.

    Literature ranges (Levitt 1971; Suarez 1997; Bedell 1956):
      Total bowel gas:  mean ≈ 200 mL, range 100-1500 mL
      Number of pockets: 3–25  (approximation)
      Pocket-size distribution: log-normal

    For each simulated individual we draw total gas volume, partition
    into N pockets, and compute the aggregate 7 Hz response at 120 dB.
    """
    rng = np.random.default_rng(seed)

    # Total bowel gas — log-normal, median ~200 mL, heavy right tail
    log_mu = np.log(200.0)
    log_sigma = 0.65  # gives 95% CI ≈ [70, 570] mL, tail to ~1500
    total_gas_mL = rng.lognormal(log_mu, log_sigma, n_individuals)
    total_gas_mL = np.clip(total_gas_mL, 30.0, 2000.0)

    # Number of discrete pockets — Poisson-ish, mean ~10
    n_pockets = rng.poisson(lam=10, size=n_individuals)
    n_pockets = np.clip(n_pockets, 2, 40)

    max_xi_um = np.zeros(n_individuals)
    total_dV_m3 = np.zeros(n_individuals)

    for i in range(n_individuals):
        N = int(n_pockets[i])
        # Dirichlet split of total volume into N pockets
        fracs = rng.dirichlet(np.ones(N))
        vols = fracs * total_gas_mL[i]  # mL per pocket

        # Randomly assign geometry
        pockets = []
        for v in vols:
            geom = rng.choice(["spherical", "cylindrical"], p=[0.3, 0.7])
            pockets.append(GasPocketParams(volume_mL=float(v), geometry=geom,
                                           wall="elastic"))

        res = multi_pocket_response(pockets, np.array([7.0]), spl_dB=120.0)
        max_xi_um[i] = float(res["max_wall_xi_um"][0])
        total_dV_m3[i] = float(res["total_delta_V_m3"][0])

    return dict(
        total_gas_mL=total_gas_mL,
        n_pockets=n_pockets,
        max_xi_um=max_xi_um,
        total_dV_m3=total_dV_m3,
        n_individuals=n_individuals,
    )


# ---------------------------------------------------------------------------
# 7. Parameter-study driver
# ---------------------------------------------------------------------------
def parameter_study() -> dict:
    """
    Sweep gas volume (1–100 mL), geometry, wall constraint, and
    frequency (1–50 Hz).  Returns a dict of result arrays.
    """
    volumes = np.array([1, 2, 5, 10, 20, 50, 100], dtype=float)
    freqs = np.linspace(1.0, 50.0, 200)
    geometries = ["spherical", "cylindrical"]
    walls = ["free", "elastic", "rigid"]

    results = {}
    for geom in geometries:
        for wall in walls:
            key = f"{geom}_{wall}"
            xi_matrix = np.zeros((len(volumes), len(freqs)))
            f0_arr = np.zeros(len(volumes))
            for iv, vol in enumerate(volumes):
                p = GasPocketParams(volume_mL=vol, geometry=geom, wall=wall)
                res = pocket_response(p, freqs, spl_dB=120.0)
                xi_matrix[iv, :] = res["xi_um"]
                f0_arr[iv] = res["f0_hz"]
            results[key] = dict(
                xi_um=xi_matrix, f0_hz=f0_arr,
                volumes=volumes, freqs=freqs,
            )
    return results


# ===================================================================
# FIGURE GENERATION
# ===================================================================
FIG_DIR = Path(__file__).resolve().parents[2] / "data" / "figures"


def fig_frequency_response(save: bool = True) -> plt.Figure:
    """
    Figure: frequency response for various pocket sizes and constraints.
    4-panel: spherical-free, spherical-elastic, cyl-free, cyl-elastic.
    """
    freqs = np.linspace(1.0, 50.0, 500)
    volumes = [1, 5, 10, 20, 50, 100]
    configs = [
        ("spherical", "free", "Spherical — free"),
        ("spherical", "elastic", "Spherical — elastic wall"),
        ("cylindrical", "free", "Cylindrical — free"),
        ("cylindrical", "elastic", "Cylindrical — elastic wall"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True, sharey=True)
    cmap = plt.cm.viridis
    colors = [cmap(i / (len(volumes) - 1)) for i in range(len(volumes))]

    for ax, (geom, wall, title) in zip(axes.flat, configs):
        for iv, vol in enumerate(volumes):
            p = GasPocketParams(volume_mL=vol, geometry=geom, wall=wall)
            res = pocket_response(p, freqs, spl_dB=120.0)
            label = f"{vol} mL (f₀={res['f0_hz']:.0f} Hz)"
            ax.semilogy(freqs, res["xi_um"], color=colors[iv], label=label,
                        linewidth=1.3)
        ax.set_title(title, fontsize=11)
        ax.axhline(0.5, color="red", ls="--", lw=0.8, alpha=0.6)
        ax.text(48, 0.55, "PIEZO threshold", ha="right", va="bottom",
                fontsize=7, color="red", alpha=0.7)
        ax.set_ylim(1e-3, 50)
        ax.set_ylabel("Wall displacement [μm]")
        ax.legend(fontsize=6.5, loc="upper right", framealpha=0.8)
        ax.grid(True, alpha=0.3)

    for ax in axes[1]:
        ax.set_xlabel("Frequency [Hz]")

    fig.suptitle(
        "Gas-pocket wall displacement at 120 dB SPL — constrained-bubble model",
        fontsize=13, fontweight="bold", y=0.98,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    if save:
        FIG_DIR.mkdir(parents=True, exist_ok=True)
        path = FIG_DIR / "fig_gas_pocket_frequency_response.png"
        fig.savefig(path, dpi=200, bbox_inches="tight")
        print(f"Saved → {path}")
    return fig


def fig_variability(save: bool = True) -> plt.Figure:
    """
    Figure: population variability — distribution of gas-pocket response.
    4 panels: (A) total gas histogram, (B) max wall displacement histogram,
    (C) scatter gas-volume vs displacement, (D) CDF of displacement with
    thresholds.
    """
    print("Running population Monte-Carlo (N=10 000) ...")
    pop = population_gas_model(n_individuals=10_000)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (A) Total bowel gas distribution
    ax = axes[0, 0]
    ax.hist(pop["total_gas_mL"], bins=80, color="steelblue", edgecolor="none",
            alpha=0.85)
    ax.set_xlabel("Total bowel gas [mL]")
    ax.set_ylabel("Count")
    ax.set_title("(A)  Total bowel gas distribution")
    ax.axvline(200, color="k", ls="--", lw=0.8, label="median ≈ 200 mL")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (B) Max pocket-wall displacement histogram
    ax = axes[0, 1]
    ax.hist(pop["max_xi_um"], bins=80, color="darkorange", edgecolor="none",
            alpha=0.85)
    ax.axvline(0.5, color="red", ls="--", lw=1.0, label="PIEZO threshold (0.5 μm)")
    ax.set_xlabel("Max pocket-wall displacement [μm]")
    ax.set_ylabel("Count")
    ax.set_title("(B)  Wall displacement distribution (7 Hz, 120 dB)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (C) Scatter: total gas vs max displacement
    ax = axes[1, 0]
    ax.scatter(pop["total_gas_mL"], pop["max_xi_um"], s=1, alpha=0.15,
               color="teal")
    ax.set_xlabel("Total bowel gas [mL]")
    ax.set_ylabel("Max pocket-wall displacement [μm]")
    ax.set_title("(C)  Gas volume → displacement coupling")
    ax.axhline(0.5, color="red", ls="--", lw=0.8)
    ax.set_xlim(0, 1500)
    ax.grid(True, alpha=0.3)

    # (D) CDF of displacement with thresholds
    ax = axes[1, 1]
    sorted_xi = np.sort(pop["max_xi_um"])
    cdf = np.arange(1, len(sorted_xi) + 1) / len(sorted_xi)
    ax.plot(sorted_xi, cdf, color="navy", lw=1.5)
    ax.axvline(0.5, color="red", ls="--", lw=0.8, label="PIEZO threshold")
    frac_above = np.mean(pop["max_xi_um"] > 0.5) * 100
    ax.axhline(1.0 - frac_above / 100, color="gray", ls=":", lw=0.7)
    ax.text(0.6, 1.0 - frac_above / 100 + 0.02,
            f"{frac_above:.0f}% above threshold", fontsize=9, color="red")
    ax.set_xlabel("Max pocket-wall displacement [μm]")
    ax.set_ylabel("Cumulative fraction")
    ax.set_title("(D)  Population CDF — who exceeds PIEZO threshold?")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.suptitle(
        "Inter-individual variability in gas-pocket acoustic response\n"
        "(7 Hz, 120 dB SPL, N = 10 000 simulated individuals)",
        fontsize=13, fontweight="bold", y=1.01,
    )
    fig.tight_layout()

    if save:
        FIG_DIR.mkdir(parents=True, exist_ok=True)
        path = FIG_DIR / "fig_gas_pocket_variability.png"
        fig.savefig(path, dpi=200, bbox_inches="tight")
        print(f"Saved → {path}")
    return fig


# ===================================================================
# CONSOLE REPORT (when run as script)
# ===================================================================
def print_report():
    """Pretty-print a summary of all analyses to the console."""
    W = 76
    print()
    print("=" * W)
    print("  BROWNTONE — Detailed Gas-Pocket Acoustic Transducer Analysis")
    print("=" * W)

    # --- Section 1: resonance frequencies ---
    print()
    print("  1. RESONANCE FREQUENCIES — constrained-bubble model")
    print("  " + "-" * (W - 4))
    header = (f"  {'Vol(mL)':>8} {'Geom':>10} {'Wall':>8} "
              f"{'f₀ (Hz)':>10} {'f_Minn':>10}")
    print(header)
    print("  " + "-" * (W - 4))

    for vol in [1, 5, 10, 20, 50, 100]:
        for geom in ["spherical", "cylindrical"]:
            for wall in ["free", "elastic"]:
                p = GasPocketParams(volume_mL=vol, geometry=geom, wall=wall)
                f0 = resonance_frequency(p)
                fm = minnaert_frequency(p)
                f0_s = f"{f0:.1f}" if np.isfinite(f0) else "—"
                print(f"  {vol:>8} {geom:>10} {wall:>8} "
                      f"{f0_s:>10} {fm:>10.1f}")
    print("  " + "-" * (W - 4))

    # --- Section 2: response at 7 Hz, 120 dB ---
    print()
    print("  2. RESPONSE AT 7 Hz, 120 dB (20 Pa)")
    print("  " + "-" * (W - 4))
    print(f"  {'Vol':>5} {'Geom':>7} {'Wall':>7} {'f₀':>7} "
          f"{'H':>7} {'ξ(μm)':>8} {'ΔV(nL)':>9} {'PIEZO':>6}")
    print("  " + "-" * (W - 4))

    for vol in [1, 5, 10, 20, 50, 100]:
        for geom in ["spherical", "cylindrical"]:
            p = GasPocketParams(volume_mL=vol, geometry=geom, wall="elastic")
            res = pocket_response(p, np.array([7.0]), spl_dB=120.0)
            f0 = res["f0_hz"]
            H = float(res["H"][0])
            xi = float(res["xi_um"][0])
            dV = float(res["delta_V_m3"][0]) * 1e9  # nanolitres
            piezo = "YES" if xi > 0.5 else "no"
            f0_s = f"{f0:.0f}" if np.isfinite(f0) else "—"
            print(f"  {vol:>5} {geom:>7} {'elast':>7} {f0_s:>7} "
                  f"{H:>7.4f} {xi:>8.3f} {dV:>9.2f} {piezo:>6}")
    print("  " + "-" * (W - 4))

    # --- Section 3: multi-pocket example ---
    print()
    print("  3. MULTI-POCKET EXAMPLE: typical bowel gas (200 mL in 10 pockets)")
    print("  " + "-" * (W - 4))
    pockets = [
        GasPocketParams(volume_mL=v, geometry="cylindrical", wall="elastic")
        for v in [5, 8, 10, 15, 20, 25, 30, 35, 27, 25]  # total = 200 mL
    ]
    res = multi_pocket_response(pockets, np.array([7.0]), spl_dB=120.0)
    print(f"    Total gas:        {res['total_gas_mL']:.0f} mL")
    print(f"    N pockets:        {res['n_pockets']}")
    print(f"    Max wall ξ:       {float(res['max_wall_xi_um'][0]):.3f} μm")
    print(f"    Total ΔV:         {float(res['total_delta_V_m3'][0])*1e9:.1f} nL")
    print("  " + "-" * (W - 4))

    # --- Section 4: tissue displacement field ---
    print()
    print("  4. TISSUE DISPLACEMENT FIELD (50 mL spherical pocket, 7 Hz, 120 dB)")
    p_field = GasPocketParams(volume_mL=50, geometry="spherical", wall="elastic")
    a_mm = p_field.a_sphere * 1e3
    print(f"     (pocket radius a = {a_mm:.1f} mm)")
    print("  " + "-" * (W - 4))
    r_mm = np.array([25, 30, 40, 50, 75, 100, 150, 200])
    r_m = r_mm * 1e-3
    u = tissue_displacement_field(p_field, 7.0, 120.0, r_m) * 1e6
    for rm, um in zip(r_mm, u):
        print(f"    r = {rm:>4} mm:  u = {um:>8.4f} μm")
    print("  " + "-" * (W - 4))

    # --- Section 5: key finding ---
    print()
    print("  5. KEY FINDING — SUSCEPTIBILITY VARIABILITY")
    print("  " + "-" * (W - 4))
    print()
    print("  5a. Total volume displacement (ΔV) — scales with total gas")
    print(f"  {'Case':>28} {'N':>4} {'max ξ':>8} {'total ΔV':>12} {'ratio':>6}")
    print("  " + "-" * (W - 4))
    N_fixed = 10
    ref_dV = None
    for label, total_mL in [("Low gas (100 mL)", 100),
                             ("Typical (200 mL)", 200),
                             ("High gas (800 mL)", 800),
                             ("Extreme (1500 mL)", 1500)]:
        vols = np.full(N_fixed, total_mL / N_fixed)
        pockets = [GasPocketParams(volume_mL=float(v), geometry="cylindrical",
                                   wall="elastic") for v in vols]
        res = multi_pocket_response(pockets, np.array([7.0]), spl_dB=120.0)
        xi = float(res["max_wall_xi_um"][0])
        dV = float(res["total_delta_V_m3"][0]) * 1e9  # nL
        if ref_dV is None:
            ref_dV = dV
        print(f"    {label:>25}: {N_fixed:>4} {xi:>7.3f}μm "
              f"{dV:>9.1f} nL {dV/ref_dV:>5.1f}×")

    print()
    print("  5b. Pocket-size distribution matters: spherical pockets")
    print("      (spherical geometry: ξ depends on radius, unlike cylindrical)")
    print("  " + "-" * (W - 4))
    print(f"  {'Case':>35} {'max ξ':>10} {'PIEZO':>6}")
    print("  " + "-" * (W - 4))
    configs_5b = [
        ("10 × 10 mL (uniform)", [10.0] * 10),
        ("9 × 5 mL + 1 × 55 mL", [5.0] * 9 + [55.0]),
        ("8 × 2 mL + 2 × 92 mL", [2.0] * 8 + [92.0, 92.0]),
        ("1 × 200 mL (single large)", [200.0]),
    ]
    for label, vol_list in configs_5b:
        pockets = [GasPocketParams(volume_mL=v, geometry="spherical",
                                   wall="elastic") for v in vol_list]
        res = multi_pocket_response(pockets, np.array([7.0]), spl_dB=120.0)
        xi = float(res["max_wall_xi_um"][0])
        print(f"    {label:>33}: {xi:>8.3f} μm "
              f"{'YES' if xi > 0.5 else ' no':>6}")

    print()
    print("  5c. SPL threshold for PIEZO activation (0.5 μm)")
    print("  " + "-" * (W - 4))
    for vol, geom in [(5, "spherical"), (20, "spherical"),
                      (50, "spherical"), (100, "spherical"),
                      (10, "cylindrical"), (50, "cylindrical")]:
        p = GasPocketParams(volume_mL=vol, geometry=geom, wall="elastic")
        # Binary search for SPL giving 0.5 μm
        lo, hi = 80.0, 160.0
        for _ in range(50):
            mid = (lo + hi) / 2.0
            r = pocket_response(p, np.array([7.0]), spl_dB=mid)
            if float(r["xi_um"][0]) > 0.5:
                hi = mid
            else:
                lo = mid
        spl_thresh = (lo + hi) / 2.0
        print(f"    {vol:>4} mL {geom:>12}: SPL threshold ≈ {spl_thresh:.0f} dB")

    print("  " + "-" * (W - 4))
    print()
    print("  SUMMARY:")
    print("  • Total volume displacement ΔV scales linearly with total gas → 15×")
    print("    variation across the physiological range (100–1500 mL)")
    print("  • Per-pocket displacement depends on pocket SIZE: a single large")
    print("    pocket (spherical, 200 mL) gives 1.8 μm vs 0.62 μm for 10 mL")
    print("  • Cylindrical pockets are governed by lumen radius (fixed), so")
    print("    individual displacement is ~1 μm regardless of volume")
    print("  • SPL thresholds range from 108–123 dB depending on pocket size")
    print("  • INDIVIDUALS WITH MORE/LARGER GAS POCKETS REQUIRE LOWER SPL")
    print()
    print("=" * W)


# ===================================================================
if __name__ == "__main__":
    print_report()
    print("\nGenerating figures ...")
    fig_frequency_response(save=True)
    fig_variability(save=True)
    plt.close("all")
    print("Done.")
