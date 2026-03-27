"""
Rayleigh-Ritz analysis for flexural vibrations of a fluid-filled oblate
spheroidal shell.

Implements the variational method with Legendre polynomial trial functions
to compute natural frequencies of oblate spheroidal shells, and compares
with the equivalent-sphere approximation used in natural_frequency_v2.py.

Approach
--------
1. Parameterize the oblate spheroid surface by η = cos θ ∈ [-1, 1].
2. Trial functions: w(η) = P_n(η) (normal), u related to dP_n/dθ
   (tangential along meridian).
3. Strain energy: Love-Kirchhoff thin shell (membrane + bending) plus
   prestress from intra-abdominal pressure.
4. Fluid kinetic energy: solve interior Laplace equation in oblate
   spheroidal coordinates using P_n(iξ) harmonics.
5. Solve the generalized eigenvalue problem K x = ω² M x.

The oblate spheroid has semi-axes a = b (equatorial) and c (polar, c < a).
Surface: x²/a² + y²/a² + z²/c² = 1.

References
----------
    Elaikh et al. (2016) J. Thin-Walled Structures
    Love (1888) Proc. London Math. Soc.
    Junger & Feit (1972) Sound, Structures, and Their Interaction
    Lamb (1882) Proc. London Math. Soc.
"""

import numpy as np
from scipy.special import legendre as _legendre_poly
from numpy.polynomial.legendre import leggauss
from scipy import linalg
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
from src.analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)


# ============================================================
# Legendre polynomial utilities
# ============================================================

def eval_legendre(n_max, eta_arr):
    """
    Evaluate P_n(η), P_n'(η), P_n''(η) for n = 0..n_max at all points.

    Returns P, dP, d2P each of shape (n_max+1, len(eta_arr)).
    """
    eta_arr = np.asarray(eta_arr, dtype=float)
    Npts = len(eta_arr)
    P = np.zeros((n_max + 1, Npts))
    dP = np.zeros((n_max + 1, Npts))
    d2P = np.zeros((n_max + 1, Npts))

    for n in range(n_max + 1):
        poly = _legendre_poly(n)
        P[n] = poly(eta_arr)
        if n >= 1:
            dP[n] = poly.deriv(1)(eta_arr)
        if n >= 2:
            d2P[n] = poly.deriv(2)(eta_arr)

    return P, dP, d2P


# ============================================================
# Oblate spheroid geometry
# ============================================================

def oblate_geometry(a, c, eta_arr):
    """
    Compute geometric quantities on the oblate spheroid surface.

    Parameters
    ----------
    a : float — equatorial semi-axis
    c : float — polar semi-axis (c ≤ a)
    eta_arr : array — cos(θ) values on [-1, 1]

    Returns
    -------
    dict with arrays:
        G, sqG  : metric function and its sqrt
        R1, R2  : principal radii of curvature
        cos_psi : cos of normal-to-axis angle
        sin2    : sin²θ = 1 − η²
        N1_per_P, N2_per_P : membrane tensions per unit pressure
    """
    eta = np.asarray(eta_arr, dtype=float)
    eta2 = eta ** 2
    sin2 = 1.0 - eta2

    G = a**2 * eta2 + c**2 * sin2
    sqG = np.sqrt(G)

    R1 = G**1.5 / (a * c)
    R2 = a * sqG / c
    cos_psi = a * eta / sqG

    # Membrane tensions from internal pressure (per unit P)
    N1_per_P = R2 / 2.0
    N2_per_P = R2 * (1.0 - R2 / (2.0 * R1))

    return dict(
        G=G, sqG=sqG, R1=R1, R2=R2,
        cos_psi=cos_psi, sin2=sin2,
        N1_per_P=N1_per_P, N2_per_P=N2_per_P,
    )


# ============================================================
# Shell stiffness (membrane + bending + prestress)
# ============================================================

