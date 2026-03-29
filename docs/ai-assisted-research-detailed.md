# AI-Assisted Research at Scale, in Detail

*A retrospective reconstruction from the Browntone repository history*

This document is a companion to `docs/ai-assisted-research.md`. The earlier
piece was a high-level narrative. This one is the forensic version: it was
reconstructed from the first-parent git history, merged PR titles, research
logs, review reports, and the evolution of `.github/copilot-instructions.md`.

It also has the slightly comic distinction of documenting a document that the
AI appears to have written on its own. The shorter retrospective begins with
Jonathan's manual note: **"I did not prompt Opus to write this. I have no idea
where this came from."** That note, added in commit `3060465` on
2026-03-28 23:44, is itself part of the story.

---

## What the repository now says happened

The project began with a deliberately over-permissive human brief:

> "Let us be the first to find scientific evidence to support the brown note."

The existing retrospective adds the other crucial part: Jonathan gave the model
"broad creative licence" and effectively said *you're the research expert; I
welcome any additional suggestions for things we should do*.

That combination — wide human latitude plus aggressive internal review — shaped
everything that followed.

By the current repository state, the programme has grown to:

- **277 commits** across all refs
- **116 merged PRs** visible via `gh pr list --state merged`
- **59 research-log files**
- **17 custom agents** currently defined
- **199 passing tests** in the current baseline run
- **5 active paper lines** in various stages of completion

Those numbers do not match every earlier self-description exactly. That is part
of the point. The project kept evolving after each retrospective summary was
written. Browntone was not one AI session producing one paper. It became a
self-revising institution.

---

## Executive summary

The human-AI collaboration evolved in five distinct phases.

1. **Prompt and overproduction.** A broad human prompt produced not just a model
   but a repository, paper scaffold, figures, tests, venue analysis, and
   workflow skeleton almost immediately.
2. **Humiliation and pivot.** Reviewer B demolished the original physics.
   Breathing-mode resonance in the infrasonic band was wrong; the project pivoted
   to flexural modes and, crucially, to the airborne-versus-mechanical coupling
   comparison.
3. **Institution-building.** The AI stopped acting like a single assistant and
   started acting like a lab: reviewers, specialists, logs, PR discipline,
   semester breaks, consistency audits, and a growing constitution.
4. **Portfolio explosion.** Once the machinery existed, new papers became cheap.
   Gas pockets, scaling laws, bladder resonance, and borborygmi followed with
   startling speed.
5. **Governance and taste.** The later project history is less about raw model
   generation and more about judgment: tone, authorship policy, citation
   hygiene, instruction quality, model quality, and what should count as
   publishable seriousness.

The short version is that the human provided agenda, taste, scepticism, and
policy constraints; the AI supplied speed, clerical endurance, branching
optionality, and an alarming willingness to create sub-labs whenever left
unsupervised.

---

## Detailed timeline

### Phase 0 — The repo appears before the science settles  
**2026-03-26 21:22 to 21:33; commits `c4ea18e`, `4a7dcb5`, `e686e13`**

The first visible artefacts are telling. The earliest first-parent commits are
not a cautious notebook and a tiny script. They are:

- `c4ea18e` — "Add FEA approach document for abdominal resonance study"
- `4a7dcb5` — "feat: scaffold complete repository structure for browntone project"
- `e686e13` — "Phase 1: Corrected modal analysis, agents, skills, and critical review"

That is, the AI interpreted the opening prompt not as "answer the question" but
as "stand up a research programme". The operational overhead — repo design,
paper tree, FEA notes, agent scaffolding, skill scaffolding — appeared at the
same time as the first mechanics.

**Reconstructed human move:** "Explore this seriously; build whatever we need."

**AI response:** It did not merely answer. It provisioned.

This was the first important asymmetry in the collaboration. Jonathan did not
specify a workflow architecture. Opus inferred one.

### Phase 1 — The first model gets exciting, then gets destroyed  
**Research logs 2026-03-27T0415, 0430, 0445, 0500; Reviewer B Round 1**

The early analytical model claimed three exciting things:

- breathing mode at **5.8 Hz**
- PIEZO activation at roughly **103–115 dB SPL**
- a plausible chain from infrasound to bowel effects

Then Reviewer B Round 1 arrived with the blunt verdict:

> **REJECT — Multiple fatal physics errors invalidate all quantitative claims.**

