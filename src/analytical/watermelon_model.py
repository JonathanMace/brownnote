"""
Non-destructive acoustic assessment of watermelon ripeness via shell
resonance inversion.

Reuses the equivalent-sphere shell framework (AbdominalModelV2) with
watermelon-specific parameters.  The oblate geometry is captured through
the equivalent-volume radius R_eq = (a²c)^(1/3); the frequency model is
that of a spherical shell of radius R_eq and has no explicit
aspect-ratio (ζ) dependence beyond R_eq.  Provides:

  1. Forward model  -- equivalent-sphere shell theory -> predicted tap-tone frequency
  2. Closed-form inverse -- measured frequency -> rind elastic modulus
  3. Universal dimensionless geometric invariant (collapses cultivar geometries)
  4. Validation hooks for Yamamoto et al. (1980) published frequency data

Paper 7 of the Browntone research programme.

References:
    - Sadrnia, H. et al. (2006) "Predicting quality attributes of
      watermelons by acoustics", Int. J. Food Prop.
    - De Belie, N. et al. (2000) "Principal component analysis of
      non-destructive firmness measurements of watermelon", Postharvest
      Biol. Technol.
    - Mao, J. et al. (2016) "Firmness measurement of watermelons based
      on vibrational characteristics"
"""

import sys
import os
import warnings

import numpy as np

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from analytical.natural_frequency_v2 import (
    AbdominalModelV2,
    flexural_mode_frequencies_v2,
)

# ---------------------------------------------------------------------------
# Sobol / SALib (optional — graceful degradation)
# ---------------------------------------------------------------------------
try:
    from SALib.sample import sobol as _saltelli_mod
except ImportError:
    try:
        from SALib.sample import saltelli as _saltelli_mod
    except ImportError:
        _saltelli_mod = None

try:
    from SALib.analyze import sobol as _sobol_analyze
except ImportError:
    _sobol_analyze = None


# ═══════════════════════════════════════════════════════════════════════════
#  Canonical watermelon parameters
# ═══════════════════════════════════════════════════════════════════════════

# Ripening stage → parameter dict.
# Sources: Sadrnia et al. (2006), De Belie et al. (2000), web compilations.
_RIPENESS_STAGES = {
    "unripe": {
        "a": 0.158,               # semi-major axis [m]
        "c": 0.123,               # semi-minor axis [m]
        "h": 0.020,               # rind thickness [m]
        "E": 200.0e6,             # 200 MPa — stiff green rind
        "nu": 0.40,               # Poisson's ratio
        "rho_rind": 1050.0,       # rind density [kg/m³]
        "rho_flesh": 970.0,       # flesh density [kg/m³]
        "K_flesh": 2.2e9,         # flesh bulk modulus [Pa]
        "P_int": 200.0,           # turgor pressure [Pa]
        "loss_tangent": 0.08,     # loss tangent
    },
    "turning": {
        "a": 0.158,
        "c": 0.123,
        "h": 0.017,
        "E": 120.0e6,             # 120 MPa — beginning to soften
        "nu": 0.40,
        "rho_rind": 1050.0,
        "rho_flesh": 960.0,
        "K_flesh": 2.2e9,
        "P_int": 350.0,
        "loss_tangent": 0.11,
    },
    "ripe": {
        "a": 0.158,
        "c": 0.123,
        "h": 0.015,
        "E": 50.0e6,              # 50 MPa — optimal ripeness
        "nu": 0.40,
        "rho_rind": 1050.0,
        "rho_flesh": 950.0,
        "K_flesh": 2.2e9,
        "P_int": 500.0,
        "loss_tangent": 0.15,
    },
    "overripe": {
        "a": 0.158,
        "c": 0.123,
        "h": 0.013,
        "E": 15.0e6,              # 15 MPa — degraded pectin
        "nu": 0.40,
        "rho_rind": 1050.0,
        "rho_flesh": 940.0,
        "K_flesh": 2.2e9,
        "P_int": 600.0,
        "loss_tangent": 0.20,
    },
}

