"""
Bladder resonance model: predicting natural frequencies of the urinary
bladder as a fluid-filled viscoelastic shell.

Uses the AbdominalModelV2 framework from the browntone project with
bladder-specific parameters. The bladder is modelled as a near-spherical
shell whose geometry and material properties change with fill volume.

Key parameters (from literature):
    Radius:         2.3 cm (50 mL) to 4.9 cm (500 mL)
    Wall thickness:  ~5 mm (empty) to ~3 mm (full) — constant tissue volume
    Young's modulus: 29 kPa (rest) to 145 kPa (distended)
    Poisson's ratio: 0.49 (nearly incompressible)
    Fluid density:   1020 kg/m³ (urine ≈ water)
    Intravesical pressure: 5–30 cmH₂O (490–2940 Pa)

Note on modulus conversion:
    Nenadic (2013) reports SHEAR moduli μ = 9.6–48.7 kPa via ultrasound
    bladder vibrometry. For nearly incompressible tissue (ν = 0.49):
        E = 2(1 + ν)μ = 2.98μ
    giving E = 29–145 kPa. Barnes (2016) tensile tests report E = 10–800 kPa
    depending on layer and stretch ratio, consistent with the converted range.

References:
    - Ultrasound bladder vibrometry (Nenadic 2013): μ = 9.6–48.7 kPa (shear)
    - Barnes (2016) PhD: viscoelastic properties of bladder wall
    - ISO 2631-1:1997: pelvic resonance 4–8 Hz
"""

import sys
import os

