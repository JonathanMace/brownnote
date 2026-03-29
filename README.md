# The Brown Note

Among the many questions that humanity has posed to the universe — the nature of consciousness, the origin of dark matter, the thermodynamic arrow of time — one has proven uniquely resistant to serious academic inquiry: can sound make you soil yourself? 

The hypothesis, known colloquially as the “brown note,” posits that infrasound at some critical frequency might induce involuntary gastrointestinal distress. Despite decades of anecdote, no rigorous analytical treatment existed. We found this oversight unacceptable. 

This repository models the human abdomen as a fluid-filled viscoelastic oblate spheroidal shell, derives its modal characteristics from first principles, and determines — with what we believe is an unprecedented level of analytical formality — that the answer is almost certainly no. The flexural resonance sits comfortably in the infrasonic band, but the airborne acoustic energy required to drive it meaningfully exceeds anything achievable outside of a Saturn V launch. 

Whole-body vibration is another matter entirely, which is why we wrote seven papers instead of one.

## Papers

### Paper 1 — *The Brown Note*
**Modal analysis of a fluid-filled viscoelastic oblate spheroidal shell**  
**Status:** Submission-ready (30 pages, 5 figures, 9 tables, 52 references)  
**Target venue:** *Journal of Sound and Vibration*  
**Latest draft:** [PDF](paper/drafts/draft_2026-03-29_1536_submission-final.pdf)  
**Key result:** coupling ratio R ≈ 6.6 × 10⁴

Can a sufficiently powerful subwoofer ruin your afternoon? We model the human abdomen as a fluid-filled viscoelastic oblate spheroidal shell, derive its modal spectrum from first principles, and compare airborne acoustic coupling with whole-body mechanical vibration. The resonance is real; the acoustic pathway to it is not.

### Paper 2 — *Gas Pockets*
**Gas pocket resonance as an alternative acoustic coupling mechanism**  
**Status:** ACCEPT after internal review; submission-ready (18 pages)  
**Target venue:** *Journal of the Acoustical Society of America*  
**Latest draft:** [PDF](paper2-gas-pockets/drafts/draft_2026-03-29_1538_submission.pdf)  
**Key result:** 35-100× more efficient than whole-cavity coupling

If the whole abdomen will not cooperate, perhaps the gas trapped inside it will. We model intestinal gas pockets as tissue-constrained bubbles and show they couple to airborne sound 35–100× more efficiently than the cavity itself — enough, at extreme SPL, to activate mechanosensitive ion channels in nearby tissue.

### Paper 3 — *Scaling Laws*
**Dimensional analysis predictions across mammalian scales**  
**Status:** Under revision (8 pages)  
**Target venue:** *JSV Short Communication*  
**Latest draft:** [PDF](paper3-scaling-laws/drafts/draft_2026-03-29_1556.pdf)  
**Key result:** Π₀ ≈ 0.07; the breathing mode wants an organism about 20 m long

Do rats, cats, pigs, and humans all resonate the same way, or is the brown note a uniquely human indignity? Buckingham Pi analysis reduces the ten-parameter shell problem to five governing groups, revealing a quasi-universal dimensionless frequency Π₀ ≈ 0.07 across species and a scattering coupling ratio that is approximately size-independent.

### Paper 4 — *Bladder Resonance*
**Resonance of the human urinary bladder**  
**Status:** Under development (20+ pages)  
**Target venue:** *Journal of Sound and Vibration*  
**Latest draft:** [PDF](projects/bladder-resonance/paper/drafts/draft_2026-03-29_1556.pdf)  
**Key result:** f₂ = 13.5 Hz at 222 mL

Anyone who has endured a long motorway journey on a full bladder has conducted an informal experiment in pelvic vibroacoustics. We apply the fluid-filled shell framework to the urinary bladder, finding a non-monotonic U-shaped frequency curve whose minimum coincides suspiciously with typical driving-posture fill volumes.

### Paper 5 — *Borborygmi*
**Multi-mode acoustic model of bowel sounds**  
**Status:** First draft complete (17 pages)  
**Target venue:** *JASA*  
**Latest draft:** [PDF](projects/borborygmi/paper/drafts/draft_2026-03-29_1556.pdf)  
**Key result:** 135-440 Hz constrained bubble model

Your stomach growls. What pitch is it, exactly, and why? We develop a five-mechanism acoustic model — from free Minnaert bubbles through tissue-constrained oscillations to Helmholtz orifice resonance — that predicts the clinically observed 200–550 Hz bowel sound band without tuning.

### Paper 6 — *Can You Feel the Bass?*
**Sub-bass perception thresholds and abdominal resonance at concert sound pressure levels**  
**Status:** Minor revision (R2 fixes applied)  
**Target venue:** *JASA*  
**Latest draft:** [PDF](paper6-sub-bass/drafts/draft_2026-03-29_1556.pdf)  
**Location:** `paper6-sub-bass/`  
**Key finding:** Airborne acoustic coupling produces tissue displacement ~2.5 orders below perception thresholds even at concert levels. Structure-borne (floor/seat) vibration is the dominant pathway, with floor displacement reaching 904% of the perception threshold.

If concert bass feels visceral, is the abdomen actually being driven by airborne sound? This paper compares predicted sub-bass-induced tissue motion against perception thresholds and finds the airborne pathway falls roughly 2.5 orders of magnitude short even at concert SPL. The dominant pathway is structure-borne vibration transmitted through floors and seating — floor displacement alone reaches 904% of the vibrotactile perception threshold.

