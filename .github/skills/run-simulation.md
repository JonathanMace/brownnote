---
description: >
  Step-by-step guide for running a simulation from mesh generation through
  solving to post-processing. Covers the full mesh → solve → postprocess pipeline.
---

# Skill: Run Simulation

Run a complete browntone simulation from geometry to results.

## Prerequisites

- Python environment with browntone installed: `pip install -e ".[fenics]"`
- OR Docker environment running: `docker compose -f docker/docker-compose.yml up -d`
- Material property file in `data/materials/`

## Steps

### 1. Define Simulation Parameters

Create or select a parameter file (JSON):

```json
{
  "geometry": {
    "type": "ellipsoid",
    "semi_major_m": 0.15,
    "semi_minor_m": 0.10,
    "wall_thickness_m": 0.015
  },
  "material": {
    "wall": {
      "youngs_modulus_pa": 50000,
      "poisson_ratio": 0.47,
      "density_kg_m3": 1050
    },
    "fluid": {
      "sound_speed_m_s": 1500,
      "density_kg_m3": 1000
    }
  },
  "solver": {
    "analysis_type": "modal",
    "n_modes": 20,
    "element_order": 2
  },
  "mesh": {
    "element_size_m": 0.005
  },
  "output_dir": "data/results/modal_001"
}
```

### 2. Generate Mesh

```bash
bt-mesh \
  --geometry ellipsoid \
  --semi-major 0.15 \
  --semi-minor 0.10 \
  --thickness 0.015 \
  --element-size 0.005 \
  --output data/results/modal_001/mesh.msh
```

Verify the mesh:
```python
from browntone.mesh.abdominal_cavity import load_and_inspect
load_and_inspect("data/results/modal_001/mesh.msh")
```

Expected output: element count, quality metrics, bounding box.

### 3. Run the Solver

```bash
# Serial
bt-modal \
  --mesh data/results/modal_001/mesh.msh \
  --n-modes 20 \
  --material soft-tissue \
  --output data/results/modal_001/

# Parallel (for large meshes)
mpirun -n 4 python -m browntone.fem.modal_analysis \
  --mesh data/results/modal_001/mesh.msh \
  --n-modes 20 \
  --output data/results/modal_001/
```

### 4. Post-process Results

```python
from browntone.postprocess.extraction import load_modal_results
from browntone.postprocess.visualization import plot_eigenfrequencies, plot_mode_shape

results = load_modal_results("data/results/modal_001/")

# Print eigenfrequency table
results.print_summary()

# Eigenfrequency bar chart
plot_eigenfrequencies(results, save_to="paper/figures/eigenfrequencies.pdf")

# Mode shape visualization
for i in range(6):
    plot_mode_shape(results, mode=i, save_to=f"paper/figures/mode_{i}.pdf")
```

### 5. Validate

- Compare first few eigenfrequencies against analytical solution:
  ```python
  from browntone.analytical.shell_vibration import cylindrical_shell_frequencies
  analytical = cylindrical_shell_frequencies(R=0.15, L=0.30, h=0.015, material="soft-tissue")
  ```
- Check that eigenfrequencies converge with mesh refinement
- Verify mode shapes are physically reasonable (symmetric modes, etc.)

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| SLEPc converges to 0 eigenvalues | Rigid body modes not constrained | Add symmetry BCs or shift-invert |
| Mesh generation fails | Geometry self-intersection | Reduce wall thickness or refine |
| Memory error | Mesh too fine | Use coarser mesh or increase MPI ranks |
| Spurious pressure modes | Inf-sup instability | Use Taylor-Hood or MINI elements |
