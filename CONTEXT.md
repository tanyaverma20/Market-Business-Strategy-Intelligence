# CONTEXT.md — Project Technical Context Document

**Project Name**: Market-Business-Strategy-Intelligence  
**Target Repository**: `Market-Business-Strategy-Intelligence`  
**Document Purpose**: Comprehensive, self-contained technical and architectural context document for an external AI model or engineer to understand, reason about, debug, explain, and evaluate the entire project without direct access to the filesystem.

---

## 1. Project Overview

### One-Sentence Explanation
Market-Business-Strategy-Intelligence is a reproducible commercial strategy and competitive intelligence platform for the Indian electric two-wheeler (e2W) market, integrating verified OEM primary-source product data across Python analytics, an embedded DuckDB SQL analytical warehouse, an automated 7-sheet Microsoft Excel model, and a 5-page Power BI Project (PBIP) with 35 DAX measures under a fail-closed data governance architecture.

### Interview-Ready Explanation
This project was engineered to solve a critical commercial strategy challenge for **Alpha Motors**, an automotive entrant evaluating strategic entry into India's rapidly electrifying two-wheeler industry (a 15–20 million unit annual market transitioning from FAME-II to PM E-DRIVE subsidies). Rather than relying on unverified internet scrapings or synthetic estimates, the project enforces a strict, auditable **Anti-Fabrication and Provenance Safeguard Policy**. It establishes a verified primary-source baseline of 11 manufacturers and 42 commercial models, processes the catalog through modular Python analytics and an embedded DuckDB SQL OLAP warehouse, and publishes the findings across an automated 7-sheet Excel workbook and an authored 5-page Power BI Project (PBIP) featuring 39 visual containers. Core strategic frameworks include competitive intensity (HHI), pricing quartiles, price-per-km/kWh value leaderboards, catalog whitespace identification, unit economics BOM sensitivity, and a multi-criteria Geographic Attractiveness Index (GAI). The entire codebase is verified by 39 automated pytest tests and 14 PBIP integrity validation checks.

### Detailed Technical Explanation
The repository is an end-to-end analytical data platform spanning the complete data engineering, analytical modeling, business intelligence, and governance lifecycle:
1. **Data Ingestion & Provenance Auditing**: Ingests primary-source product specifications and pricing directly linked to official OEM portals, ARAI compliance disclosures, and SEBI DRHP filings (Ola Electric, Ather Energy). Raw files are fingerprinted via SHA-256 and categorized into `VERIFIED` versus `PROXY_DEPRECATED` in `data/raw/DATASET_MANIFEST.csv`.
2. **Data Cleansing & Standardization**: Python pipeline (`src/data_processing.py`) enforces strict schema validation, type casting, non-negative range/battery constraints, and state code normalization across 36 Indian States and Union Territories.
3. **OLAP SQL Warehouse**: Embedded DuckDB database (`e2w_sql.duckdb`) structured into `stg`, `dim`, `fact`, `mart`, `kpi`, and `pending` schemas. Utilizes Common Table Expressions (CTEs), window functions (`ROW_NUMBER()`, `NTILE(4)`, `PERCENT_RANK()`), and ten automated data quality assertion rules.
4. **Analytical Engine**: Modular Python framework (`src/analytics/`) computing competitive benchmarks, portfolio HHI (1,326.5), pricing percentiles, IDC range realization curves, unit economics BOM margins, and strategic priority matrices.
5. **Business Intelligence Layer**: A fully authored Power BI Project (`powerbi/Market-Business-Strategy-Intelligence.pbip`) utilizing the modern PBIP/PBIR format. Comprises a semantic model (`model.bim`) with 6 tables, M Power Query partitions connected to local SQL marts, 35 DAX measures, and a report definition (`report.json`) across 5 comprehensive strategic pages.
6. **Financial & Strategic Spreadsheet**: Automated openpyxl/xlsxwriter pipeline (`src/generate_excel_workbook.py`) emitting a structured 7-sheet Excel workbook (`outputs/Market_Business_Strategy_Intelligence.xlsx`) with native formulas and formatting.
7. **Fail-Closed Governance Mechanism**: A rigorous architectural safeguard where unavailable external datasets (such as multi-year state-level MoRTH Vahan registrations) remain isolated in empty schemas (`PendingMarketRegistrations`), and all dependent DAX measures return `BLANK()` rather than fabricated proxy values.

---

## 2. Project Goals and Problem Statement

### Motivation & Context
India's two-wheeler segment represents the primary volume frontier for domestic transport decarbonization. Following the expiration of the FAME-II subsidy scheme and the introduction of the PM E-DRIVE initiative, electric 2-wheeler OEMs faced revised subsidy caps (reduced to ₹5,000/kWh in FY25, and ₹2,500/kWh in FY26), intensifying margin pressure and forcing a market-wide pricing and product realignment.

### Core Strategic Questions Addressed
1. **Competitive Landscape**: How concentrated is the commercial product landscape across established legacy OEMs (Bajaj, TVS, Hero) and EV pure-plays (Ola, Ather, Ultraviolette, Simple Energy)?
2. **Pricing Architecture**: What are the market price boundaries, median ex-showroom price points, and value thresholds on a price-per-km and price-per-kWh basis?
3. **Catalog Whitespace**: Where are commercial offerings clustered, and where does unserved product whitespace exist across price and range categories?
4. **Unit Economics & Margin Viability**: How do cell pack costs ($/kWh), chassis fabrication costs, and fixed overheads impact contribution margins and break-even manufacturing volumes?
5. **Geographic Market Prioritization**: How should state-level socioeconomic, infrastructure, and policy indicators be combined into an objective prioritization framework for network expansion?
6. **Analytical Integrity**: How can corporate decision-makers maintain complete auditability and prevent unverified proxy numbers from polluting executive dashboards?

### What the System Does NOT Attempt to Solve
- It does **not** generate speculative, unverified historical Vahan market-share numbers.
- It does **not** fabricate state registration trends or historical CAGR.
- It does **not** rely on real-time cloud APIs requiring runtime internet connectivity.

---

## 3. Technology Stack

| Category | Technology | Version | Location / Usage | Role in Architecture |
|---|---|---|---|---|
| **Language** | Python | 3.13.5 (compatible with 3.11+) | `src/`, `powerbi/` | Core programming language for processing, analytics, and automation |
| **Data Processing** | Pandas | 2.2.3 | `src/data_processing.py`, `src/analytics/` | DataFrame manipulation, data cleaning, type coercion, export |
| **Numerical Computing**| NumPy | 2.2.3 | `src/analytics/` | Vectorized mathematical operations, statistical percentiles |
| **OLAP Database** | DuckDB | 1.2.0 | `sql/`, `src/run_sql_pipeline.py` | High-performance in-process SQL OLAP database, CTEs, window functions |
| **Spreadsheet Engine** | XlsxWriter | 3.2.2 | `src/generate_excel_workbook.py` | Generates formatted 7-sheet OpenXML `.xlsx` workbook with native formulas |
| **Testing Framework** | Pytest | 9.1.1 | `src/tests/` | Automated unit testing, schema validation, resume claim verification |
| **BI Reporting** | Power BI Desktop | 2.157.1354.0 (Store AppX) | `powerbi/` | Interactive desktop application hosting the live tabular engine (`msmdsrv.exe`)|
| **Project Format** | Power BI Project (PBIP) | 1.0 (PBIR format) | `powerbi/*.pbip` | Source-controlled, human-readable JSON/BIM project structure |
| **Query Language** | DAX (Data Analysis Expressions) | N/A | `powerbi/dax_measures.dax`, `model.bim` | Analytical calculations: 25 verified formulas + 10 fail-closed BLANK() measures |
| **ETL Partitions** | Power Query (M) | N/A | `powerbi/power_query_m_scripts.m`, `model.bim` | Table partition queries importing CSV data into Power BI tabular model |
| **Hashing & Security** | hashlib (SHA-256) | Python stdlib | `src/data_processing.py` | Data integrity verification and file checksum validation |
| **Process / OS** | PowerShell / Windows WMI | Windows 11 | Deployment & validation scripts | Process monitoring, port inspection, and Power BI automation |

---

## 4. Complete Repository Structure

