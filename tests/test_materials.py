"""Tests for the material property database."""

from __future__ import annotations

import pytest

from browntone.utils.materials import (
    FLUIDS,
    MATERIALS,
    FluidMaterial,
    Material,
    get_fluid,
    get_material,
)


class TestMaterial:
    """Tests for the Material dataclass."""

    def test_valid_material(self) -> None:
        """A valid material should be created without errors."""
        mat = Material(
            name="test",
            youngs_modulus_pa=1e6,
            poisson_ratio=0.3,
            density_kg_m3=1000.0,
        )
        assert mat.youngs_modulus_pa == 1e6

    def test_negative_youngs_modulus_raises(self) -> None:
        """Negative Young's modulus should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Material(
                name="bad",
                youngs_modulus_pa=-1e6,
                poisson_ratio=0.3,
                density_kg_m3=1000.0,
            )

    def test_poisson_ratio_bounds(self) -> None:
        """Poisson's ratio outside (0, 0.5) should raise ValueError."""
        with pytest.raises(ValueError, match="Poisson"):
            Material(
                name="bad",
                youngs_modulus_pa=1e6,
                poisson_ratio=0.5,
                density_kg_m3=1000.0,
            )

    def test_shear_modulus(self) -> None:
        """Shear modulus should be E / (2(1+ν))."""
        mat = Material(
            name="test",
            youngs_modulus_pa=1e6,
            poisson_ratio=0.25,
            density_kg_m3=1000.0,
        )
        expected_G = 1e6 / (2.0 * 1.25)
        assert mat.shear_modulus_pa == pytest.approx(expected_G)

    def test_bulk_modulus(self) -> None:
        """Bulk modulus should be E / (3(1-2ν))."""
        mat = Material(
            name="test",
            youngs_modulus_pa=1e6,
            poisson_ratio=0.25,
            density_kg_m3=1000.0,
        )
        expected_K = 1e6 / (3.0 * 0.5)
        assert mat.bulk_modulus_pa == pytest.approx(expected_K)

    def test_wave_speeds_positive(self) -> None:
        """Wave speeds should be positive."""
        mat = Material(
            name="test",
            youngs_modulus_pa=1e6,
            poisson_ratio=0.3,
            density_kg_m3=1000.0,
        )
        assert mat.p_wave_speed_m_s > 0
        assert mat.s_wave_speed_m_s > 0
        assert mat.p_wave_speed_m_s > mat.s_wave_speed_m_s


class TestFluidMaterial:
    """Tests for the FluidMaterial dataclass."""

    def test_valid_fluid(self) -> None:
        """A valid fluid should be created without errors."""
        fluid = FluidMaterial(
            name="test water",
            sound_speed_m_s=1500.0,
            density_kg_m3=1000.0,
        )
        assert fluid.bulk_modulus_pa == pytest.approx(1500.0**2 * 1000.0)

    def test_impedance(self) -> None:
        """Impedance should be ρc."""
        fluid = FluidMaterial(
            name="test",
            sound_speed_m_s=1500.0,
            density_kg_m3=1000.0,
        )
        assert fluid.impedance_pa_s_m == pytest.approx(1.5e6)


class TestMaterialLibrary:
    """Tests for the built-in material library."""

    def test_all_builtin_materials_valid(self) -> None:
        """All built-in materials should have valid properties."""
        for name, mat in MATERIALS.items():
            assert mat.youngs_modulus_pa > 0, f"{name}: E <= 0"
            assert 0 < mat.poisson_ratio < 0.5, f"{name}: ν out of range"
            assert mat.density_kg_m3 > 0, f"{name}: ρ <= 0"

    def test_all_builtin_fluids_valid(self) -> None:
        """All built-in fluids should have valid properties."""
        for name, fluid in FLUIDS.items():
            assert fluid.sound_speed_m_s > 0, f"{name}: c <= 0"
            assert fluid.density_kg_m3 > 0, f"{name}: ρ <= 0"

    def test_get_material_by_name(self) -> None:
        """Should retrieve materials by name."""
        mat = get_material("soft-tissue")
        assert mat.youngs_modulus_pa == 50_000.0

    def test_get_material_case_insensitive(self) -> None:
        """Material lookup should be case-insensitive."""
        mat = get_material("Soft-Tissue")
        assert mat.name == "Generic soft tissue"

    def test_get_unknown_material_raises(self) -> None:
        """Looking up a non-existent material should raise KeyError."""
        with pytest.raises(KeyError, match="Unknown material"):
            get_material("unobtainium")

    def test_get_fluid_by_name(self) -> None:
        """Should retrieve fluids by name."""
        fluid = get_fluid("water")
        assert fluid.sound_speed_m_s == pytest.approx(1482.0)
