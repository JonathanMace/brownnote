# Paper 2 JASA Express Letter Restructuring Plan

**Author**: Opus (PI)
**Date**: 2026-03-27
**Branch**: paper2-letter-plan
**Triggered by**: Provocateur recommendation (docs/research-logs/provocateur-research-direction.md, line 146)

> "Submit Paper 1 now. Trim Paper 2 to a JASA Letter (4 pages). … The key result
> (ξ ∝ pa/3γP₀) is one equation."

---

## 1. Current State of Paper 2

| Metric | Current (full article) | JASA-EL target |
|--------|----------------------|----------------|
| Format | `\documentclass[12pt]{article}` | `\documentclass` with JASA-EL template |
| Pages (typeset) | ~14 | ≤6 (published); ~4 manuscript |
| Words (est.) | ~5,500 | ~3,000–3,500 |
| Abstract | ~150 words | ≤100 words |
| Sections | 6 + 13 subsections | 5 flat sections |
| Equations | 17 (equation + align) | 5–6 |
| Tables | 2 (params + frequencies) | 1 (merged, spherical only) |
| Figures | 4 | 2 |
| References | 28 unique | ~15–18 |
| Monte Carlo model | 10,000 individuals | Cut (move to supplementary) |

---

## 2. JASA Express Letter Format Requirements

- **Maximum**: 6 published pages (including all figures, tables, references)
- **Abstract**: ≤100 words
- **Template**: JASA-EL LaTeX class from AIP Publishing
- **Single-column**, single-spaced, 10pt font
- **Rapid review**: shorter review cycle than full JASA articles
- **Open access**: JASA-EL is gold open access
- **Supplementary material**: allowed (and recommended for derivations/data)
- **References**: aim for ~15–20; more than half from last 5 years preferred
- **Figures**: keep to 2–3; each costs ~¼ page of real estate

---

## 3. Core Argument (What MUST Stay)

The paper's contribution can be stated in one paragraph:

> Whole-body models predict negligible tissue displacement from airborne
> infrasound (Paper 1: 0.014 µm at 120 dB). But intraluminal gas pockets
> act as impedance-matching transducers: their compressibility converts
> uniform pressure to local wall strain. A constrained-bubble model (Minnaert
> with elastic wall) shows that a 5–100 mL spherical pocket produces
> 0.5–1.3 µm displacement at 120 dB — 35–100× the whole-cavity pathway
> and above the PIEZO2 mechanosensitive ion channel threshold. This is the
> only plausible airborne-infrasound→GI mechanotransduction pathway.

### Essential physics (non-negotiable)
1. **Modified Minnaert equation** (Eq. 6 in current draft → Eq. 1 in letter)
2. **Sub-resonant displacement formula** ξ = p_inc / k_eff (Eq. 10 → Eq. 2)
3. **Effective stiffness** k_eff^(sph) (Eq. 13 → Eq. 3)
4. **SPL threshold formula** (Eq. 16 → Eq. 4)
5. **PIEZO threshold criterion** ξ_PIEZO = 0.5 µm (stated, not derived)

### Essential results (non-negotiable)
- Table 2 (resonance frequencies) — **spherical rows only** (6 rows → fits in ¼ page)
- SPL threshold range: 111–120 dB for 5–100 mL spherical pockets
- 35–100× efficiency gain over whole-cavity pathway
- The 0.014 µm vs 1.3 µm comparison at 120 dB

### Essential caveats (non-negotiable)
- Acoustic short-circuit via GI air column (2–3 sentences, not a full subsection)
- In vivo threshold uncertainty for PIEZO channels

---

## 4. What Gets Cut or Moved to Supplementary

### Cut entirely (not in supplementary)
| Section/Content | Reason |
|----------------|--------|
| §2.1 Geometry subsection | Unnecessary — one sentence in theory sufficient |
| Cylindrical geometry equations (Eqs. 7–9, 14) | Provocateur: "cylindrical correction barely matters" |
| §2.3 Damping (4 damping terms) | Sub-resonant → damping irrelevant (H→1). One sentence. |
| §2.5 Volume displacement / monopole (Eqs. 15–16) | Near-field decay is obvious; not needed for threshold |
| §3.1 Resonance frequency results for cylindrical pockets | Spherical-only table is sufficient |
| §4.3 Comparison with bubble dynamics | Interesting but tangential |
| §4.4 Limitations items 1–3 (linear model, idealised geometry, quasi-static) | Standard caveats; one sentence covers all |
| Table 1 (model parameters) | Inline the 3 key values (E_w, h_w, ρ_f) |
| Fig. 1 (geometry schematic) | Self-explanatory for JASA audience |
| Fig. 3 (4-panel Monte Carlo population) | Overkill; see below |

