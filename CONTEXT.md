# CONTEXT.md — Project Technical Context

## 1. Project Purpose

Market-Business-Strategy-Intelligence is a commercial strategy and competitive intelligence platform for the Indian electric two-wheeler market. The project benchmarks verified product data across manufacturers and models, analyzes pricing and value, identifies strategic whitespace, and presents the results through a final operational Power BI dashboard.

The repository is intentionally governed to avoid presenting unverified registration data as fact. Historical Vahan registration data is not represented as verified data in the final analytical outputs, and registration-dependent metrics remain pending or fail-closed.

---

## 2. Final State Summary

The project is functionally complete as a final analytical platform:

- Verified product catalog across 11 manufacturers and 42 commercial models
- Standardized competitive, pricing, and positioning analyses
- DuckDB SQL analytical warehouse and CSV mart outputs
- Excel workbook generated from processed outputs
- Power BI dashboard repaired and validated in Power BI Desktop
- Fail-closed handling for pending registration-based metrics

This is a reliable business-analytics repository, not a registration-volume database.

---

## 3. Verified Scope and Data Boundaries

### Verified product data
The primary data source is a verified OEM/catalog product dataset. The project intentionally does not describe this as transaction or registration data.

Current verified scope:
- 42 commercial electric two-wheeler models
- 11 manufacturers
- 34 priced products

### Governance boundary
The governance model explicitly preserves the boundary between verified product intelligence and pending registration intelligence:

- Historical Vahan registration data is not represented as verified data in the final outputs
- Registration-dependent metrics remain marked as PENDING / fail-closed
- No proxy registration numbers are relabeled as official data
- This is an intentional provenance practice

---

## 4. Repository Structure

```text
Market-Business-Strategy-Intelligence/
├── README.md
├── CONTEXT.md
├── requirements.txt
├── data/
│   ├── processed/
│   │   ├── verified_product_catalog_canonical.csv
│   │   ├── processed_verified_product_catalog.csv
│   │   ├── pricing_kpis.csv
│   │   ├── kpi_registry.csv
│   │   ├── kpi_status.csv
│   │   ├── product_positioning.csv
│   │   ├── product_value_scores.csv
│   │   ├── validation_results.json
│   │   └── sql/
│   │       ├── e2w_sql.duckdb
│   │       ├── sql_pricing_analysis.csv
│   │       ├── sql_product_positioning.csv
│   │       ├── sql_kpi_results.csv
│   │       └── ...
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

## 5. Pipeline Architecture

The end-to-end workflow is:

Raw verified OEM product data
→ Python processing and validation
→ DuckDB analytical warehouse
→ analytical CSV marts
→ Excel workbook
→ Power BI semantic model and Power Query
→ DAX measures
→ 5-page interactive dashboard
→ strategic insights

This pipeline is deterministic and auditable. It separates verified commercial benchmarking from pending market-registration analysis.

---

## 6. Current Verified Metrics

The repository currently validates the following business metrics from the product catalog and analytical outputs:

- Manufacturers: 11
- Products: 42
- Priced products: 34
- Minimum price: INR 74,990
- Median price: approximately INR 126,171
- Average price: approximately INR 136,349
- Maximum price: INR 399,000
- Average certified range: approximately 159.4 km
- Average battery capacity: approximately 3.73 kWh
- Average motor power: approximately 8.02 kW
- Average price per km: approximately INR 867.71
- Product portfolio HHI: approximately 1,326.53

These values are supported by the current catalog and processed analytical outputs.

---

## 7. Pricing Analysis Schema

The pricing mart in `data/processed/sql/sql_pricing_analysis.csv` reflects the current final schema, which is 17 columns:

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

This is the schema that should be documented and referenced. Older documentation that references obsolete PricingAnalysis fields or the old 15-column schema should be treated as stale.

---

## 8. Power BI Final State

The Power BI project is final and operational in Power BI Desktop.

### Dashboard characteristics
- 5 pages
- 39 visual containers
- 35 DAX measures
- Interactive product and manufacturer analysis
- Pricing and value analysis
- Product positioning and whitespace analysis
- Strategy and opportunity framework

### Final page names
The actual report pages are:

1. Executive Market & Business Overview
2. Product & Competitive Intelligence
3. Pricing & Value Analysis
4. Product Positioning & Whitespace Analysis
5. Strategy & Opportunity Framework

### Runtime validation note
The final repair cycle validated:
- the pricing schema mismatch in Power Query was corrected to the current schema
- local CSV sources were validated
- missing Product Portfolio HHI measure references were repaired
- all five pages opened and visually checked
- KPI cards and charts rendered successfully
- Page 5 Product Portfolio HHI visual renders at approximately 1,326.53

This is recorded as final validation evidence, not as an active defect backlog.

---

## 9. Power BI Project Structure

The actual Power BI project structure is:

- `powerbi/Market-Business-Strategy-Intelligence.pbip`
- `powerbi/Market-Business-Strategy-Intelligence.Report/definition/report.json`
- `powerbi/Market-Business-Strategy-Intelligence.SemanticModel/definition/model.bim`
- `powerbi/dax_measures.dax`
- `powerbi/power_query_m_scripts.m`
- `powerbi/validate_pbip.py`

The PBIP is the source-controlled artifact. The report definition contains the 5 page structure and the model definition contains the tabular model and many DAX measures.

---

## 10. SQL / Data Warehouse Notes

The SQL layer is designed for deterministic analytics and governance separation.

- Verified product records are loaded into the main marts and dimensions
- Any market registration dataset remains pending and isolated in fail-closed forms
- The current warehouse and marts are evidence-backed and support product benchmarking
- Historical market-share metrics are not produced from synthetic or proxy registration data

---

## 11. Governance and Provenance Rules

The repository follows explicit governance principles:

- Verified product data is considered the factual operational baseline
- Unverified / proxy registration data is not used as fact
- Registration-dependent measures remain pending or blank wherever the official data is unavailable
- Unsupported market-share claims are not documented as verified outputs
- No RAG, vector database, or autonomous multi-agent architecture is included in the project design

This preserves a truthful business-analytics posture for portfolio and interview use.

---

## 12. Validation Status

The repository was validated against the current state of the project:

- Pytest suite: 39 tests passed
- PBIP validation: 14/14 checks passed

These counts reflect the current repository and should be treated as the current status, not stale totals from earlier documentation.

---

## 13. Final Project Positioning

The repository is a complete commercial intelligence platform for the Indian electric two-wheeler market, with verified product benchmarking, pricing analysis, portfolio concentration analysis, product positioning, and strategic framework outputs.

It is positioned as a defensible business-analytics platform for:
- competitive/product intelligence across 11 manufacturers and 42 models
- pricing, value, and positioning analysis
- portfolio concentration and whitespace assessment
- geographic evaluation framework with fail-closed registration guardrails

It is not positioned as a verified historical registration market-share database, and the repository does not claim that unsupported registration data has been integrated.

---

## 14. Final Notes

This context file reflects the repository’s current final state and intentionally excludes stale troubleshooting narratives, obsolete schema claims, and unsupported market-growth claims. The project is complete as a product intelligence and strategy platform and remains guarded by explicit provenance and governance standards.
