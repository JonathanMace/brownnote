# Bibliography Check & Scooping Risk Assessment — 2026-03-27T0902

**Auditor**: Bibliographer agent
**Scope**: All four papers + bladder project
**Date**: 27 March 2026

---

## 1. Scooping Risk Assessment

**Overall risk level**: LOW

No published work was found (in the repo's existing literature corpus or known
to the auditor from the acoustics/biomechanics literature through early 2026)
that replicates our core claims. The novelty position across all four papers
remains strong.

### 1.1 Paper-by-Paper Assessment

| # | Paper | Core Claim | Scooping Risk | Rationale |
|---|-------|-----------|---------------|-----------|
| 1 | Brown Note (JSV) | First-principles modal analysis of abdomen as fluid-filled shell; coupling disparity 6.6x10^4 | **NONE** | No prior work derives abdominal eigenfrequencies from shell theory with fluid-structure coupling. Existing lit is purely empirical (ISO 2631, Kitazaki & Griffin 1998). FEA models of abdomen exist for crash/blast, not resonance prediction. |
| 2 | Gas Pockets (JASA) | Constrained bubble model for bowel gas as impedance-matching transducer | **NONE** | Church (1995) and Hoff (2000) model encapsulated microbubbles for ultrasound contrast agents. Leighton (1994) covers bubble acoustics generally. Nobody has applied this to intestinal gas at infrasound frequencies. Entirely novel mechanism. |
| 3 | Scaling Laws (JSV Short) | Buckingham Pi reduces 11-param shell to 5 groups; cross-species R ~ 10^3-10^4 | **NONE** | Dimensional analysis of fluid-filled shells is classical (Junger & Feit), but the specific application to cross-species scaling of visceral resonance is novel. No competing work. |
| 4 | Bladder Resonance | f2 = 12-18 Hz for urinary bladder; WBV coupling 7,600x | **LOW** | Nenadic et al. (2013) performed ultrasound bladder vibrometry (UBV) measuring in vivo shear wave speed, but this estimates wall modulus - it does not predict resonant modes. No first-principles resonance model exists. Closest competitor is the UBV group (Mayo Clinic), who could extend their work to mode prediction. |

### 1.2 Detailed Overlap Analysis

| Potential Overlap | Closest Work | Published | Our Advantage | Severity |
|-------------------|-------------|-----------|---------------|----------|
| Modal analysis of abdominal wall | FEA crash models (Ruan 2003, Robin 2019) | Various | They model injury thresholds, not eigenfrequencies or coupling | NONE |
| Infrasound-abdomen coupling model | Leventhall (2007), von Gierke (1974) | 2007, 1974 | Qualitative reviews only; no quantitative coupling ratio | NONE |
| Gas pocket transduction | Church (1995), Hoff (2000) - encapsulated microbubbles | 1995, 2000 | Different scale (um vs cm), different frequency regime (MHz vs Hz), different application | NONE |
| Dimensional analysis of shell vibration | Barenblatt (1996), Buckingham (1914) - general methodology | Classical | Application to cross-species abdominal resonance is new | NONE |
| Bladder resonance frequency | Nenadic et al. (2013) - UBV | 2013 | They measure modulus, not predict modes; no fill-state dependence of frequency | LOW |
| WBV and urinary symptoms | Seidel (1986), occupational health literature | Various | Epidemiological only; no mechanistic model | NONE |

### 1.3 Emerging Risks to Monitor

1. **Mechanosensitive channels in GI tract**: Zeitzschel & Lechner (2024)
   published a review of mechanosensitive ion channels in GI
   mechanotransduction. Already cited in Paper 2. Their work is complementary
   (biology side), not competing (physics side).

2. **Blast injury modelling**: Active field with military funding. Current
   focus is lung/TBI, not abdominal resonance per se. If someone publishes a
   fluid-filled shell model of blast-bowel interaction, it would partially
   overlap with our broader applications section - but our infrasound coupling
   analysis remains distinct.

3. **Ultrasound bladder vibrometry group** (Nenadic, Urban, Chen - Mayo
   Clinic): They have the experimental apparatus to measure bladder resonant
   modes in vivo. If they publish mode predictions, the bladder paper would
   need repositioning. **Recommendation**: submit the bladder paper before
   this group extends their work.