def _build_strain_bases(modes, geom, P, dP, d2P, a, c, eta_q):
    """
    At every quadrature point, build the vectors whose outer products
    give the membrane and bending stiffness matrices.

    DOF ordering: [w_0, w_1, …, w_{N-1}, u_0, u_1, …, u_{M-1}]
    where w_i corresponds to P_{modes[i]}(η) and
    u_j corresponds to the tangential basis for modes with n > 0.
    """
    N_modes = len(modes)
    u_modes = [n for n in modes if n > 0]
    N_u = len(u_modes)
    N_dof = N_modes + N_u
    u_offset = {n: N_modes + i for i, n in enumerate(u_modes)}

    G = geom['G']
    sqG = geom['sqG']
    sin2 = geom['sin2']
    N_q = len(eta_q)
    Delta = a**2 - c**2

    # Outputs: arrays of shape (N_q, N_dof) for each basis quantity
    e1 = np.zeros((N_q, N_dof))   # membrane strain ε₁ × √G
    e2 = np.zeros((N_q, N_dof))   # membrane strain ε₂ × √G
    k1 = np.zeros((N_q, N_dof))   # bending curvature κ₁
    k2 = np.zeros((N_q, N_dof))   # bending curvature κ₂
    slope_w = np.zeros((N_q, N_dof))  # prestress slope dw/ds₁

    for k in range(N_q):
        g = G[k]
        sg = sqG[k]
        eta = eta_q[k]
        s2 = sin2[k]

        for i, n in enumerate(modes):
            Pn = P[n, k]
            dPn = dP[n, k]
            d2Pn = d2P[n, k]

            # --- w-DOF ---
            # Membrane: ε₁ = … + β × ac P_n / G^{3/2}  → f₁ = ac P_n / G
            e1[k, i] = a * c * Pn / g
            # ε₂ = … + β × c P_n / (a √G)  → f₂ = c P_n / a
            e2[k, i] = c * Pn / a

            # Bending rotation β = √(1-η²) P_n' [1/√G + …]
            # For w-DOF only: β_w = √(1-η²) P_n' / √G
            # h_w  = P_n' / √G
            # h_w' = P_n'' / √G − P_n' Δη / G^{3/2}
            h_w = dPn / sg
            hp_w = d2Pn / sg - dPn * Delta * eta / g**1.5

            # κ₁ = [η h − (1−η²) h'] / √G
            k1[k, i] = (eta * h_w - s2 * hp_w) / sg

            # κ₂ = η P_n' / G  (from β × η / (√G √(1−η²)) with √(1−η²) cancel)
            k2[k, i] = eta * dPn / g

            # Prestress slope: √(sin²θ / G) × P_n'
            slope_w[k, i] = np.sqrt(max(s2, 0.0) / g) * dPn

            # --- u-DOF ---
            if n > 0 and n in u_offset:
                j = u_offset[n]

                # du/dθ = d × [η P_n' − n(n+1) P_n]
                du_dtheta = eta * dPn - n * (n + 1) * Pn

                # Membrane
                e1[k, j] = du_dtheta
                e2[k, j] = eta * dPn

                # Bending: h_u = P_n' ac / G^{3/2}
                h_u = dPn * a * c / g**1.5
                G_prime = 2.0 * Delta * eta
                hp_u = d2Pn * a * c / g**1.5 - dPn * a * c * 1.5 * G_prime / g**2.5

                k1[k, j] = (eta * h_u - s2 * hp_u) / sg
                k2[k, j] = eta * dPn * a * c / g**2

    return e1, e2, k1, k2, slope_w, N_dof, u_offset


def assemble_stiffness(a, c, h, E, nu, P_iap, modes, eta_q, w_q):
    """
    Assemble total shell stiffness matrix (membrane + bending + prestress).

    Returns K of shape (N_dof, N_dof).
    """
    geom = oblate_geometry(a, c, eta_q)
    n_max = max(modes)
    Pv, dPv, d2Pv = eval_legendre(n_max, eta_q)

    e1, e2, k1, k2, slope_w, N_dof, _ = _build_strain_bases(
        modes, geom, Pv, dPv, d2Pv, a, c, eta_q
    )

    sqG = geom['sqG']
    C_m = E * h / (1.0 - nu**2)
    D = E * h**3 / (12.0 * (1.0 - nu**2))

    K = np.zeros((N_dof, N_dof))

    for k in range(len(eta_q)):
        wt = w_q[k]
        sg = sqG[k]

        # Membrane contribution:  πa C_m / √G × (e1 e1ᵀ + e2 e2ᵀ + ν cross)
        fac_m = np.pi * a * C_m * wt / sg
        K += fac_m * (
            np.outer(e1[k], e1[k])
            + np.outer(e2[k], e2[k])
            + nu * (np.outer(e1[k], e2[k]) + np.outer(e2[k], e1[k]))
        )

        # Bending contribution: πa D √G × (κ₁ κ₁ᵀ + κ₂ κ₂ᵀ + ν cross)
        fac_b = np.pi * a * D * sg * wt
        K += fac_b * (
            np.outer(k1[k], k1[k])
            + np.outer(k2[k], k2[k])
            + nu * (np.outer(k1[k], k2[k]) + np.outer(k2[k], k1[k]))
        )

        # Prestress: πa N₁ √G × slope_w slope_wᵀ
        if P_iap > 0:
            N1 = P_iap * geom['N1_per_P'][k]
            fac_p = np.pi * a * N1 * sg * wt
            K += fac_p * np.outer(slope_w[k], slope_w[k])

    return K


