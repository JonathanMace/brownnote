# Research Log — Gas Pocket Detailed Analysis

## Date
2026-03-27

## Objective

Develop a rigorous constrained-bubble model for bowel gas pockets as acoustic
transducers.  The preliminary analysis (`gas_pocket_resonance.py`) used a free
Minnaert bubble and found ~0.94 μm displacement at 120 dB for R = 2 cm pockets
— 7–17× more efficient than whole-cavity resonance.  This log documents the
full model extension.

## What Was Done

Created `src/analytical/gas_pocket_detailed.py` implementing six analysis
components:

### 1. Constrained-Bubble Model

The intestinal wall adds both stiffness (hoop stress) and mass to the gas
pocket oscillation.  For a spherical pocket of radius *a* enclosed by a thin
elastic shell (thickness *h*, Young's modulus *E_w*, Poisson's ratio *ν*):

```
K_gas  = 3γP₀                          (gas polytropic stiffness)
K_wall = 2 E_w h / [a(1 − ν)]          (thin-shell hoop stiffness)
M_gas  = ρ_f a                          (radiation added mass)
M_wall = ρ_w h                          (shell inertia)

ω₀² = (K_gas + K_wall) / [a² (M_gas + M_wall)]
```

**Key finding:** With E_wall = 10 kPa (intestinal tissue), the wall stiffness
term significantly raises the resonance frequency for small pockets:

| Volume | f₀ (free) | f₀ (elastic wall) | Ratio |
|--------|-----------|-------------------|-------|
| 1 mL   | 517 Hz    | 5503 Hz           | 10.6× |
| 10 mL  | 240 Hz    | 1894 Hz           | 7.9×  |
| 50 mL  | 140 Hz    | 877 Hz            | 6.3×  |
| 100 mL | 111 Hz    | 627 Hz            | 5.6×  |

The wall constraint pushes all resonances further above the infrasound band.
However, the sub-resonant response (which is what matters at 7 Hz) is only
weakly affected because the stiffness increase is modest compared to the
gas stiffness at these radii.

### 2. Cylindrical Geometry

Real bowel gas occupies elongated columns in the intestinal lumen (R ≈ 1.5 cm).
Two modes were modelled:

- **Radial breathing mode**: ω² = (2γP₀ + E_w h/R(1−ν²)) / (R²(ρ_f + ρ_w h/R))
- **Axial piston mode**: ω² = γP₀ πR²/L / (2 × 8ρ_f R³/3)

The axial mode is lower-frequency for long pockets and comes closest to the
infrasound band (f_ax ≈ 31 Hz for 100 mL).

**Critical insight:** For cylindrical pockets, the radial displacement is
determined by the lumen radius (fixed at ~1.5 cm), not the pocket length.
This gives ~1.05 μm at 120 dB regardless of volume.  The cylindrical radial
mode is *geometry-limited*.

### 3. Multiple Gas Pockets

At infrasound frequencies (λ_tissue ≈ 220 m at 7 Hz), all gas pockets in
the abdomen (~30 cm span) are in the same pressure zone and oscillate
coherently.  The total volume displacement sums linearly:

- 100 mL total (10 pockets):  ΔV_total = 14.0 nL
- 200 mL total:               ΔV_total = 28.2 nL
- 800 mL total:               ΔV_total = 116 nL
- 1500 mL total:              ΔV_total = 226 nL

The total volume displacement scales linearly with total gas content — a
16× variation across the physiological range.

### 4. Tissue Coupling

The gas pocket oscillation radiates into surrounding tissue as a monopole
source.  Near-field displacement:

```
u(r) = (a/r)² × ξ_wall     for r > a
```

For a 50 mL spherical pocket (a = 22.9 mm) at 120 dB:

| Distance | Tissue displacement |
|----------|-------------------|
| 25 mm    | 0.89 μm           |
| 30 mm    | 0.62 μm           |
| 50 mm    | 0.22 μm           |
| 100 mm   | 0.06 μm           |

The displacement falls off rapidly (1/r²), concentrating mechanical
stimulation in the tissue immediately surrounding the gas pocket.
This is qualitatively different from whole-cavity resonance, which
distributes displacement over the entire abdominal wall.

### 5. Parameter Study

Swept gas volume (1–100 mL), geometry (spherical/cylindrical), wall
constraint (free/elastic/rigid), and frequency (1–50 Hz).

**Figures generated:**

- `fig_gas_pocket_frequency_response.png` — 4-panel (geometry × wall):
  Shows flat sub-resonant response in the 1–20 Hz band with resonance
  peaks visible for larger cylindrical pockets approaching 30–50 Hz.
  The elastic wall strongly damps the resonance peaks.

- `fig_gas_pocket_variability.png` — 4-panel population model:
  (A) Log-normal gas distribution, (B) displacement histogram,
  (C) gas-volume → displacement scatter, (D) population CDF.

### 6. Inter-Individual Variability (Population Monte Carlo)

