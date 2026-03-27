# Paper 2 Consistency Audit Report — 2026-03-27T0900

## Overall: 3 CRITICAL, 4 WARNING, 17 PASS

---

## 1. Parameter Mismatches

### CRITICAL

| Location | Expected | Found | Severity |
|----------|----------|-------|----------|
| src/analytical/gas_pocket_resonance.py line 56 | ho_fluid = 1020 (canonical) | ho_fluid = 1040 | **CRITICAL** — stale non-canonical value |

### PASS — Paper 2 Table 1 Parameters

Paper 2 models *intestinal wall* (not the abdominal wall), so its parameters are intentionally
different from the Paper 1 canonical set. All values in Table 1 (`tab:params`) match the
code defaults in `gas_pocket_detailed.py` exactly:

| Symbol | Paper (Table 1) | Code | Match? |
|--------|----------------|------|--------|
| `gamma` | 1.4 | 1.4 | PASS |
| `P0` | 101 325 Pa | 101 325 Pa | PASS |
| `rho_f` | 1020 kg/m³ | 1020 kg/m³ | PASS |
| `E_w` | 10 kPa | 10 000 Pa | PASS |
| `nu_w` | 0.45 | 0.45 | PASS |
| `h_w` | 3 mm | 0.003 m | PASS |
| `rho_w` | 1040 kg/m³ | 1040 kg/m³ | PASS |
| `c_f` | 1540 m/s | 1540 m/s | PASS |
| `mu` | 1e-3 Pa·s | 1e-3 Pa·s | PASS |
| `R` | 15 mm | 0.015 m | PASS |

---

## 2. Cross-Table Consistency (Table 2: Resonance Frequencies)

### PASS — All values match code output exactly

| V [mL] | Geometry | Paper a/R [mm] | Code a/R [mm] | Paper f_M [Hz] | Code f_M [Hz] | Paper f0 [Hz] | Code f0 [Hz] |
|---------|----------|---------------|---------------|----------------|----------------|---------------|--------------|
| 1 | Spherical | 6.2 | 6.2 | 524 | 524 | 5556 | 5556 |
| 5 | Spherical | 10.6 | 10.6 | 306 | 306 | 2653 | 2653 |
| 10 | Spherical | 13.4 | 13.4 | 243 | 243 | 1916 | 1916 |
| 20 | Spherical | 16.8 | 16.8 | 193 | 193 | 1379 | 1379 |
| 50 | Spherical | 22.9 | 22.9 | 142 | 142 | 889 | 889 |
| 100 | Spherical | 28.8 | 28.8 | 113 | 113 | 635 | 635 |
| 10 | Cylindrical | 15.0 | 15.0 | --- | --- | 99 | 99 |
| 50 | Cylindrical | 15.0 | 15.0 | --- | --- | 44 | 44 |
| 100 | Cylindrical | 15.0 | 15.0 | --- | --- | 31 | 31 |

Footnote claims cylindrical radial mode is ~1323 Hz; code gives 1323 Hz. **PASS**.

---

## 3. Code-Paper Discrepancies

### CRITICAL — Cylindrical SPL Threshold: Paper says ~118 dB, Code gives ~113.5 dB

**Location:** Section 4.2 (`sec:res_spl`), line 488.  
**Paper text:** *"For cylindrical pockets, the threshold is nearly independent of
volume (~118 dB)"*  
**Code output (binary search for 0.5 µm at 7 Hz):**

| Volume | Geometry | Code SPL threshold |
|--------|----------|--------------------|
| 5 mL | cylindrical | 113.6 dB |
| 10 mL | cylindrical | 113.5 dB |
| 50 mL | cylindrical | 113.4 dB |
| 100 mL | cylindrical | 113.2 dB |

The paper overstates the cylindrical threshold by ~4.5 dB. This propagates to the
"9-dB range" claim in the same section; the actual range (spherical 5 mL at 120.2 dB to
cylindrical at 113.5 dB) is only about 7 dB, not 9 dB.  
**Recommendation:** Update the ~118 dB claim to ~114 dB, and the 9-dB range to ~7 dB.

### CRITICAL — Monte Carlo Displacement Range: Paper says 0.6–3.5 µm, Code gives 1.0–2.7 µm

**Location:** Section 4.3 (`sec:res_pop`), lines 518–519.  
**Paper text:** *"The distribution of maximum pocket-wall displacement spans approximately
0.6–3.5 µm, with a median of ~1.2 µm."*  
**Code output** (`population_gas_model(n_individuals=10000, seed=42)`):

| Metric | Paper claim | Code output | Discrepancy |
|--------|-------------|-------------|-------------|
| Minimum | 0.6 µm | 1.02 µm | 70% off |
| Maximum | 3.5 µm | 2.66 µm | 24% off |
| Median | ~1.2 µm | 1.08 µm | 11% off |
| 100% above 0.5 µm? | Yes | Yes (100%) | **PASS** |

The range is narrower than claimed. The minimum (1.02 µm) is well above the 0.5 µm
threshold, so the 100% claim still holds, but the stated range is wrong.  
**Recommendation:** Update to "1.0–2.7 µm, with a median of ~1.1 µm."

### WARNING — "50–100×" Efficiency Claim Understates Lower Bound

**Location:** Abstract (line 85), Section 4.4 (line 547), Conclusion (line 678).  
**Paper text:** *"50–100× more efficient than whole-cavity resonance"*  
**Code output** (ratio of gas-pocket displacement to whole-cavity 0.014 µm at 120 dB):

| Pocket | Ratio |
|--------|-------|
| 5 mL spherical | **35×** ← below 50 |
| 10 mL spherical | **44×** ← below 50 |
| 20 mL spherical | 56× |
| 50 mL spherical | 76× |
| 100 mL spherical | 96× |
| 10–100 mL cylindrical | 75–79× |

