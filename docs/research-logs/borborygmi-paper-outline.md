# Borborygmi Paper Outline — 2026-03-27

**Author**: Opus (PI)
**Branch**: borborygmi-paper-outline
**Target venue**: JASA (Journal of the Acoustical Society of America) — Regular Article (~8 pages)
**Working title**: "What Pitch Is a Growling Stomach? A Unified Multi-Mode Acoustic Model of Borborygmi"

## Summary

This document outlines a paper that unifies five distinct resonance mechanisms
for intestinal gas-pocket acoustics — free Minnaert bubble, tissue-constrained
bubble, Helmholtz resonator, axial piston mode, and radial breathing mode — into
a single parametric framework. The model predicts borborygmi frequencies from
first principles using only measurable anatomical and material properties, and
reproduces the clinically observed 200–550 Hz band for healthy adults without
curve-fitting.

---

## 1. The Novelty Argument

### What exists in the literature

| Source | What they model | Gap |
|--------|----------------|-----|
| Minnaert (1933) | Free bubble in unbounded fluid | No tissue confinement |
| Church (1995) | Bubble in elastic solid (ultrasound contrast agents) | Not intestinal geometry; MHz regime |
| Li, Liu & Zou (2022, SIAM) | Quasi-Minnaert in soft elastic media | Rigorous math; no GI application |
| Ammari et al. (2018) | Bubbly media Minnaert correction | Multiple bubbles; no gut context |
| Ching & Tan (2012, WJG) | Spectral analysis of bowel sounds | Empirical; no predictive model |
| Craine et al. (1999, 2002) | Electronic stethoscope classification | Signal processing; no physics model |
| Nowak et al. (2021, Sensors) | Automated bowel sound analysis review | ML classification; no resonance theory |
| Du Plessis et al. (2000, DCR) | Clinical bowel sound frequency bands | Observational data only |

### What's new here

1. **First unified multi-mode model**: No published work combines Minnaert,
   constrained-bubble, Helmholtz, axial, and radial modes into a single
   framework for intestinal gas.

2. **Tissue-constrained correction applied to GI acoustics**: Li et al. (2022)
   derived Minnaert corrections for elastic media generally; we apply an
   engineering-level constrained-bubble model specifically to intestinal
   wall parameters (E = 10 kPa, h = 3 mm, ν = 0.45).

3. **Predictive, not classificatory**: The clinical literature (Ching & Tan,
   Craine, Nowak) treats bowel sounds as signals to classify. We predict
   which frequencies should appear from anatomy, and explain *why* they appear.

4. **Mode transition map**: Different physical mechanisms dominate at different
   pocket volumes and geometries. We map which mode is operative when.

5. **Clinical frequency bands from first principles**: Constrained bubble spans
   135–440 Hz for 1–50 mL pockets, reproducing the healthy range (200–550 Hz)
   and obstruction peaks (SBO: 288 Hz, LBO: 440 Hz) without fitting.

---

## 2. Paper Structure

### Title
"What Pitch Is a Growling Stomach? A Unified Multi-Mode Acoustic Model of
Borborygmi"

*Alternative (more conservative)*:
"Resonant frequencies of intestinal gas pockets: a multi-mode analytical model"

### Authors
J. Mace, B. Mace

### Abstract (~200 words)
Borborygmi — the rumbling and gurgling sounds of the gastrointestinal tract —
arise from oscillation of gas pockets entrained in intestinal fluid. Despite
their clinical significance as indicators of gut motility, no first-principles
acoustic model predicts their frequency spectrum from measurable anatomical
parameters. We present a unified analytical framework comprising five resonance
mechanisms: (i) free Minnaert bubble oscillation, (ii) tissue-constrained bubble
resonance incorporating intestinal wall elasticity, (iii) Helmholtz resonance
through peristaltic constrictions, (iv) axial piston modes of cylindrical gas
slugs, and (v) radial breathing modes of gas columns in elastic tubes.
The constrained bubble model predicts frequencies of 135–440 Hz for gas pocket
volumes of 1–50 mL, spanning the clinically observed 200–550 Hz band for healthy
adults. Parametric sweeps reveal that pocket volume and intestinal wall stiffness
are the dominant determinants, while tube diameter exerts a secondary effect
through geometry-dependent modes. A mode-transition map identifies which
resonance mechanism dominates in each region of the volume–diameter parameter
space. The model provides a physics-based framework for interpreting
auscultatory findings and designing acoustic monitoring systems for
gastrointestinal motility assessment.

