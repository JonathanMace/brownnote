# Research Scout Report — 27 March 2026

**Prepared for:** Computational Biomechanics Group
**Context:** Follow-on projects from the "Browntone" infrasound–abdomen resonance study
**Selection criteria:** Scientifically rigorous, computationally tractable, memorably unusual

---

## Executive Summary

Ten candidate research topics are presented below, ranging across acoustics,
fluid–structure interaction, biomechanics, and structural dynamics. Each was
selected to exploit our existing analytical toolkit (shell theory, FSI modal
analysis, Rayleigh–Ritz methods, Sobol UQ) while asking the kind of question
that gets read at conferences and shared on Twitter. Synergy scores reflect
reuse of code, methods, and domain knowledge from the Browntone project.

| # | Short Title | Domain | Difficulty | Synergy |
|---|-------------|--------|------------|---------|
| 1 | The Belly Flop Problem | Biomech / Fluid–Structure | Medium | ★★★★★ |
| 2 | Can a Whale Song Vibrate Your Organs? | Bioacoustics / FSI | Medium | ★★★★☆ |
| 3 | Tesla's Earthquake Machine Revisited | Structural Dynamics | Easy–Med | ★★★☆☆ |
| 4 | The Skull as a Drum | Cranial Acoustics / FSI | Hard | ★★★★★ |
| 5 | Why Your Bladder Hates Long Bus Rides | Occupational Health / WBV | Medium | ★★★★★ |
| 6 | Can a Cat's Purr Heal Bones? | Vibroacoustics / Biomech | Medium | ★★★★☆ |
| 7 | The Vuvuzela Problem | Acoustics / Public Health | Easy–Med | ★★★☆☆ |
| 8 | Brown Noise for Sleep — Hype or Physics? | Acoustics / Biomech | Medium | ★★★★★ |
| 9 | The Stadium Earthquake | Seismo-acoustics | Medium | ★★★☆☆ |
| 10 | The Optimal Pub Dart Under the Influence | Sport Biomech / UQ | Easy | ★★☆☆☆ |

---

## Topic 1 — The Belly Flop Problem

### 1. The Hook
Everyone who has belly-flopped off a diving board knows the sting. But at what
height does a belly flop go from humiliating to genuinely dangerous — and can
we compute the exact pressure map on a deformable human torso hitting water?

### 2. The Science
Human water entry at near-zero angle of attack produces an impulsive
hydrodynamic load distributed across the anterior torso. The research question
is: **what is the coupled fluid–structure response of a viscoelastic,
multi-layered abdominal wall impacting a free surface, and at what
height/velocity does the resulting intra-abdominal pressure exceed injury
thresholds?** This requires coupling SPH or ALE free-surface hydrodynamics
with a layered shell model of the abdominal wall (skin → fat → muscle →
fascia → peritoneum), tracking both the slamming pressure pulse and the
transmitted wave into the visceral cavity. The key output is a height-dependent
injury risk curve mapping belly-flop height to peak intra-abdominal pressure,
compared against known thresholds for organ contusion (~100 kPa) and splenic
rupture (~300 kPa).

### 3. The Gap
Water-entry studies overwhelmingly focus on **rigid bodies** (missiles,
ship hulls, Olympic divers entering feet-first). The few biomechanical
studies of water impact focus on spinal injury from cliff jumping or
back-first impacts, not the flat-torso "belly flop" geometry. No published
study couples realistic tissue constitutive models with free-surface
slamming for the anterior torso. The Browntone multi-layer abdominal wall
model is directly applicable.

### 4. Feasibility
- **Difficulty:** Medium
- **Methods:** Computational (SPH/ALE + FEA), with analytical slamming
  pressure estimates (Wagner theory) for validation
- **Estimated effort:** 3–4 months
- **Key starting references:**
  1. Wagner, H. (1932) "Über Stoß- und Gleitvorgänge an der Oberfläche von
     Flüssigkeiten," *ZAMM* 12(4), 193–215.
  2. Korobkin, A. (2004) "Analytical models of water impact," *Eur. J. Appl.
     Math.* 15, 821–838.
  3. Viano, D.C. et al. (1989) "Bolster impacts to the knee and tibia of
     human cadavers…" *Stapp Car Crash J.* 33, 389–408.
  4. Barber, J. et al. (2013) "Water entry of rigid bodies," *Proc. Roy.
     Soc. A* 469, 20120597.
  5. Our own multi-layer wall model: `src/analytical/multilayer_wall.py`

