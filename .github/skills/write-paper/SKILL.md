---
name: write-paper
description: >
  Guide for writing and formatting the journal paper. Use when drafting
  sections, managing references, or preparing for submission to the
  Journal of Sound and Vibration.
---

# Write Paper Skill

Guide for writing the JSV manuscript on infrasound-induced abdominal resonance.

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

## Writing Style

Blend two voices (Jonathan Mace dominant, Brian Mace for theory):
- **Active voice** by default: "We show..." not "It was shown..."
- **British English**: behaviour, modelled, analysed, colour
- **`\SI{value}{unit}`** for all quantities
- **Define all symbols** at first use
- Every equation gets a **"where..." clause**
- **No overclaiming**: "The results suggest..." not "We prove..."
- Figures referenced **before** discussion: "Figure~\ref{fig:X} shows..."
- Tables: `\toprule`, `\midrule`, `\bottomrule` (booktabs)
- Subtle dry humour welcome — keep it sophisticated

See `.github/skills/jmace-writing-style/SKILL.md` and
`.github/skills/mace-writing-style/SKILL.md` for detailed guides.

## Canonical Parameters (for any tables or computations in the paper)

E=0.1 MPa, a=0.18m, c=0.12m, h=0.01m, ν=0.45, ρ_w=1100, ρ_f=1020,
K_f=2.2 GPa, P_iap=1000 Pa, η=0.25 → Q=4.0, ζ=0.125, R_eq=0.157m, ka=0.0114

**Stale v1 values that must NOT appear**: η=0.30, ka=0.017, R_eq=0.133

## Key Physics to Get Right

- Breathing modes (n=0, ~2490 Hz) ≠ flexural modes (n≥2, 4-10 Hz)
- Energy-consistent displacement (0.014 μm at 120 dB), not pressure-based (0.18 μm)
- Coupling ratio R ≈ 66,000 (6.6×10⁴, mechanical/airborne)

## Compilation

```powershell
cd C:\Users\jon\OneDrive\Projects\browntone\paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
Copy-Item main.pdf "drafts\draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
```

## Citation Management

- BibTeX: `paper/references.bib`
- Use DOIs for all entries
- Cite primary sources for specific claims
- Every numerical value from literature needs a citation
