# Reviewer B — Round 4 (Paper 7)

**Paper:** "Can You Hear the Ripeness? Non-Destructive Acoustic Assessment of Fruit Maturity via Equivalent-Sphere Shell Resonance Inversion"

**Date:** 2026-03-30

## Decision: MINOR REVISION

---

## Verification of R3 Minor Issues

### R3-M1: Π_ripe equation had wrong density form — **FIXED** ✓

The formulation now cleanly separates two density quantities (§2.2, formulation.tex lines 114–131):

- **Eq. (4):** ρ_eff = ρ_w h + ρ_f R_eq / n — mass per unit area [kg/m²], used in the eigenfrequency Eq. (8)
- **Eq. (5):** ρ̃_eff = ρ_w h / R_eq + ρ_f — volumetric effective density [kg/m³], used in Π_ripe

The Π_ripe definition (Eq. 11) now correctly uses ρ̃_eff:

    Π_ripe = f₂ R_eq √(ρ̃_eff / E_rind)

Verified dimensionally: [Hz]·[m]·[kg/m³ / Pa]^(1/2) = [s⁻¹]·[m]·[s/m] = dimensionless. ✓

Verified numerically: code (watermelon_model.py, lines 353–354) computes `rho_eff = rho_rind * h / R_eq + rho_flesh`, which matches Eq. (5). Output values (0.0601–0.0655) match Table 5 exactly. ✓

### R3-M2: "negligible error" unsupported — **FIXED** ✓

The limitations section (discussion.tex, line 92) now reads: "introduces an error of **unquantified magnitude** in the predicted tap-tone frequency." This is honest. The preceding text (lines 88–91) correctly states that two watermelons with the same R_eq but different ζ get identical predicted frequencies — a frank admission that the model has zero shape sensitivity. Lines 93–99 identify the Ritz variational extension as future work. This is exactly the candour I demanded.

### R3-M3: Overclaiming in discussion — **MOSTLY FIXED** ✓

Overstatements have been removed throughout. However, one instance remains: discussion.tex line 194:

> "This positions the framework as a *unified theory of percussive produce assessment*."

The italics signal tongue-in-cheek intent, and I recognise this paper has a lighter tone than most JSV submissions. I will not insist on removal, but note that this claim is unsupported: the model has been applied to exactly one species (watermelon), with validation showing 50% of cases outside published ranges (see below). At minimum, I suggest qualifying this as aspirational rather than established.

---

## Equivalent-Sphere Framing: Honesty Assessment

**Verdict: Exemplary.** The reframe is thorough, consistent, and appears in every relevant location:

| Location | Statement | Line(s) |
|----------|-----------|---------|
| Abstract | "equivalent-sphere approximation" | main.tex 73–76 |
| §2.1 title | "Equivalent-sphere shell model" | formulation.tex 7 |
| §2.1 body | "the frequency equation is that of a spherical shell of radius R_eq" | formulation.tex 24–32 |
| §2.2 | "no explicit dependence on the aspect ratio ζ" | formulation.tex 169–172 |
| §5.3 Limitations | "does not include explicit curvature corrections" | discussion.tex 82–99 |
| §6 Conclusions | "zero sensitivity to aspect ratio at constant R_eq" | conclusion.tex 45–50 |

I independently confirmed this: sweeping ζ from 0.50 to 0.95 at constant R_eq = 0.1453 m produces f₂ = 89.9 Hz in all cases. The model is exactly invariant, as the paper claims. The formulation (§2.1, lines 46–55) correctly distinguishes the *size* effect (varying R_eq via ζ) from the *shape* effect (curvature anisotropy at fixed R_eq), which is absent. This is a model I can trust.

---

## Dimensional Consistency Check

All equations verified:

| Equation | Expression | Units | Correct? |
|----------|------------|-------|----------|
| (1) R_eq | (a²c)^(1/3) | m | ✓ |
| (4) ρ_eff | ρ_w h + ρ_f R/n | kg/m² | ✓ |
| (5) ρ̃_eff | ρ_w h/R + ρ_f | kg/m³ | ✓ |
| (6) K_bend | n(n−1)(n+2)² h³ E / [12(1−ν²) R⁴] | Pa (N/m²) ÷ m² = kg/(m²·s²) ÷ m² | ✓ (*) |
| (7) K_memb | (h/R²) λ_n E | same | ✓ |
| (8) K_prestress | (P/R)(n−1)(n+2) | Pa/m = kg/(m²·s²) | ✓ |
| (9) f_n² | K_n / (4π² ρ_eff) | [kg/(m²·s²)] / [kg/m²] = Hz² | ✓ |
| (10) Inversion | (ω² m_eff − K_prestress) / (coeff_bend + coeff_memb) | Pa | ✓ |
| (11) Π_ripe | f₂ R_eq √(ρ̃_eff / E) | dimensionless | ✓ |

(*) Note: K_bend, K_memb, K_prestress have units of stiffness per unit area, consistent with m_eff being mass per unit area. The ω² = K/m_eff formulation is self-consistent.

---

## Π_ripe: Code–Paper Consistency

| Cultivar | Paper Table 5 | Code output | Match? |
|----------|---------------|-------------|--------|
| Crimson Sweet (ripe) | 0.0601 | 0.0601 | ✓ |
| Sugar Baby (ripe) | 0.0654 | 0.0654 | ✓ |
| Charleston Gray (ripe) | 0.0620 | 0.0620 | ✓ |
| Seedless Tri-X 313 (ripe) | 0.0607 | 0.0607 | ✓ |

