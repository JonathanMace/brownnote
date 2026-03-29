---
name: write-instructions
description: >
  Guide for writing effective copilot-instructions.md and project configuration. Use when updating global Copilot guidance or deciding how to organise repository customisation.
---

# Browntone Runtime Note

In this repository's current Copilot CLI environment, path-specific
`.github/instructions/*.instructions.md` files do not load reliably.
Prefer `.github/copilot-instructions.md` for always-on guidance and
skills for reusable scoped workflows, while using the reference below
as general cross-tool authoring guidance.

# Authoring Project Instructions for Agentic Coding Tools

This guide is the Browntone lab reference for writing, reviewing, and pruning project instruction files for agentic coding tools. It focuses on GitHub Copilot's instruction system, then compares the equivalent mechanisms in Claude Code, Cursor, and Windsurf.

## Executive summary

1. Put only **always-relevant, non-obvious, project-specific** guidance in always-on instruction files.
2. Keep the **global file short and high-signal**; move niche workflows into skills, agents, workflows, or companion docs.
3. Use **path-specific files** for language-, directory-, or artefact-specific rules.
4. Prefer **imperative, testable statements** over vague aspirations.
5. Avoid duplication across files; duplicated facts drift.
6. Treat instruction files like code: version them, review them, test them, prune them.[^gh-effective][^gh-blog-5tips][^claude-memory][^windsurf-rules]

---

## 1. File locations and what they are for

### GitHub Copilot

#### Repository-wide instructions
- **File:** `.github/copilot-instructions.md`
- **Purpose:** always-on repository context for Copilot Chat and coding agents.
- **Use for:** repository purpose, architecture map, build/test commands, universal coding standards, high-priority constraints.[^gh-cli-custom][^gh-support]

#### Path-specific instructions
- **Files:** `.github/instructions/*.instructions.md`
- **Purpose:** additional rules that apply only when the current work touches matching files.
- **Use for:** language/framework conventions, paper-writing rules, test conventions, log templates, directory-specific safety constraints.[^gh-cli-custom][^gh-repo-custom]

#### Agent instructions
- **Files:** `AGENTS.md` primarily; Copilot also recognises `CLAUDE.md` and `GEMINI.md` in some surfaces.
- **Purpose:** instructions aimed at coding agents rather than general chat alone.
- **Use for:** multi-agent workflows, agent-specific operating rules, repo-portable agent guidance.[^gh-cli-custom][^gh-agents-md][^gh-support]

#### Skills
- **Files:** `.github/skills/<skill-name>/SKILL.md`
- **Purpose:** on-demand, task-specific capability packs.
- **Use for:** workflows that should not consume tokens on every request: paper compilation, issue triage, GitHub Actions debugging, figure generation, deployment sequences.[^gh-skills]

### Claude Code
- **Global / project memory:** `CLAUDE.md` or `.claude/CLAUDE.md`
- **Path/topic-specific rules:** `.claude/rules/**/*.md` with `paths:` frontmatter
- **Purpose:** persistent project memory plus optional scoped rules; imports via `@path` keep the main file small.[^claude-memory][^claude-best]

### Cursor
- **Project rules:** `.cursor/rules/*.mdc`
- **Legacy shorthand:** `.cursorrules`
- **Also recognised:** `AGENTS.md`
- **Purpose:** persistent instructions for project, team, or user scope, optionally gated by globs and activation mode.[^cursor-rules]

### Windsurf
- **Project rules:** `.windsurfrules` or `.windsurf/rules/*.md`
- **Memories:** managed separately from rules
- **Purpose:** durable rules for standards and workflows; memories for learned context or one-off decisions.[^windsurf-intro][^windsurf-rules]

---

## 2. Syntax and structure

### 2.1 GitHub Copilot global file

`copilot-instructions.md` is plain Markdown. There is no required schema beyond “natural language instructions in Markdown”. Whitespace is ignored semantically, so structure is for humans and model readability rather than parser correctness.[^gh-cli-custom][^gh-repo-custom]

