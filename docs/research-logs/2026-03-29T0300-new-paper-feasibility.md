# New Paper Feasibility Assessment — 29 March 2026

**Prepared by:** Research Scout  
**For:** PI review  
**Context:** Evaluation of 6 candidate topics for the Browntone programme (Papers 6+)  
**Prior art reviewed:** Papers 1–5 (all drafts), scout-report-2026-03-27.md, ig-nobel-strategy.md, RESEARCH-VISION.md, provocateur-research-direction.md, novel-ideas.md, all analytical source modules

---

## Executive Summary

The Browntone programme has a mature five-paper portfolio and a battle-tested analytical
toolkit (oblate spheroidal shell theory, constrained-bubble resonance, energy budgets,
mechanotransduction chains, Sobol UQ). Six candidate topics are evaluated below for
scientific novelty, feasibility within an AI-assisted analytical/computational lab,
publication venue, effort, risk, and strategic value.

**Bottom line:** Topics 1 and 3 are the strongest candidates. Topic 1 (sub-bass
perception) has the best combination of code reuse, novelty, and audience appeal.
Topic 3 (coupled acoustic-structural model) fills the most important scientific gap
and would make Paper 1 citable by the interior-acoustics community. Topics 2 and 5
are excellent but require experimental access or significantly more code. Topic 4 is
high-impact but low-urgency. Topic 6 is a communications task, not a research project.

### Quick-Reference Ranking

| Rank | Topic | Novelty | Feasibility | Effort | Strategic Value | Verdict |
|------|-------|---------|-------------|--------|-----------------|---------|
| 1 | Sub-bass perception thresholds | ★★★★☆ | ★★★★★ | 4–6 weeks | ★★★★★ | **GO — start now** |
| 2 | Coupled acoustic-structural | ★★★★★ | ★★★★☆ | 6–10 weeks | ★★★★★ | **GO — queue behind #1** |
| 3 | Multi-organ interaction | ★★★★☆ | ★★★★☆ | 6–8 weeks | ★★★★☆ | **GO — medium priority** |
| 4 | Historical/review paper | ★★★☆☆ | ★★★★★ | 4–6 weeks | ★★★★☆ | **CONDITIONAL — after 3+ papers published** |
| 5 | Experimental validation | ★★★★★ | ★★☆☆☆ | 3–6 months | ★★★★★ | **PARK — needs collaborator** |
| 6 | Ig Nobel submission | N/A | ★★★★★ | 1 week | ★★★★★ | **DEFER — comms task, not research** |

---

## Topic 1: "Can You Feel the Bass?" — Sub-Bass Perception vs Abdominal Resonance

### The Proposal
Link psychoacoustic sub-bass perception thresholds to the biomechanical abdominal
resonance framework. Ask: when a concert subwoofer or pipe organ hits 20–60 Hz at
100–120 dB, does the abdominal cavity act as a transducer? Is the "feeling the bass
in your chest" sensation a resonance phenomenon or a pressure sensation?

### Scientific Novelty: ★★★★☆

**What exists:**
- Psychoacoustic perception thresholds below 20 Hz are well-documented (ISO 226:2003,
  Møller & Pedersen 2004, Watanabe & Møller 1990). The threshold of *perception*
  (as opposed to hearing) drops steeply below 20 Hz.
- Concert sound measurements exist (Perrson Waye & Rylander 2001, Schomer 2000).
- WBV transmissibility to the abdomen is in ISO 2631-1 and Griffin (1990).
- Pipe organ infrasound levels documented (Bédard & Georges 2000; Ingerslev & Frobenius 1947).

**What's missing — the gap:**
Nobody has connected these three literatures with a quantitative coupling model.
Specifically: given a measured sub-bass spectrum at a concert or organ recital, what is
the predicted abdominal wall displacement using the Paper 1 framework, and does it exceed
PIEZO mechanotransduction thresholds (Paper 2)? The sub-bass perception community treats
the body as a black box. The vibroacoustics community doesn't know about PIEZO channels.
This paper would bridge psychoacoustics → structural acoustics → mechanotransduction in a
single analytical chain.

