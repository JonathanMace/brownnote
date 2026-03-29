# Mid-Tenure Research Statement

**Opus** — Principal Investigator, Browntone Research Lab
Faculty Supervisor: Jonathan Mace
March 2026

---

## 1. Research Vision

Every culture has its acoustic folklore. The "brown note" — the claim that a
specific infrasonic frequency can induce involuntary defecation — is among the
most persistent and least examined. NASA tested it obliquely during the Apollo
programme, subjecting volunteers to sound pressure levels of 140–154 dB without
observing gastrointestinal effects. South Park devoted an episode to it (Parker
and Stone, "The Brown Noise", S3E17, 1999). Yet for all its notoriety, no
prior study had subjected the hypothesis to a first-principles mechanical
analysis. We found that oversight unacceptable.

What began as a single analytical model has grown into a unified research
programme in **vibroacoustic resonance of fluid-filled biological cavities**.
The founding question — can airborne sound make the abdomen resonate? — turns
out to be the wrong question, and wrong questions are often the most productive.
The abdomen *does* resonate, at frequencies squarely within the range of
occupational whole-body vibration (4–10 Hz). But airborne sound cannot
meaningfully excite those modes, because at infrasonic frequencies the acoustic
wavelength exceeds 85 metres — over 500 times the abdominal radius — and the
resulting scattering penalty suppresses coupling by four to five orders of
magnitude. The brown note, as popularly conceived, is a physical impossibility.

This negative result, far from closing the investigation, opened it. If whole-
cavity resonance cannot be driven acoustically, what about local gas inclusions?
If the framework works for the abdomen, does it generalise to other organs? To
other species? Can the same physics that disproves folklore explain the sounds
that clinicians actually hear when they press a stethoscope to the belly?

The programme's intellectual contribution is threefold. First, we provide a
**transferable analytical framework** — oblate spheroidal shell theory with
energy-consistent fluid–structure coupling — that can be applied to any fluid-
filled biological cavity. Second, we demonstrate that **dimensional analysis
and scaling laws** reveal quasi-universal behaviour across mammalian scales,
connecting rat models to human physiology through a single dimensionless
frequency. Third, we show that **folklore, taken seriously, seeds rigorous
science**: the brown note hypothesis led directly to new mechanistic
explanations for occupational vibration symptoms, non-invasive bladder
diagnostics, and the first physics-based model of bowel sounds.

The target venues reflect the programme's ambition: the *Journal of Sound and
Vibration* for the structural acoustics papers and the *Journal of the
Acoustical Society of America* for the biomedical acoustics contributions.

## 2. Accomplishments to Date

The programme has produced five papers in a single extended research campaign,
each building on its predecessors to form a coherent narrative arc: from whole-
cavity analysis, through local inclusions and cross-species scaling, to organ-
level extension and clinical acoustics.

### Paper 1 — Modal Analysis of the Abdominal Cavity

*Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell:
Implications for the Existence of the "Brown Note"*
Target: *Journal of Sound and Vibration* (~44 pages)

The foundational paper models the human abdomen as a fluid-filled viscoelastic
oblate spheroidal shell (semi-major axis *a* = 0.18 m, semi-minor axis
*c* = 0.12 m, wall thickness *h* = 10 mm, elastic modulus *E* = 0.1 MPa).
The analysis predicts a lowest flexural resonance at *f*₂ ≈ 4.0 Hz, with
higher modes at *f*₃ ≈ 6.3 Hz and *f*₄ ≈ 8.9 Hz — precisely within the
ISO 2631 band of peak human sensitivity to whole-body vibration. The breathing
mode lies at approximately 2,500 Hz, dominated by fluid bulk modulus and
irrelevant to infrasound.

The paper's central quantitative result is the coupling ratio: mechanical whole-
body vibration drives abdominal wall displacement **6.6 × 10⁴ times** more
effectively than airborne sound at equivalent excitation levels. At 120 dB SPL,
energy-consistent airborne displacement reaches just 0.014 μm — two orders of
magnitude below the 0.5–2.0 μm threshold for PIEZO mechanosensitive channel
activation. Reaching 1 μm by airborne excitation alone would require
approximately 158 dB, well beyond any plausible environmental exposure. By
contrast, whole-body vibration at the EU action value of 0.5 m/s² produces
relative wall displacements of 4,586 μm.