Recommended skeleton:

```md
# Project name

## Project overview
- What this repository does
- What success looks like

## Architecture map
- Where the main code lives
- Which directories are source of truth

## Build and validation
- Bootstrap
- Test
- Lint
- Run

## Universal rules
- Naming
- Safety constraints
- Review expectations

## Anti-patterns
- Things the agent must not do
```

### 2.2 GitHub Copilot path-specific files

Use YAML frontmatter plus Markdown body.

```md
---
applyTo: "tests/**"
---

# Test Instructions
- Use pytest.
- Add regression tests for bug fixes.
```

Key points:
- `applyTo` uses glob syntax relative to repo/workspace root.[^gh-cli-custom][^gh-repo-custom]
- Multiple patterns are written as a **comma-separated string** for GitHub documentation examples, e.g. `"**/*.ts,**/*.tsx"`.[^gh-cli-custom]
- `excludeAgent` can exclude `code-review` or `coding-agent` when needed.[^gh-cli-custom]
- For maximum GitHub compatibility, keep frontmatter minimal: `applyTo` and optionally `excludeAgent`.
- VS Code additionally understands optional `name` and `description` fields in `.instructions.md` files.[^vscode-custom]

### 2.3 Claude Code

`CLAUDE.md` is plain Markdown. Claude also supports `.claude/rules/*.md` with YAML frontmatter:

```md
---
paths:
  - "src/api/**/*.ts"
---

# API rules
- Validate input.
- Use the shared error envelope.
```

Claude also supports `@path/to/file` imports to keep the main file concise.[^claude-memory]

### 2.4 Cursor

Cursor rules are Markdown/MDX-like rule files in `.cursor/rules/`, usually with frontmatter describing scope and activation. Official docs describe project, team, and user rules plus `AGENTS.md` compatibility.[^cursor-rules]

Typical community pattern:

```md
---
description: React component rules
globs: ["src/components/**/*.tsx"]
alwaysApply: false
---

- Use function components.
- No inline styles.
```

### 2.5 Windsurf

Windsurf rules are plain Markdown files. Official material emphasises activation modes rather than a strict file schema: **Manual**, **Always On**, **Model Decision**, and **Glob**.[^windsurf-rules]

---

## 3. What belongs in instructions

Put these in always-on instructions:
- Repository purpose and domain framing.
- Build, test, lint, and validation commands.
- Directory map and source-of-truth files.
- Universal conventions that are not obvious from code alone.
- Hard constraints: safety, compliance, branch rules, required reviewers, test requirements.[^gh-effective][^gh-blog-5tips][^claude-best]

Put these in path-specific instructions:
- Filetype-specific style rules.
- Directory-scoped workflows.
- Domain rules relevant only in one subtree.
- Templates for artefacts such as logs, docs, tests, or papers.[^gh-cli-custom][^gh-effective][^claude-memory]

Put these in skills / workflows / hooks instead:
- Long, stepwise procedures.
- Optional or rare workflows.
- Reusable troubleshooting runbooks.
- Deterministic enforcement steps better handled by automation.[^gh-skills][^claude-best]

Put these in code comments or docs instead:
- Deep API details.
- Large theory sections.
- File-by-file explanations.
- Material that changes frequently.

Rule of thumb: if removing a line would not change agent behaviour in a meaningful way, it probably does not belong in the always-on file.[^claude-best]

---

## 4. Effective instruction design

### 4.1 Put the most important rules first

Models do not treat every line equally. GitHub explicitly recommends short, self-contained statements and warns that long files can be overlooked; code review reads only the first 4,000 characters of each instruction file.[^gh-effective][^gh-review]

Recommended order:
1. Mission-critical prohibitions and must-do rules.
2. Build/test/validation commands.
3. Source-of-truth architecture map.
4. Key conventions.
5. Anti-patterns.
6. Optional cultural guidance.