sys.path.insert(0, r'C:\Users\jon\OneDrive\Projects\browntone-worktrees\bladder-resonance')
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
    flexural_mode_pressure_response,
)

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIGURES_DIR = os.path.join(os.path.dirname(__file__), 'figures')
PAPER_FIGURES_DIR = os.path.join(os.path.dirname(__file__), 'paper', 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(PAPER_FIGURES_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Bladder geometry from fill volume
# ---------------------------------------------------------------------------

def bladder_radius_from_volume(vol_mL: float) -> float:
    """Equivalent sphere radius [m] from fill volume [mL]."""
    vol_m3 = vol_mL * 1e-6
    return (3 * vol_m3 / (4 * np.pi)) ** (1 / 3)


def bladder_wall_thickness(vol_mL: float) -> float:
    """
    Wall thickness [m] assuming approximately constant tissue volume.

    At 50 mL the wall is ~5 mm; at 500 mL it thins to ~3 mm.
    We assume a fixed tissue shell volume and compute h from that.
    """
    R0 = bladder_radius_from_volume(50.0)
    h0 = 5.0e-3  # 5 mm at 50 mL
    tissue_vol = (4 / 3) * np.pi * ((R0 + h0) ** 3 - R0 ** 3)
    R = bladder_radius_from_volume(vol_mL)
    # Solve (R+h)^3 = R^3 + tissue_vol * 3/(4π)
    h = ((R ** 3 + tissue_vol * 3 / (4 * np.pi)) ** (1 / 3)) - R
    return max(h, 1.5e-3)  # floor at 1.5 mm


def bladder_elastic_modulus(vol_mL: float) -> float:
    """
    Young's modulus [Pa] as a function of fill volume.

    Bladder wall stiffens dramatically with stretch.
    Nenadic (2013) reports shear moduli μ = 9.6–48.7 kPa.
    Converting to Young's modulus for nearly incompressible tissue (ν = 0.49):
        E = 2(1 + ν)μ ≈ 2.98μ
    gives E ≈ 29 kPa (rest) to 145 kPa (distended).
    """
    E_min = 29e3   # 2.98 × 9.6 kPa shear → 29 kPa Young's
    E_max = 145e3  # 2.98 × 48.7 kPa shear → 145 kPa Young's
    frac = np.clip((vol_mL - 50) / 450, 0, 1)
    return E_min * (E_max / E_min) ** frac


def intravesical_pressure(vol_mL: float) -> float:
    """
    Intravesical pressure [Pa] from fill volume.

    Low fill: ~5 cmH₂O ≈ 490 Pa (compliant phase)
    High fill: ~30 cmH₂O ≈ 2940 Pa (steep phase)
    """
    P_min = 490.0    # 5 cmH₂O
    P_max = 2940.0   # 30 cmH₂O
    frac = np.clip((vol_mL - 50) / 450, 0, 1)
    return P_min + (P_max - P_min) * frac ** 2  # convex (compliant then steep)


def make_bladder_model(vol_mL, **overrides):
    """Create AbdominalModelV2 for bladder. Accepts **overrides."""
    R = bladder_radius_from_volume(vol_mL)
    h = bladder_wall_thickness(vol_mL)
    E = bladder_elastic_modulus(vol_mL)
    P = intravesical_pressure(vol_mL)

    params = dict(
        a=R, b=R, c=R,          # spherical
        h=h,
        E=E,
        nu=0.49,                 # nearly incompressible soft tissue
        rho_wall=1050.0,         # tissue density
        loss_tangent=0.4,        # bladder is highly viscous
        rho_fluid=1020.0,        # urine
        K_fluid=2.2e9,           # bulk modulus of water
        P_iap=P,                 # intravesical pressure
    )
    params.update(overrides)
    return AbdominalModelV2(**params)


# M1: Stiffness / mass decomposition
def stiffness_decomposition(vol_mL, n=2, **overrides):
    model = make_bladder_model(vol_mL, **overrides)
    R = model.equivalent_sphere_radius
    E, h, nu = model.E, model.h, model.nu
    rho_w, rho_f = model.rho_wall, model.rho_fluid
    D = model.D
    P = model.P_iap
    K_bend = n * (n - 1) * (n + 2) ** 2 * D / R ** 4
    lambda_n = (n ** 2 + n - 2 + 2 * nu) / (n ** 2 + n + 1 - nu)
    K_memb = E * h / R ** 2 * lambda_n
    K_P = P / R * (n - 1) * (n + 2)
    K_total = K_bend + K_memb + K_P
    m_wall = rho_w * h
    m_fluid = rho_f * R / n
    m_eff = m_wall + m_fluid
    omega_sq = K_total / m_eff
    f_n = np.sqrt(max(0.0, omega_sq)) / (2 * np.pi)
    return dict(vol_mL=vol_mL, n=n, R=R, h=h, E=E, P=P, nu=nu, D=D,
        rho_w=rho_w, rho_f=rho_f, K_bend=K_bend, K_memb=K_memb,
        K_P=K_P, K_total=K_total, lambda_n=lambda_n,
        m_wall=m_wall, m_fluid=m_fluid, m_eff=m_eff, f_n=f_n)

def decomposition_vs_volume(volumes=None, n=2, **overrides):
    if volumes is None:
        volumes = np.linspace(50, 500, 200)
    keys = None
    arrays = {}
    for v in volumes:
        d = stiffness_decomposition(float(v), n=n, **overrides)
        if keys is None:
            keys = [k for k in d if k not in ("n",)]
            arrays = {k: [] for k in keys}
        for k in keys:
            arrays[k].append(d[k])
    return {k: np.asarray(v) for k, v in arrays.items()}

def find_f2_minimum(volumes=None, n=2, **overrides):
    if volumes is None:
        volumes = np.linspace(50, 500, 2000)
    results = [stiffness_decomposition(float(v), n=n, **overrides) for v in volumes]
    freqs = np.array([r["f_n"] for r in results])
    K_vals = np.array([r["K_total"] for r in results])
    m_vals = np.array([r["m_eff"] for r in results])
    idx_min = np.argmin(freqs)
    V_min = volumes[idx_min]
    f_min = freqs[idx_min]
    dlnK = np.gradient(np.log(K_vals), volumes)
    dlnm = np.gradient(np.log(m_vals), volumes)
    diff = dlnK - dlnm
    crossings = np.where(np.diff(np.sign(diff)))[0]
    V_analytic = None
    if len(crossings) > 0:
        i = crossings[0]
        dV = volumes[1] - volumes[0]
        V_analytic = volumes[i] - diff[i] * dV / (diff[i + 1] - diff[i])
    return dict(V_min=V_min, f_min=f_min, V_analytic=V_analytic,
                volumes=volumes, freqs=freqs, dlnK_dV=dlnK, dlnm_dV=dlnm)

SENSITIVITY_PARAMS = {
    "E":            (10e3,   500e3,  "$E$ (wall modulus)",              "kPa"),
    "h":            (2e-3,   6e-3,   "$h$ (wall thickness)",            "mm"),
    "rho_fluid":    (1010.0, 1030.0, r"$\rho_f$ (urine density)",      r"kg/m$^3$"),
    "nu":           (0.40,   0.50,   r"$\nu$ (Poisson ratio)",         ""),
    "loss_tangent": (0.30,   0.50,   r"$\eta$ (loss tangent)",         ""),
}

def sensitivity_analysis(vol_mL=170.0, n=2):
    f_base = stiffness_decomposition(vol_mL, n=n)["f_n"]
    results = {}
    for pname, (lo, hi, label, unit) in SENSITIVITY_PARAMS.items():
        f_lo = stiffness_decomposition(vol_mL, n=n, **{pname: lo})["f_n"]
        f_hi = stiffness_decomposition(vol_mL, n=n, **{pname: hi})["f_n"]
        delta_f = max(abs(f_hi - f_base), abs(f_lo - f_base))
        results[pname] = dict(label=label, unit=unit, lo=lo, hi=hi,
            f_lo=f_lo, f_hi=f_hi, f_base=f_base,
            delta_f=delta_f, pct=delta_f / f_base * 100)
    return results

def minimum_shift_analysis(n=2):
    base = find_f2_minimum(n=n)
    results = {"_base": dict(V_min=base["V_min"], f_min=base["f_min"])}
    vols = np.linspace(50, 500, 2000)
    for pname, (lo, hi, label, unit) in SENSITIVITY_PARAMS.items():
        for tag, val in [("lo", lo), ("hi", hi)]:
            freqs = np.array([
                stiffness_decomposition(float(v), n=n, **{pname: val})["f_n"]
                for v in vols])
            idx = np.argmin(freqs)
            results[pname + "_" + tag] = dict(
                V_min=vols[idx], f_min=freqs[idx], label=label)
    return results

# ---------------------------------------------------------------------------
# Parametric study: frequency vs fill volume
# ---------------------------------------------------------------------------

def parametric_frequency_vs_volume():
    """Compute f₂ and f₃ across fill volumes."""
    volumes = np.linspace(50, 500, 50)
    f2_vals, f3_vals = [], []
    radii, thicknesses, moduli, pressures = [], [], [], []

    for v in volumes:
        model = make_bladder_model(v)
        freqs = flexural_mode_frequencies_v2(model, n_max=4)
        f2_vals.append(freqs[2])
        f3_vals.append(freqs[3])
        radii.append(bladder_radius_from_volume(v) * 100)  # cm
        thicknesses.append(bladder_wall_thickness(v) * 1000)  # mm
        moduli.append(bladder_elastic_modulus(v) / 1e3)  # kPa
        pressures.append(intravesical_pressure(v))  # Pa

    return {
        'volumes': volumes,
        'f2': np.array(f2_vals),
        'f3': np.array(f3_vals),
        'radii': np.array(radii),
        'thicknesses': np.array(thicknesses),
        'moduli': np.array(moduli),
        'pressures': np.array(pressures),
    }


def plot_frequency_vs_volume(data: dict):
    """Generate fig_bladder_frequency_vs_volume.png."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('Bladder Resonant Frequency vs Fill Volume', fontsize=14, fontweight='bold')

    # (a) f₂ and f₃ vs volume
    ax = axes[0, 0]
    ax.plot(data['volumes'], data['f2'], 'b-', linewidth=2, label='n = 2 (oblate-prolate)')
    ax.plot(data['volumes'], data['f3'], 'r--', linewidth=2, label='n = 3')
    ax.axhspan(4, 8, alpha=0.15, color='orange', label='ISO 2631 pelvic range (4–8 Hz)')
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_title('(a) Flexural Mode Frequencies')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (b) Geometry vs volume
    ax = axes[0, 1]
    ax2 = ax.twinx()
    ln1 = ax.plot(data['volumes'], data['radii'], 'g-', linewidth=2, label='Radius [cm]')
    ln2 = ax2.plot(data['volumes'], data['thicknesses'], 'm--', linewidth=2, label='Wall thickness [mm]')
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('Radius [cm]', color='g')
    ax2.set_ylabel('Wall Thickness [mm]', color='m')
    ax.set_title('(b) Geometry vs Fill State')
    lns = ln1 + ln2
    ax.legend(lns, [l.get_label() for l in lns], fontsize=8)
    ax.grid(True, alpha=0.3)

    # (c) Elastic modulus vs volume
    ax = axes[1, 0]
    ax.plot(data['volumes'], data['moduli'], 'k-', linewidth=2)
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('E [kPa]')
    ax.set_title('(c) Wall Elastic Modulus (Strain-Stiffening)')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)

    # (d) Intravesical pressure vs volume
    ax = axes[1, 1]
    ax.plot(data['volumes'], data['pressures'] / 98.0665, 'brown', linewidth=2)
    ax.set_xlabel('Fill Volume [mL]')
    ax.set_ylabel('Intravesical Pressure [cmH₂O]')
    ax.set_title('(d) Cystometric Pressure Curve')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, 'fig_bladder_frequency_vs_volume.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {path}')
    return path


# ---------------------------------------------------------------------------
# Coupling analysis: airborne vs mechanical
# ---------------------------------------------------------------------------

def coupling_analysis():
    """
    Compare airborne acoustic coupling vs mechanical (WBV) coupling.

    Airborne: pressure gradient coupling scales as (ka)^n — very weak.
    Mechanical: direct displacement input from pelvic vibration — full coupling.
    """
    vol = 300.0  # typical "need to go" volume
    model = make_bladder_model(vol)
    R = model.equivalent_sphere_radius
    freqs = flexural_mode_frequencies_v2(model, n_max=6)
    f2 = freqs[2]

    freq_range = np.linspace(1, 20, 200)

    # Airborne coupling: (ka)^2 for n=2
    c_air = 343.0
    ka_vals = 2 * np.pi * freq_range * R / c_air
    airborne_coupling = ka_vals ** 2

    # Mechanical coupling: direct pelvic vibration
    # Transmissibility from seat to pelvis (ISO 2631 weighted)
    # Peak around 4-8 Hz with transmissibility ~1.5
    # Model as a resonant response with f_pelvis ≈ 5 Hz, Q ≈ 2
    f_pelvis = 5.5  # Hz, pelvic resonance
    zeta_pelvis = 0.25
    r_pelvis = freq_range / f_pelvis
    T_pelvis = np.sqrt((1 + (2 * zeta_pelvis * r_pelvis) ** 2) /
                       ((1 - r_pelvis ** 2) ** 2 + (2 * zeta_pelvis * r_pelvis) ** 2))

    # Bladder modal amplification (n=2)
    zeta_bladder = model.damping_ratio
    r_bladder = freq_range / f2
    H_bladder = 1 / np.sqrt((1 - r_bladder ** 2) ** 2 + (2 * zeta_bladder * r_bladder) ** 2)

    # Combined mechanical coupling: seat → pelvis → bladder wall
    mechanical_coupling = T_pelvis * H_bladder

    # Coupling ratio
    ratio = mechanical_coupling / airborne_coupling

    return {
        'freq': freq_range,
        'f2': f2,
        'ka': ka_vals,
        'airborne': airborne_coupling,
        'T_pelvis': T_pelvis,
        'H_bladder': H_bladder,
        'mechanical': mechanical_coupling,
        'ratio': ratio,
    }


def plot_coupling(data: dict):
    """Generate fig_bladder_coupling.png."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        f'Coupling Pathways to Bladder (300 mL, f₂ = {data["f2"]:.1f} Hz)',
        fontsize=13, fontweight='bold',
    )

    # (a) Airborne vs mechanical
    ax = axes[0]
    ax.semilogy(data['freq'], data['airborne'], 'b-', linewidth=2, label='Airborne (ka)²')
    ax.semilogy(data['freq'], data['mechanical'], 'r-', linewidth=2, label='Mechanical (seat→pelvis→bladder)')
    ax.axvline(data['f2'], color='gray', ls=':', label=f'f₂ = {data["f2"]:.1f} Hz')
    ax.axvspan(4, 8, alpha=0.1, color='orange')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Effective Coupling (normalised)')
    ax.set_title('(a) Coupling Pathways')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (b) Coupling ratio
    ax = axes[1]
    ax.semilogy(data['freq'], data['ratio'], 'k-', linewidth=2)
    ax.axvline(data['f2'], color='gray', ls=':')
    ax.axhspan(1, 1, color='gray')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Mechanical / Airborne Ratio')
    ax.set_title('(b) Mechanical Advantage')
    ax.grid(True, alpha=0.3)

    # (c) Components of mechanical path
    ax = axes[2]
    ax.plot(data['freq'], data['T_pelvis'], 'g-', linewidth=2, label='Seat→Pelvis transmissibility')
    ax.plot(data['freq'], data['H_bladder'], 'm--', linewidth=2, label='Bladder modal amplification')
    ax.axvline(data['f2'], color='gray', ls=':', label=f'f₂ = {data["f2"]:.1f} Hz')
    ax.axvspan(4, 8, alpha=0.1, color='orange', label='ISO 2631 range')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplification Factor')
    ax.set_title('(c) Mechanical Pathway Components')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, 'fig_bladder_coupling.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {path}')
    return path


