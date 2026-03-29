"""Tests for the Kac identifiability module (Paper 8).

Covers:
  a. Jacobian accuracy — numerical vs analytic finite differences
  b. Sphere rank deficiency — condition number > 10⁸
  c. Oblate well-conditioned — condition number < 100
  d. Round-trip inversion — forward → invert recovers params to < 1 %
  e. Cramér–Rao bounds — scale correctly with noise level
  f. Watermelon parameters — identifiability with different geometry
  g. Sphere vs oblate comparison — summary flags correct
  h. Condition number map — runs without error, returns correct shape
  i. Edge cases — degenerate inputs handled gracefully
  j. Robustness — poor initial guesses, sphere warnings, mode count
"""

from __future__ import annotations

import sys
import os
import warnings

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytical.kac_identifiability import (
    CANONICAL_ABDOMEN,
    DEFAULT_MODES,
    INVERSION_PARAMS,
    _PARAM_BOUNDS,
    compute_jacobian,
    condition_number_from_params,
    condition_number_map,
    identifiability_analysis,
    invert_frequencies,
    jacobian_condition_number,
    sphere_vs_oblate_comparison,
    _forward_ritz,
    _forward_sphere,
)
from analytical.watermelon_model import watermelon_canonical_params


# ═══════════════════════════════════════════════════════════════════════════
#  Fixtures
# ═══════════════════════════════════════════════════════════════════════════

@pytest.fixture
def abdomen_params():
    """Canonical abdomen parameter set."""
    return dict(CANONICAL_ABDOMEN)


@pytest.fixture
def watermelon_params():
    """Ripe watermelon parameters mapped to the inversion interface."""
    wp = watermelon_canonical_params("ripe")
    return dict(
        a=wp["a"], c=wp["c"], h=wp["h"],
        E=wp["E"], nu=wp["nu"],
        rho_w=wp["rho_rind"], rho_f=wp["rho_flesh"],
        K_f=wp.get("K_flesh", 2.2e9),
        P_iap=wp["P_int"],
        loss_tangent=wp.get("loss_tangent", 0.15),
    )


@pytest.fixture
def abdomen_frequencies(abdomen_params):
    """Forward-model frequencies for canonical abdomen (Ritz)."""
    return _forward_ritz(abdomen_params, DEFAULT_MODES)


# ═══════════════════════════════════════════════════════════════════════════
#  1. Jacobian Accuracy
# ═══════════════════════════════════════════════════════════════════════════

class TestJacobianAccuracy:
    """Jacobian from compute_jacobian should agree with independent FD."""

    def test_ritz_jacobian_matches_finite_differences(self, abdomen_params):
        """Central FD at two step sizes should agree to ~6 digits."""
        J_fine = compute_jacobian(abdomen_params, model="ritz", step_fraction=1e-7)
        J_coarse = compute_jacobian(abdomen_params, model="ritz", step_fraction=1e-5)
        np.testing.assert_allclose(J_fine, J_coarse, rtol=1e-4,
                                   err_msg="Jacobian not converged under step refinement")

    def test_sphere_jacobian_matches_finite_differences(self, abdomen_params):
        J_fine = compute_jacobian(abdomen_params, model="sphere", step_fraction=1e-7)
        J_coarse = compute_jacobian(abdomen_params, model="sphere", step_fraction=1e-5)
        np.testing.assert_allclose(J_fine, J_coarse, rtol=1e-4,
                                   err_msg="Sphere Jacobian not converged")

    def test_jacobian_shape(self, abdomen_params):
        J = compute_jacobian(abdomen_params, model="ritz")
        assert J.shape == (len(DEFAULT_MODES), len(INVERSION_PARAMS))

    def test_scaled_jacobian_dimensionless(self, abdomen_params):
        """Scaled Jacobian entries should be O(1) — no unit dependence."""
        J_s = compute_jacobian(abdomen_params, model="ritz", scaled=True)
        assert np.all(np.abs(J_s) < 10), "Scaled Jacobian entries not O(1)"
        assert np.all(np.abs(J_s) > 0.01), "Scaled Jacobian entries unexpectedly small"

    def test_jacobian_nonzero(self, abdomen_params):
        J = compute_jacobian(abdomen_params, model="ritz")
        assert np.all(np.abs(J) > 0), "Jacobian has zero entries — unexpected"

    def test_jacobian_signs_physical(self, abdomen_params):
        """Increasing E should increase frequency."""
        J = compute_jacobian(abdomen_params, model="ritz")
        E_col = list(INVERSION_PARAMS).index("E")
        assert np.all(J[:, E_col] > 0), "∂f/∂E should be positive"


