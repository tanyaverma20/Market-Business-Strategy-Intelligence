"""Market analytics framework that is intentionally safe with unverified or missing data.

This module does not fabricate market registration totals. It accepts market data as input,
validates that the required, verified fields are present, and otherwise returns a clear
status indicating that additional verified data is needed.
"""

from __future__ import annotations

from typing import Iterable, Mapping

import pandas as pd


def validate_required_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> pd.DataFrame:
    """Validate a DataFrame contains all required columns before computing a metric."""
    columns = list(required_columns)
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def market_status_for_verified_data(required_context: Mapping[str, object], df: pd.DataFrame | None = None) -> dict:
    """Return a structured status message when the required verified market data is absent."""
    required_columns = list(required_context.get("required_columns", []))
    dataset_name = str(required_context.get("dataset_name", "verified market dataset"))
    metric_name = str(required_context.get("metric_name", "market metric"))
    missing = []
    if isinstance(df, pd.DataFrame):
        missing = [col for col in required_columns if col not in df.columns]
    if df is None or not isinstance(df, pd.DataFrame) or df.empty or missing:
        return {
            "metric": metric_name,
            "status": "VERIFIED DATA REQUIRED",
            "dataset_name": dataset_name,
            "required_columns": required_columns,
            "missing_columns": missing,
            "message": "Verified data required before this market metric can be calculated.",
            "data_available": False,
        }
    return {
        "metric": metric_name,
        "status": "AVAILABLE",
        "dataset_name": dataset_name,
        "required_columns": required_columns,
        "missing_columns": [],
        "message": "Verified data is present.",
        "data_available": True,
    }


