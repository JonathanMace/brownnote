---
name: write-agent
description: >
  Guide for writing effective Copilot CLI agent definitions. Use when creating, reviewing, or restructuring Browntone custom agents under .github/agents/.
---

# Agent Definition Authoring Guide

Practical reference for AI agents writing or reviewing custom agent definitions in this repository. This guide is written primarily for **GitHub Copilot custom agents** and secondarily for **Claude Code**, **Cursor**, and similar agentic coding tools.

## 1. What this document is for

Use this guide when you are:

- creating a new file in `.github/agents/`
- reviewing an existing `.agent.md` file
- deciding whether something should be an **agent**, **skill**, or **instruction**
- trying to make an agent more reliable, more portable, or safer

The aim is not merely to produce a syntactically valid file. The aim is to produce an agent definition that is:

- easy for the platform to route correctly
- narrow enough to behave consistently
- explicit enough to avoid damage
- structured enough to return useful output
- portable across Copilot surfaces where possible

## 2. First principles

For GitHub Copilot, a custom agent is a **persistent persona plus tool policy plus operating manual**. Official docs describe custom agents as tailored teammates defined once in Markdown so you do not need to keep restating the same workflow, conventions, and tool access.[^gh-about] In GitHub Copilot CLI, work performed by a custom agent is carried out by a **subagent with its own context window**, which helps offload specialised work without cluttering the main conversation.[^gh-cli]

That leads to five practical design rules:

1. **One agent, one job.** Do not build a “general helper”.
2. **Description is routing metadata.** Write it so the platform knows *when* to invoke the agent.
3. **Persona shapes behaviour.** A strong identity changes output quality and consistency.
4. **Tools define blast radius.** Restrict them deliberately.
5. **The body is the real spec.** Tell the agent exactly how to think, what to inspect, what to output, and what never to do.

## 3. Agents vs skills vs instructions

Use the right customization surface.

| Surface | Best for | Loaded when | Typical contents |
|---|---|---|---|
| `.github/copilot-instructions.md` plus supporting skills | Always-on repository guidance plus reusable workflow support | Every relevant interaction or when a skill is invoked | coding standards, canonical parameters, file-specific rules, validation workflows |
| `.github/agents/*.agent.md` | Persistent specialist persona with tool restrictions and workflow | When selected explicitly or inferred from description | role, trigger conditions, SOP, output format, constraints |
| `.github/skills/<skill>/SKILL.md` | Reusable task workflow, scripts, or supporting resources | On demand / when invoked | step-by-step procedures, helper assets, validation steps |

VS Code’s own guidance is crisp: use **custom agents** for a persistent persona with specific tools or model preferences; use **prompt files** for one-off tasks; use **skills** for portable, reusable capabilities with scripts and resources.[^vscode-agents] GitHub Copilot CLI docs make the same distinction indirectly: agent files define expertise and behaviour, while skills package reusable workflows.[^gh-cli][^gh-skills]

### Practical rule

- If it should always apply to a directory or file type, write an **instruction**.
- If it is a reusable procedure that many agents may call, write a **skill**.
- If it is a specialist “teammate” with a role, voice, and bounded authority, write an **agent**.

## 4. File location, naming, and precedence

### GitHub Copilot

- **Project-level**: `.github/agents/<name>.agent.md`
- **User-level**: `~/.copilot/agents/<name>.agent.md`
- **Organisation / enterprise**: `/agents/` in a `.github-private` repository on GitHub.com[^gh-about][^gh-cli]

GitHub’s configuration reference says the **file name minus `.md` or `.agent.md` is used for deduplication**, and the lowest-level definition takes precedence.[^gh-config]

### Naming guidance

Use lowercase kebab-case for the file name and agent `name`:

- good: `reviewer-b.agent.md`
- good: `docs-writer.agent.md`
- avoid: `Reviewer B.agent.md`
- avoid: `My Great Agent.agent.md`

