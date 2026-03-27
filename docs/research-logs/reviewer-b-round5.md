# Reviewer B — Round 5

**Date:** 2025-07-15  
**Reviewer:** B (Computational Acoustics / Fluid–Structure Interaction, 25 years)  
**Manuscript:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the 'Brown Note'"  
**Journal:** Journal of Sound and Vibration  

**Documents reviewed (complete):**
- `paper/main.tex` and all section files in `paper/sections/`
- `paper/supplementary.tex`
- `paper/references.bib`
- All Python modules in `src/analytical/` (natural_frequency.py, natural_frequency_v2.py, acoustic_coupling.py, mechanical_coupling.py, energy_budget.py, modal_participation.py)
- Independent numerical verification of all key results (see below)
- Round 4 review and Reviewer A Round 5

---

## Decision: MAJOR REVISION

The paper has improved substantially since Round 4. The η/Q inconsistency is resolved (η = 0.25, Q = 4.0 throughout the main text). The ka calculation now uses correct canonical parameters. The boundary condition and oblate Ritz analyses have been incorporated. The narrative reframe is successful. Most of the prose-level issues are fixed.

However, I have identified one **near-fatal conceptual gap** and several **numerical inconsistencies** that pervade the paper's headline result. Together, these require a focused but non-trivial revision. The physics is sound, but the numbers are not self-consistent.

---

## Fatal Flaws

### F1. Missing modal participation factor renders the mechanical coupling overestimate by ~2×

This is the most significant remaining issue and was not raised in previous rounds.

The paper's mechanical coupling analysis (§2.5, Eqs. 16–17) treats the abdomen as a single-degree-of-freedom oscillator under base excitation, with the displacement transfer function:

$$H_{\rm rel}(r) = \frac{r^2}{\sqrt{(1-r^2)^2 + (2\zeta r)^2}}$$

At resonance (r = 1), this gives $H_{\rm rel} = Q = 4.0$, so $\xi_{\rm mech} = x_{\rm base} \times Q$. This implicitly assumes that **100% of the base excitation projects onto the n = 2 flexural mode**—i.e., the modal participation factor $\Gamma_2 = 1$.

**This assumption is physically inconsistent with the free-sphere model used for the eigenfrequencies.**

For a free sphere, the mode shapes are Legendre polynomials $P_n(\cos\theta)$. Vertical base excitation produces a radial displacement proportional to $\cos\theta = P_1(\cos\theta)$ on the shell surface. By the orthogonality of Legendre polynomials:

$$\int_{-1}^{1} P_n(u) \, P_1(u) \, du = 0 \qquad \text{for } n \neq 1$$

**Therefore $\Gamma_2 = 0$ exactly for a free sphere.** Pure translational base excitation of a free sphere excites only the rigid-body mode (n = 1) and has zero projection onto any flexural mode (n ≥ 2).

The resolution—which the authors clearly understand, because their code in `modal_participation.py` (lines 86–163) computes exactly this—is that the partially constrained abdomen (spine, pelvis clamping ~33% of the surface) breaks Legendre orthogonality and yields $\Gamma_2 \approx 0.37$–$0.48$ depending on constraint geometry. But **this factor never appears anywhere in the paper text**. The code exists, the physics is implemented correctly, and the numerical answer is available. It simply was never written up.

The consequence: every mechanical displacement in the paper is overestimated by approximately $1/\Gamma_2 \approx 2\times$. This propagates directly into the coupling ratio $\mathcal{R}$ and the headline numbers. For instance, Eq. 30's ratio of $6.6 \times 10^4$ becomes $\sim 3 \times 10^4$ after applying $\Gamma_2 \approx 0.48$. This does not change the qualitative conclusion ($10^4 \gg 1$), but:

1. The paper claims **quantitative** precision (four significant figures in Table 5: "4586 μm", "10549 μm") that it does not possess.
2. The omission undermines §3.5's own boundary condition analysis: that section discusses how BCs affect eigenfrequencies but ignores the more consequential effect on excitation coupling.
3. The `modal_participation.py` code also contains a full "gap budget" analysis that closes the theory-vs-ISO discrepancy from Round 4's M2—again, computed but not reported.

