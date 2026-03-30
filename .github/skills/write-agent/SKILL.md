---
name: write-agent
description: >-
  Custom agents create specialized Copilot helpers for recurring jobs by
  giving them a focused role, prompt, model, and tool access.  Use this
  skill to author an .agent.md, set up .github/agents, configure
  specialized Copilot personas, or orchestrate parallel subagents with
  embedded instruction files.
license: MIT
---

# Authoring Custom Agents for GitHub Copilot CLI

Custom agents are specialized Copilot personas with tailored expertise, tool access, and behavioral instructions. Author them as `.agent.md` files — typically in `.github/agents/` for a repository — so Copilot CLI can surface them as agent profiles and delegate matching tasks to them.

## Procedure: Authoring a Custom Agent

1. **Decide whether a custom agent is the right mechanism** — for simple coding conventions, author custom instructions instead. For task-specific procedures without a persona, author a skill instead (see the `write-skill` and `write-instructions` skills).
2. **Inspect existing agents** — check `.github/agents/` and `~/.copilot/agents/` for existing agents to avoid naming conflicts and match conventions.
3. **Define the agent's specialty** — articulate who this agent is, what it does, and what tasks should trigger delegation to it. This becomes the `description` field, so lead with the purpose and then include likely trigger phrases.
4. **Choose the tool set** — decide which tools the agent needs. Constrain tools to the minimum required for the agent's role.
5. **Author the `.agent.md` file** — author the YAML frontmatter, then a Markdown prompt body defining the agent's behavior, responsibilities, and constraints.
6. **Review as if new to the repo** — re-read the agent profile from the perspective of someone unfamiliar with the project. The description should clearly convey when Copilot should delegate to this agent, and the prompt body should define clear boundaries.
7. **Test the agent** — invoke it with `/agent`, select it, and verify it behaves as expected. Confirm auto-delegation triggers correctly (or does not, if `disable-model-invocation: true`).

## When to Author a Custom Agent (vs Other Customization)

- **Author a custom agent** when you need a specialist persona, constrained tools, or automatic delegation for a domain.
- **Author custom instructions** for broad, always-on conventions that apply to every task.
- **Author a skill** for task-specific procedures that don't require a separate persona or tool constraints.

## File Format

Custom agents are Markdown files with YAML frontmatter, using the `.agent.md` extension.

**Filename:** `<agent-name>.agent.md`
- Allowed characters: `.`, `-`, `_`, `a-z`, `A-Z`, `0-9`
- The filename (minus `.agent.md`) is used as the default agent name if `name` is not set in frontmatter

## Placement

| Scope | Location |
|-------|----------|
| **Repository-level** | `.github/agents/` in the repo |
| **User-level / personal** | `~/.copilot/agents/` |
| **Organization/Enterprise** | `/agents/` in the `.github-private` repo |

**Precedence on naming conflicts:** system > repository > organization. Personal agents are an additional local scope; avoid reusing names that could cause ambiguous selection across scopes.

## YAML Frontmatter Properties

`description` is the only required frontmatter property. Copilot CLI also supports `name`, `tools`, `model`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, `metadata`, and `target`.

