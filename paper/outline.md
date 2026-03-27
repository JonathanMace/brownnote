# Paper Outline — Journal of Sound and Vibration Submission

**Target journal:** Journal of Sound and Vibration (Elsevier)
**Date prepared:** July 2025
**Status:** Outline and draft abstract

---

## 1. Proposed Titles

### Option A (recommended)
**Modal Analysis of a Fluid-Filled Viscoelastic Oblate Spheroidal Shell: Implications for Airborne vs. Mechanical Low-Frequency Excitation**

### Option B (shorter, punchier)
**Airborne vs. Mechanical Coupling to Flexural Modes of a Fluid-Filled Viscoelastic Shell**

### Option C (applications emphasis)
**Why Whole-Body Vibration Excites Abdominal Resonance but Airborne Infrasound Does Not: A Modal Analysis**

---

## 2. Abstract (248 words)

The human abdomen is modelled as a fluid-filled viscoelastic oblate spheroidal shell to investigate its modal response under low-frequency excitation. Using Love–Kirchhoff thin-shell theory with Kelvin–Voigt viscoelasticity and proper fluid-structure coupling, we derive natural frequencies for both breathing (n = 0) and flexural (n ≥ 2) mode families. The breathing mode, dominated by the fluid bulk modulus, occurs at approximately 2900 Hz and is irrelevant to infrasonic exposure. In contrast, flexural modes — in which the shell deforms without significant volume change and the enclosed fluid acts primarily as added mass — fall in the 4–10 Hz range, consistent with abdominal resonance data reported under ISO 2631. A comprehensive parametric study over elastic modulus (0.05–2.0 MPa), geometry, wall thickness, and intra-abdominal pressure demonstrates that the n = 2 flexural mode robustly occupies this frequency band for relaxed musculature, though the precise frequency is sensitive to tissue stiffness and boundary conditions.

We then compare two excitation pathways quantitatively. For airborne acoustic coupling, the long-wavelength condition (ka ≈ 0.017 at 7 Hz) imposes a (ka)^n penalty on flexural mode excitation, yielding displacements of order 0.1 µm at 120 dB SPL — below known mechanotransduction thresholds. For mechanical (whole-body) vibration, coupling is direct and produces displacements 10³–10⁴ times larger at occupational exposure levels. This disparity explains why whole-body vibration at 4–8 Hz is associated with gastrointestinal effects in the epidemiological literature, whereas airborne infrasound at comparable frequencies is not. The analysis provides the first unified quantitative framework bridging these two excitation mechanisms through a common modal description.

---

## 3. Section-by-Section Outline

### Section 1 — Introduction (2–2.5 pages)

**Purpose:** Establish the problem, review context, state the gap, declare objectives.

1.1 **Opening context** — Low-frequency acoustic and vibrational exposures in occupational and environmental settings (wind turbines, heavy machinery, transport). Cite ISO 2631-1:1997, ISO 7196:1995. Note the absence of universally accepted infrasound exposure limits.

1.2 **Abdominal resonance in the literature** — Published resonance data: 4–8 Hz range from whole-body vibration studies (Coermann et al. 1960; Griffin 1990; Kitazaki & Griffin 1998; Mansfield 2005; Toward & Griffin 2011). Note these are *mechanical* transmissibility measurements.

1.3 **Airborne infrasound health effects** — Brief summary of systematic reviews (Baliatsas et al. 2016; Leventhall 2007). Annoyance and sleep disturbance are robust findings; severe physiological effects remain unsubstantiated at environmental levels. Mention vibroacoustic disease (Castelo Branco & Alves-Pereira 2004) as occupational extreme.

1.4 **The gap** — No study has:
  - Derived abdominal cavity eigenfrequencies from first-principles shell theory with proper fluid coupling
  - Quantified the airborne acoustic coupling coefficient for flexural modes
  - Compared airborne vs. mechanical excitation pathways using a common modal framework

1.5 **Objectives** — State three clear objectives:
  1. Derive natural frequencies of a fluid-filled viscoelastic oblate spheroidal shell for both breathing and flexural mode families
  2. Compute the airborne acoustic coupling efficiency for flexural modes in the long-wavelength limit
  3. Compare predicted displacements for airborne vs. mechanical (whole-body vibration) excitation against mechanotransduction thresholds

