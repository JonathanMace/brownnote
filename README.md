# The Brown Note

It started with a question no self-respecting acoustician would ask in public: *can sound make you soil yourself?*

The answer, it turns out, is almost certainly no. But the reason it's no led us somewhere none of us expected — through shell theory, fluid–structure coupling, spectral inverse problems, and a watermelon — to a general framework for how geometry mediates excitation, resonance, and identifiability in fluid-filled viscoelastic shells.

The brown note was the entry point. Geometry was the destination.

---

## What This Actually Is

**Browntone** is an analytical research programme investigating the vibroacoustics of fluid-filled soft shells. We model organs (and fruit) as viscoelastic oblate spheroids, derive modal spectra from first principles, and study how shape governs everything: which modes respond to forcing, where resonances sit, and whether you can invert the spectrum to recover the parameters that generated it. The shell theory is Love–Kirchhoff with Lamb's (1882) membrane expression for the equivalent sphere, and a Rayleigh–Ritz treatment for the full oblate geometry.

The programme's central thesis: **in fluid-filled viscoelastic shells, geometry does three jobs — it filters external forcing, it organises the modal spectrum, and it determines whether the spectrum can be inverted to recover the parameters that generated it.** Nine papers and a capstone establish this thesis across human organs, animal models, and agricultural products.

Nine papers. Four target journals. One capstone in preparation for *Proceedings of the Royal Society A*. All built by a human PI, an emeritus co-author, and a small bureaucracy of AI agents who take their work far too seriously.

## Papers

### Act I — The Question

| # | Title | Venue | Status | One-Line Result | Draft |
|---|-------|-------|--------|-----------------|-------|
| 1 | **The Brown Note** | *JSV* | Submission-ready (46 pp) | R ≈ 3.3 × 10⁴ — the resonance is real; the acoustic path to it is not | [PDF](papers/paper1-brown-note/drafts/draft_2026-03-30_0339.pdf) |
| 2 | **Gas Pockets** | *JASA* | Submission-ready (16 pp) | Tissue-constrained bubbles couple 35–100× better than the whole cavity | [PDF](papers/paper2-gas-pockets/drafts/draft_2026-03-29_2111.pdf) |

### Act II — The Evidence

| # | Title | Venue | Status | One-Line Result | Draft |
|---|-------|-------|--------|-----------------|-------|
| 3 | **Scaling Laws** | *JSV Short* | Under revision (8 pp) | Π₀ ≈ 0.07 across species — the brown note is not a uniquely human indignity | [PDF](papers/paper3-scaling-laws/drafts/draft_2026-03-29_2120.pdf) |
| 4 | **Bladder Resonance** | *JSV* | Draft complete | f₂ = 13.5 Hz at 222 mL; the U-curve minimum is suspiciously at driving-posture fill | [PDF](papers/paper4-bladder/drafts/draft_2026-03-29_2120.pdf) |
| 5 | **Borborygmi** | *JASA* | Submission-ready | Five mechanisms, 135–440 Hz — your stomach growls in a predictable key | [PDF](papers/paper5-borborygmi/drafts/draft_2026-03-29_2120.pdf) |
| 6 | **Can You Feel the Bass?** | *JASA* | Submission-ready | Airborne sub-bass falls 2.5 orders short; the floor does the work | [PDF](papers/paper6-sub-bass/drafts/draft_2026-03-29_2120.pdf) |

### Act III — The Theory

| # | Title | Venue | Status | One-Line Result | Draft |
|---|-------|-------|--------|-----------------|-------|
| 7 | **Can You Hear the Ripeness?** | *Postharvest B&T* | Submission-ready (32 pp) | Tap-tone inversion maps resonance to rind stiffness — folk wisdom formalised | [PDF](papers/paper7-watermelon/drafts/draft_2026-03-30_0014.pdf) |
| 8 | **Can You Hear the Shape of an Organ?** | *IPSE* | Submission-ready (29 pp) | κ\_sphere ≈ 1.37 × 10¹⁰ → κ\_oblate = 69.4 — geometry rescues identifiability | [PDF](papers/paper8-kac/drafts/draft_2026-03-30_0253.pdf) |
| 9 | **Lifting Theorem** | *JSV Short* | In preparation | Singular-value lifting for symmetry-broken spectral inverse problems | [PDF](papers/paper9-lifting-theorem/drafts/draft_2026-03-29_2301.pdf) |
| 🎓 | **Capstone** | *Proc. R. Soc. A* | Planned | *Geometry mediates excitation, resonance, and identifiability* | — |

