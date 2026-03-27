"""Material property database for biological tissues and fluids.

Provides a simple interface for accessing material properties used in
abdominal cavity simulations. Properties can be loaded from built-in
defaults or from JSON files.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Material:
    """Isotropic material properties.

    Parameters
    ----------
    name : str
        Human-readable material name.
    youngs_modulus_pa : float
        Young's modulus in pascals.
    poisson_ratio : float
        Poisson's ratio (dimensionless, 0 < ν < 0.5).
    density_kg_m3 : float
        Mass density in kg/m³.
    damping_ratio : float
        Modal damping ratio (dimensionless). Default 0.0.
    description : str
        Optional description or source reference.
    """

    name: str
    youngs_modulus_pa: float
    poisson_ratio: float
    density_kg_m3: float
    damping_ratio: float = 0.0
    description: str = ""

    def __post_init__(self) -> None:
        """Validate material properties."""
        if self.youngs_modulus_pa <= 0:
            raise ValueError(
                f"Young's modulus must be positive, got {self.youngs_modulus_pa}"
            )
        if not 0 < self.poisson_ratio < 0.5:
            raise ValueError(
                f"Poisson's ratio must be in (0, 0.5), got {self.poisson_ratio}"
            )
        if self.density_kg_m3 <= 0:
            raise ValueError(f"Density must be positive, got {self.density_kg_m3}")
        if self.damping_ratio < 0:
            raise ValueError(
                f"Damping ratio must be non-negative, got {self.damping_ratio}"
            )

    @property
    def shear_modulus_pa(self) -> float:
        """Shear modulus G = E / (2(1+ν)) in pascals."""
        return self.youngs_modulus_pa / (2.0 * (1.0 + self.poisson_ratio))

    @property
    def bulk_modulus_pa(self) -> float:
        """Bulk modulus K = E / (3(1-2ν)) in pascals."""
        return self.youngs_modulus_pa / (3.0 * (1.0 - 2.0 * self.poisson_ratio))

    @property
    def lame_lambda_pa(self) -> float:
        """First Lamé parameter λ in pascals."""
        E = self.youngs_modulus_pa
        nu = self.poisson_ratio
        return E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))

    @property
    def lame_mu_pa(self) -> float:
        """Second Lamé parameter μ (= shear modulus) in pascals."""
        return self.shear_modulus_pa

    @property
    def p_wave_speed_m_s(self) -> float:
        """P-wave (longitudinal) speed in m/s."""
        import math

        lam = self.lame_lambda_pa
        mu = self.lame_mu_pa
        rho = self.density_kg_m3
        return math.sqrt((lam + 2.0 * mu) / rho)

    @property
    def s_wave_speed_m_s(self) -> float:
        """S-wave (shear) speed in m/s."""
        import math

        return math.sqrt(self.shear_modulus_pa / self.density_kg_m3)


@dataclass(frozen=True)
class FluidMaterial:
    """Acoustic fluid material properties.

    Parameters
    ----------
    name : str
        Human-readable name.
    sound_speed_m_s : float
        Speed of sound in m/s.
    density_kg_m3 : float
        Mass density in kg/m³.
    description : str
        Optional description.
    """

    name: str
    sound_speed_m_s: float
    density_kg_m3: float
    description: str = ""

    def __post_init__(self) -> None:
        """Validate fluid properties."""
        if self.sound_speed_m_s <= 0:
            raise ValueError(
                f"Sound speed must be positive, got {self.sound_speed_m_s}"
            )
        if self.density_kg_m3 <= 0:
            raise ValueError(f"Density must be positive, got {self.density_kg_m3}")

    @property
    def bulk_modulus_pa(self) -> float:
        """Bulk modulus K = ρc² in pascals."""
        return self.density_kg_m3 * self.sound_speed_m_s**2

    @property
    def impedance_pa_s_m(self) -> float:
        """Characteristic acoustic impedance Z = ρc in Pa·s/m."""
        return self.density_kg_m3 * self.sound_speed_m_s


# =============================================================================
# Built-in material library
# =============================================================================

MATERIALS: dict[str, Material] = {
    "soft-tissue": Material(
        name="Generic soft tissue",
        youngs_modulus_pa=50_000.0,
        poisson_ratio=0.47,
        density_kg_m3=1050.0,
        damping_ratio=0.05,
        description="Representative abdominal wall tissue. E from 20-100 kPa range.",
    ),
    "soft-tissue-stiff": Material(
        name="Stiff soft tissue",
        youngs_modulus_pa=100_000.0,
        poisson_ratio=0.48,
        density_kg_m3=1100.0,
        damping_ratio=0.03,
        description="Upper bound of abdominal wall stiffness (contracted muscle).",
    ),
    "soft-tissue-compliant": Material(
        name="Compliant soft tissue",
        youngs_modulus_pa=20_000.0,
        poisson_ratio=0.45,
        density_kg_m3=1000.0,
        damping_ratio=0.08,
        description="Lower bound of abdominal wall stiffness (relaxed, fatty tissue).",
    ),
    "rubber-phantom": Material(
        name="Silicone rubber phantom",
        youngs_modulus_pa=1_000_000.0,
        poisson_ratio=0.49,
        density_kg_m3=1100.0,
        damping_ratio=0.02,
        description="Silicone rubber for experimental validation phantoms.",
    ),
    "steel-validation": Material(
        name="Steel (validation)",
        youngs_modulus_pa=200e9,
        poisson_ratio=0.30,
        density_kg_m3=7850.0,
        damping_ratio=0.001,
        description="Steel for code verification against analytical solutions.",
    ),
}

FLUIDS: dict[str, FluidMaterial] = {
    "water": FluidMaterial(
        name="Water (20°C)",
        sound_speed_m_s=1482.0,
        density_kg_m3=998.0,
        description="Pure water at 20°C.",
    ),
    "abdominal-fluid": FluidMaterial(
        name="Abdominal cavity fluid",
        sound_speed_m_s=1500.0,
        density_kg_m3=1000.0,
        description="Approximate properties of intra-abdominal fluid.",
    ),
    "air": FluidMaterial(
        name="Air (20°C, 1 atm)",
        sound_speed_m_s=343.0,
        density_kg_m3=1.225,
        description="Standard air conditions.",
    ),
}


def get_material(name: str) -> Material:
    """Look up a material by name from the built-in library.

    Parameters
    ----------
    name : str
        Material name (case-insensitive, hyphens or underscores accepted).

    Returns
    -------
    Material
        The material properties.

    Raises
    ------
    KeyError
        If the material is not found.
    """
    key = name.lower().replace("_", "-")
    if key not in MATERIALS:
        available = ", ".join(sorted(MATERIALS.keys()))
        raise KeyError(f"Unknown material '{name}'. Available: {available}")
    return MATERIALS[key]


def get_fluid(name: str) -> FluidMaterial:
    """Look up a fluid material by name.

    Parameters
    ----------
    name : str
        Fluid name (case-insensitive).

    Returns
    -------
    FluidMaterial
        The fluid properties.

    Raises
    ------
    KeyError
        If the fluid is not found.
    """
    key = name.lower().replace("_", "-")
    if key not in FLUIDS:
        available = ", ".join(sorted(FLUIDS.keys()))
        raise KeyError(f"Unknown fluid '{name}'. Available: {available}")
    return FLUIDS[key]


def load_material_from_json(path: Path | str) -> Material:
    """Load material properties from a JSON file.

    Parameters
    ----------
    path : Path or str
        Path to the JSON file.

    Returns
    -------
    Material
        Loaded material.
    """
    path = Path(path)
    with path.open() as f:
        data = json.load(f)

    return Material(
        name=data.get("name", path.stem),
        youngs_modulus_pa=data["youngs_modulus_pa"],
        poisson_ratio=data["poisson_ratio"],
        density_kg_m3=data["density_kg_m3"],
        damping_ratio=data.get("damping_ratio", 0.0),
        description=data.get("description", f"Loaded from {path}"),
    )
