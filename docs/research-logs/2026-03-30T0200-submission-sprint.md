# Submission sprint — 2026-03-30T0200

**Author**: Opus
**Branch**: p1-r4-fix
**PR**: #261-#269

## Summary
The second half of this session turned into a concentrated submission sprint across Papers 1, 7, and 8. Nine additional PRs (#261-#269) merged, bringing the session total to 29, while Paper 8 closed all nine Reviewer B R6 items and Paper 1 moved materially closer to submission through theory, bibliography, and energy-budget corrections.

The net effect is a sharper portfolio split: Paper 7 is ready for human submission, Paper 1 now looks sendable after one more technical pass, and Paper 8 has narrowed from a diffuse revision burden to a small set of explicitly identified major issues.

## Key Findings
- **Throughput**: **9** further PRs merged (**#261-#269**), taking the session total to **29** merged PRs.
- **Paper 8, Round 7/8 progress**: PR **#261** resolved **all 9** Reviewer B items from R6. PR **#265** clarified **1** `\kappa_{\mathrm{floor}}` definition, documented the Ritz model, and added **1** prolate subsection in `papers/paper8-kac/sections/methodology.tex` and `papers/paper8-kac/sections/results.tex`. PR **#266** acknowledged oblate non-monotonicity and documented smootherstep blending tied to `src/analytical/oblate_spheroid_ritz.py`.
- **Paper 8 remaining blockers**: Reviewer B remains at **MAJOR**, but the blocking list is now down to **3** concrete issues: the `\sigma_0` identity claim, unmatched proof/manuscript paths, and residual monotonicity language. Reviewer A is also at **MAJOR** and wants the paper reframed around **practical identifiability**; Reviewer C is at **MAJOR**, agrees the numbers match, but still flags the Ritz/theory mismatch and the non-monotonicity story.
- **Paper 8 scientific decision**: `\sigma_0` has been retreated from a claimed asymptotic identity to an **empirical fit coefficient**. The R9 fix is in progress on that basis, which is a substantive interpretive retreat rather than a cosmetic wording change.
- **Paper 1 progress**: PR **#267** addressed **all 8** Reviewer B priorities from R3; PR **#268** aligned `src/analytical/energy_budget.py`; PR **#269** documented the Ritz offset in `papers/paper1-brown-note/sections/results.tex`; and PR **#262** repaired `papers/paper1-brown-note/references.bib`. Reviewer B improved from **REJECT -> REJECT -> MAJOR**.
- **Paper 1 external assessments**: Dietrich returned **SUBMIT**; the editor assessment improved from **Desk Reject** to **Send to Review**. That is the strongest Paper 1 venue-fit signal of the session.
- **Paper 7 status**: Reviewer A's final check returned **GO for submission**, and the overclaim fix has already been committed in `papers/paper7-watermelon/sections/discussion.tex` and related manuscript text. Paper 7 is now ready for human submission to *Postharvest Biology and Technology*.
- **Repository validation**: the cross-paper science consistency audit returned **PASS**, and the repository currently reports **487 passing tests**.

## Changes Made
- Created `docs/research-logs/2026-03-30T0200-submission-sprint.md`.
- Created companion snapshot `docs/research-logs/2026-03-30T0200-paper-snapshot.pdf` from `papers/paper1-brown-note/main.pdf` (**757202 bytes**).
- Recorded the merged session work spanning `papers/paper8-kac/main.tex`, `papers/paper8-kac/sections/methodology.tex`, `papers/paper8-kac/sections/results.tex`, `papers/paper8-kac/sections/discussion.tex`, `papers/paper1-brown-note/sections/section2_formulation.tex`, `papers/paper1-brown-note/sections/section4_coupling.tex`, `papers/paper1-brown-note/sections/results.tex`, `papers/paper1-brown-note/references.bib`, `src/analytical/energy_budget.py`, and `papers/paper7-watermelon/sections/discussion.tex`.

## Issues Identified
- **MAJOR**: Paper 8 still has **3** explicit Reviewer B blockers: the `\sigma_0` identity statement, unmatched proof/manuscript paths, and residual monotonicity claims.
- **MAJOR**: Paper 8 framing remains unstable until the manuscript fully adopts the practical-identifiability interpretation requested by Reviewer A and reconciles the Ritz/theory mismatch highlighted by Reviewer C.
- **MAJOR**: Paper 1 still needs one more technical pass on the factor-of-2 issue, the uncertainty-quantification contradiction, and the gas-pocket physics before final submission packaging.
- **MINOR**: Paper 7 is scientifically ready, but submission now depends on prompt human handoff rather than further model development.

## Next Steps
- Complete the Paper 8 R9 fix by treating `\sigma_0` consistently as an empirical fit coefficient, aligning proof and manuscript paths, and deleting the last monotonicity overclaims before another Reviewer B pass.
- Give Paper 1 one last targeted pass on the factor-of-2 point, the UQ contradiction, and the gas-pocket-physics wording, then refresh the submission package.
- Hand Paper 7 to the human submission workflow for *Postharvest Biology and Technology*.
