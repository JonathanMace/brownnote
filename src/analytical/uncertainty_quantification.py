"""
Monte Carlo uncertainty quantification for the abdominal resonance model.

Propagates parameter uncertainty through the flexural mode model to produce
confidence intervals on all key output quantities. Includes Sobol sensitivity
analysis to identify which parameters dominate the uncertainty budget.

Usage:
    python -m src.analytical.uncertainty_quantification

Outputs:
    data/results/uq_results.json   — numerical results
    data/figures/fig_uq_frequency_histogram.png
    data/figures/fig_uq_sobol_indices.png
    data/figures/fig_uq_coupling_ratio_distribution.png
"""

import json
import os
import sys
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
    flexural_mode_pressure_response,
)

# SALib for Sobol indices
try:
    from SALib.sample import sobol as saltelli_sample
except ImportError:
    from SALib.sample import saltelli as saltelli_sample
from SALib.analyze import sobol as sobol_analyze

# ---------------------------------------------------------------------------
# Constants & output paths
# ---------------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIG_DIR = os.path.join(ROOT, "data", "figures")
RES_DIR = os.path.join(ROOT, "data", "results")

N_MC = 10_000          # Monte Carlo samples
N_SOBOL = 4096         # Saltelli base samples (total = N*(2D+2))
SPL_DB = 120.0         # dB SPL for airborne excitation
ACCEL_RMS = 0.5        # m/s² RMS for mechanical excitation
PIEZO_THRESHOLD = 1.0  # µm displacement for piezo threshold
C_AIR = 343.0          # speed of sound in air [m/s]
P_REF = 20e-6          # reference pressure [Pa]
MODE_N = 2             # flexural mode of interest

# ---------------------------------------------------------------------------
# Parameter distributions
# ---------------------------------------------------------------------------
PARAM_DEFS = {
    "E":            {"nominal": 0.1e6,  "dist": "lognormal", "low": 0.05e6, "high": 2.0e6},
    "a":            {"nominal": 0.18,   "dist": "normal",    "low": 0.15,   "high": 0.22},
    "c":            {"nominal": 0.12,   "dist": "normal",    "low": 0.08,   "high": 0.15},
    "h":            {"nominal": 0.01,   "dist": "normal",    "low": 0.005,  "high": 0.02},
    "nu":           {"nominal": 0.45,   "dist": "uniform",   "low": 0.40,   "high": 0.499},
    "rho_wall":     {"nominal": 1100.0, "dist": "normal",    "low": 1000.0, "high": 1200.0},
    "rho_fluid":    {"nominal": 1020.0, "dist": "normal",    "low": 1000.0, "high": 1060.0},
    "P_iap":        {"nominal": 1000.0, "dist": "lognormal", "low": 500.0,  "high": 3000.0},
    "loss_tangent": {"nominal": 0.25,   "dist": "uniform",   "low": 0.10,   "high": 0.40},
}

PARAM_NAMES = list(PARAM_DEFS.keys())
N_PARAMS = len(PARAM_NAMES)


# ---------------------------------------------------------------------------
# Sampling helpers
# ---------------------------------------------------------------------------
def _lognormal_params(low, high):
    """Return (mu, sigma) for a log-normal whose 5th–95th percentile spans [low, high]."""
    ln_low, ln_high = np.log(low), np.log(high)
    # 5th & 95th quantiles are at ±1.645σ from μ
    mu = (ln_low + ln_high) / 2
    sigma = (ln_high - ln_low) / (2 * 1.645)
    return mu, sigma


def _normal_params(low, high):
    """Return (mu, sigma) for a normal whose 5th–95th percentile spans [low, high]."""
    mu = (low + high) / 2
    sigma = (high - low) / (2 * 1.645)
    return mu, sigma


