# CONTEXT.md — Project Technical Context & Ground Truth

## 1. Project Purpose & High-Level Scope

**Market & Business Strategy Intelligence** is an end-to-end commercial strategy, competitive benchmarking, and market intelligence platform for the Indian electric two-wheeler (e2W) market. The project transforms primary-source product disclosures and statutory industry filings into structured analytical models, a local DuckDB analytical SQL warehouse, an automated 9-sheet Excel workbook, and a 5-page interactive Microsoft Fabric Power BI dashboard (PBIP/PBIR).

The repository is strictly governed to avoid presenting unverified, synthetic, or interpolated data as fact:
- **Product Intelligence**: Completely verified across 11 manufacturers and 42 commercial models (34 priced / 8 variant specifications) with row-level source URLs.
- **Historical Market Sizing**: Anchored strictly on primary statutory disclosures submitted to the Securities and Exchange Board of India (SEBI)—specifically the *Ola Electric Mobility Limited Red Herring Prospectus (RHP)* (August 2024), citing CRISIL Research. Covers national annual e2W sales for FY2021 through FY2024.
- **State-Level Registrations & Vahan Data**: The Ministry of Road Transport and Highways (MoRTH) Vahan 4.0 public analytics dashboard enforces graphical CAPTCHAs and restricts web exports to 1-year windows. Because an open, authenticated, CAPTCHA-free API does not exist for longitudinal state-level bulk extracts, state registration rankings and OEM registration market shares remain **fail-closed** and return `BLANK()` across analytical models.
- **TAM / SAM / SOM Market Sizing**: Future addressable market sizing for FY2025 and beyond is explicitly modeled and documented as **ASSUMPTIONS** for scenario planning, clearly segregated from observed historical figures.

---

## 2. Final State Summary

The repository is functionally complete, deterministic, and interview-defensible:
- **Verified Product Catalog**: 42 commercial models across 11 manufacturers; 34 fully priced offerings; 8 models with technical specifications but unpriced brochures.
- **DuckDB Analytical SQL Warehouse**: 9 sequential SQL scripts executing against `e2w_sql.duckdb`; all 10 automated Data Quality checks passing with 0 issues.
- **Excel Commercial Model**: 9-sheet formatted analytical workbook generated at `outputs/Market_Business_Strategy_Intelligence.xlsx`.
- **Power BI PBIP/PBIR Dashboard**: 5 operational pages, 39 visual containers, and 35 DAX measures (25 verified operational + 10 fail-closed safeguards returning `BLANK()`).
- **Automated Test Suite**: 57 / 57 tests passing in Pytest (100% pass rate) with zero failures.
- **Cross-Engine Reconciliation**: Exact agreement across Python, DuckDB SQL, CSV marts, Excel, and Power BI ($0.00 variance) for all governed metrics.
- **Strict Data Governance**: Legacy proxy datasets are quarantined as `PROXY_DEPRECATED`; zero proxy data is relabeled as official Vahan or factual data.

---

## 3. Verified Scope & Data Boundaries

### 3.1 Verified Product Catalog Scope
The primary catalog is compiled from official OEM product pages, technical brochures, press releases, and ARAI-certified testing disclosures:
- **11 Verified Manufacturers / OEMs**: Ola Electric (9 models), Ather Energy (8 models), TVS Motor Company (6 models), Bajaj Auto (5 models), Ampere (Greaves) (2 models), BGauss (2 models), Hero MotoCorp (VIDA) (2 models), Kinetic Green (2 models), Revolt Motors (2 models), Simple Energy (2 models), Ultraviolette Automotive (2 models).
- **42 Commercial Models**: 34 priced commercial models with valid ex-showroom prices; 8 spec-only variant models.
- **Product Portfolio HHI**: 1,326.53 (unconcentrated, competitive catalog breadth).

### 3.2 Verified National Market Growth Scope (SEBI Statutory Filing)
Anchored on official primary statutory disclosures (*Ola Electric Mobility Limited RHP*, August 2024, citing CRISIL Research):
- **FY2021**: 41,000 units (Baseline)
- **FY2022**: 249,000 units (+507.3% YoY)
- **FY2023**: 728,000 units (+192.4% YoY)
- **FY2024**: 944,000 units (+29.7% YoY)
- **3-Year Historical CAGR (FY21–FY24)**: **184.5%**
- **Boundary**: Covers national India totals only. State-level and OEM-level registration breakdowns were not published in this filing and are not inferred or fabricated.

