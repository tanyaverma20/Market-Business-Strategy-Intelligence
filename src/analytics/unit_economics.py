"""Unit economics framework. Cost/BOM data is intentionally treated as pending unless supplied."""

from __future__ import annotations

import pandas as pd


def build_unit_economics_input_template() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "selling_price": None,
                "cogs": None,
                "variable_cost": None,
                "fixed_cost": None,
                "units_sold": None,
                "bom_cost": None,
                "manufacturing_cost": None,
                "distribution_cost": None,
                "warranty_service_cost": None,
                "purchase_price": None,
                "subsidy": None,
                "electricity_cost": None,
                "maintenance_cost": None,
                "insurance_cost": None,
                "financing_cost": None,
                "ownership_period_years": None,
                "verification_status": "PENDING_COST_DATA",
            }
        ]
    )


def build_unit_economics_results_template() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gross_margin": None,
                "gross_margin_pct": None,
                "contribution_margin": None,
                "contribution_margin_pct": None,
                "break_even_units": None,
                "break_even_revenue": None,
                "tco": None,
                "calculation_status": "PENDING VERIFIED COST DATA",
                "metric_type": "pending",
            }
        ]
    )


def validate_cost_inputs(df: pd.DataFrame | None = None, **values) -> dict:
    payload = {**(df.to_dict(orient="records")[0] if isinstance(df, pd.DataFrame) and not df.empty else {}), **values}
    required = ["selling_price", "variable_cost", "fixed_cost", "units_sold", "bom_cost", "manufacturing_cost", "distribution_cost", "warranty_service_cost", "contribution_margin"]
    missing = [name for name in required if name not in payload or payload[name] is None]
    if missing:
        raise ValueError(f"Missing required unit economics inputs: {missing}")
    return payload


def compute_gross_margin(revenue: float, variable_cost: float) -> float:
    if revenue < 0 or variable_cost < 0:
        raise ValueError("Revenue and variable cost must be non-negative.")
    return float(revenue - variable_cost)


def compute_gross_margin_pct(revenue: float, variable_cost: float) -> float:
    if revenue <= 0:
        raise ValueError("Revenue must be greater than zero to compute gross margin percentage.")
    return float((revenue - variable_cost) / revenue * 100)


def compute_contribution_margin(revenue: float, variable_cost: float) -> float:
    return compute_gross_margin(revenue, variable_cost)


def compute_contribution_margin_pct(revenue: float, variable_cost: float) -> float:
    if revenue <= 0:
        raise ValueError("Revenue must be greater than zero to compute contribution margin percentage.")
    return float((revenue - variable_cost) / revenue * 100)


def compute_break_even_units(fixed_cost: float, unit_contribution_margin: float) -> float:
    if unit_contribution_margin <= 0:
        raise ValueError("Unit contribution margin must be greater than zero.")
    return float(fixed_cost / unit_contribution_margin)


def compute_break_even_revenue(fixed_cost: float, unit_contribution_margin: float, selling_price: float | None = None) -> float:
    """Break-even revenue = fixed cost / contribution margin rate.

    When a selling price is supplied, the margin rate is contribution margin per unit divided by
    selling price. Without a selling price, we do not fabricate a synthetic price; we return a
    clear validation error instead of forcing a number.
    """
    if fixed_cost < 0:
        raise ValueError("Fixed cost must be non-negative.")
    if selling_price is not None:
        price = float(selling_price)
        if price <= 0:
            raise ValueError("Selling price must be greater than zero.")
        if unit_contribution_margin < 0:
            raise ValueError("Unit contribution margin must be non-negative.")
        margin_rate = unit_contribution_margin / price
        if margin_rate <= 0:
            raise ValueError("Contribution margin rate must be greater than zero.")
        return float(fixed_cost / margin_rate)
    if unit_contribution_margin <= 0:
        raise ValueError("Contribution margin must be greater than zero to compute break-even revenue.")
    raise ValueError("Selling price is required to compute break-even revenue without fabricating assumptions.")


def compute_tco(
    purchase_price: float | None = None,
    subsidy: float | None = None,
    electricity_cost: float | None = None,
    maintenance_cost: float | None = None,
    insurance_cost: float | None = None,
    financing_cost: float | None = None,
    other_costs: float | None = None,
) -> dict:
    if any(value is None for value in [purchase_price, electricity_cost, maintenance_cost, insurance_cost]):
        return {"status": "PENDING VERIFIED COST DATA", "message": "Complete verified TCO inputs required.", "metric_type": "pending"}
    net_purchase = float(purchase_price or 0) - float(subsidy or 0)
    total = net_purchase + float(electricity_cost or 0) + float(maintenance_cost or 0) + float(insurance_cost or 0)
    total += float(financing_cost or 0) + float(other_costs or 0)
    return {"status": "AVAILABLE", "tco_inr": total, "metric_type": "derived"}


def compute_unit_economics_sensitivity(df: pd.DataFrame | None = None, **values) -> dict:
    if df is None and not values:
        return {"status": "PENDING VERIFIED DATA", "message": "Cost data required for unit economics.", "metric_type": "pending"}
    try:
        payload = validate_cost_inputs(df=df, **values)
    except ValueError as exc:
        return {"status": "PENDING VERIFIED DATA", "message": str(exc), "metric_type": "pending"}
    revenue = float(payload["selling_price"] * payload["units_sold"])
    variable_cost = float(payload["variable_cost"] * payload["units_sold"])
    fixed_cost = float(payload["fixed_cost"])
    margin = compute_contribution_margin(revenue, variable_cost)
    unit_margin = margin / max(payload["units_sold"], 1)
    return {
        "status": "AVAILABLE",
        "revenue": revenue,
        "variable_cost": variable_cost,
        "fixed_cost": fixed_cost,
        "gross_margin": compute_gross_margin(revenue, variable_cost),
        "gross_margin_pct": compute_gross_margin_pct(revenue, variable_cost),
        "contribution_margin": margin,
        "contribution_margin_pct": compute_contribution_margin_pct(revenue, variable_cost),
        "break_even_units": compute_break_even_units(fixed_cost, unit_margin),
        "break_even_revenue": compute_break_even_revenue(fixed_cost, unit_margin, payload["selling_price"]),
        "metric_type": "derived",
    }
