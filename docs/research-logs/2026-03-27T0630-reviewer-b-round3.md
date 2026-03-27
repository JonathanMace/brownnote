# Reviewer B — Round 3 Review

**Date:** 2026-03-27T06:30
**Reviewer:** B (Computational Acoustics / Fluid-Structure Interaction)
**Manuscript:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for Airborne vs. Mechanical Low-Frequency Excitation"
**Target journal:** Journal of Sound and Vibration

**Documents reviewed:**
- `paper/main.tex` (abstract, structure)
- `paper/sections/introduction.tex`
- `paper/sections/section2_formulation.tex` (core math)
- `paper/sections/results.tex` (parametric study)
- `paper/sections/section4_coupling.tex` (coupling comparison)
- `paper/sections/discussion.tex`
- `paper/sections/conclusion.tex`
- `paper/references.bib`
- `src/analytical/natural_frequency_v2.py` (core modal model)
- `src/analytical/mechanical_coupling.py` (WBV pathway)
- `src/analytical/energy_budget.py` (reciprocity analysis)
- `src/analytical/gas_pocket_resonance.py` (bowel gas mechanism)
- Round 2 review and response documents

---

## 1. Overall Assessment: MAJOR REVISION

The paper has improved substantially since Round 2. The qualitative physics
remains sound, and the coupling-comparison framing is the right story to tell.
However, I have identified **one near-fatal flaw** (paper–code parameter
mismatch that invalidates every number in the manuscript) and **five major
issues** that must be resolved. With these fixes, the paper could reach
MINOR REVISION status.

---

## 2. Progress Since Round 2

### What improved:
- **M1 (energy budget):** The `energy_budget.py` reciprocity analysis is a
  correct and elegant approach. The absorption cross-section formulation via
  Junger & Feit is the right physics. The framework is in place.
- **M3 (transmissibility formula):** Fixed. The code now uses the correct
  complex-valued absolute transmissibility `T_abs = √((1+(2ζr)²)/((1-r²)²+(2ζr)²))`.
  The paper's §2.6 presents the correct `H_rel` formula.
- **M5 (mechanotransduction on v1):** Resolved. All analysis now uses v2.
- **Section 4 (coupling comparison):** This section is new and is the paper's
  strongest contribution. The side-by-side tables are effective.
- **Paper structure:** The LaTeX manuscript is well-organized with proper
  section flow. The abstract tells a clear story.

### What didn't improve (or got worse):
- **M2 (theory/empirical gap):** Not addressed in the paper at all. The 3.75×
  discrepancy between theoretical SDOF and ISO transmissibility is never
  mentioned. The paper presents only the theoretical H_rel = Q result.
- **M4 (partial-shell BCs):** Still handled with a vague "1.3–3.0×" estimate
  in §3.4 with no citation or FEA validation.
- **A new critical problem has appeared:** The paper's stated parameters
  (Table 1) do not produce the numerical results claimed throughout the
  manuscript (see F1 below).

---

## 3. Fatal / Near-Fatal Flaws

### F1. EVERY NUMERICAL VALUE IN THE PAPER IS WRONG RELATIVE TO ITS STATED PARAMETERS

**Severity: Near-fatal (completely undermines quantitative credibility)**

Table 1 of the paper specifies the baseline model: a = 0.18 m, c = 0.12 m,
h = 0.010 m, E = 0.1 MPa, ν = 0.45. I ran the authors' own code
(`natural_frequency_v2.py`) with these exact parameters and compared:

| Quantity | Paper claims | Code with Table 1 params | Discrepancy |
|----------|-------------|-------------------------|-------------|
| f₀ (breathing) | ~2900 Hz | 2472 Hz | **17% too high** |
| f₂ (n=2 flexural) | 4.4 Hz | 3.93 Hz | **12% too high** |
| f₃ (n=3) | 6.7 Hz | 6.28 Hz | **7% too high** |
| f₄ (n=4) | 9.4 Hz | 8.85 Hz | **6% too high** |
| ka at 7 Hz | 0.017 | 0.020 | **18% too low** |
| ξ_mech at 1.15 m/s² | 7000 μm | 8894 μm | **21% too low** |
| x_base at 1.15 m/s² | 2150 μm | 2668 μm | **19% too low** |

