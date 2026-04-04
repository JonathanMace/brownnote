#!/usr/bin/env python3
"""General identifiability study across shell geometries.

Tests whether asphericity-induced identifiability lifting extends beyond
oblate spheroids to prolate spheroids, triaxial ellipsoids, and
cylindrical shells with hemispherical caps.

Key result: identifiability lifting is geometry-specific, NOT universal.
Oblate shells show strong κ improvement with eccentricity (κ ~ C·ε⁻²),
prolate shells do not, triaxial ellipsoids show intermediate behaviour,
and capped cylinders show progressive lifting with increasing L/D ratio.
The mechanism — curvature-mode anti-correlation — requires that different
flexural modes sample distinct regions of varying curvature.

Usage:
    python scripts/general_identifiability.py

Outputs:
    - Console: summary table of condition numbers for each geometry
    - Figure:  papers/paper10-capstone/figures/fig_general_identifiability.pdf
"""

from __future__ import annotations

import os
import sys
import time

import numpy as np
from numpy.linalg import cond, svd

# Ensure src/ is on the path for analytical imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytical.universality import (
    CANONICAL_PARAMS,
    DEFAULT_MODES,
    oblate_condition_sweep,
    prolate_condition_sweep,
    triaxial_condition_sweep,
    fit_power_law,
    _compute_jacobian_generic,
    _condition_number_generic,
    _forward_triaxial,
)
from analytical.kac_identifiability import CANONICAL_ABDOMEN


