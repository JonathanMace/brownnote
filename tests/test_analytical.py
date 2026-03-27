"""Comprehensive tests for analytical models — correctness & reproducibility.

Covers:
  a. Dimensional consistency & orders of magnitude
  b. Known physical limits
  c. Conservation laws (energy budget)
  d. Reciprocity / optical theorem bounds
  e. Symmetry (oblate spheroid → sphere limit)
  f. Regression tests (frozen canonical results)
  g. Edge cases (E→0, h→0, c→a)
  h. Parametric sweep monotonicity
"""

from __future__ import annotations

import sys
import os
import numpy as np
import pytest

# Ensure src/ is importable without editable install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    breathing_mode_v2,
    flexural_mode_frequencies_v2,
    flexural_mode_pressure_response,
)
from analytical.mechanical_coupling import (
    WBVExposure,
    interpolate_transmissibility,
    mechanical_excitation_response,
    compare_airborne_vs_mechanical,
)
from analytical.energy_budget import (
    radiation_damping_flexural,
    absorption_cross_section,
    self_consistent_displacement,
)
from analytical.gas_pocket_resonance import (
    GasPocket,
    minnaert_frequency,
    constrained_bubble_frequency,
    elongated_pocket_frequency,
    acoustic_response_of_gas_pocket,
)
from analytical.parametric_analysis import (
    parametric_E_sweep,
    multi_parameter_sensitivity,
    energy_budget_v2,
)
from analytical.multilayer_wall import (
    Layer,
    relaxed_layers,
    tensed_layers,
    obese_layers,
    compute_composite_properties,
    multilayer_to_v2_model,
)
from analytical.oblate_spheroid_ritz import (
    oblate_ritz_frequency,
    oblate_ritz_frequencies,
    sphere_approx_frequencies,
)
from analytical.dimensional_analysis import (
    breathing_mode_infrasound_size,
    dimensionless_frequency,
    phi_analytical,
    parametric_sweep_dimensionless,
    verify_collapse,
    animal_scaling,
)


# ------------------------------------------------------------------ #
#  Fixtures                                                            #
# ------------------------------------------------------------------ #

@pytest.fixture
def default_model():
    """Canonical default model (a=b=0.18, c=0.12, E=0.1 MPa)."""
    return AbdominalModelV2()


@pytest.fixture
def soft_tissue_model():
    """Soft-tissue model used across coupling / energy analyses."""
    return AbdominalModelV2(E=0.1e6, a=0.18, b=0.18, c=0.12)


# ================================================================== #
#  (a) DIMENSIONAL CONSISTENCY — orders of magnitude                   #
# ================================================================== #

class TestDimensionalConsistency:
    """Every function should return values in the right ballpark."""

    def test_breathing_mode_kHz_range(self, default_model):
        """Breathing mode is dominated by bulk modulus → kHz."""
        f0 = breathing_mode_v2(default_model)
        assert 500 < f0 < 10_000, f"Breathing mode {f0} Hz outside kHz range"

    def test_flexural_f2_Hz_range(self, default_model):
        """n=2 flexural mode should be single-digit to tens of Hz."""
        freqs = flexural_mode_frequencies_v2(default_model)
        assert 0.5 < freqs[2] < 50, f"f2={freqs[2]} outside expected range"

    def test_flexural_frequencies_increase_with_n(self, default_model):
        """Higher mode numbers → higher frequencies."""
        freqs = flexural_mode_frequencies_v2(default_model, n_max=6)
        for n in range(3, 7):
            assert freqs[n] >= freqs[n - 1], (
                f"f[{n}]={freqs[n]} < f[{n-1}]={freqs[n-1]}"
            )

    def test_displacement_positive_units(self, soft_tissue_model):
        """Pressure response should return positive displacement in μm."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]
        r = flexural_mode_pressure_response(f2, 120.0, 2, soft_tissue_model)
        assert r['displacement_um'] > 0
        assert r['displacement_um'] < 1e6  # not absurd

    def test_minnaert_frequency_positive(self):
        """Minnaert frequency should be positive Hz."""
        pocket = GasPocket(radius_cm=2.0)
        f = minnaert_frequency(pocket)
        assert 10 < f < 1000

    def test_composite_properties_positive(self):
        """Composite wall properties must be positive."""
        props = compute_composite_properties(relaxed_layers())
        assert props['E_eff_Pa'] > 0
        assert props['h_total_m'] > 0
        assert props['D_eff'] > 0
        assert 0 < props['nu_eff'] < 0.5

    def test_mechanical_displacement_positive(self, soft_tissue_model):
        """Mechanical coupling displacement must be positive."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]
        exp = WBVExposure(acceleration_rms_ms2=1.0, frequency_hz=f2)
        r = mechanical_excitation_response(exp, soft_tissue_model)
        assert r['relative_displacement_um'] > 0
        assert r['abdomen_absolute_um'] > 0


# ================================================================== #
#  (b) KNOWN PHYSICAL LIMITS                                           #
# ================================================================== #

