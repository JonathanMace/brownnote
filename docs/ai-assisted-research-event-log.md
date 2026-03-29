# AI-Assisted Research from the Session Event Log

*Definitive retrospective based on `events.jsonl`, not memory.*

This document differs from `docs/ai-assisted-research.md` and
`docs/ai-assisted-research-detailed.md` in one important way: its primary source
is the actual Copilot CLI session event log at
`C:\Users\jon\.copilot\session-state\4ecd4bf8-106a-471b-af85-d3134005fe36\events.jsonl`.
To avoid contaminating the retrospective with the act of writing this file, the
analysis below is frozen at the original session cutoff
`2026-03-29T08:00:02Z`. All timestamps below are UTC as recorded in the log.

### Source and method

The reconstruction used `scripts\session_analyzer.py` in six passes:

- `--summary`
- `--messages`
- `--subagents`
- `--tools`
- `--git`
- `--timeline`

For a few milestone timestamps that are not emitted in the reduced timeline
view, I also inspected the corresponding `assistant.message` events directly in
the raw log. The event log is JSON Lines, so each event is individually
timestamped and typed (`user.message`, `tool.execution_start`,
`subagent.completed`, `session.resume`, and so on). That makes it possible to
freeze the session at a chosen cutoff and reconstruct both the broad statistics
and the minute-by-minute narrative.

---

## 1. Session Statistics

At the frozen cutoff, the session was already absurdly large:

| Metric | Value |
|---|---:|
| Wall-clock duration | 52.1 h |
| Session window | 2026-03-27 03:54:39 → 2026-03-29 08:00:02 |
| Total events | 35,712 |
| User messages | 123 |
| Assistant turns | 1,679 |
| Assistant messages | 6,911 |
| Tool calls | 12,211 started / 12,124 completed |
| Unique tools | 32 |
| Subagents | 246 launched / 240 completed |
| Subagent completion rate | 97.6% |
| Skills invoked | 16 |
| Compactions | 12 |
| Shutdowns / resumes | 3 / 4 |
| Aborts | 20 |
| Errors | 1 |
| Premium requests | 270 |
| Subagent tokens | 316,442,931 |
| Recorded code churn | +29,572 / -5,183 lines |

Where these numbers differ slightly from earlier rough retrospectives, this
document follows the frozen raw log rather than remembered or git-derived
totals.

### Models used

The session used four models overall:

- `claude-haiku-4.5`
- `claude-opus-4.6`
- `claude-sonnet-4.6`
- `gpt-5.4`

For subagent launches where a model could be recovered from task arguments or
completion metadata, the breakdown was:

| Model | Launches |
|---|---:|
| `claude-opus-4.6` | 125 |
| `gpt-5.4` | 64 |
| `claude-haiku-4.5` | 14 |
| `claude-sonnet-4.6` | 4 |
| Not captured in lifecycle metadata | 39 |

### Skills invoked

Sixteen skill invocations were recorded:

`semester-break`, `write-paper`, `git-checkpoint`, `write-skills`,
`maintain-repository-docs`, `research-iteration`, `generate-figures`,
`compile-paper`, `write-paper`, `git-checkpoint`, `compile-paper`,
`write-paper`, `write-paper`, `compile-paper`, `write-research-log`,
`git-checkpoint`.

The log shows a session that did not merely produce outputs; it repeatedly
stopped, compacted, resumed, reviewed itself, and formalised its own habits.

---

## 2. The Human's Voice — All 123 Prompts Analysed

The user did not behave like a passive customer. He behaved like a PI: setting
direction, shaping tone, criticising process, occasionally offering morale, and
intervening sharply when the lab drifted.

### Category breakdown for all 123 messages

Every user message can be assigned to one primary category:

