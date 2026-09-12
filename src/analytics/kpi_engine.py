"""KPI registry and calculation framework.

This module keeps a centralized catalog of KPI definitions and explicitly marks
market, cost, and geographic KPIs as pending unless verified source inputs are
provided. Product-level KPIs are calculated only from the verified catalog.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .competitive_analysis import (
    compute_manufacturer_count,
    compute_manufacturer_portfolio_analysis,
    compute_price_per_km,
    compute_price_per_kwh,
    compute_product_count,
)
from .market_analysis import cagr, oem_market_share
from .pricing_analysis import (
    compute_battery_percentile,
    compute_price_percentile,
    compute_range_percentile,
    compute_value_score,
)


KPI_REGISTRY = [
    {
        "kpi_name": "Annual EV registrations",
        "business_meaning": "Total verified EV sales in a year.",
        "formula": "sum(e2w_registrations) by year",
        "required_dataset": "verified market registration dataset",
        "required_columns": ["year", "e2w_registrations"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "units",
        "calculation_function": "annual_market_volume",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Monthly EV registrations",
        "business_meaning": "Monthly EV volume for trend and seasonality analysis.",
        "formula": "sum(e2w_registrations) by date",
        "required_dataset": "verified market registration dataset",
        "required_columns": ["date", "e2w_registrations"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "units",
        "calculation_function": "monthly_market_volume",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "YoY growth",
        "business_meaning": "Annual change in EV registrations relative to the prior year.",
        "formula": "((current - previous) / previous) * 100",
        "required_dataset": "verified market registration dataset",
        "required_columns": ["year", "e2w_registrations"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "%",
        "calculation_function": "yoy_growth",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "CAGR",
        "business_meaning": "Compound annual growth rate across a multi-year trend window.",
        "formula": "((end / start)^(1 / years) - 1) * 100",
        "required_dataset": "verified market registration dataset",
        "required_columns": ["year", "e2w_registrations"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "%",
        "calculation_function": "cagr",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "EV penetration",
        "business_meaning": "Share of total 2W registrations represented by EVs.",
        "formula": "(e2w_registrations / total_2w_registrations) * 100",
        "required_dataset": "verified market registration dataset",
        "required_columns": ["e2w_registrations", "total_2w_registrations"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "%",
        "calculation_function": "ev_penetration",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "TAM",
        "business_meaning": "Total addressable market under an explicit market-size model.",
        "formula": "total_market_units * avg_price or equivalent configurable model",
        "required_dataset": "verified market sizing inputs",
        "required_columns": ["total_market_units"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "units or INR",
        "calculation_function": "tam",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "SAM",
        "business_meaning": "Serviceable addressable market in the target segment.",
        "formula": "target_units * target_share",
        "required_dataset": "verified market sizing inputs",
        "required_columns": ["target_units", "target_share"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "units or INR",
        "calculation_function": "sam",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "SOM",
        "business_meaning": "Serviceable obtainable market under explicit adoption assumptions.",
        "formula": "SAM * target_market_share",
        "required_dataset": "verified market sizing inputs",
        "required_columns": ["sam_units", "target_market_share"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "units or INR",
        "calculation_function": "som",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "OEM market share",
        "business_meaning": "Share of annual EV registrations by OEM.",
        "formula": "(OEM registrations / total registrations) * 100",
        "required_dataset": "verified OEM registration dataset",
        "required_columns": ["oem_name", "year", "e2w_registrations"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "%",
        "calculation_function": "oem_market_share",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "HHI",
        "business_meaning": "Market concentration measure based on verified OEM share data.",
        "formula": "sum(market_share_pct^2)",
        "required_dataset": "verified OEM registration dataset",
        "required_columns": ["oem_name", "year", "market_share_pct"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "index",
        "calculation_function": "market_concentration_hhi",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Manufacturer count",
        "business_meaning": "Distinct manufacturers represented in the verified product catalog.",
        "formula": "nunique(manufacturer)",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["manufacturer"],
        "source_provenance": "verified_primary_source",
        "unit": "count",
        "calculation_function": "compute_manufacturer_count",
        "current_status": "VERIFIED",
        "calculation_type": "verified",
    },
    {
        "kpi_name": "Product count",
        "business_meaning": "Distinct product variants in the verified catalog.",
        "formula": "nunique(model_name)",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["model_name"],
        "source_provenance": "verified_primary_source",
        "unit": "count",
        "calculation_function": "compute_product_count",
        "current_status": "VERIFIED",
        "calculation_type": "verified",
    },
    {
        "kpi_name": "Average product price",
        "business_meaning": "Mean verified ex-showroom price across the product set.",
        "formula": "mean(ex_showroom_price_inr)",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["ex_showroom_price_inr"],
        "source_provenance": "verified_primary_source",
        "unit": "INR",
        "calculation_function": "mean",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Median product price",
        "business_meaning": "Median verified ex-showroom price across the product set.",
        "formula": "median(ex_showroom_price_inr)",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["ex_showroom_price_inr"],
        "source_provenance": "verified_primary_source",
        "unit": "INR",
        "calculation_function": "median",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Price per certified km",
        "business_meaning": "Ex-showroom price relative to certified range.",
        "formula": "ex_showroom_price_inr / certified_range_km",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["ex_showroom_price_inr", "certified_range_km"],
        "source_provenance": "verified_primary_source",
        "unit": "INR/km",
        "calculation_function": "compute_price_per_certified_km",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Price per kWh",
        "business_meaning": "Ex-showroom price relative to battery capacity.",
        "formula": "ex_showroom_price_inr / battery_capacity_kwh",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["ex_showroom_price_inr", "battery_capacity_kwh"],
        "source_provenance": "verified_primary_source",
        "unit": "INR/kWh",
        "calculation_function": "compute_price_per_kwh",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Average battery capacity",
        "business_meaning": "Mean verified battery capacity.",
        "formula": "mean(battery_capacity_kwh)",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["battery_capacity_kwh"],
        "source_provenance": "verified_primary_source",
        "unit": "kWh",
        "calculation_function": "mean",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Average certified range",
        "business_meaning": "Mean certified range across the verified catalog.",
        "formula": "mean(certified_range_km)",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["certified_range_km"],
        "source_provenance": "verified_primary_source",
        "unit": "km",
        "calculation_function": "mean",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Range realization %",
        "business_meaning": "Real-world range as a share of certified range.",
        "formula": "(real_world_range_km / certified_range_km) * 100",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["real_world_range_km", "certified_range_km"],
        "source_provenance": "verified_primary_source",
        "unit": "%",
        "calculation_function": "compute_range_realization",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Product value score",
        "business_meaning": "A normalized weighted score for price efficiency, range, battery, and performance.",
        "formula": "weighted normalized components",
        "required_dataset": "verified_product_catalog_2025_2026.csv",
        "required_columns": ["ex_showroom_price_inr", "certified_range_km", "battery_capacity_kwh", "top_speed_kmh"],
        "source_provenance": "verified_primary_source",
        "unit": "0-100",
        "calculation_function": "compute_value_score",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Gross margin %",
        "business_meaning": "Gross margin relative to selling price.",
        "formula": "(selling_price - COGS) / selling_price * 100",
        "required_dataset": "verified cost input template",
        "required_columns": ["selling_price", "cogs"],
        "source_provenance": "PENDING_COST_DATA",
        "unit": "%",
        "calculation_function": "compute_gross_margin_pct",
        "current_status": "PENDING VERIFIED COST DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Contribution margin",
        "business_meaning": "Revenue contribution after variable costs.",
        "formula": "selling_price * units_sold - variable_cost * units_sold",
        "required_dataset": "verified cost input template",
        "required_columns": ["selling_price", "variable_cost", "units_sold"],
        "source_provenance": "PENDING_COST_DATA",
        "unit": "INR",
        "calculation_function": "compute_contribution_margin",
        "current_status": "PENDING VERIFIED COST DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Contribution margin %",
        "business_meaning": "Contribution margin as a percent of selling price.",
        "formula": "((selling_price - variable_cost) / selling_price) * 100",
        "required_dataset": "verified cost input template",
        "required_columns": ["selling_price", "variable_cost"],
        "source_provenance": "PENDING_COST_DATA",
        "unit": "%",
        "calculation_function": "compute_contribution_margin_pct",
        "current_status": "PENDING VERIFIED COST DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Break-even units",
        "business_meaning": "Units required to cover fixed costs.",
        "formula": "fixed_cost / contribution_margin_per_unit",
        "required_dataset": "verified cost input template",
        "required_columns": ["fixed_cost", "selling_price", "variable_cost"],
        "source_provenance": "PENDING_COST_DATA",
        "unit": "units",
        "calculation_function": "compute_break_even_units",
        "current_status": "PENDING VERIFIED COST DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Break-even revenue",
        "business_meaning": "Revenue needed to reach break-even.",
        "formula": "break_even_units * selling_price",
        "required_dataset": "verified cost input template",
        "required_columns": ["fixed_cost", "selling_price", "variable_cost"],
        "source_provenance": "PENDING_COST_DATA",
        "unit": "INR",
        "calculation_function": "compute_break_even_revenue",
        "current_status": "PENDING VERIFIED COST DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "TCO",
        "business_meaning": "Lifetime total cost of ownership for a verified vehicle scenario.",
        "formula": "purchase_price - subsidy + electricity + maintenance + insurance + financing + other costs",
        "required_dataset": "verified cost and ownership assumptions",
        "required_columns": ["purchase_price", "subsidy", "electricity_cost", "maintenance_cost", "insurance_cost"],
        "source_provenance": "PENDING_COST_DATA",
        "unit": "INR",
        "calculation_function": "compute_tco",
        "current_status": "PENDING VERIFIED COST DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Geographic Attractiveness Index (GAI)",
        "business_meaning": "State-level attractiveness score based on verified market, policy, and infrastructure inputs.",
        "formula": "weighted normalized components",
        "required_dataset": "verified state indicator dataset",
        "required_columns": ["state", "market_size", "ev_penetration", "growth", "purchasing_power", "charging_infrastructure", "policy_score"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "0-100",
        "calculation_function": "compute_gai_template",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
    {
        "kpi_name": "Competitive intensity score",
        "business_meaning": "A score describing competitive density for the product set.",
        "formula": "weighted manufacturer count, product count, price density, and segment density",
        "required_dataset": "verified product catalog",
        "required_columns": ["manufacturer", "model_name", "vehicle_category", "ex_showroom_price_inr"],
        "source_provenance": "verified_primary_source",
        "unit": "0-100",
        "calculation_function": "compute_competitive_intensity",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Product-market fit score",
        "business_meaning": "A fit score expressing alignment between product features and value expectations.",
        "formula": "weighted normalized range, battery, and value score",
        "required_dataset": "verified product catalog",
        "required_columns": ["certified_range_km", "battery_capacity_kwh", "ex_showroom_price_inr"],
        "source_provenance": "verified_primary_source",
        "unit": "0-100",
        "calculation_function": "compute_product_market_fit",
        "current_status": "VERIFIED",
        "calculation_type": "derived",
    },
    {
        "kpi_name": "Strategic priority score",
        "business_meaning": "Combined attractiveness and competitive score for prioritization.",
        "formula": "weighted market attractiveness + competitive intensity + product-market fit + geographic attractiveness",
        "required_dataset": "framework-ready inputs",
        "required_columns": ["market_attractiveness", "competitive_intensity", "product_market_fit", "geographic_attractiveness"],
        "source_provenance": "PENDING VERIFIED DATA",
        "unit": "0-100",
        "calculation_function": "compute_strategic_priority_score",
        "current_status": "PENDING VERIFIED DATA",
        "calculation_type": "pending",
    },
]


def get_kpi_registry() -> pd.DataFrame:
    return pd.DataFrame(KPI_REGISTRY)


def _normalize_verified_product_schema(df: pd.DataFrame | None) -> pd.DataFrame | None:
    if df is None or df.empty:
        return df
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
    return out


def calculate_kpi_status(df: pd.DataFrame | None = None) -> pd.DataFrame:
    normalized = _normalize_verified_product_schema(df)
    registry = get_kpi_registry()
    rows = []
    for _, row in registry.iterrows():
        required = row["required_columns"]
        status = "PENDING VERIFIED DATA"
        if isinstance(normalized, pd.DataFrame) and all(col in normalized.columns for col in required):
            status = "AVAILABLE"
        rows.append(
            {
                "kpi_name": row["kpi_name"],
                "current_status": row["current_status"],
                "availability_status": status,
                "required_columns": required,
                "source_provenance": row["source_provenance"],
                "calculation_type": row["calculation_type"],
            }
        )
    return pd.DataFrame(rows)


def calculate_product_kpis(df: pd.DataFrame | None) -> dict[str, Any]:
    normalized = _normalize_verified_product_schema(df)
    if normalized is None or normalized.empty:
        return {"status": "PENDING VERIFIED DATA", "metrics": {}}
    metrics = {
        "product_count": compute_product_count(normalized),
        "manufacturer_count": compute_manufacturer_count(normalized),
        "average_product_price": float(pd.to_numeric(normalized["ex_showroom_price_inr"], errors="coerce").mean()) if "ex_showroom_price_inr" in normalized.columns else None,
        "median_product_price": float(pd.to_numeric(normalized["ex_showroom_price_inr"], errors="coerce").median()) if "ex_showroom_price_inr" in normalized.columns else None,
        "average_battery_capacity": float(pd.to_numeric(normalized["battery_capacity_kwh"], errors="coerce").mean()) if "battery_capacity_kwh" in normalized.columns else None,
        "average_certified_range": float(pd.to_numeric(normalized["certified_range_km"], errors="coerce").mean()) if "certified_range_km" in normalized.columns else None,
    }
    return {"status": "AVAILABLE", "metrics": metrics}


def calculate_market_kpis(df: pd.DataFrame | None) -> dict[str, Any]:
    if df is None or df.empty:
        return {"status": "PENDING VERIFIED DATA"}
    if {"year", "e2w_registrations"}.issubset(df.columns):
        annual = df.groupby("year")["e2w_registrations"].sum().reset_index()
        return {"status": "AVAILABLE", "annual_registrations": annual.to_dict(orient="records"), "cagr": cagr(annual, year_col="year", reg_col="e2w_registrations")}
    return {"status": "PENDING VERIFIED DATA"}


def calculate_oem_kpis(df: pd.DataFrame | None) -> dict[str, Any]:
    if df is None or df.empty or not {"oem_name", "year", "e2w_registrations"}.issubset(df.columns):
        return {"status": "PENDING VERIFIED DATA"}
    return {"status": "AVAILABLE", "market_share": oem_market_share(df)}


def calculate_pricing_kpis(df: pd.DataFrame | None) -> dict[str, Any]:
    normalized = _normalize_verified_product_schema(df)
    if normalized is None or normalized.empty or not {"manufacturer", "model_name", "ex_showroom_price_inr", "certified_range_km", "battery_capacity_kwh"}.issubset(normalized.columns):
        return {"status": "PENDING VERIFIED DATA"}
    return {
        "status": "AVAILABLE",
        "price_per_km": compute_price_per_km(normalized),
        "price_per_kwh": compute_price_per_kwh(normalized),
        "price_percentile": compute_price_percentile(normalized),
        "battery_percentile": compute_battery_percentile(normalized),
        "range_percentile": compute_range_percentile(normalized),
        "value_score": compute_value_score(normalized),
    }


def generate_kpi_outputs(product_df: pd.DataFrame | None = None, output_dir: str | Path | None = None) -> dict[str, pd.DataFrame]:
    normalized = _normalize_verified_product_schema(product_df)
    base = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parents[1] / "data" / "processed"
    base.mkdir(parents=True, exist_ok=True)
    registry = get_kpi_registry()
    registry.to_csv(base / "kpi_registry.csv", index=False)
    status = calculate_kpi_status(normalized)
    status.to_csv(base / "kpi_status.csv", index=False)
    outputs: dict[str, pd.DataFrame] = {"kpi_registry": registry, "kpi_status": status}
    if normalized is not None and not normalized.empty:
        product_kpis = calculate_product_kpis(normalized)
        pd.DataFrame([product_kpis["metrics"]]).to_csv(base / "competitive_kpis.csv", index=False)
        manufacturer_summary = compute_manufacturer_portfolio_analysis(normalized)
        manufacturer_summary.to_csv(base / "manufacturer_kpis.csv", index=False)
        pricing_detail = calculate_pricing_kpis(normalized)
        if pricing_detail.get("status") == "AVAILABLE":
            pricing_detail["price_per_km"].to_csv(base / "pricing_kpis.csv", index=False)
        product_value_scores = compute_value_score(normalized)
        product_value_scores.to_csv(base / "product_value_scores.csv", index=False)
        outputs["competitive_kpis"] = pd.DataFrame([product_kpis["metrics"]])
        outputs["manufacturer_kpis"] = manufacturer_summary
        outputs["pricing_kpis"] = pricing_detail.get("price_per_km", pd.DataFrame())
        outputs["product_value_scores"] = product_value_scores
    return outputs
