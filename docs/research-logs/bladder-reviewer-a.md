# Reviewer A — Bladder Resonance Manuscript, Round 1

**Paper**: *Resonant Frequencies of the Human Urinary Bladder: A Fluid-Filled Viscoelastic Shell Model*
**Date**: 2026-03-27
**Reviewer**: Reviewer A (domain expert, structural acoustics / vibroacoustics)
**Target journal**: Journal of Sound and Vibration

---

## Overall Assessment

This is a concise, well-structured companion paper to the brown note manuscript
(Paper 1), applying the same oblate spheroidal shell framework to a smaller,
clinically relevant organ. The paper makes a clear prediction (bladder n=2 at
12–18 Hz, minimum ~12 Hz near 170 mL), identifies a physically intuitive
non-monotonic frequency–volume relationship, and quantifies the mechanical-to-
airborne coupling disparity (~7,600×). The narrative is logical and the writing
is clean for a first draft.

However, the manuscript in its current form reads more like a **technical note
or application appendix** to Paper 1 than a standalone journal article. The
novelty over Paper 1 is incremental (same equations, different parameters),
the clinical implications are gestured at but never quantified, and the paper
lacks the experimental/numerical validation or the deeper analytical insight
that would make it compelling as an independent contribution. The good news:
with targeted additions, this could become a genuinely useful paper for both
the JSV and clinical readerships.

**Summary recommendation: MAJOR REVISION** — not because of fatal errors, but
because the paper needs more substance to stand on its own.

---

## Significance and Novelty

### What is genuinely new here

1. **Fill-volume-dependent parametric analysis.** Paper 1 treated the abdomen
   at a single geometry. Here, the key parameters (R, h, E, P) all co-vary
   with a single physiological variable (fill volume), producing a non-trivial
   U-shaped frequency curve. The *minimum* at ~170 mL is a genuinely
   interesting and potentially testable prediction. This is the paper's
   strongest novel contribution.

2. **Clinical bridge.** Connecting an analytical shell model to occupational
   WBV symptomatology (vibration-induced urgency) gives the JSV readership
   a rare window into biomechanical relevance. This is undersold.

3. **The coupling ratio at a different organ scale.** Showing that the ~10⁴×
   mechanical advantage is robust across organ sizes (abdomen vs bladder)
   strengthens the general conclusion from Paper 1.

### What is NOT new

- The shell equations (§2.3–2.6) are identical to Paper 1. The breathing mode
  analysis (Eq. 6), flexural mode equations (Eqs. 8–13), airborne coupling
  (Eqs. 14–16), and mechanical coupling (Eqs. 17–20) are literally the same
  formulae with different parameter values substituted.
- The coupling analysis framework (seat→pelvis→bladder SDOF chain) is
  unchanged.

### Concern about "salami slicing"

An editor will ask: *why isn't this a section within Paper 1?* The authors
must pre-empt this question by articulating what the bladder analysis reveals
that the abdominal analysis could not. I suggest the answer is the
**fill-dependent parametric physics** and the **clinical connection to a
specific symptom** (urgency). Both need to be significantly deepened.

---

## Major Suggestions (would substantially improve the paper)

### M1. Deepen the parametric analysis — it's the core contribution

The U-shaped f₂(V) curve is the paper's headline result, but it's presented
descriptively. I want to see:

- **Analytical decomposition.** Derive the condition ∂f₂/∂V = 0 explicitly.
  Which term crosses over — bending, membrane, or pre-stress? At what volume
  does each stiffness contribution dominate? A figure showing K_bend, K_memb,
  K_P, and m_eff as functions of V (overlaid) would be far more insightful
  than the current four-panel Figure 1.
- **Sensitivity analysis.** How robust is the 170 mL minimum? Vary E_min,
  E_max, η, and the tissue-volume assumption ±20% and show how the minimum
  shifts. This is important because the material parameters have large
  uncertainties, and clinicians will want to know if the minimum is "real" or
  an artefact of the particular E(V) interpolation chosen.
- **Dimensional analysis.** Can you identify a non-dimensional group that
  controls whether the frequency is in the ascending vs descending branch?
  Something like a "strain-stiffening Cauchy number" would be publishable in
  its own right.

### M2. The clinical story needs teeth

Section 4.1 (Clinical Implications) is the most important section for impact
and citation, yet it's the weakest. Currently it describes two regimes
(sub-resonant forced response and near-resonant amplification) and then waves
at stretch receptors. Concrete improvements:

- **Quantify wall displacement.** Given a typical WBV acceleration of
  0.5 m/s² RMS (ISO 2631 action value), compute the resulting bladder wall
  displacement amplitude at 5 Hz (sub-resonant, peak pelvic transmissibility)
  and at f₂ (resonant). Are these microns? Tens of microns? This is the
  number clinicians need.
