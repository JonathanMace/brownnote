# Reviewer A ΓÇö Round 5

**Date:** 2025-07-15
**Reviewer:** A (Structural Acoustics / Vibroacoustics, 20+ years, JSV editorial board)
**Manuscript:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the Brown Note"
**Target journal:** Journal of Sound and Vibration

---

## Overall Assessment

The authors have responded comprehensively and thoughtfully to the Round 4 comments. The paper is now substantially stronger than the version I previously reviewed. The narrative leads with the coupling disparity rather than the folklore debunking; the historical context (Gavreau, von Gierke, Tandy, Leventhall) is woven into the Introduction; the Discussion now contains a rich broader-applications section (┬º5.5) connecting to blast injury, marine bioacoustics, HIFU, and obstetric ultrasonography; the 8 previously-missing references have been incorporated; and the abstract has been tightened to 166 words without losing any essential content. The parameter consistency issues flagged in Round 4 (Table 1 vs. code defaults) appear resolved ΓÇö the canonical set (E = 0.1 MPa, h = 10 mm, ╬╜ = 0.45, ╬╖ = 0.25) is now used consistently, and the breathing mode frequency is consistently stated as ~2500 Hz throughout.

This is a paper that JSV readers will download, read to the end, and cite. The physics is clean, the framework is portable, and the writing remains some of the most engaging I have encountered in a structural acoustics manuscript. One genuine quantitative inconsistency remains (the headline coupling ratio), alongside a handful of minor editorial points. I recommend **acceptance conditional on minor corrections** that can be verified editorially without re-review.

**Recommendation: ACCEPT (subject to minor corrections)**

---

## Significance and Novelty

The significance case is now convincingly made. I want to highlight what the authors have achieved, because it is easy to miss behind the colourful subject matter:

1. **The coupling-disparity framework is genuinely new.** No prior work has placed airborne acoustic and mechanical vibration coupling to a soft biological cavity within a single energy-consistent framework and derived a dimensionless ratio. This is a portable methodological contribution. Section 5.5 now makes this explicit with concrete application sketches (blast overpressure, swim bladder acoustics, HIFU targeting, fetal exposure), which substantially increases the paper's citability beyond the infrasound niche.

2. **The mode taxonomy insight is underappreciated.** The five-order-of-magnitude separation between k_fluid and k_shell (below Eq. 6) means the breathing/flexural mode split is vastly wider for the abdomen than for any engineering shell. The authors state this clearly and it is one of the paper's most pedagogically valuable observations.

3. **The gas pocket transducer mechanism (┬º5.3.1) is a genuine discovery.** The observation that intestinal gas pockets bypass the (ka)^n penalty because they respond to the full incident pressure locally is novel, testable, and explains inter-individual variability in infrasound sensitivity. This will generate follow-up work.

The paper will be cited by: (a) the ISO 2631 / occupational WBV community, (b) infrasound health effects researchers, (c) blast injury biomechanics groups, (d) anyone modelling acoustic coupling to biological cavities, and (e) science communicators debunking acoustic weapon claims. That is a broad and durable citation base.

---

## What Has Been Addressed Since Round 4

For the record, here is my assessment of how each Round 4 major suggestion was handled:

| Round 4 Item | Status | Comment |
|---|---|---|
| MS1: Reframe title/abstract | **Addressed** | Abstract now opens with the coupling disparity. Title retained ΓÇö I now find the current title acceptable; the main clause describes the physics ("Modal Analysis of a Fluid-Filled...") and the subtitle provides the motivating hook. This will maximise downloads. |
| MS2: Promote energy-consistent analysis | **Addressed** | Table 3 now presents both pressure and energy-consistent estimates, with the energy column clearly flagged. The 10^{-14} absorption efficiency is highlighted in ┬º4.4. |
| MS3: Broader applications section | **Addressed thoroughly** | ┬º5.5 provides half a page on blast injury, marine bioacoustics, HIFU/lithotripsy, and obstetric ultrasound, with 8 new references. This is exactly what I requested. |
| MS4: Oblate Ritz correction integration | **Partially addressed** | Table 5 and ┬º3.6 present the correction clearly, noting it moves fΓéé from 4.0 to 3.6 Hz. The paper still uses sphere-based values as canonical throughout. This is acceptable because the coupling ratio is independent of this correction (both pathways excite the same mode), but see Minor Issue 3 below. |
| MS5: Parameter consistency | **Addressed** | All in-text values now match Table 1 canonical set. Breathing mode consistently ~2500 Hz. |
| ms1: Historical notes in Introduction | **Addressed** | Gavreau, von Gierke, Mohr et al., Tandy & Lawrence all incorporated into ┬º1. |
| ms8: Q/╬╖ inconsistency | **Addressed** | ╬╖ = 0.25, Q = 4.0 throughout. |
| Missing references | **Addressed** | Stuhmiller, Owers, Mayorga (blast); Feuillade, Love, Southall (marine); ter Haar, Bailey, Duck (ultrasound/obstetric); Gavreau, Ishitake, Seidel, von Gierke & Brammer, Heil all added. |

