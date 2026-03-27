# Reviewer A — Round 1 (Paper 3: Scaling Laws)

**Paper:** "Scaling Laws for the Flexural Resonance of Fluid-Filled Viscoelastic Shells: From Rats to Humans"
**Target:** JSV Short Communication (~8 pages)
**Reviewer:** A (significance, novelty, narrative, broader impact)
**Date:** 2026-03-28

---

## Overall Assessment

This Short Communication applies Buckingham Pi dimensional analysis to the fluid-filled oblate spheroidal shell model developed in the companion paper (Paper 1) to derive scaling laws for flexural resonance. The central result—that 11 physical parameters reduce to 5 governing dimensionless groups for flexural modes—is correct, elegant, and practically useful. The cross-species predictions and the breathing-mode impossibility argument are genuinely valuable contributions.

However, the paper undersells itself in several ways, and there are structural and framing issues that, if addressed, would significantly increase its impact and citability. The main concern is that the paper reads as "we applied a textbook technique to our own model," when it should read as "we discovered universal scaling behaviour with immediate experimental consequences." The physics is sound; the storytelling needs sharpening.

---

## Significance and Novelty

### What is genuinely new

1. **The identification that $\Pi_0 \approx 0.065$–$0.072$ is quasi-constant across mammals.** This is a non-trivial result. It means mammalian abdominal cavities are approximately geometrically and materially similar in the dimensionless sense—a statement that has implications well beyond this specific model.

2. **The size-independence of $\mathcal{R}$.** The factor-of-two variation across a 6× range of body size is a powerful result. It provides the theoretical justification for using animal models, which experimentalists have been doing without rigorous foundation.

3. **The breathing-mode impossibility result.** The 410-metre radius calculation is memorable and conclusive. It closes an entire line of inquiry.

### What is less novel

The application of Buckingham Pi to shell vibration is itself textbook (Szilard 2004, Ventsel & Krauthammer 2001). The fact that a closed-form frequency expression can be non-dimensionalised to machine precision is expected—it would be surprising if it couldn't. The 486-point parametric collapse, while visually compelling, is essentially validating algebra, not discovering physics.

### Who would cite this?

- Researchers designing animal-model experiments for whole-body vibration
- Blast injury modellers needing cross-species scaling
- Medical ultrasound groups working with fluid-filled organ models
- Anyone using the equivalent-sphere approximation for non-spherical shells

The paper should explicitly name these communities (see Major Suggestion 1).

---

## Major Suggestions (would substantially improve the paper)

### 1. Reframe the contribution around the *physical discoveries*, not the technique

The current framing emphasises Buckingham Pi as the method. But every reader of JSV knows Buckingham Pi. What they don't know is:

- That mammalian abdominal cavities are approximately similar in the Π-group sense
- That $\mathcal{R}$ is size-independent
- That the breathing mode is permanently irrelevant

**Suggested reframing:** The Introduction should pivot from "We apply Buckingham Pi analysis" to "We show that mammalian abdominal resonance is governed by a quasi-universal dimensionless frequency $\Pi_0 \approx 0.07$, implying that animal models are valid proxies for human studies." The technique is how you got there; the discovery is the destination.

### 2. The allometric scaling needs explicit sources and error bars

Section 4 (Table 2) uses "allometric estimates of $E$ and $a$ from published data" citing only Fung (1993). But:

- What allometric relationships were used? $E \propto M^{\alpha}$? $a \propto M^{\beta}$? The exponents matter.
- Fung (1993) is a general biomechanics textbook. Where specifically do the rat, cat, and pig values come from? Tissue stiffness varies by an order of magnitude depending on strain rate, hydration, and measurement technique.
- What are the uncertainties? If $E$ for rat abdominal wall has a 3× range in the literature, how does that propagate through the scaling law?
- What about $h/a$? Is this actually constant across species? The paper holds $\Pi_1$–$\Pi_6$ values "similar" without demonstrating this quantitatively.

**This is the weakest link in the paper.** The dimensional analysis is exact; the allometric inputs are the source of all uncertainty. A table showing the assumed values of *all* Π-groups for each species (not just $a$ and $f_2$) would be far more informative.

### 3. The $\lambda_n$ membrane mode-shape factor is undefined

Equation (7) introduces $\lambda_n$ as encoding "the membrane mode-shape factor" but never defines it. From Paper 1, we know $\lambda_n = (n^2 + n - 2 + 2\nu)/(n^2 + n + 1 - \nu)$. In a Short Communication that aims to be self-contained, this expression must be given explicitly. A reader should be able to reproduce $\Phi_n$ from this paper alone.

### 4. Discuss sensitivity: which Π-group matters most?

The paper shows the collapse works but doesn't tell the reader *which dimensionless groups dominate*. A short sensitivity analysis—even qualitative—would add significant value. For $n=2$:
- Is bending or membrane stiffness dominant?
- How sensitive is $f_2$ to $h/a$ vs. $\rho_w/\rho_f$ vs. $P_\mathrm{iap}/E$?
- At what $h/a$ does the transition from bending-dominated to membrane-dominated occur?

This would transform the paper from "the scaling law works" to "here is physical insight into what controls the resonance."

### 5. Expand the broader-impact discussion

The Concluding Remarks are too brief for a Short Communication that should justify its standalone existence apart from Paper 1. Specifically:

- **Blast injury scaling:** The scaling law directly enables cross-species extrapolation for blast-overpressure abdominal injury, which is a major concern in military medicine. Cite the relevant literature (e.g., Bass et al. 2008, Stuhmiller 1996).
- **Medical ultrasound:** Fluid-filled organ models are used extensively in diagnostic and therapeutic ultrasound. The dimensionless framework applies.
- **Vehicle NVH:** Whole-body vibration standards (ISO 2631, already cited) rely on empirical transfer functions. The scaling law offers a mechanistic alternative.
- **Underwater acoustics:** Fluid-filled shells are canonical in SONAR target-strength modelling (already cited Junger & Feit). The dimensional reduction is directly applicable.

One paragraph naming these applications would substantially broaden the readership.

---

## Minor Suggestions

### 6. Equation (1) in the abstract: check the scaling form

The abstract writes $f_n = (1/2\pi)\sqrt{E/\rho_f}\,(1/a)\,\Phi_n(\Pi_1,\ldots,\Pi_5)$. This is technically correct but potentially confusing: the $1/2\pi$ is already inside $\Phi_n$ in Equation (5). Ensure consistency so the reader doesn't wonder whether $\Phi_n$ is defined with or without the $2\pi$ factor.

### 7. "Machine precision" is not a validation

The 486-point study collapses to $5.8 \times 10^{-16}$ relative error. This is because both sides of the comparison are evaluating the *same* closed-form expression—it's algebraic identity, not independent validation. The paper should say this clearly (e.g., "This confirms the algebraic consistency of the non-dimensionalisation") rather than implying it validates the physical model. The physical model was validated (or not) in Paper 1.

### 8. Highlight 3 uses $\sqrt{E/\rho_f}$ but the text uses $\sqrt{E/\rho_f}$ in $\Pi_0$

The highlight says "$f_2$ scales as $(1/a)\sqrt{E/\rho_f}$" but $\Pi_0 = f_n a \sqrt{\rho_f / E}$ (Table 1). These are consistent, but the highlight should mention that this holds only when the other Π-groups are approximately constant. As written, it implies a simple two-parameter scaling that ignores $h/a$, $c/a$, etc.

### 9. Table 2 should include $h/a$ and $c/a$ for each species

Currently the table shows only $a$, $f_2$, $\Pi_0$, $ka$, and $\mathcal{R}$. Adding the assumed $h/a$, $c/a$, and $E$ values would let the reader verify the quasi-constancy of the Π-groups independently. This is essential for the claim that "the governing Π-groups take similar values across mammalian species" (line 221–222).

### 10. The title "From Rats to Humans" promises more than delivered

The subtitle implies experimental cross-species data. The paper actually provides *predictions* based on assumed allometric parameters. Consider "Predictions Across Mammalian Scales" or similar.

### 11. Section 5 title: "The breathing mode is always ultrasonic"

At $f_0 \approx 2490$ Hz for humans, this is correct, but for a 3 cm rat the frequency would be ~15 kHz, which is ultrasonic for humans but audible for rats. The title claim is slightly imprecise. Consider "The breathing mode is always well above the infrasonic range" or "is never infrasonic."

### 12. Reference count is thin

Nine references for a JSV Short Communication is acceptable but at the lower end. Key missing references are listed below.

---

## Missing References or Comparisons

1. **Warburton (1976)** — Natural frequencies of thin cantilever shells: comparison between theory and experiment. One of the foundational scaling studies for thin shells.
2. **Junger (1952)** — Sound scattering by thin elastic shells. The original added-mass treatment for fluid-loaded spherical shells.
3. **Bass et al. (2008)** or **Stuhmiller (1996)** — Blast injury scaling across species. Directly relevant to the motivation.
4. **West et al. (1997)** — The general allometric scaling model ($M^{3/4}$ law). If allometric scaling is invoked, the theoretical framework should be cited.
5. **McMahon & Bonner (1983), "On Size and Life"** — Classic reference on allometric scaling of biological structures.
6. **Filippi et al. (2015) or Fahy & Gardonio (2007)** — Modern treatments of fluid-structure interaction that include dimensional analysis perspectives.
7. **Abramson (1966)** — "The Dynamic Behavior of Liquids in Moving Containers" (NASA SP-106). Canonical reference for fluid-filled shell dynamics with extensive dimensional analysis.

---

## What I Liked

1. **The breathing-mode impossibility argument is brilliant in its simplicity.** The 410-metre radius calculation is the kind of result that sticks in the reader's mind. It should perhaps be promoted earlier—even into the Introduction as a teaser.

2. **The cross-species table is immediately useful.** Any experimentalist designing an animal study can look at Table 2 and estimate expected frequencies. This is the kind of concrete output that gets cited.

3. **The three-panel Figure 1 tells a clear story.** The before/after/parity structure is effective pedagogy. This figure alone could justify the paper.

4. **The paper is well-scoped for a Short Communication.** It asks two clear questions and answers them definitively. The writing is clean and direct.

5. **The companion-paper relationship is properly handled.** Paper 3 adds genuine value beyond Paper 1—it's not just a reformulation but a genuine extension that enables new predictions.

---

## Summary Recommendation: MINOR REVISION

The physics is correct and the results are useful. The paper needs:

1. **Reframing** around the physical discoveries rather than the technique (Major 1)
2. **Explicit allometric data with uncertainties** (Major 2)—this is the most important revision
3. **Definition of $\lambda_n$** (Major 3)—straightforward fix
4. **Sensitivity discussion** (Major 4)—even one paragraph would help
5. **Broader impact paragraph** (Major 5)—would significantly increase citation potential

None of these require new calculations. They require clearer exposition of what is already known and careful documentation of the allometric inputs. With these revisions, the paper would be a strong Short Communication that I would expect to be well-cited.
