# Reviewer C — Round 1 (Paper 8: Kac Identifiability)

**Paper:** "Can You Hear the Shape of an Organ? Practical Identifiability of Viscoelastic Shell Parameters from Resonant Frequencies"
**Module:** `src/analytical/kac_identifiability.py` (885 lines)
**Tests:** `tests/test_kac_identifiability.py` (31 tests, all pass in 167 s)
**Reviewer:** C (computational mechanics / reproducibility specialist)
**Date:** 2026-03-30

---

## Overall Assessment

The code is well-structured, the test suite is thorough, and the core
scientific claims are computationally sound. The module cleanly implements
Jacobian computation, condition-number analysis, Fisher information, CRLB,
and round-trip inversion. All 31 tests pass.

However, I found **one systematic discrepancy** that pervades the entire paper:
every headline number was computed with **3 modes (n = 2, 3, 4)** while the text
consistently states **5 modes (n = 2, ..., 6)**. This is not a rounding issue —
the 3-mode and 5-mode results differ by up to 2× on some CRLB values. The
figure-generation script uses the 5-mode default, so the figures and the text
numbers are mutually inconsistent. This must be resolved before publication.

**Verdict: NEEDS WORK — one major discrepancy, several minor issues.**

---

## Code Verification Results (complete audit)

### Test suite

```
$ python -m pytest tests/test_kac_identifiability.py -v
31 passed in 167.12s
```

All 31 tests pass. No warnings from the module itself. Test coverage spans
Jacobian accuracy, rank deficiency, round-trip inversion, CRLB scaling,
watermelon cross-application, condition-number maps, edge cases, chain-rule
proportionality, and eccentricity sweep.

### Headline numbers: κ_sphere, κ_oblate, improvement factor

| Quantity | Paper claims | 3-mode code | 5-mode code | Match? |
|----------|-------------|-------------|-------------|--------|
| κ_sphere | 1.1 × 10¹⁰ | **1.1003 × 10¹⁰** | 1.3680 × 10¹⁰ | ✓ (3-mode) / ✗ (5-mode) |
| κ_oblate | 73.0 | **73.03** | 69.43 | ✓ (3-mode) / ✗ (5-mode) |
| Improvement | ≈ 1.5 × 10⁸ | **1.507 × 10⁸** | 1.970 × 10⁸ | ✓ (3-mode) / ✗ (5-mode) |

**All paper numbers match the 3-mode computation exactly.** The text states
"using the scaled Jacobian built from the flexural modes n = 2, ..., 6"
(results.tex line 10–11). This is incorrect — 5 modes give κ_oblate = 69.4,
not 73.0.

### Cramér–Rao bounds (Table 1, 1% noise)

| Param | Paper abs | Paper rel | 3-mode abs | 3-mode rel | 5-mode abs | 5-mode rel |
|-------|-----------|-----------|------------|------------|------------|------------|
| a | ±0.067 m | ±37% | **±0.066 m** | **±36.9%** | ±0.040 m | ±22.5% |
| c | ±0.016 m | ±13% | **±0.016 m** | **±13.3%** | ±0.007 m | ±6.0% |
| E | ±0.036 MPa | ±36% | **±0.036 MPa** | **±36.2%** | ±0.031 MPa | ±30.8% |

Again, **paper values match 3-mode computation exactly**. The 5-mode CRLB for
`c` is 6.0%, which is 2.2× better than the reported 13%. This is a large enough
difference to matter for the paper's practical conclusions.

### Watermelon cross-application

| Quantity | Paper | 3-mode code | 5-mode code |
|----------|-------|-------------|-------------|
| κ_watermelon | ≈ 104 | **104.5** | 127.8 |

Matches 3-mode computation. Watermelon parameters confirmed:
a = 0.158 m, c = 0.123 m, h = 0.015 m, E = 50 MPa (matches methodology §3.6).

### Round-trip inversion

Paper claims relative errors < 10⁻¹². Code gives:
- a: rel_err = 2.24 × 10⁻¹⁴  ✓
- c: rel_err = 5.32 × 10⁻¹⁵  ✓
- E: rel_err = 2.05 × 10⁻¹⁴  ✓

These are all well below 10⁻¹², consistent with the claim. ✓

### Sphere Jacobian proportionality (Proposition 1)

Numerical verification of the chain-rule result: the ratio
(∂f_n/∂a)/(∂f_n/∂c) is constant across all modes at the sphere model.

- Analytical prediction: 2c/a = 1.3333...
- Numerical ratios (modes 2–6): all 1.33333333 to 10 significant figures
- Scaled Jacobian columns satisfy J_s[:,a] = 2 · J_s[:,c] to within FD noise

**Proposition 1 is numerically confirmed.** ✓

### Ritz Jacobian non-proportionality (Proposition 2)

