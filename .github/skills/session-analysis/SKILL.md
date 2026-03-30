---
name: session-analysis
description: >-
  Understand what happened in a Copilot CLI session — review agent behavior,
  audit tool usage, trace subagent lifecycles, analyze token consumption, and
  inspect git activity.  Use when asked to analyze a session, review past work,
  debug agent performance, or extract insights from session logs.
license: MIT
---

# Analyzing Copilot CLI Sessions

Copilot CLI records every event in a session to `~/.copilot/session-state/<session-id>/events.jsonl`. This skill uses a streaming analyzer script to perform retrospective meta-analysis of those logs — understanding what an agent did, how efficiently it worked, and what it produced.

## When to Use This Skill

- **Retrospective review** — summarize what happened in a session after it completed
- **Debugging agent behavior** — understand why an agent took certain actions, where it stalled, or what errors occurred
- **Token and cost analysis** — track premium requests, subagent token consumption, and compaction events
- **Audit git activity** — review commits, PRs, and branch operations performed during a session
- **Subagent inspection** — see which subagents were launched, their models, durations, and tool call counts
- **Tool usage profiling** — identify which tools were called most, their success rates, and average durations
- **Conversation replay** — reconstruct the user/assistant/tool conversation flow

## Prerequisites

- Python 3.9+ (uses only stdlib — no dependencies)
- Access to the session's `events.jsonl` file

## Procedure: Analyzing a Session

1. **Locate the session log.** Session logs live at `~/.copilot/session-state/<session-id>/events.jsonl`. To find available sessions:
   ```
   ls ~/.copilot/session-state/
   ```
   Each directory name is a session ID (UUID). Pick the one to analyze. If the user provides a session ID, use it directly.

2. **Start with the summary** to get an overview of the session scope and scale:
   ```
   python scripts/session_analyzer.py <path-to-events.jsonl> --summary
   ```

3. **Drill into specific areas** based on what the summary reveals or what the user asks about — use the subcommands documented below.

