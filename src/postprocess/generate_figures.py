"""
Generate publication-quality figures for the browntone project.

Produces:
  1. Modal frequency vs material parameters
  2. PIEZO activation threshold map (SPL vs frequency)
  3. Mechanotransduction pathway summary figure
  4. SPL threshold by body type
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency import (
    AbdominalModel, shell_modal_frequencies, breathing_mode_frequency,
)
from analytical.mechanotransduction import (
    MechanotransductionParams, find_piezo_activation_threshold,
    compute_displacement_field,
)

FIG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    'font.size': 11, 'font.family': 'serif',
    'axes.labelsize': 12, 'axes.titlesize': 13,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})

BROWN_BAND = (5, 10)


def fig1_parametric_frequencies():
    """Figure 1: How material/geometric parameters affect resonance."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    ax = axes[0]
    E_vals = np.logspace(np.log10(0.02), np.log10(7), 50) * 1e6
    f0_vals = [breathing_mode_frequency(AbdominalModel(E=E)) for E in E_vals]
    ax.semilogx(E_vals / 1e6, f0_vals, 'b-', linewidth=2)
    ax.axhspan(*BROWN_BAND, alpha=0.15, color='brown', label='Brown note range')
    ax.set_xlabel("Young's Modulus E [MPa]")
    ax.set_ylabel("Breathing Mode Frequency [Hz]")
    ax.set_title("(a) Wall Stiffness")
    ax.legend(loc='upper left'); ax.grid(True, alpha=0.3)

    ax = axes[1]
    h_vals = np.linspace(3, 40, 50) * 1e-3
    f0_h = [breathing_mode_frequency(AbdominalModel(h=h)) for h in h_vals]
    ax.plot(h_vals * 1000, f0_h, 'r-', linewidth=2)
    ax.axhspan(*BROWN_BAND, alpha=0.15, color='brown', label='Brown note range')
    ax.set_xlabel("Wall Thickness h [mm]")
    ax.set_ylabel("Breathing Mode Frequency [Hz]")
    ax.set_title("(b) Wall Thickness")
    ax.legend(loc='upper left'); ax.grid(True, alpha=0.3)

    ax = axes[2]
    a_vals = np.linspace(0.08, 0.28, 50)
    f0_a = [breathing_mode_frequency(AbdominalModel(a=a, b=a, c=a*0.667))
            for a in a_vals]
    ax.plot(a_vals * 100, f0_a, 'g-', linewidth=2)
    ax.axhspan(*BROWN_BAND, alpha=0.15, color='brown', label='Brown note range')
    ax.set_xlabel("Semi-major Axis a [cm]")
    ax.set_ylabel("Breathing Mode Frequency [Hz]")
    ax.set_title("(c) Cavity Size (BMI Proxy)")
    ax.legend(loc='upper right'); ax.grid(True, alpha=0.3)

    fig.suptitle("Parametric Sensitivity of Abdominal Cavity Breathing Mode",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig1_parametric_frequencies.png')
    fig.savefig(path); plt.close()
    print(f"  Saved: {path}")


def fig2_piezo_threshold_map():
    """Figure 2: Heatmap of tissue displacement (SPL vs frequency)."""
    params = MechanotransductionParams()
    model_soft = AbdominalModel(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f_res = breathing_mode_frequency(model_soft)

    freqs = np.linspace(1, 20, 200)
    spls = np.linspace(80, 150, 200)
    result = compute_displacement_field(freqs, spls, f_res, Q=5.0, params=params)
    disp = result['displacement_um']

    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.pcolormesh(freqs, spls, disp, cmap='hot_r', shading='auto', vmin=0, vmax=10)
    fig.colorbar(im, ax=ax, label='Tissue Displacement [μm]')
    cs = ax.contour(freqs, spls, disp, levels=[0.5, 1.0, 2.0, 5.0],
                    colors=['cyan', 'lime', 'yellow', 'white'], linewidths=1.5)
    ax.clabel(cs, fmt='%.1f μm', fontsize=9)
    ax.axvspan(*BROWN_BAND, alpha=0.2, color='brown', label='Brown note range')
    ax.axvline(f_res, color='white', linestyle='--', alpha=0.7,
               label=f'Model resonance ({f_res:.1f} Hz)')

    for spl_ref, label in [(120, 'Pain threshold'), (130, 'Jet @ 30m')]:
        ax.axhline(spl_ref, color='gray', linestyle=':', alpha=0.5)
        ax.text(19.5, spl_ref + 0.5, label, ha='right', fontsize=8, color='gray')

    ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("SPL [dB re 20 μPa]")
    ax.set_title(f"Tissue Displacement vs. Frequency & SPL (f_res={f_res:.1f} Hz, Q=5)",
                 fontweight='bold')
    ax.legend(loc='lower right')
    path = os.path.join(FIG_DIR, 'fig2_piezo_threshold_map.png')
    fig.savefig(path); plt.close()
    print(f"  Saved: {path}")


def fig3_spl_threshold_by_body_type():
    """Figure 3: SPL threshold for PIEZO activation across body types."""
    params = MechanotransductionParams()
    body_types = {
        'Lean (E=1.0, a=12cm)': AbdominalModel(E=1.0e6, a=0.12, b=0.12, c=0.08),
        'Average (E=0.5, a=15cm)': AbdominalModel(E=0.5e6),
        'Relaxed (E=0.2, a=15cm)': AbdominalModel(E=0.2e6),
        'Soft (E=0.1, a=18cm)': AbdominalModel(E=0.1e6, a=0.18, b=0.18, c=0.12),
        'Large (E=0.1, a=22cm)': AbdominalModel(E=0.1e6, a=0.22, b=0.22, c=0.15),
    }
    Q_values = [2, 3, 5, 7, 10]

    fig, ax = plt.subplots(figsize=(10, 6))
    for label, model in body_types.items():
        f_res = breathing_mode_frequency(model)
        spls = [find_piezo_activation_threshold(f_res, Q, 1.0, params) for Q in Q_values]
        ax.plot(Q_values, spls, 'o-', linewidth=2, markersize=8,
                label=f'{label} (f={f_res:.1f} Hz)')

    ax.axhline(120, color='red', linestyle='--', alpha=0.5)
    ax.axhline(130, color='orange', linestyle='--', alpha=0.5)
    ax.text(10.2, 120.5, '120 dB: pain', fontsize=8, color='red')
    ax.text(10.2, 130.5, '130 dB: jet engine', fontsize=8, color='orange')

    ax.set_xlabel("Quality Factor Q"); ax.set_ylabel("Min SPL for 1 μm displacement [dB]")
    ax.set_title("SPL Required for PIEZO Activation by Body Type", fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3); ax.set_ylim(90, 155)

    path = os.path.join(FIG_DIR, 'fig3_spl_by_body_type.png')
    fig.savefig(path); plt.close()
    print(f"  Saved: {path}")


def fig4_modal_spectrum():
    """Figure 4: Modal spectrum for different body configurations."""
    configs = {
        'Baseline': AbdominalModel(),
        'Soft tissue': AbdominalModel(E=0.1e6),
        'Large cavity': AbdominalModel(a=0.20, b=0.20, c=0.13),
        'Soft + Large': AbdominalModel(E=0.1e6, a=0.18, b=0.18, c=0.12),
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    modes = list(range(11))
    width = 0.2
    offsets = np.arange(len(configs)) * width - width * len(configs) / 2

    for i, (label, model) in enumerate(configs.items()):
        freqs = shell_modal_frequencies(model, n_max=10)
        f_vals = [freqs[n] for n in modes]
        bars = ax.bar([m + offsets[i] for m in modes], f_vals, width=width,
                      label=label, alpha=0.8)

    ax.axhspan(*BROWN_BAND, alpha=0.15, color='brown', zorder=0)
    ax.text(10.5, 7.5, 'Brown note\nrange', fontsize=9, color='brown',
            ha='center', style='italic')
    ax.set_xlabel("Mode Number n"); ax.set_ylabel("Natural Frequency [Hz]")
    ax.set_title("Modal Spectrum of Abdominal Cavity Models", fontweight='bold')
    ax.set_xticks(modes)
    ax.legend(); ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 50)

    path = os.path.join(FIG_DIR, 'fig4_modal_spectrum.png')
    fig.savefig(path); plt.close()
    print(f"  Saved: {path}")


if __name__ == "__main__":
    print("\n  Generating publication figures...\n")
    fig1_parametric_frequencies()
    fig2_piezo_threshold_map()
    fig3_spl_threshold_by_body_type()
    fig4_modal_spectrum()
    print("\n  All figures generated.\n")