The Ritz model Jacobian ratio (∂f_n/∂a)/(∂f_n/∂c) varies with mode number:
- n=2: 0.394, n=3: 0.377, n=4: 0.317, n=5: 0.281, n=6: 0.274
- Coefficient of variation: 14.9%

This confirms that the oblate Ritz model breaks the proportionality
and restores full rank. ✓

### CRLB noise scaling

Verified that halving noise from 2% to 1% halves the CRLB:
- At 2%: a ±45.0%, c ±12.0%, E ±61.6%
- At 1%: a ±22.5%, c ±6.0%, E ±30.8%
- Ratios: exactly 2.0 for all parameters ✓

### 3-mode inversion fragility

The paper's claim about 3-mode local minima is confirmed:
- At 10% initial guess perturbation, 3-mode inversion converges to a
  **wrong** solution (max error 18.2%) with near-zero residual
- The wrong solution (a=0.2128, c=0.1114, E=97,667) produces **identical**
  frequencies for modes n=2,3,4 — a genuine isospectral parameter set
- 5-mode inversion correctly rejects this spurious solution

This is a strong numerical demonstration of the paper's design rule. ✓

### Forward model frequencies

Canonical abdomen (Ritz model, modes 2–6):
- n=2: 3.7996 Hz, n=3: 5.8021 Hz, n=4: 8.0910 Hz, n=5: 10.665 Hz, n=6: 13.528 Hz

---

## Reproducibility Issues

### R1. Mode count text–code inconsistency (MAJOR)

**Every headline number** in the paper was computed with modes (2, 3, 4), but
the text states modes (2, ..., 6). The code default is
`DEFAULT_MODES = (2, 3, 4, 5, 6)`. The figure-generation script
`scripts/generate_p8_figures.py` calls `sphere_vs_oblate_comparison()` which
uses `DEFAULT_MODES` (5 modes). Therefore:

- **Figures** show 5-mode results (κ_oblate ≈ 69)
- **Text** claims 5 modes but reports 3-mode numbers (κ_oblate = 73.0)
- **CRLB table** reports 3-mode bounds (a ±37%)

**Resolution required:** Either (a) recompute all numbers with 5 modes and
update the text, or (b) state clearly that headline results use 3 modes and
explain why. Option (a) is strongly preferred since the paper itself argues
that 5 modes are needed for robust inversion.

### R2. No figure-generation script for Fig. 5 (kappa vs eccentricity)

The `generate_p8_figures.py` script produces 4 of the 5 figures. Figure 5
(κ vs eccentricity) is generated by `plot_kappa_vs_eccentricity()` in the
module itself, but there is no documented pipeline to reproduce it. A reader
cannot reproduce Figure 5 from the paper text alone.

### R3. Missing functions in test imports

The test file imports `equivalent_sphere_jacobian_ratio`,
`verify_sphere_jacobian_proportionality`, and `kappa_vs_eccentricity` from the
module. These functions exist (lines 663–814) and tests pass, but they are
defined in a section of the source file (lines 658–885) that contains
analytical helpers and plotting code without documentation in the module
docstring. Minor — but a reader looking at the module's top-level docstring
wouldn't know these functions exist.

---

## Uncertainty and Statistical Rigour

### U1. CRLB interpretation needs qualification

The CRLB at 1% noise gives `a` ±37% (3-mode) or ±22.5% (5-mode). Either way,
this is a large uncertainty for the semi-major axis. The paper acknowledges this
("$a$ and $E$ are comparably less well constrained") but does not adequately
discuss whether these bounds are useful in practice. A 37% uncertainty on organ
size is not clinically useful. The discussion should explicitly state the
practical implications.

### U2. Power-law fit for κ vs eccentricity is weak

The paper claims "the data are well described by the power law κ ~ C ε^{-α}"
(results.tex §4.8). Running the code with 5-mode defaults gives R² = 0.52,
which is a poor fit. The κ vs eccentricity relationship is actually
non-monotonic:

| ζ = c/a | ε | κ (5-mode) |
|---------|-------|-----------|
| 0.10 | 0.995 | 18.3 |
| 0.20 | 0.980 | 14.7 |
| 0.30 | 0.954 | 16.1 |
| 0.50 | 0.866 | 51.7 |
| 0.667 | 0.745 | 69.5 |
| 0.80 | 0.600 | 118.0 |
| 0.95 | 0.312 | 162.7 |
| 0.99 | 0.141 | 170.6 |

At very high eccentricities (ζ < 0.3, thin-disc regime), κ actually **decreases**
rather than continuing to increase. A power law cannot capture this
non-monotonic behaviour. The claim should be weakened to: "For moderate
eccentricities (0.3 < ε < 0.95), the trend is approximately consistent with a
power-law divergence as ε → 0."

### U3. Fisher matrix formulation is consistent

