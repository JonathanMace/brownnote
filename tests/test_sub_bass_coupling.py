"""
Tests for sub_bass_coupling.py — Paper 6.

Covers dimensional consistency, known limits, regression values,
and physically meaningful checks.
"""

import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytical.sub_bass_coupling import (
    ka_parameter,
    airborne_coupling_ratio,
    tissue_displacement,
    perception_threshold_model,
    concert_spl_spectrum,
    concert_displacement_spectrum,
    coupling_transition_band,
    _sum_modal_displacement,
    RHO_AIR,
    C_AIR,
    P_REF,
)
from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def default_model():
    return AbdominalModelV2()


@pytest.fixture
def canonical_R():
    """Canonical equivalent-sphere radius (m)."""
    return AbdominalModelV2().equivalent_sphere_radius


# ── 1. ka parameter ────────────────────────────────────────────────────────

class TestKaParameter:
    """Tests for the Helmholtz number ka."""

    def test_ka_at_canonical_resonance(self, canonical_R):
        """At 3.95 Hz, ka ≈ 0.0114 (Paper 1 canonical value)."""
        ka = ka_parameter(3.95, canonical_R)
        assert abs(ka - 0.0114) < 0.001

    def test_ka_proportional_to_frequency(self, canonical_R):
        """ka should scale linearly with frequency."""
        ka1 = ka_parameter(20.0, canonical_R)
        ka2 = ka_parameter(40.0, canonical_R)
        assert abs(ka2 / ka1 - 2.0) < 1e-10

    def test_ka_at_80hz(self, canonical_R):
        """At 80 Hz, ka should be appreciable (~0.23)."""
        ka = ka_parameter(80.0, canonical_R)
        assert 0.15 < ka < 0.30

    def test_ka_array_input(self, canonical_R):
        """Should accept and return arrays."""
        f = np.array([20, 40, 60, 80])
        ka = ka_parameter(f, canonical_R)
        assert ka.shape == (4,)
        assert np.all(np.diff(ka) > 0)  # monotonically increasing


# ── 2. Airborne coupling ratio ─────────────────────────────────────────────

class TestAirborneCouplingRatio:

    def test_coupling_increases_with_frequency(self, canonical_R):
        """Coupling must increase monotonically with frequency."""
        f = np.linspace(10, 80, 50)
        result = airborne_coupling_ratio(f, canonical_R)
        assert np.all(np.diff(result['coupling_total']) > 0)

    def test_coupling_at_low_ka_matches_paper1(self, canonical_R):
        """At 4 Hz, coupling should match Paper 1's (ka)² ≈ 1.3e-4."""
        result = airborne_coupling_ratio(4.0, canonical_R, mode_n=2)
        ka_sq = result['p_ratio'][0]
        assert 1e-5 < ka_sq < 1e-3

    def test_impedance_mismatch_is_small(self):
        """Air-tissue impedance transmission coefficient ~0.001."""
        result = airborne_coupling_ratio(40.0)
        T = result['impedance_transmission']
        assert 0.0001 < T < 0.01

    def test_coupling_ratio_units(self, canonical_R):
        """Coupling ratio should be dimensionless and < 1."""
        result = airborne_coupling_ratio(80.0, canonical_R)
        assert 0 < result['coupling_total'][0] < 1

    def test_higher_mode_weaker_coupling(self, canonical_R):
        """n = 3 coupling should be weaker than n = 2 at same frequency."""
        r2 = airborne_coupling_ratio(40.0, canonical_R, mode_n=2)
        r3 = airborne_coupling_ratio(40.0, canonical_R, mode_n=3)
        assert r3['p_ratio'][0] < r2['p_ratio'][0]


# ── 3. Tissue displacement ─────────────────────────────────────────────────

class TestTissueDisplacement:

    def test_displacement_positive(self, default_model):
        """Displacement must be positive at any SPL > 0."""
        result = tissue_displacement(40.0, 100.0, model=default_model)
        assert result['xi_um'][0] > 0

    def test_displacement_increases_with_spl(self, default_model):
        """Higher SPL must give larger displacement."""
        r100 = tissue_displacement(40.0, 100.0, model=default_model)
        r120 = tissue_displacement(40.0, 120.0, model=default_model)
        assert r120['xi_um'][0] > r100['xi_um'][0]

    def test_displacement_scales_with_pressure(self, default_model):
        """20 dB increase = 10× pressure → 10× displacement (linear)."""
        r100 = tissue_displacement(40.0, 100.0, model=default_model)
        r120 = tissue_displacement(40.0, 120.0, model=default_model)
        ratio = r120['xi_um'][0] / r100['xi_um'][0]
        assert abs(ratio - 10.0) < 1.0  # within 10% of 10×

    def test_on_resonance_matches_paper1(self, default_model):
        """At n=2 resonance and 120 dB, displacement ≈ 0.18 μm (pressure-based)."""
        f2 = flexural_mode_frequencies_v2(default_model)[2]
        result = tissue_displacement(f2, 120.0, model=default_model, mode_n=2)
        # Paper 1 pressure-based: ~0.18 μm.  This should be of similar order.
        assert 0.01 < result['xi_um'][0] < 5.0

    def test_displacement_at_subbass_is_small(self, default_model):
        """At 40 Hz / 110 dB, displacement should be very small (sub-μm)."""
        result = tissue_displacement(40.0, 110.0, model=default_model)
        assert result['xi_um'][0] < 1.0  # well below 1 μm

    def test_array_frequency_input(self, default_model):
        """Should handle array frequency input."""
        f = np.array([20, 40, 60, 80])
        result = tissue_displacement(f, 115.0, model=default_model)
        assert result['xi_um'].shape == (4,)


