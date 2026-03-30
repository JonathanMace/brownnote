---
applyTo: "papers/paper7-watermelon/**"
---

# Paper 7 — Postharvest Biology and Technology (Watermelon Ripeness)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper7-watermelon
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper7-watermelon/main.pdf "papers/paper7-watermelon/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 7 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Code lives in src/analytical/watermelon_model.py.
Target: Postharvest Biology and Technology / PNAS.
