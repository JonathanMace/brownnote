"""Borborygmi acoustic model: coupled Helmholtz-bubble oscillators for gut sounds.

Models gas pockets in a fluid-filled elastic intestinal tube as constrained
Minnaert bubbles and Helmholtz resonators.  Predicts the frequency range of
borborygmi (stomach / intestinal gurgling) and compares with clinical
measurements (typically 200-550 Hz in healthy adults).

Physics
-------
1. **Free Minnaert bubble**: f = (1/2piR) sqrt(3 gamma P0 / rho_f)
2. **Elastic-wall constraint**: wall stiffness adds K_wall = 2 E_w h_w / [R (1-nu_w)]
   raising the frequency above the free-bubble value.
3. **Helmholtz resonator**: gas pocket + constriction neck gives
   f_H = (c_gas / 2pi) sqrt(A_neck / (L_eff V))
4. **Cylindrical slug**: axial piston mode of an elongated gas column trapped
   between fluid plugs in the intestinal lumen.

Clinical reference frequencies
------------------------------
- Healthy adults: 200-550 Hz, peak ~340 Hz
- Small bowel obstruction: peak ~288 Hz
- Large bowel obstruction: peak ~440 Hz

References
----------
- Minnaert (1933) Phil Mag 16:235
- Cannon (1905) Am J Physiol 12:387
- Du Plessis et al. (2000) Dis Colon Rectum 43:81
- Ching & Tan (2012) World J Gastroenterol 18:4585
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants & intestinal defaults
# ---------------------------------------------------------------------------
GAMMA = 1.4               # polytropic exponent (air, adiabatic)
P_ATM = 101_325.0         # atmospheric pressure [Pa]
P_IAP = 1_000.0           # intra-abdominal pressure [Pa]
RHO_FLUID = 1_020.0       # intestinal fluid density [kg/m^3]
C_GAS = 343.0             # speed of sound in gas (air at 37 deg C) [m/s]

# Intestinal wall defaults
E_WALL = 10.0e3           # Young's modulus of intestinal wall [Pa]
NU_WALL = 0.45            # Poisson's ratio
H_WALL = 3.0e-3           # wall thickness [m]
RHO_WALL = 1_040.0        # wall density [kg/m^3]
R_LUMEN = 0.015           # resting lumen radius [m] (small intestine ~3 cm dia)

# Helmholtz neck defaults
NECK_DIAMETER_DEFAULT = 0.005   # constriction diameter [m]
NECK_LENGTH_DEFAULT = 0.010     # constriction length [m]

FIG_DIR = Path(__file__).resolve().parents[2] / "projects" / "borborygmi" / "figures"


# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------
@dataclass
class BorborygmiParams:
    """Parameters for a borborygmi gas-pocket oscillator.

    Parameters
    ----------
    volume_mL : float
        Gas pocket volume in millilitres (1-50 mL typical).
    tube_diameter_m : float
        Internal diameter of the intestinal segment [m].
    gamma : float
        Polytropic exponent for gas.
    P0 : float
        Ambient pressure (atmospheric + IAP) [Pa].
    rho_fluid : float
        Surrounding fluid density [kg/m^3].
    E_wall : float
        Wall Young's modulus [Pa].
    nu_wall : float
        Wall Poisson's ratio.
    h_wall : float
        Wall thickness [m].
    rho_wall : float
        Wall density [kg/m^3].
    c_gas : float
        Speed of sound in the gas pocket [m/s].
    neck_diameter_m : float
        Helmholtz constriction diameter [m].
    neck_length_m : float
        Helmholtz constriction length [m].
    loss_tangent : float
        Viscoelastic loss tangent of the wall.
    """

    volume_mL: float = 10.0
    tube_diameter_m: float = 0.03
    gamma: float = GAMMA
    P0: float = P_ATM + P_IAP
    rho_fluid: float = RHO_FLUID
    E_wall: float = E_WALL
    nu_wall: float = NU_WALL
    h_wall: float = H_WALL
    rho_wall: float = RHO_WALL
    c_gas: float = C_GAS
    neck_diameter_m: float = NECK_DIAMETER_DEFAULT
    neck_length_m: float = NECK_LENGTH_DEFAULT
    loss_tangent: float = 0.25

    # --- derived quantities ------------------------------------------------

    @property
    def volume_m3(self) -> float:
        """Gas pocket volume in m^3."""
        return self.volume_mL * 1.0e-6

    @property
    def R_sphere(self) -> float:
        """Equivalent spherical radius of the gas pocket [m]."""
        return (3.0 * self.volume_m3 / (4.0 * np.pi)) ** (1.0 / 3.0)

    @property
    def R_lumen(self) -> float:
        """Lumen radius [m]."""
        return self.tube_diameter_m / 2.0

    @property
    def L_slug(self) -> float:
        """Axial length of a cylindrical gas slug filling the lumen [m]."""
        return self.volume_m3 / (np.pi * self.R_lumen ** 2)

    @property
    def Q(self) -> float:
        """Quality factor from loss tangent."""
        zeta = self.loss_tangent / 2.0
        return 1.0 / (2.0 * zeta) if zeta > 0 else float("inf")

    @property
    def neck_area(self) -> float:
        """Cross-sectional area of the Helmholtz constriction [m^2]."""
        return np.pi * (self.neck_diameter_m / 2.0) ** 2

    @property
    def neck_length_eff(self) -> float:
        """Effective neck length with end correction [m]."""
        r_neck = self.neck_diameter_m / 2.0
        return self.neck_length_m + 1.6 * r_neck  # Rayleigh end correction


# ---------------------------------------------------------------------------
# Core frequency functions
# ---------------------------------------------------------------------------

def minnaert_frequency(p: BorborygmiParams) -> float:
    """Classical Minnaert resonance of a free spherical gas bubble.

    f = (1 / 2piR) sqrt(3 gamma P0 / rho_f)

    Parameters
    ----------
    p : BorborygmiParams

    Returns
    -------
    float
        Resonant frequency [Hz].
    """
    a = p.R_sphere
    return (1.0 / (2.0 * np.pi * a)) * np.sqrt(3.0 * p.gamma * p.P0 / p.rho_fluid)


def constrained_bubble_frequency(p: BorborygmiParams) -> float:
    """Minnaert bubble with elastic-wall constraint.

    The intestinal wall wraps the bubble and adds both stiffness
    and inertia.  Reduces exactly to Minnaert when E_wall=0, h_wall=0.

    Restoring force per unit area per unit radial displacement:
      k_gas  = 3 gamma P0 / a
      k_wall = 2 E h / [a^2 (1-nu)]

    Effective mass per unit area:
      m_fluid = rho_f a      (radiation added mass)
      m_wall  = rho_w h      (shell inertia)

    omega^2 = (k_gas + k_wall) / (m_fluid + m_wall)

    Parameters
    ----------
    p : BorborygmiParams

    Returns
    -------
    float
        Resonant frequency [Hz].
    """
    a = p.R_sphere
    k_gas = 3.0 * p.gamma * p.P0 / a
    k_wall = 2.0 * p.E_wall * p.h_wall / (a ** 2 * (1.0 - p.nu_wall))
    m_fluid = p.rho_fluid * a
    m_wall = p.rho_wall * p.h_wall
    omega2 = (k_gas + k_wall) / (m_fluid + m_wall)
    return np.sqrt(max(omega2, 0.0)) / (2.0 * np.pi)


def helmholtz_frequency(p: BorborygmiParams) -> float:
    """Helmholtz resonator frequency for a gas pocket with neck constriction.

    f_H = (c_gas / 2pi) sqrt(A_neck / (L_eff * V))

    Models the scenario where peristaltic constriction creates a neck
    connecting the pocket to the rest of the lumen.

    Parameters
    ----------
    p : BorborygmiParams

    Returns
    -------
    float
        Helmholtz resonant frequency [Hz].
    """
    return (p.c_gas / (2.0 * np.pi)) * np.sqrt(
        p.neck_area / (p.neck_length_eff * p.volume_m3)
    )


def cylindrical_axial_frequency(p: BorborygmiParams) -> float:
    """Axial (piston) mode of a cylindrical gas slug in the lumen.

    Gas slug trapped between two fluid plugs oscillates axially.
    Each fluid end-mass: m_end = rho_f * (8/3) * R^3 (radiation mass).

    Parameters
    ----------
    p : BorborygmiParams

    Returns
    -------
    float
        Axial resonant frequency [Hz].
    """
    R = p.R_lumen
    L = p.L_slug
    k_gas = p.gamma * p.P0 * np.pi * R ** 2 / L
    m_end = p.rho_fluid * 8.0 * R ** 3 / 3.0
    omega2 = k_gas / (2.0 * m_end)
    return np.sqrt(max(omega2, 0.0)) / (2.0 * np.pi)


def cylindrical_radial_frequency(p: BorborygmiParams) -> float:
    """Radial breathing mode of a cylindrical gas column in an elastic tube.

    Parameters
    ----------
    p : BorborygmiParams

    Returns
    -------
    float
        Radial resonant frequency [Hz].
    """
    R = p.R_lumen
    K_gas = 2.0 * p.gamma * p.P0  # factor 2 for cylinder (vs 3 for sphere)
    K_wall = p.E_wall * p.h_wall / (R * (1.0 - p.nu_wall ** 2))
    M_fluid = p.rho_fluid * R
    M_wall = p.rho_wall * p.h_wall
    omega2 = (K_gas + K_wall) / (R ** 2 * (M_fluid + M_wall))
    return np.sqrt(max(omega2, 0.0)) / (2.0 * np.pi)


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------

def borborygmi_frequency(
    volume_mL: float = 10.0,
    tube_diameter_m: float = 0.03,
    P0: float = P_ATM + P_IAP,
    mode: Literal["minnaert", "constrained", "helmholtz", "axial", "radial"] = "constrained",
    **kwargs,
) -> float:
    """Compute borborygmi resonant frequency for a given gas pocket.

    Parameters
    ----------
    volume_mL : float
        Gas pocket volume [mL].
    tube_diameter_m : float
        Internal diameter of intestinal segment [m].
    P0 : float
        Ambient pressure [Pa].
    mode : str
        Resonance model to use:
        - ``"minnaert"``: free spherical bubble
        - ``"constrained"``: bubble + elastic wall
        - ``"helmholtz"``: pocket + neck constriction
        - ``"axial"``: cylindrical piston mode
        - ``"radial"``: cylindrical breathing mode
    **kwargs
        Additional keyword arguments passed to :class:`BorborygmiParams`.

    Returns
    -------
    float
        Resonant frequency [Hz].
    """
    p = BorborygmiParams(volume_mL=volume_mL, tube_diameter_m=tube_diameter_m,
                         P0=P0, **kwargs)
    dispatch = {
        "minnaert": minnaert_frequency,
        "constrained": constrained_bubble_frequency,
        "helmholtz": helmholtz_frequency,
        "axial": cylindrical_axial_frequency,
        "radial": cylindrical_radial_frequency,
    }
    if mode not in dispatch:
        raise ValueError(f"Unknown mode {mode!r}; choose from {list(dispatch)}")
    return dispatch[mode](p)


# ---------------------------------------------------------------------------
# Parametric sweeps
# ---------------------------------------------------------------------------

def volume_sweep(
    volumes_mL: np.ndarray | None = None,
    tube_diameter_m: float = 0.03,
    modes: list[str] | None = None,
    **kwargs,
) -> dict:
    """Sweep gas-pocket volume and compute frequencies for each resonance mode.

    Parameters
    ----------
    volumes_mL : array-like, optional
        Volumes to sweep.  Default: 1-50 mL in 100 steps.
    tube_diameter_m : float
        Tube diameter [m].
    modes : list of str, optional
        Resonance modes.  Default: all five.
    **kwargs
        Passed to :func:`borborygmi_frequency`.

    Returns
    -------
    dict
        ``{mode_name: {volumes_mL, frequencies_hz}}``.
    """
    if volumes_mL is None:
        volumes_mL = np.linspace(1.0, 50.0, 100)
    if modes is None:
        modes = ["minnaert", "constrained", "helmholtz", "axial", "radial"]

    results: dict = {}
    for mode in modes:
        freqs = np.array([
            borborygmi_frequency(v, tube_diameter_m, mode=mode, **kwargs)
            for v in volumes_mL
        ])
        results[mode] = {"volumes_mL": np.asarray(volumes_mL), "frequencies_hz": freqs}
    return results


def tube_diameter_sweep(
    diameters_m: np.ndarray | None = None,
    volume_mL: float = 10.0,
    modes: list[str] | None = None,
    **kwargs,
) -> dict:
    """Sweep tube diameter and compute frequencies for each mode.

    Parameters
    ----------
    diameters_m : array-like, optional
        Tube diameters [m].  Default: 2-5 cm in 50 steps.
    volume_mL : float
        Gas pocket volume [mL].
    modes : list of str, optional
        Default: all five.
    **kwargs
        Passed to :func:`borborygmi_frequency`.

    Returns
    -------
    dict
        ``{mode_name: {diameters_m, frequencies_hz}}``.
    """
    if diameters_m is None:
        diameters_m = np.linspace(0.02, 0.05, 50)
    if modes is None:
        modes = ["minnaert", "constrained", "helmholtz", "axial", "radial"]

    results: dict = {}
    for mode in modes:
        freqs = np.array([
            borborygmi_frequency(volume_mL, d, mode=mode, **kwargs)
            for d in diameters_m
        ])
        results[mode] = {"diameters_m": np.asarray(diameters_m), "frequencies_hz": freqs}
    return results


# ---------------------------------------------------------------------------
# Clinical comparison
# ---------------------------------------------------------------------------

# Reported clinical frequency ranges (Hz)
CLINICAL_DATA = {
    "healthy_adult": {"low": 200, "peak": 340, "high": 550},
    "small_bowel_obstruction": {"low": 173, "peak": 288, "high": 667},
    "large_bowel_obstruction": {"low": 309, "peak": 440, "high": 878},
}


def clinical_comparison(volumes_mL: np.ndarray | None = None) -> dict:
    """Compare model predictions with clinical frequency data.

    Returns
    -------
    dict
        Containing model sweep results and clinical reference bands.
    """
    if volumes_mL is None:
        volumes_mL = np.linspace(1.0, 50.0, 100)

    sweep = volume_sweep(volumes_mL)
    return {
        "model": sweep,
        "clinical": CLINICAL_DATA,
        "volumes_mL": volumes_mL,
    }


# ---------------------------------------------------------------------------
# Mode transition map
# ---------------------------------------------------------------------------

ALL_MODES: list[str] = ["minnaert", "constrained", "helmholtz", "axial", "radial"]

MODE_LABELS: dict[str, str] = {
    "minnaert": "Minnaert (free bubble)",
    "constrained": "Constrained bubble",
    "helmholtz": "Helmholtz resonator",
    "axial": "Axial standing wave",
    "radial": "Radial breathing",
}


def mode_transition_map(
    V_range: tuple[float, float] = (0.1, 100.0),
    tube_diameter_m: float = 0.03,
    n_points: int = 500,
    **kwargs: Any,
) -> dict[str, Any]:
    """Compute all 5 mode frequencies across a volume range and find crossovers.

    Parameters
    ----------
    V_range : tuple of float
        (V_min, V_max) in mL.  Default (0.1, 100).
    tube_diameter_m : float
        Internal tube diameter [m].
    n_points : int
        Number of logarithmically-spaced volume points.
    **kwargs
        Additional keyword arguments passed to :class:`BorborygmiParams`.

    Returns
    -------
    dict
        Keys:

        - ``volumes_mL`` : ndarray of shape (n_points,)
        - ``frequencies`` : dict mapping mode name → ndarray of Hz
        - ``dominant_mode`` : ndarray of mode name strings (lowest freq mode at
          each volume)
        - ``crossovers`` : list of dicts, each with ``volume_mL``,
          ``frequency_hz``, ``mode_below`` (dominant before), ``mode_above``
          (dominant after)
    """
    volumes = np.logspace(np.log10(V_range[0]), np.log10(V_range[1]), n_points)

    freq_arrays: dict[str, np.ndarray] = {}
    for mode in ALL_MODES:
        freq_arrays[mode] = np.array([
            borborygmi_frequency(v, tube_diameter_m, mode=mode, **kwargs)
            for v in volumes
        ])

    # Dominant mode = the one with the lowest frequency at each volume
    # (lowest-frequency mode most likely to be excited by broadband peristalsis)
    freq_matrix = np.column_stack([freq_arrays[m] for m in ALL_MODES])
    dominant_idx = np.argmin(freq_matrix, axis=1)
    dominant_mode = np.array([ALL_MODES[i] for i in dominant_idx])

    # Detect crossovers: where dominant mode changes
    crossovers: list[dict[str, Any]] = []
    for i in range(1, len(dominant_mode)):
        if dominant_mode[i] != dominant_mode[i - 1]:
            # Interpolate crossover volume (geometric mean of bracket)
            v_cross = np.sqrt(volumes[i - 1] * volumes[i])
            # Evaluate both modes at crossover to get approximate frequency
            f_below = borborygmi_frequency(
                v_cross, tube_diameter_m, mode=dominant_mode[i - 1], **kwargs
            )
            f_above = borborygmi_frequency(
                v_cross, tube_diameter_m, mode=dominant_mode[i], **kwargs
            )
            crossovers.append({
                "volume_mL": float(v_cross),
                "frequency_hz": float((f_below + f_above) / 2.0),
                "mode_below": str(dominant_mode[i - 1]),
                "mode_above": str(dominant_mode[i]),
            })

    return {
        "volumes_mL": volumes,
        "frequencies": freq_arrays,
        "dominant_mode": dominant_mode,
        "crossovers": crossovers,
    }


# ---------------------------------------------------------------------------
# Figure generation
# ---------------------------------------------------------------------------

def fig_frequency_vs_volume(save: bool = True):
    """Publication-quality figure: predicted borborygmi frequency vs gas pocket volume.

    Four-panel figure:
      (a) All resonance modes vs volume
      (b) Constrained bubble -- effect of tube diameter
      (c) Helmholtz -- effect of neck diameter
      (d) Comparison with clinical frequency bands
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7,
        "figure.dpi": 300,
        "savefig.dpi": 300,
    })

    vols = np.linspace(1.0, 50.0, 200)
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # --- (a) All modes vs volume -------------------------------------------
    ax = axes[0, 0]
    colours = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    labels = ["Minnaert (free)", "Constrained bubble", "Helmholtz",
              "Axial piston", "Radial breathing"]
    modes = ["minnaert", "constrained", "helmholtz", "axial", "radial"]

    for mode, col, lab in zip(modes, colours, labels):
        freqs = np.array([borborygmi_frequency(v, mode=mode) for v in vols])
        ax.semilogy(vols, freqs, color=col, label=lab, linewidth=1.2)

    ax.axhspan(200, 550, alpha=0.12, color="grey", label="Clinical range")
    ax.set_xlabel("Gas pocket volume [mL]")
    ax.set_ylabel("Frequency [Hz]")
    ax.set_title("(a) All resonance modes")
    ax.legend(loc="upper right", fontsize=6)
    ax.set_xlim(1, 50)
    ax.grid(True, alpha=0.3)

    # --- (b) Constrained bubble -- tube diameter ---------------------------
    ax = axes[0, 1]
    diameters = [0.02, 0.03, 0.04, 0.05]
    for d in diameters:
        freqs = np.array([
            borborygmi_frequency(v, tube_diameter_m=d, mode="constrained")
            for v in vols
        ])
        ax.plot(vols, freqs, linewidth=1.2,
                label=f"d = {d*100:.0f} cm")
    ax.axhspan(200, 550, alpha=0.12, color="grey")
    ax.set_xlabel("Gas pocket volume [mL]")
    ax.set_ylabel("Frequency [Hz]")
    ax.set_title("(b) Constrained bubble: tube diameter effect")
    ax.legend(fontsize=7)
    ax.set_xlim(1, 50)
    ax.grid(True, alpha=0.3)

    # --- (c) Helmholtz -- neck diameter ------------------------------------
    ax = axes[1, 0]
    neck_diams = [0.003, 0.005, 0.008, 0.012]
    for nd in neck_diams:
        freqs = np.array([
            borborygmi_frequency(v, mode="helmholtz", neck_diameter_m=nd)
            for v in vols
        ])
        ax.plot(vols, freqs, linewidth=1.2,
                label=f"neck = {nd*1000:.0f} mm")
    ax.axhspan(200, 550, alpha=0.12, color="grey")
    ax.set_xlabel("Gas pocket volume [mL]")
    ax.set_ylabel("Frequency [Hz]")
    ax.set_title("(c) Helmholtz: neck diameter effect")
    ax.legend(fontsize=7)
    ax.set_xlim(1, 50)
    ax.grid(True, alpha=0.3)

    # --- (d) Clinical comparison -------------------------------------------
    ax = axes[1, 1]
    comp = clinical_comparison(vols)
    constrained = comp["model"]["constrained"]
    ax.plot(constrained["volumes_mL"], constrained["frequencies_hz"],
            color="#1f77b4", linewidth=2, label="Model (constrained)")

    clin = comp["clinical"]
    band_colours = {"healthy_adult": "#2ca02c",
                    "small_bowel_obstruction": "#ff7f0e",
                    "large_bowel_obstruction": "#d62728"}
    band_labels = {"healthy_adult": "Healthy (200-550 Hz)",
                   "small_bowel_obstruction": "SBO (173-667 Hz)",
                   "large_bowel_obstruction": "LBO (309-878 Hz)"}

    for cond, col in band_colours.items():
        d = clin[cond]
        ax.axhspan(d["low"], d["high"], alpha=0.10, color=col)
        ax.axhline(d["peak"], color=col, linestyle="--", linewidth=0.8,
                   label=band_labels[cond])

    ax.set_xlabel("Gas pocket volume [mL]")
    ax.set_ylabel("Frequency [Hz]")
    ax.set_title("(d) Model vs clinical borborygmi frequencies")
    ax.legend(fontsize=6, loc="upper right")
    ax.set_xlim(1, 50)
    ax.set_ylim(0, 1200)
    ax.grid(True, alpha=0.3)

    fig.suptitle("What Pitch Is a Growling Stomach?\n"
                 "Predicted borborygmi frequencies from coupled Helmholtz-bubble models",
                 fontsize=11, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.94])

    if save:
        FIG_DIR.mkdir(parents=True, exist_ok=True)
        for ext in ("png", "pdf"):
            fig.savefig(FIG_DIR / f"fig_borborygmi_frequency_vs_volume.{ext}",
                        dpi=300, bbox_inches="tight")
        print(f"Saved figure to {FIG_DIR}")

    return fig


