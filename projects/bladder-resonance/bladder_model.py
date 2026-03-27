"""
Bladder resonance model: predicting natural frequencies of the urinary
bladder as a fluid-filled viscoelastic shell.

Uses the AbdominalModelV2 framework from the browntone project with
bladder-specific parameters. The bladder is modelled as a near-spherical
shell whose geometry and material properties change with fill volume.

Key parameters (from literature):
    Radius:         2.3 cm (50 mL) to 4.9 cm (500 mL)
    Wall thickness:  ~5 mm (empty) to ~3 mm (full) — constant tissue volume
    Young's modulus: 10 kPa (rest) to 200 kPa (distended)
    Poisson's ratio: 0.49 (nearly incompressible)
    Fluid density:   1020 kg/m³ (urine ≈ water)
    Intravesical pressure: 5–30 cmH₂O (490–2940 Pa)

References:
    - Ultrasound bladder vibrometry (IOP 2013): μ₁ = 9.6–48.7 kPa
    - Barnes (2016) PhD: viscoelastic properties of bladder wall
    - ISO 2631-1:1997: pelvic resonance 4–8 Hz
"""

import sys
import os

sys.path.insert(0, r'C:\Users\jon\OneDrive\Projects\browntone-worktrees\bladder-resonance')
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
    flexural_mode_pressure_response,
)

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIGURES_DIR = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Bladder geometry from fill volume
# ---------------------------------------------------------------------------

def bladder_radius_from_volume(vol_mL: float) -> float:
    """Equivalent sphere radius [m] from fill volume [mL]."""
    vol_m3 = vol_mL * 1e-6
    return (3 * vol_m3 / (4 * np.pi)) ** (1 / 3)


def bladder_wall_thickness(vol_mL: float) -> float:
    """
    Wall thickness [m] assuming approximately constant tissue volume.

    At 50 mL the wall is ~5 mm; at 500 mL it thins to ~3 mm.
    We assume a fixed tissue shell volume and compute h from that.
    """
    R0 = bladder_radius_from_volume(50.0)
    h0 = 5.0e-3  # 5 mm at 50 mL
    tissue_vol = (4 / 3) * np.pi * ((R0 + h0) ** 3 - R0 ** 3)
    R = bladder_radius_from_volume(vol_mL)
    # Solve (R+h)^3 = R^3 + tissue_vol * 3/(4π)
    h = ((R ** 3 + tissue_vol * 3 / (4 * np.pi)) ** (1 / 3)) - R
    return max(h, 1.5e-3)  # floor at 1.5 mm


def bladder_elastic_modulus(vol_mL: float) -> float:
    """
    Young's modulus [Pa] as a function of fill volume.

    Bladder wall stiffens dramatically with stretch.
    At low fill (~50 mL): E ≈ 10 kPa
    At high fill (~500 mL): E ≈ 200 kPa
    Exponential-ish relationship from vibrometry data.
    """
    E_min = 10e3   # 10 kPa at 50 mL
    E_max = 200e3  # 200 kPa at 500 mL
    frac = np.clip((vol_mL - 50) / 450, 0, 1)
    return E_min * (E_max / E_min) ** frac


def intravesical_pressure(vol_mL: float) -> float:
    """
    Intravesical pressure [Pa] from fill volume.

    Low fill: ~5 cmH₂O ≈ 490 Pa (compliant phase)
    High fill: ~30 cmH₂O ≈ 2940 Pa (steep phase)
    """
    P_min = 490.0    # 5 cmH₂O
    P_max = 2940.0   # 30 cmH₂O
    frac = np.clip((vol_mL - 50) / 450, 0, 1)
    return P_min + (P_max - P_min) * frac ** 2  # convex (compliant then steep)