# ── 4. Perception threshold model ──────────────────────────────────────────

class TestPerceptionThreshold:

    def test_threshold_positive(self):
        """Perception thresholds must be positive."""
        result = perception_threshold_model(np.array([20, 40, 60]))
        assert np.all(result['a_threshold_ms2'] > 0)
        assert np.all(result['xi_threshold_um'] > 0)

    def test_displacement_threshold_decreases_with_frequency(self):
        """
        Displacement threshold should generally decrease with frequency
        because ω² grows faster than the acceleration threshold.
        """
        f = np.array([4, 20, 80])
        result = perception_threshold_model(f)
        # At 4 Hz, displacement threshold should be larger than at 80 Hz
        assert result['xi_threshold_um'][0] > result['xi_threshold_um'][-1]

    def test_threshold_clamped_to_range(self):
        """Frequencies outside 1-80 Hz should be clamped, not error."""
        result = perception_threshold_model(np.array([0.5, 100.0]))
        assert result['xi_threshold_um'].shape == (2,)
        assert np.all(np.isfinite(result['xi_threshold_um']))


# ── 5. Concert SPL spectra ──────────────────────────────────────────────────

class TestConcertSPLSpectrum:

    def test_known_genres(self):
        """All three genres should return valid spectra."""
        for genre in ['rock', 'edm', 'organ']:
            result = concert_spl_spectrum(40.0, genre)
            assert 80 < result['spl_db'][0] < 130

    def test_edm_louder_than_organ_at_40hz(self):
        """EDM should have higher sub-bass than organ."""
        edm = concert_spl_spectrum(40.0, 'edm')
        org = concert_spl_spectrum(40.0, 'organ')
        assert edm['spl_db'][0] > org['spl_db'][0]

    def test_unknown_genre_raises(self):
        """Unknown genre should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown genre"):
            concert_spl_spectrum(40.0, 'jazz')

    def test_spectrum_shape(self):
        """Array input should return matching array."""
        f = np.array([20, 30, 40, 50, 60])
        result = concert_spl_spectrum(f, 'rock')
        assert result['spl_db'].shape == (5,)


# ── 6. Concert displacement spectrum ───────────────────────────────────────

class TestConcertDisplacementSpectrum:

    def test_default_frequency_range(self, default_model):
        """Default should span 20-80 Hz."""
        result = concert_displacement_spectrum(model=default_model)
        assert result['frequency_hz'][0] == 20.0
        assert result['frequency_hz'][-1] == 80.0

    def test_has_perception_threshold(self, default_model):
        """Result should include perception thresholds."""
        result = concert_displacement_spectrum(
            np.array([30, 50]), 'edm', default_model
        )
        assert 'perception_threshold_um' in result
        assert 'ratio_to_threshold' in result


# ── 7. Coupling transition band ────────────────────────────────────────────

class TestCouplingTransitionBand:

    def test_returns_valid_structure(self, default_model):
        """Should return expected keys."""
        result = coupling_transition_band(default_model)
        assert 'peak_ratio' in result
        assert 'peak_freq_hz' in result
        assert result['peak_ratio'] >= 0


# ── 8. Multi-modal displacement ────────────────────────────────────────────

class TestSumModalDisplacement:

    def test_total_geq_single_mode(self, default_model):
        """Multi-modal sum should be ≥ single-mode displacement."""
        f = np.array([40.0])
        single = tissue_displacement(f, 115.0, model=default_model, mode_n=2)
        multi = _sum_modal_displacement(f, 115.0, model=default_model, n_max=6)
        assert multi['xi_total_um'][0] >= single['xi_um'][0] - 1e-15


# ── 9. Dimensional & physical consistency ──────────────────────────────────

class TestPhysicalConsistency:

    def test_displacement_has_length_units(self, default_model):
        """xi_m should be in metres (order 1e-12 to 1e-6 at realistic SPLs)."""
        result = tissue_displacement(40.0, 110.0, model=default_model)
        xi = result['xi_m'][0]
        assert 1e-15 < xi < 1e-3

    def test_ka_dimensionless(self, canonical_R):
        """ka should be dimensionless and of order 0.01-1 for 1-100 Hz."""
        ka = ka_parameter(np.array([1.0, 100.0]), canonical_R)
        assert np.all(ka > 0)
        assert np.all(ka < 1)

    def test_zero_spl_gives_zero_displacement(self, default_model):
        """At 0 dB SPL (20 μPa), displacement should be negligible."""
        result = tissue_displacement(40.0, 0.0, model=default_model)
        assert result['xi_um'][0] < 1e-6  # well below any threshold
