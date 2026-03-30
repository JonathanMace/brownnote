#!/usr/bin/env python3
"""Streaming analyser for Copilot CLI session event logs (events.jsonl).

Designed for large files (100+ MB). All functions use lazy iteration
and never load the full file into memory.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator, Optional

# Default session log path
DEFAULT_PATH = (
    Path.home()
    / ".copilot"
    / "session-state"
    / "4ecd4bf8-106a-471b-af85-d3134005fe36"
    / "events.jsonl"
)

# Event types considered "key" for timeline extraction
TIMELINE_TYPES = {
    "user.message",
    "subagent.started",
    "subagent.completed",
    "skill.invoked",
    "session.compaction_start",
    "session.compaction_complete",
    "session.shutdown",
    "session.resume",
    "session.task_complete",
    "session.start",
    "session.error",
    "abort",
}


def _truncate(text: str, max_len: int = 200) -> str:
    """Truncate *text* to *max_len* chars, appending '…' if trimmed."""
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\r", "")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def _parse_ts(ts: str) -> Optional[datetime]:
    """Parse an ISO 8601 timestamp string to a datetime."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _fmt_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    if seconds < 3600:
        return f"{seconds / 60:.1f}m"
    return f"{seconds / 3600:.1f}h"


# ---------------------------------------------------------------------------
# 1. Lazy Event Iterator
# ---------------------------------------------------------------------------

def iter_events(
    path: str | Path,
    type_filter: Optional[str | set[str]] = None,
) -> Generator[dict[str, Any], None, None]:
    """Yield events one at a time from *path*, optionally filtering by type.

    Parameters
    ----------
    path : str or Path
        Path to the events.jsonl file.
    type_filter : str, set of str, or None
        If given, only yield events whose ``type`` field is in the filter.
    """
    if isinstance(type_filter, str):
        type_filter = {type_filter}
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                print(f"[WARN] Malformed JSON on line {lineno}, skipping", file=sys.stderr)
                continue
            if type_filter is None or evt.get("type") in type_filter:
                yield evt


# ---------------------------------------------------------------------------
# 2. Timeline Extractor
# ---------------------------------------------------------------------------

def _timeline_summary(evt: dict) -> str:
    """Produce a short summary string for a timeline event."""
    etype = evt["type"]
    data = evt.get("data", {})

    if etype == "user.message":
        content = data.get("content", "")
        return _truncate(content, 120)

    if etype == "subagent.started":
        name = data.get("agentName", "?")
        return f"Launched {name}"

    if etype == "subagent.completed":
        name = data.get("agentName", "?")
        model = data.get("model", "")
        dur = data.get("durationMs")
        dur_str = _fmt_duration(dur / 1000) if dur else "?"
        tools = data.get("totalToolCalls", "?")
        return f"Completed {name} ({model}, {dur_str}, {tools} tools)"

    if etype == "skill.invoked":
        return f"Skill: {data.get('name', '?')}"

    if etype == "session.compaction_start":
        tokens = data.get("conversationTokens", "?")
        return f"Compaction start ({tokens} tokens)"

    if etype == "session.compaction_complete":
        pre = data.get("preCompactionTokens", "?")
        return f"Compaction complete (was {pre} tokens)"

    if etype == "session.shutdown":
        st = data.get("shutdownType", "?")
        reqs = data.get("totalPremiumRequests", "?")
        return f"Shutdown ({st}, {reqs} requests)"

    if etype == "session.resume":
        branch = data.get("context", {}).get("branch", "?")
        return f"Resume on {branch}"

    if etype == "session.start":
        ver = data.get("copilotVersion", "?")
        return f"Session start (v{ver})"

    if etype == "session.task_complete":
        return _truncate(data.get("summary", ""), 120)

    if etype == "session.error":
        return _truncate(data.get("message", ""), 120)

    if etype == "abort":
        return data.get("reason", "")

    return ""


def extract_timeline(
    path: str | Path,
) -> list[tuple[str, str, str]]:
    """Return a list of ``(timestamp, event_type, summary)`` for key events."""
    timeline: list[tuple[str, str, str]] = []
    for evt in iter_events(path, type_filter=TIMELINE_TYPES):
        ts = evt.get("timestamp", "")
        summary = _timeline_summary(evt)
        timeline.append((ts, evt["type"], summary))
    return timeline