**Root cause identified.** The `AbdominalModelV2` class has default parameters
`h = 0.015 m` and `ν = 0.49` that differ from Table 1's `h = 0.010 m` and
`ν = 0.45`. Running the code with h=0.015, ν=0.49 reproduces the paper's
values exactly (f₂ = 4.38, f₃ = 6.74, f₄ = 9.38). Furthermore, the breathing
mode frequency of 2900 Hz matches the code's *default geometry* (a=0.15,
c=0.10 → R_eq=0.131 m), not the paper's geometry (a=0.18, c=0.12 →
R_eq=0.157 m).

**In short:** The paper's Table 1 describes one model; every numerical result
in the paper was computed with a different model. The author appears to have
updated the parameter table without recomputing the results, or vice versa.

This is not merely a presentation error—it means:
1. A reader attempting to reproduce the results from the stated parameters
   will fail.
2. The E-sweep table (Table 2) is wrong: the code gives f₂ values of
   (3.3, 3.9, 4.9, 7.0, 9.6, 13.3) Hz for the stated geometry, not the
   (3.6, 4.4, 5.6, 8.3, 11.5, 16.1) Hz in the paper.
3. The airborne displacement table (Table 3) shows systematic ~8% errors.
4. The mechanical displacement table (Table 4) has ~24% errors.

**Fix (mandatory before any further review):** Pick ONE canonical parameter
set. Recompute ALL tables, ALL in-text numbers, and ALL abstract claims from
that single parameter set using a single deterministic script. Provide the
script as supplementary material. This is a non-negotiable prerequisite for
publication in any quantitative journal.

---

## 4. Major Issues

### M1. Energy budget ratio is 13×, not the "~1.4×" claimed

**Severity: Major (internal inconsistency in the supporting analysis)**

The `energy_budget.py` code computes a pressure-to-energy displacement ratio
of **13.4×** at 120 dB (ξ_pressure = 0.152 μm vs ξ_energy = 0.011 μm). This
ratio is invariant across SPL and parameter choices. Yet the summary text
hardcoded in the same file (lines 297–303) states:

> "The factor of ~1.4 difference does not change any conclusions."

This is off by an order of magnitude. The text "~1.4" appears to be a typo or
was computed with a different (undisclosed) formulation. The actual ratio is
**13.4×**, meaning the pressure-based coupling estimate used in the paper
(§2.5, §4.1, all airborne displacement tables) overestimates displacement by
over an order of magnitude.

While this makes the airborne coupling even *weaker* than claimed
(strengthening the qualitative conclusion), it has three consequences:
1. The airborne displacement at 120 dB should be ~0.01 μm, not 0.14 μm.
2. The SPL needed to reach the PIEZO threshold rises from ~137 dB to ~157 dB.
3. The coupling ratio R increases from 10³–10⁴ to 10⁴–10⁵.

The paper must decide: use the energy-consistent displacement (correct but
requires explaining the reciprocity formulation) or the pressure-based
estimate (simpler but known to be 13× too high, requiring an explicit caveat).
Either way, Table 3 and all in-text displacement values need updating.

**Note on the physics:** The 13× discrepancy arises because the pressure-based
approach p_eff = p_inc × (ka)^n implicitly assumes the full radiation
efficiency, but the actual radiation damping ratio ζ_rad ≈ 10⁻¹⁵ is
negligible compared to structural damping ζ_struct = 0.15. The reciprocity
formula correctly accounts for this: the shell can only absorb as much energy
as it can re-radiate (times the damping partition ratio). This is textbook
Junger & Feit §9.3.

### M2. Theory/empirical mechanical coupling gap: still unaddressed

**Severity: Major (M2 from Round 2, unchanged)**

The paper presents ONLY the theoretical SDOF result (H_rel = Q = 3.33 at
resonance) for mechanical coupling. It does not mention that ISO 2631
transmissibility data give (T − 1) ≈ 0.89 at the same frequency, a factor of
3.75× lower. The `mechanical_coupling.py` code computes both, but the paper
ignores the empirical pathway entirely.

This is problematic because:
- The theoretical model predicts ξ_mech ≈ 7000–9000 μm at 1.15 m/s².
- The empirical ISO data predict ξ_mech ≈ 1900 μm.
- The paper only reports the theoretical value, which is an upper bound.

