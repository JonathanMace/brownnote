---
name: write-instructions
description: >-
  Enforce coding standards, workflow rules, and persistent behavioral
  guidance across all Copilot sessions by authoring instruction files
  that load automatically.  Use when asked to author custom instructions,
  configure copilot-instructions, or set up repo instructions.
license: MIT
---

# Authoring Custom Instructions for GitHub Copilot CLI

Custom instructions are persistent natural-language guidance that Copilot CLI automatically includes from supported instruction files. They capture coding conventions, project context, workflow expectations, and communication preferences so you do not need to repeat them in every prompt.

## Procedure: Authoring Custom Instructions

1. **Decide the instruction scope** — does this guidance belong in repository-wide instructions, path-specific instructions, or local instructions?
2. **Inspect existing instructions** — check for `.github/copilot-instructions.md` and `.github/instructions/` so you can avoid contradictions and extend the right file.
3. **Choose the right file type** (see [Instruction Types](#instruction-types) below).
4. **Author the file** — use short, self-contained statements in Markdown. For path-specific files, add the required `applyTo` frontmatter.
5. **Prioritize critical rules first** — Copilot code review only reads the first 4,000 characters of instruction files.
6. **Review as if new to the repo** — re-read your instructions from the perspective of someone unfamiliar with the project. Each statement should stand alone without requiring external context.
7. **Choose a different customization when needed** — if you need reusable task procedures, author a skill instead (see `writing-skills`). If you need a specialized persona or tool constraints, author a custom agent instead (see `writing-custom-agents`). If you need automation around session or tool events, author hooks instead (see `writing-hooks`).
8. **Test your instructions** — start a new CLI session (or use `/instructions` to verify they are active) and submit a prompt to confirm Copilot follows the guidance.

## Instruction Types

| Type | File Location | Scope |
|------|--------------|-------|
| **Repository-wide** | `.github/copilot-instructions.md` | All tasks in this repo |
| **Path-specific** | `.github/instructions/**/*.instructions.md` | Tasks involving files matching a glob pattern |
| **Local/personal** | `$HOME/.copilot/copilot-instructions.md` | All repos for this user |
| **Additional instruction dirs** | Directories listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Extra locations for the same instruction file types |

### Precedence (highest to lowest)

1. Path-specific instructions (`.github/instructions/**/*.instructions.md`)
2. Repository-wide instructions (`.github/copilot-instructions.md`)
3. Local/personal instructions

All matching instructions are combined and provided to Copilot. Avoid conflicts between levels — conflicting instructions produce non-deterministic behavior.

## Repository-Wide Instructions

### File: `.github/copilot-instructions.md`

This is the primary instruction file. Its contents are sent with every prompt in this repo.

```markdown
# Project Guidelines

- Language: TypeScript in strict mode
- Formatter: Prettier with default config
- Linter: ESLint with @typescript-eslint
- Tests: Jest with React Testing Library
- Use early returns; avoid deep nesting
- Prefer named exports over default exports
```

### What to Include

- **Project overview** — purpose, architecture, key components
- **Tech stack** — languages, frameworks, libraries, versions
- **Coding standards** — naming conventions, formatting rules, patterns to prefer/avoid
- **Build and test commands** — how to build, lint, test
- **Folder structure** — key directories and their purposes

### What to Avoid

- Task-specific procedures (author a **skill** instead)
- References to external documents Copilot cannot access
- Instructions so lengthy they crowd out the actual user prompt
- Overly prescriptive style rules that conflict with varied tasks

## Path-Specific Instructions

### Location: `.github/instructions/**/*.instructions.md`

These files provide targeted guidance for specific parts of the codebase. They activate when Copilot is working on files that match the `applyTo` glob pattern.

`applyTo` is required. Without it, the file is not a valid path-specific instruction file.

### Format

```markdown
---
applyTo: "src/frontend/**/*.tsx"
---

- Use React function components with hooks
- Use Tailwind CSS for styling; avoid inline styles
- All components must have PropTypes or TypeScript interfaces
- Prefer composition over inheritance
```

### `applyTo` Glob Syntax

| Pattern | Matches |
|---------|---------|
| `*` | All files in current directory |
| `**` or `**/*` | All files recursively |
| `*.py` | `.py` files in current directory |
| `**/*.py` | `.py` files at any depth |
| `src/**/*.ts` | `.ts` files anywhere under `src/` |
| `**/*.ts,**/*.tsx` | Multiple patterns, comma-separated |

### Optional: `excludeAgent`

Restrict which Copilot agent sees the instructions:

```markdown
---
applyTo: "**"
excludeAgent: "code-review"
---

These instructions are only used by the coding agent, not code review.
```

Valid values: `"code-review"`, `"coding-agent"`.

### Organization Tips

```
.github/instructions/
├── frontend.instructions.md     # applyTo: "src/frontend/**"
├── backend.instructions.md      # applyTo: "src/api/**"
├── testing.instructions.md      # applyTo: "**/*.test.*,**/*.spec.*"
└── database/
    └── migrations.instructions.md  # applyTo: "**/migrations/**"
```

Name files descriptively. Use subdirectories to organize by domain.

## Local Instructions

### File: `$HOME/.copilot/copilot-instructions.md`

Personal instructions that apply to all your Copilot CLI sessions, regardless of repository. Useful for individual preferences:

```markdown
- Prefer concise explanations
- Always show the file path when editing files
- Use American English spelling
```

Directories listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` can provide additional shared instruction files without changing the repository itself. Reuse the same file formats there rather than inventing a new structure.

## CLI Commands for Instructions

| Command | Purpose |
|---------|---------|
| `/instructions` | View active instruction files and toggle them on/off |
| `/init` | Initialize Copilot instructions for a repository (creates starter files) |

## Done Criteria

An authored instruction change is done when:

- The chosen file type matches the intended scope.
- Required structure is present (`applyTo` for path-specific files, correct filenames and locations for the other instruction types).
- The most important rules appear early enough to survive the 4,000-character code-review limit.
- The instructions do not conflict with other active instruction files.
- You have verified activation in a new session or with `/instructions`.

## Best Practices for Authoring Instructions

1. **Keep instructions lean** — every instruction consumes context tokens on every prompt. Only include what is broadly relevant.
2. **Use path-specific files for specialized rules** — don't put frontend rules in the global file if they only matter for `.tsx` files.
3. **Avoid contradictions** — conflicting instructions across files produce unpredictable results.
4. **Put the most important rules first** — code review only reads the first 4,000 characters of each custom instruction file.
5. **Extract procedures into skills** — if you find yourself writing step-by-step task procedures in instructions, author a skill instead (see the `writing-skills` skill).
6. **Test your instructions** — after authoring or editing, start a new CLI session and verify Copilot follows the guidance.
7. **Commit and share** — repository instructions are version-controlled and shared across the team. Review changes to instructions like code changes.
8. **Make instructions self-updating** — include an explicit rule like "If you discover a useful pattern or anti-pattern during this session, add it to this file immediately." This turns the instruction file into persistent cross-session memory that grows organically from real usage instead of letting hard-won discoveries die when a session ends.
9. **Blacklist stale values, not just prescribe new ones** — when a configuration value, API version, pattern, or convention changes, add a line stating the old value must not appear (e.g., "OLD: `timeout=30` — MUST NOT be used; current value is `timeout=15`"). This prevents silent regression to outdated defaults that agents may encounter in existing code or training data.
