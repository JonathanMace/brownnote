---
name: write-research-log
description: >-
  Document a productive research session with quantitative results, changes
  made, and next steps in docs/research-logs/. Use when logging work or
  writing a reviewer report.
license: MIT
---

# Research Log Instructions

You are writing a research log entry. Follow this format strictly.

## Required Format

Every research log entry MUST include:

```markdown
# [Topic] — [Date ISO 8601]

**Author**: [Agent name or Opus]
**Branch**: [git branch name]
**PR**: #[number] (if applicable)

## Summary
[2-3 sentence overview of what was done]

## Key Findings
- [Bullet points of quantitative results]
- [Include specific numbers, not vague claims]

## Changes Made
- [List of files created or modified]

## Issues Identified
- [Any problems found, with severity: CRITICAL / MAJOR / MINOR]

## Next Steps
- [What should happen next based on these findings]
```

## Rules

1. **Always include quantitative results.** "The frequency changed" is unacceptable.
   "f₂ shifted from 3.95 Hz to 4.19 Hz (+6%)" is correct.
2. **Every log entry should have a companion PDF snapshot** of the paper at that point,
   saved as `YYYY-MM-DDTHHMM-paper-snapshot.pdf` in this same directory.
3. **Use ISO 8601 timestamps** in filenames: `YYYY-MM-DDTHHMM-topic.md`
4. **Reference canonical parameters** — if any computation used non-canonical values, note why.
5. **Link to relevant code** — e.g., "See `src/analytical/energy_budget.py:L45`"
6. **Be honest about negative results.** "The viscous correction was <2% and can be neglected"
   is a valid and important finding.

## Reviewer Report Format

For reviewer reports specifically, also include:

```markdown
## Recommendation
[ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT]

## Fatal Flaws (if any)
[Issues that would prevent publication]

## Major Issues
[Numbered list with specific locations and suggested fixes]

## Minor Issues
[Numbered list]

## Positive Aspects
[What works well — reviewers should acknowledge strengths]
```