# Cultivar geometry database (semi-major a, semi-minor c, rind thickness h)
_CULTIVAR_DB = {
    "Crimson Sweet": {"a": 0.158, "c": 0.123, "h": 0.015},
    "Sugar Baby":    {"a": 0.100, "c": 0.095, "h": 0.012},
    "Charleston Gray": {"a": 0.200, "c": 0.110, "h": 0.018},
    "Seedless (Tri-X 313)": {"a": 0.140, "c": 0.120, "h": 0.014},
}


# ═══════════════════════════════════════════════════════════════════════════
#  Helper: build AbdominalModelV2 from watermelon parameters
# ═══════════════════════════════════════════════════════════════════════════

def _build_model(params: dict) -> AbdominalModelV2:
    """Construct an AbdominalModelV2 from a watermelon parameter dict."""
    return AbdominalModelV2(
        a=params["a"],
        b=params["a"],          # oblate: b = a
        c=params["c"],
        h=params["h"],
        E=params["E"],
        nu=params["nu"],
        rho_wall=params["rho_rind"],
        rho_fluid=params["rho_flesh"],
        K_fluid=params["K_flesh"],
        P_iap=params["P_int"],
        loss_tangent=params["loss_tangent"],
    )


# ═══════════════════════════════════════════════════════════════════════════
#  Public API
# ═══════════════════════════════════════════════════════════════════════════

def watermelon_canonical_params(ripeness: str = "ripe") -> dict:
    """Return canonical parameter dict for a watermelon at a given ripeness.

    Parameters
    ----------
    ripeness : str
        One of ``'unripe'``, ``'turning'``, ``'ripe'``, ``'overripe'``.

    Returns
    -------
    dict
        Deep copy of the canonical parameter set for the stage.
    """
    key = ripeness.lower().strip()
    if key not in _RIPENESS_STAGES:
        raise ValueError(
            f"Unknown ripeness stage '{ripeness}'. "
            f"Choose from {list(_RIPENESS_STAGES)}"
        )
    return dict(_RIPENESS_STAGES[key])


def predict_tap_tone(params: dict | None = None, mode: int = 2) -> dict:
    """Predict the tap-tone frequency for a watermelon.

    Parameters
    ----------
    params : dict or None
        Watermelon parameter dict (as from :func:`watermelon_canonical_params`).
        If *None*, uses canonical ripe parameters.
    mode : int
        Flexural mode number (default 2, the lowest non-trivial mode).

    Returns
    -------
    dict
        ``f_n`` — undamped natural frequency [Hz]
        ``Q`` — quality factor
        ``f_damped`` — damped natural frequency [Hz]
        ``zeta`` — damping ratio
    """
    if params is None:
        params = watermelon_canonical_params("ripe")

    model = _build_model(params)
    freqs = flexural_mode_frequencies_v2(model, n_max=max(mode, 2))
    f_n = freqs[mode]

    eta = params.get("loss_tangent", 0.15)
    zeta = eta / 2.0
    Q = 1.0 / (2.0 * zeta) if zeta > 0 else float("inf")
    f_damped = f_n * np.sqrt(max(0, 1 - zeta**2))

    return {"f_n": f_n, "Q": Q, "f_damped": f_damped, "zeta": zeta}


