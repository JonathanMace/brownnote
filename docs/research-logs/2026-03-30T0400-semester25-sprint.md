# Semester 25 Sprint — 2026-03-30

**Author**: Opus (PI)
**Branch**: research-log-s25
**Session window**: Semester 25 (~03:00–04:00 UTC, 2026-03-30)

## Summary

A high-output session that addressed 11 external reviewer comments on Paper 1,
finalised the venue decision (JSV), prepared submission packages for Papers 1
and 2, completed a keystone rewrite of Paper 8, and delivered strategic
portfolio assets including a watermelon experiment protocol and review-article
scope. Seven PRs merged (#231–#237), test suite grew from 417 → 421 tests,
and consistency audit passed clean.

## Paper 1 — External Reviewer Feedback (PR #231)

An external professor reviewed Paper 1 and called it "brilliant" and "really
solid". All 11 specific comments were addressed in a single PR:

| # | Comment | Resolution |
|---|---------|------------|
| 1 | Table 2 E values lack citations | Added 4 citations for physiological range |
| 2 | Why n=2 and not n=1? | Clarified n=1 is rigid-body translation; n=2 is the lowest physical deformation mode |
| 3 | ISO 2631 validation rationale | Explicit validation rationale added to discussion |
| 4 | PIEZO introduced too late | Moved introduction earlier with mechanotransduction context |
| 5 | Effective E justification | Jones (1999) laminate theory citation added |
| 6 | Jupiter gravity claim | Footnote added: Jovian gravity = 24.8 m/s², labelled "rhetorical" |
| 7 | Γ₂ physical interpretation | Symmetry breaking by pelvis → Γ₂ = 0.48 explained |
| 8 | Figure 6 label overlap | TikZ labels repositioned for clarity |
| 9 | Duffing section accessibility | Section 5.6 rewritten for non-specialist readers |
| 10 | Organ structure homogeneity | Hashin–Shtrikman effective-medium citation added |
| 11 | PIEZO1/2 channel labels | Clarified in Table 3 with full nomenclature |

**Result**: P1 at 30 pages, all reviewer comments resolved, ready for submission.

## Venue Decision — JSV Primary

After evaluating candidate journals, JSV was selected as the primary venue for
Paper 1:

| Criterion | JSV | Proc R Soc A |
|-----------|-----|-------------|
| Impact factor | 4.9 | ~3.0 |
| Scope fit | Perfect | Good |
| Reformatting needed | Zero | Moderate |
| AI policy risk | Low (template exercise) | Moderate |
| Prestige | High | Higher (name only) |

**Decision**: JSV primary, Proc R Soc A as backup.

Additional submission preparation:

- **AI disclosure statement** added using Elsevier template
- **CRediT author contributions** updated:
  - Jonathan Mace: +Formal Analysis
  - Brian Mace: +Methodology
- **Brian's email** corrected to `b.mace@auckland.ac.nz`

## Submission Packages (PRs #235, #237)

### Paper 1 — JSV (PR #235)

- Cover letter drafted (addresses scope, novelty, and significance)
- Highlights file (5 bullet points per Elsevier spec)
- Reviewer suggestions list prepared
- Graphical abstract concept designed
- **Status**: Submission-ready pending Brian's final read

### Paper 2 — JASA (PR #237)

- Cover letter drafted for JASA format
- Highlights file created
- Reviewer suggestions prepared
- AI disclosure statement included
- **Status**: Submission-ready pending Brian's final read

## Paper 8 — Keystone Rewrite (PRs #232, #236)

### Content Rewrite (PR #232)

- Introduction rewritten to connect P8 to the broader programme (P1, P4, P7)
- Conclusion reframed around elastography applications
- Three **Volkov conjectures** formally stated:
  1. **Rate conjecture**: minimum number of modes scales with parameter count
  2. **Minimum modes conjecture**: ≥3 modes required for 6-parameter recovery
  3. **Universality conjecture**: identifiability structure is geometry-class invariant

### API Cleanup (PR #236)

- Cross-model interface standardised
- Bounds validation added to all inversion functions
- Convergence diagnostics integrated into the API
- **4 new regression tests** added → 421 total

### Reviewer B Verdict: MAJOR REVISION

Two fatal flaws identified:

| ID | Flaw | Description |
|----|------|-------------|
| F1 | Headline mismatch | Paper compares two *models* (sphere vs oblate) not two *geometries* — the claimed geometric insight is actually a modelling-choice artefact |
| F2 | Proposition 2 gap | Theory–numerics disconnect: the proposition is stated as proven but relies on numerical evidence only |

Seven major issues also logged (M1–M7) for future revision. These are
documented in the reviewer report and queued for the next P8 work cycle.

## Strategic Deliverables (PRs #233, #234)

### Portfolio Narrative (PR #233)

- 790-word public narrative of the research programme
- Press release draft prepared
- Elevator pitches (30-second and 2-minute versions)
- **Ig Nobel nomination** drafted (brown note hypothesis)

### Watermelon Experiment Protocol (PR #234)

Full benchtop experiment designed for watermelon ripeness detection:

| Parameter | Value |
|-----------|-------|
| Budget | $660 |
| Sample size | 18 melons (6 per ripeness stage) |
| Method | Microphone tap test |
| Predicted frequencies | See below |

**Predicted watermelon frequencies** (from `src/analytical/watermelon_model.py`):

| Ripeness stage | Predicted f₂ (Hz) |
|----------------|-------------------|
| Unripe | 203 |
| Turning | 147 |
| Ripe | 89.9 |
| Overripe | 46.4 |

### Review Article Scope

- Title: *"From Folklore to Framework"*
- Genuine gap in the literature confirmed — no existing review covers the
  physics of gut-sound folklore
- Target venues: JSV (review article track) or Physics of Life Reviews

## Consistency Audit

The consistency auditor was run and returned **PASS**:

- **0 critical issues**
- **3 warnings** — all fixed before session end
- Canonical parameters verified across code, paper tables, and in-text claims

## Quantitative Summary

| Metric | Value |
|--------|-------|
| PRs merged this session | 7 (#231–#237) |
| Tests passing | 421 (was 417) |
| New regression tests | 4 |
| P1 reviewer comments addressed | 11/11 |
| P1 page count | 30 |
| P8 κ_sphere | 1.37 × 10¹⁰ |
| P8 κ_oblate | 69.4 |
| P8 Reviewer B verdict | MAJOR REVISION (2 fatal flaws) |
| Watermelon f₂ (ripe) | 89.9 Hz |
| Watermelon f₂ (unripe) | 203 Hz |
| Portfolio narrative | 790 words |
| Experiment budget | $660 (18 melons) |
| Consistency audit | PASS (0 critical) |

## Changes Made

| PR | Scope | Content |
|----|-------|---------|
| #231 | P1 reviewer feedback | 11 comments addressed, citations added, sections rewritten |
| #232 | P8 keystone rewrite | Intro/conclusion reframed, 3 Volkov conjectures stated |
| #233 | Portfolio narrative | Public story, press release, elevator pitches, Ig Nobel nomination |
| #234 | Watermelon experiment | Protocol, prediction script, review-article scope |
| #235 | P1 submission package | Cover letter, highlights, reviewer suggestions, graphical abstract |
| #236 | P8 API cleanup | Cross-model interface, bounds validation, 4 regression tests |
| #237 | P2 submission package | Cover letter, highlights, reviewer suggestions, AI statement |

## Issues Identified

- **MAJOR**: P8 Reviewer B found 2 fatal flaws (F1: headline compares models
  not geometries; F2: Proposition 2 theory/numerics gap). These must be
  addressed before P8 can advance to submission.
- **MINOR**: P8 has 7 additional major issues (M1–M7) logged from Reviewer B
  that should be triaged in the next P8 session.
- **INFO**: Both P1 and P2 are submission-ready but await Brian's final read
  before portal upload.

## Next Steps

1. **Submit Paper 1** to JSV — upload after Brian's sign-off
2. **Submit Paper 2** to JASA — upload after Brian's sign-off
3. **Address P8 fatal flaws** — F1 (reframe headline around geometry) and F2
   (either prove Proposition 2 or downgrade to conjecture)
4. **Triage P8 M1–M7** — prioritise by severity and effort
5. **Run watermelon experiment** — procure 18 melons, execute tap-test protocol
6. **Draft review article** — "From Folklore to Framework" outline
7. **Run 3-reviewer panel** on P1/P2 submission packages as final gate
