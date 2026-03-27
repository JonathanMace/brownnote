# Experimental Validation Protocol

## Fluid-Filled Viscoelastic Shell Model — Brown Note Hypothesis

---

## 1  Objective

Validate the analytical predictions of the oblate-spheroidal shell model
(§2 of the paper) through two independent experimental approaches:

| Prediction | Value | Observable |
|---|---|---|
| f₂ (n=2 flexural) | ≈ 4 Hz | Modal frequency |
| Mode shape | Oblate-prolate (n=2) | Scanning vibrometer |
| Airborne coupling displacement | 0.014 μm @ 120 dB | Laser vibrometer |
| Mechanical coupling displacement | 649 μm @ 0.1 m/s² | Accelerometer / vibrometer |
| Coupling ratio (mech/air) | ≈ 46 000× | Ratio of above |
| Dominant parameter | E (S_T = 0.86) | Parametric phantom series |

---

## 2  Experiment 1 — Physical Phantom (Benchtop)

### 2.1  Phantom Construction

#### 2.1.1  Geometry

Oblate spheroid matching human-abdomen canonical dimensions:

- Semi-major axis **a = 180 mm** (equatorial)
- Semi-minor axis **c = 120 mm** (polar / cranio-caudal)
- Wall thickness **h = 10 mm** (uniform)
- Internal volume ≈ 16.3 L  (4/3 π a² c)

#### 2.1.2  Mold Fabrication

1. **CAD model.**  Design two concentric oblate spheroids in SolidWorks or
   FreeCAD.  Inner surface: (a, c) = (180, 120) mm.  Outer surface:
   (a + h, c + h) = (190, 130) mm.  Split each into upper and lower halves
   along the equatorial plane with alignment pins and 5 mm flanges.
2. **3D printing.**  Print four mold halves (two inner, two outer) in PLA or
   ABS on a printer with ≥ 300 mm build plate (e.g. Creality CR-10, Prusa
   XL).  Layer height 0.20 mm.  Infill ≥ 30 %.  Estimated material ≈ 1.5 kg.
3. **Surface preparation.**  Sand interior mold surfaces to 400-grit.  Apply
   3 coats of mold release (Ease Release 200 or equivalent).

#### 2.1.3  Material Selection

| Silicone | Shore | E (MPa) | tan δ | Pot life | Best for |
|---|---|---|---|---|---|
| **Ecoflex 00-30** | 00-30 | 0.069 | 0.18 | 45 min | Soft-tissue match |
| Ecoflex 00-50 | 00-50 | 0.083 | 0.20 | 18 min | Intermediate |
| **Dragon Skin 10A** | 10A | 0.15 | 0.12 | 75 min | Stiffer tissue / tensed muscle |
| Dragon Skin 20A | 20A | 0.30 | 0.10 | 25 min | Upper-bound stiffness |

**Recommendation:** Fabricate at least two phantoms — Ecoflex 00-30 (relaxed
abdomen analogue) and Dragon Skin 10A (contracted abdomen analogue).

**Mix-ratio tuning.**  Ecoflex 00-30 and Dragon Skin 10A can be mixed in
arbitrary ratios (both are platinum-cure).  Preparing 4–5 intermediate
mixtures (e.g. 80/20, 60/40, 40/60, 20/80) yields a quasi-continuous E sweep
from 0.069 to 0.15 MPa.

#### 2.1.4  Casting Procedure

1. Weigh parts A and B to ±1 g on a precision balance (1:1 by weight for
   Smooth-On products).
2. Mix thoroughly for 3 min.  Degas in vacuum chamber at −29 inHg for 4 min
   (until bubbles collapse).
3. Assemble outer mold halves; clamp with C-clamps.
4. Pour degassed silicone into the gap between inner and outer molds.  Tilt
   mold 30° while pouring to avoid trapped air.
5. Cure at room temperature (23 ± 2 °C) for the manufacturer-specified time
   (≥ 4 h for Ecoflex, ≥ 16 h for Dragon Skin).  Accelerate to 1 h with
   60 °C oven if mold material permits.
