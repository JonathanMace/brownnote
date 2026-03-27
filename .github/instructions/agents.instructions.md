---
applyTo: ".github/agents/**"
---

# Agent Definition Instructions

You are writing or editing a custom agent definition for the Browntone research lab.

## Required Structure

Every agent `.agent.md` file must include:

### YAML Frontmatter
```yaml
---
name: agent-name
description: >
  One paragraph describing the agent's expertise and WHEN to use it.
  Be specific about trigger conditions.
tools:
  - read_file
  - edit_file
  - powershell
  - grep
  - glob
---
```

### Body Sections
1. **Identity**: Who is this agent? What is their expertise?
2. **When to Activate**: Specific conditions that trigger this agent
3. **Standard Operating Procedure**: Step-by-step workflow the agent follows EVERY TIME
4. **Output Format**: Exact structure of the agent's deliverable
5. **Constraints**: What the agent must NOT do
6. **Quality Gates**: Minimum standards the output must meet before the agent considers itself done

## Key Principles

- **Self-contained**: The agent definition must include ALL reusable logic. The orchestrator
  should only need to provide task-specific context (e.g., "review the current paper draft"),
  not workflow instructions.
- **Idempotent**: Running the agent twice on the same input should produce consistent results.
- **Scoped**: Agents work in their assigned worktree only. They do not merge, do not edit
  other branches, and do not modify files outside their scope.
- **Quantitative**: Agent outputs must include specific numbers, not vague assessments.

## Git Workflow (include in every agent)

Every agent that produces file changes must include this workflow:
```
1. Work in assigned worktree: C:\Users\jon\OneDrive\Projects\browntone-worktrees\<branch>
2. Commit: git add -A && git commit -m "[category] Description\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
3. Push: git push origin <branch>
4. Do NOT merge. The orchestrator handles merges via PRs.
```

## Existing Agents (avoid duplication)

- reviewer-a: Domain expert (novelty, significance, narrative)
- reviewer-b: Cynical gatekeeper (fatal flaws, consistency)
- reviewer-c: Methodologist (runs code, checks numbers)
- consistency-auditor: Parameter/number consistency
- lab-meeting: Holistic audit + docs freshness
- research-scout: Find new research topics
- provocateur: Devil's advocate
- communications: Outreach (abstracts, summaries)
- bibliographer: Literature tracking
- lab-manager: Infrastructure maintenance
