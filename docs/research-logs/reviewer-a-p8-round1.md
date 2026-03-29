# Reviewer A — Round 1

**Paper:** "Can You Hear the Shape of an Organ? Practical Identifiability of Viscoelastic Shell Parameters from Resonant Frequencies"
**Target venue:** Inverse Problems (IOP)
**Reviewer:** A (domain expert — structural acoustics / inverse problems)
**Date:** 2026-03-29

---

## Overall Assessment

This is a well-motivated paper that asks a good question—can the geometry and stiffness of a fluid-filled viscoelastic shell be recovered from its resonant frequencies?—and answers it with a clean numerical framework. The Kac framing is attention-grabbing and mostly appropriate. The chain-rule rank-deficiency proof (Proposition 1) is elegant and instructive. The condition-number map is a genuine contribution to experimental design. The writing quality is high, with effective dry wit ("slightly different dinner plan"; "persuade it to behave").

However, several issues prevent acceptance in the current form. The most important is a **model-identity confusion**: the paper repeatedly states that the forward model is an equivalent-sphere model (§1 ¶4, §2.1 final paragraph, §4.3), yet the headline oblate result ($\kappa = 73$) is computed using the Ritz model that integrates over the actual oblate surface. This is not a minor labelling error—it changes what the paper is about. Additionally, the Cramér–Rao bounds at 1% noise ($a \pm 37\%$, $E \pm 36\%$) are large enough to undercut the headline claim, and the paper does not sufficiently confront this. Proposition 2 is presented as an analytical result but reads as a heuristic sketch that would not satisfy Inverse Problems readers.

The bones of a strong paper are here. It needs one round of substantive revision to become publishable.

---

## Significance and Novelty

**What is new:**
1. The explicit demonstration that an $R_\mathrm{eq}$-only forward model is structurally non-identifiable for the $(a, c, E)$ triple (Proposition 1). This is a crisp, quotable result.
2. The quantitative contrast: $\kappa_\mathrm{sphere} / \kappa_\mathrm{oblate} \approx 1.5 \times 10^8$, and the condition-number map (Fig. 4/condition\_map) as a pre-experimental feasibility tool.
3. The "mode-dependent curvature sampling" mechanism as a physical explanation for identifiability restoration.
4. The practical design rule: five modes, not three.

**Who would cite this:**
- Elastography groups (Doyley, Sarvazyan communities) working on resonance-based tissue characterisation
- Agricultural NDE researchers using vibration for fruit/produce quality
- Structural identification researchers working on thin-shell systems
- Anyone doing spectral inverse problems on geometrically parametrised models

The paper would be cited primarily for the methodology (Jacobian conditioning + Fisher information as an identifiability diagnostic before inversion) and for the design rule (five modes, sufficient asphericity). This is a modest but useful contribution. For Inverse Problems, it is at the lower end of significance unless the analytical content is substantially strengthened.

---

## Major Suggestions (would substantially improve the paper)

### M1. Resolve the model-identity confusion (Critical)

The paper says, repeatedly and emphatically, that the implemented forward model is an equivalent-sphere model that depends on $(a, c)$ only through $R_\mathrm{eq} = (a^2 c)^{1/3}$ (Introduction ¶4; Theory §2.1 final paragraph "The model depends on $(a,c)$ only through $R_\mathrm{eq}$"; Results §4.3 "The implemented forward model contains no explicit aspect-ratio terms"). Yet the code reveals that the oblate results use `model="ritz"` (calling `oblate_ritz_frequencies()`), which is a genuine 2-DOF Rayleigh–Ritz model integrating strain energy over the actual oblate spheroidal surface via the geometric factor $G(\eta) = a^2\eta^2 + c^2(1-\eta^2)$. This model *does* contain explicit aspect-ratio dependence—it is the entire reason the oblate Jacobian has full rank.

