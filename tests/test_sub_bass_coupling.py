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
    floor_vibration_displacement,
    pathway_comparison,
    near_field_enhancement,
    pew_bending_resonance,
    monte_carlo_pathway_uq,
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
        """At n=2 resonance and 120 dB, displacement ≈ 0.028 μm (energy-consistent)."""
        f2 = flexural_mode_frequencies_v2(default_model)[2]
        result = tissue_displacement(f2, 120.0, model=default_model, mode_n=2)
        # Paper 1 energy-consistent: ~0.028 μm (Breit-Wigner corrected).
        assert 0.001 < result['xi_um'][0] < 0.5

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


# ── 10. Floor vibration pathway (corrected formula) ────────────────────────

class TestFloorVibrationDisplacement:

    def test_positive_displacement(self):
        """Floor pathway should give positive displacement."""
        result = floor_vibration_displacement(40.0, 115.0)
        assert result['body_displacement_um'][0] > 0

    def test_increases_with_spl(self):
        """Higher SPL should produce larger floor displacement."""
        r100 = floor_vibration_displacement(40.0, 100.0)
        r120 = floor_vibration_displacement(40.0, 120.0)
        assert r120['body_displacement_um'][0] > r100['body_displacement_um'][0]

    def test_array_input(self):
        """Should accept array frequencies."""
        f = np.array([20, 40, 60, 80])
        result = floor_vibration_displacement(f, 115.0)
        assert result['body_displacement_um'].shape == (4,)

    def test_floor_dominates_airborne(self):
        """Floor pathway should give much larger displacement than airborne."""
        f = np.array([40.0])
        floor = floor_vibration_displacement(f, 115.0)
        air = tissue_displacement(f, 115.0)
        assert floor['body_displacement_um'][0] > air['xi_um'][0] * 5

    def test_transmissibility_scaling(self):
        """Displacement should scale with transmissibility."""
        r1 = floor_vibration_displacement(40.0, 115.0, body_transmissibility=1.0)
        r2 = floor_vibration_displacement(40.0, 115.0, body_transmissibility=2.0)
        ratio = r2['body_displacement_um'][0] / r1['body_displacement_um'][0]
        assert abs(ratio - 2.0) < 0.01

    # --- NEW TESTS: dimensional consistency and corrected formula ---

    def test_floor_velocity_units_are_ms(self):
        """
        Dimensional check: v_floor = sqrt(P / (2 zeta omega m)) must
        have units of m/s.

        Hand calculation at 40 Hz, 115 dB:
          p_inc = 20e-6 * 10^(115/20) = 11.247 Pa
          I = p^2 / (2 * 1.225 * 343) = 0.1506 W/m^2
          P_floor = I * 100 * 0.01 = 0.1506 W
          omega = 2*pi*40 = 251.33 rad/s
          m_total = 200 * 100 = 20000 kg
          v = sqrt(0.1506 / (2 * 0.03 * 251.33 * 20000))
            = sqrt(0.1506 / 301596) = sqrt(4.994e-7) = 7.067e-4 m/s
        """
        result = floor_vibration_displacement(
            40.0, 115.0,
            floor_radiation_efficiency=0.01,
            floor_area=100.0,
            floor_mass_per_area=200.0,
            zeta_floor=0.03,
        )
        v = result['floor_velocity_ms'][0]
        # Check against hand calculation
        assert abs(v - 7.067e-4) / 7.067e-4 < 0.01  # within 1%

    def test_displacement_increases_with_lower_damping(self):
        """Lower floor damping → more displacement (energy trapped longer)."""
        r_low = floor_vibration_displacement(40.0, 115.0, zeta_floor=0.02)
        r_high = floor_vibration_displacement(40.0, 115.0, zeta_floor=0.05)
        assert r_low['body_displacement_um'][0] > r_high['body_displacement_um'][0]

    def test_damping_scaling_sqrt(self):
        """v scales as 1/sqrt(zeta), so halving zeta should increase v by sqrt(2)."""
        r1 = floor_vibration_displacement(40.0, 115.0, zeta_floor=0.04)
        r2 = floor_vibration_displacement(40.0, 115.0, zeta_floor=0.02)
        ratio = r2['floor_velocity_ms'][0] / r1['floor_velocity_ms'][0]
        expected = np.sqrt(0.04 / 0.02)  # = sqrt(2)
        assert abs(ratio - expected) / expected < 0.001

    def test_hand_calculation_body_displacement(self):
        """
        Full hand calculation at 40 Hz, 115 dB, zeta=0.03:
          v_floor = 7.067e-4 m/s  (from test above)
          omega = 251.33 rad/s
          xi_floor = v / omega = 2.812e-6 m = 2.812 um
          xi_body = xi_floor * 1.8 = 5.062 um
        """
        result = floor_vibration_displacement(
            40.0, 115.0,
            body_transmissibility=1.8,
            zeta_floor=0.03,
        )
        xi = result['body_displacement_um'][0]
        assert abs(xi - 5.06) / 5.06 < 0.02  # within 2%

    def test_zeta_floor_returned_in_result(self):
        """Result dict should include zeta_floor for traceability."""
        result = floor_vibration_displacement(40.0, 115.0, zeta_floor=0.04)
        assert result['zeta_floor'] == 0.04

    def test_floor_exceeds_threshold_at_peak_edm(self):
        """At 40 Hz / 115 dB, corrected floor pathway should exceed threshold."""
        result = floor_vibration_displacement(40.0, 115.0, zeta_floor=0.03)
        thresh = perception_threshold_model(np.array([40.0]))
        # floor must exceed threshold (this is the key F1-fix consequence)
        assert result['body_displacement_um'][0] > thresh['xi_threshold_um'][0]


