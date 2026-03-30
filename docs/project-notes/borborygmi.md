# What Pitch Is a Growling Stomach?

**Modelling borborygmi as coupled Helmholtz-bubble oscillators**

*Project lead*: Opus (Copilot CLI)
*Faculty supervisor*: Jonathan Mace
*Target venue*: Journal of the Acoustical Society of America (JASA)
*Status*: Preliminary framework -- exploratory

---

## Research Question

Borborygmi -- the characteristic gurgling and rumbling sounds of the
gastrointestinal tract -- are universally familiar yet poorly characterised
from a physical acoustics perspective.  Clinical studies report bowel sound
frequencies in the range 200-550 Hz for healthy adults, with spectral shifts
during intestinal obstruction.  **Can we predict the pitch of a growling
stomach from first principles?**

We model gas pockets trapped in the fluid-filled, elastic intestinal lumen
as constrained Minnaert bubbles and Helmholtz resonators, and compare model
predictions against published clinical frequency data.

## Approach

### 1. Minnaert Bubble (Baseline)

A spherical gas pocket of equivalent radius *R* in an incompressible fluid
oscillates at the Minnaert frequency:

```
f_M = (1 / 2piR) sqrt(3 gamma P0 / rho_f)
```

For a 10 mL pocket (*R* = 13.4 mm) this gives **f_M = 244 Hz**.

### 2. Constrained Bubble (Primary Model)

The intestinal wall wraps the pocket, contributing elastic stiffness
*and* inertia.  The corrected frequency is:

```
omega^2 = (k_gas + k_wall) / (m_fluid + m_wall)

k_gas  = 3 gamma P0 / R           (gas compressibility restoring force)
k_wall = 2Eh / [R^2 (1-nu)]       (elastic wall stiffness per unit displacement)
m_fluid = rho_f R                  (radiation added mass)
m_wall  = rho_w h                  (wall inertia)
```

With the soft intestinal wall (E = 10 kPa, h = 3 mm), wall mass dominates
over wall stiffness, reducing the frequency to **f = 223 Hz** for 10 mL --
a physically intuitive result (the gut wall is heavy and floppy).

### 3. Helmholtz Resonator

Peristaltic constrictions create a "neck" connecting the pocket to the lumen:

```
f_H = (c_gas / 2pi) sqrt(A_neck / L_eff V)
```

This gives **f_H = 647 Hz** for a 5 mm neck -- placing it in the upper range
of clinically observed bowel sounds and modelling "tinkling" high-pitched
sounds associated with obstruction.

### 4. Cylindrical Slug Modes

A gas slug filling the lumen behaves differently:
- **Axial piston mode**: slug oscillates between fluid plugs -> **f = 99 Hz**
  (sub-audible rumbling)
- **Radial breathing mode**: tube-constrained expansion -> **f = 1329 Hz**
  (above clinical range)

## Parameters

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Gas adiabatic exponent | gamma | 1.4 | -- | Air |
| Ambient pressure | P0 | 102,325 | Pa | P_atm + P_iap |
| Fluid density | rho_f | 1,020 | kg/m^3 | Intestinal fluid |
| Wall Young's modulus | E_w | 10 | kPa | Intestinal tissue |
| Wall Poisson's ratio | nu_w | 0.45 | -- | Soft tissue |
| Wall thickness | h_w | 3 | mm | Intestinal wall |
| Wall density | rho_w | 1,040 | kg/m^3 | Tissue |
| Lumen diameter | d | 2-5 | cm | Small/large bowel |
| Gas volume | V | 1-50 | mL | Typical range |
| Gas sound speed | c_gas | 343 | m/s | Air at 37 deg C |

## Preliminary Results

### Frequency vs Volume (Constrained Bubble)

| Volume (mL) | Frequency (Hz) | Clinical Comparison |
|-------------|----------------|---------------------|
| 1 | 440 | Near LBO peak (440 Hz) |
| 5 | 275 | Near SBO peak (288 Hz) |
| 10 | 223 | Within healthy range |
| 20 | 180 | Below healthy range |
| 50 | 135 | Sub-audible rumbling |

**Key finding**: The constrained bubble model spans 135-440 Hz for
1-50 mL gas pockets, overlapping substantially with the clinical
borborygmi range of 200-550 Hz.  Smaller pockets (1-5 mL) match
the higher-pitched sounds of obstruction; larger pockets produce
the low-frequency rumbling of normal peristalsis.