# ---------------------------------------------------------------------------
# 3. User Message Extractor
# ---------------------------------------------------------------------------

def extract_user_messages(
    path: str | Path,
) -> list[tuple[int, str, str]]:
    """Return ``(index, timestamp, content)`` for every user message."""
    messages: list[tuple[int, str, str]] = []
    idx = 0
    for evt in iter_events(path, type_filter="user.message"):
        content = evt.get("data", {}).get("content", "")
        ts = evt.get("timestamp", "")
        messages.append((idx, ts, content))
        idx += 1
    return messages


# ---------------------------------------------------------------------------
# 4. Subagent Tracker
# ---------------------------------------------------------------------------

def extract_subagents(path: str | Path) -> list[dict[str, Any]]:
    """Return a list of dicts describing each subagent lifecycle.

    Fields: name, agent_type, model, prompt (truncated), start_time,
    end_time, duration, result_summary.
    """
    # Build lookup: toolCallId -> task tool arguments (for prompt/model)
    task_args: dict[str, dict] = {}
    # Collect start/complete events keyed by toolCallId
    starts: dict[str, dict] = {}
    completions: dict[str, dict] = {}

    for evt in iter_events(path):
        etype = evt["type"]
        data = evt.get("data", {})

        if etype == "tool.execution_start" and data.get("toolName") == "task":
            task_args[data["toolCallId"]] = data.get("arguments", {})

        elif etype == "subagent.started":
            tcid = data.get("toolCallId", "")
            starts[tcid] = {
                "agent_name": data.get("agentName", ""),
                "agent_display": data.get("agentDisplayName", ""),
                "timestamp": evt.get("timestamp", ""),
            }

        elif etype == "subagent.completed":
            tcid = data.get("toolCallId", "")
            completions[tcid] = {
                "agent_name": data.get("agentName", ""),
                "model": data.get("model", ""),
                "total_tool_calls": data.get("totalToolCalls"),
                "total_tokens": data.get("totalTokens"),
                "duration_ms": data.get("durationMs"),
                "timestamp": evt.get("timestamp", ""),
            }

    # Merge
    all_ids = sorted(
        starts.keys() | completions.keys(),
        key=lambda k: starts.get(k, {}).get("timestamp", ""),
    )

    results: list[dict[str, Any]] = []
    for tcid in all_ids:
        s = starts.get(tcid, {})
        c = completions.get(tcid, {})
        args = task_args.get(tcid, {})

        start_time = s.get("timestamp", "")
        end_time = c.get("timestamp", "")
        dur_ms = c.get("duration_ms")
        duration = _fmt_duration(dur_ms / 1000) if dur_ms else "?"

        results.append({
            "name": args.get("name", s.get("agent_name", "?")),
            "agent_type": args.get("agent_type", s.get("agent_name", "?")),
            "model": args.get("model", c.get("model", "")),
            "prompt": _truncate(args.get("prompt", ""), 200),
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "tool_calls": c.get("total_tool_calls", "?"),
            "tokens": c.get("total_tokens", "?"),
            "result_summary": f"{c.get('total_tool_calls', '?')} tools, {c.get('total_tokens', '?')} tokens",
        })

    return results


# ---------------------------------------------------------------------------
# 5. Tool Usage Statistics
# ---------------------------------------------------------------------------

def tool_usage_stats(
    path: str | Path,
) -> dict[str, dict[str, Any]]:
    """Return ``{tool_name: {count, success_rate, avg_duration}}``."""
    # Collect start timestamps keyed by toolCallId
    start_times: dict[str, datetime] = {}
    # Accumulate per-tool stats
    counts: dict[str, int] = defaultdict(int)
    successes: dict[str, int] = defaultdict(int)
    durations: dict[str, list[float]] = defaultdict(list)
    tool_names: dict[str, str] = {}  # toolCallId -> toolName

    for evt in iter_events(path, type_filter={"tool.execution_start", "tool.execution_complete"}):
        data = evt.get("data", {})
        tcid = data.get("toolCallId", "")

        if evt["type"] == "tool.execution_start":
            name = data.get("toolName", "unknown")
            tool_names[tcid] = name
            counts[name] += 1
            ts = _parse_ts(evt.get("timestamp", ""))
            if ts:
                start_times[tcid] = ts

        elif evt["type"] == "tool.execution_complete":
            name = tool_names.get(tcid, data.get("toolName", "unknown"))
            if data.get("success"):
                successes[name] += 1
            end_ts = _parse_ts(evt.get("timestamp", ""))
            start_ts = start_times.get(tcid)
            if start_ts and end_ts:
                dur = (end_ts - start_ts).total_seconds()
                if dur >= 0:
                    durations[name].append(dur)

    stats: dict[str, dict[str, Any]] = {}
    for name in sorted(counts):
        total = counts[name]
        succ = successes.get(name, 0)
        durs = durations.get(name, [])
        stats[name] = {
            "count": total,
            "success_rate": round(succ / total * 100, 1) if total else 0,
            "avg_duration": round(sum(durs) / len(durs), 2) if durs else None,
        }
    return stats