For a JSV paper, failing to compare your SDOF model against well-established
empirical transfer functions (Griffin 1990, Kitazaki & Griffin 1998) is a
significant omission. The 3.75× gap needs explanation: modal participation
factor, multi-DOF energy sharing, or explicit bounding.

**Fix:** Present both theoretical and empirical estimates. Explain the
discrepancy. Use the empirical value as the primary result and the theoretical
value as an upper bound. Alternatively, introduce an effective modal
participation factor η_n ≈ 0.24 and justify it.

### M3. Section 3 is 40% TODO placeholders

**Severity: Major (incomplete manuscript)**

Section 3 (Parametric Study) contains six subsection stubs that are entirely
`% TODO` comments:
- §3.6 Acoustic Cavity Modes
- §3.7 Coupled FSI Modes (including 4 sub-TODOs)
- §3.8 Parametric Study (3 sub-TODOs)
- §3.9 Harmonic Response (3 sub-TODOs)

These are not minor omissions—they include the coupled FSI analysis, the
harmonic response function, and the systematic parametric sensitivity study.
A JSV paper on modal analysis of a fluid-filled shell *must* include coupled
mode classification and frequency response functions. The partial results in
§3.1–§3.5 are insufficient.

**Fix:** Either complete these sections or remove the stubs and restructure
§3 to present only the completed parametric results. A half-empty section
signals an unfinished manuscript.

### M4. Boundary condition uncertainty still unresolved

**Severity: Major (M4 from Round 2, minimally improved)**

Section 3.4 states: "Partial constraints (spine, pelvis, ribs) raise the n=2
frequency by an estimated factor of 1.3–3.0×." This estimate is:
1. Uncited — no reference is provided for these multipliers.
2. Too imprecise — a factor of 3× uncertainty in the *primary result* is
   unacceptable for a quantitative paper.
3. Potentially too low — my Round 2 estimate of 2.5–4.0× for a hemisphere
   clamped at the equator was based on standard FEM benchmarks (Kang & Leissa
   2005, among others).

