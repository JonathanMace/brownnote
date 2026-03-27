# Paper 2 Consistency Audit — 2026-03-27

**Author**: consistency-auditor
**Branch**: gas-pocket-audit
**PR**: (pending)

## Summary

Full consistency audit of Paper 2 (gas pockets / JASA draft) covering parameter
agreement between `main.tex`, `gas_pocket_detailed.py`, and `gas_pocket_resonance.py`;
verification of every numerical claim in the paper against code output; citation
completeness; and cross-referencing with Paper 1 canonical values. Numerous
discrepancies found, including a table of frequencies that does not match the current
code output and several quantitative claims that disagree with computed values.

## Key Findings

- **Table 2 frequencies are wrong.** Spherical constrained f₀ values in the paper
  (1014, 610, 492, 399, 299, 243 Hz) disagree with code output
  (5503, 2623, 1894, 1362, 877, 627 Hz) by factors of 2–5×.
- **Cylindrical f₀ = 443 Hz in the table matches neither the radial mode (1307 Hz)
  nor the axial mode (31–308 Hz).** The axial mode is volume-dependent but the table
  shows a constant value.
- **Paper claims "all frequencies exceed 100 Hz"** (§3.1, L284). The code gives
  f₀ = 31 Hz for a 100 mL cylindrical pocket (axial mode). This is *within* the
  infrasound range and contradicts the claim.
- **100 mL spherical displacement at 120 dB: paper says ~1.8 µm, code gives 1.34 µm**
  (34 % overestimate in paper).
- **Cylindrical SPL threshold: paper says ~118 dB, code gives ~113 dB** (5 dB error).
- **Population range: paper says 0.6–3.5 µm, code gives 1.05–2.36 µm.** Lower bound
  is 75 % too low, upper bound is 48 % too high.
- **Breathing mode of abdomen: paper says ~2900 Hz (§1, L121), Paper 1 canonical is
  ~2490 Hz.** A 16 % error in a cross-referenced quantity.
- **Figure 4 comparison uses five stale Paper 1 parameters**, making the whole-cavity
  displacement estimate unreliable.
- **Table 1 states ρ_f = 1050 kg/m³ but the Minnaert values in Table 2 were computed
  with ρ_f = 1020** (Paper 1 canonical), creating an internal inconsistency.

## Detailed Audit

### A. Parameter Consistency

#### A1. Table 1 (paper) vs `gas_pocket_detailed.py` constants

| Parameter | Table 1 | Code (`detailed.py`) | Match? |
|-----------|---------|---------------------|--------|
| γ         | 1.4     | 1.4                 | ✓      |
| P₀        | 101 325 Pa | 101 325 Pa       | ✓      |
| ρ_f       | 1050    | 1050                | ✓      |
| E_w       | 10 kPa  | 10 kPa              | ✓      |
| ν_w       | 0.45    | 0.45                | ✓      |
| h_w       | 3 mm    | 3 mm                | ✓      |
| ρ_w       | 1040    | 1040                | ✓      |
| c_f       | 1540 m/s| 1540 m/s            | ✓      |
| μ         | 1e-3    | 1e-3                | ✓      |
| R_lumen   | 15 mm   | 15 mm               | ✓      |

Table 1 and `gas_pocket_detailed.py` are self-consistent. ✓

#### A2. `gas_pocket_resonance.py` vs `gas_pocket_detailed.py`

| Parameter   | `resonance.py`  | `detailed.py` | Paper | Issue |
|-------------|-----------------|---------------|-------|-------|
| ρ_fluid     | **1040**        | 1050          | 1050  | **MISMATCH** — resonance.py is stale |
| δ_th        | **0.05**        | 0.04          | ≈0.04 | **MISMATCH** — resonance.py is stale |
| δ_wall      | **not included**| 0.3           | ≈0.3  | **MISSING** in resonance.py |
| wall model  | ad-hoc k,m     | thin-shell    | thin-shell | Different formulations |

#### A3. Paper Table 2 Minnaert values computed with wrong ρ_f

The Minnaert frequencies in Table 2 match ρ_f = 1020 (Paper 1 canonical), **not**
the ρ_f = 1050 stated in Table 1:

| V (mL) | f_M (Table 2) | f_M (ρ=1020) | f_M (ρ=1050) |
|---------|---------------|---------------|---------------|
| 1       | 524           | **524**       | 517           |
| 5       | 307           | **306**       | 302           |
| 10      | 244           | **243**       | 240           |
| 100     | 113           | **113**       | 111           |

**Verdict:** Table 2 was computed with ρ_f = 1020; Table 1 says 1050.

#### A4. Figure 4: stale Paper 1 parameters in `generate_figures.py`