- **Compare to stretch receptor thresholds.** Piezo1/Piezo2 channels activate
  at membrane tensions of ~1–10 mN/m (Coste et al. 2010, which you cite).
  Can you estimate whether the predicted wall strain reaches this threshold?
  Even an order-of-magnitude comparison would be enormously valuable.
- **Cite the urgency volume literature.** The "first desire to void" typically
  occurs at 150–250 mL (Abrams et al., ICS standardisation reports). Your
  minimum f₂ at 170 mL coincides with this range. Is that a coincidence? If
  not, you have a mechanistic hypothesis for urgency onset. This deserves a
  dedicated paragraph and possibly a figure.

### M3. Address the pelvic boundary condition more seriously

The Limitations section (§4.5, "Pelvic constraint") correctly identifies
that ~40% of the bladder contacts the pelvic bone. But this is not a minor
correction — it fundamentally changes the mode shapes and could shift f₂ by
a factor of 2 or more. At minimum:

- Estimate the effect analytically. A partial rigid boundary on a spherical
  shell is a well-studied problem (e.g., cap-constrained sphere). Even a
  scaling argument would help.
- Consider that the constraint could **lower** the effective frequency (by
  reducing the free vibrating area, hence increasing the effective n) or
  **raise** it (by adding boundary stiffness). Which is it? The reader
  deserves more than "this is not captured."
- This is also the natural place to discuss **anisotropy** of the detrusor
  muscle (three smooth muscle layers with different fibre orientations),
  which would affect the effective bending stiffness.

### M4. Add a sensitivity/uncertainty table

The model has ~10 input parameters, several of which span an order of
magnitude in the literature (E: 10–800 kPa; h: 1.5–5 mm; η: 0.3–0.5).
A tornado chart or a table showing ∂f₂/∂(parameter) for each input would
immediately tell the reader which parameters matter and where future
experimental effort should focus. This is standard practice in analytical
modelling papers and its absence is conspicuous.

### M5. Venue question — is JSV the right target?

I raise this constructively, not dismissively. The analytical framework is
identical to Paper 1 (already targeted at JSV). The new content — fill-
dependent biomechanics, urgency prediction, clinical coupling — may
resonate more strongly with:

- **Journal of Biomechanics** (biomechanical modelling community)
- **Neurourology and Urodynamics** (clinical urodynamics community)
- **International Journal of Industrial Ergonomics** (occupational health)

If the authors stay with JSV, they need to make the structural acoustics
contribution more prominent: the parametric shell analysis, the dimensional
analysis, the physics of competing stiffening mechanisms. If the story is
primarily "here's why WBV causes urgency," a clinical/biomechanics venue
would give it a much larger audience.

---

## Minor Suggestions

### m1. Abstract: the "sub-resonant response mechanism" conclusion is burying the lede

The abstract ends by saying f₂ is above the ISO 2631 band, "suggesting a
forced sub-resonant response mechanism rather than direct resonance." This is
actually the paper's most interesting nuanced finding — the bladder does
**not** resonate at the dominant WBV frequencies, yet symptoms occur anyway.
Reframe this positively: "The mismatch between bladder resonance and peak
WBV exposure implies that vibration-induced urgency arises from forced
sub-resonant loading amplified by pelvic transmissibility, not from direct
resonance."

### m2. Figure 1 (freq vs volume) needs work for publication quality

- Panel (a): The legend says "n = 2 (oblate-prolate)" — this is the mode
  shape name for a spheroidal shell, not a spherical one. For a sphere, just
  say "n = 2 quadrupole."
- Panel (b): Dual y-axes with different colours are hard to read. Consider
  normalising both to their initial values on a single axis.
- Panel (c): Log-scale E plot is fine, but add the Nenadic et al. and Barnes
  data points as discrete markers so the reader can see how the interpolation
  fits the data.
- Panel (d): The cmH₂O conversion uses division by 98.0665 in the code —
  should be documented or use siunitx consistently.
- All panels: remove the bold suptitle "Bladder Resonant Frequency vs Fill
  Volume" — the caption provides this context. For a journal figure, titles
  should be in the caption, not on the figure.
- Consider vector graphics (PDF/EPS) rather than PNG at 150 dpi. JSV requires
  300+ dpi for raster graphics.

### m3. Figure 2 (coupling) — clarify "effective coupling (normalised)"

The y-axis of panel (a) says "Effective Coupling (normalised)" but normalised
to what? The airborne curve is (ka)², which is dimensionless. The mechanical
curve is T×H, also dimensionless. But they represent different physical
quantities (pressure coupling efficiency vs displacement transfer function).
Explain why the comparison is valid — what is the common physical quantity
being compared?

### m4. Eq. (5): log-linear interpolation should be called "log-linear" not "exponential"

The text says "exponential strain-stiffening" (§3.1, item 2) but Eq. (5) is
a power-law interpolation between two endpoints, not a true exponential. The
distinction matters because the Fung model (which you cite) uses an actual
exponential constitutive law. Clarify.