**Action required:** Add a subsection (or expand §2.5) introducing the modal participation factor $\Gamma_n$ for base excitation of a partially constrained shell. Define it, state its value for the assumed constraint geometry, and incorporate it into Eq. 17 as $\xi_{\rm mech} = \Gamma_2 \times x_{\rm base} \times H_{\rm rel}$. Propagate this factor through all tables and the coupling ratio.

---

## Major Issues

### M1. Coupling ratio $\mathcal{R}$ is stated as three to four mutually inconsistent values

The paper's headline number is the coupling ratio $\mathcal{R}$, yet it appears with at least four different numerical values:

| Location | Stated value | Implied definition |
|---|---|---|
| Abstract (line 105) | $4.6 \times 10^4$ | ξ_mech / ξ_air (unspecified levels) |
| Introduction (line 76) | $4.6 \times 10^4$ | Same |
| §2.6, Eq. 18 (line 255) | $\sim 10^3$–$10^4$ | Range |
| §4.3, Eq. 30 (line 89) | $917/0.014 \approx 6.6 \times 10^4$ | 0.1 m/s² vs. 120 dB |
| Table 9 / §dimensional | $7.7 \times 10^3$ | $\approx 1/(ka)^2$, geometric only |
| Discussion (line 7, 357, 460) | $10^3$–$10^4$ | Range |
| Conclusion (line 5, 35) | $4.6 \times 10^4$ and $10^3$–$10^5$ | Mixed |

I have verified computationally that $6.6 \times 10^4$ is correct for the specific comparison in Eq. 30 (ξ_mech at 0.1 m/s² = 917 μm; ξ_air at 120 dB energy-consistent = 0.014 μm). The $4.6 \times 10^4$ claimed in the abstract does not match this calculation or any standard combination of excitation levels I can identify. The $7.7 \times 10^3$ in Table 9 corresponds approximately to $1/(ka)^2$ and is a fundamentally different quantity (the geometric penalty alone, without Q, impedance, or base excitation factors).

A paper whose central contribution is a single number cannot have that number stated inconsistently. This erodes trust in all quantitative claims.

**Action required:** Define $\mathcal{R}$ unambiguously (which excitation levels, which displacement estimate), compute it once with the canonical parameters including the modal participation factor, and use that single value consistently throughout. If different definitions are used in different contexts (geometric penalty vs. full displacement ratio), give them distinct symbols and explain the relationship.

### M2. Table 4 caption contains an incorrect formula

The caption of Table 4 (`section4_coupling.tex`, line 21) states:

> "The pressure-based upper bound overestimates by a factor of $\sqrt{2Q/\zeta_{\rm rad}} \approx 13.4$."

With Q = 4.0 and $\zeta_{\rm rad} \approx 10^{-15}$, this formula evaluates to $\sqrt{8/10^{-15}} \approx 9.4 \times 10^7$, not 13.4. The factor of 13.4 is the correct *numerical* ratio of the two displacement estimates (I verified: $\xi_{\rm pressure}/\xi_{\rm energy} = 0.184/0.0137 = 13.4$), but the given *formula* is wrong by seven orders of magnitude. This is not a rounding issue—the formula is dimensionally suspect and yields a completely different number.

The supplementary material (§S1.5) states the ratio as "approximately 12.9×", which is also inconsistent with 13.4.

**Action required:** Either derive the correct analytical expression for the pressure-to-energy ratio, or simply state it as a numerical result without an incorrect formula.

### M3. Supplementary material has arithmetic errors

Two numerical errors in the supplementary material:

1. **§S1.4** (line 229): states $f_0 \approx 2900$ Hz for the breathing mode. The arithmetic from the supplementary's own preceding expressions ($\sqrt{4.2 \times 10^{10}/171.1}/(2\pi) = 2494$ Hz) gives ~2500 Hz, matching the main text. The value 2900 Hz is simply wrong; it appears to be a transcription error (perhaps from an earlier parameter set).

2. **§S1.4** (line 211): states $k_{\rm shell} \approx 2.3 \times 10^5$ Pa/m. With canonical parameters: $k_{\rm shell} = 2 \times 10^5 \times 0.01 / (0.157^2 \times 0.55) = 1.48 \times 10^5$ Pa/m. The main text correctly states $\sim 1.5 \times 10^5$. The supplementary's value is off by 55%.

These are minor in isolation (k_shell is negligible compared to k_fluid), but in a paper that has gone through five review rounds on parameter consistency, readers will notice.

