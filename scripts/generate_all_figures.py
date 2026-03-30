"""
Generate all 12 publication-ready figures for the JSV paper (v4).

Camera-ready figures following JSV style guidelines:
- Single column: 84 mm (3.31 in), Double column: 174 mm (6.85 in)
- Font: 8–10 pt serif
- DPI: 300 (PNG + vector PDF)
- Greyscale-safe: hatching/markers supplement colour
- Output: data/figures/fig_*.{png,pdf}
"""

import sys
import os
import warnings

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize

from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2, breathing_mode_v2,
    flexural_mode_pressure_response,
)
from src.analytical.mechanical_coupling import (
    WBVExposure, ISO_2631_TRANSMISSIBILITY,
    interpolate_transmissibility, mechanical_excitation_response,
    compare_airborne_vs_mechanical,
)
from src.analytical.energy_budget import (
    radiation_damping_flexural, absorption_cross_section,
    self_consistent_displacement,
)
from src.analytical.dimensional_analysis import (
    dimensionless_frequency, phi_analytical,
    parametric_sweep_dimensionless, animal_scaling, ANIMAL_MODELS,
)
from src.analytical.nonlinear_analysis import (
    NonlinearShellModel, linear_modal_properties,
    cubic_stiffness_coefficient, backbone_freq_hz,
    duffing_frequency_response, wbv_modal_force, jump_amplitude,
)
from src.analytical.uncertainty_quantification import (
    N_MC, N_SOBOL, PARAM_NAMES, PARAM_DEFS,
    sample_parameters, evaluate_batch, summarise, run_sobol,
)

# ── Output directory ──
FIG_DIR = os.path.join(ROOT, 'papers', 'paper1-brown-note', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# ── JSV publication style ──
COLORS = plt.cm.tab10.colors
C_BLUE, C_ORANGE, C_GREEN, C_RED, C_PURPLE = COLORS[:5]
C_BROWN, C_PINK, C_GRAY, C_OLIVE, C_CYAN = COLORS[5:10]

JSV_RC = {
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 9,
    'axes.labelsize': 9,
    'axes.titlesize': 9,
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
    'lines.linewidth': 1.2,
    'lines.markersize': 4,
    'axes.prop_cycle': plt.cycler('color', list(COLORS)),
}
plt.rcParams.update(JSV_RC)

SINGLE_COL = 84 / 25.4   # 3.31 inches
DOUBLE_COL = 174 / 25.4   # 6.85 inches

# Hatching patterns for greyscale readability
HATCHES = ['///', '\\\\\\', '...', 'xxx', '+++', 'ooo']


def _save(fig, name):
    """Save figure as PNG (300 dpi) and PDF (vector)."""
    png = os.path.join(FIG_DIR, f'{name}.png')
    pdf = os.path.join(FIG_DIR, f'{name}.pdf')
    fig.savefig(png, dpi=300)
    fig.savefig(pdf)
    plt.close(fig)
    print(f"  ✓ {name}.png + .pdf")


# ═══════════════════════════════════════════════════════════════════════
# 1. GEOMETRY SCHEMATIC
# ═══════════════════════════════════════════════════════════════════════
def fig_geometry_schematic():
    """Oblate spheroid geometry with axes (a, c, h) and coordinate system."""
    fig, ax = plt.subplots(figsize=(DOUBLE_COL, 3.2))
    ax.set_aspect('equal')
    ax.set_xlim(-4.5, 5.5)
    ax.set_ylim(-2.8, 3.0)
    ax.axis('off')

    cx, cy = 0.5, 0.0
    a_draw, c_draw = 2.2, 1.5

    # Outer shell
    shell = Ellipse((cx, cy), 2 * a_draw, 2 * c_draw,
                    facecolor='#e8d4c0', edgecolor='k', linewidth=1.2, zorder=2)
    ax.add_patch(shell)

    # Inner cavity (fluid-filled)
    h_draw = 0.18
    inner = Ellipse((cx, cy), 2 * (a_draw - h_draw), 2 * (c_draw - h_draw),
                    facecolor='#c5ddf0', edgecolor='k', linewidth=0.6,
                    linestyle='--', zorder=3)
    ax.add_patch(inner)

    # Coordinate axes
    ax.annotate('', xy=(cx + 2.8, cy), xytext=(cx, cy),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.8))
    ax.annotate('', xy=(cx, cy + 2.1), xytext=(cx, cy),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.8))
    ax.text(cx + 2.9, cy - 0.1, r'$r$', fontsize=10, ha='left')
    ax.text(cx + 0.1, cy + 2.15, r'$z$', fontsize=10, ha='left')

    # Dimension labels — a (horizontal)
    y_dim_a = -1.85
    ax.annotate('', xy=(cx + a_draw, y_dim_a), xytext=(cx, y_dim_a),
                arrowprops=dict(arrowstyle='<->', color=C_RED, lw=0.8))
    ax.text(cx + a_draw / 2, y_dim_a - 0.2, r'$a$', fontsize=10,
            ha='center', color=C_RED, fontweight='bold')

    # Dimension labels — c (vertical)
    x_dim_c = cx + a_draw + 0.3
    ax.annotate('', xy=(x_dim_c, cy + c_draw), xytext=(x_dim_c, cy),
                arrowprops=dict(arrowstyle='<->', color=C_BLUE, lw=0.8))
    ax.text(x_dim_c + 0.15, cy + c_draw / 2, r'$c$', fontsize=10,
            va='center', color=C_BLUE, fontweight='bold')

    # Wall thickness — h
    theta = np.radians(40)
    x_out = cx + a_draw * np.cos(theta)
    y_out = cy + c_draw * np.sin(theta)
    x_in = cx + (a_draw - h_draw) * np.cos(theta)
    y_in = cy + (c_draw - h_draw) * np.sin(theta)
    ax.annotate(r'$h$',
                xy=((x_out + x_in) / 2, (y_out + y_in) / 2),
                xytext=(x_out + 0.5, y_out + 0.4), fontsize=10,
                color=C_GREEN, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=0.7))

    # Region labels
    ax.text(cx, cy, 'Visceral\nfluid', fontsize=7.5, ha='center',
            va='center', color='#2060a0', zorder=4)
    ax.text(cx - a_draw + 0.35, cy + c_draw - 0.35, 'Wall', fontsize=7,
            ha='center', va='center', color='#805030', zorder=4, rotation=50)

    # Airborne pathway (left)
    x_air = -3.5
    for dy in np.linspace(-0.8, 0.8, 5):
        ax.annotate('', xy=(cx - a_draw - 0.15, cy + dy * 1.2),
                    xytext=(x_air, cy + dy * 1.2),
                    arrowprops=dict(arrowstyle='->', color=C_ORANGE,
                                    lw=0.7, alpha=0.6))
    for xw in [-3.0, -2.4]:
        ys = np.linspace(-1.2, 1.2, 40)
        xs = xw + 0.08 * np.sin(ys * 5)
        ax.plot(xs, ys, color=C_ORANGE, lw=0.6, alpha=0.5)
    ax.text(x_air - 0.3, 2.0, 'Airborne\npressure\nwaves', fontsize=7.5,
            ha='center', va='bottom', color=C_ORANGE, fontweight='bold')

    # Mechanical pathway (bottom)
    y_mech = -2.4
    spine_x = np.array([-0.8, 0.0, 0.4, 1.0, 1.8])
    ax.plot(spine_x, np.full_like(spine_x, y_mech + 0.15), 's',
            color=C_GRAY, markersize=6, zorder=5)
    ax.plot([spine_x[0] - 0.3, spine_x[-1] + 0.3], [y_mech, y_mech],
            color=C_GRAY, lw=2)
    ax.text(cx, y_mech - 0.25, 'Spine / pelvis', fontsize=7, ha='center',
            color=C_GRAY)
    for xi in [0.0, 0.7, 1.4]:
        ax.annotate('', xy=(cx - 0.4 + xi, cy - c_draw + 0.05),
                    xytext=(cx - 0.4 + xi, y_mech + 0.3),
                    arrowprops=dict(arrowstyle='->', color=C_PURPLE,
                                    lw=1.0, linestyle='--'))
    ax.text(cx + 2.0, (y_mech + cy - c_draw) / 2, 'Mechanical\n(WBV)',
            fontsize=7.5, ha='left', va='center', color=C_PURPLE,
            fontweight='bold')

    # Parameter annotation box
    txt = (r'$a = 0.15$–$0.22$ m' + '\n' +
           r'$c/a = 0.5$–$0.8$' + '\n' +
           r'$h = 5$–$15$ mm' + '\n' +
           r'$E = 0.05$–$5$ MPa')
    props = dict(boxstyle='round,pad=0.4', facecolor='white',
                 edgecolor='gray', alpha=0.9)
    ax.text(4.5, 2.2, txt, fontsize=7, va='top', ha='center', bbox=props)

    _save(fig, 'fig_geometry_schematic')


