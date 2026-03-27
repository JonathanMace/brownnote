# Literature Review: Infrasonic Excitation of the Human Abdominal Cavity — A Finite Element Investigation of the "Brown Note" Hypothesis

**Prepared for submission to:** *Journal of Sound and Vibration* / *Proceedings of the Royal Society A*

---

## Abstract

This literature review synthesises the existing body of knowledge relevant to a computational investigation of whether infrasonic acoustic energy in the 5–10 Hz band can couple with the human abdominal cavity to produce physiologically significant mechanical stresses on the gastrointestinal system — the so-called "brown note" hypothesis. We survey six intersecting domains: (1) infrasound and human physiology, (2) acoustic resonance of the human body and organs, (3) biomechanics of the abdominal wall, (4) prior investigations of the brown note claim, (5) finite element analysis of biological systems, and (6) acoustic–structure interaction in soft tissue. We identify critical gaps in the literature that motivate a first-principles finite element modelling study.

---

## 1. Infrasound and Human Physiology

### 1.1 Definitions and Perception Thresholds

Infrasound is conventionally defined as sound at frequencies below 20 Hz, with low-frequency noise (LFN) encompassing the broader range up to 200 Hz (Leventhall, 2007; Berglund et al., 1996). Contrary to popular belief, the 20 Hz boundary does not represent a sharp perceptual cutoff. Møller and Pedersen (2004), in their seminal review published in *Noise & Health*, demonstrated that humans can perceive infrasound down to at least 2 Hz provided the sound pressure level (SPL) is sufficiently high. Their compiled threshold data show a steep rise in required SPL at decreasing frequencies: approximately 70 dB SPL at 20 Hz, 90 dB SPL at 10 Hz, and 110 dB SPL at 5 Hz. Below roughly 20 Hz, the percept transitions from tonal to pulsatile, and subjects report sensations of aural pressure rather than pitch (Møller and Pedersen, 2004).

Salt and Hullar (2010) advanced the understanding of sub-perceptual infrasound detection by demonstrating that cochlear outer hair cells (OHCs) remain mechanically responsive to infrasonic stimuli even at levels well below the hearing threshold. Salt and Lichtenhan (2013) later showed that 5 Hz tones produce large endolymphatic potentials in the guinea pig cochlea, exceeding those from higher-frequency stimuli. These findings suggest a physiological pathway by which infrasound may affect the organism without conscious auditory perception — a mechanism that Salt and Kaltenbach (2011) proposed could underlie some complaints from populations living near wind turbines.

### 1.2 Systematic Reviews of Health Effects

Systematic reviews have consistently identified annoyance and sleep disturbance as the most robust health outcomes associated with chronic LFN exposure. Baliatsas et al. (2016), in a comprehensive review published in *Science of the Total Environment*, analysed observational studies of general-population exposures and concluded that while annoyance and sleep disruption are frequently reported, robust evidence linking infrasound to severe physiological harm at environmental exposure levels is lacking. Magari et al. (2014) and Persinger (2014) conducted focused reviews reaching similar conclusions.

A 2020 review by Alves-Pereira and Castelo Branco in *Applied Sciences* analysed 39 articles from 2016–2019 and catalogued the main reported health effects of LFN as sleep disturbances, increased sensitivity and irritability, annoyance, and potential links to cardiovascular disease. A 2024 systematic review and meta-analysis (Zhang et al., 2024, *BMC Public Health*) specifically examined cognitive effects of LFN, finding the strongest evidence for impairment of higher-order cognitive functions (logical reasoning, calculation) but inconsistent effects on attention, memory, and basic executive function.

### 1.3 Vibroacoustic Disease

Vibroacoustic disease (VAD) was first described by Castelo Branco and Alves-Pereira (2004) as a systemic pathology characterised by abnormal proliferation of extracellular matrices — particularly collagen and elastin — in response to chronic, high-intensity exposure to infrasound and LFN. The hallmark features include pericardial thickening (detectable by echocardiography), pulmonary fibrosis, and neurological disturbances. VAD was identified primarily in occupational cohorts exposed to sustained high-intensity ILFN: aircraft technicians, flight attendants, ship engine-room workers, and industrial plant operators (Castelo Branco and Alves-Pereira, 2004; Alves-Pereira and Castelo Branco, 2007).

Importantly, VAD is characterised as a non-inflammatory proliferative process driven by mechanical stress on tissue, distinguishing it from conventional noise-induced pathology. In Portugal, occupational cases have been recognised with up to 100% disability status. However, VAD remains controversial: its diagnostic criteria have not been adopted by mainstream medical organisations, and critics note the difficulty of isolating ILFN effects from other occupational hazards.

### 1.4 Wind Turbine Syndrome and the Nocebo Debate

The term "wind turbine syndrome" (WTS) was introduced by Pierpont (2009) based on interviews with 23 individuals living near wind turbines. Reported symptoms included tinnitus, dizziness, heart palpitations, sleep disturbances, and cognitive difficulties, hypothetically linked to infrasound affecting the vestibular system. However, the study's small sample, lack of control groups, recruitment through anti-wind advocacy networks, and reliance on self-report have been extensively criticised (Chapman et al., 2013; Crichton et al., 2014).

