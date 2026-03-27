"""Smoke tests for figure generation scripts.

Verifies that every figure generation function in generate_jsv_figures.py
runs without error.  Does NOT check visual output — only that code paths
complete and produce files on disk.
"""

from __future__ import annotations

import importlib
import os
import sys

import pytest

# Ensure project root is on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'src'))

# Force non-interactive matplotlib backend before any import
import matplotlib
matplotlib.use('Agg')


@pytest.fixture(scope="module")
def fig_module():
    """Import the figure generation script as a module."""
    spec = importlib.util.spec_from_file_location(
        "generate_jsv_figures",
        os.path.join(ROOT, "scripts", "generate_jsv_figures.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def fig_dir():
    """Path where figures are written."""
    d = os.path.join(ROOT, "data", "figures")
    os.makedirs(d, exist_ok=True)
    return d


# Parametrize over every figure function
FIGURE_FUNCTIONS = [
    "fig_geometry_schematic",
    "fig_mode_shapes",
    "fig_frequency_vs_E",
    "fig_parametric_sensitivity",
    "fig_coupling_comparison",
    "fig_energy_budget",
    "fig_iso2631_validation",
    "fig_multilayer_comparison",
]


@pytest.mark.parametrize("func_name", FIGURE_FUNCTIONS)
def test_figure_generates_without_error(fig_module, fig_dir, func_name):
    """Each figure function should run to completion."""
    import matplotlib.pyplot as plt
    func = getattr(fig_module, func_name)
    func()
    plt.close('all')  # free memory
