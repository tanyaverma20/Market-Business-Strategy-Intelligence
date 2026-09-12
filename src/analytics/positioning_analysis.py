"""Product positioning framework using only verified product data."""

from __future__ import annotations

from typing import Mapping

import pandas as pd


def classify_product_segment(product: Mapping[str, object]) -> dict:
    """Classify a product by price, range, and performance. This is a framework only."""
    price = float(product.get("ex_showroom_price_inr", 0) or 0)
    range_km = float(product.get("certified_range_km", 0) or 0)
    battery_kwh = float(product.get("battery_capacity_kwh", 0) or 0)
    speed = float(product.get("top_speed_kmh", 0) or 0)

    if price < 100000:
        price_bucket = "budget"
    elif price < 150000:
        price_bucket = "mid-market"
    else:
        price_bucket = "premium"

    if range_km >= 180:
        range_bucket = "long-range"
    elif range_km >= 120:
        range_bucket = "mainstream-range"
    else:
        range_bucket = "short-range"

    if battery_kwh >= 4.5:
        battery_bucket = "high-battery"
    elif battery_kwh >= 3.0:
        battery_bucket = "standard-battery"
    else:
        battery_bucket = "compact-battery"

    if speed >= 80:
        performance_bucket = "high-performance"
    elif speed >= 60:
        performance_bucket = "balanced"
    else:
        performance_bucket = "entry"

    whitespace = []
    if price_bucket == "budget" and range_bucket == "long-range":
        whitespace.append("budget-long-range")
    if price_bucket == "premium" and range_bucket == "short-range":
        whitespace.append("premium-short-range")
    if battery_bucket == "high-battery" and price_bucket == "budget":
        whitespace.append("value-high-battery")

    return {
        "segment": f"{price_bucket}-{range_bucket}",
        "price_bucket": price_bucket,
        "range_bucket": range_bucket,
        "battery_bucket": battery_bucket,
        "performance_bucket": performance_bucket,
        "whitespace_areas": whitespace,
        "metric_type": "derived",
    }


def generate_price_vs_range_positioning(df: pd.DataFrame) -> pd.DataFrame:
    required = {"manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km"}
    if not required.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified price and range columns required."]})
    out = df.copy()
    out["price_range_position"] = out.apply(lambda row: classify_product_segment(row)["segment"], axis=1)
    out["metric_type"] = "derived"
    return out[["manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km", "price_range_position", "metric_type"]]


def generate_price_vs_battery_positioning(df: pd.DataFrame) -> pd.DataFrame:
    required = {"manufacturer", "model_name", "ex_showroom_price_inr", "battery_capacity_kwh"}
    if not required.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified price and battery columns required."]})
    out = df.copy()
    out["price_battery_position"] = out.apply(lambda row: classify_product_segment(row)["battery_bucket"], axis=1)
    out["metric_type"] = "derived"
    return out[["manufacturer", "model_name", "ex_showroom_price_inr", "battery_capacity_kwh", "price_battery_position", "metric_type"]]


def generate_price_vs_performance_positioning(df: pd.DataFrame) -> pd.DataFrame:
    required = {"manufacturer", "model_name", "ex_showroom_price_inr", "top_speed_kmh"}
    if not required.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified price and performance columns required."]})
    out = df.copy()
    out["price_performance_position"] = out.apply(lambda row: classify_product_segment(row)["performance_bucket"], axis=1)
    out["metric_type"] = "derived"
    return out[["manufacturer", "model_name", "ex_showroom_price_inr", "top_speed_kmh", "price_performance_position", "metric_type"]]


def identify_competitive_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    if {"manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km", "battery_capacity_kwh"}.issubset(df.columns):
        out = df.copy()
        out["whitespace_areas"] = out.apply(lambda row: classify_product_segment(row)["whitespace_areas"], axis=1)
        out["metric_type"] = "derived"
        return out[["manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km", "battery_capacity_kwh", "whitespace_areas", "metric_type"]]
    return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verified product data required for whitespace analysis."]})


def product_segment_classification(df: pd.DataFrame) -> pd.DataFrame:
    if not {"manufacturer", "model_name"}.issubset(df.columns):
        return pd.DataFrame({"status": ["PENDING VERIFIED DATA"], "message": ["Verification required for product classification."]})
    out = df.copy()
    out["segment_summary"] = out.apply(lambda row: classify_product_segment(row), axis=1)
    out["metric_type"] = "derived"
    return out
