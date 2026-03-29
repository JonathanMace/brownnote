# Reviewer B — Round 1 (Paper 3: Scaling Laws, post-Reviewer-A revision)

**Paper:** "Scaling Laws for the Flexural Resonance of Fluid-Filled Viscoelastic Shells: Predictions Across Mammalian Scales"
**Target:** Journal of Sound and Vibration — Short Communication
**Reviewer:** B (technical correctness, internal consistency, logical gaps, overclaiming)
**Date:** 2026-07-16
**Reviewing state:** main branch at commit 1cac786 (post-PR #149 Reviewer A fixes)

---

## Decision: MAJOR REVISION

---

## Fatal Flaws

None. The earlier fatal flaw (dimensional error in the breathing-mode calculation, R ≈ 410 m → R ≈ 20 m) has been corrected. The paper is now internally consistent on this point.

---

## Major Issues (must be addressed)

### M1. The "quasi-universal Π₀ ≈ 0.07" claim is circular

This is the central finding of the paper (Abstract line 50, §4 lines 327–331, §5 line 393, Highlight 1) and it is logically circular.

**The argument:** The paper computes Π₀ = Φ(h/a, c/a, ρ_w/ρ_f, P/E, ν) for four species and finds Π₀ varies by only 4.5% (CV). The paper presents this as a discovery about mammalian biology.

**The problem:** Π₀ is a smooth function of five dimensionless inputs. All five inputs are constrained to narrow ranges across the four species:

| Π-group | Range across species | Ratio max/min |
|---------|---------------------|---------------|
| h/a | 0.050 – 0.067 | 1.34 |
| c/a | 0.65 – 0.70 | 1.08 |
| ρ_w/ρ_f | 1.04 – 1.08 | 1.04 |
| P/E | 0.006 – 0.010 | 1.67 |
| ν | 0.45 – 0.45 | 1.00 |

When all inputs to a smooth function vary by less than a factor of 1.7, the output is *guaranteed* to be approximately constant. I computed the Π₀ range over the full cross-species parameter space: CV = 5.1%, confirming this. Over a wider but physically plausible range of h/a (0.03–0.10) and P/E (0.003–0.03), Π₀ spans 0.045–0.118, a 2.7× range.

**The real claim the paper is making** is not that Π₀ is universal, but that *the input Π-groups are approximately conserved across mammalian species*. This is an allometric biology claim, not a shell-mechanics claim. But this allometric claim rests entirely on the assumed parameter values — values that are themselves *chosen* by the authors without species-specific measurements (see M2). The argument is:

1. We assume similar h/a across species → therefore Π₀ is constant → therefore mammals are similar.

This is circular. The constancy of Π₀ is an *input assumption*, not an *output prediction*.

**The paper partially acknowledges this** (§2.3, lines 221–223: "the governing ratios h/a, ρ_w/ρ_f, and P/E are constrained by shared developmental biology"), but it still presents Π₀ ≈ 0.07 as a finding in the Abstract, Highlights, and Conclusions. The language must be reframed: the actual contribution is the *framework* that reduces the comparison to five Π-groups, not the numerical coincidence that those groups happen to be similar for the authors' assumed parameters.

**Required action:** (a) Reframe the Π₀ constancy as a consequence of assumed input constancy, not as an independent discovery. (b) Clearly separate the dimensional analysis framework (which is exact) from the allometric claim (which is hypothesis-dependent). (c) State explicitly: "If the input Π-groups were measured rather than assumed, deviations from Π₀ ≈ 0.07 would quantify the degree of inter-species dissimilarity."

### M2. Cross-species parameters remain unsourced and untraceable

Table 2 (line 310) lists specific values for four species (rat E = 0.05 MPa, cat E = 0.08 MPa, pig E = 0.10 MPa, etc.). The caption (line 303–305) cites Fung (1993), McMahon & Bonner (1983) as sources. The text (lines 277–279) acknowledges these are "estimated from broad allometric trends and tissue-mechanics ranges rather than direct organ-level measurements."

**Problems:**
- Fung (1993) is a 568-page textbook. Which page, which table, which tissue, which species? "Broad allometric trends" is not a citation — it is hand-waving.
- McMahon & Bonner (1983) discusses general allometry (body mass vs. metabolic rate, limb length, etc.). It does not provide abdominal wall moduli for rats, cats, and pigs.
- West et al. (1997) derives quarter-power metabolic scaling laws. It says nothing about abdominal wall thickness or stiffness.
- **No reference in the bibliography provides species-specific abdominal wall E, h, or P_iap values.**

The code's `ANIMAL_MODELS` dictionary (dimensional_analysis.py lines 213–222) hardcodes: rat h = 2 mm, cat h = 4 mm, pig h = 8 mm. These values exhibit suspiciously clean 2× scaling (2, 4, 8, 10 mm). Were these measured or interpolated? If interpolated, from what data?

**The 20% uncertainty stated in the caption (line 307) has no basis.** Where does ±20% come from? Is it 20% on E, h, a, or all three? The propagated uncertainty on Π₀ through the Φ function depends on which parameters are uncertain and whether their uncertainties are correlated. I computed the propagated uncertainty: with ±20% on both h and E simultaneously, the Π₀ uncertainty for each species is only ±3% (because h and E effects partially cancel through the combined h/a and P/E dependence). But the inter-species *spread* of Π₀ (4.5%) is comparable to this intra-species uncertainty, making the "constancy" statistically meaningless.

**Required action:** (a) Provide specific literature values with page-level citations, or honestly state that these are round-number assumptions. (b) Propagate uncertainties formally through the Φ function and report confidence intervals on each species' Π₀. (c) Show that the inter-species Π₀ variance is statistically distinguishable from the within-species parameter uncertainty.

### M3. Equivalent-sphere approximation error is unquantified

The entire analysis maps the oblate spheroid (semi-axes a, a, c) to an equivalent sphere of radius R_eq = (a²c)^{1/3} (line 196), then uses spherical shell mode equations (Lamb 1882, Junger & Feit 1986). For the species in Table 2, the eccentricities are:

| Species | c/a | Eccentricity e | e² |
|---------|-----|---------------|-----|
| Rat | 0.70 | 0.714 | 0.510 |
| Cat | 0.70 | 0.714 | 0.510 |
| Pig | 0.65 | 0.760 | 0.577 |
| Human | 0.67 | 0.742 | 0.551 |

The n = 2 mode frequencies of an oblate spheroid differ from those of a sphere at O(e²). With e² ≈ 0.5–0.6, these corrections are of order 50%. The equivalent-sphere approximation is being applied outside its range of validity, yet the paper never quotes an error bound or compares against a spheroidal-mode calculation.

The companion paper (Paper 1) presumably discusses this approximation, but this paper must at least:
(a) State the approximation explicitly and estimate its error.
(b) Note that the c/a variation across species (0.65–0.70) induces a systematic bias in Π₀ that is not captured by the spherical model.

This is particularly important because c/a = Π₂ is one of the five "governing" dimensionless groups, yet the spherical-mode equations are formally independent of c/a (the aspect ratio enters only through R_eq, which is a volume-preserving mapping). The actual mode-frequency dependence on c/a for an oblate spheroid includes curvature-dependent terms that the equivalent sphere ignores.

### M4. ℛ_scat = 1/(kR)² as the scattering penalty: physics justification insufficient

The paper defines ℛ_scat = 1/(kR_eq)² for the n = 2 mode (Table 2, line 296) and claims this "quantifies the Rayleigh-regime scattering penalty for airborne excitation." Several issues:

**(a) Missing derivation or reference.** The (kR)^n scaling for the n-th spherical harmonic component of a plane wave incident on a sphere follows from the expansion of e^{ikz} in spherical Bessel functions (j_n(kr) ~ (kr)^n/(2n+1)!! for kr ≪ 1). The paper asserts 1/(kR)^2 without derivation and without citing the specific result (e.g., Junger & Feit Ch. 7, or Morse & Ingard Ch. 8). The reader is left wondering: is this (kR)^n or (kR)^{2n}? Is it an amplitude ratio or a power ratio?

**(b) Amplitude vs. power ambiguity.** In acoustics, scattering cross-sections are typically defined in terms of power, giving (ka)^{2(n+1)} scaling for the n-th partial wave. The 1/(kR)² quantity in the paper is apparently an *amplitude* ratio (displacement). This should be stated explicitly.

**(c) Relationship to Paper 1's ℛ_full is confusing.** The caption (lines 298–302) says the full displacement ratio in Paper 1 is "approximately 8× larger because it additionally includes the acoustic impedance mismatch." But 8× larger than ~10⁴ gives ~8×10⁴, while Paper 1 reports ℛ_full ≈ 6.6×10⁴. The factor of 8 is consistent, but this means the impedance mismatch factor is only ~8, while Z_tissue/Z_air ≈ 3600. How does a 3600× impedance mismatch produce only an 8× correction to the coupling ratio? This needs explanation.

### M5. The "1458-point parametric validation" oversells algebraic identity

The paper improved on the earlier 486-point sweep by adding variations in ρ_w/ρ_f and ν (now 1458 points). The "maximum relative error 7.9 × 10⁻¹⁶" (line 71) is correctly described as "algebraic consistency" (line 250). However:

- Highlight 2 still reads "1458-point parametric study confirms algebraic consistency of non-dimensionalisation." This is literally true but rhetorically misleading in a highlights list, where readers expect empirical or numerical results.
- Figure 1 devotes a three-panel figure (dimensional data, collapsed data, parity plot) to showing an algebraic identity. For a Short Communication with strict space limits, this figure real-estate would be better used for sensitivity analysis, uncertainty propagation, or comparison with any experimental data.
- The parity plot (panel c) showing "max error < 10⁻¹⁵" is trivially expected and could be replaced with a single sentence.

**Suggestion:** Reduce Figure 1 to two panels (raw data and collapsed data). Use the freed space for a sensitivity plot (Π₀ vs. h/a with uncertainty bands from parameter ranges) or for showing how Π₀ varies if the assumed allometric parameters are perturbed.

---

## Minor Issues (should be addressed)

### m1. Highlight 3 is misleading without qualification

Highlight 3: "Cross-species f₂ scales as (1/a)√(E/ρ_f) when other Π-groups are approximately constant." The qualification "when other Π-groups are approximately constant" is essential but easy to miss. Since the other Π-groups *do* vary (h/a by 34%, P/E by 67%), the actual scaling deviates from 1/a, as the paper notes (Figure 2 left panel). The highlight should not imply a simple power law when the reality is more nuanced.

### m2. Eq. (3)–(6): stiffness terms need clearer dimensional statement

The stiffness terms K_bend, K_memb, K_pre (lines 189–192) and effective mass m_eff (line 193) are presented in dimensional form, but the non-dimensionalisation step (where K̃ = K·a/E and m̃ = m/(ρ_f·a)) is only shown in the code docstring (dimensional_analysis.py lines 84–87), not in the paper. The reader cannot independently verify the algebraic reduction from Eq. (3)–(6) to Φ_n without performing the non-dimensionalisation themselves. Either show the intermediate step or provide it in supplementary material.

### m3. The sensitivity analysis (§2.3) lacks quantitative metrics

Section 2.3 reports that K_memb contributes ~54%, K_pre ~45%, K_bend <2% (lines 205–207). These are useful but incomplete. What is the partial derivative ∂Π₀/∂(h/a), ∂Π₀/∂(P/E), etc., evaluated at the canonical point? A dimensionless sensitivity index (e.g., S_i = (∂Π₀/∂Π_i) × (Π_i/Π₀)) would quantify "most sensitive to" more rigorously than a stiffness-budget decomposition.

### m4. Table 2: P_iap/E values are suspiciously smooth

The P/E ratios (0.006, 0.008, 0.008, 0.010) follow a clean progression. But the underlying P_iap values in the code (300, 600, 800, 1000 Pa) and E values (50, 80, 100, 100 kPa) are round numbers. This suggests estimated rather than measured values. The paper acknowledges this (line 278) but should more prominently flag that these are order-of-magnitude estimates.

### m5. The breathing-mode formula (Eq. 10) drops the shell stiffness without justification

Equation (10) (line 372) gives f₀ ≈ (1/2π)√(3K_f/(ρ_f R²)). The full model (natural_frequency_v2.py lines 103–117) includes both shell membrane stiffness k_shell = 2Eh/(R²(1−ν)) and fluid stiffness k_fluid = 3K_f/R. For human parameters, k_fluid/k_shell ≈ 3×2.2e9/0.157 / (2×0.1e6×0.01/(0.157²×0.55)) ≈ 4.2e10 / 2340 ≈ 1.8×10⁷, so the approximation is excellent. But the paper should state the ratio explicitly to justify the simplification.

### m6. Missing comparison with known shell results

The membrane mode-shape factor λ_n (Eq. 9) and the added-mass expression m_added = ρ_f R/n are standard results but the specific combination here should be verified against at least one tabulated value. For instance, Leissa (1973, NASA SP-288) Table 11.2 gives natural frequencies of fluid-filled spherical shells. Does the present formula reproduce those values? Even one comparison point would strengthen the paper considerably.

### m7. Poisson's ratio held at ν = 0.45 across all species

The paper varies ν in the parametric sweep (0.40–0.49) but holds it fixed at 0.45 for all species in Table 2 (line 285). Soft tissue Poisson's ratio varies from ~0.3 (fat) to ~0.499 (muscle, nearly incompressible). Holding ν constant eliminates one of the five "governing" Π-groups from the cross-species comparison, effectively reducing the comparison to four Π-groups.

---

## Positive Comments

1. **The Buckingham Pi analysis is correct.** I verified: 11 variables, 3 fundamental dimensions (M, L, T), rank-3 dimension matrix, 8 independent Π-groups, repeating variables {E, a, ρ_f} span the dimension space (det = 2 ≠ 0). The identification of 5 governing groups for flexural modes (dropping K_f and η) is physically sound.

2. **Code-paper consistency is excellent.** All numerical values in Table 2 match the code output to the stated precision. The human f₂ = 3.94 Hz, Π₀ = 0.0717, kR = 0.0114, ℛ_scat = 7721 — all verified against the code. The breathing-mode R ≈ 20.2 m is correct.

3. **The breathing-mode impossibility argument is well-executed** (post-correction). The calculation is elementary but the conclusion — that the breathing mode is irrelevant to infrasound for any biological organism — is useful and clearly stated.

4. **The earlier Reviewer A and B issues have been substantially addressed.** The dimensional error is fixed, λ_n is defined, the parametric sweep now varies all 5 Π-groups, the ℛ_scat notation has been clarified relative to Paper 1, sensitivity analysis and broader-impact sections have been added, and the title no longer overpromises experimental data.

5. **The paper is concise and well-structured** for a Short Communication. The progression from dimensional analysis → parametric collapse → cross-species prediction → negative result is logical and efficient.

6. **All 24 tests related to scaling/dimensional analysis pass** (verified: `pytest tests/ -v -k "scaling or dimensional"` — 24 passed). The test suite covers Π₀ definition, Φ analytical agreement, parametric sweep point count and collapse precision, animal scaling Π₀ range, R_scat bounds, Rayleigh-regime kR, and breathing-mode radius.

---

## Summary

The paper presents a correct Buckingham Pi analysis of a fluid-filled viscoelastic shell and derives a closed-form scaling law for flexural-mode frequencies. The dimensional analysis framework is technically sound and potentially useful. However, the paper's central claim — that Π₀ ≈ 0.07 is "quasi-universal" across mammals — is circular: it is an inevitable consequence of assuming that the input dimensionless groups are approximately constant across species, which is itself an unvalidated assumption based on unsourced parameter estimates. The equivalent-sphere approximation introduces O(e²) ≈ 50% errors that are never quantified. The scattering penalty physics needs clearer justification.

The paper has substantive value as a **framework paper** — providing the Π-group decomposition, the closed-form Φ function, and the breathing-mode impossibility result. But it currently overclaims by presenting assumed-input constancy as a discovered-output universality. With honest reframing of what is demonstrated vs. what is assumed, tighter sourcing of cross-species parameters (or frank acknowledgment that they are illustrative), and an error estimate for the equivalent-sphere mapping, this would be a solid Short Communication.

**Recommendation: MAJOR REVISION**

Three issues must be resolved:
1. **Reframe the Π₀ universality claim** as a consequence of assumed input constancy, not a discovery (M1).
2. **Source or honestly characterize the cross-species parameters** (M2).
3. **Quantify the equivalent-sphere approximation error** for e² ≈ 0.5 (M3).

The remaining major issues (M4, M5) and minor issues are addressable with modest revision.
