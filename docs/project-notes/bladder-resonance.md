# Bladder Resonance: Fluid-Filled Viscoelastic Shell Model

Spin-off from the [browntone](../../README.md) project (synergy score 5/5).

## Research Question

Occupational health studies report increased urinary urgency among vehicle
operators exposed to whole-body vibration (WBV). ISO 2631 documents pelvic
resonance at 4–8 Hz. Can we predict the bladder's resonant frequency and
vibration coupling using the same fluid-filled shell framework?

## Approach

The urinary bladder is literally a fluid-filled viscoelastic shell: the
detrusor muscle wall encloses urine in a near-spherical geometry that
changes with fill state. We reuse `AbdominalModelV2` from
`src/analytical/natural_frequency_v2.py` with bladder-specific parameters.

### Parameter Mapping (Fill-State Dependent)

| Parameter | 50 mL (empty) | 300 mL (urge) | 500 mL (full) | Source |
|-----------|---------------|----------------|----------------|--------|
| Radius | 2.3 cm | 4.2 cm | 4.9 cm | Geometry |
| Wall thickness | 5.0 mm | 1.8 mm | 1.5 mm | Const. tissue vol. |
| E (Young's mod) | 29 kPa | 71 kPa | 145 kPa | Vibrometry (E≈3μ) |
| Intravesical P | 5 cmH₂O | 12.7 cmH₂O | 30 cmH₂O | Cystometry |
| ρ_fluid (urine) | 1020 kg/m³ | 1020 kg/m³ | 1020 kg/m³ | ≈ water |

## Key Results

### Modal Frequencies

The n=2 (oblate–prolate) flexural mode frequency varies with fill volume:

| Fill Volume | f₂ (Hz) | f₃ (Hz) |
|-------------|---------|---------|
| 50 mL†  | 22.7 | 36.3 |
| 150 mL | 14.2 | 22.8 |
| 300 mL | 13.9 | 24.1 |
| 500 mL | 17.1 | 30.6 |

† h/R > 0.1; thin-shell approximation violated — treat with caution.

The **minimum f₂ = 13.5 Hz** occurs at 222 mL due to competing effects:
- Larger radius → lower frequency (geometry)
- Stiffer wall at higher fill → higher frequency (strain-stiffening)

### Coupling Analysis (at 300 mL)

| Pathway | Coupling | Mechanism |
|---------|----------|-----------|
| Airborne acoustic | (ka)² ≈ 1.1 × 10⁻⁴ | Pressure gradient across body |
| Mechanical (WBV) | ~0.7 | Seat → pelvis → bladder wall |
| **Mechanical advantage** | **~6,400×** | |

Whole-body vibration bypasses the (ka)^n acoustic penalty entirely.

### Interpretation

- The bladder n=2 mode (13.5–17.1 Hz) sits **above** the ISO 2631 peak pelvic
  resonance (4–8 Hz) but within the broader WBV-affected frequency range.
- At sub-resonant frequencies (4–8 Hz), the bladder still responds as a
  forced oscillator while pelvic transmissibility amplifies the input.
- Mechanical coupling is ~10⁴× more effective than airborne sound — the
  dominant pathway is seat vibration through the pelvic skeleton.
- This is consistent with occupational reports that prolonged WBV exposure
  (truck drivers, forklift operators) increases urinary urgency.

## Figures

- [`fig_bladder_frequency_vs_volume.png`](figures/fig_bladder_frequency_vs_volume.png) —
  Parametric study of f₂ and f₃ vs fill state, with geometry and material evolution.
- [`fig_bladder_coupling.png`](figures/fig_bladder_coupling.png) —
  Airborne vs mechanical coupling pathways.

## Files

- `bladder_model.py` — Model, parametric study, and figure generation
- `literature-notes.md` — References and literature review
- `figures/` — Generated plots

## Limitations & Next Steps

1. **Spherical approximation** — the real bladder is slightly oblate and
   irregularly shaped.
2. **Pelvic constraint** — ~40% of the bladder surface contacts the pelvic
   bone; by Rayleigh's theorem, a partial rigid boundary would raise the
   effective resonant frequencies (the free-shell model is a lower bound).
3. **Nonlinear elasticity** — the exponential strain-stiffening model is
   simplified; a hyperelastic (Mooney–Rivlin or Ogden) model would be more
   accurate.
4. **Nerve activation threshold** — urgency requires stretch receptor
   activation, not just wall displacement; coupling the mechanical model to
   afferent nerve thresholds is the key clinical prediction.
5. **FEA validation** — use the browntone FEA pipeline with bladder geometry
   and pelvic boundary conditions.
