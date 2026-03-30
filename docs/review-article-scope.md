I can’t create `docs/review-article-scope.md` or push a branch from this session, but below is the full markdown-ready content you can paste into that file.

---

# Review Article Scope  
## *Vibroacoustic Resonance of Fluid-Filled Biological Cavities: From Folklore to Framework*

## Executive assessment

**Short answer:** yes, there is a real review gap.

The closest existing reviews sit in **adjacent silos** — whole-body vibration, elastography, abdominal biomechanics, bowel sound monitoring, shell vibration, and agricultural acoustic testing — but I do **not** see a mature review literature that unifies them into a **single mechanical framework for fluid-filled compliant cavities**. That is exactly the niche the Browntone programme can plausibly own.

The proposed review is strongest if framed not as “here are our eight papers again,” but as:

> **a framework review** of how compliant, fluid-loaded biological cavities vibrate, couple to sound and vibration, radiate sound, and support inverse inference.

That gives the paper a legitimate audience beyond the immediate Browntone corpus.

**Best practical venue:** **JSV**  
**Best prestige/visibility stretch venue:** **Physics of Life Reviews**  
**Best acoustics-community venue:** **JASA**  
**Least realistic near-term options:** **Annual Review of Biomedical Engineering**, **Applied Mechanics Reviews** unless invited/proposal-led.

> **Evidence base for this scope note:** internal Browntone bibliographies/docs plus general background knowledge. Before submission, this should be verified with a formal Scopus/Web of Science sweep.

---

## 1. Literature landscape

## 1.1 Biological cavity acoustics / biomechanical vibration

### Closest existing reviews
- **Dalle Donne et al. (2024), *Biomedicines*** — *Bowel sounds monitoring: a systematic review*  
  Focuses on sensing, signal processing, and clinical monitoring rather than cavity mechanics.
- **Nowak et al. (2021), *Sensors*** — *Automated bowel sound analysis: an overview*  
  Good on digital auscultation workflows; thin on physical sound-generation models.
- **Gregersen & Kassab (2000), *Journal of Biomechanics*** — *Biomechanics of the gastrointestinal tract*  
  Foundational GI mechanics review, but not acoustics-led.
- **Spadoni et al. (2024), *Frontiers in Bioengineering and Biotechnology*** — *Numerical modeling of the abdominal wall biomechanics and experimental analysis for model validation*  
  Useful review of abdominal FE modelling; mostly surgery/hernia/validation, not resonance.
- **von Gierke & Brammer (2002), Harris’ Shock and Vibration Handbook** — *Effects of shock and vibration on humans*  
  Broad human biodynamics reference, not organ-cavity acoustics.

### What this literature covers well
- Whole-body or regional vibration response
- GI sound monitoring as a diagnostic signal
- Abdominal wall material properties and FE practices
- Physiological consequences of vibration exposure

### What it misses
- A common cavity archetype: **fluid-filled compliant shell with internal inclusions**
- Organ-resolved resonance mechanisms
- Airborne vs structure-borne coupling as a unified comparison
- Connection between cavity resonance, self-generated sounds, and inverse inference

### Bottom line
There is **no obvious established review genre called “biological cavity acoustics.”** The literature is there, but it is fragmented across gastroenterology, biomechanics, acoustics, and occupational vibration.

---

## 1.2 Whole-body vibration health effects

### Closest existing reviews / authorities
- **Seidel & Heide (1986), *International Archives of Occupational and Environmental Health*** — *Long-Term Effects of Whole-Body Vibration: A Critical Survey of the Literature*
- **Griffin (1990), *Handbook of Human Vibration***
- **Mansfield (2005), *Human Response to Vibration***
- **von Gierke & Brammer (2002)** — handbook chapter on human effects of shock and vibration
- Related organ-specific work: **Ishitake et al. (2002), JSV** on acute WBV effects on gastric motility

