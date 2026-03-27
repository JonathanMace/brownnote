# Reviewer B — Paper 2, Round 1

**Manuscript:** "Bowel Gas as an Acoustic Transducer: A Constrained Bubble Model for Infrasound-Induced Mechanotransduction in the Gastrointestinal Tract"

**Submitted to:** JASA (Journal of the Acoustical Society of America)

**Review date:** 2026-03-28

---

## Decision: MAJOR REVISION

The paper presents an interesting and physically grounded idea: that intraluminal gas pockets act as impedance-matching transducers between airborne infrasound and the intestinal wall. The constrained-bubble formulation is correct in its governing equations and the sub-resonant compliance argument is sound. However, the manuscript has one potentially fatal flaw (the acoustic short-circuit problem), several internal inconsistencies between the text and the code, and pervasive overclaiming that must be addressed before this is publishable at JASA.

---

## Fatal Flaws

### F1. The Acoustic Short-Circuit Problem Is Not Addressed

**This is the most serious issue in the paper.**

The entire model assumes the gas pocket is a sealed compressible inclusion surrounded by incompressible tissue. The driving mechanism is: tissue pressure oscillates at $p_\mathrm{inc}$; gas must compress to match. This works for a sealed void (like a microbubble in bulk liquid).

However, the gastrointestinal tract is an **open tube** from mouth to anus. Gas pockets sit within the intestinal lumen, which is connected to the external atmosphere through the oropharynx and the rectum. At infrasound frequencies:

- Wavelength in air: $\lambda = 343/7 \approx 49$ m $\gg$ GI tract length (~8 m)
- Wavelength in tissue: $\lambda = 1540/7 \approx 220$ m $\gg$ body size

Both paths deliver $p_\mathrm{inc}$ to the gas pocket essentially simultaneously and in-phase. The tissue (serosal side) delivers $P_0 + p_\mathrm{inc}\sin(\omega t)$. The luminal air column (connected to the external field through mouth/anus) also delivers $P_0 + p_\mathrm{inc}\sin(\omega t)$. If both pressures are equal and in-phase, the **net differential pressure on the gas pocket is zero** and there is no compression.

The model is valid only if gas pockets are effectively **sealed** — trapped between liquid/fecal plugs that prevent rapid pressure equalization through the luminal air column. This sealing is plausible (haustral segmentation in the colon, liquid boluses in the small intestine), but it is a **critical modeling assumption** that the paper completely fails to discuss.

A rough Helmholtz-resonator estimate for a 10 mL pocket connected to the lumen by a 10 cm air column of 5 mm radius gives $f_H \approx 15$ Hz. At 7 Hz (below this Helmholtz resonance), the pocket can partially equilibrate through the luminal connection, meaning the effective driving pressure is **less than** $p_\mathrm{inc}$. This directly affects all threshold calculations.

**Required action:**
1. Explicitly state and justify the sealed-pocket assumption
2. Estimate the Helmholtz resonance of pocket + luminal connection
3. Discuss how partially open pockets reduce the effective driving pressure
4. Assess what fraction of bowel gas pockets are typically sealed vs. open

---

## Major Issues

### M1. Internal Inconsistency: Cylindrical SPL Threshold (Sec. 3.2 vs. Code)

Line 488 states that cylindrical pockets have a threshold of "~118 dB." Running the code (`gas_pocket_detailed.py`, binary search for 0.5 µm at 7 Hz) gives **~113.5 dB** for all cylindrical volumes (5–100 mL). This is confirmed by manual calculation:

$$k_\mathrm{eff}^{(\mathrm{cyl})} = \frac{2\gamma P_0}{R} + \frac{E_w h_w}{R^2(1-\nu_w^2)} = 19{,}081{,}189\;\text{Pa/m}$$

$$\text{SPL}_\mathrm{thresh} = 20\log_{10}\!\left(\frac{0.5\times 10^{-6} \times 19{,}081{,}189}{20\times 10^{-6}}\right) = 113.6\;\text{dB}$$

This is a **5 dB discrepancy** between the paper text and its own code. Since the code is correct (verified analytically), the text at line 488 must be corrected.

### M2. Overclaiming: "50–100×" Amplification Factor

The paper repeatedly claims gas pockets are "50–100× more efficient" than whole-cavity resonance (abstract line 85, Sec. 3.4, Sec. 5). Computation shows:

| Pocket | $\xi$ (µm) | Ratio vs. 0.014 µm |
|--------|-------------|---------------------|
| 5 mL sphere | 0.487 | **35×** |
| 20 mL sphere | 0.780 | 56× |
| 50 mL sphere | 1.062 | 76× |
| 100 mL sphere | 1.341 | 96× |
| Any cylindrical | ~1.05 | 75× |

For the smallest physiologically relevant pockets (5 mL), the ratio is only 35×. The "50–100×" claim requires restricting to pockets > 10 mL. This should be stated as **"35–100×"** or qualified with a volume range.

