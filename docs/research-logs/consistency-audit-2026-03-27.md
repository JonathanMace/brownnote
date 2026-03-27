# Consistency Audit — 2026-03-27

Canonical parameter set used for all checks:
```
E = 0.1 MPa, a = 0.18 m, c = 0.12 m, h = 0.01 m, ν = 0.45
ρ_w = 1100 kg/m³, ρ_f = 1020 kg/m³, K_f = 2.2 GPa
P_iap = 1000 Pa, η = 0.25 → Q = 4.0, ζ = 0.125
R_eq = (a²c)^(1/3) = 0.1572 m
```

---

## Code Output Reference Table

### natural_frequency_v2 (canonical params)

| Quantity | Code Value | Unit |
|----------|-----------|------|
| R_eq | 0.157244 | m |
| D (flexural rigidity) | 1.0449e-02 | N·m |
| c_fluid | 1468.63 | m/s |
| Q | 4.00 | — |
| ζ (damping ratio) | 0.125 | — |
| Volume | 1.6286e-02 | m³ |
| Surface area | 3.2040e-01 | m² |
| f₀ (breathing) | 2490.65 | Hz |
| f₁ (rigid body) | 0.00 | Hz |
| f₂ | 3.9524 | Hz |
| f₃ | 6.3087 | Hz |
| f₄ | 8.8795 | Hz |
| f₅ | 11.7069 | Hz |

### energy_budget (n=2, 120 dB)

| Quantity | Code Value | Unit |
|----------|-----------|------|
| ζ_rad (air) | 8.977e-16 | — |
| ζ_struct | 0.125 | — |
| σ_abs | 2.152e-11 | m² |
| σ_geo | 7.768e-02 | m² |
| Efficiency (ζ_rad/ζ_total) | 7.18e-15 | — |
| ξ_energy (120 dB) | 0.0137 | μm |
| ξ_pressure (120 dB) | 0.1844 | μm |
| Pressure-to-energy ratio | 13.42 | — |

### oblate_spheroid_ritz (a=0.18, c=0.12)

| Mode | Sphere (Hz) | Ritz (Hz) | Sphere overestimates by |
|------|------------|-----------|------------------------|
| n=2 | 3.95 | 3.80 | +4.0% |
| n=3 | 6.31 | 5.80 | +8.7% |
| n=4 | 8.88 | 8.09 | +9.7% |

### multilayer_wall

| Config | h_total (mm) | E_eff (MPa) | f₂ (Hz) | f₃ (Hz) | f₄ (Hz) |
|--------|-------------|-------------|---------|---------|---------|
| Relaxed | 25.1 | 0.0745 | 4.56 | 7.09 | 10.14 |
| Tensed | 25.1 | 2.6562 | 23.10 | 33.10 | 46.46 |
| Obese | 43.1 | 0.0360 | 4.23 | 7.07 | 10.79 |

### gas_pocket_resonance

| R (cm) | f_Minnaert (Hz) |
|--------|----------------|
| 1 | 321.95 |
| 2 | 160.97 |
| 3 | 107.32 |
| 5 | 64.39 |
| 10 | 32.19 |

Gas pocket R=3 cm at 120 dB, 7 Hz: ξ_wall = 1.416 μm, H = 1.004 (sub-resonant).

### E-sweep (canonical geometry)

| E (MPa) | f₂ code (Hz) | f₂ paper (Hz) | Match? |
|---------|-------------|--------------|--------|
| 0.05 | 3.4 | 3.4 | ✓ |
| 0.10 | 4.0 | 4.0 | ✓ |
| 0.20 | 4.9 | 4.9 | ✓ |
| 0.50 | 7.1 | 7.1 | ✓ |
| 1.00 | 9.6 | 9.6 | ✓ |
| 2.00 | 13.3 | 13.3 | ✓ |

---

## Parameter Mismatches

### M1 — **CRITICAL**: Breathing mode frequency (main.tex highlights vs code)

- **main.tex** highlights (line 85): "Breathing mode at **2900 Hz**"
- **section2_formulation.tex** eq (8) (line 108): f₀ ≈ **2900 Hz**
- **abstract** (line 97): "near **2500 Hz**"
- **conclusion** (line 7): "approximately **2500 Hz**"
- **Code output**: f₀ = **2491 Hz**
- **Verdict**: Abstract/conclusion match code (~2500). Highlights and
  section2_formulation say 2900 Hz, which is **wrong** — likely a stale value
  from an earlier parameter set.

### M2 — **CRITICAL**: Loss tangent / Q inconsistency

- **Table 1** (section2_formulation.tex, line 43): η = **0.25**
- **Section2 text** (line 71): "baseline value η = **0.30** (Q = 3.3)"
- **Code canonical model**: η = 0.25, Q = 4.0, ζ = 0.125
- **Section4 table captions** (lines 19, 59): Q = **4.0** ✓
- **Discussion** (line 38): ζ_struct = **0.15** (≠ 0.125; corresponds to η = 0.30)
- **Verdict**: Table 1 and the coupling tables say η = 0.25 / Q = 4.0.
  But the section2 body text and discussion use the older η = 0.30 / ζ = 0.15.
  These are contradictory within the same paper.