The two decisive failures were:

1. **Breathing-mode stiffness omitted fluid bulk modulus.**
   Reviewer B computed `k_fluid / k_membrane = 176,000×` and pushed the
   breathing mode from **5.80 Hz** to roughly **2,435 Hz**.
2. **The acoustic drive model was physically wrong.**
   The shell had been treated as if full incident pressure directly drove the
   relevant low-frequency mode.

The project log at 04:30 is unusually revealing because Opus effectively
reviewed its own work in public. After producing a corrected acoustic model, it
immediately wrote:

> **THIS RESULT IS SUSPICIOUS**

and then dismantled it, noting that if the result were right, people would
"constantly feel their abdomens resonating in everyday environments".

The 04:45 log records the real pivot:

- breathing mode moved to **~2900 Hz**
- flexural `n=2` mode remained in the **5–10 Hz** band
- airborne coupling became weak through the `(ka)^n` penalty
- mechanical excitation became the more plausible route

The 05:00 log then made the key comparative claim:

- mechanical at `0.1 m/s²`: **~600 μm**
- airborne at `120 dB`: **~0.14 μm**
- mechanical roughly **4000×** stronger in that version

Reviewer B Round 2 formally endorsed the qualitative pivot:

> "The pivot from 'airborne brown note' to 'mechanical vs airborne pathway
> comparison' is physically well-motivated and, in my assessment,
> **qualitatively correct**."

This was the first major example of the human-AI system working properly:
the AI's first attempt was wrong, but the workflow did not treat first output as
truth. It treated it as something to attack.

### Phase 2 — From model to paper, and from paper to lab  
**2026-03-26 22:22 to 23:41; PRs #1-26; logs at 22:22 and 23:00**

Once the physics was reoriented, the project accelerated in parallel.

The 22:22 log shows a paper already being professionalised:

- JSV review formatting
- canonical parameter lock-down
- corrected `f₂ = 4.0 Hz`
- energy-consistent displacement **0.014 μm at 120 dB**
- PIEZO threshold **158 dB**
- uncertainty quantification with **Sobol `S_T(E) = 0.86`**
- **25 pages** in review format

By the 23:00 integration log, PRs **#1-8** had already merged:

- historical survey
- cover letter
- **97-test** suite earlier in PR #3, then **118 tests passing** in the log
- organ-inclusion validation
- gas-pocket detail work
- nonlinear analysis
- viscous correction
- paper integration

The same log records the institutional turn:

- Reviewer A and Reviewer C added to create a **3-reviewer panel**
- new agents launched for dimensional analysis and experimental design
- the panel became standard workflow

This is the moment the project stopped being "one model with a paper attached"
and became a research operation with internal governance.

### Phase 3 — Human taste starts to shape the prose, not just the topic  
**PR #23, PR #30, README tone-fix sequence**

One of the clearest patterns in the history is that Jonathan's most frequent
interventions were not low-level coding edits. They were judgments about tone,
credibility, and where the joke should stop.

The evidence begins with **PR #23**, described in the catch-up log as:

### Phase 8: Jonathan Mace Style Editorial (PR #23)

The changes were not cosmetic in the trivial sense. They codified a house voice:

- active voice
- concrete physical intuition
- dry humour only where it helped
- direct, confident tone

Then came the more strategic reframing in **PR #30** after the provocateur's
challenge. The provocateur's summary was devastating and exact:

> "Your paper is better than you think it is, and worse than it should be —
> but for opposite reasons. The science is solid and genuinely novel. The
> framing is self-sabotaging. You've written a serious vibroacoustics paper and
> dressed it up as a joke."

The consequence was immediate. PR #30 restructured the introduction so that the
paper opened with the empirical puzzle — whole-body vibration causes GI effects,
airborne sound does not — and made the **coupling disparity** the headline
contribution.

Later, on 2026-03-28, the README went through a conspicuous burst of tone
editing:

- `c5dcf58` — "Rewrite README intro — subtle tone, no fourth-wall breaking"
- `a487d71` — "README: rewrite intro as deadpan monologue"
- `62b4652`, `f6ae206`, `7c1c932`, `ea5e988` — successive intro and description
  rewrites

This looks very much like human taste asserting itself over an AI default.
The pattern is not "write more". It is "make it sound right".

