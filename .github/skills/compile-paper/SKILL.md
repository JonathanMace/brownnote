# Paper Compiler Skill

## Description
Compile the LaTeX paper, preserve timestamped PDF, and report any errors. Use this after any paper content changes.

## Workflow

1. **Compile**: Run `pdflatex` + `bibtex` + two more `pdflatex` passes from `paper/` directory
2. **Check**: Report any LaTeX warnings or errors
3. **Preserve**: Copy compiled PDF to `paper/drafts/draft_YYYY-MM-DD_HHMM.pdf`
4. **Report**: Output page count, file size, and any issues

## Commands

```powershell
cd C:\Users\jon\OneDrive\Projects\browntone\paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
$ts = Get-Date -Format "yyyy-MM-dd_HHmm"
New-Item -ItemType Directory -Path drafts -Force | Out-Null
Copy-Item main.pdf "drafts\draft_$ts.pdf"
```

## Error Handling
- If `pdflatex` fails, check `main.log` for the specific error
- Common issues: missing `\cite{}` keys, undefined `\label{}` references, missing packages
- Fix issues in the source `.tex` or `.bib` files and recompile

## Output Artifacts
- `paper/main.pdf` — latest compiled paper
- `paper/drafts/draft_*.pdf` — timestamped archive copies