Paper claims: mean = 0.062, CoV = 3.3%, max deviation = 5.4%.
Computed: mean = 0.0621, CoV = 3.3%, max deviation = 5.4%. **Exact match.** ✓

Per-cultivar invariance across E (fixed geometry): CoV < 0.03% — confirming E cancellation by construction. ✓

---

## Forward Model and Inversion Consistency

| Stage | Paper f₂ (Hz) | Code f₂ (Hz) | Paper Q | Code Q | Match? |
|-------|---------------|---------------|---------|--------|--------|
| Unripe | 203.2 | 203.2 | 12.5 | 12.5 | ✓ |
| Turning | 146.7 | 146.7 | 9.1 | 9.1 | ✓ |
| Ripe | 89.9 | 89.9 | 6.7 | 6.7 | ✓ |
| Overripe | 46.4 | 46.4 | 5.0 | 5.0 | ✓ |

α = 161.5 Hz²/MPa (paper Eq. 10) vs 161.5 Hz²/MPa (code). ✓

Inversion round-trip error: 0.0000% for all four stages (exact to machine precision). ✓

---

## Fatal Flaws

**None.**

All four original fatal flaws (F1: model framing, F2: dimensional inconsistency, F3: bogus validation, F4: Π_ripe tautology) have been resolved. The paper is internally consistent between text, tables, equations, and code.

---

## Major Issues

**None remaining.**

---

## Minor Issues

### M1. Yamamoto validation: "overlaps well" is generous (validation.tex, lines 53–66)

The validation shows 3 of 6 cases outside Yamamoto's published ranges:

| Case | f₂_model (Hz) | Published range (Hz) | Deviation |
|------|---------------|---------------------|-----------|
| Small, ripe | 132 | 80–120 | +12 Hz above |
| Small, unripe | 244 | 120–180 | +64 Hz above |
| Medium, unripe | 192 | 120–180 | +12 Hz above |

The paper discusses these honestly (lines 56–66) but the opening characterisation at line 53 — "overlaps well" — is misleading given a 50% hit rate. Suggest replacing with "partially overlaps" or "shows qualitative agreement, with quantitative discrepancies for the smallest and stiffest specimens."

### M2. TODO comments in references.bib (lines 157, 168, 178, 189, 201, 212)

Six bibliographic entries have TODO comments indicating unverified metadata (authors, titles, pages). These must be verified before submission. Example:

> `% TODO: verify author list, journal, volume, and page range.` (line 157, Stone1996)

### M3. Sobol N_base: code default ≠ paper value

The paper (results.tex, line 93) states N_base = 512 (→ 5,632 evaluations). The code (watermelon_model.py, line 468) defaults to N_base = 2048 (→ 22,528 evaluations). Anyone reproducing with default code parameters will get a different analysis. Suggest either: (a) changing the code default to 512, or (b) documenting the N_base = 512 explicitly in the code's Sobol function docstring.

### M4. Uncited abdominal α claim (discussion.tex, lines 67–70)

> "The corresponding constant for the human abdomen is approximately 155 Hz²/MPa when expressed in the same dimensionless form"

This numerical value is presented without citation or derivation. Either cite the specific companion paper and equation from which it derives, or remove the comparison.

### M5. Sadrnia2006 bib key year mismatch (references.bib, lines 145–152)

The bib key is `Sadrnia2006` but the `year` field reads `2008`, and the actual publication (Journal of Food Engineering) is from 2008. The citing text (formulation.tex, line 69) attributes it to 2006. Fix the key or the year.

---

## Positive Comments

1. **The equivalent-sphere reframe is the best I have seen in this review cycle.** Every section that touches the model's geometric assumptions now includes an explicit, accurate caveat. The distinction between size effects (via R_eq) and shape effects (absent) is crisp and pedagogically valuable (formulation.tex, lines 46–55).

2. **The dual-density notation is clean.** Introducing ρ_eff for mass/area and ρ̃_eff for volumetric density, with explicit unit annotations (formulation.tex, lines 114–131), resolves the dimensional confusion from earlier rounds without cluttering the notation.

3. **The inversion self-consistency is exact** (round-trip error < 10⁻¹² relative). This is what a closed-form inversion should deliver.

4. **The Sobol analysis is now properly documented** with confidence intervals, calc_second_order specification, and correct evaluation counts.

5. **The Π_ripe interpretation has been correctly narrowed** to a geometric invariant (not a "ripeness parameter"), with the caveat that it varies when h changes during ripening. This is scientifically precise.

6. **The limitations section is among the most honest I've reviewed.** Six explicit limitations, each with a quantitative or qualitative bound. The admission that the equivalent-sphere error is "of unquantified magnitude" (discussion.tex, line 92) is exactly right — better to admit ignorance than to hand-wave.

7. **Code–paper consistency is perfect.** Every number in every table matches the code output to the precision reported. This level of reproducibility is rare and commendable.

---

## Summary

This paper has undergone a remarkable transformation across four rounds of review. The original submission had four fatal flaws (spherical model mislabelled as oblate, dimensional inconsistencies, bogus validation function, and tautological Π_ripe). All four have been comprehensively resolved.

The current manuscript is technically sound, dimensionally correct, internally consistent, and refreshingly honest about its limitations. The equivalent-sphere framing is exemplary — it says exactly what the model does and does not capture, and explains why the approximation is sufficient for the inversion application.

Five minor issues remain, all fixable in a single revision pass: the generous characterisation of the Yamamoto comparison, unverified bibliography entries, a code/paper default mismatch, one uncited numerical claim, and a bib key typo. None of these affect the scientific conclusions.

**Recommendation: MINOR REVISION.** Address M1–M5 and this paper is ready for publication.