```
Market-Business-Strategy-Intelligence/
│
├── README.md                                 # Public documentation, portfolio metrics, and reproduction instructions
├── CONTEXT.md                                # Comprehensive, deep technical context document (this file)
├── requirements.txt                          # Python dependencies (duckdb, pandas, numpy, xlsxwriter, pytest)
│
├── data/
│   ├── raw/                                  # Primary source inputs and quarantined legacy proxy datasets
│   │   ├── DATASET_MANIFEST.csv              # Audit manifest: dataset names, provenance classes, eligibility tags
│   │   ├── verified_product_catalog_2025_2026.csv # Canonical primary source catalog (42 verified models, 11 OEMs)
│   │   ├── competitor_product_catalog.csv    # Legacy proxy dataset (quarantined as PROXY_DEPRECATED)
│   │   ├── oem_e2w_registrations_annual.csv  # Legacy proxy OEM volume (quarantined as PROXY_DEPRECATED)
│   │   ├── vahan_e2w_registrations_monthly.csv # Legacy proxy Vahan volume (quarantined as PROXY_DEPRECATED)
│   │   ├── state_socioeconomic_indicators.csv # State population, urbanization, and two-wheeler density data
│   │   └── policy_incentive_timeline.csv     # Regulatory subsidy timelines (FAME-I, FAME-II, EMPS, PM E-DRIVE)
│   │
│   └── processed/                            # Standardized, audited analytical outputs
│       ├── processed_verified_product_catalog.csv # Cleaned, strongly typed canonical product catalog (42 rows)
│       ├── competitive_intensity.csv         # Computed manufacturer breadth, product counts, and portfolio HHI
│       ├── competitive_kpis.csv              # Engineering specification benchmarks (power, speed, range)
│       ├── pricing_kpis.csv                  # Ex-showroom pricing summary, quartiles, and range price ratios
│       ├── product_positioning.csv           # Model-level segmentations (price bucket, range bucket, performance)
│       ├── product_value_scores.csv          # Derived price-per-km, price-per-kWh, and value index metrics
│       ├── unit_economics_results.csv        # Modeled BOM breakdown, gross margins, and contribution margins
│       ├── kpi_registry.csv                  # Complete catalog of 35 KPIs with governance status flags
│       ├── kpi_status.csv                    # Status table feeding the BI model (verified vs. pending)
│       ├── validation_results.json           # SHA-256 hashes, row counts, and data quality check logs
│       │
│       └── sql/                              # DuckDB analytical warehouse outputs and exported marts
│           ├── e2w_sql.duckdb                # Embedded DuckDB database file containing all tables and views
│           ├── sql_competitive_analysis.csv  # Competitive analytical mart (42 rows, 18 columns)
│           ├── sql_pricing_analysis.csv      # Pricing analytical mart (42 rows, 18 columns)
│           ├── sql_product_positioning.csv   # Positioning analytical mart (42 rows, 18 columns)
│           ├── sql_kpi_results.csv           # Consolidated KPI query results (14 metrics)
│           ├── sql_data_quality_results.csv  # Results of 10 automated SQL data quality constraints
│           └── sql_pipeline_summary.json     # Execution audit summary and table row counts
│
├── sql/                                      # DuckDB modular SQL scripts executed in order
│   ├── 01_schema.sql                         # Schema creation (stg, dim, fact, mart, kpi, pending)
│   ├── 02_load_verified_data.sql             # Data ingestion into staging and dimensional star-schema tables
│   ├── 03_data_quality.sql                   # 10 assertion tests verifying integrity, ranges, and non-negativity
│   ├── 04_competitive_analysis.sql           # Mart computing manufacturer portfolio breadth, power, and speed
│   ├── 05_pricing_analysis.sql               # Mart computing price percentiles, quartiles, and price-per-km
│   ├── 06_product_positioning.sql            # Mart categorizing products into 2x2 price and range quadrants
│   ├── 07_kpi_queries.sql                    # Consolidated KPI view calculating market-wide benchmarks
│   └── 08_pending_market_queries.sql         # Empty stub schemas and views for future Vahan registration data
│
├── src/                                      # Application source code
│   ├── data_processing.py                    # Primary ingestion, validation, and standardized processing pipeline
│   ├── run_sql_pipeline.py                   # Orchestrator running DuckDB scripts, assertions, and mart exports
│   ├── generate_excel_workbook.py            # OpenXML spreadsheet generator building the 7-sheet workbook
│   ├── populate_raw_datasets.py              # Auxiliary utility populating raw template references
│   ├── test_data_processing.py               # Unit tests verifying state standardization and aliases
│   │
│   ├── analytics/                            # Modular Python analytical engine
│   │   ├── __init__.py                       # Package exports
│   │   ├── competitive_analysis.py           # Portfolio concentration, HHI, and brand breadth calculations
│   │   ├── pricing_analysis.py               # Price percentiles, quartiles, and price-to-spec ratios
│   │   ├── positioning_analysis.py           # 2x2 matrix bucketing (price tier vs. range category)
│   │   ├── unit_economics.py                 # Vehicle BOM modeling, battery sensitivity, break-even volumes
│   │   ├── geographic_analysis.py            # Geographic Attractiveness Index (GAI) multi-criteria formula
│   │   ├── strategic_analysis.py             # Strategic opportunity scoring and strategic recommendations
│   │   ├── scenario_analysis.py              # Scenario planning framework (battery cost vs. subsidy change)
│   │   ├── market_analysis.py                # Market-level calculations and growth framework stubs
│   │   └── kpi_engine.py                     # Centralized engine generating KPI registry and governance statuses
│   │
│   └── tests/                                # Automated Pytest test suite (38 tests)
│       ├── test_analytical_engine.py         # 16 tests verifying all Python analytical math and edge cases
│       ├── test_sql_pipeline.py              # 9 tests verifying DuckDB warehouse integrity, CTEs, and marts
│       ├── test_powerbi_specification.py     # 7 tests validating PBIP structure, report.json, and DAX syntax
│       └── test_resume_validation.py         # 5 tests verifying that catalog counts substantiate resume claims
│
├── powerbi/                                  # Microsoft Power BI Project (PBIP) source artifacts
│   ├── Market-Business-Strategy-Intelligence.pbip # Project root entry file linking report to semantic model
│   ├── validate_pbip.py                      # 14-point automated validator checking PBIP JSON and DAX health
│   ├── generate_model_bim.py                 # Automated generator compiling model.bim with correct JSON escapes
│   ├── patch_pbip_paths.py                   # Path patcher dynamically injecting local absolute CSV paths
│   ├── dax_measures.dax                      # Canonical repository of 35 DAX measures with documentation
│   ├── power_query_m_scripts.m               # Standalone M scripts for all table partitions
│   │
│   ├── Market-Business-Strategy-Intelligence.Report/ # PBIR Report artifact folder
│   │   ├── definition.pbir                   # Points relatively to ../Market-Business-Strategy-Intelligence.SemanticModel
│   │   ├── item.metadata.json                # V1 Report metadata (type: Report, displayName)
│   │   └── definition/
│   │       └── report.json                   # 5 report pages, 39 visual containers, filters, and themes
│   │
│   └── Market-Business-Strategy-Intelligence.SemanticModel/ # Semantic Model artifact folder
│       ├── item.metadata.json                # V1 Model metadata (type: SemanticModel, displayName)
│       └── definition/
│           └── model.bim                     # Tabular model schema: 6 tables, columns, partitions, 35 DAX measures
│
├── outputs/                                  # Generated business deliverables
│   └── Market_Business_Strategy_Intelligence.xlsx # 7-Sheet interactive Excel workbook with formulas
│
└── docs/                                     # Comprehensive technical and strategic documentation
    ├── ANALYTICAL_ENGINE.md                  # Python analytical engine methodology and formulas
    ├── DATA_DICTIONARY.md                    # Column-by-column definitions, data types, and valid ranges
    ├── DATA_SOURCE_REGISTER.md               # Audit log of every primary source URL, access date, and note
    ├── EXCEL_ANALYSIS.md                     # Documentation of the 7-sheet Excel model and formulas
    ├── FINAL_KPI_REGISTRY.md                 # Complete catalog of all 35 KPIs, formulas, and verified flags
    ├── GEOGRAPHIC_ANALYSIS.md                # Geographic Attractiveness Index (GAI) framework and weights
    ├── KPI_FRAMEWORK.md                      # Strategic KPI classification (Competitive, Pricing, Geographic)
    ├── POWER_BI_DASHBOARD_SPEC.md            # Detailed visual container layout, coordinates, and visual types
    ├── POWER_BI_DAX.md                       # Comprehensive DAX measure definitions and logic
    ├── POWER_BI_KPI_MAPPING.md               # Mapping of KPIs to specific Power BI visuals and pages
    ├── POWER_BI_MODEL.md                     # Tabular data model schema, relationships, and tables
    ├── POWER_BI_POWER_QUERY.md               # Power Query M partition documentation
    ├── PRODUCT_POSITIONING.md                # 2x2 positioning matrix definitions and whitespace logic
    ├── RESUME_CLAIM_AUDIT.md                 # Objective evidence audit against resume bullet points
    ├── RESUME_CLAIM_VALIDATION.md            # Detailed breakdown of Claim 1, Claim 2, and Claim 3 status
    ├── SQL_ANALYTICS.md                      # DuckDB warehouse architecture, SQL scripts, and marts
    ├── STRATEGIC_ANALYSIS.md                 # Strategic entry recommendations for Alpha Motors
    └── UNIT_ECONOMICS.md                     # Vehicle BOM cost breakdown, sensitivity, and break-even math
```

---

## 5. System Architecture

### Architectural Pattern
The system implements a **Separation-of-Concerns Analytical Data Pipeline**. Raw sources are ingested through strongly typed validation layers, modeled inside an embedded SQL OLAP warehouse, and exposed through presentation layers (Excel OpenXML and Power BI PBIP) backed by strict data governance.

