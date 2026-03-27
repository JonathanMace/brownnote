"""Parametric mesh generation for abdominal cavity geometries.

Generates 3D finite element meshes of simplified abdominal cavity models
using the gmsh Python API. Supports ellipsoidal and cylindrical geometries
with configurable dimensions and mesh density.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import click
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class CavityGeometry:
    """Parameters defining the abdominal cavity geometry.

    Parameters
    ----------
    shape : str
        Geometry type: ``"ellipsoid"`` or ``"cylinder"``.
    semi_major_m : float
        Semi-major axis (half-length) in metres.
    semi_minor_m : float
        Semi-minor axis (half-width/radius) in metres.
    wall_thickness_m : float
        Thickness of the abdominal wall in metres.
    element_size_m : float
        Target element size in metres.
    """

    shape: str = "ellipsoid"
    semi_major_m: float = 0.15
    semi_minor_m: float = 0.10
    wall_thickness_m: float = 0.015
    element_size_m: float = 0.005


def generate_cavity_mesh(
    geometry: CavityGeometry | None = None,
    output_path: Path | str = Path("cavity.msh"),
    order: int = 1,
) -> Path:
    """Generate a 3D mesh of the abdominal cavity.

    Parameters
    ----------
    geometry : CavityGeometry, optional
        Geometry parameters. Uses defaults if not provided.
    output_path : Path or str
        Output mesh file path (.msh format).
    order : int
        Element order (1 = linear, 2 = quadratic).

    Returns
    -------
    Path
        Path to the generated mesh file.

    Raises
    ------
    ValueError
        If geometry parameters are invalid.
    RuntimeError
        If mesh generation fails.
    """
    import gmsh

    if geometry is None:
        geometry = CavityGeometry()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    _validate_geometry(geometry)

    gmsh.initialize()
    try:
        gmsh.model.add("abdominal_cavity")
        gmsh.option.setNumber("General.Verbosity", 1)

        if geometry.shape == "ellipsoid":
            _create_ellipsoid(gmsh, geometry)
        elif geometry.shape == "cylinder":
            _create_cylinder(gmsh, geometry)
        else:
            raise ValueError(f"Unknown shape: {geometry.shape}")

        # Set mesh size
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", geometry.element_size_m)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", geometry.element_size_m * 0.5)

        # Generate 3D mesh
        gmsh.model.mesh.generate(3)

        if order > 1:
            gmsh.model.mesh.setOrder(order)

        # Write mesh
        gmsh.write(str(output_path))

        # Log mesh statistics
        node_tags, _, _ = gmsh.model.mesh.getNodes()
        elem_types, _, _ = gmsh.model.mesh.getElements()
        logger.info(
            "Generated mesh: %d nodes, shape=%s, h=%.4f m, saved to %s",
            len(node_tags),
            geometry.shape,
            geometry.element_size_m,
            output_path,
        )

    finally:
        gmsh.finalize()

    return output_path


def _create_ellipsoid(gmsh_module: object, geometry: CavityGeometry) -> None:
    """Create an ellipsoidal cavity with wall thickness in gmsh."""
    gmsh = gmsh_module
    factory = gmsh.model.occ

    a = geometry.semi_major_m
    b = geometry.semi_minor_m
    t = geometry.wall_thickness_m

    # Inner ellipsoid (fluid cavity)
    inner = factory.addSphere(0, 0, 0, 1.0)
    factory.dilate([(3, inner)], 0, 0, 0, a, b, b)

    # Outer ellipsoid (abdominal wall outer surface)
    outer = factory.addSphere(0, 0, 0, 1.0)
    factory.dilate([(3, outer)], 0, 0, 0, a + t, b + t, b + t)

    # Wall = outer - inner
    wall_dimtags, _ = factory.cut([(3, outer)], [(3, inner)], removeObject=True, removeTool=False)

    factory.synchronize()

    # Physical groups
    wall_tags = [dt[1] for dt in wall_dimtags]
    gmsh.model.addPhysicalGroup(3, wall_tags, name="wall")
    gmsh.model.addPhysicalGroup(3, [inner], name="fluid")


def _create_cylinder(gmsh_module: object, geometry: CavityGeometry) -> None:
    """Create a cylindrical cavity with hemispherical end caps in gmsh."""
    gmsh = gmsh_module
    factory = gmsh.model.occ

    R = geometry.semi_minor_m
    L = 2.0 * geometry.semi_major_m
    t = geometry.wall_thickness_m

    # Inner cylinder with hemispherical caps
    cyl_inner = factory.addCylinder(-L / 2, 0, 0, L, 0, 0, R)
    cap1 = factory.addSphere(-L / 2, 0, 0, R)
    cap2 = factory.addSphere(L / 2, 0, 0, R)
    inner_parts, _ = factory.fuse([(3, cyl_inner)], [(3, cap1), (3, cap2)])

    # Outer surface
    cyl_outer = factory.addCylinder(-L / 2, 0, 0, L, 0, 0, R + t)
    cap3 = factory.addSphere(-L / 2, 0, 0, R + t)
    cap4 = factory.addSphere(L / 2, 0, 0, R + t)
    outer_parts, _ = factory.fuse([(3, cyl_outer)], [(3, cap3), (3, cap4)])

    # Wall = outer - inner
    inner_tags = [dt[1] for dt in inner_parts]
    outer_tags = [dt[1] for dt in outer_parts]

    wall_dimtags, _ = factory.cut(
        [(3, t) for t in outer_tags],
        [(3, t) for t in inner_tags],
        removeObject=True,
        removeTool=False,
    )

    factory.synchronize()

    wall_vol_tags = [dt[1] for dt in wall_dimtags]
    inner_vol_tags = [dt[1] for dt in inner_parts]
    gmsh.model.addPhysicalGroup(3, wall_vol_tags, name="wall")
    gmsh.model.addPhysicalGroup(3, inner_vol_tags, name="fluid")


def _validate_geometry(geometry: CavityGeometry) -> None:
    """Validate cavity geometry parameters."""
    if geometry.semi_major_m <= 0:
        raise ValueError(f"Semi-major axis must be positive, got {geometry.semi_major_m}")
    if geometry.semi_minor_m <= 0:
        raise ValueError(f"Semi-minor axis must be positive, got {geometry.semi_minor_m}")
    if geometry.wall_thickness_m <= 0:
        raise ValueError(f"Wall thickness must be positive, got {geometry.wall_thickness_m}")
    if geometry.wall_thickness_m >= geometry.semi_minor_m:
        raise ValueError("Wall thickness must be less than semi-minor axis")
    if geometry.element_size_m <= 0:
        raise ValueError(f"Element size must be positive, got {geometry.element_size_m}")


def load_and_inspect(mesh_path: Path | str) -> dict:
    """Load a mesh file and print inspection statistics.

    Parameters
    ----------
    mesh_path : Path or str
        Path to the mesh file.

    Returns
    -------
    dict
        Mesh statistics including node count, element count, and bounding box.
    """
    import meshio

    mesh = meshio.read(str(mesh_path))

    n_nodes = len(mesh.points)
    n_cells = sum(len(block.data) for block in mesh.cells)
    bbox_min = mesh.points.min(axis=0)
    bbox_max = mesh.points.max(axis=0)

    stats = {
        "n_nodes": n_nodes,
        "n_cells": n_cells,
        "cell_types": [block.type for block in mesh.cells],
        "bounding_box": {
            "min": bbox_min.tolist(),
            "max": bbox_max.tolist(),
        },
    }

    logger.info("Mesh: %d nodes, %d cells", n_nodes, n_cells)
    logger.info("Bounding box: %s to %s", bbox_min, bbox_max)
    logger.info("Cell types: %s", stats["cell_types"])

    return stats


@click.command("bt-mesh")
@click.option("--geometry", type=click.Choice(["ellipsoid", "cylinder"]), default="ellipsoid")
@click.option("--semi-major", type=float, default=0.15, help="Semi-major axis (m)")
@click.option("--semi-minor", type=float, default=0.10, help="Semi-minor axis (m)")
@click.option("--thickness", type=float, default=0.015, help="Wall thickness (m)")
@click.option("--element-size", type=float, default=0.005, help="Target element size (m)")
@click.option("--order", type=int, default=1, help="Element order")
@click.option("-o", "--output", type=click.Path(), default="cavity.msh", help="Output path")
def main(
    geometry: str,
    semi_major: float,
    semi_minor: float,
    thickness: float,
    element_size: float,
    order: int,
    output: str,
) -> None:
    """Generate an abdominal cavity mesh."""
    logging.basicConfig(level=logging.INFO)

    geo = CavityGeometry(
        shape=geometry,
        semi_major_m=semi_major,
        semi_minor_m=semi_minor,
        wall_thickness_m=thickness,
        element_size_m=element_size,
    )

    path = generate_cavity_mesh(geo, output_path=Path(output), order=order)
    click.echo(f"Mesh written to {path}")


if __name__ == "__main__":
    main()