# ═══════════════════════════════════════════════════════════════════════
# 2. MODE SHAPES — n=0 (breathing), n=2, n=3, n=4
# ═══════════════════════════════════════════════════════════════════════
def fig_mode_shapes():
    """Cross-section mode shapes for n=0, 2, 3, 4."""
    fig, axes = plt.subplots(1, 4, figsize=(DOUBLE_COL, 2.2))

    mode_ns = [0, 2, 3, 4]
    mode_labels = [
        r'$n = 0$ (breathing)',
        r'$n = 2$ (oblate–prolate)',
        r'$n = 3$ (trefoil)',
        r'$n = 4$ (quadrefoil)',
    ]

    theta = np.linspace(0, 2 * np.pi, 300)

    for idx, (ax, n, label) in enumerate(zip(axes, mode_ns, mode_labels)):
        ax.set_aspect('equal')
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.7, 1.7)
        ax.axis('off')

        r_eq = 1.0
        # Equilibrium circle
        ax.plot(r_eq * np.cos(theta), r_eq * np.sin(theta),
                'k-', lw=1.0)

        if n == 0:
            # Breathing: uniform expansion/contraction
            r_exp, r_con = 1.25, 0.8
            ax.plot(r_exp * np.cos(theta), r_exp * np.sin(theta),
                    '--', color=C_RED, lw=0.9)
            ax.plot(r_con * np.cos(theta), r_con * np.sin(theta),
                    '--', color=C_BLUE, lw=0.9)
            for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
                dx, dy = 0.18 * np.cos(ang), 0.18 * np.sin(ang)
                ax.annotate('', xy=(np.cos(ang) + dx, np.sin(ang) + dy),
                            xytext=(np.cos(ang), np.sin(ang)),
                            arrowprops=dict(arrowstyle='->', color=C_RED,
                                            lw=0.6))
        else:
            amp = 0.25 if n == 2 else 0.22 if n == 3 else 0.20
            r_def1 = r_eq + amp * np.cos(n * theta)
            r_def2 = r_eq - amp * np.cos(n * theta)
            ax.plot(r_def1 * np.cos(theta), r_def1 * np.sin(theta),
                    '--', color=C_RED, lw=0.9)
            ax.plot(r_def2 * np.cos(theta), r_def2 * np.sin(theta),
                    '--', color=C_BLUE, lw=0.9)
            # Displacement arrows at lobes
            for k in range(2 * n):
                ang = k * np.pi / n
                sgn = 1 if k % 2 == 0 else -1
                dx = sgn * 0.16 * np.cos(ang)
                dy = sgn * 0.16 * np.sin(ang)
                ax.annotate('', xy=(np.cos(ang) + dx, np.sin(ang) + dy),
                            xytext=(np.cos(ang), np.sin(ang)),
                            arrowprops=dict(arrowstyle='->', color=C_RED,
                                            lw=0.6))

        ax.text(0, -1.55, label, fontsize=7, ha='center', va='top')

    leg_elements = [
        Line2D([0], [0], color='k', lw=1.0, label='Equilibrium'),
        Line2D([0], [0], color=C_RED, lw=0.9, ls='--', label='Phase A'),
        Line2D([0], [0], color=C_BLUE, lw=0.9, ls='--', label='Phase B'),
    ]
    fig.legend(handles=leg_elements, loc='upper right', ncol=3,
               frameon=True, fontsize=7, bbox_to_anchor=(0.98, 0.99))
    fig.subplots_adjust(wspace=0.05)
    _save(fig, 'fig_mode_shapes')


