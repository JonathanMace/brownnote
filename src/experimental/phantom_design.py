"""
Phantom design predictions for experimental validation of the
fluid-filled shell model.

Computes expected resonant frequencies, transfer functions, and
coupling ratios for silicone phantom shells across a range of
formulations, comparing each to the canonical human-abdomen parameters.

Usage:
    python -m src.experimental.phantom_design

Outputs:
    data/figures/fig_phantom_predictions.png
"""

import os
import sys
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)

FIG_DIR = os.path.join(ROOT, "data", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Canonical human parameters (from the paper)
# ---------------------------------------------------------------------------
HUMAN_PARAMS = dict(
    E=0.1e6,          # Pa
    a=0.18, b=0.18,   # m  (semi-major)
    c=0.12,            # m  (semi-minor)
    h=0.01,            # m  (wall thickness)
    nu=0.45,
    rho_wall=1100.0,   # kg/m³
    rho_fluid=1020.0,  # kg/m³
    K_fluid=2.2e9,     # Pa  (water)
    P_iap=1000.0,      # Pa  (~7.5 mmHg)
    loss_tangent=0.3,
)

# ---------------------------------------------------------------------------
# Silicone formulations (from manufacturer datasheets)
# ---------------------------------------------------------------------------
SILICONES = {
    "Ecoflex 00-10": dict(E=0.055e6, loss=0.15, shore="00-10"),
    "Ecoflex 00-30": dict(E=0.069e6, loss=0.18, shore="00-30"),
    "Ecoflex 00-50": dict(E=0.083e6, loss=0.20, shore="00-50"),
    "Dragon Skin 10A": dict(E=0.15e6, loss=0.12, shore="10A"),
    "Dragon Skin 20A": dict(E=0.30e6, loss=0.10, shore="20A"),
    "Dragon Skin 30A": dict(E=0.59e6, loss=0.08, shore="30A"),
}


def make_phantom_model(silicone_E: float, loss: float = 0.15) -> AbdominalModelV2:
    """Construct a phantom model with human geometry but silicone material."""
    return AbdominalModelV2(
        E=silicone_E,
        a=0.18, b=0.18, c=0.12,
        h=0.01,
        nu=0.45,           # silicone Poisson's ratio (nearly incompressible)
        rho_wall=1100.0,   # silicone density
        rho_fluid=1000.0,  # degassed water
        K_fluid=2.2e9,
        P_iap=0.0,         # no intra-abdominal pressure in phantom
        loss_tangent=loss,
    )


def compute_phantom_predictions() -> dict:
    """Compute resonant frequencies for every silicone formulation."""
    results = {}

    # Human reference
    human = AbdominalModelV2(**HUMAN_PARAMS)
    human_freqs = flexural_mode_frequencies_v2(human, n_max=6)
    results["Human (canonical)"] = {
        "model": human,
        "freqs": human_freqs,
        "E_MPa": HUMAN_PARAMS["E"] / 1e6,
    }

    for name, props in SILICONES.items():
        m = make_phantom_model(props["E"], props["loss"])
        freqs = flexural_mode_frequencies_v2(m, n_max=6)
        results[name] = {
            "model": m,
            "freqs": freqs,
            "E_MPa": props["E"] / 1e6,
        }
    return results


def transfer_function(f_array: np.ndarray, f_n: float,
                      zeta: float) -> np.ndarray:
    """
    Base-excitation relative transmissibility |H_rel(f)|.
    H_rel = r² / sqrt((1-r²)² + (2ζr)²),  r = f/f_n
    """
    r = f_array / f_n
    return r**2 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)