def sample_parameters(n: int, rng: np.random.Generator) -> np.ndarray:
    """Draw *n* independent samples for all 9 parameters.  Returns (n, 9) array."""
    samples = np.empty((n, N_PARAMS))
    for j, name in enumerate(PARAM_NAMES):
        d = PARAM_DEFS[name]
        if d["dist"] == "lognormal":
            mu, sigma = _lognormal_params(d["low"], d["high"])
            samples[:, j] = rng.lognormal(mu, sigma, size=n)
        elif d["dist"] == "normal":
            mu, sigma = _normal_params(d["low"], d["high"])
            samples[:, j] = rng.normal(mu, sigma, size=n)
        elif d["dist"] == "uniform":
            samples[:, j] = rng.uniform(d["low"], d["high"], size=n)
    return samples


# ---------------------------------------------------------------------------
# Model evaluation
# ---------------------------------------------------------------------------
def build_model(params: np.ndarray) -> AbdominalModelV2:
    """Construct an AbdominalModelV2 from a 9-element parameter vector."""
    E, a, c, h, nu, rho_wall, rho_fluid, P_iap, loss_tangent = params
    return AbdominalModelV2(
        E=float(E),
        a=float(a),
        b=float(a),          # oblate spheroid: b = a
        c=float(c),
        h=float(h),
        nu=float(np.clip(nu, 0.01, 0.4999)),
        rho_wall=float(rho_wall),
        rho_fluid=float(rho_fluid),
        P_iap=float(P_iap),
        loss_tangent=float(loss_tangent),
    )


def evaluate_sample(params: np.ndarray) -> dict:
    """Evaluate the model for one parameter vector.  Returns dict of outputs."""
    model = build_model(params)
    freqs = flexural_mode_frequencies_v2(model, n_max=MODE_N)
    f_n2 = freqs[MODE_N]

    # --- Airborne displacement at SPL_DB ---
    resp_air = flexural_mode_pressure_response(f_n2, SPL_DB, MODE_N, model)
    xi_air_um = resp_air["displacement_um"]

    # --- Mechanical displacement at ACCEL_RMS ---
    R = model.equivalent_sphere_radius
    omega_n = 2 * np.pi * f_n2
    omega = omega_n  # evaluate at resonance
    zeta = model.damping_ratio
    # Base displacement at resonance frequency
    x_base = ACCEL_RMS * np.sqrt(2) / omega_n**2 if omega_n > 0 else 0.0
    # Relative displacement FRF at resonance: r=1 → H_rel = 1/(2ζ)
    H_rel = 1.0 / (2 * zeta) if zeta > 0 else 0.0
    xi_mech_m = x_base * H_rel
    xi_mech_um = xi_mech_m * 1e6

    # Coupling ratio
    R_coupling = xi_mech_um / xi_air_um if xi_air_um > 0 else np.inf

    # SPL needed for PIEZO threshold (1 µm) via airborne path
    # ξ ∝ p_inc, so SPL_needed = SPL_DB + 20*log10(threshold / ξ_air)
    if xi_air_um > 0 and xi_air_um < PIEZO_THRESHOLD:
        spl_piezo = SPL_DB + 20 * np.log10(PIEZO_THRESHOLD / xi_air_um)
    elif xi_air_um >= PIEZO_THRESHOLD:
        spl_piezo = SPL_DB
    else:
        spl_piezo = np.nan

    return {
        "f_n2": f_n2,
        "xi_air_um": xi_air_um,
        "xi_mech_um": xi_mech_um,
        "R_coupling": R_coupling,
        "spl_piezo": spl_piezo,
    }


def evaluate_batch(param_matrix: np.ndarray) -> dict:
    """Evaluate all samples.  Returns dict of 1-D arrays."""
    n = param_matrix.shape[0]
    keys = ["f_n2", "xi_air_um", "xi_mech_um", "R_coupling", "spl_piezo"]
    out = {k: np.empty(n) for k in keys}
    for i in range(n):
        try:
            r = evaluate_sample(param_matrix[i])
        except Exception:
            r = {k: np.nan for k in keys}
        for k in keys:
            out[k][i] = r[k]
    return out


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
def summarise(arr: np.ndarray, label: str) -> dict:
    """Compute summary statistics, ignoring NaN / Inf."""
    valid = arr[np.isfinite(arr)]
    if len(valid) == 0:
        return {f"{label}_mean": None}
    return {
        f"{label}_mean":   float(np.mean(valid)),
        f"{label}_median": float(np.median(valid)),
        f"{label}_std":    float(np.std(valid)),
        f"{label}_p5":     float(np.percentile(valid, 5)),
        f"{label}_p95":    float(np.percentile(valid, 95)),
        f"{label}_ci99_lo": float(np.percentile(valid, 0.5)),
        f"{label}_ci99_hi": float(np.percentile(valid, 99.5)),
        f"{label}_n_valid": int(len(valid)),
    }


