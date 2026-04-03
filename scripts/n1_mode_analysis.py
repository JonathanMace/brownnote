#!/usr/bin/env python3
"""
n=1 mode analysis for a partially constrained abdominal shell.

An external reviewer noted that n=1 is only a rigid-body translation for a
FREE shell.  With pelvic constraint (the lower hemisphere is attached to the
spine/pelvis), n=1 becomes a genuine "belly bounce" mode with nonzero
frequency.  This script quantifies that frequency via three independent
estimates and documents why n>=2 deformation modes remain physiologically
more relevant for the "brown note" hypothesis.

Methods
-------
1. Sphere formula from natural_frequency_v2 applied to n=1 (membrane + prestress
   terms only — bending vanishes for n=1).
2. Rayleigh estimate for a partially constrained shell (free above theta_c,
   clamped below).
3. Full 2-DOF Ritz eigenvalue from oblate_spheroid_ritz with the n<2 guard
   removed.

All computations use canonical parameters (R3).
"""

import sys
import os
import numpy as np

# Ensure repo root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)
from src.analytical.oblate_spheroid_ritz import _build_KM

from numpy.polynomial.legendre import leggauss

# ============================================================
# Canonical parameters (R3)
# ============================================================
a     = 0.18       # semi-major axis [m]
c     = 0.12       # semi-minor axis [m]
h     = 0.010      # wall thickness [m]
E     = 0.1e6      # Young's modulus [Pa]  (0.1 MPa)
nu    = 0.45       # Poisson's ratio
rho_w = 1100.0     # wall density [kg/m³]
rho_f = 1020.0     # fluid density [kg/m³]
K_f   = 2.2e9      # fluid bulk modulus [Pa]
P_iap = 1000.0     # intra-abdominal pressure [Pa]
eta   = 0.25       # loss tangent

R_eq  = (a * a * c) ** (1.0 / 3.0)   # equivalent sphere radius
D     = E * h**3 / (12 * (1 - nu**2))

model = AbdominalModelV2(
    a=a, b=a, c=c, h=h, E=E, nu=nu, rho_wall=rho_w,
    rho_fluid=rho_f, K_fluid=K_f, P_iap=P_iap, loss_tangent=eta,
)

# ============================================================
# 0. Reference: n=2 from v2 (should be ~3.95 Hz)
# ============================================================
freqs_v2 = flexural_mode_frequencies_v2(model, n_max=5)
f2_ref = freqs_v2[2]

# ============================================================
# 1. Sphere formula applied to n=1 (unconstrained formula)
# ============================================================
n = 1
R = R_eq

# Bending: n(n-1)(n+2)^2 D/R^4  => 1*0*9*D/R^4 = 0
K_bend_n1 = n * (n - 1) * (n + 2)**2 * D / R**4

# Membrane (Lamb): lambda_n = (n^2+n-2+2*nu) / (n^2+n+1-nu)
#   n=1: (1+1-2+2*0.45)/(1+1+1-0.45) = 0.90/2.55
lambda_n1 = (n**2 + n - 2 + 2*nu) / (n**2 + n + 1 - nu)
K_memb_n1 = E * h / R**2 * lambda_n1

# Prestress: P/R * (n-1)(n+2) => P/R * 0 * 3 = 0
K_prestress_n1 = P_iap / R * (n - 1) * (n + 2)

K_total_n1 = K_bend_n1 + K_memb_n1 + K_prestress_n1

# Effective mass: rho_w*h + rho_f*R/n
m_eff_n1 = rho_w * h + rho_f * R / n

omega_sq_n1 = K_total_n1 / m_eff_n1
f_n1_formula = np.sqrt(max(0, omega_sq_n1)) / (2 * np.pi)

# ============================================================
# 2. Full Ritz eigenvalue for n=1 (bypass the n<2 guard)
# ============================================================
n_quad = 200
eta_q, w_q = leggauss(n_quad)
K_mat, M_mat = _build_KM(1, a, c, h, E, nu, P_iap, rho_w, rho_f, eta_q, w_q)

