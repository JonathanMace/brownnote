---
applyTo: "tests/**"
---

# Test Instructions

You are writing or editing tests for the browntone analytical suite.

## Framework
- pytest (globally installed)
- Run: `python -m pytest tests/ -v` from repo root
- Currently 118 tests, all passing. **Do not break existing tests.**

## Conventions
- Test files: `test_<module_name>.py`
- Test functions: `test_<what_is_being_tested>()`
- Use `pytest.approx()` for floating-point comparisons with appropriate tolerances
- Parametrize over canonical + edge-case values using `@pytest.mark.parametrize`

## What to Test
1. **Canonical values**: Every module should have a test that creates a model with
   canonical parameters and verifies key outputs match expected values.
2. **Physical sanity**: Frequencies must be positive, displacements must be finite,
   energy must be conserved, coupling ratio must be > 1.
3. **Edge cases**: Zero pressure, very soft/stiff walls, extreme aspect ratios.
4. **Regression**: If you fix a bug, add a test that would have caught it.

## Canonical Expected Values (for regression tests)
- f₂ (flexural n=2): ~3.95 Hz
- Breathing mode (n=0): ~2490 Hz
- Energy-consistent displacement at 120 dB: ~0.014 μm
- Coupling ratio R: ~46,000
- Sobol S_T for E: ~0.86

## Import Pattern
```python
import sys
sys.path.insert(0, r'C:\Users\jon\OneDrive\Projects\browntone')
from src.analytical.natural_frequency_v2 import AbdominalModelV2, flexural_mode_frequencies_v2
```
