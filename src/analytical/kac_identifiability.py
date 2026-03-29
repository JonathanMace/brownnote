"""Practical identifiability of viscoelastic shell parameters from resonant
frequencies — the inverse Kac problem for oblate spheroidal organs.

Paper 8: "Can You Hear the Shape of an Organ?"

Given measured resonant frequencies (f₂, f₃, f₄, ...), can we uniquely recover
the physical parameters (a, c, E)?  This module answers the question by
computing Jacobians, condition numbers, Fisher information matrices, and
Cramér–Rao bounds for both the equivalent-sphere and Ritz oblate-spheroid
forward models.

Key result: the sphere model is rank-deficient (all modes scale identically
with geometry), while the oblate Ritz model has full-rank Jacobian because
different modes sample curvature differently.
"""

from __future__ import annotations

import warnings

import numpy as np
from numpy.linalg import cond, inv, svd
from scipy.optimize import least_squares

from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)
from analytical.oblate_spheroid_ritz import (
    oblate_ritz_frequencies,
    sphere_approx_frequencies,
)


# ═══════════════════════════════════════════════════════════════════════════
#  Default canonical parameters
# ═══════════════════════════════════════════════════════════════════════════

CANONICAL_ABDOMEN = dict(
    a=0.18, c=0.12, h=0.010, E=0.1e6, nu=0.45,
    rho_w=1100.0, rho_f=1020.0, K_f=2.2e9, P_iap=1000.0,
    loss_tangent=0.25,
)

# Parameters we invert for (the identifiable triple)
INVERSION_PARAMS = ("a", "c", "E")

# Default modes used for inversion — 5+ modes recommended for robust
# global inversion.  With only 3 modes the problem is exactly determined
# and spurious zero-residual solutions can exist for poor initial guesses.
DEFAULT_MODES = (2, 3, 4, 5, 6)


# ═══════════════════════════════════════════════════════════════════════════
#  Forward model wrappers
# ═══════════════════════════════════════════════════════════════════════════

def _forward_ritz(params: dict, modes: tuple[int, ...] = DEFAULT_MODES) -> np.ndarray:
    """Compute flexural frequencies using the oblate Ritz model.

    Parameters
    ----------
    params : dict
        Must contain at least: a, c, h, E, nu, rho_w, rho_f, P_iap.
    modes : tuple of int
        Mode numbers to compute (default: 2, 3, 4).

    Returns
    -------
    np.ndarray
        Frequencies in Hz, one per requested mode.
    """
    freq_dict = oblate_ritz_frequencies(
        a=params["a"], c=params["c"], h=params["h"],
        E=params["E"], nu=params["nu"],
        rho_w=params["rho_w"], rho_f=params["rho_f"],
        P_iap=params["P_iap"], n_target=modes,
    )
    return np.array([freq_dict[n] for n in modes])


def _forward_sphere(params: dict, modes: tuple[int, ...] = DEFAULT_MODES) -> np.ndarray:
    """Compute flexural frequencies using the equivalent-sphere model.

    Parameters
    ----------
    params : dict
        Must contain at least: a, c, h, E, nu, rho_w (as rho_wall),
        rho_f (as rho_fluid), K_f (as K_fluid), P_iap, loss_tangent.
    modes : tuple of int
        Mode numbers to compute (default: 2, 3, 4).

    Returns
    -------
    np.ndarray
        Frequencies in Hz, one per requested mode.
    """
    model = AbdominalModelV2(
        a=params["a"], b=params["a"], c=params["c"],
        h=params["h"], E=params["E"], nu=params["nu"],
        rho_wall=params["rho_w"], rho_fluid=params["rho_f"],
        K_fluid=params.get("K_f", 2.2e9),
        P_iap=params["P_iap"],
        loss_tangent=params.get("loss_tangent", 0.25),
    )
    freq_dict = sphere_approx_frequencies(model, n_modes=modes)
    return np.array([freq_dict[n] for n in modes])


def _get_forward(model: str):
    """Return the appropriate forward function for *model*."""
    if model == "ritz":
        return _forward_ritz
    elif model == "sphere":
        return _forward_sphere
    else:
        raise ValueError(f"Unknown model '{model}'. Use 'ritz' or 'sphere'.")