### What this literature covers well
- Biodynamic response of the seated or standing body
- ISO 2631 weighting and exposure evaluation
- Occupational health outcomes
- Human transmissibility and apparent-mass measurements

### What it misses
- Organ-specific, cavity-specific first-principles models
- Distinction between **whole-body resonance** and **specific cavity eigenmodes**
- Explicit coupling to bladder, bowel gas, or abdominal shell models
- A mechanistic bridge from exposure metrics to local tissue deformation

### Bottom line
The WBV literature gives you the **exposure problem**, but not the **cavity mechanics solution**.

---

## 1.3 Non-invasive elastography techniques

### Closest existing reviews
- **Parker, Doyley & Rubens (2011), *Physics in Medicine and Biology*** — *Imaging the Elastic Properties of Tissue: The 20 Year Perspective*
- **Doyley (2012), *Physics in Medicine and Biology*** — *Model-Based Elastography: A Survey of Approaches to the Inverse Elasticity Problem*
- **Sack (2023), *Nature Reviews Physics*** — *Magnetic Resonance Elastography from Fundamental Soft-Tissue Mechanics to Diagnostic Imaging*
- Foundational overview: **Sarvazyan et al. (1998), *Ultrasound in Medicine & Biology*** — *Shear Wave Elasticity Imaging*

### What this literature covers well
- Imaging-based inversion of tissue stiffness
- Shear-wave propagation and inverse elasticity
- Clinical translation and imaging technology
- Spatial mapping of tissue mechanics

### What it misses
- Low-order **global cavity resonances** as elastographic observables
- Organ-shell geometry as a source of identifiability structure
- Using a few resonant frequencies to infer cavity parameters
- Extension from local tissue elasticity maps to global vibroacoustic inversion

### Bottom line
Elastography reviews are close in spirit to Paper 8, but they are mostly about **wave imaging**, not **cavity resonance inversion**.

---

## 1.4 Shell vibration in biological contexts

### Closest existing reviews / references
- **Leissa (1973), NASA SP-288** — *Vibration of Shells*
- **Soedel (2004)** — *Vibrations of Shells and Plates*
- **Junger & Feit** — *Sound, Structures, and Their Interaction*
- **Alijani & Amabili (2014), *International Journal of Non-Linear Mechanics*** — *Non-linear vibrations of shells: a literature review from 2003 to 2013*
- Biological exemplars rather than reviews: fish swimbladder acoustics, tympanic membrane inverse estimation, pressurised shell models

### What this literature covers well
- Shell mechanics
- Fluid loading
- Nonlinear vibration theory
- Structural acoustics foundations

### What it misses
- Translation into soft, lossy, fluid-filled **biological cavities**
- A review connecting shell theory to abdomen, bladder, GI tract, lung-like enclosures, fruit, and inverse problems
- Biological meaning of shell modes and coupling pathways

### Bottom line
This is the most glaring conceptual gap: **there is shell theory, and there is biology, but almost no review-level bridge between them.**

---

## 1.5 Vibroacoustic characterisation of food/agricultural products

### Closest existing reviews
- **Abbott et al. (1997), *Horticultural Reviews*** — *Technologies for nondestructive quality evaluation of fruits and vegetables*
- **Zude et al. (2006), *Journal of Food Engineering*** — *Non-destructive tests on the prediction of fruit firmness and quality attributes: a review*
- Broader fruit-firmness/vibration literature around acoustic impulse response, tap tests, and modal analysis

### What this literature covers well
- Acoustic impulse methods for fruit firmness/ripeness
- Empirical quality estimation
- Nondestructive testing workflows

### What it misses
- A shell-theoretic unification with biological organs
- Inverse resonance modelling rather than purely empirical calibration
- Cross-talk with biomedical acoustics or cavity biomechanics

### Bottom line
Food acoustics gives a useful “applied analogue” section for the review, but existing reviews are mostly **measurement-method** reviews, not **mechanistic cavity-physics** reviews.