I verified that the dimensional Fisher matrix F = J^T Σ^{-1} J and the
dimensionless version F_s = (1/ε²) J_s^T J_s give identical relative CRLB.
The two formulations are algebraically related by F_s = D_θ F D_θ where
D_θ = diag(θ_j). No inconsistency here. ✓

---

## Major Issues

### M1. 3-mode vs 5-mode inconsistency (Critical)

Summarised above in R1. This is the central finding of this review. All seven
headline numbers (κ_sphere, κ_oblate, improvement factor, three CRLB values,
watermelon κ) were computed with 3 modes but the paper claims 5 modes. The
discrepancies range from 5% (κ_oblate) to 120% (CRLB for c).

**Impact:** A reader attempting to reproduce the results using the stated mode
set (n = 2, ..., 6) would obtain different numbers and conclude the paper is
unreproducible. This is the most serious kind of text–code inconsistency.

---

## Minor Issues

### m1. Eccentricity power-law claim overstated

See U2 above. R² = 0.52 does not constitute "well described." The
non-monotonic behaviour at high eccentricity should be noted and the claim
softened.

### m2. Figure 5 not reproducible from the paper or the figure script

`generate_p8_figures.py` generates Figures 1–4. Figure 5 (κ vs eccentricity)
must be generated separately via `plot_kappa_vs_eccentricity()`. Add this to
the figure script.

### m3. Code default inconsistent with paper's recommendation

The code sets `DEFAULT_MODES = (2, 3, 4, 5, 6)` and the paper recommends
5+ modes. This is good. But the paper's actual results were computed with
3 modes. After fixing M1, this inconsistency should vanish.

### m4. Magic numbers in _PARAM_BOUNDS

```python
_PARAM_BOUNDS = {
    "a": (0.05, 0.40),   # m
    "c": (0.03, 0.40),   # m
    "E": (1e3, 1e9),      # Pa
}
```

These bounds are documented with comments but not derived from any
physical argument. For the watermelon case (E = 50 MPa), the upper bound
of 1 GPa is appropriate, but for soft tissue (E = 100 kPa) the lower
bound of 1 kPa is very close. Consider documenting the rationale.

### m5. `invert_frequencies` API requires `initial_guess` as positional arg

The function signature is `invert_frequencies(f_observed, initial_guess, ...)`
where `initial_guess` is required. The paper's methodology (§3.2) describes the
normalised-coordinate approach, but does not mention that the user must supply
an initial guess. This is fine for the code but should be noted in any
supplementary usage instructions.

### m6. Condition number at near-sphere limit for Ritz model

At ζ = 0.99 (nearly spherical), the Ritz model gives κ ≈ 171 (5-mode), not
the ~10¹⁰ that the sphere model gives. This is because the Ritz model still
performs integration over the (nearly spherical) surface, introducing tiny
mode-dependent curvature differences even when c ≈ a. The paper's statement
"κ diverges as ε → 0" for the Ritz model is only approximately true — the
divergence is much weaker than for the sphere model. Worth a brief remark.

---

## What's Done Well

1. **Clean code architecture.** The module separates forward models, Jacobian
   computation, condition analysis, inversion, and Fisher information into
   well-documented functions. The API is logical.

2. **Thorough test suite.** 31 tests covering all major functionality: Jacobian
   convergence, rank structure, round-trip inversion, CRLB scaling, chain-rule
   proportionality, edge cases. Test tolerances are physically motivated.

3. **Proposition 1 is numerically bulletproof.** The sphere Jacobian columns
   are proportional to 10 significant figures across all modes. The analytical
   proof matches the numerics perfectly.

4. **The 3-mode isospectral demonstration is compelling.** Finding that
   (a=0.213, c=0.111, E=97,667) produces identical 3-mode frequencies to
   the true parameters (a=0.18, c=0.12, E=100,000) is a powerful illustration
   of the identifiability problem.

5. **Fisher matrix implementation is correct.** Both the dimensional and
   dimensionless formulations give consistent results. Noise scaling is exact.

6. **The figure generation script** is reproducible, well-structured, and uses
   colorblind-friendly palettes.

---

## Summary Recommendation: NEEDS WORK

**One critical fix required, several minor improvements desirable.**

The critical issue is M1: every headline number was computed with 3 modes while
the text claims 5 modes. This is a straightforward fix — recompute with 5 modes
(or clarify the text) — but it affects every quantitative claim in the paper.

After that fix, the paper's numerical claims would be fully reproducible from
the code, and the scientific content is sound. The module is well-engineered
and the test coverage is strong. With the mode-count correction, all numbers
should be self-consistent.

**Priority list:**
1. Fix M1 (mode count): recompute all headline numbers with 5 modes, or
   correct the text to state 3 modes. (Prefer the former.)
2. Fix m1: soften the power-law claim or acknowledge R² ≈ 0.5.
3. Fix m2: add Figure 5 generation to the figure script.
4. Address U1: discuss practical implications of ±37% (or ±22.5%) uncertainty on `a`.