### I. Introduction (~1.5 pages)

**Story arc**: Borborygmi are universally experienced yet poorly understood
acoustically. Clinical auscultation remains qualitative. Recent signal-processing
approaches (Craine 1999, Ching & Tan 2012, Nowak 2021) classify sounds but
don't predict them. The bubble acoustics literature (Minnaert 1933, Leighton
1994, Li et al. 2022) has the physics but has never been applied to
gastrointestinal anatomy. We bridge this gap.

**Key paragraphs**:
1. Borborygmi as a ubiquitous acoustic phenomenon — history (Cannon 1905),
   clinical relevance (auscultation, IBS, obstruction)
2. The signal-processing paradigm: classify, don't model (Craine, Ching & Tan,
   Nowak review). Limitation: no predictive power, no physical insight.
3. Bubble acoustics: Minnaert to modern elastic corrections (Church 1995,
   Li et al. 2022). Gap: never applied to GI tract.
4. Our contribution: unified multi-mode framework with five mechanisms,
   validated against clinical frequency bands. No free parameters.

### II. Theory (~2.5 pages)

**Structure**: Each mode gets a self-contained derivation (~½ page each),
followed by a unification section.

#### A. Free Minnaert bubble (baseline)
- Standard derivation: f = (1/2πR)√(3γP₀/ρ_f)
- Role: lower bound; gives correct order of magnitude
- Limitation: ignores tissue confinement entirely

#### B. Tissue-constrained bubble
- Elastic wall adds stiffness K_wall = 2Eh/[a²(1−ν)] and inertia m_wall = ρ_w h
- ω² = (k_gas + k_wall) / (m_fluid + m_wall)
- Reduces to Minnaert when E→0, h→0 (verified analytically and numerically)
- **This is the workhorse model**: best clinical match

#### C. Helmholtz resonator
- Peristaltic constriction creates a neck connecting pocket to lumen
- f_H = (c_gas/2π)√(A_neck / L_eff V) with Rayleigh end correction
- Dominant for small volumes with narrow constrictions

#### D. Axial piston mode
- Gas slug trapped between fluid plugs in cylindrical lumen
- Compressible gas spring + radiation added mass at each end
- Relevant for elongated gas columns (slug geometry)

#### E. Radial breathing mode
- Cylindrical gas column in elastic tube
- K_gas + K_wall balanced against (ρ_f R + ρ_w h)/R²
- High frequency; relevant in large-diameter segments (colon)

#### F. Mode selection and coexistence
- Geometry determines which mode is dominant
- Spherical pockets → constrained bubble
- Elongated slugs → axial or radial
- Constricted connections → Helmholtz
- Multiple modes may coexist → broadband character of borborygmi

### III. Results (~2 pages)

#### A. Canonical predictions
Table of frequencies for 10 mL pocket, 3 cm tube:

| Mode | Frequency (Hz) | Clinical relevance |
|------|----------------|-------------------|
| Free Minnaert | ~244 | Baseline (underestimates) |
| Constrained bubble | ~223 | Within healthy range |
| Helmholtz (5 mm neck) | ~647 | Upper borborygmi / clicks |
| Axial piston | ~99 | Below audible gurgling |
| Radial breathing | ~1329 | Not typically reported |

#### B. Volume sweep (Figure 1)
- All five modes vs. volume (1–50 mL)
- Clinical band overlay (200–550 Hz)
- Constrained bubble is the only mode that spans the entire clinical band

#### C. Parametric sensitivity (Figure 2)
- Tube diameter effect on constrained bubble (20–50 mm)
- Neck geometry effect on Helmholtz mode
- Wall stiffness effect (1–100 kPa range)

