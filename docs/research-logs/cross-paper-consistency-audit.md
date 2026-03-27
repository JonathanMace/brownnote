# Cross-Paper Consistency Audit Report - 2026-03-27T1030

## Scope

Audited all four papers in the Browntone pipeline for parameter consistency,
cross-references, notation, and code-paper agreement.

| Paper | Location | Venue | Status |
|-------|----------|-------|--------|
| Paper 1: Brown Note | paper/ | JSV | ACCEPT |
| Paper 2: Gas Pockets | paper2-gas-pockets/ | JASA | Round 2 |
| Paper 3: Scaling Laws | paper3-scaling-laws/ | JSV Short | Draft |
| Bladder Resonance | projects/bladder-resonance/paper/ | JSV/J Biomech | Draft |

---

## Summary: 14 issues found (3 CRITICAL, 7 WARNING, 4 INFO)

---

## 1. Shared Parameter Consistency

### Canonical values (from .github/copilot-instructions.md):

| Parameter | Symbol | Canonical | Paper 1 | Paper 2 | Paper 3 | Bladder | Code v2 |
|-----------|--------|-----------|---------|---------|---------|---------|---------|
| Semi-major axis | a | 0.18 m | 0.18 OK | N/A | 0.18 OK | N/A | 0.18 OK |
| Semi-minor axis | c | 0.12 m | 0.12 OK | N/A | 0.12 (via c/a) OK | N/A | 0.12 OK |
| Wall thickness | h | 0.010 m | 0.010 OK | 3 mm (intestine) OK | 0.010 OK | 1.5-5 mm (bladder) OK | 0.010 OK |
| Elastic modulus | E | 0.1 MPa | 0.1 MPa OK | 10 kPa (intestine) OK | 0.1 MPa OK | 29-145 kPa (bladder) OK | 0.1 MPa OK |
| Poisson's ratio | nu | 0.45 | 0.45 OK | 0.45 OK | 0.45 OK | 0.49 (bladder) OK | 0.45 OK |
| Wall density | rho_w | 1100 kg/m3 | 1100 OK | 1040 (intestine) OK | 1100 OK | 1050 (bladder) OK | 1100 OK |
| Fluid density | rho_f | 1020 kg/m3 | 1020 OK | 1020 OK | 1020 OK | 1020 OK | 1020 OK |
| Fluid bulk modulus | K_f | 2.2 GPa | 2.2 GPa OK | N/A | 2.2 GPa OK | 2.2 GPa OK | 2.2 GPa OK |
| IAP | P_iap | 1000 Pa | 1000 OK | N/A | 1000 OK | 490-2940 Pa (bladder) OK | 1000 OK |
| Loss tangent | eta | 0.25 | 0.25 OK | N/A | 0.25 OK | 0.40 (bladder) OK | 0.25 OK |

**Verdict: PASS** - All shared parameters are consistent. Papers 2 and Bladder
correctly use different organ-specific values (intestinal wall E=10 kPa,
bladder nu=0.49, etc.) reflecting different anatomical structures.

---

## 2. Derived Quantity Consistency

| Quantity | Canonical | Paper 1 | Code v2 | Discrepancy |
|----------|-----------|---------|---------|-------------|
| R_eq | 0.157 m | 0.157 m | 0.1572 m | <0.2% OK |
| f2 | 3.95 Hz | 4.0 Hz | 3.9524 Hz | Paper rounds to 4.0 (1.2%) OK |
| Q | 4.0 | 4.0 | 4.0 | OK |
| zeta | 0.125 | 0.125 | 0.125 | OK |
| ka | 0.0114 | 0.0114 | 0.01138 | <0.2% OK |
| Breathing f0 | ~2490 Hz | ~2500 Hz | 2490.65 Hz | Paper rounds to 2500 (0.4%) OK |
| xi_air (energy, 120 dB) | 0.014 um | 0.014 um | 0.01374 um | 1.9% (rounding) OK |
| xi_air (pressure, 120 dB) | - | 0.18 um | 0.1844 um | 2.4% (rounding) OK |
| Coupling ratio R | ~66,000 | 6.6e4 | 65,500 | <1% OK |
| Gamma_2 | 0.48 | 0.48 | - | OK |

