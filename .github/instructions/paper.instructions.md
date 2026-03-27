---
applyTo: "paper/**"
---

# Paper Writing Instructions

You are editing the JSV manuscript. Follow these rules strictly.

## Format
- `\documentclass[review]{elsarticle}` with `lineno` package
- `elsarticle-num.bst` bibliography style
- British English throughout (behaviour, modelled, analysed, colour)
- `\SI{value}{unit}` for all quantities with units (siunitx package)
- Tables: `\toprule`, `\midrule`, `\bottomrule` (booktabs)
- Figures referenced BEFORE discussion: "Figure~\ref{fig:X} shows..."
- Every equation gets a "where..." clause defining all new symbols

## Canonical Parameters

**Every table and computation in the paper must use these values.**
If a parameter differs from this list, it is WRONG unless explicitly marked as a parametric variation.

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| a | Semi-major axis | 0.18 | m |
| c | Semi-minor axis | 0.12 | m |
| h | Wall thickness | 0.010 | m |
| E | Elastic modulus | 0.1 | MPa |
| ν | Poisson's ratio | 0.45 | — |
| ρ_w | Wall density | 1100 | kg/m³ |
| ρ_f | Fluid density | 1020 | kg/m³ |
| K_f | Fluid bulk modulus | 2.2 | GPa |
| P_iap | IAP | 1000 | Pa |
| η | Loss tangent | 0.25 | — |

Derived: R_eq=0.157 m, f₂=3.95 Hz, Q=4.0, ζ=0.125, ka=0.0114

## Writing Style

Blend two voices:
1. **Jonathan Mace** (first author, dominant voice): Active voice, direct, confident,
   "we show" not "it was shown". Concrete physical intuition. See `.github/skills/jmace-writing-style/SKILL.md`.
2. **Brian Mace** (JSV conventions): Structural precision for theory sections, hedging
   for acoustic claims, "where..." equation clauses. See `.github/skills/mace-writing-style/SKILL.md`.

Rules:
- Active voice by default. Passive only for methods where agent doesn't matter.
- No overclaiming. "The results suggest..." not "We prove..."
- Define all symbols at first use
- Subtle dry humour is welcome (the topic invites it), but keep it sophisticated

## Key Physics Errors to Avoid

- **Never** confuse breathing modes (n=0, ~2490 Hz) with flexural modes (n≥2, 4-10 Hz)
- **Never** use pressure-based displacement (0.18 μm) without noting it's a 13× overestimate
- **Always** use energy-consistent displacement (0.014 μm at 120 dB) for airborne claims
- **Never** use η=0.30 (that's stale v1). η=0.25 is canonical.
- **Never** use ka=0.017 or R_eq=0.133 (stale defaults). ka=0.0114, R_eq=0.157.

## Compilation

```powershell
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

After compiling, snapshot: `Copy-Item main.pdf "drafts\draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"`