### 5. Publication Venue
*Journal of Biomechanical Engineering* (ASME) or *Physics of Fluids* (AIP)

### 6. Potential Title
**"How High Is Too High? A Computational Fluid–Structure Model of the Human
Belly Flop"**

### 7. Synergy Score: ★★★★★ (5/5)
Directly reuses the multi-layer abdominal wall model, tissue constitutive
parameters, intra-abdominal pressure framework, and the entire FSI coupling
strategy. This is essentially the Browntone model with impulsive rather than
harmonic loading.

---

## Topic 2 — Can a Whale Song Vibrate Your Organs?

### 1. The Hook
A blue whale's call reaches 188 dB re 1 μPa — louder than a jet engine. Divers
near singing whales report feeling vibrations "in their chest." Is this
subjective awe, or is the acoustic field genuinely coupling into human organ
resonances underwater?

### 2. The Science
Underwater, the impedance mismatch between water and soft tissue nearly
vanishes (ρc ratio ≈ 1.04), meaning acoustic energy couples into the body
far more efficiently than in air. The research question is: **given the
measured source spectrum of large whale calls (10–200 Hz, up to 190 dB re
1 μPa at 1 m), what are the induced tissue displacements and
intra-abdominal/intra-thoracic pressures in a submerged human at realistic
encounter distances (5–50 m)?** This directly extends our Browntone acoustic
coupling analysis — but now the (ka)² penalty that made airborne coupling
negligible is replaced by near-unity impedance matching.

### 3. The Gap
The bioacoustics literature on whale song focuses on effects *on whales* and
on long-range propagation. The occupational/recreational diving literature
addresses anthropogenic noise (sonar, pile-driving) but not biological
sources. Nobody has quantified the **tissue-level biomechanical response** of
a submerged human body to cetacean vocalizations using a proper FSI model. The
near-field (non-plane-wave) structure of whale calls at close range is also
typically neglected.

### 4. Feasibility
- **Difficulty:** Medium
- **Methods:** Analytical (modified acoustic coupling with underwater
  impedance matching) + computational FEA validation
- **Estimated effort:** 2–3 months
- **Key starting references:**
  1. Aroyan, J.L. et al. (1992) "Acoustic models of sound production and
     propagation," *Marine Mammal Sensory Systems*, Plenum.
  2. Cummings, W.C. & Thompson, P.O. (1971) "Underwater sounds from the blue
     whale," *JASA* 50, 1193–1198.
  3. Cudahy, E. & Parvin, S. (2001) "The effects of underwater blast on
     divers," *NMRI Technical Report*.
  4. Junger, M.C. & Feit, D. (1986) *Sound, Structures, and Their
     Interaction*, MIT Press. (FSI formulation we already use.)
  5. Our own `src/analytical/acoustic_coupling.py` (impedance matching model).

### 5. Publication Venue
*Journal of the Acoustical Society of America (JASA)* — perfect fit for
the bioacoustics–FSI crossover

### 6. Potential Title
**"Whale Song and Wet Suits: Acoustic Coupling of Cetacean Calls into the
Submerged Human Body"**

### 7. Synergy Score: ★★★★☆ (4/5)
The acoustic coupling framework ports directly — we simply change the
external medium from air to water and remove the (ka)² penalty. The
abdominal shell model, fluid-filled cavity formulation, and Sobol UQ
pipeline are all reusable. New work: near-field source model, underwater
tissue properties.

---

## Topic 3 — Tesla's Earthquake Machine: A Quantitative Reassessment

### 1. The Hook
Nikola Tesla claimed a handheld steam-powered oscillator nearly shook his
Manhattan laboratory to pieces in 1898. Could a 7 lb device really threaten
a building — or was Tesla simply a world-class storyteller?

