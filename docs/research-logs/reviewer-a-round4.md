# Reviewer A — Round 4

**Date:** 2026-03-27
**Reviewer:** A (Structural Acoustics / Vibroacoustics, 20+ years, JSV editorial board experience)
**Manuscript:** "Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for the Existence of the Brown Note"
**Target journal:** Journal of Sound and Vibration

---

## Overall Assessment

This is a genuinely enjoyable and intellectually serious paper disguised as a novelty investigation. The authors take a folklore claim — that airborne infrasound can cause involuntary bowel movements — and use it as a lens to examine a real gap in the vibroacoustics literature: the quantitative comparison of airborne acoustic vs. mechanical vibration coupling to soft biological shells. The central result — a 10³–10⁴ coupling disparity arising from elementary long-wavelength acoustics — is clean, physically transparent, and surprisingly useful.

The paper has improved enormously over prior rounds. The energy-consistent reciprocity analysis (§4.4), the Rayleigh–Ritz oblate spheroid correction (§3.6), the multi-layer wall model (§3.4), and the Monte Carlo UQ (§3.3) are all substantive additions that elevate this from a "back-of-the-envelope debunking" to a proper analytical framework. The gas pocket and orifice coupling analysis in §5.3 is a particularly valuable addition — it provides a mechanistically credible explanation for sporadic anecdotal reports without undermining the main conclusion.

That said, several issues of framing, positioning, and completeness prevent me from recommending acceptance in its current form. The paper undersells its own contributions, misses opportunities to connect with active research communities, and still has some structural roughness. I believe a **minor revision** addressing the points below would produce a strong JSV paper.

**Recommendation: MINOR REVISION**

---

## Significance and Novelty

### The novelty claim needs sharpening

The paper frames its contribution as threefold (Introduction, items 1–3): first-principles eigenfrequencies, airborne coupling quantification, and airborne-vs-mechanical comparison. This is accurate but undersold. Let me articulate what I think the *actual* intellectual contributions are, because the authors should say this more clearly:

1. **The two-family mode taxonomy for biological shells.** The separation of breathing modes (fluid-dominated, kHz) from flexural modes (shell-dominated, Hz) is well-known for engineering shells (Junger & Feit, Soedel), but the authors apply it to a *biological* cavity with the specific insight that the extraordinary stiffness ratio ($k_\mathrm{fluid}/k_\mathrm{shell} \sim 10^5$, below Eq. 6) makes the mode separation vastly wider than in typical engineering structures. This is worth stating explicitly. In a submarine hull, both families are in the audible range; in the abdomen, they're separated by three decades. That's a new observation.

2. **The $(ka)^n$ coupling penalty as the resolution of a literature paradox.** The airborne-vs-WBV coupling disparity is the paper's strongest contribution. But the framing as "debunking the brown note" is self-limiting. What the authors have actually shown is that *any* attempt to excite flexural resonances of a body-scale biological cavity via airborne sound at frequencies below ~50 Hz is futile — not just the brown note, but any hypothesised infrasonic bioeffect operating through global cavity resonance. This is a much more important and citable result. I return to this below.

3. **The gas pocket mechanism as a local transducer.** Section 5.3.1 identifies intestinal gas pockets as quasi-static pressure-to-displacement converters that bypass the $(ka)^n$ penalty. This is, to my knowledge, a novel observation in the infrasound context, and it provides a testable hypothesis for inter-individual variability. The authors could elevate this from a discussion footnote to a headline result.

### The "so what?" question

Who would cite this paper, and why? In its current framing, the answer is: people interested in the brown note (a small audience) and people working on WBV health effects (ISO 2631 community). But the analytical framework is applicable to a much wider set of problems:

- **Blast injury to abdominal organs.** The coupling analysis directly applies to primary blast injury, where the question "does the airborne blast wave excite abdominal resonance, or does the whole-body displacement dominate?" is of urgent clinical interest. The $(ka)^n$ framework provides a frequency-dependent answer. The authors should cite the blast injury literature (e.g., Stuhmiller et al. 1996, Courtney & Courtney 2015) and note the applicability.

- **Diagnostic and therapeutic ultrasound.** The modal framework for a fluid-filled viscoelastic oblate shell is relevant to elastography and acoustic radiation force imaging (ARFI), where excitation of tissue modes is the objective rather than the obstacle.

- **Fetal monitoring and obstetric acoustics.** The fluid-filled oblate spheroid geometry is a reasonable first-order model for the gravid uterus. The mode taxonomy directly applies.

- **Marine biology.** Fish swim bladders are fluid-filled shells that couple to ambient sound; the $(ka)^n$ analysis applies with different impedance ratios.

The paper should include a paragraph in the Discussion articulating at least two of these broader applications. This is not padding — it is the difference between a paper that gets 5 citations and one that gets 50.

---

## Major Suggestions (would substantially improve the paper)

