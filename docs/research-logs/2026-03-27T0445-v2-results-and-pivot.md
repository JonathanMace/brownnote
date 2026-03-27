# Research Log — 2026-03-27T04:45 — V2 Analysis Results

## What Was Done

Implemented `natural_frequency_v2.py` with corrected fluid-structure coupling:
1. Breathing mode now includes fluid bulk modulus → 2897 Hz (NOT in brown note range)
2. Flexural modes (n≥2) properly treat fluid as added mass only → 5-10 Hz range ✓
3. Pre-stress from intra-abdominal pressure included
4. Acoustic coupling coefficient (ka)^n properly computed

## Key Results

### Modal Frequencies (corrected)
- Breathing mode n=0: ~2900 Hz (irrelevant — fluid compression dominated)
- Flexural n=2: 5.5 Hz (soft tissue) — IN the brown note range
- Flexural n=3: 6.0-8.4 Hz — also in range for some configurations
- Pre-stress increases frequencies (tension stiffening)

### Acoustic Coupling
- ka = 0.017 at 7 Hz (deep long-wavelength regime)
- For n=2 mode: coupling ∝ (ka)² ≈ 1.6×10⁻⁴
- Only 0.016% of incident pressure drives flexural modes
- SPL for 1 μm displacement via airborne path: ~137 dB

### Physical Interpretation
The flexural modes (shape changes without volume change) are the relevant
low-frequency modes. These are "wobbling" modes where the shell deforms
and fluid sloshes inside. The n=2 mode is oblate-prolate oscillation.

For AIRBORNE infrasound: coupling is very weak (ka penalty)
For MECHANICAL vibration: coupling is direct (no ka penalty)

This explains why whole-body vibration (ISO 2631) causes GI effects but
airborne infrasound at moderate levels does NOT.

## Critical Analysis

### What's Correct Now
- ✅ Fluid coupling properly handled (breathing mode in kHz, flexural in Hz)
- ✅ Pre-stress included
- ✅ Acoustic coupling coefficient properly computed
- ✅ Results consistent with ISO 2631 (5-10 Hz abdominal resonance)

### Remaining Issues
- ⚠️ Still using equivalent sphere approximation
- ⚠️ (ka)^n coupling may be too pessimistic — what about body wall
  transmission? Sound doesn't just diffract around the body; it also
  transmits through the chest/abdominal wall with SOME efficiency
- ⚠️ Orifice coupling (mouth → GI tract) not modeled
- ⚠️ Whole-body vibration coupling (mechanical) needs separate model
- ⚠️ Haven't validated against published whole-body resonance data

### Paper Framing Update

The paper should now have TWO main threads:
1. **Airborne acoustic pathway**: Weak coupling (ka penalty), but quantified
   for the first time. Shows why the "brown note" as popularly described
   (loudspeaker causing GI effects) is implausible at moderate SPL.
2. **Mechanical vibration pathway**: Strong coupling, consistent with ISO 2631.
   Shows why whole-body vibration at 5-10 Hz IS biologically relevant.

The novel contribution is the QUANTITATIVE comparison of these two pathways,
using the same underlying modal analysis. This has never been done.

## Plan Changes

1. ~~Fix impedance mismatch~~ → DONE (v2 analysis)
2. Next: Add mechanical vibration coupling model (ground/seat excitation)
3. Next: Validate against ISO 2631 transmissibility data
4. Next: Get reviewer-b results and address findings
5. Update figures with v2 results
