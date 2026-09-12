# SQL Analytics Layer: Indian Electric 2-Wheeler Market

## 1. Executive Summary & SQL Architecture

The SQL Analytics Layer provides an embedded, reproducible, zero-cost analytical warehouse built on **DuckDB**. It processes the verified product catalog (`data/processed/processed_verified_product_catalog.csv`), enforces provenance and data quality checks, executes advanced analytical window queries, and outputs standardized data marts.

In strict adherence to the project's **provenance safeguard policy**, registration and market volume queries remain fail-closed in a dedicated `pending` schema with zero records until official Vahan registration exports are verified.

```
+-------------------------------------------------------------------------+
|                              DATA SOURCES                               |
|   data/processed/processed_verified_product_catalog.csv (30 models)     |
+-------------------------------------------------------------------------+
                                     │
                                     ▼
+-------------------------------------------------------------------------+
|                             STAGING LAYER                               |
|   stg_verified_products (Cast types, provenance metadata, clean strings)|
+-------------------------------------------------------------------------+
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
+---------------------------------+     +---------------------------------+
|        DIMENSION TABLES         |     |           FACT TABLE            |
|   dim_manufacturer (5 OEMs)     |     |   fact_product_metrics          |
|   dim_product (30 models)       |     |   (Efficiency & power metrics)  |
+---------------------------------+     +---------------------------------+
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     ▼
+-------------------------------------------------------------------------+
|                            ANALYTICAL MARTS                             |
|   mart_competitive_analysis   (Ranks by price, range, speed, efficiency)|
|   mart_pricing_analysis       (Percentiles, quartiles, price per km/kWh)|
|   mart_product_positioning    (Price & range segmentation buckets)      |
|   kpi_status                  (14 Verified KPI metrics & benchmarks)    |
|   sql_data_quality_results    (10 Automated validation checks)          |
+-------------------------------------------------------------------------+
                                     │
                                     ▼
+-------------------------------------------------------------------------+
|                       FAIL-CLOSED PENDING LAYER                         |
|   pending.fact_ev_registrations    (0 rows - strictly pending Vahan)    |
|   pending.market_queries_template  (8 Future analytical SQL templates)  |
+-------------------------------------------------------------------------+
```

---

## 2. Technology & Compatibility Assumptions

- **SQL Engine**: DuckDB (in-process vectorized OLAP engine).
- **Driver**: Python `duckdb` (v1.0+ compatible).
- **Storage**: Local embedded database file at `data/processed/sql/e2w_sql.duckdb`.
- **Infrastructure**: Zero external server, cloud dependency, or paid licenses required.
- **Portability**: Platform-agnostic execution (Windows, Linux, macOS).

### Reproducibility Commands
To initialize and run the SQL analytics pipeline:
```bash
python src/run_sql_pipeline.py
```
To run the full automated test suite (including SQL tests):
```bash
python -m pytest -v
```

---

## 3. Warehouse Layering & Schema Definitions

### 3.1 Staging Layer
- **`stg_verified_products`**: Cleaned, strongly typed representation of the 30 verified electric two-wheeler models across 5 OEMs. Preserves audit provenance fields (`source_url`, `source_type`, `accessed_date`, `verification_status`, `provenance_class`).

### 3.2 Dimensional & Fact Model
```
  ┌────────────────────────┐                   ┌────────────────────────┐
  │    dim_manufacturer    │                   │      dim_product       │
  ├────────────────────────┤                   ├────────────────────────┤
  │ manufacturer (PK)      │1                 *│ model_name (PK)        │
  │ product_count          │───────────────────│ manufacturer (FK)      │
  │ priced_product_count   │                   │ vehicle_category       │
  │ min_price_inr          │                   │ launch_status          │
  │ max_price_inr          │                   │ source_url             │
  │ avg_price_inr          │                   │ verification_status    │
  │ median_price_inr       │                   └────────────────────────┘
  └────────────────────────┘                                │
                                                            │ 1
                                                            │
                                                            │ 1
                                               ┌────────────────────────┐
                                               │  fact_product_metrics  │
                                               ├────────────────────────┤
                                               │ model_name (PK, FK)    │
                                               │ manufacturer           │
                                               │ ex_showroom_price_inr  │
                                               │ battery_capacity_kwh   │
                                               │ range_km               │
                                               │ top_speed_kmh          │
                                               │ motor_peak_power_kw    │
                                               │ price_per_km           │
                                               │ price_per_kwh          │
                                               │ wh_per_km              │
                                               └────────────────────────┘
```

