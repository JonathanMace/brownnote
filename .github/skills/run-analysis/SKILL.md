---
name: run-analysis
description: >
  Run the full analytical computation pipeline: modal frequencies, parametric
  sweeps, mechanotransduction analysis, and figure generation. Use when you
  need to regenerate results after code changes.
---

# Run Analysis Skill

Execute the full browntone analytical computation pipeline.

## Steps

1. **Run modal frequency computation**
   ```bash
   cd C:\Users\jon\OneDrive\Projects\browntone
   python src/analytical/natural_frequency.py
   ```
   Verify: output should show modal frequencies for modes n=0..10
   Check: at least one mode in or near 5-10 Hz range for soft tissue models

2. **Run mechanotransduction pathway analysis**
   ```bash
   python src/analytical/mechanotransduction.py
   ```
   Verify: PIEZO activation thresholds computed for multiple body types
   Check: SPL thresholds should be in 100-150 dB range

3. **Generate publication figures**
   ```bash
   python src/postprocess/generate_figures.py
   ```
   Verify: 4+ figures saved to `data/figures/`
   Check: figures render correctly, legends readable

4. **Run tests** (if available)
   ```bash
   python -m pytest tests/ -v
   ```

5. **Log results**
   Create a timestamped entry in `docs/research-logs/` documenting:
   - What was run
   - Key numerical results
   - Any errors or warnings
   - Whether results changed from previous run

## Expected Outputs

| File | Description |
|------|-------------|
| `data/figures/fig1_parametric_frequencies.png` | Parameter sensitivity |
| `data/figures/fig2_piezo_threshold_map.png` | SPL×frequency heatmap |
| `data/figures/fig3_spl_by_body_type.png` | Body type comparison |
| `data/figures/fig4_modal_spectrum.png` | Modal spectrum |
| stdout | Numerical results tables |
