"""Closed-form natural frequencies for cylindrical and spherical shells.

This module implements classical shell vibration solutions from Leissa (1973)
and Soedel (2004) for use as FEA validation benchmarks.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from browntone.utils.materials import Material

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ShellMode:
    """A single shell vibration mode.

    Parameters
    ----------
    m : int
        Axial half-wave number.
    n : int
        Circumferential wave number.
    frequency_hz : float
        Natural frequency in hertz.
    """

    m: int
    n: int
    frequency_hz: float


def cylindrical_shell_frequencies(
    radius_m: float,
    length_m: float,
    thickness_m: float,
    material: Material,
    m_max: int = 5,
    n_max: int = 10,
    boundary: str = "simply-supported",
) -> list[ShellMode]:
    """Compute natural frequencies of a thin cylindrical shell.

    Uses the Donnell shell theory for a simply-supported cylindrical shell.
    Valid when h/R << 1 (thin shell assumption).

    Parameters
    ----------
    radius_m : float
        Mean radius of the shell in metres.
    length_m : float
        Length of the shell in metres.
    thickness_m : float
        Wall thickness in metres.
    material : Material
        Material properties (must have E, nu, rho).
    m_max : int
        Maximum axial half-wave number.
    n_max : int
        Maximum circumferential wave number.
    boundary : str
        Boundary condition. Currently only ``"simply-supported"`` is implemented.

    Returns
    -------
    list[ShellMode]
        Sorted list of shell modes (lowest frequency first).

    Raises
    ------
    ValueError
        If geometry or material parameters are non-physical.
    NotImplementedError
        If boundary condition is not supported.

    Notes
    -----
    The Donnell thin-shell frequency parameter is:

    .. math::

        \\Omega^2 = \\frac{\\rho h \\omega^2 R^2}{E}

    For a simply-supported shell of length L, the axial wavenumber is
    :math:`\\lambda_m = m \\pi R / L`.

    References
    ----------
    .. [1] Leissa, A.W., "Vibration of Shells", NASA SP-288, 1973.
    .. [2] Soedel, W., "Vibrations of Shells and Plates", 3rd ed., 2004.
    """
    if boundary != "simply-supported":
        raise NotImplementedError(
            f"Boundary condition '{boundary}' not implemented. "
            "Only 'simply-supported' is currently available."
        )

    _validate_shell_geometry(radius_m, length_m, thickness_m)

    R = radius_m
    L = length_m
    h = thickness_m
    E = material.youngs_modulus_pa
    nu = material.poisson_ratio
    rho = material.density_kg_m3

    # Bending stiffness parameter
    kappa2 = h**2 / (12.0 * R**2)

    modes: list[ShellMode] = []

    for m in range(1, m_max + 1):
        lam = m * np.pi * R / L  # dimensionless axial wavenumber

        for n in range(0, n_max + 1):
            # Donnell frequency parameter (squared)
            # Three roots exist per (m, n); we take the lowest (flexural)
            omega2 = _donnell_frequency_parameter(lam, n, nu, kappa2)

            if omega2 > 0:
                omega = np.sqrt(omega2 * E / (rho * (1.0 - nu**2) * R**2))
                freq_hz = omega / (2.0 * np.pi)
                modes.append(ShellMode(m=m, n=n, frequency_hz=float(freq_hz)))

    modes.sort(key=lambda mode: mode.frequency_hz)
    logger.info(
        "Computed %d cylindrical shell modes (f_min=%.2f Hz, f_max=%.2f Hz)",
        len(modes),
        modes[0].frequency_hz if modes else 0.0,
        modes[-1].frequency_hz if modes else 0.0,
    )
    return modes


def _donnell_frequency_parameter(
    lam: float, n: int, nu: float, kappa2: float
) -> float:
    """Compute the lowest Donnell frequency parameter for mode (m, n).

    Parameters
    ----------
    lam : float
        Dimensionless axial wavenumber (m * pi * R / L).
    n : int
        Circumferential wave number.
    nu : float
        Poisson's ratio.
    kappa2 : float
        Shell thickness parameter h²/(12R²).

    Returns
    -------
    float
        Lowest positive frequency parameter Ω².
    """
    s2 = lam**2 + n**2  # combined wavenumber squared

    # Membrane contribution
    a_membrane = (
        (1.0 - nu) / 2.0 * (lam**2 + n**2)
        + (1.0 + nu) / 2.0 * lam**2
    )

    # For Donnell theory, the simplified frequency parameter for the
    # lowest (primarily flexural) branch is:
    omega2 = kappa2 * s2**2 + lam**4 / s2**2 if s2 > 0 else 0.0

    return omega2


def spherical_shell_frequencies(
    radius_m: float,
    thickness_m: float,
    material: Material,
    n_max: int = 20,
) -> list[ShellMode]:
    """Compute natural frequencies of a thin spherical shell.

    Uses the membrane theory for axisymmetric modes of a complete spherical
    shell. Valid when h/R << 1.

    Parameters
    ----------
    radius_m : float
        Mean radius of the sphere in metres.
    thickness_m : float
        Wall thickness in metres.
    material : Material
        Material properties.
    n_max : int
        Maximum mode number.

    Returns
    -------
    list[ShellMode]
        Sorted list of shell modes.
    """
    R = radius_m
    h = thickness_m
    E = material.youngs_modulus_pa
    nu = material.poisson_ratio
    rho = material.density_kg_m3

    modes: list[ShellMode] = []

    for n in range(2, n_max + 1):
        # Lamb's solution for a thin spherical shell (membrane + bending)
        kappa2 = h**2 / (12.0 * R**2)
        lam_n = n * (n + 1)

        # Frequency parameter for the lower (flexural) branch
        omega2_lower = (
            E
            / (rho * R**2 * (1.0 - nu**2))
            * (
                0.5 * ((1.0 + nu) + kappa2 * (lam_n - (1.0 - nu)))
                - 0.5
                * np.sqrt(
                    ((1.0 + nu) + kappa2 * (lam_n - (1.0 - nu))) ** 2
                    - 4.0 * kappa2 * (lam_n - 2.0) * (1.0 - nu**2) / (1.0 + nu)
                )
            )
        )

        if omega2_lower > 0:
            freq_hz = np.sqrt(omega2_lower) / (2.0 * np.pi)
            modes.append(ShellMode(m=0, n=n, frequency_hz=float(freq_hz)))

    modes.sort(key=lambda mode: mode.frequency_hz)
    return modes


def _validate_shell_geometry(
    radius_m: float, length_m: float, thickness_m: float
) -> None:
    """Validate shell geometry parameters.

    Raises
    ------
    ValueError
        If any parameter is non-physical.
    """
    if radius_m <= 0:
        raise ValueError(f"Radius must be positive, got {radius_m}")
    if length_m <= 0:
        raise ValueError(f"Length must be positive, got {length_m}")
    if thickness_m <= 0:
        raise ValueError(f"Thickness must be positive, got {thickness_m}")
    if thickness_m >= radius_m:
        raise ValueError(
            f"Thickness ({thickness_m}) must be less than radius ({radius_m}) "
            "for thin shell theory"
        )
