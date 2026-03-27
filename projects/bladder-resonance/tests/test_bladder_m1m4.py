"""Tests for bladder model M1 (decomposition) and M4 (sensitivity) functions."""
import sys, os, numpy as np, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bladder_model import (
    bladder_radius_from_volume, bladder_wall_thickness, bladder_elastic_modulus,
    intravesical_pressure, make_bladder_model, stiffness_decomposition,
    decomposition_vs_volume, find_f2_minimum, sensitivity_analysis,
    minimum_shift_analysis, SENSITIVITY_PARAMS,
)

class TestStiffnessDecomposition:
    def test_returns_all_keys(self):
        d = stiffness_decomposition(300.0)
        for k in ['K_bend', 'K_memb', 'K_P', 'K_total', 'm_wall', 'm_fluid', 'm_eff', 'f_n']:
            assert k in d

    def test_stiffness_sum(self):
        d = stiffness_decomposition(300.0)
        assert abs(d['K_total'] - (d['K_bend'] + d['K_memb'] + d['K_P'])) < 1e-6

    def test_mass_sum(self):
        d = stiffness_decomposition(300.0)
        assert abs(d['m_eff'] - (d['m_wall'] + d['m_fluid'])) < 1e-10

    def test_frequency_positive(self):
        for v in [50, 100, 200, 300, 500]:
            assert stiffness_decomposition(float(v))['f_n'] > 0

    def test_frequency_matches_model(self):
        from src.analytical.natural_frequency_v2 import flexural_mode_frequencies_v2
        for v in [100, 200, 300, 400]:
            d = stiffness_decomposition(float(v))
            model = make_bladder_model(float(v))
            freqs = flexural_mode_frequencies_v2(model, n_max=2)
            assert abs(d['f_n'] - freqs[2]) < 0.01

    def test_prestress_dominates_at_high_volume(self):
        d = stiffness_decomposition(500.0)
        assert d['K_P'] / d['K_total'] > 0.5

    def test_fluid_mass_dominance(self):
        for v in [50, 100, 200, 300, 500]:
            d = stiffness_decomposition(float(v))
            assert d['m_fluid'] > d['m_wall']

    def test_overrides_E(self):
        d_base = stiffness_decomposition(300.0)
        d_soft = stiffness_decomposition(300.0, E=5e3)
        assert d_soft['E'] == 5e3
        assert d_soft['R'] == d_base['R']
        assert d_soft['K_memb'] < d_base['K_memb']

    def test_overrides_h(self):
        d_base = stiffness_decomposition(300.0)
        d_thick = stiffness_decomposition(300.0, h=10e-3)
        assert d_thick['h'] == 10e-3
        assert d_thick['m_wall'] > d_base['m_wall']

class TestDecompositionVsVolume:
    def test_returns_arrays(self):
        data = decomposition_vs_volume(volumes=np.linspace(50, 500, 10))
        assert len(data['f_n']) == 10

    def test_monotonic_mass(self):
        data = decomposition_vs_volume()
        assert np.all(np.diff(data['m_eff']) > 0)

class TestFindF2Minimum:
    def test_minimum_exists(self):
        mi = find_f2_minimum()
        assert mi['V_min'] is not None and mi['f_min'] > 0

    def test_minimum_in_range(self):
        mi = find_f2_minimum()
        assert 100 < mi['V_min'] < 300

    def test_frequency_at_minimum(self):
        mi = find_f2_minimum()
        assert 10 < mi['f_min'] < 15

    def test_analytic_crossing_agrees(self):
        mi = find_f2_minimum()
        assert mi['V_analytic'] is not None
        assert abs(mi['V_analytic'] - mi['V_min']) < 5

    def test_is_indeed_minimum(self):
        mi = find_f2_minimum()
        assert stiffness_decomposition(mi['V_min'] - 30)['f_n'] > mi['f_min']
        assert stiffness_decomposition(mi['V_min'] + 30)['f_n'] > mi['f_min']

class TestSensitivityAnalysis:
    def test_returns_all_params(self):
        sens = sensitivity_analysis()
        for p in SENSITIVITY_PARAMS:
            assert p in sens

    def test_baseline_consistent(self):
        sens = sensitivity_analysis()
        f_bases = [v['f_base'] for v in sens.values()]
        assert all(abs(f - f_bases[0]) < 1e-10 for f in f_bases)

    def test_E_dominates(self):
        sens = sensitivity_analysis()
        E_delta = sens['E']['delta_f']
        for p, v in sens.items():
            if p != 'E':
                assert v['delta_f'] <= E_delta

    def test_eta_negligible(self):
        assert sensitivity_analysis()['loss_tangent']['delta_f'] < 0.1

class TestMinimumShiftAnalysis:
    def test_returns_base(self):
        assert '_base' in minimum_shift_analysis()

    def test_all_params_present(self):
        shifts = minimum_shift_analysis()
        for p in SENSITIVITY_PARAMS:
            assert p + '_lo' in shifts and p + '_hi' in shifts

    def test_E_shifts_most(self):
        shifts = minimum_shift_analysis()
        E_shift = abs(shifts['E_hi']['V_min'] - shifts['E_lo']['V_min'])
        for p in SENSITIVITY_PARAMS:
            if p != 'E':
                assert abs(shifts[p + '_hi']['V_min'] - shifts[p + '_lo']['V_min']) <= E_shift

class TestGeometry:
    def test_radius_increases(self):
        assert bladder_radius_from_volume(500) > bladder_radius_from_volume(50)

    def test_thickness_decreases(self):
        assert bladder_wall_thickness(300) < bladder_wall_thickness(50)

    def test_modulus_increases(self):
        assert bladder_elastic_modulus(500) > bladder_elastic_modulus(50)

    def test_make_model_overrides(self):
        model = make_bladder_model(300, E=1e6, nu=0.40)
        assert model.E == 1e6 and model.nu == 0.40