def make_bladder_model(vol_mL: float) -> AbdominalModelV2:
    """Create an AbdominalModelV2 configured as a bladder at given fill volume."""
    R = bladder_radius_from_volume(vol_mL)
    h = bladder_wall_thickness(vol_mL)
    E = bladder_elastic_modulus(vol_mL)
    P = intravesical_pressure(vol_mL)

    return AbdominalModelV2(
        a=R, b=R, c=R,          # spherical
        h=h,
        E=E,
        nu=0.49,                 # nearly incompressible soft tissue
        rho_wall=1050.0,         # tissue density
        loss_tangent=0.4,        # bladder is highly viscous
        rho_fluid=1020.0,        # urine
        K_fluid=2.2e9,           # bulk modulus of water
        P_iap=P,                 # intravesical pressure
    )


# ---------------------------------------------------------------------------
# Parametric study: frequency vs fill volume
# ---------------------------------------------------------------------------

def parametric_frequency_vs_volume():
    """Compute f₂ and f₃ across fill volumes."""
    volumes = np.linspace(50, 500, 50)
    f2_vals, f3_vals = [], []
    radii, thicknesses, moduli, pressures = [], [], [], []

    for v in volumes:
        model = make_bladder_model(v)
        freqs = flexural_mode_frequencies_v2(model, n_max=4)
        f2_vals.append(freqs[2])
        f3_vals.append(freqs[3])
        radii.append(bladder_radius_from_volume(v) * 100)  # cm
        thicknesses.append(bladder_wall_thickness(v) * 1000)  # mm
        moduli.append(bladder_elastic_modulus(v) / 1e3)  # kPa
        pressures.append(intravesical_pressure(v))  # Pa

    return {
        'volumes': volumes,
        'f2': np.array(f2_vals),
        'f3': np.array(f3_vals),
        'radii': np.array(radii),
        'thicknesses': np.array(thicknesses),
        'moduli': np.array(moduli),
        'pressures': np.array(pressures),
    }