See also: [Mid-Tenure Research Statement](docs/mid-tenure-research-statement.pdf)

## The Punchline

The human abdomen has a flexural resonance near 4 Hz, so the folk intuition is not completely mad. But at 120 dB SPL the energy-consistent airborne displacement is only 0.028 μm — roughly 1.5 orders of magnitude below PIEZO mechanotransduction thresholds (0.5–2.0 μm). Whole-body vibration at 0.1 m/s² RMS produces millimetre-scale excitation of the same mode, a coupling ratio R ≈ 3.3 × 10⁴. The "brown note" is a mechanical story misremembered as an acoustic one.

What we didn't expect: the same framework that explains why sound can't shake your insides also explains why you can tap a watermelon to check if it's ripe, why your stomach growls at a predictable frequency, and why geometry — not material properties — determines whether you can invert a resonance spectrum at all. The joke was never the point. Geometry was.

## Key Results

| Quantity | Value |
|----------|-------|
| Flexural frequency f₂ (n = 2) | 3.95 Hz |
| Breathing mode (n = 0) | 2,490 Hz |
| Airborne displacement ξ\_air (120 dB) | 0.028 μm |
| Mechanical displacement ξ\_mech (0.1 m/s², SDOF upper bound) | 917 μm |
| Coupling ratio R (120 dB vs 0.1 m/s², SDOF upper bound) | ≈ 3.3 × 10⁴ |
| Dimensionless frequency Π₀ (cross-species) | 0.07 |
| Sobol total-order S\_T(E) | 0.86 |
| Condition number κ\_sphere | ≈ 1.37 × 10¹⁰ |
| Condition number κ\_oblate (canonical eccentricity) | 69.4 |
| Condition floor κ\_floor (near-sphere limit, ε → 0) | ≈ 269 |
| Scattering parameter ka | 0.0114 |

## The Bigger Picture

Papers 1–6 are evidence. Papers 7–9 and the capstone are synthesis. The programme converges on four conjectures (theorems, once the capstone is written):

1. **Rank-deficiency conjecture.** The equivalent-radius model of a fluid-filled shell is generically ill-conditioned for spectral inversion (κ ∝ 10¹⁰ for the sphere).
2. **Identifiability lifting.** Breaking spherical symmetry — introducing asphericity — lifts the Jacobian rank deficiency because different flexural modes sample curvature differently.
3. **Near-spherical conditioning asymptotics.** As eccentricity ε → 0, the condition number follows κ ~ C·ε⁻² with a finite floor set by the curvature channel.
4. **Forward adequacy ≠ inverse adequacy.** A model that predicts frequencies well (Paper 7's watermelon) may be catastrophically ill-conditioned for parameter recovery (Paper 8's sphere), and vice versa.

A Distinguished Advisory Board review scored the programme 7–8/10 across coherence, depth, breadth, and novelty, with lasting impact at 6/10 — *"could be 8–9 with consolidation."* The capstone, targeting *Proceedings of the Royal Society A*, is that consolidation. Papers 1, 7, and 8 form the backbone; papers 2–6 supply evidence.

## How It Was Made

Built with **GitHub Copilot CLI** and **24 autonomous AI agents** handling analysis, drafting, review, figures, and morale. The tally: **549 commits**, **279 PRs merged**, **487 tests**, **22 reusable skills**, **92 research logs**, ~**30 hours wall-clock**.

The agents include a 3-reviewer panel, a journal editor, a simulation engineer, a data analyst, a provocateur, a bibliographer, a pop-culture verifier, a coffee-machine guru (emeritus professor who tells you to submit the damn paper already), and a loving spouse (who suggests you talk to Dietrich). Research runs on an academic calendar — one semester per wall-clock hour, with breaks for reflection and occasionally [whisky reviews](docs/whisky/).