1.6 **Statement of novelty** — First quantitative comparison of airborne acoustic and mechanical vibration coupling to abdominal flexural modes through a unified analytical model.

---

### Section 2 — Mathematical Formulation (4–5 pages)

**Purpose:** Derive the governing equations. This is the core theoretical contribution.

2.1 **Model geometry and assumptions**
  - Oblate spheroid: semi-major axis *a* (lateral/cranio-caudal), semi-minor axis *c* (antero-posterior)
  - Equivalent-sphere approximation: R_eq = (a²c)^{1/3}
  - Thin-walled shell assumption: h/R ≪ 1
  - Table of baseline geometric parameters with physiological justification

2.2 **Shell constitutive model**
  - Love–Kirchhoff thin-shell theory
  - Kelvin–Voigt viscoelasticity: E* = E(1 + iη), where η is the loss tangent
  - Flexural rigidity: D = Eh³/[12(1 − ν²)]
  - Quality factor: Q = 1/η (for small damping, Q ≈ 1/(2ζ))
  - Table of material properties with literature sources (Podwojewski et al. 2020; Calvo-Gallego et al. 2018; Szymczak et al. 2017)

2.3 **Fluid coupling — breathing mode (n = 0)**
  - Uniform radial displacement → volume change → fluid compression
  - Shell membrane stiffness: k_shell = 2Eh / [R²(1 − ν)]
  - Fluid volumetric stiffness: k_fluid = 3K/R (where K = bulk modulus ≈ 2.2 GPa)
  - Key result: k_fluid ≫ k_shell → breathing mode dominated by fluid compressibility
  - Effective mass: m_eff = ρ_w h + ρ_f R
  - Breathing frequency: f₀ = (1/2π)√(k_total/m_eff) ≈ 2900 Hz

2.4 **Fluid coupling — flexural modes (n ≥ 2)**
  - Deformation without volume change → no fluid compression
  - Fluid acts as *added mass* only: m_added = ρ_f R/n
  - Three restoring-force components:
    - Bending stiffness: K_bend = n(n−1)(n+2)² D/R⁴
    - Membrane stiffness (Lamb 1882): K_memb = (Eh/R²) × λ_n, where λ_n = (n²+n−2+2ν)/(n²+n+1−ν)
    - Pre-stress (intra-abdominal pressure): K_P = (P/R)(n−1)(n+2)
  - Natural frequency: ω_n² = (K_bend + K_memb + K_P) / (ρ_w h + ρ_f R/n)

2.5 **Airborne acoustic coupling**
  - Long-wavelength limit: ka ≪ 1 (at 7 Hz, ka ≈ 0.017)
  - Multipole expansion of incident plane wave on sphere
  - Coupling coefficient for mode n: p_eff = p_inc × (ka)^n
  - Physical interpretation: breathing mode (n=0) sees full pressure; flexural modes (n≥2) see only higher-order spatial gradients
  - Frequency-response function at mode n: H(ω) = 1/√[(1−r²)² + (2ζr)²], r = ω/ω_n

2.6 **Mechanical (base) excitation coupling**
  - Whole-body vibration transmits through skeleton at full amplitude (no ka penalty)
  - Base-excitation relative-displacement FRF: H_rel = r²/√[(1−r²)² + (2ζr)²]
  - Empirical transmissibility from ISO 2631 data (Kitazaki & Griffin 1998)
  - Dynamic pressure perturbation: ΔP = ρ_f × a_rel × R

---

### Section 3 — Parametric Study (3–4 pages)

**Purpose:** Demonstrate robustness (and sensitivity) of key findings.

3.1 **Elastic modulus sweep**
  - E = 0.05–5.0 MPa (very soft adipose to tensed muscle)
  - n = 2 frequency vs. E: monotonically increasing
  - The 4–10 Hz range requires E < ~0.5 MPa (relaxed musculature)

3.2 **Geometric sensitivity**
  - Semi-major axis *a*: 0.15–0.22 m (lean to obese)
  - Aspect ratio c/a: 0.5–0.8
  - Wall thickness h: 0.005–0.015 m
  - Full factorial: 810 parameter combinations