The paper's actual contribution is: **the equivalent-sphere model is structurally non-identifiable, but the Ritz model (which properly represents oblate curvature) restores identifiability.** This is a more interesting and honest statement than what the abstract and introduction currently convey. The paper should:
- State clearly, from the abstract onwards, that *two* forward models are compared: the $R_\mathrm{eq}$-only model (§2.1 Eq. 5) and the oblate Ritz model
- Reserve the "equivalent-sphere" label for the sphere-limit analysis only
- Explain that Proposition 1 applies to the first model and Proposition 2 applies to the second
- Remove or correct the misleading claim in §4.3 that the oblate results use the equivalent-sphere model

This is the single most important revision. Without it, a careful reader (or referee) will conclude the paper contradicts itself.

### M2. Confront the Cramér–Rao bounds honestly

At 1% frequency noise, the CRB uncertainties are $a \pm 37\%$, $c \pm 13\%$, $E \pm 36\%$. Table 1 presents these without adequate commentary. For a paper whose title asks "Can you hear the shape?", the answer appears to be: *barely, and only $c$ with useful precision.* The paper should:

- Discuss what noise level would be needed for, say, 5–10% parameter uncertainty. Since CRBs scale linearly with $\epsilon_\mathrm{noise}$, this is a simple calculation: you would need $\sim 0.13\%$ frequency precision to get $c$ to $\pm 1.7\%$, or $\sim 0.27\%$ to get $a$ to $\pm 10\%$. Are such precisions realistic? In modal analysis of soft biological structures, frequency estimation uncertainty is typically 1–5%, so the bounds matter.
- Discuss the *anisotropy* of the CRB: why is $c$ so much better resolved than $a$ and $E$? The right singular vectors of $\mathbf{J}_s$ would illuminate this. Which parameter combination is the weakly observable direction? If it is an $a$–$E$ trade-off (size–stiffness confounding), say so—this is a known issue in elastography.
- Consider whether a Bayesian prior (even weak) on any parameter would dramatically improve the others. This is standard in the identifiability literature and natural for a paper targeting Inverse Problems.

The box plots in Fig. 4 (inversion\_noise) actually show the problem: at 5% noise, recovered $E$ errors span $\pm 500\%$, and even at 2% noise the whiskers are alarming. The figure currently undermines the narrative. Either discuss it honestly or replace the five-noise-level sweep with a more focused analysis at 0.5–2% noise where the inversion is meaningful.

### M3. Strengthen Proposition 2 or downgrade it

Proposition 2 (§2.6) is labelled as a proposition but reads as an intuitive argument with many "..." steps. Specifically:
- Eq. (19) defines $I_n^{(k)}$ but $\Delta I_n^{(k)}$ in Eq. (21) is given without derivation
- The key claim—that $\int_0^1 P_n^2(\eta)(\eta^2 - 1/2)\,d\eta$ depends on $n$—is true but stated rather than proved. For an Inverse Problems paper, this integral can be evaluated in closed form using Legendre orthogonality. Do so.
- The notation "Ritz variational model" in the proposition statement is imprecise. Which functional, which trial space, which boundary conditions?
- The correction $\delta_n$ in Eq. (22) is never given explicitly, nor is $\alpha$ in the power law (26). The reader is told these exist but never sees them.

**Options:**
(a) Complete the proof: evaluate $\int_0^1 P_n^2(\eta)(\eta^2 - 1/2)\,d\eta$ in closed form for general $n$ (it involves $4n+3$ denominators via standard Legendre recurrences), give $\delta_n$ explicitly, and fit $\alpha$ from the numerics. This would make it a genuine result.
(b) Downgrade it to a Remark or Discussion-section argument, and state clearly that it is a heuristic. Do not call it a Proposition if the proof is incomplete.

For Inverse Problems, option (a) is strongly preferred.

### M4. Add profile likelihood or discuss its absence

The paper cites Raue et al. (2009) and Wieland et al. (2021) for the definition of practical identifiability, yet does not use their signature diagnostic tool: the profile likelihood. Profile likelihood plots for each of $(a, c, E)$ would:
- Show whether the cost landscape is unimodal or has ridges/valleys
- Reveal practical identifiability in a way the Fisher matrix (which is local and Gaussian) cannot
- Be expected by any Inverse Problems referee familiar with the Raue framework

