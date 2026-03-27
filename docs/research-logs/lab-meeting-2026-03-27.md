# Lab Meeting #1 — 2026-03-27

**Facilitator:** Lab Meeting Agent  
**Scope:** Full repository audit, strategic review, documentation freshness check  
**Repository:** `browntone` (https://github.com/JonathanMace/brownnote)  
**Branch:** `lab-meeting-1` (from main @ `3c42ab7`)

---

## Active Projects Summary

| Project | Status | Last Activity | Next Action | Priority |
|---------|--------|---------------|-------------|----------|
| **Paper 1 (JSV)** — Modal analysis | Round 4 reviews complete; 31 pp | 2026-03-26 (integration v3) | Fix parameter inconsistencies (F1/F2), reframe narrative | 🔴 **Critical** |
| **Paper 2 (JASA)** — Gas pocket transduction | First draft complete in `paper2-gas-pockets/` | PR #15 merged | Internal review, figure polish | 🟡 Medium |
| **Dimensional analysis** | Analysis code done; .tex exists but orphaned | PR #10 merged | Integrate `dimensional_analysis.tex` into Paper 1 or spin off as Paper 3 | 🟡 Medium |
| **Experimental design** | Phantom protocol in `src/experimental/` | PR #9 merged | Parked until Paper 1 submitted | 🟢 Low (for now) |
| **Consistency audit** | Audit report complete | PR #14 merged | Issues overlap with Reviewer B/C findings — use as fix checklist | ✅ Done |
| **Research scouting** | 10 topic ideas generated | PR #13 merged | Review and prioritise after Paper 1 | 🟢 Low |
| **Modal participation** | Branch exists at `b239be6`; worktree active | Stale (points to broader-applications merge) | Unstarted — needed to resolve M2 gap | 🔴 **Critical** |
| **Param consistency fix** | Reviewer C R4 response committed | Branch merged into main | Fixes applied via consistency-audit; verify completeness | 🟡 Medium |
| **Reviewer B R4** | Review written, branch exists (`cec2a4b`) | Not merged to main | **Only unmerged review** — merge or extract findings | 🔴 **Critical** |

---

## Blockers & Risks

### 🔴 BLOCKER 1: Parameter Inconsistency (Fatal for Submission)

All three reviewers flagged this. The paper simultaneously uses two loss tangent values (η = 0.25 in Table 1 vs η = 0.30 in body text), producing inconsistent displacement estimates and coupling ratios throughout. Specific instances:

- **Abstract**: claims ξ_air ≈ 0.01 μm (energy-consistent) but coupling ratio 10⁴ (only valid for pressure-based ξ_air ≈ 0.14 μm)
- **Section 2 vs Table 3**: ξ_air = 0.14 μm vs 0.18 μm (factor 1.3× discrepancy from differing Q)
- **Breathing mode**: Eq. 9 says ~2900 Hz; code computes 2491 Hz; abstract says ~2500 Hz
- **Discussion**: uses ζ = 0.15 (implies η = 0.30), contradicting Table 1

**Impact**: Any careful reviewer will reject on this alone. Must be fixed in a single systematic pass.

### 🔴 BLOCKER 2: Reviewer B R4 Not Merged

Reviewer B's R4 review exists on branch `reviewer-b-r4` (`cec2a4b`) but was never merged to main. Verdict: **MAJOR REVISION** with fatal flaw F1 (abstract self-contradiction) and F2 (loss tangent inconsistency). This review contains the most actionable fix list of all three reviewers.

### 🟡 RISK: M2 Gap Unresolved

The linear model overpredicts WBV displacement by 3.75×. Nonlinear analysis accounts for ~27% (1/3 of the gap). The `modal-participation` worktree was created to address this but contains no new work — it's just pointing at the broader-applications merge commit. This is an open question the reviewers will continue to flag.

### 🟡 RISK: Documentation Drift

Multiple documents are stale or contradictory (see Documentation Freshness Audit below). New agents will inherit incorrect information.

---

## Documentation Freshness Audit

### README.md — 🔴 STALE

| Claim | Reality | Verdict |
|-------|---------|---------|
| "src/browntone/ — Python package" | Active code is in `src/analytical/`; `src/browntone/` is a legacy scaffold | ❌ Misleading |
| Project structure diagram | Lists only src/browntone/ tree; omits src/analytical/, src/experimental/, paper2-gas-pockets/ | ❌ Outdated |
| "Simulation Workflow: Mesh → Solve → Post-process" | Actual workflow is analytical models + LaTeX, no FEA pipeline used | ❌ Describes aspirational workflow, not reality |
| Dependencies table (FEniCSx, gmsh, meshio, PyVista) | Core work uses numpy/scipy/matplotlib only; FEniCSx never used in practice | ❌ Misleading |
| Quick Start instructions | `pip install -e ".[dev]"` works technically but installs wrong package | ⚠️ Technically correct, practically misleading |

**Recommendation**: Complete rewrite. README should describe the analytical modelling project it actually is, not the FEA project it was originally conceived as.

### .github/copilot-instructions.md — 🟡 PARTIALLY STALE

| Section | Status | Issue |
|---------|--------|-------|
| Project Overview | ✅ Current | — |
| Git Workflow | ✅ Current | — |
| Canonical Parameter Set | ✅ Current | — |
| Key Physics | ✅ Current | — |
| Repository Layout | ❌ **Stale** | Missing 5 modules from src/analytical/: `acoustic_coupling.py`, `dimensional_analysis.py`, `mechanotransduction.py`, `natural_frequency.py`, `orifice_coupling.py`. Also missing: `src/experimental/`, `paper2-gas-pockets/` |
| Test count "118 tests" | ✅ Accurate | Verified: 118 tests, all passing |
| Note about src/browntone/ | ⚠️ Correct but insufficient | Says "NOT the active source tree" but doesn't explain what it IS or whether it should be removed |

### docs/RESEARCH-VISION.md — 🟡 PARTIALLY STALE

| Section | Status | Issue |
|---------|--------|-------|
| Paper 1 status | ⚠️ Slightly stale | Says "1-2 more review-revise cycles"; should note Round 4 complete, all 3 reviewers responded |
| Paper 2 status | ❌ **Stale** | Says "Needs its own paper draft" — draft is now COMPLETE in `paper2-gas-pockets/` |
| Paper 3 status | ❌ **Stale** | Says "Agent running" — dimensional analysis merged (PR #10), tex file exists |
| Ideas Backlog | ❌ **Stale** | "Broader applications paragraph" marked unchecked but PR #12 merged it. Experimental protocol marked unchecked but PR #9 completed it. |

### Agent Definitions — ✅ MOSTLY CURRENT

All 9 `.agent.md` files reference existing modules. However:
- **Duplicate files**: `data-analyst.md`, `paper-writer.md`, `simulation-engineer.md`, `literature-researcher.md` exist alongside their `.agent.md` counterparts — likely pre-migration artefacts
- **simulation-engineer.md** and **data-analyst.md** reference `src/browntone/` subdirectories (correct paths exist, but these agents point at the legacy tree)

### Skill Definitions — ✅ MOSTLY CURRENT

All 9 skill directories have proper `SKILL.md` files. However:
- **Orphaned skill stubs** in `.github/skills/` root: `generate-figures.md`, `mesh-convergence.md`, `run-simulation.md`, `submit-paper.md` — these are standalone .md files without corresponding skill directories
- **Duplicate**: `jmace-writing-style/` and `mace-writing-style/` both exist (likely one superseded the other)

---

## Stale & Orphaned Content Inventory

### src/browntone/ — LEGACY, SHOULD BE REMOVED OR CONSOLIDATED

- Contains: `analytical/` (3 files: `acoustic_modes.py`, `shell_vibration.py`), `cli.py`, `fem/`, `mesh/`, `postprocess/`, `utils/`
- Referenced by: `Makefile` (mypy target), `pyproject.toml` (package definition), 2 scripts (`run_modal_analysis.py`, `run_convergence_study.py`), 2 old agent .md files, Docker
- **NOT** referenced by: any test, the actual paper, any current analysis
- **Verdict**: This is the original package scaffold from early development. All active analytical work lives in `src/analytical/`. The `src/browntone/` tree is dead code that creates confusion. Should be either removed or consolidated with `src/analytical/`.

### Orphaned .tex Files in paper/sections/

| File | Size | In main.tex? | Content | Action |
|------|------|:---:|---------|--------|
| `background.tex` | 2.5 KB | ❌ | Full subsections on infrasound, cavity mechanics, shell theory, FSI | Merge into introduction or delete |
| `historical-notes.tex` | 2.2 KB | ❌ | Gavreau, NASA, Tandy, Leventhall historical context | Merge into introduction or delete |
| `methods.tex` | 2.1 KB | ❌ | Skeleton with 5 TODOs; 65% incomplete | Delete (superseded by section2_formulation) |
| `dimensional_analysis.tex` | 4.4 KB | ❌ | Full section with equations + figure refs | Integrate into Paper 1 or move to Paper 3 |

### Orphaned Figures in data/figures/

Figures referenced in current main.tex (via sections/*.tex): 7 figures  
Total figures in data/figures/: 34 files (17 unique figures × PNG+PDF)

Unreferenced figures include: all `fig*_v2_*` variants, `fig_gas_pocket_*.png`, `fig_nonlinear_backbone.png`, `fig_organ_inclusion_effect.png`, `fig_phantom_predictions.png`, `fig_viscous_correction.png`, `fig_uq_coupling_ratio_distribution.png`, `fig_uq_frequency_histogram.png`, and various v1 figures.

**Some of these SHOULD be in the paper** (e.g., nonlinear backbone, viscous correction, UQ histograms) — they represent merged analyses that were never figure-integrated.

### Stale Local Branches (Merged but Not Cleaned Up)

**22 local branches** exist, of which **21 are fully merged** into main. Only `reviewer-b-r4` is unmerged. All the following could be deleted:

`bladder-resonance`, `broader-applications`, `code-tests`, `consistency-audit-r1`, `cover-letter`, `dimensional-analysis`, `experimental-design`, `figures-v4`, `gas-pocket-paper`, `gas-pocket-paper-draft`, `historical-survey`, `lab-infrastructure`, `modal-participation`, `nonlinear-analysis`, `organ-inclusions`, `paper-integration-v3`, `param-consistency-fix`, `readme-rewrite`, `readme-update`, `research-scouting`, `style-editorial`, `supplementary-material`, `viscous-correction`

**6 branches have no remote counterpart** and were never pushed: `bladder-resonance`, `figures-v4`, `lab-infrastructure`, `readme-rewrite`, `style-editorial`, `supplementary-material` — these appear to be branch names created for future work but pointing at merge commits (stale placeholders).

### Active Worktrees

12 worktrees exist. Most point at merged branches and could be pruned:

| Worktree | Branch | Behind Main? | Action |
|----------|--------|:---:|--------|
| `broader-applications` | broader-applications | Yes (merged) | **Remove** |
| `consistency-audit-r1` | consistency-audit-r1 | Yes (merged) | **Remove** |
| `dimensional-analysis` | dimensional-analysis | Yes (merged) | **Remove** |
| `experimental-design` | experimental-design | Yes (merged) | **Remove** |
| `gas-pocket-paper-draft` | gas-pocket-paper-draft | Yes (merged) | **Remove** |
| `modal-participation` | modal-participation | Stale; no new work | **Keep** if M2 work planned |
| `paper-integration-v3` | paper-integration-v3 | Yes (merged) | **Remove** |
| `param-consistency-fix` | param-consistency-fix | Yes (merged) | **Remove** |
| `research-scouting` | research-scouting | Yes (merged) | **Remove** |
| `reviewer-b-r4` | reviewer-b-r4 | **NOT merged** | **Merge first, then remove** |
| `lab-meeting-1` | lab-meeting-1 | Current | Active |

---

## Strategic Observations

### 1. The Paper Is Closer Than It Feels

Despite three MAJOR/MINOR verdicts, the issues are **mechanical, not conceptual**. No reviewer questioned the physics, the model, or the central result. The problems are:
- Parameter inconsistency (η = 0.25 vs 0.30) — a find-and-replace job
- Abstract self-contradiction — 30-minute fix once parameters are canonical
- Missing figure integration — figures exist, just not `\includegraphics`'d
- Narrative reframing — Reviewer A's suggestions are specific and actionable

None of these require new analysis. This is an editing job, not a research job.

### 2. We're Spreading Too Thin

Active branches/projects: Paper 1 (JSV), Paper 2 (JASA), Paper 3 (dimensional analysis), experimental design, research scouting, modal participation analysis. Plus documentation debt. **Paper 1 must be the sole focus until it's submission-ready.** Everything else is a distraction.

### 3. The Source Tree Confusion Is a Recurring Tax

Every new agent has to navigate the `src/browntone/` vs `src/analytical/` ambiguity. The copilot-instructions explains it, but agents that read README.md or pyproject.toml get the wrong picture. This should be resolved once: either move `src/analytical/*.py` into `src/browntone/analytical/` and make it the real package, or delete `src/browntone/` entirely.

### 4. The Review Panel Works Exceptionally Well

Three independent reviewers consistently found real issues, and their findings converged (all flagged η inconsistency). The panel is the project's quality control backbone. Continue using it.

### 5. The Ideas Backlog Is Growing Faster Than It's Being Worked

The scout report added 10 new ideas. The RESEARCH-VISION has ~12 ideas across 3 priority tiers. Most are interesting but none should be touched until Paper 1 is submitted. Risk: idea generation becomes a procrastination mechanism.

---

## Shortest Path to a Submittable Paper 1

### Phase A: Parameter Harmonisation (1 session, ~2 hours)

1. **Canonical value sweep**: Set η = 0.25 everywhere. Grep every .tex and .py file for `0.30`, `Q = 3.3`, `ζ = 0.15` and replace with canonical values
2. **Recompute all inline numbers**: Run each src/analytical module with canonical params, capture outputs, update paper text
3. **Fix abstract**: Choose energy-consistent ξ_air = 0.014 μm; derive coupling ratio = ξ_mech/ξ_air consistently; update abstract, Section 4, Discussion, Conclusion
4. **Fix breathing mode**: Replace "~2900 Hz" in Eq. 9 with "~2490 Hz" throughout
5. **Verify**: Run consistency auditor agent on the fixed paper

### Phase B: Figure Integration (1 session, ~1 hour)

1. Add `\includegraphics` for the 5+ analysis figures that exist but aren't referenced
2. Ensure every figure is cited before it's discussed (JSV convention)
3. Move production figures from data/figures/ to paper/figures/ (or configure graphicspath)

### Phase C: Narrative Reframing (1 session, ~2 hours)

1. Implement Reviewer A's suggestions: lead with coupling disparity, not "debunking"
2. Add broader applications paragraph (blast injury, elastography, marine bio) — PR #12 started this
3. Promote gas pocket mechanism from discussion footnote to headline finding
4. Add ~6 missing references (Junger & Feit, Leissa, Soedel, Stuhmiller, etc.)

### Phase D: Dimensional Analysis Decision (30 min)

Decide: integrate `dimensional_analysis.tex` into Paper 1 as a short subsection, or save for Paper 3. Reviewer A would likely appreciate it; it adds ~2 pages but strengthens the "general framework" narrative.

### Phase E: Final Review (1 session)

Run 3-reviewer panel Round 5 on the fixed paper. If all say MINOR or ACCEPT, proceed to formatting.

### Phase F: Submission Polish (1 session)

- JSV formatting checklist (highlights ≤85 chars, data availability, CRediT, competing interests)
- Final LaTeX compile + proofread
- Submit via Elsevier Editorial Manager

**Estimated total: 4-5 focused sessions to submission.** The bottleneck is Phase A (parameter harmonisation) because it touches every section.

---

## Recommendations for PI

### Immediate (This Week)

1. **Merge Reviewer B R4** (`reviewer-b-r4` branch) — it's the last unmerged review and contains the most specific fix list
2. **Launch parameter harmonisation agent** — single-purpose: make η = 0.25 everywhere, recompute all numbers, fix abstract contradiction. This is the #1 blocker
3. **Prune stale worktrees and branches** — 10 worktrees and 21 merged branches are cluttering the workspace

### Short Term (Next 2 Weeks)

4. **Rewrite README.md** — current README describes a different project. Replace with actual project description (analytical modelling, not FEA)
5. **Update copilot-instructions.md** — add 5 missing modules to repository layout, add `src/experimental/`, add `paper2-gas-pockets/`
6. **Resolve src/browntone/ vs src/analytical/** — either consolidate or delete. Continuing with two source trees is a tax on every agent interaction
7. **Integrate orphaned figures** — at least 5 analysis figures exist in data/figures/ that should be in the paper
8. **Update RESEARCH-VISION.md** — Paper 2 draft is done, dimensional analysis is merged, broader applications PR merged. Check off completed items

### After Paper 1 Submission

9. **Paper 2 (JASA)** — gas pocket paper has a complete first draft; run review panel on it
10. **Clean up orphaned .tex files** — decide fate of background.tex, historical-notes.tex, methods.tex, dimensional_analysis.tex
11. **Prune skill/agent duplicates** — remove old .md files in .github/agents/ and .github/skills/
12. **Address M2 gap** — modal participation analysis was planned but never started. This is a natural Paper 1 follow-up or erratum topic

### Do NOT Do Yet

- Start any new spin-off papers (Papers 3-5)
- Work on experimental phantom fabrication
- Investigate any of the 10 scouted research topics
- Add FEA capability (the analytical approach is sufficient for Paper 1)

---

## Ideas That Emerged

1. **Automated consistency checker**: A CI workflow that runs all src/analytical modules with canonical params and diffs the output against paper text. Would catch η-type inconsistencies automatically. Could be a GitHub Action triggered on paper/ changes.

2. **Parameter manifest file**: Single `params.yaml` or `params.json` that both Python code and LaTeX read from. Eliminates the source of the current inconsistencies entirely.

3. **Figure-paper linkage audit**: A script that parses main.tex for `\includegraphics` and `\ref{fig:}` and cross-references against data/figures/. Would catch orphaned figures automatically.

4. **Worktree lifecycle management**: After each PR merge, automatically suggest worktree pruning. The current 12-worktree state is unsustainable.

5. **The M2 gap as a feature, not a bug**: Rather than resolving the 3.75× overprediction, frame it explicitly as a known limitation with identified contributing factors (modal participation, nonlinear saturation, boundary conditions). A factor of 4 in biomechanics is within normal modelling uncertainty. This may be more honest than trying to close the gap with additional corrections.

---

*Meeting adjourned. Next lab meeting should follow completion of Phase A (parameter harmonisation).*