**Action required:** Correct both numerical values in the supplementary material.

### M4. UQ Table 2 mixes displacement estimate conventions without clear labelling

Table 2 (`results.tex`, line 69–86) reports:
- $\xi_{\rm air}$ at 120 dB: median 0.18 μm (caption says "pressure-based upper bound")
- SPL for PIEZO: 135 dB

But the Discussion (line 76) states that reaching the 1 μm threshold requires ~158 dB, which corresponds to the energy-consistent estimate. The UQ table's 135 dB corresponds to the pressure-based estimate ($120 + 20\log_{10}(1/0.18) \approx 135$ dB), while 158 dB corresponds to the energy-consistent one ($120 + 20\log_{10}(1/0.014) \approx 157$ dB).

A 23 dB disagreement in the PIEZO threshold SPL—between the same paper's UQ table and Discussion—is confusing. The table caption partially addresses this ("energy-consistent value is ~13× smaller"), but the SPL-for-PIEZO row does not specify which estimate it uses.

**Action required:** Either report SPL-for-PIEZO based on the energy-consistent displacement (the physically correct approach), or label the row explicitly as "pressure-based upper bound" and state the energy-consistent value alongside.

### M5. Code default parameters still do not match paper canonical values

All seven parameters in the `AbdominalModel` (natural_frequency.py) and `AbdominalModelV2` (natural_frequency_v2.py) default constructors differ from the paper's Table 1 canonical values:

| Parameter | Code default | Paper canonical |
|---|---|---|
| a | 0.15 m | 0.18 m |
| c | 0.10 m | 0.12 m |
| h | 0.015 m | 0.010 m |
| E | 0.5 MPa | 0.1 MPa |
| ν | 0.49 | 0.45 |
| ρ_w | 1050 kg/m³ | 1100 kg/m³ |
| ρ_f | 1040 kg/m³ | 1020 kg/m³ |

The scripts that generate figures and tables override these defaults, so the paper's numbers are likely correct. However, any reader who `pip install`s the package and runs the modules (as instructed in the Data Availability section) will get results that **do not match any table in the paper**. This was flagged in Round 4 (m6) and remains unfixed.

**Action required:** Update the default parameters in both model classes to match Table 1, or add a `canonical()` classmethod that returns the paper's parameter set.

---

## Minor Issues

### m1. Pre-stress accounts for 45% of total stiffness but receives minimal discussion

I verified that $K_P^{(2)} = 25{,}478$ Pa/m, comprising 45% of $K_{\rm total}^{(2)} = 56{,}388$ Pa/m. The pre-stress from intra-abdominal pressure is not a small correction—it is nearly half the total restoring force. The Sobol sensitivity analysis attributes 86% of variance to E, but this may be because P_iap was varied over a narrower range. Since IAP increases dramatically with posture (supine → standing), Valsalva manoeuvre, or obesity (where chronic IAP can reach 15–25 mmHg), the predicted frequency shifts from 2.9 Hz (P_iap = 0) to 4.8 Hz (P_iap = 2000 Pa) are clinically significant and deserving of explicit discussion. The parameter sensitivity table (Table 2) does not include P_iap as a separate variable.

### m2. Thin-shell condition marginally violated

The paper acknowledges $h/R \approx 0.06$ (§2.1, line 23) and notes the conventional limit is $h/R < 0.05$. The multi-layer model (§3.4) gives $h_{\rm total} = 25.1$ mm, for which $h/R \approx 0.16$—well into the thick-shell regime. The Limitations section (item 4) cites a "~4% Mindlin–Reissner correction," but this applies only to the 10 mm homogeneous wall. For the 25 mm composite wall, the correction would be substantially larger. This limitation should be stated explicitly when presenting the multi-layer results.

### m3. Section 2.4 Eq. 15 references §4 before §4 exists

Section 2.4 (line 209) states "the energy-consistent reciprocity analysis (§\ref{sec:coupling}) gives $\xi_{\rm air} \approx 0.014\,\mu$m" and then says the pressure estimate "yields $\approx 0.18\,\mu$m, an overestimate that violates the energy budget; see §\ref{sec:coupling}." At this point in the paper, §4 has not been reached. A forward reference is acceptable, but presenting two conflicting numbers without the derivation that reconciles them may confuse readers on first reading. Consider adding a brief sentence explaining *why* the pressure estimate is an overestimate (low radiation efficiency), so the reader does not need §4 to follow the logic.