```
[PRIMARY SOURCES]
  - OEM Official Portals (Ather, Bajaj, TVS, Ola, Hero VIDA, Ultraviolette, etc.)
  - ARAI Technical Certification Disclosures
  - Regulatory / SEBI DRHP Filings (Ola Electric, Ather Energy)
                           │
                           ▼
[INGESTION & AUDIT LAYER] (src/data_processing.py)
  - Provenance classification (VERIFIED vs. PROXY_DEPRECATED)
  - SHA-256 Checksum fingerprinting
  - Schema validation & non-negative type coercion
  - State code standardization (36 States/UTs)
                           │
                           ▼
[DATA STORAGE & WAREHOUSING] (DuckDB: data/processed/sql/e2w_sql.duckdb)
  - Staging: stg_verified_products
  - Dimensions: dim_manufacturer, dim_product
  - Facts: fact_product_metrics
  - Analytical Marts: mart_competitive_analysis, mart_pricing_analysis, mart_product_positioning
  - Quality Layer: 10 Automated Data Quality Constraints (sql_data_quality_results)
  - Fail-Closed Schemas: pending.fact_ev_registrations (0 rows)
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
[PYTHON ANALYTICAL ENGINE]         [ANALYTICAL MARTS EXPORT]
  (src/analytics/)                   (data/processed/sql/*.csv)
  - Statistical percentiles & HHI                  │
  - Whitespace 2x2 classification                 │
  - Unit economics BOM sensitivity                 │
  - GAI decision framework                         │
          │                                 │
          ▼                                 ▼
[MICROSOFT EXCEL LAYER]            [POWER BI BI/DAX LAYER]
  (src/generate_excel_workbook.py)   (powerbi/Market-Business-Strategy-Intelligence.pbip)
  - 7 Structured sheets              - SemanticModel/definition/model.bim
  - Dynamic OpenXML formulas         - Report/definition/report.json (5 Pages, 39 Visuals)
  - outputs/*.xlsx                   - 35 DAX Measures (25 Verified, 10 Fail-Closed BLANK)
```

---

## 6. End-to-End System Workflow

### Step-by-Step Execution Sequence

1. **Pipeline Execution**: The user executes `python src/data_processing.py`.
   - Reads `data/raw/DATASET_MANIFEST.csv` and loads `verified_product_catalog_2025_2026.csv`.
   - Computes SHA-256 checksums to verify that raw data has not been modified.
   - Converts strings to numeric floats (`ex_showroom_price_inr`, `battery_capacity_kwh`, `range_km`, `top_speed_kmh`, `motor_peak_power_kw`).
   - Normalizes state names and codes against the master Indian states registry (`STATES` dictionary).
   - Invokes Python analytics modules (`src/analytics/`) to compute HHI, positioning buckets, and unit economics.
   - Emits cleaned analytical CSVs into `data/processed/` and logs audit metadata to `validation_results.json`.

2. **SQL Warehouse Execution**: The user executes `python src/run_sql_pipeline.py`.
   - Initializes or connects to `data/processed/sql/e2w_sql.duckdb`.
   - Executes scripts `01_schema.sql` through `08_pending_market_queries.sql`.
   - Script `02_load_verified_data.sql` ingests the processed CSV into `stg_verified_products` and populates `dim_manufacturer`, `dim_product`, and `fact_product_metrics`.
   - Script `03_data_quality.sql` executes 10 validation queries verifying that prices are positive, ranges exceed 20 km, and HHI is within expected mathematical limits.
   - Scripts `04`–`07` build views and export them to standalone CSV marts (`sql_competitive_analysis.csv`, `sql_pricing_analysis.csv`, `sql_product_positioning.csv`, `sql_kpi_results.csv`).
   - Script `08` sets up empty schemas in the `pending` namespace.

3. **Excel Workbook Generation**: The user executes `python src/generate_excel_workbook.py`.
   - Reads the exported DuckDB CSV marts.
   - Formats headers, fonts, and borders using XlsxWriter.
   - Writes 7 sheets: `Executive_Summary`, `Competitive_Intelligence`, `Pricing_Analysis`, `Product_Positioning`, `Strategic_Recommendations`, `Data_Quality_Governance`, and `Source_Manifest`.
   - Injects native Excel formulas (`AVERAGE`, `MEDIAN`, `MIN`, `MAX`, `SUM`) and exports `outputs/Market_Business_Strategy_Intelligence.xlsx`.

4. **Power BI Project Validation**: The user executes `python powerbi/validate_pbip.py`.
   - Parses `powerbi/Market-Business-Strategy-Intelligence.pbip` and verifies report path references.
   - Inspects `powerbi/Market-Business-Strategy-Intelligence.Report/definition.pbir` and verifies the relative path to `../Market-Business-Strategy-Intelligence.SemanticModel`.
   - Parses `report.json`, asserting that exactly 5 pages and 30+ visual containers are configured.
   - Parses `model.bim`, verifying that all 6 tables exist, CSV file paths exist on disk, and 10 pending market measures strictly evaluate to `BLANK()`.
   - Exits with return code 0 on passing all 14 checks.

5. **Power BI Desktop Execution**:
   - Power BI Desktop opens `powerbi/Market-Business-Strategy-Intelligence.pbip`.
   - Spawns the internal Microsoft Analysis Services tabular engine (`msmdsrv.exe`).
   - Power Query M partitions execute `File.Contents` on local CSV marts and load 42 records per table into tabular memory.
   - The 5 report pages render cards, scatter plots, bar charts, and matrix tables.
   - The user selects **File > Save As** to compile the standalone binary `Market-Business-Strategy-Intelligence.pbix`.

---

## 7. Feature-by-Feature Breakdown

### Feature 1: Primary Source Competitor Catalog & Provenance Register
- **Purpose**: Establishes an uncompromised ground-truth dataset of 42 commercial electric two-wheelers across 11 manufacturers.
- **Implementation**: `data/raw/verified_product_catalog_2025_2026.csv` and `docs/DATA_SOURCE_REGISTER.md`.
- **Fields Tracked**: Manufacturer, model name, ex-showroom price (INR), battery capacity (kWh), IDC certified range (km), top speed (km/h), motor peak power (kW), launch status, source URL, access timestamp, verification notes, and provenance class (`VERIFIED`).
- **Manufacturers Covered**: Ather Energy (8 models), Bajaj Auto (5 models), BGauss (3 models), Greaves Electric Mobility / Ampere (2 models), Hero MotoCorp / VIDA (3 models), Kinetic Green (2 models), Ola Electric (9 models), Revolt Motors (2 models), Simple Energy (2 models), TVS Motor Company (6 models), Ultraviolette Automotive (2 models). Total: 42 products.

### Feature 2: Competitive Intensity & Portfolio HHI Analysis
- **Purpose**: Measures product catalog concentration and competitor breadth.
- **Implementation**: `src/analytics/competitive_analysis.py` and `sql/04_competitive_analysis.sql`.
- **Metric**: Herfindahl-Hirschman Index (HHI) calculated across OEM product portfolio share:
  $$\text{HHI} = \sum_{i=1}^{N} \left( \frac{\text{Products}_i}{\text{Total Products}} \times 100 \right)^2 = 1,326.5$$
- **Interpretation**: A score of 1,326.5 places the catalog in the unconcentrated to moderately concentrated bracket (HHI < 1,500), proving vibrant catalog competition between pure-play EV pioneers and incumbent automotive conglomerates.

### Feature 3: Pricing Architecture & Quartile Distribution
- **Purpose**: Establishes price distribution benchmarks and quartile thresholds for market entrants.
- **Implementation**: `src/analytics/pricing_analysis.py` and `sql/05_pricing_analysis.sql`.
- **Metrics**:
  - Sample: 34 priced commercial models (8 models pending official commercial price disclosures).
  - Minimum Price: ₹74,990 (Kinetic Green E-Luna moped).
  - Maximum Price: ₹3,99,000 (Ultraviolette F77 Recon performance motorcycle).
  - Average Price: ₹1,36,349.
  - Median Price: ₹1,26,171.
  - Quartiles: Q1 = ₹1,12,499; Q2 = ₹1,26,171; Q3 = ₹1,46,658; Q4 = ₹3,99,000.
  - Price Tiers: Budget (< ₹1,00,000; 6 models), Mid-Market (₹1,00,000–₹1,80,000; 26 models), Premium (> ₹1,80,000; 2 models).

### Feature 4: Value Proposition Metrics (Price-per-KM & Price-per-kWh)
- **Purpose**: Evaluates vehicle efficiency and consumer value equations.
- **Implementation**: `src/analytics/pricing_analysis.py` (`compute_price_per_km_and_kwh`).
- **Formulas**:
  $$\text{Price per KM} = \frac{\text{Ex-Showroom Price (INR)}}{\text{Certified IDC Range (km)}}$$
  $$\text{Price per kWh} = \frac{\text{Ex-Showroom Price (INR)}}{\text{Battery Capacity (kWh)}}$$