# ---------------------------------------------------------------------------
# Sobol sensitivity analysis
# ---------------------------------------------------------------------------
def run_sobol(n_base: int = N_SOBOL) -> dict:
    """
    Compute first-order and total Sobol indices for f_n2.

    Uses SALib's Saltelli sampling (generates N*(2D+2) evaluations) and the
    Sobol analyser.  We map each parameter to a uniform [0,1] draw and then
    apply the inverse-CDF to obtain the physical value.
    """
    problem = {
        "num_vars": N_PARAMS,
        "names": PARAM_NAMES,
        "bounds": [[0.0, 1.0]] * N_PARAMS,  # unit hypercube
    }

    # Saltelli sample on [0,1]^D
    X_unit = saltelli_sample.sample(problem, n_base, calc_second_order=False)
    n_total = X_unit.shape[0]

    # Map from uniform [0,1] to physical distributions via inverse CDF
    X_phys = np.empty_like(X_unit)
    for j, name in enumerate(PARAM_NAMES):
        d = PARAM_DEFS[name]
        u = X_unit[:, j]
        if d["dist"] == "lognormal":
            mu, sigma = _lognormal_params(d["low"], d["high"])
            from scipy.stats import lognorm
            # scipy lognorm: shape=sigma, scale=exp(mu)
            X_phys[:, j] = lognorm.ppf(u, s=sigma, scale=np.exp(mu))
        elif d["dist"] == "normal":
            mu_n, sigma_n = _normal_params(d["low"], d["high"])
            from scipy.stats import norm
            X_phys[:, j] = norm.ppf(u, loc=mu_n, scale=sigma_n)
        elif d["dist"] == "uniform":
            X_phys[:, j] = d["low"] + u * (d["high"] - d["low"])

    # Evaluate model for each sample
    print(f"  Sobol analysis: evaluating {n_total} samples …")
    results = evaluate_batch(X_phys)

    # Analyse each output quantity
    sobol_results = {}
    for key in ["f_n2", "xi_air_um", "xi_mech_um", "R_coupling"]:
        Y = results[key].copy()
        # Replace non-finite with median to avoid crashing the analyser
        median_val = np.nanmedian(Y)
        Y[~np.isfinite(Y)] = median_val
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Si = sobol_analyze.analyze(problem, Y, calc_second_order=False)
        sobol_results[key] = {
            "S1": {name: float(Si["S1"][j]) for j, name in enumerate(PARAM_NAMES)},
            "ST": {name: float(Si["ST"][j]) for j, name in enumerate(PARAM_NAMES)},
        }

    return sobol_results


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_frequency_histogram(f_arr: np.ndarray, stats: dict, path: str):
    valid = f_arr[np.isfinite(f_arr)]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(valid, bins=80, density=True, color="#4C72B0", alpha=0.85, edgecolor="white", linewidth=0.3)

    mean = stats["f_n2_mean"]
    p5, p95 = stats["f_n2_p5"], stats["f_n2_p95"]
    ax.axvline(mean, color="crimson", ls="--", lw=1.5, label=f"Mean = {mean:.2f} Hz")
    ax.axvspan(p5, p95, alpha=0.15, color="crimson", label=f"90% CI [{p5:.1f}, {p95:.1f}] Hz")

    ax.set_xlabel("$f_{{n=2}}$ Flexural Frequency [Hz]", fontsize=12)
    ax.set_ylabel("Probability Density", fontsize=12)
    ax.set_title("Monte Carlo Distribution of $n=2$ Flexural Frequency\n"
                  f"($N = {len(valid):,}$ samples)", fontsize=13)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(f"  Saved {path}")