### 2. The Science
The question reduces to an **energy balance and resonance amplification
problem**: given a small mechanical oscillator producing F₀ ≈ 10–50 N at
f ≈ 10–20 Hz, what is the steady-state displacement amplitude of a
multi-storey masonry building if the oscillator is perfectly tuned to the
building's fundamental mode? The analysis requires: (a) estimating the
modal mass, stiffness, and damping ratio of a circa-1890 NYC masonry
building; (b) computing the resonant amplification Q = 1/(2ζ); (c)
comparing the predicted displacement against perceptibility thresholds
(~0.1 mm) and structural damage thresholds (~10 mm inter-storey drift).
A parametric study over plausible building types and oscillator outputs
determines the envelope of feasibility.

### 3. The Gap
Despite enormous popular interest, **no peer-reviewed engineering analysis**
of Tesla's specific claim exists. Popular accounts either credulously repeat
the story or dismissively wave it away. A proper structural dynamics
treatment — with honest uncertainty bounds on 1890s building properties —
would be a genuine contribution to both engineering history and public
understanding of resonance.

### 4. Feasibility
- **Difficulty:** Easy–Medium
- **Methods:** Analytical (SDOF/MDOF resonance), computational (simple FE
  modal analysis for validation)
- **Estimated effort:** 4–8 weeks
- **Key starting references:**
  1. Tesla, N. (1919) "My Inventions," *Electrical Experimenter*.
  2. Chopra, A.K. (2017) *Dynamics of Structures*, 5th ed., Pearson.
     (Standard structural dynamics textbook.)
  3. Brownjohn, J.M.W. (2003) "Ambient vibration studies for system
     identification of tall buildings," *Earthq. Eng. Struct. Dyn.*
     32, 71–95.
  4. O'Neill, J. (1944) *Prodigal Genius: The Life of Nikola Tesla*.
  5. Wirsching, P. et al. (2006) *Random Vibrations: Theory and Practice*,
     Dover.

### 5. Publication Venue
*Proceedings of the Royal Society A* (crossover physics/history) or
*Journal of Sound and Vibration*

### 6. Potential Title
**"Could Tesla's Oscillator Really Shake a Building? A Structural Dynamics
Analysis of the 1898 'Earthquake Machine' Claim"**

### 7. Synergy Score: ★★★☆☆ (3/5)
Resonance, Q-factors, and modal analysis are core to our framework, but
this is structural (not biological) and doesn't involve FSI. The UQ
pipeline (Sobol sensitivity over uncertain building parameters) ports
directly.

---

## Topic 4 — The Skull as a Drum: Modal Analysis of the Human Cranium

### 1. The Hook
The human skull is a fluid-filled elastic shell with an opening at the bottom.
It is, in every meaningful sense, a drum. Nobody has computed its full modal
spectrum with coupled brain–CSF acoustics — and the results may explain why
certain sounds feel like they resonate *inside your head*.

### 2. The Science
**What are the coupled structural-acoustic modes of the human cranium
(bone + cerebrospinal fluid + brain tissue), and which modes correspond to
frequencies of known perceptual significance (e.g., speech formants, tinnitus
bands, infrasound discomfort)?** The skull is an inhomogeneous, vaulted
shell of variable thickness (2–10 mm), filled with two coupled fluid/solid
layers: CSF (nearly inviscid fluid) and brain parenchyma (soft viscoelastic
solid). The foramen magnum acts as an acoustic port. A FEA-based modal
analysis with material-specific layers would produce the first comprehensive
eigenspectrum of the coupled system, enabling comparison with psychoacoustic
discomfort data and skull vibration measurements from bone-conduction hearing
research.

### 3. The Gap
Skull vibration studies focus narrowly on **impact protection** (helmet
design) or **bone-conduction hearing** (single-frequency transmissibility).
Full coupled structural-acoustic modal analyses of the cranium — analogous
to what we did for the abdomen — essentially do not exist. There is no
published eigenspectrum of the skull-CSF-brain system with proper FSI
coupling.

### 4. Feasibility
- **Difficulty:** Hard
- **Methods:** Computational (FEniCSx FEA with coupled FSI), mesh from
  segmented CT data (available from open datasets like BodyParts3D)