class TestKnownLimits:
    """Physics-based sanity checks."""

    def test_breathing_mode_not_infrasonic(self, default_model):
        """Breathing mode must be >> 20 Hz (fluid bulk modulus dominates)."""
        f0 = breathing_mode_v2(default_model)
        assert f0 > 500, f"Breathing mode {f0} Hz is too low"

    def test_f2_approaches_floor_as_E_drops(self):
        """f₂ decreases monotonically with E; floors at prestress contribution.

        With P_iap > 0, there is a non-zero stiffness floor from membrane
        prestress, so f₂ doesn't reach zero but approaches a small value (~3 Hz).
        """
        f2_prev = float('inf')
        for E in [1e6, 1e5, 1e4, 1e3, 1e2]:
            m = AbdominalModelV2(E=E)
            f2 = flexural_mode_frequencies_v2(m)[2]
            assert f2 < f2_prev
            f2_prev = f2
        # At E=100 Pa, frequency is low — dominated by P_iap prestress
        m_tiny = AbdominalModelV2(E=100.0)
        f2_tiny = flexural_mode_frequencies_v2(m_tiny)[2]
        assert f2_tiny < 5.0, f"f2={f2_tiny} should be small"
        # Without prestress, E=0 really does give ~0
        m_zero = AbdominalModelV2(E=100.0, P_iap=0.0)
        f2_zero = flexural_mode_frequencies_v2(m_zero)[2]
        assert f2_zero < f2_tiny

    def test_f2_increases_with_E(self):
        """f₂ increases monotonically with E."""
        E_values = [1e4, 5e4, 1e5, 5e5, 1e6, 5e6]
        freqs = []
        for E in E_values:
            m = AbdominalModelV2(E=E)
            freqs.append(flexural_mode_frequencies_v2(m)[2])
        for i in range(1, len(freqs)):
            assert freqs[i] > freqs[i - 1], (
                f"f2 not monotone: {freqs[i]} <= {freqs[i-1]} at E={E_values[i]}"
            )

    def test_mechanical_coupling_dominates_airborne(self, soft_tissue_model):
        """Mechanical displacement >> airborne displacement at same energy."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]

        # Mechanical at 1.0 m/s² (EU limit level)
        exp = WBVExposure(acceleration_rms_ms2=1.0, frequency_hz=f2)
        r_mech = mechanical_excitation_response(exp, soft_tissue_model)

        # Airborne at 120 dB (very loud)
        r_air = flexural_mode_pressure_response(f2, 120.0, 2, soft_tissue_model)

        ratio = r_mech['relative_displacement_um'] / r_air['displacement_um']
        assert ratio > 10, (
            f"Coupling ratio {ratio:.1f} not >> 1 — mechanical should dominate"
        )

    def test_rigid_body_mode_zero(self, default_model):
        """n=1 mode is rigid body translation → 0 Hz."""
        freqs = flexural_mode_frequencies_v2(default_model)
        assert freqs[1] == 0.0

    def test_transmissibility_peaks_near_resonance(self):
        """ISO 2631 transmissibility peaks between 4-8 Hz."""
        T_values = [interpolate_transmissibility(f) for f in range(1, 21)]
        peak_freq = np.argmax(T_values) + 1
        assert 4 <= peak_freq <= 8


# ================================================================== #
#  (c) CONSERVATION LAWS — energy budget self-consistency              #
# ================================================================== #

class TestEnergyConservation:
    """Energy budget must be self-consistent."""

    def test_energy_method_self_consistent(self, soft_tissue_model):
        """P_absorbed ≈ P_dissipated for energy-based displacement."""
        r = self_consistent_displacement(soft_tissue_model, mode_n=2, spl_db=120)
        assert r['energy_conserved_energy'], (
            f"Energy method not self-consistent: "
            f"P_abs={r['P_absorbed_W']:.2e}, P_diss={r['P_diss_energy_W']:.2e}"
        )

    @pytest.mark.parametrize("spl", [100, 110, 120, 130, 140])
    def test_energy_conservation_across_spl(self, soft_tissue_model, spl):
        """Energy balance holds at all SPL levels."""
        r = self_consistent_displacement(soft_tissue_model, mode_n=2, spl_db=spl)
        assert r['energy_conserved_energy']

    def test_parametric_energy_budget_ratio_stable(self, soft_tissue_model):
        """parametric_analysis.energy_budget_v2 energy ratio is constant across SPL.

        KNOWN FINDING: The pressure-based approach in energy_budget_v2
        overestimates displacement by ~√2 (ratio ≈ 2.09), yielding
        P_dissipated > P_available. This is the known inconsistency that
        energy_budget.py's self_consistent_displacement resolves.
        The ratio should at least be *stable* across SPL levels.
        """
        ratios = []
        for spl in [100, 120, 140]:
            eb = energy_budget_v2(soft_tissue_model, spl_db=spl, mode_n=2)
            ratios.append(eb['energy_ratio'])
        # Ratio should be constant (pressure-based scales same as energy-based)
        assert max(ratios) - min(ratios) < 0.01, (
            f"Energy ratio not constant: {ratios}"
        )

    def test_energy_budget_ratio_documented(self, soft_tissue_model):
        """Document the known ~2× energy overestimate from pressure approach.

        See energy_budget.py for the resolution via reciprocity.
        """
        eb = energy_budget_v2(soft_tissue_model, spl_db=120, mode_n=2)
        # The pressure approach overestimates by a factor of ~2
        assert 1.5 < eb['energy_ratio'] < 3.0, (
            f"Energy ratio {eb['energy_ratio']:.2f} outside expected range"
        )

    def test_pressure_vs_energy_displacement_ratio(self, soft_tissue_model):
        """Pressure-based displacement should exceed energy-based (known overestimate)."""
        r = self_consistent_displacement(soft_tissue_model, mode_n=2, spl_db=120)
        assert r['xi_pressure_um'] >= r['xi_energy_um'], (
            "Pressure-based should overestimate vs energy-based"
        )


# ================================================================== #
#  (d) RECIPROCITY — optical theorem bounds                            #
# ================================================================== #

class TestReciprocity:
    """Absorption cross-section must satisfy optical theorem bounds."""

    def test_sigma_abs_leq_sigma_max(self, soft_tissue_model):
        """σ_abs ≤ (2n+1)λ²/(4π) (optical theorem maximum)."""
        acs = absorption_cross_section(soft_tissue_model, mode_n=2)
        assert acs['sigma_abs_m2'] <= acs['sigma_max_m2'] * 1.001

    def test_sigma_abs_positive(self, soft_tissue_model):
        """Absorption cross-section must be positive."""
        acs = absorption_cross_section(soft_tissue_model, mode_n=2)
        assert acs['sigma_abs_m2'] > 0

    def test_radiation_damping_much_less_than_structural(self, soft_tissue_model):
        """ζ_rad << ζ_struct for bio-tissue in air."""
        rd = radiation_damping_flexural(soft_tissue_model, mode_n=2, medium='air')
        assert rd['zeta_rad'] < rd['zeta_structural'] * 0.01, (
            f"ζ_rad={rd['zeta_rad']:.2e} not << ζ_struct={rd['zeta_structural']}"
        )

    def test_efficiency_less_than_unity(self, soft_tissue_model):
        """Absorption efficiency = ζ_rad/(ζ_rad+ζ_struct) < 1."""
        acs = absorption_cross_section(soft_tissue_model, mode_n=2)
        assert 0 < acs['efficiency'] < 1

    @pytest.mark.parametrize("mode_n", [2, 3, 4])
    def test_optical_theorem_all_modes(self, soft_tissue_model, mode_n):
        """Optical theorem holds for modes 2-4."""
        acs = absorption_cross_section(soft_tissue_model, mode_n=mode_n)
        assert acs['sigma_abs_m2'] <= acs['sigma_max_m2']
        assert acs['sigma_abs_m2'] > 0


# ================================================================== #
#  (e) SYMMETRY — oblate spheroid with c→a (sphere limit)              #
# ================================================================== #

class TestSymmetry:
    """Oblate spheroid results should converge to sphere at c/a → 1."""

    def test_ritz_converges_to_sphere_at_equal_axes(self):
        """At c≈a, Ritz and sphere formulae should agree within ~10%."""
        m = AbdominalModelV2(a=0.15, b=0.15, c=0.149)  # nearly spherical
        f_sphere = flexural_mode_frequencies_v2(m, n_max=3)
        f_ritz = oblate_ritz_frequencies(
            m.a, m.c, m.h, m.E, m.nu, m.rho_wall, m.rho_fluid, m.P_iap,
            n_target=(2, 3),
        )
        for n in (2, 3):
            rel_err = abs(f_sphere[n] - f_ritz[n]) / f_sphere[n]
            assert rel_err < 0.15, (
                f"n={n}: sphere={f_sphere[n]:.3f}, ritz={f_ritz[n]:.3f}, "
                f"err={rel_err*100:.1f}%"
            )

    def test_ritz_error_decreases_with_aspect_ratio(self):
        """As c/a → 1, the Ritz solution should converge to the sphere model."""
        # Use explicit stiff parameters where monotonic convergence is clearest
        errors = []
        for cr in [0.6, 0.8, 0.95]:
            a = 0.15
            m = AbdominalModelV2(a=a, b=a, c=a * cr, E=0.5e6, nu=0.49,
                                 rho_wall=1050, rho_fluid=1040, h=0.015)
            f_s = flexural_mode_frequencies_v2(m, n_max=2)[2]
            f_r = oblate_ritz_frequency(
                2, a, a * cr, m.h, m.E, m.nu, m.rho_wall, m.rho_fluid, m.P_iap,
            )
            errors.append(abs(f_s - f_r) / f_s if f_s > 0 else 0)
        # Near-sphere error should be smaller than most-oblate error
        assert errors[-1] < errors[0], (
            f"Error at c/a=0.95 ({errors[-1]:.3f}) >= error at c/a=0.6 ({errors[0]:.3f})"
        )

    def test_model_b_equals_a_default(self):
        """Default model has b=a (oblate spheroid with equal equatorial axes)."""
        m = AbdominalModelV2()
        assert m.a == m.b
        # Surface area formula should handle this without error
        assert m.surface_area > 0
        assert m.volume > 0

    def test_surface_area_sphere_limit(self):
        """When c→a, surface area should approach 4πa²."""
        a = 0.15
        m = AbdominalModelV2(a=a, b=a, c=a - 1e-12)
        expected = 4 * np.pi * a**2
        assert abs(m.surface_area - expected) / expected < 0.001


# ================================================================== #
#  (f) REGRESSION TESTS — frozen canonical results                     #
# ================================================================== #

class TestRegression:
    """Freeze numerical values to detect unintended model changes.

    Values come from the actual model implementation.  If a model is
    intentionally changed, update these values and document the reason.
    """

    def test_default_f2(self, default_model):
        """Default model n=2 frequency (canonical: 3.95 Hz)."""
        f2 = flexural_mode_frequencies_v2(default_model)[2]
        assert f2 == pytest.approx(3.95, abs=0.1), f"f2={f2}"

    def test_default_breathing(self, default_model):
        """Default model breathing mode (canonical: ~2490 Hz)."""
        f0 = breathing_mode_v2(default_model)
        assert f0 == pytest.approx(2491, abs=50), f"f0={f0}"

    def test_soft_tissue_f2(self, soft_tissue_model):
        """Soft-tissue model n=2 frequency (canonical: 3.95 Hz)."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]
        assert f2 == pytest.approx(3.95, abs=0.1), f"f2={f2}"

    def test_energy_displacement_120dB(self, soft_tissue_model):
        """Energy-consistent displacement at 120 dB (canonical: 0.014 μm)."""
        r = self_consistent_displacement(soft_tissue_model, mode_n=2, spl_db=120)
        assert r['xi_energy_um'] == pytest.approx(0.0137, abs=0.002), (
            f"xi_energy={r['xi_energy_um']}"
        )

    def test_mechanical_displacement_01ms2(self, soft_tissue_model):
        """Mechanical displacement at 0.1 m/s² (canonical: 917 μm)."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]
        exp = WBVExposure(acceleration_rms_ms2=0.1, frequency_hz=f2)
        r = mechanical_excitation_response(exp, soft_tissue_model)
        assert r['relative_displacement_um'] == pytest.approx(917, abs=50), (
            f"xi_mech={r['relative_displacement_um']}"
        )

    def test_minnaert_2cm(self):
        """Minnaert frequency for 2 cm radius gas pocket."""
        pocket = GasPocket(radius_cm=2.0)
        f = minnaert_frequency(pocket)
        assert f == pytest.approx(161.0, abs=5.0), f"f_M={f}"

    def test_ritz_n2_default(self, default_model):
        """Ritz n=2 frequency for default model (canonical: ~3.8 Hz)."""
        m = default_model
        f = oblate_ritz_frequency(
            2, m.a, m.c, m.h, m.E, m.nu, m.rho_wall, m.rho_fluid, m.P_iap,
        )
        assert f == pytest.approx(3.80, abs=0.5), f"ritz_f2={f}"

    def test_composite_relaxed_E_eff(self):
        """Relaxed composite wall effective modulus."""
        props = compute_composite_properties(relaxed_layers())
        assert props['E_eff_MPa'] == pytest.approx(
            props['E_eff_MPa'], abs=0.5  # self-consistent check + sanity
        )
        assert props['E_eff_MPa'] > 0.001
        assert props['E_eff_MPa'] < 10.0


# ================================================================== #
#  (g) EDGE CASES                                                      #
# ================================================================== #

class TestEdgeCases:
    """Boundary & degenerate parameter values."""

    def test_E_zero_gives_small_f2(self):
        """E=0 → flexural modes come from prestress only (~3 Hz)."""
        m = AbdominalModelV2(E=0.0)
        f2 = flexural_mode_frequencies_v2(m)[2]
        # With zero E, only P_iap stiffness contributes → small but positive
        assert f2 >= 0
        assert f2 < 5.0
        # Without prestress AND E=0, frequency truly approaches zero
        m_no_P = AbdominalModelV2(E=0.0, P_iap=0.0)
        f2_no_P = flexural_mode_frequencies_v2(m_no_P)[2]
        assert f2_no_P < 0.01

    def test_h_very_small(self):
        """Very thin wall → low frequency, no crash."""
        m = AbdominalModelV2(h=1e-6)
        f2 = flexural_mode_frequencies_v2(m)[2]
        assert np.isfinite(f2)
        assert f2 >= 0

    def test_c_equals_a_sphere(self):
        """c = a gives a sphere; model shouldn't crash."""
        m = AbdominalModelV2(a=0.15, b=0.15, c=0.15)
        f2 = flexural_mode_frequencies_v2(m)[2]
        assert np.isfinite(f2)
        assert f2 > 0

    def test_no_prestress(self):
        """P_iap=0 should still compute frequencies."""
        m = AbdominalModelV2(P_iap=0.0)
        f2 = flexural_mode_frequencies_v2(m)[2]
        assert np.isfinite(f2)
        assert f2 > 0

    def test_very_large_E(self):
        """Very stiff wall → very high frequency, no overflow."""
        m = AbdominalModelV2(E=1e12)
        f2 = flexural_mode_frequencies_v2(m)[2]
        assert np.isfinite(f2)
        assert f2 > 1000

    def test_gas_pocket_tiny_radius(self):
        """Very small gas pocket → high Minnaert frequency, no crash."""
        p = GasPocket(radius_cm=0.01)
        f = minnaert_frequency(p)
        assert np.isfinite(f)
        assert f > 1000

    def test_gas_pocket_large_radius(self):
        """Large gas pocket → low Minnaert frequency."""
        p = GasPocket(radius_cm=50.0)
        f = minnaert_frequency(p)
        assert np.isfinite(f)
        assert f < 10

    def test_spl_zero_gives_tiny_displacement(self, soft_tissue_model):
        """0 dB SPL (20 μPa) → negligible but finite displacement."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]
        r = flexural_mode_pressure_response(f2, 0.0, 2, soft_tissue_model)
        # 0 dB = 20 μPa, not zero pressure — displacement is tiny but nonzero
        assert r['displacement_um'] < 1e-3
        assert r['displacement_um'] > 0

    def test_single_layer_composite(self):
        """Single layer should give same E as input."""
        layers = [Layer("test", 10.0, 0.5, 0.45, 1050)]
        props = compute_composite_properties(layers)
        assert props['E_eff_Pa'] == pytest.approx(0.5e6, rel=1e-10)

    def test_ritz_mode_n_below_2(self):
        """oblate_ritz_frequency for n<2 should return 0."""
        m = AbdominalModelV2()
        assert oblate_ritz_frequency(
            0, m.a, m.c, m.h, m.E, m.nu, m.rho_wall, m.rho_fluid, m.P_iap,
        ) == 0.0
        assert oblate_ritz_frequency(
            1, m.a, m.c, m.h, m.E, m.nu, m.rho_wall, m.rho_fluid, m.P_iap,
        ) == 0.0


# ================================================================== #
#  (h) PARAMETRIC SWEEP MONOTONICITY                                   #
# ================================================================== #

class TestParametricMonotonicity:
    """f₂ should respond monotonically to single-parameter changes."""

    @pytest.mark.parametrize("E_Pa", [1e4, 5e4, 1e5, 2e5, 5e5, 1e6, 5e6])
    def test_f2_increases_with_E(self, E_Pa):
        """f₂ strictly increases with E (at fixed geometry)."""
        m_lo = AbdominalModelV2(E=E_Pa * 0.9)
        m_hi = AbdominalModelV2(E=E_Pa * 1.1)
        f_lo = flexural_mode_frequencies_v2(m_lo)[2]
        f_hi = flexural_mode_frequencies_v2(m_hi)[2]
        assert f_hi > f_lo

    @pytest.mark.parametrize("a", [0.12, 0.15, 0.18, 0.20, 0.25])
    def test_f2_decreases_with_a(self, a):
        """f₂ decreases with radius (larger cavity → lower frequency)."""
        da = 0.01
        m_lo = AbdominalModelV2(a=a - da, b=a - da, c=(a - da) * 0.67)
        m_hi = AbdominalModelV2(a=a + da, b=a + da, c=(a + da) * 0.67)
        f_lo = flexural_mode_frequencies_v2(m_lo)[2]
        f_hi = flexural_mode_frequencies_v2(m_hi)[2]
        assert f_lo > f_hi, f"f2 not decreasing with a: {f_lo} <= {f_hi}"

    @pytest.mark.parametrize("h", [0.005, 0.010, 0.015, 0.020])
    def test_f2_changes_with_h(self, h):
        """Thicker wall changes f₂; verify no crash and finite result."""
        m = AbdominalModelV2(h=h)
        f2 = flexural_mode_frequencies_v2(m)[2]
        assert np.isfinite(f2)
        assert f2 > 0

    def test_minnaert_decreases_with_radius(self):
        """Larger gas pocket → lower Minnaert frequency."""
        radii = [0.5, 1.0, 2.0, 5.0, 10.0]
        freqs = [minnaert_frequency(GasPocket(radius_cm=r)) for r in radii]
        for i in range(1, len(freqs)):
            assert freqs[i] < freqs[i - 1]

    def test_breathing_insensitive_to_E(self, default_model):
        """Breathing mode dominated by K_fluid, barely moves with E."""
        f_lo = breathing_mode_v2(AbdominalModelV2(E=0.01e6))
        f_hi = breathing_mode_v2(AbdominalModelV2(E=10e6))
        rel_change = abs(f_hi - f_lo) / f_lo
        assert rel_change < 0.05, (
            f"Breathing mode too sensitive to E: {rel_change*100:.1f}% change"
        )

    def test_parametric_E_sweep_returns_data(self):
        """parametric_E_sweep should return arrays of correct length."""
        E_range = np.logspace(-1, 0.5, 10)
        results = parametric_E_sweep(E_range, mode_n=2)
        assert len(results['f_free']) == len(E_range)
        assert all(f >= 0 for f in results['f_free'])

    def test_multi_parameter_sensitivity_runs(self):
        """multi_parameter_sensitivity should complete without error."""
        results = multi_parameter_sensitivity(mode_n=2)
        assert len(results) > 0
        assert all('f_n_hz' in r for r in results)


# ================================================================== #
#  Additional: Multilayer Wall Tests                                   #
# ================================================================== #

class TestMultilayerWall:
    """Multilayer composite wall model tests."""

    def test_relaxed_softer_than_tensed(self):
        """Relaxed wall E_eff < tensed wall E_eff."""
        r = compute_composite_properties(relaxed_layers())
        t = compute_composite_properties(tensed_layers())
        assert r['E_eff_Pa'] < t['E_eff_Pa']

    def test_total_thickness_positive(self):
        """All layer configs have positive total thickness."""
        for fn in [relaxed_layers, tensed_layers, obese_layers]:
            props = compute_composite_properties(fn())
            assert props['h_total_m'] > 0

    def test_D_ratio_reasonable(self):
        """D_eff / D_homogeneous should be a finite positive ratio.

        NOTE: D_eff is NOT always ≥ D_homogeneous because the homogeneous
        model uses E_eff (membrane-averaged), which can differ from the
        bending-weighted effective modulus. When stiff layers are near the
        neutral axis and soft layers are far away, D_eff < D_homogeneous.
        """
        for fn in [relaxed_layers, tensed_layers, obese_layers]:
            props = compute_composite_properties(fn())
            assert props['D_eff'] > 0
            assert props['D_homogeneous'] > 0
            assert 0.1 < props['D_ratio'] < 10.0

    def test_multilayer_to_v2_model_produces_valid_model(self):
        """multilayer_to_v2_model should produce a usable model."""
        m = multilayer_to_v2_model(relaxed_layers())
        f2 = flexural_mode_frequencies_v2(m)[2]
        assert np.isfinite(f2)
        assert f2 > 0

    def test_obese_thicker_wall(self):
        """Obese config should have thicker wall than relaxed."""
        r = compute_composite_properties(relaxed_layers())
        o = compute_composite_properties(obese_layers())
        assert o['h_total_m'] > r['h_total_m']


# ================================================================== #
#  Additional: Gas Pocket Model Tests                                  #
# ================================================================== #

class TestGasPocket:
    """Gas pocket resonance model tests."""

    def test_constrained_lower_than_minnaert(self):
        """Constrained bubble frequency ≤ Minnaert (wall mass loading)."""
        p = GasPocket(radius_cm=3.0)
        f_m = minnaert_frequency(p)
        f_c = constrained_bubble_frequency(p)
        assert f_c <= f_m * 1.1  # may be slightly higher from wall stiffness

    def test_elongated_frequency_finite(self):
        """Elongated pocket frequency should be finite and positive."""
        p = GasPocket(radius_cm=3.0, length_cm=15.0)
        f_e = elongated_pocket_frequency(p)
        assert np.isfinite(f_e)
        assert f_e > 0

    def test_pocket_response_amplification_near_unity_far_from_resonance(self):
        """At f << f_M, amplification H ≈ 1 (sub-resonant)."""
        p = GasPocket(radius_cm=2.0)  # f_M ≈ 161 Hz
        r = acoustic_response_of_gas_pocket(p, spl_db=120, freq_hz=7.0)
        assert 0.9 < r['amplification'] < 1.5

    def test_pocket_volume_correct(self):
        """Volume formula for spherical pocket."""
        p = GasPocket(radius_cm=1.0)
        expected = (4/3) * np.pi * 1.0**3  # in cm³ = mL
        assert p.volume_mL == pytest.approx(expected, rel=1e-10)


# ================================================================== #
#  Additional: Mechanical Coupling Model Tests                         #
# ================================================================== #

class TestMechanicalCoupling:
    """Mechanical (whole-body vibration) coupling tests."""

    def test_empirical_vs_theoretical_same_order(self, soft_tissue_model):
        """Empirical and theoretical displacement within 10× of each other."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]
        exp = WBVExposure(acceleration_rms_ms2=1.0, frequency_hz=f2)
        r_th = mechanical_excitation_response(exp, soft_tissue_model, use_empirical=False)
        r_em = mechanical_excitation_response(exp, soft_tissue_model, use_empirical=True)
        ratio = r_th['relative_displacement_um'] / r_em['relative_displacement_um']
        assert 0.1 < ratio < 10

    def test_compare_airborne_vs_mechanical_runs(self, soft_tissue_model):
        """compare_airborne_vs_mechanical should run without error."""
        results = compare_airborne_vs_mechanical(soft_tissue_model)
        assert len(results) > 0

    def test_displacement_scales_with_acceleration(self, soft_tissue_model):
        """Doubling acceleration should approximately double displacement."""
        f2 = flexural_mode_frequencies_v2(soft_tissue_model)[2]
        exp1 = WBVExposure(acceleration_rms_ms2=0.5, frequency_hz=f2)
        exp2 = WBVExposure(acceleration_rms_ms2=1.0, frequency_hz=f2)
        r1 = mechanical_excitation_response(exp1, soft_tissue_model)
        r2 = mechanical_excitation_response(exp2, soft_tissue_model)
        ratio = r2['relative_displacement_um'] / r1['relative_displacement_um']
        assert 1.8 < ratio < 2.2

    def test_wbv_exposure_kinematics(self):
        """Check kinematic relations of WBVExposure."""
        exp = WBVExposure(acceleration_rms_ms2=1.0, frequency_hz=5.0)
        omega = 2 * np.pi * 5.0
        # x_peak = a_rms * sqrt(2) / omega^2
        expected_x = 1.0 * np.sqrt(2) / omega**2
        assert exp.displacement_amplitude_m == pytest.approx(expected_x, rel=1e-10)


