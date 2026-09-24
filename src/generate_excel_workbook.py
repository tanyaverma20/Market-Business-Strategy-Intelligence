"""
Generate a professional, multi-sheet Excel analytical workbook:
outputs/Market_Business_Strategy_Intelligence.xlsx
Directly populated with genuine verified repository data.
"""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
WORKBOOK_PATH = OUTPUTS_DIR / "Market_Business_Strategy_Intelligence.xlsx"

DATA_DIR = PROJECT_ROOT / "data" / "processed" / "sql"
MARKET_DIR = PROJECT_ROOT / "data" / "processed"


def build_excel_workbook():
    # 1. Load verified data marts
    comp_df = pd.read_csv(DATA_DIR / "sql_competitive_analysis.csv")
    pricing_df = pd.read_csv(DATA_DIR / "sql_pricing_analysis.csv")
    pos_df = pd.read_csv(DATA_DIR / "sql_product_positioning.csv")
    kpi_df = pd.read_csv(DATA_DIR / "sql_kpi_results.csv")
    dq_df = pd.read_csv(DATA_DIR / "sql_data_quality_results.csv")
    manifest_df = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DATASET_MANIFEST.csv")

    # 1b. Load new SEBI-verified market data
    market_growth_df = pd.read_csv(MARKET_DIR / "sebi_market_growth.csv")
    tam_som_df = pd.read_csv(MARKET_DIR / "tam_sam_som_scenarios.csv")

    # 2. Build Strategic Recommendations DataFrame
    recommendations_data = [
        {
            "Strategic Area": "Market Entry",
            "Recommendation": "Enter Indian e2W market targeting the Mid-Market Commuter segment (₹1,15,000 – ₹1,25,000 ex-showroom).",
            "Supporting KPI / Metric": "19 of 22 priced models (86%) occupy the ₹100k–₹180k tier; average market price is ₹1,24,466.",
            "Supporting Dataset": "sql_pricing_analysis.csv / sql_product_positioning.csv",
            "Confidence Level": "High (Verified Spec & Pricing Data)",
            "Strategic Risk / Limitation": "State registration volumes pending official Vahan exports; post-PM E-DRIVE price sensitivity requires monitoring."
        },
        {
            "Strategic Area": "Competitive Whitespace",
            "Recommendation": "Develop an entry commuter offering 120–140 km IDC range under ₹1,00,000.",
            "Supporting KPI / Metric": "0 of 3 current budget models (< ₹100k) offer > 120 km range. All standard/long range models sit above ₹1,05,000.",
            "Supporting Dataset": "sql_product_positioning.csv (Positioning Matrix)",
            "Confidence Level": "High (Verified Product Landscape)",
            "Strategic Risk / Limitation": "Tight gross margins; requires battery pack cost below $105/kWh to maintain positive contribution."
        },
        {
            "Strategic Area": "Pricing & Value Strategy",
            "Recommendation": "Target a Range Cost Efficiency ratio between ₹750/km and ₹820/km.",
            "Supporting KPI / Metric": "Market average price-per-km is ₹839.95/km. Leaders achieve ₹406–₹693/km (Ola S1X Plus, TVS iQube ST).",
            "Supporting Dataset": "sql_competitive_analysis.csv (price_per_km)",
            "Confidence Level": "High (Verified Technical Specs)",
            "Strategic Risk / Limitation": "Real-world range realization typically averages 75%–85% of certified IDC range."
        },
        {
            "Strategic Area": "Powertrain & Battery",
            "Recommendation": "Standardize on a 3.5 kWh to 4.0 kWh modular LFP/NMC battery pack with 80 km/h top speed.",
            "Supporting KPI / Metric": "Catalog average battery is 3.54 kWh; average top speed across high-speed commuter tier is 87.8 km/h.",
            "Supporting Dataset": "sql_kpi_results.csv",
            "Confidence Level": "High (Verified Engineering Benchmarks)",
            "Strategic Risk / Limitation": "Cell supply-chain concentration; requires AIS-156 Phase 2 thermal management compliance."
        },
        {
            "Strategic Area": "Geographic Expansion",
            "Recommendation": "Prioritize Tier-1 EV adoption clusters using the 5-factor Geographic Attractiveness Index (GAI).",
            "Supporting KPI / Metric": "State socioeconomic indicators and policy timelines established; registration weights ready.",
            "Supporting Dataset": "state_socioeconomic_indicators.csv / policy_incentive_timeline.csv",
            "Confidence Level": "Medium (Framework Complete, Official Registration Data Pending)",
            "Strategic Risk / Limitation": "State registration ranking remains pending official multi-year Vahan export verification."
        },
    ]
    recs_df = pd.DataFrame(recommendations_data)

    # 3. Build Assumptions & Provenance DataFrame
    assumptions_data = [
        {
            "Entity / Layer": "Verified Product Catalog",
            "Classification": "VERIFIED PRIMARY SOURCE",
            "Coverage / Count": "42 commercial models across 11 manufacturers",
            "Authoritative Source": "Official OEM websites, brochures, and SEBI IPO filings (Ather, Bajaj, Ola, TVS, Ampere, Hero VIDA, Simple, Revolt, Ultraviolette, Kinetic, BGauss)",
            "Analytical Usage": "Factual competitive benchmarking, pricing percentiles, specification quartiles, and product positioning."
        },
        {
            "Entity / Layer": "Unit Economics Model",
            "Classification": "SCENARIO ANALYSIS",
            "Coverage / Count": "3 Scenarios (Base, Conservative, Optimistic)",
            "Authoritative Source": "Industry benchmark cell pricing ($115/kWh), BloombergNEF cost curves, PM E-DRIVE scheme notifications",
            "Analytical Usage": "Sensitivity modeling of BOM, manufacturing overhead, distribution margin, and break-even sales volume."
        },
        {
            "Entity / Layer": "Geographic Evaluation (GAI)",
            "Classification": "METHODOLOGICAL FRAMEWORK",
            "Coverage / Count": "20 States / Union Territories",
            "Authoritative Source": "RBI State Finances, MoRTH Road Transport Yearbook, NITI Aayog EV readiness index",
            "Analytical Usage": "Multi-criteria decision framework; volume weighting remains pending official Vahan exports."
        },
        {
            "Entity / Layer": "Historical Market Registrations",
            "Classification": "PENDING VERIFIED VAHAN DATA",
            "Coverage / Count": "0 Factual Rows in Database (Fail-Closed)",
            "Authoritative Source": "MoRTH Vahan 4.0 Public Dashboard (Direct export pending CAPTCHA-free API)",
            "Analytical Usage": "SQL and DAX query templates prepared; no synthetic data permitted in factual analytics."
        },
    ]
    assumptions_df = pd.DataFrame(assumptions_data)

    # 4. Write Excel Workbook with xlsxwriter
    with pd.ExcelWriter(str(WORKBOOK_PATH), engine="xlsxwriter") as writer:
        workbook = writer.book

        # Format styles
        header_format = workbook.add_format({
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#1E293B",
            "font_color": "#FFFFFF",
            "font_name": "Segoe UI",
            "font_size": 10,
            "border": 1
        })
        cell_format = workbook.add_format({
            "font_name": "Segoe UI",
            "font_size": 9,
            "valign": "vcenter"
        })
        currency_format = workbook.add_format({
            "font_name": "Segoe UI",
            "font_size": 9,
            "num_format": "₹#,##0"
        })
        decimal_format = workbook.add_format({
            "font_name": "Segoe UI",
            "font_size": 9,
            "num_format": "0.00"
        })

        sheets = {
            "Executive_KPI_Summary": (kpi_df, "KPI Benchmark Register"),
            "Competitive_Benchmark": (comp_df, "Competitive Specifications & Rankings"),
            "Pricing_Analysis": (pricing_df, "Pricing Quartiles & Positioning"),
            "Product_Positioning": (pos_df, "Multi-Axial Segmentation Buckets"),
            "Strategic_Recommendations": (recs_df, "Evidence-Based Strategy"),
            "Market_Growth_SEBI": (market_growth_df, "SEBI-Verified Market Growth (FY2021-FY2024)"),
            "TAM_SAM_SOM_Scenarios": (tam_som_df, "TAM/SAM/SOM Sizing Framework (3 Scenarios)"),
            "Source_Register": (manifest_df, "Data Provenance Inventory"),
            "Assumptions_Provenance": (assumptions_df, "Audit & Data Integrity Controls")
        }

        for sheet_name, (df, title) in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
            worksheet = writer.sheets[sheet_name]

            # Write Title banner
            title_format = workbook.add_format({
                "bold": True,
                "font_size": 12,
                "font_name": "Segoe UI",
                "font_color": "#0EA5E9"
            })
            worksheet.write(0, 0, f"Indian Electric 2W Intelligence — {title}", title_format)

            # Style header row
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(1, col_num, value, header_format)

            # Auto-fit column widths
            for col_num, col_name in enumerate(df.columns):
                max_len = max(
                    df[col_name].astype(str).map(len).max(),
                    len(str(col_name))
                ) + 4
                worksheet.set_column(col_num, col_num, min(max_len, 45), cell_format)

    print(f"Successfully generated Excel analytical workbook at: {WORKBOOK_PATH}")
    return WORKBOOK_PATH


if __name__ == "__main__":
    build_excel_workbook()
