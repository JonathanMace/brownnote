"""
Generate all publication-quality figures for the JSV paper.

Camera-ready figures following JSV style guidelines:
- Single column: 3.5 inch, Double column: 7 inch
- Font: 8-10 pt
- DPI: 300
- Colorblind-friendly palette (tab10)
- All axes labeled with units
- Grid: light gray, dashed
- No titles (captions in LaTeX)
- Output: PNG (300 dpi) + PDF
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc, Ellipse
from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2, breathing_mode_v2,
    flexural_mode_pressure_response,
)
from src.analytical.mechanical_coupling import (
    WBVExposure, ISO_2631_TRANSMISSIBILITY,
    interpolate_transmissibility, mechanical_excitation_response,
    compare_airborne_vs_mechanical,
)
from src.analytical.parametric_analysis import (
    parametric_E_sweep, multi_parameter_sensitivity,
    energy_budget_v2, iso2631_comparison,
)
from src.analytical.energy_budget import (
    radiation_damping_flexural, absorption_cross_section,
    self_consistent_displacement,
)
from src.analytical.gas_pocket_resonance import (
    GasPocket, minnaert_frequency, constrained_bubble_frequency,
    elongated_pocket_frequency, acoustic_response_of_gas_pocket,
)
from src.analytical.multilayer_wall import (
    Layer, relaxed_layers, tensed_layers, obese_layers,
    compute_composite_properties, multilayer_to_v2_model,
)

# ── Output directory ──
FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'papers', 'paper1-brown-note', 'figures')
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

SINGLE_COL = 3.5   # inches
DOUBLE_COL = 7.0   # inches


def _save(fig, name):
    """Save figure as PNG and PDF."""
    png = os.path.join(FIG_DIR, f'{name}.png')
    pdf = os.path.join(FIG_DIR, f'{name}.pdf')
    fig.savefig(png, dpi=300)
    fig.savefig(pdf)
    plt.close(fig)
    print(f"  ✓ {name}.png + .pdf")
    return png, pdf


def _shade_iso_band(ax, ymin=None, ymax=None):
    """Shade the 4-8 Hz ISO 2631 band."""
    if ymin is None:
        ymin = ax.get_ylim()[0]
    if ymax is None:
        ymax = ax.get_ylim()[1]
    ax.axhspan(4, 8, color=C_CYAN, alpha=0.12, zorder=0)
    ax.text(ax.get_xlim()[1], 6, ' ISO\n 2631',
            fontsize=6.5, color=C_CYAN, alpha=0.8, va='center',
            ha='left', clip_on=True)


def _shade_iso_band_x(ax, label=True):
    """Shade the ISO band when frequency is on the x-axis."""
    yl = ax.get_ylim()
    ax.axvspan(4, 8, color=C_CYAN, alpha=0.12, zorder=0)
    if label:
        ax.text(6, yl[1]*0.95, 'ISO 2631\n4–8 Hz', fontsize=6.5,
                color=C_CYAN, alpha=0.8, va='top', ha='center')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 1: Geometry Schematic
# ═══════════════════════════════════════════════════════════════════════
def fig_geometry_schematic():
    fig, ax = plt.subplots(figsize=(DOUBLE_COL, 3.2))
    ax.set_aspect('equal')
    ax.set_xlim(-4.5, 5.5)
    ax.set_ylim(-2.8, 3.0)
    ax.axis('off')

    # Oblate spheroid (cross-section is an ellipse)
    cx, cy = 0.5, 0.0
    a_draw, c_draw = 2.2, 1.5  # semi-major, semi-minor for drawing

    # Outer shell
    shell = Ellipse((cx, cy), 2*a_draw, 2*c_draw,
                    facecolor='#e8d4c0', edgecolor='k', linewidth=1.2,
                    zorder=2)
    ax.add_patch(shell)

    # Inner cavity (fluid-filled)
    h_draw = 0.18
    inner = Ellipse((cx, cy), 2*(a_draw - h_draw), 2*(c_draw - h_draw),
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
    ax.text(cx + a_draw/2, y_dim_a - 0.2, r'$a$', fontsize=10,
            ha='center', color=C_RED, fontweight='bold')

    # Dimension labels — c (vertical)
    x_dim_c = cx + a_draw + 0.3
    ax.annotate('', xy=(x_dim_c, cy + c_draw), xytext=(x_dim_c, cy),
                arrowprops=dict(arrowstyle='<->', color=C_BLUE, lw=0.8))
    ax.text(x_dim_c + 0.15, cy + c_draw/2, r'$c$', fontsize=10,
            va='center', color=C_BLUE, fontweight='bold')

    # Wall thickness annotation — h
    theta = np.radians(40)
    x_out = cx + a_draw * np.cos(theta)
    y_out = cy + c_draw * np.sin(theta)
    x_in = cx + (a_draw - h_draw) * np.cos(theta)
    y_in = cy + (c_draw - h_draw) * np.sin(theta)
    x_lab = x_out + 0.5
    y_lab = y_out + 0.4
    ax.annotate(r'$h$', xy=((x_out+x_in)/2, (y_out+y_in)/2),
                xytext=(x_lab, y_lab), fontsize=10, color=C_GREEN,
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=0.7))

    # Labels for regions
    ax.text(cx, cy, 'Visceral\nfluid', fontsize=7.5, ha='center', va='center',
            color='#2060a0', zorder=4)
    ax.text(cx - a_draw + 0.35, cy + c_draw - 0.35, 'Wall', fontsize=7,
            ha='center', va='center', color='#805030', zorder=4, rotation=50)

    # === Airborne pathway (left) ===
    x_air = -3.5
    for dy in np.linspace(-0.8, 0.8, 5):
        ax.annotate('', xy=(cx - a_draw - 0.15, cy + dy*1.2),
                    xytext=(x_air, cy + dy*1.2),
                    arrowprops=dict(arrowstyle='->', color=C_ORANGE,
                                    lw=0.7, alpha=0.6))
    # Wavefronts
    for xw in [-3.0, -2.4]:
        ys = np.linspace(-1.2, 1.2, 40)
        xs = xw + 0.08 * np.sin(ys * 5)
        ax.plot(xs, ys, color=C_ORANGE, lw=0.6, alpha=0.5)
    ax.text(x_air - 0.3, 2.0, 'Airborne\npressure\nwaves', fontsize=7.5,
            ha='center', va='bottom', color=C_ORANGE, fontweight='bold')

    # === Mechanical pathway (bottom) ===
    y_mech = -2.4
    # Spine/pelvis base
    spine_x = np.array([-0.8, 0.0, 0.4, 1.0, 1.8])
    spine_y = np.full_like(spine_x, y_mech + 0.15)
    ax.plot(spine_x, spine_y, 's', color=C_GRAY, markersize=6, zorder=5)
    ax.plot([spine_x[0]-0.3, spine_x[-1]+0.3], [y_mech, y_mech],
            color=C_GRAY, lw=2)
    ax.text(cx, y_mech - 0.25, 'Spine / pelvis', fontsize=7, ha='center',
            color=C_GRAY)

    # Vibration arrows from base to shell
    for xi in [0.0, 0.7, 1.4]:
        ax.annotate('', xy=(cx - 0.4 + xi, cy - c_draw + 0.05),
                    xytext=(cx - 0.4 + xi, y_mech + 0.3),
                    arrowprops=dict(arrowstyle='->', color=C_PURPLE,
                                    lw=1.0, linestyle='--'))
    ax.text(cx + 2.0, (y_mech + cy - c_draw) / 2,
            'Mechanical\n(WBV)', fontsize=7.5,
            ha='left', va='center', color=C_PURPLE, fontweight='bold')

    # Model parameters annotation box
    txt = (r'$a = 0.15$–$0.22$ m' + '\n' +
           r'$c/a = 0.5$–$0.8$' + '\n' +
           r'$h = 5$–$15$ mm' + '\n' +
           r'$E = 0.05$–$5$ MPa')
    props = dict(boxstyle='round,pad=0.4', facecolor='white',
                 edgecolor='gray', alpha=0.9)
    ax.text(4.5, 2.2, txt, fontsize=7, va='top', ha='center', bbox=props)

    _save(fig, 'fig_geometry_schematic')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 2: Mode Shapes
# ═══════════════════════════════════════════════════════════════════════
def fig_mode_shapes():
    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE_COL, 2.4))

    mode_labels = [r'$n = 0$ (breathing)', r'$n = 2$ (oblate–prolate)',
                   r'$n = 3$ (trefoil)']

    for i, ax in enumerate(axes):
        ax.set_aspect('equal')
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.axis('off')

        theta = np.linspace(0, 2*np.pi, 200)

        if i == 0:
            # n=0 breathing mode: uniform radial expansion/contraction
            r_eq = 1.0
            r_exp = 1.25
            r_con = 0.8
            ax.plot(r_eq * np.cos(theta), r_eq * np.sin(theta),
                    'k-', lw=1.0, label='Equilibrium')
            ax.plot(r_exp * np.cos(theta), r_exp * np.sin(theta),
                    '--', color=C_RED, lw=1.0)
            ax.plot(r_con * np.cos(theta), r_con * np.sin(theta),
                    '--', color=C_BLUE, lw=1.0)
            # Arrows showing radial displacement
            for ang in np.linspace(0, 2*np.pi, 8, endpoint=False):
                dx, dy = 0.18*np.cos(ang), 0.18*np.sin(ang)
                ax.annotate('', xy=(r_eq*np.cos(ang)+dx, r_eq*np.sin(ang)+dy),
                            xytext=(r_eq*np.cos(ang), r_eq*np.sin(ang)),
                            arrowprops=dict(arrowstyle='->', color=C_RED,
                                            lw=0.7))

        elif i == 1:
            # n=2: prolate <-> oblate oscillation
            r_eq = 1.0
            amp = 0.25
            r_def1 = r_eq + amp * np.cos(2*theta)   # prolate
            r_def2 = r_eq - amp * np.cos(2*theta)   # oblate
            ax.plot(r_eq * np.cos(theta), r_eq * np.sin(theta),
                    'k-', lw=1.0)
            ax.plot(r_def1 * np.cos(theta), r_def1 * np.sin(theta),
                    '--', color=C_RED, lw=1.0)
            ax.plot(r_def2 * np.cos(theta), r_def2 * np.sin(theta),
                    '--', color=C_BLUE, lw=1.0)
            # Arrows at quadrature points
            for ang, sgn in [(0, 1), (np.pi/2, -1),
                             (np.pi, 1), (3*np.pi/2, -1)]:
                dx = sgn*0.18*np.cos(ang)
                dy = sgn*0.18*np.sin(ang)
                ax.annotate('', xy=(r_eq*np.cos(ang)+dx, r_eq*np.sin(ang)+dy),
                            xytext=(r_eq*np.cos(ang), r_eq*np.sin(ang)),
                            arrowprops=dict(arrowstyle='->', color=C_RED,
                                            lw=0.7))

        elif i == 2:
            # n=3: trefoil
            r_eq = 1.0
            amp = 0.22
            r_def1 = r_eq + amp * np.cos(3*theta)
            r_def2 = r_eq - amp * np.cos(3*theta)
            ax.plot(r_eq * np.cos(theta), r_eq * np.sin(theta),
                    'k-', lw=1.0)
            ax.plot(r_def1 * np.cos(theta), r_def1 * np.sin(theta),
                    '--', color=C_RED, lw=1.0)
            ax.plot(r_def2 * np.cos(theta), r_def2 * np.sin(theta),
                    '--', color=C_BLUE, lw=1.0)
            for ang_deg in [0, 60, 120, 180, 240, 300]:
                ang = np.radians(ang_deg)
                sgn = 1 if (ang_deg % 120 == 0) else -1
                dx = sgn*0.16*np.cos(ang)
                dy = sgn*0.16*np.sin(ang)
                ax.annotate('', xy=(r_eq*np.cos(ang)+dx, r_eq*np.sin(ang)+dy),
                            xytext=(r_eq*np.cos(ang), r_eq*np.sin(ang)),
                            arrowprops=dict(arrowstyle='->', color=C_RED,
                                            lw=0.7))

        ax.text(0, -1.5, mode_labels[i], fontsize=8, ha='center', va='top')

    # Legend
    leg_elements = [
        Line2D([0], [0], color='k', lw=1.0, label='Equilibrium'),
        Line2D([0], [0], color=C_RED, lw=1.0, ls='--', label='Phase A'),
        Line2D([0], [0], color=C_BLUE, lw=1.0, ls='--', label='Phase B'),
    ]
    fig.legend(handles=leg_elements, loc='upper right', ncol=3,
               frameon=True, fontsize=7, bbox_to_anchor=(0.98, 0.99))
    fig.subplots_adjust(wspace=0.05)
    _save(fig, 'fig_mode_shapes')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 3: Frequency vs E (key parametric result)
# ═══════════════════════════════════════════════════════════════════════
def fig_frequency_vs_E():
    fig, ax = plt.subplots(figsize=(SINGLE_COL, 2.8))

    E_range = np.logspace(-2, 1, 200)  # 0.01 to 10 MPa

    for n, color, marker in [(2, C_BLUE, 'o'), (3, C_ORANGE, 's'),
                              (4, C_GREEN, '^')]:
        freqs = []
        for E_MPa in E_range:
            model = AbdominalModelV2(E=E_MPa*1e6, a=0.18, b=0.18, c=0.12)
            f = flexural_mode_frequencies_v2(model, n_max=n)
            freqs.append(f[n])
        ax.loglog(E_range, freqs, color=color, label=f'$n = {n}$')
        # Markers at selected points
        idx = np.array([20, 60, 100, 140, 180])
        idx = idx[idx < len(E_range)]
        ax.plot(E_range[idx], np.array(freqs)[idx], marker,
                color=color, markersize=3.5, zorder=5)

    # Shade ISO 2631 band (4-8 Hz)
    ax.axhspan(4, 8, color=C_CYAN, alpha=0.12, zorder=0)
    ax.text(0.012, 5.8, 'ISO 2631\n(4–8 Hz)', fontsize=6.5,
            color=C_CYAN, alpha=0.85, va='center')

    # Mark relaxed and tensed muscle regions
    ax.axvspan(0.05, 0.2, ymin=0, ymax=1, color=C_GREEN, alpha=0.07, zorder=0)
    ax.axvspan(5, 10, ymin=0, ymax=1, color=C_RED, alpha=0.07, zorder=0)
    ax.text(0.1, 1.4, 'Relaxed', fontsize=6.5, ha='center', color=C_GREEN,
            fontweight='bold', rotation=0)
    ax.text(7, 100, 'Tensed', fontsize=6.5, ha='center', color=C_RED,
            fontweight='bold', rotation=0)

    ax.set_xlabel("Young's modulus $E$ (MPa)")
    ax.set_ylabel('Frequency $f_n$ (Hz)')
    ax.set_xlim(0.01, 10)
    ax.set_ylim(1, 200)
    ax.legend(loc='upper left', frameon=True)
    fig.tight_layout()
    _save(fig, 'fig_frequency_vs_E')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 4: Parametric Sensitivity (2×2)
# ═══════════════════════════════════════════════════════════════════════
def fig_parametric_sensitivity():
    fig, axes = plt.subplots(2, 2, figsize=(DOUBLE_COL, 4.5))

    base = dict(E=0.1e6, a=0.18, b=0.18, c=0.12, h=0.010, P_iap=1000.0)

    def _setup_sens_ax(ax, label):
        """Common setup for sensitivity subplots."""
        ax.axhspan(4, 8, color=C_CYAN, alpha=0.08, zorder=0)
        ax.set_ylim(2, 10)
        ax.set_ylabel('$f_2$ (Hz)')
        ax.text(0.03, 0.95, label, transform=ax.transAxes, fontsize=9,
                fontweight='bold', va='top')
        # Light ISO label
        ax.text(0.97, 0.92, 'ISO\n4–8 Hz', transform=ax.transAxes,
                fontsize=5.5, color=C_CYAN, alpha=0.7, ha='right', va='top')

    # (a) Semi-major axis a
    ax = axes[0, 0]
    a_vals = np.linspace(0.12, 0.25, 50)
    f2_a = []
    for a_val in a_vals:
        m = AbdominalModelV2(**{**base, 'a': a_val, 'b': a_val, 'c': a_val*0.67})
        f2_a.append(flexural_mode_frequencies_v2(m, n_max=2)[2])
    ax.plot(a_vals*100, f2_a, color=C_BLUE, lw=1.5)
    ax.set_xlabel('Semi-major axis $a$ (cm)')
    _setup_sens_ax(ax, '(a)')

    # (b) Aspect ratio c/a
    ax = axes[0, 1]
    cr_vals = np.linspace(0.3, 1.0, 50)
    f2_cr = []
    for cr in cr_vals:
        m = AbdominalModelV2(**{**base, 'c': base['a']*cr})
        f2_cr.append(flexural_mode_frequencies_v2(m, n_max=2)[2])
    ax.plot(cr_vals, f2_cr, color=C_ORANGE, lw=1.5)
    ax.set_xlabel('Aspect ratio $c/a$')
    _setup_sens_ax(ax, '(b)')

    # (c) Wall thickness h
    ax = axes[1, 0]
    h_vals = np.linspace(0.002, 0.025, 50)
    f2_h = []
    for h_val in h_vals:
        m = AbdominalModelV2(**{**base, 'h': h_val})
        f2_h.append(flexural_mode_frequencies_v2(m, n_max=2)[2])
    ax.plot(h_vals*1000, f2_h, color=C_GREEN, lw=1.5)
    ax.set_xlabel('Wall thickness $h$ (mm)')
    _setup_sens_ax(ax, '(c)')

    # (d) Intra-abdominal pressure P_iap
    ax = axes[1, 1]
    p_vals = np.linspace(0, 5000, 50)  # 0 to ~37 mmHg
    f2_p = []
    for p_val in p_vals:
        m = AbdominalModelV2(**{**base, 'P_iap': p_val})
        f2_p.append(flexural_mode_frequencies_v2(m, n_max=2)[2])
    ax.plot(p_vals/133.322, f2_p, color=C_PURPLE, lw=1.5)
    ax.set_xlabel(r'Intra-abdominal pressure $P_\mathrm{iap}$ (mmHg)')
    _setup_sens_ax(ax, '(d)')

    fig.tight_layout()
    _save(fig, 'fig_parametric_sensitivity')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 5: Coupling Comparison (the key novel figure)
# ═══════════════════════════════════════════════════════════════════════
def fig_coupling_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE_COL, 3.0))

    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]
    R = model.equivalent_sphere_radius

    # --- Left panel: Displacement vs frequency ---
    freqs = np.linspace(1, 20, 200)

    # Airborne at 120 dB
    disp_air = []
    for f in freqs:
        r = flexural_mode_pressure_response(f, 120.0, 2, model)
        disp_air.append(r['displacement_um'])
    disp_air = np.array(disp_air)

    # Mechanical at 0.5 m/s²
    disp_mech = []
    for f in freqs:
        exp = WBVExposure(acceleration_rms_ms2=0.5, frequency_hz=f)
        r = mechanical_excitation_response(exp, model, mode_n=2,
                                           use_empirical=False)
        disp_mech.append(r['relative_displacement_um'])
    disp_mech = np.array(disp_mech)

    ax1.semilogy(freqs, disp_mech, color=C_PURPLE, lw=1.5,
                 label='WBV (0.5 m/s²)')
    ax1.semilogy(freqs, np.maximum(disp_air, 1e-12), color=C_ORANGE, lw=1.5,
                 label='Airborne (120 dB)')

    # PIEZO threshold
    ax1.axhline(0.5, color=C_RED, ls=':', lw=0.8, zorder=5)
    ax1.text(19.5, 0.35, 'PIEZO threshold', fontsize=5.5, color=C_RED,
             ha='right', va='top')

    # ISO band
    ax1.axvspan(4, 8, color=C_CYAN, alpha=0.12, zorder=0)

    # Gap annotation — draw a vertical arrow between curves at resonance
    idx_peak = np.argmin(np.abs(freqs - f2))
    if idx_peak > 0 and disp_mech[idx_peak] > 0 and disp_air[idx_peak] > 0:
        ratio = disp_mech[idx_peak] / disp_air[idx_peak]
        y_mid = np.sqrt(disp_mech[idx_peak] * disp_air[idx_peak])
        ax1.annotate('', xy=(f2, disp_mech[idx_peak]),
                     xytext=(f2, disp_air[idx_peak]),
                     arrowprops=dict(arrowstyle='<->', color=C_GRAY, lw=0.8))
        ax1.text(f2 + 0.6, y_mid, f'{ratio:.0f}×',
                 fontsize=7, color=C_GRAY, va='center', fontweight='bold')

    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Displacement (μm)')
    ax1.set_xlim(1, 20)
    ax1.set_ylim(1e-3, 2e4)
    ax1.legend(loc='lower left', fontsize=7, frameon=True)
    ax1.text(0.03, 0.95, '(a)', transform=ax1.transAxes, fontsize=9,
             fontweight='bold', va='top')

    # --- Right panel: Bar chart of 4 pathways at resonance ---
    # 1. WBV at 0.5 m/s² at resonance
    exp_wbv = WBVExposure(acceleration_rms_ms2=0.5, frequency_hz=f2)
    r_wbv = mechanical_excitation_response(exp_wbv, model, mode_n=2)
    xi_wbv = r_wbv['relative_displacement_um']

    # 2. Gas pocket (R=3cm, 120 dB at resonance)
    pocket = GasPocket(radius_cm=3.0)
    r_gas = acoustic_response_of_gas_pocket(pocket, spl_db=120.0, freq_hz=f2)
    xi_gas = r_gas['wall_displacement_um']

    # 3. Orifice coupling (estimate: acoustic particle displacement in ear canal)
    # At 120 dB (20 Pa), particle displacement in air:
    # xi = p / (rho * c * omega)
    p_120 = 20.0  # Pa at 120 dB
    omega_f2 = 2 * np.pi * f2
    xi_orifice = p_120 / (1.225 * 343.0 * omega_f2) * 1e6  # μm

    # 4. Whole-cavity airborne (our model)
    r_air = flexural_mode_pressure_response(f2, 120.0, 2, model)
    xi_air = r_air['displacement_um']

    pathways = ['WBV\n(0.5 m/s²)', 'Gas\npocket', 'Orifice\ncoupling',
                'Whole-cavity\nairborne']
    values = [xi_wbv, xi_gas, xi_orifice, xi_air]
    colors_bar = [C_PURPLE, C_GREEN, C_ORANGE, C_BLUE]

    bars = ax2.bar(pathways, values, color=colors_bar, edgecolor='k',
                   linewidth=0.5, width=0.65, zorder=3)
    ax2.set_yscale('log')
    ax2.set_ylabel('Displacement at resonance (μm)')

    # PIEZO threshold line
    ax2.axhline(0.5, color=C_RED, ls=':', lw=0.8, zorder=5)
    ax2.text(0.5, 0.7, 'PIEZO threshold', fontsize=6, color=C_RED,
             ha='center', va='bottom', transform=ax2.get_xaxis_transform())

    # Value labels on bars — place inside tall bars, above short ones
    for bar, val in zip(bars, values):
        xc = bar.get_x() + bar.get_width() / 2
        if val > 100:
            # Tall bar: place label inside near top
            ax2.text(xc, val * 0.4, f'{val:.0f}', ha='center', va='center',
                     fontsize=6.5, fontweight='bold', color='white')
        elif val > 0.01:
            ax2.text(xc, val * 1.6, f'{val:.2g}', ha='center', va='bottom',
                     fontsize=6.5)
        else:
            ax2.text(xc, val * 3, f'{val:.2g}', ha='center', va='bottom',
                     fontsize=6.5)

    ax2.set_ylim(1e-2, 2e4)
    ax2.text(0.03, 0.95, '(b)', transform=ax2.transAxes, fontsize=9,
             fontweight='bold', va='top')

    fig.tight_layout()
    _save(fig, 'fig_coupling_comparison')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 6: Energy Budget
# ═══════════════════════════════════════════════════════════════════════
def fig_energy_budget():
    fig, ax = plt.subplots(figsize=(SINGLE_COL, 3.2))

    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    R = model.equivalent_sphere_radius
    f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]
    omega = 2 * np.pi * f2

    spl = 120.0
    p_ref = 20e-6
    p_inc = p_ref * 10**(spl / 20)
    I_inc = p_inc**2 / (2 * 1.225 * 343.0)

    # Geometric intercept
    P_intercept = I_inc * np.pi * R**2

    # Reflection (impedance mismatch)
    Z_air = 1.225 * 343.0
    Z_tissue = 1040.0 * 1540.0
    R_coeff = ((Z_tissue - Z_air) / (Z_tissue + Z_air))**2
    T_coeff = 1 - R_coeff
    P_reflected = P_intercept * R_coeff
    P_transmitted = P_intercept * T_coeff

    # Scattering / (ka)^n coupling loss
    ka = omega * R / 343.0
    coupling = ka**4  # (ka)^{2n} for n=2 energy coupling
    P_scattered = P_transmitted * (1 - coupling)
    P_coupled = P_transmitted * coupling

    # Absorption cross-section (self-consistent)
    acs = absorption_cross_section(model, mode_n=2)
    P_absorbed = acs['sigma_abs_m2'] * I_inc
    efficiency = acs['efficiency']

    # Radiation
    rd = radiation_damping_flexural(model, mode_n=2, medium='air')
    # P_radiated ~ P_absorbed * (zeta_rad / zeta_total)
    P_radiated = P_absorbed * (rd['zeta_rad'] / (rd['zeta_rad'] + model.damping_ratio))
    P_dissipated = P_absorbed - P_radiated

    # Build the waterfall/log bar chart
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
        P_intercept,
        P_reflected,
        P_transmitted,
        P_scattered,
        P_coupled,
        P_absorbed,
        P_dissipated,
        P_radiated,
    ]
    colors_e = [
        C_BLUE, C_GRAY, C_ORANGE, C_GRAY,
        C_GREEN, C_PURPLE, C_RED, C_CYAN,
    ]

    # Ensure no zeros for log scale
    values = [max(v, 1e-30) for v in values]

    bars = ax.barh(range(len(labels)), values, color=colors_e,
                   edgecolor='k', linewidth=0.4, height=0.6, zorder=3)
    ax.set_xscale('log')
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel('Power (W)')

    # Annotate with orders of magnitude
    for i, (bar, val) in enumerate(zip(bars, values)):
        if val > 1e-24:
            exp = int(np.floor(np.log10(val)))
            mantissa = val / 10**exp
            if abs(mantissa - 1.0) < 0.05:
                txt = f'$10^{{{exp}}}$'
            else:
                txt = f'{mantissa:.1f}×$10^{{{exp}}}$'
            ax.text(val * 2, i, txt, va='center', fontsize=6)
        else:
            # Extremely small value — label at a visible position
            ax.text(1e-21, i, r'$\approx 0$', va='center', fontsize=6,
                    color=C_GRAY)

    # Efficiency annotation
    eff_str = f'Absorption efficiency: {efficiency:.1e}'
    ax.text(0.95, 0.02, eff_str, transform=ax.transAxes, fontsize=7,
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', fc='lightyellow', ec='gray'))

    ax.set_xlim(1e-22, 1e-2)
    fig.tight_layout()
    _save(fig, 'fig_energy_budget')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 7: ISO 2631 Validation
# ═══════════════════════════════════════════════════════════════════════
def fig_iso2631_validation():
    fig, ax = plt.subplots(figsize=(SINGLE_COL, 2.8))

    # Published ISO 2631 transmissibility data
    iso_freq = ISO_2631_TRANSMISSIBILITY[:, 0]
    iso_T = ISO_2631_TRANSMISSIBILITY[:, 1]

    # Plot empirical data
    ax.plot(iso_freq, iso_T, 'o-', color=C_BLUE, markersize=4, lw=1.2,
            label='ISO 2631 (empirical)', zorder=5)

    # Theoretical T_abs curve from our model
    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]
    zeta = model.damping_ratio

    f_theory = np.linspace(1, 20, 200)
    T_abs = []
    for f in f_theory:
        omega = 2 * np.pi * f
        omega_n = 2 * np.pi * f2
        r = omega / omega_n
        # Absolute transmissibility
        T = np.sqrt((1 + (2*zeta*r)**2) / ((1 - r**2)**2 + (2*zeta*r)**2))
        T_abs.append(T)
    T_abs = np.array(T_abs)

    ax.plot(f_theory, T_abs, '-', color=C_RED, lw=1.2,
            label=f'Model ($f_2$={f2:.1f} Hz, $\\zeta$={zeta:.2f})')

    # Additional published data points (from iso2631_comparison)
    comp = iso2631_comparison()
    markers = {'Kitazaki_Griffin_1998_seated_z': ('D', C_GREEN),
               'Mansfield_2005_seated': ('s', C_ORANGE),
               'Coermann_1962': ('^', C_PURPLE)}
    for study, (mkr, clr) in markers.items():
        d = comp['iso_data'][study]
        # Plot peak as a point with horizontal error bar for range
        ax.errorbar(d['f_peak_hz'], d['T_peak'],
                    xerr=[[d['f_peak_hz'] - d['f_range_hz'][0]],
                          [d['f_range_hz'][1] - d['f_peak_hz']]],
                    fmt=mkr, color=clr, markersize=5, capsize=2, lw=0.8,
                    label=study.replace('_', ' ').replace('seated z', '(seated)'),
                    zorder=6)

    # ISO band
    ax.axvspan(4, 8, color=C_CYAN, alpha=0.10, zorder=0)

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Transmissibility')
    ax.set_xlim(1, 20)
    ax.set_ylim(0, 3.5)
    ax.legend(loc='upper right', fontsize=6, frameon=True)
    fig.tight_layout()
    _save(fig, 'fig_iso2631_validation')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 8: Multilayer Comparison
# ═══════════════════════════════════════════════════════════════════════
def fig_multilayer_comparison():
    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE_COL, 2.8))

    # Compute CLT composite properties for relaxed multilayer
    layers_r = relaxed_layers()
    props_r = compute_composite_properties(layers_r)

    # The key comparison: CLT bending stiffness D_eff (with parallel axis
    # theorem) vs homogeneous D = E_eff × h³ / 12(1-ν²).
    # To get frequencies, we create two AbdominalModelV2 instances:
    #   - "CLT": uses E_bend derived from D_eff so that D = E_bend h³/12(1-ν²)
    #   - "Homogeneous": uses E_eff (membrane-averaged)

    h_total = props_r['h_total_m']
    nu_eff = props_r['nu_eff']
    rho_eff = props_r['rho_eff']
    D_eff = props_r['D_eff']
    D_homo = props_r['D_homogeneous']
    E_eff_membrane = props_r['E_eff_Pa']
    # Back-compute E that gives D_eff with homogeneous formula
    E_CLT_bend = D_eff * 12 * (1 - nu_eff**2) / h_total**3

    model_CLT = AbdominalModelV2(
        E=E_CLT_bend, a=0.18, b=0.18, c=0.12,
        h=h_total, nu=nu_eff, rho_wall=rho_eff,
    )
    model_homo = AbdominalModelV2(
        E=E_eff_membrane, a=0.18, b=0.18, c=0.12,
        h=h_total, nu=nu_eff, rho_wall=rho_eff,
    )
    f_CLT = flexural_mode_frequencies_v2(model_CLT, n_max=2)[2]
    f_homo = flexural_mode_frequencies_v2(model_homo, n_max=2)[2]

    labels = ['Multilayer\n(CLT)', 'Homogeneous\n(avg)']
    x_pos = np.arange(len(labels))
    w = 0.55

    # (a) Frequency comparison
    ax = axes[0]
    vals = [f_CLT, f_homo]
    ax.bar(x_pos, vals, w, color=[C_BLUE, C_ORANGE], edgecolor='k',
           linewidth=0.5, zorder=3)
    ax.set_ylabel('$f_2$ (Hz)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=7)
    pct = abs(f_CLT - f_homo) / f_homo * 100
    ax.text(0.5, max(vals)*1.05,
            f'$\\Delta$ = {pct:.1f}%', fontsize=7, ha='center', va='bottom')
    for i, v in enumerate(vals):
        ax.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontsize=7)
    ax.set_ylim(0, max(vals)*1.3)
    ax.text(0.05, 0.95, '(a)', transform=ax.transAxes, fontsize=9,
            fontweight='bold', va='top')

    # (b) Effective E comparison (bending-derived vs membrane-averaged)
    ax = axes[1]
    E_CLT_MPa = E_CLT_bend / 1e6
    E_homo_MPa = E_eff_membrane / 1e6
    vals_e = [E_CLT_MPa, E_homo_MPa]
    ax.bar(x_pos, vals_e, w, color=[C_BLUE, C_ORANGE], edgecolor='k',
           linewidth=0.5, zorder=3)
    ax.set_ylabel('Effective $E$ (MPa)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=7)
    for i, v in enumerate(vals_e):
        ax.text(i, v + max(vals_e)*0.02, f'{v:.4f}', ha='center',
                va='bottom', fontsize=7)
    ax.set_ylim(0, max(vals_e)*1.25)
    ax.text(0.05, 0.95, '(b)', transform=ax.transAxes, fontsize=9,
            fontweight='bold', va='top')

    # (c) Bending stiffness D comparison (the real difference)
    ax = axes[2]
    vals_d = [D_eff * 1e3, D_homo * 1e3]  # convert to mN·m
    ax.bar(x_pos, vals_d, w, color=[C_BLUE, C_ORANGE], edgecolor='k',
           linewidth=0.5, zorder=3)
    ax.set_ylabel('Bending stiffness $D$ (mN·m)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=7)
    D_pct = abs(D_eff - D_homo) / D_homo * 100
    ax.text(0.5, max(vals_d)*1.05,
            f'$\\Delta$ = {D_pct:.0f}%', fontsize=7, ha='center', va='bottom')
    for i, v in enumerate(vals_d):
        ax.text(i, v + max(vals_d)*0.02, f'{v:.1f}', ha='center',
                va='bottom', fontsize=7)
    ax.set_ylim(0, max(vals_d)*1.3)
    ax.text(0.05, 0.95, '(c)', transform=ax.transAxes, fontsize=9,
            fontweight='bold', va='top')

    fig.tight_layout()
    _save(fig, 'fig_multilayer_comparison')


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print()
    print("=" * 60)
    print("  Generating JSV publication figures")
    print("=" * 60)
    print()

    generators = [
        ('Fig 1', 'Geometry schematic',    fig_geometry_schematic),
        ('Fig 2', 'Mode shapes',           fig_mode_shapes),
        ('Fig 3', 'Frequency vs E',        fig_frequency_vs_E),
        ('Fig 4', 'Parametric sensitivity', fig_parametric_sensitivity),
        ('Fig 5', 'Coupling comparison',    fig_coupling_comparison),
        ('Fig 6', 'Energy budget',          fig_energy_budget),
        ('Fig 7', 'ISO 2631 validation',    fig_iso2631_validation),
        ('Fig 8', 'Multilayer comparison',  fig_multilayer_comparison),
    ]

    generated = []
    for num, desc, func in generators:
        print(f"  [{num}] {desc}...")
        try:
            func()
            generated.append((num, desc, 'OK'))
        except Exception as e:
            print(f"    ✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            generated.append((num, desc, f'FAILED: {e}'))

    print()
    print("=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    for num, desc, status in generated:
        icon = '✓' if status == 'OK' else '✗'
        print(f"  {icon} {num}: {desc} — {status}")
    print()
    print(f"  Output directory: {os.path.abspath(FIG_DIR)}")
    print(f"  Total: {sum(1 for _,_,s in generated if s=='OK')}/{len(generated)} succeeded")
    print()