### M3 — **CRITICAL**: R_eq value in Discussion

- **Discussion** (line 26): R_eq = **0.133 m**
- **Code**: R_eq = **0.157 m**
- 0.133 m = (0.15² × 0.10)^(1/3) — this is the **default model** R_eq, not
  the canonical model.
- All (ka) calculations in the discussion are affected: e.g., ka at 7 Hz
  is 0.0171 (with R=0.133) vs 0.0202 (with R=0.157).

### M4 — **MODERATE**: Airborne ξ at 120 dB

- **section2_formulation.tex** (line 207): ξ_air ≈ **0.14 μm**
- **section4 table** (line 29–35): ξ_energy = **0.014**, ξ_pressure = **0.18**
- **Code**: ξ_energy = 0.0137 μm, ξ_pressure = 0.1844 μm
- **Verdict**: Section2 says "~0.14 μm" which is ambiguous — it appears to be
  the pressure-based value (0.18) rounded down, or maybe an old calculation.
  The energy-consistent value is 0.014 μm, a factor of 10 smaller. The section4
  table is correct; the section2 text is stale/misleading.

### M5 — **MODERATE**: Mechanical table x_base convention

- **Paper Table 4** (section4_coupling.tex): at 0.1 m/s², x_base = 162 μm
- **Code** (`WBVExposure.displacement_amplitude_m`): uses a_rms × √2 / ω² = 230 μm
- **Verification**: Paper values match x_base = a_rms / ω² (treating input as
  peak, not RMS, i.e. omitting √2). The table caption says "a_rms" but the
  computation uses peak convention. The H_rel × x_base = Q × x_base is consistent
  internally within the table (649 / 162 = 4.0 = Q), so the table is self-consistent
  but uses a different convention from the code.

### M6 — **MODERATE**: Oblate correction table (E = 0.5 MPa)

- **Paper Table 6** (section results.tex): n=3 sphere = **11.3 Hz**
- **Code**: n=3 sphere = **9.95 Hz** (with canonical h=0.01 m)
- With h=0.015 (the default model thickness), n=3 = 11.58 Hz, which rounds
  to 11.6 ≈ 11.3. The table appears to have been generated with mixed
  parameter sets (E=0.5 from the sweep, but h=0.015 from defaults).
- Similarly n=4 sphere: paper says **14.4**, code gives **12.93** (h=0.01) or
  **15.23** (h=0.015). Neither matches exactly.
- Ritz column also affected.

### M7 — **MINOR**: Section2 xi_mech approximation

- **section2_formulation.tex** (line 239): ξ_mech ≈ **7,000 μm = 7 mm**
- **Code**: ξ_mech at 1.15 m/s² = **7,459 μm** (using peak convention)
- **Verdict**: Paper rounds to 7 mm; code gives 7.5 mm. Acceptable
  approximation for display, but could be more precise.

### M8 — **MINOR**: ISO validation table rounding

- **Paper** (results.tex): Lean f₂ = 6.3, Average = 4.0, Large = 3.1
- **Code**: Lean = 6.2, Average = 4.0, Large = 3.3
- Lean is off by 0.1 Hz, Large by 0.2 Hz. Minor rounding differences from
  slightly different parameter choices (Large uses c=0.133 in paper vs
  computed c=0.133 = 0.2 × 0.667).

### M9 — **MINOR**: Boundary condition table

- **Paper** Table 5: "Free sphere (Ritz)" f₁ = **4.13 Hz**
- This is not from the canonical `flexural_mode_frequencies_v2` (which gives 3.95).
  It appears to be from a separate Ritz calculation not in the currently audited
  modules. The value is plausible but not directly verifiable from the checked code.

---

## Missing Files

All 5 `\includegraphics` references resolve to existing files:

| Reference | File | Status |
|-----------|------|--------|
| `../data/figures/fig_frequency_vs_E.pdf` | ✓ exists | OK |
| `../data/figures/fig_uq_sobol_indices.png` | ✓ exists | OK |
| `../data/figures/fig_geometry_schematic.pdf` | ✓ exists | OK |
| `../data/figures/fig_mode_shapes.pdf` | ✓ exists | OK |
| `../data/figures/fig_coupling_comparison.pdf` | ✓ exists | OK |

**No missing figure files.**

---

## Citation Issues

- All 23 `\cite{key}` references are present in `references.bib`. ✓
- **3 unused bib entries**: `Fahy2007`, `Leventhall2009`, `vonGierke1966`.
  These are harmless but could be cleaned up.

---

## Stale Content

### TODO/FIXME markers in .tex files (12 instances)

All are in **background.tex** and **methods.tex** — placeholder sections
that were never completed:

| File | Line | Content |
|------|------|---------|
| background.tex | 11 | `% TODO: Review of infrasound perception thresholds` |
| background.tex | 12 | `% TODO: Historical claims about the brown note` |
| background.tex | 21 | `% TODO: Typical material properties with ranges` |
| background.tex | 22 | `% TODO: Geometric dimensions from anthropometric data` |
| background.tex | 30 | `% TODO: Key equations for cylindrical shell modes` |
| background.tex | 31 | `% TODO: Extension to ellipsoidal geometries` |
| background.tex | 47 | `% TODO: Solutions for cylindrical and ellipsoidal cavities` |
| methods.tex | 37 | `% TODO: Mesh details, element type, mesh convergence results` |
| methods.tex | 52 | `% TODO: Function space, element type, boundary conditions, solver settings` |
| methods.tex | 56 | `% TODO: Helmholtz equation discretisation, rigid-wall BCs` |
| methods.tex | 60 | `% TODO: Mixed formulation, coupling conditions` |
| methods.tex | 64 | `% TODO: Richardson extrapolation, GCI results` |

**Note**: background.tex and methods.tex are included via `\input{}` but appear
to be placeholder/unused sections (the actual content is in section2_formulation.tex,
results.tex, etc.). main.tex does NOT `\input` background.tex or methods.tex, so
these TODOs are inert but should be noted.

### Stale `src/browntone/` references (40+ instances)

The package `src/browntone/` still exists in the repository and is referenced by:

| Location | Count | Nature |
|----------|-------|--------|
| `.github/` copilot instructions & skills | 18 | Agent instructions reference stale paths |
| `docs/repo-design.md` | 8 | Architecture doc describes stale package |
| `scripts/run_*.py` | 10 | Runner scripts import from `browntone.*` |
| `src/browntone/` itself | — | Package exists with cli.py, mesh, fem, etc. |
| `README.md` | 2 | Root readme references stale paths |
| `tests/conftest.py, test_*.py` | 5 | Tests import from `browntone.*` |

The active analytical code is in `src/analytical/`, not `src/browntone/`.
The `src/browntone/` package is a vestigial earlier scaffold.

### Stale v1 natural_frequency.py imports (2 files)

| File | Import |
|------|--------|
| `src/analytical/acoustic_coupling.py` | `from analytical.natural_frequency import AbdominalModel, breathing_mode_frequency` |
| `src/postprocess/generate_figures.py` | `from analytical.natural_frequency import (...)` |

These import from the v1 module (`natural_frequency.py`) instead of v2
(`natural_frequency_v2.py`). The v1 module still exists and these files will
work, but they use the old (buggy) model that incorrectly applies fluid
compressibility stiffness to flexural modes.

---

## Test Results

```
118 passed, 1 warning in 15.31s
```

All tests pass. The single warning is a deprecation in `dateutil` (unrelated).

Test breakdown:
- `test_analytical.py`: 89 tests ✓
- `test_extraction.py`: 2 tests ✓
- `test_figures.py`: 8 tests ✓
- `test_materials.py`: 14 tests ✓
- `test_mesh.py`: 5 tests ✓

---

## Summary: 9 issues (3 critical, 3 moderate, 3 minor)

### Critical (must fix before submission)

1. **M1**: Breathing mode frequency stated as 2900 Hz in highlights and
   section2_formulation; code gives 2491 Hz. Fix to ~2500 Hz.
2. **M2**: Loss tangent η = 0.25 in Table 1 but η = 0.30 in body text and
   discussion. Unify to one value throughout.
3. **M3**: Discussion uses R_eq = 0.133 m (from default model, not canonical
   parameters). All derived (ka) values in the discussion paragraph are wrong.

### Moderate (should fix)

4. **M4**: Section2 text says ξ_air ~ 0.14 μm at 120 dB, but the
   energy-consistent value is 0.014 μm (10× smaller). The pressure-based
   value is 0.18 μm. The text should clarify which estimate is quoted.
5. **M5**: Mechanical table uses peak-amplitude convention for x_base but
   labels the input as "a_rms". Either relabel or add √2 factor.
6. **M6**: Oblate correction table at E = 0.5 MPa uses mixed parameters
   (sphere frequencies don't match canonical h = 0.01 m).

### Minor / informational

7. **M7**: ξ_mech ≈ 7 mm in text vs 7.5 mm from code. Acceptable rounding.
8. **M8**: ISO table Lean/Large f₂ off by 0.1–0.2 Hz from code.
9. **M9**: BC table Ritz frequency (4.13 Hz) not directly reproducible from
   audited modules.

### Other notes

- 12 TODO comments in background.tex / methods.tex (inert — not \input'd by main.tex).
- 3 unused bib entries (harmless).
- `src/browntone/` package is vestigial (40+ stale references across repo).
- 2 source files still import from v1 `natural_frequency.py`.
- All figure files exist; all citations resolve.
- All 118 tests pass.
