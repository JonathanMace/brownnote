# Browntone — Copilot Project Instructions

## Project Overview

**Browntone** is a computational biomechanics research project investigating whether
infrasound can induce resonance in the human abdominal cavity — the so-called "brown
note" hypothesis. We model the abdomen as a fluid-filled viscoelastic oblate spheroidal
shell and compare airborne acoustic vs mechanical (whole-body vibration) coupling.

**Target venue**: Journal of Sound and Vibration (JSV), Elsevier.

## Git Workflow: Worktrees and Pull Requests

### Branch Structure
- **`main`** — the canonical branch. Contains the integrated paper, all merged analyses,
  and the latest compilable LaTeX draft. Only the orchestrator merges to main.
- **Feature branches** — one per research stream (e.g., `nonlinear-analysis`,
  `gas-pocket-paper`, `viscous-correction`). Each has a git worktree at
  `C:\Users\jon\OneDrive\Projects\browntone-worktrees\<branch-name>`.

### For Subagents: How to Work
1. **You will be assigned a worktree path.** All your file edits go there.
2. **Commit on your branch** when done:
   ```powershell
   cd C:\Users\jon\OneDrive\Projects\browntone-worktrees\<your-branch>
   git add -A
   git commit -m "[category] Description

   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   ```
3. **Push your branch**: `git push origin <your-branch>`
4. **Do NOT** edit files on `main` or in other worktrees.
5. **Do NOT** merge branches yourself — the orchestrator handles merges via PRs.

### For the Orchestrator: Merging
- When an agent completes, push its branch and create a PR on GitHub.
- Review the PR (or have `reviewer-b` agent review it).
- Merge to main, then pull in the main worktree.
- Remote: `https://github.com/JonathanMace/brownnote`

### Commit Message Prefixes
`[analysis]` `[paper]` `[fea]` `[review]` `[infra]` `[figures]` `[tests]`

## Canonical Parameter Set

**Every computation must use these values unless explicitly varying a parameter.**
This is the single most important consistency rule in the project.

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Semi-major axis | a | 0.18 | m |
| Semi-minor axis | c | 0.12 | m |
| Wall thickness | h | 0.010 | m |
| Elastic modulus | E | 0.1 | MPa |
| Poisson's ratio | ν | 0.45 | — |
| Wall density | ρ_w | 1100 | kg/m³ |
| Fluid density | ρ_f | 1020 | kg/m³ |
| Fluid bulk modulus | K_f | 2.2 | GPa |
| Intra-abdominal pressure | P_iap | 1000 | Pa |
| Loss tangent | η | 0.25 | — |

**Derived values** (from canonical set):
- Equivalent sphere radius: R_eq = (a²c)^(1/3) = 0.157 m
- n=2 flexural frequency: f₂ = 4.0 Hz
- Quality factor: Q = 1/η = 4.0
- Damping ratio: ζ = η/2 = 0.125
- ka at f₂: 0.0114
- Breathing mode: ~2490 Hz

## Key Physics — Must Understand

### Two Mode Families
1. **Breathing mode (n=0)**: ~2500 Hz. Dominated by fluid bulk modulus. Irrelevant
   to infrasound. The fluid acts as an incredibly stiff volumetric spring.
2. **Flexural modes (n≥2)**: 4-10 Hz. The shell changes shape without compressing the
   fluid. Fluid acts only as added mass. These are the brown note candidates.

### The Coupling Disparity (Central Result)
- **Airborne**: Penalised by (ka)^n. At 4 Hz, (ka)² ≈ 1.3×10⁻⁴. Energy-consistent
  displacement at 120 dB: ~0.014 μm. Far below PIEZO threshold (0.5-2 μm).
- **Mechanical (WBV)**: Direct coupling, no ka penalty. At 0.1 m/s²: ~649 μm.
  Ratio: ~46,000×. This explains WHY WBV causes GI effects but airborne doesn't.

### Energy Budget
The shell absorbs ~10⁻¹⁴ of incident acoustic energy. The pressure-based model
overestimates displacement by ~13.4× vs the energy-consistent reciprocity analysis.
**Always use energy-consistent values for airborne coupling claims.**

## Repository Layout

```
src/analytical/          — Core analytical models (the main source tree)
  natural_frequency_v2.py   — Modal analysis (AbdominalModelV2 dataclass)
  mechanical_coupling.py    — WBV vs airborne comparison
  energy_budget.py          — Reciprocity-based self-consistent analysis
  gas_pocket_resonance.py   — Bowel gas as acoustic transducers
  gas_pocket_detailed.py    — Constrained bubble model, differential susceptibility
  parametric_analysis.py    — Sensitivity study (486 combinations)
  multilayer_wall.py        — 5-layer composite wall model
  oblate_spheroid_ritz.py   — Rayleigh-Ritz oblate correction
  uncertainty_quantification.py — Monte Carlo UQ + Sobol indices
  nonlinear_analysis.py     — Duffing oscillator, backbone curves, jump phenomenon
  viscous_correction.py     — Stokes boundary layer damping validation
  organ_inclusions.py       — Effective medium theory for organ inclusions
src/fem/                 — FEA mesh generation and Lamb-mode Rayleigh-Ritz solver
paper/                   — LaTeX manuscript (elsarticle, JSV format)
  main.tex                  — Master document
  sections/                 — Individual section .tex files
  references.bib            — BibTeX database
  drafts/                   — Timestamped PDF snapshots
  cover-letter.tex          — JSV cover letter
  graphical-abstract.py     — Matplotlib graphical abstract generator
data/figures/            — Publication figures (PNG@300dpi + PDF)
data/results/            — JSON result files
data/meshes/             — gmsh .msh files
docs/research-logs/      — Timestamped research journal + reviewer reports + PDF snapshots
docs/style-references/   — Brian Mace papers and style analysis
tests/                   — pytest test suite (118 tests, all passing)
.github/skills/          — Copilot skills (compile-paper, mace-writing-style, etc.)
.github/agents/          — Copilot agents (reviewer-a, reviewer-b, reviewer-c, etc.)
```