- **Market Benchmarks**:
  - Average Price per KM: ₹867.71/km across priced models.
  - Value Leaders: Ola S1 X Plus 5.2 kWh (₹406.25/km), Ola S1 X Plus 4 kWh (₹500.00/km), Kinetic Green E-Luna (₹681.73/km), Hero VIDA V1 Plus (₹683.92/km), TVS iQube ST 5.3 kWh (₹692.82/km).

### Feature 5: Product Positioning & Whitespace Mapping
- **Purpose**: Maps the competitive landscape across a 2x2 matrix and identifies unserved catalog whitespace.
- **Implementation**: `src/analytics/positioning_analysis.py` and `sql/06_product_positioning.sql`.
- **Classification Schema**:
  - Price Buckets: `Budget (< ₹1,00,000)`, `Mid-Market (₹1,00,000–₹1,80,000)`, `Premium (> ₹1,80,000)`.
  - Range Buckets: `Short-Range (< 100 km)`, `Standard-Range (100–150 km)`, `Long-Range (> 150 km)`.
  - Performance Buckets: `Commuter (< 70 km/h)`, `High-Speed (70–95 km/h)`, `Performance (> 95 km/h)`.
- **Identified Whitespace**: The **Budget Standard-Range** quadrant (< ₹1,00,000 price point with 120–160 km certified range) is unserved by legacy incumbents. Current offerings under ₹1,00,000 are low-speed mopeds or have sub-100 km range, while full-featured commuter scooters cluster above ₹1,15,000.

### Feature 6: Unit Economics & Battery BOM Sensitivity Model
- **Purpose**: Evaluates cost structures, gross margin profiles, and break-even production targets.
- **Implementation**: `src/analytics/unit_economics.py` (`compute_unit_economics`).
- **Model Parameters**:
  - Target ASP: ₹1,20,000 ex-showroom.
  - Battery Pack Cost Sensitivity: Evaluated from $90/kWh to $140/kWh. At a baseline of $115/kWh, a 3.5 kWh pack costs ~₹38,000–₹42,000 (representing ~35%–42% of vehicle BOM).
  - Chassis, Frame & Mechanicals: ₹20,000.
  - Motor, Controller & Inverter: ₹14,000.
  - BMS & Power Electronics: ₹8,000.
  - Variable Assembly & Freight: ₹6,500.
  - Baseline Margins: Gross margin ~24.5%; Contribution margin ~18.2% post-PM E-DRIVE subsidy phase-out.
  - Break-Even Volume: ~38,000 units annually against ₹45 Cr in fixed corporate overhead and tooling amortization.

### Feature 7: Geographic Attractiveness Index (GAI) Framework
- **Purpose**: Multi-criteria decision model sequencing market rollout across 36 Indian States and Union Territories.
- **Implementation**: `src/analytics/geographic_analysis.py` (`compute_gai_template`).
- **Formula**:
  $$\text{GAI}_s = 0.30 \cdot V_s + 0.25 \cdot I_s + 0.20 \cdot D_s + 0.15 \cdot P_s + 0.10 \cdot U_s$$
  Where $V_s$ = Normalized EV Registration Volume, $I_s$ = Per Capita Income, $D_s$ = 2W Density, $P_s$ = State Policy Subsidies, $U_s$ = Urbanization Rate.
- **Governance Safeguard**: Because official multi-year Vahan portal exports remain pending, the volume factor $V_s$ is fail-closed, and state rankings remain a transparent mathematical template rather than speculative claims.

---

## 8. Frontend Architecture (Power BI Report PBIR)

The presentation layer is implemented as an authored Power BI Project (`powerbi/Market-Business-Strategy-Intelligence.Report/definition/report.json`). It specifies **5 report pages** containing **39 visual containers**:

```
+───────────────────────────────────────────────────────────────────────────+
|               POWER BI REPORT STRUCTURE (report.json: 5 Pages)            |
+───────────────────────────────────────────────────────────────────────────+
| 1. Executive Market & Business Overview (11 Visual Containers)            |
|    - Visual 1: Header & Governance Banner                                 |
|    - Visuals 2-5: KPI Cards (Total Products, OEMs, Avg Price, Price Spread)|
|    - Visual 6: OEM Product Breadth (Stacked Bar Chart)                    |
|    - Visual 7: Price Tier Distribution (Donut Chart)                      |
|    - Visual 8: Average Price vs. Market Benchmark Comparison             |
|    - Visual 9: Top Speed vs. Motor Power Comparison                       |
|    - Visual 10: Executive Strategic Guidance Callout                      |
|    - Visual 11: Fail-Closed Market Registration Status Card               |
+───────────────────────────────────────────────────────────────────────────+
| 2. Product & Competitive Intelligence (6 Visual Containers)               |
|    - Visual 1: Page Header & Subtitle                                     |
|    - Visuals 2-3: Interactive Slicers (Manufacturer, Vehicle Category)    |
|    - Visual 4: Battery Capacity vs. Range Scatter Plot (Color = OEM)      |
|    - Visual 5: Technical Specifications Comparison Matrix (42 Models)     |
|    - Visual 6: OEM Portfolio Breadth Bar Chart                            |
+───────────────────────────────────────────────────────────────────────────+
| 3. Pricing & Value Analysis (6 Visual Containers)                         |
|    - Visual 1: Page Header                                                |
|    - Visual 2: Ex-Showroom Price Distribution Histogram                   |
|    - Visual 3: Price vs. Certified Range Scatter Plot                     |
|    - Visual 4: Value Leaderboard (Price per KM & Price per kWh)           |
|    - Visual 5: Pricing Quartile Summary Cards (Q1, Median, Q3, Q4)        |
|    - Visual 6: Detailed Model Pricing & Value Ranking Table               |
+───────────────────────────────────────────────────────────────────────────+
| 4. Product Positioning & Whitespace Analysis (6 Visual Containers)        |
|    - Visual 1: Page Header                                                |
|    - Visual 2: Price vs. Certified Range 2x2 Positioning Scatter Plot     |
|    - Visual 3: Price Tier Distribution Donut Chart                        |
|    - Visual 4: Range Bracket Distribution Donut Chart                     |
|    - Visual 5: Identified Whitespace Opportunity Callout Box              |
|    - Visual 6: Full 42-Model Positioning & Segmentation Table             |
+───────────────────────────────────────────────────────────────────────────+
| 5. Strategy & Opportunity Framework (10 Visual Containers)                |
|    - Visual 1: Page Header                                                |
|    - Visual 2: Strategic Entry Opportunity Matrix for Alpha Motors        |
|    - Visual 3: Unit Economics BOM & Contribution Margin Waterfall         |
|    - Visual 4: Geographic Attractiveness Index (GAI) Framework Grid       |
|    - Visual 5: KPI Governance Registry Status Table (Verified vs Pending) |
|    - Visuals 6-10: Strategic Indicator Cards & Action Priorities         |
+───────────────────────────────────────────────────────────────────────────+
```

### Technical Visual Specification
- Canvas dimensions: 1280 x 720 pixels (standard 16:9 widescreen layout).
- Visual types utilized: `card`, `scatterChart`, `clusteredBarChart`, `clusteredColumnChart`, `donutChart`, `matrix`, `tableEx`, `slicer`, `textbox`.
- Coordinate layout: Fully assigned bounding boxes (`x`, `y`, `width`, `height`, `z-index`) ensuring zero visual overlapping.
- Visual configurations contain full `prototypeQuery` trees referencing `_Measures` and dimensional columns.

---

## 9. Backend Architecture (Python & DuckDB)

### Python Analytical Pipeline
- **Entry point**: `src/data_processing.py`
- **Orchestration**: `src/run_sql_pipeline.py`
- **Execution pattern**: Functional, deterministic data pipelines without long-running background daemons.
- **Module Breakdown**:
  - `src/analytics/competitive_analysis.py`: Computes market breadth, manufacturer share, and portfolio HHI.
  - `src/analytics/pricing_analysis.py`: Computes percentiles, quartiles, price-per-km, and price-per-kWh.
  - `src/analytics/positioning_analysis.py`: Bins models into price, range, and performance quadrants.
  - `src/analytics/unit_economics.py`: Calculates vehicle BOM, gross margins, and contribution margins.
  - `src/analytics/geographic_analysis.py`: Evaluates the 5-factor Geographic Attractiveness Index.
  - `src/analytics/kpi_engine.py`: Emits a standardized 35-metric KPI registry with verification flags.

### DuckDB SQL Warehouse Layer
- Embedded zero-dependency OLAP database stored in `data/processed/sql/e2w_sql.duckdb`.
- Operates in-process with zero network overhead, leveraging columnar vectorization.
- Schema architecture:
  - `stg`: Ingests strongly typed product specifications.
  - `dim`: Contains `dim_manufacturer` and `dim_product`.
  - `fact`: Contains `fact_product_metrics`.
  - `mart`: Analytical views exported to CSV for Power BI and Excel ingestion.
  - `kpi`: Houses `kpi_status` tracking governance boundaries.
  - `pending`: Houses empty tables for external registration data.

---