# ═══════════════════════════════════════════════════════════════════════
# 3. FREQUENCY vs E — f₂, f₃, f₄ with ISO band and canonical point
# ═══════════════════════════════════════════════════════════════════════
def fig_frequency_vs_E():
    """Flexural mode frequencies vs Young's modulus with ISO 2631 band."""
    fig, ax = plt.subplots(figsize=(SINGLE_COL, 2.8))

    E_range = np.logspace(-2, 1, 200)  # 0.01 – 10 MPa
    markers_dict = {2: ('o', C_BLUE), 3: ('s', C_ORANGE), 4: ('^', C_GREEN)}

    for n, (mkr, clr) in markers_dict.items():
        freqs = []
        for E_MPa in E_range:
            model = AbdominalModelV2(E=E_MPa * 1e6, a=0.18, b=0.18, c=0.12)
            f = flexural_mode_frequencies_v2(model, n_max=n)
            freqs.append(f[n])
        freqs = np.array(freqs)
        ax.loglog(E_range, freqs, color=clr, label=f'$n = {n}$')
        idx = np.array([20, 60, 100, 140, 180])
        idx = idx[idx < len(E_range)]
        ax.plot(E_range[idx], freqs[idx], mkr, color=clr, markersize=3.5,
                zorder=5)

    # ISO 2631 band (4–8 Hz)
    ax.axhspan(4, 8, color=C_CYAN, alpha=0.12, zorder=0)
    ax.text(0.012, 5.8, 'ISO 2631\n(4–8 Hz)', fontsize=6.5,
            color=C_CYAN, alpha=0.85, va='center')

    # Canonical point: E = 0.1 MPa, n=2
    model_canon = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f2_canon = flexural_mode_frequencies_v2(model_canon, n_max=2)[2]
    ax.plot(0.1, f2_canon, '*', color='k', markersize=8, zorder=10,
            label=f'Canonical ($f_2$={f2_canon:.1f} Hz)')

    # Muscle state regions
    ax.axvspan(0.05, 0.2, color=C_GREEN, alpha=0.07, zorder=0)
    ax.axvspan(5, 10, color=C_RED, alpha=0.07, zorder=0)
    ax.text(0.1, 1.4, 'Relaxed', fontsize=6.5, ha='center', color=C_GREEN,
            fontweight='bold')
    ax.text(7, 100, 'Tensed', fontsize=6.5, ha='center', color=C_RED,
            fontweight='bold')

    ax.set_xlabel("Young's modulus $E$ (MPa)")
    ax.set_ylabel('Frequency $f_n$ (Hz)')
    ax.set_xlim(0.01, 10)
    ax.set_ylim(1, 200)
    ax.legend(loc='upper left', frameon=True, fontsize=7)
    fig.tight_layout()
    _save(fig, 'fig_frequency_vs_E')


# ═══════════════════════════════════════════════════════════════════════
# 4. UQ SOBOL INDICES — bar chart of S₁ and S_T
# ═══════════════════════════════════════════════════════════════════════
def fig_uq_sobol_indices():
    """Bar chart of Sobol first-order (S₁) and total-order (S_T) indices."""
    print("  Running Sobol analysis (may take a few minutes)...")
    sobol = run_sobol(n_base=1024)  # smaller base for speed
    si_f = sobol['f_n2']

    names = PARAM_NAMES
    s1 = np.array([si_f['S1'][n] for n in names])
    st = np.array([si_f['ST'][n] for n in names])

    # Sort by total-order
    order = np.argsort(st)[::-1]
    names_sorted = [names[i] for i in order]
    s1_sorted = s1[order]
    st_sorted = st[order]

    pretty = {
        'E': r'$E$',
        'a': r'$a$',
        'c': r'$c$',
        'h': r'$h$',
        'nu': r'$\nu$',
        'rho_wall': r'$\rho_w$',
        'rho_fluid': r'$\rho_f$',
        'P_iap': r'$P_{\rm iap}$',
        'loss_tangent': r'$\tan\delta$',
    }
    labels = [pretty.get(n, n) for n in names_sorted]

    fig, ax = plt.subplots(figsize=(SINGLE_COL, 3.0))
    x = np.arange(len(labels))
    w = 0.35
    bars1 = ax.barh(x + w / 2, s1_sorted, height=w, color=C_BLUE,
                    edgecolor='k', linewidth=0.4, hatch='///',
                    label='First-order $S_1$')
    bars2 = ax.barh(x - w / 2, st_sorted, height=w, color=C_ORANGE,
                    edgecolor='k', linewidth=0.4, hatch='\\\\\\',
                    label='Total-order $S_T$')
    ax.set_yticks(x)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Sobol sensitivity index')
    ax.legend(loc='lower right', fontsize=7, frameon=True)
    ax.invert_yaxis()
    ax.set_xlim(0, min(1.0, max(st_sorted.max(), s1_sorted.max()) * 1.15))
    fig.tight_layout()
    _save(fig, 'fig_uq_sobol_indices')