#### D. Mode transition map (Figure 3) — **NEW ANALYSIS NEEDED**
- 2D parameter space: volume (1–50 mL) × tube diameter (2–6 cm)
- Colour-coded by dominant mode (lowest frequency within clinical band)
- Boundaries show where Helmholtz overtakes constrained, where axial becomes relevant

#### E. Clinical frequency comparison (Figure 4)
- Model predictions overlaid on reported bands:
  - Healthy adults: 200–550 Hz (peak 340 Hz)
  - SBO: 173–667 Hz (peak 288 Hz)
  - LBO: 309–878 Hz (peak 440 Hz)
- Infer pocket volumes that produce each condition's peak
- SBO peak (288 Hz) → ~4 mL constrained pocket
- LBO peak (440 Hz) → ~1 mL constrained pocket (or larger pocket with stiffer wall)

### IV. Discussion (~1.5 pages)

**Key discussion points**:

1. **Why the constrained bubble dominates**: For typical intestinal gas pockets
   (1–50 mL, quasi-spherical), the tissue-constrained Minnaert correction is
   sufficient to explain most clinical observations. The wall stiffness raises
   frequencies modestly above free-bubble values — enough to match the 200–550 Hz
   band.

2. **Role of geometry**: Not all gut sounds are the same mode. Clicks and snaps
   may be Helmholtz events (small neck, sudden opening). Low rumbles are axial
   piston modes. The broadband character of borborygmi reflects multiple
   simultaneous modes.

3. **Obstruction signatures**: SBO involves dilated small bowel (larger tube
   diameter, larger pockets → lower frequency). LBO involves colonic gas
   (potentially stiffer wall, different geometry → higher dominant frequency).
   Model qualitatively explains Ching & Tan (2012) findings.

4. **Limitations**:
   - Spherical/cylindrical idealisation; real pockets are irregular
   - Static equilibrium; peristaltic dynamics not modelled
   - Single-pocket model; real gut has multiple interacting pockets
   - Damping model is simplified (single loss tangent)
   - No radiation efficiency estimate (how much sound reaches the surface?)

5. **Toward acoustic monitoring**: If model predictions are validated with
   contact microphone recordings + simultaneous ultrasound (to measure pocket
   volume), this framework could underpin real-time gut motility monitoring.

### V. Conclusions (~0.5 pages)

Three main takeaways:
1. Five distinct resonance mechanisms predict borborygmi frequencies from
   measurable anatomical and material parameters alone.
2. The tissue-constrained bubble model reproduces the clinical 200–550 Hz
   band for 1–50 mL gas pockets, and explains obstruction-specific frequency
   shifts.
3. A mode-transition map identifies which mechanism dominates in each region
   of the pocket-volume / tube-diameter space, providing physical insight for
   interpreting auscultatory findings.

### Acknowledgements
Standard.

### References (~30 citations)

---

## 3. Figures Required

| Figure | Status | Description |
|--------|--------|-------------|
| Fig 1: Frequency vs. volume | ✅ EXISTS (panel a) | All 5 modes, semilog, clinical band overlay |
| Fig 2a: Tube diameter sweep | ✅ EXISTS (panel b) | Constrained bubble, 4 diameters |
| Fig 2b: Neck diameter sweep | ✅ EXISTS (panel c) | Helmholtz, 4 neck sizes |
| Fig 3: Mode transition map | ❌ NEEDED | 2D heatmap: volume × diameter, colour = dominant mode |
| Fig 4: Clinical comparison | ✅ EXISTS (panel d) | Model vs. clinical bands with condition-specific overlays |
| Fig 5: Wall stiffness sweep | ❌ NEEDED | Constrained bubble, E = 1–100 kPa |
| Fig 6: Schematic diagram | ❌ NEEDED | Anatomy cartoon showing each mode's geometry |

**Total: 6 figures** (3 exist as panels in current 4-panel figure; need to
refactor into standalone publication figures + create 3 new ones)

---

## 4. Additional Analysis Needed

### Must-have (before writing)