### 3.3 Governance Boundary & Quarantined Datasets
- **Quarantined (`PROXY_DEPRECATED`)**:
  - `vahan_e2w_registrations_monthly.csv`: Legacy generator claim using fixed allocations; barred from factual analysis.
  - `oem_e2w_registrations_annual.csv`: Synthetic annual OEM volume proxy; barred from factual analysis.
  - `state_socioeconomic_indicators.csv`: Structural template inputs; barred from generating factual state rankings.
- **Fail-Closed Guardrails**:
  - `pending.fact_ev_registrations` table in DuckDB contains strictly 0 rows (`pending_market_status = 'PENDING VERIFIED VAHAN DATA'`).
  - 10 registration-dependent DAX measures return `BLANK()`.
  - State rankings in GAI are withheld (`gai_score = None`, `gai_rank = None`, `status = INCOMPLETE`).

---

## 4. Current Verified Metrics

All values are deterministic and reconciled across Python, DuckDB, Excel, and Power BI:

| Metric Category | Indicator / Dimension | Verified Value | Baseline & Calculation Context |
| :--- | :--- | ---: | :--- |
| **Catalog Scope** | Verified Manufacturers / OEMs | **11** | Ola, Ather, TVS, Bajaj, Hero VIDA, Ampere, Simple, Revolt, Ultraviolette, Kinetic, BGauss |
| **Catalog Scope** | Commercial Models Audited | **42** | Row-level primary source links in `verified_product_catalog_2025_2026.csv` |
| **Catalog Scope** | Priced Commercial Models | **34** | Models with verified ex-showroom price disclosures |
| **Catalog Scope** | Product Portfolio HHI | **1,326.53** | Catalog breadth concentration across 11 manufacturers |
| **Pricing** | Minimum Price | **₹74,990** | Kinetic Green E-Luna |
| **Pricing** | Median Price | **₹1,26,170.50** | Mid-market anchor price point across 34 priced models |
| **Pricing** | Average Price | **₹136,349.21** | Catalog mean across 34 priced models (spread of ₹3,24,010) |
| **Pricing** | Maximum Price | **₹3,99,000** | Ultraviolette F77 Mach 2 Recon |
| **Powertrain Specs** | Average Certified Range | **159.39 km** | IDC / ARAI certified testing standards |
| **Powertrain Specs** | Average Battery Pack Capacity | **3.73 kWh** | Ranging from 2.0 kWh to 10.3 kWh |
| **Powertrain Specs** | Average Top Speed | **89.17 km/h** | Top speed across models with verified speed disclosures |
| **Powertrain Specs** | Average Motor Peak Power | **8.02 kW** | Peak motor power across verified models |
| **Metric Density** | Average Price per KM | **₹867.71 / km** | Ex-showroom price divided by certified range |
| **Metric Density** | Average Price per kWh | **₹36,418.79 / kWh** | Ex-showroom price divided by battery capacity |
| **Market Growth** | FY2021 Industry Volume | **41,000 units** | SEBI statutory filing (Ola Electric RHP 2024 / CRISIL Research) |
| **Market Growth** | FY2024 Industry Volume | **944,000 units** | SEBI statutory filing (Ola Electric RHP 2024 / CRISIL Research) |
| **Market Growth** | 3-Year Historical CAGR | **184.5%** | Compound annual growth rate from FY21 to FY24 |
| **TAM Sizing** | FY2025 Base Case TAM | **1,180,000 units** | ₹1,469.1 Cr (+25% growth assumption on FY24 baseline) |
| **SAM Sizing** | FY2025 Base Case SAM | **660,800 units** | ₹822.6 Cr (70% geo focus × 80% mid-market segment) |
| **SOM Sizing** | FY2025 Base Case SOM | **19,824 units** | ₹246.8 Cr (3.0% attainable market share of addressable SAM) |
| **BI System** | Power BI Dashboard Pages | **5** | Fabric PBIR specification (39 visual containers) |
| **BI System** | DAX Measures Implemented | **35** | 25 active measures + 10 fail-closed `BLANK()` safeguards |
| **Testing** | Automated Pytest Tests | **57 / 57 Passed** | Unit, integration, GAI fail-closed, and cross-engine reconciliation |
| **Testing** | PBIP Integrity Validation | **14 / 14 Passed** | Project structure, TMDL/BIM validity, and visual container integrity |