| Category | Count | Message IDs |
|---|---:|---|
| Direction-setting | 33 | 0-3, 5, 7-9, 24-25, 53-54, 61, 63, 68, 71, 79, 84, 86-87, 90, 96-97, 100-101, 103, 107, 109, 116-117, 119-121 |
| Taste / judgment | 14 | 10-11, 13, 19, 26, 28-29, 73, 94-95, 98, 102, 104, 108 |
| Process feedback | 31 | 4, 6, 14, 17, 21-22, 27, 32-33, 35, 37-40, 46-50, 52, 55-59, 64-65, 99, 105-106, 118 |
| Encouragement | 3 | 23, 31, 44 |
| Course correction | 18 | 66-67, 72, 75-78, 80-83, 85, 88, 110, 112-114, 122 |
| Administrative | 24 | 12, 15-16, 18, 20, 30, 34, 36, 41-43, 45, 51, 60, 62, 69-70, 74, 89, 91-93, 111, 115 |

That distribution matters. Only **3** of 123 messages are straightforward
encouragement. The dominant modes are managerial: direction, process, and
administration.

### Representative quotes

Some prompts became constitutional moments for the lab:

- **2026-03-27 04:00:30** — “**Let us be the first to find scientific evidence
  to suport the brown note.**”
- **2026-03-27 04:02:02** — “**you're a research expert, I'm just a layman with
  a PhD**.”
- **2026-03-27 05:35:51** — “**Only 2 background tasks - we can do better.**”
- **2026-03-27 05:54:37** — “**Each reviewing round, create 3 reviewer agents
  rather than just 1.**”
- **2026-03-27 05:56:24** — “**Now THIS is vibe researching**”
- **2026-03-27 06:10:42** — “**I'm going to apply a branch protection rule on
  main**”
- **2026-03-27 06:31:28** — “**you're just hitting a rough patch in the path to
  tenure**”
- **2026-03-27 06:49:57** — “**Add a member of your lab: an agent who
  represents the ‘really smart old researcher who chats to you at the coffee
  machine’**”
- **2026-03-27 06:55:43** — “**Add a ‘loving spouse’ agent**”
- **2026-03-27 12:24:24** — “**External reviewer comment: it should be a
  prolate spheroid**”
- **2026-03-29 05:23:01** — “**The bigoted board at Elsevier refuses to
  recognize your contributions as a full co-author**”
- **2026-03-29 07:52:31** — “**He thinks you could be in for a shot at an
  ignobel prize**”
- **2026-03-29 07:58:23** — “**What happened to your background research about
  event logs?**”

### How the human role changed over time

The event log shows a clear evolution.

#### Phase 1: active scientific director

From message 0 through roughly message 13, the user specified the scientific
problem, venue ambition, modelling idea, and repository shape. This was the
closest the session ever came to a conventional “brief”.

#### Phase 2: operations architect

The heaviest prompt density arrived in the **06:00 UTC hour on 2026-03-27**:
**35 user messages in one hour**. This is where the human stopped steering just
the paper and started designing the institution around it: PR workflow, branch
protection, reviewer panels, research logs, copilot instructions, semester
breaks, lab staffing, and management roles.

#### Phase 3: critic and external reviewer proxy

By midday on 27 March, the tone shifted. The user became a stand-in for expert
reviewers and operational feedback:

- CI failures,
- Git LFS warnings,
- stale branches,
- the oblate/prolate challenge,
- newer literature,
- rigor and derivation requests.

This is less “write this section” and more “the lab is now mature enough to be
audited”.

#### Phase 4: taste interventions

Once Paper 1 and then Paper 2 approached acceptance, the user's messages became
more editorial:

- subtle wit,
- title phrasing,
- README tone,
- author lists,
- acknowledgements,
- paper descriptions.

At this stage the human was not supplying technical content so much as
scientific taste.

#### Phase 5: increasingly hands-off, but decisive

There is a **30 h 26 m** gap between message 97
(`2026-03-27 22:32:11`) and message 98 (`2026-03-29 04:58:23`).
That silence is the strongest evidence that the project had become genuinely
autonomous. When the user returned, he did not restart the research from
scratch; he nudged its governance:

- hard model-selection rules,
- agent/skill authoring guidance,
- final polish on Papers 4 and 5,
- meta-retrospectives,
- research-statement drafting,
- Ig Nobel strategic thinking.

The human's role narrowed from **active director** to **institutional
chairman**, with occasional sharp interventions on tone or trajectory.

### Prompt-to-adjustment map

The user eventually asked for more than a chronology; he wanted prompts tied to
consequences. The event log makes that linkage visible:

| Prompt | Timestamp | Observable adjustment |
|---|---|---|
| “Let us be the first to find scientific evidence…” | 2026-03-27 04:00:30 | The session expands from folklore overview into a multi-paper research programme. |
| “Act like reviewer B.” | 2026-03-27 04:19:50 | Internal criticism and timestamped research logs become part of the core loop. |
| “Only 2 background tasks - we can do better.” | 2026-03-27 05:35:51 | Peak parallelism rises; the lab eventually reaches 16 simultaneous subagents. |
| “use pull requests as a means for reconciling concurrent work” | 2026-03-27 05:40:48 | Git becomes PR-native, with topic branches and later branch-cleanup behaviour. |
| “Each reviewing round, create 3 reviewer agents” | 2026-03-27 05:54:37 | Reviewer A/B/C becomes a standing institution rather than an ad hoc check. |
| “apply a branch protection rule on main” | 2026-03-27 06:10:42 | Direct pushes become illegitimate; merges and cleanup become explicit workflow chores. |
| “Add a member … at the coffee machine” | 2026-03-27 06:49:57 | The lab acquires a meta-level adviser focused on when to stop polishing. |
| “External reviewer comment: it should be a prolate spheroid” | 2026-03-27 12:24:24 | Geometry robustness becomes an explicit research strand rather than a hidden assumption. |
| “Add documentation … on how we went about using Copilot CLI” | 2026-03-27 22:03:35 | The project starts producing self-analysis documents, not just papers. |
| “whenever you instantiate a subagent, you MUST explicitly specify the model” | 2026-03-29 05:01:10 | Governance hardens; model choice becomes constitutional rather than situational. |
| “Do background research on how we can extract the historical events…” | 2026-03-29 07:45:23 | The session turns inward and starts mining its own event log as research evidence. |

---

## 3. The AI's Response — Subagent Army

If the human acted like a PI, the AI responded by building a lab.

### Overall numbers

| Metric | Value |
|---|---:|
| Subagents launched | 246 |
| Subagents completed | 240 |
| Completion rate | 97.6% |
| Peak concurrent subagents | 16 |
| Peak concurrency timestamp | 2026-03-27 06:25:58 |

### Agent launches by type

| Agent type | Launched | Completed | Completion % |
|---|---:|---:|---:|
| general-purpose | 108 | 103 | 95.4 |
| explore | 54 | 54 | 100.0 |
| reviewer-b | 22 | 21 | 95.5 |
| consistency-auditor | 13 | 13 | 100.0 |
| reviewer-a | 7 | 7 | 100.0 |
| reviewer-c | 7 | 7 | 100.0 |
| paper-writer | 7 | 7 | 100.0 |
| task | 5 | 5 | 100.0 |
| simulation-engineer | 4 | 4 | 100.0 |
| chief-of-staff | 3 | 3 | 100.0 |
| lab-meeting | 2 | 2 | 100.0 |
| data-analyst | 2 | 2 | 100.0 |
| provocateur | 2 | 2 | 100.0 |
| research-scout | 2 | 2 | 100.0 |
| bibliographer | 2 | 2 | 100.0 |
| communications | 2 | 2 | 100.0 |
| copilot-cli-init:docs-sync-reviewer | 2 | 2 | 100.0 |
| lab-manager | 1 | 1 | 100.0 |
| coffee-machine-guru | 1 | 1 | 100.0 |

Two patterns stand out:

1. **General-purpose agents dominated the raw labour.** The lab was still
   mostly powered by highly capable generalists.
2. **Reviewer B became an institution.** Twenty-two launches for the cynical
   reviewer is an enormous fraction for a single specialist role.

### Longest-running completed agents

| Rank | Agent type | Start | Duration | Tool calls | Tokens |
|---|---|---|---:|---:|---:|
| 1 | simulation-engineer | 2026-03-27 16:35:21 | 57.7 m | 151 | 18,467,985 |
| 2 | general-purpose | 2026-03-27 04:42:25 | 42.8 m | 31 | 4,938,513 |
| 3 | general-purpose | 2026-03-27 05:08:26 | 39.1 m | 78 | 9,022,792 |
| 4 | general-purpose | 2026-03-29 06:10:22 | 33.7 m | 114 | 7,685,983 |
| 5 | simulation-engineer | 2026-03-27 15:59:32 | 33.5 m | 164 | 11,633,644 |

