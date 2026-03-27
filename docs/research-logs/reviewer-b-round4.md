# Reviewer B — Round 4

**Date:** 2026-03-27  
**Reviewer:** B (Computational Acoustics / Fluid–Structure Interaction)  
**Manuscript:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the 'Brown Note'"  
**Journal:** Journal of Sound and Vibration  

**Documents reviewed (complete):**
- `paper/main.tex` and all seven section files in `paper/sections/`
- All 17 Python modules in `src/analytical/`
- `data/results/fea_modal_results.json`, `data/results/uq_results.json`
- Round 3 review and prior review history

---

## Decision: MAJOR REVISION

The authors made substantial progress since Round 3: the qualitative physics is sound, the coupling-comparison framing is the right story, and the code base is now far more mature than many JSV submissions. However, **the near-fatal parameter mismatch flagged in Round 3 (F1) was only partially fixed**. Residual numerical inconsistencies—including an internally contradictory abstract—persist throughout the manuscript and will destroy the paper's credibility with any careful reader. Additionally, two prior open issues (M2 and M4) remain unresolved in the manuscript text. These are fixable, but the fix must be complete and verified before acceptance.

---

## Fatal Flaws

### F1. Abstract is internally inconsistent on the central result

The abstract (lines 106–110 of `main.tex`) simultaneously claims:

1. "wall displacements of order **0.01 μm** at 120 dB SPL" (energy-consistent estimate)
2. "mechanical whole-body vibration…produces displacements roughly **10⁴** times larger"

These two statements are mutually contradictory. If ξ_air = 0.01 μm and ξ_mech at the EU action value (0.5 m/s²) = 3243 μm (Table 4), the ratio is 3.2 × 10⁵, not 10⁴. The 10⁴ figure is only obtained using the pressure-based ξ_air ≈ 0.14 μm (Section 2, after Eq. 14). The paper cannot simultaneously use the energy estimate (0.01 μm, which is 10× smaller) and the coupling ratio derived from the pressure estimate.

**Action required:** Choose ONE displacement estimate for the airborne pathway and use it consistently in the abstract, Section 2 inline result, Table 3, Discussion, and Conclusions. Propagate the corresponding coupling ratio everywhere. Currently the paper has at least three different numbers for the same quantity at 120 dB:

| Location | ξ_air at 120 dB | Estimate type |
|----------|----------------|---------------|
| Abstract (line 107) | ~0.01 μm | Energy-consistent |
| Section 2 after Eq. 14 (line 207) | 0.14 μm | Pressure-based |
| Table 3, Section 4 (xi_energy) | 0.014 μm | Energy-consistent |
| Table 3, Section 4 (xi_pressure) | 0.18 μm | Pressure-based |

The 0.14 μm in Section 2 and the 0.18 μm in Table 3 are also inconsistent (factor 1.3×), likely from differing Q values—see F2.

### F2. Loss tangent / Q-factor inconsistency persists (partial F1 fix from Round 3)

Table 1 (`section2_formulation.tex`, line 43) states η = 0.25, implying Q = 4.0 and ζ = 0.125. However:

- The text below Eq. 3 (`section2_formulation.tex`, line 70–72) states "baseline value η = 0.30 (Q = 3.3)"
- Tables 3 and 4 (`section4_coupling.tex`) use Q = 4.0 in their captions
- The Discussion (`discussion.tex`, line 38) states ζ_struct = 0.15, which corresponds to η = 0.30
- The UQ code (`uncertainty_quantification.py`, line 73) uses nominal η = 0.25

Table 1 and the Tables 3/4 agree (η = 0.25, Q = 4.0), but the running text in Section 2 and the Discussion use η = 0.30 (Q = 3.3). This is precisely the kind of residual mismatch that Round 3 flagged. It propagates into every displacement calculation and into the PIEZO threshold SPL reported in Table 2 (135 dB—computed with what Q?).

**Action required:** Harmonise η to a single canonical value throughout. Update all inline numerical results and all tables.

---

## Major Issues

### M1. Residual v1 parameters in Section 2's ka calculation

Section 2, Eq. 12 (`section2_formulation.tex`, line 185) states ka ≈ 0.017 at 7 Hz. This value is computed from R_eq = 0.131 m, which corresponds to the v1 code defaults (a = 0.15 m, c = 0.10 m), **not** the canonical Table 1 parameters (a = 0.18, c = 0.12 → R_eq = 0.157 m). With Table 1 parameters, ka at 7 Hz = 0.020, and at f₂ = 4.0 Hz, ka = 0.011.

