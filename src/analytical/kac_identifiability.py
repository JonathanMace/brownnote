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

# Default modes used for inversion
DEFAULT_MODES = (2, 3, 4)


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

def invert_frequencies(
    f_observed: np.ndarray | list[float],
    initial_guess: dict,
    model: str = "ritz",
    modes: tuple[int, ...] = DEFAULT_MODES,
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> dict:
    """Recover physical parameters from observed resonant frequencies.

    Uses ``scipy.optimize.least_squares`` (trust-region reflective) to
    minimise the residual between observed and predicted frequencies.

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

    Returns
    -------
    dict with keys:
        ``'params'``
            dict of recovered parameter values.
        ``'residual_hz'``
            np.ndarray of frequency residuals [Hz].
        ``'cost'``
            Final cost (sum of squared residuals).
        ``'success'``
            bool, whether the solver converged.
        ``'n_iter'``
            Number of function evaluations.
    """
    f_obs = np.asarray(f_observed, dtype=float)
    forward = _get_forward(model)

    # Build working parameter set
    working = dict(initial_guess)

    # Scale factors: optimise in normalised space x_s = x / x_scale
    x0_raw = np.array([working[k] for k in inversion_params])
    x_scale = x0_raw.copy()

    # Bounds in normalised space: all positive
    lower = np.full_like(x0_raw, 1e-6)
    upper = np.full_like(x0_raw, 100.0)
    x0_norm = np.ones_like(x0_raw)  # starts at 1.0

    def residuals(x_norm):
        x_raw = x_norm * x_scale
        p = dict(working)
        for k, v in zip(inversion_params, x_raw):
            p[k] = v
        f_pred = forward(p, modes)
        # Normalise residuals by observed frequencies for unit-free conditioning
        return (f_pred - f_obs) / f_obs

    result = least_squares(
        residuals, x0_norm, bounds=(lower, upper),
        ftol=tol, xtol=tol, gtol=tol, max_nfev=max_iter * len(x0_raw),
    )

    x_final = result.x * x_scale
    recovered = dict(working)
    for k, v in zip(inversion_params, x_final):
        recovered[k] = float(v)

    # Compute raw residuals in Hz for reporting
    f_pred_final = forward(recovered, modes)
    residual_hz = f_pred_final - f_obs

    return {
        "params": recovered,
        "residual_hz": residual_hz,
        "cost": float(0.5 * np.sum(residual_hz**2)),
        "success": bool(result.success),
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
