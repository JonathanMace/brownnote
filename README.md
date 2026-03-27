# Browntone

**Computational investigation of infrasound-induced resonance in the human abdominal cavity.**

This project uses finite element analysis (FEA) and analytical methods to explore
whether infrasound at specific frequencies can excite resonant modes in the human
abdomen — the so-called "brown note" hypothesis.

## Quick Start

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests (no FEniCSx required)
pytest

# Run with Docker (includes FEniCSx)
docker compose -f docker/docker-compose.yml up -d
docker compose -f docker/docker-compose.yml exec browntone bash
```

## Project Structure

```
browntone/
├── src/browntone/        # Python package
│   ├── analytical/       # Closed-form shell/cavity solutions
│   ├── mesh/             # Gmsh geometry and meshing
│   ├── fem/              # FEniCSx solvers (modal, harmonic, FSI)
│   ├── postprocess/      # Visualization and data extraction
│   └── utils/            # Materials, constants, shared helpers
├── tests/                # pytest suite
├── data/                 # Material properties and simulation results
├── paper/                # LaTeX manuscript
├── notebooks/            # Exploratory Jupyter notebooks
├── scripts/              # Automation and batch-run scripts
├── docker/               # Containerized FEniCSx environment
└── docs/                 # Research notes and methodology
```

## Simulation Workflow

1. **Mesh** — Generate abdominal cavity geometry with `browntone.mesh`
2. **Solve** — Run modal / harmonic / FSI analysis with `browntone.fem`
3. **Post-process** — Extract eigenvalues, mode shapes, pressure fields with `browntone.postprocess`
4. **Visualize** — Publication-quality figures via matplotlib / PyVista

## Dependencies

| Package | Purpose |
|---------|---------|
| FEniCSx (DOLFINx) | Finite element solvers |
| gmsh | Mesh generation |
| numpy / scipy | Numerical computing |
| matplotlib / PyVista | Visualization |
| meshio | Mesh format conversion |

## License

MIT
