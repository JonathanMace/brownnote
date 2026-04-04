# Browntone: Vibroacoustics of Fluid-Filled Soft Shells

This repository contains the analytical framework, source code, and manuscript drafts for a research programme investigating the low-frequency vibroacoustics of fluid-filled viscoelastic shells — with applications ranging from abdominal infrasound coupling to non-destructive produce testing and spectral identifiability theory.

The programme is **purely analytical at present**. A phantom validation protocol has been designed but not yet executed; see [docs/](docs/).

## Motivation

The human abdomen possesses a real flexural resonance near 4 Hz. The long-standing conjecture — sometimes called the *brown note* — is that sufficiently intense airborne infrasound could exploit this resonance to induce involuntary gastrointestinal effects. We show that the resonance is genuine but the airborne coupling to it is not: at 120 dB SPL the energy-consistent wall displacement is only 0.028 μm, well below the 0.5–2.0 μm range associated with PIEZO-channel mechanotransduction. Whole-body mechanical vibration, by contrast, couples roughly 3.3 × 10⁴ times more effectively (SDOF upper bound; ~1.6 × 10⁴ with modal participation Γ₂ ≈ 0.48).

The interesting result is not the debunking itself but the asymmetry it reveals — and the observation that the same oblate-spheroidal shell model that explains *why* sound cannot shake your insides also determines *when* a resonance spectrum can or cannot identify the parameters that produced it.

## Principal Papers

### [Paper 1 — The Brown Note](papers/paper1-brown-note/)
*Targeting Journal of Sound and Vibration*

Paper 1 resolves the mechanical-vs-airborne coupling asymmetry from first principles. At the n = 2 flexural resonance, ka ≈ 0.01: the acoustic wavelength dwarfs the body, the impedance mismatch is severe, and the incident field barely drives the mode. Mechanical excitation through the body wall suffers none of these penalties. The conclusion is not that abdominal resonance is fictional; it is that the resonance is real while the airborne path to it is negligible.

### [Paper 7 — Watermelon Rind Stiffness](papers/paper7-watermelon/)
*Targeting Postharvest Biology and Technology*

Paper 7 applies the same shell framework to a problem with clearer practical value: mapping a watermelon's tap-tone frequency to its effective rind stiffness. The claim is deliberately narrow — inference to eating ripeness requires cultivar-specific calibration not yet demonstrated — but the forward model works well enough to make the inverse question unavoidable: under what conditions does a resonance spectrum actually identify the parameters of interest? That question motivates Papers 8–10.

## Supporting Analyses (Papers 2–6)

Papers 2–6 are not independent contributions; they probe the same shell framework across complementary organs, forcing conditions, and physiological scenarios.

| Paper | Focus | Contribution |
|-------|-------|-------------|
| [P2](papers/paper2-gas-pockets/) | Gas pocket transduction | Tissue-constrained bubbles couple far more strongly than the whole cavity |
| [P3](papers/paper3-scaling-laws/) | Cross-species scaling | The low-frequency shell mechanics are not uniquely human |
| [P4](papers/paper4-bladder/) | Bladder resonance | Organ-specific geometry yields a distinct resonance landscape |
| [P5](papers/paper5-borborygmi/) | Borborygmi | Bubble-shell acoustics reproduce clinical stomach-growl frequencies |
| [P6](papers/paper6-sub-bass/) | Sub-bass perception | Structural transmission dominates the airborne path at concert levels |

## Identifiability Theory (Papers 8–10)

The theoretical contribution of the programme rests on four formal results:

1. **Rank deficiency under scalar geometric reduction.** Equivalent-radius formulations reduce the Jacobian's column space and can render spectral inversion structurally ill-posed ([P8](papers/paper8-kac/), targeting a suitable inverse-problems venue).
2. **Identifiability lifting by oblate asphericity.** Breaking spherical symmetry in the oblate direction restores local rank and improves conditioning by ten orders of magnitude ([P8](papers/paper8-kac/)–[P10](papers/paper10-capstone/)).
3. **Near-spherical conditioning asymptotics.** As eccentricity ε → 0, the smallest singular value σ₃ vanishes as λ₁ε² + O(ε⁴); the finite floor reported in earlier Ritz calculations was a discretisation artefact ([P9](papers/paper9-lifting-theorem/)–[P10](papers/paper10-capstone/)).
4. **Forward adequacy does not imply inverse adequacy.** A model can predict resonance frequencies to within 10% yet remain catastrophically ill-conditioned for parameter recovery ([P10](papers/paper10-capstone/)).

[Paper 9](papers/paper9-lifting-theorem/) establishes that comparable prolate perturbations do not produce the same lifting — the mechanism is geometry-selective. [Paper 10](papers/paper10-capstone/) contains the formal proofs for the axisymmetric case; extensions to non-axisymmetric geometries and experimental validation are the principal next steps.

## Selected Quantitative Results

| Quantity | Value | Source |
|----------|-------|--------|
| Flexural frequency f₂ (n = 2) | 3.95 Hz | P1 |
| Breathing mode (n = 0) | ~2490 Hz | P1 |
| Airborne displacement at 120 dB | 0.028 μm | P1 |
| Coupling ratio R (120 dB vs 0.1 m/s², SDOF) | 3.3 × 10⁴ | P1 |
| Sobol sensitivity S_T(E), abdomen | 0.86 | P1 |
| Sobol sensitivity S_T(E_rind), watermelon | 0.54 ± 0.05 | P7 |
| Condition number κ (equivalent sphere) | ~1.37 × 10¹⁰ | P8 |
| Condition number κ (canonical oblate) | 69.4 | P8 |

## Scope and Limitations

- **Analytical, not experimental.** All results derive from shell-theoretic models. A phantom validation protocol exists ([docs/](docs/)) but has not been executed.
- **Rind stiffness, not ripeness.** Paper 7 recovers effective stiffness from tap-tone data; the link to consumer-relevant ripeness requires cultivar calibration not yet performed.
- **Papers 1–9 are submission-ready drafts.** Paper 10 is under active revision.
- **Latest P10 draft:** [draft_2026-04-04_1400.pdf](papers/paper10-capstone/drafts/draft_2026-04-04_1400.pdf)

## Getting Started

```bash
pip install -e .[dev]
python -m pytest tests/ -v
```

```python
from src.analytical.natural_frequency_v2 import AbdominalModelV2, flexural_mode_frequencies_v2
from src.analytical.energy_budget import self_consistent_displacement

model = AbdominalModelV2(
    E=0.1e6, a=0.18, c=0.12, h=0.01, nu=0.45,
    rho_wall=1100, rho_fluid=1020, K_fluid=2.2e9,
    P_iap=1000, loss_tangent=0.25,
)
freqs = flexural_mode_frequencies_v2(model, n_max=5)
disp = self_consistent_displacement(model, mode_n=2, spl_db=120)
```

## Citation

```bibtex
@misc{browntone2026,
  author = {Mace, Jonathan and Mace, Brian R.},
  title  = {Browntone: Vibroacoustics of Fluid-Filled Soft Shells},
  year   = {2026},
  url    = {https://github.com/JonathanMace/brownnote}
}
```

## Repository Layout

```
papers/                          src/analytical/
├── paper1-brown-note/           ├── natural_frequency_v2.py
├── paper2-gas-pockets/          ├── energy_budget.py
├── paper3-scaling-laws/         ├── oblate_spheroid_ritz.py
├── paper4-bladder/              ├── kac_identifiability.py
├── paper5-borborygmi/           ├── universality.py
├── paper6-sub-bass/             └── ...
├── paper7-watermelon/
├── paper8-kac/                  tests/          487 regression tests
├── paper9-lifting-theorem/      docs/           Research logs, protocols
└── paper10-capstone/
```

This work was produced with AI assistance; see [docs/ai-assisted-research.md](docs/ai-assisted-research.md) for methodology and disclosure.

## Licence

[MIT](LICENSE)
