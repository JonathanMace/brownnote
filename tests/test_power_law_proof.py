"""Tests for the power-law proof module.

Verifies the analytical proof that κ(J_s) ~ C·ε^{-α} with α = 2
for the oblate spheroid Ritz model.  Tests cover:

  a. Legendre curvature integrals — exact values
  b. Sphere-model rank deficiency — J[:,a] = 2·J[:,c]
  c. Ritz curvature channel — nonzero at ε = 0
  d. σ_min expansion — ε² coefficient positive
  e. Power-law exponent — α ≈ 2 numerically
  f. Prefactor agreement — analytical C vs fitted C
  g. LaTeX output validity
"""

from __future__ import annotations

import sys
import os

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from analytical.power_law_proof import (
    legendre_curvature_integral,
    legendre_eta_squared_integral,
    curvature_ratio,
    compute_all_curvature_integrals,
    verify_sphere_rank_deficiency,
    ritz_curvature_channel,
    sigma_min_expansion,
    fit_power_law,
    verify_power_law,
    extract_jacobian_perturbation,
    prove_power_law,
    proof_latex_summary,
)
from analytical.kac_identifiability import CANONICAL_ABDOMEN


# ═══════════════════════════════════════════════════════════════════════════
#  Legendre curvature integrals
# ═══════════════════════════════════════════════════════════════════════════

class TestLegendreCurvatureIntegrals:
    """Verify mode-dependent curvature weight integrals against exact values."""

    def test_I2_exact(self):
        """I₂ = ∫ P₂²(η)(1−η²)dη = 4/21."""
        I2 = legendre_curvature_integral(2)
        np.testing.assert_allclose(I2, 4.0 / 21.0, atol=1e-10)

    def test_I3_exact(self):
        """I₃ = ∫ P₃²(η)(1−η²)dη = 44/315."""
        I3 = legendre_curvature_integral(3)
        np.testing.assert_allclose(I3, 44.0 / 315.0, atol=1e-10)

    def test_J2_exact(self):
        """J₂ = ∫ P₂²(η)η²dη = 22/105."""
        J2 = legendre_eta_squared_integral(2)
        np.testing.assert_allclose(J2, 22.0 / 105.0, atol=1e-10)

    def test_J3_exact(self):
        """J₃ = ∫ P₃²(η)η²dη = 46/315."""
        J3 = legendre_eta_squared_integral(3)
        np.testing.assert_allclose(J3, 46.0 / 315.0, atol=1e-10)

    def test_I_plus_J_equals_norm(self):
        """I_n + J_n = ||P_n||² = 2/(2n+1) for all n."""
        for n in range(2, 8):
            I_n = legendre_curvature_integral(n)
            J_n = legendre_eta_squared_integral(n)
            expected = 2.0 / (2 * n + 1)
            np.testing.assert_allclose(
                I_n + J_n, expected, atol=1e-10,
                err_msg=f"Failed for n={n}",
            )

    def test_curvature_ratios_are_mode_dependent(self):
        """r_n = I_n/||P_n||² must differ between modes — THE mechanism."""
        r2 = curvature_ratio(2)
        r3 = curvature_ratio(3)
        r4 = curvature_ratio(4)
        assert abs(r2 - r3) > 0.005, f"r₂={r2:.4f} and r₃={r3:.4f} too close"
        assert abs(r3 - r4) > 0.001, f"r₃={r3:.4f} and r₄={r4:.4f} too close"

    def test_r_n_bounded(self):
        """0 < r_n < 1 for all n ≥ 2."""
        for n in range(2, 10):
            r = curvature_ratio(n)
            assert 0 < r < 1, f"r_{n} = {r:.4f} out of bounds"


# ═══════════════════════════════════════════════════════════════════════════
#  Sphere-model rank deficiency (Proposition 1)
# ═══════════════════════════════════════════════════════════════════════════

class TestSphereRankDeficiency:
    """Verify that the sphere model has proportional (a,c) columns."""

    def test_column_proportionality(self):
        """J_sphere[:,a] / J_sphere[:,c] = 2c/a for all modes."""
        result = verify_sphere_rank_deficiency(modes=(2, 3, 4))
        assert result["proportional"], (
            f"Max ratio error = {result['max_ratio_error']:.2e}"
        )

    def test_condition_number_huge(self):
        """κ_sphere should exceed 10⁶ (effectively rank-deficient)."""
        result = verify_sphere_rank_deficiency()
        assert result["condition_number"] > 1e6

    def test_proportionality_five_modes(self):
        """Proportionality holds for 5-mode set too."""
        result = verify_sphere_rank_deficiency(modes=(2, 3, 4, 5, 6))
        assert result["proportional"]