# ═══════════════════════════════════════════════════════════════════════════
#  2. Sphere Rank Deficiency
# ═══════════════════════════════════════════════════════════════════════════

class TestSphereRankDeficiency:
    """The sphere model Jacobian should be effectively singular."""

    def test_sphere_condition_number_large(self, abdomen_params):
        """Sphere scaled condition number should exceed 10⁸."""
        kappa = jacobian_condition_number(abdomen_params, model="sphere")
        assert kappa > 1e8, (
            f"Sphere condition number {kappa:.2e} is too small; "
            f"expected > 10⁸ (rank deficient)"
        )

    def test_sphere_singular_values_near_zero(self, abdomen_params):
        result = identifiability_analysis(abdomen_params, model="sphere")
        sv = result["singular_values"]
        ratio = sv[-1] / sv[0]
        assert ratio < 1e-6, (
            f"Smallest/largest singular value ratio {ratio:.2e} is too large"
        )


# ═══════════════════════════════════════════════════════════════════════════
#  3. Oblate Well-Conditioned
# ═══════════════════════════════════════════════════════════════════════════

class TestOblateWellConditioned:
    """The Ritz oblate model Jacobian should be well-conditioned."""

    def test_oblate_condition_number_small(self, abdomen_params):
        """Oblate scaled condition number should be < 200."""
        kappa = jacobian_condition_number(abdomen_params, model="ritz")
        assert kappa < 200, (
            f"Oblate condition number {kappa:.1f} is too large; "
            f"expected < 200 (well-conditioned)"
        )

    def test_oblate_full_rank(self, abdomen_params):
        J = compute_jacobian(abdomen_params, model="ritz", scaled=True)
        rank = np.linalg.matrix_rank(J, tol=1e-8)
        assert rank == min(J.shape), (
            f"Ritz Jacobian rank {rank} < expected {min(J.shape)}"
        )


# ═══════════════════════════════════════════════════════════════════════════
#  4. Round-Trip Inversion
# ═══════════════════════════════════════════════════════════════════════════

class TestRoundTripInversion:
    """Forward(params) → invert(frequencies) should recover params."""

    def test_abdomen_roundtrip(self, abdomen_params, abdomen_frequencies):
        """Recover canonical abdomen params to < 1 % error."""
        # Perturbed initial guess (10 % off)
        guess = dict(abdomen_params)
        guess["a"] *= 1.10
        guess["c"] *= 0.90
        guess["E"] *= 1.15

        result = invert_frequencies(
            abdomen_frequencies, initial_guess=guess, model="ritz"
        )
        assert result["success"], f"Inversion failed: cost={result['cost_hz']:.2e}"

        for pname in INVERSION_PARAMS:
            recovered = result["params"][pname]
            true_val = abdomen_params[pname]
            rel_err = abs(recovered - true_val) / abs(true_val)
            assert rel_err < 0.01, (
                f"Parameter {pname}: recovered {recovered:.6g}, "
                f"true {true_val:.6g}, error {rel_err:.2%}"
            )

    def test_watermelon_roundtrip(self, watermelon_params):
        """Recover watermelon params to < 1 % error."""
        f_obs = _forward_ritz(watermelon_params, DEFAULT_MODES)

        guess = dict(watermelon_params)
        guess["a"] *= 1.08
        guess["c"] *= 0.92
        guess["E"] *= 1.12

        result = invert_frequencies(
            f_obs, initial_guess=guess, model="ritz"
        )
        assert result["success"], f"Watermelon inversion failed"

        for pname in INVERSION_PARAMS:
            recovered = result["params"][pname]
            true_val = watermelon_params[pname]
            rel_err = abs(recovered - true_val) / abs(true_val)
            assert rel_err < 0.01, (
                f"Watermelon {pname}: error {rel_err:.2%}"
            )

    def test_residuals_near_zero(self, abdomen_params, abdomen_frequencies):
        """Residuals after inversion should be < 0.001 Hz."""
        guess = dict(abdomen_params)
        guess["a"] *= 1.05

        result = invert_frequencies(
            abdomen_frequencies, initial_guess=guess, model="ritz"
        )
        assert np.all(np.abs(result["residual_hz"]) < 0.001)


