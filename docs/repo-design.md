# Browntone Repository Design Document

**Project**: Computational investigation of infrasound-induced resonance in the human abdominal cavity  
**Repository**: `browntone`  
**Date**: 2024  

---

## 1. Directory Structure

```
browntone/
├── .github/
│   ├── copilot-instructions.md       # Project-wide Copilot context
│   ├── agents/                        # Custom Copilot agents
│   │   ├── simulation-engineer.md     # FEA / mesh / physics expert
│   │   ├── paper-writer.md            # Academic writing / LaTeX expert
│   │   ├── data-analyst.md            # Post-processing / figures expert
│   │   └── literature-researcher.md   # Citation / literature expert
│   ├── skills/                        # Reusable Copilot skill guides
│   │   ├── run-simulation.md          # End-to-end simulation pipeline
│   │   ├── mesh-convergence.md        # Mesh convergence study procedure
│   │   ├── generate-figures.md        # Publication-quality figure guide
│   │   └── submit-paper.md            # Paper submission checklist
│   └── workflows/                     # GitHub Actions CI/CD
│       ├── ci.yml                     # Lint + test on push/PR
│       └── paper.yml                  # LaTeX compilation
│
├── src/browntone/                     # Installable Python package
│   ├── __init__.py                    # Package metadata
│   ├── cli.py                         # Click-based CLI entry point
│   ├── analytical/                    # Closed-form solutions
│   │   ├── __init__.py
│   │   ├── shell_vibration.py         # Donnell/Lamb shell eigenfrequencies
│   │   └── acoustic_modes.py          # Helmholtz cavity modes (Bessel)
│   ├── mesh/                          # Mesh generation
│   │   ├── __init__.py
│   │   └── abdominal_cavity.py        # Parameterised gmsh geometry
│   ├── fem/                           # FEniCSx solvers
│   │   ├── __init__.py
│   │   ├── modal_analysis.py          # Structural modal (Kφ = ω²Mφ)
│   │   └── acoustic_fsi.py            # Coupled FSI solver (placeholder)
│   ├── postprocess/                   # Results processing
│   │   ├── __init__.py
│   │   ├── visualization.py           # matplotlib + PyVista figures
│   │   └── extraction.py              # Data loading, Richardson extrap.
│   └── utils/                         # Shared utilities
│       ├── __init__.py
│       ├── constants.py               # Physical constants, SI units
│       └── materials.py               # Material property database
│
├── tests/                             # pytest test suite
│   ├── __init__.py
│   ├── conftest.py                    # Shared fixtures
│   ├── test_analytical.py             # Shell & cavity mode tests
│   ├── test_mesh.py                   # Mesh validation tests
│   ├── test_materials.py              # Material database tests
│   └── test_extraction.py             # Post-processing tests
│
├── data/
│   ├── materials/                     # Material property JSON files
│   │   ├── default.json               # Baseline properties
│   │   └── README.md                  # Property documentation
│   ├── results/                       # Simulation output (git-ignored, LFS)
│   └── literature/                    # Downloaded papers / data
│
├── paper/                             # LaTeX manuscript
│   ├── main.tex                       # Root document
│   ├── references.bib                 # BibTeX database
│   ├── figures/                       # Publication figures
│   └── sections/                      # Individual section files
│       ├── introduction.tex
│       ├── background.tex
│       ├── methods.tex
│       ├── results.tex
│       ├── discussion.tex
│       └── conclusion.tex
│
├── notebooks/                         # Jupyter exploration notebooks
│   ├── README.md
│   └── 01_analytical_solutions.ipynb
│
├── scripts/                           # Automation scripts
│   ├── run_modal_analysis.py          # Full pipeline script
│   └── run_convergence_study.py       # Mesh convergence script
│
├── docker/                            # Containerisation
│   ├── Dockerfile                     # FEniCSx environment
│   └── docker-compose.yml             # Dev + Jupyter services
│
├── docs/                              # Research documentation
│   ├── repo-design.md                 # This document
│   ├── methodology.md                 # Research methodology
│   └── literature-review.md           # Annotated bibliography
│
├── .gitignore                         # Python, LaTeX, sim outputs
├── .gitattributes                     # LFS tracking, line endings
├── pyproject.toml                     # Python project config
├── Makefile                           # Common task shortcuts
├── README.md                          # Project overview
└── LICENSE                            # MIT
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `.github/` | Copilot instructions, agents, skills, and CI/CD workflows |
| `src/browntone/` | Installable Python package — all production code |
| `src/browntone/analytical/` | Closed-form solutions for shell/cavity eigenfrequencies; used as FEA validation benchmarks |
| `src/browntone/mesh/` | Gmsh-based parametric mesh generation for abdominal cavity geometries |
| `src/browntone/fem/` | FEniCSx finite element solvers: modal, harmonic, and coupled FSI |
| `src/browntone/postprocess/` | Visualization (matplotlib, PyVista) and data extraction from simulation results |
| `src/browntone/utils/` | Material property database, physical constants, unit conversions |
| `tests/` | pytest test suite with markers for slow and FEniCSx-dependent tests |
| `data/materials/` | JSON files defining material properties with documented sources |
| `data/results/` | Simulation output (mesh files, eigenvalues, mode shapes) — tracked via LFS |
| `data/literature/` | Downloaded papers and reference data |
| `paper/` | LaTeX manuscript targeting JSV or Proc. Roy. Soc. A |
| `notebooks/` | Jupyter notebooks for interactive exploration (not production code) |
| `scripts/` | CLI scripts orchestrating the mesh → solve → postprocess pipeline |
| `docker/` | Dockerfile based on `dolfinx/dolfinx` for reproducible FEniCSx environments |
| `docs/` | Research documentation: methodology, literature review, this design document |

---

## 2. Copilot Instructions

**File**: `.github/copilot-instructions.md`

The project-wide instructions cover:

- **Project context**: what the "brown note" hypothesis is, why we're studying it computationally
- **Repository layout**: where each type of code lives
- **Code conventions**: Python 3.10+, Ruff formatting, NumPy-style docstrings, type hints, SI units
- **Physics context**: abdominal cavity as fluid-filled elastic shell, relevant equations (Donnell shell theory, Helmholtz, coupled FSI), material property ranges, validation approaches
- **Simulation workflow**: mesh → solve → postprocess pipeline with CLI examples
- **Paper writing conventions**: British English, LaTeX packages (siunitx, cleveref, natbib), figure standards
- **Testing approach**: unit tests for analytics, mesh validation, solver benchmarks against analytical solutions

---

## 3. Custom Agents

### simulation-engineer.md
Expert in FEniCSx, gmsh, structural dynamics, acoustics, and FSI. Knows how to:
- Set up and debug FEniCSx solvers (function spaces, weak forms, SLEPc)
- Generate parametric meshes with gmsh
- Handle nearly-incompressible materials (volumetric locking, mixed methods)
- Validate against analytical solutions
- Run parallel simulations with MPI

### paper-writer.md
Expert in academic writing for JSV and Proc. Roy. Soc. A. Knows:
- LaTeX document preparation (elsarticle, natbib, siunitx, cleveref)
- Scientific writing style (British English, hedging, logical flow)
- Journal-specific formatting requirements
- BibTeX management and citation conventions

### data-analyst.md
Expert in post-processing simulation results. Knows:
- matplotlib publication figure standards (sizes, fonts, colour palette)
- PyVista 3D visualization of FEA results
- Convergence analysis (Richardson extrapolation, GCI)
- Parametric study visualization (heatmaps, response surfaces)

### literature-researcher.md
Expert in acoustics, biomechanics, and vibro-acoustics literature. Helps:
- Find and summarize relevant papers
- Maintain the BibTeX database with complete entries
- Track key researchers and landmark references
- Organize the annotated literature review by topic

---

## 4. Custom Skills

### run-simulation.md
Step-by-step guide for the full simulation pipeline:
1. Define parameters (JSON config)
2. Generate mesh (`bt-mesh`)
3. Run solver (`bt-modal`)
4. Post-process results (extract eigenvalues, generate figures)
5. Validate against analytical solutions

### mesh-convergence.md
How to perform a rigorous mesh convergence study:
- Select mesh sizes with consistent refinement ratio
- Run the convergence script
- Compute Richardson extrapolation and GCI
- Generate convergence plots
- Report results in the paper

### generate-figures.md
How to create publication-quality figures:
- matplotlib style configuration for journal submission
- Figure dimensions (single/double column)
- Colour palette and accessibility
- Common figure types (bar charts, convergence, heatmaps, 3D mode shapes)
- Export checklist

### submit-paper.md
Paper submission checklist covering:
- Manuscript content (abstract, sections, equations, symbols)
- Figure and table standards
- Reference completeness
- LaTeX compilation verification
- Journal-specific requirements (JSV highlights, Proc. Roy. Soc. A ethics statement)

---

## 5. Python Project Setup

**File**: `pyproject.toml`

- **Build system**: setuptools with `src/` layout
- **Package**: `browntone` installable as `pip install -e .`
- **Dependencies**: numpy, scipy, matplotlib, gmsh, meshio, pyvista, rich, click, h5py, pandas
- **Optional dependencies**:
  - `fenics`: dolfinx, ufl, basix, petsc4py, mpi4py, slepc4py
  - `dev`: pytest, ruff, mypy, pre-commit
  - `notebooks`: jupyterlab, ipywidgets, trame
  - `docs`: sphinx, myst-parser
- **Entry points**: `browntone` (CLI), `bt-modal` (modal solver), `bt-mesh` (mesh generator)
- **Testing**: pytest with markers (`slow`, `fenics`, `gpu`)
- **Linting**: Ruff (Black-compatible, NumPy docstring convention)
- **Type checking**: mypy with relaxed imports for gmsh and dolfinx

---

## 6. Docker Setup

### Dockerfile
Based on `dolfinx/dolfinx:v0.8.0` (official FEniCSx image):
- Adds system packages for headless OpenGL (mesh visualization)
- Installs browntone with all Python dependencies
- Mounts the project directory as `/work`

### docker-compose.yml
Two services:
- **browntone**: Interactive development container with bash
- **jupyter**: JupyterLab server on port 8888 for notebook work

---

## 7. Git Configuration

### .gitignore
- Python artifacts (`__pycache__`, `.egg-info`, `dist/`)
- LaTeX build artifacts (`*.aux`, `*.bbl`, `*.log`, etc.)
- Simulation outputs (`*.xdmf`, `*.h5`, `*.vtu`, `*.msh`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

### .gitattributes
- **LFS tracking**: `.h5`, `.xdmf`, `.vtu`, `.vtk`, `.msh`, `.stl`
- **Line endings**: LF for all text source files
- **Binary marking**: `.png`, `.jpg`, `.pdf`, `.eps`
- **Notebook diff**: `.ipynb` treated as text for meaningful diffs

---

## 8. CI/CD

### ci.yml
Triggered on push/PR to `main`:
1. **Lint & Type Check**: Ruff + mypy on Python 3.12
2. **Core Tests**: pytest (excluding FEniCSx tests) on Python 3.10, 3.11, 3.12
3. **FEniCSx Tests**: pytest with `@pytest.mark.fenics` inside the `dolfinx/dolfinx:v0.8.0` container

### paper.yml
Triggered on changes to `paper/`:
1. Compiles `paper/main.tex` using `xu-cheng/latex-action`
2. Uploads the PDF as a build artifact (30-day retention)

---

## Design Rationale

### Why `src/` Layout?
The `src/browntone/` layout prevents accidental imports of the uninstalled package
during development and is the recommended setuptools convention. It ensures `import browntone`
always uses the installed version.

### Why Separate Analytical and FEM Modules?
- Analytical solutions serve as **validation benchmarks** for FEA
- They can run without FEniCSx (much easier to install)
- They provide quick estimates before running expensive simulations
- Tests for analytical code are fast and have no external dependencies

### Why Optional FEniCSx?
FEniCSx is complex to install (depends on PETSc, SLEPc, MPI). By making it optional:
- Core package (analytics, mesh, postprocessing) installs trivially with `pip install .`
- FEniCSx users install with `pip install .[fenics]`
- Docker provides a guaranteed working FEniCSx environment
- CI tests FEniCSx separately in the official container

### Why Click for CLI?
Click provides a clean, composable CLI framework with automatic help generation,
type validation, and shell completion — ideal for parameterized scientific workflows.

### Why JSON for Material Properties?
- Human-readable and editable
- Easily version-controlled
- Can be loaded programmatically or referenced from scripts
- Serves as documentation of property sources
