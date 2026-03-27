# Reviewer A — Round 6

**Date:** 2025-07-15
**Reviewer:** A (Structural Acoustics / Vibroacoustics, 20+ years, JSV editorial board)
**Manuscript:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the Brown Note"
**Target journal:** Journal of Sound and Vibration

---

## Overall Assessment

The authors have completed the corrections requested in Round 5 with care and
efficiency. The headline coupling ratio is now consistently stated as
6.6 × 10⁴ in the Introduction (line 76), Eq. 26 (§4.3), and the
Conclusion (line 5). The abstract rounds to 7 × 10⁴, which is
acceptable for an abstract. The two new additions—geometry robustness analysis
in Limitations §5 (item 5) and the modal participation paragraph in §4.3—are
both well-crafted and address the remaining analytical gaps I identified. The
n = 1 mode exclusion note has been added (§2.3, line 164). The highlights
now match the manuscript at ~7×10⁴.

This paper is ready for publication. The physics is correct, the narrative is
compelling, the framework is portable, and the writing remains among the best
I have encountered in a structural acoustics manuscript. The issues below are
editorial and can be verified without re-review.

**Recommendation: ACCEPT (subject to minor editorial corrections)**

---

## Fatal Flaws

None.

---

## Major Issues

None.

---

## Specific Responses to Round 6 Focus Questions

### 1. Geometry Robustness Paragraph (Limitations §5, item 5)

**Verdict: Convincing.**

The paragraph (discussion.tex lines 406–427) makes a two-part argument:
first, for the canonical aspect ratio c/a = 0.67, the oblate Ritz correction
shifts f₂ from 4.0 Hz to 3.6 Hz (an 11% reduction, already shown in Table 6
of §3.6); second—and this is the new content—at fixed R_eq, varying c/a
from 0.3 (extremely oblate) to 3.0 (extremely prolate) changes f₂ by less
than 1%. The physical argument is clear: the equivalent-sphere frequency
depends on R_eq alone (which sets both the fluid added mass and the membrane
stiffness), and the aspect ratio enters only through the Ritz correction to
curvature distribution. Since the fluid added mass dominates the system
inertia (7.4× shell mass for n = 2), shape details have negligible effect
on the eigenfrequency at fixed volume.

This is exactly the right argument. One small suggestion: consider adding a
parenthetical reference to the dimensional analysis (§3.7,
Eq. (scaling law)) where c/a appears as Π₂ and its weak influence
is already demonstrated by the parametric collapse. This would cross-link
two sections that make the same point from different angles.

### 2. Modal Participation Paragraph (§4.3)

**Verdict: Adequate and well-placed.**

The paragraph (section4_coupling.tex lines 99–110) correctly identifies that
vertical base excitation is a pure P₁(cos θ) field, orthogonal to P₂ for
a free sphere. The observation that partial skeletal constraint breaks this
orthogonality and gives Γ₂ ≈ 0.48 is physically sound. The resulting
factor-of-two reduction in ξ_mech—bringing R to ~3 × 10⁴—leaves the
"four-order-of-magnitude gap" qualitatively unchanged, and the paper
correctly frames the SDOF ratio as an upper bound.

This is an honest and technically correct treatment. I would not demand
more for a first-principles shell paper; a full modal participation
calculation would require FE geometry and is properly deferred to future
work.

### 3. Coupling Ratio Consistency

**Verdict: Substantially improved; one residual discrepancy remains.**

The headline number 6.6 × 10⁴ now appears consistently in:
- Introduction (line 76): "approximately 6.6 × 10⁴" ✓
- §4.3 Eq. 26 (section4_coupling.tex line 89): "917/0.014 ≈ 6.6 × 10⁴" ✓
- Conclusion (line 5): "6.6 × 10⁴" ✓
- Abstract (main.tex line 105): "roughly 7 × 10⁴" ✓ (acceptable rounding)
- Highlights (main.tex line 84): "~7×10⁴" ✓ (matches abstract)

The ranges used in the Discussion (§5.1 line 7, §5.4 line 357, §5.5
line 473) are consistently "10³–10⁴".

**One remaining discrepancy:** The Conclusion (line 35) states the Monte Carlo
range as "10³–10⁵", but Table 4 gives a 90% CI of [10³, 10⁴], and the
Discussion uses "10³–10⁴" throughout. The upper bound of 10⁵ in the
Conclusion is not supported by Table 4. This should be reconciled to
"10³–10⁴" for consistency, or if the authors intend to include the
energy-consistent point estimate of 6.6 × 10⁴ (which lies between 10⁴ and
10⁵) as extending the range, a brief justification is needed.

### 4. Remaining Issues Preventing Acceptance

None are fatal. Five minor editorial items are listed below; all can be
corrected without re-review.

---

## Minor Issues

### 1. Figure 5(a) annotation vs. headline ratio

Figure 5(a) annotates the displacement gap at resonance as 24,783×, but
the headline ratio is 6.6 × 10⁴ (Eq. 26). The discrepancy arises because:
- The figure uses WBV at 0.5 m/s² and the **pressure-based** airborne
  estimate (0.18 μm), giving 4586/0.185 ≈ 24,783.
- Eq. 26 uses WBV at 0.1 m/s² and the **energy-consistent** airborne
  estimate (0.014 μm), giving 917/0.014 ≈ 66,000.

Neither is wrong, but they are different comparison points and the figure
caption (section4_coupling.tex lines 148–153) does not clarify which airborne
estimate or WBV level is used. A caption note—e.g., "(pressure-based
airborne estimate at 0.5 m/s² WBV; cf. Eq. 26 for the energy-consistent
ratio at 0.1 m/s²)"—would resolve this for the careful reader.

