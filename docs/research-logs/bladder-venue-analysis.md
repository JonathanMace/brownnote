# Bladder Resonance Paper — Publication Venue Analysis

**Author**: Opus (PI)
**Date**: 2026-03-27
**Branch**: bladder-m5-venue
**Context**: Reviewer A Major Issue M5 — "Is JSV the right target?"

## Summary

This analysis evaluates five candidate journals for the bladder resonance paper,
which models the urinary bladder as a fluid-filled viscoelastic shell and
predicts fill-volume-dependent modal frequencies (n=2 mode: 14–17 Hz) with a
non-monotonic U-shaped curve. The paper's unique contribution is the
competing-stiffness mechanism (geometric softening vs strain-stiffening) that
produces a frequency minimum at ~220 mL coinciding with the clinical urgency
threshold. It is computational-only with no experimental validation.

---

## Venue Comparison Matrix

| Criterion | JSV | J Biomech | JASA | Med Eng Phys | IJMS |
|-----------|-----|-----------|------|--------------|------|
| **IF (2025)** | 4.9 | 2.4 | 2.3 | 2.3–2.8 | 9.4 |
| **Quartile** | Q1 (Acoustics, Mech Eng) | Q1 (Biomed Eng) | Q1–Q2 (Acoustics) | Q2–Q3 (Biomed Eng) | Q1 (Mech Eng) |
| **Scope fit** | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ |
| **Comp-only OK?** | Yes | Yes (with justification) | Yes | Yes | Discouraged |
| **Review timeline** | 2–4 months | 2–4 months | 2–4 months | 3–5 months | 2–3 months |
| **Citation synergy** | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ★☆☆☆☆ |
| **Clinical audience** | ★★☆☆☆ | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★☆☆☆☆ |
| **Formatting** | Elsevier (elsarticle) | Elsevier (elsarticle) | AIP (own template) | Elsevier (elsarticle) | Elsevier (elsarticle) |

---

## Detailed Assessment

### 1. Journal of Sound and Vibration (JSV)

**Impact Factor**: 4.9 (Q1 in Acoustics, Mechanics, Mech Eng)

**Scope fit**: Strong. JSV publishes on vibration analysis, structural
dynamics, and computational mechanics, including biomechanical vibrations. The
bladder shell model — Lamb flexural modes, fluid–structure coupling, parametric
frequency analysis — is squarely within JSV's remit.

**Strengths**:
- **Companion paper synergy**: Paper 1 (brown note, abdominal cavity) is
  targeted at JSV. Paper 3 (scaling laws) is a JSV Short Communication. The
  bladder paper extends the same analytical framework to a different organ,
  creating a coherent series. Cross-citation between three JSV papers from the
  same group strengthens all of them.
- **Reviewer expertise**: JSV reviewers understand shell theory, fluid-loaded
  vibration, and modal analysis. They will evaluate the structural acoustics
  contribution on its merits rather than struggling with the mechanics.
- **Same LaTeX template**: `elsarticle` class already set up; no reformatting
  needed. Line numbering, `siunitx`, `booktabs` all compatible.
- **Computational-only papers accepted**: JSV regularly publishes purely
  analytical/computational work without experimental validation.
- **High IF (4.9)**: Strongest among all candidates.

**Weaknesses**:
- **Salami-slicing risk**: Reviewer B already flagged this (M5) — identical
  equations with parameter substitution. If the same JSV editor handles all
  three papers, they may see diminishing novelty.
- **Clinical narrative diluted**: JSV reviewers will not evaluate the
  "vibration-induced urgency" clinical hypothesis as rigorously (or as
  enthusiastically) as a biomechanics audience would.
- **Audience mismatch for clinical impact**: Urologists and occupational health
  researchers do not read JSV. The paper's most actionable finding (U-shaped
  curve, 220 mL urgency coincidence) would reach the wrong audience.

**Verdict**: Technically excellent fit, but wastes the clinical angle.

