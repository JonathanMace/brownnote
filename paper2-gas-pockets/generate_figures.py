#!/usr/bin/env python3
"""
Generate figures for Paper 2: Gas pocket transduction mechanism.

Produces four figures:
  1. Schematic of constrained bubble geometry
  2. SPL threshold vs gas pocket volume
  3. Population distribution of displacement at 120 dB
  4. Comparison: whole-cavity vs gas-pocket pathway
"""

import sys
import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse, Rectangle, Arc
from pathlib import Path

# ---------------------------------------------------------------------------
# Add project source to path so we can import the analytical modules
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from analytical.gas_pocket_detailed import (
    GasPocketParams,
    pocket_response,
    multi_pocket_response,
    population_gas_model,
    resonance_frequency,
    minnaert_frequency,
    damping_ratio,
    RHO_TISSUE,
    C_TISSUE,
    GAMMA,
    P0,
    P_REF,
    E_WALL,
    H_WALL,
    NU_WALL,
)

FIG_DIR = Path(__file__).resolve().parent / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Common style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "legend.fontsize": 8,
    "figure.dpi": 150,
})


# ===================================================================
# Figure 1: Schematic of constrained bubble geometry
# ===================================================================
def fig1_schematic():
    """Schematic showing a gas pocket constrained within a cylindrical
    intestinal lumen, with labels for key physical parameters."""
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5))

    # --- Panel A: Cylindrical geometry (longitudinal cross-section) ---
    ax = axes[0]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-2.0, 2.0)
    ax.set_aspect("equal")
    ax.set_title("(a) Cylindrical gas pocket in bowel lumen", fontsize=10)

    # Intestinal wall (outer tube)
    wall_y = 1.3
    wall_h = 0.25
    ax.add_patch(Rectangle((0.3, wall_y), 3.4, wall_h,
                            facecolor="#d4a574", edgecolor="k", lw=1.2))
    ax.add_patch(Rectangle((0.3, -wall_y - wall_h), 3.4, wall_h,
                            facecolor="#d4a574", edgecolor="k", lw=1.2))

    # Gas pocket (elliptical blob)
    gas = Ellipse((2.0, 0.0), 2.8, 2.0, facecolor="#aaddff",
                  edgecolor="#3377bb", lw=1.5, alpha=0.6)
    ax.add_patch(gas)
    ax.text(2.0, 0.0, "Gas\n($\\gamma P_0$)", ha="center", va="center",
            fontsize=9, color="#225588", fontweight="bold")

    # Tissue/fluid above and below
    ax.text(2.0, 1.8, "Intestinal wall\n($E_w, h_w, \\rho_w$)",
            ha="center", va="center", fontsize=7, color="#8B4513")

    # Dimension arrows
    ax.annotate("", xy=(0.6, -1.6), xytext=(3.4, -1.6),
                arrowprops=dict(arrowstyle="<->", color="k", lw=1.0))
    ax.text(2.0, -1.8, "$L$", ha="center", va="top", fontsize=11)

    ax.annotate("", xy=(3.8, -1.0), xytext=(3.8, 1.0),
                arrowprops=dict(arrowstyle="<->", color="k", lw=1.0))
    ax.text(4.1, 0.0, "$2R$", ha="left", va="center", fontsize=11)

    # Incident pressure arrows
    for y in [-0.6, 0.0, 0.6]:
        ax.annotate("", xy=(0.5, y), xytext=(-0.3, y),
                    arrowprops=dict(arrowstyle="->", color="red", lw=1.2))
    ax.text(-0.4, 0.9, "$p_\\mathrm{inc}$", ha="center", fontsize=11,
            color="red")

    ax.axis("off")

    # --- Panel B: Spherical equivalent (radial cross-section) ---
    ax = axes[1]
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal")
    ax.set_title("(b) Spherical equivalent model", fontsize=10)

    # Tissue background
    tissue = plt.Circle((0, 0), 2.0, facecolor="#ffe8d6", edgecolor="none")
    ax.add_patch(tissue)
    ax.text(1.5, 1.5, "Tissue\n($\\rho_f, c_f$)", fontsize=7,
            ha="center", color="#8B4513")

    # Wall shell
    wall = plt.Circle((0, 0), 1.2, facecolor="#d4a574", edgecolor="k", lw=1.0)
    ax.add_patch(wall)

    # Gas pocket
    gas = plt.Circle((0, 0), 0.95, facecolor="#aaddff", edgecolor="#3377bb",
                     lw=1.5, alpha=0.7)
    ax.add_patch(gas)
    ax.text(0, 0, "Gas\n$V = \\frac{4}{3}\\pi a^3$", ha="center",
            va="center", fontsize=8, color="#225588")

    # Radius arrow
    ax.annotate("", xy=(0.95, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="k", lw=1.2))
    ax.text(0.45, 0.15, "$a$", fontsize=12)

    # Wall thickness
    ax.annotate("", xy=(1.2, -0.5), xytext=(0.95, -0.5),
                arrowprops=dict(arrowstyle="<->", color="#8B4513", lw=1.0))
    ax.text(1.35, -0.5, "$h_w$", fontsize=9, color="#8B4513", va="center")

    # Radial displacement arrows (oscillation)
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = np.radians(angle)
        x0 = 1.2 * np.cos(rad)
        y0 = 1.2 * np.sin(rad)
        dx = 0.35 * np.cos(rad)
        dy = 0.35 * np.sin(rad)
        ax.annotate("", xy=(x0 + dx, y0 + dy), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color="red",
                                    lw=0.8, alpha=0.7))
    ax.text(-2.0, -2.0, "$\\xi(t)$", fontsize=11, color="red")

    ax.axis("off")

    fig.tight_layout()
    path = FIG_DIR / "fig1_geometry_schematic.pdf"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=200, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


