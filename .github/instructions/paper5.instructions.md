---
applyTo: "papers/paper5-borborygmi/**"
---

# Paper 5 — JASA (Borborygmi)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper5-borborygmi
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper5-borborygmi/main.pdf "papers/paper5-borborygmi/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 5 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Code lives in src/analytical/borborygmi_model.py.
Target: Journal of the Acoustical Society of America.
