"""Data extraction from simulation results.

Functions for loading and processing FEA output files (XDMF, HDF5, NPZ).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


@dataclass
class ModalResultData:
    """Loaded modal analysis data.

    Parameters
    ----------
    eigenvalues : NDArray
        Eigenvalues (ω² in rad²/s²).
    frequencies_hz : NDArray
        Natural frequencies in hertz.
    source_path : Path
        Path the data was loaded from.
    """

    eigenvalues: NDArray
    frequencies_hz: NDArray
    source_path: Path

    @property
    def n_modes(self) -> int:
        """Number of modes."""
        return len(self.frequencies_hz)

    def print_summary(self) -> None:
        """Print a formatted summary table."""
        print(f"\nModal Results from: {self.source_path}")
        print(f"{'Mode':>6} {'Frequency (Hz)':>16} {'Period (s)':>12}")
        print("-" * 36)
        for i, freq in enumerate(self.frequencies_hz):
            period = 1.0 / freq if freq > 0 else float("inf")
            print(f"{i + 1:>6} {freq:>16.4f} {period:>12.4f}")


def load_modal_results(results_dir: Path | str) -> ModalResultData:
    """Load modal analysis results from a directory.

    Looks for ``modal_results.npz`` in the given directory.

    Parameters
    ----------
    results_dir : Path or str
        Directory containing modal analysis output.

    Returns
    -------
    ModalResultData
        Loaded results.

    Raises
    ------
    FileNotFoundError
        If the results file is not found.
    """
    results_dir = Path(results_dir)
    npz_path = results_dir / "modal_results.npz"

    if not npz_path.exists():
        raise FileNotFoundError(
            f"Modal results not found at {npz_path}. "
            "Run a modal analysis first with bt-modal."
        )

    data = np.load(npz_path)
    logger.info("Loaded %d modes from %s", len(data["frequencies_hz"]), npz_path)

    return ModalResultData(
        eigenvalues=data["eigenvalues"],
        frequencies_hz=data["frequencies_hz"],
        source_path=npz_path,
    )


def compute_richardson_extrapolation(
    h_values: NDArray,
    qoi_values: NDArray,
    refinement_ratio: float | None = None,
) -> dict[str, float]:
    """Perform Richardson extrapolation on mesh convergence data.

    Uses three consecutive mesh sizes to estimate the exact solution and
    the observed order of convergence.

    Parameters
    ----------
    h_values : NDArray
        Element sizes (must have at least 3 values, coarsest to finest).
    qoi_values : NDArray
        Quantity of interest at each mesh size.
    refinement_ratio : float, optional
        Constant refinement ratio. If None, computed from h_values.

    Returns
    -------
    dict
        Keys: ``"extrapolated_value"``, ``"observed_order"``, ``"gci_fine"``
        (Grid Convergence Index for the finest mesh).

    Raises
    ------
    ValueError
        If fewer than 3 data points are provided.
    """
    if len(h_values) < 3:
        raise ValueError("Need at least 3 mesh sizes for Richardson extrapolation")

    # Use the three finest meshes
    h1, h2, h3 = h_values[-1], h_values[-2], h_values[-3]
    f1, f2, f3 = qoi_values[-1], qoi_values[-2], qoi_values[-3]

    if refinement_ratio is None:
        r = h2 / h1
    else:
        r = refinement_ratio

    # Observed order of convergence
    epsilon_32 = f3 - f2
    epsilon_21 = f2 - f1

    if abs(epsilon_21) < 1e-15 or abs(epsilon_32) < 1e-15:
        logger.warning("Near-zero differences in convergence data; results may be unreliable")
        return {
            "extrapolated_value": float(f1),
            "observed_order": float("inf"),
            "gci_fine": 0.0,
        }

    p = np.log(abs(epsilon_32 / epsilon_21)) / np.log(r)

    # Extrapolated value
    f_exact = f1 + (f1 - f2) / (r**p - 1.0)

    # Grid Convergence Index (safety factor F_s = 1.25 for 3+ grids)
    F_s = 1.25
    gci_fine = F_s * abs((f1 - f2) / f1) / (r**p - 1.0)

    result = {
        "extrapolated_value": float(f_exact),
        "observed_order": float(p),
        "gci_fine": float(gci_fine),
    }

    logger.info(
        "Richardson extrapolation: f_exact=%.6f, p=%.2f, GCI=%.4f%%",
        f_exact,
        p,
        gci_fine * 100,
    )

    return result