def coupling_ratio_vs_E(E_range: np.ndarray) -> np.ndarray:
    """
    Coupling ratio (mechanical / airborne displacement) vs elastic modulus.
    Uses the analytical expressions at each formulation's n=2 resonance.
    """
    ratios = np.empty_like(E_range)
    for i, E_val in enumerate(E_range):
        m = make_phantom_model(E_val)
        freqs = flexural_mode_frequencies_v2(m, n_max=2)
        f2 = freqs[2]
        R = m.equivalent_sphere_radius
        zeta = m.damping_ratio
        Q = m.Q

        # Airborne at 120 dB, n=2
        p_inc = 20e-6 * 10**(120 / 20)  # Pa
        ka = 2 * np.pi * f2 * R / 343.0
        p_eff = p_inc * ka**2

        # Modal stiffness
        D = m.D
        n = 2
        K_b = n * (n - 1) * (n + 2)**2 * D / R**4
        lam = (n**2 + n - 2 + 2 * m.nu) / (n**2 + n + 1 - m.nu)
        K_m = m.E * m.h / R**2 * lam
        K_total = K_b + K_m  # no IAP in phantom
        xi_air = p_eff / K_total * Q * 1e6  # μm

        # Mechanical at 0.1 m/s² (gentle), at resonance
        a_rms = 0.1
        omega = 2 * np.pi * f2
        x_base = a_rms * np.sqrt(2) / omega**2
        # At resonance H_rel ≈ 1/(2ζ) = Q
        xi_mech = x_base * Q * 1e6  # μm

        ratios[i] = xi_mech / xi_air if xi_air > 0 else np.inf
    return ratios


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def generate_figure(results: dict) -> str:
    """
    Create a 2×2 figure:
      (a) f_n vs mode number for each formulation
      (b) Transfer function H_rel(f) for three representative silicones
      (c) f₂ vs elastic modulus (phantom range + human range)
      (d) Coupling ratio (mech/air) vs E
    Returns the path to the saved figure.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(
        "Phantom Predictions — Silicone Shell Validation Design",
        fontsize=14, fontweight="bold", y=0.98,
    )

    cmap = plt.cm.viridis
    names = [k for k in results if k != "Human (canonical)"]
    colors = {n: cmap(i / max(len(names) - 1, 1)) for i, n in enumerate(names)}
    colors["Human (canonical)"] = "red"

    # ── Panel (a): mode frequencies ──
    ax = axes[0, 0]
    modes = list(range(2, 7))
    for label, data in results.items():
        freqs = [data["freqs"][n] for n in modes]
        ls = "--" if label == "Human (canonical)" else "-"
        lw = 2.5 if label == "Human (canonical)" else 1.4
        ax.plot(modes, freqs, marker="o", ls=ls, lw=lw,
                color=colors[label], label=label, markersize=5)
    ax.axhspan(3, 6, alpha=0.10, color="orange", label="Target 3–6 Hz")
    ax.set_xlabel("Mode number $n$")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("(a) Flexural mode frequencies")
    ax.legend(fontsize=7, loc="upper left")
    ax.set_xticks(modes)
    ax.grid(True, alpha=0.3)

    # ── Panel (b): transfer functions ──
    ax = axes[0, 1]
    f_arr = np.linspace(0.5, 20, 500)
    for label in ["Ecoflex 00-30", "Dragon Skin 10A", "Human (canonical)"]:
        data = results[label]
        f2 = data["freqs"][2]
        zeta = data["model"].damping_ratio
        H = transfer_function(f_arr, f2, zeta)
        ls = "--" if label == "Human (canonical)" else "-"
        lw = 2.5 if label == "Human (canonical)" else 1.4
        ax.plot(f_arr, H, ls=ls, lw=lw, color=colors[label],
                label=f"{label} ($f_2$={f2:.1f} Hz)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("|$H_{\\mathrm{rel}}$| (base excitation)")
    ax.set_title("(b) Transfer function — phantom vs human")
    ax.legend(fontsize=8)
    ax.set_yscale("log")
    ax.set_ylim(1e-2, 20)
    ax.grid(True, alpha=0.3, which="both")

    # ── Panel (c): f₂ vs E ──
    ax = axes[1, 0]
    E_sweep = np.linspace(0.03e6, 0.7e6, 200)
    f2_sweep = np.empty_like(E_sweep)
    for i, E_val in enumerate(E_sweep):
        m = make_phantom_model(E_val)
        f2_sweep[i] = flexural_mode_frequencies_v2(m, n_max=2)[2]
    ax.plot(E_sweep / 1e6, f2_sweep, "k-", lw=1.5, label="Phantom model")

    # Mark specific silicones
    for label, data in results.items():
        if label == "Human (canonical)":
            continue
        ax.plot(data["E_MPa"], data["freqs"][2], "o", color=colors[label],
                markersize=7, label=label, zorder=5)
    # Human band
    ax.axhspan(3, 6, alpha=0.10, color="orange")
    ax.axvspan(0.05, 0.3, alpha=0.08, color="blue", label="Tissue E range")
    human_f2 = results["Human (canonical)"]["freqs"][2]
    ax.plot(0.1, human_f2, "r*", markersize=14, zorder=6,
            label=f"Human canonical ({human_f2:.1f} Hz)")
    ax.set_xlabel("Elastic modulus $E$ (MPa)")
    ax.set_ylabel("$f_2$ (Hz)")
    ax.set_title("(c) $n$=2 frequency vs material stiffness")
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(True, alpha=0.3)

    # ── Panel (d): coupling ratio ──
    ax = axes[1, 1]
    E_ratio = np.linspace(0.04e6, 0.6e6, 100)
    ratios = coupling_ratio_vs_E(E_ratio)
    ax.semilogy(E_ratio / 1e6, ratios, "k-", lw=1.5)
    for label, data in results.items():
        if label == "Human (canonical)":
            continue
        E_val = data["E_MPa"] * 1e6
        m = make_phantom_model(E_val)
        freqs = flexural_mode_frequencies_v2(m, n_max=2)
        f2 = freqs[2]
        R = m.equivalent_sphere_radius
        Q = m.Q
        p_inc = 20e-6 * 10**(120 / 20)
        ka = 2 * np.pi * f2 * R / 343.0
        D = m.D
        n = 2
        K_b = n * (n-1) * (n+2)**2 * D / R**4
        lam = (n**2+n-2+2*m.nu)/(n**2+n+1-m.nu)
        K_m = m.E * m.h / R**2 * lam
        K_total = K_b + K_m
        xi_air = p_inc * ka**2 / K_total * Q * 1e6
        omega = 2 * np.pi * f2
        x_base = 0.1 * np.sqrt(2) / omega**2
        xi_mech = x_base * Q * 1e6
        r_val = xi_mech / xi_air if xi_air > 0 else np.inf
        ax.plot(data["E_MPa"], r_val, "o", color=colors[label], markersize=7)

    ax.set_xlabel("Elastic modulus $E$ (MPa)")
    ax.set_ylabel("$\\xi_{\\mathrm{mech}} / \\xi_{\\mathrm{air}}$")
    ax.set_title("(d) Coupling ratio (mech / airborne) at 120 dB, 0.1 m/s²")
    ax.grid(True, alpha=0.3, which="both")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out = os.path.join(FIG_DIR, "fig_phantom_predictions.png")
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def print_summary(results: dict) -> None:
    """Print a tabular summary of all formulations."""
    print()
    print("=" * 78)
    print("  PHANTOM DESIGN — Predicted Resonant Frequencies")
    print("=" * 78)
    print()
    header = (f"  {'Material':<22} {'E(MPa)':>8} {'f₂(Hz)':>8} "
              f"{'f₃(Hz)':>8} {'f₄(Hz)':>8} {'Q':>6} {'Match?':>8}")
    print(header)
    print("  " + "-" * 72)
    for label, data in results.items():
        f2 = data["freqs"][2]
        f3 = data["freqs"][3]
        f4 = data["freqs"][4]
        Q = data["model"].Q
        match = "YES" if 3.0 <= f2 <= 6.0 else ""
        tag = " ★" if label == "Human (canonical)" else ""
        print(f"  {label + tag:<22} {data['E_MPa']:>8.3f} {f2:>8.2f} "
              f"{f3:>8.2f} {f4:>8.2f} {Q:>6.1f} {match:>8}")
    print("  " + "-" * 72)
    print()
    print("  Target: f₂ in 3–6 Hz range (matching human canonical ≈ 4 Hz)")
    print("  Recommended phantom material: Ecoflex 00-30 or 00-50")
    print("  (closest match to human canonical E ≈ 0.1 MPa)")
    print()

    # Coupling ratio summary
    print("  COUPLING RATIO (mechanical / airborne at resonance)")
    print("  " + "-" * 72)
    print(f"  {'Material':<22} {'ξ_air(μm)':>12} {'ξ_mech(μm)':>12} {'Ratio':>12}")
    print("  " + "-" * 72)
    for label, data in results.items():
        m = data["model"]
        f2 = data["freqs"][2]
        R = m.equivalent_sphere_radius
        Q = m.Q
        D = m.D
        n = 2

        p_inc = 20e-6 * 10**(120 / 20)
        ka = 2 * np.pi * f2 * R / 343.0
        K_b = n*(n-1)*(n+2)**2 * D / R**4
        lam = (n**2+n-2+2*m.nu)/(n**2+n+1-m.nu)
        K_m = m.E * m.h / R**2 * lam
        K_pre = m.P_iap / R * (n-1)*(n+2) if m.P_iap > 0 else 0
        K_total = K_b + K_m + K_pre
        xi_air = p_inc * ka**2 / K_total * Q * 1e6

        omega = 2 * np.pi * f2
        x_base = 0.1 * np.sqrt(2) / omega**2
        xi_mech = x_base * Q * 1e6

        ratio = xi_mech / xi_air if xi_air > 0 else float("inf")
        tag = " ★" if label == "Human (canonical)" else ""
        print(f"  {label + tag:<22} {xi_air:>12.4f} {xi_mech:>12.1f} {ratio:>12.0f}×")
    print("  " + "-" * 72)
    print("  (Airborne: 120 dB SPL at resonance; Mechanical: 0.1 m/s² at resonance)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    results = compute_phantom_predictions()
    print_summary(results)

    fig_path = generate_figure(results)
    print(f"  Figure saved: {fig_path}")
    print()