---

### 2. Journal of Biomechanics

**Impact Factor**: 2.4 (Q1 in Biomedical Engineering)

**Scope fit**: Strong. J Biomech covers musculoskeletal, cardiovascular, and
soft tissue biomechanics. Bladder wall mechanics, fill-volume parametrics, and
the clinical bridge to vibration-induced urgency are all within scope.

**Strengths**:
- **Clinical audience**: Read by biomechanists, rehabilitation engineers,
  urologists, and occupational health researchers — exactly the people who care
  about "why does WBV cause urgency?"
- **Clinical narrative is the selling point**: The U-shaped frequency curve,
  the 220 mL coincidence with urgency onset, and the 6,500× mechanical
  coupling advantage are clinically actionable findings. J Biomech reviewers
  will appreciate this more than JSV reviewers.
- **Computational-only accepted**: The journal explicitly states it accepts
  "analytical, as well as experimental papers." Justification for lack of
  experimental validation is expected but not disqualifying.
- **Same publisher (Elsevier)**: `elsarticle` template compatible; minimal
  reformatting.
- **Differentiates from Papers 1 & 3**: Publishing in a different venue
  signals that this paper has a distinct contribution (clinical biomechanics)
  rather than being a parameter-substitution appendix.

**Weaknesses**:
- **Lower IF (2.4 vs 4.9)**: Significant drop from JSV. May matter for
  career metrics.
- **Reviewer expertise gap**: J Biomech reviewers may not be fluent in shell
  vibration theory, Lamb modes, or fluid-loaded structural dynamics. Risk of
  misunderstanding the acoustics contribution.
- **Weaker citation synergy**: Papers 1 and 3 in JSV will not cross-cite as
  naturally with a J Biomech paper.

**Verdict**: Best audience fit. IF penalty is real but offset by impact.

---

### 3. Journal of the Acoustical Society of America (JASA)

**Impact Factor**: 2.3 (Q1 Audiology, Q2 Acoustics)

**Scope fit**: Moderate. JASA covers bioacoustics and bioresponse to vibration,
which includes bladder mechanics under vibration exposure. However, the paper's
primary contribution is structural shell dynamics, not acoustics per se.

**Strengths**:
- **Paper 2 synergy**: The gas-pockets paper (Paper 2) is at JASA. Having
  two papers in the same journal creates some synergy.
- **Bioacoustics section**: JASA has a dedicated section for biological
  response to vibration, which is technically applicable.

**Weaknesses**:
- **Three papers is too many**: Papers 1 and 3 at JSV, Paper 2 at JASA.
  Adding the bladder paper to JASA gives us two papers at the same journal
  with overlapping methodology. Reviewers may view this as flooding.
- **Poor scope match**: The paper is about shell mechanics and clinical
  biomechanics, not acoustics. The airborne coupling pathway is shown to be
  negligible (6,500× weaker than mechanical). A paper that concludes
  "acoustics doesn't matter" is a poor fit for an acoustics journal.
- **Lower IF (2.3)**: Below both JSV and IJMS.
- **Different template**: AIP Publishing uses its own LaTeX template,
  requiring full reformatting from `elsarticle`.

**Verdict**: Poor fit. The paper's conclusion undermines the journal's focus.

---

### 4. Medical Engineering & Physics

**Impact Factor**: 2.3–2.8 (Q2–Q3 in Biomedical Engineering)

**Scope fit**: Moderate. Covers biomechanics, computational modelling, and
rehabilitation engineering. Bladder resonance under vibration exposure could
fit as an applied biomedical engineering study.

**Strengths**:
- **Applied engineering focus**: The paper's occupational health implications
  (truck drivers, forklift operators, WBV exposure) align with Med Eng Phys's
  applied emphasis.
- **Computational modelling accepted**: Explicitly within scope.
- **Same publisher (Elsevier)**: Compatible template.

