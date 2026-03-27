# Research Log — 2026-03-27T05:30 — Novel: Bowel Gas Pocket Mechanism

## What Was Done

Investigated a novel mechanism: intestinal gas pockets as acoustic displacement
transducers. This is distinct from the whole-cavity resonance model.

## The Idea

The human intestine normally contains 100-200 mL of gas distributed in pockets
ranging from 1-10 cm in effective radius. These gas pockets are compressible
(unlike the surrounding tissue/fluid) and respond to pressure changes by
expanding/contracting. The surrounding tissue (intestinal wall) moves with them.

## Key Results

### Minnaert Resonance
- Gas pocket Minnaert frequencies: 30-330 Hz (above the brown note range)
- At 7 Hz, all gas pockets are driven FAR below resonance (f/f_M ≈ 0.02-0.2)
- No resonant enhancement (H ≈ 1.0)

### Sub-Resonant Response (the important result!)
- Even without resonance, gas pockets respond to pressure because they're compressible
- The displacement is ξ ≈ p_inc / k_gas = p_inc × a / (3γP₀)
- This scales linearly with pocket radius — larger gas volumes → more displacement

### Quantitative Comparison

At 120 dB SPL (20 Pa) at 7 Hz:

| Mechanism | Wall displacement | PIEZO threshold? |
|-----------|-------------------|------------------|
| Whole-cavity resonance (n=2) | 0.14 μm | No (7× below) |
| Gas pocket R=1cm | 0.47 μm | No (just below) |
| Gas pocket R=2cm | 0.94 μm | ~YES |
| Gas pocket R=5cm | 2.4 μm | YES |

**The gas pocket mechanism is 7-17× more efficient than whole-cavity resonance
for airborne acoustic coupling!**

## Why This Is Novel

1. No previous analysis has quantified this mechanism for infrasound → GI effects
2. It explains INTER-INDIVIDUAL VARIABILITY — gas content varies enormously
   (50-500 mL), and people with more bowel gas would be more susceptible
3. It works for AIRBORNE sound (unlike the cavity resonance which requires WBV)
4. It doesn't require resonance — it works at ANY frequency where λ >> body size
5. It provides a quantitative bridge between infrasound exposure and tissue strain

## Critical Analysis

### Strengths
- Simple, well-understood physics (Minnaert/bubble dynamics)
- Quantitative predictions testable with phantom experiments
- Explains known variability in infrasound susceptibility
- Complementary to (not competing with) the cavity resonance model

### Weaknesses
1. ⚠️ The model treats gas pockets as spherical bubbles in infinite fluid.
   Real intestinal gas is distributed in elongated pockets within a tubular
   structure (gut lumen).
2. ⚠️ The intestinal wall adds significant mass and stiffness not captured
   by the simple Minnaert model.
3. ⚠️ 120 dB is still very loud — this doesn't rescue the "brown note at
   concert levels" idea.
4. ⚠️ Haven't accounted for body's acoustic shielding of the gas pockets
   (the sound must still penetrate skin/muscle to reach the gut).
5. ⚠️ The displacement comparison with PIEZO threshold is still the
   "apples-to-oranges" issue — bulk displacement vs cellular-level strain.

### The Body Shielding Issue
At 7 Hz (λ = 49 m >> body size), the body is acoustically transparent.
The pressure field inside the body equals the incident pressure to within (ka)²
corrections. So the gas pocket sees the full incident pressure. This is
actually the correct regime — the shielding only matters at higher frequencies.

## Implications for the Paper

This could be a game-changing addition to the paper:

**Original narrative**: Airborne brown note implausible, only WBV works.
**New narrative**: Airborne coupling via GAS POCKETS is a plausible mechanism
at high SPL (>120 dB), with sensitivity depending on bowel gas content.

The paper could present three mechanisms:
1. Whole-cavity resonance (airborne) — too weak (0.14 μm at 120 dB)
2. Whole-body vibration (mechanical) — strong (~600 μm at 0.1 m/s²)
3. **Gas pocket transduction (airborne) — intermediate (1-5 μm at 120 dB) [NOVEL]**

The gas pocket mechanism bridges the gap between "airborne doesn't work" and
"mechanical works great" and provides a physically plausible pathway for the
popularly described brown note phenomenon at extreme SPL.

## Plan Changes

- Add gas pocket analysis as Section 4 of the paper
- Design a phantom experiment (water-filled balloon + air bubbles + speaker)
- Investigate gas pocket response in more detail (cylindrical geometry,
  constrained by gut wall, frequency-dependent damping)
- This may justify a SECOND paper focused entirely on the gas pocket mechanism
