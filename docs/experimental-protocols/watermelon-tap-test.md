# Experimental Validation Protocol — Watermelon Tap-Test for Paper 7

## 1. Validation Target
- **Claim to test:** The Paper 7 shell model predicts that the lowest measurable structural resonance of an intact watermelon is the `n = 2` flexural mode, and that its frequency decreases as ripeness increases because rind stiffness drops faster than geometry changes.
- **Predicted value(s):**
  - Canonical Crimson Sweet model (`a = 0.158 m`, `c = 0.123 m`) predicts:
    - unripe: **203 Hz**
    - turning: **147 Hz**
    - ripe: **89.9 Hz**
    - overripe: **46.4 Hz**
  - For the cultivar/size range already used in Paper 7, ripe fruit are expected broadly in **80-120 Hz** and unripe fruit in **120-180 Hz**, with smaller fruit shifted upward and larger fruit shifted downward.
  - Geometry matters strongly, so each fruit will also be analysed using the equivalent-radius scaling
    `f ~ R_eq^(-3/2)`, where `R_eq = (a^2 c)^(1/3)`.
- **Required level of agreement:**
  - **Trend validation:** frequency must decrease monotonically with destructive ripeness/firmness class.
  - **Absolute validation:** median measured-versus-model frequency error after geometry correction should be **<= 15%**, with no class-wise bias worse than **20%**.
  - **Measurement precision target:** expanded uncertainty in extracted resonance frequency **<= 4 Hz** (`k ~ 2`), so adjacent class differences of `>= 20 Hz` remain resolvable.

## 2. Minimum Convincing Experiment
- **Experiment type:** Impact-excited tap test on intact watermelons, measured primarily with a close microphone and optionally cross-checked on a subset with a lightweight accelerometer or borrowed LDV.
- **Why this is the minimum credible test:**
  - It measures the model’s actual observable: **resonant frequency of the intact fruit**.
  - It avoids ethics approval and uses equipment that can be purchased for **well under $2000**.
  - One person can run it in a normal lab with a sling support, a pendulum striker, and destructive ripeness measurements after the acoustic test.
  - It gives both:
    1. a **frequency-versus-ripeness** validation, and
    2. a **measured-versus-predicted frequency** comparison using each fruit’s own geometry.
- **What Reviewer B would still object to:**
  - A microphone-only study does **not** directly identify mode shape.
  - Destructive Brix and firmness are proxies for the model’s rind modulus; they are not a direct modulus measurement.
  - The model assumes a free shell, while the real fruit sits in a sling.
  - Mitigation: add an **accelerometer or LDV subset check on 3-5 melons** if such equipment is available; otherwise present the experiment honestly as a minimum viable validation of the resonance-frequency prediction, not a full elastographic inversion study.

## 3. Equipment

| Item | Essential? | Assumed available? | Substitute |
|------|------------|--------------------|------------|
| USB measurement microphone (e.g. miniDSP UMIK-1) | Yes | No | ECM8000 + USB audio interface |
| Laptop with Python, NumPy, SciPy, Matplotlib | Yes | Yes | Existing lab PC |
| Pendulum tap rig: frame, string, 40-60 g rubber ball striker | Yes | No | Rubber-tipped small hammer with fixed stop |
| Soft sling support (elastic cord or fabric hammock) | Yes | No | Open-cell foam ring, if very soft |
| Digital scale, 0-15 kg, resolution <= 5 g | Yes | No | Bench scale in shared lab |
| Callipers + flexible tape measure | Yes | No | Two rulers + contour tape, but worse |
| Digital thermometer | Yes | No | IR thermometer |
| Brix refractometer, 0-20 degBx | Yes | No | Shared food science refractometer |
| Fruit penetrometer / firmness tester, 8 mm tip | Yes | No | Digital force gauge + probe stand |
| Knife, cutting board, sample cups, wipes | Yes | No | Standard food-prep kit |
| Lightweight accelerometer (<= 1.5 g) | Desirable | Maybe | Omit; use microphone only |
| USB DAQ / oscilloscope for accelerometer | Desirable | Maybe | Borrow NI/Dewesoft, or omit |
| Single-point LDV | Desirable | Maybe | Omit; use microphone + accelerometer |
| Acoustic calibrator (94 dB @ 1 kHz) | Desirable | Maybe | Manufacturer mic calibration file |
| Vibration calibrator for accelerometer | Desirable | Maybe | Reference tap on stiff beam; frequency only |

