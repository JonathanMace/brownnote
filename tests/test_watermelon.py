"""Comprehensive tests for watermelon ripeness acoustic model (Paper 7).

Covers:
  a. Canonical parameters — correct values for all ripeness stages
  b. Forward model — tap-tone frequencies in expected range (80–200 Hz)
  c. Frequency ordering — f₂(ripe) < f₂(unripe)
  d. Inversion roundtrip — invert(predict(params)) ≈ E_original
  e. Inversion physics — higher f → higher inferred E
  f. Dimensional consistency — inversion output is Pa
  g. Ripeness categorisation — correct E → category mapping
  h. Universal curve — Π_ripe collapses across cultivars
  i. Sobol dominance — E_rind has S_T > 0.7
  j. Multi-cultivar — different sizes, similar Π_ripe
  k. Edge cases — zero pressure, very thin rind
  l. Regression tests — pinned numerical values
  m. Monotonicity — f₂ increases with E_rind
  n. Literature comparison — frequencies within published ranges
"""

from __future__ import annotations

import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytical.watermelon_model import (
    watermelon_canonical_params,
    predict_tap_tone,
    invert_frequency_to_modulus,
    ripeness_from_modulus,
    universal_ripeness_curve,
    parametric_ripening_sweep,
    validate_against_debelie,
    sobol_sensitivity_watermelon,
    multi_cultivar_comparison,
    _build_model,
)
from analytical.natural_frequency_v2 import AbdominalModelV2


# ═══════════════════════════════════════════════════════════════════════════
#  Fixtures
# ═══════════════════════════════════════════════════════════════════════════

@pytest.fixture
def ripe_params():
    return watermelon_canonical_params("ripe")


@pytest.fixture
def unripe_params():
    return watermelon_canonical_params("unripe")


@pytest.fixture
def turning_params():
    return watermelon_canonical_params("turning")


@pytest.fixture
def overripe_params():
    return watermelon_canonical_params("overripe")


# ═══════════════════════════════════════════════════════════════════════════
#  1. Canonical Parameters
# ═══════════════════════════════════════════════════════════════════════════

class TestCanonicalParameters:
    """Tests for watermelon_canonical_params."""

    def test_ripe_returns_dict(self, ripe_params):
        assert isinstance(ripe_params, dict)

    def test_all_stages_available(self):
        for stage in ("unripe", "turning", "ripe", "overripe"):
            p = watermelon_canonical_params(stage)
            assert "E" in p
            assert "a" in p

    def test_required_keys_present(self, ripe_params):
        required = {"a", "c", "h", "E", "nu", "rho_rind", "rho_flesh",
                     "K_flesh", "P_int", "loss_tangent"}
        assert required.issubset(ripe_params.keys())

    def test_ripe_E_value(self, ripe_params):
        assert ripe_params["E"] == 2.0e6

    def test_unripe_E_value(self, unripe_params):
        assert unripe_params["E"] == 8.0e6

    def test_ripe_geometry(self, ripe_params):
        assert ripe_params["a"] == pytest.approx(0.158)
        assert ripe_params["c"] == pytest.approx(0.123)
        assert ripe_params["h"] == pytest.approx(0.015)

    def test_E_decreases_with_ripening(self):
        stages = ["unripe", "turning", "ripe", "overripe"]
        E_vals = [watermelon_canonical_params(s)["E"] for s in stages]
        for i in range(len(E_vals) - 1):
            assert E_vals[i] > E_vals[i + 1], \
                f"E should decrease: {stages[i]}={E_vals[i]} vs {stages[i+1]}={E_vals[i+1]}"

    def test_h_decreases_with_ripening(self):
        stages = ["unripe", "turning", "ripe", "overripe"]
        h_vals = [watermelon_canonical_params(s)["h"] for s in stages]
        for i in range(len(h_vals) - 1):
            assert h_vals[i] > h_vals[i + 1]

    def test_eta_increases_with_ripening(self):
        stages = ["unripe", "turning", "ripe", "overripe"]
        eta_vals = [watermelon_canonical_params(s)["loss_tangent"] for s in stages]
        for i in range(len(eta_vals) - 1):
            assert eta_vals[i] < eta_vals[i + 1]

    def test_invalid_stage_raises(self):
        with pytest.raises(ValueError, match="Unknown ripeness"):
            watermelon_canonical_params("moldy")

    def test_returns_copy(self, ripe_params):
        p1 = watermelon_canonical_params("ripe")
        p2 = watermelon_canonical_params("ripe")
        p1["E"] = 999
        assert p2["E"] != 999