## 10. API Documentation (Data Marts & Interfaces)

Because this is a standalone analytical intelligence system, the "APIs" are structured data contracts exposed via DuckDB SQL views and standardized CSV data marts:

### Mart 1: `mart_competitive_analysis` (`sql_competitive_analysis.csv`)
- **Location**: `data/processed/sql/sql_competitive_analysis.csv`
- **Schema**: 42 rows, 18 columns.
- **Fields**: `product` (VARCHAR), `manufacturer` (VARCHAR), `price` (DOUBLE), `battery_capacity_kwh` (DOUBLE), `range_km` (DOUBLE), `top_speed_kmh` (DOUBLE), `motor_power_kw` (DOUBLE), `price_per_km` (DOUBLE), `price_per_kwh` (DOUBLE), `manufacturer_product_count` (BIGINT), `manufacturer_product_share_pct` (DOUBLE), `market_avg_price` (DOUBLE), `market_avg_range` (DOUBLE), `market_avg_battery` (DOUBLE), `power_to_weight_proxy` (DOUBLE), `range_per_kwh` (DOUBLE), `provenance_class` (VARCHAR), `eligible_as_observed_analytics` (VARCHAR).

### Mart 2: `mart_pricing_analysis` (`sql_pricing_analysis.csv`)
- **Location**: `data/processed/sql/sql_pricing_analysis.csv`
- **Schema**: 42 rows, 15 columns.
- **Fields**: `product`, `manufacturer`, `price`, `battery_capacity_kwh`, `range_km`, `top_speed_kmh`, `price_per_km`, `price_per_kwh`, `price_percentile` (DOUBLE), `price_quartile` (BIGINT), `product_price_rank` (BIGINT), `avg_market_price` (DOUBLE), `mfg_avg_price` (DOUBLE), `relative_price_position` (DOUBLE), `price_premium_vs_market_pct` (DOUBLE).

### Mart 3: `mart_product_positioning` (`sql_product_positioning.csv`)
- **Location**: `data/processed/sql/sql_product_positioning.csv`
- **Schema**: 42 rows, 18 columns.
- **Fields**: `product`, `manufacturer`, `model_name`, `price`, `range_km`, `battery_capacity_kwh`, `top_speed_kmh`, `motor_power_kw`, `price_bucket` (VARCHAR), `range_bucket` (VARCHAR), `performance_bucket` (VARCHAR), `positioning_summary` (VARCHAR), `is_whitespace_candidate` (BOOLEAN), `price_rank_in_range_bucket` (BIGINT), `range_rank_in_price_bucket` (BIGINT), `segment_code` (VARCHAR), `provenance_class` (VARCHAR), `eligible_as_observed_analytics` (VARCHAR).

### Mart 4: `kpi_status` (`sql_kpi_results.csv`)
- **Location**: `data/processed/sql/sql_kpi_results.csv`
- **Schema**: 14 rows, 7 columns.
- **Fields**: `kpi_id`, `kpi_name`, `kpi_category`, `kpi_value_display`, `calculation_basis`, `status`, `notes`.

---

## 11. Database Architecture (DuckDB Schema)

```sql
-- DDL Definitions from sql/01_schema.sql

CREATE TABLE stg_verified_products (
    manufacturer VARCHAR,
    model_name VARCHAR,
    vehicle_category VARCHAR,
    ex_showroom_price_inr DOUBLE,
    price_basis VARCHAR,
    battery_capacity_kwh DOUBLE,
    range_km DOUBLE,
    range_standard VARCHAR,
    top_speed_kmh DOUBLE,
    motor_peak_power_kw DOUBLE,
    launch_status VARCHAR,
    source_url VARCHAR,
    source_type VARCHAR,
    accessed_date DATE,
    verification_status VARCHAR,
    verification_notes VARCHAR,
    source_dataset VARCHAR,
    provenance_class VARCHAR,
    eligible_as_observed_analytics VARCHAR,
    source VARCHAR DEFAULT 'verified_product_catalog_2025_2026.csv'
);

CREATE TABLE dim_manufacturer (
    manufacturer VARCHAR PRIMARY KEY,
    product_count BIGINT,
    priced_product_count BIGINT,
    min_price_inr DOUBLE,
    max_price_inr DOUBLE,
    avg_price_inr DOUBLE,
    median_price_inr DOUBLE,
    verification_status VARCHAR,
    source VARCHAR
);

CREATE TABLE dim_product (
    product_id VARCHAR PRIMARY KEY,
    model_name VARCHAR,
    manufacturer VARCHAR,
    vehicle_category VARCHAR,
    price_basis VARCHAR,
    range_standard VARCHAR,
    launch_status VARCHAR,
    provenance_class VARCHAR,
    eligible_as_observed_analytics VARCHAR,
    source_url VARCHAR
);

CREATE TABLE fact_product_metrics (
    product_id VARCHAR PRIMARY KEY,
    ex_showroom_price_inr DOUBLE,
    battery_capacity_kwh DOUBLE,
    range_km DOUBLE,
    top_speed_kmh DOUBLE,
    motor_peak_power_kw DOUBLE,
    price_per_km DOUBLE,
    price_per_kwh DOUBLE,
    source VARCHAR
);
```

### Automated Data Quality Rules (`sql/03_data_quality.sql`)
1. `dq_min_product_count`: Asserts product count >= 30 (Observed: 42).
2. `dq_min_manufacturer_count`: Asserts manufacturer count >= 5 (Observed: 11).
3. `dq_positive_prices`: Asserts all prices > 0 (No zero or negative prices).
4. `dq_positive_battery_capacities`: Asserts battery capacities > 0.
5. `dq_realistic_range`: Asserts certified range >= 20 km.
6. `dq_provenance_integrity`: Asserts 100% of staging rows carry `provenance_class = 'VERIFIED'`.
7. `dq_no_duplicate_products`: Asserts zero duplicate `(manufacturer, model_name)` pairs.
8. `dq_valid_vehicle_categories`: Asserts vehicle category in `('Scooter', 'Motorcycle', 'Moped')`.
9. `dq_hhi_bounds`: Asserts catalog HHI is between 500 and 5,000.
10. `dq_price_per_km_bounds`: Asserts price per km is between ₹200/km and ₹3,000/km.

---

## 12. Authentication and Authorization

- **Authentication Posture**: As a local corporate business intelligence repository, there are no web login endpoints, JWT tokens, or OAuth flows.
- **Data Governance Access Control**: Enforced through file-system permissions and git version control.
- **External Portal Authentication**: MoRTH Vahan portals require dynamic visual CAPTCHA authentication and human session verification, preventing programmatic headless scraping. This architectural reality is why external market registration datasets remain fail-closed.

---

## 13. AI / ML Architecture

The repository utilizes **deterministic statistical and econometric models** rather than opaque neural networks, prioritizing 100% auditability for corporate strategy:

1. **Portfolio Concentration Model**:
   Computes Herfindahl-Hirschman Index (HHI) across competitor catalog offerings to quantify market power and competitive density.
2. **Statistical Distribution Models**:
   Computes median, quartiles, interquartile ranges (IQR), and percentile ranks (`NTILE(4)`, `PERCENT_RANK()`) across pricing and powertrain dimensions.
3. **Product Whitespace Classification Algorithm**:
   Multi-dimensional boundary classification identifying gaps in the 2x2 price-range continuum. Flags candidate whitespace models satisfying:
   $$\text{Price} < \text{Mid-Market Floor (₹1,00,000)} \quad \land \quad \text{Range} \ge \text{Commuter Standard (120 km)}$$
4. **Geographic Multi-Criteria Decision Model (GAI)**:
   Linear weighted sum model combining 5 normalized socioeconomic and infrastructure vectors.
5. **Unit Economics Sensitivity Engine**:
   Deterministic cost-volume-profit (CVP) model evaluating battery cell cost fluctuations ($/kWh) against vehicle gross contribution margins.

---

## 14. LLM / Generative AI Architecture

- **Status in Repository**: There is **no runtime external LLM API dependency** (e.g., no OpenAI, Anthropic, or HuggingFace API calls during data execution).
- **Prompt Templates & Frameworks**:
  - `src/analytics/geographic_analysis.py` contains structured prompt and strategic scenario templates (`compute_gai_template`).
  - `src/analytics/scenario_analysis.py` defines structured strategic evaluation frameworks designed for executive synthesis.
- **Design Philosophy**: Quantitative data points, rankings, and financial margins are strictly computed via deterministic code, ensuring zero LLM hallucination in analytical reporting.

---

## 15. RAG Architecture