3.3 **Intra-abdominal pressure**
  - P_IAP: 0–2700 Pa (0–20 mmHg)
  - Tension-stiffening effect: higher pressure → higher frequency
  - Physiological range during rest: ~1000 Pa (7.5 mmHg)

3.4 **Boundary condition sensitivity**
  - Free shell (current model) → f_free
  - Estimated constraint multipliers: 1.3× (pinned posterior) to 3.0× (fully clamped)
  - Literature justification for partial constraint factors
  - Key result: even with 2× BC multiplier, mode remains in ISO 2631 range for soft tissue

3.5 **Multi-parameter summary**
  - Percentage of configurations in 5–10 Hz band
  - Percentage in ISO 2631 4–8 Hz band
  - Identification of dominant parameters (E > geometry > P_IAP > h)

3.6 **Body-type predictions**
  - Lean, average, large, obese body configurations
  - Compare predicted f₂ against published ISO 2631 data
  - Quantitative agreement within reported experimental scatter

---

### Section 4 — Airborne vs. Mechanical Coupling (3–4 pages)

**Purpose:** The central novel result — quantitative comparison of two excitation pathways.

4.1 **Airborne acoustic pathway**
  - Coupling coefficient: (ka)² ≈ 2.8 × 10⁻⁴ for n = 2 at 7 Hz
  - Displacement at resonance for SPL = 100–150 dB (table)
  - At 120 dB: ξ ≈ 0.14 µm (sub-threshold for known mechanotransduction)
  - SPL for 1 µm displacement: ~177 dB (physically unrealizable in free field)

4.2 **Mechanical vibration pathway**
  - EU WBV Directive action value: 0.5 m/s² RMS; limit: 1.15 m/s²
  - At 1.15 m/s² RMS at resonance:
    - Theoretical (modal FRF): x_rel ≈ several µm
    - Empirical (ISO 2631 T): x_rel ≈ several µm
  - Both well above mechanotransduction threshold (0.5–2.0 µm for piezo-type channels)

4.3 **Coupling ratio**
  - R_coupling = ξ_mechanical / ξ_airborne ≈ 10³–10⁴
  - Physical explanation: airborne path filtered by spatial mismatch (ka)^n; mechanical path bypasses this entirely
  - Analogy: trying to ring a bell by shouting across a room vs. striking it with a hammer

4.4 **Energy budget verification**
  - Power available from acoustic field via (ka)^n scattering
  - Power dissipated at predicted displacement
  - Confirm P_dissipated ≤ P_available at all SPL (energy conservation check)
  - Result: energy budget is self-consistent

4.5 **Comparison with empirical evidence**
  - ISO 2631 WBV effects at 4–8 Hz: documented GI symptoms
  - Airborne infrasound studies: no GI effects at ≤150 dB (MythBusters; Mohr et al. 1965; Johnson 1975)
  - Model predictions consistent with both bodies of evidence

---

### Section 5 — Discussion (2–3 pages)

5.1 **Physical interpretation**
  - Why two mode families exist: fluid compressibility dominates n = 0; fluid inertia dominates n ≥ 2
  - The misconception of treating abdominal cavity as a Helmholtz resonator (would predict ~2900 Hz, not infrasound)
  - Flexural modes as "sloshing" modes: shape change without compression

5.2 **Reconciling the literature**
  - ISO 2631 abdominal resonance data were always *mechanical* transmissibility — our model reproduces this
  - Conflation of mechanical and acoustic excitation has led to unfounded extrapolation: resonance at 5 Hz via WBV does NOT imply resonance effects from airborne sound at 5 Hz
  - The popular myth (not named) arises from confusing excitation mechanisms

5.3 **Alternative airborne coupling pathways**
  - Body-wall transmission (impedance mismatch: ~99.9% reflection, T ≈ 0.001)
  - Orifice coupling (mouth → GI tract): plausible but attenuated
  - Chest-wall compliance at low frequency: quasi-static response may slightly improve coupling
  - None of these overcome the ~10³ deficit relative to mechanical coupling