### m5. Table 2: the comparison with the abdomen is useful but incomplete

Add columns for: (a) the coupling ratio at the *pelvic resonance peak* (not
just at f₂), since that's where most occupational exposure energy sits; and
(b) the predicted wall displacement per unit input acceleration.

### m6. The n=1 mode exclusion (end of §2.4) needs a sentence about the physical constraint

You note that n=1 is rigid-body translation with zero frequency for a free
shell. But the bladder is NOT free — it's tethered by ureters, urethra, and
pelvic ligaments. This means n=1 would have a nonzero frequency (a "rocking
mode") that could be clinically relevant. Acknowledge this.

### m7. Poisson's ratio and near-incompressibility

You use ν = 0.49. Note that for truly incompressible materials (ν → 0.5),
the membrane stiffness Eh/(1-ν²) diverges, and thin shell theory can
become ill-conditioned. Comment on whether ν = 0.49 vs 0.499 matters for
your results.

### m8. Section structure

The paper has no "Methods" section separate from "Theory." For a companion
paper, consider renaming §2 to "Model and Methods" and adding a brief
subsection on the computational workflow (the Python code, the parametric
sweep, how figures were generated). This enhances reproducibility.

---

## Missing References or Comparisons

1. **Abrams et al. (2002)**, "The standardisation of terminology of lower
   urinary tract function" (Neurourology & Urodynamics). The ICS standard
   reference for cystometric capacity, first desire to void volumes, etc.
   Essential for connecting your minimum-frequency volume to clinical milestones.

2. **Torkamani et al. (2012)** or similar work on FE modelling of the bladder.
   There is a small but active literature on bladder FE models for urodynamics
   simulation. Citing it would show you're aware of the computational community
   and that your analytical model complements their numerical work.

3. **Sandhu et al. (2006)** or related work on vibration effects on the lower
   urinary tract — there are a few small clinical studies. These would
   strengthen §4.1.

4. **Leissa (1973)**, *Vibration of Shells* — the canonical reference for
   shell vibration, and specifically for partially constrained spherical shells
   (relevant to your pelvic boundary limitation).

5. **Love (1927)**, *A Treatise on the Mathematical Theory of Elasticity* —
   for the Love–Kirchhoff hypothesis you invoke in §2.1.

6. **Dijk et al. (2008)** or **Fritz (2012)** on swim bladder resonance in
   fish — the most developed literature on biological fluid-filled shell
   resonance. You cite it in Paper 1's discussion; it deserves mention here
   too as a cross-species validation of the general framework.

7. **Kitazaki & Griffin (1998)** is cited but only for "resonance behaviour of
   the seated human body." The specific data you extract (f_pelvis = 5.5 Hz,
   ζ = 0.25) should be attributed more precisely — is this from Kitazaki &
   Griffin or from Mansfield (2005)? Check the provenance.

---

## What I Liked

1. **The fill-volume minimum is a genuine prediction.** The U-shaped f₂(V)
   curve, with its physical explanation as a competition between geometric
   softening and strain-stiffening, is elegant and testable. This is the
   kind of result that gets remembered.

2. **The comparison table (Table 3) is well-conceived.** Placing the bladder
   and abdomen side-by-side makes the case for framework generality. The near-
   identical ka values (~0.01) despite very different organ sizes is a nice
   observation.

3. **The therapeutic WBV discussion (§4.3) is a shrewd addition.** Connecting
   to the rehabilitation literature broadens the potential readership and
   citation base considerably.

4. **Limitations section is honest and specific.** Five clearly stated
   limitations with physical reasoning — this is how limitations should be
   written.

5. **The writing is clear and well-paced** for a first draft. The introduction
   efficiently motivates the work, and the theory section is self-contained.

6. **Highlight #4 is clever marketing.** "Same analytical framework as
   abdominal cavity model" explicitly invites readers of Paper 1 to read
   Paper 2, and vice versa.

---

## Fatal Flaws

None identified. The physics is plausible, the numbers are in sensible ranges,
and the framework is sound. The issues are with depth, not correctness.

---

## Summary Recommendation: MAJOR REVISION

The manuscript has a solid foundation but needs significant additions to
justify standalone publication. The core requirements are:

1. **Analytical decomposition** of the frequency minimum (M1)
2. **Quantitative clinical predictions** — wall displacement, strain
   comparison to receptor thresholds (M2)
3. **Sensitivity analysis** showing robustness of key predictions (M4)
4. **Serious discussion** of the pelvic boundary constraint (M3)
5. **Venue decision** with narrative adjusted accordingly (M5)

With these additions, the paper would be a valuable contribution to
whichever journal is selected. Without them, it risks being seen as an
appendix to Paper 1.

---

*Reviewer A — Senior researcher, structural acoustics and vibroacoustics*
*20+ years JSV editorial experience*
