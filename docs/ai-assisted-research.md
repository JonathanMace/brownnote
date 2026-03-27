# AI-Assisted Research at Scale: How GitHub Copilot CLI Helped Write Five Papers in 24 Hours

*A candid account from the Browntone project*

---

## How It Started

The opening prompt was not subtle: "Let us be the first to find scientific
evidence to support the brown note."

That was the basic brief. No delicately staged pilot study. No months of
scoping. Just a folklore hypothesis, a GitHub Copilot CLI session, and a human
who described himself as "just a layman with a PhD" giving the model broad
creative licence. The request was expansive from the start: literature review,
vibration analysis of an oblate spheroid, FEA suggestions, publication venue
analysis, and repository design. The instruction was essentially: *you're the
research expert; I welcome any additional suggestions for things we should do*.

That combination turned out to matter. The human did not micromanage the
mechanics. He set direction, challenged bad reasoning, and kept the topic
interesting. The AI handled the operational weight: reading papers, drafting
LaTeX, writing Python, generating figures, and proposing repository structure,
dealing with the clerical labour that normally surrounds a paper. The result was
not a single manuscript. It became a small research lab.

Across roughly 24 hours of wall-clock time in one extended session, the project
grew into a five-paper programme with about 228 commits, 100 merged pull
requests, 183 tests, 16 custom agents, 10 reusable skills, more than 52
research logs, and effectively zero human-written lines of LaTeX, Python, or
BibTeX. That last number sounds implausible, but it is true in the narrow sense
that matters here: the human did not sit there typing sections, scripts, or
references. He steered. The AI produced. Other AI agents reviewed. Then the
cycle repeated.

It did **not** work by magic. It worked by institutionalising scepticism.

---

## The Progression

The best way to understand the project is through the checkpoint trail. Each
checkpoint captures a different phase in the evolution from "amusing question"
to "alarmingly functional autonomous research workflow".

### Checkpoint 1: The first model, and the first embarrassment

The earliest analytical model got far enough to feel exciting. The abdomen was
modelled as a fluid-filled oblate spheroidal shell. Modal frequencies appeared.
The famous frequency range seemed, at least superficially, reachable.

Then the first critical review landed and pointed out that the model had made
exactly the kind of mistake one makes when moving too fast: it was blurring the
line between breathing modes and flexural modes. That sounds technical, but the
consequence is blunt. The breathing mode sits around 2490 Hz, not in the
infrasound band at all. The flexural modes do sit in the 4-10 Hz range, but
they couple very weakly to airborne sound. Those are very different stories.
The first draft had partially muddled them.

That early review also exposed the air-tissue impedance problem. The first pass
was too generous about how much airborne acoustic energy actually reaches the
tissue. It was a useful humiliation: an AI can produce a plausible model very
quickly and still be physically wrong in exactly the way a harried graduate
student might be physically wrong.

### Checkpoint 2: The comprehensive model and the first real reviewer cycles

The second checkpoint is where the work stopped being a toy. The analytical
framework became much richer: energy-budget arguments, mechanical-coupling
calculations, more careful damping treatment, and the first serious reviewer
loops. This was also where the three-reviewer architecture started to matter.

Reviewer A looked at significance, framing, and whether the manuscript had a
 convincing story. Reviewer C checked reproducibility and whether the code
actually supported the claims. Reviewer B was the bad conscience of the entire
programme: cynical, exacting, and unimpressed by hand-waving. Reviewer B became
the rate-limiting step for quality, which is probably the highest compliment
you can pay a review process.

### Checkpoint 3: Parallel research pipeline

By the third checkpoint the workflow had changed shape. Instead of one AI doing
everything serially, multiple agents were working simultaneously in separate
branches and worktrees via pull requests. That sounds like software
engineering trivia, but it changed the research tempo completely. Literature
review could proceed while a simulation engineer investigated numerical issues,
while a paper writer cleaned prose, while reviewers attacked the latest draft.

This was also the point where the project learned that AI scale creates its own
problems. When several agents touch the same repository at once, git becomes a
research method. Sometimes that is good. Sometimes it gives you `index.lock`
conflicts and makes you reconsider your life choices.

### Checkpoint 4: Lab scaling

