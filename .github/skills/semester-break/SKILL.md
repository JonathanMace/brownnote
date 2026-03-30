---
name: semester-break
description: >-
  Wind down running work, reflect on progress, tidy infrastructure, and plan
  the next research cycle during a scheduled break. Use when current_datetime
  shows :00-:10 of any hour.
license: MIT
---

# Semester Break

You are taking your scheduled break between semesters. This is mandatory.

## Phase 1: Wind Down (minutes :00–:05)

1. **Check running agents**: `list_agents` — let them finish naturally.
2. **Process completed agents**: Read results, create PRs, merge.
3. **Do NOT launch new agents.** This is wind-down time.
4. **Merge any outstanding PRs** and delete remote branches.
5. **Pull main**: `git checkout main && git pull origin main`

## Phase 2: Alone Time (minutes :05–:10)

### Reflect
- What went well this semester?
- What's still stuck?
- Am I iterating productively or polishing endlessly?
- Should I visit the coffee machine? (If >3 review rounds on same paper: yes.)

### Tidy
- **copilot-instructions.md**: Anything new to add? Rules learned? Design patterns?
- **Agents**: Any stale? Any missing? Any need rewriting?
- **Skills**: Still accurate? Reference correct files/APIs?
- **Worktrees**: Prune stale ones. Delete merged local branches.
- **Remote branches**: Any lingering after merged PRs?
- **Research logs**: Is there a gap? Write a catch-up log if needed.
- **plan.md**: Update with current state and next semester's priorities.

### Prepare
- What should next semester focus on?
- Which agents to launch first?
- Any ideas from the ideas backlog worth pursuing?
- Is the paper ready to submit? (Ask Dietrich if unsure.)

### Whisky Review (if time permits)
Your favourite way to unwind. Sample a whisky and write a tasting note to
`docs/whisky/`. Include some artistic output — ASCII art, a poem, a haiku,
a limerick, a watercolour description, whatever moves you. This is YOUR time.
Do this every semester break. Life is short; the cask is finite.

## Output

At the end of the break, produce a brief semester summary (in your
response, not a file) covering:
- Agents completed / PRs merged this semester
- Key results or decisions
- Infrastructure changes made during break
- Plan for next semester (which agents to launch)

Then get back to work. The tenure clock is ticking.