# ---------------------------------------------------------------------------
# 6. Conversation Flow
# ---------------------------------------------------------------------------

def extract_conversation(
    path: str | Path,
    include_tool_results: bool = False,
    max_content: int = 200,
) -> list[tuple[str, str, str]]:
    """Return ``(role, timestamp, content)`` for the conversation flow.

    Roles: ``'user'``, ``'assistant'``, ``'tool'``, ``'system'``.
    """
    want = {"user.message", "assistant.message", "system.notification"}
    if include_tool_results:
        want.add("tool.execution_complete")

    conversation: list[tuple[str, str, str]] = []
    for evt in iter_events(path, type_filter=want):
        ts = evt.get("timestamp", "")
        data = evt.get("data", {})
        etype = evt["type"]

        if etype == "user.message":
            conversation.append(("user", ts, _truncate(data.get("content", ""), max_content)))

        elif etype == "assistant.message":
            content = data.get("content", "")
            # Skip empty assistant messages (pure tool-call turns)
            if content and content.strip():
                conversation.append(("assistant", ts, _truncate(content, max_content)))

        elif etype == "system.notification":
            conversation.append(("system", ts, _truncate(data.get("content", ""), max_content)))

        elif etype == "tool.execution_complete":
            result = data.get("result", {})
            text = result.get("content", "") if isinstance(result, dict) else str(result)
            conversation.append(("tool", ts, _truncate(text, max_content)))

    return conversation


# ---------------------------------------------------------------------------
# 7. PR / Commit Tracker
# ---------------------------------------------------------------------------

_GIT_PATTERNS = {
    "commit": re.compile(r"git\s+commit", re.IGNORECASE),
    "push": re.compile(r"git\s+push", re.IGNORECASE),
    "pr_create": re.compile(r"gh\s+pr\s+create", re.IGNORECASE),
    "pr_merge": re.compile(r"gh\s+pr\s+merge", re.IGNORECASE),
    "branch_create": re.compile(r"git\s+checkout\s+-b\s+([A-Za-z0-9][\w./-]+)", re.IGNORECASE),
    "branch_checkout": re.compile(r"git\s+checkout\s+(?!-b\b)(?!--)([A-Za-z0-9][\w./-]+)", re.IGNORECASE),
}

# Patterns applied to tool execution results
_RESULT_PATTERNS = {
    "pr_url": re.compile(r"https://github\.com/[^\s]+/pull/\d+"),
    "commit_sha": re.compile(r"\b[0-9a-f]{7,40}\b"),
}