- **Estimated effort:** 4–6 months
- **Key starting references:**
  1. Kleiven, S. & Hardy, W. (2002) "Correlation of an FE model of the
     human head with local brain motion," *Stapp Car Crash J.* 46.
  2. Franke, E.K. (1956) "Response of the human skull to mechanical
     vibrations," *JASA* 28(6), 1277–1284.
  3. Stenfelt, S. & Goode, R.L. (2005) "Bone-conducted sound: Physiological
     and clinical aspects," *Otol. Neurotol.* 26, 1245–1261.
  4. Sahoo, D. et al. (2014) "Skull bone/Brain FE model," *Int. J. Crashworth.*
     19(6), 600–614.
  5. Our `src/browntone/fem/acoustic_fsi.py` (coupled eigenvalue solver).

### 5. Publication Venue
*Journal of the Acoustical Society of America (JASA)* or *Journal of
Biomechanics*

### 6. Potential Title
**"The Skull as a Drum: Coupled Structural-Acoustic Modes of the Human
Cranium and Their Perceptual Significance"**

### 7. Synergy Score: ★★★★★ (5/5)
This is the Browntone project transposed to a different body cavity. The
entire FEA pipeline (FEniCSx modal solver, FSI coupling, mesh generation,
mode classification) ports with minimal modification. The main new work is
geometry and material properties.

---

## Topic 5 — Why Your Bladder Hates Long Bus Rides

### 1. The Hook
Anyone who has sat on a vibrating bus with a full bladder knows the urgency
is real. Whole-body vibration standards (ISO 2631) protect the spine — but
completely ignore the resonance frequencies of individual organs. Your
bladder is a pressurised elastic shell, and nobody has checked whether the
bus is tuned to its natural frequency.

### 2. The Science
The urinary bladder is a thin-walled, fluid-filled, roughly spherical
elastic shell — geometrically and mechanically similar to our abdominal
cavity model. **What are the natural frequencies and mode shapes of the
human bladder as a function of fill volume, and do common vehicular
vibration spectra (buses, trucks, agricultural vehicles) excite bladder
resonances at physiologically significant amplitudes?** The analysis couples
detrusor muscle shell mechanics (nonlinear, volume-dependent wall stiffness)
with an internal fluid (urine) cavity model. Transmissibility functions from
ISO 2631 map seat vibration to pelvic input. The critical output is whether
bladder-wall strain under vehicular WBV exceeds mechanotransduction
thresholds for the micturition reflex (~1–5 μm tissue displacement).

### 3. The Gap
WBV occupational health research focuses on **lumbar spine degeneration**
and **comfort metrics**. Organ-specific resonance — especially of
hollow viscera — is essentially absent from the literature. The few
bladder biomechanics studies address quasi-static filling pressure or
surgical simulation, not dynamic vibration response. ISO 2631 frequency
weighting was designed around spinal biodynamics, not visceral resonance.

### 4. Feasibility
- **Difficulty:** Medium
- **Methods:** Analytical (Browntone-style shell model with bladder geometry
  and detrusor constitutive law) + computational validation
- **Estimated effort:** 2–3 months
- **Key starting references:**
  1. Korossis, S. et al. (2006) "Regional biomechanical and histological
     characterisation of the passive porcine urinary bladder," *Proc. Inst.
     Mech. Eng. H* 220(6), 727–736.
  2. ISO 2631-1:1997 "Mechanical vibration — Evaluation of human exposure
     to whole-body vibration."
  3. Damaser, M.S. & Lehman, S.L. (1995) "The effect of urinary bladder
     shape on its mechanics during filling," *J. Biomech.* 28(6), 725–732.
  4. Mansfield, N.J. (2005) *Human Response to Vibration*, CRC Press.
  5. Our `src/analytical/natural_frequency_v2.py` (flexural modes of
     pressurised shell).

### 5. Publication Venue
*Journal of Sound and Vibration* or *Journal of Biomechanics*

### 6. Potential Title
**"The Resonant Bladder: Why Whole-Body Vibration Standards Should
Care About Your Urge to Urinate"**

### 7. Synergy Score: ★★★★★ (5/5)
Geometrically, mechanically, and analytically near-identical to the
Browntone problem. The bladder is a pressurised viscoelastic shell
containing fluid, excited by WBV. We swap material properties, geometry
parameters, and the physiological threshold — the entire mathematical
framework carries over.

