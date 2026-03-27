"""Shared test fixtures for browntone tests."""

from __future__ import annotations

import pytest

from browntone.utils.materials import FluidMaterial, Material


@pytest.fixture
def soft_tissue() -> Material:
    """Representative soft tissue material."""
    return Material(
        name="Test soft tissue",
        youngs_modulus_pa=50_000.0,
        poisson_ratio=0.47,
        density_kg_m3=1050.0,
    )


@pytest.fixture
def steel() -> Material:
    """Steel for validation tests."""
    return Material(
        name="Test steel",
        youngs_modulus_pa=200e9,
        poisson_ratio=0.30,
        density_kg_m3=7850.0,
    )


@pytest.fixture
def water() -> FluidMaterial:
    """Water for acoustic tests."""
    return FluidMaterial(
        name="Test water",
        sound_speed_m_s=1500.0,
        density_kg_m3=1000.0,
    )
