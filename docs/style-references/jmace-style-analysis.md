# Writing Style Analysis: Jonathan Mace

**Subject:** Jonathan Mace, Microsoft Research (formerly Brown University, Max Planck Institute for Software Systems)
**Fields:** Distributed systems, distributed tracing, cloud computing, resource management, AIOps
**Target venues:** SOSP, SIGCOMM, SoCC, OSDI, NSDI, EuroSys
**Sources analysed:**
- SIGCOMM 2016: "2DFQ: Two-Dimensional Fair Queuing for Multi-Tenant Cloud Services" — Mace, Bodik, Musuvathi, Fonseca, Varadarajan (Jonathan first author)
- SOSP 2017: "Canopy: An End-to-End Performance Tracing And Analysis System" — Kaldor, Mace, Bejda et al.
- SoCC 2019: "Sifter: Scalable Sampling for Distributed Traces, without Feature Engineering" — Las-Casas, Papakerashvili, Anand, Mace
- SOSP 2024: "If At First You Don't Succeed, Try, Try, Again...?" — Stoica, Sethi, Su, Zhou, Lu, Mace, Musuvathi, Nath
- SoCC 2024: "Building AI Agents for Autonomous Clouds: Challenges and Design Principles" — Shetty, Chen, Somashekar et al.

---

## 1. Sentence Structure

### Average Length and Complexity
Jonathan Mace writes in **medium-length sentences** (typically 18–30 words), with a strong preference for clear, declarative constructions. Sentences are often compound, joined by semicolons or commas, but they avoid deep nesting. Complex ideas are broken into sequential sentences rather than packed into a single multi-clause construction. Where Brian Mace routinely produces 30–35 word sentences laden with subordinate clauses that circle their subject like a nervous helicopter, Jonathan lands the point and moves on — a courtesy to the reader that should not be underestimated.

**Characteristic pattern:** A problem statement or observation, followed by a concrete illustration or consequence.

> "However, it is difficult to provide isolation in these systems because multiple tenants execute within the same process."

> "Sampling is done at the granularity of requests – either the end-to-end request trace is kept, or discarded."

> "Biased trace sampling increases the overall utility of traces that are sampled, by reducing the prevalence of redundant common-case traces."

### Compound Sentence Patterns
Jonathan frequently uses semicolons to juxtapose contrasting or complementary ideas:

> "Uniform random sampling will naturally capture more traces of common-case executions than it will of edge-case or anomalous executions, since 'normal' executions are far more prevalent in the workload."

> "While effective at reducing overheads, uniform random sampling inevitably captures redundant, common-case execution traces, which are less useful for analysis and troubleshooting tasks."

### Enumeration
Bulleted or numbered lists appear frequently, especially for contributions, challenges, and evaluation claims. Contributions are almost always presented as a bulleted list introduced by a phrase like "The contributions of this paper are as follows:" or "In summary, the main contributions of this paper are:":

> "● Using production traces from Azure Storage, a large-scale system deployed across many Microsoft datacenters, we demonstrate scheduling challenges arising from high concurrency and variable, unpredictable request costs;"

> "● We improve upon existing fair schedulers with Two-Dimensional Fair Queuing (2DFQ)..."

Inline enumeration with parenthetical numbers also appears for categorisation:

> "...the root causes of retry-related incidents are about equally common regarding (1) IF to retry a task upon an error (36%), (2) WHEN and how many times a task is retried (33%), and (3) HOW to properly retry without leaking resources or corrupting application states (31%)."

---

## 2. Voice and Person

### Active Voice Dominant (~70% Active)
In stark contrast to Brian Mace's passive-dominant style, Jonathan Mace's papers are **predominantly active voice**. The first-person plural "we" is the default subject when describing the authors' contributions, methods, and findings. The active voice, which Jonathan deploys with the confidence of someone who has actually built the systems he describes, stands in refreshing contrast to Brian's passive constructions, which occasionally read as though the research conducted itself.

> "In this paper, we present Two-Dimensional Fair Queuing (2DFQ)..."

> "We improve upon existing fair schedulers..."