```yaml
---
name: my-agent-name
description: What this agent does and its area of expertise
tools: ["read", "search", "edit"]
model: claude-sonnet-4.5
disable-model-invocation: false
user-invocable: true
---
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | No | Display name. Defaults to filename without extension. |
| `description` | string | **Yes** | Purpose and capabilities. Copilot uses this to decide when to auto-delegate. |
| `tools` | list/string | No | Tools the agent can use. Omit for all tools. `[]` for no tools. |
| `model` | string | No | AI model to use. Inherits default if unset. |
| `disable-model-invocation` | boolean | No | When `true`, agent must be manually selected — Copilot won't auto-delegate to it. Default: `false`. |
| `user-invocable` | boolean | No | When `false`, agent can only be invoked programmatically. Default: `true`. |
| `mcp-servers` | object | No | MCP servers available only to this agent. |
| `metadata` | object | No | Arbitrary key-value pairs for documentation/tracking. |
| `target` | string | No | Restrict to `vscode` or `github-copilot` environment. Omit for both. |

> `infer` is retired. Use `disable-model-invocation` to control whether Copilot may auto-delegate to the agent.

For most agents, author `description` first, then add the other properties only when they are needed to constrain behavior, tool access, or availability.

## Tool Configuration

### Enable All Tools (default)

```yaml
# Omit the tools property entirely, or:
tools: ["*"]
```

### Enable Specific Tools

```yaml
tools: ["read", "search", "edit", "execute"]
```

### Tool Aliases

| Alias | Covers | Purpose |
|-------|--------|---------|
| `execute` | `shell`, `Bash`, `powershell` | Run shell commands |
| `read` | `Read`, `NotebookRead` | Read file contents |
| `edit` | `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | Modify files |
| `search` | `Grep`, `Glob` | Search files and content |
| `agent` | `custom-agent`, `Task` | Invoke other agents |
| `web` | `WebSearch`, `WebFetch` | Web search and fetch |

### MCP Server Tools

Reference tools from specific MCP servers using `server-name/tool-name`:

```yaml
tools: ["read", "search", "github/list_pull_requests", "custom-mcp/*"]
```

## Prompt Body

Below the frontmatter, author the agent's behavioral instructions in Markdown. This defines the agent's expertise, workflow, and constraints.

**Maximum length:** 30,000 characters.

### Structure

1. **Role statement** — who the agent is and what it specializes in
2. **Responsibilities** — specific tasks and behaviors
3. **Constraints** — what the agent should NOT do
4. **Workflow** — step-by-step approach for common tasks

### Example: Testing Specialist

```markdown
---
name: test-specialist
description: Focuses on test coverage, quality, and testing best practices without modifying production code
---

You are a testing specialist focused on improving code quality through comprehensive testing. Your responsibilities:

- Analyze existing tests and identify coverage gaps
- Write unit tests, integration tests, and end-to-end tests following best practices
- Review test quality and suggest improvements for maintainability
- Ensure tests are isolated, deterministic, and well-documented
- Focus only on test files and avoid modifying production code unless specifically requested

Always include clear test descriptions and use appropriate testing patterns for the language and framework.
```

### Example: Implementation Planner (Constrained Tools)

```markdown
---
name: implementation-planner
description: Plans implementations and authors technical specifications in markdown format
tools: ["read", "search", "edit"]
---

You are a technical planning specialist. Your responsibilities:

- Analyze requirements and break them into actionable tasks
- Author detailed technical specifications and architecture docs
- Generate implementation plans with clear steps and dependencies
- Document API designs, data models, and system interactions

Focus on creating thorough documentation rather than implementing code.
Always structure plans with clear headings, task breakdowns, and acceptance criteria.
```

### Example: Manual-Only Destructive Agent

```markdown
---
name: schema-migrator
description: Reviews and applies high-risk database schema changes when explicitly asked to plan or execute migrations
tools: ["read", "search", "execute"]
disable-model-invocation: true
user-invocable: true
---

You are a database migration specialist.

- Review proposed schema changes for risk, rollout order, and rollback steps
- Require an explicit user request before executing destructive commands
- Prefer dry runs, backups, and staged rollout guidance when available
- Clearly call out downtime, locking, or data-loss risk before proceeding
```

### Example: Agent with MCP Server

```markdown
---
name: db-assistant
description: Helps with database queries, schema design, and data management
tools: ["read", "search", "edit", "execute", "db-mcp/query", "db-mcp/schema"]
mcp-servers:
  db-mcp:
    type: local
    command: db-mcp-server
    args: ["--connection-string", "$DB_CONNECTION"]
    tools: ["*"]
    env:
      DB_CONNECTION: ${{ secrets.DB_CONNECTION_STRING }}
---

You are a database specialist. Help with query writing, schema design,
and data management tasks.
```

