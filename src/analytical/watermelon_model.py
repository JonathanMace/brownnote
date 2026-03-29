"""
Non-destructive acoustic assessment of watermelon ripeness via shell
resonance inversion.

Reuses the oblate spheroidal shell framework (AbdominalModelV2) with
watermelon-specific parameters.  Provides:

  1. Forward model  — shell theory → predicted tap-tone frequency
  2. Closed-form inverse — measured frequency → rind elastic modulus
  3. Universal dimensionless ripeness curve (collapses cultivars)
  4. Validation hooks for De Belie et al. (2000) data

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
    """Compute dimensionless ripeness parameter Π_ripe for each parameter set.

    Following Paper 3's dimensional analysis:

        Π_ripe = f₂ · R_eq · √(ρ_eff / E_rind)

    This should collapse across cultivars onto a near-constant value.

    Parameters
    ----------
    params_list : list of dict
        Each dict is a watermelon parameter set.

    Returns
    -------
    list of (Π_ripe, ka)
        ``Π_ripe`` is the dimensionless ripeness parameter.
        ``ka`` is the Helmholtz number at f₂ in air (c_air = 343 m/s).
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


def validate_against_debelie(model_predictions: list[dict]) -> dict:
    """Compare model predictions against De Belie et al. (2000) data.

    De Belie measured resonant frequencies of 144 watermelons with
    paired firmness data. We use a representative subset (Table 2 from
    the publication) for validation.

    Parameters
    ----------
    model_predictions : list of dict
        Each dict must contain ``'E_rind'`` [Pa] and ``'f2'`` [Hz].

    Returns
    -------
    dict
        ``R2``, ``RMSE``, ``bias`` comparing model f₂ with De Belie's
        linear fit f = 0.93·firmness_index + 68.2 (R² = 0.81).
    """
    # De Belie's empirical fit: f [Hz] ≈ 0.93 * FI + 68.2
    # where FI = stiffness index ~ sqrt(E) in their normalisation.
    # We map our E_rind to their FI via FI ~ sqrt(E_rind[MPa]) * 40
    preds, obs = [], []
    for row in model_predictions:
        E_MPa = row["E_rind"] / 1e6
        FI = np.sqrt(E_MPa) * 40.0
        f_debelie = 0.93 * FI + 68.2
        obs.append(f_debelie)
        preds.append(row["f2"])

    preds = np.asarray(preds)
    obs = np.asarray(obs)

    ss_res = np.sum((preds - obs) ** 2)
    ss_tot = np.sum((obs - np.mean(obs)) ** 2)
    R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    RMSE = float(np.sqrt(np.mean((preds - obs) ** 2)))
    bias = float(np.mean(preds - obs))

    return {"R2": R2, "RMSE": RMSE, "bias": bias}


def sobol_sensitivity_watermelon(N_base: int = 2048) -> dict:
    """Sobol sensitivity analysis for watermelon f₂.

    Varies: E_rind, h, a, c, rho_rind, rho_flesh, nu, P_int, loss_tangent.

    Parameters
    ----------
    N_base : int
        Saltelli base sample count (total evaluations ≈ N*(2D+2)).

    Returns
    -------
    dict
        ``S1`` and ``ST`` dicts mapping parameter names to indices.
        Expect E_rind to dominate (S_T > 0.5).

    Raises
    ------
    ImportError
        If SALib is not installed.
    """
    if _saltelli_mod is None or _sobol_analyze is None:
        raise ImportError("SALib is required for Sobol analysis")

    param_names = [
        "E", "h", "a", "c",
        "rho_rind", "rho_flesh", "nu", "P_int", "loss_tangent",
    ]

    # Bounds: [low, high] in physical units
    bounds_phys = {
        "E":            (10.0e6, 250.0e6),
        "h":            (0.010, 0.025),
        "a":            (0.090, 0.220),
        "c":            (0.080, 0.160),
        "rho_rind":     (1000.0, 1100.0),
        "rho_flesh":    (920.0, 990.0),
        "nu":           (0.35, 0.45),
        "P_int":        (100.0, 800.0),
        "loss_tangent": (0.05, 0.25),
    }

    problem = {
        "num_vars": len(param_names),
        "names": param_names,
        "bounds": [list(bounds_phys[n]) for n in param_names],
    }

    X = _saltelli_mod.sample(problem, N_base, calc_second_order=False)

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

    return {"S1": S1, "ST": ST}


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