- **Status in Repository**: Vector embeddings and vector databases (e.g., Pinecone, Chroma, FAISS) are **not utilized**.
- **Deterministic Knowledge Index**: The repository replaces probabilistic RAG with an auditable **Primary Source Register** ([`docs/DATA_SOURCE_REGISTER.md`](file:///c:/Users/Tanya%20Verma/OneDrive/Desktop/Market-Business-Strategy-Intelligence/docs/DATA_SOURCE_REGISTER.md)) and dataset manifest ([`data/raw/DATASET_MANIFEST.csv`](file:///c:/Users/Tanya%20Verma/OneDrive/Desktop/Market-Business-Strategy-Intelligence/data/raw/DATASET_MANIFEST.csv)), tracking exact URLs, retrieval dates, and ARAI certificate numbers.

---

## 16. Agent / Agentic AI Architecture

- **Status in Repository**: The codebase does not run an autonomous background multi-agent loop (e.g., LangGraph, AutoGen, CrewAI).
- **Orchestration**: Operates as an orchestrated deterministic workflow driven by modular Python scripts (`run_sql_pipeline.py`, `data_processing.py`, `generate_excel_workbook.py`).

---

## 17. AI/ML + Application Integration

The integration of statistical analytics into business intelligence artifacts follows a strict contract:
1. **Python Analytics Engine** computes derived metrics (e.g., HHI, value scores, unit economics).
2. **DuckDB SQL Marts** materialize these metrics into relational tables.
3. **Power BI Tabular Model** imports the marts via M partitions.
4. **DAX Measures** compute dynamic aggregations over the imported marts.
5. **Report Visuals** bind directly to DAX measures and dimensional columns, guaranteeing that visual charts display mathematically verified figures.

---

## 18. Data Flow

```
+─────────────────────────────────────────────────────────────+
|               STEP 1: RAW DATA ACQUISITION                  |
|  - data/raw/verified_product_catalog_2025_2026.csv          |
|  - 42 commercial products across 11 manufacturers           |
+─────────────────────────────────────────────────────────────+
                               │
                               ▼
+─────────────────────────────────────────────────────────────+
|          STEP 2: INGESTION & INTEGRITY AUDIT                |
|  - src/data_processing.py                                   |
|  - SHA-256 fingerprinting & manifest verification           |
|  - Exports: data/processed/processed_verified_product_catalog|
+─────────────────────────────────────────────────────────────+
                               │
                               ▼
+─────────────────────────────────────────────────────────────+
|          STEP 3: DUCKDB WAREHOUSE & MARTS                   |
|  - src/run_sql_pipeline.py -> e2w_sql.duckdb                |
|  - Executes sql/01_schema.sql through 08_pending_market.sql |
|  - 10 Data Quality Assertion Rules passed                   |
|  - Exports: data/processed/sql/sql_*.csv                    |
+─────────────────────────────────────────────────────────────+
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
+───────────────────────────+         +───────────────────────────+
|  STEP 4A: EXCEL MODEL     |         |  STEP 4B: POWER BI PBIP   |
|  - generate_excel_workbook|         |  - validate_pbip.py       |
|  - 7 OpenXML sheets       |         |  - model.bim (6 tables)   |
|  - Dynamic formulas       |         |  - report.json (5 pages)  |
|  - outputs/*.xlsx         |         |  - 35 DAX measures        |
+───────────────────────────+         +───────────────────────────+
```

---

## 19. Important Classes, Functions and Modules

### 1. `src/data_processing.py`
- `audit(dataset, df, meta)`: Evaluates missing required columns, counts duplicate rows, and records SHA-256 checksums.
- `numeric(df, columns, report)`: Converts required string columns to numeric floats, flagging negative or non-numeric values as errors.
- `optional_numeric(df, columns, report)`: Coerces optional specifications without treating absent values as fatal errors.
- `standardise_state(df, state_column, report)`: Normalizes state names using the `STATES` mapping and `ALIASES` dictionary.

### 2. `src/run_sql_pipeline.py`
- `run_sql_pipeline(db_path, project_root)`: Main orchestrator connecting to DuckDB, executing scripts `01` through `08`, enforcing data quality checks, and exporting analytical CSV marts.

### 3. `src/analytics/competitive_analysis.py`
- `compute_manufacturer_breadth(df)`: Calculates model counts per OEM and computes portfolio share percentages.
- `compute_portfolio_hhi(df)`: Computes the Herfindahl-Hirschman Index across product offerings.

### 4. `src/analytics/pricing_analysis.py`
- `compute_pricing_metrics(df)`: Calculates average, median, min, max, and quartile distributions.
- `compute_price_per_km_and_kwh(df)`: Computes value efficiency ratios.

### 5. `src/analytics/positioning_analysis.py`
- `classify_product_positioning(df)`: Assigns price tiers (`Budget`, `Mid-Market`, `Premium`) and range brackets (`Short-Range`, `Standard-Range`, `Long-Range`).
- `identify_whitespace_candidates(df)`: Filters models meeting target whitespace criteria.

### 6. `src/analytics/unit_economics.py`
- `compute_unit_economics(target_asp, battery_kwh, cell_cost_usd_kwh, ...)`: Computes itemized vehicle BOM, gross margins, and contribution margins.

### 7. `src/generate_excel_workbook.py`
- `build_excel_workbook()`: Generates `outputs/Market_Business_Strategy_Intelligence.xlsx` with 7 formatted worksheets.

### 8. `powerbi/validate_pbip.py`
- `validate_pbip()`: 14-check validation suite testing PBIP entry points, semantic model path references, report page counts, visual container counts, and DAX fail-closed behavior.

---

## 20. Configuration

- **Database Path**: `data/processed/sql/e2w_sql.duckdb` (configured in `src/run_sql_pipeline.py`).
- **Data Mart Export Directory**: `data/processed/sql/`.
- **Excel Output Path**: `outputs/Market_Business_Strategy_Intelligence.xlsx`.
- **PBIP Root**: `powerbi/Market-Business-Strategy-Intelligence.pbip`.
- **Report Definition**: `powerbi/Market-Business-Strategy-Intelligence.Report/definition/report.json`.
- **Semantic Model Definition**: `powerbi/Market-Business-Strategy-Intelligence.SemanticModel/definition/model.bim`.

---

## 21. Environment Variables

| Variable | Purpose | Required | Used By | Example / Safe Placeholder |
|---|---|---|---|---|
| `DUCKDB_DATABASE_PATH` | Override path to DuckDB database file | No | `src/run_sql_pipeline.py` | `data/processed/sql/e2w_sql.duckdb` |
| `PROJECT_ROOT` | Override root directory for pipeline execution | No | Python scripts | `C:/Users/.../Market-Business-Strategy-Intelligence` |
| `PYTHONPATH` | Python module resolution path | Recommended | `pytest`, Python runner | `.` or `src/` |

*Security Notice: The repository contains zero private API keys, secrets, or confidential credentials.*

---

## 22. External Services and APIs

1. **OEM Manufacturer Portals**: Source of vehicle ex-showroom prices and technical specifications (Ather Energy, Bajaj Auto, TVS Motor, Ola Electric, etc.). Accessed during primary research; not called dynamically at runtime.
2. **ARAI Certification Disclosures**: Automotive Research Association of India certified IDC range disclosures.
3. **SEBI DRHP Regulatory Disclosures**: Draft Red Herring Prospectuses for Ola Electric Mobility and Ather Energy.
4. **MoRTH Vahan Portal**: Ministry of Road Transport and Highways vehicle registration portal. Pending future integration; proxy data is quarantined.

---

## 23. Error Handling

1. **Pipeline Type Enforcement**: `src/data_processing.py` uses `pd.to_numeric(errors='coerce')` combined with assertion checks that fail if negative prices or invalid battery capacities are encountered.
2. **SQL Quality Gate**: `sql/03_data_quality.sql` executes 10 assertion queries. `src/run_sql_pipeline.py` reads `sql_data_quality_results` and halts execution if any check fails.
3. **Fail-Closed BI Architecture**: If market registration data is missing, DAX measures evaluate to `BLANK()` rather than zero or synthetic estimates:
   ```dax
   Market Registration Total [PENDING] = BLANK()
   ```
4. **PBIP Metadata Validation**: `powerbi/validate_pbip.py` verifies that `model.bim` does not contain unescaped path placeholders (`DATA_PATH`) and that JSON files parse without syntax errors.

---

## 24. Security

- **Provenance Tracking**: Every single product record in `data/processed/processed_verified_product_catalog.csv` contains `source_url`, `source_type`, `accessed_date`, and `verification_status`.
- **Cryptographic File Hashing**: Ingestion scripts compute SHA-256 digests of raw files to detect tampering.
- **Anti-Fabrication Policy**: Prevents synthetic data injection by enforcing fail-closed `BLANK()` values across all unverified metrics.
- **Zero Secrets Policy**: No hardcoded API keys, tokens, or personal identifiers exist in the repository.

---

## 25. CORS / Nginx / Networking / Reverse Proxy

- The project runs as an in-process local analytical application; no reverse proxy (Nginx/Apache) or CORS middleware is required.
- Power BI Desktop communicates locally with its internal Microsoft Analysis Services engine (`msmdsrv.exe`) over local TCP loopback (`localhost:<dynamic_port>`).

---

## 26. Docker / Deployment

- **Deployment Model**: Standalone, reproducible analytical repository.
- **Containerization**: Not containerized via Docker; designed for direct local execution in standard Python 3.11+ environments.
- **Portability**: All file paths inside `src/` and `sql/` are resolved dynamically relative to `PROJECT_ROOT`, ensuring cross-platform portability between Windows, macOS, and Linux.

---

## 27. Build and Runtime Process

### Reproduction Commands
```bash
# 1. Environment Setup
git clone https://github.com/tanyaverma20/Market-Business-Strategy-Intelligence.git
cd Market-Business-Strategy-Intelligence
python -m pip install -r requirements.txt

# 2. Data Processing Pipeline
python src/data_processing.py

# 3. DuckDB SQL Analytical Warehouse Pipeline
python src/run_sql_pipeline.py

# 4. Generate Microsoft Excel Analytical Model
python src/generate_excel_workbook.py

# 5. Validate Power BI Project (PBIP) Integrity
python powerbi/validate_pbip.py

# 6. Execute Full Automated Pytest Suite
python -m pytest -v
```

---

## 28. Testing

The repository features **38 passing automated tests** across 4 test suites:

### Test Suite 1: `src/tests/test_analytical_engine.py` (16 Tests)
- `test_category_distribution`: Verifies category splits across Scooter, Motorcycle, and Moped.
- `test_gai_template`: Verifies mathematical integrity of the GAI multi-criteria scoring template.
- `test_generate_kpi_outputs_accepts_processed_schema`: Verifies end-to-end KPI engine execution.
- `test_invalid_product_values_raise_errors`: Asserts that negative prices or invalid inputs raise errors.
- `test_market_status_requires_verified_data`: Confirms that market metrics require verified inputs.
- `test_missing_columns_and_duplicates_are_handled`: Asserts handling of missing schema attributes.
- `test_positioning_classification`: Tests price tier and range bracket assignment logic.
- `test_price_and_battery_comparison`: Tests cross-metric correlation logic.
- `test_price_per_km_and_kwh`: Validates value score calculations.
- `test_pricing_metrics`: Validates average, median, min, max, and quartile calculations.
- `test_product_count_and_manufacturer_count`: Asserts 42 products and 11 manufacturers.
- `test_product_positioning_summary`: Validates positioning summary generation.
- `test_range_realization_requires_both_ranges`: Asserts IDC vs. real-world range calculations.
- `test_rank_products_by_price_and_range`: Validates sorting and ranking logic.
- `test_unit_economics`: Tests vehicle BOM margin sensitivity calculations.
- `test_validate_required_columns_catches_missing_columns`: Tests validation gatekeeper.

### Test Suite 2: `src/tests/test_sql_pipeline.py` (9 Tests)
- `test_sql_pipeline_creates_verified_warehouse`: Asserts creation of `e2w_sql.duckdb`.
- `test_sql_pipeline_keeps_market_data_pending`: Verifies that `pending.fact_ev_registrations` has 0 rows.
- `test_sql_tables_and_views_structure`: Asserts presence of required staging, dimension, and mart tables.
- `test_sql_data_quality_integrity`: Asserts that all 10 SQL data quality checks pass.
- `test_sql_window_functions_and_rankings`: Verifies `ROW_NUMBER()` and `NTILE(4)` ranking accuracy.
- `test_sql_product_positioning_buckets`: Verifies price and range bucket allocations in SQL.
- `test_no_proxy_market_data_in_factual_sql_outputs`: Confirms that deprecated proxy data is excluded.

### Test Suite 3: `src/tests/test_powerbi_specification.py` (7 Tests)
- `test_powerbi_doc_files_exist`: Verifies presence of documentation files.
- `test_powerbi_script_files_exist`: Verifies presence of M scripts and DAX measure files.
- `test_dax_measures_syntactic_integrity`: Validates DAX syntax, parentheses matching, and keywords.
- `test_dax_column_references_align_with_sql_marts`: Verifies column references against SQL marts.
- `test_pending_market_measures_return_blank`: Asserts that all 10 pending measures return `BLANK()`.
- `test_dashboard_spec_covers_five_pages`: Asserts coverage of all 5 report pages.
- `test_pbip_project_entry_file_valid`: Asserts PBIP entry file integrity.
- `test_pbip_report_json_five_pages`: Validates `report.json` schema and visual container counts.
- `test_pbip_model_bim_valid_and_fail_closed`: Validates `model.bim` schema and fail-closed DAX.

### Test Suite 4: `src/tests/test_resume_validation.py` (5 Tests)
- `test_verified_manufacturer_count_meets_resume_claim`: Asserts >= 10 manufacturers (Observed: 11).
- `test_verified_product_count_meets_resume_claim`: Asserts >= 25 products (Observed: 42).
- `test_excel_workbook_exists_and_has_seven_sheets`: Asserts presence of 7 Excel sheets.
- `test_final_kpi_registry_contains_at_least_15_verified_kpis`: Asserts >= 15 verified KPIs (Observed: 25).
- `test_no_proxy_data_relabeled_as_verified`: Verifies zero proxy data leakage into verified tables.

### Test Suite 5: `src/test_data_processing.py` (1 Test)
- `test_legacy_alias_and_code_are_standardised`: Verifies Indian state aliases (Orissa -> Odisha, etc.).

---

## 29. Performance and Optimization

- **In-Memory Columnar OLAP**: DuckDB executes analytical queries across dimensions and facts in milliseconds.
- **Vectorized Pandas Operations**: Analytical computations utilize vectorized NumPy arrays rather than iterative Python loops.
- **Optimized Power Query Partitions**: M queries in `model.bim` read directly from pre-aggregated CSV marts rather than performing heavy unindexed transformations during Power BI dashboard rendering.

---

## 30. Important Design Decisions

### Decision 1: Power BI Project (PBIP) vs. Monolithic PBIX Binary
- **Decision**: Author the report in native Power BI Project (`.pbip` / PBIR) format.
- **Rationale**: Monolithic `.pbix` files are proprietary binary blobs that cannot be version-controlled, diffed, or programmatically validated. PBIP exposes `report.json` and `model.bim` as human-readable JSON, enabling CI/CD automated validation and transparent peer review.

### Decision 2: Embedded DuckDB vs. External PostgreSQL / SQLite
- **Decision**: Use DuckDB as the analytical warehouse.
- **Rationale**: Unlike SQLite (which lacks modern analytical window functions like `PERCENT_RANK()` and native parquet/CSV ingestion), DuckDB provides enterprise-grade columnar OLAP features in-process with zero client-server configuration.

### Decision 3: Fail-Closed BLANK() DAX Measures vs. Proxy Interpolation
- **Decision**: Quarantine unverified Vahan proxy data and return `BLANK()` for market registration metrics.
- **Rationale**: In professional business analysis and management consulting, presenting proxy estimates as audited market facts destroys professional credibility. A fail-closed architecture clearly distinguishes verified primary facts from pending external telemetry.

---

## 31. Technical Trade-offs

| Trade-off | Selected Approach | Alternative | Justification |
|---|---|---|---|
| **Storage Format** | CSV Marts for Power BI Import | Direct Parquet / Database Connector | Maximizes compatibility across all Power BI Desktop versions without requiring external ODBC drivers |
| **Catalog Scope** | 42 Verified Models (11 OEMs) | 200+ Scraped Web Models | Prioritizes complete, source-verified specification accuracy over noisy web-scraped estimates |
| **BI Architecture** | Version-Controlled PBIP | Compiled Binary PBIX | Enables automated git diffing and automated pytest test suites on report visuals |

---

## 32. Current Limitations

1. **Pending Vahan Registration Integration**: Official multi-year MoRTH Vahan registration data has not been integrated due to portal CAPTCHA restrictions.
2. **Registration-Dependent DAX Measures**: 10 measures evaluating market volume, OEM market share, and state penetration evaluate to `BLANK()`.
3. **Standalone Binary PBIX**: Requires a manual File > Save As action in Power BI Desktop to compile the PBIP source project into a single binary file.

---

## 33. Known Issues / Deprecations

- **Deprecated Legacy Files**: `data/raw/vahan_e2w_registrations_monthly.csv` and `data/raw/oem_e2w_registrations_annual.csv` are marked `PROXY_DEPRECATED` in `DATASET_MANIFEST.csv` and are barred from factual analytical queries.
- **Fixed Platform Conflict**: An earlier version contained an extraneous `.platform` file in `Market-Business-Strategy-Intelligence.SemanticModel/` that conflicted with `item.metadata.json`; `.platform` was deleted, restoring full PBIP compatibility.

---

## 34. Important Constants and Business Logic

### Pricing Tiers
- **Budget**: `< ₹1,00,000`
- **Mid-Market**: `₹1,00,000 – ₹1,80,000`
- **Premium**: `> ₹1,80,000`

### Range Brackets
- **Short-Range**: `< 100 km`
- **Standard-Range**: `100 – 150 km`
- **Long-Range**: `> 150 km`

### Performance Categories
- **Commuter**: `< 70 km/h`
- **High-Speed**: `70 – 95 km/h`
- **Performance**: `> 95 km/h`

### Geographic Attractiveness Index Weights
- Registration Volume: `0.30`
- Per Capita Income: `0.25`
- Two-Wheeler Density: `0.20`
- State EV Policy Incentives: `0.15`
- Urbanization Percentage: `0.10`

---

## 35. Complete Dependency Map

```
data/raw/verified_product_catalog_2025_2026.csv
                      ↓
           src/data_processing.py
                      ↓
data/processed/processed_verified_product_catalog.csv
                      ↓
             sql/01_schema.sql
             sql/02_load_verified_data.sql
             sql/03_data_quality.sql
             sql/04_competitive_analysis.sql
             sql/05_pricing_analysis.sql
             sql/06_product_positioning.sql
             sql/07_kpi_queries.sql
             sql/08_pending_market_queries.sql
                      ↓
       data/processed/sql/e2w_sql.duckdb
                      ↓
data/processed/sql/sql_competitive_analysis.csv
data/processed/sql/sql_pricing_analysis.csv
data/processed/sql/sql_product_positioning.csv
data/processed/sql/sql_kpi_results.csv
                      ↓
         ┌────────────┴────────────┐
         ↓                         ↓
src/generate_excel_workbook.py   powerbi/Market-Business-Strategy-Intelligence.pbip
         ↓                         ↓
outputs/*.xlsx                   Power BI Desktop (msmdsrv.exe)
                                 - 5 Report Pages (39 Visuals)
                                 - 35 DAX Measures
```

---

## 36. Important Runtime Sequences

### Sequence 1: Data Quality Assertion Sequence
1. `src/run_sql_pipeline.py` executes `sql/03_data_quality.sql`.
2. 10 assertion queries run against DuckDB staging and dimensional tables.
3. Each check outputs: `check_name`, `status` (`PASS`/`FAIL`), `observed_value`, `expected_criteria`.
4. Results are stored in the table `sql_data_quality_results`.
5. The pipeline queries `SELECT COUNT(*) FROM sql_data_quality_results WHERE status = 'FAIL'`.
6. If the count exceeds zero, a `ValueError` is raised, halting pipeline execution.

### Sequence 2: Power BI Semantic Model Refresh Sequence
1. Power BI Desktop initializes and reads `definition.pbir`.
2. `definition.pbir` directs the engine to `../Market-Business-Strategy-Intelligence.SemanticModel`.
3. Power BI reads `model.bim` and parses table definitions and DAX measures.
4. M Power Query partitions execute `Csv.Document(File.Contents("..."))` on each exported CSV mart.
5. Tabular data is ingested into Analysis Services memory (`msmdsrv.exe`).
6. Calculated DAX measures evaluate over the tables.
7. Visual containers in `report.json` update their renderings based on DAX query outputs.

---

## 37. Interview Perspective

### 30-Second Elevator Pitch
"I developed an end-to-end commercial strategy and market intelligence platform for the Indian electric two-wheeler market. Benchmarking 42 verified commercial models across 11 manufacturers, I integrated Python analytics, an embedded DuckDB SQL OLAP warehouse, an automated 7-sheet Excel model, and a 5-page Power BI Project with 35 DAX measures. A major highlight was engineering a strict fail-closed data governance architecture that cleanly isolates verified primary-source specifications from pending external Vahan registration telemetry, backed by 38 passing automated tests."

### 1-Minute Overview
"This project was designed for an entrant evaluating expansion into India's 15–20 million unit two-wheeler market under the PM E-DRIVE subsidy transition. I benchmarked 11 verified OEMs across 42 commercial models to analyze price distribution, portfolio HHI concentration (1,326.5), and price-per-km efficiency. Using a 2x2 positioning framework, I identified an unserved catalog whitespace in the Budget Standard-Range commuter segment (< ₹1 Lakh with 120–160 km range). Technically, the project spans modular Python analytics, an embedded DuckDB SQL warehouse with CTEs and window functions, an automated 7-sheet Excel workbook, and an authored 5-page Power BI Project with 39 visual containers. To preserve analytical credibility, I architected a fail-closed model where unavailable multi-year Vahan registration data evaluates to BLANK(), ensuring zero data fabrication."

### 2-Minute Technical Deep-Dive
"From an architectural standpoint, the project emphasizes reproducible data engineering and strict governance:
First, data ingestion in `data_processing.py` verifies raw inputs via SHA-256 digests and standardizes 36 Indian state codes.
Second, the SQL layer uses an embedded DuckDB database structured into staging, dimension, fact, mart, and pending schemas. I implemented 10 automated SQL data quality constraints verifying non-negative pricing, realistic battery capacities, and portfolio HHI boundaries before materializing analytical marts.
Third, in the presentation layer, I authored the Power BI dashboard as a source-controlled Power BI Project (`.pbip`), exposing `model.bim` and `report.json`. The semantic model contains 6 tables, M ETL partitions, and 35 DAX measures. 25 verified measures calculate market benchmarks, while 10 pending measures return `BLANK()` under fail-closed safeguards.
Fourth, the Python analytics engine models vehicle unit economics, evaluating cell pack sensitivity from $90 to $140/kWh and establishing that a 3.5 kWh battery represents ~38% of vehicle BOM at ₹1.2 Lakh target ASP.
The entire repository is validated by 38 automated pytest tests and 14 PBIP integrity checks."

### Potential Interview Questions & Key Technical Answers

1. **Why did you use a Power BI Project (PBIP) instead of a regular PBIX file?**
   - *Key Answer*: Monolithic `.pbix` binaries cannot be peer-reviewed, git-diffed, or inspected in CI/CD. PBIP decomposes the report into human-readable JSON (`report.json`) and tabular model BIM (`model.bim`), allowing automated Python scripts to validate DAX syntax, page structures, and path references.
2. **How did you handle missing or unverified market registration data?**
   - *Key Answer*: I implemented a fail-closed governance pattern. Rather than interpolating synthetic numbers or using unverified proxy datasets, I quarantined proxy data as `PROXY_DEPRECATED`, kept the registration tables empty (0 rows), and programmed all market-share DAX measures to return `BLANK()`.
3. **What is the commercial significance of the whitespace you identified?**
   - *Key Answer*: Mapping ex-showroom price against certified range revealed that 76.5% of commuter models cluster between ₹1.0 Lakh and ₹1.5 Lakh. Incumbents under ₹1.0 Lakh offer only low-speed mopeds or sub-110 km range. Developing a commuter scooter delivering 120–140 km range at ₹95,000 captures substantial unmet commuter demand.
4. **Why DuckDB instead of SQLite or PostgreSQL?**
   - *Key Answer*: DuckDB is an embedded columnar OLAP engine. Unlike SQLite, DuckDB natively supports advanced analytical window functions (`PERCENT_RANK()`, `NTILE()`), multi-threaded vectorized query execution, and seamless CSV exports without requiring a dedicated database server daemon.

---

## 38. Project Questions an AI Should Be Able to Answer

An external AI reading this document should be able to answer:
- **What is the exact verified catalog count?** 11 verified manufacturers and 42 commercial models (34 priced).
- **What are the market price benchmarks?** Minimum ₹74,990; Maximum ₹3,99,000; Average ₹1,36,349; Median ₹1,26,171.
- **What is the portfolio HHI and what does it mean?** 1,326.5; indicates an unconcentrated to moderately concentrated catalog landscape.
- **What is the average price-per-km?** ₹867.71/km.
- **How many Power BI report pages and visuals exist?** 5 pages and 39 visual containers.
- **How many DAX measures exist?** 35 measures (25 verified calculations and 10 fail-closed measures returning `BLANK()`).
- **How many automated tests exist?** 38 pytest tests (100% passing) and 14 PBIP integrity checks (100% passing).
- **What is the status of Vahan registration data?** Pending; isolated in empty schemas under fail-closed governance.
- **How are Indian states standardized?** Via the `STATES` dictionary and `ALIASES` mapping in `src/data_processing.py`.
- **How is the Excel workbook generated?** Via `src/generate_excel_workbook.py` using XlsxWriter to build 7 formatted sheets.

---

## 39. Source-of-Truth Rules

1. **Repository Supremacy**: The actual code, scripts, schemas, and tests in the repository constitute the ultimate source of truth.
2. **Zero Fabrication**: No external market registration numbers, state volume rankings, or historical CAGRs may be invented.
3. **Distinction of Status**: Always distinguish verified primary-source facts (catalog specs, pricing, HHI) from pending analytical frameworks (Vahan registrations, state market share).
4. **Audit Alignment**: Target resume claims are objectively categorized into Fully Supported (Claims 2 & 3) versus Partially Supported / Pending (Claim 1).

---

## 40. Final Project Summary

Market-Business-Strategy-Intelligence is an enterprise-grade commercial strategy intelligence system for India's electric two-wheeler market. Driven by 11 verified OEMs and 42 commercial models, it connects Python data processing, an embedded DuckDB OLAP warehouse, an automated 7-sheet Excel model, and a 5-page Power BI Project (PBIP) with 35 DAX measures into a single auditable architecture. Enforcing a strict fail-closed governance policy for pending external registration data, the project provides corporate strategists with an uncompromised, interview-defensible platform validated by 38 passing automated tests.
