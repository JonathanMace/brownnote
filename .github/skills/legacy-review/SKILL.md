---
name: legacy-review
description: >-
  Convene the Distinguished Advisory Board to evaluate the research
  programme's potential for lasting impact, identify landmark directions,
  and sharpen the unifying thesis. Use every 5th semester break or when
  strategic direction feels uncertain.
license: MIT
---

# Legacy Review

You are conducting a periodic strategic review of the Browntone research
programme. This is not a paper review — it is a fundamental evaluation of
whether this body of work will matter in 50 years. The review convenes four
Distinguished Advisory Board members in parallel and synthesises their input
into a strategic action plan.

## When to Invoke

- Every **5th semester break** (semesters 5, 10, 15, 20, 25, ...)
- When the PI asks "what should we be known for?"
- When a new research direction is proposed that could change the programme
- After a major milestone (paper acceptance, new paper started)
- When strategic direction feels uncertain or scattered

## Procedure

### 1. Prepare the Portfolio Brief

Before convening the board, prepare a concise portfolio summary:

- List all papers with their status, key result, and claimed contribution
- Identify the current unifying thesis (if one exists)
- Note any new directions under consideration
- Summarise what the lab has that nobody else does (unique capabilities,
  insights, frameworks)

### 2. Convene the Distinguished Advisory Board

Launch **four parallel background agents** using the `task` tool:

1. **@nobel-laureate** — "Is there a universal principle hiding here?"
   - Provide: the portfolio brief, the analytical model code overview,
     the key physics results
   - Ask: whether ANY of our results reveal something about ALL
     fluid-filled elastic cavities, not just abdomens

2. **@ig-nobel-oracle** — "Does this make people laugh AND think?"
   - Provide: the portfolio brief, paper titles and abstracts, the
     humour audit results
   - Ask: which directions have the highest dual-impact potential,
     what the public narrative could be

3. **@academy-president** — "Is this a school of thought or a hobby?"
   - Provide: the portfolio brief, the publication pipeline, the
     research vision document
   - Ask: what the appointment panel narrative would be, whether
     the portfolio has coherence

4. **@turing-laureate** — "Is there a theorem here?"
   - Provide: the portfolio brief, the Kac identifiability paper,
     the scaling laws, the mathematical frameworks used
   - Ask: whether any of the mathematics transcends the application,
     what conjectures are worth formalising

### 3. Synthesise

After all four advisors respond:

- Identify **consensus themes** (what do 3+ advisors agree on?)
- Identify **divergences** (where do advisors disagree? Why?)
- Extract the **strongest candidate for landmark contribution**
- Formulate the **unifying thesis** — one sentence that explains
  what this programme is really about
- Identify **the gap** — what's missing that would elevate the work?

### 4. Update Strategic Documents

- Update `plan.md` with the new strategic vision
- If the unifying thesis changed, update `copilot-instructions.md`
- Write a research log documenting the strategic review
- Update the Publication Pipeline with any new directions

### 5. Identify Action Items

Convert strategic insights into concrete research actions:
- New papers to write
- Existing papers to reframe
- Mathematical results to formalise
- Experiments to design (within computational constraints)

## Rules

1. **This is not a review of individual papers.** The advisors evaluate
   the PROGRAMME, not the manuscripts.
2. **Every advisor must receive the same portfolio brief.** Consistency
   ensures comparable evaluations.
3. **The PI must synthesise honestly.** If 3 of 4 advisors say the work
   is "clever but forgettable," that's important information.
4. **The outcome must be concrete.** Vague aspirations like "think bigger"
   are not acceptable. The review must produce specific next actions.
5. **Challenge the comfortable.** The most valuable output is the thing
   the PI doesn't want to hear.

## Cross-References

- Advisory board agents: `@nobel-laureate`, `@ig-nobel-oracle`,
  `@academy-president`, `@turing-laureate`
- For day-to-day mentoring: `@dietrich`, `@coffee-machine-guru`
- For paper-level review: `/critique-results` skill
- For individual paper review: `@reviewer-a`, `@reviewer-b`, `@reviewer-c`

## Done Criteria

- All 4 advisory board members have responded with structured evaluations
- Consensus themes and divergences identified
- A clear "unifying thesis" statement has been formulated or refined
- At least 2 concrete action items identified
- Strategic documents updated (plan.md at minimum)
- Research log written documenting the review