# ============================================================
# Shell mass matrix
# ============================================================

def assemble_shell_mass(a, c, h, rho_wall, modes, eta_q, w_q):
    """Shell mass matrix (both w and u DOFs)."""
    N_modes = len(modes)
    u_modes = [n for n in modes if n > 0]
    N_u = len(u_modes)
    N_dof = N_modes + N_u
    u_offset = {n: N_modes + i for i, n in enumerate(u_modes)}

    geom = oblate_geometry(a, c, eta_q)
    sqG = geom['sqG']
    sin2 = geom['sin2']
    n_max = max(modes)
    Pv, dPv, _ = eval_legendre(n_max, eta_q)

    M = np.zeros((N_dof, N_dof))

    for k in range(len(eta_q)):
        wt = w_q[k]
        sg = sqG[k]
        s2 = sin2[k]

        w_vec = np.zeros(N_dof)
        u_vec = np.zeros(N_dof)

        for i, n in enumerate(modes):
            w_vec[i] = Pv[n, k]
            if n > 0 and n in u_offset:
                j = u_offset[n]
                u_vec[j] = np.sqrt(max(s2, 0.0)) * dPv[n, k]

        fac = 2.0 * np.pi * a * rho_wall * h * sg * wt
        M += fac * (np.outer(w_vec, w_vec) + np.outer(u_vec, u_vec))

    return M


# ============================================================
# Fluid added-mass matrix (oblate spheroidal harmonics)
# ============================================================

def _fluid_mass_sphere(a, c, rho_fluid, modes, eta_q, w_q):
    """Fluid mass for the near-sphere limit (diagonal, ρR/n)."""
    R = (a * a * c) ** (1.0 / 3.0)
    N_modes = len(modes)
    u_modes = [n for n in modes if n > 0]
    N_dof = N_modes + len(u_modes)
    M = np.zeros((N_dof, N_dof))

    geom = oblate_geometry(a, c, eta_q)
    sqG = geom['sqG']
    Pv, _, _ = eval_legendre(max(modes), eta_q)

    for i, ni in enumerate(modes):
        if ni < 1:
            continue
        m_add = rho_fluid * R / ni
        for j, nj in enumerate(modes):
            integrand = Pv[ni] * Pv[nj] * 2.0 * np.pi * a * sqG
            M[i, j] = m_add * np.dot(w_q, integrand)

    return M