The (ka)² penalty at Eq. 13 follows: 0.017² = 2.8 × 10⁻⁴ (paper), vs. 0.020² = 4.0 × 10⁻⁴ (Table 1), vs. 0.011² = 1.3 × 10⁻⁴ (at actual n = 2 resonance). These differ by up to 3×. **This is the remnant of the Round 3 F1 bug—it was not fully excised.**

The correct ka to use depends on what frequency you evaluate: 7 Hz (arbitrary) or f₂ ≈ 4.0 Hz (the actual resonance). Eq. 14's displacement should be evaluated at f₂, not 7 Hz, since the driving question is "what happens at resonance?" Clarify and correct.

### M2. Theory vs. ISO displacement gap still unaddressed (carried from Round 3)

The theoretical SDOF model at 1.15 m/s² predicts ξ_rel ≈ 7459 μm (Table 4). ISO 2631 transmissibility data at the same frequency gives an empirical estimate roughly 3.75× lower (~1900 μm). This gap was identified in Round 3's M2 and **is nowhere discussed in the paper**. A linear SDOF with Q = 4 is a known overestimate because:

- Multi-DOF body dynamics redistribute energy across modes
- Nonlinear strain-stiffening of tissue limits large displacements
- Partial boundary constraints reduce the effective Q

The Limitations section (§5.4, item 1) mentions nonlinearity in passing but does not quantify the expected reduction or connect it to the 3.75× gap. Since the mechanical displacement is the paper's positive claim ("WBV explains ISO 2631 effects"), overpredicting it by nearly 4× is not a neutral error—it inflates the coupling ratio and makes the argument look better than it is.

**Action required:** Add a paragraph in the Discussion comparing the SDOF prediction to ISO transmissibility-derived estimates. Acknowledge the ~4× overshoot explicitly. Argue (correctly) that the coupling *ratio* is robust because the overshoot cancels, but do not leave the reader to discover the discrepancy independently.

### M3. FEA boundary condition results exist but are absent from the paper

The file `data/results/fea_modal_results.json` contains Rayleigh–Ritz results for free, simply-supported hemisphere, clamped hemisphere, and 25%-constrained boundary conditions. These data directly address the Limitations item 3 (free-shell BC) and are far more informative than the hand-waving "1.3–3.0×" estimate in §3.5. Key findings from the JSON:

| BC | f₁ (Hz) | Ratio to free |
|----|---------|---------------|
| Free sphere (Ritz) | 4.13 | 1.00 |
| Hemisphere SS | 3.91 | 0.95 |
| Hemisphere clamped | 3.89 | 0.94 |
| 25% constrained | 3.66 | 0.89 |