### MS1. Reframe the title and abstract around the coupling disparity, not the brown note

The brown note hook is fun and it draws readers in, but it also risks the paper being dismissed as a novelty item. The *actual* contribution — quantifying the coupling disparity between airborne and mechanical excitation of biological cavities — is a general-purpose result. I suggest the title be modified to foreground the physics:

> "Airborne vs. Mechanical Coupling to Flexural Modes of a Fluid-Filled Viscoelastic Shell: Why Infrasound Cannot Excite Abdominal Resonance"

The brown note can appear in the abstract and introduction as the motivating example. Keep the wit — the writing is excellent — but let the physics carry the title.

### MS2. The energy-consistent analysis deserves promotion to a main result

The reciprocity-based absorption cross-section analysis (§4.4) is currently presented as a "verification" of the pressure-based coupling estimate. But it is actually the more rigorous result. The pressure-based approach (Eq. 16–18) is a useful approximation, but the energy budget (§4.4) is self-consistent. I would:

1. Present the energy-consistent displacement as the **primary** airborne coupling result in Table 3 (currently it shows both, which is good, but the "energy" column should be labelled as the recommended value).
2. In §2.5, after Eq. 18, add a sentence: "This estimate is an upper bound; the energy-consistent analysis of §4.4 yields a displacement approximately 13× smaller."
3. Make the absorption efficiency $\sim 10^{-14}$ a highlighted result, not buried in a paragraph. This single number is extraordinarily vivid.

### MS3. Articulate broader applications in the Discussion

As noted above, the framework is portable to blast injury, diagnostic ultrasound, obstetric acoustics, and marine bioacoustics. A subsection "§5.X: Applicability to Other Fluid-Filled Biological Cavities" would substantially increase the paper's appeal and citation potential. Even a half-page would suffice: state the geometry, note the impedance ratios, and point out what changes.

### MS4. The Rayleigh–Ritz oblate correction (§3.6) needs better integration

Table 5 (oblate correction) is an important result — the sphere model overestimates by 11–20% — but it's presented as a standalone subsection and then the paper goes back to using sphere-based numbers everywhere else. The authors should either:

(a) Use the Ritz-corrected frequencies as the canonical values throughout (preferable), or
(b) Present a clear "correction factor" $\kappa(c/a)$ and apply it consistently, noting it doesn't change the coupling ratio.

Currently, the reader doesn't know which number to trust.

### MS5. Address the parameter consistency issue flagged by Reviewer B (Round 3, F1)

I have read Reviewer B's Round 3 report. The finding that Table 1 parameters ($h = 10$ mm, $\nu = 0.45$) differ from the code defaults ($h = 15$ mm, $\nu = 0.49$) is a serious reproducibility concern. Even if the numbers have since been reconciled (I note the current manuscript does specify $h = 10$ mm, $\nu = 0.45$, and $\eta = 0.25$ in Table 1, but the abstract says "breathing mode at 2500 Hz" while §2.2 says "approximately 2900 Hz"), there remain small inconsistencies. The authors must run a single canonical script from Table 1 parameters and verify every number in the manuscript against its output. This is a prerequisite for JSV publication.

---

## Minor Suggestions

### ms1. The historical-notes section is unused

The file `historical-notes.tex` contains excellent material (Gavreau, Mohr et al., von Gierke) that is not `\input{}` anywhere in the manuscript. This historical context should be incorporated into §1 — it strengthens the argument that the brown note has "never been properly examined" by showing what *was* examined and how it differs.

### ms2. Notation inconsistency: $f_2$ vs. $f_{n=2}$

The text alternates between $f_2$ and $f_{n=2}$. Pick one and be consistent.

### ms3. Eq. 11 (added mass) lacks a derivation or citation

The formula $m_\mathrm{add}^{(n)} = \rho_f R / n$ is stated without proof. This is the Lamb (1882) result for an inviscid fluid interior to a sphere, but it deserves a one-line derivation or a clear citation to Lamb §3 or Junger & Feit §7.4.

### ms4. Table 2 (E-sweep): show the Ritz-corrected frequencies alongside

This would immediately show the reader that the qualitative story (relaxed muscle → ISO 2631 range) is robust to the oblate correction.

### ms5. Figure quality: Fig. 3 (coupling comparison)

The left panel is dense and the resonance peaks overlap visually. Consider a log-scale y-axis, which would make the four-order-of-magnitude gap immediately legible. The right panel (bar chart at $n=2$) is excellent — consider making it the full-width figure and demoting the left panel to supplementary.

### ms6. The Kelvin–Voigt model (Eq. 2) is frequency-independent $\eta$

Real soft tissue exhibits frequency-dependent viscoelasticity (power-law or fractional-order models; see Szabo & Wu 2000, JASA). A sentence acknowledging this and noting that $\eta$ = const. is a low-frequency approximation would preempt reviewer objections.

