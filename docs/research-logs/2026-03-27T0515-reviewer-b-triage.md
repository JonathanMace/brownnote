# Research Log — 2026-03-27T05:15 — Reviewer B Triage & Response

## Reviewer B Verdict: REJECT (4 fatal flaws, 5 major, 5 moderate)

## Triage Against Current State (v2 model)

### Already Fixed in v2
- **F1 (Breathing mode stiffness)** — ✅ FIXED. v2 correctly includes fluid bulk
  modulus. Breathing mode now at ~2900 Hz. We pivot to flexural modes (n≥2).
- **F2 (Full p_inc as drive)** — ✅ PARTIALLY FIXED. v2 uses (ka)^n coupling for
  flexural modes, giving p_eff = p_inc × (ka)^n. For n=2: factor ~2.8×10⁻⁴.
  This is the correct physics for scattering-driven differential pressure.
- **M5 (Binary search bug)** — ✅ Irrelevant. Was in acoustic_coupling.py (v1).
  v2 doesn't use that code path.
- **M2 (231× artifact)** — ✅ Irrelevant. Only in v1 coupling model.

### Strengthened by Reviewer B
- **F3 (Tissue exterior)** — Actually HELPS our v2 conclusion. If the shell is
  embedded in tissue, airborne acoustic coupling is even WEAKER than our (ka)^n
  estimate. The sound must first penetrate skin/fat/muscle to reach the cavity.
- **F4 (Energy budget)** — Need to VERIFY for v2 flexural modes, but our v2
  already predicts very weak airborne coupling (~0.14 μm at 120 dB), which is
  consistent with an energy budget that works.

### Still Valid — Must Address
1. **M7 (Q² error in mechanotransduction.py)** — 🔴 BUG. Need to fix.
2. **M8 (PIEZO apples-to-oranges)** — 🟡 Acknowledged. Need strain-based comparison.
3. **M9 (Boundary conditions)** — 🟡 Real issue. Constrained shell → higher freqs.
4. **M3 (E too low)** — 🟡 Need parametric sweep with realistic E range.
5. **M4 (Loss tangent uncertainty)** — 🟡 Need sensitivity analysis.
6. **M5-moderate (Organ heterogeneity/gas)** — 🟠 Important for discussion.
7. **m1 (No validation)** — 🟡 Need ISO 2631 comparison.
8. **m2 (Missing effects: gravity, respiration, posture)** — 🟠 For discussion.
9. **m3 (Inconsistent modules)** — 🟡 mechanotransduction.py still uses v1.

## Action Plan

### Immediate (this iteration)
1. Fix Q² bug in mechanotransduction.py
2. Add parametric sweep with realistic E range (0.1-2.0 MPa)
3. Verify energy budget for v2 flexural modes
4. Add boundary condition stiffening estimate

### Next iteration
5. Migrate mechanotransduction.py to v2
6. Strain-based PIEZO threshold comparison
7. ISO 2631 validation

### Paper discussion
8. Gas pocket scattering as limitation
9. Tissue exterior effects
10. Respiration, posture, gravity as confounds

## Critical Assessment

The review is devastating for v1 but our v2 already addresses the two worst
issues (F1 and F2). The remaining critiques make the case for airborne brown
note EVEN WEAKER, which is actually our v2 conclusion anyway.

The main risk to v2 is M9 (boundary conditions): if constrained BCs raise the
n=2 flexural mode from 5 Hz to 15-20 Hz, it moves out of the classic
"brown note" range. But it would still be in the whole-body vibration range.

The E sensitivity (M3) is also important: if realistic E values (0.5-2 MPa)
push the mode above 10 Hz, the connection to 7 Hz becomes tenuous.

## Key Realization

Reviewer B's recommendation #5 is exactly where v2 landed independently:
> "Consider mechanisms that don't require cavity resonance: whole-body
> vibration (skeletal transmission)..."

This validates our pivot. The paper's narrative should be:
1. We rigorously analyze the airborne acoustic pathway
2. We show it's orders of magnitude too weak
3. We show mechanical (WBV) coupling naturally explains the observations
4. The "brown note" myth conflates two different excitation pathways