# ═══════════════════════════════════════════════════════════════════════════
#  Jacobian computation
# ═══════════════════════════════════════════════════════════════════════════

def compute_jacobian(
    params: dict,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
    step_fraction: float = 1e-6,
    scaled: bool = False,
) -> np.ndarray:
    """Numerical Jacobian of frequencies w.r.t. inversion parameters.

    Uses central finite differences for accuracy.

    Parameters
    ----------
    params : dict
        Full parameter set (must include all keys needed by the forward model).
    model : str
        ``'ritz'`` for the oblate spheroid Ritz model,
        ``'sphere'`` for the equivalent-sphere model.
    modes : tuple of int
        Which modal frequencies to include (rows of J).
    inversion_params : tuple of str
        Which parameters to differentiate w.r.t. (columns of J).
    step_fraction : float
        Relative perturbation size for finite differences.
    scaled : bool
        If True, return the dimensionless elasticity matrix
        ``J_s[i,j] = (∂f_i/∂θ_j) × (θ_j / f_i)`` instead of the raw
        Jacobian.  The scaled form removes unit-dependent conditioning and
        is the correct metric for identifiability analysis.

    Returns
    -------
    J : np.ndarray, shape (len(modes), len(inversion_params))
        Jacobian matrix.  Raw  J_{ij} = ∂f_i / ∂θ_j  when ``scaled=False``,
        or dimensionless sensitivity  (∂f_i/∂θ_j)(θ_j/f_i)  when
        ``scaled=True``.
    """
    forward = _get_forward(model)
    n_freq = len(modes)
    n_param = len(inversion_params)
    J = np.zeros((n_freq, n_param))

    for j, pname in enumerate(inversion_params):
        p0 = params[pname]
        dp = abs(p0) * step_fraction
        if dp == 0:
            dp = step_fraction  # fallback for zero-valued parameters

        params_plus = dict(params)
        params_plus[pname] = p0 + dp
        f_plus = forward(params_plus, modes)

        params_minus = dict(params)
        params_minus[pname] = p0 - dp
        f_minus = forward(params_minus, modes)

        J[:, j] = (f_plus - f_minus) / (2.0 * dp)

    if scaled:
        f_nom = forward(params, modes)
        theta = np.array([params[k] for k in inversion_params])
        J = J * theta[np.newaxis, :] / f_nom[:, np.newaxis]

    return J


# ═══════════════════════════════════════════════════════════════════════════
#  Condition number analysis
# ═══════════════════════════════════════════════════════════════════════════

def jacobian_condition_number(
    params: dict,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
) -> float:
    """Condition number of the **scaled** (dimensionless) Jacobian.

    The scaled Jacobian removes unit-dependent conditioning by normalising
    each entry:  J_s[i,j] = (∂f_i/∂θ_j)(θ_j/f_i).  A condition number
    near 1 means well-conditioned; > 10⁶ indicates non-identifiability.

    Parameters
    ----------
    params, model, modes, inversion_params
        As for :func:`compute_jacobian`.

    Returns
    -------
    float
        Condition number κ(J_scaled).
    """
    J = compute_jacobian(params, model, modes, inversion_params, scaled=True)
    return float(cond(J))


def condition_number_map(
    a_range: np.ndarray,
    c_range: np.ndarray,
    E_range: np.ndarray,
    base_params: dict | None = None,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
) -> np.ndarray:
    """Sweep condition number over a 3-D parameter grid.

    Parameters
    ----------
    a_range, c_range, E_range : np.ndarray
        1-D arrays of values to sweep for semi-major axis, semi-minor axis,
        and Young's modulus respectively.
    base_params : dict or None
        Baseline parameters; *a*, *c*, *E* are overridden during the sweep.
        Defaults to :data:`CANONICAL_ABDOMEN`.
    model : str
        ``'ritz'`` or ``'sphere'``.
    modes : tuple of int
        Mode numbers used for the Jacobian.

    Returns
    -------
    np.ndarray, shape (len(a_range), len(c_range), len(E_range))
        Condition numbers at each grid point.
    """
    if base_params is None:
        base_params = dict(CANONICAL_ABDOMEN)

    na, nc, nE = len(a_range), len(c_range), len(E_range)
    kappa = np.full((na, nc, nE), np.nan)

    for i, a in enumerate(a_range):
        for j, c in enumerate(c_range):
            for k, E in enumerate(E_range):
                p = dict(base_params)
                p["a"] = a
                p["c"] = c
                p["E"] = E
                try:
                    kappa[i, j, k] = jacobian_condition_number(
                        p, model=model, modes=modes
                    )
                except Exception:
                    kappa[i, j, k] = np.inf

    return kappa