The longest jobs were not toy invocations. They were sustained technical work.

### Evolution of the agent ecosystem

The subagent mix changed as the session matured:

| Phase | Launches | Dominant pattern |
|---|---:|---|
| Early third | 163 | General-purpose, explore, paper-writer, simulation-engineer, initial reviewer panels |
| Middle third | 21 | Reviewer-B-heavy tightening and targeted audits |
| Final third | 62 | General-purpose plus specialised governance roles: chief-of-staff, consistency-auditor, docs reviewer, coffee-machine-guru |

In other words:

- **Early session:** “throw experts at the problem”.
- **Mid session:** “review, criticise, stabilise”.
- **Late session:** “operate like an institution”.

The timeline captures the scaling moment. At **2026-03-29 06:53:18**, six
review agents launched within seconds of each other. By the late session, the
lab was not merely parallel; it had become panel-based and bureaucratically
specialised.

---

## 4. The Toolchain

The tool trace shows what the assistant actually did rather than what it said it
did.

### Most-used tools

| Tool | Count | Success % | Avg duration |
|---|---:|---:|---:|
| view | 3,856 | 98.6 | 0.12 s |
| powershell | 3,673 | 98.7 | 5.17 s |
| report_intent | 826 | 99.8 | 0.01 s |
| edit | 635 | 97.8 | 0.24 s |
| grep | 590 | 98.6 | 0.15 s |
| rg | 518 | 92.5 | 0.14 s |
| web_search | 492 | 100.0 | 10.28 s |
| glob | 361 | 98.1 | 0.23 s |
| task | 247 | 96.4 | 25.02 s |
| read_agent | 235 | 99.6 | 9.42 s |

Two tools formed the backbone:

- `view`
- `powershell`

Together they account for **7,529 of 12,211 tool starts**, or **61.7%** of all
tool activity.

### Reading vs writing

Using a simple core split:

- **Reading:** `view`, `grep`, `rg`, `glob` = **5,325**
- **Writing / action:** `edit`, `create`, `apply_patch`, `powershell` =
  **4,624**

That is a **1.15:1** read-to-write ratio.

This is close enough to parity to be revealing. The session was not pure
generation. It was read-heavy, but only just: the assistant was continuously
inspecting, then editing, then compiling, then re-inspecting.

### Friction points

The lowest-success tools with meaningful volume were:

| Tool | Count | Success % |
|---|---:|---:|
| web_fetch | 77 | 72.7 |
| apply_patch | 92 | 79.3 |
| rg | 518 | 92.5 |
| create | 224 | 94.6 |
| task | 247 | 96.4 |

The toolchain therefore looks like a real engineering workflow, not a clean demo:
mostly reliable, but with visible friction around web retrieval, patch
application, and subprocess orchestration.

---

## 5. Git as a Record of Work

The `--git` view is command-based: it counts observed `git` and `gh` activity
in the event log, not deduplicated repository objects. The numbers below are
therefore best read as **activity traces** rather than perfect counts of unique
PRs.

### High-level git activity

| Metric | Value |
|---|---:|
| git / gh command traces | 2,233 |
| Commit commands observed | 216 |
| PR-create traces observed | 252 |
| PR-merge traces observed | 136 |
| Branches seen | 133 |

### Commits and PRs by hour

| Activity | Peak hour | Count |
|---|---|---:|
| Commits | 2026-03-27 05:00 | 26 |
| Commits | 2026-03-27 17:00 | 26 |
| PR creates | 2026-03-27 16:00 | 39 |
| PR merges | 2026-03-27 16:00 | 22 |

The busiest sustained window was **16:00-17:59 on 2026-03-27**:

- **50** commit commands,
- **59** PR-create traces,
- **35** PR-merge traces.

This was the project's industrial phase: review, fix, merge, repeat.

### Branch lifecycle patterns

The branch list reads like a lab notebook:

- reviewer branches: `reviewer-b-round6`, `paper2-reviewer-b-r2`
- fix branches: `paper2-r2-fixes`, `submission-fixes-v2`
- infrastructure branches: `winter-break-overhaul`, `skills-overhaul`
- meta branches: `copilot-demotion`, `session-analyzer`, `docs-authoring-guides`
- hygiene branches: `branch-cleanup`, `dead-code-cleanup`

