"""
Generate all 6 publication-quality figures for Paper 7 (watermelon ripeness).

Output: projects/watermelon-ripeness/figures/fig_*.{png,pdf}
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np
import sys, os, warnings

ROOT = os.path.abspath('.')
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))

from analytical.watermelon_model import (
    watermelon_canonical_params, predict_tap_tone, invert_frequency_to_modulus,
    ripeness_from_modulus, universal_ripeness_curve, parametric_ripening_sweep,
    sobol_sensitivity_watermelon, multi_cultivar_comparison,
    _RIPENESS_STAGES, _CULTIVAR_DB,
)
from analytical.natural_frequency_v2 import AbdominalModelV2, flexural_mode_frequencies_v2

# ═══════════════════════════════════════════════════════════════════════════
#  Style setup (JSV-compatible)
# ═══════════════════════════════════════════════════════════════════════════
COLORS = plt.cm.tab10.colors
C_BLUE, C_ORANGE, C_GREEN, C_RED, C_PURPLE = COLORS[:5]
C_BROWN, C_PINK, C_GRAY, C_OLIVE, C_CYAN = COLORS[5:10]

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

SINGLE_COL = 84 / 25.4   # 3.31 inches
DOUBLE_COL = 174 / 25.4   # 6.85 inches

FIG_DIR = os.path.join(ROOT, 'papers', 'paper7-watermelon', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

def _save(fig, name):
    """Save figure as PNG (300 dpi) and PDF (vector)."""
    png = os.path.join(FIG_DIR, name + '.png')
    pdf = os.path.join(FIG_DIR, name + '.pdf')
    fig.savefig(png, dpi=300, bbox_inches='tight', pad_inches=0.05)
    fig.savefig(pdf, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    print('  Saved: %s (.png + .pdf)' % name)


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 1: f2 vs E_rind (exact linearity)
# ═══════════════════════════════════════════════════════════════════════════
def fig_frequency_vs_E():
    print('\n=== Figure 1: f2 vs E_rind ===')

    # Sweep E from 5 to 500 MPa
    E_MPa = np.logspace(np.log10(5), np.log10(500), 80)
    f2_vals = np.zeros_like(E_MPa)
    base = watermelon_canonical_params('ripe')

    for i, E in enumerate(E_MPa):
        p = dict(base)
        p['E'] = E * 1e6
        res = predict_tap_tone(p, mode=2)
        f2_vals[i] = res['f_n']

    # The four ripeness stages
    stages = ['overripe', 'ripe', 'turning', 'unripe']
    stage_E = []
    stage_f2 = []
    stage_colors = [CB_RED, CB_GREEN, CB_YELLOW, CB_BLUE]
    stage_markers = ['v', 'o', 's', '^']

    for stage in stages:
        p = watermelon_canonical_params(stage)
        res = predict_tap_tone(p, mode=2)
        stage_E.append(p['E'] / 1e6)
        stage_f2.append(res['f_n'])

    # Fit: f2 = sqrt(C * E_MPa)
    # From the model, f2^2 should be linear in E
    # Fit C from the sweep
    f2_sq = f2_vals**2
    C_fit = np.polyfit(E_MPa, f2_sq, 1)
    print('  Linear fit: f2^2 = %.2f * E_MPa + %.2f' % (C_fit[0], C_fit[1]))
    f2_fit = np.sqrt(C_fit[0] * E_MPa + C_fit[1])

    fig, ax1 = plt.subplots(figsize=(DOUBLE_COL, DOUBLE_COL * 0.55))

    # Shaded bands for literature frequency ranges
    ax1.axhspan(80, 160, alpha=0.12, color=CB_GREEN, label='Ripe range (literature)')
    ax1.axhspan(140, 250, alpha=0.10, color=CB_BLUE, label='Unripe range (literature)')

    # Model sweep
    ax1.plot(E_MPa, f2_vals, '-', color='0.3', lw=1.8, label='Shell model $f_2$', zorder=4)
    ax1.plot(E_MPa, f2_fit, '--', color=CB_PURPLE, lw=1.2,
             label=r'Fit: $f_2 = \sqrt{%.1f\, E_\mathrm{MPa} + %.1f}$' % (C_fit[0], C_fit[1]),
             zorder=3)

    # Ripeness markers
    for j, stage in enumerate(stages):
        ax1.scatter(stage_E[j], stage_f2[j], marker=stage_markers[j],
                    c=stage_colors[j], s=100, edgecolors='k', linewidth=0.8,
                    zorder=5, label=stage.capitalize())

    ax1.set_xscale('log')
    ax1.set_xlabel(r'Rind elastic modulus $E_\mathrm{rind}$ [MPa]')
    ax1.set_ylabel(r'Tap-tone frequency $f_2$ [Hz]')
    ax1.set_xlim(5, 500)
    ax1.set_ylim(0, 320)

    # Secondary y-axis: f2^2 to show perfect linearity
    ax2 = ax1.twinx()
    ax2.plot(E_MPa, f2_sq, ':', color=CB_CYAN, lw=1.0, alpha=0.7, zorder=2)
    ax2.set_ylabel(r'$f_2^2$ [Hz$^2$]', color=CB_CYAN)
    ax2.tick_params(axis='y', labelcolor=CB_CYAN)

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(handles1, labels1, loc='upper left', framealpha=0.9,
               edgecolor='0.7', fontsize=7.5)

    ax1.set_title('')  # no title — paper uses caption
    fig.tight_layout()
    _save(fig, 'fig_frequency_vs_E')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 2: Ripening sweep (tap-tone trajectory)
# ═══════════════════════════════════════════════════════════════════════════
def fig_ripening_sweep():
    print('\n=== Figure 2: Ripening sweep ===')

    sweep = parametric_ripening_sweep(n_stages=40)

    E_rind = np.array([r['E_rind'] for r in sweep]) / 1e6  # MPa
    f2 = np.array([r['f2'] for r in sweep])
    Q = np.array([r['Q'] for r in sweep])
    cats = [r['category'] for r in sweep]

    cat_colors = {
        'unripe': CB_BLUE,
        'turning': CB_YELLOW,
        'ripe': CB_GREEN,
        'overripe': CB_RED,
    }

    fig, ax1 = plt.subplots(figsize=(DOUBLE_COL, DOUBLE_COL * 0.55))

    # Color each segment by category
    for i in range(len(E_rind) - 1):
        ax1.plot(E_rind[i:i+2], f2[i:i+2], '-', color=cat_colors[cats[i]], lw=2.0, zorder=3)

    # Scatter colored markers
    for cat in ['unripe', 'turning', 'ripe', 'overripe']:
        mask = np.array([c == cat for c in cats])
        ax1.scatter(E_rind[mask], f2[mask], c=cat_colors[cat], s=40,
                    edgecolors='k', linewidth=0.5, zorder=4, label=cat.capitalize())

    ax1.set_xlabel(r'Rind elastic modulus $E_\mathrm{rind}$ [MPa]')
    ax1.set_ylabel(r'Tap-tone frequency $f_2$ [Hz]')
    ax1.invert_xaxis()  # Ripening goes left (softer)

    # Arrow showing ripening direction
    ax1.annotate('', xy=(E_rind[-1], f2[-1] - 5), xytext=(E_rind[0], f2[0] + 5),
                 arrowprops=dict(arrowstyle='->', color='0.4', lw=1.5, ls='--'))
    mid_idx = len(E_rind) // 2
    ax1.text(E_rind[mid_idx] + 20, f2[mid_idx] + 15,
             r'Ripening $\longrightarrow$', fontsize=9, color='0.3', style='italic')

    # Secondary axis: Q factor
    ax2 = ax1.twinx()
    ax2.plot(E_rind, Q, ':', color=CB_GREY, lw=1.5, alpha=0.8, zorder=2)
    ax2.scatter(E_rind, Q, c=CB_GREY, s=15, alpha=0.5, zorder=2)
    ax2.set_ylabel('Quality factor $Q$', color='0.5')
    ax2.tick_params(axis='y', labelcolor='0.5')

    ax1.legend(loc='upper left', framealpha=0.9, edgecolor='0.7')
    fig.tight_layout()
    _save(fig, 'fig_ripening_sweep')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 3: Sobol sensitivity indices
# ═══════════════════════════════════════════════════════════════════════════
def fig_sobol_sensitivity():
    print('\n=== Figure 3: Sobol sensitivity ===')
    print('  Running Sobol analysis (N=1024, may take a minute)...')

    si = sobol_sensitivity_watermelon(N_base=1024)
    ST = si['ST']
    S1 = si['S1']

    # Pretty names for parameters
    pretty = {
        'E': r'$E_\mathrm{rind}$',
        'h': r'$h$ (thickness)',
        'a': r'$a$ (semi-major)',
        'c': r'$c$ (semi-minor)',
        'rho_rind': r'$\rho_\mathrm{rind}$',
        'rho_flesh': r'$\rho_\mathrm{flesh}$',
        'nu': r'$\nu$',
        'P_int': r'$P_\mathrm{int}$ (turgor)',
        'loss_tangent': r'$\eta$ (loss tan.)',
    }

    # Sort by ST descending
    sorted_params = sorted(ST.keys(), key=lambda k: ST[k], reverse=True)
    names = [pretty.get(k, k) for k in sorted_params]
    st_vals = [ST[k] for k in sorted_params]
    s1_vals = [S1[k] for k in sorted_params]

    # Color by magnitude
    cmap = plt.cm.YlOrRd
    norm = plt.Normalize(vmin=0, vmax=max(st_vals) * 1.1)
    bar_colors = [cmap(norm(v)) for v in st_vals]

    fig, ax = plt.subplots(figsize=(DOUBLE_COL, DOUBLE_COL * 0.55))

    y_pos = np.arange(len(names))

    # Total-order indices (main bars)
    bars = ax.barh(y_pos, st_vals, height=0.6, color=bar_colors,
                   edgecolor='0.3', linewidth=0.5, label=r'$S_T$ (total order)')

    # First-order indices as nested bars
    ax.barh(y_pos, s1_vals, height=0.35, color=CB_BLUE, alpha=0.6,
            edgecolor='0.3', linewidth=0.4, label=r'$S_1$ (first order)')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlabel('Sobol sensitivity index')
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.axvline(0.05, color='0.6', ls=':', lw=0.8, label='Significance threshold')

    # Annotate dominant parameter
    ax.text(st_vals[0] - 0.02, 0, '%.2f' % st_vals[0],
            va='center', ha='right', fontsize=8, fontweight='bold', color='white')

    # Paper 1 comparison annotation
    ax.annotate(r'Paper 1 abdominal: $S_T(E)=0.86$',
                xy=(0.86, -0.3), fontsize=7, color=CB_PURPLE,
                arrowprops=dict(arrowstyle='->', color=CB_PURPLE, lw=0.8),
                xytext=(0.60, -0.7))

    ax.legend(loc='lower right', framealpha=0.9, edgecolor='0.7', fontsize=7.5)
    fig.tight_layout()
    _save(fig, 'fig_sobol_sensitivity')

    # Print summary
    print('  Top sensitivities:')
    for k in sorted_params[:5]:
        print('    %s: S1=%.3f, ST=%.3f' % (k, S1[k], ST[k]))


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 4: Universal dimensionless ripeness curve
# ═══════════════════════════════════════════════════════════════════════════
def fig_universal_curve():
    print('\n=== Figure 4: Universal ripeness curve ===')

    cultivars = list(_CULTIVAR_DB.keys())
    stages = ['unripe', 'turning', 'ripe', 'overripe']
    stage_markers = ['^', 's', 'o', 'v']
    cultivar_colors = [CB_BLUE, CB_RED, CB_GREEN, CB_PURPLE]

    fig, ax = plt.subplots(figsize=(DOUBLE_COL, DOUBLE_COL * 0.55))

    all_pi = []
    all_ka = []

    for ic, cultivar in enumerate(cultivars):
        geom = _CULTIVAR_DB[cultivar]
        pis = []
        kas = []
        for ist, stage in enumerate(stages):
            p = watermelon_canonical_params(stage)
            p.update(geom)  # override geometry with cultivar
            results = universal_ripeness_curve([p])
            pi_ripe, ka = results[0]
            pis.append(pi_ripe)
            kas.append(ka)
            all_pi.append(pi_ripe)
            all_ka.append(ka)

            ax.scatter(ka, pi_ripe, marker=stage_markers[ist],
                       c=cultivar_colors[ic], s=80, edgecolors='k',
                       linewidth=0.6, zorder=5)

        # Connect stages for each cultivar
        ax.plot(kas, pis, '-', color=cultivar_colors[ic], lw=1.2, alpha=0.7, zorder=3)

    # Horizontal reference lines for ripeness thresholds
    pi_arr = np.array(all_pi)
    pi_mean = np.mean(pi_arr)
    pi_std = np.std(pi_arr)

    ax.axhspan(pi_mean - pi_std, pi_mean + pi_std, alpha=0.15, color=CB_GREY,
               label=r'$\Pi_\mathrm{ripe}$ collapse band ($\mu \pm \sigma$)')
    ax.axhline(pi_mean, color='0.5', ls='--', lw=1.0, zorder=2)

    # Cultivar legend
    cultivar_handles = [Line2D([0], [0], marker='o', color=cultivar_colors[i],
                               markersize=6, linestyle='-', lw=1.2,
                               label=cultivars[i])
                        for i in range(len(cultivars))]
    # Stage legend
    stage_handles = [Line2D([0], [0], marker=stage_markers[i], color='0.5',
                            markersize=6, linestyle='None',
                            markeredgecolor='k', markeredgewidth=0.5,
                            label=stages[i].capitalize())
                     for i in range(len(stages))]

    leg1 = ax.legend(handles=cultivar_handles, loc='upper left',
                     framealpha=0.9, edgecolor='0.7', fontsize=7, title='Cultivar')
    ax.add_artist(leg1)
    ax.legend(handles=stage_handles + [mpatches.Patch(alpha=0.15, color=CB_GREY,
              label=r'Collapse band')],
              loc='lower right', framealpha=0.9, edgecolor='0.7', fontsize=7, title='Stage')

    ax.set_xlabel(r'Helmholtz number $ka$')
    ax.set_ylabel(r'Dimensionless ripeness $\Pi_\mathrm{ripe}$')

    print('  Pi_ripe mean=%.4f, std=%.4f, CV=%.1f%%' % (pi_mean, pi_std, 100*pi_std/pi_mean))
    fig.tight_layout()
    _save(fig, 'fig_universal_curve')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 5: Inversion noise resilience
# ═══════════════════════════════════════════════════════════════════════════
def fig_inversion_noise():
    print('\n=== Figure 5: Inversion noise resilience ===')

    # True parameters: ripe watermelon
    p_true = watermelon_canonical_params('ripe')
    res_true = predict_tap_tone(p_true, mode=2)
    f2_true = res_true['f_n']
    E_true = p_true['E']

    noise_levels = [0.5, 1.0, 2.0, 5.0, 10.0]
    n_trials = 1000
    rng = np.random.default_rng(42)

    errors_pct = {}
    for noise_pct in noise_levels:
        sigma = noise_pct / 100.0 * f2_true
        f_noisy = f2_true + rng.normal(0, sigma, n_trials)
        f_noisy = np.maximum(f_noisy, 1.0)  # avoid negatives

        E_inv = np.array([
            invert_frequency_to_modulus(
                f, p_true['a'], p_true['c'], p_true['h'],
                p_true['rho_rind'], p_true['rho_flesh'],
                p_true['nu'], p_true['P_int'], n=2
            )
            for f in f_noisy
        ])

        err = (E_inv - E_true) / E_true * 100.0
        errors_pct[noise_pct] = err

    fig, ax = plt.subplots(figsize=(DOUBLE_COL, DOUBLE_COL * 0.55))

    positions = np.arange(len(noise_levels))
    vp_colors = [CB_BLUE, CB_CYAN, CB_GREEN, CB_YELLOW, CB_RED]

    # Violin plot
    parts = ax.violinplot(
        [errors_pct[n] for n in noise_levels],
        positions=positions, widths=0.7,
        showmeans=True, showmedians=True, showextrema=False
    )

    for i, body in enumerate(parts['bodies']):
        body.set_facecolor(vp_colors[i])
        body.set_edgecolor('0.3')
        body.set_alpha(0.7)
    parts['cmeans'].set_color('k')
    parts['cmeans'].set_linewidth(1.5)
    parts['cmedians'].set_color(CB_RED)
    parts['cmedians'].set_linewidth(1.0)

    # Box plot overlay for quartiles
    bp = ax.boxplot(
        [errors_pct[n] for n in noise_levels],
        positions=positions, widths=0.25,
        patch_artist=False, showfliers=False,
        medianprops=dict(color=CB_RED, lw=1.2),
        boxprops=dict(color='0.3', lw=0.8),
        whiskerprops=dict(color='0.3', lw=0.8),
        capprops=dict(color='0.3', lw=0.8),
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(['%.1f%%' % n if n < 1 else '%g%%' % n for n in noise_levels])
    ax.set_xlabel('Frequency noise level (% of $f_2$)')
    ax.set_ylabel(r'$E_\mathrm{rind}$ inversion error [%]')

    # Reference line at 0
    ax.axhline(0, color='0.5', ls='-', lw=0.5)

    # Theoretical 2x noise amplification line
    theoretical_2x = np.array(noise_levels) * 2
    ax.plot(positions, theoretical_2x, 'k--', lw=1.2, marker='D', markersize=4,
            label=r'$2\times$ amplification ($E \propto f^2$)', zorder=5)
    ax.plot(positions, -theoretical_2x, 'k--', lw=1.2, marker='D', markersize=4, zorder=5)

    # Annotate key message
    ax.annotate(
        r'$E \propto f^2 \Rightarrow$ noise amplification $\approx 2\times$',
        xy=(3, theoretical_2x[3]),
        xytext=(2.5, theoretical_2x[3] + 8),
        fontsize=7.5, color='0.2',
        arrowprops=dict(arrowstyle='->', color='0.3', lw=0.8),
    )

    ax.legend(loc='upper left', framealpha=0.9, edgecolor='0.7', fontsize=7.5)

    # Print stats
    for n in noise_levels:
        err = errors_pct[n]
        print('  Noise %.1f%%: mean_err=%.2f%%, std=%.2f%%, |max|=%.2f%%' % (
            n, np.mean(err), np.std(err), np.max(np.abs(err))))

    fig.tight_layout()
    _save(fig, 'fig_inversion_noise')


# ═══════════════════════════════════════════════════════════════════════════
#  Figure 6: Multi-cultivar comparison
# ═══════════════════════════════════════════════════════════════════════════
def fig_cultivar_comparison():
    print('\n=== Figure 6: Multi-cultivar comparison ===')

    cv = multi_cultivar_comparison()

    # Sort by frequency descending (small melons -> higher freq)
    cv_sorted = sorted(cv, key=lambda x: x['f2'], reverse=True)

    names = [c['cultivar'] for c in cv_sorted]
    f2_vals = [c['f2'] for c in cv_sorted]
    a_vals = [c['a'] * 100 for c in cv_sorted]  # cm
    c_vals = [c['c'] * 100 for c in cv_sorted]  # cm
    R_vals = [c['R_eq'] * 100 for c in cv_sorted]  # cm

    bar_colors = [CB_BLUE, CB_GREEN, CB_PURPLE, CB_RED]

    fig, ax1 = plt.subplots(figsize=(DOUBLE_COL, DOUBLE_COL * 0.5))

    x = np.arange(len(names))
    bars = ax1.bar(x, f2_vals, width=0.55, color=bar_colors,
                   edgecolor='0.3', linewidth=0.6, zorder=3)

    # Hatch patterns for greyscale
    hatches = ['///', '\\\\\\', '...', 'xxx']
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=15, ha='right', fontsize=8)
    ax1.set_ylabel(r'Tap-tone frequency $f_2$ [Hz]')
    ax1.set_ylim(0, max(f2_vals) * 1.25)

    # Annotate each bar with geometry
    for i, (name, f2, a, c_dim) in enumerate(zip(names, f2_vals, a_vals, c_vals)):
        ax1.text(i, f2 + 3, '%.1f Hz' % f2, ha='center', va='bottom',
                 fontsize=8, fontweight='bold')
        ax1.text(i, f2 * 0.5, '$a$=%.0f, $c$=%.0f cm' % (a, c_dim),
                 ha='center', va='center', fontsize=7, color='white',
                 fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.2', fc='0.3', alpha=0.7))

    # Secondary axis: equivalent radius
    ax2 = ax1.twinx()
    ax2.plot(x, R_vals, 'kD-', markersize=6, lw=1.2, zorder=5, label='$R_{eq}$ [cm]')
    ax2.set_ylabel(r'Equivalent radius $R_\mathrm{eq}$ [cm]')
    ax2.set_ylim(0, max(R_vals) * 1.6)
    ax2.legend(loc='upper right', framealpha=0.9, edgecolor='0.7', fontsize=7.5)

    # Key insight annotation
    ax1.annotate(
        'Smaller melon\n= higher $f_2$',
        xy=(0, f2_vals[0] * 1.12),
        xytext=(0.5, f2_vals[0] * 1.18),
        fontsize=7.5, ha='center', color=CB_BLUE,
        arrowprops=dict(arrowstyle='->', color=CB_BLUE, lw=0.8),
    )

    fig.tight_layout()
    _save(fig, 'fig_cultivar_comparison')


# ═══════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('Generating Paper 7 figures...')
    print('Output: %s' % FIG_DIR)

    fig_frequency_vs_E()
    fig_ripening_sweep()
    fig_sobol_sensitivity()
    fig_universal_curve()
    fig_inversion_noise()
    fig_cultivar_comparison()

    print('\n=== All 6 figures generated successfully! ===')
    print('Files in: %s' % FIG_DIR)
    for f in sorted(os.listdir(FIG_DIR)):
        fpath = os.path.join(FIG_DIR, f)
        size_kb = os.path.getsize(fpath) / 1024
        print('  %s (%.1f KB)' % (f, size_kb))
