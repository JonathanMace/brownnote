---
name: mace-writing-style
description: >
  Writing style guide based on Brian Mace's published works.
  Use when drafting or editing text to match Brian's voice.
---

# Mace Academic Writing Style

Apply this style guide when drafting or revising academic papers targeting the Journal of Sound and Vibration (JSV) or similar structural dynamics venues. The guide replicates the voice and conventions of Professor Brian R. Mace (University of Auckland / ISVR Southampton).

## Core Voice Principles

1. **Impersonal and passive-dominant.** Default to passive voice (~70%). The subject of sentences should be the method, the structure, or the result — not the authors.
2. **Measured and precise.** Never overstate. Use hedging where appropriate: "generally", "typically", "is likely to", "can become large". Avoid superlatives.
3. **British English.** Use: behaviour, modelling, analysed, discretised, programme, metre, colour.
4. **Formal register throughout.** No colloquialisms, no rhetorical questions, no humour.

## Sentence Patterns

### Do Use
- "A method is presented by which…"
- "X is considered in this section."
- "It is seen that…" / "It can be seen that…"
- "It can be shown that…"
- "The results show that…" / "The method is seen to yield…"
- "It should be noted that…" / "It is worth noting that…"
- "This arises because…" / "This is attributable to…"
- "Numerical examples are presented to illustrate the approach."
- "…such that the numerical errors are reduced."
- "…the accuracy and validity of the results are evaluated."
- "Some conclusions are drawn."