# ===================================================================
# Figure 2: SPL threshold vs gas pocket volume
# ===================================================================
def fig2_spl_threshold():
    """Binary-search for the SPL producing 0.5 µm displacement at 7 Hz,
    for both spherical and cylindrical geometries, sweeping volume."""
    volumes = np.logspace(np.log10(1), np.log10(200), 60)
    freq = 7.0
    threshold_um = 0.5

    results = {}
    for geom in ["spherical", "cylindrical"]:
        spls = []
        for vol in volumes:
            p = GasPocketParams(volume_mL=float(vol), geometry=geom,
                                wall="elastic")
            lo, hi = 80.0, 170.0
            for _ in range(60):
                mid = (lo + hi) / 2.0
                r = pocket_response(p, np.array([freq]), spl_dB=mid)
                if float(r["xi_um"][0]) > threshold_um:
                    hi = mid
                else:
                    lo = mid
            spls.append((lo + hi) / 2.0)
        results[geom] = np.array(spls)

    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    ax.plot(volumes, results["spherical"], "o-", ms=3, lw=1.5,
            color="#2266aa", label="Spherical (elastic wall)")
    ax.plot(volumes, results["cylindrical"], "s-", ms=3, lw=1.5,
            color="#cc5500", label="Cylindrical ($R = 15$ mm lumen)")

    # Reference lines
    ax.axhline(120, color="gray", ls="--", lw=0.8, alpha=0.6)
    ax.text(2, 121, "120 dB (threshold of pain)", fontsize=7, color="gray")
    ax.axhline(140, color="gray", ls=":", lw=0.8, alpha=0.6)
    ax.text(2, 141, "140 dB (near jet engine)", fontsize=7, color="gray")

    # Shade the physiological gas pocket range
    ax.axvspan(5, 100, alpha=0.08, color="green")
    ax.text(20, 155, "Typical pocket\nsize range", fontsize=7,
            color="green", ha="center", style="italic")

    ax.set_xscale("log")
    ax.set_xlabel("Gas pocket volume [mL]")
    ax.set_ylabel("SPL threshold for PIEZO activation [dB]")
    ax.set_title("SPL required for 0.5 µm wall displacement at 7 Hz")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.set_ylim(100, 165)
    ax.set_xlim(1, 200)
    ax.grid(True, alpha=0.3, which="both")

    fig.tight_layout()
    path = FIG_DIR / "fig2_spl_threshold_vs_volume.pdf"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=200, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