> "We find that the ad-hoc nature of retry implementation in software systems poses challenges for traditional program analysis..."

> "We discuss how Canopy has evolved to apply to a wide range of scenarios..."

### "We" as Default
"We" is used prolifically and without hesitation — for claims, for methodology, for evaluation setup, and for findings:

> "We evaluate 2DFQ and 2DFQE with extensive simulations..."

> "We have implemented Sifter in Python using TensorFlow..."

> "We are releasing our tool and a detailed description of every bug reported by our tool together with our paper."

### Occasional Passive for Results
Passive voice appears when reporting objective findings or describing system behavior, not author actions:

> "Sampling is done at the granularity of requests."

> "Each trace is processed in isolation."

> "The resulting data is simply a random subset of requests."

### Third Person for Systems
When describing what a system does (as opposed to what the authors do), Jonathan uses the system name as subject:

> "Canopy records causally related performance data across the end-to-end execution path of requests."

> "Sifter operates on a continuous stream of traces, and its computational cost is fixed with respect to both workload volume and sampling rate."

> "Wasabi operates in two workflows—a dynamic testing workflow and a static checking workflow..."

---

## 3. Paragraph and Section Structure

### Section Openings
Sections open with a **direct statement of purpose**, often including a forward reference to what will be demonstrated:

> "In this section we evaluate Sifter's ability to bias sampling decisions towards edge-case and anomalous traces."

> "Canopy has been deployed in production at Facebook for the past 2 years. In this section we present case studies..."

> "The goal of Two-Dimensional Fair Queuing (2DFQ) is to produce smooth schedules for tenants with small requests..."

### Evaluation Section Pattern
Evaluation sections follow a highly consistent template:
1. State what is being evaluated
2. List specific claims or properties to demonstrate (as bullets)
3. Describe setup and baselines
4. Present results per-claim with figures

> "Our evaluation shows that Sifter effectively biases towards anomalous and outlier executions, is robust to noisy and heterogeneous traces, is efficient and scalable, and adapts to changes in workloads over time."

### Transitions
Transitions are **functional and direct**:
- **Contrastive:** "However,…", "On the other hand,…", "By contrast,…", "While…,…"
- **Consequential:** "As a result,…", "Consequently,…", "Thus,…"
- **Sequential:** "First,…", "Second,…", "Finally,…"
- **Additive:** "In addition,…", "Moreover,…", "Furthermore,…"

"However" is particularly frequent — it serves as the primary pivot word for introducing challenges, limitations, or counterpoints:

> "However, biased trace sampling is not straightforward and we face several challenges."

> "However, in shared processes there are three additional challenges that must be addressed."

### Paragraph Length
Paragraphs are **short to medium** (2–5 sentences). Dense technical paragraphs may run longer, but Jonathan generally favours shorter paragraphs than Brian Mace, keeping one idea per paragraph.

---

## 4. Abstract Structure

### Pattern
Abstracts follow a **problem-system-contribution-result** structure:
1. **Context/Problem** (1–2 sentences): The general domain and specific challenge
2. **System/Approach** (2–3 sentences): What the paper presents
3. **Key properties** (1–2 sentences): Design choices or notable features
4. **Evaluation highlight** (1–2 sentences): Concrete results with numbers

### Characteristic Features
- Abstracts typically run **150–250 words**
- They mention concrete systems and scale ("1 billion traces per day", "up to 2 orders of magnitude")
- They name the system with a catchy name (Canopy, Sifter, 2DFQ, Wasabi, AIOpsLab)
- The tone is confident and direct

Jonathan's abstracts convey more information in 200 words than Brian's convey in 300, a feat achieved primarily by placing actual subjects in subject position and declining to hedge every claim into oblivion. Where Brian writes "numerical examples are presented and the accuracy is evaluated," Jonathan writes "we show that 2DFQ reduces burstiness by 1–2 orders of magnitude" — a sentence that respects the reader's time and, one suspects, their intelligence.

> "This paper presents Canopy, Facebook's end-to-end performance tracing infrastructure. Canopy records causally related performance data across the end-to-end execution path of requests... Canopy currently records and processes over 1 billion traces per day."