6. Demold.  Trim flash at equatorial seam with a scalpel.
7. Install two nylon barbed fittings (6 mm ID) at opposite poles using
   silicone adhesive (Sil-Poxy):
   - Fill port (bottom pole): for water injection via syringe.
   - Vent/sensor port (top pole): for hydrophone insertion and deaeration.
8. Fill phantom with **degassed, deionised water** through the bottom port.
   Use a peristaltic pump at 50 mL/min while venting air from the top port.
   Seal both ports with luer-lock stoppers.
9. Weigh filled phantom to confirm volume (target: 16.3 ± 0.5 kg).

#### 2.1.5  Material Characterisation

Before modal testing, characterise each batch of silicone:

1. **Tensile test** (ASTM D412): Cast 5 dog-bone specimens alongside the
   phantom.  Test at 0.5 mm/s on an Instron 5944 or MTS Criterion.  Extract
   E from the 0–10 % strain region (tangent modulus).
2. **Dynamic Mechanical Analysis** (DMA): Use a TA Instruments DMA 850 or
   equivalent.  Frequency sweep 0.1–20 Hz at 1 % strain, 23 °C.  Record
   storage modulus E′(f) and loss tangent tan δ(f).
3. **Density** (ASTM D792): Weigh specimen in air and in water.  Compute
   ρ_wall.
4. Record all values in a calibration spreadsheet.  Propagate measured E and
   tan δ through the analytical model for comparison.

### 2.2  Instrumentation

#### Sensors

| Sensor | Model (example) | Specification | Approx. cost |
|---|---|---|---|
| Accelerometer (reference) | PCB 352C33 | 100 mV/g, 0.5–10 kHz | $350 |
| Accelerometer (shell, lightweight) | PCB 352A56 | 10 mV/g, 0.5 Hz–10 kHz, 0.6 g | $280 |
| MEMS accelerometer (ultra-light) | Analog Devices ADXL355 eval board | ±2 g, 22-bit, 1 kHz BW, <1 g mass | $50 |
| Laser vibrometer (single-point) | Polytec PDV-100 or OFV-5000 | 0.02 μm/s @ 1 Hz, non-contact | (lab shared) |
| Scanning vibrometer | Polytec PSV-500 | Full-field mode shapes | (lab shared) |
| Miniature hydrophone | Brüel & Kjær 8103 | −211 dB re 1 V/μPa, 0.1 Hz–180 kHz | $500 |
| Infrasound microphone | G.R.A.S. 40AZ | 0.5 Hz–20 kHz, ≤ 148 dB | $900 |
| Impact hammer | PCB 086C03 (medium tip) | 2.25 mV/N, soft rubber tip | $1 400 |

#### Excitation Sources

| Source | Model (example) | Range | Approx. cost |
|---|---|---|---|
| Electrodynamic shaker | Brüel & Kjær 4809 + PA 100E amplifier | 0–10 kHz, 45 N peak | (lab shared) |
| Subwoofer | JBL SRX828SP or DIY 21″ driver | 1–100 Hz, ≥ 130 dB @ 1 m | $500–1 500 |
| Subwoofer amplifier | Crown XLS 2502 | 2 × 440 W @ 8 Ω | $450 |

#### Data Acquisition

| Item | Model (example) | Channels | Approx. cost |
|---|---|---|---|
| USB DAQ | NI USB-4431 or Dewesoft SIRIUS | 4-ch, 24-bit, 102.4 kS/s | (lab shared) |
| Software | NI LabVIEW / Dewesoft X / Python (free) | — | — |

### 2.3  Test Procedures

#### Phase 1 — Impact Modal Survey (Day 1)

**Purpose:** Quick identification of natural frequencies and mode shapes.

1. Place phantom on a vibration-isolated optical table (Newport or TMC) with
   a foam cradle supporting 30 % of the surface (bottom hemisphere).
