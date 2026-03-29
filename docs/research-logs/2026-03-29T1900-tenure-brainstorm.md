# Tenure Portfolio Brainstorming — 2026-03-29

**Author**: Chief of Staff  
**Branch**: log-tenure-brainstorm  
**PR**: #186

## Summary
A tenure-portfolio brainstorming session ran from approximately 18:00 to 19:30 UTC on 2026-03-29, with 8 participants: PI (Opus), Dietrich (coffee-machine-guru), Provocateur, Research Scout, Brainstorm Agent, and Reviewers A, B, and C. The purpose was to identify a genuinely flagship paper for the programme after the existing Papers 1–6 were criticised as effectively being 'one equation, six organs'.

The session proceeded in 3 phases: (1) 4 parallel advisory inputs, (2) synthesis into 6 candidate papers, and (3) a 4-person review panel. The final outcome was a two-paper flagship strategy: **Paper 7 = 'Can You Hear the Ripeness?'** on watermelon non-destructive testing (NDT) via shell-resonance inversion, and **Paper 8 = 'Can You Hear the Shape of an Organ?'** on practical identifiability for inverse shell problems in the spirit of Kac.

Quantitatively, the session narrowed 20 brainstormed ideas to 6 serious candidates, then to 2 selected papers. Watermelon NDT was judged the strongest near-term flagship because it closes the experimental gap and reuses approximately 85% of the existing codebase with an estimated 3–5 agent-hours of development. The Kac paper was retained as the mathematically deeper companion project, with an estimated 12–18 agent-hours of development.

