"""Geographic Attractiveness Index (GAI) framework.

The current repo does not contain verified state indicators; therefore this module
returns a configuration template and valid scoring structure rather than factual rankings.
"""

from __future__ import annotations

import pandas as pd

DEFAULT_GAI_WEIGHTS = {
    "market_size": 0.25,
    "ev_penetration": 0.20,
    "growth": 0.20,
    "purchasing_power": 0.15,
    "policy_score": 0.10,
    "charging_infrastructure": 0.10,
}


def _safe_normalize(series: pd.Series) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce")
    min_val = series.min()
    max_val = series.max()
    if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
        return pd.Series(0, index=series.index)
    return (series - min_val) / (max_val - min_val) * 100


def compute_gai_template(df: pd.DataFrame, weights: dict | None = None) -> pd.DataFrame:
    weights = weights or DEFAULT_GAI_WEIGHTS
    required = {"state", "market_size", "ev_penetration", "growth", "purchasing_power", "charging_infrastructure", "policy_score"}
    if not required.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified state indicators required for GAI scoring."]})
    out = df.copy()
    normalized = pd.DataFrame()
    for key, _ in weights.items():
        normalized[key] = _safe_normalize(out[key])
    out["weighted_score"] = sum(normalized[key] * weight for key, weight in weights.items())
    out["gai_score"] = out["weighted_score"].round(2)
    out["priority_tier"] = pd.cut(
        out["gai_score"],
        bins=[-1, 39.99, 59.99, 79.99, 101],
        labels=["Low Priority", "Watch", "Medium Priority", "High Priority"],
        right=False,
    )
    out["metric_type"] = "derived"
    out["weight_configuration"] = str(weights)
    return out[["state", "market_size", "ev_penetration", "growth", "purchasing_power", "charging_infrastructure", "policy_score", "gai_score", "priority_tier", "metric_type", "weight_configuration"]]
