"""
Analytical natural frequency computation for fluid-filled oblate spheroidal shells.

Models the human abdomen as a thin-walled oblate spheroid filled with
incompressible fluid. Computes the lowest natural frequencies using
Rayleigh-Ritz energy method and simplified shell theory.

This is the foundational calculation for the "browntone" project:
investigating whether infrasound at 5-10 Hz can excite resonance in
the human abdominal cavity.

References:
    - Elaikh, T.H. "Free Vibration of Axisymmetric Thin Oblate Shells
      Containing Fluid"
    - Junger, M.C. & Feit, D. "Sound, Structures, and Their Interaction"
    - Lamb, H. (1882) "On the Vibrations of an Elastic Sphere"
    - ISO 2631-1:1997 — Whole-body vibration evaluation

Author: Browntone Research Project
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class AbdominalModel:
    """Material and geometric properties for the abdominal cavity model.

    Default values from published biomechanical literature:
    - Geometry: Song et al. (2006), anthropometric surveys
    - Wall properties: Hernandez-Gascon et al. (2013), Forstemann et al. (2011)
    - Fluid properties: standard physiological values
    """

    # --- Geometry (oblate spheroid) ---
    a: float = 0.15          # semi-major axis (horizontal radius) [m]
    b: float = 0.15          # second semi-major axis [m] (= a for axisymmetric)
    c: float = 0.10          # semi-minor axis (anterior-posterior half-depth) [m]
    h: float = 0.015         # wall thickness (composite abdominal wall) [m]

    # --- Wall material properties ---
    E: float = 0.5e6         # Young's modulus [Pa] — mid-range for composite wall
    nu: float = 0.49         # Poisson's ratio (nearly incompressible soft tissue)
    rho_wall: float = 1050.0 # wall density [kg/m^3]

    # --- Contained fluid (abdominal contents as equivalent fluid) ---
    rho_fluid: float = 1040.0  # fluid density [kg/m^3]
    K_fluid: float = 2.2e9    # bulk modulus of water-like fluid [Pa]

    @property
    def eccentricity(self) -> float:
        return np.sqrt(1 - (self.c / self.a) ** 2)

    @property
    def aspect_ratio(self) -> float:
        return self.c / self.a

    @property
    def surface_area(self) -> float:
        e = self.eccentricity
        if e < 1e-10:
            return 4 * np.pi * self.a ** 2
        return 2 * np.pi * self.a**2 * (1 + (1 - e**2) / e * np.arctanh(e))

    @property
    def volume(self) -> float:
        return (4 / 3) * np.pi * self.a * self.b * self.c

    @property
    def fluid_mass(self) -> float:
        return self.rho_fluid * self.volume

    @property
    def wall_mass(self) -> float:
        return self.rho_wall * self.surface_area * self.h

    @property
    def D(self) -> float:
        """Flexural rigidity of the shell [N*m]."""
        return self.E * self.h**3 / (12 * (1 - self.nu**2))

    @property
    def equivalent_sphere_radius(self) -> float:
        return (self.a * self.b * self.c) ** (1/3)


def breathing_mode_frequency(model: AbdominalModel) -> float:
    """
    Breathing (n=0) mode of a fluid-filled thin spheroidal shell.
    Uses Junger-Feit approximation with equivalent sphere radius.
    """
    R = model.equivalent_sphere_radius
    E, h, nu = model.E, model.h, model.nu
    rho_w, rho_f = model.rho_wall, model.rho_fluid

    k_eff = 2 * E * h / (R**2 * (1 - nu))
    m_eff = rho_w * h + rho_f * R
    omega = np.sqrt(k_eff / m_eff)
    return omega / (2 * np.pi)


def shell_modal_frequencies(model: AbdominalModel, n_max: int = 10) -> dict:
    """
    Natural frequencies for mode numbers n = 0..n_max of a fluid-filled
    thin spheroidal shell (Lamb theory + fluid loading).
    """
    R = model.equivalent_sphere_radius
    E, h, nu = model.E, model.h, model.nu
    rho_w, rho_f = model.rho_wall, model.rho_fluid
    D_flex = model.D

    frequencies = {}
    for n in range(n_max + 1):
        if n == 0:
            frequencies[n] = breathing_mode_frequency(model)
        elif n == 1:
            frequencies[n] = 0.0  # rigid body translation
        else:
            K_bend = n * (n - 1) * (n + 2)**2 * D_flex / R**4
            lambda_n = (n**2 + n - 2 + 2*nu) / (n**2 + n + 1 - nu)
            K_memb = E * h / R**2 * lambda_n
            K_total = K_bend + K_memb
            m_eff = rho_w * h + rho_f * R / n
            omega_sq = K_total / m_eff
            frequencies[n] = np.sqrt(max(0, omega_sq)) / (2 * np.pi)
    return frequencies


def acoustic_pressure_to_displacement(
    f: float, SPL_dB: float, model: Optional[AbdominalModel] = None
) -> dict:
    """Estimate tissue displacement from incident sound at frequency f and SPL."""
    if model is None:
        model = AbdominalModel()
    p_ref = 20e-6
    p = p_ref * 10**(SPL_dB / 20)
    c_tissue = np.sqrt(model.K_fluid / model.rho_fluid)
    v = p / (model.rho_fluid * c_tissue)
    xi = v / (2 * np.pi * f) if f > 0 else 0.0
    return {
        'frequency_Hz': f, 'SPL_dB': SPL_dB,
        'acoustic_pressure_Pa': p,
        'particle_velocity_m_s': v,
        'free_field_displacement_um': xi * 1e6,
        'resonant_displacement_um_Q3': xi * 3.0 * 1e6,
        'resonant_displacement_um_Q5': xi * 5.0 * 1e6,
        'resonant_displacement_um_Q10': xi * 10.0 * 1e6,
    }


if __name__ == "__main__":
    print()
    print("=" * 65)
    print("  BROWNTONE - Infrasound Abdominal Resonance Analysis")
    print("  Analytical Modal Frequency Computation")
    print("=" * 65)
    print()

    model = AbdominalModel()
    print("  GEOMETRY & MATERIAL PROPERTIES")
    print("  " + "-" * 55)
    print(f"    Semi-major axis (a)     = {model.a*100:.1f} cm")
    print(f"    Semi-minor axis (c)     = {model.c*100:.1f} cm")
    print(f"    Aspect ratio (c/a)      = {model.aspect_ratio:.3f}")
    print(f"    Wall thickness (h)      = {model.h*1000:.1f} mm")
    print(f"    Volume                  = {model.volume*1e6:.0f} cm3 ({model.volume*1e3:.2f} L)")
    print(f"    Young's modulus (E)     = {model.E/1e6:.3f} MPa")
    print(f"    Poisson's ratio         = {model.nu:.2f}")
    print(f"    Equiv sphere radius     = {model.equivalent_sphere_radius*100:.2f} cm")
    print(f"    Wall mass               = {model.wall_mass:.2f} kg")
    print(f"    Fluid mass              = {model.fluid_mass:.2f} kg")
    print()

    freqs = shell_modal_frequencies(model, n_max=10)
    print("  MODAL FREQUENCIES")
    print("  " + "-" * 45)
    print(f"  {'Mode n':>8}  {'Freq (Hz)':>12}  {'In 5-10 Hz?':>12}")
    print("  " + "-" * 45)
    for n, f in sorted(freqs.items()):
        tag = "<<< YES >>>" if 5.0 <= f <= 10.0 else ("(rigid)" if n == 1 else "")
        print(f"  {n:>8}  {f:>12.2f}  {tag:>12}")
    print("  " + "-" * 45)
    print()

    brown = {n: f for n, f in freqs.items() if 5.0 <= f <= 10.0}
    if brown:
        print(f"  *** {len(brown)} MODE(S) IN BROWN NOTE RANGE (5-10 Hz) ***")
        for n, f in brown.items():
            print(f"      Mode {n}: {f:.2f} Hz")
    else:
        valid = {n: f for n, f in freqs.items() if f > 0}
        closest = min(valid, key=lambda n: abs(valid[n] - 7.5))
        print(f"  Closest to 7.5 Hz: mode {closest} = {valid[closest]:.2f} Hz")
    print()

    # Displacement analysis
    print("  TISSUE DISPLACEMENT AT 7 Hz vs SPL")
    print("  " + "-" * 62)
    print(f"  {'SPL(dB)':>8} {'P(Pa)':>10} {'Free(um)':>10} {'Q=5(um)':>10} {'Q=10(um)':>10}")
    print("  " + "-" * 62)
    for spl in [90, 100, 110, 120, 130, 140, 150]:
        r = acoustic_pressure_to_displacement(7.0, spl, model)
        print(f"  {spl:>8} {r['acoustic_pressure_Pa']:>10.2f} "
              f"{r['free_field_displacement_um']:>10.4f} "
              f"{r['resonant_displacement_um_Q5']:>10.4f} "
              f"{r['resonant_displacement_um_Q10']:>10.4f}")
    print("  " + "-" * 62)
    print()

    # Parametric: Young's modulus
    print("  PARAMETRIC: Wall Stiffness vs Breathing Mode (n=0)")
    print("  " + "-" * 55)
    for E_val in [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]:
        m = AbdominalModel(E=E_val * 1e6)
        f0 = breathing_mode_frequency(m)
        bar = "#" * max(1, int(f0 / 2))
        marker = " <<<" if 5.0 <= f0 <= 10.0 else ""
        print(f"    E={E_val:>5.2f} MPa -> f0={f0:>7.2f} Hz  {bar}{marker}")
    print("  " + "-" * 55)
    print()

    # Parametric: Wall thickness
    print("  PARAMETRIC: Wall Thickness vs Breathing Mode (n=0)")
    print("  " + "-" * 55)
    for h_mm in [5, 10, 15, 20, 25, 30, 40]:
        m = AbdominalModel(h=h_mm * 1e-3)
        f0 = breathing_mode_frequency(m)
        bar = "#" * max(1, int(f0 / 2))
        marker = " <<<" if 5.0 <= f0 <= 10.0 else ""
        print(f"    h={h_mm:>5.1f} mm  -> f0={f0:>7.2f} Hz  {bar}{marker}")
    print("  " + "-" * 55)
    print()

    # Parametric: Cavity size (BMI proxy)
    print("  PARAMETRIC: Cavity Size (BMI proxy) vs Breathing Mode")
    print("  " + "-" * 55)
    for a_cm in [10, 12, 15, 18, 20, 25]:
        a_val = a_cm / 100
        c_val = a_val * 0.667
        m = AbdominalModel(a=a_val, b=a_val, c=c_val)
        f0 = breathing_mode_frequency(m)
        bar = "#" * max(1, int(f0 / 2))
        marker = " <<<" if 5.0 <= f0 <= 10.0 else ""
        print(f"    a={a_cm:>5.1f} cm  -> f0={f0:>7.2f} Hz  {bar}{marker}")
    print("  " + "-" * 55)
    print()
    print("  Analysis complete.")