---

## 5. End-to-End Analytical Workflow

```text
Verified Data Sources
  ├── data/raw/verified_product_catalog_2025_2026.csv (42 source-linked models)
  ├── data/raw/sebi_verified_industry_totals.csv (FY21-FY24 national totals)
  └── Quarantined Legacy Proxies (Separated from factual analytics)
        │
        ▼
Python Data Processing & Validation (`src/data_processing.py`)
  ├── Schema standardization, numeric coercion, deduplication
  ├── Validation rule checks (bounds, range realization, price sanity)
  └── Export canonical processed CSVs
        │
        ▼
DuckDB Analytical Warehouse (`data/processed/sql/e2w_sql.duckdb`)
  ├── 01_schema.sql                 ──► Staging tables, dimensions, facts, pending schema
  ├── 02_load_verified_data.sql     ──► Ingests 42 verified models with provenance
  ├── 03_data_quality.sql           ──► 10 automated SQL assertions (nulls, bounds, duplicates)
  ├── 04_competitive_analysis.sql   ──► Window functions (RANK, DENSE_RANK), portfolio shares
  ├── 05_pricing_analysis.sql       ──► NTILE(4) quartiles, price-per-km, value leaderboard
  ├── 06_product_positioning.sql    ──► CASE WHEN positioning buckets, manufacturer summaries
  ├── 07_kpi_queries.sql            ──► Centralized kpi_status analytical view
  ├── 08_pending_market_queries.sql ──► Fail-closed market registration query templates
  └── 09_market_growth_marts.sql    ──► mart.sebi_market_growth (CAGR) & mart.tam_sam_som
        │
        ├─────────────────────────────┬─────────────────────────────┐
        ▼                             ▼                             ▼
Excel Commercial Model        Python Strategic Analytics    Power BI / PBIP Dashboard
(9 Formatted Sheets)         (Strategic Frameworks)        (5 Interactive Pages)
  ├── Executive KPIs           ├── TAM / SAM / SOM sizing    ├── Semantic Model (BIM)
  ├── Competitive Specs        ├── 5-Factor GAI Model        ├── 35 DAX Measures
  ├── Pricing Quartiles        ├── Unit economics & BOM      ├── 39 Visual Containers
  ├── Product Positioning      └── Whitespace boundaries     └── Fail-Closed Safeguards
  ├── Strategic Recs                          │                             │
  ├── SEBI Market Growth                      ▼                             ▼
  ├── TAM/SAM/SOM Scenarios        Business Intelligence & Strategy Intelligence
  ├── Source Register                         │
  └── Assumptions Provenance                  ▼
                               Evidence-Based Commercial Recommendations
```

---

## 6. SQL / DuckDB Analytical Layer & Marts

The DuckDB database is orchestrated by 9 sequential SQL scripts in `sql/`:

1. `01_schema.sql`: Initializes schemas (`main`, `mart`, `pending`), staging tables (`stg_verified_products`), dimensions (`dim_manufacturer`, `dim_product`), and facts (`fact_product_metrics`).
2. `02_load_verified_data.sql`: Loads cleaned product catalog into staging with provenance verification.
3. `03_data_quality.sql`: Executes 10 automated data quality checks (primary key uniqueness, non-null pricing, bounds validation).
4. `04_competitive_analysis.sql`: Computes manufacturer-level model counts, catalog shares, and specification ranks (`ROW_NUMBER`, `RANK`, `DENSE_RANK`).
5. `05_pricing_analysis.sql`: Builds the 17-column pricing mart featuring `NTILE(4)` pricing quartiles, price-per-km, price-per-kWh, and relative price positions.
6. `06_product_positioning.sql`: Categorizes offerings across 4 price tiers, 3 range brackets, 3 battery sizes, and 3 speed performance classes.
7. `07_kpi_queries.sql`: Generates `kpi_status` view aggregating catalog metrics and verification tags.
8. `08_pending_market_queries.sql`: Establishes fail-closed query templates for market volume, monthly trends, and state rankings (strictly isolated with 0 rows).
9. `09_market_growth_marts.sql`: Builds `mart.sebi_market_growth` (FY21–FY24 statutory volumes, YoY growth rates, 184.5% CAGR) and `mart.tam_sam_som` (3-scenario sizing model).