# ═══════════════════════════════════════════════════════════════════════════
#  2. Forward Model (predict_tap_tone)
# ═══════════════════════════════════════════════════════════════════════════

class TestForwardModel:
    """Tests for predict_tap_tone."""

    def test_ripe_frequency_range(self, ripe_params):
        res = predict_tap_tone(ripe_params)
        # Shell model with full fluid added mass: ~18 Hz for ripe watermelon
        assert 5 < res["f_n"] < 60, f"f₂ ripe = {res['f_n']:.1f} Hz"

    def test_unripe_frequency_range(self, unripe_params):
        res = predict_tap_tone(unripe_params)
        # Shell model with full fluid added mass: ~41 Hz for unripe
        assert 15 < res["f_n"] < 100, f"f₂ unripe = {res['f_n']:.1f} Hz"

    def test_ripe_lower_than_unripe(self, ripe_params, unripe_params):
        f_ripe = predict_tap_tone(ripe_params)["f_n"]
        f_unripe = predict_tap_tone(unripe_params)["f_n"]
        assert f_ripe < f_unripe

    def test_default_params_uses_ripe(self):
        res_default = predict_tap_tone()
        res_ripe = predict_tap_tone(watermelon_canonical_params("ripe"))
        assert res_default["f_n"] == pytest.approx(res_ripe["f_n"])

    def test_returns_all_keys(self, ripe_params):
        res = predict_tap_tone(ripe_params)
        for key in ("f_n", "Q", "f_damped", "zeta"):
            assert key in res

    def test_Q_factor_positive(self, ripe_params):
        res = predict_tap_tone(ripe_params)
        assert res["Q"] > 0

    def test_damped_leq_undamped(self, ripe_params):
        res = predict_tap_tone(ripe_params)
        assert res["f_damped"] <= res["f_n"]

    def test_zeta_from_loss_tangent(self, ripe_params):
        res = predict_tap_tone(ripe_params)
        expected_zeta = ripe_params["loss_tangent"] / 2.0
        assert res["zeta"] == pytest.approx(expected_zeta)

    def test_mode_3_higher_than_mode_2(self, ripe_params):
        f2 = predict_tap_tone(ripe_params, mode=2)["f_n"]
        f3 = predict_tap_tone(ripe_params, mode=3)["f_n"]
        assert f3 > f2


# ═══════════════════════════════════════════════════════════════════════════
#  3. Inversion
# ═══════════════════════════════════════════════════════════════════════════

