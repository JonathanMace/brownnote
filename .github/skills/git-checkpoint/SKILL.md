---
name: git-checkpoint
description: >-
  Standardize a conflict-free git workflow for concurrent agents by managing
  branches, worktrees, commits, PRs, merges, and cleanup as a single
  repeatable lifecycle.  Use when branching, committing, creating PRs,
  squash-merging, or cleaning up after agent work.
license: MIT
---

# Git Checkpoint: Agent Git Workflow

This skill defines the standard git lifecycle for agents working in a repository — from branch creation through PR merge and cleanup. Following this procedure keeps concurrent agents isolated, prevents merge conflicts, and leaves the repository tidy when work is complete.

## Procedure: Full Git Lifecycle

### 1. Inspect the Repository

Before creating any branches or making changes, ground yourself in the actual repository state:

```bash
# Determine the default branch name
git symbolic-ref refs/remotes/origin/HEAD

# List all local and remote branches
git branch -a

# Check remote configuration
git remote -v
```

This avoids assumptions about the default branch name, existing branches, or remote setup. Use the discovered values in all subsequent steps.

### 2. Create a Branch

Pick a descriptive, kebab-case branch name scoped to the task (e.g., `add-login-validation`, `fix-ci-timeout`). Create it from the latest default branch:

```bash
git fetch origin
git checkout -b <branch-name> origin/main
```

Replace `main` with the repository's default branch if it differs.

### 3. Create a Worktree (Multi-Agent or Concurrent Work)

When multiple agents may be active in the same repository, each agent **must** work in its own git worktree to avoid conflicts. Create the worktree in a sibling directory following this convention:

```
<repo-root>-worktrees/<branch-name>/
```

For example, if the repo lives at `~/Projects/my-repo`:

```bash
git worktree add ../my-repo-worktrees/add-login-validation add-login-validation
cd ../my-repo-worktrees/add-login-validation
```

> **When to skip worktrees:** If you are the only agent working in the repository and the user has not requested worktree isolation, you may work directly on a branch in the main checkout. When in doubt, use a worktree — it is always safe.

### 4. Do the Work

Make your changes in the worktree (or branch checkout). Follow any project-specific conventions, linters, and tests before moving to the commit step.

### 5. Commit

Stage and commit with a clear, conventional message. Always include the Copilot co-author trailer:

```bash
git add -A
git commit -m "<type>: <concise summary>

<optional body — what and why, not how>

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

**Commit message guidelines:**

- Use a conventional prefix when the project follows Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, etc.). Otherwise, write a clear imperative summary.
- Keep the subject line under 72 characters.
- The body is optional but encouraged for non-trivial changes.
- The `Co-authored-by` trailer is **required** for all agent-authored commits.

Prefer small, atomic commits over large monolithic ones when the work is logically separable.

### 6. Push

Push the branch to the remote:

```bash
git push -u origin <branch-name>
```

If the branch already exists on the remote and you have rebased, force-push with lease:

```bash
git push --force-with-lease origin <branch-name>
```

### 7. Create a Pull Request

Create a PR targeting the default branch. Include:

- **Title:** a concise summary of the change (matches or expands the commit subject).
- **Body:** context on what changed, why, and any testing performed. Link related issues with `Closes #<number>` or `Fixes #<number>` when applicable.

Use the GitHub CLI when available:

```bash
gh pr create --title "<title>" --body "<body>" --base main
```

Or use the GitHub MCP server tools if the CLI is unavailable.

**PR best practices:**

- Keep PRs focused — one logical change per PR.
- Include before/after evidence (test output, screenshots) when the change affects behavior.
- Request review when required by the project's branch protection rules.

### 8. Squash-Merge

Once the PR is approved (or if no review is required), squash-merge it:

```bash
gh pr merge <pr-number> --squash --delete-branch
```

The `--delete-branch` flag deletes the remote branch automatically. If the project prefers a different merge strategy, follow that instead.

### 9. Clean Up

After merging, clean up all local artifacts:

```bash
# Switch back to the main checkout
cd <repo-root>

# Remove the worktree (if one was created)
git worktree remove ../my-repo-worktrees/<branch-name>

# Delete the local branch (if not already deleted)
git branch -d <branch-name>

# Delete the remote branch (if --delete-branch was not used)
git push origin --delete <branch-name>

# Prune stale remote-tracking references
git fetch --prune
```

**Cleanup checklist:**

- [ ] Worktree removed (`git worktree remove`)
- [ ] Local branch deleted (`git branch -d`)
- [ ] Remote branch deleted (via `--delete-branch` or `git push origin --delete`)
- [ ] Remote references pruned (`git fetch --prune`)

## Conflict Resolution

If a rebase or merge encounters conflicts:

1. **Attempt an automatic rebase first:**

   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **If conflicts arise**, resolve them file by file:

   ```bash
   # View conflicting files
   git diff --name-only --diff-filter=U

   # After resolving each file
   git add <resolved-file>
   git rebase --continue
   ```

3. **If the rebase is too complex to resolve safely**, abort and try a merge instead:

   ```bash
   git rebase --abort
   git merge origin/main
   ```

4. **If conflicts cannot be resolved confidently**, stop and ask the user for guidance rather than guessing at the intended resolution.

5. After resolving, force-push with lease:

   ```bash
   git push --force-with-lease origin <branch-name>
   ```

## When to Use This Workflow

| Situation | Recommendation |
|-----------|----------------|
| Multiple agents working concurrently | **Always** — use worktrees and separate branches |
| Single agent, non-trivial change | **Yes** — branch, PR, and merge provide a review checkpoint |
| Trivial edit (typo fix, single-line config change) | **Optional** — the user may prefer a direct commit to the default branch |
| User explicitly requests a direct commit | **Skip** — commit directly as instructed |

When in doubt, default to the full lifecycle. It is always safe and provides an audit trail.

## Cross-References

- Agents authored with the `write-agent` skill should follow this workflow for any code changes they produce.
- The worktree sibling-directory convention is defined in the repository's `copilot-instructions.md` under "Concurrent Agents and Git Worktrees."

## Done Criteria

- [ ] Branch created with a descriptive name
- [ ] Worktree created in `<repo-root>-worktrees/<branch-name>/` (if concurrent work)
- [ ] All commits include the `Co-authored-by: Copilot` trailer
- [ ] Changes pushed to the remote
- [ ] PR created with a clear title and body
- [ ] PR squash-merged into the default branch
- [ ] Worktree, local branch, and remote branch cleaned up
- [ ] `git fetch --prune` run to remove stale references

## Browntone-Specific Conventions

### Branch Protection

`main` is branch-protected. No direct pushes. ALL changes via PRs.

### Merge Strategy

Agents merge their own PRs immediately using `gh pr merge <N> --merge` (not squash). This preserves individual commit history.

### Commit Prefixes

Use one of: `[analysis]` `[paper]` `[fea]` `[review]` `[infra]` `[figures]` `[tests]` `[research]` `[meeting]` `[audit]` `[style]` `[log]`

### Co-Author Trailer (Required)

Every commit must include:
```
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

### Worktree Location

```
C:\Users\jon\Projects\browntone-worktrees\<branch-name>
```

### Conflict Resolution

Agents resolve merge conflicts eagerly while context is fresh — rebase onto main, fix conflicts, force-push, then merge.