### Final 17-Column Pricing Mart Schema (`sql_pricing_analysis.csv`)
1. `product`
2. `manufacturer`
3. `price`
4. `battery_capacity_kwh`
5. `range_km`
6. `top_speed_kmh`
7. `price_per_km`
8. `price_per_kwh`
9. `price_bucket`
10. `value_rank`
11. `price_percentile`
12. `price_quartile`
13. `product_price_rank`
14. `avg_market_price`
15. `mfg_avg_price`
16. `relative_price_position`
17. `price_premium_vs_market_pct`

---

## 7. Python Analytical Modules (`src/analytics/`)

- `tam_som_framework.py`: Mathematical implementation of TAM/SAM/SOM sizing; computes multi-year CAGR from statutory totals; builds scenario comparison tables.
- `geographic_analysis.py`: Official 5-factor weighted Geographic Attractiveness Index (`compute_gai_scores`); implements vectorized min-max normalization (`_safe_normalize`); enforces fail-closed null detection.
- `unit_economics.py`: Models contribution margin, battery BOM sensitivity ($80 to $140/kWh), and break-even production volumes.
- `pricing_analysis.py`: Calculates price quartiles, metric densities (price/km, price/kWh), and relative price premiums.
- `positioning_analysis.py`: Multi-axial segmentation assigning models into price, range, battery, and performance buckets.
- `strategic_analysis.py`: Computes Product Portfolio HHI and catalog concentration.
- `market_analysis.py`: Growth and penetration formulas ready for future registration ingestion.
- `kpi_engine.py`: Registry engine tracking 24 verified enterprise KPIs against schema contracts.

---

## 8. Excel Commercial Modeling Layer

Generated by `src/generate_excel_workbook.py` as an executive workbook at `outputs/Market_Business_Strategy_Intelligence.xlsx`:
- Formatted with Segoe UI typography, custom `#1E293B` navy headers, white bold text, subtle borders (`#E2E8F0`), and Indian Rupee formatting (`₹#,##0`).
- **9 Structured Worksheets**:
  1. `Executive_KPI_Summary`: Executive KPI register with formulas, units, and verification tags.
  2. `Competitive_Benchmark`: Complete 42-model technical specification matrix with window ranks.
  3. `Pricing_Analysis`: Pricing quartiles, price-per-km, price-per-kWh, and market premiums.
  4. `Product_Positioning`: Multi-axial segmentation buckets and manufacturer summary counts.
  5. `Strategic_Recommendations`: Formatted strategic action plan for market entry.
  6. `Market_Growth_SEBI`: SEBI-verified historical industry volumes (FY21–FY24) and 184.5% CAGR.
  7. `TAM_SAM_SOM_Scenarios`: Conservative, Base, and Upside addressable market scenario models.
  8. `Source_Register`: Full inventory of raw datasets, source URLs, and access timestamps.
  9. `Assumptions_Provenance`: Technical audit trail and fail-closed governance definitions.

---

## 9. Power BI Solution Architecture

The Power BI project is structured as a Microsoft Fabric PBIP project (`powerbi/Market-Business-Strategy-Intelligence.pbip`) using PBIR definition format.

### 9.1 Report Pages (5 Pages, 39 Visual Containers)
1. **Executive Market & Business Overview** (11 visuals): Executive KPI cards, portfolio breadth bar chart, OEM pricing benchmark vs. market average, portfolio summary table, status banners.
2. **Product & Competitive Intelligence** (6 visuals): Multi-metric slicer strip, competitive specification matrix, price vs. range scatter plot, price-per-km efficiency leaderboard.
3. **Pricing & Value Analysis** (6 visuals): Price KPI row (Min, Median, Avg, Max), pricing quartile distribution, price-per-km and price-per-kWh value frontier.
4. **Product Positioning & Whitespace Analysis** (6 visuals): Price tier and range bracket breakdowns, multi-axial clustering quadrants, identified commercial whitespaces.
5. **Strategy & Opportunity Framework** (10 visuals): Product portfolio HHI indicator, TAM/SAM/SOM scenario sizing matrix, 5-factor GAI architecture, fail-closed registration status banners.