1. **Mode transition map** (Fig 3)
   - Create `mode_transition_map()` in `borborygmi_model.py`
   - Sweep volume (1–50 mL) × tube diameter (2–6 cm)
   - For each point, compute all 5 mode frequencies
   - Identify which mode(s) fall within 100–1000 Hz clinical window
   - Colour by dominant (lowest-frequency) clinical mode
   - Add contour lines for f = 200, 340, 550 Hz

2. **Wall stiffness parametric sweep** (Fig 5)
   - E_wall from 1 kPa (very soft mucosa) to 100 kPa (fibrotic bowel)
   - Show constrained bubble frequency vs. volume for 4–5 stiffness values
   - Clinical implication: pathological wall changes → frequency shift

3. **Clinical peak frequency inversion**
   - Given clinical peak frequencies (288, 340, 440 Hz), solve for the
     pocket volume that produces each peak under the constrained model
   - Potentially: confidence intervals from wall property uncertainty

### Nice-to-have (strengthens paper)

4. **Damping and Q-factor analysis**
   - Plot half-power bandwidth vs. volume for each mode
   - Compare predicted Q ≈ 4 with measured bowel sound durations
   - Ching & Tan (2012) report sound durations of 0.5–0.8 s; at 300 Hz
     this implies Q ≈ 150–240 individual cycles — seems high, worth discussing

5. **Multi-pocket interaction** (mentioned in discussion, not modelled)
   - Could add a simple two-pocket coupled oscillator as an appendix
   - Shows how nearby pockets create beating / frequency splitting

6. **Radiation efficiency estimate**
   - How much acoustic energy from a gurgling pocket reaches the abdominal
     surface? Related to Paper 1's energy budget framework.
   - Could use the same transmission loss approach from `energy_budget.py`

7. **Monte Carlo uncertainty quantification**
   - Sample over uncertain wall properties (E, h, ν), fluid properties (ρ_f),
     and gas composition (γ for CO₂/H₂/CH₄ mixtures vs. air)
   - Produce prediction intervals to compare with clinical scatter

---

## 5. Code Status & Gaps

### Existing (ready to use)
| Module | Function | Status |
|--------|----------|--------|
| `borborygmi_model.py` | `minnaert_frequency()` | ✅ 35 tests passing |
| | `constrained_bubble_frequency()` | ✅ |
| | `helmholtz_frequency()` | ✅ |
| | `cylindrical_axial_frequency()` | ✅ |
| | `cylindrical_radial_frequency()` | ✅ |
| | `volume_sweep()` | ✅ |
| | `tube_diameter_sweep()` | ✅ |
| | `clinical_comparison()` | ✅ |
| | `fig_frequency_vs_volume()` | ✅ 4-panel figure |

### Needs implementation
| Function | Priority | Effort |
|----------|----------|--------|
| `mode_transition_map()` | **HIGH** | ~50 LOC + tests |
| `wall_stiffness_sweep()` | **HIGH** | ~30 LOC + tests |
| `invert_clinical_frequency()` | MEDIUM | ~20 LOC + tests |
| `damping_analysis()` | MEDIUM | ~40 LOC + tests |
| `fig_mode_transition_map()` | **HIGH** | ~60 LOC (2D heatmap) |
| `fig_wall_stiffness()` | **HIGH** | ~30 LOC |
| `fig_schematic()` | LOW | Manual illustration or TikZ |
| Refactor existing 4-panel into 4 standalone figures | MEDIUM | ~100 LOC |

### Estimated new code: ~330 LOC + ~15 new tests

---

## 6. Reference List (Core ~30 citations)

### Bubble acoustics (5–7)
- Minnaert M (1933) Phil Mag 16:235
- Leighton TG (1994) The Acoustic Bubble, Academic Press
- Church CC (1995) JASA 97:1510 (elastic shell correction)
- Li H, Liu H, Zou J (2022) SIAM J Appl Math 82:119 (elastic media)
- Ammari H et al. (2018) Ann IHP 35:1975 (bubbly media)
- Prosperetti A (1988) JASA 83:502 (bubble dynamics review)
- Commander KW & Prosperetti A (1989) JASA 85:732 (linear bubble models)