# ===================================================================
# Figure 3: Population distribution at 120 dB
# ===================================================================
def fig3_population():
    """Monte Carlo population variability — displacement distribution."""
    print("  Running Monte Carlo (N=10,000) — this takes a moment...")
    pop = population_gas_model(n_individuals=10_000, seed=42)

    fig, axes = plt.subplots(2, 2, figsize=(7.5, 6.5))

    # (a) Total bowel gas histogram
    ax = axes[0, 0]
    ax.hist(pop["total_gas_mL"], bins=80, color="steelblue",
            edgecolor="none", alpha=0.85)
    ax.axvline(np.median(pop["total_gas_mL"]), color="k", ls="--", lw=0.8,
               label=f'Median = {np.median(pop["total_gas_mL"]):.0f} mL')
    ax.set_xlabel("Total bowel gas [mL]")
    ax.set_ylabel("Count")
    ax.set_title("(a) Total bowel gas distribution")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (b) Max displacement histogram
    ax = axes[0, 1]
    ax.hist(pop["max_xi_um"], bins=80, color="darkorange",
            edgecolor="none", alpha=0.85)
    ax.axvline(0.5, color="red", ls="--", lw=1.0,
               label="PIEZO threshold (0.5 µm)")
    ax.set_xlabel("Max pocket-wall displacement [µm]")
    ax.set_ylabel("Count")
    ax.set_title("(b) Displacement distribution (7 Hz, 120 dB)")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (c) Scatter: gas volume vs displacement
    ax = axes[1, 0]
    ax.scatter(pop["total_gas_mL"], pop["max_xi_um"], s=1, alpha=0.12,
               color="teal")
    ax.axhline(0.5, color="red", ls="--", lw=0.8)
    ax.set_xlabel("Total bowel gas [mL]")
    ax.set_ylabel("Max wall displacement [µm]")
    ax.set_title("(c) Gas volume vs. displacement")
    ax.set_xlim(0, 1500)
    ax.grid(True, alpha=0.3)

    # (d) CDF with threshold
    ax = axes[1, 1]
    sorted_xi = np.sort(pop["max_xi_um"])
    cdf = np.arange(1, len(sorted_xi) + 1) / len(sorted_xi)
    ax.plot(sorted_xi, cdf, color="navy", lw=1.5)
    ax.axvline(0.5, color="red", ls="--", lw=0.8, label="PIEZO threshold")
    frac_above = np.mean(pop["max_xi_um"] > 0.5) * 100
    ax.text(
        max(sorted_xi) * 0.6, 0.15,
        f"{frac_above:.0f}% exceed\nPIEZO threshold",
        fontsize=9, color="red", fontweight="bold",
    )
    ax.set_xlabel("Max wall displacement [µm]")
    ax.set_ylabel("Cumulative fraction")
    ax.set_title("(d) Population CDF")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    fig.suptitle(
        "Population variability in gas-pocket response\n"
        "(7 Hz, 120 dB SPL, $N = 10\\,000$)",
        fontsize=12, fontweight="bold", y=1.02,
    )
    fig.tight_layout()
    path = FIG_DIR / "fig3_population_variability.pdf"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=200, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