If profile likelihood computation is computationally expensive, at least show cost-function slices through the optimum along each parameter axis and along the weakly observable direction identified by the SVD. Alternatively, acknowledge explicitly that the Fisher/CRB analysis is a local, linearised diagnostic and that profile-likelihood confirmation is left to future work.

### M5. Flesh out the watermelon case or remove it

The watermelon cross-application is presented as a single number ($\kappa \approx 104$) in two short paragraphs (§4.8) with no CRB table, no inversion demonstration, no comparison to experimental data, and no discussion of what "ripe watermelon" parameters are based on. For a target journal like Inverse Problems, this is either a full case study or a throwaway remark. Suggestions:
- At minimum: add a CRB table and a round-trip inversion result for the watermelon case
- Ideally: cite the agricultural vibration literature (see Missing References below) and discuss whether published watermelon resonance data could be used for experimental validation
- The condition map (Fig. 3) already marks the watermelon operating point, which is good. Connect the text more explicitly to this figure.

---

## Minor Suggestions

### m1. The $\kappa = 100$ threshold (Fig. 1) needs justification
The dashed green line at $\kappa = 100$ is presented as a "well-conditioned threshold" without citation or justification. In numerical linear algebra, $\kappa < 10^2$ is a common rule-of-thumb for well-conditioned systems (Trefethen & Bau, Lecture 12), but in inverse problems the acceptable threshold depends on the noise level and the dimension of the problem. State this explicitly, or replace with a statement like "for 1% frequency noise, $\kappa < 100$ ensures parameter errors below X%."

### m2. Report the fitted power-law exponent $\alpha$
Section 4.9 and Fig. 5 discuss the power law $\kappa \sim C\varepsilon^{-\alpha}$ without reporting the actual fitted values of $C$ and $\alpha$. These are the quantitative design rule the paper promises. Give numbers.

### m3. Right singular vectors
The SVD singular values are shown (Fig. 2) but the corresponding right singular vectors are not. The weakly observable direction in $(a, c, E)$ space is at least as informative as the singular value itself. For the spherical case, is it the $a$–$c$ combination $(2, -1)$ as Proposition 1 predicts? For the oblate case, which parameter combination is worst? Report these explicitly.

### m4. Newton solver vs. Gauss–Newton nomenclature
The solver is described as "Newton-type" (§3.2) but uses `scipy.optimize.least_squares` with trust-region reflective, which is a Levenberg–Marquardt/Gauss–Newton variant. Be precise about the algorithm used. This matters because the convergence properties differ.

### m5. Step-size sensitivity for finite differences
The step size $\delta_j = 10^{-6}|\theta_j|$ is stated (§3.1) and convergence is asserted. Show convergence briefly: e.g., a small table of $\kappa$ at step sizes $10^{-4}$, $10^{-6}$, $10^{-8}$ confirming plateau.

### m6. Condition map numerical artefacts
The condition-number map (Fig. 3/condition\_map) has visible pixelation and a few bright outlier cells (notably the yellow pixel near $a = 0.14$, $\zeta = 0.57$). Either increase the grid resolution or apply light smoothing to remove single-cell artefacts. For an Inverse Problems publication, figure polish matters.

### m7. Notation: $\zeta_g$ vs $\zeta$
The paper defines $\zeta_g = 1 - c/a$ (§3.5) but the condition map figure axis says $\zeta = c/a$. Reconcile. The figure uses the aspect ratio, the text uses the flattening. Pick one convention and be consistent.

### m8. Abstract length
The abstract is 160 words — borderline long for IP. It reads well, but "The result has implications for non-invasive tissue characterisation and fruit quality assessment" could be cut to save space.