### Move to supplementary material
| Content | Why supplementary |
|---------|------------------|
| §2.6 Monte Carlo population model | "If 100% exceed threshold, you don't need 10,000 samples" — keep 2-sentence summary in main text |
| Fig. 3 (population variability) | Support the "nearly all exceed threshold" claim without occupying main-text space |
| Cylindrical geometry derivation | For completeness; spherical is the leading-order story |
| Full parameter table (Table 1) | Reference in supplementary for reproducibility |
| Damping derivation details | For readers who want to verify H(ω) ≈ 1 claim |

---

## 5. Proposed JASA-EL Structure

### Abstract (≤100 words)

Draft target (~95 words):
> Whole-body acoustic models predict negligible tissue displacement from
> airborne infrasound. We show that intraluminal gas pockets act as
> impedance-matching transducers, converting pressure to local wall strain
> via sub-resonant compliance. A constrained-bubble model (modified Minnaert
> frequency with elastic intestinal wall) predicts that 5–100 mL gas pockets
> produce 0.5–1.3 µm wall displacement at 120 dB and 7 Hz — 35–100×
> larger than the whole-cavity pathway and above the PIEZO2 mechanosensitive
> ion channel threshold. Gas-pocket transduction is the only plausible
> mechanism for airborne infrasound-induced gastrointestinal mechanotransduction.

### I. Introduction (½ page, ~400 words)

Structure:
1. **Opening hook** (2 sentences): "Brown note" myth + lack of evidence
2. **Paper 1 result** (2 sentences): Whole-cavity resonance fails — 0.014 µm at 120 dB, need >180 dB
3. **The neglected physics** (3 sentences): GI tract contains 100–200 mL of gas in discrete pockets. Gas = compressible inclusion in incompressible medium. Impedance mismatch of 3600:1.
4. **This paper's contribution** (2 sentences): Constrained-bubble model → SPL thresholds → PIEZO activation. 35–100× more efficient than whole-cavity.

References: Jauchem2007, Leventhall2007, Mohr1965, vonGierke1974, Levitt1971, Suarez1997, Bedell1956 (~7)

### II. Theory (1 page, ~800 words)

**A. Modified Minnaert frequency** (~¼ page)
- State the spherical constrained-bubble model in one paragraph
- Key equation: f₀ with K_gas, K_wall, M_fluid, M_wall (current Eq. 6)
- Note: K_wall contributes <2.5% → gas compressibility dominates
- State parameter values inline: E_w = 10 kPa, h_w = 3 mm, ρ_f = 1020 kg/m³

**B. Sub-resonant forced response** (~¼ page)
- Key insight: mechanism is compliance, not resonance
- ξ = p_inc / k_eff (current Eq. 10) with H(ω) → 1 for f ≪ f₀
- k_eff^(sph) expression (current Eq. 13)
- One sentence: damping is irrelevant in sub-resonant regime

**C. PIEZO activation threshold** (~¼ page)
- ξ_PIEZO = 0.5 µm (Coste et al. 2010, conservative)
- SPL_thresh formula (current Eq. 16)
- p_inc = p_ref × 10^(S/20)

**D. Comparison baseline** (~¼ page)
- Paper 1 result: ξ = 0.014 µm (energy-consistent) at 120 dB for n=2 flexural mode
- Efficiency ratio = ξ_gas / ξ_cavity = 35–100× depending on pocket volume

**Equations budget**: 4–5 equations total (f₀, ξ, k_eff, SPL_thresh, p_inc)

### III. Results (1 page, ~600 words)

**A. Resonance frequencies** (~⅓ page)
- Table: spherical pockets only, 5 rows (1, 5, 10, 50, 100 mL)
- Key finding: all f₀ > 600 Hz → well above infrasound → sub-resonant regime confirmed
- One sentence: cylindrical axial modes reach ~31 Hz (see supplementary)