### Budget estimate

| Item | Qty | Unit cost (USD) | Total (USD) |
|------|-----|------------------|-------------|
| USB measurement mic | 1 | 120 | 120 |
| Pendulum rig materials | 1 | 50 | 50 |
| Sling/support materials | 1 | 40 | 40 |
| Bench scale | 1 | 40 | 40 |
| Callipers + tape | 1 | 35 | 35 |
| Thermometer | 1 | 20 | 20 |
| Brix refractometer | 1 | 30 | 30 |
| Fruit penetrometer | 1 | 250 | 250 |
| Consumables (cups, gloves, wipes, wax, markers) | 1 | 75 | 75 |
| 24 watermelons (consumable, not equipment) | 24 | 6 | 144 |
| Optional lightweight accelerometer + simple DAQ | 1 | 350 | 350 |
| Optional mic calibrator | 1 | 180 | 180 |
| **Essential purchased total** |  |  | **660** |
| **Likely pilot total including fruit** |  |  | **804** |
| **Enhanced total with accelerometer + calibrator** |  |  | **1,334** |

This remains below the requested **$2000** cap even without assuming LDV access.

## 4. Specimen / Phantom
- **Specimen type:** Intact commercial watermelons; no human or animal ethics required.
- **Cultivar strategy:** Use **one cultivar only** for the primary experiment. Recommended: **Crimson Sweet-type** or a single seedless commercial cultivar from one grower. Do **not** mix cultivars in the pilot; Paper 7 already shows geometry is a major sensitivity driver.
- **Important biological constraint:** Watermelons are **non-climacteric**. They do not continue meaningful ripening after harvest. Therefore, do **not** create “ripeness stages” by leaving fruit on a bench for a week and pretending they ripened. The fruit must be sourced at different **harvest maturities** or classified **post hoc** by destructive ground truth.
- **Minimum sample selection:**
  - **Minimum publishable pilot:** `N = 18` total, `6` per maturity band.
  - **Preferred minimum convincing data set:** `N = 24` total, `8` per band.
  - Bands:
    1. **Early/under-mature harvest**
    2. **Commercial-ripe harvest**
    3. **Late harvest / soft / over-mature**
- **Sample size rationale:**
  - Conservative adjacent-stage difference to detect after geometry scatter: `Delta f = 25 Hz`
  - Conservative within-stage SD after geometry control: `sigma = 15 Hz`
  - Two-sample power calculation:
    `n/group ~ 2 (z_(0.975) + z_(0.8))^2 sigma^2 / Delta f^2`
    `= 2 (1.96 + 0.84)^2 (15^2) / 25^2 ~ 5.6`
  - So **6 fruit per class** is the true minimum for pairwise stage separation.
  - If analysing the continuous relation between geometry-corrected frequency and a destructive ripeness index with expected correlation `r ~ 0.60`, Fisher-z gives **N ~ 20** for `alpha = 0.05`, `power = 0.80`.
  - Hence: **18 works as a floor; 24 is the better target.**
- **Geometry inclusion criteria:**
  - Mass: **4-8 kg**
  - Equatorial diameter: **200-320 mm**
  - No visible cracks, flat spots, major bruises, or gross asymmetry
  - No fruit with stem-end damage or obvious dehydration
- **Fabrication method:** Not applicable; intact fruit only.
- **Tolerances / control limits:**
  - Keep all fruit at **20 +/- 1 C** for at least **12 h** before testing
  - Measure each fruit’s mass to **<= 5 g**
  - Measure equatorial and polar diameters to **<= 1 mm**
  - After cutting, measure rind thickness at **6 locations** to **<= 0.5 mm**

## 5. Measurement Setup
- **Excitation:**
  - Primary: **pendulum tap test** with a rubber striker.
  - Striker mass: **40-60 g**
  - Pendulum length: **250 +/- 10 mm**
  - Release angle: start at **20 deg**; increase to **30 deg** only if SNR is inadequate.
  - This gives repeatable impact energy without paying for an instrumented hammer.
- **Why not speaker sweeps as the primary method?**
  - Paper 7 predicts a structural resonance. A direct tap excites it efficiently.
  - Airborne swept-sine excitation adds room modes, low-frequency speaker distortion, and poor coupling.
  - Speaker/white-noise excitation is useful only as a later refinement, not as the minimum viable validation.
