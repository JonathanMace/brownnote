"""
Generate publication-quality figures for the v2 model.

Updated from v1 to use corrected flexural mode physics.
All figures suitable for Journal of Sound and Vibration submission.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2, breathing_mode_v2,
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 200,
    'savefig.dpi': 300,
})


def fig1_parametric_frequencies():
    """Fig 1: Parametric sensitivity of n=2 flexural mode."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # (a) E sweep
    ax = axes[0]
    E_range = np.logspace(np.log10(0.03), np.log10(5.0), 50)
    for a_val, ls in [(0.15, '--'), (0.18, '-'), (0.20, ':')]:
        freqs = []
        for E in E_range:
            m = AbdominalModelV2(E=E*1e6, a=a_val, b=a_val, c=a_val*0.67)
            freqs.append(flexural_mode_frequencies_v2(m, n_max=2)[2])
        ax.semilogx(E_range, freqs, ls, label=f'a={a_val*100:.0f} cm')

    ax.axhspan(5, 10, alpha=0.15, color='brown', label='"Brown note" range')
    ax.axhspan(4, 8, alpha=0.10, color='blue', label='ISO 2631 range')
    ax.set_xlabel('Elastic modulus E (MPa)')
    ax.set_ylabel('n=2 frequency (Hz)')
    ax.set_title('(a) Modulus sensitivity')
    ax.legend(loc='upper left', fontsize=8)
    ax.set_ylim(0, 25)
    ax.grid(True, alpha=0.3)

    # (b) Aspect ratio (c/a) sweep
    ax = axes[1]
    ca_range = np.linspace(0.4, 0.95, 40)
    for E_val, ls in [(0.1, '-'), (0.2, '--'), (0.5, ':')]:
        freqs = []
        for ca in ca_range:
            m = AbdominalModelV2(E=E_val*1e6, a=0.18, b=0.18, c=0.18*ca)
            freqs.append(flexural_mode_frequencies_v2(m, n_max=2)[2])
        ax.plot(ca_range, freqs, ls, label=f'E={E_val} MPa')

    ax.axhspan(5, 10, alpha=0.15, color='brown')
    ax.axhspan(4, 8, alpha=0.10, color='blue')
    ax.set_xlabel('Aspect ratio c/a')
    ax.set_ylabel('n=2 frequency (Hz)')
    ax.set_title('(b) Geometry sensitivity')
    ax.legend(loc='upper left', fontsize=8)
    ax.set_ylim(0, 20)
    ax.grid(True, alpha=0.3)

    # (c) Wall thickness sweep
    ax = axes[2]
    h_range = np.linspace(0.003, 0.020, 40)
    for E_val, ls in [(0.1, '-'), (0.2, '--'), (0.5, ':')]:
        freqs = []
        for h in h_range:
            m = AbdominalModelV2(E=E_val*1e6, a=0.18, b=0.18, c=0.12, h=h)
            freqs.append(flexural_mode_frequencies_v2(m, n_max=2)[2])
        ax.plot(h_range * 1000, freqs, ls, label=f'E={E_val} MPa')

    ax.axhspan(5, 10, alpha=0.15, color='brown')
    ax.axhspan(4, 8, alpha=0.10, color='blue')
    ax.set_xlabel('Wall thickness h (mm)')
    ax.set_ylabel('n=2 frequency (Hz)')
    ax.set_title('(c) Thickness sensitivity')
    ax.legend(loc='upper left', fontsize=8)
    ax.set_ylim(0, 20)
    ax.grid(True, alpha=0.3)

    fig.suptitle('Parametric sensitivity of n=2 flexural mode (v2 model)',
                 fontsize=13, y=1.02)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig1_v2_parametric_frequencies.png')
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")