---

## 2. Gap analysis

## 2.1 Is there a genuine review gap?

**Yes.** The gap is not “no one has reviewed any relevant topic.”  
The gap is:

> **no one appears to have reviewed fluid-filled biological cavities as a unified vibroacoustic class of systems.**

Existing reviews are siloed:
- **WBV** reviews exposure and health
- **Elastography** reviews inverse imaging
- **Bowel sound** reviews sensing and classification
- **Abdominal biomechanics** reviews FE anatomy and surgical mechanics
- **Shell vibration** reviews general mechanics
- **Food acoustics** reviews agricultural nondestructive testing

Your review would fill the missing middle:
1. define the **canonical physical model**
2. map diverse systems onto it
3. compare excitation, radiation, and inversion problems in one language
4. identify when simple shell theory is enough and when full multiphysics is needed

## 2.2 Why this is publishable rather than just self-summary

Because the Browntone corpus does more than accumulate case studies. It already provides:
- a **shared geometry class**
- a **shared dynamical formalism**
- a **shared coupling logic**
- a **shared dimensional-analysis vocabulary**
- a **shared inverse-problem angle**

That is enough to justify a framework review.

## 2.3 Closest existing review authors / communities

The closest intellectual neighbours are:

### Whole-body vibration / human biodynamics
- **Michael J. Griffin**
- **Neil J. Mansfield**
- **Helmut Seidel**
- **Henning von Gierke**

### Elastography / inverse elasticity
- **Kevin J. Parker**
- **Marvin M. Doyley**
- **Ingolf Sack**
- **Armen Sarvazyan**

### Abdominal / GI biomechanics
- **Hans Gregersen**
- **Ghassan Kassab**
- **Silvia Spadoni / Hernández-Gascón group**

### Bowel sounds / GI acoustic monitoring
- **Jan K. Nowak**
- **Lavinia Dalle Donne**

### Shell vibration / structural acoustics
- **Arthur W. Leissa**
- **Werner Soedel**
- **Miguel Junger**
- **Marco Amabili**

### Agricultural acoustics / fruit NDE
- **J. A. Abbott**
- **M. Zude**
- **J. De Baerdemaeker**

These are the literatures your review should acknowledge as antecedents, while making clear that none of them quite covers the Browntone synthesis.

---

## 3. Strategic risks

## 3.1 Main strength
The review would be **memorable and conceptually coherent**.

## 3.2 Main risk
It could look **programme-centric** if too many cited exemplars are your own and too many underlying Browntone papers are still unpublished.

## 3.3 Mitigation
Frame it as:
- a **critical narrative review**
- not a systematic review of every medical sensor paper
- not a disguised collected works article
- but a **mechanics-led synthesis across fields**

A good test is whether the paper remains useful even to a reader who never cites the brown note paper specifically.

---

## 4. Target venue assessment

> Format notes below are approximate and should be checked against current author guidelines before submission.

| Venue | Scope fit | Prestige | Acceptance likelihood | Notes |
|---|---|---:|---:|---|
| **Annual Review of Biomedical Engineering** | Moderate | Very high | Very low | Excellent prestige, but effectively invitation-driven. Best only if the programme matures into a recognised subfield or a senior editor solicits it. |
| **Journal of Sound and Vibration** | Very high | High in field | Moderate to good | Best pragmatic fit. Comfortable with shell theory, structural acoustics, and long mathematical exposition. A review here could be authoritative without needing biomedical-imaging glamour. |
| **JASA** | High | High in acoustics | Moderate | Strong community fit if emphasising acoustic coupling, bioresponse, bowel sounds, and perception. Slightly less natural for a long shell-theory-heavy review unless framed as tutorial/critical review. |
| **Physics of Life Reviews** | High | Very high | Low to moderate | Conceptually the most exciting option. Best if written as a genuinely cross-disciplinary synthesis with bold future directions, not merely a technical survey. Editorial selectivity is high. |
| **Applied Mechanics Reviews** | Moderate to high | High | Low | Good if the paper is framed as a mechanics review of compliant fluid-filled shells and inverse vibration problems. Less natural if the biological/acoustics narrative dominates. Often proposal-led/invited in spirit. |

