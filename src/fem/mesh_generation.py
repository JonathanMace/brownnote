"""Mesh generation for hemispherical fluid-filled shell FEA modal analysis.

Generates gmsh meshes of oblate-spheroid shells (complete and hemispherical)
with fluid interiors, suitable for eigenvalue analysis of coupled
fluid-structure interaction modes.  Two configurations are produced:

1. **Complete sphere** – validates analytical predictions.
2. **Hemisphere** clamped at the equatorial rim – models the anterior
   abdominal wall with rigid posterior boundary (spine/pelvis).

Shell surfaces are meshed with triangles (for shell elements with assigned
thickness) and the fluid interior is meshed with tetrahedra (for acoustic
elements).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

@dataclass
class ShellMeshParams:
    """Parameters for the oblate-spheroid shell mesh.

    Parameters
    ----------
    semi_major_m : float
        Equatorial semi-axis *a* of the oblate spheroid (metres).
    semi_minor_m : float
        Polar semi-axis *c* of the oblate spheroid (metres).
    wall_thickness_m : float
        Shell wall thickness *h* (metres).  Stored as a physical property
        for shell elements; the geometry uses the mid-surface only.
    element_size_m : float
        Target characteristic element length (metres).
    mesh_order : int
        Polynomial order of elements (1 = linear, 2 = quadratic).
    """

    semi_major_m: float = 0.18
    semi_minor_m: float = 0.12
    wall_thickness_m: float = 0.01
    element_size_m: float = 0.008
    mesh_order: int = 2


def _validate_params(params: ShellMeshParams) -> None:
    """Raise ``ValueError`` if any parameter is out of range."""
    if params.semi_major_m <= 0:
        msg = f"semi_major_m must be positive, got {params.semi_major_m}"
        raise ValueError(msg)
    if params.semi_minor_m <= 0:
        msg = f"semi_minor_m must be positive, got {params.semi_minor_m}"
        raise ValueError(msg)
    if params.wall_thickness_m <= 0:
        msg = f"wall_thickness_m must be positive, got {params.wall_thickness_m}"
        raise ValueError(msg)
    if params.wall_thickness_m >= min(params.semi_major_m, params.semi_minor_m):
        msg = "wall_thickness_m must be less than smallest semi-axis"
        raise ValueError(msg)
    if params.element_size_m <= 0:
        msg = f"element_size_m must be positive, got {params.element_size_m}"
        raise ValueError(msg)
    if params.mesh_order not in (1, 2):
        msg = f"mesh_order must be 1 or 2, got {params.mesh_order}"
        raise ValueError(msg)


# ---------------------------------------------------------------------------
# Complete sphere
# ---------------------------------------------------------------------------

def generate_complete_sphere(
    params: ShellMeshParams | None = None,
    output_dir: Path | str = Path("data/meshes"),
) -> tuple[Path, dict[str, Any]]:
    """Generate a mesh for a complete oblate-spheroid shell with fluid interior.

    The ellipsoidal mid-surface is meshed with triangles (physical group
    ``"shell"``) and the enclosed volume with tetrahedra (physical group
    ``"fluid"``).  Suitable for comparison with closed-form eigenvalue
    predictions of coupled fluid-structure modes.

    Parameters
    ----------
    params : ShellMeshParams | None
        Mesh parameters.  Defaults are used when *None*.
    output_dir : Path | str
        Directory for the output ``.msh`` file.

    Returns
    -------
    tuple[Path, dict]
        Path to the generated ``.msh`` file and a statistics dict.

    Raises
    ------
    ValueError
        If geometry parameters are invalid.
    """
    import gmsh

    if params is None:
        params = ShellMeshParams()
    _validate_params(params)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "complete_sphere.msh"

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Verbosity", 1)
        gmsh.model.add("complete_sphere")
        factory = gmsh.model.occ

        # Oblate spheroid: unit sphere scaled to (a, a, c)
        sphere = factory.addSphere(0, 0, 0, 1.0)
        factory.dilate(
            [(3, sphere)], 0, 0, 0,
            params.semi_major_m, params.semi_major_m, params.semi_minor_m,
        )
        factory.synchronize()

        # Tag physical groups
        volumes = gmsh.model.getEntities(dim=3)
        surfaces = gmsh.model.getEntities(dim=2)

        gmsh.model.addPhysicalGroup(
            3, [v[1] for v in volumes], name="fluid",
        )
        gmsh.model.addPhysicalGroup(
            2, [s[1] for s in surfaces], name="shell",
        )

        # Mesh controls
        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMax", params.element_size_m,
        )
        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMin", params.element_size_m * 0.3,
        )

        gmsh.model.mesh.generate(3)
        gmsh.model.mesh.setOrder(params.mesh_order)

        gmsh.write(str(output_path))
        logger.info("Complete sphere mesh → %s", output_path)

        stats = _collect_mesh_stats()
    finally:
        gmsh.finalize()

    return output_path, stats


# ---------------------------------------------------------------------------
# Hemisphere (anterior abdominal wall)
# ---------------------------------------------------------------------------

def generate_hemisphere(
    params: ShellMeshParams | None = None,
    output_dir: Path | str = Path("data/meshes"),
) -> tuple[Path, dict[str, Any]]:
    """Generate a mesh for a hemispherical shell clamped at the equatorial rim.

    The anterior (z ≥ 0) hemisphere of an oblate spheroid is extracted by
    boolean subtraction.  Physical groups:

    * ``"fluid"`` – tetrahedral volume
    * ``"shell"`` – curved shell surface (triangles)
    * ``"equatorial_plane"`` – flat closing surface at z = 0
    * ``"clamped_rim"`` – equatorial edge curve (for clamped BCs)

    Parameters
    ----------
    params : ShellMeshParams | None
        Mesh parameters.  Defaults are used when *None*.
    output_dir : Path | str
        Directory for the output ``.msh`` file.

    Returns
    -------
    tuple[Path, dict]
        Path to the generated ``.msh`` file and a statistics dict.

    Raises
    ------
    ValueError
        If geometry parameters are invalid.
    """
    import gmsh

    if params is None:
        params = ShellMeshParams()
    _validate_params(params)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "hemisphere.msh"

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Verbosity", 1)
        gmsh.model.add("hemisphere")
        factory = gmsh.model.occ

        a = params.semi_major_m
        c = params.semi_minor_m

        # Full oblate spheroid
        sphere = factory.addSphere(0, 0, 0, 1.0)
        factory.dilate(
            [(3, sphere)], 0, 0, 0, a, a, c,
        )

        # Box covering z < 0 → remove the posterior hemisphere
        box = factory.addBox(-2 * a, -2 * a, -2 * c, 4 * a, 4 * a, 2 * c)

        factory.cut([(3, sphere)], [(3, box)])
        factory.synchronize()

        # --- Classify surfaces ------------------------------------------------
        surfaces = gmsh.model.getEntities(dim=2)
        shell_tags: list[int] = []
        equatorial_tags: list[int] = []

        for _dim, tag in surfaces:
            bbox = gmsh.model.getBoundingBox(2, tag)
            z_extent = bbox[5] - bbox[2]  # zmax - zmin
            if z_extent < 1e-6:
                equatorial_tags.append(tag)
            else:
                shell_tags.append(tag)

        # Equatorial rim = boundary curves of the flat surface
        rim_curves: list[int] = []
        for stag in equatorial_tags:
            boundary = gmsh.model.getBoundary([(2, stag)], oriented=False)
            rim_curves.extend(c[1] for c in boundary)

        # --- Physical groups --------------------------------------------------
        volumes = gmsh.model.getEntities(dim=3)
        gmsh.model.addPhysicalGroup(
            3, [v[1] for v in volumes], name="fluid",
        )
        gmsh.model.addPhysicalGroup(2, shell_tags, name="shell")
        gmsh.model.addPhysicalGroup(
            2, equatorial_tags, name="equatorial_plane",
        )
        if rim_curves:
            gmsh.model.addPhysicalGroup(1, rim_curves, name="clamped_rim")

        # --- Mesh controls ----------------------------------------------------
        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMax", params.element_size_m,
        )
        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMin", params.element_size_m * 0.3,
        )

        gmsh.model.mesh.generate(3)
        gmsh.model.mesh.setOrder(params.mesh_order)

        gmsh.write(str(output_path))
        logger.info("Hemisphere mesh → %s", output_path)

        stats = _collect_mesh_stats()
    finally:
        gmsh.finalize()

    return output_path, stats


# ---------------------------------------------------------------------------
# Mesh statistics
# ---------------------------------------------------------------------------

_ELEM_TYPE_NAMES: dict[int, str] = {
    1: "line2",
    2: "tri3",
    4: "tet4",
    8: "line3",
    9: "tri6",
    11: "tet10",
    15: "point",
}


def _collect_mesh_stats() -> dict[str, Any]:
    """Return node/element counts from the active gmsh model."""
    import gmsh

    node_tags, _, _ = gmsh.model.mesh.getNodes()
    elem_types, elem_tags, _ = gmsh.model.mesh.getElements()

    elements: dict[str, int] = {}
    total = 0
    for etype, etags in zip(elem_types, elem_tags):
        name = _ELEM_TYPE_NAMES.get(etype, f"type_{etype}")
        count = len(etags)
        elements[name] = count
        total += count

    return {
        "nodes": len(node_tags),
        "elements": elements,
        "total_elements": total,
    }


def _print_mesh_stats(label: str, stats: dict[str, Any]) -> None:
    """Pretty-print mesh statistics to stdout."""
    print(f"\n{'=' * 55}")
    print(f"  {label}")
    print(f"{'=' * 55}")
    print(f"  Nodes:            {stats['nodes']:>10,}")
    print(f"  Total elements:   {stats['total_elements']:>10,}")
    print(f"  {'─' * 45}")
    for etype, count in sorted(stats["elements"].items()):
        print(f"    {etype:<14s}  {count:>10,}")
    print(f"{'=' * 55}")


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    """Generate complete-sphere and hemisphere meshes and print statistics."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    params = ShellMeshParams()
    output_dir = Path("data/meshes")

    print("Mesh generation parameters")
    print(f"  Semi-major axis (a) : {params.semi_major_m} m")
    print(f"  Semi-minor axis (c) : {params.semi_minor_m} m")
    print(f"  Wall thickness  (h) : {params.wall_thickness_m} m")
    print(f"  Element size        : {params.element_size_m} m")
    print(f"  Element order       : {params.mesh_order}")

    # -- Complete sphere ----------------------------------------------------
    print("\n--- Generating complete sphere mesh ---")
    path1, stats1 = generate_complete_sphere(params, output_dir)
    _print_mesh_stats("Complete Sphere", stats1)
    print(f"  Saved → {path1}")

    # -- Hemisphere ---------------------------------------------------------
    print("\n--- Generating hemisphere mesh ---")
    path2, stats2 = generate_hemisphere(params, output_dir)
    _print_mesh_stats("Hemisphere (clamped rim)", stats2)
    print(f"  Saved → {path2}")

    # -- Summary ------------------------------------------------------------
    print("\nPhysical groups defined:")
    print("  Complete sphere : 'fluid' (vol), 'shell' (surf)")
    print("  Hemisphere      : 'fluid' (vol), 'shell' (surf),")
    print("                    'equatorial_plane' (surf), 'clamped_rim' (line)")
    print("\nDone.")


if __name__ == "__main__":
    main()
