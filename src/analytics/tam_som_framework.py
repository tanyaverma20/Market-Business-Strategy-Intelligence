from __future__ import annotations
import pandas as pd

SEBI_VERIFIED_FY2024_INDUSTRY_UNITS = 944_000
SEBI_VERIFIED_SOURCE = "Ola Electric Mobility Limited RHP (August 2024) - SEBI statutory filing"
SEBI_VERIFIED_SECTION = "Industry Overview - CRISIL Market Research cited in prospectus"
SEBI_VERIFIED_COVERAGE = "India national e2W total, fiscal year ending March 2024"

TAM_ASSUMPTIONS = {
    "base": {
        "label": "Base Case",
        "description": "Moderate growth; PM E-DRIVE scheme operational",
        "verified_fy2024_units": SEBI_VERIFIED_FY2024_INDUSTRY_UNITS,
        "fy2025_growth_assumption_pct": 25.0,
        "fy2025_assumption_label": "ASSUMPTION - FY21-24 CAGR trend implies ~25% deceleration; NOT verified by Vahan",
        "avg_price_per_unit_inr": 124_466,
        "avg_price_source": "Verified product catalog mean - verified_product_catalog_2025_2026.csv",
    },
    "conservative": {
        "label": "Conservative Case",
        "description": "Slower adoption: policy delays, subsidy uncertainty",
        "verified_fy2024_units": SEBI_VERIFIED_FY2024_INDUSTRY_UNITS,
        "fy2025_growth_assumption_pct": 10.0,
        "fy2025_assumption_label": "ASSUMPTION - conservative scenario",
        "avg_price_per_unit_inr": 120_000,
        "avg_price_source": "Conservative assumption - slightly below catalog average",
    },
    "upside": {
        "label": "Upside Case",
        "description": "Strong adoption: PM E-DRIVE full deployment, grid expansion",
        "verified_fy2024_units": SEBI_VERIFIED_FY2024_INDUSTRY_UNITS,
        "fy2025_growth_assumption_pct": 45.0,
        "fy2025_assumption_label": "ASSUMPTION - upside scenario",
        "avg_price_per_unit_inr": 130_000,
        "avg_price_source": "Upside assumption - premium product mix enrichment",
    },
}

SAM_ASSUMPTIONS = {
    "base": {
        "label": "Base SAM",
        "geographic_concentration_pct": 70.0,
        "geographic_assumption_label": "ASSUMPTION - top 10 states approx 70%; state-level Vahan not available",
        "segment_concentration_pct": 80.0,
        "segment_assumption_label": "ASSUMPTION - mid-market approx 80%; anchored to verified catalog (76%)",
    },
    "conservative": {
        "label": "Conservative SAM",
        "geographic_concentration_pct": 60.0,
        "geographic_assumption_label": "ASSUMPTION - conservative; 8 states",
        "segment_concentration_pct": 70.0,
        "segment_assumption_label": "ASSUMPTION - conservative mid-market capture",
    },
    "upside": {
        "label": "Upside SAM",
        "geographic_concentration_pct": 80.0,
        "geographic_assumption_label": "ASSUMPTION - upside; 12 states",
        "segment_concentration_pct": 85.0,
        "segment_assumption_label": "ASSUMPTION - upside mid-market plus premium",
    },
}

SOM_ASSUMPTIONS = {
    "base": {
        "label": "Base SOM",
        "attainable_share_pct": 3.0,
        "share_assumption_label": "ASSUMPTION - 3% SAM share Year 3; new entrant benchmark",
        "timeline_years": 3,
    },
    "conservative": {
        "label": "Conservative SOM",
        "attainable_share_pct": 1.5,
        "share_assumption_label": "ASSUMPTION - 1.5% SAM share Year 3",
        "timeline_years": 3,
    },
    "upside": {
        "label": "Upside SOM",
        "attainable_share_pct": 5.0,
        "share_assumption_label": "ASSUMPTION - 5% SAM share Year 3",
        "timeline_years": 3,
    },
}


def compute_tam(scenario="base"):
    if scenario not in TAM_ASSUMPTIONS:
        raise ValueError(f"Unknown scenario: {scenario}")
    p = TAM_ASSUMPTIONS[scenario]
    units = int(p["verified_fy2024_units"] * (1 + p["fy2025_growth_assumption_pct"] / 100))
    revenue = units * p["avg_price_per_unit_inr"]
    return {
        "scenario": p["label"], "description": p["description"], "metric": "TAM",
        "tam_units": units, "tam_revenue_inr": revenue,
        "tam_revenue_inr_crore": round(revenue / 1e7, 1),
        "verified_anchor": {
            "fy2024_industry_units": p["verified_fy2024_units"],
            "source": SEBI_VERIFIED_SOURCE,
            "data_classification": "OBSERVED - SEBI statutory filing",
        },
        "assumptions": {
            "fy2025_growth_pct": p["fy2025_growth_assumption_pct"],
            "growth_basis": p["fy2025_assumption_label"],
            "avg_price_per_unit_inr": p["avg_price_per_unit_inr"],
            "price_basis": p["avg_price_source"],
            "data_classification": "ASSUMPTION",
        },
    }


