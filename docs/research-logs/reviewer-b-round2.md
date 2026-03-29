# Reviewer B — Round 2

**Paper:** "Can You Feel the Bass? Quantitative Partition of Airborne and Structure-Borne Pathways for Sub-Bass Perception at Concert Sound Pressure Levels" (Paper 6)

**Round 1 reference:** `docs/research-logs/reviewer-b-round1.md`
**Fixes under review:** PR #183 (`687992f`)

---

## Decision: MINOR REVISION

---

## Status of Round 1 Issues

### F1 (FATAL, Round 1): Floor vibration dimensional error — **RESOLVED ✓**

The original formula `v = sqrt(P/(m·ω²))` had units of `m²/s` (not `m/s`). This
has been replaced by the correct damped-plate power-balance (SEA) formula:

```
v_floor = sqrt(P_floor / (2·ζ_floor·ω·m_floor))
```

**Verification performed:**

1. **Dimensional analysis** (methods.tex lines 217–223, code lines 607–609):
   Numerator `[W] = [kg·m²·s⁻³]`; denominator `[1]·[s⁻¹]·[kg] = [kg·s⁻¹]`;
   ratio `[m²·s⁻²]`; square root `[m·s⁻¹]`. ✓

2. **Hand calculation at 40 Hz / 115 dB** (test lines 314–336):
   - p_inc = 11.247 Pa, I = 0.1505 W/m², P_floor = 0.1505 W
   - ω = 251.33 rad/s, m = 20 000 kg
   - v = sqrt(0.1505 / (2 × 0.03 × 251.33 × 20000)) = 7.065×10⁻⁴ m/s
   - Code returns 7.065×10⁻⁴ m/s. **Exact match.** ✓

3. **Physical consequence**: Floor displacement = 5.06 μm at 40 Hz / 115 dB,
   which is 9.04× the perception threshold. This is physically credible for
   a concrete floor in a concert venue and is consistent with the SEA literature.

4. **Test coverage**: 10 dedicated tests (class `TestFloorVibrationDisplacement`),
   including hand-calculation regression, damping scaling as 1/√ζ, and
   threshold exceedance. All 66 tests pass.

**Verdict: Fully fixed. The dimensional error was the paper's fatal flaw and is now corrected with a well-sourced formula.**

---

### M1 (Round 1): Table 3 data integrity — **RESOLVED ✓**

Table 3 (results.tex lines 110–137) now shows per-frequency SPL values interpolated
from the EDM third-octave spectrum, not a constant 115 dB. I regenerated all six
rows from the code and confirmed exact matches:

| f (Hz) | Paper SPL | Code SPL | Paper ξ_floor (μm) | Code ξ_floor (μm) | Match |
|--------|-----------|----------|---------------------|---------------------|-------|
| 20     | 100       | 100      | 2.54                | 2.54                | ✓     |
| 31.5   | 112       | 112      | 5.13                | 5.13                | ✓     |
| 40     | 115       | 115      | 5.06                | 5.06                | ✓     |
| 50     | 114       | 114      | 3.23                | 3.23                | ✓     |
| 63     | 110       | 110      | 1.44                | 1.44                | ✓     |
| 80     | 106       | 106      | 0.63                | 0.63                | ✓     |

All ka, ξ_air, ξ_thresh, and ξ_floor/ξ_thresh columns also match to the
precision reported in the table. **Fully fixed.**

---

### M2 (Round 1): Eq. 3 coupling prefactors — **RESOLVED ✓**

Methods §2.2 (lines 57–70) now explicitly states α₂ = 5/3, explains that it is
absorbed into the energy-consistent calibration (Eq. 8), and bounds the residual
error at <5% for n ≤ 4 in the long-wavelength regime (ka < 0.25). The code
correctly uses the energy-consistent on-resonance displacement as the reference
point, so the prefactor cancels in the off-resonance ka-ratio scaling
(Eq. 9: `(ka(f)/ka(f_n))^n`). This is technically sound. **Fully fixed.**

---

### M3 (Round 1): ISO 2631 thresholds not directly from standard — **RESOLVED ✓**

Methods §2.7 (lines 247–267) now explicitly states that the thresholds are
"interpolated from the frequency-weighted comfort boundaries in Griffin [1990]
and Mansfield [2005], which themselves are based on experimental data underlying
ISO 2631-1" and assigns ±3 dB uncertainty. The conversion formula (Eq. 12) is
verified: ξ_peak = a_rms·√2 / ω². Limitations §4.7 item 6 reiterates this.
**Fully fixed.**

