# Material Properties

This directory contains material property definitions for the browntone simulations.

## Files

- `default.json` — Reference material properties and geometry for the baseline simulation

## Property Sources

| Property | Range | Source |
|----------|-------|--------|
| Abdominal wall E | 20–100 kPa | Fung (1993), Song et al. (2006) |
| Abdominal wall ν | 0.45–0.49 | Nearly incompressible soft tissue |
| Abdominal wall ρ | 1000–1100 kg/m³ | Approximate tissue density |
| Cavity fluid c | ~1500 m/s | Speed of sound in water/tissue |
| Cavity fluid ρ | ~1000 kg/m³ | Approximate fluid density |

## Adding New Materials

Create a JSON file following the schema in `default.json`. Materials can be loaded
programmatically:

```python
from browntone.utils.materials import load_material_from_json
mat = load_material_from_json("data/materials/custom.json")
```
