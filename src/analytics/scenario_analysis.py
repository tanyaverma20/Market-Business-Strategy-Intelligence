"""Scenario analysis scaffolding that remains fail-closed without fabricated assumptions.

These templates are intentionally safe: they describe the scenario framework and
return a pending status when verified inputs are not available. No future market
assumptions are invented here.
"""

from __future__ import annotations

import pandas as pd


def build_scenario_analysis_template() -> pd.DataFrame:
    """Return a scenario template without claiming a forecasted market outcome."""
    return pd.DataFrame(
        [
            {
                "scenario": "Conservative",
                "market_assumption": "Lower adoption and delayed policy support",
                "input_status": "PENDING VERIFIED DATA",
                "base_value": None,
                "status": "PENDING VERIFIED DATA",
            },
            {
                "scenario": "Base case",
                "market_assumption": "Moderate adoption and policy continuation",
                "input_status": "PENDING VERIFIED DATA",
                "base_value": None,
                "status": "PENDING VERIFIED DATA",
            },
            {
                "scenario": "Upside",
                "market_assumption": "Higher adoption and strong policy / infrastructure support",
                "input_status": "PENDING VERIFIED DATA",
                "base_value": None,
                "status": "PENDING VERIFIED DATA",
            },
        ]
    )


__all__ = ["build_scenario_analysis_template"]