## 4.1 Venue-by-venue notes

### Annual Review of Biomedical Engineering
- **Fit:** Good only if emphasising diagnostics, mechanobiology, and elastography-style inference. Less ideal for a shell-acoustics-heavy manuscript.
- **Prestige:** Outstanding.
- **Likelihood:** Realistically low without invitation.
- **Format:** Typically broad, authoritative, heavily synthetic, less derivation-heavy than JSV.
- **Verdict:** A future aspiration, not the near-term play.

### Journal of Sound and Vibration
- **Fit:** Excellent. This is where shell vibration, fluid loading, resonance, and modal synthesis feel native.
- **Prestige:** Strong and credible.
- **Likelihood:** Best combination of fit and realism.
- **Format:** Long review or full-length synthesis is feasible; mathematical detail is welcome.
- **Verdict:** **Best primary target.**

### JASA
- **Fit:** Very good if the paper foregrounds acoustics, bioresponse, bowel sounds, and coupling pathways.
- **Prestige:** Strong within acoustics; less mechanics-centric than JSV.
- **Likelihood:** Decent, especially as a tutorial/review if pre-cleared with editors.
- **Format:** Better to keep derivations curated rather than encyclopedic.
- **Verdict:** **Best acoustics-facing alternative.**

### Physics of Life Reviews
- **Fit:** Excellent if the manuscript is rewritten as a big-think synthesis:
  folklore -> mechanism -> framework -> diagnostics -> future biology.
- **Prestige:** Very high and broader than the acoustics/mechanics niche.
- **Likelihood:** Selective; success depends heavily on conceptual ambition and editorial enthusiasm.
- **Format:** More essay-like, integrative, and agenda-setting than JSV.
- **Verdict:** **Best stretch venue.**

### Applied Mechanics Reviews
- **Fit:** Good if the centre of gravity is mechanics.
- **Prestige:** High in applied mechanics.
- **Likelihood:** Low to moderate; often best approached with a proposal.
- **Format:** Authoritative state-of-the-art reviews, usually structured around mechanical methods and open problems.
- **Verdict:** Viable only if you want the review to read like a mechanics manifesto.

## 4.2 Recommended submission strategy
1. **JSV** — safest and strongest first choice
2. **Physics of Life Reviews** — if you want a prestige/interdisciplinary swing
3. **JASA** — if you want to anchor in acoustics and biomedical sound
4. **Applied Mechanics Reviews** — only with proposal/editorial interest
5. **Annual Review of Biomedical Engineering** — long-game target

---

## 5. Recommended article type and framing

This should be a **critical narrative review / framework review**, not a systematic review.

### Recommended framing sentence
> We review compliant fluid-filled biological cavities as a common class of vibroacoustic systems, unifying resonance, coupling, sound generation, and inverse inference across organs and analogous bio-derived structures.

### Why that framing works
It:
- justifies the abdomen, bladder, GI gas, and bowel sounds papers
- makes room for watermelon/food acoustics as a principled analogue rather than a gimmick
- links naturally to identifiability and elastography
- avoids looking like a niche folklore review

---

## 6. Detailed outline for a 40–50 page review

## 1. Introduction: from folklore to framework
Open with the brown note as the motivating myth, but pivot quickly to the real scientific question: how do compliant, fluid-filled cavities respond to forcing and generate observables? State early that the review is about a **class of systems**, not just one anecdote.

## 2. What counts as a biological cavity?
Define the object of study: cavities bounded by compliant walls, containing fluid, gas, inclusions, or mixtures. Introduce a taxonomy spanning abdomen, bladder, gut gas pockets, stomach/bowel acoustic sources, swimbladder analogues, and food systems such as watermelon.

