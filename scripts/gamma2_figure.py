#!/usr/bin/env python3
"""
Generate modal participation factor Γ₂(θ_c) figure and constraint geometry diagram.

Outputs:
    papers/paper1-brown-note/figures/fig_gamma2_thetac.pdf
    papers/paper1-brown-note/figures/fig_gamma2_thetac.png
    papers/paper1-brown-note/figures/fig_constraint_geometry.pdf
    papers/paper1-brown-note/figures/fig_constraint_geometry.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.special import legendre
from scipy import integrate

# ── JSV house style ──────────────────────────────────────────────────
JSV_RC = {
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.grid": True,
    "grid.color": "#cccccc",
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "lines.linewidth": 1.2,
    "lines.markersize": 4,
    "axes.prop_cycle": plt.cycler("color", list(plt.cm.tab10.colors)),
}
plt.rcParams.update(JSV_RC)

SINGLE_COL = 84 / 25.4   # 3.31 in (JSV single column)
DOUBLE_COL = 174 / 25.4   # 6.85 in (JSV double column)

C_BLUE   = plt.cm.tab10(0)
C_ORANGE = plt.cm.tab10(1)
C_GREEN  = plt.cm.tab10(2)
C_RED    = plt.cm.tab10(3)
C_PURPLE = plt.cm.tab10(4)
C_GRAY   = plt.cm.tab10(7)

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "papers" / "paper1-brown-note" / "figures"

# ── Canonical parameters ─────────────────────────────────────────────
A_SEMI = 0.18   # semi-major axis [m]
C_SEMI = 0.12   # semi-minor axis [m]


# ── Physics functions ────────────────────────────────────────────────

def oblate_sigma(u, a, c):
    """Surface metric σ(u) = √(c² + (a²−c²)u²), u = cosθ."""
    return np.sqrt(c**2 + (a**2 - c**2) * u**2)


def participation_factor(a, c, n, theta_c):
    """
    Modal participation factor Γ_n for vertical base excitation.

    θ_c = polar angle below which shell is constrained.
    Free region: θ ∈ [0, θ_c] → u ∈ [cos(θ_c), 1].
    """
    Pn = legendre(n)
    u_c = np.cos(theta_c)

    # Numerator: a · |∫_{u_c}^{1} u·P_n(u) du|
    num, _ = integrate.quad(lambda u: u * Pn(u), u_c, 1.0)
    num = a * num

    # Denominator: ∫_{-1}^{1} P_n²(u)·σ(u) du
    den, _ = integrate.quad(
        lambda u: Pn(u)**2 * oblate_sigma(np.asarray(u), a, c), -1, 1
    )

    return abs(num / den)


def compute_gamma_sweep(n, theta_array):
    """Compute Γ_n over an array of θ_c values."""
    return np.array([
        participation_factor(A_SEMI, C_SEMI, n, tc) for tc in theta_array
    ])


def _save(fig, name):
    """Save figure as PDF and PNG."""
    for ext in (".pdf", ".png"):
        path = FIG_DIR / f"{name}{ext}"
        fig.savefig(path)
        print(f"  Saved: {path}  ({path.stat().st_size / 1024:.1f} KB)")


# ── FIGURE 1: Γ_n(θ_c) ─────────────────────────────────────────────

def make_gamma_figure():
    """Main figure: Γ₂, Γ₃, Γ₄ as functions of constraint angle θ_c."""
    N_PTS = 200
    theta = np.linspace(0.001, np.pi - 0.001, N_PTS)  # avoid exact 0 and π
    theta_deg = np.degrees(theta)

    # Compute for n=2, 3, 4
    gamma2 = compute_gamma_sweep(2, theta)
    gamma3 = compute_gamma_sweep(3, theta)
    gamma4 = compute_gamma_sweep(4, theta)

    # Find peak of Γ₂
    i_peak = np.argmax(gamma2)
    theta_peak_deg = theta_deg[i_peak]
    gamma2_peak = gamma2[i_peak]

    # Key annotation values
    annotations = {
        90:  (r"$\pi/2$",  participation_factor(A_SEMI, C_SEMI, 2, np.pi / 2)),
        120: (r"$2\pi/3$", participation_factor(A_SEMI, C_SEMI, 2, 2 * np.pi / 3)),
        150: (r"$5\pi/6$", participation_factor(A_SEMI, C_SEMI, 2, 5 * np.pi / 6)),
    }

    # Print numerical results
    print("\n── Key numerical values ──")
    print(f"  Γ₂ peak:  {gamma2_peak:.4f}  at θ_c = {theta_peak_deg:.1f}°")
    for deg, (label, val) in annotations.items():
        print(f"  Γ₂(θ_c = {deg}°):  {val:.4f}")
    print(f"  Γ₂(θ_c = 0°):   {gamma2[0]:.6f}  (fully constrained)")
    print(f"  Γ₂(θ_c = 180°): {gamma2[-1]:.6f}  (free sphere)")

    g3_120 = participation_factor(A_SEMI, C_SEMI, 3, 2 * np.pi / 3)
    g4_120 = participation_factor(A_SEMI, C_SEMI, 4, 2 * np.pi / 3)
    print(f"  Γ₃(θ_c = 120°): {g3_120:.4f}")
    print(f"  Γ₄(θ_c = 120°): {g4_120:.4f}")

    # Create figure
    fig, ax = plt.subplots(figsize=(DOUBLE_COL, DOUBLE_COL * 0.5))

    # Plot main curves
    ax.plot(theta_deg, gamma2, color=C_BLUE, linewidth=1.5,
            label=r"$\Gamma_2$ (quadrupole)", zorder=5)
    ax.plot(theta_deg, gamma3, color=C_ORANGE, linewidth=1.0,
            linestyle="--", label=r"$\Gamma_3$ (octupole)")
    ax.plot(theta_deg, gamma4, color=C_GREEN, linewidth=1.0,
            linestyle="-.", label=r"$\Gamma_4$")

    # Mark canonical value θ_c = 120°
    g2_canon = annotations[120][1]
    ax.plot(120, g2_canon, "o", color=C_BLUE, markersize=6, zorder=10)
    ax.annotate(
        rf"Canonical: $\Gamma_2 = {g2_canon:.2f}$" + "\n"
        + r"$\theta_c = 2\pi/3$",
        xy=(120, g2_canon),
        xytext=(130, g2_canon + 0.12),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="0.3", lw=0.8),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.7", lw=0.5),
    )

    # Mark peak
    ax.plot(theta_peak_deg, gamma2_peak, "v", color=C_RED, markersize=6, zorder=10)
    ax.annotate(
        rf"Peak: $\Gamma_2 = {gamma2_peak:.2f}$" + "\n"
        + rf"$\theta_c = {theta_peak_deg:.0f}°$",
        xy=(theta_peak_deg, gamma2_peak),
        xytext=(theta_peak_deg - 30, gamma2_peak + 0.05),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color=C_RED, lw=0.8),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_RED, lw=0.5, alpha=0.9),
    )

    # Mark free-sphere limit
    ax.annotate(
        r"Free sphere ($\Gamma_2 \to 0$)",
        xy=(180, 0), xytext=(155, 0.10),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="0.3", lw=0.8),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.7", lw=0.5),
    )

    # Annotate key points with dots
    for deg, (label, val) in annotations.items():
        if deg != 120:  # already annotated
            ax.plot(deg, val, "s", color=C_GRAY, markersize=4, zorder=8)

    # Axis labels and formatting
    ax.set_xlabel(r"Constraint angle $\theta_c$ (degrees)")
    ax.set_ylabel(r"Modal participation factor $\Gamma_n$")
    ax.set_xlim(0, 180)
    ax.set_ylim(bottom=0)
    ax.set_xticks([0, 30, 60, 90, 120, 150, 180])

    # Secondary x-axis with radian labels
    ax2 = ax.twiny()
    ax2.set_xlim(0, 180)
    radian_ticks = [0, 30, 60, 90, 120, 150, 180]
    radian_labels = [
        r"$0$", r"$\pi/6$", r"$\pi/3$", r"$\pi/2$",
        r"$2\pi/3$", r"$5\pi/6$", r"$\pi$",
    ]
    ax2.set_xticks(radian_ticks)
    ax2.set_xticklabels(radian_labels, fontsize=8)
    ax2.set_xlabel(r"$\theta_c$ (rad)", fontsize=8)

    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()

    _save(fig, "fig_gamma2_thetac")
    plt.close(fig)


# ── FIGURE 2: Constraint geometry diagram ────────────────────────────

def make_geometry_diagram():
    """Schematic showing the oblate spheroid with constrained/free regions."""
    fig, ax = plt.subplots(figsize=(SINGLE_COL, SINGLE_COL * 1.0))

    a, c = A_SEMI, C_SEMI
    theta_c = 2 * np.pi / 3  # canonical

    # Full ellipse outline
    theta_full = np.linspace(0, 2 * np.pi, 300)
    x_full = a * np.cos(theta_full)
    z_full = c * np.sin(theta_full)

    # Cross-section outline (right half for clarity — show full)
    ax.plot(x_full, z_full, "k-", linewidth=1.2)

    # Constrained region: θ ∈ [θ_c, π] in spheroidal coords
    # θ_c = 2π/3 ≈ 120° measured from north pole
    # In Cartesian cross-section, z = c·cos(θ), x = a·sin(θ)
    # Constrained: θ from θ_c to π (southern cap)
    theta_constrained = np.linspace(theta_c, np.pi, 100)
    x_constr_r = a * np.sin(theta_constrained)
    z_constr = c * np.cos(theta_constrained)
    x_constr_l = -x_constr_r

    # Fill constrained region (lower cap)
    x_fill = np.concatenate([x_constr_r, x_constr_l[::-1]])
    z_fill = np.concatenate([z_constr, z_constr[::-1]])
    ax.fill(x_fill, z_fill, color=C_GRAY, alpha=0.35, label="Constrained")

    # Fill free region (upper cap)
    theta_free = np.linspace(0, theta_c, 100)
    x_free_r = a * np.sin(theta_free)
    z_free = c * np.cos(theta_free)
    x_free = np.concatenate([x_free_r, -x_free_r[::-1]])
    z_free_full = np.concatenate([z_free, z_free[::-1]])
    ax.fill(x_free, z_free_full, color=C_BLUE, alpha=0.12, label="Free surface")

    # Draw the constraint boundary (horizontal dashed line)
    z_boundary = c * np.cos(theta_c)
    x_boundary = a * np.sin(theta_c)
    ax.plot([-x_boundary, x_boundary], [z_boundary, z_boundary],
            "--", color=C_RED, linewidth=1.0)

    # Draw θ_c arc from north pole
    arc_r = 0.06  # arc radius for annotation
    arc_theta = np.linspace(0, theta_c, 50)
    arc_x = arc_r * np.sin(arc_theta)
    arc_z = arc_r * np.cos(arc_theta)
    ax.plot(arc_x, arc_z, "-", color=C_RED, linewidth=0.8)

    # θ_c label
    mid_angle = theta_c / 2
    ax.text(
        arc_r * 1.5 * np.sin(mid_angle),
        arc_r * 1.5 * np.cos(mid_angle),
        r"$\theta_c$",
        fontsize=9, color=C_RED, ha="center", va="center",
    )

    # Vertical axis (dashed)
    ax.plot([0, 0], [-c - 0.02, c + 0.02], ":", color="0.5", linewidth=0.5)

    # North pole label
    ax.text(0, c + 0.015, "North pole\n" + r"($\theta = 0$)",
            fontsize=7, ha="center", va="bottom", color="0.4")

    # Labels for regions
    ax.text(0, c * 0.35, "Free\nregion",
            fontsize=8, ha="center", va="center", color=C_BLUE, weight="bold")
    ax.text(0, z_boundary - 0.025, "Constrained\n(pelvis/spine)",
            fontsize=7, ha="center", va="top", color="0.3", style="italic")

    # Dimension annotations
    # Semi-major axis a
    ax.annotate(
        "", xy=(a, 0), xytext=(0, 0),
        arrowprops=dict(arrowstyle="<->", color="0.3", lw=0.8),
    )
    ax.text(a / 2, -0.012, rf"$a = {a*100:.0f}$ cm",
            fontsize=7, ha="center", va="top", color="0.3")

    # Semi-minor axis c
    ax.annotate(
        "", xy=(0, c), xytext=(0, 0),
        arrowprops=dict(arrowstyle="<->", color="0.3", lw=0.8),
    )
    ax.text(-0.02, c / 2, rf"$c = {c*100:.0f}$ cm",
            fontsize=7, ha="right", va="center", color="0.3", rotation=90)

    # Arrow showing base excitation direction
    ax.annotate(
        "", xy=(0, -c - 0.04), xytext=(0, -c - 0.065),
        arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.2,
                        mutation_scale=10),
    )
    ax.text(0.005, -c - 0.055, r"$\ddot{z}_{\mathrm{base}}$",
            fontsize=8, ha="left", va="center", color=C_RED)

    ax.set_xlim(-a - 0.04, a + 0.04)
    ax.set_ylim(-c - 0.08, c + 0.04)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()
    _save(fig, "fig_constraint_geometry")
    plt.close(fig)


# ── Main ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating Γ₂(θ_c) figure...")
    make_gamma_figure()
    print("\nGenerating constraint geometry diagram...")
    make_geometry_diagram()
    print("\nDone.")
