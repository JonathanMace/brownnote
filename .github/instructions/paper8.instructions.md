---
applyTo: "papers/paper8-kac/**"
---

# Paper 8 — Inverse Problems (Kac Identifiability)

When modifying ANY file in this directory:

1. **Recompile** after changes:
   ```powershell
   cd papers/paper8-kac
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```

2. **Create a timestamped draft snapshot**:
   ```powershell
   Copy-Item papers/paper8-kac/main.pdf "papers/paper8-kac/drafts/draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
   ```

3. **Update README.md** — change the Paper 8 draft link to point to the new snapshot.

4. **Commit the snapshot PDF** alongside your content changes.

All content must use British English. Code lives in src/analytical/kac_identifiability.py.
Target: Inverse Problems (IOP Publishing).
