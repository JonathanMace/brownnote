# Browntone Repository Design Document

**Project**: Computational investigation of infrasound-induced resonance in the human abdominal cavity  
**Repository**: `browntone`  
**Date**: 2026-03-27

---

## 1. Directory Structure

```text
browntone/
├── .github/                     # Copilot instructions, agents, skills, workflows
│   ├── agents/                  # Lab-specific specialist agents (*.agent.md)
│   ├── instructions/            # Path-specific coding and writing instructions
│   ├── skills/                  # Reusable workflow guides (skills + legacy guides)
│   └── workflows/               # GitHub Actions
├── data/                        # Literature, materials, simulation results
├── docker/                      # Container tooling
├── docs/                        # Design notes, methodology, research logs
├── notebooks/                   # Exploratory notebooks
├── papers/                      # All paper manuscripts
│   ├── paper1-brown-note/       # Paper 1 (Brown Note) JSV manuscript
│   ├── paper2-gas-pockets/      # Paper 2 (Gas Pockets) JASA manuscript
│   ├── paper3-scaling-laws/     # Paper 3 (Scaling Laws) JSV Short
│   ├── paper4-bladder/          # Paper 4 (Bladder Resonance) JSV
│   ├── paper5-borborygmi/       # Paper 5 (Borborygmi) JASA
│   ├── paper6-sub-bass/         # Paper 6 (Sub-Bass) JASA
│   ├── paper7-watermelon/       # Paper 7 (Watermelon Ripeness)
│   └── paper8-kac/              # Paper 8 (Kac Identifiability)
├── scripts/                     # Utility and automation scripts
├── src/
│   ├── analytical/              # Canonical analytical model code (source of truth)
│   └── browntone/               # Legacy installable package and CLI support code
└── tests/                       # Pytest suite (386 tests)
```

### Directory Purposes

| Directory | Current role |
|-----------|--------------|
| `.github/` | Repository operating system: instructions, specialist agents, workflow skills, CI definitions |
| `src/analytical/` | Primary physics and acoustics models used by the papers; `natural_frequency_v2.py` is the canonical parameter container |
| `src/browntone/` | Legacy package layout retained for CLI, mesh, FEM, and compatibility code |
| `tests/` | Regression and physics sanity checks for analytical, figures, materials, mesh, and extraction code |
| `papers/` | All 8 paper manuscripts with per-paper figures, drafts, and references |
| `docs/research-logs/` | Quantitative session logs and review-cycle history |
| `docs/project-notes/` | Original project READMEs and literature notes |
| `data/` | Repository data assets; mesh artefacts have been removed from `data/meshes/` |

---

## 2. Copilot Collaboration Layout

### Project Instructions

The central instruction file is `.github/copilot-instructions.md`. It records:

- canonical abdominal model parameters,
- git and PR workflow rules,
- paper-writing conventions,
- the current publication pipeline,
- testing expectations (`python -m pytest tests/ -v`),
- and lab-management habits such as research logs and semester breaks.

### Custom Agents

The active agent roster in `.github/agents/` is:

- `chief-of-staff`
- `bibliographer`
- `coffee-machine-guru`
- `communications`
- `consistency-auditor`
- `data-analyst`
- `lab-manager`
- `lab-meeting`
- `loving-spouse`
- `paper-writer`
- `pop-culture-verifier`
- `provocateur`
- `research-scout`
- `reviewer-a`
- `reviewer-b`
- `reviewer-c`
- `simulation-engineer`

These agents cover operations, literature, writing, numerical analysis, QA, strategy,
reviewer simulation, and non-scientific citation auditing.

### Skills

Active skill directories in `.github/skills/`:

- `compile-paper`
- `critique-results`
- `generate-figures`
- `git-checkpoint`
- `jmace-writing-style`
- `mace-writing-style`
- `research-iteration`
- `run-analysis`
- `semester-break`
- `write-agent`
- `write-analysis`
- `write-instructions`
- `write-paper`
- `write-research-log`
- `write-skill`
- `write-tests`

Legacy single-file workflow notes also remain in this folder:

- `generate-figures.md`
- `mesh-convergence.md`
- `run-simulation.md`
- `submit-paper.md`

---

## 3. Publication Pipeline Snapshot

| Paper | Venue | Status | Primary location |
|-------|-------|--------|------------------|
| Paper 1: Brown Note | JSV | ~44 pp, submission-ready | `papers/paper1-brown-note/` |
| Paper 2: Gas Pockets | JASA | ACCEPT, submission-ready (16 pp) | `papers/paper2-gas-pockets/` |
| Paper 3: Scaling Laws | JSV Short | Under revision (8 pp) | `papers/paper3-scaling-laws/` |
| Paper 4: Bladder Resonance | JSV / J Biomech | Minor revision addressed | `papers/paper4-bladder/` |
| Paper 5: Borborygmi | JASA | ACCEPTED (17 pp) | `papers/paper5-borborygmi/` |
| Paper 6: Sub-Bass | JASA | ACCEPT (R2 fixes applied) | `papers/paper6-sub-bass/` |
| Paper 7: Watermelon Ripeness | Postharvest B&T | First complete draft | `papers/paper7-watermelon/` |
| Paper 8: Kac Identifiability | Inverse Problems | First complete draft | `papers/paper8-kac/` |

---

## 4. Tests, Outputs, and Tracking

- The main regression command is `python -m pytest tests/ -v`.
- Current collected test count: **386**.
- LaTeX intermediates are ignored, but PDF outputs are intentionally tracked.
- `data/meshes/` is no longer part of the working tree; mesh outputs should not be
  recreated there unless the data policy changes.

---

## 5. Design Rationale

### Why `src/analytical/` is the source of truth

The repository started with a more package-centric `src/browntone/` layout, but the
publication workflow now centres on the analytical models in `src/analytical/`.
This keeps the canonical physics close to the papers and tests while preserving the
older package structure for compatibility.

### Why PDFs are tracked

This repository treats generated manuscript PDFs as first-class research artefacts.
Draft snapshots, cover letters, and current manuscript PDFs are therefore kept under
version control, while only transient LaTeX build products are ignored.

### Why research logs are central

The lab works iteratively and quantitatively. `docs/research-logs/` captures what
changed, the numerical consequences, and the review status so paper progress does not
depend on memory or chat history.