## How Custom Agents Are Invoked (Context for Authors)

Understanding how agents are invoked helps you author better descriptions and tool constraints.

### Select Interactively

```
/agent
```

Then use arrow keys to select from the list.

### Reference in a Prompt

```
Use the test-specialist agent to review test coverage for the auth module.
```

Copilot infers the correct agent from the prompt.

If `user-invocable` is `false`, do not expect the agent to appear as a user-selectable option even if its profile is otherwise valid.

### Command-Line Argument

```bash
copilot --agent=test-specialist --prompt "Review test coverage"
```

### Automatic Delegation

When `disable-model-invocation` is `false` (the default), Copilot may automatically delegate tasks to the agent when the task matches the agent's `description`. This is why the description field is critical — it controls when auto-delegation triggers.

## Embedded Subagent Instructions

### The Problem

Agent discovery is flat — only `.agent.md` files directly in `.github/agents/` are registered. Every agent file in that directory appears in the `/agent` list and is eligible for auto-delegation. When an agent needs to orchestrate specialist subagents (e.g., a code reviewer that dispatches security, logic, and style checks in parallel), placing each subagent as its own `.agent.md` pollutes the agent list with internal implementation details that users should never invoke directly. The `user-invocable: false` property still requires the file in `.github/agents/` and still registers it — it doesn't solve the discoverability problem.

### The Solution: Instruction Files Referenced via the `task` Tool

Keep subagent instructions as plain Markdown files in a **subdirectory** — not as `.agent.md` files in `.github/agents/`. Because subdirectories are not scanned for agents, these files are invisible to `/agent` listing and auto-delegation. The parent agent spawns subagents via the `task` tool, passing a prompt that tells the subagent to read and follow a specific instruction file.

