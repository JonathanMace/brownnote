---
name: write-analysis
description: >
  Guide for writing and editing analytical model code in src/analytical/. Use when changing the Browntone analytical model implementation.
license: MIT
---

# Analytical Code Instructions

You are editing the core analytical model code. Follow these rules strictly.

## Canonical Parameters

Every function that creates an AbdominalModelV2 must use these defaults:
```python
model = AbdominalModelV2(
    E=0.1e6,       # Pa (0.1 MPa)
    a=0.18,        # m
    c=0.12,        # m (oblate: c < a)
    h=0.01,        # m
    nu=0.45,
    rho_wall=1100, # kg/m³
    rho_fluid=1020,# kg/m³
    K_fluid=2.2e9, # Pa (2.2 GPa)
    P_iap=1000,    # Pa
    loss_tangent=0.25
)
```

**If you see different values in existing code, they are WRONG.** Fix them.
Common stale values: η=0.30, R_eq=0.133, ka=0.017 — these are from v1 and must not appear.

## Code Style
- Python ≥ 3.10
- Type hints on all public functions
- NumPy-style docstrings
- SI units throughout; document in variable names where ambiguous (e.g., `E_pa`, `freq_hz`)
- `snake_case` for functions, `PascalCase` for classes
- No magic numbers — use named constants or the canonical parameter set
- `import matplotlib; matplotlib.use('Agg')` for headless figure generation

## Module Architecture

The source of truth for the model is `natural_frequency_v2.py` which defines:
- `AbdominalModelV2` dataclass — the canonical parameter container
- `flexural_mode_frequencies_v2()` — modal frequencies for n=0..n_max
- `breathing_mode_v2()` — the n=0 mode (fluid bulk modulus dominated)

Other modules IMPORT from this. Do not duplicate the dataclass or parameter definitions.

Key modules and their APIs:
- `energy_budget.py`: `self_consistent_displacement(model, mode_n=2, spl_db=120)` → dict with `xi_energy_um`
- `mechanical_coupling.py`: WBV comparison, produces the 66,000× ratio
- `uncertainty_quantification.py`: Monte Carlo + Sobol indices
- `parametric_analysis.py`: 486-point parameter sweep

## Testing

All new functions need corresponding tests in `tests/`. Run with:
```powershell
cd C:\Users\jon\Projects\browntone
python -m pytest tests/ -v
```
Currently 203 tests, all passing. Do not break them.

## Key Physics Reminders

1. Breathing mode (n=0) ≈ 2490 Hz — fluid bulk modulus dominates. Not relevant to infrasound.
2. Flexural modes (n≥2) ≈ 4-10 Hz — shell changes shape, fluid is added mass only.
3. Energy-consistent displacement at 120 dB = 0.014 μm (NOT 0.18 μm pressure-based).
4. Coupling ratio R ≈ 66,000 (6.6×10⁴, mechanical/airborne). SDOF upper bound.
