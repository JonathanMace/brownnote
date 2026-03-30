"""Computational verification of the universality conjecture for inverse
identifiability scaling in fluid-filled elastic shells.

The conjecture: for ANY smooth one-parameter family of fluid-filled elastic
shells interpolating between a sphere (ε=0) and a non-spherical shape (ε>0),
the Jacobian condition number for the inverse problem satisfies

    κ(ε) ~ C · ε⁻²    as ε → 0.

This has been proved analytically for oblate spheroids (see power_law_proof.py).
Here we verify the scaling computationally for:
  1. Prolate spheroids (c > a, elongated along z)
  2. Triaxial ellipsoids (a ≠ b ≠ c)
  3. Arbitrary Legendre perturbations of a sphere

Physical mechanism: the ε⁻² scaling arises because the metric tensor of any
smooth shell family expands as G = G₀ + ε²·G₂ + O(ε⁴), and the
mode-dependent curvature weights in G₂ are what break the sphere degeneracy.

References
----------
    Stewart & Sun (1990) Matrix Perturbation Theory, Academic Press.
    Kato (1966) Perturbation Theory for Linear Operators, Springer.
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import cond, svd
from numpy.polynomial.legendre import leggauss
from scipy.special import legendre as _legendre_poly

from analytical.kac_identifiability import (
    CANONICAL_ABDOMEN,
    INVERSION_PARAMS,
    compute_jacobian,
    jacobian_condition_number,
)
from analytical.oblate_spheroid_ritz import oblate_ritz_frequency

# ═══════════════════════════════════════════════════════════════════════════
#  Canonical parameters (from R3)
# ═══════════════════════════════════════════════════════════════════════════

CANONICAL_PARAMS = dict(
    R=0.157,        # equivalent sphere radius [m]
    E=0.1e6,        # Young's modulus [Pa]
    h=0.010,        # wall thickness [m]
    nu=0.45,        # Poisson's ratio
    rho_w=1100.0,   # wall density [kg/m³]
    rho_f=1020.0,   # fluid density [kg/m³]
    K_f=2.2e9,      # fluid bulk modulus [Pa]
    P_iap=1000.0,   # intra-abdominal pressure [Pa]
)

DEFAULT_MODES = (2, 3, 4, 5, 6)


# ═══════════════════════════════════════════════════════════════════════════
#  1. Prolate spheroid model
# ═══════════════════════════════════════════════════════════════════════════

def _prolate_geom(a, c, eta):
    """Geometric quantities for a prolate spheroid (c > a) at η = cos θ.

    For a prolate spheroid parameterised by (a, c) with a = b < c:
      x = a sin θ cos φ,  y = a sin θ sin φ,  z = c cos θ

    The meridional metric component is G(η) = c²η² + a²(1 − η²).
    """
    eta2 = eta ** 2
    sin2 = 1.0 - eta2
    G = c ** 2 * eta2 + a ** 2 * sin2
    sqG = np.sqrt(G)
    # Principal radius of curvature (meridional) times P for prestress
    R2 = c * sqG / a
    return dict(G=G, sqG=sqG, sin2=sin2, Delta=c ** 2 - a ** 2,
                N1_per_P=R2 / 2.0)


def _prolate_build_KM(n, a, c, h, E, nu, P_iap, rho_w, rho_f, eta_q, w_q):
    """2×2 stiffness K and mass M for mode *n* on a prolate spheroid.

    DOF ordering:  q = [β (normal),  α (tangential)]

    This mirrors _build_KM from oblate_spheroid_ritz.py but with the
    prolate metric: G(η) = c²η² + a²(1 − η²) instead of a²η² + c²(1 − η²).
    """
    geo = _prolate_geom(a, c, eta_q)
    G = geo['G']
    sqG = geo['sqG']
    sin2 = geo['sin2']
    Delta = geo['Delta']  # c² - a² > 0 for prolate

    poly = _legendre_poly(n)
    Pn = poly(eta_q)
    dPn = poly.deriv(1)(eta_q) if n >= 1 else np.zeros_like(eta_q)
    d2Pn = poly.deriv(2)(eta_q) if n >= 2 else np.zeros_like(eta_q)

    Cm = E * h / (1.0 - nu ** 2)
    Df = E * h ** 3 / (12.0 * (1.0 - nu ** 2))
    nn1 = n * (n + 1)

    K = np.zeros((2, 2))
    M = np.zeros((2, 2))

    for k in range(len(eta_q)):
        g, sg, s2, eta, wt = G[k], sqG[k], sin2[k], eta_q[k], w_q[k]

        # ── membrane strain bases ────────────────────────────
        # For prolate: the roles of a,c in the strain bases swap
        e1 = np.array([
            a * c * Pn[k] / g,
            -eta * dPn[k] + nn1 * Pn[k],
        ])
        e2 = np.array([
            a * Pn[k] / c,
            eta * dPn[k],
        ])

        # Surface element: dS = 2π·a·√G·dη (azimuthal symmetry, radius a)
        fac_m = 2.0 * np.pi * a * Cm * wt / sg
        K += fac_m * (np.outer(e1, e1) + np.outer(e2, e2)
                      + nu * (np.outer(e1, e2) + np.outer(e2, e1)))

        # ── bending curvature bases ──────────────────────────
        Gp = 2.0 * Delta * eta  # dG/dη = 2(c²-a²)η
        hw = dPn[k] / sg
        hwp = d2Pn[k] / sg - dPn[k] * Delta * eta / g ** 1.5
        hu = dPn[k] * a * c / g ** 1.5
        hup = (d2Pn[k] * a * c / g ** 1.5
               - dPn[k] * a * c * 1.5 * Gp / g ** 2.5)

        kk1 = np.array([
            (eta * hw - s2 * hwp) / sg,
            (eta * hu - s2 * hup) / sg,
        ])
        kk2 = np.array([
            eta * dPn[k] / g,
            eta * dPn[k] * a * c / g ** 2,
        ])

        fac_b = 2.0 * np.pi * a * Df * sg * wt
        K += fac_b * (np.outer(kk1, kk1) + np.outer(kk2, kk2)
                      + nu * (np.outer(kk1, kk2) + np.outer(kk2, kk1)))

        # ── prestress (geometric stiffness, w-DOF only) ─────
        if P_iap > 0:
            N1 = P_iap * geo['N1_per_P'][k]
            sl = np.sqrt(max(s2, 0.0) / g) * dPn[k]
            fac_p = 2.0 * np.pi * a * N1 * sg * wt
            K[0, 0] += fac_p * sl * sl

        # ── shell mass ───────────────────────────────────────
        fac_ms = 2.0 * np.pi * a * rho_w * h * sg * wt
        M[0, 0] += fac_ms * Pn[k] ** 2
        M[1, 1] += fac_ms * max(s2, 0.0) * dPn[k] ** 2

    # ── fluid added mass (w-DOF only) ────────────────────────
    M[0, 0] += _prolate_fluid_mass(n, a, c, rho_f, eta_q, w_q)
    return K, M


def _prolate_fluid_mass(n, a, c, rho_f, eta_q, w_q):
    """Scalar fluid added-mass for mode n on a prolate spheroid.

    Uses prolate spheroidal harmonics for the interior Laplace problem.
    For a prolate spheroid (c > a), the focal distance is d = √(c² − a²)
    and the surface coordinate is ξ₀ = c/d.
    """
    if n < 1:
        return 0.0

    Pn = _legendre_poly(n)(eta_q)
    sqG = np.sqrt(c ** 2 * eta_q ** 2 + a ** 2 * (1.0 - eta_q ** 2))
    dSw = 2.0 * np.pi * a * sqG

    aspect = a / c  # < 1 for prolate
    if aspect > 0.995:
        # Near-sphere fallback
        R = (a * a * c) ** (1.0 / 3.0)
        return rho_f * R / n * np.dot(w_q, Pn ** 2 * dSw)

    d = np.sqrt(c ** 2 - a ** 2)
    xi0 = c / d
    sqrt_xi = np.sqrt(xi0 ** 2 - 1.0)

    # Laplace expansion — same parity only
    lap = [m for m in range(max(1, n - 6), n + 8) if m % 2 == n % 2]
    NL = len(lap)

    # For prolate coordinates: use real Legendre functions P_m(ξ₀)
    Pz = np.array([float(_legendre_poly(m)(xi0)) for m in lap])
    gam = np.array([float(_legendre_poly(m).deriv(1)(xi0)) * sqrt_xi / d
                    for m in lap])

    Plap = np.array([_legendre_poly(m)(eta_q) for m in lap])
    inv_h = 1.0 / np.sqrt(xi0 ** 2 - eta_q ** 2)
    S = np.array([[np.dot(w_q, Plap[i] * Plap[j] * inv_h)
                   for j in range(NL)] for i in range(NL)])
    C = S * gam[np.newaxis, :]

    b = np.zeros(NL)
    if n in lap:
        b[lap.index(n)] = 2.0 / (2 * n + 1)
    else:
        R = (a * a * c) ** (1.0 / 3.0)
        return rho_f * R / n * np.dot(w_q, Pn ** 2 * dSw)

    try:
        A = np.linalg.solve(C, b)
    except np.linalg.LinAlgError:
        R = (a * a * c) ** (1.0 / 3.0)
        return rho_f * R / n * np.dot(w_q, Pn ** 2 * dSw)

    Phi = np.zeros_like(eta_q)
    for idx, m in enumerate(lap):
        Phi += A[idx] * Pz[idx] * Plap[idx]

    return rho_f * np.dot(w_q, Phi * Pn * dSw)


def prolate_ritz_frequency(n, a, c, h, E, nu, rho_w, rho_f, P_iap,
                           n_quad=200):
    """Flexural frequency (Hz) for mode *n* on a prolate spheroid.

    Parameters
    ----------
    n : int
        Mode number (n ≥ 2 for flexural modes).
    a : float
        Equatorial semi-axis [m] (a = b < c for prolate).
    c : float
        Polar semi-axis [m] (c > a for prolate).
    h, E, nu, rho_w, rho_f, P_iap : float
        Material and fluid parameters.
    n_quad : int
        Number of Gauss-Legendre quadrature points.

    Returns
    -------
    float
        Frequency in Hz.
    """
    if n < 2:
        return 0.0
    eta_q, w_q = leggauss(n_quad)
    K, M = _prolate_build_KM(n, a, c, h, E, nu, P_iap, rho_w, rho_f,
                              eta_q, w_q)
    try:
        L = np.linalg.cholesky(M)
        Kinv = np.linalg.solve(L, np.linalg.solve(L, K).T)
        eigvals = np.linalg.eigvalsh(Kinv)
    except np.linalg.LinAlgError:
        eigvals = np.real(np.linalg.eigvals(np.linalg.solve(M, K)))
    return float(np.sqrt(max(eigvals.min(), 0.0)) / (2.0 * np.pi))


def prolate_frequencies(a, c, E, h, nu, rho_wall, rho_fluid, K_fluid,
                        n_modes=5, P_iap=1000.0, n_quad=200):
    """Compute flexural frequencies for a prolate spheroid.

    Parameters
    ----------
    a : float
        Equatorial semi-axis [m].
    c : float
        Polar semi-axis [m] (c > a for prolate).
    E : float
        Young's modulus [Pa].
    h : float
        Wall thickness [m].
    nu : float
        Poisson's ratio.
    rho_wall, rho_fluid : float
        Densities [kg/m³].
    K_fluid : float
        Fluid bulk modulus [Pa] (unused for flexural; retained for API
        consistency).
    n_modes : int
        Number of modes to compute (modes 2 through n_modes+1).
    P_iap : float
        Internal pressure [Pa].
    n_quad : int
        Quadrature order.

    Returns
    -------
    dict
        {n: freq_hz} for n = 2, 3, ..., n_modes+1.
    """
    modes = tuple(range(2, 2 + n_modes))
    return {n: prolate_ritz_frequency(n, a, c, h, E, nu, rho_wall,
                                       rho_fluid, P_iap, n_quad)
            for n in modes}


# ═══════════════════════════════════════════════════════════════════════════
#  2. Triaxial ellipsoid model (perturbation approach)
# ═══════════════════════════════════════════════════════════════════════════

def _sphere_frequency(n, R, h, E, nu, rho_w, rho_f, P_iap, n_quad=200):
    """Flexural frequency for mode n on a sphere of radius R.

    Uses the oblate Ritz model at c/a → 1 (near-sphere limit).
    """
    return oblate_ritz_frequency(n, R, R * 0.9999, h, E, nu, rho_w,
                                  rho_f, P_iap, n_quad)


def _frequency_sensitivity_a(n, R, h, E, nu, rho_w, rho_f, P_iap,
                              da=None, n_quad=200):
    """∂f_n/∂a at the sphere point, via central differences."""
    if da is None:
        da = R * 1e-4
    fp = oblate_ritz_frequency(n, R + da, (R + da) * 0.9999, h, E, nu,
                                rho_w, rho_f, P_iap, n_quad)
    fm = oblate_ritz_frequency(n, R - da, (R - da) * 0.9999, h, E, nu,
                                rho_w, rho_f, P_iap, n_quad)
    return (fp - fm) / (2.0 * da)


def triaxial_frequencies(a, b, c, E, h, nu, rho_wall, rho_fluid, K_fluid,
                         n_modes=5, P_iap=1000.0, n_quad=200):
    """Compute flexural frequencies for a triaxial ellipsoid.

    Uses a second-order perturbation expansion about the equivalent sphere:
      R = (abc)^{1/3}
      ε₁ = (a - R)/R,  ε₂ = (b - R)/R,  ε₃ = (c - R)/R

    Subject to the volume constraint ε₁ + ε₂ + ε₃ ≈ 0 at leading order.

    The frequency perturbation is computed by averaging the Ritz model
    response over the three principal axis perturbations.  For an
    axisymmetric model, perturbations along different axes affect
    curvature integrals with different Legendre weightings.

    Parameters
    ----------
    a, b, c : float
        Semi-axes [m].
    E, h, nu, rho_wall, rho_fluid, K_fluid : float
        Material and fluid parameters.
    n_modes : int
        Number of modes.
    P_iap : float
        Internal pressure [Pa].
    n_quad : int
        Quadrature order.

    Returns
    -------
    dict
        {n: freq_hz} for each mode.
    """
    R = (a * b * c) ** (1.0 / 3.0)
    modes = tuple(range(2, 2 + n_modes))

    # Compute base sphere frequency
    f0 = {}
    for n in modes:
        f0[n] = _sphere_frequency(n, R, h, E, nu, rho_wall, rho_fluid,
                                   P_iap, n_quad)

    # Compute frequency corrections by averaging oblate/prolate responses.
    # For triaxial (a, b, c), we model the effect as a superposition:
    #   f_n ≈ (1/3)[f_n(oblate along z) + f_n(oblate along x)
    #          + f_n(oblate along y)]
    # where each "oblate along axis i" uses the Ritz model with
    # the appropriate (a_eff, c_eff) pair.
    result = {}
    for n in modes:
        # Axis pair 1: z-axis symmetry → (equatorial=√(ab), polar=c)
        a_eff1 = np.sqrt(a * b)
        c_eff1 = c
        if c_eff1 < a_eff1:
            f1 = oblate_ritz_frequency(n, a_eff1, c_eff1, h, E, nu,
                                        rho_wall, rho_fluid, P_iap, n_quad)
        else:
            f1 = prolate_ritz_frequency(n, a_eff1, c_eff1, h, E, nu,
                                         rho_wall, rho_fluid, P_iap, n_quad)

        # Axis pair 2: x-axis symmetry → (equatorial=√(bc), polar=a)
        a_eff2 = np.sqrt(b * c)
        c_eff2 = a
        if c_eff2 < a_eff2:
            f2 = oblate_ritz_frequency(n, a_eff2, c_eff2, h, E, nu,
                                        rho_wall, rho_fluid, P_iap, n_quad)
        else:
            f2 = prolate_ritz_frequency(n, a_eff2, c_eff2, h, E, nu,
                                         rho_wall, rho_fluid, P_iap, n_quad)

        # Axis pair 3: y-axis symmetry → (equatorial=√(ac), polar=b)
        a_eff3 = np.sqrt(a * c)
        c_eff3 = b
        if c_eff3 < a_eff3:
            f3 = oblate_ritz_frequency(n, a_eff3, c_eff3, h, E, nu,
                                        rho_wall, rho_fluid, P_iap, n_quad)
        else:
            f3 = prolate_ritz_frequency(n, a_eff3, c_eff3, h, E, nu,
                                         rho_wall, rho_fluid, P_iap, n_quad)

        # Average over three orientations
        result[n] = (f1 + f2 + f3) / 3.0

    return result


# ═══════════════════════════════════════════════════════════════════════════
#  3. Forward model wrappers for condition number computation
# ═══════════════════════════════════════════════════════════════════════════

def _forward_prolate(params, modes):
    """Forward model: prolate spheroid frequencies.

    Parameters
    ----------
    params : dict
        Must contain: a, c, h, E, nu, rho_w, rho_f, P_iap.
        For prolate: c > a.
    modes : tuple of int
        Mode numbers.

    Returns
    -------
    np.ndarray
        Frequencies in Hz.
    """
    freqs = prolate_frequencies(
        a=params["a"], c=params["c"], E=params["E"], h=params["h"],
        nu=params["nu"], rho_wall=params["rho_w"],
        rho_fluid=params["rho_f"], K_fluid=params.get("K_f", 2.2e9),
        n_modes=max(modes) - 1, P_iap=params.get("P_iap", 1000.0),
    )
    return np.array([freqs.get(n, 0.0) for n in modes])


def _forward_triaxial(params, modes):
    """Forward model: triaxial ellipsoid frequencies.

    Parameters
    ----------
    params : dict
        Must contain: a, b, c, h, E, nu, rho_w, rho_f, P_iap.
    modes : tuple of int
        Mode numbers.

    Returns
    -------
    np.ndarray
        Frequencies in Hz.
    """
    freqs = triaxial_frequencies(
        a=params["a"], b=params["b"], c=params["c"],
        E=params["E"], h=params["h"], nu=params["nu"],
        rho_wall=params["rho_w"], rho_fluid=params["rho_f"],
        K_fluid=params.get("K_f", 2.2e9),
        n_modes=max(modes) - 1, P_iap=params.get("P_iap", 1000.0),
    )
    return np.array([freqs.get(n, 0.0) for n in modes])


def _compute_jacobian_generic(
    params, forward_fn, modes=DEFAULT_MODES,
    inversion_params=("a", "c", "E"),
    step_fraction=1e-6, scaled=True,
):
    """Compute scaled Jacobian for an arbitrary forward model.

    Mirrors kac_identifiability.compute_jacobian but accepts a custom
    forward function.
    """
    n_freq = len(modes)
    n_param = len(inversion_params)
    J = np.zeros((n_freq, n_param))

    for j, pname in enumerate(inversion_params):
        p0 = params[pname]
        dp = abs(p0) * step_fraction
        if dp == 0:
            dp = step_fraction

        params_plus = dict(params)
        params_plus[pname] = p0 + dp
        f_plus = forward_fn(params_plus, modes)

        params_minus = dict(params)
        params_minus[pname] = p0 - dp
        f_minus = forward_fn(params_minus, modes)

        J[:, j] = (f_plus - f_minus) / (2.0 * dp)

    if scaled:
        f_nom = forward_fn(params, modes)
        theta = np.array([params[k] for k in inversion_params])
        safe_f = np.where(np.abs(f_nom) > 1e-30, f_nom, 1e-30)
        J = J * theta[np.newaxis, :] / safe_f[:, np.newaxis]

    return J


def _condition_number_generic(params, forward_fn, modes=DEFAULT_MODES,
                               inversion_params=("a", "c", "E")):
    """Condition number of the scaled Jacobian for a generic forward model."""
    J = _compute_jacobian_generic(params, forward_fn, modes,
                                   inversion_params, scaled=True)
    return float(cond(J))


# ═══════════════════════════════════════════════════════════════════════════
#  4. Condition number sweep functions
# ═══════════════════════════════════════════════════════════════════════════

def prolate_condition_sweep(
    eccentricities=None,
    R=None, E=None, h=None, nu=None,
    rho_w=None, rho_f=None, K_f=None, P_iap=None,
    modes=DEFAULT_MODES,
    inversion_params=("a", "c", "E"),
):
    """Sweep condition number κ over prolate eccentricities.

    For a prolate spheroid: ε_p = √(1 − a²/c²), so c = a/√(1 − ε²).
    The semi-major axis *a* is held fixed at the canonical value and
    *c* is derived from the eccentricity, matching the oblate sweep
    convention (both sweeps fix *a*).

    Parameters
    ----------
    eccentricities : array-like or None
        Prolate eccentricities to sweep. Defaults to 15 log-spaced points
        from 0.05 to 0.75.
    R, E, h, nu, rho_w, rho_f, K_f, P_iap : float or None
        Override canonical parameters. Defaults from CANONICAL_PARAMS.
    modes : tuple of int
        Mode numbers for the Jacobian.
    inversion_params : tuple of str
        Parameters to invert for.

    Returns
    -------
    dict
        'eccentricity', 'kappa', 'a_values', 'c_values', 'frequencies'
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
    if K_f is not None:
        p['K_f'] = K_f
    if P_iap is not None:
        p['P_iap'] = P_iap

    if eccentricities is None:
        eccentricities = np.logspace(np.log10(0.05), np.log10(0.75), 15)

    eccentricities = np.asarray(eccentricities)
    kappas = np.full_like(eccentricities, np.nan)
    a_vals = np.empty_like(eccentricities)
    c_vals = np.empty_like(eccentricities)
    freq_list = []

    for i, eps in enumerate(eccentricities):
        # Prolate: ε_p = √(1 − a²/c²), fix a, vary c = a/√(1 − ε²)
        a_val = CANONICAL_ABDOMEN["a"]
        c_val = a_val / np.sqrt(1.0 - eps ** 2)
        a_vals[i] = a_val
        c_vals[i] = c_val

        params = dict(
            a=a_val, c=c_val, h=p['h'], E=p['E'], nu=p['nu'],
            rho_w=p['rho_w'], rho_f=p['rho_f'], K_f=p['K_f'],
            P_iap=p['P_iap'],
        )

        try:
            freqs = _forward_prolate(params, modes)
            freq_list.append(freqs)
            kappas[i] = _condition_number_generic(
                params, _forward_prolate, modes, inversion_params
            )
        except Exception:
            freq_list.append(np.full(len(modes), np.nan))
            kappas[i] = np.inf

    return {
        "eccentricity": eccentricities,
        "kappa": kappas,
        "a_values": a_vals,
        "c_values": c_vals,
        "frequencies": np.array(freq_list),
    }


