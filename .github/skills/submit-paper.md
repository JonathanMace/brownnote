---
description: >
  Pre-submission checklist for the browntone paper. Covers manuscript
  preparation, figure checks, supplementary material, and journal requirements.
---

# Skill: Submit Paper

Complete checklist for preparing and submitting the browntone manuscript.

## Pre-Submission Checklist

### 1. Manuscript Content

- [ ] **Abstract** (≤ 250 words): background, gap, method, key result, conclusion
- [ ] **Keywords**: 4–6 relevant terms
- [ ] **All sections complete**: Introduction, Background, Methods, Results, Discussion, Conclusion
- [ ] **Word count** within journal limit (JSV: ~8000 words; Proc. Roy. Soc. A: ~10000)
- [ ] **All equations numbered** that are referenced; unnumbered otherwise
- [ ] **All symbols defined** at first use
- [ ] **All acronyms defined** at first use
- [ ] **No orphan references** (every `\cite` has a `\bibitem`; every bibitem is cited)
- [ ] **Consistent notation** throughout (check symbol table)
- [ ] **British English spelling** verified (run spell-check with British dictionary)

### 2. Figures

- [ ] All figures referenced in text with `\cref{fig:...}`
- [ ] Figure order matches order of discussion in text
- [ ] All figures have descriptive captions
- [ ] Captions are self-contained (reader can understand without text)
- [ ] Resolution: ≥ 300 DPI for raster; vector (PDF) for line art
- [ ] Fonts readable at printed column width
- [ ] Colour-blind accessible palette
- [ ] All axis labels include units
- [ ] File format acceptable to journal

### 3. Tables

- [ ] All tables referenced in text
- [ ] Use `booktabs` style (no vertical rules)
- [ ] Units in column headers, not in cells
- [ ] Consistent decimal places

### 4. References

- [ ] ≥ 30 references
- [ ] All BibTeX entries complete (authors, title, journal, year, volume, pages, DOI)
- [ ] DOIs present for all entries that have them
- [ ] Citation style matches journal requirements (author-year for JSV)
- [ ] No duplicate entries
- [ ] Recent references included (show awareness of current literature)

### 5. Supplementary Material

- [ ] Data availability statement drafted
- [ ] Code repository link included (if open-sourcing)
- [ ] Supplementary figures/tables prepared if needed
- [ ] Mesh files and input scripts archived for reproducibility

### 6. LaTeX Compilation

```bash
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

- [ ] Compiles without errors
- [ ] No overfull hbox warnings > 1pt
- [ ] No undefined references
- [ ] No missing citations
- [ ] Page count within limits
- [ ] All hyperlinks work

### 7. Author & Metadata

- [ ] All author names, affiliations, and emails correct
- [ ] Corresponding author designated
- [ ] ORCID IDs included
- [ ] Funding acknowledgements complete
- [ ] Conflict of interest statement

### 8. Journal-Specific Requirements

#### Journal of Sound and Vibration (Elsevier)
- Article class: `elsarticle` with `review` option for double-spacing
- Figures: separate files, EPS/PDF/TIFF
- Highlights: 3–5 bullet points (max 85 chars each)
- Graphical abstract: optional but recommended
- Cover letter required

#### Proceedings of the Royal Society A
- Article class: `rsproca`
- Ethics statement required
- Data accessibility statement required
- Author contributions (CRediT format)

### 9. Final Steps

1. Generate final PDF: `latexmk -pdf main.tex`
2. Proofread the PDF (not just the source)
3. Check all figure/table numbering is correct
4. Verify page numbers, headers, footers
5. Prepare cover letter
6. Submit via journal's online system
7. Archive the exact submitted version: `git tag v1.0-submitted`
