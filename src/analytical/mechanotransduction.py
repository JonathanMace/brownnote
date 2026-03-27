"""
Mechanotransduction pathway analysis for infrasound-induced GI effects.

Connects:
  1. Acoustic pressure (SPL) → tissue displacement
  2. Tissue displacement → PIEZO channel activation
  3. PIEZO activation → neural signaling → reflex potential

This script quantifies whether infrasound at abdominal resonance
frequencies can plausibly activate mechanosensitive ion channels
in the intestinal wall.

Key thresholds (from literature):
  - PIEZO1/PIEZO2 activation: 0.5-2.0 μm displacement
  - Defecation reflex: 5-15 mmHg rectal distension pressure
  - Vagal afferent activation: ~1-5 μm tissue strain

References:
  - Zeitzschel & Lechner (2024) Channels 18(1):2355123
  - Frontiers Physiol (2024) 15:1356317 — PIEZO in intestinal tract
  - ISO 2631-1:1997 — Whole-body vibration
"""

import numpy as np
import json
from dataclasses import dataclass
from typing import Optional

# Import our shell model
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency import AbdominalModel, shell_modal_frequencies, breathing_mode_frequency


@dataclass
class MechanotransductionParams:
    """Thresholds for mechanosensitive pathways in the GI tract."""

    # PIEZO channel activation thresholds [μm]
    piezo2_threshold_low: float = 0.5   # most sensitive (rapid adaptation)
    piezo1_threshold_low: float = 0.5
    piezo_threshold_mid: float = 1.0    # typical
    piezo_threshold_high: float = 2.0   # conservative

    # Quality factors for soft tissue resonance
    Q_low: float = 2.0     # heavily damped (ascites, obese)
    Q_mid: float = 5.0     # typical soft tissue
    Q_high: float = 10.0   # lean, taut abdominal wall

    # Defecation reflex thresholds [mmHg]
    reflex_threshold_low: float = 5.0    # RAIR onset
    reflex_threshold_mid: float = 10.0   # urge to defecate
    reflex_threshold_high: float = 15.0  # strong urge

    # Tissue acoustic properties
    rho_tissue: float = 1040.0   # kg/m³
    c_tissue: float = 1540.0     # m/s (speed of sound in soft tissue)


def compute_displacement_field(
    freqs_hz: np.ndarray,
    spl_db: np.ndarray,
    resonance_freq: float,
    Q: float,
    params: Optional[MechanotransductionParams] = None,
) -> dict:
    """
    Compute tissue displacement amplitude as a function of frequency and SPL,
    including resonance amplification.

    Uses a single-degree-of-freedom resonance model:
        H(f) = 1 / sqrt((1 - r²)² + (2ζr)²)
    where r = f/f_n and ζ = 1/(2Q)

    Returns 2D arrays of displacement [μm] over (freq, SPL) space.
    """
    if params is None:
        params = MechanotransductionParams()

    p_ref = 20e-6  # Pa
    zeta = 1 / (2 * Q)

    # Create 2D grid
    F, S = np.meshgrid(freqs_hz, spl_db)

    # Acoustic pressure
    P = p_ref * 10**(S / 20)

    # Free-field particle velocity
    V = P / (params.rho_tissue * params.c_tissue)

    # Free-field displacement
    XI_free = V / (2 * np.pi * np.maximum(F, 0.1))

    # Resonance amplification (frequency response)
    r = F / resonance_freq
    H = 1 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)

    # Resonant displacement [μm]
    XI_resonant = XI_free * H * 1e6

    return {
        'freqs_hz': freqs_hz,
        'spl_db': spl_db,
        'displacement_um': XI_resonant,
        'amplification': H,
        'pressure_pa': P,
        'resonance_freq': resonance_freq,
        'Q': Q,
    }


