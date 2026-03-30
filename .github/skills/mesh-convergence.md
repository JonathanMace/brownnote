---
description: >
  How to perform a mesh convergence study to verify that FEA results are
  mesh-independent. Includes Richardson extrapolation and GCI calculation.
---

# Skill: Mesh Convergence Study

Systematically verify that simulation results are independent of mesh resolution.

## Background

Mesh convergence is essential for credible FEA results. We refine the mesh
progressively and check that the quantity of interest (QoI) — typically the
lowest eigenfrequency — changes by less than a threshold (e.g., 1%).

## Steps

### 1. Select Mesh Sizes

Choose at least 4 mesh sizes with a consistent refinement ratio r ≈ 2:

```python
mesh_sizes = [0.020, 0.010, 0.005, 0.0025]  # element size in metres
```

### 2. Run the Study

Use the convergence script:

```bash
python scripts/run_convergence_study.py \
  --mesh-sizes 0.020 0.010 0.005 0.0025 \
  --geometry ellipsoid \
  --n-modes 10 \
  --output data/results/convergence/
```

Or programmatically:

```python
from browntone.mesh.abdominal_cavity import generate_cavity_mesh
from browntone.fem.modal_analysis import solve_modal
import json

results = []
for h in mesh_sizes:
    mesh_path = generate_cavity_mesh(element_size=h)
    eigenvalues = solve_modal(mesh_path, n_modes=10)
    results.append({
        "element_size": h,
        "n_elements": count_elements(mesh_path),
        "eigenfrequencies_hz": eigenvalues.tolist(),
    })

with open("data/results/convergence/convergence_data.json", "w") as f:
    json.dump(results, f, indent=2)
```

### 3. Calculate Convergence Metrics

#### Relative Change
```
ε_rel = |f_fine - f_coarse| / f_fine × 100%
```
Target: ε_rel < 1% between the two finest meshes.

#### Richardson Extrapolation
For three meshes with refinement ratio r:
```
f_exact ≈ f_1 + (f_1 - f_2) / (r^p - 1)
```
where p is the observed order of convergence:
```
p = ln((f_3 - f_2) / (f_2 - f_1)) / ln(r)
```

#### Grid Convergence Index (GCI)
```
GCI_fine = F_s × |ε| / (r^p - 1)
```
where F_s = 1.25 (safety factor for 3+ grids).

### 4. Generate Convergence Plot

```python
from browntone.postprocess.visualization import plot_convergence

plot_convergence(
    "data/results/convergence/convergence_data.json",
    qoi_index=0,  # first eigenfrequency
    save_to="papers/paper1-brown-note/figures/mesh_convergence.pdf",
)
```

The plot should show:
- x-axis: 1/h or number of DOFs (log scale)
- y-axis: eigenfrequency (Hz)
- Horizontal dashed line: Richardson-extrapolated value
- Error bars or shaded region: GCI uncertainty
- Annotation: observed convergence rate p

### 5. Interpret Results

| Observation | Interpretation |
|------------|---------------|
| Monotonic convergence | Expected; good |
| Oscillatory convergence | May indicate mixed-mode interaction; check mode tracking |
| p ≈ 2 (linear elements) | Correct asymptotic rate |
| p ≈ 4 (quadratic elements) | Correct asymptotic rate |
| p ≪ expected | Pre-asymptotic; need finer meshes |
| GCI < 2% | Mesh-independent to engineering accuracy |

### 6. Report in Paper

Include in the methodology section:
- Table of mesh sizes, element counts, DOFs, eigenfrequencies
- Convergence plot (described above)
- Statement: "A mesh with element size h = X mm (N elements, M DOFs) was
  selected, yielding a GCI of Y% for the fundamental frequency."
