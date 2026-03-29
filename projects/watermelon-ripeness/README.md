# Paper 7: Can You Hear the Ripeness?

*Non-Destructive Acoustic Assessment of Fruit Maturity via Shell Resonance
Inversion*

Spin-off from the [browntone](../../README.md) research programme (synergy
score 5/5 — flagship application).

## Research Question

Consumers and farmers have assessed watermelon ripeness by "tapping and
listening" for centuries.  Can we replace this folk heuristic with a
physics-based model?  Specifically: given a measured tap-tone frequency, can
we invert the oblate spheroidal shell model to extract the rind elastic
modulus — and from that, a quantitative ripeness score?

## Approach

The watermelon is modelled as a **fluid-filled viscoelastic oblate spheroidal
shell** — exactly the same framework developed for the human abdomen
(Paper 1).  The rind is the "wall", the flesh is the "fluid", and turgor
pressure replaces intra-abdominal pressure.

Key contributions:

1. **Physics-based forward model** — shell theory → predicted tap-tone
   frequency *f*₂ for any cultivar and ripeness stage.
2. **Closed-form inverse** — measured *f*₂ → rind elastic modulus *E* →
   ripeness category.
3. **Universal dimensionless ripeness curve** — collapses all cultivars
   onto a single Π-curve.
4. **Validation** against De Belie et al. (2000) experimental data.

## Canonical Parameters (Ripe Watermelon)

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Semi-major axis *a* | 0.158 | m | Typical ~31.5 cm |
| Semi-minor axis *c* | 0.123 | m | Typical ~24.6 cm |
| Rind thickness *h* | 0.015 | m | 12–20 mm |
| Rind E | 2.0 | MPa | Decreases with ripening |
| Flesh density | 950 | kg/m³ | 928–974 from literature |
| Loss tangent η | 0.15 | — | More damping when ripe |

## Quick Start

```bash
# Run the watermelon tests
python -m pytest tests/test_watermelon.py -v

# Predict ripe watermelon tap-tone
python -c "
from src.analytical.watermelon_model import predict_tap_tone
print(predict_tap_tone())
"
```

## Files

- `src/analytical/watermelon_model.py` — Forward model, inversion,
  parametric sweeps, Sobol analysis, multi-cultivar comparison
- `tests/test_watermelon.py` — Comprehensive test suite

## Status

- [x] Analytical module scaffolded
- [x] Tests passing
- [ ] LaTeX paper skeleton
- [ ] Figures
- [ ] De Belie validation with full dataset
- [ ] Submission draft