10,000 simulated individuals with:
- Total bowel gas: log-normal (median 200 mL, range 30–2000 mL)
- Pocket count: Poisson (mean 10, range 2–40)
- Volume split: Dirichlet (random partitioning)
- Geometry: 70% cylindrical, 30% spherical

**Key results at 7 Hz, 120 dB:**
- 100% of simulated individuals exceed the 0.5 μm PIEZO threshold
- Max pocket-wall displacement: median ~1.05 μm, tail to ~2.8 μm
- Individuals with high gas volumes AND skewed pocket-size distributions
  (one or two large pockets) show 2–3× higher displacement

## Key Finding: SPL Threshold Variability

The SPL at which gas-pocket displacement first exceeds the PIEZO threshold
(0.5 μm) depends on pocket size:

| Pocket         | Geometry    | SPL threshold |
|----------------|-------------|---------------|
| 5 mL           | Spherical   | ~120 dB       |
| 20 mL          | Spherical   | ~116 dB       |
| 50 mL          | Spherical   | ~113 dB       |
| 100 mL         | Spherical   | ~111 dB       |
| 10 mL          | Cylindrical | ~114 dB       |
| 50 mL          | Cylindrical | ~113 dB       |

**This 9 dB range (111–120 dB) corresponds to a factor of ~3× in pressure
and ~8× in intensity.**  Individuals with large gas pockets reach the
activation threshold at substantially lower SPLs.

## Discussion

### Can gas pockets explain differential susceptibility?

**Yes, partially.**  The model predicts:

1. **Total volume displacement** varies 16× across the physiological gas
   range (100–1500 mL).  More gas → more total tissue disturbance.

2. **Peak local displacement** depends on the *largest* pocket.  An individual
   with one 100 mL pocket (post-meal bloating, IBS) gets 1.3 μm vs 0.62 μm
   for someone with only 10 mL pockets.

3. **SPL thresholds** span 111–120 dB depending on the largest pocket.
   This means a person with a large gas pocket could experience the onset
   of mechanotransduction at ~111 dB, while someone with only small pockets
   needs ~120 dB — a factor of 3× in acoustic pressure.

4. **The mechanism does NOT require resonance.**  All gas pockets operate
   far below their resonance frequencies at 7 Hz.  The response is
   quasi-static: ξ ≈ p_inc / k_eff.

### Limitations

1. **Wall stiffness uncertainty.**  Intestinal wall E ranges from 1–50 kPa
   depending on muscle tone, layer, and inflation state.  At 1 kPa the
   wall constraint is negligible; at 50 kPa it reduces spherical-pocket
   displacement by ~2×.

2. **Non-spherical geometry detail.**  Real gas pockets have irregular
   shapes (haustra, flexures).  The spherical and cylindrical models
   bracket the realistic case.

3. **Viscoelastic relaxation.**  At infrasound frequencies the intestinal
   wall may behave closer to a viscous fluid than an elastic solid,
   reducing the effective wall stiffness.  This would *help* the mechanism.

4. **120 dB is still loud.**  The gas-pocket mechanism does not rescue the
   "brown note at concert levels" (95–110 dB) idea, but it does provide
   a plausible pathway at extreme SPL (>110 dB) consistent with military
   and industrial exposure scenarios.

5. **PIEZO threshold is approximate.**  The 0.5 μm threshold for
   mechanosensitive ion-channel activation comes from in-vitro studies;
   in-vivo thresholds may differ.

### Comparison with Whole-Cavity Resonance

| Mechanism | ξ at 120 dB, 7 Hz | Frequency dependence | Variability |
|-----------|-------------------|---------------------|-------------|
| Whole-cavity (n=2 mode) | 0.14 μm | Strong (resonance at ~15 Hz) | Body size |
| Gas pocket (cylindrical) | 1.05 μm | Weak (sub-resonant) | Gas content |
| Gas pocket (sph., 50 mL) | 1.06 μm | Weak | Gas content + size |

Gas pockets are **7–10× more efficient** than whole-cavity resonance for
airborne acoustic coupling and provide a physically distinct source of
inter-individual variability.

## Implications for the Paper

This analysis supports a two-mechanism narrative:

1. **Whole-body vibration** (mechanical coupling) remains the dominant
   pathway at physiological exposure levels.

2. **Gas-pocket transduction** (airborne coupling) is the most plausible
   mechanism for the popularly described "brown note" at extreme SPL.
   It explains why:
   - Effects are inconsistent across individuals (gas content varies)
   - GI symptoms predominate (gas pockets are *in* the GI tract)
   - The effect requires very high SPL (>110 dB)
   - Post-meal or IBS subjects might be more susceptible

This is sufficiently novel for a standalone paper or a major section.

## Files Created

- `src/analytical/gas_pocket_detailed.py` — full analysis module
- `data/figures/fig_gas_pocket_frequency_response.png` — frequency response
- `data/figures/fig_gas_pocket_variability.png` — population variability
- `docs/research-logs/gas-pocket-detailed-analysis.md` — this log