| Parameter | Fig 4 value | Paper 1 canonical | Error |
|-----------|-------------|-------------------|-------|
| R_abd     | 0.16 m      | 0.157 m (R_eq)    | +2 %  |
| h_abd     | **0.02 m**  | 0.01 m            | **+100 %** |
| Q         | **5.0**     | 4.0               | **+25 %** |
| P_iap     | **1500 Pa** | 1000 Pa           | **+50 %** |
| f_n2      | **4.5 Hz**  | 3.95 Hz           | **+14 %** |

Five of five Paper 1 parameters are wrong, and h is doubled.
This invalidates the whole-cavity displacement curve in Figure 4 and any
ratio comparison built on it.

---

### B. Code–Paper Numerical Verification

#### B1. Table 2: constrained f₀ (spherical, elastic wall)

| V (mL) | Paper f₀ | Code f₀ | Ratio (code/paper) |
|---------|----------|---------|-------------------|
| 1       | 1014     | 5503    | 5.4×              |
| 5       | 610      | 2623    | 4.3×              |
| 10      | 492      | 1894    | 3.9×              |
| 20      | 399      | 1362    | 3.4×              |
| 50      | 299      | 877     | 2.9×              |
| 100     | 243      | 627     | 2.6×              |

**CRITICAL:** The table is completely inconsistent with the code.
Either the code was modified after the table was typeset, or the table
was computed by hand with different wall-stiffness formulas.

#### B2. Table 2: cylindrical f₀

Paper shows f₀ = 443 Hz for all cylindrical entries (10, 50, 100 mL).
Code gives:

| V (mL) | f_rad (code) | f_ax (code) | f₀ = min | Paper |
|---------|-------------|-------------|----------|-------|
| 10      | 1307        | 97          | **97**   | 443   |
| 50      | 1307        | 44          | **44**   | 443   |
| 100     | 1307        | 31          | **31**   | 443   |

443 Hz does not match either mode. The axial mode gives *much lower*
frequencies — 31 Hz for 100 mL, which is borderline infrasound.

#### B3. SPL thresholds (0.5 µm at 7 Hz)

| Pocket           | Paper claim  | Code result | Δ      |
|------------------|-------------|-------------|--------|
| 5 mL spherical   | ~120 dB     | 120.2 dB    | ✓      |
| 100 mL spherical | ~111 dB     | 111.4 dB    | ✓      |
| 9 dB range       | 9 dB        | 8.8 dB      | ✓      |
| Cylindrical      | **~118 dB** | 113.1–113.5 | **−5 dB** |

Spherical thresholds agree. Cylindrical threshold is wrong in the paper
by ~5 dB.

#### B4. Displacement at 120 dB, 7 Hz

| Pocket            | Paper claim | Code result | Error  |
|-------------------|-------------|-------------|--------|
| 100 mL sph        | **~1.8 µm**| 1.34 µm     | **+34%** |
| Whole-cavity n=2   | **~10⁻⁴ µm** | 0.014 µm (Paper 1 canonical) | **~140× discrepancy** |

The paper claims whole-cavity displacement is ~10⁻⁴ µm at 120 dB.
Paper 1's canonical energy-consistent value is 0.014 µm — 140× larger.
The "7–10× more efficient" comparison ratio is therefore unreliable.

#### B5. Population Monte Carlo

| Metric          | Paper claim    | Code result (N=1000) | Match? |
|-----------------|---------------|---------------------|--------|
| 100 % > 0.5 µm | 100 %         | 100 %               | ✓      |
| Median          | ~1.2 µm       | 1.08 µm             | ~OK    |
| Range           | **0.6–3.5 µm**| 1.05–2.36 µm        | **✗**  |

The 100 % claim holds, but the stated range is wrong.
The minimum displacement (1.05 µm) is well above 0.5 µm because 70 %
of pockets are cylindrical with ξ ≈ 1.05 µm regardless of volume.

---

### C. Cross-Reference with Paper 1

| Quantity             | Paper 2 claim | Paper 1 canonical | Match? |
|----------------------|---------------|-------------------|--------|
| Breathing mode freq  | **~2900 Hz**  | ~2490 Hz          | **✗** (16 % error) |
| Flexural n=2 freq    | 4–10 Hz       | 3.95 Hz           | ✓ (within range) |
| Energy-consistent ξ  | **~10⁻⁴ µm** | 0.014 µm          | **✗** (140× error) |
| ka coupling          | mentioned     | 0.0114            | Not stated numerically |

---

### D. Citation Audit

All 21 `\citep{}` / `\citet{}` calls in `main.tex` resolve to entries in
`references.bib`. ✓

**Orphan bib entries** (in `.bib` but not cited):
Plesset1977, Prosperetti1988, Commander1989, Kitazaki1998, Griffin1990,
Iovino2006, iso2631 — 7 entries. Minor; typical for a draft.

---

### E. Stale / Placeholder Content

