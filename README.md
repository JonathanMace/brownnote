# Browntone: Vibroacoustics of Fluid-Filled Soft Shells

This repository contains the analytical framework, source code, and manuscript drafts for a research programme on the low-frequency vibroacoustics of fluid-filled viscoelastic shells. Its central claim is that the same shell model can explain both why some resonances are physically real yet negligibly excited by airborne sound, and when resonance spectra can or cannot identify the parameters that produced them. The questions matter in structural acoustics, biomechanics, inverse problems, and non-destructive sensing.

## Motivation

The human abdomen possesses a genuine flexural resonance near 4 Hz. A long-standing conjecture, later dubbed the *brown note*, asks whether sufficiently intense airborne infrasound could exploit that resonance to induce involuntary gastrointestinal effects. We show that the resonance is real but the airborne path to it is negligible: at 120 dB SPL the energy-consistent wall displacement is only 0.028 μm, well below the 0.5–2.0 μm range associated with PIEZO-channel mechanotransduction. Under the reference comparison used in Paper 1, whole-body vibration at 0.1 m/s² couples about 3.3 × 10⁴ times more strongly in an SDOF upper bound, or about 1.6 × 10⁴ times more strongly after modal participation correction (Γ₂ ≈ 0.48).

That asymmetry is the organising result of the programme. A model that captures the forward resonance physics also shows when inverse recovery is informative, when it is fragile, and when geometric simplification destroys identifiability altogether.

## Principal Papers

### [Paper 1 — The Brown Note](papers/paper1-brown-note/)
*Prepared for submission to Journal of Sound and Vibration*

Paper 1 establishes the airborne-versus-mechanical coupling asymmetry from first principles. At the n = 2 flexural resonance, ka ≈ 0.0114: the acoustic wavelength dwarfs the body, impedance mismatch dominates, and the incident field barely drives the mode. Mechanical excitation through the body wall suffers none of these penalties. The resonance is real; the airborne route to it is not a plausible physiological driver.

### [Paper 7 — Watermelon Rind Stiffness](papers/paper7-watermelon/)
*Prepared for submission to Postharvest Biology and Technology*

Paper 7 applies the same framework to a cleaner inverse problem: mapping a watermelon's tap-tone spectrum to effective rind stiffness. The claim remains deliberately narrow — stiffness, not eating ripeness — but the practical question is real, and the model makes the inverse question unavoidable: under what conditions does a resonance spectrum identify the parameters of interest? That question motivates Papers 8–10.

## Supporting

Supporting investigations test the same shell framework across complementary organs, forcing conditions, and physiological scenarios.

| Paper | Focus | Contribution |
|-------|-------|-------------|
| [P2](papers/paper2-gas-pockets/) | Gas pocket transduction | Tissue-constrained bubbles couple far more strongly than the whole cavity |
| [P3](papers/paper3-scaling-laws/) | Cross-species scaling | The low-frequency shell mechanics are not uniquely human |
| [P4](papers/paper4-bladder/) | Bladder resonance | Organ-specific geometry yields a distinct resonance landscape |
| [P5](papers/paper5-borborygmi/) | Borborygmi | Bubble-shell acoustics reproduce clinical stomach-growl frequencies |
| [P6](papers/paper6-sub-bass/) | Sub-bass perception | Structural transmission dominates the airborne path at concert levels |

## Theory

The deeper theoretical result is that good forward predictions do not guarantee useful inverse inference. When geometry is reduced too aggressively, resonance spectra lose parameter information; mild oblate asphericity can restore it.

1. **Rank deficiency under scalar geometric reduction.** Equivalent-radius formulations collapse the Jacobian's effective column space and can make spectral inversion structurally ill-posed ([P8](papers/paper8-kac/)).
2. **Identifiability lifting by oblate asphericity.** Breaking spherical symmetry in the oblate direction restores local rank and improves conditioning by approximately eight orders of magnitude in the canonical comparison ([P8](papers/paper8-kac/)–[P10](papers/paper10-capstone/)).
3. **Near-spherical conditioning asymptotics.** As eccentricity ε → 0, the smallest singular value σ₃ vanishes as λ₁ε² + O(ε⁴); the apparent finite floor in earlier Ritz calculations was a discretisation artefact ([P9](papers/paper9-lifting-theorem/)–[P10](papers/paper10-capstone/)).
4. **Forward adequacy does not imply inverse adequacy.** A model can predict resonance frequencies to within 10% yet remain catastrophically ill-conditioned for parameter recovery ([P10](papers/paper10-capstone/)).

[Paper 9](papers/paper9-lifting-theorem/) shows that comparable prolate perturbations do not produce the same lifting. [Paper 10](papers/paper10-capstone/) gives the formal axisymmetric proofs and frames the remaining questions for non-axisymmetric geometries and experiment.

## Results

The quantitative picture is simple: the flexural mode lies in the infrasonic band, the breathing mode does not; airborne forcing is vanishingly weak; and geometric fidelity transforms inverse conditioning.

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
- **Programme status.** The repository contains ten manuscript tracks spanning applied vibroacoustics, supporting analyses, and inverse-theory papers.
- **Current P10 drafts.** [papers/paper10-capstone/drafts/](papers/paper10-capstone/drafts/)

## Code

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

Core analytical modules live in `src/analytical/`; manuscript sources live under `papers/`; `tests/` contains the regression suite; and `docs/` collects research logs, protocols, and methodology notes, including the AI-assistance disclosure.

## Citation

```bibtex
@misc{browntone2026,
  author = {Mace, Jonathan and Mace, Brian R.},
  title  = {Browntone: Vibroacoustics of Fluid-Filled Soft Shells},
  year   = {2026},
  url    = {https://github.com/JonathanMace/brownnote}
}
```

This work was produced through an explicitly documented AI-assisted workflow; see [docs/ai-assisted-research.md](docs/ai-assisted-research.md) for the methodology, review process, and disclosure.

## Licence

[MIT](LICENSE)
