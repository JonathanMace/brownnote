# Paper 8: Can You Hear the Shape of an Organ?

**Practical Identifiability of Viscoelastic Shell Parameters from Resonant Frequencies**

## Summary

This paper addresses the inverse problem for the Browntone abdominal resonance
model: given measured resonant frequencies (f₂, f₃, f₄, ...), can we uniquely
recover the physical parameters (semi-major axis *a*, semi-minor axis *c*,
Young's modulus *E*)?

The headline result connects to Kac's famous 1966 question — "Can one hear
the shape of a drum?" — applied to viscoelastic shells:

- **Sphere model**: The Jacobian for (f₂, f₃, f₄) → (a, c, E) is
  **rank-deficient** (condition number ~ 10¹⁰) because all flexural modes
  scale identically with the equivalent-sphere radius.
- **Oblate spheroid (Ritz) model**: The Jacobian is **full rank**
  (condition number ~ 83.5) because different modes sample the oblate
  curvature differently.

> *You can hear the shape of an oblate spheroid, but NOT a sphere.*

## Target Venue

- Primary: *Inverse Problems* (IOP)
- Alternative: *Proceedings of the Royal Society A*

## Repository Layout

```
papers/paper8-kac/
├── main.tex                ← paper skeleton (elsarticle)
├── references.bib          ← bibliography
├── figures/                ← paper figures
└── sections/
    ├── introduction.tex
    ├── theory.tex
    ├── methodology.tex
    ├── results.tex
    ├── discussion.tex
    └── conclusion.tex

src/analytical/
└── kac_identifiability.py      ← inverse solver & identifiability analysis

tests/
└── test_kac_identifiability.py ← test suite
```

## Key Functions

| Function | Purpose |
|----------|---------|
| `compute_jacobian()` | Numerical Jacobian of frequencies w.r.t. (a, c, E) |
| `jacobian_condition_number()` | Condition number κ(J) |
| `condition_number_map()` | Sweep κ over parameter space |
| `invert_frequencies()` | Newton–Raphson inverse solver |
| `identifiability_analysis()` | Fisher information, Cramér–Rao bounds |
| `sphere_vs_oblate_comparison()` | Headline sphere vs oblate comparison |

## Running Tests

```bash
python -m pytest tests/test_kac_identifiability.py -v
```

## Dependencies

Uses the existing forward model from Paper 1:
- `src/analytical/natural_frequency_v2.py` — `AbdominalModelV2`
- `src/analytical/oblate_spheroid_ritz.py` — Ritz oblate model
- `src/analytical/watermelon_model.py` — watermelon validation case
