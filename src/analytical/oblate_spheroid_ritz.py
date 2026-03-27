"""
Rayleigh-Ritz analysis for flexural vibrations of a fluid-filled oblate
spheroidal shell.

For each mode number n, builds a 2-DOF Rayleigh-Ritz problem:
  w(η) = β · P_n(η)                     — normal displacement
  u(θ) = α · sin θ · P_n'(cos θ)        — tangential (meridional)

and solves the 2×2 generalised eigenvalue problem  K q = ω² M q.

Strain energy: Love-Kirchhoff thin shell (membrane + bending) plus
prestress from intra-abdominal pressure, integrated via Gauss-Legendre
quadrature over the oblate spheroid surface parameterised by η = cos θ.

Fluid kinetic energy: interior Laplace solution in oblate spheroidal
coordinates using Legendre functions P_n(iξ).

References
----------
    Elaikh et al. (2016) J. Thin-Walled Structures
    Junger & Feit (1972) Sound, Structures, and Their Interaction
    Lamb (1882) Proc. London Math. Soc.
"""

import numpy as np
from scipy.special import legendre as _legendre_poly
from numpy.polynomial.legendre import leggauss
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)


# ============================================================
# Geometry helpers
# ============================================================

def _oblate_geom(a, c, eta):
    """Return dict of geometric quantities at η = cos θ."""
    eta2 = eta**2
    sin2 = 1.0 - eta2
    G = a**2 * eta2 + c**2 * sin2
    sqG = np.sqrt(G)
    R2 = a * sqG / c
    return dict(G=G, sqG=sqG, sin2=sin2, Delta=a**2 - c**2,
                N1_per_P=R2 / 2.0)


# ============================================================
# 2×2 stiffness and mass for a single mode n
# ============================================================

def _build_KM(n, a, c, h, E, nu, P_iap, rho_w, rho_f, eta_q, w_q):
    """
    2×2 stiffness K and mass M for mode *n*.

    DOF ordering:  q = [β (normal),  α (tangential)]
    """
    geo = _oblate_geom(a, c, eta_q)
    G     = geo['G']
    sqG   = geo['sqG']
    sin2  = geo['sin2']
    Delta = geo['Delta']

    poly = _legendre_poly(n)
    Pn   = poly(eta_q)
    dPn  = poly.deriv(1)(eta_q) if n >= 1 else np.zeros_like(eta_q)
    d2Pn = poly.deriv(2)(eta_q) if n >= 2 else np.zeros_like(eta_q)

    Cm = E * h / (1.0 - nu**2)
    Df = E * h**3 / (12.0 * (1.0 - nu**2))
    nn1 = n * (n + 1)

    K = np.zeros((2, 2))
    M = np.zeros((2, 2))

    for k in range(len(eta_q)):
        g, sg, s2, eta, wt = G[k], sqG[k], sin2[k], eta_q[k], w_q[k]

        # ── membrane strain bases  (f = ε × √G) ────────────
        e1 = np.array([
            a * c * Pn[k] / g,                        # w-DOF
            -eta * dPn[k] + nn1 * Pn[k],              # u-DOF  (du/dθ)
        ])
        e2 = np.array([
            c * Pn[k] / a,                            # w-DOF
            eta * dPn[k],                              # u-DOF
        ])

        fac_m = 2.0 * np.pi * a * Cm * wt / sg
        K += fac_m * (np.outer(e1, e1) + np.outer(e2, e2)
                      + nu * (np.outer(e1, e2) + np.outer(e2, e1)))

        # ── bending curvature bases ─────────────────────────
        # h_w = P_n'/√G,  h_u = P_n' ac/G^{3/2}
        Gp = 2.0 * Delta * eta
        hw  = dPn[k] / sg
        hwp = d2Pn[k] / sg - dPn[k] * Delta * eta / g**1.5
        hu  = dPn[k] * a * c / g**1.5
        hup = (d2Pn[k] * a * c / g**1.5
               - dPn[k] * a * c * 1.5 * Gp / g**2.5)

        kk1 = np.array([
            (eta * hw  - s2 * hwp) / sg,
            (eta * hu  - s2 * hup) / sg,
        ])
        kk2 = np.array([
            eta * dPn[k] / g,
            eta * dPn[k] * a * c / g**2,
        ])

        fac_b = 2.0 * np.pi * a * Df * sg * wt
        K += fac_b * (np.outer(kk1, kk1) + np.outer(kk2, kk2)
                      + nu * (np.outer(kk1, kk2) + np.outer(kk2, kk1)))

        # ── prestress (geometric stiffness, w-DOF only) ────
        if P_iap > 0:
            N1 = P_iap * geo['N1_per_P'][k]
            sl = np.sqrt(max(s2, 0.0) / g) * dPn[k]
            fac_p = 2.0 * np.pi * a * N1 * sg * wt
            K[0, 0] += fac_p * sl * sl

        # ── shell mass ──────────────────────────────────────
        fac_ms = 2.0 * np.pi * a * rho_w * h * sg * wt
        M[0, 0] += fac_ms * Pn[k]**2
        M[1, 1] += fac_ms * max(s2, 0.0) * dPn[k]**2

    # ── fluid added mass (w-DOF only) ──────────────────────
    M[0, 0] += _fluid_mass(n, a, c, rho_f, eta_q, w_q)
    return K, M