- **Boundary conditions:**
  - Suspend each melon in a **3-point elastic sling** or soft fabric hammock.
  - Contact patch width at each support: **<= 20 mm**
  - Total support contact area: **< 5%** of fruit surface
  - Support resonance target: **< 5 Hz**, well below the expected fruit resonances (`40-250 Hz`)
  - **Model mismatch:** the analytical model assumes a free shell; the sling introduces local compliance and damping. This is acceptable only if repositioning the sling changes the extracted resonance by **<= 3 Hz** on a 3-fruit check.
- **Sensor layout:**
  - Define axes:
    - `x`: major axis through stem and blossom ends
    - `z`: minor axis, vertical in the sling
  - Microphone:
    - Position: **100 +/- 10 mm** normal distance from rind
    - Azimuth: **45 deg** away from the impact point to reduce direct contact noise
  - Optional accelerometer:
    - Mass: **<= 1.5 g including cable**
    - Position: equatorial point opposite the impact meridian (`x = -a, z = 0`)
    - Attachment: museum wax or beeswax, not cyanoacrylate
  - Optional LDV:
    - Spot at same point as the accelerometer on **3-5 fruit only**
    - Use as a mass-loading cross-check, not as the main campaign sensor
- **Impact points:**
  - Three marks around the equator at longitudes **0 deg, 120 deg, 240 deg**
  - Each mark offset **15 deg above the equator** to avoid repeatedly hitting the same local zone
  - Record **3 taps per point**, so **9 accepted taps per fruit**
- **Calibration plan:**
  - Microphone:
    - Preferred: **94 dB / 1 kHz** acoustic calibrator before and after each session
    - Acceptable fallback: use the manufacturer calibration file and verify the channel is not clipping
  - Accelerometer:
    - Preferred: pocket vibration calibrator at **159.2 Hz, 1 g**
    - Fallback: attach to a small rigid beam and confirm the dominant frequency agrees with the microphone/LDV within **2 Hz**
  - Refractometer:
    - Zero with distilled water before each batch
  - Penetrometer:
    - Zero unloaded; verify with a known dead weight or spring check
  - Scale and callipers:
    - Zero before each fruit
- **Acquisition settings:**
  - Sample rate: **48 kHz** for microphone; if accelerometer DAQ is separate, use **>= 2 kHz**
  - Record length: **2.0 s** after each tap
  - Pre-trigger: **100 ms**
  - Bit depth: **24-bit** preferred, **16-bit** acceptable
  - Repeat count: **9 accepted taps per fruit**
  - Session repeatability: re-measure **3 fruit** after complete removal/re-suspension

## 6. Procedure
1. **Source fruit**
   - Obtain `N = 18-24` watermelons from a single grower or distributor.
   - Record cultivar, harvest class, date received, and any grower maturity note.
2. **Condition fruit**
   - Store at **20 +/- 1 C** for at least **12 h** before testing.
   - Do not refrigerate some fruit and not others.
3. **Assign IDs**
   - Label each fruit `WM01`, `WM02`, ... with marker tape.
4. **Measure gross geometry**
   - Measure mass.
   - Measure equatorial diameter at two orthogonal directions; average to get `2a`.
   - Measure pole-to-pole diameter to get `2c`.
   - Compute `a`, `c`, and `R_eq = (a^2 c)^(1/3)`.
5. **Prepare the support**
   - Mount the fruit in the elastic sling.
   - Check that the fruit is stable but visibly compliant, not clamped.
6. **Calibrate sensors**
   - Run microphone calibration.
   - Zero the refractometer and penetrometer.
   - If using an accelerometer, check its calibration or reference response.
7. **Place sensors**
   - Position the microphone **100 mm** from the surface at the prescribed azimuth.
   - If used, attach the accelerometer with wax at the opposite equatorial point.
8. **Set pendulum**
   - Pull the rubber striker to **20 deg** release angle.
   - Confirm that test taps do not clip the microphone channel.
9. **Acquire tap data**
   - At each of the 3 marked impact points, collect **3 good taps**.
   - Reject and repeat any tap with double impact, clipping, or visible fruit slip.
10. **Repeatability check**
    - For every fifth fruit, remove it from the sling, remount it, and repeat one 3-tap set.
