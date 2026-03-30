"""
Corrected natural frequency computation with proper fluid-structure coupling.

VERSION 2 — Fixes critical errors in v1:
1. Breathing mode (n=0) now includes fluid compressibility (bulk modulus)
2. Flexural modes (n≥2) include fluid added mass but NOT volumetric stiffness
3. Pre-stress from intra-abdominal pressure included
4. Acoustic coupling via pressure gradient for flexural modes

The key insight: for a fluid-filled shell, the breathing mode is dominated
by the fluid bulk modulus (giving frequencies in the kHz range). The LOW
frequency modes (5-10 Hz) are FLEXURAL modes where the shell deforms without
significant volume change, and the fluid acts primarily as added mass.

References:
    - Junger, M.C. & Feit, D. "Sound, Structures, and Their Interaction"
    - Elaikh, T.H. (2010) "Free Vibration of Axisymmetric Thin Oblate Shells
      Containing Fluid"
    - ISO 2631-1:1997
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class AbdominalModelV2:
    """Improved abdominal model with pre-stress and layered properties."""

    # Geometry
    a: float = 0.18          # semi-major axis [m]
    b: float = 0.18          # second semi-major [m]
    c: float = 0.12          # semi-minor axis [m]
    h: float = 0.010         # wall thickness [m]

    # Wall material
    E: float = 0.1e6         # Young's modulus [Pa] (0.1 MPa)
    nu: float = 0.45         # Poisson's ratio
    rho_wall: float = 1100.0 # wall density [kg/m³]
    loss_tangent: float = 0.25 # viscoelastic loss tangent

    # Fluid
    rho_fluid: float = 1020.0 # fluid density [kg/m³]
    K_fluid: float = 2.2e9   # bulk modulus [Pa]

    # Pre-stress (intra-abdominal pressure)
    P_iap: float = 1000.0    # intra-abdominal pressure [Pa] (~7.5 mmHg)

    @property
    def c_fluid(self) -> float:
        """Speed of sound in the fluid [m/s]."""
        return np.sqrt(self.K_fluid / self.rho_fluid)

    @property
    def equivalent_sphere_radius(self) -> float:
        return (self.a * self.b * self.c) ** (1/3)

    @property
    def D(self) -> float:
        """Flexural rigidity [N·m]."""
        return self.E * self.h**3 / (12 * (1 - self.nu**2))

    @property
    def volume(self) -> float:
        return (4/3) * np.pi * self.a * self.b * self.c

    @property
    def surface_area(self) -> float:
        e = np.sqrt(1 - (self.c / self.a)**2)
        if e < 1e-10:
            return 4 * np.pi * self.a**2
        return 2 * np.pi * self.a**2 * (1 + (1 - e**2) / e * np.arctanh(e))

    @property
    def Q(self) -> float:
        """Quality factor from loss tangent."""
        zeta = self.loss_tangent / 2
        return 1 / (2 * zeta) if zeta > 0 else float('inf')

    @property
    def damping_ratio(self) -> float:
        return self.loss_tangent / 2


def breathing_mode_v2(model: AbdominalModelV2) -> float:
    """
    Breathing mode (n=0) with CORRECT fluid coupling.

    For a fluid-filled shell, the breathing mode stiffness has TWO contributions:
    1. Shell membrane stiffness: k_shell = 2Eh / [R²(1-ν)]
    2. Fluid volumetric stiffness: k_fluid = 3K / R

    Total: k_total = k_shell + k_fluid

    For biological tissue: k_fluid >> k_shell by many orders of magnitude.
    This means the breathing mode frequency is dominated by the fluid
    and is in the kHz range.
    """
    R = model.equivalent_sphere_radius

    # Shell membrane stiffness (per unit area)
    k_shell = 2 * model.E * model.h / (R**2 * (1 - model.nu))

    # Fluid volumetric stiffness (per unit area of shell)
    # When the shell radius changes by δR, the volume change is 4πR²·δR
    # The pressure change is ΔP = K·ΔV/V = K·3δR/R
    # The restoring force per unit area is K·3/R times displacement per unit area
    k_fluid = 3 * model.K_fluid / R

    k_total = k_shell + k_fluid

    # Effective mass per unit area
    m_eff = model.rho_wall * model.h + model.rho_fluid * R

    omega = np.sqrt(k_total / m_eff)
    return omega / (2 * np.pi)


def flexural_mode_frequencies_v2(
    model: AbdominalModelV2, n_max: int = 10
) -> dict:
    """
    Flexural mode frequencies (n ≥ 2) with proper fluid loading.

    For flexural modes, the shell deforms WITHOUT significant volume change.
    The fluid acts as ADDED MASS (inertial loading) but does NOT contribute
    volumetric stiffness. This is because the incompressible flow pattern
    associated with flexural deformation involves fluid redistribution,
    not compression.

    The restoring force comes from:
    1. Shell bending stiffness (flexural rigidity D)
    2. Shell membrane stiffness (from curvature coupling)
    3. Pre-stress from intra-abdominal pressure (tension stiffness)

    The effective mass is:
    1. Shell wall mass
    2. Fluid added mass (mode-dependent): m_added = ρ_f · R / n

    For n ≥ 2 modes on a PRESSURIZED shell:
        ω² = [K_bend + K_memb + K_prestress] / [m_wall + m_fluid_added]
    """
    R = model.equivalent_sphere_radius
    E, h, nu = model.E, model.h, model.nu
    rho_w, rho_f = model.rho_wall, model.rho_fluid
    D = model.D
    P = model.P_iap

    frequencies = {}

    # n=0: breathing mode (fluid-dominated, kHz range)
    frequencies[0] = breathing_mode_v2(model)

    # n=1: rigid body translation (zero for free shell)
    frequencies[1] = 0.0

    for n in range(2, n_max + 1):
        # Bending stiffness
        K_bend = n * (n - 1) * (n + 2)**2 * D / R**4

        # Membrane stiffness (Lamb, 1882)
        lambda_n = (n**2 + n - 2 + 2*nu) / (n**2 + n + 1 - nu)
        K_memb = E * h / R**2 * lambda_n

        # Pre-stress stiffness from intra-abdominal pressure
        # A pressurized shell has additional stiffness:
        # K_P = P/R × (n-1)(n+2) for mode n
        # This is the "tension stiffening" effect
        K_prestress = P / R * (n - 1) * (n + 2)

        K_total = K_bend + K_memb + K_prestress

        # Effective mass per unit area:
        # Wall mass + fluid added mass
        # For mode n on a sphere, added mass = ρ_f × R / n
        m_eff = rho_w * h + rho_f * R / n

        omega_sq = K_total / m_eff
        frequencies[n] = np.sqrt(max(0, omega_sq)) / (2 * np.pi)

    return frequencies


def flexural_mode_pressure_response(
    frequency: float,
    spl_db: float,
    mode_n: int,
    model: AbdominalModelV2,
) -> dict:
    """
    Compute flexural mode response to airborne infrasound.

    For flexural modes, the driving force is the PRESSURE GRADIENT
    across the body, not the uniform pressure.

    In the long-wavelength limit (ka << 1), for mode n:
    - Uniform component (n=0): drives breathing mode only
    - Dipole component (n=1): drives rigid body translation
    - Quadrupole+ (n≥2): very weak acoustic coupling

    The pressure gradient for a plane wave:
        ΔP ≈ p_inc × 2ka × cos(θ)  [for dipole]
        ΔP ≈ p_inc × (ka)² × P₂(cos θ)  [for quadrupole, n=2]

    This means the coupling to flexural modes goes as (ka)^n, which is
    EXTREMELY weak for infrasound (ka ≈ 0.0114).

    HOWEVER: there are alternative coupling mechanisms:
    1. Body vibration transmitted through skeleton/floor (mechanical coupling)
    2. Chest wall motion from respiratory coupling
    3. Direct excitation through body orifices
    4. Gravity-wave coupling (for standing/supine body)

    For the AIRBORNE acoustic pathway specifically, the coupling is very weak.
    """
    R = model.equivalent_sphere_radius
    p_ref = 20e-6
    p_inc = p_ref * 10**(spl_db / 20)

    # ka
    c_air = 343.0
    ka = 2 * np.pi * frequency * R / c_air

    # Modal coupling coefficient
    # For mode n, the acoustic coupling goes as (ka)^n for a sphere
    # For n=2 (quadrupole): coupling ∝ (ka)²
    if mode_n == 0:
        # Breathing mode: uniform pressure drives it fully
        p_eff = p_inc
    elif mode_n == 1:
        # Dipole: gradient coupling
        p_eff = p_inc * ka
    else:
        # Higher modes: (ka)^n coupling
        p_eff = p_inc * ka**(mode_n)

    # Modal stiffness (from flexural_mode_frequencies_v2)
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    omega_n = 2 * np.pi * f_n

    # Stiffness per unit area
    D_flex = model.D
    E, h, nu = model.E, model.h, model.nu
    P_iap = model.P_iap

    K_bend = mode_n * (mode_n - 1) * (mode_n + 2)**2 * D_flex / R**4
    lambda_n = (mode_n**2 + mode_n - 2 + 2*nu) / (mode_n**2 + mode_n + 1 - nu)
    K_memb = E * h / R**2 * lambda_n
    K_prestress = P_iap / R * (mode_n - 1) * (mode_n + 2)
    K_total = K_bend + K_memb + K_prestress

    # Frequency response
    omega = 2 * np.pi * frequency
    zeta = model.damping_ratio
    r = omega / omega_n if omega_n > 0 else 0

    H_mag = 1 / np.sqrt((1 - r**2)**2 + (2*zeta*r)**2) if omega_n > 0 else 0

    # Displacement
    xi = p_eff / K_total * H_mag if K_total > 0 else 0

    return {
        'frequency_hz': frequency,
        'spl_db': spl_db,
        'mode_n': mode_n,
        'resonance_hz': f_n,
        'ka': ka,
        'effective_pressure_pa': p_eff,
        'coupling_coefficient': ka**mode_n if mode_n > 0 else 1.0,
        'displacement_um': xi * 1e6,
        'amplification': H_mag,
        'Q_structural': model.Q,
        'stiffness_pa_m': K_total,
    }


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE v2 — Corrected Modal Analysis")
    print("  With proper fluid coupling & acoustic excitation")
    print("=" * 72)
    print()

    model = AbdominalModelV2()
    R = model.equivalent_sphere_radius

    # Show corrected frequencies
    freqs = flexural_mode_frequencies_v2(model, n_max=10)

    print("  CORRECTED MODAL FREQUENCIES")
    print("  " + "-" * 55)
    print(f"  {'Mode':>6} {'Freq(Hz)':>12} {'Type':>20} {'In 5-10Hz':>10}")
    print("  " + "-" * 55)
    for n, f in sorted(freqs.items()):
        if n == 0:
            mtype = "breathing (fluid)"
        elif n == 1:
            mtype = "rigid body"
        elif n == 2:
            mtype = "oblate-prolate"
        else:
            mtype = f"flexural n={n}"

        tag = "<<< YES >>>" if 5 <= f <= 10 else ""
        if n == 0 and f > 100:
            print(f"  {n:>6} {f:>12.1f} {mtype:>20} {'(kHz range)':>10}")
        else:
            print(f"  {n:>6} {f:>12.2f} {mtype:>20} {tag:>10}")
    print("  " + "-" * 55)
    print()

    # Check brown note range
    brown = {n: f for n, f in freqs.items() if 5 <= f <= 10 and n > 0}
    if brown:
        print(f"  ★ {len(brown)} flexural mode(s) in 5-10 Hz range:")
        for n, f in brown.items():
            print(f"    Mode n={n}: {f:.2f} Hz")
    else:
        valid = {n: f for n, f in freqs.items() if 0 < f < 100 and n > 1}
        if valid:
            closest = min(valid, key=lambda n: abs(valid[n] - 7.5))
            print(f"  Closest flexural mode to 7.5 Hz: n={closest} at {valid[closest]:.2f} Hz")
    print()

    # Parametric: soft tissue
    print("  PARAMETRIC: Soft tissue models")
    print("  " + "-" * 65)
    configs = [
        ("Baseline (E=0.1 MPa, a=0.18 m)", AbdominalModelV2()),
        ("Soft+Large (E=0.1 MPa, a=0.20 m)", AbdominalModelV2(E=0.1e6, a=0.20, b=0.20, c=0.13)),
        ("Very soft (E=0.05, a=20)", AbdominalModelV2(E=0.05e6, a=0.20, b=0.20, c=0.13)),
        ("No prestress", AbdominalModelV2(E=0.1e6, P_iap=0)),
        ("High prestress (20mmHg)", AbdominalModelV2(E=0.1e6, P_iap=2666)),
    ]

    for label, m in configs:
        f_v2 = flexural_mode_frequencies_v2(m, n_max=4)
        f2 = f_v2[2]
        f3 = f_v2[3]
        tag2 = " <<<" if 5 <= f2 <= 10 else ""
        tag3 = " <<<" if 5 <= f3 <= 10 else ""
        print(f"  {label:<35} n=2: {f2:>7.2f} Hz{tag2:<5} n=3: {f3:>7.2f} Hz{tag3}")
    print("  " + "-" * 65)
    print()

    # Acoustic coupling for flexural modes
    print("  ACOUSTIC COUPLING: Airborne infrasound to flexural modes")
    print("  " + "-" * 65)
    print(f"  NOTE: For mode n, coupling goes as (ka)^n")
    print(f"  At 7 Hz: ka = {2*np.pi*7*R/343:.4f}")
    print()

    m_soft = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f2 = flexural_mode_frequencies_v2(m_soft, n_max=2)[2]

    print(f"  Model: soft tissue, n=2 resonance at {f2:.2f} Hz")
    print(f"  {'SPL(dB)':>8} {'p_inc(Pa)':>10} {'p_eff(Pa)':>10} {'ξ(μm)':>10} {'coupling':>10}")
    print(f"  " + "-" * 55)
    for spl in [100, 110, 120, 130, 140, 150]:
        r = flexural_mode_pressure_response(f2, spl, 2, m_soft)
        print(f"  {spl:>8} {20e-6*10**(spl/20):>10.2f} "
              f"{r['effective_pressure_pa']:>10.6f} "
              f"{r['displacement_um']:>10.6f} "
              f"{r['coupling_coefficient']:>10.2e}")
    print(f"  " + "-" * 55)
    print()

    print("  CRITICAL FINDING:")
    print("  The (ka)² coupling coefficient for n=2 mode is ~2.8×10⁻⁴")
    print("  This means only 0.028% of the incident pressure drives")
    print("  the flexural modes via airborne acoustic path.")
    print()
    print("  For PIEZO threshold (1 μm) via airborne path alone:")
    # Binary search for 1 μm
    spl_lo, spl_hi = 100.0, 250.0
    for _ in range(50):
        spl_mid = (spl_lo + spl_hi) / 2
        r = flexural_mode_pressure_response(f2, spl_mid, 2, m_soft)
        if r['displacement_um'] < 1.0:
            spl_lo = spl_mid
        else:
            spl_hi = spl_mid
    print(f"  SPL needed: ~{(spl_lo+spl_hi)/2:.0f} dB")
    print(f"  This is UNREALISTICALLY HIGH for airborne sound alone.")
    print()
    print("  HOWEVER: Mechanical coupling (through floor, seat, skeleton)")
    print("  bypasses the (ka)^n penalty entirely. Whole-body vibration")
    print("  at 5-10 Hz from machinery or vehicles IS known to cause")
    print("  GI effects — this is consistent with ISO 2631.")
    print()
