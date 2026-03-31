# P9 minor revision and P10 theorem upgrade — 2026-03-31T1700

**Author**: Opus
**Branch**: research-log-1700
**PR**: #319

## Summary
This session converted the lab's two open theory manuscripts into much stronger scientific objects. Across **10 merged PRs** (**#309-#318**), Paper 9 moved from a vulnerable reviewer-facing draft to a **submission-ready minor revision**, while Paper 10 moved from a manifesto-style synthesis to a **stand-alone theorem paper** with proofs, figures, and a more credible *Proceedings of the Royal Society A* voice.

The decisive numerical result was that the previously observed positive spherical intercept is not physical. The new sigma-floor investigation showed that the exact sphere satisfies **\(\sigma_3(0)=0\)**, while the finite Ritz intercept grows with basis size, forcing a full rewrite of the near-sphere story in both Paper 9 and Paper 10.

## Key Findings
- **Throughput**: **10 PRs** merged in this segment (**#309-#318**). Of these, **8** directly advanced Paper 9 or Paper 10 (**#309, #312, #313, #314, #315, #316, #317, #318** with Paper 9 taking **5** revision PRs and Paper 10 taking **3** substantive PRs), **1** performed supporting code cleanup (**#310**), and **1** fixed the Paper 5 JASA template (**#311**).
- **Ritz artefact identified quantitatively**: the spherical intercept reported by the finite Ritz model grows from approximately **0.006** to **0.011** to **0.018** when the basis is enlarged from **3** to **5** to **7** modes, so it is not converging to a physical constant. The correct physics is **\(\sigma_3(0)=0\)** at the exact sphere, and the positive discrete intercept is a symmetry-breaking discretisation artefact. See `scripts/sigma0_analysis.py:236-239`, `scripts/sigma0_analysis.py:386-395`, and `papers/paper9-lifting-theorem/sections/results.tex:71-83`.
- **Paper 9 reviewer trajectory improved materially**: Reviewer B's sequence moved from **R1 MAJOR** to **R2 MAJOR** to **R3 MAJOR** to **R4 MINOR REVISION**, closing the segment at **MINOR REVISION** rather than the earlier `revision_needed` state. This improvement was delivered through **5 Paper 9 PRs** in this segment: **#312, #313, #316, #318**, plus the scientific foundation laid by **#309**.
- **Paper 9 numerical message is now internally consistent**: the manuscript now states that the equivalent-sphere reduction is singular, the sphere satisfies **\(\sigma_3=0\)**, the canonical oblate point has **\(\kappa_\mathrm{oblate}=69.4\)**, and the tested prolate continuation reaches **\(\kappa_\mathrm{prolate}=156\)** at **\(c/a=1.5\)** with the broader tested prolate range staying within **156-244** rather than showing systematic lifting. See `papers/paper9-lifting-theorem/main.tex:23-38` and `papers/paper9-lifting-theorem/sections/conclusion.tex:11-19`.
- **Paper 10 changed genre, not just tone**: the capstone moved from **4 conjectures** to **4 formal results with proofs** plus a supporting excitation proposition. The core formal statements now include **rank collapse under scalar geometric reduction**, **identifiability lifting by oblate asphericity**, **regular near-spherical asymptotics**, and the forward-vs-inverse adequacy counterexample. See `papers/paper10-capstone/sections/theory.tex:110-112`, `papers/paper10-capstone/sections/theory.tex:189-191`, `papers/paper10-capstone/sections/theory.tex:274-276`, `papers/paper10-capstone/sections/theory.tex:332-334`, and `papers/paper10-capstone/sections/theory.tex:416-445`.
- **Paper 10 now has publication-grade visual support**: **5 figures** were generated and integrated — `fig_condition_landscape`, `fig_cross_application`, `fig_forward_neq_inverse`, `fig_master_unification`, and `fig_three_jobs` — each in both **PDF** and **PNG** form under `papers/paper10-capstone/figures/`.
- **Cross-paper quantitative synthesis is now explicit**: the capstone now anchors its inverse-problem story with the severe equivalent-sphere conditioning scale **\(\kappa_\mathrm{sphere}\approx 1.37\times10^{10}\)**, the canonical oblate value **69.4**, and the corrected asymptotic law **\(\sigma_3(\varepsilon)=\lambda_1\varepsilon^2+O(\varepsilon^4)\)** rather than a finite physical floor. See `papers/paper10-capstone/sections/results.tex:191-192`, `papers/paper10-capstone/sections/results.tex:245-246`, and `papers/paper10-capstone/main.tex:83-91`.
- **Portfolio status improved**: Papers **1-8** remained `submission_ready` with **no change**; Paper **9** moved from `revision_needed` to **`submission_ready`** after **7 total revision PRs** across the broader cycle and closed this segment at **minor revision**; Paper **10** moved from **draft manifesto** to **draft_complete (revised)** as a theorem paper with figures.
- **Validation held throughout**: the repository remained green at **487/487 passing tests** throughout the segment, with no reported regressions during the PR sequence.

## Changes Made
- Created `docs/research-logs/2026-03-31T1700-p9-p10-major-advances.md`.
- Created companion snapshot `docs/research-logs/2026-03-31T1700-paper-snapshot.pdf` from `papers/paper10-capstone/main.pdf`.
- Recorded the sigma-floor investigation in `scripts/sigma0_analysis.py`, which established the non-physical nature of the Ritz spherical intercept and supplied the **3/5/7-mode** comparison that underpinned the Paper 9 and Paper 10 corrections.
- Recorded the Paper 9 code-cleanup context in `src/analytical/power_law_proof.py` and `src/analytical/universality.py`, where the docstrings and module framing now reflect the death of the old universality claim.
- Recorded the Paper 9 revision work in `papers/paper9-lifting-theorem/main.tex` and `papers/paper9-lifting-theorem/sections/{problem_setup,results,discussion,conclusion}.tex`, including the corrected statement **\(\sigma_3(0)=0\)**, the clarified prolate branch definition, the unified eccentricity notation, the basis-size caveat, and the revised singular-value presentation.
- Recorded the Paper 10 theorem upgrade in `papers/paper10-capstone/main.tex` and `papers/paper10-capstone/sections/{background,theory,results,discussion,conclusion}.tex`, where the capstone now presents formal results rather than conjectural framing.
- Recorded generation of **5 publication-quality Paper 10 figures** under `papers/paper10-capstone/figures/`.
- Recorded the supporting template repair in `papers/paper5-borborygmi/main.tex`, where the JASA manuscript was switched from `elsarticle` to `article`.

## Issues Identified
- **MAJOR**: Paper 10 is now intellectually coherent, but it is still not yet `submission_ready`. Reviewer A's first round remained **MAJOR REVISION**, Dietrich's verdict was still **"Not yet Proc Roy Soc A — needs one hard new thing"**, and round-2 review is still in progress.
- **MINOR**: Paper 9 has reached **MINOR REVISION** rather than acceptance. The scientific core is now stable, but one more tight response-to-reviewers pass may still be needed before final external closure.
- **MINOR**: The corrected asymptotic story depends on saying explicitly that the positive spherical intercept was a **Ritz artefact**, not a physical floor. Any surviving stale text in notes, talks, or future drafts that reifies **\(\sigma_0>0\)** as physics would immediately reintroduce inconsistency.

## Next Steps
- Finish Paper 10 review round 2 and determine whether the current four-theorem package already contains the "one hard new thing" Dietrich asked for or whether a further theorem-strengthening pass is required.
- Preserve the corrected near-sphere language across the programme: the exact sphere should continue to be described as **singular** with **\(\sigma_3(0)=0\)**, and any finite discrete intercept should be labelled as a **basis artefact**.
- Use Paper 9's new **MINOR REVISION** state to prepare the final response package promptly while reviewer context is still fresh.
- Keep Paper 10's stand-alone presentation strong enough for external readers who have not read Papers 1-9, since the capstone must now function as a paper rather than an internal manifesto.
