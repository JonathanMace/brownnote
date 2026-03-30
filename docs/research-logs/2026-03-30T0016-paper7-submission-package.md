# Paper 7 submission package

- **Date/time:** 2026-03-30 00:16
- **Paper:** Paper 7 — *Can You Hear the Ripeness?*
- **Scope:** Submission-package audit and completion for `papers/paper7-watermelon/`

## Changes made

1. Created `papers/paper7-watermelon/submission/` and populated it with:
   - `manuscript.pdf`
   - `cover-letter.pdf`
   - `highlights.txt`
2. Added `papers/paper7-watermelon/cover-letter.tex` and compiled `cover-letter.pdf`.
3. Added `papers/paper7-watermelon/highlights.txt` with 5 submission bullets.
4. Recompiled `papers/paper7-watermelon/main.tex` and created the required snapshot
   `papers/paper7-watermelon/drafts/draft_2026-03-30_0014.pdf`.
5. Updated `README.md` so Paper 7 metadata now matches the manuscript title, venue, draft link, scope, and compiled page count.

## Quantitative results

- Recompiled manuscript output: **32 pages**, **760,621 bytes**
- Cover letter output: **1 page**, **81,742 bytes**
- Highlights file: **5 bullets**, **427 bytes**
- Submission bundle now contains **3 core artefacts**
- Baseline/after-change validation target: **487 pytest tests**

## Notes

The cover letter frames the work as a mechanistic shell-model contribution for
*Postharvest Biology and Technology*. It states that rind elastic modulus is the
dominant acoustic driver (**Sobol index \~0.54 ± 0.05**), that the inversion
from frequency to effective stiffness is closed-form when turgor pressure is
small, and that the model is **not** itself a direct ripeness classifier without
cultivar-specific calibration.
