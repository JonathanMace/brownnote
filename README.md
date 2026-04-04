# The Brown Note

Can sound make you soil yourself? No — but the reason why leads somewhere unexpected.

That is the answer. The interesting part is why. The abdomen does have a real low-frequency flexural resonance near 4 Hz, but airborne sound couples to it so weakly that the "brown note" fails as acoustics and turns into a more useful problem in shell mechanics, vibration, and inverse theory. This repository collects the papers, code, and evidence behind that result.

## The Short Version

The central result is simple. At **120 dB SPL**, the energy-consistent airborne displacement of the abdominal wall is only **0.028 μm**, well below the roughly **1-2 μm** PIEZO mechanotransduction range. The resonance is real; the airborne path to it is not. The transfer-function ratio makes the same point more formally: **H_mech/H_air ≈ 6.5 × 10^6**. Paper 7 matters because the same shell framework can also formalise the watermelon thump test as a prediction of effective rind stiffness, and Papers 8-10 ask when that kind of inversion is mathematically possible.

## If You Read Two Papers

If you read only one paper, read **Paper 1**. If you want to know why the framework is worth keeping after the joke is settled, read **Paper 7**.

### [Paper 1: The Brown Note](papers/paper1-brown-note/) — *Journal of Sound and Vibration*

This is the paper that answers the question. It starts from an empirical asymmetry that has been obvious for decades: whole-body vibration in the 4-8 Hz range can produce gastrointestinal effects, while airborne sound at the same frequencies does not. The model explains that asymmetry from first principles. At the n = 2 flexural resonance, ka is only about 0.01: the wavelength is so long and the air-tissue mismatch so severe that the incident acoustic field barely drives the mode at all, whereas mechanical excitation transmitted through the body wall does.

The takeaway is deliberately unglamorous and therefore trustworthy: there is a genuine abdominal resonance near 4 Hz, but the "brown note" is a mechanical story misremembered as an acoustic one. If you want the definitive debunking, this is it.

### [Paper 7: The Watermelon Thump Test](papers/paper7-watermelon/) — *Postharvest Biology and Technology*

This is the surprise. People really do tap watermelons and listen for a deep, resonant thump, but the folk test has mostly lived as anecdote and produce-market lore. Paper 7 turns that intuition into a quantitative shell model linking tap-tone frequency to **effective rind stiffness** — a firmness measure, not a direct readout of sweetness or eating quality.

The claims stay restrained. The model does **not** magically infer sweetness or eating quality from a sound alone; the step from firmness to ripeness still needs cultivar-specific calibration. What it does show is that the same framework used to debunk the brown note can also formalise a practical nondestructive measurement problem.

## Supporting Analyses

Papers 2-6 are not separate grand theories. They are supporting analyses that stress-test the same framework across related organs, forcing conditions, and physiological scenarios.

| Paper | Focus | What it adds |
|---|---|---|
| [P2 Gas Pockets](papers/paper2-gas-pockets/) | Local gas inclusions | Tissue-constrained bubbles can couple much more strongly than the whole abdominal cavity. |
| [P3 Scaling Laws](papers/paper3-scaling-laws/) | Cross-species scaling | The low-frequency shell mechanics are not uniquely human. |
| [P4 Bladder Resonance](papers/paper4-bladder/) | Organ-specific variation | The same framework predicts a different resonance landscape for the bladder. |
| [P5 Borborygmi](papers/paper5-borborygmi/) | Gut sounds | Bubble-shell acoustics can account for clinically realistic stomach-growl frequencies. |
| [P6 Sub-Bass Coupling](papers/paper6-sub-bass/) | Airborne vs structural bass | Reinforces that the floor and seat matter far more than the air. |

## The Mathematics

The later papers ask a harder question than "what resonates?": **can you work backwards from a spectrum to the parameters that produced it?**