# ---------------------------------------------------------------------------
# Console report
# ---------------------------------------------------------------------------

def plot_stiffness_mass_decomposition(save_paper=True):
    data = decomposition_vs_volume()
    vols = data["vol_mL"]
    mi = find_f2_minimum()
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle(r"Stiffness / Mass Decomposition of $f_2$ vs Fill Volume", fontsize=14, fontweight="bold")
    ax = axes[0, 0]
    ax.semilogy(vols, data["K_bend"], "b-", lw=2, label=r"$K_\mathrm{bend}$")
    ax.semilogy(vols, data["K_memb"], "g-", lw=2, label=r"$K_\mathrm{memb}$")
    ax.semilogy(vols, data["K_P"], "r-", lw=2, label=r"$K_P$ (pre-stress)")
    ax.semilogy(vols, data["K_total"], "k--", lw=2.5, label=r"$K_\mathrm{total}$")
    if mi["V_min"] is not None: ax.axvline(mi["V_min"], color="grey", ls=":", alpha=0.5)
    ax.set(xlabel="Fill Volume [mL]", ylabel="Stiffness [Pa/m]", title="(a) Stiffness Components")
    ax.legend(fontsize=8, loc="upper left"); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    ax.plot(vols, data["m_wall"], "b-", lw=2, label=r"$m_\mathrm{wall} = \rho_w h$")
    ax.plot(vols, data["m_fluid"], "r-", lw=2, label=r"$m_\mathrm{fluid} = \rho_f R/n$")
    ax.plot(vols, data["m_eff"], "k--", lw=2.5, label=r"$m_\mathrm{eff}$")
    if mi["V_min"] is not None: ax.axvline(mi["V_min"], color="grey", ls=":", alpha=0.5)
    ax.set(xlabel="Fill Volume [mL]", ylabel=r"Mass per unit area [kg/m$^2$]", title="(b) Effective Mass Components")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    ax.plot(vols, data["f_n"], "b-", lw=2.5)
    if mi["V_min"] is not None:
        ax.plot(mi["V_min"], mi["f_min"], "ro", ms=10, zorder=5)
        ax.annotate("$V^* = %d$ mL\n$f_2^\\mathrm{min} = %.1f$ Hz" % (mi["V_min"], mi["f_min"]),
            xy=(mi["V_min"], mi["f_min"]), xytext=(mi["V_min"] + 80, mi["f_min"] + 1.5), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="red", alpha=0.9))
    ax.axhspan(4, 8, alpha=0.12, color="orange", label="ISO 2631 range")
    ax.set(xlabel="Fill Volume [mL]", ylabel=r"$f_2$ [Hz]", title=r"(c) $n=2$ Mode Frequency")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    ax.plot(mi["volumes"], mi["dlnK_dV"] * 1e3, "r-", lw=2, label=r"$\mathrm{d}(\ln K_\mathrm{total})/\mathrm{d}V$")
    ax.plot(mi["volumes"], mi["dlnm_dV"] * 1e3, "b-", lw=2, label=r"$\mathrm{d}(\ln m_\mathrm{eff})/\mathrm{d}V$")
    ax.axhline(0, color="grey", ls="-", alpha=0.3)
    if mi["V_analytic"] is not None: ax.axvline(mi["V_analytic"], color="grey", ls=":", alpha=0.5, label="crossing at %d mL" % mi["V_analytic"])
    ax.set(xlabel="Fill Volume [mL]", ylabel=r"Log-rate [$\times 10^{-3}$ mL$^{-1}$]", title=r"(d) Condition $\partial f_2 / \partial V = 0$")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_stiffness_mass_decomposition.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    if save_paper:
        pp = os.path.join(PAPER_FIGURES_DIR, "fig_stiffness_mass_decomposition.pdf")
        fig.savefig(pp, bbox_inches="tight"); print("  Saved:", pp)
    plt.close(fig); print("  Saved:", path); return path