def plot_sobol_indices(sobol_results: dict, path: str):
    # Use f_n2 for the bar chart (primary output)
    si_f = sobol_results["f_n2"]
    names = PARAM_NAMES
    s1 = np.array([si_f["S1"][n] for n in names])
    st = np.array([si_f["ST"][n] for n in names])

    # Sort by total-order
    order = np.argsort(st)[::-1]
    names_sorted = [names[i] for i in order]
    s1_sorted = s1[order]
    st_sorted = st[order]

    # Pretty labels
    pretty = {
        "E": "$E$ (elastic mod.)",
        "a": "$a$ (semi-major)",
        "c": "$c$ (semi-minor)",
        "h": "$h$ (wall thick.)",
        "nu": r"$\nu$ (Poisson)",
        "rho_wall": r"$\rho_w$ (wall dens.)",
        "rho_fluid": r"$\rho_f$ (fluid dens.)",
        "P_iap": "$P_{\\rm iap}$ (pressure)",
        "loss_tangent": "$\\tan\\delta$ (loss)",
    }
    labels = [pretty.get(n, n) for n in names_sorted]

    x = np.arange(len(labels))
    w = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(x + w/2, s1_sorted, height=w, color="#4C72B0", label="First-order $S_1$")
    ax.barh(x - w/2, st_sorted, height=w, color="#DD8452", label="Total-order $S_T$")
    ax.set_yticks(x)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("Sobol Sensitivity Index", fontsize=12)
    ax.set_title("Sobol Indices for $f_{{n=2}}$", fontsize=13)
    ax.legend(fontsize=10, loc="lower right")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(f"  Saved {path}")


def plot_coupling_ratio(R_arr: np.ndarray, path: str):
    valid = R_arr[np.isfinite(R_arr) & (R_arr < 1e12)]
    log_R = np.log10(np.clip(valid, 1e-3, None))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(log_R, bins=80, density=True, color="#55A868", alpha=0.85, edgecolor="white", linewidth=0.3)

    med = np.median(log_R)
    ax.axvline(med, color="crimson", ls="--", lw=1.5,
               label=f"Median $R$ = $10^{{{med:.1f}}}$ = {10**med:.0f}")

    ax.set_xlabel(r"$\log_{10}(R)$ where $R = \xi_{\rm mech} / \xi_{\rm air}$", fontsize=12)
    ax.set_ylabel("Probability Density", fontsize=12)
    ax.set_title("Distribution of Mechanical / Airborne Coupling Ratio\n"
                  f"($N = {len(valid):,}$ samples)", fontsize=13)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# LaTeX-ready formatting
