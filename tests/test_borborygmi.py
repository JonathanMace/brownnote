"""Tests for the borborygmi acoustic model."""

import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytical.borborygmi_model import (
    BorborygmiParams,
    borborygmi_frequency,
    minnaert_frequency,
    constrained_bubble_frequency,
    helmholtz_frequency,
    cylindrical_axial_frequency,
    cylindrical_radial_frequency,
    volume_sweep,
    tube_diameter_sweep,
    clinical_comparison,
    mode_transition_map,
    ALL_MODES,
    CLINICAL_DATA,
    FIG_DIR,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def default_params():
    """Default borborygmi parameters: 10 mL pocket, 3 cm tube."""
    return BorborygmiParams()


@pytest.fixture
def small_pocket():
    """Small gas pocket: 1 mL."""
    return BorborygmiParams(volume_mL=1.0)


@pytest.fixture
def large_pocket():
    """Large gas pocket: 50 mL."""
    return BorborygmiParams(volume_mL=50.0)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------

class TestBorborygmiParams:
    """Verify derived quantities in the data class."""

    def test_volume_conversion(self, default_params):
        assert default_params.volume_m3 == pytest.approx(10.0e-6, rel=1e-10)

    def test_sphere_radius_10mL(self, default_params):
        R = (3.0 * 10.0e-6 / (4.0 * np.pi)) ** (1.0 / 3.0)
        assert default_params.R_sphere == pytest.approx(R, rel=1e-10)

    def test_lumen_radius(self, default_params):
        assert default_params.R_lumen == pytest.approx(0.015, rel=1e-10)

    def test_slug_length_positive(self, default_params):
        assert default_params.L_slug > 0

    def test_quality_factor(self, default_params):
        assert default_params.Q == pytest.approx(4.0, rel=1e-3)

    def test_neck_area_positive(self, default_params):
        assert default_params.neck_area > 0

    def test_neck_effective_length(self, default_params):
        # L_eff = L + 1.6 * r_neck
        r = default_params.neck_diameter_m / 2.0
        expected = default_params.neck_length_m + 1.6 * r
        assert default_params.neck_length_eff == pytest.approx(expected, rel=1e-10)


# ---------------------------------------------------------------------------
# Dimensional / physical sanity
# ---------------------------------------------------------------------------

class TestDimensionalSanity:
    """All frequencies must be positive and in physically sensible ranges."""

    def test_minnaert_positive(self, default_params):
        f = minnaert_frequency(default_params)
        assert f > 0

    def test_constrained_positive(self, default_params):
        f = constrained_bubble_frequency(default_params)
        assert f > 0

    def test_helmholtz_positive(self, default_params):
        f = helmholtz_frequency(default_params)
        assert f > 0

    def test_axial_positive(self, default_params):
        f = cylindrical_axial_frequency(default_params)
        assert f > 0

    def test_radial_positive(self, default_params):
        f = cylindrical_radial_frequency(default_params)
        assert f > 0

    def test_minnaert_order_of_magnitude(self, default_params):
        """Minnaert for 10 mL should be in the hundreds of Hz."""
        f = minnaert_frequency(default_params)
        assert 50 < f < 5000, f"Minnaert = {f:.1f} Hz out of expected range"

    def test_constrained_with_stiff_wall_higher_than_minnaert(self):
        """With a stiff wall, elastic constraint raises the frequency above Minnaert."""
        p_stiff = BorborygmiParams(E_wall=1.0e6)
        f_min = minnaert_frequency(p_stiff)
        f_con = constrained_bubble_frequency(p_stiff)
        assert f_con > f_min

    def test_constrained_reduces_to_minnaert_no_wall(self):
        """With E_wall=0 and h_wall->0 the constrained model matches Minnaert."""
        p = BorborygmiParams(E_wall=0.0, h_wall=1e-10, rho_wall=0.0)
        f_con = constrained_bubble_frequency(p)
        f_min = minnaert_frequency(p)
        assert f_con == pytest.approx(f_min, rel=1e-4)

    def test_all_modes_finite(self, default_params):
        for mode in ["minnaert", "constrained", "helmholtz", "axial", "radial"]:
            f = borborygmi_frequency(default_params.volume_mL, mode=mode)
            assert np.isfinite(f), f"Mode {mode} returned non-finite"


# ---------------------------------------------------------------------------
# Monotonicity tests
# ---------------------------------------------------------------------------

class TestMonotonicity:
    """Frequencies should decrease with increasing volume (larger bubble = lower pitch)."""

    @pytest.mark.parametrize("mode", ["minnaert", "constrained", "helmholtz", "axial"])
    def test_frequency_decreases_with_volume(self, mode):
        f_small = borborygmi_frequency(1.0, mode=mode)
        f_large = borborygmi_frequency(50.0, mode=mode)
        assert f_small > f_large, (
            f"{mode}: f(1 mL)={f_small:.1f} should exceed f(50 mL)={f_large:.1f}"
        )

    def test_minnaert_inversely_proportional_to_radius(self):
        """f proportional to 1/R for Minnaert; doubling volume reduces f by 2^(1/3)."""
        f1 = borborygmi_frequency(10.0, mode="minnaert")
        f2 = borborygmi_frequency(20.0, mode="minnaert")
        ratio = f1 / f2
        expected = 2.0 ** (1.0 / 3.0)
        assert ratio == pytest.approx(expected, rel=0.01)


# ---------------------------------------------------------------------------
# Clinical range validation
# ---------------------------------------------------------------------------

class TestClinicalRange:
    """Model predictions should overlap with clinical borborygmi frequencies."""

    def test_constrained_10mL_in_clinical_range(self):
        """A 10 mL pocket should produce a frequency within 100-800 Hz."""
        f = borborygmi_frequency(10.0, mode="constrained")
        assert 100 < f < 800, f"f = {f:.1f} Hz outside clinical plausibility"

    def test_volume_sweep_spans_clinical_band(self):
        """Over 1-50 mL the constrained model should span most of 200-550 Hz."""
        f_small = borborygmi_frequency(1.0, mode="constrained")
        f_large = borborygmi_frequency(50.0, mode="constrained")
        assert f_small > 200
        assert f_large < 550

    def test_helmholtz_10mL_in_clinical_range(self):
        f = borborygmi_frequency(10.0, mode="helmholtz")
        assert 50 < f < 2000, f"Helmholtz = {f:.1f} Hz outside plausibility"


# ---------------------------------------------------------------------------
# Convenience function tests
# ---------------------------------------------------------------------------

class TestConvenienceFunction:
    """Test the borborygmi_frequency() wrapper."""

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match="Unknown mode"):
            borborygmi_frequency(10.0, mode="invalid")

    def test_kwargs_passthrough(self):
        """Custom E_wall should change the constrained frequency."""
        f_default = borborygmi_frequency(10.0, mode="constrained")
        f_stiff = borborygmi_frequency(10.0, mode="constrained", E_wall=100e3)
        assert f_stiff > f_default

    def test_all_modes_return_float(self):
        for mode in ["minnaert", "constrained", "helmholtz", "axial", "radial"]:
            f = borborygmi_frequency(10.0, mode=mode)
            assert isinstance(f, float)


