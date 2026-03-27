---
name: critique-results
description: >
  Invoke the Reviewer B agent to critically analyze recent computational results,
  figures, or code. Use after generating new results or completing a work phase
  to identify flaws before they propagate.
---

---
name: critique-results
description: >
  Invoke the Reviewer B agent to critically analyze recent computational results,
  figures, or code. Use after generating new results or completing a work phase
  to identify flaws before they propagate.
---

# Critique Results Skill

Quick quality gate: review recent work for flaws before they propagate.

For a full review round, use the 3-reviewer panel (reviewers A, B, C in parallel).
This skill is for lightweight, rapid checks between full rounds.

## Steps

### 1. Gather Current State

- Read the most recent research log in `docs/research-logs/`
- Check recently modified code in `src/analytical/`
- Check recently generated figures in `data/figures/`
- Run `python -m pytest tests/ -v --tb=short` to verify tests pass

### 2. Quick Consistency Check

Run the canonical model and verify key outputs:
```python
from src.analytical.natural_frequency_v2 import AbdominalModelV2, flexural_mode_frequencies_v2
from src.analytical.energy_budget import self_consistent_displacement
model = AbdominalModelV2(E=0.1e6, a=0.18, c=0.12, h=0.01, nu=0.45,
    rho_wall=1100, rho_fluid=1020, K_fluid=2.2e9, P_iap=1000, loss_tangent=0.25)
freqs = flexural_mode_frequencies_v2(model, n_max=5)
disp = self_consistent_displacement(model, mode_n=2, spl_db=120)
```

Expected: f₂≈3.95 Hz, ξ_energy≈0.014 μm, breathing≈2490 Hz.

### 3. Flag Issues

Rate each issue:
- **CRITICAL**: Wrong physics, parameter inconsistency, would invalidate results
- **MAJOR**: Missing validation, incomplete UQ, stale numbers in paper
- **MINOR**: Style, formatting, documentation gaps

### 4. Output

Write critique to `docs/research-logs/YYYY-MM-DDTHHMM-critique-{topic}.md` with:
- Summary assessment (1 paragraph)
- Issues by severity (specific file/line references)
- Recommendation for next action