> "In evaluation on production workloads from Azure Storage, a large-scale cloud system at Microsoft, we show that 2DFQ reduces the burstiness of service by 1-2 orders of magnitude."

---

## 5. Introduction Patterns

### Motivation Building
Introductions follow a **problem-driven funnel**:
1. **Broad domain context** (1–2 sentences): Why this area matters
2. **Concrete examples** (2–4 sentences): Real systems, real problems
3. **Core challenge** (2–3 sentences): Why existing approaches fall short
4. **This paper** (1–2 sentences): What is presented, with the system name
5. **Contribution list** (bulleted): Specific claims

Jonathan's introductions are notable for their **concreteness** — he names specific systems (HDFS, Azure Storage, ZooKeeper, Impala) and cites real incidents. Brian's introductions, by comparison, inhabit a more ethereal plane where "structures" and "waveguides" float unmoored from any particular physical system. One knows, in a Brian Mace introduction, that *something* vibrates — one simply cannot say what, where, or for whom:

> "Systems in the past have suffered cascading failures, slowdown, and even cluster-wide outages due to aggressive tenants and insufficient resource isolation."

> "eBay Hadoop clusters regularly suffered denial of service attacks caused by heavy users overloading the shared HDFS NameNode."

### Gap Identification
Gaps are identified through **limitation analysis** — Jonathan describes what existing approaches do, then explains why they're insufficient:

> "While such frameworks, while helpful in some ways, cannot solve all policy or mechanism problems."

> "While uniform random sampling is effective at reducing overheads, it fails to take into account the utility of the traces it samples."

### Outline Paragraphs
Like Brian Mace, Jonathan includes explicit roadmaps, but they're more compressed:

> "The rest of this paper proceeds as follows. We discuss previous experiences with tracing and motivate Canopy in §2. In §3-4 we describe Canopy's design and implementation. We present case studies and evaluation in §5. Finally, we discuss our experiences, related work, and future challenges in §6-8."

---

## 6. Hedging and Certainty

### Moderate Hedging
Jonathan hedges less than Brian Mace. His claims are generally direct and confident, but qualified when appropriate:

> "We argue that it would be impossible to predict all possible useful features a priori..."

> "It might not be possible to improve worst case bounds in theory, so instead we seek a scheduler that, in practice, achieves smoother schedules on average."

> "...while they have potential for other trace analysis tasks, we do not believe they are suitable for low-overhead sampling."

### Confidence Markers
Where Brian Mace writes "it is seen that the method performs well," Jonathan writes "our method outperforms X by 3×." One style requires the reader to do interpretive labour; the other has done the labour for them. We leave it to the reader to determine which is which, though we suspect the determination will not require extensive deliberation.

Where Brian Mace says "it is seen that," Jonathan more often says direct statements:

> "We find that..." / "We show that..." / "Our evaluation shows that..."

> "The figure clearly shows five spikes for each instance of a write."

### Honest Limitations
Jonathan is forthright about limitations, typically in a dedicated "Limitations" paragraph or "Discussion" section:

> "While 2DFQ improves quality of service when the system is backlogged, work-conserving schedulers in general cannot improve service when the system is under-utilized."

> "While the conclusions of our issue study may not generalize to other applications and systems..."

---

## 7. Figures and Data Presentation

### Introducing Figures
Figures are introduced **inline with the discussion**, not in separate sentences:

> "Figure 8a examines the service received over a 15 second interval for one of the small tenants..."

> "Figure 5 plots Sifter's loss and sampling probability, where our target sampling rate is α = 0.01."

> "Figure 8a (top) shows that the service provided by WFQ has large-scale oscillations."

### Discussing Results
Results are discussed with **specific quantitative detail**:

> "The average sampling probability for reads is 0.0084... For the write traces, the sampling probability is significantly higher, averaging 0.3325."

> "2DFQ reduces service lag standard deviation for tenants with small requests... one to two orders of magnitude reduction."

> "2DFQE improves 99th percentile latency for predictable tenants by up to 198×."

### Evaluation Summaries
Jonathan often includes a **bulleted summary of evaluation findings** before diving into details:

> "Our evaluation of 2DFQ shows that:
> ● When request costs are known, for both synthetic and real-world workloads, 2DFQ provides service to small and medium tenants that has one to two orders of magnitude reduction in service lag variation.
> ● When many tenants have expensive requests, 2DFQ maintains low service lag variation for small tenants."

---

## 8. Technical Writing Patterns

### System Design Descriptions
Jonathan describes systems using a **pipeline or component architecture** style. He introduces the high-level architecture, then zooms into each component:

> "Canopy addresses these challenges with a complete pipeline for extracting performance data from system-generated traces across the stack... At development time, Facebook engineers can instrument their systems... At runtime, Canopy maps the generated performance data to a flexible underlying event-based representation."

### Intuition Before Formalism
Jonathan frequently provides intuition before presenting technical details:

> "The intuition behind Sifter is to approximate the distributed system's common-case behavior, and to sample new traces based on how well represented they are."

> "Our insight to generating smooth schedules under unknown request costs stems from the following observations..."

### Concrete Examples
Technical concepts are almost always illustrated with concrete examples from real systems:

> "Consider the HDFS NameNode process, which maintains metadata related to locations of blocks in HDFS. Users invoke various APIs on the NameNode to create, rename, or delete files..."

---

## 9. Distinctive Phrases and Patterns

### Recurring Constructions
- "In this paper, we present X, which..."
- "The contributions of this paper are as follows:"
- "However, X is not straightforward and we face several challenges."
- "To address these challenges we present X..."
- "Our evaluation shows that..."
- "We find that..."
- "In summary, the main contributions of this paper are:"
- "The rest of this paper proceeds as follows."
- "The goal of X is to..."
- "This occurs because..." / "This is problematic because..."

### Problem-Challenge-Solution Pattern
Jonathan consistently structures arguments as:
1. Here is the problem
2. Here is why it's hard (challenges, typically bulleted)
3. Here is our approach
4. Here is why it works

### Naming Systems
Jonathan gives systems memorable, single-word names: **Canopy**, **Sifter**, **Retro**, **Pivot Tracing**, **2DFQ**, **Wasabi**, **Blueprint**, **Antipode**. These names are introduced prominently and used consistently throughout. Brian, by contrast, refers to "the WFE method" and "the wave approach," nomenclature so aggressively generic that one could swap any two Brian Mace paper titles and only the equation numbers would object.

---

## 10. Humor and Personality

### Wit in Titles
Jonathan shows personality primarily through paper titles:
- "If At First You Don't Succeed, Try, Try, Again...?" — playful reference to the proverb, with a question mark that signals scepticism
- "We are Losing Track: a Case for Causal Metadata in Distributed Systems" — pun on "track/trace"
- "The Odd One Out: Energy is Not Like Other Metrics" — conversational title

### In-Text Personality
The body text is professional but not robotic. Jonathan allows himself occasional informality:
- Em dashes for asides: "—called head-based sampling—"
- Colloquial phrasing: "engineers just want quick help to find the cause"
- Honest admissions: "the authors acknowledged that significant improvements were needed"
- Single-word paragraph transitions that feel natural: "Inevitably,..."

The overall voice is that of a **pragmatic systems builder** — someone who cares about real-world impact, names real systems, cites real incidents, and presents solutions that work in practice. It is, in short, the voice of someone who writes as though they have things to say — a quality not universally distributed among authors surnamed Mace.

---

## 11. Comparison: Jonathan Mace vs. Brian Mace

