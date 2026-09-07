"""
data_processing.py
------------------
Reproducible Data Acquisition, Validation, and Preprocessing Engine
for the Indian Electric 2-Wheeler (e2W) Market Intelligence Project.

Author: Strategy & Data Analytics Team
Project: Market-Business-Strategy-Intelligence
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List

# Define Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def ensure_directories():
    """Ensure all required project directories exist."""
    for path in [DATA_RAW_DIR, DATA_PROC_DIR, DOCS_DIR]:
        os.makedirs(path, exist_ok=True)


def validate_schema(df: pd.DataFrame, expected_columns: List[str], df_name: str) -> bool:
    """Validate that dataframe contains expected columns."""
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        print(f"[WARNING] {df_name} missing expected columns: {missing}")
        return False
    print(f"[OK] {df_name} schema validation passed ({len(df.columns)} columns).")
    return True


def audit_dataframe(df: pd.DataFrame, df_name: str) -> Dict:
    """Generate comprehensive audit metrics for a dataframe."""
    null_counts = df.isnull().sum().to_dict()
    duplicate_rows = df.duplicated().sum()
    data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    return {
        "dataset_name": df_name,
        "row_count": len(df),
        "col_count": len(df.columns),
        "duplicate_rows": int(duplicate_rows),
        "null_counts": null_counts,
        "data_types": data_types
    }


def clean_vahan_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess Vahan monthly registration data."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["year_month"] + "-01")
    df["e2w_registrations"] = pd.to_numeric(df["e2w_registrations"], errors="coerce").fillna(0).astype(int)
    df["total_2w_registrations"] = pd.to_numeric(df["total_2w_registrations"], errors="coerce").fillna(0).astype(int)
    
    # Derived penetration rate
    df["ev_penetration_pct"] = np.where(
        df["total_2w_registrations"] > 0,
        (df["e2w_registrations"] / df["total_2w_registrations"]) * 100,
        0.0
    ).round(2)
    
    return df.sort_values(by=["state", "date"]).reset_index(drop=True)


def clean_oem_registrations(df: pd.DataFrame) -> pd.DataFrame:
    """Clean OEM registration data and compute annual market shares & HHI."""
    df = df.copy()
    df["e2w_registrations"] = pd.to_numeric(df["e2w_registrations"], errors="coerce").fillna(0).astype(int)
    
    # Calculate annual market shares
    annual_totals = df.groupby("year")["e2w_registrations"].transform("sum")
    df["market_share_pct"] = np.where(
        annual_totals > 0,
        (df["e2w_registrations"] / annual_totals) * 100,
        0.0
    ).round(2)
    
    return df.sort_values(by=["year", "market_share_pct"], ascending=[True, False]).reset_index(drop=True)


def compute_hhi_series(oem_df: pd.DataFrame) -> pd.DataFrame:
    """Compute Herfindahl-Hirschman Index (HHI) for market concentration by year."""
    hhi_list = []
    for year, group in oem_df.groupby("year"):
        hhi = (group["market_share_pct"] ** 2).sum()
        hhi_list.append({"year": year, "hhi_index": round(hhi, 2), "total_oems": len(group)})
    return pd.DataFrame(hhi_list)


def clean_competitor_specs(df: pd.DataFrame) -> pd.DataFrame:
    """Clean competitor vehicle catalog and compute commercial ratios."""
    df = df.copy()
    numeric_cols = [
        "ex_showroom_price_inr", "battery_capacity_kwh", "certified_idc_range_km",
        "real_world_range_km", "top_speed_kmh", "motor_peak_power_kw", "charging_time_hours_0_80"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    # Price to Range ratio (INR / km)
    df["price_to_certified_range_ratio"] = (df["ex_showroom_price_inr"] / df["certified_idc_range_km"]).round(2)
    df["price_to_real_range_ratio"] = (df["ex_showroom_price_inr"] / df["real_world_range_km"]).round(2)
    
    # Price to Battery ratio (INR / kWh)
    df["price_to_battery_kwh_ratio"] = (df["ex_showroom_price_inr"] / df["battery_capacity_kwh"]).round(2)
    
    # Real-world range efficiency factor (%)
    df["range_realization_pct"] = ((df["real_world_range_km"] / df["certified_idc_range_km"]) * 100).round(1)
    
    # PM E-DRIVE Subsidy estimation (FY25: ₹5,000/kWh up to ₹10,000 max)
    df["pm_edrive_subsidy_fy25_inr"] = np.minimum(df["battery_capacity_kwh"] * 5000, 10000).round(0)
    df["effective_price_post_subsidy_fy25_inr"] = df["ex_showroom_price_inr"] - df["pm_edrive_subsidy_fy25_inr"]
    
    return df.sort_values(by=["ex_showroom_price_inr"]).reset_index(drop=True)


def clean_state_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Clean state socio-economic and charging infra indicators."""
    df = df.copy()
    num_cols = ["population_2024_est_millions", "urbanization_pct", "per_capita_nsdp_inr",
                "est_annual_total_2w_volume", "public_charging_stations_count",
                "road_tax_exemption_pct", "subsidy_capital_support_score"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    # Derived ratio: Charging stations per million population
    df["charging_stations_per_million_pop"] = np.where(
        df["population_2024_est_millions"] > 0,
        (df["public_charging_stations_count"] / df["population_2024_est_millions"]),
        0.0
    ).round(2)
    
    return df.sort_values(by="per_capita_nsdp_inr", ascending=False).reset_index(drop=True)


def process_all():
    """Main pipeline execution function."""
    ensure_directories()
    print("=" * 60)
    print("EXECUTING PHASE 1 DATA PROCESSING & PIPELINE VALIDATION")
    print("=" * 60)
    
    audits = []
    
    # 1. Monthly Vahan Data
    vahan_raw_path = os.path.join(DATA_RAW_DIR, "vahan_e2w_registrations_monthly.csv")
    if os.path.exists(vahan_raw_path):
        df_vahan_raw = pd.read_csv(vahan_raw_path)
        audits.append(audit_dataframe(df_vahan_raw, "vahan_e2w_registrations_monthly"))
        df_vahan_proc = clean_vahan_monthly(df_vahan_raw)
        df_vahan_proc.to_csv(os.path.join(DATA_PROC_DIR, "processed_vahan_monthly.csv"), index=False)
        print(f"[SUCCESS] Processed Vahan Monthly: {len(df_vahan_proc)} records saved.")
    
    # 2. OEM Registrations
    oem_raw_path = os.path.join(DATA_RAW_DIR, "oem_e2w_registrations_annual.csv")
    if os.path.exists(oem_raw_path):
        df_oem_raw = pd.read_csv(oem_raw_path)
        audits.append(audit_dataframe(df_oem_raw, "oem_e2w_registrations_annual"))
        df_oem_proc = clean_oem_registrations(df_oem_raw)
        df_oem_proc.to_csv(os.path.join(DATA_PROC_DIR, "processed_oem_market_shares.csv"), index=False)
        
        # HHI index
        df_hhi = compute_hhi_series(df_oem_proc)
        df_hhi.to_csv(os.path.join(DATA_PROC_DIR, "processed_market_hhi.csv"), index=False)
        print(f"[SUCCESS] Processed OEM Market Shares: {len(df_oem_proc)} records saved. HHI computed.")

    # 3. Competitor Specs
    specs_raw_path = os.path.join(DATA_RAW_DIR, "competitor_product_catalog.csv")
    if os.path.exists(specs_raw_path):
        df_specs_raw = pd.read_csv(specs_raw_path)
        audits.append(audit_dataframe(df_specs_raw, "competitor_product_catalog"))
        df_specs_proc = clean_competitor_specs(df_specs_raw)
        df_specs_proc.to_csv(os.path.join(DATA_PROC_DIR, "processed_competitor_specs.csv"), index=False)
        print(f"[SUCCESS] Processed Competitor Product Catalog: {len(df_specs_proc)} records saved.")

    # 4. State Socioeconomic Indicators
    state_raw_path = os.path.join(DATA_RAW_DIR, "state_socioeconomic_indicators.csv")
    if os.path.exists(state_raw_path):
        df_state_raw = pd.read_csv(state_raw_path)
        audits.append(audit_dataframe(df_state_raw, "state_socioeconomic_indicators"))
        df_state_proc = clean_state_indicators(df_state_raw)
        df_state_proc.to_csv(os.path.join(DATA_PROC_DIR, "processed_state_indicators.csv"), index=False)
        print(f"[SUCCESS] Processed State Socioeconomic Indicators: {len(df_state_proc)} records saved.")

    # 5. Policy Timeline
    policy_raw_path = os.path.join(DATA_RAW_DIR, "policy_incentive_timeline.csv")
    if os.path.exists(policy_raw_path):
        df_policy_raw = pd.read_csv(policy_raw_path)
        audits.append(audit_dataframe(df_policy_raw, "policy_incentive_timeline"))
        df_policy_raw.to_csv(os.path.join(DATA_PROC_DIR, "processed_policy_timeline.csv"), index=False)
        print(f"[SUCCESS] Processed Policy Timeline: {len(df_policy_raw)} records saved.")

    print("=" * 60)
    print("DATA PROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    return audits


if __name__ == "__main__":
    process_all()
