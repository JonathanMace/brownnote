"""Rayleigh-Ritz modal analysis for a fluid-filled spherical shell.

Numerical eigenvalue analysis to validate analytical natural-frequency
predictions and quantify the effect of boundary conditions on modal
frequencies — addressing Reviewer B's concern (M4) about partial BCs.

Five cases are compared:

1. **Free complete sphere** (analytical Lamb benchmark)
2. **Free complete sphere** (Rayleigh-Ritz, validation)
3. **Hemisphere, simply-supported at equator**
4. **Hemisphere, clamped at equator** (anterior abdominal wall model)
5. **75 % shell, clamped** (25 % surface constrained)

Method
------
Coupled Rayleigh-Ritz in (w, u_θ) with Legendre-polynomial basis.
Both radial displacement *w* and tangential displacement *u_θ* are
expanded independently, and the full membrane + bending strain energy
is evaluated from the exact strain-displacement relations of thin-shell
theory (no Lamb decoupling approximation on the sub-domain).  BCs are
enforced via null-space projection of the constraint matrix.

References
----------
.. [1] Lamb, H. (1882). Proc. London Math. Soc., 13, 189-212.
.. [2] Soedel, W. (2004). *Vibrations of Shells and Plates*, 3rd ed.
.. [3] Leissa, A. W. (1973). *Vibration of Shells*, NASA SP-288.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.special import legendre as legendre_poly

logger = logging.getLogger(__name__)


# =========================================================================
# Material / geometry
# =========================================================================

@dataclass
class ShellProperties:
    """Material and geometric properties of the fluid-filled shell."""

    E: float = 0.1e6          # Young's modulus [Pa]
    nu: float = 0.45           # Poisson's ratio
    rho_s: float = 1100.0      # Shell density [kg/m³]
    h: float = 0.01            # Wall thickness [m]
    R: float = 0.162           # Equivalent sphere radius [m]
    rho_f: float = 1000.0      # Interior fluid density [kg/m³]
    P_iap: float = 1500.0      # Intra-abdominal pressure [Pa]

    @property
    def D(self) -> float:
        """Flexural rigidity D = Eh³ / [12(1 − ν²)]."""
        return self.E * self.h ** 3 / (12.0 * (1.0 - self.nu ** 2))


# =========================================================================
# Analytical Lamb solution
# =========================================================================

def lamb_frequency(n: int, p: ShellProperties, *, with_fluid: bool = True) -> float:
    """Lamb (1882) natural frequency for mode *n* of a free sphere."""
    D = p.D
    k_bend = n * (n - 1) * (n + 2) ** 2 * D / p.R ** 4
    lam_n = (n ** 2 + n - 2 + 2 * p.nu) / (n ** 2 + n + 1 - p.nu)
    k_memb = p.E * p.h / p.R ** 2 * lam_n
    k_pre = p.P_iap / p.R * (n - 1) * (n + 2)
    k_total = k_bend + k_memb + k_pre
    m_eff = p.rho_s * p.h + (p.rho_f * p.R / n if with_fluid else 0.0)
    return float(np.sqrt(max(k_total / m_eff, 0.0)) / (2.0 * np.pi))


# =========================================================================
# Coupled (w, u_θ) Rayleigh-Ritz solver
# =========================================================================

class CoupledRitzSolver:
    """Coupled Rayleigh-Ritz eigenvalue solver for spherical-shell vibration.

    DOF vector  q = [a₂ … a_N,  b₂ … b_N]  where

        w(θ)  = Σ  aₙ Pₙ(cos θ)           (radial displacement)
        u_θ(θ) = Σ  bₙ dPₙ/dθ              (tangential displacement)

    Strain-displacement relations (Love–Kirchhoff thin shell):

        ε_θ  = (1/R)(du_θ/dθ + w)
        ε_φ  = (1/R)(u_θ cot θ + w)
        κ_θ  = (1/R²)(du_θ/dθ − d²w/dθ²)
        κ_φ  = (1/R²)(u_θ cot θ − cot θ dw/dθ)

    Stiffness and mass matrices are assembled by Gauss-Legendre quadrature
    over [0, θ_max].  Boundary conditions are imposed via null-space
    projection of the constraint matrix.
    """

    def __init__(
        self,
        props: ShellProperties,
        n_min: int = 2,
        n_max: int = 15,
        n_quad: int = 300,
    ) -> None:
        self.props = props
        self.n_min = n_min
        self.n_max = n_max
        self.n_quad = n_quad
        self.modes = list(range(n_min, n_max + 1))
        self.N = len(self.modes)       # basis functions per variable
        self.ndof = 2 * self.N         # total DOFs

    # -----------------------------------------------------------------
    # public API
    # -----------------------------------------------------------------

    def solve(
        self,
        theta_max: float = np.pi,
        bc: str = "free",
    ) -> tuple[np.ndarray, np.ndarray]:
        """Solve the generalised eigenvalue problem  K q = ω² M q.

        Parameters
        ----------
        theta_max : float
            Upper limit of integration (radians).
        bc : {"free", "simply-supported", "clamped"}
            Boundary condition at θ = θ_max.

        Returns
        -------
        freqs_hz, eigvecs
        """
        K = self._assemble_stiffness(theta_max)
        M = self._assemble_mass(theta_max)

        if bc in ("clamped", "simply-supported"):
            C = self._constraint_matrix(theta_max, bc)
            _, s, Vt = np.linalg.svd(C, full_matrices=True)
            rank = int(np.sum(s > 1e-12 * s[0]))
            Null = Vt[rank:].T
            K = Null.T @ K @ Null
            M = Null.T @ M @ Null

        K, M = self._regularise(K, M)
        eigenvalues, eigvecs = eigh(K, M)

        pos = eigenvalues > 1e-8 * np.max(np.abs(eigenvalues))
        omega2 = eigenvalues[pos]
        vecs = eigvecs[:, pos]
        freqs = np.sqrt(np.maximum(omega2, 0.0)) / (2.0 * np.pi)
        order = np.argsort(freqs)
        return freqs[order], vecs[:, order]

    # -----------------------------------------------------------------
    # quadrature
    # -----------------------------------------------------------------

    def _gauss_quad(self, theta_max: float):
        nodes, weights = np.polynomial.legendre.leggauss(self.n_quad)
        theta = 0.5 * theta_max * (nodes + 1.0)
        wq = 0.5 * theta_max * weights
        return theta, wq

    # -----------------------------------------------------------------
    # basis-function evaluation
    # -----------------------------------------------------------------

    def _eval_basis(self, theta: np.ndarray):
        """Pre-compute strains and curvatures for every DOF at every quad point.

        Returns arrays of shape (ndof, n_quad) for ε_θ, ε_φ, κ_θ, κ_φ,
        plus the P and S arrays (for the mass matrix) and the raw basis
        values at quad points.
        """
        x = np.cos(theta)
        sin_t = np.sin(theta)
        cos_t = x
        R = self.props.R
        N = self.N
        ndof = self.ndof
        nq = len(theta)

        eps_t = np.zeros((ndof, nq))
        eps_p = np.zeros((ndof, nq))
        kap_t = np.zeros((ndof, nq))
        kap_p = np.zeros((ndof, nq))

        # Basis for mass: w-basis = P_n,  u-basis = dP_n/dθ = -sinθ P_n'
        w_basis = np.zeros((N, nq))
        u_basis = np.zeros((N, nq))

        for i, n in enumerate(self.modes):
            Pn = legendre_poly(n)
            dPn = Pn.deriv()
            Pv = Pn(x)
            dPv = dPn(x)
            nn1 = n * (n + 1)

            w_basis[i] = Pv
            u_basis[i] = -sin_t * dPv          # dP_n/dθ

            # ── DOF i: w = P_n, u_θ = 0 ────────────────────────────
            # ε_θ = (1/R)(0 + P_n)
            eps_t[i] = Pv / R
            # ε_φ = (1/R)(0 + P_n)
            eps_p[i] = Pv / R
            # κ_θ = (1/R²)(0 − d²P_n/dθ²)
            #      = (1/R²)(n(n+1)P_n − cosθ P_n')
            kap_t[i] = (nn1 * Pv - cos_t * dPv) / R ** 2
            # κ_φ = (1/R²)(0 − cotθ dP_n/dθ) = cosθ P_n' / R²
            kap_p[i] = cos_t * dPv / R ** 2

            # ── DOF N+i: w = 0, u_θ = dP_n/dθ = −sinθ P_n' ───────
            # du_θ/dθ = d²P_n/dθ² = cosθ P_n' − n(n+1) P_n
            du_dt = cos_t * dPv - nn1 * Pv
            # u_θ cotθ = −sinθ P_n' × cosθ/sinθ = −cosθ P_n'
            u_cot = -cos_t * dPv

            # ε_θ = (1/R)(du_θ/dθ + 0) = du_dt / R
            eps_t[N + i] = du_dt / R
            # ε_φ = (1/R)(u_θ cotθ + 0) = u_cot / R
            eps_p[N + i] = u_cot / R
            # κ_θ = (1/R²)(du_θ/dθ − 0) = du_dt / R²
            kap_t[N + i] = du_dt / R ** 2
            # κ_φ = (1/R²)(u_θ cotθ − 0) = u_cot / R²
            kap_p[N + i] = u_cot / R ** 2

        return eps_t, eps_p, kap_t, kap_p, w_basis, u_basis

    # -----------------------------------------------------------------
    # stiffness assembly
    # -----------------------------------------------------------------

    def _assemble_stiffness(self, theta_max: float) -> np.ndarray:
        """Build the full membrane + bending + pre-stress stiffness matrix."""
        p = self.props
        theta, wq = self._gauss_quad(theta_max)
        eps_t, eps_p, kap_t, kap_p, _, _ = self._eval_basis(theta)

        sin_t = np.sin(theta)
        # integration weight including surface-area factor 2πR² sinθ
        W = wq * sin_t * 2.0 * np.pi * p.R ** 2     # (nq,)

        # membrane coefficient  Eh / (1 − ν²)
        Cm = p.E * p.h / (1.0 - p.nu ** 2)
        # bending coefficient D
        Cb = p.D

        # Vectorised assembly via outer products:
        #   K_ij = Cm [ε_θi ε_θj + ε_φi ε_φj + ν(ε_θi ε_φj + ε_φi ε_θj)]
        #        + Cb [κ_θi κ_θj + κ_φi κ_φj + ν(κ_θi κ_φj + κ_φi κ_θj)]
        #        all weighted by W

        def _bilinear(A: np.ndarray, B: np.ndarray, nu: float) -> np.ndarray:
            """Compute Σ_k [A_ik A_jk + B_ik B_jk + ν(A_ik B_jk + B_ik A_jk)] W_k."""
            Aw = A * W[np.newaxis, :]           # (ndof, nq)
            Bw = B * W[np.newaxis, :]
            return (Aw @ A.T + Bw @ B.T
                    + nu * (Aw @ B.T + Bw @ A.T))

        K = Cm * _bilinear(eps_t, eps_p, p.nu) + Cb * _bilinear(kap_t, kap_p, p.nu)

        # Pre-stress from intra-abdominal pressure
        # Adds geometric stiffness ∝ P_iap for radial deformations.
        # For a pressurised sphere the geometric stiffness bilinear form is:
        #   k_g(w,v) = (P/R) ∫ [dw/dθ dv/dθ + cotθ(w dv/dθ + v dw/dθ)
        #              + 2wv] sinθ dθ × 2πR²
        # A simpler approximation: P/R × <∇_s w, ∇_s v> + 2P/R <w,v>
        # For the mixed DOFs it's more complex; use the radial-radial block
        # as dominant (tangential prestress is secondary).
        if p.P_iap > 0:
            K += self._prestress_matrix(theta_max)

        return K

    def _prestress_matrix(self, theta_max: float) -> np.ndarray:
        """Geometric stiffness from intra-abdominal pressure.

        Approximate form: adds P_iap/R × surface-gradient inner product
        for the radial DOFs (dominant contribution).
        """
        p = self.props
        N = self.N
        ndof = self.ndof
        theta, wq = self._gauss_quad(theta_max)
        x = np.cos(theta)
        sin_t = np.sin(theta)
        W = wq * sin_t * 2.0 * np.pi * p.R ** 2

        # Surface gradient of w = P_n:  |∇_s P_n|² = (dP_n/dθ)²/R²
        # Pre-stress stiffness for radial modes:
        #   k_g = (P/R) ∫ [∇_s w · ∇_s v + 2wv/R²] R² sinθ dθ 2π
        K_g = np.zeros((ndof, ndof))
        dw = np.zeros((N, len(theta)))
        Pw = np.zeros((N, len(theta)))
        for i, n in enumerate(self.modes):
            Pn = legendre_poly(n)
            dPn = Pn.deriv()
            Pw[i] = Pn(x)
            dw[i] = -sin_t * dPn(x)           # dP_n/dθ

        pref = p.P_iap / p.R
        # gradient term (ww block only)
        dw_W = dw * W[np.newaxis, :] / p.R ** 2
        K_grad = pref * (dw_W @ dw.T)
        # curvature term
        Pw_W = Pw * W[np.newaxis, :] * 2.0 / p.R ** 2
        K_curv = pref * (Pw_W @ Pw.T)

        K_g[:N, :N] = K_grad + K_curv
        return K_g

    # -----------------------------------------------------------------
    # mass assembly
    # -----------------------------------------------------------------

    def _assemble_mass(self, theta_max: float) -> np.ndarray:
        """Mass matrix: shell inertia (w² + u²) + fluid added mass (w²).

        Fluid added mass uses the full-sphere approximation ρ_f R / n
        per unit area for Legendre mode *n*.  For off-diagonal (n ≠ m)
        fluid-mass terms the geometric mean √(R/n × R/m) is used.
        """
        p = self.props
        N = self.N
        ndof = self.ndof
        theta, wq = self._gauss_quad(theta_max)
        sin_t = np.sin(theta)
        W = wq * sin_t * 2.0 * np.pi * p.R ** 2

        _, _, _, _, w_basis, u_basis = self._eval_basis(theta)

        # Shell mass:  ρ_s h (w² + u_θ²)
        wW = w_basis * W[np.newaxis, :]     # (N, nq)
        uW = u_basis * W[np.newaxis, :]

        Mww_shell = p.rho_s * p.h * (wW @ w_basis.T)
        Muu_shell = p.rho_s * p.h * (uW @ u_basis.T)

        # Fluid added mass (radial DOFs only):
        #   m_fluid_n = ρ_f R / n  per unit surface area
        # For the bilinear form ∫ m_fluid × w_i w_j dA we use
        #   √(m_n m_m) × ∫ P_n P_m dA   (geometric-mean symmetrisation)
        m_fl = np.array([p.rho_f * p.R / n for n in self.modes])
        sqrt_m = np.sqrt(m_fl)
        S_ww = wW @ w_basis.T                # overlap on domain
        Mww_fluid = np.outer(sqrt_m, sqrt_m) * S_ww

        M = np.zeros((ndof, ndof))
        M[:N, :N] = Mww_shell + Mww_fluid
        M[N:, N:] = Muu_shell
        return M

    # -----------------------------------------------------------------
    # constraints
    # -----------------------------------------------------------------

    def _constraint_matrix(self, theta_max: float, bc: str) -> np.ndarray:
        """Constraint matrix  C q = 0  at θ = θ_max.

        Simply-supported:  w = 0, u_θ = 0   (2 constraints)
        Clamped:           w = 0, u_θ = 0, dw/dθ = 0   (3 constraints)
        """
        x_bc = np.cos(theta_max)
        sin_bc = np.sin(theta_max)
        N = self.N
        ndof = self.ndof

        rows: list[np.ndarray] = []

        # w(θ_max) = 0   →   Σ a_n P_n(x_bc) = 0
        c_w = np.zeros(ndof)
        for i, n in enumerate(self.modes):
            c_w[i] = legendre_poly(n)(x_bc)
        rows.append(c_w)

        # u_θ(θ_max) = 0   →   Σ b_n S_n(θ_max) = 0
        # where S_n = dP_n/dθ = −sinθ P_n'(x)
        c_u = np.zeros(ndof)
        for i, n in enumerate(self.modes):
            c_u[N + i] = -sin_bc * legendre_poly(n).deriv()(x_bc)
        rows.append(c_u)

        if bc == "clamped":
            # dw/dθ(θ_max) = 0   →  Σ a_n dP_n/dθ(θ_max) = 0
            c_dw = np.zeros(ndof)
            for i, n in enumerate(self.modes):
                c_dw[i] = -sin_bc * legendre_poly(n).deriv()(x_bc)
            rows.append(c_dw)

        C = np.array(rows)
        return C

    # -----------------------------------------------------------------
    # regularisation
    # -----------------------------------------------------------------

    @staticmethod
    def _regularise(K, M, tol=1e-10):
        eigvals, V = eigh(M)
        keep = eigvals > tol * np.max(eigvals)
        Vk = V[:, keep]
        return Vk.T @ K @ Vk, Vk.T @ M @ Vk


# =========================================================================
# Verification helper
# =========================================================================

def _verify_ritz_vs_lamb(
    props: ShellProperties,
    freqs_ritz: np.ndarray,
    n_check: int = 6,
) -> list[dict]:
    rows = []
    for i in range(min(n_check, len(freqs_ritz))):
        n = i + 2
        f_lamb = lamb_frequency(n, props)
        f_ritz = freqs_ritz[i]
        err = abs(f_ritz - f_lamb) / f_lamb * 100 if f_lamb > 0 else 0.0
        rows.append({"n": n, "f_lamb": f_lamb, "f_ritz": f_ritz, "err_pct": err})
    return rows


# =========================================================================
# Main
# =========================================================================

def main() -> None:
    """Run the full modal analysis for all BC cases."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    props = ShellProperties()
    solver = CoupledRitzSolver(props, n_min=2, n_max=15, n_quad=300)

    sep = "=" * 72

    print(f"\n{sep}")
    print("  RAYLEIGH-RITZ MODAL ANALYSIS — FLUID-FILLED SPHERICAL SHELL")
    print(f"  Coupled (w, u_θ) formulation with Legendre basis")
    print(sep)
    print(f"  E  = {props.E/1e6:.3f} MPa    ν = {props.nu}")
    print(f"  ρ_s= {props.rho_s:.0f} kg/m³   ρ_f= {props.rho_f:.0f} kg/m³")
    print(f"  h  = {props.h*1e3:.1f} mm       R  = {props.R*1e3:.1f} mm")
    print(f"  D  = {props.D:.6f} N·m      P_iap= {props.P_iap:.0f} Pa")
    print(f"  Basis: P_n, n = {solver.n_min}…{solver.n_max}  "
          f"({solver.N} per variable, {solver.ndof} total DOFs)")
    print(sep)

    results: dict = {
        "material_properties": {
            "E_Pa": props.E, "nu": props.nu,
            "rho_shell_kg_m3": props.rho_s,
            "rho_fluid_kg_m3": props.rho_f,
            "h_m": props.h, "R_m": props.R,
            "D_Nm": props.D, "P_iap_Pa": props.P_iap,
        },
        "method": "Coupled (w, u_theta) Rayleigh-Ritz, Legendre basis",
        "n_basis_range": [solver.n_min, solver.n_max],
        "n_quadrature": solver.n_quad,
    }

    # ── Case 1: Analytical Lamb ─────────────────────────────────────────
    print(f"\n{'─'*72}")
    print("  CASE 1: Free Complete Sphere — Lamb (1882) Analytical")
    print(f"{'─'*72}")
    analytical: dict[int, float] = {}
    for n in range(2, 11):
        f = lamb_frequency(n, props)
        analytical[n] = f
        print(f"    n = {n:2d}   f = {f:8.3f} Hz")
    results["analytical_lamb_hz"] = {str(k): v for k, v in analytical.items()}

    # ── Case 2: Free sphere Ritz (validation) ───────────────────────────
    print(f"\n{'─'*72}")
    print("  CASE 2: Free Complete Sphere — Rayleigh-Ritz (validation)")
    print(f"{'─'*72}")
    freqs_free, _ = solver.solve(theta_max=np.pi, bc="free")

    vrows = _verify_ritz_vs_lamb(props, freqs_free)
    for r in vrows:
        print(
            f"    n = {r['n']:2d}   Lamb = {r['f_lamb']:8.3f} Hz   "
            f"Ritz = {r['f_ritz']:8.3f} Hz   err = {r['err_pct']:.2f} %"
        )
    max_err = max(r["err_pct"] for r in vrows)
    status = "PASS" if max_err < 5.0 else "CHECK"
    print(f"    → Validation {status}: max error = {max_err:.2f} %")
    results["ritz_free_sphere_hz"] = freqs_free[:10].tolist()
    results["validation_max_error_pct"] = max_err

    # ── Case 3: Hemisphere simply-supported ─────────────────────────────
    print(f"\n{'─'*72}")
    print("  CASE 3: Hemisphere Simply-Supported at Equator (θ_max = π/2)")
    print(f"{'─'*72}")
    freqs_ss, _ = solver.solve(theta_max=np.pi / 2, bc="simply-supported")
    for i in range(min(8, len(freqs_ss))):
        print(f"    Mode {i+1:2d}   f = {freqs_ss[i]:8.3f} Hz")
    results["ritz_hemisphere_ss_hz"] = freqs_ss[:10].tolist()

    # ── Case 4: Hemisphere clamped ──────────────────────────────────────
    print(f"\n{'─'*72}")
    print("  CASE 4: Hemisphere Clamped at Equator (θ_max = π/2)")
    print(f"{'─'*72}")
    freqs_hemi, _ = solver.solve(theta_max=np.pi / 2, bc="clamped")
    for i in range(min(8, len(freqs_hemi))):
        print(f"    Mode {i+1:2d}   f = {freqs_hemi[i]:8.3f} Hz")
    results["ritz_hemisphere_clamped_hz"] = freqs_hemi[:10].tolist()

    # ── Case 5: 25 % surface constrained ────────────────────────────────
    theta_25 = 2.0 * np.pi / 3.0
    print(f"\n{'─'*72}")
    print(f"  CASE 5: 25 % Surface Constrained (θ_max = 2π/3 = 120°)")
    print(f"{'─'*72}")
    freqs_25, _ = solver.solve(theta_max=theta_25, bc="clamped")
    for i in range(min(8, len(freqs_25))):
        print(f"    Mode {i+1:2d}   f = {freqs_25[i]:8.3f} Hz")
    results["ritz_25pct_constrained_hz"] = freqs_25[:10].tolist()

    # ── Comparison table ────────────────────────────────────────────────
    f_a = analytical[2]
    f_free = float(freqs_free[0]) if len(freqs_free) else 0.0
    f_ss = float(freqs_ss[0]) if len(freqs_ss) else 0.0
    f_hemi = float(freqs_hemi[0]) if len(freqs_hemi) else 0.0
    f_25 = float(freqs_25[0]) if len(freqs_25) else 0.0

    print(f"\n{sep}")
    print("  COMPARISON TABLE  (fundamental flexural mode)")
    print(sep)
    hdr = (f"  {'BC Case':<35s} {'f₁ (Hz)':>10s} "
           f"{'f_analyt':>10s} {'Ratio':>8s}")
    print(hdr)
    print(f"  {'─'*63}")

    def _row(lbl: str, f: float) -> str:
        r = f / f_a if f_a > 0 else 0.0
        return f"  {lbl:<35s} {f:>10.3f} {f_a:>10.3f} {r:>8.3f}"

    print(_row("Free sphere (Lamb analytical)", f_a))
    print(_row("Free sphere (Rayleigh-Ritz)", f_free))
    print(_row("Hemisphere simply-supported", f_ss))
    print(_row("Hemisphere clamped", f_hemi))
    print(_row("25 % surface constrained", f_25))
    print(sep)

    results["comparison"] = {
        "free_sphere_analytical_n2_hz": f_a,
        "free_sphere_ritz_n2_hz": f_free,
        "hemisphere_ss_f1_hz": f_ss,
        "hemisphere_clamped_f1_hz": f_hemi,
        "constrained_25pct_f1_hz": f_25,
        "ratio_ss_vs_free": f_ss / f_a if f_a else 0,
        "ratio_clamped_vs_free": f_hemi / f_a if f_a else 0,
        "ratio_25pct_vs_free": f_25 / f_a if f_a else 0,
    }

    # ── Physical interpretation ─────────────────────────────────────────
    r_ss = f_ss / f_a if f_a else 0
    r_cl = f_hemi / f_a if f_a else 0
    r_25 = f_25 / f_a if f_a else 0
    print(f"\n{'─'*72}")
    print("  PHYSICAL INTERPRETATION")
    print(f"{'─'*72}")
    print(f"  Simply-supported hemisphere:  {r_ss:.2f}× free sphere  "
          f"({f_a:.2f} → {f_ss:.2f} Hz)")
    print(f"  Clamped hemisphere:           {r_cl:.2f}× free sphere  "
          f"({f_a:.2f} → {f_hemi:.2f} Hz)")
    print(f"  25 % constrained:             {r_25:.2f}× free sphere  "
          f"({f_a:.2f} → {f_25:.2f} Hz)")
    print()
    if r_cl > 1.2:
        print("  ⇒ Boundary conditions SIGNIFICANTLY shift the predicted")
        print("    natural frequency — Reviewer B's concern is well-founded.")
        print("    The partially-constrained model is more physiologically")
        print("    realistic than the free-sphere idealisation.")
    else:
        print("  ⇒ BC effects are modest for the fundamental mode.")
    print(sep)

    # ── Save ────────────────────────────────────────────────────────────
    out_dir = Path("data/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "fea_modal_results.json"
    with open(out_path, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n  Results saved → {out_path}\n")


if __name__ == "__main__":
    main()