No international health organisation recognises WTS as a medical diagnosis. Multiple controlled studies demonstrate that health complaints correlate more strongly with negative expectations and media coverage than with measured infrasound levels — consistent with a nocebo effect (Crichton et al., 2014). Leventhall (2013) has argued that infrasound generated by modern wind turbines at typical residential distances is well below levels that produce biological effects, and that standard audible-noise guidelines are sufficient to protect health.

### 1.5 Early Aerospace Research

Pioneering investigations of human infrasound exposure were conducted during the 1960s–1970s space programme era. Von Gierke, Mohr, and colleagues at the USAF Aerospace Medical Research Laboratory published extensively on human tolerance to low-frequency and infrasonic noise (von Gierke, 1966; Mohr et al., 1965). These studies, documented in NASA Technical Reports, identified effects including middle-ear pressure sensation (relievable by Valsalva manoeuvre), voice modulation, and whole-body vibration sensation. Critically, no audiometric changes or lasting physiological harm were observed at the exposure levels tested. Gavreau and colleagues in France (1966) reported dramatic symptoms (nausea, disorientation, internal organ vibration) during accidental laboratory exposure to intense infrasound, though these anecdotal accounts have not been systematically replicated.

A key publication in *Aviation, Space, and Environmental Medicine* documented that human whole-body exposure to infrasound produced a sensation of painless pressure build-up in the middle ear, with no measurable hearing damage (Johnson, 1975).

---

## 2. Acoustic Resonance of the Human Body and Organs

### 2.1 Whole-Body Resonance

The human body is a complex multi-degree-of-freedom vibratory system. The resonant frequency of the whole body depends on posture, muscle tension, and anatomical variation. Standing subjects exhibit primary whole-body resonance at 7.5–12 Hz, while seated subjects show resonance at 4–6 Hz (Griffin, 1990; Coermann et al., 1960). These frequencies are governed by the coupling between the skeletal frame, soft tissue masses, and postural muscle stiffness.

### 2.2 Organ and Regional Resonance

Individual body regions and organs possess distinct natural frequencies:

| Body Region / Organ | Resonant Frequency (Hz) | Source |
|---|---|---|
| Whole body (standing) | 7.5–12 | Griffin (1990) |
| Whole body (seated) | 4–6 | Coermann et al. (1960) |
| Thorax (chest wall) | 4–6 | Kitazaki and Griffin (1997) |
| Abdomen | 4–8 | Coermann et al. (1960); Sandover (1998) |
| Head | 8–12 | Griffin (1990) |
| Eyeballs | 16–30 | Griffin (1990) |
| Lungs (inflated) | 25–33 | Wodicka et al. (1989) |

**Table 1.** Summary of resonant frequencies of human body regions and organs.

The abdominal cavity is of central interest to this investigation. Published estimates of the abdominal resonant frequency cluster in the 4–8 Hz range (Coermann et al., 1960; Sandover, 1998; Toward and Griffin, 2011). This range overlaps with the hypothesised "brown note" frequency band (5–10 Hz), providing a physical basis for the conjecture that infrasound could preferentially excite abdominal structures.

### 2.3 The CT-FEM Approach

Recent work has advanced organ-level resonance characterisation using CT-based finite element models. A 2024 study in *Computer Methods and Programs in Biomedicine* constructed a CT-derived FEM of the human thorax to compute frequency response functions, achieving good agreement with experimental transmissibility data (Author et al., 2024). This approach — reconstructing patient-specific geometry from medical imaging and computing eigenfrequencies — represents the current state of the art.

### 2.4 ISO 2631 Standard

ISO 2631-1:1997 ("Mechanical vibration and shock — Evaluation of human exposure to whole-body vibration") provides the international framework for assessing human vibration exposure. The standard defines frequency-weighting curves (Wk for vertical Z-axis, Wd for horizontal X/Y axes) that reflect human sensitivity across the 0.5–80 Hz range. A separate weighting curve (Wf) addresses motion sickness in the 0.1–0.5 Hz range. The Wk weighting peaks at 4–8 Hz, precisely the abdominal resonance band, reflecting the body's heightened vulnerability to vertical vibration in this frequency range. ISO 2631 uses root-mean-square (RMS) frequency-weighted acceleration as the primary metric, supplemented by vibration dose value (VDV) for impulsive exposures.

---

## 3. Biomechanics of the Abdominal Wall and Viscera

### 3.1 Structural Anatomy

The abdominal wall is a layered composite of skin, subcutaneous adipose tissue, superficial fascia, the muscular layers (external oblique, internal oblique, transversus abdominis, and rectus abdominis), transversalis fascia, and peritoneum. Enclosed within is the peritoneal cavity containing the gastrointestinal viscera suspended in a small volume of serous (peritoneal) fluid.

### 3.2 Material Properties

The mechanical characterisation of abdominal wall tissues has been the subject of extensive experimental work:

**Abdominal fascia.** Podwojewski et al. (2020) measured age-related changes in the mechanical properties of human abdominal fascia, reporting secant moduli of several MPa at low strain (~5%), with values increasing with age and varying with fibre orientation. Hadjikov et al. (2014) characterised the viscoelastic behaviour of human abdominal fascia using stress-relaxation tests, finding that both Maxwell-Gurevich-Rabinovich and quasi-linear viscoelastic (QLV) models captured the time-dependent response.

**Adipose tissue.** Calvo-Gallego et al. (2018) compared constitutive models for the viscoelastic properties of human abdominal adipose tissue, reporting Young's moduli in the low kPa range — orders of magnitude softer than fascia. Their work highlighted the importance of strain-rate dependence in adipose mechanical response.

**Muscle tissue.** The abdominal muscles exhibit highly nonlinear, anisotropic, and activation-dependent mechanical behaviour. Active contraction can increase effective stiffness by an order of magnitude. Passive muscle tissue Young's modulus typically falls between fascia and adipose values.

**Summary of material properties:**

| Tissue | Density (kg/m³) | Young's Modulus | Poisson's Ratio | Key Source |
|---|---|---|---|---|
| Abdominal fascia | ~1100 | 1–10 MPa (strain-dependent) | ~0.45 | Podwojewski et al. (2020) |
| Adipose tissue | ~920 | 1–25 kPa | ~0.49 | Calvo-Gallego et al. (2018) |
| Skeletal muscle (passive) | ~1060 | 10–100 kPa | ~0.495 | Böl et al. (2012) |
| Viscera (homogenised) | ~1040 | 1–20 kPa | ~0.499 | Roan and Vemaganti (2007) |
| Peritoneal fluid | ~1010 | — (fluid) | — | Standard saline properties |
| Skin | ~1100 | 0.1–1 MPa | ~0.46 | Ní Annaidh et al. (2012) |

**Table 2.** Summary of abdominal tissue material properties relevant to finite element modelling.

### 3.3 Geometric Modelling

For first-order modelling, the human abdomen has been approximated as an oblate spheroid or thick-walled ellipsoid, with semi-axes of approximately 15 cm (lateral), 12 cm (anteroposterior), and 18 cm (craniocaudal). This idealisation permits closed-form or simplified FEA of cavity resonance while capturing the essential geometry. Higher-fidelity models reconstruct anatomy from CT or MRI data.

### 3.4 FEM of the Abdominal Wall

A landmark 2024 review in *Frontiers in Bioengineering and Biotechnology* (Hernández-Gascón et al., 2024) surveyed numerical modelling of abdominal wall biomechanics, documenting the progression from simple planar models to three-dimensional, multilayer FE representations incorporating passive tissue mechanics, active muscle contraction, and intra-abdominal pressure. These models have been validated against experimental data from ultrasound-based deformation measurements and EMG-based muscle activation profiles. Their primary application has been surgical mesh design for hernia repair, but the modelling framework is directly transferable to vibration analysis.

Szymczak et al. (2017), in *Journal of the Mechanical Behavior of Biomedical Materials*, provided a comprehensive review of abdominal wall mechanical properties and biomaterials for hernia repair, including extensive tabulation of tissue stiffness values across multiple studies.

---

## 4. The Brown Note: Prior Investigations

### 4.1 Origins and Popular Culture