If the BC multiplier is 3.0×, then f₂ shifts from 3.9 Hz (or 4.4 Hz per the
paper's numbers) to 12–13 Hz, which is **outside** the ISO 2631 abdominal
resonance range. This doesn't invalidate the coupling-disparity argument, but
it weakens the claim that the model "explains" the ISO data.

**Fix:** The FEA validation mentioned in the R2 response is the right
approach. Until it's complete, the paper must:
(a) State explicitly that the free-shell model provides a *lower bound*.
(b) Cite specific references for the BC multiplier range.
(c) Show that the coupling ratio R ∝ 10³–10⁴ is robust to BC uncertainty
    (it should be, since both pathways see the same mode shift).

### M5. No formal uncertainty quantification

**Severity: Major (new)**

The paper presents point estimates throughout with no error bars, confidence
intervals, or sensitivity indices. For a model with at least 8 free parameters
(E, a, c, h, ν, ρ_w, ρ_f, P_iap, η), many of which span an order of
magnitude in physiological range, this is a critical omission.

At minimum, the paper needs:
1. A tornado chart or Morris/Sobol sensitivity analysis showing which
   parameters dominate the uncertainty in f₂ and in the coupling ratio R.
2. Propagated uncertainty bounds on the key claims: f₂ = X ± Y Hz,
   ξ_air = X ± Y μm, R = X ± Y.
3. Explicit statement of whether the coupling ratio R is robust to parameter
   uncertainty (the paper claims it is, §2.7, but never demonstrates it
   quantitatively).

The multi-parameter factorial in §3.2 (486 combinations) is a start but is
not presented as a formal UQ analysis — it lacks output distributions, it
doesn't compute sensitivity indices, and the 37%/41% hit-rate statistics are
not meaningful without knowing the input distribution.

---

## 5. Moderate Issues

### m1. Absorption cross-section formula presented without derivation

Section 4.4 introduces the reciprocity-based absorption cross-section:

$$\sigma_{abs} = \frac{(2n+1)\lambda^2}{4\pi} \frac{\Gamma_{rad}}{\Gamma_{total}}$$

and states ζ_rad ≈ 10⁻¹⁵. This is a critical step in the argument (it proves
the shell is "transparent" to airborne infrasound), but:
- No derivation or reference path from the shell model to this formula.
- The ζ_rad value is stated without showing the computation.
- The reader cannot verify this without running the code.

**Fix:** Add at minimum 2–3 lines of derivation showing how ζ_rad is computed
from the radiation resistance of mode n in the Rayleigh limit. Cite Junger &
Feit §9.3 or Morse & Ingard §8.2 explicitly for the cross-section formula.

### m2. Airborne coupling model assumes free-field plane wave

The $(ka)^n$ coupling formula assumes a plane wave incident on a free sphere.
In reality:
- The torso is not free-standing; it is typically adjacent to reflecting
  surfaces (floor, chair, walls).
- Clothing and the chest/back surfaces modify the local pressure field.
- At infrasonic frequencies, room modes and standing waves create pressure
  fields that are not well-approximated by plane waves.
- The person's body is not spherical — the oblate geometry modifies the
  scattering coefficients.

The $(ka)^n$ scaling is robust (it's a consequence of the multipole expansion
order), but the numerical prefactors could differ by factors of 2–5 from the
idealized sphere case. This should be discussed as a limitation.

### m3. The gas pocket mechanism (§5.3) is underdeveloped

The discussion introduces bowel gas resonance as a "potentially" important
alternative mechanism, but the quantitative analysis exists only in
`gas_pocket_resonance.py` and is not presented in the paper. The code shows
that Minnaert frequencies for physiological gas pockets (30–330 Hz) are far
above the infrasonic range, and sub-resonant displacements are small.

Either:
(a) Develop this into a proper subsection with quantitative results, or
(b) Remove it from the discussion, or
(c) Relegate it to a single sentence noting it as future work.

Currently it reads as speculation in a paper that otherwise aims for
quantitative rigor.

### m4. Duplicate bibliography entries

`references.bib` contains two entries for Junger & Feit:
- `Junger1986` (year: 1986, edition: 2nd, publisher: MIT Press)
- `junger2012sound` (year: 1993, edition: 2nd, publisher: MIT Press)

These appear to be the same book with inconsistent metadata. The `lamb1882`
entry has the wrong `@book` type — Lamb 1882 is a journal article
(Proc. London Math. Soc.), not a book. These errors will confuse readers
attempting to find the references.

### m5. The "PIEZO?" column in Tables 3–4 is misleading

The binary yes/no PIEZO threshold comparison implies a sharp activation
boundary at 0.5–2.0 μm. In reality, PIEZO1/2 channel activation is
probabilistic and depends on strain rate, membrane tension, and cell type
(Coste et al. 2010 describe the channels but do not provide a universal
displacement threshold for tissue-level activation). The paper should clarify
that this is an order-of-magnitude comparison, not a precise threshold.

### m6. The multi-layer wall model result contradicts the baseline

Section 3.3 finds E_eff ≈ 0.075 MPa for the composite wall, but the baseline
model uses E = 0.1 MPa. The paper doesn't explain why the baseline isn't
set to the composite value. If the laminate analysis is correct, the baseline
should be 0.075 MPa (giving even lower frequencies), or the discrepancy
should be explained.

---

## 6. Minor Issues

### Style and presentation:
1. Abstract line 6: "approximately 2900 Hz" — code gives 2435–2472 Hz with
   the stated parameters. Must be corrected (see F1).
2. §2.3, Eq. (6): the paper says k_fluid = 4.2 × 10¹⁰ Pa/m with R=0.157 m.
   Actual: 3K_f/R = 3×2.2e9/0.157 = 4.20×10¹⁰. This is correct, but the R
   value used to compute k_shell (which says ~2.4×10⁵) should be verified
   against the stated parameters.
3. §3.3 says "approximately five distinct tissue layers" then lists six.
4. The Conclusion's "half-correct" framing (§6: "The brown note hypothesis is
   thus physically grounded") may be seen as editorializing for a JSV paper.
   Consider more neutral language.
5. Author metadata: "jon@example.com" and "City, Country" are placeholder
   values.
6. No figure is included anywhere in the manuscript. A JSV paper of this scope
   typically requires 4–8 figures (mode shapes, frequency response, parametric
   sensitivity, coupling comparison).

---

## 7. What's Missing (vs. JSV expectations)

1. **Figures.** Zero figures in the entire manuscript. At minimum:
   - Mode shape visualization (n=0, 2, 3, 4)
   - Frequency response function showing airborne vs mechanical pathways
   - Parametric sensitivity (tornado chart or contour plot)
   - Coupling ratio as a function of frequency and SPL
2. **Coupled FSI mode table.** The paper derives uncoupled shell modes with
   added mass, but never presents the full coupled fluid-structural eigenvalue
   problem. For JSV, this is expected.
3. **Comparison with published FE models.** Several groups have published FE
   models of torso vibration (Kitazaki & Griffin 1998, Fritz et al. 2009,
   Zhong et al. 2019). The paper should compare its analytical predictions
   against at least one FE benchmark.
4. **Frequency-dependent material properties.** The paper uses constant E and η
   across all frequencies, but soft tissue is well-known to exhibit frequency-
   dependent viscoelasticity (E increasing with frequency, η decreasing).
   At minimum, cite the frequency range over which the constant-property
   assumption is valid.
5. **Convergence / verification.** No mesh convergence (for future FEA), no
   truncation error analysis for the spherical harmonic expansion, no
   comparison of the equivalent-sphere approximation error against an oblate
   spheroidal solution.
6. **Reproducibility statement.** The code exists but is not referenced in the
   paper. For JSV, a data availability / code availability statement is
   expected.

---

## 8. Specific Recommendations

### Immediate (before next review):

1. **Fix F1.** Establish one canonical parameter set. Recompute every number
   in the paper from a single script. Verify each table entry matches the
   code output. This is the single most important action.

2. **Resolve the energy budget.** Choose either the pressure-based or
   energy-consistent approach. If pressure-based, state explicitly that it
   overestimates by ~13× and explain why. If energy-consistent, update all
   displacement tables. The 13× vs "~1.4×" discrepancy in the code comments
   must be corrected regardless.

3. **Address the theory/empirical gap (M2).** Add a paragraph to §4.2 or §5
   comparing the SDOF prediction against ISO transmissibility data. Present
   both estimates. The code already computes both — this is a writing task.

4. **Complete or prune Section 3.** Remove all TODO stubs. If the coupled FSI
   and harmonic response analyses aren't ready, restructure §3 to present
   only the parametric sensitivity that exists.

5. **Add at least 3 figures.** Even schematic mode shapes, an airborne vs
   mechanical displacement comparison plot, and a parametric sensitivity
   chart would substantially improve the paper.

### Medium-term (before submission):

6. **FEA validation of boundary conditions.** Even a single hemisphere-clamped
   FE model would resolve M4 and dramatically strengthen the paper.

7. **Formal uncertainty propagation.** Monte Carlo or polynomial chaos over
   the physiological parameter ranges, producing distributions for f₂ and R.

8. **Literature comparison.** Add a table comparing your f₂ predictions
   against published biomechanical models and experimental measurements.

---

## 9. Priority Ranking (by impact on publishability)

| Rank | Issue | Impact | Effort |
|------|-------|--------|--------|
| 1 | F1: Parameter mismatch | **Blocks everything** | Low (1 day) |
| 2 | M3: Section 3 TODOs | **Incomplete manuscript** | Medium (1 week) |
| 3 | M1: Energy budget 13× | **Quantitative credibility** | Low (2 days) |
| 4 | M5: No UQ | **JSV requirement** | Medium (1 week) |
| 5 | M2: Theory/empirical gap | **Omission of known data** | Low (2 days) |
| 6 | M4: BC uncertainty | **Core model limitation** | High (2+ weeks) |
| 7 | No figures | **Below JSV standard** | Medium (1 week) |
| 8 | m1–m6 moderate issues | **Polish** | Low–medium |

---

## Summary

The paper tells the right story and the qualitative physics is correct. The
coupling-disparity argument is novel and valuable. But the manuscript is not
yet at JSV standard due to: (1) a pervasive parameter mismatch that makes
every number wrong, (2) an unresolved order-of-magnitude inconsistency in the
energy budget, (3) incomplete sections, and (4) missing uncertainty
quantification. Items 1–3 are straightforward to fix; item 4 requires more
substantive work.

**Recommendation: MAJOR REVISION.** Fix F1 and M1–M3 first; the rest can
follow. The paper is within reach of publication if these issues are addressed
systematically.