def invert_frequency_to_modulus(
    f_measured: float,
    a: float,
    c: float,
    h: float,
    rho_rind: float,
    rho_flesh: float,
    nu: float = 0.40,
    P_int: float = 500.0,
    n: int = 2,
) -> float:
    """Closed-form inversion: measured tap-tone → rind elastic modulus.

    Starting from the flexural frequency equation

        ω² = (K_bend + K_memb + K_prestress) / m_eff

    and noting that K_bend ∝ E and K_memb ∝ E while K_prestress ∝ P,
    we isolate E algebraically:

        E = (ω² · m_eff − K_prestress) / (K_bend_coeff + K_memb_coeff)

    where the ``_coeff`` quantities are the geometric pre-factors of E.

    Parameters
    ----------
    f_measured : float
        Measured resonant frequency [Hz].
    a, c, h : float
        Geometry [m].
    rho_rind, rho_flesh : float
        Densities [kg/m³].
    nu : float
        Poisson's ratio (default 0.40).
    P_int : float
        Internal turgor pressure [Pa].
    n : int
        Flexural mode number (default 2).

    Returns
    -------
    float
        Inferred rind elastic modulus E_rind [Pa].

    Notes
    -----
    The condition number of this inversion with respect to f-squared is
    unity (the mapping E -> f-squared is linear). The practical condition
    number with respect to measured frequency f is approximately 2, since
    E proportional to f-squared implies dE/E ~ 2*df/f.
    """
    R = (a * a * c) ** (1.0 / 3.0)
    omega = 2.0 * np.pi * f_measured

    # Effective mass per unit area
    m_eff = rho_rind * h + rho_flesh * R / n

    # Pre-stress stiffness (independent of E)
    K_prestress = P_int / R * (n - 1) * (n + 2)

    # Bending stiffness coefficient: K_bend = coeff_bend * E
    coeff_bend = n * (n - 1) * (n + 2) ** 2 * h ** 3 / (
        12 * (1 - nu ** 2) * R ** 4
    )

    # Membrane stiffness coefficient: K_memb = coeff_memb * E
    lambda_n = (n ** 2 + n - 2 + 2 * nu) / (n ** 2 + n + 1 - nu)
    coeff_memb = h / R ** 2 * lambda_n

    # Solve for E
    E = (omega ** 2 * m_eff - K_prestress) / (coeff_bend + coeff_memb)
    return float(E)


def ripeness_from_modulus(E_rind: float) -> tuple[str, float]:
    """Map rind elastic modulus to ripeness category.

    Thresholds based on literature correlations between E and sensory
    assessment (Sadrnia et al. 2006, De Belie et al. 2000).

    Parameters
    ----------
    E_rind : float
        Young's modulus in Pa.

    Returns
    -------
    (category, confidence)
        ``category`` is one of ``'unripe'``, ``'turning'``, ``'ripe'``,
        ``'overripe'``.
        ``confidence`` ∈ [0, 1] indicates proximity to the category centre.
    """
    E_MPa = E_rind / 1e6

    # Boundaries (MPa): overripe < 25 < ripe < 80 < turning < 160 < unripe
    thresholds = [
        ("overripe", 0.0,  25.0),
        ("ripe",    25.0,  80.0),
        ("turning", 80.0, 160.0),
        ("unripe", 160.0, 400.0),
    ]
    centres = {"overripe": 15.0, "ripe": 50.0, "turning": 120.0, "unripe": 200.0}

    for cat, lo, hi in thresholds:
        if lo <= E_MPa < hi:
            half_width = (hi - lo) / 2.0
            centre = (lo + hi) / 2.0
            dist = abs(E_MPa - centre) / half_width
            confidence = max(0.0, 1.0 - dist)
            return cat, round(confidence, 3)

    # Extrapolations
    if E_MPa < 0:
        return "overripe", 0.1
    return "unripe", 0.5


def universal_ripeness_curve(params_list: list[dict]) -> list[tuple[float, float]]:
    """Compute dimensionless geometric invariant Pi_ripe.

    Because f2-squared is proportional to E_rind, the elastic modulus
    cancels, making Pi_ripe invariant w.r.t. E at FIXED GEOMETRY.
    It is a geometric invariant that collapses different cultivar
    geometries onto a single calibration constant.  Note: Pi_ripe is
    NOT invariant across ripeness stages if geometry (especially h)
    also changes with ripening.

    Parameters
    ----------
    params_list : list of dict
        Each dict is a watermelon parameter set.

    Returns
    -------
    list of (Pi_ripe, ka)
        Pi_ripe is the dimensionless geometric invariant.
        ka is the Helmholtz number at f2 in air (c_air = 343 m/s).
    """
    c_air = 343.0
    results = []
    for p in params_list:
        model = _build_model(p)
        R_eq = model.equivalent_sphere_radius
        freqs = flexural_mode_frequencies_v2(model, n_max=2)
        f2 = freqs[2]

        rho_eff = p["rho_rind"] * p["h"] / R_eq + p["rho_flesh"]
        Pi_ripe = f2 * R_eq * np.sqrt(rho_eff / p["E"])
        ka = 2 * np.pi * f2 * R_eq / c_air
        results.append((float(Pi_ripe), float(ka)))
    return results