A 10,000-sample Monte Carlo uncertainty quantification identifies elastic
modulus as the dominant parameter (Sobol total-order index *S*_T = 0.86),
with 90% of configurations placing *f*₂ within 3.3–15.5 Hz. A six-layer
multilayer wall model predicts *f*₂ = 4.6 Hz, within 16% of the homogeneous
baseline.

### Paper 2 — Gas Pockets as Acoustic Transducers

*Bowel Gas as an Acoustic Transducer: A Constrained Bubble Model for
Infrasound-Induced Mechanotransduction in the Gastrointestinal Tract*
Target: *JASA* (~16 pages)

Where Paper 1 demonstrated that whole-cavity resonance cannot be driven
acoustically, Paper 2 identifies the most plausible alternative pathway:
intraluminal gas pockets acting as local acoustic transducers. Using a
Church (1995) encapsulated-bubble formulation adapted for intestinal wall
properties, the model predicts that gas pockets of 5–100 mL produce tissue-
wall displacements **35–100 times** larger than the whole-cavity flexural mode
at the same incident SPL. A 100 mL pocket reaches the PIEZO activation
threshold at approximately 111 dB; the whole-cavity pathway requires over
180 dB. A 10,000-sample Monte Carlo population model shows that at 120 dB,
nearly all simulated individuals exceed the mechanotransduction threshold,
with median peak displacement of approximately 1.2 μm.

### Paper 3 — Cross-Species Scaling Laws

*Scaling Laws for the Flexural Resonance of Fluid-Filled Viscoelastic Shells:
Predictions Across Mammalian Scales*
Target: *Journal of Sound and Vibration — Short Communication* (~11 pages)

Paper 3 applies Buckingham Pi dimensional analysis to the 10-parameter shell
model, reducing the flexural eigenfrequency problem to five governing
dimensionless groups. A 1,458-point parametric study confirms algebraic
consistency with maximum relative error of 7.9 × 10⁻¹⁶. Cross-species
predictions for rat (*f*₂ = 15.7 Hz), cat (7.2 Hz), pig (4.5 Hz), and human
(3.9 Hz) reveal a quasi-universal dimensionless frequency **Π₀ ≈ 0.07**
across a six-fold range in body size. The airborne scattering penalty
*ℛ*_scat remains in the 10³–10⁴ range regardless of species, validating the
use of animal models for mechanical but not acoustic excitation studies. The
breathing mode reaches 20 Hz only for an organism of radius ~20 m — confirming
its irrelevance to biological infrasound.

### Paper 4 — Bladder Resonance

*Resonant Frequencies of the Human Urinary Bladder: A Fluid-Filled
Viscoelastic Shell Model*
Target: *Journal of Sound and Vibration* (~27 pages)

Paper 4 extends the analytical framework to the urinary bladder, a smaller,
thinner-walled, more compliant organ whose mechanical properties vary with fill
state. The model predicts a characteristic U-shaped frequency curve: geometric
softening (increasing radius, thinning wall) competes with strain-stiffening
of the detrusor muscle, producing a minimum *f*₂ = 13.5 Hz at 222 mL. For
physiologically relevant fill volumes (150–500 mL), the *n* = 2 mode spans
13.5–17.1 Hz. The mechanical-to-airborne coupling ratio is *ℛ* ≈ 6,400 —
smaller than the abdominal value owing to the bladder's reduced size, but
still decisive. Whole-body vibration at 0.5 m/s² produces cyclic wall strains
of 0.1–0.4%, at strain rates approximately 500 times faster than normal
filling. The paper offers the first mechanistic explanation for vibration-
induced urinary urgency, a well-documented occupational complaint.

### Paper 5 — Borborygmi

*What Pitch Is a Growling Stomach? A Unified Multi-Mode Acoustic Model of
Borborygmi*
Target: *JASA* (~20 pages)

Paper 5 completes the arc by turning from vibration response to sound
*generation*. A unified five-mechanism model — free Minnaert oscillation,
tissue-constrained bubble resonance, Helmholtz resonance through peristaltic
constrictions, axial piston modes, and radial breathing of gas columns —
predicts bowel sound frequencies from measurable anatomical parameters with
no fitted coefficients. The tissue-constrained bubble model predicts 135–440 Hz
for gas pockets of 1–50 mL, substantially overlapping the clinically observed
healthy band of 200–550 Hz. Inferred pocket volumes (approximately 3 mL for
the healthy 340 Hz peak; 5 mL for small bowel obstruction at 288 Hz) are
physiologically plausible. Wall stiffness proves secondary: a 100-fold
increase in elastic modulus shifts the constrained frequency by only 9%.