### 4.2 Use imperative, testable language

Good:
- `Run python -m pytest tests/ -v before merging.`
- `Use src/analytical/ as the source of truth; do not add new model logic under src/browntone/.`
- `Use British English in paper/**.`

Weak:
- `Write good tests.`
- `Follow best practices.`
- `Be careful with security.`

GitHub, Claude, and Windsurf all stress specificity over generic advice.[^gh-effective][^claude-memory][^windsurf-rules]

### 4.3 Keep sections sharply scoped

Each section should answer one question:
- What is this repo?
- Where do I change code?
- How do I verify?
- What must never happen?

Dense narrative prose is worse than headings and bullets.[^gh-review][^claude-memory]

### 4.4 Prefer numbered rules for hard constraints

If a repo has true non-negotiables, numbering helps:
- improves skimmability,
- gives maintainers stable names for rules,
- makes contradictions easier to spot.

### 4.5 Include anti-patterns explicitly

Models respond well to explicit “do not” lists when the forbidden behaviour is common or tempting.

Examples:
- `Do not duplicate the canonical parameter table.`
- `Do not push directly to main.`
- `Do not use pressure-based airborne displacement without labelling it as an overestimate.`

### 4.6 Prefer examples over abstract descriptions

GitHub’s code-review tutorial explicitly recommends concrete examples showing correct and incorrect patterns.[^gh-review]

---

## 5. Token budget and length: how long is too long?

### Published limits

### GitHub Copilot
- **Copilot code review** reads only the **first 4,000 characters** of any custom instruction file.[^gh-effective][^gh-review]
- GitHub does **not** publish an equivalent hard cap for Copilot Chat or coding agent in the docs above, but repeatedly recommends short, self-contained instructions and recommends generated files be **no longer than two pages**.[^gh-effective][^gh-repo-custom]

### Claude Code
- Claude says `CLAUDE.md` files consume context at session start and recommends targeting **under 200 lines per file**; longer files reduce adherence.[^claude-memory]
- Auto memory loads only the **first 200 lines or 25 KB**.[^claude-memory]

### Windsurf
- Official Windsurf guidance gives a hard cap of **6,000 characters per rule file** and **12,000 characters total** across global and workspace rules.[^windsurf-rules]

### Cursor
- Cursor’s official docs emphasise persistent rules and larger-context modes, but public docs do not give a simple universal rule-file token cap on the pages reviewed here.[^cursor-rules][^cursor-max]

### Practical authoring targets

For a repo-maintained instruction system, use these **house targets**:
- **Global always-on file:** aim for 100-200 lines.
- **Path-specific files:** usually 20-80 lines; exceed 120 lines only with good reason.
- **Per-file purpose:** one topic or one subtree.
- **Examples:** short and surgical.

These are not universal vendor limits; they are operational thresholds that reduce drift and instruction dilution.

### What gets ignored first?

Usually the least relevant, least specific, or lowest-priority content. In practice, the most vulnerable material is:
- jokes and lore,
- long prose explanations,
- duplicate rules,
- external references without inline summary,
- weakly worded preferences.

If you want a rule followed, make it short, concrete, high in the file, and broadly applicable.[^gh-effective][^claude-best]

---

## 6. Path-specific instructions: when and how to use them

Use a path-specific file when:
- one subtree has a distinct output format,
- one language/framework needs special rules,
- a workflow is relevant only in one directory,
- the global file is growing because of local exceptions.[^gh-cli-custom][^gh-effective][^gh-path-review]

Good uses in Browntone:
- `paper/**` for JSV writing rules,
- `tests/**` for pytest conventions,
- `docs/research-logs/**` for a mandatory report template,
- `src/analytical/**` for physics and parameter constraints.

Bad uses:
- repeating the global test command in every file,
- copying the same canonical table into multiple files,
- using a path-specific file for rules that actually apply repository-wide.

