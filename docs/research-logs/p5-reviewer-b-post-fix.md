# Reviewer B — Paper 5 (Borborygmi) Post-Fix Review

**Paper:** "What pitch is a growling stomach? A unified multi-mode acoustic model of borborygmi"
**Reviewing:** Current state after PR #126 (8 claimed fixes)
**Date:** 2026-03-29
**Reviewer:** B (Technical correctness, internal consistency, logical gaps)

---

## Decision: MAJOR REVISION

The authors have addressed several of the previous concerns (wall stiffness sensitivity, geometric limits, language precision), but the paper still contains critical numerical errors and a dimensionally incorrect equation that undermine the central narrative. Two of the eight fixes were incomplete or introduced new inconsistencies.

---

## Fatal Flaws

### F1. Axial mode sub-audibility claim is numerically wrong by a factor of 10 in volume

**Lines 340–341, 433, 582–583, 704** (appears FOUR times):

The paper states: "$f_\mathrm{ax} < 100$ Hz for $V > 1$ mL"

The code gives:
| Volume | $f_\mathrm{ax}$ (Hz) |
|--------|----------------------|
| 1 mL   | **314.2**            |
| 2 mL   | 222.2                |
| 5 mL   | 140.5                |
| 10 mL  | 99.4                 |

The axial mode reaches 100 Hz at $V \approx 9.9$ mL, not 1 mL. At 1 mL, $f_\mathrm{ax} = 314$ Hz — squarely within the clinical range of 200–550 Hz. This is not a minor numerical discrepancy; it is off by an order of magnitude in volume and directly falsifies the paper's central argument that "the constrained bubble mode dominates the clinically audible band across the entire physiologically relevant volume range" (line 342).

For volumes of 1–2.5 mL, the axial piston mode is simultaneously:
- The lowest-frequency mode (below constrained), AND
- Within the clinical audible band (200–550 Hz)

**This was supposed to be addressed by Fix #1 ("mode dominance narrative corrected") but was NOT fixed.**

### F2. Radial breathing mode formula (Eqs. 9–11) is dimensionally incorrect

Combining the definitions in Eqs. (9)–(10) with the formula in Eq. (11):

- $K_\mathrm{gas} = 2\gamma P_0$ has units [Pa] = [kg·m⁻¹·s⁻²]
- $M_\mathrm{fluid} = \rho_f R_l$ has units [kg·m⁻²]
- $(K_\mathrm{gas} + K_\mathrm{wall})/(M_\mathrm{fluid} + M_\mathrm{wall})$ has units [m·s⁻²]
- $\sqrt{\cdot}$ gives [m¹/²·s⁻¹]
- Multiplying by $1/(2\pi R_l)$ gives **[m⁻¹/²·s⁻¹]** — NOT [Hz]

The formula is dimensionally inconsistent. The correct stiffness per unit area per unit radial displacement is $2\gamma P_0 / R$, not $2\gamma P_0$. The paper's Eq. (11) overestimates the radial frequency by a factor of $1/\sqrt{R_l} \approx 8.2$ for $R_l = 15$ mm.

- Paper/code value: $f_r = 1329$ Hz
- Corrected value: $f_r \approx 163$ Hz

At 163 Hz, the radial breathing mode would be comparable to the constrained bubble mode at large volumes (~135–223 Hz for 10–50 mL), fundamentally altering the mode landscape described in the paper.

Compare with the spherical constrained model (Eqs. 3–5), which IS dimensionally correct: $k_\mathrm{gas} = 3\gamma P_0 / R$ has units [Pa/m], and $\omega^2 = k/m$ directly yields [s⁻²].

---

## Major Issues

### M1. Internal inconsistency in axial scaling law

**Line 337** states: "$f_\mathrm{ax} \propto V^{-1}$"
**Line 580** repeats: "$f \propto V^{-1}$"
**Line 396** correctly states: "$f \propto V^{-1/2}$ for the Helmholtz and axial modes"

The code confirms $V^{-1/2}$ scaling:
- $f(1\text{ mL})/f(10\text{ mL}) = 314.2/99.4 = 3.162 = \sqrt{10}$
- $V^{-1}$ scaling would predict a ratio of 10