def fig2_coupling_comparison():
    """Fig 2: Airborne vs mechanical coupling — the key result."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]
    R = model.equivalent_sphere_radius
    Q = model.Q

    # (a) Displacement vs SPL for airborne
    ax = axes[0]
    spl_range = np.linspace(80, 160, 80)
    p_ref = 20e-6

    for n, color in [(2, 'C0'), (3, 'C1'), (4, 'C2')]:
        m = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
        freqs = flexural_mode_frequencies_v2(m, n_max=n)
        f_n = freqs[n]
        ka = 2 * np.pi * f_n * R / 343.0

        E_val, h, nu = m.E, m.h, m.nu
        D = m.D
        K_b = n*(n-1)*(n+2)**2 * D / R**4
        lam = (n**2+n-2+2*nu)/(n**2+n+1-nu)
        K_m = E_val * h / R**2 * lam
        K_p = m.P_iap / R * (n-1)*(n+2)
        K_tot = K_b + K_m + K_p

        xi_um = []
        for spl in spl_range:
            p = p_ref * 10**(spl/20)
            p_eff = p * ka**n
            xi = p_eff / K_tot * Q * 1e6
            xi_um.append(xi)

        ax.semilogy(spl_range, xi_um, color=color,
                     label=f'n={n} (f={f_n:.1f} Hz)')

    # PIEZO thresholds
    ax.axhline(0.5, color='red', ls='--', alpha=0.6, label='PIEZO2 threshold')
    ax.axhline(2.0, color='red', ls=':', alpha=0.6, label='PIEZO1 threshold')
    ax.axvline(120, color='gray', ls=':', alpha=0.4, label='Pain threshold')
    ax.axvline(140, color='gray', ls='--', alpha=0.4, label='Jet engine')

    ax.set_xlabel('Sound Pressure Level (dB)')
    ax.set_ylabel('Displacement at resonance (μm)')
    ax.set_title('(a) Airborne acoustic coupling')
    ax.legend(fontsize=7, loc='upper left')
    ax.set_ylim(1e-4, 100)
    ax.grid(True, alpha=0.3)

    # (b) Displacement vs acceleration for mechanical
    ax = axes[1]
    a_range = np.logspace(-2, 1, 60)

    zeta = model.damping_ratio
    omega_n = 2 * np.pi * f2
    # At resonance: H_rel = 1/(2ζ) = Q
    for label, mult in [('Free shell (model)', Q),
                        ('ISO 2631 (T-1≈0.89)', 0.89)]:
        xi_um = []
        for a_rms in a_range:
            omega = omega_n  # at resonance
            x_base = a_rms * np.sqrt(2) / omega**2
            x_rel = x_base * mult
            xi_um.append(x_rel * 1e6)

        ax.loglog(a_range, xi_um, label=label)

    ax.axhline(0.5, color='red', ls='--', alpha=0.6, label='PIEZO2 threshold')
    ax.axhline(2.0, color='red', ls=':', alpha=0.6, label='PIEZO1 threshold')
    ax.axvline(0.5, color='green', ls=':', alpha=0.5, label='EU Action Value')
    ax.axvline(1.15, color='green', ls='--', alpha=0.5, label='EU Limit')

    ax.set_xlabel('Vibration acceleration RMS (m/s²)')
    ax.set_ylabel('Relative displacement (μm)')
    ax.set_title('(b) Mechanical (whole-body) coupling')
    ax.legend(fontsize=7, loc='upper left')
    ax.set_ylim(1e-1, 1e5)
    ax.grid(True, alpha=0.3)

    fig.suptitle('Airborne vs mechanical coupling to n=2 flexural mode',
                 fontsize=13, y=1.02)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig2_v2_coupling_comparison.png')
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")


def fig3_iso2631_validation():
    """Fig 3: Our model predictions vs ISO 2631 published data."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    # ISO 2631 data (approximate transmissibility curves)
    iso_freqs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20])
    iso_T = np.array([1.0, 1.1, 1.3, 1.7, 2.2, 2.5, 2.3, 1.8, 1.2, 0.9, 0.7, 0.5])
    ax.plot(iso_freqs, iso_T, 'ko-', markersize=6, label='ISO 2631 (seated, z-axis)', zorder=5)

    # Our model for different body types
    body_types = {
        'lean (E=0.2, a=15cm)': AbdominalModelV2(E=0.2e6, a=0.15, b=0.15, c=0.10, h=0.010),
        'average (E=0.1, a=18cm)': AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12, h=0.010),
        'large (E=0.08, a=20cm)': AbdominalModelV2(E=0.08e6, a=0.20, b=0.20, c=0.14, h=0.008),
    }

    freq_fine = np.linspace(1, 20, 200)
    for name, model in body_types.items():
        f_n = flexural_mode_frequencies_v2(model, n_max=2)[2]
        zeta = model.damping_ratio
        H = []
        for f in freq_fine:
            r = f / f_n
            h_val = r**2 / np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
            H.append(1 + h_val)  # absolute transmissibility
        ax.plot(freq_fine, H, '--', alpha=0.7, label=f'Model: {name}')
        ax.axvline(f_n, color='gray', ls=':', alpha=0.2)

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Transmissibility')
    ax.set_title('Model vs ISO 2631 seat-to-abdomen transmissibility')
    ax.legend(fontsize=8, loc='upper right')
    ax.set_xlim(1, 20)
    ax.set_ylim(0, 5)
    ax.grid(True, alpha=0.3)

    path = os.path.join(OUTPUT_DIR, 'fig3_v2_iso2631_validation.png')
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")