### Cross-relationship checks:
- Q = 1/eta: 1/0.25 = 4.0 OK
- zeta = eta/2: 0.25/2 = 0.125 OK
- xi_pressure / xi_energy = 13.4x (code: 13.416) OK

**Verdict: PASS** - All derived quantities match to within acceptable rounding.

---

## 3. Cross-Paper References

### 3a. Paper 2 -> Paper 1 (CRITICAL)

**Paper 2 does NOT formally cite Paper 1.** Line 112 says:
`Our companion paper (Paper~1, submitted to JSV) demonstrated that...`

There is NO \citep or \cite command and NO entry in paper2-gas-pockets/references.bib
for Paper 1. This is unacceptable for a journal submission.

| Severity | CRITICAL |
|----------|----------|
| Fix | Add @unpublished{Mace2025browntone, ...} to paper2-gas-pockets/references.bib and replace all `Paper~1` references with \citep{Mace2025browntone} |

### 3b. Paper 3 -> Paper 1 (PASS with WARNING)

Paper 3 correctly uses \cite{mace2026brown} with a matching bib entry.
**However**, the year is 2026, while the Bladder paper's citation uses year 2025
(Mace2025browntone). These cite the same work with different years.

| Severity | WARNING |
|----------|---------|
| Fix | Standardise citation key and year across all papers (recommend Mace2025browntone, year 2025) |

### 3c. Bladder -> Paper 1 (PASS)

Bladder paper correctly uses \cite{Mace2025browntone} with matching bib
entry (@unpublished, year 2025). OK

### 3d. Cross-reference of key values

| Claim | Paper 2 | Paper 3 | Bladder | Correct? |
|-------|---------|---------|---------|----------|
| Coupling ratio ~66,000 / 6.6e4 | N/A | 6.6e4 (intro) OK | ~66,000 OK | OK |
| xi_air = 0.014 um at 120 dB | 0.014 um OK | N/A | N/A | OK |
| Breathing mode ~2490 Hz | ~2490 Hz OK | ~2490 Hz OK | ~2500 Hz OK | OK |
| Flexural 4-10 Hz | 4-10 Hz OK | 4-10 Hz OK | Abdomen 4.0 Hz OK | OK |
| SPL >180 dB for 1 um | >180 dB OK | N/A | N/A | OK |

---

## 4. Coupling Ratio Definitions (WARNING)

**Paper 1** defines the coupling ratio as the full displacement ratio:
`R = xi_mech / xi_air = 917/0.014 = 6.6 x 10^4`

**Paper 3** defines the coupling ratio differently (Table 2 caption):
`R = 1/(ka)^2 (radiation-efficiency penalty only)`
This yields R = 7,700 for humans - nearly an order of magnitude smaller.

Both papers use the same symbol \mathcal{R} with fundamentally different
definitions. Paper 3's introduction correctly quotes Paper 1's 6.6e4, but
then its own R values in Table 2 and conclusion (10^3-10^4) use the different
definition. A reader would be confused.

| Severity | WARNING |
|----------|---------|
| Fix | Paper 3 should either (a) use a different symbol for 1/(ka)^2, or (b) clearly state the definition difference |

---

## 5. Internal Inconsistency: Section 2 vs Section 4 (Paper 1)

**Section 2** (Eq. coupling_ratio_def, line 258):
`\mathcal{R} \sim 10^3 -- 10^4`

**Section 4** (Eq. coupling_ratio, line 95):
`\mathcal{R} \approx 6.6 \times 10^4`

The value 6.6e4 = 66,000 lies OUTSIDE the stated range 10^3-10^4 = 1,000-10,000.
Even the Gamma_2-corrected value (~3e4) exceeds the upper bound.

The Section 2 range appears to originate from the UQ distribution (Table 3 shows
median 10^4, 90% CI [10^3, 10^4] in order-of-magnitude notation) but is misleading
when read as a range that should encompass the baseline estimate.

| Severity | CRITICAL |
|----------|----------|
| Fix | Change Section 2 to `\sim 10^4` or `\sim 10^4--10^5` to encompass the baseline value of 6.6e4 |

