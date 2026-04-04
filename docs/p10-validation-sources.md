# P10 validation sources: external modal / stiffness datasets for fluid-filled shells

## Bottom line

Paper 10 currently cites shell theory, inverse-problem theory, elastography reviews, and fruit-NDT reviews, but it **does not yet cite enough primary external datasets** that a *Proc. Roy. Soc. A* reviewer would regard as independent validation. The strongest additions are:

1. **Amabili, Pagnanelli & Pellegrini (2001)** — experimental modal analysis of a **water-filled cylindrical shell** with measured empty vs filled frequencies.
2. **Curadelli et al. (2010)** — **spherical container partially filled with water**, with FEM + experiment.
3. **Piacsek, Abdul-Wahid & Taylor (2012)** — **spherical aluminum shell under internal pressure**, directly relevant to prestress / fill-pressure tuning.
4. **Zhang et al. (2024)** — **PE pipeline** modal experiment + theory + FE, with <6% experiment/model disagreement.
5. **Sturm et al. (2017)** — **bladder shear-wave elastography** during filling; external clinical evidence that geometry/filling changes effective wall-wave response.
6. **Rusak et al. (2015)** — **healthy liver MR elastography** at a known drive frequency, useful for organ-scale modulus calibration.
7. **Yamamoto, Iwamoto & Haginuma (1980/1981)** and **De Belie et al. (2000)** — classic **fruit acoustic resonance** data supporting P7-style shell inversion.

The reviewer-proof move is to present these sources not as one undifferentiated literature dump, but as a **claim-by-claim evidence matrix**:

- **forward modal plausibility**
- **fill / stiffness / geometry change the spectrum**
- **symmetry breaking lifts degeneracy**
- **forward agreement does not guarantee inverse identifiability**

---

## What is missing from `papers/paper10-capstone/references.bib`

The current bibliography already contains:

- shell monographs: **Leissa (1973)**, **Soedel (2004)**, **Junger & Feit (1986)**
- inverse-problem / model-updating foundations: **Kac (1966)**, **Gladwell (2004, 2005)**, **Mottershead & Friswell (1993)**, **Friswell & Mottershead (1995)**
- elastography reviews: **Doyley (2012)**, **Parker et al. (2011)**, **Sack (2023)**
- fruit-NDT reviews / classics: **Yamamoto (1980)**, **Abbott et al. (1997)**

It **does not yet include** most of the primary external validation papers that would matter most for P10:

- water-filled shell / tank modal experiments (**Amabili et al. 2001**)
- spherical container FEM+measurement (**Curadelli et al. 2010**)
- pressurised spherical shell resonance (**Piacsek et al. 2012**)
- modern pipeline modal validation (**Zhang et al. 2024**)
- bladder SWE under filling (**Sturm et al. 2017**)
- liver MRE primary dataset (**Rusak et al. 2015**)
- pear/apple resonance primary data (**De Belie et al. 2000**)
- classical shell experiments not already represented by books (**Warburton 1965; Warburton & Higgs 1970**)
- explicit symmetry-breaking / mode-splitting shell experiments (**Duffey et al. 2005**)

---

## Evidence matrix by Paper 10 claim

### A. Most promising datasets

