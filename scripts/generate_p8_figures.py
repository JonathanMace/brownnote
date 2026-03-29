"""
Generate all 4 publication-quality figures for Paper 8:
"Can You Hear the Shape of an Organ?" — Kac identifiability analysis.

Output: projects/kac-identifiability/figures/fig_*.{png,pdf}

Usage:
    python scripts/generate_p8_figures.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import warnings

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))

from analytical.kac_identifiability import (
    CANONICAL_ABDOMEN,
    INVERSION_PARAMS,
    DEFAULT_MODES,
    sphere_vs_oblate_comparison,
    compute_jacobian,
    jacobian_condition_number,
    identifiability_analysis,
    invert_frequencies,
    _forward_ritz,
)

# ═══════════════════════════════════════════════════════════════════════════
#  Style setup — JSV-compatible, colorblind-friendly (Tol bright)
# ═══════════════════════════════════════════════════════════════════════════

CB_BLUE   = '#4477AA'
CB_CYAN   = '#66CCEE'
CB_GREEN  = '#228833'
CB_YELLOW = '#CCBB44'
CB_RED    = '#EE6677'
CB_PURPLE = '#AA3377'
CB_GREY   = '#BBBBBB'

JSV_RC = {
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.grid': True,
    'grid.color': '#cccccc',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
}
plt.rcParams.update(JSV_RC)

SINGLE_COL = 84 / 25.4    # 3.31 inches
DOUBLE_COL = 174 / 25.4   # 6.85 inches

FIG_DIR = os.path.join(ROOT, 'projects', 'kac-identifiability', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig, name):
    """Save figure as PNG (300 dpi) and PDF (vector)."""
    png = os.path.join(FIG_DIR, name + '.png')
    pdf = os.path.join(FIG_DIR, name + '.pdf')
    fig.savefig(png, dpi=300, bbox_inches='tight', pad_inches=0.05)
    fig.savefig(pdf, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    print(f'  Saved: {name} (.png + .pdf)')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 1: Sphere vs Oblate Comparison (headline result)
# ═══════════════════════════════════════════════════════════════════════════

def fig_sphere_vs_oblate():
    """Log-scale bar chart comparing condition numbers of the two models."""
    print('\n=== Figure 1: Sphere vs Oblate Comparison ===')

    result = sphere_vs_oblate_comparison()
    kappa_s = result['sphere_condition']
    kappa_o = result['oblate_condition']

    print(f'  Sphere κ = {kappa_s:.3e}')
    print(f'  Oblate κ = {kappa_o:.1f}')
    print(f'  Improvement: {result["improvement_factor"]:.0f}×')

    fig, ax = plt.subplots(figsize=(SINGLE_COL, SINGLE_COL * 0.85))

    bars = ax.bar(
        ['Equivalent\nsphere', 'Oblate\nspheroid'],
        [kappa_s, kappa_o],
        color=[CB_RED, CB_BLUE],
        width=0.5,
        edgecolor='black',
        linewidth=0.6,
        zorder=3,
    )

    ax.set_yscale('log')
    ax.set_ylabel(r'Condition number $\kappa(\mathbf{J}_s)$')

    # Well-conditioned threshold line at κ=100
    ax.axhline(100, color=CB_GREEN, linestyle='--', linewidth=1.2,
               label=r'Well-conditioned threshold ($\kappa = 100$)', zorder=2)

    # Annotate bars
    for bar, val in zip(bars, [kappa_s, kappa_o]):
        if val > 1e6:
            label = f'κ ≈ {val:.1e}'
        else:
            label = f'κ ≈ {val:.0f}'
        ax.text(bar.get_x() + bar.get_width() / 2, val * 2.5,
                label, ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_ylim(1, kappa_s * 50)
    ax.legend(loc='upper right', framealpha=0.9, fontsize=7)
    ax.grid(axis='y', alpha=0.3)
    ax.grid(axis='x', visible=False)

    _save(fig, 'fig_sphere_vs_oblate')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 2: Condition Number Map over (a, ζ) space
# ═══════════════════════════════════════════════════════════════════════════

def fig_condition_map():
    """2D heatmap of condition number over (a, ζ=c/a) at fixed E."""
    print('\n=== Figure 2: Condition Number Map ===')

    a_vals = np.linspace(0.10, 0.25, 20)
    zeta_vals = np.linspace(0.3, 1.0, 20)

    kappa_grid = np.full((len(a_vals), len(zeta_vals)), np.nan)
    base = dict(CANONICAL_ABDOMEN)

    total = len(a_vals) * len(zeta_vals)
    count = 0
    for i, a in enumerate(a_vals):
        for j, zeta in enumerate(zeta_vals):
            c = zeta * a
            p = dict(base)
            p['a'] = a
            p['c'] = c
            p['E'] = 0.1e6  # fixed at 0.1 MPa
            try:
                kappa_grid[i, j] = jacobian_condition_number(p, model='ritz')
            except Exception:
                kappa_grid[i, j] = np.inf
            count += 1
            if count % 50 == 0:
                print(f'  ... {count}/{total} grid points', flush=True)

    # Replace inf/nan with large value for plotting
    kappa_plot = np.where(np.isfinite(kappa_grid), kappa_grid, np.nanmax(kappa_grid[np.isfinite(kappa_grid)]) * 10)

    fig, ax = plt.subplots(figsize=(SINGLE_COL * 1.3, SINGLE_COL))

    im = ax.pcolormesh(
        a_vals, zeta_vals, np.log10(kappa_plot.T),
        cmap='viridis', shading='auto', rasterized=True,
    )

    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label(r'$\log_{10}\,\kappa(\mathbf{J}_s)$', fontsize=9)

    # Mark canonical abdomen: a=0.18, ζ=0.12/0.18=0.667
    ax.plot(0.18, 0.12 / 0.18, 'o', color='white', markersize=7,
            markeredgecolor='black', markeredgewidth=1.0, zorder=5)
    ax.annotate('Abdomen', xy=(0.18, 0.12 / 0.18), xytext=(0.20, 0.55),
                fontsize=7, color='white', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='white', lw=1.0),
                zorder=5)

    # Mark watermelon: a≈0.158, ζ≈0.78
    ax.plot(0.158, 0.78, 's', color='white', markersize=7,
            markeredgecolor='black', markeredgewidth=1.0, zorder=5)
    ax.annotate('Watermelon', xy=(0.158, 0.78), xytext=(0.115, 0.88),
                fontsize=7, color='white', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='white', lw=1.0),
                zorder=5)

    # Contour at κ=100 threshold
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        cs = ax.contour(a_vals, zeta_vals, np.log10(kappa_plot.T),
                        levels=[2.0], colors=['white'], linewidths=1.0,
                        linestyles='--')
        ax.clabel(cs, fmt=r'$\kappa=100$', fontsize=6, colors='white')

    ax.set_xlabel(r'Semi-major axis $a$ (m)')
    ax.set_ylabel(r'Aspect ratio $\zeta = c/a$')

    _save(fig, 'fig_condition_map')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3: Inversion Noise Sensitivity (Monte Carlo)
# ═══════════════════════════════════════════════════════════════════════════

def fig_inversion_noise():
    """Box plots of inversion error vs measurement noise level."""
    print('\n=== Figure 3: Inversion Noise Sensitivity ===')

    params = dict(CANONICAL_ABDOMEN)
    noise_levels = [0.005, 0.01, 0.02, 0.05, 0.10]
    n_trials = 1000

    # Compute true frequencies
    f_true = _forward_ritz(params, DEFAULT_MODES)
    print(f'  True frequencies: {f_true}')

    # Storage: for each noise level, relative errors in (a, c, E)
    errors = {k: {nl: [] for nl in noise_levels} for k in INVERSION_PARAMS}

    rng = np.random.default_rng(42)

    for nl in noise_levels:
        print(f'  Noise level {nl*100:.1f}%: running {n_trials} trials...', end='', flush=True)
        converged = 0
        for trial in range(n_trials):
            # Add Gaussian noise to frequencies
            f_noisy = f_true * (1.0 + nl * rng.standard_normal(len(f_true)))

            # Initial guess: perturb true params by ±10%
            guess = dict(params)
            for k in INVERSION_PARAMS:
                guess[k] = params[k] * (1.0 + 0.10 * rng.standard_normal())

            try:
                result = invert_frequencies(f_noisy, guess, model='ritz')
                if result['success']:
                    converged += 1
                    for k in INVERSION_PARAMS:
                        rel_err = (result['params'][k] - params[k]) / params[k]
                        errors[k][nl].append(rel_err * 100)  # percentage
            except Exception:
                pass

        print(f' {converged}/{n_trials} converged')

    # Box plot: one subplot per parameter
    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE_COL, SINGLE_COL * 0.9),
                             sharey=False)

    param_labels = {'a': r'$a$ (semi-major)', 'c': r'$c$ (semi-minor)',
                    'E': r'$E$ (modulus)'}
    param_colors = {'a': CB_BLUE, 'c': CB_GREEN, 'E': CB_RED}
    noise_labels = [f'{nl*100:.1f}%' for nl in noise_levels]

    for ax, k in zip(axes, INVERSION_PARAMS):
        data = [errors[k][nl] for nl in noise_levels]

        bp = ax.boxplot(
            data, positions=range(len(noise_levels)),
            widths=0.6, patch_artist=True,
            boxprops=dict(facecolor=param_colors[k], alpha=0.4,
                          edgecolor='black', linewidth=0.6),
            medianprops=dict(color='black', linewidth=1.2),
            whiskerprops=dict(linewidth=0.6),
            capprops=dict(linewidth=0.6),
            flierprops=dict(marker='.', markersize=2, alpha=0.3),
            showfliers=True,
        )

        ax.set_xticks(range(len(noise_levels)))
        ax.set_xticklabels(noise_labels, fontsize=7)
        ax.set_xlabel('Noise level')
        ax.set_title(param_labels[k], fontsize=9)
        ax.axhline(0, color='gray', linestyle='-', linewidth=0.5, zorder=0)
        ax.grid(axis='y', alpha=0.3)
        ax.grid(axis='x', visible=False)

    axes[0].set_ylabel('Relative error (%)')
    fig.subplots_adjust(wspace=0.35)

    _save(fig, 'fig_inversion_noise')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 4: Singular Value Spectrum
# ═══════════════════════════════════════════════════════════════════════════

def fig_singular_values():
    """Bar chart comparing singular values of sphere vs oblate Jacobians."""
    print('\n=== Figure 4: Singular Value Spectrum ===')

    params = dict(CANONICAL_ABDOMEN)

    sphere_res = identifiability_analysis(params, model='sphere')
    oblate_res = identifiability_analysis(params, model='ritz')

    sv_sphere = sphere_res['singular_values']
    sv_oblate = oblate_res['singular_values']

    print(f'  Sphere SVs: {sv_sphere}')
    print(f'  Oblate SVs: {sv_oblate}')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE_COL * 0.75, SINGLE_COL * 0.85),
                                    sharey=True)

    mode_labels = [f'$\\sigma_{i+1}$' for i in range(len(sv_sphere))]
    x = np.arange(len(sv_sphere))

    # Sphere
    ax1.bar(x, sv_sphere, color=CB_RED, edgecolor='black', linewidth=0.6,
            width=0.6, zorder=3)
    ax1.set_xticks(x)
    ax1.set_xticklabels(mode_labels)
    ax1.set_title('Equivalent sphere', fontsize=9)
    ax1.set_ylabel('Singular value')
    ax1.set_yscale('log')
    ax1.grid(axis='y', alpha=0.3)
    ax1.grid(axis='x', visible=False)

    # Annotate near-zero SV
    min_sv = sv_sphere.min()
    min_idx = np.argmin(sv_sphere)
    ax1.annotate(f'{min_sv:.1e}', xy=(min_idx, min_sv),
                 xytext=(min_idx + 0.3, min_sv * 10),
                 fontsize=7, color=CB_RED,
                 arrowprops=dict(arrowstyle='->', color=CB_RED, lw=0.8))

    # Oblate
    ax2.bar(x, sv_oblate, color=CB_BLUE, edgecolor='black', linewidth=0.6,
            width=0.6, zorder=3)
    ax2.set_xticks(x)
    ax2.set_xticklabels(mode_labels)
    ax2.set_title('Oblate spheroid', fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    ax2.grid(axis='x', visible=False)

    fig.subplots_adjust(wspace=0.08)

    _save(fig, 'fig_singular_values')


# ═══════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('=' * 60)
    print('Paper 8: Kac Identifiability — Figure Generation')
    print('=' * 60)

    fig_sphere_vs_oblate()
    fig_condition_map()
    fig_inversion_noise()
    fig_singular_values()

    print('\n' + '=' * 60)
    print('All 4 figures saved to:')
    print(f'  {FIG_DIR}')
    print('=' * 60)