def extract_git_activity(path: str | Path) -> dict[str, Any]:
    """Scan tool executions for git/gh commands.

    Returns dict with: commits, prs_created, prs_merged, branches, commands.
    """
    commits: list[dict] = []
    prs_created: list[dict] = []
    prs_merged: list[dict] = []
    branches: set[str] = set()
    git_commands: list[dict] = []

    # Also track via tool.execution_start for powershell commands
    pending_git: dict[str, dict] = {}  # toolCallId -> info

    for evt in iter_events(path, type_filter={"tool.execution_start", "tool.execution_complete"}):
        data = evt.get("data", {})
        tcid = data.get("toolCallId", "")
        ts = evt.get("timestamp", "")

        if evt["type"] == "tool.execution_start":
            tool = data.get("toolName", "")
            args = data.get("arguments", {})

            # Powershell commands containing git/gh
            if tool == "powershell":
                cmd = args.get("command", "")
                if not (re.search(r"\bgit\b", cmd) or re.search(r"\bgh\b", cmd)):
                    continue
                pending_git[tcid] = {"command": cmd, "timestamp": ts}
                git_commands.append({"timestamp": ts, "command": _truncate(cmd, 300)})

                for label, pat in _GIT_PATTERNS.items():
                    m = pat.search(cmd)
                    if not m:
                        continue
                    if label == "commit":
                        commits.append({"timestamp": ts, "command": _truncate(cmd, 300)})
                    elif label == "pr_create":
                        prs_created.append({"timestamp": ts, "command": _truncate(cmd, 300)})
                    elif label == "pr_merge":
                        prs_merged.append({"timestamp": ts, "command": _truncate(cmd, 300)})
                    elif label in ("branch_create", "branch_checkout"):
                        branches.add(m.group(1))

            # gh MCP tools
            elif tool.startswith("github-mcp-server"):
                if "pull_request" in tool or "list_pull" in tool:
                    git_commands.append({"timestamp": ts, "tool": tool, "args": str(args)[:200]})

        elif evt["type"] == "tool.execution_complete":
            if tcid in pending_git:
                result = data.get("result", {})
                text = result.get("content", "") if isinstance(result, dict) else str(result)
                pr_match = _RESULT_PATTERNS["pr_url"].search(text)
                if pr_match:
                    url = pr_match.group(0)
                    cmd_info = pending_git[tcid]
                    # Classify: was it a create or merge?
                    if "pr create" in cmd_info.get("command", "").lower():
                        prs_created.append({"timestamp": ts, "url": url})
                    elif "pr merge" in cmd_info.get("command", "").lower():
                        prs_merged.append({"timestamp": ts, "url": url})
                del pending_git[tcid]

    # Also track branches from session.context_changed
    for evt in iter_events(path, type_filter="session.context_changed"):
        branch = evt.get("data", {}).get("branch", "")
        if branch:
            branches.add(branch)

    return {
        "commits": len(commits),
        "commit_details": commits,
        "prs_created": len(prs_created),
        "pr_create_details": prs_created,
        "prs_merged": len(prs_merged),
        "pr_merge_details": prs_merged,
        "branches": sorted(branches),
        "git_commands_total": len(git_commands),
    }


# ---------------------------------------------------------------------------
# 8. Summary Statistics
# ---------------------------------------------------------------------------

def session_summary(path: str | Path) -> dict[str, Any]:
    """Return a dict of high-level session statistics."""
    counts: dict[str, int] = defaultdict(int)
    models: set[str] = set()
    first_ts: Optional[str] = None
    last_ts: Optional[str] = None
    tool_names: set[str] = set()
    agent_types: set[str] = set()
    skill_names: list[str] = []
    total_tokens: int = 0
    total_premium: int = 0
    lines_added: int = 0
    lines_removed: int = 0

    for evt in iter_events(path):
        etype = evt["type"]
        data = evt.get("data", {})
        ts = evt.get("timestamp", "")
        counts[etype] += 1

        if first_ts is None:
            first_ts = ts
        last_ts = ts

        if etype == "tool.execution_start":
            tool_names.add(data.get("toolName", ""))

        elif etype == "tool.execution_complete":
            model = data.get("model", "")
            if model:
                models.add(model)

        elif etype == "subagent.started":
            agent_types.add(data.get("agentName", ""))

        elif etype == "subagent.completed":
            tok = data.get("totalTokens", 0)
            if tok:
                total_tokens += tok
            model = data.get("model", "")
            if model:
                models.add(model)

        elif etype == "skill.invoked":
            skill_names.append(data.get("name", "?"))

        elif etype == "session.shutdown":
            reqs = data.get("totalPremiumRequests", 0)
            if reqs:
                total_premium += reqs
            changes = data.get("codeChanges", {})
            lines_added += changes.get("linesAdded", 0)
            lines_removed += changes.get("linesRemoved", 0)

    # Compute duration
    start = _parse_ts(first_ts) if first_ts else None
    end = _parse_ts(last_ts) if last_ts else None
    duration = (end - start).total_seconds() if (start and end) else 0

    return {
        "duration": _fmt_duration(duration),
        "duration_seconds": duration,
        "start_time": first_ts or "",
        "end_time": last_ts or "",
        "total_events": sum(counts.values()),
        "user_messages": counts.get("user.message", 0),
        "assistant_turns": counts.get("assistant.turn_start", 0),
        "assistant_messages": counts.get("assistant.message", 0),
        "tool_calls_started": counts.get("tool.execution_start", 0),
        "tool_calls_completed": counts.get("tool.execution_complete", 0),
        "unique_tools": sorted(tool_names),
        "subagents_launched": counts.get("subagent.started", 0),
        "subagents_completed": counts.get("subagent.completed", 0),
        "unique_agent_types": sorted(agent_types),
        "skills_invoked": counts.get("skill.invoked", 0),
        "skill_names": skill_names,
        "compactions": counts.get("session.compaction_start", 0),
        "shutdowns": counts.get("session.shutdown", 0),
        "resumes": counts.get("session.resume", 0),
        "aborts": counts.get("abort", 0),
        "errors": counts.get("session.error", 0),
        "models_used": sorted(models),
        "total_subagent_tokens": total_tokens,
        "total_premium_requests": total_premium,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "event_type_counts": dict(sorted(counts.items(), key=lambda x: -x[1])),
    }


