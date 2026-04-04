# The Brown Note

Can airborne sound make you soil yourself? No — and the mechanical-vs-airborne asymmetry is the interesting part.

The abdomen does have a real low-frequency flexural resonance near 4 Hz. The problem for the "brown note" is not resonance; it is coupling. The airborne path couples so weakly to that mode that the real story is the asymmetry between airborne forcing and mechanical vibration — and that turns out to be a useful problem in shell mechanics, vibration, and inverse theory.

**Purely analytical at present.** A phantom validation protocol has been designed but not yet executed; see [docs/](docs/).

The same shell model that explains why sound cannot shake your insides also explains when you can, and cannot, invert a resonance spectrum to recover the parameters that generated it.

## The Short Version

At 120 dB SPL, the energy-consistent airborne displacement of the whole abdominal wall is only 0.028 μm. That sits below the 0.5-2.0 μm cellular activation range usually associated with PIEZO mechanotransduction. The resonance is real; the whole-abdomen airborne coupling to it is not.

A second way to say the same thing is that H_mech/H_air ≈ 6.5 × 10^6. Paper 1 resolves the mechanical-vs-airborne asymmetry for whole-abdomen coupling, while Paper 2 shows that localised gas pockets are the notable exception.

Paper 7 is a restricted scalar inversion that estimates effective rind stiffness from a watermelon tap tone. That forward problem is exactly what motivates the broader identifiability question taken up in Papers 8-10.

## If You Read Two Papers

If you read only one paper, read Paper 1. If you want to see why the framework is useful beyond the original question, read Paper 7.

### [Paper 1: The Brown Note](papers/paper1-brown-note/) — targeting *Journal of Sound and Vibration*

This is the paper that answers the question. It starts from a simple empirical asymmetry: whole-body vibration in the 4-8 Hz range can produce gastrointestinal effects, while airborne sound at the same frequencies does not. The model explains that asymmetry from first principles.

At the n = 2 flexural resonance, ka is only about 0.01. The wavelength is enormous compared with the body, the air-tissue mismatch is severe, and the incident acoustic field barely drives the mode at all. Mechanical excitation transmitted through the body wall does not suffer those penalties. The result is not that abdominal resonance is fictional; it is that the resonance is real while the airborne coupling is not.

### [Paper 7: The Watermelon Thump Test](papers/paper7-watermelon/) — targeting *Postharvest Biology and Technology*

This is the unexpected bridge paper. People really do tap watermelons and listen for a deep, resonant thump, but the practice has mostly lived as anecdote and market lore. Paper 7 turns that intuition into a quantitative shell model that maps tap-tone frequency to effective rind stiffness.

That is a narrower claim than "ripeness prediction". Inference to eating ripeness requires cultivar-specific calibration not yet demonstrated. What Paper 7 contributes is a forward model that works well enough to make the inverse question unavoidable: when does a resonance spectrum actually identify the parameters you care about?

## Supporting Analyses

Papers 2-6 are supporting analyses, not five unrelated grand claims. They test the same framework across related organs, forcing conditions, and physiological scenarios.

| Paper | Focus | What it adds |
|---|---|---|
| [P2 Gas Pockets](papers/paper2-gas-pockets/) | Local gas inclusions | Tissue-constrained bubbles can couple much more strongly than the whole abdominal cavity. |
| [P3 Scaling Laws](papers/paper3-scaling-laws/) | Cross-species scaling | The low-frequency shell mechanics are not uniquely human. |
| [P4 Bladder Resonance](papers/paper4-bladder/) | Organ-specific variation | The same framework predicts a different resonance landscape for the bladder. |
| [P5 Borborygmi](papers/paper5-borborygmi/) | Gut sounds | Bubble-shell acoustics can account for clinically realistic stomach-growl frequencies. |
| [P6 Sub-Bass Coupling](papers/paper6-sub-bass/) | Airborne vs structural bass | Reinforces that the floor and seat matter far more than the air. |

