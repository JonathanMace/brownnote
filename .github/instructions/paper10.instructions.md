---
applyTo: "papers/paper10-capstone/**"
---

# Paper 10 — Proceedings of the Royal Society A (Capstone)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper10-capstone
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper10-capstone/main.pdf "papers/paper10-capstone/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 10 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Use `\SI{value}{unit}` for quantities.
Backbone papers: P1 (brown note), P7 (watermelon), P8 (Kac identifiability).
Target: Proceedings of the Royal Society A (backup: JSV).