GitHub’s CLI docs explicitly recommend lowercase letters and hyphens for ease of programmatic use.[^gh-cli]

## 5. File format

GitHub Copilot custom agents are Markdown files with YAML frontmatter followed by a Markdown body.[^gh-config][^gh-about][^vscode-agents]

Minimal Copilot example:

```md
---
name: docs-writer
description: Writes or improves repository documentation. Use when README, docs/, or usage guidance needs updating.
tools: [read, edit, search]
---

You are a documentation specialist.

## Identity
- You write concise, accurate developer documentation.

## When to activate
- Use for README updates, docs fixes, and API usage explanations.

## Standard operating procedure
1. Read the relevant source files first.
2. Update only documentation.
3. Validate any documented commands if practical.

## Output format
- Summary of files changed
- Key doc decisions

## Constraints
- Never edit application source code unless explicitly asked.

## Quality gates
- Every documented command must be plausible and current.
```

### Body size

GitHub’s custom-agents reference sets a maximum prompt/body length of **30,000 characters**.[^gh-config]

## 6. YAML frontmatter: what is required vs optional

### GitHub Copilot core fields

The safest cross-surface subset for Copilot is:

| Field | Status | Notes |
|---|---|---|
| `description` | **Required** | Official docs consistently treat this as the key routing field.[^gh-config][^vscode-agents] |
| `name` | Recommended | Used in UI; if omitted, filename is used.[^gh-config][^vscode-agents] |
| `tools` | Optional | Omit for all tools; `[]` for none; list for least privilege.[^gh-config] |
| `model` | Optional | Can be a single model or, in VS Code, a prioritised list.[^vscode-agents] |

### GitHub Copilot additional fields

These exist, but support varies by surface:

| Field | Meaning | Notes |
|---|---|---|
| `user-invocable` | Whether user can select the agent directly | Supported in VS Code / Copilot config docs.[^vscode-agents][^gh-config] |
| `disable-model-invocation` | Prevent other agents from invoking it as a subagent | Supported in VS Code / Copilot config docs.[^vscode-agents][^gh-config] |
| `target` | Environment context such as `vscode` or `github-copilot` | Mainly useful for cross-surface compatibility.[^vscode-agents] |
| `mcp-servers` | Agent-specific MCP server config | Supported in GitHub custom-agent config; some IDE support differs.[^gh-config] |
| `agents` | Allowed subagents | VS Code feature; if used, include the `agent` tool.[^vscode-agents] |
| `handoffs` | Guided transitions to another agent | VS Code feature; ignored on GitHub.com coding agent today.[^vscode-agents][^gh-config] |
| `argument-hint` | UI hint text | VS Code feature.[^vscode-agents] |
| `hooks` | Agent-scoped hooks | Preview feature in VS Code.[^vscode-agents] |

### Claude Code frontmatter