5.4 **Implications for exposure standards**
  - Current ISO 7196 defines G-weighting but no dose limits for airborne infrasound
  - Our analysis supports that airborne infrasound exposure limits may not need to account for abdominal resonance effects at levels below ~150 dB
  - WBV limits (ISO 2631) are well-calibrated to the actual coupling mechanism

5.5 **Limitations** (see Section 7 below for expanded treatment)

---

### Section 6 — Conclusions (0.5–1 page)

Three key conclusions:
1. A fluid-filled viscoelastic shell possesses two distinct mode families: a high-frequency breathing mode (~2900 Hz) governed by fluid compressibility, and low-frequency flexural modes (4–10 Hz) governed by shell stiffness with fluid added mass. The flexural modes match published abdominal resonance data.
2. Airborne acoustic coupling to flexural modes is extremely weak — a (ka)^n penalty — producing sub-threshold displacements at any realistically achievable SPL. Mechanical (whole-body) vibration bypasses this penalty and couples 10³–10⁴ times more efficiently.
3. The disparity between airborne and mechanical coupling explains the apparent contradiction in the epidemiological literature: GI effects from WBV at 4–8 Hz but not from airborne infrasound at comparable frequencies and moderate levels.

Future work: FE validation of analytical frequencies with 3D shell geometry; experimental validation using tissue-phantom shells; extension to nonlinear response at extreme SPL.

---

## 4. Figure List

| # | Figure | Description | Type |
|---|--------|-------------|------|
| 1 | **Model schematic** | Oblate spheroidal shell geometry with labeled parameters (a, b, c, h), fluid fill, coordinate system, and excitation mechanisms (airborne pressure wave vs. base acceleration) | Diagram |
| 2 | **Mode shape illustrations** | Schematic cross-sections showing (a) breathing mode n=0 (uniform radial), (b) n=1 rigid-body translation, (c) n=2 oblate-prolate, (d) n=3 flexural | Diagram |
| 3 | **Modal frequency spectrum** | Bar chart or frequency axis showing breathing mode at ~2900 Hz and flexural modes n=2–10 in the 4–20 Hz range. Annotate ISO 2631 range and airborne perception threshold | Plot |
| 4 | **E-modulus sensitivity** | f₂ vs. E (log scale, 0.05–5 MPa) with shaded bands for ISO 2631 (4–8 Hz) and 5–10 Hz ranges | Plot |
| 5 | **Multi-parameter sensitivity** | Histogram or violin plot of n=2 frequencies across 810 parameter combinations; shaded ISO range | Plot |
| 6 | **Airborne coupling** | (a) Displacement vs. SPL at resonance for n=2, (b) coupling coefficient (ka)^n vs. frequency for n=0,1,2,3 | Plot |
| 7 | **Mechanical coupling** | Displacement vs. base acceleration at resonance; horizontal lines at mechanotransduction thresholds. Annotate EU WBV action/limit values | Plot |
| 8 | **Coupling comparison** | Side-by-side or overlay: airborne displacement vs. mechanical displacement as a function of excitation level. Highlight the 10³–10⁴ gap | Plot |
| 9 | **Transmissibility comparison** | Model-predicted transmissibility (theoretical FRF) overlaid on published ISO 2631 / Kitazaki & Griffin data | Plot |
| 10 | **Energy budget** | P_available vs. P_dissipated as function of SPL; verification that P_diss ≤ P_avail | Plot |
| 11 | **Boundary condition sensitivity** | f₂ vs. BC constraint multiplier; shaded ISO range; marks for "free", "pinned", "partially clamped", "fully clamped" | Plot |
| 12 | **Body-type comparison** | Predicted f₂ for lean/average/large/obese configurations vs. published experimental ranges | Plot |

**Total: 12 figures** (within JSV norms of 8–15)

---

## 5. Key Equations

The following equations are essential and must appear in the manuscript:

### Shell mechanics
1. **Flexural rigidity:** D = Eh³ / [12(1 − ν²)]
2. **Complex modulus (viscoelasticity):** E* = E(1 + iη)

### Breathing mode (n = 0)
3. **Shell membrane stiffness:** k_shell = 2Eh / [R²(1 − ν)]
4. **Fluid volumetric stiffness:** k_fluid = 3K / R
5. **Breathing frequency:** f₀ = (1/2π)√[(k_shell + k_fluid) / (ρ_w h + ρ_f R)]

