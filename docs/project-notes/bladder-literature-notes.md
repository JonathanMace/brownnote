# Literature Notes — Bladder Resonance Project

## Bladder Wall Mechanical Properties

### Elastic Modulus (Young's Modulus)

| Source | Method | E (kPa) | Condition |
|--------|--------|---------|-----------|
| Ultrasound bladder vibrometry (IOP 2013) | Vibrometry | 9.6 | Rest, 187 mL, 8.6 mmHg |
| Ultrasound bladder vibrometry (IOP 2013) | Vibrometry | 48.7 | Distended, 267 mL, 17.6 mmHg |
| Barnes (2016) PhD thesis | Tensile testing | 10–800 | Depends on layer and stretch |
| Laser-induced acoustic waves (PMC 2014) | SAW | 10–200 | Varies with tissue layer |
| Shear wave elastography (J Ped Urol 2025) | SWE | Variable | Neurogenic vs normal |

**Key insight**: E increases dramatically with fill state (strain-stiffening).
At rest: ~10 kPa. At capacity: up to 200–800 kPa.

- **Reference**: https://iopscience.iop.org/article/10.1088/0031-9155/58/8/2675/pdf
- **Reference**: https://europepmc.org/articles/PMC4285607
- **Reference**: https://etheses.bham.ac.uk/6641/1/Barnes16PhD.pdf

### Viscoelastic Properties

- Viscosity: 0.2 Pa·s (rest) to several Pa·s (distended)
- Loss tangent: estimated 0.3–0.5 from dynamic measurements
- Bladder exhibits both creep and stress relaxation
- **Reference**: Viscoelastic properties of the contracting detrusor (AJP 1991)
  https://journals.physiology.org/doi/abs/10.1152/ajpcell.1991.261.2.c355

### Wall Thickness

- Empty/contracted: ~5 mm
- Full (400–500 mL): ~2–3 mm
- Thinning follows approximately constant tissue volume assumption
- **Reference**: Noninvasive Evaluation of Bladder Wall Mechanical Properties
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0157818

## Whole-Body Vibration and Urinary Symptoms

### Occupational Health Evidence

- Vehicle operators (truck, bus, forklift) report increased urinary urgency
- WBV at 4–16 Hz causes maximal mechanical response in pelvis
- Lower abdominal organs (bladder, intestines) are vulnerable at pelvic resonance
- **Reference**: https://pemftraining.com/what-frequency-do-humans-vibrate-at-complete-science-based-guide-to-human-resonant-frequencies-and-body-vibration/

### Pelvic Floor Muscle Response

- WBV at 40 Hz / 4 mm increases pelvic floor muscle (PFM) activation
- Bioelectrical activity of PFM during synchronous WBV measured
- Single exposures in healthy women do not cause PFM fatigue
- **Reference**: Bioelectrical activity of the pelvic floor muscles during synchronous WBV
  https://link.springer.com/article/10.1186/s12894-015-0103-9

### Therapeutic Use (Rehabilitation)

- WBV at 20–40 Hz used for pelvic floor rehabilitation
- Improves continence symptoms in post-prostatectomy and postpartum patients
- **Reference**: NCT03325660 (ClinicalTrials.gov)
  https://clinicaltrials.gov/study/NCT03325660
- **Reference**: https://www.academia.edu/40476838/Effect_of_whole_body_vibration_exercise_in_the_pelvic_floor_muscles_of_healthy_and_unhealthy_individuals_a_narrative_review

## ISO 2631 — Pelvic Resonance

### Key Data

| Standard | Body Region | Resonance Range | Axis |
|----------|-------------|-----------------|------|
| ISO 2631-1:1997 | Pelvis / lower torso | 4–8 Hz | Vertical (Z) |
| ISO 2631-1:1997 | Abdominal mass | 4–8 Hz | Vertical (Z) |
| General biomechanics | Whole trunk | 4–16 Hz | All |

- Health, comfort, and perception effects assessed in 0.5–80 Hz range
- **4–8 Hz is critical for seated vertical vibration** (where pelvic resonance dominates)
- Frequency weightings: Wd, Wk, Wb account for human sensitivity

### References

- ISO 2631-1:1997: https://www.iso.org/standard/7612.html
- ANSI Blog overview: https://blog.ansi.org/ansi/iso-2631-1-1997-whole-body-vibration/
- Human body vibration measurement: https://www.windturbinesyndrome.com/wp-content/uploads/2009/08/human-body-vibration-exposure-and-its-measurement.pdf
- Frequency weightings: https://larsondavis.com/learn/industrial-hygiene/human-vibration-weightings
- SVANTEK WBV overview: https://svantek.com/applications/whole-body-vibration/

## Connection to Brown Note Project

The browntone project models the abdominal cavity as a fluid-filled
viscoelastic shell to compute resonant frequencies (~5–10 Hz) and assess
whether infrasound can drive these modes. The bladder is a *smaller*
fluid-filled shell sitting *inside* the pelvic cavity, with:

- **Same physics**: flexural modes of a fluid-filled shell
- **Different scale**: R ≈ 4 cm vs R ≈ 12 cm for abdomen
- **Different coupling**: mechanical (WBV through pelvis) dominates over
  airborne acoustic coupling
- **Same framework**: AbdominalModelV2 with parameter substitution

The key prediction: the bladder's n=2 flexural mode falls in or near the
ISO 2631 pelvic resonance band (4–8 Hz) for physiological fill volumes,
providing a first-principles explanation for vibration-induced urgency.
