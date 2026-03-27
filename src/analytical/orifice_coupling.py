"""
Orifice coupling pathway analysis.

The mouth and nose provide LOW-IMPEDANCE pathways for airborne sound
to enter the GI tract, bypassing the tissue impedance mismatch.

Pathway: Airborne sound → mouth/nose → pharynx → esophagus → stomach → intestines

At each step, the acoustic impedance changes and attenuation occurs.
But the key insight is that the air column in the upper GI tract acts
as a waveguide that can transmit pressure down to the stomach/intestines.

This is a genuinely under-studied pathway for infrasound effects.

Key considerations:
1. The mouth is essentially an open aperture (R ≈ 2 cm)
2. The esophagus is a collapsible tube (collapsed diameter ~0 cm, open ~2 cm)
3. The stomach contains an air bubble (20-50 mL normally)
4. The total path length mouth → stomach is ~40 cm

At 7 Hz, λ = 49 m, so the entire GI tract is λ/100 — deeply sub-wavelength.
In this regime, the pressure is essentially uniform throughout the air column.

References:
    - Finck, A. (1966) "Aural detection of low-frequency sound" JASA 40(5)
    - von Gierke, H.E. (1971) "Response of the body to mechanical forces"
    - Leventhall, G. (2007) Review of infrasound effects, DfES report
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class UpperGITract:
    """Acoustic model of the upper GI tract as an air-filled pathway."""

    # Mouth aperture
    mouth_radius_cm: float = 2.0        # when open [cm]
    mouth_open_fraction: float = 0.3     # fraction of time mouth is open

    # Pharynx / esophagus
    esophagus_diameter_cm: float = 2.0   # when open (during swallowing)
    esophagus_length_cm: float = 25.0    # length [cm]
    esophagus_open: bool = False         # normally collapsed

    # Stomach
    stomach_volume_mL: float = 500.0     # average volume
    stomach_gas_volume_mL: float = 30.0  # gastric air bubble

    # Path properties
    total_path_length_cm: float = 40.0   # mouth to stomach

    # Air properties
    rho_air: float = 1.225
    c_air: float = 343.0


def orifice_coupling_open_mouth(
    tract: UpperGITract,
    spl_db: float = 120.0,
    freq_hz: float = 7.0,
) -> dict:
    """
    Estimate pressure transmission through open mouth to stomach.

    In the sub-wavelength regime (kL << 1), the pressure throughout
    the air column equals the incident pressure (minus losses).

    The mouth acts as a Helmholtz-resonator type aperture.
    Below resonance, pressure is transmitted nearly unchanged.
    """
    p_ref = 20e-6
    p_inc = p_ref * 10**(spl_db / 20)
    omega = 2 * np.pi * freq_hz

    L = tract.total_path_length_cm * 1e-2  # meters
    k = omega / tract.c_air
    kL = k * L

    # Sub-wavelength: pressure transmission ≈ 1
    # The air column acts as a simple pressure conduit
    # Loss from viscothermal effects in narrow tubes:
    # α = (1/a) × √(ωμ/(2ρc²)) for a tube of radius a
    # At 7 Hz in a 1cm radius tube: α ≈ very small
    a_eso = tract.esophagus_diameter_cm * 1e-2 / 2  # radius in m
    mu_air = 1.8e-5  # dynamic viscosity of air [Pa·s]

    # Viscothermal attenuation per meter
    if a_eso > 0:
        alpha_vt = (1/a_eso) * np.sqrt(omega * mu_air / (2 * tract.rho_air * tract.c_air**2))
    else:
        alpha_vt = float('inf')

    transmission_loss_dB = 20 * np.log10(np.exp(-alpha_vt * L))

    # Pressure at stomach
    p_stomach = p_inc * np.exp(-alpha_vt * L)

    # The stomach gas bubble acts as a compliant element
    # When pressurized, the gas compresses and the stomach wall displaces
    V_gas = tract.stomach_gas_volume_mL * 1e-6  # m³
    R_bubble = (3 * V_gas / (4 * np.pi))**(1/3)  # equivalent radius

    # Displacement of stomach wall from gas compression
    # ΔV/V = ΔP / (γP₀), ΔR/R = ΔP / (3γP₀)
    gamma = 1.4
    P0 = 101325 + 1000  # atmospheric + IAP
    delta_R = R_bubble * p_stomach / (3 * gamma * P0)

    return {
        'freq_hz': freq_hz,
        'spl_db': spl_db,
        'p_inc_Pa': p_inc,
        'kL': kL,
        'alpha_vt_per_m': alpha_vt,
        'transmission_loss_dB': transmission_loss_dB,
        'p_stomach_Pa': p_stomach,
        'p_ratio': p_stomach / p_inc,
        'gas_bubble_radius_mm': R_bubble * 1000,
        'gas_displacement_um': delta_R * 1e6,
        'pathway': 'open_mouth',
    }


def orifice_coupling_closed_mouth(
    tract: UpperGITract,
    spl_db: float = 120.0,
    freq_hz: float = 7.0,
) -> dict:
    """
    With mouth closed, the only pathway is through tissue.

    The nose provides a partial air pathway (nose → nasopharynx → pharynx)
    but it's more tortuous. With mouth AND nose closed (e.g., Valsalva),
    there's no air pathway at all.

    With mouth closed, the body surface is the only coupling pathway,
    which has the (ka)^n penalty.
    """
    p_ref = 20e-6
    p_inc = p_ref * 10**(spl_db / 20)
    R_body = 0.16  # m
    omega = 2 * np.pi * freq_hz
    ka = omega * R_body / 343.0

    # For n=2 flexural mode
    p_eff = p_inc * ka**2

    return {
        'freq_hz': freq_hz,
        'spl_db': spl_db,
        'p_inc_Pa': p_inc,
        'ka': ka,
        'p_eff_Pa': p_eff,
        'p_ratio': p_eff / p_inc,
        'pathway': 'closed_mouth_body_surface',
    }


def nasal_pathway(
    tract: UpperGITract,
    spl_db: float = 120.0,
    freq_hz: float = 7.0,
) -> dict:
    """
    Nasal breathing provides a continuous air pathway even with mouth closed.

    Nose → nasal cavity → nasopharynx → pharynx → esophagus → stomach

    The nasal passages are narrower (effective diameter ~5mm per nostril)
    and more tortuous, leading to higher viscothermal losses.
    """
    p_ref = 20e-6
    p_inc = p_ref * 10**(spl_db / 20)
    omega = 2 * np.pi * freq_hz

    # Nasal passage parameters
    a_nasal = 0.0025  # effective radius ~2.5mm per nostril
    L_nasal = 0.10    # nasal passage length ~10 cm
    L_total = L_nasal + tract.esophagus_length_cm * 1e-2  # total to stomach
    mu_air = 1.8e-5

    # Viscothermal attenuation in narrow nasal passages
    alpha_nasal = (1/a_nasal) * np.sqrt(omega * mu_air / (2 * tract.rho_air * tract.c_air**2))
    alpha_eso = (1/(tract.esophagus_diameter_cm*1e-2/2)) * np.sqrt(
        omega * mu_air / (2 * tract.rho_air * tract.c_air**2))

    total_loss = np.exp(-alpha_nasal * L_nasal - alpha_eso * tract.esophagus_length_cm * 1e-2)
    p_stomach = p_inc * total_loss

    return {
        'freq_hz': freq_hz,
        'spl_db': spl_db,
        'p_inc_Pa': p_inc,
        'alpha_nasal': alpha_nasal,
        'alpha_esophagus': alpha_eso,
        'total_transmission': total_loss,
        'p_stomach_Pa': p_stomach,
        'p_ratio': p_stomach / p_inc,
        'pathway': 'nasal',
    }


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  BROWNTONE — Orifice Coupling Pathway Analysis")
    print("  Mouth/nose as low-impedance acoustic pathways")
    print("=" * 72)
    print()

    tract = UpperGITract()

    # Compare three pathways
    print("  PATHWAY COMPARISON AT 120 dB, 7 Hz")
    print("  " + "-" * 60)
    print(f"  {'Pathway':>25} {'p_stomach/p_inc':>16} {'p_stomach(Pa)':>14} {'Loss(dB)':>10}")
    print("  " + "-" * 60)

    r_open = orifice_coupling_open_mouth(tract, 120.0, 7.0)
    r_nasal = nasal_pathway(tract, 120.0, 7.0)
    r_closed = orifice_coupling_closed_mouth(tract, 120.0, 7.0)

    print(f"  {'Open mouth':>25} {r_open['p_ratio']:>16.6f} {r_open['p_stomach_Pa']:>14.4f} "
          f"{r_open['transmission_loss_dB']:>10.2f}")
    print(f"  {'Nasal breathing':>25} {r_nasal['p_ratio']:>16.6f} {r_nasal['p_stomach_Pa']:>14.4f} "
          f"{20*np.log10(r_nasal['p_ratio']):>10.2f}")
    print(f"  {'Closed (body surface)':>25} {r_closed['p_ratio']:>16.6f} {r_closed['p_eff_Pa']:>14.4f} "
          f"{20*np.log10(r_closed['p_ratio']):>10.2f}")

    print("  " + "-" * 60)
    print(f"  Open mouth delivers {r_open['p_ratio']/r_closed['p_ratio']:.0f}× more pressure to stomach")
    print(f"  than body-surface (ka)² coupling!")
    print()

    # Effect on stomach gas bubble
    print("  STOMACH GAS BUBBLE DISPLACEMENT")
    print("  " + "-" * 55)
    print(f"  {'Pathway':>25} {'SPL':>6} {'ξ_bubble(μm)':>14} {'PIEZO?':>8}")
    print("  " + "-" * 55)

    for spl in [100, 110, 120, 130, 140]:
        r = orifice_coupling_open_mouth(tract, spl, 7.0)
        piezo = "YES" if r['gas_displacement_um'] > 0.5 else "no"
        print(f"  {'Open mouth':>25} {spl:>6} {r['gas_displacement_um']:>14.4f} {piezo:>8}")

    print("  " + "-" * 55)
    print()

    # Frequency sweep
    print("  FREQUENCY SWEEP (open mouth, 120 dB)")
    print("  " + "-" * 55)
    for f in [1, 2, 5, 7, 10, 20, 50, 100]:
        r = orifice_coupling_open_mouth(tract, 120.0, f)
        print(f"    f={f:>4} Hz: transmission={r['p_ratio']:.6f}, "
              f"ξ={r['gas_displacement_um']:.4f} μm")
    print("  " + "-" * 55)
    print()

    # The key insight: esophagus is normally closed
    print("  " + "=" * 65)
    print("  CRITICAL CAVEAT: ESOPHAGUS IS NORMALLY COLLAPSED")
    print("  " + "=" * 65)
    print()
    print("  The esophagus is a collapsible muscular tube that is CLOSED")
    print("  at rest. It only opens during swallowing (0.5-1.0 s per swallow).")
    print("  This means the continuous air pathway exists only during:")
    print("    - Swallowing (brief)")
    print("    - Belching (brief)")
    print("    - Gastroesophageal reflux (pathological)")
    print("    - Open-mouth breathing with relaxed upper esophageal sphincter")
    print()
    print("  At rest with mouth/nose open, pressure still reaches the")
    print("  PHARYNX (supraglottic space) with minimal loss, but cannot")
    print("  reach the STOMACH without an open esophagus.")
    print()
    print("  However, the pharyngeal/laryngeal tissue IS exposed to the")
    print("  full pressure, and there are mechanoreceptors in this region.")
    print()

    # Comparison of ALL coupling mechanisms
    print("  " + "=" * 68)
    print("  GRAND COMPARISON: ALL COUPLING MECHANISMS AT 120 dB, 7 Hz")
    print("  " + "=" * 68)
    print()

    mechanisms = [
        ("1. Cavity resonance (n=2, airborne)", 0.14, "Very weak"),
        ("2. Gas pocket R=2cm (airborne)", 0.94, "Near threshold"),
        ("3. Gas pocket R=5cm (airborne)", 2.4, "Above threshold"),
        ("4. Orifice (open mouth → stomach)", r_open['gas_displacement_um'], "Small"),
        ("5. WBV at 0.1 m/s² (mechanical)", 623.0, "Far above"),
        ("6. WBV at 1.15 m/s² EU limit (mech)", 7165.0, "Enormous"),
    ]

    print(f"  {'Mechanism':>45} {'ξ(μm)':>10} {'Assessment':>15}")
    print("  " + "-" * 68)
    for name, xi, assess in mechanisms:
        piezo = "✓" if xi > 0.5 else "✗"
        print(f"  {name:>45} {xi:>10.2f} {assess:>15} {piezo}")
    print("  " + "-" * 68)
    print(f"  PIEZO threshold: 0.5-2.0 μm")
    print()
    print("  RANKING (strongest to weakest):")
    print("    1. Mechanical WBV (overwhelming)")
    print("    2. Bowel gas pockets ≥3cm (plausible at 120+ dB)")
    print("    3. Orifice pathway (limited by esophageal closure)")
    print("    4. Whole-cavity resonance (negligible)")
    print()
