# JSV Submission Readiness Checklist — 2026-03-27

**Author**: Lab Manager (Copilot CLI)
**Branch**: main
**PR**: (pending)

## Summary

Pre-submission audit of the manuscript against the Journal of Sound and
Vibration author guidelines.  The paper is substantially ready; three items
require attention before upload.

## Checklist

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | **Format** `\documentclass[review]{elsarticle}` + `lineno` | ✅ PASS | Line 1: `\documentclass[review]{elsarticle}`, Line 14: `\usepackage{lineno}` |
| 2 | **Highlights** 3–5 bullets, each ≤85 chars | ⚠️ FAIL | 5 bullets (count OK). Bullet 1 = 93 chars (+8 over), Bullet 2 = 96 chars (+11 over). Bullets 3–5 OK. |
| 3 | **Abstract** present and ≤200 words | ⚠️ FAIL | Present. ~246 words — exceeds JSV 200-word limit by ~46 words. |
| 4 | **Keywords** 4–6 after abstract | ✅ PASS | 6 keywords: fluid-filled shell vibration, viscoelastic oblate spheroid, infrasound, whole-body vibration, acoustic–structural coupling, ISO 2631. |
| 5 | **Data availability statement** | ✅ PASS | `\section*{Data availability}` present at L170–172. |
| 6 | **CRediT author statement** | ✅ PASS | `\section*{CRediT authorship contribution statement}` covers all 4 authors (Jonathan Mace, Brian R. Mace, Springbank 10 Year Old, GitHub Copilot CLI). |
| 7 | **Competing interests** | ✅ PASS | `\section*{Declaration of competing interest}` at L185–188. |
| 8 | **Cover letter** | ✅ PASS | `cover-letter.tex` exists (102 lines). Addresses the editor, explains contributions, suggests reviewer expertise areas. |
| 9 | **Graphical abstract** | ✅ PASS | `graphical-abstract.png` (143.9 KB) exists, plus `graphical-abstract.py` generation script. |
| 10 | **Supplementary material** | ✅ PASS | `supplementary.tex` exists (detailed derivations, parameter tables). Also `supplementary.pdf` present. |
| 11 | **References** all `\cite{}` keys resolve | ✅ PASS | 24 unique cite keys, all present in `references.bib` (32 entries). 8 unused bib entries (see below). |
| 12 | **Figures** all `\includegraphics` files exist | ✅ PASS | All 7 referenced figures exist in `data/figures/`. |
| 13 | **Line numbering** `\linenumbers` present | ✅ PASS | `\linenumbers` at L27. |
| 14 | **Page count** | ℹ️ INFO | **31 pages** (review double-spaced format). |

## Overall Verdict

**11/13 checks pass.  2 items require fixes before submission.**

## Issues Identified

### ⚠️ MAJOR — Abstract exceeds 200-word limit

- **Current**: ~246 words
- **Required**: ≤200 words (JSV guideline)
- **Action**: Cut ~46 words.  Candidates for trimming: the breathing-mode
  sentence (readers don't need it in the abstract), the Monte Carlo detail
  sentence, or the final "brown note" resolution sentence.

### ⚠️ MAJOR — Two highlights exceed 85-character limit

- **Highlight 1** (93 chars): "Mechanical–airborne coupling disparity of ~10⁴
  explains gastrointestinal vibration asymmetry"
  → Suggested: "~10⁴ mechanical–airborne coupling disparity explains GI vibration asymmetry" (76 chars)
- **Highlight 2** (96 chars): "Fluid-filled viscoelastic shell model predicts
  abdominal resonance at 4–10 Hz (matches ISO 2631)"
  → Suggested: "Viscoelastic shell model predicts abdominal resonance at 4–10 Hz (ISO 2631)" (76 chars)

### ℹ️ MINOR — Multiply-defined label

- LaTeX warning: `Label 'eq:coupling_ratio' multiply defined`.
- Two sections define the same equation label.  Rename one to avoid
  cross-reference ambiguity.

### ℹ️ MINOR — 12 hyperref PDF-string warnings

- `Package hyperref Warning: Token not allowed in a PDF string (Unicode)` ×12.
- Cosmetic only; caused by math in section titles.  Fix with `\texorpdfstring`.

### ℹ️ MINOR — 8 unused BibTeX entries

Entries present in `references.bib` but never cited:
1. `Junger1986` (duplicate of `junger2012sound`)
2. `Fahy2007`
3. `Fung1993`
4. `Geuzaine2009`
5. `Baratta2023`
6. `Hernandez2005`
7. `Leventhall2009`
8. `vonGierke1966`

These do not affect compilation but should be pruned or cited before
submission to keep the reference list clean.

## Figures Inventory

| Figure | File | Size |
|--------|------|------|
| Geometry schematic | `fig_geometry_schematic.pdf` | 34.9 KB |
| Mode shapes | `fig_mode_shapes.pdf` | 29.5 KB |
| Frequency vs E | `fig_frequency_vs_E.pdf` | 31.7 KB |
| UQ Sobol indices | `fig_uq_sobol_indices.png` | 51.3 KB |
| Coupling comparison | `fig_coupling_comparison.pdf` | 33.3 KB |
| Dimensional collapse | `fig_dimensional_collapse.png` | 173.0 KB |
| Scaling law | `fig_scaling_law.png` | 142.5 KB |

## Next Steps

1. **Trim abstract** to ≤200 words (MAJOR — blocks submission)
2. **Shorten highlights 1 & 2** to ≤85 characters each (MAJOR — blocks submission)
3. Fix duplicate `eq:coupling_ratio` label (MINOR)
4. Add `\texorpdfstring` wrappers for math in section headings (MINOR)
5. Prune or cite the 8 unused bib entries (MINOR)
6. After fixes, recompile and verify zero warnings
7. Generate final `supplementary.pdf` from `supplementary.tex`
8. Upload to Elsevier Editorial Manager: main.tex, figures, cover letter,
   graphical abstract, highlights, supplementary material