### M3. The PIEZO Threshold Comparison Is Apples-to-Oranges

The PIEZO activation threshold of 0.5 µm (line 393) comes from Coste et al. (2010), who measured membrane indentation via a **glass micropipette pressing directly on a cell membrane** in vitro. The paper equates this with radial displacement of a gas–tissue interface that is separated from the mechanosensitive cells by the **full thickness of the intestinal wall** (3 mm).

Key issues:
1. **Spatial scale mismatch:** Patch-clamp indentation is applied over ~1–2 µm²; gas pocket oscillation affects the entire luminal surface area.
2. **Attenuation through wall:** If PIEZO channels are in the myenteric plexus (outer part of muscularis), the displacement is attenuated by $(a/(a+h_w))^2$. For a 10 mL spherical pocket (a = 13.4 mm), this gives 67% of luminal displacement, potentially dropping below threshold.
3. **Strain vs. displacement:** PIEZO channels may respond to membrane strain, not absolute displacement. The strain at the cell membrane from a 1 µm bulk tissue oscillation is not well characterized.

The paper acknowledges this in the limitations (line 663), but the threshold comparison throughout the paper presents it as established fact rather than a rough order-of-magnitude estimate. The language should consistently reflect this uncertainty.

### M4. Wall Constraint Is Physically Negligible but Rhetorically Central

The paper's title and framing emphasize the "constrained bubble model" — Minnaert dynamics modified for the elastic intestinal wall. However, the wall stiffness contribution to $k_\mathrm{eff}$ is only **0.9–2.4%** of the total:

| Pocket | $k_\mathrm{gas}$ | $k_\mathrm{wall}$ | Wall fraction |
|--------|-------------------|---------------------|---------------|
| 5 mL sphere | 13.5 MPa/m | 330 kPa/m | 2.4% |
| 100 mL sphere | 14.8 MPa/m | 132 kPa/m | 0.9% |
| Any cylinder | 18.9 MPa/m | 167 kPa/m | 0.9% |

The "constrained bubble" is, for all practical purposes, a **free bubble**. The displacement differs by only 1–2% between free and elastic-wall cases. This should be stated explicitly. The elaborate elastic-shell formulation (Eqs. 3–6, 8, 14, 18, 19), while correct, creates an impression of physical sophistication that masks the fact that gas compressibility completely dominates.

### M5. Monte Carlo Result Is Tautological Given Geometry Assumptions

The 100% population exceeding threshold (Sec. 3.3) is driven by the fact that **all cylindrical pockets exceed threshold regardless of volume**, because $k_\mathrm{eff}$ depends only on the fixed lumen radius $R = 15$ mm. Since 70% of pockets are assigned cylindrical geometry, every simulated individual has at least one cylindrical pocket with $\xi \approx 1.05$ µm $> 0.5$ µm.

This is not a biological finding — it's an artifact of the modeling choices. If all pockets were spherical, the smallest individuals (30 mL total gas, 40 pockets, max pocket ~2 mL) would produce $\xi \approx 0.37$ µm, **below threshold**. The 100% claim should be qualified with its dependence on the geometry assumption.

### M6. $P_0$ Should Include Intra-Abdominal Pressure

Table 1 (line 189) defines $P_0$ as "ambient + intra-abdominal pressure" but uses the value 101,325 Pa, which is atmospheric pressure only. Intra-abdominal pressure (IAP) is typically 500–2000 Pa (supine) and can reach 5000 Pa (standing, Valsalva). The code (`gas_pocket_detailed.py`, line 58) also uses 101,325 Pa.

While IAP is only 0.5–2% of atmospheric, and its omission doesn't materially affect results, the table description is incorrect. Either change the description to "Atmospheric pressure" or add IAP to the value.

---

## Minor Issues

### m1. Equation (10) Denominators Need Clarification

Eq. (10) for the cylindrical radial mode has the denominator $R^2(\rho_f R + \rho_w h_w)$, which has units of m² × (kg/m³ × m + kg/m³ × m) = m² × kg/m² = kg. But the numerator has units of Pa = kg/(m·s²). So $\omega^2$ has units 1/(m·s²) × (1/kg) × ... The dimensional analysis should be shown or verified. Looking at the code (line 165), it matches the equation, but the reader would benefit from seeing the full derivation to confirm units.

### m2. Impedance Mismatch Ratio

Line 129 states "~3600:1" for the gas–tissue impedance ratio. The actual ratio $Z_\mathrm{tissue}/Z_\mathrm{air} = (\rho_\mathrm{tissue} c_\mathrm{tissue})/(\rho_\mathrm{air} c_\mathrm{air}) = 1{,}570{,}800/420 = 3738$:1 for air at STP, or ~4000:1 for bowel gas at 37°C. The "3600:1" figure appears to be an approximation that doesn't match either case precisely. State the calculation or cite a source.

### m3. Missing Frequency Dependence Discussion