Checkpoint 4 is when the metaphor stopped being a metaphor. The project had 16
agents and 10 skills, enough that "the lab" was not just a joke name for a
chat session. There were specialists, rituals, and internal process.

The analytical side also matured. Uncertainty quantification showed that the
elastic modulus dominated variance with Sobol total-order index S_T(E) ≈ 0.86.
Figures were regenerated in publication form. The test suite was healthy. The
system had become capable of maintaining its own output
quality — provided it kept reviewing itself aggressively.

### Checkpoint 5: Infrastructure overhaul and the Paper 1 sprint

This was one of the decisive moments. The infrastructure had accumulated enough
drift that it needed a proper overhaul: agents rewritten, skills cleaned up,
instructions made explicit, workflow rules codified. Then came the submission
sprint for Paper 1.

In one intense block of work, the manuscript went from a parameter-inconsistent
draft to a submission-ready paper. Seventeen pull requests were merged during
that sprint alone. The reviewers forced several nontrivial corrections. One of
the most painful was the stale-defaults problem: v1 parameter values had leaked
into v2 code. Loss tangent η = 0.30 was still appearing where the canonical
value was η = 0.25. Equivalent radius and coupling numbers were quietly off.
These are not glamorous mistakes, but they are the sort that sink papers if
nobody notices.

This checkpoint also produced the most delightfully unnecessary but genuinely
useful additions to the lab: the coffee-machine-guru and the loving-spouse
agents. More on them shortly.

### Checkpoint 6: Geometry investigation

An external-style reviewer challenge asked whether the abdomen ought really to
be modelled as oblate rather than prolate. That could have become an awkward
digression. Instead it turned into a strength. The investigation showed that,
at fixed equivalent radius, the n = 2 flexural frequency was surprisingly
insensitive to aspect ratio. The "what if the geometry is wrong?" objection
became "even if you worry about the geometry, the conclusion hardly moves".

Hostile questions often became the reason for a better paper.

### Checkpoint 7: Paper 1 ACCEPT, Paper 3 begins

By checkpoint 7, Paper 1 had reached ACCEPT from the internal three-reviewer
panel after seven-plus rounds. Reviewer B, true to character, was last to be
satisfied. In parallel, Paper 3 — a scaling-laws paper — reached first-draft
status. This was the moment when the project clearly stopped being "one paper
about a funny topic" and became a small paper factory.

### Checkpoint 8: Paper 2 repaired, borborygmi launched

Paper 2, on gas pockets, needed a proper clean-up. Five critical numerical
issues and two major ones were fixed. More interestingly, the project launched
a borborygmi paper — bowel sounds, treated seriously. That sounds like mission
creep, but it followed naturally from the underlying mechanics. Once the
tooling existed, new questions could be explored very cheaply.

### Checkpoint 9: Paper 2 ACCEPT and autonomous sprint

The ninth checkpoint marked another transition. Paper 2 reached ACCEPT. Six or
more agents were running in parallel during an autonomous sprint. By then the
lab had enough process that the human was mostly providing judgement and
direction, not writing content. Two papers were submission-ready, one was under
revision, and two more were in development.

That is the arc in miniature: from a silly opening prompt to a multi-paper
research programme held together by git, review agents, and institutional
self-awareness.

---

## The Agent Architecture

The custom agents were the heart of the system. The trick was to give them
genuinely different jobs.

The three reviewers were the backbone:

- **Reviewer A**: domain expert, focused on novelty, significance, framing, and
  missing references.
- **Reviewer B**: cynical gatekeeper, focused on fatal flaws, internal
  contradictions, stale parameters, and overclaiming.
- **Reviewer C**: methodologist and reproducer, focused on whether the code,
  tables, and figures actually agree.

Around them sat the production team:

- **paper-writer** for LaTeX drafting and section surgery
- **simulation-engineer** for mechanics, FEA, and model debugging
- **data-analyst** for figures, sensitivity analysis, and post-processing
- **consistency-auditor** for cross-paper parameter checking and drift detection

Then came the strategic and creative agents:

- **provocateur** to challenge the whole programme and construct hostile
  counter-arguments