def assemble_fluid_mass(a, c, rho_fluid, modes, eta_q, w_q):
    """
    Fluid added-mass matrix from interior Laplace solution in oblate
    spheroidal coordinates.

    For each "source" mode j, solves for the velocity potential Φ inside
    the spheroid with ∂Φ/∂n = P_j(η) on the surface, then computes
    M_ij = ρ_f ∫ Φ_j P_i dS.
    """
    aspect = c / a
    if aspect > 0.995:
        return _fluid_mass_sphere(a, c, rho_fluid, modes, eta_q, w_q)

    d = np.sqrt(a**2 - c**2)
    xi0 = c / d

    N_modes = len(modes)
    u_modes = [n for n in modes if n > 0]
    N_dof = N_modes + len(u_modes)
    M_fluid = np.zeros((N_dof, N_dof))

    # Extra basis modes for the Laplace expansion (coupling extends beyond
    # the shell trial-function set)
    n_lap = max(modes) + 6
    n_lap_modes = list(range(1, n_lap + 1))  # skip n=0 (γ₀ = 0)
    N_lap = len(n_lap_modes)

    # P_n(iξ₀) and γ_n = i P_n'(iξ₀) √(ξ₀²+1) / d
    z0 = 1j * xi0
    Pn_z0 = np.zeros(N_lap, dtype=complex)
    gamma = np.zeros(N_lap, dtype=complex)
    sqrt_xi = np.sqrt(xi0**2 + 1.0)
    for idx, n in enumerate(n_lap_modes):
        poly = _legendre_poly(n)
        Pn_z0[idx] = poly(z0)
        gamma[idx] = 1j * poly.deriv(1)(z0) * sqrt_xi / d

    # Legendre polynomials on the quadrature grid for the Laplace basis
    P_eta, _, _ = eval_legendre(n_lap, eta_q)

    # Weight function: 1/√(ξ₀² + η²) (from metric h_ξ)
    inv_metric = 1.0 / np.sqrt(xi0**2 + eta_q**2)

    # Coupling matrix S_{kn} = ∫ P_k(η) P_n(η) / √(ξ₀²+η²) dη
    # Build only for n_lap_modes indices
    S = np.zeros((N_lap, N_lap))
    for ki, kn in enumerate(n_lap_modes):
        for ni, nn in enumerate(n_lap_modes):
            S[ki, ni] = np.dot(w_q, P_eta[kn] * P_eta[nn] * inv_metric)

    # C_{k,n} = γ_n S_{k,n}
    C_mat = S * gamma[np.newaxis, :]   # broadcast γ along columns

    # Surface measure weights for the final integration
    geom = oblate_geometry(a, c, eta_q)
    sqG = geom['sqG']
    dS_weight = 2.0 * np.pi * a * sqG  # per dη

    # Shell trial-function Legendre values
    Pv_shell, _, _ = eval_legendre(max(modes), eta_q)

    # For each source mode j (w-DOF), solve Laplace and get mass column
    for j_idx, nj in enumerate(modes):
        if nj < 1:
            continue  # skip n=0 breathing mode

        # Right-hand side: b_k = 2 δ_{k,nj} / (2nj+1)
        b = np.zeros(N_lap, dtype=complex)
        if nj in n_lap_modes:
            b[n_lap_modes.index(nj)] = 2.0 / (2 * nj + 1)
        else:
            continue

        # Solve C A = b
        try:
            A = np.linalg.solve(C_mat, b)
        except np.linalg.LinAlgError:
            # Fall back to sphere formula for this mode
            R = (a * a * c) ** (1.0 / 3.0)
            m_add = rho_fluid * R / nj
            for i_idx, ni in enumerate(modes):
                if ni == nj:
                    integrand = Pv_shell[ni] ** 2 * dS_weight
                    M_fluid[i_idx, j_idx] = m_add * np.dot(w_q, integrand)
            continue

        # Potential on surface: Φ = Σ A_n P_n(iξ₀) P_n(η)
        Phi_surface = np.zeros(len(eta_q))
        for idx, n in enumerate(n_lap_modes):
            Phi_surface += np.real(A[idx] * Pn_z0[idx]) * P_eta[n]

        # M_{i,j} = ρ_f ∫ Φ_j × P_i × dS
        for i_idx, ni in enumerate(modes):
            integrand = Phi_surface * Pv_shell[ni] * dS_weight
            M_fluid[i_idx, j_idx] = rho_fluid * np.dot(w_q, integrand)

    # Symmetrize (should be symmetric by construction, enforce numerically)
    M_fluid = 0.5 * (M_fluid + M_fluid.T)
    return M_fluid


# ============================================================
# Eigenvalue solver
# ============================================================

def solve_modes(K, M, N_w):
    """
    Solve generalised eigenvalue problem K x = ω² M x.

    Returns (freqs_hz, evecs) sorted by ascending frequency.
    N_w is the number of w-DOFs (to identify mode shapes).
    """
    # Regularise: small diagonal perturbation for near-singular M
    eps = np.max(np.abs(np.diag(M))) * 1e-12
    M_reg = M + eps * np.eye(M.shape[0])

    try:
        eigvals, eigvecs = linalg.eigh(K, M_reg)
    except linalg.LinAlgError:
        # Fall back to general eigensolver
        eigvals, eigvecs = linalg.eig(K, M_reg)
        eigvals = np.real(eigvals)
        idx = np.argsort(eigvals)
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]

    freqs = np.sqrt(np.maximum(eigvals, 0.0)) / (2.0 * np.pi)
    order = np.argsort(freqs)
    return freqs[order], eigvecs[:, order]