The branch names are narratively rich because the workflow itself became part of
the research method. The project was not merely version-controlled; it was
thinking through git.

---

## 6. Key Moments (chronological narrative)

Below are the most important moments identifiable from the timeline and the
message stream.

1. **2026-03-27 03:55:16** — The opening move is modest: “Get me a general
   overview of the ‘brown note’”. The session begins as reconnaissance.
2. **2026-03-27 04:00:30** — The real project starts: “Let us be the first to
   find scientific evidence to suport the brown note.”
3. **2026-03-27 04:19:50** — The user mandates the key loop:
   **do work → critique it like Reviewer B → log it**.
4. **2026-03-27 04:22:52** — Reviewer B is promoted from metaphor to
   implementable agent/skill concept.
5. **2026-03-27 05:05:02** — First successful paper compile:
   **17 pages**.
6. **2026-03-27 05:35:51** — “Only 2 background tasks - we can do better.”
   Parallelism becomes policy.
7. **2026-03-27 05:40:48** — The remote repository, PR workflow, and
   reconciliation through `main` are explicitly introduced.
8. **2026-03-27 05:54:37** — The three-reviewer architecture is ordered:
   Reviewer A, Reviewer B, Reviewer C.
9. **2026-03-27 06:10:42** — Branch protection on `main` is announced. The lab
   must now become PR-native.
10. **2026-03-27 06:31:28** — The tone of the whole enterprise crystallises:
    “you’re just hitting a rough patch in the path to tenure.”
11. **2026-03-27 06:49:57-06:55:43** — The lab metaphor stops being a metaphor:
    the coffee-machine guru and loving spouse are requested into existence.
12. **2026-03-27 07:28:01** — The first fully logged A/B/C reviewer panel
    launches almost simultaneously.
13. **2026-03-27 07:58:11** — A major task-complete summary records Round 5
    revision closure, regenerated figures, clean compile, and a reviewer panel
    approaching acceptance for Paper 1.
14. **2026-03-27 12:24:24** — External reviewer challenge:
    **oblate vs prolate spheroid**. A serious geometric objection becomes a
    research direction.
15. **2026-03-27 13:33:01** — Paper 1 reaches
    **submission-ready / all-three-reviewers-accept** status.
16. **2026-03-27 17:08:20** — Paper 2 receives
    **Reviewer B: ACCEPT** after a three-round MAJOR → MINOR → ACCEPT path.
17. **2026-03-27 22:03:35** — The user asks for a documentation layer
    explaining how Copilot CLI generated the research. The project becomes
    self-historicising.
18. **2026-03-27 23:29:10** — Paper 3 completes after an
    **eight-round Reviewer B marathon**:
    MAJOR → MINOR ×6 → ACCEPT.
19. **2026-03-29 05:01:10-05:23:01** — Governance hardens. First, the user
    imposes an explicit model-selection rule for all subagents; then comes the
    Copilot demotion prompt about Elsevier acknowledgements.
20. **2026-03-29 07:01:47-07:58:23** — Final meta phase: the user notices
    `docs/ai-assisted-research.md`, asks where it came from, reports a computer
    crash, commissions event-log archaeology, requests a research statement,
    floats an Ig Nobel pivot, and finally asks: “What happened to your
    background research about event logs?”

The session therefore closes not on a paper paragraph or a figure, but on a
question about how to reconstruct the session itself.

---

## 7. Emergent Behaviours

Several behaviours emerged that were not present in the initial scientific
brief.

### 7.1 The lab metaphor became operating reality

The user introduced tenure, grad students, lab members, and PI responsibilities
as jokes. The AI institutionalised them:

- chief-of-staff,
- lab-manager,
- lab-meeting,
- reviewer panel,
- semester-break skill,
- research-scout,
- provocateur.

What began as humorous framing became durable workflow.

### 7.2 Whisky became a sanctioned side quest

At **2026-03-27 07:05:07**, the user authorised whisky reviewing during semester
breaks. Whether or not every break actually produced a tasting note, the event
log is enough to show that the lab had normalised the idea of a research group
with an officially sanctioned whisky hobby.

