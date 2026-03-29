# Journal Editor agent creation

- Timestamp: `2026-03-29T0130`
- Branch: `create-editor`
- Scope: add a pre-submission JSV Associate Editor persona for desk-rejection filtering.

## Files changed
- `.github/agents/journal-editor.md` — new agent definition
- `.github/copilot-instructions.md` — agent roster updated
- `README.md` — custom-agent count updated from 16 to 17

## Quantitative summary
- Agents in `.github/agents/`: 16 -> 17 (+1, +6.25%)
- Repository files edited: 3 existing files + 1 new agent file
- Tests run: 0 (agent/documentation-only change; no repository validation target exists for agent markdown)

## Editorial design choices
1. Positioned the role as an Associate Editor, not a reviewer, to keep the decision centred on desk rejection versus send-to-review.
2. Added explicit journal-redirection guidance so the agent can recommend JASA, Applied Acoustics, IJMS, or biomechanics venues when JSV fit is weak.
3. Added a seriousness threshold for joke-adjacent topics so the paper must clear the "brown note" filter immediately.

## Risks
- The new agent file uses the user-requested filename `journal-editor.md` rather than the more common `.agent.md` suffix used elsewhere in the repository.
- No automated validation currently checks agent frontmatter or section completeness.