### m4. Table 9 (cross-species scaling) uses f₂ = 3.9 Hz vs. main text 4.0 Hz

Table 9 reports f₂ = 3.9 Hz for the human case, while all other locations in the paper state 4.0 Hz. The actual computed value is 3.95 Hz, so both are rounding artefacts, but using different rounding in different tables is unnecessarily confusing.

### m5. `junger2012sound` bibliography key used in text but bib file has `Junger1986`

The main text cites `\cite{junger2012sound}` (§2.1, line 10; §2.4, line 191) for Junger & Feit, but the `.bib` file (line 39) lists the entry as `Junger1986` with publication year 1986. If the reference is the 2012 reprint, the `.bib` entry should reflect this; if 1986 is correct, the citation key should match. (I cannot verify compilation, but a mismatched key will produce a "?" in the PDF.)

### m6. Highlights line "Coupling disparity of ~$10^4$" is imprecise

The highlights state "$\sim 10^4$" while the abstract says "$4.6 \times 10^4$" and Eq. 30 gives $6.6 \times 10^4$. This further contributes to the inconsistency documented in M1.

---

## Grudging Positive Aspects

1. **The coupling-comparison framework remains the paper's genuine and significant contribution.** The idea of quantifying why two excitation pathways to the same resonance differ by orders of magnitude, using the (ka)^n penalty and energy-consistent reciprocity, is novel and elegant. I have not seen this in the infrasound-physiology literature. If the numbers are made self-consistent, this will be widely cited.

2. **The energy budget analysis (§4.4) is rigorous.** The absorption efficiency of ~10⁻¹⁴ is a memorable and physically transparent result. The reciprocity-based derivation in the supplementary material (Eqs. S13–S17) is correct and well-presented, with the exception of the f₀ arithmetic error.

3. **The gas pocket transducer mechanism (§5.3.1) is genuinely original.** The observation that intestinal gas bypasses the (ka)^n penalty because each pocket responds locally to the full incident pressure is a novel physical insight. The quantitative estimates (0.94 μm at 120 dB for a 2 cm pocket) are testable and explain inter-individual variability. This mechanism alone could justify a separate paper.

4. **The boundary condition and oblate spheroid analyses (§3.5–3.6) directly address prior weaknesses.** The Rayleigh–Ritz results (Table 6, Table 7) are informative and well-presented. The finding that the fluid added mass dominates system inertia (7.4× wall mass), making eigenfrequencies insensitive to BCs, is a clean physical insight.

5. **The uncertainty quantification with Sobol indices is exemplary.** The finding that E accounts for 86% of output variance provides actionable experimental guidance. This is the kind of result that elevates a theoretical paper above pure speculation.

6. **The writing quality is exceptional.** The prose is clear, engaging, and technically precise (when the numbers cooperate). The Discussion section—particularly §5.5 on broader applications—is among the best I have read in a JSV submission. The Limitations section is commendably honest and comprehensive.

7. **The experimental validation proposal (§5.6) is concrete and practical.** Specifying the phantom material (Ecoflex 00-30 to Dragon Skin 10A), predicted frequencies, and a cost estimate (< US$3,100) demonstrates that the authors take validation seriously.

---

## Summary

The paper has matured into a strong contribution to the infrasound-physiology and fluid–structure interaction literature. The qualitative physics is correct and the framing is compelling. However, the quantitative execution has a significant gap (the missing modal participation factor for mechanical coupling) and pervasive numerical inconsistencies in the headline coupling ratio (at least four different values across the manuscript). The Table 4 caption formula is simply wrong, and the supplementary material contains arithmetic errors.

None of these issues are architecturally fatal. The modal participation factor is already computed in the codebase and merely needs to be written up and propagated through the tables. The coupling ratio inconsistency requires choosing one definition and enforcing it consistently. The supplementary arithmetic must be corrected. These are targeted fixes that should take one concentrated revision cycle.

I recommend **Major Revision** rather than Minor because the modal participation factor is a conceptual omission that changes the paper's specific numerical claims, and the coupling ratio inconsistency is too pervasive to be handled as a Minor correction.

Upon satisfactory revision, I expect to recommend acceptance.