def plot_mode_transition_map(
    V_range: tuple[float, float] = (0.1, 100.0),
    tube_diameter_m: float = 0.03,
    n_points: int = 500,
    save: bool = True,
    save_dir: Path | str | None = None,
    **kwargs: Any,
):
    """Publication-quality mode transition map for the borborygmi paper.

    Single-panel figure with log-log axes showing all 5 resonance modes
    vs gas pocket volume, with clinical frequency band shading and
    crossover markers.

    Parameters
    ----------
    V_range : tuple of float
        (V_min, V_max) in mL.
    tube_diameter_m : float
        Internal tube diameter [m].
    n_points : int
        Volume resolution.
    save : bool
        If True, save PNG and PDF.
    save_dir : Path or str, optional
        Output directory.  Default: ``paper2-gas-pockets/figures/``.
    **kwargs
        Passed to :func:`mode_transition_map`.

    Returns
    -------
    matplotlib.figure.Figure
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
        "font.size": 10,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8,
        "figure.dpi": 300,
        "savefig.dpi": 300,
    })

    data = mode_transition_map(V_range, tube_diameter_m, n_points, **kwargs)
    volumes = data["volumes_mL"]
    freqs = data["frequencies"]
    crossovers = data["crossovers"]

    colours = {
        "minnaert": "#1f77b4",
        "constrained": "#ff7f0e",
        "helmholtz": "#2ca02c",
        "axial": "#d62728",
        "radial": "#9467bd",
    }
    linestyles = {
        "minnaert": "-",
        "constrained": "-",
        "helmholtz": "--",
        "axial": "-.",
        "radial": ":",
    }

    fig, ax = plt.subplots(figsize=(8, 5.5))

    # Clinical frequency band
    ax.axhspan(200, 550, alpha=0.10, color="#888888", zorder=0)
    ax.axhline(200, color="#aaaaaa", linewidth=0.5, linestyle="--", zorder=0)
    ax.axhline(550, color="#aaaaaa", linewidth=0.5, linestyle="--", zorder=0)
    ax.text(
        V_range[0] * 1.3, 360, "Clinical range\n(200–550 Hz)",
        fontsize=7, color="#666666", fontstyle="italic", va="center",
    )

    # Mode frequency lines
    for mode in ALL_MODES:
        ax.loglog(
            volumes, freqs[mode],
            color=colours[mode],
            linestyle=linestyles[mode],
            linewidth=1.8,
            label=MODE_LABELS[mode],
            zorder=2,
        )

    # Crossover markers
    for xo in crossovers:
        ax.plot(
            xo["volume_mL"], xo["frequency_hz"],
            marker="o", markersize=7, color="black",
            markerfacecolor="white", markeredgewidth=1.5,
            zorder=5,
        )
        ax.annotate(
            f'{xo["mode_below"]}→{xo["mode_above"]}',
            xy=(xo["volume_mL"], xo["frequency_hz"]),
            xytext=(8, 8), textcoords="offset points",
            fontsize=6, color="#333333",
            arrowprops=dict(arrowstyle="-", color="#999999", lw=0.5),
        )

    # Dominant-mode background shading
    dom = data["dominant_mode"]
    i = 0
    while i < len(dom):
        j = i
        while j < len(dom) and dom[j] == dom[i]:
            j += 1
        mode_name = dom[i]
        v_lo = volumes[i]
        v_hi = volumes[min(j, len(volumes) - 1)]
        ax.axvspan(v_lo, v_hi, alpha=0.04, color=colours[mode_name], zorder=0)
        i = j

    ax.set_xlabel("Gas pocket volume [mL]")
    ax.set_ylabel("Frequency [Hz]")
    ax.set_xlim(V_range)
    ax.set_ylim(10, 20_000)
    ax.grid(True, which="both", alpha=0.15, linewidth=0.5)
    ax.legend(loc="upper right", framealpha=0.9)
    ax.set_title(
        "Mode transition map: borborygmi resonance regimes",
        fontsize=11, fontweight="bold", pad=10,
    )

    fig.tight_layout()

    if save:
        if save_dir is None:
            out = Path(__file__).resolve().parents[2] / "paper2-gas-pockets" / "figures"
        else:
            out = Path(save_dir)
        out.mkdir(parents=True, exist_ok=True)
        for ext in ("png", "pdf"):
            fig.savefig(
                out / f"fig_mode_transition_map.{ext}",
                dpi=300, bbox_inches="tight",
            )
        print(f"Saved mode transition map to {out}")

    return fig


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("Borborygmi Acoustic Model -- Preliminary Results")
    print("=" * 70)

    p = BorborygmiParams()
    print(f"\nDefault parameters:")
    print(f"  Volume:         {p.volume_mL:.1f} mL  (R_sphere = {p.R_sphere*1e3:.1f} mm)")
    print(f"  Tube diameter:  {p.tube_diameter_m*100:.1f} cm")
    print(f"  Slug length:    {p.L_slug*100:.1f} cm")
    print(f"  P0:             {p.P0:.0f} Pa")

    print(f"\nResonant frequencies (10 mL pocket, 3 cm tube):")
    for mode in ["minnaert", "constrained", "helmholtz", "axial", "radial"]:
        f = borborygmi_frequency(10.0, mode=mode)
        print(f"  {mode:15s}: {f:7.1f} Hz")

    print(f"\nVolume sweep (constrained bubble):")
    for v in [1, 5, 10, 20, 50]:
        f = borborygmi_frequency(v, mode="constrained")
        print(f"  {v:3d} mL: {f:7.1f} Hz")

    print(f"\nClinical comparison:")
    for cond, d in CLINICAL_DATA.items():
        print(f"  {cond:30s}: {d['low']}-{d['high']} Hz (peak {d['peak']} Hz)")

    fig = fig_frequency_vs_volume(save=True)
    print("\nDone.")
