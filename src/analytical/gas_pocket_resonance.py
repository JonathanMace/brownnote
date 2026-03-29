"""
Bowel gas bubble resonance analysis.

A NOVEL idea: The human intestine normally contains 100-200 mL of gas.
These gas pockets create air-tissue interfaces INSIDE the abdomen,
which dramatically changes the acoustic coupling:

1. At an air-tissue interface, the impedance mismatch is ~3600:1
2. Gas pockets can have Minnaert resonances at low frequencies
3. Gas-containing bowel loops act as bubble-like resonators

The Minnaert resonance of an air bubble in water is:
  f_M = (1/(2πa)) × sqrt(3γP₀/ρ_f)
  where a = bubble radius, γ = 1.4, P₀ = atmospheric, ρ_f = fluid density

For a 2cm radius gas pocket: f_M ≈ 163 Hz (too high)
For a 5cm radius: f_M ≈ 65 Hz (still too high)
For a 10cm radius: f_M ≈ 33 Hz (closer but still above 10 Hz)

BUT: Minnaert assumes a free, spherical bubble. Intestinal gas pockets are:
  - Elongated (cylindrical) not spherical
  - Constrained by the intestinal wall (adding mass)
  - In a viscoelastic medium (not pure water)
  - Sometimes contain a mix of gases at different pressures

The key question: can constrained gas pockets in the gut resonate at 5-10 Hz?

If so, this creates a TOTALLY DIFFERENT mechanism for the brown note:
  Airborne infrasound → penetrates body (weakly) → BUT finds gas pockets
  that act as resonant receivers → local amplification → tissue strain
  → PIEZO activation

This would be MUCH more efficient than whole-shell resonance because:
  - Gas pockets have very different impedance from surrounding tissue
  - They CAN be excited by airborne sound (unlike the fluid-filled cavity)
  - Individual variability in gas content explains why effects are inconsistent

References:
  - Minnaert (1933) Phil. Mag. 16(104):235
  - Leighton (1994) "The Acoustic Bubble" Academic Press
  - Commander & Prosperetti (1989) JASA 85(2):732
  - Plesset & Prosperetti (1977) Ann. Rev. Fluid Mech. 9:145
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class GasPocket:
    """A gas pocket in the intestine."""
    radius_cm: float = 2.0          # effective radius [cm]
    length_cm: float = 10.0         # length for cylindrical pockets [cm]
    gamma: float = 1.4              # ratio of specific heats (air)
    P0_Pa: float = 101325.0         # atmospheric pressure
    rho_fluid: float = 1040.0       # surrounding fluid density [kg/m³]
    sigma: float = 0.05             # surface tension [N/m] (intestinal wall)

    @property
    def radius_m(self) -> float:
        return self.radius_cm * 1e-2

    @property
    def length_m(self) -> float:
        return self.length_cm * 1e-2

    @property
    def volume_mL(self) -> float:
        """Volume in mL (assuming sphere for simple cases)."""
        return (4/3) * np.pi * (self.radius_cm)**3


def minnaert_frequency(pocket: GasPocket) -> float:
    """
    Minnaert resonance frequency for a spherical gas bubble.

    f_M = (1/2πa) × √(3γP₀/ρ)
    """
    a = pocket.radius_m
    return (1 / (2 * np.pi * a)) * np.sqrt(
        3 * pocket.gamma * pocket.P0_Pa / pocket.rho_fluid
    )


def constrained_bubble_frequency(
    pocket: GasPocket,
    wall_mass_per_area: float = 5.0,  # kg/m² (intestinal wall mass loading)
    wall_stiffness: float = 100.0,    # Pa/m (intestinal wall elastic restoring)
) -> float:
    """
    Modified Minnaert frequency for a gas pocket constrained by intestinal wall.

    The wall adds mass loading (reducing frequency) and stiffness (increasing).

    f = (1/2πa) × √((3γP₀ + k_wall × a²) / (ρ_f + m_wall / a))

    where m_wall = wall mass per unit area.
    """
    a = pocket.radius_m
    k_gas = 3 * pocket.gamma * pocket.P0_Pa  # gas stiffness [Pa]
    k_wall_eff = wall_stiffness * a**2
    m_gas = pocket.rho_fluid  # fluid added mass [kg/m³]
    m_wall = wall_mass_per_area / a  # wall mass contribution [kg/m³]

    omega_sq = (k_gas + k_wall_eff) / (a**2 * (m_gas + m_wall))
    return np.sqrt(max(omega_sq, 0)) / (2 * np.pi)


def elongated_pocket_frequency(pocket: GasPocket) -> float:
    """
    For an elongated cylindrical gas pocket (L >> R), the lowest
    resonance is different from Minnaert:

    For a cylinder of length L with closed ends:
      f_1 = c_gas / (2L)  where c_gas = √(γP₀/ρ_gas)

    For a gas pocket surrounded by liquid in a tube (pipe mode):
      f_1 = (1/2L) × √(γP₀/ρ_f)  × correction_factor

    The correction factor accounts for radiation impedance at the ends.
    """
    L = pocket.length_m
    # Speed of sound in the gas-liquid system
    # For a gas slug in a tube: effective c depends on gas compliance + liquid inertia
    # Simplified: f ≈ (1/2π) × √(γP₀/(ρ_f × L × a))
    a = pocket.radius_m
    omega = np.sqrt(pocket.gamma * pocket.P0_Pa / (pocket.rho_fluid * L * a))
    return omega / (2 * np.pi)


def acoustic_response_of_gas_pocket(
    pocket: GasPocket,
    spl_db: float = 120.0,
    freq_hz: float = 7.0,
) -> dict:
    """
    Compute the response of an intestinal gas pocket to incident sound.

    At the gas-tissue interface, there is a massive impedance mismatch:
      Z_tissue ≈ 1.6 × 10⁶ Pa·s/m
      Z_gas ≈ 420 Pa·s/m
      Reflection coefficient R ≈ (Z_t - Z_g)/(Z_t + Z_g) ≈ 0.9995

    BUT: the gas pocket is INSIDE the body. The incident pressure wave
    creates a spatially uniform pressure field in the tissue (long λ).
    This uniform pressure drives the gas pocket walls, compressing/expanding
    the gas. The bubble displacement is:

    ξ = p_inc / (k_eff - ω²m_eff)  (forced oscillator)
    """
    p_ref = 20e-6
    p_inc = p_ref * 10**(spl_db / 20)
    omega = 2 * np.pi * freq_hz

    # Minnaert natural frequency
    f_M = minnaert_frequency(pocket)
    omega_M = 2 * np.pi * f_M

    a = pocket.radius_m
    rho = pocket.rho_fluid

    # Stiffness per unit displacement of wall
    k_gas = 3 * pocket.gamma * pocket.P0_Pa / a  # Pa/m

    # Effective mass per unit area
    m_eff = rho * a  # added mass of surrounding fluid

    # Damping (radiation + thermal + viscous)
    # Radiation damping for bubble: δ_rad = ω a / c_liquid
    c_liquid = 1540.0
    delta_rad = omega * a / c_liquid
    # Thermal damping for air bubble: δ_th ≈ 0.01-0.1 (frequency dependent)
    delta_th = 0.05
    # Viscous damping
    mu = 0.001  # Pa·s (water-like)
    delta_vis = 4 * mu / (rho * omega * a**2)

    zeta = (delta_rad + delta_th + delta_vis) / 2

    # Frequency response
    r = omega / omega_M
    H = 1 / np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)

    # Wall displacement
    xi = (p_inc / k_gas) * H

    # Internal pressure oscillation
    delta_p = p_inc * H * (omega/omega_M)**2  # pressure inside bubble

    return {
        'f_minnaert_hz': f_M,
        'f_drive_hz': freq_hz,
        'frequency_ratio': r,
        'amplification': H,
        'damping_ratio': zeta,
        'wall_displacement_um': xi * 1e6,
        'p_inc_Pa': p_inc,
        'internal_pressure_Pa': delta_p,
        'spl_db': spl_db,
        'pocket_radius_cm': pocket.radius_cm,
        'pocket_volume_mL': pocket.volume_mL,
    }


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE — Bowel Gas Pocket Resonance Analysis")
    print("  A NOVEL mechanism for infrasound-tissue interaction")
    print("=" * 72)
    print()

    # Minnaert frequencies for different pocket sizes
    print("  1. MINNAERT FREQUENCIES (spherical, unconstrained)")
    print("  " + "-" * 55)
    print(f"  {'R(cm)':>8} {'Vol(mL)':>10} {'f_M(Hz)':>10} {'In 5-10Hz?':>12}")
    print("  " + "-" * 55)

    for r_cm in [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]:
        pocket = GasPocket(radius_cm=r_cm)
        f_M = minnaert_frequency(pocket)
        vol = pocket.volume_mL
        in_range = "YES" if 5 <= f_M <= 10 else "no"
        print(f"  {r_cm:>8.1f} {vol:>10.1f} {f_M:>10.1f} {in_range:>12}")

    print("  " + "-" * 55)
    print("  Minnaert frequencies too high for brown note range.")
    print("  BUT: real gas pockets are constrained and elongated.")
    print()

    # Constrained pocket frequencies
    print("  2. CONSTRAINED GAS POCKET FREQUENCIES")
    print("  " + "-" * 60)
    print(f"  {'R(cm)':>8} {'f_Minnaert':>12} {'f_constrained':>14} {'f_elongated':>12}")
    print("  " + "-" * 60)

    for r_cm in [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]:
        pocket = GasPocket(radius_cm=r_cm, length_cm=r_cm*3)
        f_M = minnaert_frequency(pocket)
        f_c = constrained_bubble_frequency(pocket)
        f_e = elongated_pocket_frequency(pocket)
        print(f"  {r_cm:>8.1f} {f_M:>12.1f} {f_c:>14.1f} {f_e:>12.1f}")

    print("  " + "-" * 60)
    print()

    # Key question: response at 7 Hz for various pocket sizes
    print("  3. GAS POCKET RESPONSE TO 7 Hz INFRASOUND")
    print("  " + "-" * 70)
    print(f"  {'R(cm)':>8} {'f_M(Hz)':>10} {'SPL':>6} {'f/f_M':>8} "
          f"{'H':>8} {'ξ(μm)':>10} {'PIEZO?':>8}")
    print("  " + "-" * 70)

    for r_cm in [1.0, 2.0, 5.0, 10.0]:
        for spl in [100, 120, 140]:
            pocket = GasPocket(radius_cm=r_cm)
            resp = acoustic_response_of_gas_pocket(pocket, spl_db=spl, freq_hz=7.0)
            piezo = "YES" if resp['wall_displacement_um'] > 0.5 else "no"
            print(f"  {r_cm:>8.1f} {resp['f_minnaert_hz']:>10.1f} {spl:>6} "
                  f"{resp['frequency_ratio']:>8.4f} {resp['amplification']:>8.4f} "
                  f"{resp['wall_displacement_um']:>10.4f} {piezo:>8}")

    print("  " + "-" * 70)
    print()

    # Frequency sweep for a typical gas pocket
    print("  4. FREQUENCY SWEEP: R=5cm pocket at 120 dB")
    print("  " + "-" * 55)
    pocket = GasPocket(radius_cm=5.0)
    for f in [1, 2, 5, 7, 10, 20, 50, 65, 100]:
        resp = acoustic_response_of_gas_pocket(pocket, spl_db=120.0, freq_hz=f)
        print(f"    f={f:>4} Hz: H={resp['amplification']:>8.3f}, "
              f"ξ={resp['wall_displacement_um']:>10.4f} μm")
    print("  " + "-" * 55)
    print()

    # Summary
    print("  " + "=" * 65)
    print("  SUMMARY: BOWEL GAS AS RESONANCE MECHANISM")
    print("  " + "=" * 65)
    print()
    print("  Minnaert frequencies for physiological gas pockets (1-10 cm)")
    print("  range from ~30 Hz (large) to ~330 Hz (small).")
    print()
    print("  At 7 Hz, the frequency ratio f/f_M ≈ 0.02-0.2, so gas pockets")
    print("  are driven FAR below resonance. The amplification H ≈ 1.0")
    print("  (no resonant enhancement).")
    print()
    print("  However, the gas pockets DO respond to incident pressure")
    print("  because they are compressible (unlike the surrounding tissue).")
    print("  The displacement ξ = p_inc / k_gas is independent of frequency")
    print("  in the sub-resonant regime.")
    print()

    # Key number: displacement of gas pocket wall at 120 dB
    pocket = GasPocket(radius_cm=3.0)
    p_120 = 20e-6 * 10**(120/20)  # 20 Pa
    k_gas = 3 * 1.4 * 101325 / 0.03  # Pa/m
    xi_gas = p_120 / k_gas
    print(f"  At 120 dB (20 Pa): R=3cm pocket wall displacement = {xi_gas*1e6:.3f} μm")
    print(f"  At 140 dB (200 Pa): = {xi_gas*10*1e6:.3f} μm")
    print()
    print("  THIS IS SMALL but not negligible! The gas pocket concentrates")
    print("  the acoustic displacement into a small tissue region,")
    print("  unlike the whole-cavity resonance model.")
    print()
    print("  NOVEL HYPOTHESIS: Inter-individual variability in brown note")
    print("  susceptibility may be explained by bowel gas content.")
    print("  More gas → more sites for pressure-displacement conversion.")
    print()