---

## Fatal Flaws

None.

---

## Major Issues

None that would require re-review. One quantitative inconsistency that must be corrected editorially:

### 1. Reconcile the headline coupling ratio across the manuscript

The "coupling ratio" R = ╬╛_mech / ╬╛_air is the paper's signature number, but it appears with three different values:

- **Abstract** (line 105), **Introduction** (line 76 of introduction.tex), **Conclusion** (line 5): R Γëê 4.6 ├ù 10Γü┤
- **Eq. 26 in ┬º4.3** (section4_coupling.tex line 89): R = 917/0.014 Γëê 6.6 ├ù 10Γü┤
- **Fig. 5a annotation**: 22,044├ù
- **Monte Carlo 90% CI** (Table 4 in results.tex): median 10Γü┤, range [10┬│, 10Γü┤]
- **Discussion ┬º5.1, ┬º5.4, ┬º5.6**: 10┬│ΓÇô10Γü┤
- **Cover letter**: 46,000├ù
- **Conclusion line 35**: 10┬│ΓÇô10Γü╡

The discrepancies arise from different WBV reference levels (0.1 vs 0.5 vs 1.15 m/s┬▓) and different airborne estimates (energy-consistent vs pressure-based), but this is not made explicit. The reader encounters "4.6 ├ù 10Γü┤" in the abstract, then "6.6 ├ù 10Γü┤" in Eq. 26, and has no way to reconcile them without recalculating.

**Fix:** Pick one canonical comparison point (I suggest 0.5 m/s┬▓ WBV at 120 dB SPL, energy-consistent airborne ΓÇö the occupationally relevant comparison) and state the ratio unambiguously. Then define the Monte Carlo range as the uncertainty band around that point. The figure annotation should match the text, or a caption note should explain the different comparison level. The ranges "10┬│ΓÇô10Γü┤" and "10┬│ΓÇô10Γü╡" in different locations also need reconciliation ΓÇö is the upper bound 10Γü┤ or 10Γü╡?

---

## Minor Issues

### 1. Cover letter title does not match manuscript title

The cover letter opening reads "Can Infrasound Induce Abdominal Resonance? Modal Analysis of..." while the manuscript title is "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the Brown Note." These must match before submission.

### 2. The n = 1 mode is never discussed

The formulation jumps from n = 0 (breathing, ┬º2.2) to n ΓëÑ 2 (flexural, ┬º2.3) without mentioning n = 1. In Lamb's classification, n = 1 is a rigid-body translation of the fluid-filled sphere ΓÇö it has zero frequency for a free shell because it involves no deformation. A single sentence in ┬º2.3 ("The n = 1 mode corresponds to rigid-body translation and has zero natural frequency for a free shell; it is therefore excluded") would close this gap and prevent a sharp reviewer from wondering whether it was overlooked.

### 3. Sphere vs. oblate canonical values

While I accept the decision to use sphere-based canonical values throughout, a parenthetical reminder when the headline numbers appear would help: e.g., in the abstract or conclusion, "(fΓéé Γëê 4.0 Hz for the equivalent sphere; oblate correction gives Γëê 3.6 Hz, ┬º3.6)." This costs one clause and prevents the reader from thinking the oblate analysis in ┬º3.6 was ignored.

### 4. Frequency-dependent viscoelasticity not acknowledged in main text

The KelvinΓÇôVoigt model (Eq. 2) assumes frequency-independent ╬╖. Real soft tissue exhibits power-law or fractional-order viscoelasticity (see, e.g., Szabo & Wu 2000, JASA 107:2437). The supplementary material discusses this (line 700), but the main text should include a single sentence below Eq. 2 noting that constant ╬╖ is a low-frequency approximation valid over the narrow infrasonic band of interest. This pre-empts a standard reviewer objection.

### 5. Figure 5(b) bar labels vs. Table 6

Figure 5(b) shows WBV displacement as 3115 ╬╝m and whole-cavity airborne as 0.14 ╬╝m, giving a ratio of ~22,000. But Table 4 at 0.1 m/s┬▓ gives ╬╛_rel = 917 ╬╝m, and at 0.5 m/s┬▓ gives 4586 ╬╝m. Neither matches 3115. The figure appears to use an intermediate WBV level or different parameters. A caption note specifying the exact comparison conditions (acceleration level, SPL, whether energy-consistent or pressure-based) would resolve this.

### 6. Duplicate bibliography entries for Junger & Feit

The reference list contains both Junger1986 and junger2012sound, which are the same book (2nd edition, MIT Press). The year differs (1986 vs. 1993) ΓÇö neither is correct for a "2012" key. The entry junger2012sound has year 1993 which is the ASA reprint; Junger1986 has year 1986 which is the original MIT Press edition. These should be consolidated into a single entry with the correct year.

### 7. Minor typographic issues