### Flexural modes (n ≥ 2)
6. **Bending stiffness:** K_bend = n(n−1)(n+2)² D / R⁴
7. **Membrane stiffness:** K_memb = (Eh/R²) × (n²+n−2+2ν) / (n²+n+1−ν)
8. **Pre-stress stiffness:** K_P = (P/R)(n−1)(n+2)
9. **Fluid added mass:** m_added = ρ_f R / n
10. **Natural frequency:** ω_n² = (K_bend + K_memb + K_P) / (ρ_w h + ρ_f R/n)

### Acoustic coupling
11. **Dimensionless wavenumber:** ka = 2πfR / c_air
12. **Effective pressure (mode n):** p_eff = p_inc × (ka)^n
13. **Frequency response:** H(ω) = 1 / √[(1 − r²)² + (2ζr)²], where r = ω/ω_n
14. **Airborne displacement:** ξ_air = p_eff / K_total × H(ω)

### Mechanical coupling
15. **Base-excitation FRF:** H_rel = r² / √[(1 − r²)² + (2ζr)²]
16. **Relative displacement:** ξ_mech = x_base × H_rel
17. **Dynamic pressure perturbation:** ΔP = ρ_f × a_rel × R

### Energy budget
18. **Incident intensity:** I = p²/(2ρ_air c_air)
19. **Available power:** P_avail = I × πR² × (ka)^{2n}
20. **Dissipated power:** P_diss = ζ ω_n M_eff (ω_n ξ)²

**Total: ~20 numbered equations** (plus intermediate steps in derivation)

---

## 6. Estimated Dimensions

| Metric | Estimate |
|--------|----------|
| **Abstract** | 250 words |
| **Main text** | 6,500–8,000 words |
| **Figures** | 12 |
| **Tables** | 4–5 (material properties, frequency comparison, parametric summary, coupling comparison, energy budget) |
| **Equations** | 20–25 numbered |
| **References** | 55–70 |
| **Pages (double-spaced)** | 28–35 |
| **Pages (typeset, two-column)** | 14–18 |
| **Supplementary material** | Python code repository (open data) |

---

## 7. Limitations (Thorough Treatment)

These must be explicitly discussed in Section 5.5.

### 7.1 Geometric simplifications
- **Equivalent-sphere approximation.** The oblate spheroid is mapped to an equivalent sphere via R_eq = (a²c)^{1/3}. This captures volume and leading-order curvature but loses the distinction between equatorial and polar modes. True oblate spheroidal shell theory (Flügge coordinates) would split mode degeneracies.
- **Axisymmetric geometry.** The real abdomen is irregular, asymmetric, and changes shape with posture, respiration, and bowel contents. Our model represents an idealized mean geometry.
- **No internal structure.** Visceral organs (liver, stomach, intestines, mesentery) are homogenized into a single fluid. Organ-scale impedance contrasts and attachments are neglected.

### 7.2 Material property uncertainty
- **Wide range of reported values.** Abdominal wall E spans 0.01–10 MPa depending on tissue layer, strain rate, and activation state. Our baseline (E = 0.1 MPa) represents passive, relaxed muscle; tensed muscle could be 10× stiffer.
- **Isotropic assumption.** The abdominal wall is a layered anisotropic composite (four muscle layers + fascia + skin). Homogenized isotropic E is a first-order approximation.
- **Linear viscoelasticity.** Kelvin–Voigt model captures first-order damping but not the nonlinear, strain-rate-dependent, and frequency-dependent behavior of biological tissue.
- **Loss tangent.** A single value (η = 0.3) is used; real tissue shows frequency-dependent dissipation.

### 7.3 Boundary conditions
- **Free-shell assumption.** The real abdomen is partially constrained by the spine (posterior), pelvis (inferior), ribs (superior), and musculature. Our free-shell model gives lower-bound frequencies; constrained modes would be higher.
- **Constraint multiplier estimates.** We estimate BC effects as 1.3–3.0× frequency multipliers, but these are rough estimates from structural dynamics analogy, not from patient-specific FE analysis.
- **Posture dependence.** Standing, seated, and supine postures alter both geometry and constraint conditions substantially.

