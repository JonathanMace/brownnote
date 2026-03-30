"""
Generate the oblate-versus-prolate identifiability contrast figure for Paper 8.

Outputs
-------
- papers/paper8-kac/figures/fig_oblate_prolate_comparison.pdf
- papers/paper8-kac/figures/fig_oblate_prolate_comparison.png
"""

from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import svd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
src_dir = os.path.join(ROOT, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from src.analytical.kac_identifiability import CANONICAL_ABDOMEN, compute_jacobian
from src.analytical.power_law_proof import ritz_curvature_channel, sigma_min_expansion
from src.analytical.universality import (
    _compute_jacobian_generic,
    _forward_prolate,
    oblate_condition_sweep,
    prolate_condition_sweep,
)


CB_BLUE = "#4477AA"
CB_RED = "#CC3311"
CB_GREY = "#888888"

JSV_RC = {
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "axes.grid": True,
    "grid.color": "#D0D0D0",
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "lines.linewidth": 1.8,
}
plt.rcParams.update(JSV_RC)

DOUBLE_COL = 174.0 / 25.4
FIG_DIR = os.path.join(ROOT, "papers", "paper8-kac", "figures")
OUT_STEM = os.path.join(FIG_DIR, "fig_oblate_prolate_comparison")
MODES = (2, 3, 4, 5, 6)


def _prolate_sigma_min(eccentricity: float) -> float:
    a_val = CANONICAL_ABDOMEN["a"]
    params = {
        "a": a_val,
        "c": a_val / np.sqrt(1.0 - eccentricity**2),
        "h": CANONICAL_ABDOMEN["h"],
        "E": CANONICAL_ABDOMEN["E"],
        "nu": CANONICAL_ABDOMEN["nu"],
        "rho_w": CANONICAL_ABDOMEN["rho_w"],
        "rho_f": CANONICAL_ABDOMEN["rho_f"],
        "K_f": CANONICAL_ABDOMEN["K_f"],
        "P_iap": CANONICAL_ABDOMEN["P_iap"],
    }
    jacobian = _compute_jacobian_generic(
        params,
        _forward_prolate,
        modes=MODES,
        scaled=True,
    )
    return float(svd(jacobian, compute_uv=False)[-1])


def _oblate_sigma_min(eccentricity: float) -> float:
    params = dict(CANONICAL_ABDOMEN)
    params["c"] = params["a"] * np.sqrt(1.0 - eccentricity**2)
    jacobian = compute_jacobian(
        params,
        model="ritz",
        modes=MODES,
        scaled=True,
    )
    return float(svd(jacobian, compute_uv=False)[-1])


def main() -> None:
    os.makedirs(FIG_DIR, exist_ok=True)

    eccentricity = np.linspace(0.05, 0.95, 20)
    oblate = oblate_condition_sweep(eccentricity, modes=MODES)
    prolate = prolate_condition_sweep(eccentricity, modes=MODES)

    sigma_oblate = np.array([_oblate_sigma_min(eps) for eps in eccentricity])
    sigma_prolate = np.array([_prolate_sigma_min(eps) for eps in eccentricity])

    curvature_floor = ritz_curvature_channel(modes=MODES, zeta_sphere=0.99995)
    sigma_fit = sigma_min_expansion(modes=MODES)
    kappa_floor = float(curvature_floor["kappa_floor"])
    sigma_0 = float(sigma_fit["sigma_0"])
    prolate_midrange = (eccentricity >= 0.15) & (eccentricity <= 0.80)

    canonical_eps = np.sqrt(1.0 - (CANONICAL_ABDOMEN["c"] / CANONICAL_ABDOMEN["a"]) ** 2)
    canonical_kappa = float(
        oblate_condition_sweep(np.array([canonical_eps]), modes=MODES)["kappa"][0]
    )

    prolate_kappa_plot = np.full_like(prolate["kappa"], np.nan, dtype=float)
    prolate_kappa_plot[prolate_midrange] = prolate["kappa"][prolate_midrange]
    sigma_prolate_plot = np.full_like(sigma_prolate, np.nan, dtype=float)
    sigma_prolate_plot[prolate_midrange] = sigma_prolate[prolate_midrange]

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(DOUBLE_COL, DOUBLE_COL * 0.36),
        constrained_layout=True,
    )

    ax = axes[0]
    ax.plot(
        eccentricity,
        oblate["kappa"],
        color=CB_BLUE,
        linestyle="-",
        label="Oblate",
        zorder=3,
    )
    ax.plot(
        eccentricity,
        prolate_kappa_plot,
        color=CB_RED,
        linestyle="--",
        label="Prolate",
        zorder=3,
    )
    ax.axhline(
        kappa_floor,
        color=CB_GREY,
        linestyle=":",
        linewidth=1.2,
        label=rf"$\kappa_{{\mathrm{{floor}}}} \approx {kappa_floor:.0f}$",
        zorder=2,
    )
    ax.scatter(
        [canonical_eps],
        [canonical_kappa],
        marker="*",
        s=110,
        facecolor="#FDB515",
        edgecolor="black",
        linewidth=0.5,
        zorder=4,
        label="Canonical oblate",
    )
    ax.set_yscale("log")
    ax.set_xlim(0.0, 0.95)
    ax.set_ylim(10, 1e3)
    ax.set_xlabel(r"Eccentricity $\varepsilon$")
    ax.set_ylabel(r"Condition number $\kappa$")
    ax.text(0.02, 0.97, "(a)", transform=ax.transAxes, ha="left", va="top", fontweight="bold")
    ax.annotate(
        rf"$(\varepsilon={canonical_eps:.2f},\,\kappa={canonical_kappa:.1f})$",
        xy=(canonical_eps, canonical_kappa),
        xytext=(0.56, 0.22),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "-", "lw": 0.8, "color": "#444444"},
        fontsize=8,
    )
    ax.legend(loc="upper right", frameon=True, framealpha=0.95)

    ax = axes[1]
    ax.plot(
        eccentricity,
        sigma_oblate,
        color=CB_BLUE,
        linestyle="-",
        label="Oblate",
        zorder=3,
    )
    ax.plot(
        eccentricity,
        sigma_prolate_plot,
        color=CB_RED,
        linestyle="--",
        label="Prolate",
        zorder=3,
    )
    ax.axhline(
        sigma_0,
        color=CB_GREY,
        linestyle=":",
        linewidth=1.2,
        label=rf"$\sigma_0 \approx {sigma_0:.3f}$",
        zorder=2,
    )
    ax.set_xlim(0.0, 0.95)
    ax.set_ylim(0.0, max(0.125, 1.05 * np.nanmax(sigma_oblate)))
    ax.set_xlabel(r"Eccentricity $\varepsilon$")
    ax.set_ylabel(r"Minimum singular value $\sigma_{\min}$")
    ax.text(0.02, 0.97, "(b)", transform=ax.transAxes, ha="left", va="top", fontweight="bold")

    for axis in axes:
        axis.grid(True, which="major", alpha=0.8)
        axis.grid(False, which="minor")

    fig.savefig(OUT_STEM + ".pdf")
    fig.savefig(OUT_STEM + ".png", dpi=300)
    plt.close(fig)

    print(f"Saved {OUT_STEM}.pdf")
    print(f"Saved {OUT_STEM}.png")
    print(f"Canonical oblate point: eps={canonical_eps:.6f}, kappa={canonical_kappa:.3f}")
    print(f"kappa_floor={kappa_floor:.3f}, sigma_0={sigma_0:.6f}")


if __name__ == "__main__":
    main()
