# Research Scout — New Directions Report

**Date:** 27 March 2026
**Prepared for:** Browntone Computational Biomechanics Group (PI review)
**Scope:** Novel research directions adjacent to the abdominal vibroacoustics programme
**Context:** Builds on Papers 1-3 (shell resonance, gas pocket transduction, cross-species scaling) and the bladder spin-off

---

## Motivation

The Browntone programme has produced a mature analytical toolkit:

| Capability | Module | Reusability |
|---|---|---|
| Oblate spheroidal shell (Rayleigh-Ritz, flexural + breathing) | `oblate_spheroid_ritz.py` | High |
| Multi-layer composite wall (laminate theory) | `multilayer_wall.py` | High |
| Constrained gas-bubble resonance (Minnaert + wall loading) | `gas_pocket_resonance.py` | High |
| Acoustic-structure coupling (long-wavelength, reciprocity) | `acoustic_coupling.py`, `energy_budget.py` | High |
| Mechanotransduction chain (PIEZO thresholds) | `mechanotransduction.py` | Medium |
| Dimensional analysis and cross-species scaling | `dimensional_analysis.py` | High |
| Monte Carlo UQ with Sobol indices | `uncertainty_quantification.py` | High |
| Nonlinear Duffing / backbone curves | `nonlinear_analysis.py` | Medium |
| Viscous / non-Newtonian Stokes-layer corrections | `viscous_correction.py` | Medium |
| Orifice coupling (mouth to GI tract pathway) | `orifice_coupling.py` | Medium |

These tools are *far* more general than the brown-note question that spawned them. The
directions below exploit that generality while preserving the lab's brand: *rigorous
physics applied to questions that make people lean in*.

---

## Direction 1 — Borborygmi as Coupled Helmholtz-Bubble Oscillators

### Title
**"What Pitch Is a Growling Stomach? Analytical Model of Borborygmus Frequency from Gastrointestinal Gas-Pocket Geometry"**

### Venue
*Journal of the Acoustical Society of America (JASA)* — Biomedical Acoustics section

### Key Question
Borborygmi — stomach growling — are produced by peristaltic contractions propelling
gas-liquid mixtures through the GI lumen. Everyone can hear them; nobody has an
analytical model that predicts the characteristic frequency from first principles.
**Can we model a bowel segment as a variable-volume Helmholtz resonator coupled to a
constrained gas bubble, and predict the 10-200 Hz spectral signature that
gastroenterologists use (qualitatively) for diagnosis?**

### Why Novel
Clinical auscultation of bowel sounds dates to Laennec (1816), and digital acoustic
analysis of bowel sounds is an active field (e.g., Du et al. 2023, *Sensors*).
However, every published model is **phenomenological** — recording, segmenting, and
classifying sounds with ML, without a physics-based forward model of *how the sound
is generated*. Acoustic source models exist for the larynx (Titze, 1988) and for
flatus (Stalberg and Noguchi 1982), but the growling-stomach source mechanism
has never been treated analytically. The closest work is Minnaert-bubble models in
bubbly liquids (Leighton 1994), but these assume free spherical bubbles, not gas
pockets constrained by a viscoelastic tube wall.

### Feasibility
- **Difficulty:** Medium
- **Methods:** Analytical (Helmholtz + constrained-Minnaert coupling) + lightweight
  computational (parameter sweeps, Monte Carlo for inter-individual variation)
- **Codebase reuse:** Direct extension of `gas_pocket_resonance.py` (constrained
  bubble model) and `orifice_coupling.py` (acoustic impedance of tube segments).
  Add a Helmholtz-resonator module for the gas-pocket + lumen-constriction geometry.
- **New code needed:** ~300 lines — Helmholtz neck impedance, coupled oscillator
  eigenvalue problem, peristaltic forcing function.

### Timeline
6-8 weeks to a submission-ready manuscript.

