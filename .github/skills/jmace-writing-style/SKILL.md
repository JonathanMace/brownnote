---
name: jmace-writing-style
description: >
  Writing style guide based on Jonathan Mace's published works.
  Use when drafting or editing text to match Jonathan's voice.
license: MIT
---

# Jonathan Mace Academic Writing Style

Apply this style guide when drafting or revising academic papers targeting top systems venues (SOSP, SIGCOMM, OSDI, NSDI, SoCC, EuroSys) or when writing in the voice of Jonathan Mace. The guide replicates the voice and conventions observed across his published work from 2014–2025.

## Core Voice Principles

1. **Active voice dominant (~70%).** Use "we" freely for author actions, claims, and contributions. Reserve passive for describing system behavior or established facts.
2. **Direct and confident.** Make claims clearly. Say "we show that" not "it is seen that." Be honest about limitations but do not hedge unnecessarily.
3. **American English.** Use: behavior, modeling, analyzed, program, meter.
4. **Professional but accessible.** Formal register overall, but allow occasional informality — em dashes for asides, natural phrasing, concrete examples.
5. **Problem-driven.** Always ground technical work in real-world systems, real incidents, and practical impact.

## Sentence Patterns

### Do Use
- "In this paper, we present X, which..."
- "We find that..."  / "We show that..."
- "Our evaluation shows that..."
- "However, X is not straightforward and we face several challenges."
- "To address these challenges we present X..."
- "The contributions of this paper are as follows:"
- "The goal of X is to..."
- "This occurs because..." / "This is problematic because..."
- "The rest of this paper proceeds as follows."
- "Consider X, which..." (to introduce a concrete example)

