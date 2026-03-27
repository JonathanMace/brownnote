# Git Checkpoint Skill

## Description
Create a git checkpoint with a descriptive message. Use between major research iterations.

## Workflow

1. **Stage**: `git add -A` in the repository root
2. **Status**: Check what's being committed with `git status --short`
3. **Commit**: Use a descriptive message following the format: `[phase] description`
   - Phase prefixes: `[analysis]`, `[paper]`, `[fea]`, `[review]`, `[infra]`, `[figures]`
4. **Verify**: Confirm commit was created

## Commands

```powershell
cd C:\Users\jon\OneDrive\Projects\browntone
git add -A
git status --short
git commit -m "[phase] description`n`nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

## Notes
- Always include the Co-authored-by trailer
- Keep messages concise but descriptive
- Include key findings or changes in the commit body if significant
