# Consistency Audit Report — Round 7 Final Pre-Submission

**Date**: 2026-03-27T0608
**Auditor**: Consistency Auditor (automated)
**Scope**: Final JSV pre-submission check — all paper/*.tex, src/analytical/*.py, cover letter

---

## RESULT: FAIL — 3 CRITICAL issues must be fixed before submission

---

### 1. CRITICAL: Dangling Cross-Reference `\ref{sec:coupling_ratio}`

| Item | Detail |
|------|--------|
| **File** | `paper/sections/section4_coupling.tex` line 65 |
| **Text** | `(\S\ref{sec:coupling_ratio}) are approximately half those shown.` |
| **Problem** | No `\label{sec:coupling_ratio}` exists anywhere in the manuscript |
| **Effect** | Compiles to **"(§??)"** in the PDF — visible to every reviewer |
| **Fix** | Add `\label{sec:coupling_ratio}` to the subsection heading at line 88 of the same file, changing `\subsection{The Coupling Ratio}` to `\subsection{The Coupling Ratio}\label{sec:coupling_ratio}` |

### 2. CRITICAL: Cover Letter Title Does Not Match Paper Title

| Item | Detail |
|------|--------|
| **Cover letter** (line 22) | "Can Infrasound Induce Abdominal Resonance? Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell Model of the Human Abdomen" |
| **Paper** (main.tex line 38–39) | "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the 'Brown Note'" |
| **Problem** | Completely different titles. An editor will notice immediately. |
| **Fix** | Update cover-letter.tex line 22 to match the paper title exactly |

### 3. CRITICAL: Cover Letter MC Range Overstates Upper Bound

| Item | Detail |
|------|--------|
| **Cover letter** (line 61) | `$10^3$--$10^5$` |
| **Paper** (results.tex line 82, conclusion.tex line 37, discussion.tex lines 7, 360, 476) | `$10^3$--$10^4$` consistently |
| **Problem** | Cover letter claims the coupling ratio spans up to 10⁵; paper consistently says 10⁴. An order-of-magnitude discrepancy. |
| **Fix** | Change cover-letter.tex line 61 from `$10^3$--$10^5$` to `$10^3$--$10^4$` |

---

### WARNINGS (Non-blocking but should fix)

#### W1. README.md Has Stale Coupling Ratio (46,000×)

- **Lines 11, 22**: Still say "~46,000×" instead of "~66,000×" (6.6×10⁴)
- Not submitted to JSV, but visible on GitHub. Fix after submission.

#### W2. TODO Comments in Unused Draft Sections

- `paper/sections/background.tex`: 7 TODO comments (lines 11, 12, 21, 22, 30, 31, 47)
- `paper/sections/methods.tex`: 5 TODO comments (lines 37, 52, 56, 60, 64)
- These files are **not** `\input`'d by main.tex, so they don't appear in the compiled PDF.
- Should be cleaned up or deleted to avoid confusion if the repo goes public.

#### W3. v1 Imports in Legacy Code

- `src/analytical/acoustic_coupling.py` line 43: imports from `natural_frequency` (v1)
- `src/postprocess/generate_figures.py` line 19: imports from `natural_frequency` (v1)
- Not used by the paper pipeline. Mark as deprecated or update.

#### W4. 8 Unused BibTeX Entries

Baratta2023, Fahy2007, Fung1993, Geuzaine2009, Hernandez2005, Junger1986, Leventhall2009, vonGierke1966 — present in references.bib but never cited. Not an error (BibTeX only includes cited entries) but untidy.

---

### PASS — Verified Items

#### Coupling Ratio Values ✅

| Location | Value | Correct? |
|----------|-------|----------|
| Abstract (main.tex line 105) | `$7 \times 10^4$` (rounded) | ✅ |
| Highlight 1 (main.tex line 84) | `${\sim}7\times 10^4$` | ✅ |
| Introduction (introduction.tex line 76) | `$6.6 \times 10^4$` | ✅ |
| Section 2 range (section2_formulation.tex line 258) | `$\sim 10^3$--$10^4$` (MC range) | ✅ |
| Eq. 30 (section4_coupling.tex line 94) | `$\frac{917}{0.014} \approx 6.6 \times 10^4$` | ✅ |
| Γ₂-corrected (section4_coupling.tex line 129) | `$\sim 3 \times 10^4$` | ✅ |
| Conclusion (conclusion.tex line 5) | `$6.6 \times 10^4$` | ✅ |
| Cover letter (lines 34, 50, 55, 77) | `$6.6 \times 10^4$` | ✅ |

#### Canonical Parameters — Code vs Paper ✅

| Parameter | Code Default | Table 1 | Match? |
|-----------|-------------|---------|--------|
| a | 0.18 m | 0.18 m | ✅ |
| c | 0.12 m | 0.12 m | ✅ |
| h | 0.010 m | 0.010 m | ✅ |
| E | 0.1e6 Pa | 0.1 MPa | ✅ |
| ν | 0.45 | 0.45 | ✅ |
| ρ_w | 1100 kg/m³ | 1100 kg/m³ | ✅ |
| ρ_f | 1020 kg/m³ | 1020 kg/m³ | ✅ |
| K_f | 2.2e9 Pa | 2.2 GPa | ✅ |
| P_iap | 1000 Pa | 1000 Pa | ✅ |
| η | 0.25 | 0.25 | ✅ |

#### Code-Paper Numerical Agreement ✅

| Quantity | Code Output | Paper Value | Δ |
|----------|------------|-------------|---|
| R_eq | 0.1572 m | 0.157 m | <1% |
| f₂ | 3.95 Hz | 4.0 Hz | 1.3% (rounding) |
| f₀ | 2491 Hz | ~2500 Hz | <1% (rounding) |
| ka | 0.0114 | 0.0114 | exact |
| (ka)² | 1.30×10⁻⁴ | 1.3×10⁻⁴ | exact |
| ξ_energy (120 dB) | 0.0137 μm | 0.014 μm | 2% (rounding) |
| ξ_pressure (120 dB) | 0.184 μm | 0.18 μm | 2% (rounding) |
| ratio press/energy | 13.42 | ~13.4 | exact |
| ξ_mech (0.1 m/s²) | 917.3 μm | 917 μm | <0.1% |
| ξ_mech (0.5 m/s²) | 4586.3 μm | 4586 μm | <0.1% |
| ξ_mech (1.15 m/s²) | 10548.6 μm | 10549 μm | <0.1% |
| Q | 4.0 | 4.0 | exact |
| ζ | 0.125 | 0.125 | exact |
| k_shell | 1.47×10⁵ Pa/m | ~1.5×10⁵ Pa/m | 2% (rounding) |

All discrepancies are standard rounding to 2 significant figures. **No violations >1%.**

#### Other Checks ✅

| Check | Result |
|-------|--------|
| ka = 0.0114 at f₂ ≈ 4 Hz | ✅ Correct |
| PIEZO thresholds labelled (pressure vs energy) | ✅ Table 4 footnote + Table 4 dual rows |
| Γ₂ notation vs ζ_rad notation | ✅ No conflict (different quantities) |
| Abstract word count | ✅ ~161 words (limit: 200) |
| Highlights character count | ✅ All ≤70 chars (limit: 85) |
| No stale 46,000 or 4.6×10⁴ in paper .tex files | ✅ |
| No stale η=0.30, ka=0.017, R_eq=0.133 | ✅ |
| Supplementary k_shell uses (1-ν)=0.55 | ✅ (line 211) |
| Supplementary k_shell gives ~1.5×10⁵ | ✅ (line 212) |
| All \cite{} keys exist in references.bib | ✅ (32/32 found) |
| All figure files exist | ✅ (7/7 found) |
| Q = 1/η, ζ = η/2 self-consistent | ✅ |

---

## Summary

| Severity | Count | Items |
|----------|-------|-------|
| **CRITICAL** | **3** | Dangling \ref, title mismatch, MC range mismatch |
| WARNING | 4 | Stale README, TODOs in unused sections, v1 imports, unused bib entries |
| PASS | 20+ | All coupling ratios, parameters, code-paper values, citations, figures |

**Recommendation**: Fix the 3 CRITICAL issues (estimated 5 minutes of LaTeX editing) before submission. The warnings can be addressed post-submission.