# ============================================================
# Fluid added mass via oblate spheroidal harmonics
# ============================================================

def _fluid_mass(n, a, c, rho_f, eta_q, w_q):
    """Scalar fluid added-mass for mode n (contribution to M[0,0])."""
    if n < 1:
        return 0.0

    Pn = _legendre_poly(n)(eta_q)
    sqG = np.sqrt(a**2 * eta_q**2 + c**2 * (1.0 - eta_q**2))
    dSw = 2.0 * np.pi * a * sqG

    aspect = c / a
    if aspect > 0.995:
        R = (a * a * c) ** (1.0 / 3.0)
        return rho_f * R / n * np.dot(w_q, Pn**2 * dSw)

    d = np.sqrt(a**2 - c**2)
    xi0 = c / d
    z0 = 1j * xi0
    sqrt_xi = np.sqrt(xi0**2 + 1.0)

    # Laplace expansion — same parity only
    lap = [m for m in range(max(1, n - 6), n + 8) if m % 2 == n % 2]
    NL = len(lap)

    Pz = np.array([_legendre_poly(m)(z0) for m in lap])
    gam = np.array([1j * _legendre_poly(m).deriv(1)(z0) * sqrt_xi / d
                     for m in lap])

    Plap = np.array([_legendre_poly(m)(eta_q) for m in lap])
    inv_h = 1.0 / np.sqrt(xi0**2 + eta_q**2)
    S = np.array([[np.dot(w_q, Plap[i] * Plap[j] * inv_h)
                    for j in range(NL)] for i in range(NL)])
    C = S * gam[np.newaxis, :]

    b = np.zeros(NL, dtype=complex)
    if n in lap:
        b[lap.index(n)] = 2.0 / (2 * n + 1)
    else:
        R = (a * a * c) ** (1.0 / 3.0)
        return rho_f * R / n * np.dot(w_q, Pn**2 * dSw)

    try:
        A = np.linalg.solve(C, b)
    except np.linalg.LinAlgError:
        R = (a * a * c) ** (1.0 / 3.0)
        return rho_f * R / n * np.dot(w_q, Pn**2 * dSw)

    Phi = np.zeros_like(eta_q)
    for idx, m in enumerate(lap):
        Phi += np.real(A[idx] * Pz[idx]) * Plap[idx]

    return rho_f * np.dot(w_q, Phi * Pn * dSw)


# ============================================================
# Public API
# ============================================================

def oblate_ritz_frequency(n, a, c, h, E, nu, rho_w, rho_f, P_iap,
                          n_quad=200):
    """Flexural frequency (Hz) for mode *n* via 2-DOF Rayleigh-Ritz."""
    if n < 2:
        return 0.0
    eta_q, w_q = leggauss(n_quad)
    K, M = _build_KM(n, a, c, h, E, nu, P_iap, rho_w, rho_f, eta_q, w_q)
    eps = max(np.abs(np.diag(M)).max(), 1e-30) * 1e-14
    M += eps * np.eye(2)
    eigvals = np.linalg.eigvalsh(np.linalg.solve(M, K))
    return np.sqrt(max(eigvals.min(), 0.0)) / (2.0 * np.pi)


def oblate_ritz_frequencies(a, c, h, E, nu, rho_w, rho_f, P_iap,
                            n_target=(2, 3, 4), n_quad=200):
    """Dict {n: freq_hz} for each requested mode."""
    return {n: oblate_ritz_frequency(n, a, c, h, E, nu, rho_w, rho_f,
                                     P_iap, n_quad)
            for n in n_target}


def sphere_approx_frequencies(model, n_modes=(2, 3, 4)):
    """Equivalent-sphere frequencies from natural_frequency_v2."""
    f = flexural_mode_frequencies_v2(model, n_max=max(n_modes))
    return {n: f[n] for n in n_modes}


# ============================================================
# Comparison driver
# ============================================================