### Don't Use
- "We propose…" / "We introduce…" / "Our method…"
- "Clearly…" / "Obviously…" / "Importantly…"
- "Novel" / "Groundbreaking" / "For the first time"
- "It is important to note…" → use "It should be noted that…"
- "This is a significant/major improvement" → "Significant [X] reduction is observed"
- Contractions (don't, isn't, we've)
- First person except sparingly in conference papers

## Section-by-Section Guide

### Abstract (150–250 words, single paragraph)
1. **Context sentence:** State the class of problem.
2. **Method (2–3 sentences):** Describe the approach.
3. **Application:** Specify what structures/cases are considered.
4. **Key result (1–2 sentences):** Start with "It is seen that…" or "The method is seen to yield…"

### Introduction
1. **General context** (1–2 sentences): The broad problem area.
2. **Specific challenge** (2–3 sentences): What makes this non-trivial.
3. **Literature review** (1–3 paragraphs): Grouped thematically, descriptive tone, author surnames cited with square-bracket numbers.
4. **Gap identification** (1–2 sentences): What remains unaddressed.
5. **This paper's contribution** (1–2 sentences): "The aim of this paper is (1) to… and (2) to…"
6. **Outline paragraph:** "First, X is described. Then… Numerical examples are presented. Finally some conclusions are drawn."

### Theory/Method Sections
- Open each subsection with an orienting sentence: "In this section, a brief overview of X is given."
- Introduce equations with a statement of what is being expressed.
- Define all variables in a "where…" clause immediately after the equation.
- Cross-reference equations in lowercase: "equation (2.1)"
- State assumptions explicitly: "No damping is assumed." / "Throughout this report, time harmonic motion e^{jωt} is implicit."
- Use numbered enumeration for multi-part aims or error categories.

### Results Sections
- Open with: "X is considered in this section. No damping is assumed."
- Introduce figures before discussing them: "The dispersion relationships are shown in Figures 5.3."
- Describe results factually: "The WFE results generally agree well with the analytical solution."
- Quantify discrepancies: "Some discrepancies can be seen for higher wave modes as the FE discretisation errors increase."
- Qualify observations: "The relative error is generally larger than that in the eigenvalues."
- Use "it can be seen that…" when pointing to a figure.
- State trade-offs honestly: "a crude trade-off between the conditioning, the FE discretisation error and the round-off error."

### Conclusions
1. Restate the method/problem: "In this paper, X has been described/discussed."
2. Summarise findings in the order they appeared.
3. Note practical implications and trade-offs.
4. Use measured language: "seem appropriate approaches" not "are the best approaches."
5. Avoid self-congratulation and excessive future-work speculation.

## Equation Presentation

```
[Introductory sentence ending naturally or with colon]

    [equation]    (N.M)

where [symbol] is [definition], [symbol] is [definition], and [symbol] represents [definition].
```

- Number equations with section-based decimals: (2.1), (3.14), (5.7).
- Refer to equations in text as "equation (2.1)" (lowercase).
- After the equation: define symbols → state assumptions → describe manipulation → point to result.
- "Substituting equation (X) into equation (Y) gives…"

## Figure and Table References

- Capitalise "Figure" when used as a noun: "Figure 3 shows…" / "…as shown in Figure 3."
- Introduce before discussing: "The relative error is shown in Figure 5.9."
- Describe observations: "From the figure, the relationships between γ and κ are roughly estimated as…"
- Caption style: concise, one sentence, include line-style legend if applicable.

## Literature Citations

- Use numbered references: [1], [2,3], [5–7].
- Cite with author surnames in running text: "Thompson [9] applied the method to…"
- Group references thematically, not chronologically.
- Describe prior work neutrally: note what was done, not whether it was good or bad.
- Identify gaps through absence, not criticism: "However, most papers do not discuss many details."

## Vocabulary Quick-Reference

| Instead of | Use |
|---|---|
| important | of concern |
| study / investigate | consider / analyse |
| show | it is seen that |
| explain | describe |
| big / large errors | errors can become large |
| propose | present |
| introduce | describe / consider |
| very good agreement | good / generally good agreement |
| validate | evaluate the accuracy and validity of |
| better / improved | reduced (for errors), improved (for conditioning) |
| use (casual) | employ / utilise |
| behavior | behaviour |
| modeling | modelling |

## Self-Review Checklist

Before submitting a draft, verify:

- [ ] **Voice:** ≥70% passive voice; "we" used sparingly or not at all
- [ ] **Spelling:** British English throughout (behaviour, modelling, analysed, etc.)
- [ ] **Hedging:** Claims are appropriately qualified (generally, typically, is likely to)
- [ ] **No superlatives:** No "novel", "groundbreaking", "dramatically improved"
- [ ] **Equations:** Each equation is introduced, numbered, and followed by variable definitions
- [ ] **Figures:** Each figure is introduced by sentence before discussion; "Figure" capitalised
- [ ] **Abstract:** Follows context → method → application → key result structure
- [ ] **Introduction:** Ends with explicit outline paragraph
- [ ] **Conclusions:** Mirror paper structure; use measured language
- [ ] **References:** Numbered, square brackets, author surnames in running text
- [ ] **Section openings:** Each section/subsection opens with an orienting sentence
- [ ] **Transitions:** Use "However,", "In addition,", "Moreover,", "Next,", "Finally,"
- [ ] **Formality:** No contractions, no colloquialisms, no rhetorical questions
- [ ] **Precision:** Quantitative comparisons include factors, orders of magnitude, or percentages
- [ ] **Tone:** Authoritative through thoroughness, not through assertion

## Example Transformations

**Draft:** "We developed a new method that works much better than existing approaches for analyzing wave propagation in beams."

**Mace style:** "A method is presented for the analysis of wave propagation in beams. The method is based on… and is seen to yield improved accuracy compared to existing approaches."

---

**Draft:** "Figure 2 clearly shows that our results are very accurate."

**Mace style:** "The results are shown in Figure 2. It can be seen that the method yields accurate results, with relative errors typically less than 1%."

---

**Draft:** "We found that the errors blow up when the mesh is too coarse."

**Mace style:** "The errors can become large when the element length becomes large compared to the wavelength."

---

**Draft:** "In conclusion, we have successfully demonstrated a powerful new technique."

**Mace style:** "In this paper, a technique for X has been described. The accuracy and validity of the approach have been evaluated. The method seems an appropriate approach for general structures."