# ═══════════════════════════════════════════════════════════════════════
# 5. UQ FREQUENCY DISTRIBUTION — histogram/KDE of f₂ with CI markers
# ═══════════════════════════════════════════════════════════════════════
def fig_uq_frequency_distribution():
    """Monte Carlo histogram of f₂ with 90% CI and mean markers."""
    print("  Running Monte Carlo (N=10000)...")
    rng = np.random.default_rng(seed=42)
    X = sample_parameters(N_MC, rng)
    results = evaluate_batch(X)
    f_arr = results['f_n2']
    stats = summarise(f_arr, 'f_n2')

    valid = f_arr[np.isfinite(f_arr)]

    fig, ax = plt.subplots(figsize=(SINGLE_COL, 2.8))
    ax.hist(valid, bins=60, density=True, color=C_BLUE, alpha=0.75,
            edgecolor='white', linewidth=0.3, zorder=3)

    # KDE overlay
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(valid)
    x_kde = np.linspace(valid.min(), valid.max(), 300)
    ax.plot(x_kde, kde(x_kde), '-', color='k', lw=1.2, zorder=4, label='KDE')

    # Mean and CI markers
    mean = stats['f_n2_mean']
    p5, p95 = stats['f_n2_p5'], stats['f_n2_p95']
    ax.axvline(mean, color=C_RED, ls='--', lw=1.0, zorder=5,
               label=f'Mean = {mean:.1f} Hz')
    ax.axvspan(p5, p95, alpha=0.12, color=C_RED, zorder=1,
               label=f'90% CI [{p5:.1f}, {p95:.1f}] Hz')

    ax.set_xlabel(r'$f_2$ (Hz)')
    ax.set_ylabel('Probability density')
    ax.legend(loc='upper right', fontsize=6.5, frameon=True)
    fig.tight_layout()
    _save(fig, 'fig_uq_frequency_distribution')


# ═══════════════════════════════════════════════════════════════════════
# 6. COUPLING COMPARISON — airborne vs mechanical displacement
# ═══════════════════════════════════════════════════════════════════════
def fig_coupling_comparison():
    """Side-by-side bar chart: airborne vs mechanical at matched exposures."""
    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]

    # Airborne displacements at various SPL
    spls = [100, 110, 120, 130]
    xi_air = []
    for spl in spls:
        r = flexural_mode_pressure_response(f2, spl, 2, model)
        xi_air.append(r['displacement_um'])

    # Mechanical displacements at various accelerations
    accels = [0.25, 0.5, 1.0, 1.15]  # m/s² RMS
    xi_mech = []
    for a_rms in accels:
        exp = WBVExposure(acceleration_rms_ms2=a_rms, frequency_hz=f2)
        r = mechanical_excitation_response(exp, model, mode_n=2,
                                           use_empirical=False)
        xi_mech.append(r['relative_displacement_um'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE_COL, 2.8))

    # Left: Airborne
    x1 = np.arange(len(spls))
    bars1 = ax1.bar(x1, xi_air, color=C_ORANGE, edgecolor='k', linewidth=0.4,
                    width=0.6, hatch='///', zorder=3)
    ax1.set_yscale('log')
    ax1.set_xticks(x1)
    ax1.set_xticklabels([f'{s} dB' for s in spls])
    ax1.set_ylabel('Displacement (μm)')
    ax1.set_xlabel('Sound pressure level')
    ax1.axhline(1.0, color=C_RED, ls=':', lw=0.8, zorder=5)
    ax1.text(0.97, 0.93, 'Piezo\nthreshold', fontsize=6, color=C_RED,
             ha='right', va='top', transform=ax1.transAxes)
    ax1.text(0.03, 0.95, '(a) Airborne', transform=ax1.transAxes,
             fontsize=8, fontweight='bold', va='top')
    for bar, val in zip(bars1, xi_air):
        xc = bar.get_x() + bar.get_width() / 2
        ax1.text(xc, val * 1.3, f'{val:.2g}', ha='center', va='bottom',
                 fontsize=6)

    # Right: Mechanical
    x2 = np.arange(len(accels))
    bars2 = ax2.bar(x2, xi_mech, color=C_PURPLE, edgecolor='k', linewidth=0.4,
                    width=0.6, hatch='\\\\\\', zorder=3)
    ax2.set_yscale('log')
    ax2.set_xticks(x2)
    ax2.set_xticklabels([f'{a} m/s²' for a in accels])
    ax2.set_ylabel('Displacement (μm)')
    ax2.set_xlabel('RMS acceleration')
    ax2.axhline(1.0, color=C_RED, ls=':', lw=0.8, zorder=5)
    ax2.text(0.03, 0.95, '(b) Mechanical (WBV)', transform=ax2.transAxes,
             fontsize=8, fontweight='bold', va='top')
    for bar, val in zip(bars2, xi_mech):
        xc = bar.get_x() + bar.get_width() / 2
        ax2.text(xc, val * 1.3, f'{val:.0f}', ha='center', va='bottom',
                 fontsize=6)

    # Match y-limits across panels
    y_lo = min(ax1.get_ylim()[0], ax2.get_ylim()[0])
    y_hi = max(ax1.get_ylim()[1], ax2.get_ylim()[1])
    ax1.set_ylim(y_lo, y_hi)
    ax2.set_ylim(y_lo, y_hi)

    fig.tight_layout()
    _save(fig, 'fig_coupling_comparison')


