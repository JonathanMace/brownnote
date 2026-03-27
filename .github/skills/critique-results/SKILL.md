---
name: critique-results
description: >
  Invoke the Reviewer B agent to critically analyze recent computational results,
  figures, or code. Use after generating new results or completing a work phase
  to identify flaws before they propagate.
---

# Critique Results Skill

When this skill is invoked, perform the following steps:

## 1. Gather Current State

- Read the most recent research log in `docs/research-logs/`
- Read the analytical computation code in `src/analytical/`
- Check any recently generated figures in `data/figures/`
- Read the most recent test results if available

## 2. Apply Reviewer B Criteria

Evaluate all recent work against these standards:

### Physics Correctness
- [ ] Are governing equations dimensionally consistent?
- [ ] Are material properties within published ranges?
- [ ] Is the acoustic-structure coupling properly formulated?
- [ ] Is the impedance mismatch accounted for?
- [ ] Is the quality factor Q justified (not just assumed)?

### Numerical Quality
- [ ] Are results converged (mesh/frequency resolution)?
- [ ] Do limiting cases recover known solutions?
- [ ] Are boundary conditions physically motivated?

### Scientific Honesty
- [ ] Are claims proportional to evidence?
- [ ] Are limitations explicitly stated?
- [ ] Is the PIEZO channel comparison valid (bulk displacement vs local indentation)?
- [ ] Are uncertainty bounds provided?

### Presentation Quality
- [ ] Do figures have proper labels, units, legends?
- [ ] Are axes scaled appropriately?
- [ ] Is the color scheme accessible?

## 3. Output

Write a critique to a new timestamped file:
`docs/research-logs/YYYY-MM-DDTHHMM-critique-{topic}.md`

Format:
```markdown
# Critique — [Topic] — [Date]

## Summary Assessment
[One paragraph: overall quality and publishability]

## Major Issues (Must Fix)
1. [Issue with specific reference to code/figure/equation]
...

## Minor Issues (Should Fix)
1. [Issue]
...

## Questions
1. [What needs clarification or investigation]
...

## Recommendation
[What to do next, prioritized]
```
