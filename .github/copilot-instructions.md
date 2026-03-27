# Browntone — Copilot Project Instructions

## Project Overview

**Browntone** is a computational biomechanics research project investigating whether
infrasound (very low-frequency sound, typically < 20 Hz) can induce resonance in the
human abdominal cavity. The name is a playful portmanteau of "brown note/tone" and
the fundamental frequency being studied.

**Never refer to this as the "brown note" in publication text, code comments intended
for the paper, or any formal output.** Use "infrasound-induced abdominal resonance."

## Critical Physics Notes

When working on this codebase, understand these key physics:

1. **Long-wavelength regime**: At 5-10 Hz, λ_air ≈ 35-70m. The body (~0.5m) is
   1/70th to 1/140th of a wavelength. The pressure field is essentially uniform
   across the body — the body does NOT see a propagating wave.

2. **Acoustic coupling in the long-wavelength limit**: The full incident pressure
   acts on the shell exterior. The air-tissue impedance mismatch (Z ratio ~1:4000)
   determines radiation efficiency and energy absorption, but NOT the driving
   pressure. The shell responds to pressure, not energy flux.

3. **Quality factor Q**: The most sensitive and uncertain parameter. Soft tissue
   Q ≈ 2-10. Always present results as Q-dependent and be explicit about this
   uncertainty. Derive Q from published loss tangent: Q = 1/tan(δ).

4. **PIEZO comparison**: Patch-clamp thresholds (0.5-2 μm) represent localized
   membrane indentation, not bulk tissue oscillation. Wall bending strain, not
   displacement, is the correct comparison metric.

## Iterative Workflow

Every work phase must follow: DO WORK → CRITIQUE (reviewer-b agent) → LOG
(timestamped research-log) → REFINE PLAN → ITERATE.

The project combines:
- **Analytical models**: closed-form solutions for cylindrical/ellipsoidal shell vibration
  and acoustic cavity modes
- **Finite element analysis**: FEniCSx-based modal, harmonic-response, and
  fluid–structure interaction (FSI) simulations
- **Publication**: a journal paper targeting *Journal of Sound and Vibration* or
  *Proceedings of the Royal Society A*

## Repository Layout

```
src/browntone/
  analytical/    — closed-form eigenvalue problems (shell theory, cavity acoustics)
  mesh/          — gmsh-based geometry and mesh generation
  fem/           — FEniCSx solvers (modal, harmonic, coupled FSI)
  postprocess/   — data extraction, visualisation, figure generation
  utils/         — material property database, physical constants, helpers
tests/           — pytest test suite (unit + integration)
data/            — material property JSON files and simulation output
paper/           — LaTeX manuscript, BibTeX references, figures
notebooks/       — Jupyter exploration notebooks
scripts/         — batch-run and automation scripts
docker/          — Dockerfile and compose for reproducible FEniCSx env
```

## Code Conventions

### Python Style
- **Python ≥ 3.10** — use modern syntax (`match`, `X | Y` unions, etc.)
- **Formatting**: Ruff with 88-char line length (Black-compatible)
- **Type hints on every public function** — use `numpy.typing.NDArray` for arrays
- **Docstrings**: NumPy style on all public functions and classes
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes,
  `UPPER_SNAKE` for constants
- **Units**: SI throughout. Always document units in docstrings and variable names
  where ambiguous (e.g., `pressure_pa`, `frequency_hz`)
- **No magic numbers** — define named constants in `utils/constants.py`

### Imports
```python
# Standard library
from __future__ import annotations
import pathlib

# Third-party
import numpy as np
from scipy import linalg

# Local
from browntone.utils.materials import Material
```