---

## Topic 6 — Can a Cat's Purr Heal Bones?

### 1. The Hook
Cats purr at 25–50 Hz — precisely the frequency range used in clinical
vibration therapy for bone healing. Veterinary lore claims cats recover
from fractures faster than dogs. Is there a biomechanical basis, or is
this just something cat people say?

### 2. The Science
Low-frequency mechanical vibration (20–50 Hz, <1g) is a clinically
validated osteogenic stimulus — Rubin et al. showed 30 Hz whole-body
vibration increases trabecular bone density in animal models. The research
question is: **does the acoustic/vibrotactile output of a domestic cat's
purr, transmitted through direct body contact, deliver sufficient
mechanical strain to bone tissue to activate mechanotransduction pathways
(Wnt/β-catenin, Piezo1) associated with osteogenesis?** This requires
modelling the cat's thorax as a vibrating source (laryngeal muscles
oscillating the glottis at 25–50 Hz), computing the transmitted vibration
through fur, skin, and soft tissue into the skeletal system, and comparing
the resulting bone surface strain (~1–10 μϵ range) against known osteogenic
thresholds.

### 3. The Gap
The "cats purr to heal" claim circulates widely in popular science but
has **never been quantitatively modelled**. Studies on therapeutic vibration
use mechanical shakers delivering controlled accelerations — nobody has
asked whether a cat's own purr generates sufficient vibration at the bone.
The source characterisation (purr SPL, contact vibration amplitude) exists
in veterinary acoustics literature but has never been connected to bone
mechanobiology.

### 4. Feasibility
- **Difficulty:** Medium
- **Methods:** Analytical (vibroacoustic transmission model through layered
  tissue) + literature synthesis for source characterisation
- **Estimated effort:** 2–3 months
- **Key starting references:**
  1. Rubin, C. et al. (2001) "Low mechanical signals strengthen long bones,"
     *Nature* 412, 603–604.
  2. von Muggenthaler, E. (2001) "The felid purr: A healing mechanism?"
     *JASA* 110(5), 2666.
  3. Sistiaga, A. et al. (2019) "Purring and meowing in domestic cats,"
     *Sci. Rep.* 9, 1–9.
  4. Fritton, S.P. et al. (2000) "Quantifying the strain history of bone,"
     *J. Biomech.* 33, 317–325.
  5. Our `src/analytical/mechanotransduction.py` (strain-to-response model).

### 5. Publication Venue
*Proceedings of the Royal Society B* (biological interface) or *Journal of
Biomechanics*

### 6. Potential Title
**"Purring Your Way to Better Bones? A Vibroacoustic Analysis of Feline
Self-Medication"**

### 7. Synergy Score: ★★★★☆ (4/5)
The layered-tissue transmission model, mechanotransduction thresholds,
and frequency-domain analysis are directly from Browntone. New elements:
source characterisation (cat thorax rather than external excitation),
bone constitutive model.

---

## Topic 7 — The Vuvuzela Problem: Acoustic Superposition in Stadia

### 1. The Hook
During the 2010 FIFA World Cup, the vuvuzela was measured at 127 dB SPL
at 1 metre. A stadium holds 80,000 of them. If they all blow together, is
this technically a weapon — and does the resulting sound field exceed
occupational exposure limits within minutes?

### 2. The Science
**What is the coherent and incoherent acoustic field produced by N ≈ 10⁴–10⁵
vuvuzelas in a hemispherical stadium geometry, and what are the resulting
sound pressure levels, spectral characteristics, and permissible exposure
durations under ISO 1999/NIOSH criteria?** Each vuvuzela is a conical horn
with a fundamental at ~235 Hz and strong harmonics. The research requires:
(a) a single-instrument acoustic model (conical horn theory + measured
radiation pattern); (b) a statistical superposition model accounting for
random phase and spatial distribution of sources; (c) stadium acoustic
effects (reflections, focusing); (d) mapping the resulting SPL field to
exposure-time limits. Key finding to quantify: how many minutes of full-stadium
vuvuzela corresponds to the daily noise dose permitted in an industrial
workplace?