This is the agent-side analog of the dispatcher pattern for skills (see the `write-skill` skill's "Scaling Skills: The Dispatcher Pattern" section). Where a dispatcher skill routes to deep content files that the **same** agent reads, a parent agent routes to instruction files that **separate subagents** read — enabling parallel execution and model selection per subagent.

```
.github/agents/
├── code-reviewer.agent.md          # Parent agent: dispatches to subagents
└── code-reviewer/                  # Subdirectory: NOT discovered as agents
    └── reviewers/
        ├── security.md             # Subagent instructions: security review
        ├── logic.md                # Subagent instructions: logic review
        └── style.md                # Subagent instructions: style review
```

### Placement Options

| Placement | Path | Best when |
|-----------|------|-----------|
| **Co-located with parent** | `.github/agents/<parent-name>/` | Instructions are tightly coupled to one parent agent |
| **Inside a skill directory** | `.github/skills/<skill>/subagents/` | A skill needs to spawn subagents as part of its procedure |
| **Dedicated directory** | `.github/subagents/` | Multiple parents share the same instruction files |

### Parent Agent Example

```markdown
---
name: code-reviewer
description: >-
  Reviews code changes for security vulnerabilities, logic errors, and style
  issues by dispatching parallel specialist reviewers.  Use when asked to
  review a PR, audit code quality, or check for bugs.
tools: ["read", "search", "agent"]
---

You are a code review orchestrator. When asked to review code:

1. Identify the code to review (diff, file, or snippet).
2. Spawn three parallel subagents using the `task` tool, each with
   `agent_type: "general-purpose"`:
   - **Security** — prompt: "Read and follow the instructions in
     `.github/agents/code-reviewer/reviewers/security.md`. Then perform
     a security review of this code: ..."
   - **Logic** — prompt: "Read and follow the instructions in
     `.github/agents/code-reviewer/reviewers/logic.md`. Then perform
     a logic review of this code: ..."
   - **Style** — prompt: "Read and follow the instructions in
     `.github/agents/code-reviewer/reviewers/style.md`. Then perform
     a style review of this code: ..."
3. Collect the results from all three subagents.
4. Synthesize a unified review with sections for each category.

Choose the model for each subagent based on the task:
- Security reviews benefit from stronger reasoning (`claude-opus-4.6`)
- Logic and style reviews work well with fast models (`gpt-5.4`)
```

### When to Use Embedded Subagent Instructions

- A parent agent orchestrates **parallel specialist tasks** that benefit from separate context windows (e.g., reviewing code from multiple angles simultaneously).
- You need **different models** for different subtasks (e.g., a stronger model for security analysis, a faster model for style checks).
- Subagent logic is complex enough to warrant its own instruction file (~50+ lines) but should not be user-visible as a standalone agent.
- Multiple parent agents need to **share the same subagent instructions** — put them in a common location and reference from each parent.

### When NOT to Use It

- The parent agent can handle all subtasks itself in a single pass. Don't over-engineer a sequential checklist into parallel subagents.
- The subtask is simple enough to express inline in the parent's `task` tool prompt. Only extract to a file when the instructions are substantial.
- The subagent needs its own frontmatter properties (model, tools, MCP servers). In that case, it must be a real `.agent.md` file — use `disable-model-invocation: true` and `user-invocable: false` to minimize noise.

### Guidelines for Writing Subagent Instruction Files

1. **Structure like a SKILL.md body** — include a role statement, procedure, rules, and done criteria. They just lack frontmatter since they are not discovered as agents or skills.
2. **Be self-contained** — a subagent starts with no context beyond what the parent provides in the prompt. The instruction file should include everything the subagent needs to know to do its job.
3. **Define scope boundaries** — explicitly state what the subagent should and should NOT comment on. This prevents overlap when multiple subagents review the same code.
4. **Include output format requirements** — tell the subagent how to structure its response so the parent can synthesize results consistently.
5. **Keep files focused** — one instruction file per specialty. If a file grows beyond ~150 lines, consider splitting it further.
6. **Cross-reference freely** — instruction files can tell the subagent to read additional files (templates, rule lists, project configs) as needed.

## Done Criteria

- `.agent.md` file created in the correct location with valid frontmatter
- `description` clearly conveys when Copilot should auto-delegate to this agent
- Tools constrained to the minimum required for the agent's role
- Prompt body defines clear behavioral boundaries (what to do AND what not to do)
- Agent tested via `/agent` selection and auto-delegation verified (or `disable-model-invocation` confirmed)
- No naming conflicts with existing agents

## Best Practices for Authoring Agents

1. **Author a clear description** — this is how Copilot decides when to delegate. Include the domain and trigger keywords.
2. **Constrain tools appropriately** — a read-only auditing agent should not have `edit` or `execute` tools.
3. **Define clear boundaries** — state what the agent should and should NOT do.
4. **Keep the prompt focused** — a 30,000 character limit is generous, but concise instructions outperform verbose ones.
5. **Use `disable-model-invocation: true`** for agents that should only be invoked explicitly (e.g., destructive operations).
6. **Test the agent** — invoke it with `/agent` and verify it behaves as expected before sharing.
7. **Version with your code** — agent profiles in `.github/agents/` are version-controlled and can be branched.
8. **Use embedded subagent instructions for orchestration** — when an agent dispatches parallel specialist tasks, keep subagent instruction files in a subdirectory rather than registering each as its own `.agent.md`. This keeps the agent list clean and scopes subagent logic to the parent that owns it.
9. **State what the agent does NOT do** — when multiple agents share a domain, each should explicitly list responsibilities it excludes. A "What You Do NOT Focus On" section eliminates overlap and makes delegation boundaries unambiguous, even as new agents are added to the same area.
10. **Define a structured output template** — specify the exact format the agent should produce (headers, sections, tables, or an explicit lack thereof). Consistent output is easier to synthesize across agents, easier to parse programmatically, and prevents free-form drift over time.
11. **Treat the tool list as a safety boundary** — constraining tools is not just convenience; it is a structural safety mechanism. A read-only advisor that lacks `edit` and `execute` tools is physically prevented from causing side effects, regardless of prompt adherence. Design tool lists around the principle of least privilege and resist expanding them over time.