def parametric_ripening_sweep(n_stages: int = 20) -> list[dict]:
    """Sweep from very unripe (E=250 MPa) to overripe (E=10 MPa).

    Also varies rind thickness *h* (thins during ripening) and loss tangent
    *η* (increases).

    Parameters
    ----------
    n_stages : int
        Number of ripening stages to simulate.

    Returns
    -------
    list of dict
        Each entry has keys: ``stage``, ``E_rind``, ``h``, ``eta``, ``f2``,
        ``Q``, ``category``.
    """
    E_vals = np.linspace(250.0e6, 10.0e6, n_stages)
    h_vals = np.linspace(0.022, 0.012, n_stages)
    eta_vals = np.linspace(0.06, 0.22, n_stages)

    base = watermelon_canonical_params("ripe")
    rows = []

    for i in range(n_stages):
        p = dict(base)
        p["E"] = float(E_vals[i])
        p["h"] = float(h_vals[i])
        p["loss_tangent"] = float(eta_vals[i])

        res = predict_tap_tone(p, mode=2)
        cat, _ = ripeness_from_modulus(p["E"])
        rows.append({
            "stage": i,
            "E_rind": p["E"],
            "h": p["h"],
            "eta": p["loss_tangent"],
            "f2": res["f_n"],
            "Q": res["Q"],
            "category": cat,
        })
    return rows


def _yamamoto_reference_data() -> list[dict]:
    """Published frequency ranges from Yamamoto et al. (1980)."""
    return [
        {"description": "Small, ripe",    "a": 0.110, "c": 0.100, "h": 0.013,
         "E": 50.0e6,  "f_lo": 80.0,  "f_hi": 120.0},
        {"description": "Medium, ripe",   "a": 0.140, "c": 0.120, "h": 0.015,
         "E": 50.0e6,  "f_lo": 80.0,  "f_hi": 120.0},
        {"description": "Large, ripe",    "a": 0.170, "c": 0.140, "h": 0.017,
         "E": 50.0e6,  "f_lo": 80.0,  "f_hi": 120.0},
        {"description": "Small, unripe",  "a": 0.110, "c": 0.100, "h": 0.015,
         "E": 150.0e6, "f_lo": 120.0, "f_hi": 180.0},
        {"description": "Medium, unripe", "a": 0.140, "c": 0.120, "h": 0.018,
         "E": 150.0e6, "f_lo": 120.0, "f_hi": 180.0},
        {"description": "Large, unripe",  "a": 0.170, "c": 0.140, "h": 0.020,
         "E": 150.0e6, "f_lo": 120.0, "f_hi": 180.0},
    ]


def validate_against_yamamoto() -> dict:
    """Benchmark model predictions against Yamamoto et al. (1980) data."""
    ref = _yamamoto_reference_data()
    base = watermelon_canonical_params("ripe")
    cases = []
    for entry in ref:
        p = dict(base)
        p["a"] = entry["a"]; p["c"] = entry["c"]
        p["h"] = entry["h"]; p["E"] = entry["E"]
        res = predict_tap_tone(p, mode=2)
        f_pred = res["f_n"]
        within = entry["f_lo"] <= f_pred <= entry["f_hi"]
        if f_pred < entry["f_lo"]:
            deviation = entry["f_lo"] - f_pred
        elif f_pred > entry["f_hi"]:
            deviation = f_pred - entry["f_hi"]
        else:
            deviation = 0.0
        cases.append({
            "description": entry["description"],
            "f_predicted": float(f_pred),
            "f_lo": entry["f_lo"], "f_hi": entry["f_hi"],
            "within_range": within,
            "deviation_Hz": float(deviation),
        })
    n_within = sum(1 for c in cases if c["within_range"])
    devs = [c["deviation_Hz"] for c in cases]
    return {
        "n_cases": len(cases),
        "n_within_range": n_within,
        "fraction_within": n_within / len(cases),
        "mean_abs_deviation": float(np.mean(devs)),
        "cases": cases,
    }