def plot_tornado_chart(vol_mL=170.0, save_paper=True):
    sens = sensitivity_analysis(vol_mL=vol_mL)
    f_base = list(sens.values())[0]["f_base"]
    items = sorted(sens.items(), key=lambda x: x[1]["delta_f"])
    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(items))
    for i, (pname, v) in enumerate(items):
        left, right = min(v["f_lo"], v["f_hi"]), max(v["f_lo"], v["f_hi"])
        ax.barh(i, right - left, left=left, height=0.6, color="steelblue", alpha=0.8, edgecolor="navy")
        ax.text(right + 0.15, i, r"$\Delta f_2 = %.1f$ Hz (%.0f%%)" % (v["delta_f"], v["pct"]), va="center", fontsize=9)
    ax.axvline(f_base, color="red", ls="--", lw=1.5, label="Baseline $f_2 = %.1f$ Hz" % f_base)
    ax.set_yticks(y_pos); ax.set_yticklabels([v["label"] for _, v in items], fontsize=10)
    ax.set_xlabel(r"$f_2$ [Hz]", fontsize=11)
    ax.set_title("Tornado Chart: Parameter Sensitivity at $V = %d$ mL" % vol_mL, fontsize=13, fontweight="bold")
    ax.legend(fontsize=9); ax.grid(True, axis="x", alpha=0.3); plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_tornado_sensitivity.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    if save_paper:
        pp = os.path.join(PAPER_FIGURES_DIR, "fig_tornado_sensitivity.pdf")
        fig.savefig(pp, bbox_inches="tight"); print("  Saved:", pp)
    plt.close(fig); print("  Saved:", path); return path