### Glob guidance

Safe patterns:
- `tests/**`
- `paper/**`
- `src/analytical/**`
- `**/*.py`
- `src/components/**/*.{tsx,jsx}`

Avoid patterns that are too broad unless that is intentional:
- `**`
- `*`

Prefer directory scopes over huge extension-wide scopes when the repo mixes concerns.

---

## 7. Anti-patterns

### Anti-pattern 1: the constitution problem
A giant global file tries to encode everything: repo map, workflows, lore, edge cases, historical notes, and humour. Result: poor adherence and harder maintenance.

### Anti-pattern 2: duplicated source-of-truth blocks
If the same parameter table or command list appears in multiple files, one copy will go stale.

### Anti-pattern 3: vague values language
`Be thoughtful`, `write elegant code`, and `follow best practices` consume context without changing outputs.

### Anti-pattern 4: contradictory layering
If the global file says one thing and a path-specific file says another, Copilot may resolve the conflict non-deterministically.[^gh-cli-custom][^gh-effective]

### Anti-pattern 5: instructions that should be automation
Hooks, CI, linters, and test scripts should enforce what they can. Instruction files are advisory, not guarantees.[^claude-best]

### Anti-pattern 6: relying on external links alone
GitHub code review docs explicitly call out external-link instructions as ineffective; copy the essential rule into the instruction file instead.[^gh-review]

---

## 8. Cross-tool comparison