4. **Interpret the results** using the guidance in [Interpretation: What to Look For](#interpretation-what-to-look-for).

5. **Report findings** — summarize the key insights concisely. Lead with the most important or surprising findings.

## The Analyzer Script

The script is at `scripts/session_analyzer.py` (relative to this skill directory). It streams events lazily and never loads the full file into memory, so it handles 100+ MB logs efficiently.

### Subcommands

All subcommands take the path to `events.jsonl` as the first positional argument. If no flags are specified, `--summary` is the default.

#### `--summary` — Session Overview

Prints high-level statistics: duration, event counts, user messages, tool calls, subagents, skills, compactions, models, token totals, premium requests, and code changes (lines added/removed).

```
python scripts/session_analyzer.py ~/...events.jsonl --summary
```

Use this first to understand the shape of a session before drilling deeper.

#### `--timeline` — Key Event Timeline

Prints key events in chronological order: user messages, subagent start/complete, skill invocations, compactions, shutdowns, resumes, errors, and aborts. Each entry shows timestamp, event type tag, and a short summary.

```
python scripts/session_analyzer.py ~/...events.jsonl --timeline
```

Use this to understand the narrative arc of a session — what happened and in what order.

#### `--messages` — User Messages

Lists every user message with its index number and timestamp. Shows the first line of each message.

```
python scripts/session_analyzer.py ~/...events.jsonl --messages
```

Use this to see what the user asked for. Message indices can be passed to `--conversation N` to focus on a specific exchange.

#### `--subagents` — Subagent Details

Prints a table of all subagents: name, type, model, duration, tool call count, and token count.

```
python scripts/session_analyzer.py ~/...events.jsonl --subagents
```

Use this to audit subagent efficiency — which ones ran long, used many tokens, or had unusual tool call counts.

#### `--tools` — Tool Usage Statistics

Prints per-tool statistics: invocation count, success rate (%), and average duration.

```
python scripts/session_analyzer.py ~/...events.jsonl --tools
```

Use this to identify tool failures (low success rate), hot tools (high count), or slow tools (high avg duration).

#### `--conversation [N]` — Conversation Flow

Without `N`, prints the full user/assistant/system conversation flow with emoji role markers (👤 user, 🤖 assistant, 📢 system). With `N`, focuses on a window around user message `N` (3 messages before, 10 after).

```
# Full conversation
python scripts/session_analyzer.py ~/...events.jsonl --conversation

# Focused around user message 5
python scripts/session_analyzer.py ~/...events.jsonl --conversation 5
```

Use this to replay specific exchanges or understand context around a particular user request.

#### `--git` — Git Activity

Summarizes git/gh commands: commit count, PRs created/merged, branches seen, and detailed command logs.

```
python scripts/session_analyzer.py ~/...events.jsonl --git
```

Use this to audit what code changes were committed, which PRs were opened or merged, and what branches were involved.

#### `--export FILE` — JSON Export

Exports the timeline to a JSON file for external analysis or further processing.

```
python scripts/session_analyzer.py ~/...events.jsonl --export timeline.json
```

### Combining Subcommands

Multiple flags can be combined in a single invocation:

```
python scripts/session_analyzer.py ~/...events.jsonl --summary --timeline --subagents
```

## Understanding events.jsonl

Each line is a JSON object with at minimum `type` and `timestamp` fields. Common event types:

| Event Type | Description |
|---|---|
| `user.message` | User prompt (content in `data.content`) |
| `assistant.message` | Assistant text response |
| `assistant.turn_start` | Start of an assistant reasoning turn |
| `tool.execution_start` | Tool invocation (tool name, arguments in `data`) |
| `tool.execution_complete` | Tool result (success flag, result content) |
| `subagent.started` | Subagent launched (agent name, toolCallId) |
| `subagent.completed` | Subagent finished (model, duration, tokens, tool calls) |
| `skill.invoked` | Skill activated (name in `data.name`) |
| `session.compaction_start` | Context compaction triggered (token count) |
| `session.compaction_complete` | Compaction finished (pre/post token counts) |
| `session.shutdown` | Session ended (shutdown type, premium requests, code changes) |
| `session.resume` | Session resumed (branch context) |
| `session.error` | Error occurred (message) |
| `abort` | User abort (reason) |

Events are linked by `toolCallId` — a tool start and its completion share the same ID, as do subagent starts and their parent task tool invocation.

## Interpretation: What to Look For

### Session Health
- **High compaction count** — the session hit context limits repeatedly; consider breaking work into smaller sessions or using more subagents to offload context
- **Errors or aborts** — check the timeline for `session.error` and `abort` events to understand failure modes
- **Shutdown type** — `session.shutdown` data includes `shutdownType` (normal, timeout, error)

### Efficiency
- **Tool success rate below 90%** — investigate which tools are failing and why (bad arguments? network issues? permissions?)
- **Subagents with high token counts but few tool calls** — may indicate verbose prompts or unnecessary context being passed
- **Long subagent durations** — compare similar subagents to spot outliers; long durations may indicate retry loops or blocked I/O
- **Premium request count** — track cost; compare across sessions to establish baselines

### Patterns
- **Repeated tool calls** — many calls to the same tool in sequence may indicate retry loops or inefficient search patterns
- **Conversation flow gaps** — long gaps between user messages may indicate the agent was stuck or doing extensive autonomous work
- **Subagent model usage** — verify that expensive models (opus) are only used where needed and cheaper models (haiku) are used for routine tasks
- **Git activity without user prompts** — autonomous commits or PR operations should be reviewed for correctness

### Code Impact
- **Lines added vs removed** — large net additions may warrant review; high churn (both high adds and removes) may indicate iteration
- **Commit frequency** — many small commits suggests incremental work; few large commits may indicate batch operations
- **Branch count** — multiple branches may indicate parallel workstreams or exploratory approaches

## Done Criteria

- Session log located and readable
- Summary produced covering key metrics (duration, turns, tool calls, token usage)
- Specific user questions answered with evidence from the log
- Key anomalies or patterns identified and explained
- Recommendations provided if analysis reveals inefficiencies

## Cross-References

- `writing-skills` — skill invocation events (`skill.invoked`) in session logs correspond to skills authored with that guidance
- `writing-hooks` — hook execution events map to hooks authored with that skill
- `writing-custom-agents` — subagent lifecycle events (`subagent.started`, `subagent.completed`) correspond to agents and embedded subagent instructions authored with that skill