def fig4_mechanism_diagram():
    """Fig 4: Schematic of the two coupling pathways."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(5, 6.5, 'Two pathways for low-frequency excitation of abdominal resonance',
            ha='center', va='center', fontsize=13, fontweight='bold')

    # AIRBORNE pathway (left)
    ax.text(2.5, 5.5, 'AIRBORNE ACOUSTIC', ha='center', fontsize=11,
            fontweight='bold', color='C0',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightskyblue', alpha=0.3))

    steps_air = [
        (2.5, 4.8, 'Sound source (loudspeaker)'),
        (2.5, 4.2, 'Air → tissue interface\n(~99.9% reflection)'),
        (2.5, 3.4, 'Scattering: p_eff = p × (ka)ⁿ\n(ka ≈ 0.017, huge penalty)'),
        (2.5, 2.6, 'Flexural mode excitation\n(~0.14 μm at 120 dB)'),
        (2.5, 1.8, '< PIEZO threshold (0.5 μm)'),
    ]
    for x, y, txt in steps_air:
        ax.text(x, y, txt, ha='center', va='center', fontsize=8,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='lightblue', alpha=0.15))

    for i in range(len(steps_air)-1):
        ax.annotate('', xy=(2.5, steps_air[i+1][1]+0.25),
                     xytext=(2.5, steps_air[i][1]-0.25),
                     arrowprops=dict(arrowstyle='->', color='C0', lw=1.5))

    ax.text(2.5, 1.1, '✗ IMPLAUSIBLE', ha='center', fontsize=11,
            fontweight='bold', color='red')

    # MECHANICAL pathway (right)
    ax.text(7.5, 5.5, 'MECHANICAL (WBV)', ha='center', fontsize=11,
            fontweight='bold', color='C1',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.3))

    steps_mech = [
        (7.5, 4.8, 'Vibration source (floor/seat)'),
        (7.5, 4.2, 'Skeletal transmission\n(no impedance mismatch)'),
        (7.5, 3.4, 'Direct base excitation\n(full amplitude coupling)'),
        (7.5, 2.6, 'Flexural mode resonance\n(~600 μm at 0.1 m/s²)'),
        (7.5, 1.8, '>> PIEZO threshold (0.5 μm)'),
    ]
    for x, y, txt in steps_mech:
        ax.text(x, y, txt, ha='center', va='center', fontsize=8,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.15))

    for i in range(len(steps_mech)-1):
        ax.annotate('', xy=(7.5, steps_mech[i+1][1]+0.25),
                     xytext=(7.5, steps_mech[i][1]-0.25),
                     arrowprops=dict(arrowstyle='->', color='C1', lw=1.5))

    ax.text(7.5, 1.1, '✓ PLAUSIBLE', ha='center', fontsize=11,
            fontweight='bold', color='green')

    # Dividing line
    ax.plot([5, 5], [1, 6], 'k--', alpha=0.3, lw=1)

    # Bottom note
    ax.text(5, 0.3, 'The "brown note" myth conflates these pathways.\n'
            'Airborne infrasound is orders of magnitude too weak; '
            'whole-body vibration is the real mechanism.',
            ha='center', va='center', fontsize=9, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.2))

    path = os.path.join(OUTPUT_DIR, 'fig4_v2_mechanism_pathways.png')
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")


if __name__ == '__main__':
    print()
    print("Generating v2 publication figures...")
    print()

    fig1_parametric_frequencies()
    fig2_coupling_comparison()
    fig3_iso2631_validation()
    fig4_mechanism_diagram()

    print()
    print("All figures generated successfully.")