The paper emphasizes that the sub-resonant response is "frequency-independent" (line 332) and "broadband" (line 139). This is true for the gas compressibility term, but the cylindrical axial mode can have $f_0$ as low as 31 Hz (100 mL pocket), giving $r = 7/31 = 0.23$ at 7 Hz. The frequency response function $H(7\;\text{Hz}) = 1.049$ in this case — a 5% enhancement. While small, this contradicts the claim of strict frequency independence. The text should note that the largest cylindrical pockets show weak frequency dependence at the upper end of the infrasound band.

### m4. Table 2: Missing Units/Labels

The column headers "$a$ or $R$ [mm]" and "$f_0$ [Hz]" are fine, but the cylindrical entries show $R = 15.0$ mm for all volumes. It would be helpful to also show the length $L$ for cylindrical pockets to give the reader a physical picture (e.g., 100 mL cylindrical pocket has $L = 141$ mm).

### m5. Damping Model: $\delta_\mathrm{wall} = 0.3$ Needs a Source

The structural loss factor for the intestinal wall is set to $\delta_\mathrm{wall} = 0.3$ (line 304) without citation. While this is within the range of soft biological tissues (0.1–0.5), a peer-reviewed source should be cited. This value dominates the total damping (δ_wall >> δ_rad + δ_th + δ_vis), though it doesn't affect results since we're in the sub-resonant regime.

### m6. Reference Formatting Issues

- Gregersen (2000): the journal volume (line 243 of bib) says "8" but that paper is from Neurogastroenterology and Motility vol. 8, or possibly a review elsewhere. Verify.
- Iovino (2006): volume 109 of Gastroenterology doesn't match 2006 publication year. Gastroenterology vol. 109 is from 1995.

### m7. Thermal Damping Value

$\delta_\mathrm{th} \approx 0.04$ is stated as a constant (line 299), appropriate for bubbles in water at ultrasound frequencies. At infrasound frequencies, the thermal diffusion length $l_\mathrm{th} = \sqrt{2\kappa/\omega} \approx 1.0$ mm at 7 Hz, which is small compared to pocket radii (6–29 mm). The adiabatic assumption is reasonable, but $\delta_\mathrm{th} = 0.04$ should be justified for this specific frequency regime, not simply imported from the ultrasound bubble literature.

### m8. Abstract Overclaiming

The abstract states this is "the only plausible mechanism by which airborne infrasound could induce GI mechanotransduction" (lines 87–89). This is too strong. The paper shows this mechanism is more efficient than whole-cavity resonance by 1–2 orders of magnitude, but has not demonstrated that no other mechanism exists (e.g., direct vibrotactile coupling through the abdominal wall, peristaltic entrainment, or thoracic pressure coupling via the diaphragm).

---

## Positive Aspects

1. **The core physical insight is sound.** Gas pockets as compressible inclusions in incompressible tissue is the correct framework. The analogy with ultrasound contrast agent microbubbles (Sec. 4.3) is apt and well-drawn.

2. **The mathematics is correct.** I verified all governing equations (Eqs. 1–19) against both the code and independent derivation. The Minnaert formulation, elastic shell modifications, damping model, and forced-response function are all standard and properly applied.

3. **Code-paper consistency is good (with exceptions noted).** Table 2 resonance frequencies match the code exactly. The displacement values at 120 dB match. The only discrepancy is the cylindrical threshold text (M1).

4. **Honest limitations section.** Section 4.4 acknowledges five significant limitations, including the lack of experimental validation. This is commendable.

5. **Testable predictions.** The four predictions in Sec. 5 (correlation with gas content, post-prandial susceptibility, simethicone attenuation, broadband response) are specific and experimentally accessible. This is good science.

6. **The paper fills an important gap.** Paper 1 showed airborne coupling is negligible; this paper proposes a viable alternative. The logical progression is compelling.

7. **The sub-resonant compliance argument is the key insight** and is physically correct: you don't need resonance to get displacement; you just need compressibility. This is under-appreciated in the infrasound biology literature.

---

## Summary

This paper presents a physically well-motivated model with correct governing equations and an important insight about sub-resonant compliance. However, the failure to address the acoustic short-circuit problem (F1) is a serious gap — it could reduce the effective driving pressure by an order of magnitude for open gas pockets. The cylindrical threshold discrepancy (M1) and pervasive overclaiming (M2, M5, m8) erode confidence. The PIEZO threshold comparison (M3) conflates in-vitro patch-clamp indentation with bulk tissue oscillation. The wall constraint being negligible (M4) makes much of the formalism ornamental.

After addressing F1 and M1–M6, this paper would make a valuable contribution to JASA. The core argument is correct: gas pockets DO amplify tissue displacement relative to whole-cavity resonance, and the sub-resonant compliance mechanism IS the right framework. But the paper must be more careful about what it has actually shown versus what it has assumed.

**Bottom line:** Fix the acoustic short-circuit discussion, correct the numerical inconsistencies, and temper the claims. Then this is publishable.
