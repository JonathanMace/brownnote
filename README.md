# Browntone

Browntone investigates whether infrasound can induce resonance in the human abdominal cavity — the so-called “brown note” hypothesis. We model the abdomen as a fluid-filled viscoelastic oblate spheroidal shell and compare airborne acoustic coupling with whole-body mechanical vibration. The flexural mode sits comfortably in the infrasonic band; the airborne forcing does not come close to driving it meaningfully. Five connected papers, a validated analytical codebase, and a comprehensive parameter study explore why.

## Papers

### Paper 1 — *The Brown Note*
**Modal analysis of a fluid-filled viscoelastic oblate spheroidal shell**  
**Status:** Submission-ready (~44 pages, 52 references)  
**Target venue:** *Journal of Sound and Vibration*  
**Latest draft:** [PDF](paper/drafts/draft_2026-03-27_1455.pdf)  
**Key result:** coupling ratio R ≈ 6.6 × 10⁴

This is the main paper: the abdomen model, the modal analysis, the coupling estimates, and the central negative result. The flexural mode does sit in the infrasonic band; the airborne forcing does not come close to driving it meaningfully.

### Paper 2 — *Gas Pockets*
**Gas pocket resonance as an alternative acoustic coupling mechanism**  
**Status:** Submission-ready (~16 pages)  
**Target venue:** *JASA Express Letters*  
**Latest draft:** [PDF](paper2-gas-pockets/drafts/draft_2026-03-27_1023.pdf)  
**Key result:** 35-100× more efficient than whole-cavity coupling

If the whole abdomen is a poor acoustic receiver, local gas pockets are the obvious suspects. This paper shows that constrained bubbles are much better candidates for audible and sub-audible acoustic effects than the entire cavity sloshing about like a well-behaved shell.

### Paper 3 — *Scaling Laws*
**Dimensional analysis predictions across mammalian scales**  
**Status:** Under revision (8 pages)  
**Target venue:** *JSV Short Communication*  
**Latest draft:** [PDF](paper3-scaling-laws/main.pdf)  
**Key result:** Π₀ ≈ 0.07; the breathing mode wants an organism about 20 m long

This is the compact Buckingham-Π paper. It asks what happens if you scale the idea across mammals and, in the process, makes the breathing-mode story even less plausible for anything roughly human-sized.

### Paper 4 — *Bladder Resonance*
**Resonance of the human urinary bladder**  
**Status:** Under development (20+ pages)  
**Target venue:** *Journal of Sound and Vibration*  
**Latest draft:** [PDF](projects/bladder-resonance/paper/drafts/draft_2026-03-27_0910.pdf)  
**Key result:** f₂ = 13.5 Hz at 222 mL

Same modelling philosophy, smaller organ, different loading problem. The bladder turns out to be a cleaner resonance problem than the bowel, and a more believable one.

### Paper 5 — *Borborygmi*
**Multi-mode acoustic model of bowel sounds**  
**Status:** First draft (17 pages)  
**Target venue:** *JASA*  
**Latest draft:** [PDF](projects/borborygmi/paper/main.pdf)  
**Key result:** 135-440 Hz constrained bubble model

This is the bowel-sounds spinout: less mythology, more acoustics. It connects the gas-pocket work to something clinicians and acousticians might actually want to measure.

## The Punchline

The abdomen does have a low-order flexural resonance near 4 Hz, so the folk intuition is not completely mad. What fails is the coupling: even at 120 dB SPL, the energy-consistent airborne displacement is only about 0.014 μm, around four orders of magnitude below mechanotransduction thresholds. Whole-body vibration, by contrast, produces millimetre-scale effective excitation of the relevant mode. In short: the “brown note” is a mechanical story misremembered as an acoustic one.

## Key Results

| Quantity | Value |
|----------|-------|
| n=2 flexural frequency (f₂) | 3.95 Hz |
| Breathing mode (n=0) | 2,490 Hz |
| Airborne displacement (ξ_air, 120 dB) | 0.014 μm |
| Mechanical displacement (ξ_mech, 0.5 m/s²) | 4,586 μm |
| Coupling ratio R | ≈ 66,000× (6.6×10⁴) |
| Sobol total-order index S_T(E) | 0.86 |

## How It Was Made

This repository was built with **GitHub Copilot CLI** and a small bureaucracy of autonomous AI agents handling analysis, drafting, review, figure generation, and repo maintenance. The current tally is roughly **228 commits**, **100 pull requests merged**, **183 tests passing**, **16 custom agents**, **10 reusable skills**, **52+ research logs**, and about **24 hours of wall-clock interaction time**.  

See [docs/ai-assisted-research.md](docs/ai-assisted-research.md) for the workflow notes.

## Quick Start

```bash
pip install -e .
python -m pytest tests/ -v
```

```python
import sys
sys.path.insert(0, r"C:\path\to\browntone")

from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)
from src.analytical.energy_budget import self_consistent_displacement
from src.analytical.mechanical_coupling import mechanical_coupling_analysis

model = AbdominalModelV2(
    E=0.1e6,
    a=0.18,
    c=0.12,
    h=0.01,
    nu=0.45,
    rho_wall=1100,
    rho_fluid=1020,
    K_fluid=2.2e9,
    P_iap=1000,
    loss_tangent=0.25,
)

freqs = flexural_mode_frequencies_v2(model, n_max=5)
disp = self_consistent_displacement(model, mode_n=2, spl_db=120)
mech = mechanical_coupling_analysis(model)
```

If you only want one number, ask the model for the n=2 flexural mode. If you want the whole joke explained properly, read Paper 1.

## Repository Structure

```text
browntone/
├── paper/                        # Paper 1: brown note manuscript + drafts
├── paper2-gas-pockets/          # Paper 2: gas-pocket resonance
├── paper3-scaling-laws/         # Paper 3: dimensional analysis note
├── projects/
│   ├── bladder-resonance/       # Paper 4
│   └── borborygmi/              # Paper 5
├── src/analytical/              # Core analytical models
├── tests/                       # Pytest regression suite
├── docs/research-logs/          # Quantitative research logs
└── .github/                     # Agents, skills, workflows, instructions
```

## Tests

The analytical suite currently has **183 passing tests**. From the repository root:

```bash
python -m pytest tests/ -v
```

## Authors

| Who | Affiliation | Role |
|-----|-------------|------|
| **Jonathan Mace** | MSR | Lead author, concept, writing, supervision |
| **Brian R. Mace** | University of Auckland | Vibroacoustics expertise, theory, supervision |
| **GitHub Copilot CLI (Opus)** | GitHub, Inc. | Analysis, drafting, review orchestration, code |
| **Springbank 10 Year Old** | Campbeltown, Scotland | Moral support, tonal calibration, occasional strategic clarity |

## Licence

[MIT](LICENSE)