try:
    L = np.linalg.cholesky(M_mat)
    Kinv = np.linalg.solve(L, np.linalg.solve(L, K_mat).T)
    eigvals_ritz = np.linalg.eigvalsh(Kinv)
except np.linalg.LinAlgError:
    eigvals_ritz = np.real(np.linalg.eigvals(np.linalg.solve(M_mat, K_mat)))

f_n1_ritz = np.sqrt(max(eigvals_ritz.min(), 0.0)) / (2 * np.pi)
f_n1_ritz_max = np.sqrt(max(eigvals_ritz.max(), 0.0)) / (2 * np.pi)

# ============================================================
# 3. Rayleigh estimate for partially constrained shell
#    (clamped below theta_c, free above)
# ============================================================
theta_c = 2 * np.pi / 3   # constraint boundary (120°)

# Trial function: w(theta) = cos(theta) for 0 <= theta <= theta_c
#                 w(theta) = 0           for theta > theta_c
# On a sphere of radius R, ds = R^2 sin(theta) d(theta) d(phi)

N_int = 2000
theta = np.linspace(0, np.pi, N_int + 1)
dtheta = theta[1] - theta[0]

# Free region: theta < theta_c
free = theta <= theta_c

# Trial displacement (normal to surface, approximating n=1 translation)
w_trial = np.where(free, np.cos(theta), 0.0)

# ---- Kinetic energy (T_max = 0.5 * omega^2 * T_ref) ----
# Shell mass
T_shell = 0.0
for i in range(N_int):
    th = 0.5 * (theta[i] + theta[i + 1])
    wt = 0.5 * (np.cos(theta[i]) + np.cos(theta[i + 1]))
    if th <= theta_c:
        wt_val = np.cos(th)
    else:
        wt_val = 0.0
    T_shell += rho_w * h * wt_val**2 * 2 * np.pi * R**2 * np.sin(th) * dtheta

# Fluid added mass (entrained fluid of the free cap)
# For a rigid cap translating, the added mass is approximately the
# mass of fluid in a hemisphere of the free portion.
# More precisely, for a spherical cap subtending angle theta_c:
#   V_cap = (2/3) pi R^3 (1 - cos(theta_c))
# The added mass coefficient for a translating body ~ 0.5 * rho_f * V_cap
# (hemisphere analogy).  For a more careful estimate:
#   T_fluid = integral of rho_f * R / 1 * |w|^2 dS  (using n=1 added-mass
#   formula over the free portion only)
T_fluid = 0.0
for i in range(N_int):
    th = 0.5 * (theta[i] + theta[i + 1])
    if th <= theta_c:
        wt_val = np.cos(th)
    else:
        wt_val = 0.0
    # Added mass per unit area ~ rho_f * R / n with n=1
    T_fluid += rho_f * R * wt_val**2 * 2 * np.pi * R**2 * np.sin(th) * dtheta

T_ref = T_shell + T_fluid

# ---- Potential energy (V_max) ----
# Two contributions at the constraint boundary:
#
# (a) Membrane stretching at the boundary: the trial function has a
#     discontinuity in slope at theta_c.  The meridional strain from the
#     abrupt stop creates a concentrated membrane force.
#     V_memb ~ (E*h / R^2) * lambda_1 * integral |w|^2 dS  (over free part)
#     (same as the sphere formula but integrated only over the free cap).
#
# (b) IAP prestress:  For a constrained shell the prestress contribution
#     comes from the meridional membrane force N_theta ~ P*R/2 acting on the
#     slope discontinuity.  The work done is:
#     V_prestress = N_theta * 2*pi*R*sin(theta_c) * (dw/dtheta)^2 * R * dtheta_eff
#
# For a simple Rayleigh upper bound we use the membrane stiffness integrated
# over the free cap, which gives the dominant restoring mechanism:

# Membrane stiffness integrated over free cap
V_memb = 0.0
for i in range(N_int):
    th = 0.5 * (theta[i] + theta[i + 1])
    if th <= theta_c:
        wt_val = np.cos(th)
    else:
        wt_val = 0.0
    V_memb += (E * h / R**2) * lambda_n1 * wt_val**2 * 2 * np.pi * R**2 * np.sin(th) * dtheta

# Prestress: concentrated at boundary ring
# N_theta = P * R / 2 (membrane stress in pressurised sphere)
# The slope jump at theta_c:  dw/dtheta |_{theta_c^-} = -sin(theta_c)
# Strain energy ~ N_theta * (dw/ds)^2 * delta_s
# where ds = R * sin(theta_c) * 2*pi is the ring circumference
# This is a small correction; compute it but expect it to be minor.
N_theta = P_iap * R / 2
dw_ds = np.sin(theta_c) / R   # slope of cos(theta) at theta_c, per unit arc
ring_circ = 2 * np.pi * R * np.sin(theta_c)
# Effective width of the boundary layer ~ h (wall thickness)
V_prestress_boundary = N_theta * dw_ds**2 * R * ring_circ * h

V_total = V_memb + V_prestress_boundary

omega_sq_rayleigh = V_total / T_ref
f_n1_rayleigh = np.sqrt(max(0, omega_sq_rayleigh)) / (2 * np.pi)

# ============================================================
# 4. Constraint stiffness approach (spring-mass analogy)
# ============================================================
# The constrained shell is like a mass-spring system where:
#   m = mass of free portion (shell + entrained fluid)
#   k = membrane stiffness + IAP stiffness at constraint ring
#
# Mass of free cap (shell):
m_cap_shell = rho_w * h * 2 * np.pi * R**2 * (1 - np.cos(theta_c))
# Mass of entrained fluid (volume of cap):
V_cap = (2.0 / 3.0) * np.pi * R**3 * (1 - np.cos(theta_c))
m_cap_fluid_entrained = rho_f * V_cap
# Added mass coefficient for oscillating cap ~ 0.5 (hemisphere approximation)
m_added = 0.5 * rho_f * V_cap
m_total_cap = m_cap_shell + m_added

# Stiffness from membrane stretching at constraint boundary:
# Ring of circumference 2*pi*R*sin(theta_c), membrane force E*h*strain
# For unit displacement d, strain ~ d/R, force ~ E*h/R * d * ring_circumference / R
# But we need per-unit-displacement stiffness:
k_memb_ring = E * h / R * ring_circ * np.sin(theta_c) / R
# This accounts for the meridional membrane force resisting the displacement.

# Prestress stiffness: N_theta at the boundary resists the angular displacement
# For displacement d at the top, the angle change at the boundary ring is d/R
# Restoring force ~ N_theta * (d/R) * ring_circumference
k_prestress_ring = N_theta / R * ring_circ

k_total_ring = k_memb_ring + k_prestress_ring
f_n1_spring = np.sqrt(k_total_ring / m_total_cap) / (2 * np.pi)

# ============================================================
# Print results
# ============================================================
print("=" * 72)
print("  n=1 MODE ANALYSIS: Partially Constrained Abdominal Shell")
print("=" * 72)

print("\n--- Canonical Parameters (R3) ---")
print(f"  Semi-major axis  a     = {a} m")
print(f"  Semi-minor axis  c     = {c} m")
print(f"  Wall thickness   h     = {h} m")
print(f"  Young's modulus  E     = {E/1e6} MPa")
print(f"  Poisson's ratio  ν     = {nu}")
print(f"  Wall density     ρ_w   = {rho_w} kg/m³")
print(f"  Fluid density    ρ_f   = {rho_f} kg/m³")
print(f"  IAP              P     = {P_iap} Pa")
print(f"  Equiv. sphere R  R_eq  = {R_eq:.4f} m")
print(f"  Flexural rigidity D    = {D:.6e} N·m")
print(f"  Constraint angle θ_c   = {np.degrees(theta_c):.1f}° (= 2π/3)")

