# Writing Style Analysis: Professor Brian R. Mace

**Subject:** Emeritus Professor Brian R. Mace, University of Auckland (formerly ISVR, University of Southampton)
**Fields:** Structural dynamics, vibro-acoustics, wave propagation, statistical energy analysis
**Target venue:** Journal of Sound and Vibration (JSV)
**Sources analysed:**
- ISVR Technical Memorandum No. 922 (2003): "Finite Element Analysis of the Vibrations of Waveguides and Periodic Structures" — Duhamel, Mace & Brennan
- ISVR Technical Memorandum No. 928 (2004): "Wave Propagation, Reflection and Transmission in Non-Uniform One-Dimensional Structural Waveguides" — Lee, Mace & Brennan
- ISVR Technical Memorandum No. 964 (2006): "On Numerical Issues for the Wave/Finite Element Method" — Waki, Mace & Brennan
- Eurodyn 2011 conference paper: "Vibration Modelling of Waveguide Structures using the Wave and Finite Element Method" — Renno & Mace
- Conference abstract (ICSVS 1997): "Energy Flow and S.E.A. at Low Modal Overlap" — Mace
- Multiple JSV abstracts and publication metadata from ORCID, Google Scholar, and institutional repositories

---

## 1. Sentence Structure

### Average Length and Complexity
Mace writes in **medium-to-long sentences** (typically 20–35 words), with a clear preference for compound sentences joined by commas or semicolons. Short declarative sentences are used sparingly, usually to introduce a new topic or to deliver a key conclusion.

**Characteristic pattern:** A main clause stating what is done or found, followed by one or two subordinate clauses providing qualification or detail.

> "The method involves postprocessing a conventional, but low order, FE model, the mass and stiffness matrices of which are typically found using a conventional FE package."

> "The method involves the reformulation of the dynamic stiffness matrix, which includes the mass and stiffness matrices of a section of the structure, into the transfer matrix."

> "Structural wave motion is expressed in terms of the eigenvalues and the eigenvectors of this matrix and these represent the wavenumbers and the wave modes respectively."

### Subordinate Clause Usage
- **Relative clauses** (introduced by "which", "where", "such that") are frequent and serve to add precision inline rather than in separate sentences.
- **Conditional clauses** ("When…", "If…", "For the case where…") are used to specify the conditions under which a statement holds.
- **Purpose clauses** ("such that", "so that", "in order to") are used to explain the rationale for methodological choices.

### Enumeration
Mace uses inline numbered lists for methodological aims or error categories:
> "The aim of this report is (1) to identify and quantify the potential numerical problems and (2) to suggest alternative ways of determining the wave properties of a structure such that the numerical errors are reduced."

> "numerical errors arise because of (1) the FE discretisation error, (2) round-off errors due to the inertia term and (3) ill-conditioning."

---

## 2. Voice and Person

### Active vs. Passive Ratio
The writing is **predominantly passive** (~70–75% passive constructions), which is standard for JSV and structural dynamics literature. However, active voice appears regularly, especially when:
- Describing what the paper/report does: "This report concerns…", "The method starts from…"
- Introducing numerical procedures: "We use…", "One can show…"

### Use of "We" vs. Impersonal
- **Impersonal constructions dominate.** The default subject is the method, the matrix, the result, or the structure — not the authors.
- **"We" is rare** in the technical memoranda. When it appears, it tends to be in conference papers.
- **Common impersonal subjects:** "The method", "The results", "The transfer matrix", "The approach", "It is seen that…", "It can be shown that…"

### Characteristic Passive Constructions
> "A periodicity condition is applied, the wavenumbers following from the eigensolution of the resulting transfer matrix."

> "The quasi-longitudinal waves in a rod are considered in this section."

> "No damping is assumed."

> "The accuracy of results calculated by the WFE method is discussed in this section."

---

## 3. Paragraph and Section Structure

### Section Openings
Each section and subsection typically begins with a **brief orienting sentence** that states what will be covered:
> "In this section, a brief overview of the WFE formulation is given."

> "The quasi-longitudinal waves in a rod and flexural waves in a beam are considered."

> "For two-dimensional structures, the conditioned eigenvalue problem should be applied to improve ill-conditioning occurring in the transfer matrix approach."

### Transitions Between Ideas
Transitions are **understated and logical** rather than rhetorical. Common patterns:
- **Sequential:** "First…", "Next…", "Finally…"
- **Contrastive:** "However,…", "On the other hand,…", "In contrast to…"
- **Consequential:** "such that…", "so that…", "Therefore…"
- **Additive:** "In addition,…", "Moreover,…", "Furthermore,…"