**B. SPL threshold for PIEZO activation** (~⅓ page)
- **Figure 1** (replaces current Fig. 2): SPL threshold vs volume, spherical only
  - Threshold: 120 dB (5 mL) → 111 dB (100 mL)
  - 9-dB range maps to inter-individual gas variability
  - Horizontal lines: 120 dB (pain), 140 dB (jet engine)

**C. Pathway comparison** (~⅓ page)
- **Figure 2** (replaces current Fig. 4): displacement vs SPL, gas pocket vs whole-cavity
  - 100 mL pocket: 1.3 µm at 120 dB vs whole-cavity: 0.014 µm
  - Gas pocket crosses PIEZO threshold at ~111 dB; whole-cavity needs >180 dB
  - Quote the 35–100× ratio explicitly

### IV. Discussion (½ page, ~400 words)

Structure:
1. **Impedance-matching transducer analogy** (3 sentences): Middle ear analogy — compliance mismatch converts pressure to displacement at interface where PIEZO channels reside
2. **Acoustic short-circuit caveat** (4 sentences): GI tract is open tube → luminal air could equalize pressure. But liquid plugs segment the tract → gas pockets are acoustically isolated in vivo. Helmholtz estimate: f_H ≈ 15 Hz. Partial equalization at f < f_H but still above PIEZO threshold for pockets >20 mL.
3. **Clinical implications** (4 sentences): IBS patients (elevated gas + visceral hypersensitivity), post-prandial states, SIBO → enhanced susceptibility. Explains sporadic/individual nature of reported infrasound GI effects. Gas content varies 15× across population.
4. **Testable predictions** (3 sentences): SPL threshold should correlate with gas content (measurable by X-ray/CT). Simethicone should attenuate. Effect should be broadband.

### V. Conclusion (¼ page, ~150 words)

- Gas pockets = impedance-matching acoustic transducers
- 35–100× more efficient than whole-cavity
- Only plausible airborne infrasound → GI mechanotransduction pathway
- SPL threshold: 111–120 dB (physiological pocket range)
- Predictions amenable to experimental validation

---

## 6. Figure Plan

### Keep (2 figures)
| Letter fig. | Current fig. | Content | Modifications |
|-------------|-------------|---------|---------------|
| Fig. 1 | Fig. 2 | SPL threshold vs volume | Remove cylindrical curve; spherical only; simplify |
| Fig. 2 | Fig. 4 | Pathway comparison (displacement vs SPL) | Keep as-is; this is the money plot |

### Cut from main text
| Current fig. | Disposition |
|-------------|-------------|
| Fig. 1 (schematic) | Cut — JASA audience knows bubble dynamics |
| Fig. 3 (Monte Carlo 4-panel) | Move to supplementary |

---

## 7. Reference Triage

### Keep (~16 references)
| Ref | Role |
|-----|------|
| Minnaert1933 | Foundational — Minnaert frequency |
| Leighton1994 | Bubble acoustics textbook |
| Church1995 | Encapsulated bubble dynamics |
| Hoff2000 | Shell-bubble oscillation |
| Levitt1971 | Bowel gas physiology (volume) |
| Suarez1997 | Gas composition/distribution |
| Bedell1956 | Gas volume measurements |
| Serra2001 | Gas dynamics and tolerance |
| Coste2010 | PIEZO channels (Nobel Prize work) |
| Alcaino2017 | PIEZO2 in enteric neurons |
| Zeitzschel2024 | Recent mechanotransduction review |
| Leventhall2007 | Infrasound review |
| Mohr1965 | Early infrasound-GI evidence |
| vonGierke1974 | NASA infrasound report |
| Fung1993 | Tissue biomechanics |
| Junger1986 | Acoustic impedance matching |

### Move to supplementary or cut
| Ref | Reason |
|-----|--------|
| Commander1989 | Bubbly liquids — tangential |
| Plesset1977 | Cavitation — not relevant to linear model |
| Prosperetti1988 | Ocean bubbles — not cited in core argument |
| Gregersen2000 | GI biomechanics — only needed if full parameter table included |
| Higa2007 | Colon tissue properties — supplementary |
| Kitazaki1998 | Seated body resonance — Paper 1 territory |
| Griffin1990 | Human vibration handbook — Paper 1 territory |
| iso2631 | WBV standard — not relevant to gas pocket model |
| Jauchem2007 | Military acoustics — cut (Leventhall covers it) |
| Iovino2006 | Sympathetic nervous system — tangential |
| Harder2003 | Gas distribution and symptoms — supplementary |
| Mazzuoli2015 | Enteric neurons — Alcaino2017 covers it |