**Weaknesses**:
- **Lower prestige**: Q2–Q3 ranking, IF 2.3–2.8. Neither the highest IF nor
  the best audience reach.
- **Neither fish nor fowl**: Less acoustics expertise than JSV/JASA, less
  biomechanics prestige than J Biomech. Does not excel in either dimension.
- **Slower review**: Reports suggest 3–5 months typical turnaround.
- **Weaker citation synergy**: No companion papers at this venue.

**Verdict**: Acceptable fallback, but not optimal for any criterion.

---

### 5. International Journal of Mechanical Sciences (IJMS)

**Impact Factor**: 9.4 (Q1 in Mechanics and Mechanical Engineering)

**Scope fit**: Weak. IJMS focuses on computational and structural mechanics
in engineering contexts. While shell mechanics is in scope, the biological
application and clinical narrative are outside their typical readership.

**Strengths**:
- **Highest IF (9.4)**: By far the most prestigious journal considered.
- **Shell mechanics expertise**: Reviewers would understand the structural
  dynamics perfectly.

**Weaknesses**:
- **Experimental validation expected**: IJMS explicitly discourages "purely
  mathematical or computational techniques unless directly applied to
  engineering problems." A biological shell with no experimental validation
  is a tough sell.
- **No clinical audience**: IJMS readers are mechanical engineers, not
  biomechanists or clinicians. The urgency hypothesis would be lost.
- **No citation synergy**: No companion papers at IJMS.
- **Scope mismatch**: Bladder mechanics is too far from IJMS's core
  engineering applications (metals, composites, manufacturing).

**Verdict**: IF is tempting but scope mismatch is disqualifying.

---

### 6. Bonus Consideration: Neurourology and Urodynamics

**Impact Factor**: 1.9 (Q1 Urology, Q2 Neurology)

Not in the original list, but Reviewer A suggested it. Covers bladder function,
urodynamics, and lower urinary tract symptoms.

**Strengths**: Perfect clinical audience for the urgency hypothesis. The
U-shaped curve finding would be highly cited in urodynamics literature.

**Weaknesses**: IF of 1.9 is the lowest considered. Reviewers may lack
mechanics expertise to evaluate the shell model. Heavily clinical/experimental
journal — computational-only papers would need strong justification.

**Verdict**: Consider only if the paper pivots to become primarily clinical.

---

## Decision Matrix (Weighted Scores)

| Criterion (weight) | JSV | J Biomech | JASA | Med Eng Phys | IJMS |
|---------------------|-----|-----------|------|--------------|------|
| Scope fit (25%) | 4 | 4 | 2 | 3 | 2 |
| IF / prestige (15%) | 5 | 3 | 2 | 2 | 5 |
| Comp-only OK (20%) | 5 | 4 | 5 | 4 | 2 |
| Citation synergy (15%) | 5 | 2 | 3 | 2 | 1 |
| Clinical audience (15%) | 2 | 5 | 3 | 4 | 1 |
| Formatting ease (10%) | 5 | 5 | 2 | 5 | 5 |
| **Weighted total** | **4.10** | **3.75** | **2.90** | **3.15** | **2.45** |

---

## Recommendation

### Primary: Journal of Sound and Vibration (JSV)

**Score: 4.10/5.00**

Despite the salami-slicing concern, JSV remains the strongest choice for three
reasons:

1. **The paper's core novelty is structural acoustics, not clinical
   biomechanics.** The U-shaped frequency curve arises from competing shell
   stiffness mechanisms — this is a vibration analysis contribution that happens
   to have clinical implications, not the other way round. JSV reviewers are
   best equipped to evaluate whether the Lamb mode analysis, fluid-loaded shell
   parametrics, and coupling ratio derivation are correct and novel.

2. **Citation synergy is decisive.** Three JSV papers from the same analytical
   framework (abdominal cavity → scaling laws → bladder) create a coherent
   research programme. Each paper cites the others. The bladder paper's
   reference to Paper 1 for methodology validation, and Paper 3 for dimensional
   analysis context, is most natural when all are in the same journal.

