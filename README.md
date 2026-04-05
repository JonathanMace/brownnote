# Browntone

The *brown note* is one of the more durable pieces of acoustic folklore: an infrasonic tone supposedly capable of inducing involuntary loss of bowel control. The story turns up in urban legends, military apocrypha, and popular culture, including *South Park* (“World Wide Recorder Concert”, also known as “The Brown Noise”, S3E17, 2000). It has never been demonstrated experimentally.

We took the claim seriously enough to ask the more interesting question. If the abdomen really does possess a low-frequency resonance, can airborne sound excite it strongly enough to matter? This repository contains the analytical framework, code, and manuscript drafts for the research programme that grew from that problem: first a debunking, then a broader theory of resonance, geometry, and inverse identifiability in fluid-filled soft shells.

## The Question

The human abdomen does possess a genuine flexural resonance near 4 Hz, well inside the infrasonic range. Whole-body vibration in this band has long been associated with gastrointestinal discomfort. The folklore question is therefore not absurd in outline; it is simply wrong in mechanism. Can *airborne* sound exploit the same mode?

Paper 1 shows that it cannot. At the canonical *n* = 2 flexural mode, the acoustic wavelength is vastly larger than the body (*ka* ≈ 0.011), the air–tissue impedance mismatch is severe, and the modal coupling is correspondingly feeble. Mechanical excitation through the seat, floor, or body wall is orders of magnitude more effective. The resonance is real; the loudspeaker pathway to it is negligible.

That much is [Paper 1](papers/paper1-brown-note/) ([PDF](papers/paper1-brown-note/drafts/draft_2026-04-03_2000.pdf)).

## Where It Leads

What began as a debunking exercise quickly became a more general inverse-problem question: when a resonance spectrum moves, when does it actually identify the parameter that moved? The same oblate-spheroidal shell framework that answers the folklore question also exposes that harder problem.

That is where [Paper 7](papers/paper7-watermelon/) ([PDF](papers/paper7-watermelon/drafts/draft_2026-03-31_0939.pdf)) enters. People tap watermelons and listen for a deep thump; the practice is old, widespread, and only intermittently reliable. Paper 7 turns that bit of market folklore into a clean modelling problem: a fluid-filled spheroidal shell whose tap-tone frequency tracks effective rind stiffness. The forward model is useful. The inverse question — can stiffness be recovered from the spectrum, rather than merely correlated with it? — is the real prize.

[Papers 8–10](papers/paper8-kac/) take up that question directly. They show that an equivalent-sphere reduction can reproduce the lowest flexural frequencies to within about 10% and still be a poor inverse model. Oblate geometry restores the missing information; prolate geometry does not do so in the same way; and the exact sphere is a singular point of the inverse problem. The forward problem and the inverse problem are not the same problem, however similar their spectra may look.

### [Paper 10](papers/paper10-capstone/) — the capstone

Paper 10 gives the programme its theoretical centre of gravity. Targeting *Proceedings of the Royal Society A*, it makes the central point explicit: a forward model may be accurate enough for prediction and still be unusable for parameter recovery. The paper consolidates the rank-collapse result for the spherical reduction, the oblate lifting result, the corrected near-spherical asymptotics from Kato perturbation theory, and the formal separation between forward adequacy and inverse adequacy. It also shows that the lifting survives parameter sweeps and measured-mode variations rather than depending on one convenient canonical point. The broader claim is sober but important: whenever resonance data are used to infer hidden parameters, geometry decides which inferences are defensible.

**Latest draft:** [papers/paper10-capstone/drafts/draft_2026-04-04_1740.pdf](papers/paper10-capstone/drafts/draft_2026-04-04_1740.pdf)

## Supporting Papers

Papers 2–6 stress-test the same shell framework across neighbouring organs and forcing pathways. They are not side quests; each isolates a mechanism that matters somewhere in the programme.

| Paper | What it examines |
|-------|-----------------|
| [P2](papers/paper2-gas-pockets/) ([PDF](papers/paper2-gas-pockets/drafts/draft_2026-03-30_2332.pdf)) | Gas pockets — tissue-constrained bubbles couple far more effectively than the whole cavity |
| [P3](papers/paper3-scaling-laws/) ([PDF](papers/paper3-scaling-laws/drafts/draft_2026-03-30_2332.pdf)) | Cross-species scaling — the low-frequency mechanics are not uniquely human |
| [P4](papers/paper4-bladder/) ([PDF](papers/paper4-bladder/drafts/draft_2026-03-30_2332.pdf)) | Bladder resonance — organ-specific geometry yields a distinct modal landscape |
| [P5](papers/paper5-borborygmi/) ([PDF](papers/paper5-borborygmi/drafts/draft_2026-03-31_1006.pdf)) | Borborygmi — constrained-bubble acoustics reproduce clinical gut-sound frequencies |
| [P6](papers/paper6-sub-bass/) ([PDF](papers/paper6-sub-bass/drafts/draft_2026-03-30_2332.pdf)) | Sub-bass coupling — at concert levels, the floor matters more than the air |

[Paper 8](papers/paper8-kac/) ([PDF](papers/paper8-kac/drafts/draft_2026-03-31_0854.pdf)) and [Paper 9](papers/paper9-lifting-theorem/) ([PDF](papers/paper9-lifting-theorem/drafts/draft_2026-04-02_2301.pdf)) supply the theory that Paper 10 consolidates: rank deficiency in equivalent-radius models, identifiability lifting in oblate shells, and the oblate–prolate asymmetry.

## Scope and Limitations

This is an analytical programme. The results come from shell-theoretic models, not from completed benchtop validation, although an experimental phantom protocol has been designed (see [docs/](docs/)). Paper 7 recovers rind stiffness, not eating quality; that consumer-facing step still requires cultivar-specific calibration. Papers 1–9 are submission-ready drafts. Paper 10 is the capstone currently under final review.

## Getting Started

```bash
pip install -e .[dev]
python -m pytest tests/ -v          # 487 regression tests
```

If you want the scientific story, start with the papers. If you want the working implementation behind them, start with `src/analytical/natural_frequency_v2.py` for the canonical abdominal model, `src/analytical/energy_budget.py` for the airborne-coupling analysis, and `src/analytical/kac_identifiability.py` for the inverse-problem machinery.

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
