# Pop-culture citation audit — 2026-03-28T2230

**Author**: Opus
**Branch**: pop-culture-citations
**PR**: pending

## Summary
Created a dedicated pop-culture-verifier agent, added an explicit non-scientific citation rule to copilot-instructions.md, and completed a first-pass audit of all requested manuscript trees for pop-culture, media, folklore, and other non-traditional references. The audit focused on whether each non-scientific reference was specific, sourceable, and backed by complete BibTeX metadata.

## Key Findings
- Audited 6 manuscript roots: paper, paper/sections, paper2-gas-pockets, paper3-scaling-laws, projects/bladder-resonance/paper, and projects/borborygmi/paper.
- Found 3 actionable pop-culture/media references requiring citation tightening: the South Park brown-note episode, the MythBusters televised debunking, and the gas-pockets paper's broad popular-culture framing.
- Added 4 BibTeX entries across 2 bibliographies (2 unique media sources duplicated where cited): SouthPark2000BrownNoise and MythBusters2005BrownNote in paper/references.bib and paper2-gas-pockets/references.bib.
- Tightened 3 manuscript passages to cite exact episode-level sources, replacing vague references with season/episode/title/air-date-resolvable citations.
- Validation passed: python -m pytest tests\ -v completed with 198/198 tests passing; paper/main.tex and paper2-gas-pockets/main.tex both compiled successfully.

## Changes Made
- .github/agents/pop-culture-verifier.agent.md
- .github/copilot-instructions.md
- paper/sections/introduction.tex
- paper/references.bib
- paper2-gas-pockets/main.tex
- paper2-gas-pockets/references.bib
- docs/research-logs/2026-03-28T2230-pop-culture-citations.md
- docs/research-logs/2026-03-28T2230-paper-snapshot.pdf
- docs/research-logs/2026-03-28T2230-paper2-gas-pockets-snapshot.pdf

## Issues Identified
- MINOR: projects/bladder-resonance/paper/sections/discussion.tex still contains the uncited anecdotal phrase "the long drive phenomenon". It is not a formal pop-culture citation, but it remains an unsupported cultural/general-experience reference that may merit either a citation or softer wording.
- MINOR: paper/main.log retains pre-existing Hyperref PDF-string warnings unrelated to this citation audit.

## Next Steps
- Run the new pop-culture-verifier agent before submission of any manuscript with cultural framing or media references.
- Decide whether to cite or soften the bladder paper's long drive phenomenon wording.
- If more popular-media framing is added later, prefer exact episode/film/news metadata immediately rather than retrofitting the bibliography during final polishing.