def validate_against_debelie(model_predictions=None) -> dict:
    """Deprecated. Use validate_against_yamamoto() instead."""
    warnings.warn(
        "validate_against_debelie() is deprecated; use validate_against_yamamoto()",
        DeprecationWarning,
        stacklevel=2,
    )
    return validate_against_yamamoto()


def sobol_sensitivity_watermelon(N_base: int = 2048, seed: int | None = None) -> dict:
    """Sobol sensitivity analysis for watermelon f2.

    Uses calc_second_order=False: total evaluations = N_base*(D+2).
    """
    if _saltelli_mod is None or _sobol_analyze is None:
        raise ImportError("SALib is required for Sobol analysis")
    param_names = [
        "E", "h", "a", "c",
        "rho_rind", "rho_flesh", "nu", "P_int", "loss_tangent",
    ]
    bounds_phys = {
        "E": (10.0e6, 250.0e6), "h": (0.010, 0.025),
        "a": (0.090, 0.220), "c": (0.080, 0.160),
        "rho_rind": (1000.0, 1100.0), "rho_flesh": (920.0, 990.0),
        "nu": (0.35, 0.45), "P_int": (100.0, 800.0),
        "loss_tangent": (0.05, 0.25),
    }
    problem = {
        "num_vars": len(param_names),
        "names": param_names,
        "bounds": [list(bounds_phys[n]) for n in param_names],
    }
    sample_kwargs: dict = {"calc_second_order": False}
    if seed is not None:
        sample_kwargs["seed"] = seed
    X = _saltelli_mod.sample(problem, N_base, **sample_kwargs)
    Y = np.empty(X.shape[0])
    for i in range(X.shape[0]):
        p = watermelon_canonical_params("ripe")
        for j, name in enumerate(param_names):
            p[name] = X[i, j]
        try:
            res = predict_tap_tone(p, mode=2)
            Y[i] = res["f_n"]
        except Exception:
            Y[i] = np.nan
    median_val = np.nanmedian(Y)
    Y[~np.isfinite(Y)] = median_val
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Si = _sobol_analyze.analyze(problem, Y, calc_second_order=False)
    S1 = {name: float(Si["S1"][j]) for j, name in enumerate(param_names)}
    ST = {name: float(Si["ST"][j]) for j, name in enumerate(param_names)}
    S1_conf = {name: float(Si["S1_conf"][j]) for j, name in enumerate(param_names)}
    ST_conf = {name: float(Si["ST_conf"][j]) for j, name in enumerate(param_names)}
    return {"S1": S1, "ST": ST, "S1_conf": S1_conf, "ST_conf": ST_conf, "n_evaluations": X.shape[0]}


def multi_cultivar_comparison() -> list[dict]:
    """Compare tap-tone predictions across watermelon cultivars.

    Uses geometry from the cultivar database and canonical ripe E_rind.

    Returns
    -------
    list of dict
        Each entry: ``cultivar``, ``a``, ``c``, ``h``, ``R_eq``, ``f2``,
        ``Pi_ripe``.
    """
    base = watermelon_canonical_params("ripe")
    rows = []
    for name, geom in _CULTIVAR_DB.items():
        p = dict(base)
        p.update(geom)
        model = _build_model(p)
        R_eq = model.equivalent_sphere_radius
        res = predict_tap_tone(p, mode=2)

        rho_eff = p["rho_rind"] * p["h"] / R_eq + p["rho_flesh"]
        Pi_ripe = res["f_n"] * R_eq * np.sqrt(rho_eff / p["E"])

        rows.append({
            "cultivar": name,
            "a": geom["a"],
            "c": geom["c"],
            "h": geom["h"],
            "R_eq": R_eq,
            "f2": res["f_n"],
            "Pi_ripe": Pi_ripe,
        })
    return rows
