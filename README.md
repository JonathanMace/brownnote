# Browntone 🎵💩

**Modal analysis of a fluid-filled viscoelastic oblate spheroidal shell — or, why the brown note doesn't work (but whole-body vibration does).**

## The Punchline

The n=2 flexural mode of the abdomen sits at ~4 Hz, right in the infrasound
range — but airborne sound can barely reach it. At 120 dB SPL the
energy-consistent wall displacement is 0.014 μm, roughly 10,000× below the
mechanotransduction threshold. Whole-body vibration at a modest 0.5 m/s²
delivers 3,243 μm — a coupling ratio of ~46,000×. The brown note is a
mechanical effect misattributed to acoustics.

## Key Results

| Quantity | Value |
|----------|-------|
| n=2 flexural frequency (f₂) | 3.95 Hz |
| Breathing mode (n=0) | 2,490 Hz |
| Airborne displacement (ξ_air, 120 dB) | 0.014 μm |
| Mechanical displacement (ξ_mech, 0.5 m/s²) | 3,243 μm |
| Coupling ratio R | ≈ 46,000× |
| Sobol total-order index S_T(E) | 0.86 |

## Project Structure

```
browntone/
├── src/
│   ├── analytical/            # Core analytical models (17 modules)
│   │   ├── natural_frequency_v2.py    # Modal analysis (AbdominalModelV2)
│   │   ├── natural_frequency.py       # Legacy v1 modal model
│   │   ├── acoustic_coupling.py       # Airborne pressure → shell coupling
│   │   ├── mechanical_coupling.py     # WBV vs airborne comparison
│   │   ├── energy_budget.py           # Reciprocity-based self-consistent analysis
│   │   ├── dimensional_analysis.py    # Buckingham-π groupings
│   │   ├── gas_pocket_resonance.py    # Bowel gas as acoustic transducers
│   │   ├── gas_pocket_detailed.py     # Constrained bubble model
│   │   ├── parametric_analysis.py     # Sensitivity study (486 combinations)
│   │   ├── multilayer_wall.py         # 5-layer composite wall model
│   │   ├── oblate_spheroid_ritz.py    # Rayleigh-Ritz oblate correction
│   │   ├── uncertainty_quantification.py  # Monte Carlo UQ + Sobol indices
│   │   ├── nonlinear_analysis.py      # Duffing oscillator, backbone curves
│   │   ├── viscous_correction.py      # Stokes boundary layer damping
│   │   ├── organ_inclusions.py        # Effective medium theory
│   │   ├── mechanotransduction.py     # Cellular response thresholds
│   │   └── orifice_coupling.py        # Orifice impedance model
│   ├── fem/                   # FEA mesh and modal solvers
│   │   ├── mesh_generation.py         # Gmsh geometry & meshing
│   │   └── modal_analysis.py          # Lamb-mode Rayleigh-Ritz solver
│   └── experimental/          # Phantom experiment design
│       └── phantom_design.py          # Silicone phantom specification
├── paper/                     # LaTeX manuscript (elsarticle, JSV format)
│   ├── main.tex
│   ├── sections/              # introduction, methods, results, discussion, …
│   ├── references.bib
│   └── drafts/                # Timestamped PDF snapshots
├── data/
│   ├── figures/               # Publication figures (PNG@300dpi + PDF)
│   ├── results/               # JSON result files
│   ├── meshes/                # Gmsh .msh files
│   ├── materials/             # Material property data
│   └── literature/            # Reference PDFs & notes
├── docs/                      # Research logs, methodology, style references
├── tests/                     # pytest suite
├── scripts/                   # Automation & batch-run scripts
├── notebooks/                 # Exploratory Jupyter notebooks
├── .github/
│   ├── agents/                # Copilot agents (reviewers, paper-writer, …)
│   └── skills/                # Copilot skills (compile-paper, run-analysis, …)
└── docker/                    # Containerised FEniCSx environment
```

## Quick Start

**Requirements:** Python 3.10+

```bash
pip install numpy scipy matplotlib SALib gmsh meshio
```

### Run the model

```python
import sys
sys.path.insert(0, r"path/to/browntone")

from src.analytical.natural_frequency_v2 import AbdominalModelV2, flexural_mode_frequencies_v2

model = AbdominalModelV2(
    E=0.1e6, a=0.18, b=0.18, c=0.12, h=0.01,
    nu=0.45, rho_wall=1100, rho_fluid=1020,
    K_fluid=2.2e9, P_iap=1000, loss_tangent=0.25,
)
freqs = flexural_mode_frequencies_v2(model, n_max=5)
print(freqs)  # {0: 2490.6, 1: 0.0, 2: 3.95, 3: 6.31, 4: 8.88, 5: 11.71}
```

### Run tests

```bash
pytest tests/
```

### Compile the paper

```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

## Git Workflow

- **`main` is protected** — all changes via pull requests.
- Feature branches live in worktrees at `browntone-worktrees/<branch>`.
- Merged remote branches are deleted to keep the branch list clean.

## Authors

| Who | Affiliation | Role |
|-----|-------------|------|
| **Jonathan Mace** | MSR | Corresponding author |
| **Brian R. Mace** | University of Auckland | Supervision & vibroacoustics expertise |
| **Springbank 10 Year Old** | Springbank Distillery | Morale & inspiration |
| **Opus / GitHub Copilot CLI** | GitHub, Inc. | Computation, drafting, & existential dread |

## Licence

[MIT](LICENSE)