### Clinical Reference Data

| Condition | Range (Hz) | Peak (Hz) | Source |
|-----------|-----------|-----------|--------|
| Healthy adult | 200-550 | 340 | Ching & Tan (2012) |
| Small bowel obstruction | 173-667 | 288 | Yoshino et al. (1990) |
| Large bowel obstruction | 309-878 | 440 | Du Plessis et al. (2000) |

### Figure

![Borborygmi frequency vs volume](figures/fig_borborygmi_frequency_vs_volume.png)

*Four-panel figure showing: (a) all resonance modes vs volume, (b) constrained
bubble sensitivity to tube diameter, (c) Helmholtz sensitivity to neck diameter,
(d) comparison with clinical frequency bands.*

## Physics Insights

1. **Wall mass matters more than wall stiffness** for the soft intestinal wall.
   At E = 10 kPa, the constrained frequency is *lower* than the free Minnaert
   frequency -- the wall adds inertia without proportionate stiffness.

2. **Volume is the primary determinant of pitch**.  The 1/R dependence of Minnaert
   means small (1-5 mL) pockets produce audible 275-440 Hz sounds, while large
   (>20 mL) pockets produce infrasonic rumbling (<180 Hz).

3. **Multiple mechanisms coexist**.  Real borborygmi likely involve a superposition
   of constrained bubble modes (radial pulsation), Helmholtz modes (flow through
   constrictions), and axial slug modes (piston-like oscillation).

4. **Peristaltic dynamics are the excitation**.  The model predicts resonant
   frequencies; actual borborygmi are excited by peristaltic waves compressing
   and releasing gas pockets -- a transient broadband excitation.

## Connection to Browntone Programme

This project extends the lab's gas-pocket analysis (Paper 2: `papers/paper2-gas-pockets/`)
from infrasound (brown note context) to audible acoustics (clinical borborygmi).
The analytical framework reuses the same Minnaert and constrained-bubble physics
but targets a different frequency regime and application.

## Files

```
papers/paper5-borborygmi/
    figures/
        fig_borborygmi_frequency_vs_volume.png
        fig_borborygmi_frequency_vs_volume.pdf

src/analytical/
    borborygmi_model.py           <- Core model code

tests/
    test_borborygmi.py            <- 35 tests
```

## Limitations & Next Steps

### Limitations
- Spherical approximation for non-spherical gas pockets
- Static geometry (no peristaltic dynamics)
- Single-pocket model (no inter-pocket coupling)
- No viscous/thermal damping of bubble oscillation
- No tissue transmission loss to skin surface

### Next Steps (if pursued)
1. **Coupled multi-pocket model**: array of bubbles with mutual radiation coupling
2. **Peristaltic excitation**: time-varying tube geometry driving transient response
3. **Tissue transmission**: attenuation from gas pocket -> abdominal surface
4. **Experimental validation**: record borborygmi with contact microphone + ultrasound
   for gas-pocket volume estimation
5. **Clinical correlation**: compare predicted frequency shifts with obstruction data

## Publication Plan

- **Venue**: JASA (Journal of the Acoustical Society of America)
- **Format**: Letter or Express article (~4 pages)
- **Title**: "What pitch is a growling stomach? Predicting borborygmi frequencies
  from gas-pocket resonance"
- **Angle**: Accessible yet rigorous -- the topic has inherent public appeal and
  the physics is clean (Minnaert + elastic constraint)
- **Timeline**: Exploratory phase; park until Paper 1 (brown note) is submitted

## References

1. Minnaert M (1933). On musical air-bubbles and the sounds of running water.
   *Phil Mag* 16:235-248.
2. Cannon WB (1905). Auscultation of the rhythmic sounds produced by the stomach
   and intestines. *Am J Physiol* 12:387-395.
3. Ching SS, Tan YK (2012). Spectral analysis of bowel sounds in intestinal
   obstruction using an electronic stethoscope. *World J Gastroenterol* 18:4585.
4. Yoshino H et al. (1990). Clinical application of spectral analysis of bowel
   sounds in intestinal obstruction. *Dis Colon Rectum* 33:753.
5. Du Plessis J et al. (2000). Spectral analysis of bowel sounds.
   *Dis Colon Rectum* 43:81.
6. Leighton TG (1994). *The Acoustic Bubble*. Academic Press.