### m9. Conclusion actionability
The conclusion's practical recommendation ("measure at least five low-order flexural resonances") is valuable. Strengthen it: what is the minimum eccentricity (asphericity) for the inverse problem to be feasible at, say, 1% noise? The condition-number map contains this information—extract and state a number.

---

## Missing References or Comparisons

The bibliography (13 entries) is thin for a paper targeting Inverse Problems. Key gaps:

1. **Oberai, Gokhale & Feijóo (2003)** — "Solution of inverse problems in elasticity imaging using the adjoint method," *Inverse Problems* 19(2):297. Directly relevant: identifiability of elastic moduli from vibrational data.

2. **Barbone & Bamber (2002)** — "Quantitative elasticity imaging: what can and cannot be inferred from strain images," *Phys. Med. Biol.* 47:2147. Canonical discussion of what spectral/strain data can identify.

3. **McLaughlin & Renzi (2006)** — "Shear wave speed recovery in transient elastography and supersonic imaging using propagating fronts," *Inverse Problems* 22(2):681. Uniqueness results for wave-based elastography.

4. **Zelditch (2004)** — "Inverse spectral problem for analytic domains, I," *Annals of Mathematics* 160:401. Modern treatment of spectral geometry connecting to Kac. Would strengthen the mathematical framing.

5. **Chen & De Baerdemaeker (1993)** and **Cooke (1972)** — vibration-based fruit firmness estimation. The agricultural application deserves actual citations from the extensive melon/apple/fruit vibration literature.

6. **Trefethen & Bau (1997)** — *Numerical Linear Algebra.* For the condition-number interpretation and threshold.

7. **Nocedal & Wright (2006)** — *Numerical Optimization.* For the trust-region solver description.

8. **Choi, Oberai & others (2015)** — more recent identifiability analysis in elasticity, showing parameter trade-offs in soft tissue.

The paper cites Gladwell (2004/2005), Henrot (2006), Hald (1978/1984), and Kato (1966), which are all appropriate. But citing them in the discussion without engagement is insufficient for IP. At minimum, say concretely how the present problem relates to Gladwell's classification of inverse vibration problems.

---

## What I Liked

1. **The title.** It is memorable, accurate enough, and will make people read the abstract.
2. **Proposition 1.** The chain-rule rank deficiency is one of those results that, once seen, seems obvious—but someone had to write it down clearly and connect it to the identifiability question. This is a service to the community.
3. **Honesty about limitations.** The limitations section (§5.7) is unusually thorough and candid. The paper does not oversell.
4. **The condition-number map (Fig. 3).** This is the figure I would show in a tutorial on experimental design for inverse problems. It conveys the key message immediately: avoid the spherical limit, and a broad region of parameter space is viable.
5. **Writing quality.** The prose is clear, concise, and occasionally witty without being cute. The sentence "spherical simplifications are serviceable on the blackboard; in inverse problems they become noticeably less cooperative" (§5.4) is well-crafted.
6. **The singular-value comparison (Fig. 2).** Side-by-side, log-scale, clean labelling. Publication quality.
7. **Reproducibility.** Code and data are available via a public repository. This is appreciated.

---

## Summary Recommendation: **MAJOR REVISION**

The paper contains a valid and useful contribution, but the model-identity confusion (M1) is serious enough that a referee unfamiliar with the code would be misled about what was actually computed. The CRB interpretation (M2) and the incomplete Proposition 2 (M3) are substantive weaknesses for Inverse Problems. All three can be addressed in one revision.

**Path to acceptance:**
1. Fix M1 (model clarity) — this is non-negotiable.
2. Address M2 (honest CRB discussion) and M3 (strengthen or downgrade Prop 2).
3. Add M4 (profile likelihood or cost-landscape slices) or justify its omission.
4. Flesh out M5 (watermelon case) to at least include CRBs.
5. Add 4–6 missing references and connect to them substantively.
6. Clean up the minor points (m1–m9).

With these changes, the paper would be a solid contribution to Inverse Problems. Without M1 at minimum, I cannot recommend acceptance.
