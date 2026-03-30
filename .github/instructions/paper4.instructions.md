---
applyTo: "papers/paper4-bladder/**"
---

# Paper 4 — JSV (Bladder Resonance)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper4-bladder
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper4-bladder/main.pdf "papers/paper4-bladder/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 4 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Code lives in src/analytical/bladder_resonance.py.
Target: Journal of Sound and Vibration.
