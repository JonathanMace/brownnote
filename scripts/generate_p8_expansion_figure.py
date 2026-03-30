"""Generate the sigma_min expansion-fit figure for Paper 8."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import svd


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.analytical.kac_identifiability import CANONICAL_ABDOMEN, compute_jacobian
from src.analytical.power_law_proof import sigma_min_expansion


FIG_DIR = ROOT / "papers" / "paper8-kac" / "figures"
FIG_STEM = FIG_DIR / "fig_expansion_fit"
MODES = (2, 3, 4, 5, 6)

SIGMA_0 = 0.01113
LAMBDA_1 = 0.00507
LAMBDA_2 = 0.02401

EPS_MIN = 0.01
EPS_MAX = 0.75
SINGLE_COL = 84.0 / 25.4

CB_BLUE = "#0072B2"
CB_ORANGE = "#D55E00"
CB_GREEN = "#009E73"
GRID = "#B8B8B8"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
        "font.size": 9,
        "axes.labelsize": 10,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.04,
        "axes.linewidth": 0.7,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "lines.linewidth": 1.8,
        "lines.markersize": 5.2,
        "mathtext.default": "regular",
    }
)


def _canonical_sigma_min() -> tuple[float, float]:
    """Return the canonical eccentricity and corresponding Ritz sigma_min."""
    params = dict(CANONICAL_ABDOMEN)
    epsilon = float(np.sqrt(1.0 - (params["c"] / params["a"]) ** 2))
    jacobian = compute_jacobian(params, model="ritz", modes=MODES, scaled=True)
    sigma = svd(jacobian, compute_uv=False)
    return epsilon, float(sigma[-1])


def main() -> None:
    """Generate and save the publication-quality expansion-fit figure."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    result = sigma_min_expansion(modes=MODES)
    eps_all = np.asarray(result["eps"], dtype=float)
    sigma_all = np.asarray(result["sigma_min"], dtype=float)
    mask = (eps_all >= EPS_MIN) & (eps_all <= EPS_MAX)
    eps_data = eps_all[mask]
    sigma_data = sigma_all[mask]

    eps_curve = np.linspace(EPS_MIN, EPS_MAX, 400)
    sigma_fit = SIGMA_0 + LAMBDA_1 * eps_curve**2 + LAMBDA_2 * eps_curve**4

    eps_canonical, sigma_canonical = _canonical_sigma_min()

    fig, ax = plt.subplots(figsize=(SINGLE_COL, SINGLE_COL * 0.76))
    ax.scatter(
        eps_data,
        sigma_data,
        s=28,
        color=CB_BLUE,
        edgecolors="white",
        linewidths=0.45,
        zorder=3,
        label="Ritz data",
    )
    ax.plot(
        eps_curve,
        sigma_fit,
        color=CB_ORANGE,
        linewidth=2.0,
        zorder=2,
        label=r"Expansion fit: $\sigma_0 + \lambda_1 \varepsilon^2 + \lambda_2 \varepsilon^4$",
    )
    ax.plot(
        eps_canonical,
        sigma_canonical,
        marker="D",
        markersize=6,
        linestyle="None",
        color=CB_GREEN,
        markeredgecolor="black",
        markeredgewidth=0.5,
        zorder=4,
        label=rf"Canonical abdomen ($\varepsilon={eps_canonical:.3f}$)",
    )

    coeff_text = (
        r"$\sigma_0 = 0.01113$" "\n"
        r"$\lambda_1 = 0.00507$" "\n"
        r"$\lambda_2 = 0.02401$"
    )
    ax.text(
        0.035,
        0.965,
        coeff_text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "0.65"},
    )

    ax.annotate(
        rf"$(\varepsilon={eps_canonical:.3f},\ \sigma_{{\min}}={sigma_canonical:.4f})$",
        xy=(eps_canonical, sigma_canonical),
        xytext=(0.47, 0.18),
        textcoords="axes fraction",
        fontsize=8,
        ha="left",
        va="bottom",
        arrowprops={"arrowstyle": "->", "lw": 0.9, "color": "0.25"},
    )

    ax.set_xlim(EPS_MIN, EPS_MAX + 0.01)
    y_min = min(np.min(sigma_data), np.min(sigma_fit))
    y_max = max(np.max(sigma_data), np.max(sigma_fit), sigma_canonical)
    pad = 0.08 * (y_max - y_min)
    ax.set_ylim(y_min - pad, y_max + pad)
    ax.set_xlabel(r"Eccentricity, $\varepsilon$")
    ax.set_ylabel(r"Minimum singular value, $\sigma_{\min}$")
    ax.grid(True, color=GRID, linewidth=0.75, alpha=0.8)
    ax.tick_params(direction="out", length=4)
    ax.legend(loc="lower right", frameon=False, handlelength=2.8)

    fig.savefig(FIG_STEM.with_suffix(".pdf"))
    fig.savefig(FIG_STEM.with_suffix(".png"), dpi=300)
    plt.close(fig)

    print(f"Saved {FIG_STEM.with_suffix('.pdf')}")
    print(f"Saved {FIG_STEM.with_suffix('.png')}")
    print(
        "Fitted coefficients from numerical data: "
        f"sigma_0={result['sigma_0']:.8f}, "
        f"lambda_1={result['lambda_1']:.8f}, "
        f"lambda_2={result['lambda_2']:.8f}"
    )


if __name__ == "__main__":
    main()