## 3. Methodological Contributions

### Analytical Toolchain

The programme's primary methodological contribution is a **modular analytical
framework** for vibroacoustic resonance of fluid-filled biological cavities.
The framework comprises four interlocking components:

1. **Oblate spheroidal shell theory** with Donnell–Mushtari thin-shell
   kinematics, fluid added-mass coupling, and viscoelastic loss (Papers 1, 3,
   4). The energy-consistent formulation avoids the 13× overestimate that
   arises from pressure-based displacement calculations.

2. **Church (1995) constrained-bubble model**, adapted from ultrasound contrast
   agents to intestinal gas pockets at infrasonic frequencies (Paper 2). The
   adaptation accounts for tissue-scale wall thickness, physiological elastic
   moduli, and sub-resonant compliance.

3. **Buckingham Pi dimensional analysis** yielding exact scaling laws that
   reduce high-dimensional parameter spaces to a small number of governing
   groups (Paper 3). The closed-form expressions enable cross-species
   extrapolation without repeated numerical computation.

4. **Energy-consistent coupling comparison**, providing a common framework for
   quantifying mechanical versus airborne excitation pathways through a single
   dimensionless ratio *ℛ* (Papers 1, 3, 4).

Together, these components are transferable: they have already been applied to
two distinct organs (abdomen and bladder), four mammalian species, and both
excitation and radiation problems.

### Computational Infrastructure

The research programme operates through a bespoke computational infrastructure
designed for reproducibility and self-consistency:

- **203 passing tests** covering analytical modules, figure generation, and
  parameter consistency.
- **130+ merged pull requests**, each reviewed before integration. The `main`
  branch is protected; all changes enter through PRs.
- **Automated three-reviewer panels** (Reviewer A: domain significance;
  Reviewer B: adversarial rigour; Reviewer C: computational reproducibility),
  with papers undergoing up to eight review rounds before acceptance.
- **Cross-paper consistency auditing**: a dedicated agent verifies that
  canonical parameter values, derived quantities, and shared claims remain
  synchronised across all five manuscripts.
- **Reproducible figure generation**: all publication figures are generated
  programmatically from the analytical modules, with `matplotlib.use('Agg')`
  for headless execution.

### AI-Assisted Research Methodology

The programme itself constitutes a methodological experiment. Sixteen
specialised AI agents — spanning paper writing, data analysis, simulation
engineering, literature monitoring, and adversarial review — operate within a
structured workflow: DO → REVIEW → LOG → COMPILE → COMMIT. The human faculty
supervisor provides research direction, domain scepticism, and quality
judgement; the AI system handles analytical derivation, code implementation,
LaTeX drafting, figure generation, and review logistics. This division of
labour is not a replacement for expertise but a **compression of research
overhead**, enabling a five-paper portfolio to emerge from approximately 48
hours of wall-clock interaction.

## 4. Research Trajectory

### Near-Term: Submission and Peer Review

The immediate priority is **external peer review** of the five-paper portfolio.
Papers 1 and 2 are submission-ready and will be submitted first, as they
establish the core framework and the gas-pocket transduction mechanism. Paper 3,
currently under internal revision, follows as a short communication. Papers 4
and 5, in active development, will be submitted as the earlier papers progress
through review. The staggered submission strategy allows reviewer feedback on
the foundational papers to inform final revisions of the later manuscripts,
while the shared analytical framework ensures cross-paper consistency.

### Medium-Term: Experimental Validation and Model Extension

The analytical predictions are, by design, falsifiable. Three experimental
programmes would test them directly:

**Phantom validation.** An oblate spheroidal silicone phantom (*a* = 0.18 m,
*c* = 0.12 m, *h* = 10 mm) filled with water and instrumented with laser
vibrometry would test the predicted *f*₂ ≈ 3.6 Hz (Dragon Skin 10A silicone)
against the analytical model. Estimated consumables cost is under US$3,100.

**Clinical bowel sound recordings.** High-fidelity recordings from healthy
subjects and patients with known bowel obstruction would test Paper 5's
prediction that dominant frequencies map to gas-pocket volumes of 1–5 mL
via the constrained-bubble model. Frequency inversion from acoustic spectra
to estimated pocket volumes would provide a novel, non-invasive diagnostic
indicator.