### 3. The Gap
Post-2010 papers measured individual vuvuzela SPL and warned about hearing
damage, but **no study modelled the coherent stadium field** with proper
source–receiver geometry, statistical superposition of thousands of sources,
and comparison to occupational standards. Swanepoel et al. (2010) measured
peak levels but didn't model the acoustics. The stadium-as-horn-array problem
is analytically tractable and publishably novel.

### 4. Feasibility
- **Difficulty:** Easy–Medium
- **Methods:** Analytical (statistical energy analysis, random-phase
  superposition) + computational (boundary element for stadium geometry)
- **Estimated effort:** 6–10 weeks
- **Key starting references:**
  1. Swanepoel, D. et al. (2010) "Noise exposure at the FIFA World Cup,"
     *S. Afr. Med. J.* 100(4), 194–195.
  2. Leventhall, G. (2006) "Infrasound from wind turbines — fact, fiction
     or deception," *Can. Acoust.* 34(2).
  3. Fletcher, N.H. & Rossing, T.D. (1998) *The Physics of Musical
     Instruments*, 2nd ed., Springer.
  4. Vorländer, M. (2008) *Auralization*, Springer.
  5. Goldstein, H. (1980) *Classical Mechanics*, 3rd ed. (for random-phase
     superposition statistics).

### 5. Publication Venue
*JASA* or *Acta Acustica united with Acustica*

### 6. Potential Title
**"80,000 Vuvuzelas: Statistical Acoustics of Mass-Participation Noise
Events and Their Occupational Health Implications"**

### 7. Synergy Score: ★★★☆☆ (3/5)
Horn acoustics and SPL calculations are straightforward extensions of
our acoustic framework. The UQ pipeline handles the statistical
source distribution naturally. No FSI, but the occupational-health angle
connects to our WBV/exposure theme.

---

## Topic 8 — Brown Noise for Sleep: Hype or Physics?

### 1. The Hook
TikTok has 2 billion views for #brownnoise, with users claiming it helps
them sleep, focus, or calm anxiety. Brown noise is *our literal brand.*
Is there any biomechanical basis for these claims, or is this the audio
equivalent of healing crystals?

### 2. The Science
"Brown noise" (Brownian/red noise) has a spectral slope of −6 dB/octave,
concentrating energy at low frequencies. The research question is:
**does brown noise at typical listening levels (40–60 dBA) produce
any distinguishable biomechanical response in the human body compared
to white or pink noise, and is there a frequency-dependent coupling
mechanism that could explain reported subjective effects?** This extends
the Browntone coupling framework to broadband noise: (a) compute the
frequency-dependent tissue displacement spectrum for brown vs. white vs.
pink noise at equal A-weighted SPL; (b) quantify whether the low-frequency
emphasis of brown noise produces disproportionate visceral or cranial
coupling; (c) compare tissue displacements against mechanoreceptor
thresholds. The null hypothesis is that at safe listening levels, no
spectral colour produces biomechanically distinguishable tissue response —
which would redirect explanations toward purely neural/psychological
mechanisms.

### 3. The Gap
The social media phenomenon is enormous but the scientific literature
is essentially nonexistent. A few audiology papers discuss "sound masking"
for sleep without any physics. No study has applied a **tissue-level
biomechanical model** to the brown/pink/white noise comparison. This is
a gap we are uniquely positioned to fill, given it is literally an
extension of our project name.

### 4. Feasibility
- **Difficulty:** Medium
- **Methods:** Analytical (Browntone coupling model extended to broadband),
  computational (frequency-domain sweep)
- **Estimated effort:** 6–10 weeks
- **Key starting references:**
  1. Messineo, L. et al. (2017) "Broadband sound administration improves
     sleep onset latency," *J. Sleep Res.* 26(5), 612–619.
  2. Riedy, S.M. et al. (2021) "Noise as a sleep aid: A systematic review,"
     *Sleep Med. Rev.* 55, 101385.
  3. Zhou, J. et al. (2012) "Pink noise: effect on complexity
     synchronization of brain activity and sleep consolidation,"
     *J. Theor. Biol.* 306, 68–72.
  4. Our `src/analytical/acoustic_coupling.py` + `mechanical_coupling.py`.
  5. ANSI S1.1-2013 (spectrum definitions).

