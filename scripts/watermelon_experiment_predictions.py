"""Generate simple prediction tables and plots for the watermelon experiment."""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


STAGES = ("unripe", "turning", "ripe", "overripe")
SIZE_FACTORS = {
    "small": 0.85,
    "medium": 1.00,
    "large": 1.15,
}


def scaled_stage_params(stage: str, size_factor: float) -> dict:
    """Return stage parameters with geometry scaled at fixed aspect ratio."""
    from analytical.watermelon_model import watermelon_canonical_params

    params = watermelon_canonical_params(stage)
    for key in ("a", "c", "h"):
        params[key] *= size_factor
    return params


def build_prediction_rows() -> list[dict]:
    """Build a discrete prediction table for small/medium/large melons."""
    from analytical.watermelon_model import predict_tap_tone

    rows: list[dict] = []
    for size_name, size_factor in SIZE_FACTORS.items():
        for stage in STAGES:
            params = scaled_stage_params(stage, size_factor)
            result = predict_tap_tone(params, mode=2)
            rows.append(
                {
                    "size": size_name,
                    "stage": stage,
                    "size_factor": size_factor,
                    "a_mm": params["a"] * 1000,
                    "c_mm": params["c"] * 1000,
                    "h_mm": params["h"] * 1000,
                    "E_MPa": params["E"] / 1e6,
                    "f2_Hz": result["f_n"],
                    "Q": result["Q"],
                }
            )
    return rows


def print_prediction_table(rows: list[dict]) -> None:
    """Print a compact comparison table."""
    header = (
        f"{'size':<8} {'stage':<10} {'a [mm]':>8} {'c [mm]':>8} "
        f"{'h [mm]':>8} {'E [MPa]':>8} {'f2 [Hz]':>10} {'Q':>6}"
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row['size']:<8} {row['stage']:<10} "
            f"{row['a_mm']:8.1f} {row['c_mm']:8.1f} {row['h_mm']:8.1f} "
            f"{row['E_MPa']:8.1f} {row['f2_Hz']:10.1f} {row['Q']:6.2f}"
        )


def make_plot(rows: list[dict], output_path: str | None) -> None:
    """Plot expected frequency versus ripeness stage for several melon sizes."""
    x = np.arange(len(STAGES))

    fig, ax = plt.subplots(figsize=(8, 4.8))
    colors = {
        "small": "#4477AA",
        "medium": "#228833",
        "large": "#CCBB44",
    }
    markers = {
        "small": "o",
        "medium": "s",
        "large": "^",
    }

    for size_name in SIZE_FACTORS:
        size_rows = [row for row in rows if row["size"] == size_name]
        frequencies = [row["f2_Hz"] for row in size_rows]
        ax.plot(
            x,
            frequencies,
            marker=markers[size_name],
            linewidth=2.0,
            markersize=7,
            label=f"{size_name.capitalize()} melon",
            color=colors[size_name],
        )

    ax.set_xticks(x)
    ax.set_xticklabels([stage.capitalize() for stage in STAGES])
    ax.set_ylabel("Predicted n=2 resonance frequency [Hz]")
    ax.set_xlabel("Ripeness stage")
    ax.set_title("Paper 7 prediction: resonance frequency drops with ripeness")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    fig.tight_layout()

    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        fig.savefig(output_path, dpi=200, bbox_inches="tight")
        print(f"\nSaved plot to: {output_path}")
    else:
        print(
            "\nNo plot file written. Re-run with "
            "--output <path> to save the figure."
        )

    plt.close(fig)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate predicted Paper 7 resonance frequencies for a range of "
            "watermelon sizes and ripeness stages."
        )
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Optional path for the PNG figure, e.g. "
            "docs/experimental-protocols/watermelon-frequency-vs-ripeness.png"
        ),
    )
    return parser.parse_args()


def main() -> None:
    """Run the prediction utility."""
    args = parse_args()
    rows = build_prediction_rows()
    print_prediction_table(rows)
    make_plot(rows, args.output)


if __name__ == "__main__":
    main()