# ═══════════════════════════════════════════════════════════════════════
# 7. ENERGY BUDGET — waterfall showing where acoustic energy goes
# ═══════════════════════════════════════════════════════════════════════
def fig_energy_budget():
    """Waterfall / horizontal log bar showing the acoustic energy pathway."""
    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    R = model.equivalent_sphere_radius
    f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]
    omega = 2 * np.pi * f2

    spl = 120.0
    p_inc = 20e-6 * 10 ** (spl / 20)
    I_inc = p_inc ** 2 / (2 * 1.225 * 343.0)

    P_intercept = I_inc * np.pi * R ** 2

    # Impedance mismatch
    Z_air = 1.225 * 343.0
    Z_tissue = 1040.0 * 1540.0
    R_coeff = ((Z_tissue - Z_air) / (Z_tissue + Z_air)) ** 2
    T_coeff = 1 - R_coeff
    P_reflected = P_intercept * R_coeff
    P_transmitted = P_intercept * T_coeff

    # Scattering / (ka)^n coupling loss
    ka = omega * R / 343.0
    coupling = ka ** 4  # (ka)^{2n} for n=2
    P_scattered = P_transmitted * (1 - coupling)
    P_coupled = P_transmitted * coupling

    # Self-consistent absorption
    acs = absorption_cross_section(model, mode_n=2)
    P_absorbed = acs['sigma_abs_m2'] * I_inc
    efficiency = acs['efficiency']

    rd = radiation_damping_flexural(model, mode_n=2, medium='air')
    P_radiated = P_absorbed * (rd['zeta_rad'] / (rd['zeta_rad'] + model.damping_ratio))
    P_dissipated = P_absorbed - P_radiated

    fig, ax = plt.subplots(figsize=(SINGLE_COL, 3.2))

    labels = [
        'Incident\n(120 dB)',
        'Reflected\n(impedance)',
        'Transmitted',
        'Scattering\nloss $(ka)^4$',
        'Modal\ncoupled',
        'Absorbed\n(reciprocity)',
        'Dissipated\n(structural)',
        'Re-radiated',
    ]
    values = [
        P_intercept, P_reflected, P_transmitted, P_scattered,
        P_coupled, P_absorbed, P_dissipated, P_radiated,
    ]
    colors_e = [
        C_BLUE, C_GRAY, C_ORANGE, C_GRAY,
        C_GREEN, C_PURPLE, C_RED, C_CYAN,
    ]
    hatches_e = ['', '///', '', '\\\\\\', '', '...', 'xxx', '+++']

    values = [max(v, 1e-30) for v in values]

    bars = ax.barh(range(len(labels)), values, color=colors_e,
                   edgecolor='k', linewidth=0.4, height=0.6, zorder=3)
    for bar, h in zip(bars, hatches_e):
        bar.set_hatch(h)

    ax.set_xscale('log')
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel('Power (W)')

    for i, (bar, val) in enumerate(zip(bars, values)):
        if val > 1e-24:
            exp = int(np.floor(np.log10(val)))
            mantissa = val / 10 ** exp
            txt = f'$10^{{{exp}}}$' if abs(mantissa - 1.0) < 0.05 else \
                  f'{mantissa:.1f}×$10^{{{exp}}}$'
            ax.text(val * 2, i, txt, va='center', fontsize=5.5)

    eff_str = f'Absorption efficiency: {efficiency:.1e}'
    ax.text(0.95, 0.02, eff_str, transform=ax.transAxes, fontsize=6.5,
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', fc='lightyellow', ec='gray'))

    ax.set_xlim(1e-22, 1e-2)
    fig.tight_layout()
    _save(fig, 'fig_energy_budget')


# ═══════════════════════════════════════════════════════════════════════
# 8. DIMENSIONAL COLLAPSE — raw vs dimensionless
# ═══════════════════════════════════════════════════════════════════════
def fig_dimensional_collapse():
    """Three-panel: (a) raw scattered, (b) collapsed Π₀ vs h/a, (c) parity."""
    print("  Computing parametric sweep for dimensional collapse...")
    results = parametric_sweep_dimensionless()

    ca_vals = sorted(set(r['c_over_a'] for r in results))
    E_vals = sorted(set(r['E_MPa'] for r in results))
    markers = ['o', 's', '^', 'D', 'v', 'p']
    colors_da = plt.cm.viridis(np.linspace(0.15, 0.85, len(ca_vals)))

    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE_COL, 2.5))

    # Panel (a): raw dimensional — scattered
    ax = axes[0]
    for j, ca in enumerate(ca_vals):
        for k, E in enumerate(E_vals):
            subset = [r for r in results
                      if r['c_over_a'] == ca and r['E_MPa'] == E]
            if not subset:
                continue
            h_mm = [r['h_m'] * 1000 for r in subset]
            f_hz = [r['f_hz'] for r in subset]
            label = f'$c/a$={ca}' if k == 0 else None
            ax.scatter(h_mm, f_hz, c=[colors_da[j]],
                       marker=markers[k % len(markers)],
                       s=12, alpha=0.5, edgecolors='none', label=label)
    ax.set_xlabel('$h$ (mm)')
    ax.set_ylabel('$f_2$ (Hz)')
    ax.text(0.05, 0.95, '(a)', transform=ax.transAxes, fontsize=9,
            fontweight='bold', va='top')
    ax.legend(fontsize=5.5, loc='upper left', markerscale=0.7)

    # Panel (b): collapsed Π₀ vs h/a
    ax = axes[1]
    rho_r = results[0]['rho_ratio']
    nu_val = results[0]['nu']
    ha_line = np.linspace(0.015, 0.11, 200)
    P_E_vals = sorted(set(r['P_over_E'] for r in results))

    for j, ca in enumerate(ca_vals):
        phi_stack = np.array([
            phi_analytical(ha_line, ca, rho_r, pe, nu_val, n=2)
            for pe in P_E_vals
        ])
        phi_mid = phi_stack[len(P_E_vals) // 2]
        ax.plot(ha_line, phi_mid, color=colors_da[j], lw=1.2, alpha=0.8,
                label=f'$c/a$={ca}')

    # Overlay numerical points (deduplicated)
    seen = set()
    for j, ca in enumerate(ca_vals):
        for k, E in enumerate(E_vals):
            subset = [r for r in results
                      if r['c_over_a'] == ca and r['E_MPa'] == E]
            for r in subset:
                key = (r['h_over_a'], r['c_over_a'], r['E_MPa'])
                if key in seen:
                    continue
                seen.add(key)
                ax.scatter(r['h_over_a'], r['Pi_0'], c=[colors_da[j]],
                           marker=markers[k % len(markers)],
                           s=12, alpha=0.6, edgecolors='none')

    ax.set_xlabel(r'$\Pi_1 = h/a$')
    ax.set_ylabel(r'$\Pi_0 = f_2 \, a \sqrt{\rho_f / E}$')
    ax.text(0.05, 0.95, '(b)', transform=ax.transAxes, fontsize=9,
            fontweight='bold', va='top')
    ax.legend(fontsize=5.5, loc='upper left', markerscale=0.7)

    # Panel (c): parity
    ax = axes[2]
    Pi_num = np.array([r['Pi_0'] for r in results])
    Pi_ana = np.array([r['Pi_0_analytical'] for r in results])
    ca_arr = np.array([r['c_over_a'] for r in results])

    for j, ca in enumerate(ca_vals):
        mask = ca_arr == ca
        ax.scatter(Pi_ana[mask], Pi_num[mask], c=[colors_da[j]], s=8,
                   alpha=0.6, edgecolors='none', label=f'$c/a$={ca}')

    lims = [min(Pi_num.min(), Pi_ana.min()) * 0.95,
            max(Pi_num.max(), Pi_ana.max()) * 1.05]
    ax.plot(lims, lims, 'k--', lw=0.7, alpha=0.5)
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel(r'$\Phi_2$ (analytical)')
    ax.set_ylabel(r'$\Pi_0$ (numerical)')
    ax.set_aspect('equal')
    ax.text(0.05, 0.95, '(c)', transform=ax.transAxes, fontsize=9,
            fontweight='bold', va='top')

    fig.tight_layout()
    _save(fig, 'fig_dimensional_collapse')


# ═══════════════════════════════════════════════════════════════════════
# 9. SCALING LAW — f₂ vs body size across species
# ═══════════════════════════════════════════════════════════════════════
def fig_scaling_law():
    """f₂ vs body size (semi-major axis a) for rat → cat → pig → human."""
    data = animal_scaling(mode_n=2)
    species_order = ['rat', 'cat', 'pig', 'human']
    species_labels = ['Rat', 'Cat', 'Pig', 'Human']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE_COL, 2.8))

    a_vals = [data[sp]['a_cm'] for sp in species_order]
    f_vals = [data[sp]['f_hz'] for sp in species_order]
    Pi0_vals = [data[sp]['Pi_0'] for sp in species_order]
    markers_sp = ['D', 's', '^', 'o']
    colors_sp = [C_RED, C_ORANGE, C_GREEN, C_BLUE]

    # Left panel: f₂ vs a (log-log)
    for sp, lab, a, f, mkr, clr in zip(species_order, species_labels,
                                        a_vals, f_vals, markers_sp, colors_sp):
        ax1.plot(a, f, mkr, color=clr, markersize=7, label=lab, zorder=5)

    # Fit power law f = C * a^alpha
    a_arr = np.array(a_vals)
    f_arr = np.array(f_vals)
    log_a, log_f = np.log10(a_arr), np.log10(f_arr)
    slope, intercept = np.polyfit(log_a, log_f, 1)
    a_fit = np.linspace(a_arr.min() * 0.8, a_arr.max() * 1.2, 50)
    f_fit = 10 ** (slope * np.log10(a_fit) + intercept)
    ax1.plot(a_fit, f_fit, 'k--', lw=0.8, alpha=0.5,
             label=f'$f_2 \\propto a^{{{slope:.2f}}}$')

    # ISO band
    ax1.axhspan(4, 8, color=C_CYAN, alpha=0.12, zorder=0)
    ax1.text(a_arr.max() * 0.85, 5.5, 'ISO\n4–8 Hz', fontsize=6, color=C_CYAN,
             alpha=0.8, ha='center')

    ax1.set_xlabel('Semi-major axis $a$ (cm)')
    ax1.set_ylabel('$f_2$ (Hz)')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.legend(loc='upper right', fontsize=6.5, frameon=True)
    ax1.text(0.03, 0.95, '(a)', transform=ax1.transAxes, fontsize=9,
             fontweight='bold', va='top')

    # Right panel: dimensionless Π₀ (should be roughly constant if scaling holds)
    x_pos = np.arange(len(species_order))
    bars = ax2.bar(x_pos, Pi0_vals, color=colors_sp, edgecolor='k',
                   linewidth=0.4, width=0.6, zorder=3)
    for bar, h_v in zip(bars, HATCHES[:len(bars)]):
        bar.set_hatch(h_v)

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(species_labels)
    ax2.set_ylabel(r'$\Pi_0 = f_2 \, a \sqrt{\rho_f / E}$')
    ax2.text(0.03, 0.95, '(b)', transform=ax2.transAxes, fontsize=9,
             fontweight='bold', va='top')

    # Annotate values
    for i, (bar, val) in enumerate(zip(bars, Pi0_vals)):
        ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.001,
                 f'{val:.4f}', ha='center', va='bottom', fontsize=6.5)

    fig.tight_layout()
    _save(fig, 'fig_scaling_law')