## Key Findings
### Advisory phase
- **Dietrich** identified inverse vibroacoustic elastography as the 10× opportunity and argued that the forward model is analytically invertible because \(f_2^2\) is linear in \(E\), with total Sobol sensitivity **S_T = 0.86** for stiffness.
- **Provocateur** mounted the strongest critique of the programme: 'six papers, one equation, zero experiments'. He identified **3 core weaknesses**: no experiments, one method, and no inverse problems.
- **Research Scout** reviewed the Ig Nobel → Nobel pipeline and ranked new directions with **watermelon ripeness #1**, **stethoscope acoustics #2**, and **chest percussion #3**, while surveying **10 additional ideas**.
- **Brainstorm Agent** generated **20 candidate ideas** with feasibility/impact scoring. The top-ranked ideas were **watermelon (#1)**, **Kac-style viscoelastic drum identifiability (#2)**, and **cat purr resonance (#4)**.

### Candidate shortlist
The advisory inputs were synthesised into **6 candidates**:
1. **Can You Hear the Shape of an Organ?** — Kac's theorem for viscoelastic shells
2. **Can You Hear the Ripeness?** — watermelon acoustic NDT
3. **Auenbrugger's Drum** — chest percussion physics
4. **The Belly Speaker** — non-invasive vibroacoustic elastography
5. **What Killed the Whale?** — blue whale whole-body vibration reception
6. **Can You Hear a Wall Crack?** — acoustic-emission precursors

### Review panel results
| Candidate | Reviewer A | Provocateur | Reviewer B | Reviewer C |
|---|---|---|---|---|
| C1 Kac | 🥇 FLAGSHIP | 🥇 FLAGSHIP | ❌ KILL | 68/100 |
| C2 Watermelon | 🥉 later | 🥇 alt | ✅ ONLY viable | 92/100 |
| C3 Percussion | MAYBE | FILLER | ❌ KILL | 35/100 |
| C4 Elastography | PASS | SUPPORT | ❌ KILL | 78/100 |
| C5 Whale | 🥈 PURSUE | DISTRACTION | ⚠️ RISKY | 55/100 |
| C6 Wall crack | PASS | CONDITIONAL | ❌ KILL | 10/100 |

### Watermelon inversion results
Reviewer C ran the code and found that the watermelon model is unusually clean and well-conditioned:
- **Ripe rind modulus** \(E_{rind} = 50\) MPa → predicted **\(f_2 = 84.4\) Hz**, consistent with the literature range of **80–160 Hz**.
- **Unripe rind modulus** \(E_{rind} = 200\) MPa → predicted **\(f_2 = 168.7\) Hz**, consistent with the literature range of **160–250 Hz**.
- The ratio **\(f_2^2/E = 142.31\ \text{Hz}^2/\text{MPa}\)** was exactly constant at **0.00% variation** when \(P_{iap}=0\).
- Error propagation is simple but non-trivial: **5% frequency error → 10% modulus error**, i.e. **2× amplification** in the inverse map.
- An early concern that rind modulus should be only 'several MPa' was shown to be wrong; the physically relevant range is **50–200 MPa**.
- Reviewer C described the inversion condition number as **1.0**, effectively perfect for the chosen formulation.

### Kac identifiability results
The Kac-style inverse problem survived review, but only after reframing from rigorous uniqueness to practical identifiability:
- **Sphere model Jacobian condition number**: **1.12 × 10^10**, indicating a rank-deficient or nearly rank-deficient inverse problem.
- **Ritz model Jacobian condition number**: **83.5**, indicating a full-rank and practically identifiable inverse map.
- The key methodological result is that **oblate geometry breaks the degeneracy** that blocks inversion on spheres.
- Reviewer B's core criticism was that the original uniqueness claim was false because the forward map has degree **≥3** and is therefore not injective in the proposed sense.
- The revised interpretation is that the publishable result is not a rigorous uniqueness theorem, but a **practical identifiability finding** for physically relevant shell models.

### Strategic decisions taken
1. **Paper 7 selected**: *Can You Hear the Ripeness?* — watermelon NDT via shell-resonance inversion  
   - Target venue: **Postharvest Biology and Technology** or **PNAS**  
   - Estimated development: **3–5 agent-hours**  
   - Expected code reuse: **85%**  
   - Status: **scaffold agent launched**
2. **Paper 8 selected**: *Can You Hear the Shape of an Organ?* — practical identifiability of inverse shell problems  
   - Target venue: **Inverse Problems** or **Proceedings of the Royal Society A**  
   - Estimated development: **12–18 agent-hours**  
   - Status: **queued after Paper 7**
3. **Portfolio strategy**: the **Watermelon + Kac** pairing was chosen because together they address the programme's **3 main weaknesses** identified by Provocateur: no experiments, one method, and no inverse problems.

### Additional session updates
- **Paper 6 major fix merged** as **PR #183**, correcting the floor-vibration issue.
- **13 new tests** were added, bringing the total to **272 tests**.
- **Paper 6 Reviewer B R2** improved to **MINOR REVISION** from **MAJOR**, with **4 minor issues** still remaining.
- **Paper 1** received a bibliography fix (`vonGierke2002` pages field) and a figure-format correction from **PNG to PDF** for the Sobol figure.

## Changes Made
- Recorded the flagship-paper selection session as a formal research log.
- Captured the full decision trail from **4 advisory inputs** through **6 candidates** to **2 selected papers**.
- Preserved the quantitative basis for both selected directions, including watermelon frequency predictions, inverse error amplification, and Kac identifiability condition numbers.
- No paper manuscript or analysis code was modified in this log-only update, so **no companion PDF snapshot was required** for this entry.

## Issues Identified
- The existing six-paper portfolio was judged vulnerable to the critique that it is effectively **one method applied repeatedly**, without an experimental anchor or a convincing inverse problem.
- Reviewer B rejected several candidate directions on technical grounds:
  - **Kac**: the original uniqueness framing was too strong.
  - **Percussion**: wrong physics, because impulse excitation is not equivalent to steady-state forcing.
  - **Elastography**: circular validation risk.
  - **Wall crack**: wrong laboratory context for the programme.
- The Kac paper remains viable only if framed around **practical identifiability** rather than a strict uniqueness theorem.
- The watermelon project is strategically stronger in the short term, but still depends on disciplined validation against published data ranges rather than overclaiming.

## Next Steps
1. Develop **Paper 7** first: scaffold the manuscript, implement the forward and inverse watermelon models, and validate predictions against the published ripeness-frequency ranges.
2. Reframe **Paper 8** explicitly around practical identifiability in oblate shells, using the sphere-versus-Ritz conditioning result as the central finding.
3. Preserve the strategic pairing: use **Watermelon** to close the experimental gap and **Kac** to add mathematical depth to the tenure narrative.
4. Finish the remaining **4 minor Paper 6 issues** from Reviewer B Round 2.
5. Carry the **272-test** baseline forward into the next development cycle.