def monthly_registrations(df: pd.DataFrame, date_col: str = "date", reg_col: str = "e2w_registrations") -> pd.DataFrame | dict:
    """Aggregate a monthly registration series. Requires official registrations data."""
    status = market_status_for_verified_data({"metric_name": "Monthly registrations", "required_columns": [date_col, reg_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validated = validate_required_columns(df, [date_col, reg_col]).copy()
    out = validated[[date_col, reg_col]].groupby(date_col, as_index=False)[reg_col].sum()
    out = out.rename(columns={date_col: "date", reg_col: "monthly_registrations"})
    out["metric_type"] = "derived"
    return out


def annual_registrations(df: pd.DataFrame, year_col: str = "year", reg_col: str = "e2w_registrations") -> pd.DataFrame | dict:
    """Annual total registrations. Requires a verified year-level dataset."""
    status = market_status_for_verified_data({"metric_name": "Annual registrations", "required_columns": [year_col, reg_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validated = validate_required_columns(df, [year_col, reg_col]).copy()
    out = validated.groupby(year_col, as_index=False)[reg_col].sum().rename(columns={reg_col: "annual_registrations"})
    out["metric_type"] = "derived"
    return out


def yoy_growth(df: pd.DataFrame, year_col: str = "year", reg_col: str = "e2w_registrations") -> pd.DataFrame | dict:
    """Year-over-year growth rate. Formula: ((current - prior) / prior) * 100."""
    status = market_status_for_verified_data({"metric_name": "YoY growth", "required_columns": [year_col, reg_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validated = validate_required_columns(df, [year_col, reg_col]).copy()
    out = validated.sort_values(year_col).copy()
    out["previous_year_value"] = out[reg_col].shift(1)
    out["yoy_growth_pct"] = (out[reg_col] - out["previous_year_value"]) / out["previous_year_value"] * 100
    out = out[[year_col, reg_col, "yoy_growth_pct"]].rename(columns={reg_col: "annual_registrations"})
    out["metric_type"] = "derived"
    return out


def cagr(df: pd.DataFrame, year_col: str = "year", reg_col: str = "e2w_registrations") -> float | dict:
    """Compound annual growth rate for the full window. Requires verified values for start and end year."""
    status = market_status_for_verified_data({"metric_name": "CAGR", "required_columns": [year_col, reg_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validated = validate_required_columns(df, [year_col, reg_col]).copy().sort_values(year_col)
    if len(validated) < 2:
        return {"metric": "CAGR", "status": "PENDING VERIFIED DATA", "message": "At least two annual observations are required."}
    start = validated.iloc[0][reg_col]
    end = validated.iloc[-1][reg_col]
    years = validated.iloc[-1][year_col] - validated.iloc[0][year_col]
    if start <= 0 or years <= 0:
        return {"metric": "CAGR", "status": "PENDING VERIFIED DATA", "message": "Zero or invalid numerator/denominator for CAGR."}
    value = ((end / start) ** (1 / years) - 1) * 100
    return {"metric": "CAGR", "status": "AVAILABLE", "value": round(float(value), 4), "metric_type": "derived", "formula": "((end/start)^(1/years)-1)*100"}


def ev_penetration(df: pd.DataFrame, ev_col: str = "e2w_registrations", total_col: str = "total_2w_registrations") -> pd.DataFrame | dict:
    """EV penetration = EV registrations / total vehicle registrations across the same period."""
    status = market_status_for_verified_data({"metric_name": "EV penetration", "required_columns": [ev_col, total_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validated = validate_required_columns(df, [ev_col, total_col]).copy()
    out = validated.copy()
    out["ev_penetration_pct"] = (out[ev_col] / out[total_col] * 100)
    out["metric_type"] = "derived"
    return out


def market_size(df: pd.DataFrame, ev_col: str = "e2w_registrations", price_col: str = "average_price_inr") -> dict:
    """Total market size metric. Requires verified sales and unit values."""
    required = [ev_col, price_col]
    status = market_status_for_verified_data({"metric_name": "Market size", "required_columns": required}, df)
    if status["status"] != "AVAILABLE":
        return status
    validate_required_columns(df, required)
    total_units = float(df[ev_col].sum())
    total_value = float((df[ev_col] * df[price_col]).sum())
    return {"metric": "market_size", "status": "AVAILABLE", "total_units": total_units, "total_market_value_inr": total_value, "metric_type": "derived"}


def tam(df: pd.DataFrame, total_market_units_col: str = "total_2w_market_units") -> dict:
    """TAM placeholder wrapper. Calculation only if a verified total-market input is supplied."""
    status = market_status_for_verified_data({"metric_name": "TAM", "required_columns": [total_market_units_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    total_units = float(df[total_market_units_col].sum())
    return {"metric": "TAM", "status": "AVAILABLE", "value_units": total_units, "metric_type": "derived"}


def sam(df: pd.DataFrame, target_units_col: str = "target_units", target_share_col: str = "target_share") -> dict:
    """SAM placeholder wrapper. Needs serviceable market inputs, not proxy assumptions."""
    status = market_status_for_verified_data({"metric_name": "SAM", "required_columns": [target_units_col, target_share_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validate_required_columns(df, [target_units_col, target_share_col])
    value = float((df[target_units_col] * df[target_share_col]).sum())
    return {"metric": "SAM", "status": "AVAILABLE", "value_units": value, "metric_type": "derived"}


def som(df: pd.DataFrame, sam_col: str = "sam_units", market_share_col: str = "target_market_share") -> dict:
    """SOM placeholder wrapper. Requires serviceable market and realistic share assumptions."""
    status = market_status_for_verified_data({"metric_name": "SOM", "required_columns": [sam_col, market_share_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validate_required_columns(df, [sam_col, market_share_col])
    value = float((df[sam_col] * df[market_share_col]).sum())
    return {"metric": "SOM", "status": "AVAILABLE", "value_units": value, "metric_type": "derived"}


def monthly_trend(df: pd.DataFrame, date_col: str = "date", reg_col: str = "e2w_registrations") -> pd.DataFrame | dict:
    return monthly_registrations(df, date_col=date_col, reg_col=reg_col)


def annual_trend(df: pd.DataFrame, year_col: str = "year", reg_col: str = "e2w_registrations") -> pd.DataFrame | dict:
    return annual_registrations(df, year_col=year_col, reg_col=reg_col)


def state_level_market_analysis(df: pd.DataFrame, state_col: str = "state", reg_col: str = "e2w_registrations") -> pd.DataFrame | dict:
    """State-level market analysis is only valid for verified state registration data."""
    status = market_status_for_verified_data({"metric_name": "State-level market analysis", "required_columns": [state_col, reg_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    out = validate_required_columns(df, [state_col, reg_col]).copy()
    out = out.groupby(state_col, as_index=False)[reg_col].sum().rename(columns={reg_col: "state_registrations"})
    out["metric_type"] = "derived"
    return out


def oem_market_share(df: pd.DataFrame, oem_col: str = "oem_name", year_col: str = "year", reg_col: str = "e2w_registrations") -> pd.DataFrame | dict:
    """Market share by OEM. Requires official OEM volumes, not proxy-generated allocations."""
    status = market_status_for_verified_data({"metric_name": "OEM market share", "required_columns": [oem_col, year_col, reg_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validated = validate_required_columns(df, [oem_col, year_col, reg_col]).copy()
    totals = validated.groupby(year_col, as_index=False)[reg_col].sum().rename(columns={reg_col: "total_registrations"})
    merged = validated.merge(totals, on=year_col, how="left")
    merged["market_share_pct"] = (merged[reg_col] / merged["total_registrations"] * 100)
    merged["metric_type"] = "derived"
    return merged[[oem_col, year_col, reg_col, "market_share_pct", "metric_type"]]


def market_concentration_hhi(df: pd.DataFrame, oem_col: str = "oem_name", year_col: str = "year", share_col: str = "market_share_pct") -> pd.DataFrame | dict:
    """Herfindahl-Hirschman Index. Only valid when verified OEM share data is supplied."""
    status = market_status_for_verified_data({"metric_name": "HHI", "required_columns": [oem_col, year_col, share_col]}, df)
    if status["status"] != "AVAILABLE":
        return status
    validated = validate_required_columns(df, [oem_col, year_col, share_col]).copy()
    out = validated.groupby(year_col, as_index=False)[share_col].apply(lambda s: float((s ** 2).sum())).reset_index(name="hhi_index")
    out["metric_type"] = "derived"
    return out