- Table 6 caption: "at SI{120}{decibel} SPL, SI{7}{hertz}" ΓÇö verify these render correctly in the compiled PDF.
- ┬º4.2 (section4_coupling.tex line 53): "does not knock politely at the acoustic impedance doorΓÇöit kicks it open" ΓÇö wonderful prose, but the em-dash rendering should be checked (three hyphens vs. LaTeX ---).
- Conclusion final paragraph: "finite element analysis" should be "finite-element analysis" (compound adjective) for consistency with JSV style.

### 8. Sobol index figure uses tan ╬┤ notation

Figure 4 (Sobol indices) labels the loss tangent axis as "tan ╬┤" while the text and Table 1 use ╬╖ throughout. These should match.

---

## Missing References or Comparisons

The reference list is now substantially complete. Two remaining gaps, neither critical:

1. **Szabo & Wu (2000)**, "A model for longitudinal and shear wave propagation in viscoelastic media," JASA 107:2437 ΓÇö for justifying the constant-╬╖ approximation (see Minor Issue 4).

2. **Kang & Leissa (2005)**, "Free vibration analysis of complete paraboloidal shells of revolution with variable thickness," JSV 282:1049 ΓÇö relevant to the boundary condition analysis in ┬º3.5 / ┬º5.4 item 3, and would connect the paper to JSV's own literature on shells with partial constraints.

Neither is essential for acceptance.

---

## What I Liked

1. **The energy budget figure (Fig. S? / data figures)** is outstanding. The cascade from incident power (3.7 ├ù 10Γü╗┬▓ W) through impedance reflection, (ka)Γü┤ scattering loss, modal coupling, to absorbed power (1.1 ├ù 10Γü╗┬╣┬╣ W) tells the entire story of acoustic invisibility in a single image. If this is not already in the main text, it should be ΓÇö it is the single most convincing visualization of the paper's central argument. I note it exists in the figure set as ig_energy_budget.pdf. If space permits, I would promote this to the main text.

2. **The Discussion (┬º5) is now among the strongest I have seen in a JSV submission.** The treatment of alternative pathways (┬º5.3), the nonlinear amplitude analysis (┬º5.4), the broader applications (┬º5.5), the experimental validation proposal (┬º5.6), and the honest 9-point limitations enumeration (┬º5.5) are all individually strong; together they transform the paper from a theoretical exercise into a research programme.

3. **The experimental validation section (┬º5.6)** is unusually concrete and actionable. Specifying phantom materials (Ecoflex 00-30 to Dragon Skin 10A), predicted frequencies for each formulation, instrumentation (Polytec PSV-500), sample sizes (n = 15, power = 0.80), and cost estimates (< US,100) lowers the barrier for any experimentalist who reads this paper and wants to test it. This is how theoretical papers should end.

4. **The writing remains exceptional.** "One part in a hundred trillion of the incident acoustic energy ΓÇö a figure that puts the brown note hypothesis on rather thin thermodynamic ice." "One could double the elastic modulus, halve the wall thickness, or relocate the subject to Jupiter, and the ratio would scarcely budge." The voice is confident, precise, and funny without ever becoming flippant. The wit serves the physics, not the reverse. Preserve this in the final version.

5. **The broader applications section (┬º5.5)** is exactly what I asked for and more than I expected. The blast injury application ΓÇö noting that blast frequencies place ka near unity, removing the geometric penalty that suppresses infrasonic coupling ΓÇö is genuinely insightful and directly useful to the blast biomechanics community. The swim bladder and HIFU discussions are well-targeted. The observation that the coupling-comparison methodology, rather than the brown-note conclusion, is the transferable contribution (┬º5.5, final paragraph) shows excellent self-awareness.

6. **Figure quality.** All figures examined are publication-ready. The geometry schematic (Fig. 1) clearly shows both excitation pathways with labeled dimensions. The mode shapes (Fig. 2) are clean and pedagogically effective. The coupling comparison (Fig. 5) uses log scales appropriately and the PIEZO threshold line provides immediate visual context. The Sobol indices (Fig. 4) are clear. The frequency vs. E figure (Fig. 3) with the ISO 2631 band overlay and relaxed/tensed annotations tells the parametric story at a glance.

---

## Summary Recommendation: ACCEPT (subject to minor corrections)

The paper has matured into a genuinely strong contribution to JSV. The coupling-disparity framework is novel, physically transparent, and portable to problems of considerably greater practical consequence than its motivating example. The analysis is thorough (modal decomposition, energy-consistent reciprocity, Monte Carlo UQ, nonlinear perturbation, oblate Ritz correction, boundary condition sensitivity, multi-layer wall model, gas pocket mechanism). The Discussion is exemplary. The writing is a pleasure.

The one issue requiring correction before publication is the inconsistency in the headline coupling ratio (Major Issue 1). This is a bookkeeping error, not a physics error ΓÇö the underlying calculations appear correct, but the same quantity is reported at different comparison points without making this explicit. Reconciling the numbers is a 30-minute task.

With that correction and the minor editorial items above, this paper is ready for publication. I look forward to seeing it in print and to citing it in my own work on fluid-loaded shell dynamics.

---

*Reviewer A, Round 5*
*Associate Editor, Journal of Sound and Vibration*