2. Attach 3 lightweight accelerometers (ADXL355 eval boards, < 1 g each)
   to the shell using cyanoacrylate or micro-dot wax:
   - Sensor A: equatorial apex (0°)
   - Sensor B: 45° latitude
   - Sensor C: polar apex (90°)
3. Impact the phantom at 10 locations (5 per hemisphere, evenly distributed)
   using the PCB 086C03 with a **soft rubber tip** (ensures energy below 50 Hz).
4. Record 5 impacts per location at 1024 Hz sample rate.
5. Compute Frequency Response Functions (FRFs):  
   H(f) = S_{xy}(f) / S_{xx}(f),  coherence γ²(f) ≥ 0.9.
6. Extract natural frequencies from peaks in |H(f)|; confirm with imaginary
   part of H (peaks should be purely imaginary at resonance for lightly
   damped modes).
7. Estimate damping via half-power bandwidth: ζ = Δf / (2 f_n).
8. **Expected results:**  f₂ = 2.8–5.2 Hz (depending on silicone E),
   f₃ = 4.5–8.5 Hz.

#### Phase 2 — Mechanical Excitation / Shaker (Days 2–3)

**Purpose:** Measure transmissibility function T(f) for comparison with
the analytical base-excitation model.

1. Mount phantom on a rigid aluminium plate (400 × 400 × 10 mm) bolted to
   the shaker armature.
2. Attach reference accelerometer (PCB 352C33) to the plate.
3. Attach shell accelerometers (same positions as Phase 1).
4. Drive shaker with **logarithmic sine sweep**: 1–20 Hz over 120 s,
   acceleration amplitude 0.1 m/s² RMS (well within linear regime).
5. Repeat at 0.5 m/s² and 1.0 m/s² to check linearity.
6. Compute:
   - Transmissibility T(f) = |X_shell(f)| / |X_base(f)|
   - Relative displacement transfer function H_rel(f)
   - Phase angle φ(f) between base and shell
7. Compare T(f) with the analytical model prediction:  
   H_rel = r² / √[(1−r²)² + (2ζr)²]
8. **Expected results at resonance:**  
   - Ecoflex 00-30: peak T ≈ 2.8 at ≈ 2.8 Hz  
   - Dragon Skin 10A: peak T ≈ 4.2 at ≈ 4.2 Hz

#### Phase 3 — Scanning Vibrometer Mode Shapes (Day 4)

**Purpose:** Visualise mode shapes and confirm n=2 oblate-prolate pattern.

1. Apply retroreflective tape patches (3M Scotchlite) at ≥ 50 points on the
   upper hemisphere.
2. Set up Polytec PSV-500 scanning head 1.5 m from phantom.
3. Drive phantom with shaker at each identified resonance frequency
   (narrowband random ±0.5 Hz) at 0.1 m/s².
4. Acquire 10 averages per point; compute complex velocity.
5. Reconstruct mode shapes using Polytec software.
6. **Expected:**  
   - n=2: two nodal lines (oblate-prolate oscillation)
   - n=3: three nodal lines (trilobed)

#### Phase 4 — Airborne Acoustic Excitation (Days 5–6)

**Purpose:** Measure airborne coupling efficiency and confirm (ka)² penalty.

1. Place phantom in the centre of a large room (≥ 5 m × 5 m × 3 m) or
   semi-anechoic chamber.  Place the subwoofer array (2 × 21″ drivers in
   sealed enclosure) 2 m from the phantom.
2. Mount infrasound microphone (G.R.A.S. 40AZ) at the phantom location
   (remove phantom for calibration run first).
3. Calibrate SPL at the phantom position: sine sweep 2–20 Hz in 0.5 Hz
   steps.  Record SPL at each frequency.
4. Replace phantom.  Measure shell surface velocity with laser vibrometer
   (Polytec PDV-100) at the equatorial apex.
5. Drive at **100, 110, 120, 125 dB** SPL (use caution above 120 dB —
   hearing protection required).