# ═══════════════════════════════════════════════════════════════════════
# 10. TRANSMISSIBILITY — model H(f) vs ISO 2631 data range
# ═══════════════════════════════════════════════════════════════════════
def fig_transmissibility():
    """Model transmissibility H(f) overlaid on ISO 2631 empirical data."""
    fig, ax = plt.subplots(figsize=(SINGLE_COL, 2.8))

    # ISO 2631 empirical data
    iso_freq = ISO_2631_TRANSMISSIBILITY[:, 0]
    iso_T = ISO_2631_TRANSMISSIBILITY[:, 1]
    ax.plot(iso_freq, iso_T, 'o-', color=C_BLUE, markersize=4, lw=1.2,
            label='ISO 2631 (empirical)', zorder=5)

    # Model transmissibility for several E values
    E_vals_MPa = [0.05, 0.1, 0.3]
    colors_t = [C_GREEN, C_RED, C_ORANGE]
    styles = ['-', '-', '--']

    f_theory = np.linspace(1, 25, 300)
    for E_MPa, clr, ls in zip(E_vals_MPa, colors_t, styles):
        model = AbdominalModelV2(E=E_MPa * 1e6, a=0.18, b=0.18, c=0.12)
        f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]
        zeta = model.damping_ratio
        T_abs = []
        for f in f_theory:
            r_ratio = f / f2
            T = np.sqrt((1 + (2 * zeta * r_ratio) ** 2) /
                        ((1 - r_ratio ** 2) ** 2 + (2 * zeta * r_ratio) ** 2))
            T_abs.append(T)
        T_abs = np.array(T_abs)
        ax.plot(f_theory, T_abs, ls, color=clr, lw=1.0,
                label=f'Model $E$={E_MPa} MPa ($f_2$={f2:.1f} Hz)')

    # ISO 2631 sensitive band
    ax.axvspan(4, 8, color=C_CYAN, alpha=0.10, zorder=0)
    ax.text(6, ax.get_ylim()[1] * 0.9 if ax.get_ylim()[1] > 1 else 3.0,
            'ISO 2631\n4–8 Hz', fontsize=6, color=C_CYAN, alpha=0.8,
            ha='center', va='top')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Transmissibility $|H(f)|$')
    ax.set_xlim(1, 25)
    ax.set_ylim(0, 4.0)
    ax.legend(loc='upper right', fontsize=6, frameon=True)
    fig.tight_layout()
    _save(fig, 'fig_transmissibility')


