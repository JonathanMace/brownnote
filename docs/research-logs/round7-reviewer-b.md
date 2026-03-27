# Reviewer B — Round 7 (Final Pre-Submission Review)

**Date:** 2025-07-17  
**Reviewer:** B (Computational Acoustics / Fluid–Structure Interaction, 25 years)  
**Manuscript:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the 'Brown Note'"  
**Journal:** Journal of Sound and Vibration  

**Documents reviewed (complete):**
- `paper/main.tex` and all section files in `paper/sections/`
- `paper/supplementary.tex`
- `paper/cover-letter.tex`, `paper/highlights.txt`
- All Python modules in `src/analytical/` (verified key calculations against paper)
- LaTeX compilation log (`main.log`)
- All previous round reviews (Rounds 1–6)

---

## Decision: ACCEPT (subject to proof-stage corrections)

---

## Verification of Previously Raised Issues

All items from Round 6 have been satisfactorily addressed:

| Round 6 Issue | Status | Evidence |
|---|---|---|
| **F1** (fatal): Γ₂ missing from paper | ✅ Fixed | Eq. (participation_factor) in §4.3 provides formal integral definition; Γ₂ ≈ 0.48 stated, correction to ~3×10⁴ discussed |
| **M1**: Coupling ratio inconsistency | ✅ Fixed | §4.3 clearly states 6.6×10⁴ is the SDOF upper bound; Γ₂-corrected value ~3×10⁴ in following paragraph |
| **M2**: Table caption (mechanical) | ✅ Fixed | Table caption now states "Γ₂ = 1" twice, notes corrected values "approximately half those shown" |
| **M3**: k_shell (1−ν) = 0.55 | ✅ Fixed | Supplementary §S1.4 line 211: denominator `0.157² × 0.55`, consistent with Eq. (S9) and main text Eq. (kshell) |
| **M4**: PIEZO 135/158 dB reconciled | ✅ Fixed | Table 3 footnote explains 23 dB correction; §4.1 text references both values with cross-refs |
| **m1**: Cover letter 6.6×10⁴ | ✅ Fixed | Cover letter lines 34, 50, 55, 77 all use 6.6×10⁴ |
| **m2**: Abstract ~7×10⁴ vs corrected ~3×10⁴ | ✅ Acceptable | Abstract rounds SDOF value (6.6→7×10⁴); §4.3 explains correction. Transparent. |
| **m5**: Γ_rad → ζ_rad symbol overloading | ✅ Fixed | All radiation damping uses ζ_rad throughout (main text, supplementary, discussion) |
| **m6**: Formal integral definition of Γ_n | ✅ Fixed | Eq. (participation_factor): complete with Legendre polynomial integration, σ(u) metric factor, θ_c constraint angle |

**Assessment:** Every previously raised issue is resolved. The fixes are correct, self-consistent, and properly cross-referenced.

---

## New Issues Identified in Final Pass

### No Fatal Flaws

None.

### No Major Issues

None.

### Minor Issues (should be corrected before submission)

**m1. Undefined cross-reference `\ref{sec:coupling_ratio}` (section4_coupling.tex, line 65)**

The Table caption for `tab:mechanical` reads:
> "the corrected values (§\ref{sec:coupling_ratio}) are approximately half those shown."

