---
applyTo: "papers/paper1-brown-note/**"
---

# Paper 1 — Journal of Sound and Vibration

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper1-brown-note
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper1-brown-note/main.pdf "papers/paper1-brown-note/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 1 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English and canonical parameters from R3.
Target: Journal of Sound and Vibration (Elsevier).
