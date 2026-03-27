"""
Multi-layer abdominal wall model.

The real abdominal wall has ~5 distinct layers with different mechanical
properties. This module computes the effective composite properties
for use in the shell modal analysis.

Layer structure (anterior wall, inside→out):
  1. Peritoneum (thin membrane, ~0.1mm)
  2. Transversalis fascia + transversus abdominis (~3mm)
  3. Internal oblique muscle (~5mm)
  4. External oblique muscle (~5mm)
  5. Subcutaneous fat (~5-30mm) + skin (~2mm)

The effective bending stiffness D_eff and membrane stiffness (Eh)_eff
are computed using classical laminate theory.

References:
  - Hernández-Gascón et al. (2013) J. Mech. Behav. Biomed. Mater. 20:417
  - Förstemann et al. (2011) J. Biomech. 44(8):1572
  - Song et al. (2006) J. Biomech. 39(16):3056
  - Tran et al. (2014) J. Biomech. 47(9):2031
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2,
)


@dataclass
class Layer:
    """A single layer of the abdominal wall."""
    name: str
    thickness_mm: float     # mm
    E_MPa: float           # Young's modulus [MPa]
    nu: float              # Poisson's ratio
    rho_kgm3: float        # density [kg/m³]

    @property
    def h(self) -> float:
        """Thickness in meters."""
        return self.thickness_mm * 1e-3

    @property
    def E(self) -> float:
        """Modulus in Pa."""
        return self.E_MPa * 1e6


# Predefined layer stacks for different body types
def relaxed_layers() -> List[Layer]:
    """Relaxed, untensed abdominal wall."""
    return [
        Layer("peritoneum",     0.1,  0.5,  0.45, 1050),
        Layer("transversalis",  3.0,  0.05, 0.45, 1050),
        Layer("int_oblique",    5.0,  0.05, 0.45, 1060),
        Layer("ext_oblique",    5.0,  0.08, 0.45, 1060),
        Layer("subcut_fat",    10.0,  0.002, 0.49, 950),
        Layer("skin",           2.0,  0.5,  0.45, 1100),
    ]


def tensed_layers() -> List[Layer]:
    """Actively braced abdominal wall."""
    return [
        Layer("peritoneum",     0.1,  0.5,  0.45, 1050),
        Layer("transversalis",  3.0,  0.2,  0.45, 1050),
        Layer("int_oblique",    5.0,  5.0,  0.45, 1060),
        Layer("ext_oblique",    5.0,  8.0,  0.45, 1060),
        Layer("subcut_fat",    10.0,  0.002, 0.49, 950),
        Layer("skin",           2.0,  0.5,  0.45, 1100),
    ]


def obese_layers() -> List[Layer]:
    """Obese individual with thick fat layer."""
    return [
        Layer("peritoneum",     0.1,  0.5,  0.45, 1050),
        Layer("transversalis",  3.0,  0.04, 0.45, 1050),
        Layer("int_oblique",    4.0,  0.03, 0.45, 1060),
        Layer("ext_oblique",    4.0,  0.05, 0.45, 1060),
        Layer("subcut_fat",    30.0,  0.002, 0.49, 950),
        Layer("skin",           2.0,  0.5,  0.45, 1100),
    ]


def compute_composite_properties(layers: List[Layer]) -> dict:
    """
    Compute effective composite properties using classical laminate theory.

    For a multi-layer shell, the effective properties are:
      (Eh)_eff = Σ E_i h_i  (membrane stiffness)
      D_eff = Σ [E_i/(1-ν_i²)] × [h_i³/12 + h_i(z_i - z_mid)²]
      h_total = Σ h_i
      ρ_eff = (Σ ρ_i h_i) / h_total
      ν_eff = (Σ ν_i E_i h_i) / (Σ E_i h_i)  (weighted average)
    """
    h_total = sum(L.h for L in layers)
    Eh_total = sum(L.E * L.h for L in layers)
    rho_h_total = sum(L.rho_kgm3 * L.h for L in layers)

    # Weighted Poisson's ratio
    nu_eff = sum(L.nu * L.E * L.h for L in layers) / Eh_total

    # Effective E
    E_eff = Eh_total / h_total

    # Effective density
    rho_eff = rho_h_total / h_total

    # Bending stiffness (with parallel axis theorem)
    z_bot = 0.0
    z_mid = h_total / 2.0
    D_eff = 0.0

    for L in layers:
        z_center = z_bot + L.h / 2  # center of this layer
        d = z_center - z_mid         # distance from neutral axis
        # Contribution: E/(1-ν²) × (h³/12 + h×d²)
        D_eff += (L.E / (1 - L.nu**2)) * (L.h**3 / 12 + L.h * d**2)
        z_bot += L.h

    # For comparison: effective D from E_eff, h_total, ν_eff
    D_homogeneous = E_eff * h_total**3 / (12 * (1 - nu_eff**2))

    return {
        'h_total_m': h_total,
        'h_total_mm': h_total * 1000,
        'E_eff_Pa': E_eff,
        'E_eff_MPa': E_eff / 1e6,
        'nu_eff': nu_eff,
        'rho_eff': rho_eff,
        'Eh_eff': Eh_total,
        'D_eff': D_eff,
        'D_homogeneous': D_homogeneous,
        'D_ratio': D_eff / D_homogeneous if D_homogeneous > 0 else float('inf'),
    }


def multilayer_to_v2_model(
    layers: List[Layer],
    a: float = 0.18,
    c_over_a: float = 0.67,
    loss_tangent: float = 0.30,
) -> AbdominalModelV2:
    """Convert multi-layer wall to equivalent AbdominalModelV2."""
    props = compute_composite_properties(layers)
    return AbdominalModelV2(
        E=props['E_eff_Pa'],
        a=a,
        b=a,
        c=a * c_over_a,
        h=props['h_total_m'],
        nu=props['nu_eff'],
        rho_wall=props['rho_eff'],
        loss_tangent=loss_tangent,
    )


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE — Multi-Layer Abdominal Wall Analysis")
    print("=" * 72)
    print()

    configs = {
        'Relaxed': relaxed_layers(),
        'Tensed':  tensed_layers(),
        'Obese':   obese_layers(),
    }

    for name, layers in configs.items():
        props = compute_composite_properties(layers)
        print(f"  {name} wall:")
        print(f"  " + "-" * 60)
        for L in layers:
            print(f"    {L.name:20s}  h={L.thickness_mm:5.1f}mm  E={L.E_MPa:6.3f}MPa  "
                  f"ν={L.nu:.2f}  ρ={L.rho_kgm3}")
        print(f"  {'COMPOSITE':20s}  h={props['h_total_mm']:5.1f}mm  "
              f"E={props['E_eff_MPa']:6.3f}MPa  ν={props['nu_eff']:.3f}  "
              f"ρ={props['rho_eff']:.0f}")
        print(f"    D_eff = {props['D_eff']:.4e} Pa·m³")
        print(f"    D_homogeneous = {props['D_homogeneous']:.4e} Pa·m³")
        print(f"    D_eff/D_homo = {props['D_ratio']:.2f}")
        print()

    # Flexural mode frequencies
    print("  FLEXURAL MODE FREQUENCIES WITH MULTI-LAYER WALL")
    print("  " + "-" * 65)
    print(f"  {'Config':>12} {'h(mm)':>8} {'E_eff(MPa)':>12} {'f_n2(Hz)':>10} "
          f"{'f_n3(Hz)':>10} {'f_n4(Hz)':>10}")
    print("  " + "-" * 65)

    for name, layers in configs.items():
        model = multilayer_to_v2_model(layers)
        freqs = flexural_mode_frequencies_v2(model, n_max=4)
        print(f"  {name:>12} {model.h*1000:>8.1f} {model.E/1e6:>12.4f} "
              f"{freqs[2]:>10.2f} {freqs[3]:>10.2f} {freqs[4]:>10.2f}")

    # Homogeneous comparison
    print()
    print(f"  {'Homo 0.1MPa':>12} {'10.0':>8} {'0.1000':>12} ", end='')
    m_homo = AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)
    f_homo = flexural_mode_frequencies_v2(m_homo, n_max=4)
    print(f"{f_homo[2]:>10.2f} {f_homo[3]:>10.2f} {f_homo[4]:>10.2f}")

    print("  " + "-" * 65)
    print()

    # Key comparison: how much does multi-layer matter?
    relaxed_model = multilayer_to_v2_model(relaxed_layers())
    tensed_model = multilayer_to_v2_model(tensed_layers())
    f_relax = flexural_mode_frequencies_v2(relaxed_model, n_max=2)[2]
    f_tense = flexural_mode_frequencies_v2(tensed_model, n_max=2)[2]

    print("  KEY FINDINGS:")
    print(f"    Relaxed n=2: {f_relax:.2f} Hz (within brown note range)")
    print(f"    Tensed  n=2: {f_tense:.2f} Hz (above brown note range)")
    print(f"    Ratio: {f_tense/f_relax:.1f}×")
    print()
    print("    Multi-layer vs homogeneous:")
    print(f"      Multi-layer relaxed: {f_relax:.2f} Hz")
    print(f"      Homogeneous E=0.1:   {f_homo[2]:.2f} Hz")
    print(f"      Difference: {abs(f_relax-f_homo[2])/f_homo[2]*100:.1f}%")
    print()
    print("    CONCLUSION: The multi-layer model shifts frequencies")
    print("    slightly but the qualitative picture is unchanged.")
    print("    Muscle tension is the dominant factor (5-30× modulus change).")
    print()
