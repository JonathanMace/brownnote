"""Rayleigh-Ritz modal analysis for a fluid-filled spherical shell.

Numerical eigenvalue analysis to validate analytical natural frequency
predictions and quantify the effect of boundary conditions on modal
frequencies — addressing Reviewer B's concern (M4) about partial BCs.

Three boundary-condition cases are compared:

1. **Free complete sphere** — validates against Lamb (1882) analytical solution
2. **Hemispherical shell clamped at equator** — anterior abdominal wall model
3. **Sphere with 25 % surface constrained** — intermediate BC case

Method
------
Rayleigh-Ritz expansion in Legendre polynomial basis functions
P_n(cos θ) for n = 2 … N_max.  Stiffness and mass matrices are assembled
from analytical modal stiffnesses (Lamb theory) projected onto the
integration domain, with boundary conditions enforced via a penalty method.

The bending component of the stiffness matrix is computed *exactly* from the
shell-curvature bilinear form; the membrane component uses the Lamb modal
stiffness (geometric-mean symmetrisation for off-diagonal terms).

References
----------
.. [1] Lamb, H. (1882). Proc. London Math. Soc., 13, 189-212.
.. [2] Soedel, W. (2004). *Vibrations of Shells and Plates*, 3rd ed.
.. [3] Leissa, A. W. (1973). *Vibration of Shells*, NASA SP-288.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.special import legendre as legendre_poly

logger = logging.getLogger(__name__)


# =========================================================================
# Material / geometry dataclass
# =========================================================================

@dataclass
class ShellProperties:
    """Material and geometric properties of the fluid-filled spherical shell.

    Default values correspond to the *stiff soft-tissue* configuration
    used in the paper (E = 0.1 MPa, oblate spheroid a = 0.18 m, c = 0.12 m
    approximated as an equivalent sphere of radius R = 0.162 m).
    """

    E: float = 0.1e6          # Young's modulus [Pa]
    nu: float = 0.45           # Poisson's ratio
    rho_s: float = 1100.0      # Shell density [kg/m³]
    h: float = 0.01            # Wall thickness [m]
    R: float = 0.162           # Equivalent sphere radius [m]
    rho_f: float = 1000.0      # Interior fluid density [kg/m³]
    P_iap: float = 1500.0      # Intra-abdominal pressure [Pa] (~11 mmHg)

    @property
    def D(self) -> float:
        """Flexural rigidity D = Eh³ / [12(1 − ν²)]."""
        return self.E * self.h ** 3 / (12.0 * (1.0 - self.nu ** 2))


# =========================================================================
# Analytical Lamb solution (free complete sphere)
# =========================================================================

def lamb_frequency(n: int, p: ShellProperties, *, with_fluid: bool = True) -> float:
    """Lamb (1882) natural frequency for mode *n* of a free sphere.

    Includes bending + membrane stiffness, pre-stress from intra-abdominal
    pressure, and (optionally) fluid added mass.
    """
    D = p.D

    # Bending stiffness
    k_bend = n * (n - 1) * (n + 2) ** 2 * D / p.R ** 4

    # Membrane stiffness (tangential-displacement coupling via λ_n)
    lam_n = (n ** 2 + n - 2 + 2 * p.nu) / (n ** 2 + n + 1 - p.nu)
    k_memb = p.E * p.h / p.R ** 2 * lam_n

    # Pre-stress stiffening from IAP
    k_pre = p.P_iap / p.R * (n - 1) * (n + 2)

    k_total = k_bend + k_memb + k_pre

    # Effective mass per unit area
    m_shell = p.rho_s * p.h
    m_fluid = p.rho_f * p.R / n if with_fluid else 0.0
    m_eff = m_shell + m_fluid

    omega2 = k_total / m_eff
    return float(np.sqrt(max(omega2, 0.0)) / (2.0 * np.pi))


# =========================================================================
# Rayleigh-Ritz solver
# =========================================================================

class RayleighRitzSolver:
    """Rayleigh-Ritz eigenvalue solver for spherical-shell vibration.

    The radial displacement is expanded as

        w(θ) = Σ_n  a_n  P_n(cos θ),   n = n_min … n_max

    Stiffness and mass matrices are assembled by numerical quadrature over
    [0, θ_max] and the generalised eigenvalue problem  K a = ω² M a  is
    solved with :func:`scipy.linalg.eigh`.
    """

    def __init__(
        self,
        props: ShellProperties,
        n_min: int = 2,
        n_max: int = 25,
        n_quad: int = 300,
    ) -> None:
        self.props = props
        self.n_min = n_min
        self.n_max = n_max
        self.n_quad = n_quad
        self.modes = list(range(n_min, n_max + 1))
        self.N = len(self.modes)

    # -----------------------------------------------------------------
    # public API
    # -----------------------------------------------------------------

    def solve(
        self,
        theta_max: float = np.pi,
        clamped: bool = False,
        penalty_alpha: float | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Solve the generalised eigenvalue problem.

        Parameters
        ----------
        theta_max : float
            Upper limit of the integration domain (radians).
            π   → full sphere, π/2 → hemisphere.
        clamped : bool
            If *True*, apply penalty constraints for w = dw/dθ = 0 at
            θ = θ_max.
        penalty_alpha : float or None
            Penalty parameter.  If *None* an automatic value is chosen.

        Returns
        -------
        freqs_hz : ndarray
            Positive natural frequencies in ascending order.
        eigvecs : ndarray
            Corresponding Ritz coefficient vectors (columns).
        """
        K = self._build_stiffness(theta_max)
        M = self._build_mass(theta_max)

        if clamped:
            if penalty_alpha is None:
                penalty_alpha = 1000.0 * np.max(np.abs(np.diag(K)))
            K += self._penalty_matrix(theta_max, penalty_alpha)

        # On sub-domains (hemisphere etc.) the Legendre basis can become
        # nearly linearly dependent.  Project onto the well-conditioned
        # subspace of the overlap / mass matrix before solving.
        K, M = self._regularise(K, M, tol=1e-8)

        eigenvalues, eigvecs = eigh(K, M)

        pos = eigenvalues > 1e-6 * np.max(eigenvalues)
        omega2 = eigenvalues[pos]
        vecs = eigvecs[:, pos]

        freqs = np.sqrt(omega2) / (2.0 * np.pi)
        order = np.argsort(freqs)
        return freqs[order], vecs[:, order]

    @staticmethod
    def _regularise(
        K: np.ndarray, M: np.ndarray, tol: float = 1e-8
    ) -> tuple[np.ndarray, np.ndarray]:
        """Project K and M onto the positive-definite subspace of M.

        Drops directions where M has near-zero eigenvalues (relative to
        the largest), which arise when the Legendre basis is nearly
        linearly dependent on a sub-domain of the sphere.
        """
        eigvals_m, V = eigh(M)
        max_eig = np.max(eigvals_m)
        keep = eigvals_m > tol * max_eig
        V_keep = V[:, keep]
        # Project both matrices into the reduced subspace
        K_red = V_keep.T @ K @ V_keep
        M_red = V_keep.T @ M @ V_keep
        return K_red, M_red

    # -----------------------------------------------------------------
    # quadrature helpers
    # -----------------------------------------------------------------

    def _gauss_quad(self, theta_max: float):
        """Return Gauss-Legendre nodes and weights on [0, θ_max]."""
        nodes, weights = np.polynomial.legendre.leggauss(self.n_quad)
        theta = 0.5 * theta_max * (nodes + 1.0)
        w = 0.5 * theta_max * weights
        return theta, w

    def _legendre_at_quad(self, theta: np.ndarray):
        """Evaluate P_n(cos θ) and dP_n/dx(cos θ) at quadrature points."""
        x = np.cos(theta)
        N = self.N
        npts = len(x)
        P = np.zeros((N, npts))
        dP = np.zeros((N, npts))
        for i, n in enumerate(self.modes):
            Pn = legendre_poly(n)
            dPn = Pn.deriv()
            P[i] = Pn(x)
            dP[i] = dPn(x)
        return x, P, dP

    # -----------------------------------------------------------------
    # overlap matrix  S_nm = ∫ P_n P_m sin θ dθ
    # -----------------------------------------------------------------

    def _overlap_matrix(self, theta_max: float) -> np.ndarray:
        theta, wq = self._gauss_quad(theta_max)
        _, P, _ = self._legendre_at_quad(theta)
        sin_theta = np.sin(theta)
        # S_ij = Σ_k  P_i(k) P_j(k) sin θ(k) w(k)
        Pw = P * (sin_theta * wq)[np.newaxis, :]   # (N, npts)
        return Pw @ P.T                              # (N, N)

    # -----------------------------------------------------------------
    # bending stiffness (exact curvature bilinear form)
    # -----------------------------------------------------------------

    def _bending_matrix(self, theta_max: float) -> np.ndarray:
        """Bending-energy bilinear form  a_b(P_n, P_m).

        Uses the exact thin-shell curvature-change expressions:

            κ_θ = −(1/R²) d²w/dθ²  =  (1/R²)[n(n+1)P_n − x P_n']
            κ_φ = −(cot θ / R²) dw/dθ  =  (x / R²) P_n'

        Energy density:  D/2 [κ_θ² + κ_φ² + 2ν κ_θ κ_φ]
        """
        p = self.props
        theta, wq = self._gauss_quad(theta_max)
        x, P, dP = self._legendre_at_quad(theta)
        sin_theta = np.sin(theta)

        N = self.N
        # A_i = R² κ_θ(P_i) = n(n+1) P_n − x P_n'
        # B_i = R² κ_φ(P_i) = x P_n'
        A = np.zeros((N, len(x)))
        B = np.zeros((N, len(x)))
        for i, n in enumerate(self.modes):
            nn1 = n * (n + 1)
            A[i] = nn1 * P[i] - x * dP[i]
            B[i] = x * dP[i]

        prefactor = 2.0 * np.pi * p.D / p.R ** 2
        wsin = sin_theta * wq                    # (npts,)

        # K_b[i,j] = prefactor * Σ_k [A_i A_j + B_i B_j + ν(A_i B_j + A_j B_i)] w·sinθ
        K_b = np.zeros((N, N))
        for i in range(N):
            for j in range(i, N):
                integrand = (
                    A[i] * A[j]
                    + B[i] * B[j]
                    + p.nu * (A[i] * B[j] + B[i] * A[j])
                )
                val = np.dot(integrand, wsin)
                K_b[i, j] = prefactor * val
                K_b[j, i] = K_b[i, j]

        return K_b

    # -----------------------------------------------------------------
    # membrane stiffness (Lamb modal approximation)
    # -----------------------------------------------------------------

    def _membrane_matrix(self, theta_max: float) -> np.ndarray:
        """Membrane stiffness using Lamb modal stiffness per mode.

        Off-diagonal terms are symmetrised with the geometric mean.
        """
        p = self.props
        S = self._overlap_matrix(theta_max)
        N = self.N

        k_memb = np.zeros(N)
        for i, n in enumerate(self.modes):
            lam_n = (n ** 2 + n - 2 + 2 * p.nu) / (n ** 2 + n + 1 - p.nu)
            k_memb[i] = p.E * p.h / p.R ** 2 * lam_n

        # K_m[i,j] = √(k_i k_j) × S_ij × 2π R²
        sqrt_k = np.sqrt(k_memb)
        K_m = np.outer(sqrt_k, sqrt_k) * S * (2.0 * np.pi * p.R ** 2)
        return K_m

    # -----------------------------------------------------------------
    # pre-stress stiffness from intra-abdominal pressure
    # -----------------------------------------------------------------

    def _prestress_matrix(self, theta_max: float) -> np.ndarray:
        """Geometric stiffness from intra-abdominal pressure."""
        p = self.props
        S = self._overlap_matrix(theta_max)
        N = self.N

        k_pre = np.zeros(N)
        for i, n in enumerate(self.modes):
            k_pre[i] = p.P_iap / p.R * (n - 1) * (n + 2)

        sqrt_k = np.sqrt(np.maximum(k_pre, 0.0))
        K_p = np.outer(sqrt_k, sqrt_k) * S * (2.0 * np.pi * p.R ** 2)
        return K_p

    # -----------------------------------------------------------------
    # total stiffness
    # -----------------------------------------------------------------

    def _build_stiffness(self, theta_max: float) -> np.ndarray:
        return (
            self._bending_matrix(theta_max)
            + self._membrane_matrix(theta_max)
            + self._prestress_matrix(theta_max)
        )

    # -----------------------------------------------------------------
    # mass matrix (shell + fluid added mass)
    # -----------------------------------------------------------------

    def _build_mass(self, theta_max: float) -> np.ndarray:
        p = self.props
        S = self._overlap_matrix(theta_max)
        N = self.N

        m_eff = np.zeros(N)
        for i, n in enumerate(self.modes):
            m_eff[i] = p.rho_s * p.h + p.rho_f * p.R / n

        sqrt_m = np.sqrt(m_eff)
        return np.outer(sqrt_m, sqrt_m) * S * (2.0 * np.pi * p.R ** 2)

    # -----------------------------------------------------------------
    # penalty matrix for clamped BCs
    # -----------------------------------------------------------------

    def _penalty_matrix(
        self, theta_max: float, alpha: float
    ) -> np.ndarray:
        """Penalty stiffness enforcing w = 0 and dw/dθ = 0 at θ_max."""
        p = self.props
        N = self.N
        K_pen = np.zeros((N, N))

        x_bc = np.cos(theta_max)
        sin_bc = np.sin(theta_max)
        circumference = 2.0 * np.pi * p.R * max(sin_bc, 1e-12)

        vals = np.zeros(N)
        dvals = np.zeros(N)
        for i, n in enumerate(self.modes):
            Pn = legendre_poly(n)
            dPn = Pn.deriv()
            vals[i] = Pn(x_bc)
            dvals[i] = -sin_bc * dPn(x_bc)   # dP_n/dθ = −sin θ P_n'(x)

        # displacement constraint:  w(θ_max) = 0
        K_pen += alpha * np.outer(vals, vals) * circumference
        # slope constraint:  dw/dθ(θ_max) = 0
        K_pen += alpha * np.outer(dvals, dvals) * circumference / p.R

        return K_pen


