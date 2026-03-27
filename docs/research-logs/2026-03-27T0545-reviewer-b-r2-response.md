# Research Log — 2026-03-27T05:45 — Reviewer B Round 2 Response

## Reviewer B Round 2 Verdict: MAJOR REVISION (0 fatal flaws!)

Significant improvement from REJECT. The qualitative physics is now correct.

## Issues Addressed This Iteration

### M3 (Absolute transmissibility formula) — FIXED ✓
Replaced `x_abs = x_base * (1 + H_rel)` with correct:
`T_abs = sqrt((1 + (2ζr)²) / ((1-r²)² + (2ζr)²))`
24% error eliminated.

### M5 (mechanotransduction.py on v1) — FIXED ✓
Migrated to v2 model. Key change: now uses (ka)^n coupling for flexural modes.
Result: SPL for 1 μm via n=2 = 137 dB (v1 predicted ~65 dB, a 72 dB error!)
This confirms the airborne brown note is implausible.

## Issues Still Outstanding

### M1 (Energy budget 2× violation)
- Ratio P_diss/P_avail ≈ 2.08 (constant across SPL)
- Root cause: inconsistency between pressure-based and energy-based coupling
- Reviewer B suggests using Junger & Feit reciprocity formulation
- TODO: Derive self-consistent energy budget
- NOTE: The violation makes airborne coupling WEAKER, strengthening our conclusion

### M2 (3.75× theory/empirical discrepancy in mechanical coupling)
- Theoretical SDOF gives H_rel = Q = 3.33 at resonance
- ISO empirical gives T-1 = 0.89
- Root causes: multi-DOF body, modal participation, different phenomena
- TODO: Introduce effective Q or modal participation factor
- FIX APPROACH: Use empirical as primary, theoretical as upper bound

### M4 (Complete-sphere for partial shell)
- Reviewer B says BC multipliers should be 2.5-4.0×, not 1.3-2.2×
- This would push n=2 from 4.4 Hz to 11-18 Hz (above brown note range!)
- CRITICAL: Need FEA validation to resolve this
- Rayleigh-Ritz agent still running — may partially address this

## Issues NOT Addressed Yet (lower priority)

- m1: Thick shell (h/R = 9.6%, ~4% freq correction for n=2)
- m2: Ellipsoidal mode splitting (~33% for c/a=0.67)
- m3: Loss tangent at high damping (~4% error)
- m4: ISO data attribution
- m5: PIEZO displacement vs strain
- m6: Internal pressure angular dependence

## Key Numerical Results (all v2)

| Quantity | Value |
|----------|-------|
| n=2 frequency (free, E=0.1 MPa) | 4.38 Hz |
| Breathing mode | 2435 Hz |
| SPL for 1 μm (airborne, n=2) | 137 dB |
| ξ at 120 dB (airborne, n=2) | 0.14 μm |
| ξ at 1.15 m/s² (WBV, theoretical) | 7165 μm |
| ξ at 1.15 m/s² (WBV, empirical) | 1911 μm |
| Coupling ratio (WBV/airborne) | ~10³-10⁴ |

## Assessment

The paper is now "within reach" of JSV publication per Reviewer B.
Key remaining work:
1. FEA validation (hemispherical shell, ~2 weeks)
2. Energy budget reconciliation (~1 week)
3. Effective Q / participation factor (~1 week)
4. Section 2 of paper drafted (mathematical formulation)

The Rayleigh-Ritz oblate spheroid analysis (running) will help with m2
(mode splitting) and provide a better geometry treatment.

## What Changed in the Plan

- M3 and M5 are now done (paper-blocking issues removed)
- M1, M2, M4 remain as the three critical path items
- FEA mesh generation moves up in priority (for M4)
- Paper Section 2 (math formulation) has been drafted in LaTeX
