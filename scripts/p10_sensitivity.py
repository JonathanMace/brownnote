#!/usr/bin/env python3
"""Paper 10 — Robustness sensitivity study for identifiability lifting.

Addresses Reviewer D's concern that the lifting result κ=69.4 may be too
local.  Tests parameter variations, mode-set changes, aspect ratio sweeps,
and numerical convergence of the quadrature scheme.

Generates: papers/paper10-capstone/figures/fig_sensitivity.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from analytical.kac_identifiability import (
    CANONICAL_ABDOMEN,
    DEFAULT_MODES,
    INVERSION_PARAMS,
    jacobian_condition_number,
    kappa_vs_eccentricity,
)
from analytical.oblate_spheroid_ritz import oblate_ritz_frequencies

# ───────────────────────────────────────────────────────────────────────
#  Helpers
# ───────────────────────────────────────────────────────────────────────

def _kappa_with_override(overrides: dict, model: str = "ritz",
                         modes: tuple[int, ...] = DEFAULT_MODES) -> float:
    """Compute κ with selected parameter overrides."""
    p = dict(CANONICAL_ABDOMEN)
    p.update(overrides)
    return jacobian_condition_number(p, model=model, modes=modes)


def _kappa_at_nquad(n_quad: int, params: dict | None = None,
                    modes: tuple[int, ...] = DEFAULT_MODES,
                    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
                    step_fraction: float = 1e-6) -> float:
    """Build the scaled Jacobian from raw oblate_ritz_frequencies at a
    given quadrature order, bypassing the hardcoded n_quad=200 in the
    convenience API.  Returns κ(J_scaled)."""
    if params is None:
        params = dict(CANONICAL_ABDOMEN)

    def _forward(p, ms):
        fd = oblate_ritz_frequencies(
            a=p["a"], c=p["c"], h=p["h"], E=p["E"], nu=p["nu"],
            rho_w=p["rho_w"], rho_f=p["rho_f"], P_iap=p["P_iap"],
            n_target=ms, n_quad=n_quad,
        )
        return np.array([fd[n] for n in ms])

    n_freq = len(modes)
    n_param = len(inversion_params)
    J = np.zeros((n_freq, n_param))

    for j, pname in enumerate(inversion_params):
        p0 = params[pname]
        dp = abs(p0) * step_fraction
        if dp == 0:
            dp = step_fraction

        pp = dict(params); pp[pname] = p0 + dp
        pm = dict(params); pm[pname] = p0 - dp
        J[:, j] = (_forward(pp, modes) - _forward(pm, modes)) / (2.0 * dp)

    f_nom = _forward(params, modes)
    theta = np.array([params[k] for k in inversion_params])
    J_scaled = J * theta[np.newaxis, :] / f_nom[:, np.newaxis]
    return float(np.linalg.cond(J_scaled))


# ───────────────────────────────────────────────────────────────────────
#  Panel (a): Parameter robustness — E sweep
# ───────────────────────────────────────────────────────────────────────

def panel_a():
    """Sweep E from 0.01 to 1.0 MPa; compute κ_oblate and κ_sphere."""
    E_values = np.logspace(np.log10(0.01e6), np.log10(1.0e6), 20)
    kappa_ritz = np.empty(len(E_values))
    kappa_sphere = np.empty(len(E_values))

    for i, E in enumerate(E_values):
        kappa_ritz[i] = _kappa_with_override({"E": E}, model="ritz")
        kappa_sphere[i] = _kappa_with_override({"E": E}, model="sphere")

    # Also sweep h and rho_f (report numbers, not plotted)
    h_values = np.linspace(0.005, 0.020, 7)
    rho_f_values = np.linspace(500, 1500, 7)

    kappa_h = [_kappa_with_override({"h": h}) for h in h_values]
    kappa_rho = [_kappa_with_override({"rho_f": rho}) for rho in rho_f_values]

    print("\n=== Panel (a): Parameter robustness ===")
    print(f"  E range: {E_values[0]/1e6:.3f}–{E_values[-1]/1e6:.3f} MPa")
    print(f"  κ_oblate range: {kappa_ritz.min():.1f}–{kappa_ritz.max():.1f}")
    print(f"  κ_sphere range: {kappa_sphere.min():.1e}–{kappa_sphere.max():.1e}")
    print(f"  h sweep ({h_values[0]:.3f}–{h_values[-1]:.3f} m): "
          f"κ_oblate {min(kappa_h):.1f}–{max(kappa_h):.1f}")
    print(f"  ρ_f sweep ({rho_f_values[0]:.0f}–{rho_f_values[-1]:.0f} kg/m³): "
          f"κ_oblate {min(kappa_rho):.1f}–{max(kappa_rho):.1f}")

    return E_values / 1e6, kappa_ritz, kappa_sphere


# ───────────────────────────────────────────────────────────────────────
#  Panel (b): Mode-set robustness
# ───────────────────────────────────────────────────────────────────────

def panel_b():
    """Compare κ across different mode sets (all overdetermined, ≥4 modes)."""
    mode_sets = {
        "{2,3,4,5}": (2, 3, 4, 5),
        "{2,3,4,5,6}": (2, 3, 4, 5, 6),
        "{2,3,4,5,6,7,8}": (2, 3, 4, 5, 6, 7, 8),
    }

    # Leave-one-out from canonical set {2,...,6}
    canonical = [2, 3, 4, 5, 6]
    for drop in canonical:
        subset = tuple(n for n in canonical if n != drop)
        mode_sets[f"−n={drop}"] = subset

    labels = []
    kappas_oblate = []
    kappas_sphere = []

    for label, modes in mode_sets.items():
        ko = jacobian_condition_number(CANONICAL_ABDOMEN, model="ritz", modes=modes)
        ks = jacobian_condition_number(CANONICAL_ABDOMEN, model="sphere", modes=modes)
        labels.append(label)
        kappas_oblate.append(ko)
        kappas_sphere.append(ks)

    print("\n=== Panel (b): Mode-set robustness ===")
    for lb, ko, ks in zip(labels, kappas_oblate, kappas_sphere):
        print(f"  {lb:18s}: κ_oblate={ko:8.1f}, κ_sphere={ks:.2e}")

    return labels, kappas_oblate, kappas_sphere


# ───────────────────────────────────────────────────────────────────────
#  Panel (c): Aspect ratio sweep
# ───────────────────────────────────────────────────────────────────────

def panel_c():
    """Sweep c/a from 0.50 to 0.95."""
    zeta_vals = np.linspace(0.50, 0.95, 25)
    result = kappa_vs_eccentricity(zeta_values=zeta_vals)

    print("\n=== Panel (c): Aspect ratio sweep ===")
    for z, k in zip(result["zeta"], result["kappa"]):
        if np.isfinite(k):
            print(f"  c/a={z:.3f}: κ={k:.1f}")
        else:
            print(f"  c/a={z:.3f}: κ=∞ (singular)")
    print(f"  Power-law fit: κ ~ {result['fit_C']:.1f} · ε^{{−{result['fit_alpha']:.2f}}}, "
          f"R²={result['fit_r_squared']:.4f}")

    return result


# ───────────────────────────────────────────────────────────────────────
#  Panel (d): Quadrature convergence
# ───────────────────────────────────────────────────────────────────────

def panel_d():
    """Vary n_quad in the Ritz model; show κ converges."""
    n_quad_values = [10, 20, 50, 100, 200, 400]
    kappas = []

    for nq in n_quad_values:
        k = _kappa_at_nquad(nq)
        kappas.append(k)

    print("\n=== Panel (d): Quadrature convergence ===")
    for nq, k in zip(n_quad_values, kappas):
        print(f"  n_quad={nq:4d}: κ={k:.2f}")

    # Relative change from n_quad=200 to n_quad=400
    ref = kappas[n_quad_values.index(200)]
    final = kappas[-1]
    print(f"  Relative change (200→400): {abs(final - ref)/ref*100:.4f}%")

    return n_quad_values, kappas


# ───────────────────────────────────────────────────────────────────────
#  Figure generation
# ───────────────────────────────────────────────────────────────────────

def make_figure(data_a, data_b, data_c, data_d, outpath: str):
    """Generate 2×2 sensitivity panel figure."""
    fig, axes = plt.subplots(2, 2, figsize=(7.5, 6.5))
    fig.subplots_adjust(hspace=0.38, wspace=0.35)

    # ── Panel (a): κ vs E ──
    ax = axes[0, 0]
    E_mpa, kr, ks = data_a
    ax.semilogy(E_mpa, kr, "o-", color="C0", ms=4, lw=1.2, label=r"$\kappa_\mathrm{oblate}$")
    ax.semilogy(E_mpa, ks, "s--", color="C3", ms=4, lw=1.2, label=r"$\kappa_\mathrm{sphere}$")
    ax.set_xscale("log")
    ax.set_xlabel("$E$ (MPa)")
    ax.set_ylabel(r"$\kappa$")
    ax.set_title("(a) Parameter robustness")
    ax.legend(fontsize=8, loc="center right")
    ax.axvline(0.1, color="grey", ls=":", lw=0.8, alpha=0.6)

    # ── Panel (b): κ vs mode set ──
    ax = axes[0, 1]
    labels, ko_list, ks_list = data_b
    x = np.arange(len(labels))
    width = 0.35
    ax.bar(x - width/2, ko_list, width, color="C0", label=r"$\kappa_\mathrm{oblate}$")
    ax.bar(x + width/2, ks_list, width, color="C3", label=r"$\kappa_\mathrm{sphere}$")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    ax.set_ylabel(r"$\kappa$")
    ax.set_title("(b) Mode-set robustness")
    ax.legend(fontsize=7, loc="upper left")

    # ── Panel (c): κ vs c/a ──
    ax = axes[1, 0]
    result_c = data_c
    mask = np.isfinite(result_c["kappa"])
    ax.semilogy(result_c["zeta"][mask], result_c["kappa"][mask],
                "o-", color="C0", ms=4, lw=1.2)
    ax.axvline(0.667, color="grey", ls=":", lw=0.8, alpha=0.6, label="canonical $c/a$")
    ax.set_xlabel("$c/a$")
    ax.set_ylabel(r"$\kappa_\mathrm{oblate}$")
    ax.set_title("(c) Aspect ratio sweep")
    ax.legend(fontsize=8)

    # ── Panel (d): κ vs n_quad ──
    ax = axes[1, 1]
    nq_vals, kq_vals = data_d
    ax.plot(nq_vals, kq_vals, "o-", color="C0", ms=5, lw=1.2)
    ax.set_xlabel("$N_\\mathrm{quad}$")
    ax.set_ylabel(r"$\kappa_\mathrm{oblate}$")
    ax.set_title("(d) Quadrature convergence")
    ax.set_xscale("log")

    for a in axes.flat:
        a.tick_params(labelsize=8)

    fig.savefig(outpath, bbox_inches="tight", dpi=300)
    fig.savefig(outpath.replace(".pdf", ".png"), bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"\nFigure saved: {outpath}")


# ───────────────────────────────────────────────────────────────────────
#  Main
# ───────────────────────────────────────────────────────────────────────

def main():
    print("Paper 10 — Robustness sensitivity study")
    print("=" * 50)

    # Canonical baseline
    k_canon = jacobian_condition_number(CANONICAL_ABDOMEN, model="ritz")
    k_sphere = jacobian_condition_number(CANONICAL_ABDOMEN, model="sphere")
    print(f"\nCanonical: κ_oblate={k_canon:.1f}, κ_sphere={k_sphere:.2e}")

    data_a = panel_a()
    data_b = panel_b()
    data_c = panel_c()
    data_d = panel_d()

    # Generate figure
    outdir = Path(__file__).resolve().parents[1] / "papers" / "paper10-capstone" / "figures"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = str(outdir / "fig_sensitivity.pdf")
    make_figure(data_a, data_b, data_c, data_d, outpath)

    # Summary
    E_mpa, kr, ks = data_a
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"κ_oblate across all E values:  {kr.min():.1f}–{kr.max():.1f}")
    print(f"κ_sphere across all E values:  {ks.min():.1e}–{ks.max():.1e}")
    print(f"Lifting persists across 100× E variation: "
          f"gap ≥ {(ks.min()/kr.max()):.0e}×")

    labels, ko_list, _ = data_b
    print(f"κ_oblate across mode sets:     {min(ko_list):.1f}–{max(ko_list):.1f}")

    result_c = data_c
    finite_k = result_c["kappa"][np.isfinite(result_c["kappa"])]
    print(f"κ_oblate across c/a sweep:     {finite_k.min():.1f}–{finite_k.max():.1f}")

    nq, kq = data_d
    print(f"κ_oblate converged value:      {kq[-1]:.2f} (n_quad=400)")


if __name__ == "__main__":
    main()