For small spherical pockets (5–10 mL), the ratio drops below 50×. The "50–100×" claim
holds for pockets ≥ 20 mL and all cylindrical pockets, but not universally.  
**Recommendation:** Qualify as "50–100× for typical pocket sizes (≥ 20 mL)" or widen
to "35–100×."

### PASS — Paper 1 Cross-Reference

Paper 2 cites whole-cavity ξ ≈ 0.014 µm at 120 dB; Paper 1 code gives 0.0137 µm.
Within rounding. **PASS** (1.8% off).

### PASS — 100 mL Displacement at 120 dB

Paper says ~1.3 µm; code gives 1.341 µm. **PASS** (3% rounding).

### PASS — SPL Thresholds (spherical)

| Volume | Paper | Code |
|--------|-------|------|
| 5 mL | ~120 dB | 120.2 dB |
| 100 mL | ~111 dB | 111.4 dB |

Both **PASS**.

### PASS — All Equations Match Code

Verified all key equations against `gas_pocket_detailed.py` implementation:

- Eq 3 (Minnaert): PASS
- Eq 4–5 (constrained sphere f0, stiffness, mass): PASS
- Eq 8 (cylindrical radial mode): PASS
- Eq 9 (cylindrical axial mode): PASS
- Eq 10 (damping components): PASS
- Eq 12 (frequency response H): PASS
- Eq 14 (k_eff spherical): PASS
- Eq 15 (k_eff cylindrical): PASS
- Eq 16 (SPL threshold): PASS

---

## 4. Citation Completeness

### PASS — No Missing Citations

All 21 `\cite` keys in `main.tex` have matching entries in `references.bib`.

### WARNING — 7 Unused Bibliography Entries

The following bib entries are defined but never cited:

| Key | Why it may be needed |
|-----|---------------------|
| Commander1989 | Bubble dynamics — could strengthen model justification |
| Griffin1990 | WBV handbook — could support discussion |
| Iovino2006 | GI sensitivity — could support clinical section |
| iso2631 | Vibration standard — could support occupational context |
| Kitazaki1998 | Seated resonance — marginal relevance |
| Plesset1977 | Bubble dynamics — foundational |
| Prosperetti1988 | Ambient noise — marginal relevance |

**Recommendation:** Either cite the relevant ones (Commander1989, Plesset1977, Iovino2006)
or remove them from the .bib to keep it clean.

---

## 5. Label/Reference Consistency

### PASS — No Undefined References

All `\ref{}` targets have matching `\label{}` definitions.

### WARNING — 31 Orphan Labels (defined but never `\ref`'d)

This is expected for a first draft (many section/equation labels are defined for future
cross-references). Key orphans that *should* be cross-referenced in the final version:

- `eq:minnaert`, `eq:f0_sphere`, `eq:f0_cyl_rad`, `eq:f0_cyl_ax` — the resonance
  equations are never referenced from the results section.
- `sec:damping`, `sec:forced`, `sec:coupling` — model subsections not cross-referenced.

**Recommendation:** Add cross-references in the Results section back to the relevant
model equations.

---

## 6. Figure Files

### PASS — All 4 Figures Exist

| Figure | File | Status |
|--------|------|--------|
| Fig 1 (schematic) | `figures/fig1_geometry_schematic.pdf` | EXISTS |
| Fig 2 (SPL threshold) | `figures/fig2_spl_threshold_vs_volume.pdf` | EXISTS |
| Fig 3 (population) | `figures/fig3_population_variability.pdf` | EXISTS |
| Fig 4 (comparison) | `figures/fig4_pathway_comparison.pdf` | EXISTS |

---

## 7. Stale Content

### PASS — No TODO/FIXME/XXX markers
### PASS — No stale v1 references
### PASS — No placeholder numbers (TBD, ???)

### WARNING — 4 Placeholder Text Fields (Expected for Working Draft)

- `[Authors]` (line 58)
- `[Affiliations]` (line 59)
- `[email]` (line 60)
- `[repository URL]` (line 708)

---

## 8. LaTeX Compilation

### PASS — Compiles Without Errors

Only font-size warnings (`T1/cmr/m/n in size 153.57` — from draft watermark).
No undefined references, no missing citations, no compilation errors.

---

## Summary

| Category | Critical | Warning | Pass |
|----------|----------|---------|------|
| Parameter consistency | 1 (gas_pocket_resonance.py rho_f) | 0 | 10 |
| Table accuracy | 0 | 0 | 1 |
| Code-paper agreement | 2 (cyl threshold, MC range) | 1 (50–100× bound) | 5 |
| Citations | 0 | 1 (unused entries) | 1 |
| Labels/refs | 0 | 1 (orphan labels) | 1 |
| Figures | 0 | 0 | 1 |
| Stale content | 0 | 1 (placeholders) | 3 |
| Compilation | 0 | 0 | 1 |
| **Total** | **3** | **4** | **23** |

### Action Items (Priority Order)

1. **[CRITICAL]** Fix cylindrical SPL threshold: change ~118 dB → ~114 dB in Section 4.2
2. **[CRITICAL]** Fix Monte Carlo range: change "0.6–3.5 µm, median ~1.2" → "1.0–2.7 µm, median ~1.1" in Section 4.3
3. **[CRITICAL]** Fix `gas_pocket_resonance.py` rho_fluid: 1040 → 1020
4. **[WARNING]** Qualify "50–100×" claim or widen to "35–100×" (abstract, Section 4.4, conclusion)
5. **[WARNING]** Cite or remove 7 unused bib entries
6. **[WARNING]** Add cross-references for orphan equation/section labels
7. **[WARNING]** Fill placeholders before submission