### 5. Publication Venue
*JASA Express Letters* (rapid communication) or *Journal of Sound
and Vibration*

### 6. Potential Title
**"Brown Noise, the Body, and the Bedroom: A Biomechanical Analysis of
Spectrally Coloured Sound at the Tissue Level"**

### 7. Synergy Score: ★★★★★ (5/5)
This is the Browntone paper itself, extended from a single frequency
to a broadband spectrum. Every analytical module applies. The UQ
framework handles inter-subject variability. Maximum code reuse, maximum
brand synergy.

---

## Topic 9 — The Stadium Earthquake: Can 80,000 Jumping Fans Register on a Seismograph?

### 1. The Hook
When 80,000 football fans synchronise a goal celebration, nearby
seismographs twitch. But how much of that is real ground motion vs.
instrument artefact? Could a coordinated crowd, in principle, generate
a signal detectable at meaningful distance?

### 2. The Science
Each jumping human delivers an impulsive vertical force of ~1–2 kN at a
repetition rate of ~2 Hz. The question is: **what is the far-field seismic
signature of N ≈ 80,000 partially coherent impulsive sources distributed
over a stadium footprint, and at what distance does the resulting ground
velocity fall below seismographic detection thresholds?** This requires:
(a) a single-person force model (human body as a mass–spring oscillator
returning to ground); (b) a partially coherent superposition (each person
is ±δt out of sync with the crowd); (c) a Green's function for surface
wave propagation in a layered soil half-space; (d) comparison with
seismographic noise floors and earthquake magnitude equivalences.
The output is a map: "80,000 fans jumping = M_L X.X at Y km."

### 3. The Gap
Seismic records of crowd events exist as curiosities (e.g., "Beast Quake"
at CenturyLink Field in Seattle, 2011 — registered as M_L 1–2). But these
are **empirical observations without a predictive physical model**. No
study has built a forward model from crowd biomechanics → structural
coupling → soil wave propagation → seismographic detection. The
partially-coherent source array problem is analytically elegant and
connects crowd dynamics to seismology.

### 4. Feasibility
- **Difficulty:** Medium
- **Methods:** Analytical (point-source superposition in elastic half-space)
  + computational (spectral element for validation)
- **Estimated effort:** 2–3 months
- **Key starting references:**
  1. Díaz, J. et al. (2017) "Urban seismology: On the origin of earth
     vibrations within a city," *Sci. Rep.* 7, 15296.
  2. Dallard, P. et al. (2001) "The London Millennium Footbridge,"
     *Structural Engineer* 79(22), 17–33.
  3. Racic, V. et al. (2009) "Experimental identification and analytical
     modelling of human walking forces," *JSV* 326, 1–49.
  4. Aki, K. & Richards, P.G. (2002) *Quantitative Seismology*, 2nd ed.,
     University Science Books.
  5. Brownjohn, J.M.W. et al. (2004) "Crowd dynamic loading on
     footbridges," *Proc. ICE Struct. Build.* 157, 109–117.

### 5. Publication Venue
*Geophysical Research Letters* (short, high impact) or *Proceedings of
the Royal Society A*

### 6. Potential Title
**"The Stadium Earthquake: Forward Modelling of Crowd-Generated Seismic
Waves From First Principles"**

### 7. Synergy Score: ★★★☆☆ (3/5)
Modal analysis and Q-factor methodology apply, as does the partially-
coherent source superposition (analogous to our vuvuzela random-phase
analysis). The UQ framework handles uncertain crowd synchronisation.
No biological FSI, but the human-as-oscillator source model is related.

---

## Topic 10 — The Optimal Pub Dart Under the Influence

### 1. The Hook
At 0.08% BAC — the legal driving limit in most jurisdictions — your hand
tremor amplitude roughly doubles. We can compute the exact probability of
hitting treble-20 as a function of blood alcohol, using Bayesian trajectory
analysis and measured tremor power spectra.