4. **Wind turbine infrasound**: Continuing controversy but no new coupling
   models. Salt & Hullar (2010) cochlear pathway is distinct from our
   abdominal pathway.

---

## 2. Citation Health Check

### 2.1 Paper 1 - Brown Note (paper/)

**BibTeX entries**: 36 total

#### Cite keys used in TeX files:

`iso2631`, `griffin1990handbook`, `mansfield2005human`, `Mohr1965`,
`Leventhall2007`, `Gavreau1966`, `vonGierke1974`, `vonGierke2002`,
`Tandy1998`, `Leventhall2003`, `Altmann1999`, `Jauchem2007`,
`junger2012sound`, `lamb1882`, `parker2011imaging`,
`kitazaki1998resonance`, `Heil1996`, `coste2010piezo1`,
`Seidel1986`, `Ishitake2002`, `Moller2004`, `Soedel2004`,
`Leissa1973`, `Stuhmiller2008`, `Owers2011`, `Mayorga1997`,
`Feuillade1996`, `Love1978`, `Southall2007`, `terHaar2007`,
`Bailey2003`, `Duck1999`

**Total cite keys**: 32
**All keys resolve**: Yes

#### Orphaned BibTeX entries (defined but never cited):

| Key | Entry | Action |
|-----|-------|--------|
| `Fahy2007` | Fahy & Gardonio, Sound and Structural Vibration | Consider citing in S2 (formulation) or remove |
| `Fung1993` | Fung, Biomechanics | Should be cited in Table 1 as source for tissue properties |
| `Geuzaine2009` | Gmsh | Remove unless FEA content is added |
| `Baratta2023` | DOLFINx | Remove unless FEA content is added |
| `Hernandez2005` | SLEPc | Remove unless FEA content is added |
| `Junger1986` | Junger & Feit (year=1986) | **DUPLICATE** of `junger2012sound` - remove |
| `Leventhall2009` | Leventhall, JLFNVAC | Consider citing alongside Leventhall2007, or remove |
| `vonGierke1966` | von Gierke 1966 NASA report | Overlaps with vonGierke1974; remove or cite |

**Orphaned count**: 8

#### Duplicate entries:

| Entry 1 | Entry 2 | Same Work? | Action |
|---------|---------|-----------|--------|
| `Junger1986` (year=1986, 2nd ed, MIT Press) | `junger2012sound` (year=1993, 2nd ed, MIT Press) | **YES** - same book, different year metadata | Remove `Junger1986`; keep `junger2012sound`. Fix year from 1993 to 1986. |

#### Formatting issues:

| Key | Issue | Fix |
|-----|-------|-----|
| `lamb1882` | Type is @book but it's a journal article (Proc. London Math. Soc.) | Change to @article, fix publisher to journal, add doi |
| `junger2012sound` | Year listed as 1993; the MIT Press 2nd edition was published 1986 | Change year to 1986 |
| `Baratta2023` | @article with no journal/volume/pages (it's a Zenodo preprint) | Change to @misc or add journal if published |
| `Duck1999` | @book with booktitle field (should be @incollection or @article) | Fix entry type |
| `vonGierke1966` | Missing journal field; just has note | Add journal or change to @techreport |
| `Moller2004` | Missing doi | Add doi = {10.4103/1463-1741.6296} |
| `kitazaki1998resonance` | Missing doi | Add doi = {10.1016/S0021-9290(97)00126-7} |
| `Feuillade1996` | Key says 1996 but year field says 1998 | Rename key to Feuillade1998 or accept inconsistency |

---

### 2.2 Paper 2 - Gas Pockets (paper2-gas-pockets/)

**BibTeX entries**: 30 total

#### Cite keys used:

`Jauchem2007`, `Leventhall2007`, `Mohr1965`, `vonGierke1974`,
`Levitt1971`, `Suarez1997`, `Bedell1956`, `Serra2001`,
`Coste2010`, `Alcaino2017`, `Zeitzschel2024`, `Fung1993`,
`Gregersen2000`, `Higa2007`, `Minnaert1933`, `Church1995`,
`Hoff2000`, `Leighton1994`, `Mazzuoli2015`, `Junger1986`,
`Harder2003`

**Total cite keys**: 21
**All keys resolve**: Yes (uses natbib with \citep and \citet)

#### Orphaned BibTeX entries:

| Key | Entry | Action |
|-----|-------|--------|
| `Commander1989` | Commander & Prosperetti - bubbly liquids | Highly relevant - cite in S2 (resonance) or S5 (comparison) |
| `Plesset1977` | Plesset & Prosperetti - bubble dynamics | Cite in introduction or model section |
| `Prosperetti1988` | Prosperetti - bubble noise in ocean | Less directly relevant; consider removing |
| `iso2631` | ISO 2631 | Should be cited in introduction when discussing WBV context |
| `Kitazaki1998` | Kitazaki & Griffin | Consider citing for body resonance context |
| `Griffin1990` | Griffin, Handbook | Should be cited; overlaps with griffin1990handbook in Paper 1 |
| `Iovino2006` | Iovino et al. - sympathetic modulation of gut distention | Relevant to clinical implications - cite in S5 |

**Orphaned count**: 7

#### Formatting issues:

| Key | Issue | Fix |
|-----|-------|-----|
| `Alcaino2017` | Missing doi | Add DOI |
| `Iovino2006` | Volume 109 appears incorrect for Gastroenterology 2006 | Verify: likely vol. 130 (2006) or this is the 1995 paper (vol. 109) |
| `Gregersen2000` | Volume 8 incorrect for Neurogastro Motil; doi prefix 10.1007 is Springer | Verify journal/volume/doi |

---

### 2.3 Paper 3 - Scaling Laws (paper3-scaling-laws/)

**BibTeX entries**: 3 total (Soedel2004, Leissa1973, mace2026brown)

**Total cite keys**: 3
**All keys resolve**: Yes

#### CRITICAL ISSUE: Severely under-referenced

A short communication still requires adequate referencing. Paper 3 should cite:

| Missing Reference | Why Needed | Where |
|-------------------|-----------|-------|
| Buckingham (1914) or Barenblatt (1996) | Foundational reference for Pi theorem | S2, first mention of Buckingham Pi |
| Junger & Feit (1986) | Fluid-filled shell theory used throughout | S2, shell equations |
| Fung (1993) | Tissue property ranges in parametric study | S3 |
| ISO 2631 | Cross-species validation context | S4 |
| Griffin (1990) | WBV and abdominal resonance | S4 |
| Lamb (1882) | Added mass formulation | S2 |
| Kitazaki & Griffin (1998) | Experimental validation data | S4 |

**Orphaned entries**: None (all 3 are cited).

---

### 2.4 Bladder Resonance (projects/bladder-resonance/paper/)

#### CRITICAL: No references.bib file exists

The LaTeX source (main.tex) calls \bibliography{references} but there is no
references.bib file in projects/bladder-resonance/paper/. **The paper will
not compile.**

#### Cite keys used (all broken):

`iso2631`, `Seidel1986`, `griffin1990handbook`, `Mace2025browntone`,
`Nenadic2013`, `Barnes2016`, `VanMastrigt1991`, `Akkus2014`,
`Griffiths1980`, `coste2010piezo1`, `mansfield2005human`,
`Pelvic2019`, `Lauper2009`, `NCT03325660`, `Fung1993`, `lamb1882`,
`junger2012sound`

**Total cite keys**: 17
**Keys with matching bib entry**: 0 / 17

**Action required**: Create references.bib with all 17 entries.

---

## 3. Suggested New References

### 3.1 Paper 1 - Brown Note

| Reference | Where to Cite | Why |
|-----------|--------------|-----|
| Fung (1993) - already in bib | Table 1 (parameter sources) | Justifies tissue density, Poisson's ratio values |
| Fahy & Gardonio (2007) - already in bib | S2 (formulation), alongside Junger & Feit | Standard reference for sound-structure interaction |
| Coermann et al. (1960) | S1 or S3, ISO 2631 discussion | Original experimental measurement of seated body resonance at 4-6 Hz |
| Sandover (1998) | S3, validation section | Measured abdominal resonance in the 4-8 Hz range |
| Toward & Griffin (2011) | S3, validation section | Updated experimental transmissibility data |
| Rayleigh (1877/1945) Theory of Sound | S2.4, Rayleigh regime discussion | Foundational reference for long-wavelength scattering |

### 3.2 Paper 2 - Gas Pockets

| Reference | Where to Cite | Why |
|-----------|--------------|-----|
| Commander & Prosperetti (1989) - already in bib | S2.1 or S5 | Validates bubbly-liquid wave propagation theory |
| Plesset & Prosperetti (1977) - already in bib | S1, bubble dynamics context | Foundational bubble dynamics review |
| Keller & Miksis (1980) | S2, bubble oscillation | More complete bubble dynamics equation |
| de Jong et al. (2002) | S5, comparison with contrast agents | Encapsulated bubble review |
| Iovino et al. (2006) - already in bib | S5, clinical implications | Sympathetic modulation of gut distention perception |

### 3.3 Paper 3 - Scaling Laws

| Reference | Where to Cite | Why |
|-----------|--------------|-----|
| Buckingham (1914) Phys. Rev. | S2, Buckingham Pi theorem | Original Pi theorem paper |
| Barenblatt (1996) Scaling | S2, dimensional analysis | Standard modern reference |
| Junger & Feit (1986) | S2, shell equations | Source of the fluid-filled shell formulation used |
| Fung (1993) | S3, tissue properties | Source of parameter ranges |
| ISO 2631:1997 | S4, cross-species context | Establishes the 4-8 Hz band being predicted |
| Lamb (1882) | S2, added mass | Classical fluid loading result |

### 3.4 Bladder Resonance

| Reference | Where to Cite | Why |
|-----------|--------------|-----|
| Nenadic et al. (2013) Phys. Med. Biol. | S1 (intro), S2 (theory) | In vivo bladder wall modulus measurements; key validation data |
| Barnes (2016) PhD thesis, Birmingham | S1, S2 | Ex vivo tensile testing of bladder wall |
| Van Mastrigt (1991) J. Smooth Muscle Res. | S2, viscoelastic properties | Detrusor viscoelastic characterisation |
| Akkus et al. (2014) PLoS ONE | S2, wall thickness | In vivo wall thickness vs fill state |
| Griffiths (1980) Med. Biol. Eng. Comput. | S2, cystometry data | Intravesical pressure vs fill volume |

---

## 4. Cross-Paper Consistency Issues

| Issue | Papers Affected | Severity |
|-------|----------------|----------|
| Junger & Feit cited as junger2012sound (P1), Junger1986 (P2), not cited (P3) | 1, 2, 3 | MEDIUM |
| Griffin cited as griffin1990handbook (P1, bladder) vs Griffin1990 (P2 bib, uncited) | 1, 2, bladder | LOW |
| coste2010piezo1 (P1) vs Coste2010 (P2) - same paper, different keys | 1, 2 | LOW |
| kitazaki1998resonance (P1) vs Kitazaki1998 (P2 bib, uncited) - same paper | 1, 2 | LOW |
| Fung1993 orphaned in P1 but cited in P2 and bladder | 1, 2, bladder | LOW |
| Paper 3 cites mace2026brown - verify this key stays synchronised with Paper 1 | 3 | LOW |

---

## 5. Related Work Radar

### 5.1 Directly Competing

| Paper | Status | Overlap | Our Action |
|-------|--------|---------|------------|
| *None identified* | - | - | Monitor Google Scholar alerts |

### 5.2 Complementary

| Paper | Category | One-Line Summary | Our Action |
|-------|----------|-----------------|------------|
| Zeitzschel & Lechner (2024) Channels | Mechanotransduction | Review of mechanosensitive ion channels in GI tract | Already cited in Paper 2 |
| Coermann et al. (1960) | Body resonance | Original seated body resonance measurements at 4-6 Hz | Add to Paper 1 refs |
| Sandover (1998) | Abdominal resonance | Measured abdominal resonance data | Add to Paper 1 refs |
| Toward & Griffin (2011) | Abdominal transmissibility | Updated experimental transmissibility | Add to Paper 1 refs |
| Nenadic et al. (2013) PMB | Bladder vibrometry | In vivo shear wave speed for bladder wall modulus | Critical for bladder paper |

### 5.3 Methodologically Relevant

| Paper | Category | One-Line Summary | Our Action |
|-------|----------|-----------------|------------|
| Church (1995) JASA | Encapsulated bubbles | Elastic shell effects on gas bubble pulsation | Already cited in Paper 2 |
| Hoff et al. (2000) JASA | Polymeric microbubbles | Oscillations of encapsulated contrast agents | Already cited in Paper 2 |
| Barenblatt (1996) | Dimensional analysis | Standard reference for scaling/Pi analysis | Add to Paper 3 |

### 5.4 Application Overlap

| Paper | Category | One-Line Summary | Our Action |
|-------|----------|-----------------|------------|
| Stuhmiller et al. (2008) | Blast injury | Physics of primary blast injury | Already cited in Paper 1 |
| Feuillade & Nero (1998) JASA | Fish acoustics | Viscoelastic swimbladder resonance model | Already cited in Paper 1 |
| Southall et al. (2007) | Marine mammal noise | Noise exposure criteria for marine mammals | Already cited in Paper 1 |

---

## 6. Summary of Actions

### Critical (blocking)

1. **Create references.bib for bladder paper** - 17 cite keys with no bib
   file. Paper will not compile.

### High Priority (before submission)

2. **Remove duplicate** Junger1986 from Paper 1 bib; fix year in
   junger2012sound from 1993 to 1986.
3. **Fix lamb1882** entry type from @book to @article with correct journal
   field.
4. **Cite Fung1993** in Paper 1 Table 1 (currently orphaned but is the source
   for tissue parameters).
5. **Add at least 4 references to Paper 3** - currently has only 3 refs,
   inadequate even for a short communication.
6. **Cite orphaned entries or remove them** - 8 orphaned in Paper 1, 7 in
   Paper 2.

### Medium Priority (strengthens papers)

7. Add Coermann et al. (1960), Sandover (1998), and Toward & Griffin (2011)
   to Paper 1 validation.
8. Cite Commander & Prosperetti (1989) and Plesset & Prosperetti (1977) in
   Paper 2 (currently orphaned but relevant).
9. Cite iso2631 in Paper 2 introduction (currently orphaned but clearly
   relevant).
10. Standardise citation keys across papers for shared references (Junger,
    Griffin, Kitazaki, Coste, Fung).

### Low Priority (nice to have)

11. Add DOIs to entries missing them (Moller2004, kitazaki1998resonance, etc.).
12. Verify Gregersen2000 and Iovino2006 bibliographic details (volume numbers
    appear incorrect).
13. Add Rayleigh (1877) to Paper 1 for completeness in the scattering
    discussion.
14. Fix Feuillade1996 key/year inconsistency (key says 1996, entry says 1998).

---

## 7. Monitoring Recommendations

Set up Google Scholar alerts for:
- "abdominal resonance" AND "modal analysis"
- "fluid-filled shell" AND "infrasound"
- "bowel gas" AND "acoustic"
- "bladder resonance" AND "vibration"
- "Buckingham Pi" AND "shell vibration"
- "whole-body vibration" AND "gastrointestinal" AND "model"

Monitor specific authors:
- **Nenadic / Urban / Chen** (Mayo Clinic) - bladder vibrometry
- **Leventhall** - infrasound reviews
- **Griffin / Toward** (ISVR Southampton) - WBV experimental data
- **Prosperetti** - bubble dynamics extensions

Check conference proceedings:
- JASA/ASA meetings (November, May)
- Inter-Noise / Noise-Con
- JSV special issues on bio-acoustics
- ESB (European Society of Biomechanics) annual meeting

---

*Report generated by the Bibliographer agent. No internet access was available
during this audit; scooping risk assessment is based on the existing literature
corpus in the repository and the auditor's knowledge of the field through early
2026. A web-based search should be conducted before submission to verify no new
competing publications have appeared.*
