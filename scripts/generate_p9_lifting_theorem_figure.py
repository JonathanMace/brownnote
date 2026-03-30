"""Generate the singular-value lifting theorem figure for Paper 9.

This script creates a two-panel publication-quality figure:
    (a) condition number kappa versus eccentricity epsilon for the oblate shell
    (b) a conceptual schematic of singular-value lifting

Outputs are saved as both PDF and PNG in:
    papers/paper9-lifting-theorem/figures/
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.analytical.kac_identifiability import CANONICAL_ABDOMEN, jacobian_condition_number
from src.analytical.power_law_proof import fit_power_law, kappa_vs_eccentricity, ritz_curvature_channel


FIG_DIR = ROOT / "papers" / "paper9-lifting-theorem" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

DOUBLE_COL = 174 / 25.4  # inches

# Reuse the repository's common tab10-based publication palette.
COLORS = plt.cm.tab10.colors
C_BLUE, C_ORANGE, C_GREEN, C_RED, C_PURPLE = COLORS[:5]

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "lines.linewidth": 1.8,
        "lines.markersize": 5.5,
        "axes.grid": False,
        "mathtext.default": "regular",
    }
)


def _panel_a(ax: plt.Axes) -> None:
    """Plot kappa vs eccentricity."""
    modes = (2, 3, 4, 5, 6)  # n_modes = 5

    # Requested epsilon window for the final panel.
    eps_data = np.linspace(0.05, 0.75, 20)
    zeta_data = np.sqrt(1.0 - eps_data**2)

    data = kappa_vs_eccentricity(zeta_values=zeta_data, model="ritz", modes=modes)

    # Fit the practical power-law regime away from the near-spherical floor.
    eps_fit = np.linspace(0.20, 0.75, 14)
    zeta_fit = np.sqrt(1.0 - eps_fit**2)
    fit = fit_power_law(modes=modes, zeta_values=zeta_fit)
    fit_curve = fit["C_fit"] * eps_fit ** (-fit["alpha_fit"])

    canonical = dict(CANONICAL_ABDOMEN)
    eps_canonical = float(np.sqrt(1.0 - (canonical["c"] / canonical["a"]) ** 2))
    kappa_canonical = float(jacobian_condition_number(canonical, model="ritz", modes=modes))

    kappa_floor = float(ritz_curvature_channel(modes=modes)["kappa_floor"])

    floor_xmax = 0.12
    ax.axvspan(0.05, floor_xmax, color="0.85", alpha=0.55, zorder=0)
    ax.hlines(
        kappa_floor,
        0.05,
        floor_xmax,
        colors="0.4",
        linestyles=":",
        linewidth=1.4,
        zorder=1,
    )

    ax.plot(
        data["eccentricity"],
        data["kappa"],
        color=C_BLUE,
        marker="o",
        markerfacecolor="white",
        markeredgecolor=C_BLUE,
        linewidth=1.6,
        label="Ritz model data",
        zorder=3,
    )
    ax.plot(
        eps_fit,
        fit_curve,
        color=C_ORANGE,
        linestyle="--",
        linewidth=2.0,
        label=rf"Power-law fit: $\kappa \propto \varepsilon^{{-{fit['alpha_fit']:.2f}}}$",
        zorder=2,
    )

    ax.plot(
        eps_canonical,
        kappa_canonical,
        marker="*",
        markersize=11,
        color=C_RED,
        markeredgecolor="black",
        markeredgewidth=0.5,
        linestyle="None",
        label=rf"Canonical point $(\varepsilon={eps_canonical:.3f},\ \kappa={kappa_canonical:.1f})$",
        zorder=4,
    )

    ax.annotate(
        "Near-spherical\nfloor region",
        xy=(0.075, 235),
        xytext=(0.17, 240),
        fontsize=8.5,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", lw=0.9, color="0.25"),
    )
    ax.annotate(
        "Canonical\noperating point",
        xy=(eps_canonical, kappa_canonical),
        xytext=(0.60, 95),
        fontsize=8.5,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", lw=0.9, color="0.25"),
    )

    ax.set_yscale("log")
    ax.set_xlim(0.05, 0.75)
    ax.set_ylim(60, 320)
    ax.set_xlabel(r"Eccentricity, $\varepsilon$")
    ax.set_ylabel(r"Condition number, $\kappa$")
    ax.set_title(r"Oblate-shell conditioning")
    ax.yaxis.grid(True, which="major", color="0.88", linewidth=0.6)
    ax.tick_params(direction="out", length=4)
    ax.legend(loc="upper right", frameon=False, handlelength=2.8)
    ax.text(-0.16, 1.03, "(a)", transform=ax.transAxes, fontsize=11, fontweight="bold")


def _panel_b(ax: plt.Axes) -> None:
    """Draw the conceptual lifting schematic."""
    delta = np.linspace(0.0, 1.0, 300)
    curvature_floor = 0.12 * np.ones_like(delta)
    shape_channel = 0.74 * delta**2
    total = curvature_floor + shape_channel

    ax.add_patch(
        Rectangle(
            (0.0, 0.0),
            0.10,
            1.0,
            transform=ax.transAxes,
            facecolor="0.95",
            edgecolor="none",
            zorder=0,
        )
    )

    ax.plot(delta, total, color=C_BLUE, linewidth=2.2, label=r"Lifted $\sigma_{\min}$")
    ax.plot(
        delta,
        shape_channel,
        color=C_ORANGE,
        linestyle="--",
        linewidth=1.8,
        label=r"Shape channel $\propto |\delta|^{p}$",
    )
    ax.plot(
        delta,
        curvature_floor,
        color="0.35",
        linestyle=":",
        linewidth=1.8,
        label="Curvature channel",
    )

    ax.plot(0.0, 0.0, marker="o", markersize=6.5, markerfacecolor="white", markeredgecolor="black")
    ax.plot(0.0, curvature_floor[0], marker="o", markersize=5.8, color="0.35")

    ax.annotate(
        r"Sphere: degenerate Jacobian" "\n" r"$\sigma_{\min}=0$",
        xy=(0.0, 0.0),
        xytext=(0.20, 0.16),
        fontsize=8.8,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", lw=0.9, color="0.25"),
    )
    ax.annotate(
        "Curvature channel",
        xy=(0.58, curvature_floor[0]),
        xytext=(0.42, 0.25),
        fontsize=8.8,
        ha="left",
        va="center",
        color="0.25",
        arrowprops=dict(arrowstyle="->", lw=0.9, color="0.25"),
    )
    ax.annotate(
        "Shape channel",
        xy=(0.72, shape_channel[np.searchsorted(delta, 0.72)]),
        xytext=(0.56, 0.53),
        fontsize=8.8,
        ha="left",
        va="center",
        color=C_ORANGE,
        arrowprops=dict(arrowstyle="->", lw=0.9, color=C_ORANGE),
    )
    ax.annotate(
        r"Symmetry broken:" "\n" r"$\sigma_{\min} \sim \sigma_{\mathrm{curv}} + C|\delta|^{p}$",
        xy=(0.82, total[np.searchsorted(delta, 0.82)]),
        xytext=(0.38, 0.83),
        fontsize=8.8,
        ha="left",
        va="center",
        color=C_BLUE,
        arrowprops=dict(arrowstyle="->", lw=0.9, color=C_BLUE),
    )

    ax.text(0.02, 0.93, r"$\varepsilon=0$", transform=ax.transAxes, fontsize=9, ha="left", va="top")
    ax.text(0.62, 0.93, r"$\varepsilon>0$", transform=ax.transAxes, fontsize=9, ha="left", va="top")

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel(r"Symmetry-breaking perturbation, $\delta \sim \varepsilon$")
    ax.set_ylabel(r"Smallest singular value, $\sigma_{\min}$")
    ax.set_title(r"Singular-value lifting mechanism")
    ax.set_xticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax.tick_params(direction="out", length=4)
    ax.legend(loc="lower right", frameon=False, handlelength=2.8)
    ax.text(-0.16, 1.03, "(b)", transform=ax.transAxes, fontsize=11, fontweight="bold")


def main() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_COL, 3.0), constrained_layout=True)

    _panel_a(axes[0])
    _panel_b(axes[1])

    pdf_path = FIG_DIR / "fig_lifting_theorem.pdf"
    png_path = FIG_DIR / "fig_lifting_theorem.png"
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)

    print(f"Saved PDF: {pdf_path}")
    print(f"Saved PNG: {png_path}")


if __name__ == "__main__":
    main()
