# Methodology

## Research Question

Can infrasound at specific frequencies excite resonant modes in the human
abdominal cavity, and if so, what displacement amplitudes would result from
physiologically plausible sound pressure levels?

## Approach

### 1. Analytical Estimates

- Model the abdomen as a fluid-filled elastic shell (cylindrical or ellipsoidal)
- Compute natural frequencies using Donnell shell theory and Helmholtz cavity modes
- Estimate coupled (FSI) frequencies using Junger & Feit formulations
- Establish expected frequency ranges to guide FEA

### 2. Finite Element Analysis

- **Geometry**: Simplified ellipsoidal cavity with uniform wall thickness
- **Mesh**: gmsh with controlled element size; convergence study performed
- **Structural model**: Linear elastic, isotropic abdominal wall (parametric E, ν, ρ)
- **Fluid model**: Acoustic Helmholtz equation in the cavity interior
- **Coupling**: Fluid–structure interface with continuity of normal velocity and pressure
- **Solver**: FEniCSx with SLEPc eigenvalue solver
- **Analyses**:
  - Structural modal analysis (dry modes)
  - Acoustic cavity modal analysis (rigid-wall modes)
  - Coupled FSI modal analysis
  - Harmonic response under infrasound pressure loading

### 3. Parametric Study

Sweep over:
- Material stiffness: E = 20, 50, 100 kPa
- Wall thickness: h = 10, 15, 20 mm
- Cavity geometry: vary semi-axes
- Damping ratio: ζ = 0.01 to 0.10

### 4. Validation

- Compare structural modes against Leissa shell solutions
- Compare acoustic modes against Bessel function solutions
- Compare coupled modes against Junger & Feit
- Mesh convergence study with Richardson extrapolation
- Energy balance verification

## Assumptions and Limitations

- Small-strain, linear elastic material behaviour
- Isotropic, homogeneous material properties
- Simplified geometry (no internal organs modelled explicitly)
- No air–tissue interface (external sound transmission not modelled)
- Steady-state response (no transient effects)
