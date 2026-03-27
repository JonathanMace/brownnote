"""Visualization functions for simulation results.

Publication-quality figure generation using matplotlib and PyVista.
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)

# Project colour palette
COLOURS = {
    "primary": "#2166AC",
    "secondary": "#B2182B",
    "tertiary": "#4DAF4A",
    "quaternary": "#FF7F00",
    "quinary": "#984EA3",
}

COLOUR_LIST = list(COLOURS.values())


def set_publication_style() -> None:
    """Configure matplotlib for publication-quality figures.

    Sets font sizes, line widths, and other parameters suitable for
    single-column journal figures (~85 mm wide).
    """
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
            "font.family": "serif",
            "font.size": 9,
            "mathtext.fontset": "cm",
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "lines.linewidth": 1.2,
            "lines.markersize": 4,
            "axes.grid": True,
            "grid.alpha": 0.3,
        }
    )


def plot_eigenfrequencies(
    frequencies_hz: NDArray,
    n_modes: int | None = None,
    analytical_hz: NDArray | None = None,
    save_to: Path | str | None = None,
    title: str = "",
) -> plt.Figure:
    """Create a bar chart of eigenfrequencies.

    Parameters
    ----------
    frequencies_hz : NDArray
        Computed eigenfrequencies in Hz.
    n_modes : int, optional
        Number of modes to plot. Defaults to all.
    analytical_hz : NDArray, optional
        Analytical comparison values (plotted as markers).
    save_to : Path or str, optional
        Path to save the figure.
    title : str
        Figure title.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.
    """
    set_publication_style()

    if n_modes is not None:
        frequencies_hz = frequencies_hz[:n_modes]
        if analytical_hz is not None:
            analytical_hz = analytical_hz[:n_modes]

    n = len(frequencies_hz)
    modes = np.arange(1, n + 1)

    fig, ax = plt.subplots(figsize=(3.35, 2.5))

    ax.bar(modes, frequencies_hz, color=COLOURS["primary"], alpha=0.8, label="FEA")

    if analytical_hz is not None:
        ax.scatter(
            modes,
            analytical_hz,
            color=COLOURS["secondary"],
            marker="x",
            s=30,
            zorder=5,
            label="Analytical",
        )

    ax.set_xlabel("Mode number")
    ax.set_ylabel("Frequency (Hz)")
    if title:
        ax.set_title(title)
    ax.set_xticks(modes)
    if analytical_hz is not None:
        ax.legend()

    fig.tight_layout()

    if save_to is not None:
        save_to = Path(save_to)
        save_to.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_to)
        logger.info("Figure saved to %s", save_to)

    return fig


def plot_convergence(
    mesh_sizes: NDArray,
    qoi_values: NDArray,
    qoi_label: str = "Frequency (Hz)",
    extrapolated_value: float | None = None,
    save_to: Path | str | None = None,
) -> plt.Figure:
    """Plot mesh convergence of a quantity of interest.

    Parameters
    ----------
    mesh_sizes : NDArray
        Element sizes (m) or reciprocals for x-axis.
    qoi_values : NDArray
        Quantity of interest at each mesh size.
    qoi_label : str
        Label for the y-axis.
    extrapolated_value : float, optional
        Richardson-extrapolated value (plotted as horizontal line).
    save_to : Path or str, optional
        Path to save the figure.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(3.35, 2.5))

    # Plot as 1/h (higher = finer mesh)
    x = 1.0 / np.array(mesh_sizes)

    ax.plot(x, qoi_values, "o-", color=COLOURS["primary"], label="Computed")

    if extrapolated_value is not None:
        ax.axhline(
            y=extrapolated_value,
            ls="--",
            color=COLOURS["secondary"],
            alpha=0.7,
            label=f"Extrapolated = {extrapolated_value:.2f}",
        )

    ax.set_xlabel(r"$1/h$ (m$^{-1}$)")
    ax.set_ylabel(qoi_label)
    ax.set_xscale("log")
    ax.legend()

    fig.tight_layout()

    if save_to is not None:
        save_to = Path(save_to)
        save_to.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_to)
        logger.info("Figure saved to %s", save_to)

    return fig


def plot_parametric_heatmap(
    param_x: NDArray,
    param_y: NDArray,
    values: NDArray,
    xlabel: str = "Parameter X",
    ylabel: str = "Parameter Y",
    zlabel: str = "Response",
    save_to: Path | str | None = None,
) -> plt.Figure:
    """Create a heat map for a two-parameter study.

    Parameters
    ----------
    param_x : NDArray
        Values of the first parameter (1D).
    param_y : NDArray
        Values of the second parameter (1D).
    values : NDArray
        Response values (2D array, shape = [len(param_y), len(param_x)]).
    xlabel, ylabel, zlabel : str
        Axis labels.
    save_to : Path or str, optional
        Path to save the figure.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(3.35, 3.0))

    X, Y = np.meshgrid(param_x, param_y)
    pcm = ax.pcolormesh(X, Y, values, cmap="cividis", shading="auto")
    cbar = fig.colorbar(pcm, ax=ax, label=zlabel)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.tight_layout()

    if save_to is not None:
        save_to = Path(save_to)
        save_to.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_to)
        logger.info("Figure saved to %s", save_to)

    return fig