---

### M4 (Round 1): No uncertainty quantification — **RESOLVED ✓**

Full Monte Carlo analysis implemented (`monte_carlo_pathway_uq`, code lines
831–925) with N = 10,000 samples. Three parameters varied: E (±50%, uniform),
ζ_floor ([0.02, 0.05], uniform), SPL (±3 dB, uniform). Results at 10K samples:

| Quantity               | Paper (Table 5) | Code (10K, seed=42) | Match |
|------------------------|-----------------|---------------------|-------|
| Floor/airborne p5      | 2040            | 2040                | ✓     |
| Floor/airborne p50     | 2390            | 2393                | ✓     |
| Floor/airborne p95     | 3060            | 3062                | ✓     |
| Floor/threshold p5 (%) | 575             | 575                 | ✓     |
| Floor/threshold p50 (%)| 853             | 853                 | ✓     |
| Floor/threshold p95 (%)| 1265            | 1265                | ✓     |
| Air/threshold p5 (%)   | 0.25            | 0.25                | ✓     |
| Air/threshold p50 (%)  | 0.35            | 0.35                | ✓     |
| Air/threshold p95 (%)  | 0.48            | 0.48                | ✓     |

Test coverage: 4 dedicated tests (class `TestMonteCarloUQ`), including
reproducibility with seed, floor-always-dominates, and spread sensitivity.
**Fully fixed.**

---

### M5 (Round 1): "97% of perceptible energy" overclaim — **RESOLVED ✓**

The overclaim has been replaced throughout. Discussion §4.1 (line 33–36):
"Neither pathway independently accounts for the full visceral experience, which
likely also involves chest-wall coupling, somatosensory stimulation, and
vestibular input." Conclusion (line 55–57) echoes this. The ">99.9%" figure
now refers specifically to the fraction of *abdominal wall displacement* from
structure-borne transmission, which is supported by the 2600× ratio. **Fully fixed.**

---

### M6 (Round 1): Frequency-dependent tissue properties ignored — **RESOLVED ✓**

Discussion §4.6 (lines 140–174) now addresses frequency-dependent viscoelasticity:
- Cites Duck (1990) and Fung (1993)
- Quantifies the effect: E doubling → f₂ increases ~40%, net displacement <2×
- η decrease from 0.25→0.15 increases Q but has little off-resonance effect
- MC brackets E over ±50%, encompassing plausible stiffening range
- Limitations item 7 (line 210–213) reiterates

**Fully fixed.**

---

## New Issues Identified in Round 2

### m1 (Minor): "Minimum 5.8×" is actually the 5th percentile, not the minimum

Results.tex line 230 states:
> "the floor pathway *always* exceeds the perception threshold (minimum 5.8×)"

The word "minimum" is misleading. At 10,000 MC samples (seed=42), the **actual
minimum** floor/threshold ratio is **4.97×**, not 5.8×. The value 5.8× is the
5th percentile (= lower bound of the 90% CI). While the floor pathway does
indeed always exceed the threshold in all samples (minimum 4.97× > 1.0×), the
parenthetical should read "(5th percentile: 5.8×)" or "(90% CI lower bound:
5.8×)" rather than "minimum."

The abstract (line 109) and conclusions (line 32–33) correctly label this as a
90% CI, so only the results section text needs correction.

### m2 (Minor): RMS vs. peak displacement basis inconsistent between pathways

The **airborne** tissue displacement from the energy-consistent formulation
(energy_budget.py line 193: `ξ² = P_abs / (ζ·ω³·M)`) yields **peak**
displacement. This was verified by re-deriving:
`P_diss = ζ·ω³·M·ξ_peak²` for time-averaged power.

The **floor** displacement from the SEA formula yields **RMS** velocity, hence
**RMS** displacement: `v_rms = √(P/(2ζωm))`, `ξ_rms = v_rms/ω`.

The **perception threshold** is converted to **peak** displacement:
`ξ_peak = a_rms·√2/ω²` (Eq. 12).

Therefore:
- Airborne ratio = ξ_peak(air) / ξ_peak(thresh) → **peak vs. peak** ✓
- Floor ratio = ξ_rms(floor) / ξ_peak(thresh) → **RMS vs. peak** — conservative by √2