### 9.2 Power BI Screenshots
The five high-resolution dashboard preview screenshots are located at:
`docs/powerbi/screenshots/`
- `docs/powerbi/screenshots/01_executive_market_overview.png`
- `docs/powerbi/screenshots/02_product_competitive_intelligence.png`
- `docs/powerbi/screenshots/03_pricing_value_analysis.png`
- `docs/powerbi/screenshots/04_product_positioning_whitespace.png`
- `docs/powerbi/screenshots/05_strategy_opportunity_framework.png`

### 9.3 DAX Library (35 Measures)
Defined in `powerbi/dax_measures.dax`:
- **25 Verified Operational Measures**: Portfolio counts, pricing averages, medians, range and battery benchmarks, Product Portfolio HHI (1,326.53), SEBI statutory growth metrics, and TAM/SAM/SOM scenario measures.
- **10 Fail-Closed Safeguard Measures**: Return `BLANK()` with explicit explanatory comments for Vahan-dependent metrics (`Total EV Registrations (Pending)`, `YoY Market Growth Pct (Pending)`, `OEM Registration Market Share Pct (Pending)`, `State Registration Rank (Pending)`, etc.).

---

## 10. Analytical Frameworks & Methodologies

### 10.1 Product Portfolio Concentration (HHI)
$$\text{HHI} = \sum_{i=1}^{11} (\text{Catalog Share}_i)^2 = \mathbf{1,326.53}$$
Indicates an unconcentrated, competitive product landscape across 11 manufacturers.

### 10.2 Geographic Attractiveness Index (GAI) Framework
5-Factor Model:
$$\text{GAI Score}_s = 0.30 \cdot \text{Vol}_s + 0.25 \cdot \text{Inc}_s + 0.20 \cdot \text{Dens}_s + 0.15 \cdot \text{Pol}_s + 0.10 \cdot \text{Urb}_s$$
- Registration Volume (30%) — *Status: PENDING VAHAN*
- Per Capita Income (25%) — *Verified RBI / MoSPI*
- Two-Wheeler Fleet Density (20%) — *Verified MoRTH Yearbook*
- State EV Policy (15%) — *Verified Gazette Notifications*
- Urbanization Rate (10%) — *Verified Census*
*Fail-Closed Rule*: If verified registration volume is unavailable, `gai_score = None`, `gai_rank = None`, and status is `INCOMPLETE - Missing inputs: fail-closed`. Zero state rankings are produced from proxy data.

### 10.3 TAM / SAM / SOM Scenario Framework
Anchored on the observed FY2024 national industry total of **944,000 units** (SEBI RHP):
- **Conservative Case** (+10% FY25 growth; 60% geo; 70% segment; 1.5% SOM share):
  - TAM: **1,038,400 units** (₹1,246.1 Cr) | SAM: **435,648 units** | SOM: **6,534 units** (₹78.4 Cr).
- **Base Case** (+25% FY25 growth; 70% geo; 80% segment; 3.0% SOM share):
  - TAM: **1,180,000 units** (₹1,469.1 Cr) | SAM: **660,800 units** | SOM: **19,824 units** (₹246.8 Cr).
- **Upside Case** (+45% FY25 growth; 80% geo; 85% segment; 5.0% SOM share):
  - TAM: **1,369,800 units** (₹1,780.7 Cr) | SAM: **930,660 units** | SOM: **46,533 units** (₹604.9 Cr).
*Governance Rule*: All forward TAM/SAM/SOM numbers are explicitly labeled as **ASSUMPTIONS** for scenario planning.

---

## 11. Testing & Validation

- **Pytest Test Suite**: **57 / 57 passed (100%)**
  - `test_analytical_engine.py`: 16 unit tests for data transformation, bounds, and pricing math.
  - `test_market_growth_tam_som.py`: 18 tests for SEBI volume growth, CAGR, TAM/SAM/SOM, GAI fail-closed mechanics, and cross-engine reconciliation.
  - `test_powerbi_specification.py`: 9 integration tests for PBIP structure, TMDL/BIM validity, PBIR 5-page directories, and DAX measure syntax.
  - `test_sql_pipeline.py`: 8 tests for DuckDB pipeline execution, table structures, and 10 SQL data quality checks.
  - `test_resume_validation.py`: 6 audit tests verifying catalog scopes (11 OEMs, 42 models, 34 priced), Excel sheets, and HHI regression (1,326.53).