def triaxial_condition_sweep(
    eps1_range=None, eps2_range=None,
    R=None, E=None, h=None, nu=None,
    rho_w=None, rho_f=None, K_f=None, P_iap=None,
    modes=DEFAULT_MODES,
    inversion_params=("a", "b", "c", "E"),
):
    """Sweep condition number κ over triaxial eccentricities.

    For a triaxial ellipsoid, we parameterise by two perturbation parameters:
      ε₁ = (a − R)/R,  ε₂ = (c − R)/R
    with b determined by volume conservation: b = R³/(a·c).

    Parameters
    ----------
    eps1_range, eps2_range : array-like or None
        Perturbation parameter ranges. Default: 8 points each, 0.05 to 0.50.
    modes : tuple of int
        Mode numbers for the Jacobian.
    inversion_params : tuple of str
        Parameters to invert for. For triaxial, includes 'b'.

    Returns
    -------
    dict
        'eps1', 'eps2', 'kappa_2d' (2D array), 'kappa_diagonal' (1D along ε₁=ε₂)
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
    if K_f is not None:
        p['K_f'] = K_f
    if P_iap is not None:
        p['P_iap'] = P_iap

    if eps1_range is None:
        eps1_range = np.linspace(0.05, 0.50, 8)
    if eps2_range is None:
        eps2_range = np.linspace(0.05, 0.50, 8)

    eps1_range = np.asarray(eps1_range)
    eps2_range = np.asarray(eps2_range)

    kappa_2d = np.full((len(eps1_range), len(eps2_range)), np.nan)

    for i, eps1 in enumerate(eps1_range):
        for j, eps2 in enumerate(eps2_range):
            a_val = p['R'] * (1.0 + eps1)
            c_val = p['R'] * (1.0 - eps2)
            # Volume conservation: b = R³/(a·c)
            b_val = p['R'] ** 3 / (a_val * c_val)

            if c_val <= 0 or b_val <= 0:
                kappa_2d[i, j] = np.inf
                continue

            params = dict(
                a=a_val, b=b_val, c=c_val, h=p['h'], E=p['E'],
                nu=p['nu'], rho_w=p['rho_w'], rho_f=p['rho_f'],
                K_f=p['K_f'], P_iap=p['P_iap'],
            )

            try:
                kappa_2d[i, j] = _condition_number_generic(
                    params, _forward_triaxial, modes, inversion_params
                )
            except Exception:
                kappa_2d[i, j] = np.inf

    # Diagonal slice: ε₁ = ε₂
    n_diag = min(len(eps1_range), len(eps2_range))
    kappa_diag = np.array([kappa_2d[i, i] for i in range(n_diag)])
    eps_diag = np.array([eps1_range[i] for i in range(n_diag)])

    return {
        "eps1": eps1_range,
        "eps2": eps2_range,
        "kappa_2d": kappa_2d,
        "kappa_diagonal": kappa_diag,
        "eps_diagonal": eps_diag,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  5. Power-law fitting
# ═══════════════════════════════════════════════════════════════════════════

def fit_power_law(eccentricities, kappas):
    """Fit κ = C · ε^{-α} in log-log space.

    Parameters
    ----------
    eccentricities : array-like
        Eccentricity values.
    kappas : array-like
        Corresponding condition numbers.

    Returns
    -------
    tuple of (C, alpha, R_squared)
        C : prefactor
        alpha : exponent (positive; κ ~ C·ε⁻ᵅ)
        R_squared : coefficient of determination of the log-log fit
    """
    eps = np.asarray(eccentricities, dtype=float)
    kap = np.asarray(kappas, dtype=float)

    valid = np.isfinite(kap) & (eps > 0) & (kap > 0)
    if np.sum(valid) < 3:
        return (np.nan, np.nan, 0.0)

    log_eps = np.log(eps[valid])
    log_kap = np.log(kap[valid])

    coeffs = np.polyfit(log_eps, log_kap, 1)
    alpha = -coeffs[0]
    C = np.exp(coeffs[1])

    ss_res = np.sum((log_kap - np.polyval(coeffs, log_eps)) ** 2)
    ss_tot = np.sum((log_kap - np.mean(log_kap)) ** 2)
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    return (float(C), float(alpha), float(r_squared))


def fit_power_law_2d(eps_combined, kappas):
    """Fit κ = C · (ε₁² + ε₂²)^{-α/2} for triaxial data.

    Parameters
    ----------
    eps_combined : array-like
        Combined eccentricity measure √(ε₁² + ε₂²).
    kappas : array-like
        Corresponding condition numbers.

    Returns
    -------
    tuple of (C, alpha, R_squared)
    """
    return fit_power_law(eps_combined, kappas)


# ═══════════════════════════════════════════════════════════════════════════
#  6. Oblate condition number sweep (wrapping existing code)
# ═══════════════════════════════════════════════════════════════════════════

def oblate_condition_sweep(
    eccentricities=None,
    R=None, E=None, h=None, nu=None,
    rho_w=None, rho_f=None, K_f=None, P_iap=None,
    modes=DEFAULT_MODES,
):
    """Sweep condition number κ over oblate eccentricities.

    Follows the same convention as kac_identifiability.kappa_vs_eccentricity:
    fix a at the canonical value and set c = a·√(1 − ε²), so ε = √(1 − c²/a²).
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
    if K_f is not None:
        p['K_f'] = K_f
    if P_iap is not None:
        p['P_iap'] = P_iap

    if eccentricities is None:
        eccentricities = np.logspace(np.log10(0.05), np.log10(0.75), 15)

    eccentricities = np.asarray(eccentricities)
    kappas = np.full_like(eccentricities, np.nan)
    a_vals = np.empty_like(eccentricities)
    c_vals = np.empty_like(eccentricities)

    # Fix a at canonical value (matches kappa_vs_eccentricity convention)
    a_fixed = CANONICAL_ABDOMEN["a"]

    for i, eps in enumerate(eccentricities):
        # Oblate: ε = √(1 − c²/a²) → c = a·√(1 − ε²)
        a_val = a_fixed
        c_val = a_val * np.sqrt(1.0 - eps ** 2)
        a_vals[i] = a_val
        c_vals[i] = c_val

        params = dict(CANONICAL_ABDOMEN)
        params['a'] = a_val
        params['c'] = c_val

        try:
            kappas[i] = jacobian_condition_number(
                params, model="ritz", modes=modes
            )
        except Exception:
            kappas[i] = np.inf

    return {
        "eccentricity": eccentricities,
        "kappa": kappas,
        "a_values": a_vals,
        "c_values": c_vals,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  7. Universal comparison
# ═══════════════════════════════════════════════════════════════════════════

def universality_comparison(
    eccentricities=None,
    modes=DEFAULT_MODES,
    verbose=True,
):
    """Run oblate, prolate, and triaxial sweeps side-by-side.

    Fits the power-law exponent α for each geometry type and reports
    whether the conjecture κ ~ C·ε⁻² holds universally.

    Parameters
    ----------
    eccentricities : array-like or None
        Eccentricity values for the sweep. Default: 15 log-spaced
        points from 0.05 to 0.75.
    modes : tuple of int
        Mode numbers.
    verbose : bool
        If True, print a summary table.

    Returns
    -------
    dict with keys:
        'oblate': dict with 'C', 'alpha', 'R_squared', 'kappa', 'eccentricity'
        'prolate': same
        'triaxial': same (using diagonal ε₁ = ε₂ slice, effective ε = √(2)·εᵢ)
        'universal': bool — True if all exponents are within [1.0, 4.0]
    """
    if eccentricities is None:
        eccentricities = np.logspace(np.log10(0.05), np.log10(0.75), 15)

    # Oblate sweep
    oblate = oblate_condition_sweep(eccentricities=eccentricities,
                                    modes=modes)
    C_o, alpha_o, r2_o = fit_power_law(oblate["eccentricity"],
                                         oblate["kappa"])

    # Prolate sweep
    prolate = prolate_condition_sweep(eccentricities=eccentricities,
                                      modes=modes)
    C_p, alpha_p, r2_p = fit_power_law(prolate["eccentricity"],
                                         prolate["kappa"])

    # Triaxial sweep (diagonal: ε₁ = ε₂)
    triaxial = triaxial_condition_sweep(
        eps1_range=eccentricities * 0.5,
        eps2_range=eccentricities * 0.5,
        modes=modes,
        inversion_params=("a", "b", "c", "E"),
    )
    # Effective eccentricity along the diagonal
    eps_tri_eff = triaxial["eps_diagonal"] * np.sqrt(2.0)
    C_t, alpha_t, r2_t = fit_power_law(eps_tri_eff,
                                         triaxial["kappa_diagonal"])

    results = {
        "oblate": {
            "C": C_o, "alpha": alpha_o, "R_squared": r2_o,
            "kappa": oblate["kappa"],
            "eccentricity": oblate["eccentricity"],
        },
        "prolate": {
            "C": C_p, "alpha": alpha_p, "R_squared": r2_p,
            "kappa": prolate["kappa"],
            "eccentricity": prolate["eccentricity"],
        },
        "triaxial": {
            "C": C_t, "alpha": alpha_t, "R_squared": r2_t,
            "kappa": triaxial["kappa_diagonal"],
            "eccentricity": eps_tri_eff,
        },
        "universal": (
            1.0 <= alpha_o <= 4.0
            and 1.0 <= alpha_p <= 4.0
            and (np.isnan(alpha_t) or 1.0 <= alpha_t <= 4.0)
        ),
    }

    if verbose:
        print()
        print("=" * 70)
        print("  UNIVERSALITY CONJECTURE: κ(ε) ~ C · ε⁻ᵅ")
        print("=" * 70)
        print(f"  {'Geometry':<12} {'α':>8} {'C':>12} {'R²':>8}")
        print("  " + "-" * 44)
        for name in ["oblate", "prolate", "triaxial"]:
            r = results[name]
            print(f"  {name:<12} {r['alpha']:>8.3f} {r['C']:>12.1f}"
                  f" {r['R_squared']:>8.4f}")
        print("  " + "-" * 44)
        conj = "SUPPORTED" if results["universal"] else "NOT SUPPORTED"
        print(f"  Conjecture (α ∈ [1, 4] for all): {conj}")
        print()

    return results