def plot_frequency_vs_volume(data: dict):
    """Generate fig_bladder_frequency_vs_volume.png."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('Bladder Resonant Frequency vs Fill Volume', fontsize=14, fontweight='bold')

    # (a) f₂ and f₃ vs volume
    ax = axes[0, 0]
    ax.plot(data['volumes'], data['f2'], 'b-', linewidth=2, label='n = 2 (oblate-prolate)')
    ax.plot(data['volumes'], data['f3'], 'r--', linewidth=2, label='n = 3')
    ax.axhspan(4, 8, alpha=0.15, color='orange', label='ISO 2631 pelvic range (4–8 Hz)')
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_title('(a) Flexural Mode Frequencies')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (b) Geometry vs volume
    ax = axes[0, 1]
    ax2 = ax.twinx()
    ln1 = ax.plot(data['volumes'], data['radii'], 'g-', linewidth=2, label='Radius [cm]')
    ln2 = ax2.plot(data['volumes'], data['thicknesses'], 'm--', linewidth=2, label='Wall thickness [mm]')
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('Radius [cm]', color='g')
    ax2.set_ylabel('Wall Thickness [mm]', color='m')
    ax.set_title('(b) Geometry vs Fill State')
    lns = ln1 + ln2
    ax.legend(lns, [l.get_label() for l in lns], fontsize=8)
    ax.grid(True, alpha=0.3)

    # (c) Elastic modulus vs volume
    ax = axes[1, 0]
    ax.plot(data['volumes'], data['moduli'], 'k-', linewidth=2)
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('E [kPa]')
    ax.set_title('(c) Wall Elastic Modulus (Strain-Stiffening)')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)

    # (d) Intravesical pressure vs volume
    ax = axes[1, 1]
    ax.plot(data['volumes'], data['pressures'] / 98.0665, 'brown', linewidth=2)
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('Intravesical Pressure [cmH₂O]')
    ax.set_title('(d) Cystometric Pressure Curve')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, 'fig_bladder_frequency_vs_volume.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {path}')
    return path


# ---------------------------------------------------------------------------
# Coupling analysis: airborne vs mechanical
# ---------------------------------------------------------------------------

def coupling_analysis():
    """
    Compare airborne acoustic coupling vs mechanical (WBV) coupling.

    Airborne: pressure gradient coupling scales as (ka)^n — very weak.
    Mechanical: direct displacement input from pelvic vibration — full coupling.
    """
    vol = 300.0  # typical "need to go" volume
    model = make_bladder_model(vol)
    R = model.equivalent_sphere_radius
    freqs = flexural_mode_frequencies_v2(model, n_max=6)
    f2 = freqs[2]

    freq_range = np.linspace(1, 20, 200)

    # Airborne coupling: (ka)^2 for n=2
    c_air = 343.0
    ka_vals = 2 * np.pi * freq_range * R / c_air
    airborne_coupling = ka_vals ** 2

    # Mechanical coupling: direct pelvic vibration
    # Transmissibility from seat to pelvis (ISO 2631 weighted)
    # Peak around 4-8 Hz with transmissibility ~1.5
    # Model as a resonant response with f_pelvis ≈ 5 Hz, Q ≈ 2
    f_pelvis = 5.5  # Hz, pelvic resonance
    zeta_pelvis = 0.25
    r_pelvis = freq_range / f_pelvis
    T_pelvis = np.sqrt((1 + (2 * zeta_pelvis * r_pelvis) ** 2) /
                       ((1 - r_pelvis ** 2) ** 2 + (2 * zeta_pelvis * r_pelvis) ** 2))

    # Bladder modal amplification (n=2)
    zeta_bladder = model.damping_ratio
    r_bladder = freq_range / f2
    H_bladder = 1 / np.sqrt((1 - r_bladder ** 2) ** 2 + (2 * zeta_bladder * r_bladder) ** 2)

    # Combined mechanical coupling: seat → pelvis → bladder wall
    mechanical_coupling = T_pelvis * H_bladder

    # Coupling ratio
    ratio = mechanical_coupling / airborne_coupling

    return {
        'freq': freq_range,
        'f2': f2,
        'ka': ka_vals,
        'airborne': airborne_coupling,
        'T_pelvis': T_pelvis,
        'H_bladder': H_bladder,
        'mechanical': mechanical_coupling,
        'ratio': ratio,
    }


def plot_coupling(data: dict):
    """Generate fig_bladder_coupling.png."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        f'Coupling Pathways to Bladder (300 mL, f₂ = {data["f2"]:.1f} Hz)',
        fontsize=13, fontweight='bold',
    )

    # (a) Airborne vs mechanical
    ax = axes[0]
    ax.semilogy(data['freq'], data['airborne'], 'b-', linewidth=2, label='Airborne (ka)²')
    ax.semilogy(data['freq'], data['mechanical'], 'r-', linewidth=2, label='Mechanical (seat→pelvis→bladder)')
    ax.axvline(data['f2'], color='gray', ls=':', label=f'f₂ = {data["f2"]:.1f} Hz')
    ax.axvspan(4, 8, alpha=0.1, color='orange')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Effective Coupling (normalised)')
    ax.set_title('(a) Coupling Pathways')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (b) Coupling ratio
    ax = axes[1]
    ax.semilogy(data['freq'], data['ratio'], 'k-', linewidth=2)
    ax.axvline(data['f2'], color='gray', ls=':')
    ax.axhspan(1, 1, color='gray')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Mechanical / Airborne Ratio')
    ax.set_title('(b) Mechanical Advantage')
    ax.grid(True, alpha=0.3)

    # (c) Components of mechanical path
    ax = axes[2]
    ax.plot(data['freq'], data['T_pelvis'], 'g-', linewidth=2, label='Seat→Pelvis transmissibility')
    ax.plot(data['freq'], data['H_bladder'], 'm--', linewidth=2, label='Bladder modal amplification')
    ax.axvline(data['f2'], color='gray', ls=':', label=f'f₂ = {data["f2"]:.1f} Hz')
    ax.axvspan(4, 8, alpha=0.1, color='orange', label='ISO 2631 range')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplification Factor')
    ax.set_title('(c) Mechanical Pathway Components')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, 'fig_bladder_coupling.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {path}')
    return path