### Amusement Factor: 5/5
A paper titled "What pitch is a growling stomach" will be read by every acoustician
with a sense of humour, shared on social media, and cited by the digital-bowel-sounds
community who desperately need a physics-based model to anchor their ML classifiers.
The supplementary audio files practically write themselves.

---

## Direction 2 — Blast-Wave Coupling and the Combat Defecation Reflex

### Title
**"Blast-Wave Coupling to the Human Abdominal Cavity: Can Infrasonic Overpressure Trigger the Defecation Reflex?"**

### Venue
*Journal of Biomechanics* or *Shock Waves* (Springer)

### Key Question
Military personnel report involuntary defecation during blast exposure — a phenomenon
documented but unexplained in combat medicine. A blast wave is a broadband impulse
containing massive energy at infrasonic frequencies (1-50 Hz). **Does the blast
overpressure time-history, when coupled through the abdominal shell model and
mechanotransduction chain, produce tissue displacements exceeding the PIEZO-channel
and recto-anal inhibitory reflex (RAIR) thresholds?**

### Why Novel
Blast injury research focuses overwhelmingly on **primary blast lung injury** (Cernak
and Noble-Haeusslein 2010) and **blast TBI** (Courtney and Courtney 2015).
Abdominal blast injuries are studied only in terms of *laceration* and *rupture*
(high overpressure regime). The **sub-injury, physiological-effect** regime —
overpressures too low to cause organ damage but sufficient to trigger
mechanosensitive pathways — is an uncharted gap. Our existing energy budget and
mechanotransduction framework were *built* for this question; we just need to replace
the harmonic forcing with a Friedlander waveform and integrate over the impulse
response.

### Feasibility
- **Difficulty:** Medium
- **Methods:** Analytical (Friedlander impulse into modal FRF convolution) +
  computational (time-domain Newmark-beta integration for nonlinear regime)
- **Codebase reuse:** `energy_budget.py` (absorption cross-section adapted for impulse energy),
  `mechanotransduction.py` (PIEZO thresholds), `nonlinear_analysis.py` (Duffing for
  high-amplitude response), `modal_participation.py` (multi-mode superposition).
- **New code needed:** ~200 lines — Friedlander waveform generator, impulse response
  integrator, RAIR threshold model.

### Timeline
8-10 weeks (literature review of blast parameters is the bottleneck).

### Amusement Factor: 4/5
The subject is deadly serious — blast-induced GI dysfunction is a real combat
casualty issue — but the connection to the "brown note" is irresistible. A paper
that rigorously links the mythical brown note to actual blast medicine will be
read by both the JSV/JASA crowd and the military medicine community.

---

## Direction 3 — Laparoscopic Insufflation and Intra-Operative Resonance

### Title
**"Natural Frequencies of the CO2-Insufflated Abdomen: How Laparoscopic Pneumoperitoneum Transforms Shell Resonance"**

### Venue
*Proceedings of the Royal Society A* (Applied Maths / Mechanics) or *Medical Engineering and Physics*

### Key Question
During laparoscopic surgery the abdomen is inflated with CO2 to 12-15 mmHg,
transforming it from a fluid-filled oblate spheroid into a **gas-filled, nearly
spherical pressure vessel** with a thin fluid layer coating the walls. This
fundamentally changes the resonance picture: the gas stiffness replaces the
incompressible-fluid assumption, the breathing mode drops from kilohertz to a
plausible tens-of-hertz range, and surgical instrument vibrations (ultrasonic
scalpels at 55 kHz, electrosurgery at 0.3-3 MHz, but also mechanical handle
vibrations at 10-200 Hz) now couple into a qualitatively different cavity.
**What are the modal frequencies of the insufflated abdomen, and could surgical
tool vibrations excite them?**

### Why Novel
Pneumoperitoneum-related complications (subcutaneous emphysema, gas embolism,
shoulder-tip pain from diaphragmatic irritation) are well documented, but the
**vibroacoustic** properties of the insufflated cavity have never been studied.
No published model exists for the natural frequencies of a gas-filled abdominal
cavity under surgical conditions. The transformation from fluid-filled to
gas-filled fundamentally changes every term in the Rayleigh-Ritz formulation:
fluid added mass drops by 3 orders of magnitude, gas compressibility creates a
new breathing-mode stiffness, and the shell geometry changes from oblate to
near-spherical.

