"""Closed-form acoustic cavity mode solutions.

Analytical eigenfrequencies for canonical cavity geometries (cylindrical,
spherical, rectangular) using Bessel and trigonometric function solutions
to the Helmholtz equation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
from scipy.special import jnp_zeros

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AcousticMode:
    """A single acoustic cavity mode.

    Parameters
    ----------
    indices : tuple[int, ...]
        Mode indices (interpretation depends on geometry).
    frequency_hz : float
        Natural frequency in hertz.
    description : str
        Human-readable mode description.
    """

    indices: tuple[int, ...]
    frequency_hz: float
    description: str = ""


def rectangular_cavity_modes(
    lx_m: float,
    ly_m: float,
    lz_m: float,
    sound_speed_m_s: float,
    n_max: int = 5,
) -> list[AcousticMode]:
    """Eigenfrequencies of a rigid-walled rectangular acoustic cavity.

    Parameters
    ----------
    lx_m, ly_m, lz_m : float
        Cavity dimensions in metres.
    sound_speed_m_s : float
        Speed of sound in the fluid (m/s).
    n_max : int
        Maximum mode index in each direction.

    Returns
    -------
    list[AcousticMode]
        Sorted list of acoustic modes (excluding the trivial (0,0,0) mode).

    Notes
    -----
    For a rigid-walled rectangular cavity, the eigenfrequencies are:

    .. math::

        f_{n_x, n_y, n_z} = \\frac{c}{2}
        \\sqrt{\\left(\\frac{n_x}{L_x}\\right)^2
             + \\left(\\frac{n_y}{L_y}\\right)^2
             + \\left(\\frac{n_z}{L_z}\\right)^2}
    """
    _validate_positive(lx_m=lx_m, ly_m=ly_m, lz_m=lz_m, c=sound_speed_m_s)

    modes: list[AcousticMode] = []
    c = sound_speed_m_s

    for nx in range(0, n_max + 1):
        for ny in range(0, n_max + 1):
            for nz in range(0, n_max + 1):
                if nx == 0 and ny == 0 and nz == 0:
                    continue
                freq = (
                    c
                    / 2.0
                    * np.sqrt(
                        (nx / lx_m) ** 2 + (ny / ly_m) ** 2 + (nz / lz_m) ** 2
                    )
                )
                modes.append(
                    AcousticMode(
                        indices=(nx, ny, nz),
                        frequency_hz=float(freq),
                        description=f"({nx},{ny},{nz})",
                    )
                )

    modes.sort(key=lambda m: m.frequency_hz)
    return modes


def cylindrical_cavity_modes(
    radius_m: float,
    length_m: float,
    sound_speed_m_s: float,
    m_max: int = 5,
    n_max: int = 5,
    q_max: int = 5,
) -> list[AcousticMode]:
    """Eigenfrequencies of a rigid-walled cylindrical acoustic cavity.

    Parameters
    ----------
    radius_m : float
        Cavity radius in metres.
    length_m : float
        Cavity length in metres.
    sound_speed_m_s : float
        Speed of sound in the fluid (m/s).
    m_max : int
        Maximum circumferential mode number.
    n_max : int
        Maximum radial mode number.
    q_max : int
        Maximum axial mode number.

    Returns
    -------
    list[AcousticMode]
        Sorted list of acoustic modes.

    Notes
    -----
    Eigenfrequencies for a rigid-walled cylinder are:

    .. math::

        f_{m,n,q} = \\frac{c}{2\\pi}
        \\sqrt{\\left(\\frac{\\alpha'_{mn}}{R}\\right)^2
             + \\left(\\frac{q\\pi}{L}\\right)^2}

    where :math:`\\alpha'_{mn}` is the n-th zero of :math:`J'_m` (derivative of
    the Bessel function of the first kind of order m).
    """
    _validate_positive(R=radius_m, L=length_m, c=sound_speed_m_s)

    modes: list[AcousticMode] = []
    c = sound_speed_m_s
    R = radius_m
    L = length_m

    for m in range(0, m_max + 1):
        # Zeros of the derivative of J_m
        alpha_primes = jnp_zeros(m, n_max)

        for n_idx, alpha_mn in enumerate(alpha_primes):
            n = n_idx + 1
            for q in range(0, q_max + 1):
                if m == 0 and n == 1 and q == 0:
                    # Skip if this corresponds to the zero eigenvalue
                    if abs(alpha_mn) < 1e-12:
                        continue

                k_squared = (alpha_mn / R) ** 2 + (q * np.pi / L) ** 2
                if k_squared > 0:
                    freq = c / (2.0 * np.pi) * np.sqrt(k_squared)
                    modes.append(
                        AcousticMode(
                            indices=(m, n, q),
                            frequency_hz=float(freq),
                            description=f"(m={m},n={n},q={q})",
                        )
                    )

    modes.sort(key=lambda mode: mode.frequency_hz)
    return modes


def spherical_cavity_modes(
    radius_m: float,
    sound_speed_m_s: float,
    n_max: int = 10,
    l_max: int = 5,
) -> list[AcousticMode]:
    """Eigenfrequencies of a rigid-walled spherical acoustic cavity.

    Parameters
    ----------
    radius_m : float
        Cavity radius in metres.
    sound_speed_m_s : float
        Speed of sound in the fluid (m/s).
    n_max : int
        Maximum angular mode number.
    l_max : int
        Maximum radial mode number.

    Returns
    -------
    list[AcousticMode]
        Sorted list of acoustic modes.

    Notes
    -----
    Eigenfrequencies satisfy :math:`j'_n(kR) = 0`, where :math:`j_n` is the
    spherical Bessel function of the first kind.  For n=0 (breathing modes),
    :math:`kR = l\\pi`.
    """
    _validate_positive(R=radius_m, c=sound_speed_m_s)

    modes: list[AcousticMode] = []
    c = sound_speed_m_s
    R = radius_m

    # For each angular order, find radial zeros of j'_n(kr)
    # Using the relation between spherical and cylindrical Bessel functions:
    # j_n(x) = sqrt(pi/(2x)) * J_{n+1/2}(x)
    for n in range(0, n_max + 1):
        # Get zeros of the derivative of the spherical Bessel function
        # For n=0: j_0(x) = sin(x)/x, j'_0(x)=0 at x = tan(x)
        # We use numerical root finding via the cylindrical Bessel zeros
        # as an approximation
        if n == 0:
            # Breathing modes: zeros of j'_0(x) = 0 → tan(x) = x
            # Approximate roots: x ≈ (l+0.5)π for l = 1, 2, ...
            for l in range(1, l_max + 1):
                # Newton refinement of tan(x) = x starting near (l+0.5)π
                x = _find_tan_x_root(l)
                freq = c * x / (2.0 * np.pi * R)
                modes.append(
                    AcousticMode(
                        indices=(n, l),
                        frequency_hz=float(freq),
                        description=f"(n={n},l={l}) breathing",
                    )
                )
        else:
            # Higher-order modes: use Bessel function zeros as approximation
            alpha_primes = jnp_zeros(n, l_max)
            for l_idx, alpha in enumerate(alpha_primes):
                l = l_idx + 1
                freq = c * alpha / (2.0 * np.pi * R)
                modes.append(
                    AcousticMode(
                        indices=(n, l),
                        frequency_hz=float(freq),
                        description=f"(n={n},l={l})",
                    )
                )

    modes.sort(key=lambda mode: mode.frequency_hz)
    return modes


def _find_tan_x_root(l: int, tol: float = 1e-12, max_iter: int = 50) -> float:
    """Find the l-th positive root of tan(x) = x using Newton's method.

    Parameters
    ----------
    l : int
        Root index (1, 2, 3, ...).
    tol : float
        Convergence tolerance.
    max_iter : int
        Maximum iterations.

    Returns
    -------
    float
        The l-th root.
    """
    # Initial guess just past (l + 0.5)π to avoid the asymptote
    x = (l + 0.5) * np.pi - 0.1

    for _ in range(max_iter):
        f = np.tan(x) - x
        fp = 1.0 / np.cos(x) ** 2 - 1.0
        dx = f / fp
        x -= dx
        if abs(dx) < tol:
            break

    return float(x)


def _validate_positive(**kwargs: float) -> None:
    """Validate that all keyword arguments are positive."""
    for name, value in kwargs.items():
        if value <= 0:
            raise ValueError(f"{name} must be positive, got {value}")
