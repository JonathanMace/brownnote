# Lab Meeting #2 — 2026-03-27 (Round 6 Comprehensive Audit)

**Facilitator:** Lab Meeting Agent  
**Scope:** Full repository audit per PI checklist — README, instructions, agents, skills, tests, git, paper, logs  
**Repository:** `browntone` (https://github.com/JonathanMace/brownnote)  
**Branch:** `round6-lab-meeting` (from main @ `501411c`)

---

## Executive Summary

The project has made significant progress since Lab Meeting #1. The parameter
harmonisation (η = 0.25 throughout), narrative reframe (coupling disparity as
lead), broader applications section, and missing references have all been
addressed. The paper now compiles cleanly at **37 pages** with **zero undefined
references**. The test suite is **118/118 passing**. Reviewer A has given
**ACCEPT (minor corrections)** — the first acceptance recommendation in the
project's history.

However, Reviewer B Round 5 issued **MAJOR REVISION** with one near-fatal
finding: the modal participation factor (Γ₂ ≈ 0.48) exists in code
(`modal_participation.py`) but was never written into the paper text,
meaning all mechanical displacements are overstated by ~2×. This is the
single remaining blocker to submission.

**Bottom line:** The paper is 1 focused revision away from submission-ready.
The revision is a write-up task, not a research task.

---

## Active Projects Summary

| Project | Status | Last Activity | Next Action | Priority |
|---------|--------|---------------|-------------|----------|
| **Paper 1 (JSV)** — Modal analysis | 37pp, R5 complete: A=ACCEPT, B=MAJOR | 2026-03-27 (PR #41) | Write up modal participation, fix coupling ratio | 🔴 **Critical** |
| **Paper 2 (JASA)** — Gas pocket transduction | First draft complete + figures | 2026-03-27 | Run review panel after Paper 1 submits | 🟡 Medium |
| **Paper 3** — Dimensional analysis / scaling | Analysis code done, .tex orphaned | Stale | Decide: integrate into Paper 1 or spin off | 🟢 Low |
| **Bladder resonance** | Early stage, project directory exists | Stale | Parked until Paper 1 submitted | 🟢 Low |
| **Experimental design** | Phantom protocol in `src/experimental/` | Stale | Parked until Paper 1 submitted | 🟢 Low |

---

## Check 1: README.md — ✅ CURRENT

The README was comprehensively rewritten in PR #19 and updated through PR #41.
It now accurately describes the project.

| Claim | Reality | Verdict |
|-------|---------|---------|
| "Modal analysis of a fluid-filled viscoelastic oblate spheroidal shell" | Correct — this is the project | ✅ |
| Project structure showing `src/analytical/` (17 modules) | All 17 modules exist and are listed | ✅ |
| `paper2-gas-pockets/` in structure | Directory exists with draft | ✅ |
| Key results table (f₂=3.95 Hz, R≈46,000, etc.) | Matches code output | ✅ |
| Quick Start code example | Works with canonical params | ✅ |
| "pytest tests/" instructions | 118 tests, all passing | ✅ |
| "main is protected — all changes via PRs" | Correct | ✅ |
| Authors table (Jonathan, Brian, Springbank, Opus) | Current | ✅ |

**Minor issue:** README doesn't mention the paper page count or review status.
Not critical — README is for the repo, not the paper.

---

## Check 2: .github/copilot-instructions.md — 🟡 MOSTLY CURRENT (4 issues)

| Section | Status | Issue |
|---------|--------|-------|
| Identity & Project | ✅ Current | — |
| R1: Git Workflow | ✅ Current | — |
| R2: Research Logs | ✅ Current | — |
| R3: Canonical Parameters | ✅ Current | All values correct, stale values flagged |
| R4: Physics Integrity | ✅ Current | — |
| R5: Code Quality | ✅ Current | "118+ tests" — exact |
| R6: Documentation Sync | ✅ Current | — |
| R7: Review Standards | ✅ Current | — |
| R8: Writing Standards | ✅ Current | — |
| Agent Git Workflow | ✅ Current | — |
| Key Physics | ⚠️ **Stale** | Lists Γ₂ = 0.48 (correct) but paper doesn't include it yet |
| Agent table | ✅ Current | All 16 agents listed |
| Skills table | ⚠️ **Incomplete** | Lists 9 skills but `semester-break` skill exists and is not listed |
| Publication Pipeline | ⚠️ **Stale** | Says "~31pp" — paper is now **37 pages**. Says "M2 gap closed" — Reviewer B R5 says it's still open in the paper text |
| Chief-of-staff agent | ⚠️ **Stale path** | References `C:\Users\jon\.copilot\session-state\4ecd4bf8-...` — session-specific path |

### Recommended fixes:
1. Update Publication Pipeline: "~31pp" → "37pp"
2. Update "M2 gap closed" → "M2 gap: code done, paper write-up pending"
3. Add `semester-break` to skills table
4. Remove session-state path from chief-of-staff (or make it generic)

---

## Check 3: Agent Definitions (.github/agents/) — ✅ ALL CURRENT

**16 agents defined**, all with proper `.agent.md` format:

| Agent | File | Canonical Params | Physics Rules | Git Workflow | Verdict |
|-------|------|:---:|:---:|:---:|:---:|
| chief-of-staff | ✅ | n/a | n/a | ✅ | ✅ |
| reviewer-a | ✅ | n/a | n/a | ✅ | ✅ |
| reviewer-b | ✅ | n/a | n/a | ✅ | ✅ |
| reviewer-c | ✅ | ✅ | ✅ | ✅ | ✅ |
| paper-writer | ✅ | ✅ | ✅ | ✅ | ✅ |
| simulation-engineer | ✅ | ✅ | ✅ | ✅ | ✅ |
| data-analyst | ✅ | ✅ | ✅ | ✅ | ✅ |
| consistency-auditor | ✅ | n/a | n/a | ✅ | ✅ |
| lab-meeting | ✅ | n/a | n/a | ✅ | ✅ |
| lab-manager | ✅ | n/a | n/a | n/a | ✅ |
| research-scout | ✅ | n/a | n/a | ✅ | ✅ |
| provocateur | ✅ | n/a | n/a | ✅ | ✅ |
| communications | ✅ | n/a | n/a | ✅ | ✅ |
| bibliographer | ✅ | n/a | n/a | ✅ | ✅ |
| coffee-machine-guru | ✅ | n/a | n/a | n/a | ✅ |
| loving-spouse | ✅ | n/a | n/a | n/a | ✅ |

**No stale references found.** All agents reference `src/analytical/` (not legacy
`src/browntone/`). Persona definitions are well-crafted and differentiated.
The review panel (A/B/C) has clear scope separation.

**One minor issue:** `chief-of-staff.agent.md` references a hardcoded
session-state path (`C:\Users\jon\.copilot\session-state\4ecd4bf8-...`). This
will break across sessions. Should use a relative or configurable path.

---

## Check 4: Skills (.github/skills/) — 🟡 CURRENT but CLUTTERED

### Proper skill directories (9) — all with SKILL.md:
| Skill | Purpose | Current? |
|-------|---------|:---:|
| `research-iteration/` | Full DO→REVIEW→LOG→COMPILE→COMMIT | ✅ |
| `compile-paper/` | LaTeX compilation + PDF snapshot | ✅ |
| `run-analysis/` | Analytical pipeline + verify | ✅ |
| `generate-figures/` | Publication figures (replaces standalone) | ✅ |
| `critique-results/` | 3-reviewer panel | ✅ |
| `write-paper/` | JSV drafting guide | ✅ |
| `git-checkpoint/` | Branch→PR→merge→cleanup | ✅ |
| `jmace-writing-style/` | Jonathan Mace voice | ✅ |
| `mace-writing-style/` | Brian Mace JSV voice | ✅ |

### Unlisted skill directory (1):
| Skill | Purpose | In copilot-instructions? |
|-------|---------|:---:|
| `semester-break/` | Mandatory hourly reflection | ❌ **Missing from table** |

### Orphaned standalone .md files (4) — pre-migration artefacts:
| File | Status | Issue |
|------|--------|-------|
| `generate-figures.md` | 🔴 **STALE** | References `browntone.postprocess.visualization` (legacy `src/browntone/`). Superseded by `generate-figures/SKILL.md` |
| `run-simulation.md` | 🔴 **STALE** | References `browntone.fem`, `browntone.mesh`, `browntone.analytical` — all legacy imports. Describes FEniCSx pipeline never used |
| `mesh-convergence.md` | 🔴 **STALE** | References `browntone.mesh.abdominal_cavity`, `browntone.fem.modal_analysis` — legacy. Describes FEA workflow not used |
| `submit-paper.md` | ✅ Current | Generic JSV checklist, no stale references |

### Recommended actions:
1. Delete `generate-figures.md` (superseded by directory version)
2. Delete `run-simulation.md` (describes unused FEniCSx workflow)
3. Delete `mesh-convergence.md` (describes unused FEA workflow)
4. Add `semester-break` to skills table in `copilot-instructions.md`

---

## Check 5: Test Suite — ✅ ALL PASSING

```
platform win32 -- Python 3.12.10, pytest-9.0.2
collected 118 items

tests/test_analytical.py       90 passed   [ 75%]
tests/test_extraction.py        2 passed   [ 77%]
tests/test_figures.py            8 passed   [ 83%]
tests/test_materials.py         14 passed   [ 95%]
tests/test_mesh.py               4 passed   [100%]
============ 118 passed, 1 warning in 14.31s ============
```

| Metric | Value |
|--------|-------|
| Total tests | 118 |
| Passed | 118 (100%) |
| Failed | 0 |
| Skipped | 0 |
| Warnings | 1 (dateutil deprecation — external, harmless) |
| Test files | 7 |
| Source modules | 44 (across `src/`) |
| Runtime | 14.31s |

**Code health is excellent.** No regressions detected.

---

## Check 6: Git Status — 🟡 NEEDS CLEANUP

### Working tree
- **Branch:** `main` (up to date with `origin/main`)
- **Untracked files:** 2 draft PDFs in `paper/drafts/` (gitignored — fine)
- **Uncommitted changes:** None

### Local branches (9 stale, all merged)
All of the following are fully merged into main and should be deleted:

| Branch | Status |
|--------|--------|
| `add-semester-break` | ✅ Merged |
| `branch-cleanup` | ✅ Merged |
| `fix-highlights-coupling` | ✅ Merged |
| `geometry-and-modal` | ✅ Merged |
| `instruction-architecture` | ✅ Merged |
| `revision-round5` | ✅ Merged |
| `semester-1-break` | ✅ Merged |
| `submission-fixes-v2` | ✅ Merged |
| `winter-break-overhaul` | ✅ Merged |

### Remote branches (8 stale)
| Remote Branch | Status | Action |
|---------------|--------|--------|
| `origin/catch-up-log` | Merged | Delete |
| `origin/consistency-audit-r1` | Merged | Delete |
| `origin/cover-letter-update` | Already deleted on GitHub | Prune |
| `origin/gas-pocket-paper-draft` | Merged | Delete |
| `origin/missing-refs` | Already deleted on GitHub | Prune |
| `origin/narrative-reframe` | Merged | Delete |
| `origin/provocateur-r1` | Merged | Delete |
| `origin/reviewer-b-round5` | Merged | Delete |
| `origin/workflow-update` | Already deleted on GitHub | Prune |
| `origin/fix-highlights-coupling` | Merged | Delete |

### Worktrees
Only the main worktree exists. **Previous cleanup was thorough.** ✅

### Recommended actions:
```powershell
# Delete 9 merged local branches
git branch -d add-semester-break branch-cleanup fix-highlights-coupling geometry-and-modal instruction-architecture revision-round5 semester-1-break submission-fixes-v2 winter-break-overhaul

# Prune stale remote-tracking refs
git remote prune origin

# Delete remaining stale remote branches
git push origin --delete catch-up-log consistency-audit-r1 gas-pocket-paper-draft narrative-reframe provocateur-r1 reviewer-b-round5 fix-highlights-coupling
```

---

## Check 7: Paper Status — 🟡 COMPILES CLEAN, CONTENT ISSUES REMAIN

### Compilation
```
Output written on main.pdf (37 pages, 634,887 bytes)
```

| Metric | Value |
|--------|-------|
| Page count | **37** (review double-spaced format) |
| File size | 634 KB |
| LaTeX errors | **0** |
| Undefined references | **0** |
| Missing citations | **0** |
| BibTeX warnings | 1 (empty `pages` in `vonGierke2002`) |
| Overfull vbox | 2 (page break — cosmetic) |
| Hyperref warnings | 12 (Unicode tokens — cosmetic) |

### Orphaned .tex files (not included in main.tex)
| File | TODOs | Status |
|------|:---:|--------|
| `background.tex` | 7 | Never included — legacy scaffold |
| `methods.tex` | 5 | Never included — superseded by `section2_formulation.tex` |
| `historical-notes.tex` | 0 | Content integrated into introduction |
| `dimensional_analysis.tex` | 0 | Candidate for Paper 3 or integration |

### Review Status (Round 5)

| Reviewer | Verdict | Key Issues |
|----------|---------|------------|
| **A** | **ACCEPT** (minor corrections) | M1: Coupling ratio appears as 3–4 different values. 8 minor editorial items. |
| **B** | **MAJOR REVISION** | F1: Modal participation Γ₂ missing from paper (code exists). M1–M5: coupling ratio inconsistency, Table 4 formula wrong, supp. arithmetic errors, UQ labelling, code defaults mismatch. |
| **C** | (Last reviewed R4) | Identified parameter inconsistencies — mostly fixed in R5. |

### Critical paper issues remaining:

**1. Modal participation factor (Reviewer B F1) — BLOCKING**
- `src/analytical/modal_participation.py` computes Γ₂ ≈ 0.48 for ~33% constraint
- Code includes full gap budget analysis closing the theory-vs-ISO discrepancy
- **None of this is written into the paper.** All mechanical displacements are
  overstated by ~2×.
- Fix: Add subsection to §2.5, incorporate Γ₂ into Eq. 17, propagate through tables

**2. Coupling ratio inconsistency (Reviewers A M1, B M1) — BLOCKING**
- R appears as: 4.6×10⁴ (abstract), 6.6×10⁴ (Eq. 26), ~22,000 (Fig. 5a),
  7.7×10³ (Table 9), 10³–10⁵ (conclusion)
- Need: one canonical definition, one canonical value, used consistently throughout

**3. Code defaults mismatch (Reviewer B M5) — SHOULD FIX**
- `AbdominalModelV2` default parameters differ from Table 1 canonical values
- Readers following Data Availability instructions will get wrong numbers

**4. Supplementary arithmetic (Reviewer B M3) — EASY FIX**
- f₀ ≈ 2900 Hz (should be ~2500 Hz) — transcription error
- k_shell ≈ 2.3×10⁵ (should be ~1.5×10⁵) — parameter error

**5. Table 4 caption formula (Reviewer B M2) — EASY FIX**
- Formula gives 9.4×10⁷, not 13.4. Numerical ratio is correct; formula is wrong.

---

## Check 8: Research Logs — ✅ COMPREHENSIVE

**32 log files** spanning the entire project history.

### Most recent logs (chronological):
| Log | Content | Status |
|-----|---------|--------|
| `reviewer-a-round5.md` | **ACCEPT** with minor corrections | Current |
| `reviewer-b-round5.md` | **MAJOR REVISION** — Γ₂ missing, ratio inconsistency | Current |
| `reviewer-c-round4.md` | Last C review; param issues (mostly fixed) | Current |
| `lab-meeting-2026-03-27.md` | Lab Meeting #1 — comprehensive audit | Historical |
| `2026-03-27T0710-submission-checklist.md` | JSV format check | Current |

### Coverage assessment:
- ✅ All review rounds (1–5) documented for all reviewers
- ✅ All major analyses have logs with quantitative results
- ✅ Consistency audits documented
- ✅ Paper snapshots accompany relevant logs
- ⚠️ No log yet for PR #41 (geometry-and-modal) — the most recent merge

---

## RESEARCH-VISION.md — 🟡 PARTIALLY STALE

| Section | Status | Issue |
|---------|--------|-------|
| Paper 1 status | ⚠️ **Stale** | Says "Draft at 31 pages, under internal review (Round 4)." Reality: 37 pages, Round 5 complete, Reviewer A says ACCEPT |
| Paper 2 status | ⚠️ **Stale** | Says "Needs its own paper draft." Reality: Draft is COMPLETE in `paper2-gas-pockets/` with figures |
| Paper 3 status | ⚠️ **Stale** | Says "Agent running." Reality: Analysis merged, .tex file exists |
| Ideas Backlog | ⚠️ **Stale** | Multiple items checked off in PRs but still listed as unchecked |
| Research Questions | ✅ Current | M2 gap discussion still relevant |

---

## Blockers & Risks

### 🔴 BLOCKER: Modal Participation Factor Not in Paper Text

**Severity:** Paper is unpublishable without it (Reviewer B F1).
**Effort:** Medium — code is done, need ~2 paragraphs + table updates.
**Impact:** Changes all mechanical displacements by factor of ~0.48,
changes coupling ratio from ~6.6×10⁴ to ~3.2×10⁴. Qualitative conclusion
unchanged (still 10⁴ >> 1). Also closes the M2 gap with ISO data.

### 🔴 BLOCKER: Coupling Ratio Inconsistency

**Severity:** Both remaining reviewers flagged this. Must be one number.
**Effort:** Low — pick canonical comparison, grep-and-replace throughout.
**Impact:** Cosmetic but credibility-destroying if not fixed.

### 🟡 RISK: Code Defaults Don't Match Paper

**Severity:** Reproducibility concern. Any reader running the code gets wrong
numbers.
**Effort:** Trivial — update 7 default values in two Python files.
**Impact:** Would cause a reject from Reviewer C if they re-run code.

---

## Strategic Observations

### 1. We Are One Revision From Submission

Reviewer A said ACCEPT. Reviewer B's issues are all addressable without new
research. The modal participation write-up is the biggest task, but the code
and numbers exist. This is a 1-session editing job.

### 2. The Review Panel Has Proven Its Value

Five rounds of internal review caught every issue that matters. The convergence
between Reviewer A and B on the coupling ratio inconsistency demonstrates the
panel is functioning as real peer review. Keep using it.

### 3. Paper Has Grown From 31 to 37 Pages

The additions (broader applications, historical context, modal participation
table, geometry robustness) have pushed the paper to 37 review-format pages.
This is within JSV norms but at the upper end. Consider whether anything
can be trimmed or moved to supplementary.

### 4. Infrastructure Is Clean

Lab Meeting #1 found 22 stale local branches, 12 worktrees, orphaned .tex files,
and significant documentation drift. Most of this has been cleaned up. The
remaining 9 merged local branches and 8 stale remote branches are cosmetic.
The source tree confusion (src/browntone vs src/analytical) persists but is
well-documented.

### 5. Ideas Backlog Is Appropriately Parked

One scout report exists with 10 ideas. Paper 2 has a complete draft. Paper 3
analysis is done. Bladder resonance project is created. None of these should
be touched until Paper 1 submits. The restraint is correct.

### 6. Three Stale Skills Reference Legacy Code

`run-simulation.md`, `mesh-convergence.md`, and `generate-figures.md`
(standalone) all reference the never-used `browntone.fem`/`browntone.mesh`
FEniCSx pipeline. These will confuse any agent that reads them. They should
be deleted — the proper skill directories supersede them.

---

## Recommendations for PI

### Immediate — Next Session (Gets Paper to Submission)

1. **Write up the modal participation factor** (Reviewer B F1)
   - Add §2.5.1 or expand §2.5: define Γₙ, state Γ₂ ≈ 0.48 for ~33% constraint
   - Modify Eq. 17: ξ_mech = Γ₂ × x_base × H_rel
   - Recompute all mechanical displacement tables with Γ₂
   - Add the gap budget analysis (closes M2 with ISO data)
   - **This is the #1 priority.**

2. **Fix coupling ratio globally** (Reviewers A M1, B M1)
   - Choose: R = ξ_mech(0.5 m/s², Γ₂=0.48) / ξ_air(120 dB, energy) as canonical
   - Compute once: R ≈ 3,243 × 0.48 / 0.014 ≈ 1.1 × 10⁵ (or recompute precisely)
   - Use this ONE value in abstract, introduction, Eq. 26, conclusion
   - Use Monte Carlo range as uncertainty band
   - Give Table 9's geometric ratio a different symbol (e.g., R_geom)

3. **Fix supplementary arithmetic** (Reviewer B M3)
   - f₀ ≈ 2900 → ~2500 Hz
   - k_shell ≈ 2.3×10⁵ → ~1.5×10⁵ Pa/m

4. **Fix Table 4 caption formula** (Reviewer B M2)
   - Remove the wrong formula; state the 13.4× ratio as numerical result

5. **Update code defaults** (Reviewer B M5)
   - Change AbdominalModelV2 defaults to canonical values, OR
   - Add `@classmethod canonical()` that returns the paper's parameter set

### Short Term — After Revision

6. **Run Reviewer B Round 6** to verify fixes before submission
7. **Run consistency auditor** on final paper
8. **Final compilation + JSV checklist** (highlights ≤85 chars, abstract ≤200 words)

### Housekeeping — Can Be Done Anytime

9. **Delete 9 merged local branches:**
   `add-semester-break, branch-cleanup, fix-highlights-coupling, geometry-and-modal, instruction-architecture, revision-round5, semester-1-break, submission-fixes-v2, winter-break-overhaul`

10. **Delete stale remote branches:**
    `catch-up-log, consistency-audit-r1, gas-pocket-paper-draft, narrative-reframe, provocateur-r1, reviewer-b-round5, fix-highlights-coupling`

11. **Prune remote-tracking refs:** `git remote prune origin`

12. **Delete 3 stale standalone skill files:**
    `generate-figures.md, run-simulation.md, mesh-convergence.md`

13. **Update copilot-instructions.md:**
    - Publication pipeline: 31pp → 37pp
    - M2 gap: "closed" → "code done, paper write-up pending"
    - Add semester-break to skills table

14. **Update RESEARCH-VISION.md:**
    - Paper 1: 37pp, Round 5 complete, Reviewer A ACCEPT
    - Paper 2: Draft complete
    - Paper 3: Analysis merged
    - Check off completed backlog items

### After Paper 1 Submission

15. Run review panel on Paper 2 (gas pockets, JASA)
16. Decide fate of `dimensional_analysis.tex` (Paper 3 vs integration)
17. Delete orphaned .tex files (`background.tex`, `methods.tex`, `historical-notes.tex`)
18. Resolve `src/browntone/` legacy tree (delete or consolidate)

---

## Ideas That Emerged

1. **Canonical parameter classmethod**: Add `AbdominalModelV2.canonical()` that
   returns the exact paper parameter set. Eliminates default-mismatch class of
   bugs permanently. Could also read from a `params.yaml` shared with LaTeX.

2. **Coupling ratio taxonomy**: The paper uses "coupling ratio" for at least 3
   different quantities (full displacement ratio, geometric penalty, dimensional
   scaling). Giving each a distinct symbol (R, R_geom, Π_R) would prevent the
   inconsistency from recurring.

3. **Modal participation as Paper 1's closing contribution**: The gap budget
   analysis (theory → Γ₂ correction → nonlinear → ISO match) is actually a
   strong narrative closer. Frame it as: "our framework predicts ISO 2631
   comfort thresholds from first principles." This elevates the paper from
   "debunking the brown note" to "predictive biomechanical modelling."

4. **Reviewer C Round 5**: Reviewer C hasn't reviewed the R5 paper. Before
   submission, a quick Reviewer C pass to verify the now-fixed parameter
   consistency would catch any residual mismatches.

---

## Summary Scoreboard

| Area | Score | Notes |
|------|:---:|-------|
| README.md | ✅ A | Accurate and comprehensive |
| copilot-instructions.md | 🟡 B+ | 4 minor stale items |
| Agent definitions | ✅ A | All 16 current, well-differentiated |
| Skill definitions | 🟡 B | 3 stale legacy files to delete |
| Test suite | ✅ A+ | 118/118, 14s, no flakes |
| Git hygiene | 🟡 B- | 9+8 stale branches, 0 worktrees (good) |
| Paper compilation | ✅ A | 37pp, 0 errors, 0 undefined refs |
| Paper content | 🟡 B | 2 blocking issues (Γ₂, ratio) |
| Research logs | ✅ A | Comprehensive, all rounds documented |
| RESEARCH-VISION.md | 🟡 B- | Multiple stale status claims |
| Strategic focus | ✅ A | Correctly parked all non-Paper-1 work |

**Overall project health: GOOD — one focused session from submission-ready.**

---

*Meeting adjourned. Next meeting should follow the Γ₂ revision + Reviewer B R6.*