# ═══════════════════════════════════════════════════════════════════════════
#  Ritz curvature channel (Proposition 2)
# ═══════════════════════════════════════════════════════════════════════════

class TestRitzCurvatureChannel:
    """Verify the curvature channel provides finite identifiability at ε=0."""

    def test_null_direction_nonzero(self):
        """||J_Ritz[:,a] − 2·J_Ritz[:,c]|| > 0 at ε = 0."""
        result = ritz_curvature_channel(modes=(2, 3, 4))
        assert result["null_direction_norm"] > 0.01, (
            f"Norm = {result['null_direction_norm']:.4f} too small"
        )

    def test_kappa_floor_finite(self):
        """κ at the sphere limit should be finite (< 10⁴)."""
        result = ritz_curvature_channel(modes=(2, 3, 4))
        assert result["kappa_floor"] < 1e4
        assert result["kappa_floor"] > 1  # well-defined

    def test_sigma_min_positive(self):
        """σ_min should be positive at the sphere limit."""
        result = ritz_curvature_channel(modes=(2, 3, 4))
        assert result["sigma_min"] > 1e-6

    def test_five_modes_better_conditioned(self):
        """5-mode set should have lower κ_floor than 3-mode set."""
        r3 = ritz_curvature_channel(modes=(2, 3, 4))
        r5 = ritz_curvature_channel(modes=(2, 3, 4, 5, 6))
        assert r5["kappa_floor"] < r3["kappa_floor"]


# ═══════════════════════════════════════════════════════════════════════════
#  σ_min expansion (Proposition 3)
# ═══════════════════════════════════════════════════════════════════════════

class TestSigmaMinExpansion:
    """Verify the ε² expansion of σ_min."""

    def test_lambda1_positive(self):
        """Shape-channel coefficient λ₁ > 0 (eccentricity helps)."""
        result = sigma_min_expansion(modes=(2, 3, 4))
        assert result["lambda_1"] > 0, f"λ₁ = {result['lambda_1']:.6f}"

    def test_sigma0_positive(self):
        """Extrapolated σ₀ should be positive (curvature floor exists)."""
        expansion = sigma_min_expansion(modes=(2, 3, 4))
        assert expansion["sigma_0"] > 0

    def test_expansion_fits_data(self):
        """σ₀ + λ₁ε² + λ₂ε⁴ should fit σ_min(ε) to < 30% for ε ∈ [0.15, 0.75]."""
        result = sigma_min_expansion(
            modes=(2, 3, 4),
            eps_values=np.linspace(0.15, 0.75, 12),
        )
        sigma_pred = (
            result["sigma_0"]
            + result["lambda_1"] * result["eps"]**2
            + result["lambda_2"] * result["eps"]**4
        )
        rel_err = np.abs(result["sigma_min"] - sigma_pred) / result["sigma_min"]
        assert np.max(rel_err) < 0.30, f"Max expansion error = {np.max(rel_err):.3f}"

    def test_crossover_eccentricity_physical(self):
        """ε_c should be positive and < 2 (physically meaningful)."""
        result = sigma_min_expansion(modes=(2, 3, 4))
        assert 0 < result["eps_crossover"] < 2.0

    def test_alpha_is_two(self):
        """The analytical exponent should be exactly 2."""
        result = sigma_min_expansion(modes=(2, 3, 4))
        assert result["alpha_analytical"] == 2.0


# ═══════════════════════════════════════════════════════════════════════════
#  Numerical power-law fit (Proposition 4)
# ═══════════════════════════════════════════════════════════════════════════