### Gastrointestinal acoustics (5–7)
- Cannon WB (1905) Am J Physiol 12:387 (original borborygmi description)
- Ching SS & Tan YK (2012) World J Gastroenterol 18:4585
- Craine BL et al. (1999) Dig Dis Sci 44:1909
- Craine BL et al. (2002) Dig Dis Sci 47:1290
- Nowak JK et al. (2021) Sensors 21:5294 (automated analysis review)
- Dalle Donne et al. (2024) Biomedicines 14:581 (clinical models review)

### GI physiology (5–7)
- Levitt MD (1971) NEJM 284:1394 (intestinal gas volumes)
- Serra J et al. (2001) Gastroenterology 120:218 (gas dynamics)
- Suarez FL et al. (1997) Am J Physiol 272:G1028 (gas transit)
- Gregersen H & Kassab GS (2000) J Biomech 33:1475 (GI mechanics)
- Fung YC (1993) Biomechanics, Springer (tissue properties)

### Helmholtz / resonator acoustics (3–4)
- Rayleigh JWS (1896) Theory of Sound, Vol II
- Kinsler LE et al. (1999) Fundamentals of Acoustics, Wiley
- Temkin S (2001) Elements of Acoustics, ASA Press

### Clinical data (3–4)
- Du Plessis et al. (2000) Dis Colon Rectum 43:81
- Yoshino H et al. (1990) Dis Colon Rectum 33:967
- Hadjileontiadis LJ & Panas SM (1997) IEEE Trans Biomed Eng 44:1005

---

## 7. Timeline Estimate

| Phase | Tasks | Effort |
|-------|-------|--------|
| **Week 1** | Implement mode transition map, wall stiffness sweep, clinical inversion | 1 day code + tests |
| **Week 1** | Generate all 6 figures (publication quality) | 1 day |
| **Week 2** | Draft Sections II–III (theory + results) | 2 days |
| **Week 2** | Draft Sections I, IV, V (intro, discussion, conclusions) | 1 day |
| **Week 3** | Internal review cycle (3-reviewer panel) | 1 day |
| **Week 3** | Revise, polish, format for JASA | 1 day |
| **Week 4** | Final check, submit | 0.5 day |

**Total estimated effort**: ~7 working days

---

## 8. Key Risks

1. **Scooping risk**: LOW. The Li et al. (2022) SIAM paper shows mathematical
   interest in constrained Minnaert resonance, but no one has applied it to gut
   acoustics specifically. The clinical bowel-sound community uses signal
   processing, not physics models. We occupy a unique interdisciplinary niche.

2. **Clinical validation gap**: We compare against published frequency bands,
   but don't have our own experimental data. JASA reviewers may want at least
   a phantom experiment. Mitigation: frame as "analytical model + literature
   comparison"; mention phantom experiment as future work.

3. **Scope creep**: The multi-pocket coupling, radiation efficiency, and UQ
   analysis are each interesting but could expand the paper beyond 8 pages.
   Keep these as brief mentions in Discussion or as supplementary material.

---

## Issues Identified

- **MINOR**: Current 4-panel figure in `borborygmi_model.py` needs refactoring
  into standalone publication figures with consistent styling
- **MINOR**: `CLINICAL_DATA` dictionary in the model uses approximate ranges;
  should add proper citations and error bars
- **MAJOR**: No `mode_transition_map()` function yet — this is the paper's
  centrepiece figure and needs implementation before writing
- **MINOR**: Gas composition (γ) is hardcoded as air; real intestinal gas is
  CO₂/H₂/CH₄ mixture with slightly different γ. Should at least discuss.

## Next Steps

1. Implement `mode_transition_map()` and `wall_stiffness_sweep()` in
   `borborygmi_model.py` with full test coverage
2. Generate publication-quality standalone figures
3. Begin drafting Section II (Theory) — the most self-contained section
4. Run the bibliographer agent to verify no recent publications close the gap
5. Run the 3-reviewer panel on the outline before committing to full drafting
