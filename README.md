# Market-Business-Strategy-Intelligence

A verified commercial strategy and competitive intelligence platform for the Indian electric two-wheeler market. The repository combines primary-source product intelligence with Python analytics, DuckDB SQL, Excel workbook outputs, and a repaired, fully operational Power BI dashboard.

> Final status: The project is functionally complete as an end-to-end commercial strategy and competitive intelligence platform. Verified product intelligence is in place across 11 manufacturers and 42 commercial models. Historical Vahan registration data remains intentionally pending and fail-closed; registration-dependent metrics are not represented as verified market-share data.

---

## 1. Executive Summary

The repository is designed to answer the questions that matter to a market entrant, commercial strategy team, or business analyst evaluating the Indian electric two-wheeler segment:

- Which manufacturers and product models are active in the verified catalog?
- How concentrated is the current product portfolio?
- Where are the price and value clusters across real catalog offerings?
- Which product segments show whitespace or strategic opportunity?
- How should pricing, battery capacity, and certified range be benchmarked?
- Which metrics are verified, and which remain intentionally pending due to governance constraints?

The project delivers a fully auditable workflow from verified OEM product records to Python analysis, DuckDB marts, Excel outputs, and a 5-page Power BI dashboard. It is intentionally designed to avoid replacing missing market-registration data with proxy metrics or synthetic estimates.

---

## 2. Business Problem and Objectives

### Business problem
The Indian electric two-wheeler market is a dynamic commercial environment with many price points, battery capacities, certified ranges, and competitor strategies. Decision-makers need a defensible benchmark of the real catalog landscape without relying on unverified registration data or fabricated market-share claims.

### Objectives
- Benchmark the verified product catalog across 11 manufacturers and 42 models.
- Quantify pricing, value, and portfolio concentration using evidence-backed metrics.
- Identify product positioning and whitespace across the catalog.
- Produce a usable strategic and analytical framework for pricing and market entry.
- Maintain strict data provenance and fail-closed governance for pending registration-dependent metrics.

---

## 3. Verified Product Catalog Scope

The final verified catalog is based on OEM and catalog sources and is not described as historical transaction data.

Verified current scope:
- 42 commercial electric two-wheeler models
- 11 manufacturers
- 34 priced products

This project does not claim inclusion of verified multi-year Vahan registration data. The registration layer remains intentionally pending/fail-closed.

---

## 4. Key Verified Results

| Metric | Result |
|---|---:|
| Verified Manufacturers | 11 |
| Verified Commercial Models | 42 |
| Priced Products | 34 |
| Minimum Price | ₹74,990 |
| Median Price | approximately ₹1,26,171 |
| Average Price | approximately ₹1,36,349 |
| Maximum Price | ₹3,99,000 |
| Average Certified Range | approximately 159.4 km |
| Average Battery Capacity | approximately 3.73 kWh |
| Average Price per KM | approximately ₹867.71/km |
| Product Portfolio HHI | approximately 1,326.53 |
| SEBI-Verified Historical Industry Totals | 4 Fiscal Years (FY21: 41k, FY22: 249k, FY23: 728k, FY24: 944k) |
| SEBI 3-Year Industry CAGR (FY21-FY24) | 184.5% |
| TAM / SAM / SOM Sizing Scenarios | 3 (Conservative, Base, Upside) |
| DAX Measures | 35 |
| Power BI Pages | 5 |
| Visual Containers | 39 |
| Automated Tests | 57 passed (100%) |
| PBIP Integrity Checks | 14/14 passed |

The values above are aligned with the current processed catalog and validated repository outputs.

---

## 5. Data Sources and Provenance

The repository is intentionally strict about source provenance.

### Verified data sources
- **SEBI Statutory Filings:** *Ola Electric Mobility Limited — Red Herring Prospectus (RHP, August 2024)*, citing CRISIL Market Research Report filed with SEBI. Covers national e2W annual industry totals (FY2021–FY2024).
- **Verified OEM Product Catalog:** Official OEM product pages, brochures, and press releases for 42 commercial models across 11 manufacturers with row-level source URLs.
- **ARAI / Certified Disclosures:** Specification disclosures cited by official manufacturer releases.