# ---------------------------------------------------------------------------
# CLI Formatting Helpers
# ---------------------------------------------------------------------------

def _print_table(headers: list[str], rows: list[list], max_col: int = 60) -> None:
    """Print a simple ASCII table."""
    # Compute column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            text = str(cell)[:max_col]
            if i < len(widths):
                widths[i] = max(widths[i], len(text))

    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print(fmt.format(*("-" * w for w in widths)))
    for row in rows:
        cells = [str(c)[:max_col] for c in row]
        # Pad if needed
        while len(cells) < len(headers):
            cells.append("")
        print(fmt.format(*cells))


# ---------------------------------------------------------------------------
# 9. CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse a Copilot CLI session event log.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_PATH),
        help="Path to events.jsonl (default: most recent session)",
    )
    parser.add_argument("--summary", action="store_true", help="Print session summary stats")
    parser.add_argument("--timeline", action="store_true", help="Print key event timeline")
    parser.add_argument("--messages", action="store_true", help="Print all user messages")
    parser.add_argument("--subagents", action="store_true", help="Print subagent summary table")
    parser.add_argument("--tools", action="store_true", help="Print tool usage stats")
    parser.add_argument(
        "--conversation",
        nargs="?",
        const=-1,
        type=int,
        metavar="N",
        help="Print conversation flow (optionally around user message N)",
    )
    parser.add_argument("--git", action="store_true", help="Print git activity summary")
    parser.add_argument("--export", metavar="FILE", help="Export full timeline to JSON file")

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    # Default to --summary if nothing specified
    if not any([
        args.summary, args.timeline, args.messages, args.subagents,
        args.tools, args.conversation is not None, args.git, args.export,
    ]):
        args.summary = True

    if args.summary:
        s = session_summary(path)
        print("=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)
        print(f"  Duration:            {s['duration']} ({s['start_time'][:19]} → {s['end_time'][:19]})")
        print(f"  Total events:        {s['total_events']:,}")
        print(f"  User messages:       {s['user_messages']}")
        print(f"  Assistant turns:     {s['assistant_turns']}")
        print(f"  Tool calls:          {s['tool_calls_started']:,} started, {s['tool_calls_completed']:,} completed")
        print(f"  Unique tools:        {len(s['unique_tools'])}")
        print(f"  Subagents:           {s['subagents_launched']} launched, {s['subagents_completed']} completed")
        print(f"  Agent types:         {', '.join(s['unique_agent_types'])}")
        print(f"  Skills invoked:      {s['skills_invoked']} ({', '.join(s['skill_names'])})")
        print(f"  Compactions:         {s['compactions']}")
        print(f"  Shutdowns/Resumes:   {s['shutdowns']} / {s['resumes']}")
        print(f"  Aborts:              {s['aborts']}")
        print(f"  Errors:              {s['errors']}")
        print(f"  Models used:         {', '.join(s['models_used'])}")
        print(f"  Subagent tokens:     {s['total_subagent_tokens']:,}")
        print(f"  Premium requests:    {s['total_premium_requests']}")
        print(f"  Code changes:        +{s['lines_added']:,} / -{s['lines_removed']:,} lines")
        print()
        print("Event type breakdown:")
        for etype, cnt in s["event_type_counts"].items():
            print(f"  {cnt:>6,}  {etype}")

    if args.timeline:
        tl = extract_timeline(path)
        print(f"\nTIMELINE ({len(tl)} key events)")
        print("-" * 80)
        for ts, etype, summary in tl:
            short_ts = ts[:19].replace("T", " ") if ts else "?"
            tag = etype.split(".")[-1]
            print(f"  {short_ts}  [{tag:<20}] {summary}")

    if args.messages:
        msgs = extract_user_messages(path)
        print(f"\nUSER MESSAGES ({len(msgs)} total)")
        print("-" * 80)
        for idx, ts, content in msgs:
            short_ts = ts[:19].replace("T", " ") if ts else "?"
            # Show first line only for display
            first_line = content.split("\n")[0][:120] if content else ""
            print(f"  [{idx:>3}] {short_ts}  {first_line}")

    if args.subagents:
        agents = extract_subagents(path)
        print(f"\nSUBAGENTS ({len(agents)} total)")
        print("-" * 100)
        headers = ["#", "Name", "Type", "Model", "Duration", "Tools", "Tokens"]
        rows = []
        for i, a in enumerate(agents):
            rows.append([
                i,
                a["name"][:25],
                a["agent_type"][:18],
                a["model"][:20] if a["model"] else "",
                a["duration"],
                a["tool_calls"],
                a["tokens"],
            ])
        _print_table(headers, rows)

    if args.tools:
        stats = tool_usage_stats(path)
        print(f"\nTOOL USAGE ({len(stats)} tools)")
        print("-" * 70)
        headers = ["Tool", "Count", "Success %", "Avg Duration"]
        rows = []
        for name, s in sorted(stats.items(), key=lambda x: -x[1]["count"]):
            dur = f"{s['avg_duration']:.2f}s" if s["avg_duration"] is not None else "N/A"
            rows.append([name, s["count"], f"{s['success_rate']}%", dur])
        _print_table(headers, rows)

    if args.conversation is not None:
        n = args.conversation
        conv = extract_conversation(path, include_tool_results=False, max_content=300)
        if n >= 0:
            # Find the Nth user message and show context around it
            user_indices = [i for i, (role, _, _) in enumerate(conv) if role == "user"]
            if n < len(user_indices):
                center = user_indices[n]
                start = max(0, center - 3)
                end = min(len(conv), center + 10)
                conv = conv[start:end]
                print(f"\nCONVERSATION around user message {n}")
            else:
                print(f"User message {n} not found (max {len(user_indices) - 1})")
                return
        else:
            print(f"\nFULL CONVERSATION ({len(conv)} entries)")

        print("-" * 80)
        for role, ts, content in conv:
            short_ts = ts[:19].replace("T", " ") if ts else "?"
            prefix = {"user": "👤", "assistant": "🤖", "tool": "🔧", "system": "📢"}.get(role, "?")
            print(f"  {prefix} [{short_ts}] {content[:200]}")

    if args.git:
        g = extract_git_activity(path)
        print("\nGIT ACTIVITY")
        print("-" * 60)
        print(f"  Total git/gh commands:  {g['git_commands_total']}")
        print(f"  Commits:                {g['commits']}")
        print(f"  PRs created:            {g['prs_created']}")
        print(f"  PRs merged:             {g['prs_merged']}")
        print(f"  Branches seen:          {len(g['branches'])}")
        if g["branches"]:
            for b in g["branches"]:
                print(f"    - {b}")
        if g["pr_create_details"]:
            print("\n  PR Create Details:")
            for pr in g["pr_create_details"][:20]:
                ts = pr.get("timestamp", "")[:19]
                cmd = pr.get("command", pr.get("url", ""))
                print(f"    {ts}  {_truncate(cmd, 120)}")
        if g["pr_merge_details"]:
            print("\n  PR Merge Details:")
            for pr in g["pr_merge_details"][:20]:
                ts = pr.get("timestamp", "")[:19]
                cmd = pr.get("command", pr.get("url", ""))
                print(f"    {ts}  {_truncate(cmd, 120)}")

    if args.export:
        tl = extract_timeline(path)
        export_data = [
            {"timestamp": ts, "event_type": etype, "summary": summary}
            for ts, etype, summary in tl
        ]
        out_path = Path(args.export)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(export_data, fh, indent=2, ensure_ascii=False)
        print(f"\nExported {len(export_data)} timeline events to {out_path}")


if __name__ == "__main__":
    main()
