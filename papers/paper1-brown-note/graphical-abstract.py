#!/usr/bin/env python3
"""
Graphical abstract for JSV submission.

Creates a side-by-side comparison showing the 10^4 coupling disparity
between airborne infrasound and mechanical whole-body vibration excitation
of abdominal flexural resonance.

Output: paper/graphical-abstract.pdf and paper/graphical-abstract.png
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

# ── Global style ─────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.linewidth": 0.6,
    "mathtext.default": "regular",
})

# Professional colour palette
COL_SHELL      = "#4A7C9B"   # muted steel blue
COL_SHELL_EDGE = "#2C4F6B"
COL_FLUID      = "#A8D0E6"   # light blue interior
COL_SOUND      = "#E8873A"   # warm orange for sound waves
COL_VIB        = "#C0392B"   # red for vibration platform
COL_ARROW      = "#2C3E50"   # dark charcoal
COL_ACCENT     = "#27AE60"   # green accent
COL_BG         = "#FAFBFC"   # near-white
COL_DISP_AIR   = "#E74C3C"  # red for airborne (bad)
COL_DISP_MECH  = "#27AE60"  # green for mechanical (effective)
COL_THRESHOLD  = "#7F8C8D"

# ── Figure geometry ──────────────────────────────────────────────────────
# JSV graphical abstract: ~560 px wide at 300 dpi → 1.87 in.
# Use wider for legibility; let Elsevier scale to column.
fig_w = 6.5   # inches (will be ~1950 px at 300 dpi)
fig_h = 3.0
dpi = 300

fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")

# Layout: three columns — airborne | central label | mechanical
# Use gridspec for fine control
gs = fig.add_gridspec(
    2, 5,
    width_ratios=[2.2, 0.3, 1.0, 0.3, 2.2],
    height_ratios=[1, 0.08],
    hspace=0.05, wspace=0.05,
    left=0.02, right=0.98, top=0.88, bottom=0.08,
)

ax_air  = fig.add_subplot(gs[0, 0])
ax_mid  = fig.add_subplot(gs[0, 2])
ax_mech = fig.add_subplot(gs[0, 4])
ax_bot  = fig.add_subplot(gs[1, :])

for ax in [ax_air, ax_mid, ax_mech, ax_bot]:
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")

ax_bot.set_aspect("auto")


# ── Helper: draw oblate spheroid ─────────────────────────────────────────
def draw_spheroid(ax, cx, cy, a, b, fill_col=COL_FLUID, edge_col=COL_SHELL_EDGE,
                  lw=2.0, deform=0.0):
    """Draw a filled ellipse representing the oblate spheroid cross-section.
    deform > 0 makes it slightly prolate (n=2 flexural bulge)."""
    theta = np.linspace(0, 2 * np.pi, 200)
    # Apply n=2 deformation: r -> r + deform * cos(2*theta)
    r_a = a + deform * np.cos(2 * theta)
    r_b = b + deform * np.cos(2 * theta + np.pi)
    x = cx + r_a * np.cos(theta)
    y = cy + r_b * np.sin(theta)
    ax.fill(x, y, color=fill_col, alpha=0.5, zorder=2)
    ax.plot(x, y, color=edge_col, lw=lw, zorder=3)


def draw_sound_waves(ax, x0, y0, direction="right", n_arcs=4, color=COL_SOUND):
    """Draw concentric arc segments representing incoming sound."""
    sign = 1 if direction == "right" else -1
    for i in range(n_arcs):
        r = 0.12 + i * 0.09
        theta_start = 70 if direction == "right" else 110
        theta_end = -70 if direction == "right" else 250
        arc = mpatches.Arc(
            (x0, y0), 2 * r, 2 * r,
            angle=0, theta1=min(theta_start, theta_end),
            theta2=max(theta_start, theta_end),
            color=color, lw=1.5, alpha=0.6 + 0.1 * (n_arcs - i) / n_arcs,
            zorder=1,
        )
        ax.add_patch(arc)


def draw_platform(ax, cx, cy, w, h, color=COL_VIB):
    """Draw a vibrating platform with motion indicators."""
    rect = mpatches.FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.02",
        facecolor=color, edgecolor="#922B21", lw=1.5, zorder=4,
    )
    ax.add_patch(rect)
    # Vibration zigzag lines below platform
    n_teeth = 6
    zx = np.linspace(cx - w * 0.35, cx + w * 0.35, n_teeth * 2 + 1)
    zy_base = cy - h / 2 - 0.08
    zy = np.array([zy_base + (0.04 if i % 2 == 0 else -0.04) for i in range(len(zx))])
    ax.plot(zx, zy, color="#922B21", lw=1.2, zorder=4)
    # Ground line
    ax.plot([cx - w * 0.45, cx + w * 0.45], [zy_base - 0.06, zy_base - 0.06],
            color="#7F8C8D", lw=1.0, zorder=4)


def draw_displacement_arrow(ax, cx, cy, length, color, label, label_pos="right"):
    """Draw a double-headed arrow showing displacement magnitude."""
    if length < 0.01:
        # Tiny: draw a dot instead
        ax.plot(cx, cy, "o", color=color, ms=4, zorder=5)
        offset = 0.08 if label_pos == "right" else -0.08
        ha = "left" if label_pos == "right" else "right"
        ax.text(cx + offset, cy, label, fontsize=6.5, color=color,
                ha=ha, va="center", fontweight="bold", zorder=6)
    else:
        ax.annotate(
            "", xy=(cx, cy + length / 2), xytext=(cx, cy - length / 2),
            arrowprops=dict(arrowstyle="<->", color=color, lw=1.8),
            zorder=5,
        )
        offset = 0.06 if label_pos == "right" else -0.06
        ha = "left" if label_pos == "right" else "right"
        ax.text(cx + offset, cy, label, fontsize=6.5, color=color,
                ha=ha, va="center", fontweight="bold", zorder=6)


# ══════════════════════════════════════════════════════════════════════════
# LEFT PANEL: Airborne infrasound → tiny displacement
# ══════════════════════════════════════════════════════════════════════════

ax_air.set_xlim(-1.1, 1.1)
ax_air.set_ylim(-1.0, 1.0)

# Sound waves from left
draw_sound_waves(ax_air, -0.85, 0.0, direction="right", n_arcs=5)

# Undeformed spheroid (sound barely moves it)
draw_spheroid(ax_air, 0.15, 0.0, a=0.52, b=0.35)

# Tiny displacement indicator
ax_air.plot(0.15, 0.42, "o", color=COL_DISP_AIR, ms=3, zorder=5)
ax_air.text(0.15, 0.52, "0.028 μm", fontsize=7, color=COL_DISP_AIR,
            ha="center", va="bottom", fontweight="bold", zorder=6)
ax_air.text(0.15, 0.44, "(sub-threshold)", fontsize=5.5, color="#999999",
            ha="center", va="bottom", zorder=6)

# SPL label
ax_air.text(-0.82, -0.55, "120 dB SPL", fontsize=7, color=COL_SOUND,
            ha="left", va="center", fontweight="bold")
ax_air.text(-0.82, -0.68, "λ ≈ 85 m  →  ka ≈ 0.02", fontsize=5.5,
            color="#777777", ha="left", va="center")

# Panel title
ax_air.text(0.05, 0.95, "Airborne Infrasound", fontsize=9,
            fontweight="bold", color=COL_ARROW, ha="center", va="top",
            transform=ax_air.transAxes)

# Red X
ax_air.text(0.15, -0.55, "X", fontsize=16, color=COL_DISP_AIR,
            ha="center", va="center", fontweight="bold", zorder=6,
            fontfamily="sans-serif")
ax_air.text(0.15, -0.72, "Below PIEZO\nthreshold", fontsize=5.5,
            color=COL_DISP_AIR, ha="center", va="center", zorder=6)


# ══════════════════════════════════════════════════════════════════════════
# CENTRE PANEL: Coupling ratio callout
# ══════════════════════════════════════════════════════════════════════════

ax_mid.set_xlim(-1.2, 1.2)
ax_mid.set_ylim(-1.2, 1.2)

# Large "10^4×" label
ax_mid.text(0.0, 0.25, r"$\mathbf{10^4}$×", fontsize=20, color=COL_ARROW,
            ha="center", va="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EBF5FB",
                      edgecolor=COL_SHELL, lw=1.5),
            zorder=6)
ax_mid.text(0.0, -0.15, "coupling\ndisparity", fontsize=7, color="#555555",
            ha="center", va="center", style="italic", zorder=6)

# Arrows pointing left and right
ax_mid.annotate("", xy=(-1.0, 0.25), xytext=(-0.55, 0.25),
                arrowprops=dict(arrowstyle="->", color=COL_DISP_AIR, lw=1.5),
                zorder=5)
ax_mid.annotate("", xy=(1.0, 0.25), xytext=(0.55, 0.25),
                arrowprops=dict(arrowstyle="->", color=COL_DISP_MECH, lw=1.5),
                zorder=5)

# Threshold annotation
ax_mid.plot([-0.4, 0.4], [-0.65, -0.65], "--", color=COL_THRESHOLD, lw=0.8)
ax_mid.text(0.0, -0.75, "PIEZO1/2 threshold\n0.5–2.0 μm", fontsize=5.5,
            color=COL_THRESHOLD, ha="center", va="center")


# ══════════════════════════════════════════════════════════════════════════
# RIGHT PANEL: Mechanical WBV → large displacement
# ══════════════════════════════════════════════════════════════════════════

ax_mech.set_xlim(-1.1, 1.1)
ax_mech.set_ylim(-1.0, 1.0)

# Vibrating platform
draw_platform(ax_mech, 0.0, -0.6, w=0.9, h=0.12)

# Deformed spheroid (visibly distorted — n=2 flexural mode)
draw_spheroid(ax_mech, 0.0, -0.05, a=0.50, b=0.38, deform=0.06)

# Large displacement arrow
ax_mech.annotate(
    "", xy=(0.60, 0.15), xytext=(0.60, -0.25),
    arrowprops=dict(arrowstyle="<->", color=COL_DISP_MECH, lw=2.0),
    zorder=5,
)
ax_mech.text(0.68, -0.05, "3,200 μm", fontsize=7, color=COL_DISP_MECH,
             ha="left", va="center", fontweight="bold", zorder=6)

# Upward excitation arrows from platform into shell
for xoff in [-0.2, 0.0, 0.2]:
    ax_mech.annotate(
        "", xy=(xoff, -0.40), xytext=(xoff, -0.52),
        arrowprops=dict(arrowstyle="-|>", color=COL_VIB, lw=1.5,
                        mutation_scale=10),
        zorder=5,
    )

# Acceleration label
ax_mech.text(0.0, -0.82, "0.5 m/s² RMS", fontsize=7, color=COL_VIB,
             ha="center", va="center", fontweight="bold")
ax_mech.text(0.0, -0.93, "(EU action value)", fontsize=5.5,
             color="#777777", ha="center", va="center")

# Panel title
ax_mech.text(0.5, 0.95, "Whole-Body Vibration", fontsize=9,
             fontweight="bold", color=COL_ARROW, ha="center", va="top",
             transform=ax_mech.transAxes)

# Green check (use matplotlib mathtext checkmark)
ax_mech.text(0.0, 0.50, r"$\checkmark$", fontsize=18, color=COL_DISP_MECH,
             ha="center", va="center", fontweight="bold", zorder=6)
ax_mech.text(0.0, 0.38, "Exceeds threshold\nby 1,000×", fontsize=5.5,
             color=COL_DISP_MECH, ha="center", va="center", zorder=6)


# ══════════════════════════════════════════════════════════════════════════
# BOTTOM BAR: title / takeaway
# ══════════════════════════════════════════════════════════════════════════

ax_bot.set_xlim(0, 1)
ax_bot.set_ylim(0, 1)
ax_bot.text(
    0.5, 0.5,
    "Abdominal flexural resonance (4–10 Hz) is real — "
    "but airborne infrasound cannot excite it to physiological relevance",
    fontsize=7, color=COL_ARROW, ha="center", va="center",
    style="italic",
)


# ── Save ─────────────────────────────────────────────────────────────────
out_dir = Path(__file__).resolve().parent
fig.savefig(out_dir / "graphical-abstract.pdf", dpi=dpi, bbox_inches="tight",
            facecolor="white")
fig.savefig(out_dir / "graphical-abstract.png", dpi=dpi, bbox_inches="tight",
            facecolor="white")
print(f"Saved: {out_dir / 'graphical-abstract.pdf'}")
print(f"Saved: {out_dir / 'graphical-abstract.png'}")
plt.close(fig)
