---
applyTo: "papers/paper2-gas-pockets/**"
---

# Paper 2 — JASA (Gas Pocket Transduction)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper2-gas-pockets
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper2-gas-pockets/main.pdf "papers/paper2-gas-pockets/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 2 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Code lives in src/analytical/gas_pocket_detailed.py.
Target: Journal of the Acoustical Society of America.