These show that partial clamping **lowers** the fundamental frequency (contrary to the paper's claim that "partial constraints raise the n = 2 frequency by 1.3–3.0×" in §3.5, line 119). This is presumably because constraining part of the boundary changes the mode shape, and the lowest eigenvalue of a partially constrained problem can shift in either direction depending on the constraint geometry. The paper's claim of 1.3–3.0× frequency *increase* from partial clamping appears to be **wrong**, at least for the geometries tested.

**Action required:** Incorporate the FEA results into the paper (a table or figure). Correct or remove the 1.3–3.0× claim. This is essential for the paper's credibility on boundary conditions.

### M4. Equation 11 vs. Table 4: √2 inconsistency in base displacement

Equation 11 (`section2_formulation.tex`, line 223) defines:

$$x_\text{base} = \frac{a_\text{rms} \sqrt{2}}{\omega^2}$$

This converts RMS acceleration to peak displacement. However, Table 4's numerical values are consistent with x_base = a_rms / ω² (no √2). For example, at 0.1 m/s² and f₂ ≈ 3.95 Hz: Eq. 11 gives x_base = 229 μm, but Table 4 reports 162 μm, which matches a_rms/ω² = 162 μm exactly. I verified this computationally.

Either Eq. 11 or Table 4 is wrong. If the equation is correct, every mechanical displacement in the paper is understated by √2 ≈ 1.41×. If the table is correct, the equation needs fixing. This ambiguity propagates into the coupling ratio.

**Action required:** Clarify whether displacements are peak or RMS throughout. Ensure the equation and all tables are consistent. I recommend using peak values (as Eq. 11 states) and recalculating the tables.

### M5. Table 4 vs. Table 6 internal inconsistency

Tables 4 and 6 (`section4_coupling.tex` and `discussion.tex`) both report mechanical displacements at the same conditions but give different numbers:

| Condition | Table 4 (§4) | Table 6 (§5) | Ratio |
|-----------|-------------|-------------|-------|
| 0.5 m/s² | 3243 μm | 3115 μm | 1.041 |
| 1.15 m/s² | 7459 μm | 7165 μm | 1.041 |

The constant 4.1% ratio suggests these were computed with slightly different parameters or code versions. In a paper whose prior reviews have flagged parameter consistency, this is unacceptable.

**Action required:** Regenerate all tables from a single canonical computation. A simple validation script that produces every number in every table from a single parameter file would prevent this class of error.

### M6. Coupling ratio Eq. 17 compares non-equivalent exposure conditions

Equation 17 and the surrounding text (`section4_coupling.tex`, line 89) define:

$$\mathcal{R} = \frac{\xi_\text{mech}}{\xi_\text{air}} = \frac{649}{0.014} \approx 4.6 \times 10^4$$

This uses ξ_mech at 0.1 m/s² (a sub-regulatory, moderate exposure) and ξ_air at 120 dB (the threshold of pain—an extreme exposure). Comparing mild mechanical with extreme acoustic is physically misleading. A more defensible comparison would use matched occupational exposures: EU action value (0.5 m/s²) vs. typical environmental infrasound (60–80 dB), yielding a ratio on the order of 10⁶–10⁷, or the EU limit vs. 120 dB, yielding ≈ 5 × 10⁵.

The paper's choice of 0.1 m/s² vs. 120 dB actually *understates* the coupling disparity. While this makes the argument conservative, it invites criticism that the comparison is cherry-picked. More importantly, the 10⁴ claim is used as the paper's headline number (abstract, highlights, conclusion) even though it depends entirely on which exposure levels are paired.

**Action required:** Define the coupling ratio for matched occupational conditions and explain the sensitivity to exposure level. Consider presenting a figure showing R as a function of both a_rms and SPL.

---

## Minor Issues

### m1. UQ median E does not match Table 1 baseline

The uncertainty quantification (`uncertainty_quantification.py`, line 65) places E on a log-normal distribution with 5th percentile = 0.05 MPa and 95th = 2.0 MPa. The resulting log-normal median is exp[(ln 50000 + ln 2000000)/2] ≈ 316 kPa = 0.316 MPa—more than 3× the Table 1 baseline of 0.1 MPa. This explains why the UQ median f₂ (7.5 Hz in Table 2) is much higher than the canonical point estimate (4.0 Hz) and why the UQ median ξ_mech (600 μm) is 5.4× lower than the canonical (3243 μm). The discrepancy is not an error per se—the wide log-normal range is physiologically defensible—but it should be explicitly discussed so readers understand why the "baseline" and "UQ median" differ so dramatically.

### m2. Uncertainty not propagated to all key results

Table 2 provides MC intervals for f₂, ξ_air, ξ_mech, R, and the PIEZO-threshold SPL—good. However, the breathing mode frequency f₀, the BC multiplier, and the oblate spheroid correction factor (Table 7) have no uncertainty estimates. The Sobol analysis covers only f₂. Since the paper argues that the *ratio* R is robust, showing MC distributions for R decomposed by contributing factors (ka penalty, Q, frequency) would substantially strengthen this claim.

### m3. Breathing mode frequency: ~2900 Hz in abstract, ~2500 Hz in conclusion

The abstract (line 98) says "breathing mode…sits near 2500 Hz." The highlights (line 85) say 2900 Hz. My computation with Table 1 parameters gives 2491 Hz. These should be consistent. (The difference is inconsequential to the argument but looks sloppy.)

### m4. historical-notes.tex not integrated

The file `paper/sections/historical-notes.tex` contains excellent historical context on Gavreau, Mohr et al., von Gierke, Tandy & Lawrence, and the MythBusters episode. It is referenced nowhere in `main.tex` and does not appear in the paper. This material belongs in the Introduction—it provides the scholarly context that a JSV paper on this topic needs.

### m5. Orphan sections: methods.tex and background.tex

The files `paper/sections/methods.tex` and `paper/sections/background.tex` contain incomplete FEA-based formulations with multiple TODO placeholders. These are not included in `main.tex` and appear to be from an earlier draft. They should be deleted or clearly marked as supplementary to avoid confusion.

### m6. Code v1 vs. v2 model: both still present

`natural_frequency.py` (v1) and `natural_frequency_v2.py` (v2) coexist. The v1 code uses different defaults (a = 0.15, E = 0.5 MPa, h = 0.015, ν = 0.49, ρ_wall = 1050) that do not match Table 1. Several modules (`acoustic_coupling.py`) still import from v1. While the paper appears to use v2 results, a reviewer cannot easily verify this without running the code. A canonical parameter file imported by all modules would eliminate this risk.

### m7. Section numbering gap

The paper structure implies six sections (Introduction, Formulation, Parametric Study, Coupling, Discussion, Conclusions) but Section 2 contains the coupling analysis derivation that properly belongs with Section 4. The parametric study (§3) follows the formulation naturally but precedes the coupling comparison (§4) in a way that splits the coupling story across two non-adjacent sections.

### m8. Missing references

The following relevant works appear uncited:

- Leissa (1993), *Vibration of Shells*—the standard reference for shell vibration modes, cited in the Limitations but not in the formulation section where the actual shell theory is developed
- Fahy & Gardonio (2007), *Sound and Structural Vibration*—relevant to the acoustic coupling framework
- Prospective FEA validation references (e.g., COMSOL/ABAQUS shell-fluid benchmarks)

### m9. Thin-shell validity marginal

Section 2 (`section2_formulation.tex`, line 23) acknowledges h/R ≈ 0.06, which exceeds the conventional thin-shell limit of 0.05. With the multi-layer model (h_total = 25.1 mm, §3.4), h/R ≈ 0.16, well into the thick-shell regime. The claimed "4% Mindlin–Reissner correction" (Discussion, item 4) applies only to the 10 mm wall; for the multi-layer case the correction would be substantially larger. This should be noted.

### m10. Figures not verifiable

All figures reference PDF/PNG files in `data/figures/` that I cannot render from the TeX source alone. The paper should include figure generation scripts or at minimum specify which code module and parameters produce each figure, enabling reproduction.

---

## Positive Comments

1. **The coupling-comparison framework is the paper's genuine contribution.** The idea of comparing airborne and mechanical pathways to the *same* modal structure via the (ka)^n penalty is elegant, physically correct, and—to my knowledge—novel in the infrasound-physiology literature. This alone justifies publication if the numbers are cleaned up.

2. **The energy-budget reciprocity analysis (§4.4)** is a rigorous self-consistency check that most JSV papers on fluid–structure coupling do not attempt. The absorption efficiency of ~10⁻¹⁴ is a striking and memorable result.

3. **The alternative pathways analysis (§5.3)** adds genuine scientific value. The gas-pocket mechanism as a local pressure-to-displacement transducer is a genuinely novel observation that explains inter-individual variability and deserves follow-up.

4. **Code quality is above average** for an analytical acoustics paper. The `src/analytical/` modules are well-documented, physically motivated, and include parametric sweeps and sensitivity analyses that go well beyond what appears in the paper. The viscous correction analysis (proving inviscid approximation is justified to within 1%) is particularly thorough.

5. **The writing is unusually good** for a technical acoustics paper. The prose is clear, occasionally witty ("on rather thin thermodynamic ice"), and maintains consistent voice throughout. The Discussion is balanced and the Limitations section is commendably honest.

6. **The Rayleigh–Ritz oblate spheroid analysis** (Table 7, `oblate_spheroid_ritz.py`) is a valuable contribution showing the sphere approximation overestimates frequencies by 11–20%. This provides the reader with a quantified correction, which is more useful than the common practice of simply noting the approximation.

7. **The uncertainty quantification** (Sobol indices identifying E as 86% of variance) gives the reader actionable guidance for future experimental work—precisely the kind of result that elevates a theoretical paper.

---

## Summary

This is a creative and well-framed paper addressing a question that is equal parts absurd and legitimate. The physics is fundamentally sound, the coupling-disparity argument is correct and novel, and the code base is impressive. However, the manuscript contains a web of numerical inconsistencies—different parameter values in the text vs. tables, different displacement estimates for the same scenario across sections, an abstract that contradicts itself, and FEA results that contradict a claim in the text but are never shown. These are not physics errors; they are bookkeeping failures that could be fixed in a disciplined editing pass with a single canonical computation script.

My recommendation is **Major Revision** because the number of interrelated fixes is large enough that the corrected manuscript will need fresh verification. The path to acceptance is clear:

1. Fix F1 and F2 (canonical parameters, one displacement estimate, consistent Q).
2. Incorporate the FEA BC results (M3) and correct the 1.3–3.0× claim.
3. Discuss the SDOF vs. ISO gap (M2) honestly.
4. Fix the √2 issue (M4) and regenerate all tables from one script (M5).
5. Redefine the coupling ratio for matched conditions (M6).
6. Integrate the historical notes (m4) and clean up orphan files (m5).

With these changes—none of which require new physics—the paper would be a strong contribution to JSV.
