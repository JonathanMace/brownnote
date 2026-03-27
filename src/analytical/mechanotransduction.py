"""
Mechanotransduction pathway analysis for infrasound-induced GI effects.

UPDATED TO V2 MODEL — uses corrected flexural mode physics.

Connects:
  1. Acoustic pressure (SPL) → tissue displacement (via v2 flexural modes)
  2. Tissue displacement → PIEZO channel activation
  3. PIEZO activation → neural signaling → reflex potential

Key thresholds (from literature):
  - PIEZO1/PIEZO2 activation: 0.5-2.0 μm displacement (cell-level)
  - Defecation reflex: 5-15 mmHg rectal distension pressure
  - Vagal afferent activation: ~1-5 μm tissue strain

References:
  - Zeitzschel & Lechner (2024) Channels 18(1):2355123
  - Frontiers Physiol (2024) 15:1356317 — PIEZO in intestinal tract
  - ISO 2631-1:1997 — Whole-body vibration
  - Coste et al. (2010) Science 330(6000):55-60 — PIEZO1 discovery
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2, breathing_mode_v2,
)


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


def find_piezo_activation_threshold_v2(
    model: AbdominalModelV2,
    mode_n: int = 2,
    piezo_threshold_um: float = 1.0,
) -> float:
    """
    Find the minimum SPL (dB) at resonance needed to produce tissue
    displacement exceeding the PIEZO channel threshold, using v2 physics.

    Uses (ka)^n coupling for airborne path.
    Returns SPL in dB.
    """
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    R = model.equivalent_sphere_radius
    ka = 2 * np.pi * f_n * R / 343.0

    # Modal stiffness
    D = model.D
    E, h, nu = model.E, model.h, model.nu
    n = mode_n
    K_bend = n*(n-1)*(n+2)**2 * D / R**4
    lam_n = (n**2+n-2+2*nu)/(n**2+n+1-nu)
    K_memb = E*h/R**2 * lam_n
    K_pre = model.P_iap/R * (n-1)*(n+2)
    K_total = K_bend + K_memb + K_pre

    # At resonance: xi = p_eff / K_total * Q = p_inc * (ka)^n / K_total * Q
    # Solve for p_inc:
    target_xi = piezo_threshold_um * 1e-6
    p_required = target_xi * K_total / (model.Q * ka**n)

    p_ref = 20e-6
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
    # Dynamic pressure from oscillating fluid mass
    # ΔP = ρ_f × ω² × ξ × R (characteristic length)
    # NOTE: Do NOT multiply by Q here — the caller provides the
    # already-resonant displacement. Q amplification is in the input.
    R_char = 0.16  # characteristic abdominal radius [m]
    delta_p = params.rho_tissue * (2 * np.pi * freq)**2 * xi_m * R_char

    # Convert Pa to mmHg (1 mmHg = 133.322 Pa)
    return delta_p / 133.322


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("  BROWNTONE — Mechanotransduction Pathway Analysis (v2)")
    print("  Can infrasound activate PIEZO channels in the intestinal wall?")
    print("=" * 70)
    print()

    params = MechanotransductionParams()

    # Use v2 model
    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    freqs = flexural_mode_frequencies_v2(model, n_max=6)
    f_breathe = breathing_mode_v2(model)
    f_n2 = freqs[2]
    R = model.equivalent_sphere_radius
    Q = model.Q

    print("  ABDOMINAL MODEL RESONANCES (v2 corrected)")
    print("  " + "-" * 50)
    print(f"    Breathing mode (n=0):  {f_breathe:.0f} Hz (KILOHERTZ — not infrasound!)")
    print(f"    Flexural n=2:          {f_n2:.2f} Hz")
    print(f"    Flexural n=3:          {freqs[3]:.2f} Hz")
    print(f"    Flexural n=4:          {freqs[4]:.2f} Hz")
    print()

    # PIEZO activation thresholds with v2 physics
    print("  AIRBORNE SPL FOR PIEZO ACTIVATION (v2 with (ka)^n coupling)")
    print("  " + "-" * 65)
    print(f"  {'Mode':>8} {'f(Hz)':>8} {'ka':>8} {'(ka)^n':>10} {'SPL 0.5μm':>10} {'SPL 1.0μm':>10}")
    print("  " + "-" * 65)

    for n in [2, 3, 4]:
        f = freqs[n]
        ka = 2 * np.pi * f * R / 343.0
        spl_05 = find_piezo_activation_threshold_v2(model, mode_n=n, piezo_threshold_um=0.5)
        spl_10 = find_piezo_activation_threshold_v2(model, mode_n=n, piezo_threshold_um=1.0)
        print(f"  {'n='+str(n):>8} {f:>8.2f} {ka:>8.4f} {ka**n:>10.2e} {spl_05:>10.1f} {spl_10:>10.1f}")

    print("  " + "-" * 65)
    print("  For reference: 120 dB = threshold of pain, 140 dB = near jet engine")
    print()

    # Sensitivity to E
    print("  SENSITIVITY: SPL for 1 μm vs. tissue stiffness")
    print("  " + "-" * 55)
    for E_MPa in [0.05, 0.1, 0.2, 0.5, 1.0]:
        m = AbdominalModelV2(E=E_MPa*1e6, a=0.18, b=0.18, c=0.12)
        f2 = flexural_mode_frequencies_v2(m, n_max=2)[2]
        spl = find_piezo_activation_threshold_v2(m, mode_n=2, piezo_threshold_um=1.0)
        print(f"    E={E_MPa:.2f} MPa: f2={f2:.1f} Hz, SPL(1μm)={spl:.1f} dB")
    print("  " + "-" * 55)
    print()

    # Comparison: airborne displacement at 120 dB for each mode
    print("  AIRBORNE DISPLACEMENT AT 120 dB SPL")
    print("  " + "-" * 55)
    p_120 = 20e-6 * 10**(120/20)
    for n in [2, 3, 4]:
        f = freqs[n]
        ka = 2 * np.pi * f * R / 343.0
        p_eff = p_120 * ka**n

        D = model.D
        E_val, h, nu = model.E, model.h, model.nu
        K_b = n*(n-1)*(n+2)**2 * D / R**4
        lam = (n**2+n-2+2*nu)/(n**2+n+1-nu)
        K_m = E_val*h/R**2*lam
        K_p = model.P_iap/R*(n-1)*(n+2)
        K_tot = K_b + K_m + K_p

        xi = p_eff / K_tot * Q * 1e6

        piezo = "✓ YES" if xi > 0.5 else "✗ below"
        print(f"    n={n}: f={f:.1f} Hz, ξ={xi:.4f} μm  PIEZO: {piezo}")

    print("  " + "-" * 55)
    print()

    # Summary
    print("  " + "=" * 65)
    print("  CONCLUSIONS (v2)")
    print("  " + "=" * 65)
    print()
    print("  The v2 model with corrected physics gives dramatically different")
    print("  results from v1:")
    print()
    print("  1. The breathing mode is at ~2900 Hz, NOT in the infrasound range.")
    print("     The 'cavity resonance at 7 Hz' idea was based on an error.")
    print()
    print("  2. Flexural modes (n≥2) ARE at 4-10 Hz for soft tissue. These")
    print("     match ISO 2631 data and ARE the relevant modes for vibration.")
    print()
    print("  3. Airborne acoustic coupling to flexural modes is NEGLIGIBLE:")
    spl_target = find_piezo_activation_threshold_v2(model, mode_n=2, piezo_threshold_um=1.0)
    print(f"     Need {spl_target:.0f} dB SPL for 1 μm displacement via n=2 mode.")
    print("     This is beyond any realistic acoustic exposure.")
    print()
    print("  4. The popularly described 'brown note' via loudspeaker is")
    print("     IMPLAUSIBLE based on fundamental acoustic physics.")
    print()
    print("  5. Whole-body vibration (mechanical pathway) is the REAL mechanism")
    print("     for GI effects at 5-10 Hz, consistent with epidemiological data.")
    print()