# ── 11. Pathway comparison ─────────────────────────────────────────────────

class TestPathwayComparison:

    def test_returns_all_keys(self, default_model):
        """Should return all expected pathway keys."""
        result = pathway_comparison(np.array([40.0]), 115.0, default_model)
        for key in ['airborne_um', 'floor_um', 'threshold_um',
                     'airborne_ratio', 'floor_ratio', 'floor_to_airborne_ratio']:
            assert key in result

    def test_floor_exceeds_airborne(self, default_model):
        """Floor pathway should dominate airborne at 40 Hz."""
        result = pathway_comparison(np.array([40.0]), 115.0, default_model)
        assert result['floor_um'][0] > result['airborne_um'][0]

    def test_airborne_below_threshold(self, default_model):
        """Airborne ratio should be well below 1 at concert SPLs."""
        result = pathway_comparison(np.array([40.0]), 115.0, default_model)
        assert result['airborne_ratio'][0] < 0.1

    def test_floor_exceeds_threshold(self, default_model):
        """With corrected formula, floor pathway exceeds perception threshold."""
        result = pathway_comparison(np.array([40.0]), 115.0, default_model)
        assert result['floor_ratio'][0] > 1.0

    def test_floor_to_airborne_ratio_order_of_magnitude(self, default_model):
        """Floor/airborne ratio should be ~1000-5000× with corrected formula."""
        result = pathway_comparison(np.array([40.0]), 115.0, default_model)
        ratio = result['floor_to_airborne_ratio'][0]
        assert 500 < ratio < 10000

    def test_array_frequencies(self, default_model):
        """Should work with array of frequencies."""
        f = np.array([20, 40, 60, 80])
        result = pathway_comparison(f, 115.0, default_model)
        assert result['airborne_um'].shape == (4,)
        assert result['floor_um'].shape == (4,)

    def test_zeta_floor_passthrough(self, default_model):
        """zeta_floor parameter should affect floor results."""
        r1 = pathway_comparison(np.array([40.0]), 115.0, default_model, zeta_floor=0.02)
        r2 = pathway_comparison(np.array([40.0]), 115.0, default_model, zeta_floor=0.05)
        assert r1['floor_um'][0] > r2['floor_um'][0]


# ── 12. Near-field enhancement ─────────────────────────────────────────────

class TestNearFieldEnhancement:

    def test_enhancement_positive(self):
        """Near-field enhancement should be positive."""
        result = near_field_enhancement(np.array([40.0]), 1.0)
        assert result['enhancement_dB'][0] > 0

    def test_decreases_with_distance(self):
        """Enhancement should decrease with distance."""
        r_near = near_field_enhancement(np.array([40.0]), 0.5)
        r_far = near_field_enhancement(np.array([40.0]), 5.0)
        assert r_near['enhancement_dB'][0] > r_far['enhancement_dB'][0]

    def test_far_field_negligible(self):
        """At large distances, enhancement should be negligible."""
        result = near_field_enhancement(np.array([40.0]), 50.0)
        assert result['enhancement_dB'][0] < 0.1

    def test_significant_at_half_lambda_over_2pi(self):
        """At λ/(2π), enhancement should be ~3 dB."""
        f = np.array([40.0])
        d = 343.0 / (40.0 * 2 * np.pi)  # λ/(2π) at 40 Hz
        result = near_field_enhancement(f, d)
        assert 2.5 < result['enhancement_dB'][0] < 3.5

    def test_array_input(self):
        """Should accept array frequencies."""
        f = np.array([20, 40, 60, 80])
        result = near_field_enhancement(f, 1.0)
        assert result['enhancement_dB'].shape == (4,)

    def test_low_freq_stronger(self):
        """Near-field enhancement should be stronger at lower frequencies."""
        r20 = near_field_enhancement(np.array([20.0]), 1.0)
        r80 = near_field_enhancement(np.array([80.0]), 1.0)
        assert r20['enhancement_dB'][0] > r80['enhancement_dB'][0]


# ── 13. Pew bending resonance ──────────────────────────────────────────────