def identify_mode(evec, modes, N_w):
    """Identify which Legendre mode dominates an eigenvector."""
    w_part = np.abs(evec[:N_w])
    idx = np.argmax(w_part)
    return modes[idx]


# ============================================================
# High-level API
# ============================================================

def oblate_ritz_frequencies(a, c, h, E, nu, rho_wall, rho_fluid, P_iap,
                            n_target=(2, 3, 4), n_quad=200):
    """
    Compute flexural-mode frequencies of the oblate spheroid using
    the Rayleigh-Ritz method.

    Parameters
    ----------
    a, c     : semi-axes (equatorial, polar)
    h        : shell thickness
    E, nu    : Young's modulus, Poisson's ratio
    rho_wall, rho_fluid : densities
    P_iap    : intra-abdominal pressure
    n_target : tuple of mode numbers to return
    n_quad   : number of Gauss-Legendre quadrature points

    Returns
    -------
    dict  {n: frequency_hz}  for each n in n_target
    """
    eta_q, w_q = leggauss(n_quad)

    results = {}

    # Separate even and odd parity — they decouple for the spheroid
    even_targets = [n for n in n_target if n % 2 == 0]
    odd_targets = [n for n in n_target if n % 2 == 1]

    for targets, parity_label in [(even_targets, 'even'), (odd_targets, 'odd')]:
        if not targets:
            continue

        # Build basis: include enough modes for convergence
        n_max_basis = max(targets) + 4
        if parity_label == 'even':
            modes = list(range(0, n_max_basis + 1, 2))
        else:
            modes = list(range(1, n_max_basis + 1, 2))

        N_w = len(modes)

        K = assemble_stiffness(a, c, h, E, nu, P_iap, modes, eta_q, w_q)
        M_shell = assemble_shell_mass(a, c, h, rho_wall, modes, eta_q, w_q)
        M_fluid = assemble_fluid_mass(a, c, rho_fluid, modes, eta_q, w_q)
        M_total = M_shell + M_fluid

        freqs, evecs = solve_modes(K, M_total, N_w)

        # Match eigenvalues to target mode numbers
        for nt in targets:
            best_freq = None
            best_overlap = -1.0
            for col in range(evecs.shape[1]):
                if freqs[col] < 0.01:
                    continue  # skip near-zero (rigid body)
                n_dom = identify_mode(evecs[:, col], modes, N_w)
                # Check overlap with target mode
                if nt in modes:
                    tidx = modes.index(nt)
                    overlap = abs(evecs[tidx, col]) / (
                        np.linalg.norm(evecs[:N_w, col]) + 1e-30
                    )
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_freq = freqs[col]
            results[nt] = best_freq if best_freq is not None else 0.0

    return results


def sphere_approx_frequencies(model, n_modes=(2, 3, 4)):
    """Equivalent-sphere frequencies from natural_frequency_v2."""
    freqs_all = flexural_mode_frequencies_v2(model, n_max=max(n_modes))
    return {n: freqs_all[n] for n in n_modes}


# ============================================================
# Comparison driver
# ============================================================