### ms7. Equation numbering

Some equations in §2 are numbered and some aren't (e.g., the base-displacement formula Eq. 14 is numbered but the base-excitation FRF Eq. 15 is also numbered, while the coupling ratio in §2.7 repeats the label of Eq. 16 from §4). Check for duplicate labels.

### ms8. The Q = 4.0 in Table 3 vs. $\eta$ = 0.25 in Table 1

$Q = 1/\eta = 4.0$ is consistent with $\eta = 0.25$, but the baseline $\eta$ in Table 1 is listed as 0.25 while the text below Eq. 2 says "baseline value $\eta = 0.30$." This is contradictory — one of these must be corrected. (Note: the code's `AbdominalModelV2` default is `loss_tangent = 0.3`, adding further confusion.)

---

## Missing References or Comparisons

The reference list is adequate for shell theory and infrasound, but misses several relevant bodies of work:

1. **Blast overpressure and abdominal injury.** Stuhmiller et al. (1996, *J. Trauma*) and Courtney & Courtney (2015, *Shock Waves*) address the same fundamental question — does airborne pressure couple to abdominal organs? — in a context where the answer matters for body armor design. The coupling framework in the present paper is directly applicable and would broaden the citation network.

2. **Acoustic radiation force in tissue.** Nightingale et al. (2002, *Ultrasound in Med. & Biol.*) and Palmeri et al. (2005, *JASA*) use focused ultrasound to excite tissue modes; the reciprocity framework connects.

3. **Fish swim bladder acoustics.** Sand & Karlsen (2000, *Comp. Biochem. Physiol.*) and Popper & Fay (2011, *Springer Handbook*) treat the swim bladder as a pressure-to-displacement transducer — essentially the same physics as the gas pocket analysis in §5.3.1.

4. **Frequency-dependent tissue viscoelasticity.** Szabo & Wu (2000, *JASA*) or Sinkus et al. (2005, *MRM*) for justification of the constant-$\eta$ approximation at low frequency.

5. **Shell vibrations with partial boundary constraints.** Kang & Leissa (2005, *JSV*) provide exact solutions for spherical shells with various edge conditions — this would directly address the boundary condition limitation (§5.4, item 3).

6. **Soedel (2004)** is cited but Leissa's NASA monograph (already in the bib) is underused. The mode-splitting estimate for oblate shells in §5.4.5 could be tightened with reference to Leissa's tabulated results.

---

## What I Liked

1. **The writing.** This is one of the best-written technical papers I've reviewed in years. Sentences like "one part in a hundred trillion of the incident acoustic energy — a figure that puts the brown note hypothesis on rather thin thermodynamic ice" and "one might reasonably conclude that hearing loss would present a more urgent clinical concern than any intestinal disturbance" are genuinely delightful. JSV papers are not usually fun to read; this one is. *Do not lose this voice in revision.*

2. **The two-pathway comparison.** The airborne-vs-WBV framing in §4 is a model of how to present a negative result constructively. Rather than simply saying "it doesn't work," the authors show *why* it doesn't work and *what does* work, resolving a real paradox in the occupational health literature.

3. **The gas pocket mechanism.** Section 5.3.1 is the kind of analysis that spawns follow-up studies. The observation that intestinal gas pockets act as local pressure transducers, bypassing the $(ka)^n$ penalty, is novel and testable. The connection to inter-individual variability via bowel gas content is inspired.

4. **The Monte Carlo UQ.** The Sobol sensitivity analysis (§3.3, Fig. 6) showing that E accounts for 86% of the output variance is a crisp result with direct experimental implications ("measure the wall stiffness"). This is how UQ should be used — not just to attach error bars, but to guide future experiments.

5. **The oblate Rayleigh–Ritz analysis.** The `oblate_spheroid_ritz.py` implementation is technically sound (proper Gauss–Legendre quadrature, oblate spheroidal fluid added mass via Legendre functions, 2-DOF variational formulation). The sphere-limit convergence check is good practice.

6. **Intellectual honesty.** The limitations section (§5.4) is unusually thorough for a first-submission paper. The authors identify eight specific limitations and assess the likely direction of each one's effect on the conclusions. This builds credibility.

---

## Summary Recommendation: MINOR REVISION

The physics is sound, the central result is novel and useful, and the writing is excellent. The paper needs:

1. Sharper framing of the novelty claim (coupling disparity > brown note debunking)
2. Broader applications paragraph to increase citability
3. Integration of the oblate Ritz correction into the canonical results
4. Resolution of all parameter-consistency issues (Table 1 vs. code vs. in-text values)
5. Incorporation of historical-notes material into the Introduction
6. Several missing references to connect with blast injury, ultrasound, and marine bioacoustics communities

None of these require new analysis — they are framing, integration, and polishing tasks. With these changes, I would expect to recommend acceptance.