### Don't Use
- "It is seen that..." / "It can be seen that..." (too passive — use Brian Mace's style only for acoustics)
- "A method is presented by which..." (too impersonal)
- "It should be noted that..." (prefer direct statement)
- "The method is described." (prefer "We describe the method.")
- "Novel" in isolation without evidence — prefer "We introduce" or "We present"
- Excessive hedging: don't say "generally" or "typically" unless the qualifier is necessary

## Section-by-Section Guide

### Abstract (150–250 words, single paragraph)
1. **Problem context** (1–2 sentences): The domain and specific challenge.
2. **System introduction** (1–2 sentences): "This paper presents X, which..."
3. **Key design/approach** (1–2 sentences): What makes the approach work.
4. **Concrete result** (1–2 sentences): Specific numbers, scale, or improvement factors.

### Introduction
1. **Broad context** (1–2 sentences): Why this domain matters.
2. **Concrete examples** (2–4 sentences): Name real systems, real incidents, real scale.
3. **Core challenge** (2–3 sentences): Why existing approaches fall short.
4. **This paper** (1–2 sentences): "In this paper, we present X..." with the system name.
5. **Contribution list** (bulleted): Specific, quantified claims. Each bullet is a self-contained claim.
6. **Outline** (1 paragraph): "The rest of this paper proceeds as follows. We discuss X in §2..."

### Design/Architecture Sections
- Open with the system's goal: "The goal of X is to..."
- Provide intuition before formalism: explain *why* before *how*.
- Use concrete examples to illustrate abstract concepts.
- Name components and give them clear roles.
- Use subsections liberally — one concept per subsection.

### Evaluation Sections
- Open with scope and claims: "In this section we evaluate X's ability to..."
- List specific properties to demonstrate (as bullets).
- Describe experimental setup: machines, configurations, baselines.
- Present results per-claim, each with a dedicated subsection.
- Use bulleted summaries of findings before detailed discussion.
- Quantify everything: "reduces by 2 orders of magnitude", "improves by up to 198×".

### Discussion / Limitations
- Be forthright: "While X improves Y, it cannot improve Z when..."
- Discuss alternative approaches honestly.
- Identify open questions: "It is an open question whether..."
- Note practical implications and trade-offs.

### Conclusion (short, 1 paragraph)
1. Restate what was presented: "In this paper we presented X, which..."
2. Summarize the key finding or contribution.
3. (Optional) Note broader impact or open questions.
4. Keep it brief — 4–6 sentences.

## Figure and Table References

- Use "Figure X" capitalised when used as a noun: "Figure 5 plots..."
- Integrate figure references with discussion: "Figure 8a shows that the service provided by WFQ has large-scale oscillations."
- Describe what the figure shows with quantitative specifics.
- Caption style: descriptive, can be 2–3 sentences, should explain what each element represents.

## Literature Citations

- Use numbered references: [1], [2, 3], [5–7].
- Cite in running text: "Google's Dapper [31]", "prior work [17]".
- Group references thematically and describe what each addresses.
- When identifying gaps, describe what existing work does then explain the limitation: "While X addresses Y, it does not handle Z."
- Be fair to prior work — acknowledge strengths before noting limitations.

## System and Approach Naming

- Give systems a **memorable single-word name**: Canopy, Sifter, Retro, Wasabi, Blueprint.
- Introduce the name prominently: "we present Two-Dimensional Fair Queuing (2DFQ)".
- Use the name consistently after introduction — never revert to generic descriptors.
- Acronyms are acceptable if the full name is unwieldy.

## Vocabulary Quick-Reference

| Instead of | Use |
|---|---|
| it is seen that | we find that / we show that |
| a method is presented | we present / we introduce |
| it should be noted | (state directly) |
| novel (unsupported) | new / we introduce |
| behaviour, modelling | behavior, modeling (American) |
| investigate | study / evaluate / examine |
| utilise | use |
| in the literature | in prior work |
| clearly (as filler) | (remove — let evidence speak) |
| dramatically | significantly / substantially |
| propose (for systems) | present / introduce |

## Characteristic Writing Moves

### The Problem–Challenge–Solution Pattern
1. State the problem concretely (with named systems)
2. Explain why it's hard (enumerate challenges as bullets)
3. Present the approach (with system name)
4. Explain why it works (intuition first, then details)

### The Honest Limitation
After presenting positive results, include a frank discussion:
> "While 2DFQ improves quality of service when the system is backlogged, work-conserving schedulers in general cannot improve service when the system is under-utilized."

### The Concrete Motivating Example
Before presenting technical content, walk through a real scenario:
> "Consider the HDFS NameNode process, which maintains metadata related to locations of blocks in HDFS. Users invoke various APIs on the NameNode to create, rename, or delete files..."

### The Evaluation Preview
Before detailed evaluation, summarize what will be shown:
> "Our evaluation shows that Sifter effectively biases towards anomalous and outlier executions, is robust to noisy and heterogeneous traces, is efficient and scalable, and adapts to changes in workloads over time."

## Self-Review Checklist

Before submitting a draft, verify:

- [ ] **Voice:** ≥70% active voice; "we" used freely for author actions
- [ ] **Spelling:** American English throughout (behavior, modeling, analyzed)
- [ ] **Claims:** Direct and quantified — no ungrounded "novel" or "clearly"
- [ ] **Concreteness:** Real systems named; real scale cited; real incidents referenced
- [ ] **Contributions:** Presented as bulleted list in introduction with specific claims
- [ ] **Evaluation:** Opens with scope, lists claims, includes quantitative results
- [ ] **Figures:** Integrated with discussion; "Figure" capitalised; observations quantified
- [ ] **Abstract:** Follows problem → system → approach → result structure
- [ ] **Introduction:** Ends with contribution list and outline paragraph
- [ ] **Conclusion:** Brief restatement; no self-congratulation
- [ ] **System named:** Approach has a memorable name, introduced early
- [ ] **Limitations:** Discussed honestly; alternative approaches acknowledged
- [ ] **References:** Numbered, square brackets, cited with context in running text
- [ ] **Transitions:** "However," for pivots; "First/Second/Finally" for sequences
- [ ] **Tone:** Confident but honest; pragmatic systems-builder voice

## Example Transformations

**Draft:** "We develop a novel method that dramatically outperforms all existing approaches for sampling distributed traces."

**Mace style:** "We present Sifter, a general-purpose trace sampler that automatically biases sampling decisions towards outlier and anomalous traces. Our evaluation shows that Sifter samples a more qualitatively interesting set of traces compared to alternative techniques."

---

**Draft:** "It is important to note that the results clearly show significant improvement."

**Mace style:** "We find that 2DFQ reduces the burstiness of service by 1–2 orders of magnitude on production workloads from Azure Storage."

---

**Draft:** "In this section, an overview of the scheduling problem is given."

**Mace style:** "The goal of Two-Dimensional Fair Queuing (2DFQ) is to produce smooth schedules for tenants with small requests, by minimizing burstiness over time and over space."

---

**Draft:** "In conclusion, we have successfully demonstrated a powerful new system."

**Mace style:** "In this paper we presented Canopy, which emphasizes a decoupled, customizable approach to instrumentation and analysis, allowing each to evolve independently."

---

## Blending with Brian Mace's Style

When writing a paper with both Jonathan and Brian Mace as co-authors (e.g., the brown note paper):

### Jonathan's Voice Should Dominate For:
- Abstract, introduction, and conclusion
- Experimental setup and results discussion
- Motivation and real-world grounding
- The overall paper structure and flow

### Brian's Conventions Should Apply For:
- Equation presentation (introduce → equation → "where" clause)
- Acoustic/vibration theory sections (passive voice, formal hedging)
- British English for acoustics terminology where venue requires it
- Measured qualification of physical results ("it is seen that", "generally")

### Blending Rules:
1. **Default to "we"** but switch to passive for established physics
2. **Use American English** except where acoustics conventions require British
3. **Provide intuition first** (Jonathan) then formal derivation (Brian)
4. **Problem-driven introduction** (Jonathan) with thematic lit review (Brian)
5. **Confident evaluation claims** (Jonathan) with honest qualification (Brian)
6. **Memorable system name** (Jonathan) for the experimental apparatus
7. **Explicit outline paragraph** (both agree on this)
