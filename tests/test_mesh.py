"""Tests for mesh generation utilities."""

from __future__ import annotations

import pytest

from browntone.mesh.abdominal_cavity import CavityGeometry, _validate_geometry


class TestCavityGeometry:
    """Tests for CavityGeometry validation."""

    def test_default_geometry_valid(self) -> None:
        """Default geometry should pass validation."""
        geo = CavityGeometry()
        _validate_geometry(geo)  # Should not raise

    def test_negative_radius_raises(self) -> None:
        """Negative semi-minor axis should raise ValueError."""
        geo = CavityGeometry(semi_minor_m=-0.1)
        with pytest.raises(ValueError, match="positive"):
            _validate_geometry(geo)

    def test_thickness_exceeds_radius_raises(self) -> None:
        """Wall thicker than radius should raise ValueError."""
        geo = CavityGeometry(semi_minor_m=0.10, wall_thickness_m=0.15)
        with pytest.raises(ValueError, match="less than"):
            _validate_geometry(geo)

    def test_zero_element_size_raises(self) -> None:
        """Zero element size should raise ValueError."""
        geo = CavityGeometry(element_size_m=0.0)
        with pytest.raises(ValueError, match="positive"):
            _validate_geometry(geo)

    def test_custom_geometry_valid(self) -> None:
        """Custom valid geometry should pass."""
        geo = CavityGeometry(
            shape="cylinder",
            semi_major_m=0.20,
            semi_minor_m=0.12,
            wall_thickness_m=0.010,
            element_size_m=0.008,
        )
        _validate_geometry(geo)