---

## 4. Analytical Marts & Window Functions

The SQL layer demonstrates advanced ANSI SQL analytical capabilities, utilizing window functions, CTEs, and partitioning to answer core business questions.

### 4.1 Competitive Analysis Mart (`mart_competitive_analysis`)
Integrates product performance, pricing, efficiency, and multi-tier rankings:
- `ROW_NUMBER() OVER (PARTITION BY manufacturer ORDER BY price ASC NULLS LAST, product)`: Identifies product positioning hierarchy within each OEM.
- `DENSE_RANK() OVER (ORDER BY price ASC NULLS LAST)`: Evaluates market-wide price hierarchy.
- `RANK() OVER (ORDER BY price_per_km ASC NULLS LAST)`: Ranks vehicles by range cost efficiency (lowest INR/km).
- `RANK() OVER (ORDER BY certified_range_km DESC NULLS LAST)`: Ranks vehicles by certified IDC range.
- `COUNT(*) OVER (PARTITION BY manufacturer)`: Dynamic portfolio breadth per OEM.
- `ROUND(100.0 * COUNT(*) OVER (PARTITION BY manufacturer) / COUNT(*) OVER (), 1)`: OEM share of available product offerings.

### 4.2 Pricing Mart (`mart_pricing_analysis`)
Evaluates market price distribution and premium positioning:
- `PERCENT_RANK() OVER (...)`: Relative price position between 0.0 (lowest) and 1.0 (highest).
- `NTILE(4) OVER (...)`: Assigns products into price quartiles (Q1 = Budget, Q4 = Premium).
- `AVG(ex_showroom_price_inr) OVER ()`: Dynamic benchmark market average price (₹124,466.14).
- `AVG(ex_showroom_price_inr) OVER (PARTITION BY manufacturer)`: OEM average price benchmark.
- Relative positioning classification: Identifies whether a model is `'below market average'`, `'above market average'`, or `'at market average'`.

### 4.3 Product Positioning Mart (`mart_product_positioning`)
Classifies models using transparent, documented business rules:
- **Price Buckets**:
  - `budget`: Price < ₹100,000 (high price sensitivity, commuter focus)
  - `mid-market`: ₹100,000 ≤ Price ≤ ₹180,000 (core adoption segment)
  - `premium`: Price > ₹180,000 (flagship / performance tier)
  - `unpriced`: Pricing not yet captured from primary verified sources
- **Range Buckets**:
  - `short-range`: Certified Range < 120 km
  - `standard-range`: 120 km ≤ Certified Range ≤ 180 km
  - `long-range`: Certified Range > 180 km
- **Battery Buckets**:
  - `compact-battery`: < 3.0 kWh
  - `standard-battery`: 3.0 kWh to 4.5 kWh
  - `high-battery`: > 4.5 kWh
- **Performance Buckets**:
  - `entry`: Top Speed < 70 km/h
  - `balanced`: 70 km/h to 90 km/h
  - `high-performance`: Top Speed > 90 km/h

---

## 5. Data Quality Validation Framework

All checks run during pipeline execution via `sql/03_data_quality.sql` and record results in `sql_data_quality_results`. The pipeline raises an exception and halts if any check fails:

| Check Name | Target Rule | Issue Count | Status |
| :--- | :--- | :---: | :---: |
| `duplicate_products` | Duplicate model names across catalog | 0 | PASS |
| `duplicate_manufacturer_model` | Duplicate OEM + model combinations | 0 | PASS |
| `null_required_fields` | Nulls in manufacturer, model, category, status | 0 | PASS |
| `negative_prices` | ex_showroom_price_inr < 0 | 0 | PASS |
| `invalid_battery_capacities` | battery_capacity_kwh ≤ 0 | 0 | PASS |
| `invalid_ranges` | range_km ≤ 0 | 0 | PASS |
| `invalid_speed_values` | top_speed_kmh ≤ 0 | 0 | PASS |
| `invalid_motor_power` | motor_peak_power_kw ≤ 0 | 0 | PASS |
| `unverified_records` | verification_status != 'verified' | 0 | PASS |
| `missing_provenance` | Missing source_url, dataset, or date | 0 | PASS |

---

## 6. Fail-Closed Market Data Architecture

In accordance with strict data integrity rules, unverified proxy registration figures are **never** converted into factual SQL analytics. 

1. **`pending.fact_ev_registrations`**:
   - Schema defined for future Vahan data ingestion: `date`, `month`, `year`, `state`, `vehicle_category`, `fuel_type`, `manufacturer`, `registrations`, `source`, `verification_status`.
   - **Current row count: 0 (Strictly empty).**
2. **`pending.market_queries_template`**:
   - Defines verified prerequisites and SQL templates for future market intelligence:
     - `annual_market_volume`
     - `monthly_market_volume`
     - `yoy_growth` (using `LAG() OVER (ORDER BY year)`)
     - `cagr` (using compound annual growth window functions)
     - `ev_penetration` (EV registrations / Total 2W registrations)
     - `oem_market_share` (using `SUM(registrations) / SUM(SUM(registrations)) OVER ()`)
     - `hhi` (Herfindahl-Hirschman Index of registration shares)
     - `state_ranking` (using `DENSE_RANK() OVER (PARTITION BY year ORDER BY registrations DESC)`)

---

## 7. Business Questions Answered by SQL

The SQL layer answers the 8 strategic questions directly from verified data:

### 1. Which manufacturers have the largest verified product portfolios?
- **Ola Electric**: 9 models (30.0% of catalog), 7 priced, avg ₹130,142.
- **Ather Energy**: 8 models (26.7% of catalog), 4 priced, avg ₹131,127.
- **TVS Motor Company**: 6 models (20.0% of catalog), 6 priced, avg ₹116,876.
- **Bajaj Auto**: 5 models (16.7% of catalog), 3 priced, avg ₹116,168.
- **Ampere (Greaves)**: 2 models (6.7% of catalog), 2 priced, avg ₹126,499.

### 2. Which products offer the best price-per-range?
Top 5 most efficient models by certified range cost (lowest ₹/km):
1. **Ola S1 X Plus Gen 3 5.2 kWh**: ₹406.25 / km (320 km range @ ₹129,999 introductory)
2. **Ola S1 X Plus Gen 3 4 kWh**: ₹500.00 / km (242 km range @ ₹120,999)
3. **TVS iQube ST 5.3 kWh**: ₹692.82 / km (212 km range @ ₹146,877)
4. **TVS iQube S 4.7 kWh**: ₹744.80 / km (175 km range @ ₹130,340)
5. **TVS iQube 3.5 kWh**: ₹760.00 / km (145 km range @ ₹110,200)

### 3. Which products are relatively expensive for their range?
Models with the highest price per certified km (least range efficiency):
1. **Ampere Nexus ST**: ₹1,314.99 / km (100 km real-world range @ ₹131,499)
2. **Ampere Nexus EX**: ₹1,214.99 / km (100 km real-world range @ ₹121,499)
3. **Ather Rizta Z 2.9 kWh**: ₹1,054.11 / km (123 km IDC range @ ₹129,656)
4. **Ather Rizta Z 3.7 kWh**: ₹941.18 / km (159 km IDC range @ ₹149,647)
5. **Ather Rizta S 2.9 kWh**: ₹879.32 / km (123 km IDC range @ ₹108,156)