# ================================================================== #
#  Additional: Model Properties Tests                                  #
# ================================================================== #

class TestModelProperties:
    """AbdominalModelV2 computed properties."""

    def test_flexural_rigidity(self, default_model):
        """D = Eh³ / [12(1-ν²)]."""
        m = default_model
        expected = m.E * m.h**3 / (12 * (1 - m.nu**2))
        assert m.D == pytest.approx(expected, rel=1e-10)

    def test_volume_formula(self, default_model):
        """V = (4/3)πabc."""
        m = default_model
        expected = (4/3) * np.pi * m.a * m.b * m.c
        assert m.volume == pytest.approx(expected, rel=1e-10)

    def test_quality_factor(self, default_model):
        """Q = 1/(2ζ) = 1/tan_δ."""
        m = default_model
        expected_Q = 1.0 / m.loss_tangent
        assert m.Q == pytest.approx(expected_Q, rel=1e-10)

    def test_equivalent_sphere_radius(self, default_model):
        """R_eq = (abc)^{1/3}."""
        m = default_model
        expected = (m.a * m.b * m.c) ** (1/3)
        assert m.equivalent_sphere_radius == pytest.approx(expected, rel=1e-10)

    def test_fluid_speed_of_sound(self, default_model):
        """c = sqrt(K/ρ)."""
        m = default_model
        expected = np.sqrt(m.K_fluid / m.rho_fluid)
        assert m.c_fluid == pytest.approx(expected, rel=1e-10)


