---
name: research-iteration
description: >
  Full research iteration protocol: DO → REVIEW → LOG → COMPILE → COMMIT → PLAN.
  Use when starting a new iteration cycle or when you need to remember the
  correct sequence of steps.
---

# Research Iteration Protocol

The authoritative workflow for every research cycle.

## The Cycle

```
DO → REVIEW → LOG → COMPILE → COMMIT → PLAN → MAINTAIN
```

### 1. DO (Parallel Work)
Launch ≥6 concurrent background agents, each on its own worktree/branch.
Mix of: analysis, paper writing, review, infrastructure, scouting.

Each agent MUST:
- Work only in its assigned worktree
- Commit with `[category]` prefix and Co-authored-by trailer
- Push its branch
- Create a PR: `gh pr create --base main --head <branch> ...`
- Merge its own PR: `gh pr merge <N> --merge`
- Delete remote branch: `git push origin --delete <branch>`
- Resolve merge conflicts eagerly via rebase

### 2. REVIEW (3-Reviewer Panel)
After major paper updates, launch 3 reviewers in parallel:
- **Reviewer A**: Domain expert — novelty, significance, narrative, missing refs
- **Reviewer B**: Cynical gatekeeper — fatal flaws, parameter consistency, logic
- **Reviewer C**: Methodologist — runs code, checks every number against paper

Each reviewer writes to `docs/research-logs/reviewer-X-roundN.md`.
Synthesise all 3 into an action plan before next iteration.

### 3. LOG
Create `docs/research-logs/YYYY-MM-DDTHHMM-topic.md` with:
- Quantitative results (specific numbers, not vague claims)
- Changes made (file list)
- Issues identified (with severity)
- Next steps

Include PDF snapshot: `YYYY-MM-DDTHHMM-paper-snapshot.pdf`

### 4. COMPILE
```powershell
cd papers/paper1-brown-note  # adjust to the paper being compiled
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
Copy-Item main.pdf "drafts\draft_$(Get-Date -Format 'yyyy-MM-dd_HHmm').pdf"
```

### 5. COMMIT
Branch → commit → push → PR → merge → delete remote branch → pull main.

### 6. PLAN
- Update SQL todos
- Identify next parallel batch
- Update `.github/copilot-instructions.md` if anything material changed

### 7. MAINTAIN
- Run lab-meeting agent for docs freshness audit
- Run consistency-auditor before paper compilation
- Clean up stale worktrees and branches
- Visit the coffee machine if things feel stale