# ---------------------------------------------------------------------------
# Sweep tests
# ---------------------------------------------------------------------------

class TestSweeps:
    """Parametric sweep functions return correct shapes."""

    def test_volume_sweep_shape(self):
        vols = np.linspace(1, 50, 20)
        results = volume_sweep(vols, modes=["minnaert", "constrained"])
        assert len(results) == 2
        for mode_name in ["minnaert", "constrained"]:
            assert results[mode_name]["frequencies_hz"].shape == (20,)
            assert results[mode_name]["volumes_mL"].shape == (20,)

    def test_diameter_sweep_shape(self):
        diams = np.linspace(0.02, 0.05, 15)
        results = tube_diameter_sweep(diams, modes=["radial"])
        assert results["radial"]["frequencies_hz"].shape == (15,)

    def test_clinical_comparison_structure(self):
        comp = clinical_comparison(np.linspace(1, 50, 10))
        assert "model" in comp
        assert "clinical" in comp
        assert "healthy_adult" in comp["clinical"]


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Extreme parameter values should not crash."""

    def test_very_small_volume(self):
        f = borborygmi_frequency(0.1, mode="minnaert")
        assert np.isfinite(f) and f > 0

    def test_very_large_volume(self):
        f = borborygmi_frequency(200.0, mode="minnaert")
        assert np.isfinite(f) and f > 0

    def test_zero_wall_stiffness(self):
        """With E_wall=0 and negligible wall mass, the constrained model -> Minnaert."""
        p = BorborygmiParams(E_wall=0.0, h_wall=1e-10, rho_wall=0.0)
        f_con = constrained_bubble_frequency(p)
        f_min = minnaert_frequency(p)
        assert f_con == pytest.approx(f_min, rel=0.01)

    def test_very_stiff_wall(self):
        """Very stiff wall should push constrained frequency higher than default."""
        f_default = borborygmi_frequency(10.0, mode="constrained")
        f_stiff = borborygmi_frequency(10.0, mode="constrained", E_wall=1e6)
        assert f_stiff > 1.5 * f_default

    def test_large_tube_diameter(self):
        f = borborygmi_frequency(10.0, tube_diameter_m=0.10, mode="axial")
        assert np.isfinite(f) and f > 0


# ---------------------------------------------------------------------------
# Mode transition map tests
# ---------------------------------------------------------------------------

class TestModeTransitionMap:
    """Tests for the mode_transition_map function."""

    @pytest.fixture(autouse=True)
    def _compute_map(self):
        """Compute the map once for the class."""
        self.data = mode_transition_map(
            V_range=(0.1, 100.0), n_points=200
        )

    def test_return_keys(self):
        """Return dict has all expected keys."""
        assert set(self.data.keys()) == {
            "volumes_mL", "frequencies", "dominant_mode", "crossovers",
        }

    def test_volume_array_shape(self):
        assert self.data["volumes_mL"].shape == (200,)

    def test_all_modes_present(self):
        """Every mode has a frequency array of the right length."""
        for mode in ALL_MODES:
            assert mode in self.data["frequencies"]
            assert self.data["frequencies"][mode].shape == (200,)

    def test_all_frequencies_positive_finite(self):
        """Every frequency value must be positive and finite."""
        for mode in ALL_MODES:
            f = self.data["frequencies"][mode]
            assert np.all(np.isfinite(f)), f"{mode} has non-finite values"
            assert np.all(f > 0), f"{mode} has non-positive values"

    @pytest.mark.parametrize("mode", ["minnaert", "constrained", "helmholtz", "axial"])
    def test_frequency_monotonically_decreasing(self, mode):
        """For bubble/slug modes, frequency must decrease with volume."""
        f = self.data["frequencies"][mode]
        assert np.all(np.diff(f) < 0), (
            f"{mode}: frequency is not monotonically decreasing with volume"
        )

    def test_radial_mode_independent_of_volume(self):
        """Radial mode depends on tube diameter, not gas pocket volume."""
        f = self.data["frequencies"]["radial"]
        assert np.std(f) / np.mean(f) < 1e-10, "Radial mode should be volume-independent"

    def test_dominant_mode_length(self):
        assert len(self.data["dominant_mode"]) == 200

    def test_dominant_mode_valid_names(self):
        """All dominant mode labels are valid mode names."""
        for m in self.data["dominant_mode"]:
            assert m in ALL_MODES

    def test_crossovers_are_list_of_dicts(self):
        xo = self.data["crossovers"]
        assert isinstance(xo, list)
        for item in xo:
            assert "volume_mL" in item
            assert "frequency_hz" in item
            assert "mode_below" in item
            assert "mode_above" in item

    def test_crossover_volumes_within_range(self):
        """All crossover volumes lie within the requested range."""
        for xo in self.data["crossovers"]:
            assert 0.1 <= xo["volume_mL"] <= 100.0

    def test_crossover_frequencies_positive(self):
        for xo in self.data["crossovers"]:
            assert xo["frequency_hz"] > 0

    def test_crossover_modes_differ(self):
        """mode_below and mode_above must be different at each crossover."""
        for xo in self.data["crossovers"]:
            assert xo["mode_below"] != xo["mode_above"]

    def test_clinical_range_overlap(self):
        """At least one mode must produce frequencies in the clinical range (200-550 Hz)."""
        clinical_lo, clinical_hi = 200.0, 550.0
        found = False
        for mode in ALL_MODES:
            f = self.data["frequencies"][mode]
            if np.any((f >= clinical_lo) & (f <= clinical_hi)):
                found = True
                break
        assert found, "No mode overlaps with clinical borborygmi range 200-550 Hz"

    def test_stiff_wall_constrained_above_minnaert(self):
        """With a stiff wall, elastic constraint raises frequency above Minnaert."""
        stiff = mode_transition_map(
            V_range=(0.1, 10.0), n_points=20, E_wall=1.0e6,
        )
        f_con = stiff["frequencies"]["constrained"]
        f_min = stiff["frequencies"]["minnaert"]
        assert np.all(f_con > f_min)

    def test_custom_tube_diameter(self):
        """Function accepts tube_diameter_m and produces valid results."""
        data2 = mode_transition_map(V_range=(1, 50), tube_diameter_m=0.05, n_points=50)
        assert data2["volumes_mL"].shape == (50,)
        for mode in ALL_MODES:
            assert np.all(data2["frequencies"][mode] > 0)


class TestPlotModeTransitionMap:
    """Smoke test for figure generation (headless)."""

    def test_figure_generates_without_error(self):
        import matplotlib
        matplotlib.use("Agg")
        from analytical.borborygmi_model import plot_mode_transition_map

        fig = plot_mode_transition_map(
            V_range=(0.5, 80.0), n_points=50, save=False,
        )
        assert fig is not None
        axes = fig.get_axes()
        assert len(axes) >= 1
        # Check log scales
        assert axes[0].get_xscale() == "log"
        assert axes[0].get_yscale() == "log"


def test_borborygmi_paper_figure_directory_points_to_manuscript_folder():
    """Publication figures should save beside the borborygmi manuscript."""
    assert FIG_DIR.parts[-3:] == ("borborygmi", "paper", "figures")