print("\n--- Method 1: Sphere Formula Applied to n=1 (free shell) ---")
print(f"  K_bend      = n(n-1)(n+2)²D/R⁴ = {K_bend_n1:.6e}  [zero — no bending for n=1]")
print(f"  λ₁          = (n²+n-2+2ν)/(n²+n+1-ν) = {lambda_n1:.6f}")
print(f"  K_memb      = Eh/R² × λ₁ = {K_memb_n1:.6e}")
print(f"  K_prestress = P/R×(n-1)(n+2) = {K_prestress_n1:.6e}  [zero for n=1]")
print(f"  K_total     = {K_total_n1:.6e}")
print(f"  m_eff       = ρ_w·h + ρ_f·R/1 = {m_eff_n1:.4f} kg/m²")
print(f"  ω²          = {omega_sq_n1:.6e} rad²/s²")
print(f"  f₁ (sphere formula) = {f_n1_formula:.4f} Hz")

print("\n--- Method 2: Full Ritz Eigenvalue for n=1 (oblate, free shell) ---")
print(f"  2×2 eigenvalues: {eigvals_ritz}")
print(f"  f₁ (Ritz, lower) = {f_n1_ritz:.4f} Hz")
print(f"  f₁ (Ritz, upper) = {f_n1_ritz_max:.4f} Hz")

print("\n--- Method 3: Rayleigh Estimate (constrained shell, θ_c = 120°) ---")
print(f"  T_shell     = {T_shell:.6e}")
print(f"  T_fluid     = {T_fluid:.6e}")
print(f"  T_ref       = {T_ref:.6e}")
print(f"  V_memb      = {V_memb:.6e}")
print(f"  V_prestress = {V_prestress_boundary:.6e}")
print(f"  V_total     = {V_total:.6e}")
print(f"  f₁ (Rayleigh, constrained) = {f_n1_rayleigh:.4f} Hz")

print("\n--- Method 4: Spring-Mass (constraint ring stiffness) ---")
print(f"  m_cap_shell = {m_cap_shell:.4f} kg")
print(f"  m_added     = {m_added:.4f} kg  (entrained fluid)")
print(f"  m_total_cap = {m_total_cap:.4f} kg")
print(f"  k_memb_ring = {k_memb_ring:.4f} N/m")
print(f"  k_prest_ring= {k_prestress_ring:.4f} N/m")
print(f"  k_total     = {k_total_ring:.4f} N/m")
print(f"  f₁ (spring-mass) = {f_n1_spring:.4f} Hz")

print("\n--- Comparison: n=2 Reference ---")
print(f"  f₂ (v2 formula) = {f2_ref:.4f} Hz  [expected ~3.95 Hz]")
for n_mode in range(2, 6):
    print(f"  f_{n_mode} = {freqs_v2[n_mode]:.4f} Hz")

print("\n--- Summary Table ---")
print(f"  {'Method':<45} {'f₁ [Hz]':>10}")
print(f"  {'-'*45} {'-'*10}")
print(f"  {'Sphere formula (n=1, membrane only)':<45} {f_n1_formula:>10.4f}")
print(f"  {'Ritz eigenvalue (n=1, oblate, free)':<45} {f_n1_ritz:>10.4f}")
print(f"  {'Rayleigh (constrained, θ_c=120°)':<45} {f_n1_rayleigh:>10.4f}")
print(f"  {'Spring-mass (constraint ring)':<45} {f_n1_spring:>10.4f}")
print(f"  {'n=2 (for comparison)':<45} {f2_ref:>10.4f}")