### Paragraph Length
Paragraphs are **medium-length** (3–6 sentences typically). Each paragraph usually contains:
1. A topic sentence
2. Technical detail or derivation context
3. A concluding qualification or forward reference

---

## 4. Technical Prose and Equation Presentation

### Introducing Equations
Mace introduces equations with a **statement of what is being expressed**, followed by the equation, followed by **variable definitions immediately after**:

> "The equation of motion for uniform structural waveguides can be expressed as
>
> Mq̈ + Cq̇ + Kq = f     (2.1)
>
> where M, K, and C are the mass, stiffness and damping matrices respectively, f represents the loading vector and q is the vector of the nodal displacement degrees of freedom (DOFs)."

**Key patterns:**
- The phrase preceding an equation typically ends with a colon or flows naturally into it
- Variables are defined in a "where…" clause immediately following the equation
- Cross-references use "equation (X.Y)" in lowercase
- Equations are numbered sequentially within sections (e.g., 2.1, 2.2, 5.7)

### After Equations
After presenting an equation, Mace typically:
1. Defines all symbols
2. States any assumptions or simplifications
3. Describes what happens when you substitute or manipulate the equation
4. Points forward to the result or next step

> "Throughout this report, time harmonic motion e^{jωt} is implicit. Equation (2.1) then becomes…"

### Describing Results
Results are described with **factual precision** and referenced to specific figures:
> "The dispersion relationship is shown in Figures 5.3."

> "The WFE results generally agree well with the analytical solution. Some discrepancies can be seen for higher wave modes and for large kₓLᵧ/π as the FE discretisation errors (and the round-off error due to the inertia term at low frequencies) increase."

> "It can be seen that the relative error associated with the SVD approach is generally smaller especially at low frequencies and around the cut-off frequency."

---

## 5. Tone

### Formal vs. Conversational
The tone is **consistently formal and measured**. There is no conversational language, no first-person anecdotes, and no rhetorical questions. The writing conveys authority through precision rather than assertion.

### Hedging and Qualification
Mace uses hedging judiciously — not excessively, but enough to maintain scientific rigour:
- "might be", "may be", "is likely to"
- "generally", "typically", "usually"
- "can become large", "seem appropriate"
- "roughly estimated as"

> "the eigenvectors are likely to be less accurate than the eigenvalues such that the finite difference method is typically more accurate"

> "the power and energy relationship and the finite difference method seem appropriate approaches specifically for general structures"

### No Humour or Personality
The writing is **strictly impersonal and objective**. There are no asides, no colloquialisms, and no attempts at wit. The personality comes through in the **methodical thoroughness** and **systematic approach** to problem-solving.

---

## 6. Vocabulary Patterns

### Characteristic Technical Phrases
- "is of concern" (rather than "is important" or "matters")
- "is considered" (as an opening for a new section topic)
- "it is seen that…" / "it can be seen that…" (for results observation)
- "it can be shown that…" (for derivations)
- "the accuracy is evaluated" / "the validity has been investigated"
- "numerical examples are presented"
- "the method is described"
- "some conclusions are drawn"
- "the forced response can be calculated using the wave approach"
- "the full power of existing element libraries can be employed"

### Hedging Language
- "might be" (preferred over "may be" for possibility)
- "can be" (for capability/possibility)
- "is likely to" (for probabilistic statements)
- "generally", "typically" (for qualified generalisations)
- "roughly estimated as" (for approximate quantification)
- "a crude trade-off" (refreshingly honest qualification)

### Emphasis Strategies
Emphasis is achieved through:
- **Adverbs of degree:** "specifically", "especially", "significantly", "particularly"
- **Contrastive structure:** "However,…" followed by the point of emphasis
- **Explicit comparison:** stating what is better/worse and by how much
- Not through exclamation marks, bold text, or superlatives

### British English
Mace uses **British English spelling** throughout:
- "behaviour" (not "behavior")
- "modelling" (not "modeling")
- "analysed" (not "analyzed")
- "discretised" (not "discretized")
- "metre" in some contexts
- "programme" (not "program" for research context)

---

## 7. Figure and Table References

### Introducing Figures
Figures are introduced with **simple declarative sentences** that state what is shown:
> "The dispersion relationships are shown in Figures 5.3."

> "Figure 4.8 shows the relative error in the various estimates of the group velocity."