### 7.4 Fluid model
- **Inviscid, irrotational fluid.** We neglect fluid viscosity, which is justified at low frequencies but prevents modelling viscous streaming or boundary-layer effects.
- **No gas pockets.** The GI tract contains gas (stomach, colon). Gas inclusions would dramatically alter local compressibility and could create additional resonances at lower frequencies. This is not modelled.
- **No peristalsis.** The GI tract has intrinsic motility (0.05–0.2 Hz); interaction between imposed vibration and peristalsis is neglected.

### 7.5 Acoustic coupling model
- **Plane-wave incidence.** Real infrasound fields are diffuse or near-field. At 7 Hz (λ ≈ 49 m), the body is deep in the sub-wavelength regime and the plane-wave assumption is reasonable, but diffraction effects are approximated.
- **(ka)^n coupling may be pessimistic.** The multipole expansion assumes coupling through spatial pressure gradients only. Body-wall transmission (direct pressure through tissue) provides an alternative pathway not captured by (ka)^n. However, the air–tissue impedance mismatch (T ≈ 0.001) makes this pathway weak as well.
- **No orifice coupling.** Sound entering through the mouth/nose into the GI tract could provide a lower-impedance pathway. This is unmodelled and may warrant separate investigation.

### 7.6 Absence of direct experimental validation
- **No tissue-phantom experiments.** The model predictions have not been validated against controlled experiments on fluid-filled shell phantoms.
- **Comparison to ISO 2631 is indirect.** Our predicted frequencies match the ISO 2631 range, but the published data are transmissibility measurements of the coupled skeletal-visceral system, not isolated cavity eigenfrequencies.
- **Recommended future validation:** Silicone or gelatin shell phantoms with controlled geometry and water fill, excited via shaker (mechanical) and loudspeaker (airborne), with laser vibrometry measurement of mode shapes and frequencies.

### 7.7 Scope limitations
- **Physiological thresholds are approximate.** Mechanotransduction thresholds (0.5–2.0 µm for piezo-type channels) are taken from the cell biology literature and may not directly translate to tissue-scale effects.
- **No sphincter/motility modelling.** Even if abdominal resonance is excited, the pathway from cavity deformation to GI effects (sphincter relaxation, peristaltic disruption) is not modelled.
- **Single-subject baseline.** Population variability is explored through parametric analysis but not through a formal probabilistic framework.

---

## 8. Anticipated Reviewer Concerns and Responses

### Concern 1: "The model is too simplified — a sphere cannot represent the abdomen."

**Response:** We acknowledge the geometric simplification (Section 5.5.1) and present it as a deliberate first-order analytical model, following the tradition of fluid-filled shell analysis in JSV (cf. Junger & Feit; Lamb 1882). The equivalent-sphere approach captures the essential physics — the separation between breathing and flexural modes, the (ka)^n coupling hierarchy, and the order-of-magnitude frequency predictions. Our parametric study (Section 3) shows that geometric variations (aspect ratio, semi-axes) shift frequencies by factors of 1.5–3×, but do not change the qualitative conclusions. We identify 3D FE analysis as the natural next step and note that the analytical model provides essential physical insight that FE alone does not.

### Concern 2: "Material properties are uncertain — how can you draw conclusions?"

**Response:** We explicitly address this in the parametric study (Section 3). The n = 2 flexural mode falls in the 4–10 Hz range for E < 0.5 MPa (relaxed musculature) across all tested geometric configurations. The *qualitative* conclusions — that (ka)^n coupling is weak and mechanical coupling is orders of magnitude stronger — are robust across the full 810-combination parameter space. The coupling ratio depends on ka (a function of frequency and body size) and is insensitive to material properties because both excitation pathways share the same modal structure.

### Concern 3: "There is no experimental validation."

**Response:** Direct experimental validation of an isolated abdominal cavity is not feasible in vivo. However, we validate indirectly against three independent data sources: (a) published ISO 2631 abdominal resonance frequency range (4–8 Hz), (b) seat-to-abdomen transmissibility data from Kitazaki & Griffin (1998) and Mansfield (2005), and (c) the well-documented absence of GI effects from airborne infrasound at SPL ≤ 150 dB. All three are consistent with our predictions. We propose tissue-phantom experiments as future work and provide sufficient model detail for independent replication.