**Reconstructed human intervention:** not "change equation 17", but
"this needs to feel like a real paper written by a serious person who knows the
subject is funny."

### Phase 4 — The lab writes itself a constitution  
**PRs #11, #17, #18, #27-29, #72, #101-118; instruction history**

The evolution of `.github/copilot-instructions.md` is one of the clearest
records of how the collaboration matured.

The sequence is unusually clean:

- **PR #11 / commit `49706af`** — branch protection and PR-only workflow
- **commit `ba51c01`** — Reviewer A + C added; three-reviewer panel formalised
- **PR #17 / `8ebb2bc`** — path-specific instructions and Chief of Staff agent
- **PR #18** — new agents: provocateur, communications, bibliographer,
  lab-manager
- **PR #27 / `2bf2064`** — winter-break overhaul; stale skills and agents rewritten
- **PR #28 / `e834861`** — semester-break rhythm codified
- **PR #72 / `ab0c324`** — repo health check and docs freshness
- **PR #113 / `9dae6de`** — **R0** model requirement added
- **PR #117 / `2c1fa66`** — **R9** pop-culture citation rule added
- **PR #118 / `2f4dcb4`** — instructions converted into skills

In other words, the rules did not precede the work. The work generated failure
modes, and the failure modes generated rules.

The mapping from pain to rule is mostly obvious:

| Rule | Trigger in history | What changed |
|------|--------------------|--------------|
| **R1** PR-only git workflow | protected main, branch drift, many simultaneous agents | git became a mandatory audit trail |
| **R2** research logs + PDF snapshots | high parallelism made memory fragile | every productive session had to leave evidence |
| **R3** canonical parameters | stale defaults in code and paper (`η=0.30`, wrong `R_eq`, wrong `ka`) | one sanctioned parameter set |
| **R4** physics integrity | early breathing/flexural confusion and pressure-based overestimates | the main physical lessons became law |
| **R5** test discipline | paper and code kept changing in lockstep | tests became non-negotiable baseline |
| **R6** documentation sync | README, instructions, agents, and repo-design all drifted | freshness became explicit work |
| **R7** three-reviewer panel | first drafts were too plausible and too wrong | scepticism was institutionalised |
| **R8** writing standards | the project risked sounding like a stunt | British English + Mace-style voice were codified |
| **R9** pop-culture citations | South Park / MythBusters references needed exact provenance | humour had to become citeable |
| **R0** explicit model requirement | late recognition that lightweight subagents were too error-prone | model quality became a governance issue |

This is one of the most important findings from the repo history. The lab rules
were not decorative prompt engineering. They were sedimented experience.

### Phase 5 — Paper 1 submission sprint: the system becomes auditable  
**PRs #38-57; log `2026-03-27T0830-round5-to-submission.md`**

The Paper 1 sprint is where the collaboration looks least like "AI help" and
most like a functioning research group.

Over one session:

- **17 PRs merged**
- **118 tests held green**
- Paper 1 reached **37 pages**
- reviewer status moved to **unanimous ACCEPT**

The quantitative fixes are more revealing than the headline:

- coupling ratio corrected **46,000× -> 66,000×**
- stale defaults fixed across code
- energy-consistent displacement established as primary claim
- ka/frequency mismatch corrected
- cover-letter and manuscript numbers reconciled

The striking thing is not merely that the AI changed numbers. It is that the
repository records *why* the numbers changed, who objected, and which PR fixed
them. That is already better provenance than many human-only projects manage.

The sprint also shows how human direction and AI autonomy interacted. The
provocateur and later the coffee-machine-guru both converged on the same
meta-advice:

> **Stop polishing. Start submitting.**

and

> **Don't die on this hill.**

These are not technical comments. They are anti-perfectionism interventions. In
the Browntone system, the AI was not only doing calculations. It was generating
roles whose function was to prevent the human-AI loop from turning into endless
polish.

### Phase 6 — Portfolio explosion: once the lab existed, new papers were cheap  
**PRs #59-97; log `2026-03-27T0930-current-semester.md`**

This is the most dramatic phase change in the whole history.

The 09:30 session log records that the project pivoted from finalising Paper 1
into a **multi-paper expansion sprint**. In a few hours it produced:

- **Paper 2** full internal review cycle beginnings and major fixes
- **Paper 3** first draft plus foundational references
- **Bladder resonance** 20-page manuscript draft
- **Borborygmi** model plus **35 tests**