This inconsistency makes the floor comparison **conservative** (understates the
floor pathway by ~41%), so it does not threaten the conclusions. However, the
paper should either (a) convert the floor displacement to peak (multiply by √2
for sinusoidal, or state a crest factor for broadband), or (b) convert the
threshold to RMS (divide by √2), or (c) explicitly note this conservatism.

The floor/airborne ratio (~2600) mixes RMS and peak bases and is therefore not
on a consistent footing, though this is an order-of-magnitude estimate anyway.

### m3 (Minor): MC does not vary body transmissibility or floor coupling efficiency

The Monte Carlo analysis varies E, ζ_floor, and SPL, but holds constant:
- Body transmissibility T = 1.8 (literature range ~1.2–2.5)
- Floor coupling efficiency η_f = 0.01 (no experimental basis cited)
- Floor area A_f = 100 m² (venue-dependent)
- Floor mass/area ρ_f' = 200 kg/m² (material-dependent)

These parameters contribute significant uncertainty to the floor pathway. In
particular, η_f = 0.01 is the most consequential assumption for the absolute
magnitude of floor displacement, yet it is not varied. Adding η_f and T to the
MC would strengthen the analysis. At minimum, a brief justification for fixing
these parameters should be added.

### m4 (Minor, editorial): Paper claims "2.5 orders of magnitude" — actually 2.46

Multiple locations (abstract line 100, results line 99, discussion line 15,
conclusion line 27) state "~2.5 orders of magnitude." The actual value is
log₁₀(0.560/0.00195) = 2.458, which rounds to 2.5. This is acceptable with
the "~" qualifier, but the precision could be tightened to "~2.45 orders" given
that the exact value is now computable.

---

## Positive Comments

1. **The F1 fix is exemplary.** The corrected floor vibration formula is
   physically well-motivated (SEA power balance), dimensionally verified in the
   text, independently hand-checked in the test suite, and produces results
   consistent with the qualitative expectation that concert floor vibration is
   perceptible. The test at lines 314–336 with a full hand calculation is
   exactly the kind of verification I want to see.

2. **Table 3 is now a model of data integrity.** Every cell can be reproduced
   from the code, the SPL values vary correctly with the EDM spectrum, and the
   floor/threshold ratios are self-consistent.

3. **The MC analysis is well-implemented.** Seed-based reproducibility, summary
   statistics, and range-sensitivity tests demonstrate good software engineering
   practice. The 90% CIs are clearly labeled and the conclusions are robust
   across the sampled parameter space.

4. **The discussion of limitations is thorough and honest.** Eight specific
   limitations are enumerated (§4.7), including the frequency-dependent tissue
   properties, the simplified floor model, and the derived (not tabulated)
   perception thresholds. This is exactly the level of intellectual honesty I
   expect.

5. **The reframing of the conclusion (M5 fix) is scientifically mature.** The
   paper no longer overclaims a single number for "perceptible energy" but
   instead frames the result as a pathway partition problem, correctly noting
   that additional pathways (chest wall, vestibular, somatosensory) likely
   contribute to the full experience.

6. **The off-resonance scaling formula (Eq. 9) is elegant and correct.** The
   factorisation ξ(f) = ξ_on-res × H(r,ζ)/Q × (ka(f)/ka(f_n))^n cleanly
   separates the on-resonance energy budget, the off-resonance transfer
   function, and the frequency-dependent coupling — each independently
   verifiable.

---

## Summary

All six issues raised in Round 1 (including the fatal dimensional error F1)
have been resolved satisfactorily. The corrected floor vibration model is
physically sound, the numerical results are reproducible and internally
consistent, the uncertainty quantification is adequate, and the conclusions
are appropriately hedged.

Four minor issues remain: (m1) mislabeling the 5th percentile as "minimum,"
(m2) an RMS-vs-peak inconsistency in the floor comparison that is conservative
but should be acknowledged, (m3) incomplete parameter coverage in the MC, and
(m4) a precision nit on "2.5 orders." None of these threatens the paper's
conclusions or requires new computation — they are clarifications and editorial
fixes.

**Recommendation: MINOR REVISION.** Address m1–m3 (m4 is optional), and the
paper is acceptable for publication.