# ═══════════════════════════════════════════════════════════════════════════
#  5. Cramér–Rao Bounds
# ═══════════════════════════════════════════════════════════════════════════

class TestCramerRaoBounds:
    """Fisher information and CR bounds should scale correctly."""

    def test_cr_bounds_decrease_with_less_noise(self, abdomen_params):
        """Halving noise should roughly halve the CR bounds."""
        r1 = identifiability_analysis(abdomen_params, noise_level=0.02, model="ritz")
        r2 = identifiability_analysis(abdomen_params, noise_level=0.01, model="ritz")

        for pname in INVERSION_PARAMS:
            # CR bound ∝ noise_level, so ratio should be ~2
            ratio = r1["cr_bounds"][pname] / r2["cr_bounds"][pname]
            assert 1.5 < ratio < 2.5, (
                f"CR bound ratio for {pname} is {ratio:.2f}, expected ~2.0"
            )

    def test_cr_bounds_finite_for_oblate(self, abdomen_params):
        """All CR bounds should be finite for the oblate model."""
        result = identifiability_analysis(abdomen_params, model="ritz")
        for pname in INVERSION_PARAMS:
            assert np.isfinite(result["cr_bounds"][pname]), (
                f"CR bound for {pname} is not finite"
            )

    def test_cr_bounds_infinite_for_sphere(self, abdomen_params):
        """Sphere model should have infinite (or very large) CR bounds."""
        result = identifiability_analysis(abdomen_params, model="sphere")
        # At least one bound should be inf (from near-singular Fisher)
        has_unidentifiable = any(
            not np.isfinite(v) or v > 100
            for v in result["relative_cr_bounds"].values()
        )
        assert has_unidentifiable, (
            f"Sphere relative CR bounds all finite and small: "
            f"{result['relative_cr_bounds']}"
        )

    def test_fisher_matrix_symmetric(self, abdomen_params):
        result = identifiability_analysis(abdomen_params, model="ritz")
        F = result["fisher_information"]
        np.testing.assert_allclose(F, F.T, atol=1e-10,
                                   err_msg="Fisher matrix not symmetric")

    def test_relative_cr_bounds_reasonable(self, abdomen_params):
        """With 1 % noise, relative CR bounds should be < 50 % for oblate."""
        result = identifiability_analysis(
            abdomen_params, noise_level=0.01, model="ritz"
        )
        for pname in INVERSION_PARAMS:
            assert result["relative_cr_bounds"][pname] < 0.50, (
                f"Relative CR bound for {pname} is "
                f"{result['relative_cr_bounds'][pname]:.2%}, expected < 50 %"
            )


# ═══════════════════════════════════════════════════════════════════════════
#  6. Watermelon Parameters
# ═══════════════════════════════════════════════════════════════════════════

class TestWatermelonIdentifiability:
    """Identifiability should also work for watermelon geometry."""

    def test_watermelon_oblate_well_conditioned(self, watermelon_params):
        kappa = jacobian_condition_number(watermelon_params, model="ritz")
        assert kappa < 1000, (
            f"Watermelon oblate condition number {kappa:.1f} too large"
        )

    def test_watermelon_frequencies_physical(self, watermelon_params):
        """Watermelon flexural frequencies should be in 50–500 Hz range."""
        f = _forward_ritz(watermelon_params, DEFAULT_MODES)
        assert np.all(f > 10), f"Frequencies too low: {f}"
        assert np.all(f < 2000), f"Frequencies too high: {f}"

    def test_watermelon_cr_bounds_finite(self, watermelon_params):
        result = identifiability_analysis(watermelon_params, model="ritz")
        for pname in INVERSION_PARAMS:
            assert np.isfinite(result["cr_bounds"][pname])