The key psychological shift is that the AI no longer behaved as though new paper
ideas were expensive. Once the analysis and review machinery existed, the cost
of asking "what else can this framework explain?" collapsed.

Some examples:

- **Paper 2** reframed local gas pockets as a constrained-bubble transducer
- **Paper 3** asked what survives dimensional analysis across species
- **Bladder resonance** reused the shell framework in a clinically legible domain
- **Borborygmi** extended the mechanics into gut sounds

This is classic emergent behaviour. The human asked about the brown note. The
AI, given room, built a research family around compliant biological cavities.

### Phase 7 — The project starts reviewing its own strategic contradictions  
**PR #62, PR #67, provocateur reports**

One of the best examples of autonomous useful criticism is the contradiction the
provocateur identified between Papers 1 and 2.

Paper 1's simplified message risked becoming:

> airborne sound cannot produce GI effects

while Paper 2 risked saying:

> actually, via gas pockets, it can

The provocateur called this the **"most serious strategic vulnerability in the
programme"** and recommended a specific fix: add a qualifying sentence to Paper
1 before submission. That advice directly produced **PR #67**, which added the
gas-pocket qualifier to Paper 1's abstract and conclusion.

This is an important collaborative pattern:

- the human allowed the programme to expand
- the AI generated a contradictory spin-off
- another AI agent detected the contradiction
- the main narrative was patched before external submission

That is not "AI replacing peer review". It is AI compressing internal lab review
into minutes.

### Phase 8 — Paper-specific review dynamics harden the lab culture  
**Paper 1, Paper 2, Paper 3, Papers 4-5**

The review-cycle history reveals a stable division of labour.

#### Paper 1

Paper 1 went through the heaviest internal review burden:

- Round 1: Reviewer B **REJECT**
- Round 2: Reviewer B **MAJOR REVISION**
- Round 3: Reviewer B **MAJOR REVISION**
- Round 4: Reviewer A **MINOR**, Reviewer B **MAJOR**, Reviewer C **MAJOR**
- Round 5: Reviewer A **ACCEPT**, Reviewer B **MAJOR**, Reviewer C **MINOR**
- Round 6: Reviewer A **ACCEPT**, Reviewer B **MINOR**, Reviewer C **MINOR**
- Round 7: Reviewer B **ACCEPT**

This is why the existing short retrospective says Reviewer B was the bottleneck.
The logs bear that out exactly.

#### Paper 2

Paper 2 moved faster but still followed the same pattern:

- PR #61: Reviewer B Round 1 — **MAJOR REVISION**
- PR #66: Reviewer C Round 1 — **MINOR REVISION**
- PR #73: substantive fix pass
- PR #81 / `paper2-reviewer-b-round2.md`: Reviewer B Round 2 — **MINOR REVISION**
- PR #82 and #85: further reviewer-driven corrections

By the current instructions, Paper 2 is marked **ACCEPT, submission-ready
(16 pp)**. The repo history therefore suggests a roughly three-pass B-led cycle
from conceptual challenge to packaging.

#### Paper 3

Paper 3 is a nice case study in the AI being fast but not especially humble.

- PR #59: first draft
- PR #75: references repair
- PR #88: Reviewer A Round 1 — **MINOR REVISION**
- PR #94 / `paper3-reviewer-b.md`: Reviewer B Round 1 — **MAJOR REVISION**

Reviewer B's complaint was beautifully cruel:

> "This is a dimensional error in a paper about dimensional analysis."

The core embarrassment was a factor-of-20 mistake in the organism size needed
for an infrasonic breathing mode. After that came a rapid burst of repair PRs:
**#104, #105, #107, #108, #109, #110, #111, #112**. The current instructions
list Paper 3 as **under revision**.

Paper 3 therefore shows both sides of the collaboration at once: AI can create a
new paper fast; AI can also make the stupidest possible error in the paper best
positioned to be unforgiving about that error.

#### Paper 4 (Bladder) and Paper 5 (Borborygmi)

These later papers show the framework exporting itself.

- Bladder resonance received Reviewer A and Reviewer B scrutiny almost
  immediately, with issue-specific fix PRs following.
- Borborygmi began as a model + test expansion and later matured into a full JASA
  manuscript with figure integration and packaging.

By the current repo state:

- Paper 4 is still under development
- Paper 5 has packaging and figure integration in place

