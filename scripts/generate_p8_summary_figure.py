#!/usr/bin/env python3
"""Generate Paper 8 take-home summary figure: κ vs ε with annotated regimes.

Produces a single figure showing condition number κ(J_s) as a function of
eccentricity ε for oblate and prolate branches, with annotated regions for
the three identifiability regimes (singular, regular bounded, non-lifting).

Output: papers/paper8-kac/figures/fig_summary_identifiability.{pdf,png}
"""

import sys
import os
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Ensure the repo root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analytical.kac_identifiability import (
    CANONICAL_ABDOMEN,
    DEFAULT_MODES,
    INVERSION_PARAMS,
    jacobian_condition_number,
)


def compute_oblate_sweep(n_points=40):
    """Sweep ζ = c/a for oblate shells, compute κ at each point."""
    zeta_values = np.linspace(0.05, 0.995, n_points)
    eps_values = np.sqrt(1.0 - zeta_values**2)
    kappa_values = np.full_like(eps_values, np.nan)

    base = dict(CANONICAL_ABDOMEN)
    a_fixed = base['a']

    for i, zeta in enumerate(zeta_values):
        params = dict(base)
        params['c'] = a_fixed * zeta
        try:
            kappa_values[i] = jacobian_condition_number(
                params, model='ritz', modes=DEFAULT_MODES,
                inversion_params=INVERSION_PARAMS,
            )
        except Exception:
            kappa_values[i] = np.nan

    return eps_values, kappa_values


def compute_prolate_sweep(n_points=25):
    """Sweep eccentricity for prolate shells at fixed R_eq."""
    base = dict(CANONICAL_ABDOMEN)
    R_eq = (base['a']**2 * base['c'])**(1.0 / 3.0)

    eps_values = np.linspace(0.30, 0.65, n_points)
    kappa_values = np.full_like(eps_values, np.nan)

    for i, eps in enumerate(eps_values):
        # Prolate: a < c, ε = sqrt(1 - (a/c)^2)
        # At fixed R_eq = (a^2 c)^{1/3}: a = R_eq * (1 - eps^2)^{1/6} * (factor)
        # a^2 * c = R_eq^3, and a/c = sqrt(1 - eps^2)
        ratio = np.sqrt(1.0 - eps**2)  # a/c
        # a^2 * c = R_eq^3  =>  a^2 * (a/ratio) = R_eq^3  =>  a^3/ratio = R_eq^3
        a_prolate = R_eq * ratio**(1.0 / 3.0)
        c_prolate = a_prolate / ratio

        params = dict(base)
        params['a'] = a_prolate
        params['c'] = c_prolate
        try:
            kappa_values[i] = jacobian_condition_number(
                params, model='ritz', modes=DEFAULT_MODES,
                inversion_params=INVERSION_PARAMS,
            )
        except Exception:
            kappa_values[i] = np.nan

    return eps_values, kappa_values


def make_summary_figure(output_dir):
    """Create the take-home summary figure."""
    print("Computing oblate sweep...")
    eps_oblate, kappa_oblate = compute_oblate_sweep()
    print("Computing prolate sweep...")
    eps_prolate, kappa_prolate = compute_prolate_sweep()

    # Canonical operating point
    canon_eps = np.sqrt(1.0 - (0.12 / 0.18)**2)  # ≈ 0.745
    canon_kappa = 69.4

    fig, ax = plt.subplots(1, 1, figsize=(7, 4.5))

    # --- Shaded regime regions ---
    # Regular bounded (oblate): broad green band across full width
    ax.axhspan(20, 300, alpha=0.06, color='#2ca02c', zorder=0)

    # Non-lifting (prolate): orange band in the prolate κ range
    ax.axhspan(500, 800, alpha=0.10, color='#ff7f0e', zorder=0)

    # Singular: red band at top (κ > 10^3, near ε = 0)
    ax.fill_between([0, 0.08], 2e3, 2e5, alpha=0.10, color='#d62728',
                    zorder=0)

    # --- Data ---
    # Oblate branch
    ax.semilogy(eps_oblate, kappa_oblate, 'o-', color='#1f77b4',
                markersize=3, linewidth=1.8, label='Oblate Ritz', zorder=3)

    # Prolate branch
    ax.semilogy(eps_prolate, kappa_prolate, 's-', color='#ff7f0e',
                markersize=3.5, linewidth=1.8, label='Prolate Ritz', zorder=3)

    # Canonical operating point
    ax.plot(canon_eps, canon_kappa, marker='*', color='#2ca02c',
            markersize=14, markeredgecolor='black', markeredgewidth=0.8,
            zorder=5, label=r'Canonical oblate ($\kappa = 69.4$)')

    # --- Reference lines ---
    kappa_floor = 269
    ax.axhline(y=kappa_floor, color='grey', linestyle='--', linewidth=0.8,
               alpha=0.6, zorder=1)
    ax.annotate(r'$\kappa_{\mathrm{floor}} \approx 269$',
                xy=(0.15, kappa_floor), xytext=(0.15, 450),
                fontsize=8, color='grey', ha='center',
                arrowprops=dict(arrowstyle='->', color='grey', lw=0.8),
                zorder=4)

    # --- Regime annotations ---
    ax.text(0.04, 1.5e4, 'Singular\n(equiv. sphere,\n'
            r'$\kappa > 10^{10}$)',
            fontsize=7.5, color='#d62728', ha='center', style='italic',
            zorder=4)

    ax.text(0.82, 35, 'Regular bounded\n(oblate)',
            fontsize=8, color='#2ca02c', ha='center', style='italic',
            zorder=4)

    ax.text(0.70, 900, 'Non-lifting (prolate)',
            fontsize=8, color='#e67300', ha='center', style='italic',
            zorder=4)

    # Improvement arrow — entirely below both curves in clear space
    ax.annotate('', xy=(0.60, 55), xytext=(0.15, 55),
                arrowprops=dict(arrowstyle='->', color='#1f77b4',
                                lw=1.5))
    ax.text(0.37, 43, r'Eccentricity improves $\kappa$',
            fontsize=7.5, color='#1f77b4', ha='center', style='italic')

    ax.set_xlabel(r'Eccentricity $\varepsilon = \sqrt{1 - c^2/a^2}$',
                  fontsize=10)
    ax.set_ylabel(r'Condition number $\kappa(\mathbf{J}_s)$', fontsize=10)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(20, 2e5)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax.tick_params(labelsize=9)

    ax.grid(True, which='major', alpha=0.3, linewidth=0.5)
    ax.grid(True, which='minor', alpha=0.15, linewidth=0.3)

    fig.tight_layout()

    for ext in ('pdf', 'png'):
        path = os.path.join(output_dir, f'fig_summary_identifiability.{ext}')
        fig.savefig(path, dpi=300, bbox_inches='tight')
        print(f"Saved: {path}")

    plt.close(fig)


if __name__ == '__main__':
    output_dir = os.path.join(
        os.path.dirname(__file__), '..', 'papers', 'paper8-kac', 'figures'
    )
    os.makedirs(output_dir, exist_ok=True)
    make_summary_figure(output_dir)
    print("Done.")