| Tool | Always-on project file | Scoped file mechanism | Extra mechanisms | Best use |
|---|---|---|---|---|
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/instructions/*.instructions.md` with `applyTo` | `AGENTS.md`, skills | Repo-wide constraints + scoped directory rules |
| Claude Code | `CLAUDE.md` / `.claude/CLAUDE.md` | `.claude/rules/*.md` with `paths` | `@imports`, skills, hooks, auto memory | Lean main memory + modular scoped rules |
| Cursor | `.cursor/rules/*.mdc` / `.cursorrules` | globs and activation modes in rule metadata | Team/user rules, `AGENTS.md`, Max Mode | Modular editor-integrated rules |
| Windsurf | `.windsurfrules` / `.windsurf/rules/*.md` | activation mode incl. glob | memories, workflows | Small explicit rule packs with tight char budgets |

Important conceptual differences:
- **Copilot skills** and **Claude skills** are on-demand; they are not for always-on repo context.[^gh-skills][^claude-best]
- **Windsurf memories** are not version-controlled rules.[^windsurf-intro]
- **Claude auto memory** is learned context, not authored policy.[^claude-memory]
- **Cursor and Windsurf** both place more emphasis on activation mode than GitHub’s simpler global/path-specific split.[^cursor-rules][^windsurf-rules]

---

## 9. Layering strategy: instructions vs skills vs agents vs comments

### Put in `copilot-instructions.md` / `CLAUDE.md`
- universal repo context,
- high-value commands,
- architecture overview,
- hard constraints.

### Put in path-specific instruction files / `.claude/rules`
- local conventions,
- artefact templates,
- subtree-specific safety and style.

### Put in skills
- reusable procedures with multiple steps,
- task packs that should load only when relevant,
- troubleshooting playbooks and operational runbooks.[^gh-skills]

### Put in agents
- specialised personas with a role, SOP, output format, and quality gates.
- use when you want delegation, not just guidance.

### Put in hooks / CI
- deterministic checks such as formatting, linting, blocking writes, or required test runs.[^claude-best]

### Put in code comments / docs
- detailed technical rationale needed by humans near the code.

A good rule system is layered so the always-on surface stays lean.

---

## 10. Browntone assessment

### What is working well

### 10.1 Strong global identity and mission
`.github/copilot-instructions.md` clearly states the project identity, venue, physics context, canonical parameters, and lab structure. That is high-value context an agent cannot infer cheaply from code alone.

### 10.2 Hard constraints are explicit
The numbered rule structure (`R0`, `R1`, …) is excellent for true non-negotiables: git workflow, canonical parameters, review standards, writing standards.

### 10.3 Path-specific files are sensibly divided
The current path-specific set is exactly what GitHub recommends: global rules plus local files for `paper/**`, `tests/**`, `docs/research-logs/**`, `.github/agents/**`, and `src/analytical/**`.

### 10.4 Local files are task-shaped
The paper, tests, research-log, and analytical files each tell the agent what “good” looks like in that subtree. This is much better than one monolithic global file.

### What could be improved

### 10.5 The global file is probably too long for some surfaces
Current size is about **308 lines / 13,886 characters**. That is workable for coding agents with larger context, but it is far beyond Copilot code review’s 4,000-character per-file limit, and it increases dilution risk everywhere else.

**Recommendation:** split the file into:
- a short always-on core,
- path-specific files for specialised domains,
- optional skills for lore-heavy or workflow-heavy sections.

### 10.6 Some content is culturally rich but operationally optional
Sections such as the academic calendar, coffee machine, loving spouse, and similar lab lore are memorable and valuable to humans, but they are not equally relevant on every coding turn.

**Recommendation:** keep a brief cultural note in the global file, but move the detailed behavioural scripts to skills or agent definitions.

### 10.7 Duplicated facts create drift risk
Canonical parameters and testing expectations appear in multiple places. Historical copies in this repository drifted to **118** and **183** tests, while the current canonical count is **203**.

**Recommendation:** keep one canonical source for counts and frequently changing numbers, and reference it briefly elsewhere.

### 10.8 Some path-specific files can be even leaner
For example, `analysis.instructions.md` and `paper.instructions.md` both restate large canonical-parameter blocks. That helps local compliance, but duplicated tables are expensive in tokens.

**Recommendation:** keep a short “canonical parameters must match the repo standard” rule in scoped files and reserve the full table for one authoritative location unless repeated numbers are absolutely mission-critical.

### 10.9 The top of the global file should become more triaged
Right now important operational rules share space with broader context. For stronger adherence, the top section should be a short **Critical rules first** block:
- branch protection / PR workflow,
- test command,
- source-of-truth directories,
- canonical physics constraints.

### 10.10 Consider an interoperability layer
Because Copilot, Claude Code, and some editors now recognise `AGENTS.md` or `CLAUDE.md`, Browntone could benefit from a small cross-tool shim:
- either a root `AGENTS.md` that mirrors the short core rules,
- or a root `CLAUDE.md` importing the same shared text.

Keep the shared layer short and tool-agnostic.

---

## 11. Annotated examples from Browntone

### Good example: scoped paper-writing guidance
File: `.github/skills/write-paper/SKILL.md`

Why it works:
- narrow scope (`paper/**`),
- concrete journal style rules,
- explicit canonical values,
- clear anti-errors section,
- compile command included.

### Good example: research log template
File: `.github/skills/write-research-log/SKILL.md`

Why it works:
- forces a deliverable shape,
- requires quantitative findings,
- includes reviewer-report extension.

### Good example: analytical source-of-truth note
File: `.github/skills/write-analysis/SKILL.md`

Why it works:
- names the core dataclass and source module,
- lists the main APIs,
- includes testing expectations.

### Improvement example: global file length
File: `.github/copilot-instructions.md`

Why it needs attention:
- excellent content density overall, but too much of it is always-on.
- some sections are rules; some are lore; some are workflow guides; some are a project handbook.

A better pattern is:
1. **Core always-on rules**,
2. **scoped files**,
3. **skills for long workflows**,
4. **agents for specialised roles**.

---

## 12. Quick review checklist

Before merging any instruction-file change, check:

### Scope
- [ ] Is this guidance always relevant? If not, move it to a scoped file or skill.
- [ ] Is the file in the right location for the intended tool?
- [ ] Is the glob tight enough?

### Quality
- [ ] Are the first 10-20 lines the most important ones?
- [ ] Are rules imperative and testable?
- [ ] Are examples short and concrete?
- [ ] Are headings and bullets used instead of dense prose?

### Consistency
- [ ] Does this duplicate facts already stated elsewhere?
- [ ] Could it contradict another instruction file?
- [ ] Are counts, commands, paths, and parameter values current?

### Budget
- [ ] Is the file short enough for its tool?
- [ ] Could any section move to a skill, hook, or ordinary doc?
- [ ] For Copilot code review, is each relevant file’s critical content inside the first 4,000 characters?

### Validation
- [ ] Did we test the behaviour on a realistic task?
- [ ] Did we verify that the right scoped file actually triggers?
- [ ] Did we prune obsolete guidance instead of only adding new text?

---

## 13. Suggested Browntone house style for future instruction files

Use this template unless there is a good reason not to:

```md
---
applyTo: "path/**"
---

# Short title

One sentence: what this file governs.

## Critical rules
- Rule 1
- Rule 2

## Required commands / validation
- Command 1
- Command 2

## Local conventions
- Convention 1
- Convention 2

## Anti-patterns
- Do not ...
- Never ...
```

For the global file:

```md
# Project name

## Critical rules
- Top 5-10 must-follow rules only

## Project overview
- Elevator pitch

## Architecture map
- Source-of-truth directories

## Build, test, lint
- Verified commands

## Universal conventions
- Naming, safety, review

## Anti-patterns
- Known failure modes
```

---

## Sources

[^gh-cli-custom]: GitHub Docs, “Adding custom instructions for GitHub Copilot CLI”: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
[^gh-repo-custom]: GitHub Docs, “Adding repository custom instructions for GitHub Copilot”: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
[^gh-support]: GitHub Docs, “Support for different types of custom instructions”: https://docs.github.com/en/copilot/reference/custom-instructions-support
[^gh-effective]: GitHub Docs, “About customizing Copilot responses” / “Writing effective custom instructions”: https://docs.github.com/en/copilot/concepts/prompting/response-customization#writing-effective-custom-instructions
[^gh-review]: GitHub Docs, “Using custom instructions to unlock the power of Copilot code review”: https://docs.github.com/en/copilot/tutorials/use-custom-instructions
[^gh-skills]: GitHub Docs, “Creating agent skills for GitHub Copilot”: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills
[^gh-agents-md]: GitHub Blog, “Copilot coding agent now supports AGENTS.md custom instructions”: https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/
[^gh-path-review]: GitHub Blog, “Copilot code review: Path-scoped custom instruction file support”: https://github.blog/changelog/2025-09-03-copilot-code-review-path-scoped-custom-instruction-file-support/
[^gh-blog-5tips]: GitHub Blog, “5 tips for writing better custom instructions for Copilot”: https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/
[^vscode-custom]: VS Code Docs, “Use custom instructions in VS Code”: https://code.visualstudio.com/docs/copilot/customization/custom-instructions
[^claude-memory]: Claude Code Docs, “How Claude remembers your project”: https://code.claude.com/docs/en/memory
[^claude-best]: Claude Code Docs, “Best practices for Claude Code”: https://code.claude.com/docs/en/best-practices
[^cursor-rules]: Cursor Docs, “Rules”: https://cursor.com/docs/rules and https://cursor.com/help/customization/rules
[^cursor-max]: Cursor Docs, “Max Mode”: https://cursor.com/help/ai-features/max-mode
[^windsurf-intro]: Windsurf University, “Intro to Rules, Workflows & Memories”: https://windsurf.com/university/general-education/intro-rules-memories
[^windsurf-rules]: Windsurf University, “Enforce Coding Standards with Rules”: https://windsurf.com/university/general-education/creating-modifying-rules
