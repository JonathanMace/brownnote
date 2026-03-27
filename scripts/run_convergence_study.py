#!/usr/bin/env python
"""Run a mesh convergence study.

Generates meshes at several resolutions, solves the modal problem for each,
and computes Richardson extrapolation to estimate mesh-independent values.

Usage:
    python scripts/run_convergence_study.py
    python scripts/run_convergence_study.py --mesh-sizes 0.020 0.010 0.005 0.0025
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import click
import numpy as np

from browntone.mesh.abdominal_cavity import CavityGeometry, generate_cavity_mesh, load_and_inspect
from browntone.postprocess.extraction import compute_richardson_extrapolation
from browntone.postprocess.visualization import plot_convergence, set_publication_style
from browntone.utils.materials import get_material

logger = logging.getLogger(__name__)

DEFAULT_MESH_SIZES = [0.020, 0.010, 0.005, 0.0025]
RESULTS_DIR = Path("data/results/convergence")


@click.command()
@click.option(
    "--mesh-sizes",
    type=float,
    multiple=True,
    default=DEFAULT_MESH_SIZES,
    help="Element sizes to test (m). Specify multiple times.",
)
@click.option(
    "--geometry",
    type=click.Choice(["ellipsoid", "cylinder"]),
    default="ellipsoid",
)
@click.option("--n-modes", type=int, default=10)
@click.option(
    "--output",
    type=click.Path(),
    default=str(RESULTS_DIR),
    help="Output directory",
)
def main(
    mesh_sizes: tuple[float, ...],
    geometry: str,
    n_modes: int,
    output: str,
) -> None:
    """Run mesh convergence study."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)

    material = get_material("soft-tissue")
    convergence_data: list[dict] = []

    for h in sorted(mesh_sizes, reverse=True):  # coarsest first
        logger.info("=== Mesh size: %.4f m ===", h)

        geo = CavityGeometry(shape=geometry, element_size_m=h)
        mesh_dir = out_dir / f"h_{h:.4f}"
        mesh_dir.mkdir(parents=True, exist_ok=True)

        # Generate mesh
        mesh_path = generate_cavity_mesh(
            geometry=geo,
            output_path=mesh_dir / "mesh.msh",
        )

        stats = load_and_inspect(mesh_path)

        # Solve (requires FEniCSx)
        try:
            from browntone.fem.modal_analysis import solve_modal

            results = solve_modal(
                mesh_path=mesh_path,
                n_modes=n_modes,
                youngs_modulus_pa=material.youngs_modulus_pa,
                poisson_ratio=material.poisson_ratio,
                density_kg_m3=material.density_kg_m3,
                output_dir=mesh_dir,
            )

            convergence_data.append({
                "element_size_m": h,
                "n_nodes": stats["n_nodes"],
                "n_cells": stats["n_cells"],
                "frequencies_hz": results.frequencies_hz.tolist(),
                "n_dofs": results.n_dofs,
            })

        except ImportError:
            logger.warning(
                "FEniCSx not available. Recording mesh stats only."
            )
            convergence_data.append({
                "element_size_m": h,
                "n_nodes": stats["n_nodes"],
                "n_cells": stats["n_cells"],
                "frequencies_hz": [],
                "n_dofs": 0,
            })

    # Save convergence data
    with open(out_dir / "convergence_data.json", "w") as f:
        json.dump(convergence_data, f, indent=2)

    # Richardson extrapolation (if we have FEA results)
    if convergence_data and len(convergence_data[-1].get("frequencies_hz", [])) > 0:
        h_values = np.array([d["element_size_m"] for d in convergence_data])
        f1_values = np.array([d["frequencies_hz"][0] for d in convergence_data])

        richardson = compute_richardson_extrapolation(h_values, f1_values)

        with open(out_dir / "richardson_results.json", "w") as f:
            json.dump(richardson, f, indent=2)

        # Convergence plot
        set_publication_style()
        plot_convergence(
            h_values,
            f1_values,
            qoi_label=r"$f_1$ (Hz)",
            extrapolated_value=richardson["extrapolated_value"],
            save_to=out_dir / "convergence_plot.pdf",
        )

        logger.info(
            "Richardson extrapolation: f_exact=%.4f Hz, p=%.2f, GCI=%.4f%%",
            richardson["extrapolated_value"],
            richardson["observed_order"],
            richardson["gci_fine"] * 100,
        )

    logger.info("Convergence study complete. Results in %s", out_dir)


if __name__ == "__main__":
    main()
