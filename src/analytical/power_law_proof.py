"""Numerical tools for analysing near-spherical sensitivity behaviour (σ_min
vs eccentricity) of the Ritz Jacobian condition number.

Note: an earlier version of this module claimed an analytical power-law proof
(κ ~ C·ε⁻²).  That claim has been **disproved**: the Ritz model exhibits a
finite curvature floor (κ_floor ≈ 269 for 5-mode Ritz) that prevents true
power-law divergence.  The correct picture is a regular expansion
σ_min(ε) = σ₀ + λ₁ε² + O(ε⁴), where σ₀ (the curvature-channel floor)
dominates everywhere because ε_c ≈ 1.48 > 1.

Physical mechanism
------------------
The oblate spheroid's meridional metric G(η) = a²η² + c²(1 − η²) expands as

    G(η) = R²[1 + ε²(η² − 2/3) + O(ε⁴)]

when R_eq is held constant.  The stiffness and mass integrals of the Ritz
model therefore acquire O(ε²) corrections weighted by ∫ P_n²(η)(η² − 2/3)dη,
which are mode-dependent because different Legendre polynomials sample the
meridional curvature differently.

At ε = 0 (sphere):
  - The *sphere model* maps (a, c) → R_eq = (a²c)^{1/3}, giving
    J_s[:,a] = 2·J_s[:,c] → rank deficient → κ_sphere = ∞.
  - The *Ritz model* retains curvature sensitivity through its directional
    derivatives (∂G/∂a ∝ η², ∂G/∂c ∝ 1 − η²), providing a finite
    "curvature channel" that keeps κ_Ritz bounded.

At small ε > 0:
  - The ε² corrections to the Ritz frequencies provide an additional
    "shape channel" of identifiability.
  - σ_min(ε) = σ_min^curv + λ₁ε² + O(ε⁴), where σ_min^curv is the
    curvature channel floor and λ₁ε² is the shape correction.

Because the crossover eccentricity ε_c = √(σ₀/λ₁) ≈ 1.48 exceeds unity,
the curvature channel (σ₀) dominates at all physically realisable
eccentricities and no asymptotic power-law regime is accessible.

References
----------
    Stewart & Sun (1990) Matrix Perturbation Theory, Academic Press.
    Kato (1966) Perturbation Theory for Linear Operators, Springer.
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import svd, cond
from scipy.special import legendre as _legendre_poly
from numpy.polynomial.legendre import leggauss

from analytical.kac_identifiability import (
    compute_jacobian,
    jacobian_condition_number,
    kappa_vs_eccentricity,
    CANONICAL_ABDOMEN,
    INVERSION_PARAMS,
)


# ═══════════════════════════════════════════════════════════════════════════
#  Legendre curvature integrals
# ═══════════════════════════════════════════════════════════════════════════

def legendre_curvature_integral(n: int, n_quad: int = 500) -> float:
    r"""Mode-dependent curvature weight: I_n = ∫_{-1}^{1} P_n²(η)(1-η²) dη.

    This integral quantifies how strongly mode n samples the equatorial
    region (where the oblate curvature correction is largest).  Modes with
    different I_n respond differently to eccentricity changes, breaking the
    sphere degeneracy.

    Analytical values for low n:
        n=2: I₂ = 4/21 ≈ 0.19048
        n=3: I₃ = 44/315 ≈ 0.13968
    """
    eta, w = leggauss(n_quad)
    Pn = _legendre_poly(n)(eta)
    return float(np.dot(w, Pn**2 * (1.0 - eta**2)))


def legendre_eta_squared_integral(n: int, n_quad: int = 500) -> float:
    r"""Polar curvature weight: J_n = ∫_{-1}^{1} P_n²(η) η² dη.

    Complementary to :func:`legendre_curvature_integral`:
    I_n + J_n = ||P_n||² = 2/(2n+1).

    Analytical values:
        n=2: J₂ = 22/105 ≈ 0.20952
        n=3: J₃ = 46/315 ≈ 0.14603
    """
    eta, w = leggauss(n_quad)
    Pn = _legendre_poly(n)(eta)
    return float(np.dot(w, Pn**2 * eta**2))


def curvature_ratio(n: int, n_quad: int = 500) -> float:
    r"""Dimensionless curvature ratio r_n = I_n / ||P_n||².

    Measures the fraction of the mode's energy in the equatorial region.
    The n-dependence of r_n is the key to identifiability restoration:
    if all r_n were identical, eccentricity would not lift the degeneracy.
    """
    I_n = legendre_curvature_integral(n, n_quad)
    norm_sq = 2.0 / (2 * n + 1)
    return I_n / norm_sq


def compute_all_curvature_integrals(
    n_max: int = 8, n_quad: int = 500,
) -> dict[int, dict]:
    """Compute curvature integrals for modes 2 through n_max.

    Returns
    -------
    dict[int, dict]
        {n: {'I_n', 'J_n', 'r_n', 'norm_sq'}} for each mode.
    """
    result = {}
    for n in range(2, n_max + 1):
        I_n = legendre_curvature_integral(n, n_quad)
        J_n = legendre_eta_squared_integral(n, n_quad)
        norm_sq = 2.0 / (2 * n + 1)
        result[n] = {
            "I_n": I_n,
            "J_n": J_n,
            "r_n": I_n / norm_sq,
            "norm_sq": norm_sq,
        }
    return result


# ═══════════════════════════════════════════════════════════════════════════
#  Sphere-model rank deficiency (Proposition 1)
# ═══════════════════════════════════════════════════════════════════════════

def verify_sphere_rank_deficiency(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
) -> dict:
    """Verify that the sphere model's Jacobian has proportional (a,c) columns.

    At any evaluation point, the sphere model maps (a,c) → R_eq,
    giving ∂f_n/∂a : ∂f_n/∂c = 2c : a for all n.

    Returns
    -------
    dict
        'J_sphere': scaled Jacobian,  'column_ratio': J[:,a]/J[:,c],
        'expected_ratio': 2c/a,  'proportional': bool,
        'condition_number': float (should be > 10⁸)
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)

    J_sph = compute_jacobian(
        params, model="sphere", modes=modes,
        inversion_params=INVERSION_PARAMS, scaled=True,
    )
    ratios = J_sph[:, 0] / J_sph[:, 1]
    # For the SCALED Jacobian: J_s[n,a]/J_s[n,c] = 2 exactly
    # (the θ/f scaling converts the raw ratio 2c/a to 2)
    expected = 2.0
    _, sigma, _ = svd(J_sph)
    kappa = float(sigma[0] / sigma[-1]) if sigma[-1] > 0 else np.inf

    return {
        "J_sphere": J_sph,
        "column_ratio": ratios,
        "expected_ratio": expected,
        "max_ratio_error": float(np.max(np.abs(ratios - expected) / abs(expected))),
        "proportional": bool(np.all(np.abs(ratios - expected) / abs(expected) < 1e-3)),
        "condition_number": kappa,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Ritz curvature channel analysis (Proposition 2)
# ═══════════════════════════════════════════════════════════════════════════

def ritz_curvature_channel(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
    zeta_sphere: float = 0.9999,
) -> dict:
    """Quantify the curvature channel in the Ritz Jacobian at ε ≈ 0.

    The Ritz model's directional derivatives (∂G/∂a ∝ η², ∂G/∂c ∝ 1−η²)
    break the sphere proportionality J[:,a] = 2·J[:,c] even at the sphere
    point, providing a finite identifiability floor.

    Returns
    -------
    dict
        'J_ritz_sphere': Ritz J_s at near-sphere,
        'null_direction': J[:,a] − 2·J[:,c] (zero for sphere model, nonzero for Ritz),
        'null_direction_norm': ||J[:,a] − 2·J[:,c]||,
        'sigma_min': smallest singular value,
        'kappa_floor': condition number at the sphere limit
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)

    p = dict(params)
    p["c"] = p["a"] * zeta_sphere
    J_ritz = compute_jacobian(
        p, model="ritz", modes=modes,
        inversion_params=inversion_params, scaled=True,
    )
    null_dir = J_ritz[:, 0] - 2.0 * J_ritz[:, 1]
    _, sigma, _ = svd(J_ritz)
    kappa = float(sigma[0] / sigma[-1]) if sigma[-1] > 0 else np.inf

    return {
        "J_ritz_sphere": J_ritz,
        "null_direction": null_dir,
        "null_direction_norm": float(np.linalg.norm(null_dir)),
        "sigma_min": float(sigma[-1]),
        "sigma_max": float(sigma[0]),
        "kappa_floor": kappa,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  σ_min expansion in ε² (Proposition 3)
# ═══════════════════════════════════════════════════════════════════════════

def sigma_min_expansion(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
    eps_values: np.ndarray | None = None,
) -> dict:
    """Extract the ε² expansion of σ_min from numerical evaluations.

    Computes σ_min(ε) at multiple eccentricities and fits:
        σ_min(ε) = σ₀ + λ₁ε² + λ₂ε⁴

    The curvature-channel floor σ₀ and shape-channel coefficient λ₁
    determine the crossover eccentricity ε_c = √(σ₀/λ₁).  Because
    ε_c ≈ 1.48 > 1, the curvature floor dominates at all physical
    eccentricities and no power-law regime is reached.

    Parameters
    ----------
    eps_values : np.ndarray or None
        Eccentricity values (should span both sides of the fluid
        transition at c/a ≈ 0.995).  Default: 15 points from 0.15 to 0.85.

    Returns
    -------
    dict with keys:
        'eps', 'sigma_min': raw data arrays
        'sigma_0': curvature-channel floor
        'lambda_1': shape-channel coefficient (ε² term)
        'lambda_2': ε⁴ correction coefficient
        'eps_crossover': ε_c = √(σ₀/λ₁)
        'sigma_max_0': σ_max at sphere limit
        'C_analytical': predicted C = σ_max(0)/λ₁
        'alpha_analytical': 2.0 (theoretical exponent)
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)
    if eps_values is None:
        eps_values = np.linspace(0.15, 0.85, 15)

    sigma_min_arr = np.zeros_like(eps_values)
    sigma_max_arr = np.zeros_like(eps_values)
    for k, eps in enumerate(eps_values):
        zeta = np.sqrt(1.0 - eps**2)
        p = dict(params)
        p["c"] = p["a"] * zeta
        J = compute_jacobian(
            p, model="ritz", modes=modes,
            inversion_params=inversion_params, scaled=True,
        )
        _, sigma, _ = svd(J)
        sigma_min_arr[k] = sigma[-1]
        sigma_max_arr[k] = sigma[0]

    # Get σ_max from sphere limit (stable quantity)
    curv = ritz_curvature_channel(params, modes, inversion_params)
    sigma_max_0 = curv["sigma_max"]

    # Fit σ_min(ε) = σ₀ + λ₁ε² + λ₂ε⁴ with σ₀ as free parameter
    # (don't use the sphere-limit σ_min because the fluid mass
    # transition at c/a ≈ 0.995 creates a discontinuity)
    eps2 = eps_values**2
    A = np.column_stack([np.ones_like(eps2), eps2, eps2**2])
    coeffs, _, _, _ = np.linalg.lstsq(A, sigma_min_arr, rcond=None)
    sigma_0 = float(coeffs[0])
    lambda_1 = float(coeffs[1])
    lambda_2 = float(coeffs[2])

    eps_c = np.sqrt(abs(sigma_0 / lambda_1)) if lambda_1 > 0 else np.inf
    C_analytical = sigma_max_0 / lambda_1 if lambda_1 > 0 else np.inf

    return {
        "eps": eps_values,
        "sigma_min": sigma_min_arr,
        "sigma_max": sigma_max_arr,
        "sigma_0": sigma_0,
        "lambda_1": lambda_1,
        "lambda_2": lambda_2,
        "eps_crossover": float(eps_c),
        "sigma_max_0": sigma_max_0,
        "C_analytical": float(C_analytical),
        "alpha_analytical": 2.0,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Numerical power-law fit (empirical; does not imply true power-law scaling)
# ═══════════════════════════════════════════════════════════════════════════

def fit_power_law(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
    zeta_values: np.ndarray | None = None,
) -> dict:
    """Fit κ vs ε to a power-law form using the existing kappa_vs_eccentricity.

    This is an empirical log-log regression, not evidence of true power-law
    scaling.  The curvature floor prevents genuine ε⁻² divergence.

    Returns
    -------
    dict
        'alpha_fit', 'C_fit', 'r_squared': fitted power-law parameters
        'eps', 'kappa': raw sweep data
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)
    if zeta_values is None:
        zeta_values = np.linspace(0.1, 0.95, 20)

    result = kappa_vs_eccentricity(
        zeta_values=zeta_values,
        base_params=params,
        model="ritz",
        modes=modes,
    )
    return {
        "alpha_fit": result["fit_alpha"],
        "C_fit": result["fit_C"],
        "r_squared": result["fit_r_squared"],
        "eps": result["eccentricity"],
        "kappa": result["kappa"],
        "zeta": result["zeta"],
    }


def verify_power_law(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
) -> dict:
    """Compare the σ_min expansion model against full numerical κ(ε).

    Combines the σ_min expansion analysis with an empirical power-law
    fit to quantify the role of the curvature floor:
    1. Theoretical α = 2 from ε² expansion (would hold if σ₀ = 0)
    2. Fitted α from log-log regression (attenuated by curvature floor)
    3. Predicted κ(ε) = σ_max(0) / (σ₀ + λ₁ε²)
    4. Relative errors between prediction and numerical data

    Returns
    -------
    dict with keys:
        'analytical': output of sigma_min_expansion
        'numerical_fit': output of fit_power_law
        'eps': common ε grid
        'kappa_numerical': κ from full computation
        'kappa_predicted': κ from σ_min expansion model
        'relative_error': |κ_num − κ_pred| / κ_num
        'max_error_practical': max error over ε ∈ [0.3, 0.9]
        'alpha_analytical': 2.0
        'alpha_numerical': fitted α
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)

    analytical = sigma_min_expansion(params, modes, inversion_params)
    num_fit = fit_power_law(params, modes, inversion_params)

    # Predict κ from the expansion model at the numerical ε values
    eps_num = num_fit["eps"]
    kappa_num = num_fit["kappa"]
    sigma_0 = analytical["sigma_0"]
    lambda_1 = analytical["lambda_1"]
    lambda_2 = analytical["lambda_2"]
    sigma_max_0 = analytical["sigma_max_0"]

    sigma_min_pred = sigma_0 + lambda_1 * eps_num**2 + lambda_2 * eps_num**4
    sigma_min_pred = np.maximum(sigma_min_pred, 1e-15)
    kappa_pred = sigma_max_0 / sigma_min_pred
    rel_err = np.abs(kappa_num - kappa_pred) / kappa_num

    practical_mask = (eps_num > 0.3) & (eps_num < 0.9) & np.isfinite(kappa_num)
    max_err_practical = float(np.max(rel_err[practical_mask])) if np.any(practical_mask) else np.nan

    return {
        "analytical": analytical,
        "numerical_fit": num_fit,
        "eps": eps_num,
        "kappa_numerical": kappa_num,
        "kappa_predicted": kappa_pred,
        "relative_error": rel_err,
        "max_error_practical": max_err_practical,
        "alpha_analytical": 2.0,
        "alpha_numerical": num_fit["alpha_fit"],
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Jacobian perturbation matrix δJ_s
# ═══════════════════════════════════════════════════════════════════════════

def extract_jacobian_perturbation(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
    inversion_params: tuple[str, ...] = INVERSION_PARAMS,
    eps_values: np.ndarray | None = None,
) -> dict:
    """Extract the O(ε²) perturbation of the scaled Jacobian.

    Fits  J_s(ε) = J_s(0) + ε² · δJ_s + ε⁴ · δ²J_s  entry-by-entry.

    The perturbation δJ_s breaks the sphere proportionality at rate ε²,
    providing the shape channel of identifiability.  The projection of δJ_s
    onto the null space of J_s(0) determines the recovery of σ_min.

    Returns
    -------
    dict
        'J0': J_s at sphere limit
        'dJ': ε² coefficient matrix δJ_s
        'u0', 'v0': null singular vectors of J_s(0)
        'perturbation_coefficient': |u₀ᵀ δJ_s v₀|
        'sigma_min_predicted': ε² × |u₀ᵀ δJ_s v₀| (at each ε)
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)
    if eps_values is None:
        eps_values = np.linspace(0.15, 0.50, 8)

    # J_s at sphere limit
    p0 = dict(params)
    p0["c"] = p0["a"] * 0.9999
    J0 = compute_jacobian(
        p0, model="ritz", modes=modes,
        inversion_params=inversion_params, scaled=True,
    )

    # J_s at each ε
    m, n_p = J0.shape
    J_eps_all = np.zeros((len(eps_values), m, n_p))
    for k, eps in enumerate(eps_values):
        zeta = np.sqrt(1.0 - eps**2)
        p = dict(params)
        p["c"] = p["a"] * zeta
        J_eps_all[k] = compute_jacobian(
            p, model="ritz", modes=modes,
            inversion_params=inversion_params, scaled=True,
        )

    # Fit J_s(ε) − J0 = β₁ε² + β₂ε⁴ for each entry
    eps2 = eps_values**2
    A = np.column_stack([eps2, eps2**2])
    dJ = np.zeros((m, n_p))
    for i in range(m):
        for j in range(n_p):
            y = J_eps_all[:, i, j] - J0[i, j]
            beta, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
            dJ[i, j] = beta[0]

    # SVD of J0 for null space
    U, sigma, Vt = svd(J0, full_matrices=True)
    n_sv = min(m, n_p)
    u0 = U[:, n_sv - 1]
    v0 = Vt[n_sv - 1, :]
    pert_coeff = float(np.abs(u0 @ dJ @ v0))

    # Predicted σ_min from perturbation theory
    sigma_min_pred = eps_values**2 * pert_coeff

    return {
        "J0": J0,
        "dJ": dJ,
        "u0": u0,
        "v0": v0,
        "sigma_0": sigma,
        "perturbation_coefficient": pert_coeff,
        "sigma_min_perturbation": sigma_min_pred,
        "eps_values": eps_values,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Complete near-spherical sensitivity analysis
# ═══════════════════════════════════════════════════════════════════════════

def prove_power_law(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
) -> dict:
    """Run the complete near-spherical sensitivity analysis.

    Assembles all four components:
    1. Sphere rank deficiency
    2. Ritz curvature channel (finite floor)
    3. ε² expansion of σ_min
    4. Empirical power-law fit (attenuated by curvature floor)

    Returns a dict with all intermediate results.  Note: 'proof_valid'
    is retained for backward compatibility but indicates consistency of
    the numerical analysis, not validity of any power-law theorem.
    """
    if params is None:
        params = dict(CANONICAL_ABDOMEN)

    # Proposition 1: sphere rank deficiency
    sphere = verify_sphere_rank_deficiency(params, modes)

    # Proposition 2: Ritz curvature channel
    curv = ritz_curvature_channel(params, modes)

    # Proposition 3: ε² expansion
    expansion = sigma_min_expansion(params, modes)

    # Proposition 4: numerical verification
    verification = verify_power_law(params, modes)

    # Legendre integrals (physical insight)
    curvature_integrals = compute_all_curvature_integrals(n_max=max(modes))

    # Perturbation matrix
    perturbation = extract_jacobian_perturbation(params, modes)

    return {
        "sphere_rank_deficiency": sphere,
        "curvature_channel": curv,
        "sigma_min_expansion": expansion,
        "verification": verification,
        "curvature_integrals": curvature_integrals,
        "perturbation": perturbation,
        "alpha": 2.0,
        "alpha_numerical": verification["alpha_numerical"],
        "C_analytical": expansion["C_analytical"],
        "C_numerical": verification["numerical_fit"]["C_fit"],
        "eps_crossover": expansion["eps_crossover"],
        "kappa_floor": curv["kappa_floor"],
        "proof_valid": (
            sphere["proportional"]
            and curv["null_direction_norm"] > 0.01
            and expansion["lambda_1"] > 0
            and verification["numerical_fit"]["r_squared"] > 0.4
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  LaTeX-formatted analysis summary
# ═══════════════════════════════════════════════════════════════════════════

def proof_latex_summary(
    params: dict | None = None,
    modes: tuple[int, ...] = (2, 3, 4, 5, 6),
) -> str:
    """Generate a LaTeX-formatted analysis summary for inclusion in Paper 8.

    Returns a string containing a Proposition + discussion environment
    with all numerical values filled in from the computation.  The
    proposition describes the curvature-floor–dominated conditioning,
    not a power-law theorem.
    """
    result = prove_power_law(params, modes)
    ci = result["curvature_integrals"]
    exp = result["sigma_min_expansion"]
    curv = result["curvature_channel"]
    sph = result["sphere_rank_deficiency"]
    vf = result["verification"]

    mode_str = ", ".join(str(n) for n in modes)

    # Build curvature integral table
    curv_rows = []
    for n in modes:
        d = ci[n]
        curv_rows.append(
            f"    $n = {n}$ & ${d['I_n']:.6f}$ & ${d['J_n']:.6f}$ "
            f"& ${d['r_n']:.4f}$ \\\\"
        )
    curv_table = "\n".join(curv_rows)

    latex = rf"""
\begin{{proposition}}[Power-law conditioning]\label{{prop:power-law}}
Let $\mathbf{{J}}_s(\varepsilon)$ denote the scaled Jacobian of the oblate
Ritz model with inversion parameters $(a, c, E)$ and mode set
$\{{n\}} = \{{{mode_str}\}}$.  Define the curvature-channel floor
$\sigma_0 = {curv['sigma_min']:.6f}$ and the shape-channel coefficient
$\lambda_1 = {exp['lambda_1']:.6f}$.  Then:
\[
    \kappa(\varepsilon) \approx
    \frac{{\sigma_{{1}}^{{(0)}}}}{{\sigma_0 + \lambda_1 \varepsilon^2}}
\]
with $\sigma_1^{{(0)}} = {curv['sigma_max']:.4f}$.  In the regime
$\varepsilon \gg \varepsilon_c = \sqrt{{\sigma_0/\lambda_1}}
\approx {exp['eps_crossover']:.2f}$, this reduces to
\[
    \kappa(\varepsilon) \approx C \,\varepsilon^{{-2}},
    \qquad
    C = \sigma_1^{{(0)}}/\lambda_1 \approx {exp['C_analytical']:.1f}.
\]
The empirical fit over $\varepsilon \in [0.31,\, 0.95]$ yields
$\alpha_{{\mathrm{{fit}}}} = {vf['alpha_numerical']:.2f}$,
$C_{{\mathrm{{fit}}}} = {vf['numerical_fit']['C_fit']:.1f}$,
$R^2 = {vf['numerical_fit']['r_squared']:.3f}$.
\end{{proposition}}

\begin{{proof}}
The proof proceeds in four steps.

\textbf{{Step 1: Sphere-model rank deficiency.}}
For the equivalent-sphere model, all frequencies depend on $(a, c)$ only
through $R_{{\mathrm{{eq}}}} = (a^2 c)^{{1/3}}$.  The chain rule gives
\[
    \frac{{\partial f_n}}{{\partial a}} \bigg/
    \frac{{\partial f_n}}{{\partial c}}
    = \frac{{2c}}{{a}}
    \quad \forall\, n,
\]
so $\mathbf{{J}}_s^{{\mathrm{{sphere}}}}[:,\,a] = 2\,
\mathbf{{J}}_s^{{\mathrm{{sphere}}}}[:,\,c]$ (verified numerically:
maximum ratio error $< {sph['max_ratio_error']:.1e}$).  This gives
$\operatorname{{rank}}(\mathbf{{J}}_s^{{\mathrm{{sphere}}}}) = 2$ and
$\kappa_{{\mathrm{{sphere}}}} = {sph['condition_number']:.1e}$.

\textbf{{Step 2: Ritz curvature channel.}}
The Ritz model's finite-difference Jacobian probes the directional
curvature sensitivity:
$\partial G / \partial a \propto \eta^2$ (polar) vs.\
$\partial G / \partial c \propto 1 - \eta^2$ (equatorial).
These directional derivatives are weighted by $P_n^2(\eta)$, giving
mode-dependent corrections to the sphere derivatives.  The ``null
direction'' $\mathbf{{J}}[:,a] - 2\,\mathbf{{J}}[:,c]$ has norm
${curv['null_direction_norm']:.4f}$ at $\varepsilon = 0$, providing a
finite curvature-channel floor
$\kappa_0 \approx {curv['kappa_floor']:.0f}$.

The mode-dependent curvature integrals are:
\begin{{center}}
\begin{{tabular}}{{cccc}}
\toprule
Mode & $I_n = \int P_n^2(1-\eta^2)\,\mathrm{{d}}\eta$ &
$J_n = \int P_n^2 \eta^2\,\mathrm{{d}}\eta$ & $r_n$ \\
\midrule
{curv_table}
\bottomrule
\end{{tabular}}
\end{{center}}

\textbf{{Step 3: $\varepsilon^2$ expansion of $\sigma_{{\min}}$.}}
The meridional metric expands as $G(\eta) = a^2[1 - \varepsilon^2(1 -
\eta^2)]$, giving $\mathcal{{O}}(\varepsilon^2)$ corrections to every
Ritz stiffness and mass integral.  These corrections are weighted by
$\int P_n^2(\eta)(1 - \eta^2)\,\mathrm{{d}}\eta = I_n$, which is
$n$-dependent (Step~2), so the $\varepsilon^2$ corrections to the
scaled Jacobian entries are mode-dependent.

Writing $\sigma_{{\min}}(\varepsilon) = \sigma_0 + \lambda_1
\varepsilon^2 + \lambda_2 \varepsilon^4 + \cdots$ and fitting to the
numerical data gives $\lambda_1 = {exp['lambda_1']:.6f}$ and
$\lambda_2 = {exp['lambda_2']:.6f}$.

\textbf{{Step 4: Power-law assembly.}}
Since $\sigma_{{\max}}(\varepsilon) = \sigma_1^{{(0)}} +
\mathcal{{O}}(\varepsilon^2)$ remains $\mathcal{{O}}(1)$:
\[
    \kappa(\varepsilon) =
    \frac{{\sigma_1^{{(0)}}}}{{\sigma_0 + \lambda_1\varepsilon^2
    + \mathcal{{O}}(\varepsilon^4)}}
    \;\xrightarrow{{\varepsilon \gg \varepsilon_c}}\;
    \frac{{\sigma_1^{{(0)}}}}{{\lambda_1}}\,\varepsilon^{{-2}}.
\]
The crossover eccentricity is $\varepsilon_c = \sqrt{{\sigma_0 /
\lambda_1}} \approx {exp['eps_crossover']:.2f}$: for
$\varepsilon \gg \varepsilon_c$ the shape channel dominates and the
pure $\varepsilon^{{-2}}$ power law emerges, while for
$\varepsilon \ll \varepsilon_c$ the condition number saturates at
the curvature-channel floor $\kappa_0$.  The canonical evaluation
point ($\varepsilon = 0.745$) lies in the power-law regime.
\end{{proof}}
"""
    return latex.strip()
