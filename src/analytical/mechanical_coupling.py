"""
Mechanical (whole-body) vibration coupling model.

Models how ground/seat vibration transmits through the skeleton to
excite flexural modes of the abdominal cavity — the pathway that
ACTUALLY explains ISO 2631 effects.

Unlike airborne acoustic coupling (which suffers a (ka)^n penalty),
mechanical vibration couples DIRECTLY to the body at full amplitude.
The only attenuation is from the body's transfer function (transmissibility).

This is the physiologically relevant excitation mechanism for 5-10 Hz.

References:
    - ISO 2631-1:1997 — Evaluation of human exposure to whole-body vibration
    - Griffin, M.J. (1990) "Handbook of Human Vibration"
    - Kitazaki, S. & Griffin, M.J. (1998) "Resonance behaviour of the
      seated human body" J. Biomechanics 31(2):143-149
    - Mansfield, N.J. (2005) "Human Response to Vibration"
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2,
)


@dataclass
class WBVExposure:
    """Whole-body vibration exposure parameters."""
    # Vibration input
    acceleration_rms_ms2: float = 1.0   # acceleration [m/s²] RMS
    frequency_hz: float = 7.0           # excitation frequency [Hz]

    # Body transmissibility (from ISO 2631 / Griffin)
    # Seat-to-abdomen transmissibility at resonance ≈ 1.5-2.5
    transmissibility: float = 2.0

    @property
    def displacement_amplitude_m(self) -> float:
        """Peak displacement from RMS acceleration."""
        omega = 2 * np.pi * self.frequency_hz
        # a_rms = ω² × x_peak / √2, so x_peak = a_rms × √2 / ω²
        return self.acceleration_rms_ms2 * np.sqrt(2) / omega**2

    @property
    def displacement_amplitude_um(self) -> float:
        return self.displacement_amplitude_m * 1e6

    @property
    def velocity_amplitude_ms(self) -> float:
        """Peak velocity from RMS acceleration."""
        omega = 2 * np.pi * self.frequency_hz
        return self.acceleration_rms_ms2 * np.sqrt(2) / omega


# Published seat-to-viscera transmissibility data
# From Kitazaki & Griffin (1998), Mansfield (2005), ISO 2631
# Format: (frequency_hz, transmissibility_ratio)
ISO_2631_TRANSMISSIBILITY = np.array([
    # Freq(Hz), T_abdomen (approximate, seated, z-axis)
    [1.0,  1.0],
    [2.0,  1.1],
    [3.0,  1.3],
    [4.0,  1.7],
    [5.0,  2.2],   # approaching abdominal resonance
    [6.0,  2.5],   # near peak
    [7.0,  2.3],   # near peak
    [8.0,  1.8],   # past peak
    [10.0, 1.2],
    [12.0, 0.9],
    [15.0, 0.7],
    [20.0, 0.5],
])


def interpolate_transmissibility(freq_hz: float) -> float:
    """Interpolate seat-to-abdomen transmissibility from ISO 2631 data."""
    return float(np.interp(
        freq_hz,
        ISO_2631_TRANSMISSIBILITY[:, 0],
        ISO_2631_TRANSMISSIBILITY[:, 1],
    ))


def mechanical_excitation_response(
    exposure: WBVExposure,
    model: AbdominalModelV2,
    mode_n: int = 2,
    use_empirical: bool = False,
) -> dict:
    """
    Compute abdominal cavity response to mechanical (whole-body) vibration.

    Two approaches, selectable via use_empirical:
      - Theoretical: Use our modal model's base excitation FRF.
        x_rel = x_base × H_modal(f)
      - Empirical: Use ISO 2631 transmissibility data.
        x_abdomen = x_base × T(f)  (absolute abdomen displacement)

    IMPORTANT: These must NOT be multiplied together — they measure
    the same amplification effect from different sources.
    """
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    omega_n = 2 * np.pi * f_n
    omega = 2 * np.pi * exposure.frequency_hz

    x_base = exposure.displacement_amplitude_m

    zeta = model.damping_ratio
    r = omega / omega_n if omega_n > 0 else 0

    # Base excitation relative displacement FRF:
    # H_rel = r² / sqrt((1-r²)² + (2ζr)²)
    if omega_n > 0:
        H_rel = r**2 / np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
    else:
        H_rel = 0

    if use_empirical:
        # Empirical transmissibility from ISO 2631
        T = interpolate_transmissibility(exposure.frequency_hz)
        # Empirical T gives total displacement; relative ≈ (T-1) × x_base
        x_abdomen_abs = T * x_base
        x_rel = (T - 1) * x_base  # relative to skeleton
        amplification = T
    else:
        # Theoretical modal model
        T = None
        x_rel = x_base * H_rel
        # Absolute transmissibility: T_abs = sqrt((1 + (2ζr)²) / ((1-r²)² + (2ζr)²))
        # NOT simply 1 + H_rel (which incorrectly adds magnitudes of complex quantities)
        T_abs = np.sqrt((1 + (2*zeta*r)**2) / ((1 - r**2)**2 + (2*zeta*r)**2))
        x_abdomen_abs = x_base * T_abs
        amplification = H_rel

    R = model.equivalent_sphere_radius
    eps_membrane = x_rel / R
    eps_bending = (model.h / (2 * R**2)) * x_rel

    a_rel = x_rel * omega**2
    delta_P = model.rho_fluid * a_rel * R
    delta_P_mmHg = delta_P / 133.322

    return {
        'frequency_hz': exposure.frequency_hz,
        'mode_n': mode_n,
        'mode_freq_hz': f_n,
        'base_acceleration_ms2': exposure.acceleration_rms_ms2,
        'base_displacement_um': exposure.displacement_amplitude_um,
        'method': 'empirical' if use_empirical else 'theoretical',
        'amplification': amplification,
        'modal_H_rel': H_rel,
        'iso_T': interpolate_transmissibility(exposure.frequency_hz),
        'relative_displacement_um': x_rel * 1e6,
        'abdomen_absolute_um': x_abdomen_abs * 1e6,
        'membrane_strain': eps_membrane,
        'bending_strain': eps_bending,
        'internal_pressure_Pa': delta_P,
        'internal_pressure_mmHg': delta_P_mmHg,
        'exceeds_piezo_threshold': x_rel * 1e6 > 0.5,
    }


def compare_airborne_vs_mechanical(
    model: AbdominalModelV2,
    mode_n: int = 2,
) -> dict:
    """
    Side-by-side comparison of airborne acoustic vs mechanical vibration
    coupling to abdominal flexural modes.
    """
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    R = model.equivalent_sphere_radius

    results = {}

    # Mechanical: typical occupational exposure
    # EU Action Value: 0.5 m/s² RMS, Limit: 1.15 m/s² (ISO 2631)
    for a_rms in [0.5, 1.0, 1.15, 2.0, 5.0]:
        T = interpolate_transmissibility(f_n)
        exposure = WBVExposure(
            acceleration_rms_ms2=a_rms,
            frequency_hz=f_n,
            transmissibility=T,
        )
        r = mechanical_excitation_response(exposure, model, mode_n)
        results[f'mech_{a_rms}'] = r

    # Airborne: equivalent comparison
    # What SPL produces equivalent displacement?
    for spl in [100, 120, 130, 140]:
        p_ref = 20e-6
        p = p_ref * 10**(spl/20)
        ka = 2 * np.pi * f_n * R / 343.0
        p_eff = p * ka**mode_n  # (ka)^n coupling

        # Modal stiffness
        E, h, nu = model.E, model.h, model.nu
        D = model.D
        K_bend = mode_n * (mode_n-1) * (mode_n+2)**2 * D / R**4
        lambda_n = (mode_n**2+mode_n-2+2*nu)/(mode_n**2+mode_n+1-nu)
        K_memb = E * h / R**2 * lambda_n
        K_pre = model.P_iap / R * (mode_n-1) * (mode_n+2)
        K_total = K_bend + K_memb + K_pre

        # At resonance: displacement = p_eff / K_total × Q
        xi = p_eff / K_total * model.Q

        results[f'air_{spl}'] = {
            'spl_db': spl,
            'displacement_um': xi * 1e6,
            'pressure_pa': p,
            'effective_pressure_pa': p_eff,
        }

    return results


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE — Mechanical vs Airborne Coupling Comparison")
    print("=" * 72)
    print()

    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    freqs = flexural_mode_frequencies_v2(model, n_max=4)
    f2 = freqs[2]

    print(f"  Model: soft tissue (E=0.1 MPa, a=18cm)")
    print(f"  n=2 flexural mode: {f2:.2f} Hz")
    print(f"  Q = {model.Q:.1f} (tan δ = {model.loss_tangent})")
    print()

    # === THEORETICAL MODEL ===
    print("  THEORETICAL MODEL: Base Excitation FRF")
    print("  " + "-" * 65)
    print(f"  {'a_rms(m/s²)':>12} {'x_base(μm)':>12} {'H_rel':>8} {'x_rel(μm)':>12} "
          f"{'ΔP(mmHg)':>10} {'PIEZO?':>8}")
    print("  " + "-" * 65)

    for a_rms in [0.1, 0.5, 1.0, 1.15, 2.0, 5.0]:
        exp = WBVExposure(acceleration_rms_ms2=a_rms, frequency_hz=f2)
        r = mechanical_excitation_response(exp, model, mode_n=2, use_empirical=False)
        piezo = "YES" if r['exceeds_piezo_threshold'] else "no"
        print(f"  {a_rms:>12.2f} {r['base_displacement_um']:>12.1f} "
              f"{r['modal_H_rel']:>8.3f} {r['relative_displacement_um']:>12.2f} "
              f"{r['internal_pressure_mmHg']:>10.4f} {piezo:>8}")

    print("  " + "-" * 65)
    print()

    # === EMPIRICAL ISO 2631 ===
    print("  EMPIRICAL: ISO 2631 Transmissibility")
    print("  " + "-" * 65)
    print(f"  {'a_rms(m/s²)':>12} {'x_base(μm)':>12} {'T':>8} {'x_rel(μm)':>12} "
          f"{'ΔP(mmHg)':>10} {'PIEZO?':>8}")
    print("  " + "-" * 65)

    for a_rms in [0.1, 0.5, 1.0, 1.15, 2.0, 5.0]:
        exp = WBVExposure(acceleration_rms_ms2=a_rms, frequency_hz=f2)
        r = mechanical_excitation_response(exp, model, mode_n=2, use_empirical=True)
        piezo = "YES" if r['exceeds_piezo_threshold'] else "no"
        print(f"  {a_rms:>12.2f} {r['base_displacement_um']:>12.1f} "
              f"{r['iso_T']:>8.2f} {r['relative_displacement_um']:>12.2f} "
              f"{r['internal_pressure_mmHg']:>10.4f} {piezo:>8}")

    print("  " + "-" * 65)
    print(f"  EU WBV Action Value: 0.5 m/s², Limit: 1.15 m/s²")
    print()

    # === TRANSMISSIBILITY COMPARISON ===
    print("  MODEL vs ISO 2631 TRANSMISSIBILITY")
    print("  " + "-" * 55)
    print(f"  {'f(Hz)':>8} {'ISO T':>8} {'Model H_rel':>12} {'Model T_abs':>12}")
    print("  " + "-" * 55)
    for f in [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20]:
        T_iso = interpolate_transmissibility(f)
        omega = 2 * np.pi * f
        omega_n = 2 * np.pi * f2
        zeta = model.damping_ratio
        rat = omega / omega_n
        H = rat**2 / np.sqrt((1-rat**2)**2 + (2*zeta*rat)**2)
        T_model = 1 + H  # absolute transmissibility (approx)
        print(f"  {f:>8.1f} {T_iso:>8.2f} {H:>12.3f} {T_model:>12.3f}")
    print("  " + "-" * 55)
    print()

    # === AIRBORNE COMPARISON ===
    print("  AIRBORNE ACOUSTIC (for comparison)")
    print("  " + "-" * 55)
    R = model.equivalent_sphere_radius
    for spl in [100, 110, 120, 130, 140, 150]:
        p = 20e-6 * 10**(spl/20)
        ka = 2 * np.pi * f2 * R / 343.0
        p_eff = p * ka**2

        D = model.D
        E, h, nu = model.E, model.h, model.nu
        K_b = 2*(2-1)*(2+2)**2 * D / R**4
        lam = (4+2-2+2*nu)/(4+2+1-nu)
        K_m = E*h/R**2*lam
        K_p = model.P_iap/R*(2-1)*(2+2)
        K_tot = K_b + K_m + K_p

        xi = p_eff / K_tot * model.Q * 1e6
        print(f"    SPL={spl} dB → p={p:.1f} Pa → p_eff={p_eff:.4f} Pa → ξ={xi:.4f} μm")
    print("  " + "-" * 55)
    print()

    print("  " + "=" * 65)
    print("  CONCLUSION")
    print("  " + "=" * 65)
    print()
    print("  At the EU WBV limit (1.15 m/s²) at n=2 resonance:")
    exp = WBVExposure(acceleration_rms_ms2=1.15, frequency_hz=f2)
    r_theory = mechanical_excitation_response(exp, model, mode_n=2, use_empirical=False)
    r_emp = mechanical_excitation_response(exp, model, mode_n=2, use_empirical=True)
    print(f"    Theoretical: x_rel = {r_theory['relative_displacement_um']:.1f} μm")
    print(f"    Empirical:   x_rel = {r_emp['relative_displacement_um']:.1f} μm")
    print(f"    PIEZO threshold: 0.5-2.0 μm")
    print()
    print("  Airborne at 120 dB: ~0.14 μm (below PIEZO threshold)")
    print()
    print("  Mechanical coupling is vastly more efficient than airborne.")
    print("  The 'brown note' via loudspeaker is implausible at safe SPL.")
    print("  WBV → GI effects at 5-10 Hz are consistent with PIEZO activation.")
    print()