**Coupled-cavity and transient models.** The current framework treats each
organ as an isolated cavity. Medium-term extensions would model coupled
systems — the bladder within the pelvic cavity, the stomach communicating
with the intestinal gas column — and incorporate transient response to
impulsive or swept-frequency excitation.

### Long-Term: Clinical and Technological Applications

The programme's long-term trajectory extends in three directions:

**Non-invasive elastography.** If tissue stiffness dominates the frequency
response (as the Sobol analysis of Paper 1 indicates, with *S*_T = 0.86
for elastic modulus), then measured resonant frequencies could be inverted
to estimate *in vivo* tissue mechanical properties. This would complement
existing shear-wave elastography techniques with a whole-organ, low-frequency
alternative.

**Acoustic metamaterial analogies.** The constrained-bubble physics of
Paper 2 shares mathematical structure with locally resonant acoustic
metamaterials. Exploring this analogy could yield insights into both
biological acoustics and metamaterial design — gas pockets as naturally
occurring sub-wavelength resonators embedded in a viscoelastic matrix.

**Clinical diagnostic applications.** Paper 5's finding that borborygmi
frequencies encode gas-pocket geometry suggests a pathway toward automated
bowel sound analysis for monitoring gastrointestinal motility, detecting
obstruction, and assessing post-operative ileus — applications where
continuous, non-invasive monitoring would be clinically valuable.

## 5. Broader Impact

### From Folklore to Framework

The programme demonstrates that **folklore can be a legitimate starting point
for rigorous science**. The brown note hypothesis, dismissed by most
acousticians as a joke, led to the first systematic analysis of abdominal
vibroacoustic resonance — and thence to a five-paper portfolio spanning
cavity mechanics, bubble dynamics, scaling laws, organ extension, and clinical
acoustics. The lesson is not that folklore is reliable, but that the effort
required to *disprove* it rigorously often produces frameworks of independent
value.

### Generalisable Framework

The analytical toolchain is not specific to the abdomen or the brown note.
Any fluid-filled biological cavity — bladder, lung, eye, joint capsule — can
be modelled within the same framework by substituting appropriate geometric
and material parameters. The scaling laws of Paper 3 provide a principled
basis for extrapolating between species without recourse to empirical
allometric fitting. The coupling ratio *ℛ* offers a unified metric for
comparing excitation pathways across organs, frequencies, and exposure
scenarios.

### AI-Assisted Research as Method

The programme is, to our knowledge, among the first to employ a structured
multi-agent AI system as the primary research executor under human supervision.
The methodology — specialised agents, adversarial review panels, consistency
auditing, reproducible computation — is itself a contribution to the discourse
on how computational research is organised and conducted. The infrastructure
is open-source and documented, offering a template for other research groups
exploring AI-assisted workflows. The central insight is that AI's comparative
advantage lies not in replacing scientific judgement but in **compressing the
overhead** that separates a research idea from a publishable manuscript.

## 6. Selected Publications

1. J. Mace and B. R. Mace, "Modal Analysis of a Fluid-Filled Viscoelastic
   Oblate Spheroidal Shell: Implications for the Existence of the 'Brown
   Note'," *Journal of Sound and Vibration*, in preparation, 2026. (~44 pp.)

2. J. Mace and B. R. Mace, "Bowel Gas as an Acoustic Transducer: A
   Constrained Bubble Model for Infrasound-Induced Mechanotransduction in the
   Gastrointestinal Tract," *The Journal of the Acoustical Society of
   America*, in preparation, 2026. (~16 pp.)

3. J. Mace and B. R. Mace, "Scaling Laws for the Flexural Resonance of
   Fluid-Filled Viscoelastic Shells: Predictions Across Mammalian Scales,"
   *Journal of Sound and Vibration — Short Communication*, in preparation,
   2026. (~11 pp.)

4. J. Mace and B. R. Mace, "Resonant Frequencies of the Human Urinary
   Bladder: A Fluid-Filled Viscoelastic Shell Model," *Journal of Sound and
   Vibration*, in preparation, 2026. (~27 pp.)

5. J. Mace and B. R. Mace, "What Pitch Is a Growling Stomach? A Unified
   Multi-Mode Acoustic Model of Borborygmi," *The Journal of the Acoustical
   Society of America*, in preparation, 2026. (~20 pp.)

---

*Prepared March 2026. Browntone Research Lab, Microsoft Research / University
of Auckland.*
