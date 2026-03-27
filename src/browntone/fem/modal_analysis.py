"""Modal analysis solver using FEniCSx and SLEPc.

Solves the generalised eigenvalue problem K φ = ω² M φ for the natural
frequencies and mode shapes of the abdominal cavity structure.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import click
import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


@dataclass
class ModalResults:
    """Container for modal analysis results.

    Parameters
    ----------
    eigenvalues : NDArray
        Array of eigenvalues (ω² in rad²/s²).
    frequencies_hz : NDArray
        Natural frequencies in hertz.
    mesh_path : Path
        Path to the mesh used.
    n_dofs : int
        Number of degrees of freedom.
    """

    eigenvalues: NDArray
    frequencies_hz: NDArray
    mesh_path: Path
    n_dofs: int

    def print_summary(self) -> None:
        """Print a table of eigenfrequencies."""
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title="Modal Analysis Results")
        table.add_column("Mode", justify="right")
        table.add_column("Frequency (Hz)", justify="right")
        table.add_column("Period (s)", justify="right")

        for i, freq in enumerate(self.frequencies_hz):
            period = 1.0 / freq if freq > 0 else float("inf")
            table.add_row(f"{i + 1}", f"{freq:.4f}", f"{period:.4f}")

        console.print(table)
        console.print(f"DOFs: {self.n_dofs}")


def solve_modal(
    mesh_path: Path | str,
    n_modes: int = 20,
    youngs_modulus_pa: float = 50_000.0,
    poisson_ratio: float = 0.47,
    density_kg_m3: float = 1050.0,
    element_order: int = 2,
    output_dir: Path | str | None = None,
) -> ModalResults:
    """Run a structural modal analysis on the cavity wall.

    Solves K φ = ω² M φ using FEniCSx and SLEPc.

    Parameters
    ----------
    mesh_path : Path or str
        Path to the mesh file (XDMF or MSH).
    n_modes : int
        Number of eigenvalues to compute.
    youngs_modulus_pa : float
        Young's modulus of the wall material in Pa.
    poisson_ratio : float
        Poisson's ratio (< 0.5 for compressible; use mixed formulation if > 0.49).
    density_kg_m3 : float
        Material density in kg/m³.
    element_order : int
        Polynomial order of the finite elements.
    output_dir : Path or str, optional
        Directory to save results. If None, results are not saved.

    Returns
    -------
    ModalResults
        Eigenvalues and frequencies.

    Raises
    ------
    ImportError
        If FEniCSx/DOLFINx is not installed.
    """
    try:
        import dolfinx
        import dolfinx.fem
        import dolfinx.io
        import ufl
        from mpi4py import MPI
        from petsc4py import PETSc
        from slepc4py import SLEPc
    except ImportError as e:
        raise ImportError(
            "FEniCSx stack (dolfinx, ufl, petsc4py, slepc4py) is required "
            "for modal analysis. Install with: pip install browntone[fenics] "
            "or use the Docker container."
        ) from e

    mesh_path = Path(mesh_path)
    logger.info("Starting modal analysis: mesh=%s, n_modes=%d", mesh_path, n_modes)

    # Read mesh
    with dolfinx.io.XDMFFile(MPI.COMM_WORLD, str(mesh_path), "r") as xdmf:
        domain = xdmf.read_mesh(name="Grid")

    # Function space (vector for displacement)
    V = dolfinx.fem.functionspace(domain, ("Lagrange", element_order, (domain.geometry.dim,)))
    n_dofs = V.dofmap.index_map.size_global * V.dofmap.index_map_bs

    logger.info("Function space: %d DOFs", n_dofs)

    # Material parameters (Lamé constants)
    E = dolfinx.fem.Constant(domain, PETSc.ScalarType(youngs_modulus_pa))
    nu = dolfinx.fem.Constant(domain, PETSc.ScalarType(poisson_ratio))
    rho = dolfinx.fem.Constant(domain, PETSc.ScalarType(density_kg_m3))

    lmbda = E * nu / ((1 + nu) * (1 - 2 * nu))
    mu = E / (2 * (1 + nu))

    # Variational forms
    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)

    def epsilon(w):
        return ufl.sym(ufl.grad(w))

    def sigma(w):
        return lmbda * ufl.tr(epsilon(w)) * ufl.Identity(len(w)) + 2 * mu * epsilon(w)

    # Stiffness: a(u, v) = ∫ σ(u) : ε(v) dx
    k_form = ufl.inner(sigma(u), epsilon(v)) * ufl.dx

    # Mass: m(u, v) = ∫ ρ u · v dx
    m_form = rho * ufl.inner(u, v) * ufl.dx

    # Assemble
    K = dolfinx.fem.petsc.assemble_matrix(dolfinx.fem.form(k_form))
    K.assemble()
    M = dolfinx.fem.petsc.assemble_matrix(dolfinx.fem.form(m_form))
    M.assemble()

    # Eigenvalue solver (SLEPc)
    eigensolver = SLEPc.EPS().create(MPI.COMM_WORLD)
    eigensolver.setOperators(K, M)
    eigensolver.setProblemType(SLEPc.EPS.ProblemType.GHEP)
    eigensolver.setType(SLEPc.EPS.Type.KRYLOVSCHUR)
    eigensolver.setWhichEigenpairs(SLEPc.EPS.Which.SMALLEST_MAGNITUDE)
    eigensolver.setDimensions(nev=n_modes)

    # Spectral transform: shift-invert to find smallest eigenvalues
    st = eigensolver.getST()
    st.setType(SLEPc.ST.Type.SINVERT)
    st.setShift(0.1)

    eigensolver.solve()

    n_converged = eigensolver.getConverged()
    logger.info("Converged eigenvalues: %d / %d requested", n_converged, n_modes)

    # Extract eigenvalues
    eigenvalues = []
    for i in range(min(n_converged, n_modes)):
        eigval = eigensolver.getEigenvalue(i)
        if eigval.real > 0:
            eigenvalues.append(eigval.real)

    eigenvalues_arr = np.array(sorted(eigenvalues))
    frequencies_hz = np.sqrt(eigenvalues_arr) / (2.0 * np.pi)

    results = ModalResults(
        eigenvalues=eigenvalues_arr,
        frequencies_hz=frequencies_hz,
        mesh_path=mesh_path,
        n_dofs=n_dofs,
    )

    # Save results
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        np.savez(
            output_dir / "modal_results.npz",
            eigenvalues=eigenvalues_arr,
            frequencies_hz=frequencies_hz,
        )
        logger.info("Results saved to %s", output_dir / "modal_results.npz")

    results.print_summary()
    return results


@click.command("bt-modal")
@click.option("--mesh", "mesh_path", required=True, type=click.Path(exists=True))
@click.option("--n-modes", type=int, default=20, help="Number of modes to extract")
@click.option("--youngs-modulus", type=float, default=50_000.0, help="Young's modulus (Pa)")
@click.option("--poisson-ratio", type=float, default=0.47, help="Poisson's ratio")
@click.option("--density", type=float, default=1050.0, help="Density (kg/m³)")
@click.option("--order", type=int, default=2, help="Element order")
@click.option("-o", "--output", type=click.Path(), default=None, help="Output directory")
def main(
    mesh_path: str,
    n_modes: int,
    youngs_modulus: float,
    poisson_ratio: float,
    density: float,
    order: int,
    output: str | None,
) -> None:
    """Run structural modal analysis."""
    logging.basicConfig(level=logging.INFO)

    solve_modal(
        mesh_path=Path(mesh_path),
        n_modes=n_modes,
        youngs_modulus_pa=youngs_modulus,
        poisson_ratio=poisson_ratio,
        density_kg_m3=density,
        element_order=order,
        output_dir=Path(output) if output else None,
    )


if __name__ == "__main__":
    main()