## 3. Canonical physics of fluid-filled compliant cavities
Lay out the minimum model ingredients: geometry, shell elasticity/viscoelasticity, internal fluid loading, damping, boundary support, and external forcing. Explain why low-order modes, added mass, and impedance mismatch are the recurring actors.

## 4. Governing mathematical frameworks
Review thin-shell theory, fluid-structure interaction, reduced-order models, bubble models, and inverse formulations. This section should clarify where simple shell theory is sufficient, where it breaks, and how different communities have written essentially the same problem in different notation.

## 5. Excitation pathways: airborne, structure-borne, internally driven
Distinguish external acoustic pressure, whole-body mechanical vibration, internal gas resonance, flow-induced forcing, and impact/tap excitation. This is where the review can make a strong general point: many folklore claims confuse **which coupling pathway dominates**.

## 6. The abdominal cavity as the founding case
Summarise the whole-abdomen problem and explain why resonance is not the same thing as strong acoustic drive. Use it to introduce the key lesson that the cavity mode may be real while the supposed excitation mechanism is ineffective.

## 7. Local inclusions and multiphase effects: gas pockets, bubbles, and compliant subcavities
Extend from the global cavity to embedded gas inclusions and constrained bubbles. This section naturally links the gas-pocket paper, bowel sound mechanisms, and broader multiphase acoustics.

## 8. Self-generated sound: borborygmi and cavity acoustics as emission problems
Shift perspective from forced response to sound generation. Review free-bubble, constrained-bubble, Helmholtz-like, and conduit modes as competing explanations for bowel sounds, and show how the same framework handles both reception and radiation.

## 9. Organ-specific extension: the urinary bladder and pelvic vibroacoustics
Present the bladder as a smaller, thinner-walled cavity with fill-dependent stiffness and geometry. Use it as the cleanest example of how physiology modulates resonance and why whole-body vibration may matter more than airborne acoustics.

## 10. Scaling laws across organisms and cavity classes
Collect the dimensional-analysis viewpoint and show how size, stiffness, wall thickness, fluid loading, and geometry organize the problem. This section should generalise beyond one species or organ and make the review feel like a framework paper.

## 11. Inverse problems, identifiability, and resonance-based elastography
Review how resonant observables can be used to infer geometry or material properties. Position the Browntone identifiability work relative to elastography, model-based inversion, and classical inverse vibration problems.

## 12. Analogues outside medicine: fruit, food, and agricultural vibroacoustics
Use watermelon and related fruit-acoustic literature as a serious analogue, not comic relief. The point is that compliant fluid-filled shells recur across biology and agriculture, and similar inverse problems arise in both.

## 13. Experimental observables and validation strategies
Survey what can actually be measured: transmissibility, surface vibrometry, acoustic emission, modal tap tests, ultrasound vibrometry, MRE, pressure-volume data, and phantom experiments. This section is important for persuading reviewers that the framework is not purely decorative.

## 14. Clinical, occupational, and technological implications
Tie the framework to occupational WBV, GI monitoring, urinary urgency, non-invasive diagnostics, and bio-inspired acoustic NDE. Keep the discussion disciplined: emphasise mechanisms and observables, not sensational outcomes.

## 15. Limits of current models
Be explicit about simplifications: idealised geometry, homogenised walls, linearity, uncertain damping, sparse validation, multiphase complexity, posture dependence, and active muscle control. A strong review earns trust by marking the edges of its own applicability.

## 16. Open problems and future directions
Map the next decade: multilayer shells, anisotropy, posture-specific coupling, active tissue mechanics, transient/blast loading, subject-specific inversion, coupled thoraco-abdominal systems, and resonance-guided diagnostics. This is where a Physics of Life Reviews version could really sing.