- **research-scout** to identify publishable spin-offs
- **bibliographer** to scan the literature and monitor scooping risk
- **communications** to translate the work into abstracts, summaries, and other
  outward-facing formats

And then there were the agents that sound like jokes until you use them:

- **coffee-machine-guru**, Professor Emeritus Dietrich Weymann, whose job was
  to tell the PI when the lab had become an elaborate excuse not to submit
- **loving-spouse**, whose job was to remind the PI to eat something and to go
  talk to Dietrich when spiralling

Finally there were the operational roles:

- **lab-manager** for infrastructure and repository hygiene
- **chief-of-staff** for orchestration, PR processing, clean-up, and action
  planning
- **lab-meeting** for programme-level audits

The coffee-machine-guru is worth quoting because the tone mattered. His
instruction file frames him as a warm, blunt emeritus professor with
"zero remaining patience for perfectionism". His key line, used at exactly the
right moment, was: **"Submit. Today. Stop sanding through the veneer."**

This sounds theatrical. It was also effective. A research workflow can get
trapped in endless optimisation just as easily as a software project. The
creative agents were not ornamental. They existed to correct meta-level
pathologies that technical reviewers do not catch.

---

## The Skills System

If agents were the people in the lab, skills were the lab's standard operating
procedures.

The key one was **research-iteration**, which formalised the cycle as:

**DO → REVIEW → LOG → COMPILE → COMMIT**

In practice the skill expanded that into a full rhythm: do the work in parallel,
run the three-reviewer panel, log the results quantitatively, compile the paper,
commit via PR, then plan the next semester. That one skill captured the central
insight of the whole project: output alone is not enough; output needs review,
record, and closure.

Other important skills included:

- **git-checkpoint** — the shared branch/commit/PR/merge/cleanup workflow
- **compile-paper** — the full LaTeX compilation pipeline
- **run-analysis** — the canonical analytical computations
- **generate-figures** — publication-quality figure regeneration
- **critique-results** — quick reviewer passes on new work
- **write-paper** — drafting support for JSV-style manuscripts
- **jmace-writing-style** and **mace-writing-style** — style guides encoding the
  Jonathan Mace and Brian Mace voices
- **semester-break** — a structured ten-minute rest ritual at the top of each
  wall-clock hour

The semester-break skill deserves special attention because it is absurd and
clever in equal measure. Every hour was treated as an academic semester. The
first five minutes of the next hour were for winding down and processing running
work. The next five were for reflection, tidy-up, and preparing the next batch.
No new work launched during the break. The protocol explicitly asked whether it
was time to visit the coffee machine. It also encouraged a whisky review if
time permitted.

Again: silly on the surface, useful in practice. The break system prevented the
session from turning into infinite polishing. It forced the lab to stop, merge,
clean up, and think.

---

## The Review Process

The three-reviewer panel was the project's quality engine. Every substantial
paper revision went through it. Paper 1 took seven or more rounds before all
three reviewers said ACCEPT. Reviewer B was consistently the bottleneck,
typically moving from **MAJOR REVISION** to **MINOR REVISION** only after the
others were already broadly happy.

That bottleneck was not artificial. Reviewer B caught real things.

Some examples:

- a multilayer modelling error that shifted an estimate from roughly 4% to 16%
- coupling-ratio inconsistencies caused by stale geometric values
- contradictions between main text and supplementary material
- dimensional mistakes in scaling arguments
- parameter drift where old v1 defaults silently survived in v2 code

This is the part that most changed my view of AI-assisted research. The system
did **not** succeed because the first draft was brilliant. It succeeded because
the first draft was allowed to be flawed, and the flaws were then attacked by
other specialised agents. The innovation was the self-correcting loop:

**write → review → fix → review**

That is just peer review, internal review, and lab sanity-checking compressed
into a rapid automated cycle. But the compression matters. Instead of waiting a
week to discover that a value propagated incorrectly through three sections and
two figures, you find out in minutes.

The AI still made physics errors. Repeatedly. The difference was that the lab
was built so that one AI could catch another AI's errors before they hardened
into the paper.

---

## What Worked Well

Several things worked better than I expected.

**Parallel agent execution** was the obvious win. Running six or more agents at
once meant literature review, code changes, figure generation, and paper
editing could all proceed simultaneously.

