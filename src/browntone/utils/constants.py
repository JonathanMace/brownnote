"""Physical constants and project-wide parameters.

All constants in SI units unless otherwise noted.
"""

from __future__ import annotations

import math

# =============================================================================
# Physical constants
# =============================================================================

SPEED_OF_SOUND_WATER_M_S: float = 1500.0
"""Speed of sound in water at ~20°C (m/s)."""

SPEED_OF_SOUND_AIR_M_S: float = 343.0
"""Speed of sound in air at ~20°C (m/s)."""

DENSITY_WATER_KG_M3: float = 1000.0
"""Density of water at ~20°C (kg/m³)."""

DENSITY_AIR_KG_M3: float = 1.225
"""Density of air at sea level, ~20°C (kg/m³)."""

ATMOSPHERIC_PRESSURE_PA: float = 101_325.0
"""Standard atmospheric pressure (Pa)."""

# =============================================================================
# Infrasound range
# =============================================================================

INFRASOUND_LOWER_HZ: float = 0.1
"""Lower bound of the infrasound range (Hz)."""

INFRASOUND_UPPER_HZ: float = 20.0
"""Upper bound of the infrasound range (Hz). Below human hearing threshold."""

# =============================================================================
# Reference abdominal geometry
# =============================================================================

ABDOMEN_LENGTH_M: float = 0.30
"""Typical abdominal cavity length (m)."""

ABDOMEN_RADIUS_M: float = 0.15
"""Typical abdominal cavity radius (m)."""

ABDOMEN_WALL_THICKNESS_M: float = 0.015
"""Typical abdominal wall thickness (m)."""

# =============================================================================
# Unit conversions
# =============================================================================


def hz_to_rad_s(frequency_hz: float) -> float:
    """Convert frequency from hertz to radians per second."""
    return 2.0 * math.pi * frequency_hz


def rad_s_to_hz(omega_rad_s: float) -> float:
    """Convert angular frequency from radians per second to hertz."""
    return omega_rad_s / (2.0 * math.pi)


def kpa_to_pa(value_kpa: float) -> float:
    """Convert kilopascals to pascals."""
    return value_kpa * 1_000.0


def pa_to_kpa(value_pa: float) -> float:
    """Convert pascals to kilopascals."""
    return value_pa / 1_000.0