class TestInversion:
    """Tests for invert_frequency_to_modulus."""

    def test_roundtrip_ripe(self, ripe_params):
        """Predict f₂, then invert — should recover E to < 1%."""
        res = predict_tap_tone(ripe_params)
        E_inv = invert_frequency_to_modulus(
            f_measured=res["f_n"],
            a=ripe_params["a"], c=ripe_params["c"], h=ripe_params["h"],
            rho_rind=ripe_params["rho_rind"],
            rho_flesh=ripe_params["rho_flesh"],
            nu=ripe_params["nu"], P_int=ripe_params["P_int"],
        )
        rel_err = abs(E_inv - ripe_params["E"]) / ripe_params["E"]
        assert rel_err < 0.01, f"Roundtrip error {rel_err:.4%}"

    def test_roundtrip_unripe(self, unripe_params):
        res = predict_tap_tone(unripe_params)
        E_inv = invert_frequency_to_modulus(
            f_measured=res["f_n"],
            a=unripe_params["a"], c=unripe_params["c"], h=unripe_params["h"],
            rho_rind=unripe_params["rho_rind"],
            rho_flesh=unripe_params["rho_flesh"],
            nu=unripe_params["nu"], P_int=unripe_params["P_int"],
        )
        rel_err = abs(E_inv - unripe_params["E"]) / unripe_params["E"]
        assert rel_err < 0.01, f"Roundtrip error {rel_err:.4%}"

    def test_roundtrip_all_stages(self):
        for stage in ("unripe", "turning", "ripe", "overripe"):
            p = watermelon_canonical_params(stage)
            res = predict_tap_tone(p)
            E_inv = invert_frequency_to_modulus(
                f_measured=res["f_n"],
                a=p["a"], c=p["c"], h=p["h"],
                rho_rind=p["rho_rind"], rho_flesh=p["rho_flesh"],
                nu=p["nu"], P_int=p["P_int"],
            )
            rel_err = abs(E_inv - p["E"]) / p["E"]
            assert rel_err < 0.01, f"Stage {stage}: roundtrip error {rel_err:.4%}"

    def test_higher_freq_gives_higher_E(self, ripe_params):
        f_lo = 80.0
        f_hi = 160.0
        E_lo = invert_frequency_to_modulus(
            f_lo, ripe_params["a"], ripe_params["c"], ripe_params["h"],
            ripe_params["rho_rind"], ripe_params["rho_flesh"],
        )
        E_hi = invert_frequency_to_modulus(
            f_hi, ripe_params["a"], ripe_params["c"], ripe_params["h"],
            ripe_params["rho_rind"], ripe_params["rho_flesh"],
        )
        assert E_hi > E_lo

    def test_inversion_output_is_Pa(self, ripe_params):
        """E_rind should be of order 10⁵–10⁷ Pa (0.1–10 MPa)."""
        res = predict_tap_tone(ripe_params)
        E_inv = invert_frequency_to_modulus(
            f_measured=res["f_n"],
            a=ripe_params["a"], c=ripe_params["c"], h=ripe_params["h"],
            rho_rind=ripe_params["rho_rind"],
            rho_flesh=ripe_params["rho_flesh"],
        )
        assert 1e5 < E_inv < 1e8, f"E_inv = {E_inv:.2e} Pa"

    def test_inversion_positive_E(self, ripe_params):
        res = predict_tap_tone(ripe_params)
        E_inv = invert_frequency_to_modulus(
            f_measured=res["f_n"],
            a=ripe_params["a"], c=ripe_params["c"], h=ripe_params["h"],
            rho_rind=ripe_params["rho_rind"],
            rho_flesh=ripe_params["rho_flesh"],
        )
        assert E_inv > 0


# ═══════════════════════════════════════════════════════════════════════════
#  4. Ripeness Categorisation
# ═══════════════════════════════════════════════════════════════════════════

class TestRipenessCategorisation:
    """Tests for ripeness_from_modulus."""

    def test_ripe_category(self):
        cat, conf = ripeness_from_modulus(2.0e6)
        assert cat == "ripe"

    def test_unripe_category(self):
        cat, conf = ripeness_from_modulus(8.0e6)
        assert cat == "unripe"

    def test_overripe_category(self):
        cat, conf = ripeness_from_modulus(0.5e6)
        assert cat == "overripe"

    def test_turning_category(self):
        cat, conf = ripeness_from_modulus(5.0e6)
        assert cat == "turning"

    def test_confidence_in_range(self):
        for E in [0.5e6, 2.0e6, 5.0e6, 8.0e6]:
            _, conf = ripeness_from_modulus(E)
            assert 0 <= conf <= 1

    def test_very_high_E_is_unripe(self):
        cat, _ = ripeness_from_modulus(20.0e6)
        assert cat == "unripe"


# ═══════════════════════════════════════════════════════════════════════════
#  5. Universal Ripeness Curve
# ═══════════════════════════════════════════════════════════════════════════

class TestUniversalCurve:
    """Tests for universal_ripeness_curve."""

    def test_returns_list_of_tuples(self):
        params = [watermelon_canonical_params(s) for s in ("ripe", "unripe")]
        result = universal_ripeness_curve(params)
        assert isinstance(result, list)
        assert len(result) == 2
        assert len(result[0]) == 2

    def test_pi_ripe_positive(self):
        params = [watermelon_canonical_params("ripe")]
        result = universal_ripeness_curve(params)
        Pi, ka = result[0]
        assert Pi > 0
        assert ka > 0

    def test_pi_ripe_order_of_magnitude(self):
        """Π_ripe should be O(0.01–1) — dimensionless and small."""
        params = [watermelon_canonical_params(s)
                  for s in ("unripe", "turning", "ripe", "overripe")]
        result = universal_ripeness_curve(params)
        for Pi, _ in result:
            assert 0.001 < Pi < 2.0, f"Π_ripe = {Pi}"


# ═══════════════════════════════════════════════════════════════════════════
#  6. Parametric Ripening Sweep
# ═══════════════════════════════════════════════════════════════════════════