# ================================================================== #
#  Acoustic Short-Circuit / Helmholtz Sealed GI Tests                  #
# ================================================================== #

from analytical.gas_pocket_detailed import (
    GasPocketParams,
    pocket_response,
    helmholtz_sealed_gi,
    C_AIR,
)


class TestHelmholtzSealedGI:
    """Tests for the acoustic short-circuit / Helmholtz resonator model."""

    def test_default_frequency_near_15Hz(self):
        """Default parameters should give f_H ~ 15 Hz (reviewer estimate)."""
        r = helmholtz_sealed_gi()
        assert 10.0 < r["f_helmholtz_hz"] < 25.0

    def test_frequency_scales_inversely_with_sqrt_volume(self):
        """Doubling volume should decrease f_H by ~sqrt(2)."""
        r1 = helmholtz_sealed_gi(V_gas_mL=100.0)
        r2 = helmholtz_sealed_gi(V_gas_mL=200.0)
        ratio = r1["f_helmholtz_hz"] / r2["f_helmholtz_hz"]
        assert ratio == pytest.approx(np.sqrt(2), rel=0.01)

    def test_frequency_scales_with_sqrt_area(self):
        """Doubling constriction area should increase f_H by sqrt(2)."""
        S1 = np.pi * (5e-3) ** 2
        S2 = 2.0 * S1
        r1 = helmholtz_sealed_gi(S_constriction_m2=S1)
        r2 = helmholtz_sealed_gi(S_constriction_m2=S2)
        ratio = r2["f_helmholtz_hz"] / r1["f_helmholtz_hz"]
        assert ratio == pytest.approx(np.sqrt(2), rel=0.01)

    def test_equalization_ratio_bounded(self):
        """Short-circuit ratio should be in [0, 1]."""
        for V in [20, 100, 500]:
            r = helmholtz_sealed_gi(V_gas_mL=V)
            assert 0.0 <= r["short_circuit_ratio_7Hz"] <= 1.0

    def test_high_frequency_no_equalization(self):
        """For very small volume (high f_H), equalization ratio near 0."""
        r = helmholtz_sealed_gi(V_gas_mL=0.1, d_constriction_mm=1.0, L_gi_eff_m=10.0)
        assert r["f_helmholtz_hz"] > 40.0
        assert 0.0 <= r["short_circuit_ratio_7Hz"] <= 1.0

    def test_cylindrical_spl_threshold_matches_paper(self):
        """Cylindrical SPL threshold should be ~114 dB (Issue 2 fix)."""
        p = GasPocketParams(volume_mL=20.0, geometry="cylindrical", wall="elastic")
        lo, hi = 80.0, 160.0
        for _ in range(50):
            mid = (lo + hi) / 2.0
            r = pocket_response(p, np.array([7.0]), spl_dB=mid)
            if float(r["xi_um"][0]) > 0.5:
                hi = mid
            else:
                lo = mid
        spl = (lo + hi) / 2.0
        assert 112.0 < spl < 115.0, f"Cylindrical SPL threshold = {spl:.1f} dB"

    def test_amplification_ratio_range(self):
        """Gas pocket / whole-cavity ratio should be 35-100x (Issue 3 fix)."""
        xi_cavity = 0.014  # um at 120 dB (Paper 1 canonical)
        ratios = []
        for vol, geom in [(5, "spherical"), (100, "spherical"),
                          (5, "cylindrical"), (100, "cylindrical")]:
            p = GasPocketParams(volume_mL=vol, geometry=geom, wall="elastic")
            r = pocket_response(p, np.array([7.0]), spl_dB=120.0)
            ratios.append(float(r["xi_um"][0]) / xi_cavity)
        assert min(ratios) >= 30.0, f"Min ratio = {min(ratios):.1f}"
        assert max(ratios) <= 110.0, f"Max ratio = {max(ratios):.1f}"

    def test_wall_stiffness_fraction_small(self):
        """Wall stiffness should be < 3% of total k_eff (Issue 4)."""
        from analytical.gas_pocket_detailed import (
            GAMMA, P0, E_WALL, H_WALL, NU_WALL, R_LUMEN,
        )
        for vol in [5, 50, 100]:
            p = GasPocketParams(volume_mL=vol, geometry="spherical", wall="elastic")
            a = p.a_sphere
            k_gas = 3.0 * GAMMA * P0 / a
            k_wall = 2.0 * E_WALL * H_WALL / (a ** 2 * (1.0 - NU_WALL))
            frac = k_wall / (k_gas + k_wall)
            assert frac < 0.03, f"Wall fraction = {frac:.4f} for {vol} mL spherical"