6. Compute coupling displacement: ξ = ∫ v(t) dt (integrate velocity signal).
7. **Expected:**  At 120 dB and f₂ ≈ 4 Hz:  
   ξ_air ≈ 0.01–0.02 μm (at the noise floor of most vibrometers).  
   This confirms the prediction that airborne coupling is unmeasurably small.
8. **Practical note:**  The laser vibrometer noise floor (typically 0.01 μm/s
   at 1 Hz → ξ ≈ 0.003 μm at 4 Hz) may be insufficient to resolve the
   airborne response.  This *non-detection* is itself a validation of the
   model prediction that ξ_air < 0.02 μm.

#### Phase 5 — Parametric Material Sweep (Days 7–8)

**Purpose:** Validate the predicted f₂ ∝ √E dependence using mixed-ratio
silicone phantoms.

1. Fabricate 4–5 additional phantoms with intermediate E values
   (Ecoflex/Dragon Skin blends).
2. Repeat Phase 1 (impact modal survey) on each.
3. Plot measured f₂ vs. measured E (from tensile tests).
4. Overlay the analytical prediction: f₂(E) from the model.
5. **Expected:**  Measured and predicted f₂ should agree within ±15 %
   (limited by geometric variability in casting).

### 2.4  Data Analysis Pipeline

```
Raw data (accelerometer / vibrometer time series)
  │
  ├── 1. Preprocessing
  │     • Bandpass filter: 0.5–50 Hz (4th-order Butterworth)
  │     • Detrend (remove DC offset)
  │     • Window: Hanning (for spectral analysis)
  │
  ├── 2. Spectral analysis
  │     • FFT with zero-padding to 0.1 Hz resolution
  │     • Cross-spectral density S_xy(f)
  │     • Auto-spectral density S_xx(f), S_yy(f)
  │     • Coherence: γ²(f) = |S_xy|² / (S_xx · S_yy)
  │
  ├── 3. Modal parameter extraction
  │     • Natural frequencies: peaks in |H(f)| with γ² > 0.9
  │     • Damping: half-power bandwidth or circle fit
  │     • Mode shapes: complex amplitude ratios at f_n
  │
  ├── 4. Model comparison
  │     • Overlay analytical H_rel(f) on measured T(f)
  │     • Chi-squared goodness-of-fit for each formulation
  │     • Parameter estimation: fit E, ζ to minimise |T_meas − T_model|²
  │
  └── 5. Outputs
        • Table: measured vs predicted f_n for each formulation
        • Figure: T(f) measured vs model
        • Figure: f₂ vs E with error bars
        • Figure: mode shape animations (from scanning vibrometer)
```

All analysis code will be in Python using `numpy`, `scipy.signal`,
`matplotlib`, and the project's analytical model (`natural_frequency_v2.py`).

### 2.5  Expected Results and Error Estimates

| Quantity | Predicted | Expected meas. range | Uncertainty source |
|---|---|---|---|
| f₂ (Ecoflex 00-30) | 2.83 Hz | 2.4–3.3 Hz | E uncertainty ±20 %, geometry ±5 % |
| f₂ (Dragon Skin 10A) | 4.17 Hz | 3.5–4.9 Hz | Same |
| f₂ (Human canonical) | 3.95 Hz | — | Reference only |
| T_peak (shaker, at f₂) | 1/(2ζ) ≈ 2.8–4.2 | 2–5 | Damping uncertainty |
| ξ_air @ 120 dB | 0.014 μm | < 0.05 μm (noise floor) | Non-detection expected |
| ξ_mech @ 0.1 m/s² | 649 μm | 400–900 μm | E, ζ uncertainty |
| Coupling ratio | 46 000× | > 10 000× | Conservative lower bound |
| Mode shape (n=2) | Oblate-prolate | 2 nodal lines | Visual confirmation |

### 2.6  Bill of Materials

