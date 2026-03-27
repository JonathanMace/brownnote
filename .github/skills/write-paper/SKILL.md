---
name: write-paper
description: >
  Guide for writing and formatting the journal paper. Use when drafting
  sections, managing references, or preparing for submission to the
  Journal of Sound and Vibration.
---

# Write Paper Skill

Guide for writing the journal paper on infrasound-induced abdominal resonance.

## CRITICAL RULE

**Never use the term "brown note" in the paper.** Use these instead:

| Colloquial | Academic |
|------------|----------|
| Brown note | Infrasound-induced abdominal resonance |
| Brown tone | Low-frequency acoustic excitation of the peritoneal cavity |
| Bowel effects | Mechanotransduction-mediated gastrointestinal response |
| Gut shaking | Visceral mechanical stimulation |

## Paper Title (working)

"Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell:
Implications for Low-Frequency Acoustic Exposure and Abdominal Resonance"

## Target Journal

**Journal of Sound and Vibration** (Elsevier)
- Format: Elsevier article class (`elsarticle`)
- Reference style: numbered, Elsevier Harvard
- Max length: ~8000 words + figures
- Required sections: Abstract, Introduction, Methods, Results, Discussion, Conclusions

## Section Outline

1. **Abstract** (200 words max)
2. **Introduction** — Motivate via occupational health / ISO standards gap
3. **Mathematical Formulation** — Shell theory, fluid coupling, Rayleigh-Ritz
4. **Material Properties** — Table of all parameters with literature sources
5. **Analytical Results** — Modal frequencies, parametric sensitivity
6. **Finite Element Validation** — Mesh convergence, comparison with analytical
7. **Acoustic-Structure Interaction** — Impedance, coupling, realistic excitation
8. **Mechanotransduction Analysis** — PIEZO thresholds, displacement comparison
9. **Discussion** — Limitations, implications, comparison with ISO 2631
10. **Conclusions** — Measured claims only

## LaTeX Setup

```bash
cd C:\Users\jon\OneDrive\Projects\browntone\paper
# Compile with:
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## Citation Management

- BibTeX file: `paper/references.bib`
- Use DOIs for all entries
- Cite primary sources, not review articles, for specific claims
- Every numerical value must have a citation

## Writing Process

1. Draft equations and figures first
2. Write Methods around the equations
3. Write Results around the figures
4. Write Discussion connecting to literature
5. Write Introduction last (to frame what you actually did)
6. Write Abstract last of all