## Formal Results

The theoretical spine of the programme is compact enough to state plainly:

1. **Rank deficiency of equivalent-radius models.** Sphere-like equivalent-radius formulations are badly ill-conditioned for spectral inversion (P8, targeting a suitable inverse-problems venue).
2. **Identifiability lifting by oblate asphericity.** Breaking spherical symmetry in the oblate direction lifts identifiability and improves conditioning (P8-P10).
3. **Near-spherical conditioning asymptotics.** As spherical symmetry is restored, conditioning worsens sharply; the apparent finite floor in earlier low-order Ritz calculations was a discretisation artefact, and the correct limit is κ → ∞ as ε → 0 (P9-P10).
4. **Forward adequacy ≠ inverse adequacy.** A model can predict resonance frequencies well and still fail as a parameter-identification tool; P7 is the motivating example, P8-P10 make the point formal.

P9 adds the cross-check that comparable prolate perturbations do not produce the same lifting. P10 currently contains the formal results for the axisymmetric case; extension to non-axisymmetric geometries and experimental validation are the next steps.

## Key Results

| Quantity | Value | Paper |
|----------|-------|-------|
| Flexural frequency f₂ (n = 2) | 3.95 Hz | P1 |
| Breathing mode (n = 0) | 2490 Hz | P1 |
| Airborne displacement ξ_air at 120 dB | 0.028 μm | P1 |
| PIEZO cellular activation range | 0.5-2.0 μm | P1 |
| Transfer-function ratio H_mech/H_air | ≈ 6.5 × 10^6 | P1 |
| Mechanical displacement ξ_mech at 0.1 m/s² RMS (SDOF upper bound) | 917 μm | P1 |
| Coupling ratio R (120 dB vs 0.1 m/s², SDOF upper bound) | ≈ 3.3 × 10^4 (≈ 1.6 × 10^4 with Γ₂ ≈ 0.48) | P1 |
| Abdominal Sobol total-order sensitivity S_T(E) | 0.86 | P1 |
| Dimensionless frequency Π₀ (cross-species) | 0.07 | P3 |
| Watermelon Sobol total-order sensitivity S_T(E_rind) | 0.54 ± 0.05 | P7 |
| Condition number κ_sphere | ≈ 1.37 × 10^10 | P8 |
| Condition number κ_oblate | 69.4 | P8 |
| Scattering parameter ka | 0.0114 | P1 |

## What This Repo Is and Isn't

- **An analytical programme, not an experimental one.** The papers and code are modelling work; an experimental validation protocol exists, but it has not yet been executed.
- **A rind-stiffness framework, not a ripeness oracle.** Paper 7 maps tap-tone frequency to effective rind stiffness; inference to eating ripeness requires cultivar-specific calibration not yet demonstrated.
- **A mostly finished arc, not a closed book.** Papers 1-9 contain the current core results. Paper 10 is the synthesis still being refined.

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
│   ├── paper1-brown-note/       # Resolves the mechanical-vs-airborne asymmetry
│   ├── paper2-gas-pockets/      # Supporting analysis
│   ├── paper3-scaling-laws/     # Supporting analysis
│   ├── paper4-bladder/          # Supporting analysis
│   ├── paper5-borborygmi/       # Supporting analysis
│   ├── paper6-sub-bass/         # Supporting analysis
│   ├── paper7-watermelon/       # The thump-test application
│   ├── paper8-kac/              # Identifiability theory
│   ├── paper9-lifting-theorem/  # Oblate-prolate asymmetry
│   └── paper10-capstone/        # Axisymmetric synthesis, extensions next
├── src/analytical/              # Core shell models and coupling calculations
├── tests/                       # Regression suite
└── docs/                        # Research logs, validation plans, and notes
```

This work was produced with AI assistance; for methodology and disclosure details, see [docs/ai-assisted-research.md](docs/ai-assisted-research.md).

## Licence

[MIT](LICENSE)