| Source | Geometry | What was measured | Key numerical values | P10 use | Support strength |
|---|---|---|---|---|---|
| **Amabili, Pagnanelli & Pellegrini (2001)**, *Experimental modal analysis of a water-filled circular cylindrical tank*, WIT Trans. Built Env. 56, 241-250. DOI: **10.2495/FSI010241** | Thin circular cylindrical steel tank; reported dimensions approx. **L = 1.26 m, D = 0.433 m, h = 1.35 mm** | Experimental modal frequencies + mode shapes for empty and water-filled shell | Web-accessible summary reports first three empty frequencies approx. **57.65, 63.49, 76.90 Hz** and filled frequencies **49.81, 55.87, 67.75 Hz**; about **12-14% downward shift** on filling | Best external benchmark for **fluid added-mass shifting a shell spectrum**; supports P10’s forward model and geometry-organised modal structure | **Partial analogue** (cylindrical, not oblate) |
| **Curadelli, Ambrosini, Mirasso & Amani (2010)**, *Resonant frequencies in an elevated spherical container partially filled with water: FEM and measurement*, *J. Fluids Struct.* 26(1), 148-159. DOI: **10.1016/j.jfluidstructs.2009.10.002** | Elevated spherical tank, partially filled | Measured and FEM-predicted resonant frequencies vs fill level | Full paper reports frequency-vs-fill tables/plots; summary confirms **monotonic frequency decrease with increasing water level** and that a **three-mass reduced model** is needed for acceptable fidelity | Strongest non-biological **spherical** analogue; supports claims that **fill geometry changes the spectrum** and that oversimplified reduced models lose information | **Direct/partial** (sphere rather than oblate shell) |
| **Piacsek, Abdul-Wahid & Taylor (2012)**, *Resonance frequencies of a spherical aluminum shell subject to static internal pressure*, *J. Acoust. Soc. Am.* 131, 506-512. DOI: **10.1121/1.4721647** | Spherical aluminum shell, air- or water-filled, under static internal pressure | Resonance-frequency shift with pressure | Public summaries state some resonances shift **proportionally with internal pressure**, independent of whether the shell is filled with air or water; exact shift tables likely require institutional access | Very high-value citation for **prestress / internal-pressure tuning** of shell spectra; would strengthen P10’s geometry + preload narrative | **Direct analogue** |
| **Zhang et al. (2024)**, *Modal analysis of PE pipeline under seabed dynamic pressure*, *Scientific Reports* 14, Art. 29198. DOI: **10.1038/s41598-024-80583-z** | Polyethylene cylindrical pipeline treated as thin-walled shell | First three modal frequencies + mode shapes; experiment vs theory vs COMSOL | Reported **<6% discrepancy** between experiment, theory and FE; **<5%** between theory and FE; radius, thickness, length and load were swept | Good modern SHM-style evidence that geometry and loading are experimentally recoverable in fluid-carrying shell-like structures | **Partial analogue** |
| **Sturm et al. (2017)**, *Ultrasound Shear Wave Elastography: A Novel Method to Evaluate Bladder Pressure*, *J. Urol.* DOI: **10.1016/j.juro.2017.03.127** | Human bladder wall during filling | Shear-wave velocity (SWE) vs filling/pressure | In “safe” bladders: **1.46 ± 0.05 m/s** empty to **1.49 ± 0.09 m/s** end fill; in “hostile” bladders: **1.49 ± 0.11 m/s** empty to **2.01 ± 0.12 m/s** end fill; **p = 0.007**, overall pressure correlation **p < 0.0001** | Best clinical external evidence that **filling geometry / wall tension changes dynamic response** in a hollow organ | **Partial analogue** |
| **Rusak et al. (2015)**, *Whole-organ and segmental stiffness measured with liver magnetic resonance elastography in healthy adults: significance of the region of interest*, *Abdominal Imaging* 40, 776-782. DOI: **10.1007/s00261-014-0278-7** | Human liver | Whole-organ MRE stiffness at known drive frequency | Healthy whole-liver stiffness **1.56-2.75 kPa** at **64 Hz** excitation | External organ-scale modulus / drive-frequency datum for calibrating “soft, fluid-rich abdominal organ” parameter ranges | **Contextual / partial analogue** |
| **Yamamoto, Iwamoto & Haginuma (1980)**, *Acoustic impulse response method for measuring natural frequency of intact fruits and preliminary applications to internal quality evaluation of apples and watermelons*, *J. Texture Studies* 11, 117-136 | Whole apples and watermelons | Acoustic natural frequencies from impact testing | Classical fruit resonance dataset; later follow-up reports apples typically in the **~500-1200 Hz** range depending on cultivar/ripeness | Independent support for P7/P10 claim that **shell-like produce geometry and stiffness are inferable from resonance** | **Direct analogue for P7-style application** |
| **Yamamoto, Iwamoto & Haginuma (1981)**, *Nondestructive acoustic impulse response method for measuring internal quality of apples and watermelons*, *J. Japan. Soc. Hort. Sci.* 50(2), 247-261 | Whole apples and watermelons | Natural frequencies + firmness indices vs storage/ripeness | Extracted text reports apple firmness index **m f² ≈ 1.7 × 10^8 Hz² g**; watermelons analysed using the **first three peaks**; power spectrum resolved over **0-2500 Hz** with **4.89 Hz** resolution | Stronger than the 1980 paper for quantitative fruit-quality comparison; useful to justify shell inversion outside Browntone | **Direct analogue for P7-style application** |
| **De Belie, Duquaine & De Baerdemaeker (2000)**, *Instrumental measurement of fruit firmness*, *Postharvest Biol. Technol.* 18(1), 45-55. DOI reported in secondary databases as **10.1016/S0925-5214(99)00069-7** | Apples / pears | Resonance-based firmness indices vs destructive firmness | Secondary summaries report resonant frequencies typically **~400 Hz to >1 kHz** depending on fruit and maturity | Reinforces that external resonance data can recover internal firmness in non-spherical biological shells | **Direct analogue for P7-style application** |

### B. Additional high-value contextual sources

These are useful, but they are either less direct or I could not harvest exact frequency tables from open sources during this pass.