# ═══════════════════════════════════════════════════════════════════════
# 11. NONLINEAR BACKBONE — backbone curve + jump phenomenon
# ═══════════════════════════════════════════════════════════════════════
def fig_nonlinear_backbone():
    """Backbone curve showing hardening behaviour and jump phenomenon."""
    nl_model = NonlinearShellModel()
    n = 2

    props = linear_modal_properties(nl_model, n)
    f0 = props['f_hz']
    alpha = cubic_stiffness_coefficient(nl_model, n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE_COL, 2.8))

    # Left: backbone curve
    A_range = np.linspace(0, nl_model.h * 2.0, 200)  # up to 2h
    f_backbone = backbone_freq_hz(f0, alpha, A_range)

    ax1.plot(A_range * 1e3, f_backbone, '-', color=C_BLUE, lw=1.5,
             label='Backbone $\\omega(A)$')
    ax1.axhline(f0, color=C_GRAY, ls=':', lw=0.8, alpha=0.7)
    ax1.text(A_range[-1] * 1e3 * 0.6, f0 * 0.98,
             f'$f_0$ = {f0:.2f} Hz', fontsize=7, color=C_GRAY)

    # Mark nonlinearity threshold (5% shift)
    from src.analytical.nonlinear_analysis import nonlinearity_threshold
    thresh = nonlinearity_threshold(nl_model, n)
    A_crit = thresh['A_crit_m']
    f_crit = backbone_freq_hz(f0, alpha, np.array([A_crit]))[0]
    ax1.plot(A_crit * 1e3, f_crit, 'v', color=C_RED, markersize=6, zorder=6,
             label=f'5% shift ($A$={A_crit * 1e3:.1f} mm)')

    # Mark h
    ax1.axvline(nl_model.h * 1e3, color=C_GREEN, ls='--', lw=0.8, alpha=0.7)
    ax1.text(nl_model.h * 1e3 * 1.05, ax1.get_ylim()[0] + 0.1 if ax1.get_ylim()[0] > 0 else f0 * 0.97,
             '$h$', fontsize=8, color=C_GREEN)

    ax1.set_xlabel('Amplitude $A$ (mm)')
    ax1.set_ylabel('Resonance frequency (Hz)')
    ax1.legend(loc='upper left', fontsize=6.5, frameon=True)
    ax1.text(0.03, 0.95, '(a)', transform=ax1.transAxes, fontsize=9,
             fontweight='bold', va='top')

    # Right: frequency response showing jump
    F_over_m_low = wbv_modal_force(nl_model, n, a_wbv=0.3)
    F_over_m_high = wbv_modal_force(nl_model, n, a_wbv=1.5)

    f_sweep = np.linspace(f0 * 0.6, f0 * 1.6, 400)

    for F_m, lbl, clr, ls in [
        (F_over_m_low, '0.3 m/s²', C_GREEN, '-'),
        (F_over_m_high, '1.5 m/s²', C_RED, '-'),
    ]:
        A_stab, A_unstab = duffing_frequency_response(
            nl_model, n, F_m, f_sweep, use_amplitude_damping=True)
        ax2.plot(f_sweep, A_stab * 1e3, ls, color=clr, lw=1.2,
                 label=f'$a_{{\\rm rms}}$ = {lbl}')
        # Unstable branch (dashed)
        valid = ~np.isnan(A_unstab)
        if valid.any():
            ax2.plot(f_sweep[valid], A_unstab[valid] * 1e3, '--', color=clr,
                     lw=0.8, alpha=0.6)

    # Backbone overlay
    ax2.plot(f_backbone, A_range * 1e3, ':', color=C_GRAY, lw=0.8,
             label='Backbone', zorder=2)

    ax2.axvline(f0, color=C_GRAY, ls=':', lw=0.5, alpha=0.5)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Amplitude $A$ (mm)')
    ax2.legend(loc='upper right', fontsize=6.5, frameon=True)
    ax2.text(0.03, 0.95, '(b)', transform=ax2.transAxes, fontsize=9,
             fontweight='bold', va='top')

    # Arrow indicating "jump" if bistable region exists
    jmp = jump_amplitude(nl_model, n)
    if jmp['A_jump_m'] > 0:
        ax2.annotate('Jump', xy=(f0 * 1.1, jmp['A_jump_m'] * 1e3),
                     fontsize=7, color=C_RED, fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color=C_RED, lw=0.8),
                     xytext=(f0 * 1.3, jmp['A_jump_m'] * 1e3 * 1.5))

    fig.tight_layout()
    _save(fig, 'fig_nonlinear_backbone')


