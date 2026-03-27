---
name: generate-figures
description: >
  Generate or regenerate publication-quality figures for the browntone project.
  Use when figures need updating after code changes, or when new figure types
  are needed for the paper.
---

# Generate Figures Skill

Create publication-quality figures for the browntone research project.

## Figure Standards

- **Resolution**: 300 DPI
- **Font**: Serif (Times/Computer Modern), 10-12 pt
- **Line width**: 1.5-2 pt for data, 1 pt for gridlines
- **Colors**: Colorblind-safe palette; avoid red-green only distinction
- **Brown note band**: Always show 5-10 Hz range as shaded brown band (alpha=0.15)
- **Format**: PNG for review, PDF for paper submission
- **Output**: `data/figures/`

## Current Figure Set

1. `fig1_parametric_frequencies.png` — 3-panel: E, h, a vs breathing mode
2. `fig2_piezo_threshold_map.png` — Heatmap: SPL vs freq, displacement contours
3. `fig3_spl_by_body_type.png` — Lines: body types, Q vs min SPL
4. `fig4_modal_spectrum.png` — Grouped bar: mode number vs frequency by model

## Figures Still Needed

5. `fig5_impedance_corrected.png` — Corrected displacement with coupling model
6. `fig6_validation_iso2631.png` — Comparison with ISO 2631 resonance data
7. `fig7_mechanism_schematic.png` — Pathway diagram (acoustic → mechanical → neural)
8. `fig8_Q_sensitivity.png` — How Q affects everything (most sensitive parameter)

## Generation Command

```bash
cd C:\Users\jon\OneDrive\Projects\browntone
python src/postprocess/generate_figures.py
```

## Review Checklist

After generating, verify:
- [ ] All text legible at journal column width (~84mm single, ~174mm double)
- [ ] Axis labels include units in brackets: "Frequency [Hz]"
- [ ] Legend doesn't overlap data
- [ ] Color scheme consistent across figures
- [ ] Brown note band present where relevant