def comparison_table(model_base=None, aspect_ratios=None,
                     E_values=None, n_modes=(2, 3, 4)):
    if model_base is None:
        model_base = AbdominalModelV2()
    if aspect_ratios is None:
        aspect_ratios = [0.50, 0.60, 0.667, 0.70, 0.80, 0.90]
    if E_values is None:
        E_values = [model_base.E]

    a = model_base.a
    rows = []
    for Ev in E_values:
        for ar in aspect_ratios:
            cv = a * ar
            msph = AbdominalModelV2(a=a, b=a, c=cv, h=model_base.h,
                                    E=Ev, nu=model_base.nu,
                                    rho_wall=model_base.rho_wall,
                                    rho_fluid=model_base.rho_fluid,
                                    P_iap=model_base.P_iap)
            fs = sphere_approx_frequencies(msph, n_modes)
            fr = oblate_ritz_frequencies(a, cv, model_base.h, Ev,
                                         model_base.nu, model_base.rho_wall,
                                         model_base.rho_fluid,
                                         model_base.P_iap, n_modes)
            row = {'E_MPa': Ev / 1e6, 'c/a': ar}
            for n in n_modes:
                err = (fs[n] - fr[n]) / fr[n] * 100 if fr[n] > 0 else float('nan')
                row[f'f{n}_sphere'] = fs[n]
                row[f'f{n}_ritz']   = fr[n]
                row[f'f{n}_err%']   = err
            rows.append(row)
    return rows


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print()
    print("=" * 78)
    print("  OBLATE SPHEROID RAYLEIGH-RITZ ANALYSIS")
    print("  Flexural vibrations of a fluid-filled oblate spheroidal shell")
    print("=" * 78)
    print()

    model = AbdominalModelV2()
    n_modes = (2, 3, 4)

    # ── 1. Baseline ──────────────────────────────────────────
    print("  1. BASELINE: default geometry (a=0.15 m, c=0.10 m, E=0.5 MPa)")
    print("  " + "-" * 50)
    fs = sphere_approx_frequencies(model, n_modes)
    fr = oblate_ritz_frequencies(model.a, model.c, model.h, model.E,
                                 model.nu, model.rho_wall, model.rho_fluid,
                                 model.P_iap, n_modes)
    print(f"  {'Mode':>6} {'Sphere(Hz)':>12} {'Ritz(Hz)':>12} {'Err(%)':>10}")
    print("  " + "-" * 50)
    for n in n_modes:
        e = (fs[n] - fr[n]) / fr[n] * 100 if fr[n] > 0 else float('nan')
        print(f"  n={n:>3} {fs[n]:>12.3f} {fr[n]:>12.3f} {e:>+10.1f}")
    print()

    # ── 2. Sphere-limit sanity check ─────────────────────────
    print("  2. SPHERE-LIMIT CHECK (c/a → 1)")
    print("  " + "-" * 60)
    print(f"  {'c/a':>6}  {'n=2 sph':>8} {'n=2 Ritz':>9} {'n=3 sph':>8}"
          f" {'n=3 Ritz':>9}")
    for ar in [0.90, 0.95, 0.99]:
        cv = model.a * ar
        ms = AbdominalModelV2(a=model.a, b=model.a, c=cv)
        s = sphere_approx_frequencies(ms, (2, 3))
        r = oblate_ritz_frequencies(model.a, cv, model.h, model.E,
                                    model.nu, model.rho_wall,
                                    model.rho_fluid, model.P_iap, (2, 3))
        print(f"  {ar:>6.3f}  {s[2]:>8.2f} {r[2]:>9.2f} {s[3]:>8.2f}"
              f" {r[3]:>9.2f}")
    print()

    # ── 3. Aspect-ratio sweep ─────────────────────────────────
    aspect_ratios = [0.50, 0.60, 0.667, 0.70, 0.80, 0.90]

    for Ev, label in [(0.5e6, "E = 0.5 MPa (baseline)"),
                      (0.1e6, "E = 0.1 MPa (soft tissue)")]:
        print(f"  3. ASPECT-RATIO SWEEP — {label}")
        print("  " + "-" * 74)
        hdr = f"  {'c/a':>5}"
        for n in n_modes:
            hdr += f" {'Sph n='+str(n):>9} {'Ritz n='+str(n):>10} {'err%':>7}"
        print(hdr)
        print("  " + "-" * 74)

        rows = comparison_table(model_base=model,
                                aspect_ratios=aspect_ratios,
                                E_values=[Ev], n_modes=n_modes)
        for r in rows:
            line = f"  {r['c/a']:>5.3f}"
            for n in n_modes:
                line += (f" {r[f'f{n}_sphere']:>9.2f}"
                         f" {r[f'f{n}_ritz']:>10.2f}"
                         f" {r[f'f{n}_err%']:>+7.1f}")
            print(line)
        print("  " + "-" * 74)
        print()

    # ── 4. Summary ────────────────────────────────────────────
    print("  4. SUMMARY")
    print("  " + "-" * 70)
    print("  • The sphere model consistently OVERESTIMATES the flexural")
    print("    frequencies of the oblate spheroid.")
    print("  • Error grows with oblateness (lower c/a) and is non-trivial")
    print("    even at c/a = 0.9.")
    print("  • Physical reason: oblate geometry has larger equatorial radii")
    print("    of curvature → lower membrane stiffness; and different")
    print("    fluid inertia from oblate spheroidal flow pattern.")
    print("  • For the default model (c/a ≈ 0.67, E = 0.5 MPa), the")
    print("    n = 2 sphere model error is significant for quantitative")
    print("    predictions of resonance frequency.")
    print()
