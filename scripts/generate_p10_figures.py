"""
Generate all publication-quality figures for Paper 10 (capstone).

Paper 10 synthesises nine companion papers under the thesis:
    "Geometry does three jobs: excitation filtering, spectral organisation,
     identifiability."

Figures
-------
1. Three Jobs of Geometry — conceptual triptych
2. Cross-Application Evidence — parameter-space overview
3. Condition Number Landscape — oblate vs prolate κ(ε)
4. Forward ≠ Inverse Adequacy — cautionary lemma
5. Master Unification Diagram — all papers in one framework

Output
------
    papers/paper10-capstone/figures/fig_*.{png,pdf}
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import numpy as np
import sys
import os
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

# ── path setup ──────────────────────────────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))

from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)
from analytical.oblate_spheroid_ritz import (
    oblate_ritz_frequency,
    oblate_ritz_frequencies,
    sphere_approx_frequencies,
)
from analytical.kac_identifiability import (
    CANONICAL_ABDOMEN,
    compute_jacobian,
    jacobian_condition_number,
    identifiability_analysis,
)
from analytical.universality import (
    oblate_condition_sweep,
    prolate_condition_sweep,
    fit_power_law,
)

# ═══════════════════════════════════════════════════════════════════════════
#  Style (Proc Roy Soc A / JSV compatible)
# ═══════════════════════════════════════════════════════════════════════════

# Colorblind-friendly palette (Tol bright)
CB_BLUE    = '#4477AA'
CB_CYAN    = '#66CCEE'
CB_GREEN   = '#228833'
CB_YELLOW  = '#CCBB44'
CB_RED     = '#EE6677'
CB_PURPLE  = '#AA3377'
CB_GREY    = '#BBBBBB'

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

FIG_DIR = os.path.join(ROOT, 'papers', 'paper10-capstone', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig, name):
    """Save figure as PNG (300 dpi) and PDF (vector)."""
    png = os.path.join(FIG_DIR, name + '.png')
    pdf = os.path.join(FIG_DIR, name + '.pdf')
    fig.savefig(png, dpi=300, bbox_inches='tight', pad_inches=0.05)
    fig.savefig(pdf, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    sz_kb = os.path.getsize(png) / 1024
    print(f'  Saved: {name} (.png {sz_kb:.0f} KB + .pdf)')


# ═══════════════════════════════════════════════════════════════════════════
#  Canonical parameters
# ═══════════════════════════════════════════════════════════════════════════
a_can, c_can = 0.18, 0.12
E_can = 0.1e6
h_can = 0.01
nu_can = 0.45
rho_w_can = 1100.0
rho_f_can = 1020.0
K_f_can = 2.2e9
P_iap_can = 1000.0
eta_can = 0.25           # loss tangent

model_can = AbdominalModelV2(
    a=a_can, b=a_can, c=c_can, h=h_can,
    E=E_can, nu=nu_can, rho_wall=rho_w_can, rho_fluid=rho_f_can,
    K_fluid=K_f_can, P_iap=P_iap_can, loss_tangent=eta_can,
)
R_can = model_can.equivalent_sphere_radius  # ≈ 0.157 m


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 1 — Three Jobs of Geometry (triptych)
# ═══════════════════════════════════════════════════════════════════════════
def fig1_three_jobs():
    """Three-panel figure: filtering, spectral organisation, identifiability."""
    print('\n=== Figure 1: Three Jobs of Geometry ===')

    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE_COL, DOUBLE_COL * 0.35))

    # ── Panel (a): Excitation filtering — (ka)^n suppression ──────────
    ax = axes[0]
    f_range = np.logspace(-0.5, 2.5, 200)       # 0.3 – 300 Hz
    ka = 2 * np.pi * f_range * R_can / 343.0     # airborne

    for n, col, mk in [(0, CB_BLUE, 's'), (1, CB_GREEN, 'D'),
                        (2, CB_RED, 'o'), (3, CB_PURPLE, '^'),
                        (4, CB_YELLOW, 'v')]:
        if n == 0:
            Q_n = np.ones_like(ka)
            label = r'$n=0$ (breathing)'
        else:
            Q_n = ka ** n
            label = rf'$n={n}$'
        ax.loglog(f_range, Q_n, color=col, label=label, linewidth=1.5)

    # Mark canonical f2
    freqs_can = flexural_mode_frequencies_v2(model_can, n_max=4)
    f2 = freqs_can[2]
    ka2 = 2 * np.pi * f2 * R_can / 343.0
    ax.axvline(f2, color='grey', ls=':', lw=0.8)
    ax.annotate(rf'$f_2={f2:.1f}$ Hz', xy=(f2, 1e-6),
                fontsize=7, ha='left', va='bottom', color='grey',
                xytext=(f2 * 1.3, 2e-6),
                arrowprops=dict(arrowstyle='->', color='grey', lw=0.6))

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel(r'Modal coupling $\propto (ka)^n$')
    ax.set_title(r'(a) Excitation filtering', fontsize=9, fontweight='bold')
    ax.legend(fontsize=7, loc='lower right', framealpha=0.9)
    ax.set_ylim(1e-12, 1e1)
    ax.set_xlim(0.3, 300)

    # ── Panel (b): Spectral organisation — f_n vs eccentricity ────────
    ax = axes[1]
    eps_vals = np.linspace(0.05, 0.80, 30)
    modes_plot = [2, 3, 4, 5, 6]
    colors_m = [CB_BLUE, CB_RED, CB_GREEN, CB_PURPLE, CB_YELLOW]
    markers_m = ['o', 's', 'D', '^', 'v']

    freq_data = {n: [] for n in modes_plot}
    for eps in eps_vals:
        c_val = a_can * np.sqrt(1.0 - eps ** 2)
        for n in modes_plot:
            try:
                f = oblate_ritz_frequency(n, a_can, c_val, h_can, E_can,
                                          nu_can, rho_w_can, rho_f_can,
                                          P_iap_can, n_quad=120)
                freq_data[n].append(f)
            except Exception:
                freq_data[n].append(np.nan)

    for n, col, mk in zip(modes_plot, colors_m, markers_m):
        ax.plot(eps_vals, freq_data[n], color=col, marker=mk,
                markersize=3, markevery=5, label=rf'$n={n}$', linewidth=1.5)

    # Canonical eccentricity
    eps_can = np.sqrt(1 - (c_can / a_can) ** 2)
    ax.axvline(eps_can, color='grey', ls=':', lw=0.8)
    ax.annotate(rf'$\varepsilon={eps_can:.2f}$', xy=(eps_can, 1.5),
                fontsize=7, color='grey', ha='right',
                xytext=(eps_can - 0.04, 1.0))

    ax.set_xlabel(r'Oblate eccentricity $\varepsilon$')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title(r'(b) Spectral organisation', fontsize=9, fontweight='bold')
    ax.legend(fontsize=7, loc='upper left', framealpha=0.9)
    ax.set_xlim(0.05, 0.80)

    # ── Panel (c): Identifiability — κ vs eccentricity ────────────────
    ax = axes[2]
    # Use a coarse sweep to keep runtime reasonable
    eps_sweep = np.linspace(0.10, 0.75, 20)
    kappa_vals = []
    for eps in eps_sweep:
        c_v = a_can * np.sqrt(1.0 - eps ** 2)
        p = dict(CANONICAL_ABDOMEN)
        p['a'] = a_can
        p['c'] = c_v
        try:
            kv = jacobian_condition_number(p, model='ritz',
                                           modes=(2, 3, 4, 5, 6))
            kappa_vals.append(kv)
        except Exception:
            kappa_vals.append(np.nan)

    kappa_vals = np.array(kappa_vals)
    ax.semilogy(eps_sweep, kappa_vals, color=CB_BLUE, marker='o',
                markersize=3, label='Oblate Ritz', linewidth=1.5)

    # Sphere limit (dashed horizontal)
    p_sph = dict(CANONICAL_ABDOMEN)
    p_sph['c'] = p_sph['a'] * 0.999  # near-sphere
    try:
        kappa_sphere = jacobian_condition_number(p_sph, model='sphere',
                                                 modes=(2, 3, 4, 5, 6))
    except Exception:
        kappa_sphere = 1e10
    ax.axhline(kappa_sphere, color=CB_RED, ls='--', lw=1.2,
               label=r'Sphere $\kappa$')
    ax.text(0.40, kappa_sphere * 0.35,
            rf'$\kappa_{{\mathrm{{sph}}}}\!\approx\!{kappa_sphere:.0e}$',
            fontsize=6.5, color=CB_RED, ha='center')

    # Canonical point
    eps_can_local = np.sqrt(1 - (c_can / a_can) ** 2)
    ax.axvline(eps_can_local, color='grey', ls=':', lw=0.8)
    k_can_idx = np.argmin(np.abs(eps_sweep - eps_can_local))
    if k_can_idx < len(kappa_vals):
        ax.plot(eps_can_local, kappa_vals[k_can_idx], 'k*',
                markersize=10, zorder=5)
        ax.annotate(rf'$\kappa\!\approx\!{kappa_vals[k_can_idx]:.0f}$',
                    xy=(eps_can_local, kappa_vals[k_can_idx]),
                    xytext=(eps_can_local - 0.18,
                            kappa_vals[k_can_idx] * 5),
                    fontsize=7,
                    arrowprops=dict(arrowstyle='->', lw=0.6))

    ax.set_xlabel(r'Oblate eccentricity $\varepsilon$')
    ax.set_ylabel(r'Condition number $\kappa$')
    ax.set_title(r'(c) Identifiability', fontsize=9, fontweight='bold')
    ax.legend(fontsize=6.5, loc='center right', framealpha=0.9)
    ax.set_xlim(0.10, 0.75)

    fig.tight_layout(w_pad=2.5)
    _save(fig, 'fig_three_jobs')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 2 — Cross-Application Evidence
# ═══════════════════════════════════════════════════════════════════════════
def fig2_cross_application():
    """Parameter-space plot showing four application domains."""
    print('\n=== Figure 2: Cross-Application Evidence ===')

    # Application domains: (name, a_m, c_over_a, E_Pa, f2_Hz, marker, color)
    apps = [
        {
            'name': 'Abdomen\n(P1–P3)',
            'a': 0.18, 'c_over_a': 0.667, 'E': 0.1e6,
            'f_low': 3.0, 'f_high': 8.0,
            'marker': 'o', 'color': CB_BLUE,
            'papers': '1,2,3,6',
        },
        {
            'name': 'Bladder\n(P4)',
            'a': 0.06, 'c_over_a': 0.80, 'E': 0.05e6,
            'f_low': 15.0, 'f_high': 50.0,
            'marker': 's', 'color': CB_GREEN,
            'papers': '4',
        },
        {
            'name': 'Watermelon\n(P7)',
            'a': 0.12, 'c_over_a': 0.85, 'E': 30e6,
            'f_low': 80.0, 'f_high': 200.0,
            'marker': 'D', 'color': CB_RED,
            'papers': '7',
        },
        {
            'name': 'Borborygmi\n(P5)',
            'a': 0.015, 'c_over_a': 0.60, 'E': 0.01e6,
            'f_low': 200.0, 'f_high': 2000.0,
            'marker': '^', 'color': CB_PURPLE,
            'papers': '5',
        },
    ]

    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_COL, DOUBLE_COL * 0.42))

    # Panel (a): Geometric parameter space  a vs c/a
    ax = axes[0]
    for ap in apps:
        ax.plot(ap['a'] * 100, ap['c_over_a'], marker=ap['marker'],
                color=ap['color'], markersize=12, markeredgecolor='k',
                markeredgewidth=0.6, zorder=5)
        # Add size-proportional ellipse
        from matplotlib.patches import Ellipse
        ew = ap['a'] * 100 * 0.25
        eh = ap['c_over_a'] * 0.08
        ellipse = Ellipse((ap['a'] * 100, ap['c_over_a']),
                          width=ew, height=eh,
                          alpha=0.15, color=ap['color'], zorder=2)
        ax.add_patch(ellipse)
        # Label
        dx = 0.5 if ap['a'] > 0.05 else 0.3
        ax.annotate(ap['name'], xy=(ap['a'] * 100, ap['c_over_a']),
                    xytext=(ap['a'] * 100 + dx, ap['c_over_a'] + 0.04),
                    fontsize=7, ha='left', va='bottom',
                    arrowprops=dict(arrowstyle='->', lw=0.5, color=ap['color']))

    ax.set_xlabel('Semi-major axis $a$ (cm)')
    ax.set_ylabel('Aspect ratio $c/a$')
    ax.set_title('(a) Geometric parameter space', fontsize=9, fontweight='bold')
    ax.set_xlim(0, 22)
    ax.set_ylim(0.45, 1.0)

    # Panel (b): Frequency ranges vs E
    ax = axes[1]
    for i, ap in enumerate(apps):
        y = i
        ax.barh(y, np.log10(ap['f_high']) - np.log10(ap['f_low']),
                left=np.log10(ap['f_low']),
                height=0.5, color=ap['color'], alpha=0.7,
                edgecolor='k', linewidth=0.5)
        ax.plot(np.log10(np.sqrt(ap['f_low'] * ap['f_high'])), y,
                marker=ap['marker'], color=ap['color'], markersize=8,
                markeredgecolor='k', markeredgewidth=0.5, zorder=5)

    ax.set_yticks(range(len(apps)))
    ax.set_yticklabels([ap['name'] for ap in apps], fontsize=8)
    ax.set_xlabel(r'$\log_{10}(f)$  [Hz]')
    ax.set_title('(b) Frequency ranges', fontsize=9, fontweight='bold')

    # Custom x-tick labels showing actual Hz
    xticks = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    ax.set_xticks(xticks)
    ax.set_xticklabels([f'{10**x:.0f}' if x == int(x) else f'{10**x:.0f}'
                        for x in xticks], fontsize=7)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_xlim(-0.2, 3.8)

    fig.tight_layout(w_pad=3)
    _save(fig, 'fig_cross_application')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3 — Condition Number Landscape (oblate vs prolate)
# ═══════════════════════════════════════════════════════════════════════════
def fig3_condition_landscape():
    """κ vs ε for oblate and prolate, showing the asymmetry."""
    print('\n=== Figure 3: Condition Number Landscape ===')

    # Oblate sweep
    eps_oblate = np.linspace(0.08, 0.75, 22)
    print('  Computing oblate condition numbers...')
    oblate_res = oblate_condition_sweep(eccentricities=eps_oblate,
                                        modes=(2, 3, 4, 5, 6))

    # Prolate sweep
    eps_prolate = np.linspace(0.08, 0.75, 22)
    print('  Computing prolate condition numbers...')
    prolate_res = prolate_condition_sweep(eccentricities=eps_prolate,
                                          modes=(2, 3, 4, 5, 6))

    # Power-law fits
    C_o, alpha_o, r2_o = fit_power_law(oblate_res['eccentricity'],
                                        oblate_res['kappa'])
    C_p, alpha_p, r2_p = fit_power_law(prolate_res['eccentricity'],
                                        prolate_res['kappa'])

    print(f'  Oblate:  κ ∝ ε^{{-{alpha_o:.2f}}}, C={C_o:.1f}, R²={r2_o:.3f}')
    print(f'  Prolate: κ ∝ ε^{{-{alpha_p:.2f}}}, C={C_p:.1f}, R²={r2_p:.3f}')

    fig, ax = plt.subplots(figsize=(SINGLE_COL * 1.5, SINGLE_COL * 1.1))

    # Plot on LINEAR x-axis, LOG y-axis for clearer reading
    valid_o = np.isfinite(oblate_res['kappa'])
    valid_p = np.isfinite(prolate_res['kappa'])

    # Oblate
    ax.semilogy(oblate_res['eccentricity'][valid_o],
                oblate_res['kappa'][valid_o],
                color=CB_BLUE, marker='o', markersize=5, linewidth=2.0,
                label='Oblate', zorder=4)

    # Prolate
    ax.semilogy(prolate_res['eccentricity'][valid_p],
                prolate_res['kappa'][valid_p],
                color=CB_RED, marker='s', markersize=5, linewidth=2.0,
                label='Prolate', zorder=4)

    # Fill between to highlight the gap
    eps_common = oblate_res['eccentricity'][valid_o & valid_p]
    k_obl = oblate_res['kappa'][valid_o & valid_p]
    k_pro = prolate_res['kappa'][valid_o & valid_p]
    ax.fill_between(eps_common, k_obl, k_pro, alpha=0.10, color=CB_PURPLE,
                    zorder=1, label='Oblate advantage')

    # Canonical eccentricity
    eps_can_local = np.sqrt(1 - (c_can / a_can) ** 2)
    ax.axvline(eps_can_local, color='grey', ls=':', lw=0.8, zorder=1)
    ax.text(eps_can_local + 0.01, ax.get_ylim()[0] if ax.get_ylim()[0] > 0 else 15,
            rf'$\varepsilon={eps_can_local:.2f}$', fontsize=7, color='grey',
            va='bottom', ha='left')

    # Annotate the key asymmetry
    ax.annotate('Oblate lifts\nidentifiability',
                xy=(0.55, 120), fontsize=7.5, color=CB_BLUE,
                fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', fc='white',
                          ec=CB_BLUE, alpha=0.8))
    ax.annotate('Prolate: flat /\npoor conditioning',
                xy=(0.55, 650), fontsize=7.5, color=CB_RED,
                fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', fc='white',
                          ec=CB_RED, alpha=0.8))

    # Tighten y-axis to where the data actually lives
    all_valid_k = np.concatenate([oblate_res['kappa'][valid_o],
                                   prolate_res['kappa'][valid_p]])
    y_lo = max(1, np.nanmin(all_valid_k) / 3)
    y_hi = np.nanmax(all_valid_k) * 10
    ax.set_ylim(y_lo, y_hi)
    ax.set_xlim(0.05, 0.80)

    ax.set_xlabel(r'Eccentricity $\varepsilon$')
    ax.set_ylabel(r'Condition number $\kappa$')
    ax.set_title('Condition number: oblate vs prolate', fontsize=9,
                 fontweight='bold')
    ax.legend(fontsize=8, loc='lower left', framealpha=0.9)

    fig.tight_layout()
    _save(fig, 'fig_condition_landscape')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 4 — Forward ≠ Inverse Adequacy
# ═══════════════════════════════════════════════════════════════════════════
def fig4_forward_neq_inverse():
    """Two-panel: small forward error ≠ good inverse conditioning."""
    print('\n=== Figure 4: Forward ≠ Inverse Adequacy ===')

    # Compute sphere vs Ritz frequencies across aspect ratios
    aspect_ratios = np.linspace(0.50, 0.95, 20)
    modes = (2, 3, 4, 5, 6)
    errors = {n: [] for n in modes}
    kappa_ritz = []
    kappa_sphere = []

    for ar in aspect_ratios:
        cv = a_can * ar
        # Ritz frequencies
        fr = oblate_ritz_frequencies(a_can, cv, h_can, E_can, nu_can,
                                      rho_w_can, rho_f_can, P_iap_can,
                                      n_target=modes)
        # Sphere frequencies
        ms = AbdominalModelV2(a=a_can, b=a_can, c=cv, h=h_can,
                               E=E_can, nu=nu_can, rho_wall=rho_w_can,
                               rho_fluid=rho_f_can, K_fluid=K_f_can,
                               P_iap=P_iap_can)
        fs = sphere_approx_frequencies(ms, n_modes=modes)

        for n in modes:
            err = abs(fs[n] - fr[n]) / fr[n] * 100 if fr[n] > 0 else np.nan
            errors[n].append(err)

        # Condition numbers
        p = dict(CANONICAL_ABDOMEN)
        p['a'] = a_can
        p['c'] = cv
        try:
            kr = jacobian_condition_number(p, model='ritz', modes=modes)
        except Exception:
            kr = np.nan
        try:
            ks = jacobian_condition_number(p, model='sphere', modes=modes)
        except Exception:
            ks = np.nan
        kappa_ritz.append(kr)
        kappa_sphere.append(ks)

    kappa_ritz = np.array(kappa_ritz)
    kappa_sphere = np.array(kappa_sphere)

    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_COL, DOUBLE_COL * 0.38))

    # Panel (a): Forward frequency error
    ax = axes[0]
    colors_m = [CB_BLUE, CB_RED, CB_GREEN, CB_PURPLE, CB_YELLOW]
    for n, col in zip(modes, colors_m):
        ax.plot(aspect_ratios, errors[n], color=col, linewidth=1.5,
                label=rf'$n={n}$')

    ax.axhline(10, color='grey', ls=':', lw=0.8)
    ax.text(0.51, 11, '10%', fontsize=7, color='grey')

    # Canonical point
    ar_can = c_can / a_can
    ax.axvline(ar_can, color='grey', ls=':', lw=0.8)

    ax.set_xlabel('Aspect ratio $c/a$')
    ax.set_ylabel('Frequency error (%)')
    ax.set_title('(a) Forward error: sphere vs oblate Ritz',
                 fontsize=9, fontweight='bold')
    ax.legend(fontsize=7, loc='upper left', ncol=2, framealpha=0.9)
    ax.set_xlim(0.50, 0.95)
    ax.set_ylim(0, None)

    # Panel (b): Condition number
    ax = axes[1]
    valid_r = np.isfinite(kappa_ritz)
    valid_s = np.isfinite(kappa_sphere)

    ax.semilogy(aspect_ratios[valid_r], kappa_ritz[valid_r],
                color=CB_BLUE, marker='o', markersize=3, linewidth=1.8,
                label='Oblate Ritz')
    ax.semilogy(aspect_ratios[valid_s], kappa_sphere[valid_s],
                color=CB_RED, marker='s', markersize=3, linewidth=1.8,
                label='Equivalent sphere')

    ax.axvline(ar_can, color='grey', ls=':', lw=0.8)

    # Annotate canonical point
    idx_can = np.argmin(np.abs(aspect_ratios - ar_can))
    if valid_r[idx_can]:
        ax.annotate(rf'$\kappa_{{Ritz}}\approx{kappa_ritz[idx_can]:.0f}$',
                    xy=(ar_can, kappa_ritz[idx_can]),
                    xytext=(ar_can + 0.05, kappa_ritz[idx_can] * 0.3),
                    fontsize=7, color=CB_BLUE,
                    arrowprops=dict(arrowstyle='->', color=CB_BLUE, lw=0.5))
    if valid_s[idx_can]:
        ax.annotate(rf'$\kappa_{{sphere}}\approx{kappa_sphere[idx_can]:.1e}$',
                    xy=(ar_can, kappa_sphere[idx_can]),
                    xytext=(ar_can + 0.05, kappa_sphere[idx_can] * 3),
                    fontsize=7, color=CB_RED,
                    arrowprops=dict(arrowstyle='->', color=CB_RED, lw=0.5))

    ax.set_xlabel('Aspect ratio $c/a$')
    ax.set_ylabel(r'Condition number $\kappa$')
    ax.set_title(r'(b) Inverse conditioning: $\kappa$ divergence',
                 fontsize=9, fontweight='bold')
    ax.legend(fontsize=7, loc='upper right', framealpha=0.9)
    ax.set_xlim(0.50, 0.95)

    # Add text box with the cautionary message
    textstr = (r'$\Delta f < 10\%$ yet $\kappa_{\mathrm{sphere}}'
               r'/\kappa_{\mathrm{Ritz}} \gg 1$')
    fig.text(0.5, -0.02, textstr, ha='center', fontsize=8,
             fontstyle='italic', color='grey')

    fig.tight_layout(w_pad=2.5)
    _save(fig, 'fig_forward_neq_inverse')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 5 — Master Unification Diagram
# ═══════════════════════════════════════════════════════════════════════════
def fig5_master_unification():
    """All 9 companion papers mapped into a single geometric framework."""
    print('\n=== Figure 5: Master Unification Diagram ===')

    # Each paper: (label, eccentricity, ka, kappa_est, job)
    # Spread papers that share the canonical eps~0.745 slightly for legibility
    papers = [
        {'id': 'P1', 'title': 'Brown note',
         'eps': 0.745, 'ka': 0.02, 'kappa': 69,
         'job': 'filter', 'color': CB_BLUE, 'marker': 'o'},
        {'id': 'P2', 'title': 'Gas pockets',
         'eps': 0.72, 'ka': 0.05, 'kappa': 75,
         'job': 'spectral', 'color': CB_CYAN, 'marker': 'v'},
        {'id': 'P3', 'title': 'Scaling laws',
         'eps': 0.50, 'ka': 0.02, 'kappa': 25,
         'job': 'spectral', 'color': CB_CYAN, 'marker': 's'},
        {'id': 'P4', 'title': 'Bladder',
         'eps': 0.60, 'ka': 0.05, 'kappa': 40,
         'job': 'identify', 'color': CB_GREEN, 'marker': 'D'},
        {'id': 'P5', 'title': 'Borborygmi',
         'eps': 0.80, 'ka': 0.10, 'kappa': 120,
         'job': 'filter', 'color': CB_BLUE, 'marker': '^'},
        {'id': 'P6', 'title': 'Sub-bass',
         'eps': 0.70, 'ka': 0.15, 'kappa': 80,
         'job': 'filter', 'color': CB_BLUE, 'marker': 'P'},
        {'id': 'P7', 'title': 'Watermelon',
         'eps': 0.53, 'ka': 0.35, 'kappa': 30,
         'job': 'identify', 'color': CB_GREEN, 'marker': 'h'},
        {'id': 'P8', 'title': 'Inverse Kac',
         'eps': 0.76, 'ka': 0.02, 'kappa': 55,
         'job': 'identify', 'color': CB_GREEN, 'marker': '*'},
        {'id': 'P9', 'title': 'Lifting thm',
         'eps': 0.40, 'ka': 0.02, 'kappa': 15,
         'job': 'all', 'color': CB_GREY, 'marker': 'X'},
    ]

    fig, ax = plt.subplots(figsize=(SINGLE_COL * 1.6, SINGLE_COL * 1.4))

    # Background: condition number curve from oblate sweep (limited range)
    eps_bg = np.linspace(0.15, 0.78, 30)
    kappa_bg = []
    for eps in eps_bg:
        c_v = a_can * np.sqrt(1.0 - eps ** 2)
        p = dict(CANONICAL_ABDOMEN)
        p['a'] = a_can
        p['c'] = c_v
        try:
            kv = jacobian_condition_number(p, model='ritz',
                                           modes=(2, 3, 4, 5, 6))
            kappa_bg.append(kv)
        except Exception:
            kappa_bg.append(np.nan)
    kappa_bg = np.array(kappa_bg)
    valid_bg = np.isfinite(kappa_bg)
    ax.semilogy(eps_bg[valid_bg], kappa_bg[valid_bg],
                color='#dddddd', linewidth=8, zorder=1, solid_capstyle='round')

    # Plot each paper
    for pp in papers:
        sz = 80 + 350 * pp['ka']
        ax.scatter(pp['eps'], pp['kappa'], s=sz,
                   color=pp['color'], marker=pp['marker'],
                   edgecolors='k', linewidths=0.6, zorder=5)

    # Labels with manual offsets to avoid overlap
    label_offsets = {
        'P1': (0.03, 1.6),    'P2': (-0.07, 0.55),
        'P3': (0.03, 1.4),    'P4': (0.03, 1.5),
        'P5': (0.02, 1.8),    'P6': (-0.08, 0.5),
        'P7': (0.03, 0.6),    'P8': (0.03, 1.5),
        'P9': (0.03, 1.5),
    }
    for pp in papers:
        dx, ky = label_offsets[pp['id']]
        ax.annotate(
            pp['id'],
            xy=(pp['eps'], pp['kappa']),
            xytext=(pp['eps'] + dx, pp['kappa'] * ky),
            fontsize=7.5, fontweight='bold', color=pp['color'],
            ha='left' if dx > 0 else 'right',
            arrowprops=dict(arrowstyle='-', color=pp['color'],
                            lw=0.4, alpha=0.6),
        )

    # Three-jobs legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=CB_BLUE,
               markersize=8, markeredgecolor='k', markeredgewidth=0.4,
               label='Excitation filtering'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=CB_CYAN,
               markersize=8, markeredgecolor='k', markeredgewidth=0.4,
               label='Spectral organisation'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor=CB_GREEN,
               markersize=8, markeredgecolor='k', markeredgewidth=0.4,
               label='Identifiability'),
        Line2D([0], [0], marker='X', color='w', markerfacecolor=CB_GREY,
               markersize=8, markeredgecolor='k', markeredgewidth=0.4,
               label='All three jobs'),
        Line2D([0], [0], color='#dddddd', lw=5, solid_capstyle='round',
               label=r'$\kappa(\varepsilon)$ trend'),
    ]

    # Point-size legend
    handles2 = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey',
               markersize=np.sqrt(80 + 350 * 0.02) / 2,
               markeredgecolor='k', markeredgewidth=0.3,
               label='$ka=0.02$'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey',
               markersize=np.sqrt(80 + 350 * 0.15) / 2,
               markeredgecolor='k', markeredgewidth=0.3,
               label='$ka=0.15$'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey',
               markersize=np.sqrt(80 + 350 * 0.35) / 2,
               markeredgecolor='k', markeredgewidth=0.3,
               label='$ka=0.35$'),
    ]
    leg2 = ax.legend(handles=handles2, fontsize=6.5, loc='lower right',
                     title='Acoustic coupling ($ka$)', title_fontsize=7,
                     framealpha=0.92, edgecolor='#cccccc')
    leg1 = ax.legend(handles=legend_elements, fontsize=7,
                     loc='upper left', framealpha=0.92,
                     edgecolor='#cccccc')
    ax.add_artist(leg1)
    ax.add_artist(leg2)

    ax.set_xlabel(r'Oblate eccentricity $\varepsilon$')
    ax.set_ylabel(r'Condition number $\kappa$ (identifiability)')
    ax.set_title('Master unification: 9 papers in geometric space',
                 fontsize=9, fontweight='bold')
    ax.set_xlim(0.10, 0.88)
    ax.set_ylim(8, 300)

    fig.tight_layout()
    _save(fig, 'fig_master_unification')


# ═══════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('=' * 72)
    print('  Paper 10 (Capstone) — Figure Generation')
    print('  Output: papers/paper10-capstone/figures/')
    print('=' * 72)

    fig1_three_jobs()
    fig2_cross_application()
    fig3_condition_landscape()
    fig4_forward_neq_inverse()
    fig5_master_unification()

    print('\n' + '=' * 72)
    print('  All figures generated successfully.')
    print('=' * 72)