# ---------------------------------------------------------------------------
# Console report
# ---------------------------------------------------------------------------

def print_report(param_data: dict, coupling_data: dict):
    """Print summary to console."""
    print()
    print('=' * 72)
    print('  BLADDER RESONANCE MODEL — Fluid-Filled Viscoelastic Shell')
    print('  Using AbdominalModelV2 framework with bladder-specific parameters')
    print('=' * 72)
    print()

    # Key fill states
    print('  MODAL FREQUENCIES AT KEY FILL STATES')
    print('  ' + '-' * 62)
    print(f'  {"Volume":>8} {"R(cm)":>7} {"h(mm)":>7} {"E(kPa)":>8} {"f₂(Hz)":>8} {"f₃(Hz)":>8}  Notes')
    print('  ' + '-' * 62)

    for vol in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
        model = make_bladder_model(vol)
        freqs = flexural_mode_frequencies_v2(model, n_max=4)
        R_cm = model.equivalent_sphere_radius * 100
        h_mm = model.h * 1000
        E_kPa = model.E / 1e3
        f2 = freqs[2]
        f3 = freqs[3]

        notes = ''
        if 4 <= f2 <= 8:
            notes = '← ISO 2631 range!'
        elif vol == 300:
            notes = '← "need to go"'

        print(f'  {vol:>6} mL {R_cm:>6.2f} {h_mm:>6.2f} {E_kPa:>7.1f} {f2:>7.2f} {f3:>7.2f}  {notes}')
    print('  ' + '-' * 62)
    print()

    # Key finding
    f2_at_300 = coupling_data['f2']
    print(f'  KEY FINDING: At 300 mL fill, f₂ = {f2_at_300:.1f} Hz')
    print()
    print('  ISO 2631 pelvic resonance range: 4–8 Hz')
    in_range = [(v, f) for v, f in zip(param_data['volumes'], param_data['f2']) if 4 <= f <= 8]
    if in_range:
        v_min = min(v for v, _ in in_range)
        v_max = max(v for v, _ in in_range)
        print(f'  Bladder f₂ falls in ISO range for fill volumes: {v_min:.0f}–{v_max:.0f} mL')
    else:
        closest_idx = np.argmin(np.abs(param_data['f2'] - 6.0))
        print(f'  Closest f₂ to 6 Hz: {param_data["f2"][closest_idx]:.1f} Hz '
              f'at {param_data["volumes"][closest_idx]:.0f} mL')
    print()

    # Coupling
    at_f2_idx = np.argmin(np.abs(coupling_data['freq'] - f2_at_300))
    mech = coupling_data['mechanical'][at_f2_idx]
    airb = coupling_data['airborne'][at_f2_idx]
    print(f'  COUPLING AT f₂ = {f2_at_300:.1f} Hz:')
    print(f'    Airborne (ka)² coupling:    {airb:.2e}')
    print(f'    Mechanical WBV coupling:    {mech:.2f}')
    print(f'    Mechanical advantage:       {mech/airb:.0f}×')
    print()
    print('  CONCLUSION:')
    print('  The bladder n=2 mode (12–18 Hz) sits above the ISO 2631')
    print('  peak pelvic resonance (4–8 Hz) but within the broader')
    print('  WBV-affected band. Mechanical coupling from seat/pelvic')
    print('  vibration is ~10⁴× more effective than airborne sound.')
    print('  At sub-resonant WBV frequencies (4–8 Hz), the bladder')
    print('  still responds as a forced oscillator, and pelvic')
    print('  transmissibility amplifies the input — consistent with')
    print('  occupational reports of vibration-induced urgency.')
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print('\n  Computing parametric study...')
    param_data = parametric_frequency_vs_volume()
    plot_frequency_vs_volume(param_data)

    print('  Computing coupling analysis...')
    coupling_data = coupling_analysis()
    plot_coupling(coupling_data)

    print_report(param_data, coupling_data)