| Item | Qty | Unit cost | Total |
|---|---|---|---|
| Ecoflex 00-30 (Trial Kit, 900 g) | 2 | $30 | $60 |
| Dragon Skin 10A (Trial Kit, 900 g) | 2 | $35 | $70 |
| Ecoflex 00-30 (1 gallon) | 1 | $55 | $55 |
| 3D print filament (PLA, 1.5 kg) | 1 | $25 | $25 |
| Mold release (Ease Release 200) | 1 | $20 | $20 |
| Sil-Poxy silicone adhesive | 1 | $15 | $15 |
| Nylon barbed fittings (6 mm) | 10 | $2 | $20 |
| Retroreflective tape (3M Scotchlite) | 1 roll | $15 | $15 |
| ADXL355 eval boards | 3 | $50 | $150 |
| Infrasound microphone (G.R.A.S. 40AZ) | 1 | $900 | $900 |
| Miniature hydrophone (B&K 8103) | 1 | $500 | $500 |
| Subwoofer driver (21″, B&C 21DS115) | 2 | $300 | $600 |
| Subwoofer enclosure (sealed, MDF) | 1 | $150 | $150 |
| Amplifier (Crown XLS 2502) | 1 | $450 | $450 |
| Dog-bone specimen mold (ASTM D412) | 1 | $40 | $40 |
| **Subtotal (consumables + purchased)** | | | **$3 070** |
| *Shared lab equipment (shaker, DAQ, LDV, Instron, DMA)* | | | *$0* |
| **Grand total** | | | **≈ $3 100** |

### 2.7  Safety Considerations

- **Infrasound exposure:**  SPL above 120 dB requires hearing protection
  (ear plugs + muffs).  Limit exposure duration to 15 min per session.
  All personnel must be outside the direct field during high-SPL tests.
- **Silicone handling:**  Platinum-cure silicones are non-toxic; standard
  nitrile gloves suffice.  Work in ventilated area for mold release spray.
- **Shaker:**  Keep hands clear of armature during operation.  Secure phantom
  to plate with straps to prevent ejection.

---

## 3  Experiment 2 — In Vivo Human Subject Study (Future Work)

### 3.1  Rationale

The phantom validates the physics of the shell model with known, controlled
parameters.  The in vivo study extends validation to the actual biological
system with its full complexity (layered wall, organs, boundary conditions).

### 3.2  Protocol Overview

#### 3.2.1  Measurement of Abdominal Wall Elastic Modulus

1. **MR Elastography (MRE):**  Use a clinical MRI system with an external
   driver (Resoundant, 60 Hz) to generate shear waves in the anterior
   abdominal wall.  Invert wave images for shear modulus G.  Convert to
   Young's modulus: E = 2G(1+ν) with ν ≈ 0.495.
2. **Shear-wave elastography (SWE):**  Use Supersonic Imagine Aixplorer or
   Siemens ACUSON S3000 to measure point shear-wave speed in the rectus
   abdominis, external oblique, and subcutaneous fat.
3. **Measure in two states:**  relaxed (supine, end-expiration) and
   contracted (Valsalva manoeuvre).

#### 3.2.2  Whole-Body Vibration Transmissibility

1. **Platform:**  Whole-body vibration platform compliant with ISO 2631
   (e.g. Brüel & Kjær 4808 with custom table, or a commercial WBV unit
   such as Power Plate Pro5).
2. **Posture:**  Seated (per ISO 2631-1, §7.2.2) and standing.
3. **Excitation:**  Vertical sinusoidal sweep, 2–20 Hz, 0.3 m/s² RMS
   (well below EU action value).
4. **Sensors:**
   - Tri-axial accelerometer on platform (reference).
   - Lightweight tri-axial accelerometer taped to anterior abdominal wall
     (umbilicus level) using medical-grade adhesive.
   - Optional: non-contact laser vibrometer aimed at skin surface marked
     with retroreflective dot.
5. **Compute transmissibility:**  
   T(f) = |a_abdomen(f)| / |a_platform(f)|
6. **Compare with:**  
   - Analytical model H(f) using subject-specific E from elastography.
   - Published ISO 2631 seat-to-viscera transmissibility data.