---

## 8. Supplementary Material Contents

The supplementary PDF should contain:

1. **Full parameter table** (current Table 1)
2. **Cylindrical geometry derivation** (Eqs. 7–9, 14) + cylindrical rows from Table 2
3. **Damping model details** (Eq. 5 and the four δ terms)
4. **Monte Carlo population model** description + Fig. 3 (4-panel)
5. **Volume displacement and monopole decay** (Eqs. 15–16)
6. **Extended limitations discussion**

Estimated supplementary length: 4–5 pages.

---

## 9. Effort Estimate

| Task | Est. hours | Notes |
|------|-----------|-------|
| Install JASA-EL LaTeX template | 0.5 | Download from AIP Publishing |
| Rewrite abstract (≤100 words) | 0.5 | Tight editing pass |
| Rewrite Introduction | 1.0 | Cut from 48 lines to ~25 |
| Rewrite Theory | 1.5 | Merge 6 subsections into 4 paragraphs |
| Rewrite Results | 1.0 | Spherical only; 1 table + 2 figures |
| Rewrite Discussion | 1.0 | 4 focused paragraphs |
| Rewrite Conclusion | 0.5 | Tighten to 5 bullet points as prose |
| Prepare supplementary | 1.5 | Migrate cut content |
| Regenerate figures | 1.0 | Remove cylindrical from Fig. 2; reformat |
| Reference cleanup | 0.5 | Trim to ~16 |
| Internal review (consistency-auditor) | 0.5 | Parameters, numbers |
| Reviewer panel (A, B, C) | 1.0 | Quick pass on letter draft |
| **Total** | **~10 hours** | |

---

## 10. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Referee says "too brief, need more derivation" | MEDIUM | Supplementary contains full derivation; cite it |
| JASA-EL scope mismatch (not enough "acoustics") | LOW | Core is Minnaert bubble dynamics — classic JASA |
| Acoustic short-circuit objection dominates review | HIGH | Address explicitly in Discussion; acknowledge honestly |
| Overlap with Paper 1 flagged as duplicate | LOW | Different mechanism, different journal, cross-reference |
| Loss of cylindrical results weakens generality claim | LOW | Mention in supplementary; spherical is conservative |

---

## 11. Key Decision Points for PI

1. **Spherical-only or keep cylindrical in main text?**
   Recommendation: Spherical only. Cylindrical adds complexity without changing the conclusion (provocateur: "cylindrical correction barely matters"). Supplementary has the cylindrical derivation.

2. **Keep Monte Carlo in main text?**
   Recommendation: No. One sentence ("Nearly all simulated individuals exceed the threshold; see supplementary") suffices. The 100% exceedance rate is a consequence of the model, not an independent finding.

3. **Include the middle-ear analogy?**
   Recommendation: Yes, but one sentence only. It's the most intuitive way to explain impedance matching for the JASA audience.

4. **Acoustic short-circuit: how much space?**
   Recommendation: 4 sentences in Discussion + 1 sentence in Conclusion. This is the most likely reviewer objection; it needs honest acknowledgement but not a full subsection.

5. **Submit before or after Paper 1 acceptance?**
   Recommendation: After. Paper 2 cites Paper 1 results (0.014 µm, 66,000× coupling ratio). Submitting simultaneously risks "see companion paper" objections from reviewers who can't access it.

---

## Next Steps

1. PI approves this plan (or modifies)
2. Create `paper2-gas-pockets/letter/` directory for JASA-EL version
3. Download and configure JASA-EL LaTeX template
4. Draft letter version following this outline
5. Regenerate Fig. 1 (SPL threshold, spherical only) and Fig. 2 (pathway comparison)
6. Prepare supplementary material PDF
7. Run consistency-auditor on letter draft
8. Run 3-reviewer panel
9. Submit after Paper 1 is accepted
