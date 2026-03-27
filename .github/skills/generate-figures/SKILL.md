---
name: generate-figures
description: >
  Generate or regenerate publication-quality figures for the browntone project.
  Use when figures need updating after code changes, or when new figure types
  are needed for the paper.
---

# Generate Figures Skill

Create publication-quality figures for JSV submission.

## Figure Standards (JSV)

- **Column widths**: 84 mm (single), 174 mm (double)
- **Resolution**: 300 DPI minimum
- **Font**: Serif (Times/Computer Modern), 8-10 pt
- **Line width**: 1.5-2 pt for data, 0.75 pt for gridlines
- **Colors**: Colorblind-safe; greyscale-safe with hatching/markers
- **Format**: PNG@300dpi for review, PDF vector for submission
- **Output**: `data/figures/`
- **Headless**: Always `import matplotlib; matplotlib.use('Agg')`

## Master Generation Script

```powershell
cd C:\Users\jon\OneDrive\Projects\browntone
python scripts/generate_all_figures.py
```

## Current Figure Set (12 figures)

| # | File | Content |
|---|------|---------|
| 1 | `fig_geometry_schematic` | Oblate spheroid with axes (a, c, h) |
| 2 | `fig_mode_shapes` | n=0,2,3,4 cross-sections |
| 3 | `fig_frequency_vs_E` | f₂,₃,₄ vs E + ISO band + canonical marker |
| 4 | `fig_uq_sobol_indices` | Sobol S₁/S_T bar chart |
| 5 | `fig_uq_frequency_distribution` | MC histogram+KDE with 90% CI |
| 6 | `fig_coupling_comparison` | Airborne vs mechanical displacement bars |
| 7 | `fig_energy_budget` | Waterfall energy cascade |
| 8 | `fig_dimensional_collapse` | Raw→Π₀ collapse→parity (486 pts) |
| 9 | `fig_scaling_law` | f₂ vs body size (rat→human) |
| 10 | `fig_transmissibility` | Model H(f) vs ISO 2631 data |
| 11 | `fig_nonlinear_backbone` | Duffing backbone + jump phenomenon |
| 12 | `fig_bc_comparison` | Free/SS/clamped BC frequency comparison |

## Checklist After Generating

- [ ] All text legible at 84mm column width
- [ ] Axis labels include units: "Frequency (Hz)"
- [ ] Legend doesn't overlap data
- [ ] Colour scheme consistent across all figures
- [ ] Greyscale print check: can distinguish all data series?
- [ ] Canonical parameters used (check f₂=3.95 Hz marker)