class TestPewBendingResonance:

    def test_resonance_in_expected_range(self):
        """First mode of a 2.5m pew should be ~10–20 Hz."""
        result = pew_bending_resonance(length_m=2.5)
        assert 5 < result['f1_hz'] < 30

    def test_shorter_pew_higher_frequency(self):
        """Shorter pew should have higher resonance."""
        r_short = pew_bending_resonance(length_m=2.0)
        r_long = pew_bending_resonance(length_m=3.0)
        assert r_short['f1_hz'] > r_long['f1_hz']

    def test_modes_ascending(self):
        """Higher modes should have higher frequencies."""
        result = pew_bending_resonance(length_m=2.5)
        assert result['f1_hz'] < result['f2_hz'] < result['f3_hz']

    def test_clamped_higher_than_simply_supported(self):
        """Clamped boundary should give higher frequencies."""
        r_ss = pew_bending_resonance(length_m=2.5, boundary='simply_supported')
        r_cl = pew_bending_resonance(length_m=2.5, boundary='clamped')
        assert r_cl['f1_hz'] > r_ss['f1_hz']

    def test_invalid_boundary_raises(self):
        """Invalid boundary should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown boundary"):
            pew_bending_resonance(boundary='free')

    def test_description_string(self):
        """Should include a human-readable description."""
        result = pew_bending_resonance(length_m=2.5)
        assert 'Hz' in result['description']
        assert '2.5' in result['description']


# ── 14. Energy-consistent displacement regression ──────────────────────────

class TestEnergyConsistentRegression:
    """Regression tests for the corrected energy-consistent displacement."""

    def test_displacement_order_of_magnitude(self, default_model):
        """At 115 dB and 40 Hz, displacement ~0.002 μm (energy-consistent)."""
        result = tissue_displacement(40.0, 115.0, model=default_model)
        assert 1e-4 < result['xi_um'][0] < 0.1

    def test_ratio_to_threshold_at_40hz(self, default_model):
        """At 40 Hz / 115 dB, ratio ~0.35% of threshold."""
        result = tissue_displacement(np.array([40.0]), 115.0, model=default_model)
        thresh = perception_threshold_model(np.array([40.0]))
        ratio = result['xi_um'][0] / thresh['xi_threshold_um'][0]
        assert 0.001 < ratio < 0.05  # ~0.35%, not the old ~0.003%

    def test_not_pressure_based(self, default_model):
        """Energy-consistent values should be ~6.5× smaller than old pressure-based."""
        # The old pressure-based on-resonance at 120 dB was ~0.18 μm
        # Energy-consistent should be ~0.028 μm (Breit-Wigner corrected)
        f2 = flexural_mode_frequencies_v2(default_model)[2]
        result = tissue_displacement(f2, 120.0, model=default_model)
        assert result['xi_um'][0] < 0.05  # well below old 0.18 μm


# ── 15. Monte Carlo UQ ─────────────────────────────────────────────────────

class TestMonteCarloUQ:
    """Tests for Monte Carlo uncertainty quantification."""

    def test_returns_expected_keys(self):
        """MC result should have all required keys."""
        mc = monte_carlo_pathway_uq(n_samples=100)
        assert 'summary' in mc
        assert 'floor_to_airborne_ratio' in mc
        assert len(mc['floor_to_airborne_ratio']) == 100
        for k in ['floor_to_airborne', 'floor_over_threshold',
                   'airborne_over_threshold']:
            assert k in mc['summary']
            for stat in ['p5', 'p50', 'p95', 'mean', 'std']:
                assert stat in mc['summary'][k]

    def test_floor_always_dominates_airborne(self):
        """In all MC samples, floor > airborne."""
        mc = monte_carlo_pathway_uq(n_samples=500, seed=123)
        assert np.all(mc['floor_to_airborne_ratio'] > 1.0)

    def test_reproducible_with_seed(self):
        """Same seed should give same results."""
        mc1 = monte_carlo_pathway_uq(n_samples=50, seed=42)
        mc2 = monte_carlo_pathway_uq(n_samples=50, seed=42)
        np.testing.assert_array_equal(
            mc1['floor_to_airborne_ratio'],
            mc2['floor_to_airborne_ratio'],
        )

    def test_wider_range_increases_spread(self):
        """Wider parameter ranges should increase output spread."""
        mc_narrow = monte_carlo_pathway_uq(
            n_samples=500, E_range=(0.09e6, 0.11e6),
            zeta_floor_range=(0.029, 0.031), spl_delta=0.5,
        )
        mc_wide = monte_carlo_pathway_uq(
            n_samples=500, E_range=(0.05e6, 0.15e6),
            zeta_floor_range=(0.02, 0.05), spl_delta=3.0,
        )
        std_narrow = mc_narrow['summary']['floor_to_airborne']['std']
        std_wide = mc_wide['summary']['floor_to_airborne']['std']
        assert std_wide > std_narrow