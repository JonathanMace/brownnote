---
applyTo: "paper6-sub-bass/**"
---

# Paper 6 — Journal of Sound and Vibration (Sub-Bass Coupling)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd paper6-sub-bass
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item paper6-sub-bass/main.pdf "paper6-sub-bass/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 6 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English and canonical parameters from R3.
Analytical code lives in `src/analytical/sub_bass_coupling.py`.
Target: Journal of Sound and Vibration (Elsevier).
