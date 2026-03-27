"""
Acoustic-structure coupling model for a shell in a long-wavelength pressure field.

This module properly handles the physics of how airborne infrasound couples
into the abdominal cavity shell model. Key insight: in the long-wavelength
limit (body << wavelength), the FULL incident pressure acts on the shell.

Physics:
    At 7 Hz, wavelength in air = c/f = 343/7 ≈ 49 m.
    Body dimension ≈ 0.3 m → ka ≈ 2π·0.15/49 ≈ 0.019 << 1.

    In this limit:
    - The scattered field is negligible (Rayleigh scattering regime)
    - The incident pressure acts uniformly on the shell surface
    - For the breathing mode (n=0), the shell responds as a spherical
      pressure vessel to the oscillating external pressure
    - The shell's mechanical impedance determines the response,
      NOT the acoustic impedance mismatch

    The impedance mismatch IS relevant for:
    - How much energy the shell absorbs from the sound field
    - The radiation damping of the shell vibration
    - But NOT the amplitude of the driving force

    Think of it like pushing a pendulum with your hand: the driving
    force is your hand's force, not the "impedance mismatch" between
    your hand and the pendulum.

References:
    - Junger, M.C. & Feit, D. "Sound, Structures, and Their Interaction"
      Ch. 7-9 (acoustic loading of shells)
    - Morse, P.M. & Ingard, K.U. "Theoretical Acoustics" Ch. 8
      (scattering from obstacles)
    - Fahy, F.J. "Sound and Structural Vibration" (radiation and coupling)
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency import AbdominalModel, breathing_mode_frequency


# Physical constants
RHO_AIR = 1.225      # kg/m³
C_AIR = 343.0         # m/s
Z_AIR = RHO_AIR * C_AIR  # ≈ 420 Pa·s/m


@dataclass
class CouplingResult:
    """Results from acoustic-structure coupling analysis."""
    frequency_hz: float
    spl_db: float
    incident_pressure_pa: float
    ka: float                        # wavenumber × radius (dimensionless)
    shell_displacement_m: float      # shell wall displacement amplitude
    shell_displacement_um: float
    amplification_factor: float      # Q at resonance, H(f) off-resonance
    radiation_damping_ratio: float   # ζ_rad
    total_damping_ratio: float       # ζ_total = ζ_structural + ζ_rad
    effective_Q: float               # 1/(2·ζ_total)
    wall_bending_strain: float       # ε_bending at outer fiber
    wall_membrane_strain: float      # ε_membrane (circumferential)
    is_long_wavelength: bool         # ka << 1?
    energy_absorption_fraction: float  # fraction of incident energy absorbed
    coupling_notes: str


def compute_ka(frequency: float, radius: float) -> float:
    """Dimensionless wavenumber-radius product ka."""
    k = 2 * np.pi * frequency / C_AIR
    return k * radius


def radiation_impedance_sphere(frequency: float, radius: float,
                                rho_ext: float = RHO_AIR,
                                c_ext: float = C_AIR) -> complex:
    """
    Radiation impedance of a pulsating sphere (breathing mode) in a fluid.

    Z_rad = ρc · S · [(ka)² + j·ka] / [1 + (ka)²]

    For ka << 1: Z_rad ≈ ρc · S · [(ka)² + j·ka]
    The real part (radiation resistance) goes as (ka)² — very small for infrasound.
    The imaginary part (radiation reactance) represents added mass of the external fluid.

    Returns complex impedance [Pa·s/m³ · m²] = [kg/s]
    """
    ka = compute_ka(frequency, radius)
    S = 4 * np.pi * radius**2  # surface area of sphere

    Z = rho_ext * c_ext * S * (ka**2 + 1j * ka) / (1 + ka**2)
    return Z


def radiation_damping_ratio(frequency: float, model: AbdominalModel) -> float:
    """
    Compute the radiation damping ratio for the breathing mode.

    The radiation resistance extracts energy from the shell vibration and
    re-radiates it as sound. For ka << 1, this is tiny — the shell is a
    very poor radiator, which also means it's weakly coupled to the sound field.

    ζ_rad = R_rad / (2 · m_eff · ω_n)
    """
    R = model.equivalent_sphere_radius
    Z_rad = radiation_impedance_sphere(frequency, R)
    R_rad = Z_rad.real  # radiation resistance

    # Effective mass of the breathing mode
    m_eff = (model.rho_wall * model.h + model.rho_fluid * R) * 4 * np.pi * R**2

    omega_n = 2 * np.pi * breathing_mode_frequency(model)

    if omega_n > 0 and m_eff > 0:
        return R_rad / (2 * m_eff * omega_n)
    return 0.0


def structural_damping_ratio(loss_tangent: float = 0.3) -> float:
    """
    Convert tissue loss tangent to damping ratio.

    For viscoelastic tissue: tan(δ) = E''/E' = 2ζ (for small damping)
    So ζ = tan(δ)/2

    Published values for soft tissue:
    - Abdominal wall muscle: tan(δ) ≈ 0.15 - 0.40 (Parker et al., 2011)
    - Liver: tan(δ) ≈ 0.2 - 0.5 (Klatt et al., 2007)
    - Fat: tan(δ) ≈ 0.1 - 0.3

    Default: 0.3 (mid-range for abdominal wall composite)
    """
    return loss_tangent / 2


def shell_response_to_pressure(
    frequency: float,
    spl_db: float,
    model: AbdominalModel,
    loss_tangent: float = 0.3,
) -> CouplingResult:
    """
    Compute the shell wall displacement response to an incident acoustic
    pressure field, properly accounting for:

    1. Uniform pressure loading (long-wavelength limit)
    2. Shell mechanical impedance (stiffness + inertia)
    3. Structural damping (from viscoelastic properties)
    4. Radiation damping (energy re-radiated to air)
    5. Frequency response function (amplification at resonance)

    This is the CORRECTED model that replaces the naive
    "free-field displacement × Q" approach.

    The breathing mode responds to uniform pressure as:
        ξ = p_inc / (k_shell - ω²·m_eff + j·ω·c_total)

    where:
        k_shell = membrane stiffness of shell
        m_eff = shell mass + fluid added mass
        c_total = structural damping + radiation damping
    """
    R = model.equivalent_sphere_radius
    E, h, nu = model.E, model.h, model.nu
    rho_w, rho_f = model.rho_wall, model.rho_fluid

    # Incident pressure
    p_ref = 20e-6  # Pa
    p_inc = p_ref * 10**(spl_db / 20)

    # Dimensionless parameter
    ka = compute_ka(frequency, R)

    # Shell breathing mode parameters (per unit area, then integrated)
    # Membrane stiffness per unit area: k = 2Eh / [R²(1-ν)]
    k_per_area = 2 * E * h / (R**2 * (1 - nu))

    # Mass per unit area: wall + fluid added mass
    m_per_area = rho_w * h + rho_f * R

    # Natural frequency
    omega_n = np.sqrt(k_per_area / m_per_area)
    f_n = omega_n / (2 * np.pi)

    # Damping
    zeta_struct = structural_damping_ratio(loss_tangent)
    zeta_rad = radiation_damping_ratio(frequency, model)
    zeta_total = zeta_struct + zeta_rad
    Q_eff = 1 / (2 * zeta_total) if zeta_total > 0 else float('inf')

    # Frequency response
    omega = 2 * np.pi * frequency
    r = omega / omega_n  # frequency ratio

    # Complex frequency response function H(ω)
    # ξ = p_inc / k · H(r) where H = 1/[(1-r²) + j·2ζr]
    H_complex = 1 / ((1 - r**2) + 2j * zeta_total * r)
    H_mag = abs(H_complex)

    # Shell displacement (radial, uniform breathing mode)
    # The pressure acts on the shell → displacement = p / k_eff × H
    xi = p_inc / k_per_area * H_mag

    # Wall strains
    # Membrane (circumferential) strain: ε_m = ξ/R
    eps_membrane = xi / R

    # Bending strain at outer fiber: ε_b ≈ (h/2R²) × ξ for breathing mode
    # (this is small for breathing mode; larger for higher modes)
    eps_bending = (h / (2 * R**2)) * xi

    # Energy absorption
    # Power absorbed = radiation resistance × velocity²
    # Power incident on cross-section = (p²/ρc) × πR²
    velocity = xi * omega
    P_absorbed = radiation_impedance_sphere(frequency, R).real * velocity**2 / (4 * np.pi * R**2)
    P_incident = p_inc**2 / (RHO_AIR * C_AIR)
    cross_section = np.pi * R**2
    P_intercepted = P_incident * cross_section

    absorption = P_absorbed / P_intercepted if P_intercepted > 0 else 0.0

    return CouplingResult(
        frequency_hz=frequency,
        spl_db=spl_db,
        incident_pressure_pa=p_inc,
        ka=ka,
        shell_displacement_m=xi,
        shell_displacement_um=xi * 1e6,
        amplification_factor=H_mag,
        radiation_damping_ratio=zeta_rad,
        total_damping_ratio=zeta_total,
        effective_Q=Q_eff,
        wall_bending_strain=eps_bending,
        wall_membrane_strain=eps_membrane,
        is_long_wavelength=(ka < 0.1),
        energy_absorption_fraction=absorption,
        coupling_notes=(
            f"ka={ka:.4f} ({'long-wavelength' if ka < 0.1 else 'WARNING: not long-wavelength'}), "
            f"ζ_struct={zeta_struct:.3f}, ζ_rad={zeta_rad:.2e}, "
            f"Q_eff={Q_eff:.1f}, f_n={f_n:.2f} Hz"
        ),
    )


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE — Corrected Acoustic-Structure Coupling Analysis")
    print("  Properly accounting for long-wavelength regime physics")
    print("=" * 72)
    print()

    # === Demonstrate the key physics ===
    model = AbdominalModel()
    R = model.equivalent_sphere_radius
    f = 7.0  # Hz

    ka = compute_ka(f, R)
    print(f"  LONG-WAVELENGTH CHECK")
    print(f"  Frequency: {f} Hz")
    print(f"  Wavelength in air: {C_AIR/f:.1f} m")
    print(f"  Body radius: {R*100:.1f} cm")
    print(f"  ka = {ka:.4f}  ({'<< 1: LONG-WAVELENGTH LIMIT' if ka < 0.1 else 'WARNING'})")
    print()

    # === Radiation damping ===
    Z_rad = radiation_impedance_sphere(f, R)
    print(f"  RADIATION IMPEDANCE (breathing mode at {f} Hz)")
    print(f"  Z_rad = {Z_rad.real:.4e} + j·{Z_rad.imag:.4e}")
    print(f"  Radiation resistance (real): {Z_rad.real:.4e} kg/s")
    print(f"  Radiation reactance (imag): {Z_rad.imag:.4e} kg/s")
    zeta_r = radiation_damping_ratio(f, model)
    print(f"  Radiation damping ratio: ζ_rad = {zeta_r:.2e}")
    print(f"  (Compare structural: ζ_struct ≈ 0.05-0.20)")
    print(f"  → Radiation damping is NEGLIGIBLE vs structural damping")
    print()

    # === Corrected shell response ===
    print(f"  CORRECTED SHELL RESPONSE (baseline model)")
    print(f"  " + "-" * 65)
    print(f"  {'SPL(dB)':>8} {'P(Pa)':>10} {'H(f)':>8} {'ξ(μm)':>10} "
          f"{'ε_memb':>12} {'ε_bend':>12} {'Q_eff':>8}")
    print(f"  " + "-" * 65)

    for spl in [90, 100, 110, 120, 130, 140, 150]:
        r = shell_response_to_pressure(f, spl, model, loss_tangent=0.3)
        print(f"  {spl:>8} {r.incident_pressure_pa:>10.2f} "
              f"{r.amplification_factor:>8.2f} {r.shell_displacement_um:>10.4f} "
              f"{r.wall_membrane_strain:>12.2e} {r.wall_bending_strain:>12.2e} "
              f"{r.effective_Q:>8.1f}")
    print(f"  " + "-" * 65)
    print()

    # === Compare old (naive) vs new (corrected) at resonance ===
    print(f"  COMPARISON: NAIVE vs CORRECTED (at resonance)")
    print(f"  " + "-" * 60)

    # Soft tissue model that resonates in the brown note range
    model_soft = AbdominalModel(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f_res = breathing_mode_frequency(model_soft)
    print(f"  Model: soft tissue (E=0.1 MPa, a=18cm)")
    print(f"  Resonance frequency: {f_res:.2f} Hz")
    print()

    for spl in [100, 110, 120, 130, 140]:
        # Corrected
        r_corr = shell_response_to_pressure(f_res, spl, model_soft, loss_tangent=0.3)

        # Old naive: free-field displacement × Q
        p = 20e-6 * 10**(spl/20)
        c_tissue = np.sqrt(model_soft.K_fluid / model_soft.rho_fluid)
        v_free = p / (model_soft.rho_fluid * c_tissue)
        xi_naive = v_free / (2 * np.pi * f_res) * r_corr.effective_Q * 1e6

        print(f"  SPL={spl} dB: corrected={r_corr.shell_displacement_um:.4f} μm, "
              f"naive={xi_naive:.4f} μm, "
              f"ratio={r_corr.shell_displacement_um/xi_naive:.2f}x" if xi_naive > 0 else
              f"  SPL={spl} dB: corrected={r_corr.shell_displacement_um:.4f} μm")

    print()

    # === Key result: what SPL is needed for PIEZO threshold? ===
    print(f"  CORRECTED PIEZO THRESHOLD ANALYSIS")
    print(f"  " + "-" * 60)
    print(f"  Model: soft tissue, resonance at {f_res:.2f} Hz")
    print()

    for tan_d in [0.15, 0.20, 0.30, 0.40]:
        Q = 1 / (2 * (tan_d / 2))
        # Binary search for SPL giving 1.0 μm displacement
        spl_lo, spl_hi = 80.0, 200.0
        for _ in range(50):
            spl_mid = (spl_lo + spl_hi) / 2
            r = shell_response_to_pressure(f_res, spl_mid, model_soft, loss_tangent=tan_d)
            if r.shell_displacement_um < 1.0:
                spl_lo = spl_mid
            else:
                spl_hi = spl_mid

        spl_threshold = (spl_lo + spl_hi) / 2
        r_at_thresh = shell_response_to_pressure(f_res, spl_threshold, model_soft, loss_tangent=tan_d)
        print(f"  tan(δ)={tan_d:.2f} → Q={Q:.1f}: "
              f"SPL for 1μm = {spl_threshold:.1f} dB "
              f"(ε_memb={r_at_thresh.wall_membrane_strain:.2e})")

    print()
    print(f"  PIEZO threshold context:")
    print(f"    0.5-2.0 μm: patch-clamp membrane indentation threshold")
    print(f"    Wall membrane strain at 1μm displacement: ~{1e-6/model_soft.equivalent_sphere_radius:.1e}")
    print(f"    This is BULK strain, not localized indentation")
    print(f"    → Direct comparison with PIEZO threshold is CONSERVATIVE")
    print(f"    → The actual cellular-level strain depends on stress")
    print(f"       concentration at tissue interfaces and cell geometry")
    print()

    # === Long-wavelength argument summary ===
    print("=" * 72)
    print("  KEY INSIGHT: WHY THE CORRECTED MODEL GIVES LARGER DISPLACEMENTS")
    print("=" * 72)
    print()
    print("  The naive model computed: particle_velocity / (2πf)")
    print("  This is the displacement of a fluid element in a FREE sound field.")
    print()
    print("  The corrected model computes: p_incident / k_shell × H(f)")
    print("  This is the shell's mechanical response to the APPLIED pressure.")
    print()
    print("  The difference: the shell is much MORE compliant than the bulk")
    print("  fluid. A thin, soft shell deforms much more than the surrounding")
    print("  medium under the same pressure. At resonance, this is amplified")
    print("  by the quality factor Q.")
    print()
    print("  The air-tissue impedance mismatch affects:")
    print("    ✗ NOT the driving pressure (which is the full incident p)")
    print("    ✓ The radiation damping (very small for ka << 1)")
    print("    ✓ The energy extracted from the sound field (very small)")
    print()
    print("  Conclusion: The corrected model actually predicts LARGER")
    print("  displacements than the naive model for soft shells, because")
    print("  the shell's compliance dominates over the acoustic impedance.")
    print()
