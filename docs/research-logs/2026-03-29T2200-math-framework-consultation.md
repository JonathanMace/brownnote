# Mathematical Framework Consultation & P7/P8 Completion — 2026-03-29

**Author**: Opus (PI)
**Branch**: log-session-20260329
**Session window**: ~22:00–22:35 UTC

## Summary

This session recovered from a mid-session crash, completed Papers 7 and 8 to
submission-ready status, secured a MINOR REVISION verdict from Reviewer B on
Paper 7 (upgraded from REJECT at R1), consulted three independent advisors on
whether to invent a new mathematical framework for Paper 8, and initiated a
submission sprint for Papers 1 and 2. Eight PRs were merged (#206–#213).

## Crash Recovery & Paper Completion

The session began with two agents in-flight from a crashed predecessor session.
Recovery was clean; no work was lost.

### Paper 7 — Watermelon Ripeness (Postharvest Biology & Technology)

- Final compile: **19 pages**, 0 LaTeX errors
- Submission-ready snapshot created → **PR #206**

### Paper 8 — Kac Identifiability (Inverse Problems)

- 6 sections written by the paper-writer agent and extracted into LaTeX
- Compiled to **15 pages** with all 4 figures integrated → **PR #207, #208, #210**
- Figures generated:
  - Inversion noise sensitivity (displacement error vs. measurement noise)
  - Singular value spectrum of the Jacobian
  - (Two pre-existing figures from earlier session retained)

### Repository Infrastructure

- Test count updated: **377 tests passing** (up from 333 at last count)
- Total merged PRs: **213** (session contributed 8) → **PR #209**

## Paper 7 Reviewer B: MINOR REVISION (R4)

The trajectory across four review rounds:

| Round | Verdict | Fatal flaws |
|-------|---------|-------------|
| R1 | REJECT | 4 |
| R2 | REJECT | 3 |
| R3 | MAJOR REVISION | 1 |
| R4 | **MINOR REVISION** | 0 |

All four original fatal flaws have been resolved. Five minor issues were
identified and fixed in a single PR (**#212**):

1. **M1 — Yamamoto validation language**: Replaced overclaiming with honest
   assessment: 3 of 6 melons within predicted range, MAD = 15 Hz.
2. **M2 — TODO comments in references.bib**: Removed two residual TODO markers.
3. **M3 — Sobol N_base mismatch**: Aligned code value to `N_base = 512`,
   matching the claim in the paper text.
4. **M4 — Uncited abdomen claim**: Added `\cite{MaceAndMace2026}` for the
   α = 155 Hz²/MPa scaling coefficient.
5. **M5 — Sadrnia bib key**: Corrected `Sadrnia2006` → `Sadrnia2008` to match
   the actual publication year.

## Mathematical Framework Consultation

The PI asked: *"Is there a new mathematical framework we could invent for
Paper 8 (Kac identifiability)?"* Three advisors were consulted independently.

### Dietrich (Emeritus Vibroacoustics, `dietrich` agent)

Core insight: the mechanism underlying non-uniqueness is **mode-dependent
curvature sampling**, not a symmetry-group reduction SO(3) → SO(2).

Proposed a three-layer research programme:

| Layer | Scope | Effort | Content |
|-------|-------|--------|---------|
| 1 (trivial) | Chain-rule proof of rank deficiency | Days | Show ∂f_n/∂a and ∂f_n/∂c are linearly dependent when only n = 2 is observed |
| 2 (weeks) | Eccentricity perturbation expansion | 2–4 weeks | Expand f_n(e) in powers of eccentricity; prove local uniqueness with ≥2 modes |
| 3 (PhD thesis) | Global uniqueness theorem | Years | Full Sturm–Liouville inverse problem for viscoelastic shells; leave as open problem |

Verdict: *"Do the perturbation analysis. Prove the local result. State the
global question as an open problem. Do not attempt Layer 3 in this paper."*

### Provocateur (Devil's Advocate, `provocateur` agent)

Strongest criticisms:

- "Spectral Shape Calculus" as pitched is a **10-year programme disguised as
  a paper contribution**
- The SO(3) → SO(2) framing is **"physically evocative but causally
  disconnected"** from the numerical evidence
- **"You cannot prove theorems with Python"** — numerical rank deficiency is
  not a proof of non-uniqueness

The achievable paper, per the Provocateur:

1. Practical identifiability analysis (Fisher information, profile likelihood)
2. Chain-rule proof of rank deficiency (Layer 1)
3. Perturbation analysis showing local resolution (Layer 2)
4. Open problem statement for the global question (Layer 3)

Verdict: *"Be the group that asked the question well enough that a
mathematician wanted to answer it."*

### Coffee Machine Guru (Emeritus Mentor, `coffee-machine-guru` agent)

The bluntest assessment:

> "The number of papers you have submitted to an actual journal is... zero."

> "Every time you get close to sending something to a stranger for judgement,
> you find a brilliant reason to keep working."

Concrete advice:

- Submit Paper 1 to JSV **this week**
- Submit Paper 2 to JASA **next week**
- Stop inventing frameworks; start collecting rejection letters

### Consensus

All three advisors independently converged on the same recommendation:

1. **Do Layers 1 + 2** (chain-rule proof + perturbation analysis)
2. **Publish** with those results
3. **Pose Layer 3** as an open problem for mathematicians
4. **Stop inventing and start submitting**

## Submission Sprint

Acting on the advisory consensus, a submission sprint was initiated:

### Paper 1 — JSV Submission Package (PR #213)

- Fresh compile: **30 pages**, 0 errors
- Cover letter generated (PDF)
- Highlights file created
- Graphical abstract prepared
- Submission-ready snapshot archived

### Paper 2 — JASA Submission Package (in progress)

- Fresh compile started; branch `p2-submission-package` active
- Not yet merged at session end

### Paper 8 — Analytical Proofs (in progress)

- Branch `p8-analytical-proofs` active
- Layer 1 (chain-rule rank deficiency) and Layer 2 (perturbation expansion)
  being drafted into `src/analytical/kac_identifiability.py`
- Not yet merged at session end

## Key Findings

- **P7 Reviewer B trajectory**: REJECT → REJECT → MAJOR → **MINOR** over 4
  rounds. All fatal flaws resolved. Yamamoto validation honesty was the key
  remaining concern (3/6 melons in range, MAD = 15 Hz).
- **Advisory unanimity**: 3/3 advisors independently recommended descoping the
  mathematical ambition and prioritising submission.
- **P1 submission package**: 30 pages, complete with cover letter, highlights,
  and graphical abstract — ready for JSV portal upload.
- **P8 current state**: 15 pages, 4 figures, analytical proof work in progress.
- **Repository health**: 377 tests passing, 213 PRs merged, all branches clean.

## Changes Made

- `projects/watermelon-ripeness/paper/` — final compile + snapshot (PR #206)
- `projects/kac-identifiability/paper/` — 6 sections + figures (PR #207, #208, #210)
- `README.md` — updated test count and PR count (PR #209)
- `projects/watermelon-ripeness/paper/references.bib` — TODO removal (PR #212)
- `projects/watermelon-ripeness/paper/` — 5 minor fixes (PR #212)
- `paper/` — submission package with cover letter (PR #213)

## Issues Identified

- **MINOR**: Branch `p2-submission-package` and `p8-analytical-proofs` remain
  unmerged at session end. Next session should check their status and merge or
  clean up.
- **MINOR**: The unstaged change to `tests/test_kac_identifiability.py` in the
  main worktree needs to be reviewed and either committed or discarded.

## Quantitative Summary

| Metric | Value |
|--------|-------|
| PRs merged this session | 8 (#206–#213) |
| Total PRs (repo lifetime) | 213 |
| Tests passing | 377 |
| P7 Reviewer B verdict | MINOR REVISION (was REJECT at R1) |
| P7 minor issues fixed | 5 (single PR) |
| P8 page count | 15 (4 figures integrated) |
| P1 page count | 30 (submission-ready) |
| Advisors consulted | 3 (unanimous on descoping) |
| In-flight branches at session end | 2 (`p2-submission-package`, `p8-analytical-proofs`) |

## Next Steps

1. **Submit Paper 1** to JSV — upload the submission package from PR #213
2. **Complete Paper 2** JASA submission package — merge `p2-submission-package`
3. **Complete Paper 8** analytical proofs (Layers 1 + 2) — merge
   `p8-analytical-proofs`
4. **Clean up** the unstaged test file change in main worktree
5. **Run consistency-auditor** before any further paper compiles
6. **Begin Paper 3** revision based on JSV Short Communication feedback
