---
name: write-hooks
description: >-
  Hooks automatically run commands before or after agent actions — logging
  activity, blocking unsafe commands, or triggering side effects.  Use this
  skill to author hooks.json files, add pre/post tool guards, or set up
  .github/hooks.
license: MIT
---

# Authoring Hooks for GitHub Copilot CLI

Hooks let you author event-driven shell commands that run at specific points during a Copilot CLI session lifecycle. They provide programmable guardrails, logging, and automation around prompts, tool use, errors, and session boundaries.

## Procedure: Authoring Hooks

1. **Decide whether a hook is the right mechanism** — for workflow instructions, author a skill instead. For persistent preferences, author custom instructions instead. For a specialized persona or delegated workflow, author a custom agent instead. For new external capabilities, add an MCP server. See the `write-skill`, `write-agent`, and `write-instructions` skills.
2. **Inspect existing hooks** — check `.github/hooks/` for existing hook files to avoid conflicts, understand existing triggers, and match conventions.
3. **Choose the trigger** — identify which lifecycle event should fire the hook (see [Available Hook Triggers](#available-hook-triggers) below).
4. **Author or edit a `*.json` file in `.github/hooks/`** — the filename is up to you, and multiple hook files are supported.
5. **Author the hook entry** — define `type: "command"`, provide `bash` and/or `powershell`, and set `cwd`, `timeoutSec`, and `env` when needed.
6. **Author supporting scripts** (if needed) — for complex logic, reference external scripts rather than long inline commands.
7. **Define the stdin/stdout contract** — confirm what JSON the hook will read on stdin and whether its stdout is ignored or interpreted.
8. **Test the hook in isolation** — pipe representative JSON into your script and verify exit code, stderr logging, and stdout shape before deploying.
9. **Test in a live session** — start a Copilot CLI session and trigger the lifecycle event. Verify the hook fires and behaves as expected.

## When to Author Hooks (vs Other Customization)

- **Author hooks** for programmable guardrails, logging, automation, or policy enforcement around tool use and session events.
- **Author skills** for workflow instructions and task-specific procedures.
- **Author custom instructions** for persistent preferences and coding standards.
- **Add MCP servers** for new external capabilities and tool integrations.

## File Location and Scope

```
.github/hooks/
├── hooks.json          # Any filename ending in .json works
└── security-hooks.json # Multiple hook files are supported
```

Copilot CLI loads hook files from `.github/hooks/*.json` in the repository rooted at the current working directory. Hook files must be on the repository's **default branch** for Copilot coding agent to use them.

## Configuration Format

Hooks are defined in JSON with `version: 1` and a `hooks` object whose keys are lifecycle trigger names. Include only the triggers you need; each trigger maps to an array of hook entries, and multiple entries run in order.

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [],
    "sessionEnd": [],
    "userPromptSubmitted": [],
    "preToolUse": [],
    "postToolUse": [],
    "errorOccurred": [],
    "agentStop": [],
    "subagentStop": []
  }
}
```

## Available Hook Triggers

| Hook | Fires When | Notes |
|------|-----------|-------|
| `sessionStart` | A CLI session begins or resumes | Useful for initialization and audit logging |
| `sessionEnd` | A CLI session ends | Useful for cleanup and final reporting |
| `userPromptSubmitted` | A user submits a prompt | Good for prompt logging or policy checks |
| `preToolUse` | Before a tool is executed | The only hook type that can deny tool execution |
| `postToolUse` | After a tool finishes executing | Useful for audit logs, metrics, and failure alerts |
| `errorOccurred` | An error occurs during execution | Useful for error logging and notifications |
| `agentStop` | The main agent finishes responding | Useful for end-of-response automation |
| `subagentStop` | A subagent completes before returning to its parent | Useful for delegated-task logging |

## Hook Command Syntax

Each hook entry is a JSON object. Use `type: "command"` and author `bash`, `powershell`, or both:

```json
{
  "type": "command",
  "bash": "echo \"Session started: $(date)\" >> logs/session.log",
  "powershell": "Add-Content -Path logs/session.log -Value \"Session started: $(Get-Date)\"",
  "cwd": ".",
  "timeoutSec": 10,
  "env": {
    "LOG_LEVEL": "INFO"
  }
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | Must be `"command"` |
| `bash` | string | Yes on Unix-like systems* | Command to run on Unix-like systems |
| `powershell` | string | Yes on Windows* | Command to run on Windows |
| `cwd` | string | No | Working directory, relative to the repository root |
| `timeoutSec` | number | No | Timeout in seconds (default: 30) |
| `env` | object | No | Additional environment variables merged into the existing environment |

*At least one of `bash` or `powershell` must be provided. For portable hooks, author both.

## Hook Input and Output

### Input JSON

Hook scripts receive **compact JSON on stdin**. The payload depends on the trigger:

| Trigger | Important input fields |
|---------|------------------------|
| `sessionStart` | `timestamp`, `cwd`, `source`, `initialPrompt` |
| `sessionEnd` | `timestamp`, `cwd`, `reason` |
| `userPromptSubmitted` | `timestamp`, `cwd`, `prompt` |
| `preToolUse` | `timestamp`, `cwd`, `toolName`, `toolArgs` |
| `postToolUse` | `timestamp`, `cwd`, `toolName`, `toolArgs`, `toolResult.resultType`, `toolResult.textResultForLlm` |
| `errorOccurred` | `timestamp`, `cwd`, `error` |
| `agentStop` | Session-completion context for the main agent |
| `subagentStop` | Completion context for the subagent |

Notes:

- `toolArgs` is itself a JSON string, so many hooks need to parse JSON twice.
- Input arrives on stdin; do not expect positional command-line arguments.
- For trigger-specific payload details, consult the official **Hooks configuration** reference before authoring a non-trivial script.

### Output JSON

Hook scripts can emit **compact JSON on stdout**, but not every hook type consumes it:

- **`preToolUse`** can return a decision object such as `{"permissionDecision":"deny","permissionDecisionReason":"Destructive command blocked"}`.
- `permissionDecision` may be `allow`, `deny`, or `ask`, but only **`deny` is currently processed**.
- Other hook types may write JSON to stdout, but current CLI behavior ignores that output.
- Send diagnostics to **stderr**, not stdout, because stdout is reserved for hook responses.

### Minimal script patterns

**Bash**

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.toolName // empty')
TOOL_ARGS=$(echo "$INPUT" | jq -r '.toolArgs // "{}"')
```

**PowerShell**

```powershell
$ErrorActionPreference = "Stop"
$inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
$toolName = $inputJson.toolName
$toolArgs = if ($inputJson.toolArgs) { $inputJson.toolArgs | ConvertFrom-Json } else { $null }
```

## Examples

### Session Logging

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "bash": "echo \"Session started: $(date)\" >> logs/session.log",
        "powershell": "Add-Content -Path logs/session.log -Value \"Session started: $(Get-Date)\"",
        "cwd": ".",
        "timeoutSec": 10
      }
    ],
    "sessionEnd": [
      {
        "type": "command",
        "bash": "echo \"Session ended: $(date)\" >> logs/session.log",
        "powershell": "Add-Content -Path logs/session.log -Value \"Session ended: $(Get-Date)\"",
        "cwd": ".",
        "timeoutSec": 10
      }
    ]
  }
}
```

### Prompt Logging with External Script

```json
{
  "version": 1,
  "hooks": {
    "userPromptSubmitted": [
      {
        "type": "command",
        "bash": "./scripts/log-prompt.sh",
        "powershell": ".\\scripts\\log-prompt.ps1",
        "cwd": ".",
        "env": {
          "LOG_LEVEL": "INFO"
        }
      }
    ]
  }
}
```

### Pre-Tool Guard (Block Dangerous Commands)

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "./scripts/validate-tool.sh",
        "powershell": ".\\scripts\\validate-tool.ps1",
        "cwd": ".",
        "timeoutSec": 5
      }
    ]
  }
}
```

For `preToolUse`, the script can deny execution by returning compact JSON such as:

```json
{"permissionDecision":"deny","permissionDecisionReason":"Dangerous command detected"}
```

### Post-Tool Audit Logging

```json
{
  "version": 1,
  "hooks": {
    "postToolUse": [
      {
        "type": "command",
        "bash": "./scripts/log-tool-result.sh",
        "powershell": ".\\scripts\\log-tool-result.ps1",
        "cwd": ".",
        "timeoutSec": 5
      }
    ]
  }
}
```

## Debugging Hooks

### Enable debug mode in scripts

```bash
#!/bin/bash
set -x  # Enable bash debug mode
INPUT=$(cat)
echo "DEBUG: Received input" >&2
echo "$INPUT" >&2
# ... rest of script
```

```powershell
$ErrorActionPreference = "Stop"
$rawInput = [Console]::In.ReadToEnd()
Write-Error "DEBUG: Received input"
Write-Error $rawInput
```

### Test hooks locally

```bash
# Pipe test input into your hook script
echo '{"timestamp":1704614400000,"cwd":"/path/to/project","toolName":"bash","toolArgs":"{\"command\":\"ls\"}"}' | ./my-hook.sh