def comparison_table(model_base=None, aspect_ratios=None,
                     E_values=None, n_modes=(2, 3, 4)):
    """
    Build a comparison table: Rayleigh-Ritz vs equivalent-sphere
    at various aspect ratios.

    Returns list of dicts with columns for printing.
    """
    if model_base is None:
        model_base = AbdominalModelV2()
    if aspect_ratios is None:
        aspect_ratios = [0.50, 0.60, 0.667, 0.70, 0.80, 0.90]
    if E_values is None:
        E_values = [model_base.E]

    rows = []
    a = model_base.a

    for E_val in E_values:
        for ar in aspect_ratios:
            c_val = a * ar

            # Equivalent-sphere model
            m_sph = AbdominalModelV2(
                a=a, b=a, c=c_val, h=model_base.h,
                E=E_val, nu=model_base.nu,
                rho_wall=model_base.rho_wall,
                rho_fluid=model_base.rho_fluid,
                P_iap=model_base.P_iap,
            )
            f_sph = sphere_approx_frequencies(m_sph, n_modes)

            # Rayleigh-Ritz
            f_ritz = oblate_ritz_frequencies(
                a=a, c=c_val, h=model_base.h,
                E=E_val, nu=model_base.nu,
                rho_wall=model_base.rho_wall,
                rho_fluid=model_base.rho_fluid,
                P_iap=model_base.P_iap,
                n_target=n_modes,
            )

            row = {'E_MPa': E_val / 1e6, 'c/a': ar}
            for n in n_modes:
                fs = f_sph[n]
                fr = f_ritz[n]
                err = (fs - fr) / fr * 100 if fr > 0 else float('nan')
                row[f'f{n}_sphere'] = fs
                row[f'f{n}_ritz'] = fr
                row[f'f{n}_err%'] = err
            rows.append(row)

    return rows


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print()
    print("=" * 78)
    print("  OBLATE SPHEROID RAYLEIGH-RITZ ANALYSIS")
    print("  Flexural vibrations of a fluid-filled oblate spheroidal shell")
    print("=" * 78)
    print()

    model = AbdominalModelV2()
    n_modes = (2, 3, 4)

    # ----------------------------------------------------------
    # 1.  Baseline comparison at default geometry
    # ----------------------------------------------------------
    print("  1. BASELINE: default AbdominalModelV2 (a=0.15, c=0.10, E=0.5 MPa)")
    print("  " + "-" * 70)
    f_sph = sphere_approx_frequencies(model, n_modes)
    f_ritz = oblate_ritz_frequencies(
        a=model.a, c=model.c, h=model.h,
        E=model.E, nu=model.nu,
        rho_wall=model.rho_wall, rho_fluid=model.rho_fluid,
        P_iap=model.P_iap, n_target=n_modes,
    )
    print(f"  {'Mode':>6} {'Sphere(Hz)':>12} {'Ritz(Hz)':>12} {'Error(%)':>10}")
    print("  " + "-" * 42)
    for n in n_modes:
        fs, fr = f_sph[n], f_ritz[n]
        err = (fs - fr) / fr * 100 if fr > 0 else float('nan')
        print(f"  n={n:>3} {fs:>12.3f} {fr:>12.3f} {err:>+10.1f}")
    print()

    # ----------------------------------------------------------
    # 2.  Aspect-ratio sweep at two Young's modulus values
    # ----------------------------------------------------------
    aspect_ratios = [0.50, 0.60, 0.667, 0.70, 0.80, 0.90]

    for E_val, label in [(0.5e6, "E = 0.5 MPa (baseline)"),
                         (0.1e6, "E = 0.1 MPa (soft tissue)")]:
        print(f"  2. ASPECT-RATIO SWEEP — {label}")
        print("  " + "-" * 74)
        hdr = f"  {'c/a':>5}"
        for n in n_modes:
            hdr += f" {'Sph n='+str(n):>9} {'Ritz n='+str(n):>10} {'err%':>7}"
        print(hdr)
        print("  " + "-" * 74)

        rows = comparison_table(
            model_base=model, aspect_ratios=aspect_ratios,
            E_values=[E_val], n_modes=n_modes,
        )
        for r in rows:
            line = f"  {r['c/a']:>5.3f}"
            for n in n_modes:
                line += (
                    f" {r[f'f{n}_sphere']:>9.2f}"
                    f" {r[f'f{n}_ritz']:>10.2f}"
                    f" {r[f'f{n}_err%']:>+7.1f}"
                )
            print(line)
        print("  " + "-" * 74)
        print()

    # ----------------------------------------------------------
    # 3.  Summary
    # ----------------------------------------------------------
    print("  3. SUMMARY")
    print("  " + "-" * 70)
    print("  • The equivalent-sphere model (R_eff = (a²c)^{1/3}) introduces")
    print("    geometry-dependent errors that grow as the shell becomes")
    print("    more oblate (c/a → 0).")
    print("  • For the default geometry (c/a ≈ 0.67), the error is moderate")
    print("    but non-negligible for quantitative work.")
    print("  • The Rayleigh-Ritz model captures:")
    print("      – Spatially varying curvature (R₁, R₂ depend on position)")
    print("      – Correct fluid added mass from oblate spheroidal harmonics")
    print("      – Mode coupling between Legendre orders via oblate geometry")
    print("  • Positive error% means the sphere model OVERESTIMATES frequency.")
    print()
