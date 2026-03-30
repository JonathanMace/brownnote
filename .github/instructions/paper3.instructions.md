---
applyTo: "papers/paper3-scaling-laws/**"
---

# Paper 3 — JSV Short Communication (Scaling Laws)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper3-scaling-laws
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper3-scaling-laws/main.pdf "papers/paper3-scaling-laws/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 3 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English and canonical parameters from R3.
Target: Journal of Sound and Vibration — Short Communication.
