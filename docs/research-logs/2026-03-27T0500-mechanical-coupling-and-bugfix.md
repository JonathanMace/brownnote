# Research Log — 2026-03-27T05:00 — Mechanical Coupling & Bug Fix

## What Was Done

1. Implemented `mechanical_coupling.py` — whole-body vibration excitation model
2. Compared airborne vs mechanical coupling quantitatively
3. Included ISO 2631 transmissibility data

## Bug Found: Double-Counting in Mechanical Model

The original code multiplied:
```
x_rel = T(f) × x_base × H_modal(f)
```

This is WRONG. The ISO transmissibility T(f) already captures the amplified
response at resonance (it's measured seat-to-abdomen, including body dynamics).
The modal response H_rel is the THEORETICAL version of the same thing.

Must use EITHER:
- Empirical: `x_abdomen = T(f) × x_seat` (from ISO 2631 data)
- Theoretical: `x_rel = H_modal(f) × x_base` (from our model)

NOT both multiplied together.

## Corrected Estimates

At 0.1 m/s² RMS, 4.4 Hz:
- x_base = 187 μm (base displacement)
- Using ISO T ≈ 1.9: x_abdomen ≈ 353 μm absolute
- Using model Q ≈ 3.3: x_rel ≈ 617 μm relative to skeleton

These are different quantities but same order of magnitude.
The relative displacement (what matters for tissue strain) is 617 μm at
0.1 m/s² — still FAR above PIEZO thresholds.

At the EU Action Value (0.5 m/s²): x_rel ≈ 3000 μm = 3 mm
This is enormous relative displacement — consistent with the known
discomfort and GI effects reported in WBV studies.

## Key Finding (Unchanged)

The mechanical coupling result holds even after fixing the bug:
- Mechanical at 0.1 m/s²: ~600 μm (well above PIEZO threshold)
- Airborne at 120 dB: ~0.14 μm (well below PIEZO threshold)
- Mechanical is ~4000× more efficient

## Critique of Current State

### Issues Still Outstanding
1. ⚠️ The base excitation FRF (H_rel) may itself be too simple — a single
   DOF model doesn't capture the multi-segment body dynamics
2. ⚠️ The relative displacement between skeleton and abdominal wall is not
   the same as strain in the intestinal wall — need a tissue-level model
3. ⚠️ Haven't compared our predicted transmissibility with the ISO 2631 data
4. ⚠️ The (ka)^n coupling for airborne may be too pessimistic — real body
   geometry (non-spherical, with orifices) may allow better coupling

### What This Means for the Paper

The paper should present BOTH coupling mechanisms:
1. Airborne: quantify the (ka)^n penalty, show it's very weak
2. Mechanical: show it naturally produces resonant amplification at 5-10 Hz
3. The comparison is the novel contribution

The "brown note" as popularly understood (loudspeaker → bowel effects) is
implausible. But WBV → GI effects is real and well-documented. Our model
provides the first mechanistic explanation connecting the two via PIEZO
channel activation.

## Plan Changes

- Fix the double-counting bug in mechanical_coupling.py
- Add transmissibility comparison (our model vs ISO 2631 data)
- Reviewer-b results expected soon — address findings
