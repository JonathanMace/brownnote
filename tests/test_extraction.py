"""Tests for post-processing extraction utilities."""

from __future__ import annotations

import numpy as np
import pytest

from browntone.postprocess.extraction import compute_richardson_extrapolation


class TestRichardsonExtrapolation:
    """Tests for Richardson extrapolation."""

    def test_quadratic_convergence(self) -> None:
        """Should recover the exact value for a known quadratic convergence case."""
        # Simulate f(h) = f_exact + C * h^2
        f_exact = 10.0
        C = 100.0
        h_values = np.array([0.04, 0.02, 0.01])
        qoi_values = f_exact + C * h_values**2

        result = compute_richardson_extrapolation(h_values, qoi_values)

        assert result["extrapolated_value"] == pytest.approx(f_exact, rel=1e-6)
        assert result["observed_order"] == pytest.approx(2.0, rel=0.1)
        assert result["gci_fine"] >= 0

    def test_too_few_points_raises(self) -> None:
        """Should raise ValueError with fewer than 3 data points."""
        with pytest.raises(ValueError, match="at least 3"):
            compute_richardson_extrapolation(
                np.array([0.02, 0.01]),
                np.array([10.1, 10.05]),
            )
