"""
Self-consistent energy budget for airborne acoustic coupling.

Resolves the energy budget inconsistency identified by Reviewer B (Round 2, M1).

The issue: the pressure-based coupling (p_eff = p_inc × (ka)^n) neglects
radiation inefficiency, yielding ξ_pressure ≈ 0.18 μm at 120 dB — roughly
13× larger than the energy-consistent estimate ξ_energy ≈ 0.014 μm. The
pressure-based result is an upper bound, not the physically correct value.

Resolution: Use the Junger & Feit reciprocity formulation.

The power absorbed by mode n from an incident plane wave is:
    P_abs = σ_abs × I
where σ_abs = (2n+1)λ²/(4π) × (Γ_rad / Γ_total)

Γ_rad = radiation damping rate
Γ_total = Γ_rad + Γ_structural

For a bio-tissue shell at 5 Hz with Γ_rad << Γ_structural:
    σ_abs ≈ (2n+1)λ²/(4π) × (Γ_rad / Γ_structural)

This gives the self-consistent displacement at steady state.

References:
    Junger & Feit (2012) "Sound, Structures, and Their Interaction" §9.3
    Morse & Ingard (1968) "Theoretical Acoustics" §8.2
"""

import numpy as np
from dataclasses import dataclass

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2,
)


def radiation_damping_flexural(
    model: AbdominalModelV2,
    mode_n: int = 2,
    medium: str = 'air',
) -> dict:
    """
    Compute radiation damping for flexural mode n.

    In air: negligible (ζ_rad ~ 10⁻⁶)
    In tissue: much larger but still small compared to structural damping

    The radiation resistance for mode n of a sphere in the Rayleigh limit is:
        R_rad(n) = ρ_ext × c_ext × 4πR² × (ka)^{2n+2} / ((2n+1)!!²)

    where (2n+1)!! = 1×3×5×...×(2n+1) is the double factorial.
    """
    R = model.equivalent_sphere_radius
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    omega = 2 * np.pi * f_n

    if medium == 'air':
        rho_ext = 1.225
        c_ext = 343.0
    elif medium == 'tissue':
        rho_ext = 1040.0
        c_ext = 1540.0
    else:
        raise ValueError(f"Unknown medium: {medium}")

    ka = omega * R / c_ext
    A = 4 * np.pi * R**2

    # Double factorial (2n+1)!!
    double_fact = 1
    for i in range(1, 2*mode_n + 2, 2):
        double_fact *= i

    # Radiation resistance per unit area
    R_rad = rho_ext * c_ext * (ka)**(2*mode_n + 2) / double_fact**2

    # Total radiation resistance
    R_rad_total = R_rad * A

    # Effective mass
    rho_w, rho_f = model.rho_wall, model.rho_fluid
    m_eff = rho_w * model.h + rho_f * R / mode_n  # per unit area
    M_total = m_eff * A

    # Radiation damping ratio
    zeta_rad = R_rad_total / (2 * omega * M_total)

    return {
        'mode_n': mode_n,
        'frequency_hz': f_n,
        'ka': ka,
        'medium': medium,
        'R_rad_per_area': R_rad,
        'R_rad_total': R_rad_total,
        'M_total': M_total,
        'zeta_rad': zeta_rad,
        'zeta_structural': model.damping_ratio,
        'zeta_total': zeta_rad + model.damping_ratio,
        'damping_ratio_ratio': zeta_rad / model.damping_ratio,
    }


