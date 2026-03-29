---
name: write-skill
description: >
  Guide for writing effective Copilot CLI skill files. Use when creating, reviewing, or restructuring skills under .github/skills/.
---

# Skill Author Reference

Practical guidance for writing reusable skill files for GitHub Copilot CLI and adjacent agentic coding tools.

## 1. What a skill is

In GitHub Copilot, an **agent skill** is a folder of instructions, scripts, and resources that Copilot loads **only when relevant to the task**. Officially, skills live in `.github/skills/<skill-name>/SKILL.md` (or the equivalent `.claude/skills/` / `.agents/skills/` locations), and Copilot chooses them by matching the task against the skill description.  
Sources: GitHub Docs — create skills: <https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills>; customization cheat sheet: <https://docs.github.com/en/copilot/reference/customization-cheat-sheet>

**Use a skill when** you want reusable, on-demand workflow guidance.  
**Do not use a skill when** the rule should always apply, when you need a dedicated persona/tool budget, or when the output should become a durable seeded file.

## 2. Canonical GitHub Copilot skill layout

Official layout:

```text
.github/
  skills/
    my-skill/
      SKILL.md
      scripts/        # optional
      examples/       # optional
      assets/         # optional
```

Officially supported locations include:

- project: `.github/skills/`, `.claude/skills/`, `.agents/skills/`
- personal: `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/`

The subdirectory name should be lowercase and use hyphens. `SKILL.md` is required and must be named exactly `SKILL.md`.  
Source: <https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills>

## 3. YAML frontmatter: what is actually supported

### 3.1 Official GitHub fields

GitHub’s current public docs for Copilot skills document:

```yaml
---
name: my-skill
description: >
  What the skill does, and when Copilot should use it.
license: MIT   # optional
---
```

Field guidance:

| Field | Status | Notes |
| --- | --- | --- |
| `name` | Required | Lowercase, hyphens, usually matches directory name. |
| `description` | Required | Must say both **what** the skill does and **when to use it**. |
| `license` | Optional | Useful for portable/public skills; often omitted in repo-local skills. |

Source: <https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills>

### 3.2 About `tools`

For **GitHub Copilot skills**, `tools` is **not** part of the public official skill schema. GitHub documents `tools` for **custom agents**, not for skills.  
Sources: custom agents config: <https://docs.github.com/en/copilot/reference/custom-agents-configuration>; create custom agents: <https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents>

Some community material and the broader Agent Skills ecosystem mention extra fields such as `allowed-tools`, `compatibility`, or `metadata`, but these are not the safest portable default for Copilot CLI skills. For this repository, prefer **only**:

- `name`
- `description`
- optional `license`

Unless GitHub’s official docs change, do **not** invent a `tools` field in `SKILL.md`.

## 4. Recommended body structure

The Markdown body is free-form, but the best skills are structured as an executable workflow rather than as prose.

Recommended template:

```md
---
name: my-skill
description: >
  One-sentence trigger. Use when ...
---

# My Skill

One-sentence purpose.

## Inspect First

- Related file or doc
- Relevant tests or manifest
- Existing examples to copy

## Workflow

1. First action.
2. Next decision.
3. Validation step.
4. Docs-sync or follow-up step.

## Output / Done Criteria

- Expected artifact(s)
- What must be true before stopping

## Related Assets

- Link to agents, instructions, prompts, commands, or docs
```

Useful sections:

| Section | Why include it |
| --- | --- |
| `Inspect First` | Prevents the skill from acting without reading the local source of truth. |
| `Workflow` | Core ordered steps. This is the most important section. |
| `Decision points` | Helps the agent branch correctly instead of guessing. |
| `Output` / `Done Criteria` | Makes completion verifiable. |
| `Constraints` | Good when the skill must stay read-only or avoid certain files. |
| `Validation` | Prevents “write and hope” behaviour. |
| `Related Assets` | Avoids duplicating large documents or agent definitions. |

`Identity`, `procedure`, `output format`, `constraints`, and `quality gates` are excellent sections when they genuinely help execution; they are good **design patterns**, not GitHub-required syntax.

## 5. What makes a skill effective

Good Copilot skills have five properties:

1. **Clear trigger**  
   The description should say when the skill should load.
2. **Narrow scope**  
   One reusable workflow per skill.
3. **Ordered actions**  
   The body should tell the agent what to inspect, decide, do, and validate.
4. **Cross-references instead of duplication**  
   Link to the durable source of truth.
5. **Verifiable done state**  
   End with validation, output expectations, or docs-sync.

This matches both GitHub’s official “description decides relevance” model and the CopilotCLInit guidance for writing skills as reusable workflows rather than short reminders.  
Sources: GitHub skill docs above; CopilotCLInit plugin asset guide: `C:\Users\jon\.copilot\installed-plugins\_direct\JonathanMace--CopilotCLInit\docs\guides\plugin-assets.md:26-37`

## 6. Skill vs agent vs instructions vs prompt vs hook