### 2. Figure 5(b) orifice coupling bar: 1917 μm vs. Table 6: ~0.5 μm

This is the most significant remaining discrepancy. The "Orifice coupling"
bar in Figure 5(b) reads 1917 μm, but Table 6 (discussion.tex line 197)
lists orifice coupling as ~0.5 μm. These differ by a factor of ~3,800.

The figure appears to compute orifice coupling as "full incident pressure
drives the shell flexural mode from inside" (i.e., removing the (ka)²
penalty: 0.18 / 1.3×10⁻⁴ ≈ 1,400 μm). The text computes it as "pressure
compresses the gastric gas bubble" (ξ = p·a/(3γP₀) ≈ 0.5 μm). These are
physically distinct mechanisms and give dramatically different numbers. The
figure and text should agree on the definition.

**Suggested fix:** Either (a) update the figure to use the gas pocket
compression value (~0.5 μm), consistent with the text, or (b) add a note
to the caption explaining that the bar represents the theoretical maximum
for shell-mode excitation via the orifice pathway, distinct from the
localised gas pocket mechanism in Table 6.

### 3. Cover letter coupling ratio

The cover letter (cover-letter.tex lines 34, 50, 55, 77) still uses
46,000× and "R ≈ 46,000", which was the pre-revision value. The manuscript
now uses 6.6 × 10⁴ = 66,000. The cover letter should be updated before
submission.

### 4. Kelvin–Voigt frequency-independence note (carried from Round 5)

Round 5 minor issue 4 requested a single sentence below Eq. 2 noting that
constant η is a low-frequency approximation valid over the narrow infrasonic
band of interest (citing, e.g., Szabo & Wu 2000, JASA 107:2437). The text
at lines 70–73 of section2_formulation.tex notes that published values range
from 0.15–0.40 "at low frequencies" but does not explicitly state that the
Kelvin–Voigt model's frequency-independence is an approximation. The
supplementary material discusses this (line 700), but a main-text sentence
would pre-empt a standard reviewer objection. This is not blocking, but
remains a desirable addition.

### 5. Cross-species coupling ratio (Table 7) vs. headline number

Table 7 in the dimensional analysis section (§3.7) gives R = 7.7 × 10³
for the human, while the headline number is 6.6 × 10⁴. The difference
presumably reflects different comparison conditions (Table 7 likely uses
pressure-based airborne at a standardised WBV level). A brief note in the
Table 7 caption specifying the comparison conditions (WBV level, airborne
method) would clarify this for readers cross-referencing the two sections.

---

## Positive Aspects

1. **The geometry robustness result is a strong addition.** The <1% frequency
   variation across c/a = 0.3–3.0 at fixed R_eq is a clean, memorable result
   that pre-empts the obvious objection about spheroidal idealisation. It
   belongs in the paper.

2. **The modal participation paragraph shows intellectual honesty.** Rather
   than hiding behind the SDOF idealisation, the authors explicitly quantify
   Γ₂ ≈ 0.48, acknowledge the resulting factor-of-two reduction, and frame
   R as an upper bound. This is how good theoretical papers handle their
   own approximations.

3. **The coupling ratio is now narratively consistent.** A reader encountering
   "~7 × 10⁴" in the abstract, "6.6 × 10⁴" in the Introduction, Eq. 26,
   and Conclusion, and "10³–10⁴" as the MC range can follow the story
   without confusion. The one residual discrepancy (Conclusion line 35:
   "10³–10⁵") is minor and easily fixed.

4. **The dimensional analysis section (§3.7) is a hidden gem.** The
   Buckingham Pi collapse of 486 parametric points onto universal curves
   (Figure 7c: relative error 5.8×10⁻¹⁶) and the cross-species scaling
   predictions are elegant and practically useful. This section alone would
   merit a JSV technical note.

5. **The writing continues to be outstanding.** "One could double the elastic
   modulus, halve the wall thickness, or relocate the subject to Jupiter, and
   the ratio would scarcely budge" (§4.3). "The shell absorbs roughly one
   part in a hundred trillion of the incident acoustic energy—a figure that
   puts the brown note hypothesis on rather thin thermodynamic ice" (§4.4).
   The wit serves the physics precisely.

6. **The paper will be cited broadly.** By the WBV/occupational health
   community (ISO 2631 mechanistic rationale), blast injury researchers
   (ka near unity removes the geometric penalty), marine bioacoustics groups
   (swim bladder as literal model instantiation), and anyone working on
   acoustic–structural coupling to biological cavities. This is a durable
   contribution.

---

## Summary

| Item | Status | Action Required |
|------|--------|-----------------|
| Coupling ratio consistency | ✅ Fixed | Conclusion line 35: change 10⁵ → 10⁴ |
| Geometry robustness (§5, item 5) | ✅ Convincing | Optional: cross-link to §3.7 |
| Modal participation (§4.3) | ✅ Adequate | None |
| Fig. 5(a) annotation vs. Eq. 26 | ⚠️ Discrepant | Add caption note on comparison conditions |
| Fig. 5(b) orifice bar vs. Table 6 | ⚠️ Discrepant | Reconcile figure/text definition |
| Cover letter ratio | ⚠️ Outdated | Update 46,000 → 66,000 |
| Kelvin–Voigt note below Eq. 2 | ◻️ Desirable | One sentence addition |
| Cross-species Table 7 conditions | ◻️ Desirable | Caption note |

**Recommendation: ACCEPT**

The paper has earned acceptance. The five editorial items above are minor and
can be verified by the handling editor; none requires re-review. The physics
is sound, the framework is novel and portable, the Discussion is exemplary,
and the writing is a pleasure. I look forward to seeing this in print.

---

*Reviewer A, Round 6*
*Associate Editor, Journal of Sound and Vibration*