# ═══════════════════════════════════════════════════════════════════════════
#  Newton–Raphson inverse solver
# ═══════════════════════════════════════════════════════════════════════════

# Physically motivated bounds for the inversion parameters.
# Independent of initial guess to avoid artificially restricted search.
_PARAM_BOUNDS = {
    "a": (0.05, 0.40),   # m  — covers small organs to large fruits
    "c": (0.03, 0.40),   # m
    "E": (1e3, 1e9),      # Pa — soft tissue to hard shell
}


def invert_frequencies(
    f_observed: np.ndarray | list[float],
    initial_guess: dict,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
    tol: float = 1e-10,
    max_iter: int = 200,
    validation_rtol: float = 1e-3,
) -> dict:
    """Recover physical parameters from observed resonant frequencies.

    Uses ``scipy.optimize.least_squares`` (trust-region reflective) to
    minimise the residual between observed and predicted frequencies.

    .. note::

       Using 5 or more modes is strongly recommended for robust global
       inversion.  With only 3 modes the system is exactly determined
       (3 equations, 3 unknowns) and spurious zero-residual solutions
       can exist, especially when the initial guess is far from the true
       values.  The default ``modes=(2, 3, 4, 5, 6)`` provides a healthy
       overdetermined system.

    .. warning::

       Sphere model inversion (``model='sphere'``) is ill-posed because
       the sphere Jacobian is rank-deficient — all modes scale identically
       with geometry, so multiple parameter combinations produce identical
       frequencies.  Results from sphere inversion should not be trusted.

    Parameters
    ----------
    f_observed : array-like, shape (len(modes),)
        Measured resonant frequencies [Hz].
    initial_guess : dict
        Starting parameter values.  Must contain keys for every entry in
        *inversion_params*.
    model : str
        ``'ritz'`` or ``'sphere'``.
    modes : tuple of int
        Mode numbers corresponding to the entries in *f_observed*.
    inversion_params : tuple of str
        Parameters to recover.
    tol : float
        Convergence tolerance on the cost function.
    max_iter : int
        Maximum number of iterations.
    validation_rtol : float
        Relative tolerance for post-inversion validation (default 0.1 %).
        Recovered parameters are checked against this threshold.

    Returns
    -------
    dict with keys:
        ``'params'``
            dict of recovered parameter values.
        ``'residual_hz'``
            np.ndarray of frequency residuals [Hz].
        ``'cost_hz'``
            float, 0.5 × Σ(residual_hz²) — cost in raw Hz.
        ``'cost_normalized'``
            float, 0.5 × Σ((residual/f_obs)²) — the normalised cost
            that the optimiser actually minimised.
        ``'success'``
            bool, True only if the optimiser converged **and**
            post-inversion validation passes (residuals below
            *validation_rtol* and recovered parameters physically
            reasonable and within bounds).
        ``'n_iter'``
            Number of function evaluations.
    """
    f_obs = np.asarray(f_observed, dtype=float)
    forward = _get_forward(model)

    # Warn on sphere inversion
    if model == "sphere":
        warnings.warn(
            "Sphere model inversion is ill-posed: the sphere Jacobian is "
            "rank-deficient and multiple parameter combinations produce "
            "identical frequencies. Use model='ritz' for reliable inversion.",
            UserWarning,
            stacklevel=2,
        )

    # Warn if fewer than 4 modes
    if len(modes) < 4:
        warnings.warn(
            f"Only {len(modes)} modes requested for inversion of "
            f"{len(inversion_params)} parameters. With fewer than 4 modes "
            f"the system is (near-)exactly determined and spurious solutions "
            f"can exist. Use 5+ modes for robust inversion.",
            UserWarning,
            stacklevel=2,
        )

    # Build working parameter set
    working = dict(initial_guess)

    # Physically motivated bounds — independent of initial guess
    lower_raw = np.array([
        _PARAM_BOUNDS.get(k, (1e-12, np.inf))[0] for k in inversion_params
    ])
    upper_raw = np.array([
        _PARAM_BOUNDS.get(k, (1e-12, np.inf))[1] for k in inversion_params
    ])

    # Scale factors: optimise in normalised space x_s = x / x_scale
    x0_raw = np.array([working[k] for k in inversion_params])
    x_scale = x0_raw.copy()

    # Bounds in normalised space
    lower_norm = lower_raw / x_scale
    upper_norm = upper_raw / x_scale
    x0_norm = np.ones_like(x0_raw)  # starts at 1.0

    def residuals(x_norm):
        x_raw = x_norm * x_scale
        p = dict(working)
        for k, v in zip(inversion_params, x_raw):
            p[k] = v
        f_pred = forward(p, modes)
        return (f_pred - f_obs) / f_obs

    result = least_squares(
        residuals, x0_norm, bounds=(lower_norm, upper_norm),
        ftol=tol, xtol=tol, gtol=tol, max_nfev=max_iter * len(x0_raw),
    )

    x_final = result.x * x_scale
    recovered = dict(working)
    for k, v in zip(inversion_params, x_final):
        recovered[k] = float(v)

    # Compute residuals for reporting
    f_pred_final = forward(recovered, modes)
    residual_hz = f_pred_final - f_obs
    residual_norm = residual_hz / f_obs

    cost_hz = float(0.5 * np.sum(residual_hz**2))
    cost_normalized = float(0.5 * np.sum(residual_norm**2))

    # Post-inversion validation
    optimizer_ok = bool(result.success)
    residuals_ok = bool(np.all(np.abs(residual_norm) < validation_rtol))
    bounds_ok = True
    for k, v in zip(inversion_params, x_final):
        lo, hi = _PARAM_BOUNDS.get(k, (0.0, np.inf))
        if v <= 0 or v < lo or v > hi:
            bounds_ok = False
            break

    success = optimizer_ok and residuals_ok and bounds_ok

    return {
        "params": recovered,
        "residual_hz": residual_hz,
        "cost_hz": cost_hz,
        "cost_normalized": cost_normalized,
        "success": success,
        "n_iter": int(result.nfev),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Fisher information and Cramér–Rao bounds
# ═══════════════════════════════════════════════════════════════════════════

def identifiability_analysis(
    params: dict,
    noise_level: float = 0.01,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
) -> dict:
    """Fisher information matrix and Cramér–Rao lower bounds.

    Assumes additive Gaussian noise on each measured frequency with standard
    deviation  σ_i = noise_level × f_i  (i.e. *noise_level* is fractional).

    Parameters
    ----------
    params : dict
        Nominal parameter values.
    noise_level : float
        Fractional noise standard deviation (e.g. 0.01 = 1 %).
    model : str
        ``'ritz'`` or ``'sphere'``.
    modes, inversion_params
        As for :func:`compute_jacobian`.

    Returns
    -------
    dict with keys:
        ``'jacobian'``
            np.ndarray, the Jacobian matrix.
        ``'fisher_information'``
            np.ndarray, the Fisher information matrix  F = Jᵀ Σ⁻¹ J.
        ``'covariance'``
            np.ndarray, Cramér–Rao lower-bound covariance  F⁻¹.
        ``'cr_bounds'``
            dict mapping parameter name → minimum achievable std dev.
        ``'relative_cr_bounds'``
            dict mapping parameter name → minimum achievable fractional std dev.
        ``'condition_number'``
            float, condition number of J.
        ``'singular_values'``
            np.ndarray, singular values of J.
    """
    forward = _get_forward(model)
    f_nominal = forward(params, modes)

    # Raw Jacobian (for Fisher information — dimensional)
    J = compute_jacobian(params, model, modes, inversion_params)

    # Scaled Jacobian (for condition number — dimensionless)
    J_scaled = compute_jacobian(params, model, modes, inversion_params,
                                scaled=True)

    # Noise covariance: diagonal with σ_i = noise_level * f_i
    sigma = noise_level * f_nominal
    Sigma_inv = np.diag(1.0 / sigma**2)

    # Fisher information matrix
    F = J.T @ Sigma_inv @ J

    # Cramér–Rao bound: minimum covariance = F⁻¹
    try:
        cov = inv(F)
        # Guard against negative diagonal from near-singular inversion
        cr_abs = {}
        cr_rel = {}
        for i, k in enumerate(inversion_params):
            if cov[i, i] > 0:
                cr_abs[k] = np.sqrt(cov[i, i])
                cr_rel[k] = np.sqrt(cov[i, i]) / abs(params[k])
            else:
                cr_abs[k] = np.inf
                cr_rel[k] = np.inf
    except np.linalg.LinAlgError:
        # Singular Fisher matrix — parameters not identifiable
        n_p = len(inversion_params)
        cov = np.full((n_p, n_p), np.inf)
        cr_abs = {k: np.inf for k in inversion_params}
        cr_rel = {k: np.inf for k in inversion_params}

    U, s_scaled, Vt = svd(J_scaled)

    return {
        "jacobian": J,
        "jacobian_scaled": J_scaled,
        "fisher_information": F,
        "covariance": cov,
        "cr_bounds": cr_abs,
        "relative_cr_bounds": cr_rel,
        "condition_number": float(cond(J_scaled)),
        "singular_values": s_scaled,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Sphere vs oblate comparison
# ═══════════════════════════════════════════════════════════════════════════

def sphere_vs_oblate_comparison(
    params: dict | None = None,
    modes: tuple[int, ...] = DEFAULT_MODES,
    noise_level: float = 0.01,
) -> dict:
    """Direct comparison of identifiability for sphere vs oblate models.

    This is the headline result: the sphere Jacobian is rank-deficient while
    the oblate Ritz Jacobian has full rank.

    Parameters
    ----------
    params : dict or None
        Parameter set (defaults to canonical abdomen).
    modes : tuple of int
        Mode numbers to use.
    noise_level : float
        Fractional noise for Cramér–Rao analysis.

    Returns
    -------
    dict with keys ``'sphere'`` and ``'oblate'``, each containing the
    output of :func:`identifiability_analysis`, plus top-level summary:
        ``'sphere_condition'``
            Condition number for sphere model.
        ``'oblate_condition'``
            Condition number for oblate Ritz model.
        ``'improvement_factor'``
            Ratio sphere_condition / oblate_condition.
        ``'sphere_rank_deficient'``
            bool, True if sphere condition > 10⁶.
        ``'oblate_well_conditioned'``
            bool, True if oblate condition < 1000.
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)

    sphere_result = identifiability_analysis(
        params, noise_level=noise_level, model="sphere", modes=modes,
    )
    oblate_result = identifiability_analysis(
        params, noise_level=noise_level, model="ritz", modes=modes,
    )

    kappa_s = sphere_result["condition_number"]
    kappa_o = oblate_result["condition_number"]

    return {
        "sphere": sphere_result,
        "oblate": oblate_result,
        "sphere_condition": kappa_s,
        "oblate_condition": kappa_o,
        "improvement_factor": kappa_s / kappa_o if kappa_o > 0 else np.inf,
        "sphere_rank_deficient": kappa_s > 1e6,
        "oblate_well_conditioned": kappa_o < 1000,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Cross-model convenience helpers
# ═══════════════════════════════════════════════════════════════════════════

def condition_number_from_params(
    params_dict: dict,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
) -> float:
    """Compute Jacobian condition number from a parameter dict.

    This is a convenience wrapper around :func:`jacobian_condition_number`
    that accepts parameter dicts produced by external model helpers such as
    ``watermelon_canonical_params()``.  The dict keys are mapped
    automatically — for example, ``rho_rind`` → ``rho_w``,
    ``rho_flesh`` → ``rho_f``, etc.

    Parameters
    ----------
    params_dict : dict
        Parameter dictionary.  May use either the internal naming
        convention (``rho_w``, ``rho_f``, ``K_f``, ``P_iap``) or
        external naming (``rho_rind``, ``rho_flesh``, ``K_flesh``,
        ``P_int``).
    model : str
        ``'ritz'`` or ``'sphere'``.
    modes : tuple of int
        Mode numbers for the Jacobian.
    inversion_params : tuple of str
        Parameters to differentiate w.r.t.

    Returns
    -------
    float
        Condition number κ(J_scaled).
    """
    # Map external watermelon-style keys to internal names
    _KEY_MAP = {
        "rho_rind": "rho_w",
        "rho_flesh": "rho_f",
        "K_flesh": "K_f",
        "P_int": "P_iap",
    }
    p = {}
    for k, v in params_dict.items():
        p[_KEY_MAP.get(k, k)] = v

    return jacobian_condition_number(p, model=model, modes=modes,
                                     inversion_params=inversion_params)


# ═══════════════════════════════════════════════════════════════════════════
#  Analytical chain-rule proof helpers
# ═══════════════════════════════════════════════════════════════════════════

def equivalent_sphere_jacobian_ratio(a: float, c: float) -> float:
    """Analytical ratio (df_n/da) / (df_n/dc) for the equivalent-sphere model.

    By the chain rule through R_eq = (a^2 c)^{1/3}, this ratio equals 2c/a
    for ALL mode numbers n, proving that the Jacobian columns for a and c
    are proportional (Proposition 1 in the paper).

    Parameters
    ----------
    a : float
        Semi-major axis.
    c : float
        Semi-minor axis.

    Returns
    -------
    float
        The constant ratio 2c/a.
    """
    return 2.0 * c / a


def verify_sphere_jacobian_proportionality(
    params: dict,
    modes: tuple[int, ...] = DEFAULT_MODES,
    rtol: float = 1e-4,
) -> dict:
    """Numerically verify that sphere-model Jacobian columns are proportional.

    Computes the numerical Jacobian for the sphere model and checks that
    the ratio (df_n/da)/(df_n/dc) = 2c/a for every mode n.

    Parameters
    ----------
    params : dict
        Full parameter set.
    modes : tuple of int
        Mode numbers to check.
    rtol : float
        Relative tolerance for the proportionality check.

    Returns
    -------
    dict with keys:
        'analytical_ratio' : float
            The predicted ratio 2c/a.
        'numerical_ratios' : np.ndarray
            Ratio (df_n/da)/(df_n/dc) for each mode.
        'max_relative_error' : float
            Maximum relative deviation from the analytical ratio.
        'proportional' : bool
            True if all ratios match to within rtol.
    """
    J = compute_jacobian(params, model="sphere", modes=modes,
                         inversion_params=("a", "c"))
    ratios = J[:, 0] / J[:, 1]
    analytical = equivalent_sphere_jacobian_ratio(params["a"], params["c"])
    rel_errors = np.abs(ratios - analytical) / abs(analytical)

    return {
        "analytical_ratio": analytical,
        "numerical_ratios": ratios,
        "max_relative_error": float(np.max(rel_errors)),
        "proportional": bool(np.all(rel_errors < rtol)),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Eccentricity sweep — kappa vs epsilon analysis
# ═══════════════════════════════════════════════════════════════════════════

def kappa_vs_eccentricity(
    zeta_values: np.ndarray | None = None,
    base_params: dict | None = None,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
) -> dict:
    """Compute condition number kappa as a function of eccentricity epsilon.

    Sweeps the aspect ratio zeta = c/a from near-spherical to highly oblate,
    computing the scaled Jacobian condition number at each point.

    Parameters
    ----------
    zeta_values : np.ndarray or None
        Array of zeta = c/a values.  Defaults to 30 points from 0.01 to 0.99.
    base_params : dict or None
        Baseline parameters.  Defaults to CANONICAL_ABDOMEN.
        The value of c is overridden during the sweep; a is kept fixed.
    model : str
        'ritz' or 'sphere'.
    modes : tuple of int
        Mode numbers for the Jacobian.

    Returns
    -------
    dict with keys:
        'zeta' : np.ndarray
            Aspect ratio values c/a.
        'eccentricity' : np.ndarray
            Eccentricity epsilon = sqrt(1 - zeta^2).
        'kappa' : np.ndarray
            Condition numbers at each zeta.
        'fit_C' : float
            Fitted prefactor in kappa ~ C * epsilon^{-alpha}.
        'fit_alpha' : float
            Fitted exponent alpha.
        'fit_r_squared' : float
            R^2 of the log-linear fit.
    """
    if zeta_values is None:
        zeta_values = np.linspace(0.01, 0.99, 30)
    if base_params is None:
        base_params = dict(CANONICAL_ABDOMEN)

    a = base_params["a"]
    kappas = np.full_like(zeta_values, np.nan)

    for i, zeta in enumerate(zeta_values):
        p = dict(base_params)
        p["c"] = a * zeta
        try:
            kappas[i] = jacobian_condition_number(p, model=model, modes=modes)
        except Exception:
            kappas[i] = np.inf

    # Eccentricity
    eps = np.sqrt(1.0 - zeta_values**2)

    # Power-law fit: log(kappa) = log(C) - alpha * log(epsilon)
    valid = np.isfinite(kappas) & (eps > 0) & (kappas > 0)
    if np.sum(valid) >= 3:
        log_eps = np.log(eps[valid])
        log_kappa = np.log(kappas[valid])
        coeffs = np.polyfit(log_eps, log_kappa, 1)
        alpha = -coeffs[0]
        C = np.exp(coeffs[1])
        # R-squared
        ss_res = np.sum((log_kappa - np.polyval(coeffs, log_eps))**2)
        ss_tot = np.sum((log_kappa - np.mean(log_kappa))**2)
        r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    else:
        C, alpha, r_squared = np.nan, np.nan, 0.0

    return {
        "zeta": zeta_values,
        "eccentricity": eps,
        "kappa": kappas,
        "fit_C": float(C),
        "fit_alpha": float(alpha),
        "fit_r_squared": float(r_squared),
    }


def plot_kappa_vs_eccentricity(
    result: dict | None = None,
    output_path: str | None = None,
    **kwargs,
) -> None:
    """Generate publication-quality figure of kappa vs eccentricity.

    Parameters
    ----------
    result : dict or None
        Output of kappa_vs_eccentricity().  If None, computes it
        using default parameters and any extra **kwargs.
    output_path : str or None
        If given, saves the figure to this path (PDF recommended).
    **kwargs
        Passed to kappa_vs_eccentricity() if result is None.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if result is None:
        result = kappa_vs_eccentricity(**kwargs)

    eps = result["eccentricity"]
    kappa = result["kappa"]
    C = result["fit_C"]
    alpha = result["fit_alpha"]
    r2 = result["fit_r_squared"]

    valid = np.isfinite(kappa) & (kappa > 0)

    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.semilogy(eps[valid], kappa[valid], "o-", color="#2c3e50",
                markersize=5, linewidth=1.5, label="Ritz model")

    # Overlay fitted power law
    if np.isfinite(C) and np.isfinite(alpha):
        eps_fit = np.linspace(eps[valid].min(), eps[valid].max(), 200)
        kappa_fit = C * eps_fit**(-alpha)
        ax.semilogy(eps_fit, kappa_fit, "--", color="#e74c3c", linewidth=1.2,
                     label=(r"$\kappa \sim {:.1f}\,\varepsilon^{{-{:.2f}}}$"
                            r" ($R^2={:.3f}$)").format(C, alpha, r2))

    # Mark canonical operating point
    canonical_eps = np.sqrt(1.0 - (0.12 / 0.18)**2)
    canonical_kappa = result["kappa"][
        np.argmin(np.abs(result["eccentricity"] - canonical_eps))
    ]
    if np.isfinite(canonical_kappa):
        ax.plot(canonical_eps, canonical_kappa, "s", color="#27ae60",
                markersize=8, zorder=5,
                label=r"Canonical ($\zeta=0.667$)")

    ax.set_xlabel(r"Eccentricity $\varepsilon = \sqrt{1 - c^2/a^2}$",
                  fontsize=11)
    ax.set_ylabel(r"Condition number $\kappa(\mathbf{J}_s)$", fontsize=11)
    ax.legend(fontsize=9, loc="upper right")
    ax.set_xlim(0, 1.05)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()

    if output_path is not None:
        import os
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.close(fig)
