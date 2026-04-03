#!/usr/bin/env python
"""Ritz convergence study for the n=2 flexural mode of an oblate spheroidal shell.

Enriches the 2-DOF-per-mode Rayleigh-Ritz basis from Paper 1 with
higher-order Legendre polynomials and demonstrates that the fundamental
flexural frequency converges rapidly — providing formal convergence
evidence requested by reviewers.

Basis enrichment (same-parity Legendre ladder)::

    w(eta) = sum_i  beta_i  P_{n+2i}(eta)               i = 0 .. N-1
    u(theta)= sum_j  alpha_j sin(theta) P'_{n+2j}(cos theta)  j = 0 .. N-1

giving a 2N-DOF generalised eigenvalue problem  K q = omega^2 M q.

Shell strain energy is integrated over the *oblate spheroid* (not the
equivalent sphere), so different Legendre orders couple through the
position-dependent curvature.  Fluid added mass uses the equivalent-
sphere approximation (diagonal in the Legendre basis).

Usage::

    python scripts/ritz_convergence.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from scipy.special import legendre as _legendre_poly
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eigh
import sys
import os

# ---------------------------------------------------------------------------
# Path setup — allow imports from repo root
# ---------------------------------------------------------------------------
_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, _REPO)

from src.analytical.oblate_spheroid_ritz import oblate_ritz_frequency, _fluid_mass
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)

# ---------------------------------------------------------------------------
# Canonical parameters (R3)
# ---------------------------------------------------------------------------
A_SEMI = 0.18       # semi-major axis [m]
C_SEMI = 0.12       # semi-minor axis [m]
H_WALL = 0.010      # wall thickness  [m]
E_MOD  = 0.1e6      # Young's modulus [Pa]  (0.1 MPa)
NU     = 0.45        # Poisson's ratio
RHO_W  = 1100.0      # wall density    [kg/m^3]
RHO_F  = 1020.0      # fluid density   [kg/m^3]
P_IAP  = 1000.0      # intra-abdominal pressure [Pa]
N_QUAD = 300         # Gauss-Legendre quadrature points
TARGET_MODE = 2      # n = 2 flexural mode


# ===================================================================
# Core Ritz engine with enriched basis
# ===================================================================

def _evaluate_legendre(m, eta):
    """Return (P_m, P_m', P_m'') evaluated at *eta* = cos theta."""
    poly = _legendre_poly(m)
    Pm = poly(eta)
    dPm = poly.deriv(1)(eta) if m >= 1 else np.zeros_like(eta)
    d2Pm = poly.deriv(2)(eta) if m >= 2 else np.zeros_like(eta)
    return Pm, dPm, d2Pm


def build_enriched_KM(n, N_basis, a, c, h, E, nu, P_iap,
                      rho_w, rho_f, eta_q, w_q):
    """
    Build 2N x 2N stiffness **K** and mass **M** for enriched Ritz basis.

    Parameters
    ----------
    n : int
        Target mode number (>= 2).
    N_basis : int
        Number of Legendre terms per displacement component.
    a, c : float
        Oblate spheroid semi-axes.
    h, E, nu, P_iap, rho_w, rho_f : float
        Material / loading parameters.
    eta_q, w_q : ndarray
        Gauss-Legendre nodes and weights on [-1, 1].

    Returns
    -------
    K, M : ndarray (2N, 2N)
        Stiffness and mass matrices.
    """
    Nd = 2 * N_basis
    K = np.zeros((Nd, Nd))
    M = np.zeros((Nd, Nd))

    # ── oblate spheroid geometry ──────────────────────────────
    eta2 = eta_q ** 2
    sin2 = 1.0 - eta2
    G    = a**2 * eta2 + c**2 * sin2           # metric G(eta)
    sqG  = np.sqrt(G)
    Delta = a**2 - c**2
    Gp   = 2.0 * Delta * eta_q                  # dG/d(eta)

    # Membrane pre-stress resultant  N_1 = P * R_2 / 2
    R2   = a * sqG / c
    N1_pre = P_iap * R2 / 2.0

    # Material constants
    Cm = E * h / (1.0 - nu**2)
    Df = E * h**3 / (12.0 * (1.0 - nu**2))

    # ── pre-compute Legendre values ──────────────────────────
    degrees = [n + 2 * i for i in range(N_basis)]
    leg_data = [_evaluate_legendre(m, eta_q) for m in degrees]
    # leg_data[idx] = (Pm, dPm, d2Pm)

    Nq = len(eta_q)

    # ── strain / curvature / mass shape arrays ───────────────
    e1     = np.zeros((Nd, Nq))     # membrane meridional
    e2     = np.zeros((Nd, Nq))     # membrane circumferential
    kk1    = np.zeros((Nd, Nq))     # curvature change kappa_1
    kk2    = np.zeros((Nd, Nq))     # curvature change kappa_2
    sl     = np.zeros((N_basis, Nq))  # prestress rotation (w-DOFs only)
    w_sh   = np.zeros((Nd, Nq))     # radial displacement shape
    u_sh   = np.zeros((Nd, Nq))     # tangential displacement shape

    for idx in range(N_basis):
        m = degrees[idx]
        mm = m * (m + 1)
        Pm, dPm, d2Pm = leg_data[idx]

        # --- radial DOF (index = idx) ---
        dw = idx

        # membrane strains  (stored as eps * sqrt(G))
        e1[dw] = a * c * Pm / G
        e2[dw] = c * Pm / a

        # bending curvatures (following oblate_spheroid_ritz._build_KM)
        hw   = dPm / sqG
        hwp  = d2Pm / sqG - dPm * Delta * eta_q / G**1.5
        kk1[dw] = (eta_q * hw - sin2 * hwp) / sqG
        kk2[dw] = eta_q * dPm / G

        # prestress rotation  sqrt(sin^2 theta / G) * P'_m
        sl[idx] = np.sqrt(np.maximum(sin2, 0.0) / G) * dPm

        # mass shape (radial)
        w_sh[dw] = Pm

        # --- tangential DOF (index = N_basis + idx) ---
        du = N_basis + idx

        # membrane strains  (stored as eps * sqrt(G))
        e1[du] = -eta_q * dPm + mm * Pm
        e2[du] = eta_q * dPm

        # bending curvatures
        hu   = dPm * a * c / G**1.5
        hup  = (d2Pm * a * c / G**1.5
                - dPm * a * c * 1.5 * Gp / G**2.5)
        kk1[du] = (eta_q * hu - sin2 * hup) / sqG
        kk2[du] = eta_q * dPm * a * c / G**2

        # mass shape (tangential: sin theta * P'_m)
        u_sh[du] = np.sqrt(np.maximum(sin2, 0.0)) * dPm

    # ── assemble K and M by Gauss-Legendre quadrature ────────
    for k in range(Nq):
        sg  = sqG[k]
        wt  = w_q[k]

        e1k  = e1[:, k]
        e2k  = e2[:, k]
        kk1k = kk1[:, k]
        kk2k = kk2[:, k]

        # membrane stiffness   (factor = 2 pi a Cm / sqrt(G)  * wt)
        fac_m = 2.0 * np.pi * a * Cm * wt / sg
        K += fac_m * (np.outer(e1k, e1k) + np.outer(e2k, e2k)
                      + nu * (np.outer(e1k, e2k) + np.outer(e2k, e1k)))

        # bending stiffness    (factor = 2 pi a Df sqrt(G)  * wt)
        fac_b = 2.0 * np.pi * a * Df * sg * wt
        K += fac_b * (np.outer(kk1k, kk1k) + np.outer(kk2k, kk2k)
                      + nu * (np.outer(kk1k, kk2k) + np.outer(kk2k, kk1k)))

        # prestress geometric stiffness  (w-w block only)
        if P_iap > 0:
            N1k   = N1_pre[k]
            fac_p = 2.0 * np.pi * a * N1k * sg * wt
            slk   = sl[:, k]                        # length N_basis
            K[:N_basis, :N_basis] += fac_p * np.outer(slk, slk)

        # shell mass
        fac_ms = 2.0 * np.pi * a * rho_w * h * sg * wt
        wk = w_sh[:, k]
        uk = u_sh[:, k]
        M += fac_ms * (np.outer(wk, wk) + np.outer(uk, uk))

    # ── fluid added mass (oblate harmonics, diagonal in w-block) ─
    for idx in range(N_basis):
        m = degrees[idx]
        if m < 1:
            continue
        m_fluid = _fluid_mass(m, a, c, rho_f, eta_q, w_q)
        M[idx, idx] += m_fluid

    return K, M


def enriched_ritz_frequency(n, N_basis, a=A_SEMI, c=C_SEMI, h=H_WALL,
                            E=E_MOD, nu=NU, P_iap=P_IAP,
                            rho_w=RHO_W, rho_f=RHO_F, n_quad=N_QUAD):
    """Lowest flexural frequency (Hz) for mode *n* with *N_basis* terms."""
    if n < 2:
        return 0.0
    eta_q, w_q = leggauss(n_quad)
    K, M = build_enriched_KM(n, N_basis, a, c, h, E, nu, P_iap,
                             rho_w, rho_f, eta_q, w_q)
    try:
        eigvals = eigh(K, M, eigvals_only=True)
        omega_sq = max(eigvals[0], 0.0)
    except np.linalg.LinAlgError:
        eigvals = np.real(np.linalg.eigvals(np.linalg.solve(M, K)))
        omega_sq = max(eigvals.min(), 0.0)
    return np.sqrt(omega_sq) / (2.0 * np.pi)


# ===================================================================
# Main — convergence study and figure generation
# ===================================================================

def main():
    print()
    print("=" * 72)
    print("  RITZ CONVERGENCE STUDY")
    print("  n=2 flexural mode, oblate spheroidal shell (canonical R3)")
    print("=" * 72)
    print()
    print(f"  Geometry:   a = {A_SEMI} m,  c = {C_SEMI} m,  h = {H_WALL} m")
    print(f"  Material:   E = {E_MOD/1e6} MPa,  nu = {NU}")
    print(f"  Densities:  rho_w = {RHO_W} kg/m^3,  rho_f = {RHO_F} kg/m^3")
    print(f"  Pressure:   P_iap = {P_IAP} Pa")
    print(f"  Quadrature: {N_QUAD} Gauss-Legendre points")
    print()

    # ── 1. Validate N=1 against existing 2-DOF code ─────────
    f_existing = oblate_ritz_frequency(
        TARGET_MODE, A_SEMI, C_SEMI, H_WALL, E_MOD, NU,
        RHO_W, RHO_F, P_IAP, n_quad=N_QUAD,
    )
    f_enriched_1 = enriched_ritz_frequency(TARGET_MODE, 1)

    print("  1. VALIDATION (N=1 vs existing 2-DOF code)")
    print("  " + "-" * 55)
    print(f"     Existing oblate_ritz_frequency:  {f_existing:.6f} Hz")
    print(f"     Enriched Ritz (N=1):             {f_enriched_1:.6f} Hz")
    reldiff = abs(f_enriched_1 - f_existing) / f_existing * 100
    tag = "PASS" if reldiff < 0.1 else "MISMATCH"
    print(f"     Relative difference:             {reldiff:.4f}%  [{tag}]")
    print()

    # ── 2. Reference values ──────────────────────────────────
    model = AbdominalModelV2()
    f_sphere = flexural_mode_frequencies_v2(model, n_max=TARGET_MODE)[TARGET_MODE]
    print(f"  Reference: equivalent-sphere f_2 = {f_sphere:.4f} Hz")
    print()

    # ── 3. Convergence sweep N = 1 .. 8 ─────────────────────
    N_values = list(range(1, 9))
    freqs = []
    for N in N_values:
        f = enriched_ritz_frequency(TARGET_MODE, N)
        freqs.append(f)

    f_ref = freqs[-1]       # highest-N result as reference

    print("  2. CONVERGENCE TABLE")
    print("  " + "-" * 65)
    print(f"  {'N':>3}  {'2N DOFs':>7}  {'f_2 (Hz)':>10}  "
          f"{'Df vs N=8 (%)':>14}  {'Df vs sphere (%)':>17}")
    print("  " + "-" * 65)

    for i, N in enumerate(N_values):
        err_ref = (freqs[i] - f_ref) / f_ref * 100
        err_sph = (freqs[i] - f_sphere) / f_sphere * 100
        print(f"  {N:>3}  {2*N:>7}  {freqs[i]:>10.5f}  "
              f"{err_ref:>+14.5f}  {err_sph:>+17.2f}")

    print("  " + "-" * 65)
    print(f"  Converged value (N=8):     f_2 = {f_ref:.5f} Hz")
    print(f"  Equivalent-sphere model:   f_2 = {f_sphere:.4f} Hz")
    print()

    # ── 4. Convergence verdict ───────────────────────────────
    err_1dof = abs(freqs[0] - f_ref) / f_ref * 100
    err_2dof = abs(freqs[1] - f_ref) / f_ref * 100 if len(freqs) > 1 else 0

    print("  3. CONVERGENCE VERDICT")
    print("  " + "-" * 55)
    if err_1dof < 5:
        print(f"  PASS  2-DOF model (N=1) within {err_1dof:.3f}% of converged")
        print(f"        value (tolerance 5%).")
    else:
        print(f"  NOTE  2-DOF model deviates by {err_1dof:.3f}% from converged.")
    if err_2dof < 1:
        print(f"  PASS  4-DOF model (N=2) within {err_2dof:.3f}% (< 1%).")
    print()

    # Monotone-decreasing check (Rayleigh-Ritz upper-bound property)
    monotone = all(freqs[i] >= freqs[i+1] - 1e-8 for i in range(len(freqs)-1))
    print(f"  Upper-bound monotonicity:  {'PASS' if monotone else 'FAIL'}")
    print(f"  (Rayleigh-Ritz frequencies must decrease with enrichment.)")
    print()

    # ── 5. Generate publication figure ───────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    # Left: frequency vs N
    ax1.plot(N_values, freqs, 'ko-', markersize=7, linewidth=1.5,
             label='Enriched Ritz', zorder=3)
    ax1.axhline(f_ref, color='0.6', ls='--', lw=0.8, zorder=1,
                label=f'$N=8$ ref ({f_ref:.3f} Hz)')
    ax1.axhline(f_sphere, color='C0', ls=':', lw=1.0, zorder=1,
                label=f'Equiv. sphere ({f_sphere:.2f} Hz)')
    ax1.set_xlabel('Basis functions per component, $N$')
    ax1.set_ylabel(r'$f_2$ (Hz)')
    ax1.set_title(r'(a) Convergence of $n{=}2$ flexural frequency')
    ax1.set_xticks(N_values)
    ax1.legend(fontsize=8, loc='upper right')
    ax1.grid(True, alpha=0.25)

    # Right: relative error vs N  (log scale)
    errors_pct = [abs(freqs[i] - f_ref) / f_ref * 100
                  for i in range(len(freqs) - 1)]
    ax2.semilogy(N_values[:-1], errors_pct, 'rs-', markersize=7,
                 linewidth=1.5, zorder=3)
    ax2.axhline(1.0, color='green', ls='--', lw=0.8, alpha=0.7,
                label='1 % threshold')
    ax2.axhline(5.0, color='orange', ls='--', lw=0.8, alpha=0.7,
                label='5 % threshold')
    ax2.set_xlabel('Basis functions per component, $N$')
    ax2.set_ylabel('Relative error vs $N{=}8$ (%)')
    ax2.set_title('(b) Convergence rate')
    ax2.set_xticks(N_values[:-1])
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.25)

    plt.tight_layout()

    out_path = os.path.join(
        _REPO, 'papers', 'paper1-brown-note', 'figures',
        'fig_ritz_convergence.pdf',
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, bbox_inches='tight', dpi=300)

    # Also save PNG for quick inspection
    fig.savefig(out_path.replace('.pdf', '.png'), bbox_inches='tight', dpi=150)
    plt.close(fig)

    print(f"  Figure saved: {os.path.relpath(out_path, _REPO)}")
    print(f"                {os.path.relpath(out_path.replace('.pdf', '.png'), _REPO)}")
    print()
    print("=" * 72)
    print("  DONE")
    print("=" * 72)


if __name__ == "__main__":
    main()