| Source | Why it matters | Validation scope |
|---|---|---|
| **Warburton (1965)**, *Vibration of Thin Cylindrical Shells*, *J. Mech. Eng. Sci.* 7, 399-407. DOI: **10.1243/JMES_JOUR_1965_007_062_02** | Classical experimental shell-frequency baseline in vacuo | Validates the **shell-only limit**, not fluid filling |
| **Warburton & Higgs (1970)**, *Natural Frequencies of Thin Cantilever Cylindrical Shells*, *J. Sound Vib.* 11, 335-338. DOI: **10.1016/S0022-460X(70)80037-2** | Another shell-only experimental benchmark | Good for the “empty-shell / vacuum” control case |
| **Duffey et al. (2005)**, *Vibrations of Complete Spherical Shells with Imperfections*, IMAC-XXIII, LA-UR-04-9778 | Explicit experiment on symmetry breaking / imperfection-induced frequency splitting; summary reports splitting in the **40-70 Hz** range for a **152 mm** diameter, **1.6 mm** thick shell | Best external analogue for P10/P9 claim that **breaking spherical symmetry lifts degeneracy** |
| **Akkas (1975)**, *Dynamic analysis of a fluid-filled spherical sandwich shell—a model of the human head*, *J. Biomech.* 8, 275-284. DOI: **10.1016/0021-9290(75)90079-2** | Early fluid-filled spherical-shell biomechanics model | More contextual than validating, but very relevant precedent |
| **El Baroudi, Razafimahery & Rakotomanana-Ravelonarivo (2012)**, *Study of a spherical head model. Analytical and numerical solutions in fluid-structure interaction approach*, *Int. J. Eng. Sci.* 51, 1-13. DOI: **10.1016/j.ijengsci.2011.11.007** | Analytical + numerical FSI for a shell/brain/CSF system | Supports organ-scale FSI plausibility, not identifiability directly |

---

## Which Paper 10 claim each source can support

### 1. Forward modal plausibility

**Best support**

- **Amabili et al. (2001)** — experimental shell modes shift downward when the shell is filled.
- **Curadelli et al. (2010)** — spherical container frequencies decrease with liquid level, with FEM/measurement agreement.
- **Zhang et al. (2024)** — experiment/theory/FE pipeline frequencies agree within 5-6%.
- **Warburton (1965)** — shell-only benchmark for the empty-shell limit.

**What this validates in P10**

- Our shell framework is not an isolated Browntone construction; the same qualitative frequency shifts appear in **external shell-fluid experiments**.
- A reviewer can no longer say “you only showed that your own model predicts its own frequencies”.

### 2. Equivalent-radius reduction loses information

**Best support**

- **Curadelli et al. (2010)** — the note that at least **three lumped masses** are needed is useful rhetorical support against over-aggressive reduction.
- **Sturm et al. (2017)** — bladder response depends on filling state; one scalar “effective radius” is unlikely to capture both geometry and tension.
- **Rusak et al. (2015)** — segmental vs whole-organ stiffness variability reinforces that spatial structure matters.

**How to use it**

These papers do **not** directly prove rank deficiency of equivalent-radius models, but they support the argument that **single-parameter reductions erase physically relevant structure**.

### 3. Asphericity / symmetry breaking lifts separability

**Best support**

- **Duffey et al. (2005)** — direct imperfection-induced lifting of spherical degeneracy.
- **Warburton / shell experiments** — classical repeated-mode behaviour in symmetric shells.

**How to use it**

This is the cleanest external analogue for the P9/P10 thesis that **symmetry creates degeneracy and broken symmetry separates modes**. It is still an analogue, not a one-to-one validation of the specific oblate-shell theorem.

### 4. Forward adequacy != inverse adequacy

**Best support**

- **Mottershead & Friswell (1993)** and **Friswell & Mottershead (1995)** — already in the bib, but should be cited more explicitly in the capstone discussion.
- **Bartilson (2019)**, *Model updating in structural dynamics: advanced parametrization, regularization and balancing*, Columbia dissertation — explicit discussion of ill-conditioning, non-uniqueness and sensitivity-rank issues in vibration-based updating.
- **Zhang et al. (2024)** — useful as an example where forward agreement is good, but inverse observability is not the same claim.

**How to use it**

State explicitly that:

> External SHM/model-updating literature agrees with the capstone’s distinction between matching measured frequencies and uniquely recovering the parameters that generated them.

That sentence is defensible even if the external papers do not use our exact oblate-shell geometry.

---

## Specific numerical comparisons worth adding to P10

### Comparison 1: fluid loading shifts shell frequencies downward

- **External datum:** Amabili et al. (2001), cylindrical tank  
  Empty: **57.65, 63.49, 76.90 Hz**  
  Filled: **49.81, 55.87, 67.75 Hz**  
  Relative drop: about **13.6%, 12.0%, 11.9%**