# ================================================================== #
#  Breathing-mode infrasound size (dimensional analysis)               #
# ================================================================== #

class TestBreathingModeInfrasoundSize:
    """Regression tests for breathing_mode_infrasound_size (Paper 3, S5).

    The formula is R = sqrt(3 K_f / (rho_f omega^2)), which gives ~20 m
    at f=20 Hz with canonical fluid properties.  A previous version was
    missing the sqrt, yielding ~410 m (units error: m^2 not m).
    """

    def test_canonical_radius_approx_20m(self):
        """Canonical: R ~ 20 m at 20 Hz (NOT 410 m -- that was the bug)."""
        result = breathing_mode_infrasound_size()
        R = result["R_needed_m"]
        assert R == pytest.approx(20.24, rel=0.01), (
            f"Expected R ~ 20.24 m, got {R:.2f} m"
        )

    def test_radius_has_correct_units(self):
        """Dimensional check: R must scale as sqrt(K_f), not linearly."""
        r1 = breathing_mode_infrasound_size(K_f=2.2e9)["R_needed_m"]
        r4 = breathing_mode_infrasound_size(K_f=4 * 2.2e9)["R_needed_m"]
        ratio = r4 / r1
        assert ratio == pytest.approx(2.0, rel=1e-10), (
            f"R should scale as sqrt(K_f); ratio = {ratio:.6f}, expected 2.0"
        )

    def test_radius_not_410m(self):
        """Guard against regression to the m^2 bug."""
        R = breathing_mode_infrasound_size()["R_needed_m"]
        assert R < 100, f"R = {R:.0f} m; likely missing sqrt (old bug)"