Note: `src/browntone/` also exists (created by an early agent) but is NOT the active
source tree. Use `src/analytical/` for all model code.

## How to Use the Core Model

```python
import sys
sys.path.insert(0, r'C:\Users\jon\OneDrive\Projects\browntone')
# OR from a worktree:
sys.path.insert(0, r'C:\Users\jon\OneDrive\Projects\browntone-worktrees\<branch>')

from src.analytical.natural_frequency_v2 import AbdominalModelV2, flexural_mode_frequencies_v2

# Canonical parameters
model = AbdominalModelV2(
    E=0.1e6, a=0.18, b=0.18, c=0.12, h=0.01,
    nu=0.45, rho_wall=1100, rho_fluid=1020,
    K_fluid=2.2e9, P_iap=1000, loss_tangent=0.25
)
freqs = flexural_mode_frequencies_v2(model, n_max=5)
# freqs = {0: 2490.6, 1: 0.0, 2: 3.95, 3: 6.31, 4: 8.88, 5: 11.71}
```

## Paper Compilation

```powershell
cd C:\Users\jon\OneDrive\Projects\browntone\paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
# Preserve snapshot:
$ts = Get-Date -Format "yyyy-MM-dd_HHmm"
Copy-Item main.pdf "drafts\draft_$ts.pdf"
```

**JSV format requirements**: `\documentclass[review]{elsarticle}`, line numbering
(`lineno`), highlights (3-5, ≤85 chars), `elsarticle-num.bst`, data availability
statement, CRediT, competing interests.

## Writing Style

We blend two voices:
1. **Brian Mace's JSV conventions** (see `.github/skills/mace-writing-style/SKILL.md`):
   Structural precision, measured hedging, systematic section openings, explicit
   equation presentation with "where..." clauses.
2. **Accessible and engaging**: Active voice where it aids clarity, subtle dry humour
   about the subject matter (the topic invites it), vivid physical analogies.

**Rules**:
- British English (behaviour, modelled, analysed)
- `\SI{}{}` for all quantities with units
- Define all symbols at first use
- No overclaiming. "The results suggest..." not "We prove..."
- Figures referenced before discussion: "Figure 3 shows..."
- Tables use `\toprule`, `\midrule`, `\bottomrule` (booktabs)

## Research Iteration Cycle

Every major phase follows: **DO → REVIEW → LOG → COMPILE → COMMIT → PLAN NEXT**

- **DO**: Launch parallel agents on independent work streams. Each agent gets its own
  worktree and branch (see Git Workflow above). Every agent must commit and push.
- **REVIEW**: Launch a **3-reviewer panel** (see below). Each reviewer works in a
  read-only capacity and writes their review to `docs/research-logs/`.
- **LOG**: Timestamped entry in `docs/research-logs/YYYY-MM-DDTHHMM-topic.md`,
  with a copy of the current compiled PDF as `YYYY-MM-DDTHHMM-paper-snapshot.pdf`
- **COMPILE**: Build LaTeX, preserve timestamped PDF in `paper/drafts/`
- **COMMIT**: Git commit with descriptive message + push to main
- **PLAN NEXT**: Update SQL todos, identify next parallel batch, update these instructions

### 3-Reviewer Panel

Each review round launches 3 reviewers in parallel on separate worktrees/branches:

| Reviewer | Role | Focus |
|----------|------|-------|
| **Reviewer A** | Domain expert (vibroacoustics) | Novelty, significance, framing, "so what?", missing refs, narrative arc |
| **Reviewer B** | Cynical gatekeeper | Fatal flaws, technical errors, parameter consistency, logical gaps |
| **Reviewer C** | Methodologist / reproducer | Code-paper consistency, UQ completeness, reproducibility, runs the code |

Each reviewer:
1. Gets a worktree + branch (e.g., `review-a-r4`, `review-b-r4`, `review-c-r4`)
2. Reads the full paper and source code
3. Writes their review to `docs/research-logs/reviewer-X-roundN.md`
4. Commits and pushes their branch
5. Does NOT edit paper or source files — review only

The orchestrator synthesises all 3 reviews into an action plan before the next iteration.

### Keeping These Instructions Current

**After every major iteration**, the orchestrator must review and update this file to
reflect: new modules added, changed canonical values, new workflow patterns, lessons
learned. This file is the single source of truth for all agents.

## Code Conventions

- **Python ≥ 3.10**, numpy/scipy/matplotlib (globally installed)
- Type hints on public functions
- NumPy-style docstrings
- SI units throughout; document in variable names where ambiguous
- `snake_case` for functions, `PascalCase` for classes
- No magic numbers — use the canonical parameter set or named constants
- `import matplotlib; matplotlib.use('Agg')` for headless figure generation

## What NOT to Do

- Do not use "brown note" in any LaTeX content destined for the paper.
  Use "infrasound-induced abdominal resonance" or similar.
- Do not use the pressure-based displacement estimate without noting it is an
  upper bound (~13× overestimate). Use energy-consistent values.
- Do not confuse breathing modes (n=0, ~2500 Hz) with flexural modes (n≥2, 4-10 Hz).
  This was the fatal error in v1 of the model.
- Do not edit files outside your assigned worktree.
- Do not merge branches — only the orchestrator merges via PRs.