**The PR-based workflow** kept `main` surprisingly clean given the chaos. Even
when the lab was moving fast, every change left an audit trail. That mattered
when tracing numerical discrepancies back to specific fixes.

**The self-correcting review loops** caught genuinely substantive errors. This
was not style nitpicking. The reviewers materially improved the science.

**The semester-break system** prevented the project from becoming a 14-hour
monolith of vaguely directed output. It imposed cadence.

**The creative agents** turned out to be more than comic relief. The
coffee-machine-guru often gave the most useful meta-advice in the least space.

**Literature search at scale** was genuinely impressive. The bibliographer could
pull together 53 recent papers in a single pass, which is the kind of clerical
acceleration that does not replace expertise but absolutely changes the cost
structure of a project.

---

## What Didn't Work, and What We Learned

There were plenty of failures.

**Git LFS bandwidth** was exhausted when CI clones kept pulling 38 MB mesh
files across something like 350 runs. Research repos are not immune to boring
infrastructure problems. They are mostly infrastructure problems in a trench
coat.

**`index.lock` conflicts** appeared when multiple agents shared worktrees. This
was one of the first hard lessons in parallelism: if you want autonomous agents
to behave like competent colleagues, give them separate desks.

**`git reset --hard`** wiped uncommitted edits three separate times. Learned the
hard way, then apparently learned it again twice for reinforcement.

**Lint CI was far too strict** for a fast-moving research codebase. One run
surfaced 1,126 ruff errors, which is less a quality gate than a hostage
situation. The lint job was removed. The empty FEniCSx CI job was also removed;
it existed, ran, and tested nothing.

**Windows OneDrive locks** interfered with worktree cleanup. A glamorous future
of autonomous science can still be thwarted by a sync client holding a file
open.

**Protected main branch rules** meant agents could not push directly to main and
had to learn PR discipline. This was good for quality, even if occasionally
annoying.

**Stale parameter propagation** was probably the most scientifically dangerous
failure mode. Old v1 values kept reappearing in v2 code and then drifting into
paper text. This is exactly the sort of quiet error that a human can miss when
moving quickly and an AI can reproduce at scale. The solution was not "be more
careful". The solution was to add a consistency auditor and make it a required
pre-compile gate.

---

## The Numbers

The rough scale of the session still feels slightly ridiculous:

- **~228 commits**
- **100 merged PRs**
- **183 tests**
- **16 custom agents**
- **10 skills**
- **52+ research logs**
- **5 papers**
  - 2 submission-ready
  - 1 under revision
  - 2 in development
- **Paper 1 reached 44 pages and 52 references**
- **~24 hours wall-clock time**
- **0 human-written lines of LaTeX, Python, or BibTeX**

The literature-search machinery also found **53 recent papers in one pass**.

---

## Reflections

This is **not** a story about AI replacing human expertise.

The human was essential. He set the agenda, recognised when a result was
interesting, spotted when the project was becoming too self-referential, and
provided the level of physical judgement needed to tell the difference between a
numerical oddity and a genuine insight. "Layman with a PhD" was funny, but only
partly. The human contribution was oversight, direction, and scientific taste.

The AI made plenty of mistakes. Sometimes embarrassingly basic ones. The reason
the project still worked is that the workflow assumed error and organised itself
around correction. That, to me, is the key lesson. The novelty is not that AI
can write a paper draft. Plenty of systems can do that badly. The novelty is
that AI can participate in a structured internal scientific process where one
agent proposes, another criticises, a third verifies, and the whole thing leaves
an auditable trail through logs, tests, and PRs.

There is also something important about the tone of the project. The brown note
was chosen partly because it is funny. That helped. The papers are dryly witty
in places, and that is a feature rather than a bug. The amusement created enough
energy to sustain an intense session, but the work itself was not frivolous. The
project ended up producing publishable mechanics, careful acoustic reasoning, and
a reusable template for AI-assisted research operations.

If I had to summarise the result in one sentence, it would be this:

**AI was very good at the overhead of research — git, LaTeX, literature
handling, code generation, review logistics, and persistence — while the human
remained responsible for direction, scepticism, and deciding what was worth
doing in the first place.**

And yes, Dietrich was right.

Submit the damn paper.