### Error Handling
- Raise `ValueError` for bad physics inputs (e.g., negative Young's modulus)
- Use `logging` (not print) for status messages in solvers
- Wrap gmsh/FEniCSx calls in try/finally to ensure cleanup (gmsh.finalize())

## Physics Context

When helping with this project, keep these physics concepts in mind:

### Abdominal Cavity Model
- The abdomen is modelled as a **fluid-filled elastic cavity**
- Geometry: simplified ellipsoidal or cylindrical shell
- Typical dimensions: ~30 cm length, ~15 cm radius
- The abdominal wall is a **layered viscoelastic shell** (skin, fat, muscle, fascia)
- Internal organs provide additional distributed mass and stiffness

### Relevant Physics
- **Structural modal analysis**: natural frequencies and mode shapes of the abdominal wall
- **Acoustic cavity modes**: standing waves inside the fluid-filled cavity
- **Fluid–structure interaction (FSI)**: coupled vibration where cavity pressure loads
  the wall and wall motion drives acoustic waves
- **Infrasound range**: 1–20 Hz; frequencies below human hearing threshold
- **Resonance condition**: when driving frequency ≈ natural frequency → amplified response

### Key Equations
- **Donnell shell theory** for thin cylindrical shells
- **Helmholtz equation** for acoustic cavity modes: ∇²p + k²p = 0
- **Coupled eigenvalue problem**: [K_s - ω²M_s + C_fs; C_sf + K_f - ω²M_f]{u,p} = 0
- Material damping via **Rayleigh damping** (α M + β K) or complex modulus

### Material Properties
- Abdominal wall tissue: E ≈ 20–100 kPa, ν ≈ 0.45–0.49 (nearly incompressible),
  ρ ≈ 1000–1100 kg/m³
- Abdominal fluid (approx water): c ≈ 1500 m/s, ρ ≈ 1000 kg/m³
- These are soft-tissue ranges; parametric studies sweep over them

### Validation Approaches
- Compare analytical shell eigenfrequencies against FEA
- Check acoustic cavity modes against Bessel-function solutions
- Verify coupled FSI against published benchmarks (e.g., Junger & Feit)

## Simulation Workflow

The standard workflow is **mesh → solve → postprocess**:

### 1. Mesh Generation (`browntone.mesh`)
```bash
bt-mesh --geometry ellipsoid --length 0.30 --radius 0.15 --resolution 0.005 -o cavity.msh
```
- Uses gmsh Python API
- Parameterised geometry (dimensions, wall thickness, element size)
- Exports to `.msh` format; meshio converts to XDMF for FEniCSx

### 2. Solve (`browntone.fem`)
```bash
bt-modal --mesh cavity.msh --n-modes 20 --material soft-tissue -o results/
```
- Modal analysis: solve Kφ = ω²Mφ for eigenvalues/vectors
- Harmonic response: frequency sweep with prescribed pressure BC
- FSI: coupled acoustic–structural eigenvalue problem

### 3. Post-process (`browntone.postprocess`)
- Extract eigenfrequencies, mode shapes, participation factors
- Generate displacement / pressure contour plots (PyVista)
- Publication figures (matplotlib, LaTeX-ready)
- Export data to CSV/HDF5 for further analysis

## Paper Writing Conventions

### LaTeX Style
- Use `\SI{}{}` from `siunitx` for all quantities with units
- Equations: `align` environment, numbered only if referenced
- Figures: vector format (PDF/EPS) preferred; 300 DPI minimum for raster
- Citations: `natbib` with author-year style
- Cross-references: `\cref{}` from `cleveref`

### Writing Style
- British English spelling (behaviour, modelled, analysed)
- Present tense for established facts; past tense for what *we* did
- Passive voice acceptable in methods; active preferred elsewhere
- Define abbreviations on first use: "finite element analysis (FEA)"
- All symbols defined at point of first use in text

## Testing Approach

### Test Categories
1. **Unit tests** (`tests/test_analytical.py`): analytical solutions against known results
2. **Mesh tests** (`tests/test_mesh.py`): mesh generation produces valid meshes
3. **Material tests** (`tests/test_materials.py`): material database consistency
4. **Solver tests** (`tests/test_fem.py`, marked `@pytest.mark.fenics`): FEA solvers
   against analytical benchmarks
5. **Integration tests** (marked `@pytest.mark.slow`): full workflow end-to-end

### Running Tests
```bash
pytest                              # all tests (needs FEniCSx)
pytest -m "not fenics"              # skip FEniCSx tests
pytest -m "not slow and not fenics" # fast unit tests only
pytest --cov=browntone              # with coverage
```

## How to Run Simulations

### Local (with FEniCSx installed)
```bash
pip install -e ".[fenics]"
python scripts/run_modal_analysis.py --config data/materials/default.json
```

### Docker (recommended)
```bash
docker compose -f docker/docker-compose.yml run --rm browntone \
    python scripts/run_modal_analysis.py --config data/materials/default.json
```

### Parametric Study
```bash
python scripts/run_convergence_study.py \
    --mesh-sizes 0.02 0.01 0.005 0.0025 \
    --output data/results/convergence/
```