def find_piezo_activation_threshold(
    resonance_freq: float,
    Q: float,
    piezo_threshold_um: float = 1.0,
    params: Optional[MechanotransductionParams] = None,
) -> float:
    """
    Find the minimum SPL (dB) at the resonance frequency needed to
    produce tissue displacement exceeding the PIEZO channel threshold.

    Returns SPL in dB.
    """
    if params is None:
        params = MechanotransductionParams()

    p_ref = 20e-6
    target_xi = piezo_threshold_um * 1e-6  # convert to meters

    # At resonance, H = Q (for underdamped system)
    # displacement = (p / (rho * c)) / (2*pi*f) * Q
    # Solve for p:
    p_required = target_xi * (2 * np.pi * resonance_freq) * params.rho_tissue * params.c_tissue / Q

    spl = 20 * np.log10(p_required / p_ref)
    return spl


def pressure_from_displacement(
    displacement_um: float,
    freq: float,
    Q: float,
    params: Optional[MechanotransductionParams] = None,
) -> float:
    """Convert resonant displacement to equivalent oscillating pressure [mmHg]."""
    if params is None:
        params = MechanotransductionParams()

    # At resonance, the wall displacement creates pressure oscillation
    # in the contained fluid via bulk modulus coupling
    # ΔP ≈ K * (Δξ / R) for volumetric strain of a sphere
    # More conservatively: ΔP = ρ * (2πf)² * ξ * Q (from momentum)

    xi_m = displacement_um * 1e-6
    # Dynamic pressure from oscillating fluid
    delta_p = params.rho_tissue * (2 * np.pi * freq)**2 * xi_m
    # Amplified at resonance
    delta_p_resonant = delta_p * Q

    # Convert Pa to mmHg (1 mmHg = 133.322 Pa)
    return delta_p_resonant / 133.322


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("  BROWNTONE — Mechanotransduction Pathway Analysis")
    print("  Can infrasound activate PIEZO channels in the intestinal wall?")
    print("=" * 70)
    print()

    params = MechanotransductionParams()
    model = AbdominalModel()

    # Compute modal frequencies
    freqs = shell_modal_frequencies(model, n_max=6)
    f_breathe = freqs[0]
    f_n2 = freqs[2]

    print("  ABDOMINAL MODEL RESONANCES")
    print("  " + "-" * 50)
    print(f"    Breathing mode (n=0):  {f_breathe:.2f} Hz")
    print(f"    First flexural (n=2):  {f_n2:.2f} Hz")
    print()

    # Also compute for physiologically realistic soft tissue
    model_soft = AbdominalModel(E=0.1e6)  # relaxed muscle
    f_soft = breathing_mode_frequency(model_soft)
    print(f"    Soft tissue (E=0.1 MPa) breathing mode: {f_soft:.2f} Hz")

    model_large = AbdominalModel(a=0.20, b=0.20, c=0.13)
    f_large = breathing_mode_frequency(model_large)
    print(f"    Large cavity (a=20cm)  breathing mode: {f_large:.2f} Hz")

    model_target = AbdominalModel(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f_target = breathing_mode_frequency(model_target)
    print(f"    Combined soft+large    breathing mode: {f_target:.2f} Hz")
    print()

    # Find minimum SPL for PIEZO activation at each resonance
    print("  MINIMUM SPL FOR PIEZO CHANNEL ACTIVATION")
    print("  " + "-" * 65)
    print(f"  {'Scenario':<30} {'f_res(Hz)':>10} {'Q':>5} {'SPL(dB)':>10} {'Feasible?':>10}")
    print("  " + "-" * 65)

    scenarios = [
        ("Baseline (E=0.5, a=15)", f_breathe, 5.0),
        ("Soft tissue (E=0.1)", f_soft, 5.0),
        ("Large cavity (a=20)", f_large, 5.0),
        ("Soft+large combo", f_target, 5.0),
        ("Soft+large, high Q", f_target, 10.0),
        ("Soft+large, low Q", f_target, 2.0),
        ("Flexural n=2", f_n2, 5.0),
    ]

    for name, f_res, Q in scenarios:
        for thresh in [0.5, 1.0, 2.0]:
            spl = find_piezo_activation_threshold(f_res, Q, thresh, params)
            feasible = "YES" if spl <= 140 else "marginal" if spl <= 150 else "no"
            if thresh == 1.0:  # only print mid threshold
                print(f"  {name:<30} {f_res:>10.2f} {Q:>5.0f} {spl:>10.1f} {feasible:>10}")

    print("  " + "-" * 65)
    print()

    # Detailed threshold table for the most favorable scenario
    print("  DETAILED: SPL THRESHOLDS FOR SOFT+LARGE MODEL")
    print("  " + "-" * 60)
    print(f"  {'PIEZO thresh':>14} {'Q=2':>10} {'Q=5':>10} {'Q=10':>10} {'Q=20':>10}")
    print("  " + "-" * 60)
    for thresh in [0.5, 1.0, 1.5, 2.0]:
        vals = []
        for Q in [2, 5, 10, 20]:
            spl = find_piezo_activation_threshold(f_target, Q, thresh, params)
            vals.append(f"{spl:.1f}")
        print(f"  {thresh:>10.1f} um  {'':>2}{'':>2}".rstrip() +
              f"  {vals[0]:>8}  {vals[1]:>8}  {vals[2]:>8}  {vals[3]:>8}")
    print("  " + "-" * 60)
    print()

    # Pressure analysis — can resonant displacement create defecation-relevant pressure?
    print("  RESONANT INTERNAL PRESSURE AT VARIOUS SPL (f=7 Hz)")
    print("  " + "-" * 65)
    print(f"  {'SPL(dB)':>8} {'Disp(um)':>10} {'Q=5 P(mmHg)':>14} {'Q=10 P(mmHg)':>14}")
    print("  " + "-" * 65)
    for spl in [100, 110, 120, 130, 140, 150]:
        for Q_val in [5.0]:
            # Displacement at resonance
            p_ref = 20e-6
            p = p_ref * 10**(spl / 20)
            v = p / (params.rho_tissue * params.c_tissue)
            xi_free = v / (2 * np.pi * 7.0)
            xi_res = xi_free * Q_val * 1e6  # μm

            p5 = pressure_from_displacement(xi_res, 7.0, 5.0, params)
            p10 = pressure_from_displacement(xi_res, 7.0, 10.0, params)
            print(f"  {spl:>8} {xi_res:>10.3f} {p5:>14.4f} {p10:>14.4f}")
    print("  " + "-" * 65)
    print(f"  Defecation reflex threshold: 5-15 mmHg")
    print()

    # Summary
    print("  " + "=" * 65)
    print("  SUMMARY OF KEY FINDINGS")
    print("  " + "=" * 65)
    print()
    print("  1. RESONANCE OVERLAP: The abdominal cavity (with relaxed")
    print("     musculature or large body habitus) has natural frequencies")
    print(f"     of {f_soft:.1f}-{f_target:.1f} Hz — overlapping the 5-10 Hz 'brown note' range.")
    print()

    spl_best = find_piezo_activation_threshold(f_target, 10.0, 0.5, params)
    spl_typ = find_piezo_activation_threshold(f_target, 5.0, 1.0, params)
    print(f"  2. PIEZO ACTIVATION: Minimum SPL for PIEZO channel activation:")
    print(f"     Best case  (Q=10, 0.5um threshold): {spl_best:.1f} dB")
    print(f"     Typical    (Q=5,  1.0um threshold): {spl_typ:.1f} dB")
    print(f"     For reference: 120 dB = threshold of pain")
    print(f"                    130 dB = jet engine at 30m")
    print(f"                    140 dB = near jet engine / firearms")
    print()
    print("  3. MECHANISM CHAIN:")
    print("     Infrasound (5-10 Hz, >120 dB SPL)")
    print("       -> Resonant amplification in abdominal cavity")
    print("       -> Micrometer-scale tissue displacement")
    print("       -> PIEZO1/PIEZO2 mechanosensitive channel activation")
    print("       -> Intracellular Ca2+ influx")
    print("       -> Vagal afferent nerve stimulation")
    print("       -> Potential GI motility modulation")
    print()
    print("  4. CONCLUSION: A plausible mechanotransduction pathway EXISTS")
    print("     but requires extreme SPL (>120 dB). The 'brown note' as")
    print("     popularly described (causing effects at moderate volumes)")
    print("     remains unsupported. However, at occupationally-relevant")
    print("     extreme levels, resonance-mediated PIEZO activation is")
    print("     quantitatively feasible.")
    print()
