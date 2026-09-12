"""Pricing analytics for verified product catalogs only.

Weights are configurable and intentionally documented as default assumptions.
"""

from __future__ import annotations

import pandas as pd

DEFAULT_VALUE_WEIGHTS = {
    "range": 0.40,
    "battery": 0.20,
    "price_efficiency": 0.25,
    "performance": 0.15,
}


def _numeric_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def compute_ex_showroom_price(df: pd.DataFrame) -> pd.DataFrame:
    if "ex_showroom_price_inr" not in df.columns:
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified product price required."]})
    out = df[["manufacturer", "model_name", "ex_showroom_price_inr"]].copy()
    out["metric_type"] = "observed"
    return out.rename(columns={"ex_showroom_price_inr": "ex_showroom_price_inr"})


def compute_effective_price_after_subsidy(df: pd.DataFrame) -> pd.DataFrame:
    required = ["ex_showroom_price_inr"]
    if not all(col in df.columns for col in required):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified subsidized price data required before computing effective price."]})
    out = df[["manufacturer", "model_name", "ex_showroom_price_inr"]].copy()
    subsidy_cols = ["subsidy_inr", "subsidy_applicable", "subsidy_verified"]
    if all(col in df.columns for col in subsidy_cols):
        out["effective_price_after_subsidy_inr"] = pd.to_numeric(df["ex_showroom_price_inr"], errors="coerce") - pd.to_numeric(df["subsidy_inr"], errors="coerce")
        out["metric_type"] = "derived"
        out["status"] = "verified"
    else:
        out["effective_price_after_subsidy_inr"] = pd.to_numeric(df["ex_showroom_price_inr"], errors="coerce")
        out["metric_type"] = "observed"
        out["status"] = "PENDING VERIFIED SUBSIDY DATA"
    return out[["manufacturer", "model_name", "effective_price_after_subsidy_inr", "metric_type", "status"]]


def compute_price_per_certified_km(df: pd.DataFrame) -> pd.DataFrame:
    if not {"ex_showroom_price_inr", "certified_range_km"}.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified price and certified range required."]})
    out = df[["manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km"]].copy()
    out["price_per_certified_km_inr"] = _numeric_series(out["ex_showroom_price_inr"]) / _numeric_series(out["certified_range_km"])
    out["metric_type"] = "derived"
    return out


def compute_price_per_kwh(df: pd.DataFrame) -> pd.DataFrame:
    if not {"ex_showroom_price_inr", "battery_capacity_kwh"}.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified price and battery capacity required."]})
    out = df[["manufacturer", "model_name", "ex_showroom_price_inr", "battery_capacity_kwh"]].copy()
    out["price_per_kwh_inr"] = _numeric_series(out["ex_showroom_price_inr"]) / _numeric_series(out["battery_capacity_kwh"])
    out["metric_type"] = "derived"
    return out


def compute_price_percentile(df: pd.DataFrame) -> pd.DataFrame:
    if "ex_showroom_price_inr" not in df.columns:
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified product prices required."]})
    out = df[["manufacturer", "model_name", "ex_showroom_price_inr"]].copy()
    prices = _numeric_series(out["ex_showroom_price_inr"])
    out["price_percentile"] = prices.rank(method="average", pct=True) * 100
    out["metric_type"] = "derived"
    return out


def compute_range_percentile(df: pd.DataFrame) -> pd.DataFrame:
    if "certified_range_km" not in df.columns:
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified certified ranges required."]})
    out = df[["manufacturer", "model_name", "certified_range_km"]].copy()
    ranges = _numeric_series(out["certified_range_km"])
    out["range_percentile"] = ranges.rank(method="average", pct=True) * 100
    out["metric_type"] = "derived"
    return out


def compute_battery_percentile(df: pd.DataFrame) -> pd.DataFrame:
    if "battery_capacity_kwh" not in df.columns:
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified battery capacity required."]})
    out = df[["manufacturer", "model_name", "battery_capacity_kwh"]].copy()
    battery = _numeric_series(out["battery_capacity_kwh"])
    out["battery_percentile"] = battery.rank(method="average", pct=True) * 100
    out["metric_type"] = "derived"
    return out


def compute_value_score(df: pd.DataFrame, weights: dict | None = None) -> pd.DataFrame:
    """Default assumptions: range gets the highest weight; price efficiency rewards value per km."""
    weights = weights or DEFAULT_VALUE_WEIGHTS
    required = {"manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km", "battery_capacity_kwh", "top_speed_kmh"}
    if not required.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified product specs required for value score."]})
    out = df[["manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km", "battery_capacity_kwh", "top_speed_kmh"]].copy()
    out["product"] = out["model_name"]
    price = _numeric_series(out["ex_showroom_price_inr"])
    range_km = _numeric_series(out["certified_range_km"])
    battery = _numeric_series(out["battery_capacity_kwh"])
    speed = _numeric_series(out["top_speed_kmh"])
    price_efficiency = 1 / (price / range_km)
    range_score = (range_km - range_km.min()) / (range_km.max() - range_km.min()) * 100 if range_km.max() != range_km.min() else 100
    battery_score = (battery - battery.min()) / (battery.max() - battery.min()) * 100 if battery.max() != battery.min() else 100
    price_efficiency_score = (price_efficiency - price_efficiency.min()) / (price_efficiency.max() - price_efficiency.min()) * 100 if price_efficiency.max() != price_efficiency.min() else 100
    performance_score = (speed - speed.min()) / (speed.max() - speed.min()) * 100 if speed.max() != speed.min() else 100
    out["range_score"] = range_score
    out["battery_score"] = battery_score
    out["price_efficiency_score"] = price_efficiency_score
    out["performance_score"] = performance_score
    out["value_score"] = (
        weights.get("range", 0.40) * range_score
        + weights.get("battery", 0.20) * battery_score
        + weights.get("price_efficiency", 0.25) * price_efficiency_score
        + weights.get("performance", 0.15) * performance_score
    )
    out["metric_type"] = "derived"
    out["methodology_version"] = "value-score-v1"
    out["normalization_method"] = "min-max across verified catalog; price efficiency = 1 / (price_per_km)"
    out["weight_configuration"] = str(weights)
    return out[["manufacturer", "product", "model_name", "value_score", "range_score", "battery_score", "price_efficiency_score", "performance_score", "metric_type", "methodology_version", "normalization_method", "weight_configuration"]]
