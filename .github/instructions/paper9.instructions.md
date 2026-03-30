---
applyTo: "papers/paper9-lifting-theorem/**"
---

# Paper 9 — Inverse Problems (Lifting Theorem)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper9-lifting-theorem
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper9-lifting-theorem/main.pdf "papers/paper9-lifting-theorem/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 9 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Use `\SI{value}{unit}` for quantities.
Target: Inverse Problems (IOP Publishing).
