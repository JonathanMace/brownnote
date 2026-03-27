---
description: >
  How to create publication-quality figures for the browntone paper.
  Covers matplotlib setup, style, export settings, and common figure types.
---

# Skill: Generate Publication Figures

Create figures suitable for submission to JSV or Proc. Roy. Soc. A.

## Setup

### matplotlib Style

The project uses a custom style. Load it at the top of every figure script:

```python
from browntone.postprocess.visualization import set_publication_style
set_publication_style()
```

Or manually:
```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "font.family": "serif",
    "font.size": 9,
    "mathtext.fontset": "cm",
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "lines.linewidth": 1.2,
    "lines.markersize": 4,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "text.usetex": True,
})
```

### Figure Dimensions

| Layout | Width (mm) | Width (inches) |
|--------|-----------|----------------|
| Single column | 85 | 3.35 |
| 1.5 column | 120 | 4.72 |
| Double column | 170 | 6.69 |

```python
fig, ax = plt.subplots(figsize=(3.35, 2.5))  # single-column
```

### Colour Palette

Use a consistent 5-colour palette across all figures:

```python
COLOURS = {
    "primary": "#2166AC",    # blue
    "secondary": "#B2182B",  # red
    "tertiary": "#4DAF4A",   # green
    "quaternary": "#FF7F00",  # orange
    "quinary": "#984EA3",    # purple
}
```

For continuous data, use `cividis` (perceptually uniform and colour-blind safe).

## Common Figure Types

### 1. Eigenfrequency Bar Chart

```python
from browntone.postprocess.visualization import plot_eigenfrequencies

plot_eigenfrequencies(
    results,
    n_modes=10,
    compare_analytical=analytical_freqs,
    save_to="paper/figures/eigenfrequencies.pdf",
)
```

### 2. Mode Shape Contour Plot (3D)

```python
from browntone.postprocess.visualization import plot_mode_shape

plot_mode_shape(
    results,
    mode=0,
    field="displacement_magnitude",
    colormap="cividis",
    save_to="paper/figures/mode_0.pdf",
)
```

### 3. Convergence Plot

```python
from browntone.postprocess.visualization import plot_convergence

plot_convergence(
    convergence_data,
    qoi_label=r"$f_1$ (Hz)",
    save_to="paper/figures/convergence.pdf",
)
```

### 4. Parametric Study (Response Surface)

```python
from browntone.postprocess.visualization import plot_parametric_heatmap

plot_parametric_heatmap(
    param_x=youngs_moduli,
    param_y=wall_thicknesses,
    values=eigenfrequencies,
    xlabel=r"Young's modulus $E$ (kPa)",
    ylabel=r"Wall thickness $h$ (mm)",
    zlabel=r"$f_1$ (Hz)",
    save_to="paper/figures/parametric_Eh.pdf",
)
```

### 5. Frequency Response Function

```python
fig, ax = plt.subplots(figsize=(3.35, 2.5))
ax.semilogy(frequencies_hz, amplitude_m, color=COLOURS["primary"])
ax.set_xlabel(r"Frequency (Hz)")
ax.set_ylabel(r"Displacement amplitude (m)")
ax.axvline(x=f_resonance, ls="--", color=COLOURS["secondary"], label="Resonance")
ax.legend()
fig.savefig("paper/figures/frf.pdf")
```

## Export Checklist

- [ ] File format: PDF for line art, PNG (300 DPI) for 3D renders
- [ ] Axes labelled with units
- [ ] Legend present if multiple series
- [ ] Font size readable at printed column width
- [ ] Colours distinguishable in grayscale
- [ ] Figure referenced in LaTeX with `\cref{fig:name}`
- [ ] Caption written in `paper/main.tex` or section file
- [ ] File saved to `paper/figures/`
