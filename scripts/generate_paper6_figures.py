"""
Generate publication-quality figures for Paper 6: Sub-Bass Pathway Partition.

Produces four figures:
1. fig_coupling_competition.pdf — ka² coupling vs H(r) penalty vs product
2. fig_displacement_spectrum.pdf — Concert displacement vs threshold
3. fig_pathway_comparison.pdf — Airborne vs floor vs threshold bar chart
4. fig_spl_sensitivity.pdf — Frequency × SPL contour, colour = ratio-to-threshold

Usage:
    python scripts/generate_paper6_figures.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytical.sub_bass_coupling import (
    ka_parameter,
    tissue_displacement,
    perception_threshold_model,
    concert_displacement_spectrum,
    pathway_comparison,
    near_field_enhancement,
    pew_bending_resonance,
)
from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)

# Style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'lines.linewidth': 1.5,
})

OUTDIR = os.path.join(os.path.dirname(__file__), '..', 'paper6-sub-bass', 'figures')
os.makedirs(OUTDIR, exist_ok=True)

model = AbdominalModelV2()
f2 = flexural_mode_frequencies_v2(model)[2]


def fig_coupling_competition():
    """Figure 1: ka² coupling vs H(r) off-resonance penalty vs product."""
    f = np.linspace(1, 100, 500)
    ka = ka_parameter(f, model.equivalent_sphere_radius)
    ka_sq = ka ** 2

    # SDOF transfer function
    zeta = model.damping_ratio
    r = f / f2
    H = 1.0 / np.sqrt((1 - r ** 2) ** 2 + (2 * zeta * r) ** 2)
    H_norm = H / model.Q  # normalised so =1 at resonance

    product = ka_sq * H_norm

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(f, ka_sq, 'b-', label=r'$(ka)^2$ coupling')
    ax.semilogy(f, H_norm, 'r--', label=r'$H(r)/Q$ off-resonance')
    ax.semilogy(f, product, 'k-', linewidth=2, label='Product')
    ax.axvline(f2, color='gray', linestyle=':', alpha=0.5, label=f'$f_2 = {f2:.1f}$ Hz')
    ax.axvspan(20, 80, alpha=0.05, color='orange', label='Sub-bass band')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Normalised factor')
    ax.set_xlim(1, 100)
    ax.set_ylim(1e-7, 10)
    ax.legend(loc='best', framealpha=0.9)
    ax.set_title('Coupling competition: improved $ka$ vs off-resonance penalty')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_coupling_competition.pdf'))
    plt.close(fig)
    print('  [1/4] fig_coupling_competition.pdf')


def fig_displacement_spectrum():
    """Figure 2: Concert displacement vs perception threshold."""
    f = np.arange(20, 81, 1.0)

    fig, ax = plt.subplots(figsize=(6, 4))

    colours = {'edm': '#e41a1c', 'rock': '#377eb8', 'organ': '#4daf4a'}
    labels = {'edm': 'EDM', 'rock': 'Rock', 'organ': 'Pipe organ'}

    for genre in ['edm', 'rock', 'organ']:
        cd = concert_displacement_spectrum(f, genre, model)
        ax.semilogy(f, cd['xi_um'], color=colours[genre],
                    label=labels[genre])

    # Perception threshold
    thresh = perception_threshold_model(f)
    ax.semilogy(f, thresh['xi_threshold_um'], 'k--', linewidth=2,
                label='Perception threshold (ISO 2631)')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel(r'Displacement ($\mu$m)')
    ax.set_xlim(20, 80)
    ax.legend(loc='best', framealpha=0.9)
    ax.set_title('Airborne tissue displacement at concert SPLs')

    # Annotate the gap
    ax.annotate('', xy=(50, 2e-3), xytext=(50, 0.46),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
    ax.text(52, 0.03, '~2.5 orders\ngap', fontsize=8, color='gray',
            ha='left', va='center')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_displacement_spectrum.pdf'))
    plt.close(fig)
    print('  [2/4] fig_displacement_spectrum.pdf')


def fig_pathway_comparison():
    """Figure 3: Bar chart — airborne vs floor vs threshold at 40 Hz."""
    f = np.array([40.0])
    pc = pathway_comparison(f, 115.0, model)

    categories = ['Airborne\n(acoustic)', 'Floor\n(structural)', 'Perception\nthreshold']
    values = [pc['airborne_um'][0], pc['floor_um'][0], pc['threshold_um'][0]]
    colours = ['#377eb8', '#e41a1c', '#999999']

    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(categories, values, color=colours, edgecolor='black',
                  linewidth=0.5, width=0.6)

    ax.set_yscale('log')
    ax.set_ylabel(r'Displacement ($\mu$m)')
    ax.set_title('Pathway comparison at 40 Hz, 115 dB SPL')

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val * 1.5,
                f'{val:.4f}' if val < 0.01 else f'{val:.3f}',
                ha='center', va='bottom', fontsize=9)

    ax.set_ylim(1e-4, 5)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_pathway_comparison.pdf'))
    plt.close(fig)
    print('  [3/4] fig_pathway_comparison.pdf')


def fig_spl_sensitivity():
    """Figure 4: Contour — frequency × SPL, colour = log10(ratio-to-threshold)."""
    f = np.linspace(20, 80, 100)
    spl = np.linspace(90, 130, 100)
    F, SPL = np.meshgrid(f, spl)

    # Compute ratio for each (f, SPL)
    # Use vectorised approach: compute at reference SPL and scale
    ref_spl = 120.0
    result_ref = tissue_displacement(f, ref_spl, model=model, mode_n=2)
    thresh = perception_threshold_model(f)

    xi_ref = result_ref['xi_um']  # shape (len(f),)
    thresh_um = thresh['xi_threshold_um']

    # Scale for each SPL row: displacement scales linearly with pressure
    ratio = np.zeros_like(F)
    for j, s in enumerate(spl):
        p_scale = 10 ** ((s - ref_spl) / 20)
        ratio[j, :] = (xi_ref * p_scale) / thresh_um

    log_ratio = np.log10(ratio + 1e-30)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    levels = np.linspace(-5, 0, 20)
    cs = ax.contourf(F, SPL, log_ratio, levels=levels, cmap='RdYlBu_r')
    ax.contour(F, SPL, log_ratio, levels=[-2, -1, 0], colors='k',
               linewidths=[0.5, 1.0, 2.0])

    cbar = fig.colorbar(cs, ax=ax)
    cbar.set_label(r'$\log_{10}(\xi / \xi_\mathrm{thresh})$')

    # Mark typical concert levels
    ax.plot(40, 115, 'w*', markersize=12, markeredgecolor='k', label='EDM peak')
    ax.plot(63, 108, 'ws', markersize=8, markeredgecolor='k', label='Rock peak')
    ax.plot(40, 105, 'w^', markersize=8, markeredgecolor='k', label='Organ peak')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Sound Pressure Level (dB)')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.set_title('Airborne displacement / perception threshold')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_spl_sensitivity.pdf'))
    plt.close(fig)
    print('  [4/4] fig_spl_sensitivity.pdf')


if __name__ == '__main__':
    print()
    print('Generating Paper 6 figures...')
    print()
    fig_coupling_competition()
    fig_displacement_spectrum()
    fig_pathway_comparison()
    fig_spl_sensitivity()
    print()
    print(f'All figures saved to {os.path.abspath(OUTDIR)}')
    print()