Claude Code uses a similar Markdown-plus-YAML pattern, but its schema is richer: `name` and `description` are required; optional fields include `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, and others.[^claude-subagents]

### Cursor

Cursor’s nearest equivalents are not a direct `.agent.md` match. Cursor primarily uses:

- `.cursor/rules/*.mdc` for scoped rules
- mode / agent configuration in Cursor settings or `.cursor/modes.json`
- `AGENTS.md` as a cross-tool compatibility layer in some workflows[^cursor-rules]

So if you are writing for Cursor specifically, do **not** assume Copilot’s `.agent.md` schema carries over unchanged.

## 7. Tool selection and least privilege

GitHub’s custom-agent config docs define the main portable tool aliases as follows:[^gh-config]

| Portable alias | Compatible aliases | Meaning |
|---|---|---|
| `execute` | `shell`, `bash`, `powershell` | run commands |
| `read` | `Read`, `NotebookRead` | read files |
| `edit` | `Edit`, `Write`, `MultiEdit`, `NotebookEdit` | edit files |
| `search` | `Grep`, `Glob` | search files or contents |
| `agent` | `custom-agent`, `Task` | invoke another agent |
| `web` | `WebSearch`, `WebFetch` | web access |
| `todo` | `TodoWrite` | task-list management; not universally supported |

### Important practical recommendation

For **GitHub Copilot portability**, prefer the documented aliases:

- `read`
- `edit`
- `search`
- `execute`
- `agent`
- `web`

Avoid repository-local or runtime-specific tool spellings unless you have a strong reason.

### Important Browntone note: public docs vs current repo house style

The Browntone house style captured in this skill still discusses the older `read_file`, `edit_file`, `powershell`, `grep`, and `glob` examples alongside newer portable aliases.[^repo-agent-instr] Public Copilot documentation, by contrast, documents portable aliases such as `read`, `edit`, `search`, `execute`, `agent`, and `web`.[^gh-config]

So the practical rule in this repository is:

1. **When editing an existing Browntone agent, keep its tool naming internally consistent.**
2. **When doing a repository-wide clean-up or writing cross-surface guidance, prefer the documented portable aliases.**
3. **Do not standardise one file in isolation.** If you change naming convention, update the instruction template and the affected agent set together.

### Why this matters in this repository

Our existing agent files currently mix multiple naming styles:

- `paper-writer.agent.md` uses `read_file`, `edit_file`, `create_file`, `glob`, `grep`, `powershell`.[^paper-writer]
- `chief-of-staff.agent.md` uses `read_file`, `edit_file`, `create_file`, `powershell`, `grep`, `glob`, `view`, and explicit GitHub MCP function names.[^chief-of-staff]
- `consistency-auditor.agent.md` uses the more portable `read`, `glob`, `grep`, `powershell` pattern.[^consistency-auditor]
- `bibliographer.agent.md`, `research-scout.agent.md`, and the reviewer agents use `web_search`, which behaves like web access in this runtime but is not the portable alias shown in GitHub’s public tool table.[^bibliographer][^research-scout][^reviewer-c][^reviewer-b]
- `lab-manager.agent.md` and `communications.agent.md` use `create`, another runtime-specific spelling not covered by the portable alias table.[^lab-manager][^communications]

That mix can still work in a specific runtime, but it is **less portable** and harder for future authors to copy consistently. For portability, prefer the documented aliases. For local maintenance, prefer consistency within the existing file or do a coordinated standardisation pass.

### Least-privilege heuristics

Grant the minimum tool set that still lets the agent succeed:

- **Reviewer / auditor / planner**: `read`, `search`, maybe `web`
- **Writer**: `read`, `edit`, `search`
- **Implementer**: `read`, `edit`, `search`, `execute`
- **Coordinator**: `agent`, plus whatever it needs to inspect status
- **Research agent**: `read`, `search`, `web`, perhaps `execute` for scripted checks

If the agent should not modify files, do **not** give it edit tools.

If the agent should not run commands, do **not** give it shell access.

If the agent should only be callable by another orchestrator, consider `user-invocable: false`.

## 8. Recommended body structure for Browntone agents

The Browntone house style for agent definitions already uses frontmatter plus body sections for **Identity**, **When to Activate**, **Standard Operating Procedure**, **Output Format**, **Constraints**, and **Quality Gates**.[^repo-agent-instr]

Treat that as the local house style.

### Recommended template

```md
---
name: <kebab-case-name>
description: >
  One paragraph describing the agent's expertise and exactly when to use it.
tools:
  - read
  - search
  - edit
---

# <Agent title>

## Identity
- Who the agent is
- What it knows
- What it optimises for

## When to Activate
- Explicit trigger conditions
- Include phrases like “Use when...”
- Distinguish from nearby agents

## Standard Operating Procedure
1. Gather context
2. Inspect specific files or data sources
3. Perform the task
4. Validate results
5. Produce output in the required format

## Output Format
~~~text
# Report title
## Summary
## Findings
## Risks
## Recommended actions
~~~

## Constraints
- What it must never do
- Directories or file types it must not touch
- Whether it may run commands, edit files, open PRs, etc.

## Quality Gates
- Specific checks before declaring success
- Quantitative thresholds where applicable
```

### Why this structure works

- **Identity** improves voice and decision-making.
- **When to Activate** improves routing.
- **SOP** reduces variance.
- **Output Format** makes downstream orchestration easier.
- **Constraints** reduce harm.
- **Quality Gates** prevent premature “done”.

## 9. Persona design: why identity matters

GitHub’s blog analysis of 2,500+ public `agents.md` files found the best agents were not vague helpers; they were specialists with a clear job, concrete commands, examples, and explicit boundaries.[^gh-blog] Claude Code docs make the same point from a delegation angle: the **description** tells Claude when to delegate, and the focused system prompt shapes specialised behaviour in the subagent’s isolated context.[^claude-subagents]

### Design a persona with these ingredients

1. **Professional identity**  
   Example: “computational mechanics reviewer”, “technical writer”, “operational manager”.

2. **Epistemic style**  
   What does the agent care about? Rigour? clarity? safety? novelty? reproducibility?

3. **Temperament**  
   Constructive, adversarial, sceptical, nurturing, terse, forensic.

4. **Blind spots or non-goals**  
   Good agents know what they do **not** handle.

5. **Deliverable style**  
   Report, patch, checklist, plan, narrative response, table.

### Good persona examples in this repo

- `loving-spouse.agent.md` has a very strong, consistent voice and clear non-goals: it explicitly forbids technical advice and action lists, which keeps the role coherent.[^loving-spouse]
- `reviewer-c.agent.md` sharply defines its viewpoint around reproducibility and number-checking, which helps separate it from reviewers A and B, even though it is not a full six-section template match.[^reviewer-c]
- `bibliographer.agent.md` combines a clear persona with a specific analytical remit and a structured output format, again as a **partial** example rather than a full template-conformance example.[^bibliographer]

### Persona caution

Persona should shape behaviour, not replace procedure. A colourful voice without SOP, constraints, and output structure is still under-specified.

## 10. Effective agent design patterns

### 10.1 Write the description like a routing rule

Bad:

> Helpful engineering assistant.

Good:

> Reviews computational results for code-paper consistency and uncertainty reporting. Use when validating numerical claims, reproducing tables, or checking whether code outputs match manuscript values.

The description is not marketing copy. It is a dispatch rule.

### 10.2 Put commands and checks early

GitHub’s blog explicitly recommends putting executable commands early because agents reference them often.[^gh-blog]

If an agent routinely runs:

- `python -m pytest tests/ -v`
- `pdflatex -interaction=nonstopmode main.tex`
- `gh pr list --state all`

put those commands somewhere obvious.

### 10.3 Prefer examples over abstract prose

One concrete output skeleton usually beats several paragraphs of explanation.[^gh-blog]

### 10.4 Keep agents stateless

Assume the agent starts with only:

- its file definition
- the current task prompt
- the current workspace

Do not rely on “as discussed above” or hidden conversational memory.

### 10.5 Make agents idempotent

Running the same agent twice on the same input should produce roughly the same action pattern and output structure.

### 10.6 Separate coordination from execution

Use one agent to **coordinate** and another to **implement** if needed. VS Code custom agents even support explicit handoffs between agents for this reason.[^vscode-agents]

### 10.7 Add quality gates, not just workflow

SOP tells the agent what to do. Quality gates tell it when it is allowed to stop.

## 11. Anti-patterns

### 11.1 Over-scoped agents

If one file claims to plan, implement, test, review, document, deploy, and manage Git, it will behave inconsistently.

### 11.2 Vague trigger conditions

If the description does not say when to use the agent, inference will be unreliable.

### 11.3 Tool bloat

Giving every agent edit, shell, web, and agent-delegation access is lazy and unsafe.

### 11.4 Missing constraints

Many failures come from not stating what the agent must never touch. GitHub’s blog specifically calls out “never commit secrets” and similar boundaries as highly useful.[^gh-blog]

### 11.5 Missing output format

If you do not specify the output shape, do not complain when the agent returns prose instead of a checklist, table, or structured report.

### 11.6 Hidden environment assumptions

Avoid embedding ephemeral machine- or session-specific paths unless the agent genuinely requires them.

Example from this repository: `chief-of-staff.agent.md` references a session-specific `plan.md` path under `C:\Users\jon\.copilot\session-state\...`, which is powerful in the current environment but fragile as a reusable pattern.[^chief-of-staff]

### 11.7 Copying tool names from one host into another

Do not assume a Cursor rule, a Claude subagent, and a Copilot agent all accept the same tool schema.

## 12. Existing Browntone agents: what works, what is inconsistent, what is missing

This section gives an **illustrative but broad** audit of the current `.github/agents/` directory, highlighting the most reusable patterns and the most important inconsistencies.

### 12.1 Strengths

The repository already does several things well:

- **Strong personas**: `loving-spouse`, `coffee-machine-guru`, `reviewer-b`, and `bibliographer` are memorable and behaviourally distinct.[^loving-spouse][^bibliographer][^reviewer-b]
- **Quantitative orientation**: many agents ask for numerical outputs, severity levels, or structured tables.
- **Workflow awareness**: most agents include a branch / commit / PR workflow.
- **Domain context**: several agents encode canonical parameters, physics caveats, and project-specific priorities.

### 12.2 Inconsistencies

#### Mixed tool naming

The tool lists are not standardised:

- portable style: `read`, `glob`, `grep`, `powershell` in `consistency-auditor.agent.md`[^consistency-auditor]
- runtime-specific style: `read_file`, `edit_file`, `create_file`, `view` in `chief-of-staff.agent.md`[^chief-of-staff]
- mixed editing/runtime style in `paper-writer.agent.md` and `data-analyst.agent.md`[^paper-writer][^data-analyst]

Recommendation: standardise new agents on documented Copilot aliases unless a host-specific reason is explicit.

#### Structure varies widely

Some files closely resemble the intended local template:

- `chief-of-staff.agent.md` includes SOP, constraints, and quality gates.[^chief-of-staff]
- `bibliographer.agent.md` includes persona, mandate, source material, output format, and workflow, although it still lacks explicit “When to Activate”, “Constraints”, and “Quality Gates” headings.[^bibliographer]

Others are much lighter and omit some core sections:

- `paper-writer.agent.md` has style, parameters, and Git workflow, but no explicit **When to Activate**, **Constraints**, or **Quality Gates** sections.[^paper-writer]
- `data-analyst.agent.md` similarly lacks explicit **Output Format**, **Constraints**, and **Quality Gates**.[^data-analyst]
- `research-scout.agent.md` has a good mission but no explicit constraints or quality gates.[^research-scout]
- `consistency-auditor.agent.md` is strong procedurally but lacks explicit constraints / quality gates headings.[^consistency-auditor]
- `reviewer-b.agent.md` has a strong persona and output format but still lacks explicit **When to Activate**, **Constraints**, and **Quality Gates** headings.[^reviewer-b]

#### Some files are less portable than they need to be

- absolute machine-specific paths appear in operational agents[^chief-of-staff]
- some files assume local skills and workflows without distinguishing what is core agent behaviour versus external orchestration

### 12.3 What is missing most often

Across the current set, the most commonly missing ingredients are:

1. **Explicit “When to Activate” headings**
2. **Explicit constraints**
3. **Explicit quality gates**
4. **Portable tool names**
5. **A clear output skeleton in some implementation-facing agents**

### 12.4 One more local gotcha: the house-style “existing agents” list is incomplete

The Browntone house-style guidance includes an “Existing Agents (avoid duplication)” list, but it does **not** enumerate every agent currently present in `.github/agents/`. Treat that list as helpful but incomplete; always inspect the actual directory before concluding a role is free.[^repo-agent-instr]

### 12.5 Other active agents worth noting

To avoid accidental duplication, remember that the directory also includes several active roles not discussed above in detail:

- `simulation-engineer.agent.md`: implementation-facing technical specialist with `read_file` / `edit_file` / `create_file` style tools and a clear SOP, but no explicit constraints or quality gates headings.[^simulation-engineer]
- `communications.agent.md`: outreach-focused writer with a strong output menu and `create` tool usage, but no explicit constraints or quality gates headings.[^communications]
- `lab-meeting.agent.md`: strategic audit / status-report role with a structured output format, but lighter procedural guardrails than `chief-of-staff`.[^lab-meeting]
- `provocateur.agent.md`: strong adversarial persona with explicit output structure and web research, useful as a contrast with reviewer-style agents.[^provocateur]
- `reviewer-a.agent.md`: strong narrative / significance reviewer persona, complementary to reviewers B and C, but still not a full six-section template match.[^reviewer-a]

## 13. Annotated examples

### 13.1 Good partial local example: `bibliographer.agent.md`

Why it works:

- the description clearly signals *when* to invoke it[^bibliographer]
- the body has a distinct persona
- the mandate is broken into numbered responsibilities
- the output format is explicit and structured
- the workflow tells the agent exactly what artefact to produce

What to learn from it:

- pair a strong persona with a structured deliverable
- name source materials explicitly

What it still lacks:

- explicit “When to Activate”
- explicit constraints
- explicit quality gates

### 13.2 Good local example: `chief-of-staff.agent.md`

Why it works:

- very clear role separation: operational management, not research[^chief-of-staff]
- SOP is ordered and concrete
- constraints and quality gates are explicit

Caution:

- this file is powerful but also highly environment-specific
- session-specific paths and extensive operational authority make it a poor template for general-purpose agents unless adapted

### 13.3 Good local example: `loving-spouse.agent.md`

Why it works:

- superb behavioural consistency from persona to output format to constraints[^loving-spouse]
- the file demonstrates that even a “soft” agent needs hard constraints

What to learn from it:

- voice matters
- forbidding the wrong kind of help can improve quality

### 13.4 Incomplete local example: `paper-writer.agent.md`

What is good:

- strong domain context
- explicit canonical parameters
- clear compilation commands[^paper-writer]

What is missing:

- no explicit “use when ...” section
- no explicit constraints
- no explicit quality gates
- no structured output format

How to improve it:

- add activation triggers
- specify expected deliverable shape
- add “never” rules
- add pre-completion checks

### 13.5 Incomplete local example: `data-analyst.agent.md`

What is good:

- concise expertise list
- valuable figure standards
- quantitative expected values[^data-analyst]

What is missing:

- no output template
- no constraints
- no quality gates
- little guidance on how to choose among multiple figure tasks

### 13.6 Public example pattern: GitHub’s docs-agent

GitHub’s blog example works because it combines:

- a sharply defined role
- concrete project knowledge
- executable commands early
- three-tier boundaries: always / ask first / never[^gh-blog]

That is an excellent pattern for any agent that edits files.

### 13.7 Public example pattern: VS Code planning agent

The VS Code docs show a planning agent with restricted search tools and a handoff to implementation.[^vscode-agents] That is a strong example of:

- read-only planning
- explicit workflow staging
- using agent transitions instead of one agent doing everything

## 14. Cross-tool comparison

| Capability | GitHub Copilot CLI / GitHub custom agents | Claude Code subagents | Cursor |
|---|---|---|---|
| File format | `.agent.md` Markdown + YAML | Markdown + YAML in `.claude/agents/` | Rules / modes, not one universal `.agent.md` schema |
| Required fields | `description` effectively required; `name` strongly recommended[^gh-config] | `name` and `description` required[^claude-subagents] | Varies by feature |
| Tool restriction | yes | yes, plus `disallowedTools`[^claude-subagents] | yes, via rules/modes |
| Model selection | yes | yes | yes |
| Separate context | yes; CLI custom agents run via subagents[^gh-cli] | yes; core design feature[^claude-subagents] | agent/mode dependent |
| Handoffs / subagents | supported in VS Code with `agents` and `handoffs`[^vscode-agents] | subagents supported; nested spawning constrained[^claude-subagents] | workflow/mode based |
| Skills / reusable workflows | yes (`.github/skills/`) | yes (`skills` field)[^claude-subagents] | closest analogue is rules/prompts/tooling, not a direct skill standard |

### Portability takeaway

The common cross-tool pattern is:

- Markdown file
- YAML frontmatter
- description-based routing
- persona in the body
- restricted tools
- focused scope

The platform-specific details are:

- exact frontmatter fields
- tool names
- handoff support
- permission models
- hooks and MCP configuration

Write the body portably. Write the frontmatter for the actual host.

## 15. Recommended checklist for new Browntone agents

Before considering a new agent definition complete, verify:

### Role and routing

- [ ] Is the file named `.github/agents/<kebab-case>.agent.md`?
- [ ] Does `description` say both **what the agent does** and **when to use it**?
- [ ] Is the role distinct from existing agents?

### Tool policy

- [ ] Are tools limited to the minimum necessary?
- [ ] Are tool names portable for the intended host?
- [ ] If subagent invocation is needed, is the `agent` tool declared?

### Body quality

- [ ] Is there an explicit **Identity** section?
- [ ] Is there an explicit **When to Activate** section?
- [ ] Is there a step-by-step **Standard Operating Procedure**?
- [ ] Is there a precise **Output Format**?
- [ ] Are **Constraints** explicit?
- [ ] Are **Quality Gates** explicit?

### Practicality

- [ ] Are commands concrete and current?
- [ ] Are paths real and durable?
- [ ] Does the file avoid hidden assumptions about prior conversation state?
- [ ] Would a newcomer understand how and when to use the agent?

### Safety

- [ ] Does the agent forbid dangerous or out-of-scope actions?
- [ ] Is it clear what it must never edit, delete, publish, or merge?

## 16. Recommended house style for future Browntone agents

For new agent files in this repository:

1. Keep tool naming consistent with the target host and the surrounding repository. For cross-surface portability, prefer documented Copilot aliases (`read`, `edit`, `search`, `execute`, `agent`, `web`). For edits to existing Browntone agents, do not silently switch conventions in one file only.
2. Include all six local body sections:
   - Identity
   - When to Activate
   - Standard Operating Procedure
   - Output Format
   - Constraints
   - Quality Gates
3. Put high-value commands near the top of the body.
4. Include a concrete output skeleton.
5. Prefer durable repository-relative paths over session-specific absolute paths.
6. Keep the role narrow and memorable.
7. If multiple agents need the same workflow, put that workflow in a **skill**, not repeated prose.

## 17. References

[^gh-about]: GitHub Docs, “About custom agents.” https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-custom-agents
[^gh-cli]: GitHub Docs, “Creating and using custom agents for GitHub Copilot CLI.” https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli
[^gh-config]: GitHub Docs, “Custom agents configuration.” https://docs.github.com/en/copilot/reference/custom-agents-configuration
[^gh-skills]: GitHub Docs, “Creating agent skills for GitHub Copilot.” https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills
[^vscode-agents]: VS Code Docs, “Custom agents in VS Code.” https://code.visualstudio.com/docs/copilot/customization/custom-agents
[^claude-subagents]: Claude Code Docs, “Subagents.” https://code.claude.com/docs/en/sub-agents
[^cursor-rules]: Cursor Docs, “Rules.” https://cursor.com/docs/rules
[^gh-blog]: GitHub Blog, “How to write a great agents.md: Lessons from over 2,500 repositories.” https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
[^repo-agent-instr]: Browntone house style for agent definitions now lives in `.github/skills/write-agent/SKILL.md` after the instruction files were converted to skills.
[^chief-of-staff]: `.github/agents/chief-of-staff.agent.md:1-220`
[^paper-writer]: `.github/agents/paper-writer.agent.md:1-83`
[^consistency-auditor]: `.github/agents/consistency-auditor.agent.md:1-88`
[^loving-spouse]: `.github/agents/loving-spouse.agent.md:1-103`
[^research-scout]: `.github/agents/research-scout.agent.md:1-80`
[^bibliographer]: `.github/agents/bibliographer.agent.md:1-129`
[^reviewer-c]: `.github/agents/reviewer-c.agent.md:1-95`
[^reviewer-b]: `.github/agents/reviewer-b.agent.md`
[^reviewer-a]: `.github/agents/reviewer-a.agent.md`
[^data-analyst]: `.github/agents/data-analyst.agent.md:1-61`
[^lab-manager]: `.github/agents/lab-manager.agent.md`
[^communications]: `.github/agents/communications.agent.md`
[^simulation-engineer]: `.github/agents/simulation-engineer.agent.md`
[^lab-meeting]: `.github/agents/lab-meeting.agent.md`
[^provocateur]: `.github/agents/provocateur.agent.md`


\
        ## Browntone-Specific Conventions

The following repository-specific guidance is merged from the former
`.github/instructions/agents.instructions.md` file so agent authors still have
access to the local house rules in one place.

        ### Required Structure

        Every Browntone agent `.agent.md` file should include:

        1. YAML frontmatter with at least:
           ```yaml
           ---
           name: agent-name
           description: >
             One paragraph describing the agent's expertise and when to use it.
             Be specific about trigger conditions.
           tools:
             - read
             - edit
             - search
             - execute
           ---
           ```
        2. Body sections for:
           - **Identity**
           - **When to Activate**
           - **Standard Operating Procedure**
           - **Output Format**
           - **Constraints**
           - **Quality Gates**

        ### Key Principles

        - **Self-contained**: put reusable logic in the agent file so the orchestrator
          only needs task-specific context.
        - **Idempotent**: running the same agent twice on the same input should produce
          consistent behaviour.
        - **Scoped**: agents work in their assigned worktree only and should not modify
          unrelated files.
        - **Quantitative**: outputs must include specific numbers, not vague assessments.

        ### Browntone Git Workflow

        Every agent that produces file changes should encode the current lab workflow:

        ```text
        1. Work in an assigned worktree: C:\Users\jon\OneDrive\Projects\browntone-worktrees\<branch>
        2. Commit: git add -A && git commit -m "[category] Description\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
        3. Push: git push origin <branch>
        4. Create a PR: gh pr create --base main --head <branch> ...
        5. Merge its own PR: gh pr merge <N> --merge
        6. Delete the remote branch after merge: git push origin --delete <branch>
        ```

        If you mention merge-conflict handling, instruct the agent to rebase onto
        `origin/main`, resolve conflicts promptly, force-push with lease, then merge.

        ### Existing Agents (avoid duplication)

        Before inventing a new role, check the current Browntone roster:

        - `reviewer-a`: Domain expert (novelty, significance, narrative)
        - `reviewer-b`: Cynical gatekeeper (fatal flaws, consistency)
        - `reviewer-c`: Methodologist (runs code, checks numbers)
        - `consistency-auditor`: Parameter and number consistency checker
        - `lab-meeting`: Holistic audit plus documentation freshness
        - `research-scout`: New research topic discovery
        - `provocateur`: Devil's advocate
        - `communications`: Outreach and public-facing summaries
        - `bibliographer`: Literature tracking and citation radar
        - `lab-manager`: Infrastructure maintenance