def plot_minimum_shift(save_paper=True):
    shifts = minimum_shift_analysis()
    base_V, base_f = shifts["_base"]["V_min"], shifts["_base"]["f_min"]
    rows = [(label, shifts[pname + "_lo"]["V_min"], shifts[pname + "_hi"]["V_min"], shifts[pname + "_lo"]["f_min"], shifts[pname + "_hi"]["f_min"]) for pname, (lo, hi, label, unit) in SENSITIVITY_PARAMS.items()]
    rows.sort(key=lambda r: abs(r[2] - r[1]))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    y_pos = np.arange(len(rows))
    for i, (label, V_lo, V_hi, f_lo, f_hi) in enumerate(rows):
        ax1.barh(i, max(V_lo,V_hi)-min(V_lo,V_hi), left=min(V_lo,V_hi), height=0.6, color="coral", alpha=0.8, edgecolor="darkred")
        ax1.text(max(V_lo,V_hi)+5, i, "%d--%d mL" % (min(V_lo,V_hi), max(V_lo,V_hi)), va="center", fontsize=9)
        ax2.barh(i, max(f_lo,f_hi)-min(f_lo,f_hi), left=min(f_lo,f_hi), height=0.6, color="steelblue", alpha=0.8, edgecolor="navy")
        ax2.text(max(f_lo,f_hi)+0.15, i, "%.1f--%.1f Hz" % (min(f_lo,f_hi), max(f_lo,f_hi)), va="center", fontsize=9)
    ax1.axvline(base_V, color="red", ls="--", lw=1.5, label="Baseline $V^* = %d$ mL" % base_V)
    ax1.set_yticks(y_pos); ax1.set_yticklabels([r[0] for r in rows], fontsize=10)
    ax1.set_xlabel("Volume at $f_2$ Minimum [mL]"); ax1.set_title("(a) Shift in $V^*$")
    ax1.legend(fontsize=9); ax1.grid(True, axis="x", alpha=0.3)
    ax2.axvline(base_f, color="red", ls="--", lw=1.5, label=r"Baseline $f_2^\mathrm{min} = %.1f$ Hz" % base_f)
    ax2.set_yticks(y_pos); ax2.set_yticklabels([r[0] for r in rows], fontsize=10)
    ax2.set_xlabel(r"$f_2^\mathrm{min}$ [Hz]"); ax2.set_title(r"(b) Shift in $f_2^\mathrm{min}$")
    ax2.legend(fontsize=9); ax2.grid(True, axis="x", alpha=0.3)
    fig.suptitle(r"Robustness of the $f_2$ Minimum to Parameter Uncertainty", fontsize=13, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_minimum_shift.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    if save_paper:
        pp = os.path.join(PAPER_FIGURES_DIR, "fig_minimum_shift.pdf")
        fig.savefig(pp, bbox_inches="tight"); print("  Saved:", pp)
    plt.close(fig); print("  Saved:", path); return path

def print_report(param_data, coupling_data):
    print("\n" + "=" * 72 + "\n  BLADDER RESONANCE MODEL\n" + "=" * 72)
    mi = find_f2_minimum()
    d = stiffness_decomposition(mi["V_min"])
    print("\n  f2 MINIMUM: V*=%d mL, f2=%.1f Hz" % (mi["V_min"], mi["f_min"]))
    print("  K_bend=%5.1f%% K_memb=%5.1f%% K_P=%5.1f%%" % (d["K_bend"]/d["K_total"]*100, d["K_memb"]/d["K_total"]*100, d["K_P"]/d["K_total"]*100))
    print()

if __name__ == '__main__':
    print('\n  Computing...')
    param_data = parametric_frequency_vs_volume()
    plot_frequency_vs_volume(param_data)
    coupling_data = coupling_analysis()
    plot_coupling(coupling_data)
    plot_stiffness_mass_decomposition()
    plot_tornado_chart()
    plot_minimum_shift()
    print_report(param_data, coupling_data)