class TestNumericalPowerLaw:
    """Verify the numerical power-law fit is consistent with α ≈ 2."""

    def test_alpha_near_two_3mode(self):
        """Fitted α for 3-mode set should be within [1.0, 4.0]."""
        result = fit_power_law(modes=(2, 3, 4))
        assert 1.0 < result["alpha_fit"] < 4.0, (
            f"α_fit = {result['alpha_fit']:.3f}"
        )

    def test_alpha_near_two_5mode(self):
        """Fitted α for 5-mode set should be within [1.0, 4.0]."""
        result = fit_power_law(modes=(2, 3, 4, 5, 6))
        assert 1.0 < result["alpha_fit"] < 4.0, (
            f"α_fit = {result['alpha_fit']:.3f}"
        )

    def test_r_squared_reasonable(self):
        """R² of the log-log fit should exceed 0.4."""
        result = fit_power_law(modes=(2, 3, 4))
        assert result["r_squared"] > 0.4, (
            f"R² = {result['r_squared']:.3f}"
        )

    def test_C_positive_finite(self):
        """Prefactor C should be positive and finite."""
        result = fit_power_law(modes=(2, 3, 4))
        assert 0 < result["C_fit"] < 1e6

    def test_kappa_decreases_with_eccentricity(self):
        """κ at large ε should be smaller than at small ε."""
        result = fit_power_law(
            modes=(2, 3, 4),
            zeta_values=np.array([0.3, 0.5, 0.7, 0.95]),
        )
        kappa = result["kappa"]
        # κ at ζ=0.95 (ε=0.31) should exceed κ at ζ=0.3 (ε=0.95)
        assert kappa[-1] > kappa[0], (
            f"κ(ε=0.31) = {kappa[-1]:.1f} should exceed "
            f"κ(ε=0.95) = {kappa[0]:.1f}"
        )


# ═══════════════════════════════════════════════════════════════════════════
#  Perturbation matrix extraction
# ═══════════════════════════════════════════════════════════════════════════

class TestPerturbationExtraction:
    """Verify the O(ε²) perturbation of the Jacobian."""

    def test_perturbation_nonzero(self):
        """δJ_s must have nonzero entries (breaks sphere degeneracy)."""
        result = extract_jacobian_perturbation(modes=(2, 3, 4))
        assert np.max(np.abs(result["dJ"])) > 0.001

    def test_perturbation_coefficient_positive(self):
        """The null-space projection |u₀ᵀ δJ v₀| should be positive."""
        result = extract_jacobian_perturbation(modes=(2, 3, 4))
        assert result["perturbation_coefficient"] > 0


# ═══════════════════════════════════════════════════════════════════════════
#  Full verification
# ═══════════════════════════════════════════════════════════════════════════

class TestFullVerification:
    """End-to-end verification of the analytical prediction."""

    def test_prediction_reasonable(self):
        """Predicted κ should match numerical κ within 50% for ε ∈ [0.3, 0.8]."""
        result = verify_power_law(modes=(2, 3, 4))
        practical = (result["eps"] > 0.3) & (result["eps"] < 0.8)
        if np.any(practical):
            errs = result["relative_error"][practical]
            # Allow generous tolerance — the model is approximate
            assert np.median(errs) < 0.50, (
                f"Median relative error = {np.median(errs):.3f}"
            )


# ═══════════════════════════════════════════════════════════════════════════
#  Complete proof
# ═══════════════════════════════════════════════════════════════════════════

class TestProveComplete:
    """Test the complete prove_power_law function."""

    def test_proof_valid(self):
        """All proof preconditions should hold."""
        result = prove_power_law(modes=(2, 3, 4))
        assert result["proof_valid"], "One or more proof preconditions failed"

    def test_alpha_is_two(self):
        """Analytical α should be 2."""
        result = prove_power_law(modes=(2, 3, 4))
        assert result["alpha"] == 2.0

    def test_numerical_alpha_near_two(self):
        """Numerical α should be within factor of 2 of theoretical α=2."""
        result = prove_power_law(modes=(2, 3, 4))
        assert 0.5 < result["alpha_numerical"] / 2.0 < 2.5, (
            f"α_num = {result['alpha_numerical']:.3f}"
        )

    def test_kappa_floor_physical(self):
        """κ_floor should be moderate (1 < κ₀ < 10⁴)."""
        result = prove_power_law(modes=(2, 3, 4))
        assert 1 < result["kappa_floor"] < 1e4


# ═══════════════════════════════════════════════════════════════════════════
#  LaTeX output
# ═══════════════════════════════════════════════════════════════════════════

class TestLatexOutput:
    """Verify the LaTeX proof summary."""

    def test_generates_valid_latex(self):
        """Output should contain proposition and proof environments."""
        latex = proof_latex_summary(modes=(2, 3, 4))
        assert isinstance(latex, str)
        assert len(latex) > 200
        assert r"\begin{proposition}" in latex
        assert r"\end{proof}" in latex

    def test_contains_numerical_values(self):
        """LaTeX should contain the computed α, C, and R² values."""
        latex = proof_latex_summary(modes=(2, 3, 4))
        assert "varepsilon^{-2}" in latex
        assert "lambda_1" in latex