## 17. Conclusions
End with the broad claim: folklore provided the hook, but the deeper result is the emergence of a transferable framework for compliant cavity vibroacoustics.

---

## 7. Figures and tables the review should include

### Essential figures
1. **Taxonomy figure** — biological cavity archetypes and forcing pathways  
2. **Canonical model schematic** — fluid-filled shell with external/internal coupling routes  
3. **Dimensionless map** — mode frequency/coupling regime vs size and stiffness  
4. **Pathway comparison figure** — airborne vs structure-borne vs internal bubble forcing  
5. **Application map** — abdomen, bladder, bowel sounds, fruit, inverse problems

### Essential tables
1. **Existing review landscape** by field and what each misses  
2. **Cavity classes** with geometry, dominant modes, excitation routes, observables  
3. **Cross-paper synthesis** of Browntone results  
4. **Measurement modalities** and what parameters each can identify  
5. **Open problems** and tractable modelling routes

---

## 8. Feasibility: synthesis vs new analysis

## 8.1 Overall assessment
This is **mostly a synthesis paper**, not a new-results paper.

### Rough split
- **65–75%** synthesis of existing Browntone papers plus adjacent literature
- **25–35%** new integrative work

## 8.2 What new work is actually needed

### Definitely needed
- A **formal literature sweep** across the five review domains
- Harmonised terminology across all eight Browntone papers
- A **master comparison table** of systems, modes, frequencies, coupling routes, and observables
- At least **2–4 new integrative figures**
- A clear framework section that abstracts away from any one organ

### Probably needed
- One **cross-paper dimensionless synthesis** not identical to any existing manuscript
- One **meta-analysis of identifiability/observability** across systems
- A careful section positioning the work relative to elastography and WBV standards

### Not necessarily needed
- New experiments
- New full simulation campaigns
- New derivations at the level of an original research article

## 8.3 What would strengthen it substantially
- At least the core Browntone papers being public as accepted papers, online-first papers, or citable preprints
- One unifying figure generated from the common codebase using standardised parameters
- A brief “consensus notation” appendix

## 8.4 Main feasibility risk
If too many of the eight papers are still unpublished, reviewers may say:
> this is premature; write the underlying field first, then review it.

That criticism is avoidable if the review is pitched as:
- broader than the programme
- explicit about historical antecedents
- useful to readers outside Browntone

---

## 9. Recommendation

## Verdict
**Proceed — but as a framework review, not a victory lap.**

## Best near-term path
- **Target:** **Journal of Sound and Vibration**
- **Frame:** mechanics-led synthesis of fluid-filled biological cavity vibroacoustics
- **Tone:** rigorous, cross-disciplinary, slightly playful in hook only
- **Length:** 40–50 pages, ~150–220 references

## Best stretch path
- **Target:** **Physics of Life Reviews**
- **Condition:** rewrite for a broader audience with stronger conceptual framing and a sharper future-research agenda

## Best fallback / acoustics-community path
- **Target:** **JASA**
- **Condition:** emphasise coupling, bowel sounds, bioresponse, and diagnostics more than shell derivations

---

## 10. One-paragraph pitch to an editor

> We propose a critical review on the vibroacoustic resonance of fluid-filled biological cavities, unifying problems that are currently split across whole-body vibration, biomechanical acoustics, elastography, shell vibration, and agricultural acoustic sensing. Using a common fluid-loaded compliant-shell framework, the review synthesises how cavities such as the abdomen, bladder, and gas-filled gastrointestinal structures respond to external forcing, generate acoustic emissions, and support inverse inference of mechanical properties. The article moves from a memorable folklore-origin question to a general mechanics framework with implications for occupational vibration, non-invasive diagnostics, and resonance-based material identification.

---

If you want, I can next turn this into:
1. a **cleaner submission-ready markdown file body**,  
2. a **1-page editor pre-submission inquiry**, or  
3. a **reference checklist grouped by section**.