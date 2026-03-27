"""Coupled acoustic–structural (FSI) solver using FEniCSx.

Solves the coupled eigenvalue problem for a fluid-filled elastic cavity,
capturing both structural and acoustic modes and their interaction.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


@dataclass
class FSIResults:
    """Container for coupled FSI analysis results.

    Parameters
    ----------
    eigenvalues : NDArray
        Coupled eigenvalues (ω² in rad²/s²).
    frequencies_hz : NDArray
        Coupled natural frequencies in hertz.
    structural_participation : NDArray
        Structural participation factor for each mode (0 = pure acoustic, 1 = pure structural).
    """

    eigenvalues: NDArray
    frequencies_hz: NDArray
    structural_participation: NDArray

    def classify_modes(self, threshold: float = 0.5) -> dict[str, NDArray]:
        """Classify modes as structural, acoustic, or coupled.

        Parameters
        ----------
        threshold : float
            Participation threshold. Modes with structural participation > threshold
            are classified as structural; < (1-threshold) as acoustic; otherwise coupled.

        Returns
        -------
        dict
            Keys: "structural", "acoustic", "coupled"; values: arrays of frequencies.
        """
        structural_mask = self.structural_participation > threshold
        acoustic_mask = self.structural_participation < (1.0 - threshold)
        coupled_mask = ~structural_mask & ~acoustic_mask

        return {
            "structural": self.frequencies_hz[structural_mask],
            "acoustic": self.frequencies_hz[acoustic_mask],
            "coupled": self.frequencies_hz[coupled_mask],
        }


def solve_coupled_fsi(
    mesh_path: Path | str,
    n_modes: int = 20,
    wall_youngs_modulus_pa: float = 50_000.0,
    wall_poisson_ratio: float = 0.47,
    wall_density_kg_m3: float = 1050.0,
    fluid_sound_speed_m_s: float = 1500.0,
    fluid_density_kg_m3: float = 1000.0,
    output_dir: Path | str | None = None,
) -> FSIResults:
    """Solve the coupled acoustic–structural eigenvalue problem.

    This sets up a mixed formulation with displacement (u) in the structural
    domain and pressure (p) in the fluid domain, coupled through the
    fluid–structure interface.

    Parameters
    ----------
    mesh_path : Path or str
        Path to the mesh file with tagged domains ("wall" and "fluid").
    n_modes : int
        Number of coupled modes to compute.
    wall_youngs_modulus_pa : float
        Young's modulus of the cavity wall (Pa).
    wall_poisson_ratio : float
        Poisson's ratio of the wall.
    wall_density_kg_m3 : float
        Density of the wall (kg/m³).
    fluid_sound_speed_m_s : float
        Speed of sound in the cavity fluid (m/s).
    fluid_density_kg_m3 : float
        Density of the cavity fluid (kg/m³).
    output_dir : Path or str, optional
        Directory to save results.

    Returns
    -------
    FSIResults
        Coupled eigenvalues, frequencies, and mode classification.

    Raises
    ------
    ImportError
        If FEniCSx is not installed.
    NotImplementedError
        This is a placeholder for the full FSI implementation.
    """
    raise NotImplementedError(
        "Coupled FSI solver is under development. "
        "Use browntone.fem.modal_analysis for structural-only analysis."
    )
