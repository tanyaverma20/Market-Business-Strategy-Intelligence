"""Safe strategic and competitive scoring framework.

This module does not invent market or strategic recommendations. When required
verified inputs are absent, the functions return a template with a clear pending
status instead of reporting fabricated scores.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def compute_competitive_intensity(df: pd.DataFrame | None) -> pd.DataFrame:
    """Compute a competitive density score only from verified catalog inputs."""
    if df is None or df.empty:
        return pd.DataFrame(
            [{
                "metric": "competitive_intensity",
                "score": None,
                "manufacturer_count": None,
                "product_count": None,
                "price_range_inr": None,
                "status": "PENDING VERIFIED DATA",
            }]
        )

    required = ["manufacturer", "model_name", "ex_showroom_price_inr"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for competitive intensity: {missing}")

    product_count = int(len(df))
    manufacturer_count = int(df["manufacturer"].nunique())
    prices = _coerce_numeric(df["ex_showroom_price_inr"])
    price_range = float(prices.max() - prices.min()) if prices.notna().any() else None
    score = None
    if prices.notna().any():
        density = (manufacturer_count / max(product_count, 1)) * 100
        spread = (price_range / max(prices.max(), 1)) * 100 if price_range is not None and prices.max() else 0.0
        score = round(float((density * 0.6) + (spread * 0.4)), 2)

    return pd.DataFrame([
        {
            "metric": "competitive_intensity",
            "score": score,
            "manufacturer_count": manufacturer_count,
            "product_count": product_count,
            "price_range_inr": price_range,
            "status": "VERIFIED" if score is not None else "PENDING VERIFIED DATA",
        }
    ])


def compute_product_market_fit(df: pd.DataFrame | None) -> pd.DataFrame:
    """A template-only product-market fit score when no verified fit inputs are supplied."""
    if df is None or df.empty:
        return pd.DataFrame([
            {
                "metric": "product_market_fit",
                "score": None,
                "status": "PENDING VERIFIED DATA",
            }
        ])

    required = ["certified_range_km", "battery_capacity_kwh", "ex_showroom_price_inr"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for product-market fit: {missing}")

    values = df[required].copy()
    numeric = values.apply(_coerce_numeric)
    if numeric.empty or numeric.isna().all().all():
        return pd.DataFrame([
            {"metric": "product_market_fit", "score": None, "status": "PENDING VERIFIED DATA"}
        ])

    # Safe, data-driven combination of normalized attributes. No fake external assumptions.
    range_score = numeric["certified_range_km"].mean() / max(numeric["certified_range_km"].max(), 1)
    battery_score = numeric["battery_capacity_kwh"].mean() / max(numeric["battery_capacity_kwh"].max(), 1)
    value_score = 1 - (numeric["ex_showroom_price_inr"].mean() / max(numeric["ex_showroom_price_inr"].max(), 1))
    score = round(float((range_score * 0.45 + battery_score * 0.35 + value_score * 0.20) * 100), 2)
    return pd.DataFrame([
        {"metric": "product_market_fit", "score": score, "status": "VERIFIED"}
    ])


def compute_strategic_priority_score(df: pd.DataFrame | None) -> pd.DataFrame:
    """Return a template or calculated score from verified inputs without fabricating strategy."""
    if df is None or df.empty:
        return pd.DataFrame([
            {
                "market_attractiveness": None,
                "competitive_intensity": None,
                "product_market_fit": None,
                "geographic_attractiveness": None,
                "strategic_priority_score": None,
                "status": "PENDING VERIFIED DATA",
            }
        ])

    required = ["market_attractiveness", "competitive_intensity", "product_market_fit", "geographic_attractiveness"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        return pd.DataFrame([
            {
                "market_attractiveness": None,
                "competitive_intensity": None,
                "product_market_fit": None,
                "geographic_attractiveness": None,
                "strategic_priority_score": None,
                "status": "PENDING VERIFIED DATA",
                "missing_columns": missing,
            }
        ])

    values = df[required].apply(_coerce_numeric)
    with pd.option_context("mode.use_inf_as_na", True):
        numeric = values.dropna(how="all")
    if numeric.empty:
        return pd.DataFrame([
            {
                "market_attractiveness": None,
                "competitive_intensity": None,
                "product_market_fit": None,
                "geographic_attractiveness": None,
                "strategic_priority_score": None,
                "status": "PENDING VERIFIED DATA",
            }
        ])

    row = numeric.iloc[0].to_dict()
    score = (
        float(row.get("market_attractiveness", 0)) * 0.35
        + float(row.get("competitive_intensity", 0)) * 0.25
        + float(row.get("product_market_fit", 0)) * 0.25
        + float(row.get("geographic_attractiveness", 0)) * 0.15
    )
    return pd.DataFrame([
        {
            "market_attractiveness": row.get("market_attractiveness"),
            "competitive_intensity": row.get("competitive_intensity"),
            "product_market_fit": row.get("product_market_fit"),
            "geographic_attractiveness": row.get("geographic_attractiveness"),
            "strategic_priority_score": round(float(score), 2),
            "status": "VERIFIED",
        }
    ])


__all__ = [
    "compute_competitive_intensity",
    "compute_product_market_fit",
    "compute_strategic_priority_score",
]