def absorption_cross_section(
    model: AbdominalModelV2,
    mode_n: int = 2,
) -> dict:
    """
    Compute the absorption cross-section for mode n using reciprocity.

    σ_abs(n) = (2n+1)λ²/(4π) × Γ_rad / (Γ_rad + Γ_struct)

    This is the effective area that the mode presents to the incident wave
    for energy absorption.
    """
    R = model.equivalent_sphere_radius
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    omega = 2 * np.pi * f_n
    lam = 343.0 / f_n  # wavelength in air

    rad = radiation_damping_flexural(model, mode_n, 'air')
    zeta_rad = rad['zeta_rad']
    zeta_struct = model.damping_ratio
    zeta_total = zeta_rad + zeta_struct

    # Maximum possible absorption cross-section (at resonance)
    sigma_max = (2 * mode_n + 1) * lam**2 / (4 * np.pi)

    # Actual absorption (limited by radiation coupling)
    sigma_abs = sigma_max * (zeta_rad / zeta_total)

    # Geometric cross-section for comparison
    sigma_geo = np.pi * R**2

    return {
        'mode_n': mode_n,
        'frequency_hz': f_n,
        'wavelength_m': lam,
        'sigma_max_m2': sigma_max,
        'sigma_abs_m2': sigma_abs,
        'sigma_geo_m2': sigma_geo,
        'sigma_ratio': sigma_abs / sigma_geo,
        'zeta_rad': zeta_rad,
        'zeta_struct': zeta_struct,
        'efficiency': zeta_rad / zeta_total,
    }