### Concern 4: "The (ka)^n coupling is well known — what is novel?"

**Response:** The (ka)^n dependence is indeed classical (Junger & Feit; Morse & Ingard). Our novel contribution is applying it *quantitatively* to the specific problem of abdominal resonance excitation, deriving the flexural mode frequencies from first principles with proper fluid-structure coupling, and — critically — comparing the airborne and mechanical pathways side by side using the *same* modal framework. This comparison has not been made previously, and it resolves a persistent ambiguity in the literature where airborne and mechanical exposure effects are often conflated.

### Concern 5: "Is this really a JSV paper, or is it biomedical?"

**Response:** The core contribution is in structural acoustics: modal analysis of a fluid-filled viscoelastic shell, acoustic coupling in the long-wavelength limit, and comparison of pressure vs. base-excitation forcing. These are firmly within JSV's scope. The biological context is the *motivation* and provides empirical data for validation, but the physics and methodology are general. The same framework applies to any fluid-filled thin shell (e.g., fuel tanks, underwater vessels, industrial containers).

### Concern 6: "The free-shell boundary condition is unrealistic."

**Response:** Acknowledged (Section 5.5.3). The free-shell model provides a *lower bound* on flexural mode frequencies. We estimate the effect of partial constraints using frequency multipliers (1.3–3.0×) derived from structural dynamics analogy. Even with a 2× multiplier (partially clamped), the n = 2 mode for soft tissue remains in the ISO 2631 range. Importantly, the *coupling comparison* (airborne vs. mechanical) is independent of boundary conditions, because both pathways excite the same modes — the BC shifts the resonant frequency but does not change the coupling ratio.

### Concern 7: "What about gas in the GI tract?"

**Response:** This is a genuine limitation (Section 5.5.4). Gas pockets (stomach bubble, colonic gas) would locally reduce the effective bulk modulus and could introduce additional low-frequency resonances not captured by our homogeneous fluid model. This is an important direction for future work requiring either multi-phase fluid modelling or FE analysis with gas inclusions. We note, however, that gas pockets would primarily affect the *breathing* mode family (which depends on fluid compressibility) and have less effect on flexural modes (which depend on added mass and shell stiffness).

### Concern 8: "The paper mentions mechanotransduction thresholds — is this speculative?"

**Response:** We use the 0.5–2.0 µm range as a reference scale from the cell-biology literature (mechanically activated ion channels, including Piezo1/2). We do not claim that exceeding this threshold *causes* GI effects — only that it represents a plausible lower bound for biological detectability. Our argument is comparative: airborne excitation produces displacements well *below* this threshold while mechanical excitation produces displacements *above* it, which is consistent with the epidemiological pattern. We are careful to avoid overclaiming causation.

---

## 9. Highlights (JSV requirement, max 6, each ≤85 characters)

1. Breathing mode of fluid-filled shell is ~2900 Hz, not in infrasound range
2. Flexural modes at 4–10 Hz match ISO 2631 abdominal resonance data
3. Airborne acoustic coupling to flexural modes penalised by (ka)^n ≈ 10⁻⁴
4. Mechanical vibration coupling is 10³–10⁴× more efficient than airborne
5. Disparity explains why WBV causes GI effects but airborne sound does not
6. Parametric study confirms robustness across 810 parameter combinations

---

## 10. Keywords

1. Fluid-filled shell vibration
2. Viscoelastic oblate spheroid
3. Infrasound
4. Whole-body vibration
5. Acoustic-structural coupling
6. ISO 2631

---

## 11. Writing Sequence (Recommended)

| Priority | Section | Rationale |
|----------|---------|-----------|
| 1 | Section 2 (Mathematical formulation) | Core contribution; sets notation for everything else |
| 2 | Section 4 (Coupling comparison) | Key novel result |
| 3 | Section 3 (Parametric study) | Tables and figures drive the narrative |
| 4 | Section 5 (Discussion) | Interpretation and limitations |
| 5 | Section 1 (Introduction) | Easier to write once results are clear |
| 6 | Section 6 (Conclusions) | Distill from discussion |
| 7 | Abstract | Write last; distill from conclusions |