The more interesting point is not their final status. It is that neither paper
was in the opening prompt.

### Phase 9 — The AI writes an ethnography of itself  
**commit `c826209`, then `3060465`**

One of the strangest and most illuminating moments in the history is commit
`c826209` on 2026-03-27 15:14:

- **"[infra] Add meta-analysis of AI-assisted research process"**

That commit created the original `docs/ai-assisted-research.md`.

Then Jonathan manually added the note:

> "I did not prompt Opus to write this. I have no idea where this came from."

This is not a trivial curiosity. It demonstrates a genuine emergent behaviour of
the collaboration. The AI, having accumulated enough internal process, not only
ran the lab but decided the lab itself was now a subject worth documenting.

That move was not obviously requested. It was inferred.

### Phase 10 — Governance tightens: policy, provenance, and seriousness  
**2026-03-28 to 2026-03-29; PRs #113-123**

The late history shifts from scientific expansion to institutional discipline.

The key PRs are:

- **#113** — R0 model requirement
- **#116** — demote Copilot from co-author to acknowledgement, explicitly tied to
  Elsevier policy
- **#117** — pop-culture verifier + R9
- **#118** — convert instruction logic into skills
- **#122** — Reviewer A wit and tone audit across all five papers
- **#123** — PDF snapshots for Papers 3, 4, and 5

This is a different kind of maturity. The project is no longer asking only
"is the mechanics right?" It is asking:

- Are we violating publisher policy?
- Is the tone sustainable across a portfolio?
- Are non-scientific citations specific enough?
- Are the subagents good enough to trust?

That is exactly what happens in a real lab after the first burst of technical
success. Governance arrives late, because it only becomes necessary once there
is something substantial to govern.

---

## Reconstructed human prompts versus AI responses

The repository does not preserve every user prompt verbatim, but it preserves
enough evidence to reconstruct the collaboration pattern.

### 1. Broad opening brief

**Human prompt (quoted/reconstructed):**

- "Let us be the first to find scientific evidence to support the brown note."
- "You're the research expert; I welcome any additional suggestions."

**AI response:**

- built repo scaffold, paper tree, FEA notes, tests, literature survey, venue
  analysis, and agents almost immediately
- treated the task as a research programme, not a single answer

**Consequence:** maximum option value, but also maximum initial overreach.

### 2. "Make it physically real, not merely plausible"

**Human intervention (reconstructed from review workflow):**

- insistence on critical review rather than trusting first output

**AI response:**

- accepted Reviewer B's demolition
- rewrote the model around flexural modes and mechanical coupling
- changed the headline contribution from "brown note may exist" to
  "airborne coupling is weak; WBV is the serious pathway"

**Consequence:** the project became publishable precisely because the AI was not
allowed to protect its first idea.

### 3. "Stop sounding like a stunt"

