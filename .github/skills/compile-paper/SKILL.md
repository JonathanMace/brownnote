---
name: compile-paper
description: >
  Compile the LaTeX paper, preserve timestamped PDF, and report any errors.
  Use this after any paper content changes.
license: MIT
---

# Paper Compiler Skill

## Description
Compile any Browntone paper, preserve a timestamped PDF snapshot, update
the README draft link, and report any errors. **Use this after ANY paper
content changes.** Works for all 8 papers.

## Paper Directories

| Paper | Directory |
|-------|-----------|
| P1 Brown Note | `papers/paper1-brown-note/` |
| P2 Gas Pockets | `papers/paper2-gas-pockets/` |
| P3 Scaling Laws | `papers/paper3-scaling-laws/` |
| P4 Bladder | `papers/paper4-bladder/` |
| P5 Borborygmi | `papers/paper5-borborygmi/` |
| P6 Sub-bass | `papers/paper6-sub-bass/` |
| P7 Watermelon | `papers/paper7-watermelon/` |
| P8 Kac | `papers/paper8-kac/` |

## Workflow (ALL 5 steps are mandatory)

1. **Compile**: `pdflatex` → `bibtex` → `pdflatex` → `pdflatex`
2. **Check**: Report any LaTeX warnings or errors
3. **Snapshot**: Copy PDF to `drafts/draft_YYYY-MM-DD_HHMM.pdf`
4. **Update README**: Change the paper's draft link in the root README.md
5. **Commit**: Include `main.pdf`, snapshot, and README in the same commit

**Skipping steps 3–5 is an anti-pattern.** The repo drifts out of sync.

## Commands

Replace `$paperDir` with the appropriate paper directory:

```powershell
$paperDir = "papers/paper1-brown-note"   # ← change per paper
cd C:\Users\jon\Projects\browntone\$paperDir
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# Snapshot
$ts = Get-Date -Format "yyyy-MM-dd_HHmm"
New-Item -ItemType Directory -Path drafts -Force | Out-Null
Copy-Item main.pdf "drafts\draft_$ts.pdf"

# Update README draft link (do this manually — find the paper's row and
# update the link to point to the new snapshot path)
```

## Error Handling
- If `pdflatex` fails, check `main.log` for the specific error
- Common issues: missing `\cite{}` keys, undefined `\label{}` references, missing packages
- Fix issues in the source `.tex` or `.bib` files and recompile

## Output Artifacts
- `$paperDir/main.pdf` — latest compiled paper
- `$paperDir/drafts/draft_*.pdf` — timestamped archive copies
- `README.md` — updated draft link
