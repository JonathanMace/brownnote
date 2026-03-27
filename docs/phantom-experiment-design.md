# Phantom Experiment Design — Validation of Fluid-Filled Shell Model

## Objective

Design a laboratory experiment to validate the analytical predictions of
flexural mode frequencies and coupling efficiencies for a fluid-filled
viscoelastic shell, using a tissue-mimicking phantom.

## Motivation

The strongest reviewer criticism is the absence of experimental validation.
Even a simple phantom experiment comparing analytical predictions with
measured frequencies/amplitudes would dramatically strengthen the paper.

## Phantom Design

### Option A: Silicone Rubber Shell (Recommended)

**Construction:**
1. Cast a hollow oblate spheroidal silicone shell using 3D-printed molds
2. Inner mold: oblate spheroid (a=18cm, c=12cm)
3. Outer mold: slightly larger oblate spheroid (a=19cm, c=13cm) → h=10mm
4. Material: Ecoflex 00-30 or Dragon Skin 10 (Shore 00-30 to 10A)
5. Fill with degassed water through a sealed port

**Material Calibration:**
- Measure E of the silicone with a tensile test (Instron or similar)
- Expected range: 0.05-0.5 MPa (Ecoflex) or 0.1-2 MPa (Dragon Skin)
- Measure loss tangent with DMA (Dynamic Mechanical Analysis)
- Target: E ≈ 0.1 MPa to match relaxed abdominal wall

**Advantages:**
- E can be tuned by silicone formulation
- Geometry is well-controlled and measurable
- Water-filled → known fluid properties
- Can inject air bubbles for gas pocket experiments
- Can be constrained (partially clamped) to test BC effects

**Disadvantages:**
- Isotropic (real tissue is anisotropic)
- Uniform wall (real wall is multi-layer)
- No organs or mesentery

### Option B: Gelatin Shell

**Construction:**
1. Double balloon technique: inflate balloon to spheroid shape in gelatin mold
2. Multiple dipping to build up wall thickness
3. Control E through gelatin concentration (10-20% w/v)
4. Fill with water

**Material properties:**
- E = 0.01-0.1 MPa (tunable with concentration)
- More biologically realistic viscoelastic behavior
- Limited shelf life (days), temperature-sensitive

### Option C: Commercial Rubber Balloon (Quick Validation)

**Construction:**
1. Large latex balloon (~15-20cm diameter when inflated)
2. Fill with water to oblate spheroid shape (support in a bowl)
3. Very thin wall (h ≈ 0.3-1mm)

**Advantages:** Fast, cheap, immediately available
**Disadvantages:** Geometry not well controlled, very thin wall

## Instrumentation

### Frequency Measurement (Modal Analysis)

1. **Laser Doppler Vibrometer (LDV)** — Gold standard
   - Polytec PSV-500 or similar
   - Scan the shell surface for mode shapes
   - Frequency resolution: 0.01 Hz
   - Non-contact → no mass loading

2. **Accelerometers** — Simpler
   - Lightweight MEMS accelerometers (< 1g mass)
   - Mount to shell surface with wax
   - Multiple points for mode identification
   - Concern: mass loading on soft shell

3. **Hydrophone** — Internal pressure measurement
   - B&K 8103 or similar miniature hydrophone
   - Insert through sealed port
   - Measures internal pressure oscillation

### Excitation

**Mechanical (WBV simulation):**
- Electrodynamic shaker (Brüel & Kjær 4809 or similar)
- Phantom sits on rigid plate mounted to shaker
- Sine sweep 1-20 Hz, acceleration 0.1-2.0 m/s²
- Control with accelerometer on plate

**Airborne acoustic:**
- Large subwoofer (18" or 21") in sealed enclosure
- Or: dedicated infrasound source (Rotary Woofer, pneumatic)
- Calibration microphone (G.R.A.S. 40AZ or similar)
- SPL range: 90-130 dB at 2-20 Hz
- Test in anechoic chamber or large room (λ ≈ 50m at 7 Hz!)

**Impact (for modal identification):**
- Instrumented impact hammer with soft tip
- Impulse response → FFT → natural frequencies
- Quick screening method before detailed sweeps