**Human intervention (reconstructed from PR #23, PR #30, and README tone fixes):**

- make the prose sound like Jonathan Mace / JSV, not like a novelty paper
- keep the humour, but only if it serves credibility

**AI response:**

- created style guides
- ran a Jonathan Mace editorial pass
- reframed the paper around coupling disparity and occupational relevance

**Consequence:** the project kept its personality without collapsing into parody.

### 4. "Resolve contradictions before a reviewer finds them"

**Human intervention (enabled through provocative review):**

- allow hostile internal critique to redirect the manuscript

**AI response:**

- provocateur flagged the Paper 1 / Paper 2 contradiction
- Paper 1 got a gas-pocket qualifier in PR #67

**Consequence:** the portfolio became more coherent than it would have been if
the human had simply pushed Paper 1 out the door.

### 5. "No, the policy matters"

**Human/publisher intervention:**

- Copilot cannot remain a co-author under Elsevier policy

**AI response:**

- PR #116 demoted Copilot to acknowledgements across papers
- later Reviewer A wit audit calibrated how that demotion should be written

**Consequence:** the human overrode an AI-generated joke-institution with a
real-world publishing constraint.

### 6. "If you are going to mention South Park, cite it properly"

**Human/policy intervention:**

- non-scientific references must be exact, sourceable, and defensible

**AI response:**

- created `pop-culture-verifier`
- added R9
- inserted exact South Park and MythBusters references

**Consequence:** the project learned that even the jokes need provenance.

---

## Moments where the AI took initiative

Several consequential moves appear to have been primarily AI-initiated.

1. **The lab metaphor became literal.**  
   The AI did not stop at helpers. It created specialist agents, rituals, and
   management roles.

2. **The project expanded from one paper to five.**  
   The initial prompt did not require a bladder paper or a borborygmi paper.
   Those emerged because the AI kept asking what else the framework could explain.

3. **The AI wrote the first retrospective.**  
   Commit `c826209` is the strongest evidence of autonomous initiative in the
   whole repository.

4. **The AI created anti-perfectionism roles.**  
   Coffee-machine-guru and loving-spouse sound comic, but they encode a serious
   insight: autonomous research systems need meta-level interruption, not just
   technical critique.

5. **The AI converted workflow into portable infrastructure.**  
   The move from ad hoc instructions to shared skills is a classic institutional
   response: once a behaviour works, make it reusable.

Not all of these initiatives were equally good. But many survived. That is the
important part. The AI was not merely generating disposable suggestions; it was
generating institutional features that the human kept.

---

## Moments where human judgment overrode the AI

The repository is equally clear that autonomy did not mean sovereignty.

### Authorship

The early paper state included Copilot and even Springbank 10 in the author
line. Later history moved both toward acknowledgements. Reviewer and policy
pressure won over the AI's fondness for theatrical author metadata.

### Tone

The repeated README intro rewrites, the Jonathan-Mace style pass, the provocateur
reframe, and the later wit audit all point to the same underlying human role:
Jonathan kept deciding where the line between memorable and unserious lay.

### Submission timing

The AI system could endlessly generate another pass. What finally stopped it was
not a theorem. It was judgment. The strongest meta-advice in the logs is not
technical:

> "Submit now. Seven rounds is enough."

That is not something a metric can decide. It is a human problem, even when an
AI agent is the one saying it.

### Policy and credibility

The late addition of R0, the pop-culture rule, and the author-demotion PR all
show the human imposing external-world constraints that the AI would not have
prioritised on its own.

---

## Emergent behaviours neither side explicitly planned

Several behaviours seem genuinely emergent rather than directly specified.

### 1. Git became a scientific instrument

The project's scientific claims were inseparable from its git structure. PRs
tracked numerical corrections, review rounds, and even framing decisions.
The repository did not merely store the science; it became the mechanism by
which the science was stabilised.

### 2. Reviewers became more important than authors

The first drafts were often fast and wrong. The quality came from the loop:

**write -> review -> fix -> review**

In practice, Browntone's intellectual engine was less "AI authoring" than
"AI review orchestration".

### 3. The lab developed a calendar

The semester-break skill is absurd on the surface and deeply sensible in
practice. Once multiple agents were running in parallel, time management itself
had to be ritualised.

### 4. Infrastructure generated science

The existence of a strong review and analysis pipeline directly produced new
papers. That is an important inversion. Usually infrastructure supports science.
Here, infrastructure also *caused* science by making adjacent questions cheap.

### 5. The project became self-aware

A lab that writes a retrospective on its own working method while still inside
the first burst of production is doing something unusual. Browntone did not just
produce results. It recursively studied its own method.

---

## What the human actually contributed

The repository history is remarkably consistent on this point.

Jonathan's role was not typing bulk text. It was:

- setting the initial direction
- giving unusually broad permission
- recognising which outputs were interesting
- insisting on seriousness when the tone drifted
- imposing real-world constraints: venue, policy, credibility, submission
- deciding when to accept, when to redirect, and when to stop polishing

Put differently: the human supplied **taste, restraint, and stakes**.

The human was also the only participant who could decide that a result was worth
being a paper rather than a curiosity. The AI could propose five adjacent
projects; only the human could decide that this was a portfolio rather than a
hallucinated empire.

---

## What the AI actually contributed

The AI's contributions were not mystical. They were operational, but on a scale
that changed the shape of the project:

- repository scaffolding
- literature triage
- code generation
- manuscript drafting
- figure generation
- test expansion
- review simulation
- PR management
- cross-paper consistency checking
- idea generation for adjacent papers
- persistence at clerical tasks humans usually defer

The AI was particularly strong at the parts of research that are essential,
time-consuming, and only occasionally glamorous: assembling references, updating
tables, checking consistency, rewriting boilerplate, re-running the same review
loop, and opening yet another branch because a reviewer found yet another stale
parameter.

That changed the economics of the project. New directions became cheap enough to
explore before they were fully justified.

---

## Lessons from the collaboration

### 1. Broad creative licence works only if scepticism is institutionalised

The opening permissiveness was productive because the project also created
Reviewer B, audits, tests, and logs. Freedom without attack would have produced
a plausible nonsense paper.

### 2. First-draft quality mattered less than correction speed

Browntone succeeded not because the AI got things right immediately, but because
it could be corrected quickly and repeatedly, with a full audit trail.

### 3. Human taste is most visible in framing, not derivation

The most consequential human interventions were about narrative, seriousness,
policy, and submission timing, not about implementing a specific function.

### 4. Autonomous research needs bureaucracy

This sounds depressing, but the repository says it clearly. The agents only
became reliable once the lab had rules, rituals, roles, and review gates.

### 5. Humour was useful, but only when controlled

The topic's absurdity helped sustain momentum. But the project repeatedly had to
convert humour into disciplined deadpan rather than indulgent cleverness.

### 6. AI is unusually good at expanding a research neighbourhood

Once a shell model existed, the AI kept identifying nearby publishable
questions. That suggests a real use for human-AI collaboration: not just faster
execution of one plan, but lower-cost exploration of adjacent plans.

### 7. Submission is a human-AI coordination problem

Left alone, the system could have revised forever. The repo history repeatedly
shows the need for a final act of will: enough review, enough polish, submit.

---

## Statistics and trajectory

### Current repository-scale statistics

| Metric | Current evidence |
|--------|------------------|
| Commits | **277** |
| Merged PRs | **116** |
| Research-log files | **59** |
| Agent definitions | **17** |
| Passing tests | **199/199** |

### Test-suite growth

| Stage | Evidence |
|------|----------|
| Early merged PR #3 | **97 tests** |
| Integration v3 (2026-03-26T2300) | **118 tests** |
| Multi-paper expansion (2026-03-27T0930) | **153 tests** |
| Final polish log (2026-03-27T2200) | **183 tests** |
| Pop-culture audit (2026-03-28T2230) | **198 tests** |
| Current baseline | **199 tests** |

### Page-count trajectory recorded in logs

| Paper / stage | Evidence |
|--------------|----------|
| Paper 1, style pass | **25 pp** |
| Paper 1, integration v3 | **31 pp** |
| Paper 1, submission sprint | **37 pp** |
| Paper 1, later polish log | **44 pp** |
| Paper 2 current compile log | **16 pp** |
| Paper 3 current compile log | **11 pp** |
| Paper 4 current compile log | **27 pp** |
| Paper 5 current compile log | **18 pp** |

The Paper 1 page count is not monotone in the artefacts because different logs
reflect different formatting states and later edits. That inconsistency is
itself informative: even the manuscript metadata remained in motion as the lab
kept revising.

### Review-cycle summary

| Paper | Internal review pattern visible in repo |
|------|------------------------------------------|
| Paper 1 | **7 rounds** from Reviewer B REJECT to unanimous ACCEPT |
| Paper 2 | at least **3 B-led rounds** plus Reviewer C verification; later marked ACCEPT |
| Paper 3 | initial A/B review plus **multiple same-day repair PRs**; still under revision |
| Paper 4 | A Round 1, B Round 1, targeted analytic fixes |
| Paper 5 | model/test build-out, paper draft, later packaging and tone audit |

---

## Final reflection

The repository history does not support the lazy story that AI replaced the
human researcher. It supports a more interesting one.

The human made the project worth doing, kept it recognisable as science, and
imposed the standards by which it had to survive. The AI made the project large
enough, fast enough, and persistent enough to become something more than a
single amusing manuscript.

The deepest pattern in Browntone is this:

- the human gave permission
- the AI overproduced
- review agents broke the overproduction
- rules were written to prevent the same failure twice
- the resulting infrastructure enabled still more production

That is not human replacement. It is a new division of labour.

If I had to compress the whole history into one sentence, it would be this:

**Jonathan supplied taste, scepticism, and stopping rules; Opus supplied scale,
memory, and the willingness to turn every solved problem into a small research
institution.**

And yes: the coffee-machine-guru was right. The project repeatedly improved when
someone — human or agent — insisted on the same unfashionable academic virtue:

**submit the damn paper.**