Lines 337 and 580 are wrong and contradict line 396 within the same paper. The incorrect $V^{-1}$ claim is used to justify why the axial mode "drops more steeply" — with the correct $V^{-1/2}$ scaling, the axial mode still drops faster than the constrained ($V^{-1/3}$) but less dramatically than claimed.

### M2. Mode dominance narrative remains incorrect for small volumes

Even after Fix #1, the paper claims (lines 341–344): "the constrained bubble mode dominates the clinically audible band (200–550 Hz) across the entire physiologically relevant volume range."

With the corrected numbers:
- At 1 mL: $f_\mathrm{ax} = 314$ Hz (within clinical band), $f_\mathrm{con} = 440$ Hz
- At 2 mL: $f_\mathrm{ax} = 222$ Hz (within clinical band), $f_\mathrm{con} = 360$ Hz
- At 2.5 mL: $f_\mathrm{ax} \approx 199$ Hz (exits clinical band)

For the 1–2.5 mL range, the axial mode IS audible and IS lower than the constrained mode. Whether it is actually excited depends on geometry (the slug at 1 mL is only 1.4 mm long in a 30 mm tube — arguably too short for a piston mode), but the paper needs to discuss this rather than assert blanket dominance of the constrained mode.

### M3. Q factor inconsistent with burst duration

**Lines 664–670:** The paper claims Q = 4 ($\eta = 0.25$) is "consistent with the short duration (~0.5–0.8 s) of individual bowel sound bursts."

Q = 4 at $f_c = 223$ Hz gives a ring-down time of:
$$\tau = Q/(\pi f) = 4/(\pi \times 223) = 5.7 \text{ ms}$$

The number of oscillation cycles before decay is ~Q = 4, so the ring-down time is ~$4/223 = 18$ ms. This is **30–45× shorter** than the claimed 0.5–0.8 s burst duration. Q = 4 implies a burst should last ~20 ms, not 500–800 ms.

The observed long bursts are consistent with sustained peristaltic forcing, not free decay of a Q = 4 resonator. The word "consistent" at line 669 is misleading; "inconsistent unless sustained forcing is invoked" would be more accurate.

### M4. Five mechanisms or four?

The paper claims five "distinct" mechanisms (line 106, 134). However, the Minnaert and constrained bubble modes share the same geometry (spherical bubble), the same oscillation pattern (radial pulsation), and the same governing physics (gas compressibility restoring force). The constrained model is a perturbation of Minnaert adding wall stiffness and inertia — they differ by only 9% for default parameters. These are the same mechanism with and without wall correction, not two independent mechanisms. Counting them as distinct inflates the apparent richness of the framework.

A more honest framing: four resonance mechanisms (bubble, Helmholtz, axial piston, radial breathing), with the bubble model having a wall-corrected variant.

---

## Minor Issues

### m1. Cylindrical added mass for axial piston mode (Eq. 7)

The radiation mass $m_\mathrm{end} = (8/3)\rho R^3$ is the standard result for a rigid circular piston radiating into free half-space (Kinsler et al., 1999). However, in a tube, the radiation impedance of the fluid plug face differs significantly from the free-field piston result due to waveguide effects. This approximation should be acknowledged as a limitation.

### m2. End correction for Helmholtz neck

The end correction $L_\mathrm{eff} = L_n + 1.6 r_n$ implies two flanged-like corrections of $0.8r$ each. Standard values range from $0.6r$ (unflanged) to $0.85r$ (infinite flange) per end. The choice of $0.8r$ per end is within the reasonable range but should be cited.

### m3. Self-citation to unpublished work

**Line 112:** The reference \cite{Mace2026gaspockets} is listed as "Submitted" with year 2026. Reviewers cannot verify this citation. The key constrained-bubble formulation should be fully self-contained in this paper.

### m4. Gas composition effect underestimated

