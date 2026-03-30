---
name: write-skill
description: >-
  Skills teach agents reusable procedures, workflows, and domain expertise
  they can invoke by name or that auto-activate from context.  Use this skill
  to author a SKILL.md, package a repeatable workflow, or set up a
  .github/skills directory.
license: MIT
---

# Authoring Agent Skills for GitHub Copilot CLI

Agent skills are folders of instructions, scripts, and resources that Copilot loads on-demand to improve its performance on specialized tasks. Each skill is a self-contained directory with a `SKILL.md` file and optional supporting assets.

A well-authored skill should let a future contributor repeat the same workflow without relying on session history or tribal knowledge.

## Procedure: Authoring a Skill

1. **Decide whether a skill is the right mechanism** (see [When to Author a Skill](#when-to-author-a-skill-vs-other-customization) below).
2. **Inspect neighboring skills first** — if the repository already has skills in `.github/skills/`, match their frontmatter shape, tone, and structural conventions for consistency.
3. **Define the trigger before authoring** — articulate the kind of request or task that should cause Copilot to load this skill. This becomes your `description` field and sets the scope boundary for the entire skill.
4. **Choose a placement** — for Copilot CLI, prefer project-level (`.github/skills/`) or personal (`~/.copilot/skills/`).
5. **Create a directory** named in lowercase with hyphens (e.g., `github-actions-debugging`).
6. **Author the `SKILL.md`** — author YAML frontmatter (`name`, `description`, optional `license`) followed by a Markdown body with instructions. Keep the body narrowly scoped to the trigger you defined in step 3. If the domain is broad, use the dispatcher pattern (see [Scaling Skills: The Dispatcher Pattern](#scaling-skills-the-dispatcher-pattern)) — keep the SKILL.md thin and point to deeper content files.
7. **Add supporting files** (optional) — scripts, templates, or examples in the skill directory.
8. **Review as if new to the repo** — re-read the skill from the perspective of someone who has never seen the repository. It should clearly explain when to use it, what steps to follow, what "done" looks like, and which related docs or validations must accompany the change.
9. **Test the skill** — run `/skills reload`, then prompt Copilot with a task that should trigger it. Verify it activates and produces good results.

## When to Author a Skill (vs Other Customization)

- **Author a skill** for repeatable, task-specific instructions that Copilot should only load when relevant (e.g., debugging CI failures, generating tests, reviewing PRs).
- **Author custom instructions** (`.github/copilot-instructions.md`) for broad, always-on guidance like coding standards that apply to every task (see the `writing-custom-instructions` skill).
- **Author a custom agent** (`.agent.md`) when you need a specialized persona with constrained tools or a distinct approach (see the `writing-custom-agents` skill).

Skills are the right choice when you want "just-in-time" expertise without permanently enlarging the context window.

## Directory Structure

```
.github/skills/
└── my-skill-name/
    ├── SKILL.md              # Required — skill definition
    ├── scripts/              # Optional — helper scripts
    │   └── run-checks.sh
    └── templates/            # Optional — templates, examples
        └── checklist.md
```

### Placement Options

| Scope | Location |
|-------|----------|
| **Project skills** (single repo) | `.github/skills/` in repo root |
| **Personal skills** (all repos) | `~/.copilot/skills/` in your home directory |

Copilot CLI can also read `.claude/skills/`, `.agents/skills/`, and their home-directory equivalents for compatibility. For Copilot-focused repositories, prefer `.github/skills/` and `~/.copilot/skills/`.

### Naming Rules

- Directory name: **lowercase, hyphens for spaces** (e.g., `github-actions-debugging`)
- The directory name should match the `name` field in the YAML frontmatter
- Use descriptive, specific names that convey the skill's purpose

## SKILL.md Format

Every skill requires a `SKILL.md` file (the filename must be exactly `SKILL.md`). It consists of **YAML frontmatter** followed by a **Markdown body**.

### YAML Frontmatter

```yaml
---
name: release-notes
description: >-
  Produce consistent, well-structured release notes by summarizing changes,
  categorizing features and fixes, and applying repository-specific checks.
  Use when drafting release notes, changelog entries, or release summaries.
license: MIT
---
```

Include `license` only when you want to declare the license for the skill; otherwise omit it.

| Property | Required | Description |
|----------|----------|-------------|
| `name` | **Yes** | Unique identifier. Lowercase, hyphens for spaces. It should match the directory name, and in this repo you should keep them identical. |
| `description` | **Yes** | Explains what the skill does AND when to use it. This is critical — Copilot matches user prompts against this text to decide whether to load the skill. |
| `license` | No | License that applies to the skill. |

### Writing an Effective Description

The `description` is the single most important field. Copilot uses it to decide when to auto-invoke the skill. Write **purpose-first** descriptions:

1. **Lead with what the artifact achieves** — the first sentence should explain the capability or outcome so agents discover the skill even when they don't know the Copilot CLI term for it.
2. **State when to use it** — include trigger phrases and keywords that users would naturally type.
3. **Be specific** — vague descriptions cause false matches or missed invocations.
4. **Keep it concise** — 1–3 short sentences is usually enough.

**Good examples (purpose-first):**

```yaml
# First sentence explains what the skill achieves, not what it is
description: >-
  Diagnose and fix failing GitHub Actions workflows by analyzing logs,
  reproducing failures locally, and applying targeted fixes.  Use when
  asked to debug, fix, or investigate CI/CD failures or broken builds.
```

```yaml
description: >-
  Hooks automatically run commands before or after agent actions —
  logging activity, blocking unsafe commands, or triggering side effects.
  Use this skill to author hooks.json files or add pre/post tool guards.
```

**Bad examples:**

```yaml
# Tautological — requires the user to already know the term
description: Guide for authoring GitHub Actions debugging skills.

# Too vague — when would Copilot use this?
description: Helps with code stuff.

# Too narrow — misses many valid prompts
description: Use only when user types exactly "run the test helper".
```

### Markdown Body

The body contains the actual instructions Copilot will follow when the skill is loaded. Author these instructions as if you are onboarding a skilled developer who has never seen your project.

**Structure your instructions with:**

1. **Context** — brief background on what the skill addresses
2. **Step-by-step procedure** — numbered steps Copilot should follow
3. **Rules and constraints** — what to do and what to avoid
4. **Cross-references** — call out related agents, docs, hooks, or other skills rather than duplicating their content
5. **Examples** — concrete input/output samples when helpful
6. **Done criteria** — what "done" looks like, including any validation or documentation steps

The instructions should tell Copilot what to do, when to use supporting files, and how to recognize completion without relying on session history.

For **procedural skills** (e.g., "debug CI failures"), use a numbered step-by-step workflow. For **reference skills** (e.g., "how to author X"), organize by topic with sections and tables, but still include a top-level procedure summarizing the authoring workflow.

Prefer cross-references over duplication — link to the durable doc, agent, or skill that owns deeper context instead of embedding long background sections.

```markdown
---
name: github-actions-failure-debugging
description: >-
  Diagnose and fix failing GitHub Actions workflows by analyzing logs,
  reproducing failures locally, and applying targeted fixes.  Use when
  asked to debug, fix, or investigate CI/CD failures or broken builds.
---

To debug failing GitHub Actions workflows, follow this process:

1. Use `list_workflow_runs` to look up recent workflow runs and their status
2. Use `summarize_job_log_failures` to get an AI summary of the failure logs
3. If more detail is needed, use `get_job_logs` for full logs
4. Try to reproduce the failure locally
5. Fix the failing build and verify the fix before committing
```

## Referencing Supporting Files

You can include scripts, templates, and other assets in the skill directory and reference them in the instructions. Reference them by relative path and explain when Copilot should use them:

```markdown
When creating a new test file, use the template at `templates/test-template.md`
as a starting point.

To run the validation checks, execute `scripts/validate.sh` from the skill
directory.
```

Copilot can read and execute files within the skill directory when instructed to do so.

## Scaling Skills: The Dispatcher Pattern

### The Problem

Copilot auto-loads every skill's `description` into context on every LLM call to decide which skills are relevant. At scale (dozens or hundreds of skills), this description overhead becomes significant. Additionally, complex domains may need far more content than fits comfortably in a single SKILL.md body without bloating the context when the skill fires.

### The Solution: Thin Dispatchers with Deep Content

Keep the `SKILL.md` thin — just a purpose-first description and a short body that **points the agent to deeper content files**. The agent is intelligent enough to open and follow any file you reference. Only the description is always loaded; the body is loaded only on match; and the referenced files are loaded only when the agent reads them.

```
.github/skills/
└── ci-workflows/
    ├── SKILL.md              # Thin dispatcher: description + routing logic
    └── guides/
        ├── debugging.md      # Deep content: CI debugging procedure
        ├── authoring.md      # Deep content: writing new workflows
        └── optimization.md   # Deep content: speeding up slow pipelines
```

### Dispatcher SKILL.md Example

```markdown
---
name: ci-workflows
description: >-
  Diagnose failing CI pipelines, author new GitHub Actions workflows, and
  optimize slow builds.  Use when asked to debug CI, fix broken builds,
  write or edit GitHub Actions workflows, or speed up pipelines.
---

# CI Workflows

This skill covers CI/CD with GitHub Actions. Read the guide that matches
the task:

- **Debugging a failure** — read and follow `guides/debugging.md`
- **Authoring a new workflow** — read and follow `guides/authoring.md`
- **Optimizing pipeline speed** — read and follow `guides/optimization.md`

If the task spans multiple areas, read the relevant guides in order.
```

### When to Use the Dispatcher Pattern

- The domain is broad enough that a single SKILL.md body would exceed ~200 lines or cover distinct sub-tasks.
- You want a single description to cover several related capabilities without registering each as a separate skill.
- Multiple skills or agents need to reference the same deep content — put the content in a shared location and point to it from each.

### When NOT to Use It

- The skill is simple enough to fit comfortably in a single SKILL.md body (~50-150 lines). Don't over-engineer.
- The sub-topics are unrelated enough that they deserve separate descriptions for auto-matching. In that case, author separate skills.

### Guidelines for Dispatcher Skills

1. **Keep the dispatcher body short** — its job is routing, not teaching. A list of sub-topics with file references is enough.
2. **Make routing unambiguous** — the agent should be able to pick the right file from the task description without guessing.
3. **Deep content files follow the same structure as a SKILL.md body** — procedure, rules, examples, done criteria. They just lack frontmatter.
4. **Use conditional routing when needed** — "If the project uses Python, read `guides/python.md`; if TypeScript, read `guides/typescript.md`."
5. **Cross-reference freely** — deep content files can reference other files, scripts, templates, or even other skills.

## How Skills Are Invoked (Context for Authors)

Understanding how skills are invoked helps you author better descriptions and instructions.

### Automatic Invocation

Copilot automatically loads a skill when it determines the skill is relevant to the current task, based on the skill's `description` matching the user's prompt. When that happens, the `SKILL.md` body is added to the agent's context. This is why the `description` field is critical — it controls discoverability, while the body supplies the working instructions.

### Manual Invocation

Users can invoke a skill explicitly by prefixing its name with `/` in their prompt:

```
Use the /github-actions-failure-debugging skill to fix the CI failures.
```

### Skills Management Commands

| Command | Purpose |
|---------|---------|
| `/skills list` | List all available skills |
| `/skills` | Toggle skills on/off interactively |
| `/skills info` | View detailed info about a skill (including location) |
| `/skills reload` | Reload skills without restarting the CLI |
| `/skills add` | Add an alternative skills directory |
| `/skills remove SKILL-DIR` | Remove a directly-added skill |

## Done Criteria

- Skill directory created with lowercase-hyphen name matching `name` frontmatter field
- `SKILL.md` has valid YAML frontmatter (`name`, `description`, and optionally `license`)
- Description is purpose-first — first sentence explains what the skill achieves, not what it is
- Description includes trigger phrases for auto-invocation
- Body includes a numbered procedure with an "Inspect First" opening step
- Cross-references to related skills, agents, or docs present (no unnecessary duplication)
- Examples included where helpful
- Done criteria section defined
- Skill tested with `/skills reload` and verified via both auto-invocation and explicit `/skill-name` prompt

## Best Practices for Authoring Skills

1. **One skill per task domain** — keep skills focused and modular.
2. **Define the trigger first** — articulate what kind of request should load this skill before writing the body. The body should be narrowly scoped to that trigger.
3. **Write purpose-first descriptions** — lead with what the skill achieves, not what it is. Agents discover skills by intent; a tautological description like "Guide for authoring X" only matches if the user already knows the term.
4. **Prefer cross-references over duplication** — link to related agents, docs, hooks, or other skills that own deeper context rather than embedding long background sections.
5. **Prefer skills over bloated instructions** — move task-specific guidance out of `copilot-instructions.md` and into skills to keep the base context lean.
6. **Include concrete examples** — Copilot performs better when instructions include examples of expected behavior.
7. **Test your skill** — after authoring a skill, run `/skills reload`, then try both a natural prompt that should auto-invoke the skill and an explicit `/skill-name` prompt. Verify it activates and produces good results.
8. **Keep instructions actionable** — author numbered steps, not vague aspirations. Tell Copilot what to do, what to check, and when to use supporting files.
9. **Match existing conventions** — if the repository already has skills, match their tone, frontmatter shape, and structural patterns.
10. **Reference scripts for complex logic** — if a procedure involves complex shell commands or multi-step automation, include a script in the skill directory rather than embedding long code blocks in the Markdown.
11. **Open with an "Inspect First" step** — start your procedure by listing the specific files, configs, or state the agent should read before making any changes. This grounds the agent in current reality and prevents stale-context mistakes or assumptions that drift from what's actually in the repo.
12. **Use the dispatcher pattern for broad domains** — when a skill covers multiple sub-tasks or would exceed ~200 lines, keep the SKILL.md thin and route to deeper content files. This keeps description overhead low and avoids context bloat.
13. **Consider packaging as a plugin** — if you want to distribute a collection of skills (plus agents, hooks, and MCP configs), package them as a plugin for easy installation via `/plugin install`.