### Governance boundary & Fail-Closed Safeguards
- Official state-level registration series and granular multi-year Vahan records are **not** publicly exportable via automated CAPTCHA-free APIs. Therefore:
  - Industry-level market volume (FY21–FY24): **VERIFIED**
  - 10+ years coverage: **NOT VERIFIED** (authoritatively bounded to 4 fiscal years)
  - 20+ states registration data: **NOT VERIFIED** (national totals only)
  - OEM registration market share: **NOT VERIFIED** (pending verified OEM volume series)
  - State registration trends: **NOT VERIFIED**
- State-registration-dependent GAI components and the 10 registration-dependent DAX measures remain strictly **BLANK()** and fail-closed.
- No proxy registration numbers or deprecated proxy files (`vahan_e2w_registrations_monthly.csv`, `oem_e2w_registrations_annual.csv`, `state_socioeconomic_indicators.csv`) are ever relabeled as official data or used in factual rankings.

### Quarantined data
Legacy proxy datasets are retained only with `PROXY_DEPRECATED` classification and are prohibited from factual analysis.

---

## 6. Architecture and Workflow

The repository is implemented as an end-to-end commercial intelligence workflow:

Raw verified OEM product data
→ Python data processing and analytical engine
→ DuckDB SQL analytical warehouse
→ analytical CSV marts
→ Excel analytical workbook
→ Power BI semantic model and Power Query
→ DAX measures
→ 5-page interactive Power BI dashboard
→ strategic business insights

This pipeline is deterministic, auditable, and designed to maintain clear boundaries between verified catalog metrics and deferred registration metrics.

---

## 7. SQL / DuckDB Layer

The SQL warehouse is implemented with DuckDB and is used to transform cleaned product records into analytical marts and governance-aware KPI views.

### Current pricing mart schema
The current pricing schema in the final repository is 17 columns and is reflected in `data/processed/sql/sql_pricing_analysis.csv`:

- product
- manufacturer
- price
- battery_capacity_kwh
- range_km
- top_speed_kmh
- price_per_km
- price_per_kwh
- price_bucket
- value_rank
- price_percentile
- price_quartile
- product_price_rank
- avg_market_price
- mfg_avg_price
- relative_price_position
- price_premium_vs_market_pct

This is the schema currently reflected in the data and should be used for documentation and reporting instead of older schema references.

---

## 8. Excel Layer

The Excel workbook is generated from the repository pipeline and provides a structured analytical layer for summary review and business analysis.

- Output: `outputs/Market_Business_Strategy_Intelligence.xlsx`
- Workbook includes the core strategic and analytical summary sheets
- Structured for review alongside the Power BI final dashboard and SQL marts

---

## 9. Power BI Dashboard Final State

The dashboard is now operational in Power BI Desktop and was validated after the repair work.

### Final dashboard characteristics
- 5 pages
- 39 visual containers
- 35 DAX measures
- Interactive manufacturer and product analysis
- Pricing and value analysis
- Product positioning and whitespace analysis
- Strategy and opportunity framework

### Actual page names
The final PBIP contains these five pages:

1. Executive Market & Business Overview
2. Product & Competitive Intelligence
3. Pricing & Value Analysis
4. Product Positioning & Whitespace Analysis
5. Strategy & Opportunity Framework

### Repair and runtime validation note
The final validation confirmed:
- the pricing analysis schema mismatch was repaired to the actual final mart schema
- local CSV sources were validated
- missing measure references were repaired in the final model
- all five dashboard pages were opened and visually checked
- KPI cards and charts populated correctly
- the final Product Portfolio HHI result renders at approximately 1,326.53

This is documented as a final operational validation note rather than an open troubleshooting item.

---

## 10. Analytical Framework

The project supports a structured competitive and strategic framework:

- competitive landscape benchmarking across 11 manufacturers
- price and value analysis using verified catalog fields
- product positioning by price and range context
- portfolio concentration measurement via HHI
- unit economics and margin sensitivity framework
- geographic attractiveness framework with fail-closed registration dependencies

The project may be used for strategic analysis, market-entry work, and executive review, but it does not claim unverified registration market share as actual market share.