# ═══════════════════════════════════════════════════════════════════════
# 12. BC COMPARISON — f₂ for different boundary conditions
# ═══════════════════════════════════════════════════════════════════════
def fig_bc_comparison():
    """Bar chart of f₂ for free, simply-supported, and clamped BCs."""
    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)

    # Free boundary (our standard model — no constraints)
    f_free = flexural_mode_frequencies_v2(model, n_max=4)

    # Simply-supported: additional membrane constraint raises frequency ~1.5×
    # Clamped: full constraint raises frequency ~2× (Leissa, 1973)
    bc_factors = {
        'Free': 1.0,
        'Simply\nsupported': 1.5,
        'Clamped': 2.0,
    }

    modes = [2, 3, 4]
    mode_colors = [C_BLUE, C_ORANGE, C_GREEN]
    mode_hatches = ['///', '\\\\\\', '...']

    fig, ax = plt.subplots(figsize=(SINGLE_COL, 3.0))
    bc_names = list(bc_factors.keys())
    x = np.arange(len(bc_names))
    width = 0.22

    for i, (n, clr, hatch) in enumerate(zip(modes, mode_colors, mode_hatches)):
        f_base = f_free[n]
        vals = [f_base * factor for factor in bc_factors.values()]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width, color=clr, edgecolor='k',
                      linewidth=0.4, hatch=hatch, label=f'$n = {n}$',
                      zorder=3)

    # ISO 2631 band
    ax.axhspan(4, 8, color=C_CYAN, alpha=0.12, zorder=0)
    ax.text(0.97, 0.93, 'ISO 2631\n4–8 Hz', transform=ax.transAxes,
            fontsize=6, color=C_CYAN, ha='right', va='top', alpha=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(bc_names)
    ax.set_ylabel('Frequency $f_n$ (Hz)')
    ax.set_xlabel('Boundary condition')
    ax.legend(loc='upper left', fontsize=7, frameon=True)
    fig.tight_layout()
    _save(fig, 'fig_bc_comparison')


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  JSV Paper — Publication-Ready Figure Set v4")
    print("  Generating 12 camera-ready figures")
    print("=" * 60)
    print()

    generators = [
        ("1/12", "Geometry schematic", fig_geometry_schematic),
        ("2/12", "Mode shapes", fig_mode_shapes),
        ("3/12", "Frequency vs E", fig_frequency_vs_E),
        ("4/12", "UQ Sobol indices", fig_uq_sobol_indices),
        ("5/12", "UQ frequency distribution", fig_uq_frequency_distribution),
        ("6/12", "Coupling comparison", fig_coupling_comparison),
        ("7/12", "Energy budget", fig_energy_budget),
        ("8/12", "Dimensional collapse", fig_dimensional_collapse),
        ("9/12", "Scaling law", fig_scaling_law),
        ("10/12", "Transmissibility", fig_transmissibility),
        ("11/12", "Nonlinear backbone", fig_nonlinear_backbone),
        ("12/12", "BC comparison", fig_bc_comparison),
    ]

    failed = []
    for num, name, func in generators:
        print(f"[{num}] {name}...")
        try:
            func()
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed.append((name, str(e)))

    print()
    print("=" * 60)
    if failed:
        print(f"  {len(generators) - len(failed)}/{len(generators)} figures generated")
        for name, err in failed:
            print(f"  FAILED: {name}: {err}")
    else:
        print(f"  All {len(generators)} figures generated successfully")
    print(f"  Output: {FIG_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