print("\n" + "=" * 72)
print("  PHYSICAL INTERPRETATION")
print("=" * 72)
print("""
1. FREE SHELL (n=1 → 0 Hz):
   For a free shell, n=1 is rigid-body translation — zero frequency.
   The current code correctly returns 0 Hz for this case.

2. CONSTRAINED SHELL ("belly bounce"):
   With pelvic constraint, the lower hemisphere is immobilised.
   The free upper portion oscillates against the constraint,
   giving a nonzero n=1 frequency.  Our estimates place it in the
   range shown above.

3. WHY n=1 IS LESS RELEVANT TO THE "BROWN NOTE":
   - n=1 is TRANSLATIONAL: the belly moves up and down as a rigid
     cap.  There is minimal deformation of the abdominal wall tissue.
   - n≥2 modes are DEFORMATIONAL: the shell changes shape (oblate ↔
     prolate oscillation for n=2).  This squishing motion creates
     strain in the intestinal tissue, which is the putative mechanism
     for mechanotransduction and visceral sensation.
   - Even if n=1 has a lower frequency than n=2, the STRAIN PATTERN
     is fundamentally different:
       • n=1 strain is localised at the constraint boundary (pelvic ring)
       • n=2 strain is distributed over the entire abdominal surface
   - Airborne acoustic coupling to n=1 is dipole-order (pressure
     gradient across the body), which is weak at infrasonic frequencies
     where ka << 1.
   - Whole-body vibration couples primarily to n=1 (rigid translation),
     but this produces discomfort via acceleration/vestibular pathways,
     not via tissue deformation — a qualitatively different mechanism.

4. CONCLUSION:
   The reviewer is correct that n=1 is not zero for a constrained
   shell.  However, this mode is translational, not deformational.
   The "brown note" hypothesis concerns tissue distortion, which
   requires n≥2 shape modes.  We should acknowledge the n=1 mode
   in the paper discussion but maintain that n≥2 modes are the
   physiologically relevant ones for mechanotransduction.
""")

# ============================================================
# Sensitivity: vary theta_c
# ============================================================
print("=" * 72)
print("  SENSITIVITY: n=1 frequency vs. constraint angle θ_c")
print("=" * 72)
print(f"\n  {'θ_c [°]':>8}  {'f₁_Rayleigh [Hz]':>16}  {'f₁_spring [Hz]':>15}")
print(f"  {'--------':>8}  {'----------------':>16}  {'---------------':>15}")

for theta_c_deg in [90, 100, 110, 120, 130, 140, 150, 160]:
    tc = np.radians(theta_c_deg)

    # Rayleigh
    V_m = 0.0
    T_s = 0.0
    T_fl = 0.0
    for i in range(N_int):
        th = 0.5 * (theta[i] + theta[i + 1])
        wv = np.cos(th) if th <= tc else 0.0
        area_elem = 2 * np.pi * R**2 * np.sin(th) * dtheta
        V_m += (E * h / R**2) * lambda_n1 * wv**2 * area_elem
        T_s += rho_w * h * wv**2 * area_elem
        T_fl += rho_f * R * wv**2 * area_elem

    N_th = P_iap * R / 2
    dw = np.sin(tc) / R
    rc = 2 * np.pi * R * np.sin(tc)
    V_p = N_th * dw**2 * R * rc * h
    f_ray = np.sqrt(max(0, (V_m + V_p) / (T_s + T_fl))) / (2 * np.pi)

    # Spring-mass
    m_cs = rho_w * h * 2 * np.pi * R**2 * (1 - np.cos(tc))
    V_c = (2.0 / 3.0) * np.pi * R**3 * (1 - np.cos(tc))
    m_a = 0.5 * rho_f * V_c
    m_tc = m_cs + m_a
    k_mr = E * h / R * rc * np.sin(tc) / R
    k_pr = N_th / R * rc
    f_spr = np.sqrt((k_mr + k_pr) / m_tc) / (2 * np.pi)

    print(f"  {theta_c_deg:>8.0f}  {f_ray:>16.4f}  {f_spr:>15.4f}")

print()
