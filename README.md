# The Brown Note

Can sound make you soil yourself? No — but the reason why leads somewhere unexpected.

The abdomen does have a real low-frequency flexural resonance near 4 Hz. The problem for the "brown note" is not resonance; it is coupling. Airborne sound couples so weakly to that mode that the story collapses as acoustics and becomes more interesting as shell mechanics, vibration, and inverse theory.

The same shell model that explains why sound can't shake your insides also explains when you can (and can't) invert a resonance spectrum to recover the parameters that generated it.

## The Short Version

At 120 dB SPL, the energy-consistent airborne displacement of the abdominal wall is only 0.028 μm. That is well below the roughly 1-2 μm PIEZO mechanotransduction range. The resonance is real; the airborne path to it is not.

The transfer-function ratio makes the same point more formally: H_mech/H_air ≈ 6.5 × 10^6. Paper 1 is the definitive physics-based debunking. Paper 7 shows why the framework survived the debunking: the same shell mechanics can formalise the watermelon thump test as a rind-stiffness problem rather than folklore.

## If You Read Two Papers

If you read only one paper, read Paper 1. If you want to know why the framework is useful beyond the joke, read Paper 7.

### [Paper 1: The Brown Note](papers/paper1-brown-note/) — *Journal of Sound and Vibration*

This is the paper that answers the question. It starts from a simple empirical asymmetry: whole-body vibration in the 4-8 Hz range can produce gastrointestinal effects, while airborne sound at the same frequencies does not. The model explains that asymmetry from first principles.

At the n = 2 flexural resonance, ka is only about 0.01. The wavelength is enormous compared with the body, the air-tissue mismatch is severe, and the incident acoustic field barely drives the mode at all. Mechanical excitation transmitted through the body wall does not suffer those penalties.

The conclusion is deliberately unglamorous and therefore trustworthy: there is a genuine abdominal resonance near 4 Hz, but the "brown note" is a mechanical story misremembered as an acoustic one.

### [Paper 7: The Watermelon Thump Test](papers/paper7-watermelon/) — *Postharvest Biology and Technology*

This is the unexpected application. People really do tap watermelons and listen for a deep, resonant thump, but the practice has mostly lived as anecdote and market lore. Paper 7 turns that intuition into a quantitative shell model linking tap-tone frequency to effective rind stiffness.

The claim is intentionally narrower than "ripeness prediction". The model supports stiffness and firmness inference, not validated eating-ripeness prediction, and the step from firmness to consumer ripeness still needs cultivar-specific calibration. What the paper does show is that the shell framework can formalise a practical nondestructive measurement problem.

## Supporting Analyses

Papers 2-6 are supporting analyses, not five unrelated grand claims. They test the same framework across related organs, forcing conditions, and physiological scenarios.

| Paper | Focus | What it adds |
|---|---|---|
| [P2 Gas Pockets](papers/paper2-gas-pockets/) | Local gas inclusions | Tissue-constrained bubbles can couple much more strongly than the whole abdominal cavity. |
| [P3 Scaling Laws](papers/paper3-scaling-laws/) | Cross-species scaling | The low-frequency shell mechanics are not uniquely human. |
| [P4 Bladder Resonance](papers/paper4-bladder/) | Organ-specific variation | The same framework predicts a different resonance landscape for the bladder. |
| [P5 Borborygmi](papers/paper5-borborygmi/) | Gut sounds | Bubble-shell acoustics can account for clinically realistic stomach-growl frequencies. |
| [P6 Sub-Bass Coupling](papers/paper6-sub-bass/) | Airborne vs structural bass | Reinforces that the floor and seat matter far more than the air. |

## The Mathematics

The later papers ask a harder question than "what resonates?": can you work backwards from a spectrum to the parameters that produced it?

| Paper | Role |
|---|---|
| [P8 Kac Identifiability](papers/paper8-kac/) | Shows that the equivalent-sphere inverse problem is catastrophically ill-conditioned, and that oblate geometry can rescue identifiability. |
| [P9 Lifting Theorem](papers/paper9-lifting-theorem/) | Sharpens the result: not all symmetry breaking helps equally; oblate shells lift the degeneracy, prolate shells do not. |
| [P10 Capstone](papers/paper10-capstone/) | Intended synthesis of excitation, resonance, and identifiability across the programme; the synthesis is still in progress. |

P8-P9 contain the current mathematical backbone. P10 is the synthesis in progress.

## Key Results

| Quantity | Value |
|----------|-------|
| Flexural frequency f₂ (n = 2) | 3.95 Hz |
| Breathing mode (n = 0) | 2490 Hz |
| Airborne displacement ξ_air at 120 dB | 0.028 μm |
| PIEZO threshold range | 1-2 μm |
| Transfer-function ratio H_mech/H_air | ≈ 6.5 × 10^6 |
| Mechanical displacement ξ_mech at 0.1 m/s² RMS (SDOF upper bound) | 917 μm |
| Coupling ratio R (120 dB vs 0.1 m/s², SDOF upper bound) | ≈ 3.3 × 10^4 |
| Dimensionless frequency Π₀ (cross-species) | 0.07 |
| Watermelon Sobol total-order sensitivity S_T(E) (P7) | 0.86 |
| Condition number κ_sphere | ≈ 1.37 × 10^10 |
| Condition number κ_oblate | 69.4 |
| Scattering parameter ka | 0.0114 |

## What This Repo Is and Isn't

- **An analytical programme, not an experimental one.** The papers and code are modelling work; an experimental validation protocol exists, but it has not yet been executed.
- **A rind-stiffness framework, not a magic ripeness oracle.** The watermelon application supports firmness-related stiffness inference; cultivar-specific calibration is still needed for ripeness claims.
- **A mostly finished arc, not a closed book.** P1-P9 contain the current core results; P10 is the synthesis still being written.

## For Researchers

The core model treats the abdomen as a fluid-filled viscoelastic oblate spheroidal shell. In the forward problem, an equivalent-radius formulation captures the dominant low-frequency behaviour. In the inverse problem, the full oblate geometry matters because asphericity is exactly what breaks the spectral degeneracy. Flexural modes (n ≥ 2) govern the infrasonic response; the breathing mode (n = 0) sits around 2490 Hz and is not the low-frequency story.

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
├── papers/
│   ├── paper1-brown-note/       # Definitive debunking
│   ├── paper2-gas-pockets/      # Supporting analysis
│   ├── paper3-scaling-laws/     # Supporting analysis
│   ├── paper4-bladder/          # Supporting analysis
│   ├── paper5-borborygmi/       # Supporting analysis
│   ├── paper6-sub-bass/         # Supporting analysis
│   ├── paper7-watermelon/       # Watermelon thump-test / rind-stiffness application
│   ├── paper8-kac/              # Identifiability theory
│   ├── paper9-lifting-theorem/  # Oblate-prolate asymmetry
│   └── paper10-capstone/        # Synthesis in progress
├── src/analytical/              # Core shell models and coupling calculations
├── tests/                       # Regression suite
└── docs/                        # Research logs, validation plans, and notes
```

The repository also contains the Copilot workflow used to produce the papers, but that infrastructure matters only insofar as it serves the science.

## Licence

[MIT](LICENSE)
