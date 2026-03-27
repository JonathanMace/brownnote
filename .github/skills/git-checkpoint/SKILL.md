---
name: git-checkpoint
description: >
  Branch, commit, push, PR, merge, and cleanup workflow. Use when you need
  to checkpoint your work to main via a pull request.
---

# Git Checkpoint Skill

The complete workflow for getting changes from a worktree into main.

## Full Workflow

### From a worktree (agent or orchestrator):

```powershell
cd C:\Users\jon\OneDrive\Projects\browntone-worktrees\<branch>

# 1. Commit
git add -A
git status --short
git commit -m "[category] Description

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# 2. Push
git push origin <branch>

# 3. Create PR
gh pr create --base main --head <branch> --title "[category] Title" --body "Summary"

# 4. Merge PR (agents merge their own PRs immediately)
gh pr merge <N> --merge

# 5. Delete remote branch
git push origin --delete <branch>
```

### If merge fails (conflict):

```powershell
git fetch origin main
git rebase origin/main
# Resolve conflicts in each file
git add -A
git rebase --continue
git push origin <branch> --force-with-lease
gh pr merge <N> --merge
git push origin --delete <branch>
```

### From the main worktree (orchestrator quick fix):

```powershell
cd C:\Users\jon\OneDrive\Projects\browntone
git checkout -b <short-lived-branch>
# ... make changes ...
git add -A
git commit -m "[category] Description

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push origin <short-lived-branch>
gh pr create --base main --head <short-lived-branch> --title "..." --body "..."
gh pr merge <N> --merge
git push origin --delete <short-lived-branch>
git checkout main
git pull origin main
```

## Commit Prefixes

`[analysis]` `[paper]` `[fea]` `[review]` `[infra]` `[figures]` `[tests]`
`[research]` `[meeting]` `[audit]` `[style]` `[log]`

## Rules

- **Never push directly to main** — it's branch-protected.
- **Always include the Co-authored-by trailer.**
- **Always delete remote branches after merging.**
- **Resolve merge conflicts eagerly** while context is fresh.