See [docs/ai-assisted-research.md](docs/ai-assisted-research.md) for the methodology.

## For Researchers

The core framework models a fluid-filled viscoelastic oblate spheroid using Love–Kirchhoff shell theory with a volume-preserving equivalent radius R\_eq = (a²c)^{1/3}. Flexural modes (n ≥ 2) are the physically relevant modes at infrasonic frequencies; the breathing mode (n = 0, ~2490 Hz) is dominated by the fluid bulk modulus and is irrelevant to low-frequency coupling. Damping is Kelvin–Voigt with a single relaxation time (loss tangent η = 0.25). For identifiability analysis (Papers 7–8), the full oblate Ritz model replaces the equivalent-sphere approximation, and it is precisely the asphericity that breaks the Jacobian degeneracy and rescues parameter recovery.

**Key cross-disciplinary connections:** The three-class identifiability taxonomy (singular / regular bounded / non-lifting) from Paper 8 applies to any spectral inverse problem on shells where symmetry breaking lifts rank deficiency. Researchers in structural health monitoring, clinical elastography, or postharvest quality assessment may find the curvature–mode anti-correlation mechanism relevant to their own geometries.

**Experimental validation:** A phantom validation protocol using silicone oblate shells with laser Doppler vibrometry has been designed ([docs/](docs/)) but not yet executed. The programme is purely analytical at present.

**How to cite:** Individual papers should be cited by their arXiv or journal references when available. For the programme as a whole:

```bibtex
@misc{browntone2026,
  author = {Mace, Jonathan and Mace, Brian R.},
  title  = {Browntone: Vibroacoustics of Fluid-Filled Soft Shells},
  year   = {2026},
  url    = {https://github.com/JonathanMace/brownnote}
}
```

## Quick Start

```bash
pip install -e .[dev]
python -m pytest tests/ -v
```

```python
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2, flexural_mode_frequencies_v2,
)
from src.analytical.energy_budget import self_consistent_displacement
from src.analytical.mechanical_coupling import compare_airborne_vs_mechanical

model = AbdominalModelV2(
    E=0.1e6, a=0.18, c=0.12, h=0.01, nu=0.45,
    rho_wall=1100, rho_fluid=1020, K_fluid=2.2e9,
    P_iap=1000, loss_tangent=0.25,
)

freqs = flexural_mode_frequencies_v2(model, n_max=5)   # modal spectrum
disp = self_consistent_displacement(model, mode_n=2, spl_db=120)  # 0.028 μm
ratio = compare_airborne_vs_mechanical(model)           # ≈ 3.3×10⁴
```

If you only want one number, ask for the n = 2 flexural mode. If you want the whole joke explained properly, read Paper 1.

## Repository Structure

```text
browntone/
├── papers/
│   ├── paper1-brown-note/       # The one that started it all
│   ├── paper2-gas-pockets/      # The bubble detour
│   ├── paper3-scaling-laws/     # Do rats resonate too?
│   ├── paper4-bladder/          # The motorway problem
│   ├── paper5-borborygmi/       # Why stomachs growl
│   ├── paper6-sub-bass/         # Can you feel the bass?
│   ├── paper7-watermelon/       # The fruit that brought it together
│   ├── paper8-kac/              # Can you hear the shape of an organ?
│   └── paper9-lifting-theorem/  # The theorem underneath
├── src/analytical/              # Core analytical models
├── tests/                       # 487 regression tests
├── docs/research-logs/          # 92 quantitative session logs
└── .github/                     # 24 agents, 22 skills, workflows
```

## Tests

```bash
python -m pytest tests/ -v   # 487 tests
```

## Authors

| Who | Role |
|-----|------|
| **Jonathan Mace** | Lead author, concept, supervision |
| **Brian R. Mace** | Vibroacoustics theory, co-supervision |
| **GitHub Copilot CLI (Opus)** | Analysis, drafting, review, code |
| **Springbank 10 Year Old** | Moral support, strategic clarity |

## Licence

[MIT](LICENSE)