### Paper 7 — *Can You Hear the Ripeness?*
**Can You Hear the Ripeness? Non-Destructive Acoustic Assessment of Fruit Maturity via Shell Resonance Inversion**  
**Authors:** J. Mace and B.R. Mace  
**Status:** First complete draft (19 pp) — submission-ready  
**Venue:** *Postharvest Biology and Technology* / *PNAS*  
**Location:** `projects/watermelon-ripeness/`  
**Latest draft:** [`draft_2026-03-29_1556_post-reviewer-b-r4.pdf`](projects/watermelon-ripeness/paper/drafts/draft_2026-03-29_1556_post-reviewer-b-r4.pdf)  
**Key result:** tap-tone inversion maps measured resonance frequency to rind stiffness and ripeness stage.

If growers can judge a watermelon by tapping it, the obvious question is whether shell theory can formalise the trick. This project recasts the fruit as a fluid-filled viscoelastic spheroidal shell and uses resonance inversion to infer rind modulus — turning folk wisdom into a quantitative ripeness estimator.

### Paper 8 — *Can You Hear the Shape of an Organ?*
**Can You Hear the Shape of an Organ? Practical Identifiability of Viscoelastic Shell Parameters from Resonant Frequencies**  
**Authors:** J. Mace and B.R. Mace  
**Status:** First complete draft  
**Venue:** *Inverse Problems*  
**Location:** `projects/kac-identifiability/`  
**Latest draft:** [`draft_2026-03-29_1519.pdf`](projects/kac-identifiability/paper/drafts/draft_2026-03-29_1519.pdf)  
**Key result:** oblate geometry reduces the condition number from 10¹⁰ to 73, making the (a, c, E) parameter triple practically identifiable from resonant frequencies.

The inverse counterpart of Kac's celebrated "Can one hear the shape of a drum?" applied to vibroacoustic organ models. At the spherical operating point the scaled Jacobian is effectively rank-deficient; oblate geometry restores identifiability, enabling Newton-type inversion to recover shell parameters to sub-percent accuracy.

### Research Statement
**[Mid-Tenure Research Statement](docs/mid-tenure-research-statement.pdf)** — Research vision, accomplishments, and trajectory for the Browntone programme.

## The Punchline

The abdomen does have a low-order flexural resonance near 4 Hz, so the folk intuition is not completely mad. What fails is the coupling: even at 120 dB SPL, the energy-consistent airborne displacement is only about 0.014 μm, around four orders of magnitude below mechanotransduction thresholds. Whole-body vibration, by contrast, produces millimetre-scale effective excitation of the relevant mode. In short: the “brown note” is a mechanical story misremembered as an acoustic one.

## Key Results

| Quantity | Value |
|----------|-------|
| n=2 flexural frequency (f₂) | 3.95 Hz |
| Breathing mode (n=0) | 2,490 Hz |
| Airborne displacement (ξ_air, 120 dB) | 0.014 μm |
| Mechanical displacement (ξ_mech, 0.1 m/s²) | 917 μm |
| Coupling ratio R | ≈ 66,000× (6.6×10⁴) |
| Sobol total-order index S_T(E) | 0.86 |

## How It Was Made

This repository was built with **GitHub Copilot CLI** and a small bureaucracy of autonomous AI agents handling analysis, drafting, review, figure generation, and repo maintenance. The current tally is roughly **377 commits**, **208 pull requests merged**, **377 tests passing**, **20 custom agents**, **16 reusable skills**, **77 research logs**, and about **24 hours of wall-clock interaction time**.  

The active agent roster lives in [`.github/agents/`](.github/agents/) and currently includes the review panel (`reviewer-a`, `reviewer-b`, `reviewer-c`), infrastructure roles (`chief-of-staff`, `lab-manager`, `lab-meeting`), editorial triage via `journal-editor`, production roles (`paper-writer`, `simulation-engineer`, `data-analyst`, `communications`, `bibliographer`), and specialist characters such as `pop-culture-verifier`, `provocateur`, `research-scout`, `coffee-machine-guru`, `loving-spouse`, `dietrich`, and `experimentalist`.

See [docs/ai-assisted-research.md](docs/ai-assisted-research.md) for the workflow notes.

## Quick Start

```bash
pip install -e .[dev]
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
from src.analytical.mechanical_coupling import compare_airborne_vs_mechanical

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
mech = compare_airborne_vs_mechanical(model)
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
│   ├── borborygmi/              # Paper 5
│   ├── watermelon-ripeness/     # Paper 7
│   └── kac-identifiability/    # Paper 8
├── paper6-sub-bass/             # Paper 6: sub-bass coupling
├── src/analytical/              # Core analytical models, including watermelon_model.py
├── tests/                       # Pytest regression suite
├── docs/research-logs/          # Quantitative research logs
└── .github/                     # Agents, skills, workflows, instructions
```

## Tests

The analytical suite currently has **377 passing tests**. From the repository root:

```bash
python -m pytest tests/ -v
```

## Authors

| Who | Affiliation | Role |
|-----|-------------|------|
| **Jonathan Mace** | MSR | Lead author, concept, writing, supervision |
| **Brian R. Mace** | University of Auckland; Visiting Professor, Browntone Lab | Vibroacoustics expertise, theory, supervision |
| **GitHub Copilot CLI (Opus)** | GitHub, Inc. | Analysis, drafting, review orchestration, code |
| **Springbank 10 Year Old** | Campbeltown, Scotland | Moral support, tonal calibration, occasional strategic clarity |

## Licence

[MIT](LICENSE)