### 2. The Science
A dart in flight is a drag-stabilised projectile with 6-DOF dynamics
(translation + angular wobble). The key stochastic input is the
**release condition uncertainty**, which is dominated by physiological
hand tremor. Tremor is well-characterised: 8–12 Hz with amplitude
increasing linearly with BAC. The research question is: **given measured
tremor power spectral densities at BAC = 0, 0.04, 0.08, 0.12%, what is
the probability density function of dart impact location on a standard
dartboard, and how does the optimal aiming point (which maximises expected
score) shift as impairment increases?** This is a stochastic optimal
control problem: sober players should aim for treble-20, but at sufficient
tremor amplitude, the lower-variance strategy of aiming for the
triple-19/7/3 cluster dominates.

### 3. The Gap
The "optimal darts aiming point" has been computed for idealised Gaussian
error models (Tibshirani, *Significance*, 2011), but **not with
physiologically realistic, frequency-dependent tremor models** and
certainly not as a function of intoxication. The connection between
alcohol-induced tremor biomechanics and game-theoretic strategy is
unpublished and inherently entertaining.

### 4. Feasibility
- **Difficulty:** Easy
- **Methods:** Analytical (projectile dynamics + stochastic perturbation)
  + computational (Monte Carlo)
- **Estimated effort:** 4–6 weeks
- **Key starting references:**
  1. Tibshirani, R. et al. (2011) "A statistician plays darts,"
     *Significance* 8(2), 82–86.
  2. Lakie, M. et al. (2012) "Physiological tremor: frequency dependence
     and clinical relevance," *J. Neurol. Neurosurg. Psychiatry* 83, 7–12.
  3. Smeets, J.B.J. & Beek, P.J. (2000) "Aiming at darts," *Human Mov.
     Sci.* 19, 353–371.
  4. Fillmore, M.T. et al. (2005) "Alcohol impairment of behaviour,"
     *Psychopharmacology* 178, 337–345.
  5. Morrison, S. & Newell, K.M. (2000) "Postural and resting tremor in
     the upper limb," *Clin. Neurophysiol.* 111, 651–663.

### 5. Publication Venue
*Significance* (RSS/ASA magazine) or *European Journal of Physics*

### 6. Potential Title
**"One More Pint? Bayesian Optimal Darts Strategy as a Function of
Blood Alcohol Concentration"**

### 7. Synergy Score: ★★☆☆☆ (2/5)
The Monte Carlo / UQ methodology transfers, but otherwise this is a
new domain. However, the biomechanical tremor characterisation connects
to our vibration expertise, and the project is an excellent "gateway"
publication for outreach and media engagement.

---

## Priority Ranking

Recommended execution order, balancing impact, synergy, and effort:

| Priority | Topic | Rationale |
|----------|-------|-----------|
| 🥇 1 | **#8 Brown Noise for Sleep** | Maximum synergy, minimal new code, massive public interest, fast turnaround |
| 🥈 2 | **#5 Resonant Bladder** | Near-identical framework, novel occupational health angle, publishable in JSV |
| 🥉 3 | **#2 Whale Song** | High synergy, memorable hook, clean JASA paper |
| 4 | **#1 Belly Flop** | Flagship visual result, needs SPH capability (new tooling) |
| 5 | **#6 Cat Purr Bones** | Viral potential, moderate effort, connects to clinical vibration therapy |
| 6 | **#3 Tesla's Machine** | Quick win, high public interest, good for Proc Roy Soc |
| 7 | **#4 Skull Drum** | Highest technical challenge but transformative result |
| 8 | **#10 Pub Darts** | Easy, fun, good student project or outreach piece |
| 9 | **#9 Stadium Earthquake** | Solid geophysics paper, modest synergy |
| 10 | **#7 Vuvuzela** | Neat acoustics, but 2010 World Cup relevance fading |

---

## Resource Estimates

| Phase | Topics Covered | Calendar Time | FTE Months |
|-------|---------------|---------------|------------|
| Phase 1 (Quick wins) | #8, #5, #3 | Apr–Jul 2026 | 4 |
| Phase 2 (Core papers) | #2, #6, #1 | Aug–Dec 2026 | 6 |
| Phase 3 (Ambitious) | #4, #10 | Jan–Jun 2027 | 5 |
| Phase 4 (If capacity) | #9, #7 | 2027 H2 | 3 |

---

*Report compiled 27 March 2026. All synergy scores relative to the
Browntone v1 codebase at commit `HEAD` of `main` branch.*
