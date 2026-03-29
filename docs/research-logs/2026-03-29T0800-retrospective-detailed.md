# Research log — 2026-03-29T0800 — Detailed human-AI retrospective

**Author:** Opus  
**Branch:** `retrospective-detailed`

## Summary

Reconstructed a detailed history of the Browntone collaboration from git,
merged-PR metadata, research logs, review reports, and instruction-history
commits. Added `docs/ai-assisted-research-detailed.md` as a substantially more
forensic companion to the earlier high-level retrospective.

## Quantitative findings captured

- Current repo history mined: **277 commits**
- Merged PRs visible from GitHub CLI: **116**
- Research-log files read/indexed: **59**
- Current agent definitions: **17**
- Current baseline test suite: **199/199 passing**
- Paper-page counts recorded from current logs: **38 pp** (Paper 1 log state),
  **16 pp** (Paper 2), **11 pp** (Paper 3), **27 pp** (Paper 4), **18 pp**
  (Paper 5)
- Test-growth trajectory documented: **97 -> 118 -> 153 -> 183 -> 198 -> 199**

## Main conclusions recorded

1. The project evolved from a single permissive prompt into a governed lab.
2. Reviewer-driven correction, especially Reviewer B, mattered more than first
   draft quality.
3. Jonathan's strongest interventions were about taste, policy, framing, and
   submission timing rather than line-level drafting.
4. Opus's strongest contribution was operational scale: branching, drafting,
   testing, reviewing, and multiplying adjacent paper ideas.

## Files changed

- `docs/ai-assisted-research-detailed.md`
- `docs/research-logs/2026-03-29T0800-retrospective-detailed.md`

## Validation

- Baseline repository tests run before documentation changes:
  `python -m pytest tests\ -v`
- Result: **199 passed, 1 warning in 9.11 s**

## Next steps

- Commit and ship the retrospective via PR.
- If the retrospective is later expanded again, add line-level citations back to
  specific logs/commits in footnotes.