> "The condition numbers as a function of the area of an element are shown in Figure 5.6."

### Discussing Figures
After introduction, figures are discussed with specific observations:
> "From the figure, the relationships between γ and κ are roughly estimated as…"

> "In the figure, only the imaginary part is plotted for clarity."

> "The result is shown in Figure 5.17. The relative error for the 1st order approximation is poor at high frequencies and becomes about 1% at Ω = 110⁻¹."

### Figure Captions
Captions are **concise and descriptive**, typically one sentence with line-style legend:
> "Figure 4.4: Relative errors in the propagation wavenumber for ― the conditioned eigenvalue problem (3.9), – – the transfer matrix approach (2.15), ····· asymptote ±40dB/decade."

---

## 8. Introduction Style

### Problem Motivation
Introductions follow a **tight funnel structure**:
1. **General context** (1–2 sentences): The broad class of problem
2. **Specific challenge** (2–3 sentences): What makes this problem non-trivial
3. **Literature overview** (paragraph): What others have done, chronologically or thematically grouped
4. **Gap identification** (1–2 sentences): What remains unaddressed
5. **This paper's contribution** (1–2 sentences): What is presented here

> "The waveguide finite element (WFE) method is a useful method when the dynamic behaviour of a uniform structure is of concern. The method involves the reformulation of the dynamic stiffness matrix… However, several numerical difficulties arise when the problem is reformulated from a conventional finite element (FE) model. The aim of this report is (1) to identify and quantify the potential numerical problems and (2) to suggest alternative ways of determining the wave properties of a structure such that the numerical errors are reduced."

### Literature Review Style
- References are cited by number in square brackets: [1,2,3] or [5,6,7]
- The review is **grouped thematically** (e.g., early work, railway applications, WFE extensions)
- Each group gets 2–3 sentences with author surnames and brief methodological notes
- The tone is **descriptive, not evaluative** — Mace rarely criticises prior work directly; instead, he notes limitations as motivation for the current work

> "Thompson [9] and Gry et al [10,11] applied the method to analyse railway vibration, and Houillon et al [12] investigated wave motion in a general thin-shell structure."

### Outline Paragraphs
Mace frequently includes an **explicit outline paragraph** at the end of the introduction:
> "In this report, only free wave propagation is described and, in particular, numerical issues are discussed. First, the WFE formulation is briefly introduced and the conditioning of the eigenvalue problem is described… Numerical examples are presented for simple waveguides where the analytical solutions are available. The accuracy and validity of the results using different algorithms and FE models are also discussed. All calculations are performed in MATLAB. Finally some conclusions are drawn."

---

## 9. Conclusion Style

### Structure
Conclusions are **methodical summaries** that mirror the paper structure:
1. Restate the method/problem
2. Summarise each major finding in order
3. Note practical implications
4. (Rarely) suggest future work

### Characteristic Conclusion Language
> "In this report, the numerical issues for the waveguide finite element (WFE) method have been discussed."

> "Potential numerical errors have been discussed and categorised into the FE discretisation errors, the round-off errors due to the inertia term and errors induced by ill-conditioning."

> "The power and energy relationship and the finite difference method seem appropriate approaches specifically for general structures."

### What Mace Emphasises
- **Practical utility** of the methods developed
- **Trade-offs** between competing approaches
- **Validation** against analytical solutions
- **Generality** — whether the method extends to complex structures

### What Mace Avoids
- Overstating significance ("groundbreaking", "novel", "for the first time")
- Excessive future-work speculation
- Self-congratulatory language

---

## 10. JSV-Specific Conventions

### Observed in Mace's JSV Publications
- **Abstract length:** Typically 150–250 words, single paragraph
- **Abstract structure:** Method → Application → Key finding
- **Equation presentation:** Right-justified numbering (2.1), (2.2) etc.
- **Reference format:** Numbered, cited as [1], [2,3], or [5-7]
- **Section numbering:** Decimal system (1., 1.1, 1.1.1)
- **Figure references:** "Figure X" capitalised when used as a noun
- **Key phrase:** "Numerical examples are presented to illustrate the approach" (appears across multiple papers)

### JSV Abstract Pattern (from Mace's papers)
The abstract follows a consistent template:
1. **Context sentence** (what type of problem is addressed)
2. **Method description** (2–3 sentences on the approach)
3. **Specific application** (what structures/cases are considered)
4. **Key result** (1–2 sentences, often starting with "It is seen that…" or "The method is seen to yield…")