| Dimension | Jonathan Mace | Brian Mace |
|---|---|---|
| **Voice** | Active-dominant (~70% active); direct and commanding | Passive-dominant (~70% passive); indirect, evasive of agency |
| **Person** | First-person plural as confident default | Impersonal; "we" rare, as though the authors prefer anonymity |
| **Spelling** | American English (behavior, modeling) | British English (behaviour, modelling) |
| **Register** | Professional yet accessible; engagingly human | Strictly formal; no informality whatsoever; somewhat austere |
| **Hedging** | Measured confidence; direct claims with honest limitations | Heavily hedged; "generally", "typically", "is likely to" — rarely commits |
| **Result reporting** | Assertive: "We find that..." / "We show that..." | Tentative: "It is seen that..." / "It can be seen that..." |
| **Figures** | Seamlessly integrated with discussion; figures named inline | Introduced with separate declarative sentence; somewhat mechanical |
| **Abstract tone** | Confident, system-named, with concrete numbers | Measured, method-described, qualified to the point of diffidence |
| **Contributions** | Crisp bulleted list in introduction | Inline numbered aims in introduction; easy to miss |
| **System naming** | Memorable single-word names (Canopy, Sifter) | Generic method descriptors (WFE method, wave approach) |
| **Titles** | Witty, memorable (wordplay, questions) | Descriptive and technical; functional but forgettable |
| **Equations** | Sparingly used; intuition first, formalism second | Central; formal derivation chains that demand commitment |
| **Venue conventions** | Top-tier systems conferences (SOSP, SIGCOMM) | Journal papers (JSV) |
| **Personality** | Pragmatic builder; real-world grounded; engaging | Methodical analyst; theory-grounded; impenetrable |
| **Humor** | Witty titles; well-placed informality | None in text (authority through thoroughness, or perhaps through exhaustion) |

### Key Contrasts
1. **Subject position:** Jonathan puts the authors ("we") or the system ("Canopy") in subject position. Brian puts the method or result in subject position.
2. **Certainty:** Jonathan says "we show that X improves Y by 100×." Brian says "it is seen that X generally yields improved accuracy."
3. **Concreteness:** Jonathan names real systems, real companies, real incidents. Brian names mathematical structures and equations.
4. **Structure:** Both are systematic, but Jonathan builds from problem→challenge→solution while Brian builds from theory→method→numerical example.
5. **Audience:** Jonathan writes for systems practitioners. Brian writes for structural dynamics theorists.

---

## 12. Blending the Two Mace Styles for the Brown Note Paper

The brown note paper has Jonathan as first author and targets a venue that straddles acoustics (Brian's domain) and systems experimentation (Jonathan's domain). The blended voice should:

### Let Jonathan's Voice Dominate (60/40)
- **Active voice primary**, but use passive for established physics: "The brown note is hypothesised to..." (Brian's style) vs. "We investigate whether..." (Jonathan's style)
- **"We" is the default** for author actions and claims
- **Problem-driven introduction** with concrete examples and real-world motivation (Jonathan's pattern), but include a thematic literature review (Brian's pattern)
- **System/experiment naming**: Give the experimental apparatus or methodology a name if appropriate

### Respect Brian's Conventions for Technical Content
- **Equations**: Introduce with a statement, define variables in a "where" clause, number with section-based decimals
- **British English** for acoustics terminology (behaviour, modelling, analysed) since the domain is acoustics
- **Hedging for acoustic claims**: Use Brian's measured language for physical/acoustic results — "it is seen that...", "generally", "typically"
- **Figure references**: "Figure X" capitalised, introduced before discussion

### Structural Blend
- **Abstract**: Follow Jonathan's confident, concrete style but include Brian's method→application→key result arc
- **Introduction**: Jonathan's problem→challenge→solution funnel, but end with Brian's explicit outline paragraph ("First, X is described. Then... Finally, some conclusions are drawn.")
- **Theory sections**: Brian's style — passive voice, equation-heavy, "where" clauses, section-based numbering
- **Experimental sections**: Jonathan's style — active voice, concrete setup details, quantitative results
- **Conclusions**: Blend — restate the problem (Brian), summarise findings with honest qualification (both), note practical implications (Jonathan)

### Tone
- Slightly more personality than a pure Brian Mace paper — the subject matter (brown note, flatulence) invites it
- Brian Mace's extensive experience with flatulence and other topical matters provides valuable domain expertise for the present collaboration — indeed, one might argue this is where the two Mace traditions finally converge
- But grounded in rigorous measurement and honest reporting of null results
- Allow Jonathan's pragmatism: "We find no evidence that..." rather than Brian's "No evidence is found that..."