---

## 6. Missing Figure Files

### Paper 1 (PASS)
All 7 \includegraphics references resolve to files in data/figures/. OK

### Paper 2 (PASS)
All 4 \includegraphics references resolve to files in paper2-gas-pockets/figures/. OK

### Paper 3 (PASS)
Both \includegraphics references resolve to files in paper3-scaling-laws/figures/. OK

### Bladder (CRITICAL - 3 missing figures)

| Referenced path | Exists? |
|----------------|---------|
| ../figures/fig_bladder_frequency_vs_volume.png | YES |
| figures/fig_stiffness_mass_decomposition.pdf | MISSING |
| figures/fig_tornado_sensitivity.pdf | MISSING |
| figures/fig_minimum_shift.pdf | MISSING |
| ../figures/fig_bladder_coupling.png | YES |

The projects/bladder-resonance/paper/figures/ directory does not exist.

| Severity | CRITICAL |
|----------|----------|
| Fix | Generate the 3 missing figures or update .tex to reference existing files |

---

## 7. Notation Consistency Across Papers

| Quantity | Paper 1 | Paper 2 | Paper 3 | Bladder | Consistent? |
|----------|---------|---------|---------|---------|-------------|
| Elastic modulus | E | E_w | E | E | OK (P2 subscript appropriate) |
| Poisson's ratio | nu | nu_w | nu | nu | OK |
| Wall density | rho_w | rho_w | rho_w | rho_w | OK |
| Fluid density | rho_f | rho_f | rho_f | rho_f | OK |
| Shell thickness | h | h_w | h | h | OK |
| Geometry | a, c | R (lumen) | a, c | R (sphere) | OK (different shapes) |
| Coupling ratio | R = xi_mech/xi_air | - | R = 1/(ka)^2 | R | WARNING: P3 redefines! |

**Verdict: WARNING** - Coupling ratio symbol used with different definitions
in Paper 1 vs Paper 3 (see section 4).

---

## 8. Code-Paper Agreement

Ran the canonical model via AbdominalModelV2() and associated functions.

### Key comparisons:

| Quantity | Code output | Paper 1 value | Match? |
|----------|-------------|---------------|--------|
| f2 | 3.9524 Hz | 4.0 Hz | 1.2% (rounding) OK |
| f3 | 6.3087 Hz | 6.3 Hz | 0.14% OK |
| f4 | 8.8795 Hz | 8.9 Hz | 0.23% OK |
| f0 (breathing) | 2490.65 Hz | ~2500 Hz | 0.4% OK |
| ka | 0.01138 | 0.0114 | 0.2% OK |
| R_eq | 0.1572 m | 0.157 m | 0.1% OK |
| xi_energy (120 dB) | 0.01374 um | 0.014 um | 1.9% (rounding) OK |
| xi_pressure (120 dB) | 0.1844 um | 0.18 um | 2.4% (rounding) OK |
| xi_mech (0.5 m/s2) | 4586 um | 4586 um | exact OK |
| xi_mech (1.15 m/s2) | 10549 um | 10549 um | exact OK |
| Coupling ratio | 65,500 | 66,000 | 0.8% OK |

### Code default parameter check:
All 10 default parameters in AbdominalModelV2 match the canonical table exactly. OK

**Verdict: PASS** - All code outputs agree with paper claims within rounding tolerance.

---

## 9. Stale Content Detection

### TODOs in .tex files