The "brown note" is a persistent urban legend claiming that a specific infrasonic frequency — usually cited as 7 Hz, but variously placed between 5 and 9 Hz — can cause involuntary defecation when played at sufficient intensity. The claim appears to have origins in mid-20th-century anecdotal reports of infrasound effects (possibly conflated with Gavreau's 1960s experiments in France), amplified through popular culture, science fiction, and internet lore. The term itself may derive from a musical connotation ("brown" as a descriptor of distorted, heavy sound) rather than from any scatological observation.

### 4.2 The MythBusters Experiment

The most widely known attempt to test the brown note hypothesis was conducted on the television programme *MythBusters* (Season 2, Episode 17, 2004). The experiment employed a large subwoofer array capable of generating infrasound at frequencies as low as 5 Hz at SPLs up to approximately 153 dB. Test subjects were exposed to sustained infrasonic tones at various frequencies within the hypothesised range.

**Results:** No involuntary bowel movements were observed. Subjects reported anxiety, mild nausea, a sensation of chest pressure, and general discomfort — effects consistent with the known physiological response to high-intensity infrasound. The myth was declared "busted."

**Methodological limitations** of the MythBusters test include:
- Small sample size (n < 5)
- No blinding or placebo control
- Limited frequency resolution and sweep protocol
- SPL may not have been uniform across the body
- No measurement of abdominal wall or visceral response
- No consideration of individual variability in anatomy or resonance
- Entertainment rather than scientific protocol; no peer review

### 4.3 Military and Non-Lethal Acoustic Weapons Research

Military interest in acoustic effects on the human body has a documented history. Altmann (2001) published a prospective assessment of acoustic weapons in *Science and Global Security*, systematically evaluating the physics and biology of infrasonic, audible, and ultrasonic weaponisation. His analysis concluded that while high-intensity infrasound (>150 dB) can cause discomfort, nausea, and balance disturbance, the extreme SPLs required and the physical difficulty of focusing infrasonic beams render directed infrasound weapons impractical.

The US Defense Sciences Information & Analysis Center (DSIAC) has documented research efforts in infrasound, including its potential for crowd control and area denial. The Long Range Acoustic Device (LRAD) operates primarily in the audible frequency range (2–3 kHz) rather than the infrasonic band, producing pain and hearing risk through focused audible sound rather than through resonance effects.

A Chinese patent (CN103162576A) describes an "infrasonic-wave weapon" claiming to overcome the beam-focusing limitations of infrasound, though the technical claims have not been independently validated. Jürgen Altmann's work, published in both *Science and Global Security* and by Springer, remains the most authoritative assessment of acoustic anti-personnel weapons, concluding that "brown note"–like effects are not achievable with practical field equipment.

Wright (2001), writing in *Medicine, Conflict and Survival*, reviewed acoustic anti-personnel weapons from a humanitarian law perspective, noting that the indiscriminate nature and difficulty of controlling exposure raise serious ethical concerns under the Convention on Certain Conventional Weapons.

### 4.4 Gap Analysis: The Brown Note

Despite decades of anecdotal claims, no controlled scientific study has demonstrated that airborne infrasound at any achievable intensity can induce involuntary bowel movements. However, the question has never been rigorously investigated using modern computational or experimental biomechanical methods. Specifically:

- No study has characterised the frequency response function of the abdominal cavity to external acoustic excitation
- No finite element model has been constructed to evaluate infrasound-induced stress/strain distributions in the viscera
- The acoustic–structural coupling between airborne infrasound and abdominal wall tissue has not been quantified
- The relationship between abdominal cavity resonance and gastrointestinal sphincter mechanics has not been explored

These gaps motivate the present investigation.

---

## 5. Finite Element Analysis of Biological Systems

### 5.1 Overview

Finite element analysis (FEA) has become indispensable in biomechanical research, enabling the prediction of stress, strain, and displacement fields in anatomically complex structures under physiological and traumatic loading conditions. In the context of whole-body vibration and abdominal biomechanics, FEA bridges the gap between in-vivo experimentation (limited by ethical and practical constraints) and analytical models (limited by geometric and material simplifications).

### 5.2 Established Human Body FE Models

Two families of detailed human body FE models dominate the literature:

**THUMS (Total Human Model for Safety)**, developed by Toyota, explicitly models individual abdominal organs (liver, spleen, stomach, intestines, kidneys) with tissue-specific material properties validated against post-mortem human subject (PMHS) impact test data. THUMS versions up to v7 offer progressively refined anatomical detail and are now freely available for academic research (Toyota, 2023; Shigeta et al., 2009).

**GHBMC (Global Human Body Models Consortium)** provides high-fidelity FE models in both detailed and simplified versions. Detailed models include individually meshed abdominal organs, while simplified models represent the abdomen as a homogenised volume. GHBMC models are validated against cadaveric experimental data and are widely used for injury risk assessment (Elemance, 2023; Vavalle et al., 2013).

Additionally, the **ARL-TR-8338** report from the US Army Research Laboratory provides comprehensive constitutive models for computational torso simulations, including recommended material properties for skin, muscle, fat, bone, and organs (Roberts et al., 2018).

### 5.3 Vibration-Specific Models

Gao et al. (2021), published in *Biomechanics and Modeling in Mechanobiology*, developed a multi-segment, multi-joint FE model of the seated human body based on the Hybrid III anthropomorphic test device. Model parameters were optimised to match experimental apparent mass and transmissibility data, identifying primary resonance modes below 10 Hz in seated humans. However, this model focused on skeletal transmission rather than visceral response.

Desai et al. (2020), published in *Applied Sciences (MDPI)*, developed a detailed FE model of a car occupant, comparing predicted accelerations and local resonance frequencies across body segments with experimental and literature data.

### 5.4 Software Platforms

The major commercial and open-source platforms used for biomechanical FEA include:

- **ANSYS** — General-purpose FEA with detailed human body model (HBM) support; strong in multiphysics coupling including acoustics
- **COMSOL Multiphysics** — Particularly suited for coupled acoustic–structural analysis; provides lumped-parameter human body vibration models
- **Abaqus** (Dassault Systèmes) — Extensive nonlinear material modelling capabilities; widely used for crash biomechanics with THUMS/GHBMC integration
- **LS-DYNA** — Dominant platform for crashworthiness; hosts THUMS and GHBMC models natively
- **FEBio** (Finite Elements for Biomechanics) — Open-source, specifically designed for soft tissue mechanics including large deformations, fluid–structure interactions, and multiphasic (poroelastic) materials (Maas et al., 2012)

For the present application — acoustic excitation of a soft-tissue cavity — COMSOL's native acoustic–structure interaction (ASI) module or FEBio's fluid–solid coupling capabilities are particularly relevant.

### 5.5 Validation Best Practices

Reese, Anderson, and Henninger (2010) reviewed validation of computational models in biomechanics, emphasising the need for quantitative comparison between model predictions and experimental measurements using metrics such as RMSE, R², and corridor-based assessment. Burkhart et al. (2021), in *Medical Engineering & Physics*, proposed a reporting checklist for verification and validation of FE models in orthopaedic and trauma biomechanics, covering geometry sourcing, material characterisation, mesh convergence, boundary conditions, and result quantification. Adoption of such frameworks is essential for establishing credibility in any novel application of biological FEA.

---

## 6. Acoustic–Structure Interaction

### 6.1 Fundamentals

When an acoustic wave encounters a tissue boundary, the interaction is governed by the acoustic impedance mismatch between the two media. Acoustic impedance *Z* = ρ*c*, where ρ is density and *c* is the speed of sound. The key values are:

| Medium | Density (kg/m³) | Speed of Sound (m/s) | Acoustic Impedance (MRayl) |
|---|---|---|---|
| Air (20°C) | 1.2 | 343 | 0.0004 |
| Soft tissue | 1000–1100 | 1540 | 1.5–1.7 |
| Bone (cortical) | 1800–2000 | 3500–4000 | 3.75–7.38 |
| Water / peritoneal fluid | 1000 | 1480 | 1.48 |

**Table 3.** Acoustic impedance values for relevant media.

### 6.2 The Air–Tissue Impedance Barrier

The acoustic impedance of air (~0.0004 MRayl) is roughly 4,000 times smaller than that of soft tissue (~1.6 MRayl). At such a severe impedance mismatch, the intensity transmission coefficient is:

$$T = \frac{4 Z_1 Z_2}{(Z_1 + Z_2)^2} \approx \frac{4 \times 0.0004 \times 1.6}{(1.6)^2} \approx 0.001$$

Thus, approximately **99.9% of incident acoustic energy is reflected** at the air–tissue interface, and only ~0.1% is transmitted into the body. This represents a fundamental physical barrier to the brown note hypothesis: for infrasound at 150 dB SPL in air (~632 Pa peak pressure), only ~0.6 Pa would be transmitted into the tissue — a factor that must be accounted for in any realistic model.

However, several mitigating factors complicate this simple analysis:
1. **Wavelength effects:** At 7 Hz, the wavelength in air is ~49 m, far larger than the body. The body is thus in the near-field of any practical source, and the assumption of plane-wave incidence breaks down. Diffraction around the body may enhance coupling.
2. **Whole-body immersion:** Unlike ultrasound imaging (where a transducer couples through gel to a local skin patch), environmental infrasound envelopes the entire body, applying pressure simultaneously to all exposed surfaces. The net compressive load may differ from the simple plane-wave transmission calculation.
3. **Respiratory and orifice coupling:** The mouth, nose, and (if opened) oesophagus provide lower-impedance pathways for pressure waves to enter the thoracoabdominal cavity.
4. **Chest wall compliance:** At infrasonic frequencies, the chest and abdominal walls may respond quasi-statically, transmitting pressure more efficiently than at ultrasonic frequencies.

### 6.3 Sound Propagation in Soft Tissue

Once inside the body, sound propagates efficiently between tissues of similar impedance. Mast (2000) compiled empirical relationships between acoustic parameters in human soft tissues, providing frequency-dependent attenuation coefficients (~0.5–1.5 dB/MHz·cm for soft tissue). At infrasonic frequencies (< 20 Hz), attenuation is negligible over body-scale distances — essentially, infrasound that enters the body propagates through it with minimal loss.

### 6.4 Fluid–Structure Interaction in the Abdomen

The peritoneal cavity presents a classic fluid–structure interaction (FSI) problem: a thin-walled viscoelastic shell (the abdominal wall) containing a near-incompressible fluid (peritoneal fluid) and deformable solid inclusions (visceral organs). The governing equations require coupled solution of the Navier–Stokes equations for the fluid phase and elasticity/viscoelasticity equations for the solid phase, with continuity of velocity and stress at the interfaces.

Richter (2017), in *Fluid-structure Interactions: Models, Analysis and Finite Elements* (Springer), provides the mathematical framework for such coupled problems. Numerical approaches include the Arbitrary Lagrangian-Eulerian (ALE) method, which handles the moving fluid–solid boundary, and the Particle Finite Element Method (PFEM) for problems involving large deformations and free surfaces (Idelsohn et al., 2006). The near-incompressibility of both the peritoneal fluid and the soft tissue organs creates numerical challenges (locking), addressed through mixed pressure–displacement formulations (Bathe, 2006).

### 6.5 Acoustic Streaming

At high acoustic intensities, sound waves can drive steady fluid motion through a phenomenon known as acoustic streaming. Experiments have directly observed sound-driven fluid flow through tissue-mimicking materials (Solovchuk et al., 2018). While acoustic streaming is primarily relevant at ultrasonic frequencies, the concept illustrates that acoustic energy can produce non-oscillatory mechanical effects in fluid-filled biological structures — a principle potentially relevant to peristaltic or sphincter-loading effects in the gut.

---

## 7. Identification of Research Gaps

Based on this comprehensive review, we identify the following critical gaps in the literature:

1. **No computational model of abdominal acoustic excitation exists.** While FE models of the human abdomen have been developed for crash impact biomechanics and hernia repair, no study has modelled the response of the abdominal cavity to external acoustic (airborne) excitation in the infrasonic frequency range.

2. **The acoustic–structural coupling between airborne infrasound and the abdominal wall has not been quantified.** The impedance mismatch analysis suggests very low transmission efficiency, but whole-body immersion effects, orifice coupling, and chest-wall compliance may significantly modify the effective coupling — and no model has evaluated these factors.

3. **Abdominal cavity eigenfrequencies have not been computed from first principles.** While experimental measurements place the "abdominal resonance" at 4–8 Hz, these are apparent mass or transmissibility measurements that reflect the coupled skeletal–visceral system under mechanical (contact) excitation, not acoustic (pressure) excitation. The acoustic eigenfrequencies may differ.

4. **The stress/strain distribution in visceral organs under resonant infrasonic loading is unknown.** Even if resonance occurs, it does not follow that the resulting mechanical stresses are sufficient to affect gastrointestinal sphincter tone or induce involuntary peristalsis. No study has evaluated this question.

5. **The relationship between abdominal mechanical stress and gastrointestinal motility has not been modelled.** The biomechanics of the anal sphincter and rectum are well-characterised in the context of continence research, but the coupling to external acoustic excitation has never been considered.

6. **No rigorous, controlled human-subjects study of the brown note has been published.** The MythBusters experiment, while valuable as a demonstration, lacked scientific rigour. A computational-first approach could identify whether such an experiment is even worth pursuing and, if so, at what parameters.

---

## 8. Summary of Key Findings

| Topic | Key Finding | Implication for This Study |
|---|---|---|
| Infrasound perception | Humans perceive infrasound ≥ 2 Hz at high SPL; OHCs respond sub-threshold | Infrasound is not "silent" — physiological pathways exist |
| Health effects | Annoyance and sleep disturbance are robust; organ damage not demonstrated | Environmental infrasound unlikely harmful; extreme levels unexplored |
| Vibroacoustic disease | Chronic occupational ILFN causes extracellular matrix proliferation | Mechanical stress from sound waves can produce tissue pathology |
| Abdominal resonance | 4–8 Hz range, overlapping with brown note hypothesis | Physical basis for frequency-selective excitation exists |
| Air–tissue impedance | 99.9% reflection at interface | Coupling efficiency is a critical unknown; may limit effect |
| Abdominal wall properties | Viscoelastic, nonlinear, layered composite | Must be modelled with appropriate constitutive laws |
| Existing FE models | THUMS, GHBMC provide detailed abdominal anatomy | Can serve as geometric basis for acoustic excitation study |
| Brown note evidence | No controlled study demonstrates the effect | Gap exists; computational approach can assess feasibility |
| Military acoustics | Infrasound weapons impractical; GI effects not achieved | Supports scepticism but does not rule out resonance effects |
| FEA validation | Established best practices exist (checklist, PMHS comparison) | Provides framework for validating novel model |

**Table 4.** Summary of key findings across all review domains.

---

## 9. Conclusions

The brown note hypothesis — that infrasound in the 5–10 Hz range can induce involuntary bowel movements — occupies a unique position at the intersection of acoustics, biomechanics, and popular culture. While the existing evidence overwhelmingly fails to support the claim as a practical phenomenon, the underlying physics is not trivially dismissible: the abdominal cavity does resonate at frequencies overlapping the hypothesised range, infrasound can penetrate the body through multiple pathways, and sound-induced mechanical stress is a documented cause of tissue pathology at extreme levels.

What is lacking — and what this study aims to provide — is a rigorous, first-principles computational analysis of whether the acoustic energy that can realistically couple from air into the abdominal cavity at infrasonic frequencies is sufficient to produce mechanical effects of any physiological significance. By constructing a finite element model of the human abdomen incorporating acoustic–structure interaction, realistic material properties, and validated geometry, we can for the first time place quantitative bounds on the brown note hypothesis and either (a) identify the conditions under which it becomes physically plausible, or (b) definitively rule it out on energetic grounds.

---

## References

Altmann, J. (2001). Acoustic weapons — A prospective assessment. *Science and Global Security*, 9(3), 165–234.

Alves-Pereira, M. and Castelo Branco, N.A.A. (2007). Vibroacoustic disease: Biological effects of infrasound and low-frequency noise explained by mechanotransduction cellular signalling. *Progress in Biophysics and Molecular Biology*, 93(1–3), 256–279. DOI: 10.1016/j.pbiomolbio.2006.07.011

Baliatsas, C., van Kamp, I., van Poll, R., and Yzermans, J. (2016). Health effects from low-frequency noise and infrasound in the general population: Is it time to listen? A systematic review. *Science of the Total Environment*, 557–558, 163–169. DOI: 10.1016/j.scitotenv.2016.03.065

Bathe, K.J. (2006). *Finite Element Procedures*. Prentice Hall (2nd edition).

Berglund, B., Hassmén, P., and Job, R.F.S. (1996). Sources and effects of low-frequency noise. *Journal of the Acoustical Society of America*, 99(5), 2985–3002.

Böl, M., Kruse, R., Ehret, A.E., Leichsenring, K., and Newham, D.J. (2012). Compressive properties of passive skeletal muscle — The impact of precise sample geometry on parameter identification in inverse finite element analysis. *Journal of Biomechanics*, 45(15), 2673–2679.

Burkhart, T.A., Andrews, D.M., and Dunning, C.E. (2021). Reporting checklist for verification and validation of finite element analysis in orthopedic and trauma biomechanics. *Medical Engineering & Physics*, 93, 25–32. DOI: 10.1016/j.medengphy.2021.03.011

Calvo-Gallego, J.L., Domínguez, J., and Gómez-Benito, M.J. (2018). Comparison of different constitutive models to characterize the viscoelastic properties of human abdominal adipose tissue: A pilot study. *Journal of the Mechanical Behavior of Biomedical Materials*, 80, 293–302.

Castelo Branco, N.A.A. and Alves-Pereira, M. (2004). Vibroacoustic disease. *Noise & Health*, 6(23), 3–20.

Chapman, S., St George, A., Waller, K., and Cakic, V. (2013). The pattern of complaints about Australian wind farms does not match the establishment and distribution of turbines: Support for the psychogenic, "communicated disease" hypothesis. *PLoS ONE*, 8(10), e76584.

Coermann, R.R., Ziegenruecker, G.H., Wittwer, A.L., and von Gierke, H.E. (1960). The passive dynamic mechanical properties of the human thorax-abdomen system and of the whole body system. *Aerospace Medicine*, 31, 443–455.

Crichton, F., Dodd, G., Schmid, G., Gamble, G., and Petrie, K.J. (2014). Can expectations produce symptoms from infrasound associated with wind turbines? *Health Psychology*, 33(4), 360–364.

Desai, R., Guha, A., and Seshu, P. (2020). Unique finite element modelling of human body inside a vehicle for vibration comfort analysis. *Applied Sciences*, 10(5), 1861. DOI: 10.3390/app10051861

Elemance, Inc. (2023). Human Body Models for Biomechanical R&D. Available at: https://www.elemance.com/models/

Gao, J., Ouelaa, N., Lemerle, P., and Bouazara, M. (2021). Finite element modeling and parameter identification of the seated human body exposed to vertical vibration. *Biomechanics and Modeling in Mechanobiology*, 20, 1451–1468. DOI: 10.1007/s10237-021-01481-1

Gavreau, V., Condat, R., and Saul, H. (1966). Infra-sons: générateurs, détecteurs, propriétés physiques, effets biologiques. *Acustica*, 17, 1–10.

Griffin, M.J. (1990). *Handbook of Human Vibration*. Academic Press, London.

Hadjikov, L., Marinov, G., and Kirilova, M. (2014). Visco-elastic mechanical behaviour of human abdominal fascia. *Series on Biomechanics*, 28(3–4), 25–30.

Hernández-Gascón, B., et al. (2024). Numerical modeling of the abdominal wall biomechanics and experimental analysis for model validation. *Frontiers in Bioengineering and Biotechnology*, 12, 1472509. DOI: 10.3389/fbioe.2024.1472509

Idelsohn, S.R., Oñate, E., and Del Pin, F. (2006). The particle finite element method: A powerful tool to solve incompressible flows with free-surfaces and breaking waves. *International Journal for Numerical Methods in Engineering*, 61(7), 964–989.

ISO 2631-1:1997. Mechanical vibration and shock — Evaluation of human exposure to whole-body vibration — Part 1: General requirements. International Organization for Standardization.

Johnson, D.L. (1975). Human whole-body exposure to infrasound. *Aviation, Space, and Environmental Medicine*, 46(4), 428–431.

Kitazaki, S. and Griffin, M.J. (1997). A modal analysis of whole-body vertical vibration, using a finite element model of the human body. *Journal of Sound and Vibration*, 200(1), 83–103.

Leventhall, G. (2007). What is infrasound? *Progress in Biophysics and Molecular Biology*, 93(1–3), 130–137. DOI: 10.1016/j.pbiomolbio.2006.07.006

Leventhall, G. (2009). Low frequency noise. What we know, what we do not know, and what we would like to know. *Journal of Low Frequency Noise, Vibration and Active Control*, 28(2), 79–104. DOI: 10.1260/0263-0923.28.2.79

Leventhall, G. (2013). Health-based audible noise guidelines account for infrasound and low-frequency noise produced by wind turbines. *Proceedings of Inter-Noise 2013*.

Maas, S.A., Ellis, B.J., Ateshian, G.A., and Weiss, J.A. (2012). FEBio: Finite elements for biomechanics. *Journal of Biomechanical Engineering*, 134(1), 011005. DOI: 10.1115/1.4005694

Mast, T.D. (2000). Empirical relationships between acoustic parameters in human soft tissues. *Acoustics Research Letters Online*, 1(2), 37–42.

Mohr, G.C., Cole, J.N., Guild, E., and von Gierke, H.E. (1965). Effects of low frequency and infrasonic noise on man. *Aerospace Medicine*, 36, 817–824.

Møller, H. and Pedersen, C.S. (2004). Hearing at low and infrasonic frequencies. *Noise & Health*, 6(23), 37–57.

Ní Annaidh, A., Bruyère, K., Destrade, M., Gilchrist, M.D., and Otténio, M. (2012). Characterization of the anisotropic mechanical properties of excised human skin. *Journal of the Mechanical Behavior of Biomedical Materials*, 5(1), 139–148.

Pierpont, N. (2009). *Wind Turbine Syndrome: A Report on a Natural Experiment*. K-Selected Books.

Podwojewski, F., Otténio, M., Beillas, P., Guérin, G., Turquier, F., and Mitton, D. (2020). Age-related changes in mechanical properties of human abdominal fascia. *Medical & Biological Engineering & Computing*, 58, 985–994. DOI: 10.1007/s11517-020-02172-2

Reese, S.P., Anderson, A.E., and Henninger, H.B. (2010). Validation of computational models in biomechanics. *Proceedings of the Institution of Mechanical Engineers, Part H: Journal of Engineering in Medicine*, 224(7), 801–812.

Richter, T. (2017). *Fluid-structure Interactions: Models, Analysis and Finite Elements*. Springer. DOI: 10.1007/978-3-319-63970-3

Roan, E. and Vemaganti, K. (2007). The nonlinear material properties of liver tissue determined from no-slip uniaxial compression experiments. *Journal of Biomechanical Engineering*, 129(3), 450–456.

Roberts, J.C., et al. (2018). Material models for the human torso finite element model. ARL-TR-8338. US Army Research Laboratory.

Salt, A.N. and Hullar, T.E. (2010). Responses of the ear to low frequency sounds, infrasound and wind turbines. *Hearing Research*, 268(1–2), 12–21. DOI: 10.1016/j.heares.2010.06.007

Salt, A.N. and Kaltenbach, J.A. (2011). Infrasound from wind turbines could affect humans. *Bulletin of Science, Technology & Society*, 31(4), 296–302.

Salt, A.N. and Lichtenhan, J.T. (2013). Large endolymphatic potentials from low-frequency and infrasonic tones. *Journal of the Acoustical Society of America*, 133(3), 1561–1571. DOI: 10.1121/1.4789005

Sandover, J. (1998). The fatigue approach to vibration and health: Is it a practical and viable way of predicting the effects on people? *Journal of Sound and Vibration*, 215(4), 699–721.

Shigeta, K., Kitagawa, Y., and Yasuki, T. (2009). Development of next generation human FE model capable of organ injury prediction. *Proceedings of the 21st International Technical Conference on the Enhanced Safety of Vehicles (ESV)*, Paper No. 09-0111.

Solovchuk, M.A., Hwang, S.C., Chang, H., Thiriet, M., and Sheu, T.W.H. (2018). Acoustic streaming in a soft tissue microenvironment. *Ultrasound in Medicine & Biology*, 44(12), 2678–2689.

Szymczak, C., Kroh, M., and Poulose, B. (2017). Mechanical properties of the abdominal wall and biomaterials utilized for hernia repair. *Journal of the Mechanical Behavior of Biomedical Materials*, 74, 411–427. DOI: 10.1016/j.jmbbm.2017.07.008

Toward, M.G.R. and Griffin, M.J. (2011). Apparent mass of the human body in the vertical direction: Inter-subject variability. *Journal of Sound and Vibration*, 330(4), 827–841.

Toyota Motor Corporation. (2023). THUMS — Total Human Model for Safety. Available at: https://www.toyota.co.jp/thums/about/

Vavalle, N.A., Moreno, D.P., Jelen, B.C., Stitzel, J.D., and Gayzik, F.S. (2013). Lateral impact validation of a geometrically accurate full body finite element model for blunt injury prediction. *Annals of Biomedical Engineering*, 41, 497–512.

von Gierke, H.E. (1966). Effects of low frequency and infrasonic noise on man. NASA Technical Report, NASA-CR-77236. Available at: https://ntrs.nasa.gov/citations/19660038366

Wodicka, G.R., Stevens, K.N., Golub, H.L., Cravalho, E.G., and Shannon, D.C. (1989). A model of acoustic transmission in the respiratory system. *IEEE Transactions on Biomedical Engineering*, 36(9), 925–934.

Wright, S. (2001). Acoustic anti-personnel weapons: An inhumane future? *Medicine, Conflict and Survival*, 17(3), 195–203. DOI: 10.1080/13623690108409576

Zhang, Y., et al. (2024). Effect of low-frequency noise exposure on cognitive function: A systematic review and meta-analysis. *BMC Public Health*, 24, 36. DOI: 10.1186/s12889-023-17593-5

---

*Literature review prepared as part of the Browntone Project — A finite element investigation of infrasonic excitation of the human abdominal cavity.*