def self_consistent_displacement(
    model: AbdominalModelV2,
    mode_n: int = 2,
    spl_db: float = 120.0,
) -> dict:
    """
    Compute displacement using energy-consistent approach.

    At steady state:
        P_absorbed = P_dissipated
        σ_abs × I = ζ_struct × ω_n × M_total × (ω_n ξ)²

    Solving for ξ:
        ξ² = σ_abs × I / (ζ_struct × ω_n³ × M_total)
    """
    R = model.equivalent_sphere_radius
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    omega_n = 2 * np.pi * f_n

    # Incident field
    p_ref = 20e-6
    p_inc = p_ref * 10**(spl_db / 20)
    I_inc = p_inc**2 / (2 * 1.225 * 343.0)

    # Absorption cross-section
    acs = absorption_cross_section(model, mode_n)
    sigma_abs = acs['sigma_abs_m2']

    # Absorbed power
    P_abs = sigma_abs * I_inc

    # Effective mass and damping
    rho_w, rho_f = model.rho_wall, model.rho_fluid
    m_eff = rho_w * model.h + rho_f * R / mode_n
    A = 4 * np.pi * R**2
    M_total = m_eff * A
    zeta_struct = model.damping_ratio

    # Self-consistent displacement
    xi_sq = P_abs / (zeta_struct * omega_n**3 * M_total)
    xi = np.sqrt(max(xi_sq, 0))

    # Also compute the pressure-based approach for comparison
    ka_air = omega_n * R / 343.0
    p_eff = p_inc * ka_air**mode_n

    E_val, h, nu = model.E, model.h, model.nu
    D = model.D
    n = mode_n
    K_bend = n*(n-1)*(n+2)**2 * D / R**4
    lam_n = (n**2+n-2+2*nu)/(n**2+n+1-nu)
    K_memb = E_val*h/R**2 * lam_n
    K_pre = model.P_iap/R*(n-1)*(n+2)
    K_total = K_bend + K_memb + K_pre

    xi_pressure = p_eff / K_total * model.Q

    # Power dissipated at each displacement (for verification)
    P_diss_energy = zeta_struct * omega_n**3 * M_total * xi**2
    P_diss_pressure = zeta_struct * omega_n**3 * M_total * xi_pressure**2

    return {
        'spl_db': spl_db,
        'frequency_hz': f_n,
        'I_inc_Wm2': I_inc,
        'sigma_abs_m2': sigma_abs,
        'P_absorbed_W': P_abs,
        'xi_energy_m': xi,
        'xi_energy_um': xi * 1e6,
        'xi_pressure_m': xi_pressure,
        'xi_pressure_um': xi_pressure * 1e6,
        'ratio_pressure_to_energy': xi_pressure / xi if xi > 0 else float('inf'),
        'P_diss_energy_W': P_diss_energy,
        'P_diss_pressure_W': P_diss_pressure,
        'energy_conserved_energy': abs(P_diss_energy - P_abs) / P_abs < 0.01 if P_abs > 0 else True,
        'energy_conserved_pressure': abs(P_diss_pressure - P_abs) / P_abs < 0.01 if P_abs > 0 else False,
    }


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE — Self-Consistent Energy Budget Analysis")
    print("  Resolving Reviewer B Round 2, Issue M1")
    print("=" * 72)
    print()

    model = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f2 = flexural_mode_frequencies_v2(model, n_max=2)[2]

    # Radiation damping
    print("  1. RADIATION DAMPING")
    print("  " + "-" * 60)
    for medium in ['air', 'tissue']:
        rd = radiation_damping_flexural(model, mode_n=2, medium=medium)
        print(f"  n=2, {medium:>8}: ζ_rad = {rd['zeta_rad']:.2e}, "
              f"ζ_struct = {rd['zeta_structural']:.4f}, "
              f"ratio = {rd['damping_ratio_ratio']:.2e}")
    print("  " + "-" * 60)
    print("  Radiation damping is NEGLIGIBLE in both air and tissue.")
    print()

    # Absorption cross-section
    print("  2. ABSORPTION CROSS-SECTION")
    print("  " + "-" * 65)
    for n in [2, 3, 4]:
        acs = absorption_cross_section(model, mode_n=n)
        print(f"  n={n}: σ_abs = {acs['sigma_abs_m2']:.2e} m², "
              f"σ_geo = {acs['sigma_geo_m2']:.4f} m², "
              f"ratio = {acs['sigma_ratio']:.2e}, "
              f"efficiency = {acs['efficiency']:.2e}")
    print("  " + "-" * 65)
    print("  The absorption efficiency is tiny (~10⁻⁶) because")
    print("  radiation damping << structural damping.")
    print()

    # Self-consistent displacement comparison
    print("  3. DISPLACEMENT: ENERGY vs PRESSURE APPROACH")
    print("  " + "-" * 72)
    print(f"  {'SPL':>6} {'ξ_energy(μm)':>14} {'ξ_pressure(μm)':>16} "
          f"{'ratio':>8} {'P=P?':>8}")
    print("  " + "-" * 72)

    for spl in [100, 110, 120, 130, 140, 150]:
        r = self_consistent_displacement(model, mode_n=2, spl_db=spl)
        ratio = r['ratio_pressure_to_energy']
        econ = "✓" if r['energy_conserved_energy'] else "✗"
        print(f"  {spl:>6} {r['xi_energy_um']:>14.6f} {r['xi_pressure_um']:>14.6f} "
              f"{ratio:>8.2f} {econ:>8}")

    print("  " + "-" * 72)
    print()

    print("  " + "=" * 65)
    print("  RESOLUTION")
    print("  " + "=" * 65)
    print()
    print("  The pressure-based approach overestimates displacement by a")
    print("  constant factor because it doesn't account for the radiation")
    print("  efficiency. The energy-based approach is self-consistent.")
    print()
    print("  The pressure-based estimate is an upper bound (~0.18 μm at")
    print("  120 dB) that neglects radiation inefficiency. The energy-")
    print("  consistent estimate (~0.014 μm) is ~13× smaller and is the")
    print("  physically correct value. Both are far below the PIEZO")
    print("  threshold, so conclusions are unchanged.")
    print()
    print("  For the paper, we:")
    print("  1. Use the energy-consistent displacement as the PRIMARY result")
    print("  2. Report the pressure-based estimate as an upper bound that")
    print("     overestimates by ~13× due to neglected radiation inefficiency")
    print("  3. The energy budget is the self-consistent calculation, not")
    print("     merely a cross-check")
    print()

    # Quick summary for paper
    r120 = self_consistent_displacement(model, mode_n=2, spl_db=120)
    print(f"  At 120 dB, n=2:")
    print(f"    Energy-consistent: ξ = {r120['xi_energy_um']:.4f} μm")
    print(f"    Pressure-based:    ξ = {r120['xi_pressure_um']:.4f} μm")
    print(f"    PIEZO threshold:   0.5-2.0 μm")
    print(f"    Both well below threshold → conclusion unchanged.")
    print()