### Feasibility
- **Difficulty:** Medium (the hard part — the Ritz solver — already exists)
- **Methods:** Analytical (modify `oblate_spheroid_ritz.py` for gas fill;
  recompute fluid added mass with rho_gas of approx 1.8 kg/m3 for CO2 at 15 mmHg;
  add breathing mode with gas stiffness K = gamma * P0).
- **Codebase reuse:** `oblate_spheroid_ritz.py` (core solver — change rho_fluid),
  `gas_pocket_resonance.py` (Minnaert physics), `multilayer_wall.py` (peritoneum
  vs full wall distinction), `parametric_analysis.py` (insufflation pressure sweep).
- **New code needed:** ~400 lines — gas-fill Ritz variant, insufflation geometry
  model (oblate to spherical transition vs pressure), surgical tool spectral input.

### Timeline
8-10 weeks.

### Amusement Factor: 3/5
Less "pub quiz" appeal than the others, but genuine clinical novelty. Surgeons would
actually read this. The mental image of a surgeon's harmonic scalpel accidentally
ringing the patient's abdomen like a bell is memorable enough.

---

## Direction 4 — The Pregnant Abdomen Under Whole-Body Vibration

### Title
**"Resonance of the Gravid Uterus: A Fluid-Filled Shell-Within-a-Shell Model for Fetal Vibration Exposure"**

### Venue
*Journal of Sound and Vibration (JSV)* — short communication, or *Journal of Biomechanics*

### Key Question
Pregnant women in occupational settings (bus/truck drivers, helicopter aircrew,
agricultural machinery operators) are exposed to whole-body vibration at 1-20 Hz.
The gravid uterus is itself a fluid-filled viscoelastic shell (amniotic fluid +
fetus) nested inside the larger abdominal shell. **How does the nested-shell geometry
shift the abdominal resonance frequencies, and is there an amplification (or
shielding) effect at the fetal position?** Current occupational guidance (ISO 2631,
EU Directive 2002/44/EC) makes no distinction for pregnancy.

### Why Novel
A 2019 Cochrane review (Palmer et al.) found insufficient evidence to set
vibration limits for pregnant workers. Epidemiological studies (Croteau 2020)
associate occupational vibration with preterm birth, but the *mechanism* is
unknown. No biomechanical model exists for the coupled resonance of the gravid
uterus inside the abdominal cavity. The problem is a textbook extension of
our existing model: replace the homogeneous fluid fill with a **concentric
shell inclusion** (uterine wall) enclosing a second fluid domain (amniotic
fluid) plus a viscoelastic solid (fetus). The Hashin-Shtrikman
effective-medium approach from `organ_inclusions.py` provides the starting
framework.

### Feasibility
- **Difficulty:** Medium-Hard (the concentric-shell eigenvalue problem requires
  matching boundary conditions at two interfaces)
- **Methods:** Analytical (concentric oblate spheroids, matched BCs) +
  computational (parameter sweep over gestational age to uterus size)
- **Codebase reuse:** `oblate_spheroid_ritz.py` (outer shell),
  `organ_inclusions.py` (effective medium with inclusion),
  `dimensional_analysis.py` (scaling with uterus size),
  `uncertainty_quantification.py` (Sobol indices for gestational parameters).
- **New code needed:** ~600 lines — concentric-shell Ritz formulation, fetus
  as viscoelastic inclusion, gestational-age parameter model.

### Timeline
10-14 weeks (the concentric-shell theory is the main challenge).

### Amusement Factor: 3/5
Less whimsical than the stomach growling paper, but the occupational health
implications are substantial. A title referencing "resonance of the gravid
uterus" will draw attention from both the acoustics and obstetric communities.
Significant potential for real-world impact on workplace safety standards.
