# Research Log — 2026-03-27T04:30 — Corrected Acoustic Coupling Model

## What Was Done

Implemented `src/analytical/acoustic_coupling.py` — a corrected model for
how airborne infrasound couples into the abdominal cavity shell model.

### Key Physics Arguments

1. **Long-wavelength limit confirmed**: ka = 0.017 at 7 Hz — body is 1/70th
   of a wavelength. The pressure field is uniform across the body.

2. **Radiation damping negligible**: ζ_rad = 3.67×10⁻⁶, which is 4-5 orders
   of magnitude smaller than structural damping (ζ_struct ≈ 0.05-0.20).

3. **Full pressure drives the shell**: The shell responds to p_incident / k_shell,
   where k_shell is the membrane stiffness. Not to the acoustic particle
   displacement.

### Results

| Model | SPL=100 dB | SPL=120 dB | SPL=130 dB |
|-------|-----------|-----------|-----------|
| Naive (old) | 0.12 μm | 1.21 μm | 3.83 μm |
| Corrected | 28.0 μm | 280 μm | 886 μm |
| Ratio | 232× | 232× | 232× |

PIEZO threshold (1 μm) reached at **80 dB** for all Q values tested.

## Critical Self-Analysis

### 🔴 THIS RESULT IS SUSPICIOUS

28 μm displacement at 100 dB (normal conversation level) is extremely large.
If this were correct, people would constantly feel their abdomens resonating
in everyday environments. This does not match reality.

### Possible Errors

1. **The abdomen is NOT a free shell in air.** It's embedded inside the body,
   surrounded by other tissue. The exterior surface doesn't face air — it faces
   muscle, fat, and skin. The acoustic pressure from air must FIRST transmit
   through the body wall before reaching the peritoneal cavity. My model skips
   this entirely.

2. **The stiffness calculation may be wrong.** With E=0.1 MPa, the membrane
   stiffness is only ~261 Pa/m. This means a 1 Pa pressure produces 4 mm of
   displacement. That's clearly wrong for soft tissue in a physiological context
   — intra-abdominal pressure is 5-12 mmHg (667-1600 Pa) and the abdomen
   doesn't inflate by meters.

3. **Missing: pre-stress from intra-abdominal pressure.** The abdominal wall
   is under tension from intra-abdominal pressure (~1000 Pa). This pre-stress
   dramatically increases the effective stiffness. It's like a drum head — the
   membrane stiffness is low, but the tension stiffness is high.

4. **Missing: fluid compressibility.** The contained fluid has bulk modulus
   K = 2.2 GPa. For volumetric compression of the cavity, the fluid stiffness
   k_fluid = 3K/R is enormous. The breathing mode MUST overcome the fluid's
   bulk modulus to compress the cavity. This should dominate over the shell
   membrane stiffness by many orders of magnitude.

### The Real Physics

For the breathing mode of a fluid-filled shell:
- Shell membrane stiffness: k_shell = 2Eh / [R²(1-ν)] ≈ 261 Pa/m
- Fluid volumetric stiffness: k_fluid = 3K / R ≈ 3×2.2×10⁹ / 0.15 ≈ 4.4×10¹⁰ Pa/m

**The fluid stiffness dominates by 8 orders of magnitude!**

The breathing mode frequency should be dominated by the fluid bulk modulus,
not the shell membrane stiffness. My calculation of the breathing mode
frequency using k_shell alone is fundamentally wrong for the breathing mode
of a fluid-filled shell.

The CORRECT breathing mode frequency for a fluid-filled rigid shell (Helmholtz):
f_0 = c_fluid / (2πR) × √(3) ≈ 1540 / (2π × 0.15) × 1.73 ≈ 2830 Hz

This is WAY above the 5-10 Hz range. The fluid bulk modulus makes the
breathing mode thousands of Hz, not single digits.

### What Modes ARE in 5-10 Hz?

The modes in the 5-10 Hz range must be **flexural/bending modes** where the
shell deforms without significant volume change. Like a water balloon wobbling —
the water sloshes, the shape changes, but the total volume barely changes.

These are the n ≥ 2 modes where the fluid acts as added mass (inertial loading)
but NOT as a volumetric spring. The fluid moves with the shell walls, increasing
the effective mass, but the restoring force comes from shell bending stiffness,
not fluid compression.

This means:
- Breathing mode (n=0): very high frequency (>1000 Hz) — NOT relevant
- Flexural modes (n≥2): potentially in the 5-10 Hz range
- The n=2 mode is the most relevant (oblate-prolate oscillation)

### Impact

The entire acoustic coupling model needs to be rewritten. The driving mechanism
is NOT uniform pressure → volumetric compression. It's:
1. Pressure gradient across the body → differential loading on shell
2. Shell flexural response (n≥2 modes) → shape change without volume change
3. Fluid sloshing / redistribution inside the cavity

For flexural modes driven by pressure gradient, the coupling is:
- ΔP across the body ≈ p × 2ka (pressure difference over body diameter)
- At ka = 0.017: ΔP = 0.034 × p_incident
- This 3.4% pressure gradient is what drives the flexural modes

This significantly reduces the predicted displacement and is probably the
correct physics.

## Plan Changes

1. **[URGENT]** Rewrite coupling model for flexural modes with pressure gradient
2. **[URGENT]** Add fluid compressibility to breathing mode (will push it to kHz)
3. Focus on n=2 mode as the physiologically relevant mode
4. Include pre-stress from intra-abdominal pressure
5. Need to wait for reviewer-b agent results for additional issues

## Ideas

The n=2 mode (oblate-prolate oscillation) is actually very interesting because:
- It's a "sloshing" mode where fluid redistributes inside the cavity
- It could cause localized pressure variations against intestinal walls
- The mode shape concentrates displacement at the equator (anterior wall)
- This is where the thinnest tissue is and where people "feel" subwoofers