For GitHub Copilot, use the smallest correct surface:

| Need | Use | Why |
| --- | --- | --- |
| Always-on project rules | Instructions | They apply automatically to broad work. |
| Reusable on-demand workflow | Skill | Loaded only when relevant. |
| Explicit one-shot task template | Prompt file / command | Manual entrypoint. |
| Specialist persona or restricted tools | Custom agent | Better isolation and specialization. |
| Deterministic lifecycle automation | Hook | Runs at fixed lifecycle events. |

Official Copilot comparison: <https://docs.github.com/en/copilot/reference/customization-cheat-sheet>

Repo-specific guidance from CopilotCLInit says the same in operational terms: instructions are broad policy, skills are on-demand workflow guidance, agents are specialized delegated work, and seed-pack artifacts are durable files copied into target repositories.  
Source: `C:\Users\jon\.copilot\installed-plugins\_direct\JonathanMace--CopilotCLInit\docs\guides\plugin-assets.md:5-15`

## 7. Cross-tool comparison

There is no perfect one-to-one mapping across tools.

| Tool | Closest equivalent to a Copilot skill | Notes |
| --- | --- | --- |
| **GitHub Copilot CLI / coding agent** | `.github/skills/<name>/SKILL.md` | True skill system; relevance-based loading. |
| **Claude Code** | No exact direct equivalent; combine `CLAUDE.md`, `.claude/rules/*.md`, and commands/agents | `CLAUDE.md` is always-on memory, not on-demand skill loading. |
| **Cursor** | `.cursor/rules/*.mdc` or `AGENTS.md` | Rules are persistent/scoped instructions, not true “skills”. |
| **Windsurf** | Workflows plus rules | Workflows are the closest match for multi-step reusable procedures; rules are more like instructions. |

### 7.1 Claude Code

Claude Code’s main primitives are:

- `CLAUDE.md` for persistent shared or personal instructions
- `.claude/rules/*.md` for modular or path-scoped rules
- optional agents/commands under `.claude/`

Important difference: `CLAUDE.md` is loaded at session start and should stay concise; it is **not** a relevance-triggered skill file.  
Source: official Claude Code memory docs: <https://code.claude.com/docs/en/memory>

Practical mapping:

- Copilot **instruction** ↔ Claude `CLAUDE.md` or unconditional `.claude/rules/*.md`
- Copilot **path-specific instruction** ↔ Claude `.claude/rules/*.md` with `paths:` frontmatter
- Copilot **skill** ↔ Claude command/agent + referenced workflow doc, not a single native file type

### 7.2 Cursor

Cursor’s modern rule system lives in `.cursor/rules/` and supports persistent project, user, and team rules, with `AGENTS.md` also recognized. This is closer to Copilot **instructions** than to Copilot **skills**.  
Source: Cursor docs: <https://cursor.com/docs/rules>

Practical mapping:

- Put always-on conventions in Cursor rules.
- For a “skill-like” reusable workflow, create a focused rule file plus a command or explicit invocation convention.
- Avoid using deprecated `.cursorrules` for new work unless a legacy repo already relies on it.

### 7.3 Windsurf

Windsurf distinguishes:

- **Rules** for persistent guidance
- **Workflows** for reusable multi-step automation
- **Memories** for retained context

That makes Windsurf **workflows** the closest conceptual match to Copilot skills.  
Source: official Windsurf overview: <https://windsurf.com/university/general-education/intro-rules-memories>

## 8. Repo-local patterns found in `browntone`

This repository currently contains **two patterns**:

1. **Modern, GitHub-compliant folder skills**  
   Example: `.github/skills/git-checkpoint/SKILL.md`
2. **Legacy flat Markdown notes in `.github/skills/*.md`**  
   Example: `.github/skills/mesh-convergence.md`

Only the first pattern matches GitHub’s documented skill layout.

### 8.1 Good local examples

#### Example A: `git-checkpoint`

Why it works:

- clean official frontmatter
- explicit trigger in description
- numbered operational workflow
- failure branch for merge conflicts
- concrete done-state rules

See: `C:\Users\jon\OneDrive\Projects\browntone\.github\skills\git-checkpoint\SKILL.md:1-80`

#### Example B: `research-iteration`

Why it works:

- strong reuse trigger
- workflow broken into named phases
- contains sequencing, artifacts, and maintenance expectations
- gives the agent a full loop rather than a single command

See: `C:\Users\jon\OneDrive\Projects\browntone\.github\skills\research-iteration\SKILL.md:1-72`

### 8.2 Weak or legacy local examples

#### Example C: `mesh-convergence.md`

Why it is weak as a Copilot skill:

- lives at `.github/skills\mesh-convergence.md`, not `.github/skills/mesh-convergence/SKILL.md`
- frontmatter omits `name`
- behaves more like a reference note than a discoverable skill package

See: `C:\Users\jon\OneDrive\Projects\browntone\.github\skills\mesh-convergence.md:1-120`

#### Example D: `critique-results`

Why it is risky:

- duplicated YAML frontmatter (`---` block repeated twice)
- extra duplicated metadata creates ambiguity and looks malformed to maintainers

See: `C:\Users\jon\OneDrive\Projects\browntone\.github\skills\critique-results\SKILL.md:1-15`

## 9. Good and bad patterns

### Good

```md
---
name: compile-paper
description: >
  Compile the LaTeX paper, preserve timestamped PDF, and report any errors.
  Use this after any paper content changes.
---

# Compile Paper

## Inspect First
- `paper/main.tex`
- latest log if compilation is already failing

## Workflow
1. Run the standard compile sequence.
2. Check for errors and warnings.
3. Preserve a timestamped PDF.
4. Report output artifact details.

## Done
- `paper/main.pdf` exists
- archived draft copy exists
- errors are reported or cleared
```

Why it is good:

- short trigger
- inspect-first guidance
- ordered steps
- verifiable end state

### Bad

```md
---
description: Helps with papers.
---

Write the paper well. Check everything. Use the right style.
```

Why it is bad:

- missing `name`
- trigger is vague
- no ordered workflow
- no inspection points
- no validation

## 10. Anti-patterns

Avoid these:

1. **Vague description**  
   “Helps with docs” is too broad. Say what task should trigger the skill.
2. **Background dump instead of workflow**  
   Skills are operational. Long essays belong in docs.
3. **Duplicating agent logic**  
   If the work needs specialized delegation or a restricted tool budget, write an agent.
4. **Policy in a skill that should be always-on**  
   Repository-wide coding standards belong in instructions.
5. **Missing validation**  
   Every workflow should state what to run or check at the end.
6. **Malformed frontmatter**  
   Missing `name`, duplicate YAML blocks, or ad hoc fields reduce portability.
7. **Flat legacy placement**  
   `.github/skills/foo.md` is not the documented GitHub format.
8. **No “inspect first” step**  
   Skills should point the agent at the source of truth before acting.
9. **Hidden assumptions**  
   If a workflow depends on another doc, manifest, script, or agent, say so.

## 11. Best-practice authoring rules for this repository

When authoring a new skill in `browntone`:

1. Use `.github/skills/<skill-name>/SKILL.md`.
2. Keep frontmatter to `name` + `description` (+ optional `license`).
3. Start by naming the trigger: “Use when...”
4. Lead with what the reader should inspect first.
5. Write numbered workflow steps.
6. Add validation or completion criteria.
7. Cross-reference related docs/agents instead of pasting their full contents.
8. If the content is durable repository scaffolding, consider a seed-pack instead.
9. If the task needs a persona or bounded tools, consider an agent instead.

This matches both the official GitHub skill model and the CopilotCLInit `write-skills` guidance.

## 12. Seed-pack note (CopilotCLInit)

`CopilotCLInit` appears to define a **repo-specific** seed-pack system. This is **not** a GitHub-native Copilot skill format; it is plugin-specific scaffolding.

In that plugin, each `seed-packs/*/manifest.json` contains:

- `name`
- `version`
- `entries[]`
  - `id`
  - `source`
  - `target`
  - `modes` (`init`, `enrich`)
  - `strategy` (`create-if-missing`)
  - optional `description`
  - optional `conflict_hint`

Sources:

- `C:\Users\jon\.copilot\installed-plugins\_direct\JonathanMace--CopilotCLInit\docs\architecture\seed-pack-contract.md:5-18`
- `C:\Users\jon\.copilot\installed-plugins\_direct\JonathanMace--CopilotCLInit\seed-packs\core\manifest.json`

Treat this as **plugin-local infrastructure**, not as part of GitHub Copilot’s official skill syntax.

## 13. Review checklist before committing a skill

- [ ] File is at `.github/skills/<skill-name>/SKILL.md`
- [ ] Directory name is lowercase kebab-case
- [ ] `name` exists and matches directory name
- [ ] `description` says both **what it does** and **when to use it**
- [ ] No unsupported frontmatter fields added casually
- [ ] Body starts with purpose and/or inspect-first guidance
- [ ] Workflow is ordered and actionable
- [ ] Related docs/agents/scripts are referenced
- [ ] Completion or validation criteria are explicit
- [ ] Skill does not duplicate broad project policy better kept in instructions
- [ ] Skill does not pretend to be an agent with hidden specialization requirements
- [ ] If the workflow produces durable repo scaffolding, you evaluated seed-pack/command alternatives

## 14. Minimal starter template

```md
---
name: example-skill
description: >
  Briefly say what this skill does. Use when the task is ...
---

# Example Skill

One-sentence purpose.

## Inspect First

- `path/to/source-of-truth`
- neighboring skill or doc

## Workflow

1. Read the source of truth.
2. Decide which branch of the workflow applies.
3. Perform the change or analysis.
4. Validate the result.
5. Update related docs if the behaviour changed.

## Done

- Expected artifact exists
- Validation has run
- Related docs are synchronized
```

This template is the default starting point for new Copilot skills in this repository.