11. **Optional cross-check**
    - On 3-5 fruit spanning the frequency range, repeat one tap set with LDV or accelerometer.
12. **Destructive testing**
    - Cut the fruit immediately after acoustic measurement.
    - Photograph the cut face.
13. **Rind thickness**
    - Measure rind thickness at **6 locations**:
      - 2 near stem end
      - 2 near blossom end
      - 2 equatorial
    - Record mean and SD.
14. **Brix**
    - Take juice from **3 locations**:
      - heart
      - mid-radius
      - near-rind red flesh
    - Record each reading and the mean `degBx`.
15. **Firmness**
    - Use the penetrometer at **3 locations** on red flesh after removing a small rind patch.
    - Record peak force in **N**.
16. **Visual maturity notes**
    - Record mealiness, internal cracking, voids, watery texture, and flesh colour.
17. **Clean and reset**
    - Clean sensor contact areas and support surfaces between fruit.

## 7. Analysis Plan
- **Primary observables:**
  - Dominant resonance frequency from microphone, `f_peak,mic`
  - Optional structural confirmation frequency from accelerometer/LDV, `f_peak,struct`
  - Damping estimate / quality factor from half-power bandwidth, where SNR permits
  - Destructive ground truth:
    - mean Brix
    - mean firmness
    - mean rind thickness
    - visual maturity features
- **Signal processing:**
  1. Band-pass filter each trace to **20-300 Hz** (4th-order zero-phase Butterworth).
  2. Detect impact time from the maximum absolute sample.
  3. Remove the first **8-10 ms** after impact to avoid contact transient and microphone overload.
  4. Use the following **250 ms** of ring-down for the spectral estimate.
  5. Apply a **Tukey window** (`alpha = 0.1`).
  6. FFT the windowed segment; zero-pad to give an interpolated bin spacing of **<= 0.25 Hz**.
  7. Pick the dominant peak between **30 and 250 Hz**.
  8. Refine the peak using **quadratic interpolation** on the log-magnitude spectrum.
  9. Average the 9 peak estimates per fruit; report mean and within-fruit SD.
- **Why this processing is acceptable despite short decay:**
  - The model predicts modest damping (`Q ~ 5-12`), so the resonance is broad.
  - The real requirement is **repeatable peak location**, not a razor-thin FFT line.
  - Quadratic peak interpolation and repeated impacts are more valuable here than extremely long records.
- **Ground-truth ripeness classification:**
  - Use destructive measures, not visual supermarket folklore.
  - Suggested operational rules:
    - **under-mature:** `Brix < 9.5 degBx` and `firmness > 20 N`
    - **market-ripe:** `10.0 <= Brix <= 12.0 degBx` and `10 <= firmness <= 20 N`
    - **over-mature:** `firmness < 10 N` and visual evidence of watery/mealy texture or internal voiding
  - If farm harvest labels exist, retain them as the nominal class and use Brix/firmness as verification.
- **Model comparison:**
  - For each fruit, compute the model prediction using measured `a`, `c`, and post-cut mean rind thickness `h`.
  - Compare measured `f_peak` with:
    1. the Paper 7 stage bands, and
    2. the geometry-normalised frequency
       `f_norm = f_peak (R_eq / R_ref)^(3/2)`,
       with `R_ref = 0.1453 m` for the canonical fruit.
  - Also compute the inverted rind modulus from measured frequency using `invert_frequency_to_modulus(...)` and test whether:
    - inferred modulus decreases with decreasing firmness, and
    - inferred modulus places fruit into sensible Paper 7 ripeness bands.
- **Statistics:**
  - Primary inferential test: one-way ANOVA or Kruskal-Wallis on `f_norm` across the 3 maturity classes.
  - Planned post-hoc comparisons: under-mature vs ripe, ripe vs over-mature.
  - Secondary analyses:
    - Pearson/Spearman correlation of `f_norm` with firmness
    - weaker, exploratory correlation of `f_norm` with Brix

## 8. Error Budget