# =========================================================================
# Verification: check Ritz recovers Lamb on the full sphere
# =========================================================================

def _verify_ritz_vs_lamb(
    props: ShellProperties,
    freqs_ritz: np.ndarray,
    n_check: int = 6,
) -> list[dict]:
    """Compare Ritz free-sphere frequencies against Lamb analytical."""
    rows = []
    for i in range(min(n_check, len(freqs_ritz))):
        n = i + 2  # modes start at n = 2
        f_lamb = lamb_frequency(n, props)
        f_ritz = freqs_ritz[i]
        err = abs(f_ritz - f_lamb) / f_lamb * 100 if f_lamb > 0 else 0.0
        rows.append({"n": n, "f_lamb": f_lamb, "f_ritz": f_ritz, "err_pct": err})
    return rows


# =========================================================================
# Main driver
# =========================================================================

def main() -> None:
    """Run the full modal analysis for all three BC cases."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )

    props = ShellProperties()
    solver = RayleighRitzSolver(props, n_min=2, n_max=25, n_quad=300)

    sep = "=" * 72

    # -- header -----------------------------------------------------------
    print(f"\n{sep}")
    print("  RAYLEIGH-RITZ MODAL ANALYSIS — FLUID-FILLED SPHERICAL SHELL")
    print(sep)
    print(f"  E  = {props.E/1e6:.3f} MPa    ν = {props.nu}")
    print(f"  ρ_s= {props.rho_s:.0f} kg/m³   ρ_f= {props.rho_f:.0f} kg/m³")
    print(f"  h  = {props.h*1e3:.1f} mm       R  = {props.R*1e3:.1f} mm")
    print(f"  D  = {props.D:.6f} N·m      P_iap= {props.P_iap:.0f} Pa")
    print(f"  Basis: P_n, n = {solver.n_min}…{solver.n_max}  "
          f"({solver.N} functions, {solver.n_quad}-pt quadrature)")
    print(sep)

    results: dict = {
        "material_properties": {
            "E_Pa": props.E,
            "nu": props.nu,
            "rho_shell_kg_m3": props.rho_s,
            "rho_fluid_kg_m3": props.rho_f,
            "h_m": props.h,
            "R_m": props.R,
            "D_Nm": props.D,
            "P_iap_Pa": props.P_iap,
        },
        "method": "Rayleigh-Ritz with Legendre polynomial basis",
        "n_basis_min": solver.n_min,
        "n_basis_max": solver.n_max,
        "n_quadrature": solver.n_quad,
    }

    # ── Case 1: Analytical Lamb (free complete sphere) ──────────────────
    print(f"\n{'─'*72}")
    print("  CASE 1: Free Complete Sphere — Analytical Lamb (1882)")
    print(f"{'─'*72}")
    analytical: dict[int, float] = {}
    for n in range(2, 11):
        f = lamb_frequency(n, props)
        analytical[n] = f
        print(f"    n = {n:2d}   f = {f:8.3f} Hz")

    results["analytical_lamb_hz"] = {str(k): v for k, v in analytical.items()}

    # ── Case 2: Rayleigh-Ritz, free full sphere (validation) ────────────
    print(f"\n{'─'*72}")
    print("  CASE 2: Free Complete Sphere — Rayleigh-Ritz (validation)")
    print(f"{'─'*72}")
    freqs_free, _ = solver.solve(theta_max=np.pi, clamped=False)

    vrows = _verify_ritz_vs_lamb(props, freqs_free)
    for r in vrows:
        print(
            f"    n = {r['n']:2d}   Lamb = {r['f_lamb']:8.3f} Hz   "
            f"Ritz = {r['f_ritz']:8.3f} Hz   err = {r['err_pct']:.2f} %"
        )

    max_err = max(r["err_pct"] for r in vrows)
    status = "PASS" if max_err < 1.0 else "CHECK"
    print(f"    → Validation {status}: max error = {max_err:.2f} %")

    results["ritz_free_sphere_hz"] = freqs_free[:10].tolist()
    results["validation_max_error_pct"] = max_err

    # ── Case 3: Hemisphere clamped at equator ───────────────────────────
    print(f"\n{'─'*72}")
    print("  CASE 3: Hemisphere Clamped at Equator (θ_max = π/2)")
    print(f"{'─'*72}")
    freqs_hemi, vecs_hemi = solver.solve(
        theta_max=np.pi / 2, clamped=True
    )
    for i in range(min(8, len(freqs_hemi))):
        print(f"    Mode {i+1:2d}   f = {freqs_hemi[i]:8.3f} Hz")

    results["ritz_hemisphere_clamped_hz"] = freqs_hemi[:10].tolist()

    # ── Case 4: 25 % surface constrained ────────────────────────────────
    # Free domain [0, θ_f] with clamped BC at θ_f.
    # 75 % free surface → 2πR²(1−cos θ_f) = 0.75 × 4πR²  ⇒  θ_f = 2π/3
    theta_25 = 2.0 * np.pi / 3.0
    print(f"\n{'─'*72}")
    print(f"  CASE 4: 25 % Surface Constrained (θ_max = 2π/3 = 120°)")
    print(f"{'─'*72}")
    freqs_25, _ = solver.solve(theta_max=theta_25, clamped=True)
    for i in range(min(8, len(freqs_25))):
        print(f"    Mode {i+1:2d}   f = {freqs_25[i]:8.3f} Hz")

    results["ritz_25pct_constrained_hz"] = freqs_25[:10].tolist()

    # ── Comparison table ────────────────────────────────────────────────
    f_a = analytical[2]
    f_free = float(freqs_free[0]) if len(freqs_free) > 0 else 0.0
    f_hemi = float(freqs_hemi[0]) if len(freqs_hemi) > 0 else 0.0
    f_25 = float(freqs_25[0]) if len(freqs_25) > 0 else 0.0

    print(f"\n{sep}")
    print("  COMPARISON TABLE  (fundamental flexural mode)")
    print(sep)
    hdr = f"  {'BC Case':<35s} {'f₁ (Hz)':>10s} {'f_analytical':>13s} {'Ratio':>8s}"
    print(hdr)
    print(f"  {'─'*66}")

    def _row(label: str, f: float) -> str:
        ratio = f / f_a if f_a > 0 else 0.0
        return f"  {label:<35s} {f:>10.3f} {f_a:>13.3f} {ratio:>8.3f}"

    print(_row("Free sphere (Lamb analytical)", f_a))
    print(_row("Free sphere (Rayleigh-Ritz)", f_free))
    print(_row("Hemisphere clamped at equator", f_hemi))
    print(_row("25 % surface constrained", f_25))
    print(sep)

    results["comparison"] = {
        "free_sphere_analytical_n2_hz": f_a,
        "free_sphere_ritz_n2_hz": f_free,
        "hemisphere_clamped_f1_hz": f_hemi,
        "constrained_25pct_f1_hz": f_25,
        "ratio_hemisphere_vs_free": f_hemi / f_a if f_a else 0,
        "ratio_25pct_vs_free": f_25 / f_a if f_a else 0,
    }

    # ── Physical interpretation ─────────────────────────────────────────
    print(f"\n{'─'*72}")
    print("  PHYSICAL INTERPRETATION")
    print(f"{'─'*72}")
    ratio_h = f_hemi / f_a if f_a else 0
    ratio_25 = f_25 / f_a if f_a else 0
    print(f"  Clamping the equator raises the fundamental frequency by a")
    print(f"  factor of {ratio_h:.2f}×  ({f_a:.2f} → {f_hemi:.2f} Hz).")
    print(f"  A 25 %-surface constraint gives {ratio_25:.2f}×  "
          f"({f_a:.2f} → {f_25:.2f} Hz).")
    print()
    print("  The frequency increase is driven by two effects:")
    print("    1. Reduced vibrating mass (smaller shell area + less")
    print("       fluid participating as added mass)")
    print("    2. Increased constraint stiffness from the clamped boundary")
    print()
    if ratio_h > 1.5:
        print("  ⇒ Boundary conditions have a SIGNIFICANT effect on the")
        print("    predicted natural frequency — Reviewer B's concern is")
        print("    well-founded.  The partially-constrained model is more")
        print("    physiologically realistic than the free-sphere idealisation.")
    else:
        print("  ⇒ Boundary conditions shift frequencies modestly.")
    print(sep)

    # ── Save results ────────────────────────────────────────────────────
    out_dir = Path("data/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "fea_modal_results.json"
    with open(out_path, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n  Results saved → {out_path}")
    print()


if __name__ == "__main__":
    main()
