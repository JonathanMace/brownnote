---
name: run-analysis
description: >
  Run the full analytical computation pipeline: modal frequencies, parametric
  sweeps, mechanotransduction analysis, and figure generation. Use when you
  need to regenerate results after code changes.
---

# Run Analysis Skill

Execute the browntone analytical pipeline and verify outputs match canonical values.

## Steps

### 1. Modal Frequencies
```powershell
cd C:\Users\jon\OneDrive\Projects\browntone
python -c "
from src.analytical.natural_frequency_v2 import AbdominalModelV2, flexural_mode_frequencies_v2
model = AbdominalModelV2(E=0.1e6, a=0.18, c=0.12, h=0.01, nu=0.45, rho_wall=1100, rho_fluid=1020, K_fluid=2.2e9, P_iap=1000, loss_tangent=0.25)
freqs = flexural_mode_frequencies_v2(model, n_max=5)
for n, f in freqs.items(): print(f'  n={n}: {f:.2f} Hz')
"
```
**Verify**: f₂ ≈ 3.95 Hz, breathing (n=0) ≈ 2490 Hz.

### 2. Energy-Consistent Displacement
```powershell
python -c "
from src.analytical.natural_frequency_v2 import AbdominalModelV2
from src.analytical.energy_budget import self_consistent_displacement
model = AbdominalModelV2(E=0.1e6, a=0.18, c=0.12, h=0.01, nu=0.45, rho_wall=1100, rho_fluid=1020, K_fluid=2.2e9, P_iap=1000, loss_tangent=0.25)
result = self_consistent_displacement(model, mode_n=2, spl_db=120)
print(f'  xi_energy = {result[\"xi_energy_um\"]:.4f} um')
"
```
**Verify**: ξ_energy ≈ 0.014 μm at 120 dB.

### 3. Mechanical Coupling
```powershell
python -c "
from src.analytical.natural_frequency_v2 import AbdominalModelV2
from src.analytical.mechanical_coupling import compare_airborne_vs_mechanical
model = AbdominalModelV2(E=0.1e6, a=0.18, c=0.12, h=0.01, nu=0.45, rho_wall=1100, rho_fluid=1020, K_fluid=2.2e9, P_iap=1000, loss_tangent=0.25)
result = compare_airborne_vs_mechanical(model)
print(f'  Coupling ratio R = {result[\"coupling_ratio\"]:.0f}')
"
```
**Verify**: R ≈ 66,000.

### 4. Run Tests
```powershell
python -m pytest tests/ -v --tb=short
```
**Verify**: All 118+ tests pass.

### 5. Log Results
Create timestamped entry in `docs/research-logs/` documenting what was run,
key numerical results, and whether they match canonical expected values.