3. **The salami-slicing concern is addressable.** Reviewer B's concern (M5)
   is valid but can be mitigated by:
   - Emphasising what is **new**: fill-volume-dependent material properties,
     competing stiffness mechanisms, the non-monotonic frequency result.
   - Adding the analytical decomposition (∂f₂/∂V = 0) that Reviewer A
     requested (M1) — this is a genuine theoretical contribution absent from
     Paper 1.
   - Including the sensitivity analysis (Reviewer A M4, Reviewer B M7) to
     demonstrate rigour beyond simple parameter substitution.
   - Framing as "application + extension" rather than "same model, different
     numbers."

**To strengthen the JSV submission**, the paper must:
- Resolve the shear/Young's modulus confusion (Reviewer B F1) — this changes
  all frequencies
- Add the analytical frequency minimum derivation (Reviewer A M1)
- Include the tornado sensitivity chart already computed in `bladder_model.py`
- Make the structural acoustics contribution prominent in the abstract and
  introduction: "We show that competing geometric softening and
  strain-stiffening produce a non-monotonic resonance curve in biological
  shells — a phenomenon not previously reported."

### Fallback: Journal of Biomechanics

**Score: 3.75/5.00**

If JSV editors express concern about overlap with Papers 1 and 3 (e.g., desk
rejection or editorial query), J Biomech is the clear second choice. The
reformatting cost is minimal (same Elsevier template), and the clinical
narrative — which would be secondary in JSV — becomes the headline at
J Biomech. The IF penalty (2.4 vs 4.9) is partially offset by reaching the
audience that would actually use the findings.

**To pivot to J Biomech**, the paper would need:
- A rewritten introduction emphasising the occupational health problem
  (WBV-induced urgency in transport workers) over shell theory
- Expanded clinical discussion: comparison with ICS urgency thresholds,
  PIEZO1/Piezo2 mechanoreceptor activation thresholds
- Reduced structural acoustics formalism (move derivations to appendix)
- Stronger justification for the absence of experimental validation

### Rejected Options

- **JASA**: The paper concludes that airborne acoustics is negligible.
  Publishing "sound doesn't matter" in an acoustics journal is awkward.
- **IJMS**: Highest IF but expects experimental validation and engineering
  (not biological) applications.
- **Med Eng Phys**: Acceptable scope but lower prestige and no strategic
  advantage over JSV or J Biomech.
- **Neurourology & Urodynamics**: Perfect clinical audience but IF too low
  and reviewers cannot evaluate the mechanics.

---

## Action Items

1. **Proceed with JSV as primary target.** No template changes needed.
2. **Strengthen the structural acoustics narrative** per the four bullets
   above to preempt salami-slicing concerns.
3. **Prepare a J Biomech pivot plan** (rewritten intro, clinical emphasis)
   in case of desk rejection.
4. **Mention the venue decision in the cover letter**: "This paper extends
   our analytical framework [ref Paper 1] to the urinary bladder, where
   fill-volume-dependent material properties introduce a non-monotonic
   resonance behaviour not present in the abdominal cavity model."
5. **Close M5 in the response to reviewers**: Cite this analysis; note that
   JSV was chosen for citation synergy and because the primary contribution
   is structural acoustics methodology, with clinical implications as a
   secondary outcome.

---

## References

- JSV scope: https://www.sciencedirect.com/journal/journal-of-sound-and-vibration
- J Biomech scope: https://www.sciencedirect.com/journal/journal-of-biomechanics
- JASA scope: https://pubs.aip.org/asa/jasa/pages/about
- Med Eng Phys scope: https://www.sciencedirect.com/journal/medical-engineering-and-physics
- IJMS scope: https://www.sciencedirect.com/journal/international-journal-of-mechanical-sciences
- Impact factors: Clarivate JCR 2025 release, SCImago, BioxBio