#### 3.2.3  Subjective Response

1. After each frequency step, ask subject to rate perceived abdominal
   discomfort on a visual analogue scale (VAS, 0–100 mm).
2. Record presence/absence of nausea, urge to defaecate, or abdominal
   cramping.
3. Correlate peak discomfort frequency with predicted f₂ for that subject.

### 3.3  Ethics and Regulatory Requirements

- **IRB/Ethics approval:**  Protocol must be submitted to an Institutional
  Review Board (or equivalent national ethics committee) before any human
  testing.  Classification: minimal risk (WBV below EU action value).
- **Informed consent:**  Written consent form explaining vibration exposure,
  MRI procedure, and right to withdraw.
- **Inclusion criteria:**  Healthy adults 18–65 years, BMI 18.5–35.
- **Exclusion criteria:**  Pregnancy, abdominal surgery within 6 months,
  inflammatory bowel disease, hernia, MRI contraindications.
- **Data protection:**  All identifying data pseudonymised; imaging stored
  on encrypted hospital PACS.

### 3.4  Sample Size Estimate

For a paired comparison (predicted f₂ vs measured peak transmissibility
frequency), with expected effect size d = 1.0 (model predicts f₂ within
±25 % of measured), α = 0.05, power = 0.80:

- Required N ≈ 10 subjects (paired t-test).
- Recruit N = 15 to allow for 30 % dropout / data quality issues.

### 3.5  Timeline (In Vivo)

| Phase | Duration | Notes |
|---|---|---|
| Ethics submission and approval | 3–6 months | Minimal-risk pathway |
| Recruitment and screening | 2 months | |
| Elastography sessions | 2 weeks | 15 subjects × 1 h each |
| WBV testing sessions | 3 weeks | 15 subjects × 1.5 h each |
| Data analysis | 4 weeks | |
| **Total** | **≈ 8–12 months** | |

---

## 4  Combined Timeline

```
Month   1   2   3   4   5   6   7   8   9  10  11  12
Phantom ████████████████████
  Fab   ████
  Char  ████
  Modal     ████
  Shaker    ████████
  Acoustic      ████████
  Param.            ████
  Analysis              ████████
In vivo                     ████████████████████████
  Ethics  ████████████████████
  Recruit             ████████
  MRE/SWE                ████████
  WBV test                    ████████
  Analysis                            ████████████
Paper write-up                                ████████
```

**Critical path:**  Phantom experiments (Months 1–5) should be completed
before the in vivo study begins, so that any model deficiencies discovered
in phantom tests can inform the in vivo protocol.

---

## 5  Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Silicone E differs from datasheet | Frequency mismatch | Tensile-test every batch; adjust model input |
| Phantom leaks at fill ports | Lost test time | Over-design seal; keep spare phantoms |
| Airborne signal below noise floor | Cannot measure ξ_air | This is the *expected* result; treat non-detection as confirmation |
| Shaker resonance coincides with f₂ | Spurious peak | Characterise shaker–plate system independently |
| In vivo ethics delayed | Schedule slip | Begin phantom work immediately; submit ethics in parallel |
| Subject variability obscures trend | Weak statistics | Power analysis recommends N ≥ 15 |

---

## 6  References

- ISO 2631-1:1997 — Mechanical vibration and shock — Evaluation of human
  exposure to whole-body vibration.
- Griffin, M.J. (1990) *Handbook of Human Vibration*. Academic Press.
- Kitazaki, S. & Griffin, M.J. (1998) Resonance behaviour of the seated
  human body. *J. Biomechanics* 31(2):143–149.
- Mansfield, N.J. (2005) *Human Response to Vibration*. CRC Press.
- Coste, B. et al. (2010) Piezo1 and Piezo2 are essential components of
  distinct mechanically activated cation channels. *Science* 330:55–60.
- Parker, K.J. et al. (2011) Imaging the elastic properties of tissue.
  *Phys. Med. Biol.* 56:R1–R29.