| Item | Location | Status |
|------|----------|--------|
| `[Authors]` | L58 | Placeholder — expected for first draft |
| `[Affiliations]` | L59 | Placeholder |
| `[email]` | L60 | Placeholder |
| `[To be added.]` | L699 (acknowledgements) | Placeholder |
| `[repository URL]` | L702 (data availability) | Placeholder |
| DRAFT watermark | L34–38 | Intentional for draft |
| `\documentclass[12pt]{article}` | L5 | Not JASA format — expected pre-submission |

---

## Issues Identified

### CRITICAL (would produce incorrect results if published)

1. **Table 2 spherical f₀ values are 2.6–5.4× too low** compared to
   `constrained_sphere_frequency()` output.
   Severity: CRITICAL. Location: `main.tex` L456–461.

2. **Table 2 cylindrical f₀ = 443 Hz is fictional** — matches neither the
   radial (1307 Hz) nor axial (31–308 Hz) mode from `gas_pocket_detailed.py`.
   Severity: CRITICAL. Location: `main.tex` L462–464.

3. **"All frequencies exceed 100 Hz" is false.** Cylindrical axial modes for
   V ≥ 10 mL are below 100 Hz; at V = 100 mL, f₀ = 31 Hz, which is barely
   above the infrasound range. This fundamentally changes the "sub-resonant"
   narrative for large cylindrical pockets.
   Severity: CRITICAL. Location: `main.tex` L282–286.

4. **Whole-cavity displacement "~10⁻⁴ µm" contradicts Paper 1 canonical
   value of 0.014 µm** — the ratio is 140×, not a rounding difference.
   The "7–10× more efficient" claim depends on this comparison and is
   therefore unreliable.
   Severity: CRITICAL. Location: `main.tex` L545–548, Fig 4.

5. **Figure 4 uses five wrong Paper 1 parameters** (h doubled, Q +25 %,
   P_iap +50 %, f₂ +14 %, R +2 %). The whole-cavity curve is invalid.
   Severity: CRITICAL. Location: `generate_figures.py` L316–332.

### MAJOR (quantitative errors in text)

6. **Breathing mode ~2900 Hz should be ~2490 Hz** (Paper 1 canonical).
   Severity: MAJOR. Location: `main.tex` L121.

7. **100 mL displacement ~1.8 µm should be ~1.34 µm** (+34 % error).
   Severity: MAJOR. Location: `main.tex` L548.

8. **Cylindrical SPL threshold ~118 dB should be ~113 dB** (−5 dB error).
   Severity: MAJOR. Location: `main.tex` L482–483.

9. **Population displacement range 0.6–3.5 µm should be ~1.05–2.36 µm.**
   Severity: MAJOR. Location: `main.tex` L513–514.

10. **Table 2 Minnaert frequencies computed with ρ_f = 1020** but Table 1
    states ρ_f = 1050. Internal inconsistency.
    Severity: MAJOR. Location: `main.tex` L196 vs L454–464.

### MINOR

11. **`gas_pocket_resonance.py` uses ρ_f = 1040** (neither 1050 nor 1020).
    Severity: MINOR. Location: `gas_pocket_resonance.py` L56.

12. **Thermal damping δ_th = 0.05 in `resonance.py`** vs 0.04 in
    `detailed.py` and paper.
    Severity: MINOR. Location: `gas_pocket_resonance.py` L173.

13. **`gas_pocket_resonance.py` omits wall structural damping** (δ_wall = 0.3
    in detailed.py and paper).
    Severity: MINOR. Location: `gas_pocket_resonance.py` L168–178.

14. **Seven orphan bib entries** not cited in paper.
    Severity: MINOR. Location: `references.bib`.

15. **Placeholder text** for authors, affiliations, acknowledgements.
    Severity: MINOR (expected for first draft).

## Changes Made

- No code or paper changes made. This is a read-only audit.

## Next Steps

1. **Regenerate Table 2** by running the actual code and pasting the output.
   Decide whether the cylindrical "lowest frequency" should include the
   axial mode (it should, per the formula in §2.2).
2. **Reconcile ρ_f**: choose 1050 (intestinal context) or 1020 (Paper 1
   context) and use it consistently everywhere.
3. **Fix Figure 4**: update `generate_figures.py` L316–332 to use Paper 1
   canonical values (R_eq=0.157, h=0.01, Q=4.0, P_iap=1000, f₂=3.95).
4. **Update the "7–10×" claim** after fixing the whole-cavity comparison.
   The actual ratio may be much larger or much smaller.
5. **Fix breathing mode frequency** in introduction: 2900 → 2490 Hz.
6. **Rethink the "sub-resonant" narrative** for cylindrical pockets: at
   100 mL, the axial resonance is 31 Hz, so a 7 Hz drive gives r ≈ 0.23,
   which is not deeply sub-resonant. This could be a feature (partial
   amplification), not a bug.
7. **Sync `gas_pocket_resonance.py`** parameters with `gas_pocket_detailed.py`
   or deprecate the older module.
8. **Run the Monte Carlo at full N=10,000** and update the range/median
   claims to match.