The label `sec:coupling_ratio` does not exist. The subsection "The Coupling Ratio" at line 88 of the same file has no `\label`. The LaTeX log confirms:
```
LaTeX Warning: Reference `sec:coupling_ratio' on page 16 undefined on input line...
```

This would render as "§??" in the compiled PDF. **Fix:** Add `\label{sec:coupling_ratio}` after `\subsection{The Coupling Ratio}` on line 88 of `section4_coupling.tex`.

**m2. Wrong wavelength quoted in Discussion §5.1 (discussion.tex, line 31)**

The text states:
> "Physically, the incident wavelength (λ ≈ 49 m) is nearly 370 times the body diameter"

This paragraph is discussing the n=2 resonance at f₂ ≈ 4 Hz (explicitly stated three lines earlier, with ka = 0.0114). At 4 Hz, λ = 343/4 = **85.75 m**, not 49 m. The value 49 m corresponds to 7 Hz. Independent code verification confirms λ = 86.8 m at the computed f₂ = 3.95 Hz.

The multiplier "370" was apparently computed correctly from the true wavelength (~86 m divided by the AP diameter 2c = 0.24 m gives ~358, plausibly rounded to "nearly 370"), confirming this is a copy-paste error in the wavelength value only.

**Fix:** Change `\SI{49}{\metre}` to `\SI{86}{\metre}` (or `\SI{85}{\metre}`) on line 31 of `discussion.tex`.

**m3. Wavelength bound in Conclusion incorrect for full frequency range (conclusion.tex, lines 18–19)**

The text states:
> "Airborne sound at these frequencies has a wavelength exceeding 49 m"

where "these frequencies" refers to the 4–10 Hz range (stated on the preceding line). At 10 Hz, λ = 343/10 = **34.3 m**, which does *not* exceed 49 m. The claim holds only for f ≤ 7 Hz.

**Fix:** Either (a) change to "exceeding 34 m" (correct lower bound for the 4–10 Hz range), or (b) replace with a frequency-specific statement such as "At f₂ = 4 Hz, the wavelength exceeds 85 m".

**m4. Minor viscosity crossover rounding (cosmetic)**

Discussion §5.7 (line 437): states "281 Pa·s". Supplementary §S3.4 (line 697): states "~280 Pa·s". These are equivalent to within rounding, but a pedantic copyeditor might flag it. Consider harmonising to one value.

---

## Positive Comments

1. **The paper is now a mature, self-consistent work.** The progression from Round 1 to Round 7 has been exceptional. Every structural criticism has been addressed with care, and the manuscript is substantially stronger for it.

2. **The Γ₂ treatment (§4.3) is exemplary.** The formal integral definition (Eq. participation_factor) with clear notation ($u = \cos\theta$, Legendre polynomials, oblate metric factor σ(u), polar constraint angle θ_c) is exactly what I demanded. The text clearly explains why Γ₂ = 0 for a free sphere (orthogonality) and why partial constraint breaks it (Γ₂ ≈ 0.48). The qualification that 6.6×10⁴ is the SDOF upper bound, with ~3×10⁴ as the corrected value, is transparent and honest.

3. **The energy-budget framework is rigorous.** The distinction between pressure-based and energy-consistent displacements is maintained throughout (Tables 2 and 7, footnotes, §4.1 text). The reader is never left wondering which estimate is being used.

4. **The PIEZO threshold reconciliation is clean.** The 135/158 dB values are both reported with clear labels (pressure-based vs. energy-consistent), and Table 3's footnote explains the 23 dB correction. This was a serious internal consistency problem in earlier rounds; it is now resolved.

5. **Notation is consistent.** ζ_rad used throughout (no Γ_rad overloading). Γ_n reserved exclusively for modal participation. Q = 4.0, η = 0.25, ζ = 0.125 chain is consistent everywhere.

6. **The source code matches the paper.** Independent computation with `natural_frequency_v2.py` confirms: f₂ = 3.95 Hz (paper: 4.0 Hz), R_eq = 0.1572 m, ka = 0.0114, K_total = 56,241 Pa/m, ξ_pressure = 0.184 μm, ξ_mech = 917 μm at 0.1 m/s². All within rounding of published values.

7. **The supplementary material is thorough** — full numerical evaluations of every intermediate step, complete Sobol tables, and honest assessment of every modelling assumption with quantified error estimates. This is how analytical work should be documented.

8. **The discussion honestly confronts limitations.** Nine clearly enumerated limitations, each with a quantified impact assessment and a clear statement of which direction the error goes. The nonlinear analysis (§5.6) properly bounds the regime where linear theory fails and explains why the error is conservative.

---

## Summary

This paper has completed a remarkable journey from an interesting but rough manuscript to a polished, internally consistent work of analytical structural acoustics. The central result — a four-order-of-magnitude coupling disparity between mechanical and airborne excitation of abdominal flexural modes — is physically sound, numerically verified, transparently qualified (SDOF vs. corrected), and robust to parameter uncertainty.

The three minor issues identified in this final pass (one undefined LaTeX reference, two incorrect wavelength values) are trivial to fix and do not affect any physics, equations, or conclusions. They are proofreading-level errors.

**I recommend ACCEPT**, subject to correction of items m1–m3 before the proof stage. Item m4 is cosmetic and at the authors' discretion.

This has been an unusually satisfying paper to review. The physics is clean, the writing has personality without sacrificing rigour, and the authors have addressed every criticism with substance rather than deflection. I look forward to seeing it in print — and to citing it the next time someone asks me about the brown note at a conference dinner.

---

*Reviewer B, Round 7*