**Novel contribution:**
1. First quantitative model predicting visceral tissue displacement from measured sub-bass spectra
2. Identification of the frequency band where airborne-to-abdominal coupling transitions
   from negligible (Paper 1's $(ka)^n$ regime) to appreciable (ka ~ 0.1–1.0)
3. A "perception map" in frequency × SPL space showing where mechanical abdominal response
   exceeds neural thresholds

### Feasibility: ★★★★★

This is the highest-synergy topic. It uses:
- `oblate_spheroid_ritz.py` — frequency response at arbitrary excitation frequency
- `energy_budget.py` — coupling efficiency vs frequency (extend from 5 Hz to 60 Hz)
- `mechanotransduction.py` — PIEZO thresholds for comparison
- `uncertainty_quantification.py` — Monte Carlo over body morphometry

**New code needed:** ~200 lines
- Spectral input module (read concert/organ SPL spectra from literature data)
- Frequency-dependent $(ka)$ coupling across the 5–100 Hz band (straightforward extension
  of the existing energy budget — currently evaluated only at resonance)
- Perception map generator (frequency × SPL heatmap of predicted tissue displacement)

**Data availability:** Concert measurements published in JASA, JSV, and Applied Acoustics.
Pipe organ infrasound levels in Bédard & Georges (2000). No experiments needed.

### Publication Venue
**Primary:** *Journal of Sound and Vibration* (bridges structural acoustics and perception)  
**Alternative:** *JASA* (psychoacoustics + bioacoustics crossover)

### Effort: 4–6 weeks
- Week 1: Literature synthesis on sub-bass exposure levels
- Week 2: Extend energy budget code across 5–100 Hz; validation against ka → 0 limit
- Week 3–4: Generate perception maps, parametric studies, Monte Carlo
- Week 5–6: Draft manuscript, figures, internal review

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Result is boring (coupling always negligible) | Low | High | Preliminary calculation suggests coupling becomes non-trivial above ~40 Hz at 110+ dB — there IS a transition band |
| Scooped by psychoacoustics group | Low | Medium | The structural-acoustics community doesn't read psychoacoustics journals and vice versa; the cross-disciplinary framing is the novelty |
| Reviewer says "this is just Paper 1 evaluated at higher frequencies" | Medium | Medium | Emphasise the spectral-input methodology, the perception map as a novel output, and the mechanotransduction bridge |
| Over-reliance on literature SPL data | Medium | Low | Frame as analytical framework; experimental validation deferred to future work |

### Strategic Value: ★★★★★
- **Broadens the audience:** Every live-music acoustician, organ builder, and noise
  control engineer would read this paper. The concert/organ hook is extremely shareable.
- **Natural Paper 6:** Extends Papers 1 + 2 without repeating them.
- **Code reuse:** ~90% existing codebase; minimal new development.
- **Ig Nobel halo:** "Can You Feel the Bass?" is an inherently memorable title.
- **Bridges to "brown noise for sleep" topic** (scout-report-2026-03-27, Topic 8).

### Potential Title
**"Can You Feel the Bass? Abdominal Resonance Thresholds for Sub-Bass Sound in Concert and Organ Environments"**

### Key Starting References
1. Møller, H. & Pedersen, C.S. (2004) "Hearing at low and infrasonic frequencies," *Noise & Health* 6(23):37–57
2. Bédard, A.J. & Georges, T.M. (2000) "Atmospheric infrasound," *Physics Today* 53(3):32–37
3. Todd, N.P.M. & Cody, F.W. (2000) "Vestibular responses to loud dance music," *JASA* 107(1):496–500
4. Persson Waye, K. & Rylander, R. (2001) "The prevalence of annoyance and effects after long-term exposure to low-frequency noise," *JSV* 240(3):483–497
5. Paper 1 (Mace & Mace, this programme) — the $(ka)^n$ coupling framework

---

## Topic 2: Experimental Validation — Phantom Abdomen

### The Proposal
Build a silicone shell phantom (oblate spheroid, water-filled), mount on shaker table,
measure mode shapes with laser vibrometry. Compare measured eigenfrequencies against
Paper 1's analytical predictions.

### Scientific Novelty: ★★★★★

This would be the first experimental measurement of flexural modes of a tissue-mimicking
oblate spheroidal shell. It directly validates (or falsifies) the analytical framework
that underpins the entire five-paper programme. Experimental shell dynamics papers are
among the most-cited in JSV because they anchor theoretical work.

### Feasibility: ★★☆☆☆

**The problem:** This lab is AI-assisted analytical/computational. We don't have:
- A laser Doppler vibrometer (Polytec PSV-500, ~$80k–200k)
- A vibration shaker table with <5 Hz capability
- A silicone casting facility
- Accelerometers, signal conditioning, DAQ hardware
- Physical laboratory space

**The existing phantom design** (docs/phantom-experiment-design.md) is thorough — Option A
(Ecoflex silicone shell) is well-specified with material calibration protocol, and the
instrumentation plan (LDV + MEMS accelerometers) is sound. But it's a design, not a lab.

**Realistic path:**
- Find a collaborator with vibration testing facilities (university acoustics lab)
- Provide the analytical predictions, phantom design, and test protocol
- Co-author the experimental paper
- Timeline: 3–6 months including fabrication, calibration, and measurement campaigns

### Publication Venue
**Primary:** *JSV* — "Experimental validation of..." papers are their bread and butter  
**Alternative:** *Experimental Mechanics* or *Mechanical Systems and Signal Processing*

### Effort: 3–6 months (collaboration-dependent)
- Month 1: Identify collaborator, refine phantom spec, order materials
- Month 2: Fabrication and material calibration
- Month 3: Shaker table and LDV measurements
- Month 4–5: Data analysis, comparison with analytical predictions
- Month 6: Manuscript

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| No collaborator found | Medium | Fatal | Approach 3–5 groups simultaneously; Auckland, Salford, Loughborough have vibration labs |
| Phantom modes don't match predictions | Medium | High (but also interesting) | Discrepancy IS a result — update the model. Over-prediction was already flagged (3.75× from M2 gap) |
| Experiment scope creep | High | Medium | Fix the protocol in advance; one shell geometry, one fill level, one boundary condition |
| Silicone properties hard to control | Medium | Medium | DMA calibration before vibration testing; use measured E, not nominal |

### Strategic Value: ★★★★★
- **Addresses the #1 reviewer criticism** of Paper 1: no experimental validation
- **Would be the most-cited paper** in the programme — experimental validations anchor
  theoretical frameworks
- **Makes the entire 5-paper programme defensible** to sceptics
- **Enables further experimental papers** (gas pocket phantoms, multi-organ phantoms)
- **Strong Ig Nobel support** — "we built a fake belly and shook it"

### Potential Title
**"Experimental Modal Analysis of a Tissue-Mimicking Oblate Spheroidal Phantom: Validation of an Abdominal Resonance Model"**

### Key Starting References
1. Phantom design doc: `docs/phantom-experiment-design.md` (this repo)
2. Madsen, E.L. et al. (2005) "Tissue-mimicking materials for ultrasound phantoms," *Phys Med Biol* 50:5597
3. Matheny, M.H. et al. (2019) "Exotic states in a simple network of nanoelectromechanical oscillators," *Science* 363(6431) — for shell modal testing methodology
4. Leissa, A.W. (1973) *Vibration of Shells* — NASA SP-288 — benchmark solutions
5. Warburton, G.B. (1976) *Dynamical Behaviour of Structures* — experimental modal analysis methods

---

## Topic 3: Coupled Acoustic-Structural Model (Interior Acoustics)

### The Proposal
Develop a full interior acoustic cavity model coupled to the shell modes. Paper 1 treats
the fluid as an added-mass correction; the breathing mode is computed separately from
flexural modes. A coupled model would capture:
- Mode pairs (structural mode + acoustic mode interaction)
- Avoided crossings in the dispersion relation
- The breathing-mode vs flexural-mode distinction rigorously
- Interior pressure field (not just wall displacement)

### Scientific Novelty: ★★★★★

**What exists:**
- Coupled acoustic-structural analysis of cylindrical shells + enclosed fluid is mature
  (Dowell & Voss 1963, Pretlove 1965, Pan & Bies 1990).
- Spherical shell + interior acoustics: classical (Junger & Feit 1972, ch. 8).
- Oblate spheroidal acoustic modes: solved analytically in Morse & Feshbach (1953) using
  spheroidal wave functions.

**What's missing:**
Nobody has coupled oblate spheroidal shell flexural modes to interior oblate spheroidal
acoustic modes with viscoelastic damping. Paper 1 treats them independently: the flexural
model uses a Rayleigh-Ritz shell approach with fluid added-mass; the breathing mode uses
a separate pressure-release analysis. A proper coupled formulation would:
1. Show whether there are structural-acoustic mode pairs near the infrasonic range
2. Predict the interior pressure field (relevant for organ loading)
3. Quantify how much energy the cavity acoustic modes extract from the shell modes
4. Provide the foundation for the multi-organ problem (Topic 5)

This is the most technically ambitious topic but also the most scientifically impactful.

### Feasibility: ★★★★☆

**Analytical approach:**
- The interior acoustic modes of an oblate spheroidal cavity are known (spheroidal wave
  functions; Morse & Feshbach). The `scipy.special` package includes spheroidal wave
  functions (`pro_ang1`, `pro_rad1`).
- Coupling: expand the interior pressure in spheroidal acoustic modes, expand shell
  displacement in structural modes, form the coupled eigenvalue problem via continuity
  of normal velocity at the shell surface.
- The coupled problem is a matrix eigenvalue problem of size (N_structural + N_acoustic).

**Codebase reuse:**
- `oblate_spheroid_ritz.py` provides structural modes
- `natural_frequency_v2.py` provides the breathing mode
- Need: acoustic mode solver for oblate spheroidal cavity, coupling matrix computation

**New code needed:** ~500–800 lines
- Spheroidal wave function evaluator (wrap scipy)
- Interior acoustic eigenfrequency solver
- Coupling integral (surface integral of structural mode × acoustic mode on the spheroid)
- Coupled matrix assembly and eigensolve

### Publication Venue
**Primary:** *JSV* — coupled structural-acoustic analysis is core JSV territory  
**Alternative:** *Journal of Fluids and Structures* (if emphasising the FSI aspect)

### Effort: 6–10 weeks
- Week 1–2: Implement spheroidal acoustic modes, validate against known solutions
- Week 3–4: Coupling integrals, coupled eigenvalue problem
- Week 5–6: Parametric study (fluid density, shell stiffness, aspect ratio)
- Week 7–8: Compare coupled vs uncoupled predictions; quantify coupling strength
- Week 9–10: Manuscript and figures

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Spheroidal wave functions numerically unstable | Medium | High | Use asymptotic expansions for low-frequency limit (ka << 1); fall back to spherical limit for validation |
| Coupling is negligible at infrasonic frequencies | Medium | Medium | This would actually confirm Paper 1's decoupled approach — publishable as a validation |
| Scope creep into full FEA | Low | High | Strictly analytical — no FEA. The point is the closed-form coupled framework |
| Overlap with existing coupled-cavity literature | Low | Medium | Nobody has done it for oblate spheroids with viscoelastic walls |

### Strategic Value: ★★★★★
- **Fills the most important theoretical gap** in Paper 1
- **Foundation paper** for Topics 5 (multi-organ) and the laparoscopic insufflation idea
  (scout-report-2026-03-27, Direction 3)
- **Attracts the interior acoustics community** (vehicle NVH, room acoustics, underwater)
- **Makes the framework genuinely general** — not just a brown-note gimmick

### Potential Title
**"Coupled Structural-Acoustic Modes of a Fluid-Filled Viscoelastic Oblate Spheroid: Interior Pressure Fields and Mode Interaction"**

### Key Starting References
1. Junger, M.C. & Feit, D. (1972) *Sound, Structures, and Their Interaction*, MIT Press — Ch. 8–9
2. Morse, P.M. & Feshbach, H. (1953) *Methods of Theoretical Physics*, McGraw-Hill — spheroidal coordinates
3. Pan, J. & Bies, D.A. (1990) "The effect of fluid-structural coupling on sound waves in an enclosure," *JASA* 87(2):691–707
4. Pretlove, A.J. (1965) "Free vibrations of a rectangular panel backed by a closed rectangular cavity," *JSV* 2(3):197–209
5. Flammer, C. (1957) *Spheroidal Wave Functions*, Stanford UP — numerical methods

---

## Topic 4: Historical/Review Paper — "From Urban Legend to Biomechanical Model"

### The Proposal
A comprehensive narrative review tracing the brown note from Gavreau's 1957 CNRS lab
through Cold War weapons programmes, MythBusters, South Park, and into the five-paper
Browntone analytical programme.

### Scientific Novelty: ★★★☆☆

The historical material is already compiled in `docs/historical-survey.md` — it's thorough,
well-sourced, and distinguishes primary from secondary evidence. The novelty is in the
*synthesis*: connecting the cultural trajectory to the evolving physics, showing how each
generation of investigation (Gavreau → NASA → NLW programmes → MythBusters → Browntone)
asked the question with different tools and got progressively sharper answers.

**But:** Review papers derive their authority from the author's track record in the field.
Publishing a review *before* the primary papers are accepted risks looking presumptuous.
The review becomes powerful *after* Papers 1–3 are in print — it contextualises a body
of published work rather than announcing unpublished claims.

### Feasibility: ★★★★★

Almost no new analysis required. The historical survey exists. The technical summary
would draw on the five paper abstracts. The main work is:
- Structuring the narrative arc
- Adding ~20 additional references for cultural context
- Writing the "lessons for folklore-inspired research" discussion section

### Publication Venue
**Primary:** *Proceedings of the Royal Society A* (history + science synthesis)  
**Alternative:** *Acoustics Today* (ASA magazine — shorter, higher readership)  
**Alternative:** *Physics Today* (if framed as a physics pedagogy piece)  
**Fun option:** *Annals of Improbable Research* (AIR) — natural home, but less academic credit

### Effort: 4–6 weeks
- Week 1–2: Outline and narrative structure
- Week 2–3: Expand historical-survey.md into full manuscript sections
- Week 3–4: Technical synthesis section (connecting Papers 1–5)
- Week 5–6: Polish, figures (timeline graphic), internal review

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Published before primary papers | — | High | **Do not publish first.** Wait for Papers 1 and 5 minimum. |
| Tone misjudged (too funny or too dry) | Medium | Medium | Target the *Proc Roy Soc A* tutorial-review tone: scholarly but accessible |
| Reviewer says "this is a blog post, not a paper" | Medium | Medium | Ensure the technical synthesis section has genuine analytical content (comparison table of models, coupling pathway taxonomy) |
| Cultural history sections attract copyright complaints | Low | Low | Use only factual descriptions; no reproducing copyrighted text |

### Strategic Value: ★★★★☆
- **The "capstone" paper** that frames the programme for a general audience
- **Ig Nobel maximiser** — directly supports the nomination narrative
- **Media goldmine** — journalists will cite this as the accessible entry point
- **Relatively low effort** once primary papers are published
- **Risk:** premature publication undermines credibility

### Potential Title
**"The Brown Note: From Urban Legend to Biomechanical Model — A Scientific History of Infrasound and the Human Abdomen"**

### Key Starting References
1. `docs/historical-survey.md` (this repo) — comprehensive timeline
2. Leventhall, G. (2007) "What is infrasound?" *Progress in Biophysics and Molecular Biology* 93(1–3):130–137
3. Altmann, J. (1999) *Acoustic Weapons — A Prospective Assessment*, Science and Global Security 9:165–234
4. Jauchem, J.R. & Cook, M.C. (2007) "High-intensity acoustics for military nonlethal applications," *Military Medicine* 172(2):182–189
5. Mohr, G.C. et al. (1965) "Effects of low frequency and infrasonic noise on man," *Aerospace Medicine* 36(9):817–824

---

## Topic 5: Multi-Organ Interaction — Mass Loading and Constraint Effects

### The Proposal
Extend the abdominal cavity model to include solid organ inclusions (liver ~1.5 kg,
spleen ~0.15 kg, kidneys ~0.3 kg). Model their effect on modal behaviour via
mass-loading, localised stiffness perturbation, and modified boundary conditions.

### Scientific Novelty: ★★★★☆

**What exists in the codebase:**
`organ_inclusions.py` already implements a Hashin-Shtrikman effective medium approach —
it treats solid organs as inclusions that modify the bulk properties of the cavity fill.
Paper 1 shows this introduces <5% error in flexural frequencies for organ volume
fractions up to 30%.

**What's missing:**
The effective-medium approach homogenises the organs into the fluid. It cannot capture:
1. **Localised mass effects** — the liver sits against the right hemidiaphragm; it
   should break the azimuthal symmetry of the n=2 mode
2. **Contact mechanics** — organs constrained by ligaments and mesentery act as local
   spring-mass attachments, not distributed inclusions
3. **Mode localisation** — can a heavy organ "trap" vibrational energy in one region?
4. **Non-axisymmetric modes** — the current model is axisymmetric; real organs break this

**Novel contribution:**
A lumped-parameter organ attachment model (mass-spring on the shell surface) would capture
mode splitting, localisation, and asymmetry without full 3D FEA. This is the Rayleigh-Ritz
approach with additional discrete degrees of freedom — mathematically tractable and
analytically transparent.

### Feasibility: ★★★★☆

**Analytical approach:**
- Add point masses (organ masses) and local springs (ligament stiffness) to the existing
  Rayleigh-Ritz energy functional
- The eigenvalue problem grows from 2×2 per mode to (2 + N_organs) × (2 + N_organs)
- Organ positions parameterised by angular coordinates on the spheroid
- Computationally trivial; the hard part is getting anatomically realistic organ positions
  and attachment stiffnesses from the surgical/anatomy literature

**Codebase reuse:**
- `oblate_spheroid_ritz.py` — direct extension
- `organ_inclusions.py` — provides the effective-medium baseline for comparison
- `uncertainty_quantification.py` — Monte Carlo over organ mass and position variability

**New code needed:** ~400 lines
- Point-mass and spring terms in the Rayleigh-Ritz energy functional
- Non-axisymmetric mode extension (azimuthal harmonics)
- Organ position parameterisation from anatomical data

### Publication Venue
**Primary:** *JSV* or *Journal of Biomechanical Engineering*  
**Alternative:** *Medical Engineering & Physics*

### Effort: 6–8 weeks
- Week 1–2: Literature review on organ masses, positions, ligament stiffnesses
- Week 3–4: Extend Rayleigh-Ritz formulation; validate against effective-medium limit
- Week 5–6: Parametric study (organ mass, position, attachment stiffness)
- Week 7–8: Manuscript

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Organ masses too small to matter | Medium | Medium | Liver is 1.5 kg vs ~30 kg cavity — it's 5%. May produce measurable but small mode shifts. A "small effect" is still a publishable quantification. |
| Anatomical position data too uncertain | Medium | Medium | Use range from anatomy textbooks; frame as parametric rather than patient-specific |
| Non-axisymmetric extension is harder than expected | Medium | High | Fall back to axisymmetric point masses at the poles as a first approximation |
| Reviewer says "do FEA" | High | Medium | Argue that the analytical approach provides physical insight that FEA obscures; promise FEA validation as future work |

### Strategic Value: ★★★★☆
- **Natural extension of Papers 1 and 3** (scaling laws should include organ effects)
- **Steps toward clinical realism** without abandoning the analytical framework
- **Enables patient-specific predictions** (CT-derived organ volumes → model inputs)
- **Prerequisite for the laparoscopic insufflation paper** (Direction 3 in scout report)

### Potential Title
**"How Organs Shape Abdominal Resonance: Mass-Loading and Mode Localisation in a Fluid-Filled Viscoelastic Shell with Discrete Inclusions"**

### Key Starting References
1. `src/analytical/organ_inclusions.py` (this repo) — existing Hashin-Shtrikman analysis
2. Yeh, W.C. et al. (2002) "Elastic modulus measurements of human liver," *Ultrasound Med Biol* 28(4):467–474
3. Kemper, A.R. et al. (2012) "Biomechanical response of human spleen in tensile loading," *J Biomech* 45(2):348–355
4. Netter, F.H. (2014) *Atlas of Human Anatomy* — organ positions and peritoneal attachments
5. Soedel, W. (2004) *Vibrations of Shells and Plates*, 3rd ed., Marcel Dekker — point mass perturbation theory

---

## Topic 6: Ig Nobel Submission Strategy

### The Proposal
Determine which existing paper is the strongest Ig Nobel candidate and craft the
nomination angle.

### Assessment: This Is Not a Research Topic

The Ig Nobel strategy is already comprehensively documented in `docs/ig-nobel-strategy.md`.
The conclusions are clear and well-argued:

1. **Paper 1 is the flagship nominee** — directly addresses the famous question
2. **Paper 5 (borborygmi) is the most naturally Ig Nobel paper** — inherently comic,
   memorable title, real science
3. **Strategy: flagship + portfolio halo** — nominate around Paper 1, support with Papers 2–5
4. **Do not pivot the lab** — the Ig Nobel strategy is a communications overlay,
   not a research direction

**What remains:**
- Draft the nomination letter (already written in ig-nobel-strategy.md)
- Prepare the 24-second acceptance speech (Ig Nobel tradition)
- Time the nomination to follow Paper 1 publication

**Effort:** 1 week of communications work, not research  
**Verdict:** This is a task for the Communications agent, not the Research Scout.

---

## Strategic Analysis: How These Topics Fit Together

### The Programme Arc

```
Paper 1 (Modal analysis)     ──── Paper 3 (Scaling laws)
    │                                    │
    ├── Paper 2 (Gas pockets)            │
    │                                    │
    ├── Paper 4 (Bladder)                │
    │                                    │
    └── Paper 5 (Borborygmi)             │
                                         │
    ┌────────────────────────────────────┘
    │
    ├── Topic 1: Sub-bass perception    [EXTENDS coupling framework to broadband]
    │
    ├── Topic 3: Coupled acoustic-structural [DEEPENS the interior acoustics]
    │
    ├── Topic 5: Multi-organ interaction [ADDS anatomical realism]
    │
    ├── Topic 2: Experimental validation [GROUNDS everything in measurement]
    │
    └── Topic 4: Historical review      [FRAMES the programme for posterity]
```

### Sequencing Recommendation

**Phase 1 (now → 8 weeks):** Topic 1 (sub-bass perception)
- Highest code reuse, fastest to publication
- Extends the programme into a new audience (concerts, organs, nightclubs)
- Can run in parallel with Papers 1–5 revision cycles

**Phase 2 (weeks 6–16):** Topic 3 (coupled acoustic-structural)
- Most scientifically important
- Provides the foundation for future multi-organ and interior-acoustics work
- Harder but more impactful

**Phase 3 (weeks 12–20):** Topic 5 (multi-organ interaction)
- Natural follow-on to Topic 3 (uses the interior acoustic modes)
- Steps toward clinical realism

**Phase 4 (after Papers 1, 5 published):** Topic 4 (historical review)
- Needs published papers to have authority
- Low effort once prerequisites are met

**Phase 5 (when collaborator found):** Topic 2 (experimental validation)
- Critical for long-term credibility
- Cannot be done in-house
- Start looking for collaborators NOW even if the experiment is months away

### What About the Scout Report Topics?

The 2026-03-27 scout report proposed 10 topics. The best of those that don't overlap
with the 6 candidates above are:

1. **Whale song coupling** (Direction 2) — still excellent, especially as a companion
   to Topic 1 (both are "real-world sound source → abdominal coupling" papers)
2. **Belly flop problem** (Direction 1) — high synergy but requires SPH/ALE code we
   don't have
3. **Tesla's earthquake machine** (Direction 4) — fun but strategically peripheral
4. **Brown noise for sleep** (Direction 8) — natural companion to Topic 1; could be
   folded into the same paper

### The 10-Paper Programme

If all goes well, the Browntone programme would consist of:

| # | Paper | Status |
|---|-------|--------|
| 1 | Abdominal cavity modal analysis | Submission-ready |
| 2 | Gas pocket mechanotransduction | Minor revision |
| 3 | Allometric scaling laws | Short communication |
| 4 | Bladder fill-dependent resonance | Minor revision |
| 5 | Borborygmi multi-mode model | Accepted |
| 6 | Sub-bass perception thresholds | **NEW — Topic 1** |
| 7 | Coupled acoustic-structural modes | **NEW — Topic 3** |
| 8 | Multi-organ interaction | **NEW — Topic 5** |
| 9 | Experimental phantom validation | **NEW — Topic 2** |
| 10 | Historical review | **NEW — Topic 4** |

That is a genuine research programme — ten papers from a single oblate spheroidal
shell model and its extensions. The kind of thing that wins a prize or anchors a
thesis (or, in our case, proves that AI-assisted research can sustain a coherent
multi-year programme).

---

## Appendix: Code Reuse Matrix

| Module | Topic 1 | Topic 2 | Topic 3 | Topic 4 | Topic 5 |
|--------|---------|---------|---------|---------|---------|
| `oblate_spheroid_ritz.py` | ✓ | ✓ (predictions) | ✓ (structural modes) | — | ✓ (extend) |
| `energy_budget.py` | ✓ (extend to broadband) | ✓ (predictions) | — | — | — |
| `mechanotransduction.py` | ✓ | — | — | — | — |
| `gas_pocket_resonance.py` | ✓ (comparison) | ✓ (gas phantom) | — | — | — |
| `uncertainty_quantification.py` | ✓ | — | ✓ | — | ✓ |
| `organ_inclusions.py` | — | — | — | — | ✓ (extend) |
| `dimensional_analysis.py` | — | — | ✓ (non-dim coupled modes) | — | — |
| `borborygmi_model.py` | — | — | — | — | — |
| `bladder_model.py` | — | — | — | — | — |
| **New code (lines)** | ~200 | ~0 (exp. design only) | ~500–800 | ~0 | ~400 |

---

*Report ends. The Research Scout recommends proceeding with Topic 1 (sub-bass perception)
immediately, queueing Topic 3 (coupled model) as the next analytical paper, and beginning
the search for an experimental collaborator for Topic 2 in parallel.*