- **PBIP Validation**: **14 / 14 checks passed (ALL PASS)** via `powerbi/validate_pbip.py`.
- **Reconciliation**: Exact $0.00 variance across Python, DuckDB, Excel, and Power BI.

---

## 12. Repository Structure

```text
Market-Business-Strategy-Intelligence/
├── README.md                                          # Master project overview & executive case study
├── CONTEXT.md                                         # Technical architecture & project ground-truth record
├── requirements.txt                                   # Python dependencies
│
├── data/
│   ├── raw/
│   │   ├── verified_product_catalog_2025_2026.csv     # 42 source-linked commercial models
│   │   ├── sebi_verified_industry_totals.csv          # FY21-FY24 national industry totals (SEBI RHP)
│   │   ├── DATASET_MANIFEST.csv                       # Provenance metadata & governance classification
│   │   ├── vahan_e2w_registrations_monthly.csv        # Quarantined proxy dataset (PROXY_DEPRECATED)
│   │   ├── oem_e2w_registrations_annual.csv           # Quarantined proxy dataset (PROXY_DEPRECATED)
│   │   └── state_socioeconomic_indicators.csv         # Quarantined proxy dataset (PROXY_DEPRECATED)
│   └── processed/
│       ├── processed_verified_product_catalog.csv     # Cleaned canonical product catalog
│       ├── pricing_kpis.csv                           # Calculated pricing summary metrics
│       ├── kpi_registry.csv                           # Master KPI registry with formulas
│       ├── kpi_status.csv                             # KPI status and validation metadata
│       └── sql/
│           ├── e2w_sql.duckdb                         # Local DuckDB analytical warehouse
│           ├── sql_competitive_analysis.csv           # Competitive specifications & window ranks
│           ├── sql_pricing_analysis.csv               # Pricing quartiles & price/km metrics
│           ├── sql_product_positioning.csv            # Multi-axial positioning buckets
│           ├── sql_kpi_results.csv                    # Consolidated KPI view outputs
│           ├── sql_data_quality_results.csv           # 10 Data Quality check results
│           ├── sql_sebi_market_growth.csv             # SEBI-verified historical market growth mart
│           ├── sql_tam_sam_som.csv                    # TAM/SAM/SOM scenario sizing mart
│           └── sql_pipeline_summary.json              # Automated SQL pipeline execution summary
│
├── sql/
│   ├── 01_schema.sql                                  # Relational schemas & fail-closed tables
│   ├── 02_load_verified_data.sql                      # Provenance ingestion logic
│   ├── 03_data_quality.sql                            # 10 automated SQL DQ assertion rules
│   ├── 04_competitive_analysis.sql                    # Competitive benchmarking mart
│   ├── 05_pricing_analysis.sql                        # Pricing quartile & value mart
│   ├── 06_product_positioning.sql                     # Multi-axial product positioning mart
│   ├── 07_kpi_queries.sql                             # Executive KPI status view
│   ├── 08_pending_market_queries.sql                  # Fail-closed market registration templates
│   └── 09_market_growth_marts.sql                     # SEBI growth & TAM/SAM/SOM marts
│
├── src/
│   ├── data_processing.py                             # Python cleaning & validation pipeline
│   ├── run_sql_pipeline.py                            # Automated DuckDB orchestration harness
│   ├── generate_excel_workbook.py                     # 9-sheet executive Excel generator
│   ├── analytics/
│   │   ├── __init__.py                                # Analytics package exports
│   │   ├── tam_som_framework.py                       # TAM/SAM/SOM sizing & SEBI growth analytics
│   │   ├── geographic_analysis.py                     # 5-factor GAI model & fail-closed gates
│   │   ├── unit_economics.py                          # BOM cost sensitivity & contribution margin
│   │   ├── pricing_analysis.py                        # Price quartiles & metric density
│   │   ├── positioning_analysis.py                    # Multi-axial positioning segmentation
│   │   ├── strategic_analysis.py                      # Portfolio HHI & concentration analysis
│   │   ├── market_analysis.py                         # Market growth formulas & CAGR models
│   │   └── kpi_engine.py                              # Central KPI registration engine
│   └── tests/
│       ├── test_market_growth_tam_som.py              # Tests for SEBI growth, TAM, GAI, & reconciliation
│       ├── test_analytical_engine.py                  # Unit tests for analytics modules
│       ├── test_sql_pipeline.py                       # Integration tests for DuckDB pipeline
│       ├── test_powerbi_specification.py              # Tests for PBIP structure & DAX integrity
│       └── test_resume_validation.py                  # Audit tests for catalog scope & HHI regression
│
├── powerbi/
│   ├── Market-Business-Strategy-Intelligence.pbip     # Power BI project entry file
│   ├── validate_pbip.py                               # PBIP integrity validation script (14 checks)
│   ├── dax_measures.dax                               # 35 production DAX measures (with safeguards)
│   ├── power_query_m_scripts.m                        # Power Query M scripts for all 8 tables
│   ├── Market-Business-Strategy-Intelligence.Report/   # PBIR report definitions & 5 page folders
│   └── Market-Business-Strategy-Intelligence.SemanticModel/ # Tabular semantic model & TMDL schemas
│
├── outputs/
│   └── Market_Business_Strategy_Intelligence.xlsx     # 9-sheet formatted commercial Excel workbook
│
└── docs/
    ├── powerbi/
    │   └── screenshots/                               # 5 high-resolution dashboard preview screenshots
    │       ├── 01_executive_market_overview.png
    │       ├── 02_product_competitive_intelligence.png
    │       ├── 03_pricing_value_analysis.png
    │       ├── 04_product_positioning_whitespace.png
    │       └── 05_strategy_opportunity_framework.png
    ├── TAM_SAM_SOM_METHODOLOGY.md                     # Auditable market sizing methodology
    ├── GEOGRAPHIC_ANALYSIS.md                         # 5-factor GAI framework specification
    ├── FINAL_KPI_REGISTRY.md                          # Registry of 24 verified enterprise KPIs
    ├── POWER_BI_DASHBOARD_SPEC.md                     # Complete 5-page visual layout manual
    ├── POWER_BI_DAX.md                                # DAX measure dictionary & formulas
    ├── POWER_BI_MODEL.md                              # Semantic model schema & relationships
    ├── POWER_BI_POWER_QUERY.md                        # Power Query M documentation
    ├── SQL_ANALYTICS.md                               # DuckDB SQL documentation
    ├── DATA_SOURCE_REGISTER.md                        # Source provenance register
    └── RESUME_CLAIM_VALIDATION.md                     # Granular resume claim audit report
```