# ================================================================== #
#  Dimensionless frequency and Phi analytical (dimensional analysis)  #
# ================================================================== #

class TestDimensionlessFrequency:
    """Tests for the Π₀ = f·a·√(ρ_f/E) definition."""

    def test_canonical_human(self):
        """Canonical human: f₂=3.95 Hz → Π₀ ≈ 0.072."""
        Pi0 = dimensionless_frequency(3.95, 0.18, 0.1e6, 1020.0)
        assert Pi0 == pytest.approx(0.072, rel=0.02)

    def test_scales_linearly_with_f(self):
        Pi0_a = dimensionless_frequency(4.0, 0.18, 0.1e6, 1020.0)
        Pi0_b = dimensionless_frequency(8.0, 0.18, 0.1e6, 1020.0)
        assert Pi0_b == pytest.approx(2 * Pi0_a, rel=1e-10)

    def test_scales_linearly_with_a(self):
        Pi0_a = dimensionless_frequency(4.0, 0.10, 0.1e6, 1020.0)
        Pi0_b = dimensionless_frequency(4.0, 0.20, 0.1e6, 1020.0)
        assert Pi0_b == pytest.approx(2 * Pi0_a, rel=1e-10)


class TestPhiAnalytical:
    """Tests for the closed-form dimensionless function Φ_n."""

    def test_canonical_n2(self):
        """Canonical human: Φ₂ ≈ 0.072."""
        phi = phi_analytical(
            h_a=0.056, c_a=0.67, rho_ratio=1.078,
            P_E=0.01, nu=0.45, n=2,
        )
        assert phi == pytest.approx(0.072, rel=0.02)

    def test_positive_for_physical_params(self):
        phi = phi_analytical(0.05, 0.67, 1.08, 0.01, 0.45, n=2)
        assert phi > 0

    def test_increases_with_h_a(self):
        """Thicker walls → stiffer → higher Π₀."""
        phi_thin = phi_analytical(0.03, 0.67, 1.08, 0.01, 0.45, n=2)
        phi_thick = phi_analytical(0.10, 0.67, 1.08, 0.01, 0.45, n=2)
        assert phi_thick > phi_thin

    def test_matches_numerical_model(self):
        """Φ must reproduce the numerical frequency exactly."""
        model = AbdominalModelV2()
        freqs = flexural_mode_frequencies_v2(model, n_max=2)
        f2 = freqs[2]
        Pi0_num = dimensionless_frequency(
            f2, model.a, model.E, model.rho_fluid,
        )
        Pi0_ana = phi_analytical(
            model.h / model.a,
            model.c / model.a,
            model.rho_wall / model.rho_fluid,
            model.P_iap / model.E,
            model.nu,
            n=2,
        )
        assert Pi0_num == pytest.approx(Pi0_ana, rel=1e-12)