**Suggested use in P10:** add a short paragraph noting that the sign and order of the fluid-loading shift seen in Browntone are consistent with external shell experiments.

### Comparison 2: fill level changes spherical-container resonances

- **External datum:** Curadelli et al. (2010), spherical container  
  Frequency decreases monotonically with water level; FEM tracks measurement closely.

**Suggested use in P10:** cite as the spherical engineering analogue of our bladder/fill-geometry story.

### Comparison 3: filling stiffens / retensions organ walls

- **External datum:** Sturm et al. (2017), bladder SWE  
  Safe bladders: **1.46 -> 1.49 m/s**  
  Hostile bladders: **1.49 -> 2.01 m/s**

**Suggested use in P10:** this directly supports the statement that **changing fill state changes both geometry and effective dynamic stiffness**, which is one of the capstone’s core mechanistic claims.

### Comparison 4: abdominal-organ stiffness scale is plausible

- **External datum:** Rusak et al. (2015), liver MRE at **64 Hz**  
  Healthy whole-organ stiffness: **1.56-2.75 kPa**

**Suggested use in P10:** use as an external order-of-magnitude sanity check for soft-organ viscoelastic parameters.

### Comparison 5: shell-like biological objects really do admit resonance-based inversion

- **External datum:** Yamamoto et al. (1981)  
  Apple firmness index **m f² ≈ 1.7 × 10^8 Hz² g**  
  Watermelons analysed through **first three resonance peaks**

**Suggested use in P10:** this is the cleanest external bridge from Paper 7 to the capstone: resonance-based parameter inference in biological, fluid-rich objects is not just a Browntone invention.

### Comparison 6: symmetry breaking lifts degeneracy

- **External datum:** Duffey et al. (2005)  
  Imperfect spherical shells exhibited splitting in the **40-70 Hz** range.

**Suggested use in P10:** use this as an external analogue to the P9 theorem: exact symmetry produces repeated or near-repeated modes; imperfections / asphericity split them.

---

## Recommended additions to P10's results section

### Recommended new subsection

Add a short subsection after the main theorem/results discussion:

## External validation analogues

Suggested structure:

1. **Shell / tank benchmarks**
   - Amabili et al. (2001)
   - Curadelli et al. (2010)
   - Zhang et al. (2024)

2. **Organ-scale dynamic measurements**
   - Sturm et al. (2017)
   - Rusak et al. (2015)

3. **Biological acoustic inversion precedents**
   - Yamamoto et al. (1980, 1981)
   - De Belie et al. (2000)

4. **Symmetry-breaking analogue**
   - Duffey et al. (2005)

### Recommended text-level claims

Safe claims:

- “Independent experiments on fluid-loaded cylindrical and spherical shells report modal downshifts of the same qualitative type predicted by the present framework.”
- “Clinical bladder and liver elastography provide external organ-scale dynamic measurements in the same stiffness regime as the present model.”
- “Fruit acoustic-resonance studies show that resonance-based inference of internal mechanical state is already established outside the present work.”
- “Classical symmetry-breaking experiments on shells support the broader claim that geometric departure from exact symmetry separates previously clustered modes.”

Avoid overclaiming:

- Do **not** say these papers externally prove the exact **oblate near-sphere asymptotics**.
- Do **not** say they directly validate the full identifiability theorem.
- Do say they provide **independent forward and mechanistic support**, plus external analogues for symmetry breaking and inverse ill-conditioning.

### Recommended figure/table addition

Add a compact table in P10:

| External source | Geometry | Observable | Quantitative result | Which P10 claim it supports |
|---|---|---|---|---|

If space is tight, put the full version in the supplement and cite the short version in the main text.

---

## Practical next steps before revising the manuscript

1. **Add to `references.bib` first**
   - Amabili et al. (2001)
   - Curadelli et al. (2010)
   - Piacsek et al. (2012)
   - Zhang et al. (2024)
   - Sturm et al. (2017)
   - Rusak et al. (2015)
   - De Belie et al. (2000)
   - Warburton (1965)
   - Warburton & Higgs (1970)
   - Duffey et al. (2005) if report citations are acceptable

2. **Harvest exact tables from subscription-gated papers**
   - Piacsek et al. (2012)
   - Curadelli et al. (2010)
   - any exact Warburton frequency tables needed for an appendix comparison

3. **Use external evidence honestly**
   - **Direct validation:** fluid-loaded shell spectra, fruit resonance inversion
   - **Partial analogy:** bladder/liver elastography
   - **Context only:** model-updating ill-conditioning literature

4. **Rewrite one paragraph in P10 explicitly distinguishing**
   - forward agreement,
   - geometry-mediated modal separation,
   - inverse identifiability.

That distinction is already the paper’s conceptual core; these citations finally give it external anchors.