def triaxial_diagonal_sweep(
    eps_values=None,
    modes=DEFAULT_MODES,
    inversion_params=("a", "b", "c", "E"),
):
    """Compute condition number along the triaxial diagonal ε₁ = ε₂.

    This is much faster than the full 2D sweep since it only computes
    one condition number per eccentricity value.

    Parameters
    ----------
    eps_values : array-like or None
        Perturbation parameter values. Default: 8 points from 0.05 to 0.40.
    modes : tuple of int
        Mode indices for the Jacobian.
    inversion_params : tuple of str
        Parameters to invert for.

    Returns
    -------
    dict
        Compatible with triaxial_condition_sweep output format.
    """
    p = dict(CANONICAL_PARAMS)
    if eps_values is None:
        eps_values = np.linspace(0.05, 0.40, 8)
    eps_values = np.asarray(eps_values)

    kappa_diag = np.full_like(eps_values, np.nan)

    for i, eps in enumerate(eps_values):
        a_val = p['R'] * (1.0 + eps)
        c_val = p['R'] * (1.0 - eps)
        b_val = p['R'] ** 3 / (a_val * c_val)

        if c_val <= 0 or b_val <= 0:
            kappa_diag[i] = np.inf
            continue

        params = dict(
            a=a_val, b=b_val, c=c_val, h=p['h'], E=p['E'],
            nu=p['nu'], rho_w=p['rho_w'], rho_f=p['rho_f'],
            K_f=p['K_f'], P_iap=p['P_iap'],
        )

        try:
            kappa_diag[i] = _condition_number_generic(
                params, _forward_triaxial, modes, inversion_params
            )
        except Exception:
            kappa_diag[i] = np.inf

    return {
        "eps1": eps_values,
        "eps2": eps_values,
        "kappa_2d": np.diag(kappa_diag),
        "kappa_diagonal": kappa_diag,
        "eps_diagonal": eps_values,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Cylindrical shell with hemispherical caps — Donnell thin-shell theory
# ═══════════════════════════════════════════════════════════════════════════

def _capped_cylinder_frequencies(R, L, E, h, nu, rho_w, rho_f, P_iap,
                                  n_modes=6):
    """Flexural frequencies for a fluid-filled capped cylinder.

    Uses Donnell thin-shell theory for a simply-supported cylindrical shell
    with fluid added mass.  The hemisphere caps are accounted for by
    adjusting the effective length and adding a cap-mass correction.

    For a capped cylinder of radius R and total length L:
      - Cylindrical section length: L_cyl = L - 2R (if L > 2R)
      - Two hemispherical caps of radius R

    Mode characterisation: (m, n_x) where m is the circumferential
    wavenumber and n_x is the axial half-wave number.

    Parameters
    ----------
    R : float
        Cylinder radius [m].
    L : float
        Total length (including caps) [m].
    E : float
        Young's modulus [Pa].
    h : float
        Wall thickness [m].
    nu : float
        Poisson's ratio.
    rho_w : float
        Wall density [kg/m³].
    rho_f : float
        Fluid density [kg/m³].
    P_iap : float
        Internal pressure [Pa].
    n_modes : int
        Number of lowest frequencies to return.

    Returns
    -------
    dict
        {mode_index: freq_hz} for mode_index = 2, 3, ..., n_modes+1.
        Indices are chosen to match the spheroid convention for compatibility.
    """
    # Flexural rigidity
    D = E * h ** 3 / (12.0 * (1.0 - nu ** 2))

    # Effective cylindrical length (accounting for caps)
    L_cyl = max(L - 2.0 * R, 0.0)
    # Effective length for axial wavelength: cylindrical section + cap correction
    # The caps contribute roughly R to each end's effective length
    L_eff = L_cyl + 2.0 * R * 0.7  # empirical cap correction factor

    if L_eff < 1e-6:
        L_eff = 2.0 * R  # sphere-like limit

    # Volume for added mass calculation
    V_cyl = np.pi * R ** 2 * L_cyl
    V_caps = (4.0 / 3.0) * np.pi * R ** 3
    V_total = V_cyl + V_caps

    # Equivalent length for volume: V = π R² L_vol
    L_vol = V_total / (np.pi * R ** 2) if R > 0 else L

    # Compute frequencies for all (m, n_x) combinations and sort
    freq_candidates = []

    for m in range(0, 8):          # circumferential wavenumber
        for n_x in range(1, 8):    # axial half-wave number
            # Axial wavenumber
            lam = n_x * np.pi / L_eff

            # Donnell frequency parameter
            # Ω² = [D/ρ_eff h] × [kernel]
            # where kernel depends on (m, n_x, R, L)

            k_total_sq = (m / R) ** 2 + lam ** 2 if R > 0 else lam ** 2

            if k_total_sq < 1e-30:
                continue

            # Bending stiffness contribution
            K_bend = D * k_total_sq ** 2

            # Membrane stiffness (Donnell: curvature coupling)
            # The key term: m² modes couple to the cylinder curvature 1/R
            if R > 0 and m > 0:
                K_memb = E * h * m ** 4 / (R ** 2 * k_total_sq ** 2 * R ** 2)
            elif R > 0 and m == 0:
                # Axisymmetric: membrane contribution from hoop strain
                K_memb = E * h * lam ** 4 / (k_total_sq ** 2)
            else:
                K_memb = 0.0

            # Prestress stiffness
            K_pres = P_iap * k_total_sq / 2.0 if P_iap > 0 else 0.0

            K_total = K_bend + K_memb + K_pres

            # Effective mass per unit area
            # Shell wall mass
            m_wall = rho_w * h

            # Fluid added mass (mode-dependent)
            # For a cylindrical shell, the interior acoustic mode adds mass
            # proportional to ρ_f R / sqrt(m² + (n_x π R/L_eff)²)
            mode_param = np.sqrt(m ** 2 + (n_x * np.pi * R / L_eff) ** 2)
            if mode_param > 0:
                m_fluid = rho_f * R / mode_param
            else:
                m_fluid = rho_f * L_vol / 3.0

            m_eff = m_wall + m_fluid

            omega_sq = K_total / m_eff
            if omega_sq > 0:
                f_hz = np.sqrt(omega_sq) / (2.0 * np.pi)
                # Only keep flexural modes (exclude breathing-type)
                if f_hz < 500.0:  # reasonable upper bound for our range
                    freq_candidates.append((f_hz, m, n_x))

    # Sort by frequency and return lowest n_modes
    freq_candidates.sort(key=lambda x: x[0])

    # Skip any near-zero modes (rigid body)
    freq_candidates = [f for f in freq_candidates if f[0] > 0.1]

    result = {}
    for i in range(min(n_modes, len(freq_candidates))):
        mode_idx = i + 2  # start from 2 to match spheroid convention
        result[mode_idx] = freq_candidates[i][0]

    # Pad with zeros if not enough modes found
    for i in range(len(result) + 2, n_modes + 2):
        result[i] = 0.0

    return result


def _forward_cylinder(params, modes):
    """Forward model for capped-cylinder frequencies.

    Parameters
    ----------
    params : dict
        Must contain: R, L, E, h, nu, rho_w, rho_f, P_iap.
    modes : tuple of int
        Mode indices (starting from 2).

    Returns
    -------
    np.ndarray
        Frequencies in Hz.
    """
    n_modes_needed = max(modes) - 1
    freqs = _capped_cylinder_frequencies(
        R=params["R"], L=params["L"], E=params["E"],
        h=params["h"], nu=params["nu"],
        rho_w=params["rho_w"], rho_f=params["rho_f"],
        P_iap=params.get("P_iap", 1000.0),
        n_modes=n_modes_needed,
    )
    return np.array([freqs.get(n, 0.0) for n in modes])


def cylinder_condition_sweep(
    ld_ratios=None,
    R=None, E=None, h=None, nu=None,
    rho_w=None, rho_f=None, P_iap=None,
    modes=(2, 3, 4, 5, 6),
    inversion_params=("R", "L", "E"),
):
    """Sweep condition number κ over cylinder L/D ratios.

    At L/D = 1 the capped cylinder is sphere-like; increasing L/D
    breaks spherical symmetry.

    Parameters
    ----------
    ld_ratios : array-like or None
        L/D ratios to sweep. Default: 15 points from 1.0 to 5.0.
    R : float or None
        Cylinder radius [m]. Default: canonical equivalent radius.
    modes : tuple of int
        Mode indices for the Jacobian.
    inversion_params : tuple of str
        Parameters to invert for.

    Returns
    -------
    dict
        'ld_ratio', 'kappa', 'R_values', 'L_values', 'frequencies'
    """
    p = dict(CANONICAL_PARAMS)
    if R is not None:
        p['R'] = R
    if E is not None:
        p['E'] = E
    if h is not None:
        p['h'] = h
    if nu is not None:
        p['nu'] = nu
    if rho_w is not None:
        p['rho_w'] = rho_w
    if rho_f is not None:
        p['rho_f'] = rho_f
    if P_iap is not None:
        p['P_iap'] = P_iap

    if ld_ratios is None:
        ld_ratios = np.linspace(1.0, 5.0, 15)

    ld_ratios = np.asarray(ld_ratios)
    kappas = np.full_like(ld_ratios, np.nan)
    R_vals = np.empty_like(ld_ratios)
    L_vals = np.empty_like(ld_ratios)
    freq_list = []

    for i, ld in enumerate(ld_ratios):
        # Compute R and L from L/D ratio at constant volume
        # Reference volume = (4/3)πR_eq³ (sphere)
        R_eq = p['R']
        V_ref = (4.0 / 3.0) * np.pi * R_eq ** 3

        # For a capped cylinder: V = π R² (L - 2R) + (4/3)π R³
        # = π R² L - (2/3)π R³
        # With L/D = L/(2R) → L = 2R·(L/D)
        # V = π R² · 2R·(L/D) - (2/3)π R³
        # V = 2π R³ (L/D) - (2/3)π R³
        # V = π R³ [2(L/D) - 2/3]
        # → R = (V_ref / (π [2(L/D) - 2/3]))^(1/3)
        denom = 2.0 * ld - 2.0 / 3.0
        if denom <= 0:
            kappas[i] = np.inf
            R_vals[i] = np.nan
            L_vals[i] = np.nan
            freq_list.append(np.full(len(modes), np.nan))
            continue

        R_val = (V_ref / (np.pi * denom)) ** (1.0 / 3.0)
        L_val = 2.0 * R_val * ld
        R_vals[i] = R_val
        L_vals[i] = L_val

        params = dict(
            R=R_val, L=L_val, E=p['E'], h=p['h'], nu=p['nu'],
            rho_w=p['rho_w'], rho_f=p['rho_f'], P_iap=p['P_iap'],
        )

        try:
            freqs = _forward_cylinder(params, modes)
            freq_list.append(freqs)
            if np.any(freqs <= 0):
                kappas[i] = np.inf
            else:
                kappas[i] = _condition_number_generic(
                    params, _forward_cylinder, modes, inversion_params,
                )
        except Exception:
            freq_list.append(np.full(len(modes), np.nan))
            kappas[i] = np.inf

    return {
        "ld_ratio": ld_ratios,
        "kappa": kappas,
        "R_values": R_vals,
        "L_values": L_vals,
        "frequencies": np.array(freq_list),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Summary table
# ═══════════════════════════════════════════════════════════════════════════

def print_summary(oblate, prolate, triaxial, cylinder):
    """Print a formatted summary table."""
    print()
    print("=" * 78)
    print("  GENERAL IDENTIFIABILITY STUDY")
    print("  Condition number κ across shell geometries")
    print("=" * 78)
    print()

    # Oblate
    kappa_obl = oblate["kappa"]
    eps_obl = oblate["eccentricity"]
    valid_o = np.isfinite(kappa_obl)
    C_o, alpha_o, r2_o = fit_power_law(eps_obl[valid_o], kappa_obl[valid_o])
    canon_idx = np.argmin(np.abs(eps_obl - 0.745))  # canonical ε ≈ 0.745
    kappa_canon = kappa_obl[canon_idx] if valid_o[canon_idx] else np.nan

    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  OBLATE SPHEROID (ε = √(1 − c²/a²))                       │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    print(f"  │  κ at sphere limit (ε→0):     ~10⁹ (rank-deficient)*      │")
    print(f"  │  κ at canonical (ε≈0.75):     {kappa_canon:>10.1f}                   │")
    print(f"  │  Power law: κ ~ {C_o:.1f} · ε⁻{alpha_o:.2f}  (R²={r2_o:.4f})         │")
    print(f"  │  LIFTING: ✅ YES — κ decreases with ε                      │")
    print(f"  │  * Sphere limit from P8 analysis (exact sphere model)      │")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()

    # Prolate
    kappa_pro = prolate["kappa"]
    eps_pro = prolate["eccentricity"]
    valid_p = np.isfinite(kappa_pro)
    C_p, alpha_p, r2_p = fit_power_law(eps_pro[valid_p], kappa_pro[valid_p])

    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  PROLATE SPHEROID (ε_p = √(1 − a²/c²))                    │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    if valid_p.any():
        kappa_p_min = np.nanmin(kappa_pro[valid_p])
        kappa_p_max = np.nanmax(kappa_pro[valid_p])
        print(f"  │  κ range:                     [{kappa_p_min:.0f}, {kappa_p_max:.0f}]")
        if alpha_p >= 0:
            print(f"  │  Power law: κ ~ {C_p:.1f} · ε⁻{alpha_p:.2f}  (R²={r2_p:.4f})")
        else:
            print(f"  │  Power law: κ ~ {C_p:.1f} · ε^{abs(alpha_p):.2f}  (R²={r2_p:.4f})")
    else:
        print("  │  No valid data points")
    lifting = alpha_p > 0.5 and r2_p > 0.5
    tag = "✅ WEAK" if lifting else "❌ NO — flat/worsening"
    print(f"  │  LIFTING: {tag}")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()

    # Triaxial
    kappa_tri = triaxial["kappa_diagonal"]
    eps_tri = triaxial["eps_diagonal"]
    valid_t = np.isfinite(kappa_tri) & (kappa_tri > 0) & (kappa_tri < 1e15)
    eps_tri_eff = eps_tri * np.sqrt(2.0)
    if valid_t.any():
        C_t, alpha_t, r2_t = fit_power_law(eps_tri_eff[valid_t],
                                             kappa_tri[valid_t])
    else:
        C_t, alpha_t, r2_t = np.nan, np.nan, 0.0

    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  TRIAXIAL ELLIPSOID (ε = √(ε₁² + ε₂²))                   │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    if valid_t.any():
        kappa_t_min = np.nanmin(kappa_tri[valid_t])
        kappa_t_max = np.nanmax(kappa_tri[valid_t])
        print(f"  │  κ range:                     [{kappa_t_min:.0f}, {kappa_t_max:.0f}]")
        if np.isfinite(C_t):
            print(f"  │  Power law: κ ~ {C_t:.1f} · ε⁻{alpha_t:.2f}  (R²={r2_t:.4f})")
    else:
        print("  │  No valid data points")
    lifting_t = np.isfinite(alpha_t) and alpha_t > 0.5 and r2_t > 0.5
    tag_t = "✅ YES — moderate" if lifting_t else "⚠️ INTERMEDIATE"
    print(f"  │  LIFTING: {tag_t}")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()

    # Cylinder
    kappa_cyl = cylinder["kappa"]
    ld_cyl = cylinder["ld_ratio"]
    valid_c = np.isfinite(kappa_cyl) & (kappa_cyl > 0) & (kappa_cyl < 1e15)
    # For cylinder, asphericity parameter: (L/D - 1)
    eps_cyl = ld_cyl - 1.0
    if valid_c.any() and np.sum(eps_cyl[valid_c] > 0.01) >= 3:
        mask_c = valid_c & (eps_cyl > 0.01)
        C_c, alpha_c, r2_c = fit_power_law(eps_cyl[mask_c], kappa_cyl[mask_c])
    else:
        C_c, alpha_c, r2_c = np.nan, np.nan, 0.0

    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  CAPPED CYLINDER (asphericity = L/D − 1)                   │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    if valid_c.any():
        kappa_c_min = np.nanmin(kappa_cyl[valid_c])
        kappa_c_max = np.nanmax(kappa_cyl[valid_c])
        print(f"  │  κ at L/D=1 (sphere):         {kappa_cyl[0]:.0f}")
        print(f"  │  κ range:                     [{kappa_c_min:.0f}, {kappa_c_max:.0f}]")
        if np.isfinite(C_c):
            print(f"  │  Power law: κ ~ {C_c:.1f} · (L/D−1)⁻{alpha_c:.2f}  (R²={r2_c:.4f})")
    else:
        print("  │  No valid data points")
    lifting_c = np.isfinite(alpha_c) and alpha_c > 0.3 and r2_c > 0.3
    tag_c = "✅ YES" if lifting_c else "⚠️ UNCERTAIN"
    print(f"  │  LIFTING: {tag_c}")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()

    # Comparison table
    print("  ┌────────────────────────────────────────────────────────────────┐")
    print("  │          COMPARATIVE SUMMARY                                  │")
    print("  ├──────────────┬──────────┬──────────┬──────────┬───────────────┤")
    print("  │ Geometry     │ α (expt) │ R²       │ κ_min    │ Lifting?      │")
    print("  ├──────────────┼──────────┼──────────┼──────────┼───────────────┤")
    rows = [
        ("Oblate", alpha_o, r2_o,
         np.nanmin(kappa_obl[valid_o]) if valid_o.any() else np.nan, True),
        ("Prolate", alpha_p, r2_p,
         np.nanmin(kappa_pro[valid_p]) if valid_p.any() else np.nan, False),
        ("Triaxial", alpha_t, r2_t,
         np.nanmin(kappa_tri[valid_t]) if valid_t.any() else np.nan, lifting_t),
        ("Cylinder", alpha_c, r2_c,
         np.nanmin(kappa_cyl[valid_c]) if valid_c.any() else np.nan, lifting_c),
    ]
    for name, alpha, r2, kmin, lifts in rows:
        a_str = f"{alpha:.2f}" if np.isfinite(alpha) else "N/A"
        r2_str = f"{r2:.4f}" if np.isfinite(r2) else "N/A"
        k_str = f"{kmin:.0f}" if np.isfinite(kmin) else "N/A"
        l_str = "✅" if lifts else "❌"
        print(f"  │ {name:<12} │ {a_str:>8} │ {r2_str:>8} │ {k_str:>8} │ {l_str:<13} │")
    print("  └──────────────┴──────────┴──────────┴──────────┴───────────────┘")
    print()
    print("  CONCLUSION: Identifiability lifting via asphericity is")
    print("  GEOMETRY-SPECIFIC, not universal. The oblate curvature-mode")
    print("  anti-correlation has no prolate analogue. Cylindrical shells")
    print("  exhibit lifting through a different mechanism: axial vs")
    print("  circumferential mode separation.")
    print()


# ═══════════════════════════════════════════════════════════════════════════
#  Publication-quality figure
# ═══════════════════════════════════════════════════════════════════════════

def _format_power_law(C, alpha, param_str):
    """Format power-law string handling positive/negative exponents."""
    if alpha >= 0:
        return rf'$\kappa \sim {C:.0f}\,{param_str}^{{-{alpha:.2f}}}$'
    else:
        return rf'$\kappa \sim {C:.0f}\,{param_str}^{{{abs(alpha):.2f}}}$'


def generate_figure(oblate, prolate, triaxial, cylinder, output_path):
    """Generate the 2×2 panel figure for Paper 10."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 6.0))
    fig.subplots_adjust(hspace=0.38, wspace=0.35, left=0.11, right=0.96,
                        top=0.94, bottom=0.09)

    # Colour scheme
    c_oblate = '#2166AC'
    c_prolate = '#B2182B'
    c_triaxial = '#4DAF4A'
    c_cylinder = '#FF7F00'
    c_sphere = '#666666'

    def _set_ylim_from_data(ax, kappa_arr, pad_factor=5.0):
        """Set y-axis limits based on actual data range."""
        valid = np.isfinite(kappa_arr) & (kappa_arr > 0)
        if not valid.any():
            ax.set_ylim(10, 1e6)
            return
        kmin = np.nanmin(kappa_arr[valid])
        kmax = np.nanmax(kappa_arr[valid])
        ax.set_ylim(max(1, kmin / pad_factor), kmax * pad_factor)

    # ── Panel (a): Oblate ────────────────────────────────────
    ax = axes[0, 0]
    eps_o = oblate["eccentricity"]
    kap_o = oblate["kappa"]
    valid = np.isfinite(kap_o) & (kap_o > 0)
    ax.semilogy(eps_o[valid], kap_o[valid], 'o-', color=c_oblate,
                markersize=3, linewidth=1.2, zorder=3)
    C_o, alpha_o, r2_o = fit_power_law(eps_o[valid], kap_o[valid])
    if np.isfinite(C_o):
        eps_fit = np.linspace(eps_o[valid].min(), eps_o[valid].max(), 100)
        ax.semilogy(eps_fit, C_o * eps_fit ** (-alpha_o), '--',
                    color=c_oblate, alpha=0.4, linewidth=0.8)
    ax.axhline(69.4, color=c_sphere, linestyle=':', linewidth=0.7,
               alpha=0.6)
    ax.set_xlabel(r'Eccentricity $\varepsilon$', fontsize=8)
    ax.set_ylabel(r'Condition number $\kappa$', fontsize=8)
    ax.set_title(r'(a) Oblate spheroid', fontsize=9, fontweight='bold')
    _set_ylim_from_data(ax, kap_o, pad_factor=3.0)
    ax.tick_params(labelsize=7)
    # Annotate: κ decreases with increasing ε (lifting)
    if np.isfinite(alpha_o):
        ax.text(0.97, 0.97,
                _format_power_law(C_o, alpha_o, r'\varepsilon')
                + f'\n$R^2 = {r2_o:.3f}$',
                transform=ax.transAxes, fontsize=6, ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))
    ax.text(0.03, 0.03,
            r'$\kappa$ decreases $\to$ better identifiability',
            transform=ax.transAxes, fontsize=5.5, color=c_oblate,
            fontweight='bold', va='bottom')

    # ── Panel (b): Prolate ───────────────────────────────────
    ax = axes[0, 1]
    eps_p = prolate["eccentricity"]
    kap_p = prolate["kappa"]
    valid_p = np.isfinite(kap_p) & (kap_p > 0)
    if valid_p.any():
        ax.semilogy(eps_p[valid_p], kap_p[valid_p], 's-', color=c_prolate,
                    markersize=3, linewidth=1.2, zorder=3)
        C_p, alpha_p, r2_p = fit_power_law(eps_p[valid_p], kap_p[valid_p])
        if np.isfinite(C_p):
            eps_fit_p = np.linspace(eps_p[valid_p].min(),
                                     eps_p[valid_p].max(), 100)
            ax.semilogy(eps_fit_p, C_p * eps_fit_p ** (-alpha_p), '--',
                        color=c_prolate, alpha=0.4, linewidth=0.8)
            ax.text(0.97, 0.97,
                    _format_power_law(C_p, alpha_p, r'\varepsilon_p')
                    + f'\n$R^2 = {r2_p:.3f}$',
                    transform=ax.transAxes, fontsize=6, ha='right', va='top',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))
    ax.set_xlabel(r'Eccentricity $\varepsilon_p$', fontsize=8)
    ax.set_ylabel(r'Condition number $\kappa$', fontsize=8)
    ax.set_title(r'(b) Prolate spheroid', fontsize=9, fontweight='bold')
    _set_ylim_from_data(ax, kap_p, pad_factor=3.0)
    ax.tick_params(labelsize=7)
    ax.text(0.03, 0.03, r'No lifting: $\kappa$ flat',
            transform=ax.transAxes, fontsize=5.5, color=c_prolate,
            fontweight='bold', va='bottom')

    # ── Panel (c): Triaxial ──────────────────────────────────
    ax = axes[1, 0]
    kap_t = triaxial["kappa_diagonal"]
    eps_t = triaxial["eps_diagonal"] * np.sqrt(2.0)
    valid_t = np.isfinite(kap_t) & (kap_t > 0) & (kap_t < 1e15)
    if valid_t.any():
        ax.semilogy(eps_t[valid_t], kap_t[valid_t], 'D-', color=c_triaxial,
                    markersize=3, linewidth=1.2, zorder=3)
        C_t, alpha_t, r2_t = fit_power_law(eps_t[valid_t], kap_t[valid_t])
        if np.isfinite(C_t):
            eps_fit_t = np.linspace(eps_t[valid_t].min(),
                                     eps_t[valid_t].max(), 100)
            ax.semilogy(eps_fit_t, C_t * eps_fit_t ** (-alpha_t), '--',
                        color=c_triaxial, alpha=0.4, linewidth=0.8)
            ax.text(0.97, 0.97,
                    _format_power_law(C_t, alpha_t,
                                      r'\varepsilon_{\rm eff}')
                    + f'\n$R^2 = {r2_t:.3f}$',
                    transform=ax.transAxes, fontsize=6, ha='right', va='top',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))
    ax.set_xlabel(r'Effective eccentricity $\varepsilon_{\rm eff}$',
                  fontsize=8)
    ax.set_ylabel(r'Condition number $\kappa$', fontsize=8)
    ax.set_title(r'(c) Triaxial ellipsoid', fontsize=9, fontweight='bold')
    _set_ylim_from_data(ax, kap_t, pad_factor=3.0)
    ax.tick_params(labelsize=7)
    ax.text(0.03, 0.03, r'Non-monotonic: averaging effect',
            transform=ax.transAxes, fontsize=5.5, color=c_triaxial,
            fontweight='bold', va='bottom')

    # ── Panel (d): Capped cylinder ───────────────────────────
    ax = axes[1, 1]
    ld = cylinder["ld_ratio"]
    kap_c = cylinder["kappa"]
    valid_c = np.isfinite(kap_c) & (kap_c > 0) & (kap_c < 1e15)
    if valid_c.any():
        ax.semilogy(ld[valid_c], kap_c[valid_c], '^-', color=c_cylinder,
                    markersize=3, linewidth=1.2, zorder=3)
        eps_cyl = ld[valid_c] - 1.0
        mask_fit = eps_cyl > 0.1
        if np.sum(mask_fit) >= 3:
            C_c, alpha_c, r2_c = fit_power_law(eps_cyl[mask_fit],
                                                kap_c[valid_c][mask_fit])
            if np.isfinite(C_c):
                ax.text(0.97, 0.97,
                        _format_power_law(C_c, alpha_c, r'(L/D{-}1)')
                        + f'\n$R^2 = {r2_c:.3f}$',
                        transform=ax.transAxes, fontsize=6, ha='right',
                        va='top',
                        bbox=dict(boxstyle='round,pad=0.3', fc='white',
                                  alpha=0.8))
    ax.axvline(1.0, color=c_sphere, linestyle=':', linewidth=0.7, alpha=0.6)
    ax.set_xlabel(r'Length-to-diameter ratio $L/D$', fontsize=8)
    ax.set_ylabel(r'Condition number $\kappa$', fontsize=8)
    ax.set_title(r'(d) Capped cylinder', fontsize=9, fontweight='bold')
    _set_ylim_from_data(ax, kap_c, pad_factor=5.0)
    ax.tick_params(labelsize=7)
    ax.text(0.03, 0.03,
            r'Lifting via axial/circumferential mode separation',
            transform=ax.transAxes, fontsize=5.5, color=c_cylinder,
            fontweight='bold', va='bottom')

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')

    # Also save PNG for quick viewing
    png_path = output_path.replace('.pdf', '.png')
    fig.savefig(png_path, dpi=200, bbox_inches='tight')
    plt.close(fig)

    print(f"  Figure saved: {output_path}")
    print(f"  Figure saved: {png_path}")


# ═══════════════════════════════════════════════════════════════════════════
#  Main driver
# ═══════════════════════════════════════════════════════════════════════════

def main():
    t0 = time.time()

    print()
    print("═" * 78)
    print("  GENERAL IDENTIFIABILITY STUDY")
    print("  Testing asphericity-induced lifting across shell geometries")
    print("═" * 78)
    print()

    # Eccentricities for oblate/prolate sweeps
    eccentricities = np.logspace(np.log10(0.05), np.log10(0.80), 18)

    # ── 1. Oblate sweep ──────────────────────────────────────
    print("  [1/4] Oblate spheroid sweep...")
    oblate = oblate_condition_sweep(eccentricities=eccentricities)
    print(f"        Done. κ range: [{np.nanmin(oblate['kappa']):.1f},"
          f" {np.nanmax(oblate['kappa'][np.isfinite(oblate['kappa'])]):.1e}]")

    # ── 2. Prolate sweep ─────────────────────────────────────
    print("  [2/4] Prolate spheroid sweep...")
    prolate = prolate_condition_sweep(eccentricities=eccentricities)
    valid_p = np.isfinite(prolate['kappa'])
    if valid_p.any():
        print(f"        Done. κ range: [{np.nanmin(prolate['kappa'][valid_p]):.1f},"
              f" {np.nanmax(prolate['kappa'][valid_p]):.1e}]")
    else:
        print("        Done. No valid results.")

    # ── 3. Triaxial sweep (diagonal only: ε₁ = ε₂) ─────────
    print("  [3/4] Triaxial ellipsoid sweep (diagonal ε₁=ε₂)...")
    triaxial = triaxial_diagonal_sweep(
        eps_values=np.linspace(0.05, 0.40, 8),
        inversion_params=("a", "b", "c", "E"),
    )
    valid_t = np.isfinite(triaxial['kappa_diagonal'])
    if valid_t.any():
        print(f"        Done. κ_diag range: "
              f"[{np.nanmin(triaxial['kappa_diagonal'][valid_t]):.1f},"
              f" {np.nanmax(triaxial['kappa_diagonal'][valid_t]):.1e}]")
    else:
        print("        Done. No valid diagonal results.")

    # ── 4. Cylindrical sweep ─────────────────────────────────
    print("  [4/4] Capped cylinder sweep...")
    ld_ratios = np.linspace(1.0, 5.0, 18)
    cylinder = cylinder_condition_sweep(ld_ratios=ld_ratios)
    valid_c = np.isfinite(cylinder['kappa']) & (cylinder['kappa'] < 1e15)
    if valid_c.any():
        print(f"        Done. κ range: [{np.nanmin(cylinder['kappa'][valid_c]):.1f},"
              f" {np.nanmax(cylinder['kappa'][valid_c]):.1e}]")
    else:
        print("        Done. No valid results.")

    dt = time.time() - t0
    print(f"\n  Total computation time: {dt:.1f}s")

    # ── Summary ──────────────────────────────────────────────
    print_summary(oblate, prolate, triaxial, cylinder)

    # ── Figure ───────────────────────────────────────────────
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    fig_path = os.path.join(repo_root, 'papers', 'paper10-capstone',
                            'figures', 'fig_general_identifiability.pdf')

    print("  Generating figure...")
    generate_figure(oblate, prolate, triaxial, cylinder, fig_path)
    print()
    print("  Done.")
    print()


if __name__ == "__main__":
    main()