### 4. Which manufacturers dominate particular product segments?
- **Budget Segment (< ₹100,000)**: Competitively contested by 3 OEMs:
  - Ola Electric: S1 X Gen 3 2 kWh (₹84,999 — market lowest price)
  - Bajaj Auto: Chetak C2501 (₹91,504)
  - TVS Motor Company: iQube 2.3 kWh (₹95,124)
- **Mid-Market Segment (₹100,000 – ₹180,000)**: Dominated by **Ola Electric** (6 models) and **TVS Motor Company** (5 models).
- **Long-Range Segment (> 180 km)**: Dominated by **Ola Electric** (3 models up to 320 km) and **TVS Motor Company** (iQube ST with 212 km).

### 5. Which products rank highest (most accessible entry price) within their manufacturer?
- **Ola Electric**: S1 X Gen 3 2 kWh (Rank 1, ₹84,999)
- **Bajaj Auto**: Chetak C2501 (Rank 1, ₹91,504)
- **TVS Motor Company**: iQube 2.3 kWh (Rank 1, ₹95,124)
- **Ather Energy**: Rizta S 2.9 kWh (Rank 1, ₹108,156)
- **Ampere**: Nexus EX (Rank 1, ₹121,499)

### 6. Which products represent potential competitive whitespace?
- **Budget + Standard Range (120–180 km under ₹100,000)**: **Completely unoccupied.** Currently, all budget models have short range (< 120 km). A product offering 120–140 km range at ₹95,000–₹99,999 represents high-potential competitive whitespace.
- **Premium Long-Range (> ₹180,000, > 200 km)**: Currently empty in the verified catalog; top models max out at ₹169,999 (Ola S1 Pro Plus 5.3 kWh).

### 7. How does product pricing vary by manufacturer?
- **Ather Energy**: ₹108,156 to ₹149,647 (Median ₹133,352; Avg ₹131,127) — positioned as a premium ecosystem player.
- **Ola Electric**: ₹84,999 to ₹169,999 (Median ₹129,999; Avg ₹130,142) — widest price span (₹85k spread) covering entry commuter to flagship performance.
- **Ampere**: ₹121,499 to ₹131,499 (Avg ₹126,499) — narrow band, centered around ₹125k.
- **TVS Motor Company**: ₹95,124 to ₹146,877 (Median ₹111,976; Avg ₹116,876) — highly disciplined progression across 6 battery tiers.
- **Bajaj Auto**: ₹91,504 to ₹134,500 (Median ₹122,500; Avg ₹116,168) — accessible entry commuter to metal-body lifestyle scooter.

### 8. Which products provide the strongest measurable value based on verified data?
Top overall value combinations (balancing low price per km, high range, and battery capacity):
1. **Ola S1 X Plus Gen 3 5.2 kWh**: ₹406.25/km, 320 km range, 5.2 kWh battery, ₹129,999.
2. **Ola S1 X Plus Gen 3 4 kWh**: ₹500.00/km, 242 km range, 4.0 kWh battery, ₹120,999.
3. **TVS iQube ST 5.3 kWh**: ₹692.82/km, 212 km range, 5.3 kWh battery, ₹146,877.
4. **TVS iQube S 4.7 kWh**: ₹744.80/km, 175 km range, 4.7 kWh battery, ₹130,340.
5. **TVS iQube 3.5 kWh**: ₹760.00/km, 145 km range, 3.5 kWh battery, ₹110,200.

---

## 8. Verified Outputs & Artifacts

All analytical outputs are exported to `data/processed/sql/`:
- `sql_competitive_analysis.csv`: 30 models with rankings, specs, and price-per-km/kWh metrics.
- `sql_pricing_analysis.csv`: 30 models with price percentiles, quartiles, and market premium comparisons.
- `sql_product_positioning.csv`: 30 models segmented by price, range, battery, and speed.
- `sql_kpi_results.csv`: 14 benchmark KPIs with calculation methodology and provenance tags.
- `sql_data_quality_results.csv`: 10 automated data quality checks (all 0 issues).
- `sql_pipeline_summary.json`: Execution metadata and verification status.