# ===================================================================
# Figure 4: Whole-cavity vs gas-pocket comparison
# ===================================================================
def fig4_comparison():
    """Compare whole-cavity airborne path with gas-pocket transduction."""
    spl_range = np.linspace(80, 150, 200)
    freq = 7.0
    p_ref = 20e-6

    # --- Whole-cavity path (from mechanotransduction.py v2 model) ---
    # Flexural n=2 mode: f ~ 4.5 Hz, ka coupling
    # Using simplified model parameters from paper 1
    R_abd = 0.16          # equivalent abdominal radius [m]
    E_abd = 0.1e6         # abdominal wall modulus [Pa]
    h_abd = 0.02          # abdominal wall thickness [m]
    nu_abd = 0.45
    Q_abd = 5.0
    n_mode = 2
    f_n2 = 4.5            # flexural n=2 frequency [Hz]
    ka = 2 * np.pi * f_n2 * R_abd / 343.0

    # Modal stiffness (simplified)
    D = E_abd * h_abd**3 / (12 * (1 - nu_abd**2))
    K_bend = n_mode * (n_mode - 1) * (n_mode + 2)**2 * D / R_abd**4
    lam_n = (n_mode**2 + n_mode - 2 + 2*nu_abd) / (n_mode**2 + n_mode + 1 - nu_abd)
    K_memb = E_abd * h_abd / R_abd**2 * lam_n
    P_iap = 1500.0  # intra-abdominal pressure [Pa]
    K_pre = P_iap / R_abd * (n_mode - 1) * (n_mode + 2)
    K_total = K_bend + K_memb + K_pre

    p_inc = p_ref * 10**(spl_range / 20)
    p_eff_cavity = p_inc * ka**n_mode
    xi_cavity_um = p_eff_cavity / K_total * Q_abd * 1e6

    # --- Gas pocket path: representative pockets ---
    xi_gp_100mL = np.zeros_like(spl_range)
    xi_gp_20mL = np.zeros_like(spl_range)
    xi_gp_5mL = np.zeros_like(spl_range)

    for i, spl in enumerate(spl_range):
        r100 = pocket_response(
            GasPocketParams(volume_mL=100, geometry="spherical", wall="elastic"),
            np.array([freq]), spl_dB=spl,
        )
        r20 = pocket_response(
            GasPocketParams(volume_mL=20, geometry="cylindrical", wall="elastic"),
            np.array([freq]), spl_dB=spl,
        )
        r5 = pocket_response(
            GasPocketParams(volume_mL=5, geometry="cylindrical", wall="elastic"),
            np.array([freq]), spl_dB=spl,
        )
        xi_gp_100mL[i] = float(r100["xi_um"][0])
        xi_gp_20mL[i] = float(r20["xi_um"][0])
        xi_gp_5mL[i] = float(r5["xi_um"][0])

    fig, ax = plt.subplots(figsize=(6.0, 4.5))

    # Whole-cavity
    ax.semilogy(spl_range, xi_cavity_um, "k--", lw=2.0, alpha=0.7,
                label="Whole-cavity (n=2 flexural)")

    # Gas pockets
    ax.semilogy(spl_range, xi_gp_100mL, "-", lw=1.8, color="#2266aa",
                label="Gas pocket: 100 mL (spherical)")
    ax.semilogy(spl_range, xi_gp_20mL, "-", lw=1.8, color="#cc5500",
                label="Gas pocket: 20 mL (cylindrical)")
    ax.semilogy(spl_range, xi_gp_5mL, "-", lw=1.8, color="#228833",
                label="Gas pocket: 5 mL (cylindrical)")

    # PIEZO threshold
    ax.axhline(0.5, color="red", ls=":", lw=1.0, alpha=0.7)
    ax.text(82, 0.55, "PIEZO threshold (0.5 µm)", fontsize=8, color="red")

    # Annotations
    ax.fill_betweenx([1e-6, 100], 80, 120, alpha=0.05, color="green")
    ax.text(100, 30, "Occupational\nexposure range", fontsize=7,
            color="green", ha="center", style="italic", alpha=0.7)

    ax.set_xlabel("Sound Pressure Level [dB re 20 µPa]")
    ax.set_ylabel("Tissue displacement amplitude [µm]")
    ax.set_title("Whole-cavity vs. gas-pocket transduction at 7 Hz")
    ax.set_xlim(80, 150)
    ax.set_ylim(1e-6, 50)
    ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3, which="both")

    fig.tight_layout()
    path = FIG_DIR / "fig4_pathway_comparison.pdf"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=200, bbox_inches="tight")
    print(f"  Saved: {path}")
    plt.close(fig)


# ===================================================================
if __name__ == "__main__":
    print("Generating Paper 2 figures...")
    print()
    fig1_schematic()
    fig2_spl_threshold()
    fig3_population()
    fig4_comparison()
    print()
    print("All figures generated.")
