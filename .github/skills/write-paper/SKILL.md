---
name: write-paper
description: >
  Guide for writing and formatting the journal paper. Use when drafting sections, managing references, or preparing for submission to the Journal of Sound and Vibration.
license: MIT
---

# Write Paper Skill

Guide for writing the JSV manuscript on infrasound-induced abdominal resonance.

## Inspect First

- `papers/paper1-brown-note/main.tex`
- `papers/paper1-brown-note/references.bib`
- `.github/skills/jmace-writing-style/SKILL.md`
- `.github/skills/mace-writing-style/SKILL.md`
- the latest compiled draft and any recent reviewer notes

## Paper Title (current)

"Can Infrasound Induce Abdominal Resonance? Modal Analysis of a Fluid-Filled
Viscoelastic Oblate Spheroidal Shell Model of the Human Abdomen"

## Target Journal

**Journal of Sound and Vibration** (Elsevier)
- Format: `\documentclass[review]{elsarticle}` with `lineno`
- References: `elsarticle-num.bst`, numbered
- Required: Highlights (3-5, ≤85 chars), data availability, CRediT, competing interests
- Structure: Abstract, Introduction, Formulation, Results, Coupling Analysis,
  Discussion, Conclusions

## Format

- `\documentclass[review]{elsarticle}` with `lineno` package
- `elsarticle-num.bst` bibliography style
- British English throughout (behaviour, modelled, analysed, colour)
- `\SI{value}{unit}` for all quantities with units (siunitx package)
- Tables: `\toprule`, `\midrule`, `\bottomrule` (booktabs)
- Figures referenced before discussion: `Figure~\ref{fig:X} shows...`
- Every equation gets a `where...` clause defining all new symbols

## Writing Style

Blend two voices (Jonathan Mace dominant, Brian Mace for theory):
- **Active voice** by default: `We show...` not `It was shown...`
- **British English**: behaviour, modelled, analysed, colour
- **`\SI{value}{unit}`** for all quantities
- **Define all symbols** at first use
- Every equation gets a **`where...` clause**
- **No overclaiming**: `The results suggest...` not `We prove...`
- Figures referenced **before** discussion: `Figure~\ref{fig:X} shows...`
- Tables: `\toprule`, `\midrule`, `\bottomrule` (booktabs)
- Subtle dry humour welcome — keep it sophisticated

See `.github/skills/jmace-writing-style/SKILL.md` and
`.github/skills/mace-writing-style/SKILL.md` for detailed guides.

## Canonical Parameters

**Every table and computation in the paper must use these values.**
If a parameter differs from this list, it is wrong unless explicitly marked as a parametric variation.

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Semi-major axis | a | 0.18 | m |
| Semi-minor axis | c | 0.12 | m |
| Wall thickness | h | 0.010 | m |
| Elastic modulus | E | 0.1 | MPa |
| Poisson's ratio | ν | 0.45 | — |
| Wall density | ρ_w | 1100 | kg/m³ |
| Fluid density | ρ_f | 1020 | kg/m³ |
| Fluid bulk modulus | K_f | 2.2 | GPa |
| IAP | P_iap | 1000 | Pa |
| Loss tangent | η | 0.25 | — |

Derived: `R_eq=0.157 m`, `f₂=3.95 Hz`, `Q=4.0`, `ζ=0.125`, `ka=0.0114`

**Stale v1 values that must NOT appear**: `η=0.30`, `ka=0.017`, `R_eq=0.133`

## Key Physics to Get Right

- Breathing modes (`n=0`, ~2490 Hz) are not flexural modes (`n≥2`, 4-10 Hz)
- Always use the energy-consistent displacement (`0.014 μm` at 120 dB) for airborne claims
- Pressure-based displacement (`0.18 μm`) is a `13×` overestimate and must be labelled if mentioned
- Coupling ratio `R ≈ 66,000` (`6.6×10⁴`, mechanical/airborne)
- Do not use stale defaults `η=0.30`, `ka=0.017`, or `R_eq=0.133`

## Citation Management

- BibTeX source: `papers/paper1-brown-note/references.bib`
- Use DOIs for all entries where available
- Cite primary sources for specific claims
- Every numerical value from the literature needs a citation

## Compilation

```powershell
cd C:\Users\jon\Projects\browntone\papers\paper1-brown-note
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
Copy-Item main.pdf "drafts\draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
```

## Done Criteria

- the edited section follows JSV structure and Browntone style conventions
- all quantities use canonical parameters unless explicitly marked otherwise
- figures, equations, and citations are introduced and formatted correctly
- the paper compiles cleanly, or any remaining errors are reported precisely
- a timestamped PDF snapshot is preserved after successful compilation