| Paper | Role |
|---|---|
| [P8 Kac Identifiability](papers/paper8-kac/) | Shows that the equivalent-sphere inverse problem is catastrophically ill-conditioned, and that oblate geometry can rescue identifiability. |
| [P9 Lifting Theorem](papers/paper9-lifting-theorem/) | Sharpens the result: not all symmetry breaking helps equally; oblate shells lift the degeneracy, prolate shells do not. |
| [P10 Capstone](papers/paper10-capstone/) | Intended synthesis of excitation, resonance, and identifiability across the whole programme. The ambition is clear; the final paper is still evolving. |

Taken together, these papers are the mathematical backbone of the project. They are the reason Browntone is more than a curiosity about infrasound.

## Key Results

| Quantity | Value |
|----------|-------|
| Flexural frequency f₂ (n = 2) | 3.95 Hz |
| Breathing mode (n = 0) | 2490 Hz |
| Transfer-function ratio H_mech/H_air | ≈ 6.5 × 10^6 |
| Airborne displacement ξ_air at 120 dB | 0.028 μm |
| PIEZO threshold range | 1-2 μm |
| Mechanical displacement ξ_mech at 0.1 m/s² RMS (SDOF upper bound) | 917 μm |
| Coupling ratio R (120 dB vs 0.1 m/s², SDOF upper bound) | ≈ 3.3 × 10^4 |
| Dimensionless frequency Π₀ (cross-species) | 0.07 |
| Watermelon Sobol total-order sensitivity S_T(E) (P7) | 0.86 |
| Condition number κ_sphere | ≈ 1.37 × 10^10 |
| Condition number κ_oblate | 69.4 |
| Scattering parameter ka | 0.0114 |

## Scope and Status

- **Analytical, not yet experimental.** The code and papers are modelling work; a validation protocol exists, but it has not yet been executed.
- **Useful, but not magical.** The watermelon application estimates firmness-related stiffness; cultivar-specific ripeness calibration still sits outside the model.
- **Mostly settled, not entirely finished.** Papers 1-9 contain the current core results of the programme; Paper 10 is the synthesis still being written.

## For Researchers

The core model treats the abdomen as a **fluid-filled viscoelastic oblate spheroidal shell**. In the forward problem, an equivalent-radius formulation captures the dominant low-frequency behaviour; in the inverse problem, the full oblate geometry matters because asphericity is exactly what breaks the spectral degeneracy. Flexural modes (n ≥ 2) govern the infrasonic response. The breathing mode (n = 0) sits around 2490 Hz and is not the low-frequency story. At present, the programme is analytical; an experimental validation protocol exists, but it has not yet been executed.

### Quick Start

```bash
pip install -e .[dev]
python -m pytest tests/ -v
```

```python
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)
from src.analytical.energy_budget import self_consistent_displacement
from src.analytical.mechanical_coupling import compare_airborne_vs_mechanical

model = AbdominalModelV2(
    E=0.1e6, a=0.18, c=0.12, h=0.01, nu=0.45,
    rho_wall=1100, rho_fluid=1020, K_fluid=2.2e9,
    P_iap=1000, loss_tangent=0.25,
)

freqs = flexural_mode_frequencies_v2(model, n_max=5)
disp = self_consistent_displacement(model, mode_n=2, spl_db=120)
ratio = compare_airborne_vs_mechanical(model)
```

### Citation

```bibtex
@misc{browntone2026,
  author = {Mace, Jonathan and Mace, Brian R.},
  title  = {Browntone: Vibroacoustics of Fluid-Filled Soft Shells},
  year   = {2026},
  url    = {https://github.com/JonathanMace/brownnote}
}
```

## Repository Structure

```text
browntone/
├── papers/paper1-brown-note/   # The definitive debunking
├── papers/paper7-watermelon/   # The firmness/stiffness application
├── papers/paper2-gas-pockets/ ... paper6-sub-bass/  # Supporting analyses
├── papers/paper8-kac/ ... paper10-capstone/         # Identifiability theory and synthesis
├── src/analytical/             # Core shell models and coupling calculations
├── tests/                      # Regression suite
└── docs/                       # Research logs, validation plans, and notes
```

The repository also contains the Copilot/agent workflow used to produce the papers, but that infrastructure is only useful insofar as it serves the science.

## Licence

[MIT](LICENSE)



