"""Validate and standardise local project data without inventing or downloading it.

Each processed row carries the provenance class in data/raw/DATASET_MANIFEST.csv.
Run: python src/data_processing.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analytics.geographic_analysis import compute_gai_template
from analytics.kpi_engine import generate_kpi_outputs
from analytics.positioning_analysis import build_product_positioning_summary
from analytics.scenario_analysis import build_scenario_analysis_template
from analytics.strategic_analysis import compute_competitive_intensity, compute_strategic_priority_score
from analytics.unit_economics import build_unit_economics_input_template, build_unit_economics_results_template

BASE = Path(__file__).resolve().parents[1]
RAW, OUT = BASE / "data" / "raw", BASE / "data" / "processed"
MANIFEST = RAW / "DATASET_MANIFEST.csv"

STATES = {
    "Andaman and Nicobar Islands":"AN", "Andhra Pradesh":"AP", "Arunachal Pradesh":"AR", "Assam":"AS", "Bihar":"BR", "Chandigarh":"CH", "Chhattisgarh":"CG", "Dadra and Nagar Haveli and Daman and Diu":"DH", "Delhi":"DL", "Goa":"GA", "Gujarat":"GJ", "Haryana":"HR", "Himachal Pradesh":"HP", "Jammu and Kashmir":"JK", "Jharkhand":"JH", "Karnataka":"KA", "Kerala":"KL", "Ladakh":"LA", "Lakshadweep":"LD", "Madhya Pradesh":"MP", "Maharashtra":"MH", "Manipur":"MN", "Meghalaya":"ML", "Mizoram":"MZ", "Nagaland":"NL", "Odisha":"OR", "Puducherry":"PY", "Punjab":"PB", "Rajasthan":"RJ", "Sikkim":"SK", "Tamil Nadu":"TN", "Telangana":"TS", "Tripura":"TR", "Uttar Pradesh":"UP", "Uttarakhand":"UK", "West Bengal":"WB"
}
ALIASES = {"Orissa":"Odisha", "Pondicherry":"Puducherry", "Uttaranchal":"Uttarakhand"}
SCHEMAS = {
    "vahan_e2w_registrations_monthly.csv": ["year","month","year_month","state","state_code","e2w_registrations","total_2w_registrations","data_source"],
    "oem_e2w_registrations_annual.csv": ["year","oem_name","oem_category","e2w_registrations","data_source"],
    "competitor_product_catalog.csv": ["manufacturer","model_name","product_category","ex_showroom_price_inr","battery_capacity_kwh","certified_idc_range_km","data_source"],
    "state_socioeconomic_indicators.csv": ["state","state_code","population_2024_est_millions","data_source"],
    "policy_incentive_timeline.csv": ["policy_scheme","start_date","end_date","data_source"],
    "verified_product_catalog_2025_2026.csv": ["manufacturer","model_name","source_url","source_type","accessed_date","verification_status"],
}

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def audit(dataset, df, meta):
    required = SCHEMAS[dataset]
    return {"dataset":dataset, "provenance_class":meta.provenance_class,
            "eligible_as_observed_analytics":meta.eligible_as_observed_analytics,
            "rows":len(df), "sha256":digest(RAW/dataset),
            "missing_required_columns":[x for x in required if x not in df],
            "duplicate_full_rows":int(df.duplicated().sum()),
            "missing_values":{k:int(v) for k,v in df.isna().sum().items() if v},
            "errors":[], "warnings":[]}

def numeric(df, columns, report):
    for col in columns:
        values = pd.to_numeric(df[col], errors="coerce")
        bad = int(values.isna().sum() + (values < 0).sum())
        if bad: report["errors"].append(f"{col}: {bad} missing, non-numeric, or negative values")
        df[col] = values

def optional_numeric(df, columns, report):
    """Convert optional numeric specification fields without treating an absent source value as zero/error."""
    for col in columns:
        original = df[col]
        values = pd.to_numeric(original, errors="coerce")
        supplied = original.notna() & original.astype(str).str.strip().ne("")
        bad = int((supplied & values.isna()).sum() + (values < 0).sum())
        if bad: report["errors"].append(f"{col}: {bad} non-numeric or negative supplied values")
        df[col] = values

def standardise_states(df, report):
    df = df.copy(); df["state"] = df.state.astype("string").str.strip().replace(ALIASES)
    unknown = sorted(df.loc[~df.state.isin(STATES), "state"].dropna().unique())
    if unknown: report["errors"].append(f"unrecognised state names: {unknown}")
    expected = df.state.map(STATES)
    mismatch = int((expected.notna() & (df.state_code.astype("string").str.upper() != expected)).sum())
    if mismatch: report["errors"].append(f"state code mismatch: {mismatch} rows")
    df["state_code"] = expected.fillna(df.state_code).astype("string").str.upper()
    return df

def vahan(df, report):
    numeric(df, ["e2w_registrations","total_2w_registrations"], report)
    if df.duplicated(["year","month","state"]).any(): report["errors"].append("duplicate year/month/state keys")
    df = standardise_states(df, report)
    dates = pd.to_datetime(df.year_month.astype(str)+"-01", format="%Y-%m-%d", errors="coerce")
    mismatch = ((dates.dt.year != df.year) | (dates.dt.month != df.month)).fillna(False)
    bad = int(dates.isna().sum() + (~df.month.between(1,12)).sum() + (~df.year.between(1900,2100)).sum() + mismatch.sum())
    if bad: report["errors"].append(f"invalid date/year/month values: {bad}")
    if (df.e2w_registrations > df.total_2w_registrations).any(): report["errors"].append("e2w registrations exceed total 2W registrations")
    df["date"] = dates
    df["ev_penetration_pct"] = np.where(df.total_2w_registrations > 0, (df.e2w_registrations / df.total_2w_registrations * 100).round(4), np.nan)
    return df.sort_values(["state","date"])

def oem(df, report):
    numeric(df, ["e2w_registrations"], report)
    if df.duplicated(["year","oem_name"]).any(): report["errors"].append("duplicate year/OEM keys")
    df.oem_name = df.oem_name.astype("string").str.strip()
    df["market_share_pct"] = (df.e2w_registrations / df.groupby("year").e2w_registrations.transform("sum") * 100).round(4)
    return df.sort_values(["year","market_share_pct","oem_name"], ascending=[True,False,True])

def specs(df, report):
    cols = [c for c in ["ex_showroom_price_inr","battery_capacity_kwh","certified_idc_range_km","real_world_range_km","top_speed_kmh","motor_peak_power_kw","charging_time_hours_0_80"] if c in df]
    numeric(df, cols, report)
    if df.duplicated(["manufacturer","model_name"]).any(): report["errors"].append("duplicate manufacturer/model keys")
    df.manufacturer, df.model_name = df.manufacturer.astype("string").str.strip(), df.model_name.astype("string").str.strip()
    df["price_to_certified_range_ratio"] = (df.ex_showroom_price_inr / df.certified_idc_range_km).round(2)
    return df.sort_values(["manufacturer","model_name"])

def states(df, report):
    df = standardise_states(df, report)
    cols = [c for c in ["population_2024_est_millions","urbanization_pct","per_capita_nsdp_inr","est_annual_total_2w_volume","public_charging_stations_count","road_tax_exemption_pct","subsidy_capital_support_score"] if c in df]
    numeric(df, cols, report)
    if df.duplicated("state").any(): report["errors"].append("duplicate state keys")
    return df.sort_values("state")

def policies(df, report):
    start, end = pd.to_datetime(df.start_date, errors="coerce"), pd.to_datetime(df.end_date, errors="coerce")
    if int(start.isna().sum()+end.isna().sum()+(end<start).sum()): report["errors"].append("invalid policy start/end dates")
    df["start_date"], df["end_date"] = start.dt.date, end.dt.date
    return df.sort_values("start_date")

def verified_products(df, report):
    optional_numeric(df, [c for c in ["ex_showroom_price_inr","battery_capacity_kwh","range_km","top_speed_kmh","motor_peak_power_kw"] if c in df], report)
    if df.duplicated(["manufacturer","model_name"]).any(): report["errors"].append("duplicate manufacturer/model keys")
    dates = pd.to_datetime(df.accessed_date, format="%Y-%m-%d", errors="coerce")
    if dates.isna().any(): report["errors"].append("invalid accessed_date")
    if (df.verification_status != "verified").any(): report["errors"].append("verified catalog contains non-verified rows")
    return df.sort_values(["manufacturer","model_name"])


def process_all():
    OUT.mkdir(exist_ok=True)
    manifest = pd.read_csv(MANIFEST).set_index("dataset_name")
    jobs = {
        "vahan_e2w_registrations_monthly.csv": (vahan, "processed_vahan_monthly.csv"),
        "oem_e2w_registrations_annual.csv": (oem, "processed_oem_market_shares.csv"),
        "competitor_product_catalog.csv": (specs, "processed_competitor_specs.csv"),
        "state_socioeconomic_indicators.csv": (states, "processed_state_indicators.csv"),
        "policy_incentive_timeline.csv": (policies, "processed_policy_timeline.csv"),
        "verified_product_catalog_2025_2026.csv": (verified_products, "processed_verified_product_catalog.csv"),
    }
    reports = []
    for name, (transform, output) in jobs.items():
        frame = pd.read_csv(RAW / name)
        report = audit(name, frame, manifest.loc[name])
        if report["missing_required_columns"]:
            report["errors"].append("not processed: required columns absent")
            reports.append(report)
            continue
        frame = transform(frame, report)
        frame["source_dataset"], frame["provenance_class"], frame["eligible_as_observed_analytics"] = name, manifest.loc[name, "provenance_class"], manifest.loc[name, "eligible_as_observed_analytics"]
        frame.to_csv(OUT / output, index=False)
        reports.append(report)

    product_df = pd.read_csv(OUT / "processed_verified_product_catalog.csv")
    oem_data = pd.read_csv(OUT / "processed_oem_market_shares.csv")
    hhi = oem_data.groupby(["year", "provenance_class", "eligible_as_observed_analytics"], as_index=False).agg(
        hhi_index=("market_share_pct", lambda x: round((x ** 2).sum(), 2)),
        total_oems=("oem_name", "nunique"),
    )
    hhi.to_csv(OUT / "processed_market_hhi.csv", index=False)
    geo_template = pd.DataFrame(
        [{"state": "state_name", "market_size": None, "ev_penetration": None, "growth": None, "purchasing_power": None, "charging_infrastructure": None, "policy_score": None, "status": "PENDING VERIFIED DATA"}]
    )
    geo_template.to_csv(OUT / "geographic_scoring_template.csv", index=False)
    unit_input_template = build_unit_economics_input_template()
    unit_input_template.to_csv(OUT / "unit_economics_input_template.csv", index=False)
    unit_results_template = build_unit_economics_results_template()
    unit_results_template.to_csv(OUT / "unit_economics_results.csv", index=False)
    strategic_template = compute_strategic_priority_score(pd.DataFrame([{"market_attractiveness": None, "competitive_intensity": None, "product_market_fit": None, "geographic_attractiveness": None}]))
    strategic_template.to_csv(OUT / "strategic_priority_template.csv", index=False)
    scenario_template = build_scenario_analysis_template()
    scenario_template.to_csv(OUT / "scenario_analysis_template.csv", index=False)
    competitive_intensity = compute_competitive_intensity(product_df)
    competitive_intensity.to_csv(OUT / "competitive_intensity.csv", index=False)
    product_positioning = build_product_positioning_summary(product_df)
    product_positioning.to_csv(OUT / "product_positioning.csv", index=False)
    generate_kpi_outputs(product_df, OUT)
    (OUT / "validation_results.json").write_text(json.dumps({"generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(), "datasets": reports}, indent=2), encoding="utf-8")
    print(f"Processed {len(reports)} datasets. Validation errors: {sum(len(r['errors']) for r in reports)}")
    return reports


if __name__ == "__main__": process_all()