| File | Count | In compiled paper? |
|------|-------|--------------------|
| paper/sections/background.tex | 6 TODO comments | No (not \input'd) |
| paper/sections/methods.tex | 6 TODO comments | No (not \input'd) |
| All other papers | 0 | - |

These are stale draft files from early development. Not in the compiled papers.

| Severity | INFO |
|----------|------|
| Fix | Delete background.tex and methods.tex or move to _archive/ |

### Legacy path references

paper/supplementary.tex line 927 references:
`Core library (src/browntone/)`

The canonical instructions state: src/browntone/ is LEGACY. Use src/analytical/.

| Severity | WARNING |
|----------|---------|
| Fix | Update supplementary.tex to reference src/analytical/ |

### Stale v1 values
No instances of eta=0.30, ka=0.017, or R_eq=0.133 found. OK

### Placeholder values
No instances of TBD, XX, or ??? found. OK

---

## 10. Paper 2 Placeholder Content (WARNING)

Paper 2 contains placeholder text that must be filled before submission:

| Location | Content |
|----------|---------|
| Line 58 | [Authors] |
| Line 59 | [Affiliations] |
| Line 60 | [email] |
| Line 815 | [To be added.] (Acknowledgements) |
| Line 818 | [repository URL] (Data availability) |

| Severity | WARNING |
|----------|---------|
| Fix | Fill in author/affiliation metadata and repository URL before submission |

---

## 11. Contradictions Check

No outright contradictions found between papers. All papers agree on:
- Breathing mode irrelevant to infrasound OK
- Flexural modes at 4-10 Hz (abdomen) OK
- Airborne coupling negligible via (ka)^n penalty OK
- Mechanical vibration dominant by orders of magnitude OK
- Energy-consistent displacement ~0.014 um at 120 dB OK

Paper 2's 35-100x more efficient than airborne flexural coupling claim
is internally consistent: gas pocket displacement 0.5-1.3 um vs cavity
displacement 0.014 um gives factor of 36-93x. OK

**Verdict: PASS** - No contradictions found.

---

## Issue Tracker Summary

| # | Severity | Paper | Issue |
|---|----------|-------|-------|
| 1 | CRITICAL | Paper 2 | No formal citation of Paper 1 (no bib entry) |
| 2 | CRITICAL | Bladder | 3 figure files missing (paper/figures/ directory absent) |
| 3 | CRITICAL | Paper 1 | Section 2 R ~ 10^3-10^4 conflicts with Section 4 R = 6.6e4 |
| 4 | WARNING | Paper 3 | Coupling ratio R redefined as 1/(ka)^2 vs Paper 1's xi_mech/xi_air |
| 5 | WARNING | Paper 3/Bladder | Inconsistent citation year for Paper 1 (2026 vs 2025) |
| 6 | WARNING | Paper 1 | Supplementary references legacy src/browntone/ path |
| 7 | WARNING | Paper 2 | Placeholder author/affiliation/URL metadata unfilled |
| 8 | WARNING | Paper 1 | Discussion and conclusion use 10^3-10^4 for a baseline of 6.6e4 |
| 9 | WARNING | Paper 1 | Breathing mode ~2500 Hz in paper vs ~2490 Hz in canonical |
| 10 | WARNING | Paper 2 | Draft watermark still present |
| 11 | INFO | Paper 1 | Stale background.tex and methods.tex with 12 TODOs (not compiled) |
| 12 | INFO | Paper 1 | f2 reported as 4.0 Hz (rounded) vs canonical 3.95 Hz |
| 13 | INFO | Paper 3 | f2 reported as 3.9 Hz (rounded differently from Paper 1's 4.0) |
| 14 | INFO | Paper 2 | Uses c_f=1540 m/s (tissue) while Paper 1 uses K_f=2.2 GPa (water) |

---

## Prioritised Action Items

1. [CRITICAL] Add Paper 1 citation to Paper 2's references.bib - required before JASA submission
2. [CRITICAL] Generate 3 missing bladder paper figures or update references
3. [CRITICAL] Fix Section 2 coupling ratio range - change 10^3-10^4 to ~10^4 or 10^4-10^5
4. [HIGH] Standardise Paper 1 citation key/year - use Mace2025browntone and year 2025 in Paper 3
5. [HIGH] Distinguish coupling ratio symbols in Paper 3 from Paper 1 definition
6. [MEDIUM] Fill Paper 2 placeholder metadata - authors, affiliations, URLs
7. [LOW] Update supplementary.tex legacy path - src/browntone/ to src/analytical/
8. [LOW] Clean up stale .tex files - delete or archive background.tex, methods.tex

---

*Audit performed by Consistency Auditor agent. Code validated against
src/analytical/natural_frequency_v2.py and src/analytical/energy_budget.py.*