**Lines 656–662:** The paper estimates a 4% frequency reduction for CO₂-rich gas ($\gamma \approx 1.3$ vs 1.4). However, intestinal gas can also contain significant H₂ and CH₄, and the sound speed used in the Helmholtz mode (343 m/s) assumes air. The effective sound speed in a CO₂-rich mixture is ~260 m/s, which would reduce the Helmholtz frequency by ~24%, not 4%.

---

## Assessment of the 8 Claimed Fixes

| # | Fix | Status | Comment |
|---|-----|--------|---------|
| 1 | Mode dominance narrative | **NOT FIXED** | The narrative direction was corrected (axial acknowledged as lowest-frequency), but the numerical claim "$f_{ax} < 100$ Hz for $V > 1$ mL" is wrong by 10× |
| 2 | Wall stiffness 9% | ✅ Fixed | Verified: 1 kPa → 100 kPa gives 220.7 → 240.5 Hz = 9.0% |
| 3 | Stiffness sweep replaces tube diameter | ✅ Fixed | Panel (b) now shows E sweep; constrained independence from tube diameter acknowledged |
| 4 | 50 mL geometric limit | ✅ Fixed | 14 mL limit properly stated (lines 631–639) |
| 5 | "No fitted parameters" | ✅ Fixed | Lines 107, 697 |
| 6 | c_gas comment | ✅ Fixed | Footnote at line 163 correctly states room temperature |
| 7 | Clinical validation softened | ✅ Fixed | "If validated experimentally" (line 618) |
| 8 | Five-mechanism distinctness | **Partial** | Paper now distinguishes geometry requirements but still counts Minnaert and constrained as separate mechanisms |

**Score: 5/8 fully fixed, 1 partial, 2 not fixed**

---

## Positive Comments

1. **The core physics is sound.** The constrained bubble formulation (Eqs. 1–5) is correct, properly derived, and reduces to Minnaert in the appropriate limit. This is verified analytically and numerically in both code and tests.

2. **Reproducible computational framework.** The codebase is clean, well-documented, and includes 55 passing tests covering dimensional sanity, monotonicity, limiting cases, and clinical range overlap. This level of computational reproducibility is commendable.

3. **Honest acknowledgment of limitations.** The geometric limit (§5.4), radiation/transmission gap (§5.4), and single-pocket model limitation are transparently stated.

4. **Clinical comparison is well-framed.** Table 3 provides a useful mapping between clinical conditions and predicted pocket volumes. The language is appropriately cautious ("if validated experimentally").

5. **Wall stiffness insensitivity is a genuinely interesting result.** The 9% shift across a 100× range of E values is physically significant — it means borborygmi frequencies are robust biomarkers of gas volume, not wall properties.

6. **The concept is novel and valuable.** Despite the errors identified, this is the first attempt to provide a first-principles acoustic model for borborygmi, and the fundamental approach of treating gut gas as constrained Minnaert bubbles is physically well-motivated.

---

## Summary

The paper presents a creative and potentially valuable first-principles framework for borborygmi acoustics. Five of the eight post-PR-#126 fixes are properly implemented. However, three significant issues remain:

1. **A persistent numerical error** (axial < 100 Hz at V > 1 mL) that appears four times and directly falsifies the central mode-dominance claim;
2. **An internally inconsistent scaling law** ($V^{-1}$ at lines 337/580 vs. the correct $V^{-1/2}$ at line 396);
3. **A dimensionally incorrect equation** (Eqs. 9–11) for the radial breathing mode, overestimating its frequency by a factor of ~8.

Issues 1 and 2 are straightforward to fix (change "1 mL" to "~10 mL" and "$V^{-1}$" to "$V^{-1/2}$", then revise the mode dominance discussion to acknowledge axial competition at small volumes). Issue 3 requires rederiving Eq. (11) and recomputing the radial mode, then updating the mode transition map and discussion.

The paper's central thesis — that constrained bubble resonance explains most of the audible borborygmi spectrum — likely survives these corrections for the bulk of the physiological volume range (V > 2.5 mL), but the narrative must be tightened and qualified. I would be prepared to recommend acceptance after these corrections are made.

**Verdict: MAJOR REVISION** — the errors are correctable but affect equations, figures, and the central narrative.