# ---------------------------------------------------------------------------
def latex_summary(stats: dict, sobol: dict) -> str:
    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append("  UNCERTAINTY QUANTIFICATION — LaTeX-Ready Summary")
    lines.append("=" * 72)
    lines.append("")

    def _ci(key, unit, fmt=".1f"):
        m   = stats.get(f"{key}_mean")
        sd  = stats.get(f"{key}_std")
        p5  = stats.get(f"{key}_p5")
        p95 = stats.get(f"{key}_p95")
        c99lo = stats.get(f"{key}_ci99_lo")
        c99hi = stats.get(f"{key}_ci99_hi")
        if m is None:
            return f"  {key}: insufficient data"
        return (
            f"  ${key.replace('_',',')}$ = {m:{fmt}} $\\pm$ {sd:{fmt}} {unit}  "
            f"(90\\% CI: {p5:{fmt}}--{p95:{fmt}}; 99\\% CI: {c99lo:{fmt}}--{c99hi:{fmt}})"
        )

    lines.append("  Key results (Monte Carlo, N = {:,}):".format(N_MC))
    lines.append("")

    m  = stats["f_n2_mean"]
    sd = stats["f_n2_std"]
    p5 = stats["f_n2_p5"]
    p95 = stats["f_n2_p95"]
    lines.append(f"  $f_2 = {m:.1f} \\pm {sd:.1f}$ Hz  (90% CI: {p5:.1f}--{p95:.1f} Hz)")

    m  = stats["xi_air_um_mean"]
    sd = stats["xi_air_um_std"]
    p5 = stats["xi_air_um_p5"]
    p95 = stats["xi_air_um_p95"]
    lines.append(f"  $\\xi_{{\\rm air}}$ at {SPL_DB:.0f} dB = {m:.4f} $\\pm$ {sd:.4f} µm  "
                 f"(90% CI: {p5:.4f}--{p95:.4f})")

    m  = stats["xi_mech_um_mean"]
    sd = stats["xi_mech_um_std"]
    p5 = stats["xi_mech_um_p5"]
    p95 = stats["xi_mech_um_p95"]
    lines.append(f"  $\\xi_{{\\rm mech}}$ at {ACCEL_RMS} m/s² = {m:.1f} $\\pm$ {sd:.1f} µm  "
                 f"(90% CI: {p5:.1f}--{p95:.1f})")

    m  = stats["R_coupling_mean"]
    md = stats["R_coupling_median"]
    p5 = stats["R_coupling_p5"]
    p95 = stats["R_coupling_p95"]
    lines.append(f"  Coupling ratio $R$ median = {md:.0f}  "
                 f"(90% CI: {p5:.0f}--{p95:.0f})")

    m  = stats["spl_piezo_mean"]
    md = stats["spl_piezo_median"]
    p5 = stats["spl_piezo_p5"]
    p95 = stats["spl_piezo_p95"]
    lines.append(f"  SPL for 1 µm (piezo) = {md:.0f} dB  "
                 f"(90% CI: {p5:.0f}--{p95:.0f} dB)")

    lines.append("")
    lines.append("  Dominant parameters (Sobol total-order for f_n2):")
    si_f = sobol["f_n2"]
    ranked = sorted(si_f["ST"].items(), key=lambda x: -x[1])
    for name, st in ranked:
        s1 = si_f["S1"][name]
        lines.append(f"    {name:>15}:  S1 = {s1:.3f},  ST = {st:.3f}")

    lines.append("")
    lines.append("=" * 72)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    os.makedirs(RES_DIR, exist_ok=True)

    rng = np.random.default_rng(seed=42)

    # ---- Monte Carlo ----
    print("\n  ── Monte Carlo Simulation ──")
    print(f"  Sampling {N_MC:,} parameter sets …")
    X = sample_parameters(N_MC, rng)
    print(f"  Evaluating model …")
    mc = evaluate_batch(X)
    print(f"  Done.")

    # Statistics
    all_stats = {}
    for key in ["f_n2", "xi_air_um", "xi_mech_um", "R_coupling", "spl_piezo"]:
        all_stats.update(summarise(mc[key], key))

    # ---- Sobol ----
    print("\n  ── Sobol Sensitivity Analysis ──")
    sobol = run_sobol(N_SOBOL)
    print("  Done.")

    # ---- Figures ----
    print("\n  ── Generating Figures ──")
    plot_frequency_histogram(
        mc["f_n2"], all_stats,
        os.path.join(FIG_DIR, "fig_uq_frequency_histogram.png"),
    )
    plot_sobol_indices(
        sobol,
        os.path.join(FIG_DIR, "fig_uq_sobol_indices.png"),
    )
    plot_coupling_ratio(
        mc["R_coupling"],
        os.path.join(FIG_DIR, "fig_uq_coupling_ratio_distribution.png"),
    )

    # ---- LaTeX summary ----
    summary = latex_summary(all_stats, sobol)
    print(summary)

    # ---- Save JSON ----
    json_out = {
        "meta": {
            "N_MC": N_MC,
            "N_SOBOL_base": N_SOBOL,
            "SPL_dB": SPL_DB,
            "accel_rms_ms2": ACCEL_RMS,
            "mode_n": MODE_N,
            "seed": 42,
        },
        "parameters": {
            name: {
                "nominal": d["nominal"],
                "distribution": d["dist"],
                "range_low": d["low"],
                "range_high": d["high"],
            }
            for name, d in PARAM_DEFS.items()
        },
        "monte_carlo": all_stats,
        "sobol": sobol,
    }
    json_path = os.path.join(RES_DIR, "uq_results.json")
    with open(json_path, "w") as f:
        json.dump(json_out, f, indent=2)
    print(f"\n  Saved {json_path}")
    print()


if __name__ == "__main__":
    main()