# Check exit code
echo $?

# Validate output is valid JSON
./my-hook.sh < test-input.json | jq -c .
```

```powershell
# Pipe test input into your hook script
'{"timestamp":1704614400000,"cwd":"C:\\repo","toolName":"view","toolArgs":"{\"path\":\"README.md\"}"}' | .\my-hook.ps1

# Validate output is compact JSON
Get-Content test-input.json -Raw | .\my-hook.ps1 | ConvertFrom-Json | ConvertTo-Json -Compress
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hooks not executing | Verify the file is in `.github/hooks/`, check JSON syntax, ensure `version: 1` is set, and confirm the file is on the default branch if you need coding-agent support |
| Hooks timing out | Increase `timeoutSec`, optimize script performance |
| Invalid JSON output | Ensure output is on a single line; use `jq -c` (Unix) or `ConvertTo-Json -Compress` (Windows) |
| Script not found | Check `cwd`, use a path that matches that working directory, and ensure the script is executable on Unix-like systems |
| Hook logs break behavior | Send logs to stderr; keep stdout reserved for compact JSON responses |

## Done Criteria

- Hook file is valid JSON with `version: 1` and at least one `hooks` entry
- Trigger correctly maps to the intended agent event
- Both `bash` and `powershell` commands provided (or justified single-platform)
- Script handles missing dependencies gracefully
- Hook tested in isolation (`copilot hooks test` if available) and in a live session
- No conflicts with existing hooks on the same trigger

## Best Practices for Authoring Hooks

1. **Keep hooks fast** — hooks run synchronously and block the agent. Use reasonable timeouts.
2. **Provide both `bash` and `powershell`** — ensures cross-platform compatibility.
3. **Treat stdin as the API contract** — author scripts against the documented JSON payload for that trigger.
4. **Use compact JSON on stdout** — especially for `preToolUse`; log diagnostics to stderr.
5. **Use scripts for complex logic** — inline commands get unwieldy; reference external scripts.
6. **Test hooks in isolation** — pipe sample JSON into your scripts before deploying.
7. **Set appropriate timeouts** — the default 30 seconds is generous; most hooks should complete in under 5 seconds.
8. **Don't block unnecessarily** — hooks that deny tool use should have clear, documented reasons.
9. **Validate and sanitize inputs** — hook payloads may contain untrusted prompt text, tool arguments, and error messages.
