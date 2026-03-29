"""
Sub-bass acoustic coupling model for concert sound pressure levels.

Paper 6: "Can You Feel the Bass?"

Extends Paper 1's flexural shell model to the 20–80 Hz range where the
ka coupling parameter transitions from negligible (<0.01) to appreciable
(~0.05–0.3).  At these frequencies airborne acoustic coupling may become
non-negligible — potentially explaining the "feel it in your gut"
experience at concerts and pipe-organ recitals.

Physics overview
----------------
At the canonical n = 2 flexural resonance (~4 Hz), ka ≈ 0.011 and the
acoustic coupling to flexural modes scales as (ka)^n, yielding
negligible airborne excitation.  At 20–80 Hz, ka rises to 0.06–0.23.
While the abdomen is no longer at flexural resonance, the improved
coupling efficiency may still produce physiologically meaningful tissue
displacement at concert SPLs (100–120 dB).

The model treats the abdomen as a forced, damped oscillator driven
off-resonance by airborne sound, using the energy-consistent (Junger &
Feit reciprocity) method from Paper 1.

Key functions
-------------
- airborne_coupling_ratio  — ka-dependent coupling vs frequency
- tissue_displacement      — displacement at given SPL and frequency
- perception_threshold_model — ISO 2631-based whole-body perception
- concert_spl_spectrum     — literature-derived concert SPL spectra

References
----------
    Junger & Feit (2012) "Sound, Structures, and Their Interaction"
    ISO 2631-1:1997
    ISO 226:2003 (equal-loudness contours)
    Merchant et al. (2015) J. Acoust. Soc. Am. 137(3):1282-1292
    Todd & Cody (2000) Neurosci. Lett. 278(1-2):1-4
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Dict, Tuple

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)
from analytical.energy_budget import (
    radiation_damping_flexural,
    absorption_cross_section,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
RHO_AIR = 1.225          # kg/m³
C_AIR = 343.0            # m/s
P_REF = 20e-6            # Pa  (reference SPL)
RHO_TISSUE = 1040.0      # kg/m³
C_TISSUE = 1540.0        # m/s


# ---------------------------------------------------------------------------
# Core coupling model
# ---------------------------------------------------------------------------

def ka_parameter(f: float | np.ndarray, R_eq: float = 0.157,
                 c: float = C_AIR) -> float | np.ndarray:
    """Helmholtz number ka = 2π f R / c."""
    return 2 * np.pi * np.asarray(f) * R_eq / c


def airborne_coupling_ratio(
    f: float | np.ndarray,
    R_eq: float = 0.157,
    rho_air: float = RHO_AIR,
    c_air: float = C_AIR,
    rho_tissue: float = RHO_TISSUE,
    c_tissue: float = C_TISSUE,
    mode_n: int = 2,
) -> dict:
    """
    Ka-dependent airborne acoustic coupling as a function of frequency.

    For mode *n* of a fluid-filled shell in the long-wavelength limit the
    effective pressure driving the mode scales as (ka)^n.  The impedance
    mismatch between air and tissue further attenuates the coupling.

    Returns a dict with arrays over *f*:
        ka          — Helmholtz number
        p_ratio     — (ka)^n  pressure coupling factor
        Z_air       — acoustic impedance of air  [Pa·s/m]
        Z_tissue    — acoustic impedance of tissue  [Pa·s/m]
        impedance_transmission — 4 Z₁ Z₂ / (Z₁ + Z₂)²
        coupling_total — product of pressure coupling and impedance terms
    """
    f = np.atleast_1d(np.asarray(f, dtype=float))
    ka = ka_parameter(f, R_eq, c_air)

    # Acoustic coupling scales as (ka)^n
    p_ratio = ka ** mode_n

    # Impedance mismatch
    Z_air = rho_air * c_air
    Z_tissue = rho_tissue * c_tissue
    impedance_T = 4 * Z_air * Z_tissue / (Z_air + Z_tissue) ** 2

    coupling_total = p_ratio * impedance_T

    return {
        'frequency_hz': f,
        'ka': ka,
        'p_ratio': p_ratio,
        'Z_air': Z_air,
        'Z_tissue': Z_tissue,
        'impedance_transmission': impedance_T,
        'coupling_total': coupling_total,
    }


def tissue_displacement(
    f: float | np.ndarray,
    spl_db: float,
    R_eq: float = 0.157,
    model: Optional[AbdominalModelV2] = None,
    mode_n: int = 2,
) -> dict:
    """
    Tissue displacement at arbitrary frequency and SPL (energy-consistent).

    Uses the off-resonance forced-response of the modal oscillator.
    At the modal resonance the displacement matches Paper 1's canonical
    value; away from resonance it falls off via the SDOF transfer
    function H(r, ζ).

    Parameters
    ----------
    f : float or array
        Excitation frequency [Hz].
    spl_db : float
        Sound pressure level [dB re 20 μPa].
    R_eq : float
        Equivalent sphere radius [m].  Default: canonical 0.157 m.
    model : AbdominalModelV2, optional
        Shell model.  Uses canonical defaults if *None*.
    mode_n : int
        Dominant mode order.  Default 2 (n = 2 quadrupole).

    Returns
    -------
    dict with arrays over *f*:
        frequency_hz, ka, p_eff_Pa, H_transfer,
        xi_m, xi_um  (displacement in m and μm)
    """
    if model is None:
        model = AbdominalModelV2()

    f = np.atleast_1d(np.asarray(f, dtype=float))
    R = model.equivalent_sphere_radius

    # Incident pressure
    p_inc = P_REF * 10 ** (spl_db / 20)

    ka = ka_parameter(f, R, C_AIR)
    p_eff = p_inc * ka ** mode_n  # effective modal pressure

    # Modal parameters
    freqs = flexural_mode_frequencies_v2(model, n_max=mode_n)
    f_n = freqs[mode_n]
    omega_n = 2 * np.pi * f_n

    # Stiffness per unit area
    E, h, nu = model.E, model.h, model.nu
    D = model.D
    P_iap = model.P_iap
    n = mode_n

    K_bend = n * (n - 1) * (n + 2) ** 2 * D / R ** 4
    lam_n = (n ** 2 + n - 2 + 2 * nu) / (n ** 2 + n + 1 - nu)
    K_memb = E * h / R ** 2 * lam_n
    K_pre = P_iap / R * (n - 1) * (n + 2)
    K_total = K_bend + K_memb + K_pre

    # SDOF transfer function  H(r, ζ) = 1 / sqrt((1 - r²)² + (2ζr)²)
    zeta = model.damping_ratio
    r = f / f_n
    H = 1.0 / np.sqrt((1 - r ** 2) ** 2 + (2 * zeta * r) ** 2)

    # Static displacement (pressure / stiffness)
    xi_static = p_eff / K_total

    # Dynamic displacement with resonance amplification
    xi = xi_static * H

    return {
        'frequency_hz': f,
        'ka': ka,
        'p_inc_Pa': float(p_inc),
        'p_eff_Pa': p_eff,
        'f_resonance_hz': f_n,
        'K_total': K_total,
        'H_transfer': H,
        'zeta': zeta,
        'xi_m': xi,
        'xi_um': xi * 1e6,
    }


def _sum_modal_displacement(
    f: float | np.ndarray,
    spl_db: float,
    model: Optional[AbdominalModelV2] = None,
    n_max: int = 6,
) -> dict:
    """
    Sum displacement contributions from modes n = 2 … n_max.

    Higher-order modes have weaker coupling ((ka)^n) but higher
    resonance frequencies — closer to the sub-bass band.
    """
    if model is None:
        model = AbdominalModelV2()

    f = np.atleast_1d(np.asarray(f, dtype=float))
    xi_total = np.zeros_like(f)
    mode_contributions = {}

    for n in range(2, n_max + 1):
        result = tissue_displacement(f, spl_db, model=model, mode_n=n)
        mode_contributions[n] = result['xi_um'].copy()
        # Sum in quadrature (uncorrelated modes)
        xi_total = np.sqrt(xi_total ** 2 + result['xi_um'] ** 2)

    return {
        'frequency_hz': f,
        'xi_total_um': xi_total,
        'mode_contributions': mode_contributions,
    }


# ---------------------------------------------------------------------------
# Perception threshold model
# ---------------------------------------------------------------------------

# ISO 2631-1:1997, Table 1 — whole-body vibration perception thresholds
# (z-axis, standing/seated, r.m.s. acceleration)
# Values interpolated / extended to cover 1–100 Hz.
_ISO2631_PERCEPTION = np.array([
    #  f [Hz]   a_rms [m/s²]
    [1.0,    0.010],
    [2.0,    0.007],
    [4.0,    0.005],
    [8.0,    0.005],
    [10.0,   0.006],
    [12.5,   0.008],
    [16.0,   0.010],
    [20.0,   0.013],
    [25.0,   0.016],
    [31.5,   0.020],
    [40.0,   0.025],
    [50.0,   0.032],
    [63.0,   0.040],
    [80.0,   0.050],
])


def perception_threshold_model(
    f: float | np.ndarray,
) -> dict:
    """
    Whole-body vibration perception thresholds from ISO 2631-1.

    Returns the r.m.s. acceleration threshold [m/s²] and the
    corresponding displacement amplitude [m] at each frequency.

    Parameters
    ----------
    f : float or array
        Frequency [Hz].  Clamped to [1, 80] Hz.

    Returns
    -------
    dict with:
        frequency_hz, a_threshold_ms2, xi_threshold_m, xi_threshold_um
    """
    f = np.atleast_1d(np.asarray(f, dtype=float))
    f_clamp = np.clip(f, 1.0, 80.0)

    a_thresh = np.interp(
        f_clamp,
        _ISO2631_PERCEPTION[:, 0],
        _ISO2631_PERCEPTION[:, 1],
    )

    omega = 2 * np.pi * f_clamp
    # a_rms = ω² × x_peak / √2  →  x_peak = a_rms √2 / ω²
    xi_peak = a_thresh * np.sqrt(2) / omega ** 2

    return {
        'frequency_hz': f,
        'a_threshold_ms2': a_thresh,
        'xi_threshold_m': xi_peak,
        'xi_threshold_um': xi_peak * 1e6,
    }


# ---------------------------------------------------------------------------
# Concert SPL spectra
# ---------------------------------------------------------------------------

@dataclass
class ConcertSPLSpectrum:
    """Third-octave SPL spectrum for a concert genre."""
    genre: str
    centre_freqs_hz: np.ndarray
    spl_db: np.ndarray
    reference: str = ""


def _make_spectrum(genre: str, freqs: list, spls: list,
                   ref: str = "") -> ConcertSPLSpectrum:
    return ConcertSPLSpectrum(
        genre=genre,
        centre_freqs_hz=np.array(freqs, dtype=float),
        spl_db=np.array(spls, dtype=float),
        reference=ref,
    )


# Literature-derived third-octave concert spectra.
# Sources: Gunderson et al. (2016), Opperman et al. (2006),
# Bickerdike & Gregory (1966) — pipe organ measurements.
_CONCERT_SPECTRA: Dict[str, ConcertSPLSpectrum] = {}


def _init_spectra() -> None:
    """Populate concert spectra on first call."""
    if _CONCERT_SPECTRA:
        return

    # Rock concert — emphasis on kick drum & bass guitar (~40-100 Hz)
    # Broadband 100-110 dB, sub-bass peak ~105 dB at 63 Hz
    _CONCERT_SPECTRA['rock'] = _make_spectrum(
        'rock',
        [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200],
        [95, 98, 102, 105, 107, 108, 106, 104, 102, 100, 98],
        ref="Gunderson et al. (2016) JASA",
    )

    # EDM (electronic dance music) — very strong sub-bass 30-60 Hz
    # Sub-woofer-driven, peak SPL in 31.5-50 Hz band
    _CONCERT_SPECTRA['edm'] = _make_spectrum(
        'edm',
        [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200],
        [100, 105, 112, 115, 114, 110, 106, 102, 100, 98, 95],
        ref="Opperman et al. (2006) J. Laryngol. Otol.",
    )

    # Pipe organ — extreme infrasound extension, 16' and 32' pipes
    # 32' rank produces fundamental at 16 Hz
    _CONCERT_SPECTRA['organ'] = _make_spectrum(
        'organ',
        [16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200],
        [90, 95, 100, 104, 105, 103, 100, 97, 95, 93, 90, 88],
        ref="Bickerdike & Gregory (1966) J. Sound Vib.",
    )


def concert_spl_spectrum(
    f: float | np.ndarray,
    genre: str = 'edm',
) -> dict:
    """
    Interpolated concert SPL at arbitrary frequencies.

    Parameters
    ----------
    f : float or array
        Frequency [Hz].
    genre : {'rock', 'edm', 'organ'}
        Concert type.

    Returns
    -------
    dict with:
        frequency_hz, spl_db, genre, reference
    """
    _init_spectra()
    f = np.atleast_1d(np.asarray(f, dtype=float))

    if genre not in _CONCERT_SPECTRA:
        raise ValueError(
            f"Unknown genre '{genre}'. Choose from: "
            f"{list(_CONCERT_SPECTRA.keys())}"
        )

    spec = _CONCERT_SPECTRA[genre]
    spl = np.interp(f, spec.centre_freqs_hz, spec.spl_db)

    return {
        'frequency_hz': f,
        'spl_db': spl,
        'genre': genre,
        'reference': spec.reference,
    }


# ---------------------------------------------------------------------------
# Composite analysis — displacement at concert SPLs
# ---------------------------------------------------------------------------

def concert_displacement_spectrum(
    f: Optional[np.ndarray] = None,
    genre: str = 'edm',
    model: Optional[AbdominalModelV2] = None,
    mode_n: int = 2,
) -> dict:
    """
    Tissue displacement produced by a concert spectrum.

    Combines :func:`concert_spl_spectrum` with :func:`tissue_displacement`
    to compute the frequency-dependent displacement that a concertgoer's
    abdomen would experience from the airborne sound field alone.

    Parameters
    ----------
    f : ndarray, optional
        Frequencies [Hz].  Defaults to 20–80 Hz in 1 Hz steps.
    genre : str
        Concert genre for SPL spectrum.
    model : AbdominalModelV2, optional
        Shell model.
    mode_n : int
        Dominant mode order.

    Returns
    -------
    dict with arrays:
        frequency_hz, spl_db, ka, xi_um, perception_threshold_um,
        ratio_to_threshold
    """
    if model is None:
        model = AbdominalModelV2()
    if f is None:
        f = np.arange(20, 81, 1.0)

    f = np.atleast_1d(np.asarray(f, dtype=float))

    # Concert SPL at each frequency
    spec = concert_spl_spectrum(f, genre)
    spl = spec['spl_db']

    # Displacement at each frequency (using per-frequency SPL)
    xi_um = np.zeros_like(f)
    ka_arr = np.zeros_like(f)
    for i, (fi, spli) in enumerate(zip(f, spl)):
        result = tissue_displacement(np.array([fi]), float(spli),
                                     model=model, mode_n=mode_n)
        xi_um[i] = result['xi_um'][0]
        ka_arr[i] = result['ka'][0]

    # Perception threshold
    thresh = perception_threshold_model(f)

    return {
        'frequency_hz': f,
        'spl_db': spl,
        'genre': genre,
        'ka': ka_arr,
        'xi_um': xi_um,
        'perception_threshold_um': thresh['xi_threshold_um'],
        'ratio_to_threshold': xi_um / thresh['xi_threshold_um'],
    }


def coupling_transition_band(
    model: Optional[AbdominalModelV2] = None,
    spl_db: float = 115.0,
    threshold_fraction: float = 0.01,
) -> dict:
    """
    Identify the frequency band where airborne coupling becomes significant.

    Scans 1–100 Hz and finds where the coupling-induced displacement
    first exceeds *threshold_fraction* of the perception threshold.

    Parameters
    ----------
    model : AbdominalModelV2, optional
    spl_db : float
        Constant SPL across the band.
    threshold_fraction : float
        Fraction of perception threshold to use as "significant" criterion.

    Returns
    -------
    dict with:
        f_lower_hz, f_upper_hz  — edges of the transition band
        ka_lower, ka_upper
        peak_ratio — maximum ratio of displacement to perception threshold
        peak_freq_hz — frequency of peak ratio
    """
    if model is None:
        model = AbdominalModelV2()

    f = np.linspace(1, 100, 500)
    result = tissue_displacement(f, spl_db, model=model, mode_n=2)
    thresh = perception_threshold_model(f)

    ratio = result['xi_um'] / thresh['xi_threshold_um']

    above = np.where(ratio >= threshold_fraction)[0]
    if len(above) == 0:
        return {
            'f_lower_hz': None,
            'f_upper_hz': None,
            'ka_lower': None,
            'ka_upper': None,
            'peak_ratio': float(np.max(ratio)),
            'peak_freq_hz': float(f[np.argmax(ratio)]),
        }

    f_lower = float(f[above[0]])
    f_upper = float(f[above[-1]])
    ka_vals = ka_parameter(np.array([f_lower, f_upper]),
                           model.equivalent_sphere_radius)

    return {
        'f_lower_hz': f_lower,
        'f_upper_hz': f_upper,
        'ka_lower': float(ka_vals[0]),
        'ka_upper': float(ka_vals[1]),
        'peak_ratio': float(np.max(ratio)),
        'peak_freq_hz': float(f[np.argmax(ratio)]),
    }


# ---------------------------------------------------------------------------
# Quick-run summary
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')

    print()
    print("=" * 72)
    print("  BROWNTONE — Paper 6: Sub-Bass Coupling Analysis")
    print("=" * 72)
    print()

    model = AbdominalModelV2()
    R = model.equivalent_sphere_radius
    print(f"  Canonical model: R_eq = {R:.3f} m, "
          f"f₂ = {flexural_mode_frequencies_v2(model)[2]:.2f} Hz")
    print()

    # 1. ka transition
    print("  1. ka vs frequency")
    print("  " + "-" * 50)
    for freq in [4, 10, 20, 30, 40, 50, 60, 80]:
        kav = ka_parameter(freq, R)
        print(f"    f = {freq:4d} Hz  →  ka = {kav:.4f}")
    print()

    # 2. Coupling ratio
    print("  2. Coupling ratio (n=2)")
    print("  " + "-" * 50)
    for freq in [4, 20, 40, 60, 80]:
        cr = airborne_coupling_ratio(freq, R)
        print(f"    f = {freq:4d} Hz  →  (ka)² = {cr['p_ratio'][0]:.2e}, "
              f"total = {cr['coupling_total'][0]:.2e}")
    print()

    # 3. Displacement at 115 dB
    print("  3. Tissue displacement at 115 dB SPL")
    print("  " + "-" * 60)
    print(f"  {'f(Hz)':>6} {'ka':>8} {'ξ(μm)':>12} {'thresh(μm)':>12} {'ratio':>10}")
    freqs = np.array([20, 30, 40, 50, 60, 80])
    res = tissue_displacement(freqs, 115.0, model=model)
    thr = perception_threshold_model(freqs)
    for i, freq in enumerate(freqs):
        r = res['xi_um'][i] / thr['xi_threshold_um'][i]
        print(f"  {freq:6.0f} {res['ka'][i]:8.4f} "
              f"{res['xi_um'][i]:12.6f} {thr['xi_threshold_um'][i]:12.3f} "
              f"{r:10.2e}")
    print()

    # 4. Concert displacement
    print("  4. Concert displacement spectra")
    for genre in ['rock', 'edm', 'organ']:
        cd = concert_displacement_spectrum(freqs, genre, model)
        peak_i = np.argmax(cd['xi_um'])
        print(f"    {genre:5}: peak ξ = {cd['xi_um'][peak_i]:.6f} μm "
              f"at {cd['frequency_hz'][peak_i]:.0f} Hz "
              f"(SPL = {cd['spl_db'][peak_i]:.0f} dB)")
    print()

    # 5. Coupling transition band
    ctb = coupling_transition_band(model, spl_db=115.0)
    print("  5. Coupling transition band (at 115 dB)")
    print(f"    Peak ratio to threshold: {ctb['peak_ratio']:.2e} "
          f"at {ctb['peak_freq_hz']:.1f} Hz")
    if ctb['f_lower_hz'] is not None:
        print(f"    Band: {ctb['f_lower_hz']:.1f} – "
              f"{ctb['f_upper_hz']:.1f} Hz")
    else:
        print("    No frequency exceeds threshold criterion")
    print()