---

## 13. Critical Resume Claim Status & Defense

| Resume Claim | Implementation Status | Exact Auditable Evidence & Governance Ground Truth |
| :--- | :---: | :--- |
| **Claim 1: Multi-Year Market Data Across 20+ States** | **PARTIALLY VERIFIED** | **Verified**: 4 fiscal years of national industry totals (FY21: 41k, FY22: 249k, FY23: 728k, FY24: 944k units; 184.5% CAGR) from SEBI statutory filings.<br>**Not Verified**: 10+ years series and 20+ states registration breakdown (source provides national totals only). Factual state-level volume rankings remain fail-closed to prevent proxy data relabeling. |
| **Claim 2: Competitor & Product Benchmarking** | **VERIFIED** | Benchmarked **11 competitors** (exceeds "10+") and **42 commercial models** (34 priced, exceeds "25+"). Analyzed pricing (₹74.9k–₹399k), price/km (avg ₹867.71), price/kWh (avg ₹36,419), positioning buckets, catalog whitespace, and catalog concentration (Product Portfolio HHI = 1,326.53). |
| **Claim 3: Strategic Frameworks & 5-Page Power BI Dashboard** | **VERIFIED** | Built TAM/SAM/SOM 3-scenario sizing model, contribution margin & BOM sensitivity model, 5-factor GAI architecture, 24 verified KPIs registered, 9-sheet Excel workbook, and fully operational 5-page Fabric PBIP dashboard with 39 visual containers and 35 DAX measures. |

---

## 14. Document Version & Maintenance

- **Document Version**: 2.0 (Authoritative Technical Ground Truth)
- **Last Verified**: September 2026
- **Test Status**: 57 / 57 passing (100%)
- **Governance Gate**: Fail-Closed Active
