# Notebooks

Jupyter notebooks for interactive exploration and prototyping.

## Notebooks

- `01_analytical_solutions.ipynb` — Explore analytical shell and cavity mode solutions

## Usage

```bash
pip install -e ".[notebooks]"
jupyter lab notebooks/
```

## Guidelines

- Notebooks are for **exploration only** — production code goes in `src/browntone/`
- Clear all outputs before committing (or use `nbstripout`)
- Number notebooks to suggest reading order
- Keep notebooks self-contained with markdown explanations