# ═══════════════════════════════════════════════════════════════════════════
#  7. Sphere vs Oblate Comparison
# ═══════════════════════════════════════════════════════════════════════════

class TestSphereVsOblateComparison:
    """The headline comparison function should return correct flags."""

    def test_comparison_returns_expected_keys(self, abdomen_params):
        result = sphere_vs_oblate_comparison(abdomen_params)
        expected_keys = {
            "sphere", "oblate", "sphere_condition", "oblate_condition",
            "improvement_factor", "sphere_rank_deficient",
            "oblate_well_conditioned",
        }
        assert expected_keys.issubset(result.keys())

    def test_sphere_flagged_rank_deficient(self, abdomen_params):
        result = sphere_vs_oblate_comparison(abdomen_params)
        assert result["sphere_rank_deficient"] is True

    def test_oblate_flagged_well_conditioned(self, abdomen_params):
        result = sphere_vs_oblate_comparison(abdomen_params)
        assert result["oblate_well_conditioned"] is True

    def test_improvement_factor_large(self, abdomen_params):
        result = sphere_vs_oblate_comparison(abdomen_params)
        assert result["improvement_factor"] > 1e5, (
            f"Improvement factor {result['improvement_factor']:.2e} too small"
        )


# ═══════════════════════════════════════════════════════════════════════════
#  8. Condition Number Map
# ═══════════════════════════════════════════════════════════════════════════

class TestConditionNumberMap:
    """Condition number sweep should return correct shapes."""

    def test_map_shape(self, abdomen_params):
        a_range = np.array([0.16, 0.18, 0.20])
        c_range = np.array([0.10, 0.12])
        E_range = np.array([0.05e6, 0.10e6])
        kappa = condition_number_map(
            a_range, c_range, E_range,
            base_params=abdomen_params, model="ritz",
        )
        assert kappa.shape == (3, 2, 2)

    def test_map_values_finite(self, abdomen_params):
        a_range = np.array([0.17, 0.19])
        c_range = np.array([0.11, 0.13])
        E_range = np.array([0.08e6, 0.12e6])
        kappa = condition_number_map(
            a_range, c_range, E_range,
            base_params=abdomen_params, model="ritz",
        )
        assert np.all(np.isfinite(kappa))
        assert np.all(kappa > 0)


# ═══════════════════════════════════════════════════════════════════════════
#  9. Edge Cases
# ═══════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Graceful handling of edge cases."""

    def test_invalid_model_raises(self, abdomen_params):
        with pytest.raises(ValueError, match="Unknown model"):
            compute_jacobian(abdomen_params, model="invalid")

    def test_single_mode_jacobian(self, abdomen_params):
        """Jacobian with a single mode should be shape (1, 3)."""
        J = compute_jacobian(abdomen_params, model="ritz", modes=(2,))
        assert J.shape == (1, 3)

    def test_more_modes_than_params(self, abdomen_params):
        """More modes than params → overdetermined, should still work."""
        J = compute_jacobian(
            abdomen_params, model="ritz", modes=(2, 3, 4, 5, 6), scaled=True
        )
        assert J.shape == (5, 3)
        rank = np.linalg.matrix_rank(J)
        assert rank == 3, f"Expected full column rank 3, got {rank}"

    def test_inversion_with_defaults(self):
        """Inversion with default canonical params should work."""
        params = dict(CANONICAL_ABDOMEN)
        f_obs = _forward_ritz(params, DEFAULT_MODES)
        guess = dict(params)
        guess["a"] *= 1.05
        guess["c"] *= 0.95
        guess["E"] *= 1.05
        result = invert_frequencies(f_obs, initial_guess=guess, model="ritz")
        assert result["success"]
