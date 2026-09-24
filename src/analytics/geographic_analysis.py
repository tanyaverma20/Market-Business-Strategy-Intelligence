"""Geographic Attractiveness Index (GAI) framework.

Two computation modes:
1. compute_gai_template() - legacy 6-factor compatibility mode
2. compute_gai_scores()   - 5-factor official GAI model with fail-closed governance

GOVERNANCE: States with any missing required input return data_quality_status=INCOMPLETE
and receive no rank. Fail-closed behaviour is preserved.
"""
from __future__ import annotations
import pandas as pd

GAI_WEIGHTS = {
    "registration_volume_score": 0.30,
    "per_capita_income_score": 0.25,
    "two_w_density_score": 0.20,
    "ev_policy_score": 0.15,
    "urbanization_score": 0.10,
}

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
    mn, mx = series.min(), series.max()
    if pd.isna(mn) or pd.isna(mx) or mx == mn:
        return pd.Series(0.0, index=series.index)
    return (series - mn) / (mx - mn) * 100


def compute_gai_template(df: pd.DataFrame, weights: dict | None = None) -> pd.DataFrame:
    weights = weights or DEFAULT_GAI_WEIGHTS
    required = {"state","market_size","ev_penetration","growth",
                "purchasing_power","charging_infrastructure","policy_score"}
    if not required.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"],
                             "message": ["Verified state indicators required for GAI scoring."]})
    out = df.copy()
    norm = {k: _safe_normalize(out[k]) for k in weights}
    out["weighted_score"] = sum(norm[k] * w for k, w in weights.items())
    out["gai_score"] = out["weighted_score"].round(2)
    out["priority_tier"] = pd.cut(out["gai_score"],
        bins=[-1,39.99,59.99,79.99,101],
        labels=["Low Priority","Watch","Medium Priority","High Priority"], right=False)
    out["metric_type"] = "derived"
    out["weight_configuration"] = str(weights)
    return out[["state","market_size","ev_penetration","growth","purchasing_power",
                "charging_infrastructure","policy_score","gai_score","priority_tier",
                "metric_type","weight_configuration"]]


def compute_gai_scores(df: pd.DataFrame, weights: dict | None = None) -> pd.DataFrame:
    """
    Compute GAI scores for all states using the 5-factor weighted model.
    Fail-closed: states with any missing input receive no score or rank.
    """
    weights = weights or GAI_WEIGHTS
    required = list(weights.keys()) + ["state"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        return pd.DataFrame({"status": ["INCOMPLETE"],
                             "message": [f"Missing required columns: {missing}"]})
    out = df.copy()
    norm = {f: _safe_normalize(out[f]) for f in weights}
    has_null = pd.Series(False, index=out.index)
    for f in weights:
        has_null |= out[f].isna()
    out["gai_score"] = sum(norm[f] * w for f, w in weights.items())
    out["gai_score"] = out["gai_score"].round(2)
    out.loc[has_null, "gai_score"] = None
    out["data_quality_status"] = "COMPLETE"
    out.loc[has_null, "data_quality_status"] = "INCOMPLETE - Missing inputs: fail-closed"
    complete_mask = out["data_quality_status"] == "COMPLETE"
    out["gai_rank"] = None
    if complete_mask.any():
        out.loc[complete_mask, "gai_rank"] = (
            out.loc[complete_mask, "gai_score"].rank(ascending=False, method="dense").astype(int)
        )
    out["priority_tier"] = pd.cut(out["gai_score"],
        bins=[-1,39.99,59.99,79.99,101],
        labels=["Low Priority","Watch","Medium Priority","High Priority"], right=False)
    for f in weights:
        out[f"{f}_normalized"] = norm[f]
    out["weight_config"] = str(weights)
    out["methodology_version"] = "v2.0 - 2026-09-24"
    cols = (["state","gai_score","gai_rank","priority_tier","data_quality_status"]
            + list(weights.keys())
            + [f"{f}_normalized" for f in weights]
            + ["weight_config","methodology_version"])
    return out[[c for c in cols if c in out.columns]]