Example (from JASA 2005, representative of his JSV style):
> "A method is presented by which the wavenumbers for a one-dimensional waveguide can be predicted from a finite element (FE) model. The method involves postprocessing a conventional, but low order, FE model… A periodicity condition is applied, the wavenumbers following from the eigensolution of the resulting transfer matrix. The method is described, estimation of wavenumbers, energy, and group velocity discussed, and numerical examples presented… The method is seen to yield accurate results for the wavenumbers and group velocities of both propagating and evanescent waves."

---

## 11. Side-by-Side Transformation Guide

### Generic Academic → Mace Style

| Generic Academic Prose | Mace-Style Equivalent |
|---|---|
| "We propose a new method for…" | "A method is presented by which…" |
| "This paper introduces…" | "This paper concerns…" / "In this paper, X is considered." |
| "Our results show that…" | "It is seen that…" / "The results show that…" |
| "We can clearly see from Figure 3 that…" | "From Figure 3, it can be seen that…" |
| "It is important to note that…" | "It should be noted that…" / "It is worth noting that…" |
| "We found that the method works really well." | "The method is seen to yield accurate results." |
| "The errors are huge when…" | "The errors can become large when…" |
| "We validated our approach against…" | "The accuracy and validity of the results are evaluated by comparison with…" |
| "This is a major improvement." | "Significant error reduction is observed." |
| "The method doesn't work for…" | "The method is limited to…" / "Numerical difficulties may be encountered when…" |
| "We think this happens because…" | "This arises because…" / "This is attributable to…" |
| "In conclusion, our method is better." | "The [method] seems an appropriate approach for…" |
| "behavior" / "modeling" / "analyzed" | "behaviour" / "modelling" / "analysed" |

### Transformation Principles
1. **Remove "we" → use passive or method-as-subject constructions**
2. **Replace evaluative adjectives → use measured qualifiers** ("significant" not "dramatic")
3. **Replace colloquial → use formal equivalents** ("is of concern" not "is important")
4. **Add qualification → hedge appropriately** ("generally", "typically", "is likely to")
5. **Restructure for precision → front-load the technical content, qualify afterward**
6. **British English throughout**

---

## 12. Representative Excerpts

### Introduction Excerpt (TM964)
> "The waveguide finite element (WFE) method is a useful method when the dynamic behaviour of a uniform structure is of concern. The method involves the reformulation of the dynamic stiffness matrix, which includes the mass and stiffness matrices of a section of the structure, into the transfer matrix. Structural wave motion is expressed in terms of the eigenvalues and the eigenvectors of this matrix and these represent the wavenumbers and the wave modes respectively. However, several numerical difficulties arise when the problem is reformulated from a conventional finite element (FE) model."

### Literature Review Excerpt (TM964)
> "Many structures have uniformity or periodicity in certain directions. To analyse such structures, Floquet theory [1], which is one of the basic theories of wave propagation in periodic structures, or the transfer matrix method e.g. [2] can be used. The basic idea is that the propagation properties of waves in a periodic structure can be obtained from the propagation constants or by the transfer matrix. Although most of the early papers give the analytical dispersion relationship for relatively simple structures [3,4], numerical calculation is generally needed for complex structures."

### Results Discussion Excerpt (TM964)
> "The WFE results generally agree well with the analytical solution. Some discrepancies can be seen for higher wave modes and for large kₓLᵧ/π as the FE discretisation errors (and the round-off error due to the inertia term at low frequencies) increase. At low frequencies, two nearfield waves calculated in the WFE method become complex conjugate pairs as a numerical artefact. The real part is small compared to the imaginary part by a factor of about 10."

### Conference Abstract Excerpt (ICSVS 1997)
> "This paper concerns energy flow and statistical energy analysis (SEA) models of structural vibrations when modal overlap is small. In this circumstance the accuracy of SEA predictions is often poor. Particular reference is made to equipartition of energy (i.e., uniform energy density or modal energy throughout a system). It is seen, from both wave and modal analyses, that equipartition of energy does not occur in mechanical systems."

### Conclusions Excerpt (Eurodyn 2011)
> "In this paper a hybrid wave finite element/finite element (WFE/FE) approach for calculating the scattering properties of joints is used to obtain the vibrational behaviour of a waveguide structure. The waveguides are modelled using the WFE method where the FE model of a small segment of the waveguide is post-processed using periodic structure theory to obtain the wave characteristics of the waveguide… Thus, the vibrational behaviour of the structure is described in the wave domain which has many advantages."
