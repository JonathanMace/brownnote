# Paper 8 sigma-min expansion fit

- Generated `papers/paper8-kac/figures/fig_expansion_fit.pdf` and `fig_expansion_fit.png` from a new script, `scripts/generate_p8_expansion_figure.py`.
- The figure overlays Ritz-model `\sigma_{\min}(\varepsilon)` data with the quartic expansion
  `\sigma_{\min} = \sigma_0 + \lambda_1 \varepsilon^2 + \lambda_2 \varepsilon^4`
  using `\sigma_0 = 0.01113`, `\lambda_1 = 0.00507`, and `\lambda_2 = 0.02401`.
- Numerical verification from `sigma_min_expansion()` returned
  `\sigma_0 = 0.01112987`, `\lambda_1 = 0.00507161`, and `\lambda_2 = 0.02401141`,
  i.e. relative differences of `0.0012%`, `0.0317%`, and `0.0059%` from the rounded paper values.
- Output assets:
  - `fig_expansion_fit.pdf`: `26,095` bytes
  - `fig_expansion_fit.png`: `91,846` bytes
  - PNG raster size: `977 × 724` px at `300` dpi
- Recompiled `papers/paper8-kac/main.tex`, updated `papers/paper8-kac/main.pdf`, created snapshot
  `papers/paper8-kac/drafts/draft_2026-03-30_0045.pdf`, and updated the root `README.md` draft link.
- Validation:
  - `python scripts/generate_p8_expansion_figure.py` completed successfully.
  - Focused Paper 8 consistency audit passed.
  - Baseline `python -m pytest tests/ -q` completed successfully before final git packaging.
