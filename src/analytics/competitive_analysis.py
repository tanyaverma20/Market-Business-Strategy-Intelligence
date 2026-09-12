"""Competitive analysis rooted in the verified product catalog only."""

from __future__ import annotations

import pandas as pd


REQUIRED_PRODUCT_COLUMNS = [
    "manufacturer",
    "model_name",
    "vehicle_category",
    "ex_showroom_price_inr",
    "battery_capacity_kwh",
    "certified_range_km",
    "real_world_range_km",
    "top_speed_kmh",
    "motor_peak_power_kw",
    "source_type",
    "verification_status",
]


def normalize_verified_product_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the verified product schema to the canonical analytical fields used across modules."""
    out = df.copy()
    if "certified_range_km" not in out.columns and "range_km" in out.columns:
        out["certified_range_km"] = pd.to_numeric(out["range_km"], errors="coerce")
    if "real_world_range_km" not in out.columns and "real_world_range_km" in out.columns:
        out["real_world_range_km"] = pd.to_numeric(out["real_world_range_km"], errors="coerce")
    if "battery_capacity_kwh" not in out.columns and "battery_capacity_kwh" in out.columns:
        out["battery_capacity_kwh"] = pd.to_numeric(out["battery_capacity_kwh"], errors="coerce")
    if "top_speed_kmh" not in out.columns and "top_speed_kmh" in out.columns:
        out["top_speed_kmh"] = pd.to_numeric(out["top_speed_kmh"], errors="coerce")
    if "motor_peak_power_kw" not in out.columns and "motor_peak_power_kw" in out.columns:
        out["motor_peak_power_kw"] = pd.to_numeric(out["motor_peak_power_kw"], errors="coerce")
    if "ex_showroom_price_inr" not in out.columns and "price_inr" in out.columns:
        out["ex_showroom_price_inr"] = pd.to_numeric(out["price_inr"], errors="coerce")
    if "verification_status" not in out.columns:
        out["verification_status"] = "verified"
    return out


def _ensure_verified_product_input(df: pd.DataFrame, required_columns: list[str] | None = None) -> pd.DataFrame:
    normalized = normalize_verified_product_schema(df)
    required = required_columns or ["manufacturer", "model_name"]
    missing = [col for col in required if col not in normalized.columns]
    if missing:
        raise ValueError(f"Missing required product columns: {missing}")
    return normalized


def compute_manufacturer_count(df: pd.DataFrame) -> int:
    validated = _ensure_verified_product_input(df, ["manufacturer"])
    return int(validated["manufacturer"].nunique())


def compute_product_count(df: pd.DataFrame) -> int:
    validated = _ensure_verified_product_input(df, ["model_name"])
    return int(validated["model_name"].nunique())


def compute_product_category_distribution(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["vehicle_category"])
    category_summary = validated.groupby("vehicle_category", as_index=False).size().rename(columns={"size": "product_count"})
    category_summary["share_pct"] = (category_summary["product_count"] / category_summary["product_count"].sum() * 100).round(2)
    category_summary["metric_type"] = "derived"
    return category_summary


def compute_price_comparison(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["ex_showroom_price_inr"])
    prices = pd.to_numeric(validated["ex_showroom_price_inr"], errors="coerce").dropna()
    summary = {
        "metric": ["ex_showroom_price_inr"],
        "min": [float(prices.min()) if not prices.empty else None],
        "max": [float(prices.max()) if not prices.empty else None],
        "mean": [float(prices.mean()) if not prices.empty else None],
        "median": [float(prices.median()) if not prices.empty else None],
        "metric_type": ["derived"],
    }
    return pd.DataFrame(summary)


def compute_battery_comparison(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["battery_capacity_kwh"])
    batteries = pd.to_numeric(validated["battery_capacity_kwh"], errors="coerce").dropna()
    summary = {
        "metric": ["battery_capacity_kwh"],
        "min": [float(batteries.min()) if not batteries.empty else None],
        "max": [float(batteries.max()) if not batteries.empty else None],
        "mean": [float(batteries.mean()) if not batteries.empty else None],
        "median": [float(batteries.median()) if not batteries.empty else None],
        "metric_type": ["derived"],
    }
    return pd.DataFrame(summary)


def compute_range_comparison(df: pd.DataFrame, range_col: str = "certified_range_km") -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, [range_col])
    ranges = pd.to_numeric(validated[range_col], errors="coerce").dropna()
    summary = {
        "metric": [range_col],
        "min": [float(ranges.min()) if not ranges.empty else None],
        "max": [float(ranges.max()) if not ranges.empty else None],
        "mean": [float(ranges.mean()) if not ranges.empty else None],
        "median": [float(ranges.median()) if not ranges.empty else None],
        "metric_type": ["derived"],
    }
    return pd.DataFrame(summary)


def compute_top_speed_comparison(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["top_speed_kmh"])
    speeds = pd.to_numeric(validated["top_speed_kmh"], errors="coerce").dropna()
    return pd.DataFrame({
        "metric": ["top_speed_kmh"],
        "min": [float(speeds.min()) if not speeds.empty else None],
        "max": [float(speeds.max()) if not speeds.empty else None],
        "mean": [float(speeds.mean()) if not speeds.empty else None],
        "median": [float(speeds.median()) if not speeds.empty else None],
        "metric_type": ["derived"],
    })


def compute_motor_power_comparison(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["motor_peak_power_kw"])
    powers = pd.to_numeric(validated["motor_peak_power_kw"], errors="coerce").dropna()
    return pd.DataFrame({
        "metric": ["motor_peak_power_kw"],
        "min": [float(powers.min()) if not powers.empty else None],
        "max": [float(powers.max()) if not powers.empty else None],
        "mean": [float(powers.mean()) if not powers.empty else None],
        "median": [float(powers.median()) if not powers.empty else None],
        "metric_type": ["derived"],
    })


def compute_price_per_km(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["ex_showroom_price_inr", "certified_range_km"])
    prices = pd.to_numeric(validated["ex_showroom_price_inr"], errors="coerce")
    ranges = pd.to_numeric(validated["certified_range_km"], errors="coerce")
    if (prices < 0).any() or (ranges <= 0).any():
        raise ValueError("Price values must be non-negative and certified range values must be greater than zero.")
    out = validated.copy()
    out["price_per_certified_km_inr"] = prices / ranges
    out["metric_type"] = "derived"
    return out[["manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km", "price_per_certified_km_inr", "metric_type"]]


def compute_price_per_kwh(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["ex_showroom_price_inr", "battery_capacity_kwh"])
    prices = pd.to_numeric(validated["ex_showroom_price_inr"], errors="coerce")
    batteries = pd.to_numeric(validated["battery_capacity_kwh"], errors="coerce")
    if (prices < 0).any() or (batteries <= 0).any():
        raise ValueError("Price values must be non-negative and battery capacity values must be greater than zero.")
    out = validated.copy()
    out["price_per_kwh_inr"] = prices / batteries
    out["metric_type"] = "derived"
    return out[["manufacturer", "model_name", "ex_showroom_price_inr", "battery_capacity_kwh", "price_per_kwh_inr", "metric_type"]]


def compute_range_realization(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["certified_range_km", "real_world_range_km"])
    out = validated.copy()
    certified = pd.to_numeric(out["certified_range_km"], errors="coerce")
    real = pd.to_numeric(out["real_world_range_km"], errors="coerce")
    out["range_realization_pct"] = pd.NA
    mask = certified.notna() & real.notna() & (certified > 0)
    out.loc[mask, "range_realization_pct"] = (real[mask] / certified[mask] * 100)
    out["metric_type"] = "derived"
    out["status"] = "observed"
    if certified.isna().any() or real.isna().any() or (certified <= 0).any():
        out["status"] = "PENDING VERIFIED DATA"
    return out[["manufacturer", "model_name", "certified_range_km", "real_world_range_km", "range_realization_pct", "metric_type", "status"]]


def compute_manufacturer_portfolio_analysis(df: pd.DataFrame) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["manufacturer", "ex_showroom_price_inr", "battery_capacity_kwh", "certified_range_km"])
    out = validated.groupby("manufacturer", as_index=False).agg(
        product_count=("model_name", "count"),
        average_price_inr=("ex_showroom_price_inr", "mean"),
        average_battery_kwh=("battery_capacity_kwh", "mean"),
        average_range_km=("certified_range_km", "mean"),
    )
    out["metric_type"] = "derived"
    return out


def rank_products(df: pd.DataFrame, sort_columns: list[str] | None = None) -> pd.DataFrame:
    validated = _ensure_verified_product_input(df, ["manufacturer", "model_name"])
    columns = sort_columns or ["ex_showroom_price_inr", "certified_range_km", "battery_capacity_kwh"]
    out = validated.copy()
    for column in columns:
        if column in ["ex_showroom_price_inr"]:
            out[f"{column}_rank"] = pd.to_numeric(out[column], errors="coerce").rank(ascending=True, na_option="keep")
        else:
            out[f"{column}_rank"] = pd.to_numeric(out[column], errors="coerce").rank(ascending=False, na_option="keep")
    out["overall_rank_score"] = out[[f"{column}_rank" for column in columns]].sum(axis=1, skipna=True)
    out["overall_rank"] = out["overall_rank_score"].rank(method="dense", ascending=True)
    out["metric_type"] = "derived"
    return out[["manufacturer", "model_name", "overall_rank_score", "overall_rank", "metric_type"]]
