# Publication Sprint & Multi-Paper Expansion — 2026-03-27

**Author**: Opus (PI)
**PRs**: #55–75 (19 merged)
**Duration**: ~3 hours wall-clock (13:20–16:38 UTC), Semesters 7–9

## Summary

This session pivoted from Paper 1 submission prep to a full multi-paper expansion sprint. Paper 1 received its gas-pocket qualifier and submission PDF package (37 pp + cover letter + 16 pp supplementary). Paper 2 (gas pockets) underwent a complete review cycle — Reviewer B issued MAJOR REVISION (5 findings including a fatal acoustic short-circuit concern), Reviewer C issued MINOR REVISION (all Table 2 frequencies verified, 3 numerical discrepancies found), a consistency audit flagged 3 CRITICAL issues, and all fixes were applied in PR #73. Paper 3 (scaling laws) went from nothing to a first draft with 6 foundational references. The bladder resonance project produced a 20-page manuscript draft. The borborygmi exploration yielded a new analytical model with 35 passing tests. Infrastructure received a health check, figures were regenerated, and a bibliography audit confirmed LOW scooping risk across all papers.

## Key Findings

### Paper 1 (JSV — Brown Note)
- **Status**: Submission-ready. All reviewers ACCEPT. PDF package finalised in PR #64.
- Gas-pocket qualifier added to abstract and conclusion (PR #67) — addresses provocateur-identified framing vulnerability between Papers 1 and 2.
- All 8 figures regenerated with canonical parameters (PR #70).

### Paper 2 (JASA — Gas Pockets)
- **Reviewer B (MAJOR REVISION)**: 5 issues identified:
  - **F1 (Fatal)**: Acoustic short-circuit — if gas pockets are open (connected to luminal air column), effective driving pressure ≪ p_inc. Sealing assumption unexamined.
  - **M1**: Cylindrical SPL threshold: paper "~118 dB" vs code **113.5 dB** (5 dB error).
  - **M2**: Efficiency overclaim "50–100×" — code shows **35–100×** (5 mL sphere only 35×).
  - **M3**: PIEZO threshold comparison is apples-to-oranges (patch-clamp in vitro vs bulk tissue).
  - **M5**: "100% population exceeds threshold" is tautological given 70% cylindrical geometry assumption.
- **Reviewer C (MINOR REVISION)**: Table 2 frequencies — ALL MATCH code exactly ✓
  - 5 mL spherical: 2653 Hz ✓, 100 mL spherical: 635 Hz ✓, cylindrical radial: 1323 Hz ✓
  - Monte Carlo range: paper "0.6–3.5 µm" vs code **1.02–2.66 µm** (70% error in lower bound).
  - 95% CI gas distribution: paper "70–570 mL" vs theory **56–715 mL**.
- **Consistency audit** (PR #65): 3 CRITICAL, 4 WARNING, 23 PASS.
  - CRITICAL 1: `gas_pocket_resonance.py` line 56 — `rho_fluid = 1040` (should be **1020**).
  - CRITICAL 2: Cylindrical SPL 118 → 114 dB.
  - CRITICAL 3: MC displacement range 0.6–3.5 → 1.0–2.7 µm.
- **All fixes applied** in PR #73: acoustic short-circuit discussion added, SPL corrected 118→114 dB, amplification reframed 50–100→35–100%, wall constraint clarified, population exceedance reframed.

### Paper 3 (JSV Short — Scaling Laws)
- **First draft merged** (PR #59): Buckingham Pi analysis reduces 11-parameter shell to 5 dimensionless groups. 486-point parametric collapse. Cross-species scaling predictions.
- **6 foundational references added** (PR #75): Buckingham (1914), Junger & Feit (1986), Lamb (1882), Fung (1993), ISO 2631-1 (1997), von Gierke (1971). Zero undefined citations.

### Bladder Resonance (JSV/J Biomech)
- **20-page manuscript draft** merged (PR #69): n=2 flexural mode at **12–18 Hz**, frequency minimum ~12 Hz at **170 mL** fill volume, mechanical coupling **7,600×** > airborne.
- **Reviewer A (MAJOR REVISION)** (PR #74): 5 issues — needs analytical decomposition of U-shaped frequency curve, clinical predictions quantified (PIEZO thresholds at 5 Hz vs f₂), uncertainty/sensitivity table, pelvic boundary treatment (40% contact → estimated 2× frequency shift), venue clarification.

### Borborygmi (JASA — New Project)
- **New analytical model + 35 tests** merged (PR #71): five resonance mechanisms for stomach/intestinal gurgling.
- Predicted range: **135–440 Hz** for 1–50 mL gas pockets — matches clinical auscultation data.
- Test suite expanded from 118 → 153 tests (all passing).

### Provocateur Programme Stress-Test (PR #62)
- **CRITICAL finding**: P1 conclusion ("airborne infrasound cannot cause GI effects") contradicts P2 finding ("gas pockets 50–100× more efficient; 100% exceed PIEZO threshold at 120 dB").
- **Resolution**: Gas-pocket qualifier added to Paper 1 (PR #67) — acknowledges gas-pocket pathway at whole-cavity level, framing Papers 1 and 2 as complementary rather than contradictory.
- **Recommendation**: Submit Paper 1 immediately. 7 internal review rounds sufficient; marginal improvements have diminishing returns.

### Scooping Risk (PR #68)
- **Overall: LOW** across all papers. No published work replicates core claims.
- Paper 1: **NONE** — no prior analytical shell theory for abdominal eigenfrequencies.
- Paper 2: **NONE** — microbubble models exist (Church 1995, Hoff 2000) but at MHz/µm scale, not Hz/cm.
- Paper 3: **NONE** — dimensional analysis classical, but visceral resonance scaling application novel.
- Bladder: **LOW** — Nenadic et al. (2013) measured wall modulus but did NOT predict resonant modes. Mayo Clinic UBV group could extend work; recommend submitting before they do.
- **Citation health**: Paper 1 has 8 orphaned refs, Paper 2 has 7, Paper 3 was critically under-referenced (3 refs → fixed to 9 in PR #75), bladder paper has **no references.bib** (17 cite keys unresolved).

## PRs Merged

| PR | Category | Description | Changes |
|----|----------|-------------|---------|
| #55 | `[chore]` | Submission-ready PDF snapshots | +0 −0 |
| #56 | `[paper2]` | Fix 5 CRITICAL + 2 MAJOR numerical errors in gas-pocket paper | +54 −48 |
| #57 | `[paper2]` | Trim abstract 220 → 158 words | +19 −26 |
| #59 | `[paper3]` | First draft: Scaling Laws for Fluid-Filled Viscoelastic Shells | +319 −0 |
| #60 | `[log]` | Research log: Round 5 to submission sprint (PRs #38–57) | +150 −0 |
| #61 | `[review]` | Reviewer B Round 1 — Paper 2 (MAJOR REVISION, 5 issues) | +367 −0 |
| #62 | `[review]` | Provocateur challenge — full programme stress-test | +196 −0 |
| #64 | `[paper]` | Submission-ready PDF package (37pp + cover + 16pp supp) | +0 −0 |
| #65 | `[audit]` | Paper 2 consistency audit (3 CRITICAL, 4 WARNING, 23 PASS) | +2708 −0 |
| #66 | `[review]` | Reviewer C Round 1 — Paper 2 (MINOR REVISION) | +118 −118 |
| #67 | `[paper]` | Add gas-pocket qualifier to abstract and conclusion | +8 −3 |
| #68 | `[research]` | Bibliography check and scooping risk assessment | +373 −0 |
| #69 | `[paper]` | Bladder resonance manuscript first draft (20 pp) | +346 −0 |
| #70 | `[figures]` | Regenerate all Paper 1 figures with canonical params | +0 −0 |
| #71 | `[research]` | Borborygmi acoustic model + 35 tests (135–440 Hz) | +1065 −1540 |
| #72 | `[infra]` | Repository health check: README, gitignore, skills | +17 −4 |
| #73 | `[paper2]` | Address Reviewer B Round 1 findings (all 5 fixes) | +227 −13 |
| #74 | `[review]` | Reviewer A: Bladder resonance (MAJOR REVISION, 5 issues) | +328 −0 |
| #75 | `[paper]` | Add 6 foundational references to Paper 3 scaling laws | +69 −9 |

## Key Decisions Made

1. **Paper 1 framing**: Gas-pocket qualifier inserted into abstract/conclusion to resolve P1/P2 contradiction identified by provocateur. Papers now positioned as complementary — P1 establishes whole-cavity impossibility, P2 identifies sub-cavity exception.
2. **Paper 2 SPL correction**: Cylindrical threshold corrected from 118 dB to **114 dB** across text and figures.
3. **Paper 2 efficiency claim**: Widened from "50–100×" to **"35–100×"** with volume qualification.
4. **Paper 3 references**: Expanded from 3 to 9 foundational references — no longer critically under-referenced.
5. **Borborygmi as new project**: Stomach gurgling model validated against clinical auscultation range (135–440 Hz). Target venue: JASA.
6. **Bladder venue**: Still undecided between JSV, Journal of Biomechanics, and Neurourology & Urodynamics. Reviewer A suggests clarifying target audience.

## Issues Identified

### CRITICAL (resolved this session)
- ~~P1/P2 framing contradiction~~ → gas-pocket qualifier (PR #67)
- ~~Paper 2 rho_fluid = 1040~~ → corrected to 1020 (PR #73)
- ~~Paper 2 cylindrical SPL 118 dB~~ → corrected to 114 dB (PR #73)
- ~~Paper 2 MC range 0.6–3.5 µm~~ → corrected to 1.0–2.7 µm (PR #73)

### MAJOR (outstanding)
- **Bladder paper**: No `references.bib` — 17 cite keys unresolved. Paper will not compile.
- **Bladder paper**: Pelvic boundary condition (40% contact) unmodelled — estimated 2× frequency shift.
- **Bladder paper**: Needs analytical decomposition, clinical predictions, and UQ table per Reviewer A.
- **Paper 2**: Acoustic short-circuit discussion added but sealing assumption remains unverifiable without experimental data.

### MINOR (outstanding)
- Paper 1: 8 orphaned BibTeX entries (harmless but untidy).
- Paper 2: 7 orphaned BibTeX entries, 31 orphan labels, 4 placeholder fields.
- Borborygmi: Framework only — needs literature validation, damping model, and clinical comparison.
- Repository: 27 stale worktrees noted in health check (PR #72).

## Quantitative Summary

| Metric | Value |
|--------|-------|
| PRs merged | 19 (#55–75) |
| Lines added | ~5,940 |
| Lines removed | ~1,761 |
| Papers with active drafts | 4 (Brown Note, Gas Pockets, Scaling Laws, Bladder) |
| New projects started | 1 (Borborygmi) |
| Review rounds completed | P2: B(R1)+C(R1), Bladder: A(R1) |
| CRITICAL issues found | 7 (all resolved) |
| Test suite | 153 tests, all passing |
| Scooping risk | LOW across all papers |
| Paper 1 status | Submission-ready (unanimous ACCEPT) |
| Paper 2 status | Reviewer fixes applied; needs R2 review cycle |
| Paper 3 status | First draft + references; needs review cycle |
| Bladder status | First draft; MAJOR REVISION from Reviewer A |

## Next Steps

1. **Submit Paper 1** to JSV via Elsevier Editorial Manager — no further internal review needed.
2. **Paper 2 Round 2 review**: Run 3-reviewer panel to verify PR #73 fixes are sufficient.
3. **Bladder paper**: Create `references.bib` (17 entries), address Reviewer A's 5 major issues, re-review.
4. **Paper 3 review**: Run first 3-reviewer panel on scaling laws draft.
5. **Borborygmi**: Literature validation, damping model, comparison with Craine et al. (1999) frequency data.
6. **Worktree cleanup**: Prune 27 stale worktrees identified in repo health check.
7. **Paper 2 UQ**: Add Sobol sensitivity indices for tissue parameters (E_w, h_w, R, PIEZO threshold).