## Experimental Protocol

### Phase 1: Modal Identification (Impact Test)

1. Fill phantom, seal, equilibrate temperature (22°C)
2. Mount phantom on vibration-isolated stand
3. Impact with instrumented hammer at 10 locations
4. Record response at 3-5 locations (accelerometers or LDV)
5. Compute FRFs → identify natural frequencies and mode shapes
6. Compare with analytical predictions

### Phase 2: Mechanical Excitation (Shaker)

1. Mount phantom on shaker platform
2. Sine sweep: 1-20 Hz, 0.1 m/s² to 2.0 m/s²
3. Record:
   - Base acceleration (control accelerometer)
   - Shell surface displacement (LDV)
   - Internal pressure (hydrophone)
4. Compute transfer functions
5. Compare with model predictions:
   - Resonant frequency
   - Transmissibility T(f)
   - Internal pressure amplitude

### Phase 3: Airborne Excitation

1. Place phantom in anechoic environment (or large room)
2. Expose to infrasound: 2-20 Hz, 90-130 dB
3. Record:
   - Incident pressure (reference microphone)
   - Shell surface displacement (LDV)
   - Internal pressure (hydrophone)
4. Measure coupling coefficient: ξ_measured / ξ_predicted
5. KEY TEST: Verify (ka)^n coupling penalty

### Phase 4: Gas Pocket Experiments

1. Inject known volumes of air (1, 5, 10, 20, 50 mL)
2. Repeat Phase 3 at each air volume
3. Measure:
   - Change in natural frequencies
   - Change in airborne coupling
   - Local displacement near gas pocket (LDV pointed at bubble)
4. Compare with gas pocket resonance model predictions

### Phase 5: Boundary Condition Effects

1. Partially clamp phantom (rigid supports simulating spine/pelvis)
2. Repeat Phase 1 with different constraint configurations
3. Measure frequency shift vs. constraint geometry
4. Compare with BC multiplier estimates

## Expected Results

### What We Expect to Confirm
- n=2 flexural mode at 4-10 Hz (depending on silicone E)
- Breathing mode at much higher frequency (>100 Hz for silicone)
- Mechanical coupling >> airborne coupling (by 10³ factor)
- Gas injection increases airborne coupling

### What Might Surprise Us
- Non-linear effects at large amplitude (WBV)
- Mode coupling between flexural and sloshing modes
- The breathing mode might be measurable as internal pressure oscillation
- Gas pocket resonance might be at unexpected frequency (not Minnaert)

## Budget Estimate

| Item | Cost Range |
|------|------------|
| Silicone (Ecoflex 00-30, 2 gallons) | $80-120 |
| 3D-printed molds (resin, ~500g) | $50-100 |
| Accelerometers (3× MEMS) | $50-200 |
| Hydrophone (miniature) | $200-500 |
| Impact hammer (PCB 086C03) | ~$1500 (may borrow) |
| Shaker + amplifier (existing lab) | $0 (shared facility) |
| Subwoofer (18") | $200-500 |
| Calibration microphone | $500-1000 |
| Data acquisition system | $0 (existing lab) |
| **Total (excluding shared equipment)** | **$600-2500** |

## Timeline

- Phantom fabrication: 1-2 weeks
- Material characterization: 1 week
- Modal testing: 1 week
- Mechanical excitation: 1 week
- Acoustic excitation: 1-2 weeks
- Gas pocket experiments: 1 week
- Data analysis and comparison: 2 weeks
- **Total: 8-10 weeks**

## Key Measurements for Paper

The minimum set needed for a compelling validation section:

1. **Measured f₂ vs. predicted f₂** — the core frequency validation
2. **Transmissibility T(f) curve** — compare with model and ISO 2631
3. **Airborne displacement vs. SPL** — confirm weak coupling
4. **Mechanical displacement vs. acceleration** — confirm strong coupling
5. **Coupling ratio: ξ_mech / ξ_air** — the key novel result

If time permits:
6. Mode shapes from scanning LDV
7. Gas pocket coupling enhancement
8. BC sensitivity