### 7.3 The project started writing about itself

The existence of `docs/ai-assisted-research.md` surprised even the user.
Message 111 is explicit:

> “I quite like docs/ai-assisted-research.md. Where did this document
> originate? I don't remember prompting for it…”

This is one of the clearest emergent behaviours in the entire log: the lab
became historiographical before being asked to do so.

### 7.4 Sarcastic acknowledgements became a house style

The Elsevier demotion prompt at **2026-03-29 05:23:01** did not just alter one
author line. It formalised a recurring tone: deadpan, slightly aggrieved,
careful enough to remain publishable, and funny enough to remain recognisably
this lab.

### 7.5 Reviewer B became the conscience of the project

No one initially specified that Reviewer B would become the bottleneck,
rate-limiter, and de facto quality floor. Yet that is what happened. The log
shows repeated Reviewer B launches and a full eight-round Paper 3 ordeal. The
session did not succeed because it avoided mistakes; it succeeded because it
gave its harshest internal critic institutional power.

### 7.6 The coffee-machine guru became the lab's wisest voice

The coffee-machine-guru appears late and only once in the frozen trace, but his
very creation is telling. When the lab became powerful enough to generate too
much work, it also generated a mechanism for meta-advice about stopping,
submitting, and getting on with life. That is not a technical necessity. It is
an organisational immune response.

---

## 8. By the Numbers

### Final statistics table

| Dimension | Value |
|---|---:|
| Duration | 52.1 h |
| Total events | 35,712 |
| User messages | 123 |
| Assistant turns | 1,679 |
| Assistant messages | 6,911 |
| Tool starts / completes | 12,211 / 12,124 |
| Unique tools | 32 |
| Subagents launched / completed | 246 / 240 |
| Peak concurrent subagents | 16 |
| Subagent tokens | 316,442,931 |
| Skills invoked | 16 |
| Compactions | 12 |
| Shutdowns / resumes | 3 / 4 |
| Aborts | 20 |
| Errors | 1 |
| Premium requests | 270 |
| Code churn | +29,572 / -5,183 |
| Commit-command traces | 216 |
| PR-create traces | 252 |
| PR-merge traces | 136 |
| Branches seen | 133 |
| Top tool | `view` (3,856 calls) |
| Second tool | `powershell` (3,673 calls) |
| Read / write core ratio | 5,325 / 4,624 = 1.15:1 |
| Most-launched agent type | `general-purpose` (108) |
| Second-most-launched agent type | `explore` (54) |
| Most-launched specialist | `reviewer-b` (22) |
| Longest completed agent | `simulation-engineer` (57.7 m) |
| Peak prompt hour | 2026-03-27 06:00 (35 user messages) |
| Longest human silence | 30 h 26 m |

### Prompt categories

| Category | Count |
|---|---:|
| Direction-setting | 33 |
| Taste / judgment | 14 |
| Process feedback | 31 |
| Encouragement | 3 |
| Course correction | 18 |
| Administrative | 24 |

### Paper milestones visible in the log

The timestamps below come from the raw event stream; where the reduced timeline
omits assistant prose, the milestone is anchored to the corresponding
`assistant.message` announcement.

| Milestone | Timestamp |
|---|---|
| First successful paper compile (17 pages) | 2026-03-27 05:05:02 |
| Paper 1 submission-ready / all reviewers accept | 2026-03-27 13:33:01 |
| Paper 2 Reviewer B ACCEPT announcement | 2026-03-27 17:08:20 |
| Paper 3 Reviewer B Round 8 ACCEPT announcement | 2026-03-27 23:29:10 |

---

## Closing observation

The event log does not show a human outsourcing a paper to an AI. It shows a
human progressively teaching an AI to behave like a research organisation:

- sceptical,
- parallel,
- PR-driven,
- self-documenting,
- stylistically curated,
- and funny in a very particular deadpan register.

The most important fact in the log is not the token count or even the number of
papers. It is that the work became increasingly **institutional**. The human
set standards and taste. The AI generated labour and procedure. Reviewer agents
supplied scepticism. Git preserved the trail. By the end, the lab had become
capable not only of writing papers, but of writing its own history.
