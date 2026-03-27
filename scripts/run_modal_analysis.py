#!/usr/bin/env python
"""Run a modal analysis of the abdominal cavity.

This script orchestrates the full mesh → solve → postprocess pipeline
for a structural modal analysis.

Usage:
    python scripts/run_modal_analysis.py
    python scripts/run_modal_analysis.py --config data/materials/default.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import click
import numpy as np

from browntone.analytical.shell_vibration import cylindrical_shell_frequencies
from browntone.mesh.abdominal_cavity import CavityGeometry, generate_cavity_mesh
from browntone.postprocess.visualization import plot_eigenfrequencies, set_publication_style
from browntone.utils.materials import Material, get_material

logger = logging.getLogger(__name__)

RESULTS_DIR = Path("data/results/modal_default")


@click.command()
@click.option(
    "--config",
    type=click.Path(exists=True),
    default=None,
    help="JSON configuration file",
)
@click.option("--n-modes", type=int, default=20, help="Number of modes to extract")
@click.option("--element-size", type=float, default=0.005, help="Mesh element size (m)")
@click.option(
    "--output-dir",
    type=click.Path(),
    default=str(RESULTS_DIR),
    help="Output directory",
)
@click.option("--analytical-only", is_flag=True, help="Only compute analytical solution")
def main(
    config: str | None,
    n_modes: int,
    element_size: float,
    output_dir: str,
    analytical_only: bool,
) -> None:
    """Run modal analysis pipeline."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load or use default material
    material = get_material("soft-tissue")
    geometry = CavityGeometry(element_size_m=element_size)

    if config:
        with open(config) as f:
            cfg = json.load(f)
        logger.info("Loaded config from %s", config)

    # --- Step 1: Analytical solution ---
    logger.info("Computing analytical shell frequencies...")
    analytical_modes = cylindrical_shell_frequencies(
        radius_m=geometry.semi_minor_m,
        length_m=2.0 * geometry.semi_major_m,
        thickness_m=geometry.wall_thickness_m,
        material=material,
        m_max=5,
        n_max=10,
    )

    analytical_freqs = np.array([m.frequency_hz for m in analytical_modes[:n_modes]])
    logger.info(
        "Analytical fundamental frequency: %.2f Hz",
        analytical_freqs[0] if len(analytical_freqs) > 0 else 0,
    )

    # Save analytical results
    np.savez(
        out_dir / "analytical_results.npz",
        frequencies_hz=analytical_freqs,
    )

    if analytical_only:
        logger.info("Analytical-only mode; skipping FEA.")
        return

    # --- Step 2: Generate mesh ---
    logger.info("Generating mesh...")
    mesh_path = generate_cavity_mesh(
        geometry=geometry,
        output_path=out_dir / "mesh.msh",
    )
    logger.info("Mesh written to %s", mesh_path)

    # --- Step 3: Run FEA (requires FEniCSx) ---
    try:
        from browntone.fem.modal_analysis import solve_modal

        logger.info("Running FEA modal analysis...")
        results = solve_modal(
            mesh_path=mesh_path,
            n_modes=n_modes,
            youngs_modulus_pa=material.youngs_modulus_pa,
            poisson_ratio=material.poisson_ratio,
            density_kg_m3=material.density_kg_m3,
            output_dir=out_dir,
        )
    except ImportError:
        logger.warning(
            "FEniCSx not available. Skipping FEA. "
            "Use Docker or install with: pip install browntone[fenics]"
        )
        return

    # --- Step 4: Comparison plot ---
    logger.info("Generating comparison plot...")
    set_publication_style()
    fig = plot_eigenfrequencies(
        results.frequencies_hz,
        n_modes=min(10, len(results.frequencies_hz)),
        analytical_hz=analytical_freqs[:10] if len(analytical_freqs) >= 10 else analytical_freqs,
        save_to=out_dir / "eigenfrequency_comparison.pdf",
        title="Analytical vs FEA Eigenfrequencies",
    )

    logger.info("Done. Results saved to %s", out_dir)


if __name__ == "__main__":
    main()