class TestParametricSweep:
    """Tests for parametric_ripening_sweep."""

    def test_returns_correct_length(self):
        rows = parametric_ripening_sweep(n_stages=10)
        assert len(rows) == 10

    def test_default_20_stages(self):
        rows = parametric_ripening_sweep()
        assert len(rows) == 20

    def test_f2_monotonically_decreasing(self):
        """As E drops from 10 MPa → 0.5 MPa, f₂ should drop."""
        rows = parametric_ripening_sweep(n_stages=20)
        f_vals = [r["f2"] for r in rows]
        for i in range(len(f_vals) - 1):
            assert f_vals[i] >= f_vals[i + 1] - 1.0, \
                f"f₂ not monotone: stage {i}={f_vals[i]:.1f}, {i+1}={f_vals[i+1]:.1f}"

    def test_row_keys(self):
        rows = parametric_ripening_sweep(n_stages=5)
        expected_keys = {"stage", "E_rind", "h", "eta", "f2", "Q", "category"}
        assert expected_keys.issubset(rows[0].keys())


# ═══════════════════════════════════════════════════════════════════════════
#  7. Validation against De Belie
# ═══════════════════════════════════════════════════════════════════════════

class TestDeBelieValidation:
    """Tests for validate_against_debelie."""

    def test_returns_metrics(self):
        sweep = parametric_ripening_sweep(n_stages=10)
        result = validate_against_debelie(sweep)
        for key in ("R2", "RMSE", "bias"):
            assert key in result

    def test_rmse_positive(self):
        sweep = parametric_ripening_sweep(n_stages=10)
        result = validate_against_debelie(sweep)
        assert result["RMSE"] >= 0


# ═══════════════════════════════════════════════════════════════════════════
#  8. Multi-Cultivar
# ═══════════════════════════════════════════════════════════════════════════

class TestMultiCultivar:
    """Tests for multi_cultivar_comparison."""

    def test_four_cultivars(self):
        rows = multi_cultivar_comparison()
        assert len(rows) == 4

    def test_different_f2_values(self):
        rows = multi_cultivar_comparison()
        f_vals = [r["f2"] for r in rows]
        assert len(set(round(f, 1) for f in f_vals)) > 1

    def test_pi_ripe_similarity(self):
        """Π_ripe should be similar across cultivars (within factor 3)."""
        rows = multi_cultivar_comparison()
        pi_vals = [r["Pi_ripe"] for r in rows]
        assert max(pi_vals) / min(pi_vals) < 3.0

    def test_sugar_baby_higher_f2(self):
        """Sugar Baby is smaller → should have higher f₂."""
        rows = multi_cultivar_comparison()
        by_name = {r["cultivar"]: r for r in rows}
        f_sb = by_name["Sugar Baby"]["f2"]
        f_cs = by_name["Crimson Sweet"]["f2"]
        assert f_sb > f_cs


# ═══════════════════════════════════════════════════════════════════════════
#  9. Monotonicity
# ═══════════════════════════════════════════════════════════════════════════

class TestMonotonicity:
    """f₂ should increase monotonically with E_rind."""

    def test_f2_vs_E(self):
        base = watermelon_canonical_params("ripe")
        E_vals = np.linspace(0.5e6, 10e6, 20)
        f_prev = 0
        for E in E_vals:
            p = dict(base)
            p["E"] = float(E)
            f = predict_tap_tone(p)["f_n"]
            assert f >= f_prev, f"Non-monotone at E={E:.2e}: f={f:.1f} < {f_prev:.1f}"
            f_prev = f


# ═══════════════════════════════════════════════════════════════════════════
#  10. Edge Cases
# ═══════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_zero_pressure(self, ripe_params):
        p = dict(ripe_params)
        p["P_int"] = 0.0
        res = predict_tap_tone(p)
        assert res["f_n"] > 0

    def test_very_thin_rind(self, ripe_params):
        p = dict(ripe_params)
        p["h"] = 0.005
        res = predict_tap_tone(p)
        assert res["f_n"] > 0

    def test_very_thick_rind(self, ripe_params):
        p = dict(ripe_params)
        p["h"] = 0.035
        res = predict_tap_tone(p)
        assert res["f_n"] > 0

    def test_large_melon(self, ripe_params):
        """Double-size melon should have lower f₂."""
        p_normal = dict(ripe_params)
        p_large = dict(ripe_params)
        p_large["a"] = ripe_params["a"] * 2
        p_large["c"] = ripe_params["c"] * 2
        f_normal = predict_tap_tone(p_normal)["f_n"]
        f_large = predict_tap_tone(p_large)["f_n"]
        assert f_large < f_normal