---

## 11. KPI Framework

The repository contains a verified KPI framework grounded in catalog facts and governance-aware pending metrics.

Validated values currently supported by the repo include:
- Manufacturers: 11
- Products: 42
- Priced products: 34
- Minimum price: ₹74,990
- Median price: approximately ₹1,26,171
- Average price: approximately ₹1,36,349
- Maximum price: ₹3,99,000
- Average certified range: approximately 159.4 km
- Average battery capacity: approximately 3.73 kWh
- Average price per km: approximately ₹867.71
- Product portfolio HHI: approximately 1,326.53

Registration-dependent KPIs remain explicitly pending and fail-closed unless verified official registration data is loaded.

---

## 12. Validation and Testing

The current repository state was validated directly.

- Pytest: 39 tests passed
- PBIP validation: 14/14 checks passed

The checks include project structure validation, DAX integrity, schema checks, fail-closed measure behavior, and current product portfolio HHI conditions.

---

## 13. Repository Structure

```text
Market-Business-Strategy-Intelligence/
├── README.md
├── CONTEXT.md
├── requirements.txt
├── data/
│   ├── processed/
│   │   ├── processed_verified_product_catalog.csv
│   │   ├── pricing_kpis.csv
│   │   ├── kpi_registry.csv
│   │   ├── kpi_status.csv
│   │   ├── product_positioning.csv
│   │   ├── product_value_scores.csv
│   │   ├── validation_results.json
│   │   └── sql/
│   │       ├── sql_pricing_analysis.csv
│   │       ├── sql_product_positioning.csv
│   │       ├── sql_kpi_results.csv
│   │       └── e2w_sql.duckdb
│   └── raw/
│       ├── DATASET_MANIFEST.csv
│       └── verified_product_catalog_2025_2026.csv
├── docs/
│   ├── FINAL_KPI_REGISTRY.md
│   ├── DATA_SOURCE_REGISTER.md
│   ├── POWER_BI_DAX.md
│   ├── POWER_BI_MODEL.md
│   ├── POWER_BI_POWER_QUERY.md
│   ├── SQL_ANALYTICS.md
│   └── ...
├── outputs/
│   └── Market_Business_Strategy_Intelligence.xlsx
├── powerbi/
│   ├── Market-Business-Strategy-Intelligence.pbip
│   ├── validate_pbip.py
│   ├── dax_measures.dax
│   ├── power_query_m_scripts.m
│   ├── Market-Business-Strategy-Intelligence.Report/
│   └── Market-Business-Strategy-Intelligence.SemanticModel/
├── sql/
│   ├── 01_schema.sql
│   ├── 02_load_verified_data.sql
│   ├── 03_data_quality.sql
│   ├── 04_competitive_analysis.sql
│   ├── 05_pricing_analysis.sql
│   ├── 06_product_positioning.sql
│   ├── 07_kpi_queries.sql
│   └── 08_pending_market_queries.sql
├── src/
│   ├── data_processing.py
│   ├── run_sql_pipeline.py
│   ├── generate_excel_workbook.py
│   ├── analytics/
│   └── tests/
└── pytest_out.txt
```

---

## 14. How to Run the Project

```bash
git clone https://github.com/tanyaverma20/Market-Business-Strategy-Intelligence.git
cd Market-Business-Strategy-Intelligence
python -m pip install -r requirements.txt

python src/data_processing.py
python src/run_sql_pipeline.py
python src/generate_excel_workbook.py
python powerbi/validate_pbip.py
python -m pytest -v
```

Open the Power BI project in Power BI Desktop to review the final dashboard and validate the repaired output visually.

---

## 15. Final Project Status

The repository is now in its final documented state:

- Verified product intelligence is complete and audit-ready
- Pricing, value, competitive, and positioning analysis are complete
- Power BI dashboard is operational in Power BI Desktop
- Vahan registration data remains intentionally pending and fail-closed
- Project outputs remain consistent with repository evidence and governance requirements

This is a complete commercial strategy intelligence platform for verified product benchmarking and strategic planning, with clear governance controls on any pending market-registration metrics.
