"""Forward-inverse adequacy gap — twin-axis figure for Paper 10.

Computes forward error ||F_oblate - F_sphere||/||F_oblate|| and condition
numbers κ_oblate, κ_sphere across eccentricity, then generates a single
twin-axis plot showing forward error (small) vs condition number (huge).

Output:
    papers/paper10-capstone/figures/fig_forward_inverse_gap.{pdf,png}
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# ── Path setup ──────────────────────────────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))

from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)
from analytical.oblate_spheroid_ritz import (
    oblate_ritz_frequencies,
    sphere_approx_frequencies,
)
from analytical.kac_identifiability import (
    CANONICAL_ABDOMEN,
    compute_jacobian,
    jacobian_condition_number,
)

# ── Style ───────────────────────────────────────────────────────────────
CB_BLUE   = '#4477AA'
CB_RED    = '#EE6677'
CB_GREEN  = '#228833'

plt.rcParams.update({
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
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'lines.linewidth': 1.8,
    'lines.markersize': 5,
})

SINGLE_COL = 84 / 25.4   # 3.31 in
FIG_DIR = os.path.join(ROOT, 'papers', 'paper10-capstone', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# ── Canonical parameters ────────────────────────────────────────────────
a_can, c_can = 0.18, 0.12
E_can = 0.1e6
h_can, nu_can = 0.01, 0.45
rho_w_can, rho_f_can = 1100.0, 1020.0
K_f_can, P_iap_can = 2.2e9, 1000.0
eta_can = 0.25
MODES = (2, 3, 4, 5, 6)
eps_can = np.sqrt(1.0 - (c_can / a_can) ** 2)


def sweep_eccentricity():
    """Compute forward error and condition numbers vs eccentricity."""
    aspect_ratios = np.linspace(0.50, 0.95, 25)
    n = len(aspect_ratios)
    eps = np.array([np.sqrt(1 - ar**2) for ar in aspect_ratios])
    fwd_err = np.full(n, np.nan)
    kappa_ritz = np.full(n, np.nan)
    kappa_sphere = np.full(n, np.nan)

    for i, ar in enumerate(aspect_ratios):
        c_val = a_can * ar
        p = dict(CANONICAL_ABDOMEN, a=a_can, c=c_val)
        try:
            fr = oblate_ritz_frequencies(a_can, c_val, h_can, E_can, nu_can,
                                          rho_w_can, rho_f_can, P_iap_can,
                                          n_target=MODES)
            ms = AbdominalModelV2(a=a_can, b=a_can, c=c_val, h=h_can,
                                   E=E_can, nu=nu_can, rho_wall=rho_w_can,
                                   rho_fluid=rho_f_can, K_fluid=K_f_can,
                                   P_iap=P_iap_can, loss_tangent=eta_can)
            fs = sphere_approx_frequencies(ms, n_modes=MODES)
            f_r = np.array([fr[n] for n in MODES])
            f_s = np.array([fs[n] for n in MODES])
            fwd_err[i] = np.linalg.norm(f_s - f_r) / np.linalg.norm(f_r)
        except Exception:
            pass
        try:
            kappa_ritz[i] = jacobian_condition_number(
                p, model='ritz', modes=MODES)
        except Exception:
            pass
        try:
            kappa_sphere[i] = jacobian_condition_number(
                p, model='sphere', modes=MODES)
        except Exception:
            pass

    return eps, fwd_err, kappa_ritz, kappa_sphere


def print_canonical_values():
    """Print key numbers at the canonical operating point."""
    p = dict(CANONICAL_ABDOMEN)
    fr = oblate_ritz_frequencies(a_can, c_can, h_can, E_can, nu_can,
                                  rho_w_can, rho_f_can, P_iap_can,
                                  n_target=MODES)
    ms = AbdominalModelV2(a=a_can, b=a_can, c=c_can, h=h_can,
                           E=E_can, nu=nu_can, rho_wall=rho_w_can,
                           rho_fluid=rho_f_can, K_fluid=K_f_can,
                           P_iap=P_iap_can, loss_tangent=eta_can)
    fs = sphere_approx_frequencies(ms, n_modes=MODES)
    f_r = np.array([fr[n] for n in MODES])
    f_s = np.array([fs[n] for n in MODES])
    E_fwd = np.linalg.norm(f_s - f_r) / np.linalg.norm(f_r)

    kr = jacobian_condition_number(p, model='ritz', modes=MODES)
    ks = jacobian_condition_number(p, model='sphere', modes=MODES)

    J_ritz = compute_jacobian(p, model='ritz', modes=MODES, scaled=True)
    J_sph = compute_jacobian(p, model='sphere', modes=MODES, scaled=True)
    sv_r = np.linalg.svd(J_ritz, compute_uv=False)
    sv_s = np.linalg.svd(J_sph, compute_uv=False)

    # Kernel-direction check: v_null = (1, -2, 0)/√5 in scaled space
    v_null = np.array([1.0, -2.0, 0.0]) / np.sqrt(5.0)
    psi_ritz = np.linalg.norm(J_ritz @ v_null)
    psi_sphere = np.linalg.norm(J_sph @ v_null)

    print('=' * 60)
    print('  Forward-Inverse Adequacy Gap — Canonical Point')
    print('=' * 60)
    print(f'  ε = {eps_can:.4f}  (c/a = {c_can/a_can:.3f})')
    print()
    print(f'  Forward error ℰ_fwd = {E_fwd:.4f}  ({E_fwd*100:.2f}%)')
    print()
    print(f'  Oblate Ritz:  κ = {kr:.1f}')
    print(f'    σ = [{", ".join(f"{s:.4f}" for s in sv_r)}]')
    print(f'    ‖J̃·v_null‖ = {psi_ritz:.4f}  (full model sees null dir)')
    print()
    print(f'  Equiv sphere: κ = {ks:.2e}')
    print(f'    σ = [{", ".join(f"{s:.2e}" for s in sv_s)}]')
    print(f'    ‖J̃·v_null‖ = {psi_sphere:.2e}  (reduced model blind)')
    print()
    print(f'  Gap ratio κ_sphere / κ_ritz = {ks/kr:.2e}')
    print(f'  Column proportionality J[:,a]/J[:,c] = '
          f'{J_sph[:,0]/J_sph[:,1]}')
    print('=' * 60)


def generate_figure(eps, fwd_err, kappa_ritz, kappa_sphere):
    """Twin-axis figure: forward error (left) + condition numbers (right)."""
    fig, ax_fwd = plt.subplots(figsize=(SINGLE_COL * 1.25, SINGLE_COL * 0.9))
    ax_kap = ax_fwd.twinx()

    valid = np.isfinite(fwd_err) & np.isfinite(kappa_ritz)
    mask_s = np.isfinite(kappa_sphere)

    # Forward error — left axis (linear)
    l1, = ax_fwd.plot(eps[valid], fwd_err[valid] * 100,
                       color=CB_BLUE, linewidth=2.0, zorder=5,
                       label=r'$\mathcal{E}_\mathrm{fwd}$ (%)')
    ax_fwd.axhline(10, color=CB_BLUE, ls=':', lw=0.6, alpha=0.5)
    ax_fwd.set_ylabel(r'Forward error $\mathcal{E}_\mathrm{fwd}$ (%)',
                       color=CB_BLUE)
    ax_fwd.tick_params(axis='y', labelcolor=CB_BLUE)
    ax_fwd.set_ylim(0, 32)
    ax_fwd.set_xlabel(r'Eccentricity $\varepsilon$')
    ax_fwd.set_xlim(0.30, 0.88)

    # Condition numbers — right axis (log)
    l2, = ax_kap.semilogy(eps[valid], kappa_ritz[valid],
                           color=CB_GREEN, marker='o', markersize=3,
                           markevery=3, linewidth=1.5, zorder=4,
                           label=r'$\kappa_\mathrm{oblate}$')
    l3, = ax_kap.semilogy(eps[mask_s], kappa_sphere[mask_s],
                           color=CB_RED, marker='s', markersize=3,
                           markevery=3, linewidth=1.5, zorder=4,
                           label=r'$\kappa_\mathrm{sphere}$')

    # Shade the gap
    eps_both = eps[valid & mask_s]
    kr_both = kappa_ritz[valid & mask_s]
    ks_both = kappa_sphere[valid & mask_s]
    ax_kap.fill_between(eps_both, kr_both, ks_both,
                         alpha=0.10, color=CB_RED, zorder=1)

    ax_kap.set_ylabel(r'Condition number $\kappa$')
    ax_kap.set_ylim(10, 5e11)

    # Canonical point
    ax_fwd.axvline(eps_can, color='grey', ls='--', lw=0.7, zorder=2)
    ax_fwd.text(eps_can - 0.02, 30, r'canonical $\varepsilon$',
                fontsize=7, color='grey', ha='right', va='top')

    # Annotation: gap ratio at canonical point
    idx_can = np.argmin(np.abs(eps - eps_can))
    if np.isfinite(kappa_ritz[idx_can]) and np.isfinite(kappa_sphere[idx_can]):
        gap = kappa_sphere[idx_can] / kappa_ritz[idx_can]
        ax_kap.annotate(
            rf'$\kappa_\mathrm{{sphere}}/\kappa_\mathrm{{oblate}}'
            rf'\approx {gap:.0e}$',
            xy=(eps_can, np.sqrt(kappa_ritz[idx_can] * kappa_sphere[idx_can])),
            xytext=(0.45, 3e6),
            fontsize=7, color='grey',
            arrowprops=dict(arrowstyle='->', color='grey', lw=0.5),
        )

    # Combined legend
    lines = [l1, l2, l3]
    ax_fwd.legend(lines, [l.get_label() for l in lines],
                   loc='upper left', fontsize=7, framealpha=0.9)

    # Remove grid from twin axis; keep on primary
    ax_fwd.grid(True, color='#cccccc', ls='--', lw=0.4)
    ax_kap.grid(False)

    fig.tight_layout()
    for ext in ['pdf', 'png']:
        path = os.path.join(FIG_DIR, f'fig_forward_inverse_gap.{ext}')
        fig.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    sz = os.path.getsize(os.path.join(FIG_DIR, 'fig_forward_inverse_gap.png'))
    print(f'  Saved: fig_forward_inverse_gap (.png {sz/1024:.0f} KB + .pdf)')


if __name__ == '__main__':
    print_canonical_values()
    eps, fwd_err, kappa_ritz, kappa_sphere = sweep_eccentricity()
    generate_figure(eps, fwd_err, kappa_ritz, kappa_sphere)
