# Browntone

There is a persistent piece of acoustic folklore — sometimes called the *brown note* — which holds that a sufficiently powerful infrasonic tone can induce involuntary loss of bowel control. The idea surfaces reliably in urban legend compilations, military apocrypha, and at least one memorable episode of *South Park* (Parker and Stone, "The Brown Noise," S3E17, 1999). It has never been demonstrated experimentally. Nobody, to our knowledge, has previously bothered to work out *why* it does not work.

This repository contains the analytical framework, code, and manuscript drafts for a research programme that began by taking the question seriously and ended up somewhere rather more interesting.

## The Question

The human abdomen does possess a real flexural resonance near 4 Hz — firmly in the infrasonic range. Whole-body vibration at these frequencies is known to produce gastrointestinal discomfort; military and occupational health literatures have documented this for decades. The brown note conjecture simply asks: can *airborne* sound at the same frequency exploit the same resonance?

The answer, it turns out, is no, and the reason is instructive. At the n = 2 flexural mode, the acoustic wavelength exceeds the body by two orders of magnitude (ka ≈ 0.01), the air–tissue impedance mismatch is enormous, and the incident pressure field barely couples to the mode shape at all. Mechanical excitation through the body wall suffers none of these penalties. The coupling asymmetry exceeds 10⁴. The resonance is genuine; the airborne path to it is negligible.

That much is [Paper 1](papers/paper1-brown-note/).

## Where It Leads

A model that can explain why something *doesn't* happen is only modestly interesting. What made the project worth continuing was the realisation that the same oblate-spheroidal shell framework — built to model the abdomen — raises a question that is considerably harder than the one we started with.

People tap watermelons in the supermarket and listen for a deep thump. This is real folk acoustics, practised worldwide, and it works about as well as you would expect an untrained ear and an uncontrolled impact to work. [Paper 7](papers/paper7-watermelon/) formalises the practice: a fluid-filled spheroidal shell model maps tap-tone frequency to effective rind stiffness. The forward model is straightforward. The inverse question — *can you actually recover the stiffness from the spectrum?* — is not, and its answer depends on the geometry in a way that is not obvious.

That question is the subject of [Papers 8–10](papers/paper8-kac/). When does a resonance spectrum identify the parameters that produced it? When does it fail? The answer, briefly: an equivalent-sphere model can predict frequencies to within 10% and yet be catastrophically ill-conditioned for parameter recovery. Oblate asphericity is precisely what restores identifiability — and prolate asphericity does not. The mechanism is geometry-selective, and the gap between the two cases spans ten orders of magnitude in conditioning.

### [Paper 10](papers/paper10-capstone/) — the capstone

Paper 10, targeting *Proceedings of the Royal Society A*, consolidates the formal results: a rank-collapse theorem for the spherical case, a lifting proposition for the oblate case, near-spherical asymptotics via Kato perturbation theory, and a forward-vs-inverse adequacy result showing that predictive accuracy does not imply invertibility. It includes a sensitivity study across stiffness, aspect ratio, mode count, and basis size, demonstrating that the identifiability lifting is robust rather than parameter-specific. The discussion argues that the same forward ≠ inverse gap arises wherever resonance data are used for parameter recovery — in structural health monitoring, elastography, geophysics, and agricultural acoustics alike.

**Latest draft:** [papers/paper10-capstone/drafts/draft_2026-04-04_1712.pdf](papers/paper10-capstone/drafts/draft_2026-04-04_1712.pdf)

## The Supporting Cast

Papers 2–6 explore the same shell framework across complementary organs and forcing conditions. They are supporting analyses rather than standalone contributions, but each tests a distinct aspect of the model.

| Paper | What it examines |
|-------|-----------------|
| [P2](papers/paper2-gas-pockets/) | Gas pockets — tissue-constrained bubbles couple far more effectively than the whole cavity |
| [P3](papers/paper3-scaling-laws/) | Cross-species scaling — the low-frequency mechanics are not uniquely human |
| [P4](papers/paper4-bladder/) | Bladder resonance — organ-specific geometry yields a distinct modal landscape |
| [P5](papers/paper5-borborygmi/) | Borborygmi — constrained-bubble acoustics reproduce clinical gut-sound frequencies |
| [P6](papers/paper6-sub-bass/) | Sub-bass coupling — at concert levels, the floor matters more than the air |

[Paper 8](papers/paper8-kac/) and [Paper 9](papers/paper9-lifting-theorem/) develop the identifiability theory that Paper 10 consolidates: rank deficiency of equivalent-radius models, the oblate lifting mechanism, and the oblate–prolate asymmetry.

## Scope and Limitations

This is an analytical programme. All results derive from shell-theoretic models; an experimental phantom-validation protocol has been designed but not yet executed (see [docs/](docs/)). Paper 7 recovers rind stiffness, not eating ripeness — the link to consumer-relevant quality requires cultivar-specific calibration not yet performed. Papers 1–9 are submission-ready drafts; Paper 10 is under final review.

## Getting Started

```bash
pip install -e .[dev]
python -m pytest tests/ -v          # 487 regression tests
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

This work was produced with AI assistance; see [docs/ai-assisted-research.md](docs/ai-assisted-research.md) for full methodology and disclosure.

## Licence

[MIT](LICENSE)