| Source | Estimated effect | Mitigation |
|--------|------------------|------------|
| Peak-picking / spectral interpolation | +/- 0.3 Hz | 9 taps per fruit; quadratic spectral interpolation |
| Tap-to-tap repeatability | +/- 1.0 Hz | Fixed pendulum angle and striker mass |
| Support boundary-condition variation | +/- 1.5 Hz | Soft sling; re-suspension check on 3 fruit |
| Microphone placement variation | +/- 0.5 Hz | Fixed 100 mm standoff jig |
| Accelerometer mass loading (if used) | up to 1-2 Hz on smallest fruit | Keep sensor <= 1.5 g; confirm on subset with mic-only or LDV |
| Geometry measurement (`a`, `c`) | ~2-5% effect on predicted f | Measure diameters to <= 1 mm and use mean of repeats |
| Rind-thickness measurement | ~4-5% effect on predicted f | Measure 6 points after cutting and use mean |
| Fruit-to-fruit biological variability within class | 10-20 Hz | Single cultivar; same grower; class by destructive ground truth |
| Temperature variation | < 1 Hz if held within +/- 1 C | Equilibrate before measurement |
| Room noise / HVAC | false low-frequency peaks | Close microphone, quiet room, 20-300 Hz band-pass |

### Combined uncertainty estimate
- For extracted frequency alone, combining the first four instrumental terms in RSS:
  `u_f ~ sqrt(0.3^2 + 1.0^2 + 1.5^2 + 0.5^2) ~ 1.9 Hz`
- Expanded uncertainty:
  `U ~ 2 u_f ~ 3.8 Hz`
- This is the required order of precision: it is far smaller than the modelled under-mature-to-ripe shift (`~ 50-110 Hz`, depending on size and class spacing).

## 9. Acceptance Criteria
- **Supporting outcome:**
  - A reproducible dominant peak is measurable in at least **80%** of fruit.
  - Geometry-normalised resonance frequency decreases monotonically from under-mature to ripe to over-mature.
  - The class means differ by at least **20 Hz** between adjacent classes.
  - Median absolute measured-versus-model error is **<= 15%**.
  - Inferred modulus decreases with firmness and places most fruit in the expected Paper 7 ripeness band.
- **Refuting outcome:**
  - No reproducible resonance peak appears in the predicted **30-250 Hz** band.
  - Frequency shows no monotonic relation with destructive firmness class.
  - Measured frequencies are systematically inconsistent with geometry-corrected model predictions by **> 25%**.
- **Ambiguous outcome:**
  - Peaks are measurable, but support-condition shifts or mixed-cultivar sourcing dominate the variance.
  - Frequency correlates weakly with Brix but not with firmness, implying the test is measuring edible sweetness rather than the shell stiffness the model claims to predict.
  - A microphone peak exists, but accelerometer/LDV on the subset fails to confirm a structural resonance at the same frequency.

## 10. Risks and Next Steps
- **Main practical risks:**
  - Sourcing true maturity bands from one cultivar is harder than buying supermarket fruit.
  - Watermelon is non-climacteric, so storage time after purchase is not a valid maturity-control variable.
  - Support stiffness can masquerade as a boundary-condition effect.
  - A heavy accelerometer can perturb the very mode being measured.
- **Ethical or safety issues:**
  - No ethics approval required.
  - Standard knife safety, slip prevention, and food-waste disposal only.
  - If using an LDV, follow laser eye-safety rules.
- **Recommended follow-on experiment:**
  - Add a **direct rind-modulus measurement** on post-cut rind coupons using a small compression or 3-point-bend rig.
  - Then compare:
    1. measured resonance frequency,
    2. inverted modulus from the shell model, and
    3. coupon-derived modulus.
  - That is the next step if the minimum tap test supports the Paper 7 trend.

## Practical notes for the postdoc running this

### Recommended measurement hierarchy
1. **Start with microphone only** on all fruit.
2. If available, add **accelerometer or LDV** on a small subset to prove the peak is structural.
3. Do **not** let the perfect instrument stop the cheap experiment this month.

### Data to record for every fruit
- ID
- cultivar
- source / grower / harvest class
- date and room temperature
- mass
- `2a`, `2c`, `a`, `c`, `R_eq`
- microphone peak frequency for each of 9 taps
- optional accelerometer/LDV peak frequency
- within-fruit SD of peak frequency
- estimated `Q` if measurable
- rind thickness at 6 locations
- mean Brix and individual Brix readings
- mean firmness and individual firmness readings
- notes on hollowness, mealiness, cracking, or voids

### Simple pass/fail summary
- If you can show **one clean figure** of measured `f_peak` dropping across destructive maturity class, and a second figure of measured-versus-predicted frequency with most points inside **+/- 15%**, Reviewer B loses the main objection.