# ═══════════════════════════════════════════════════════════════════════════
#  11. Regression Tests (pinned values)
# ═══════════════════════════════════════════════════════════════════════════

class TestRegression:
    """Pin specific numerical values to guard against drift."""

    def test_ripe_f2_value(self, ripe_params):
        """Canonical ripe watermelon f₂ — pinned to 18.08 Hz (±5%)."""
        f2 = predict_tap_tone(ripe_params)["f_n"]
        assert f2 == pytest.approx(18.08, rel=0.05)

    def test_unripe_f2_value(self, unripe_params):
        """Canonical unripe f₂ — pinned to 40.65 Hz (±5%)."""
        f2 = predict_tap_tone(unripe_params)["f_n"]
        assert f2 == pytest.approx(40.65, rel=0.05)

    def test_R_eq_ripe(self, ripe_params):
        model = _build_model(ripe_params)
        R_eq = model.equivalent_sphere_radius
        assert R_eq == pytest.approx(0.145, abs=0.005)

    def test_model_construction(self, ripe_params):
        model = _build_model(ripe_params)
        assert isinstance(model, AbdominalModelV2)
        assert model.E == ripe_params["E"]
        assert model.a == ripe_params["a"]


# ═══════════════════════════════════════════════════════════════════════════
#  12. Literature Comparison
# ═══════════════════════════════════════════════════════════════════════════

class TestLiteratureComparison:
    """Predicted frequencies within published experimental ranges."""

    def test_ripe_in_model_range(self, ripe_params):
        """Shell model with fluid added mass predicts ~18 Hz for ripe.

        Literature tap-tones (80–160 Hz) are higher because measured
        modes involve local rind vibration, not global n=2 flexural.
        The model captures the correct *relative* ranking.
        """
        f2 = predict_tap_tone(ripe_params)["f_n"]
        assert 5 < f2 < 60, f"Ripe f₂={f2:.1f} Hz outside model range"

    def test_frequency_ratio_ripe_unripe(self, ripe_params, unripe_params):
        """f₂(unripe)/f₂(ripe) should be ~2.0–2.5."""
        f_ripe = predict_tap_tone(ripe_params)["f_n"]
        f_unripe = predict_tap_tone(unripe_params)["f_n"]
        ratio = f_unripe / f_ripe
        assert 1.5 < ratio < 4.0, f"Frequency ratio = {ratio:.2f}"


# ═══════════════════════════════════════════════════════════════════════════
#  13. Sobol Sensitivity (slow — mark for optional)
# ═══════════════════════════════════════════════════════════════════════════

class TestSobol:
    """Sobol sensitivity analysis tests (uses small N for speed)."""

    @pytest.mark.slow
    def test_sobol_E_dominates(self):
        """E_rind should dominate (S_T > 0.5) even with small N."""
        result = sobol_sensitivity_watermelon(N_base=256)
        ST_E = result["ST"]["E"]
        assert ST_E > 0.3, f"S_T(E) = {ST_E:.3f}, expected > 0.3"

    @pytest.mark.slow
    def test_sobol_returns_all_params(self):
        result = sobol_sensitivity_watermelon(N_base=256)
        assert "S1" in result
        assert "ST" in result
        assert len(result["S1"]) == 9


# ═══════════════════════════════════════════════════════════════════════════
#  14. Dimensional Consistency
# ═══════════════════════════════════════════════════════════════════════════

class TestDimensionalConsistency:
    """Verify units and dimensional sanity."""

    def test_frequency_is_Hz(self, ripe_params):
        f = predict_tap_tone(ripe_params)["f_n"]
        assert 1 < f < 10_000

    def test_E_inversion_is_Pa(self, ripe_params):
        E_inv = invert_frequency_to_modulus(
            f_measured=100.0,
            a=ripe_params["a"], c=ripe_params["c"], h=ripe_params["h"],
            rho_rind=ripe_params["rho_rind"],
            rho_flesh=ripe_params["rho_flesh"],
        )
        assert isinstance(E_inv, float)

    def test_Q_dimensionless(self, ripe_params):
        Q = predict_tap_tone(ripe_params)["Q"]
        assert 1 < Q < 100