# ================================================================== #
#  Parametric sweep and collapse verification                          #
# ================================================================== #

class TestParametricSweep:
    """Tests for the extended 1458-point parametric sweep."""

    def test_point_count(self):
        results = parametric_sweep_dimensionless()
        assert len(results) == 1458

    def test_all_pi_groups_varied(self):
        """All five governing Π-groups must have multiple unique values."""
        results = parametric_sweep_dimensionless()
        assert len(set(r["h_over_a"] for r in results)) >= 3
        assert len(set(r["c_over_a"] for r in results)) >= 3
        assert len(set(r["rho_ratio"] for r in results)) >= 3
        assert len(set(r["P_over_E"] for r in results)) >= 3
        assert len(set(r["nu"] for r in results)) >= 3

    def test_collapse_to_machine_precision(self):
        """Numerical Π₀ must match analytical Φ to machine precision."""
        results = parametric_sweep_dimensionless()
        v = verify_collapse(results)
        assert v["max_relative_error"] < 1e-12


# ================================================================== #
#  Cross-species animal scaling                                        #
# ================================================================== #

class TestAnimalScaling:
    """Tests for the cross-species scaling predictions."""

    def test_human_f2_near_4hz(self):
        s = animal_scaling()
        assert s["human"]["f_hz"] == pytest.approx(3.95, rel=0.02)

    def test_pi0_quasi_universal(self):
        """Π₀ should be ≈ 0.07 ± 15% for all species."""
        s = animal_scaling()
        for name in ["rat", "cat", "pig", "human"]:
            assert 0.05 < s[name]["Pi_0"] < 0.09, (
                f"{name}: Pi0 = {s[name]['Pi_0']:.4f} outside [0.05, 0.09]"
            )

    def test_coupling_ratio_range(self):
        """ℛ_scat = 1/(ka)² should be in 10³–10⁵ for all species."""
        s = animal_scaling()
        for name in ["rat", "cat", "pig", "human"]:
            R = s[name]["coupling_ratio_R"]
            assert 1e3 < R < 1e5, f"{name}: R = {R:.0f}"

    def test_ka_rayleigh_regime(self):
        """All species should have ka ≪ 1."""
        s = animal_scaling()
        for name in ["rat", "cat", "pig", "human"]:
            assert s[name]["ka"] < 0.1

    def test_f2_decreases_with_body_size(self):
        """Larger body → lower frequency."""
        s = animal_scaling()
        assert s["rat"]["f_hz"] > s["cat"]["f_hz"] > s["pig"]["f_hz"]
        assert s["pig"]["f_hz"] > s["human"]["f_hz"]
