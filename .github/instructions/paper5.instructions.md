---
applyTo: "projects/borborygmi/paper/**"
---

# Paper 5 — JASA (Borborygmi)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd projects/borborygmi/paper
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item projects/borborygmi/paper/main.pdf "projects/borborygmi/paper/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 5 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Code lives in src/analytical/borborygmi_model.py.
Target: Journal of the Acoustical Society of America.