def compute_sam(scenario="base", tam_units=None):
    if scenario not in SAM_ASSUMPTIONS:
        raise ValueError(f"Unknown scenario: {scenario}")
    tam = compute_tam(scenario)
    units = tam_units if tam_units is not None else tam["tam_units"]
    p = SAM_ASSUMPTIONS[scenario]
    sam_units = int(units * p["geographic_concentration_pct"] / 100 * p["segment_concentration_pct"] / 100)
    avg_price = TAM_ASSUMPTIONS[scenario]["avg_price_per_unit_inr"]
    return {
        "scenario": p["label"], "metric": "SAM",
        "sam_units": sam_units, "sam_revenue_inr": sam_units * avg_price,
        "sam_revenue_inr_crore": round(sam_units * avg_price / 1e7, 1), "tam_units": units,
        "assumptions": {
            "geographic_concentration_pct": p["geographic_concentration_pct"],
            "geographic_basis": p["geographic_assumption_label"],
            "segment_concentration_pct": p["segment_concentration_pct"],
            "segment_basis": p["segment_assumption_label"],
            "data_classification": "ASSUMPTION",
        },
    }


def compute_som(scenario="base", sam_units=None):
    if scenario not in SOM_ASSUMPTIONS:
        raise ValueError(f"Unknown scenario: {scenario}")
    sam = compute_sam(scenario)
    units = sam_units if sam_units is not None else sam["sam_units"]
    p = SOM_ASSUMPTIONS[scenario]
    som_units = int(units * p["attainable_share_pct"] / 100)
    avg_price = TAM_ASSUMPTIONS[scenario]["avg_price_per_unit_inr"]
    return {
        "scenario": p["label"], "metric": "SOM",
        "som_units": som_units, "som_revenue_inr": som_units * avg_price,
        "som_revenue_inr_crore": round(som_units * avg_price / 1e7, 1), "sam_units": units,
        "assumptions": {
            "attainable_share_pct": p["attainable_share_pct"],
            "share_basis": p["share_assumption_label"],
            "timeline_years": p["timeline_years"],
            "data_classification": "ASSUMPTION",
        },
    }


def build_tam_sam_som_table():
    rows = []
    for scenario in ["conservative", "base", "upside"]:
        tam = compute_tam(scenario)
        sam = compute_sam(scenario, tam_units=tam["tam_units"])
        som = compute_som(scenario, sam_units=sam["sam_units"])
        rows.append({
            "scenario": tam["scenario"], "description": tam["description"],
            "verified_fy2024_industry_units": SEBI_VERIFIED_FY2024_INDUSTRY_UNITS,
            "verified_source": SEBI_VERIFIED_SOURCE,
            "fy2025_growth_assumption_pct": TAM_ASSUMPTIONS[scenario]["fy2025_growth_assumption_pct"],
            "tam_units": tam["tam_units"], "tam_revenue_inr_crore": tam["tam_revenue_inr_crore"],
            "geographic_concentration_pct": SAM_ASSUMPTIONS[scenario]["geographic_concentration_pct"],
            "segment_concentration_pct": SAM_ASSUMPTIONS[scenario]["segment_concentration_pct"],
            "sam_units": sam["sam_units"], "sam_revenue_inr_crore": sam["sam_revenue_inr_crore"],
            "attainable_share_pct": SOM_ASSUMPTIONS[scenario]["attainable_share_pct"],
            "som_units": som["som_units"], "som_revenue_inr_crore": som["som_revenue_inr_crore"],
            "avg_price_per_unit_inr": TAM_ASSUMPTIONS[scenario]["avg_price_per_unit_inr"],
            "data_classification_tam": "OBSERVED (FY24) + ASSUMPTION (growth)",
            "data_classification_sam": "ASSUMPTION", "data_classification_som": "ASSUMPTION",
            "methodology_version": "v1.0 - 2026-09-24",
        })
    return pd.DataFrame(rows)


def build_sebi_market_growth_table():
    sebi_data = [
        {"fiscal_year": "FY2021", "calendar_year_end": 2021, "industry_e2w_units": 41000,
         "data_classification": "OBSERVED - SEBI RHP 2024"},
        {"fiscal_year": "FY2022", "calendar_year_end": 2022, "industry_e2w_units": 249000,
         "data_classification": "OBSERVED - SEBI RHP 2024"},
        {"fiscal_year": "FY2023", "calendar_year_end": 2023, "industry_e2w_units": 728000,
         "data_classification": "OBSERVED - SEBI RHP 2024"},
        {"fiscal_year": "FY2024", "calendar_year_end": 2024, "industry_e2w_units": 944000,
         "data_classification": "OBSERVED - SEBI RHP 2024"},
    ]
    df = pd.DataFrame(sebi_data)
    df["yoy_growth_pct"] = df["industry_e2w_units"].pct_change() * 100
    df["yoy_growth_pct"] = df["yoy_growth_pct"].round(1)
    start = df.iloc[0]["industry_e2w_units"]
    end = df.iloc[-1]["industry_e2w_units"]
    years = df.iloc[-1]["calendar_year_end"] - df.iloc[0]["calendar_year_end"]
    cagr = round(((end / start) ** (1 / years) - 1) * 100, 1)
    df["cagr_fy2021_fy2024_pct"] = cagr
    df["source"] = SEBI_VERIFIED_SOURCE
    df["provenance_status"] = "verified_primary_source"
    df["coverage_note"] = "National India e2W total; state-level breakdown not available from this source"
    return df


__all__ = [
    "compute_tam", "compute_sam", "compute_som",
    "build_tam_sam_som_table", "build_sebi_market_growth_table",
    "SEBI_VERIFIED_FY2024_INDUSTRY_UNITS", "SEBI_VERIFIED_SOURCE",
    "TAM_ASSUMPTIONS", "SAM_ASSUMPTIONS", "SOM_ASSUMPTIONS",
]
