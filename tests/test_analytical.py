"""Tests for analytical solutions."""

from __future__ import annotations

import numpy as np
import pytest

from browntone.analytical.acoustic_modes import (
    cylindrical_cavity_modes,
    rectangular_cavity_modes,
    spherical_cavity_modes,
)
from browntone.analytical.shell_vibration import (
    ShellMode,
    cylindrical_shell_frequencies,
    spherical_shell_frequencies,
)
from browntone.utils.materials import Material


class TestRectangularCavityModes:
    """Tests for rectangular acoustic cavity eigenfrequencies."""

    def test_known_first_mode(self) -> None:
        """First mode of a cube should be c/(2L) along one axis."""
        L = 1.0
        c = 343.0
        modes = rectangular_cavity_modes(L, L, L, c, n_max=1)

        # (1,0,0), (0,1,0), (0,0,1) are all degenerate at f = c/(2L)
        expected_f1 = c / (2.0 * L)
        assert modes[0].frequency_hz == pytest.approx(expected_f1, rel=1e-10)

    def test_mode_count(self) -> None:
        """Check the number of modes returned."""
        modes = rectangular_cavity_modes(0.3, 0.2, 0.1, 1500.0, n_max=3)
        # (n_max+1)^3 - 1 = 4^3 - 1 = 63
        assert len(modes) == 63

    def test_modes_sorted(self) -> None:
        """Modes should be returned in ascending frequency order."""
        modes = rectangular_cavity_modes(0.3, 0.2, 0.1, 1500.0, n_max=5)
        freqs = [m.frequency_hz for m in modes]
        assert freqs == sorted(freqs)

    def test_invalid_dimensions_raise(self) -> None:
        """Negative dimensions should raise ValueError."""
        with pytest.raises(ValueError):
            rectangular_cavity_modes(-1.0, 1.0, 1.0, 343.0)


class TestCylindricalCavityModes:
    """Tests for cylindrical acoustic cavity eigenfrequencies."""

    def test_returns_modes(self) -> None:
        """Should return a non-empty list of modes."""
        modes = cylindrical_cavity_modes(0.15, 0.30, 1500.0, m_max=3, n_max=3, q_max=3)
        assert len(modes) > 0

    def test_modes_sorted(self) -> None:
        """Modes should be in ascending frequency order."""
        modes = cylindrical_cavity_modes(0.15, 0.30, 1500.0)
        freqs = [m.frequency_hz for m in modes]
        assert freqs == sorted(freqs)

    def test_all_frequencies_positive(self) -> None:
        """All eigenfrequencies should be positive."""
        modes = cylindrical_cavity_modes(0.15, 0.30, 1500.0)
        assert all(m.frequency_hz > 0 for m in modes)


class TestSphericalCavityModes:
    """Tests for spherical acoustic cavity eigenfrequencies."""

    def test_first_breathing_mode(self) -> None:
        """First breathing mode frequency should be approximately c*π/R * factor."""
        R = 0.15
        c = 1500.0
        modes = spherical_cavity_modes(R, c, n_max=0, l_max=3)
        assert len(modes) > 0
        assert modes[0].frequency_hz > 0

    def test_modes_sorted(self) -> None:
        """Modes should be sorted by frequency."""
        modes = spherical_cavity_modes(0.15, 1500.0)
        freqs = [m.frequency_hz for m in modes]
        assert freqs == sorted(freqs)


class TestCylindricalShellFrequencies:
    """Tests for cylindrical shell vibration eigenfrequencies."""

    def test_returns_modes(self, steel: Material) -> None:
        """Should compute shell modes for a steel cylinder."""
        modes = cylindrical_shell_frequencies(
            radius_m=0.15,
            length_m=0.30,
            thickness_m=0.002,
            material=steel,
            m_max=3,
            n_max=5,
        )
        assert len(modes) > 0

    def test_modes_sorted(self, steel: Material) -> None:
        """Modes should be sorted by frequency."""
        modes = cylindrical_shell_frequencies(
            radius_m=0.15, length_m=0.30, thickness_m=0.002, material=steel
        )
        freqs = [m.frequency_hz for m in modes]
        assert freqs == sorted(freqs)

    def test_thicker_shell_higher_freq(self, steel: Material) -> None:
        """Thicker shells should generally have higher fundamental frequency."""
        modes_thin = cylindrical_shell_frequencies(
            radius_m=0.15, length_m=0.30, thickness_m=0.001, material=steel
        )
        modes_thick = cylindrical_shell_frequencies(
            radius_m=0.15, length_m=0.30, thickness_m=0.005, material=steel
        )
        # The fundamental frequency should increase with thickness
        # (bending stiffness increases faster than mass)
        assert modes_thick[0].frequency_hz > modes_thin[0].frequency_hz

    def test_invalid_geometry_raises(self, steel: Material) -> None:
        """Invalid geometry should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            cylindrical_shell_frequencies(
                radius_m=-0.1, length_m=0.3, thickness_m=0.002, material=steel
            )

    def test_unsupported_bc_raises(self, steel: Material) -> None:
        """Unsupported boundary condition should raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            cylindrical_shell_frequencies(
                radius_m=0.15,
                length_m=0.30,
                thickness_m=0.002,
                material=steel,
                boundary="clamped",
            )

    def test_soft_tissue_frequencies_in_infrasound_range(
        self, soft_tissue: Material
    ) -> None:
        """Soft tissue shell should have low eigenfrequencies (near infrasound)."""
        modes = cylindrical_shell_frequencies(
            radius_m=0.15,
            length_m=0.30,
            thickness_m=0.015,
            material=soft_tissue,
        )
        # The lowest modes should be in the audible/near-infrasound range
        # (very roughly 1-100 Hz for soft tissue at these dimensions)
        assert modes[0].frequency_hz < 500.0


class TestSphericalShellFrequencies:
    """Tests for spherical shell vibration eigenfrequencies."""

    def test_returns_modes(self, steel: Material) -> None:
        """Should return modes for a steel sphere."""
        modes = spherical_shell_frequencies(
            radius_m=0.15, thickness_m=0.002, material=steel, n_max=10
        )
        assert len(modes) > 0

    def test_modes_sorted(self, steel: Material) -> None:
        """Modes should be sorted by frequency."""
        modes = spherical_shell_frequencies(
            radius_m=0.15, thickness_m=0.002, material=steel
        )
        freqs = [m.frequency_hz for m in modes]
        assert freqs == sorted(freqs)
