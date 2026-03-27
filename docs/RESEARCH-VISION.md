# Browntone Research Programme — Vision & Roadmap

*Last updated: 2026-03-27*

## Programme Overview

This research programme investigates the biomechanics of infrasound-abdomen interaction,
using the "brown note" hypothesis as a motivating lens. The core contribution is a
rigorous analytical framework for fluid-filled viscoelastic shell vibration with
applications beyond the original question.

## Publication Pipeline

### Paper 1 (Primary): Modal Analysis of the Abdomen — JSV
**Status**: Draft at 31 pages, under internal review (Round 4).
**Core result**: 10⁴× coupling disparity between mechanical and airborne pathways.
**Timeline**: 1-2 more review-revise cycles to submission-ready.

### Paper 2 (Spin-off): Gas Pocket Transduction Mechanism — JASA
**Status**: Analysis complete. Needs its own paper draft.
**Core result**: Bowel gas pockets act as impedance-matching transducers, creating
a 9 dB susceptibility range across the population. Explains differential vulnerability.
**Novel**: First quantitative model of constrained gas bubble mechanotransduction in GI tract.

### Paper 3 (Short Communication): Dimensional Analysis & Scaling — JSV or IJMS
**Status**: Agent running.
**Core result**: Universal dimensionless curves collapsing all parameters. Cross-species
scaling predictions.
**Novel**: Enables comparison across animal models without full re-analysis.

### Paper 4 (Future): Coupled Thoraco-Abdominal Oscillator
**Idea**: Model the diaphragm as a coupling membrane between chest and abdominal cavities.
Predict phase relationships and energy transfer between compartments.
**Why it matters**: Extends to blast injury modelling and ventilator-induced lung injury.

### Paper 5 (Future): Acoustic Metamaterial Analogy
**Idea**: Periodic rib structure as a phononic crystal. Predict stop bands for body-wall
wave propagation. Could explain frequency-selective transmission.
**Why it matters**: Connects to metamaterial community; high citation potential.

## Research Questions (Open)

1. **Why does the linear model overpredict WBV displacement by 3.75×?** (M2 issue)
   - Hypotheses: modal participation factor < 1, nonlinear saturation, boundary effects
   - The nonlinear analysis shows 27% reduction — accounts for ~1/3 of the gap
   - Remaining 2.7× could be modal participation + BC effects combined

2. **Can gas pockets explain the anecdotal brown note reports?**
   - Our model says: at 120 dB with large gas pockets (100 mL), displacement exceeds
     PIEZO threshold. This is the only pathway where airborne infrasound could plausibly
     cause GI effects.
   - Needs experimental validation (phantom with air inclusions)

3. **Is abdominal wall stiffness measurable via vibration response?**
   - Clinical application: non-invasive elastography via resonance tracking
   - f₂ is a strong function of E (S_T = 0.86) — could be a diagnostic biomarker
   - Prior art: liver elastography, but not whole-abdomen

4. **Does the coupling disparity hold for transient loading (blast)?**
   - Steady-state analysis may not apply to millisecond-scale blast waves
   - Blast wavelengths are much shorter → ka could be >> 1 → geometric filtering vanishes
   - This would be a different paper with significant defence applications

## Ideas Backlog (Prioritised)

### High Priority (would strengthen Paper 1)
- [ ] Broader applications paragraph (blast, ultrasound, marine bio)
- [ ] Missing references: Junger & Feit, Leissa, Soedel, etc.
- [ ] Resolve M2 gap with modal participation factor analysis
- [ ] Experimental validation protocol (phantom)

### Medium Priority (spin-off papers or future work)
- [ ] Gas pocket paper draft (Paper 2)
- [ ] Coupled thoraco-abdominal model prototype
- [ ] Clinical elastography application note
- [ ] Cross-species scaling validation against veterinary WBV data

### Low Priority (interesting but speculative)
- [ ] Peristalsis interaction (time-varying stiffness → parametric amplification)
- [ ] Acoustic metamaterial rib model
- [ ] Historical/cultural paper for popular science venue
- [ ] Comparison with Gavreau's original apparatus parameters

## Key Principles

1. **Rigour over novelty**: We'd rather be correct and boring than wrong and exciting
2. **Honest uncertainty**: Every claim gets error bars. Partial UQ is worse than none.
3. **Reproducibility**: All results must be regenerable from source code + canonical params
4. **The brown note is the hook, not the point**: The real contribution is the analytical
   framework and the coupling disparity result
5. **Humour is a feature**: Subtle, dry, and never at the expense of scientific credibility
